"""Offline tests using the released scheduler functions and a simulated sbatch."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import early

CODE = Path(sys.argv.pop(1)).resolve()
sys.path.insert(0, str(CODE))
import site_ops as site


class EarlyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.ops = Path(temp.name)
        self.early = self.ops / "early"
        self.early.mkdir()
        (self.ops / "results").mkdir()
        self.call = []
        self.queue = "373356|RUNNING|20\n373357|PENDING|20\n368469|RUNNING|6\n373358|RUNNING|6"
        self.ub = "RUNNING"
        self.fail = False
        self.finish_ub_on_send = False
        for obj,key,value in [(site,"OPS",self.ops),(site.e,"OPS",self.ops),
                              (site,"queue",lambda:self.queue),(site,"acct",self.account),
                              (site,"command",self.command),(early,"validate_sources",lambda *_:None),
                              (site,"detach",lambda:None)]:
            override = patch.object(obj,key,value)
            override.start()
            self.addCleanup(override.stop)
        for arm,jid in [("UC","373359"),("UT","373358")]:
            d=self.ops/"attempts"/arm/"000001"
            d.mkdir(parents=True)
            site.p.publish(d/"ack.json",{"arm":arm,"job":jid,"resume":None})
        self.sentinel=self.ops/"original_UB"
        self.sentinel.mkdir()
        (self.sentinel/"selection.json").write_text("preserve")
        self.addCleanup(lambda:self.assertEqual(list(self.sentinel.iterdir()),[self.sentinel/"selection.json"]))
        self.addCleanup(lambda:self.assertEqual((self.sentinel/"selection.json").read_text(),"preserve"))

    def account(self,jid):
        states={"368469":self.ub,"373358":"RUNNING","373359":"COMPLETED","701":"PENDING"}
        return dict(job=jid,state=states[jid],exit_code="0:0")

    def command(self,argv):
        self.assertEqual(argv[0],"sbatch")
        self.assertIn("--ntasks=6",argv)
        self.assertIn("--time=5-00:00:00",argv)
        self.assertIn("--no-requeue",argv)
        self.assertTrue((self.ops/"results/UVa.hold.json").exists())
        self.assertFalse(site.attempts("UVa"))
        self.call.append(argv)
        if self.finish_ub_on_send:
            site.p.publish(site.result("UB"),{"scheduler":{"state":"COMPLETED"},"receipt":{"technical_ok":True,"runner_rc":0}})
            site.process("UVa")
        if self.fail:raise RuntimeError("lost sbatch response")
        return "701\n"

    def go(self):
        return early.launch(site,self.early)

    def test_same_journal_double_go_and_original_monitor(self):
        self.finish_ub_on_send=True
        self.go()
        self.assertEqual(len(site.attempts("UVa")),1)
        ack=site.p.read(site.attempts("UVa")[0]/"ack.json")
        self.assertEqual((ack["job"],ack["resume"],ack["projected_user_cpus"]),("701",None,58))
        site.process("UVa")
        self.go()
        self.assertEqual(len(self.call),1)
        self.assertFalse((self.ops/"results/UVa.hold.json").exists())

    def test_queue_exceeds_before_claim(self):
        self.queue+="\n373555|PENDING|3"
        with self.assertRaisesRegex(ValueError,"CAPACITY_STOP"):self.go()
        self.assertFalse(self.call)
        self.assertFalse((self.ops/"results/UVa.hold.json").exists())

    def test_original_ub_ending_yields_to_original_monitor(self):
        self.ub="COMPLETED"
        self.go()
        self.assertFalse(self.call)
        self.assertFalse((self.ops/"results/UVa.hold.json").exists())

    def test_existing_attempt_is_preserved(self):
        d=self.ops/"attempts/UVa/000001"
        d.mkdir(parents=True)
        site.p.publish(d/"ack.json",{"job":"701","arm":"UVa","resume":None})
        self.go()
        self.assertFalse(self.call)
        self.assertEqual(site.p.read(d/"ack.json")["job"],"701")

    def test_foreign_hold_is_preserved(self):
        h=self.ops/"results/UVa.hold.json"
        site.p.publish(h,{"reason":"other"})
        with self.assertRaises(ValueError):self.go()
        self.assertTrue(h.exists())
        self.assertFalse(self.call)

    def test_lost_submit_response_is_not_retried(self):
        self.fail=True
        with self.assertRaises(RuntimeError):self.go()
        self.assertTrue((self.ops/"results/UVa.hold.json").exists())
        with self.assertRaisesRegex(ValueError,"AMBIGUOUS"):self.go()
        self.assertEqual(len(self.call),1)

    def test_recover_known_ack_without_new_submit(self):
        rename = Path.rename
        def fail_once(path, target):
            if path == self.early/"segment":raise OSError("interrupted publication")
            return rename(path,target)
        with patch.object(Path,"rename",fail_once):
            with self.assertRaises(OSError):self.go()
        self.assertEqual(len(self.call),1)
        self.go()
        self.assertEqual(len(self.call),1)
        self.assertEqual(site.p.read(site.attempts("UVa")[0]/"ack.json")["job"],"701")

    def test_worker_invokes_original_batch_in_canonical_segment(self):
        first=self.ops/"attempts"/"UVa"/"000001"
        first.mkdir(parents=True)
        (first/"ack.json").write_text('{"job":"701"}')
        (self.early/"batch.sh").write_text('[[ "$2" == UVa && "$3" == "$PWD" && "$4" =~ ^[a-f0-9]{64}$ ]]\n')
        wrapper=Path(__file__).with_name("worker.sh")
        subprocess.run(["bash",str(wrapper),str(self.early),str(first),early.MANIFEST],cwd=self.ops,check=True)

if __name__=="__main__":unittest.main()
