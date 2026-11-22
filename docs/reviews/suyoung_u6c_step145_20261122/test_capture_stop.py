"""Small checks on the capture boundary using synthetic single-node data."""
import argparse
import importlib.util
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import numpy as np


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cap = load("capture", Path(__file__).with_name("capture_stop.py"))


def two_nodes():
    centers = np.array([[-1., -.2], [1., -.1], [.1, 1.]])
    ids = np.tile([0,1,2], 2)
    nodes = np.repeat([71,94], 3)
    m = np.ones(6)
    grad = centers[ids].copy()
    velocity = np.vstack((centers, -centers))
    return ids, nodes, m, grad, velocity, centers, .5


class Capture(unittest.TestCase):
    def test_only_unsolved_rows_and_exact_inputs(self):
        data = two_nodes()
        initial = data[4].copy()
        with mock.patch.object(kernel, "MAX_ITERATIONS", 0):
            try:
                kernel.project_contacts(*data)
            except ArithmeticError as err:
                expected = str(err)
            else:
                self.fail("Expected synthetic stop")
            observer = cap.StopObserver(kernel, target=1, expected=expected)
            with self.assertRaises(cap.ExpectedCapture):
                observer.project_contacts(*data)
        np.testing.assert_array_equal(initial, data[4])
        self.assertEqual(len(observer.nodes), 1)
        item = observer.nodes[0]
        self.assertEqual(item["node_id"], 94)
        fields = item["field_ids"]
        np.testing.assert_array_equal(item["incoming"], -data[5][fields])
        np.testing.assert_array_equal(item["grad"], data[5][fields])
        self.assertEqual(item["mu"], .5)
        self.assertEqual(item["iteration"], 0)
        self.assertGreater(item["residual"], item["speed_tol"])
        self.assertEqual(list(zip(item["left"],item["right"])), [(0,1), (0,2), (1,2)])
        with self.assertRaisesRegex(ValueError, "STEP_CEILING"):
            observer.project_contacts(*data)

    def test_pass_at_stop_step_cannot_advance(self):
        stub = SimpleNamespace(project_contacts=mock.Mock())
        observer = cap.StopObserver(stub, target=3)
        observer.project_contacts()
        observer.project_contacts()
        with self.assertRaisesRegex(ValueError, "EXPECTED_STOP_ABSENT"):
            observer.project_contacts()
        with self.assertRaisesRegex(ValueError, "STEP_CEILING"):
            observer.project_contacts()
        self.assertEqual(stub.project_contacts.call_count, 3)

    def test_early_failure_keeps_native_stop(self):
        stub = SimpleNamespace(project_contacts=mock.Mock(side_effect=ArithmeticError(cap.EXPECTED)))
        observer = cap.StopObserver(stub)
        with self.assertRaises(ArithmeticError):
            observer.project_contacts()
        self.assertEqual(observer.nodes, [])

    def test_different_native_reason_not_accepted(self):
        stub = SimpleNamespace(project_contacts=mock.Mock(side_effect=ArithmeticError("different")))
        with self.assertRaisesRegex(ValueError, "CHANGED_STOP_REASON"):
            cap.StopObserver(stub, target=1).project_contacts()

    def test_matching_error_text_without_native_frames_not_accepted(self):
        def unrelated(*args):
            raise ArithmeticError(cap.EXPECTED)
        stub = SimpleNamespace(project_contacts=unrelated, _simultaneous=lambda: None)
        with self.assertRaisesRegex(ValueError, "NATIVE_FRAME_MISSING"):
            cap.StopObserver(stub, target=1).project_contacts()

    def test_mismatched_prior_does_not_load_kernel(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/"prior").write_bytes(b"unrelated")
            with mock.patch.object(cap, "load", side_effect=AssertionError):
                with self.assertRaisesRegex(ValueError, "WRONG_PRIOR_ARCHIVE"):
                    cap.execute(root, root/"prior", root)

    def test_mismatched_prefix_suppresses_witness(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/"replay").mkdir()
            (root/"replay"/"trace.csv").write_bytes(b"altered prefix")
            observer = SimpleNamespace(calls=145, nodes=[{"node_id":1}])
            with self.assertRaisesRegex(ValueError, "TRACE_PREFIX_MISMATCH"):
                cap.publish(observer, {}, root)
            self.assertFalse((root/"failing_nodes.json").exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    args, rest = parser.parse_known_args()
    kernel = load("pinned_capture_subject", args.source_dir/"suyoung_multicontact_dev.py")
    unittest.main(argv=[sys.argv[0]] + rest)
