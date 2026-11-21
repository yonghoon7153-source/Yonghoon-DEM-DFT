"""Exercise the WSL one-shot launcher with a synthetic calculation and reader."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
GO = "GO_SUYOUNG_F8_DENSE_SEED_ONCE"
WALL = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
HALF = "e574396d010514b3cd77f57d2e06d0c25227c88a7b6e985577f2981aa8c154e4"
FAKE = """import sys
from pathlib import Path
if '--help' in sys.argv:
    sys.exit(0)
mode = sys.argv[1]
out = Path(sys.argv[sys.argv.index('--out')+1])
if mode == 'run':
    assert sys.argv[sys.argv.index('--budget')+1] == '1740'
    assert Path(sys.argv[sys.argv.index('--source-dir')+1]).is_dir()
    out.mkdir()
    (out/'trace.csv').write_text('synthetic')
    if (Path.home()/'partial').exists(): sys.exit(4)
elif mode == 'read':
    assert Path(sys.argv[sys.argv.index('--wall')+1]).read_bytes() == b'prior'
    assert Path(sys.argv[sys.argv.index('--half')+1]).read_bytes() == b'half'
    assert (Path(sys.argv[sys.argv.index('--arm')+1])/'trace.csv').is_file()
    out.write_text('{"status":"fixture"}')
    if (Path.home()/'invalid').exists(): sys.exit(4)
else: sys.exit(2)
"""


class Operator(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.home = root/"home"
        self.pkg = root/"pkg"
        self.driver = self.pkg/"docs/reviews/suyoung_u6c_dt_return_20261122/seed_control.py"
        self.driver.parent.mkdir(parents=True)
        (self.pkg/"scripts").mkdir()
        self.driver.write_text(FAKE)
        self.prior = root/"wall return with space.tar.gz"
        self.prior.write_bytes(b"prior")
        self.half = root/"half return.tar.gz"
        self.half.write_bytes(b"half")
        sums = (hashlib.sha256(self.driver.read_bytes()).hexdigest() + "  "
                + self.driver.relative_to(self.pkg).as_posix() + "\n").encode()
        (self.pkg/"SOURCE_SHA256SUMS").write_bytes(sums)
        self.block = self.pkg/"inner.txt"
        template = (HERE/"run_wsl.in").read_text()
        self.block.write_text(template.replace(WALL, hashlib.sha256(b"prior").hexdigest()).replace(
            HALF, hashlib.sha256(b"half").hexdigest()).replace(
            "@PIN@", "1"*40).replace("@SOURCE_SUMS@", hashlib.sha256(sums).hexdigest()))
        venv = self.home/"Yonghoon-DEM-DFT/venv/bin"
        venv.mkdir(parents=True)
        (venv/"python").write_text('#!/bin/sh\nexec "' + sys.executable + '" "$@"\n')
        (venv/"python").chmod(0o700)

    def invoke(self, token, *paths):
        return subprocess.run(["bash",str(self.block),token,*map(str,paths)],
                              cwd=self.prior.parent,env=dict(os.environ,HOME=str(self.home)),
                              capture_output=True,text=True,timeout=30)

    def test_check_only_and_bad_tokens_never_reserve(self):
        p = self.invoke("CHECK_ONLY", self.prior.name,self.half.name)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("CHECK_OK",p.stdout)
        self.assertNotEqual(self.invoke(GO).returncode,0)
        self.assertNotEqual(self.invoke("GO",self.prior,self.half).returncode,0)
        self.assertEqual(list(self.home.glob("suyoung_seed_*")),[])

    def test_half_mismatch_stops_before_reserving(self):
        self.half.write_bytes(b"wrong")
        self.assertNotEqual(self.invoke(GO,self.prior,self.half).returncode,0)
        self.assertEqual(list(self.home.glob("suyoung_seed_*")),[])

    def test_prior_mismatch_stops_before_reserving(self):
        self.prior.write_bytes(b"wrong")
        self.assertNotEqual(self.invoke(GO,self.prior,self.half).returncode,0)
        self.assertEqual(list(self.home.glob("suyoung_seed_*")),[])

    def test_source_mismatch_stops_before_reserving(self):
        self.driver.write_text("wrong")
        self.assertNotEqual(self.invoke(GO,self.prior,self.half).returncode,0)
        self.assertEqual(list(self.home.glob("suyoung_seed_*")),[])

    def test_success_returns_one_new_arm_and_declines_reentry(self):
        p = self.invoke(GO,self.prior.name,self.half.name)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        ret, = self.home.glob("suyoung_seed_return_*")
        screen = (ret/"screen.txt").read_text()
        self.assertIn("READBACK_REQUIRED", screen)
        self.assertIn("DEVELOPMENT_ONLY", screen)
        self.assertNotIn(str(self.home), screen)
        self.assertIn("RETURN_DIRECTORY="+str(ret), p.stdout)
        self.assertIn("RETURN_DIRECTORY="+str(ret), (self.home/"suyoung_seed_once_1122/receipt.txt").read_text())
        subprocess.run(["sha256sum","-c","SHA256SUMS"],cwd=ret,check=True,capture_output=True)
        with tarfile.open(ret/"suyoung_seed_result.tar.gz") as z:
            self.assertIn("run/seed_summary.json",z.getnames())
            self.assertIn("run/F8_DENSE/trace.csv",z.getnames())
        self.assertNotEqual(self.invoke(GO,self.prior,self.half).returncode,0)
        self.assertEqual(len(list(self.home.glob("suyoung_seed_return_*"))),1)

    def test_incomplete_run_returns_partial_evidence(self):
        (self.home/"partial").touch()
        p=self.invoke(GO,self.prior,self.half)
        self.assertEqual(p.returncode,4,p.stdout+p.stderr)
        ret, = self.home.glob("suyoung_seed_return_*")
        screen=(ret/"screen.txt").read_text()
        self.assertIn("F8_DENSE_RC=4",screen)
        self.assertNotIn("READBACK_REQUIRED",screen)
        self.assertNotIn("SUMMARY_RC=",screen)
        with tarfile.open(ret/"suyoung_seed_result.tar.gz") as z:
            self.assertIn("run/F8_DENSE/trace.csv",z.getnames())

    def test_reader_failure_reports_incomplete_and_archives_its_output(self):
        (self.home/"invalid").touch()
        p=self.invoke(GO,self.prior,self.half)
        self.assertEqual(p.returncode,4,p.stdout+p.stderr)
        ret, = self.home.glob("suyoung_seed_return_*")
        self.assertIn("SUMMARY_RC=4",(ret/"screen.txt").read_text())
        self.assertNotIn("READBACK_REQUIRED",(ret/"screen.txt").read_text())
        with tarfile.open(ret/"suyoung_seed_result.tar.gz") as z:
            self.assertIn("run/seed_summary.json",z.getnames())


if __name__ == "__main__":
    unittest.main()
