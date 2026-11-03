"""Pure-Python protocol probe. Never executes a runner, DEM, scheduler, or shell.

Extracts only runnerck.render's AST from the pinned resume_ckpt.sh, feeds two
synthetic deck byte strings with real SHA-256 hashes, and saves its actual
rendered main/trial runners. The fixture hashes are not ibb evidence.
"""
import ast
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parent / "source" / "repo"
script = (REPO / "scripts" / "resume_ckpt.sh").read_text(encoding="utf-8")
runner_source = script.split("runnerck(){ python3 -I - \"$@\" <<'PY'\n", 1)[1].split("\nPY\n}", 1)[0]
tree = ast.parse(runner_source)
render_node = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "render")
ns = {}
exec(compile(ast.Module(body=[render_node], type_ignores=[]), "pinned-runner-render", "exec"), ns)

case, suffix = "kg50_d07_b50", "r56"
work = "/synthetic/dem_test/" + case
checkpoint = work + "/restart_" + case + "/restart_compress_1000000.bin"
main_deck = "read_restart restart_compress_1000000.bin\nrun 2\nlabel loop_press\nrun 5000\n"
trial_deck = "read_restart restart_compress_1000000.bin\nrun 2\nrun 1998\n"
digest = lambda text: hashlib.sha256(text.encode()).hexdigest()
info = {
    "sb": {"--time=": "5-00:00:00"},
    "env": [],
    "ab": {
        "재개 덱": work + "/input_" + case + "_r56.liggghts",
        "시험 덱": work + "/input_" + case + "_r56t.liggghts",
    },
    "sha": {"재개 덱": digest(main_deck), "시험 덱": digest(trial_deck), "체크포인트": digest("synthetic checkpoint")},
    "ckp": checkpoint,
}

rendered = {}
for trial, role in ((False, "main"), (True, "trial")):
    text = ns["render"](case, suffix, "56", work, info, trial)
    (BASE / (role + "_runner.synthetic.sh")).write_text(text, encoding="utf-8", newline="\n")
    key = "시험 덱" if trial else "재개 덱"
    rendered[role] = {
        "expected_deck_path": info["ab"][key],
        "expected_deck_sha256": info["sha"][key],
        "receipt_row": 3 if trial else 1,
        "identity_output_template": next(x for x in text.splitlines() if x.startswith('echo "LMP_IDENTITY ')),
        "expected_hash_guard": next(x for x in text.splitlines() if x.startswith('[ "$ds"')),
    }
assert rendered["main"]["expected_deck_path"] != rendered["trial"]["expected_deck_path"]
assert rendered["main"]["expected_deck_sha256"] != rendered["trial"]["expected_deck_sha256"]

# Read the actual fixture, but do not execute its LIGGGHTS commands.
actual_deck = (REPO / "docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts").read_text(encoding="utf-8")
prefix, loop = actual_deck.split("label loop_press", 1)
runs = [int(s.split()[1]) for s in prefix.splitlines() if s.strip().startswith("run ")]
entry = sum(runs)
period = int(next(s.split()[1] for s in loop.splitlines() if s.strip().startswith("run ")))
phases = [{"S0": s0, "phase": (s0 - entry) % period, "residual": period - ((s0 - entry) % period), "next_decision": s0 + period - ((s0 - entry) % period)} for s0 in (1000000, 1200000, 1400000, 2000000)]
assert entry == 400002 and period == 5000 and all(x["residual"] == 2 for x in phases)
result = {"kind": "synthetic protocol probe; not actual -T evidence", "source_sha256": hashlib.sha256((REPO / "scripts" / "resume_ckpt.sh").read_bytes()).hexdigest(), "rendered": rendered, "actual_fixture_prefix_runs": runs, "entry": entry, "period": period, "phase_samples": phases, "literal_main_vs_trial_identity_equal": False, "assertions": "PASS"}
out = json.dumps(result, ensure_ascii=False, indent=2)
(BASE / "probe_identity_mapping.json").write_text(out + "\n", encoding="utf-8")
print(out)
