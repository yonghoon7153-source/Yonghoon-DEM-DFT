"""Expected outcomes for a repeated numerical experiment; synthetic rows only."""
import copy
import csv
import hashlib
import io
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import repeat_readback as readback
except ModuleNotFoundError:
    readback = None


def sample(cells, phi):
    # Width and reference area are constant; pressure first reaches 0.12 E here.
    raw = io.StringIO(newline="")
    trace = csv.writer(raw)
    trace.writerow(["step", "time_code", "height", "bottom_pressure_E", "phi_m"])
    trace.writerows([(0, 0, 1.0, 0, 0.78), (1, 0.001, 0.78 / phi, 0.12, phi)])
    result = {"cells": cells, "points": 12 if cells == 12 else 16, "steps_attempted": 1,
              "status": "TARGET_BRACKETED", "qualified": False, "elapsed_s": 10.0,
              "phi_m": phi, "disks": 49, "dt": 0.001, "wall_speed": 0.02, "target_E": 0.12,
              "friction": 0.5, "protocol": "development-mode-1-nodal-gradient",
              "label": "DEVELOPMENT_ONLY", "contact": "shared_node_approach"}
    trace_bytes = raw.getvalue().encode("ascii")
    return result, trace_bytes


class RepeatTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(readback, "paired reader is required")
        self.arms = {str(n): sample(n, phi) for n, phi in ((12, 0.9900), (16, 0.9851))}
        self.reference = {name: {"result": copy.deepcopy(result),
                                 "trace_sha256": hashlib.sha256(trace).hexdigest()}
                          for name, (result, trace) in self.arms.items()}

    def evaluate(self):
        return readback.compare_pair(self.reference, self.arms, {"12": 0, "16": 0})

    def test_identical_repeat(self):
        report = self.evaluate()
        self.assertEqual(report["assessment"], "WITHIN_DEVELOPMENT_BAND")
        self.assertTrue(report["both_traces_identical"])
        self.assertEqual(report["max_within_resolution_abs_delta"], 0.0)
        self.assertIsNone(report["selected_setting"])
        self.assertFalse(report["u6_qualified"])

    def test_changed_endpoint_keeps_first_run_and_exposes_threshold_crossing(self):
        self.arms["16"] = sample(16, 0.9848)
        report = self.evaluate()
        self.assertEqual(report["assessment"], "OUTSIDE_DEVELOPMENT_BAND")
        self.assertEqual(report["first_assessment"], "WITHIN_DEVELOPMENT_BAND")
        self.assertFalse(report["both_traces_identical"])
        self.assertAlmostEqual(report["max_within_resolution_abs_delta"], 0.0003)

    def test_matching_endpoint_with_changed_trace(self):
        result, trace = self.arms["16"]
        self.arms["16"] = result, trace.replace(b"0.12,", b"0.120,")
        report = self.evaluate()
        self.assertFalse(report["both_traces_identical"])
        self.assertEqual(report["max_within_resolution_abs_delta"], 0)

    def test_time_limit_yields_no_pair_estimate(self):
        self.arms["16"][0].update(status="TIME_LIMIT", phi_m=None)
        report = self.evaluate()
        self.assertEqual(report["assessment"], "INCOMPLETE")
        self.assertIsNone(report["repeat_abs_grid_delta"])
        self.assertIsNone(report["max_within_resolution_abs_delta"])

    def test_rejects_modified_fixed_condition(self):
        self.arms["12"][0]["wall_speed"] *= 2
        with self.assertRaisesRegex(ValueError, "fixed condition"):
            self.evaluate()

    def test_rejects_inconsistent_reported_endpoint(self):
        self.arms["16"][0]["phi_m"] += 0.0001
        with self.assertRaisesRegex(ValueError, "interpolated"):
            self.evaluate()

    def test_reported_success_requires_first_crossing_at_last_step(self):
        result, trace = self.arms["12"]
        extra = trace.splitlines(keepends=True)[-1].replace(b"1,0.001,", b"2,0.002,")
        self.arms["12"] = result | {"steps_attempted":2}, trace + extra
        with self.assertRaisesRegex(ValueError, "first crossing"):
            self.evaluate()

    def test_failed_process_is_incomplete_even_with_a_result_file(self):
        report = readback.compare_pair(self.reference, self.arms, {"12": 0, "16": 124})
        self.assertEqual(report["assessment"], "INCOMPLETE")
        self.assertIsNone(report["repeat_abs_grid_delta"])


if __name__ == "__main__":
    unittest.main()
