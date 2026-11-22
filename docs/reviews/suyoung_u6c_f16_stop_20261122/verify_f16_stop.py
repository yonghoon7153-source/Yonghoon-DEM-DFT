"""Read and bind the first updated F16 stop. No solver import or field execution."""
import argparse
import csv
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
from pathlib import PurePosixPath
import subprocess
import tarfile


PIN = "e5c3ac7bba373efc4a7a0367c6f6ecee41018f29"
MODEL = "2cf17b1df57396ef01505a72641e01b19629bed5"
KERNEL = "8af03f07e8149219a13baa1d1ca79c2fc87940bb991c6055769ac0beeb3a8880"
F8 = "9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b"
SOURCE_TAR = "a4171ff2fc564394743683c9e81e954783bec99cbcdbc782524127dba5989a3d"
SOURCE_SUMS = "ed4d91f19047665ea57374fc931cb4c1b207cf1eec1bd6f4d3a235f2909b82b3"
RETURN = "bdd10395a7acc1aa7e64f7aaa6d8509a343ea448b47ee39e0770f520e310ec6d"
SCREEN = "4bd0a2851c1d46feb810bd8d5f1a499443807b0e6b01d10a5b7ebf6a33c84683"
TRACE = "aba3b5e93bbdda6400777e2bc73ebf75a5eb7792aed2da9661be048836999def"
STOP = "c424d8e7a4d799969d052acac3692c47a44a1a6657ab6497c62cbf516146e775"
EXPECTED_FILES = {"run/F16.log","run/F16_process_stop.txt","run/origin.txt","run/screen.txt",
                  "run/SOURCE_SHA256SUMS","run/F16/contact_stop.json","run/F16/incomplete.json","run/F16/trace.csv"}
WIDTH = .7024180763115129
DT = .0011231835082397789
SPEED = .034*math.sqrt(1/(2*(1+.45)))


def need(condition,code):
    if not condition:
        raise ValueError(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_member(archive,key):
    info=archive.getmember(key)
    need(info.isfile(),"MEMBER_NOT_FILE")
    return archive.extractfile(info).read()


def manifest(data):
    parsed={}
    for line in data.decode("ascii").splitlines():
        h,name=line.split("  ",1)
        path=PurePosixPath(name)
        need(len(h)==64 and set(h)<=set("0123456789abcdef") and name not in parsed and
             not path.is_absolute() and ".." not in path.parts and "\\" not in name and ":" not in name,"MANIFEST_FORMAT")
        parsed[name]=h
    return parsed


def verify_source(data,repo=None,source_tar=None):
    need(sha(data)==SOURCE_SUMS,"SOURCE_MANIFEST_SHA")
    sources=manifest(data)
    need(len(sources)==13 and sources["scripts/suyoung_multicontact_dev.py"]==KERNEL,"SOURCE_FOOTPRINT")
    release=(PIN+"\n"+MODEL+"\n").encode("ascii")
    need(sources["RELEASE"]==sha(release),"RELEASE_BINDING")
    if source_tar is not None:
        raw=source_tar.read_bytes()
        need(sha(raw)==SOURCE_TAR,"SOURCE_ARCHIVE_SHA")
        with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as archive:
            all_names=archive.getnames()
            need(len(all_names)==len(set(all_names)) and read_member(archive,"SOURCE_SHA256SUMS")==data,
                 "SOURCE_ARCHIVE_MANIFEST")
            outer=manifest(read_member(archive,"SHA256SUMS"))
            need(set(outer)==set(all_names)-{"SHA256SUMS"},"SOURCE_ARCHIVE_INVENTORY")
            for name,expected in {**outer,**sources}.items():
                need(sha(read_member(archive,name))==expected,"SOURCE_MEMBER_SHA")
            need(all(outer[name]==h for name,h in sources.items()),"SOURCE_MANIFEST_DISAGREEMENT")
    if repo is not None:
        git_root=repo.resolve().as_posix()
        for path,expected in sources.items():
            if path=="RELEASE":
                continue
            blob=subprocess.check_output(["git","-c","safe.directory="+git_root,"-C",git_root,"show",PIN+":"+path])
            need(sha(blob)==expected,"SOURCE_GIT_BLOB")
    need(repo is not None or source_tar is not None,"SOURCE_REFERENCE_REQUIRED")
    return len(sources)


def trace_rows(trace,last_step):
    reader=csv.reader(io.StringIO(trace.decode("ascii")))
    need(next(reader,None)==["step","time_code","height","bottom_pressure_E","phi_m"],"TRACE_HEADER")
    rows=0
    for i,row in enumerate(reader):
        need(len(row)==5 and row[0]==str(i),"TRACE_STEP_SEQUENCE")
        t,h,p,phi=map(float,row[1:])
        need(t==DT*i and h==WIDTH-i*DT*SPEED and h>=.75*WIDTH,"NATIVE_F16_GRID")
        need(math.isfinite(p) and 0<=p<.12 and (i>0 or p==0),"INCOMPLETE_BEFORE_PRESSURE_TARGET")
        need(math.isclose(phi,49*math.pi*.05**2/(WIDTH*h),rel_tol=1e-12),"NATIVE_SEED_AREA")
        rows+=1
    need(rows==last_step+1 and rows>0,"TRACE_LENGTH")
    return rows


def verify_stop(stop,inc,trace):
    need(inc["stage3_go"] is False and inc["u6_qualified"] is False and
         inc["label"]=="DEVELOPMENT_ONLY" and inc["status"]=="CONTACT_STOP","STOP_DISPOSITION")
    need(stop["scope"]=="NATIVE_UNRESOLVED_ROWS" and len(stop["nodes"])==1 and
         stop["exception"] == inc["exception"]=="ArithmeticError" and stop["message"]==inc["message"] and
         stop["attempted_step"]==inc["attempted_step"]==4803 and inc["candidate_sha256"]==KERNEL,"STOP_SOURCE")
    last_step=inc["attempted_step"]-1
    need(inc["trace"]=={"bytes":len(trace),"present":True,"sequence_valid":True,
                        "last_complete_step":last_step,"sha256":sha(trace)},"PARTIAL_TRACE_BINDING")
    n=stop["nodes"][0]
    need(n["node_id"]==16810 and n["iteration"]==512 and n["mu"]==.5 and len(set(n["field_ids"]))==3 and
         len(n["field_ids"])==3 and list(zip(n["left"],n["right"]))==list(itertools.combinations(range(3),2)),
         "NODE_IDENTITY")
    for key in ("jn_scaled","jt_scaled","closing","slip"):
        need(len(n[key])==3 and all(math.isfinite(v) for v in n[key]),"PAIR_QUANTITIES")
    errors=[]
    for jn,jt,closing,slip in zip(n["jn_scaled"],n["jt_scaled"],n["closing"],n["slip"]):
        dn=max(-jn,closing)
        lo=(-n["mu"]*jn-jt)-n["mu"]*dn
        hi=(n["mu"]*jn-jt)+n["mu"]*dn
        errors.append(max(abs(dn),abs(max(lo,min(slip,hi)))))
    speeds=[math.dist(n["incoming"][i],n["incoming"][j]) for i,j in zip(n["left"],n["right"])]
    tol=1e-13+1e-11*max(speeds)
    residual=max(errors)
    need(math.isclose(tol,n["speed_tol"],rel_tol=2e-15) and math.isclose(residual,n["residual"],rel_tol=2e-14)
         and residual>tol,"TERMINAL_RESIDUAL")
    return {"rows":trace_rows(trace,last_step),"last_complete_step":last_step,"attempted_step":last_step+1,
            "node":n["node_id"],"fields":3,"contact_pairs":3,"updates":512,"native_residual":n["residual"],
            "speed_tolerance":n["speed_tol"],"native_residual_over_tolerance":n["residual"]/n["speed_tol"]}


def check(args):
    archive_bytes=args.result.read_bytes()
    screen=(args.result.parent/"screen.txt").read_bytes()
    need(sha(archive_bytes)==RETURN and sha(screen)==SCREEN,"RETURN_IDENTITY")
    need(manifest((args.result.parent/"SHA256SUMS").read_bytes()) ==
         {"screen.txt":SCREEN,"suyoung_f16_contact_result.tar.gz":RETURN},"RETURN_MANIFEST")
    with tarfile.open(fileobj=io.BytesIO(archive_bytes),mode="r:gz") as ar:
        names=ar.getnames()
        files={m.name for m in ar.getmembers() if m.isfile()}
        need(len(set(names))==len(names) and files==EXPECTED_FILES,"EXACT_STOP_INVENTORY")
        origin=dict(line.split("=",1) for line in read_member(ar,"run/origin.txt").decode("ascii").splitlines())
        required={"release":PIN,"contact_source_pin":MODEL,"source_sums":SOURCE_SUMS,"final_f8_sha256":F8,
                  "kernel_sha256":KERNEL,"CPU":"0","arm_budget_s":"1740","per_arm_hard_s":"1800"}
        need(all(origin[k]==v for k,v in required.items()),"FIELD_ORIGIN")
        count=verify_source(read_member(ar,"run/SOURCE_SHA256SUMS"),args.repo,args.source_tar)
        need(read_member(ar,"run/screen.txt")==screen and screen.decode("ascii").splitlines()==
             ["DEVELOPMENT_ONLY","F16_BEGIN="+origin["started_utc"],"F16_RC=4","COMMAND_RC=4"] and
             read_member(ar,"run/F16.log").decode("ascii").splitlines()==["CONTACT_STOP"],"PROCESS_RC")
        trace=read_member(ar,"run/F16/trace.csv")
        need(sha(trace)==TRACE and read_member(ar,"run/F16_process_stop.txt").decode("ascii").splitlines()==
             ["command_rc=4",TRACE+"  F16/trace.csv"],"PROCESS_TRACE")
        raw=read_member(ar,"run/F16/contact_stop.json")
        inc=json.loads(read_member(ar,"run/F16/incomplete.json"))
        need(sha(raw)==inc["contact_stop_sha256"]==STOP,"NODE_BYTES")
        info=verify_stop(json.loads(raw),inc,trace)
    return {"readback":"VERIFIED_INCOMPLETE","label":"DEVELOPMENT_ONLY","field_command_rc":4,"field_arm_rc":4,
            "release":PIN,"contact_source_pin":MODEL,"kernel_sha256":KERNEL,"source_manifest_entries":count,
            "source_git_blobs_checked":args.repo is not None,"source_tar_checked":args.source_tar is not None,
            "archive_sha256":RETURN,"trace_sha256":TRACE,"contact_stop_sha256":STOP,"arm":"F16_ORIGINAL","stop":info,
            "F8_F16":{"comparison":"HOLD","reason":"F16_INCOMPLETE","ratio":None},"F12_F24":{"comparison":"HOLD","reason":"UPDATED_PAIR_MISSING"},
            "u6_qualified":False,"stage3_go":False,"new_field_executions_by_readback":0}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--result",type=Path,required=True)
    p.add_argument("--source-tar",type=Path,help="Original source package; use this for a Git-free replay")
    p.add_argument("--repo",type=Path,help="Optional clone containing the field release")
    p.add_argument("--out",type=Path,required=True,help="New public JSON receipt")
    a=p.parse_args()
    if not(a.repo or a.source_tar):
        p.error("--source-tar or --repo required")
    report=check(a)
    with a.out.open("x",encoding="ascii",newline="\n") as f:
        json.dump(report,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")
    print(report["readback"],"F8_F16_HOLD")
