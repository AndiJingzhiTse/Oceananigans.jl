"""Validate profile artifacts and reporting with temporary fixtures, without GPUs."""
import csv
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import nsight_series as series


def fixture(case, gpus, partition):
    case.mkdir(parents=True)
    config = series.config_for(gpus, partition)
    entries = [dict(rank=r, grid_size=config['local_resolution'], float_type='Float64',
                    samples=5, time_steps=10, Δt=60, time_per_step_seconds=0.25,
                    time_per_step_median_seconds=0.26, time_per_step_max_seconds=0.3,
                    metadata={'num_threads': 1}, configuration=config, finite_state=True)
               for r in range(gpus)]
    (case / 'results.json').write_text(json.dumps(entries))
    (case / 'gpu_layout.json').write_text(json.dumps([
        dict(rank=r, hostname='gpu-node', gpu_uuid=f'GPU-{r}') for r in range(gpus)]))
    for rank in range(gpus):
        destination = case / f'rank_{rank}'
        destination.mkdir()
        trace = destination / 'fixture.nsys-rep'
        trace.write_bytes(b'unit-test fixture, not a real trace')
        (destination / 'trace_path.txt').write_text(str(trace))
        (destination / 'trace_bytes.txt').write_text(str(trace.stat().st_size))
        (destination / 'trace_sha256.txt').write_text(hashlib.sha256(trace.read_bytes()).hexdigest())
        (destination / 'exit_code.txt').write_text('0')
        (destination / 'summary_cuda_gpu_kern_sum.csv').write_text(
            'Total Time (ns),Instances,Name\n100,5,gpu_compute_hydrostatic_free_surface_Gc_kernel\n'
            '200,10,compute_hydrostatic_free_surface_Gu!\n300,5,compute_hydrostatic_free_surface_Gv!\n400,3,halo_kernel\n')
    (case / 'finished.txt').write_text('finished')
    (case / 'exit_code.txt').write_text('0')


class NsightTests(unittest.TestCase):
    def test_all_six_layouts_preserve_global_grid(self):
        count = 0
        for gpus, partitions in series.CASES.items():
            for partition in partitions:
                config = series.config_for(gpus, partition)
                self.assertEqual([a*b for a,b in zip(config['partition'], config['local_resolution'])], [1440,720,200])
                count += 1
        self.assertEqual(count, 6)
        for invalid in ('0x1x1', '2x1', '3x1x1'):
            with self.assertRaises(ValueError):
                series.config_for(2, invalid)

    def test_validates_every_rank_and_aggregates_kernels(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / 'case'
            fixture(case, 2, '2x1x1')
            fastest, median, totals = series.validate(case, 2, '2x1x1')
            self.assertEqual((fastest, median), (0.25, 0.26))
            self.assertEqual(totals, dict(Gc=200, Gu=400, Gv=600, Others=800))
            (case / 'rank_1/fixture.nsys-rep').unlink()
            with self.assertRaises(OSError):
                series.validate(case, 2, '2x1x1')

    def test_rejects_duplicate_gpus_and_nonfinite_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / 'case'
            fixture(case, 2, '1x2x1')
            layout = json.loads((case / 'gpu_layout.json').read_text())
            layout[1]['gpu_uuid'] = layout[0]['gpu_uuid']
            (case / 'gpu_layout.json').write_text(json.dumps(layout))
            with self.assertRaises(ValueError):
                series.validate(case, 2, '1x2x1')
            layout[1]['gpu_uuid'] = 'GPU-1'
            (case / 'gpu_layout.json').write_text(json.dumps(layout))
            entries = json.loads((case / 'results.json').read_text())
            entries[1]['finite_state'] = False
            (case / 'results.json').write_text(json.dumps(entries))
            with self.assertRaises(ValueError):
                series.validate(case, 2, '1x2x1')

    def test_partial_failure_retains_completed_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            fixture(folder / '4_gpus/4x1x1', 4, '4x1x1')
            failed = folder / '4_gpus/2x2x1'
            failed.mkdir()
            (failed / 'finished.txt').write_text('finished')
            (failed / 'exit_code.txt').write_text('1')
            (folder / '4_gpus/1x4x1').mkdir()
            jobs = [dict(gpus=4, partitions=list(series.CASES[4]), job_id='123', state='SUBMITTED', details='')]
            (folder / 'jobs.json').write_text(json.dumps(jobs))
            with patch.object(series, 'run', return_value=SimpleNamespace(returncode=0, stdout='123|FAILED|1:0|None|\n')):
                done, rows = series.refresh(folder)
            self.assertTrue(done)
            self.assertEqual([r['state'] for r in rows], ['COMPLETED', 'FAILED', 'NOT_RUN'])
            self.assertTrue((folder / 'kernel_breakdown.svg').exists())

    def test_finished_markers_survive_accounting_outage(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            fixture(folder / '1_gpus/1x1x1', 1, '1x1x1')
            (folder / 'jobs.json').write_text(json.dumps([dict(gpus=1, partitions=['1x1x1'], job_id='123', state='RUNNING', details='')]))
            with patch.object(series, 'run', return_value=SimpleNamespace(returncode=1, stdout='Database unavailable')) as mocked:
                done, rows = series.refresh(folder)
            self.assertTrue(done)
            self.assertEqual(rows[0]['state'], 'COMPLETED')
            self.assertEqual(mocked.call_count, 1)


if __name__ == '__main__':
    unittest.main()
