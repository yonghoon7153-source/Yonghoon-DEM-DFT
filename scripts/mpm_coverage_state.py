"""Bind a periodic scaffold MPM restart and its DEM geometry to the C(0) measurement grid."""
import argparse
from contextlib import ExitStack
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import numpy as np

if __name__ == "__main__" and sys.flags.isolated:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from mpm_coverage_c0 import compare, seed_counts


def grid_shape(n_grid, nz):
    if type(n_grid) is not int or type(nz) is not int or min(n_grid, nz) < 1:
        raise ValueError("require positive integer n_grid and nz")
    origin = round(.04 * n_grid)
    width = round((.96 - .04) * n_grid)
    if width < 1 or origin + width > n_grid:
        raise ValueError("invalid periodic crop")
    return origin, (width, width, nz)


def cell_numbers(xyz, n_grid, nz):
    """Map native box coordinates to flattened xyz cells in the snapped periodic crop."""
    origin, shape = grid_shape(n_grid, nz)
    xyz = np.asarray(xyz)
    if xyz.ndim != 2 or xyz.shape[1] != 3 or xyz.dtype.kind != "f":
        raise ValueError("expected floating point (n,3) box coordinates")
    if not np.isfinite(xyz).all():
        raise ValueError("nonfinite point coordinate")
    # Promote the stored coordinates before flooring so multiplication never
    # rounds a just-below-face position onto the other side in float32.
    cells = np.floor(xyz.astype(np.float64, copy=False) * n_grid)
    if np.any(np.abs(cells) >= 2**62) or np.any((cells[:,2] < 0) | (cells[:,2] >= nz)):
        raise ValueError("point outside vertical grid or integer range")
    cells = cells.astype(np.int64)
    cells[:,:2] = (cells[:,:2] - origin) % shape[0]
    return np.ravel_multi_index(cells.T, shape)


def spheres(rows, kinds, scale, floor, stretch):
    rows = np.asarray(rows)
    if (rows.ndim != 2 or rows.shape[1] != 5 or rows.dtype.kind not in "fiu"
            or not np.isfinite(rows).all() or not np.isin(rows[:,0],kinds).all()
            or np.any(rows[:,4] <= 0)):
        raise ValueError("invalid type,x,y,z,r scaffold")
    rows = rows.astype(np.float64, copy=False)
    result = np.empty((len(rows),4),dtype=np.float64)
    result[:,:2] = .04 + rows[:,1:3]*scale
    result[:,2] = floor + rows[:,3]*scale*stretch
    result[:,3] = rows[:,4]*scale
    return result


def am_grid(xyzr, types, n_grid, origin, shape):
    """Reproduce the writer's last-row priority where different AM phases overlap."""
    empty = np.zeros(shape, dtype=np.uint8)
    first, second = (seed_counts(empty, xyzr[types == phase], n_grid, origin) != 0
                     for phase in (1, 2))
    grid = first.astype(np.uint8)
    grid[second] = 2
    overlap = np.argwhere(first & second)
    if len(overlap):
        # Overlap indices are ordered by x; limit each sphere to its x columns.
        width = shape[0]
        x_offsets = np.searchsorted(overlap[:, 0], np.arange(width + 1))
        for (cx, cy, cz, radius), phase in zip(xyzr, types):
            left = math.floor((cx - radius) * n_grid)
            right = math.ceil((cx + radius) * n_grid)
            columns = (np.arange(left, right) - origin) % width if right-left < width else range(width)
            for column in columns:
                ijk = overlap[x_offsets[column]:x_offsets[column+1]]
                if not len(ijk):
                    continue
                xy = ijk[:, :2].astype(np.float64) + origin + .5
                center = np.array([cx, cy])
                xy += width * np.rint((center * n_grid - xy) / width)
                delta = xy / n_grid - center
                dz = (ijk[:,2] + .5) / n_grid - cz
                hit = delta[:,0]**2 + delta[:,1]**2 + dz**2 <= radius**2
                grid[tuple(ijk[hit].T)] = phase
    return grid


def state_grids(state, am_rows, se_rows):
    """Native mpm3d_state_v1 pristine scaffold case, with separate original AM/SE rows."""
    text = np.asarray(state["meta_json"])
    if text.shape != () or text.dtype.kind != "U":
        raise ValueError("expected a scalar JSON string")
    meta = json.loads(text.item())
    if (meta["schema"] != "mpm3d_state_v1" or meta["periodic"] is not True
            or meta["am_scaffold"] is not True or meta["se_dump"] is not True
            or meta["am_radii_deformed"] is not False or meta["FLOOR"] != .05):
        raise ValueError("expected an undeformed periodic DEM scaffold frame")
    n_grid, nz = meta["n_grid"], meta["nz"]
    origin, shape = grid_shape(n_grid, nz)
    lateral = meta["lateral_box"]
    stretch = meta["dilate_z"]
    if any(type(v) not in (float,int) or not math.isfinite(v) or v<=0 for v in (lateral,stretch)):
        raise ValueError("invalid scaffold transform")
    scale = (.96 - .04)/lateral
    um_box = 1000./scale
    if meta["um_box_um"] != um_box:
        raise ValueError("state length scale differs from scaffold transform")
    xyzr = spheres(am_rows,(1,2),scale,.05,max(stretch,1.))
    if (meta["n_am"] != len(xyzr)
            or not np.array_equal(state["am_pos"],xyzr[:,:3])
            or not np.array_equal(state["am_r_pristine"],xyzr[:,3])
            or not np.array_equal(state["am_r_applied"],xyzr[:,3])):
        raise ValueError("AM centers, radii or row order differ from the source")
    se = spheres(se_rows,(3,),scale,.05,max(stretch,1.))

    am = am_grid(xyzr, np.asarray(am_rows)[:,0], n_grid, origin, shape)
    seed = seed_counts(am, se, n_grid, origin)

    xyz, phase = np.asarray(state["x"]), np.asarray(state["phase"])
    if (xyz.shape != (meta["n_pts"],3) or xyz.dtype.kind != "f"
            or phase.shape != (len(xyz),) or phase.dtype.kind not in "iu"
            or not np.isin(phase,(1,2,3,4,5,6)).all()):
        raise ValueError("invalid native scaffold point/phase layout")
    end = np.zeros(shape,dtype=np.int64)
    for start in range(0,len(xyz),262144):
        sl = slice(start,start+262144)
        cells = cell_numbers(xyz[sl][phase[sl]==1],n_grid,nz)
        np.add.at(end.ravel(),cells,1)
    if int(end.sum()) != int(seed.sum()):
        raise ValueError("SE count differs from eight points per reconstructed seed cell")
    return am, seed, end, um_box/n_grid


def identifiers(values, name):
    a = np.asarray(values)
    if a.ndim != 1 or a.dtype.kind not in "iu" or np.any(a < 0) or np.any(a > np.iinfo(np.int64).max):
        raise ValueError(name+" requires nonnegative, exact signed-64 representable integers")
    return a.astype(np.int64,copy=False)


def transport_owners(seed_keys, seed_atom_ids, final_keys, final_xyz, canonical_ranks, n_grid, nz):
    """Vote in occupied SE cells using caller-supplied stable point keys and certified DEM IDs."""
    sk = identifiers(seed_keys,"seed point keys")
    fk = identifiers(final_keys,"final point keys")
    atom = identifiers(seed_atom_ids,"DEM atom IDs")
    if len(sk)!=len(atom) or len(fk)!=len(final_xyz) or np.any(atom==0):
        raise ValueError("inconsistent point or DEM identity")
    order = np.argsort(sk)
    sorted_keys = sk[order]
    if np.any(sorted_keys[1:]==sorted_keys[:-1]) or not np.array_equal(sorted_keys,np.sort(fk)):
        raise ValueError("point lineage requires the same distinct key set at both stages")
    atom_final = atom[order[np.searchsorted(sorted_keys,fk)]]
    cells = cell_numbers(final_xyz,n_grid,nz)
    _,shape=grid_shape(n_grid,nz)
    out = np.full(shape,-1,dtype=np.int64)
    if not isinstance(canonical_ranks,dict) or any(
        not isinstance(i,(int,np.integer)) or isinstance(i,bool) or int(i)<=0
        or not isinstance(v,(int,np.integer)) or isinstance(v,bool) or not 0<=int(v)<=np.iinfo(np.int64).max
        for i,v in canonical_ranks.items()
    ):
        raise ValueError("invalid external canonical ranks")
    id_order = np.unique(atom)
    if set(canonical_ranks)!=set(id_order) or len(set(canonical_ranks.values()))!=len(id_order):
        raise ValueError("every represented atom requires a distinct canonical rank")
    if not len(cells):
        return out
    ix = np.lexsort((atom_final,cells))
    cells, owners = cells[ix],atom_final[ix]
    groups = np.flatnonzero(np.r_[True,(cells[1:]!=cells[:-1]) | (owners[1:]!=owners[:-1])])
    votes = np.diff(np.r_[groups,len(cells)])
    cells, owners = cells[groups],owners[groups]
    ranks = np.array([canonical_ranks[k] for k in id_order],dtype=np.int64)[np.searchsorted(id_order,owners)]
    ix = np.lexsort((ranks,-votes,cells))
    cells,owners,votes = cells[ix],owners[ix],votes[ix]
    first = np.flatnonzero(np.r_[True,cells[1:]!=cells[:-1]])
    keep = first[np.add.reduceat(votes,first)>=4]
    out.ravel()[cells[keep]]=owners[keep]
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for role in ("state","am_scaffold","se_scaffold","source_receipt"):
        parser.add_argument(role,type=Path)
    args = parser.parse_args(argv)
    roles = ("state","am_scaffold","se_scaffold")
    try:
        receipt = json.loads(args.source_receipt.read_text(encoding="utf-8"))
        if set(receipt)!=set(roles):
            raise ValueError("receipt must identify all three source roles")
        with ExitStack() as stack:
            streams={}
            for role in roles:
                f=stack.enter_context(getattr(args,role).open("rb"))
                sha=hashlib.sha256()
                for chunk in iter(lambda:f.read(1024*1024),b""):
                    sha.update(chunk)
                if not isinstance(receipt[role],str) or not re.fullmatch("[0-9a-f]{64}",receipt[role]) or sha.hexdigest()!=receipt[role]:
                    raise ValueError("source SHA256 mismatch for "+role)
                f.seek(0)
                streams[role]=f
            state=stack.enter_context(np.load(streams["state"],allow_pickle=False))
            am,se=(np.loadtxt(streams[k],delimiter=",",ndmin=2) for k in roles[1:])
            grid,seed,end,h=state_grids(state,am,se)
            result=compare(grid,seed,end,h,[None,None])
    except (KeyError,TypeError,ValueError,OSError,IndexError) as exc:
        parser.exit(2,"coverage input: "+str(exc)+"\n")
    output = {
        "source_sha256": receipt,
        "execution_source_identity": "NOT_ESTABLISHED",
        "coverage_source_scope": "CONDITIONAL_ON_EXTERNAL_RUN_BINDING",
        "se_point_identity": "UNESTABLISHED",
        "coverage": result,
    }
    print(json.dumps(output, allow_nan=False, sort_keys=True))


if __name__ == "__main__":
    main()
