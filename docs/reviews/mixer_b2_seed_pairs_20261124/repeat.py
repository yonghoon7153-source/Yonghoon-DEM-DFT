"""One author intent, two consecutive pairs, independent from the running ladder."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
WAVES={"S2":49979687,"S3":67867967}
LEGACY=("373356","373357")
GO="GO_MIXER_B2_SEEDS_ONCE"
TERMINAL={"COMPLETED","TIMEOUT","FAILED","CANCELLED","PREEMPTED","OUT_OF_MEMORY","NODE_FAIL",
          "BOOT_FAIL","DEADLINE","REVOKED","SPECIAL_EXIT"}
ACTIVE={"PENDING","RUNNING","COMPLETING","CONFIGURING","SUSPENDED","RESIZING","REQUEUED",
        "REQUEUE_FED","SIGNALING","STAGE_OUT","STOPPED"}

def need(ok,why):
    if not ok:
        raise ValueError(why)

def state_of(account,jid):
    rows=[r.split("|") for r in account.splitlines() if r.split("|")[0].strip()==jid]
    need(len(rows)<=1,"ambiguous scheduler accounting "+jid)
    return rows[0][1].strip().split()[0] if rows and len(rows[0])>=3 and rows[0][1].strip() else ""

def finished(states):
    return len(states)==2 and all(s in TERMINAL for s in states)

def allocations(snapshot):
    rows={}
    for line in snapshot.splitlines():
        if not line.strip():continue
        cols=[s.strip() for s in line.split("|")]
        need(len(cols)==3,"invalid squeue row")
        j,s,n=cols
        need(re.fullmatch(r"[0-9]+(?:_[0-9]+)?(?:\+[0-9]+)?",j) and s in ACTIVE and
             n.isdigit() and int(n)>0 and j not in rows,"unknown active allocation")
        rows[j]=int(n)
    return rows

def projected_rows(rows,prior,prior_finished=False):
    if prior in rows:
        need(rows[prior]==20,"previous job CPU count changed")
    return sum(rows.values())+(20 if prior in rows or prior_finished else 40)

def read(path):return json.loads(path.read_bytes())

def checksum(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def source_check():
    m=read(ROOT/"campaign.json")
    need(m["seeds"]==WAVES and m["predecessors"]==list(LEGACY),"wrong campaign registration")
    for n,h in m["files"].items():
        path=ROOT/n
        need(path.resolve()==path and path.is_file() and checksum(path)==h,"source drift "+n)
    return m

def wave(name):
    need(name in WAVES,"unknown pair")
    spec=importlib.util.spec_from_file_location("frozen_ladder",ROOT/"ladder_base.py")
    a=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a)
    a.ROOT=ROOT/name
    a.ARMS=(name+"U",name+"C")
    return a

def clock():return time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())

def command(argv):
    while True:
        try:
            return subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,
                                  check=True,timeout=60).stdout
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired):
            progress("WAIT_SCHEDULER_QUERY "+argv[0])
            time.sleep(60)

def account(jid):
    return state_of(command(["sacct","-n","-P","-j",jid,"-o","JobIDRaw,State%40,ExitCode"]),jid)

def queue():
    return command(["squeue","--array","-h","-u",os.environ["USER"],"-o","%i|%T|%C"])

def progress(state):
    print(clock(),state,flush=True)
    dest=ROOT/"progress.json"
    tmp=dest.with_suffix(".tmp")
    tmp.write_text(json.dumps(dict(utc=clock(),state=state))+"\n")
    tmp.replace(dest)

def wait_done(jobs):
    prev=None
    while True:
        states=[account(j) for j in jobs]
        if finished(states) and not set(jobs).intersection(allocations(queue())):return
        if states!=prev:
            progress("WAIT "+str(dict(zip(jobs,states))))
            prev=states
        time.sleep(45)

def room(prior=None):
    warned=False
    while True:
        rows=allocations(queue())
        n=projected_rows(rows,prior)
        if n>60 and prior and prior not in rows and account(prior) in TERMINAL:
            n=projected_rows(allocations(queue()),prior,prior_finished=True)
        if n<=60:return n
        if not warned:
            progress("WAIT_CAPACITY projected=%d/60"%n)
            warned=True
        time.sleep(45)

def launch():
    need(socket.gethostname().split(".")[0]=="ibb-master" and not any(k.startswith(("SLURM_","SBATCH_","SRUN_","SALLOC_")) for k in os.environ),"wrong login context")
    m=source_check()
    a=wave("S2")
    a.put(ROOT/"intent.json",dict(mode=GO,pin=m["pin"],utc=clock(),seeds=WAVES))
    predecessors=LEGACY
    for name,seed in WAVES.items():
        wait_done(predecessors)
        room()
        a=wave(name)
        lib=a.library()
        release=a.verify(lib["base"])
        runtime=a.environment()
        a.put(a.ROOT/"authorization.json",dict(token=GO,levels=release["arms"],seed=seed,release=m["pin"]))
        a.put(a.ROOT/"pair_intent.json",dict(arms=a.ARMS,seed=seed,prior_jobs=predecessors,utc=clock()))
        for arm in a.ARMS:
            a.setup(arm,lib,runtime,release)
        jobs=[]
        for arm in a.ARMS:
            n=room(jobs[0] if jobs else None)
            a.put(a.context(arm)/"capacity.json",dict(utc=clock(),projected=n,prior=jobs[:]))
            jid=a.submit(arm,lib["base"])
            need(jid not in (*jobs,*predecessors),"duplicate scheduler identity")
            a.monitor_detached(arm,jid)
            jobs.append(jid)
        predecessors=jobs
        progress("SUBMITTED "+str(dict(zip(a.ARMS,jobs))))
    progress("FOUR_SUBMISSIONS_ACKNOWLEDGED")

def show(action):
    source_check()
    if (ROOT/"progress.json").exists():
        print(read(ROOT/"progress.json")["state"])
    for name in WAVES:
        a=wave(name)
        a.inspect(action,a.library())

def monitor(name,arm,jid):
    source_check()
    a=wave(name)
    need(arm in a.ARMS and re.fullmatch(r"[1-9]\d*",jid),"wrong detached monitor arguments")
    a.collect(arm,jid,a.library(),True)

if __name__=="__main__":
    try:
        mode,=sys.argv[1:]
        if mode==GO:
            import fcntl
            with (ROOT/"coordinator.lock").open("ab") as lock:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                launch()
        elif mode in ("STATUS","RETURN"):
            show(mode)
        else:raise ValueError("action")
    except Exception as ex:
        print("DISPATCH_STOP",str(ex),file=sys.stderr,flush=True)
        sys.exit(2)
