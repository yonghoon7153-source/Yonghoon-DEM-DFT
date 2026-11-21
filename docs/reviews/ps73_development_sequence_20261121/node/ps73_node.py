"""Run one registered 7:3 development arm with the sealed 368315 origin."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile


BED = "ps_7_3_r45"
WORK = "ps45_a5_rj_9fd6aa9d3bee_1120_once"
OPS = "ps73_dev_ops_20261121"
PYTHON_SHA = "561c350efec08f1712162c4d649f4b668bacceb68388e973efec964f0073cd92"
MPI_SHA = "407990f94f9d3863be273b44e6e8fc96b9a015a3b14763ae0aab60857d1ee72d"
LMP_SHA = "ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f"
SUMS_SHA = "26bdbdc05ba3f6c71a0b042ebd13adb64b38271c1889a894898a4ccf55322f1d"
SITE_SHA = "b7749d2b68237d126b779e606d26d5231e9a66533ff80c7cf73b84430469fc36"
VERDICT_SHA = "b049a3707aede899f4c6badc7176eb63246da8986dea58459dbea4aae45e73e6"
MANIFEST_SHA = "d4647c1654acf8d225b2b24f64c5e0d8246328f299c057ff3c033b6e6944b5e1"
BASE_SHA = "016f0402edba632864ef0a0423a5aaf8360a7eac2054e0b5b4191917648ce272"
STAGES = {"UB":"U_UB", "UT":"UT", "UC":"UC", "UVa":"U_UVa", "UVb":"U_UVb", "UTc":"U_UT3"}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def check_arm(arm):
    need(arm in STAGES, "unsupported arm (gravity is pending REG 15-7)")


def digest_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def checked(path, expected):
    need(path.is_file() and not path.is_symlink() and digest_file(path) == expected,
         "wrong input identity: "+path.name)


def allocation(e):
    job = e.get("SLURM_JOB_ID", "")
    need(re.fullmatch(r"[1-9][0-9]*", job) and e.get("SLURM_NTASKS") == "6"
         and e.get("SLURM_JOB_NUM_NODES", e.get("SLURM_NNODES","")) == "1"
         and e.get("SLURM_CPUS_PER_TASK", "1") == "1" and e.get("SLURM_JOB_PARTITION") == "cpu"
         and e.get("SLURM_RESTART_COUNT","0") == "0" and not any(k.startswith("SLURM_ARRAY_") for k in e),
         "requires a fresh single non-array allocation, cpu partition, one node, NP6")
    return job


def fresh(root, arm):
    check_arm(arm)
    bed = root/BED
    need(not os.path.lexists(str(bed/arm)) and not os.path.lexists(str(bed/(arm+".report.tgz"))),
         "existing arm or return; no rerun")


def write_once(path, obj):
    # Complete, durable bytes before committing an exclusive receipt name.
    temp = path.with_name(path.name+".writing")
    with temp.open("x",encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=True, sort_keys=True, allow_nan=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.link(str(temp),str(path))
    temp.unlink()


def pinned_kit(root):
    kit = root/"fixed_kit"
    dirs = (root,root/BED,root/BED/"in",root/BED/"RJ",kit)
    need(all(d.is_dir() and not d.is_symlink() for d in dirs), "wrong origin directory")
    checked(kit/"A5_SHA256SUMS",SUMS_SHA)
    rows=(kit/"A5_SHA256SUMS").read_text(encoding="ascii").splitlines()
    need(len(rows)==142,"kit manifest inventory")
    for row in rows:
        sha,name=row.split("  ",1)
        checked(kit/name,sha)
    checked(root/"site_receipt.json",SITE_SHA)
    for name,sha in json.loads((root/"site_receipt.json").read_bytes())["input_sha256"].items():
        checked(root/BED/"in"/name,sha)
    prove_origin(root)
    return kit


def prove_origin(root):
    rj=root/BED/"RJ"
    checked(rj/"restore_verdict.json",VERDICT_SHA)
    checked(rj/"run_manifest.txt",MANIFEST_SHA)
    checked(root/BED/"ul_base.in",BASE_SHA)
    lines=(rj/"run_manifest.txt").read_text(encoding="utf-8").splitlines()
    need(sum(x.startswith("slurm_job=368315 ") for x in lines)==1, "wrong source job")


def check_gate(root,kit,arm,python):
    fresh(root,arm)
    # The sealed dispatcher substitutes a5_certificate.admits inside the ordinary gate.
    cmd=[str(python),"-I","-B",str(kit/"rt_dispatch_a5.py"),"gate",str(root),BED,arm]
    r=subprocess.run(cmd,stdout=subprocess.PIPE,check=False)
    lines=r.stdout.decode("utf-8").splitlines()
    need(r.returncode==0 and len(lines)==1 and lines[0].startswith("GATE bed="+BED+" job="+arm+" ALLOW "),
         "sealed A5 ordinary-arm gate refused "+arm)


def outcome(root,arm,job):
    check_arm(arm)
    jd=root/BED/arm
    need(jd.is_dir() and not jd.is_symlink(), "missing original run directory")
    m=jd/"run_manifest.txt"
    need(m.is_file() and not m.is_symlink(), "missing arm manifest")
    lines=m.read_text(encoding="utf-8").splitlines()
    expected={"bed=":"bed="+BED,"job=":"job="+arm,"np=":"np=6","gate=":"gate=ALLOW","resume=":"resume=0",
              "reader_arm_rc=":"reader_arm_rc=0","reader_select_rc=":"reader_select_rc=0",
              "stage=":"stage="+STAGES[arm]+" screen=screen.txt rc=0 check=PASS"}
    for prefix,line in expected.items():
        need([x for x in lines if x.startswith(prefix)]==[line],"missing or conflicting "+prefix)
    ends=[x for x in lines if x.startswith("end=")]
    need(len(ends)==1 and ends[0]==lines[-1] and re.fullmatch(r"end=\S+ fails=0 reader_rc=0",ends[0]),
         "incomplete arm receipt")
    s=[x for x in lines if x.startswith("slurm_job=")]
    need(len(s)==1 and re.fullmatch("slurm_job="+re.escape(job)+r" slurm_ntasks=6 slurm_nodes=\S+",s[0]),
         "wrong workload identity")
    if arm=="UTc":
        need("continues=UT" in lines and "parent_dir="+str(jd.parent/"UT") in lines,
             "UTc origin mismatch")
        need([x for x in lines if x.startswith("parent_sums_sha256=")]==
             ["parent_sums_sha256="+digest_file(jd/"parent_UT.sha256")],"UTc parent sums")
    v=jd/"arm_verdict.json"
    sel=jd.parent/"selection.json"
    rep=jd.parent/(arm+".report.tgz")
    need(all(p.is_file() and not p.is_symlink() for p in (v,sel,rep)), "missing original verdict, selection or report")
    verdict=json.loads(v.read_bytes())
    select=json.loads(sel.read_bytes())
    need(verdict.get("bed")==BED and verdict.get("job")==arm and isinstance(verdict.get("primary_status"),str)
         and isinstance(verdict.get("trajectory_status"),str) and isinstance(select.get("stage"),str),
         "arm verdict/selection structure")
    # Check actual bundle contains these exact copies before issuing a pass. No extraction.
    with tarfile.open(str(rep),"r:gz") as t:
        for p in (m,v,sel):
            name=p.relative_to(jd.parent).as_posix()
            matches=[i for i in t.getmembers() if i.name==name]
            need(len(matches)==1 and matches[0].isfile() and matches[0].size==p.stat().st_size,
                 "absent or duplicate report member: "+name)
            with t.extractfile(matches[0]) as f:
                need(hashlib.sha256(f.read()).hexdigest()==digest_file(p),"stale cached report: "+name)
    return dict(arm=arm,job_id=job,runner_rc=0, technical_ok=True,manifest_sha256=digest_file(m),
                verdict_sha256=digest_file(v), selection_sha256=digest_file(sel),report_sha256=digest_file(rep),
                primary_status=verdict["primary_status"],trajectory_status=verdict["trajectory_status"],
                selection_stage=select["stage"])


def engine_env(home,root):
    python=home/".conda/envs/myenv/bin/python3"
    mpi=python.parent/"mpirun"
    lmp=Path("/lustre"+str(home))/"LIGGGHTS-PUBLIC/src/lmp_mpi"
    for p,sha in ((python,PYTHON_SHA),(mpi,MPI_SHA),(lmp,LMP_SHA)):
        # The known runtime can be installed via a symlink.
        need(os.access(str(p),os.X_OK) and digest_file(p)==sha,"wrong executable "+p.name)
    env=dict(os.environ)
    for k in ("BASH_ENV","ENV","ALLOW_OTHER_LMP","ALLOW_CONCURRENT","UL_KIT","UL_STAMP","RESUME","A5_AUTHOR_GO",
              "HIST_VERDICT","GRAMMAR_VERDICT","RT_FIXTURE_SITE"):
        env.pop(k,None)
    env.update(WORK_ROOT=str(root),PY=str(python),MPIRUN=str(mpi),LMP=str(lmp),NP="6",
               MPIRUN_FLAGS="--oversubscribe --bind-to none",PATH=str(python.parent)+":"+env.get("PATH",""))
    return env


def main(args):
    need(len(args)==2 and args[0] in ("gate","preflight","run"),"usage: gate|preflight|run ARM")
    mode,arm=args
    check_arm(arm)
    home=Path.home()
    root=home/WORK
    py=home/".conda/envs/myenv/bin/python3"
    need(digest_file(py)==PYTHON_SHA,"unexpected field Python")
    kit=pinned_kit(root)
    check_gate(root,kit,arm,py)
    if mode=="gate":
        print("A5_BOUND_GATE=ALLOW ARM="+arm,flush=True)
        return 0
    job=allocation(os.environ)
    env=engine_env(home,root)
    cmd=["bash",str(kit/"run_unload.sh"),BED,arm]
    if mode=="preflight":
        return subprocess.run(cmd+["--preflight-only"],env=env,cwd=str(root)).returncode
    # All arms share a mutable selection.json. Keep the whole calculation + copy atomic w.r.t this workflow.
    import fcntl
    state=home/OPS/"state"
    out=state/"jobs"/arm
    need(out.is_dir() and not out.is_symlink() and out.resolve()==Path.cwd().resolve(),"wrong per-arm directory")
    with (state/"worker.lock").open("ab") as lock:
        fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        fresh(root,arm)
        check_gate(root,kit,arm,py)
        write_once(out/"node_started.json",dict(arm=arm,job_id=job,source_job="368315",utc=now()))
        rc=None
        try:
            rc=subprocess.run(cmd,cwd=str(root),env=env).returncode
            need(rc==0,"ordinary arm runner returned "+str(rc))
            prove_origin(root)
            r=outcome(root,arm,job)
        except Exception as e:
            r=dict(arm=arm,job_id=job,runner_rc=rc,technical_ok=False,reason=str(e))
        r.update(source_job="368315",end_utc=now(),automatic_retry=False)
        write_once(out/"node_finished.json",r)
        print("ARM="+arm+" TECHNICAL_OK="+str(r["technical_ok"]),flush=True)
        return 0 if r["technical_ok"] else 2


if __name__=="__main__":
    os.umask(0o077)
    try:
        code=main(sys.argv[1:])
    except Exception as exc:
        print("ARM_WORKER_HOLD="+str(exc),file=sys.stderr)
        code=2
    sys.exit(code)
