"""Run and read four author-operated development arms with the original gate arithmetic."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
from types import SimpleNamespace


BASE = "docs/reviews/suyoung_u6a_gates_20261123/"
CELLS = (8, 12, 16, 24)
RULE = "rule/suyoung_u6c_force_rule_20261122/"
PROTOCOL = "U6c-setting2-material-surface-carriers-v1"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location("bound_" + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup(root, prior):
    manifest = root / "SOURCE_SHA256SUMS"
    release = (root / "RELEASE").read_text("ascii").strip()
    check(re.fullmatch(r"[0-9a-f]{40}", release), "candidate release")
    paths = set()
    for line in manifest.read_text("ascii").splitlines():
        expected, name = line.split("  ", 1)
        path = root / name
        check(name not in paths and path.resolve().is_relative_to(root) and digest(path) == expected,
              "candidate source manifest " + name)
        paths.add(name)
    check({"app.py", "correction.py", "RELEASE", "baseline/SOURCE_SHA256SUMS", "rule/gate.py",
           RULE + "force_rule.py", RULE + "rule.json"} <= paths, "missing sources")
    check(Path(__file__).resolve() == root/"app.py", "entry source")
    gate = load(root/"rule/gate.py")
    before = gate.evaluate(prior)
    check(before["status"] == "PASS" and before["selected_setting"] == 2, "original selection")
    baseline = root/"baseline"
    check(digest(baseline/"SOURCE_SHA256SUMS") == gate.SOURCE_HASH and
          (baseline/"RELEASE").read_text("ascii").strip() == gate.RELEASE, "original setting 2 package")
    old = load(baseline / BASE / "setting2_run.py")
    fine = load(baseline/"history"/old.FINE_PATH)
    ctx = fine.context(baseline/"history")
    original_floor = ctx.floor
    correction = load(root/"correction.py")
    floor = SimpleNamespace(make_advance=lambda solver, n: correction.make_advance(original_floor, solver, n))
    force = load(root/RULE/"force_rule.py")
    check(digest(root/RULE/"rule.json") == force.RULE_SHA256 and
          digest(baseline/old.REGISTERED_READER) == gate.RULE_HASH, "changed decision source")
    old.PROTOCOL = PROTOCOL
    return SimpleNamespace(old=old, fine=fine, ctx=ctx._replace(floor=floor),
                           gap=load(baseline / BASE / "gap_kernel.py"),
                           rule=load(baseline/old.REGISTERED_READER), force=force,
                           identity=dict(release=release, protocol=PROTOCOL, setting=2,
                           gap_correction=True, distance_filter=False, friction=.5,
                           baseline_return_sha256=before["return_tar_sha256"],
                           baseline_floor_sha256=ctx.identity["floor_sha256"],
                           carrier_correction_sha256=digest(root/"correction.py"),
                           package_manifest_sha256=digest(manifest),
                           force_rule_sha256=digest(root/RULE/"rule.json"),
                           u6_qualified=False, stage3_go=False, three_dimensional_go=False))


def assess(env, arms, curves):
    check(set(arms) == set(curves) == set(CELLS), "four independent, complete native curves required")
    delta, selection = env.old.decision(env.rule, {n: a["phi_m"] for n, a in arms.items()})
    pairs = {}
    for n, f in ((8, 16), (12, 24)):
        check(arms[n]["dt"] == 2*arms[f]["dt"] and arms[n]["wall_speed"] == arms[f]["wall_speed"],
              "pair clock or loading differs")
        pairs[f"F{n}_F{f}"] = env.force.compare(curves[n], curves[f])
    comparison = env.force.aggregate(pairs)
    return dict(pair_results=pairs, candidate_u6a=selection, candidate_phi_m_abs_delta=delta,
                native_comparison=comparison, item_6=comparison if selection == "PASS" else "HOLD_SELECTION",
                u6b_interval="UNCONFIRMED", other_seven_items="UNASSESSED", u6_qualified=False,
                stage3_go=False, three_dimensional_go=False)


def operator_elapsed(table, budgets):
    elapsed = {}
    with table.open(encoding="ascii", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        check(reader.fieldnames == ["grid", "start_utc", "elapsed_s", "process_rc", "watchdog_status"],
              "operator timing columns")
        for row in reader:
            n = int(row["grid"])
            seconds = int(row["elapsed_s"])
            check(n in budgets and n not in elapsed and None not in row and
                  re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", row["start_utc"]) and
                  0 <= seconds <= budgets[n]+31 and
                  row["process_rc"] == "0" and row["watchdog_status"] == "none", "incomplete operator arm")
            elapsed[n] = seconds
    check(tuple(elapsed) == CELLS, "incomplete or reordered operator record")
    return elapsed


def read_run(env, run):
    check(not (run/"operator_incomplete.json").exists(), "operator recorded incomplete")
    elapsed = operator_elapsed(run/"arm_status.tsv", env.old.BUDGET)
    arms, curves, counts = {}, {}, {}
    for n in CELLS:
        folder = run / f"F{n}"
        check(not (folder/"incomplete.json").exists(), "incomplete F" + str(n))
        obs = json.loads((folder/"observation.json").read_bytes())
        seed, dt, hashes = env.old.seed_and_clock(env, n)
        receipt = env.old.target_receipt(env, n, folder, obs, dt, hashes, len(seed[1]))
        check(receipt == json.loads((folder/"target_receipt.json").read_bytes()), "candidate receipt mismatch")
        check("carrier" in obs["floor"], "missing native carrier evidence")
        native = env.ctx.compare.read_native((folder/"trace.csv").read_bytes(), env.ctx.solver.WIDTH,
                                             receipt["wall_speed"], dt, receipt["status"])
        curves[n] = list(zip(*native, strict=True))
        arms[n] = receipt
        counts[n] = obs["floor"]["carrier"]
    summary = assess(env, arms, curves)
    summary.update(label="DEVELOPMENT_ONLY", identity=env.identity, arms=arms, carrier=counts,
                   arm_seconds_total=math.fsum(a["elapsed_seconds"] for a in arms.values()),
                   operator_seconds_by_grid=elapsed, timeouts_this_complete_return=0, automatic_retries=0)
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=("check", "arm", "summary", "recheck"))
    p.add_argument("--root", required=True, type=Path)
    p.add_argument("--prior", required=True, type=Path)
    p.add_argument("--run", type=Path)
    p.add_argument("--cells", choices=CELLS, type=int)
    args = p.parse_args()
    root = args.root.resolve()
    env = setup(root, args.prior)
    if args.mode == "check":
        for n in CELLS:
            seed, dt, _ = env.old.seed_and_clock(env, n)
            check(len(seed[0]) == len(seed[1]) and dt > 0, "source seed or clock")
        print("SELECTED_2_RETURN_AND_FOUR_CLOCKS_BOUND")
        return
    check(args.run and args.run.is_dir() and all((args.run/k).read_bytes() == (root/k).read_bytes()
          for k in ("RELEASE", "SOURCE_SHA256SUMS")), "run is not bound to package")
    if args.mode == "arm":
        check(args.cells in CELLS, "one native arm required")
        env.old.run_arm(env, args.cells, args.run / f"F{args.cells}")
        return
    result = read_run(env, args.run)
    if args.mode == "recheck":
        saved = json.loads((args.run/"summary.json").read_bytes())
        check(saved == json.loads(json.dumps(result, allow_nan=False)), "returned summary differs")
    else:
        env.old.write_json(args.run/"summary.json", result)
    for key, pair in result["pair_results"].items():
        print(key, pair["comparison"], pair["ratio"])
    print("CANDIDATE_U6A", result["candidate_u6a"], "ITEM6", result["item_6"])


if __name__ == "__main__":
    main()
