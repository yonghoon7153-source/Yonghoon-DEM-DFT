"""Synthetic regressions of the offline readback only."""
import importlib.util
import math
from pathlib import Path
import unittest

s=importlib.util.spec_from_file_location("independent_reader",Path(__file__).with_name("verify_f8_pair.py"))
r=importlib.util.module_from_spec(s)
s.loader.exec_module(r)


class ReadbackContract(unittest.TestCase):
    def fixture(self,pressures=(0.,.02,.12),mutate=lambda i,h:h):
        width,dt=.7,.001
        speed=.034*math.sqrt(1/(2*(1+.45)))
        parts=["step,time_code,height,bottom_pressure_E,phi_m"]
        for i,p in enumerate(pressures):
            t=i*dt
            h=mutate(i,width-t*speed)
            phi=49*math.pi*.05**2/(width*h)
            parts.append(f"{i},{t!r},{h!r},{p!r},{phi!r}")
        data=("\n".join(parts)+"\n").encode("ascii")
        native={"status":"TARGET_BRACKETED","setting":1,"cells":8,"arm":"F","label":"DEVELOPMENT_ONLY",
                "trace_sha256":r.sha(data),"steps":len(pressures)-1}
        return data,native,width,dt,10.

    def test_pressure_conversion_and_first_bracket(self):
        curve=r.parse_native(*self.fixture())
        self.assertEqual([p for u,p in curve],[0.,.2,1.2])

    def test_checksum_and_native_schedule_are_both_required(self):
        data,results,*metadata=self.fixture()
        with self.assertRaisesRegex(ValueError,"identity"):
            r.parse_native(data+b"\n",results,*metadata)
        with self.assertRaisesRegex(ValueError,"schedule"):
            r.parse_native(*self.fixture(mutate=lambda i,h:h+.0001 if i==1 else h))

    def test_earlier_crossing_and_terminal_undershoot_rejected(self):
        for ps in ((0.,.12,.13),(0.,.03,.11)):
            with self.assertRaisesRegex(ValueError,"first bracket"):
                r.parse_native(*self.fixture(ps))

    def test_equal_steps_need_equal_displacements(self):
        a=[(0.,0.),(.2,.3),(.3,.4)]
        b=[(0.,0.),(.1,.3),(.3,.4)]
        with self.assertRaisesRegex(ValueError,"grid"):
            r.shared((a,b))

    def test_common_support_truncates_longer_tail(self):
        a=[(0.,0.),(.1,.4),(.2,500.)]
        b=[(0.,0.),(.1,.3)]
        ds,i=r.delta(a,b)
        self.assertEqual((len(ds),i),(2,1))
        self.assertAlmostEqual(ds[i],.1)

    def test_interpolation_only_within_support(self):
        curve=[(0.,0.),(.5,1.),(1.,3.)]
        self.assertEqual(r.at(curve,.75),2.)
        self.assertEqual(r.at(curve,1.),3.)
        self.assertIsNone(r.at(curve,1.01))
        self.assertIsNone(r.at(curve,-.01))

    def test_peak_metadata_including_negative_sign_and_ties(self):
        a=[(0.,.2),(.05,.5),(.1,.4)]
        b=[(0.,.45),(.05,.25),(.1,.4)]
        expected={"samples":3,"start_u":0.,"end_u":.1,"max_abs_MPa":.25,
                  "first_worst":{"step":0,"u":0.,"original_MPa":.2,"reversed_MPa":.45,
                                 "original_minus_reversed_MPa":-.25},"at_fixed_anchor":None}
        self.assertEqual(r.check_pair(a,b,expected)[1],0)
        expected["first_worst"]["step"]=1
        with self.assertRaisesRegex(ValueError,"pair metadata"):
            r.check_pair(a,b,expected)

    def test_qualification_stays_false(self):
        record={"label":"DEVELOPMENT_ONLY","stage3_go":False,"u6_qualified":False}
        r.no_go(record)
        for key in ("stage3_go","u6_qualified"):
            for rejected in (True,0,None):
                with self.assertRaisesRegex(ValueError,"qualification"):
                    r.no_go(dict(record,**{key:rejected}))


if __name__=="__main__":
    unittest.main(verbosity=2)
