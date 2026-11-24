"""Use same-body reference-space carrier weights for a transported material boundary."""
from pathlib import Path
import hashlib

import numpy as np


ORIGINAL_FLOOR_SHA256 = "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b"
POLICY = "reference_quadratic_bspline_same_body_material_carriers_v1"


def _basis(u):
    a = np.abs(u)
    return np.where(a <= .5, .75 - a*a, .5*np.maximum(1.5-a,0.)**2)


def build_boundary(original_floor_module, x, ids, positions, groups, pitch):
    x = np.asarray(x, dtype=float)
    ids = np.asarray(ids)
    positions = np.asarray(positions, dtype=float)
    groups = np.asarray(groups)
    if (x.shape != (len(ids),2) or positions.shape != (len(groups),2) or not len(groups)
            or not np.isfinite(x).all() or not np.isfinite(positions).all()
            or not np.isfinite(pitch) or pitch <= 0. or ids.dtype.kind not in "iu"
            or groups.dtype.kind not in "iu"):
        raise ValueError("invalid reference carriers")
    carrier_rows = [None]*len(positions)
    weight_rows = [None]*len(positions)
    owners = np.empty(len(positions),dtype=int)
    near_ties = 0
    for group in np.unique(groups):
        points = np.flatnonzero(ids == group)
        if not len(points):
            raise ValueError("missing same-body carriers")
        # The sums follow reference geometry even after a permutation of the input table.
        points = points[np.lexsort((x[points,1],x[points,0]))]
        points_x = x[points]
        for idx in np.flatnonzero(groups == group):
            distance = (positions[idx] - points_x)/pitch
            # Compact tensor-product support in the initial (material) configuration.
            inside = np.all(np.abs(distance) < 1.5, axis=1)
            candidates = points[inside]
            dr = distance[inside]
            if not len(candidates):
                raise ValueError("material surface outside reference carrier support")
            coeff = np.prod(_basis(dr), axis=1)
            keep = coeff > 0.
            candidates, dr, coeff = candidates[keep], dr[keep], coeff[keep]
            if not len(candidates):
                raise ValueError("absent positive reference weight")
            carrier_rows[idx] = candidates
            weight_rows[idx] = coeff / coeff.sum()
            norm2 = np.einsum("pi,pi->p", dr, dr)
            first = int(np.argmin(norm2))
            owners[idx] = candidates[first]   # Representative for metadata; transfer uses the blend.
            near_ties += int(np.sum(np.abs(norm2-norm2[first]) <= 64*np.finfo(float).eps) > 1)
    counts = np.array([len(row) for row in carrier_rows])
    width = int(counts.max())
    all_ids = np.repeat(owners[:,None],width,axis=1)
    alpha = np.zeros((len(positions),width))
    for idx,(row,weights) in enumerate(zip(carrier_rows,weight_rows)):
        all_ids[idx,:len(row)] = row
        alpha[idx,:len(row)] = weights
    if not np.allclose(alpha.sum(axis=1),1.,rtol=0,atol=5e-15):
        raise ArithmeticError("reference partition of unity")
    base = original_floor_module.MaterialBoundary(owners, positions, groups)
    return CarrierBoundary(original_floor_module,base,all_ids,alpha,counts,near_ties,pitch)


class CarrierBoundary:
    def __init__(self, original_floor_module, base, indices, alpha, counts, near_ties, pitch):
        self.floor = original_floor_module
        self.owners = base.owners
        self.positions = base.positions
        self.groups = base.groups
        self.indices = indices
        self.alpha = alpha
        self.statistics = dict(policy=POLICY, vertices=len(counts), pitch=float(pitch),
                               nearest_ties_64eps=int(near_ties),
                               carriers_histogram={str(k):int(np.sum(counts==k)) for k in np.unique(counts)},
                               partition_error=float(np.max(np.abs(alpha.sum(axis=1)-1.))))

    def bind(self,x,weights,offset,slots,grid,floor,dt):
        # Reconstruct each material vertex velocity from each carrier's APIC map.
        # Exactly this weighted row also acts by its transpose in the original mass-metric projector.
        rel = self.positions[:,None,:] - x[self.indices]
        factor = 1. + 4*grid**2*np.einsum("skqi,ski->skq",offset[self.indices],rel)
        rows = (self.alpha[:,:,None]*weights[self.indices])*factor
        slot_rows = slots[self.indices].reshape(len(rows),-1)
        coeff = rows.reshape(slot_rows.shape)
        if not np.isfinite(coeff).all() or not np.isfinite(dt) or dt <= 0.:
            raise ArithmeticError("invalid blended surface kinematics")
        return self.floor.SurfaceStep(self,slot_rows,coeff,floor,dt)


class CarrierAdvance:
    def __init__(self,floor,solver,cells):
        if cells not in (8,12,16,24):
            raise ValueError("unsupported development grid")
        self.floor, self.solver, self.cells = floor, solver, cells
        self.native = floor.make_advance(solver,cells)

    @property
    def audit(self):
        return self.native.audit

    @property
    def boundary(self):
        return self.native.boundary

    def __call__(self,x,v,affine,elastic,ids,volume,grid,dt,lid):
        if self.boundary is None:
            seed = self.floor.disk_boundary(self.solver,x,ids,self.cells)
            if grid != round(self.cells/self.solver.DIAMETER):
                raise ValueError("native grid mismatch")
            self.native.boundary = build_boundary(self.floor,x,ids,seed.positions,seed.groups,.5/grid)
            self.audit["carrier"] = self.boundary.statistics
        return self.native(x,v,affine,elastic,ids,volume,grid,dt,lid)


def make_advance(original_floor_module, solver, cells):
    if hashlib.sha256(Path(original_floor_module.__file__).read_bytes()).hexdigest() != ORIGINAL_FLOOR_SHA256:
        raise ValueError("pinned material-floor implementation required")
    return CarrierAdvance(original_floor_module,solver,cells)
