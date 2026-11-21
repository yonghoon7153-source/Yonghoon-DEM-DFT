"""Synthetic regression tests for returned force/displacement curves."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("doubling", Path(__file__).with_name("doubling.py"))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class CurveTests(unittest.TestCase):
    def test_same_straight_line_with_different_step_grids(self):
        m = d.compare([(0., 0.), (.5, 1.), (1., 2.)],
                      [(0., 0.), (.25, .5), (.75, 1.5), (1., 2.)])
        self.assertEqual(m["max_abs_difference_MPa"], 0.)
        self.assertEqual(m["u_at_first_max_abs"], 0.)
        self.assertEqual(m["union_knots"], 5)

    def test_interior_peak_only_on_fine_grid(self):
        m = d.compare([(0., 0.), (1., 0.)],
                      [(0., 0.), (.375, 8.), (1., 0.)])
        self.assertEqual(m["max_abs_difference_MPa"], 8.)
        self.assertEqual(m["u_at_first_max_abs"], .375)
        self.assertEqual(m["min_coarse_minus_fine_MPa"], -8.)
        self.assertEqual(m["max_coarse_minus_fine_MPa"], 0.)

    def test_common_support_interpolates_its_endpoint_without_extension(self):
        m = d.compare([(0., 0.), (.5, 1.), (1., 2.)],
                      [(0., 0.), (.75, 0.)])
        self.assertEqual(m["common_end_u"], .75)
        self.assertEqual(m["end_u_coarse_minus_fine"], .25)
        self.assertEqual(m["coarse_samples_in_common"], 2)
        self.assertEqual(m["union_knots"], 3)
        self.assertEqual(m["coarse_minus_fine_at_common_end_MPa"], 1.5)
        self.assertEqual(m["u_at_first_max_abs"], .75)

    def test_unknown_or_unsorted_displacement_is_rejected(self):
        for samples in [[(.1, 0.), (1., 1.)], [(0., 0.), (0., 1.)],
                        [(0., 0.), (1., float("nan"))], [(0., 0.)]]:
            with self.subTest(samples=samples), self.assertRaises(ValueError):
                d.compare(samples, [(0., 0.), (1., 1.)])


if __name__ == "__main__":
    unittest.main()
