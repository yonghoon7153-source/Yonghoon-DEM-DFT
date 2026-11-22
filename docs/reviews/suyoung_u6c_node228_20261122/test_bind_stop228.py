"""Synthetic source binding and optional read-only checks of the actual returned bytes."""
import argparse
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest import mock


spec = importlib.util.spec_from_file_location("bind_stop228",Path(__file__).with_name("bind_stop228.py"))
bind = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bind)
author_return = None


class SourceBinding(unittest.TestCase):
    def test_only_changed_kernel_with_same_driver_matches(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root/"scripts").mkdir()
            kernel = root/"scripts/suyoung_multicontact_dev.py"
            auxiliary = root/"auxiliary.py"
            auxiliary.write_bytes(b"fixed helper")
            kernel.write_bytes(b"new")
            expected = {"RELEASE":"provenance", "scripts/suyoung_multicontact_dev.py":bind.sha(b"old"),
                        "auxiliary.py":bind.sha(auxiliary.read_bytes())}
            with mock.patch.object(bind,"KERNEL",bind.sha(b"old")):
                bind.verify_sources(expected,root)
                kernel.write_bytes(b"old")
                with self.assertRaisesRegex(ValueError,"KERNEL_UNCHANGED"):
                    bind.verify_sources(expected,root)
                kernel.write_bytes(b"new")
                auxiliary.write_bytes(b"changed")
                with self.assertRaisesRegex(ValueError,"DRIVER_CHANGED"):
                    bind.verify_sources(expected,root)


class TestReceipt(unittest.TestCase):
    def setUp(self):
        if author_return is None:
            self.skipTest("author-only return not supplied")

    def test_true_return(self):
        sources = bind.read_return(author_return)
        self.assertEqual(sources["scripts/suyoung_multicontact_dev.py"],bind.KERNEL)

    def mutated(self, filename, edit, expected_issue):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)/"synthetic.tar.gz"
            with tarfile.open(author_return) as original, tarfile.open(out,"w:gz") as mutated:
                for item in original:
                    if item.isfile():
                        content = original.extractfile(item).read()
                        if item.name == filename:
                            content = edit(content)
                        item.size = len(content)
                        mutated.addfile(item,io.BytesIO(content))
                    else:
                        mutated.addfile(item)
            with mock.patch.object(bind,"ARCHIVE",bind.sha(out.read_bytes())):
                with self.assertRaisesRegex(ValueError,expected_issue):
                    bind.read_return(out)

    def test_repacked_prefix_mismatch(self):
        self.mutated("run/ORIGINAL/trace.csv",lambda data: data.splitlines(keepends=True)[0],"STOP228_PREFIX")

    def test_repacked_wrong_attempt(self):
        def wrong(data):
            receipt = json.loads(data)
            receipt["attempted_step"] = 229
            return json.dumps(receipt).encode("ascii")
        self.mutated("run/ORIGINAL/stop.json",wrong,"STOP228_NODE")

    def test_repacked_false_terminal(self):
        self.mutated("run/screen.txt",lambda data:data.replace(b"COMMAND_RC=4",b"COMMAND_RC=0"),"STOP228_SCREEN")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--return-archive",type=Path)
    args,rest = parser.parse_known_args()
    author_return = args.return_archive
    unittest.main(argv=[sys.argv[0]]+rest)
