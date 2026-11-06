"""Safety boundary tests; fake external commands must never be called."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
class PrepareOnly(unittest.TestCase):
    def test_every_action_refuses_even_with_fake_go(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            marker = root / 'external_called'
            for name in ('ssh','sbatch','srun','mpirun','squeue','sacct','scancel','rsync','lmp_mpi'):
                p = root / name
                p.write_text('#!/bin/sh\nprintf called >> "$CALL_MARKER"\nexit 0\n')
                p.chmod(0o755)
            env = dict(os.environ, PATH=str(root)+':'+os.environ['PATH'], CALL_MARKER=str(marker), GO='YES', EXECUTE='1')
            for action in ('preflight','launch','watch','return','stop','unknown',''):
                p = subprocess.run(['/bin/bash',str(HERE/'prepare_only.sh'),action], env=env, capture_output=True, text=True)
                self.assertEqual(p.returncode, 64, (action,p.stdout,p.stderr))
                self.assertIn('PREPARATION_ONLY',p.stderr)
            self.assertFalse(marker.exists())
if __name__ == '__main__': unittest.main()
