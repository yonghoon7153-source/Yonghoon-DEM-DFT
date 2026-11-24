"""Single author dispatch for two development rotations. No requeue or restart action."""
import argparse
import json
import os
from pathlib import Path
import re
import runpy
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

ARMS = ("L020", "L050")
GO = "GO_MIXER_LADDER_020_050_ONCE"
ACTIVE = {"PENDING","CONFIGURING","RUNNING","COMPLETING","SUSPENDED","RESIZING","REQUEUED",
          "REQUEUE_FED","SIGNALING","STAGE_OUT"}
ROOT = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def read(path):
    return json.loads(path.read_bytes())


def put(path, data):
    with path.open("x", encoding="utf8") as f:
        json.dump(data, f, indent=2, allow_nan=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())


def budget(output, first_job):
    reserved = {}
    for line in output.splitlines():
        if not line.strip():
            continue
        cols = line.strip().split("|")
        need(len(cols) == 3, "unparsed squeue row")
        jid,state,n = cols
        need(re.fullmatch(r"[0-9]+(?:_[0-9]+)?(?:\+[0-9]+)?",jid) and jid not in reserved
             and state in ACTIVE and n.isdigit() and int(n)>0,"unknown/duplicate allocation")
        reserved[jid] = int(n)
    if first_job in reserved:
        need(reserved[first_job] == 20, "wrong first arm allocation")
    # On the second snapshot Slurm may not yet show the newly acknowledged first arm.
    projected = sum(reserved.values()) + (20 if first_job in reserved else 40)
    need(projected <= 60, f"capacity stop: projected={projected} limit=60")
    return projected


def dispatch(root, capacity, send, monitor):
    put(root/"pair_intent.json", {"arms":ARMS,"token":GO})
    prior = None
    for arm in ARMS:
        capacity(prior)
        jid = send(arm)
        need(jid.isdigit() and jid != prior,"ambiguous submission")
        monitor(arm,jid)
        prior = jid


def classify(state, normal, frames_ok, w9):
    if state == "TIMEOUT":
        return "TECH_MISSING_TIMEOUT"
    return "COMPLETE" if state=="COMPLETED" and normal and frames_ok and w9=="LIVE_TERMINAL_MATCH" else "TECH_MISSING"


def case(arm):
    need(arm in ARMS,"unapproved arm")
    return "MIXER_B2_"+arm


def context(arm):
    return ROOT/"arms"/arm


def library():
    return runpy.run_path(str(ROOT/"lib/mixer_b1_pair_ibb.py"))


def environment():
    prefix = Path(os.environ["CONDA_PREFIX"]).resolve(strict=True)
    mpi = Path(shutil.which("mpirun")).resolve(strict=True)
    binary = (Path.home()/"LIGGGHTS-PUBLIC/src/lmp_mpi").resolve(strict=True)
    return binary,mpi,prefix


def verify(base):
    manifest = read(ROOT/"release.json")
    need(set(manifest["arms"]) == set(ARMS) and re.fullmatch("[0-9a-f]{40}",manifest["pin"]), "release identity")
    for name,h in manifest["files"].items():
        p = ROOT/name
        need(p.resolve()==p and p.is_file() and base["sha"](p)==h,"package drift: "+name)
    return manifest


def capture_preflight(ctx, runtime, lib):
    base = lib["base"]
    capture = base["capture"]
    relative = ctx/"evidence"/"preflight"
    user=os.environ["USER"]
    def cap(k,argv):
        return capture(relative,k,argv)[0]
    assoc = cap("assoc",["sacctmgr","-n","-P","show","assoc","user="+user,"format=User,QOS,MaxWall"])
    part = cap("partition",["scontrol","show","partition","cpu","-o"])
    qos = cap("qos",["sacctmgr","-n","-P","show","qos","cpu-60","format=Name,MaxTRESPU"])
    wall = cap("wall",["sacctmgr","-n","-P","show","qos","cpu-60","format=Name,MaxWall"])
    lib["rotation"]["wall_limits"](wall,assoc,part,user)
    base["scheduler_ok"](qos,assoc,part,user)
    storage=base["storage_ok"](cap("df",["df","-PB1",str(ctx)]),cap("inode",["df","-Pi",str(ctx)]),
                               cap("ost",["lfs","df",str(ctx)]))
    need(not re.search(r"\d+\*",cap("quota",["lfs","quota","-u",user,str(ctx)])), "quota exceeded")
    need(base["runtime"](ctx,*runtime,"runtime_pre")["matches"],"pre runtime differs")
    return storage


def setup(arm,lib,runtime,release):
    base=lib["base"]
    ctx=context(arm)
    ctx.mkdir(parents=True,exist_ok=False)
    ctl=ctx/"control"
    ctl.mkdir()
    (ctx/"evidence").mkdir()
    shutil.copyfile(ROOT/"control/runtime_reference.json",ctl/"runtime_reference.json")
    run=ctx/case(arm)
    shutil.copytree(ROOT/"assets"/arm,run)
    jobstart=ROOT/"lib/job_start.py.txt"
    runner=ctx/"runner.sbatch"
    ap=ctl/"approval.json"
    runner.write_text("#!/bin/bash\nset -eu\nexec "+shlex.join([sys.executable,"-I","-B",str(jobstart),str(ap)])+"\n")
    live=capture_preflight(ctx,runtime,lib)
    def record(name,obj):
        p=ctl/(name+".json")
        put(p,obj)
        return base["ref"](p)
    scope=record("policy",{"execution_authorized":True,"allowed_to_submit":[case(arm)]})
    src=record("sources",{"files":[base["ref"](p) for p in
                         [jobstart,ROOT/"ladder.py",ROOT/"release.json",*sorted(run.iterdir())]]})
    approval=dict(np=20,gate="MAP_CASE_GO",execution_authorized=True,case=case(arm),case_dir=str(run),
                  wave_release=[case(arm)],author_choices_confirmed=True,author_go=base["ref"](ROOT/"authorization.json"),
                  qualification=record("qualification",{"prior_pair":"B2","jobs":["368758","369734"],"development_only":True}),
                  mxd2r_disposition=record("scope",{"ratio":release["arms"][arm],"protocol":"ladder.md"}),
                  policy=scope,live_preflight=record("preflight",live),source_manifest=src,runner=base["ref"](runner),
                  binary=base["ref"](runtime[0]),mpi_launcher=base["ref"](runtime[1]),
                  minimum_free_bytes=base["FREE_BYTES"],minimum_free_inodes=base["FREE_INODES"])
    put(ap,approval)


def submit(arm,base):
    ctx=context(arm)
    run=ctx/case(arm)
    put(run/"submission.claim.json",{"approval_sha256":base["sha"](ctx/"control/approval.json")})
    argv=["sbatch","--parsable","--no-requeue","--partition=cpu","--qos=cpu-60","--nodes=1","--ntasks=20",
          "--cpus-per-task=1","--time=2-00:00:00","--job-name=mx"+arm,"--chdir="+str(run),
          "--output="+str(run/"slurm.stdout"),"--error="+str(run/"slurm.stderr"),str(ctx/"runner.sbatch")]
    reply=base["command"](argv,90)
    put(ctx/"submit_response.json",{"rc":reply.returncode,"stdout":reply.stdout,"stderr":reply.stderr})
    m=re.fullmatch(r"([0-9]+)(?:;[\w.-]+)?",reply.stdout.strip())
    need(reply.returncode==0 and m,"uncertain sbatch reply; inspect STATUS")
    jid=m.group(1)
    put(ctx/"submission.json",{"case":case(arm),"job_id":jid})
    print(f"ACKNOWLEDGED {arm} JOB_ID={jid}",flush=True)
    return jid


def monitor_detached(arm,jid):
    ctx=context(arm)
    with (ctx/"worker.log").open("xb") as log:
        subprocess.Popen([sys.executable,"-I","-B","-u",str(ROOT/"ladder.py"),"monitor",arm,jid],
                         stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)


def launch(lib):
    base=lib["base"]
    release=verify(base)
    need(not any(k.startswith(("SBATCH_","SLURM_","SALLOC_","SRUN_")) for k in os.environ),"wrong login context")
    put(ROOT/"authorization.json",dict(token=GO,levels=release["arms"],seed=32452843,release=release["pin"]))
    runtime=environment()
    for arm in ARMS:
        setup(arm,lib,runtime,release)
    def capacity(prior):
        arm=ARMS[0] if prior is None else ARMS[1]
        text,_=base["capture"](context(arm)/"evidence","queue_before_submission",
                             ["squeue","--array","-h","-u",os.environ["USER"],"-o","%i|%T|%C"],10)
        projected=budget(text,prior)
        print(f"CAPACITY_OK arm={arm} projected={projected}/60",flush=True)
    dispatch(ROOT,capacity,lambda arm:submit(arm,base),monitor_detached)


def confirmed_job(arm):
    ctx=context(arm)
    p=ctx/"submission.json"
    if p.is_file():
        r=read(p)
        need(r["case"]==case(arm) and re.fullmatch("[0-9]+",r["job_id"]),"job pointer mismatch")
        return r["job_id"]
    # Interrupted client or sbatch acknowledgement. Only use the verified job's own start record.
    run=ctx/case(arm)
    if (run/"job_start.json").is_file():
        r=read(run/"job_start.json")
        need(r["case"]==case(arm) and re.fullmatch("[0-9]+",r["job_id"]) and
             r["approval_sha256"]==read(run/"submission.claim.json")["approval_sha256"]==
             library()["base"]["sha"](ctx/"control/approval.json"),"unbound job start")
        return r["job_id"]
    return None


def archive(root, path, inputs):
    with tarfile.open(path,"x:gz",compresslevel=1) as tar:
        for p in inputs:
            need(p.is_file() and p.resolve()==p,"nonregular return file")
            tar.add(p,p.relative_to(root).as_posix(),recursive=False)


def collect(arm,jid,lib,live):
    ctx=context(arm)
    run=ctx/case(arm)
    base,rot=lib["base"],lib["rotation"]
    if not live and not base["terminal"](rot["account"](jid),jid):
        print(f"{arm} JOB_ID={jid} ACTIVE_OR_ACCOUNTING_PENDING")
        return
    with lib["collection_lease"](ctx):
        if (ctx/"return.json").exists():
            return
        need(jid==confirmed_job(arm),"monitor job mismatch")
        acct=rot["monitor"](run,jid) if live else rot["account"](jid)
        terminal=base["terminal"](acct,jid)
        if not terminal:
            print(f"{arm} JOB_ID={jid} ACTIVE_OR_ACCOUNTING_PENDING")
            return
        out=Path(tempfile.mkdtemp(prefix="collection_",dir=ctx))
        start=time.time()
        error=None
        try:
            runtime=base["runtime"](ctx,*environment(),out.name+"_post")
            match=runtime["matches"]
        except (OSError,ValueError,subprocess.SubprocessError) as exc:
            match,error=False,str(exc)
        end=read(run/"job_end.json") if (run/"job_end.json").is_file() else {}
        frames=[p.name for p in (run/"post").glob("mix_*.liggghts")]
        exact=rot["frames_ok"](frames)
        w9=lib["w9_status"](match,live,end.get("end_unix"),start)
        disposition=classify(terminal["state"],rot["completed"](acct,jid,end),exact,w9)
        r=dict(case=case(arm),role=arm,ratio=read(ROOT/"release.json")["arms"][arm],
               release_pin=read(ROOT/"release.json")["pin"],job_id=jid,job_end_id=end.get("job_id"),
               label="DEVELOPMENT_DATA_ONLY",scheduler=terminal,runner_rc=end.get("returncode"),frame_count=len(frames),
               exact_frame_names=exact,post_runtime_matches=match,w9=w9,post_runtime_error=error,
               post_start_unix=start,post_finished_unix=time.time(),job_end_unix=end.get("end_unix"),
               disposition=disposition,return_ready=disposition=="COMPLETE")
        receipt=ctx/"evidence"/(out.name+".json")
        put(receipt,r)
        full=out/"b2_full_result.tar.gz"
        report=out/"b2_report.tar.gz"
        archive(ctx,full,sorted(p for p in run.rglob("*") if p.is_file()))
        evidence=[ROOT/"release.json",ROOT/"authorization.json",ROOT/"pair_intent.json",ctx/"control/approval.json",
                  ctx/"runner.sbatch",run/"submission.claim.json"]
        evidence.extend(p for p in sorted((ctx/"control").glob("*.json")) if p not in evidence)
        evidence.extend(p for p in sorted((ctx/"evidence").rglob("*")) if p.is_file())
        evidence.extend(p for p in (ctx/"submission.json",ctx/"submit_response.json",run/"job_start.json",run/"job_end.json") if p.exists())
        archive(ROOT,report,evidence)
        hashes={p.name:base["sha"](p) for p in (report,full)}
        (out/"SHA256SUMS").write_text("".join(f"{h}  {n}\n" for n,h in hashes.items()))
        lib["publish_return"](ctx,dict(r,directory=out.name,archive_hashes=hashes))
        print(f"{arm} JOB_ID={jid} STATE={terminal['state']} W9={w9} {disposition}",flush=True)


def inspect(action,lib):
    for arm in ARMS:
        ctx=context(arm)
        jid=confirmed_job(arm)
        if not jid:
            state="SUBMISSION_UNCONFIRMED" if (ctx/case(arm)/"submission.claim.json").exists() else "NO_ACKNOWLEDGED_JOB"
            print(arm,state)
            continue
        if action=="RETURN" and not (ctx/"return.json").is_file():
            try:
                collect(arm,jid,lib,False)
            except BlockingIOError:
                print(arm,"LIVE_MONITOR_OR_COLLECTION_IN_PROGRESS")
        p=ctx/"return.json"
        if p.is_file():
            r=read(p)
            need(r["job_id"]==jid and r["role"]==arm and re.fullmatch(r"collection_[a-zA-Z0-9_]+",r["directory"]),"return pointer")
            print(f"{arm} JOB_ID={jid} STATE={r['scheduler']['state']} RUNNER_RC={r['runner_rc']} "
                  f"FRAMES={r['frame_count']} W9={r['w9']} RETURN_READY={str(r['return_ready']).upper()} "
                  f"{r['disposition']}")
            if action=="RETURN":
                print("COPY",arm,r["directory"])
        else:
            acct=lib["rotation"]["account"](jid)
            rows=[r.split("|") for r in acct.splitlines() if r.split("|")[0]==jid]
            print(arm,"JOB_ID="+jid,"STATE="+(rows[0][1] if len(rows)==1 else "ACCOUNTING_PENDING"),
                  "FRAMES="+str(sum(1 for _ in (ctx/case(arm)/"post").glob("mix_*.liggghts"))))


if __name__=="__main__":
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("action",choices=[GO,"STATUS","RETURN","monitor"])
    a.add_argument("args",nargs="*")
    opt=a.parse_args()
    lib=library()
    if opt.action=="monitor":
        need(len(opt.args)==2 and opt.args[0] in ARMS,"monitor input")
        collect(*opt.args,lib,True)
    else:
        need(not opt.args,"unexpected arguments")
        if opt.action==GO:
            launch(lib)
        else:
            inspect(opt.action,lib)
