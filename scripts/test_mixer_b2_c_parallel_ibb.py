"""Offline authorization and return tests for the single overlapping B2-C arm."""
import json
from pathlib import Path
import runpy
import tarfile
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
API = runpy.run_path(str(HERE / "mixer_b2_c_ibb.py"))
TOKEN = "GO_B2_C_PARALLEL_ONCE"
U = API["u_completion"]
C = API["CASE"]


class Parallel(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.u = self.root / "u"
        self.c = self.root / "c"
        f8 = self.u / "B" / API["F8"]
        self.release = self.u / "control/pair_pin.json"
        self.go = self.u / "control/pair_authority.json"
        self.ap = f8 / "approvals" / U["U_CASE"] / "approval.json"
        self.receipt = f8 / "cases" / U["U_CASE"] / "submission.receipt.json"
        self.snapshot = self.c / "control/b2_u_submission.json"
        API["put"](self.release, dict(commit=U["U_PIN"]))
        API["put"](self.go, dict(release_pin=U["U_PIN"], author_action="GO_B2_U_ONCE",
                                  allowed_to_submit=[U["U_CASE"]], execution_authorized=True))
        API["put"](self.ap, dict(case=U["U_CASE"], wave_release=[U["U_CASE"]], np=20,
                                 execution_authorized=True, author_go=API["ref"](self.go)))
        API["put"](self.receipt, dict(case=U["U_CASE"], job_id=U["U_JOB"], state="SUBMITTED",
                                      returncode=0, approval_sha256=API["sha"](self.ap)))

    def prior(self):
        self.assertIn("acknowledged_peer", API)
        return API["acknowledged_peer"](self.u)

    def test_acknowledged_peer_without_completion_or_w9(self):
        files = {p:p.read_bytes() for p in self.u.rglob("*") if p.is_file()}
        peer = self.prior()
        self.assertEqual(peer["job_id"], U["U_JOB"])
        self.assertEqual(peer["evidence_type"], "SUBMISSION_ACKNOWLEDGEMENT")
        self.assertEqual(peer["files"]["submission"], API["ref"](self.receipt))
        self.assertEqual(set(peer["files"]), {"submission", "approval", "authority", "release"})
        self.assertNotIn("w9", peer)
        self.assertEqual(files, {p:p.read_bytes() for p in self.u.rglob("*") if p.is_file()})

    def test_receipt_job_case_state_and_approval_hash_are_bound(self):
        original = json.loads(self.receipt.read_bytes())
        for key, bad in (("job_id","1"), ("state","AMBIGUOUS_OR_FAILED_HOLD"), ("case",C),
                         ("approval_sha256","0"*64), ("returncode",1), ("returncode",False)):
            with self.subTest(key=key):
                self.receipt.write_text(json.dumps(dict(original, **{key:bad})))
                with self.assertRaises(ValueError):
                    self.prior()

    def test_pin_and_u_approval_are_bound(self):
        self.release.write_text(json.dumps({"commit":"0"*40}))
        with self.assertRaises(ValueError):
            self.prior()
        self.release.write_text(json.dumps({"commit":U["U_PIN"]}))
        self.go.write_bytes(self.go.read_bytes()+b" ")
        with self.assertRaises(ValueError):
            self.prior()

    def test_incomplete_u_record_rejected(self):
        self.ap.unlink()
        with self.assertRaises((FileNotFoundError, ValueError)):
            self.prior()

    def test_authority_is_single_c_with_explicit_deviation(self):
        self.assertIn("PARALLEL_TOKEN", API)
        auth = API["authority"]("c"*40, {}, parallel=True)
        self.assertEqual(auth["author_action"], TOKEN)
        self.assertEqual(auth["runtime_concurrency"], 2)
        self.assertEqual(auth["allowed_to_submit"], [C])
        self.assertFalse(auth["automatic_retry"])
        self.assertEqual(auth["peer_admission"], "B2_U_TERMINAL_AND_W9_WAIVED_20261123")
        for role,token in (("U",TOKEN), ("C",API["TOKEN"]), ("C","")):
            with self.subTest(role=role, token=token), self.assertRaises(ValueError):
                API["author_token"](role, token, parallel=True)
        API["author_token"]("C", TOKEN, parallel=True)
        with self.assertRaises(ValueError):
            API["author_token"]("C", TOKEN)

    def test_parallel_collect_archives_ack_and_measures_own_w9(self):
        self.assertIn("PARALLEL_TOKEN", API)
        for live,w9 in ((True,"LIVE_TERMINAL_MATCH"),(False,"RECOVERY_ONLY")):
            root=self.c/str(live)
            case=root/"B"/API["F8"]/"cases"/C
            (case/"post").mkdir(parents=True)
            for i in range(1,235):
                (case/"post"/("mix_%d.liggghts" % (32976*i))).touch()
            API["put"](case/"job_end.json",dict(returncode=0,job_id="51",end_unix=100.))
            for n in ("control/b2_u_submission.json", "B_manifest.json", "control/pair_pin.json",
                      "control/pair_authority.json", "arms/C/evidence/author_arm.json",
                      "B/"+API["F8"]+"/campaign_policy.json", "B/"+API["F8"]+"/approvals/"+C+"/approval.json",
                      "B/"+API["F8"]+"/admission/"+C+".submission.json"):
                API["put"](root/n,{})
            with patch.dict(API["base"], runtime=lambda *a: {"matches":True}):
                self.assertEqual(API["collect"](root,"C","51","51|COMPLETED|0:0|",(),live,
                                                "c"*40,parallel=True),0)
            arm=root/"arms/C"
            receipt=json.loads((arm/"return.json").read_bytes())
            self.assertEqual(receipt["w9"],w9)
            self.assertEqual(receipt["frame_count"],234)
            self.assertTrue(receipt["return_ready"])
            with tarfile.open(arm/receipt["directory"]/"b2_report.tar.gz") as archive:
                self.assertIn("control/b2_u_submission.json",archive.getnames())
                self.assertNotIn("control/b2_u_return.json",archive.getnames())


if __name__ == "__main__":
    unittest.main()
