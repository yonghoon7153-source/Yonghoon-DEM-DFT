"""Reviewer-owned byte/JSON/AST inspection only. Never executes received source."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"
PRIOR = ROOT.parent / "reil_c4e_e1_v4_prereview_20261021" / "source"
DOC = "bms-balancing/docs/"
def h(b):
    return hashlib.sha256(b).hexdigest()
def ident(p):
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": h(b)}
def out(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
checks = []
def check(name, condition, details=None):
    checks.append({"name": name, "matched": bool(condition), "details": details})

meta = json.loads((ROOT / "CAPTURE_METADATA.json").read_text(encoding="utf-8"))
identities = []
trees = {}
functions = []
for entry in meta["files"]:
    rel = entry["path"]
    p = SRC / rel
    b = p.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(b)).encode("ascii") + b"\0" + b).hexdigest()
    check("GitHub blob byte identity " + rel, blob == entry["git_blob_sha1"])
    identities.append({**entry, **ident(p), "captured_git_blob_sha1": blob})
    if rel.endswith((".py", ".py.txt")):
        tree = ast.parse(b.decode("utf-8"), filename=rel)
        trees[rel] = tree
        functions.extend({"path": rel, "name": n.name, "line": n.lineno, "end_line": n.end_lineno}
                         for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
out("SOURCE_IDENTITIES.json", {"commit": meta["commit"], "files": identities})
out("FUNCTION_SPANS.json", functions)

names = {
"L": "REIL_C4E1_LAUNCHER_DRAFT_v5_20261027.py.txt",
"S": "REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v5_20261027.py.txt",
"LC": "REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v5_20261027.py.txt",
"RC": "REIL_C4E1_RUNNER_CONTROLS_DRAFT_v3_20261027.py.txt",
"R": "REIL_C4E1_STEP_RUNNER_DRAFT_v5_20261027.py.txt",
}
expected = {
"L": (51957, "2269d775f1701e2f657d386f42bc950d26a6b56bd37323611dd6ab4cc1a75396"),
"S": (13646, "e6f72de2245a41a4a80e0bb7adcc7734991f0b95fb1c1764ea6bfda579849182"),
"LC": (51121, "4720585c86f555bb0f9cfea3e12aab5b283f8ee4243a3ef257f77849759b777d"),
"RC": (36478, "ae42d8e8c0fb0c680d324348d2e1edc8f11865bd6bedea7cb0becf9b00fe6042"),
"R": (36189, "f6070f9776baa7dfc9b5e26ac5e6f378dd2969e7628566e5baa3c02685814a2a"),
}
# Exact author-declared SHA; no fixture or target behavior evaluated.
for k, (size, sha) in expected.items():
    check("draft seal " + k, ident(SRC / DOC / names[k]) == {"bytes": size, "sha256": sha})
check("approval request seal", h((SRC / DOC / "REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md").read_bytes()) ==
      "18db9f15cff07a0336d52bbc014f23759f82dc7fe24d0408870b3c0f746d5d69")

ts = {k: trees[DOC+n] for k,n in names.items()}
def defs(tree):
    return {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}
def lit_assign(tree, name):
    return next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
fixed = ast.literal_eval(lit_assign(ts["R"], "_FIXED"))
launch_slot = ast.literal_eval(lit_assign(ts["R"], "LAUNCH"))
target_node = lit_assign(ts["R"], "TARGETS")
targets = [launch_slot if isinstance(n, ast.Name) and n.id == "LAUNCH" else ast.literal_eval(n)
           for n in target_node.elts]
check("TARGETS unique 14 and fixed 13", len(targets) == len(set(targets)) == 14 and len(fixed) == 13 and set(targets) == set(fixed) | {launch_slot})
copy_map = {
 "bms-balancing/tests/test_reil_c4e1_launch.py": DOC+names["LC"],
 "bms-balancing/tests/test_reil_c4e1_runner.py": DOC+names["RC"],
}
for path, value in fixed.items():
    check("EXPECT fixed bytes " + path, ident(SRC / copy_map.get(path, path)) == value)
for key, k in [("SKELETON","S"), ("IMPL","L")]:
    check("EXPECT " + key, ast.literal_eval(lit_assign(ts["R"],key)) == ident(SRC / DOC / names[k]))
expect_dump = ast.dump(lit_assign(ts["R"], "EXPECT"))
check("EXPECT phase mapping", expect_dump.count("id='SKELETON'") == 2 and expect_dump.count("id='IMPL'") == 1
      and expect_dump.count("id='_FIXED'") == 3)
L, S = defs(ts["L"]), defs(ts["S"])
check("35 skeleton signatures", len(L) == len(S) == 35 and list(L) == list(S)
      and all(ast.dump(L[n].args) == ast.dump(S[n].args) for n in L))
check("35 skeleton NotImplementedError bodies", all(len(n.body) == 1 and isinstance(n.body[0],ast.Raise)
      and isinstance(n.body[0].exc,ast.Call) and isinstance(n.body[0].exc.func,ast.Name)
      and n.body[0].exc.func.id == "NotImplementedError"
      and ast.literal_eval(n.body[0].exc.args[0]).startswith("E1-0 RED 골격") for n in S.values()))
def structural(tree):
    return [ast.dump(n) for n in tree.body[1:] if not isinstance(n,ast.FunctionDef)]
check("skeleton imports constants main same", structural(ts["L"]) == structural(ts["S"]))
for key, fun in [("L","git_run"), ("R","git")]:
    node = defs(ts[key])[fun]
    calls = [n for n in ast.walk(node) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
             and isinstance(n.func.value,ast.Name) and n.func.value.id=="subprocess" and n.func.attr=="run"]
    kw = {k.arg:ast.literal_eval(k.value) for k in calls[0].keywords if k.arg in ("text","encoding","errors")} if len(calls)==1 else {}
    check("wrapper literal decoding "+key, len(calls)==1 and kw == {"text":True,"encoding":"utf-8","errors":"replace"}, {"line":node.lineno,"keywords":kw})
counts = {}
for rel in [DOC+names["LC"], DOC+names["RC"], "bms-balancing/tests/test_reil_c4e.py", "bms-balancing/tests/test_reil_c4e_fix.py"]:
    tree = trees[rel]
    cases = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith("test_")]
    counts[rel] = len(cases)
    check("no parametrize "+rel, not any(isinstance(n,ast.Attribute) and n.attr=="parametrize" for n in ast.walk(tree)))
check("static declared case counts 27 11 21 6", list(counts.values()) == [27,11,21,6])
for key, alias, target in [("LC","L","L"), ("RC","R","R")]:
    attrs = sorted({n.attr for n in ast.walk(ts[key]) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id==alias})
    defined = {n.name for n in ts[target].body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    for n in ts[target].body:
        if isinstance(n,ast.Assign):
            defined.update(t.id for t in n.targets if isinstance(t,ast.Name))
        elif isinstance(n,ast.Import):
            defined.update(a.asname or a.name.split('.')[0] for a in n.names)
        elif isinstance(n,ast.ImportFrom):
            defined.update(a.asname or a.name for a in n.names)
    check("control target members "+alias, set(attrs) <= defined | {"__file__"}, {"count":len(attrs),"names":attrs})
# Compare preserved references to the prior reviewer snapshots, not the remote machine.
unchanged = []
for entry in meta["files"]:
    rel = entry["path"]
    if (PRIOR / rel).is_file():
        same = (PRIOR / rel).read_bytes() == (SRC / rel).read_bytes()
        unchanged.append({"path":rel,"identical":same})
check("13 unchanged references", len(unchanged)==13 and all(r["identical"] for r in unchanged), unchanged)
old_names = {
"L":"REIL_C4E1_LAUNCHER_DRAFT_v4_20261021.py.txt",
"S":"REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v4_20261021.py.txt",
"LC":"REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v4_20261021.py.txt",
"RC":"REIL_C4E1_RUNNER_CONTROLS_DRAFT_v2_20261021.py.txt",
"R":"REIL_C4E1_STEP_RUNNER_DRAFT_v4_20261021.py.txt",
}
diffs = []
for key, old in old_names.items():
    diffs.extend(difflib.unified_diff((PRIOR/DOC/old).read_text(encoding="utf-8").splitlines(True),
                 (SRC/DOC/names[key]).read_text(encoding="utf-8").splitlines(True),
                 fromfile="v4/"+old, tofile="v5/"+names[key]))
(ROOT/"DRAFT_DIFFS.txt").write_text("".join(diffs),encoding="utf-8")
result = {"kind":"REVIEWER_STATIC_DATA_AUDIT","source_count":len(identities),
          "ast_parsed_files":len(trees),"function_spans":len(functions),
          "conditions":len(checks),"matched":sum(c["matched"] for c in checks),
          "case_counts":counts,"checks":checks,
          "received_program_imports_or_calls":0,"functional_tests":0,"git_fixture_commands":0,
          "limitation":"Source identity and AST/text checks only; not a test result or remote execution/environment audit."}
out("STATIC_AUDIT.json",result)
print(json.dumps({k:v for k,v in result.items() if k not in ("checks","case_counts")},ensure_ascii=False))
print(json.dumps({"unmatched":[c for c in checks if not c["matched"]]},ensure_ascii=False))

