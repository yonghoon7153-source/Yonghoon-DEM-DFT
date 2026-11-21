"""Test the operator's one-shot workflow using a dummy solver and temporary home."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "run_wsl.in"
GO = "GO_SUYOUNG_DENSE_ONCE"
DUMMY = """import json, sys
from pathlib import Path
args = sys.argv[1:]
out = Path(args[args.index('--out') + 1])
if 'summarize' in args:
    out.write_text(json.dumps({'arms': sorted(p.name for p in Path(args[args.index('--runs')+1]).iterdir() if p.is_dir())}))
    sys.exit(0)
out.mkdir()
(out/'result.json').write_text('{}')
if __file__.endswith('suyoung_u6c_dev.py'):
    (out/'u6c_observations.json').write_text('{}')
if (Path(__file__).resolve().parents[1]/'stop_on').is_file() and out.name=='S12':
    sys.exit(4)
"""

class Workflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pkg = self.root / "operator"
        self.scripts = self.pkg / "scripts"
        self.scripts.mkdir(parents=True)
        self.home = self.root / "home"
        venv = self.home / "Yonghoon-DEM-DFT/venv/bin"
        venv.mkdir(parents=True)
        # Retain an existing venv's pyvenv.cfg and scientific packages.
        (venv / "python").write_text('#!/bin/sh\nexec "'+sys.executable+'" "$@"\n')
        (venv / "python").chmod(0o700)
        for name in ("suyoung_u6b_dev.py", "suyoung_u6c_dev.py"):
            (self.scripts/name).write_text(DUMMY)
        for cells in (12,16):
            hist = self.pkg/"historical"/("F%d"%cells)
            hist.mkdir(parents=True)
            (hist/"trace.csv").write_text("synthetic\n")
        files=sorted(p for p in self.pkg.rglob("*") if p.is_file())
        sums="".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(self.pkg).as_posix()+"\n" for p in files).encode()
        (self.pkg/"SOURCE_SHA256SUMS").write_bytes(sums)
        self.block=self.pkg/"PASTE.txt"
        self.block.write_text(TEMPLATE.read_text().replace("@SOURCE_SUMS@",hashlib.sha256(sums).hexdigest()).replace("@PIN@", "1"*40))
        self.env=dict(os.environ,HOME=str(self.home))

    def invoke(self, *argv):
        return subprocess.run(["bash",str(self.block),*argv],cwd=self.root,env=self.env,
                              capture_output=True,text=True,timeout=45)

    def test_no_token_or_mismatch_creates_no_attempt(self):
        self.assertEqual(self.invoke().returncode,2)
        (self.scripts/"suyoung_u6b_dev.py").write_text("changed")
        self.assertNotEqual(self.invoke(GO).returncode,0)
        self.assertFalse(list(self.home.glob("suyoung_dense_once_*")))

    def test_complete_has_eight_arms_and_one_observer(self):
        run=self.invoke(GO)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
        ret=next(self.root.glob("suyoung_dense_return_*"))
        with tarfile.open(ret/"suyoung_dense_result.tar.gz","r:gz") as bundle:
            names=bundle.getnames()
            summary=json.load(bundle.extractfile("run/summary.json"))
            self.assertEqual(len(summary["arms"]),8)
            self.assertEqual([n for n in names if n.endswith("u6c_observations.json")], ["run/arms/F8/u6c_observations.json"])
        self.assertEqual(self.invoke(GO).returncode,2)
        self.assertEqual(len(list(self.root.glob("suyoung_dense_return_*"))),1)

    def test_failed_arm_retains_logs_and_blocks_next_arm(self):
        (self.pkg/"stop_on").touch()
        run=self.invoke(GO)
        self.assertEqual(run.returncode,4,run.stdout+run.stderr)
        ret=next(self.root.glob("suyoung_dense_return_*"))
        self.assertIn("COMMAND_RC=4",(ret/"screen.txt").read_text())
        with tarfile.open(ret/"suyoung_dense_result.tar.gz","r:gz") as bundle:
            self.assertIn("run/arms/S12/result.json",bundle.getnames())
            self.assertNotIn("run/arms/F24/result.json",bundle.getnames())
            self.assertIn("run/partial_summary.json",bundle.getnames())
        self.assertEqual(self.invoke(GO).returncode,2)

if __name__=="__main__":
    unittest.main()
