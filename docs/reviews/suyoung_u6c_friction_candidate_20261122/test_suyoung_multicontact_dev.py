"""Synthetic, O(1) nodal fixtures. No time steps or field data."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

import numpy as np


NATIVE_SHA = "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5"
MODEL_SHA = "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4"
FIXTURE_SHA = "d8eccd805f0a51a66b33b95ad7b12ae8480378c6cf8e98e93fecdf7eba6e0cc6"
ATOL = 2e-8


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def checked(path, digest):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError("Source identity mismatch: " + path.name)
    return data


def one_node(x, m, v, mu, ids=None, rows=None, zero_grad=False):
    x, m, v = [np.asarray(a, dtype=float) for a in (x, m, v)]
    nr = len(x)
    ids = np.arange(nr) if ids is None else np.array(ids)
    rows = np.arange(nr) if rows is None else np.array(rows)
    centers = np.empty_like(x)
    centers[ids] = x
    grad = np.zeros_like(x) if zero_grad else m[:, None]*x
    speed = v[rows].copy()
    SUBJECT.project_contacts(ids[rows], np.full(nr, 17), m[rows], grad[rows],
                             speed, centers, mu)
    result = np.empty_like(speed)
    result[rows] = speed
    return result


def node_values(key):
    case = CASES[key]
    return tuple(np.array(case[name], dtype=float) for name in
                 ("positions_and_gradient_per_mass", "mass", "incoming_velocity"))


def impulses_explain_result(x, m, vin, vout, mu):
    """Test for at least one admissible impulse decomposition from final speeds.

    An open pair has zero impulse. A closed sliding pair allows one ray on
    the Coulomb boundary opposite its final slip. At zero tangential velocity
    the two extremal rays span the full 2-D static cone. For these triangles
    each possible conic representation has a linearly independent sub-basis.
    """
    changed = (m[:, None]*(vout-vin)).ravel()
    rays = []
    speed_tol = 2e-7
    for i, j in itertools.combinations(range(len(m)), 2):
        normal = x[j] - x[i]
        normal /= np.linalg.norm(normal)
        tangent = np.array([-normal[1], normal[0]])
        relative = vout[j]-vout[i]
        opening = float(relative @ normal)
        if opening < -speed_tol:
            return False
        if opening > speed_tol:
            continue
        slip = float(relative @ tangent)
        ratios = (-mu, mu) if abs(slip) <= speed_tol else (-np.sign(slip)*mu,)
        for ratio in ratios:
            impulse = normal + ratio*tangent
            col = np.zeros_like(vout)
            col[i] = -impulse
            col[j] = impulse
            rays.append(col.ravel())
    if np.linalg.norm(changed) <= ATOL:
        return True
    for ncols in range(1, min(len(rays), 2*len(x)-2)+1):
        for subset in itertools.combinations(rays, ncols):
            matrix = np.column_stack(subset)
            weights = np.linalg.lstsq(matrix, changed, rcond=None)[0]
            if min(weights) >= -ATOL and np.linalg.norm(matrix@weights-changed) <= 1e-7:
                return True
    return False


class NodalContract(unittest.TestCase):
    def assert_close(self, measured, expected):
        np.testing.assert_allclose(measured, expected, atol=ATOL, rtol=0)

    def test_isolated_stick(self):
        self.assert_close(one_node([[-1, 0], [1, 0]], [1, 3], [[2, .8], [0, 0]], .5),
                          [[.5, .2], [.5, .2]])

    def test_isolated_slide_both_tangent_signs_and_limit(self):
        for sign in [-1, 1]:
            # Reduced mass .75; normal impulse 1.5, |tangent impulse| .75.
            self.assert_close(one_node([[-1, 0], [1, 0]], [1, 3],
                                       [[2, 4*sign], [0, 0]], .5),
                              [[.5, 3.25*sign], [.5, .25*sign]])

    def test_open_or_tangent_isolated(self):
        for speed in [-1., 0.]:
            v = [[speed, 4.], [0., 0.]]
            self.assert_close(one_node([[-1, 0], [1, 0]], [1, 3], v, .5), v)

    def test_two_body_native_bytes(self):
        x, m, v = node_values("two_body_control")
        native = v.copy()
        NATIVE.project_contacts(np.arange(2), np.ones(2, dtype=int), m, m[:, None]*x,
                                native, x, .5)
        np.testing.assert_array_equal(one_node(x, m, v, .5), native)

    def test_symmetric_triangle_relabels(self):
        self.assert_relabels(node_values("symmetric_triangle"))

    def test_asymmetric_triangle_relabels(self):
        self.assert_relabels(node_values("asymmetric_triangle"))

    def assert_relabels(self, data):
        x, m, v = data
        target = one_node(x, m, v, .5)
        for perm in itertools.permutations(range(len(m))):
            with self.subTest(physical_to_id=perm):
                # An independently permuted storage ordering must yield the
                # same physical-body outputs for each numerical labeling.
                self.assert_close(one_node(x, m, v, .5, perm, np.roll(perm, 1)), target)

    def test_four_body_relabels(self):
        x = np.array([[-1., -.22], [.9, -.6], [1.04, .74], [-.55, 1.1]])
        m = np.array([1.6, 1., .8, .65])
        v = -x + np.array([[.1, .4], [0., .2], [.15, -.2], [-.3, .12]])
        self.assert_relabels((x, m, v))

    def test_frictionless_oracle(self):
        for key in ("symmetric_triangle", "asymmetric_triangle"):
            x, m, v = node_values(key)
            expected, _ = ORACLE.solve(x, m, v)
            for ids in itertools.permutations(range(3)):
                with self.subTest(case=key, ids=ids):
                    self.assert_close(one_node(x, m, v, 0., ids), expected)

    def test_friction_impulses_explain_final_velocity(self):
        for key in ("symmetric_triangle", "asymmetric_triangle"):
            x, m, v = node_values(key)
            for ids in itertools.permutations(range(3)):
                with self.subTest(case=key, ids=ids):
                    vp = one_node(x, m, v, .5, ids)
                    self.assertTrue(impulses_explain_result(x, m, v, vp, .5))

    def test_balance(self):
        for key in ("symmetric_triangle", "asymmetric_triangle"):
            x, m, v = node_values(key)
            for mu in (0., .5):
                for ids in itertools.permutations(range(3)):
                    vp = one_node(x, m, v, mu, ids)
                    self.assert_close(m @ vp, m @ v)
                    self.assertLessEqual(np.sum(m[:, None]*vp**2),
                                         np.sum(m[:, None]*v**2)+ATOL)

    def test_rigid_coordinate_transform_and_galilean_boost(self):
        x, m, v = node_values("asymmetric_triangle")
        rot = np.array([[.8, -.6], [.6, .8]])
        shift, boost = np.array([4., -2.]), np.array([-.7, 1.1])
        expected = one_node(x, m, v, .5) @ rot.T + boost
        self.assert_close(one_node(x @ rot.T + shift, m, v @ rot.T + boost, .5),
                          expected)

    def test_mass_scale(self):
        x, m, v = node_values("asymmetric_triangle")
        ref = one_node(x, m, v, .5)
        for scale in (1.e-8, 1.e4):
            self.assert_close(one_node(x, m*scale, v, .5), ref)

    def test_weak_gradient_falls_back_to_centers(self):
        x, m, v = node_values("asymmetric_triangle")
        self.assert_close(one_node(x, m, v, .5, zero_grad=True), one_node(x, m, v, .5))

    def test_mixed_single_pair_and_triple_nodes(self):
        x, m, v = node_values("asymmetric_triangle")
        rows = np.array([0, 1, 0, 0, 2, 1, 2])
        nodes = np.array([8, 11, 11, 23, 8, 8, 43])
        vm = v[rows].copy()
        m2 = m[rows]
        extra = np.array([.1, -.2])
        vm[nodes == 11] += extra
        expected = vm.copy()
        expected[nodes == 8] = one_node(x, m, v, .5)[rows[nodes == 8]]
        expected[nodes == 11] = one_node(x[:2], m[:2], v[:2]+extra, .5)[[1, 0]]
        SUBJECT.project_contacts(rows, nodes, m2, x[rows]*m2[:, None], vm, x, .5)
        self.assert_close(vm, expected)

    def test_solver_budget_stop_preserves_all_velocities(self):
        x, m, v = node_values("asymmetric_triangle")
        fields = np.array([0, 1, 0, 1, 2])
        nodes = np.array([3, 3, 9, 9, 9])
        box_vel = v[fields].copy()
        before = box_vel.copy()
        # The historical baseline has no budget guard and still returns a
        # projected state under this controlled zero-budget experiment.
        with mock.patch.object(SUBJECT, "MAX_ITERATIONS", 0, create=True):
            with self.assertRaises(ArithmeticError):
                SUBJECT.project_contacts(fields, nodes, m[fields],
                                         x[fields]*m[fields, None], box_vel, x, .5)
        np.testing.assert_array_equal(box_vel, before)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--subject", type=Path, required=True)
    args, rest = parser.parse_known_args()
    scripts = args.repo/"scripts"
    prior = args.repo/"docs/reviews/suyoung_u6c_seed_return_20261122"/"node_permutation.json"
    normal = args.repo/"docs/reviews/suyoung_u6c_order_return_20261122"/"normal_reference.py"
    checked(scripts/"suyoung_u6_first_dev.py", NATIVE_SHA)
    checked(scripts/"dem_suyoung_sf2d_dev.py", MODEL_SHA)
    global SUBJECT, NATIVE, ORACLE, CASES
    CASES = json.loads(checked(prior, FIXTURE_SHA))["cases"]
    NATIVE = module_at("prior_projector", scripts/"suyoung_u6_first_dev.py")
    ORACLE = module_at("prior_oracle", normal)
    SUBJECT = module_at("current_projector", args.subject)
    unittest.main(argv=[sys.argv[0]]+rest)


if __name__ == "__main__":
    main()
