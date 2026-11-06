#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""변이 확인 2 단계 (2026-11-06 · `SELF-155` 고침) — PMUT 탐침 밖에서 대조 묶음 전체가 변이를 잡는가.

변이마다: scripts/carbon_junction.py 를 변이 사본으로 잠시 바꾸고 (대상 문자열 = 정확히 한 번) → `test_carbon_junction.py --only
PSRCH,PEQ,PREG,PS0,PTIE,PMEM,PEDGE,CP-ORD` 와 `test_ca_s0_census.py` 를 돌려 실패 검사 이름을 모은다 → 원본 바이트를 되돌리고 sha256 을 확인한다
(finally · 되돌림 실패 = 이 도구 실패).  PMUT 묶음은 뺀다 (지금 소스에서 변이를 만들므로 변이된 소스에서는 대상 문자열이 없다).

  python3 docs/reviews/rint2_s0_mem_fix_20261106/tools/mutation_full.py <로그 폴더>
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
TARGET = os.path.join(ROOT, 'scripts', 'carbon_junction.py')
MUTANTS = (
    ('M1_radius_D_only', '반지름 = D 만 (조각 길이 항 없음)', 'r = (2.0 * float(hs.max()) + float(D))', 'r = (0.0 * float(hs.max()) + float(D))'),
    ('M2_half_len_half', '조각 반 길이 반', 'hs = 0.5 * sl[par] / nsub[par]', 'hs = 0.25 * sl[par] / nsub[par]'),
    ('M3_mid_at_start', '조각 중점 → 조각 시작점', 'u = (kk + 0.5) / nsub[par]', 'u = kk / nsub[par]'),
    ('M4_drop_last_chunk', '판정 마지막 덩어리 버림', 'for c0 in range(0, len(pr), ch):', 'for c0 in range(0, (len(pr) // ch) * ch, ch):'),
    ('M5_no_tie_keys', '동률 키 뺌 (옛 순서)', "o = np.lexsort((np.array(out['sj_min'], np.int64), np.array(out['si_min'], np.int64), ",
     'o = np.lexsort(('),
    ('M6_no_margin', '반올림 여유 0 (경계 칼날)', 'r = (2.0 * float(hs.max()) + float(D)) * (1.0 + 1.0e-9) + 1.0e-12 * (1.0 + span)',
     'r = (2.0 * float(hs.max()) + float(D)) * 1.0'),
    ('M7_ball_no_half', '점 ↔ 선분 후보 반지름에서 조각 반 길이 항 뺌 (S0 쪽)', 'r = (rq + float(hs.max()))', 'r = (rq + 0.0 * float(hs.max()))'),
)
SUITES = (('carbon_junction', ['scripts/test_carbon_junction.py', '--only', 'PSRCH,PEQ,PREG,PS0,PTIE,PMEM,PEDGE,CP-ORD']),
          ('ca_s0_census', ['scripts/test_ca_s0_census.py']))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    orig = open(TARGET, 'rb').read()
    orig_sha = sha(orig)
    src = orig.decode('utf-8')
    summary = {'target_sha256_before': orig_sha, 'mutants': []}
    try:
        for tag, nm, old, new in MUTANTS:
            rec = {'tag': tag, 'name': nm, 'target_count': src.count(old)}
            if src.count(old) != 1:
                rec['status'] = 'target string not found exactly once'
                summary['mutants'].append(rec)
                continue
            with open(TARGET, 'wb') as fh:
                fh.write(src.replace(old, new).encode('utf-8'))
            rec['mutant_sha256'] = sha(open(TARGET, 'rb').read())
            for sname, argv in SUITES:
                p = subprocess.run([sys.executable] + argv, cwd=ROOT, capture_output=True, text=True)
                log = os.path.join(out, f'{tag}__{sname}.log')
                with open(log, 'w', encoding='utf-8') as fh:
                    fh.write(p.stdout + p.stderr)
                fails = [ln.strip()[6:][:150] for ln in p.stdout.splitlines() if ln.strip().startswith('FAIL ')]
                last = [ln for ln in p.stdout.splitlines() if 'PASS' in ln and ('==' in ln or '·' in ln)][-1:] or ['']
                rec[sname] = {'rc': p.returncode, 'n_fail_lines': len(fails), 'fails': fails[:12], 'summary': last[0][:160]}
            rec['caught'] = any(rec[s]['rc'] != 0 for s, _ in SUITES)
            summary['mutants'].append(rec)
            print(f"{tag}: 잡힘 {rec['caught']} · carbon_junction rc {rec['carbon_junction']['rc']} 실패 {rec['carbon_junction']['n_fail_lines']} "
                  f"· ca_s0_census rc {rec['ca_s0_census']['rc']} 실패 {rec['ca_s0_census']['n_fail_lines']}", flush=True)
    finally:
        with open(TARGET, 'wb') as fh:
            fh.write(orig)
        after = sha(open(TARGET, 'rb').read())
        summary['target_sha256_after'] = after
        summary['restored'] = after == orig_sha
        with open(os.path.join(out, 'mutation_full.json'), 'w', encoding='utf-8') as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=1)
        print(f"원본 되돌림 {summary['restored']} · sha256 {after}")
    return 0 if summary['restored'] else 2


if __name__ == '__main__':
    sys.exit(main())
