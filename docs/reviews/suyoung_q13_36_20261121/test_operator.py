"""Exercise the author block with a fake model and a temporary HOME."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
GO = "GO_SUYOUNG_36_ONCE"
SOURCE = "6bdfac91520c868b5036071e6d60464972727f49"
DUMMY = """import json,sys
from pathlib import Path
a=sys.argv[1:]
out=Path(a[a.index('--out')+1])
if a[0]=='summarize':
    runs=Path(a[a.index('--runs')+1])
    out.write_text(json.dumps(sorted(p.name for p in runs.iterdir())))
    sys.exit(0)
model=a[a.index('--model')+1]
out.mkdir()
(out/'result.json').write_text(model)
if model=='S' and (Path.home()/'stop_s').exists(): sys.exit(4)
"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fake_history(path, wrong_trace=False):
    content = {'run/origin.txt': ('release='+SOURCE+'\n').encode()}
    entries = {}
    for model in 'SF':
        for cells in (12, 16, 24):
            label = model+str(cells)
            raw = (label+'\n').encode()
            trace_hash = '0'*64 if wrong_trace else sha(raw)
            entries[label] = {'trace_sha256': trace_hash}
            folder = 'run/arms/'+label+'/'
            content[folder+'trace.csv'] = raw
            content[folder+'result.json'] = json.dumps(dict(arm=model,cells=cells,
                trace_sha256=trace_hash,status='TARGET_BRACKETED')).encode()
    content['run/summary.json'] = json.dumps({'inputs': entries}).encode()
    with tarfile.open(path, "w:gz") as archive:
        for name, data in content.items():
            item = tarfile.TarInfo(name)
            item.size = len(data)
            archive.addfile(item, io.BytesIO(data))


class OperatorBlock(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.home = self.root/'home'
        self.pkg = self.root/'kit'
        (self.pkg/'scripts').mkdir(parents=True)
        (self.pkg/'scripts/suyoung_u6b36_dev.py').write_text(DUMMY)
        (self.pkg/'check_prior.py').write_bytes((HERE/'check_prior.py').read_bytes())
        venv = self.home/'Yonghoon-DEM-DFT/venv/bin'
        venv.mkdir(parents=True)
        (venv/'python').write_text('#!/bin/sh\nexec "'+sys.executable+'" "$@"\n')
        (venv/'python').chmod(0o700)
        self.history = self.root/'previous.tar.gz'
        self.block = self.pkg/'PASTE.txt'
        self.env = dict(os.environ, HOME=str(self.home))
        self.bind()

    def bind(self, wrong_trace=False):
        fake_history(self.history, wrong_trace)
        files = [self.pkg/'check_prior.py',self.pkg/'scripts/suyoung_u6b36_dev.py']
        sums = ''.join(sha(p.read_bytes())+'  '+p.relative_to(self.pkg).as_posix()+'\n' for p in files).encode()
        (self.pkg/'SOURCE_SHA256SUMS').write_bytes(sums)
        template = (HERE/'run_wsl.in').read_text()
        self.block.write_text(template.replace('@PIN@', '1'*40).replace('@SOURCE_SUMS@',sha(sums))
            .replace('a3877d077b56d74877a04215e06135bc3217b5c0f055bf0061a9ba93fcf49f00',sha(self.history.read_bytes())))

    def invoke(self, mode):
        return subprocess.run(['bash', str(self.block), mode, str(self.history)], cwd=self.root,
                              env=self.env, capture_output=True, text=True, timeout=35)

    def test_check_only_and_wrong_go_do_not_reserve(self):
        checked = self.invoke('CHECK_ONLY')
        self.assertEqual(checked.returncode,0,checked.stderr)
        self.assertIn('PRIOR_TRACES_OK=6',checked.stdout)
        self.assertNotEqual(self.invoke('GO').returncode,0)
        self.assertFalse(list(self.home.glob('suyoung_q13_once_*')))
        self.assertFalse(list(self.home.glob('suyoung_q13_return_*')))

    def test_rejects_corrupted_history_before_reservation(self):
        with self.history.open('ab') as stream:
            stream.write(b'extra')
        self.assertNotEqual(self.invoke(GO).returncode,0)
        self.assertFalse(list(self.home.glob('suyoung_q13_once_*')))

    def test_checks_individual_historical_trace(self):
        self.bind(wrong_trace=True)
        self.assertNotEqual(self.invoke('CHECK_ONLY').returncode,0)

    def test_only_new_arms_once_and_return_hashes(self):
        p = self.invoke(GO)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        ret, = self.home.glob('suyoung_q13_return_*')
        self.assertIn('S36_RC=0',(ret/'screen.txt').read_text())
        with tarfile.open(ret/'suyoung_q13_result.tar.gz') as archive:
            self.assertEqual(json.load(archive.extractfile('run/summary.json')),['F36','S36'])
            self.assertFalse(any('previous.tar.gz' in n for n in archive.getnames()))
        subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=ret,check=True,stdout=subprocess.PIPE)
        self.assertNotEqual(self.invoke(GO).returncode,0)
        self.assertEqual(len(list(self.home.glob('suyoung_q13_return_*'))),1)

    def test_stop_after_first_failure_pack_evidence(self):
        (self.home/'stop_s').touch()
        p = self.invoke(GO)
        self.assertEqual(p.returncode,4,p.stdout+p.stderr)
        ret, = self.home.glob('suyoung_q13_return_*')
        with tarfile.open(ret/'suyoung_q13_result.tar.gz') as archive:
            self.assertIn('run/arms/S36/result.json',archive.getnames())
            self.assertNotIn('run/arms/F36',archive.getnames())
        self.assertNotEqual(self.invoke(GO).returncode,0)


if __name__ == '__main__':
    unittest.main()
