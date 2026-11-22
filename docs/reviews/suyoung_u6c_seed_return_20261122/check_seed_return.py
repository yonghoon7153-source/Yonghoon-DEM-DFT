"""Recompute signed contrasts from four hash-bound pressure traces, without a solver."""

import argparse
from bisect import bisect_left
import csv
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


WALL = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
HALF = "e574396d010514b3cd77f57d2e06d0c25227c88a7b6e985577f2981aa8c154e4"
DENSE = "96205a44f9bf5eaa4439a536d4044570337b3f88362b30ff281b4fa0e8d0a409"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_members(path, expected, *names):
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == expected, "Archive identity")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            result = []
            for name in names:
                info = archive.getmember("run/" + name)
                require(info.isfile(), "Unexpected member type")
                result.append(archive.extractfile(info).read())
            return result


def load_trace(data):
    rows = csv.DictReader(io.StringIO(data.decode("ascii"), newline=""))
    width = None
    x, y = [], []
    for i, row in enumerate(rows):
        height = float(row["height"])
        if i == 0:
            width = height
        u, p = width - height, 10 * float(row["bottom_pressure_E"])
        require(i == int(row["step"]) and math.isfinite(p) and p >= 0 and
                (u > x[-1] if x else (u, p) == (0., 0.)), "Native trace order")
        x.append(u)
        y.append(p)
    require(len(x) > 1, "Missing nonzero steps")
    return x, y


def value(curve, u):
    x, y = curve
    require(x[0] <= u <= x[-1], "Outside support")
    i = bisect_left(x, u)
    if x[i] == u:
        return y[i]
    weight = (u - x[i-1]) / (x[i] - x[i-1])
    return y[i-1] + (y[i] - y[i-1]) * weight


def knots(*curves):
    end = min(x[-1] for x, _ in curves)
    return sorted({u for x, _ in curves for u in x if u <= end})


def area_max(curve, axis):
    return max(abs(value(curve, u)) for u in axis)


def sample(h, d, f, u):
    half, dense, fine = (value(curve, u) for curve in (h, d, f))
    return dict(u=u, F8_half_MPa=half, F8_dense_MPa=dense, F16_MPa=fine,
                gaps_MPa={"F8_half_minus_F16":half-fine, "F8_half_minus_F8_dense":half-dense,
                          "F8_dense_minus_F16":dense-fine})


def check_return(wall_file, half_file, dense_file):
    c_raw, f_raw = read_members(wall_file, WALL, "arms/F8/trace.csv", "arms/F16/trace.csv")
    h_raw, = read_members(half_file, HALF, "F8_HALF/trace.csv")
    d_raw, summary_raw, result_raw = read_members(dense_file, DENSE, "F8_DENSE/trace.csv",
                                                   "seed_summary.json", "F8_DENSE/result.json")
    c, h, d, f = (load_trace(data) for data in (c_raw, h_raw, d_raw, f_raw))
    old_axis = knots(c, f)
    anchor = max(old_axis, key=lambda u: abs(value(c, u) - value(f, u)))
    axis = knots(h, d, f)
    original_peak = area_max(f, old_axis)
    common_peak = area_max(f, axis)
    rows = [sample(h, d, f, u) for u in axis]
    baseline = "F8_half_minus_F16"
    seed = "F8_half_minus_F8_dense"
    grid = "F8_dense_minus_F16"
    worst = max(rows, key=lambda r: abs(r["gaps_MPa"][baseline]))
    max_roundoff = max(abs(g[baseline]-g[seed]-g[grid]) for g in (r["gaps_MPa"] for r in rows))
    require(max_roundoff < 1e-14, "Signed closure failed")
    at = sample(h,d,f,anchor) if anchor <= axis[-1] else None
    report = json.loads(summary_raw)
    native = json.loads(result_raw)
    require(native["points_count"] == 39053 and native["steps"]+1 == len(d[0]),
            "Point count or trace length")
    require(hashlib.sha256(d_raw).hexdigest() == native["trace_sha256"] == report["seed_trace_sha256"],
            "Native trace identity")
    require(report["status"] == "DEVELOPMENT_SEED_GRID_CONTRAST" and not report["u6_qualified"]
            and not report["stage3_go"], "Arm status")
    comp = report["comparison"]
    require(comp["fixed_u"] == anchor and comp["at_original_anchor"] == at and
            comp["largest_residual_on_common_support"] == worst and
            (comp["common_start_u"],comp["common_end_u"],comp["common_knots"]) == (0.,axis[-1],len(axis)),
            "Return comparison mismatch")
    require((comp["anchor_status"] == "REACHED") == (at is not None), "Anchor coverage")
    statistics = {}
    for name in (baseline,seed,grid):
        record = max(rows, key=lambda r:abs(r["gaps_MPa"][name]))
        signed = record["gaps_MPa"][name]
        statistics[name] = {
            "max_abs_MPa":abs(signed), "signed_at_max_MPa":signed, "u_at_max":record["u"],
            "above_five_percent_of_common_F16_peak_points":sum(
                20 * Fraction(abs(row["gaps_MPa"][name])) > Fraction(common_peak) for row in rows)}
    original_breakdown = None
    if at is not None:
        old = value(c,anchor) - at["F16_MPa"]
        g = at["gaps_MPa"]
        original_breakdown = {
            "original_F8_minus_F16_MPa":old, "dt_MPa":value(c,anchor)-at["F8_half_MPa"],
            "seed_MPa":g[seed], "grid_MPa":g[grid], "grid_percent_of_original_F16_peak":100*g[grid]/original_peak,
            "seed_percent_of_prior_residual":100*g[seed]/g[baseline],
            "grid_percent_of_prior_residual":100*g[grid]/g[baseline],
        }
    return {"fixed_u":anchor, "at_fixed_u":at, "anchor_breakdown":original_breakdown,
            "common_max_baseline":worst, "common_end":axis[-1], "common_knots":len(axis),
            "common_F16_peak_MPa":common_peak, "original_F16_peak_MPa":original_peak,
            "common_max_closure_roundoff_MPa":max_roundoff, "common_statistics":statistics,
            "native_steps":native["steps"], "native_points":native["points_count"],
            "native_status":native["status"], "native_elapsed_s":native["elapsed_s"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for role in ("wall","half","dense"):
        parser.add_argument(role, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = check_return(args.wall,args.half,args.dense)
    data = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        with args.out.open("x", encoding="ascii", newline="\n") as out:
            out.write(data)
    else:
        print(data, end="")
