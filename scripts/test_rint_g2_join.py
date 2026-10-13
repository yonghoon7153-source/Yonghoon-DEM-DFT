#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint G2 ①′ — 덤프 경로 조인 관문 T4-2 · N5′ · N1 시험 (반례 먼저 · 규율 ② · 2026-10-13).

계약 = v2 §3-7 (조인 관문 1–4) · §4 T4-2 · N1 · N5 + v3 §6-3 (G-geo = 기하 대응 · G-frame = 같은 프레임 · 재사용 = 선언 · N5′) ·
v3 §6-6 R3 (`iface_join` 에 G-geo · G-frame 결과 · `iface_geom_reuse`).  판정 = docs/reviews/codex_review_rint_g2_v3_20261007.md.

실데이터 (리포 안): docs/data/real14_reference_20260928/ (atom · contact 2,060,000 · 같은 TIMESTEP) + docs/data/real14_am_scaffold.csv ·
docs/data/case15_corner_20261001/ (atom · contact 1,710,000 + case15_am_scaffold.csv).  변조는 **임시 사본**에만 (커밋된 자료 무변경).

⚠ 이 시험의 PASS 는 조인 관문 (기하 대응 · 같은 프레임 · 선언된 재사용) 의 증거다 — 덤프 경로의 부류 · 면적 (c_cpl[22]) 채택이나
  ①′ 정량 채택이 아니다 (면적 원천 = scaffold lens 그대로 · 정량 채택 · 생산 HOLD).

  python3 scripts/test_rint_g2_join.py
  python3 scripts/test_rint_g2_join.py --s3 PATH

묶음:
  J0  읽기 동등 — 우리 덤프 읽기 = lhs_descriptor_harvest.read_contact_dump · lhs_perc_extract.read_atom_dump · 반폭 = _half_ulp
  J1  real_14 통과 (G-geo 457 ↔ 457 · G-frame 같은 step · pos1/pos2 = 원자 위치 (주기 영상 포함) · δ · A · 접촉 집합)
  J2  case15 통과 (형 지도 1 = AM_P · 2 = SE)
  J3  한 줄 변조 — 원자 1 nm · 접촉 pos1 1 nm · scaffold 1 nm · δ 부호 · A +1 % · 상자 · 고아 id · 두 프레임 · 접촉 행 삭제 → 거부
  N5′ 다른 step 머리 (위치 같음) → 거부 · 선언된 재사용만 통과 + 기록 · 틀린 선언 · 불필요한 선언 → 거부
  N1  dilate_z ≠ 1 → 거부 · 형 지도 없음 → TypeError
  J4  계획 기록 — iface_join · iface_join_status · iface_geom_reuse (요청할 때만) · 실패 · 다른 입자 · 변조된 조인 → 정량 거부 ·
      join=None 은 σ · 행 · 다른 기록 비트 같음 · 원장 ↔ DEM 접촉 대조 (보고만)
"""
import argparse
import contextlib
import gzip
import importlib.util
import io
import os
import shutil
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

S3 = None
S3_PATH = None
J = None
TMP = None
_ok, _fail = 0, []

R14 = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
R14_ATOM = os.path.join(R14, 'atom_2060000.liggghts.gz')
R14_CONT = os.path.join(R14, 'contact_2060000.liggghts.gz')
R14_SCAF = os.path.join(ROOT, 'docs', 'data', 'real14_am_scaffold.csv')
R14_TMAP = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
C15 = os.path.join(ROOT, 'docs', 'data', 'case15_corner_20261001')
C15_ATOM = os.path.join(C15, 'atom_v4_1710000.liggghts.gz')
C15_CONT = os.path.join(C15, 'contact_v4_1710000.liggghts.gz')
C15_SCAF = os.path.join(C15, 'case15_am_scaffold.csv')
C15_TMAP = {1: 'AM_P', 2: 'SE'}


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return bool(cond)


CASES = []


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def raises(fn, exc=(ValueError, TypeError)):
    try:
        fn()
    except exc:
        return True
    return False


def codes(obj):
    return sorted(x['code'] for x in obj['rejections'])


_TXT = {}


def text_lines(path):
    if path not in _TXT:
        op = gzip.open if path.endswith('.gz') else open
        with op(path, 'rt', encoding='utf-8') as fh:
            _TXT[path] = fh.read().split('\n')
    return list(_TXT[path])


def write_copy(lines, name):
    p = os.path.join(TMP, name)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    return p


def item_index(lines, item):
    return next(i for i, ln in enumerate(lines) if ln.startswith(item))


def am_ids(lines, tmap):
    """원자 덤프에서 AM 원자 id · 행 번호 (마지막 프레임 하나)."""
    i = item_index(lines, 'ITEM: ATOMS')
    out = []
    k = i + 1
    while k < len(lines) and lines[k].strip() and not lines[k].startswith('ITEM:'):
        v = lines[k].split()
        if tmap.get(int(v[1])) in ('AM_P', 'AM_S'):
            out.append((int(v[0]), k))
        k += 1
    return out


def first_am_am_row(cl, al, tmap):
    """접촉 덤프에서 AM–AM 이고 주기 영상이 아닌 (pos 토큰 = 원자 토큰) 첫 행 번호."""
    ia = item_index(al, 'ITEM: ATOMS')
    kind, tok = {}, {}
    k = ia + 1
    while k < len(al) and al[k].strip() and not al[k].startswith('ITEM:'):
        v = al[k].split()
        kind[int(v[0])] = tmap.get(int(v[1])); tok[int(v[0])] = v[2:5]
        k += 1
    ic = item_index(cl, 'ITEM: ENTRIES')
    k = ic + 1
    while k < len(cl) and cl[k].strip() and not cl[k].startswith('ITEM:'):
        v = cl[k].split()
        a, b = int(float(v[6])), int(float(v[7]))
        if kind.get(a) in ('AM_P', 'AM_S') and kind.get(b) in ('AM_P', 'AM_S') and v[0:3] == tok[a] and v[3:6] == tok[b]:
            return k
        k += 1
    raise AssertionError('AM–AM 행이 없다')


def g6(x):
    """덤프와 같은 `%g` 6 유효숫자 — 변조 토큰이 파일의 유효숫자 (반폭 규약) 를 바꾸지 않게."""
    return '%.6g' % x


def bump(tok, d):
    return g6(float(tok) + d)


_JR14 = None


def join_r14():
    global _JR14
    if _JR14 is None:
        _JR14 = J.am_iface_join(R14_SCAF, R14_ATOM, R14_CONT, type_map=R14_TMAP)
    return _JR14


# ═════════════════════════ J0 ═════════════════════════
@case('J0 읽기 동등 — 우리 덤프 읽기 = 리포의 읽기 · 반폭 = _half_ulp')
def t_readers():
    print('J0 — real_14 를 임시 평문으로 풀어 리포 읽기 함수와 대조')
    import lhs_descriptor_harvest as H
    from lhs_perc_extract import read_atom_dump
    from lhs_contact_audit import _half_ulp, _sigfigs
    pa = write_copy(text_lines(R14_ATOM), 'r14_atom_plain.liggghts')
    pc = write_copy(text_lines(R14_CONT), 'r14_cont_plain.liggghts')
    A = J.read_atom_dump_frame(R14_ATOM)
    Cc = J.read_contact_dump_frame(R14_CONT)
    i1, i2, ar, hdr, xc = H.read_contact_dump(pc, extra_cols=('c_cpl[23]', 'c_cpl[9]'))
    chk('J0 접촉: id1 · id2 · c_cpl[22] · c_cpl[23] · c_cpl[9] = read_contact_dump (마지막 프레임 · 106,563 행)',
        np.array_equal(Cc['id1'], i1) and np.array_equal(Cc['id2'], i2) and np.array_equal(Cc['area'], ar)
        and np.array_equal(Cc['delta'], xc['c_cpl[23]']) and np.array_equal(Cc['pflag'], xc['c_cpl[9]']) and len(i1) == 106563)
    out, blo, bhi, bc = read_atom_dump(pa)
    chk('J0 원자: x · y · z · radius · type · 상자 · 플래그 = read_atom_dump (33,289 행)',
        np.array_equal(A['x'][:, 0], out['x']) and np.array_equal(A['x'][:, 2], out['z']) and np.array_equal(A['r'], out['radius'])
        and np.array_equal(A['types'], out['type']) and np.array_equal(A['box_lo'], blo) and np.array_equal(A['box_hi'], bhi)
        and tuple(A['box_flags']) == tuple(bc) and len(A['ids']) == 33289)
    toks = ['0.0250327', '1.74768e-06', '0.006', '0.0005', '0.00730768', '0.000908212', '2.06753e-07']
    S = max(6, max(_sigfigs(t) for t in toks))
    hv = J.half_ulp_tokens(np.array(toks), S)
    chk('J0 반폭 = lhs_contact_audit._half_ulp (토큰 문자열 · 파일 유효숫자 S)',
        all(float(hv[k]) == _half_ulp(t, S) for k, t in enumerate(toks)), repr(hv))
    chk('J0 덤프 유효숫자 S = 6 (원자 · 접촉) · scaffold 소수 자리 6 (반폭 5e−7 상자 단위)',
        A['sigfig'] == 6 and Cc['sigfig'] == 6 and J.read_scaffold_csv(R14_SCAF)['half'] == 5e-7,
        f"{A['sigfig']} {Cc['sigfig']} {J.read_scaffold_csv(R14_SCAF)['half']}")


# ═════════════════════════ J1 · J2 ═════════════════════════
@case('J1 real_14 — G-geo · G-frame 통과')
def t_real14():
    print('J1 — real_14 scaffold (457) ↔ atom 2,060,000 ↔ contact 2,060,000')
    jn = join_r14()
    chk('J1 상태 PASS · 거부 없음 · 종류 am_iface_join', jn['status'] == 'PASS' and jn['rejections'] == []
        and jn['kind'] == 'am_iface_join', repr(codes(jn)))
    g, f = jn['g_geo'], jn['g_frame']
    chk('J1 G-geo: scaffold 457 행 ↔ AM 원자 457 개 1:1 · 형 · 반경 일치 · 최대 위치 편차 / 허용폭 ≤ 1',
        g['n_scaffold'] == 457 and g['n_dump_am'] == 457 and g['n_matched'] == 457 and g['max_pos_ratio'] <= 1.0
        and g['max_radius_ratio'] <= 1.0, repr(g)[:400])
    chk('J1 G-frame: step 2,060,000 = 2,060,000 · 프레임 각 1 · 상자 같음 · 고아 id 0 · 원자 수 = 머리',
        f['atom_step'] == 2060000 and f['contact_step'] == 2060000 and f['atom_frames'] == 1 and f['contact_frames'] == 1
        and f['box_equal'] is True and f['n_orphan_rows'] == 0, repr(f)[:400])
    chk('J1 G-frame: pos1/pos2 = 원자 위치 (주기 영상 이동 행 수 기록 > 0) · δ 자기 일관 (최대 / 허용폭 < 1)',
        f['n_pos_mismatch'] == 0 and f['n_rows_image_shift'] > 0 and f['max_delta_pos_ratio'] < 1.0, repr(f)[:400])
    chk('J1 G-geo: AM–AM 접촉 660 행 (주기 이음매 70) · δ_dump ↔ δ_scaffold · A_dump ↔ lens 포괄 · 확실한 접촉 누락 0',
        g['n_dem_am_am'] == 660 and g['n_dem_am_am_seam'] == 70 and g['n_delta_scaffold_mismatch'] == 0
        and g['n_area_beyond'] == 0 and g['n_dem_contact_missing'] == 0, repr(g)[:400])
    chk('J1 기록: 파일 sha256 (풀린 바이트 = README 표) · scaffold 프레임 주장 = G-geo 만 · 재사용 없음',
        jn['files']['atom']['sha256_content'].startswith('079c85f1') and jn['files']['contact']['sha256_content'].startswith('a609ba94')
        and 'G-geo' in jn['scaffold_frame_claim'] and jn['geom_reuse'] is None, repr(jn['files'])[:300])
    chk('J1 인증 입자 = scaffold × 1000 µm · fp_particles = step3_sigma._iface_particles_fp · 지문 fp_join 자기 일관',
        len(jn['particles']['c_um']) == 457 and abs(float(jn['particles']['r_um'].max()) - 6.0) < 1e-12
        and jn['fp_particles'] == S3._iface_particles_fp(jn['particles']['c_um'], jn['particles']['r_um'], jn['particles']['t'])
        and S3.iface_join_fp(jn) == jn['fp_join'])


@case('J2 case15 — 형 지도 1 = AM_P · 2 = SE')
def t_case15():
    print('J2 — case15 scaffold (104) ↔ atom 1,710,000 ↔ contact 1,710,000')
    jn = J.am_iface_join(C15_SCAF, C15_ATOM, C15_CONT, type_map=C15_TMAP)
    chk('J2 상태 PASS · 104 ↔ 104 · step 1,710,000 · 거부 없음',
        jn['status'] == 'PASS' and jn['g_geo']['n_matched'] == 104 and jn['g_frame']['atom_step'] == 1710000
        and jn['rejections'] == [], repr(codes(jn)) + repr(jn['g_geo'])[:200])


# ═════════════════════════ J3 ═════════════════════════
@case('J3 한 줄 변조 → 거부')
def t_tamper():
    print('J3 — 임시 사본에 한 줄씩 변조 (커밋된 자료 무변경)')
    al, cl = text_lines(R14_ATOM), text_lines(R14_CONT)
    sl = text_lines(R14_SCAF)
    am = am_ids(al, R14_TMAP)
    #  ① 원자 덤프 AM 한 행 x + 1 nm (1e−6 sim)
    a2 = list(al); _id, k = am[0]
    v = a2[k].split(); v[2] = bump(v[2], 1e-6); a2[k] = ' '.join(v) + ' '
    jn = J.am_iface_join(R14_SCAF, write_copy(a2, 'a_shift.liggghts'), R14_CONT, type_map=R14_TMAP)
    chk('J3 ① 원자 AM 한 행 x + 1 nm → REJECT (G-geo 위치 · G-frame pos 불일치)',
        jn['status'] == 'REJECT' and 'pos_mismatch' in codes(jn)
        and any(c in codes(jn) for c in ('scaffold_row_unmatched', 'dump_am_unmatched')), repr(codes(jn)))
    #  ② 접촉 AM–AM 한 행 δ 부호 반전
    c2 = list(cl); k = first_am_am_row(cl, al, R14_TMAP)
    v = c2[k].split(); v[22] = g6(-float(v[22])); c2[k] = ' '.join(v) + ' '
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c2, 'c_dflip.liggghts'), type_map=R14_TMAP)
    chk('J3 ② 접촉 AM–AM 한 행 δ 부호 반전 → REJECT (δ 자기 일관 · δ ≤ 0 · δ_scaffold · 면적)',
        jn['status'] == 'REJECT' and {'delta_pos_mismatch', 'delta_nonpositive', 'delta_scaffold_mismatch'} <= set(codes(jn)),
        repr(codes(jn)))
    #  ③ 접촉 한 행 pos1 x + 1 nm
    c3 = list(cl); k = first_am_am_row(cl, al, R14_TMAP)
    v = c3[k].split(); v[0] = bump(v[0], 1e-6); c3[k] = ' '.join(v) + ' '
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c3, 'c_pos.liggghts'), type_map=R14_TMAP)
    chk('J3 ③ 접촉 한 행 pos1 x + 1 nm → REJECT (pos_mismatch)', jn['status'] == 'REJECT' and 'pos_mismatch' in codes(jn),
        repr(codes(jn)))
    #  ④ scaffold 한 행 x + 1 nm (6 째 소수 자리 +1)
    s4 = list(sl); k = next(i for i, ln in enumerate(s4) if ln and not ln.startswith('#'))
    v = s4[k].split(','); v[1] = f'{float(v[1]) + 1e-6:.6f}'; s4[k] = ','.join(v)
    jn = J.am_iface_join(write_copy(s4, 's_shift.csv'), R14_ATOM, R14_CONT, type_map=R14_TMAP)
    chk('J3 ④ scaffold 한 행 x + 1 nm → REJECT (G-geo 1:1 깨짐)',
        jn['status'] == 'REJECT' and any(c in codes(jn) for c in ('scaffold_row_unmatched', 'dump_am_unmatched')), repr(codes(jn)))
    #  ⑤ 접촉 AM–AM 한 행 면적 + 1 %
    c5 = list(cl); k = first_am_am_row(cl, al, R14_TMAP)
    v = c5[k].split(); v[21] = g6(float(v[21]) * 1.01); c5[k] = ' '.join(v) + ' '
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c5, 'c_area.liggghts'), type_map=R14_TMAP)
    chk('J3 ⑤ 접촉 AM–AM 한 행 c_cpl[22] + 1 % → REJECT (area_enclosure)', jn['status'] == 'REJECT' and 'area_enclosure' in codes(jn),
        repr(codes(jn)))
    #  ⑥ 접촉 덤프 상자 한 줄
    c6 = list(cl); k = item_index(c6, 'ITEM: BOX BOUNDS') + 1; c6[k] = '0 0.0500001'
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c6, 'c_box.liggghts'), type_map=R14_TMAP)
    chk('J3 ⑥ 접촉 덤프 상자 x 상한 바꿈 → REJECT (box_mismatch)', jn['status'] == 'REJECT' and 'box_mismatch' in codes(jn),
        repr(codes(jn)))
    #  ⑦ 고아 id
    c7 = list(cl); k = item_index(c7, 'ITEM: ENTRIES') + 1
    v = c7[k].split(); v[7] = '99999999'; c7[k] = ' '.join(v) + ' '
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c7, 'c_orphan.liggghts'), type_map=R14_TMAP)
    chk('J3 ⑦ 접촉 한 행 id2 = 없는 원자 → REJECT (orphan_id)', jn['status'] == 'REJECT' and 'orphan_id' in codes(jn), repr(codes(jn)))
    #  ⑧ 원자 덤프 두 프레임
    a8 = list(al) + [x for x in al if x != '']
    jn = J.am_iface_join(R14_SCAF, write_copy(a8, 'a_2frames.liggghts'), R14_CONT, type_map=R14_TMAP)
    chk('J3 ⑧ 원자 덤프 두 프레임 → REJECT (multi_frame)', jn['status'] == 'REJECT' and 'multi_frame' in codes(jn), repr(codes(jn)))
    #  ⑨ 접촉 AM–AM 한 행 삭제 (머리 개수도 맞춤) — 확실한 접촉이 덤프에서 빠짐
    c9 = list(cl); k = first_am_am_row(cl, al, R14_TMAP); del c9[k]
    kn = item_index(c9, 'ITEM: NUMBER OF ENTRIES') + 1; c9[kn] = str(int(c9[kn]) - 1)
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c9, 'c_drop.liggghts'), type_map=R14_TMAP)
    chk('J3 ⑨ 접촉 AM–AM 한 행 삭제 (머리 개수 맞춤) → REJECT (dem_contact_missing)',
        jn['status'] == 'REJECT' and 'dem_contact_missing' in codes(jn), repr(codes(jn)))
    #  ⑩ 머리 원자 수 ≠ 행 수
    a10 = list(al); kn = item_index(a10, 'ITEM: NUMBER OF ATOMS') + 1; a10[kn] = str(int(a10[kn]) + 1)
    jn = J.am_iface_join(R14_SCAF, write_copy(a10, 'a_count.liggghts'), R14_CONT, type_map=R14_TMAP)
    chk('J3 ⑩ 원자 덤프 머리 수 ≠ 행 수 → REJECT (count_mismatch)', jn['status'] == 'REJECT' and 'count_mismatch' in codes(jn),
        repr(codes(jn)))


# ═════════════════════════ N5′ ═════════════════════════
@case('N5′ reject_frame — 다른 step (위치 같음) 거부 · 선언된 재사용만 통과')
def t_n5():
    print('N5′ — 접촉 덤프 TIMESTEP 만 2,050,000 으로 (위치 · 나머지 그대로 = 정지 침대 모사)')
    cl = text_lines(R14_CONT)
    c2 = list(cl); k = item_index(c2, 'ITEM: TIMESTEP') + 1; c2[k] = '2050000'
    p = write_copy(c2, 'c_step.liggghts')
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, p, type_map=R14_TMAP)
    f = jn['g_frame']
    chk('N5′ 다른 step + 위치 같음 → REJECT (timestep_mismatch) · pos 불일치 0 (위치로는 못 가른다)',
        jn['status'] == 'REJECT' and codes(jn) == ['timestep_mismatch'] and f['n_pos_mismatch'] == 0, repr(codes(jn)))
    decl = {'atom_step': 2060000, 'contact_step': 2050000, 'reason': '시험 — 정지 침대의 기하 재사용 선언'}
    jr = J.am_iface_join(R14_SCAF, R14_ATOM, p, type_map=R14_TMAP, geom_reuse=decl)
    gr = jr.get('geom_reuse') or {}
    chk('N5′ 선언된 재사용 (두 step 기록) → PASS · geom_reuse = 선언 + 관측 step · accepted',
        jr['status'] == 'PASS' and gr.get('status') == 'accepted' and gr.get('declared', {}).get('contact_step') == 2050000
        and gr.get('observed') == {'atom_step': 2060000, 'contact_step': 2050000}, repr(gr))
    bad = J.am_iface_join(R14_SCAF, R14_ATOM, p, type_map=R14_TMAP, geom_reuse=dict(decl, contact_step=2040000))
    chk('N5′ 틀린 선언 (step 다름) → REJECT (geom_reuse_mismatch)', bad['status'] == 'REJECT' and 'geom_reuse_mismatch' in codes(bad),
        repr(codes(bad)))
    nn = J.am_iface_join(R14_SCAF, R14_ATOM, R14_CONT, type_map=R14_TMAP,
                         geom_reuse={'atom_step': 2060000, 'contact_step': 2060000, 'reason': 'x'})
    chk('N5′ 같은 step 인데 재사용 선언 → REJECT (geom_reuse_not_needed)', nn['status'] == 'REJECT' and 'geom_reuse_not_needed' in codes(nn),
        repr(codes(nn)))
    chk('N5′ 선언 모양 틀림 (step 없음) → TypeError', raises(lambda: J.am_iface_join(R14_SCAF, R14_ATOM, p, type_map=R14_TMAP,
                                                                                geom_reuse={'reason': 'x'}), (TypeError,)))


# ═════════════════════════ N1 ═════════════════════════
@case('N1 reject_dilate · 형 지도 필수')
def t_n1():
    print('N1 — dilate_z ≠ 1 (기하가 DEM 이 아님) · 형 지도 없음')
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, R14_CONT, type_map=R14_TMAP, dilate_z=1.0214)
    chk('N1 dilate_z 1.0214 → REJECT (dilate_z)', jn['status'] == 'REJECT' and 'dilate_z' in codes(jn), repr(codes(jn)))
    chk('N1 형 지도 없음 (None) → TypeError (기본값 없음 · 추측하지 않는다)',
        raises(lambda: J.am_iface_join(R14_SCAF, R14_ATOM, R14_CONT, type_map=None), (TypeError,)))
    chk('N1 형 지도에 AM 이 없음 → ValueError', raises(lambda: J.am_iface_join(R14_SCAF, R14_ATOM, R14_CONT, type_map={3: 'SE'}),
                                                   (ValueError,)))


# ═════════════════════════ J4 ═════════════════════════
def r14_ledger(vox=0.4, bridge=None):
    jn = join_r14()
    c, r, t = jn['particles']['c_um'], jn['particles']['r_um'], jn['particles']['t']
    hi = (50.0, 50.0, float((c[:, 2] + r).max()))
    sid, pid = S3.rasterize(c, r, t, None, None, (0.0, 0.0, 0.0), hi, vox, bridge_um=bridge)
    L = S3.am_iface_ledger(c, r, t, sid, sid, (0.0, 0.0, 0.0), vox, delta_bound_um=jn['g_geo']['delta_bound_um'], bridge_um=bridge)
    return sid, L


RT3 = {'AM_S|AM_S': 1e-3, 'AM_S|AM_P': 1e-3, 'AM_P|AM_P': 1e-3}
LAWS = dict(gap_law='cut', unreg_law='cut', ambiguous_arm='cut')


@case('J4 계획 기록 — iface_join · iface_geom_reuse (요청할 때만)')
def t_plan():
    print('J4 — real_14 AM-only raster (vox 0.4 · 기본 브리지) · 같은 원장으로 join 유무 계획')
    sid, L = r14_ledger()
    jn = join_r14()
    P0 = S3.am_iface_plan(L, RT3, **LAWS)
    P1 = S3.am_iface_plan(L, RT3, join=jn, **LAWS)
    r0, r1 = P0['record'], P1['record']
    chk('J4 join=None: iface_join None · iface_geom_reuse None · 상태 문구 = 조인 요청 없음',
        r0['iface_join'] is None and r0['iface_geom_reuse'] is None and '요청 없음' in r0['iface_join_status'], repr(r0['iface_join_status']))
    chk('J4 join 통과: 거부 추가 없음 · 계획 행 지문 같음 (조인은 출처 증명만 · σ 경로 무변경)',
        codes(P1) == codes(P0) and P1['fp_rows'] == P0['fp_rows'], f'{codes(P0)} {codes(P1)}')
    ij = r1['iface_join'] or {}
    chk('J4 기록 iface_join: 상태 PASS · G-geo · G-frame 결과 · 파일 sha256 · step · fp_join · scaffold 프레임 주장',
        ij.get('status') == 'PASS' and 'g_geo' in ij.get('gates', {}) and 'g_frame' in ij.get('gates', {})
        and ij.get('files', {}).get('contact', {}).get('sha256_content', '').startswith('a609ba94')
        and ij.get('steps') == {'atom': 2060000, 'contact': 2060000} and ij.get('fp_join') == jn['fp_join']
        and 'G-geo' in ij.get('scaffold_frame_claim', ''), repr(ij)[:400])
    chk('J4 iface_join_status = 통과 문구 (면적 원천 scaffold lens 그대로 표지) · iface_area_source 그대로 · iface_geom_reuse None',
        '통과' in r1['iface_join_status'] and 'scaffold lens' in r1['iface_join_status']
        and r1['iface_area_source'] == r0['iface_area_source'] and r1['iface_geom_reuse'] is None, repr(r1['iface_join_status']))
    other = {k: v for k, v in r1.items() if k not in ('iface_join', 'iface_join_status', 'iface_geom_reuse')}
    base = {k: v for k, v in r0.items() if k not in ('iface_join', 'iface_join_status', 'iface_geom_reuse')}
    chk('J4 그 밖의 기록 키 · 값은 join 유무와 같다', repr(other) == repr(base))
    xc = ij.get('ledger_crosscheck') or {}
    chk('J4 원장 ↔ DEM 접촉 대조 (보고만): 부류별 DEM 포함 수 · 이음매 70 · 원장 미등록 DEM 쌍 0',
        'by_class' in xc and xc.get('n_dem_seam') == 70 and xc.get('n_dem_not_registered') == 0, repr(xc)[:400])
    #  실패 · 다른 입자 · 변조
    bad = dict(jn); bad['status'] = 'REJECT'; bad['rejections'] = [{'code': 'pos_mismatch', 'gate': 'G-frame', 'n': 1}]
    bad['fp_join'] = S3.iface_join_fp(bad)
    Pb = S3.am_iface_plan(L, RT3, join=bad, **LAWS)
    chk('J4 실패한 조인 → join_gate_failed 거부 · 정량 솔브 거부',
        'join_gate_failed' in codes(Pb) and raises(lambda: quiet(S3.solve_sigma_z, sid, S3.electronic_sigma_table(0.01, 0.005, 100.0, 10.0, 250.0),
                                                                0.4, iface=Pb)), repr(codes(Pb)))
    j15 = J.am_iface_join(C15_SCAF, C15_ATOM, C15_CONT, type_map=C15_TMAP)
    Pm = S3.am_iface_plan(L, RT3, join=j15, **LAWS)
    chk('J4 다른 침대의 조인 (case15 → real_14 원장) → join_particles_mismatch 거부', 'join_particles_mismatch' in codes(Pm), repr(codes(Pm)))
    tm = dict(jn); tm['g_geo'] = dict(jn['g_geo'], n_matched=999)
    Pt = S3.am_iface_plan(L, RT3, join=tm, **LAWS)
    chk('J4 만든 뒤 바뀐 조인 (지문 그대로) → join_record_tampered 거부', 'join_record_tampered' in codes(Pt), repr(codes(Pt)))
    chk('J4 조인이 아닌 것 → TypeError', raises(lambda: S3.am_iface_plan(L, RT3, join={'kind': 'x'}, **LAWS), (TypeError,)))


def main():
    global S3, S3_PATH, J, TMP
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--s3', default=os.path.join(SCRIPTS, 'step3_sigma.py'))
    a = ap.parse_args()
    S3_PATH = os.path.abspath(a.s3)
    spec = importlib.util.spec_from_file_location('step3_sigma', S3_PATH)
    S3 = importlib.util.module_from_spec(spec)
    sys.modules['step3_sigma'] = S3
    spec.loader.exec_module(S3)
    print(f'step3_sigma = {S3_PATH}')
    try:
        import rint_iface_join as _J
        J = _J
    except Exception as e:                              # noqa: BLE001 — 고치기 전 (모듈 없음) 도 사례 단위로 기록
        print(f'  (rint_iface_join import 실패: {type(e).__name__}: {e})')
        J = None
    TMP = tempfile.mkdtemp(prefix='rint_join_test_')
    try:
        for tag, fn in CASES:
            print(f'\n── {tag}')
            try:
                if J is None:
                    raise ImportError('rint_iface_join 없음')
                fn()
            except Exception as e:                      # noqa: BLE001
                chk(f'{tag}: 실행', False, f'{type(e).__name__}: {e}')
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
