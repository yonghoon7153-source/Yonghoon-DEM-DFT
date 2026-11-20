"""Offline Linux exercise of both arm approvals through the frozen canonical submitter.

Arguments: exact previously deployed N0 source tar and exact N0 return pointer.
Stages private copies in a fresh temporary directory. No actual scheduler, MPI or DEM.
"""
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tarfile
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
sys.path.insert(0,str(REPO/"scripts"))
import mixer_b1_pair_ibb as driver
N0_SOURCE="cef09eea445c5080231d906275d6cad187f4260c22d3f8549b126c147c3641f8"

def test(source,n0_pointer):
    if not sys.platform.startswith("linux") or driver.sha(source)!=N0_SOURCE or driver.sha(n0_pointer)!=driver.N0_POINTER:
        raise ValueError("Linux or source identity")
    with tempfile.TemporaryDirectory() as work:
        root=Path(work)/"packet"
        root.mkdir()
        with tarfile.open(source) as t:
            for m in t:
                name=m.name
                if (name.startswith("packet/B/") or name in ("packet/control/runtime_reference.json",
                      "packet/B_manifest.json","packet/control/AB_RECEIPT.json")):
                    target=Path(work)/driver.base["safe_rel"](name)
                    assert m.isfile()
                    target.parent.mkdir(parents=True,exist_ok=True)
                    with target.open("xb") as out:
                        out.write(t.extractfile(m).read())
        shutil.copyfile(n0_pointer,root/"control/n0_return.json")
        pin="1"*40
        driver.put(root/"control/pair_pin.json",{"commit":pin})
        runtime=tuple(Path(work)/k for k in ("sim","mpirun","prefix"))
        for file in runtime[:2]:
            file.write_bytes(b"synthetic runtime")
        runtime[2].mkdir()
        jids=iter(("5101","5102"))
        submitted=[]
        def fake_sbatch(argv,**kwargs):
            assert argv[:4]==["sbatch","--parsable","--no-requeue","--partition=cpu"]
            assert "--ntasks=20" in argv and "--time=2-00:00:00" in argv and "--nodes=1" in argv
            assert not any("--array" in a for a in argv)
            jid=next(jids)
            submitted.append(jid)
            return SimpleNamespace(stdout=jid+"\n",stderr="",returncode=0)
        def live(root,ctx,*args):
            import time
            output=ctx/"evidence/mock_live.json"
            driver.put(output,dict(observed_unix=time.time(),running_first8=0,reserved_cpus=0,
                              qos="cpu-60",partition="cpu",qos_verified=True,disk_budget_verified=True,
                              inode_budget_verified=True,d07_finished=True,paths_verified=True,
                              qualification_accepted=True))
            return output
        def account(jid):
            return jid+"|COMPLETED|0:0|\n"
        with patch.object(driver,"runtime_preflight",live), patch.dict(driver.rotation,account=account), \
             patch.dict(driver.base,runtime=lambda *a: {"matches":True}), \
             patch.dict(os.environ,{"PATH":os.environ["PATH"],"HOME":work,"USER":"test"},clear=True):
            for role in ("U","C"):
                cmd,ap=driver.prepare(root,role,"GO_B1_"+role+"_ONCE",pin,runtime)
                with patch.object(subprocess,"run",fake_sbatch):
                    runpy.run_path(str(cmd))["main"](str(ap))
                case=root/"B"/driver.F8/"cases"/driver.case_name(role)
                jid=json.loads((case/"submission.receipt.json").read_bytes())["job_id"]
                assert jid==submitted[-1]
                driver.put(case/"job_end.json",dict(job_id=jid,returncode=0,end_unix=driver.time.time()))
                (case/"post").mkdir()
                for i in range(1,235):
                    (case/"post"/("mix_%d.liggghts"%(i*32976))).write_bytes(b"fixture")
                assert driver.collect(root,role,jid,account(jid),runtime,True,pin)==0
                ret=driver.read(root/"arms"/role/"return.json")
                assert driver.verified_sums(root/"arms"/role/ret["directory"])==ret["archive_hashes"]
            assert submitted==["5101","5102"]
            path=root/"B"/driver.F8/"admission"
            assert sorted(i.name for i in path.iterdir())==sorted(driver.case_name(role)+suffix
                    for role in ("U","C") for suffix in (".reservation.json",".submission.json"))
            checks=driver.read(root/"B"/driver.F8/"campaign_policy.json")
            assert checks["max_concurrency"]==2 and checks["np"]==20
            print("CANONICAL_U_C_OK mocked sbatch 2, actual 0, reservations 2, return hashes 4")
if __name__=="__main__":
    test(*map(Path,sys.argv[1:]))
