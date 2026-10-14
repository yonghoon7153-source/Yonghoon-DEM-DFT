"""Independent cases exercising the pinned reader's file-to-verdict-to-gate path.

Production _mk_arm is used solely as a dump/CSV serializer; the counterexamples,
expected behavior, and mutations below are independent of its selftests.
No production sources or DEM runs are changed or executed.
"""
from pathlib import Path
import copy
from datetime import datetime, timezone
import json
import sys

REVIEW = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REVIEW / "source/docs/data/ps45_unload_20261009"))
import ul_reader as r

P = r.ul_lib.load_params()
OUT = REVIEW / "evidence/reader_cases" / datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%S_%fZ")
OUT.mkdir(parents=True, exist_ok=True)
B = r.B73
BASE = r._ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4])
for i, step in enumerate(BASE[1:], 1):
    step.update(kind="A" if i == 1 else "B", phase=1 if i >= 3 else 0)
    step.pop("n_move", None)
results = {"fixture_root": str(OUT)}


def fixture(case, job="UB", steps=None, summary=None, events=None):
    root = OUT / case
    d = r._mk_arm(str(root), B, job, {
        "W": 10000 if job in ("UT", "UVb") else 5000,
        "dt": 5e-7 if job in ("UT", "UVb") else 1e-6,
        "steps": copy.deepcopy(BASE if steps is None else steps),
        "summary": summary,
        "events": [("CROSS", 2, "first"), ("RM", 4, "ncross2")] if events is None else events,
    }, P)
    return root, d


def verdict(root, d, job="UB"):
    v = r.arm_verdict(d, B, job, P, root=str(root))
    Path(d, "adversarial_verdict.json").write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
    return v


def compact(v):
    return {k: v.get(k) for k in ("primary_status", "rho_pct", "bracket_um", "union_bracket_um", "nonmonotone", "rank_eligible", "trajectory_status", "s4_status", "separation", "why")}


# Control: complete normal first crossing and two confirmations, then timeout.
root, d = fixture("control")
v = verdict(root, d)
assert v["primary_status"] == "OK" and abs(v["rho_pct"] - .2026077873428664) < 1e-12
results["control"] = compact(v)

# Both confirmation steps reach the registered 12-window budget UNSTEADY.
# The generator nevertheless writes rows and an RM event, and the reader only
# counts rows after j, so the invalid measurement becomes a valid selection input.
bad = copy.deepcopy(BASE)
for s in bad[3:]:
    s.update(steady=False, nw=12, phase=1, s3="bad")
root, d = fixture("confirmation_invalid", "UT", bad, "RM_STOP")
vbad = verdict(root, d, "UT")
_, dub = fixture("confirmation_invalid", "UB")
vub = verdict(root, dub)
r._w(str(root / B / "RJ/restore_verdict.json"), json.dumps({"status": "RESTORED"}))
r._w(str(root / B / "ul_base.in"), "variable ul_S2max equal 1\n")
results["confirmation_invalid"] = {
    "expected": "UNIDENTIFIED and SELECTION_UNRESOLVED; no UV submission",
    "actual": compact(vbad),
    "confirmation_records": r.read_run(d, P)["steps"][-2:],
    "selection": r.selection_state(str(root), P),
    "UVa_gate": r.gate(str(root), B, "UVa", P),
}
assert vbad["primary_status"] == "OK" and r.gate(str(root), B, "UVa", P)[0]

# Valid first crossing occurs between k=0 and k=1. The reader's first-crossing
# search accepts it, but union construction starts at steps[1:] and drops it.
first = r._ladder([0.2, 0.25, 0.3], [0.8, 0.6, 0.4])
for i, step in enumerate(first[1:], 1):
    step.update(kind="A" if i == 1 else "B", phase=1 if i >= 2 else 0)
    step.pop("n_move", None)
root, d = fixture("first_step_cross", steps=first, events=[("CROSS", 1, "first"), ("RM", 3, "ncross2")])
vfirst = verdict(root, d)
other = copy.deepcopy(vfirst)
other["union_bracket_pct"] = [1.0, 1.2]
pair = r.pair_table({r.BEDS[0]: vfirst, r.BEDS[1]: other})[0]
results["first_step_cross"] = {"expected": "union equals the valid actual bracket; pair is SEPARATED", "actual": compact(vfirst), "pair": pair}
assert vfirst["primary_status"] == "OK" and vfirst["union_bracket_um"] is None and pair["relation"] == "UNIDENTIFIED"

# The same omission can falsely distinguish beds after a later rebound. Here
# every post-first lift is exactly the registered B increment, all steps valid.
rebound = r._ladder([.2, .25, .3, .35, .4], [.8, .6, .4, 1.2, .7])
for i, step in enumerate(rebound[1:], 1):
    step.update(kind="A" if i == 1 else "B", phase=0 if i == 1 else (1 if i <= 3 else 2))
    step.pop("n_move", None)
root, d = fixture("first_step_rebound", steps=rebound, events=[("CROSS", 1, "first"), ("RM", 3, "ncross2")])
vrebound = verdict(root, d)
otherbed = r.BEDS[0]
otherdir = r._mk_arm(str(root), otherbed, "UB", {"W": 5000, "dt": 1e-6, "steps": BASE, "summary": None,
    "events": [("CROSS", 2, "first"), ("RM", 4, "ncross2")]}, P)
vother = r.arm_verdict(otherdir, otherbed, "UB", P, root=str(root))
relation = next(p for p in r.pair_table({otherbed: vother, B: vrebound}) if p["a"] == otherbed and p["b"] == B)
correct = copy.deepcopy(vrebound)
correct["union_bracket_pct"] = [0., 100 * .4 / (P["beds"][B]["h0"] * P["units"]["um_per_deck_m"])]
correctrelation = next(p for p in r.pair_table({otherbed: vother, B: correct}) if p["a"] == otherbed and p["b"] == B)
results["first_step_rebound"] = {"expected": "union includes k=0-to-1 bracket; pair OVERLAP", "actual": compact(vrebound),
    "other_bed": compact(vother), "actual_pair": relation, "pair_with_complete_union": correctrelation}
assert relation["relation"] == "SEPARATED" and correctrelation["relation"] == "OVERLAP"

# Reader observes recontact or a missing wall dump after a valid declaration.
# Geometric deck counter can still finish DONE. Requirement says reader wins
# and incomplete auxiliary observation must not be reported as complete.
for tag, last in (("recontact", [-1.0]), ("missing", "missing")):
    steps = copy.deepcopy(BASE)
    steps.append({"lift_um": .4, "P": .0, "steady": True, "nw": 5, "kind": "B", "phase": 3,
                  "modeB": 1, "n_move": 0, "wall": [[], [], [], [], last], "surface": [120.] * 5})
    root, d = fixture("done_" + tag, steps=steps, summary="DONE")
    v = verdict(root, d)
    results["done_" + tag] = {"expected": "valid primary preserved; trajectory separation/surface incomplete", "actual": compact(v)}
    assert v["primary_status"] == "OK" and v["trajectory_status"] == "DONE" and not v["separation"]["separated_final"]

# C14: two rows after crossing may both carry NaN pressure, yet still count.
badnan = copy.deepcopy(BASE)
for s in badnan[3:]:
    s.update(Pbar="nan", phase=1)
root, d = fixture("confirmation_nan", steps=badnan)
v = verdict(root, d)
results["confirmation_nan"] = {"expected": "UNIDENTIFIED", "actual": compact(v)}
assert v["primary_status"] == "OK"

# A first UV submission is allowed. Its partial folder, containing a valid
# first crossing but only one completed confirmation, makes retry gate REFUSE.
root, _ = fixture("uv_retry", "UB")
fixture("uv_retry", "UT")
r._w(str(root / B / "RJ/restore_verdict.json"), json.dumps({"status": "RESTORED"}))
r._w(str(root / B / "ul_base.in"), "variable ul_S2max equal 1\n")
before = r.gate(str(root), B, "UVa", P)
fixture("uv_retry", "UVa", BASE[:-1], events=[("CROSS", 2, "first")])
after = r.gate(str(root), B, "UVa", P)
results["uv_retry"] = {"classification": "Not a finding: run_unload.sh:85 skips this gate when RESUME=1", "before": before, "after": after, "selection_after": r.selection_state(str(root), P)}
assert before[0] and not after[0]

dest = REVIEW / "evidence/reader_adversarial.json"
dest.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(results, ensure_ascii=False, indent=2))
