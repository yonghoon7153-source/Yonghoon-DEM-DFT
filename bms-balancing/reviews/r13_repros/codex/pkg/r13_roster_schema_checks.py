"""Safe functional R13 schema checks using ordinary synthetic CSV/JSON data.

No evidence replayers, security boundary tests, original data, or solvers are run.
The target checkout is imported read-only with bytecode writing disabled.
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, pathlib, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--target", required=True, type=pathlib.Path)
ap.add_argument("--out", required=True, type=pathlib.Path)
a = ap.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(a.target))
from bms_balancing import schema as S
from bms_balancing import data as D

a.out.mkdir(parents=True, exist_ok=True)
ENV = dict(python="3.11.0", numpy="1.26.0", scipy="1.11.0", pandas="2.0.0", platform="synthetic")
CI = {"half_cell": {"path": "half.xlsx", "sha256": "1" * 64},
      "full_cell": {"path": "full.xlsx", "sha256": "2" * 64},
      "literature": {"gr": {"path": "gr.csv", "sha256": "3" * 64},
                     "si": {"path": "si.csv", "sha256": "4" * 64}}}
RCI = json.loads(json.dumps(CI))
RCI["half_cell"]["sha256"] = "5" * 64

def meta(f, rid):
    raw = f.read_bytes()
    m = dict(artifact=f.name, run_id=rid, sha256=hashlib.sha256(raw).hexdigest(), env=ENV,
             started_utc="2026-09-13T00:00:00Z", git_commit_at_start="0" * 40,
             git_state_changed_during_run=False, git_dirty=False, git_modified_code=[],
             state="100", half_cell_source="GITT", si_source="Li", starts=2, seed=0,
             argv=["synthetic-scientific-schema-check"], roster=S.body_roster(f.name, raw))
    f.with_name(f.name + ".meta.json").write_text(json.dumps(m), encoding="utf-8")

def rows(kind, keys, roster):
    columns = S.required_columns(kind)
    ans = []
    for key in keys:
        r = {k: "1.0" for k in columns}
        r.update(run_id="placeholder", bounds="-", consumed_inputs=json.dumps(CI),
                 ref_consumed_inputs=json.dumps(RCI), inputs_sha=S.inputs_digest(CI),
                 ref_inputs_sha=S.inputs_digest(RCI))
        if kind == "profile":
            r.update(gamma_Si=str(key), profile_scale="global", gamma_roster=json.dumps(roster))
        else:
            r.update(half_cell=key[0], si=key[1], w_dqdv=str(key[2]), ref_bounds="-",
                     scale_audit_target='{"pocv": true}', scale_audit_ref='{"pocv": true}',
                     combo_roster=json.dumps(roster))
        ans.append(r)
    return ans

def publish(d, name, data, rid):
    d.mkdir(parents=True, exist_ok=True)
    f = d / name
    if isinstance(data, list):
        with f.open("w", encoding="utf-8", newline="") as stream:
            w = csv.DictWriter(stream, fieldnames=list(data[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(dict(r, run_id=rid) for r in data)
    else:
        f.write_text(json.dumps(dict(data, run_id=rid)), encoding="utf-8")
    meta(f, rid)
    return f

def gate(d, name, old_data, new_data=None):
    old, new = d / "old", d / "new"
    publish(old, name, old_data, "synthetic-old")
    publish(new, name, old_data if new_data is None else new_data, "synthetic-new")
    p = subprocess.run([sys.executable, "-B", str(a.target / "scripts/check_u14.py"),
                        "--old", str(old), "--new", str(new)], capture_output=True, text=True)
    (d / "gate.stdout.txt").write_text(p.stdout, encoding="utf-8")
    (d / "gate.stderr.txt").write_text(p.stderr, encoding="utf-8")
    line = next((x for x in p.stdout.splitlines() if x.startswith("PROMOTION ")), None)
    return dict(rc=p.returncode, promotion=json.loads(line[10:]) if line else None)

results = {}
gammas = [i / 40 for i in range(21)]
full_gamma = dict(authority=21, requested=21, succeeded=21, missing=[])
combos = [(hc, si, w) for hc in D.HALF_FILE for si in D.SI_SOURCES for w in (0.0, 1.0)]
full_combo = dict(authority=len(combos), requested=len(combos), succeeded=len(combos),
                  missing_input=[], failed=[], absent=[])

cases = {
    "control_profile_complete": ("profile", rows("profile", gammas, full_gamma)),
    "profile_one_gamma_missing": ("profile", rows("profile", gammas[:-1],
        dict(full_gamma, succeeded=20, missing=[0.5]))),
    "profile_twenty_duplicate_missing": ("profile", rows("profile", [0.0],
        dict(full_gamma, succeeded=1, missing=[0.5] * 20))),
    "profile_wrong_grid": ("profile", rows("profile", [i / 50 for i in range(21)], full_gamma)),
    "control_matrix_complete": ("matrix", rows("matrix", combos, full_combo)),
    "matrix_self_declared_one_row_authority": ("matrix", rows("matrix", [("GITT", "Li", 0.0)],
        dict(full_combo, authority=1, requested=1, succeeded=1))),
    "matrix_one_input_missing": ("matrix", rows("matrix", combos[:-1],
        dict(full_combo, succeeded=31, missing_input=["|".join(map(str, combos[-1]))]))),
    "matrix_wrong_member": ("matrix", rows("matrix", combos[:-1] + [(combos[-1][0], "Li2", 1.0)], full_combo)),
}
for label, (kind, rs) in cases.items():
    results[label] = dict(schema_problems=S.check_rows(kind, rs, list(S.required_columns(kind))),
                          body_rows=len(rs), gate=gate(a.out / label, f"{kind}_100.csv", rs))

deg = {k: 1.0 for k in S.DEGENERACY_KEYS}
deg.update(state="100", si_source="Li", half_cell="GITT", w_dqdv=0.0, n_starts=2, seed=0,
           n_grid=21, n_samples=10, n_accepted=1, run_id="placeholder", env=ENV,
           consumed_inputs=CI, ref_consumed_inputs=RCI, inputs_sha=S.inputs_digest(CI),
           best_obj=1.0, best_p=[1.0, 0.0, 1.0, 0.0, 0.25], ref_p=[1.0, 0.0, 1.0, 0.0, 0.25],
           best_modes_percent={"LAM_PE": 0.0, "LAM_NE": 0.0, "LLI": 0.0},
           LAM_PE_percent={"min": 0.0, "max": 0.0, "span": 0.0},
           LAM_NE_percent={"min": 0.0, "max": 0.0, "span": 0.0},
           LLI_percent={"min": 0.0, "max": 0.0, "span": 0.0})
for label, over in {
    "control_degeneracy": {},
    "degeneracy_nonnumeric_objective": {"best_obj": "not-computed"},
    "degeneracy_empty_parameter_vector": {"best_p": []},
    "degeneracy_empty_mode_statistics": {"LLI_percent": {}},
    "degeneracy_boolean_objective": {"best_obj": True},
}.items():
    new = dict(deg, **over)
    results[label] = dict(schema_problems=S.check_degeneracy(new),
                          gate=gate(a.out / label, "degeneracy_100_Li.json", new))
results["degeneracy_boolean_vs_numeric_baseline"] = dict(
    schema_problems=S.check_degeneracy(dict(deg, best_obj=True)),
    gate=gate(a.out / "degeneracy_boolean_vs_numeric_baseline", "degeneracy_100_Li.json", deg,
              dict(deg, best_obj=True)))

# Invoke the real shape CSV writer on finite synthetic scientific measurements.
# This tests producer -> consumer compatibility without fitting or source workbooks.
spec = importlib.util.spec_from_file_location("r13_ne_shape_functional", a.target / "scripts/ne_shape.py")
shape = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shape)
from types import SimpleNamespace
shapedir = a.out / "fresh_shape_producer"
shape_states = D.declared_states("GITT")
shape_art = shape._write_csv(shapedir, SimpleNamespace(source="GITT", si_source="Li", out_dir="synthetic-matrix"),
    [(state, 12.0, 6.0, 0.5, 10.0, 5.0, 0.25, 0.2, 1.0, 0.5) for state in shape_states],
    {state: 99.0 for state in shape_states}, 100.0,
    {state: (state, 0.3, 10.0) for state in shape_states},
    headroom={state: {"dneg": -0.2, "dpos": 0.3, "fam_max": 20.0, "g_at_max": 0.5,
                        "witness": 0.3, "wdelta": 0.1} for state in shape_states},
    consumed={"synthetic": True}, pairing={"authority": shape_states, "requested": shape_states,
       "paired": shape_states, "missing": [], "missing_input": []}, status="complete")
p = subprocess.run([sys.executable, "-B", str(a.target / "scripts/check_u14.py"),
                    "--new", str(shapedir), "--schema-only"], capture_output=True, text=True)
(shapedir / "gate.stdout.txt").write_text(p.stdout, encoding="utf-8")
(shapedir / "gate.stderr.txt").write_text(p.stderr, encoding="utf-8")
line = next((x for x in p.stdout.splitlines() if x.startswith("PROMOTION ")), None)
results["fresh_shape_producer"] = dict(rc=p.returncode, artifact=str(shape_art),
    promotion=json.loads(line[10:]) if line else None,
    limitation="Actual CSV writer invoked; finite measurements and pairing supplied synthetically. No solver run.")

(a.out / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
for label, r in results.items():
    g = r.get("gate", r)
    promo = g.get("promotion") or {}
    print(json.dumps(dict(case=label, schema_count=len(r.get("schema_problems", [])),
        rc=g["rc"], eligible=promo.get("promotion_eligible"), blocked_by=promo.get("blocked_by"))))
