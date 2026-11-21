"""U6(b) development comparison on the fixed 49-disk compression input."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = {
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}
HISTORICAL = {
    12: "452155b0a82e0b5237b23feb06f0544e1e320afcd0f687e0dcbad06943ddbf89",
    16: "5475cc87df297533002afb621cbdac06c0319ca40eb65ddf40322ae6c018b0de",
}
GRIDS = (8, 12, 16, 24)
TARGETS = (0.84, 0.90, 0.95)
COLUMNS = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
PROTOCOL = "U6b-setting1-bottom-loading-v1"
CAP_MPA, THETA_MPA, E_MPA = 1.2, .008, 10.
DELTA, TAU = .02, .02


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value, message):
    if not value:
        raise ValueError(message)


# Import the exact loading integrator used for the setting-1 F12/F16 reference.
# S and F differ only in the IDs used to scatter to, and gather from, the grid.
def fixed_solver():
    for name, sha in SOURCE.items():
        require(digest(HERE/name) == sha, "fixed source mismatch: " + name)
    spec = importlib.util.spec_from_file_location("u6_fixed", HERE/"suyoung_u6_first_dev.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def field_ids(arm, original_ids):
    require(arm in ("S", "F"), "unknown arm")
    return np.zeros_like(original_ids) if arm == "S" else original_ids


def write_json(path, value):
    with path.open("x", encoding="ascii") as out:
        json.dump(value, out, sort_keys=True, indent=2, allow_nan=False)
        out.write("\n")


def step_size(solver, cells):
    return .35 / (round(cells / solver.DIAMETER) *
                  math.sqrt(solver.model.LAM + 2 * solver.model.MU))


def run_arm(arm, cells, budget, out, *, advance=None):
    require(arm in ("S", "F") and cells in GRIDS, "unknown arm or resolution")
    require(isinstance(budget, (int, float)) and math.isfinite(budget) and budget > 0, "invalid budget")
    solver = fixed_solver()
    advance = solver.advance if advance is None else advance
    out = Path(out)
    out.mkdir(exist_ok=False)
    start = time.monotonic()
    dt = step_size(solver, cells)
    grid = round(cells / solver.DIAMETER)
    x, original_ids, volume = solver.seed(cells)
    fields = field_ids(arm, original_ids)
    v = np.zeros_like(x)
    affine = np.zeros((len(x), 2, 2))
    elastic = np.broadcast_to(np.eye(2), affine.shape).copy()
    total = float(volume.sum())
    trace = out/"trace.csv"
    steps = 0
    status = "TIME_LIMIT"
    with trace.open("x", encoding="ascii", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(COLUMNS)
        writer.writerow((0, 0, solver.WIDTH, 0, total / solver.WIDTH**2))
        while time.monotonic() - start < budget:
            next_step = steps + 1
            height = solver.WIDTH - dt*next_step*solver.WALL_SPEED
            if height < .75*solver.WIDTH:
                status = "GEOMETRY_LIMIT"
                break
            x, v, affine, elastic, pressure = advance(
                x, v, affine, elastic, fields, volume, grid, dt, solver.LO + height)
            require(math.isfinite(pressure) and pressure >= 0.0, "invalid bottom reaction")
            steps = next_step
            writer.writerow((steps, steps*dt, height, pressure, total / (solver.WIDTH*height)))
            if not steps % 25:
                stream.flush()
            if pressure >= solver.TARGET:
                status = "TARGET_BRACKETED"
                break
    result = {
        "protocol": PROTOCOL, "label": "DEVELOPMENT_ONLY", "setting": 1, "arm": arm,
        "cells": cells, "source_sha256": SOURCE, "trace_sha256": digest(trace), "steps": steps,
        "points_count": len(x), "status": status, "budget_s": budget,
        "elapsed_s": time.monotonic() - start, "origin": "new",
    }
    write_json(out/"result.json", result)
    return result


def import_trace(cells, source, out):
    require(cells in HISTORICAL, "only the two identified historical F traces may be imported")
    data = Path(source).read_bytes()
    require(hashlib.sha256(data).hexdigest() == HISTORICAL[cells], "historical F trace mismatch")
    out = Path(out)
    out.mkdir(exist_ok=False)
    trace = out/"trace.csv"
    with trace.open("xb") as dst:
        dst.write(data)
    result = {
        "protocol": PROTOCOL, "label": "DEVELOPMENT_ONLY", "setting": 1, "arm": "F",
        "cells": cells, "source_sha256": SOURCE, "trace_sha256": HISTORICAL[cells],
        "steps": len(data.splitlines())-2, "status": "TARGET_BRACKETED", "origin": "11-20-fixed-repeat",
    }
    write_json(out/"result.json", result)
    return result


def pressures_at_targets(samples):
    """Interpolate loading reaction to the first target height. Since h ∝ 1/Φ,
    interpolation in height uses reciprocal Φ, also on the cap-crossing step."""
    targets = {format(t, ".2f"): {"state": "NOT_REACHED", "pressure_MPa": None} for t in TARGETS}
    previous = None
    for fraction, pressure in samples:
        require(math.isfinite(fraction) and fraction > 0 and math.isfinite(pressure) and pressure >= 0,
                "invalid compression sample")
        if previous is not None:
            f0, p0 = previous
            require(fraction > f0 and p0 < CAP_MPA, "unordered or post-cap sample")
            for target in TARGETS:
                if f0 < target <= fraction:
                    alpha = (1/f0 - 1/target) / (1/f0 - 1/fraction)
                    value = p0 + alpha * (pressure-p0) if target != fraction else pressure
                    if value <= CAP_MPA:
                        targets[format(target, ".2f")] = {
                            "state": "VALUE" if value > THETA_MPA else "NOISE",
                            "pressure_MPa": value,
                        }
        previous = fraction, pressure
    require(previous is not None, "missing trace")
    return targets


def trace_samples(path, solver, cells, receipt):
    dt = step_size(solver, cells)
    area = 49 * math.pi * (solver.DIAMETER/2)**2
    with path.open("r", encoding="ascii", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == COLUMNS, "trace columns differ")
        last = -1
        final_pressure = None
        for step, row in enumerate(reader):
            require(None not in row and row["step"] == str(step), "trace step gap or extra column")
            t, h, p, phi = [float(row[k]) for k in COLUMNS[1:]]
            require(math.isclose(t, step*dt, rel_tol=1e-12, abs_tol=1e-15) and
                    math.isclose(h, solver.WIDTH-t*solver.WALL_SPEED, rel_tol=1e-12) and
                    h >= .75*solver.WIDTH and math.isclose(phi, area/(solver.WIDTH*h), rel_tol=1e-12),
                    "inconsistent loading geometry or time")
            if step == 0:
                require(p == 0, "initial reaction")
            last, final_pressure = step, p
            yield phi, p * E_MPA
    require(last > 0 and last == receipt["steps"], "receipt step count differs")
    if receipt["status"] == "TARGET_BRACKETED":
        require(final_pressure >= solver.TARGET, "missing terminal pressure crossing")
    else:
        require(final_pressure < solver.TARGET and solver.WIDTH-(last+1)*dt*solver.WALL_SPEED < .75*solver.WIDTH,
                "unsubstantiated geometry limit")


def read_run(folder, arm, cells):
    r = json.loads((folder/"result.json").read_bytes())
    require(r.get("arm") == arm and r.get("cells") == cells and r.get("label") == "DEVELOPMENT_ONLY" and
            r.get("protocol") == PROTOCOL and r.get("setting") == 1 and
            r.get("source_sha256") == SOURCE, "arm binding")
    require(r.get("status") in ("TARGET_BRACKETED", "GEOMETRY_LIMIT"), "incomplete arm")
    trace = folder/"trace.csv"
    sha = digest(trace)
    require(sha == r.get("trace_sha256"), "trace hash")
    if r.get("origin") == "11-20-fixed-repeat":
        require(arm == "F" and HISTORICAL.get(cells) == sha, "historical identity")
    else:
        require(r.get("origin") == "new", "unknown provenance")
    points = pressures_at_targets(trace_samples(trace, fixed_solver(), cells, r))
    return {"trace_sha256": sha, "steps": r["steps"], "status": r["status"],
            "origin": r["origin"], "points": points}


def arm_rule(x):
    """Memo 3.2 §4 U6(b) and Appendix D-1, original resolution ladder."""
    require(len(x) == 4 and all(math.isfinite(v) for v in x[1:]) and
            (x[0] is None or math.isfinite(x[0])), "invalid log pressures")
    d0 = x[1]-x[0] if x[0] is not None else None
    d1, d2 = x[2]-x[1], x[3]-x[2]
    same = (d1 > 0 and d2 > 0) or (d1 < 0 and d2 < 0)
    a = same and .5*abs(d1) <= abs(d2) <= 1.1*abs(d1)
    admissible = [d1, d2]
    if d0 is not None and abs(d0) <= TAU:
        admissible.append(d0)
    one_sign = all(v>0 for v in admissible) or all(v<0 for v in admissible)
    one_term = sorted((1.46*d1, 4.23*d1))
    distance = None if d0 is None else max(one_term[0]-d0, 0., d0-one_term[1])
    result = {"rule": "UNCONVERGED", "interval": None, "d0_d1_d2": [d0,d1,d2],
              "suspect_asymptotic": None if d0 is None else a and d0*d1 < 0,
              "bias_signal": None if d0 is None else abs(d0) > TAU and distance > TAU,
              "noise_signal": not a and d1*d2 < 0 and max(abs(d1),abs(d2)) > TAU/2}
    if a:
        lo, hi = sorted((x[3], x[3] + 3*d2))
        result.update(rule="A", interval=[lo-DELTA, hi+DELTA])
    elif max(abs(d1),abs(d2)) <= TAU and not one_sign:
        half = DELTA + 3*max(abs(v) for v in admissible)
        result.update(rule="B", interval=[x[3]-half, x[3]+half])
    return result


def compare(values, unavailable=None):
    expected = {(a,c) for a in ("S","F") for c in GRIDS}
    unavailable = {} if unavailable is None else unavailable
    require(not set(values).intersection(unavailable) and set(values).union(unavailable) == expected,
            "all eight arm/resolution observations required")
    comparisons = {}
    for t in TARGETS:
        key = format(t, ".2f")
        rows = {a:[values[(a,c)][key] if (a,c) in values else
                   {"state":"UNAVAILABLE","pressure_MPa":None} for c in GRIDS] for a in ("S","F")}
        states = {o["state"] for arm in rows.values() for o in arm}
        common = False if "NOT_REACHED" in states else (None if "UNAVAILABLE" in states else True)
        arms = {}
        ratio = None
        for a, data in rows.items():
            logs = [math.log(o["pressure_MPa"]) if o["state"] == "VALUE" else None for o in data]
            usable = (common is not False and all(v is not None for v in logs[1:]) and
                      (logs[0] is not None or data[0]["state"] == "UNAVAILABLE"))
            resolution = arm_rule(logs) if usable else None
            interval = resolution["interval"] if resolution else None
            if common is True and all(o["state"] == "NOISE" for o in data[1:]):
                interval = [None, math.log(THETA_MPA)]
            arms[a] = {"points_in_grid_order": data, "ln_sigma_MPa": logs,
                       "resolution": resolution, "ln_pressure_interval": interval}
        if common is True and all(arm["ln_pressure_interval"] for arm in arms.values()):
            sl, sh = arms["S"]["ln_pressure_interval"]
            fl, fh = arms["F"]["ln_pressure_interval"]
            if sl is not None or fl is not None:
                ratio = [None if sl is None else sl-fh, None if fl is None else sh-fl]
        comparisons[key] = {"common":common, "arms":arms, "ln_S_over_F_interval_report_only":ratio}
    common_points = [p for p in comparisons.values() if p["common"]]
    status = "DEVELOPMENT_READBACK"
    if unavailable:
        status = "INCOMPLETE_INPUT"
    elif not common_points:
        status = "NO_COMMON_TARGET"
    elif not any(all(arm["resolution"] for arm in item["arms"].values()) for item in common_points):
        status = "NO_ABOVE_NOISE_SET"
    return {"protocol":PROTOCOL, "label":"DEVELOPMENT_ONLY", "setting":1, "status":status,
            "resolutions":list(GRIDS), "cap_MPa":CAP_MPA, "noise_floor_MPa":THETA_MPA,
            "unavailable":{a+str(c):reason for (a,c),reason in unavailable.items()},
            "targets":comparisons, "u6_qualified":False, "stage3_go":False}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--arm", choices=["S","F"], required=True)
    run.add_argument("--cells", type=int, choices=GRIDS, required=True)
    run.add_argument("--budget", type=float, required=True)
    run.add_argument("--out", type=Path, required=True)
    old = commands.add_parser("import-trace")
    old.add_argument("--cells", type=int, choices=HISTORICAL, required=True)
    old.add_argument("--source", type=Path, required=True)
    old.add_argument("--out", type=Path, required=True)
    summary = commands.add_parser("summarize")
    summary.add_argument("--runs", type=Path, required=True)
    summary.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        if args.command == "run":
            result = run_arm(args.arm, args.cells, args.budget, args.out)
        elif args.command == "import-trace":
            result = import_trace(args.cells, args.source, args.out)
        else:
            arms, unavailable = {}, {}
            for a in ("S","F"):
                for c in GRIDS:
                    try:
                        arms[(a,c)] = read_run(args.runs/(a+str(c)), a, c)
                    except FileNotFoundError:
                        unavailable[(a,c)] = "MISSING_ARM_OR_TRACE"
                    except (OSError, ValueError, ArithmeticError, KeyError, TypeError) as exc:
                        unavailable[(a,c)] = type(exc).__name__ + ": " + str(exc)
            result = compare({key: arm["points"] for key,arm in arms.items()}, unavailable)
            result["inputs"] = {a+str(c):{k:v for k,v in arm.items() if k != "points"}
                                for (a,c),arm in arms.items()}
            write_json(args.out, result)
        print(json.dumps({"status":result["status"],"output":str(args.out)}, ensure_ascii=True))
        return 4 if result["status"] in ("TIME_LIMIT", "INCOMPLETE_INPUT") else 0
    except (OSError, ValueError, ArithmeticError, KeyError, TypeError) as exc:
        print("U6B_INCOMPLETE",str(exc),file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
