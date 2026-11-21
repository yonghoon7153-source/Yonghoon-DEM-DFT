"""Synthetic wall calls, a small stencil, and readback guards. No field run."""
import csv
import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

import numpy as np


SPEC = importlib.util.spec_from_file_location("test_subject", Path(__file__).with_name("observe.py"))
obs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(obs)


class WallTests(unittest.TestCase):
    def test_wall_probe_reads_preclamp_values_and_preserves_velocity(self):
        solver = obs.load_driver().fixed_solver()
        mass = np.array([2., 3., 0., 1.])
        xy = np.array([[.2, .15], [.2, .90], [.2, .95], [.3, .4]])
        vel = np.array([[0., -2.], [0., .25], [0., 1.], [0., -.5]])
        original = vel.copy()
        baseline = solver.walls(mass, xy, original, .8, -.25)
        collector = obs.WallObserver(solver, lambda: self.fail("unexpected writes"))
        actual = solver.walls(mass, xy, vel, .8, -.25)
        self.assertEqual(actual, baseline)
        self.assertEqual(vel.tobytes(), original.tobytes())
        self.assertEqual(collector.calls, [(4., 1.5, 1, 1)])

    def test_complete_advance_preserves_small_synthetic_state_bytewise(self):
        driver = obs.load_driver()
        plain, monitored = driver.fixed_solver(), driver.fixed_solver()
        stream = io.StringIO()
        collector = obs.WallObserver(monitored, lambda: stream)
        grid, dt = 80, driver.step_size(plain, 8)
        lid = plain.LO + (plain.WIDTH - dt*plain.WALL_SPEED)
        particles = np.array([[.2, .15], [.4, lid-.001]])
        vel = np.array([[.01, -.2], [-.01, .2]])
        args = (particles, vel, np.zeros((2,2,2)), np.repeat(np.eye(2)[None],2,axis=0),
                np.array([0,1]), np.full(2,1e-5), grid,dt,lid)
        expected = plain.advance(*args)
        got = collector.advance(*args)
        for a, b in zip(expected[:-1], got[:-1]):
            self.assertEqual(a.tobytes(), b.tobytes())
        self.assertEqual(expected[-1], got[-1])
        row, = csv.DictReader(io.StringIO(stream.getvalue()))
        self.assertEqual(int(row["step"]), 1)
        self.assertEqual(float(row["bottom_pressure_E"]), got[-1])
        self.assertEqual(float(row["plate_displacement_code"]), plain.WIDTH - (plain.WIDTH - dt*plain.WALL_SPEED))
        self.assertGreater(float(row["bottom_J_pre"]), 0)

    def test_missing_second_wall_is_rejected(self):
        solver = obs.load_driver().fixed_solver()
        solver.advance = lambda *args: (None,None,None,None,0.)
        collector = obs.WallObserver(solver, lambda: self.fail("unexpected writes"))
        with self.assertRaisesRegex(ValueError, "wall calls"):
            collector.advance(None, None, None, None, None, None, 80, .01, .8)

    def test_source_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp)/"suyoung_u6b_dev.py"
            file.write_bytes(b"raise RuntimeError('should never import')")
            with self.assertRaisesRegex(ValueError, "source"):
                obs.load_driver(Path(tmp))

    def test_trace_status_will_not_adopt_timeout_or_wrong_trajectory(self):
        sha = obs.EXPECTED[16]
        self.assertEqual(obs.classification("TARGET_BRACKETED", sha, 16), "DEVELOPMENT_WALL_READBACK")
        self.assertEqual(obs.classification("TIME_LIMIT", sha, 16), "INCOMPLETE")
        self.assertEqual(obs.classification("TARGET_BRACKETED", hashlib.sha256(b"different").hexdigest(), 16),
                         "TRACE_MISMATCH")


if __name__ == "__main__":
    unittest.main()
