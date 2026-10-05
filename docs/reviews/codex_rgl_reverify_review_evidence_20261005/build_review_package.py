"""Validate independent evidence and package only this review's selected outputs."""
from pathlib import Path, PurePosixPath
import hashlib,json,math,re,sys,zipfile
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
def read(rel):return json.loads((R/rel).read_text(encoding="utf8"))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def emit(rel,obj):
    (R/rel).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf8")
PIN="bf4fb6aee0b388375ddf65694ac405e63e0e381c"
manifest=read("source_manifest.json")
assert manifest["commit"]==PIN
assert len(manifest["files"])==432
for x in manifest["files"]:
    p=R/"source"/x["path"]; b=p.read_bytes()
    assert x["verified"] and digest(p)==x["sha256"]
    assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==x["expected"]

# Preserve intermediate records but explicitly identify the final record for every job.
final={}
for f in ("baseline_all.json","baseline_chain_lhs_rint_labels_group.json","baseline_lhs_group.json","baseline_lhs.json"):
    rows=read("evidence/"+f)
    if isinstance(rows,dict):rows=[rows]
    for x in rows:final[x["name"]]={**x,"record_source":"evidence/"+f}
assert len(final)==18
for n,x in final.items():assert x["rc"]==(1 if n=="lw" else 0),(n,x["rc"])
final["lw"]["limitation"]="68/69 executed assertions; real14 fixture group unavailable; not certified as 76/76."
final["boundary"]["limitation"]="8/8; git-based ninth comparison skipped; independently reproduced by raw18."
for n,x in final.items():
    x["log"]="evidence/"+n+".log"
    assert (R/x["log"]).is_file()
    x["log_sha256"]=digest(R/x["log"])
emit("evidence/final_test_summary.json",dict(
    commit=PIN,order="Later named baseline records supersede earlier missing-fixture attempts",
    results=list(final.values()),full_check_all_executed=False,
    labels13_log="evidence_g4/labels.stdout.txt",
    limitations=["No WSL/real14/194-production execution or resealing","General Stage E numerical step stubbed only in the explicitly marked general-helper probe"]))

network=read("evidence/network_adversarial.json"); cases={x["name"]:x for x in network}
assert len(network)==12 and len(cases)==12
assert cases["positive"]["status"]=="done" and cases["positive"]["tau"]["ion_net_status_hertz"]=="OK"
assert cases["no_through"]["status"]=="done" and cases["no_through"]["tau"]["ion_net_status_hertz"]=="NOT_PERCOLATING"
assert cases["solver_failed_stop"]["status"]=="failed"
assert cases["solver_failed_general"]["status"]=="done" and cases["solver_failed_general"]["stage_e_stub"]
for n in ("legitimate_band","band_ratio_missing","band_ratio_nan","band_ratio_negative","band_fraction_above1"):
    assert cases[n]["status"]=="done" and cases[n]["tau"]["ion_net_status_hertz"]=="BAND_FALLBACK"
a,b=cases["positive"],cases["ratio_times4"]
assert b["status"]=="done"
assert b["hertz"]["sigma_full"]==4*a["hertz"]["sigma_full"]
assert b["grade_tau2"]==a["grade_tau2"]
assert math.isclose(b["tau"]["tau2_ion_hertz"],a["tau"]["tau2_ion_hertz"]/4,rel_tol=1e-14)
assert cases["rejected_retry_preserves_generation"]["previous_generation_identical"] is True
exc=cases["write_failure_after_stamp"]
assert exc["status"]=="EXCEPTION" and exc["provenance"]["network_run_id"]!=exc["full_metrics_run_id"]
lw=read("evidence/lw_replay.json")
assert lw["finite_wrong_virial"]["status"].startswith("FAILED")
assert lw["nan_hides_wrong_virial"]["status"]=="OK"
assert lw["nan_hides_wrong_virial"]["parsed_cstr_present"]==[False,False]
assert lw["partial_cstr_tuple"]["status"]=="OK"
g1=read("evidence_g1/adversarial_results.json")
assert len(g1["producer"])==4
for x in g1["producer"]:
    assert (x["rc"],x["published"])==((0,True) if x["mode"]=="normal" else (3,False))
assert g1["producer"][0]["check_arm_rc"]==0
raw=read("evidence/raw18.json")
assert len(raw["old_new"]["checks"])==18
assert all(x["raw_output_hex_identical"] and x["boundaries_identical"] for x in raw["old_new"]["checks"])
assert math.isclose(raw["independent_power"]["relative_to_ideal_percent"],12.051760767398445,abs_tol=1e-12)
handover=read("evidence/handover_replay.json")
assert sum(x["rows"] for x in handover)==194
assert all(x["contact_network_rows_identical"] and x["columns_identical"] for x in handover)
report=(R/"codex_review_rgl_reverify_20261005.md").read_text(encoding="utf8")
assert all("### Q"+str(i) in report for i in range(1,8))
# Check all pinned source links really have that line at this verified source snapshot.
for path,line in re.findall(re.escape(PIN)+r"/([^)#]+)#L(\d+)",report):
    p=R/"source"/path
    assert p.is_file() and int(line)<=len(p.read_text(encoding="utf8").splitlines())
findings=read("findings_review.json")
assert findings["verdict"]=="HOLD" and len(findings["findings"])==3
assert all(x["severity"]=="P2" for x in findings["findings"])

root_files=[
"README.md","codex_review_rgl_reverify_20261005.md","findings_review.json",
"source_manifest.json","compare_metadata.json","acquisition.json","fixture_acquisition.json",
"verify_source.py","restore_transport.py","run_tests.py","run_probes.py","build_review_package.py"]
selected={R/x for x in root_files}
for d in ("source","inputs","diffs","probes","evidence_g1","evidence_g4"):
    selected.update((R/d).rglob("*"))
selected.update((R/"evidence").glob("*.json"))
selected.update((R/"evidence").glob("*.log"))
case_dirs=[]
for x in network:
    p=R/x["path"].replace("\\","/")
    assert p.resolve().is_relative_to((R/"evidence").resolve()) and p.is_dir()
    selected.update(p.rglob("*"));case_dirs.append(p.relative_to(R).as_posix())
    # Current active artifacts match the recorded evidence hash.
    for name,sha in x["current_hashes"].items():assert digest(p/name)==sha
lw_dirs=list((R/"evidence").glob("lw_parser_*"))
latest_lw=max(lw_dirs,key=lambda p:p.stat().st_mtime_ns)
assert (latest_lw/"nan_hides_wrong_virial.csv").is_file()
selected.update(latest_lw.rglob("*"))
selected={p for p in selected if p.is_file() and "__pycache__" not in p.parts and p.suffix not in (".pyc",".pyo")}
for p in selected:
    assert p.resolve().is_relative_to(R.resolve()) and not p.is_symlink()
qa=dict(
    source_blobs_verified=432,baseline_jobs=18,baseline_nonzero_expected={"lw":"missing real14"},
    actual_network_cases=12,raw_hex_cases=18,committed_summary_rows=194,
    production_runs=0,new_p1=0,new_p2=3,verdict="HOLD",
    selected_network_evidence_dirs=case_dirs,selected_lw_csv_dir=latest_lw.relative_to(R).as_posix(),
    exclusions="Orphan development temp directories, caches and dependency installations; no evidence deletion.")
emit("evidence/package_qa.json",qa);selected.add(R/"evidence/package_qa.json")
rows=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=digest(p)) for p in sorted(selected)]
emit("package_manifest.json",dict(schema="review_package/v1",commit=PIN,
    note="Contains all archived files except this manifest; ZIP receipt is external to avoid recursive hashing.",files=rows))
archive=R/"codex_rgl_reverify_review_20261005.zip"
with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for x in rows:z.write(R/x["path"],x["path"])
    z.write(R/"package_manifest.json","package_manifest.json")
with zipfile.ZipFile(archive) as z:
    names=z.namelist(); hazards=[]
    for n in names:
        p=PurePosixPath(n)
        if p.is_absolute() or ".." in p.parts or "\\" in n or ":" in n:hazards.append(n)
    assert not hazards and len(names)==len(set(names))
    assert set(names)=={x["path"] for x in rows}|{"package_manifest.json"}
    assert z.testzip() is None
    for x in rows:
        b=z.read(x["path"]);assert len(b)==x["bytes"] and hashlib.sha256(b).hexdigest()==x["sha256"]
receipt=dict(schema="review_delivery_receipt/v1",utc=datetime.now(timezone.utc).isoformat(),
    commit=PIN,review_verdict="HOLD",archive_verified=True,
    zip=dict(name=archive.name,bytes=archive.stat().st_size,sha256=digest(archive),entries=len(names)),
    manifest_sha256=digest(R/"package_manifest.json"),entry_hazards=[],
    validation="Every archive member compared to file manifest; CRC checked; exact entry set; source Git blobs independently checked.",
    exclusions=["Not scientific validation of real194 results","Not WSL/real14 integration approval","Not a production reseal"])
emit("package_receipt.json",receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))

