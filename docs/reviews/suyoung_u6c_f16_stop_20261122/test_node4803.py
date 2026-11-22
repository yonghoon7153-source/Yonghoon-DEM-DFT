"""Fixed F16 three-field node, native field-law and search-domain checks. No field time stepping."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import unittest

import numpy as np


CAPTURE = "c424d8e7a4d799969d052acac3692c47a44a1a6657ab6497c62cbf516146e775"
CORE_SHA = "a0a26056b72b016e17d1d8f0e190131d7e58aca0782aa09a9e6795f7f4484752"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enumerate_probed_modes(body_count, mu, open_indices):
    """Force each private face check to reject to audit reachability, not physical validity."""
    left, right = np.triu_indices(body_count,1)
    pair_count = len(left)
    incidence = np.zeros((body_count,pair_count))
    incidence[left,np.arange(pair_count)] = -1.
    incidence[right,np.arange(pair_count)] = 1.
    normal = np.tile([1.,0.],(pair_count,1))
    tangent = np.tile([0.,1.],(pair_count,1))
    guess = np.ones(pair_count)
    guess[open_indices] = -2.
    seen = []
    def capture(frame,event,value):
        if (event=="call" and frame.f_code.co_name=="on_face" and
                frame.f_globals is SOLVER.__dict__):
            seen.append(tuple(frame.f_locals["modes"]))
    previous_profiler=sys.getprofile()
    sys.setprofile(capture)
    try:
        # Negative tolerance is deliberately used only for this exhaustive
        # private search audit. It cannot enter through project_contacts().
        result=SOLVER._polish_node(np.zeros((body_count,2)),np.ones(body_count),incidence,
                                   normal,tangent,np.full(pair_count,.5),mu,
                                   np.zeros(pair_count),np.zeros(pair_count),guess,np.zeros(pair_count),-1.)
        assert result is None
    finally:
        sys.setprofile(previous_profiler)
    return seen


class Node4803(unittest.TestCase):
    def test_decimal_terminal_and_independent_witness(self):
        q = np.column_stack((NODE["jn_scaled"],NODE["jt_scaled"])).ravel()
        self.assertGreater(AUDIT.evaluate_impulse(NODE,q)["residual"],1.e6*NODE["speed_tol"])
        self.assertEqual(WITNESS["modes"],["plus","open","stick"])
        result=AUDIT.evaluate_impulse(NODE,WITNESS["scaled_impulses_nt"])
        self.assertTrue(result["energy_bound_satisfied"])
        self.assertLessEqual(result["residual"],NODE["speed_tol"])

    def test_cold_node_accepted_at_original_tolerance(self):
        fixture = CORE.Fixture(NODE)
        velocity = fixture.run()
        fixture.assert_solution(velocity)
        np.testing.assert_allclose(velocity,fixture.apply(CORE.WITNESS),atol=NODE["speed_tol"],rtol=0)

    def test_six_relabels_and_two_storage_orders(self):
        fixture = CORE.Fixture(NODE)
        reference = fixture.run()
        for ids in itertools.permutations(fixture.ids):
            for rows in (np.arange(3),np.arange(2,-1,-1)):
                velocity=fixture.run(ids,rows)
                np.testing.assert_array_equal(velocity,reference)
                fixture.assert_solution(velocity)

    def assert_full_domain(self,body_count):
        for mu,choices in ((0.,("open","normal")),(.5,("open","stick","positive","negative"))):
            pair_count=body_count*(body_count-1)//2
            expected=set(itertools.product(choices,repeat=pair_count))
            for open_indices in ([],[0]):
                seen=enumerate_probed_modes(body_count,mu,open_indices)
                self.assertEqual(len(seen),len(set(seen)))
                self.assertEqual(set(seen),expected)

    def test_three_field_all_faces_once(self):
        self.assert_full_domain(3)

    def test_four_field_all_faces_once(self):
        self.assert_full_domain(4)

    def test_five_field_original_search_envelope(self):
        for mu,choices in ((0.,("open","normal")),(.5,("open","stick","positive","negative"))):
            seen=enumerate_probed_modes(5,mu,[0])
            first=seen[0]
            # Exactly original warm state + one- and two-mode changes.
            self.assertEqual(len(seen),1+10*(len(choices)-1)+45*(len(choices)-1)**2)
            self.assertEqual(len(seen),len(set(seen)))
            self.assertTrue(all(sum(a!=b for a,b in zip(first,mode))<=2 for mode in seen))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for name in ("repo","node","subject","out"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    if digest(args.node)!=CAPTURE:
        raise SystemExit("Wrong fixed observation")
    capture=json.loads(args.node.read_bytes())
    NODE,=capture["nodes"]
    if (capture["attempted_step"],capture["scope"],NODE["node_id"])!=(4803,"NATIVE_UNRESOLVED_ROWS",16810):
        raise SystemExit("Wrong captured row")
    shared=args.repo/"docs/reviews/suyoung_u6c_node145_20261122/test_captured_contact.py"
    if digest(shared)!=CORE_SHA:
        raise SystemExit("Wrong fixture checker")
    CORE=load("existing_frozen_fixtures",shared)
    SOLVER=CORE.SUBJECT=load("candidate_projector",args.subject)
    AUDIT=load("independent_law",args.repo/"docs/reviews/suyoung_u6c_step145_20261122/analyze_stop_node.py")
    WITNESS=AUDIT.look_for_witness(NODE)
    CORE.WITNESS=np.array(WITNESS["scaled_impulses_nt"])
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Node4803)
    titles=[t._testMethodName for t in suite]
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    record=dict(tests=titles,source_sha256=digest(args.subject),capture_sha256=CAPTURE,
                failed=[t.id() for t,_ in result.failures],errors=[t.id() for t,_ in result.errors],
                rc=int(not result.wasSuccessful()))
    with args.out.open("x",encoding="ascii",newline="\n") as stream:
        json.dump(record,stream,sort_keys=True,indent=2)
        stream.write("\n")
    raise SystemExit(record["rc"])
