"""Postprocess four archived particle states. No particle or grid evolution runs here."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


LAYER_SOURCES = {
    "flat_patch.py": "636b96e5f5480527e22dba5e93594c8ec33168abd74068a80843996e00fe8229",
    "read_wall_layers.py": "35b7a683d41e38582547a971edaf3385a75955bdf27cd9fe89fc0ed42bb81a0a",
}
COMPONENTS = ("yy", "yx", "stress_MPa")


def load_source(folder, name):
    path = folder / name
    if hashlib.sha256(path.read_bytes()).hexdigest() != LAYER_SOURCES[name]:
        raise ValueError("unrecognized source: " + name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def assert_close(a, b, label):
    if not math.isclose(a, b, abs_tol=1e-12, rel_tol=1e-12):
        raise ValueError(f"{label}: {a} vs {b}")


def saved_masks(records, steps, grid):
    if [r["step"] for r in records] != list(steps):
        raise ValueError("missing, duplicated or unexpected mask step")
    masks = {}
    for row in records:
        keys = row["projection"]["keys"]
        if not keys or any(type(k) is not int or not 0 <= k < 49*(grid+1)**2
                           for k in keys) or keys != sorted(set(keys)):
            raise ValueError("invalid saved mask keys")
        if any(20*(k % (grid+1)) > 3*grid for k in keys):
            raise ValueError("saved mask above the physical floor")
        masks[row["step"]] = keys
    return masks


def geometric_keys(model, state, grid):
    # All 49 particle fields use the same geometric half-space. Keys outside
    # positive spline support carry zero and need not be materialized.
    nodes, weights, _, _ = model.stencil(state["x"], grid)
    field_nodes = state["ids"][:, None] * (grid+1)**2 + nodes
    wall = 20 * (nodes % (grid+1)) <= 3 * grid
    return np.unique(field_nodes[wall & (weights > 0)]).tolist()


def totals(projected, selected):
    yy, yx = (math.fsum(np.asarray(projected[k])[selected]) for k in ("yy", "yx"))
    return dict(yy=yy, yx=yx, stress_MPa=math.fsum((yy, yx)))


def difference(left, right):
    return {k: left[k] - right[k] for k in COMPONENTS}


def corner(model, cross, state, grid, width, keys, ref):
    geometric = geometric_keys(model, state, grid)
    union = sorted(set(geometric).union(keys))
    projected = cross.project_state(model, state, grid, width, union)
    on_saved = np.isin(union, keys)
    on_geometry = np.isin(union, geometric)
    if projected["positive_support_keys"] != len(geometric):
        raise ValueError("positive-support wall set")
    actual = totals(projected, on_saved)
    full = totals(projected, on_geometry)
    omitted = totals(projected, on_geometry & ~on_saved)
    for k in COMPONENTS:
        assert_close(actual[k], ref["values"][k], "archived actual " + k)
        assert_close(full[k], actual[k] + omitted[k], "wall mask partition " + k)
    if (len(keys), int((on_geometry & on_saved).sum())) != (
            ref["requested_keys"], ref["positive_support_keys"]):
        raise ValueError("archived support counts")
    return dict(grid=grid, saved_keys=len(keys),
                saved_supported_keys=int((on_geometry & on_saved).sum()),
                geometric_supported_keys=len(geometric),
                saved=actual, geometric=full, saved_minus_geometric=difference(actual, full))


def decompose(coarse, fine):
    result = {name: difference(coarse[name], fine[name])
              for name in ("saved", "geometric", "saved_minus_geometric")}
    for k in COMPONENTS:
        assert_close(result["saved"][k],
                     result["geometric"][k] + result["saved_minus_geometric"][k],
                     "coarse-minus-fine telescope " + k)
    return result


def analyze(layers_dir, source_root, cross_path, probe_path):
    flat = load_source(layers_dir, "flat_patch.py")
    layers = load_source(layers_dir, "read_wall_layers.py")
    model, cross = flat.load_pinned_sources(source_root)
    if flat.FLOOR != layers.FLOOR or flat.FLOOR != 3/20:
        raise ValueError("floor mismatch")
    with cross_path.open("rb") as raw, layers.fixed_archive(raw, layers.CROSS_SHA) as tar:
        summary = json.loads(layers.payload(tar, "summary.json"))
        states = {n: layers.read_snapshots(tar, n, list(steps)) for n, steps in cross.STEPS.items()}
    with probe_path.open("rb") as raw, layers.fixed_archive(raw, layers.PROBE_SHA) as tar:
        masks = {n: saved_masks(json.loads(layers.payload(tar, f"F{n}/probe.json")), steps, 10*n)
                 for n, steps in cross.STEPS.items()}
    rows = []
    for pair in summary["paired"]:
        pair_steps = dict(zip((8, 16), pair["steps"]))
        references = {(r["source_cells"], r["target_cells"]): r for r in pair["corners"]}
        for n, step in pair_steps.items():
            projections = []
            for target, target_step in pair_steps.items():
                ref = references[n, target]
                if (ref["source_step"], ref["target_step"], ref["status"]) != (step, target_step, "OK"):
                    raise ValueError("unexpected archived corner")
                projected = corner(model, cross, states[n][step], 10*target, layers.WIDTH,
                                   masks[target][target_step], ref)
                projections.append(dict(target_step=target_step, **projected))
            rows.append(dict(source_cells=n, source_step=step, projections=projections,
                             coarse_minus_fine=decompose(*projections)))
    return dict(floor_y=flat.FLOOR, width=layers.WIDTH,
                scope="Fixed archived incoming particle states; signed first lower-wall stress projection in MPa.",
                geometric="All field-nodes with y <= 0.15 on each target grid, independent of momentum sign; this is an algebraic projection.",
                mask_contribution="(saved - geometric) on grid 80 minus (saved - geometric) on grid 160.",
                identities=dict(archives=dict(cross=layers.CROSS_SHA, probe=layers.PROBE_SHA),
                                sources={**LAYER_SOURCES, **flat.SOURCES}),
                rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layers-dir", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--cross", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(analyze(args.layers_dir, args.source_root, args.cross, args.probe),
                        indent=2, allow_nan=False)
    if args.output is None:
        print(result)
    else:
        with args.output.open("x", encoding="utf-8", newline="\n") as output:
            output.write(result + "\n")
