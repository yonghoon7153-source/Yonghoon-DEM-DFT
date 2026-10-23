#!/usr/bin/env python3
"""Independently remove three RESUME authorization guards from current reader.

Portable invocation: python -I authorization_mutations.py --repo REPO --out OUT
No repository file is modified. Each isolated mutant runs the reader selftest.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

SPECS = [
    ('resume_outside_manifest_condition', "elif e['step'] not in rf:", 'elif False:'),
    ('resume_nonnumeric_condition', "if e['k'] is None or e['step'] is None:", 'if False:'),
    ('resume_state_match_condition', "if st.get('ul_rstep') == s and st.get('ul_k') == ks[0]:", 'if True:'),
]
LOADER = """import pathlib,sys
source,kit=sys.argv[1:]
sys.path.insert(0,kit)
p=str(pathlib.Path(kit)/'ul_reader.py')
sys.argv=[p,'--selftest']
exec(compile(pathlib.Path(source).read_text(),p,'exec'), {'__name__':'__main__','__file__':p})
"""

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    kit = a.repo.resolve() / 'docs/data/ps45_unload_20261009'
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    source = kit / 'ul_reader.py'
    src = source.read_text()
    results = []
    for name, old, new in SPECS:
        if src.count(old) != 1:
            raise RuntimeError((name, src.count(old)))
        path = out / (name + '.py')
        path.write_text(src.replace(old, new, 1))
        r = subprocess.run([sys.executable, '-I', '-c', LOADER, str(path), str(kit)],
                           cwd=kit, capture_output=True, text=True)
        log = r.stdout + r.stderr
        (out / (name + '.log')).write_text(log)
        failures = [line.strip() for line in log.splitlines() if '✗' in line]
        expected = [line for line in failures if 'R38 ULPR-02' in line]
        related = [line for line in failures if name == 'resume_state_match_condition'
                   and re.search(r'R28 ULKRR-02 이어 돌림 꼴인데 상태 파일 (?:ul_k 0 ≠ RESUME 사건 k 1|\(state_unload_<s_r>\.in\) 없음)', line)]
        unexpected = [line for line in failures if line not in expected and line not in related]
        trace = 'Traceback (most recent call last)' in log
        record = dict(name=name, old=old, new=new, rc=r.returncode,
                      mutant_sha256=sha(path), failures=failures,
                      expected_failures=expected, related_existing_R28_failures=related,
                      unexpected_failures=unexpected,
                      traceback=trace,
                      killed_for_expected_reason=(r.returncode == 1 and bool(expected)
                                                  and not unexpected and not trace))
        results.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
    result = dict(source_sha256=sha(source), script_sha256=sha(Path(__file__)),
                  python=sys.version, mutations=results)
    (out / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    return 0 if all(x['killed_for_expected_reason'] for x in results) else 1

if __name__ == '__main__':
    raise SystemExit(main())
