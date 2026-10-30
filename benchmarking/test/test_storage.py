"""Storage moves preserve data and never archive a still-running case."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_suite import runner
from suite.storage import copy_verified, archive_finished_case, archive_runtime, runtime_environment


class StorageTests(unittest.TestCase):
    def test_verified_move_and_mismatched_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, destination = root / 'capture', root / 'results/capture'
            source.write_bytes(b'profile data' * 10000)
            record = copy_verified(source, destination, remove=True)
            self.assertFalse(source.exists())
            self.assertEqual(destination.stat().st_size, record['bytes'])
            source.write_bytes(b'different data')
            with self.assertRaises(ValueError):
                copy_verified(source, destination, remove=True)
            self.assertTrue(source.exists())
            self.assertEqual(destination.read_bytes(), b'profile data' * 10000)

    def test_cpu_records_wait_for_case_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'study'
            case = {'id': '96_ranks', 'series': 'cpu_mpi_scaling_super_fine', 'state': 'RUNNING'}
            source = folder / case['id']
            source.mkdir(parents=True)
            (source / 'job.out').write_text('ongoing')
            self.assertFalse(archive_finished_case(folder, case, root / 'results'))
            case['state'] = 'COMPLETED'
            (source / 'finished.txt').write_text('finished')
            self.assertTrue(archive_finished_case(folder, case, root / 'results'))
            destination = root / 'results' / case['series'] / 'run_records' / case['id']
            self.assertEqual((destination / 'job.out').read_text(), 'ongoing')
            self.assertTrue((source / 'job.out').exists())
            index = json.loads((root / 'results' / case['series'] / 'run_records_manifest.json').read_text())
            self.assertIn('96_ranks', index)

    def test_runtime_files_move_under_results_and_use_short_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime = root / ('a' * 100) / '.runtime/48_ranks'
            with patch('pathlib.Path.home', return_value=root):
                environment = runtime_environment(runtime)
            self.assertEqual(Path(environment['TMPDIR']).resolve(), runtime)
            self.assertLess(len(environment['TMPDIR']), len(str(runtime)))
            (runtime / 'mpi_session').write_bytes(b'MPI evidence')
            records = archive_runtime(runtime, root / 'run_records/runtime')
            self.assertFalse(runtime.exists())
            self.assertEqual(records[0]['bytes'], 12)
            self.assertEqual((root / 'run_records/runtime/mpi_session').read_bytes(), b'MPI evidence')

    def test_default_trace_and_temporary_paths_do_not_use_tmp(self):
        server = runner.load_server(runner.ROOT / 'server/rondeau/config.json', 'NonhydrostaticModel')
        self.assertTrue(server['trace_root'].endswith('results/non_hydrostatic_models/rondeau/baseline'))
        script = '\n'.join(runner.environment_lines(server))
        self.assertIn('export TMPDIR=', script)
        self.assertIn('export OMPI_MCA_orte_tmpdir_base=', script)
        self.assertNotIn('/tmp/benchmark_traces', script)


if __name__ == '__main__':
    unittest.main()
