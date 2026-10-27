"""Reviewer-owned static data checks. Never imports or executes received sources."""
import ast
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source"
META = json.loads((ROOT / "CAPTURE_METADATA.json").read_text(encoding="utf-8"))
DOCS = "bms-balancing/docs/"
NAMES = {
    "launcher": "REIL_C4E1_LAUNCHER_DRAFT_v4_20261021.py.txt",
    "skeleton": "REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v4_20261021.py.txt",
    "launcher_tests": "REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v4_20261021.py.txt",
    "runner_tests": "REIL_C4E1_RUNNER_CONTROLS_DRAFT_v2_20261021.py.txt",
    "runner": "REIL_C4E1_STEP_RUNNER_DRAFT_v4_20261021.py.txt",
}
checks = []
def check(name, condition, detail=None):
    checks.append({"name": name, "matched": bool(condition), "detail": detail})
def ident(p):
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def save(name, obj):
    p = ROOT / name
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with p.open("xb") as f:
        f.write(raw)
def resolve(node, known):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return known[node.id]
    if isinstance(node, (ast.Tuple, ast.List)):
        vals = [resolve(x, known) for x in node.elts]
        return tuple(vals) if isinstance(node, ast.Tuple) else vals
    if isinstance(node, ast.Dict):
        out = {}
        for k, v in zip(node.keys, node.values):
            if k is None:
                out.update(resolve(v, known))
            else:
                out[resolve(k, known)] = resolve(v, known)
        return out
    raise ValueError(type(node).__name__)
def literals(tree):
    known = {}
    for n in tree.body:
        if isinstance(n, ast.Assign):
            try:
                value = resolve(n.value, known)
            except (KeyError, ValueError, TypeError):
                continue
            for t in n.targets:
                if isinstance(t, ast.Name):
                    known[t.id] = value
    return known

sources = []
trees = {}
for row in META["files"]:
    path = row["path"]
    b = (SRC / path).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
    check("git_blob:" + path, blob == row["git_blob_sha1"])
    sources.append({**row, **ident(SRC / path), "computed_git_blob_sha1": blob})
    if path.endswith((".py", ".py.txt")):
        trees[path] = ast.parse(b.decode("utf-8"), filename=path)
check("capture_count", len(sources) == 21, len(sources))
uploads = []
for n in ("REIL_C4E_E1_APPROVAL_REQUEST_v4_20261021.md", "REIL_C4E_E1_PREREVIEW_SEND_v4_20261021.md"):
    p = Path("C:/Users/Administrator/Downloads") / n
    check("uploaded_equals_pinned:" + n, p.read_bytes() == (SRC / DOCS / n).read_bytes())
    uploads.append({"path": str(p), **ident(p)})

lt = trees[DOCS + NAMES["launcher"]]
st = trees[DOCS + NAMES["skeleton"]]
rt = trees[DOCS + NAMES["runner"]]
lf = {n.name: n for n in lt.body if isinstance(n, ast.FunctionDef)}
sf = {n.name: n for n in st.body if isinstance(n, ast.FunctionDef)}
check("launcher_skeleton_function_set", set(lf) == set(sf), len(lf))
check("launcher_skeleton_signatures", all(ast.dump(lf[k].args) == ast.dump(sf[k].args) for k in lf))
check("skeleton_all_functions_raise_NotImplementedError", all(
    isinstance(n.body[-1], ast.Raise) and isinstance(n.body[-1].exc, ast.Call)
    and isinstance(n.body[-1].exc.func, ast.Name) and n.body[-1].exc.func.id == "NotImplementedError"
    for n in sf.values()))
def header(tree):
    return [ast.dump(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign))]
check("launcher_skeleton_imports_constants", header(lt) == header(st))

rl = literals(rt)
mapping = {
    "bms-balancing/tests/test_reil_c4e1_launch.py": DOCS + NAMES["launcher_tests"],
    "bms-balancing/tests/test_reil_c4e1_runner.py": DOCS + NAMES["runner_tests"],
}
for stage, expected in rl["EXPECT"].items():
    check("targets_exact:" + stage, set(expected) == set(rl["TARGETS"]) and len(expected) == 14)
    for path, exp in expected.items():
        captured = mapping.get(path, path)
        if path == rl["LAUNCH"]:
            captured = DOCS + NAMES["launcher" if stage == "03_green" else "skeleton"]
        check("expected_identity:" + stage + ":" + path, ident(SRC / captured) == exp)
check("expect_only_launcher_varies", all(rl["EXPECT"]["01_red_launcher"][p] == rl["EXPECT"]["02_red_runner"][p] == rl["EXPECT"]["03_green"][p]
                                       for p in rl["TARGETS"] if p != rl["LAUNCH"]))

test_paths = [("baseline", "bms-balancing/tests/test_reil_c4e.py", 21), ("fix", "bms-balancing/tests/test_reil_c4e_fix.py", 6),
              ("launcher", DOCS + NAMES["launcher_tests"], 27), ("runner", DOCS + NAMES["runner_tests"], 11)]
test_counts = {}
for label, path, expected in test_paths:
    tests = [n for n in trees[path].body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    test_counts[label] = len(tests)
    check("test_function_count:" + label, len(tests) == expected)
    check("test_no_decorators:" + label, all(not n.decorator_list for n in tests))
check("planned_green_count_65", sum(test_counts.values()) == 65)
check("planned_new_controls_38", test_counts["launcher"] + test_counts["runner"] == 38)

sl = json.loads((SRC / "bms-balancing/evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json").read_text(encoding="utf-8"))
for path, exp in sl["files"].items():
    check("five_module_source_binding:" + path, ident(SRC / sl["base"] / path) == exp)
seal = SRC / "bms-balancing/reil_c6_rebuild_20261013"
manifest = json.loads((seal / "MANIFEST.json").read_text(encoding="utf-8"))
check("seal_manifest_fixed_hash", ident(seal / "MANIFEST.json")["sha256"] == "4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc")
check("manifest_lock_binding", ident(seal / "REIL_C6.lock.txt")["sha256"] == manifest["REIL_C6.lock.txt"])
check("lock_env_profile_header", ident(SRC / "degradation-degeneracy/tools/env_profile.py")["sha256"] in (seal / "REIL_C6.lock.txt").read_text(encoding="utf-8").splitlines()[0])
prior = ROOT.parent / "reil_c4e_e1_v3_prereview_20261021" / "source"
same_prior = []
for row in sources:
    p = prior / row["path"]
    if p.is_file():
        same = ident(p) == {"bytes": row["bytes"], "sha256": row["sha256"]}
        check("prior_v3_reference_unchanged:" + row["path"], same)
        same_prior.append(row["path"])

spans = []
for kind in NAMES:
    path = DOCS + NAMES[kind]
    raw = (SRC / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    for n in trees[path].body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            begin = sum(map(len, lines[:n.lineno - 1]))
            end = sum(map(len, lines[:n.end_lineno]))
            spans.append({"path": path, "name": n.name, "line_start": n.lineno, "line_end": n.end_lineno,
                          "byte_start_0": begin, "byte_end_exclusive": end,
                          "sha256": hashlib.sha256(raw[begin:end]).hexdigest()})
result = {"kind": "REVIEWER_STATIC_DATA_CHECKS_NOT_TARGET_TESTS", "utc": datetime.now(timezone.utc).isoformat(),
          "commit": META["ref"], "checks": checks, "all_matched": all(c["matched"] for c in checks),
          "source_count": len(sources), "ast_parsed_source_count": len(trees), "function_class_spans": len(spans),
          "test_function_counts": test_counts, "same_prior_reference_count": len(same_prior),
          "target_imports": 0, "target_calls": 0, "target_tests": 0, "git_fixture_runs": 0,
          "interpretation": "Identity/AST/data checks only. Neither functional PASS nor execution approval."}
save("SOURCE_IDENTITIES.json", {"commit": META["ref"], "files": sources, "uploaded_files": uploads})
save("FUNCTION_SPANS.json", {"scope": "Top-level functions/classes of five v4 drafts, including line endings; no execution", "spans": spans})
save("STATIC_DATA_CHECKS.json", result)
selected = uploads + [{"path": str(SRC / r["path"]), "bytes": r["bytes"], "sha256": r["sha256"]} for r in sources]
save("SELECTED_REVIEW_INPUTS_BEFORE.json", {"utc": datetime.now(timezone.utc).isoformat(), "count": len(selected),
     "boundary": "After read/static data analysis; before review prose and packaging. Local uploads/captures only, not original Linux or whole-PC preservation.",
     "files": selected})
print(json.dumps({"all_matched": result["all_matched"], "conditions": len(checks), "mismatches": [c for c in checks if not c["matched"]],
                  "source_count": len(sources), "ast_sources": len(trees), "spans": len(spans), "test_counts": test_counts,
                  "same_prior_reference_count": len(same_prior), "target_tests": 0}, ensure_ascii=False))
