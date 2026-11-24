"""Use the actual NP20 launcher, archiver and local verifier against an offline simulator stand-in."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

def module(name,p):
    spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def check(package):
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp).resolve()
        with tarfile.open(package) as t:
            for m in t:
                p=root/m.name
                assert m.isfile() and root in p.resolve().parents
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(t.extractfile(m).read())
        r=module("repeat_test",root/"repeat.py")
        rb=module("readback_test",root/"readback.py")
        manifest=r.source_check()
        a=r.wave("S2");lib=a.library();base,rot=lib["base"],lib["rotation"]
        release=a.verify(base)
        mpi=root/"fixture_mpi"
        mpi.write_text('#!/bin/bash\ntest "$5" = 20 && test "$8" = in.mixer\n')
        mpi.chmod(0o700)
        binary=root/"fake_simulator";binary.write_text("fixture")
        runtime=(binary,mpi,root)
        def stamp(ctx,*args):
            f=ctx/"evidence"/args[-1]/"runtime.json"
            f.parent.mkdir(parents=True)
            a.put(f,dict(matches=True))
            return a.read(f)
        def capture(_,label,argv,*args):
            return {"assoc":"tester|cpu-60|3-00:00:00","partition":"State=UP MaxTime=3-00:00:00",
                    "qos":"cpu-60|cpu=60","wall":"cpu-60|2-00:00:00",
                    "df":"header\nfs 900000000000 1 800000000000 1% /","inode":"header\nfs 90000000 1 80000000 1% /",
                    "ost":"fs-OST0 900000000 1 800000000 1% /","quota":"fixture"}[label],{}
        a.put(a.ROOT/"authorization.json",dict(token=r.GO,seed=r.WAVES["S2"]))
        a.put(a.ROOT/"pair_intent.json",dict(arms=a.ARMS))
        for i,arm in enumerate(a.ARMS):
            jid=str(101+i)
            state="COMPLETED" if i==0 else "TIMEOUT"
            def scheduler(argv,_):
                assert argv[0]=="sbatch" and "--ntasks=20" in argv and "--time=2-00:00:00" in argv
                return SimpleNamespace(returncode=0,stdout=jid+"\n",stderr="")
            def accounting(job):
                assert job==jid
                return job+"|"+state+"|0:0|0|0|0\n"
            with patch.dict(os.environ,{"USER":"tester"}),patch.object(a,"environment",return_value=runtime), \
                 patch.dict(base,{"runtime":stamp,"capture":capture,"command":scheduler}), \
                 patch.dict(rot,{"account":accounting,"monitor":lambda _,j:accounting(j)}):
                a.setup(arm,lib,runtime,release)
                assert a.submit(arm,base)==jid
                ctx=a.context(arm);run=ctx/a.case(arm)
                if i==0:
                    env=dict(os.environ,SLURM_NTASKS="20",SLURM_JOB_PARTITION="cpu",SLURM_JOB_QOS="cpu-60",
                             SLURM_CPUS_PER_TASK="1",SLURM_JOB_NUM_NODES="1",SLURM_JOB_ID=jid)
                    subprocess.run(["bash",str(ctx/"runner.sbatch")],env=env,cwd=run,check=True)
                    (run/"post").mkdir()
                    for n in range(1,235):(run/"post"/("mix_%d.liggghts"%(n*32976))).touch()
                    (run/"log.liggghts").write_text("fixture")
                a.collect(arm,jid,lib,True)
                receipt=a.read(ctx/"return.json")
                folder=ctx/receipt["directory"]
                (folder/"return.json").write_bytes((ctx/"return.json").read_bytes())
                checked=rb.verify_return(folder,arm,manifest)
                assert checked["disposition"]==("COMPLETE" if i==0 else "TECH_MISSING_TIMEOUT")
                if i==0:
                    staging=root/"staged"
                    assert rb.extract(folder/"b2_full_result.tar.gz",staging,arm,jid).name==a.case(arm)
                    (folder/"return.json").write_text(json.dumps(dict(receipt,w9="STALE")))
                    try:rb.verify_return(folder,arm,manifest)
                    except ValueError:pass
                    else:raise AssertionError("stale W9 admitted")
        print("NATIVE_NP20_JOB_START_RECEIPT_W9_FRAMES_TIMEOUT_AND_TAMPER_OK")
if __name__=="__main__":check(sys.argv[1])
