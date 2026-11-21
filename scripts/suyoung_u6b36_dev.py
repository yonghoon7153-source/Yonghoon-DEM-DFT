"""S36/F36 development comparison with the bound 12/16/24-cell observations."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tarfile


GRIDS = (12, 16, 24, 36)
HISTORY_SHA = "a3877d077b56d74877a04215e06135bc3217b5c0f055bf0061a9ba93fcf49f00"
DRIVER_SHA = "50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762"
HISTORY_PIN = "6bdfac91520c868b5036071e6d60464972727f49"


def arm_rule(x):
    """Memo 3.2 appendix D-1. The shifted witness is 12, the endpoint is 36."""
    legacy.require(len(x) == 4 and all(math.isfinite(v) for v in x[1:]) and
                   (x[0] is None or math.isfinite(x[0])), "invalid log pressures")
    d0 = x[1] - x[0] if x[0] is not None else None
    d1, d2 = x[2] - x[1], x[3] - x[2]
    used = [d1, d2]
    if d0 is not None and abs(d0) <= legacy.TAU:
        used.append(d0)
    same_sign = (d1 > 0 and d2 > 0) or (d1 < 0 and d2 < 0)
    interval = None
    rule = "UNCONVERGED"
    if same_sign and .29*abs(d1) <= abs(d2) <= .75*abs(d1):
        rule = "A"
        lo, hi = sorted((x[3], x[3] + 3*d2))
        interval = [lo-legacy.DELTA, hi+legacy.DELTA]
    elif max(abs(d1), abs(d2)) <= legacy.TAU and min(used) <= 0 <= max(used):
        rule = "B"
        half = legacy.DELTA + 3*max(abs(v) for v in used)
        interval = [x[3]-half, x[3]+half]
    return {"rule":rule, "interval":interval, "d0_d1_d2":[d0, d1, d2],
            "suspect_asymptotic":None if d0 is None else rule == "A" and d0*d1 < 0,
            "noise_signal":rule != "A" and d1*d2 < 0 and max(abs(d1),abs(d2)) > legacy.TAU/2}


def load_driver():
    path = Path(__file__).resolve().with_name("suyoung_u6b_dev.py")
    if hashlib.sha256(path.read_bytes()).hexdigest() != DRIVER_SHA:
        raise ValueError("original U6(b) driver identity mismatch")
    spec = importlib.util.spec_from_file_location("private_u6b_shifted_driver", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Private instance only. The pinned integrator, plate, trace reader, noise
    # handling and interval subtraction are reused for the shifted comparison.
    module.GRIDS = GRIDS
    module.arm_rule = arm_rule
    return module


legacy = load_driver()


def read_history(path, expected_sha=HISTORY_SHA):
    """Read the original summary and validate all six supporting trace receipts."""
    from io import BytesIO
    data = Path(path).read_bytes()
    legacy.require(hashlib.sha256(data).hexdigest() == expected_sha, "wrong U6(b) history archive")
    with tarfile.open(fileobj=BytesIO(data), mode="r:gz") as archive:
        members = archive.getmembers()
        legacy.require(len({item.name for item in members}) == len(members), "duplicate history member")

        def member(name):
            info = archive.getmember(name)
            legacy.require(info.isfile(), "history member is not a regular file")
            return archive.extractfile(info).read()

        previous = json.loads(member("run/summary.json"))
        legacy.require(previous["resolutions"] == [8,12,16,24] and previous["setting"] == 1
                       and previous["label"] == "DEVELOPMENT_ONLY" and previous["protocol"] == legacy.PROTOCOL
                       and previous["status"] == "DEVELOPMENT_READBACK", "historical ladder identity mismatch")
        rows = {}
        for arm in ("S", "F"):
            for index, cells in enumerate(GRIDS[:-1], start=1):
                name = arm + str(cells)
                info = previous["inputs"][name]
                receipt = json.loads(member(f"run/arms/{name}/result.json"))
                trace_sha = hashlib.sha256(member(f"run/arms/{name}/trace.csv")).hexdigest()
                legacy.require(receipt["arm"] == arm and receipt["cells"] == cells
                               and receipt["setting"] == 1 and receipt["label"] == "DEVELOPMENT_ONLY"
                               and receipt["protocol"] == legacy.PROTOCOL and receipt["source_sha256"] == legacy.SOURCE
                               and trace_sha == info["trace_sha256"]
                               and all(info[k] == receipt[k] for k in ("trace_sha256","steps","status","origin")),
                               "historical arm or trace identity mismatch: " + name)
                rows[(arm,cells)] = dict(info, points={
                    key: previous["targets"][key]["arms"][arm]["points_in_grid_order"][index]
                    for key in (format(t, ".2f") for t in legacy.TARGETS)})
    return rows


def run(arm, budget, out):
    return legacy.run_arm(arm, 36, budget, out)


def compare(rows, unavailable):
    summary = legacy.compare({pair: row["points"] for pair, row in rows.items()}, unavailable)
    missing_points = {}
    for arm in ("S","F"):
        latest = rows.get((arm,36))
        if latest is not None:
            missing = [key for key, point in latest["points"].items() if point["state"] == "NOT_REACHED"]
            if missing:
                missing_points[arm+"36"] = missing
    summary.update(history_sha256=HISTORY_SHA, history_pin=HISTORY_PIN, witness_cells=12,
                   comparison_cells=[16,24,36], missing_36_targets=missing_points,
                   inputs={a+str(c):{k:v for k,v in row.items() if k != "points"}
                           for (a,c),row in rows.items()})
    return summary


def summarize(history, runs, out):
    rows = read_history(history)
    unavailable = {}
    for arm in ("S", "F"):
        name = arm+"36"
        directory = runs/name
        try:
            raw = json.loads((directory/"result.json").read_bytes())
        except FileNotFoundError:
            unavailable[(arm,36)] = "MISSING_ARM_OR_RECEIPT"
            continue
        legacy.require(raw.get("arm") == arm and raw.get("cells") == 36 and raw.get("origin") == "new"
                       and raw.get("label") == "DEVELOPMENT_ONLY" and raw.get("setting") == 1
                       and raw.get("protocol") == legacy.PROTOCOL and raw.get("source_sha256") == legacy.SOURCE,
                       "new receipt identity mismatch: " + name)
        if raw["status"] == "TIME_LIMIT":
            unavailable[(arm,36)] = "TIME_LIMIT"
            continue
        try:
            row = legacy.read_run(directory, arm, 36)
        except FileNotFoundError:
            unavailable[(arm,36)] = "MISSING_TRACE"
            continue
        rows[(arm,36)] = row
    summary = compare(rows, unavailable)
    legacy.write_json(out, summary)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    r = commands.add_parser("run")
    r.add_argument("--model", choices=("S","F"), required=True)
    r.add_argument("--budget", type=float, required=True)
    r.add_argument("--out", type=Path, required=True)
    s = commands.add_parser("summarize")
    s.add_argument("--history", type=Path, required=True)
    s.add_argument("--runs", type=Path, required=True)
    s.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            result = run(args.model, args.budget, args.out)
        else:
            result = summarize(args.history, args.runs, args.out)
        print(json.dumps({"status":result["status"], "output":str(args.out)}, ensure_ascii=True))
        return 4 if result["status"] in ("TIME_LIMIT","INCOMPLETE_INPUT") else 0
    except (OSError, ValueError, ArithmeticError, KeyError, TypeError, tarfile.TarError) as exc:
        print("U6B36_INCOMPLETE", str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
