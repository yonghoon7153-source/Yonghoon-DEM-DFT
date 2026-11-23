"""Synthetic patches only. No call to the native 49-disk seed or run driver."""
import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent


def load(path):
    spec = importlib.util.spec_from_file_location("test_" + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


candidate = load(HERE / "material_lid.py")
default_root = HERE.parents[2]
root = Path(os.environ.get("SUYOUNG_SOURCE_ROOT", default_root))
floor = load(root / "docs/reviews/suyoung_floor_contact_20261123/material_floor.py")
model = load(root / "scripts/suyoung_u6_first_dev.py").model
DT, INITIAL_TOP, SPEED, GRID = .001, .65, .02, 80


class SyntheticLid(unittest.TestCase):
    def setup_patch(self, y, v, *, markers=None, exchange=None, with_lid=True, x=None):
        n = len(y)
        x = np.asarray(x if x is not None else [.35] * n)
        points = np.column_stack((x, y))
        ids = np.arange(n, dtype=int)
        volume = np.full(n, .0003)
        boundary = floor.MaterialBoundary(ids, points if markers is None else markers, ids)
        affine = np.zeros((n, 2, 2))
        elastic = np.broadcast_to(np.eye(2), affine.shape).copy()
        solver = SimpleNamespace(model=model, LO=.15, WIDTH=.5, WALL_SPEED=SPEED,
                                 project_contacts=(exchange or (lambda *args: None)))
        if with_lid:
            advance = candidate.make_advance(solver, 12, floor_module=floor, boundary=boundary)
        else:
            advance = floor.make_advance(solver, 12, boundary=boundary)
        return advance, (points, np.array(v, dtype=float), affine, elastic, ids, volume), boundary

    def run_step(self, advance, state, step=1):
        return advance(*state, GRID, DT, INITIAL_TOP - step * DT * SPEED)

    def test_open_gap_on_occupied_top_nodes(self):
        old, a, _ = self.setup_patch([.644], [[0., 0.]], with_lid=False)
        new, b, boundary = self.setup_patch([.644], [[0., 0.]])
        self.assertLess(self.run_step(old, a)[1][0, 1], 0.)
        out = self.run_step(new, b)
        self.assertEqual(out[1][0, 1], 0.)
        self.assertEqual(boundary.positions[0, 1], .644)
        self.assertEqual(new.last_step["lid_downward_impulse"], 0.)
        self.assertEqual(new.lid_audit["positive_passes"], 0)

    def test_lid_closes_half_step_gap_at_analytic_relative_speed(self):
        initial_y = INITIAL_TOP - .5 * DT * SPEED
        new, state, boundary = self.setup_patch([initial_y], [[.003, 0.]])
        out = self.run_step(new, state)
        target = INITIAL_TOP - DT * SPEED
        expected_velocity = (target - initial_y) / DT
        self.assertAlmostEqual(out[1][0, 1], expected_velocity, places=13)
        self.assertAlmostEqual(out[1][0, 0], .003, places=15)
        self.assertAlmostEqual(new.last_step["lid_signed_impulse"], state[5][0] * expected_velocity, places=16)
        self.assertAlmostEqual(boundary.positions[0, 1], target, places=14)
        self.assertEqual(new.lid_audit["positive_passes"], 1)
        self.assertEqual(new.last_step["floor_impulse"], 0.)

    def test_touching_marker_separating_from_plate(self):
        new, state, _ = self.setup_patch([INITIAL_TOP], [[0., -2 * SPEED]])
        self.run_step(new, state)
        self.assertEqual(new.last_step["lid_downward_impulse"], 0.)
        self.assertGreater(new.last_step["top_gap_after"], 0.)

    def test_positive_endpoint_gap_but_upward_marker_closes_it(self):
        end = INITIAL_TOP - DT * SPEED
        new, state, _ = self.setup_patch([end - .25 * DT * SPEED], [[0., SPEED]])
        out = self.run_step(new, state)
        self.assertGreater(new.last_step["top_gap_before"], 0.)
        self.assertAlmostEqual(out[1][0, 1], .25 * SPEED, places=12)
        self.assertAlmostEqual(new.last_step["top_gap_after"], 0., places=14)
        self.assertGreater(new.last_step["lid_downward_impulse"], 0.)

    def test_responds_again_after_interbody_and_transports_markers_once(self):
        calls = []
        def kick(ids, nodes, mass, grad, gv, centers, friction):
            calls.append(friction)
            gv[ids == 1, 1] += .035
            gv[ids == 0, 1] -= .035

        new, state, boundary = self.setup_patch([.15, INITIAL_TOP], [[0., -.01], [0., 0.]], exchange=kick)
        out = self.run_step(new, state)
        self.assertEqual(calls, [.5])
        self.assertEqual(new.audit["positive_passes"], 2)
        self.assertEqual(new.lid_audit["positive_passes"], 2)
        self.assertEqual(new.lid_audit["lid_passes"], 2)
        self.assertAlmostEqual(new.last_step["floor_impulse"], (.01 + .035) * state[5][0], places=15)
        self.assertAlmostEqual(new.last_step["lid_downward_impulse"], (SPEED + .035) * state[5][1], places=15)
        self.assertAlmostEqual(float(state[5] @ (out[1][:, 1] - state[1][:, 1])),
                               new.last_step["floor_impulse"] + new.last_step["lid_signed_impulse"], places=16)
        self.assertAlmostEqual(boundary.positions[0, 1], .15, places=15)
        self.assertAlmostEqual(boundary.positions[1, 1], INITIAL_TOP - DT * SPEED, places=15)
        self.assertLess(new.last_step["lid_grid_impulse_error"], 1.e-17)

    def test_lower_and_side_action_far_from_lid_bit_for_bit(self):
        def exchange(ids, nodes, mass, grad, gv, centers, friction):
            gv[ids == 0, 1] -= .01
            gv[ids == 1, 1] += .01
        args = dict(y=[.15, .4], v=[[-.01, -.02], [.02, .01]], x=[.15, .64], exchange=exchange)
        legacy, old_input, old_markers = self.setup_patch(**args, with_lid=False)
        new, new_input, new_markers = self.setup_patch(**args)
        original_function = floor._other_walls
        for step in range(1, 4):
            old_out = self.run_step(legacy, old_input, step)
            new_out = self.run_step(new, new_input, step)
            for a, b in zip(old_out, new_out):
                self.assertEqual(np.asarray(a).tobytes(), np.asarray(b).tobytes())
            self.assertEqual(old_markers.positions.tobytes(), new_markers.positions.tobytes())
            old_input = (*old_out[:4], *old_input[4:])
            new_input = (*new_out[:4], *new_input[4:])
        self.assertEqual(legacy.audit, new.audit)
        self.assertEqual(new.lid_audit["steps"], 3)
        self.assertEqual(new.lid_audit["lid_passes"], 6)
        self.assertEqual(new.lid_audit["accumulated_downward_impulse"], 0.)
        self.assertIs(floor._other_walls, original_function)

    def test_offcenter_marker_obeys_same_affine_transport_and_support(self):
        initial_y = INITIAL_TOP - DT * SPEED / 3
        p0 = np.array([.35, .647])
        b0 = np.array([.352, initial_y])
        new, state, boundary = self.setup_patch([p0[1]], [[.004, .012]], markers=[b0])
        state[2][0, :, :] = [[.13, -.11], [.2, .3]]
        out = self.run_step(new, state)
        expected_position = b0 + DT * (out[1][0] + out[2][0] @ (b0 - p0))
        np.testing.assert_allclose(boundary.positions[0], expected_position, rtol=0, atol=2.e-16)
        self.assertAlmostEqual(new.last_step["top_gap_after"], 0., places=14)
        self.assertGreater(new.last_step["lid_downward_impulse"], 0.)
        self.assertAlmostEqual(float(state[5] @ (out[1][:, 1] - state[1][:, 1])),
                               new.last_step["lid_signed_impulse"], places=16)

    def test_wrong_clock_previous_overlap_and_failed_retry(self):
        for y, step, expected in ((.5, 2, "previous"), (INITIAL_TOP + 1.e-5, 1, "incoming"),
                                  (.15 - 1.e-5, 1, "incoming")):
            new, state, _ = self.setup_patch([y], [[0., 0.]])
            with self.assertRaisesRegex((ArithmeticError, ValueError), expected):
                self.run_step(new, state, step)
            self.assertEqual(new.lid_audit["steps"], 0)
            self.assertIsNone(new.last_step)
            with self.assertRaisesRegex(RuntimeError, "cannot resume"):
                self.run_step(new, state)
        new, state, _ = self.setup_patch([.5], [[0., 0.]])
        out = self.run_step(new, state)
        with self.assertRaisesRegex(ValueError, "previous"):
            self.run_step(new, (*out[:4], *state[4:]), 1)
        self.assertEqual(new.lid_audit["steps"], 1)

    def test_fail_closed_on_penetration_after_both_projections(self):
        new, state, boundary = self.setup_patch([.5], [[0., 0.]])
        native_bind = boundary.bind
        def faulty_transport(*args):
            s = native_bind(*args)
            s.transport = lambda grid: boundary.positions.__setitem__((0, 1), INITIAL_TOP + .01)
            return s
        boundary.bind = faulty_transport
        with self.assertRaisesRegex(ArithmeticError, "transported"):
            self.run_step(new, state)
        self.assertEqual(new.lid_audit["steps"], 0)
        self.assertEqual(new.audit["steps"], 0)

    def test_refuses_nonmatching_material_source(self):
        new, _, _ = self.setup_patch([.5], [[0., 0.]])
        with self.assertRaisesRegex(ValueError, "unrecognized"):
            candidate.make_advance(new.solver, 12, floor_module=SimpleNamespace(__file__=__file__))


if __name__ == "__main__":
    unittest.main()
