"""Server plans implement the requested workloads for all four run variants."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_suite import runner, plan, report
from suite.servers import GPU_SERIES, load_series
from suite.variants import comparison_rows, write_comparison


class ServerPlanTests(unittest.TestCase):
    def test_exact_server_workloads_for_both_models_and_variants(self):
        for machine in ('rondeau', 'nibi', 'rorqual', 'fir'):
            local = machine == 'rondeau'
            counts = [1, 2, 4] if local else [1, 2, 4, 8, 16]
            grids = ['default', 'fine'] if local else ['default', 'fine', 'super_fine']
            partitions = [] if local else [[16, 1, 1], [8, 2, 1], [4, 4, 1], [2, 8, 1]]
            expected_series = tuple(s for s in GPU_SERIES if not local or s != 'gpu_partition_fine')
            physical_workloads = []
            for model in plan.MODEL_FOLDERS:
                variants = []
                for mode in ('baseline', 'dagger'):
                    with self.subTest(machine=machine, model=model, mode=mode):
                        server = runner.load_server(runner.ROOT / 'server' / machine / 'config.json', model)
                        server['execution_mode'] = mode
                        cases = plan.build_plan(server)
                        self.assertEqual(plan.machine_series(server), expected_series)
                        self.assertEqual(len(cases), 16 if local else 30)
                        grouped = {s: [c for c in cases if c['series'] == s] for s in GPU_SERIES}
                        self.assertEqual([c['grid_name'] for c in grouped['gpu_resolution']], grids)
                        self.assertTrue(all(c['ranks'] == 1 for c in grouped['gpu_resolution']))
                        for prefix in ('gpu_scaling_', 'gpu_nsight_scaling_'):
                            for grid in ('default', 'fine'):
                                selected = grouped[prefix + grid]
                                self.assertEqual([c['ranks'] for c in selected], counts)
                                self.assertTrue(all(c['configuration']['global_resolution'] == plan.GRIDS[grid]
                                                    for c in selected))
                                self.assertEqual({c['configuration']['profile'] for c in selected},
                                                 {prefix == 'gpu_nsight_scaling_'})
                        self.assertEqual([c['partition'] for c in grouped['gpu_partition_fine']], partitions)
                        if local:
                            with self.assertRaisesRegex(ValueError, 'not configured'):
                                plan.build_plan(server, ('gpu_partition_fine',))
                        weak = grouped['gpu_weak_scaling']
                        self.assertEqual([(c['grid_name'], c['ranks']) for c in weak], list(zip(grids, [1, 4, 16])))
                        for case, seconds in zip(weak, (1, 2, 4)):
                            case.update(state='COMPLETED', measurement=dict(fastest=seconds, median=seconds))
                            self.assertEqual(report.efficiencies(case, weak[0]), (1, 1))
                        variants.append([{k: v for k, v in c.get('configuration', {}).items()
                                          if k != 'execution_mode'} for c in cases])
                        physical_workloads.append([(c['id'], c['grid_name'], c['ranks'], c['partition']) for c in cases])
                        self.assertTrue(all(c['configuration']['execution_mode'] == mode
                                            for c in cases if 'configuration' in c))
                self.assertEqual(*variants)
            self.assertTrue(all(p == physical_workloads[0] for p in physical_workloads))

    def test_cluster_fine_partitions_are_feasible_and_exclude_removed_case(self):
        for machine in ('nibi', 'rorqual', 'fir'):
            server = runner.load_server(runner.ROOT / 'server' / machine / 'config.json')
            cases = plan.build_plan(server, ('gpu_partition_fine',))
            self.assertEqual(len(cases), 4)
            self.assertEqual([c['state'] for c in cases], ['PLANNED'] * 4)
            self.assertNotIn([1, 16, 1], [c['partition'] for c in cases])

    def test_capacity_reductions_preserve_requested_counts_without_extra_cases(self):
        server = runner.load_server(runner.ROOT / 'server/nibi/config.json')
        server['max_gpus'] = 2
        cases = plan.build_plan(server, ('gpu_scaling_default',))
        self.assertEqual([c['ranks'] for c in cases], [1, 2, 4, 8, 16])
        self.assertEqual([c['state'] for c in cases], ['PLANNED'] * 2 + ['RESOURCE_LIMIT'] * 3)
        with self.assertRaisesRegex(ValueError, 'not configured'):
            plan.build_plan(server, ('gpu_scaling_super_fine',))

    def test_relative_series_path_and_loaded_workloads_survive_file_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = runner.ROOT / 'server/rondeau'
            (root / 'series.json').write_text((source / 'series.json').read_text())
            (root / 'config.json').write_text((source / 'config.json').read_text())
            server = runner.load_server(root / 'config.json')
            self.assertEqual(server['series_file'], str(root / 'series.json'))
            original = plan.build_plan(server)
            (root / 'series.json').write_text('{}')
            self.assertEqual(plan.build_plan(server), original)
            frozen = json.loads(json.dumps(server))
            self.assertEqual(plan.build_plan(frozen), original)

    def test_schema_rejects_duplicate_gpu_counts_and_mismatched_partitions(self):
        original = json.loads((runner.ROOT / 'server/rondeau/series.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'series.json'
            for key, value in [('gpus', [1, 1, 4]), ('gpus', [1, -2, 4])]:
                data = copy.deepcopy(original)
                data['series']['gpu_scaling_default'][key] = value
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'GPU counts'):
                    load_series(path)
            data = copy.deepcopy(original)
            data['series']['gpu_weak_scaling']['cases'][1]['partition'] = [1, 2, 1]
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'partition'):
                load_series(path)

    def test_comparison_uses_actual_server_and_weak_sequence(self):
        server = runner.load_server(runner.ROOT / 'server/nibi/config.json')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(runner, 'snapshot'):
                runner.prepare(root / 'baseline/gpu_weak_scaling', server, ('gpu_weak_scaling',))
            write_comparison(root, root / 'published', plotting=False,
                             selected=('gpu_weak_scaling',), model_type='HydrostaticFreeSurfaceModel', machine='nibi')
            text = (root / 'published/comparison.md').read_text()
            self.assertIn('# Nibi: hydrostatic', text)
            self.assertIn('720 × 360 × 100 on 4 GPU(s)', text)
            self.assertIn('1440 × 720 × 200 on 16 GPU(s)', text)
            self.assertIn('3,240,000, 6,480,000, 12,960,000', text)
            self.assertNotIn('51,840,000', text)


if __name__ == '__main__':
    unittest.main()
