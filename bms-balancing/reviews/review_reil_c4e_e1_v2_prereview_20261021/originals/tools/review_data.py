"""Reviewer-owned data checks only: no imports or execution of reviewed programs."""
import ast, hashlib, json, sys, zipfile, zlib, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source"
DOC = SRC / "bms-balancing/docs"
PRIOR = ROOT.parent / "reil_c4e_e1_prereview_20261015"
def digest(b): return hashlib.sha256(b).hexdigest()
def identity(p):
    b=p.read_bytes()
    return {"path":str(p), "bytes":len(b), "sha256":digest(b)}
def save(name,obj):
    p=ROOT/name
    if p.exists():
        assert load(p)==obj, 'Refuse to overwrite different review record: '+name
        return
    with p.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(obj,f,ensure_ascii=False,indent=2); f.write("\n")
def load(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def static():
    prov=load(ROOT/"CAPTURE_PROVENANCE.json")
    rows=[]
    for f in prov["files"]:
        p=SRC/f["path"]; b=p.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
        rows.append({**f,"bytes":len(b),"sha256":digest(b),"git_blob_verified":actual==f["git_blob_sha"]})
    assert all(x["git_blob_verified"] for x in rows)
    save("SOURCE_INDEX.json",{"commit":prov["commit"],"count":len(rows),"files":rows})
    inputs=[]; upload_matches=[]
    for name in ("REIL_C4E_E1_APPROVAL_REQUEST_v2_20261020.md","REIL_C4E_E1_PREREVIEW_SEND_v2_20261020.md"):
        p=Path("C:/Users/Administrator/Downloads")/name
        inputs.append(identity(p))
        upload_matches.append({"name":name,"match":p.read_bytes()==(DOC/name).read_bytes()})
    for name in ("CLAUDE_REPLY_KO.md","DECISION.json"):
        inputs.append(identity(PRIOR/name))
    src_list=load(SRC/"bms-balancing/evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json")
    module_matches=[]
    prior_rel=[*(src_list["files"]), "tests/test_reil_c4e.py","tests/test_reil_c4e_fix.py","evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json"]
    prior_matches=[]
    for rel in prior_rel:
        old=PRIOR/"source"/rel; new=SRC/"bms-balancing"/rel
        inputs.append(identity(old))
        prior_matches.append({"path":rel,"byte_equal":old.read_bytes()==new.read_bytes()})
    for rel,expect in src_list["files"].items():
        b=(SRC/"bms-balancing"/rel).read_bytes()
        module_matches.append({"path":rel,"match":len(b)==expect["bytes"] and digest(b)==expect["sha256"]})
    drafts=["REIL_C4E1_LAUNCHER_DRAFT_v2_20261020.py.txt","REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v2_20261020.py.txt","REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v2_20261020.py.txt","REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt"]
    trees={}
    for p in sorted(SRC.rglob("*")):
        if p.is_file() and (p.name.endswith(".py") or p.name in drafts):
            trees[p.relative_to(SRC).as_posix()]=ast.parse(p.read_text(encoding="utf-8-sig"),filename=p.name,feature_version=(3,11))
    funcs=lambda t:[n for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    ltree=trees["bms-balancing/docs/"+drafts[0]]
    stree=trees["bms-balancing/docs/"+drafts[1]]
    def literals(t):
        out={}
        def literal(n):
            if isinstance(n,ast.Name):
                if n.id not in out: raise ValueError(n.id)
                return out[n.id]
            if isinstance(n,ast.Dict): return {literal(k):literal(v) for k,v in zip(n.keys,n.values)}
            if isinstance(n,ast.Tuple): return tuple(literal(v) for v in n.elts)
            if isinstance(n,ast.List): return [literal(v) for v in n.elts]
            return ast.literal_eval(n)
        for n in t.body:
            if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
                try: out[n.targets[0].id]=literal(n.value)
                except (ValueError,TypeError): pass
        return out
    lc=literals(ltree); sc=literals(stree)
    signatures_equal={n.name:ast.dump(n.args) for n in funcs(ltree)}=={n.name:ast.dump(n.args) for n in funcs(stree)}
    skeleton_raise=all(isinstance(n.body[-1],ast.Raise) and isinstance(n.body[-1].exc,ast.Call) and isinstance(n.body[-1].exc.func,ast.Name) and n.body[-1].exc.func.id=="NotImplementedError" for n in funcs(stree))
    test_counts={p:len([n for n in funcs(t) if n.name.startswith("test_")]) for p,t in trees.items() if "/tests/" in p or "CONTROLS_DRAFT" in p}
    extra=[]
    for rel,e in lc["EXTRA_EXECUTED"].items():
        b=(SRC/rel).read_bytes()
        extra.append({"path":rel,"match":len(b)==e["bytes"] and digest(b)==e["sha256"]})
    seal=SRC/"bms-balancing/reil_c6_rebuild_20261013"
    man=(seal/"MANIFEST.json").read_bytes(); lock=(seal/"REIL_C6.lock.txt").read_bytes()
    bindings={
       "manifest_sha":digest(man)==lc["SEAL_MANIFEST_SHA256"],
       "manifest_lock_entry":json.loads(man)["REIL_C6.lock.txt"]==lc["C6_LOCK_SHA256"],
       "lock_sha":digest(lock)==lc["C6_LOCK_SHA256"],
       "lock_header_env_profile_sha":lc["EXTRA_EXECUTED"]["degradation-degeneracy/tools/env_profile.py"]["sha256"] in lock.decode().splitlines()[0],
    }
    result={"kind":"READ_ONLY_STATIC_DATA_CHECKS_NOT_FUNCTIONAL_TESTS","upload_matches_pinned_sources":upload_matches,"source_captures":len(rows),"all_git_blob_identities_match":True,"prior_source_comparisons":prior_matches,"five_source_manifest_matches":module_matches,"AST_python_3_11_grammar_files":len(trees),"launcher_top_level_functions":len(funcs(ltree)),"skeleton_top_level_functions":len(funcs(stree)),"launcher_skeleton_signatures_equal":signatures_equal,"skeleton_functions_end_NotImplementedError":skeleton_raise,"shared_literal_constants_equal":all(lc[k]==v for k,v in sc.items() if k in lc),"planned_test_function_counts":test_counts,"planned_GREEN_total":sum(test_counts.values()),"extra_executed_source_matches":extra,"seal_bindings":bindings,"target_imports":0,"functional_tests":0,"probe_runs":0,"git_fixture_runs":0,"numeric_work_budget":None,"scope":"Static source facts only, not acceptance of program behavior or Linux runtime."}
    assert all(x["match"] for x in upload_matches+module_matches+extra)
    assert all(x["byte_equal"] for x in prior_matches)
    assert all(bindings.values())
    save("STATIC_CHECKS.json",result)
    save("SELECTED_LOCAL_INPUTS_BEFORE_PACKAGE.json",{"phase":"After source reading/capture and review analysis; before review report/package creation. Not a pre-task snapshot.","count":len(inputs),"files":inputs})
    print(json.dumps(result,ensure_ascii=False,indent=2))
def package():
    exclude={"PACKAGE_MANIFEST.json","DELIVERY_RECEIPT.json","FINAL_PACKAGE_TOOL_RETURN.json","SELECTED_LOCAL_INPUTS_POST_PACKAGE.json","FINAL_CHECK.json"}
    paths=sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name not in exclude and p.suffix!=".zip")
    rows=[{"path":p.relative_to(ROOT).as_posix(),"bytes":p.stat().st_size,"sha256":digest(p.read_bytes())} for p in paths]
    manifest={"kind":"REVIEW_PACKAGE_MANIFEST","payload_count":len(rows),"files":rows}
    save("PACKAGE_MANIFEST.json",manifest)
    archive=ROOT/"REIL_C4E_E1_V2_PREREVIEW_20261021.zip"
    with zipfile.ZipFile(archive,"x",zipfile.ZIP_DEFLATED) as z:
        for p in paths+[ROOT/"PACKAGE_MANIFEST.json"]: z.write(p,p.relative_to(ROOT).as_posix())
    expected=rows+[{"path":"PACKAGE_MANIFEST.json",**{k:v for k,v in identity(ROOT/"PACKAGE_MANIFEST.json").items() if k!="path"}}]
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(expected)
        assert {x["path"] for x in expected}==set(z.namelist())
        assert len({x.casefold() for x in z.namelist()})==len(expected)
        for r in expected:
            n=r["path"]; assert not n.startswith("/") and ":" not in n and ".." not in Path(n).parts
            b=z.read(n)
            assert len(b)==r["bytes"] and digest(b)==r["sha256"]
            assert zlib.crc32(b)&0xffffffff==z.getinfo(n).CRC
    before=load(ROOT/"SELECTED_LOCAL_INPUTS_BEFORE_PACKAGE.json")
    after=[identity(Path(r["path"])) for r in before["files"]]
    assert after==before["files"]
    save("SELECTED_LOCAL_INPUTS_POST_PACKAGE.json",{"count":len(after),"all_match":True,"files":after,"scope":"Selected local uploaded/prior review files only; not remote working tree preservation."})
    receipt={"kind":"STATIC_PREREVIEW_DELIVERY_RECEIPT","recipient":None,"archive":identity(archive),"manifest":identity(ROOT/"PACKAGE_MANIFEST.json"),"payload_count":len(rows),"entries":len(rows)+1,"verification":"Exact set, relative paths, casefold uniqueness, sizes, decompressed SHA256 and independent CRC32 matched.","selected_local_preserved":len(after),"decision":"CHANGES_REQUIRED_NO_EXECUTION","target_imports":0,"functional_tests":0,"probe_runs":0,"COMSOL_runs":0,"execution_approved":False,"numeric_work_budget":None,"elapsed_claim":None,"boundary":"After ZIP readback and selected-input rehash; before receipt write/tool return."}
    save("DELIVERY_RECEIPT.json",receipt)
    print(json.dumps({"kind":"REVIEW_PACKAGE_READY","archive":identity(archive),"receipt":identity(ROOT/"DELIVERY_RECEIPT.json"),"payload_count":len(rows),"selected_preserved":len(after),"target_execution":0,"decision":"CHANGES_REQUIRED_NO_EXECUTION"},ensure_ascii=False))
if __name__=="__main__":
    {"static":static,"package":package}[sys.argv[1]]()
