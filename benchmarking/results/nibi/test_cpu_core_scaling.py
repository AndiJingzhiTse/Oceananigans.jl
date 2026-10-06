"""Replacement sweep configuration, physical core isolation, and scaling arithmetic."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import cpu_core_scaling as scaling


def fixture(case, config):
    entries, layout = [], []
    ry = config['partition'][1]
    for rank in range(config['ranks']):
        ix, iy = divmod(rank, ry)
        entries.append(dict(rank=rank, grid_size=[config['x_sizes'][ix], config['y_sizes'][iy], 200],
                            configuration=config, finite_state=True, metadata=dict(num_threads=config['threads_per_rank']),
                            float_type='Float64', samples=5, time_steps=10, Δt=60,
                            time_per_step_seconds=1.0, time_per_step_median_seconds=1.1,
                            time_per_step_max_seconds=1.2))
        host = rank // config['ranks_per_node']
        first_core = rank % config['ranks_per_node'] * config['threads_per_rank']
        layout.append(dict(rank=rank, hostname=f'c{host}', threads=config['threads_per_rank'],
                           cpus_per_task=config['threads_per_rank'],
                           thread_affinities=[str(first_core + i) for i in range(config['threads_per_rank'])]))
    (case / 'results.json').write_text(json.dumps(entries))
    (case / 'cpu_layout.json').write_text(json.dumps(layout))
    return entries, layout


class CPUCoreScalingTests(unittest.TestCase):
    def test_completed_jobs_do_not_require_live_queue_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            case = folder / '3_cores'
            case.mkdir()
            config = scaling.configuration(3)
            (case / 'configuration.json').write_text(json.dumps(config))
            (case / 'exit_code.txt').write_text('0\n')
            fixture(case, config)
            scaling.save_jobs(folder, [dict(cores=3, nodes=1, job_id='123', state='RUNNING', details='')])
            # Only sacct is available: Slurm has already purged the live job.
            with patch.object(scaling, 'run', return_value=SimpleNamespace(returncode=0, stdout='123|COMPLETED|0:0|None|\n')) as call:
                done, rows = scaling.refresh(folder)
                self.assertEqual(call.call_count, 1)
            self.assertTrue(done)
            self.assertEqual(rows[0]['state'], 'COMPLETED')

    def test_doubling_core_counts_and_balanced_geometry(self):
        for count in (3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072, 6144, 12288):
            config = scaling.configuration(count)
            self.assertEqual(config['ranks'], count)
            self.assertEqual(config['threads_per_rank'], 1)
            self.assertEqual(sum(config['x_sizes']), 1440)
            self.assertEqual(sum(config['y_sizes']), 720)
            self.assertLessEqual(max(config['x_sizes']) - min(config['x_sizes']), 1)
            self.assertLessEqual(max(config['y_sizes']) - min(config['y_sizes']), 1)
            self.assertGreaterEqual(min(config['x_sizes']), 7)
            self.assertGreaterEqual(min(config['y_sizes']), 7)
            self.assertFalse(config['extend_free_surface_halos'])
        with self.assertRaises(ValueError):
            scaling.configuration(24576)
        self.assertEqual(scaling.configuration(1536)['nodes'], 8)

    def test_rejects_overlapping_cpu_bindings_and_wrong_local_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp)
            config = scaling.configuration(3)
            entries, layout = fixture(case, config)
            self.assertEqual(scaling.validate(case, config), (1.0, 1.1))
            layout[1]['thread_affinities'] = layout[0]['thread_affinities']
            (case / 'cpu_layout.json').write_text(json.dumps(layout))
            with self.assertRaises(ValueError):
                scaling.validate(case, config)
            fixture(case, config)
            entries[0]['grid_size'][0] += 1
            (case / 'results.json').write_text(json.dumps(entries))
            with self.assertRaises(ValueError):
                scaling.validate(case, config)

    def test_uneven_partition_preserves_every_grid_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp)
            # Custom small fixture exercises uneven dimensions without writing
            # thousands of redundant production-rank JSON records.
            config = scaling.configuration(3)
            config.update(partition=[1, 3, 1], x_sizes=[1440], y_sizes=[239, 240, 241])
            fixture(case, config)
            self.assertEqual(scaling.validate(case, config), (1.0, 1.1))

    def test_three_core_efficiency_requires_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            row = dict(cores=6, nodes=1, ranks=6, threads_per_rank=1, partition='3x2x1',
                       resolution='1440x720x200', grid_type='LatitudeLongitudeGrid', job_id='2',
                       state='COMPLETED', fastest=0.6, median=0.65, details='Verified')
            scaling.report(folder, [row])
            self.assertNotIn('83.3%', (folder / 'plot.md').read_text())
            baseline = dict(row, cores=3, ranks=3, partition='3x1x1', fastest=1.0, median=1.1)
            scaling.report(folder, [baseline, row])
            self.assertIn('83.3% / 84.6%', (folder / 'plot.md').read_text())


if __name__ == '__main__':
    unittest.main()
