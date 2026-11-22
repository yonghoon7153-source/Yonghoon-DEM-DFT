"""Fixed-mask arithmetic and frozen replay contracts, without field integration."""
import argparse
import importlib.util
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np


class MomentumTests(unittest.TestCase):
    def test_signed_contributions_do_not_reclip(self):
        state={"key":np.array([0,1,4]),"mass":np.array([1.,2.,1.]),"grid":2,
               "native_y":np.array([-1.,-2.,3.]),"translation":np.array([-2.,-4.,-1.]),
               "apic":np.array([1.,2.,3.]),"stress":np.array([0.,0.,1.])}
        xy=np.column_stack(np.divmod(state["key"],3))/2
        vel=np.column_stack((np.zeros(3),state["native_y"]/state["mass"]))
        rec=m.capture_first(state,state["mass"],xy,vel,.15)
        self.assertEqual(rec["keys"],[0])
        computed=m.reduce_mask(rec,.5,1.,.15)
        self.assertEqual(computed["J"],dict(translation=2.,apic=-1.,stress=0.))
        self.assertEqual(computed["native_J"],1.)
        self.assertEqual(computed["without_J"]["translation"],-1.)
        self.assertEqual(computed["p_MPa"]["apic"],-20.)

    def test_empty_mask_preserves_zero(self):
        state={"key":np.array([0]),"mass":np.array([0.]),"grid":2,"native_y":np.array([0.]),
               **{k:np.zeros(1) for k in m.TERMS}}
        rec=m.capture_first(state,state["mass"],np.zeros((1,2)),np.zeros((1,2)),.15)
        self.assertEqual(rec["keys"],[])
        self.assertEqual(m.reduce_mask(rec,1.,1.,.15)["native_J"],0.)

    def test_state_alignment_and_tampering(self):
        state={"key":np.array([0]),"mass":np.array([1.]),"grid":2,"native_y":np.array([-1.]),
               "translation":np.array([-2.]),"apic":np.array([1.]),"stress":np.zeros(1)}
        for mass,xy,v in ((np.array([1.1]),np.zeros((1,2)),np.array([[0.,-1.]])),
                          (state["mass"],np.ones((1,2)),np.array([[0.,-1.]])),
                          (state["mass"],np.zeros((1,2)),np.array([[0.,-.5]]))):
            with self.assertRaises(ValueError):
                m.capture_first(state,mass,xy,v,.15)
        rec=m.capture_first(state,state["mass"],np.zeros((1,2)),np.array([[0.,-1.]]),.15)
        rec["apic"][0]=0.
        with self.assertRaises(ValueError):
            m.reduce_mask(rec,1.,1.,.15)

    def test_real_stencil_three_separate_terms(self):
        solver=mods["driver"].fixed_solver()
        x=np.array([[.16,.15],[.25,.14],[.24,.20]])
        vel=np.array([[.5,-.3],[-.4,.1],[.1,-.2]])
        affine=np.array([[[.1,.2],[.5,-.6]],[[0.,-.1],[.1,.4]],[[1.,.5],[-.3,.2]]])
        elastic=np.array([np.eye(2),[[1.02,0.],[0.,.98]],[[1.,.03],[.02,1.]]])
        ids=np.array([0,1,0])
        sample=(x,vel,affine,elastic,ids,np.array([.21,.05,.11]),80,.002,.76)
        s=m.scatter(solver,*sample)
        self.assertTrue(all(np.max(np.abs(s[k]))>0 for k in m.TERMS))
        np.testing.assert_allclose(s["native_y"],sum(s[k] for k in m.TERMS),rtol=1e-13,atol=1e-14)
        self.assertAlmostEqual(s["translation"].sum(),np.dot(sample[5],vel[:,1]))

    def test_direction_consistency_and_cancellation(self):
        self.assertEqual(m.direction(dict(translation=2.,apic=.1,stress=.4))["label"],"TRANSLATION_APIC")
        self.assertEqual(m.direction(dict(translation=.2,apic=.3,stress=2.))["label"],"STRESS")
        self.assertEqual(m.direction(dict(translation=9.,apic=-8.,stress=.1))["label"],"UNRESOLVED")
        self.assertEqual(m.direction(dict(translation=0.,apic=0.,stress=0.))["label"],"UNRESOLVED")
        self.assertEqual(m.direction(dict(translation=.9,apic=0.,stress=.7))["label"],"UNRESOLVED")

    def test_bound_prior(self):
        hist,walls=m.history(PRIOR,prefix,pair)
        for n in (8,16):
            self.assertEqual(len(walls[n]),prefix.STEPS[n])
            prefix.validate_prefix(hist[n],n,hist)
            self.assertEqual(len(m.TARGETS[n]),2 if n==8 else 3)

    def test_observer_delegates_both_calls_and_rejects_changed_prior(self):
        n=8
        dt,width=prefix.DT[n],prefix.WIDTH
        mass=np.array([1.])
        xy=np.array([[0.,0.]])
        state=dict(key=np.array([0]),mass=mass,grid=80,native_y=np.array([-1.]),
                   translation=np.array([-2.]),apic=np.array([1.]),stress=np.array([0.]))
        pri=[None]*268
        phases=[]
        def native_wall(mass,xy,velocity,lid,speed):
            phases.append("native")
            impulse=-float(velocity[0,1])
            velocity[0,1]=0.
            return impulse
        solver=SimpleNamespace(WIDTH=width,WALL_SPEED=.02,LO=.15,walls=native_wall)
        for step in (269,270):
            height=width-dt*step*solver.WALL_SPEED
            pri.append(dict(step=step,u=width-height,p_MPa=10.*(1.25/(dt*width)),
                            pre=dict(M=1.,count=1,mean_down=1.,J=1.),
                            post=dict(M=1.,count=1,mean_down=.25,J=.25)))
        def stub_arm(pair,mods,hist,n,folder):
            folder.mkdir()
            solver.walls=native_wall
            obs=prefix.Observer(solver,SimpleNamespace(project_contacts=lambda *args:None),n)
            obs.rows=[None]*268
            def advance(*args):
                lid=args[-1]
                vel=np.array([[0.,-1.]])
                j=obs.wall(mass,xy,vel,lid,-.02)
                obs.project(.5)
                vel[0,1]=-.25
                j+=obs.wall(mass,xy,vel,lid,-.02)
                return (j/(dt*width),)
            solver.advance=advance
            for step in (269,270):
                obs.advance(80,dt,solver.LO+(width-dt*step*solver.WALL_SPEED))
            (folder/"prefix_receipt.json").write_bytes(b"stub")
        with tempfile.TemporaryDirectory() as root, patch.object(prefix,"arm",stub_arm), \
                patch.object(prefix,"checked_records",return_value=pri), patch.object(m,"scatter",return_value=state):
            folder=Path(root)/"ok"
            m.arm(prefix,None,None,None,{8:pri},n,folder)
            self.assertEqual((folder/"momentum_receipt.json").is_file(),True)
            self.assertEqual(len(phases),4)
            changed=list(pri)
            changed[-1]=dict(pri[-1],post=dict(pri[-1]["post"],J=.26))
            folder=Path(root)/"bad"
            with self.assertRaisesRegex(ValueError,"PRIOR_WALL_PHASES"):
                m.arm(prefix,None,None,None,{8:changed},n,folder)
            self.assertFalse((folder/"momentum_receipt.json").exists())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--prior",type=Path,required=True)
    parser.add_argument("--subject",type=Path,default=Path(__file__).with_name("observe_momentum.py"))
    a,rest=parser.parse_known_args()
    PRIOR=a.prior
    spec=importlib.util.spec_from_file_location("momentum_test_subject",a.subject)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    prefix,pair,mods=m.sources(a.repo)
    unittest.main(argv=[sys.argv[0]]+rest)
