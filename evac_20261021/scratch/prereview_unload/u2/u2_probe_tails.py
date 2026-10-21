#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""U2 독립 탐침 — ULPR-01 (승인 경계 뒤 줄 = 시도 증명) 을 손으로 만든 작은 기록으로 친다.

기준 궤적 = 키트 합성기 U._mk_arm (덤프 · thermo · CSV 를 한 시도가 처음부터 끝까지 쓴 꼴) — 이어 돌림 층은 이 탐침이 직접 만든다
(고친 사람의 _resume_mix 를 쓰지 않는다).  덱 쓰는 순서 (in.UT.liggghts:229 창 줄 → :267 단 줄 → :268–298 단 끝 사건 → :319–330 restart_unload + 상태 파일 ·
:186 RESUME 사건) · 러너 (run_unload.sh:267–272 마지막 restart_unload + 짝 상태 파일 · :89 요약 있으면 이어 돌림 거부) 를 따른다.
각 경우 = (resumed 판정, fresh 쌍둥이 판정 — 새 시도 줄만 있는 한 시도 기록) · 기대 = 등록 §14-12 ① 문장 그대로.
사용: python3 -I -B u2_probe_tails.py <키트 폴더> <출력 JSON>
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
R = P['records']
WC, SC, EC = R['windows_cols'], R['steps_cols'], R['events_cols']
B73 = U.B73
LAD = dict(lifts=[0.2, 0.25, 0.3, 0.35], Ps=[1.2, 0.8, 0.6, 0.4], events=[('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], summary='RM_STOP')
NOC = dict(lifts=[0.2, 0.25, 0.3, 0.35], Ps=[1.6, 1.4, 1.2, 0.4], events=[('CROSS', 4, 'first')], summary='DONE')


def base(root):
    U._fake_restored(root, B73)
    U._w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
    U._mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': U._ladder(LAD['lifts'], LAD['Ps']), 'summary': 'DONE', 'events': list(LAD['events'])}, P)


def fresh_full(root, lad, job='UT', extra_steps=(), events=None, summary=None):
    d = os.path.join(root, B73, job)
    shutil.rmtree(d, ignore_errors=True)
    st = U._ladder(lad['lifts'], lad['Ps']) + list(extra_steps)
    return U._mk_arm(root, B73, job, {'W': 10000 if job == 'UT' else 5000, 'dt': 5e-7 if job == 'UT' else 1e-6, 'steps': st,
                                      'summary': summary or lad['summary'], 'events': list(events if events is not None else lad['events'])}, P)


def rd(d):
    out = {}
    for n in ('windows', 'steps', 'events'):
        L = [ln.split(',') for ln in open(os.path.join(d, f'ul_{n}.csv')).read().splitlines() if ln.strip()]
        out[n] = L[1:]
    return out


def cat(head, rows):
    return '\n'.join([','.join(head)] + [','.join(r) for r in rows]) + '\n'


def layer(d, kr, old, new, resumed=True):
    """d = 한 시도 기준 궤적 → (resumed) 옛 시도 (단 kr + 1 의 일부) + RESUME + 새 시도 / (아니면) 새 시도 줄만 (fresh 쌍둥이).
    old = {'nw': 창 수, 'line': 단 줄, 'ev': 기준의 그 단 사건 (단 끝 · 창 사건 전부)}
    new = {'nw': 단 kr+1 창 수, 'skip_w': [지울 창 번호], 'line': 단 줄, 'ev': 그 단 사건, 'rest': kr+2 부터 끝 + 기준 요약, 'state': 단 kr+1 끝 상태 파일,
           'summary': 요약 글 (result=…), 'extra_ev': [(이름, k, step 꼴 'sr+N' | int)], 'no_windows_csv_rows': 새 창 줄을 안 씀}."""
    r = rd(d)
    wk, ws = WC.index('k'), WC.index('step')
    sk, ss = SC.index('k'), SC.index('step')
    ek, es = EC.index('k'), EC.index('step')
    rowk = next(x for x in r['steps'] if int(x[sk]) == kr)
    sr, k1 = int(rowk[ss]), kr + 1
    W1 = [x for x in r['windows'] if int(x[wk]) == k1]
    S1 = [x for x in r['steps'] if int(x[sk]) == k1]
    E1 = [x for x in r['events'] if int(x[es]) > sr and int(x[ek]) == k1]
    Wr = [x for x in r['windows'] if int(x[wk]) > k1]
    Sr = [x for x in r['steps'] if int(x[sk]) > k1]
    Er = [x for x in r['events'] if int(x[es]) > sr and int(x[ek]) > k1]
    keep = {n: [x for x in r[n] if int(x[(ws, ss, es)[i]]) <= sr] for i, n in enumerate(('windows', 'steps', 'events'))}
    old_w = W1[:old.get('nw', 0)]
    old_s = S1 if old.get('line') else []
    old_e = E1 if old.get('ev') else []
    new_w = [x for x in W1[:new.get('nw', 0)] if int(x[WC.index('w')]) not in new.get('skip_w', ())]
    new_w += (Wr if new.get('rest') else [x for x in Wr if int(x[wk]) == k1 + 1][:new.get('next_only_nw', 0)])
    new_s = (S1 if new.get('line') else []) + (Sr if new.get('rest') else [])
    new_e = (E1 if new.get('ev') else []) + (Er if new.get('rest') else [])
    for nm, kk, stp in new.get('extra_ev', ()):
        s_ = sr + int(stp[3:]) if isinstance(stp, str) and stp.startswith('sr+') else int(stp)
        new_e.append([nm, str(kk), str(s_), rowk[SC.index('plate_z')], rowk[SC.index('lift')], 'u2'])
    res = [['RESUME', str(kr), str(sr), rowk[SC.index('plate_z')], rowk[SC.index('lift')], 'state']]
    if new.get('dup_resume'):   # 같은 경계 RESUME 두 줄 (중복) — ULKRF-01 = 승인 없음
        res = res + [list(res[0])]
    if resumed:
        U._w(os.path.join(d, 'ul_windows.csv'), cat(WC, keep['windows'] + old_w + new_w))
        U._w(os.path.join(d, 'ul_steps.csv'), cat(SC, keep['steps'] + old_s + new_s))
        U._w(os.path.join(d, 'ul_events.csv'), cat(EC, keep['events'] + old_e + res + new_e))
        U._w(os.path.join(d, 'restart', f'restart_unload_{sr}.bin'), 'x')
        U._w(os.path.join(d, 'restart', f'state_unload_{sr}.in'), f'variable ul_rstep equal {sr}\nvariable ul_k equal {kr}\nvariable ul_phase equal 0\n'
             'variable ul_modeB equal 1\n')
    else:
        U._w(os.path.join(d, 'ul_windows.csv'), cat(WC, keep['windows'] + new_w))
        U._w(os.path.join(d, 'ul_steps.csv'), cat(SC, keep['steps'] + new_s))
        U._w(os.path.join(d, 'ul_events.csv'), cat(EC, keep['events'] + new_e))
    if new.get('state') and S1:
        s1 = int(S1[0][ss])
        U._w(os.path.join(d, 'restart', f'restart_unload_{s1}.bin'), 'x')
        U._w(os.path.join(d, 'restart', f'state_unload_{s1}.in'), f'variable ul_rstep equal {s1}\nvariable ul_k equal {k1}\nvariable ul_phase equal 0\n'
             'variable ul_modeB equal 1\n')
    if new.get('state_other'):   # 경계 뒤 단 끝 상태 파일 하나 — 그러나 단 kr + 1 끝 step 이 아님 (s_r + 7)
        U._w(os.path.join(d, 'restart', f'state_unload_{sr + 7}.in'), f'variable ul_rstep equal {sr + 7}\nvariable ul_k equal {k1}\n')
    smp = os.path.join(d, 'ul_summary.txt')
    summ = open(smp).read() if os.path.exists(smp) else None
    if os.path.exists(smp):
        os.remove(smp)
    job, bed = os.path.basename(d), os.path.basename(os.path.dirname(d))
    if new.get('summary'):
        U._w(smp, f'{new["summary"]}\narm={job}\nbed={bed}\n')
    elif new.get('rest') and summ:
        U._w(smp, summ)
    done = os.path.exists(smp)
    a1 = f'bed={bed}\njob={job}\nresume=0\ngate=ALLOW\nstart=a1\n'
    if resumed:
        man = (a1 + f'stage={job} screen=screen.txt rc=1 check= rc=1\nreader_arm_rc=0\nend=a1 fails=1 reader_rc=0\n'
               f'bed={bed}\njob={job}\nresume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\n'
               + (f'stage={job} screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n' if done else ''))
    else:
        man = a1 + (f'stage={job} screen=screen.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a1 fails=0 reader_rc=0\n' if done else '')
    U._w(os.path.join(d, 'run_manifest.txt'), man)
    return sr


def verdict(root, job='UT'):
    d = os.path.join(root, B73, job)
    u = U.arm_verdict(d, B73, job, P, root=root)
    rr = U.read_run(d, P)
    out = {'primary': u['primary_status'], 'rho': u['rho_pct'], 'lb': u.get('lower_bound_pct'), 'traj': u['trajectory_status'],
           'steps_k': [x['k'] for x in rr['steps']], 'win_k_last': [(x['k'], x['w']) for x in rr['windows'][-5:]], 'sup': rr['n_superseded_rows'],
           'events': [(e['event'], e['k']) for e in rr['events'] if e['event'] not in ('START',)], 'problems': rr['problems'][:3], 'why': u['why'][:2],
           'tails': rr.get('resume_tails')}
    if job == 'UT':
        g = U.gate(root, B73, 'UVa', P)
        out['gate_UVa'] = g[0]
    return out


def case(name, lad, kr, old, new, job='UT', extra_steps=(), events=None):
    res = {}
    for tag, resumed in (('resumed', True), ('fresh_twin', False)):
        with tempfile.TemporaryDirectory(prefix=f'u2_{name}_{tag}_') as root:
            base(root)
            d = fresh_full(root, lad, job, extra_steps, events)
            try:
                layer(d, kr, old, new, resumed=resumed)
                res[tag] = verdict(root, job)
            except Exception as ex:  # noqa: BLE001
                res[tag] = {'error': f'{type(ex).__name__}: {ex}'}
    return res


C = {}
# ── 원 반례 꼴 (UT · 교차 k2 · 확인 k3 · k4 · R_M k4) — 같은 꼴 fresh 와 같아야 ──
C['A2_old_k4_full_new_2win_timeout'] = case('a2', LAD, 3, dict(nw=4, line=True, ev=True), dict(nw=2))
C['A5_old_k4_full_new_nothing'] = case('a5', LAD, 3, dict(nw=4, line=True, ev=True), dict())
# ── 이웃: 단 줄은 다시 썼는데 창 기록이 모자람 (새 창 w3 빠짐) · 새 단 줄만 있고 새 창 없음 ──
C['N1_new_rewrote_line_window_w3_missing'] = case('n1', LAD, 3, dict(nw=4, line=True, ev=True), dict(nw=4, skip_w=[3], line=True, ev=True, rest=True))
C['N1b_new_rewrote_line_no_new_windows'] = case('n1b', LAD, 3, dict(nw=4, line=True, ev=True), dict(nw=0, line=True, ev=True, rest=True))
# ── 이웃: 증거가 하나만 (요약만 · RESUME 뒤 사건만) — 옛 시도 = 사건 없는 단 (교차 전 k3) 창 넷 + 단 줄 · 새 시도 = 창 없음 ──
#    (덱으로는 만들 수 없는 기록 — GUARD 는 창 뒤 · LIFT_CAP 이면 옛 시도도 같은 판단 · 판독기가 이런 기록을 어떻게 읽는지 본다)
C['N2a_eventless_old_line_new_summary_only'] = case('n2a', NOC, 2, dict(nw=4, line=True), dict(summary='result=GUARD'))
C['N2b_eventless_old_line_new_event_only'] = case('n2b', NOC, 2, dict(nw=4, line=True), dict(extra_ev=[('GUARD', 3, 'sr+1')]))
C['N2c_eventless_old_line_new_summary_and_event'] = case('n2c', NOC, 2, dict(nw=4, line=True), dict(summary='result=GUARD', extra_ev=[('GUARD', 3, 'sr+1')]))
C['N2d_eventless_old_line_new_state_only_for_other_stage'] = case('n2d', NOC, 2, dict(nw=4, line=True), dict(summary=None, extra_ev=[('LIFT_CAP', 2, 'sr+0')]))
C['N2e_eventless_old_line_new_later_stage_windows_only'] = case('n2e', NOC, 2, dict(nw=4, line=True), dict(next_only_nw=2))
C['N2f_eventless_old_line_new_state_file_other_step'] = case('n2f', NOC, 2, dict(nw=4, line=True), dict(state_other=True))
# 확인 단 1 (k3 · 사건 없는 CONFIRM — 덱 ul_end_confirm 은 ncross < 2 이면 사건 없이 ul_step_done) 을 옛 시도 줄로 채우고 새 시도는 k4 부터 (덱으로는 안 생김)
C['N2g_old_confirm1_line_new_skips_to_k4_complete'] = case('n2g', LAD, 2, dict(nw=4, line=True), dict(rest=True))
C['N4_dup_resume_same_boundary_new_completes'] = case('n4', LAD, 3, dict(nw=4, line=True, ev=True), dict(nw=4, line=True, ev=True, rest=True, dup_resume=True))
C['N4b_dup_resume_old_k4_new_2win'] = case('n4b', LAD, 3, dict(nw=4, line=True, ev=True), dict(nw=2, dup_resume=True))
# ── 이웃: 경계 0 · 마지막 단 ──
C['N5a_boundary_k0_old_k1_full_new_2win'] = case('n5a', LAD, 0, dict(nw=4, line=True), dict(nw=2))
C['N5b_boundary_k0_new_completes'] = case('n5b', LAD, 0, dict(nw=4, line=True), dict(nw=4, line=True, ev=True, rest=True))
C['N5c_boundary_last_k3_new_completes'] = case('n5c', LAD, 3, dict(nw=4, line=True, ev=True), dict(nw=4, line=True, ev=True, rest=True))
# ── 보수 쪽 대가 (설계 — 결함 아님) · 옛 시도가 경계 뒤 아무것도 안 씀 ──
C['L1_old_nothing_new_2win_timeout'] = case('l1', LAD, 3, dict(), dict(nw=2))
C['L2_old_nothing_new_full_line_eventless_no_state'] = case('l2', NOC, 2, dict(), dict(nw=4, line=True))
C['L3_old_nothing_new_full_line_with_state'] = case('l3', NOC, 2, dict(), dict(nw=4, line=True, state=True))

json.dump(C, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for k, v in C.items():
    for tag in ('resumed', 'fresh_twin'):
        x = v[tag]
        if 'error' in x:
            print(f'{k:56s} {tag:10s} ERROR {x["error"]}')
            continue
        print(f'{k:56s} {tag:10s} primary={x["primary"]} rho={x["rho"]} lb={x["lb"]} traj={x["traj"]} k={x["steps_k"]} sup={x["sup"]} '
              f'gate={x.get("gate_UVa")} pr={[p[:70] for p in x["problems"][:2]]}')
