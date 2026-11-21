"""Synthetic guard and readback tests. No site access or simulation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("worker", Path(__file__).with_name("ps73_node.py"))
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.ctx = tempfile.TemporaryDirectory()
        self.addCleanup(self.ctx.cleanup)
        self.p = Path(self.ctx.name)
        self.env = dict(SLURM_JOB_ID="123", SLURM_NTASKS="6", SLURM_JOB_NUM_NODES="1",
                        SLURM_CPUS_PER_TASK="1", SLURM_JOB_PARTITION="cpu",
                        SLURM_RESTART_COUNT="0")
        self.arm = "UB"
        self.jd = self.p / "ps_7_3_r45" / self.arm
        self.jd.mkdir(parents=True)
        self.man = ("bed=ps_7_3_r45\njob=UB\nnp=6\nresume=0\ngate=ALLOW\n"
                    "slurm_job=123 slurm_ntasks=6 slurm_nodes=node01\n"
                    "stage=U_UB screen=screen.txt rc=0 check=PASS\n"
                    "reader_arm_rc=0\nreader_select_rc=0\nend=x fails=0 reader_rc=0\n")
        self.mfile = self.jd / "run_manifest.txt"
        self.mfile.write_text(self.man)
        self.verdict = dict(job="UB", bed="ps_7_3_r45", primary_status="NO_BRACKET",
                            trajectory_status="LIFT_CAP")
        (self.jd / "arm_verdict.json").write_text(json.dumps(self.verdict))
        (self.jd.parent / "selection.json").write_text(json.dumps(dict(stage="need_arms")))
        import io, tarfile
        with tarfile.open(str(self.jd.parent / "UB.report.tgz"), "w:gz") as z:
            for path in (self.mfile,self.jd/"arm_verdict.json",self.jd.parent/"selection.json"):
                z.add(str(path),arcname=path.relative_to(self.jd.parent).as_posix())

    def test_allowed_arms(self):
        for arm in ("UB","UT","UC","UVa","UVb","UTc"):
            worker.check_arm(arm)
        for arm in ("UT3","RJ","RJ2","EXT","G_UT","G_UB","G_UVa","G_UVb","G_UT3","../UB","UB "):
            with self.subTest(arm=arm), self.assertRaises(ValueError):
                worker.check_arm(arm)

    def test_allocation(self):
        self.assertEqual(worker.allocation(self.env),"123")
        for k,v in {"SLURM_JOB_ID":"123_1","SLURM_NTASKS":"1","SLURM_JOB_NUM_NODES":"2",
                    "SLURM_CPUS_PER_TASK":"2","SLURM_JOB_PARTITION":"gpu",
                    "SLURM_ARRAY_TASK_ID":"0","SLURM_RESTART_COUNT":"1"}.items():
            with self.subTest(k=k),self.assertRaises(ValueError):
                worker.allocation(dict(self.env,**{k:v}))

    def test_technical_vs_physical(self):
        r=worker.outcome(self.p,self.arm,"123")
        self.assertTrue(r["technical_ok"])
        self.assertEqual(r["primary_status"],"NO_BRACKET")
        self.assertEqual(r["trajectory_status"],"LIFT_CAP")
        self.assertEqual(r["runner_rc"],0)
        self.assertEqual(r["manifest_sha256"], hashlib.sha256(self.mfile.read_bytes()).hexdigest())

    def test_wrong_receipts_and_partial_fail(self):
        for line in ("reader_select_rc=0","reader_arm_rc=0","stage=U_UB screen=screen.txt rc=0 check=PASS","end=x fails=0 reader_rc=0"):
            for change in ("",line+"\n"+line):
                with self.subTest(line=line, change=change),self.assertRaises(ValueError):
                    self.mfile.write_text(self.man.replace(line,change))
                    worker.outcome(self.p,self.arm,"123")
        self.mfile.write_text(self.man)
        with self.assertRaises(ValueError):
            worker.outcome(self.p,self.arm,"124")

    def test_archived_report_agrees(self):
        v=dict(self.verdict, trajectory_status="TECH")
        (self.jd/"arm_verdict.json").write_text(json.dumps(v))
        with self.assertRaises(ValueError):
            worker.outcome(self.p,self.arm,"123")

    def test_missing_archive_and_stale_outputs(self):
        self.assertRaises(ValueError, worker.fresh, self.p, "UB")
        worker.fresh(self.p,"UT")
        (self.jd.parent/"UT.report.tgz").write_bytes(b"earlier")
        self.assertRaises(ValueError, worker.fresh, self.p,"UT")
        (self.jd.parent/"UB.report.tgz").unlink()
        with self.assertRaises((OSError,ValueError)):
            worker.outcome(self.p,self.arm,"123")

    def test_no_overwrite(self):
        p=self.p/"receipt.json"
        worker.write_once(p,{"one":True})
        with self.assertRaises(FileExistsError):
            worker.write_once(p,{"two":True})
        self.assertEqual(json.loads(p.read_text()),{"one":True})


if __name__=="__main__":
    unittest.main()
