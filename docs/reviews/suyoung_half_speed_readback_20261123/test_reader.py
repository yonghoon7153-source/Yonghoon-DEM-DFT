"""Synthetic readback checks plus optional verification of the author's existing archives."""
from pathlib import Path
import os
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reader


def arm(height, pressure, dt):
    n = len(height)
    return reader.Arm(height, pressure, [i*dt for i in range(n)],
                      [0.]+[.5]*(n-1),[0.]+[-.25]*(n-1),[i*.25 for i in range(n)],dt,1.,0.)


class Readback(unittest.TestCase):
    def test_interpolates_only_pressure(self):
        arms = {12:arm([1.,.75,.5],[0.,.4,.3],.5),24:arm([1.,.875,.75,.625,.5],[0.,.05,.1,.15,.2],.25)}
        subset = reader.pressure_curve(arms,[.875,.75])
        self.assertAlmostEqual(subset[0]["gap_MPa"],.15)
        self.assertIsNone(subset[0]["F12_step"])
        self.assertIsNone(reader.force_comparison(arms,subset[0]))
        self.assertEqual(subset[1]["F12_step"],1)
        with self.assertRaisesRegex(ValueError,"range"):
            reader.pressure_curve(arms,[.4])

    def test_native_and_equal_duration(self):
        arms = {12:arm([1.,.75,.5],[0.,.4,.3],.5),24:arm([1.,.875,.75,.625,.5],[0.,.05,.1,.15,.2],.25)}
        flow = reader.force_comparison(arms,reader.pressure_curve(arms,[.75])[0])
        self.assertEqual(flow["F24_equal_duration"]["steps"],[1,2])
        self.assertEqual(flow["F24"]["ratio"],2.)
        self.assertEqual(flow["gap"]["particle_delta_MPa"],flow["gap"]["wall_net_MPa"])
        arms[12].lid[1] = 0.
        self.assertIsNone(reader.window(arms[12],1,1)["ratio"])

    def test_absolute_peak_and_strict_crossing(self):
        curve = [dict(displacement_D=.0,F12_step=None,F24_step=0,F12_MPa=0.,F24_MPa=0.,gap_MPa=0.),
                 dict(displacement_D=.1,F12_step=None,F24_step=1,F12_MPa=0.,F24_MPa=.05*reader.REF_MPA,gap_MPa=-.05*reader.REF_MPA),
                 dict(displacement_D=.2,F12_step=None,F24_step=2,F12_MPa=0.,F24_MPa=.1,gap_MPa=-.1)]
        expected = dict(displacement_diameters=.2,F12_MPa=0.,F24_MPa=.1,signed_gap_MPa=-.1)
        summary = dict(samples=3,peak=expected,first_above=expected,fixed_reference_percent=100*.1/reader.REF_MPA)
        got = reader.summary_features({},curve,summary)
        self.assertEqual(got["first_above_5pct"]["F24_step"],2)
        self.assertLess(got["peak"]["gap_MPa"],0)
        with self.assertRaisesRegex(ValueError,"percentage"):
            reader.summary_features({},curve,dict(summary,fixed_reference_percent=5.))

    @unittest.skipUnless("HALF_SPEED_RESULT" in os.environ and "ORIGINAL_SPEED_RESULT" in os.environ,
                         "set paths to the two returned archives to check their wire identities")
    def test_existing_fixed_returns(self):
        current = Path(os.environ["HALF_SPEED_RESULT"])
        original = Path(os.environ["ORIGINAL_SPEED_RESULT"])
        with self.assertRaisesRegex(ValueError,"archive hash"):
            reader.evaluate(original,current)
        report = reader.evaluate(current,original)
        self.assertEqual([report[k]["samples"] for k in ("original_common","half_common","half_native")],[1139,1139,2277])
        self.assertEqual(report["half_common"]["peak"],report["half_native"]["peak"])
        self.assertGreater(report["half_common"]["peak_pct"],5)
        self.assertEqual(report["first_observed_impulses"]["half"]["F24"]["first_positive_floor"]["step"],977)
        for row in report["same_clock_diagnostic"]:
            self.assertAlmostEqual(row["original"]["displacement_D"],2*row["half"]["displacement_D"])
            for label in ("original", "half"):
                gaps = row[label]["signed_wall_gaps_MPa"]
                self.assertAlmostEqual(gaps["floor_MPa"],row[label]["floor_gap_MPa"])
                self.assertAlmostEqual(gaps["floor_MPa"],gaps["lid_down_MPa"]+gaps["wall_net_MPa"])


if __name__ == "__main__":
    unittest.main()
