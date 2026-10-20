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
  ── RIMP-02 · 03 (Codex 10-14 · 판정문 §3 · §4 · 수정 계획 Q2 (가) — 새 소비자에서 엄격 · 봉인 helper 무변경) ──
  J5  입구 검사 — real_14 한 칸씩 (Codex 행 = 첫 AM–AM 행 · id 1 · 201): pos1.x · δ · A = NaN · A 음수 · A inf · 반경 ≤ 0 ·
      기울어진 상자 (xy xz yz · 다른 tilt · 같은 tilt) · 상자 lo ≥ hi · step 2060000.9 · id · type · 머리 수 비정수 → 사유별 거부
  J6  형식 — 6 자리 `%g` 생산 포맷만 (16 자리 균일 · +1 ppm · 끝 0 덧붙인 토큰 한 개 = 거부) · 정상 real_14 · case15 = g6
  J7  미인증 면적 — `%g` 합성 근동심 쌍 (d 하한 ≤ 0) 의 면적 100 sim² · 참 면적 둘 다 PASS 아님 (area_uncertified) · 양성 합성 PASS
  J8  소비 경로 — 합성 조인 → 원장 → 계획 (join=…) → 정량 관문: 변이마다 거부 · 양성 통과
  J9  양성 유지 기록 — real_14 · case15 전 AM–AM 행 인증 (tested = 행 수) · 음수 면적 = AM–AM 밖 행만 (case15 AM_P–SE 2 행 · 인증 대상 밖)
  ── RIMPR-01 · 02 (Codex 10-15 · 판정문 docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md §2 · §3 — 시험 먼저) ──
  J10 파서 전수 소비 — Codex 반례 (블록 안 24 열 접촉 행 · 7 열 원자 행 · 블록 끝 짧은 행 · 필수 열 중복 (뒤 열 nan) · step `100 0.9` ·
      count `1 garbage`) + 같은 뿌리 (TIMESTEP 절 둘째 줄 · 줄 안 VT · 모르는 ITEM 절 · 절 두 번 · BOX BOUNDS 넷째 줄 · 프레임 앞 줄 ·
      TIMESTEP · NUMBER OF 머리 줄 뒤 토큰) →
      입구 REJECT · 계획 join_gate_failed · 정량 관문 거부 · 양성 차단 대조 (폭 정상 중복 행 = 그대로 REJECT) · 빈 줄 처리 보존 (옛 판과 같은
      결과 — 머리 바로 다음 · 경계 줄 사이 빈 줄 = REJECT · 절 끝 · 행 절 안 빈 줄 = PASS) · D19 양성 · real_14 전 행 소비
  J11 float64 입구 — scaffold 반경 · 좌표 1e309 · 고정소수 ±10^309 (Decimal 유한 · float64 무한) · µm 변환 넘침 · int64 넘는 정수 토큰
      (id · type · step) → 입구 REJECT (구조화 · 예외 아님) · 계획 · 정량 관문 거부 · int64 최댓값 id = PASS
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


# ═════════════════════════ RIMP-02 · 03 (Codex 10-14) ═════════════════════════
def codex_am_am_row(cl, al, tmap):
    """Codex `join_adversarial.py` 의 행 — 접촉 덤프에서 두 id 가 모두 AM 인 **첫** 행 (주기 영상 여부 무관 · real_14 = 22 째 줄 · id 1 · 201)."""
    ia = item_index(al, 'ITEM: ATOMS')
    kind = {}
    k = ia + 1
    while k < len(al) and al[k].strip() and not al[k].startswith('ITEM:'):
        v = al[k].split()
        kind[int(v[0])] = tmap.get(int(v[1]))
        k += 1
    ic = item_index(cl, 'ITEM: ENTRIES')
    for k in range(ic + 1, len(cl)):
        v = cl[k].split()
        if len(v) >= 23 and kind.get(int(v[6])) in ('AM_P', 'AM_S') and kind.get(int(v[7])) in ('AM_P', 'AM_S'):
            return k
    raise AssertionError('AM–AM 행이 없다')


def put(lines, k, col, tok):
    v = lines[k].split(); v[col] = tok; lines[k] = ' '.join(v)
    return lines


def tilt_box(lines, tilts):
    """BOX BOUNDS 머리를 삼사정계 꼴 (`xy xz yz` + 플래그) 로 · 경계 줄마다 tilt 토큰 하나 (Codex 꼴)."""
    i = item_index(lines, 'ITEM: BOX BOUNDS')
    flags = lines[i].split()[-3:]
    lines[i] = 'ITEM: BOX BOUNDS xy xz yz ' + ' '.join(flags)
    for k in range(3):
        lines[i + 1 + k] = lines[i + 1 + k] + ' ' + tilts[k]
    return lines


def synth(tag, *, fmt='g6', distance=0.0015, area=None, badpos=None, baddelta=None, radius=0.001, tilts=None, edit=None):
    """두 AM_P 구 합성 (Codex `join_synthetic.py` 꼴 · 상자 단위) — fmt 'g6' = `%g` (생산 포맷) · '16' = `%.15e` (16 유효숫자 균일).
    edit = 쓰기 직전 줄 목록 [scaffold, atom, contact] 을 고치는 함수 (RIMPR-01 · 02 반례 — 파일 줄 단위 변이 · 기본 None = 그대로).
    → (scaffold, atom, contact) 경로 · 참 면적 (lens_geometry)."""
    from lens_geometry import intersection_disc_area
    c = np.array([[0.002, 0.002, 0.002], [0.002 + distance, 0.002, 0.002]])
    delta = 2.0 * radius - distance
    exact = intersection_disc_area(radius, radius, delta)
    area = exact if area is None else area
    f = (lambda x: '%g' % float(x)) if fmt == 'g6' else (lambda x: f'{float(x):.15e}')
    box = ['ITEM: BOX BOUNDS ff ff ff', '0 0.01', '0 0.01', '0 0.01']
    at = ['ITEM: TIMESTEP', '100', 'ITEM: NUMBER OF ATOMS', '2'] + box + ['ITEM: ATOMS id type x y z radius']
    at += [f'{i + 1} 1 ' + ' '.join(f(v) for v in [*c[i], radius]) for i in range(2)]
    tok = [*map(f, c[0]), *map(f, c[1]), '1', '2', '0'] + ['0'] * 12 + [f(area) if not isinstance(area, str) else area, f(delta)]
    if badpos is not None:
        tok[0] = badpos
    if baddelta is not None:
        tok[22] = baddelta
    ct = (['ITEM: TIMESTEP', '100', 'ITEM: NUMBER OF ENTRIES', '1'] + box
          + ['ITEM: ENTRIES ' + ' '.join(f'c_cpl[{i}]' for i in range(1, 24)), ' '.join(tok)])
    if tilts is not None:
        at, ct = tilt_box(at, (tilts[0], '0', '0')), tilt_box(ct, (tilts[1], '0', '0'))
    sc = [','.join(['1', *(f'{x:.12f}' for x in [*c[i], radius])]) for i in range(2)]
    if edit is not None:
        edit([sc, at, ct])
    paths = []
    for suffix, lines in (('sc.csv', sc), ('atom.dump', at), ('contact.dump', ct)):
        paths.append(write_copy(lines, f'syn_{tag}_{suffix}'))
    return tuple(paths), exact


TM1 = {1: 'AM_P'}


@case('J5 입구 검사 — 비유한 · 음수 · 비정수 · 기울어진 상자 (RIMP-02)')
def t_entrance():
    print('J5 — real_14 임시 사본 한 칸씩 (Codex 행 = 첫 AM–AM 행) · 사유별 거부 (고치기 전 = PASS)')
    al, cl = text_lines(R14_ATOM), text_lines(R14_CONT)
    k = codex_am_am_row(cl, al, R14_TMAP)
    v = cl[k].split()
    chk('J5 Codex 행 = id 1 · 201 · pos1.x 0.0250327 · A 1.8247e−06 · δ 0.000199496 (판정문 §3-1)',
        (v[6], v[7], v[0], v[21], v[22]) == ('1', '201', '0.0250327', '1.8247e-06', '0.000199496'), repr(v[:8] + v[21:23]))
    for tag, col, tok, want in (('pos1.x NaN', 0, 'nan', 'nonfinite_value'), ('δ NaN', 22, 'nan', 'nonfinite_value'),
                                ('A NaN', 21, 'nan', 'nonfinite_value'), ('A inf', 21, 'inf', 'nonfinite_value'),
                                ('A 음수 (−1.8247e−06)', 21, '-1.8247e-06', 'area_negative'),
                                ('id2 비정수 (201.0)', 7, '201.0', 'int_token')):
        c2 = put(list(cl), k, col, tok)
        jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c2, 'j5.liggghts'), type_map=R14_TMAP)
        chk(f'J5 접촉 {tag} → REJECT ({want})', jn['status'] == 'REJECT' and want in codes(jn), repr(codes(jn)))
    #  상자 — 다른 tilt (앞 두 경계 열 같음 · Codex) · 같은 tilt (지원 밖 = 명시 거부) · lo ≥ hi
    for tag, ta, tc in (('다른 tilt (원자 0.001 · 접촉 0.002)', '0.001', '0.002'), ('같은 tilt (둘 다 0.001)', '0.001', '0.001')):
        jn = J.am_iface_join(R14_SCAF, write_copy(tilt_box(list(al), (ta, '0', '0')), 'j5_ta.liggghts'),
                             write_copy(tilt_box(list(cl), (tc, '0', '0')), 'j5_tc.liggghts'), type_map=R14_TMAP)
        chk(f'J5 기울어진 상자 머리 (xy xz yz) {tag} → REJECT (box_tilted · 직교 상자만 지원)',
            jn['status'] == 'REJECT' and 'box_tilted' in codes(jn), repr(codes(jn)))
    a3, c3 = list(al), list(cl)
    for L_ in (a3, c3):
        L_[item_index(L_, 'ITEM: BOX BOUNDS') + 1] = '0.05 0'
    jn = J.am_iface_join(R14_SCAF, write_copy(a3, 'j5_ab.liggghts'), write_copy(c3, 'j5_cb.liggghts'), type_map=R14_TMAP)
    chk('J5 상자 x 경계 lo ≥ hi (두 덤프 같게) → REJECT (box_format)', jn['status'] == 'REJECT' and 'box_format' in codes(jn), repr(codes(jn)))
    #  정수 — step · 원자 type · 머리 수
    c4 = list(cl); c4[item_index(c4, 'ITEM: TIMESTEP') + 1] = '2060000.9'
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c4, 'j5_step.liggghts'), type_map=R14_TMAP)
    chk('J5 접촉 step 2060000.9 → REJECT (int_token) · step 을 2060000 으로 줄이지 않는다',
        jn['status'] == 'REJECT' and 'int_token' in codes(jn) and jn['steps']['contact'] != 2060000, repr(codes(jn)) + repr(jn['steps']))
    a5 = list(al); am = am_ids(al, R14_TMAP); _id, ka = am[0]
    a5 = put(a5, ka, 1, a5[ka].split()[1] + '.0')
    jn = J.am_iface_join(R14_SCAF, write_copy(a5, 'j5_type.liggghts'), R14_CONT, type_map=R14_TMAP)
    chk('J5 원자 type 비정수 (1.0) → REJECT (int_token)', jn['status'] == 'REJECT' and 'int_token' in codes(jn), repr(codes(jn)))
    a6 = list(al); a6[item_index(a6, 'ITEM: NUMBER OF ATOMS') + 1] = '33289.0'
    jn = J.am_iface_join(R14_SCAF, write_copy(a6, 'j5_cnt.liggghts'), R14_CONT, type_map=R14_TMAP)
    chk('J5 원자 머리 수 비정수 (33289.0) → REJECT (int_token)', jn['status'] == 'REJECT' and 'int_token' in codes(jn), repr(codes(jn)))
    #  반경 ≤ 0 (AM 원자 · %g 토큰)
    a7 = put(list(al), ka, 5, '-0.006')
    jn = J.am_iface_join(R14_SCAF, write_copy(a7, 'j5_rad.liggghts'), R14_CONT, type_map=R14_TMAP)
    chk('J5 원자 반경 −0.006 → REJECT (nonpositive_radius)', jn['status'] == 'REJECT' and 'nonpositive_radius' in codes(jn), repr(codes(jn)))
    #  scaffold 비유한
    s8 = list(text_lines(R14_SCAF)); ks = next(i for i, ln in enumerate(s8) if ln and not ln.startswith('#'))
    vs = s8[ks].split(','); vs[1] = 'nan'; s8[ks] = ','.join(vs)
    jn = J.am_iface_join(write_copy(s8, 'j5_scaf.csv'), R14_ATOM, R14_CONT, type_map=R14_TMAP)
    chk('J5 scaffold 한 행 x = nan → REJECT (nonfinite_value · 예외 아님)', jn['status'] == 'REJECT' and 'nonfinite_value' in codes(jn),
        repr(codes(jn)))


@case('J6 형식 — 6 자리 %g 생산 포맷만 (RIMP-03)')
def t_format():
    print('J6 — 16 자리 균일 합성 (Codex) · 끝 0 덧붙인 토큰 하나 (값 같음 · Codex join_global_precision) → 거부 · 정상 = g6')
    (sc, at, ct), exact = synth('f16', fmt='16')
    jn = J.am_iface_join(sc, at, ct, type_map=TM1)
    chk('J6 16 자리 균일 (참 면적) → REJECT (numeric_format — 6 자리 %g 생산 포맷만 지원)',
        jn['status'] == 'REJECT' and 'numeric_format' in codes(jn), repr(codes(jn)))
    (sc, at, ct), _ = synth('f16p', fmt='16', area=exact * (1.0 + 1e-6))
    jn = J.am_iface_join(sc, at, ct, type_map=TM1)
    chk('J6 16 자리 균일 + 면적 +1 ppm (판정문 §4 · A 1.374448160392321e−06) → REJECT (PASS 아님)',
        jn['status'] == 'REJECT' and 'numeric_format' in codes(jn), repr(codes(jn)))
    al, cl = text_lines(R14_ATOM), text_lines(R14_CONT)
    i = item_index(al, 'ITEM: ATOMS') + 1
    a2 = put(list(al), i, 2, al[i].split()[2] + '0000000000')
    jn = J.am_iface_join(R14_SCAF, write_copy(a2, 'j6_a.liggghts'), R14_CONT, type_map=R14_TMAP)
    chk('J6 원자 첫 행 x 끝 0 덧붙임 (0.0250327 → 0.02503270000000000 · 값 같음) → REJECT (numeric_format)',
        jn['status'] == 'REJECT' and 'numeric_format' in codes(jn), repr(codes(jn)))
    i = item_index(cl, 'ITEM: ENTRIES') + 1
    c2 = put(list(cl), i, 0, cl[i].split()[0] + '0000000000')
    jn = J.am_iface_join(R14_SCAF, R14_ATOM, write_copy(c2, 'j6_c.liggghts'), type_map=R14_TMAP)
    chk('J6 접촉 첫 행 pos1.x 끝 0 덧붙임 → REJECT (numeric_format · 전역 S 를 올려 다른 토큰의 폭을 줄이지 않는다)',
        jn['status'] == 'REJECT' and 'numeric_format' in codes(jn), repr(codes(jn)))
    jr = join_r14()
    fm = (jr.get('entrance') or {}).get('format') or {}
    chk('J6 정상 real_14: 형식 = g6 (원자 · 접촉) · 면적 helper 의 고정 6 자리 = 파일 유효숫자 6 (같은 가정)',
        fm.get('rule') == 'g6' and fm.get('atom_ok') is True and fm.get('contact_ok') is True
        and jr['g_frame']['atom_sigfig'] == jr['g_frame']['contact_sigfig'] == 6 == jr['g_geo'].get('area_sigfig_assumed'),
        repr(fm) + repr(jr['g_geo'].get('area_sigfig_assumed')))


@case('J7 미인증 면적 — PASS 와 분리 (RIMP-02)')
def t_uncertified():
    print('J7 — `%g` 합성 근동심 쌍 (중심 거리 1e−8 sim · δ 0.00199999) — 면적 포괄 미인증 (d 하한 ≤ 0) 행')
    (sc, at, ct), exact = synth('g6ok', fmt='g6')
    jn = J.am_iface_join(sc, at, ct, type_map=TM1)
    chk('J7 양성: `%g` 합성 (중심 거리 0.0015 · δ 0.0005) → PASS · AM–AM 1 행 인증 (tested 1)',
        jn['status'] == 'PASS' and jn['g_geo']['n_area_tested'] == 1 and jn['g_geo']['n_dem_am_am'] == 1, repr(codes(jn)))
    for tag, area in (('면적 100 sim² (Codex)', 100.0), ('참 면적', None)):
        (sc, at, ct), ex = synth('unc' + ('100' if area else 'ok'), fmt='g6', distance=1e-8, area=area)
        jn = J.am_iface_join(sc, at, ct, type_map=TM1)
        chk(f'J7 근동심 {tag} → REJECT (area_uncertified · 포괄 밖 0 ≠ 전 행 인증)',
            jn['status'] == 'REJECT' and 'area_uncertified' in codes(jn) and jn['g_geo'].get('n_area_uncertified') == 1, repr(codes(jn)))


@case('J8 소비 경로 — 조인 → 원장 → 계획 → 정량 관문 (RIMP-02 · 03)')
def t_consumer_reach():
    print('J8 — 합성 0.25 µm raster (Codex join_synthetic 꼴) · 변이 조인마다 계획 · 정량 관문')
    (sc, at, ct), exact = synth('base', fmt='g6')
    base = J.am_iface_join(sc, at, ct, type_map=TM1)
    c, r, t = (base['particles'][k] for k in ('c_um', 'r_um', 't'))
    sid, _pid = quiet(S3.rasterize, c, r, t, None, None, (0, 0, 0), (6, 4, 4), 0.25, bridge_um=0.24)
    L = S3.am_iface_ledger(c, r, t, sid, sid, (0, 0, 0), 0.25, delta_bound_um=base['g_geo']['delta_bound_um'], bridge_um=0.24)
    law = dict(gap_law='cut', unreg_law='cut', ambiguous_arm='cut')
    P = S3.am_iface_plan(L, {'AM_P|AM_P': 1e-3}, join=base, **law)
    chk('J8 양성: 합성 조인 PASS → 계획 거부 없음 · 정량 관문 통과', base['status'] == 'PASS' and P['rejections'] == []
        and S3.iface_require_quantitative(P, sid=sid) is P, repr(codes(P)))
    for tag, kw in (('면적 음수', dict(area=-exact)), ('면적 NaN', dict(area='nan')), ('pos1.x NaN', dict(badpos='nan')),
                    ('δ NaN', dict(baddelta='nan')), ('16 자리 + 1 ppm', dict(fmt='16', area=exact * (1.0 + 1e-6))),
                    ('다른 tilt 상자', dict(tilts=('0.001', '0.002')))):
        (sc2, at2, ct2), _ = synth('m', **kw)
        jm = J.am_iface_join(sc2, at2, ct2, type_map=TM1)
        Pm = S3.am_iface_plan(L, {'AM_P|AM_P': 1e-3}, join=jm, **law)
        chk(f'J8 {tag}: 조인 REJECT → 계획 join_gate_failed → 정량 관문 거부 (고치기 전 = 셋 다 통과)',
            jm['status'] == 'REJECT' and 'join_gate_failed' in codes(Pm)
            and raises(lambda: S3.iface_require_quantitative(Pm, sid=sid)), f"{jm['status']} {codes(jm)} {codes(Pm)}")


@case('J9 양성 유지 — 전 AM–AM 행 인증 · 음수 면적 = 인증 대상 밖 행만 (RIMP-02)')
def t_positive_scope():
    print('J9 — real_14 · case15 의 AM–AM 행 전부 tested · 음수 · 미인증 0 · case15 의 음수 면적 2 행 = AM_P–SE (조인 면적 인증 밖)')
    jr = join_r14()
    g = jr['g_geo']
    chk('J9 real_14: AM–AM 660 행 전부 인증 (tested 660 · 음수 0 · 미인증 0 · area_all_certified) · 음수 면적 (AM–AM 밖) 0',
        g['n_area_tested'] == g['n_dem_am_am'] == 660 and g.get('n_area_negative') == 0 and g['n_area_uncertified'] == 0
        and g.get('area_all_certified') is True and g.get('n_area_negative_not_am_am') == 0, repr({k: g.get(k) for k in (
            'n_area_tested', 'n_dem_am_am', 'n_area_negative', 'n_area_uncertified', 'area_all_certified', 'n_area_negative_not_am_am')}))
    j15 = J.am_iface_join(C15_SCAF, C15_ATOM, C15_CONT, type_map=C15_TMAP)
    g = j15['g_geo']
    chk('J9 case15: PASS · AM–AM 119 행 전부 인증 · 음수 면적 2 행 = AM–AM 밖 (AM_P–SE · 조인이 인증하지 않는 행 — 기록만)',
        j15['status'] == 'PASS' and g['n_area_tested'] == g['n_dem_am_am'] == 119 and g.get('n_area_negative') == 0
        and g.get('area_all_certified') is True and g.get('n_area_negative_not_am_am') == 2, repr(codes(j15)) + repr({k: g.get(k) for k in (
            'n_area_tested', 'n_dem_am_am', 'n_area_negative', 'area_all_certified', 'n_area_negative_not_am_am')}))
    e = jr.get('entrance') or {}
    chk('J9 기록 entrance: 규칙 문구 · 비유한 0 · 비정수 0 · 지원 상자 (직교 · pp pp ff) · 형식 g6',
        e.get('status') == 'PASS' and e.get('n_nonfinite') == 0 and e.get('n_int_token_bad') == 0
        and e.get('box') == {'atom': 'orthogonal', 'contact': 'orthogonal'} and (e.get('format') or {}).get('rule') == 'g6', repr(e)[:400])


# ═════════════════════════ RIMPR-01 · 02 (Codex 10-15) ═════════════════════════
LAW3 = dict(gap_law='cut', unreg_law='cut', ambiguous_arm='cut')
RT_PP = {'AM_P|AM_P': 1e-3}


def consumer_ctx():
    """합성 기준 조인 → 0.25 µm raster → 원장 (J8 · Codex join_independent 꼴) — 변이 조인을 **같은 원장**의 계획 · 정량 관문에 넣는다."""
    (sc, at, ct), _ = synth('ctx', fmt='g6')
    base = J.am_iface_join(sc, at, ct, type_map=TM1)
    c, r, t = (base['particles'][k] for k in ('c_um', 'r_um', 't'))
    sid, _pid = quiet(S3.rasterize, c, r, t, None, None, (0, 0, 0), (6, 4, 4), 0.25, bridge_um=0.24)
    L = S3.am_iface_ledger(c, r, t, sid, sid, (0, 0, 0), 0.25, delta_bound_um=base['g_geo']['delta_bound_um'], bridge_um=0.24)
    return base, sid, L


def try_join(paths, **kw):
    """조인 실행 — 예외도 결과로 (고치기 전 코드는 일부 반례에서 ValueError · OverflowError 로 끝난다 · 사례 단위로 기록)."""
    try:
        return J.am_iface_join(*paths, type_map=TM1, **kw), None
    except Exception as e:                                  # noqa: BLE001
        return None, f'{type(e).__name__}: {e}'


def entrance_reject(jm, err, want):
    """조인 = REJECT · 사유 `want` 가 **입구** (관문 계산 전) 에서 · 관문 = 계산 안 함 (skipped)."""
    if jm is None:
        return False, err
    ok = (jm['status'] == 'REJECT' and any(x['code'] == want and x['gate'] == 'entrance' for x in jm['rejections'])
          and 'skipped' in jm['g_geo'] and 'skipped' in jm['g_frame'])
    return ok, f"{jm['status']} {[(x['code'], x['gate']) for x in jm['rejections']]}"


def consumer_blocks(jm, sid, L):
    """후속 계획이 조인 REJECT 를 이어받는가 — 계획 join_gate_failed · 정량 관문 (vox 0.25 = 원장 격자) 거부."""
    if jm is None:
        return False, '조인 예외 — 계획에 넣을 기록 없음'
    Pm = S3.am_iface_plan(L, RT_PP, join=jm, **LAW3)
    ok = 'join_gate_failed' in codes(Pm) and raises(lambda: S3.iface_require_quantitative(Pm, sid=sid, vox=0.25))
    return ok, repr(codes(Pm))


def _dup_col(item_row, col):
    """열 머리에 이미 있는 필수 열 `col` 을 하나 더 (뒤 열 값 = nan · Codex duplicate_radius_column 꼴)."""
    def ed(Ls):
        k = item_row[0]
        Ls[k][item_row[1]] += ' ' + col
        for r_ in item_row[2]:
            Ls[k][r_] += ' nan'
    return ed


def _set(fi, row, val):
    def ed(Ls):
        Ls[fi][row] = val
    return ed


def _ins(fi, row, val_of):
    def ed(Ls):
        Ls[fi].insert(row, val_of(Ls))
    return ed


@case('J10 조인 파서 전수 소비 — 버린 행 · 열 · 토큰 = 입구 REJECT · 후속 계획 이어받음 (RIMPR-01)')
def t_parser_complete():
    print('J10 — 합성 두 구 (r 0.001 · 거리 0.0015 · δ 0.0005 sim) 파일 줄 변이 · 고치기 전 = 전부 PASS / 정량 ACCEPT (판정문 §2)')
    base, sid, L = consumer_ctx()
    Pb = S3.am_iface_plan(L, RT_PP, join=base, **LAW3)
    chk('J10 양성: 합성 기준 조인 PASS · 계획 거부 없음 · 정량 관문 (vox 0.25) 통과',
        base['status'] == 'PASS' and Pb['rejections'] == [] and S3.iface_require_quantitative(Pb, sid=sid, vox=0.25) is Pb,
        repr(codes(base)) + repr(codes(Pb)))
    #  줄 번호 (synth): atom 9 · 10 = 행 · 8 = ATOMS 머리 · 1 = step · 3 = 머리 수 / contact 9 = 행 · 8 = ENTRIES 머리 · 1 · 3 / scaffold 0 · 1
    codex = (
        ('접촉 24 열 행을 블록 안 정상 행 앞에 (선언 1 · 실제 2 · Codex)', _ins(2, 9, lambda Ls: Ls[2][9] + ' 0'), 'row_width'),
        ('원자 7 열 행을 블록 안 정상 행들 앞에 (선언 2 · 실제 3 · Codex)', _ins(1, 9, lambda Ls: Ls[1][9] + ' 0'), 'row_width'),
        ('접촉 블록 끝에 4 토큰 행 (Codex malformed_extra_contact_row)', lambda Ls: Ls[2].append('0.002 0.002 nan malformed'), 'row_width'),
        ('원자 블록 끝에 3 토큰 행 (Codex malformed_extra_atom_row)', lambda Ls: Ls[1].append('3 1 nan'), 'row_width'),
        ('원자 radius 필수 열 중복 (뒤 열 nan · 폭 7 = 7 · Codex)', _dup_col((1, 8, (9, 10)), 'radius'), 'header_duplicate'),
        ('접촉 c_cpl[22] 필수 열 중복 (뒤 열 nan)', _dup_col((2, 8, (9,)), 'c_cpl[22]'), 'header_duplicate'),
        ('접촉 step 줄 `100 0.9` (Codex)', _set(2, 1, '100 0.9'), 'int_token'),
        ('접촉 count 줄 `1 garbage` (Codex)', _set(2, 3, '1 garbage'), 'int_token'),
        ('원자 step 줄 `100 0.9`', _set(1, 1, '100 0.9'), 'int_token'),
        ('원자 count 줄 `2 garbage`', _set(1, 3, '2 garbage'), 'int_token'),
    )
    same_root = (
        ('접촉 TIMESTEP 절 둘째 줄 `0.9` (절 몸통 전수)', _ins(2, 2, lambda Ls: '0.9'), 'int_token'),
        ('접촉 step 줄 `100<VT>0.9` (splitlines 가 줄을 쪼갠다)', _set(2, 1, '100\x0b0.9'), 'int_token'),
        ('접촉 프레임 안 모르는 ITEM 절 (`ITEM: FOO` · `1 2 3`)', lambda Ls: Ls[2].__setitem__(slice(8, 8), ['ITEM: FOO', '1 2 3']),
         'frame_layout'),
        ('접촉 NUMBER OF ENTRIES 절 두 번', lambda Ls: Ls[2].__setitem__(slice(4, 4), ['ITEM: NUMBER OF ENTRIES', '1']), 'frame_layout'),
        ('접촉 BOX BOUNDS 절 넷째 줄 (`0 0.01`)', _ins(2, 8, lambda Ls: '0 0.01'), 'box_format'),
        ('접촉 첫 프레임 앞 비어 있지 않은 줄', _ins(2, 0, lambda Ls: 'junk'), 'frame_layout'),
        ('접촉 TIMESTEP 머리 줄 뒤 토큰 (`ITEM: TIMESTEP 0.9`)', _set(2, 0, 'ITEM: TIMESTEP 0.9'), 'frame_layout'),
        ('원자 NUMBER OF ATOMS 머리 줄 뒤 토큰 (`ITEM: NUMBER OF ATOMS 7`)', _set(1, 2, 'ITEM: NUMBER OF ATOMS 7'), 'frame_layout'),
    )
    for gi, (group, rows) in enumerate((('Codex 반례', codex), ('같은 뿌리 (판정문 밖 · 버리던 줄)', same_root))):
        for k, (tag, ed, want) in enumerate(rows):
            (sc, at, ct), _ = synth(f'r1_{gi}_{k}', fmt='g6', edit=ed)
            jm, err = try_join((sc, at, ct))
            ok, why = entrance_reject(jm, err, want)
            chk(f'J10 [{group}] {tag} → 입구 REJECT ({want}) · 관문 계산 안 함', ok, why)
            ok, why = consumer_blocks(jm, sid, L)
            chk(f'J10 [{group}] {tag} → 계획 join_gate_failed · 정량 관문 거부 (고치기 전 = 정량 ACCEPT)', ok, why)
    #  양성 차단 대조 — 폭이 정상인 중복 행은 전부 소비돼 그대로 REJECT (열 수 사유 아님)
    for k, (tag, ed, want) in enumerate((
            ('접촉 폭 정상 중복 행 (선언 1 · 실제 2)', _ins(2, 9, lambda Ls: Ls[2][9]), {'count_mismatch', 'dem_duplicate_pair'}),
            ('원자 폭 정상 중복 행 (선언 2 · 실제 3)', _ins(1, 9, lambda Ls: Ls[1][9]), {'count_mismatch', 'atom_id_duplicate'}))):
        (sc, at, ct), _ = synth(f'r1_ctl{k}', fmt='g6', edit=ed)
        jm, err = try_join((sc, at, ct))
        chk(f'J10 양성 차단 대조: {tag} → REJECT {sorted(want)} 유지 · row_width 아님',
            jm is not None and jm['status'] == 'REJECT' and want <= set(codes(jm)) and 'row_width' not in codes(jm),
            err or repr(codes(jm)))
    #  빈 줄 처리 보존 — 절 전수 소비가 빈 줄을 옛 판 (고정 위치 읽기) 보다 느슨하게 하지 않는다 (고치기 전 · 뒤 모두 같은 결과여야 한다)
    def blank_ok(Ls):
        _sc, at_, ct_ = Ls
        ct_.insert(8, '')                                   # BOX BOUNDS 내용 뒤 (ENTRIES 머리 앞) = 절 끝
        ct_.insert(2, '   ')                                # TIMESTEP 값 뒤 = 절 끝 (공백뿐)
        ct_.append('')
        at_.insert(10, '')                                  # 행 절 안 (두 원자 행 사이)
        at_.append('  ')
    for k, (tag, ed, want) in enumerate((
            ('접촉 TIMESTEP 머리 바로 다음 빈 줄 (값 앞)', _ins(2, 1, lambda Ls: ''), 'int_token'),
            ('접촉 BOX BOUNDS 경계 줄 사이 빈 줄', _ins(2, 6, lambda Ls: ''), 'box_format'))):
        (sc, at, ct), _ = synth(f'r1_blank{k}', fmt='g6', edit=ed)
        jm, err = try_join((sc, at, ct))
        ok, why = entrance_reject(jm, err, want)
        chk(f'J10 빈 줄 보존: {tag} → 입구 REJECT ({want}) — 옛 판과 같음', ok, why)
    (sc, at, ct), _ = synth('r1_blank_ok', fmt='g6', edit=blank_ok)
    jm, err = try_join((sc, at, ct))
    chk('J10 빈 줄 보존: 절 끝 · 행 절 안 · 파일 끝 빈 줄 → PASS (내용 아님 — 옛 판과 같음)',
        jm is not None and jm['status'] == 'PASS' and jm['rejections'] == [], err or repr(codes(jm)))
    #  양성 — D19 선언된 재사용 (다른 step · 같은 기하)
    (sc, at, ct), _ = synth('r1_d19', fmt='g6', edit=_set(2, 1, '101'))
    jd, err = try_join((sc, at, ct), geom_reuse={'atom_step': 100, 'contact_step': 101, 'reason': '시험 — D19 같은 기하'})
    ok = False
    if jd is not None:
        Pd = S3.am_iface_plan(L, RT_PP, join=jd, **LAW3)
        ok = (jd['status'] == 'PASS' and (jd['geom_reuse'] or {}).get('status') == 'accepted' and Pd['rejections'] == []
              and S3.iface_require_quantitative(Pd, sid=sid, vox=0.25) is Pd)
    chk('J10 양성: D19 선언된 재사용 (atom 100 · contact 101) → PASS · 계획 거부 없음 · 정량 관문 통과', ok,
        err or repr(codes(jd)))
    #  정상 real_14 기록 — 전 행 소비 (물리 행 = 머리 수) · 열 수 불일치 0 · 필수 열 중복 없음 · 프레임 배치 깨끗
    e = join_r14().get('entrance') or {}
    chk('J10 정상 real_14: 물리 행 33,289 · 106,563 (= 머리 수) · 열 수 불일치 0 · 필수 열 중복 없음 · 프레임 배치 위반 0',
        e.get('n_rows_physical') == {'atom': 33289, 'contact': 106563} and e.get('n_row_width_bad') == 0
        and e.get('header_duplicate') == {'atom': [], 'contact': []}
        and isinstance(e.get('frame_layout'), dict) and sum(e['frame_layout'].values()) == 0,
        repr({k: e.get(k) for k in ('n_rows_physical', 'n_row_width_bad', 'header_duplicate', 'frame_layout')}))


@case('J11 float64 유한 · µm 변환 · int64 정수 = 입구 REJECT (RIMPR-02)')
def t_float64_entrance():
    print('J11 — scaffold 토큰 = Decimal 유한 · float64 무한 (1e309 · 고정소수 10^309) · µm 변환 넘침 · int64 넘는 정수 토큰')
    base, sid, L = consumer_ctx()
    big = '1' + '0' * 309 + '.000000000000'

    def scaf(row, col, val):
        def ed(Ls):
            v = Ls[0][row].split(',')
            v[col] = val
            Ls[0][row] = ','.join(v)
        return ed

    def far(Ls):
        """한 구만 (scaffold x = 10^306 고정소수 · 원자 x `1e+306`) · 접촉 0 행 — float64 유한이지만 µm 변환 (×1000) = inf."""
        sc, at, ct = Ls
        del sc[1]
        v = sc[0].split(',')
        v[1] = '1' + '0' * 306 + '.000000000000'
        sc[0] = ','.join(v)
        del at[10]
        at[3] = '1'
        w = at[9].split()
        w[2] = '1e+306'
        at[9] = ' '.join(w)
        del ct[9]
        ct[3] = '0'

    def ct_tok(col, val):
        def ed(Ls):
            v = Ls[2][9].split()
            v[col] = val
            Ls[2][9] = ' '.join(v)
        return ed

    def both_steps(val):
        def ed(Ls):
            Ls[1][1] = val
            Ls[2][1] = val
        return ed

    i64_over = '9223372036854775808'
    rows = (
        ('scaffold 반경 `1e309` (Codex)', scaf(1, 4, '1e309'), 'nonfinite_value', 'scaffold'),
        ('scaffold 반경 고정소수 10^309 (Codex)', scaf(1, 4, big), 'nonfinite_value', 'scaffold'),
        ('scaffold 반경 고정소수 −10^309 (Codex)', scaf(1, 4, '-' + big), 'nonfinite_value', 'scaffold'),
        ('scaffold x 고정소수 10^309 (고치기 전 = cKDTree ValueError)', scaf(1, 1, big), 'nonfinite_value', 'scaffold'),
        ('scaffold x `-1e309`', scaf(1, 1, '-1e309'), 'nonfinite_value', 'scaffold'),
        ('µm 변환 넘침 — 한 구 x 10^306 sim (float64 유한 · ×1000 = inf · 고치기 전 = PASS · c_um inf)', far, 'nonfinite_value',
         'scaffold_um'),
        ('원자 id int64 넘침 `9223372036854775808` (Codex · 고치기 전 = OverflowError)',
         lambda Ls: Ls[1].__setitem__(9, i64_over + Ls[1][9][1:]), 'int_token', 'atom_id'),
        ('접촉 id1 int64 넘침', ct_tok(6, i64_over), 'int_token', 'contact_id1'),
        ('scaffold type int64 넘침', scaf(0, 0, i64_over), 'int_token', 'scaffold_type'),
        ('두 덤프 step int64 넘침 (e3 = int64 정수 · 같은 규칙)', both_steps(i64_over), 'int_token', 'atom_step'),
    )
    for k, (tag, ed, want, where) in enumerate(rows):
        (sc, at, ct), _ = synth(f'r2_{k}', fmt='g6', edit=ed)
        jm, err = try_join((sc, at, ct))
        ok, why = entrance_reject(jm, err, want)
        ent = (jm or {}).get('entrance') or {}
        cnt = (ent.get('nonfinite') or {}) if want == 'nonfinite_value' else (ent.get('int_token_bad') or {})
        chk(f'J11 {tag} → 입구 REJECT ({want} · {where} ≥ 1) · 관문 계산 안 함', ok and int(cnt.get(where, 0)) >= 1,
            why + f' {where}={cnt.get(where)!r}')
        ok, why = consumer_blocks(jm, sid, L)
        chk(f'J11 {tag} → 계획 join_gate_failed · 정량 관문 거부', ok, why)
    #  경계 양성 — int64 최댓값 id 는 정확한 정수 (range 검사의 한 끝 · 같은 기하)
    i64_max = '9223372036854775807'
    (sc, at, ct), _ = synth('r2_i64max', fmt='g6',
                            edit=lambda Ls: (Ls[1].__setitem__(9, i64_max + Ls[1][9][1:]), ct_tok(6, i64_max)(Ls)))
    jm, err = try_join((sc, at, ct))
    chk('J11 경계 양성: 원자 · 접촉 id = int64 최댓값 9223372036854775807 → PASS (거부 없음)',
        jm is not None and jm['status'] == 'PASS' and jm['rejections'] == [], err or repr(codes(jm)))


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
