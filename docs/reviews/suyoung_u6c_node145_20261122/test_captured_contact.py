"""One frozen nodal regression. Supply original capture and a standalone kernel path."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import unittest

import numpy as np


CAPTURE_SHA = "525c57f0d73987c7ea6da8cf3324079712fea4b524757cf148a80989c51bc1e6"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


class Fixture:
    def __init__(self, record, angle=0., boost=(0., 0.), offset=(0., 0.), scale=1.):
        r = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        self.ids = np.array(record["field_ids"], dtype=int)
        self.mass = np.array(record["mass"]) * scale
        self.centers = np.array(record["centers"]) @ r.T + offset
        self.grad = np.array(record["grad"]) @ r.T * scale
        self.v = np.array(record["incoming"]) @ r.T + boost
        self.mu = record["mu"]
        self.tol = record["speed_tol"]
        self.left = np.array(record["left"])
        self.right = np.array(record["right"])
        n = self.grad[self.right]/self.mass[self.right,None] - self.grad[self.left]/self.mass[self.left,None]
        self.normal = n / np.linalg.norm(n, axis=1)[:,None]
        self.tangent = np.column_stack((-self.normal[:,1], self.normal[:,0]))
        rm = 1 / (1/self.mass[self.left] + 1/self.mass[self.right])
        # Each column maps a unit impulse, in pair reduced-mass units, to body velocities.
        cols = []
        for i, j, red, normal, tangent in zip(self.left, self.right, rm, self.normal, self.tangent):
            for direction in (normal, tangent):
                col = np.zeros_like(self.v)
                col[i] = -red * direction / self.mass[i]
                col[j] = red * direction / self.mass[j]
                cols.append(col.ravel())
        self.map = np.column_stack(cols)

    def run(self, ids=None, rows=None):
        labels = self.ids if ids is None else np.array(ids)
        rows = np.arange(len(labels)) if rows is None else rows
        table = np.full((max(labels)+1, 2), np.nan)
        table[labels] = self.centers
        velocities = self.v[rows].copy()
        try:
            SUBJECT.project_contacts(labels[rows], np.full(len(rows), 2976), self.mass[rows],
                                     self.grad[rows], velocities, table, self.mu)
        except ArithmeticError as exc:
            raise AssertionError("admissible fixture rejected: " + str(exc)) from exc
        return velocities[np.argsort(rows)]

    def relative(self, v):
        rel = v[self.left] - v[self.right]
        return np.sum(rel*self.normal, axis=1), np.sum(rel*self.tangent, axis=1)

    def apply(self, impulse):
        return self.v + (self.map @ impulse).reshape(self.v.shape)

    def assert_law(self, impulse, out):
        closing, slip = self.relative(out)
        jn, jt = impulse[::2], impulse[1::2]
        dn = np.maximum(-jn, closing)
        dt = np.clip(slip, -self.mu*(jn+dn)-jt, self.mu*(jn+dn)-jt)
        require(np.max(np.abs(np.r_[dn, dt])) <= self.tol, "original Coulomb tolerance exceeded")
        require(np.max(np.abs(self.apply(impulse)-out)) <= self.tol, "witness does not explain velocity")

    def known_witness(self):
        if WITNESS is not None:
            return WITNESS
        # Recover the published witness's contact face from independent, reduced linear equations.
        # Only the modes are frozen here. No captured physical magnitude is embedded.
        basis = np.eye(self.map.shape[1])
        spans = [basis[0], basis[1], basis[2] + self.mu*basis[3], basis[8], basis[9]]
        expand = np.column_stack(spans)
        def speeds(v):
            n, t = self.relative(v)
            return np.column_stack((n,t)).ravel()[[0,1,2,8,9]]
        response = np.column_stack([speeds((self.map @ ray).reshape(self.v.shape)) for ray in spans])
        weights = np.linalg.solve(response, -speeds(self.v))
        return expand @ weights

    def assert_solution(self, out):
        q = self.known_witness()
        self.assert_law(q, self.apply(q))
        require(np.isfinite(out).all(), "nonfinite solution")
        com = np.average(self.v, axis=0, weights=self.mass)
        weights = self.mass[:,None]
        require(np.max(np.abs(np.sum(weights*(out-self.v),axis=0))) <= self.mass.sum()*self.tol,
                "unbalanced momentum")
        before = np.sum(weights*(self.v-com)**2)
        after = np.sum(weights*(out-com)**2)
        require(after <= before*(1+1e-11)+self.mass.sum()*self.tol**2, "energy increase")
        if np.max(np.abs(self.apply(q) - out)) <= self.tol:
            self.assert_law(q, out)
            return
        # Nonunique impulses/velocities are admissible if independently explained by a feasible
        # decomposition. Enumerate bases of the Coulomb rays permitted by the actual output.
        closing, slip = self.relative(out)
        require(np.max(closing) <= self.tol, "closing pair remains")
        rays = []
        for pair in range(len(closing)):
            if closing[pair] < -self.tol:
                continue
            ratios = (-self.mu, self.mu) if abs(slip[pair]) <= self.tol else (np.sign(slip[pair])*self.mu,)
            for ratio in ratios:
                ray = np.zeros_like(q)
                ray[2*pair:2*pair+2] = [1.,ratio]
                rays.append(ray)
        for k in range(1,min(6,len(rays))+1):
            for chosen in itertools.combinations(rays,k):
                support = np.column_stack(chosen)
                coeff = np.linalg.lstsq(self.map @ support,(out-self.v).ravel(),rcond=None)[0]
                if np.min(coeff) < -self.tol:
                    continue
                try:
                    self.assert_law(support @ coeff,out)
                except AssertionError:
                    continue
                return
        raise AssertionError("no admissible balancing impulse found")


class Node145(unittest.TestCase):
    def test_capture_mapping_and_original_tolerance(self):
        require(NODE["node_id"] == 2976 and len(set(FIX.ids)) == 4, "captured identity mismatch")
        np.testing.assert_allclose(FIX.normal, NODE["normal"], atol=3e-15, rtol=0)
        i, j = np.triu_indices(4, 1)
        np.testing.assert_array_equal(FIX.left,i)
        np.testing.assert_array_equal(FIX.right,j)
        tol = 1e-13 + 1e-11*np.max(np.linalg.norm(FIX.v[i]-FIX.v[j],axis=1))
        self.assertEqual(tol,FIX.tol)

    def test_witness_explains_contact(self):
        witness = FIX.known_witness()
        FIX.assert_law(witness,FIX.apply(witness))

    def test_cold_original_field_rows(self):
        FIX.assert_solution(FIX.run())

    def test_all_label_permutations_in_both_storage_orders(self):
        base = FIX.run()
        for labels in itertools.permutations(FIX.ids):
            for order in (np.arange(4),np.arange(3,-1,-1)):
                result = FIX.run(labels,order)
                np.testing.assert_array_equal(result,base)
                FIX.assert_solution(result)

    def test_rotated_boosted_mass_scaled_span(self):
        fixture = Fixture(NODE,angle=.63,boost=(.12,-.07),offset=(.4,-.8),scale=7.5)
        fixture.assert_solution(fixture.run())

    def test_negatives_unresolved_zero_and_spurious_drift(self):
        feasible = FIX.apply(FIX.known_witness())
        with self.assertRaises(AssertionError):
            FIX.assert_solution(FIX.v)
        with self.assertRaises(AssertionError):
            FIX.assert_solution(feasible + (.01,0.))
        with self.assertRaises(AssertionError):
            FIX.assert_law(np.zeros(12),feasible)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--capture",type=Path,required=True)
    p.add_argument("--subject",type=Path,required=True)
    p.add_argument("--witness",type=Path)
    p.add_argument("--out",type=Path)
    a = p.parse_args()
    subject_sha = sha(a.subject)
    require(sha(a.capture) == CAPTURE_SHA, "unexpected capture SHA256")
    raw = json.loads(a.capture.read_bytes())
    require(raw["step"] == 145 and len(raw["nodes"]) == 1,"capture scope")
    NODE = raw["nodes"][0]
    WITNESS = None
    if a.witness:
        w = json.loads(a.witness.read_bytes())
        require(w["capture_sha256"] == CAPTURE_SHA and len(w["nodes"]) == 1,"unbound witness")
        WITNESS = np.array(w["nodes"][0]["witness"]["scaled_impulses_nt"])
        require(WITNESS.shape == (12,) and np.isfinite(WITNESS).all(),"invalid witness layout")
    FIX = Fixture(NODE)
    spec = importlib.util.spec_from_file_location("contact_subject",a.subject)
    SUBJECT = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(SUBJECT)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Node145)
    names = [t._testMethodName for t in suite]
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    require(sha(a.subject) == subject_sha, "source changed during run")
    if a.out:
        data = {"tests":names,"failures":[t._testMethodName for t,_ in result.failures],
                "errors":[t._testMethodName for t,_ in result.errors],"run":result.testsRun,
                "rc":int(not result.wasSuccessful()),"capture_sha256":CAPTURE_SHA,
                "subject_sha256":subject_sha,"test_sha256":sha(Path(__file__)),
                "witness_sha256":sha(a.witness) if a.witness else None}
        with a.out.open("x",encoding="utf-8") as f:
            json.dump(data,f,indent=2)
            f.write("\n")
    sys.exit(int(not result.wasSuccessful()))
