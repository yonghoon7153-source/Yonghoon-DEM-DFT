#!/usr/bin/env python3
"""PRE-D3V2 탐침 10 — R08 순서 (S3a < 측정 · 측정 직후 암호화 push · S3b < 봉인 < 열쇠 < 열람) 의 참조 구현 order_ok 가
설계 문장이 금지하는 순서를 받아들이는가.  대조 순서 Y (C08 대조) 에서 한 사건만 바꾼 변이.

재실행: python3 -I p10_r08_order.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
Y = ['S3a_commit', 'C0_start', 'measure_start', 'measure_end', 'raw_push_enc', 'C0_end', 'S3_commit',
     'S3b_commit', 'curve_seal', 'key_commit', 'raw_open']


def mv(seq, ev, after):
    s = [e for e in seq if e != ev]
    s.insert(s.index(after) + 1, ev)
    return s


variants = {
    'Y (대조)': (Y, True),
    '열쇠 커밋 없이 열람 (key_commit 삭제)': ([e for e in Y if e != 'key_commit'], False),
    'C0 없이 S3b (C0_start · C0_end 삭제 — S3b = "C0 로 정하는 값")': ([e for e in Y if e not in ('C0_start', 'C0_end')], False),
    '암호화 push 를 곡선 봉인 뒤로 ("측정 직후" 위반)': (mv(Y, 'raw_push_enc', 'curve_seal'), False),
    'C1 시작이 S3b 보다 먼저 (C1 런 목록 = S3b)': (mv(Y, 'C1_start', 'measure_end'), False),
    # ⚠ 이 행은 참조 구현 ↔ 설계 문장 어긋남이 아니다 — v2 설계 문장 (§3-7 · §3-8 ⑤) 자체가 f_cal · 속도 셋을 S3b (측정 뒤) 에 둔다.
    #   기대값 False = 원장 MXD3-08 제목 (*"S3 등록 (… f_cal · 속도 셋) 이 측정 뒤에 커밋된다"*) 이 결함으로 적은 순서.
    'f_cal · 속도 셋 확정이 측정 뒤 (MXD3-08 제목의 두 항목 · v2 설계 = S3b · 설계도 받음)': (Y[:Y.index('S3b_commit')] + ['protocol_fcal_speeds_fixed'] + Y[Y.index('S3b_commit'):], False),
    '평문 원자료 반입이 열람 직후 · 열쇠 커밋 전 (key 없이)': ([e for e in Y if e != 'key_commit'] + ['raw_push_plain'], False),
}
out = {}
for k, (seq, should_accept) in variants.items():
    got = R2.order_ok(seq)
    out[k] = dict(seq=seq, order_ok=got, design_should_accept=should_accept, mismatch=(got != should_accept))
pcommon.dump('p10_r08_order.json', out)
for k, v in out.items():
    print(f"{'⚠ ' if v['mismatch'] else '  '}{k}: order_ok = {v['order_ok']} (설계 문장대로면 {v['design_should_accept']})")
