"""Synthetic wall/transfer tests and fail-closed return readback tests."""
import csv
from importlib.util import module_from_spec, spec_from_file_location
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np


spec=spec_from_file_location("early",Path(__file__).with_name("early_wall_observer.py"))
m=module_from_spec(spec)
spec.loader.exec_module(m)


class Surface:
    def __init__(self):
        self.boundary=SimpleNamespace(positions=np.array([[.3,.1],[.3,.9]]))

    def project(self,mass,vel):
        old=vel[0,1]
        vel[0,1]=max(old,0.)
        return float(mass[0]*(vel[0,1]-old))


def upper(solver,xy,v,lid):
    v[1,1]=min(v[1,1],0.)


def contact(ids,nodes,mass,grad,v,centers,friction):
    v[:,1]+=np.array([-.25,.25])/mass


def synth(observe=True):
    floor=SimpleNamespace(SurfaceStep=Surface,_other_walls=upper)
    solver=SimpleNamespace(LO=0.)
    surface=Surface()
    v=np.array([[.40,-1.],[-.20,.25]])
    input_y=v[:,1].copy()
    mass=np.array([1.,2.])
    ids=np.array([0,1])
    r=m.Recorder()
    r.begin()
    def run(v,project):
        j=surface.project(mass,v)
        floor._other_walls(solver,None,v,.95)
        project(ids,None,mass,None,v,None,.5)
        j+=surface.project(mass,v)
        floor._other_walls(solver,None,v,.95)
        return j
    if not observe:
        return run(v,contact),v
    with m.monitor(floor,r):
        j=run(v,lambda *a:r.contact(contact,*a))
    return r.finish(1,.125,ids,mass,input_y,v[:,1]),j,v


class BalanceTests(unittest.TestCase):
    def test_material_floor_candidate_on_six_manufactured_points(self):
        # Runs the actual pinned advance on a synthetic two-field patch, for just one increment.
        root=Path(os.environ.get("SUYOUNG_SOURCE_ROOT",Path(__file__).resolve().parents[3]))
        def source(name,path):
            spec=spec_from_file_location(name,root/path)
            module=module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        native=source("synthetic_solver","scripts/suyoung_u6_first_dev.py")
        floor=source("candidate_surface","docs/reviews/suyoung_floor_contact_20261123/material_floor.py")
        s=SimpleNamespace(model=native.model,LO=.15,WIDTH=.5,WALL_SPEED=.02)
        x=np.array([[.35,.15],[.355,.15],[.36,.15],[.35,.645],[.355,.645],[.36,.645]])
        ids=np.array([0,0,0,1,1,1])
        vol=np.full(len(ids),1.e-4)
        vel=np.array([[0.,-.01]]*3+[[0.,.03]]*3)
        affine=np.zeros((len(x),2,2))
        elastic=np.broadcast_to(np.eye(2),affine.shape).copy()
        def conserving_exchange(ids,nodes,mass,grad,v,centers,friction):
            # Equal/opposite field impulses, including a downwards kick to the lower layer.
            for k,dv in ((0,-.02),(1,.02)):
                pick=(ids==k)&(mass>0.)
                v[pick,1]+=dv*vol[:3].sum()/mass[pick].sum()
        def advance():
            b=floor.MaterialBoundary(np.arange(6),x.copy())
            return floor.make_advance(s,12,boundary=b)(x,vel,affine,elastic,ids,vol,80,.001,.65)
        s.project_contacts=conserving_exchange
        plain=advance()
        r=m.Recorder()
        r.begin()
        s.project_contacts=lambda *args:r.contact(conserving_exchange,*args)
        with m.monitor(floor,r):
            traced=advance()
        for a,b in zip(plain,traced):
            self.assertEqual(np.asarray(a).tobytes(),np.asarray(b).tobytes())
        row=r.finish(1,0.,ids,vol,vel[:,1],traced[1][:,1])
        m.facts(row,10.*traced[-1],.001,s.WIDTH)
        self.assertGreater(row["floor_all"],0.)
        self.assertLess(row["lid_all"],0.)
        self.assertLess(row["contact_bottom_row"],0.)

    def test_observer_preserves_every_velocity_bit_and_impulse(self):
        j0,v0=synth(False)
        row,j,v=synth()
        self.assertEqual(v.tobytes(),v0.tobytes())
        self.assertEqual(j,j0)
        self.assertEqual(row["native_floor_impulse"],1.25)
        self.assertEqual(row["lid_all"],-.75)

    def test_per_field_internal_transfer_and_momentum_close(self):
        row,_,_=synth()
        self.assertEqual(row["contact_all"],0.)
        self.assertEqual(row["contact_bottom_row"],-.25)
        self.assertEqual(row["grid_change_bottom_row"],1.)
        self.assertEqual(row["grid_change_all"],.5)
        self.assertAlmostEqual(row["top_gap_before"],.05)
        m.facts(row,12.5,1.,1.)

    def test_wall_or_interbody_sign_and_both_conservation_checks(self):
        base,_,_=synth()
        for key,value in (("lid_all",.75),("floor_all",-1.),("contact_all",.25),
                          ("particle_change_bottom_row",0.),("grid_change_all",.125),
                          ("contact_bottom_row",-.5),("top_gap_before",float("nan"))):
            with self.subTest(key=key), self.assertRaises(ValueError):
                m.facts({**base,key:value},12.5,1.,1.)
        with self.assertRaisesRegex(ValueError,"pressure"):
            m.facts(base,11.,1.,1.)

    def test_hook_restored_after_exception_and_early_contact_refused(self):
        floor=SimpleNamespace(SurfaceStep=Surface,_other_walls=upper)
        original=Surface.project
        r=m.Recorder()
        r.begin()
        with self.assertRaisesRegex(ValueError,"interbody"):
            with m.monitor(floor,r):
                r.contact(contact,None,None,None,None,None,None,.5)
        self.assertIs(Surface.project,original)
        self.assertIs(floor._other_walls,upper)

    def test_refuses_other_return_before_extracting(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/"wrong.tar.gz"
            path.write_bytes(b"not the delivered data")
            with self.assertRaisesRegex(ValueError,"wrong F12/F24 return"):
                m.prior_traces(path,None,None)

    def test_synthetic_reread_binds_trace_observer_receipt_and_samples(self):
        with TemporaryDirectory() as tmp, patch.dict(m.STEPS,{12:2,24:2}), patch.dict(m.SAMPLES,{12:(1,2),24:(1,2)}):
            run=Path(tmp)
            fine=SimpleNamespace(DT={12:1.,24:1.})
            ctx=SimpleNamespace(solver=SimpleNamespace(WIDTH=1.))
            prior={}
            for n in m.STEPS:
                dest=run/f"F{n}"
                dest.mkdir()
                prior[n]=b"step,height,bottom_pressure_E\r\n0,1,0\r\n1,.875,1.25\r\n2,.75,1.25\r\n"
                (dest/"trace.csv").write_bytes(prior[n])
                row,_,_=synth()
                with (dest/"wall_impulses.csv").open("w",newline="") as o:
                    w=csv.DictWriter(o,m.COLUMNS,lineterminator="\n")
                    w.writeheader()
                    w.writerows((row,{**row,"step":2,"displacement_code":.25}))
                receipt=m.check_arm(fine,ctx,{},prior,n,dest)
                self.assertEqual(receipt["steps_with_lid_impulse_and_positive_material_gap"],2)
                (dest/"balance_receipt.json").write_text(json.dumps(receipt))
            summary=m.summarize(fine,ctx,{},prior,run)
            self.assertEqual(summary["samples"][0]["F12"]["floor_MPa"],12.5)
            self.assertFalse(summary["u6_qualified"])
            receipt_path=run/"F12"/"balance_receipt.json"
            r=json.loads(receipt_path.read_bytes())
            r["steps"]=1
            receipt_path.write_text(json.dumps(r))
            with self.assertRaisesRegex(ValueError,"observer receipt"):
                m.summarize(fine,ctx,{},prior,run)
            (run/"F12"/"trace.csv").write_bytes(prior[12].replace(b"\r\n",b"\n"))
            with self.assertRaisesRegex(ValueError,"raw prefix"):
                m.check_arm(fine,ctx,{},prior,12,run/"F12")


if __name__=="__main__":
    unittest.main()
