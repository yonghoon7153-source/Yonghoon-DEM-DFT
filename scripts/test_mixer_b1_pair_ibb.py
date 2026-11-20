"""Offline B1 pair admission and archive contracts. No scheduler or DEM invocation."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

def load_driver():
    path = Path(__file__).with_name("mixer_b1_pair_ibb.py")
    if not path.is_file():
        raise AssertionError("B1 driver absent")
    spec = importlib.util.spec_from_file_location("b1_driver_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class PairTests(unittest.TestCase):
    def setUp(self):
        self.b = load_driver()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "packet"
        self.root.mkdir()

    def test_no_implicit_go_or_cross_arm_token(self):
        for role in ("U", "C"):
            self.b.author_token(role, "GO_B1_" + role + "_ONCE")
            for wrong in ("", "GO_N0_ONCE", "GO_B1_ONCE", "GO_B1_" + ("C" if role=="U" else "U") + "_ONCE"):
                with self.subTest(role=role,wrong=wrong), self.assertRaises(ValueError):
                    self.b.author_token(role, wrong)

    def test_second_arm_needs_original_completed_peer(self):
        valid = dict(case="PRECAL_R1_B1_U", role="U", job_id="55", job_end_id="55",
                     runner_rc=0, return_ready=True, exact_frame_names=True, frame_count=234,
                     w9="LIVE_TERMINAL_MATCH", post_runtime_matches=True, release_pin="a"*40,
                     scheduler={"job_id":"55","state":"COMPLETED","exit_code":"0:0"})
        self.b.check_peer(valid, "a"*40)
        for key, value in [("runner_rc", False),("role","C"),("job_end_id","56"),("return_ready",False),
                           ("w9","LATE"),("frame_count",233),("case","PRECAL_N0"),("release_pin","b"*40),
                           ("scheduler",{"job_id":"55","state":"TIMEOUT","exit_code":"0:0"})]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.b.check_peer(dict(valid, **{key:value}),"a"*40)

    def test_w9_separates_live_from_late_collection(self):
        for is_live,now,match,want in [(True,151.,True,"LIVE_TERMINAL_MATCH"),(False,151.,True,"RECOVERY_ONLY"),
                                       (True,166.,True,"LIVE_TERMINAL_MATCH"),(True,102.,False,"MISMATCH"),
                                       (True,99.,True,"UNKNOWN_TIME")]:
            self.assertEqual(self.b.w9_status(match, is_live, 100.,now),want)

    def test_second_attempt_or_missing_peer_does_not_submit(self):
        for role in ("U","C"):
            folder = self.root/"arms"/role
            folder.mkdir(parents=True)
            with self.subTest(role=role), self.assertRaises(FileExistsError):
                self.b.create_attempt(self.root, role)
        with self.assertRaises(ValueError):
            self.b.prior_return(self.root, "a"*40)

    def test_nonterminal_collection_writes_nothing(self):
        expected = list(self.root.iterdir())
        with self.assertRaises(ValueError):
            self.b.collect(self.root,"U","41","41|RUNNING|0:0|",(),True,"a"*40)
        self.assertEqual(list(self.root.iterdir()),expected)

    def test_collection_preserves_case_and_rejects_late_as_peer(self):
        case_name = self.b.case_name("U")
        case = self.root/"B"/self.b.F8/"cases"/case_name
        (case/"post").mkdir(parents=True)
        for i in range(1,235):
            (case/"post"/("mix_%d.liggghts"%(i*32976))).write_text("synthetic")
        ctx=self.b.create_attempt(self.root,"U")
        (ctx/"control").mkdir()
        (ctx/"evidence").mkdir()
        self.b.put(case/"job_end.json", dict(job_id="41", returncode=0, end_unix=100.))
        for name in ("control/pair_pin.json","control/pair_authority.json","B_manifest.json"):
            self.b.put(self.root/name,{})
        for name in ("campaign_policy.json","approvals/"+case_name+"/approval.json","admission/"+case_name+".reservation.json","admission/"+case_name+".submission.json"):
            self.b.put(self.root/"B"/self.b.F8/name,{})
        with self.b.collection_lease(ctx), self.assertRaises(BlockingIOError):
            self.b.collect(self.root,"U","41","41|COMPLETED|0:0|",(0,0,0),False,"a"*40)
        self.assertFalse((ctx/"return.json").exists())
        with patch.dict(self.b.base, runtime=lambda *args: {"matches":True}), patch.object(self.b.time,"time",return_value=137.):
            self.assertEqual(self.b.collect(self.root,"U","41","41|COMPLETED|0:0|", (0,0,0),False,"a"*40),0)
        record=self.b.read(ctx/"return.json")
        self.assertEqual(record["w9"],"RECOVERY_ONLY")
        self.assertTrue(record["return_ready"])
        with self.assertRaises(ValueError):
            self.b.check_peer(record,"a"*40)
        result=ctx/record["directory"]
        self.assertEqual(len((result/"SHA256SUMS").read_text().splitlines()),2)
        self.assertEqual(self.b.verified_sums(result), record["archive_hashes"])

    def test_sums_bind_both_persisted_archives(self):
        d=self.root/"returns"
        d.mkdir()
        for n in ("b1_report.tar.gz","b1_full_result.tar.gz"):
            (d/n).write_bytes(b"synthetic")
        (d/"SHA256SUMS").write_text("".join(self.b.sha(d/n)+"  "+n+"\n" for n in ("b1_report.tar.gz","b1_full_result.tar.gz")))
        self.assertEqual(len(self.b.verified_sums(d)),2)
        (d/"b1_full_result.tar.gz").write_bytes(b"other")
        with self.assertRaises(ValueError):
            self.b.verified_sums(d)

if __name__=="__main__":
    unittest.main()
