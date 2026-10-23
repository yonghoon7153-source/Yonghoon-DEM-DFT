#!/usr/bin/env python3
"""ULPR-02 six diagnostic/guard mutations; execute each full reader selftest without editing the kit.
Usage: python mutation_check.py --kit docs/data/ps45_unload_20261009 --out /tmp/ulpr-mutations
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

MUTATIONS = {
    'resume_outside_manifest': ("            pr.append(f'ul_events.csv: RESUME (k {e[\"k\"]} · step {e[\"step\"]}) 의 step ∉ 러너 resume_from {sorted(rf)} — 상충 · 승인 없음 (ULKRF-01)')", '            pass'),
    'resume_nonnumeric': ("            pr.append(f'ul_events.csv: RESUME 사건 k · step 숫자 아님 ({e[\"k\"]} · {e[\"step\"]}) — 승인 없음 (ULKRF-01)')", '            pass'),
    'resume_state_mismatch': ("            pr.append(f'RESUME (k {ks[0]} · step {s}) ≠ 상태 파일 state_unload_{s}.in (ul_k {st.get(\"ul_k\")} · ul_rstep {st.get(\"ul_rstep\")}) — '\n                      '상충 · 승인 없음 (ULKRF-01)')", '            pass'),
    'event_rewind_k_guard': (" and all(x['k'] is not None and x['k'] > e['k'] for x in stale)", ''),
    'reader_listed_hash': ('elif listed is None or listed.get(n) != h:', 'elif False:'),
    'reader_process_rc': (' or p.returncode != 0:', ':'),
}
LOADER = """import pathlib,sys
source,kit=sys.argv[1:]
sys.path.insert(0,kit)
p=str(pathlib.Path(kit)/'ul_reader.py')
sys.argv=[p,'--selftest']
exec(compile(pathlib.Path(source).read_text(),p,'exec'), {'__name__':'__main__','__file__':p})
"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kit', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    kit, out = args.kit.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    src = (kit / 'ul_reader.py').read_text()
    records = []
    for name, (old, new) in MUTATIONS.items():
        if src.count(old) != 1:
            raise RuntimeError(f'{name}: expected exactly one mutation site, got {src.count(old)}')
        p = out / (name + '.py')
        p.write_text(src.replace(old, new, 1))
        r = subprocess.run([sys.executable, '-I', '-c', LOADER, str(p), str(kit)], cwd=kit, capture_output=True, text=True)
        log = r.stdout + r.stderr
        (out / (name + '.log')).write_text(log)
        failures = [x.strip() for x in log.splitlines() if '✗' in x]
        rec = {'mutation': name, 'rc': r.returncode, 'killed': r.returncode != 0,
               'failures': failures, 'expected_guard_failure': any('R38 ULPR-02' in x for x in failures),
               'unexpected_failures': [x for x in failures if 'R38 ULPR-02' not in x],
               'mutant_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        records.append(rec)
        print(json.dumps(rec, ensure_ascii=False), flush=True)
    result = {'source_sha256': hashlib.sha256((kit / 'ul_reader.py').read_bytes()).hexdigest(),
              'python': sys.version, 'mutations': records}
    (out / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return 0 if all(x['killed'] and x['expected_guard_failure'] and not x['unexpected_failures'] for x in records) else 1

if __name__ == '__main__':
    raise SystemExit(main())
