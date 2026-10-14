"""UT -> UTc causal layout reproduction, without DEM or production edits."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import json
import shutil
import sys

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "source/docs/data/ps45_unload_20261009"))
import ul_reader as r
P = r.ul_lib.load_params()
B = r.B73
root = R / "evidence/reader_continuation" / datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%S_%fZ")


def make(basedir, job, steps, events, summary=None):
    half = job != "UB"
    return Path(r._mk_arm(str(basedir), B, job, {"W": 10000 if half else 5000, "dt": 5e-7 if half else 1e-6,
        "steps": copy.deepcopy(steps), "events": events, "summary": summary}, P))


ubs = r._ladder([.2, .25, .3, .35], [1.2, .8, .6, .4])
uts = r._ladder([.2, .4, .45, .5, .55], [5., 1.2, .8, .6, .4])
for i, s in enumerate(uts[1:], 1):
    s.update(kind="A" if i <= 2 else "B", phase=1 if i >= 4 else 0)
    s.pop("n_move", None)
make(root, "UB", ubs, [("CROSS", 2, "first"), ("RM", 4, "ncross2")])
ut = make(root, "UT", uts, [("CROSS", 3, "first"), ("RM", 5, "ncross2")], "RM_STOP")
make(root, "UVb", uts, [("CROSS", 3, "first"), ("RM", 5, "ncross2")])
utv = r.arm_verdict(str(ut), B, "UT", P, root=str(root))
sel = r.selection_state(str(root), P)
assert sel["tuple"] == "t3" and utv["primary_status"] == "OK"
rm = r.read_run(str(ut), P)["steps"][-1]["step"]

# A serializer staging directory supplies only the newly generated continuation
# outputs. Runner lines 199-201 copy CSV history and run U_UT3 in the UTc folder;
# atom/contact/wall/thermo evidence at or before R_M stays in the UT directory.
fullsteps = copy.deepcopy(uts)
fullsteps.append({"lift_um": .60, "P": 0., "steady": True, "nw": 5, "kind": "B", "phase": 3,
    "modeB": 1, "wall": [[], [], [], [], []], "surface": [120.] * 5})
stage = make(root / "serializer", "UTc", fullsteps,
    [("CROSS", 3, "first"), ("RM", 5, "ncross2"), ("RESUME", 5, "state"), ("POST_DONE", 6, "w5")], "DONE")
utc = root / B / "UTc"
(utc / "dump").mkdir(parents=True)
for name in ("ul_windows.csv", "ul_steps.csv", "ul_events.csv", "ul_summary.txt"):
    shutil.copyfile(stage / name, utc / name)
for path in (stage / "dump").iterdir():
    step = int(path.stem.rsplit("_", 1)[1])
    if step > rm:
        shutil.copyfile(path, utc / "dump" / path.name)
# Preserve only post-R_M thermo blocks emitted by the resumed trajectory.
blocks = (stage / "screen.txt").read_text().split("    Step    Atoms")
kept = [blocks[0]]
for block in blocks[1:]:
    rows = block.splitlines()
    start = int(rows[1].split()[0])
    if start >= rm:
        kept.append("    Step    Atoms" + block)
(utc / "screen.txt").write_text("".join(kept))
(utc / "run_manifest.txt").write_text(f"continues=UT rm_step={rm}\n")
utcv = r.arm_verdict(str(utc), B, "UTc", P, root=str(root))
report = r.report(str(root), P)
out = {"fixture_root": str(root), "selection": sel, "UT": utv, "UTc": utcv, "report": report,
    "expected": "Report t3 retains UT primary rho and bracket while appending UTc trajectory observations"}
dest = R / "evidence/reader_continuation.json"
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
assert utcv["primary_status"] == "UNIDENTIFIED" and utcv["rho_pct"] is None
assert report["selection"]["tuple"] == "t3" and report["beds"][B]["rho_pct"] is None
print(json.dumps({"fixture_root": str(root), "selection_tuple": sel["tuple"], "UT_status": utv["primary_status"],
    "UT_rho": utv["rho_pct"], "UTc_status": utcv["primary_status"], "UTc_rho": utcv["rho_pct"],
    "UTc_why": utcv["why"], "report_7_3_status": report["beds"][B]["primary_status"],
    "report_7_3_rho": report["beds"][B]["rho_pct"]}, ensure_ascii=False, indent=2))
