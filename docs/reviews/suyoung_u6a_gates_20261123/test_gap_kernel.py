"""Analytic single-step contact tests. No seeded pressing run is performed."""
import importlib.util
import itertools
import os
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


here = Path(__file__).resolve()
candidate = load("option_two", here.with_name("gap_kernel.py"))
native = Path(os.environ.get("SUYOUNG_GAP_NATIVE",
                            here.parents[3] / "scripts" / "suyoung_multicontact_dev.py"))
kernel = load("original_multicontact", native)


def surface(centers, radius=.25):
    theta = np.arange(256) * (2*np.pi/256)
    circle = radius * np.column_stack((np.cos(theta), np.sin(theta)))
    return SimpleNamespace(groups=np.repeat(np.arange(len(centers)), 256),
                           positions=np.concatenate([center+circle for center in centers]))


def fixture(centers, velocities):
    ids = np.arange(len(centers))
    return [ids, np.zeros(len(ids), dtype=int), np.ones(len(ids)), np.zeros((len(ids), 2)),
            np.array(velocities, dtype=float), np.asarray(centers, dtype=float), .5]


class GapKernelTest(unittest.TestCase):
    def setUp(self):
        self.projector = candidate.GapProjector(kernel)

    def test_free_and_threshold(self):
        for speed in (-.75, .25, .5):
            args = fixture([(0,0),(1,0)], [(speed,.3),(0.,-.1)])
            original = args[4].copy()
            self.projector.project(surface(args[5]), 1., *args)
            np.testing.assert_array_equal(args[4], original)

    def test_partial_approach_and_coulomb_in_both_directions(self):
        for sy in (-1, 1):
            args = fixture([(0,0),(1,0)], [(1.,sy),(0.,0.)])
            self.projector.project(surface(args[5]), 1., *args)
            np.testing.assert_allclose(args[4], [[.75,sy*.875],[.25,sy*.125]], atol=1e-14)
            np.testing.assert_allclose(args[4].sum(axis=0), [1.,sy])

    def test_exact_historical_path_with_negative_gap(self):
        for positions in [[(0,0),(.5,0)],[(0,0),(.4,0)],[(0,0),(.3,0),(.15,.25)]]:
            args = fixture(positions, [(1,.4),(-.2,0.),(-.1,-.8)][:len(positions)])
            expected = args[4].copy()
            kernel.project_contacts(*args[:4], expected, *args[5:])
            self.projector.project(surface(args[5]), .1, *args)
            np.testing.assert_array_equal(args[4], expected)

    def test_sticking_with_positive_allowance_and_swapped_ids(self):
        xy=np.array([(0,0),(1,0)])
        v=np.array([(1.,.1),(0.,0.)])
        for index in ([0,1],[1,0]):
            args=fixture(xy[index],v[index])
            self.projector.project(surface(args[5]),1.,*args)
            np.testing.assert_allclose(args[4][np.argsort(index)],[[.75,.05],[.25,.05]],atol=1e-14)

    def test_positive_gap_three_body_friction_under_all_id_permutations(self):
        xy=np.array([[0,0],[.74,0],[.48,.73]])
        v=np.array([[1.,.9],[-.3,.7],[-.1,-.5]])
        expected=None
        for perm in itertools.permutations(range(3)):
            perm=np.asarray(perm)
            args=fixture(xy[perm],v[perm])
            self.projector.project(surface(args[5]), 1., *args)
            out=args[4][np.argsort(perm)]
            if expected is None:
                expected=out.copy()
            np.testing.assert_allclose(out,expected,rtol=0.,atol=2e-12)
            np.testing.assert_allclose(out.sum(axis=0),v.sum(axis=0),atol=2e-12)
            self.assertLess(np.square(out).sum(), np.square(v).sum())
            verts=surface(xy).positions.reshape(3,256,2)
            for a,b in itertools.combinations(range(3),2):
                n=(xy[b]-xy[a])/np.linalg.norm(xy[b]-xy[a])
                allowed=max(0, (verts[b]@n).min() - (verts[a]@n).max())
                self.assertLessEqual((out[a]-out[b])@n,allowed+4e-11)

    def test_inherited_polish_handles_nonzero_allowance(self):
        self.projector.derived.MAX_ITERATIONS=1
        polished=[]
        previous=self.projector.derived._polish_node
        def capture(*args):
            polished.append(args[-1].copy())
            return previous(*args)
        self.projector.derived._polish_node=capture
        xy=[(0,0),(.74,0),(.48,.73)]
        args=fixture(xy,[(1,.9),(-.3,.7),(-.1,-.5)])
        self.projector.project(surface(args[5]),1.,*args)
        self.assertTrue(polished)
        self.assertTrue(np.all(polished[0]>0))
        for a,b in itertools.combinations(range(3),2):
            n=np.subtract(xy[b],xy[a]); n=n/np.linalg.norm(n)
            allowed=max(0, np.min(surface(args[5]).positions.reshape(3,256,2)[b]@n)-
                           np.max(surface(args[5]).positions.reshape(3,256,2)[a]@n))
            self.assertLessEqual(np.dot(args[4][a]-args[4][b],n),allowed+1e-10)

    def test_surface_is_current_at_each_call(self):
        xy=[(0,0),(1,0)]
        b=surface(xy)
        args=fixture(xy,[(.25,0),(0,0)])
        self.projector.project(b,1.,*args)
        np.testing.assert_array_equal(args[4],[[.25,0],[0,0]])
        b.positions[b.groups==1,0]-=.5
        self.projector.project(b,1.,*args)
        np.testing.assert_allclose(args[4],[[.125,0],[.125,0]],atol=1e-15)

    def test_no_new_node_pair_and_time_scaling(self):
        args=fixture([(0,0),(1,0)], [(1.,0.),(0.,0.)])
        args[1][:]=[1,2]
        self.projector.project(surface(args[5]),2.,*args)
        np.testing.assert_array_equal(args[4],[[1.,0.],[0.,0.]])
        args[1][:]=0
        self.projector.project(surface(args[5]),2.,*args)
        np.testing.assert_allclose(args[4],[[.625,0.],[.375,0.]])
        self.assertFalse(self.projector.metadata()["distance_based_contact_detection"])

    def test_missing_surface_is_rejected_before_velocities_change(self):
        args=fixture([(0,0),(1,0),(2,0)], [(1.,0.),(0.,0.),(-1.,0.)])
        b=surface(args[5])
        b.groups=b.groups[:-1]; b.positions=b.positions[:-1]
        with self.assertRaises(ValueError):
            self.projector.project(b,1.,*args)
        np.testing.assert_array_equal(args[4],[[1,0],[0,0],[-1,0]])

    def test_ambiguous_normal_defers_all_updates(self):
        args=fixture([(0,0),(.4,0),(1,0),(1,0),(1,0)],
                     [(1.,0.),(0.,0.),(0.,0.),(0.,0.),(0.,0.)])
        args[1][:]=[0,0,1,1,1]
        before=args[4].copy()
        with self.assertRaisesRegex(ArithmeticError,"undefined nodal"):
            self.projector.project(surface(args[5]),1.,*args)
        np.testing.assert_array_equal(args[4],before)


if __name__ == "__main__":
    unittest.main()
