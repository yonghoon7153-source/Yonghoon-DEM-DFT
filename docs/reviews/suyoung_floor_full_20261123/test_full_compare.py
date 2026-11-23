"""Synthetic native trajectories for the complete F8/F16 readback only."""
import csv
import io
import unittest

import full_compare as r


def trace(pressures, dt):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(("step", "time_code", "height", "bottom_pressure_E", "phi_m"))
    for step, p in enumerate(pressures):
        time = step * dt
        writer.writerow((step, time, 1.0 - time, p, 0.78 / (1.0 - time)))
    return stream.getvalue().encode("ascii")


def analyse(p8, p16, **overrides):
    opts = dict(width=1., speed=1., dt8=.0625, dt16=.03125,
                terminal8="GEOMETRY_LIMIT", terminal16="GEOMETRY_LIMIT")
    opts.update(overrides)
    return r.compare_pair(trace(p8, opts["dt8"]), trace(p16, opts["dt16"]), **opts)


class TestFullCompare(unittest.TestCase):
    def test_checked_units_native_odd_knot_peak_and_matches(self):
        result = analyse([0,.01,.02,.03,.04], [0,.005,.01,.015,.02,.07,.03,.035,.04])
        self.assertEqual(result["common"]["samples"], 9)
        self.assertAlmostEqual(result["common"]["max_abs_difference_MPa"], .45)
        self.assertEqual(result["common"]["first_worst"]["u"], 5/32)
        self.assertEqual(result["common"]["first_worst"]["F8_native"], False)
        self.assertAlmostEqual(result["fine_peak_on_common_support_MPa"], .7)
        self.assertAlmostEqual(result["fixed_reference_MPa"], .6636991103)
        self.assertEqual(result["both_positive_knots"]["samples"], 8)
        self.assertEqual(result["common"]["first_worst"]["F16_native"], True)
        self.assertEqual(result["arms"]["F8"]["first_positive"]["step"], 1)

    def test_different_endpoints_no_extrapolation(self):
        result = analyse([0,.01,.06,.14], [0,.01,.02,.03,.04,.05,.06,.07,.08],
                         terminal8="TARGET_BRACKETED")
        self.assertEqual(result["common"]["end_u"], 3/16)
        self.assertEqual(result["common"]["samples"], 7)
        self.assertAlmostEqual(result["fine_peak_on_common_support_MPa"], .6)
        self.assertEqual(result["arms"]["F16"]["last_positive"]["step"], 8)
        self.assertEqual(result["arms"]["F8"]["last_positive"]["step"], 3)

    def test_zero_fine_and_zero_pair_no_contact(self):
        result = analyse([0]*5, [0]*9)
        self.assertEqual(result["common"]["fine_peak_comparison"], "HOLD_ZERO_REFERENCE")
        self.assertEqual(result["common"]["fixed_reference_comparison"], "WITHIN")
        self.assertEqual(result["both_positive_knots"]["samples"], 0)
        self.assertIsNone(result["arms"]["F16"]["first_positive"])
        self.assertFalse(result["u6_qualified"])
        self.assertFalse(result["stage3_go"])

    def test_within_each_fine_vs_fixed_reference_reported_separately(self):
        result = analyse([0,.08,.08,.08,.08], [0,.04375,.08375,.081875,.08,.08,.08,.08,.08])
        self.assertEqual(result["common"]["fixed_reference_comparison"], "EXCEEDS")
        self.assertEqual(result["common"]["fine_peak_comparison"], "WITHIN")

    def test_strict_earliest_crossing_and_terminal(self):
        with self.assertRaises(ValueError):
            analyse([0,.12,.11,.12], [0]*9, terminal8="TARGET_BRACKETED")
        with self.assertRaises(ValueError):
            analyse([0,.01,.02], [0]*9, terminal8="GEOMETRY_LIMIT")
        with self.assertRaises(ValueError):
            analyse([0,.01,.02], [0]*9, terminal8="TARGET_BRACKETED")
        with self.assertRaises(ValueError):
            analyse([0,.01,.02], [0]*9, terminal8="TIME_LIMIT")

    def test_rejects_invalid_samples_and_clocks(self):
        valid8 = trace([0]*5, .0625)
        valid16 = trace([0]*9, .03125)
        for changed in (valid8.replace(b"1,0.0625", b"1,0.0624"),
                        valid8.replace(b"2,0.125", b"3,0.125"), valid8 + b"\r\n,\r\n",
                        valid8.replace(b"0,0.0,1.0,0,", b"0,0.0,1.0,nan,"),
                        valid8.replace(b"0,0.0,1.0,0,", b"0,0.0,1.0,0.001,")):
            with self.subTest(raw=changed), self.assertRaises(ValueError):
                r.compare_pair(changed, valid16, width=1., speed=1., dt8=.0625, dt16=.03125,
                               terminal8="GEOMETRY_LIMIT", terminal16="GEOMETRY_LIMIT")
        with self.assertRaises(ValueError):
            analyse([0]*5, [0]*9, dt16=.03)

    def test_equality_counts_as_within(self):
        self.assertFalse(r.exceeds(.015625, .3125))
        self.assertTrue(r.exceeds(.015625000000000003, .3125))


if __name__ == "__main__":
    unittest.main()
