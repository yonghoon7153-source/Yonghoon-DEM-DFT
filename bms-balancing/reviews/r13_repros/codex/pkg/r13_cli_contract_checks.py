"""Ordinary scientific artifact/CLI checks for R13. No security replay.

Consumes synthetic positive controls produced by r13_roster_schema_checks.py.
All generated data and captured logs stay under --out; target stays read-only.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import pathlib
import shutil
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--target", type=pathlib.Path, required=True)
ap.add_argument("--fixtures", type=pathlib.Path, required=True)
ap.add_argument("--out", type=pathlib.Path, required=True)
a = ap.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(a.target))
from bms_balancing import schema as S

a.out.mkdir(parents=True, exist_ok=True)
results = {}

def clone(label, control="control_degeneracy"):
    dest = a.out / label
    if dest.exists():
        raise SystemExit(f"Use a fresh output directory: {dest}")
    shutil.copytree(a.fixtures / control / "old", dest / "old")
    shutil.copytree(a.fixtures / control / "new", dest / "new")
    return dest

def artifact(folder):
    return next(p for p in folder.iterdir() if p.suffix in (".csv", ".json") and not p.name.endswith(".meta.json"))

def update_json(folder, change, bom=False):
    p = artifact(folder)
    j = json.loads(p.read_text(encoding="utf-8-sig"))
    change(j)
    raw = json.dumps(j).encode("utf-8")
    if bom:
        raw = b"\xef\xbb\xbf" + raw
    p.write_bytes(raw)
    side = p.with_name(p.name + ".meta.json")
    meta = json.loads(side.read_text())
    meta["sha256"] = hashlib.sha256(raw).hexdigest()
    # BOM is a representation test; the logical body roster is unchanged.
    meta["roster"] = S.body_roster(p.name, raw.removeprefix(b"\xef\xbb\xbf"))
    side.write_text(json.dumps(meta), encoding="utf-8")

def execute(label, folder=None, schema_only=False, candidate=None):
    dest = folder or a.out / label
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-B", str(a.target / "scripts/check_u14.py"),
           "--new", str(candidate or dest / "new")]
    cmd += ["--schema-only"] if schema_only else ["--old", str(dest / "old")]
    p = subprocess.run(cmd, capture_output=True, text=True)
    (dest / "stdout.txt").write_text(p.stdout, encoding="utf-8")
    (dest / "stderr.txt").write_text(p.stderr, encoding="utf-8")
    line = next((x for x in p.stdout.splitlines() if x.startswith("PROMOTION ")), None)
    results[label] = dict(command=cmd, rc=p.returncode,
        promotion=json.loads(line[10:]) if line else None,
        stderr_tail=p.stderr.splitlines()[-3:])

execute("current_out_schema_only", schema_only=True, candidate=a.target / "out")
execute("control_comparison", clone("control_comparison"))
execute("control_schema_only", clone("control_schema_only"), schema_only=True)

d = clone("both_reference_receipts_empty")
for side in ("old", "new"):
    update_json(d / side, lambda j: j.update(ref_consumed_inputs={}))
execute("both_reference_receipts_empty", d)

d = clone("candidate_reference_receipt_empty")
update_json(d / "new", lambda j: j.update(ref_consumed_inputs={}))
execute("candidate_reference_receipt_empty", d)

d = clone("baseline_reference_receipt_empty")
update_json(d / "old", lambda j: j.update(ref_consumed_inputs={}))
execute("baseline_reference_receipt_empty", d)

d = clone("reference_receipt_string_missing_locator")
def missing_locator_string(j):
    r = j["ref_consumed_inputs"]
    r["half_cell"].pop("path")
    j["ref_consumed_inputs"] = json.dumps(r)
for side in ("old", "new"):
    update_json(d / side, missing_locator_string)
execute("reference_receipt_string_missing_locator", d)

d = clone("candidate_audit_empty_object", "control_matrix_complete")
# Supply an internally consistent, producer-shaped three-metric audit control
# on both sides before checking removal of the candidate's audit content.
audit = {metric: dict(n=50, n_finite=50, n_inf=0, n_nan=0, n_exception=0,
    raw_lower_half_mean=1.0, scale=1.0000000000000002,
    eps_rel=2.220446049250313e-16, equivalent_within_rel=True)
    for metric in ("pocv", "dvdq", "dqdv")}
for folder in (d / "old", d / "new"):
    art = artifact(folder)
    rd = csv.DictReader(io.StringIO(art.read_text()))
    rs, cols = list(rd), rd.fieldnames
    for r in rs:
        r.update(scale_seed="0", n_scale_samples="50",
                 scale_audit_target=json.dumps(audit), scale_audit_ref=json.dumps(audit))
        for side_name in ("target", "ref"):
            for metric in audit:
                r[f"scale_{metric}_{side_name}"] = "1.0000000000000002"
    buf = io.StringIO()
    wr = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    wr.writeheader()
    wr.writerows(rs)
    raw_control = buf.getvalue().encode()
    art.write_bytes(raw_control)
    sidecar = art.with_name(art.name + ".meta.json")
    m = json.loads(sidecar.read_text())
    m.update(sha256=hashlib.sha256(raw_control).hexdigest(), roster=S.body_roster(art.name, raw_control))
    sidecar.write_text(json.dumps(m), encoding="utf-8")
execute("complete_audit_control", d)
# Preserve the positive-control output separately from the changed-candidate run.
shutil.copytree(d / "new", d / "control.new")
(d / "stdout.txt").rename(d / "control.stdout.txt")
(d / "stderr.txt").rename(d / "control.stderr.txt")
p = artifact(d / "new")
reader = csv.DictReader(io.StringIO(p.read_text()))
rows, header = list(reader), reader.fieldnames
for row in rows:
    row["scale_audit_target"] = "{}"
    row["scale_audit_ref"] = "{}"
buffer = io.StringIO()
writer = csv.DictWriter(buffer, fieldnames=header, lineterminator="\n")
writer.writeheader()
writer.writerows(rows)
raw = buffer.getvalue().encode()
p.write_bytes(raw)
side = p.with_name(p.name + ".meta.json")
meta = json.loads(side.read_text())
meta.update(sha256=hashlib.sha256(raw).hexdigest(), roster=S.body_roster(p.name, raw))
side.write_text(json.dumps(meta), encoding="utf-8")
execute("candidate_audit_empty_object", d)

d = clone("bom_json_schema_only")
update_json(d / "new", lambda j: None, bom=True)
execute("bom_json_schema_only", d, schema_only=True)

d = clone("schema_only_missing_env_fields")
p = artifact(d / "new")
side = p.with_name(p.name + ".meta.json")
meta = json.loads(side.read_text())
meta["env"] = {"python": meta["env"]["python"]}
side.write_text(json.dumps(meta), encoding="utf-8")
execute("schema_only_missing_env_fields", d, schema_only=True)

(a.out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
for name, r in results.items():
    pr = r["promotion"] or {}
    print(json.dumps(dict(case=name, rc=r["rc"], promotion=pr.get("promotion_eligible"),
                         blocked_by=pr.get("blocked_by"), stderr=r["stderr_tail"]), ensure_ascii=False))
