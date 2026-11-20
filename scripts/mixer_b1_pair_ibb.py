"""Author-operated B1 rotation pair, with separate serial releases in one installation."""
import argparse
import math
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tarfile
import time

HERE = Path(__file__).resolve().parent
rotation = runpy.run_path(str(HERE / "mixer_rotation_n0_ibb.py"))
base = rotation["base"]
need, sha, put, read, ref = (base[key] for key in ("need","sha","put","read","ref"))
F8 = base["F8"]
WALL = rotation["WALL"]
B_MANIFEST = "088460cc6a71db4fcc0b6fd326fb89ae629767a2ded45846952640ca44ac0ee0"
N0_POINTER = "0995202dc25e59ff144647333956ee86ec456715ee228dcea7e8dc1fb215a659"
INPUTS = {
    "U": ("bb00b3251d76d45f311139606fdcbfd842e485489e49447a7d2373d5bfa891c6",
          "c6c6554586a4eabd5cdb3a1bb12ad980a8e17596b56fc63c5345ba55df970806"),
    "C": ("7875e1f053411e8531cecd616ffe1d016044a50b57d500f515edcd197e4d0d7d",
          "32eead6431f1aad09f3aca4d988939b5a7b846e62b852739e626e3b073965c19")}
ARCHIVES = ("b1_report.tar.gz","b1_full_result.tar.gz")

def case_name(role):
    need(role in INPUTS,"unknown B1 arm")
    return "PRECAL_R1_B1_" + role

def author_token(role, token):
    case_name(role)
    need(token=="GO_B1_"+role+"_ONCE","separate author GO required")

def create_attempt(root,role):
    case_name(role)
    ctx=root/"arms"/role
    ctx.mkdir(parents=True,exist_ok=False)
    return ctx

def verified_sums(result):
    rows={}
    for line in (result/"SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest,name=line.split("  ",1)
        need(name in ARCHIVES and name not in rows and not (result/name).is_symlink(),"archive member")
        need(sha(result/name)==digest,"archive mismatch")
        rows[name]=digest
    need(set(rows)==set(ARCHIVES),"archive set")
    return rows

def check_peer(record,pin):
    jid=record.get("job_id")
    s=record.get("scheduler",{})
    need(isinstance(jid,str) and re.fullmatch("[1-9][0-9]*",jid)
         and record.get("release_pin")==pin and record.get("role")=="U"
         and record.get("case")==case_name("U") and record.get("return_ready") is True
         and record.get("exact_frame_names") is True and record.get("frame_count")==234
         and record.get("post_runtime_matches") is True and record.get("w9")=="LIVE_TERMINAL_MATCH"
         and record.get("job_end_id")==jid and type(record.get("runner_rc")) is int
         and record["runner_rc"]==0 and s.get("job_id")==jid and s.get("state")=="COMPLETED"
         and s.get("exit_code")=="0:0","U terminal, runtime, arm or pin evidence missing")

def prior_return(root,pin):
    ctx=root/"arms/U"
    path=ctx/"return.json"
    need(path.is_file() and not path.is_symlink(),"U receipt required")
    record=read(path)
    check_peer(record,pin)
    need(re.fullmatch("collection_[0-9]+",record["directory"]),"U return directory")
    need(verified_sums(ctx/record["directory"])==record["archive_hashes"],"U return bytes")
    remote_id=record["job_id"]
    here=root/"B"/F8
    prior=here/"cases"/case_name("U")
    private=read(prior/"submission.receipt.json")
    admission=read(here/"admission"/(case_name("U")+".submission.json"))
    need(private==admission and admission["state"]=="SUBMITTED"
         and admission["job_id"]==remote_id and admission["case"]==case_name("U"),"U admission binding")
    end=read(prior/"job_end.json")
    need(rotation["completed"](rotation["account"](remote_id),remote_id,end),"U accounting no longer confirmed")
    return ref(path)

def w9_status(matches,live,end,start):
    if not matches:
        return "MISMATCH"
    if not live:
        return "RECOVERY_ONLY"
    if type(end) not in (int,float) or not math.isfinite(end) or start<end:
        return "UNKNOWN_TIME"
    return "LIVE_TERMINAL_MATCH"

def verify_sources(root,role):
    manifest_path=root/"B_manifest.json"
    need(sha(manifest_path)==B_MANIFEST,"B manifest mismatch")
    if role=="U":
        manifest=base["verify_deployment"](root)
    else:
        manifest=read(manifest_path)
        for row in manifest["files"]:
            path=root/"B"/base["safe_rel"](row["path"])
            need(not path.is_symlink() and path.stat().st_size==row["bytes"] and sha(path)==row["sha256"],
                 "original B file changed")
    need(manifest["source_pin"]==rotation["PIN_B"] and len(manifest["files"])==283
         and manifest["approved_return_sha256"]==rotation["A_B_RETURN"],"B provenance")
    here=root/"B"/F8
    assets=here/"planned_assets"/case_name(role)
    need((sha(assets/"in.mixer"),sha(assets/"deck_meta.json"))==INPUTS[role],"B1 deck or metadata identity")
    return manifest

def runtime_preflight(root,ctx,binary,mpi,prefix):
    shutil.copyfile(root/"control/runtime_reference.json",ctx/"control/runtime_reference.json")
    cap=base["capture"]
    area=ctx/"evidence/wall"
    user=os.environ["USER"]
    qos,_=cap(area,"qos",["sacctmgr","-n","-P","show","qos","cpu-60","format=Name,MaxWall"])
    assoc,_=cap(area,"assoc",["sacctmgr","-n","-P","show","assoc","user="+user,"format=User,QOS,MaxWall"])
    part,_=cap(area,"partition",["scontrol","show","partition","cpu","-o"])
    rotation["wall_limits"](qos,assoc,part,user)
    live=base["preflight"](ctx,binary,mpi,prefix)
    live.update(qualification_accepted=True,qualification_scope="E0_DEVELOPMENT_ONLY",
                E0_job="366423",N0_job="367547",e0_W9_at_T9=False)
    live_path=ctx/"evidence/b1_live.json"
    put(live_path,live)
    return live_path

def prepare(root,role,token,pin,runtime):
    author_token(role,token)
    manifest=verify_sources(root,role)
    here=root/"B"/F8
    binary,mpi,prefix=runtime
    need(sha(root/"control/n0_return.json")==N0_POINTER,"N0 receipt identity")
    if role=="C":
        peer=prior_return(root,pin)
    else:
        peer=ref(root/"control/n0_return.json")
    ctx=create_attempt(root,role)
    (ctx/"control").mkdir()
    (ctx/"evidence").mkdir()
    auth=root/"control/pair_authority.json"
    policy_path=here/"campaign_policy.json"
    campaign=dict(label="DEVELOPMENT_DATA_ONLY",release_pin=pin,asset_manifest=B_MANIFEST,
                  order=[case_name("U"),case_name("C")],runtime_concurrency=1,
                  requires_explicit_arm_token=True,no_automatic_release_or_retry=True)
    if role=="U":
        put(auth,campaign)
        policy=base["policy"](str(here),sha(auth))
        # The unchanged submitter counts every historical reservation forever.
        # Two ledger slots hold this serial pair. C also checks the completed U return.
        policy["max_concurrency"]=2
        put(policy_path,policy)
    else:
        need(read(auth)==campaign,"pair authority changed")
        expected=base["policy"](str(here),sha(auth))
        expected["max_concurrency"]=2
        need(read(policy_path)==expected,"pair campaign changed")
    case_id=case_name(role)
    case=here/"cases"/case_id
    case.mkdir(parents=True)
    folder=here/"approvals"/case_id
    folder.mkdir(parents=True)
    parts=("in.mixer","deck_meta.json","Drum.stl","Front.stl","Back.stl")
    for name in parts:
        shutil.copyfile(here/"planned_assets"/case_id/name,case/name)
    put(ctx/"evidence/author_arm.json",dict(token=token,case=case_id,pin=pin,previous=peer,
                                            label="DEVELOPMENT_DATA_ONLY",automatic_retry=False))
    put(folder/"qualification.json",dict(E0_development_accepted=True,paper_qualified=False,
                                         E0_W9_at_T9=False,N0_readback="OK",previous=peer))
    put(folder/"policy.json",dict(policy_id="B1_DEVELOPMENT_SERIAL",execution_authorized=True,
                                   allowed_to_submit=[case_id]))
    put(folder/"mxd2r_disposition.json",dict(scope="one development arm",E0_known_limit="MXE0-02",
                                            paper_release=False))
    python=Path(sys.executable).resolve(strict=True)
    paths=[root/"B"/base["safe_rel"](row["path"]) for row in manifest["files"]]
    paths.extend(case/name for name in parts)
    paths.extend([python,HERE/"mixer_b1_pair_ibb.py",HERE/"mixer_rotation_n0_ibb.py",HERE/"mixer_e0_pilot_ibb.py",
                  auth,root/"control/n0_return.json",root/"control/pair_pin.json",root/"control/AB_RECEIPT.json",
                  root/"control/runtime_reference.json",root/"B_manifest.json",ctx/"evidence/author_arm.json"])
    put(folder/"source_manifest.json",{"files":[ref(p) for p in paths]})
    live=runtime_preflight(root,ctx,binary,mpi,prefix)
    approval=dict(schema="mixer_first8_execution_approval/1",gate="MAP_CASE_GO",execution_authorized=True,
                  case=case_id,case_dir=str(case),np=20,author_choices_confirmed=True,approved_concurrency=2,
                  wave_release=[case_id],runner_reviewed=True,walltime_approved=True,source_root=str(root/"B"),
                  source_pin=rotation["PIN_B"],minimum_free_bytes=base["FREE_BYTES"],
                  minimum_free_inodes=base["FREE_INODES"],campaign_policy=ref(policy_path),author_go=ref(auth),
                  qualification=ref(folder/"qualification.json"),policy=ref(folder/"policy.json"),
                  mxd2r_disposition=ref(folder/"mxd2r_disposition.json"),live_preflight=ref(live),
                  source_manifest=ref(folder/"source_manifest.json"),binary=ref(binary),mpi_launcher=ref(mpi),
                  runner_bindings=dict(python=str(python),job_start=str(here/"job_start.py.txt"),
                                       stdout=str(case/"slurm.stdout"),stderr=str(case/"slurm.stderr"),walltime=WALL))
    submit=here/"submit_one.py.txt"
    ap=folder/"approval.json"
    runner=folder/"runner.sbatch"
    with runner.open("x",encoding="utf-8",newline="\n") as handle:
        handle.write(runpy.run_path(str(submit))["canonical_runner"](approval,str(ap)))
    approval["runner"]=ref(runner)
    put(ap,approval)
    return submit,ap

def collect(root,role,jid,acct,runtime,live,pin):
    terminal=base["terminal"](acct,jid)
    need(terminal is not None,"not accounted terminal")
    ctx=root/"arms"/role
    lock=ctx/"collection.lock"
    lock.mkdir()
    try:
        return collect_terminal(root,role,jid,acct,runtime,live,pin,terminal)
    finally:
        lock.rmdir()

def collect_terminal(root,role,jid,acct,runtime,live,pin,terminal):
    ctx=root/"arms"/role
    need(not (ctx/"return.json").exists(),"return already exists")
    case_id=case_name(role)
    here=root/"B"/F8
    case=here/"cases"/case_id
    attempt="collection_"+str(time.time_ns())
    start=time.time()
    runtime_error=None
    try:
        match=base["runtime"](ctx,*runtime,attempt+"_post")["matches"]
    except (OSError,ValueError,KeyError,RuntimeError,subprocess.SubprocessError) as exc:
        match=False
        runtime_error=str(exc)
    end=read(case/"job_end.json") if (case/"job_end.json").is_file() else {}
    names=[p.name for p in (case/"post").glob("mix_*.liggghts")]
    exact=rotation["frames_ok"](names)
    ready=bool(exact and match and rotation["completed"](acct,jid,end))
    w9=w9_status(match,live,end.get("end_unix"),start)
    rec=dict(label="DEVELOPMENT_DATA_ONLY",case=case_id,role=role,release_pin=pin,job_id=jid,
             scheduler=terminal,runner_rc=end.get("returncode"),job_end_id=end.get("job_id"),
             frame_count=len(names),exact_frame_names=exact,return_ready=ready,post_runtime_matches=match,
             w9=w9,post_runtime_error=runtime_error,post_start_unix=start,post_finished_unix=time.time(),
             job_end_unix=end.get("end_unix"))
    put(ctx/"evidence"/(attempt+".json"),rec)
    out=ctx/attempt
    out.mkdir()
    with tarfile.open(out/ARCHIVES[1],"x:gz",compresslevel=1) as archive:
        for file in sorted(case.rglob("*")):
            need(not file.is_symlink() and (file.is_file() or file.is_dir()),"nonregular result")
            if file.is_file():
                archive.add(file,case_id+"/"+file.relative_to(case).as_posix(),recursive=False)
    with tarfile.open(out/ARCHIVES[0],"x:gz",compresslevel=1) as archive:
        for name in ("control/pair_pin.json","control/pair_authority.json","B_manifest.json"):
            archive.add(root/name,name)
        archive.add(ctx/"evidence","evidence")
        for name in ("campaign_policy.json","approvals/"+case_id,"admission"):
            archive.add(here/name,name)
    hashes={n:sha(out/n) for n in ARCHIVES}
    with (out/"SHA256SUMS").open("x",encoding="ascii") as f:
        for name,digest in hashes.items():
            f.write(digest+"  "+name+"\n")
    put(ctx/"return.json",dict(rec,directory=attempt,archive_hashes=hashes))
    print("JOB_ID=%s RUNNER_RC=%s F=%d W9=%s RETURN_READY=%s"%
          (jid,rec["runner_rc"],len(names),w9,str(ready).upper()),flush=True)
    return 0 if ready else 1

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("role",choices=("U","C"))
    p.add_argument("action")
    for key in ("root","binary","mpi","prefix"):
        p.add_argument("--"+key,type=Path,required=True)
    a=p.parse_args()
    root=a.root.resolve(strict=True)
    runtime=tuple(v.resolve(strict=True) for v in (a.binary,a.mpi,a.prefix))
    need(sys.platform.startswith("linux"),"Linux required")
    need(not any(k.startswith(("SBATCH_","SLURM_","SALLOC_","SRUN_")) for k in os.environ),"inherited scheduler options/allocation")
    keep={k:os.environ[k] for k in ("PATH","HOME","USER","LOGNAME","LANG","LC_ALL","TMPDIR") if k in os.environ}
    os.environ.clear(); os.environ.update(keep)
    pin=read(root/"control/pair_pin.json")
    need(re.fullmatch("[0-9a-f]{40}",pin["commit"]),"invalid release")
    names=("mixer_b1_pair_ibb.py","mixer_rotation_n0_ibb.py","mixer_e0_pilot_ibb.py")
    need(set(pin["controllers"])==set(names) and all(sha(HERE/n)==pin["controllers"][n] for n in names),
         "controller identity")
    live=a.action!="collect"
    if live:
        author_token(a.role,a.action)
        submit,ap=prepare(root,a.role,a.action,pin["commit"],runtime)
        reply=base["command"]([sys.executable,"-I","-B",str(submit),str(ap)],90)
        put(root/"arms"/a.role/"evidence/submit.json",dict(rc=reply.returncode,stdout=reply.stdout,stderr=reply.stderr))
        print("SUBMIT_RC="+str(reply.returncode),flush=True)
        need(reply.returncode==0,"submission failed or uncertain; no retry")
    name=case_name(a.role)
    case=root/"B"/F8/"cases"/name
    receipt=read(case/"submission.receipt.json")
    jid=str(receipt["job_id"])
    need(receipt["case"]==name and receipt["state"]=="SUBMITTED" and re.fullmatch("[1-9][0-9]*",jid),"no confirmed original job")
    print("JOB_ID="+jid,flush=True)
    acct=rotation["monitor"](case,jid) if live else rotation["account"](jid)
    return collect(root,a.role,jid,acct,runtime,live,pin["commit"])

if __name__=="__main__":
    raise SystemExit(main())
