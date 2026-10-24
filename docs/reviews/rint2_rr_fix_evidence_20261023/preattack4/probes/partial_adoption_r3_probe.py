#!/usr/bin/env python3
"""Round-4 probe — Q9 design rev 3 (4040e4388) §3-2 부분 채택 · §3-4 ATTEMPT_AFTER_ADOPTED · §3-5 결과 전/뒤 · 재실행, against the
one-machine chain, using the REAL `Predict` (no overflow → current order = rev-2/3 new order, round-3 order_probe S0).

Rules are encoded literally from the rev-3 text (line numbers of `git show 4040e4388:…/q9_predict_units_design.md`):
  L119  결과 전 = 시도 폴더에 payload 없음 AND 러너 멈춤 기록의 원인 ∈ {풀기 전 거부, 자식 신호 9, CUDA OOM}
  L123  재실행 = 자원 · 인프라 멈춤 (신호 9 · CUDA OOM · 러너 기록 없음) 이 '첫 payload 뒤에 나면' · 같은 기계 · 환경 · 멈춘 런부터
  L128  '러너 멈춤 기록이 없는 시도의 처분' = 같은 기계 · 환경 = 재실행 · 다른 기계 = 결과 뒤
  L129  채택 = 원장 차례로 처음으로 결과 전 멈춤이 아닌 시도 + 그 재실행 사슬
  L105  채택 뒤 같은 단위의 시도 (완주 · 멈춤 무관) = 멈춤 ATTEMPT_AFTER_ADOPTED
  L68   부분 채택 — 멈춤은 다시 계산이 그 런을 요청할 때
no-op runs are excluded from the predict run count (rev 3 moves them to the ladder stage) — counts WITH no-op are also printed.
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import rint_r_chain as C  # noqa: E402
sys.path.insert(0, sys.argv[2])
from q9r3_lib import LAD, arm, base_arm0, rr_of, unit_of, RUN_OF_ROLE  # noqa: E402

BEFORE_CAUSES = {'presolve', 'signal9', 'cuda_oom'}
RESOURCE_CAUSES = {'signal9', 'cuda_oom', 'no_record'}


def result_before(att):
    if att.get('rejected'):
        return True                                       # 풀기 전 거부 기록 (L118 · 유일한 폴더 없는 예외)
    payload = att.get('payload', False)
    return (not payload) and att.get('cause') in BEFORE_CAUSES


def resumable(att, reading):
    """L123 (첫 payload 뒤 · 자원 · 인프라) vs L128 (러너 기록 없음 = 같은 기계 · 환경 재실행, 첫 payload 와 무관)."""
    if att.get('cause') not in RESOURCE_CAUSES or result_before(att):
        return False
    if reading == 'L123':
        return bool(att.get('payload'))
    return True                                           # 'L128'


def adopt(atts, resume_reading, aaa_reading):
    """→ ('ok', bundle) | ('stop', code).  bundle = {'stop_at': run# | None, 'code': ...}."""
    first = None
    for i, a in enumerate(atts):
        if a['kind'] == 'unit' and not result_before(a):
            first = i
            break
    if first is None:
        return 'missing', None
    base = atts[first]
    eff = {'stop_at': base.get('stop_at'), 'code': base.get('code')}
    chain_idx = {first}
    cur = base
    for j in range(first + 1, len(atts)):
        a = atts[j]
        if a['kind'] == 'resume' and a.get('of') == first:
            in_chain = (not a.get('rejected')) or aaa_reading == 'B'      # B = 거부된 재실행 항목도 사슬의 일부
            if not in_chain:
                continue
            chain_idx.add(j)
            if a.get('rejected'):
                continue
            if not resumable(cur, resume_reading):
                return 'stop', 'RESUME_NOT_ALLOWED(이름 없음)'
            eff = {'stop_at': a.get('stop_at'), 'code': a.get('code')}
            cur = a
    for j in range(first + 1, len(atts)):
        if j not in chain_idx:
            return 'stop', 'ATTEMPT_AFTER_ADOPTED'
    return 'ok', eff        # eff['stop_at'] = None (완주) 또는 남은 멈춤 (재실행 없음 → 그 멈춤이 그 단위의 결과 · L129)


def run_predict(fetch):
    pr = C.Predict(fetch, LAD, None, sv_scope=None)
    try:
        pr.run()
        return 'PREDICTED', None
    except C.Stop as e:
        return (e.code if e.code in C.PREDICT_OUTCOMES else 'STOPPED'), e.code


def make_chain(events):
    """events[(unit, run#)] = stop code — the one-machine chain sees the adopted (+resumed) records = these events."""
    log = {'dbe': 0, 'all': 0}

    def fetch(kit, role, law, c, rj, arms, sv_cf=False):
        log['all'] += 1
        if role == 'sbe_noop':
            return [arm(LAD[law]['r0_sigma'])]
        log['dbe'] += 1
        rr = rr_of(law, rj)
        u = unit_of(role, law, c, rr)
        code = events.get((u, RUN_OF_ROLE.get(role)))
        if code:
            raise C.Stop(code, f'{u} {role}', f'dbe{log["dbe"]}')
        a0 = base_arm0()[(c, law, rr)]
        return [arm(a0)] if role == 'corner' else [arm(a0), arm(a0)]
    return fetch, log


def make_merge(attempts, resume_reading='L123', aaa_reading='A', extra_unit_stop=None):
    log = {'dbe': 0, 'all': 0}
    decided = {}

    def fetch(kit, role, law, c, rj, arms, sv_cf=False):
        log['all'] += 1
        if role == 'sbe_noop':
            return [arm(LAD[law]['r0_sigma'])]
        log['dbe'] += 1
        rr = rr_of(law, rj)
        u = unit_of(role, law, c, rr)
        if u not in decided:                                       # L67 대조 시점 = 처음 요청될 때
            atts = attempts.get(u, [{'kind': 'unit'}])
            decided[u] = adopt(atts, resume_reading, aaa_reading)
            if extra_unit_stop and u in extra_unit_stop:
                decided[u] = ('stop', extra_unit_stop[u])
        st, b = decided[u]
        if st == 'stop':
            raise C.Stop(b, f'{u} (합치기 대조)', f'dbe{log["dbe"]}')
        if st == 'missing':
            raise C.Stop('UNIT_MISSING', u, f'dbe{log["dbe"]}')
        if b['stop_at'] is not None and RUN_OF_ROLE.get(role) == b['stop_at']:
            raise C.Stop(b['code'], f'{u} {role} (부분 채택)', f'dbe{log["dbe"]}')   # L68
        a0 = base_arm0()[(c, law, rr)]
        return [arm(a0)] if role == 'corner' else [arm(a0), arm(a0)]
    return fetch, log


def scenario(name, events, attempts, **kw):
    fc, lc = make_chain(events)
    fm, lm = make_merge(attempts, **kw)
    rc, rm = run_predict(fc), run_predict(fm)
    return {'name': name, 'chain': {'status': rc[0], 'stop': rc[1], 'dbe_runs': lc['dbe'], 'runs_incl_noop': lc['all']},
            'merge': {'status': rm[0], 'stop': rm[1], 'dbe_runs': lm['dbe'], 'runs_incl_noop': lm['all']},
            'same': (rc, lc['dbe']) == (rm, lm['dbe']), 'rules': kw}


A = 'U(c0,P0,R_j0)'
B = 'U(c1,P1,R_j_hi)'
out = []
# S1 — round-3 counterexample under rev-3 partial adoption (the one rev 3 claims to close)
out.append(scenario('S1 round-3 lazy counterexample (A origin NOT_COMPUTED · B corner ARM_CONTRACT)',
                    {(A, 2): 'NOT_COMPUTED', (B, 1): 'ARM_CONTRACT'},
                    {A: [{'kind': 'unit', 'payload': True, 'cause': 'content', 'stop_at': 2, 'code': 'NOT_COMPUTED'}],
                     B: [{'kind': 'unit', 'payload': True, 'cause': 'content', 'stop_at': 1, 'code': 'ARM_CONTRACT'}]}))
# S2 — CUDA OOM at A's origin after corner payload → resume (same machine · env) completes
out.append(scenario('S2 resume after post-payload CUDA OOM',
                    {},
                    {A: [{'kind': 'unit', 'payload': True, 'cause': 'cuda_oom', 'stop_at': 2, 'code': 'RES_RUNNER_RC'},
                         {'kind': 'resume', 'of': 0, 'payload': True, 'cause': None, 'stop_at': None}]}))
# S3 — same, but the first resume entry is rejected pre-solve (thread env var differs) and a second resume completes
for rd in ('A', 'B'):
    out.append(scenario(f'S3 rejected resume then good resume (ATTEMPT_AFTER_ADOPTED reading {rd})',
                        {},
                        {A: [{'kind': 'unit', 'payload': True, 'cause': 'cuda_oom', 'stop_at': 2, 'code': 'RES_RUNNER_RC'},
                             {'kind': 'resume', 'of': 0, 'rejected': True},
                             {'kind': 'resume', 'of': 0, 'payload': True, 'cause': None, 'stop_at': None}]},
                        aaa_reading=rd))
# S4 — power cut during A's FIRST run (no payload · no runner record) → resume? L123 says no (needs first payload) · L128 says yes
for rr_ in ('L123', 'L128'):
    out.append(scenario(f'S4 pre-payload parent death then same-machine resume (resume rule {rr_})',
                        {},
                        {A: [{'kind': 'unit', 'payload': False, 'cause': 'no_record', 'stop_at': 1, 'code': 'RES_NO_RECORD'},
                             {'kind': 'resume', 'of': 0, 'payload': True, 'cause': None, 'stop_at': None}]},
                        resume_reading=rr_))
# S5 — gabia unit with a wrong numpy (entry committed with that fingerprint → pre-solve passes) → merge version check stops;
#      a later correct attempt = ATTEMPT_AFTER_ADOPTED (no ledger-legal path to PREDICTED)
out.append(scenario('S5 version mismatch found only at merge · re-run blocked',
                    {},
                    {B: [{'kind': 'unit', 'payload': True, 'cause': None, 'stop_at': None},
                         {'kind': 'unit', 'payload': True, 'cause': None, 'stop_at': None}]},
                    extra_unit_stop=None))
out[-1]['note'] = 'second attempt alone → ATTEMPT_AFTER_ADOPTED; without it the merge stops on the python/numpy/scipy inequality (§3-3)'
fm, lm = make_merge({B: [{'kind': 'unit', 'payload': True, 'cause': None, 'stop_at': None}]},
                    extra_unit_stop={B: 'UNIT_PROVENANCE_MISMATCH(판 다름 · §3-3)'})
out.append({'name': 'S5b same, without the second attempt', 'merge': dict(zip(('status', 'stop'), run_predict(fm)), dbe_runs=lm['dbe'])})
# S6 — kill the bash runner during A's corner solve on kgy (cause = 자식 신호 9 · attempt folder has no payload) · the orphaned payload
#      process writes σ into $RUN (outside the attempt folder · probe orphan_kill_probe.py) · then #2 on gabia completes
out.append(scenario('S6 signal-9 attempt whose σ landed in $RUN, then another machine',
                    {},
                    {A: [{'kind': 'unit', 'payload': False, 'cause': 'signal9', 'stop_at': 1, 'code': 'RES_RUNNER_RC'},
                         {'kind': 'unit', 'payload': True, 'cause': None, 'stop_at': None}]}))
out[-1]['note'] = 'ledger rules accept #2 (L119: #1 = 결과 전) although #1 σ was readable in $RUN before #2 started'
print(json.dumps(out, ensure_ascii=False, indent=1))
