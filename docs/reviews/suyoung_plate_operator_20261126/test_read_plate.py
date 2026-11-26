"""Edge cases for the saved-trace diagnostic. No solver is imported."""
import runpy
import unittest
from pathlib import Path

reader = runpy.run_path(str(Path(__file__).with_name("read_plate.py")))


class PlateReadbackTests(unittest.TestCase):
    def test_crossing_is_strict_and_reports_both_native_samples(self):
        r = reader["crossing"]([0.0,0.008,0.0081], [0.,2.,4.], [0.,1.,2.])
        self.assertEqual((r["previous_step"],r["step"],r["previous_u"],r["u"]), (1,2,2.,4.))
        self.assertIsNone(reader["crossing"]([0.,0.008], [0.,1.], [0.,1.]))

    def test_tied_extrema_across_boundary_preserve_signs(self):
        coarse = ([0.,1.,2.,3.],[0.,2.,0.,1.])
        fine = ([0.,1.,2.,3.],[0.,1.,1.,1.])
        r = reader["compare"](coarse,fine,2.)
        self.assertEqual(r["location"],"MIXED")
        self.assertEqual([p["coarse_minus_fine_MPa"] for p in r["overall"]["ties"]],[1.,-1.])
        self.assertEqual(r["after"]["first_u"],2.)

    def test_both_windows_use_common_fine_peak(self):
        r = reader["compare"](([0.,1.,2.],[0.,2.,4.]), ([0.,1.,2.,3.],[0.,1.,4.,80.]), 2.)
        self.assertEqual(r["fine_peak_MPa"],4.)
        self.assertEqual(r["before"]["percent"],25.)
        self.assertEqual(r["overall"]["n"],3)
        self.assertEqual(r["location"],"BEFORE")

    def test_absent_detection_holds_its_attribution(self):
        curve=([0.,1.],[0.,1.])
        r = reader["compare"](curve,curve,None)
        self.assertEqual(r["location"],"HOLD")
        self.assertIsNone(r["after"])

    def test_union_includes_fine_only_extremum(self):
        r = reader["compare"](([0.,2.],[0.,2.]), ([0.,1.,2.],[0.,0.,2.]), 1.)
        self.assertEqual((r["overall"]["first_u"],r["overall"]["percent"],r["location"]),(1.,50.,"AFTER"))


if __name__ == "__main__":
    unittest.main()
