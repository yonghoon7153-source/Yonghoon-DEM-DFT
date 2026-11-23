"""Read four fixed incoming states and decompose their bottom wall stress transfer by height."""
import argparse
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import tarfile

import numpy as np


CROSS_SHA = "4bb6fe0cdff8964c6bf02cfbf3f9dd9f7bdec5199cfddce0e3d8160b0dd4f391"
PROBE_SHA = "fcf9fd337d57c77cb9b4f751a6b938ce60a1d9010e438026ac10ffa762104cfd"
STENCIL_SHA = "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4"
FLOOR = 0.15
WIDTH = 0.7024180763115129
EDGES = np.array([0., .5, 1., 1.5, 2., 3.])/160


def require(ok, message):
    if not ok:
        raise ValueError(message)


def layer_index(distance):
    return np.searchsorted(EDGES, distance, side="right")


def point_rows(stencil, state, grid, width, keys):
    nodes, weights, _, offsets = stencil(state["x"], grid)
    masked = np.isin(state["ids"][:, None]*(grid+1)**2 + nodes, np.asarray(keys, dtype=np.int64))
    w = weights * masked
    g = (40.*grid**2/width)*state["volume"][:, None]*w
    geom_y = np.sum(g*offsets[:, :, 1], axis=1)
    geom_x = np.sum(g*offsets[:, :, 0], axis=1)
    return dict(active=np.any(w > 0, axis=1), masked_volume=state["volume"]*np.sum(w, axis=1),
                K=-geom_y, yy_MPa=geom_y*state["yy"], yx_MPa=geom_x*state["yx"])


def reduce_points(points, select):
    select = select & points["active"]
    vk = points["K"][select]
    k, k_abs = math.fsum(vk), math.fsum(np.abs(vk))
    yy = math.fsum(points["yy_MPa"][select])
    yx = math.fsum(points["yx_MPa"][select])
    effective = yy/k if abs(k) > 1e-12*k_abs else None
    return dict(active_points=int(select.sum()), masked_volume=math.fsum(points["masked_volume"][select]),
                K=k, K_abs=k_abs, effective_compression_solver_units=effective,
                yy_MPa=yy, yx_MPa=yx, stress_MPa=math.fsum((yy,yx)))


def match_totals(total, original):
    pairs = (("yy_MPa","yy"), ("yx_MPa","yx"), ("stress_MPa","stress_MPa"))
    for name, reference in pairs:
        require(math.isclose(total[name], original[reference], rel_tol=1e-12, abs_tol=1e-12), "fixed projection: " + name)
    require(math.isclose(total["K"], -original["unit_yy"], rel_tol=1e-12, abs_tol=1e-12), "geometry factor")


def product_split(a, b):
    """Signed symmetric product identity for the aggregate normal component only."""
    ca, cb = (row["effective_compression_solver_units"] for row in (a,b))
    if ca is None or cb is None:
        return None
    ka, kb = a["K"], b["K"]
    return dict(geometry_MPa=(ka-kb)*(ca+cb)/2, effective_compression_MPa=(ka+kb)*(ca-cb)/2,
                yy_difference_MPa=ka*ca-kb*cb)


def fixed_archive(stream, expected):
    require(hashlib.file_digest(stream, "sha256").hexdigest() == expected, "archive identity")
    stream.seek(0)
    return tarfile.open(fileobj=stream, mode="r:gz")


def payload(tar, name):
    member = tar.getmember("run/" + name)
    require(member.isfile(), "regular return member required")
    return tar.extractfile(member).read()


def read_snapshots(tar, n, steps):
    receipt = json.loads(payload(tar, f"F{n}/cross_receipt.json"))
    require(receipt["cells"] == n and receipt["steps"] == steps, "registered steps")
    result = {}
    for step in steps:
        name = f"state_{step}.npz"
        raw = payload(tar, f"F{n}/{name}")
        require(hashlib.sha256(raw).hexdigest() == receipt["files"][name], "snapshot receipt")
        with np.load(io.BytesIO(raw), allow_pickle=False) as archive:
            result[step] = {key: archive[key] for key in ("x","volume","ids","yy","yx")}
    return result


def analyze(cross_file, probe_file, model_file):
    require(hashlib.sha256(model_file.read_bytes()).hexdigest() == STENCIL_SHA, "stencil source")
    spec = importlib.util.spec_from_file_location("fixed_wall_stencil", model_file)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    with cross_file.open("rb") as raw, fixed_archive(raw, CROSS_SHA) as tar:
        reference = json.loads(payload(tar, "summary.json"))
        states = {n:read_snapshots(tar,n,steps) for n,steps in ((8,[269,270]),(16,[538,540]))}
    with probe_file.open("rb") as raw, fixed_archive(raw, PROBE_SHA) as tar:
        masks = {n:{row["step"]:row["projection"]["keys"] for row in json.loads(payload(tar, f"F{n}/probe.json"))}
                 for n in (8,16)}
    samples = []
    for compare in reference["paired"]:
        corners = {}
        for ref in compare["corners"]:
            n, t = ref["source_cells"], ref["target_cells"]
            s, monitor = ref["source_step"], ref["target_step"]
            state = states[n][s]
            points = point_rows(model.stencil, state, 10*t, WIDTH, masks[t][monitor])
            levels = layer_index(state["x"][:,1] - FLOOR)
            cells = [reduce_points(points, levels == k) for k in range(len(EDGES)+1)]
            total = reduce_points(points, np.ones(len(levels), dtype=bool))
            match_totals(total, ref["values"])
            for key in ("active_points","masked_volume","K","K_abs","yy_MPa","yx_MPa","stress_MPa"):
                require(math.isclose(math.fsum(row[key] for row in cells), total[key], rel_tol=1e-12, abs_tol=1e-12),
                        "nonadditive layers: " + key)
            corners[n,t] = dict(source_cells=n, target_cells=t, total=total, layers=cells)
        contrasts = {}
        for name,p,q in (("native",(8,8),(16,16)), ("F8_target",(8,8),(16,8)), ("F16_target",(8,16),(16,16))):
            left,right = corners[p],corners[q]
            diff = [a["stress_MPa"]-b["stress_MPa"] for a,b in zip(left["layers"],right["layers"])]
            contrasts[name] = dict(normal_product_split=product_split(left["total"],right["total"]),
                                   summed_stress_difference_MPa=math.fsum(diff), layer_stress_difference_MPa=diff)
        samples.append(dict(steps=compare["steps"], corners=list(corners.values()), contrasts=contrasts))
    return dict(scope="Development, two incoming snapshot pairs; fixed particle data and target wall masks",
                cross_sha256=CROSS_SHA,probe_sha256=PROBE_SHA,stencil_sha256=STENCIL_SHA,
                layers=dict(origin_y=FLOOR, unit="normalized model length", edge_distance=EDGES.tolist(),
                            boundaries="lower inclusive, upper exclusive; first and last bins open outward"),
                definition="K = -sum(normal geometry coefficient); effective compression = yy_MPa / K",
                samples=samples,stage3_go=False,u6_qualified=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("cross","probe","model","output"):
        parser.add_argument("--"+key, type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.cross, args.probe, args.model)
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(result, out, indent=2, sort_keys=True, allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
