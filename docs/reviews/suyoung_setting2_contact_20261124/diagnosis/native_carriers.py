"""Inspect material attachments in the four initial geometries; no solver advance."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(prefix_root,candidate):
    solver=load(prefix_root / "scripts/suyoung_u6_first_dev.py")
    floor=load(prefix_root / "docs/reviews/suyoung_floor_contact_20261123/material_floor.py")
    candidate=load(candidate)
    rows=[]
    for cells in (8,12,16,24):
        x,ids,vol=solver.seed(cells)
        grid=round(cells/solver.DIAMETER)
        old=floor.disk_boundary(solver,x,ids,cells)
        new=candidate.build_boundary(floor,x,ids,old.positions,old.groups,.5/grid)
        if not np.array_equal(old.groups,new.groups) or not np.array_equal(old.positions,new.positions):
            raise ValueError("seed outline changed")
        all_same_body = bool(np.all(ids[new.indices]==new.groups[:,None]))
        if not all_same_body:
            raise ValueError("carrier crossed physical disk")
        old_distance = np.linalg.norm(old.positions-x[old.owners],axis=1)*grid
        bottom = old.positions[:,1] <= old.positions[:,1].min()+2.e-15
        median_distance = float(np.median(old_distance))
        bottom_distance = old_distance[bottom]
        rows.append(dict(cells=cells, points=len(x), seed_position_sha256=hashlib.sha256(
            x.astype("<f8",copy=False).tobytes()).hexdigest(), all_same_body=all_same_body,
            unchanged_initial_polygons=bool(np.array_equal(old.positions,new.positions)),
            old_median_distance_over_h=median_distance, old_max_distance_over_h=float(old_distance.max()),
            bottom_marker_count=int(bottom.sum()), bottom_owner_distance_over_h=bottom_distance.tolist(),
            bottom_carrier_counts=(new.alpha[bottom]>0).sum(axis=1).tolist(),
            **new.statistics))
    return rows


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("prefix_root", type=Path)
    p.add_argument("candidate", type=Path)
    args=p.parse_args()
    print(json.dumps(run(**vars(args)),allow_nan=False,indent=2))
