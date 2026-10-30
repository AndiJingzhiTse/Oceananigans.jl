"""Exercise the shared controller across selections, backends and adapters."""
import copy
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_suite import runner, fixture, report
from suite import workflow
from suite.execution import ADAPTER_ROOT, describe_adapter
from suite.variants import comparison_rows


class WorkflowTests(unittest.TestCase):
    def config(self, root, backend='local'):
        data = json.loads((runner.ROOT / 'server/rondeau/config.json').read_text())
        data.update(machine='testbox', backend=backend,
                    series_file=str(runner.ROOT / 'server/rondeau/series.json'),
                    cpu_cores_per_node=2, gpus_per_node=2, matplotlib=False)
        path = root / 'config.json'
        path.write_text(json.dumps(data))
        return path

    def args(self, root, config):
        return ['--study', str(root / 'study'), '--config', str(config),
                '--publish', str(root / 'results'), '--series', 'gpu_resolution']

    def test_selection_supports_every_subset_of_four_combinations(self):
        pairs = list(itertools.product(('hydrostatic', 'nonhydrostatic'), ('baseline', 'dagger')))
        for count in range(1, 5):
            for chosen in itertools.combinations(pairs, count):
                spelling = ','.join(m + ':' + mode for m, mode in chosen)
                self.assertEqual(workflow.selections(combinations=spelling),
                                 [(workflow.MODELS[m], mode) for m, mode in chosen])
        self.assertEqual(len(workflow.selections('both', 'both')), 4)
        self.assertEqual(len(workflow.selections('both', 'baseline')), 2)
        self.assertEqual(len(workflow.selections('hydrostatic', 'both')), 2)
        with self.assertRaises(ValueError):
            workflow.selections(combinations='hydrostatic:dagger,hydrostatic:dagger')

    def test_same_cli_plans_all_combinations_on_local_and_slurm(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for machine in ('rondeau', 'nibi'):
                study = root / machine
                args = [sys.executable, str(runner.ROOT / 'scripts/benchmark_suite.py'),
                        '--study', str(study), '--config', str(runner.ROOT / 'server' / machine / 'config.json'),
                        '--all', '--series', 'gpu_resolution', '--plan', '--publish', str(root / 'results')]
                result = subprocess.run(args, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                manifest = json.loads((study / 'study.json').read_text())
                self.assertEqual(len(manifest['selections']), 4)
                self.assertEqual({e['backend'] for e in manifest['selections']}, {'local' if machine == 'rondeau' else 'slurm'})
                for entry, folder, data in workflow.load_studies(manifest):
                    self.assertEqual(len(data['cases']), 2 if machine == 'rondeau' else 3)
                    self.assertEqual({c['state'] for c in data['cases']}, {'PLANNED'})
                    request = data['resource_requests'][0]['submission']
                    self.assertEqual(request[0], 'bash' if machine == 'rondeau' else 'sbatch')
                    command = (folder / data['cases'][0]['id'] / 'command.txt').read_text()
                    self.assertEqual('srun' in command, machine != 'rondeau')
                    self.assertTrue((folder / 'run_metadata/src/suite/adapter/adapter.jl').exists())
                    descriptor = data['cases'][0]['configuration']['execution_adapter']
                    self.assertEqual(descriptor['mode'], entry['mode'])
                self.assertFalse(any(study.rglob('job.out')))
            self.assertFalse((root / 'results').exists())

    def test_local_executes_without_slurm_and_uses_shared_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = self.config(root)
            mpi = root / 'mpi.sh'
            mpi.write_text('#!/bin/bash\nwhile [[ "$1" != bash ]]; do shift; done\nexec "$@"\n')
            julia = root / 'fake-julia'
            julia.write_text('#!/usr/bin/env python3\nimport json,sys\nfrom pathlib import Path\n'
                             'if sys.argv[1:]==["--version"]: print("Synthetic worker"); raise SystemExit\n'
                             f'sys.path.insert(0,{str(runner.ROOT / "test")!r})\n'
                             'from test_suite import fixture\n'
                             'p=Path(sys.argv[-1]); fixture(p,json.loads((p/"configuration.json").read_text()))\n')
            julia.chmod(0o700)
            data = json.loads(config.read_text())
            data.update(mpi=['bash', str(mpi)], julia=str(julia))
            config.write_text(json.dumps(data))
            original = runner.command
            def command(args, **kwargs):
                if args[0] in ('sbatch', 'srun', 'sacct', 'squeue'):
                    raise AssertionError('A local run must not use Slurm')
                if args[0] == 'nvidia-smi':
                    output = '0, GPU-0, 5\n' if '--query-gpu=index,uuid,memory.used' in args else 'GPU-0\n' if '--query-gpu=uuid' in args else ''
                    return SimpleNamespace(returncode=0, stdout=output)
                return original(args, **kwargs)
            with patch.object(runner, 'command', side_effect=command):
                workflow.main(runner, self.args(root, config) + ['--modes', 'both', '--execute'])
            manifest = json.loads((root / 'study/study.json').read_text())
            self.assertEqual(manifest['state'], 'COMPLETED')
            self.assertEqual(manifest['outcomes'], {'COMPLETED': 4})
            self.assertTrue(all(v == ['GPU-0'] for v in manifest['allocations'].values()))
            for _, folder, data in workflow.load_studies(manifest):
                self.assertFalse(any((folder / '.runtime').glob('*')))
                self.assertTrue(all(c['configuration']['execution_adapter']['source_sha256'] for c in data['cases']))
            compared = comparison_rows(root / 'results/hydrostatic_free_surface_models/testbox', ('gpu_resolution',))
            self.assertTrue(all(r['speedup_median'] == 1 for r in compared))

    def test_slurm_submission_resume_and_finalizer_refresh_share_workflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = self.config(root, 'slurm')
            submissions = []
            original = runner.command
            def command(args, **kwargs):
                if args[0] == 'sbatch':
                    submissions.append(args)
                    return SimpleNamespace(returncode=0, stdout=str(1000 + len(submissions)) + '\n')
                if args[0] in ('sacct', 'squeue'):
                    return SimpleNamespace(returncode=0, stdout='')
                return original(args, **kwargs)
            with patch.object(runner, 'command', side_effect=command):
                workflow.main(runner, self.args(root, config) + ['--modes', 'both', '--execute'])
                manifest = json.loads((root / 'study/study.json').read_text())
                self.assertEqual(manifest['state'], 'SUBMITTED')
                self.assertEqual(len(submissions), 6)  # Four cases plus two report finalizers.
                for _, folder, data in workflow.load_studies(manifest):
                    finalizer = (folder / 'run_metadata/finalize.sh').read_text()
                    self.assertIn('--study', finalizer)
                    self.assertIn('--refresh', finalizer)
                    self.assertTrue(all(c['job_id'] for c in data['cases']))
                    for case in data['cases']:
                        (folder / '.runtime' / case['id'] / 'mpi_session').write_text('Runtime evidence')
                workflow.main(runner, ['--study', str(root / 'study'), '--resume'])
                self.assertEqual(len(submissions), 6, 'Resume must not submit queued cases twice')
                for _, folder, data in workflow.load_studies(manifest):
                    for case in data['cases']:
                        self.assertTrue((folder / '.runtime' / case['id'] / 'mpi_session').exists())
                        fixture(folder / case['id'], case['configuration'])
                workflow.main(runner, ['--study', str(root / 'study'), '--refresh'])
            final = json.loads((root / 'study/study.json').read_text())
            self.assertEqual(final['state'], 'COMPLETED')
            self.assertEqual(final['outcomes'], {'COMPLETED': 4})
            for _, folder, _ in workflow.load_studies(final):
                self.assertFalse(any((folder / '.runtime').glob('*')))

    def test_repeated_profile_plans_use_distinct_capture_paths(self):
        import shlex
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = self.config(root)
            captures = []
            for index in (1, 2):
                study = root / f'study{index}'
                workflow.main(runner, ['--study', str(study), '--config', str(config), '--plan',
                                      '--series', 'gpu_nsight_scaling_default', '--publish', str(root / 'results')])
                manifest = json.loads((study / 'study.json').read_text())
                _, folder, data = workflow.load_studies(manifest)[0]
                captures.append(shlex.split((folder / data['cases'][0]['id'] / 'command.txt').read_text())[-2])
            self.assertNotEqual(*captures)
            self.assertTrue(all('/raw_profiles/' in path for path in captures))

    def test_dagger_only_plan_does_not_add_baseline_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow.main(runner, self.args(root, self.config(root)) + ['--models', 'both', '--modes', 'dagger', '--plan'])
            manifest = json.loads((root / 'study/study.json').read_text())
            self.assertEqual(len(manifest['selections']), 2)
            self.assertEqual({e['mode'] for e in manifest['selections']}, {'dagger'})
            self.assertFalse(any((root / 'study').glob('*/testbox/baseline/*/suite.json')))
            with self.assertRaisesRegex(ValueError, 'saved selections'):
                workflow.main(runner, ['--study', str(root / 'study'), '--models', 'both', '--resume'])

    def test_adapter_replacement_is_captured_and_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adapter = root / 'replacement'
            shutil.copytree(ADAPTER_ROOT / 'baseline', adapter)
            info = json.loads((adapter / 'adapter.json').read_text())
            info.update(mode='dagger', id='replacement', version='2')
            (adapter / 'adapter.json').write_text(json.dumps(info))
            config = self.config(root)
            workflow.main(runner, self.args(root, config) + ['--modes', 'dagger', '--dagger-adapter', str(adapter), '--plan'])
            manifest = json.loads((root / 'study/study.json').read_text())
            _, folder, data = workflow.load_studies(manifest)[0]
            planned = data['cases'][0]['configuration']['execution_adapter']
            self.assertEqual(planned['id'], 'replacement')
            self.assertEqual(planned['version'], '2')
            (adapter / 'adapter.jl').write_text('Replacement source changed after capture')
            workflow.verify_source(root / 'study')  # Original adapter is no longer a dependency.
            captured = folder / 'run_metadata/src/suite/adapter/adapter.jl'
            captured.write_text('Captured source changed')
            with self.assertRaisesRegex(RuntimeError, 'captured worker'):
                workflow.verify_source(root / 'study')

    def test_comparisons_require_timing_contract_and_use_retained_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = self.config(root)
            workflow.main(runner, self.args(root, config) + ['--modes', 'both', '--plan'])
            manifest = json.loads((root / 'study/study.json').read_text())
            for entry, folder, data in workflow.load_studies(manifest):
                for case in data['cases']:
                    fixture(folder / case['id'], case['configuration'])
                    case['measurement'] = report.validate(folder / case['id'], case['configuration'])
                    case['state'] = 'COMPLETED'
                runner.atomic_json(folder / 'suite.json', data)
            studies = workflow.load_studies(manifest)
            workflow.update(runner, root / 'study', manifest, studies, publish=True)
            model_root = Path(studies[0][0]['folder']).parent
            rows = comparison_rows(model_root, ('gpu_resolution',))
            self.assertEqual(rows[0]['speedup_median'], 1)
            baseline = model_root / 'baseline/gpu_resolution/suite.json'
            baseline.unlink()
            references = root / 'results/hydrostatic_free_surface_models/testbox'
            rows = comparison_rows(model_root, ('gpu_resolution',), references)
            self.assertEqual(rows[0]['speedup_median'], 1)
            self.assertIn('results', rows[0]['baseline_source'])
            dagger = model_root / 'dagger/gpu_resolution/suite.json'
            data = json.loads(dagger.read_text())
            data['cases'][0]['configuration']['execution_adapter']['timing_contract'] = 'different-workload/v1'
            runner.atomic_json(dagger, data)
            rows = comparison_rows(model_root, ('gpu_resolution',), references)
            self.assertEqual(rows[0]['speedup_median'], '')
            self.assertIn('Incompatible', rows[0]['details'])

    def test_validation_rejects_wrong_execution_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            server = runner.load_server(runner.ROOT / 'server/rondeau/config.json')
            config = runner.build_plan(server, ('gpu_resolution',))[0]['configuration']
            config['execution_adapter'] = describe_adapter(server)
            entries = fixture(root, config)
            entries[0]['metadata']['execution_adapter'] = dict(config['execution_adapter'], id='wrong')
            (root / 'results.json').write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError, 'adapter provenance'):
                report.validate(root, config)


if __name__ == '__main__':
    unittest.main()
