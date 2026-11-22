"""Synthetic stress response and frozen fixture binding. No model timesteps."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.solver = mods["driver"].fixed_solver()
        self.x = np.array([[.161,.146], [.163,.147], [.164,.157]])
        self.ids = np.array([1, 0, 1])
        self.volume = np.array([.21, .05, .11])
        self.tau = np.array([[[3.,7.],[-.9,-2.]], [[5.,4.],[2.8,.7]], [[4.,5.],[0.3,1.7]]])
        self.elastic = np.repeat(np.eye(2)[None], 3, axis=0)
        self.grid = 80

    def run_project(self, tensor):
        with patch.object(self.solver.model,"stress",return_value=tensor):
            return p.project(self.solver,self.x,self.elastic,self.ids,self.volume,self.grid,prefix.WIDTH)

    def test_literal_nonuniform_sum_by_field_key(self):
        actual=self.run_project(self.tau)
        nodes,w,_,r=self.solver.model.stencil(self.x,self.grid)
        ref={}
        for i,vol in enumerate(self.volume):
            for j,node in enumerate(nodes[i]):
                key=int(self.ids[i]*(self.grid+1)**2+node)
                values=ref.setdefault(key, [0.]*4)
                a=40.*self.grid**2 / prefix.WIDTH * vol * w[i,j]
                values[0] += a*r[i,j,1]*self.tau[i,1,1]
                values[1] += a*r[i,j,0]*self.tau[i,1,0]
                values[2] += a*r[i,j,1]
                values[3] += a*r[i,j,0]
        self.assertEqual(actual["key"].tolist(), sorted(ref))
        for c,k in enumerate(p.COLS):
            np.testing.assert_allclose(actual[k],[ref[key][c] for key in sorted(ref)],rtol=1.e-14,atol=1.e-13)
        self.assertGreater(np.max(abs(actual["yx"])), 0.)

    def test_signed_pure_compression_and_shear(self):
        tau=np.zeros_like(self.tau); tau[:,1,1]=-1.
        normal=self.run_project(tau)
        np.testing.assert_allclose(normal["yy"],-normal["unit_yy"],atol=1e-13)
        np.testing.assert_array_equal(normal["yx"], 0.)
        tau[:,1,1]=0.; tau[:,1,0]=1.; tau[:,0,1]=1.
        shear=self.run_project(tau)
        np.testing.assert_allclose(shear["yx"],shear["unit_yx"],atol=1e-13)
        np.testing.assert_array_equal(shear["yy"], 0.)

    def test_actual_pressure_and_mask_are_native(self):
        dt=prefix.DT[8]; width=prefix.WIDTH
        with patch.object(self.solver.model,"stress",return_value=self.tau):
            s=m.scatter(self.solver,self.x,np.tile([.1,-.02],(3,1)),np.zeros_like(self.tau),
                        self.elastic,self.ids,self.volume,self.grid,dt,.65)
        mass=s["mass"]
        vy=np.divide(s["native_y"],mass,out=np.zeros_like(mass),where=mass>0)
        xy=np.column_stack(np.divmod(s["key"]%(self.grid+1)**2,self.grid+1))/self.grid
        mask=m.capture_first(s,mass,xy,np.column_stack((np.zeros_like(vy),vy)),self.solver.LO)
        record=p.subset(self.run_project(self.tau),mask)
        self.assertGreater(len(record["keys"]),0)
        self.assertEqual(record["keys"],mask["keys"])
        p.reduce_record(record,mask,dt,width)
        for key in ("keys","yy","yx","unit_yy"):
            bad={k:(v[:] if type(v) is list else v) for k,v in record.items()}
            if key=="keys": bad[key].reverse()
            elif key.startswith("unit"): bad[key][0]=float("nan")
            else: bad[key][0] += 1.
            with self.subTest(key=key), self.assertRaises(ValueError):
                p.reduce_record(bad,mask,dt,width)

    def test_subset_preserves_signed_weights_and_refuses_missing_keys(self):
        full=dict(key=np.array([0,2]), **{k:np.array([-.1,.6]) for k in p.COLS})
        part=p.subset(full,{"keys":[0]})
        self.assertEqual(part["unit_yy"],[-.1])
        for keys in ([1],[4]):
            with self.assertRaises(ValueError): p.subset(full,{"keys":keys})
        empty=p.subset(full,{"keys":[]})
        self.assertEqual(p.reduce_record(empty,{"keys":[],"stress":[]},.1,1.)["yy"],0.)

    def test_unit_tensor_invariant_under_native_stress_change(self):
        a=self.run_project(self.tau); b=self.run_project(self.tau*2)
        for k in ("unit_yy","unit_yx"): np.testing.assert_array_equal(a[k],b[k])
        for k in ("yy","yx"): np.testing.assert_array_equal(a[k]*2,b[k])

    def test_nested_observers_keep_native_first_and_second_wall(self):
        n=8; dt=prefix.DT[n]; width=prefix.WIDTH
        mass=np.array([1.]); xy=np.zeros((1,2))
        state=dict(key=np.array([0]),mass=mass,grid=80,native_y=np.array([-1.]),
                   translation=np.array([-.9]),apic=np.array([.1]),stress=np.array([-.2]))
        projection=dict(key=state["key"],yy=np.array([.3*10/(dt*width)]),
                        yx=np.array([-.1*10/(dt*width)]),unit_yy=np.array([-.9]),unit_yx=np.array([.03]))
        def native_wall(m,coords,vel,lid,speed):
            impulse=-float(vel[0,1]); vel[0,1]=0.
            return impulse
        solver=SimpleNamespace(WIDTH=width,WALL_SPEED=.02,LO=.15,walls=native_wall)
        rows=[None]*268
        for step in (269,270):
            height=width-dt*step*solver.WALL_SPEED
            rows.append(dict(step=step,u=width-height,p_MPa=10*(1.25/(dt*width)),
                    pre=dict(M=1.,count=1,mean_down=1.,J=1.),post=dict(M=1.,count=1,mean_down=.25,J=.25)))
        def fixed_loop(pair,mods,hist,n,folder):
            folder.mkdir()
            o=prefix.Observer(solver,SimpleNamespace(project_contacts=lambda *args:None),n)
            o.rows=rows[:268]
            def step(*args):
                vel=np.array([[0.,-1.]]); lid=args[-1]
                j=o.wall(mass,xy,vel,lid,-.02); o.project(.5)
                vel[0,1]=-.25; j+=o.wall(mass,xy,vel,lid,-.02)
                return (j/(dt*width),)
            solver.advance=step
            for k in (269,270):
                o.advance(None,None,None,None,None,None,80,dt,solver.LO+(width-dt*k*solver.WALL_SPEED))
            for filename in ("trace.csv","wall_observations.json","prefix_receipt.json"):
                (folder/filename).write_bytes(b"mock-frozen")
        with (tempfile.TemporaryDirectory() as temp, patch.object(m,"scatter",return_value=state),
              patch.object(p,"project",return_value=projection), patch.object(prefix,"arm",fixed_loop),
              patch.object(prefix,"checked_records",return_value=rows)):
            base=Path(temp)/"old"
            m.arm(prefix,None,None,None,{n:rows},n,base)
            old={f:(base/f).read_bytes() for f in p.FILES}
            folder=Path(temp)/"new"
            p.arm(m,prefix,None,None,None,{n:rows},old,n,folder)
            result=p.read_arm(n,folder,old,prefix)
            self.assertEqual(result[270]["unit_yy"],-.9)
            (folder/"probe.json").write_bytes(b"[]")
            with self.assertRaisesRegex(ValueError,"PROBE_RECEIPT"): p.read_arm(n,folder,old,prefix)
            mixed=dict(old)
            mixed["trace.csv"]=b"changed"
            with self.assertRaisesRegex(ValueError,"PREVIOUS_FILE"): p.arm(m,prefix,None,None,None,{n:rows},mixed,n,Path(temp)/"bad")
            self.assertFalse((Path(temp)/"bad"/"probe_receipt.json").exists())

    def test_bound_return(self):
        hist,walls=m.history(ARGS.prior,prefix,pair)
        old=p.history(ARGS.momentum, m,prefix,pair,hist,walls,self.solver.LO)
        self.assertEqual(set(old),{8,16})
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            for key,val in old[8].items(): (folder/key).write_bytes(val)
            p.match_old(folder,old[8])
            (folder/"trace.csv").write_bytes(old[8]["trace.csv"]+b"\n")
            with self.assertRaises(ValueError): p.match_old(folder,old[8])


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--prior",type=Path,required=True)
    ap.add_argument("--momentum",type=Path,required=True)
    ap.add_argument("--subject",type=Path,default=Path(__file__).with_name("probe.py"))
    ARGS,rest=ap.parse_known_args()
    spec=importlib.util.spec_from_file_location("test_stress_probe",ARGS.subject)
    p=importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
    m,prefix,pair,mods=p.sources(ARGS.repo)
    unittest.main(argv=[sys.argv[0]]+rest)
