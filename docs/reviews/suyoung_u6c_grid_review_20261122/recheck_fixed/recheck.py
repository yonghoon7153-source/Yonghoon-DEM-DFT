"""Portable readback for the first corrected U6(c) F8/F16 pair. No model imports."""
import argparse
from bisect import bisect_left
import csv
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path


KERNEL_SHA = "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645"
PAIR_SHA = "ac41923ff100546da8a2e675b1c89fc748819ee2ab3609946c02c3c4ce3fc2cf"
# From the two author returns identified in data/provenance.json.
COMPLETE = {
    8: dict(steps=2659,
            candidate="b1a836894831dc4fa7f86736a739c95d27491b5ee0c62c70ccc6de6bee661ecb",
            prefix="d7cac0ca9edff65eed6d76588c05f0e50dc4d5cfee8f334e14e51f52a4015f26"),
    16: dict(steps=6542,
             candidate="39750688132418b0f6408e91fe703611938c3a0823387a7b85aa1c7aa2a67dad",
             prefix="5faeaae50e85b52771ee5900285ab095fb2f472a123d12173791c51ad9920ebf"),
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def close(a, b):
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-14)


def check_phase(record, dt):
    mass, speed, impulse = record["M"], record["mean_down"], record["J"]
    if record["count"] == 0:
        require(mass == impulse == 0 and speed is None, "empty wall support")
        return 0., None, 0.
    require(type(record["count"]) is int and record["count"] > 0, "wall entry count")
    require(all(isinstance(x, (float, int)) and math.isfinite(x) and x > 0
                for x in (mass, speed, impulse)), "wall support factors")
    require(close(mass * speed, impulse), "wall impulse differs from M times weighted speed")
    return mass / dt, speed, impulse / dt


def pinned_json(raw, expected, name):
    require(hashlib.sha256(raw).hexdigest() == expected, name + " byte identity")
    return json.loads(raw)


def read_grid(data, n):
    grid = "F" + str(n)
    full = data / "full" / grid
    pins = COMPLETE[n]
    pair = pinned_json((data / "full/grid_comparison.json").read_bytes(), PAIR_SHA, "completed pair receipt")
    require(pair["status"] == "DEVELOPMENT_PAIR_READ_BACK" and pair["kernel_sha256"] == KERNEL_SHA,
            "pair completion or kernel identity")
    candidate = pinned_json((full / "candidate.json").read_bytes(), pins["candidate"], grid + " candidate")
    result = pinned_json((full / "result.json").read_bytes(), candidate["native_result_sha256"], grid + " result")
    raw = (full / "trace.csv").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == candidate["trace_sha256"] == result["trace_sha256"],
            grid + " full trace byte identity")
    require(candidate == pair["receipts"][grid] and candidate["kernel_sha256"] == pair["kernel_sha256"]
            and result["cells"] == candidate["cells"] == n and result["arm"] == "F"
            and result["steps"] == candidate["candidate_calls"] == pins["steps"]
            and result["status"] == candidate["status"] == "TARGET_BRACKETED",
            grid + " completed arm receipts")
    prefix = data / "prefix" / grid
    short = (prefix / "trace.csv").read_bytes()
    obs = (prefix / "wall_observations.json").read_bytes()
    receipt = pinned_json((prefix / "prefix_receipt.json").read_bytes(), pins["prefix"], grid + " prefix receipt")
    require(receipt["kernel_sha256"] == candidate["kernel_sha256"]
            and receipt["geometry"] == candidate["geometry"] and receipt["mapping"] == candidate["mapping"]
            and receipt["runner_sha256"] == candidate["runner_sha256"] and receipt["status"] == "DEVELOPMENT_PREFIX_OBSERVED",
            grid + " prefix/full identity")
    walls = json.loads(obs)
    require(hashlib.sha256(short).hexdigest() == receipt["raw_prefix_sha256"]
            and hashlib.sha256(obs).hexdigest() == receipt["observations_sha256"], "prefix hashes")
    require(raw.startswith(short) and short.endswith(b"\n")
            and len(short.splitlines()) == len(walls) + 2, "prefix bytes/count")
    rows = list(csv.DictReader(io.StringIO(raw.decode("ascii"), newline="")))
    require(len(rows) == result["steps"] + 1 and len(walls) == receipt["steps"], grid + " record count")
    axis, values = [], []
    width = float(rows[0]["height"])
    dt = float(rows[1]["time_code"])
    require(dt > 0 and dt == receipt["dt"] and receipt["cells"] == n, "grid identity")
    for step, row in enumerate(rows):
        u = width - float(row["height"])
        p = 10 * float(row["bottom_pressure_E"])
        require(step == int(row["step"]) and float(row["time_code"]) == step * dt
                and math.isfinite(u) and math.isfinite(p) and (not axis or u > axis[-1]), "trace")
        axis.append(u)
        values.append(p)
        if 0 < step <= len(walls):
            record = walls[step-1]
            require((record["step"], record["u"], record["p_MPa"]) == (step, u, p), "wall/trace misalignment")
            pressure = sum(check_phase(record[phase], dt)[2] for phase in ("pre", "post")) * 10 / width
            require(close(pressure, p), "two impulses differ from recorded pressure")
    require(axis[0] == 0 and all(p < 1.2 for p in values[:-1]) and values[-1] >= 1.2, "target bracket")
    return axis, values, width, dt, walls


def at(u, x, y):
    i = bisect_left(x, u)
    if i < len(x) and x[i] == u:
        return y[i], i
    require(0 < i < len(x), "extrapolation")
    t = (u - x[i-1]) / (x[i] - x[i-1])
    return y[i-1] + t * (y[i] - y[i-1]), None


def compare(x8, y8, x16, y16):
    lo, hi = max(x8[0], x16[0]), min(x8[-1], x16[-1])
    require(hi > lo, "empty overlap")
    knots = sorted(set(u for xs in (x8, x16) for u in xs if lo <= u <= hi))
    pairs = [(at(u, x8, y8), at(u, x16, y16)) for u in knots]
    gaps = [abs(coarse[0] - fine[0]) for coarse, fine in pairs]
    peak = max(abs(fine[0]) for _, fine in pairs)
    maximum = max(gaps)
    above = ([i for i, gap in enumerate(gaps) if 20 * Fraction(gap) > Fraction(peak)] if peak else [])
    metric = dict(common_end=hi, common_knots=len(knots), fine_peak_MPa=peak, max_gap_MPa=maximum,
                  u_at_max_gap=knots[gaps.index(maximum)], above_5_percent=len(above) if peak else None,
                  ratio=maximum/peak if peak else None,
                  status="ZERO_REFERENCE" if not peak else ("EXCEEDS" if above else "WITHIN"))
    if not above:
        return metric, None
    i = above[0]
    (coarse, cstep), (fine, fstep) = pairs[i]
    metric["first_exceedance"] = dict(u=knots[i], F8_native_step=cstep, F16_native_step=fstep,
                                      F8_pressure_MPa=coarse, F16_pressure_MPa=fine,
                                      F8_minus_F16_MPa=coarse-fine, threshold_MPa=peak/20)
    return metric, knots[i]


def split_wall(c, f, dt8, dt16, width):
    a, v, impulse8 = check_phase(c, dt8)
    b, w, impulse16 = check_phase(f, dt16)
    scale = 10 / width
    if v is None or w is None:
        return 0., 0., scale * (impulse8 - impulse16)
    # Average the two possible orders of replacing factors in the product.
    mass_effect = scale * (a - b) * ((v + w) / 2)
    speed_effect = scale * ((a + b) / 2) * (v - w)
    return mass_effect, speed_effect, 0.


def readback(data):
    x8, y8, width8, dt8, w8 = read_grid(data, 8)
    x16, y16, width16, dt16, w16 = read_grid(data, 16)
    require(width8 == width16 and dt8 == 2 * dt16, "geometry or dt")
    metric, u = compare(x8, y8, x16, y16)
    require(u is not None and u not in x8 and u in x16, "first crossing should be fine-native only")
    endpoints = []
    shared = sorted(set(x8).intersection(x16))
    j = bisect_left(shared, u)
    require(0 < j < len(shared), "missing bracketing native points")
    for loc in shared[j-1:j+1]:
        _, ci = at(loc, x8, y8)
        _, fi = at(loc, x16, y16)
        require(0 < ci <= len(w8) and 0 < fi <= len(w16), "missing native factors")
        rc, rf = w8[ci-1], w16[fi-1]
        phases = [split_wall(rc[k], rf[k], dt8, dt16, width8) for k in ("pre", "post")]
        contributions = [sum(pair) for pair in zip(*phases)]
        gap = y8[ci] - y16[fi]
        require(close(sum(contributions), gap), "symmetric split fails to reconstruct pressure difference")
        endpoints.append(dict(F8_step=ci, F16_step=fi, u=loc, gap_MPa=gap,
                              mass_over_dt_MPa=contributions[0], speed_MPa=contributions[1],
                              one_sided_MPa=contributions[2],
                              signed_percent=[100*v/gap for v in contributions] if gap else None))
    return dict(development_only=True, U6c_qualified=False, stage3_go=False,
                grid=metric, adjacent_native=endpoints, F12_F24="NOT_MEASURED_WITH_THIS_KERNEL")


def synthetic():
    def s(m, v):
        return dict(count=int(m>0), M=m, mean_down=v, J=m*v if v is not None else 0.)
    x, y, z = split_wall(s(2.,3.),s(1.,1.),1.,1.,10.)
    require((x,y,z)==(2.,3.,0.), "joint-factor example")
    require(split_wall(s(3.,2.),s(0.,None),1.,.5,10.)==(0.,0.,6.), "one-sided support")
    require(split_wall(s(2.,2.),s(1.,2.),1.,.5,10.)==(0.,0.,0.), "dt weighting")
    metric,u=compare([0.,2.],[0.,0.],[0.,1.,2.,3.],[0.,1.,0.,100.])
    require(metric["fine_peak_MPa"]==1 and u==1 and metric["first_exceedance"]["F8_native_step"] is None,
            "fine-only knot or common denominator")
    require(compare([0.,1.],[0.,0.],[0.,1.],[0.,0.])[0]["status"]=="ZERO_REFERENCE", "zero denominator")
    require(compare([0.,1.],[0.,19.],[0.,1.],[0.,20.])[0]["status"]=="WITHIN", "strict 5%")
    try:
        at(3., [0.,2.], [0.,2.])
    except ValueError:
        pass
    else:
        raise AssertionError("extrapolated past either arm")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, required=True)
    args = p.parse_args()
    synthetic()
    print(json.dumps(readback(args.data), sort_keys=True, indent=2, allow_nan=False))
