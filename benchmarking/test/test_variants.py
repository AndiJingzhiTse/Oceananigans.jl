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
        self.assertEqual(len(cases), 12)
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
