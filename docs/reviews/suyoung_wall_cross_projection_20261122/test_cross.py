"""Synthetic four-entry fixed-mask diagnostic; no dynamical steps."""
import argparse
import json
import importlib.util
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
import numpy as np


class CrossTests(unittest.TestCase):
    def setUp(self):
        self.solver = mods["driver"].fixed_solver()
        self.x = np.array([[.5625,.25]])
        self.ids = np.array([17],dtype=np.int64)
        self.v = np.array([3/7])
        self.state = dict(x=self.x, ids=self.ids, volume=self.v,
                          yy=np.array([-.375]), yx=np.array([.125]))
        self.keys = [17*25+3*5]

    def test_exact_asymmetric_stencil_and_empty_support(self):
        keys=[0]+self.keys+[48*25+24]
        ans=c.project_state(self.solver.model,self.state,4,2.5,keys)
        self.assertEqual((ans["requested_keys"],ans["positive_support_keys"],ans["unsupported_keys"]),(3,1,2))
        factor=40*16/2.5*(3/7)*(9/256)
        expected=dict(yy=factor*(-.25)*(-.375),yx=factor*(3/16)*.125,
                      unit_yy=factor*(-.25),unit_yx=factor*(3/16))
        for k,v in expected.items(): np.testing.assert_allclose(ans[k],[0,v,0],atol=1e-15)
        self.assertEqual(c.totals(ans)["compression_minus_one_MPa"],-sum(ans["unit_yy"]))
        with self.assertRaises(ValueError): c.project_state(self.solver.model,self.state,4,2.5,[*self.keys,*self.keys])

    def test_missing_target_not_extrapolated(self):
        ans=c.project_state(self.solver.model,self.state,4,2.5,[2,3])
        self.assertEqual(ans["unsupported_keys"],2)
        for k in c.COLS: self.assertEqual(ans[k],[0.,0.])
        bad=dict(self.state,x=np.array([[-1.,.25]]))
        with self.assertRaises(ValueError): c.project_state(self.solver.model,bad,4,2.5,self.keys)
        # Valid native fine-grid support can lie outside the supported target stencil.
        self.assertIsNone(c.target_projection(self.solver.model,bad,4,2.5,self.keys,False)["values"])
        with self.assertRaises(ValueError): c.target_projection(self.solver.model,bad,4,2.5,self.keys,True)

    def test_stress_and_geometry_move_independently(self):
        b=dict(self.state,yy=np.array([-.75]),yx=np.array([.25]))
        left=c.project_state(self.solver.model,self.state,4,2.5,self.keys)
        right=c.project_state(self.solver.model,b,4,2.5,self.keys)
        for k in ("yy","yx"): np.testing.assert_allclose(np.array(left[k])*2,right[k])
        for k in ("unit_yy","unit_yx"): self.assertEqual(left[k],right[k])
        empty=c.project_state(self.solver.model,self.state,8,2.5,[17*81+8])
        self.assertEqual(empty["unsupported_keys"],1)

    def test_signed_both_paths_and_change_of_gaps(self):
        q=c.contrasts({(8,8):8.,(8,16):5.,(16,8):7.,(16,16):2.})
        self.assertEqual(q["native_F8_minus_F16"],6.)
        self.assertEqual(q["state_F8_minus_F16_on_F8_target"],1.)
        self.assertEqual(q["state_F8_minus_F16_on_F16_target"],3.)
        self.assertEqual(q["target_F8_minus_F16_at_F8_state"],3.)
        self.assertEqual(q["target_F8_minus_F16_at_F16_state"],5.)
        self.assertEqual(q["interaction"],-2.)

    def test_per_key_native_not_just_aggregate(self):
        row=dict(keys=[1,2],**{k:[-0.1,.4] for k in c.COLS})
        c.match_native(row,row)
        bad=dict(row,yy=[-.2,.5])
        with self.assertRaises(ValueError): c.match_native(bad,row)

    def test_native_snapshots_isolated_no_pickle(self):
        state=c.snapshot(self.solver,self.x,np.tile(np.eye(2),(1,1,1)),self.ids,self.v)
        self.x[0,0]=.1
        self.assertEqual(state["x"][0,0],.5625)
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/"state.npz"
            c.save_state(file,state)
            with self.assertRaises(FileExistsError): c.save_state(file,state)
            with np.load(file,allow_pickle=False) as inputs:
                self.assertEqual(set(inputs.files),set(state))
                for k in state: np.testing.assert_array_equal(inputs[k],state[k])

    def test_fixed_histories_without_computation(self):
        hist,walls,old=c.histories(args.prior,args.probe,p,m,prefix,pair,mods["driver"].fixed_solver().LO)
        self.assertEqual((len(walls[8]),len(walls[16])),(270,540))
        self.assertEqual(c.endpoints(walls,prefix,269,538)["common_end_u"],walls[8][268]["u"])
        times=c.endpoints(walls,prefix,269,538)
        self.assertNotEqual(times["incoming_u"][8],times["incoming_u"][16])
        with self.assertRaises(ValueError): c.endpoints(walls,prefix,269,540)
        self.assertEqual(sorted(old[16]["projection"]),[538,540])

    def test_crossed_matrix_keeps_fixed_target_keys_and_native_receipts(self):
        model=self.solver.model
        states={8:{},16:{}}
        olds={8:{"projection":{}},16:{"projection":{}}}
        band={n:[dict(u=(i+1)*(2 if n==8 else 1)) for i in range(count)]
              for n,count in ((8,270),(16,540))}
        for n,steps in c.STEPS.items():
            grid=10*n
            x=.45 if n==8 else .75
            for step in steps:
                state=dict(self.state,x=np.array([[x,.125]]),yy=np.array([-.75 if n==8 else -.125]))
                states[n][step]=state
                keys=[17*(grid+1)**2+round(x*grid)*(grid+1)+round(.125*grid)-1]
                native=c.project_state(model,state,grid,2.5,keys)
                olds[n]["projection"][step]={col:native[col] for col in ("keys",*c.COLS)}
        pf=SimpleNamespace(DT={8:.002,16:.001},WIDTH=2.5)
        rep=c.summary(model,pf,band,olds,states)
        self.assertTrue(rep["native_diagonal_checked"])
        for sample in rep["paired"]:
            entries={(r["source_cells"],r["target_cells"]):r for r in sample["corners"]}
            for k,r in entries.items():
                if k[0]!=k[1]:
                    self.assertEqual((r["positive_support_keys"],r["unsupported_keys"]),(0,1))
                    self.assertEqual(r["values"]["stress_MPa"],0.)
            diagonal=entries[(8,8)]["values"]["stress_MPa"]-entries[(16,16)]["values"]["stress_MPa"]
            self.assertEqual(sample["contrasts"]["stress_MPa"]["native_F8_minus_F16"],diagonal)
        olds[8]["projection"][269]["yy"][0] += .25
        with self.assertRaises(ValueError): c.summary(model,pf,band,olds,states)

    def test_native_delegation_and_tampered_snapshot_receipt(self):
        solver=self.solver
        xx=np.array([[.45,.125]])
        E=np.repeat(np.diag([.9,.8])[None],1,axis=0)
        initial=c.snapshot(solver,xx,E,self.ids,self.v)
        geometry={key:c.sha(initial[col].tobytes()) for col,key in (("ids","physical_ids"),("volume","volume"))}
        fake_pair=SimpleNamespace(expected_geometry=lambda n:geometry)
        grid=80
        keys=[17*(grid+1)**2+36*(grid+1)+9]
        native=c.project_state(solver.model,initial,grid,2.5,keys)
        raw={k:native[k] for k in ("keys",*c.COLS)}
        old={"projection":{269:raw,270:raw},"files":{k:b"native mock"+k.encode() for k in c.PREFIX_FILES}}
        called=[]
        class Native:
            def advance(self,*a):
                called.append("advance")
                a[0][:]=.2  # native mutates x; incoming diagnostics must already have taken a copy.
                return 1579
        def run_fixed(pair,mods,hist,n,folder):
            folder.mkdir(exist_ok=False)
            for name,data in old["files"].items(): (folder/name).write_bytes(data)
            obs=pf.Observer(); obs.solver=solver
            for s in (269,270):
                obs.rows=[None]*(s-1)
                self.assertEqual(obs.advance(xx.copy(),None,None,E,self.ids,self.v,grid,.002,.7),1579)
        pf=SimpleNamespace(Observer=Native,arm=run_fixed,WIDTH=2.5,DT={8:.002},write=prefix.write)
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"records"
            c.arm(pf,fake_pair,{}, {},old,8,out)
            self.assertIs(pf.Observer,Native)
            self.assertEqual(called,["advance","advance"])
            restored=c.read_arm(8,out,old,geometry)
            for row in restored.values(): np.testing.assert_array_equal(row["x"],xx)
            rec=out/"cross_receipt.json";data=json.loads(rec.read_bytes());data["steps"]=[268,270]
            rec.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,"CROSS_RETURN_IDENTITY"):
                c.read_arm(8,out,old,geometry)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for key in ("repo","prior","probe"): parser.add_argument("--"+key,type=Path,required=True)
    args,remaining=parser.parse_known_args()
    spec=importlib.util.spec_from_file_location("cross_candidate",Path(__file__).with_name("cross.py"))
    c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    p,m,prefix,pair,mods=c.sources(args.repo)
    unittest.main(argv=[__file__]+remaining)
