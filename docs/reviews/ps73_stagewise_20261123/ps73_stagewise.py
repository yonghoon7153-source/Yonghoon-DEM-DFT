"""Single-arm author approvals for the existing ps73 development sequence on ibb."""
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sys


LEGACY = "b3e96718e99fcc6334182079c6b077ab5bff0b9d2d2a9a091fa2cee26e8f6685"
PYTHON = "561c350efec08f1712162c4d649f4b668bacceb68388e973efec964f0073cd92"
OPS = "ps73_dev_ops_20261121"
BARRIER = ".ps73_author_steps_1123"
STAGES = ("UT", "UC", "UVa", "UVb", "UTc")
BOUNDARIES = {"UT": STAGES, "UC": ("UC","UVa","UVb","UTc"),
              "UV": ("UVa","UVb","UTc"), "UTc": ("UTc",)}


class Hold(Exception):
    pass


def need(ok, reason):
    if not ok:
        raise Hold(reason)


def marked(path, marker):
    return (path.is_file() and not path.is_symlink() and marker.is_file()
            and not marker.is_symlink() and os.path.samefile(path, marker))


class Stagewise:
    def __init__(self, state, old, site, release):
        self.state, self.old, self.site, self.release = state, old, site, release
        self.jobs = state / "jobs"
        self.manual = state / "author_stages_1123"
        self.barrier = self.jobs / BARRIER
        self.marker = self.manual / "before_UT.json"
        self.pick_owner()

    def pick_owner(self):
        for arm in BOUNDARIES:
            candidate = self.manual / ("before_"+arm+".json")
            if marked(self.barrier,candidate):
                self.marker = candidate
                return arm
        return None

    def anchor(self):
        for directory in (self.state, self.jobs, self.jobs/"UB"):
            need(directory.is_dir() and not directory.is_symlink(), "invalid existing sequence directory")
        intent = self.old.read(self.state/"intent.json")
        ub = self.old.read(self.jobs/"UB"/"reply.json")
        need(intent.get("mode")==self.old.FULL and intent.get("release_sha256")==LEGACY
             and ub.get("arm")=="UB" and ub.get("job_id")=="368469",
             "wrong UB, release, or original author intent")

    def manifest(self, arm):
        return dict(action="AUTHOR_REQUESTED_STAGEWISE", before=arm, ub_job="368469",
                    legacy_release=LEGACY, stagewise_sha256=self.release)

    def set_barrier(self, name):
        target = self.jobs/name
        try:
            os.link(self.marker, target)
            self.old.sync_dir(self.jobs)
        except FileExistsError:
            need(marked(target,self.marker), "existing job or unrelated entry won boundary: "+name)

    def takeover(self, before, check_monitor):
        self.anchor()
        need(before in BOUNDARIES, "unsupported takeover boundary")
        owner = self.pick_owner()
        need(owner is None or owner == before, "another boundary already owns the reservation")
        self.marker = self.manual / ("before_"+before+".json")
        if self.manual.exists() or self.manual.is_symlink():
            need(self.manual.is_dir() and not self.manual.is_symlink(), "invalid author journal")
        if self.marker.exists() or self.marker.is_symlink():
            data = self.old.read(self.marker)
            need(data == self.manifest(before), "another author decision already recorded")
        armed = self.manual/"active.json"
        if marked(self.barrier,self.marker) and armed.exists():
            rec = self.old.read(armed)
            need(rec.get("before")==before and rec.get("stagewise_sha256")==self.release,"unexpected active receipt")
            return dict(rec,status="ALREADY_STAGEWISE",submitted=False)
        if not marked(self.barrier,self.marker):
            actual = {p.name for p in self.jobs.iterdir()}
            expected = {"UT":{"UB"},"UC":{"UB","UT"},"UV":{"UB","UT","UC"}}.get(before)
            if before=="UTc":
                options = actual.intersection(("UVa","UVb"))
                need(len(options)==1, "need one acknowledged UV predecessor")
                expected = {"UB","UT","UC"} | options
            need(actual == expected, "boundary passed, ambiguous, or predecessor not present; no takeover")
            for arm in expected:
                self.acknowledged(arm)
            need(not (self.state/"sequence_result.json").exists(), "original sequence has ended")
            check_monitor()
        if not self.manual.exists():
            self.old.new_dir(self.manual)
        if not self.marker.exists():
            self.old.publish(self.marker,self.manifest(before))
        # Stop every new old-controller loop at its inventory check. A loop that
        # already took an inventory can still claim one arm, which the exclusive
        # arm names below arbitrate. Leave real directories and receipts intact.
        self.set_barrier(BARRIER)
        raced, uncertain = {}, []
        for arm in BOUNDARIES[before]:
            path = self.jobs/arm
            try:
                self.set_barrier(arm)
            except Hold:
                try:
                    raced[arm] = self.acknowledged(arm)["job_id"]
                except Hold:
                    uncertain.append(arm)
        need(not uncertain,"UNACKNOWLEDGED_OR_FOREIGN: "+",".join(uncertain)+"; inspect STATUS")
        need(len(raced)<=1,"more than one stage already claimed during handover; inspect STATUS")
        rec = dict(before=before, stagewise_sha256=self.release, previously_claimed=raced,
                   status="BOUNDARY_RESERVED" if not raced else "STAGEWISE_AFTER_EXISTING_CLAIM",
                   submitted=False)
        self.old.publish(armed,rec)
        return rec

    def acknowledged(self,arm):
        path = self.jobs/arm
        need(path.is_dir() and not path.is_symlink(),"unknown or unrelated arm entry: "+arm)
        need((path/"reply.json").is_file(),"existing job claim lacks acknowledgement: "+arm)
        ack=self.old.read(path/"reply.json")
        need(ack.get("arm")==arm and self.old.id_ok(ack.get("job_id")),"invalid job acknowledgement: "+arm)
        return ack

    def stage_jobs(self):
        need(self.manual.is_dir() and not self.manual.is_symlink() and marked(self.barrier,self.marker),
             "takeover not established")
        data = self.old.read(self.marker)
        boundary = data.get("before")
        need(boundary in BOUNDARIES and data==self.manifest(boundary), "takeover source mismatch")
        active=self.old.read(self.manual/"active.json")
        need(active.get("before")==boundary and active.get("stagewise_sha256")==self.release,
             "takeover incomplete; repeat only the same takeover after STATUS")
        result = {}
        for p in sorted(self.jobs.iterdir()):
            if p.name == BARRIER or (p.name in BOUNDARIES[boundary] and marked(p,self.marker)):
                continue
            need(p.name in self.old.ARMS and p.is_dir() and not p.is_symlink(),
                 "unrecognized or unacknowledged arm entry")
            need((p/"reply.json").is_file(), "existing submission lacks acknowledgement; reconcile")
            ack = self.old.read(p/"reply.json")
            need(ack.get("arm")==p.name and self.old.id_ok(ack.get("job_id")), "bad job acknowledgement")
            result[p.name] = p
        return result

    def act(self, requested):
        self.anchor()
        claimed = self.stage_jobs()
        if requested:
            need(requested in STAGES and requested not in claimed, "arm already claimed or unsupported")
        receipts = {arm:self.old.terminal_receipt(path,self.site) for arm,path in claimed.items()}
        plan = self.site.plan(receipts)
        decision = plan.get("status")
        need(decision in ("READY","STOP","REVIEW"), "unknown frozen selection decision")
        finalpath = self.state/"sequence_result.json"
        if finalpath.exists():
            saved = self.old.read(finalpath)
            need(saved.get("status")==decision and saved.get("plan")==plan
                 and decision in ("STOP","REVIEW"), "unexpected final sequence record")
        elif decision in ("STOP","REVIEW"):
            self.old.publish(finalpath, dict(status=decision, plan=plan, utc=self.old.now()))
        need(decision != "STOP", "registered sequence stop: "+str(plan.get("reason")))
        if requested is None:
            return plan
        need(decision=="READY" and plan.get("next_arm")==requested,
             "wrong arm for registered plan; inspect RECORD_ONLY")
        evidence = self.site.gate(requested)
        path = self.jobs/requested
        if marked(path,self.marker):
            # Only our same-inode guard can be dropped, with the permanent guard
            # in place and the legacy dispatch directory locked by this caller.
            path.unlink()
            self.old.sync_dir(self.jobs)
        self.old.new_dir(path)
        self.old.publish(path/"intent.json", dict(arm=requested,utc=self.old.now(),
                         mode="GO_"+requested+"_ONCE",release_sha256=LEGACY,pre_submit=evidence))
        jid = self.site.submit(requested,path)
        need(self.old.id_ok(jid), "uncertain job acknowledgement; manual reconciliation")
        self.old.publish(path/"reply.json",dict(arm=requested,job_id=jid,utc=self.old.now()))
        return dict(status="ONE_ARM_ACKNOWLEDGED",arm=requested,job_id=jid,additional_submissions=0)

    def snapshot(self):
        self.anchor()
        view = self.old.status(self.state)
        if marked(self.barrier,self.marker):
            boundary = self.old.read(self.marker)["before"]
            for target in BOUNDARIES[boundary]:
                if marked(self.jobs/target,self.marker):
                    view["jobs"].pop(target,None)
            view["stage_control"] = ("AUTHOR_GO_PER_ARM" if (self.manual/"active.json").is_file()
                                     else "TAKEOVER_INCOMPLETE_INSPECT_SAME_BOUNDARY")
            view["takeover_boundary"] = boundary
            view["original_driver_status"] = view["status"]
            final = self.state/"sequence_result.json"
            view["status"] = self.old.read(final)["status"] if final.exists() else "STAGEWISE"
        return view


@contextlib.contextmanager
def lockdir(path):
    import fcntl
    fd = os.open(str(path), os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise Hold("controller owns directory lock; no stage action; inspect STATUS later") from error
        yield
    finally:
        os.close(fd)


def fixed_monitor(ops, old):
    state = ops/"state"
    starts = sorted(state.glob("driver_*_start.json"))
    need(len(starts)==1 and starts[0].name=="driver_000001_start.json"
         and not (state/"driver_000001_end.json").exists(),"expected live original controller missing")
    rec = old.read(starts[0])
    pid = rec.get("pid")
    need(rec.get("host")==socket.gethostname() and rec.get("action")=="run"
         and rec.get("process_token") and old.proc_token(pid)==rec["process_token"],
         "legacy controller process identity changed")
    proc = Path("/proc")/str(pid)
    cmd = (proc/"cmdline").read_bytes().split(b"\0")[:-1]
    need(cmd == [os.fsencode(Path.home()/".conda/envs/myenv/bin/python3"),b"-I",b"-B",
                 os.fsencode(ops/"phase_controller.py"),b"run",old.FULL.encode()]
         and (proc/"cwd").resolve()==ops.resolve(), "legacy controller command mismatch")


def nonblocking_wait(site,old,jid):
    q = site.query(["squeue","--noheader","-j",jid,"--format=%i|%T"])
    need(not old.queue_running(jid,q.returncode,q.stdout,q.stderr), "existing job remains in queue: "+jid)
    a = site.query(["sacct","-n","-P","-j",jid,"--format=JobIDRaw,State%40,ExitCode"])
    need(a.returncode==0 and not a.stderr.strip(), "sacct query failed")
    result = old.accounting(jid,a.stdout)
    need(result is not None, "terminal accounting not yet available: "+jid)
    return result


def main(mode, code_sha):
    os.umask(0o077)
    home = Path.home()
    ops = home/OPS
    state = ops/"state"
    need(socket.gethostname().split(".")[0]=="ibb-master" and not any(
         k.startswith(("SLURM_","SBATCH_")) for k in os.environ), "wrong login node or job environment")
    need(Path(sys.executable).samefile(home/".conda/envs/myenv/bin/python3")
         and hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()==PYTHON, "field Python mismatch")
    need(ops.is_dir() and not ops.is_symlink() and state.is_dir() and not state.is_symlink(), "missing release")
    sums = (ops/"SOURCE_SHA256SUMS").read_bytes()
    need(hashlib.sha256(sums).hexdigest()==LEGACY, "wrong installed release")
    for line in sums.decode("ascii").splitlines():
        digest, name = line.split("  ",1)
        f = ops/name
        need(f.is_file() and not f.is_symlink() and hashlib.sha256(f.read_bytes()).hexdigest()==digest,
             "legacy source mismatch")
    spec = importlib.util.spec_from_file_location("phase_controller", ops/"phase_controller.py")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    site = old.Site(ops,LEGACY)
    site.wait = lambda jid: nonblocking_wait(site,old,jid)
    switch = Stagewise(state,old,site,code_sha)
    if mode=="STATUS":
        return switch.snapshot()
    with lockdir(state):
        if mode in ["GO_TAKEOVER_BEFORE_"+arm for arm in BOUNDARIES]:
            return switch.takeover(mode.rsplit("_",1)[1],lambda:fixed_monitor(ops,old))
        need(mode=="RECORD_ONLY" or mode in ["GO_"+arm+"_ONCE" for arm in STAGES], "unknown action")
        with lockdir(ops):
            return switch.act(None if mode=="RECORD_ONLY" else mode[3:-5])


if __name__ == "__main__":
    try:
        print(json.dumps(main(sys.argv[1],sys.argv[2]),sort_keys=True))
    except Exception as error:
        print("HOLD_OR_INCOMPLETE="+str(error),file=sys.stderr)
        sys.exit(2)
