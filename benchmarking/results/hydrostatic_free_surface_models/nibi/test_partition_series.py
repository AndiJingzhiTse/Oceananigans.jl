"""Test result validation and partial-failure reporting without submitting jobs."""
import csv
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import partition_series
from scaling import read_results


def fixture(partition):
    shape = [n // p for n, p in zip((1440, 720, 200), partition)]
    return [dict(rank=rank, grid_size=shape, float_type="Float64", samples=5,
                 time_steps=10, Δt=60, time_per_step_seconds=0.25,
                 time_per_step_median_seconds=0.26, time_per_step_max_seconds=0.3)
            for rank in range(4)]


class PartitionSeriesTests(unittest.TestCase):
    def test_rejects_wrong_partition_shape_and_duplicate_ranks(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            data = fixture((4, 1, 1))
            (folder / "results.json").write_text(json.dumps(data))
            self.assertEqual(len(read_results(folder, 4, (4, 1, 1))), 4)
            with self.assertRaises(ValueError):
                read_results(folder, 4, (2, 2, 1))
            data[3]["rank"] = 0
            (folder / "results.json").write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                read_results(folder, 4, (4, 1, 1))

    def test_keeps_successful_case_when_another_case_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "job_id.txt").write_text("123\n")
            completed = folder / "4x1x1"
            completed.mkdir()
            (completed / "exit_code.txt").write_text("0\n")
            (completed / "results.json").write_text(json.dumps(fixture((4, 1, 1))))
            failed = folder / "2x2x1"
            failed.mkdir()
            (failed / "exit_code.txt").write_text("1\n")
            responses = [SimpleNamespace(returncode=0, stdout="123|FAILED|1:0|None|\n"),
                         SimpleNamespace(returncode=0, stdout="")]
            with patch.object(partition_series, "run", side_effect=responses):
                self.assertTrue(partition_series.summarize(folder))
            with (folder / "partition_results.csv").open() as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual([r["state"] for r in rows], ["COMPLETED", "FAILED", "NOT_RUN"])
            self.assertTrue((folder / "partition_comparison.svg").exists())


if __name__ == "__main__":
    unittest.main()
