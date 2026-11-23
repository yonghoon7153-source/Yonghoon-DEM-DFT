"""Material-surface, frictionless lower wall for the 2D U6 development solver."""
import math

import numpy as np


DISK_BOUNDARY_VERTICES = 256
EPS = np.finfo(float).eps


class MaterialBoundary:
    """Surface vertices attached to the kinematic affine maps of their material points."""

    def __init__(self, owners, positions, groups=None):
        self.owners = np.asarray(owners, dtype=int).copy()
        self.positions = np.array(positions, dtype=float, copy=True)
        self.groups = np.zeros(len(self.owners), dtype=int) if groups is None else np.asarray(groups).copy()
        if (self.positions.shape != (len(self.owners), 2) or self.groups.shape != self.owners.shape
                or not len(self.owners) or np.any(self.owners < 0) or not np.isfinite(self.positions).all()):
            raise ValueError("invalid material surface")

    def bind(self, x, weights, offset, slots, grid, floor, dt):
        # G2P gives v_p=sum(w_i v_i) and C_p=4/h² sum(w_i v_i r_i^T).
        # A material offset r advances by (I+dt C_p)r, independently of plastic return.
        rel = self.positions - x[self.owners]
        factor = 1. + (4.*grid**2)*np.einsum("sqi,si->sq", offset[self.owners], rel)
        coefficients = weights[self.owners] * factor
        if not np.isfinite(coefficients).all() or dt <= 0:
            raise ArithmeticError("invalid material kinematics")
        return SurfaceStep(self, slots[self.owners], coefficients, floor, dt)


def disk_boundary(solver, x, ids, cells):
    """Seed the prescribed circles independently of the occupied grid or outermost points."""
    if cells not in (8, 12, 16, 24) or not np.array_equal(np.unique(ids), np.arange(49)):
        raise ValueError("expected original 49-disk F fields")
    theta = 2.*np.pi*np.arange(DISK_BOUNDARY_VERTICES)/DISK_BOUNDARY_VERTICES
    circle = solver.DIAMETER*.5*np.column_stack((np.cos(theta), np.sin(theta)))
    positions, owners = [], []
    for body in range(49):
        center = solver.LO + (np.array(divmod(body, 7)) + .5)*(solver.WIDTH/7)
        surface = center + circle
        idx = np.flatnonzero(ids == body)
        # Only the attachment is discretized. It stays fixed for this material vertex's lifetime.
        delta = surface[:, None, :] - x[idx][None, :, :]
        closest = np.argmin(np.einsum("sqi,sqi->sq", delta, delta), axis=1)
        positions.append(surface)
        owners.append(idx[closest])
    owners = np.concatenate(owners)
    return MaterialBoundary(owners, np.concatenate(positions), ids[owners])


def _minimum_norm(H, d, initial):
    """Feasible active-set solve: min |z|²/2 subject to normalized rows H z >= d."""
    z = initial.copy()
    active = []
    eps = 64.*EPS
    for _ in range(16*(len(d) + 1) + 100):
        if active:
            A = H[active]
            # Minimum-norm displacement meeting the active, physically positioned surfaces.
            star = np.linalg.lstsq(A, d[active], rcond=None)[0]
        else:
            star = np.zeros_like(z)
        direction = star - z
        slack = H @ z - d
        change = H @ direction
        allowed = np.ones(len(d), dtype=bool)
        allowed[active] = False
        tol = eps*max(1.e-12, np.linalg.norm(z), np.linalg.norm(star), np.max(np.abs(d)))
        blocking = allowed & (change < -tol) & (slack + change < -tol)
        if blocking.any():
            candidates = np.flatnonzero(blocking)
            fraction = np.maximum(slack[candidates], 0.) / -change[candidates]
            k = np.argmin(fraction)
            z += min(1., fraction[k])*direction
            active.append(int(candidates[k]))
            continue
        z = star
        if not active:
            return z, np.zeros(len(d))
        multipliers = np.linalg.lstsq(A.T, z, rcond=None)[0]
        worst = int(np.argmin(multipliers))
        if multipliers[worst] >= -tol:
            impulses = np.zeros(len(d))
            impulses[active] = np.maximum(multipliers, 0.)
            return z, impulses
        active.pop(worst)
    raise ArithmeticError("lower wall active-set iteration limit")


def _project_rows(slots, coefficients, mass, before, limit):
    indices, col = np.unique(slots, return_inverse=True)
    col = col.reshape(coefficients.shape)
    N = np.zeros((len(limit), len(indices)))
    np.add.at(N, (np.arange(len(limit))[:, None], col), coefficients)
    if np.any(N[:, mass[indices] == 0.] != 0.):
        raise ArithmeticError("nonzero surface weight at a massless node")
    occupied = mass[indices] > 0.
    indices, N = indices[occupied], N[:, occupied]
    sqrt_m = np.sqrt(mass[indices])
    H = N / sqrt_m
    norms = np.linalg.norm(H, axis=1)
    required = limit - N @ before[indices]
    # Constant upward velocity is feasible because each G2P/affine row sums to one.
    initial = sqrt_m*(max(0., np.max(required)) + 64*EPS*max(1., np.max(np.abs(required))))
    _, normalized_impulse = _minimum_norm(H / norms[:, None], required / norms, initial)
    impulse = normalized_impulse / norms
    return indices, (N.T @ impulse)/mass[indices], float(impulse.sum())


class SurfaceStep:
    def __init__(self, boundary, slots, coefficients, floor, dt):
        self.boundary, self.slots, self.coefficients = boundary, slots, coefficients
        self.dt = dt
        # Only enough approach to close an existing physical gap is allowed this step.
        self.limit = -np.maximum(boundary.positions[:, 1] - floor, 0.)/dt
        self.last_grid_error = 0.
        self.last_speed_violation = 0.

    def project(self, mass, gv):
        original = gv[:, 1].copy()
        normal = np.einsum("sq,sq->s", self.coefficients, original[self.slots])
        tol = 256.*EPS*max(1., np.max(np.abs(original)))
        violated = normal < self.limit - tol
        total = 0.
        for group in np.unique(self.boundary.groups[violated]):
            rows = np.flatnonzero(self.boundary.groups == group)
            selected = violated[rows].copy()
            # Enlarge the patch if coupling at shared field nodes would close another gap.
            for _ in range(len(rows) + 1):
                subset = rows[selected]
                index, dv, impulse = _project_rows(self.slots[subset], self.coefficients[subset],
                                                   mass, original, self.limit[subset])
                gv[index, 1] = original[index] + dv
                u = np.einsum("sq,sq->s", self.coefficients[rows], gv[self.slots[rows], 1])
                missed = (u < self.limit[rows] - tol) & ~selected
                if not missed.any():
                    if np.any(u < self.limit[rows] - 8.*tol):
                        raise ArithmeticError("lower material surface still approaches through plate")
                    total += impulse
                    break
                selected |= missed
            else:
                raise ArithmeticError("material contact set did not close")
        after = gv[:, 1]
        error = abs(float(mass @ (after-original)) - total)
        scale = max(1., float(mass @ np.abs(original)), float(mass @ np.abs(after)), total)
        if not np.isfinite(after).all() or not math.isfinite(total) or error > 2.e-12*scale:
            raise ArithmeticError("lower wall impulse balance")
        self.last_grid_error = error
        new_normal = np.einsum("sq,sq->s", self.coefficients, after[self.slots])
        self.last_speed_violation = max(0., float(np.max(self.limit - new_normal)))
        return total

    def transport(self, gv):
        material_velocity = np.einsum("sq,sqi->si", self.coefficients, gv[self.slots])
        self.boundary.positions += self.dt*material_velocity
        if not np.isfinite(self.boundary.positions).all():
            raise ArithmeticError("nonfinite material boundary")


def _other_walls(solver, xy, gv, lid):
    # Preserve the pinned upper and side velocity projections and order.
    top = (xy[:, 1] >= lid) & (gv[:, 1] > -solver.WALL_SPEED)
    gv[top, 1] = -solver.WALL_SPEED
    gv[(xy[:, 0] <= solver.LO) & (gv[:, 0] < 0), 0] = 0.
    gv[(xy[:, 0] >= solver.LO + solver.WIDTH) & (gv[:, 0] > 0), 0] = 0.


class CandidateAdvance:
    def __init__(self, solver, cells, boundary=None):
        self.solver, self.cells, self.boundary = solver, cells, boundary
        self.audit = dict(steps=0, floor_passes=0, positive_passes=0, accumulated_impulse=0.,
                          max_grid_impulse_error=0., max_g2p_momentum_error=0., max_penetration=0.,
                          disk_boundary_vertices=DISK_BOUNDARY_VERTICES)

    def __call__(self, x, v, affine, elastic, ids, volume, grid, dt, lid):
        s = self.solver
        if self.boundary is None:
            self.boundary = disk_boundary(s, x, ids, self.cells)
        nodes, weights, gradient, offset = s.model.stencil(x, grid)
        nn = (grid + 1)**2
        key, slots = np.unique((ids[:, None]*nn + nodes).ravel(), return_inverse=True)
        slots = slots.reshape(weights.shape)
        wm = volume[:, None]*weights
        transfer = volume[:, None, None]*(affine - dt*4*grid**2*s.model.stress(elastic))
        momentum = wm[:, :, None]*v[:, None, :] + weights[:, :, None]*np.einsum(
            "pij,pqj->pqi", transfer, offset)
        flat = slots.ravel()
        def collect(a):
            return np.bincount(flat, weights=a.ravel(), minlength=len(key))
        mass = collect(wm)
        if abs(float(mass.sum()) - float(volume.sum())) > 1.e-12:
            raise ArithmeticError("mass mismatch")
        mom = np.column_stack([collect(momentum[:, :, k]) for k in range(2)])
        grad = np.column_stack([collect(-volume[:, None]*gradient[:, :, k]) for k in range(2)])
        gv = np.divide(mom, mass[:, None], out=np.zeros_like(mom), where=mass[:, None] > 0.)
        node = key % nn
        xy = np.column_stack(np.divmod(node, grid + 1)) / grid
        wall = self.boundary.bind(x, weights, offset, slots, grid, s.LO, dt)
        impulses, errors = [], []
        def walls():
            impulses.append(wall.project(mass, gv))
            errors.append(wall.last_grid_error)
            _other_walls(s, xy, gv, lid)
        walls()
        count = np.bincount(ids)
        centers = np.column_stack([np.bincount(ids, weights=x[:, k])/count for k in range(2)])
        s.project_contacts(key // nn, node, mass, grad, gv, centers, .5)
        walls()
        velocity = gv[slots]
        v = np.einsum("pq,pqi->pi", weights, velocity)
        affine = 4*grid**2*np.einsum("pq,pqi,pqj->pij", weights, velocity, offset)
        x = x + dt*v
        elastic = s.model.plastic_project((np.eye(2) + dt*affine) @ elastic)
        bottom = sum(impulses)
        pressure = bottom/(dt*s.WIDTH)
        err = abs(float(volume @ v[:, 1]) - float(mass @ gv[:, 1]))
        if (not math.isfinite(pressure) or not np.isfinite(x).all()
                or err > 2.e-12*max(1., float(mass @ np.abs(gv[:, 1])), bottom)):
            raise ArithmeticError("nonfinite state or G2P momentum mismatch")
        wall.transport(gv)
        penetration = max(0., float(s.LO - self.boundary.positions[:, 1].min()))
        if penetration > 2.e-12*max(1., abs(s.LO)):
            raise ArithmeticError("transported material boundary penetrated the lower plate")
        self.audit["steps"] += 1
        self.audit["floor_passes"] += 2
        self.audit["positive_passes"] += sum(j > 0 for j in impulses)
        self.audit["accumulated_impulse"] += bottom
        self.audit["max_grid_impulse_error"] = max(self.audit["max_grid_impulse_error"], *errors)
        self.audit["max_g2p_momentum_error"] = max(self.audit["max_g2p_momentum_error"], err)
        self.audit["max_penetration"] = max(self.audit["max_penetration"], penetration)
        return x, v, affine, elastic, pressure


def make_advance(solver, cells, *, boundary=None):
    return CandidateAdvance(solver, cells, boundary)
