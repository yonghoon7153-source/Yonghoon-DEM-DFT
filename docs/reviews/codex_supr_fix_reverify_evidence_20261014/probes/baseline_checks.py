"""Read-only verification of the pinned snapshot; writes only reviewer evidence."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time

R = Path(__file__).resolve().parents[1]
S = R / 'source'
E = R / 'evidence'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
           TEMP=str(R/'tmp'), TMP=str(R/'tmp'), TMPDIR=str(R/'tmp'),
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
runs = []
for label, argv in [
    ('receipt_selftest', ['scripts/supp20_input_receipt.py', '--selftest']),
    ('receipt_container', ['scripts/supp20_input_receipt.py']),
    ('release_v13', ['scripts/test_lhs_release_v13.py']),
]:
    start = time.monotonic()
    p = subprocess.run([sys.executable, '-X', 'utf8', '-B', *argv], cwd=S,
                       env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=240)
    (E/(label+'.log')).write_bytes(p.stdout)
    rec = dict(label=label, argv=argv, rc=p.returncode,
               seconds=round(time.monotonic()-start, 3),
               output_sha256=hashlib.sha256(p.stdout).hexdigest())
    runs.append(rec)
    print(json.dumps(rec), flush=True)
    print(p.stdout.decode('utf8', 'replace')[-1200:], flush=True)
(E/'baseline_results.json').write_text(json.dumps(runs, ensure_ascii=False, indent=2), encoding='utf8')

sys.path.insert(0, str(S/'scripts'))
spec=importlib.util.spec_from_file_location('review_np', S/'scripts/run_network_194_parallel.py')
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)
hashes=mod.code_hashes()
comp=json.loads((E/'compare.json').read_text(encoding='utf8'))
changed={f['filename'] for f in comp['files']}
record=dict(code_fp=mod.code_fp(hashes), code_files=len(mod.CODE_FILES),
            handover_files=len(mod.HANDOVER_FILES),
            numerical_changed=sorted(changed.intersection(mod.CODE_FILES)),
            handover_changed=sorted(changed.intersection(mod.HANDOVER_FILES)),
            hashes=hashes)
manifest=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
bad=[]
for f in manifest['files']:
    path=S/f['path']
    if os.name=='nt': path=Path('\\\\?\\'+str(path))
    b=path.read_bytes()
    if hashlib.sha256(b).hexdigest()!=f['sha256']:
        bad.append(f['path'])
record['snapshot_files_checked']=len(manifest['files'])
record['snapshot_modified']=bad
assert record['code_fp']=='e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71'
assert not record['numerical_changed'] and not record['handover_changed'] and not bad
(E/'source_integrity.json').write_text(json.dumps(record, indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in record.items() if k!='hashes'}),flush=True)
