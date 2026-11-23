"""Manufactured walking clocks and native-runner wiring, with no particle simulation."""
from contextlib import contextmanager
import csv
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
import quarter_speed as q


def import_frozen(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


here=Path(__file__).resolve().parent
frozen=here.parent/"suyoung_half_speed_readback_20261123"
depth=import_frozen("depth_test_reference",frozen/"depth_prefix.py")
frozen_half=here.parent/"suyoung_material_lid_return_20261123"
hs=import_frozen("half_test_reference",frozen_half/"half_speed.py")


@contextmanager
def override(obj, **kwargs):
    old = {k:getattr(obj,k) for k in kwargs}
    try:
        for k,v in kwargs.items(): setattr(obj,k,v)
        yield
    finally:
        for k,v in old.items(): setattr(obj,k,v)


def fake_traces(n, scale):
    return [dict(step=str(i),height=str(1.0-(i/scale)/n/16),bottom_pressure_E=str(.02*i/scale/n),
                 time_code=str(i/n/16),phi_m=str(.5/(1.0-(i/scale)/n/16))) for i in range(2*n*scale+1)]


def encode(rows):
    buf=io.StringIO(newline="")
    w=csv.DictWriter(buf,tuple(rows[0]),lineterminator="\n"); w.writeheader(); w.writerows(rows)
    return buf.getvalue().encode()


class Tests(unittest.TestCase):
    def test_common_schedule_includes_original_odd_fine_knots(self):
        old=fake_traces(2,1)
        quarter={12:fake_traces(1,4),24:fake_traces(2,4)}
        quarter[12][2]["bottom_pressure_E"]=".7"
        report=q.shared_knots(quarter,old,1.,1.,(1,4))
        self.assertEqual(report["samples"],5)
        self.assertEqual(report["peak"]["step_F24_original"],1)
        self.assertEqual(report["peak"]["step_F12_quarter"],2)
        self.assertEqual(report["peak"]["step_F24_quarter"],4)
        self.assertAlmostEqual(report["peak"]["signed_gap_MPa"],6.9)
        quarter[12][2]["height"]=".8"
        with self.assertRaisesRegex(ValueError,"height"):
            q.shared_knots(quarter,old,1.,1.,(1,4))

    def test_quarter_is_relative_to_original(self):
        self.assertEqual(q.schedule(.5,.25),.125)
        with self.assertRaisesRegex(ValueError,"speed"):
            q.schedule(.5,.125)
        self.assertEqual(q.STEPS,{12:2276,24:4552})
        self.assertEqual(q.MARKS,{12:(1860,2276),24:(3720,4552)})

    def test_native_driver_gets_original_seed_api_and_restores_speed(self):
        native=SimpleNamespace(STEPS={12:3}, BUDGET={12:20}, paired_trace=None)
        ctx=SimpleNamespace(solver=SimpleNamespace(WALL_SPEED=.5,LO=0.,WIDTH=1.))
        fine=SimpleNamespace(initial=lambda c,n:("seed",n))
        material_points=np.array([[0,.1],[0,.5],[0,.9]])
        v=np.zeros_like(material_points)
        class Stub:
            last_step=dict(step=1,floor_impulse=.5,lid_signed_impulse=-.25)
            def __call__(self,x,v,*others):
                return x[::-1],v+np.array([[0.,.5],[0.,-.25],[0.,0.]]),None,None,None
        model=SimpleNamespace(make_advance=lambda *a,**k:Stub())
        def native_run(f,c,observed,reference,identity,n,dest):
            self.assertEqual(f.initial(c,n),("seed",12))
            self.assertEqual(c.solver.WALL_SPEED,.125)
            self.assertEqual(native.BUDGET,q.BUDGET)
            self.assertEqual(native.STEPS,q.STEPS)
            self.assertEqual(reference[12],b"previous")
            self.assertEqual(n,12)
            dest.mkdir()
            observer=observed.make_advance()
            observer(material_points,v,None,None,None,np.ones(3),120,.25,.95)
        native.run_arm=native_run
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/"F12"
            with patch.object(q,"read_arm",return_value=(None,None,None,{"status":"stub"})):
                q.run_arm(depth,hs,native,fine,ctx,model,{12:b"previous"},dict(quarter_wall_speed=.125),12,dest)
            self.assertEqual(json.loads((dest/"quarter_speed_receipt.json").read_bytes()),{"status":"stub"})
            self.assertEqual(json.loads((dest/"layer_spec.json").read_bytes())["counts"],[1,1,1])
            observed=next(csv.DictReader((dest/"particle_momentum.csv").read_text().splitlines()))
            self.assertEqual(float(observed["particle_delta_Py"]),.25)
            layer=next(csv.DictReader((dest/"layer_steps.csv").read_text().splitlines()))
            self.assertEqual([float(layer[k+"_delta"]) for k in depth.LAYERS],[.5,-.25,0.])
            self.assertEqual(ctx.solver.WALL_SPEED,.5)
            self.assertEqual(native.STEPS,{12:3})

    def test_zero_plate_reading_is_not_contact(self):
        trace=fake_traces(1,1)
        walls=[dict(floor_impulse="0",lid_downward_impulse="1",floor_gap_after=".2"),
               dict(floor_impulse=".1",lid_downward_impulse="1",floor_gap_after="0")]
        events=q.onsets(walls,trace,1.)
        self.assertEqual(events["first_floor_impulse"]["step"],2)
        self.assertEqual(events["first_floor_gap_within_tolerance"]["step"],2)
        self.assertEqual(events["first_lid_impulse"]["step"],1)
        walls[1]["floor_impulse"]="0"
        self.assertIsNone(q.onsets(walls,trace,1.)["first_floor_impulse"])


if __name__=="__main__":
    unittest.main()
