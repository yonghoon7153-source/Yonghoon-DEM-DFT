"""Synthetic boundaries and a one-row fixture. Never advances a field."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import unittest


s=importlib.util.spec_from_file_location("field_grid_reader", Path(__file__).with_name("read_f8_f16.py"))
r=importlib.util.module_from_spec(s)
s.loader.exec_module(r)


class GridContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rule=r.get_rule(REPO)

    def compare(self,coarse,fine):
        report=r.blank_report()
        rc=r.apply(self.rule,report,coarse,fine)
        self.assertIs(report["u6_qualified"],False)
        self.assertIs(report["stage3_go"],False)
        self.assertEqual(report["pairs"]["F12_F24"]["comparison"],"HOLD")
        return rc,report["pairs"]["F8_F16"],report["development_grid_comparison"]

    def test_unrounded_5_percent_including_equality(self):
        for y,expected in ((math.nextafter(21.,20.),"WITHIN"),(21.,"WITHIN"),
                           (math.nextafter(21.,22.),"EXCEEDS")):
            rc,pair,combined=self.compare([(0.,0.),(1.,y)],[(0.,0.),(1.,20.)])
            self.assertEqual((rc,pair["comparison"]),(0,expected))
            self.assertEqual(combined,"EXCEEDS" if expected=="EXCEEDS" else "HOLD")

    def test_union_includes_coarse_only_and_fine_only_peaks(self):
        _,pair,_=self.compare([(0.,0.),(.25,6.),(1.,10.)],[(0.,0.),(.5,3.),(1.,10.)])
        self.assertEqual((pair["union_knots"],pair["fine_peak_MPa"],pair["u_at_first_max_abs"]),(4,10.,.25))
        self.assertEqual(pair["max_abs_difference_MPa"],4.5)

    def test_fine_denominator_ends_at_shared_cutoff(self):
        _,pair,_=self.compare([(0.,0.),(.5,4.5)],[(0.,0.),(.25,2.),(1.,8.)])
        self.assertEqual((pair["common_end_u"],pair["union_knots"],pair["fine_peak_MPa"]),(.5,3,4.))
        self.assertEqual((pair["max_abs_difference_MPa"],pair["ratio"]),(.5,.125))

    def test_invalid_axis_and_zero_reference_hold(self):
        for fine in ([(0.,0.),(.2,2.),(.2,4.)],[(0.,0.),(1.,0.)],[(0.,0.),(1.,math.nan)]):
            rc,pair,combined=self.compare([(0.,0.),(1.,1.)],fine)
            self.assertEqual((rc,pair["comparison"],combined),(2,"HOLD","HOLD"))

    def test_final_f8_original_identity(self):
        r.verify_source(REPO)
        curve,proof=r.read_f8(F8)
        self.assertEqual((len(curve),proof["trace_sha256"],proof["archive_sha256"]),
                         (2660,r.F8_TRACE,r.F8_ARCHIVE))
        self.assertEqual(curve[-1][0],.11925565145330064)

    def test_changed_f8_bytes_are_rejected_before_unpack(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"changed.tar.gz"
            p.write_bytes(F8.read_bytes()+b"\n")
            with self.assertRaisesRegex(ValueError,"FINAL_F8_ARCHIVE_IDENTITY"):
                r.read_f8(p)

    def fixture(self,folder):
        # Generate CSV bytes plus an adapter-format receipt from prescribed (fabricated) reactions.
        adapter=r.module(REPO/r.ADAPTER,"f16_fixture_adapter")
        dt,w,speed=r.DT[16],r.WIDTH,r.SPEED
        h=w-dt*speed
        rows=["step,time_code,height,bottom_pressure_E,phi_m",f"0,0,{w},0,{49*math.pi*.05**2/w**2}",
              f"1,{dt},{h},0.12,{49*math.pi*.05**2/(w*h)}"]
        trace=("\n".join(rows)+"\n").encode("ascii")
        native=dict(arm="F",budget_s=1740.,cells=16,elapsed_s=0.,label="DEVELOPMENT_ONLY",
                    origin="new",points_count=39053,protocol="U6b-setting1-bottom-loading-v1",
                    setting=1,source_sha256={k:r.BASE[k] for k in ("dem_suyoung_sf2d_dev.py","suyoung_u6_first_dev.py")},
                    status="TARGET_BRACKETED",steps=1,trace_sha256=r.digest(trace))
        (folder/"trace.csv").write_bytes(trace)
        (folder/"result.json").write_text(json.dumps(native),encoding="ascii")
        receipt=adapter.receipt(adapter.modules(REPO),folder,native,1,adapter.GEOMETRY)
        (folder/"candidate.json").write_text(json.dumps(receipt),encoding="ascii")
        return trace,native,receipt

    def test_synthetic_f16_complete_adapter_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            self.fixture(p)
            curve,proof=r.read_f16(REPO,p)
            self.assertEqual((len(curve),curve[-1][1],proof["points"],proof["steps"]),(2,1.2,39053,1))
            _,pair,_=self.compare([(0.,0.),(curve[-1][0],1.2)],curve)
            self.assertEqual((pair["comparison"],pair["fine_peak_MPa"]),("WITHIN",1.2))

    def test_wrong_scope_counts_lineage_and_field_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            _,_,original=self.fixture(folder)
            for mutation in ({"u6_qualified":True},{"mapping":"REVERSED"},{"cells":8},{"candidate_calls":2},
                             {"candidate_sha256":"0"*64},{"f8_archive_sha256":"0"*64},
                             {"geometry_sha256":dict(original["geometry_sha256"],field_ids=r.EXPECTED_IDS[8])}):
                with self.subTest(key=next(iter(mutation))):
                    (folder/"candidate.json").write_text(json.dumps(dict(original,**mutation)),encoding="ascii")
                    with self.assertRaises(ValueError):
                        r.read_f16(REPO,folder)

    def test_incomplete_marker_and_truncated_trace_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            self.fixture(folder)
            (folder/"incomplete.json").write_bytes(b"{}")
            with self.assertRaises(ValueError):
                r.read_f16(REPO,folder)
            (folder/"incomplete.json").unlink()
            (folder/"trace.csv").write_bytes((folder/"trace.csv").read_bytes().splitlines(True)[0])
            with self.assertRaises(ValueError):
                r.read_f16(REPO,folder)

    def test_rehashed_native_cannot_skip_target_or_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            trace,native,_=self.fixture(Path(tmp))
            for changed in (trace.replace(b",0.12,",b",0.11,"), trace.replace(b"\n1,",b"\n2,")):
                with self.assertRaises(ValueError):
                    r.native_curve(changed,dict(native,trace_sha256=r.digest(changed)),16)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--f8",type=Path,required=True)
    args,remaining=parser.parse_known_args()
    REPO,F8=args.repo,args.f8
    unittest.main(argv=["test_read_f8_f16.py",*remaining],verbosity=2)
