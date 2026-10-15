"""Run submitted A4 sections unchanged with a verified snapshot Git adapter.

Only review evidence and review/tmp are written; source/base remain read-only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
SOURCE = ROOT / "source"
BASE = ROOT / "base"
BASE_PIN = "0c557e72aaffdf6cfd033c0667c643de4501c5b1"
SOURCE_PIN = "9e3ef54ca228111360bfe5f6d9dad4ebe26d54af"
TMP = ROOT / "tmp"
EVIDENCE = ROOT / "evidence"
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUTF8"] = "1"
os.environ["TMP"] = os.environ["TEMP"] = str(TMP)
deps = [WORK / "lhs_coverage_review_20260930/deps", WORK / "gen2_network_reverify3_20261007/deps"]
os.environ["PYTHONPATH"] = os.pathsep.join(map(str, deps))
sys.path[:0] = [str(SOURCE / "scripts"), str(SOURCE / "webapp"), *map(str, deps)]
sys.dont_write_bytecode = True
tempfile.tempdir = str(TMP)

ADAPTER_CALLS = []
MANIFESTS = {}
for label, expected in (("base", BASE_PIN), ("source", SOURCE_PIN)):
    manifest = json.loads((ROOT / f"{label}_manifest.json").read_text(encoding="utf-8"))
    if manifest["pin"] != expected:
        raise RuntimeError(f"Wrong {label} manifest pin")
    MANIFESTS[label] = {row["path"]: row for row in manifest["files"]}


def verified_bytes(label, rel):
    rel = rel.replace("\\", "/")
    row = MANIFESTS[label].get(rel)
    if row is None:
        raise RuntimeError(f"Unmanifested input {label}/{rel}")
    p = ROOT / label / rel
    p.resolve().relative_to((ROOT / label).resolve())
    data = p.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if sha != row["sha256"] or len(data) != row["bytes"]:
        raise RuntimeError(f"Manifest hash/size mismatch {label}/{rel}")
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if blob != row["git_blob"]:
        raise RuntimeError(f"Git blob hash mismatch {label}/{rel}")
    return data


def git_bytes_adapter(*args):
    if args[0] == "show" and len(args) == 2:
        pin, rel = args[1].split(":", 1)
        if pin != BASE_PIN:
            raise RuntimeError(f"Unexpected show pin {pin}")
        data = verified_bytes("base", rel)
    elif args == ("diff", "--name-only", BASE_PIN, "--", "scripts", "webapp"):
        names = sorted({name for manifest in MANIFESTS.values() for name in manifest
                        if name.startswith(("scripts/", "webapp/"))})
        changed = []
        for name in names:
            b = verified_bytes("base", name) if name in MANIFESTS["base"] else None
            s = verified_bytes("source", name) if name in MANIFESTS["source"] else None
            if b != s:
                changed.append(name)
        data = ("\n".join(changed) + "\n").encode()
    elif args == ("archive", "--format=tar", BASE_PIN, "webapp", "scripts"):
        # Archive exactly the manifested tracked scripts/webapp bytes, not temporary outputs.
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tf:
            for name in sorted(MANIFESTS["base"]):
                if not name.startswith(("scripts/", "webapp/")):
                    continue
                content = verified_bytes("base", name)
                member = tarfile.TarInfo(name)
                member.size = len(content)
                tf.addfile(member, io.BytesIO(content))
        data = buf.getvalue()
    else:
        raise RuntimeError(f"Unsupported Git adapter operation {args!r}")
    ADAPTER_CALLS.append({"args": args, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return data


def main():
    started = time.time()
    original = SOURCE / "docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.py"
    original_bytes = verified_bytes("source", str(original.relative_to(SOURCE)).replace("\\", "/"))
    spec = importlib.util.spec_from_file_location("submitted_l214_a4", original)
    a4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a4)
    a4.git_bytes = git_bytes_adapter
    changed = a4.git_bytes("diff", "--name-only", BASE_PIN, "--", "scripts", "webapp").decode().splitlines()
    import network_conductivity as nc_new
    import tau_flux as tf_new
    import lhs_release_build as lrb_new
    all_inputs = [
        "docs/data/real14_reference_20260928/atom_2060000.liggghts.gz",
        "docs/data/real14_reference_20260928/contact_2060000.liggghts.gz",
        "docs/data/case15_corner_20261001/atom_v4_1710000.liggghts.gz",
        "docs/data/case15_corner_20261001/contact_v4_1710000.liggghts.gz",
        "docs/data/case15_corner_20261001/mesh_v4_1710000.stl",
        "docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz",
        "docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/lhs_handover_v12_20261006.csv",
        "docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/lhsx_handover_v12_20261006.csv",
        "docs/reviews/codex_lhs214_failures_review_evidence_20261014/submitted/lhs214_run_evidence_1014_1520.tgz"]
    inputs = []
    for rel in all_inputs:
        data = verified_bytes("source", rel)
        inputs.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    section_time = {}
    # Original functions keep all numerical expressions, comparison logic, and W subprocesses.
    with tempfile.TemporaryDirectory(prefix="numeric_a4_", dir=TMP) as tmp:
        nc_old = a4.load_base(BASE_PIN, "scripts/network_conductivity.py", "nc_base", tmp)
        tf_old = a4.load_base(BASE_PIN, "scripts/tau_flux.py", "tf_base", tmp)
        tf_old._nc_mod = lambda: nc_old  # Identical binding performed by submitted main().
        lrb_old = a4.load_base(BASE_PIN, "scripts/lhs_release_build.py", "lrb_base", tmp)
        print("A4 N started: submitted section_n, real_14 + case15 included", flush=True)
        t = time.time()
        rows_n, added, beds = a4.section_n(nc_new, nc_old, False)
        section_time["N"] = time.time() - t
        print(f"A4 N complete: {sum(r['identical'] for r in rows_n)}/{len(rows_n)}", flush=True)
        t = time.time()
        rows_t = a4.section_t(tf_new, tf_old, beds, tmp)
        section_time["T"] = time.time() - t
        print(f"A4 T complete: {sum(r['identical'] for r in rows_t)}/{len(rows_t)}", flush=True)
        t = time.time()
        rows_r = a4.section_r(lrb_new, lrb_old)
        section_time["R"] = time.time() - t
        print(f"A4 R complete: {sum(r['identical'] for r in rows_r)}/{len(rows_r)}", flush=True)
        t = time.time()
        rows_w, w_changes = a4.section_w(BASE_PIN, tmp)
        section_time["W"] = time.time() - t
        print(f"A4 W complete: {sum(r['identical'] for r in rows_w)}/{len(rows_w)}", flush=True)
    rows = rows_n + rows_t + rows_r + rows_w
    execution_errors = [{"case": label, "mode": mode, "error": value["__error__"]}
                        for (label, mode), value in beds.items()
                        if isinstance(value, dict) and "__error__" in value]
    ok = (all(r["identical"] for r in rows)
          and all(not any(k in x["base_has"] for k in a4.L214_ADDED) for x in added)
          and all(r["guard_fields"] == 0 for r in rows_n))
    result = {"base": BASE_PIN, "source": SOURCE_PIN, "submitted_script_sha256": hashlib.sha256(original_bytes).hexdigest(),
              "changed_files": changed, "adapter": {"description": "Only a4.git_bytes replaced: git show/diff/archive -> SHA256 + Git blob verified snapshots; all section functions and W_PROBE/run_probe unchanged", "calls": ADAPTER_CALLS},
              "environment": {"python": sys.version, "PYTHONPATH": os.environ["PYTHONPATH"], "TMP": str(TMP), "threads": 1},
              "input_hashes": inputs, "rows": rows, "added_keys": added, "w_changes": w_changes, "ok": ok,
              "producer_execution_errors": execution_errors,
              "section_seconds": section_time, "elapsed_seconds": time.time() - started}
    out = EVIDENCE / "a4_independent.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"A4 {'PASS' if ok else 'FAIL'} {sum(r['identical'] for r in rows)}/{len(rows)}, evidence={out}, elapsed={result['elapsed_seconds']:.1f}s", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
