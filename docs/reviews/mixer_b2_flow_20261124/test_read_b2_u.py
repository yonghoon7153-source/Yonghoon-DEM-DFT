import hashlib
import io
import json
from pathlib import Path
import runpy
import tarfile
import tempfile
import unittest
from unittest.mock import patch


R = runpy.run_path(str(Path(__file__).with_name("read_b2_u.py")))
C = R["CASE"]


def packed(path, pairs):
    with tarfile.open(path, "w:gz") as output:
        for name, raw in pairs:
            member = tarfile.TarInfo(name)
            member.size = len(raw)
            output.addfile(member, io.BytesIO(raw))


def files():
    return [(C + "/in.mixer", b"deck"), (C + "/deck_meta.json", b"meta"),
            (C + "/job_end.json", b'{"job_id":"368758","returncode":0,"end_unix":123}')] + [
        (C + "/post/mix_%d.liggghts" % (i * 32976), str(i * 32976).encode())
        for i in reversed(range(1, 235))]


class ReadbackTests(unittest.TestCase):
    def run_dumps(self, members):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "full.tar.gz"
            packed(path, members)
            reader = R["inspect_full"]
            options = {"DECK_SHA": hashlib.sha256(b"deck").hexdigest(),
                       "META_SHA": hashlib.sha256(b"meta").hexdigest()}
            with patch.dict(reader.__globals__, options):
                return reader(path, {"job_end_unix": 123}, self.read_frame)

    @staticmethod
    def read_frame(stream, expected):
        if int(stream.read()) != expected:
            raise ValueError("native timestamp")
        return {"step": expected}

    def test_chronology_and_last_nonrotating_sample(self):
        frames, bindings = self.run_dumps(files())
        self.assertEqual([f["step"] for f in frames], [n * 32976 for n in range(34, 235)])
        self.assertEqual(len(bindings), 201)
        self.assertEqual(bindings[0]["sha256"], hashlib.sha256(b"1121184").hexdigest())

    def test_missing_early_unmeasured_dump(self):
        with self.assertRaises(ValueError):
            self.run_dumps(files()[:-1])

    def test_duplicate_member(self):
        f = files()
        with self.assertRaises(ValueError):
            self.run_dumps(f + [f[-1]])

    def test_swapped_timestep(self):
        f = files()
        f[3] = (f[3][0], b"1")
        with self.assertRaisesRegex(ValueError, "native timestamp"):
            self.run_dumps(f)

    def test_foreign_dump(self):
        with self.assertRaises(ValueError):
            self.run_dumps(files() + [(C + "/post/mix_999.liggghts", b"1")])

    def test_wrong_source_or_job_end(self):
        for i in (0, 1, 2):
            with self.subTest(i=i), self.assertRaises((KeyError, ValueError)):
                f = files()
                f[i] = (f[i][0], b"{}")
                self.run_dumps(f)

    def test_traversal_or_foreign_case(self):
        for n in ("../x", C + "/../escape", "OTHER/else", C + "/bad\\name"):
            with self.subTest(path=n), self.assertRaises(ValueError):
                self.run_dumps(files() + [(n, b"x")])


def report_facts():
    pin = R["PIN"]
    manifest = hashlib.sha256(b"b").hexdigest()
    receipt = dict(directory="collection_867", archive_hashes={}, scheduler={"state": "COMPLETED",
                   "exit_code": "0:0", "raw": ["368758", "COMPLETED", "0:0", "1-06:41:30"]},
                   w9="LIVE_TERMINAL_MATCH", runner_rc=0, job_end_unix=100, post_start_unix=110,
                   post_finished_unix=120, post_runtime_error=None)
    runtime = dict(matches=True, mismatches=[], linked=["library"], packages=["engine"])
    contents = {
        "B_manifest.json": "b",
        "control/pair_pin.json": {"commit": pin},
        "control/pair_authority.json": dict(release_pin=pin, allowed_to_submit=[C],
                                            author_action="GO_B2_U_ONCE", asset_manifest=manifest),
        "evidence/author_arm.json": dict(pin=pin, case=C, token="GO_B2_U_ONCE"),
        "admission/" + C + ".submission.json": dict(case=C, state="SUBMITTED", job_id="368758"),
        "evidence/collection_867.json": {k: v for k, v in receipt.items() if k not in ("directory", "archive_hashes")},
        "evidence/runtime_pre/runtime.json": dict(runtime, collected_unix=9),
        "evidence/collection_867_post/runtime.json": dict(runtime, collected_unix=115),
    }
    return receipt, contents, manifest


class ArchivedReportTests(unittest.TestCase):
    def inspect(self, mutate=None):
        receipt, contents, manifest = report_facts()
        if mutate:
            mutate(receipt, contents)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.tar.gz"
            packed(path, [(name, obj.encode() if isinstance(obj, str) else json.dumps(obj).encode())
                          for name, obj in contents.items()])
            with patch.dict(R["inspect_report"].__globals__, B_MANIFEST=manifest):
                return R["inspect_report"](path, receipt)

    def test_archived_w9_resources_and_timing(self):
        self.assertEqual(self.inspect()["end_to_post_start_s"], 10)

    def test_partial_embedded_receipt(self):
        with self.assertRaisesRegex(ValueError, "collection"):
            self.inspect(lambda receipt, contents: contents["evidence/collection_867.json"].pop("runner_rc"))

    def test_wrong_submission(self):
        with self.assertRaisesRegex(ValueError, "submission"):
            self.inspect(lambda receipt, c: c["admission/" + C + ".submission.json"].update(job_id="123"))

    def test_runtime_files_or_declared_post_time_conflict(self):
        for updates in (dict(packages=["other"]), dict(matches=False), dict(mismatches=["binary"]),
                        dict(collected_unix=130)):
            with self.subTest(updates=updates), self.assertRaisesRegex(ValueError, "Runtime"):
                self.inspect(lambda receipt, c: c["evidence/collection_867_post/runtime.json"].update(updates))

    def test_protect_original_return_from_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            with self.assertRaisesRegex(ValueError, "outside"):
                R["readback"](folder, folder / "nested")


if __name__ == "__main__":
    unittest.main()
