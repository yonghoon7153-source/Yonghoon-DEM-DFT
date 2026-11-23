"""Exercise the observation wrapper on manufactured fields with the pinned depth observer."""
import argparse
import base64
from contextlib import contextmanager
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
import original_layer as app


def table(records):
    stream=io.StringIO(newline="")
    w=csv.DictWriter(stream,list(records[0]),lineterminator="\n")
    w.writeheader()
    w.writerows(records)
    return stream.getvalue().encode("ascii")


def parse(data):
    return list(csv.DictReader(io.StringIO(data.decode("ascii"))))


@contextmanager
def override(obj,**changes):
    previous={k:getattr(obj,k) for k in changes}
    try:
        for k,v in changes.items():
            setattr(obj,k,v)
        yield
    finally:
        for k,v in previous.items():
            setattr(obj,k,v)


class TestOriginalLayer(unittest.TestCase):
    def setUp(self):
        self.xy=np.array([[0,.15],[0,.55],[0,.90]])
        self.mass=np.array([1.,2.,1.])
        self.ids=np.arange(3)
        self.solver=SimpleNamespace(LO=0.,WIDTH=1.,WALL_SPEED=.5)
        self.wall=table([dict(step=i,floor_impulse=.5,lid_signed_impulse=-.25) for i in (1,2)])
        self.trace=table([dict(step=i,pressure=i*.5) for i in (0,1,2)])
        g=FROZEN.LayerObservation(None,0.,1.,None,None)
        g.group(self.xy,self.mass)
        self.spec=g.spec

    def base(self):
        class Advance:
            step=0
            def __call__(self,x,v,*unused):
                self.step+=1
                self.last_step=dict(step=self.step,floor_impulse=.5,lid_signed_impulse=-.25)
                return x[::-1].copy(),v+np.array([[0.,.5],[0.,-.125],[0.,0.]]),None,None,None
        return Advance()

    def test_direct_particles_and_fixed_initial_layers(self):
        rows=[]
        fn=app.Observe(FROZEN,self.base(),self.solver,parse(self.wall),self.spec,rows.append)
        x,v=self.xy,np.zeros_like(self.xy)
        for _ in range(2):
            x,v,*_=fn(x,v,None,None,self.ids,self.mass,0,.1,.8)
        self.assertEqual([rows[1][group+"_after"] for group in FROZEN.LAYERS],[1.,-.5,0.])
        self.assertEqual(rows[1]["whole_delta"],.25)
        self.assertEqual(rows[1]["whole_delta"],rows[1]["wall_signed_J"])

    def test_changed_wall_and_changed_composition_fail(self):
        for historical,spec in ((self.wall.replace(b"0.5",b"0.6"),self.spec),(self.wall,dict(self.spec,masses=[9.,2.,1.]))):
            fn=app.Observe(FROZEN,self.base(),self.solver,parse(historical),spec,lambda row: self.fail("wrote changed path"))
            with self.assertRaises(ValueError):
                fn(self.xy,np.zeros_like(self.xy),None,None,self.ids,self.mass,0,.1,.8)

    def test_native_wrapper_and_archived_prefix(self):
        nat=SimpleNamespace(STEPS={},BUDGET={},rows=parse)
        model=SimpleNamespace(make_advance=lambda *args:self.base())
        def native_run(fine,ctx,model,traces,identity,n,dest):
            self.assertEqual(ctx.solver.WALL_SPEED,.5)
            self.assertEqual(nat.STEPS,{12:2})
            self.assertEqual(nat.BUDGET[12],600)
            fn=model.make_advance()
            dest.mkdir()
            x,v=self.xy,np.zeros_like(self.xy)
            for i in (1,2):
                x,v,*_=fn(x,v,None,None,self.ids,self.mass,0,.1,.8)
            (dest/"trace.csv").write_bytes(traces[n])
            (dest/"wall_steps.csv").write_bytes(self.wall)
        nat.run_arm=native_run
        e=SimpleNamespace(depth=FROZEN,half=SimpleNamespace(override=override),native=nat,
                          ctx=SimpleNamespace(solver=self.solver),model=model,fine=None,refs={12:(self.trace,self.wall)},
                          specs={12:self.spec},identity=dict(wall_speed=.5,label="DEVELOPMENT_ONLY"))
        with tempfile.TemporaryDirectory() as tmp, patch.object(app,"STEPS",{12:2}):
            dest=Path(tmp)/"F12"
            app.arm(e,12,dest)
            data,receipt=app.verify(e,dest,12)
            self.assertEqual(receipt,json.loads((dest/"layer_receipt.json").read_bytes()))
            self.assertEqual(data[-1]["whole_after"],.5)
            self.assertEqual(receipt["max_abs_direct_wall_residual_J"],0.)
            raw=(dest/"layer_steps.csv").read_bytes()
            (dest/"layer_steps.csv").write_bytes(raw.replace(b"-0.25",b"-0.125",1))
            with self.assertRaises(ValueError):
                app.verify(e,dest,12)
            (dest/"layer_steps.csv").write_bytes(raw)
            for target in ("trace.csv","wall_steps.csv"):
                stream=dest/target
                orig=stream.read_bytes()
                stream.write_bytes(orig+b"\n")
                with self.assertRaisesRegex(ValueError,"prefix bytes"):
                    app.verify(e,dest,12)
                stream.write_bytes(orig)

    def test_comparisons_use_equal_time_and_distinct_displacements(self):
        def synthetic(n):
            data=[]
            for i in range(1,2*n+1):
                row=dict(step=i, floor_J=1./n, lid_signed_J=-.25/n)
                for k,v in (("lower",.5),("middle",.25),("upper",0.),("whole",.75)):
                    row[k+"_before"]=v*(i-1)/n
                    row[k+"_after"]=v*i/n
                data.append(row)
            return data
        pair={12:synthetic(1),24:synthetic(2)}
        e=SimpleNamespace(half=SimpleNamespace(override=override),depth=FROZEN,
                          fine=SimpleNamespace(DT={12:.5,24:.25}),ctx=SimpleNamespace(solver=self.solver),
                          identity=dict(wall_speed=.5),half_layers=pair)
        with patch.object(app,"EVENTS",((2,4),)):
            rec=app.compare(e,pair)[0]
        self.assertEqual(rec["time_code"],1.)
        self.assertEqual(rec["original_travel_D"],2*rec["half_travel_D"])
        self.assertEqual(rec["original"]["F12_minus_F24_equal_duration"]["whole_delta_MPa"],0.)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("previous_depth_block",type=Path)
    block=p.parse_args().previous_depth_block.read_bytes()
    assert hashlib.sha256(block).hexdigest()=="12e2aa889c5a35a69c13b3acd6b26a5ad8d6c9e872557348d49b04b8e1ce2cc8"
    payload=block.split(b"<<'DEPTH_PREFIX_SOURCES'\n",1)[1].split(b"\nDEPTH_PREFIX_SOURCES\n",1)[0]
    with tarfile.open(fileobj=io.BytesIO(base64.b64decode(payload)),mode="r:gz") as source:
        module=source.extractfile(app.FROZEN).read()
    FROZEN=ModuleType("frozen_test_depth")
    exec(compile(module,app.FROZEN,"exec"),FROZEN.__dict__)
    unittest.main(argv=[sys.argv[0]])
