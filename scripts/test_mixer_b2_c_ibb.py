"""Offline tests for B2-C admission, using synthetic returns only."""
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
U_PIN = "f9c8ee5a2cc590ceb70766d144e82ad571942535"
CASE = "PRECAL_R1_B2_U"
JOB = "368758"
NAMES = ("b2_report.tar.gz", "b2_full_result.tar.gz")


class B2C(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.local = root / "local"
        self.local.mkdir()
        self.remote = root / "original"
        self.proof = root / "proof.json"
        self.arm = self.remote / "arms/U"
        self.coll = self.arm / "collection_17"
        self.coll.mkdir(parents=True)
        self.job = self.remote / "B/docs/reviews/mixer_first8_launch_preparation_20261106/cases" / CASE / "submission.receipt.json"
        self.job.parent.mkdir(parents=True)
        self.job.write_text(json.dumps(dict(case=CASE, state="SUBMITTED", job_id=JOB)))
        hashes = {}
        for name in NAMES:
            (self.local / name).write_bytes(name.encode())
            hashes[name] = hashlib.sha256(name.encode()).hexdigest()
        self.record = dict(case=CASE, role="U", job_id=JOB, job_end_id=JOB, release_pin=U_PIN,
                           label="DEVELOPMENT_DATA_ONLY", runner_rc=0, return_ready=True,
                           frame_count=234, exact_frame_names=True, post_runtime_matches=True,
                           w9="LIVE_TERMINAL_MATCH", directory=self.coll.name, archive_hashes=hashes,
                           scheduler=dict(job_id=JOB, state="COMPLETED", exit_code="0:0"))
        self.sums = "".join(h+"  "+n+"\n" for n, h in hashes.items())
        self.save()
        self.api = runpy.run_path(str(HERE / "mixer_b2_u_completion.py"))

    def save(self):
        for folder in (self.local, self.coll):
            (folder / "SHA256SUMS").write_text(self.sums, encoding="ascii")
        for folder in (self.local, self.arm):
            (folder / "return.json").write_text(json.dumps(self.record), encoding="ascii")

    def local_check(self):
        self.api["verify_local"](self.local, self.proof)

    def remote_check(self):
        return self.api["verify_original"](self.remote, self.proof)

    def test_matching_receipts(self):
        self.local_check()
        self.assertEqual(self.remote_check(), self.arm / "return.json")

    def test_completion_identity_requirements(self):
        for key, bad in dict(case="PRECAL_R1_B2_C", role="C", release_pin="0"*40, job_id="1",
                             job_end_id="2", runner_rc=False, frame_count=233, exact_frame_names=False,
                             return_ready=False, post_runtime_matches=False, w9="RECOVERY_ONLY", directory="../other").items():
            with self.subTest(key=key):
                record = dict(self.record, **{key:bad})
                with self.assertRaises(ValueError):
                    self.api["check_record"](record)

    def test_scheduler_identity(self):
        for key, v in (("state","RUNNING"), ("exit_code","1:0"), ("job_id","1")):
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.api["check_record"](dict(self.record, scheduler=dict(self.record["scheduler"], **{key:v})))

    def test_both_local_archives_verified(self):
        for name in NAMES:
            with self.subTest(name=name):
                (self.local / name).write_bytes(b"changed")
                with self.assertRaises(ValueError):
                    self.local_check()
                self.assertFalse(self.proof.exists())
                (self.local / name).write_bytes(name.encode())

    def test_archives_and_checksum_inventory_exact(self):
        self.record["archive_hashes"].pop(NAMES[1])
        self.save()
        with self.assertRaises(ValueError):
            self.local_check()

    def test_remote_manifest_must_agree(self):
        self.local_check()
        (self.coll / "SHA256SUMS").write_text(self.sums + self.sums)
        with self.assertRaises(ValueError):
            self.remote_check()

    def test_remote_pointer_bytes_bound(self):
        self.local_check()
        p = self.arm / "return.json"
        p.write_bytes(p.read_bytes() + b" ")
        with self.assertRaises(ValueError):
            self.remote_check()

    def test_original_submission_bound(self):
        self.local_check()
        self.job.write_text(json.dumps(dict(case=CASE,state="SUBMITTED",job_id="1")))
        with self.assertRaises(ValueError):
            self.remote_check()

    def test_local_copy_exclusive(self):
        self.local_check()
        with self.assertRaises(FileExistsError):
            self.local_check()

    def test_separate_c_authority(self):
        c = runpy.run_path(str(HERE/"mixer_b2_c_ibb.py"))
        for role, token in (("U","GO_B2_U_ONCE"), ("C","GO_B2_U_ONCE"), ("C",""), ("U","GO_B2_C_ONCE")):
            with self.subTest(role=role, token=token), self.assertRaises((ValueError,RuntimeError)):
                c["author_token"](role,token)
        c["author_token"]("C","GO_B2_C_ONCE")
        a=c["authority"]("a"*40, {})
        self.assertEqual(a["allowed_to_submit"],["PRECAL_R1_B2_C"])
        self.assertEqual(a["runtime_concurrency"],1)
        self.assertFalse(a["automatic_retry"])

    def test_refuse_same_or_overlapping_prior_root_before_writes(self):
        from types import SimpleNamespace
        b = SimpleNamespace(**runpy.run_path(str(HERE / "mixer_b2_c_ibb.py")))
        self.root = Path(self.tmp.name)/"c"
        self.root.mkdir()
        for prior in [self.root, self.root / "child", self.root.parent]:
            with self.subTest(prior=prior), self.assertRaises(ValueError):
                b.prepare(self.root, prior, "C", "GO_B2_C_ONCE", "a"*40, ())
        self.assertEqual(list(self.root.iterdir()), [])

    def test_unfinished_accounting_and_cross_arm_create_nothing(self):
        from types import SimpleNamespace
        b = SimpleNamespace(**runpy.run_path(str(HERE / "mixer_b2_c_ibb.py")))
        self.root = Path(self.tmp.name)/"c"
        self.root.mkdir()
        with self.assertRaises(ValueError):
            b.collect(self.root, "C", "51", "51|RUNNING|0:0|", (), True, "a"*40)
        with self.assertRaises(ValueError):
            b.collect(self.root, "U", "51", "51|COMPLETED|0:0|", (), True, "a"*40)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_terminal_w9_and_exclusive_publication(self):
        from types import SimpleNamespace
        b = SimpleNamespace(**runpy.run_path(str(HERE / "mixer_b2_c_ibb.py")))
        self.root = Path(self.tmp.name)/"c"
        self.root.mkdir()
        for live,expected_w9 in [(True,"LIVE_TERMINAL_MATCH"),(False,"RECOVERY_ONLY")]:
            root = self.root / str(live)
            case = root / "B" / b.F8 / "cases" / b.CASE
            (case / "post").mkdir(parents=True)
            for i in range(1,235):
                (case / "post" / ("mix_%d.liggghts" % (32976*i))).write_bytes(b"fixture")
            b.put(case / "job_end.json", {"returncode":0, "job_id":"51", "end_unix":100.})
            b.put(root / "arms/C/evidence/author_arm.json", {})
            for n in ["control/b2_u_return.json","B_manifest.json","control/pair_pin.json","control/pair_authority.json",
                      "B/"+b.F8+"/campaign_policy.json","B/"+b.F8+"/approvals/"+b.CASE+"/approval.json",
                      "B/"+b.F8+"/admission/"+b.CASE+".submission.json"]:
                b.put(root / n, {})
            ctx = root / "arms/C"
            with patch.dict(b.base,runtime=lambda *a: {"matches":True}):
                self.assertEqual(b.collect(root,"C","51","51|COMPLETED|0:0|",(),live,"a"*40),0)
                receipt = (ctx / "return.json").read_bytes()
                result = json.loads(receipt)
                self.assertEqual(result["w9"], expected_w9)
                self.assertTrue(result["return_ready"])
                self.assertEqual(set(result["archive_hashes"]), set(b.ARCHIVES))
                for n,digest in result["archive_hashes"].items():
                    self.assertEqual(b.sha(ctx / result["directory"] / n), digest)
                with self.assertRaises(ValueError):
                    b.collect(root,"C","51","51|COMPLETED|0:0|",(),False,"a"*40)
                self.assertEqual((ctx / "return.json").read_bytes(), receipt)


if __name__ == "__main__":
    unittest.main()
