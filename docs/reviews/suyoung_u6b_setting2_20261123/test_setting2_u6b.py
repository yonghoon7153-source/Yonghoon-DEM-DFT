"""Synthetic S field separation, hash binding and operational-gate tests."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

import numpy as np

spec = importlib.util.spec_from_file_location("setting2_u6b", Path(__file__).with_name("setting2_u6b.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class SingleFieldTests(unittest.TestCase):
    def test_material_surface_ownership_preserved(self):
        ids = np.array([0, 1, 1])
        boundary = SimpleNamespace(owners=np.array([1, 0, 2]), positions=np.array([[0., 0.], [1., 0.], [2., 0.]]),
                                   groups=np.array([1, 0, 1]))
        nodes = boundary.positions.copy()
        app.merge_surface_fields(boundary, ids)
        np.testing.assert_array_equal(boundary.owners, [1, 0, 2])
        np.testing.assert_array_equal(boundary.positions, nodes)
        np.testing.assert_array_equal(boundary.groups, [0, 0, 0])

    def test_mismatched_physical_owner_rejected(self):
        boundary = SimpleNamespace(owners=np.array([0]), groups=np.array([1]))
        with self.assertRaises(ValueError):
            app.merge_surface_fields(boundary, np.array([0]))

    def test_single_field_no_impulse(self):
        vel = np.ones((2, 2))
        initial = vel.copy()
        app.single_field_contact(np.zeros(2, int), np.array([1, 3]), None, None, vel, np.ones((1, 2)), .5)
        np.testing.assert_array_equal(vel, initial)

    def test_foreign_field_rejected(self):
        with self.assertRaises(ValueError):
            app.single_field_contact(np.array([0, 1]), np.array([1, 3]), None, None, None, np.ones((1, 2)), .5)

    def test_shared_physical_node_has_one_grid_unknown(self):
        with self.assertRaises(ValueError):
            app.single_field_contact(np.zeros(2, int), np.array([1, 1]), None, None, None, np.ones((1, 2)), .5)

    def test_gate_rejects_foreign_setting(self):
        value = dict(gate='U6(a)', setting=1, selected_setting=1, assessment='PASS', distance_filter=False,
                     gap_correction=True, threshold=.005, absolute_delta=.001)
        with self.assertRaises(ValueError):
            app.confirm_selection(value, {12:.91,16:.911})

    def test_selected_gate_cannot_honor_false_summary(self):
        value = dict(gate='U6(a)', setting=2, selected_setting=2, assessment='PASS', distance_filter=False,
                     gap_correction=True, threshold=.005, absolute_delta=.002)
        with self.assertRaises(ValueError):
            app.confirm_selection(value, {12:.91,16:.922})

    def test_manifest_rejects_duplicate_or_missing_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            raw = b"x"
            (root / "sample").write_bytes(raw)
            line = hashlib.sha256(raw).hexdigest() + "  sample\n"
            (root / "SOURCE_SHA256SUMS").write_text(line + line)
            with self.assertRaises(ValueError):
                app.verify_manifest(root)

if __name__ == "__main__":
    unittest.main()
