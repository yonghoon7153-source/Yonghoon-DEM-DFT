"""Read-only candidate pure functions + explicit fix-slot model. Never launches Bash/DEM/SLURM."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys

OUT = Path(__file__).resolve().parent
REPO = OUT.parent / "source" / "repo"
SCRIPT = REPO / "scripts" / "resume_ckpt.sh"
MAIN = REPO / "docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts"
TEST = REPO / "scripts/test_resume_ckpt.py"
raw_script = SCRIPT.read_text(encoding="utf-8")
assert hashlib.sha256(SCRIPT.read_bytes()).hexdigest() == "66006239ec58043f963fa885f9db545c63614d279bfb6cac1665a2eae9884c6d"
embedded = raw_script.split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]
tree = ast.parse(embedded)
# Only the definition preamble, preceding every top-level dispatch branch.
defs = []
for node in tree.body:
    if isinstance(node, (ast.If, ast.Try)):
        break
    assert isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.ClassDef))
    defs.append(node)
scope = {"__name__": "candidate_pure_functions"}
exec(compile(ast.Module(body=defs, type_ignores=[]), str(SCRIPT), "exec"), scope)

test_tree = ast.parse(TEST.read_text(encoding="utf-8"))
raw_fn = next(n for n in test_tree.body if isinstance(n, ast.FunctionDef) and n.name == "qb_raw")
model_harness = {"re": re, "SFX": "r56"}
exec(compile(ast.Module(body=[raw_fn], type_ignores=[]), str(TEST), "exec"), model_harness)
main_text = MAIN.read_text(encoding="utf-8")
raw = model_harness["qb_raw"](main_text, "kg50_d07_b50",
    "restart_kg50_d07_b50/restart_compress_1000000.bin", order="r075",
    stl="plate_kg50_d07_b50_r56.stl")
# These are explicitly synthetic reference-deck-derived input artifacts.
raw_path = OUT / "synthetic_r075_input.liggghts"
raw_path.write_text(raw, encoding="utf-8", newline="\n")
M = scope["deck"](str(MAIN))
R = scope["deck"](str(raw_path))
im = M.index("label loop_press")
ir = R.index("label loop_press")
rr = next(i for i,l in enumerate(R) if l.startswith("read_restart "))
perm, key = scope["prep_order"](M[:im], R[rr+1:ir])
ordered = R[:rr+1] + [R[rr+1+k] for k in perm] + R[ir:]
(OUT / "synthetic_5b_preparation.liggghts").write_text("\n".join(ordered)+"\n",encoding="utf-8", newline="\n")

def slots(commands):
    """Explicit deck commands only; source-backed same-ID replace/unfix slot model."""
    ids, state = [], {}
    for l in commands:
        w = l.split()
        if w[0] == "fix":
            if w[1] not in state:
                ids.append(w[1])
            state[w[1]] = l
        elif w[0] == "unfix":
            if w[1] in state:
                del state[w[1]]
                ids.remove(w[1])
    selected = {"wall/gran", "nve/sphere", "gravity", "viscous", "mesh/surface/stress", "move/mesh", "setforce"}
    return [i for i in ids if state[i].split()[3] in selected]

main_slots = slots(M[:im])
raw_slots = slots(R[:ir])
new_slots = slots(ordered[:ir])
assert main_slots == ["zwall_bot", "integr", "gravi", "top_mesh", "zwall_top", "damp", "move_press"]
assert raw_slots == ["zwall_bot", "integr", "gravi", "damp", "top_mesh", "zwall_top", "move_press"]
assert new_slots == ["zwall_bot", "integr", "top_mesh", "zwall_top", "gravi", "damp", "move_press"]
issues = []
scope["setup_order"](ordered[:ir], M[:im], issues)
# read_restart is excluded by the actual checker before setup_order.
assert len(issues) == 0, issues

# C: direct pure-function boundary checks. These do not claim the full harness tests them.
c_less = scope["prep_order"](["thermo 1000","thermo 1","thermo 1000"], ["thermo 1000"])
assert c_less == ([0], [2])
c_more = scope["prep_order"](["fix x all viscous 0.5"], ["fix x all viscous 0.5","fix x all viscous 0.5"])
assert c_more == ([0,1], [None,0])

# Exact-arithmetic additive map witness; no claim about a multi-step simulation.
f0, g, wall, viscous = 10.0, -9.81, 20.0, -0.5
before = ((f0 + g) + wall) + viscous
after = ((f0 + wall) + g) + viscous
# IEEE-754 mesh reaction can change via (f + contact) - f, even if total f is unchanged.
f0_cancel, g_cancel, wall_cancel = 2.0**53, 2.0, 1.0
reaction_before = ((f0_cancel+g_cancel)+wall_cancel) - (f0_cancel+g_cancel)
reaction_after = (f0_cancel+wall_cancel)-f0_cancel
assert reaction_before == 2.0 and reaction_after == 0.0

# General B noncommuting witness is deliberately outside this one-deck scope.
before_setforce = 0.0
after_setforce = -9.81
result = {
  "classification": "PURE FUNCTION AND SLOT/SCALAR MODEL ONLY. No actual LIGGGHTS/helper/MPI/SLURM/WSL execution.",
  "candidate_pin": "50b5fb4b74c14df8738a3f34cdb36c53c6448bc1",
  "tool_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
  "main_sha256": hashlib.sha256(MAIN.read_bytes()).hexdigest(),
  "main_explicit_dynamical_slots": main_slots,
  "synthetic_helper_raw_slots": raw_slots,
  "synthetic_5b_sorted_slots": new_slots,
  "setup_order_issues": issues,
  "identical_thermo_one_of_two_key": c_less,
  "too_many_identical_fixes_keys": c_more,
  "simple_additive_step": {"before":before,"after":after},
  "mesh_force_difference_scalar_extreme_illustration": {
    "context":"Synthetic floating-point cancellation example only, NOT realistic D0.7 magnitudes",
    "initial_force":f0_cancel,"gravity":g_cancel,"contact":wall_cancel,
    "gravity_before_wall_reported_contact":reaction_before,
    "gravity_after_wall_reported_contact":reaction_after
  },
  "out_of_scope_setforce_general_witness": {"gravity_then_setforce":before_setforce,"setforce_then_gravity":after_setforce}
}
(OUT / "probe_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))

