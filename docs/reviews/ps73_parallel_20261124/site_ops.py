"""Login-node controller for one isolated development release."""
import datetime
import fcntl
import getpass
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
import zipfile

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import parallel as p
import engine as e

OPS=e.OPS

def command(args):
    env={k:v for k,v in os.environ.items() if k in ("PATH","HOME","USER","LANG","LC_ALL","LOGNAME","LD_LIBRARY_PATH","SHELL","TMPDIR")}
    env.update(LC_ALL="C")
    return subprocess.run(args,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          universal_newlines=True,timeout=45).stdout

def queue():
    return command(["squeue","--array","-h","-u",getpass.getuser(),"-o","%i|%T|%C"])

def acct(jid):
    raw=command(["sacct","-n","-P","-j",jid,"-o","JobIDRaw,State%40,ExitCode,Elapsed,Timelimit"])
    rows=[row.split("|") for row in raw.splitlines() if row.split("|")[0].strip()==jid]
    if not rows:
        return dict(state="ACCOUNTING_PENDING",job=jid)
    p.need(len(rows)==1 and len(rows[0])>=5,"ambiguous accounting "+jid)
    _,state,code,elapsed,limit=map(str.strip,rows[0][:5])
    return dict(job=jid,state=state.split()[0],exit_code=code,elapsed=elapsed,limit=limit)

def attempts(arm):
    base=OPS/"attempts"/arm
    return sorted(base.iterdir()) if base.is_dir() else []

def paths(arm):
    return p.arm_dir(OPS,e.ROOT,arm)

def last(arm):
    seq=attempts(arm)
    if not seq:
        return (None,acct(p.UB_JOB)) if arm=="UB" else (None,{"state":"WAITING"})
    d=seq[-1]
    if not (d/"ack.json").is_file():
        return d,dict(state="SUBMISSION_AMBIGUOUS",attempt=d.name)
    return d,acct(p.read(d/"ack.json")["job"])

def capacity(n):
    unseen={}
    for arm in p.ARMS:
        d,view=last(arm)
        if view["state"] in p.ACTIVE|{"ACCOUNTING_PENDING"}:
            unseen[view["job"]]=6
        p.need(view["state"]!="SUBMISSION_AMBIGUOUS","unresolved submission "+arm)
    return p.projected(queue(),n,unseen)

def submit(arm,meta=None,previous=None):
    p.need(arm in p.ARMS and (arm!="UB" or meta is not None),"invalid arm dispatch")
    e.reserved()
    intent=OPS/"intent.json"
    if intent.exists():
        p.need(p.read(intent)["source_manifest"]==p.digest(HERE/"SOURCE_SHA256SUMS"),"installed source changed")
    projected=capacity(6)
    # Create the journal only after the resource check. Even an interrupted
    # sbatch can never result in a second submission at this journal position.
    base=OPS/"attempts"/arm
    base.mkdir(parents=True,exist_ok=True)
    d=base/("%06d"%(len(attempts(arm))+1))
    d.mkdir()
    rec=dict(arm=arm,resume=meta,previous=previous,projected_user_cpus=projected)
    def send():
        out=command(["sbatch","--parsable","--no-requeue","--nodes=1","--ntasks=6","--cpus-per-task=1",
             "--partition=cpu","--qos=cpu-60","--time=5-00:00:00","--job-name=ps73_"+arm,
             "--chdir="+str(d),"--output="+str(d/"slurm.out"),"--error="+str(d/"slurm.err"),
             str(HERE/"batch.sh"),str(HERE),arm,str(d),p.digest(HERE/"SOURCE_SHA256SUMS")]).strip()
        if not re.fullmatch(r"[1-9]\d*(?:;[A-Za-z0-9_.-]+)?",out):
            raise ValueError("ambiguous sbatch reply")
        return out.split(";")[0]
    job=p.claim_submit(d,rec,send)
    print("SUBMITTED",arm,job,"NP6 projected",projected,flush=True)

def result(arm):
    return OPS/"results"/(arm+".json")

def finish(arm,d,v):
    p.need(v.get("exit_code")=="0:0","nonzero exit "+arm)
    if d is None:
        rec=e.original.outcome(e.ROOT,"UB",p.UB_JOB)
        receipt=p.read(e.STATE/"jobs"/"UB"/"node_finished.json")
        p.need(receipt["job_id"]==p.UB_JOB and p.ub_ready(v["state"],receipt)
               and receipt["manifest_sha256"]==rec["manifest_sha256"]
               and receipt["verdict_sha256"]==rec["verdict_sha256"],"old UB return identity")
        verdict=p.read(e.ROOT/p.BED/"UB"/"arm_verdict.json")
    else:
        rec=p.read(d/"finished.json")
        jd=paths(arm)
        p.need(rec["job"]==v["job"] and rec["arm"]==arm and rec["runner_rc"]==0 and
               rec["manifest"]==p.digest(jd/"run_manifest.txt") and
               rec["verdict"]==p.digest(jd/"arm_verdict.json"),"invalid individual receipt "+arm)
        verdict=p.read(jd/"arm_verdict.json")
    p.need(verdict["job"]==arm and verdict["bed"]==p.BED,"wrong individual verdict")
    p.publish(result(arm),dict(scheduler=v,receipt=rec,verdict=verdict))

def decision(results,reader,params):
    receipts={arm:r["receipt"] for arm,r in results.items()}
    if not all(receipts[a]["technical_ok"] for a in ("UT","UB","UC")) or not receipts["UC"]["control_ok"]:
        return dict(stage="TECHNICAL_HOLD",next=[],UVa_role="undetermined")
    ub,ut,uv=(results[a]["verdict"] for a in ("UB","UT","UVa"))
    if not all(receipts[a]["endpoint_usable"] for a in ("UB","UT")):
        return dict(stage="SELECTION_UNRESOLVED",next=[],UVa_role="undetermined")
    valid=reader._valid_rho(ub) and reader._valid_rho(ut)
    use_uva=valid and reader._le(abs(ub["rho_pct"]-ut["rho_pct"]),params["selection"]["delta_max_pp"])
    if use_uva and not (receipts["UVa"]["technical_ok"] and receipts["UVa"]["endpoint_usable"]):
        return dict(stage="SELECTION_UNRESOLVED",next=[],UVa_role="selected_for_speed_comparison")
    verdict=reader.selection(ub,ut,uv if use_uva else None,params)
    role="selected_for_speed_comparison" if use_uva else ("auxiliary" if valid else "undetermined")
    return dict(verdict,UVa_role=role,threshold_pp=params["selection"]["delta_max_pp"],
                separate_GO_required_for_UVb=bool(valid and not use_uva))

def process(arm):
    if result(arm).exists() or (OPS/"results"/(arm+".hold.json")).exists():
        return
    d,v=last(arm)
    state=v["state"]
    if state=="WAITING":
        if arm=="UVa":
            if not result("UB").is_file():
                return
            ub=p.read(result("UB"))
            p.need(p.ub_ready(ub["scheduler"]["state"],ub["receipt"]),"UB technical readback did not qualify")
        submit(arm)
    elif state=="COMPLETED":
        finish(arm,d,v)
    elif state=="TIMEOUT":
        jd=paths(arm) if d is not None else e.ROOT/p.BED/"UB"
        p.need(arm in ("UB","UT","UVa") and not (jd/"ul_summary.txt").exists(),"no eligible restart "+arm)
        previous=p.read(d/"ack.json")["resume"] if d else None
        meta=p.checkpoint(jd)
        p.need(p.resume_ok(arm,state,meta["step"],previous["step"] if previous else p.S0),"NO_FORWARD_CHECKPOINT")
        submit(arm,meta,d.name if d else None)
    elif state not in p.ACTIVE|{"ACCOUNTING_PENDING"}:
        raise ValueError("review terminal or ambiguous state "+state+" "+arm)

def final_inputs(reader,params):
    rows={a:p.read(result(a)) for a in p.ARMS}
    for arm,obj in rows.items():
        external=arm=="UB" and obj["scheduler"]["job"]==p.UB_JOB
        d=e.ROOT/p.BED/"UB" if external else paths(arm)
        receipt=obj["receipt"]
        key="verdict_sha256" if external else "verdict"
        man="manifest_sha256" if external else "manifest"
        p.need(p.digest(d/"arm_verdict.json")==receipt[key] and p.digest(d/"run_manifest.txt")==receipt[man],
               "source changed before final readback "+arm)
        again,usable,control=e.assess(reader,params,d,arm)
        p.need(all(again.get(k)==obj["verdict"].get(k) for k in ("rho_pct","primary_status","trajectory_status")),
               "final original readback disagrees "+arm)
        receipt["endpoint_usable"]=usable
        receipt["control_ok"]=control
    return rows

def loop():
    e.reserved()
    if not any(attempts(a) for a in ("UT","UC")):
        kit=e.original.pinned_kit(e.ROOT)
        e.reader(kit)
        _,_,_,ident=e.inputs(kit,"UT")
        for a in ("UT","UC"):
            e.original.check_gate(e.ROOT,kit,a,e.HOME/".conda/envs/myenv/bin/python3")
        capacity(12)
        if not (OPS/"source.json").exists():
            p.publish(OPS/"source.json",ident)
    while not (OPS/"final.json").exists():
        for arm in p.ARMS:
            try:
                process(arm)
            except ValueError as ex:
                if "CAPACITY_STOP" in str(ex) or "unresolved submission" in str(ex):
                    raise
                h=OPS/"results"/(arm+".hold.json")
                if not h.exists():
                    p.publish(h,dict(arm=arm,reason=str(ex),utc=e.original.now()))
        if all(result(arm).exists() for arm in p.ARMS):
            kit=e.original.pinned_kit(e.ROOT)
            old=e.reader(kit)
            params=p.read(kit/"unload_params.json")
            sel=decision(final_inputs(old,params),old,params)
            p.publish(OPS/"final.json",dict(selection=sel,development_only=True,
                      receipt_hashes={a:p.digest(result(a)) for a in p.ARMS}))
            return
        h=OPS/"results"
        if (h/"UB.hold.json").exists() and not result("UVa").exists() and not (h/"UVa.hold.json").exists():
            p.publish(h/"UVa.hold.json",dict(reason="UB terminal receipt pending review"))
        if all(result(a).exists() or (h/(a+".hold.json")).exists() for a in p.ARMS):
            return
        time.sleep(45)

def status():
    left=command(["squeue","--array","-h","-u",getpass.getuser(),"-o","%i|%L"])
    times=dict(x.strip().split("|") for x in left.splitlines() if x.strip())
    arms={}
    for arm in p.ARMS:
        d,v=last(arm)
        if v.get("job") in times:
            v["time_left"]=times[v["job"]]
        if d:
            v["segment"]=d.name
            ack=d/"ack.json"
            if ack.is_file():
                c=p.read(ack)["resume"]
                v["restart_step"]=c["step"] if c else None
        hold=OPS/"results"/(arm+".hold.json")
        if hold.exists():
            v["hold"]=p.read(hold)
        arms[arm]=v
    pidfile=OPS/"monitor.pid"
    pid=pidfile.read_text().strip() if pidfile.exists() else ""
    proc=Path("/proc")/pid/"cmdline"
    try:
        live=bool(pid and proc.is_file() and b"DAEMON" in proc.read_bytes().split(b"\0"))
    except FileNotFoundError:
        live=False
    logs=sorted(OPS.glob("monitor_*.log"))
    tail=[]
    if logs:
        with logs[-1].open("rb") as f:
            f.seek(max(0,logs[-1].stat().st_size-3000))
            tail=f.read().decode(errors="replace").splitlines()[-4:]
    # The live run can be appending the newest state. This is a progress
    # indicator only; the actual continuation validates both files after exit.
    live_dir=e.ROOT/p.BED/"UB" if not attempts("UB") else paths("UB")
    steps=[]
    for file in (live_dir/"restart").glob("state_unload_*.in"):
        m=re.fullmatch(r"state_unload_(\d+)\.in",file.name)
        if m and file.is_file() and (file.parent/("restart_unload_"+m[1]+".bin")).is_file():
            steps.append(int(m[1]))
    arms["UB"]["last_observed_checkpoint_step"]=max(steps) if steps else None
    return dict(original_UB=acct(p.UB_JOB),arms=arms,monitor_live=live,monitor_tail=tail,
                final_ready=(OPS/"final.json").is_file(),automatic_UVb=False)

def detach():
    log=OPS/("monitor_%020d.log"%int(time.time()*1000000))
    with log.open("xb") as f:
        subprocess.Popen([sys.executable,"-I","-B",str(HERE/"site_ops.py"),"DAEMON"],stdin=subprocess.DEVNULL,
                         stdout=f,stderr=f,start_new_session=True,close_fds=True)

def archive():
    snap=status()
    base=Path(tempfile.mkdtemp(prefix="return_",dir=str(OPS)))
    src=[p for p in [OPS/"source.json",OPS/"intent.json",OPS/"final.json",*sorted((OPS/"results").glob("*.json")),
                      *sorted((OPS/"attempts").glob("*/*/*.json"))] if p.is_file()]
    raw={path.relative_to(OPS).as_posix():path.read_bytes() for path in src}
    raw["status.json"]=json.dumps(snap,sort_keys=True).encode()
    raw["SHA256SUMS"]="".join(hashlib.sha256(data).hexdigest()+"  "+name+"\n" for name,data in sorted(raw.items())).encode()
    z=base/"ps73_return.zip"
    with zipfile.ZipFile(z,"x",zipfile.ZIP_DEFLATED) as out:
        for name,data in raw.items():
            out.writestr(name,data)
    print(base.name,p.digest(z),"FINAL" if "final.json" in raw else "PARTIAL")

def main(args):
    mode=args[0]
    if mode=="WORKER":
        e.worker(args[1],Path(args[2]))
        return
    p.need(socket.gethostname().split(".")[0]=="ibb-master","wrong login host")
    if mode=="DAEMON":
        with (OPS/"monitor.lock").open("ab") as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            (OPS/"monitor.pid").write_text(str(os.getpid()))
            loop()
    elif mode==p.GO:
        e.reserved()
        capacity(12)
        (OPS/"results").mkdir()
        p.publish(OPS/"intent.json",dict(mode=p.GO,UB=p.UB_JOB,utc=e.original.now(),source_manifest=p.digest(HERE/"SOURCE_SHA256SUMS")))
        detach()
    elif mode=="RESUME":
        p.need(p.read(OPS/"intent.json")["mode"]==p.GO and not (OPS/"final.json").exists(),"no live intent")
        if not status()["monitor_live"]:
            detach()
    elif mode=="STATUS":
        print(json.dumps(status(),sort_keys=True))
    elif mode=="INITIAL_STATUS":
        for _ in range(25):
            if all(any((d/"ack.json").is_file() for d in attempts(a)) for a in ("UT","UC")):
                break
            if list((OPS/"results").glob("*.hold.json")):
                break
            time.sleep(2)
        print(json.dumps(status(),sort_keys=True))
    elif mode=="RETURN":
        archive()
    else:
        raise ValueError("unknown mode")

if __name__=="__main__":
    os.umask(0o077)
    try:
        main(sys.argv[1:])
    except Exception as exc:
        print("PS73_STOP "+str(exc),file=sys.stderr,flush=True)
        sys.exit(2)
