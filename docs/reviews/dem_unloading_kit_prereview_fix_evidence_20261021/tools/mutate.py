#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mutation run (ULPR-01..04 fix) — one changed line at a time on a mirror copy; the targeted new tests must fail for that reason.
python3 -I -B mutate.py <mirror root> <work dir> <out JSON> [names ...]
Per mutation: copy mirror → replace text (must occur exactly once) → recompute that file's SHA256SUMS line → run the listed selftests →
failing check names (✗ lines) vs expected prefixes (must_fail) and controls (must_pass)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

SRC, WORK, OUT = (os.path.abspath(x) for x in sys.argv[1:4])
ONLY = sys.argv[4:]
KREL = os.path.join('docs', 'data', 'ps45_unload_20261009')

R33a = 'R33 ULPR-02 승인된 RESUME 바로 뒤에 러너 resume_from 밖'
R33b = 'R33 ULPR-02 승인된 RESUME 바로 뒤에 k 숫자 아닌'
R33c = 'R33 ULPR-02 상태 파일 ul_k 0'
R33d = 'R33 ULPR-02 사건 되감기'
R36a = 'R36 ULPR-02 그 런 kit 사본 판독기'
R36b = 'R36 ULPR-02 재판독 프로세스 rc'
A_MOVE = 'R37 ULPR-01 옛 시도 = 단 k 4 창 넷 · 단 줄 · RM 사건 뒤 요약 전 끊김 → RESUME (k 3 · s_r) → 새 시도가 단 k 4 로 이동 중'
A_SAME = 'R37 ULPR-01 옛 시도 = 단 k 4 창 넷 · 단 줄 · RM 사건 뒤 요약 전 끊김 → RESUME (k 3 · s_r) → 새 시도가 옛 시도와 같은 창 수'
A_TWO = 'R37 ULPR-01 옛 시도 = 단 k 4 창 넷 · 단 줄 · RM 사건 뒤 요약 전 끊김 → RESUME (k 3 · s_r) → 새 시도가 단 k 4 창 둘 뒤 TIMEOUT'
B_TWO = 'R37 ULPR-01 교차 전 단 — 옛 시도 = 단 k 3 창 넷 · 단 줄 (사건 없는 단) 뒤 끊김 → RESUME (k 2) → 새 시도 창 둘'
B_SAME = 'R37 ULPR-01 교차 전 단 — 옛 시도 = 단 k 3 창 넷 · 단 줄 (사건 없는 단) 뒤 끊김 → RESUME (k 2) → 새 시도 옛 시도와 같은 창 넷'
B_ZERO = 'R37 ULPR-01 교차 전 단 — 옛 시도 = 단 k 3 창 넷 · 단 줄 (사건 없는 단) 뒤 끊김 → RESUME (k 2) → 새 시도 이동 중 끝'
UNDET = 'R37 시도 미확정'
CONTRA = 'R37 ULPR-01 모순'
CONSIST = 'R37 ULPR-01 경계 뒤 단 줄 ↔ 그 단 창 기록'
CORRUPT = 'R37 ULPR-01 옛 단 줄 (n_windows 4)'
POS_STATE = 'R37 양성 대조: 사건 없는 단'
POS_RM = 'R37 양성 대조: 옛 시도 = 단 k 4 창 넷 (단 줄 전'
POS_LATER = 'R37 양성 대조: 새 시도 증거 = 경계 뒤 단 k 3 창'
POS_ALL = ('R37 대조', 'R37 양성 대조', 'R28 양성 대조', 'R33 대조', 'R34 대조', 'R34 ULKRF-02 같은 길이', 'R10 ')

M = [
    # (name, file, old text, new text, selftests, must_fail prefixes, must_pass prefixes)
    ('ULPR02_out_of_rf_reason_removed', 'ul_reader.py',
     "            pr.append(f'ul_events.csv: RESUME (k {e[\"k\"]} · step {e[\"step\"]}) 의 step ∉ 러너 resume_from {sorted(rf)} — 상충 · 승인 없음 (ULKRF-01)')",
     "            pass", ['ul_reader'], [R33a], ['R33 대조']),
    ('ULPR02_nonnumeric_reason_removed', 'ul_reader.py',
     "            pr.append(f'ul_events.csv: RESUME 사건 k · step 숫자 아님 ({e[\"k\"]} · {e[\"step\"]}) — 승인 없음 (ULKRF-01)')",
     "            pass", ['ul_reader'], [R33b], ['R33 대조']),
    ('ULPR02_state_mismatch_reason_removed', 'ul_reader.py',
     "            pr.append(f'RESUME (k {ks[0]} · step {s}) ≠ 상태 파일 state_unload_{s}.in",
     "            0 and pr.append(f'RESUME (k {ks[0]} · step {s}) ≠ 상태 파일 state_unload_{s}.in", ['ul_reader'], [R33c], ['R33 대조']),
    ('ULPR02_rewind_k_condition_removed', 'ul_reader.py',
     " and all(x['k'] is not None and x['k'] > e['k'] for x in stale):",
     ":", ['ul_reader'], [R33d], ['R33 대조']),
    ('ULPR02_kit_sums_reader_line_check_removed', 'ul_reader.py',
     "        elif listed is None or listed.get(n) != h:",
     "        elif False:", ['ul_reader'], [R36a], ['R36 Q3 양성']),
    ('ULPR02_reread_rc_check_removed', 'ul_reader.py',
     " or ec != 0 or p.returncode != 0:",
     " or ec != 0:", ['ul_reader'], [R36b], ['R36 Q3 양성']),
    ('ULPR01_no_evidence_drop_off', 'ul_reader.py',
     "        if not any(ev.values()):",
     "        if False:", ['ul_reader'], [A_MOVE, B_ZERO, UNDET], POS_ALL),
    ('ULPR01_old_holdend_proof_off', 'ul_reader.py',
     "                    old_pf = any(e['event'] in HOLD_END_EVENTS and (e['k'], e['step']) == key for e in old_ev)",
     "                    old_pf = False", ['ul_reader'], [CORRUPT], POS_ALL),
    ('ULPR01_ambiguous_line_kept', 'ul_reader.py',
     "                    elif not new_pf and m_old and m_new:",
     "                    elif False:", ['ul_reader'], [B_SAME], POS_ALL),
    ('ULPR01_old_windows_only_drop_off', 'ul_reader.py',
     "                    elif not new_pf and m_old and not m_new:",
     "                    elif False:", ['ul_reader'], [B_TWO], POS_ALL),
    ('ULPR01_consistency_check_off', 'ul_reader.py',
     "            if not _windows_match(L, wins):",
     "            if False:", ['ul_reader'], [CONSIST], POS_ALL),
    ('ULPR01_state_file_evidence_off', 'ul_reader.py',
     "        states = _state_steps_after(d, sr)",
     "        states = set()", ['ul_reader'], [POS_STATE], ('R37 대조', 'R28 양성 대조', 'R33 대조')),
    ('ULPR01_new_holdend_proof_off', 'ul_reader.py',
     "                    new_pf = L.get('step') in states or any(e['event'] in HOLD_END_EVENTS and (e['k'], e['step']) == key for e in new_ev)",
     "                    new_pf = L.get('step') in states", ['ul_reader'], [POS_RM], ('R37 대조', 'R28 양성 대조', 'R33 대조')),
    ('ULPR01_later_stage_evidence_off', 'ul_reader.py',
     "        later = any(x.get('k') is not None and x['k'] > k1 for x in tw + ts)",
     "        later = False", ['ul_reader'], [POS_LATER], ('R37 대조', 'R28 양성 대조', 'R33 대조')),
    ('ULPR01_contradiction_off', 'ul_reader.py',
     "            if old_ev and not w_old.get(b):",
     "            if False:", ['ul_reader'], [CONTRA], POS_ALL),
    ('ULPR01_whole_tail_pass_off', 'ul_reader.py',
     "    if auth:   # ULPR-01",
     "    if False:   # ULPR-01", ['ul_reader'], [A_TWO, A_MOVE, B_TWO, UNDET, CONTRA, CONSIST], ('R37 대조', 'R28 양성 대조', 'R33 대조', 'R34 대조')),
    ('ULPR03_g2_dup_check_off', 'ul_gates.py',
     "        if ids is not None and len(set(ids)) != len(ids):",
     "        if False:", ['ul_gates', 'ul_reader'], ['C5 ULPR-03 G2 시험 덤프에 같은 ID', 'R35 ULPR-03 복원', 'R16 ULPR-03 중력 팔 R_M 원자 덤프에 같은 ID'],
     ('C5 ULPR-03 대조', 'R14 복원 판정 조립')),
    ('ULPR03_g2_requested_step_off', 'ul_gates.py',
     "    if step is not None and d['step'] != step:",
     "    if False:", ['ul_gates', 'ul_reader'], ['C5 ULPR-03 G2 요청 step', 'R16 ULPR-03 중력 팔 R_M 원자 덤프 두 개'], ('C5 ULPR-03 대조',)),
    ('ULPR03_g2_pair_step_off', 'ul_gates.py',
     "    if not out['why'] and sa != sb:",
     "    if False:", ['ul_gates'], ['C5 ULPR-03 G2 시험 덤프 머리 TIMESTEP'], ('C5 ULPR-03 대조',)),
    ('ULPR03_g2_empty_both_off', 'ul_gates.py',
     "    if not out['why'] and not a and not b:",
     "    if False:", ['ul_gates'], ['C5 ULPR-03 같은 부류 — 비교 열에 NaN'], ('C5 ULPR-03 대조',)),
    ('ULPR03_g2c_pair_step_off', 'ul_gates.py',
     "    hs = [f'머리 step 시험 {dt[\"step\"]} ≠ 원 {do[\"step\"]}'] if dt['step'] != do['step'] else []",
     "    hs = []", ['ul_gates'], ['C5 ULPR-03 같은 부류 — G2c 시험 쌍 덤프 머리 step'], ('C5 ULPR-03 대조',)),
    ('ULPR04_g2c_observation_loss_as_FAIL', 'ul_gates.py',
     "    out = {'status': 'NOT_COMPUTED', 'why': []}\n    dt, T, dupt, ct = _contacts(test_contact_path, box)",
     "    out = {'status': 'FAIL', 'why': []}\n    dt, T, dupt, ct = _contacts(test_contact_path, box)", ['ul_gates', 'ul_reader'],
     ['C4 ULKRF-03 G2c 시험 쪽', 'C4 ULKRF-03 G2c 원 쪽', 'C3 ULKRR-04 G2c', 'R35 ULKRF-03 · ULPR-04 복원', 'R35 ULKRF-03 · ULPR-04 실제 restore CLI'],
     ('C4 ULPR-04 대조', 'R35 ULPR-04 대조')),
    ('ULPR04_g2_observation_loss_as_FAIL', 'ul_gates.py',
     "    out = {'status': 'NOT_COMPUTED', 'why': []}\n    try:\n        a, sa, pa = _dump_tokens(",
     "    out = {'status': 'FAIL', 'why': []}\n    try:\n        a, sa, pa = _dump_tokens(", ['ul_gates', 'ul_reader'],
     ['C3 ULKRR-04 G2 원자 ID', 'C5 ULPR-03 G2 시험 덤프에 같은 ID', 'R35 ULPR-03 복원'], ('C5 ULPR-03 대조',)),
    ('ULPR03_reader_restore_step_arg_off', 'ul_reader.py',
     "ul_gates.g2_compare(g2a, orig_atom, step=s0)",
     "ul_gates.g2_compare(g2a, orig_atom)", ['ul_reader'], ['R35 ULPR-03 복원: R/g2 · 원 in/ 원자 덤프 머리 step 둘 다'], ('R35 ULPR-04 대조',)),
    ('ULPR03_reader_gravity_step_arg_off', 'ul_reader.py',
     "os.path.join(src, 'dump', f'atom_{rm}.dump'), step=rm)",
     "os.path.join(src, 'dump', f'atom_{rm}.dump'))", ['ul_reader'], ['R16 ULPR-03 중력 팔 R_M 원자 덤프 두 개'], ('R16 중력 팔 복원',)),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def reseal(kit, rel):
    sp = os.path.join(kit, 'SHA256SUMS')
    out = []
    for ln in open(sp, encoding='utf-8').read().splitlines():
        w = ln.split(None, 1)
        out.append(f'{sha(os.path.join(kit, rel))}  {rel}' if len(w) == 2 and w[1].strip() == rel else ln)
    open(sp, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')


res = {}
os.makedirs(WORK, exist_ok=True)
for name, rel, old, new, tests, must_fail, must_pass in M:
    if ONLY and name not in ONLY:
        continue
    root = os.path.join(WORK, name)
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(SRC, root)
    kit = os.path.join(root, KREL)
    p = os.path.join(kit, rel)
    txt = open(p, encoding='utf-8').read()
    n = txt.count(old)
    r = res[name] = {'file': rel, 'occurrences': n, 'tests': {}}
    if n != 1:
        r['error'] = f'old text occurs {n} times (must be exactly once)'
        print(name, r['error'])
        shutil.rmtree(root, ignore_errors=True)
        continue
    open(p, 'w', encoding='utf-8', newline='\n').write(txt.replace(old, new, 1))
    reseal(kit, rel)
    env = dict(os.environ, TMPDIR=os.path.join(WORK, 'tmp'), OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    os.makedirs(env['TMPDIR'], exist_ok=True)
    for t in tests:
        q = subprocess.run([sys.executable, '-I', '-B', os.path.join(kit, f'{t}.py'), '--selftest'], capture_output=True, text=True, timeout=1800, env=env,
                           cwd=root)
        fails = [ln.strip()[2:].strip() for ln in q.stdout.splitlines() if ln.strip().startswith('✗')]
        oks = [ln.strip()[2:].strip() for ln in q.stdout.splitlines() if ln.strip().startswith('✓')]
        r['tests'][t] = {'rc': q.returncode, 'n_ok': len(oks), 'n_fail': len(fails), 'fails': [f[:160] for f in fails],
                         'last': q.stdout.strip().splitlines()[-1:]}
    allf = [f for t in r['tests'].values() for f in t['fails']]
    r['must_fail_hit'] = {mf: any(f.startswith(mf) for f in allf) for mf in must_fail}
    r['must_pass_ok'] = {mp: not any(f.startswith(mp) for f in allf) for mp in must_pass}
    r['killed'] = bool(allf)
    r['as_expected'] = all(r['must_fail_hit'].values()) and all(r['must_pass_ok'].values()) and (r['killed'] or not must_fail)
    print(name, 'killed' if r['killed'] else 'SURVIVED', {t: (v['n_ok'], v['n_fail']) for t, v in r['tests'].items()},
          'must_fail_hit', all(r['must_fail_hit'].values()), 'must_pass_ok', all(r['must_pass_ok'].values()), flush=True)
    shutil.rmtree(root, ignore_errors=True)
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done', len(res), 'mutations ·', sum(1 for v in res.values() if v.get('killed')), 'killed ·',
      sum(1 for v in res.values() if v.get('as_expected')), 'as expected')
