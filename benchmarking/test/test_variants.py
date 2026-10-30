"""Matched variant comparisons must never turn failures into speedups."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_suite import runner, plan
from suite.variants import comparison_rows, write_comparison
from compare_dagger import annotate_failures
import compare_dagger


class VariantTests(unittest.TestCase):
    def test_automatic_commits_include_new_metadata_but_exclude_raw_profiles(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(['git', 'init', '-q', '-b', 'main', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'config', 'user.name', 'Benchmark test'], check=True)
            subprocess.run(['git', '-C', str(root), 'config', 'user.email', 'benchmark@example.invalid'], check=True)
            (root / '.gitignore').write_text('*.json\n*.md\n')
            subprocess.run(['git', '-C', str(root), 'add', '.gitignore'], check=True)
            subprocess.run(['git', '-C', str(root), 'commit', '-qm', 'Initial'], check=True)
            destination = root / 'results/hydrostatic_free_surface_models/rondeau'
            case = destination / 'baseline/gpu_resolution/default'
            case.mkdir(parents=True)
            (case / 'results.json').write_text('{}')
            raw = destination / 'baseline/gpu_resolution/raw_profiles'
            raw.mkdir()
            (raw / 'capture.json').write_text('must remain untracked')
            (root / 'user.txt').write_text('Unrelated user work')
            with patch.object(runner, 'REPO', root):
                compare_dagger.commit_records(destination)
            tracked = subprocess.check_output(['git', '-C', str(root), 'ls-files'], text=True)
            self.assertIn('default/results.json', tracked)
            self.assertNotIn('capture.json', tracked)
            self.assertNotIn('user.txt', tracked)

    def test_source_change_records_a_stopped_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(compare_dagger, 'source_fingerprint', return_value={'src': 'changed'}):
                with self.assertRaises(RuntimeError):
                    compare_dagger.verify_source({'src': 'original'}, root)
            self.assertEqual(json.loads((root / 'progress.json').read_text())['state'], 'STOPPED_SOURCE_CHANGE')

    def test_hydrostatic_gpu_only_plan_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / 'hydrostatic_free_surface_models/rondeau'
            output.mkdir(parents=True)
            (output / 'plot.md').write_text('Previously accepted results\n')
            args = ['compare_dagger.py', '--config', str(runner.ROOT / 'scripts/configs/rondeau.json'),
                    '--project', str(root / 'environment'), '--study', str(root / 'study'),
                    '--publish', str(output), '--model', 'HydrostaticFreeSurfaceModel', '--gpu-only', '--plan']
            with patch('sys.argv', args), patch.object(runner, 'snapshot'):
                compare_dagger.main()
            expected = {s for s in plan.SERIES if s.startswith('gpu_')}
            rows = comparison_rows(root / 'study')
            self.assertEqual({r['series'] for r in rows}, expected)
            self.assertEqual(len(expected), 7)
            for path in (root / 'study').glob('*/*/suite.json'):
                data = json.loads(path.read_text())
                self.assertEqual(data['server']['model_type'], 'HydrostaticFreeSurfaceModel')
                self.assertTrue(all(c['configuration']['model_type'] == 'HydrostaticFreeSurfaceModel'
                                    for c in data['cases'] if 'configuration' in c))
                self.assertTrue(all(c['configuration']['free_surface'] == 'SplitExplicitFreeSurface'
                                    for c in data['cases'] if 'configuration' in c))
                self.assertTrue(all(c['configuration']['initial_condition_seed'] == 1234
                                    for c in data['cases'] if 'configuration' in c))
            self.assertEqual((output / 'previous_results.md').read_text(), 'Previously accepted results\n')
            self.assertIn('# Rondeau: hydrostatic baseline', (output / 'comparison.md').read_text())
            self.assertFalse((root / 'study/baseline/cpu_resolution').exists())
            self.assertNotIn('four independent single-GPU simulations', (output / 'comparison.md').read_text())

    def test_idle_gpu_selection_rejects_occupied_devices(self):
        from types import SimpleNamespace
        responses = [SimpleNamespace(returncode=0, stdout='0, GPU-a, 5\n1, GPU-b, 4096\n2, GPU-c, 5\n3, GPU-d, 5\n'),
                     SimpleNamespace(returncode=0, stdout='GPU-b\nGPU-d\n')]
        with patch.object(runner, 'command', side_effect=responses), patch.dict('os.environ', {}, clear=True):
            self.assertEqual(compare_dagger.free_gpu_uuids(), ['GPU-a', 'GPU-c'])
        responses = [SimpleNamespace(returncode=0, stdout='0, GPU-a, 5\n2, GPU-c, 5\n'),
                     SimpleNamespace(returncode=0, stdout='')]
        with patch.object(runner, 'command', side_effect=responses), patch.dict('os.environ', {'CUDA_VISIBLE_DEVICES': '2'}, clear=True):
            self.assertEqual(compare_dagger.free_gpu_uuids(), ['GPU-c'])

    def test_pending_pairs_prioritize_smaller_allocations_and_skip_terminal_cases(self):
        studies = {}
        for mode in ('baseline', 'dagger'):
            studies[mode, 'gpu_scaling_super_fine'] = (Path('/unused'), {'cases': [
                dict(id='4_ranks', ranks=4, state='PLANNED'),
                dict(id='2_ranks', ranks=2, state='PLANNED'),
                dict(id='1_ranks', ranks=1, state='COMPLETED'),
                dict(id='8_ranks', ranks=8, state='RESOURCE_LIMIT')]})
        pairs = compare_dagger.pending_pairs(studies, ('gpu_scaling_super_fine',))
        self.assertEqual([p[0] for p in pairs], [2, 4])

    def test_paired_plan_creates_empty_variant_destinations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = ['compare_dagger.py', '--config', str(runner.ROOT / 'scripts/configs/rondeau.json'),
                    '--project', str(root / 'environment'), '--study', str(root / 'study'),
                    '--publish', str(root / 'results'), '--plan']
            with patch('sys.argv', args), patch.object(runner, 'snapshot'):
                compare_dagger.main()
            for mode in ('baseline', 'dagger'):
                self.assertTrue((root / 'results' / mode / 'plot.md').exists())
                self.assertTrue((root / 'results' / mode / 'status.json').exists())
            rows = comparison_rows(root / 'study')
            self.assertEqual({r['series'] for r in rows}, set(plan.RONDEAU_SERIES))

    def test_nested_gpu_memory_error_is_reported_after_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / 'default').mkdir()
            (folder / 'default/job.out').write_text('ERROR: LoadError: TaskFailedException\nOut of GPU memory trying to allocate\n')
            data = {'cases': [{'id': 'default', 'state': 'FAILED', 'details': 'Execution exit 1'}]}
            annotate_failures(folder, data)
            case = data['cases'][0]
            self.assertEqual(case['state'], 'OUT_OF_MEMORY')
            self.assertIn('Out of GPU memory', case['details'])
            annotate_failures(folder, data)
            self.assertEqual(case['details'].count('Execution failed'), 1)

    def test_execution_mode_reaches_every_configuration(self):
        server = runner.load_server(runner.ROOT / 'scripts/configs/rondeau.json', 'NonhydrostaticModel')
        for mode in ('baseline', 'dagger'):
            server['execution_mode'] = mode
            cases = plan.build_plan(server)
            self.assertEqual({c['series'] for c in cases}, set(plan.RONDEAU_SERIES))
            self.assertTrue(all(c['configuration']['execution_mode'] == mode
                                for c in cases if 'configuration' in c))

    def test_ratios_require_completed_matching_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / 'study'
            for mode, elapsed in (('baseline', 2.0), ('dagger', 1.0)):
                path = study / mode / 'cpu_resolution'
                path.mkdir(parents=True)
                config = plan.configuration('cpu_resolution', 1, model_type='NonhydrostaticModel')
                config['execution_mode'] = mode
                case = dict(id='default', series='cpu_resolution', ranks=1, configuration=config,
                            state='COMPLETED', measurement={'fastest': elapsed, 'median': elapsed * 1.2})
                failed = copy.deepcopy(case)
                failed.update(id='fine', state='FAILED', details='Pressure solver did not converge')
                mismatch = copy.deepcopy(case)
                mismatch['id'] = 'super_fine'
                if mode == 'dagger':
                    mismatch['configuration']['dt'] = 30
                (path / 'suite.json').write_text(json.dumps({'cases': [case, failed, mismatch]}))
            rows = {r['case']: r for r in comparison_rows(study)}
            self.assertAlmostEqual(rows['default']['speedup_median'], 2)
            self.assertEqual(rows['fine']['speedup_median'], '')
            self.assertEqual(rows['super_fine']['speedup_median'], '')
            output = Path(tmp) / 'published'
            write_comparison(study, output, plotting=True)
            text = (output / 'comparison.md').read_text()
            self.assertTrue(all(f'## {s}' in text for s in plan.SERIES))
            self.assertIn('Pressure solver did not converge', text)
            self.assertTrue((output / 'dagger/status.json').is_file())
            self.assertIn('Equal time (1)', (output / 'comparisons/cpu_resolution.svg').read_text())

    def test_rondeau_reduced_plan_and_increasing_load_reference(self):
        from suite.report import efficiencies
        server = dict(machine='rondeau', model_type='NonhydrostaticModel', max_cpu_cores=128, max_gpus=4)
        cases = plan.build_plan(server)
        self.assertEqual(tuple(dict.fromkeys(c['series'] for c in cases)), plan.RONDEAU_SERIES)
        self.assertEqual(cases[0]['series'], 'gpu_weak_scaling')
        self.assertEqual(len(cases), 14)
        self.assertTrue(all(c['series'].startswith('gpu_') for c in cases))
        weak = [c for c in cases if c['series'] == 'gpu_weak_scaling']
        self.assertEqual([(c['ranks'], c['configuration']['global_resolution']) for c in weak],
                         [(1, [360,180,50]), (2, [720,360,100]), (4, [1440,720,200])])
        for case, seconds in zip(weak, (1, 4, 16)):
            case.update(state='COMPLETED', measurement=dict(fastest=seconds, median=seconds))
            self.assertEqual(efficiencies(case, weak[0]), (1, 1))
        for name, grid in (('gpu_scaling_fine', 'fine'), ('gpu_nsight_scaling_default','default')):
            selected = [c for c in cases if c['series']==name]
            self.assertEqual([c['ranks'] for c in selected], [1,2,4])
            self.assertTrue(all(c['configuration']['global_resolution']==plan.GRIDS[grid] for c in selected))
            self.assertEqual({c['configuration']['profile'] for c in selected}, {'nsight' in name})

    def test_cpu_rank_disables_cuda_before_starting_julia(self):
        import os, subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'configuration.json').write_text(json.dumps(dict(device='CPU',profile=False)))
            fake = root/'fake-julia'
            fake.write_text('#!/bin/bash\nprintf "visible=%s\\n" "$CUDA_VISIBLE_DEVICES"\n')
            fake.chmod(0o700)
            result = subprocess.run(['bash',str(runner.ROOT/'src/suite/rank.sh'), str(root),str(root),
                                     'worker.jl',str(root/'profiles'),str(fake)],
                                    env=dict(os.environ,CUDA_VISIBLE_DEVICES='0,1,2,3'),capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(result.stdout.strip(),'visible=')
            (root/'configuration.json').write_text(json.dumps(dict(device='GPU',profile=False)))
            result = subprocess.run(['bash',str(runner.ROOT/'src/suite/rank.sh'), str(root),str(root),
                                     'worker.jl',str(root/'profiles'),str(fake)],
                                    env=dict(os.environ,CUDA_VISIBLE_DEVICES='2,3'),capture_output=True,text=True)
            self.assertEqual(result.stdout.strip(),'visible=2,3')

    def test_paired_profiles_use_retained_series_folder(self):
        server=runner.load_server()
        server['profile_layout']='series'
        cfg=plan.configuration('gpu_nsight_scaling_default',1,'default')
        command=runner.launch_command(server,cfg,Path('/study/1_ranks'),Path('/metadata'),Path('/results/baseline'))
        self.assertEqual(command[-2],'/results/baseline/gpu_nsight_scaling_default/raw_profiles/1_ranks')


if __name__ == '__main__':
    unittest.main()
