"""Read-only review: validate and unpack supplied evidence, rerun pinned reader."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'source/docs/data/ps45_unload_20261009'
SRC = ROOT / 'source/docs/reviews/dem_unloading_history_test_20261014'
DEST = ROOT / 'evidence/history_actual'
archive = SRC / 'hist_20261014_094731.report.tgz'
report = {'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
          'slurm_sha256': hashlib.sha256((SRC / 'ulHist_283122.out').read_bytes()).hexdigest()}
with tarfile.open(archive, 'r:gz') as tf:
    members = tf.getmembers()
    problems = []
    seen = set()
    for m in members:
        p = PurePosixPath(m.name)
        if p.is_absolute() or '..' in p.parts or '\\' in m.name or ':' in m.name or not (m.isfile() or m.isdir()):
            problems.append({'path': m.name, 'type': str(m.type)})
        if m.name.casefold() in seen:
            problems.append({'duplicate': m.name})
        seen.add(m.name.casefold())
    report['archive_members'] = len(members)
    report['archive_file_count'] = sum(m.isfile() for m in members)
    report['archive_unpacked_bytes'] = sum(m.size for m in members)
    report['unsafe_members'] = problems
    assert not problems, problems
    # Python's data filter realpath(strict=ALLOW_MISSING) is rejected by this
    # Windows sandbox. Equivalent path/type checks above precede manual data
    # extraction; no archive permissions, links, or device nodes are applied.
    DEST.mkdir(exist_ok=True)
    for m in members:
        target = DEST.joinpath(*PurePosixPath(m.name).parts)
        if m.isdir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                assert hashlib.sha256(target.read_bytes()).digest() == hashlib.sha256(tf.extractfile(m).read()).digest()
            else:
                target.write_bytes(tf.extractfile(m).read())
run = DEST / 'hist_20261014_094731'
cmd = [sys.executable, '-X', 'utf8', '-I', str(KIT / 'history_test/read_history.py'), str(run), '--params',
       str(KIT / 'history_test/history_params.json'), '--out', str(ROOT / 'evidence/history_reread.json')]
p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
(ROOT / 'evidence/history_reread.stdout.txt').write_text(p.stdout, encoding='utf-8')
(ROOT / 'evidence/history_reread.stderr.txt').write_text(p.stderr, encoding='utf-8')
report['reader_rc'] = p.returncode
actual = json.loads((ROOT / 'evidence/history_reread.json').read_text(encoding='utf-8'))
submitted = json.loads((run / 'history_verdict.json').read_text(encoding='utf-8'))
actual.pop('run_dir', None)
submitted.pop('run_dir', None)
report['equal_except_run_dir'] = actual == submitted
report['rows'] = {k: v['status'] for k, v in actual['rows'].items()}
report['info'] = actual['info']
report['manifest'] = (run / 'run_manifest.txt').read_text(encoding='utf-8')
report['sealed_manifest_matches'] = []
for seal in DEST.rglob('SHA256SUMS'):
    report['sealed_manifest_matches'].append({'path': str(seal.relative_to(DEST)),
      'sha256': hashlib.sha256(seal.read_bytes()).hexdigest(),
      'equals_pinned': seal.read_bytes() == (KIT / 'history_test/SHA256SUMS').read_bytes()})
sys.path.insert(0, str(KIT / 'history_test'))
import read_history as H
P = H.load_params(str(KIT / 'history_test/history_params.json'))
report['stage_checks'] = {}
for stage in H.STAGES:
    st = H.load_stage(str(run), stage, P)
    s = st.get('screen', {})
    report['stage_checks'][stage] = {key: st.get(key) for key in ('rc', 'np', 'tech_ok', 'problems')}
    report['stage_checks'][stage].update({key: sorted(s.get(key, [])) if key == 'resets' else s.get(key)
                                         for key in ('banner', 'git', 'loops', 'errors', 'resets')})
    deck_name = (run / stage / 'deck.txt').read_text().strip()
    report['stage_checks'][stage]['deck_equals_pinned'] = (run / stage / deck_name).read_bytes() == (KIT / 'history_test' / deck_name).read_bytes()
    report['stage_checks'][stage]['plate_equals_pinned'] = (run / stage / 'plate_hist.stl').read_bytes() == (KIT / 'history_test/plate_hist.stl').read_bytes()
out = ROOT / 'evidence/history_actual_audit.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k not in ('stage_checks', 'info', 'manifest')}, ensure_ascii=False, indent=2))
