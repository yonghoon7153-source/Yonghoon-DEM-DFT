"""Manufactured contacts and knots; this suite does not advance a particle solver."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify_pressure import Arm, REF, arrival, delay_diagnostic, native_union, pair_window, statistics


class PressureReadback(unittest.TestCase):
    def test_interpolates_actual_height_and_rejects_distinct_endpoints(self):
        coarse=Arm([1,.5],[0.,1.],[],[],[])
        fine=Arm([1,.875,.5],[0.,.1,.2],[],[],[])
        sample=native_union({12:coarse,24:fine})[1]
        self.assertAlmostEqual(sample["F12_MPa"],.25)
        self.assertAlmostEqual(sample["gap_MPa"],.15)
        coarse.height[-1]=.4
        with self.assertRaisesRegex(ValueError,"native heights"):
            native_union({12:coarse,24:fine})

    def test_threshold_is_strict_and_absolute(self):
        values=[dict(gap_MPa=x) for x in (.05*REF,-.06*REF,.03*REF)]
        result=statistics(values)
        self.assertIs(result["first_above"],values[1])
        self.assertAlmostEqual(result["max_percent"],6.)
        self.assertIsNone(statistics(values[:1])["first_above"])

    def test_native_and_equal_duration_signed_balance(self):
        def make(pairs, width, times):
            increment=0.
            walls,momentum=[],[]
            for a,b in pairs:
                walls.append(dict(floor_impulse=a,lid_signed_impulse=b))
                start=increment
                increment+=a+b
                momentum.append(dict(particle_Py_before=start,particle_Py_after=increment))
            return Arm([width],[],times,walls,momentum)
        coarse=make([(2.,-1.)],2.,[0.,1.])
        fine=make([(.6,-.3),(1.4,-.7)],2.,[0.,.5])
        windows=pair_window({12:coarse,24:fine},2)
        self.assertAlmostEqual(windows["F12_minus_F24"]["floor_MPa"],-4.)
        self.assertAlmostEqual(windows["F12_minus_F24"]["direct_momentum_MPa"],-2.)
        self.assertAlmostEqual(windows["F12_minus_F24_same_duration"]["floor_MPa"],0.)
        self.assertIsNone(pair_window({12:coarse,24:fine},1))

    def test_first_actual_force_agrees_with_gap(self):
        walls=[dict(floor_impulse="0",floor_gap_after=".1"),dict(floor_impulse=".07",floor_gap_after="0")]
        arm=Arm([1.,.99,.98],[],[0.,.02,.04],walls,[])
        self.assertEqual(arrival(arm)["step"],2)
        self.assertAlmostEqual(arrival(arm)["displacement_D"],.2)
        walls[0]["floor_gap_after"]="0"
        with self.assertRaisesRegex(ValueError,"different steps"):
            arrival(arm)

    def test_signed_onset_shift_uses_overlap_and_records_interpolated_markers(self):
        c=Arm([1.,.8,.6,.4],[0.,1.,2.,3.],[0.,1.,2.,3.],[],[])
        f=Arm([1.,.9,.8,.7,.6,.5,.4],[-.5,0.,.5,1.,1.5,2.,2.5],[i*.5 for i in range(7)],[],[])
        out=delay_diagnostic(c,f,1,3,6,2)
        self.assertEqual(out["at_first_common_crossing"]["aligned_F24_step"],3)
        self.assertEqual((out["F12_first_step"],out["F12_last_step"],out["comparison_samples"]),(0,2,3))
        self.assertAlmostEqual(out["same_time_peak"]["same_time_gap_MPa"],.5)
        self.assertAlmostEqual(out["aligned_peak"]["aligned_gap_MPa"],0.)
        self.assertTrue(out["at_original_native_peak"]["F12_interpolated"])
        self.assertAlmostEqual(out["at_original_native_peak"]["aligned_gap_MPa"],0.)
        self.assertIsNone(out["at_original_common_peak"])
        rev=delay_diagnostic(c,f,-1,0,6)
        self.assertEqual((rev["F12_first_step"],rev["F12_last_step"]),(1,3))
        self.assertAlmostEqual(rev["aligned_peak"]["aligned_gap_MPa"],1.)
        self.assertFalse(rev["use_for_qualification"])
        with self.assertRaisesRegex(ValueError,"no common native F12 support"):
            delay_diagnostic(c,f,10,0,0)


if __name__=="__main__":
    unittest.main()
