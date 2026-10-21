#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 리뷰 탐침 (기타) — ULKRF-01 주변 · ULKRF-03 주변 (G2 옆 자리 · 중력 팔) · Q4 토큰 · Q3 kit 목록 (리포에 쓰지 않는다).
python3 -I -B probe_misc.py <키트 폴더> <출력 JSON>"""
import json
import os
import shutil
import sys
import tempfile

K = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]
sys.path.insert(0, K)
import ul_gates  # noqa: E402
import ul_lib  # noqa: E402
import ul_reader as U  # noqa: E402

P = ul_lib.load_params()
B73 = U.B73
res = {}


def setup(root):
    U._fake_restored(root, B73)
    U._w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
    U._mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': U._ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]), 'summary': 'DONE',
                                'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)
    d = os.path.join(root, B73, 'UT')
    shutil.rmtree(d, ignore_errors=True)
    return U._mk_arm(root, B73, 'UT', {'W': 10000, 'dt': 5e-7, 'steps': U._ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]), 'summary': 'RM_STOP',
                                       'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)


def ev(root, d):
    u = U.arm_verdict(d, B73, 'UT', P, root=root)
    rr = U.read_run(d, P)
    g = U.gate(root, B73, 'UVa', P)
    return {'primary': u['primary_status'], 'rho': u['rho_pct'], 'auth': rr['resume_auth'], 'sup': rr['n_superseded_rows'],
            'problems': [p[:150] for p in rr['problems'][:3]], 'gate_UVa': g[0]}


def edit(path, fn):
    t = open(path, encoding='utf-8').read()
    U._w(path, fn(t))


# ── ULKRF-01 주변 ─────────────────────────────────────────────────────────────
def r1(name, mut):
    with tempfile.TemporaryDirectory(prefix='pre_misc_r1_') as root:
        d = setup(root)
        sr = U._resume_layout(d, P, job='UT')
        mut(d, sr)
        res[name] = ev(root, d)


r1('R1a_control_true_resume', lambda d, sr: None)
FW = str.maketrans('0123456789', '０１２３４５６７８９')
r1('R1b_fullwidth_digits_in_resume_from', lambda d, sr: edit(os.path.join(d, 'run_manifest.txt'),
                                                              lambda t: t.replace(f'resume_from={sr}', f'resume_from={str(sr).translate(FW)}')))
r1('R1c_extra_RESUME_at_step_not_in_resume_from', lambda d, sr: edit(os.path.join(d, 'ul_events.csv'),
                                                                     lambda t: t + f'RESUME,0,{sr - 1},0,0,state\n'))
r1('R1d_extra_RESUME_nonnumeric_k', lambda d, sr: edit(os.path.join(d, 'ul_events.csv'), lambda t: t + f'RESUME,x,{sr},0,0,state\n'))
r1('R1e_RESUME_step_decimal_token_rounds', lambda d, sr: edit(os.path.join(d, 'ul_events.csv'), lambda t: t.replace(f'RESUME,1,{sr},', f'RESUME,1,{sr}.4,')))
r1('R1f_RESUME_k_decimal_token_rounds', lambda d, sr: edit(os.path.join(d, 'ul_events.csv'), lambda t: t.replace(f'RESUME,1,{sr},', f'RESUME,1.4,{sr},')))
r1('R1g_two_resume_from_lines_same_step', lambda d, sr: edit(os.path.join(d, 'run_manifest.txt'), lambda t: t + f'resume_from={sr}\n'))

# ── ULKRF-03 주변 ─────────────────────────────────────────────────────────────
with tempfile.TemporaryDirectory(prefix='pre_misc_g2_') as td:
    cols = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz']
    base = [{'id': i, 'type': 3, 'x': 0.001 * i, 'y': 0.002, 'z': 0.003, 'radius': 0.0005, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0} for i in range(1, 6)]
    o = os.path.join(td, 'o.a')
    ul_lib.write_custom(o, 3200000, cols, base)
    t1 = os.path.join(td, 't_dup.a')
    ul_lib.write_custom(t1, 3200000, cols, [dict(base[2], x=0.9)] + base)   # 원자 3 이 두 번 (첫 줄 = 다른 x · 뒤 = 원과 같음 · 선언 수 6)
    t2 = os.path.join(td, 't_step.a')
    ul_lib.write_custom(t2, 9999999, cols, base)                               # 머리 TIMESTEP 다름
    t3 = os.path.join(td, 't_trunc.a')
    ul_lib.write_custom(t3, 3200000, cols, base)
    edit(t3, lambda t: t.replace('\n5 3 ', '\n5 3 0.005 ', 1) if False else t.rstrip('\n') + '\n3 3 0.9\n')   # 원자 3 의 잘린 (열 수 다른) 줄 덧붙임
    res['G2a_duplicate_conflicting_row_in_test'] = ul_gates.g2_compare(t1, o)
    res['G2b_header_timestep_differs'] = ul_gates.g2_compare(t2, o)
    res['G2c_truncated_extra_row'] = ul_gates.g2_compare(t3, o)
    res['G2_reference_read_dump_on_dup'] = {'ok': ul_lib.read_dump(t1, 'custom', cols)['ok'], 'problems': ul_lib.read_dump(t1, 'custom', cols)['problems'][:3]}
    # G2c 양쪽 열 결손
    ccols = [f'c_cpl[{i}]' for i in range(1, 27)]
    row = dict(zip(ccols, [0.001, 0.01, 0.01, 0.0015, 0.01, 0.01, 1, 2, 0, -0.5, 0, 0, -0.5, 0, 0, 0, 0.01, 0, 0, 0, 0, 1e-8, 1e-5, 0.00125, 0.01, 0.01]))
    a, b = os.path.join(td, 'a.c'), os.path.join(td, 'b.c')
    for p_ in (a, b):
        ul_lib.write_local(p_, 3200000, ccols, [row])
        edit(p_, lambda t: t.replace(' c_cpl[7] ', ' not_c_cpl[7] ', 1))
    g = ul_gates.g2c_compare(a, b)
    res['G2c_both_files_column_missing'] = {'status': g['status'], 'why': g['why'][:3]}

# 중력 팔 복원 경로 (_g_restore) — 출처 팔 R_M 쌍 덤프 머리 c_cpl[7] 결손
with tempfile.TemporaryDirectory(prefix='pre_misc_grav_') as root:
    try:
        U._fake_restored(root, B73)
        U._w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        src = U._mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': U._ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]), 'summary': 'DONE',
                                          'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)
        rm = [ln.split(',') for ln in open(os.path.join(src, 'ul_events.csv')).read().splitlines() if ln.startswith('RM,')][0]
        rm_step = int(rm[2])
        g = os.path.join(root, B73, 'G_UB')
        os.makedirs(os.path.join(g, 'dump'), exist_ok=True)
        for nm in (f'atom_{rm_step}.dump', f'contact_{rm_step}.dump'):
            shutil.copyfile(os.path.join(src, 'dump', nm), os.path.join(g, 'dump', nm))
        edit(os.path.join(src, 'dump', f'contact_{rm_step}.dump'), lambda t: t.replace(' c_cpl[7] ', ' not_c_cpl[7] ', 1))
        U._w(os.path.join(g, 'ul_events.csv'), ','.join(P['records']['events_cols']) + f'\nSTART,0,{rm_step},0,0,s0\n')
        for n_ in ('windows', 'steps'):
            U._w(os.path.join(g, f'ul_{n_}.csv'), ','.join(P['records'][f'{n_}_cols']) + '\n')
        U._w(os.path.join(g, 'screen.txt'), 'LIGGGHTS-PUBLIC 3.8.0 (git 3d5c00f)\n')
        U._w(os.path.join(g, 'run_manifest.txt'), f'source={src} rm_step={rm_step}\n')
        run = U.read_run(g, P)
        gr = U._g_restore(g, run, root, B73, 'G_UB')
        res['GRAV_source_contact_column_missing'] = {'status': gr['status'], 'G2c': gr.get('G2c'), 'why': gr.get('why')}
    except Exception as e:  # noqa: BLE001
        res['GRAV_source_contact_column_missing'] = {'exception': f'{type(e).__name__}: {e}'}

# ── Q4 토큰 ───────────────────────────────────────────────────────────────────
toks = ['2', '+2', '0002', '2.0', '1e3', '1_000', '٣', '３', '9007199254740993', '9007199254740993.0', '+9007199254740993',
        '٩٠٠٧١٩٩٢٥٤٧٤٠٩٩٣', '2.0000000000000001', '0x10', 'nan', '-1', '0']
tk = {}
for t in toks:
    try:
        v, p_ = ul_lib._id_value(t)
        tk[repr(t)] = {'value': repr(v), 'problem': p_, 'exact_id': ul_lib.exact_id(v)}
    except Exception as e:  # noqa: BLE001
        tk[repr(t)] = {'exception': f'{type(e).__name__}: {e}'}
res['Q4_tokens'] = tk

# ── Q3 kit 목록 (실제 판독기 파일 = 봉인 · kit SHA256SUMS 의 판독기 줄만 다름 · sums_sha256 맞춤) ─────────────────────────
with tempfile.TemporaryDirectory(prefix='pre_misc_q3_') as base:
    files = {n: open(os.path.join(K, 'history_test', n), encoding='utf-8').read() for n in U.GRAMMAR_INPUTS}
    lmp = 'a' * 64
    vp = U._mk_gram(base, lmp, files)
    kit = os.path.join(base, 'work', 'kit_20261014_000000')
    sp = os.path.join(kit, 'SHA256SUMS')
    edit(sp, lambda t: t.replace(U.GRAMMAR_READER['read_history.py'], 'f' * 64))
    man = os.path.join(os.path.dirname(vp), 'run_manifest.txt')
    edit(man, lambda t: '\n'.join((f'sums_sha256={ul_lib.sha256_file(sp)}' if ln.startswith('sums_sha256=') else ln) for ln in t.splitlines()) + '\n')
    ok, pr, rec = U.grammar_prereq(vp, lmp)
    res['Q3a_kit_sums_lists_other_reader_hash_file_sealed'] = {'ok': ok, 'problems': [x[:160] for x in pr[:3]], 'reread': (rec.get('reread') or {}).get('status')}
    vp2 = U._mk_gram(os.path.join(base, 'b2'), lmp, files)
    ok2, pr2, rec2 = U.grammar_prereq(vp2, lmp)
    res['Q3b_control_positive'] = {'ok': ok2, 'problems': pr2[:2], 'reread': (rec2.get('reread') or {}).get('status')}

json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for k, v in res.items():
    print(k, json.dumps(v, ensure_ascii=False, default=str)[:400])
