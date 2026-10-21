#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""U2 — 자체시험 R10 의 기록 꼴을 그대로 다시 만들어 (ul_reader.selftest 의 R10 블록 글 그대로) resume_tails 를 본다.
R10 = 창 CSV 경계 뒤에 옛 k2 창 둘 (P 9.999) · 사건 CSV 끝에 RESUME 한 줄을 덧붙임 (새 시도 사건 CROSS · RM 뒤) · 단 CSV 그대로.
변형 = RESUME 줄을 덱 순서 (경계 뒤 첫 사건 앞) 로.
사용: python3 -I -B u2_probe_r10.py <키트 폴더> <출력 JSON>"""
import json
import os
import sys
import tempfile

K = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]
sys.path.insert(0, K)
import ul_lib  # noqa: E402
import ul_reader as U  # noqa: E402

P = ul_lib.load_params()
B73 = U.B73
out = {}
for variant in ('as_in_selftest', 'resume_in_deck_order'):
    with tempfile.TemporaryDirectory(prefix='u2_r10_') as root:
        sp = {'W': 5000, 'dt': 1e-6, 'steps': U._ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]),
              'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}
        d = U._mk_arm(root, B73, 'UB', sp, P)
        wpath = os.path.join(d, 'ul_windows.csv')
        L = open(wpath).read().splitlines()
        stale = [ln.split(',') for ln in L[1:] if ln.split(',')[2] == '2']
        resume_step = int([ln.split(',') for ln in L[1:] if ln.split(',')[2] == '1'][-1][5])
        extra = [','.join(r[:5] + [str(int(r[5]))] + r[6:8] + ['9.999'] + r[9:]) for r in stale[:2]]
        U._w(wpath, '\n'.join(L[:1] + [ln for ln in L[1:] if int(ln.split(',')[5]) <= resume_step] + extra
                              + L[1:][len([1 for ln in L[1:] if int(ln.split(',')[5]) <= resume_step]):]) + '\n')
        ep = os.path.join(d, 'ul_events.csv')
        if variant == 'as_in_selftest':
            open(ep, 'a').write(f'RESUME,1,{resume_step},0.111252,0.0002,state\n')
        else:
            EL = open(ep).read().splitlines()
            i = next(i for i, x in enumerate(EL[1:], 1) if int(x.split(',')[2]) > resume_step)
            U._w(ep, '\n'.join(EL[:i] + [f'RESUME,1,{resume_step},0.111252,0.0002,state'] + EL[i:]) + '\n')
        U._w(os.path.join(d, 'run_manifest.txt'), f'bed={B73}\njob=UB\nresume=0\ngate=ALLOW\nend=a1 fails=1 reader_rc=0\nbed={B73}\njob=UB\nresume=1\ngate=RESUME\n'
             f'resume_from={resume_step}\nend=a2 fails=0 reader_rc=0\n')
        U._w(os.path.join(d, 'restart', f'state_unload_{resume_step}.in'), f'variable ul_rstep equal {resume_step}\nvariable ul_k equal 1\n')
        u = U.arm_verdict(d, B73, 'UB', P, root=root)
        rr = U.read_run(d, P)
        out[variant] = {'primary': u['primary_status'], 'rho': u['rho_pct'], 'sup': rr['n_superseded_rows'],
                        'events_kept': [(e['event'], e['k']) for e in rr['events']], 'tails': rr['resume_tails'], 'problems': rr['problems'][:2]}
        print(variant, json.dumps(out[variant], ensure_ascii=False, default=str)[:700])
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
