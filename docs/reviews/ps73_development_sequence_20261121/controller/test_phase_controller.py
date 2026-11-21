"""Synthetic scheduler and worker receipts. No site access."""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import tempfile
import subprocess
import unittest


def module():
    target = Path(__file__).with_name("phase_controller.py")
    spec = importlib.util.spec_from_file_location("phase_controller", target)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FakeSite:
    release_id = "d"*64
    def __init__(self, ctl):
        self.ctl = ctl
        self.submitted = []
        self.bad = False
        self.ambiguous = False
        self.node_ok = True
        self.arm_order = ["UB", "UT", "UC", "UVb"]

    def gate(self, arm):
        pass

    def submit(self, arm, job):
        self.submitted.append(arm)
        n = str(100 + len(self.submitted))
        if self.ambiguous:
            raise self.ctl.Hold("missing ack")
        data = dict(arm=arm, job_id=n, technical_ok=self.node_ok, runner_rc=0,
                    manifest_sha256="a"*64, verdict_sha256="b"*64)
        self.ctl.publish(job/"node_finished.json", data)
        return n

    def wait(self, job_id):
        return ("FAILED", "2:0") if self.bad else ("COMPLETED", "0:0")

    def plan(self, receipts):
        for arm in self.arm_order:
            if arm not in receipts:
                return dict(status="READY", next_arm=arm, reason="synthetic", completed=list(receipts))
        return dict(status="REVIEW", next_arm=None, reason="finished", completed=list(receipts))


class Lifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = module()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root/"state"
        self.fake = FakeSite(self.m)

    def go(self, op, token=None):
        return self.m.advance(self.state, self.fake, op, token)

    def test_ub_only_then_explicit_upgrade(self):
        self.assertEqual(self.go("run", self.m.UB)["status"], "UB_RETURN_READY")
        self.assertEqual(self.fake.submitted, ["UB"])
        self.assertEqual(self.go("resume")["status"], "UB_RETURN_READY")
        with self.assertRaises(self.m.Hold):
            self.go("run", self.m.UB)
        self.assertEqual(self.go("run", self.m.FULL)["status"], "REVIEW")
        self.assertEqual(self.fake.submitted, ["UB","UT","UC","UVb"])

    def test_full_first_and_resume_no_duplicate(self):
        self.go("run", self.m.FULL)
        self.assertEqual(self.go("resume")["status"], "REVIEW")
        self.assertEqual(self.fake.submitted, self.fake.arm_order)

    def test_uncertain_submission_no_second_submission(self):
        self.fake.ambiguous = True
        with self.assertRaises(self.m.Hold):
            self.go("run", self.m.FULL)
        with self.assertRaises(self.m.Hold):
            self.go("resume")
        self.assertEqual(self.fake.submitted, ["UB"])

    def test_failed_scheduler_and_failed_worker_block(self):
        self.fake.bad = True
        with self.assertRaises(self.m.Hold):
            self.go("run", self.m.FULL)
        self.assertEqual(self.fake.submitted, ["UB"])
        self.assertTrue((self.state/"jobs"/"UB"/"accounting.json").is_file())
        self.fake.bad = False
        with self.assertRaises(self.m.Hold):
            self.go("resume")
        self.assertEqual(self.fake.submitted, ["UB"])

    def test_worker_failure_blocks(self):
        self.fake.node_ok = False
        with self.assertRaises(self.m.Hold):
            self.go("run", self.m.FULL)
        self.assertEqual(self.fake.submitted, ["UB"])

    def test_reconciliation_after_monitor_interruption(self):
        orig = self.fake.wait
        self.fake.wait = lambda jid: (_ for _ in ()).throw(KeyboardInterrupt())
        with self.assertRaises(KeyboardInterrupt):
            self.go("run", self.m.UB)
        self.fake.wait = orig
        self.assertEqual(self.go("resume")["status"], "UB_RETURN_READY")
        self.assertEqual(self.fake.submitted, ["UB"])

    def test_old_slurm_purged_is_only_narrow_absent_diagnostic(self):
        read = self.m.queue_running
        diag = "slurm_load_jobs error: Invalid job id specified"
        self.assertFalse(read("42", 1, "", diag))
        self.assertFalse(read("42", 0, "", ""))
        self.assertTrue(read("42", 0, "42|RUNNING\n", ""))
        for args in [(1,"","network down"), (1,"other\n",diag),(2,"",diag),(0,"99|RUNNING\n","")]:
            with self.assertRaises(self.m.Hold):
                read("42", *args)

    def test_only_exact_accounting_job(self):
        self.assertEqual(self.m.accounting("42","42.batch|COMPLETED|0:0\n42|COMPLETED|0:0\n"), ("COMPLETED","0:0"))
        self.assertIsNone(self.m.accounting("42","42.batch|COMPLETED|0:0\n"))
        with self.assertRaises(self.m.Hold):
            self.m.accounting("42","42|COMPLETED|0:0\n42|RUNNING|0:0\n")

    def test_status_never_creates_state(self):
        self.assertEqual(self.m.status(self.state)["status"], "NO_INTENT")
        self.assertFalse(self.state.exists())

    def test_no_resume_without_go(self):
        with self.assertRaises(self.m.Hold):
            self.go("resume")
        self.assertEqual(self.fake.submitted, [])

    def test_stopped_and_interrupted_controller_status(self):
        self.go("run", self.m.UB)
        self.m.publish(self.state/"driver_000001_start.json",dict(utc="t",pid=-1,process_token=None))
        self.assertEqual(self.m.status(self.state)["status"],"RECONCILE_EXISTING_JOB")
        self.m.publish(self.state/"driver_000001_end.json",dict(driver_rc=2,reason="fixture hold"))
        snapshot = self.m.status(self.state)
        self.assertEqual(snapshot["status"],"HOLD_OR_RECONCILE")
        self.assertEqual(snapshot["controller"]["reason"],"fixture hold")

    @unittest.skipUnless(os.name=="posix","Linux worker semantics")
    def test_home_alias_spooled_pin_and_linked_job(self):
        real = self.root/"physical"
        real.mkdir()
        home = self.root/"login_home"
        home.symlink_to(real, target_is_directory=True)
        ops = real/self.m.OPS
        job = ops/"state"/"jobs"/"UB"
        job.mkdir(parents=True)
        run = ops/"run_arm.sh"
        run.write_text('printf "SYNTHETIC_ARM=%s\\n" "$1"\n')
        sums = ops/"SOURCE_SHA256SUMS"
        sums.write_text(hashlib.sha256(run.read_bytes()).hexdigest()+"  run_arm.sh\n")
        pin = hashlib.sha256(sums.read_bytes()).hexdigest()
        worker = str(Path(__file__).with_name("phase_arm.sbatch").resolve())
        env = dict(PATH="/usr/bin:/bin",HOME=str(home),SLURM_JOB_ID="42",
                   SLURM_NTASKS="6",SLURM_JOB_NUM_NODES="1",SLURM_CPUS_PER_TASK="1")
        def call(arm):
            return subprocess.run(["bash",worker,arm,pin],cwd=job,env=env,capture_output=True)
        ok = call("UB")
        self.assertEqual((ok.returncode,ok.stdout),(0,b"SYNTHETIC_ARM=UB\n"))
        (job.parent/"UT").symlink_to(job,target_is_directory=True)
        self.assertNotEqual(call("UT").returncode,0)
        sums.write_text(sums.read_text()+"\n")
        self.assertNotEqual(call("UB").returncode,0)


if __name__ == "__main__":
    unittest.main()
