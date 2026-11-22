"""Offline B2-U development scope, prior-evidence and terminal collection tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


class B2Tests(unittest.TestCase):
    def setUp(self):
        filename = Path(__file__).with_name("mixer_b2_u_ibb.py")
        self.assertTrue(filename.is_file(), "B2-U controller missing")
        spec = importlib.util.spec_from_file_location("b2test", filename)
        self.b = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.b)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_only_u_authority_and_explicit_go(self):
        b = self.b
        self.assertEqual(b.case_name("U"), "PRECAL_R1_B2_U")
        b.author_token("U", "GO_B2_U_ONCE")
        for role, token in [("C", "GO_B2_C_ONCE"), ("U", ""), ("U", "GO_B1_U_ONCE"), ("U", "collect")]:
            with self.subTest(role=role, token=token), self.assertRaises(ValueError):
                b.author_token(role, token)
        a = b.authority("a" * 40, {"path": "prior", "sha256": "b" * 64})
        self.assertEqual(a["allowed_to_submit"], ["PRECAL_R1_B2_U"])
        self.assertFalse(a["automatic_retry"])
        self.assertEqual(a["runtime_concurrency"], 1)

    def test_previous_pair_binds_both_original_pointers_and_small_manifests(self):
        b = self.b
        prev = self.root / "prev"
        pair = {"status": "DEVELOPMENT_READBACK_OK", "formal_review": False, "next_wave_author_go": False}
        pair_file = self.root / "pair.json"
        u_hash = None
        for role, jid in (("U", "368139"), ("C", "368316")):
            ctx = prev / "arms" / role
            out = ctx / "collection_123"
            out.mkdir(parents=True)
            archives = {"b1_report.tar.gz": "c" * 64, "b1_full_result.tar.gz": "e" * 64}
            (out / "SHA256SUMS").write_text("".join(h + "  " + k + "\n" for k,h in archives.items()), encoding="ascii")
            pointer = dict(label="DEVELOPMENT_DATA_ONLY", case="PRECAL_R1_B1_" + role, role=role,
                           release_pin=b.B1_PIN, job_id=jid, job_end_id=jid, runner_rc=0, return_ready=True,
                           exact_frame_names=True, frame_count=234, w9="LIVE_TERMINAL_MATCH",
                           post_runtime_matches=True, scheduler=dict(job_id=jid,state="COMPLETED",exit_code="0:0"),
                           directory=out.name, archive_hashes=archives)
            b.put(ctx / "return.json", pointer)
            digest = b.sha(ctx / "return.json")
            pair[role] = {"technical": {"return_pointer_sha256": digest, "archive_sha256": archives,
                                        "previous_return_sha256": u_hash if role == "C" else b.b1["N0_POINTER"]}}
            if role == "U":
                u_hash = digest
        b.put(pair_file, pair)
        with patch.object(b, "PAIR_SHA", b.sha(pair_file)):
            ref = b.previous_pair(prev, pair_file)
            self.assertEqual(ref, b.ref(prev / "arms/C/return.json"))
            sums_path = prev / "arms/C/collection_123/SHA256SUMS"
            sums_path.write_bytes(b"")
            with self.assertRaises(ValueError):
                b.previous_pair(prev, pair_file)
        with self.assertRaises(ValueError):
            b.previous_pair(prev, pair_file)

    def test_prior_rejects_changed_w9_wrong_job_and_boolean_rc(self):
        b = self.b
        record = dict(label="DEVELOPMENT_DATA_ONLY",case="PRECAL_R1_B1_C",role="C",release_pin=b.B1_PIN,
                      job_id="368316",job_end_id="368316",runner_rc=0,return_ready=True,
                      exact_frame_names=True,frame_count=234,w9="LIVE_TERMINAL_MATCH",post_runtime_matches=True,
                      scheduler=dict(job_id="368316",state="COMPLETED",exit_code="0:0"))
        b.prior_completion(record, "C", "368316")
        for k,v in (("w9","RECOVERY_ONLY"), ("runner_rc",False), ("job_id","368139"),
                    ("case","PRECAL_R1_B2_U"), ("frame_count",233), ("release_pin","0" * 40)):
            with self.subTest(k=k), self.assertRaises(ValueError):
                b.prior_completion(dict(record, **{k:v}), "C", "368316")

    def test_refuse_same_or_overlapping_prior_root_before_writes(self):
        b = self.b
        for prior in [self.root, self.root / "child", self.root.parent]:
            with self.subTest(prior=prior), self.assertRaises(ValueError):
                b.prepare(self.root, prior, "U", "GO_B2_U_ONCE", "a"*40, ())
        self.assertEqual(list(self.root.iterdir()), [])

    def test_unfinished_accounting_and_cross_arm_create_nothing(self):
        b = self.b
        with self.assertRaises(ValueError):
            b.collect(self.root, "U", "51", "51|RUNNING|0:0|", (), True, "a"*40)
        with self.assertRaises(ValueError):
            b.collect(self.root, "C", "51", "51|COMPLETED|0:0|", (), True, "a"*40)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_terminal_w9_and_exclusive_publication(self):
        b = self.b
        for live,expected_w9 in [(True,"LIVE_TERMINAL_MATCH"),(False,"RECOVERY_ONLY")]:
            root = self.root / str(live)
            case = root / "B" / b.F8 / "cases" / b.CASE
            (case / "post").mkdir(parents=True)
            for i in range(1,235):
                (case / "post" / ("mix_%d.liggghts" % (32976*i))).write_bytes(b"fixture")
            b.put(case / "job_end.json", {"returncode":0, "job_id":"51", "end_unix":100.})
            b.put(root / "arms/U/evidence/author_arm.json", {})
            for n in ["B_manifest.json","control/pair_pin.json","control/pair_authority.json",
                      "B/"+b.F8+"/campaign_policy.json","B/"+b.F8+"/approvals/"+b.CASE+"/approval.json",
                      "B/"+b.F8+"/admission/"+b.CASE+".submission.json"]:
                b.put(root / n, {})
            ctx = root / "arms/U"
            with patch.dict(b.base,runtime=lambda *a: {"matches":True}):
                self.assertEqual(b.collect(root,"U","51","51|COMPLETED|0:0|",(),live,"a"*40),0)
                receipt = (ctx / "return.json").read_bytes()
                result = json.loads(receipt)
                self.assertEqual(result["w9"], expected_w9)
                self.assertTrue(result["return_ready"])
                self.assertEqual(set(result["archive_hashes"]), set(b.ARCHIVES))
                for n,digest in result["archive_hashes"].items():
                    self.assertEqual(b.sha(ctx / result["directory"] / n), digest)
                with self.assertRaises(ValueError):
                    b.collect(root,"U","51","51|COMPLETED|0:0|",(),False,"a"*40)
                self.assertEqual((ctx / "return.json").read_bytes(), receipt)


if __name__ == "__main__":
    unittest.main()
