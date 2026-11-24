"""Read original on/off gap-correction traces. No MPM source is executed."""
import argparse
import csv
import hashlib
import io
import json
import math
import sys
import tarfile
from bisect import bisect_left
from pathlib import Path


PINNED_ARCHIVES = (
    "aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65",
    "c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673",
    "882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af",
)


def require(predicate, detail):
    if not predicate:
        raise ValueError(detail)


def arm(archive, grid, leaf):
    prefix = f"run/F{grid}/"
    record = json.load(archive.extractfile(prefix + leaf))
    raw = archive.extractfile(prefix + "trace.csv").read()
    require(hashlib.sha256(raw).hexdigest() == record["trace_sha256"], "trace hash")
    rows = csv.DictReader(io.StringIO(raw.decode("ascii")))
    heights, times, pressures = [], [], []
    for i, r in enumerate(rows):
        require(int(r["step"]) == i and float(r["time_code"]) == i * record["dt"], "clock")
        heights.append(float(r["height"]))
        times.append(float(r["time_code"]))
        pressures.append(10.0 * float(r["bottom_pressure_E"]))
    require(pressures[-1] >= 1.2 and max(pressures[:-1]) < 1.2, "1.2 MPa cap")
    return record, [heights[0] - h for h in heights], times, pressures


def value(x, knots, values):
    i = bisect_left(knots, x)
    require(i < len(knots) and x >= knots[0], "extrapolation")
    if knots[i] == x:
        return values[i]
    return values[i-1] + (x-knots[i-1]) / (knots[i]-knots[i-1]) * (values[i]-values[i-1])


def geometry(row):
    return row.get("geometry_hashes", row.get("geometry_sha256"))


def audit(files):
    hashes = [hashlib.sha256(f.read_bytes()).hexdigest() for f in files]
    require(tuple(hashes) == PINNED_ARCHIVES, "wrong archive identities")
    old, new = {}, {}
    with tarfile.open(files[0], "r:gz") as f:
        for n in (8, 16):
            old[n] = arm(f, n, "full_receipt.json")
    with tarfile.open(files[1], "r:gz") as f:
        for n in (12, 24):
            old[n] = arm(f, n, "fine_receipt.json")
    with tarfile.open(files[2], "r:gz") as f:
        for n in old:
            new[n] = arm(f, n, "target_receipt.json")
    single = {}
    for n in sorted(old):
        a, u, t, p = old[n]
        b, v, s, q = new[n]
        length = min(len(p), len(q))
        require(u[:length] == v[:length] and t[:length] == s[:length], "same native trajectory times and wall displacement")
        require(geometry(a) is not None and geometry(a) == geometry(b)
                and a["dt"] == b["dt"] and a["floor_sha256"] == b["floor_sha256"]
                and a.get("physics_pin", a.get("base_physics_pin")) == b["base_physics_pin"],
                "changed grid input")
        first = next((i for i in range(length) if p[i] != q[i]), None)
        single[n] = {
            "first_unequal_pressure_step": first,
            "first_positive_pressure_step_s1": next(i for i, v in enumerate(p) if v > 0),
            "first_positive_pressure_step_s2": next(i for i, v in enumerate(q) if v > 0),
            "peak_abs_s2_minus_s1_at_same_u_MPa": max(abs(p[i]-q[i]) for i in range(length)),
        }
    comparisons = {}
    for coarse, fine in [(8, 16), (12, 24)]:
        traces = [matrix[n] for matrix in (old, new) for n in (coarse, fine)]
        most = min(curve[1][-1] for curve in traces)
        knots = sorted({x for curve in traces for x in curve[1] if x <= most})
        def matched(x):
            p1c, p1f, p2c, p2f = (value(x, u, p) for _, u, _, p in traces)
            return dict(u_code=x, s1_coarse=p1c, s1_fine=p1f, s2_coarse=p2c, s2_fine=p2f,
                        s1_gap=p1c-p1f, s2_gap=p2c-p2f, delta_gap=(p2c-p2f)-(p1c-p1f))
        all_rows = [matched(x) for x in knots]
        peak = max(all_rows, key=lambda r:abs(r["s2_gap"]))
        comparisons[f"F{coarse}_F{fine}"] = {
            "four_curve_union_count": len(knots),
            "common_end_u_code": most,
            "s1_max_grid_difference_MPa": max(abs(r["s1_gap"]) for r in all_rows),
            "s2_max_grid_difference_MPa": abs(peak["s2_gap"]),
            "same_u_s2_peak": peak,
            "max_absolute_change_in_grid_difference_MPa": max(abs(r["delta_gap"]) for r in all_rows),
        }
    return dict(status="DEVELOPMENT_ONLY", registered_rule_modified=False, new_simulations=0,
                input_sha256=hashes, same_grid_comparison=single, common_four_curve_window=comparisons)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("setting1_full_pair", type=Path)
    ap.add_argument("setting1_fine_pair", type=Path)
    ap.add_argument("setting2_four_grids", type=Path)
    args = ap.parse_args()
    print(json.dumps(audit([args.setting1_full_pair, args.setting1_fine_pair, args.setting2_four_grids]),
                     indent=2, allow_nan=False))
