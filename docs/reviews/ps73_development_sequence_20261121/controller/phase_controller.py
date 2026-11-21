"""One-shot ps73 development submissions and receipt-based sequencing on the login node."""
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time


UB = "GO_UB_ONCE"
FULL = "GO_PS73_SEQUENCE_ONCE"
ARMS = ("UB", "UT", "UC", "UVa", "UVb", "UTc")
RUNNING = {"PENDING","RUNNING","COMPLETING","CONFIGURING","SUSPENDED","RESIZING","STAGE_OUT","SIGNALING"}
PURGED = {"slurm_load_jobs error: Invalid job id specified",
          "squeue: error: slurm_load_jobs error: Invalid job id specified",
          "squeue: error: Invalid job id specified", "Invalid job id specified"}
WORK = "ps45_a5_rj_9fd6aa9d3bee_1120_once"
OPS = "ps73_dev_ops_20261121"


class Hold(Exception):
    pass


def need(ok, why):
    if not ok:
        raise Hold(why)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sync_dir(path):
    if os.name == "posix":
        fd = os.open(str(path), os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def publish(path, obj):
    """Publish complete, durable bytes exclusively. Never overwrite receipts."""
    raw = (json.dumps(obj, sort_keys=True, ensure_ascii=True)+"\n").encode()
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix="."+path.name+".")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.link(tmp, str(path))
        sync_dir(path.parent)
    finally:
        os.unlink(tmp)


def read(path):
    need(path.is_file() and not path.is_symlink() and path.stat().st_size < 1048576,
         "missing or invalid receipt: "+path.name)
    data = json.loads(path.read_bytes())
    need(type(data) is dict, "invalid receipt object: "+path.name)
    return data


def new_dir(path):
    path.mkdir(mode=0o700)
    sync_dir(path.parent)


def id_ok(x):
    return type(x) is str and re.fullmatch("[1-9][0-9]*", x) is not None


def queue_running(jid, rc, stdout, stderr):
    out, err = stdout.strip(), stderr.strip()
    if rc == 1 and not out and err in PURGED:
        return False
    need(rc == 0 and not err, "squeue failed; keep existing job id")
    if not out:
        return False
    parts = out.split("|")
    need(len(parts) == 2 and parts[0] == jid and re.fullmatch(r"[A-Z_]+", parts[1]),
         "unrecognized squeue reply; keep existing job id")
    return parts[1] in RUNNING


def accounting(jid, stdout):
    rows = [s.split("|") for s in stdout.splitlines() if s.split("|",1)[0] == jid]
    if not rows:
        return None
    need(len(rows)==1 and len(rows[0])==3, "ambiguous sacct record")
    state, code = rows[0][1:]
    need(state.strip() and re.fullmatch(r"[0-9]+:[0-9]+",code), "invalid sacct record")
    if state in RUNNING:
        return None
    return state, code


def clean_env():
    keep = ("HOME","PATH","USER","LOGNAME","LD_LIBRARY_PATH","SHELL","TMPDIR")
    env = {k:os.environ[k] for k in keep if k in os.environ}
    env.update(LANG="C", LC_ALL="C")
    return env


class Site:
    def __init__(self, ops, release):
        self.ops = ops
        self.release_id = release
        self.work = Path.home()/WORK
        self.py = Path.home()/".conda/envs/myenv/bin/python3"
        spec = importlib.util.spec_from_file_location("ps73_sequence",ops/"ps73_sequence.py")
        self.sequence = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.sequence)

    def plan(self, receipts):
        return self.sequence.recommend(self.work, self.work/"fixed_kit", receipts)

    def gate(self, arm):
        prior = read(self.work/"author_intent.json")
        floor = prior.get("planned_total_bytes")
        need(type(floor) is int and floor>0 and prior.get("previous_job")=="323957",
             "previous A5 storage plan unavailable")
        available = shutil.disk_usage(str(self.work)).free
        need(available>=floor, "available shared storage below original A5 planned budget")
        cmd = [str(self.py),"-I","-B",str(self.ops/"ps73_node.py"),"gate",arm]
        result = subprocess.run(cmd, env=clean_env(), cwd=self.ops, capture_output=True)
        if result.returncode:
            reason = "pre-submit node identity check failed: "+arm
            for line in result.stderr.decode("ascii",errors="replace").splitlines():
                if line.startswith("ARM_WORKER_HOLD="):
                    reason += " (" + line[len("ARM_WORKER_HOLD="):][:240] + ")"
                    break
            raise Hold(reason)
        return {"prior_planned_total_bytes":floor,"available_filesystem_bytes":available,
                "quota_basis":"prior author receipt; no new quota measurement"}

    def submit(self, arm, job):
        cmd = ["sbatch","--parsable","--no-requeue","--nodes=1","--ntasks=6","--cpus-per-task=1",
               "--partition=cpu","--qos=cpu-60","--time=5-00:00:00","--export=ALL",
               "--job-name=ps73_"+arm,"--chdir="+str(job),"--output="+str(job/"slurm-%j.out"),
               "--error="+str(job/"slurm-%j.err"),str(self.ops/"phase_arm.sbatch"),arm,self.release_id]
        with (job/"sbatch.stdout").open("xb") as out, (job/"sbatch.stderr").open("xb") as err:
            rc = subprocess.run(cmd, env=clean_env(), cwd=self.ops, stdout=out, stderr=err).returncode
            for f in (out,err):
                f.flush()
                os.fsync(f.fileno())
        m = re.fullmatch(rb"([1-9][0-9]*)(?:;[A-Za-z0-9._-]+)?\r?\n?", (job/"sbatch.stdout").read_bytes())
        need(rc==0 and m is not None, "sbatch acknowledgement missing or uncertain; manual reconciliation")
        return m.group(1).decode()

    def query(self, cmd):
        return subprocess.run(cmd,env=clean_env(),capture_output=True,universal_newlines=True,timeout=60)

    def wait(self, jid):
        missing = 0
        while True:
            q = self.query(["squeue","--noheader","-j",jid,"--format=%i|%T"])
            if queue_running(jid, q.returncode, q.stdout, q.stderr):
                missing = 0
            else:
                a = self.query(["sacct","-n","-P","-j",jid,"--format=JobIDRaw,State%40,ExitCode"])
                need(a.returncode==0 and not a.stderr.strip(),"sacct query error; preserve and reconcile")
                terminal = accounting(jid, a.stdout)
                if terminal:
                    return terminal
                missing += 1
                need(missing<=10, "terminal accounting delayed; resume to reconcile the same job")
            time.sleep(60)


def proc_token(pid):
    if type(pid) is not int or pid<=0:
        return None
    try:
        stat = (Path("/proc")/str(pid)/"stat").read_text()
        cols = stat[stat.rfind(") ")+2:].split()
        if cols[0] in ("Z","X"):
            return None
        return (Path("/proc/sys/kernel/random/boot_id").read_text().strip()+":"+cols[19])
    except (OSError, IndexError):
        return None


def status(state):
    if not state.exists():
        return {"status":"NO_INTENT"}
    need(state.is_dir() and not state.is_symlink(),"bad state directory")
    intent = state/"intent.json"
    out = {"status":"NO_INTENT" if not intent.exists() else "INTENT_RECORDED","jobs":{}}
    if intent.exists():
        out["mode"] = FULL if (state/"go_full.json").exists() else read(intent)["mode"]
    for arm in ARMS:
        job = state/"jobs"/arm
        if job.exists():
            item = {"status":"SUBMIT_STATE_UNCERTAIN"}
            for filename, label in [("reply.json","ACKNOWLEDGED"),("accounting.json","TERMINAL_ACCOUNTING"),("receipt.json","TECHNICAL_RECEIPT")]:
                path = job/filename
                if path.exists():
                    data = read(path)
                    item.update({k:data[k] for k in ("job_id","state","exit_code","runner_rc","technical_ok") if k in data})
                    item["status"] = label
            out["jobs"][arm] = item
    if (state/"sequence_result.json").exists():
        terminal = read(state/"sequence_result.json")
        out["status"] = terminal["status"]
        out["reason"] = terminal["plan"].get("reason")
    elif (state/"ub_return.json").exists() and out.get("mode")==UB:
        out["status"]="UB_RETURN_READY"
    starts = sorted(state.glob("driver_*_start.json"))
    if starts:
        record = read(starts[-1])
        end = state/(starts[-1].name[:-len("start.json")]+"end.json")
        if end.is_file():
            result = read(end)
            out["controller"] = result
            if result["driver_rc"] != 0:
                out["status"] = "HOLD_OR_RECONCILE"
        elif record.get("process_token") and record.get("host")==socket.gethostname() and proc_token(record.get("pid"))==record["process_token"]:
            out["controller"] = {"state":"MONITOR_PROCESS_LIVE","since_utc":record["utc"]}
        else:
            out["controller"] = {"state":"MONITOR_EXIT_WITHOUT_RECEIPT","since_utc":record["utc"]}
            out["status"] = "RECONCILE_EXISTING_JOB"
    return out


def terminal_receipt(job, site):
    arm = job.name
    need(job.is_dir() and not job.is_symlink(),"bad arm job directory")
    intent = read(job/"intent.json")
    need(intent.get("arm")==arm,"job intent mismatch")
    if not (job/"reply.json").is_file():
        raise Hold("unacknowledged "+arm+" submission; preserve and reconcile, no resubmit")
    ack = read(job/"reply.json")
    jid = ack.get("job_id")
    need(id_ok(jid) and ack.get("arm")==arm,"invalid sbatch receipt")
    acc = job/"accounting.json"
    if not acc.exists():
        st, code = site.wait(jid)
        publish(acc,dict(arm=arm,job_id=jid,state=st,exit_code=code,observed_utc=now()))
    info = read(acc)
    need(info.get("job_id")==jid and info.get("arm")==arm and info.get("state")=="COMPLETED"
         and info.get("exit_code")=="0:0","scheduler rejected "+arm+"; no successor")
    data = read(job/"node_finished.json")
    need(data.get("arm")==arm and data.get("job_id")==jid and data.get("technical_ok") is True
         and type(data.get("runner_rc")) is int and data["runner_rc"]==0,"worker receipt rejected: "+arm)
    for k in ("manifest_sha256","verdict_sha256"):
        need(type(data.get(k)) is str and re.fullmatch("[a-f0-9]{64}",data[k]),"incomplete node receipt")
    record = dict(data, state=info["state"],exit_code=info["exit_code"])
    path = job/"receipt.json"
    if not path.exists():
        publish(path, record)
    need(read(path) == record, "saved receipt changed: "+arm)
    return record


def advance(state, site, action, token=None):
    need(action in ("run","resume"),"unknown action")
    if action == "run":
        need(token in (UB,FULL),"explicit author GO required")
        if not state.exists():
            new_dir(state)
    need(state.is_dir() and not state.is_symlink(),"no valid state directory")
    if not (state/"intent.json").exists():
        need(action=="run","resume requires an existing author GO")
        publish(state/"intent.json",dict(mode=token,utc=now(),planned_first_arm="UB",
                                        release_sha256=site.release_id,autorun_retries=0))
    elif action=="run":
        old = read(state/"intent.json")
        need(token==FULL and old.get("mode")==UB and (state/"ub_return.json").is_file()
             and not (state/"go_full.json").exists(),"duplicate GO or UB still incomplete")
        publish(state/"go_full.json",dict(mode=FULL,utc=now(),release_sha256=site.release_id))
    orig = read(state/"intent.json")
    need(orig.get("release_sha256")==site.release_id and orig.get("mode") in (UB,FULL),"source or intent mismatch")
    mode = orig["mode"]
    if (state/"go_full.json").exists():
        add = read(state/"go_full.json")
        need(mode==UB and add.get("mode")==FULL and add.get("release_sha256")==site.release_id,"bad upgrade")
        mode = FULL
    jobs = state/"jobs"
    if not jobs.exists():
        new_dir(jobs)
    need(jobs.is_dir() and not jobs.is_symlink(),"bad job root")
    if action=="resume":
        need(any(p.name in ARMS and (p/"reply.json").is_file() for p in jobs.iterdir()),
             "no acknowledged submission to resume; inspect existing intent")
    while True:
        entries = list(jobs.iterdir())
        need(all(p.name in ARMS and p.is_dir() and not p.is_symlink() for p in entries),"unknown stored job")
        need(sum(not (p/"receipt.json").exists() for p in entries)<=1,"multiple unresolved submissions")
        receipts = {p.name:terminal_receipt(p,site) for p in entries}
        plan = site.plan(receipts)
        decision = plan.get("status")
        need(decision in ("READY","REVIEW","STOP"),"invalid phase decision")
        if (state/"sequence_result.json").is_file():
            saved = read(state/"sequence_result.json")
            need(saved.get("status")==decision and saved.get("plan")==plan,"saved sequence outcome mismatch")
            need(decision=="REVIEW","registered sequence stop: "+str(plan.get("reason")))
            return saved
        if decision in ("STOP","REVIEW"):
            record=dict(status=decision,plan=plan,utc=now())
            publish(state/"sequence_result.json",record)
            need(decision=="REVIEW","registered sequence stop: "+str(plan.get("reason")))
            return record
        arm = plan.get("next_arm")
        need(arm in ARMS and arm not in receipts and (bool(receipts) or arm=="UB"),"invalid next arm")
        if mode == UB and "UB" in receipts:
            handoff=dict(status="UB_RETURN_READY",next_if_authorized=arm,job_id=receipts["UB"]["job_id"])
            if not (state/"ub_return.json").exists():
                publish(state/"ub_return.json",handoff)
            need(read(state/"ub_return.json")==handoff,"saved UB result mismatch")
            return handoff
        evidence = site.gate(arm)
        job = jobs/arm
        new_dir(job)
        publish(job/"intent.json",dict(arm=arm,utc=now(),mode=mode,release_sha256=site.release_id,
                                      pre_submit=evidence))
        jid = site.submit(arm,job)
        need(id_ok(jid),"unknown submission response")
        publish(job/"reply.json",dict(arm=arm,job_id=jid,utc=now()))
        print("SUBMITTED ARM="+arm+" JOB_ID="+jid,flush=True)


def check_sources(ops):
    manifest = ops/"SOURCE_SHA256SUMS"
    need(manifest.is_file() and not manifest.is_symlink(),"source manifest")
    raw = manifest.read_bytes()
    names = set()
    for line in raw.decode("ascii").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z][A-Za-z0-9_.-]*)",line)
        need(m and m[2] not in names,"bad source manifest entry")
        p = ops/m[2]
        need(p.is_file() and not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==m[1],
             "source mismatch: "+p.name)
        names.add(m[2])
    need({"phase_controller.py","ps73_node.py","run_arm.sh","ps73_sequence.py","phase_arm.sbatch"}<=names,
         "incomplete release")
    return hashlib.sha256(raw).hexdigest()


def main(argv):
    os.umask(0o077)
    ops = Path(__file__).resolve().parent
    need(ops == Path.home().resolve()/OPS and not (Path.home()/OPS).is_symlink(),"wrong operator directory")
    state = ops/"state"
    if argv == ["status"]:
        return status(state)
    need((len(argv)==2 and argv[0]=="run" and argv[1] in (UB,FULL)) or argv==["resume"],"invalid operation or GO")
    need(socket.gethostname().split(".")[0]=="ibb-master" and not any(k.startswith(("SBATCH_","SLURM_"))
         for k in os.environ),"requires ibb login outside scheduler")
    # A lock on the already-existing private release directory claims no job.
    import fcntl
    lock = os.open(str(ops),os.O_RDONLY|os.O_DIRECTORY)
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if not state.exists():
            need(argv[0]=="run","no intent to resume")
            new_dir(state)
        need(state.is_dir() and not state.is_symlink(),"invalid driver state")
        attempt=len(list(state.glob("driver_*_start.json")))+1
        prefix = "driver_%06d_" % attempt
        publish(state/(prefix+"start.json"), dict(utc=now(),pid=os.getpid(),host=socket.gethostname(),
                process_token=proc_token(os.getpid()),action=argv[0]))
        try:
            release = check_sources(ops)
            site = Site(ops,release)
            result = advance(state,site,argv[0], argv[1] if len(argv)==2 else None)
        except Exception as error:
            publish(state/(prefix+"end.json"),dict(utc=now(),driver_rc=2,state="HOLD_OR_RECONCILE",
                                                  reason=str(error)[:512]))
            raise
        publish(state/(prefix+"end.json"),dict(utc=now(),driver_rc=0,state=result["status"]))
        return result
    finally:
        os.close(lock)


if __name__=="__main__":
    try:
        print(json.dumps(main(sys.argv[1:]),ensure_ascii=True,sort_keys=True),flush=True)
    except (Hold,OSError,ValueError,KeyError,subprocess.SubprocessError) as e:
        print(json.dumps(dict(status="HOLD_OR_RECONCILE",reason=str(e),automatic_retry=False)),flush=True)
        sys.exit(2)
