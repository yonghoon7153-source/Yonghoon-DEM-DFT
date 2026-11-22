"""Synthetic regressions for the signed product decomposition."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("factors", Path(__file__).with_name("pressure_factors.py"))
factors = importlib.util.module_from_spec(spec)
spec.loader.exec_module(factors)


def wall(mass, speed):
    return {"M": mass, "mean_down": speed, "J": 0. if speed is None else mass * speed, "count": int(mass > 0)}


def row(pre, post, dt):
    return {"step": 1, "u": 1., "pre": pre, "post": post, "p_MPa": 10 * (pre["J"] + post["J"]) / dt}


class PressureFactors(unittest.TestCase):
    empty = wall(0., None)

    def split(self, coarse, fine, dt8=1., dt16=1.):
        return factors.breakdown(row(coarse, self.empty, dt8), row(fine, self.empty, dt16), dt8, dt16, 1.)

    def test_equal_rate_different_dt(self):
        parts = self.split(wall(2., 3.), wall(1., 2.), 1., .5)["contributions"]
        self.assertEqual(parts, {"mass_rate_MPa": 0., "speed_MPa": 20., "one_sided_MPa": 0.})

    def test_both_factors_and_reverse(self):
        a, b = wall(2., 3.), wall(1., 1.)
        parts = self.split(a, b)["contributions"]
        self.assertEqual(parts, {"mass_rate_MPa": 20., "speed_MPa": 30., "one_sided_MPa": 0.})
        self.assertEqual(self.split(b, a)["contributions"], {key: -v for key, v in parts.items()})

    def test_missing_speed_on_one_or_both_sides(self):
        a = wall(2., 1.)
        for first, second, expected in ((a, self.empty, 20.), (self.empty, a, -20.)):
            self.assertEqual(self.split(first, second)["contributions"],
                             {"mass_rate_MPa": 0., "speed_MPa": 0., "one_sided_MPa": expected})
        self.assertIsNone(self.split(self.empty, self.empty)["signed_percent"])

    def test_cancellation_across_wall_applications(self):
        c = row(wall(.5, 1.), wall(.5, 3.), 1.)
        f = row(wall(1., 1.), wall(.5, 1.), 1.)
        result = factors.breakdown(c, f, 1., 1., 1.)
        self.assertEqual(result["F8_minus_F16_MPa"], 5.)
        self.assertEqual(result["signed_percent"], {"mass_rate_MPa": -100., "speed_MPa": 200., "one_sided_MPa": 0.})

    def test_requires_matched_native_displacement_and_total(self):
        c = row(wall(2., 2.), self.empty, 1.)
        f = row(wall(1., 1.), self.empty, 1.)
        for faulty in (dict(f, u=0.), dict(f, p_MPa=f["p_MPa"] + .125)):
            with self.assertRaises(ValueError):
                factors.breakdown(c, faulty, 1., 1., 1.)


if __name__ == "__main__":
    unittest.main()
