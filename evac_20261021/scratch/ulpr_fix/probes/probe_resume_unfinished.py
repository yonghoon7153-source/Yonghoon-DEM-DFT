#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 리뷰 탐침 PRE-UL-01 — 승인된 이어 돌림의 새 시도가 단 k_r + 1 을 끝내지 못하면 (TIMEOUT · GUARD) 옛 시도의 단 줄이 남는가.

덱 순서 (in.UT.liggghts:229 창 줄 · :267 단 줄 · :268–298 사건 · :319–330 단 끝 restart · 상태 파일 · ul_rm 은 restart_unload 를 쓰지 않는다):
  옛 시도 = 단 k_r + 1 (예 k4 = 둘째 확인 단) 의 창 · 단 줄 · 사건 (RM) 을 쓴 뒤 요약 전에 끊김 → 마지막 restart_unload = 단 k_r 끝 (s_r)
  새 시도 = RESUME (k_r · s_r) → 단 k_r + 1 창 몇 개 → TIMEOUT (요약 없음) 또는 GUARD (요약 GUARD) — 새 단 줄 없음.
기대 (등록 · README '끊긴 시도가 남긴 줄 = 버림 · 버린 행을 정상 부분 관측으로 쓰지 않는다'): 옛 단 k_r + 1 줄을 쓰지 않는다 →
  새 시도 단독 (같은 꼴 fresh TIMEOUT) 과 같은 판정 (둘째 확인 단 없음 → UNIDENTIFIED · UVa 거부).
사용: python3 -I -B probe_resume_unfinished.py <키트 폴더> <출력 JSON>   (리포에 쓰지 않는다 · 임시 폴더 = TMPDIR)
"""
import json
import os
import shutil
import sys
import tempfile

K = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]
sys.path.insert(0, K)
import ul_lib  # noqa: E402
import ul_reader as U  # noqa: E402

P = ul_lib.load_params()
B73 = U.B73
LIFTS, PS = [0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]
LIFTS_NC, PS_NC = [0.2, 0.25, 0.3, 0.35], [1.6, 1.4, 1.2, 0.4]   # 교차 = k4 (k1–k3 교차 전)


def base(root):
    U._fake_restored(root, B73)
    U._w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
    U._mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': U._ladder(LIFTS, PS), 'summary': 'DONE',
                                'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)


def ut_full(root, lifts=LIFTS, ps=PS, events=(('CROSS', 2, 'first'), ('RM', 4, 'ncross2')), summary='RM_STOP'):
    d = os.path.join(root, B73, 'UT')
    shutil.rmtree(d, ignore_errors=True)
    return U._mk_arm(root, B73, 'UT', {'W': 10000, 'dt': 5e-7, 'steps': U._ladder(lifts, ps), 'summary': summary, 'events': list(events)}, P)


def rows(d, n):
    L = [ln.split(',') for ln in open(os.path.join(d, f'ul_{n}.csv')).read().splitlines() if ln.strip()]
    return L[0], L[1:]


def cat(head, rr):
    return '\n'.join([','.join(head)] + [','.join(r) for r in rr]) + '\n'


def make_unfinished(d, kr, n_new, end, resumed=True):
    """d = 옛 시도가 단 kr + 1 까지 쓴 폴더 (_mk_arm 꼴) → resumed: 옛 시도 (단 kr + 1 끝 줄 · 사건까지 · 요약 전 끊김) + RESUME + 새 시도 창 n_new 개 + end.
    resumed=False: 새 시도 없이 같은 처음 시도가 단 kr + 1 의 창 n_new 개 뒤 end (fresh 대조 — 옛 단 kr + 1 줄 · 사건 없음)."""
    hw, W = rows(d, 'windows')
    hs, S = rows(d, 'steps')
    he, E = rows(d, 'events')
    wk, ws = hw.index('k'), hw.index('step')
    sk, ss = hs.index('k'), hs.index('step')
    es = he.index('step')
    rowk = next(r for r in S if int(r[sk]) == kr)
    sr = int(rowk[ss])
    keep_w = [r for r in W if int(r[ws]) <= sr]
    keep_s = [r for r in S if int(r[ss]) <= sr]
    keep_e = [r for r in E if int(r[es]) <= sr]
    old_w = [r for r in W if int(r[wk]) == kr + 1]
    old_s = [r for r in S if int(r[sk]) == kr + 1]
    old_e = [r for r in E if int(r[es]) > sr and int(r[he.index('k')]) == kr + 1]
    new_w = [list(r) for r in old_w[:n_new]]
    guard = []
    if end == 'GUARD':
        guard = [['GUARD', str(kr + 1), new_w[-1][ws], new_w[-1][hw.index('plate_z')], new_w[-1][hw.index('lift')], 'ke_trans_inst']]
    res = [['RESUME', str(kr), str(sr), rowk[hs.index('plate_z')], rowk[hs.index('lift')], 'state']]
    if resumed:
        U._w(os.path.join(d, 'ul_windows.csv'), cat(hw, keep_w + old_w + new_w))
        U._w(os.path.join(d, 'ul_steps.csv'), cat(hs, keep_s + old_s))
        U._w(os.path.join(d, 'ul_events.csv'), cat(he, keep_e + old_e + res + guard))
        U._w(os.path.join(d, 'restart', f'restart_unload_{sr}.bin'), 'x')
        U._w(os.path.join(d, 'restart', f'state_unload_{sr}.in'), f'variable ul_rstep equal {sr}\nvariable ul_k equal {kr}\nvariable ul_phase equal 1\n'
             'variable ul_modeB equal 1\n')
        man = (f'bed={B73}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nstage=UT screen=screen.txt rc=1 check= rc=1\nreader_arm_rc=0\nend=a1 fails=1 reader_rc=0\n'
               f'bed={B73}\njob=UT\nresume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\n')
        if end == 'GUARD':
            man += 'stage=UT screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n'
        U._w(os.path.join(d, 'run_manifest.txt'), man)
    else:
        U._w(os.path.join(d, 'ul_windows.csv'), cat(hw, keep_w + new_w))
        U._w(os.path.join(d, 'ul_steps.csv'), cat(hs, keep_s))
        U._w(os.path.join(d, 'ul_events.csv'), cat(he, keep_e + guard))
        man = f'bed={B73}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\n'
        if end == 'GUARD':
            man += 'stage=UT screen=screen.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a1 fails=0 reader_rc=0\n'
        U._w(os.path.join(d, 'run_manifest.txt'), man)
        for nm in os.listdir(os.path.join(d, 'dump')):   # fresh: 단 kr + 1 끝 프레임 없음 (그 단을 끝내지 못했다)
            st = int(nm.split('_')[1].split('.')[0])
            if nm.startswith(('atom_', 'contact_')) and st > sr:
                os.remove(os.path.join(d, 'dump', nm))
        rmd = os.path.join(d, 'restart')
        for nm in (os.listdir(rmd) if os.path.isdir(rmd) else []):
            if nm.startswith(('restart_RM_', 'state_RM_')):
                os.remove(os.path.join(rmd, nm))
    smp = os.path.join(d, 'ul_summary.txt')
    if os.path.exists(smp):
        os.remove(smp)
    if end == 'GUARD':
        U._w(smp, f'result=GUARD\narm=UT\nbed={B73}\n')
    return sr


def verdict(root):
    d = os.path.join(root, B73, 'UT')
    u = U.arm_verdict(d, B73, 'UT', P, root=root)
    rr = U.read_run(d, P)
    s = U.selection_state(root, P)
    g = U.gate(root, B73, 'UVa', P)
    return {'primary_status': u['primary_status'], 'rho_pct': u['rho_pct'], 'lower_bound_pct': u.get('lower_bound_pct'),
            'trajectory_status': u['trajectory_status'], 'n_superseded_rows': u['n_superseded_rows'], 'steps_k': [x['k'] for x in rr['steps']],
            'steps_Pbar': [x.get('Pbar') for x in rr['steps']], 'windows_k_last': [(x['k'], x['w']) for x in rr['windows'][-6:]],
            'events': [(e['event'], e['k'], e['step']) for e in rr['events']], 'resume_auth': rr['resume_auth'], 'problems': rr['problems'][:4],
            'why': u['why'][:4], 'selection': s['stage'], 'next': s.get('next'), 'gate_UVa': g[0], 'gate_why': g[1][:200]}


def case(name, fn):
    with tempfile.TemporaryDirectory(prefix=f'pre_ul01_{name}_') as root:
        base(root)
        fn(root)
        return verdict(root)


out = {}
out['A0_fresh_complete'] = case('a0', lambda r: ut_full(r))
out['A1_fresh_timeout_in_k4'] = case('a1', lambda r: make_unfinished(ut_full(r), 3, 2, 'TIMEOUT', resumed=False))
out['A2_resumed_timeout_in_k4'] = case('a2', lambda r: make_unfinished(ut_full(r), 3, 2, 'TIMEOUT', resumed=True))
out['A3_fresh_guard_in_k4'] = case('a3', lambda r: make_unfinished(ut_full(r), 3, 2, 'GUARD', resumed=False))
out['A4_resumed_guard_in_k4'] = case('a4', lambda r: make_unfinished(ut_full(r), 3, 2, 'GUARD', resumed=True))
out['A5_resumed_timeout_in_k4_move_no_new_window'] = case('a5', lambda r: make_unfinished(ut_full(r), 3, 0, 'TIMEOUT', resumed=True))


def no_resume_event(r):
    d = ut_full(r)
    make_unfinished(d, 3, 0, 'TIMEOUT', resumed=True)
    he, E = rows(d, 'events')
    U._w(os.path.join(d, 'ul_events.csv'), cat(he, [e for e in E if e[0] != 'RESUME'] + [['RM', '4', str(int(rows(d, 'steps')[1][-1][6])), '0', '0', 'ncross2']]))


out['A6_resume_from_but_no_RESUME_event_single_attempt_record'] = case('a6', no_resume_event)
ev_nc = (('CROSS', 4, 'first'),)
out['B1_fresh_timeout_in_k3_nocross'] = case('b1', lambda r: make_unfinished(ut_full(r, LIFTS_NC, PS_NC, ev_nc, 'DONE'), 2, 2, 'TIMEOUT', resumed=False))
out['B2_resumed_timeout_in_k3_nocross'] = case('b2', lambda r: make_unfinished(ut_full(r, LIFTS_NC, PS_NC, ev_nc, 'DONE'), 2, 2, 'TIMEOUT', resumed=True))

exp = {'A0_fresh_complete': lambda v: v['primary_status'] == 'OK' and v['gate_UVa'] is True,
       'A1_fresh_timeout_in_k4': lambda v: v['primary_status'] != 'OK' and v['gate_UVa'] is False,
       'A2_resumed_timeout_in_k4': lambda v: v['primary_status'] != 'OK' and v['gate_UVa'] is False,
       'A3_fresh_guard_in_k4': lambda v: v['primary_status'] != 'OK' and v['gate_UVa'] is False,
       'A4_resumed_guard_in_k4': lambda v: v['primary_status'] != 'OK' and v['gate_UVa'] is False,
       'A5_resumed_timeout_in_k4_move_no_new_window': lambda v: v['primary_status'] != 'OK' and v['gate_UVa'] is False,
       'A6_resume_from_but_no_RESUME_event_single_attempt_record': lambda v: True,   # 관찰 — 한 시도 기록 (섞임 없음) · 결함 판정에 쓰지 않음
       'B1_fresh_timeout_in_k3_nocross': lambda v: True,
       'B2_resumed_timeout_in_k3_nocross': lambda v: v['steps_k'] == out['B1_fresh_timeout_in_k3_nocross']['steps_k']
       and v['lower_bound_pct'] == out['B1_fresh_timeout_in_k3_nocross']['lower_bound_pct']}
res = {'kit': K, 'cases': out, 'expect_met': {k: bool(f(out[k])) for k, f in exp.items()}}
res['failed_expectations'] = [k for k, v in res['expect_met'].items() if not v]
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=str)
for k, v in out.items():
    print(f'{k}: primary={v["primary_status"]} rho={v["rho_pct"]} lb={v["lower_bound_pct"]} traj={v["trajectory_status"]} '
          f'steps_k={v["steps_k"]} sup={v["n_superseded_rows"]} gate_UVa={v["gate_UVa"]} expect_met={res["expect_met"][k]}')
print('failed_expectations', res['failed_expectations'])
