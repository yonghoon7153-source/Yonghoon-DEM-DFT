"""Synthetic frozen arithmetic checks. No trajectory runner."""
import importlib.util
import itertools
from pathlib import Path
import unittest

import numpy as np


spec = importlib.util.spec_from_file_location("analysis",Path(__file__).with_name("analyze_stop_node.py"))
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def terminal(x, mass, incoming, mu, qn, qt):
    left, right = np.triu_indices(len(mass), 1)
    normal = x[right]-x[left]
    normal /= np.linalg.norm(normal,axis=1)[:,None]
    tangent = np.column_stack((-normal[:,1],normal[:,0]))
    reduced = 1./(1./mass[left]+1./mass[right])
    kick = reduced[:,None]*(qn[:,None]*normal + qt[:,None]*tangent)
    incidence = np.zeros((len(mass),len(left)))
    incidence[left,np.arange(len(left))] = -1.
    incidence[right,np.arange(len(left))] = 1.
    v = incoming + (incidence@kick)/mass[:,None]
    dv = v[left]-v[right]
    c, s = (np.einsum("pi,pi->p",dv,basis) for basis in (normal,tangent))
    dn = np.maximum(-qn,c)
    dt = np.clip(s,(-mu*qn-qt)-mu*dn,(mu*qn-qt)+mu*dn)
    peak = float(np.max(np.linalg.norm(incoming[left]-incoming[right],axis=1)))
    return {"mass":mass.tolist(),"incoming":incoming.tolist(),"left":left.tolist(),"right":right.tolist(),
            "normal":normal.tolist(),"mu":mu,"speed_tol":1e-13+1e-11*peak,"jn_scaled":qn.tolist(),
            "jt_scaled":qt.tolist(),"closing":c.tolist(),"slip":s.tolist(),"node_id":8,"iteration":512,
            "residual":float(max(max(abs(dn)),max(abs(dt))))}


def triangle():
    x = np.array([[-1.,0.],[1.,0.],[0.,1.]])
    return terminal(x,np.ones(3),-x,.5,np.zeros(3),np.zeros(3))


def coarse_world_velocity():
    # A single frictionless pair on an oblique normal. The third body separates.
    # Round each outgoing world-frame velocity once, as in the pinned iteration.
    boost = float(2**20)
    u = np.spacing(boost)
    x = np.array([[0.,0.],[3.,4.],[6.,8.]])
    vin = boost + u*np.array([[8.,4.],[0.,0.],[100.,100.]])
    return terminal(x,np.ones(3),vin,0.,np.array([8*u,0.,0.]),np.zeros(3))


class Diagnostics(unittest.TestCase):
    def test_terminal_impulses_can_be_wrong_despite_existing_solution(self):
        result = analysis.analyze(triangle())
        self.assertGreater(result["native_ratio"],1e8)
        self.assertTrue(result["terminal_residual_survives_decimal_check"])
        self.assertEqual(result["witness"]["status"],"WITNESS_AT_ORIGINAL_TOLERANCE")

    def test_roundoff_at_large_common_velocity(self):
        result = analysis.analyze(coarse_world_velocity())
        self.assertGreater(result["native_ratio"],100.)
        self.assertLess(result["decimal_ratio_same_terminal_impulses"],.01)
        self.assertEqual(result["witness"]["status"],"WITNESS_AT_ORIGINAL_TOLERANCE")

    def test_mismatched_captured_residual_is_rejected(self):
        node = triangle()
        node["residual"] += .5
        with self.assertRaisesRegex(ValueError,"captured native residual"):
            analysis.analyze(node)

    def test_five_fields_leave_face_existence_open(self):
        x = np.array([[i,i*i] for i in range(5)],float)
        p = len(list(itertools.combinations(x,2)))
        result = analysis.analyze(terminal(x,np.ones(5),x,.5,np.zeros(p),np.zeros(p)))
        self.assertEqual(result["witness"]["status"],"SKIPPED_MORE_THAN_FOUR_FIELDS")


if __name__ == "__main__":
    unittest.main()
