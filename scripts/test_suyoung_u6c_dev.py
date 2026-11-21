"""Finite invented contact cases only. No research run or scheduler is called."""
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import suyoung_u6_first_dev as fixed
try:
    import suyoung_u6c_dev as candidate
except ModuleNotFoundError as missing:
    if missing.name != "suyoung_u6c_dev":
        raise
    candidate = None


def mixed():
    # Three shared fields at node 11, isolated pair at node 12, single field at 13.
    ids = np.array([2, 0, 1, 1, 0, 0])
    nodes = np.array([11, 11, 11, 12, 12, 13])
    mass = np.array([.008, .011, .005, .003, .007, .01])
    grad = np.array([[1., 0.], [.3, .6], [-.2, .1], [0., .4], [-.8, 1.], [.9, -.3]])
    centers = np.array([[.2, .4], [.5, .6], [.1, .5]])
    velocity = np.array([[0., -.5], [.3, .4], [-.2, .7], [.1, 1.], [.1, -.5], [.2, -.3]])
    return ids, nodes, mass, grad, velocity, centers


class ContactTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(candidate, "dense contact observation entry point missing")

    def test_original_projection_bytes_and_denominators(self):
        ids, nodes, m, grad, gv, centers = mixed()
        original = gv.copy()
        fixed.project_contacts(ids, nodes, m, grad, original, centers, .5)
        c = candidate.ContactObservations()
        c.grid = 9
        c.project(ids, nodes, m, grad, gv, centers, .5)
        self.assertEqual(gv.tobytes(), original.tobytes())
        self.assertEqual(c.data["dense_node_steps"], 1)
        self.assertEqual(c.data["dense_pair_steps"], 3)
        self.assertEqual(c.data["dense_pair_projections"], 12)

    def test_one_or_two_field_nodes_do_not_enter_denominators(self):
        ids, nodes, m, grad, gv, centers = mixed()
        nodes = np.arange(len(ids))
        nodes[1] = nodes[0]
        c = candidate.ContactObservations(); c.grid = 9
        ref = gv.copy()
        fixed.project_contacts(ids, nodes, m, grad, ref, centers, .5)
        c.project(ids, nodes, m, grad, gv, centers, .5)
        self.assertEqual(gv.tobytes(), ref.tobytes())
        self.assertEqual(c.data["dense_node_steps"], 0)
        self.assertIsNone(c.data["max_positive_friction_work"])

    def test_friction_work_uses_final_relative_velocity_and_impulse_on_right(self):
        c = candidate.ContactObservations(); c.grid = 9
        # A pair has accumulated tangential impulse +0.2 on the right.
        # Its final relative tangential velocity +2 gives +0.4 (wrong direction).
        ids = np.array([0, 1, 2]); node=np.array([11, 11, 11])
        mass=np.ones(3); pre=np.zeros((3,2)); post=np.array([[0.,0.],[0.,2.],[0.,0.]])
        left=np.array([0,0,1]); right=np.array([1,2,2]); normals=np.array([[1.,0.]]*3)
        impulse=np.array([[1.,.2],[0.,0.],[0.,0.]])
        c.measure(node, mass, pre, post, left, right, normals, impulse, .5)
        self.assertAlmostEqual(c.data["max_positive_friction_work"], .4)
        self.assertAlmostEqual(c.data["max_positive_contact_energy_change_node"], 2.)
        self.assertGreater(c.data["max_linear_residual"], 0.)
        self.assertEqual(c.data["positive_work_pairs_raw"], 1)
        self.assertEqual(c.data["max_friction_cone_excess"],0.)

    def test_zero_impulse_has_no_relative_denominator(self):
        c = candidate.ContactObservations(); c.grid = 9
        zero=np.zeros((3,2))
        c.measure(np.ones(3,dtype=int),np.ones(3),zero,zero,np.array([0,0,1]),np.array([1,2,2]),
                  np.array([[1.,0.]]*3),zero,.5)
        self.assertEqual(c.data["linear_zero_scale_node_steps"],1)
        self.assertIsNone(c.data["max_relative_linear_residual"])

    def test_full_step_bit_identity_and_sampling(self):
        c=candidate.ContactObservations(sample_every=2)
        ids=np.array([0,1,2])
        x=np.array([[.401,.402],[.405,.399],[.404,.405]])
        v=np.array([[.001,0.],[-.001,.001],[0.,-.0001]])
        affine=np.zeros((3,2,2)); elastic=np.repeat(np.eye(2)[None,:,:],3,axis=0)
        vol=np.full(3,.001)
        a=(x,v,affine,elastic); b=tuple(y.copy() for y in a)
        original=fixed.project_contacts
        for _ in range(3):
            expected=fixed.advance(*a,ids,vol,10,.0001,.8)
            got=c.advance(*b,ids,vol,10,.0001,.8)
            for l,r in zip(expected,got):
                self.assertEqual(np.asarray(l).tobytes(),np.asarray(r).tobytes())
            a,b=expected[:4],got[:4]
        self.assertIs(fixed.project_contacts, original)
        self.assertEqual(c.data["sampled_steps"],2)
        self.assertEqual(c.data["steps_seen"],3)
        self.assertGreater(c.data["dense_node_steps"],0)

    def test_changed_point_identity_is_rejected(self):
        c=candidate.ContactObservations()
        c.observe_ids(np.array([0,0,1,1]))
        with self.assertRaises(ValueError):
            c.observe_ids(np.array([0,1,0,1]))

    def test_empty_and_partial_never_qualify(self):
        c=candidate.ContactObservations()
        res=c.report("TIME_LIMIT",8,"f"*64)
        self.assertEqual(res["u6c_status"],"HOLD")
        self.assertFalse(res["u6_qualified"])
        self.assertEqual(len(res["obligations"]),8)
        self.assertIn("geometry",res["obligations"]["1"])
        self.assertIsNone(res["metrics"]["max_positive_contact_energy_change_node"])
        json.dumps(res,allow_nan=False)

    def test_registered_identity_violation_takes_precedence(self):
        c=candidate.ContactObservations()
        c.observe_ids(np.array([0,1]))
        with self.assertRaises(ValueError):
            c.observe_ids(np.array([0,0]))
        self.assertEqual(c.report("INCOMPLETE",8,None)["u6c_status"],"FAIL")

    def test_sampler_validation(self):
        for n in (0,-1,True,1.5):
            with self.subTest(n=n),self.assertRaises(ValueError):
                candidate.ContactObservations(n)

    def test_explicit_momentum_violation_precedes_missing_inputs(self):
        c = candidate.ContactObservations(); c.grid = 9
        node = np.full(3, 11); pre=np.zeros((3,2)); post=pre.copy(); post[1,1]=1.
        c.measure(node,np.ones(3),pre,post,np.array([0,0,1]),np.array([1,2,2]),
                  np.array([[1.,0.]]*3),np.array([[1.,0.],[0.,0.],[0.,0.]]),.5)
        self.assertEqual(c.report("INCOMPLETE",8,None)["obligations"]["4"],"FAIL")
        self.assertEqual(c.report("INCOMPLETE",8,None)["u6c_status"],"FAIL")

    def test_time_limited_new_run_writes_partial_observations(self):
        def fake(arm,cells,budget,out,*,advance):
            out.mkdir(exist_ok=False)
            self.assertEqual(arm,"F")
            return {"status":"TIME_LIMIT","trace_sha256":"a"*64}
        module=types.SimpleNamespace(run_arm=fake)
        with tempfile.TemporaryDirectory() as temp, patch.dict(sys.modules,{"suyoung_u6b_dev":module}):
            target=Path(temp)/"F8"
            self.assertEqual(candidate.main(["--cells","8","--budget","1","--out",str(target)]),2)
            doc=json.loads((target/"u6c_observations.json").read_bytes())
            self.assertEqual((doc["arm_status"],doc["u6c_status"]),("TIME_LIMIT","HOLD"))

    def test_exception_preserves_observation_and_trace_identity(self):
        def fake(arm,cells,budget,out,*,advance):
            out.mkdir(exist_ok=False)
            (out/"trace.csv").write_bytes(b"synthetic\n")
            advance.__self__.data["steps_seen"]=1
            raise ArithmeticError("synthetic")
        import hashlib
        with tempfile.TemporaryDirectory() as temp, patch.dict(sys.modules,{"suyoung_u6b_dev":types.SimpleNamespace(run_arm=fake)}):
            target=Path(temp)/"F8"
            self.assertEqual(candidate.main(["--cells","8","--budget","1","--out",str(target)]),2)
            doc=json.loads((target/"u6c_observations.json").read_bytes())
            self.assertEqual(doc["arm_status"],"INCOMPLETE")
            self.assertEqual(doc["trace_sha256"],hashlib.sha256(b"synthetic\n").hexdigest())


if __name__=="__main__":
    unittest.main()
