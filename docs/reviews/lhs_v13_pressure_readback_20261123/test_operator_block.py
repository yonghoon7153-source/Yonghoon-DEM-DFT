"""Whole operator TXT and return reader, with a simulated scanner and an isolated temporary home."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

HERE = Path(__file__).parent
ROOT = Path(sys.argv.pop()).resolve()
MAKER = runpy.run_path(str(HERE / "make_live_block.py"))
READER = runpy.run_path(str(HERE / "check_return.py"))
sha = READER["sha"]
SAMPLE = runpy.run_path(str(HERE / "test_live_metadata.py"))["valid"]


class SimulatedOperator(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.txt = self.dir / "block.txt"
        self.prior = self.dir / "historical.json"
        pin = "9352c4ece"
        name = "docs/data/lhs_wsl30_inventory_20261108/lhs_wsl30_inventory_received_20261108.json"
        self.prior.write_bytes(subprocess.check_output(
            ["git", "-c", "safe.directory=" + ROOT.as_posix(), "-C", str(ROOT), "show", pin + ":" + name]))
        with contextlib.redirect_stdout(io.StringIO()):
            MAKER["main"](ROOT, self.txt)
        self.body = self.txt.read_text("ascii").split("<<'LHS_LIVE'\n", 1)[1].rsplit("\nLHS_LIVE\n", 1)[0]

    def run_block(self, output, rc=0):
        fakepwd = SimpleNamespace(getpwuid=lambda uid: SimpleNamespace(pw_dir=str(self.dir)))

        def scanner(argv, **kwargs):
            self.assertEqual(argv, ["/bin/sh", "-s", "--", "wsl"])
            self.assertEqual(sha(kwargs["input"]), READER["D"]["SCANNER_SHA"])
            return SimpleNamespace(stdout=output, stderr=b"", returncode=rc)
        with patch.dict(sys.modules, {"pwd": fakepwd}), patch("os.geteuid", create=True, return_value=1), \
                patch("platform.release", return_value="microsoft-fixture"), patch("subprocess.run", side_effect=scanner), \
                contextlib.redirect_stdout(io.StringIO()) as screen, self.assertRaises(SystemExit) as ex:
            exec(compile(self.body, "operator.txt", "exec"), {})
        archive = next(self.dir.glob("lhs_wsl30_pressure_return_*/*.zip"))
        return ex.exception.code, archive, screen.getvalue()

    def test_success_and_archive_hash_check(self):
        rc, archive, screen = self.run_block(json.dumps(SAMPLE()).encode())
        self.assertEqual(rc, 0)
        self.assertIn(sha(archive.read_bytes()), screen)
        result = READER["compare"](archive, sha(archive.read_bytes()), self.prior)
        self.assertEqual(len(result["changed_metadata_cases_since_2026_11_08"]), 30)
        self.assertEqual(result["section5"], "UNRESOLVED")
        with self.assertRaises(ValueError):
            READER["compare"](archive, "0" * 64, self.prior)

    def test_incomplete_stdout_is_not_archived_or_printed(self):
        rc, archive, screen = self.run_block(b'{"pressure_mpa":"VALUE_CANARY"}', 2)
        self.assertEqual(rc, 2)
        self.assertNotIn("VALUE_CANARY", screen)
        with zipfile.ZipFile(archive) as z:
            self.assertEqual(set(z.namelist()), {"receipt.json", "SHA256SUMS"})
            self.assertTrue(all(b"VALUE_CANARY" not in z.read(n) for n in z.namelist()))
        result = READER["compare"](archive, sha(archive.read_bytes()), self.prior)
        self.assertEqual(result["status"], "INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
