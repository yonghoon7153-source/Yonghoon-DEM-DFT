"""Finite boundary tests for the offline grid comparison; no model import."""
import argparse
import copy
import importlib.util
import json
import math
from pathlib import Path
import tarfile
import unittest


s=importlib.util.spec_from_file_location("grid",Path(__file__).with_name("verify_first_grid.py"))
r=importlib.util.module_from_spec(s)
s.loader.exec_module(r)


class FirstGrid(unittest.TestCase):
    def test_accepted_full_result_bytes_and_prior_bindings(self):
        out=r.run(ARGS)
        self.assertEqual(out["F8_F16"]["comparison"],"EXCEEDS")
        self.assertEqual(out["F8_F16"]["union_knots"],5319)
        self.assertEqual(out["F12_F24"]["comparison"],"HOLD")
        self.assertFalse(out["stage3_go"])
        self.assertFalse(out["u6_qualified"])

    def test_exact_limit_and_adjacent_binary_values(self):
        f=[(0.,0.),(1.,20.)]
        for last,expected in ((math.nextafter(21.,20.),"WITHIN"),(21.,"WITHIN"),(math.nextafter(21.,22.),"EXCEEDS")):
            self.assertEqual(r.evaluate(([(0.,0.),(1.,last)],f))["comparison"],expected)

    def test_coarse_only_knots_and_fine_peak_within_shared_range(self):
        c=[(0.,0.),(.25,1.),(.5,0.)]
        f=[(0.,0.),(.4,1.),(1.,4.)]
        x=r.evaluate((c,f))
        self.assertEqual(x["union_knots"],4)
        self.assertAlmostEqual(x["fine_peak_MPa"],1.5)
        self.assertEqual(x["common_end_u"],.5)
        self.assertEqual(x["u_at_first_max_abs"],.5)

    def test_unusable_reference_and_invalid_support(self):
        self.assertEqual(r.evaluate(([(0.,0.),(1.,2.)],[(0.,0.),(1.,0.)]))["reason"],"ZERO_REFERENCE")
        for f in ([(0.,0.),(0.,1.)],[(0.,0.),(1.,math.nan)],[(1.,1.)]):
            with self.assertRaisesRegex(ValueError,"invalid curve"):
                r.evaluate(([(0.,0.),(1.,2.)],f))

    def valid(self):
        with tarfile.open(ARGS.result) as ar:
            report=json.loads(r.entry(ar,"run/grid_comparison.json"))
            curves=[]
            for n in (8,16):
                stem=f"run/F{n}/"
                curves.append(r.samples(r.entry(ar,stem+"trace.csv"),json.loads(r.entry(ar,stem+"result.json")),n))
        return report,curves

    def test_rounded_ratio_and_wrong_incidence_are_detected(self):
        x,curves=self.valid()
        for k,bad in (("exceeding_knots",1),("ratio",.81),("u_at_first_max_abs",.05)):
            forged=copy.deepcopy(x)
            forged["pairs"]["F8_F16"][k]=bad
            with self.assertRaisesRegex(ValueError,"registered pair result mismatch"):
                r.verify_pair_report(forged,curves)

    def test_missing_pair_and_approval_flags_cannot_be_upgraded(self):
        x,curves=self.valid()
        for k in ("u6_qualified","stage3_go"):
            with self.assertRaisesRegex(ValueError,"scope"):
                r.verify_pair_report(dict(x,**{k:True}),curves)
        x["pairs"]["F12_F24"]["comparison"]="WITHIN"
        with self.assertRaisesRegex(ValueError,"registered pair"):
            r.verify_pair_report(x,curves)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    for key in ("result","source","old-f8","old-f16-stop"):
        p.add_argument("--"+key,type=Path,required=True)
    p.add_argument("--repo",type=Path)
    ARGS,rest=p.parse_known_args()
    unittest.main(argv=["test_verify_first_grid.py",*rest],verbosity=2)
