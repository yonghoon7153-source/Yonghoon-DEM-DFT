"""Development-only material-marker projection for the moving upper plate."""
import hashlib
import math
from pathlib import Path
from types import ModuleType

import numpy as np


FLOOR_SHA256 = "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b"


def _isolated_floor(floor_module):
    # The historical advance calls its module-level _other_walls twice. Give this
    # candidate its own namespace for those calls and execute the attested bytes.
    path = Path(floor_module.__file__)
    source = path.read_bytes()
    if hashlib.sha256(source).hexdigest() != FLOOR_SHA256:
        raise ValueError("unrecognized lower-wall source")
    private = ModuleType("suyoung_private_material_floor")
    private.__file__ = str(path)
    exec(compile(source, str(path), "exec"), private.__dict__)
    return private


class MaterialLidAdvance:
    def __init__(self, solver, cells, floor_module, boundary):
        self.solver = solver
        self.cells = cells
        self.floor = _isolated_floor(floor_module)
        self.boundary = boundary
        self.previous_lid = float(solver.LO + solver.WIDTH)
        self.original_walls = self.floor._other_walls
        self.floor._other_walls = self._upper_and_sides
        self.native = self.floor.make_advance(solver, cells, boundary=self)
        self.audit = self.native.audit.copy()
        self.lid_audit = dict(steps=0, lid_passes=0, positive_passes=0,
                              accumulated_downward_impulse=0., max_grid_impulse_error=0.,
                              max_penetration=0., max_clock_error=0.)
        self.last_step = None
        self.failed = False

    @property
    def positions(self):
        return self.boundary.positions

    def bind(self, x, weights, offset, slots, grid, floor, dt):
        # The native step calls this once after P2G. Both walls use precisely the
        # same APIC evaluation at each marker, including potentially negative weights.
        if self.upper is not None or dt != self.dt:
            raise RuntimeError("unexpected material bind")
        lower = self.boundary.bind(x, weights, offset, slots, grid, floor, dt)
        self.upper = self.floor.SurfaceStep(self.boundary, lower.slots, lower.coefficients, floor, dt)
        # For reflected nodal velocities q = -v_y the frictionless inequality
        # y + dt*N*v_y <= lid_end is N*q >= (y - lid_end)/dt.
        self.upper.limit = (self.positions[:, 1] - self.lid) / dt
        native_project = lower.project

        def lower_project(mass, gv):
            if self.mass is not None:
                raise RuntimeError("two lower projections without upper projection")
            self.mass, self.velocity = mass, gv
            impulse = native_project(mass, gv)
            self.floor_impulses.append(impulse)
            return impulse

        lower.project = lower_project
        return lower

    def _upper_and_sides(self, solver, xy, gv, lid):
        if (solver is not self.solver or self.velocity is not gv or self.mass is None
                or lid != self.lid or len(self.impulses) >= 2):
            raise RuntimeError("unexpected upper-wall projection")
        reflected = gv.copy()
        reflected[:, 1] = -gv[:, 1]
        impulse = self.upper.project(self.mass, reflected)
        # Measure the signed change on the physical grid before writing it back.
        signed_delta = float(self.mass @ (-reflected[:, 1] - gv[:, 1]))
        error = abs(signed_delta + impulse)
        scale = max(1., impulse, float(self.mass @ np.abs(gv[:, 1])))
        if not all(map(math.isfinite, (signed_delta, impulse, error))) or impulse < 0. or error > 2.e-12 * scale:
            raise ArithmeticError("upper-wall signed impulse balance")
        if impulse:
            gv[:, 1] = -reflected[:, 1]
        self.impulses.append(float(impulse))
        self.errors.append(error)
        self.mass = self.velocity = None
        # Infinite lid makes the historical upper node mask empty. Its original
        # left and right projections still run after the upper constraint.
        self.original_walls(solver, xy, gv, math.inf)

    def __call__(self, x, v, affine, elastic, ids, volume, grid, dt, lid):
        if self.failed:
            raise RuntimeError("failed development arm cannot resume")
        self.failed = True
        speed = self.solver.WALL_SPEED
        if not all(map(math.isfinite, (dt, lid, speed))) or dt <= 0. or speed <= 0.:
            raise ValueError("invalid moving-wall clock")
        clock_error = abs((self.previous_lid - lid) - dt * speed)
        if clock_error > 64. * np.finfo(float).eps * max(1., abs(self.previous_lid), abs(lid)):
            raise ValueError("previous and prescribed end lid disagree")
        if self.boundary is None:
            self.boundary = self.floor.disk_boundary(self.solver, x, ids, self.cells)
        y = self.positions[:, 1]
        tol = 2.e-12 * max(1., abs(self.solver.LO), abs(lid), abs(self.previous_lid))
        if not np.isfinite(y).all() or y.max() > self.previous_lid + tol or y.min() < self.solver.LO - tol:
            raise ArithmeticError("incoming material surface penetrates a plate")
        top_gap_before = float(lid - y.max())
        self.dt, self.lid = dt, lid
        self.upper = self.mass = self.velocity = None
        self.impulses, self.errors, self.floor_impulses = [], [], []
        result = self.native(x, v, affine, elastic, ids, volume, grid, dt, lid)
        # The native advance transports the single marker set after its second
        # wall pass. Test both inequalities on the resulting physical markers.
        if len(self.impulses) != 2 or len(self.floor_impulses) != 2 or self.mass is not None:
            raise RuntimeError("incomplete two-pass wall projection")
        top_gap_after = float(lid - self.positions[:, 1].max())
        floor_gap_after = float(self.positions[:, 1].min() - self.solver.LO)
        if min(top_gap_after, floor_gap_after) < -tol:
            raise ArithmeticError("transported material surface penetrates a plate")
        downward = math.fsum(self.impulses)
        self.audit.update(self.native.audit)
        audit = self.lid_audit
        audit["steps"] += 1
        audit["lid_passes"] += len(self.impulses)
        audit["positive_passes"] += sum(j > 0. for j in self.impulses)
        audit["accumulated_downward_impulse"] += downward
        audit["max_grid_impulse_error"] = max(audit["max_grid_impulse_error"], *self.errors)
        audit["max_penetration"] = max(audit["max_penetration"], -top_gap_after)
        audit["max_clock_error"] = max(audit["max_clock_error"], clock_error)
        self.last_step = dict(step=audit["steps"], floor_impulse=float(sum(self.floor_impulses)),
                              lid_downward_impulse=downward, lid_signed_impulse=-downward,
                              top_gap_before=top_gap_before, top_gap_after=top_gap_after,
                              floor_gap_after=floor_gap_after, lid_grid_impulse_error=max(self.errors))
        self.previous_lid = lid
        self.failed = False
        return result


def make_advance(solver, cells, *, floor_module, boundary=None):
    return MaterialLidAdvance(solver, cells, floor_module, boundary)
