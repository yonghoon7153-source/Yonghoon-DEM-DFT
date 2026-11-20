"""Compare one new CPU run per U6(a) resolution with its frozen first run."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import sys

FIXED = ("cells", "protocol", "label", "disks", "points", "contact",
         "friction", "wall_speed", "target_E", "dt", "qualified")
BAND = 0.005


def bracket_value(trace, target, expected_steps):
    rows = csv.DictReader(io.StringIO(trace.decode("ascii")))
    reference_area_per_width = None
    previous = None
    crossing = None
    for index, row in enumerate(rows):
        step = int(row["step"])
        h = float(row["height"])
        p = float(row["bottom_pressure_E"])
        phi = float(row["phi_m"])
        if step != index or h <= 0 or phi <= 0 or not all(map(math.isfinite, (h, p, phi))):
            raise ValueError("invalid trace row")
        if index == 0:
            reference_area_per_width = h * phi
        if not math.isclose(h * phi, reference_area_per_width, rel_tol=1e-12):
            raise ValueError("reference area drift")
        if previous is not None and crossing is None:
            last_step, last_h, last_p = previous
            if last_p < target <= p:
                h_at_target = last_h + (h-last_h) * (target-last_p)/(p-last_p)
                crossing = (step, reference_area_per_width/h_at_target)
        previous = (step, h, p)
    if not previous or not crossing or crossing[0] != previous[0] or previous[0] != expected_steps:
        raise ValueError("last record must be the first crossing")
    return crossing[1]


def grid_status(difference):
    return "WITHIN_DEVELOPMENT_BAND" if difference <= BAND else "OUTSIDE_DEVELOPMENT_BAND"


def compare_pair(reference, arms, exit_codes):
    obs = {}
    for name in ("12", "16"):
        old = reference[name]
        rec, trace = arms[name]
        obs[name] = {"command_rc": exit_codes[name], "first_phi": old["result"]["phi_m"],
                     "repeat_phi": None, "repeat_status": rec.get("status"), "within_resolution_delta": None}
        if exit_codes[name] != 0:
            continue
        if any(rec.get(k) != old["result"][k] for k in FIXED):
            raise ValueError(f"F{name}: fixed condition differs")
        digest = hashlib.sha256(trace).hexdigest()
        obs[name].update(trace_sha256=digest, trace_identical=(digest == old["trace_sha256"]),
                         steps=rec["steps_attempted"], elapsed_s=rec["elapsed_s"])
        if rec["status"] != "TARGET_BRACKETED":
            continue
        phi = rec["phi_m"]
        if not isinstance(phi, float) or not math.isclose(
                bracket_value(trace, rec["target_E"], rec["steps_attempted"]), phi,
                abs_tol=1e-13, rel_tol=1e-13):
            raise ValueError(f"F{name}: interpolated endpoint differs")
        obs[name].update(repeat_phi=phi, within_resolution_delta=phi-obs[name]["first_phi"])
    old_gap = abs(obs["12"]["first_phi"]-obs["16"]["first_phi"])
    complete = all(value["repeat_phi"] is not None for value in obs.values())
    new_gap = abs(obs["12"]["repeat_phi"]-obs["16"]["repeat_phi"]) if complete else None
    return {"arms":obs, "assessment":grid_status(new_gap) if complete else "INCOMPLETE",
            "first_assessment":grid_status(old_gap), "first_abs_grid_delta":old_gap,
            "repeat_abs_grid_delta":new_gap, "repeat_band_margin":BAND-new_gap if complete else None,
            "max_within_resolution_abs_delta":max(abs(v["within_resolution_delta"]) for v in obs.values()) if complete else None,
            "both_traces_identical":all(v.get("trace_identical") for v in obs.values()) if complete else None,
            "band":BAND, "label":"DEVELOPMENT_ONLY", "selected_setting":None, "u6_qualified":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("arm", "compare"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--cells", type=int, choices=(12,16))
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if args.action == "arm":
        if args.cells is None:
            parser.error("--cells is required for arm")
        sys.path.insert(0, str(root))
        import suyoung_u6_first_dev as solver
        solver.run(args.cells, args.output, {12:570.,16:1170.}[args.cells])
        return 0
    reference = json.loads((root/"first_runs.json").read_bytes())
    codes = {}
    arms = {}
    for name in ("12", "16"):
        leaf = args.output/("F"+name)
        codes[name] = int((args.output/("rc_"+name+".txt")).read_text())
        arms[name] = (json.loads((leaf/"result.json").read_bytes()), (leaf/"trace.csv").read_bytes()) if codes[name] == 0 else ({}, b"")
    result = compare_pair(reference, arms, codes)
    with (args.output/"comparison.json").open("x",encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")
    print(result["assessment"], "repeat_abs_delta=",result["repeat_abs_grid_delta"])
    return 4 if result["assessment"]=="INCOMPLETE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
