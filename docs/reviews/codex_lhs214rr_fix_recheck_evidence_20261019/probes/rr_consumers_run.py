"""Fresh consumer evidence runner; source snapshots and old evidence are read-only.

chain: original 10-15 probe bytes, with source/evidence/temp paths rebound only.
resurrection: original 10-17 H0 probe bytes, with helper paths rebound; capture
the expected early refusal without changing any old verdict or mutant.
suites: run the two submitted tests unchanged in isolated temporary storage.
baseline: actual old release adapter with unmutated ml_physics source.
"""
from pathlib import Path
import contextlib
import hashlib
import json
import os
import subprocess
import sys
import time
import traceback
import types

REVIEW = Path(__file__).resolve().parents[1]
WS = REVIEW.parent
SOURCE = REVIEW / 'source'
EV = REVIEW / 'evidence/rr_consumers'
TMP = REVIEW / 'tmp/rr_consumers'
OLD = WS / 'lhs214r_fix_recheck_20261017/probes'
EV.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
deps = [WS / 'lhs_coverage_review_20260930/deps', WS / 'gen2_network_reverify3_20261007/deps']
sys.path[:0] = list(map(str, deps)) + [str(SOURCE / 'scripts'), str(SOURCE / 'webapp')]
os.environ.update(PYTHONPATH=os.pathsep.join(map(str, deps)), PYTHONUTF8='1',
                  PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1', TMP=str(TMP), TEMP=str(TMP))
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'

def save(name, obj):
    (EV / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding='utf-8')

def payload(path):
    raw = path.read_bytes()
    return raw.decode('utf-8'), {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def replace_one(code, before, after, changes):
    assert code.count(before) == 1, before
    changes.append({'before': before, 'after': after})
    return code.replace(before, after)

def helper():
    code, provenance = payload(OLD / 'consumer_adversarial.py')
    changes = []
    code = replace_one(code, "EV = REVIEW / 'evidence'", "EV = REVIEW / 'evidence/rr_consumers'", changes)
    code = replace_one(code, "str(REVIEW / 'tmp')", "str(REVIEW / 'tmp/rr_consumers')", changes)
    module = types.ModuleType('consumer_adversarial')
    module.__file__ = str(REVIEW / 'probes/rr_consumers_adversarial_path_binding.py')
    exec(compile(code, str(OLD / 'consumer_adversarial.py'), 'exec'), module.__dict__)
    sys.modules['consumer_adversarial'] = module
    return module, dict(provenance, changes=changes, rebound_file=module.__file__)

def main():
    mode = sys.argv[1]
    if mode == 'suites':
        summary = []
        for name in ('test_l214r_r01_restored_full.py', 'test_l214r_r04_cf_label.py'):
            path = SOURCE / 'scripts' / name
            began = time.monotonic()
            proc = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(path)], cwd=SOURCE, capture_output=True)
            out, err = [v.decode('utf-8', errors='backslashreplace') for v in (proc.stdout, proc.stderr)]
            (EV / (name + '.log')).write_text(out + '\nSTDERR\n' + err, encoding='utf-8')
            result = dict(test=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(), rc=proc.returncode,
                          seconds=time.monotonic()-began, tail=out.splitlines()[-12:], stderr=err.splitlines()[-8:])
            summary.append(result)
            save('submitted_suites.json', summary)
            print(json.dumps(result, ensure_ascii=False), flush=True)
        return
    if mode == 'chain':
        path = WS / 'lhs214_fix_reverify_20261015/probes/l214_consumers.py'
        code, prov = payload(path)
        assert prov['sha256'] == '804de03d58902862f74006afaf1e24dfed97a42a254d02b86a4cc98797de243a'
        changes = []
        code = replace_one(code, "EVIDENCE = REVIEW / 'evidence'", "EVIDENCE = REVIEW / 'evidence/rr_consumers'", changes)
        code = replace_one(code, "SCRATCH = EVIDENCE / 'consumers_temp'", "SCRATCH = REVIEW / 'tmp/rr_consumers'", changes)
        scope = {'__file__': str(__file__), '__name__': '__main__'}
        save('chain_provenance.json', dict(prov, changes=changes, rebound_file=str(__file__)))
        with (EV / 'chain_stdout.log').open('w', encoding='utf-8') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            exec(compile(code, str(path), 'exec'), scope)
        print('Fresh original-chain probe completed.', flush=True)
        return
    C, prov = helper()
    if mode == 'baseline':
        report = {'scope': 'Fresh actual build/check baseline using unchanged old adapter; selected genuine ml_physics source; other rows synthetic.', 'helper_provenance': prov}
        with (EV / 'baseline_stdout.log').open('w', encoding='utf-8') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            C.release_probe(report, target_name='ml_physics', minimal=True)
        save('baseline.json', report)
        print(json.dumps({k:report.get(k) for k in ('release_baseline', 'release_baseline_check', 'selected')}, ensure_ascii=False, default=str), flush=True)
        return
    assert mode == 'resurrection'
    path = OLD / 'consumer_h0_resurrection.py'
    code, original = payload(path)
    scope = {'__file__': str(REVIEW / 'probes/rr_consumers_h0_path_binding.py'), '__name__': '__main__'}
    error = None
    try:
        exec(compile(code, str(path), 'exec'), scope)
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    report = scope.get('report', {})
    report.update(original_probe=original, helper_provenance=prov, caught_exception=error)
    cid = C.load(EV / 'consumers_probe.json')['handover']['cases']['ml_hertz']['case_id']
    cd = C.ROOT / 'batch/merged/lhs/results' / cid
    report['independent_after_refusal_reread'] = C.call(C.RR.reread_case, cd, 'g2', C.ps, C.tf)
    report['release_output_exists'] = (C.ROOT / 'output').exists()
    save('resurrection_capture.json', report)
    print(json.dumps({'caught_exception': error, 'after': report.get('after'), 'release_output_exists': report['release_output_exists']}, ensure_ascii=False, default=str), flush=True)

if __name__ == '__main__':
    main()
