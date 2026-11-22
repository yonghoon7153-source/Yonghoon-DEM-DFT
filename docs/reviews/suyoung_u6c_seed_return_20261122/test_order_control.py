"""Synthetic interface and readback checks for field label reversal."""
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import order_control as ctl


class OrderTests(unittest.TestCase):
    def test_native_receives_same_objects_and_one_relabelled_array(self):
        width = math.sqrt(49*math.pi*.05**2/.78)
        offsets = [(i*.00625,j*.00625) for i in range(-8,9) for j in range(-8,9)
                   if (i*.00625)**2 + (j*.00625)**2 <= .05**2]
        centers = [(.15+(i+.5)*width/7,.15+(j+.5)*width/7) for i in range(7) for j in range(7)]
        x = np.array([(a+i,b+j) for a,b in centers for i,j in offsets])
        ids = np.repeat(np.arange(49,dtype=np.int64),len(offsets))
        volume = np.full(len(ids), math.pi*.05**2/len(offsets))
        def original_seed(n):
            self.assertEqual(n,8)
            return x,ids,volume
        solver = SimpleNamespace(seed=original_seed)
        factory = lambda:solver
        calls = []
        def run_arm(arm,n,budget,out):
            calls.append((arm,n,budget,out))
            xx,mapped,vv = driver.fixed_solver().seed(n)
            self.assertIs(xx,x)
            self.assertIs(vv,volume)
            np.testing.assert_array_equal(48-mapped,ids)
            return {"status":"TIME_LIMIT"}
        driver = SimpleNamespace(fixed_solver=factory,run_arm=run_arm)
        result,geometry = ctl.integrate(driver, 2, Path("unused"))
        self.assertEqual(geometry,ctl.GEOMETRY)
        self.assertEqual(result["status"],"TIME_LIMIT")
        self.assertEqual(calls,[("F",8,2,Path("unused"))])
        self.assertIs(driver.fixed_solver,factory)
        self.assertIs(solver.seed,original_seed)
        x[0,0] += .001
        with self.assertRaisesRegex(ValueError,"INITIAL_GEOMETRY"):
            ctl.integrate(driver, 2, Path("unused"))
        self.assertIs(driver.fixed_solver,factory)
        self.assertIs(solver.seed,original_seed)

    def test_mapping_preserves_physical_row_order(self):
        ids = np.repeat(np.arange(49, dtype=np.int64), 197)
        expected = np.repeat(np.arange(48, -1, -1, dtype=np.int64), 197)
        mapped = ctl.reverse_ids(ids)
        np.testing.assert_array_equal(mapped, expected)
        np.testing.assert_array_equal(48-mapped, ids)
        self.assertEqual(hashlib.sha256(ids.tobytes()).hexdigest(), ctl.GEOMETRY["physical_ids"])
        with self.assertRaises(ValueError):
            ctl.reverse_ids(ids[::-1])

    def test_anchor_and_signed_first_peak(self):
        old = ctl.dt.Curve((0., 1., 2.), (0., 1., 2.))
        new = ctl.dt.Curve((0., .5, 1., 2.), (0., 1.5, 2., 1.))
        result = ctl.compare(old,new,2.)
        self.assertEqual(result["first_worst"]["u"], .5)
        self.assertEqual(result["first_worst"]["original_minus_relabelled_MPa"], -1.)
        self.assertEqual(result["at_fixed_anchor"]["original_minus_relabelled_MPa"], 1.)
        self.assertEqual(result["common_knots"],4)

    def test_no_extrapolation(self):
        old = ctl.dt.Curve((0., 1., 2.),(0., 1., 2.))
        short = ctl.dt.Curve((0., .75), (0., 1.))
        result = ctl.compare(old, short, 2.)
        self.assertEqual(result["anchor_status"],"NOT_REACHED")
        self.assertIsNone(result["at_fixed_anchor"])
        self.assertEqual(result["common_end_u"], .75)

    def test_zero_difference_is_measurable(self):
        old = ctl.dt.Curve((0.,1.),(0.,2.))
        r = ctl.compare(old,old,1.)
        self.assertEqual(r["max_abs_difference_MPa"], 0.)
        self.assertEqual(r["first_worst"]["u"], 0.)

    def test_wrong_prior_returns_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad = root/"wall.tar"
            bad.write_bytes(b"invalid")
            status = root/"status.json"
            self.assertEqual(ctl.read_command(bad,root/"arm",status),4)
            result = json.loads(status.read_bytes())
            self.assertEqual(result["status"],"INCOMPLETE")
            self.assertNotIn("comparison",result)

    def test_full_synthetic_receipt_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            arm = Path(tmp)
            width, dt = .71, .02
            trace = [",".join(ctl.dt.COLUMNS)]
            for step, p in enumerate((0.,.03,.13)):
                h = width-dt*step*ctl.dt.SPEED
                trace.append(f"{step},{dt*step},{h},{p},{49*math.pi*.05**2/(width*h)}")
            data = ("\n".join(trace)+"\n").encode()
            (arm/"trace.csv").write_bytes(data)
            native = {"protocol":ctl.dt.NATIVE,"arm":"F","cells":8,"steps":2,"status":"TARGET_BRACKETED",
                      "label":"DEVELOPMENT_ONLY","origin":"new","setting":1,"points_count":9653,
                      "source_sha256":{k:v for k,v in ctl.dt.SOURCE.items() if k!="suyoung_u6b_dev.py"},
                      "trace_sha256":ctl.dt.sha(data)}
            ctl.dt.write_json(arm/"result.json",native)
            receipt = ctl.make_receipt(arm,native,ctl.GEOMETRY)
            ctl.dt.write_json(arm/"order_control.json",receipt)
            ref = {"dt":dt,"width":width,"points_count":9653}
            self.assertEqual(ctl.load_arm(arm,ref)[0].p[-1],1.3)
            for overrides in ({"mapping":"identity"},{"geometry_sha256":{}},{"status":"TIME_LIMIT"}):
                altered = dict(receipt,**overrides)
                (arm/"order_control.json").write_text(json.dumps(altered))
                with self.assertRaises(ValueError):
                    ctl.load_arm(arm,ref)
            (arm/"order_control.json").write_text(json.dumps(receipt))
            (arm/"trace.csv").write_bytes(data+b"\n")
            with self.assertRaises(ValueError):
                ctl.load_arm(arm,ref)


if __name__=="__main__":
    unittest.main()
