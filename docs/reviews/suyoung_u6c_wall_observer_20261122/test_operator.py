"""Exercise only the local one-shot orchestration with a synthetic observer."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
GO = "GO_SUYOUNG_WALL_ONCE"
DUMMY = """import sys
from pathlib import Path
def main():
    if '--help' in sys.argv: return
    cells = sys.argv[sys.argv.index('--cells') + 1]
    folder = Path(sys.argv[sys.argv.index('--out') + 1])
    folder.mkdir()
    for name in ('wall.csv', 'observer.json', 'result.json'):
        (folder/name).write_text('fixture')
    (folder/'trace.csv').write_text(cells)
    if cells == '8' and (Path.home()/'stop').exists(): sys.exit(4)
if __name__ == '__main__': main()
"""


class Operator(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.home = root/"home"
        self.pkg = root/"pkg"
        self.obs = self.pkg/"docs/reviews/suyoung_u6c_wall_observer_20261122/observe.py"
        self.obs.parent.mkdir(parents=True)
        self.obs.write_text(DUMMY)
        summary = self.obs.with_name("wall_summary.py")
        summary.write_text("import sys\nfrom pathlib import Path\n"
                           "if '--help' not in sys.argv: Path(sys.argv[-1]).write_text('{}')\n")
        sums = "".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  "
                       + p.relative_to(self.pkg).as_posix() + "\n" for p in (self.obs,summary)).encode()
        (self.pkg/"SOURCE_SHA256SUMS").write_bytes(sums)
        self.block = self.pkg/"inner.txt"
        template = (HERE/"run_wsl.in").read_text()
        for src, cell in [("03f3bc2c106aa466f1ccc2b774e0b768f2a902792006609680faa53038434cdf", "8"),
                          ("5475cc87df297533002afb621cbdac06c0319ca40eb65ddf40322ae6c018b0de", "16")]:
            template = template.replace(src, hashlib.sha256(cell.encode()).hexdigest())
        self.block.write_text(template.replace("@PIN@", "1"*40).replace(
            "@SOURCE_SUMS@", hashlib.sha256(sums).hexdigest()))
        venv = self.home/"Yonghoon-DEM-DFT/venv/bin"
        venv.mkdir(parents=True)
        (venv/"python").write_text('#!/bin/sh\nexec "' + sys.executable + '" "$@"\n')
        (venv/"python").chmod(0o700)

    def invoke(self, token):
        return subprocess.run(["bash",str(self.block),token],env=dict(os.environ,HOME=str(self.home)),
                              capture_output=True,text=True,timeout=30)

    def test_check_only_and_bad_token_create_no_receipt(self):
        p = self.invoke("CHECK_ONLY")
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("CHECK_OK",p.stdout)
        self.assertNotEqual(self.invoke("GO").returncode,0)
        self.assertEqual(list(self.home.glob("suyoung_wall_*")),[])

    def test_source_mismatch_stops_before_reserving(self):
        self.obs.write_text("changed")
        self.assertNotEqual(self.invoke(GO).returncode,0)
        self.assertEqual(list(self.home.glob("suyoung_wall_*")),[])

    def test_success_archives_two_arms_and_blocks_reentry(self):
        p = self.invoke(GO)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        ret, = self.home.glob("suyoung_wall_return_*")
        self.assertIn("F16_RC=0", (ret/"screen.txt").read_text())
        self.assertIn("SUMMARY_RC=0", (ret/"screen.txt").read_text())
        subprocess.run(["sha256sum","-c","SHA256SUMS"],cwd=ret,check=True,capture_output=True)
        self.assertNotEqual(self.invoke(GO).returncode,0)
        self.assertEqual(len(list(self.home.glob("suyoung_wall_return_*"))),1)

    def test_f8_failure_collects_only_first_arm(self):
        (self.home/"stop").touch()
        p=self.invoke(GO)
        self.assertEqual(p.returncode,4,p.stdout+p.stderr)
        ret, = self.home.glob("suyoung_wall_return_*")
        text=(ret/"screen.txt").read_text()
        self.assertIn("F8_RC=4",text)
        self.assertNotIn("F16_BEGIN",text)
        self.assertIn("COMMAND_RC=4",text)

    def test_successful_observer_with_different_trace_stops_before_f16(self):
        wrong_pin = self.block.read_text().replace(hashlib.sha256(b"8").hexdigest(), "0"*64)
        self.block.write_text(wrong_pin)
        p = self.invoke(GO)
        self.assertEqual(p.returncode,4,p.stdout+p.stderr)
        ret, = self.home.glob("suyoung_wall_return_*")
        screen = (ret/"screen.txt").read_text()
        self.assertIn("F8_RC=4",screen)
        self.assertNotIn("F16_BEGIN",screen)


if __name__ == "__main__":
    unittest.main()
