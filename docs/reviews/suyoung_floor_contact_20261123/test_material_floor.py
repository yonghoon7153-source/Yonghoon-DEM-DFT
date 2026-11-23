"""Synthetic geometry, impulse and G2P checks. No production arm is launched."""
import importlib.util
import itertools
import os
from pathlib import Path
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


root = Path(os.environ.get("SUYOUNG_SOURCE_ROOT", HERE.parents[2]))
solver = load("pinned_fixture", root / "scripts/suyoung_u6_first_dev.py")
old = os.environ.get("SUYOUNG_TEST_OLD_FLOOR") == "1"
candidate = None if old else load("candidate_fixture", HERE / "material_floor.py")


def prepare(x, volume, grid, fields=None):
    nodes, weights, _, offset = solver.model.stencil(x, grid)
    if fields is not None:
        nodes += fields[:, None] * (grid + 1)**2
    key, slots = np.unique(nodes, return_inverse=True)
    slots = slots.reshape(weights.shape)
    mass = np.bincount(slots.ravel(), weights=(weights * volume[:, None]).ravel())
    xy = np.column_stack(np.divmod(key % (grid + 1)**2, grid + 1)) / grid
    return weights, offset, slots, mass, xy


class MaterialFloorTests(unittest.TestCase):
    def test_physical_gap_has_zero_reaction_on_both_grids(self):
        # Same 8-layer Gauss slab and independently specified lower face as the matched return.
        gap, width, thickness = .0125, .4, .025
        depth, qw = np.polynomial.legendre.leggauss(2)
        y = gap + thickness / 8 * (np.arange(8)[:, None] + .5 * (1 + depth))
        xx = .3 + (np.arange(64) + .5) * width / 64
        x = np.column_stack([np.tile(xx, 16), np.repeat(solver.LO + y.ravel(), 64)])
        volume = np.repeat(np.tile(qw, 8), 64) * width * thickness / (64 * 16)
        face = np.column_stack([xx, np.full(64, solver.LO + gap)])
        for grid in (80, 160):
            with self.subTest(grid=grid):
                w, off, slots, m, xy = prepare(x, volume, grid)
                gv = np.tile([0., -.02], (len(m), 1))
                if old:
                    j = solver.walls(m, xy, gv, solver.LO + solver.WIDTH, 0.)
                else:
                    b = candidate.MaterialBoundary(np.arange(64), face)
                    s = b.bind(x, w, off, slots, grid, solver.LO, .0011231835082397789)
                    j = s.project(m, gv)
                self.assertEqual(j, 0.)

    def test_contact_separation_rigid_tilt_and_g2p(self):
        x = np.array([[.3, .151], [.5, .151], [.7, .151]])
        surface = x.copy()
        surface[:, 1] = [.15, .15, .151]
        volume = np.array([.003, .002, .004])
        for grid in (80, 160):
            w, off, slots, mass, xy = prepare(x, volume, grid)
            # Rigid angular velocity plus translation reaches the floor locally only.
            gv = np.column_stack([-.1 * (xy[:, 1] - .15), .1 * (xy[:, 0] - .4)])
            before = gv.copy()
            b = candidate.MaterialBoundary(np.arange(3), surface)
            s = b.bind(x, w, off, slots, grid, .15, .01)
            j = s.project(mass, gv)
            self.assertGreater(j, 0.)
            np.testing.assert_array_equal(before[:, 0], gv[:, 0])
            np.testing.assert_array_equal(before[slots[1:]], gv[slots[1:]])
            self.assertAlmostEqual(float(mass @ (gv-before)[:, 1]), j, places=14)
            v0 = np.einsum("pq,pqi->pi", w, before[slots])
            v = np.einsum("pq,pqi->pi", w, gv[slots])
            self.assertAlmostEqual(float(volume @ (v-v0)[:, 1]), j, places=14)
            self.assertEqual(s.project(mass, gv), 0.)
            s.transport(gv)
            self.assertAlmostEqual(b.positions[0, 1], .15, places=13)
            self.assertGreater(b.positions[1, 1], .15)
            self.assertGreater(b.positions[2, 1], .151)

    def test_crossing_only_stops_at_contact_and_allows_release(self):
        x = np.array([[.4, .155]])
        w, off, slots, mass, xy = prepare(x, np.array([1.]), 80)
        b = candidate.MaterialBoundary([0], np.array([[.4, .1501]]))
        s = b.bind(x, w, off, slots, 80, .15, .01)
        gv = np.tile([.012, -.02], (len(mass), 1))
        self.assertGreater(s.project(mass, gv), 0.)
        s.transport(gv)
        self.assertAlmostEqual(b.positions[0, 1], .15, places=14)
        gv[:, 1] = .03
        s = b.bind(x, w, off, slots, 80, .15, .01)
        self.assertEqual(s.project(mass, gv), 0.)
        s.transport(gv)
        self.assertGreater(b.positions[0, 1], .15)

    def test_unforced_affine_motion_reproduces_surface_velocity(self):
        x = np.array([[.35, .25], [.61, .28]])
        p = x + np.array([[-.001, -.002], [.0015, -.001]])
        grad = np.array([[.21, -.23], [.17, .13]])
        constant = np.array([.11, -.31])
        for grid in (80, 160):
            w, off, slots, _, xy = prepare(x, np.ones(2), grid)
            gv = xy @ grad.T + constant
            b = candidate.MaterialBoundary([0, 1], p)
            s = b.bind(x, w, off, slots, grid, .15, .01)
            np.testing.assert_allclose(s.coefficients.sum(axis=1), 1., atol=8e-15)
            s.transport(gv)
            np.testing.assert_allclose(b.positions, p + .01*(p @ grad.T + constant), rtol=0, atol=2e-16)

    def test_reference_disks_start_at_exact_physical_extent(self):
        for cells in (8, 12, 16, 24):
            x, ids, _ = solver.seed(cells)
            b = candidate.disk_boundary(solver, x, ids, cells)
            ibody = ids[b.owners] == 0
            center = solver.LO + solver.WIDTH / 14
            self.assertEqual(ibody.sum(), 256)
            np.testing.assert_allclose(np.linalg.norm(b.positions[ibody] - center, axis=1),
                                       solver.DIAMETER / 2, atol=3e-16, rtol=0)
            self.assertAlmostEqual(b.positions[ibody, 1].min(), center - solver.DIAMETER/2, places=15)
            self.assertTrue(np.all(np.bincount(ids[b.owners]) == 256))

    def test_interbody_kick_is_caught_by_second_floor_pass(self):
        # A six-point toy body exercises the normal native advance signature, not an F-arm trajectory.
        fake = type("SyntheticSolver", (), {})()
        fake.model, fake.WALL_SPEED, fake.LO, fake.WIDTH = solver.model, .02, .15, .5
        x = np.array([[.35, .15], [.355, .15], [.36, .15], [.35, .155], [.355, .155], [.36, .155]])
        volume = np.full(len(x), 1e-4)
        ids = np.zeros(len(x), dtype=int)
        affine = np.zeros((len(x), 2, 2))
        elastic = np.broadcast_to(np.eye(2), affine.shape).copy()
        called = []
        def kick(ids, nodes, mass, grad, vel, centers, friction):
            called.append(friction)
            vel[:, 1] -= .01
        fake.project_contacts = kick
        boundary = candidate.MaterialBoundary([0, 1, 2], x[:3])
        advance = candidate.make_advance(fake, 8, boundary=boundary)
        _, v, _, _, p = advance(x, np.zeros_like(x), affine, elastic, ids, volume, 80, .001, .65)
        self.assertEqual(called, [.5])
        self.assertEqual(advance.audit["floor_passes"], 2)
        self.assertEqual(advance.audit["positive_passes"], 1)
        self.assertGreater(p, 0.)
        self.assertAlmostEqual(float(volume @ v[:, 1]) + .01*sum(volume), p*.001*.5, places=14)
        self.assertAlmostEqual(boundary.positions[:, 1].min(), .15, places=14)

    def test_touching_contact_accepts_repeated_load_without_switching(self):
        x = np.array([[.4, .153], [.404, .153]])
        volume = np.array([1., 1.5])
        face = np.array([[.4, .15], [.404, .15]])
        b = candidate.MaterialBoundary([0, 1], face)
        v = np.zeros_like(x)
        for _ in range(20):
            w, off, slots, mass, _ = prepare(x, volume, 80)
            s = b.bind(x, w, off, slots, 80, .15, .001)
            gv = np.tile([0., -.02], (len(mass), 1))
            before = gv.copy()
            j = s.project(mass, gv)
            self.assertGreater(j, 0.)
            self.assertLessEqual(float(mass @ np.square(gv[:, 1])),
                                 float(mass @ np.square(before[:, 1])))
            self.assertAlmostEqual(float(mass @ (gv-before)[:, 1]), j, places=14)
            s.transport(gv)
            x = x + .001*np.einsum("pq,pqi->pi", w, gv[slots])
            np.testing.assert_allclose(b.positions[:, 1], .15, rtol=0., atol=3e-15)

    def test_overlapping_body_fields_do_not_share_floor_impulses(self):
        x = np.array([[.4, .151], [.4, .151]])
        fields = np.array([0, 1])
        w, off, slots, mass, _ = prepare(x, np.ones(2), 80, fields)
        b = candidate.MaterialBoundary([0, 1], np.array([[.4, .15], [.4, .15]]), fields)
        s = b.bind(x, w, off, slots, 80, .15, .001)
        gv = np.zeros((len(mass), 2))
        gv[slots[0], 1] = -.03
        gv[slots[1], 1] = .01
        initial = gv.copy()
        self.assertGreater(s.project(mass, gv), 0.)
        np.testing.assert_array_equal(gv[slots[1]], initial[slots[1]])
        s.transport(gv)
        self.assertAlmostEqual(b.positions[0, 1], .15, places=14)
        self.assertAlmostEqual(b.positions[1, 1], .15001, places=14)

    def test_native_top_and_both_side_reactions_preserved_exactly(self):
        # Both sides and the descending lid act on this toy strip well away from the floor.
        x = np.array([[solver.LO+.002, .601], [solver.LO+solver.WIDTH-.002, .601]])
        ids = np.zeros(2, dtype=int)
        volume = np.array([.0003, .0002])
        v = np.array([[-.04, .07], [.04, .07]])
        affine = np.zeros((2, 2, 2))
        elastic = np.broadcast_to(np.eye(2), affine.shape).copy()
        args = (x, v, affine, elastic, ids, volume, 80, .001, .6)
        baseline = solver.advance(*args)
        b = candidate.MaterialBoundary([0, 1], x.copy())
        advance = candidate.make_advance(solver, 8, boundary=b)
        observed = advance(*args)
        self.assertTrue(np.all(baseline[1][:, 1] < v[:, 1]))
        self.assertTrue(np.all(np.abs(baseline[1][:, 0]) < np.abs(v[:, 0])))
        for a, expected in zip(observed, baseline):
            np.testing.assert_array_equal(a, expected)
        self.assertEqual(advance.audit["positive_passes"], 0)

    def test_coupled_contact_matches_exhaustive_active_sets(self):
        # Independent tiny QP witness, including signed affine coefficients and duplicated rows.
        rng = np.random.default_rng(257)
        for case in range(30):
            N = rng.normal(.3, .27, (4, 6))
            N /= N.sum(axis=1, keepdims=True)
            limit = -rng.uniform(0., .03, len(N))
            if case % 3 == 0:
                N[-1] = N[0]
                limit[-1] = limit[0]
            mass = rng.uniform(.2, 2., N.shape[1])
            before = rng.normal(-.01, .1, len(mass))
            H = N / np.sqrt(mass)
            deficit = limit - N @ before
            answer = None
            for nactive in range(len(N) + 1):
                for active in itertools.combinations(range(len(N)), nactive):
                    rows = H[list(active)]
                    target = deficit[list(active)]
                    lam = np.linalg.lstsq(rows @ rows.T, target, rcond=None)[0]
                    z = rows.T @ lam
                    if (np.all(lam >= -1e-11) and np.all(H @ z >= deficit - 1e-11)
                            and np.allclose(rows @ z, target, atol=1e-11, rtol=0)):
                        answer = z / np.sqrt(mass)
                        break
                if answer is not None:
                    break
            self.assertIsNotNone(answer)
            slots = np.broadcast_to(np.arange(len(mass)), N.shape)
            indices, correction, impulse = candidate._project_rows(slots, N, mass, before, limit)
            np.testing.assert_allclose(correction, answer[indices], atol=3e-12, rtol=0)
            self.assertAlmostEqual(float(mass @ answer), impulse, places=11)


if __name__ == "__main__":
    unittest.main()
