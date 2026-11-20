"""Manufactured checks only; the 49-disk development load is author-run."""
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import suyoung_u6_first_dev as u


class PilotChecks(unittest.TestCase):
    def test_resolution_keeps_geometry_and_reference_amount(self):
        for resolution in (12, 16):
            x, ids, vol = u.seed(resolution)
            self.assertEqual(len(np.unique(ids)), 49)
            np.testing.assert_allclose(np.bincount(ids, weights=vol), np.full(49, np.pi * .05**2))
            self.assertAlmostEqual(vol.sum() / u.WIDTH**2, .78)
            self.assertEqual(len(x), len(vol))

    def test_interpolation_and_no_extrapolation(self):
        self.assertAlmostEqual(u.first_crossing(0.1, 0.14, 1., .8, .12), .9)
        self.assertIsNone(u.first_crossing(.05, .10, 1., .9, .12))
        self.assertIsNone(u.first_crossing(.14, .1, .9, .8, .12))

    def test_contact_approach_and_separation(self):
        m = np.ones(2)
        ids = np.array([0, 1])
        nodes = np.array([5, 5])
        g = np.array([[-1., 0.], [1., 0.]])
        centers = g.copy()
        for initial, expected in (([1., -1.], [0., 0.]), ([-1., 1.], [-1., 1.])):
            v = np.column_stack((initial, [0., 0.]))
            u.project_contacts(ids, nodes, m, g, v, centers, .5)
            np.testing.assert_allclose(v[:, 0], expected)

    def test_floor_impulse_only_and_unilateral_lid(self):
        xy = np.array([[.5, u.LO], [.5, u.LO + u.WIDTH], [.5, u.LO], [.5, .5]])
        v = np.array([[0., -2.], [0., 3.], [0., 2.], [0., 1.]])
        j = u.walls(np.ones(4), xy, v, u.LO + u.WIDTH, -.1)
        self.assertEqual(j, 2.)
        np.testing.assert_allclose(v[:, 1], [0., -.1, 2., 1.])

    def test_decision_uses_phi_only(self):
        def arm(n, phi):
            return dict(status='TARGET_BRACKETED', cells=n, phi_m=phi, protocol=u.PROTOCOL)
        self.assertEqual(u.assess(arm(12, .8), arm(16, .803)), 'WITHIN_DEVELOPMENT_BAND')
        self.assertEqual(u.assess(arm(12, .8), arm(16, .81)), 'OUTSIDE_DEVELOPMENT_BAND')
        self.assertEqual(u.assess(arm(12, .8), arm(12, .803)), 'INCOMPLETE')
        self.assertEqual(u.assess(arm(12, .8), dict(status='TIME_LIMIT')), 'INCOMPLETE')

    def test_sparse_transfer_matches_reference_for_manufactured_overlap(self):
        # Two local fields, synthetic points, one time step. No campaign arm.
        from unittest.mock import patch
        x = np.array([[.47, .49], [.48, .50], [.50, .49], [.51, .50]])
        ids = np.array([0,0,1,1])
        v = np.array([[.02,0.], [.02,0.], [-.02,0.], [-.02,0.]])
        f = np.tile(np.eye(2), (4,1,1))
        f[:,0,0] = 1.001
        c = np.zeros_like(f)
        grid = 32
        vol = np.full(4, (.5/grid)**2)
        dt = .0002
        lid = u.LO + u.WIDTH
        result = u.advance(x, v, c, f, ids, vol, grid, dt, lid)
        old = dict(x=x.copy(), v=v.copy(), C=c.copy(), F=f.copy(), ids=ids)
        with patch.multiple(u.model, LEFT=u.LO, RIGHT=u.LO+u.WIDTH, FLOOR=u.LO):
            u.model.step(old, 'F', grid, dt, lid, -u.WALL_SPEED, .5)
        for actual, key in zip(result, ('x','v','C','F')):
            np.testing.assert_allclose(actual, old[key], atol=1e-13, rtol=1e-12)
        self.assertEqual(result[4], 0.)

    def test_three_field_shared_node_matches_reference(self):
        ids = np.arange(3)
        m = np.array([1.,2.,3.])
        g = np.array([[-1.,0.],[0.,1.],[1.,0.]])
        v = np.array([[1.,.3],[0.,-.5],[-1.,.2]])
        baseline = v[:,None,:].copy()
        u.model.contact(m[:,None], baseline, g[:,None,:], g, .5)
        u.project_contacts(ids, np.zeros(3, dtype=int), m, g, v, g, .5)
        np.testing.assert_allclose(v, baseline[:,0], atol=1e-14)

    def test_timeout_record_cannot_yield_a_selection(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            dest = Path(root)/'synthetic'
            u.run(12, dest, 0)
            report = json.loads((dest/'result.json').read_text())
            self.assertEqual(report['status'], 'TIME_LIMIT')
            self.assertIsNone(report['phi_m'])
            self.assertEqual(report['steps_attempted'], 0)

    def test_material_identity(self):
        matrix = np.eye(2)[None]
        np.testing.assert_allclose(u.model.stress(matrix), np.zeros_like(matrix))
        np.testing.assert_allclose(u.model.plastic_project(matrix), matrix)
        self.assertAlmostEqual(u.model.YIELD, .04 * np.sqrt(2/3))


if __name__ == '__main__':
    unittest.main()
