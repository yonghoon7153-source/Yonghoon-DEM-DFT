"""Setting 1 dense-node observer for the 49-disk development run. CPU only."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = {
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}
MOMENTUM_LIMIT = .01  # Memo §4 U5(c) ④.


def private_solver():
    for name, h in SOURCE.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != h:
            raise ValueError("changed dense solver or material definition")
    path = HERE / "suyoung_u6_first_dev.py"
    spec = importlib.util.spec_from_file_location("u6c_private_dense_solver", path)
    solver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver)
    return solver


def cross2(a, b):
    return a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]


class ContactObservations:
    def __init__(self, sample_every=25):
        if type(sample_every) is not int or sample_every < 1:
            raise ValueError("sample stride must be a positive integer")
        self.sample_every = sample_every
        self.solver = private_solver()
        self.original = self.solver.project_contacts
        self.ids = None
        self.grid = None
        self.data = dict.fromkeys((
            "steps_seen", "sampled_steps", "dense_node_steps", "dense_pair_steps",
            "dense_pair_projections", "separating_subprojections", "separating_nonzero_impulses",
            "positive_work_pairs_raw", "nonzero_slip_pairs_raw", "positive_energy_node_steps_raw",
            "linear_zero_scale_node_steps", "angular_zero_scale_node_steps",
            "linear_over_one_percent", "angular_over_one_percent", "point_identity_changes",
        ), 0)
        self.data.update(dict.fromkeys((
            "max_positive_friction_work", "max_friction_cone_excess", "max_tensile_impulse",
            "max_sliding_magnitude_mismatch_raw", "max_positive_contact_energy_change_node",
            "max_positive_contact_energy_change_sample", "max_linear_residual", "max_angular_residual",
            "max_relative_linear_residual", "max_relative_angular_residual", "max_final_approach_speed",
        ), None))

    def maximum(self, key, values):
        values = np.asarray(values)
        if values.size:
            value = float(np.max(values))
            if not np.isfinite(value):
                raise ArithmeticError("nonfinite contact statistic")
            previous = self.data[key]
            self.data[key] = value if previous is None else max(previous, value)

    def observe_ids(self, ids):
        if self.ids is None:
            self.ids = ids.copy()
        elif not np.array_equal(self.ids, ids):
            self.data["point_identity_changes"] += 1
            raise ValueError("input point identity changed during F run")

    def advance(self, x, v, affine, elastic, ids, volume, grid, dt, lid):
        self.observe_ids(ids)
        self.data["steps_seen"] += 1
        sample = (self.data["steps_seen"] - 1) % self.sample_every == 0
        if sample:
            self.data["sampled_steps"] += 1
            self.grid = grid
            self.solver.project_contacts = self.project
        try:
            return self.solver.advance(x, v, affine, elastic, ids, volume, grid, dt, lid)
        finally:
            self.solver.project_contacts = self.original

    def project(self, ids, nodes, mass, grad, vel, centers, friction):
        # Source-pinned projection schedule. pair_impulse and the rest of the step remain original.
        active = np.flatnonzero(mass > 1e-14 * mass.max())
        order = active[np.lexsort((ids[active], nodes[active]))]
        pairs = []
        for shift in range(1, len(order)):
            equal = nodes[order[:-shift]] == nodes[order[shift:]]
            if not equal.any():
                break
            pairs.append(np.column_stack((order[:-shift][equal], order[shift:][equal])))
        if not pairs:
            return
        left, right = np.concatenate(pairs).T
        normal = grad[right] / mass[right, None] - grad[left] / mass[left, None]
        norms = np.linalg.norm(normal, axis=1)
        weak = norms < 1e-12
        normal[weak] = centers[ids[right[weak]]] - centers[ids[left[weak]]]
        norms[weak] = np.linalg.norm(normal[weak], axis=1)
        if np.any(norms <= 0):
            raise ArithmeticError("undefined normal")
        normal /= norms[:, None]
        _, inverse, counts = np.unique(nodes[left], return_inverse=True, return_counts=True)
        isolated = counts[inverse] == 1
        dense = ~isolated

        def solve(indices, observe):
            a, b = left[indices], right[indices]
            before_a, before_b = vel[a], vel[b]
            va, vb, jn, jt = self.solver.model.pair_impulse(
                mass[a], mass[b], before_a, before_b, normal[indices], friction)
            if observe:
                # Reconstitute the fixed kernel's vector from its returned jn, jt and its
                # pre-update tangent. A mass times rounded velocity difference can erase
                # an impulse on the heavy side of a pair. These values do not update vel.
                relative = before_a - before_b
                n = normal[indices]
                closing = np.sum(relative * n, axis=1)
                tangent = relative - closing[:, None] * n
                speed = np.linalg.norm(tangent, axis=1)
                net_impulse[indices] += jn[:, None] * n + jt[:, None] * tangent / np.maximum(speed[:, None], 1e-30)
                separating = closing <= 0
                self.data["dense_pair_projections"] += len(b)
                self.data["separating_subprojections"] += int(np.count_nonzero(separating))
                self.data["separating_nonzero_impulses"] += int(np.count_nonzero(separating & ((jn != 0) | (jt != 0))))
            vel[a], vel[b] = va, vb

        if isolated.any():
            solve(isolated, False)
        if dense.any():
            before = vel.copy()  # isolated and dense node sets are disjoint
            net_impulse = np.zeros_like(normal)
            groups = ids[left] * len(centers) + ids[right]
            subsets = [dense & (groups == key) for key in np.unique(groups[dense])]
            for _ in range(4):
                for subset in subsets:
                    solve(subset, True)
            self.measure(nodes, mass, before, vel, left[dense], right[dense],
                         normal[dense], net_impulse[dense], friction)

    def measure(self, nodes, mass, before, after, left, right, normal, impulse, friction):
        # One observation per pair/node/step after all four sweeps and before the second wall update.
        bodies = np.union1d(left, right)
        dense_nodes, body_index = np.unique(nodes[bodies], return_inverse=True)
        pair_index = np.searchsorted(dense_nodes, nodes[left])
        xy = np.column_stack(np.divmod(dense_nodes, self.grid + 1)) / self.grid
        self.data["dense_node_steps"] += len(dense_nodes)
        self.data["dense_pair_steps"] += len(left)
        jn = np.einsum("ij,ij->i", impulse, normal)
        jt = cross2(normal, impulse)
        relative = after[right] - after[left]
        slip = cross2(normal, relative)
        work = jt * slip
        self.maximum("max_positive_friction_work", np.maximum(work, 0.))
        self.maximum("max_friction_cone_excess", np.maximum(np.abs(jt) - friction * jn, 0.))
        self.maximum("max_tensile_impulse", np.maximum(-jn, 0.))
        self.maximum("max_final_approach_speed", np.maximum(-np.sum(relative * normal, axis=1), 0.))
        self.data["positive_work_pairs_raw"] += int(np.count_nonzero(work > 0))
        moving = slip != 0
        self.data["nonzero_slip_pairs_raw"] += int(np.count_nonzero(moving))
        self.maximum("max_sliding_magnitude_mismatch_raw", np.abs(np.abs(jt[moving]) - friction * jn[moving]))

        delta_energy = .5 * mass[bodies] * np.sum((after[bodies] - before[bodies]) * (after[bodies] + before[bodies]), axis=1)
        energy_per_node = np.bincount(body_index, weights=delta_energy)
        self.maximum("max_positive_contact_energy_change_node", np.maximum(energy_per_node, 0.))
        self.maximum("max_positive_contact_energy_change_sample", max(float(energy_per_node.sum()), 0.))
        self.data["positive_energy_node_steps_raw"] += int(np.count_nonzero(energy_per_node > 0))

        delta_p = mass[bodies, None] * (after[bodies] - before[bodies])
        p_node = np.column_stack([np.bincount(body_index, weights=delta_p[:, k]) for k in (0, 1)])
        measures = (
            ("linear", np.linalg.norm(p_node, axis=1), np.linalg.norm(impulse, axis=1)),
            ("angular", np.abs(cross2(xy, p_node)), np.abs(cross2(xy[pair_index], impulse))),
        )
        for key, residual, moment_scale in measures:
            scale = np.bincount(pair_index, weights=moment_scale)
            self.maximum("max_" + key + "_residual", residual)
            nonzero = scale > 0
            self.data[key + "_zero_scale_node_steps"] += int(np.count_nonzero(~nonzero))
            ratio = residual[nonzero] / scale[nonzero]
            self.maximum("max_relative_" + key + "_residual", ratio)
            self.data[key + "_over_one_percent"] += int(np.count_nonzero(ratio > MOMENTUM_LIMIT))

    def report(self, arm_status, cells, trace_hash):
        counts = self.data
        momentum_fail = bool(counts["linear_over_one_percent"] or counts["angular_over_one_percent"])
        # Conservative subset. Missing thresholds/inputs never auto-pass the U6 gate.
        failed = momentum_fail or bool(counts["point_identity_changes"] or counts["separating_nonzero_impulses"])
        obligations = {
            "1": "HOLD: nodal closing speed available; disk geometry penetration unmeasured",
            "2": "partial: aggregate applied impulse and per-projection separation; final pair separation protocol and magnitude tolerance missing",
            "2_prime": "partial: final-slip work and saturation residual measured; sticking and rounding tolerances missing",
            "3": "partial: node and sample energy changes measured; rounding tolerance missing",
            "4": "FAIL" if momentum_fail else "sampled residual with defined nonzero scale; zero-scale cases reported separately",
            "5": "HOLD: no independent permutations of complete runs or agreed tolerance",
            "6": "HOLD: no matched force-displacement pair and curve comparison convention",
            "7": "partial: point ID continuity and pinned one-field-per-ID construction; upstream independent ownership audit absent",
        }
        driver = HERE / "suyoung_u6b_dev.py"
        return dict(schema="suyoung_u6c_observation_v1", label="DEVELOPMENT_ONLY",
                    setting=1, cells=cells, arm="F", arm_status=arm_status, trace_sha256=trace_hash,
                    source_sha256=SOURCE, observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    dense_run_driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest() if driver.is_file() else None,
                    point_id_order_i64le_sha256=(hashlib.sha256(np.asarray(self.ids, dtype="<i8").tobytes()).hexdigest()
                                                 if self.ids is not None else None),
                    sampler=dict(first_step=1, stride=self.sample_every, eligible="all active nodes with at least three fields"),
                    metrics=dict(counts), obligations=obligations, u6c_status="FAIL" if failed else "HOLD", u6_qualified=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", required=True, type=int, choices=(8,12,16,24))
    parser.add_argument("--budget", required=True, type=int)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.budget < 1:
        parser.error("positive wall-clock budget required")
    if args.out.exists() or args.out.is_symlink():
        parser.error("new output directory required")
    sys.path.insert(0, str(HERE))
    from suyoung_u6b_dev import run_arm
    observer = ContactObservations()
    try:
        result = run_arm("F", args.cells, args.budget, args.out, advance=observer.advance)
    except (ArithmeticError, ValueError, OSError) as exc:
        # Reaching advance proves this invocation passed run_arm's exclusive mkdir.
        # An exception before the first step never writes into an unowned directory.
        if observer.data["steps_seen"]:
            trace = args.out / "trace.csv"
            trace_hash = hashlib.sha256(trace.read_bytes()).hexdigest() if trace.is_file() else None
            summary = observer.report("INCOMPLETE", args.cells, trace_hash)
            summary["failure_type"] = type(exc).__name__
            write_observations(args.out, summary)
        print("U6C_ARM_INCOMPLETE", type(exc).__name__, file=sys.stderr)
        return 2
    summary = observer.report(result["status"], args.cells, result["trace_sha256"])
    write_observations(args.out, summary)
    print("U6C_STATUS=" + summary["u6c_status"])
    return 0 if result["status"] in ("TARGET_BRACKETED", "GEOMETRY_LIMIT") and summary["u6c_status"] != "FAIL" else 2


def write_observations(folder, summary):
    with (folder / "u6c_observations.json").open("x", encoding="ascii") as out:
        json.dump(summary, out, allow_nan=False, indent=2)
        out.write("\n")


if __name__ == "__main__":
    sys.exit(main())
