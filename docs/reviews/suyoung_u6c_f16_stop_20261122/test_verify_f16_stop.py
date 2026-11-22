"""Receipt regressions on a read-only capture and small in-memory mutations."""
import argparse
import copy
import importlib.util
import json
import math
from pathlib import Path
import tarfile
import unittest


spec=importlib.util.spec_from_file_location("receipt_reader",Path(__file__).with_name("verify_f16_stop.py"))
r=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class StopReceipt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tarfile.open(ARGS.result,mode="r:gz") as ar:
            cls.trace=r.read_member(ar,"run/F16/trace.csv")
            cls.stop=json.loads(r.read_member(ar,"run/F16/contact_stop.json"))
            cls.inc=json.loads(r.read_member(ar,"run/F16/incomplete.json"))
            cls.sums=r.read_member(ar,"run/SOURCE_SHA256SUMS")

    def test_original_incomplete_return(self):
        result=r.check(ARGS)
        self.assertEqual((result["readback"],result["stop"]["rows"],result["stop"]["node"]),
                         ("VERIFIED_INCOMPLETE",4803,16810))
        self.assertEqual(result["F8_F16"],{"comparison":"HOLD","ratio":None,"reason":"F16_INCOMPLETE"})
        self.assertFalse(result["u6_qualified"])
        self.assertFalse(result["stage3_go"])
        self.assertEqual(result["new_field_executions_by_readback"],0)

    def test_caps_and_scope_cannot_be_promoted(self):
        for key,value in (("stage3_go",True),("u6_qualified",True),("status","TARGET_BRACKETED")):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,"STOP_DISPOSITION"):
                r.verify_stop(self.stop,dict(self.inc,**{key:value}),self.trace)

    def test_partial_trace_binding_and_step_gaps(self):
        truncated=b"".join(self.trace.splitlines(True)[:-1])
        with self.assertRaisesRegex(ValueError,"PARTIAL_TRACE_BINDING"):
            r.verify_stop(self.stop,self.inc,truncated)
        with self.assertRaisesRegex(ValueError,"TRACE_LENGTH"):
            r.trace_rows(truncated,4802)
        lines=self.trace.splitlines(True)
        del lines[1]
        with self.assertRaisesRegex(ValueError,"TRACE_STEP_SEQUENCE"):
            r.trace_rows(b"".join(lines),4802)

    def test_native_residual_and_branch_identity_checked(self):
        for key,value,reason in (("residual",0.,"TERMINAL_RESIDUAL"),("speed_tol",1.,"TERMINAL_RESIDUAL"),
                                 ("iteration",513,"NODE_IDENTITY"),("node_id",2976,"NODE_IDENTITY")):
            bad=copy.deepcopy(self.stop)
            bad["nodes"][0][key]=value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,reason):
                r.verify_stop(bad,self.inc,self.trace)

    def test_partial_pressure_grid_has_no_cap_crossing(self):
        def dummy(p):
            w,t=r.WIDTH,r.DT
            h=w-t*r.SPEED
            area=49*math.pi*.05**2
            return (f"step,time_code,height,bottom_pressure_E,phi_m\n0,0,{w},0,{area/w**2}\n"
                    f"1,{t},{h},{p},{area/(w*h)}\n").encode("ascii")
        self.assertEqual(r.trace_rows(dummy(.11),1),2)
        for p in (.12,-.01,math.nan):
            with self.assertRaisesRegex(ValueError,"INCOMPLETE_BEFORE_PRESSURE_TARGET"):
                r.trace_rows(dummy(p),1)

    def test_source_identity_and_manifest_names(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_MANIFEST_SHA"):
            r.verify_source(self.sums+b"\n",ARGS.repo,ARGS.source_tar)
        for names in (["../other"],["thing","thing"],["/file"],["w\\x"]):
            data="".join("0"*64+"  "+name+"\n" for name in names).encode("ascii")
            with self.assertRaisesRegex(ValueError,"MANIFEST_FORMAT"):
                r.manifest(data)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--result",type=Path,required=True)
    p.add_argument("--repo",type=Path)
    p.add_argument("--source-tar",type=Path)
    ARGS,rest=p.parse_known_args()
    unittest.main(argv=["test_verify_f16_stop.py",*rest],verbosity=2)
