"""Test fixed material groups, signed momentum and frozen driver wiring using manufactured particles."""
from contextlib import contextmanager
import csv
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
import depth_prefix as depth


def csv_bytes(records):
    out=io.StringIO(newline="")
    writer=csv.DictWriter(out,tuple(records[0]),lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return out.getvalue().encode("ascii")


def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("ascii"),newline="")))


@contextmanager
def override(obj,**values):
    before={k:getattr(obj,k) for k in values}
    try:
        for k,v in values.items(): setattr(obj,k,v)
        yield
    finally:
        for k,v in before.items(): setattr(obj,k,v)


class Tests(unittest.TestCase):
    def test_groups_boundaries_and_empty_group(self):
        obs=depth.LayerObservation(None,0.,1.,None,None)
        y=np.array([0.,1/3,2/3,1.])
        obs.group(np.column_stack([y*0,y]),np.ones(4))
        self.assertEqual(list(obs.labels),[0,1,2,2])
        self.assertEqual(obs.spec["masses"],[1.,1.,2.])
        for bad in (np.array([-.01,.5,.9]), np.array([0.,.2,1.])):
            with self.assertRaises(ValueError):
                obs.group(np.column_stack([bad*0,bad]),np.ones(len(bad)))

    def test_rejects_unbalanced_or_changed_external_impulse(self):
        class Bad:
            last_step=dict(step=1,floor_impulse=1.,lid_signed_impulse=0.)
            def __call__(self,x,v,*rest): return x,v,None,None,None
        x=np.array([[0,.1],[0,.5],[0,.9]])
        v=np.zeros_like(x)
        ref=[dict(step="1",particle_Py_before="0",particle_Py_after="0",wall_signed_J="1")]
        fn=depth.LayerObservation(Bad(),0.,1.,ref,lambda row:None)
        with self.assertRaisesRegex(ValueError,"wall momentum"):
            fn(x,v,None,None,None,np.ones(3),0,.1,.99)
        ref[0]["wall_signed_J"]="0"
        with self.assertRaisesRegex(ValueError,"historical"):
            fn(x,v,None,None,None,np.ones(3),0,.1,.99)

    def test_complete_production_wrapper_on_manufactured_fields(self):
        # The three material points swap their geometric layers after step one.
        # A fresh grouping at step two would attribute the acceleration to the wrong layer.
        solver=SimpleNamespace(LO=0.,WIDTH=1.,WALL_SPEED=.5)
        ctx=SimpleNamespace(solver=solver)
        x=np.array([[0.,.1],[0.,.5],[0.,.9]])
        ids=np.array([0,1,2])
        mass=np.ones(3)
        trace=b"height,bottom_pressure_E\n1.,0\n.99,0\n.98,0\n"
        wall=[dict(step=i,floor_impulse=.5,lid_signed_impulse=-.25) for i in (1,2)]
        motion=[dict(step=str(i),particle_Py_before=str(.25*(i-1)),particle_Py_after=str(.25*i),wall_signed_J=".25") for i in (1,2)]
        expect={12:(trace,csv_bytes(wall),motion)}
        class Advance:
            step=0
            def __call__(self,coords,v,*args):
                self.step+=1
                self.last_step=wall[self.step-1]
                return coords[::-1].copy(),v+np.array([[0,.5],[0,-.25],[0,0.]]),None,None,None
        model=SimpleNamespace(make_advance=lambda *args:Advance())
        native=SimpleNamespace(STEPS={},BUDGET={},rows=rows)
        def native_run(fine,context,wrapper,previous,ident,n,dest):
            self.assertEqual(context.solver.WALL_SPEED,.25)
            self.assertEqual(native.BUDGET,{12:600,24:1200})
            self.assertEqual(native.STEPS,{12:2})
            # Frozen native.receipt adds these keys.
            self.assertNotIn("label",ident)
            dest.mkdir()
            fn=wrapper.make_advance()
            coords,v=x,np.zeros_like(x)
            for i in (1,2):
                coords,v,_,_,_=fn(coords,v,None,None,ids,mass,0,.1,.99)
            (dest/"trace.csv").write_bytes(previous[n])
            (dest/"wall_steps.csv").write_bytes(csv_bytes(wall))
        native.run_arm=native_run
        with tempfile.TemporaryDirectory() as temp,patch.object(depth,"STEPS",{12:2}):
            dest=Path(temp)/"F12"
            depth.run_arm(SimpleNamespace(override=override),native,None,ctx,model,expect,
                          dict(half_speed=.25,label="DEVELOPMENT_ONLY"),12,dest)
            self.assertEqual(solver.WALL_SPEED,.5)
            rec=json.loads((dest/"layer_receipt.json").read_bytes())
            self.assertEqual(rec["layer_spec"]["counts"],[1,1,1])
            records=depth.verify_arm(native,dest,12,expect[12])
            self.assertEqual([records[-1][k+"_after"] for k in depth.LAYERS],[1.,-.5,0.])
            self.assertEqual(records[-1]["whole_after"],.5)
            txt=(dest/"layer_steps.csv").read_bytes()
            (dest/"layer_steps.csv").write_bytes(txt.replace(b"-0.25",b"-0.2",1))
            with self.assertRaises(ValueError):
                depth.verify_arm(native,dest,12,expect[12])
            (dest/"layer_steps.csv").write_bytes(txt)
            (dest/"trace.csv").write_bytes(trace+b"\n")
            with self.assertRaisesRegex(ValueError,"native pressure"):
                depth.verify_arm(native,dest,12,expect[12])

    def test_signed_sums_and_identical_duration_window(self):
        def series(n,count):
            records=[]
            for i in range(1,count+1):
                each={layer+"_before":0. for layer in depth.LAYERS} if i==1 else {
                      layer+"_before":records[-1][layer+"_after"] for layer in depth.LAYERS}
                for layer,rate in zip(depth.LAYERS,(1.,-.5,.25)):
                    each[layer+"_after"]=each[layer+"_before"]+rate/n
                each.update(whole_before=.75*(i-1)/n,whole_after=.75*i/n,floor_J=1./n,lid_signed_J=-.25/n)
                records.append(each)
            return records
        with patch.object(depth,"SAMPLES",((2,4),)):
            s=depth.summarize({12:series(1,2),24:series(2,4)},{12:.5,24:.25},1.)[0]
        self.assertEqual(s["F12"]["middle_delta_MPa"],-10.)
        self.assertEqual(s["F12_minus_F24_equal_duration"]["whole_delta_MPa"],0.)
        self.assertEqual(sum(s["F12"][k+"_delta_MPa"] for k in depth.LAYERS),s["F12"]["whole_delta_MPa"])


if __name__=="__main__":
    unittest.main()
