#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""U2 — 승인 경계 둘 (러너는 두 번째 이어 돌림을 막는다 · run_unload.sh:88 — 판독기 '경계마다' 견고성만 본다).
att1: 단 k2 창 둘 뒤 끊김 → att2: RESUME (1, s1) · k2 다시 (창 넷 · 단 줄 · CROSS) · state s2 · k3 창 넷 · 단 줄 (확인 1 · 사건 없음) 뒤 끊김 →
att3: RESUME (2, s2) · k3 다시 · state s3 · k4 · RM · RM_STOP · 요약.  기대 = 한 시도 fresh 와 같음 (OK ρ 0.2026…).
변형 B: att3 가 k3 창 둘 뒤 TIMEOUT → 기대 = fresh (k3 창 둘 뒤 TIMEOUT) 와 같음.
사용: python3 -I -B u2_probe_two_boundaries.py <키트 폴더> <출력 JSON>"""
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


def cat(head, rows):
    return '\n'.join([','.join(head)] + [','.join(r) for r in rows]) + '\n'


def build(root, variant):
    U._fake_restored(root, B73)
    U._w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
    U._mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': U._ladder(LAD['lifts'], LAD['Ps']), 'summary': 'DONE', 'events': list(LAD['events'])}, P)
    d = U._mk_arm(root, B73, 'UT', {'W': 10000, 'dt': 5e-7, 'steps': U._ladder(LAD['lifts'], LAD['Ps']), 'summary': 'RM_STOP', 'events': list(LAD['events'])}, P)
    rd = {n: [ln.split(',') for ln in open(os.path.join(d, f'ul_{n}.csv')).read().splitlines()[1:] if ln.strip()] for n in ('windows', 'steps', 'events')}
    wk, sk, ss, ek, es = WC.index('k'), SC.index('k'), SC.index('step'), EC.index('k'), EC.index('step')
    S = {int(r[sk]): r for r in rd['steps']}
    s1, s2 = int(S[1][ss]), int(S[2][ss])
    Wk = {k: [r for r in rd['windows'] if int(r[wk]) == k] for k in range(5)}
    Ek = {k: [r for r in rd['events'] if int(r[ek]) == k and r[0] != 'START'] for k in range(5)}
    start = [r for r in rd['events'] if r[0] == 'START']
    res1 = ['RESUME', '1', str(s1), S[1][SC.index('plate_z')], S[1][SC.index('lift')], 'state']
    res2 = ['RESUME', '2', str(s2), S[2][SC.index('plate_z')], S[2][SC.index('lift')], 'state']
    if variant == 'A':
        att3_w = Wk[3] + Wk[4]
        att3_s = [S[3], S[4]]
        att3_e = Ek[3] + Ek[4]
    else:
        att3_w, att3_s, att3_e = Wk[3][:2], [], []
    W = Wk[0] + Wk[1] + Wk[2][:2] + Wk[2] + Wk[3] + att3_w
    St = [S[0], S[1]] + [S[2], S[3]] + att3_s
    E = start + Ek[0] + Ek[1] + [res1] + Ek[2] + Ek[3] + [res2] + att3_e
    U._w(os.path.join(d, 'ul_windows.csv'), cat(WC, W))
    U._w(os.path.join(d, 'ul_steps.csv'), cat(SC, St))
    U._w(os.path.join(d, 'ul_events.csv'), cat(EC, E))
    for s, k in ((s1, 1), (s2, 2)):
        U._w(os.path.join(d, 'restart', f'restart_unload_{s}.bin'), 'x')
        U._w(os.path.join(d, 'restart', f'state_unload_{s}.in'), f'variable ul_rstep equal {s}\nvariable ul_k equal {k}\nvariable ul_phase equal 0\nvariable ul_modeB equal 1\n')
    if variant == 'A':
        s3 = int(S[3][ss])
        U._w(os.path.join(d, 'restart', f'state_unload_{s3}.in'), f'variable ul_rstep equal {s3}\nvariable ul_k equal 3\n')
    else:
        os.remove(os.path.join(d, 'ul_summary.txt'))
    man = (f'bed={B73}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nend=a1 fails=1 reader_rc=0\n'
           f'bed={B73}\njob=UT\nresume=1\ngate=RESUME\nstart=a2\nresume_from={s1}\nend=a2 fails=1 reader_rc=0\n'
           f'bed={B73}\njob=UT\nresume=1\ngate=RESUME\nstart=a3\nresume_from={s2}\n' + ('end=a3 fails=0 reader_rc=0\n' if variant == 'A' else ''))
    U._w(os.path.join(d, 'run_manifest.txt'), man)
    return d


out = {}
for v in ('A', 'B'):
    with tempfile.TemporaryDirectory(prefix=f'u2_two_{v}_') as root:
        d = build(root, v)
        u = U.arm_verdict(d, B73, 'UT', P, root=root)
        rr = U.read_run(d, P)
        g = U.gate(root, B73, 'UVa', P)
        out[v] = {'primary': u['primary_status'], 'rho': u['rho_pct'], 'traj': u['trajectory_status'], 'k': [x['k'] for x in rr['steps']],
                  'auth': rr['resume_auth'], 'sup': rr['n_superseded_rows'], 'problems': rr['problems'][:3], 'gate_UVa': g[0], 'tails': rr['resume_tails']}
        print(v, {k: out[v][k] for k in ('primary', 'rho', 'traj', 'k', 'auth', 'sup', 'gate_UVa')}, [p[:90] for p in out[v]['problems']])
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
