"""Synthetic filesystem and scheduler callbacks for the 7:3 controller handover."""
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock
import importlib.util

SPEC = importlib.util.spec_from_file_location("ps73_stagewise", Path(__file__).with_name("ps73_stagewise.py"))
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class Journal:
    FULL = "GO_PS73_SEQUENCE_ONCE"
    ARMS = ("UB", "UT", "UC", "UVa", "UVb", "UTc")
    read = staticmethod(lambda p: json.loads(p.read_text()))
    now = staticmethod(lambda: "synthetic")
    sync_dir = staticmethod(lambda p: None)
    id_ok = staticmethod(lambda n: type(n) is str and n.isdigit())
    new_dir = staticmethod(lambda p: p.mkdir())

    @staticmethod
    def publish(p, value):
        with p.open("x") as handle:
            json.dump(value, handle)

    @staticmethod
    def terminal_receipt(p, site):
        data = dict(arm=p.name, job_id=Journal.read(p/"reply.json")["job_id"])
        if not (p/"receipt.json").exists():
            Journal.publish(p/"receipt.json", data)
        return data


class FakeSite:
    def __init__(self):
        self.submits = []
        self.route = ["UB", "UT", "UC", "UVb", "UTc"]

    def plan(self, done):
        next_arm = next((a for a in self.route if a not in done), None)
        return dict(status="READY" if next_arm else "REVIEW", next_arm=next_arm, completed=list(done))

    def gate(self, arm):
        return {"synthetic": True}

    def submit(self, arm, job):
        self.submits.append(arm)
        return str(400000 + len(self.submits))


class Stagewise(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.state = Path(tmp.name)/"state"
        self.jobs = self.state/"jobs"
        ub = self.jobs/"UB"
        ub.mkdir(parents=True)
        Journal.publish(self.state/"intent.json", {"mode":Journal.FULL, "release_sha256":mod.LEGACY})
        Journal.publish(ub/"reply.json", {"arm":"UB", "job_id":"368469"})
        self.site = FakeSite()
        self.ops = mod.Stagewise(self.state, Journal, self.site, "e"*64)
        self.live = mock.Mock()

    def adopt(self, arm="UT"):
        return self.ops.takeover(arm, self.live)

    def add(self, arm, jobid):
        path = self.jobs/arm
        path.mkdir()
        Journal.publish(path/"reply.json", {"arm":arm, "job_id":jobid})

    def test_atomic_fence_wins_and_legacy_cannot_mkdir(self):
        self.adopt()
        with self.assertRaises(FileExistsError):
            (self.jobs/"UT").mkdir()
        self.assertEqual(self.site.submits, [])
        self.assertTrue((self.jobs/mod.BARRIER).is_file())
        self.assertTrue(os.path.samefile(self.jobs/"UT",self.jobs/mod.BARRIER))

    def test_legacy_wins_and_its_directory_is_preserved(self):
        self.add("UT","32")
        with self.assertRaises(mod.Hold):
            self.adopt()
        self.assertFalse((self.jobs/mod.BARRIER).exists())
        self.assertEqual(Journal.read(self.jobs/"UT"/"reply.json")["job_id"],"32")

    def test_claimed_UT_can_explicitly_choose_next_UC(self):
        self.add("UT","32")
        self.adopt("UC")
        self.assertTrue((self.jobs/"UC").is_file())
        self.assertTrue((self.jobs/"UT").is_dir())

    def test_recover_own_permanent_fence_before_all_stage_links(self):
        self.adopt()
        (self.ops.manual/"active.json").unlink()
        for arm in ("UC","UVa","UVb","UTc"):
            (self.jobs/arm).unlink()
        self.adopt()
        self.assertTrue((self.jobs/"UTc").is_file())
        self.assertTrue((self.ops.manual/"active.json").is_file())

    def test_repeated_takeover_idempotent_no_submit(self):
        self.adopt()
        self.adopt()
        self.assertEqual(self.site.submits, [])

    def test_wrong_UB_identity_rejected_before_fence(self):
        (self.jobs/"UB"/"reply.json").write_text('{"arm":"UB","job_id":"65"}')
        with self.assertRaises(mod.Hold):
            self.adopt()
        self.assertFalse((self.jobs/mod.BARRIER).exists())

    def test_unacknowledged_previous_job_blocks_takeover(self):
        (self.jobs/"UT").mkdir()
        with self.assertRaises(mod.Hold):
            self.adopt("UC")
        self.assertFalse((self.jobs/mod.BARRIER).exists())

    def test_go_without_takeover_is_rejected(self):
        with self.assertRaises(mod.Hold):
            self.ops.act("UT")
        self.assertEqual(self.site.submits,[])

    def test_wrong_GO_and_readback_submit_nothing(self):
        self.adopt()
        self.assertEqual(self.ops.act(None)["next_arm"], "UT")
        with self.assertRaises(mod.Hold):
            self.ops.act("UC")
        self.assertEqual(self.site.submits, [])

    def test_one_approved_arm_only_and_duplicate_fails(self):
        self.adopt()
        self.assertEqual(self.ops.act("UT")["arm"], "UT")
        self.assertEqual(self.site.submits, ["UT"])
        with self.assertRaises(mod.Hold):
            self.ops.act("UT")
        self.assertEqual(self.site.submits, ["UT"])
        self.assertTrue((self.jobs/mod.BARRIER).is_file())

    def test_only_selected_UV_and_only_t3_UTc(self):
        self.adopt()
        for arm in ["UT","UC"]:
            self.ops.act(arm)
        with self.assertRaises(mod.Hold):
            self.ops.act("UVa")
        self.ops.act("UVb")
        self.ops.act("UTc")
        self.assertEqual(self.ops.act(None)["status"], "REVIEW")
        self.assertEqual(self.site.submits, ["UT","UC","UVb","UTc"])

    def test_submit_reply_lost_creates_no_second_submission(self):
        self.adopt()
        self.site.submit = mock.Mock(side_effect=OSError("connection interrupted"))
        with self.assertRaises(OSError):
            self.ops.act("UT")
        with self.assertRaises(mod.Hold):
            self.ops.act("UT")
        self.assertEqual(self.site.submit.call_count,1)

    def test_foreign_file_cannot_be_removed(self):
        self.adopt()
        (self.jobs/"UT").unlink()
        (self.jobs/"UT").write_text("foreign")
        with self.assertRaises(mod.Hold):
            self.ops.act("UT")
        self.assertEqual((self.jobs/"UT").read_text(),"foreign")

    def test_receipt_from_race_preserves_UT_and_fences_UC(self):
        def win():
            self.add("UT","100000")
        rec=self.ops.takeover("UT",win)
        self.assertEqual(rec["previously_claimed"],{"UT":"100000"})
        self.assertTrue((self.jobs/"UC").is_file())
        self.assertEqual(Journal.read(self.jobs/"UT"/"reply.json")["job_id"],"100000")

    def test_UC_in_progress_exclusive_both_UVs_and_t3(self):
        self.add("UT","400010")
        self.add("UC","400011")
        self.adopt("UV")
        for name in ("UVa","UVb","UTc"):
            self.assertTrue(os.path.samefile(self.jobs/name,self.jobs/mod.BARRIER))
        self.assertEqual(self.ops.act(None)["next_arm"],"UVb")
        self.ops.act("UVb")
        self.assertTrue((self.jobs/"UVa").is_file())
        self.assertEqual(self.site.submits,["UVb"])

    def test_UVb_race_preserves_its_receipt_and_covers_t3(self):
        self.add("UT","400010")
        self.add("UC","400011")
        rec=self.ops.takeover("UV",lambda:self.add("UVb","400012"))
        self.assertEqual(rec["previously_claimed"],{"UVb":"400012"})
        self.assertTrue((self.jobs/"UTc").is_file())
        self.assertEqual(self.site.submits,[])

    def test_inflight_UVb_keeps_future_fence_with_no_activation(self):
        self.add("UT","400010")
        self.add("UC","400011")
        with self.assertRaises(mod.Hold):
            self.ops.takeover("UV",lambda:(self.jobs/"UVb").mkdir())
        self.assertTrue((self.jobs/"UTc").is_file())
        self.assertFalse((self.ops.manual/"active.json").exists())
        Journal.publish(self.jobs/"UVb"/"reply.json",{"arm":"UVb","job_id":"400012"})
        self.assertEqual(self.adopt("UV")["previously_claimed"],{"UVb":"400012"})

    def test_after_UV_ack_before_UTc(self):
        for arm, jid in [("UT","400010"),("UC","400011"),("UVb","400012")]:
            self.add(arm,jid)
        self.adopt("UTc")
        self.assertTrue((self.jobs/"UTc").is_file())
        self.assertEqual(self.ops.act(None)["next_arm"],"UTc")

    def test_status_preserves_final_stop_and_review(self):
        self.adopt()
        for decision in ("STOP","REVIEW"):
            result = self.state/"sequence_result.json"
            result.write_text(json.dumps({"status":decision}))
            with mock.patch.object(Journal,"status",create=True,side_effect=lambda s:{
                    "status":"HOLD_OR_RECONCILE","jobs":{"UB":{},"UT":{"status":"SUBMIT_STATE_UNCERTAIN"}}}):
                view=self.ops.snapshot()
            self.assertEqual(view["status"],decision)
            self.assertEqual(view["original_driver_status"],"HOLD_OR_RECONCILE")
            self.assertNotIn("UT",view["jobs"])
            self.assertEqual(view["stage_control"],"AUTHOR_GO_PER_ARM")

    def test_known_failed_predecessor_cannot_submit_successor(self):
        self.adopt()
        with mock.patch.object(Journal,"terminal_receipt",side_effect=mod.Hold("FAILED")):
            with self.assertRaises(mod.Hold):
                self.ops.act("UT")
        self.assertEqual(self.site.submits,[])

    @unittest.skipUnless(os.name=="posix","requires flock with separate open directory descriptors")
    def test_stage_cannot_lock_live_legacy_directory(self):
        with mod.lockdir(self.state):
            with self.assertRaises(mod.Hold):
                with mod.lockdir(self.state):
                    self.fail("same directory admitted another owner")

    @unittest.skipUnless(os.name=="posix","real exclusive publish and flock on Linux")
    def test_fixed_legacy_and_staged_control_share_one_pending_UB(self):
        paths = [p/"ps73_development_sequence_20261121/controller/phase_controller.py"
                 for p in Path(__file__).parents]
        if os.environ.get("PS73_TEST_LEGACY_CONTROLLER"):
            paths.insert(0,Path(os.environ["PS73_TEST_LEGACY_CONTROLLER"]))
        fixed_path = next((p for p in paths if p.is_file()),None)
        self.assertIsNotNone(fixed_path,"provide the fixed controller path for this integration test")
        spec = importlib.util.spec_from_file_location("old_7_3",fixed_path)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        state = self.state.parent/"second"
        waiting = threading.Event()
        finish = threading.Event()
        errors = []
        site = FakeSite()
        site.release_id = mod.LEGACY
        def submit(arm, job):
            site.submits.append(arm)
            jid = "368469" if arm=="UB" else "400102"
            old.publish(job/"node_finished.json",dict(arm=arm, job_id=jid,
                        technical_ok=True,runner_rc=0,manifest_sha256="a"*64,verdict_sha256="b"*64))
            return jid
        site.submit = submit
        def wait(jid):
            waiting.set()
            self.assertTrue(finish.wait(5))
            return "COMPLETED","0:0"
        site.wait=wait
        def legacy_worker():
            try:
                with mod.lockdir(state.parent):
                    old.advance(state,site,"run",old.FULL)
            except (old.Hold,FileExistsError) as error:
                errors.append(str(error))
        worker=threading.Thread(target=legacy_worker)
        worker.start()
        try:
            self.assertTrue(waiting.wait(5))
            switch = mod.Stagewise(state,old,site,"b"*64)
            switch.takeover("UT",lambda:None)
            self.assertEqual(site.submits,["UB"])
        finally:
            finish.set()
            worker.join(5)
        self.assertFalse(worker.is_alive())
        self.assertTrue(errors)
        self.assertEqual(site.submits,["UB"])
        with self.assertRaises(old.Hold):
            old.advance(state,site,"resume")
        with mod.lockdir(state.parent):
            self.assertEqual(switch.act("UT")["arm"],"UT")
        self.assertEqual(site.submits,["UB","UT"])


if __name__ == "__main__":
    unittest.main()
