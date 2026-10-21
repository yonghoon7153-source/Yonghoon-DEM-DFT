#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 리뷰 변이 시험 — 고친 줄을 하나씩 되돌려 (또는 지워) 새 시험이 '옳은 이유로' 실패하는지 본다 (리포에 쓰지 않는다 · 거울 사본에서만).

python3 -I -B mutate.py <거울 루트 (m_pin)> <작업 폴더> <출력 JSON> [변이 이름 …]
변이마다: 거울을 새 폴더로 복사 → 키트 파일 한 곳 글자 바꿈 (정확히 한 번 나와야) → 키트 SHA256SUMS 의 그 줄만 다시 계산 (러너 시험이 봉인 검사에서 엉뚱하게 멈추지 않게) →
지정 자체시험 실행 → 실패한 검사 이름 (✗ 줄) 과 기대 검사 접두를 대조."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

SRC, WORK, OUT = (os.path.abspath(x) for x in sys.argv[1:4])
ONLY = sys.argv[4:]
KREL = os.path.join('docs', 'data', 'ps45_unload_20261009')

M = [
    # (이름, 파일, 옛 글자, 새 글자, 돌릴 시험, 실패해야 할 검사 접두, 실패하면 안 되는 검사 접두 (양성 대조))
    ('ULKRF01_dup_check_removed', 'ul_reader.py',
     "        if len(ks) > 1:\n            pr.append(",
     "        if False:\n            pr.append(",
     ['ul_reader'], ['R33 ULKRF-01 러너 resume_from 한 줄', 'R33 ULKRF-01 같은 RESUME 두 줄', 'R33 ULKRF-01 같은 step'], ['R33 대조']),
    ('ULKRF01_out_of_rf_problem_removed', 'ul_reader.py',
     "            pr.append(f'ul_events.csv: RESUME (k {e[\"k\"]} · step {e[\"step\"]}) 의 step ∉ 러너 resume_from {sorted(rf)} — 상충 · 승인 없음 (ULKRF-01)')",
     "            pass",
     ['ul_reader'], [], []),
    ('ULKRF01_nonnumeric_problem_removed', 'ul_reader.py',
     "            pr.append(f'ul_events.csv: RESUME 사건 k · step 숫자 아님 ({e[\"k\"]} · {e[\"step\"]}) — 승인 없음 (ULKRF-01)')",
     "            pass",
     ['ul_reader'], [], []),
    ('ULKRF01_event_rewind_k_condition_removed', 'ul_reader.py',
     " and all(x['k'] is not None and x['k'] > e['k'] for x in stale):",
     ":",
     ['ul_reader'], [], []),
    ('ULKRF01_state_mismatch_problem_removed', 'ul_reader.py',
     "            pr.append(f'RESUME (k {ks[0]} · step {s}) ≠ 상태 파일 state_unload_{s}.in",
     "            0 and pr.append(f'RESUME (k {ks[0]} · step {s}) ≠ 상태 파일 state_unload_{s}.in",
     ['ul_reader'], [], []),
    ('ULKRF02_kback_off', 'ul_reader.py',
     "        kback = steps_csv and prev is not None",
     "        kback = False and prev is not None",
     ['ul_reader'], ['R34 ULKRF-02 승인된 이어 돌림'], ['R34 대조', 'R34 ULKRF-02 같은 길이', 'R34 ULKRF-02 승인 없는']),
    ('ULKRF02_kback_also_windows', 'ul_reader.py',
     "        kback = steps_csv and prev is not None",
     "        kback = prev is not None",
     ['ul_reader'], [], []),
    ('ULKRF03_early_return_removed', 'ul_gates.py',
     "    if not d['ok']:   # ULKRF-03",
     "    if False:   # ULKRF-03",
     ['ul_gates', 'ul_reader'], ['C4 ULKRF-03', 'R35 ULKRF-03'], []),
    ('Q3_reread_disabled', 'ul_reader.py',
     "    rpr, rec['reread'] = _grammar_reread(rd, kit, listed, ch if isinstance(ch, dict) else {})",
     "    rpr, rec['reread'] = [], {'status': 'PASS', 'reader_sha256': GRAMMAR_READER['read_history.py']}",
     ['ul_reader', 'ul_runner_test'], ['R36 Q3 판정 JSON', 'R36 Q3 그 런 kit', 'M25'], ['R32']),
    ('Q3_listed_check_removed', 'ul_reader.py',
     "        elif listed is None or listed.get(n) != h:",
     "        elif False:",
     ['ul_reader'], [], []),
    ('Q3_rc_check_removed', 'ul_reader.py',
     " or ec != 0 or p.returncode != 0:",
     " or ec != 0:",
     ['ul_reader'], [], []),
    ('Q3_diff_check_removed', 'ul_reader.py',
     "    if diff:\n        pr.append(f'원자료 재판독 검사 ≠ 판정 JSON",
     "    if 0:\n        pr.append(f'원자료 재판독 검사 ≠ 판정 JSON",
     ['ul_reader'], [], []),
    ('Q4_int_token_off', 'ul_lib.py',
     "    if _INT_TOK.fullmatch(tok):\n        return int(tok), None",
     "    if False:\n        return int(tok), None",
     ['ul_lib'], ['L14 Q4 원자 덤프', 'L14 Q4 쌍 덤프'], []),
    ('Q4_decimal_mask_off', 'ul_lib.py',
     "        if exact != decimal.Decimal(int(v)):",
     "        if False:",
     ['ul_lib'], ['L14 Q4 쌍 덤프'], []),
    ('Q4_lf_writer_reverted', 'ul_reader.py',
     "    with open(path, 'w', encoding='utf-8', newline='\\n') as f:\n        f.write(text)",
     "    with open(path, 'w', encoding='utf-8') as f:\n        f.write(text)",
     ['ul_reader'], [], []),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def reseal(kit, rel):
    sp = os.path.join(kit, 'SHA256SUMS')
    L = open(sp, encoding='utf-8').read().splitlines()
    out = []
    for ln in L:
        w = ln.split(None, 1)
        if len(w) == 2 and w[1].strip() == rel:
            out.append(f'{sha(os.path.join(kit, rel))}  {rel}')
        else:
            out.append(ln)
    open(sp, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')


res = {}
os.makedirs(WORK, exist_ok=True)
for name, rel, old, new, tests, must_fail, must_pass in M:
    if ONLY and name not in ONLY:
        continue
    root = os.path.join(WORK, name)
    if os.path.isdir(root):
        shutil.rmtree(root)
    shutil.copytree(SRC, root)
    kit = os.path.join(root, KREL)
    p = os.path.join(kit, rel)
    txt = open(p, encoding='utf-8').read()
    n = txt.count(old)
    r = res[name] = {'file': rel, 'occurrences': n, 'tests': {}}
    if n != 1:
        r['error'] = f'옛 글자 {n} 번 (정확히 한 번이어야)'
        print(name, r['error'])
        continue
    open(p, 'w', encoding='utf-8', newline='\n').write(txt.replace(old, new, 1))
    reseal(kit, rel)
    env = dict(os.environ, TMPDIR=os.path.join(WORK, 'tmp'), OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    os.makedirs(env['TMPDIR'], exist_ok=True)
    for t in tests:
        q = subprocess.run(['nice', '-n', '19', sys.executable, '-I', '-B', os.path.join(kit, f'{t}.py'), '--selftest'], capture_output=True, text=True,
                           timeout=1800, env=env, cwd=root)
        fails = [ln.strip()[2:].strip() for ln in q.stdout.splitlines() if ln.strip().startswith('✗')]
        oks = [ln.strip()[2:].strip() for ln in q.stdout.splitlines() if ln.strip().startswith('✓')]
        r['tests'][t] = {'rc': q.returncode, 'n_ok': len(oks), 'n_fail': len(fails), 'fails': [f[:140] for f in fails], 'last': q.stdout.strip().splitlines()[-1:]}
    allf = [f for t in r['tests'].values() for f in t['fails']]
    r['must_fail_hit'] = {mf: any(f.startswith(mf) for f in allf) for mf in must_fail}
    r['must_pass_ok'] = {mp: not any(f.startswith(mp) for f in allf) for mp in must_pass}
    r['killed'] = bool(allf)
    print(name, 'killed' if r['killed'] else 'SURVIVED', {t: (v['n_ok'], v['n_fail']) for t, v in r['tests'].items()}, r['must_fail_hit'], r['must_pass_ok'])
    shutil.rmtree(root, ignore_errors=True)
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
