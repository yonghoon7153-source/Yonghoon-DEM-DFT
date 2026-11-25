"""Pair scheduling and read-only return archive verification for the local operator."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import signal
import subprocess
import sys
import tarfile
import time

def require(ok, text):
    if not ok:
        raise ValueError(text)

def topology(cpu):
    folder = Path(f"/sys/devices/system/cpu/cpu{cpu}/topology")
    ids = tuple(int((folder/key).read_text()) for key in ("physical_package_id","core_id"))
    require(min(ids)>=0,"WSL physical-core topology unavailable")
    return ids

def choose_cores(mapping):
    ordered = sorted(mapping)
    if ordered:
        first = ordered[0]
        for second in ordered[1:]:
            if mapping[first] != mapping[second]:
                return {"S":first,"F":second}
    raise ValueError("two distinct eligible physical cores required")

def eligible():
    return choose_cores({k:topology(k) for k in os.sched_getaffinity(0)})

def validate_execution(results):
    require(set(results)=={"S","F"},"two arm timing receipts required")
    for name,r in results.items():
        require(r["arm"]==name and r["affinity"]==[r["cpu"]] and r["threads"]==1 and r["rc"]==0,
                "arm execution incomplete or wrong affinity")
    s,f = results["S"],results["F"]
    require(s["cpu"]!=f["cpu"] and s["core"]!=f["core"],"same core")
    require(max(s["started_ns"],f["started_ns"]) < min(s["ended_ns"],f["ended_ns"]), "arms did not overlap")

def run_pair(root,run,sdir,fdir):
    from importlib.util import spec_from_file_location, module_from_spec
    spec=spec_from_file_location("q13",root/"q13.py")
    q=module_from_spec(spec)
    spec.loader.exec_module(q)
    cpus=eligible()
    pending={}
    all_jobs=[]
    records={}
    def stop(signum,_frame):
        raise InterruptedError(f"received signal {signum}")
    for sig in (signal.SIGHUP,signal.SIGTERM):
        signal.signal(sig,stop)
    try:
        for arm,cpu in cpus.items():
            command=["taskset","-c",str(cpu),sys.executable,"-I","-X","utf8","-B",str(root/"q13.py"),
                     "arm",str(root),str(sdir),str(fdir),"--run",str(run),"--arm",arm,"--cpu",str(cpu)]
            with (run/(arm+"36.log")).open("xb") as log:
                start=time.time_ns()
                mono=time.monotonic()
                proc=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            all_jobs.append(proc)
            pending[arm]=(proc,start,mono)
            print(f"{arm}36_BEGIN cpu={cpu} core={topology(cpu)} utc_ns={start}",flush=True)
        while pending:
            for arm,(proc,start,mono) in list(pending.items()):
                cpu=cpus[arm]
                rc=proc.poll()
                if rc is None and time.monotonic()-mono > q.BUDGET[arm]+30:
                    proc.kill()
                    proc.wait()
                    rc=124
                if rc is None:
                    continue
                bind=run/(arm+"_affinity.json")
                row=json.loads(bind.read_bytes()) if bind.is_file() else dict(arm=arm,cpu=cpu,core=list(topology(cpu)),affinity=[],threads=0)
                require(row["cpu"]==cpu and row["core"]==list(topology(cpu)),"worker affinity vs assignment")
                row.update(started_ns=start,ended_ns=time.time_ns(),rc=rc)
                records[arm]=row
                del pending[arm]
                print(f"{arm}36_RC={rc}",flush=True)
            if pending:
                time.sleep(.5)
    finally:
        for proc in all_jobs:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
        with (run/"execution.json").open("x") as stream:
            json.dump(records,stream,indent=2,sort_keys=True)
    validate_execution(records)

def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()

def checks(folder, required):
    lines=(folder/"SHA256SUMS").read_text("ascii").splitlines()
    entries=[line.split("  ",1) for line in lines]
    require(len(entries)==len(required) and {n for _,n in entries}==set(required),"manifest coverage")
    for value,name in entries:
        require(digest(folder/name)==value,"hash mismatch "+name)

def unpack_return(directory,temp):
    name="suyoung_q13_pair_result.tar.gz"
    checks(directory,[name,"screen.txt"])
    seen=set()
    with tarfile.open(directory/name,"r:gz") as archive:
        for item in archive:
            p=PurePosixPath(item.name)
            require(p.parts and p.parts[0]=="run" and ".." not in p.parts and str(p)==item.name
                    and p not in seen and (item.isdir() or item.isfile()), "unexpected return member")
            seen.add(p)
            dest=temp.joinpath(*p.parts)
            if item.isdir():
                dest.mkdir(exist_ok=True,parents=True)
            else:
                import shutil
                dest.parent.mkdir(exist_ok=True,parents=True)
                with archive.extractfile(item) as src,dest.open("xb") as out:
                    shutil.copyfileobj(src,out)
    run=temp/"run"
    checks(run,[p.relative_to(run).as_posix() for p in run.rglob("*") if p.is_file() and p!=run/"SHA256SUMS"])
    require((run/"screen.txt").read_bytes()==(directory/"screen.txt").read_bytes() and
            (run/"screen.txt").read_bytes().splitlines()[-1]==b"COMMAND_RC=0","incomplete return")
    print(run)

if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="cores":
        print(json.dumps(eligible()))
    elif mode=="pair":
        run_pair(*(Path(a).resolve() for a in sys.argv[2:]))
    elif mode=="unpack":
        unpack_return(*(Path(a).resolve() for a in sys.argv[2:]))
    else:
        raise ValueError("unknown mode")
