"""Analytic and fixed-kernel checks for the manufactured flat stress component."""
import importlib.util
import os
from pathlib import Path
import unittest

import numpy as np


HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location("flat_patch", HERE.with_name("flat_patch.py"))
patch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)


class FlatPatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = os.environ.get("SUYOUNG_PATCH_SOURCE_ROOT", HERE.parents[3])
        cls.model, cls.cross = patch.load_pinned_sources(root)
        cls.slab = patch.common_slab()

    def test_common_quadrature_integrates_area_and_first_depth_moment(self):
        _, v, z = self.slab
        self.assertTrue(np.all(v > 0.))
        self.assertAlmostEqual(v.sum(), .4*.025, places=14)
        self.assertAlmostEqual(v @ z, .4*.025**2/2, places=14)

    def test_uniform_stress_has_same_transfer(self):
        for grid in (80, 160):
            with self.subTest(grid=grid):
                reading = patch.sample(self.model, self.cross, self.slab, grid, 1., 0.)
                self.assertAlmostEqual(reading["measured_MPa"], 9.0625, places=11)

    def test_linear_manufactured_field_recovers_positive_analytic_difference(self):
        coarse, fine = [patch.sample(self.model, self.cross, self.slab, g, 1., 8.)
                        for g in (80, 160)]
        self.assertAlmostEqual(coarse["measured_MPa"], 9.575, places=11)
        self.assertAlmostEqual(fine["measured_MPa"], 9.31875, places=11)
        self.assertAlmostEqual(coarse["measured_MPa"]-fine["measured_MPa"], .25625, places=11)

    def test_reversing_gradient_reverses_resolution_shift(self):
        coarse, fine = [patch.sample(self.model, self.cross, self.slab, g, 1., -8.)
                        for g in (80, 160)]
        self.assertAlmostEqual(coarse["measured_MPa"]-fine["measured_MPa"], -.25625, places=11)


if __name__ == "__main__":
    unittest.main()
