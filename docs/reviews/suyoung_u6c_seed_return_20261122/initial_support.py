"""Project the undeformed native F16 seed to two grids without advancing either."""
import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import io
import itertools
import json
import math
from pathlib import Path
import tarfile

import numpy as np


SOURCES = {"suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
           "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4"}
SEED = {"positions": "ce12e262721141b2c4fc36cc72733686055a9e22ce62a8cc733a1e2ad591858a",
        "ids": "da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
        "volume": "06f4c3ce49ffece1d401bdcae453605728c4ba0e7731b4c2c6027e337cdc88b4"}
WALL_TAR = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"


def require(value, message):
    if not value:
        raise ValueError(message)


def contacts(ids, nodes, mass, centers, diameter, grid):
    # Native project_contacts applies this strict field-node mass cutoff.
    active = np.flatnonzero(mass > 1.e-14 * mass.max())
    order = active[np.lexsort((ids[active], nodes[active]))]
    shared = dense = 0
    observations = Counter()
    for _, group in itertools.groupby(order, key=lambda i: nodes[i]):
        fields = [int(ids[i]) for i in group]
        if len(fields) >= 2:
            shared += 1
            dense += int(len(fields) >= 3)
            observations.update(itertools.combinations(fields, 2))
    gaps = [float(np.linalg.norm(centers[a] - centers[b])) - diameter for a,b in observations]
    oblique = sum(bool(np.all(centers[a] != centers[b])) for a,b in observations)
    entries = sum(observations.values())
    return {"shared_nodes": shared, "at_least_three_fields_nodes": dense,
            "unique_candidate_pairs": len(gaps), "axis_aligned_center_pairs": len(gaps)-oblique,
            "oblique_center_pairs": oblique, "positive_geometric_gap_pairs": sum(g > 0. for g in gaps),
            "smallest_candidate_geometric_gap": min(gaps, default=None),
            "largest_candidate_geometric_gap": max(gaps, default=None),
            "candidate_pair_node_entries": entries, "candidate_pair_node_entries_times_dx_squared": entries / grid**2}


def project(model, grid, seed, dt, centers):
    x, ids, vol = seed
    nodes, weights, _, _ = model.model.stencil(x, grid)
    nn = (grid + 1)**2
    keys, slots = np.unique((ids[:,None] * nn + nodes).ravel(), return_inverse=True)
    mass = np.bincount(slots.ravel(), weights=(vol[:,None]*weights).ravel(), minlength=len(keys))
    total = float(np.sum(mass))
    require(abs(total - 49 * math.pi * (model.DIAMETER/2)**2) <= 1.e-12, "AREA_MISMATCH")
    fields, node = np.divmod(keys, nn)
    y = (node % (grid+1)) / grid
    # The first moving-lid evaluation in the fixed driver uses this exact schedule.
    lid = model.LO + (model.WIDTH - dt*model.WALL_SPEED)
    top = y >= lid
    bottom = y <= model.LO
    top_mass = float(np.sum(mass[top]))
    return {"grid_cells_per_axis": grid, "material_volume": total,
            "top_start_node_y": math.ceil(lid * grid)/grid, "first_step_lid":lid,
            "upper_supported_mass": top_mass, "lower_supported_mass":float(np.sum(mass[bottom])),
            "expected_first_top_pre_impulse":top_mass * model.WALL_SPEED,
            "candidate_support": contacts(fields,node,mass,centers,model.DIAMETER,grid)}


def read(source_dir, wall_tar):
    for name, digest in SOURCES.items():
        require(hashlib.sha256((source_dir/name).read_bytes()).hexdigest() == digest, "SOURCE_HASH")
    spec = importlib.util.spec_from_file_location("native_initial_support", source_dir/"suyoung_u6_first_dev.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    seed = native.seed(16)
    hashes = {key: hashlib.sha256(arr.astype(typ,copy=False).tobytes(order="C")).hexdigest()
              for key,arr,typ in zip(SEED,seed,("<f8","<i8","<f8"),strict=True)}
    require(hashes == SEED and len(seed[0]) == 39053, "INITIAL_GEOMETRY")
    centers = np.array([(native.LO+(i+.5)*native.WIDTH/7, native.LO+(j+.5)*native.WIDTH/7)
                        for i in range(7) for j in range(7)])
    dt = .35/(160*math.sqrt(native.model.LAM + 2*native.model.MU))
    report = {"development_only": True, "seed_sha256":hashes,"dt":dt,
              "method":"initial_mass_scatter_no_time_steps", "arms":{
                  f"F{cells}": project(native,10*cells,seed,dt,centers) for cells in (8,16)}}
    raw = wall_tar.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==WALL_TAR, "WALL_RETURN_HASH")
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as archive:
        data=archive.extractfile("run/arms/F16/wall.csv").read()
    first=next(csv.DictReader(io.StringIO(data.decode("ascii"),newline="")))
    actual=float(first["top_J_down_pre"])
    expected=report["arms"]["F16"]["expected_first_top_pre_impulse"]
    require(int(first["step"])==1 and float(first["lid_code"])==report["arms"]["F16"]["first_step_lid"]
            and math.isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-18), "NATIVE_FIRST_TOP_IMPULSE")
    report["F16_first_step_witness"]={"wall_archive_sha256":WALL_TAR,"actual_first_top_pre_impulse":actual,
                                      "absolute_error":abs(actual-expected)}
    return report


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir",type=Path,required=True)
    parser.add_argument("--wall",type=Path,required=True)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    text=json.dumps(read(args.source_dir,args.wall),sort_keys=True,indent=2,allow_nan=False)+"\n"
    if args.out:
        with args.out.open("x",encoding="ascii",newline="\n") as target:
            target.write(text)
    else:
        print(text,end="")
