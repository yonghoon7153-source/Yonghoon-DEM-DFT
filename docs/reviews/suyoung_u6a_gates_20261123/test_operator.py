"""Exercise the real WSL operator shell with a manufactured driver, including a partial return."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
DRIVER = "docs/reviews/suyoung_u6a_gates_20261123/setting2_run.py"
PIN = "a" * 40
STUB = """import os,sys
from pathlib import Path
mode=sys.argv[1]
if mode=='arm':
    grid=sys.argv[sys.argv.index('--cells')+1]
    (Path(os.environ['HOME'])/'calls').open('a').write(grid+'\\n')
    if grid==os.environ.get('FAIL_CELL'): raise SystemExit(4)
elif mode=='summary':
    (Path(sys.argv[sys.argv.index('--run')+1])/'summary.json').write_text('{}')
"""


@unittest.skipUnless(sys.platform=="linux", "test in the operator WSL venv")
class OperatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)/"home"
        self.pkg = Path(self.tmp.name)/"pkg"
        py = self.home/"Yonghoon-DEM-DFT/venv/bin/python"
        py.parent.mkdir(parents=True)
        py.write_text('#!/bin/sh\nexec "'+sys.executable+'" "$@"\n')
        py.chmod(0o700)
        stub = self.pkg/DRIVER
        stub.parent.mkdir(parents=True)
        stub.write_text(STUB)
        (self.pkg/"RELEASE").write_text(PIN+"\n")
        (self.pkg/"SOURCE_SHA256SUMS").write_text("".join(
            hashlib.sha256((self.pkg/name).read_bytes()).hexdigest()+"  "+name+"\n"
            for name in ("RELEASE",DRIVER)))
        self.shell = self.pkg/"operator.sh"
        shutil.copyfile(HERE/"run_setting2.sh", self.shell)
        self.full,self.fine = self.home/"full.tar",self.home/"fine.tar"
        self.full.touch()
        self.fine.touch()

    def invoke(self, mode, **env):
        return subprocess.run(["bash",self.shell,mode,self.full,self.fine],cwd=self.pkg,
                              env=dict(os.environ,HOME=str(self.home),**env),
                              capture_output=True,text=True)

    def test_preflight_and_one_complete_return(self):
        self.assertEqual(self.invoke("CHECK_ONLY").returncode,0)
        self.assertFalse((self.home/"calls").exists())
        result=self.invoke("GO_SUYOUNG_U6A_SETTING2_ONCE")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual((self.home/"calls").read_text().splitlines(),["8","12","16","24"])
        self.assertNotEqual(self.invoke("GO_SUYOUNG_U6A_SETTING2_ONCE").returncode,0)
        self.assertEqual(len((self.home/"calls").read_text().splitlines()),4)
        archive=next(self.home.glob("*_return_*/*.tar.gz"))
        with tarfile.open(archive) as tar:
            self.assertIn("run/summary.json",tar.getnames())
            self.assertNotIn("run/operator_incomplete.json",tar.getnames())

    def test_partial_return(self):
        result=self.invoke("GO_SUYOUNG_U6A_SETTING2_ONCE",FAIL_CELL="12")
        self.assertEqual(result.returncode,4,result.stderr)
        self.assertEqual((self.home/"calls").read_text().splitlines(),["8","12"])
        archive=next(self.home.glob("*_return_*/*.tar.gz"))
        with tarfile.open(archive) as tar:
            self.assertIn("run/operator_incomplete.json",tar.getnames())
            self.assertNotIn("run/summary.json",tar.getnames())
            self.assertTrue(tar.extractfile("run/screen.txt").read().endswith(b"COMMAND_RC=4\n"))


if __name__=="__main__":
    unittest.main()
