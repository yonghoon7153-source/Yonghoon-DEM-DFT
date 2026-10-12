"""Read-only R7 scope/provenance probe. No solver or production launcher calls."""
from pathlib import Path
import ast
import decimal
import difflib
import gzip
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("\\\\?\\" + str(ROOT / "source"))
OLD = Path("\\\\?\\" + str(ROOT / 'baseline_r6' if (ROOT / 'baseline_r6').exists() else ROOT.parent / "gen2_network_reverify6_20261011"))
PIN = "3cedd40a5911d0606bf33ed2085d5cb93c4db2e0"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def tree(path):
    return ast.parse(path.read_text(encoding="utf-8"))


def assignment(path, name):
    node = next(n for n in tree(path).body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    # Selected literal tuple/dict registration assignment only; no module import.
    return eval(compile(ast.Expression(node.value), str(path), "eval"), {"__builtins__": {}, "dict": dict})


def function_asts(path):
    return {n.name: ast.dump(n, include_attributes=False) for n in tree(path).body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def chk_asts(path):
    return [ast.dump(n, include_attributes=False) for n in ast.walk(tree(path))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "chk"]


manifest = json.loads((ROOT / "source_manifest.json").read_text(encoding="utf-8"))
upstream = json.loads((ROOT / "tree.json").read_text(encoding="utf-8"))
up = {r["path"]: r for r in upstream["tree"] if r["type"] == "blob"}
bad = []
for row in manifest["files"]:
    data = (SRC / row["path"]).read_bytes()
    if not (digest(data) == row["sha256"] and blob(data) == row["sha"] == up[row["path"]]["sha"]
            and len(data) == row["bytes"] == up[row["path"]]["size"]):
        bad.append(row["path"])

runner = SRC / "scripts/run_network_194_parallel.py"
sealed = assignment(runner, "CODE_FILES")
handover = assignment(runner, "HANDOVER_FILES")
hashes = {p: digest((SRC / p).read_bytes()) for p in sealed}
old_hashes = {p: digest((OLD / "source" / p).read_bytes()) for p in sealed}
code_fp = digest(json.dumps(sorted(hashes.items()), separators=(",", ":")).encode())
fp_expected = "e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71"
hd = {p: {"current": digest((SRC / p).read_bytes()), "r6": digest((OLD / "source" / p).read_bytes())}
      for p in handover}

fix = json.loads((ROOT / "evidence/commit_ec9c51149.json").read_text(encoding="utf-8"))
comparison = json.loads((ROOT / "evidence/compare_r6_r7.json").read_text(encoding="utf-8"))
code_changed = [r["filename"] for r in comparison["files"] if r["filename"].startswith(("scripts/", "webapp/"))]
patch_scope = {}
for rel in ("scripts/g2_network_reread.py", "scripts/wsl_network_smoke.py"):
    a, b = ROOT / "parent" / rel, SRC / rel
    fa, fb = function_asts(a), function_asts(b)
    diff = list(difflib.unified_diff(a.read_text(encoding="utf-8").splitlines(), b.read_text(encoding="utf-8").splitlines()))
    fix_row = next(r for r in fix["files"] if r["filename"] == rel)
    patch_scope[rel] = {
        "added_lines": sum(l.startswith("+") and not l.startswith("+++") for l in diff),
        "deleted_lines": sum(l.startswith("-") and not l.startswith("---") for l in diff),
        "changed_functions": sorted(k for k in fa.keys() & fb.keys() if fa[k] != fb[k]),
        "added_functions": sorted(fb.keys() - fa.keys()),
        "removed_functions": sorted(fa.keys() - fb.keys()),
        "fix_blob_equals_review_pin": fix_row["sha"] == blob(b.read_bytes()),
        "chk_count_parent": len(chk_asts(a)), "chk_count_pin": len(chk_asts(b)),
        "all_chk_asts_identical": chk_asts(a) == chk_asts(b),
    }

registry = assignment(SRC / "scripts/g2_network_reread.py", "CASE15_NEGCTL")
case_dir = SRC / "docs/data/case15_corner_20261001"
readme = case_dir / "README.md"
readme_rows = {}
for line in readme.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^([0-9a-f]{64})\s+([\d,]+) B\s+(\S+)", line)
    if m:
        readme_rows[m[3]] = {"sha256": m[1], "bytes": int(m[2].replace(",", ""))}
raw = {}
for filename, expected in registry["raw_sha256"].items():
    path = case_dir / filename
    packed = not path.is_file()
    if packed:
        path = path.with_suffix(path.suffix + ".gz")
    size, h = 0, hashlib.sha256()
    with (gzip.open(path, "rb") if packed else path.open("rb")) as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            size += len(chunk)
            h.update(chunk)
    actual = h.hexdigest()
    raw[filename] = {"path": str(path.relative_to(SRC)), "uncompressed_bytes": size,
                     "actual_sha256": actual, "registry_sha256": expected,
                     "readme": readme_rows.get(filename),
                     "match": actual == expected == readme_rows[filename]["sha256"] and size == readme_rows[filename]["bytes"]}

# Parse the source contact dump directly without parser, solver, or shared verifier.
# c_cpl[22] and c_cpl[23] contain original area and overlap. Decimal performs the
# registered unit scaling and six-decimal display rounding independently.
contact_rows = 0
negative = []
with gzip.open(case_dir / "contact_v4_1710000.liggghts.gz", "rt", encoding="utf-8") as stream:
    for line in stream:
        if line.startswith("ITEM: ENTRIES"):
            columns = line[len("ITEM: ENTRIES"):].split()
            break
    indexes = [columns.index(k) for k in ("c_cpl[7]", "c_cpl[8]", "c_cpl[22]", "c_cpl[23]")]
    D = decimal.Decimal
    for line in stream:
        if not line.strip() or line.startswith("ITEM"):
            continue
        contact_rows += 1
        fields = line.split()
        a, b, area, delta = [fields[i] for i in indexes]
        if D(area) < 0:
            negative.append([int(D(a)), int(D(b)),
                             float((D(area) * 1000000).quantize(D("0.000001"))),
                             float((D(delta) * 1000).quantize(D("0.000001")))])

imported_dir = SRC / "docs/reviews/codex_gen2_network_reverify6_evidence_20261011/evidence"
imports = []
for path in sorted(imported_dir.glob("r6_s0b_*.input.json")):
    old = OLD / "evidence" / path.name
    imports.append({"name": path.name, "sha256": digest(path.read_bytes()),
                    "equals_r6_original_bytes": old.is_file() and path.read_bytes() == old.read_bytes()})

report = {
    "pin": PIN,
    "provenance": {"manifest_pin": manifest["pin"], "upstream_tree_sha": upstream["sha"],
                   "verified_files": len(manifest["files"]), "mismatches": bad,
                   "request_equals_pin_bytes": (ROOT / "submitted/request.md").read_bytes() == (SRC / "docs/reviews/codex_gen2_network_reverify7_request_20261011.md").read_bytes()},
    "scope": {"fix": fix["sha"], "parent": fix["parents"][0]["sha"],
              "fix_files": [{k: r[k] for k in ("filename", "status", "additions", "deletions")} for r in fix["files"]],
              "r6_to_r7_code_changed": code_changed, "patches": patch_scope},
    "sealed32": {"files": len(sealed), "code_fp": code_fp, "expected_code_fp_match": code_fp == fp_expected,
                 "changed_from_r6": [p for p in sealed if hashes[p] != old_hashes[p]], "hashes": hashes},
    "handover": hd,
    "raw_case15": raw,
    "negative_rows": {"source_contact_rows": contact_rows, "independent_decimal_rows": negative,
                      "registry_rows": registry["negative_rows_ref"],
                      "matches_registration": sorted(negative) == sorted(map(list, registry["negative_rows_ref"]))},
    "imported_regressions": imports,
    "limits": ["No solver, DEM, MPM, run194, selftest-real, or WSL run was executed by this probe.",
               "Full byte hashing of this review's four raw files is separate from S0b's 12-character report-prefix validation.",
               "Original experiment/run provenance beyond supplied bytes remains subject to README's author-statement limit.",
               "Supplemental20 and any 214-case release are excluded from this review."]
}
out = ROOT / "evidence/r7_contract.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"evidence": str(out), "verified_files": len(manifest["files"]), "bad_files": bad,
                  "code_fp": code_fp, "sealed_changed": report["sealed32"]["changed_from_r6"],
                  "raw_all_match": all(x["match"] for x in raw.values()), "negative_rows": negative,
                  "imported_inputs_unchanged": all(x["equals_r6_original_bytes"] for x in imports),
                  "producer_scope": patch_scope["scripts/wsl_network_smoke.py"]}, ensure_ascii=False))
