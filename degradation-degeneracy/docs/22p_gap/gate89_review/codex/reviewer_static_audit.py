import ast, copy, difflib, hashlib, json, pathlib, re
root = pathlib.Path(__file__).parent
s = json.loads((root / "RECEIVED_SNAPSHOT.json").read_text(encoding="utf-8"))
oldscope = json.loads((root / "PRIOR_RUN_SCOPE_SNAPSHOT.json").read_text(encoding="utf-8"))
old = json.loads((root / "PRIOR_RECEIVED_SNAPSHOT.json").read_text(encoding="utf-8"))
P = "degradation-degeneracy/"
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
def diff(a,b):
    return "\n".join(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile="gate88",tofile="gate89",lineterm=""))
checks = []
for path,d in s["files"].items():
    b = d["content"].encode("utf-8")
    checks.append({"path":path,"bytes":len(b),"sha256":sha(b),"git_blob_match":blob(b)==d["sha"]})
by_path = {x["path"]:x for x in checks}
logchecks=[]
for e in s["evidence_manifest"]:
    path=P+"docs/22p_gap/gate89_evidence/"+e["name"]
    got=by_path[path]
    logchecks.append(dict(e,size_match=e["bytes"]==got["bytes"],sha_match=e["sha256"]==got["sha256"]))
e=s["supplement"]; got=by_path[e["path"]]
supplement=dict(e,size_match=e["bytes"]==got["bytes"],sha_match=e["sha256"]==got["sha256"])
entries={e["path"]:e for e in s["scope_entries"]}
old_entries={e["path"]:e for e in oldscope["entries"]}
scope_files=dict(oldscope["files"])
scope_files[P+"tools/preserve.py"]=s["files"][P+"tools/preserve.py"]
scope_ids=[]; h=hashlib.sha256()
for path in sorted(entries):
    d=scope_files[path]; b=d["content"].encode("utf-8")
    h.update(path.removeprefix(P).encode()); h.update(b)
    scope_ids.append({"path":path,"bytes":len(b),"sha256":sha(b),"git_blob":blob(b),
        "blob_tree_match":blob(b)==entries[path]["sha"]==d["sha"],
        "unchanged_since_gate88":entries[path]["sha"]==old_entries.get(path,{}).get("sha")})
a=old["files"][P+"tools/preserve.py"]["content"]
b=s["files"][P+"tools/preserve.py"]["content"]
ta,tb=ast.parse(a),ast.parse(b)
fa={n.name:n for n in ta.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
fb={n.name:n for n in tb.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
changed=[name for name in sorted(set(fa)|set(fb)) if name not in fa or name not in fb or ast.dump(fa[name])!=ast.dump(fb[name])]
new_calls=[n for n in ast.walk(fb["finalize_leg"]) if isinstance(n,ast.Call) and ast.unparse(n.func)=="_assert_external_input_binding"]
target=new_calls[0]
parent={}
for n in ast.walk(tb):
    for c in ast.iter_child_nodes(n): parent[c]=n
ancestors=[]; n=target
while n in parent:
    n=parent[n]
    if isinstance(n,ast.If): ancestors.append({"kind":"if","line":n.lineno,"test":ast.unparse(n.test)})
    if isinstance(n,ast.With): ancestors.append({"kind":"with","line":n.lineno,"items":[ast.unparse(x.context_expr) for x in n.items]})
class RemoveNewCall(ast.NodeTransformer):
    def visit_Expr(self,node):
        if isinstance(node.value,ast.Call) and node.value.lineno==target.lineno and ast.unparse(node.value.func)=="_assert_external_input_binding":
            return None
        return self.generic_visit(node)
stripped=RemoveNewCall().visit(copy.deepcopy(tb))
ast_review={"top_level_function_set_unchanged":set(fa)==set(fb),"changed_functions":changed,
 "new_call_count_in_finalizer":len(new_calls),"new_call_line":target.lineno,"new_call_expression":ast.unparse(target),
 "ancestors":ancestors,"entire_module_ast_after_removing_call_equals_prior":ast.dump(ta)==ast.dump(stripped)}
receipt_checks={}
for leg in ("paired_fixed5_v4","grid_fit_v5"):
    path=P+"docs/22p_gap/receipts/"+leg+".validate.yaml"
    hist=P+"docs/22p_gap/receipts/history/"+leg+".validate.7dd546baaee9e823.yaml"
    before=old["files"][path]["content"]; after=s["files"][path]["content"]
    receipt_checks[leg]={"history_byte_identical_to_prior_current":before==s["files"][hist]["content"],
                         "unified_diff":diff(before,after)}
lp=P+"docs/22p_gap/LEG_PRESERVATION.yaml"
mp=P+"docs/22p_gap/mutation_replay.py"
gp=P+"tests/test_gate88_fit_only_lifecycle.py"
logs={}
for name in ("10_full_pytest_66129fc6a_2139passed.log","11_smoke_66129fc6a_rc0.log","12_full_replay_66129fc6a_397_of_397_rc0.log","14_docs_lint_send_8113f12bd_358passed.log"):
    text=s["files"][P+"docs/22p_gap/gate89_evidence/"+name]["content"]
    lines=text.splitlines()
    logs[name]={"boundary_lines":[line for line in lines if re.search(r"HEAD|dirty|status|start|end|rc[ =:]|passed|xfailed|scenario|executable|declared|^ran|preimage|^site",line,re.I)],
        "killed_lines":sum(line.startswith("물었다") for line in lines),
        "declared_lines":sum(line.startswith("신고") for line in lines),
        "unexpected_outcome_lines":[line for line in lines if "★안 물었다" in line or "★실행오류" in line]}
frozen=s["frozen_spec"]; now=s["files"][P+"docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md"]
out={"method":"Reviewer-owned standard-library byte/hash/AST/text inspection only. No received modules imported, project tests, fits, smoke, restore, mutation replay, or COMSOL executed.",
 "received_file_count":len(checks),"file_checks":checks,
 "all_git_blobs_match":all(x["git_blob_match"] for x in checks),
 "log_checks":logchecks,"all_15_manifest_log_size_sha_match":all(x["size_match"] and x["sha_match"] for x in logchecks),
 "supplemental_send_log":supplement,
 "run_scope":{"count":len(scope_ids),"path_set_unchanged":set(entries)==set(old_entries),"digest":h.hexdigest()[:16],
 "sha256_full":h.hexdigest(),"all_blobs_match":all(x["blob_tree_match"] for x in scope_ids),
 "changed":[x["path"] for x in scope_ids if not x["unchanged_since_gate88"]],"files":scope_ids},
 "production_diff":diff(a,b),"ast_review":ast_review,
 "gate88_tests_byte_identical":old["files"][gp]["content"]==s["files"][gp]["content"],
 "frozen_spec_byte_identical":frozen["content"]==now["content"] and frozen["sha"]==now["sha"],
 "receipt_checks":receipt_checks,"ledger_diff":diff(old["files"][lp]["content"],s["files"][lp]["content"]),
 "mutation_registry_diff":diff(old["files"][mp]["content"],s["files"][mp]["content"]),
 "final_log_observations":logs,
 "reviewer_program_executions":{"received_source":0,"project_tests":0,"mutation_replay":0,"receipt_regeneration":0,"native_or_comsol":0}}
out["integrity_and_ast_checks_pass"]=all([out["all_git_blobs_match"],out["all_15_manifest_log_size_sha_match"],supplement["size_match"],supplement["sha_match"],out["run_scope"]["path_set_unchanged"],out["run_scope"]["all_blobs_match"],out["run_scope"]["digest"]=="803e2b7781cbc9cd",out["gate88_tests_byte_identical"],out["frozen_spec_byte_identical"],ast_review["entire_module_ast_after_removing_call_equals_prior"],all(x["history_byte_identical_to_prior_current"] for x in receipt_checks.values())])
print(json.dumps(out,ensure_ascii=False))
