"""Exercise the WSL shell without advancing any material points."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
DRIVER = "docs/reviews/suyoung_u6b_setting2_20261123/setting2_u6b.py"
MODE = "GO_SUYOUNG_U6B_SETTING2_ONCE"


@unittest.skipUnless(sys.platform == "linux", "operator uses the WSL author venv")
class Operator(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.pkg = Path(temporary.name) / "source"
        self.home = Path(temporary.name) / "home"
        py = self.home / "Yonghoon-DEM-DFT/venv/bin/python"
        py.parent.mkdir(parents=True)
        py.write_text('#!/bin/sh\nexec "' + sys.executable + '" "$@"\n')
        py.chmod(0o700)
        script = self.pkg / DRIVER
        script.parent.mkdir(parents=True)
        script.write_text("""
import os, sys
from pathlib import Path
assert Path(sys.argv[sys.argv.index('--gate') + 1]).read_text() == 'fixture'
if sys.argv[1] == 'arm':
    cells = sys.argv[sys.argv.index('--cells') + 1]
    with (Path.home() / 'calls').open('a') as f:
        print(cells, file=f)
    if cells == os.environ.get('FAIL_CELL'):
        sys.exit(4)
if sys.argv[1] == 'summary':
    (Path(sys.argv[sys.argv.index('--run') + 1]) / 'summary.json').write_text('{}')
""")
        (self.pkg / "RELEASE").write_text("a"*40 + "\n")
        manifest = "".join(hashlib.sha256((self.pkg / name).read_bytes()).hexdigest() + "  " + name + "\n"
                           for name in ("RELEASE", DRIVER))
        (self.pkg / "SOURCE_SHA256SUMS").write_text(manifest)
        self.gate = self.home / "gate.tar.gz"
        self.gate.write_text("fixture")

    def shell(self, mode, **env):
        return subprocess.run(["bash", HERE / "run_u6b.sh", mode, self.gate], cwd=self.pkg,
                              env=dict(os.environ, HOME=str(self.home), **env), capture_output=True, text=True)

    def test_one_run_and_read_only_check(self):
        pre = self.shell("CHECK_ONLY")
        self.assertEqual(pre.returncode, 0, pre.stderr)
        self.assertFalse((self.home / "calls").exists())
        self.assertEqual(list(self.home.glob("*_once_*")), [])
        good = self.shell(MODE)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertNotEqual(self.shell(MODE).returncode, 0)
        self.assertEqual((self.home / "calls").read_text().splitlines(), ["8", "12", "16", "24"])
        archive = next(self.home.glob("*_return_*/*.tar.gz"))
        with tarfile.open(archive) as tar:
            self.assertIn("run/summary.json", tar.getnames())
            self.assertNotIn("run/operator_incomplete.json", tar.getnames())

    def test_partial_runs_keep_the_rc_and_log(self):
        failure = self.shell(MODE, FAIL_CELL="12")
        self.assertEqual(failure.returncode, 4, failure.stderr)
        self.assertEqual((self.home / "calls").read_text().splitlines(), ["8", "12"])
        with tarfile.open(next(self.home.glob("*_return_*/*.tar.gz"))) as tar:
            self.assertIn("run/operator_incomplete.json", tar.getnames())
            self.assertNotIn("run/summary.json", tar.getnames())
            self.assertTrue(tar.extractfile("run/screen.txt").read().endswith(b"COMMAND_RC=4\n"))


if __name__ == "__main__":
    unittest.main()
