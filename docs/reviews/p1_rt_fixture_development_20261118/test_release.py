"""Exercise the actual fixture worker on a local six-rank command double."""
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'p1_rt_fixture_runner_preparation_20261117'))
import test_rt_assembly as prior

class FixtureRun(unittest.TestCase):
    def exercise(self, mode='ok', ranks='6', bad_binary=False):
        self.assertTrue((HERE / 'build_release.py').exists(), 'development fixture builder required')
        spec = importlib.util.spec_from_file_location('new_release', HERE / 'build_release.py')
        release = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(release)
        with tempfile.TemporaryDirectory() as scratch:
            base = Path(scratch)
            packet = base / 'packet'
            release.build(packet)
            self.assertNotIn('run_unload_rt_candidate.sh', {p.name for p in packet.rglob('*')})
            (base / 'template').mkdir()
            prior.F.fixture(base / 'template', packet)
            (base / 'fake.py').write_text(prior.FAKE)
            mpi = base / 'mpirun'
            mpi.write_text('#!/bin/sh\nexec '+sys.executable+' '+str(base/'fake.py')+' "$@"\n')
            mpi.chmod(0o700)
            binary = base / 'lmp'
            binary.write_bytes(b'synthetic')
            binary.chmod(0o700)
            worker = packet / 'fixture.sh'
            raw = worker.read_text()
            self.assertEqual(raw.count(release.LMP_SHA), 1)
            if not bad_binary:
                worker.write_text(raw.replace(release.LMP_SHA, hashlib.sha256(b'synthetic').hexdigest()))
            env = dict(os.environ, SLURM_JOB_ID='123', SLURM_NTASKS=ranks, FAKE_ROOT=str(base),
                       FAKE_MODE=mode, LMP=str(binary), PATH=str(base)+':'+os.environ['PATH'])
            run = subprocess.run(['bash',str(worker)], cwd=base, env=env, capture_output=True, timeout=45)
            calls = base / 'calls.txt'
            names = [s.split()[0] for s in calls.read_text().splitlines()] if calls.exists() else []
            return run.returncode, names, (base / 'work/fixture.report.tgz').exists(), run.stderr
    def test_pass(self):
        rc, names, archive, err = self.exercise()
        self.assertEqual(rc, 0, err); self.assertEqual(names, ['P','RT1','RT2']); self.assertTrue(archive)
    def test_wrong_allocation_or_binary(self):
        for args in ({'ranks':'4'}, {'bad_binary':True}):
            rc, names, _, _ = self.exercise(**args)
            self.assertNotEqual(rc, 0); self.assertFalse(names)
    def test_failure_after_writing_checkpoint(self):
        rc, names, archive, _ = self.exercise('RT1_fail')
        self.assertNotEqual(rc, 0); self.assertEqual(names, ['P','RT1']); self.assertTrue(archive)
if __name__ == '__main__':
    unittest.main()
