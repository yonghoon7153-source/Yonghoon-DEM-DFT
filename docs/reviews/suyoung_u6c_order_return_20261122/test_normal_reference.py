import itertools
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normal_reference import solve


class NormalReference(unittest.TestCase):
    def test_two_body_inelastic_only_in_normal_direction(self):
        v, meta = solve([(-1, 0), (1, 0)], [1, 2], [(3, 4), (0, 5)])
        np.testing.assert_allclose(v, [(1, 4), (1, 5)], atol=1e-12)
        np.testing.assert_allclose(meta['pair_impulses'], [2.])
        self.assertAlmostEqual(meta['objective'], 3.)

    def test_separating_pair_preserves_velocity(self):
        old = [(-1, 9), (1, -2)]
        v, meta = solve([(-1, 0), (1, 0)], [1, 3], old)
        np.testing.assert_array_equal(v, old)
        self.assertEqual(meta['pair_impulses'], [0.])

    def test_all_permutations_same_three_body_reference(self):
        pos = np.array([[-.8,-.5],[1.2,-.3],[.1,.9]])
        vel = np.array([[.9,.3],[-.6,.1],[.25,-.8]])
        mass = np.array([1.,1.5,.75])
        v, _ = solve(pos, mass, vel)
        for order in itertools.permutations(range(3)):
            perm = list(order)
            trial, meta = solve(pos[perm], mass[perm], vel[perm])
            np.testing.assert_allclose(v[perm], trial, atol=1e-12, rtol=0)
            self.assertGreaterEqual(min(meta['final_separating_speed']), -1e-12)
            self.assertGreaterEqual(min(meta['pair_impulses']), -1e-12)

    def test_symmetric_radial_collapse_comes_to_rest(self):
        pos = np.array([[1.,0.],[-.5,np.sqrt(3)/2],[-.5,-np.sqrt(3)/2]])
        v, _ = solve(pos, np.ones(3), -pos)
        np.testing.assert_allclose(v, 0., rtol=0, atol=1e-12)


if __name__ == '__main__':
    unittest.main()
