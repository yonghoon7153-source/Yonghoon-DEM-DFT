#!/usr/bin/env python3
"""recheck 10-21 — do the fixed readback's D2 guards (the ones the selftest may not pin) actually fire?  In-memory edits of a real
fixed-generator D2 deck (GMuu ref20 lab) + its deck_meta; each case = one edit; record d2_check problems (expect the named reason).
usage: python3 -I -B probe_rb_guards.py <W>   (writes probe_rb_guards.json)"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
sys.path.insert(0, os.path.join(W, 'scripts'))
s = importlib.util.spec_from_file_location('rbx', os.path.join(W, 'scripts', 'mixer_deck_readback.py'))
rb = importlib.util.module_from_spec(s)
s.loader.exec_module(rb)
D0 = os.path.join(HERE, 'decks', 'recheck', 'GMuu_ref20_lab')
T = open(os.path.join(D0, 'in.mixer'), encoding='utf-8').read()
M = json.load(open(os.path.join(D0, 'deck_meta.json'), encoding='utf-8'))
TC = open(os.path.join(HERE, 'decks', 'recheck', 'GMcc_exp_ref20_lab', 'in.mixer'), encoding='utf-8').read()


def run(text, meta, want):
    import hashlib
    if meta is not None:
        meta = dict(meta, deck_sha256=hashlib.sha256(text.encode('utf-8')).hexdigest())
    R = rb.d2_check(rb.read_deck(text, 'x', meta=meta))
    return dict(is_d2=R['is_d2'], n=len(R['problems']), hit=any(want in p for p in R['problems']), first=[p[:170] for p in R['problems'][:3]])


head = [l for l in T.split('\n') if l.startswith('# ★ D2 결합 규칙 (기하평균')][0]
cases = {
    'control (as generated)': (T, M, ''),
    'R03 header gamma_W != 0.0256*rho (wall line gamma_W 0.00768 -> 0.00769 in both lines)':
        (T.replace('γ_W/γ_SE 0.00768 ·', 'γ_W/γ_SE 0.00769 ·').replace('× ρ_비코팅 0.3 = 0.00768 —', '× ρ_비코팅 0.3 = 0.00769 —'), None, 'Q2'),
    'R17 insertion line says uniform (deck has 2 insert/pack)': (T.replace('삽입 = 층상 (AM → SE · D11 (가))', '삽입 = 균일'), None, '삽입'),
    'R19 explicit wall line with uncoated NCM (header only)':
        (T.replace('#   벽 = 비코팅 NCM 에 묶음 (1저자 10-14 Q2): γ_W/γ_SE = 0.0256 (Hare 2026 Table 3) × ρ_비코팅 0.3 = 0.00768 — 같은 ρ 세계의 코팅 팔도 같은 벽',
                   '#   벽 γ_W/γ_SE = 명시 입력 0.00768 — NCM 상 γ 전부 1 (코팅 · 같은 γ 세계) 인 팔만 (1저자 10-14 Q2) · 이 벽의 비코팅 NCM 함의 ρ = γ_W/0.0256 = 0.3'),
         None, '명시 벽'),
    'R20 full-width Bo token in header': (T.replace('SE–SE Bo_code 0.5 (', 'SE–SE Bo_code ０.５ ('), None, 'ASCII'),
    'R20b underscore gamma token in header': (T.replace('γ/γ_SE: AM_P 0.3 ', 'γ/γ_SE: AM_P 0_3 '), None, 'ASCII'),
    'R21 head line twice': (T.replace(head, head + '\n' + head), None, '머리 줄'),
    'R16 head line removed but meta has adhesion_rule': (T.replace(head + '\n', ''), M, '선언이 없다'),
    'R18 surface line says coated for gamma 0.3': (T.replace('AM_P 비코팅 · AM_S 비코팅', 'AM_P 코팅 · AM_S 비코팅'), None, '표면'),
    'R04 NCM gamma neither 1 nor rho (AM_S 0.5 in header, CED as generated)': (T.replace('· AM_S 0.3 · SE 1 ·', '· AM_S 0.5 · SE 1 ·'), None, 'Q2'),
    'G gravity changed in deck (9.81 -> 9.80)': (T.replace('gravity 9.81', 'gravity 9.80'), None, 'Bo'),
    'X explicit-coated deck: implied rho token wrong (0.3 -> 0.31)': (TC.replace('함의 ρ = γ_W/0.0256 = 0.3', '함의 ρ = γ_W/0.0256 = 0.31'), None, '함의 ρ'),
}
res = {k: run(*v) for k, v in cases.items()}
for k, v in res.items():
    print(f"{k[:78]:78s} is_d2={v['is_d2']} n={v['n']} hit={v['hit']} | {(v['first'] or ['—'])[0][:120]}")
json.dump(res, open(os.path.join(HERE, 'probe_rb_guards.json'), 'w'), ensure_ascii=False, indent=1)
