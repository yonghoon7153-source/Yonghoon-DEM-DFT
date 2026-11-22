"""Development candidate for simultaneous inelastic Coulomb contact at an F node.

The single-pair law, active mass cutoff and normal definition are inherited
from the F8 driver. Multi-field nodes use accumulated impulses from a common
velocity iterate. No project or material parameters are changed on import.
"""
import importlib.util
import itertools
from pathlib import Path

import numpy as np


def _load_pair_impulse():
    source = Path(__file__).with_name("dem_suyoung_sf2d_dev.py")
    spec = importlib.util.spec_from_file_location("suyoung_pair_material", source)
    material = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(material)
    return material.pair_impulse


_pair_impulse = _load_pair_impulse()
MAX_ITERATIONS = 512
ABS_SPEED_TOL = 1e-13
REL_SPEED_TOL = 1e-11


def _normals(rows, left, right, ids, mass, grad, centers):
    a, b = rows[:, left], rows[:, right]
    direction = grad[b] / mass[b, None] - grad[a] / mass[a, None]
    norms = np.linalg.norm(direction, axis=2)
    weak = norms < 1e-12
    if np.any(weak):
        direction[weak] = centers[ids[b[weak]]] - centers[ids[a[weak]]]
        norms[weak] = np.linalg.norm(direction[weak], axis=1)
    if np.any(norms <= 0.) or not np.isfinite(norms).all():
        raise ArithmeticError("undefined nodal contact normal")
    return direction / norms[:, :, None]


def _impulse_changes(jn, jt, closing, slip, mu):
    # Algebraically these are the projected impulses minus the current ones.
    # Evaluate the *changes* to avoid losing a small closing or slip speed
    # when the scaled accumulated impulse is comparatively large.
    change_n = np.maximum(-jn, closing)
    low = (-mu*jn - jt) - mu*change_n
    high = (mu*jn - jt) + mu*change_n
    return change_n, np.clip(slip, low, high)


def _remaining_four_body_faces(guess, choices):
    """Order previously untested faces by changes other than opening a pair."""
    buckets = [[] for _ in range(len(guess) + 1)]
    for modes in itertools.product(choices, repeat=len(guess)):
        changed = [new for old, new in zip(guess, modes) if old != new]
        retained_changes = sum(new != "open" for new in changed)
        # Hamming distances 0--2 and all release-only faces were tried first.
        if len(changed) > 2 and retained_changes:
            buckets[retained_changes].append(modes)
    for bucket in buckets:
        yield from bucket


def _polish_node(incoming, mass, incidence, normal, tangent, reduced_mass,
                 mu, jn, jt, guess_n, guess_t_raw, speed_tol):
    """Solve a proposed linear contact face, then check the original nonlinear law."""
    pair_count = len(jn)
    directions = np.stack((normal, tangent), axis=1)
    jacobian = (incidence.T[:, None, :, None] * directions[:, :, None, :]).reshape(
        2*pair_count, -1)
    inv_mass = 1. / np.repeat(mass, 2)
    scale = np.repeat(reduced_mass, 2)
    # J v is separating/slip speed with the opposite signs to 'closing/slip'.
    response = ((jacobian * inv_mass) @ jacobian.T) * scale
    initial_closing = -(jacobian @ incoming.ravel())
    guess = []
    for pn, pt in zip(guess_n, guess_t_raw):
        if pn <= speed_tol:
            mode = "open"
        elif mu == 0.:
            mode = "normal"
        elif abs(pt) <= mu*pn:
            mode = "stick"
        else:
            mode = "positive" if pt > 0. else "negative"
        guess.append(mode)

    def on_face(modes):
        equations = []
        columns = []
        base = []
        for pair, mode in enumerate(modes):
            if mode == "open":
                continue
            n, t = 2*pair, 2*pair+1
            normal_column = np.zeros(2*pair_count)
            normal_column[n] = 1.
            if mode in ("positive", "negative"):
                normal_column[t] = mu if mode == "positive" else -mu
            columns.append(normal_column)
            equations.append(n)
            base.append(jn[pair])
            if mode == "stick":
                tangent_column = np.zeros(2*pair_count)
                tangent_column[t] = 1.
                columns.append(tangent_column)
                equations.append(t)
                base.append(jt[pair])
        scaled_impulse = np.zeros(2*pair_count)
        if columns:
            mapping = np.column_stack(columns)
            block = response[equations] @ mapping
            rhs = initial_closing[equations] - block @ base
            # In a redundant contact network keep the correction close to the
            # last simultaneous iterate, rather than assuming unique impulses.
            delta, *_ = np.linalg.lstsq(block, rhs, rcond=None)
            scaled_impulse = mapping @ (np.asarray(base) + delta)
        v = incoming + ((jacobian.T @ (scale * scaled_impulse)) * inv_mass).reshape(-1, 2)
        closing, slip = (-(jacobian @ v.ravel())).reshape(-1, 2).T
        pn, pt = scaled_impulse.reshape(-1, 2).T
        dn, dt = _impulse_changes(pn, pt, closing, slip, mu)
        error = np.max(np.maximum(np.abs(dn), np.abs(dt)))
        if np.isfinite(error) and error <= speed_tol:
            return v
        return None

    result = on_face(guess)
    if result is not None:
        return result
    # A rapidly changing neighbour can keep an opening/sticking decision on
    # the wrong side. Try one adjacent contact mode at a time; larger groups
    # still fail closed if their Jacobi iterations and this polish both fail.
    choices = ("open", "normal") if mu == 0. else ("open", "stick", "positive", "negative")
    for index, mode in itertools.product(range(pair_count), choices):
        if mode != guess[index]:
            alternative = guess.copy()
            alternative[index] = mode
            result = on_face(alternative)
            if result is not None:
                return result
    if len(mass) <= 5:
        # At most ten pairs. Two simultaneous mode changes cover the case
        # in which neither single change gives an admissible solution.
        # Maximum extra trials for mu > 0: C(10,2) * 3**2 = 405.
        for a, b in itertools.combinations(range(pair_count), 2):
            for mode_a, mode_b in itertools.product(choices, repeat=2):
                if mode_a == guess[a] or mode_b == guess[b]:
                    continue
                alternative = guess.copy()
                alternative[a], alternative[b] = mode_a, mode_b
                result = on_face(alternative)
                if result is not None:
                    return result
    if len(mass) <= 4:
        # Redundant small networks may release three or more contacts at
        # once. Keep the predicted stick/slide law on the other contacts.
        # Enumerate only subsets of currently closed contacts (at most
        # 42 extra faces for six pairs), using the same residual gate.
        closed = [i for i, mode in enumerate(guess) if mode != "open"]
        for count in range(3, len(closed) + 1):
            for released in itertools.combinations(closed, count):
                alternative = guess.copy()
                for i in released:
                    alternative[i] = "open"
                result = on_face(alternative)
                if result is not None:
                    return result
    if len(mass) in (3, 4):
        # Three or six pairs give at most 4**3 or 4**6 labels across all tiers.
        # A singular face has one least-squares representative tested here.
        for modes in _remaining_four_body_faces(guess, choices):
            result = on_face(modes)
            if result is not None:
                return result
    return None


def _simultaneous(incoming, mass, left, right, normal, mu):
    """Solve independent nodes with the same number of fields in a batch.

    A positive normal relative speed is closing. An impulse acts on the
    right body and its opposite acts on the left body. The impulse variables
    below are divided by the pair's reduced mass, so residuals are speeds.
    Only a zero of BOTH projected impulse updates satisfies the implemented
    normal complementarity and sticking/sliding law.
    """
    node_count, body_count, _ = incoming.shape
    pairs = np.arange(len(left))
    incidence = np.zeros((body_count, len(pairs)))
    incidence[left, pairs] = -1.
    incidence[right, pairs] = 1.
    reduced_mass = 1. / (1. / mass[:, left] + 1. / mass[:, right])
    tangent = np.stack((-normal[:, :, 1], normal[:, :, 0]), axis=2)
    speed_scale = np.max(np.linalg.norm(incoming[:, left] - incoming[:, right], axis=2), axis=1)
    speed_tol = ABS_SPEED_TOL + REL_SPEED_TOL * speed_scale
    jn = np.zeros((node_count, len(pairs)))
    jt = np.zeros_like(jn)
    velocity = incoming.copy()
    relax = 0.9 / (body_count - 1)
    for iteration in range(MAX_ITERATIONS + 1):
        relative = velocity[:, left] - velocity[:, right]
        closing = np.einsum("npi,npi->np", relative, normal)
        slip = np.einsum("npi,npi->np", relative, tangent)
        change_n, change_t = _impulse_changes(jn, jt, closing, slip, mu)
        residual = np.maximum(np.abs(change_n), np.abs(change_t)).max(axis=1)
        if not np.isfinite(residual).all():
            raise ArithmeticError("nonfinite multi-contact residual")
        converged = residual <= speed_tol
        if iteration == MAX_ITERATIONS and iteration > 0:
            for idx in np.flatnonzero(~converged):
                polished = _polish_node(
                    incoming[idx], mass[idx], incidence, normal[idx], tangent[idx],
                    reduced_mass[idx], mu, jn[idx], jt[idx], jn[idx] + change_n[idx],
                    jt[idx] + slip[idx], speed_tol[idx])
                if polished is not None:
                    velocity[idx] = polished
                    converged[idx] = True
        if np.all(converged):
            # Remove common translation before the kinetic-energy check. This
            # avoids cancellation against a large shared transport velocity.
            frame = incoming[:, :1]
            initial_energy = np.sum(mass[:, :, None] * (incoming - frame)**2, axis=(1, 2))
            final_energy = np.sum(mass[:, :, None] * (velocity - frame)**2, axis=(1, 2))
            bound = 1e-11 * initial_energy + mass.sum(axis=1) * speed_tol**2
            if np.any(final_energy > initial_energy + bound):
                raise ArithmeticError("nodal kinetic energy increased")
            return velocity
        if iteration == MAX_ITERATIONS:
            raise ArithmeticError(
                f"multi-contact residual unresolved after {iteration} updates; "
                f"worst unresolved iteration residual / tolerance = "
                f"{np.max((residual / speed_tol)[~converged]):.6g}"
            )
        # A harder independent node in this batch must not change when an
        # already converged node stops updating its accumulated impulses.
        change_n[converged] = 0.
        change_t[converged] = 0.
        jn += relax * change_n
        jt += relax * change_t
        impulse = reduced_mass[:, :, None] * (jn[:, :, None]*normal + jt[:, :, None]*tangent)
        velocity = incoming + (incidence @ impulse) / mass[:, :, None]


def project_contacts(ids, nodes, mass, grad, vel, centers, friction):
    """Update active-field velocities in place only after all nodes succeed."""
    if not np.isfinite(friction) or friction < 0.:
        raise ValueError("invalid contact friction")
    if not len(mass):
        return
    if np.any(mass < 0.) or not np.isfinite(mass).all():
        raise ValueError("invalid field mass")
    active = np.flatnonzero(mass > 1e-14 * mass.max())
    if len(active) < 2:
        return
    # Physical order only fixes floating-point accumulation. Nodes sharing
    # bodies never share nodal velocity or impulse storage.
    positions = centers[ids[active]]
    order = active[np.lexsort((grad[active, 1], grad[active, 0],
                               positions[:, 1], positions[:, 0], nodes[active]))]
    _, starts, counts = np.unique(nodes[order], return_index=True, return_counts=True)
    updates = []
    for k in np.unique(counts[counts >= 2]):
        rows = order[starts[counts == k, None] + np.arange(k)]
        left, right = np.triu_indices(k, k=1)
        if k == 2:
            # Preserve the pinned isolated-pair path, including its orientation.
            swap = ids[rows[:, 0]] > ids[rows[:, 1]]
            rows[swap] = rows[swap, ::-1]
        normal = _normals(rows, left, right, ids, mass, grad, centers)
        if k == 2:
            a, b = rows.T
            va, vb, _, _ = _pair_impulse(mass[a], mass[b], vel[a], vel[b], normal[:, 0], friction)
            result = np.stack((va, vb), axis=1)
        else:
            result = _simultaneous(vel[rows], mass[rows], left, right, normal, friction)
        if not np.isfinite(result).all():
            raise ArithmeticError("nonfinite contact velocity")
        updates.append((rows, result))
    for rows, result in updates:
        vel[rows] = result
