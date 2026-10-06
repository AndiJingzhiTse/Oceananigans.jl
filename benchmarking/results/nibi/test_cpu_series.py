"""CPU allocation validation and honest reporting when runs fail or are missing."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import cpu_series
from scaling import partition_for


def fixture(case, nodes, partition):
    shape = [n // p for n, p in zip((1440, 720, 200), partition)]
    entries = [dict(rank=i, grid_size=shape, float_type="Float64", samples=5,
                    time_steps=10, Δt=60, time_per_step_seconds=1.0,
                    time_per_step_median_seconds=1.1, time_per_step_max_seconds=1.2,
                    metadata=dict(num_threads=192)) for i in range(nodes)]
    (case / "results.json").write_text(json.dumps(entries))
    layout = [dict(rank=i, hostname=f"c{i}", threads=192, cpus_per_task=192,
                   cpu_affinity="0-191") for i in range(nodes)]
    (case / "cpu_layout.json").write_text(json.dumps(layout))
    return layout


class CPUSeriesTests(unittest.TestCase):
    def test_rejects_underthreaded_unbound_and_shared_node_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp)
            original = fixture(case, 4, (2, 2, 1))
            self.assertEqual(cpu_series.validate(case, 4, "2x2x1"), (1.0, 1.1))
            for key, value in (("threads", 1), ("cpu_affinity", "0-95"), ("hostname", "c1")):
                layout = [dict(r) for r in original]
                layout[0][key] = value
                (case / "cpu_layout.json").write_text(json.dumps(layout))
                with self.assertRaises(ValueError):
                    cpu_series.validate(case, 4, "2x2x1")

    def test_partial_partition_failure_retains_verified_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            cpu_series.save_jobs(folder, [dict(nodes=4, cores=768, partitions=list(cpu_series.PARTITIONS),
                                               folder=".", job_id="123", state="SUBMITTED")])
            (folder / "mode.txt").write_text("partition\n")
            case = folder / "4x1x1"
            case.mkdir()
            fixture(case, 4, (4, 1, 1))
            (case / "exit_code.txt").write_text("0\n")
            failed = folder / "2x2x1"
            failed.mkdir()
            (failed / "exit_code.txt").write_text("1\n")
            responses = [SimpleNamespace(returncode=0, stdout="123|FAILED|1:0|None|\n"),
                         SimpleNamespace(returncode=0, stdout="")]
            with patch.object(cpu_series, "run", side_effect=responses):
                done, rows = cpu_series.refresh(folder)
            self.assertTrue(done)
            self.assertEqual([r["state"] for r in rows], ["COMPLETED", "FAILED", "NOT_RUN"])
            self.assertTrue((folder / "cpu_comparison.svg").exists())
            self.assertIsNone(rows[1]["fastest"])

    def test_scaling_requires_baseline_and_reports_correct_efficiency(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            rows = [dict(nodes=2, cores=384, partition="1x2x1", job_id="123", state="COMPLETED",
                         fastest=0.6, median=0.65, details="Verified")]
            cpu_series.report(folder, "scaling", rows)
            self.assertNotIn("83.3%", (folder / "plot.md").read_text())
            rows.insert(0, dict(nodes=1, cores=192, partition="1x1x1", job_id="122", state="COMPLETED",
                                fastest=1.0, median=1.1, details="Verified"))
            cpu_series.report(folder, "scaling", rows)
            self.assertIn("83.3% / 84.6%", (folder / "plot.md").read_text())

    def test_horizontal_grid_limit_and_disjoint_affinity_ranges(self):
        self.assertEqual(partition_for(512), (32, 16))
        with self.assertRaises(ValueError):
            partition_for(1024)
        self.assertEqual(cpu_series.affinity_count("0-95,192-287"), 192)
        with self.assertRaises(ValueError):
            cpu_series.affinity_count("0-95,90-191")


if __name__ == "__main__":
    unittest.main()
