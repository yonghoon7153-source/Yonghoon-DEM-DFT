#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""U2 — ULPR-03 · 04 작은 반례 (ul_gates.g2_compare · g2c_compare 직접) · 리포에 쓰지 않는다 (임시 폴더 = TMPDIR).
사용: python3 -I -B u2_probe_g2.py <키트 폴더> <출력 JSON>"""
import json
import os
import sys
import tempfile

K = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]
sys.path.insert(0, K)
import ul_lib  # noqa: E402
import ul_gates as G  # noqa: E402

C = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz']
base = [{'id': i, 'type': 3, 'x': 0.001 * i, 'y': 0.002, 'z': 0.003, 'radius': 0.0005, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0} for i in range(1, 6)]
CC = [f'c_cpl[{c}]' for c in range(1, 27)]


def crow(i, j, fn):
    v = [0.001 * i, 0.01, 0.01, 0.001 * j, 0.01, 0.01, i, j, 0, fn, 0, 0, -fn, 0, 0, 0, 0.01, 0, 0, 0, 0, 1e-8, 1e-5, 0.00125, 0.01, 0.01]
    return dict(zip(CC, v))


res = {}
with tempfile.TemporaryDirectory(prefix='u2_g2_') as td:
    def p(n):
        return os.path.join(td, n)
    ul_lib.write_custom(p('o.a'), 3200000, C, base)
    # a. 같은 ID 의 완전히 같은 줄 두 번 (값 같음 · 선언 수 = 행 수)
    ul_lib.write_custom(p('a.a'), 3200000, C, base + [dict(base[2])])
    res['a_exact_duplicate_line'] = G.g2_compare(p('a.a'), p('o.a'), step=3200000)
    # b. 원 쪽도 같은 중복 (두 쪽이 같다 — 같다는 것만으로 PASS 하지 않아야)
    ul_lib.write_custom(p('b.o'), 3200000, C, base + [dict(base[2])])
    res['b_same_duplicate_both_sides'] = G.g2_compare(p('a.a'), p('b.o'), step=3200000)
    # c. 선언 수 5 인데 행 6 (머리 손댐)
    ul_lib.write_custom(p('c.a'), 3200000, C, base + [dict(base[0], id=6)])
    t = open(p('c.a')).read().replace('ITEM: NUMBER OF ATOMS\n6\n', 'ITEM: NUMBER OF ATOMS\n5\n', 1)
    open(p('c.a'), 'w').write(t)
    res['c_declared_count_mismatch'] = G.g2_compare(p('c.a'), p('o.a'), step=3200000)
    # d. 두 덤프 모두 같은 다른 step (서로 같음 · 요청 step 과 다름) — G2 · G2c 둘 다
    ul_lib.write_custom(p('d1.a'), 3199000, C, base)
    ul_lib.write_custom(p('d2.a'), 3199000, C, base)
    res['d_g2_both_same_wrong_step'] = G.g2_compare(p('d1.a'), p('d2.a'), step=3200000)
    rows = [crow(1, 2, -0.5), crow(2, 3, -0.5)]
    ul_lib.write_local(p('d1.c'), 3199000, CC, rows)
    ul_lib.write_local(p('d2.c'), 3199000, CC, rows)
    res['d_g2c_both_same_wrong_step'] = G.g2c_compare(p('d1.c'), p('d2.c'), step=3200000)
    res['d_g2c_both_same_wrong_step_no_request'] = G.g2c_compare(p('d1.c'), p('d2.c'))
    # e. 원 덤프 없음 (파일 없음) — 관측 결손
    res['e_orig_missing'] = G.g2_compare(p('o.a'), p('nope.a'), step=3200000)
    # f. 두 프레임 (덤프 끝에 같은 머리 한 번 더)
    t = open(p('o.a')).read()
    open(p('f.a'), 'w').write(t + t)
    res['f_two_frames'] = G.g2_compare(p('f.a'), p('o.a'), step=3200000)
    # g. ID 0 · 음수 · 2^53 + 1
    for tag, bad in (('g_id_zero', '0'), ('g_id_negative', '-3'), ('g_id_2p53p1', '9007199254740993')):
        t = open(p('o.a')).read().replace('\n3 3 ', f'\n{bad} 3 ', 1)
        open(p(tag + '.a'), 'w').write(t)
        res[tag] = G.g2_compare(p(tag + '.a'), p('o.a'), step=3200000)
    # h. 대조: 같은 덤프 = PASS · 값 하나 다름 = FAIL
    res['h_control_same'] = G.g2_compare(p('o.a'), p('o.a'), step=3200000)
    ul_lib.write_custom(p('h.a'), 3200000, C, [dict(base[0], x=0.5)] + base[1:])
    res['h_control_value'] = G.g2_compare(p('h.a'), p('o.a'), step=3200000)
out = {k: {'status': v.get('status'), 'why': (v.get('why') or [])[:2]} for k, v in res.items()}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(f'{k:42s} {v["status"]:13s} {[w[:80] for w in v["why"]]}')
