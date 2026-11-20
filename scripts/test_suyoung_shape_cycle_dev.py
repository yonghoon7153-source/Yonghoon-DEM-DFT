"""Synthetic checks for the unqualified two-dimensional shape development cycle."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dem_suyoung_sf2d_dev as model
try:
    import suyoung_shape_cycle_dev as cycle
except ModuleNotFoundError as exc:
    if exc.name != "suyoung_shape_cycle_dev":
        raise
    cycle = None


class ShapeCycleTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(cycle, "phase cycle implementation required")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_same_loading_then_fixed_relax_rise_and_hold(self):
        schedule = list(cycle.schedule())
        loading = schedule[:1200]
        self.assertEqual([(e.top, e.velocity) for e in loading],
                         [(model.TOP0 - .15*.0005*i, -.15) for i in range(1,1201)])
        for entry in schedule[1200:1800]:
            self.assertEqual((entry.phase, entry.top, entry.velocity), ("RELAX", loading[-1].top, 0.))
        rise = schedule[1800:3400]
        self.assertTrue(all(e.phase=="LIFT" and e.velocity==.15 for e in rise))
        self.assertTrue(all(b.top > a.top for a,b in zip(rise,rise[1:])))
        self.assertEqual({(e.phase,e.top,e.velocity) for e in schedule[3400:]},
                         {("POST_LIFT", rise[-1].top, 0.)})
        self.assertEqual([e.step for e in schedule], list(range(1,4001)))

    def test_release_evidence_counts_after_compression_and_requires_clear_window(self):
        def r(i, phase, pressure, gap):
            return dict(step=i, phase=phase, plate_pressure=pressure, cell_gap=gap)
        seq = [r(1,"LOAD",1.,-.01),r(2,"RELAX",0.,-.01),r(3,"LIFT",0.,.01),
               r(4,"POST_LIFT",.1,.01),r(5,"POST_LIFT",0.,.01),r(6,"POST_LIFT",0.,.01)]
        result = cycle.release_evidence(seq,2)
        self.assertEqual(result["first_zero_pressure_step"],2)
        self.assertEqual(result["first_positive_cell_gap_step"],3)
        self.assertEqual(result["last_positive_pressure_step"],4)
        self.assertEqual(result["clear_tail_steps"],2)
        self.assertTrue(result["separated_in_final_window"])
        for seq2 in (seq[:-1], seq[:-1]+[r(6,"POST_LIFT",0.,0.)],
                     [r(1,"LOAD",0.,0.)]+seq[1:]):
            self.assertFalse(cycle.release_evidence(seq2,2)["separated_in_final_window"])

    def test_gap_uses_carried_cell_extent_as_well_as_point_centers(self):
        x = np.array([[.4,.7],[.6,.6]])
        total = np.tile(np.eye(2),(2,1,1))
        total[0,1] = [-2.,3.]
        center, geom = cycle.wall_gaps(x,total,.73,32)
        self.assertAlmostEqual(center,.03)
        self.assertAlmostEqual(geom,.03-.25/32*5)
        self.assertLess(geom,0.)

    def test_rising_wall_only_projects_closing_velocity(self):
        mass=np.ones((1,3))
        velocity=np.array([[[0.,-.02],[0.,.02],[0.,.4]]])
        coords=np.array([[.5,.8],[.5,.8],[.5,.8]])
        impulse=model.boundary(mass,velocity,coords,.79,.15)
        self.assertAlmostEqual(impulse,.25)
        np.testing.assert_array_equal(velocity[0,:,1],[-.02,.02,.15])

    def test_one_continuous_state_and_real_frame_order_in_both_arms(self):
        schedule=list(cycle.schedule((2,2,2,2)))
        for arm in ("S","F"):
            seed = Mock(wraps=model.initial_state)
            seen=[]
            def kernel(state, *args):
                seen.append(id(state))
                return model.step(state,*args)
            path=self.root/arm
            res=cycle.run_arm(arm,path,counts=(2,2,2,2),initialize=seed,advance=kernel)
            self.assertEqual(seed.call_count,1)
            self.assertEqual(len(set(seen)),1)
            self.assertEqual(len(seen),8)
            self.assertEqual(len(res["transitions"]),3)
            self.assertTrue(all(a["before_sha256"]==a["after_sha256"] for a in res["transitions"]))
            frames=res["frames"]
            self.assertEqual([f["step"] for f in frames],[0,2,4,5,6,8])
            with (path/"trace.csv").open(newline="") as f:
                trace = list(csv.DictReader(f))
            for frame in frames:
                i=frame["step"]
                raw=(path/frame["file"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(),frame["sha256"])
                with np.load(path/frame["file"],allow_pickle=False) as data:
                    self.assertEqual(float(data["top_code"]),schedule[i-1].top if i else model.TOP0)
                    self.assertEqual(int(data["step"]),i)
                    if i==0:
                        ids=data["particle_id"].copy()
                        total=np.tile(np.eye(2),(len(ids),1,1))
                        self.assertIsNone(frame["plate_pressure"])
                    else:
                        self.assertEqual(frame["plate_pressure"],float(trace[i-1]["plate_pressure"]))
                        self.assertEqual(frame["cell_gap"],float(trace[i-1]["cell_gap"]))
                    np.testing.assert_array_equal(data["particle_id"],ids)
                    np.testing.assert_array_equal(data["point_id"],np.arange(len(ids)))
                    self.assertEqual(data["F_total"].shape,total.shape)
            # Short synthetic loading produces no sustained loaded-to-separated event.
            self.assertFalse(res["release"]["separated_in_final_window"])
        code=cycle.compare(self.root)
        self.assertEqual(code,4)
        self.assertTrue((self.root/"shape_pair.svg").is_file())
        self.assertFalse(json.loads((self.root/"comparison.json").read_text())["u6_qualified"])

    def test_observer_is_passive_on_short_compression(self):
        out=self.root/"F"
        result=cycle.run_arm("F",out,counts=(4,2,2,2))
        physical=model.initial_state(32)
        for entry in list(cycle.schedule((4,2,2,2)))[:4]:
            model.step(physical,"F",32,.0005,entry.top,entry.velocity,.20)
        frame=next(f for f in result["frames"] if f["step"]==4)
        with np.load(out/frame["file"]) as z:
            for name, expected in (("x",physical["x"]),("v",physical["v"]),("C",physical["C"]),
                                   ("F_elastic",physical["F"]),("particle_id",physical["ids"])):
                np.testing.assert_array_equal(z[name],expected)

    def test_partial_or_changed_frame_is_not_compared(self):
        for arm in ("S","F"):
            cycle.run_arm(arm,self.root/arm,counts=(2,2,2,2))
        path=next((self.root/"S").glob("frame*.npz"))
        path.write_bytes(b"changed")
        with self.assertRaises(ValueError):
            cycle.compare(self.root)
        self.assertFalse((self.root/"comparison.json").exists())

    def test_false_clear_tail_summary_rejected_against_bound_trace(self):
        for arm in ("S","F"):
            cycle.run_arm(arm,self.root/arm,counts=(2,2,2,2))
        name=self.root/"S"/"arm.json"
        report=json.loads(name.read_bytes())
        report["release"]["separated_in_final_window"]=True
        name.write_text(json.dumps(report))
        with self.assertRaises(ValueError):
            cycle.compare(self.root)

    def test_budget_and_existing_output_fail_without_complete_receipt(self):
        out=self.root/"cap"
        t=iter([0.,999.])
        with self.assertRaises(TimeoutError):
            cycle.run_arm("F",out,counts=(1,1,1,1),clock=lambda:next(t))
        self.assertFalse((out/"arm.json").exists())
        with self.assertRaises(FileExistsError):
            cycle.run_arm("S",out,counts=(1,1,1,1))

    def test_imported_kernel_bytes_checked_before_either_entrypoint(self):
        fake=self.root/"candidate.py"
        fake.write_bytes(b"old kernel")
        seed=Mock(side_effect=AssertionError("started a calculation"))
        out=self.root/"trial"
        with patch.object(model,"__file__",str(fake)):
            with self.assertRaisesRegex(ValueError,"kernel"):
                cycle.run_arm("F",out,initialize=seed)
            with self.assertRaisesRegex(ValueError,"kernel"):
                cycle.compare(self.root)
        seed.assert_not_called()
        self.assertFalse(out.exists())

    def test_same_omitted_or_relabelled_frame_on_both_arms_is_rejected(self):
        originals={}
        for arm in ("S","F"):
            originals[arm]=cycle.run_arm(arm,self.root/arm,counts=(2,2,2,2))
        for scenario in ("omit_mid_lift","relabel_load"):
            for arm in ("S","F"):
                r=json.loads(json.dumps(originals[arm]))
                if scenario=="omit_mid_lift":
                    r["frames"].pop(3)
                else:
                    r["frames"][1]["phase"]="POST_LIFT"
                (self.root/arm/"arm.json").write_text(json.dumps(r))
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValueError):
                    cycle.compare(self.root)

    def test_nonfinite_gap_and_negative_pressure_rejected_during_readback(self):
        for arm in ("S","F"):
            cycle.run_arm(arm,self.root/arm,counts=(2,2,2,2))
        path=self.root/"S"/"trace.csv"
        original=path.read_text()
        for key,value in (("cell_gap","nan"),("plate_pressure","-1")):
            rows=list(csv.DictReader(original.splitlines()))
            rows[0][key]=value
            with path.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
            report=self.root/"S"/"arm.json"
            r=json.loads(report.read_bytes())
            r["trace_sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
            report.write_text(json.dumps(r))
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError,"reaction|clearance"):
                    cycle.compare(self.root)


if __name__=="__main__":
    unittest.main()
