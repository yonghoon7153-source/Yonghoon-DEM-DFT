"""Synthetic node and trace cases only; no field arm is advanced."""
import argparse
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import numpy as np


here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("observed_pair", here/"node145_pair.py")
op = importlib.util.module_from_spec(spec)
spec.loader.exec_module(op)


def fields():
    centers = np.array([[-1., -.2], [1., -.1], [.1, 1.]])
    ids = np.tile([0, 1, 2], 2)
    return ids, np.repeat([71, 94], 3), np.ones(6), centers[ids].copy(), np.vstack((centers, -centers)), centers, .5


class NativeObserve(unittest.TestCase):
    def test_later_residual_retains_only_failing_node_without_replay_or_velocity_change(self):
        observer = op.ObservedProjector(kernel, capture)
        args = fields()
        initial = args[4].copy()
        success = list(fields())
        success[4] = np.zeros_like(initial)
        for _ in range(150):
            observer.project_contacts(*success)
        with mock.patch.object(kernel, "MAX_ITERATIONS", 0):
            with self.assertRaisesRegex(ArithmeticError, "residual"):
                observer.project_contacts(*args)
        self.assertEqual(observer.stop["attempted_step"], 151)
        self.assertEqual(observer.stop["scope"], "NATIVE_UNRESOLVED_ROWS")
        node, = observer.stop["nodes"]
        self.assertEqual(node["node_id"], 94)
        np.testing.assert_array_equal(node["incoming"], -args[5][node["field_ids"]])
        np.testing.assert_array_equal(node["mass"], np.ones(3))
        np.testing.assert_array_equal(args[4], initial)
        self.assertGreater(node["residual"], node["speed_tol"])

    def test_invalid_input_with_no_bound_node_preserves_exception_and_no_invented_node(self):
        observer = op.ObservedProjector(kernel, capture)
        args = list(fields())
        args[-1] = -1.
        with self.assertRaisesRegex(ValueError, "friction"):
            observer.project_contacts(*args)
        self.assertEqual(observer.stop["scope"], "NO_BOUND_NODE_ROWS")
        self.assertEqual(observer.stop["nodes"], [])
        self.assertEqual(observer.stop["exception"], "ValueError")

    def test_prefix_preserves_actual_bytes_and_detects_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/"trace.csv"
            self.assertFalse(op.trace_info(p)["present"])
            p.write_bytes(b"step,x\r\n0,42\r\n1,7\r\n")
            self.assertEqual(op.trace_info(p)["last_complete_step"], 1)
            self.assertEqual(op.trace_info(p)["sha256"], hashlib.sha256(p.read_bytes()).hexdigest())
            p.write_bytes(p.read_bytes()+b"3,1\r\n")
            self.assertFalse(op.trace_info(p)["sequence_valid"])

    def test_noncontact_driver_failure_and_budget_have_distinct_receipts(self):
        for stop in ("raise", "budget"):
            with self.subTest(stop=stop), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                args = SimpleNamespace(source_dir=path, mapping="REVERSED", budget=570, out=path/"arm")
                (path/"kernel.py").write_bytes(b"fixture")
                def integrate(driver, observer, mapping, budget, out):
                    out.mkdir()
                    (out/"trace.csv").write_bytes(b"step,x\n0,42\n")
                    if stop == "raise":
                        raise RuntimeError("synthetic pre-contact driver exception")
                    return {"status":"TIME_LIMIT"}, {}, 0
                pair = SimpleNamespace(KERNEL="kernel.py", integrate=integrate)
                stderr = io.StringIO()
                with mock.patch.object(op,"load",return_value=SimpleNamespace()), redirect_stderr(stderr), redirect_stdout(io.StringIO()):
                    self.assertEqual(op.run_arm(args,pair,capture),4)
                receipt = json.loads((args.out/"stop.json").read_bytes())
                self.assertEqual(receipt["trace"]["last_complete_step"],0)
                self.assertNotIn("attempted_step",receipt)
                self.assertFalse((args.out/"contact_stop.json").exists())
                if stop == "raise":
                    self.assertEqual(receipt["status"],"OTHER_EXCEPTION")
                    self.assertIn("synthetic pre-contact",stderr.getvalue())
                else:
                    self.assertEqual(receipt["status"],"NATIVE_STOP")
                    self.assertEqual(receipt["native_status"],"TIME_LIMIT")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel", type=Path, required=True)
    parser.add_argument("--capture-helper", type=Path, required=True)
    args, rest = parser.parse_known_args()
    kernel = op.load("source_under_test", args.kernel)
    capture = op.load("frozen_observer", args.capture_helper)
    unittest.main(argv=[sys.argv[0]]+rest)
