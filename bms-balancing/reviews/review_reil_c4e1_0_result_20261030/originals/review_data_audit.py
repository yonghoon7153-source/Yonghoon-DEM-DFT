"""Reviewer-owned data inspector; does not import or execute received programs."""
import ast
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SRC=ROOT/"source"
PRIOR=ROOT/"basis/prior_v5/source"
EV="bms-balancing/evidence/reil_c4e1_0_20261030/"
checks=[]
def check(name,condition,details=None):
    checks.append({"name":name,"matched":bool(condition),"details":details})
def sha(data):return hashlib.sha256(data).hexdigest()
def identity(p):
    b=p.read_bytes()
    return {"bytes":len(b),"sha256":sha(b)}
def write(name,obj):
    if (ROOT/name).exists():
        assert json.loads((ROOT/name).read_text(encoding="utf-8"))==obj, name
        return
    with (ROOT/name).open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
capture=json.loads((ROOT/"CAPTURE_METADATA.json").read_text(encoding="utf-8"))
identities=[]
for r in capture["files"]:
    p=ROOT/r["local"]
    b=p.read_bytes()
    gh=hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()
    check("captured Git blob "+r["local"],gh==r["git_blob_sha1"])
    identities.append({**r,**identity(p)})
write("SOURCE_IDENTITIES.json",{"files":identities})
evfiles=list((SRC/EV).iterdir())
check("evidence set 24 files 117742 bytes",len(evfiles)==24 and all(p.is_file() for p in evfiles) and sum(p.stat().st_size for p in evfiles)==117742)
seal_map={
 "bms-balancing/scripts/reil_c4e1_launch.py":"REIL_C4E1_LAUNCHER_DRAFT_v5_20261027.py.txt",
 "bms-balancing/tests/test_reil_c4e1_launch.py":"REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v5_20261027.py.txt",
 "bms-balancing/tests/test_reil_c4e1_runner.py":"REIL_C4E1_RUNNER_CONTROLS_DRAFT_v3_20261027.py.txt",
 EV+"00_step_runner.py":"REIL_C4E1_STEP_RUNNER_DRAFT_v5_20261027.py.txt",
}
for path,old in seal_map.items():
    check("approved copy "+path,(SRC/path).read_bytes()==(PRIOR/"bms-balancing/docs"/old).read_bytes())
hist=ROOT/"history/935b52aa/bms-balancing/scripts/reil_c4e1_launch.py"
check("historical skeleton matches approved",(hist).read_bytes()==(PRIOR/"bms-balancing/docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v5_20261027.py.txt").read_bytes())
check("approval v5 unchanged",(SRC/"bms-balancing/docs/REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md").read_bytes()==(PRIOR/"bms-balancing/docs/REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md").read_bytes())
runner=ast.parse((SRC/EV/"00_step_runner.py").read_text(encoding="utf-8"))
def literal(name):
    return ast.literal_eval(next(n.value for n in runner.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)))
fixed=literal("_FIXED")
launch=literal("LAUNCH")
for path,row in fixed.items():
    check("fixed current source "+path,identity(SRC/path)==row)
    if (PRIOR/path).is_file():
        check("unchanged reference "+path,(SRC/path).read_bytes()==(PRIOR/path).read_bytes())
skeleton=literal("SKELETON")
impl=literal("IMPL")
steps=["01_red_launcher","02_red_runner","03_green"]
heads=["935b52aa507caff59123f9ae77f5112a2af2cd9e","83e727fa72f9b7342d6f2a8173e6de3932d1c992","4391b3a345c4e0fd17e86f7ca788576a790f758c"]
end=json.loads((SRC/EV/"04_end.json").read_text(encoding="utf-8"))
step_rows=[]
for index,step in enumerate(steps):
    m=json.loads((SRC/EV/(step+".meta.json")).read_text(encoding="utf-8"))
    expected=dict(fixed,**{launch:skeleton if index<2 else impl})
    check(step+" EXPECT tables",len(expected)==14 and m["source_start"]==m["source_end"]==expected and set(m["targets"])==set(expected))
    t=(SRC/EV/(step+".source_sha256.txt")).read_text(encoding="utf-8")
    te=(SRC/EV/(step+".source_sha256_end.txt")).read_text(encoding="utf-8")
    parsed=dict((path,digest) for digest,path in (line.split("  ",1) for line in t.splitlines() if not line.startswith("#")))
    check(step+" text source hashes",t==te and parsed=={p:r["sha256"] for p,r in expected.items()} and len(t.splitlines())==15)
    check(step+" runner self recorded",m["runner"]["sha256"]==identity(SRC/EV/"00_step_runner.py")["sha256"] and m["runner"]["sha256"] in t.splitlines()[-1])
    c=m["cleanup"]
    check(step+" meta success conditions",m["started"] is True and m["runner_ok"] is True and m["timed_out"] is False and m["rc"]==([1,1,0][index]) and
          not any(m[k] for k in ("problems","end_problems","errors")) and m["first_error"] is None and
          c["status"]=="empty" and c["deadline_hit"] is False and c["emergency"] is False and not c["errors"] and not c["settle"]["errors"] and not c["settle"]["alive"])
    check(step+" Git heads",m["records"]["head_start"]["out"]==m["records"]["head_end"]["out"]==heads[index] and
          all(r["rc"]==0 and not r.get("error") and not r["err"] for r in m["records"].values()))
    check(step+" empty stderr",(SRC/EV/(step+".stderr.log")).stat().st_size==0)
    check(step+" recorded budget",m["timeout_s"]==[120,120,600][index] and m["times"]["child_s"]<m["timeout_s"] and m["times"]["cleanup_s"]<15)
    summ=end["steps"][step]
    check(step+" end summary",all(summ[k]==m[k] for k in ("rc","runner_ok","started","timed_out","times")) and summ["cleanup_status"]==c["status"] and
          summ["head_start"]==summ["head_end"]==heads[index])
    step_rows.append({"step":step,"child_rc":m["rc"],"runner_return_reported":[1,1,0][index],
                      "runner_return_evidence":"Submitted report plus return logic, not separate captured outer-shell exit status",
                      "times":m["times"],"start_utc":m["start_utc"],"end_utc":m["end_utc"],
                      "runner_ok":m["runner_ok"],"cleanup_status":c["status"],"source_count":len(expected)})
check("end copies hashes",all(identity(SRC/p)["sha256"]==v for p,v in end["copies_sha256"].items()) and len(end["copies_sha256"])==4)
start=(SRC/EV/"00_start.txt").read_text(encoding="utf-8").splitlines()
start_hashes=[line.split("  ",1) for line in start[3:]]
ok=True
for digest,path in start_hashes:
    if path=="scripts/reil_c4e1_launch.py":p=hist
    elif path.startswith("docs/"):p=PRIOR/"bms-balancing"/path
    else:p=SRC/"bms-balancing"/path
    ok &= sha(p.read_bytes())==digest
check("start 9 hashes",len(start_hashes)==9 and ok)
elapsed=(datetime.fromisoformat(end["utc"])-datetime.fromisoformat(start[0])).total_seconds()
check("start record -> end snapshot 273s",elapsed==273)
history=json.loads((ROOT/"COMMIT_HISTORY.json").read_text(encoding="utf-8"))
check("commit ancestry",all(history[i]["parents"]==[history[i-1]["sha"]] for i in range(1,len(history))))
bysha={r["sha"]:r for r in history}
pre=bysha[heads[0]]
check("preseal before first step by recorded UTC",datetime.fromisoformat(pre["commit"]["committer"]["date"])<datetime.fromisoformat(step_rows[0]["start_utc"]))
id_by_path={r["path"]:r for r in identities if r["ref"]==capture["head"]}
for c in history[2:7]:
    for f in c["files"]:
        if f["filename"].startswith(EV):
            check("commit evidence blob "+f["filename"],f["sha"]==id_by_path[f["filename"]]["git_blob_sha1"])
pre_expected={
 "bms-balancing/scripts/reil_c4e1_launch.py":next(r["git_blob_sha1"] for r in identities if r["local"].startswith("history/")),
 "bms-balancing/tests/test_reil_c4e1_launch.py":id_by_path["bms-balancing/tests/test_reil_c4e1_launch.py"]["git_blob_sha1"],
 "bms-balancing/tests/test_reil_c4e1_runner.py":id_by_path["bms-balancing/tests/test_reil_c4e1_runner.py"]["git_blob_sha1"],
 EV+"00_step_runner.py":id_by_path[EV+"00_step_runner.py"]["git_blob_sha1"],
 EV+"00_start.txt":id_by_path[EV+"00_start.txt"]["git_blob_sha1"]
}
check("preseal commit exact 4 copies plus start",len(pre["files"])==5 and {f["filename"]:f["sha"] for f in pre["files"]}==pre_expected)
sc=json.loads((ROOT/"SCOPE_COMPARE.json").read_text(encoding="utf-8"))
outside={f["filename"] for f in sc["files"] if not f["filename"].startswith(EV)}
expected_outside={"bms-balancing/.gitattributes","bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md",
                 "bms-balancing/scripts/reil_c4e1_launch.py","bms-balancing/tests/test_reil_c4e1_launch.py","bms-balancing/tests/test_reil_c4e1_runner.py"}
check("execution tracked diff scope",outside==expected_outside and len(sc["files"])==29 and sc["total_commits"]==6)
write("STEP_RECORD_SUMMARY.json",{"steps":step_rows,"evidence_files":24,"evidence_bytes":117742,
 "start_record_to_end_snapshot_s":elapsed,"a_name_check_to_end_snapshot_reported_s":327,
 "timing_limit":"UTC snapshots do not certify all-process wallclock completion or tool-return time."})
result={"kind":"REVIEWER_DATA_AUDIT","conditions":len(checks),"matched":sum(c["matched"] for c in checks),"checks":checks,
 "received_program_execution":0,"functional_retests":0,"scope":"Saved bytes/JSON/AST and GitHub commit records; not independent OS execution audit."}
write("STATIC_AUDIT.json",result)
print(json.dumps({"conditions":len(checks),"matched":result["matched"],"unmatched":[c for c in checks if not c["matched"]],"source_snapshots":len(identities)},ensure_ascii=False))
