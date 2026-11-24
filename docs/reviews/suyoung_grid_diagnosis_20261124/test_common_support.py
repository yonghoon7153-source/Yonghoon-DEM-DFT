"""Synthetic arithmetic checks. No simulation or returned curves are used."""
import importlib.util
import unittest
from pathlib import Path


def load_reader():
    spec = importlib.util.spec_from_file_location("read_common_support", Path(__file__).with_name("read_common_support.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CommonSupportTests(unittest.TestCase):
    def test_different_ends_denominators_and_signed_shifts(self):
        reader = load_reader()
        old = [[(0., 0.), (1., 3.), (2., 6.)], [(0., 0.), (1., 2.), (2., 3.)]]
        new = [[(0., 0.), (0.5, 2.5), (1., 4.)], [(0., 0.), (1., 1.), (2., 5.)]]
        with reader.official_readers(Path(__file__).resolve().parents[3]) as (rule, _):
            result = reader.decompose(rule, old, new)
        self.assertEqual(result["common_knots"], 3)
        self.assertEqual(result["common_end_u"], 1.)
        self.assertAlmostEqual(result["A"], 1.)
        self.assertAlmostEqual(result["B"], 1.5)
        self.assertAlmostEqual(result["C"], -.5)
        self.assertLessEqual(abs(result["closure_residual"]), 1.e-12)
        self.assertEqual(len(result["matched_extrema"]), 1)
        point = result["matched_extrema"][0]
        self.assertEqual((point["delta_coarse_MPa"], point["delta_fine_MPa"]), (1., -1.))

    def test_earliest_distinct_maxima_and_interpolation(self):
        reader = load_reader()
        old = [[(0.,0.), (1.,3.), (2.,4.)], [(0.,0.), (2.,4.)]]
        new = [[(0.,0.), (2.,6.)], [(0.,0.), (1.,3.), (2.,4.)]]
        with reader.official_readers(Path(__file__).resolve().parents[3]) as (rule, _):
            result = reader.decompose(rule, old, new)
        self.assertEqual([p["u"] for p in result["matched_extrema"]], [1.,2.])
        self.assertEqual(result["matched_extrema"][0]["old_fine_MPa"], 2.)
        self.assertAlmostEqual(result["A"], .25)

    def test_zero_reference_on_joint_interval_holds(self):
        reader = load_reader()
        old = [[(0.,0.), (1.,2.), (2.,3.)], [(0.,0.), (1.,0.), (2.,1.)]]
        new = [[(0.,0.), (1.,2.)], [(0.,0.), (1.,1.)]]
        with reader.official_readers(Path(__file__).resolve().parents[3]) as (rule, _):
            with self.assertRaisesRegex(ValueError, "common reference"):
                reader.decompose(rule, old, new)


if __name__ == "__main__":
    unittest.main()
