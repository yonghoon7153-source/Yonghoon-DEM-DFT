import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import unittest
from unittest.mock import patch


D = runpy.run_path(str(Path(__file__).with_name("read_inventory_receipts.py")))
ROOT = Path(sys.argv.pop()).resolve().as_posix()


class Receipts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixed = {name: subprocess.check_output(
            ["git", "-c", "safe.directory=" + ROOT, "-C", ROOT, "show", D["BASE"] + ":" + name])
            for name in D["BLOBS"]}

    def test_received_case_coverage_and_limits(self):
        with patch("builtins.open", side_effect=AssertionError("study path access")):
            result = D["readback"](self.fixed)
        self.assertEqual((result["cases_counted"], result["logs_counted"]), (30, 60))
        self.assertEqual({r["case"] for r in result["cases"]}, {"lhs00_%03d" % n for n in range(100, 130)})
        self.assertEqual(result["source_lead_as_reported"], "NONE_KNOWN")
        self.assertEqual(result["execution_identity"], "NOT_ESTABLISHED")
        self.assertEqual(result["section5_pressure_qualification"], "UNRESOLVED")
        self.assertEqual((result["tau"], result["release_v13"]), ("NOT_EVALUATED", "NOT_AUTHORIZED"))
        for row in result["cases"]:
            self.assertEqual(set(row), {"case", "b7_rows_each", "log_liggghts_bytes", "log_txt_bytes"})

    def test_tampered_raw_value_cannot_reach_report(self):
        raw = dict(self.fixed)
        name = next(iter(raw))
        record = json.loads(raw[name])
        record["cases"][0]["logs"]["log.txt"]["pressure_mpa"] = "VALUE_CANARY"
        raw[name] = json.dumps(record).encode()
        with self.assertRaisesRegex(ValueError, "^fixed metadata contract mismatch$"):
            D["readback"](raw)

    def test_missing_and_extra_members(self):
        raw = dict(self.fixed)
        raw.pop(next(iter(raw)))
        for subset in [raw, dict(self.fixed, ibb184=b"VALUE_CANARY")]:
            with self.subTest(keys=len(subset)), self.assertRaises(ValueError):
                D["readback"](subset)

    def test_removed_row_even_if_synthetic_hash_declared(self):
        hashes = D["readback"].__globals__["BLOBS"]
        raw = dict(self.fixed)
        p = next(iter(raw))
        inventory = json.loads(raw[p])
        inventory["cases"].pop()
        raw[p] = json.dumps(inventory).encode()
        q = list(raw)[1]
        receipt = json.loads(raw[q])
        receipt["extracted_json_sha256"] = hashlib.sha256(raw[p]).hexdigest()
        raw[q] = json.dumps(receipt).encode()
        altered = {k: hashlib.sha256(v).hexdigest() for k, v in raw.items()}
        with patch.dict(hashes, altered), self.assertRaises(ValueError):
            D["readback"](raw)

    def test_duplicate_and_damaged_payload(self):
        with self.assertRaises(ValueError):
            D["unique"]([("a", 0), ("a", 1)])
        with self.assertRaises(ValueError):
            D["unpack_metadata"]("?!broken")


if __name__ == "__main__":
    unittest.main()
