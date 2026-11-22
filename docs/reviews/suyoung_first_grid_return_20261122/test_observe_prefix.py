"""Isolated wall/provenance checks. These tests never advance field state."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import numpy as np


def load(path):
    spec=importlib.util.spec_from_file_location("prefix_contract_subject",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrefixTests(unittest.TestCase):
    def test_weighted_gate_uses_downward_positive_mass_before_clamp(self):
        m=np.array([1.,3.,5.,0.,7.])
        xy=np.array([[0.,.1],[0.,.15],[0.,.1],[0.,.1],[0.,.2]])
        velocity=np.array([[0.,-2.],[7.,-4.],[0.,1.],[0.,-99.],[0.,-77.]])
        before=velocity.copy()
        record=p.floor_measure(m,xy,velocity,.15)
        self.assertEqual(record,dict(count=2,M=4.,mean_down=3.5))
        np.testing.assert_array_equal(velocity,before)
        self.assertEqual(p.component(dict(record,J=14.),.5,1.),280.)

    def test_empty_support_mean_is_null(self):
        rec=p.floor_measure(np.array([2.]),np.array([[.1,.2]]),np.array([[0.,-1.]]),.15)
        self.assertEqual(rec,dict(count=0,M=0.,mean_down=None))
        self.assertEqual(p.component(dict(rec,J=0.),.5,1.),0.)
        with self.assertRaises(ValueError):
            p.component(dict(rec,J=0.,mean_down=0.),.5,1.)

    def test_mismatch_denied(self):
        for rec in [dict(count=1,M=1.,J=10.,mean_down=3.),dict(count=1,M=-3.,J=1.,mean_down=1.),
                    dict(count=1,M=1.,J=float("nan"),mean_down=1.)]:
            with self.assertRaises(ValueError):
                p.component(rec,.5,1.)

    def test_actual_two_native_walls_preserve_arrays_and_impulses(self):
        native=mods["driver"].fixed_solver()
        m=np.array([2.,3.]); xy=np.array([[.2,.12],[.2,.7]])
        vin=np.array([[.2,-2.],[.1,2.]])
        kernel=Mock(); kernel.project_contacts.side_effect=lambda *args:None
        obs=p.Observer(native,kernel,8)
        obs.begin(1)
        v1,v2=vin.copy(),vin.copy()
        expected=native.walls(m,xy,v1,.7,-.01)
        got=obs.wall(m,xy,v2,.7,-.01)
        self.assertEqual(got,expected)
        np.testing.assert_array_equal(v2,v1)
        obs.project(None,None,m,None,v2,None,.5)
        obs.wall(m,xy,v2,.7,-.01)
        self.assertEqual(obs.events,["wall","contact","wall"])
        self.assertEqual(obs.parts[1]["mean_down"],None)

    def test_no_extra_step(self):
        native=mods["driver"].fixed_solver()
        obs=p.Observer(native,mods["kernel"],8)
        obs.rows=[{}]*270
        with self.assertRaises(p.PrefixComplete):
            obs.advance(None)
        self.assertEqual(obs.rows,[{}]*270)

    def test_source_and_real_initialization(self):
        for n in (8,16):
            driver=mods["driver"]
            self.assertEqual(pair.setup_geometry(driver,driver.fixed_solver(),n),pair.expected_geometry(n))

    def test_prior_exact_prefix(self):
        for n,stop in p.STEPS.items():
            raw=hist[n]
            self.assertEqual(len(raw.splitlines()),stop+2)
            with self.assertRaises(ValueError):
                p.validate_prefix(raw+b"\n",n,hist)
            self.assertEqual(len(p.validate_prefix(raw,n,hist)),stop+1)

    def synthetic_arm(self,n,folder):
        # The native writer is used. A test double replaces the integrator
        # and supplies the recorded pressure as the reaction of one fake node.
        driver=mods["driver"]
        solver=driver.fixed_solver()
        replay=p.validate_prefix(hist[n],n,hist)
        seen=[]
        def synthetic(x,v,a,e,fields,vol,grid,dt,lid):
            step=len(seen)+1
            self.assertLessEqual(step,p.STEPS[n])
            pressure=float(replay[step]["bottom_pressure_E"])
            denom=dt*solver.WIDTH
            j=pressure*denom
            if j/denom!=pressure:
                j=math.nextafter(j,math.inf if j/denom<pressure else -math.inf)
            self.assertEqual(j/denom,pressure)
            mass=np.array([1.])
            xy=np.array([[.2,solver.LO]])
            vel=np.array([[0.,-j]])
            speed=-solver.WALL_SPEED
            solver.walls(mass,xy,vel,lid,speed)
            solver.project_contacts(np.array([0]),np.array([0]),mass,np.array([[0.,0.]]),vel,xy,.5)
            solver.walls(mass,xy,vel,lid,speed)
            seen.append(step)
            return x,v,a,e,pressure
        with patch.object(solver,"advance",side_effect=synthetic),patch.object(driver,"fixed_solver",return_value=solver):
            p.arm(pair,mods,hist,n,folder)
        self.assertEqual(seen,list(range(1,p.STEPS[n]+1)))
        return p.checked_records(pair,hist,n,folder)

    def test_synthetic_replay_read_and_rebound_tampering(self):
        with tempfile.TemporaryDirectory() as scratch:
            src=Path(scratch)
            coarse=self.synthetic_arm(8,src/"F8")
            fine=self.synthetic_arm(16,src/"F16")
            summary=p.summarize(coarse,fine)
            self.assertEqual(summary["status"],p.STATUS)
            self.assertTrue(summary["first_exceedance"]["coarse_minus_fine_MPa"]>p.FINE_PEAK/20)
            self.assertEqual(summary["matched"]["components_MPa"]["post"],0.)
            self.assertNotIn("mass_over_dt",summary["first_exceedance"])
            false_path=src/"F8"/"wall_observations.json"
            coarse[-1]["pre"]["mean_down"]*=.5
            false_path.write_text(json.dumps(coarse),encoding="ascii")
            receipt_path=src/"F8"/"prefix_receipt.json"
            receipt=json.loads(receipt_path.read_bytes())
            receipt["observations_sha256"]=p.sha(false_path.read_bytes())
            receipt_path.write_text(json.dumps(receipt),encoding="ascii")
            with self.assertRaises(ValueError):
                p.checked_records(pair,hist,8,src/"F8")

    def test_wall_contact_sequence_rejection(self):
        solver=mods["driver"].fixed_solver()
        observation=p.Observer(solver,mods["kernel"],8)
        observation.begin(1)
        with self.assertRaises(ValueError):
            observation.project(None,None,None,None,None,None,.5)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--prior",type=Path,required=True)
    ap.add_argument("--subject",type=Path,default=Path(__file__).with_name("observe_prefix.py"))
    a,rest=ap.parse_known_args()
    p=load(a.subject)
    pair,mods=p.sources(a.repo)
    hist=p.history(a.prior)
    unittest.main(argv=[sys.argv[0]]+rest)
