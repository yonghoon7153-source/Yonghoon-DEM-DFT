"""Offline integration check. Uses a local dummy MPI command and a simulated scheduler."""
import argparse
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
from types import SimpleNamespace
from unittest import mock


def check(ok, reason):
    if not ok:
        raise AssertionError(reason)


def validate(package):
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp).resolve()
        with tarfile.open(package) as tar:
            for member in tar:
                rel=Path(member.name)
                check(member.isfile() and not rel.is_absolute() and ".." not in rel.parts,"package path")
                p=root/rel
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(tar.extractfile(member).read())
        spec=importlib.util.spec_from_file_location("ladder_test_target",root/"ladder.py")
        app=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app)
        lib=app.library()
        base,rot=lib["base"],lib["rotation"]
        states={}
        watches=[]
        received=[]
        mpi=root/"dummy_mpi"
        mpi.write_text('#!/bin/sh\n[ "$1" = --oversubscribe ] && [ "$6" = "$DUMMY_EXEC" ] && [ "$8" = in.mixer ]\n')
        mpi.chmod(0o700)
        binary=root/"dummy_simulator"
        binary.write_text("# local fixture only\n")
        runtime=(binary,mpi,root)
        def fake_runtime(ctx,*args):
            p=ctx/"evidence"/args[-1]/"runtime.json"
            p.parent.mkdir(parents=True)
            app.put(p,{"matches":True})
            return app.read(p)
        def capture(_,label,argv,*args):
            if label=="queue_before_submission":
                check(argv[-1]=="%i|%T|%C","queue columns")
                return "368469|RUNNING|6\n",{}
            return {"assoc":"author|cpu-60|3-00:00:00","partition":"State=UP MaxTime=3-00:00:00",
                    "qos":"cpu-60|cpu=60","wall":"cpu-60|2-00:00:00",
                    "df":"header\nfs 900000000000 1 800000000000 1% /","inode":"header\nfs 90000000 1 80000000 1% /",
                    "ost":"fs-OST0 900000000 1 800000000 1% /","quota":"fixture"}[label],{}
        def command(argv,_):
            arm=app.ARMS[len(received)]
            path=app.context(arm)/app.case(arm)
            check(argv[0]=="sbatch" and "--no-requeue" in argv and "--ntasks=20" in argv
                  and "--time=2-00:00:00" in argv and "--chdir="+str(path) in argv, "scheduler request")
            jid=str(101+len(received))
            received.append((arm,jid))
            states[jid]="RUNNING"
            return SimpleNamespace(returncode=0,stdout=jid+"\n",stderr="")
        def acct(jid):
            return jid+"|"+states[jid]+"|0:0|0|0|0\n"
        with mock.patch.dict(base,{"runtime":fake_runtime,"capture":capture,"command":command}), \
             mock.patch.dict(rot,{"account":acct,"monitor":lambda _,j:acct(j)}), \
             mock.patch.object(app,"environment",return_value=runtime), \
             mock.patch.object(app,"monitor_detached",side_effect=lambda a,j:watches.append((a,j))), \
             mock.patch.dict(os.environ,{"USER":"author","DUMMY_EXEC":str(binary)},clear=False):
            app.launch(lib)
            check(watches==received==[("L020","101"),("L050","102")],"distinct submitted jobs")
            app.inspect("RETURN",lib)
            check(not any(app.context(a).joinpath("return.json").exists() for a in app.ARMS),"pending return")
            for arm,jid in received:
                ctx=app.context(arm)
                run=ctx/app.case(arm)
                if arm=="L020":
                    env=dict(os.environ,SLURM_NTASKS="20",SLURM_JOB_PARTITION="cpu",SLURM_JOB_QOS="cpu-60",
                             SLURM_CPUS_PER_TASK="1",SLURM_JOB_NUM_NODES="1",SLURM_JOB_ID=jid)
                    subprocess.run(["bash",str(ctx/"runner.sbatch")],env=env,cwd=run,check=True)
                    check(app.read(run/"job_end.json")["returncode"]==0,"actual immutable job starter")
                    (run/"post").mkdir()
                    for i in range(1,235):
                        (run/"post"/f"mix_{i*32976}.liggghts").touch()
                    states[jid]="COMPLETED"
                else:
                    states[jid]="TIMEOUT"
                app.collect(arm,jid,lib,True)
                r=app.read(ctx/"return.json")
                check(r["disposition"]==("COMPLETE" if arm=="L020" else "TECH_MISSING_TIMEOUT"),"return classification")
                folder=ctx/r["directory"]
                for n,v in r["archive_hashes"].items():
                    check(hashlib.sha256((folder/n).read_bytes()).hexdigest()==v,"archive digest")
                with tarfile.open(folder/"b2_report.tar.gz") as t:
                    terminal=json.load(t.extractfile(f"arms/{arm}/evidence/{r['directory']}.json"))
                    check(terminal=={k:v for k,v in r.items() if k not in ("archive_hashes","directory")},"terminal identity")
                check(len(list((ctx).glob("collection_*/SHA256SUMS")))==1,"exclusive terminal receipt")
            with redirect_stdout(io.StringIO()) as stream:
                app.inspect("STATUS",lib)
                app.inspect("RETURN",lib)
            check(stream.getvalue().count("COPY ")==2 and len(received)==2,"read-only actions cannot submit")
    print("TWO_ARMS_NORMAL_AND_TIMEOUT_RETURNS_OK")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("package",type=Path)
    validate(p.parse_args().package)
