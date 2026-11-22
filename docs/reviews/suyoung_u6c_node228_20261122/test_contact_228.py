"""Known-solution four-body contacts, frozen evidence and failure atomicity. No time integration."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import unittest

import numpy as np


STOP_SHA = "fca406d296c8a6f2b5bb260784711afdc87a34cda48f71ce93c8abcaf7f1059f"
SHARED_SHA = "a0a26056b72b016e17d1d8f0e190131d7e58aca0782aa09a9e6795f7f4484752"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manufacture(seed, mode):
    """Prescribe outgoing states and impulses first, then infer incoming velocities."""
    rng = np.random.default_rng(seed)
    block = np.array([[-1.4, -.65], [-1.25, .61], [1.23, -.56], [1.34, .74]])
    x = block + rng.uniform(-.055, .055, size=(4, 2))
    m = np.exp(rng.uniform(-2.5,2.5,size=4))
    mu = rng.uniform(.14,.80)
    i, j = np.triu_indices(4,1)
    spin = 1. if seed%2 else -1.
    drift = rng.uniform(-.5,.5,size=2)
    # For the split case the two left bodies stick; two right bodies slide;
    # all four cross-pairs separate strictly. In the full case all six slide.
    v = spin*np.column_stack((-x[:,1],x[:,0]))
    if mode == "split":
        v[:2] = [-2.,0.]
        v[2:] += [2.,0.]
    v += drift
    n = x[j]-x[i]
    n /= np.linalg.norm(n,axis=1)[:,None]
    t = np.column_stack((-n[:,1],n[:,0]))
    q = np.zeros((6,2))
    for k,(a,b) in enumerate(zip(i,j)):
        rel = v[a]-v[b]
        c, s = rel @ n[k], rel @ t[k]
        if c < -1e-12:
            continue
        if abs(c) > 1e-12:
            raise AssertionError("invalid manufactured closing speed")
        q[k,0] = rng.uniform(.2,1.0)
        q[k,1] = mu*q[k,0]*(np.sign(s) if abs(s)>1e-12 else .2)
    active = np.flatnonzero(q[:,0]>0)
    if len(active) != (2 if mode=="split" else 6):
        raise AssertionError("manufactured contact graph mismatch")
    vin = v.copy()
    reduced = 1./(1./m[i] + 1./m[j])
    impulse = reduced[:,None]*(q[:,0,None]*n + q[:,1,None]*t)
    np.add.at(vin,i,impulse/m[i,None])
    np.add.at(vin,j,-impulse/m[j,None])
    tol = 1e-13+1e-11*np.max(np.linalg.norm(vin[i]-vin[j],axis=1))
    record = {"mass":m,"field_ids":[17,3,21,6],"left":i,"right":j,"speed_tol":tol,
              "centers":x,"grad":x*m[:,None],"incoming":vin,"mu":mu}
    return CORE.Fixture(record),q.ravel(),v


class FrozenAndHeldOut(unittest.TestCase):
    def setUp(self):
        CORE.WITNESS = None

    def test_frozen_cold_contact_at_step_228(self):
        frozen = CORE.Fixture(NODE)
        frozen.assert_solution(frozen.run())

    def test_frozen_relabel_and_reverse_storage(self):
        frozen = CORE.Fixture(NODE)
        base = frozen.run()
        for labels in itertools.permutations(frozen.ids):
            for order in (np.arange(4),np.arange(3,-1,-1)):
                result = frozen.run(labels,order)
                np.testing.assert_array_equal(result,base)
                frozen.assert_solution(result)

    def test_six_sliding_contacts_known_solutions(self):
        self.check_manufactured("full")

    def test_mixed_sliding_sticking_and_open_known_solutions(self):
        self.check_manufactured("split")

    def check_manufactured(self, mode):
        for seed in range(943,955):
            with self.subTest(seed=seed,mode=mode):
                fixture,q,expected = manufacture(seed,mode)
                fixture.assert_law(q,expected)
                CORE.WITNESS = q
                measured = fixture.run()
                fixture.assert_solution(measured)
                reversed_state = fixture.run(fixture.ids[::-1],np.arange(3,-1,-1))
                np.testing.assert_array_equal(measured,reversed_state)

    def test_atomic_rejection_after_valid_pair(self):
        ids = np.arange(6)
        nodes = np.array([3,3,9,9,9,9])
        mass = np.ones(6)
        centers = np.array([[0.,0.],[1.,0.],[3.,1.],[3.,1.],[3.,1.],[3.,1.]])
        grad = centers.copy()
        vin = np.array([[1.,0.],[-1.,0.],[0.,1.],[0.,0.],[.2,-1.],[-.2,.4]])
        v = vin.copy()
        CORE.SUBJECT.project_contacts(ids[:2],nodes[:2],mass[:2],grad[:2],v[:2],centers,.42)
        self.assertFalse(np.array_equal(v[:2],vin[:2]))
        v = vin.copy()
        with self.assertRaisesRegex(ArithmeticError,"undefined nodal contact normal"):
            CORE.SUBJECT.project_contacts(ids,nodes,mass,grad,v,centers,.42)
        np.testing.assert_array_equal(v,vin)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    for flag in ("repo","node","subject","out"):
        p.add_argument("--"+flag,required=True,type=Path)
    args = p.parse_args()
    core_path = args.repo/"docs/reviews/suyoung_u6c_node145_20261122/test_captured_contact.py"
    if sha(core_path) != SHARED_SHA or sha(args.node) != STOP_SHA:
        raise SystemExit("Fixture or verifier identity differs")
    raw = json.loads(args.node.read_bytes())
    if raw["attempted_step"] != 228 or len(raw["nodes"])!=1 or raw["nodes"][0]["node_id"] != 2304:
        raise SystemExit("Frozen evidence scope differs")
    NODE = raw["nodes"][0]
    before = sha(args.subject)
    CORE = load(core_path,"independent_contact_checks")
    CORE.SUBJECT = load(args.subject,"nodal_subject")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FrozenAndHeldOut)
    names = [t._testMethodName for t in suite]
    results = unittest.TextTestRunner(verbosity=2).run(suite)
    if sha(args.subject) != before:
        raise SystemExit("Source changed during fixture")
    receipt = {"tests":names,"failed":[t.id() for t,_ in results.failures],
               "errors":[t.id() for t,_ in results.errors],"scope":"frozen and manufactured nodes only",
               "source_sha256":before,"test_sha256":sha(Path(__file__)),"capture_sha256":STOP_SHA,
               "manufactured_per_mode":12,"manufactured_modes":2,"rc":int(not results.wasSuccessful())}
    with args.out.open("x",encoding="ascii",newline="\n") as out:
        json.dump(receipt,out,indent=2,sort_keys=True)
        out.write("\n")
    sys.exit(receipt["rc"])
