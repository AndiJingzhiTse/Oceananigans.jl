import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

path = Path(__file__).parents[1] / "scripts" / "pressure_solver_study.py"
spec = importlib.util.spec_from_file_location("pressure_solver_study", path)
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


class AcceptanceTests(unittest.TestCase):
    def write_records(self, directory, devices):
        for rank, device in enumerate(devices):
            record = dict(rank=rank, ranks=len(devices), status="COMPLETED", gpu_uuid=device,
                          configuration=dict(windows=1), pressure_timing=dict(maximum_rank_seconds=[1]),
                          timestep_timing=dict(maximum_rank_seconds=[1]),
                          pressure_validation=dict(passed=True, tolerance=1e-10, relative_residual=1e-15, relative_error=1e-15),
                          model_validation=dict(passed=True, tolerance=1e-10, maximum_divergence=1e-15))
            (directory / f"rank_{rank}.json").write_text(json.dumps(record))

    def test_placement_and_numerical_gates(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write_records(directory, ["first", "second"])
            self.assertEqual(len(study.accepted_records(directory, 2, ["GPU-first", "GPU-second"])), 2)
            self.write_records(directory, ["first", "first"])
            with self.assertRaisesRegex(ValueError, "GPU placement"):
                study.accepted_records(directory, 2, ["first", "second"])
            self.write_records(directory, ["first", "second"])
            path = directory / "rank_1.json"
            record = json.loads(path.read_text())
            record["pressure_validation"]["passed"] = False
            path.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, "Numerical"):
                study.accepted_records(directory, 2, ["first", "second"])
            record["pressure_validation"].update(passed=True, relative_residual=float("nan"))
            path.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, "Numerical"):
                study.accepted_records(directory, 2, ["first", "second"])


if __name__ == "__main__":
    unittest.main()
