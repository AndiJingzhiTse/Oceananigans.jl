"""Matched variant comparisons must never turn failures into speedups."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from test_suite import runner, plan
from suite.variants import comparison_rows, write_comparison
from compare_dagger import annotate_failures


class VariantTests(unittest.TestCase):
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
            self.assertEqual({c['series'] for c in cases}, set(plan.SERIES))
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


if __name__ == '__main__':
    unittest.main()
