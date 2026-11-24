"""Synthetic B2 flow tests, independently runnable without a return."""
import importlib.util
import io
import unittest
from pathlib import Path

import numpy as np


def fixture(moving=True, slope=0.4):
    # Cross-section with evenly spaced surface points above a rigidly rotating bulk.
    radius, omega = .01258325, 2 * np.pi / .782508
    y, d = np.meshgrid(np.linspace(-.66, .66, 361) * radius,
                       np.arange(.005, .60, .01) * radius)
    y, d = y.ravel(), d.ravel()
    r = np.full_like(y, .006 * radius)
    z = slope * y - d * np.hypot(1, slope)
    vy, vz = -omega * z, omega * y
    if moving:
        active = d < .087 * radius
        vy[active], vz[active] = -.6 * omega * radius, -.6 * omega * radius * slope
    return np.zeros_like(y), y, z, vy, vz, r


class FlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("flow_observer", Path(__file__).with_name("flow_observer.py"))
        # A new observer is required for same-step, native-time measurement.
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_surface_and_known_layer(self):
        result = self.mod.measure(*fixture(), rotating=True)
        self.assertAlmostEqual(result["theta_signed_deg"], np.degrees(np.arctan(.4)), delta=.7)
        self.assertEqual(result["layer_status"], "RESOLVED")
        self.assertAlmostEqual(result["delta_over_R"], .087, delta=.028)
        self.assertEqual(len(result["layer_sensitivity"]), 3)

    def test_rigid_rotation_is_not_flow(self):
        result = self.mod.measure(*fixture(False), rotating=True)
        self.assertIsNone(result["delta_over_R"])

    def test_reverse_surface_mirror_has_signed_angle(self):
        original = list(fixture())
        original[1] = -original[1]
        original[3] = -original[3]
        result = self.mod.measure(*original, rotating=True)
        self.assertAlmostEqual(result["theta_signed_deg"], -np.degrees(np.arctan(.4)), delta=.7)

    def test_shell_slip_uses_local_rigid_angular_velocity(self):
        mod = self.mod
        angle = np.linspace(-2.8, 2.8, 100)
        r = np.full_like(angle, .01 * mod.RADIUS)
        y, z = .985 * mod.RADIUS * np.cos(angle), .985 * mod.RADIUS * np.sin(angle)
        slip = mod.wall_slip(y, z, -.80 * mod.OMEGA * z, .80 * mod.OMEGA * y, r, True)
        self.assertAlmostEqual(slip["azimuthal_slip_fraction"], .20)
        self.assertEqual(slip["near_wall_particles"], len(angle))

    def test_disconnected_depth_does_not_fill_missing_bins(self):
        a = dict(depth_R=.01, lab_over_omega_R=.3, relative_over_omega_R=.3)
        gap = dict(depth_R=.03, lab_over_omega_R=None, relative_over_omega_R=None)
        c = dict(depth_R=.05, lab_over_omega_R=-.2, relative_over_omega_R=-.2)
        result = self.mod.layer_boundary([a, gap, c], .05)
        self.assertEqual(result["status"], "DEPTH_COVERAGE_GAP")
        self.assertIsNone(result["delta_over_R"])

    def test_axial_wall_does_not_change_surface(self):
        original = fixture()
        side = list(fixture(slope=-.7))
        side[0] += .002
        joined = [np.r_[a, b] for a, b in zip(original, side)]
        a = self.mod.measure(*original, rotating=True)
        b = self.mod.measure(*joined, rotating=True)
        self.assertEqual(a["theta_signed_deg"], b["theta_signed_deg"])
        self.assertEqual(a["delta_over_R"], b["delta_over_R"])

    def test_horizontal_and_pre_rotation_skip_layer(self):
        flat = self.mod.measure(*fixture(slope=0), rotating=True)
        self.assertIsNone(flat["delta_over_R"])
        pre = self.mod.measure(*fixture(), rotating=False)
        self.assertIsNone(pre["delta_over_R"])
        self.assertIsNotNone(pre["theta_signed_deg"])

    def test_frame_identity_and_clock(self):
        row = b"1 1 0 0 0 0 1 2 0 0 0 .0006813\n"
        header = (b"ITEM: TIMESTEP\n1121184\nITEM: NUMBER OF ATOMS\n1\n"
                  b"ITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\n"
                  b"ITEM: ATOMS id type x y z vx vy vz fx fy fz radius\n")
        result = self.mod.observe_frame(io.BytesIO(header + row), 1121184)
        self.assertEqual(result["phase"], "PRE_ROTATION")
        self.assertEqual(result["atom_count"], 1)
        with self.assertRaises(ValueError):
            self.mod.observe_frame(io.BytesIO(header + row), 1121185)
        with self.assertRaises(ValueError):
            self.mod.observe_frame(io.BytesIO(header.replace(b"NUMBER OF ATOMS\n1", b"NUMBER OF ATOMS\n2") + row),1121184)

    def test_whole_plan_and_temporal_groups(self):
        result = self.mod.measure(*fixture(), rotating=True)
        records = [dict(result, step=i * 32976) for i in range(34,235)]
        summary = self.mod.summarize(records[::-1])
        self.assertEqual(summary["turn_0_to_1"]["frames"], 99)
        self.assertEqual(summary["turn_1_to_2"]["frames"], 100)
        self.assertEqual(summary["post_two_turns_frames"], 1)
        self.assertEqual(summary["independent_seeds"], 1)
        self.assertIsNone(summary["mu_wall_effective"])
        with self.assertRaises(ValueError):
            self.mod.summarize(records[:-1] + records[:1])


if __name__ == "__main__":
    unittest.main()
