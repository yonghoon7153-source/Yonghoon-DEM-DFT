#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""U2 추가 변이 (고친 사람의 25 개 밖) — 한 줄씩 · 거울 사본 · 그 파일 봉인 줄만 다시 계산 · 자체시험 실패 줄 기록.
python3 -I -B u2_mutate.py <거울 root> <작업 폴더> <출력 JSON> [이름 …]"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

SRC, WORK, OUT = (os.path.abspath(x) for x in sys.argv[1:4])
ONLY = sys.argv[4:]
KREL = os.path.join('docs', 'data', 'ps45_unload_20261009')

M = [
    # (이름, 파일, 옛 글, 새 글, 자체시험)
    ('U_windows_match_no_last_step', 'ul_reader.py',
     "    return (bool(wins) and isinstance(n, int) and n >= 1 and [x.get('w') for x in wins] == list(range(1, n + 1))\n"
     "            and wins[-1].get('step') is not None and wins[-1]['step'] == line.get('step'))",
     "    return (bool(wins) and isinstance(n, int) and n >= 1 and [x.get('w') for x in wins] == list(range(1, n + 1)))", ['ul_reader']),
    ('U_windows_match_count_only', 'ul_reader.py',
     "[x.get('w') for x in wins] == list(range(1, n + 1))", "len(wins) == n", ['ul_reader']),
    ('U_state_files_include_boundary', 'ul_reader.py',
     "if m and int(m.group(1)) > sr and _state_vars", "if m and int(m.group(1)) >= sr and _state_vars", ['ul_reader']),
    ('U_state_files_no_rstep_check', 'ul_reader.py',
     "if m and int(m.group(1)) > sr and _state_vars(os.path.join(rd, nm)).get('ul_rstep') == int(m.group(1)):",
     "if m and int(m.group(1)) > sr:", ['ul_reader']),
    ('U_new_ev_ge_sr', 'ul_reader.py',
     "if e['step'] is not None and e['step'] > sr]", "if e['step'] is not None and e['step'] >= sr]", ['ul_reader']),
    ('U_summary_evidence_off', 'ul_reader.py',
     "    summ = os.path.exists(os.path.join(d, 'ul_summary.txt'))", "    summ = False", ['ul_reader']),
    ('U_events_evidence_off', 'ul_reader.py',
     "'events_after_resume': bool(new_ev),", "'events_after_resume': False,", ['ul_reader']),
    ('U_steps_rollback_evidence_off', 'ul_reader.py',
     "'steps_rollback': bool(s_old.get(b)),", "'steps_rollback': False,", ['ul_reader']),
    ('U_windows_rollback_evidence_off', 'ul_reader.py',
     "ev = {'windows_rollback': bool(w_old.get(b)),", "ev = {'windows_rollback': False,", ['ul_reader']),
    ('U_no_evidence_other_k_check_off', 'ul_reader.py',
     "            if other:\n", "            if False:\n", ['ul_reader']),
    ('U_holdend_drop_CROSS', 'ul_reader.py',
     "HOLD_END_EVENTS = frozenset({'HOLD0_DONE', 'MODE_B', 'CROSS', 'RM',", "HOLD_END_EVENTS = frozenset({'HOLD0_DONE', 'MODE_B', 'RM',", ['ul_reader']),
    ('U_holdend_add_GUARD', 'ul_reader.py',
     "'NO_BRACKET', 'TECH', 'LIFT_CAP'})", "'NO_BRACKET', 'TECH', 'LIFT_CAP', 'GUARD', 'SEPARATED'})", ['ul_reader']),
    ('U_why_line_not_dropped', 'ul_reader.py',
     "                        steps = drop(steps, [L])\n", "                        pass\n", ['ul_reader']),
    ('U_supersede_by_not_recorded', 'ul_reader.py',
     "                    by[(kr, sr)] = list(stale)\n", "                    pass\n", ['ul_reader']),
    ('U_ev_old_not_recorded', 'ul_reader.py',
     "                ev_old[b] = stale   # ULPR-01", "                pass   # ULPR-01", ['ul_reader']),
    ('U_g2c_requested_step_off', 'ul_gates.py',
     "    hs += [f'머리 step {n} {s} ≠ 요청 {step}' for n, s in (('시험', dt['step']), ('원', do['step'])) if step is not None and s != step]\n",
     "    pass\n", ['ul_gates', 'ul_reader']),
    ('U_restore_g2c_step_arg_off', 'ul_reader.py',
     "ul_gates.g2c_compare(g2c, orig_con, step=s0)", "ul_gates.g2c_compare(g2c, orig_con)", ['ul_reader']),
    ('U_gravity_g2c_step_arg_off', 'ul_reader.py',
     "os.path.join(src, 'dump', f'contact_{rm}.dump'), step=rm)", "os.path.join(src, 'dump', f'contact_{rm}.dump'))", ['ul_reader']),
    ('U_g2_ignore_read_dump_problems', 'ul_gates.py',
     "    pr = list(d['problems'])\n    if d['cols'] is not None and [c for c in cols if c not in d['cols']]:",
     "    pr = []\n    if d['cols'] is not None and [c for c in cols if c not in d['cols']]:", ['ul_gates', 'ul_reader']),
    ('U_g2c_only_test_side_ok', 'ul_gates.py',
     "    if not (dt['ok'] and do['ok']):", "    if not dt['ok']:", ['ul_gates', 'ul_reader']),
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
for name, rel, old, new, tests in M:
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
        print(name, r['error'], flush=True)
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
        r['tests'][t] = {'rc': q.returncode, 'n_ok': len(oks), 'n_fail': len(fails), 'fails': [f[:200] for f in fails],
                         'last': q.stdout.strip().splitlines()[-1:], 'stderr_tail': q.stderr.strip().splitlines()[-2:]}
    r['killed'] = any(v['n_fail'] or v['rc'] for v in r['tests'].values())
    print(name, 'killed' if r['killed'] else 'SURVIVED', {t: (v['n_ok'], v['n_fail'], v['rc']) for t, v in r['tests'].items()}, flush=True)
    shutil.rmtree(root, ignore_errors=True)
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done', len(res), 'mutations ·', sum(1 for v in res.values() if v.get('killed')), 'killed ·',
      sum(1 for v in res.values() if 'error' in v), 'errors')
