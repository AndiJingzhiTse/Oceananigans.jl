"""Constant-work geometry, physics, reporting and FFT acceptance checks."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from test_suite import runner, plan, report, fixture
from suite.servers import load_series


class Weak512Tests(unittest.TestCase):
    config_path = runner.ROOT / 'server/fir/weak512_config.json'

    def test_both_models_keep_cells_spacing_and_timestep_fixed(self):
        for model in plan.MODEL_FOLDERS:
            server = runner.load_server(self.config_path, model, 'baseline')
            cases = plan.build_plan(server)
            self.assertEqual(len(cases), 5)
            for case, n in zip(cases, (1, 2, 4, 8, 16)):
                cfg = case['configuration']
                self.assertEqual(case['state'], 'PLANNED')
                self.assertEqual(cfg['global_resolution'], [512*n, 512, 512])
                self.assertEqual(cfg['partition'], [n, 1, 1])
                self.assertEqual(cfg['x_sizes'], [512]*n)
                self.assertEqual(cfg['y_sizes'], [512])
                self.assertEqual(cfg['domain_extent_m'], [512000*n, 512000, 5120])
                self.assertEqual(cfg['dt'], 10)
                self.assertEqual(cfg['tracers'], ['b'])
                self.assertIsNone(cfg['closure'])
                self.assertEqual(cfg['momentum_advection'], 'WENO5')
                self.assertEqual(cfg['execution_mode'], 'baseline')
                self.assertFalse(cfg['profile'])
                self.assertEqual(cfg['scaling_type'], 'weak')
                request = runner.sbatch_command(server, [case], Path('/allocation.sh'))
                self.assertIn('--gpus-per-task=h100:1', request)
                self.assertNotIn('--exclusive', request)
                if model == 'NonhydrostaticModel':
                    self.assertEqual(cfg['pressure_solver'], 'DistributedFFTBasedPoissonSolver')
                    self.assertIsNone(cfg['pressure_preconditioner'])

    def test_schema_rejects_inconsistent_constant_work(self):
        original = json.loads(self.config_path.with_name('weak512_series.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'series.json'
            for size, label in (([1024, 512, 256], '1024x512x256'),
                                ([1024, 512, 512], 'wrong'),
                                ([1024, 512, -1], '1024x512x-1')):
                data = copy.deepcopy(original)
                data['series']['gpu_weak_scaling_512_x']['cases'][1].update(global_resolution=size, grid=label)
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_series(path)

    def test_fft_acceptance_requires_small_finite_divergence(self):
        server = runner.load_server(self.config_path, 'NonhydrostaticModel')
        cfg = plan.build_plan(server)[0]['configuration']
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            entries = fixture(folder, cfg)
            entry = entries[0]
            entry.update(pressure_solver=cfg['pressure_solver'], pressure_solves=None,
                         pressure_projection_validation=dict(passed=True, maximum_divergence_per_second=1e-15,
                                                             tolerance_per_second=1e-10))
            (folder / 'results.json').write_text(json.dumps(entries))
            self.assertGreater(report.validate(folder, cfg)['median'], 0)
            for divergence in (1e-6, float('nan'), -1e-6):
                entry['pressure_projection_validation']['maximum_divergence_per_second'] = divergence
                (folder / 'results.json').write_text(json.dumps(entries))
                with self.assertRaisesRegex(ValueError, 'projection'):
                    report.validate(folder, cfg)

    def test_reports_use_actual_grid_and_constant_time_reference(self):
        server = runner.load_server(self.config_path)
        cases = plan.build_plan(server)
        for case in cases:
            case.update(state='COMPLETED', measurement=dict(fastest=1, median=2, retained_substeps=[21]))
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            report.write_report(folder, cases, plotting=True)
            content = (folder / 'plot.md').read_text()
            self.assertIn('RectilinearGrid', content)
            self.assertIn('Δt=10', content)
            self.assertNotIn('T/S', content)
            self.assertIn('Ideal: constant time', (folder / 'gpu_weak_scaling_512_x.svg').read_text())
            self.assertIn('134,217,728', content)
            self.assertEqual(report.efficiencies(cases[-1], cases[0]), (1, 1))


if __name__ == '__main__':
    unittest.main()
