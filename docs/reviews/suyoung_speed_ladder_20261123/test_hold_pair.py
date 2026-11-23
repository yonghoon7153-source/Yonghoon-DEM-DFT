"""Manufactured clock/marker/energy tests. No development arm or historical seed is run."""
from pathlib import Path
from contextlib import contextmanager
import csv
import io
import json
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import os

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
import hold_pair as hold


class StopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        default=Path(__file__).resolve().parent.parent/"suyoung_wall_balance_return_20261123"/"material_lid.py"
        cls.model=SimpleNamespace(__file__=os.environ.get("HOLD_TEST_LID_SOURCE",str(default)))
        cls.stop=staticmethod(hold.stationary_call(cls.model))

    def test_stationary_source_one_guard_and_pinned_bytes(self):
        source=Path(self.model.__file__).read_bytes()
        changed=hold.stationary_source(source)
        a,b=source.splitlines(),changed.splitlines()
        self.assertEqual(len(a),len(b))
        self.assertEqual(sum(x!=y for x,y in zip(a,b)),1)
        self.assertIn(b"speed != 0. or lid != self.previous_lid",changed)
        with self.assertRaisesRegex(ValueError,"source"):
            hold.stationary_source(source+b"\n")

    def test_stationary_method_enforces_fixed_exact_clock_and_preserves_state(self):
        def build():
            class Native:
                audit={"steps":0}
                def __call__(self,*args):
                    state.impulses.extend([.25,0.])
                    state.errors.extend([0.,0.])
                    state.floor_impulses.extend([.125,0.])
                    self.audit["steps"]+=1
                    return args[:4]+(.125,)
            state=SimpleNamespace(failed=False,solver=SimpleNamespace(WALL_SPEED=0.,LO=.15),previous_lid=.8,
                                  boundary=object(),positions=np.array([[.4,.2],[.6,.75]]),native=Native(),audit={},
                                  lid_audit=dict(steps=1,lid_passes=2,positive_passes=1,accumulated_downward_impulse=.5,
                                                 max_grid_impulse_error=0.,max_penetration=0.,max_clock_error=0.))
            return state
        state=build()
        arrays=tuple(object() for _ in range(6))
        marker_id=id(state.boundary)
        args=arrays+(24,.01,.8)
        result=self.stop(state,*args)
        self.assertEqual(result[:4],arrays[:4])
        self.assertEqual(state.last_step["lid_signed_impulse"],-.25)
        self.assertEqual(state.last_step["step"],2)
        self.assertEqual(state.lid_audit["accumulated_downward_impulse"],.75)
        self.assertEqual(id(state.boundary),marker_id)
        for speed,lid in ((.01,.8),(0.,.8000000000000002),(-.01,.8)):
            state=build()
            state.solver.WALL_SPEED=speed
            with self.assertRaises(ValueError):
                self.stop(state,*args[:-1],lid)
            self.assertTrue(state.failed)
        state=build()
        state.positions[0,1]=.1
        with self.assertRaises(ArithmeticError):
            self.stop(state,*args)

    def test_switch_preserves_the_original_instance_and_has_no_implicit_retry(self):
        class Native:
            failed=False
            previous_lid=.9
            solver=SimpleNamespace(WALL_SPEED=.1)
            def __call__(self,*args):
                self.previous_lid=args[-1]
                return (self,args)
        b=Native()
        trial=hold.PhaseLid(b,lambda obj,*args:(obj,args))
        a=object()
        self.assertEqual(trial(a,.8),(b,(a,.8)))
        with self.assertRaises(ValueError):
            trial.hold(.85)
        trial.hold(.8)
        with self.assertRaises(ValueError):
            trial(a,.8)
        b.solver.WALL_SPEED=0.
        self.assertEqual(trial(a,.8),(b,(a,.8)))
        with self.assertRaises(ValueError):
            trial(a,.81)
        with self.assertRaises(ValueError):
            trial.hold(.8)

    def test_prefix_includes_trace_zero_and_rejects_changed_wall_even_when_pressures_agree(self):
        samples={k:b"header\n1\n2\n3\n" for k in hold.OBS}
        with tempfile.TemporaryDirectory() as d,patch.object(hold,"RAMP",{12:2}):
            path=Path(d)
            for name,raw in samples.items():
                (path/name).write_bytes(raw+b"4\n")
            got=hold.observed_prefix(path,samples,12)
            self.assertEqual(got["trace.csv"],hold.digest(samples["trace.csv"]))
            self.assertEqual(got["layer_steps.csv"],hold.digest(b"header\n1\n2\n"))
            (path/"wall_steps.csv").write_bytes(b"header\n1\n8\n3\n")
            with self.assertRaisesRegex(ValueError,"wall_steps"):
                hold.observed_prefix(path,samples,12)

    def test_fixed_window_pressure_momentum_and_translational_energy(self):
        velocity=np.array([[3.,4.],[0.,-2.]])
        self.assertEqual(hold.energy(velocity,np.array([2.,1.])),(27.,18.,5.))
        ws=[dict(floor_impulse=.2,lid_downward_impulse=.1,floor_gap_after=0.,top_gap_after=.03)]*2
        ls=[dict(lower_delta=.09,middle_delta=.03,upper_delta=-.02,whole_delta=.1)]*2
        es=[dict(particle_ke=1.,vertical_ke=.1,max_particle_speed=.8)]*2
        result=hold.window(ws,ls,es,.1,2.)
        self.assertEqual(result["floor_mean_MPa"],10.)
        self.assertEqual(result["floor_minus_lid_mean_MPa"],5.)
        self.assertEqual(result["particle_ke"]["mean"],1.)
        with self.assertRaises(ValueError):
            hold.window(ws,ls,es[:1],.1,2.)

    def test_manufactured_driver_keeps_fork_state_and_matches_four_prefixes(self):
        # Two compression steps and two hold steps on three deliberately manufactured points.
        mass=np.array([.25,.25,.5])
        x=np.array([[.5,.15],[.5,.55],[.5,.9]])
        ids=np.arange(3)
        s=SimpleNamespace(WIDTH=1.,LO=0.,TARGET=2.,WALL_SPEED=1.,project_contacts=None)
        dt=.0625
        speed=.125
        @contextmanager
        def override(obj,**changes):
            saved={k:getattr(obj,k) for k in changes}
            try:
                for k,v in changes.items():
                    setattr(obj,k,v)
                yield
            finally:
                for k,v in saved.items():
                    setattr(obj,k,v)
        wall_columns=("step","floor_impulse","lid_signed_impulse")
        class Wall:
            previous_lid,failed,solver=1.,False,s
            positions=x.copy()
            audit,lid_audit={},{}
            step=0
            def __call__(self,x,v,C,F,ids,mass,grid,dt,lid):
                self.step+=1
                self.solver.project_contacts(.5)
                self.previous_lid=lid
                self.last_step=dict(step=self.step,floor_impulse=0.,lid_signed_impulse=0.)
                return x,v,C,F,0.
        phases=[]
        def stationary(base,*args):
            phases.append((base.step,args[-1]))
            return base(*args)
        class Observe:
            def __init__(self,d,h,base,s,record):
                self.base,self.record=base,record
                self.groups=SimpleNamespace(spec={"counts":[1,1,1]})
            def __call__(self,*args):
                r=self.base(*args)
                for f in ("particle_momentum.csv","layer_steps.csv"):
                    self.record(f,{"step":self.base.last_step["step"],"sum":0.})
                return r
        native=SimpleNamespace(WALL_COLUMNS=wall_columns,STEPS=None,
            receipt=lambda *args:dict(floor=args[-2],lid=args[-1]))
        e=SimpleNamespace(ctx=SimpleNamespace(solver=s,kernel=SimpleNamespace(project_contacts=lambda *args:None),floor=None),
            native=native,half=SimpleNamespace(override=override,MOMENTUM=("step","sum")),depth=SimpleNamespace(COLUMNS=("step","sum")),
            q=SimpleNamespace(LayerAdvance=Observe,write_json=lambda p,o:p.write_text(json.dumps(o))),
            fine=SimpleNamespace(DT={12:dt},initial=lambda *args:(x,ids,mass)),speed=speed,
            model=SimpleNamespace(make_advance=lambda *a,**kw:Wall()),stationary=stationary,identity={})
        def table(cols,rows,term):
            stream=io.StringIO(newline="")
            writer=csv.writer(stream,lineterminator=term)
            writer.writerows([cols,*rows])
            return stream.getvalue().encode()
        ref={f:table(("step","sum"),[(1,0.),(2,0.)],"\n") for f in ("particle_momentum.csv","layer_steps.csv")}
        ref["wall_steps.csv"]=table(wall_columns,[(1,0.,0.),(2,0.,0.)],"\n")
        ref["trace.csv"]=table(hold.TRACE,[(0,0,1.,0,1.)]+[(i,dt*i,1.-dt*i*speed,0.,1./(1.-dt*i*speed))
                                for i in (1,2)],"\r\n")
        e.old={12:ref}
        with tempfile.TemporaryDirectory() as temp,patch.object(hold,"RAMP",{12:2}),patch.object(hold,"HOLD",{12:2}):
            dest=Path(temp)/"F12"
            hold.run_arm(e,12,dest)
            rec=json.loads((dest/"hold_receipt.json").read_bytes())
            self.assertEqual(rec["fork"]["step"],2)
            self.assertEqual(rec["fork"]["prefix_sha256"],{k:hold.digest(raw) for k,raw in ref.items()})
            tr=list(csv.DictReader((dest/"trace.csv").read_text().splitlines()))
            self.assertEqual([r["height"] for r in tr[-3:]],[tr[2]["height"]]*3)
            self.assertEqual(phases,[(2,float(tr[2]["height"])),(3,float(tr[2]["height"]))])
            self.assertEqual(s.WALL_SPEED,1.)


if __name__=="__main__":
    unittest.main()
