#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""④b Love–Weber 입자 응력 — 시험 (J20-s · 1저자 비준 10-04 *"권고대로"* · 원장 LHS-29).

옛 열 (`stress_cv` · `stress_ratio_<상>`) = LIGGGHTS `compute stress/atom` 의 입자 접촉 몫 (0.5 · (x_i − x_j) ⊗ F 를 두 입자에
똑같이 — 50/50 분할) · 대각 성분만.  새 열 = 접촉 덤프 (힘 · 접촉점) 로 계산한 **Love–Weber** 입자 평균 응력
σ_i = (1/V_i) Σ_c (x_c − x_i) ⊗ f_c  (f_c = 접촉 c 가 입자 i 에 주는 힘 · 인장 양수 = c_strs 와 같은 부호) — 전체 텐서의 대칭부로 VM.
벽 (바닥 zplane 0 · 판 mesh) 접촉은 두 규약 다 없다 → 벽에 닿은 입자 표지 · 벽 제외 통계.

  python3 scripts/test_love_weber_stress.py

기대값은 손으로 (또는 독립 구현 `lhs_stress_constriction_audit.per_particle_virials` 로) 셈한다 — 생산 함수를 다시 부르지 않는다.

R 묶음 = 원장 RGL-06 (Codex 10-05 · P2) 반례 — 입력 기하 (위치 · 반경 · 부피 · 주기 길이 · 판 높이 · c_strs) 검증 · 비유한 텐서/VM ·
영 분모 (평균 VM 0 = 무하중 → UNDEFINED · 0 으로 위장 금지) · 힘 분해 · virial 의 영 척도 분기 · 전역 virial 검사의 증명 범위 (프레임
대응 증명 아님) · 이름 한정 (입자 접촉력 기반 대칭 응력의 VM · 벽 제외 = 선별 모집단 · 덱 가정 미검증).  반례 입력은 **실제
`analyze_contacts.load_atoms_raw` · `load_contacts_raw` 로 읽은 CSV** 다 (손으로 만든 결과 dict 아님 · 기하 = Codex
`probe_lw_independent.py` 그대로: 반경 1 · 중심 간격 1.8 dimer · 접촉점 = 가운데).
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

FAILS, N = [], [0]


def chk(name, ok, extra=''):
    N[0] += 1
    print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok or not extra else f'  — {extra}'))
    if not ok:
        FAILS.append(name)


def close(a, b, rel=1e-9, ab=0.0):
    try:
        return abs(float(a) - float(b)) <= max(ab, rel * max(abs(float(a)), abs(float(b)), 1e-300))
    except (TypeError, ValueError):
        return False


def vm_of(s):
    """손 VM — 대칭 3×3 (list of lists)."""
    sxx, syy, szz = s[0][0], s[1][1], s[2][2]
    sxy, syz, szx = s[0][1], s[1][2], s[2][0]
    return math.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3 * (sxy ** 2 + syz ** 2 + szx ** 2))


def atom(t, x, y, z, r, cstr=None):
    a = {'type': t, 'x': x, 'y': y, 'z': z, 'radius': r}
    if cstr is not None:                                  # analyze_contacts.load_atoms_raw 와 같은 저장 (c_strs ÷ 부피)
        v = 4.0 / 3.0 * math.pi * r ** 3
        a['sigma_xx'], a['sigma_yy'], a['sigma_zz'] = cstr[0] / v, cstr[1] / v, cstr[2] / v
    return a


def contact(i, j, f, cp, fn=None, drop=()):
    """f = id1 이 받는 전체 힘 · fn 을 안 주면 f 전부를 법선으로 (ft = 0)."""
    fn = f if fn is None else fn
    ft = tuple(f[k] - fn[k] for k in range(3))
    c = {'id1': i, 'id2': j, 'fn': math.sqrt(sum(v * v for v in fn)), 'ft': math.sqrt(sum(v * v for v in ft)),
         'fn_x': fn[0], 'fn_y': fn[1], 'fn_z': fn[2], 'ft_x': ft[0], 'ft_y': ft[1], 'ft_z': ft[2],
         'fx': f[0], 'fy': f[1], 'fz': f[2], 'cp_x': cp[0], 'cp_y': cp[1], 'cp_z': cp[2],
         'contact_area': 1e-8, 'delta': 1e-5}
    for k in drop:
        c.pop(k, None)
    return c


def lw(atoms, contacts, tm, plate_z=1.0, src='mesh', box=(None, None), arrays=False):
    import dem_analysis_core as D
    return D.calc_love_weber_stress(atoms, contacts, tm, plate_z, box_x=box[0], box_y=box[1],
                                    plate_z_source=src, return_arrays=arrays)


# ── RGL-06 반례 입력 — CSV 로 써서 실제 파서 (analyze_contacts.load_atoms_raw · load_contacts_raw) 로 읽는다 ──────────
#   Codex 증거 `evidence_g23/atoms_nan_radius.csv` 의 바이트 그대로 (고립 SE 하나의 반경만 NaN · AM_P dimer 는 정상).
CODEX_NAN_RADIUS_CSV = ('id,type,x,y,z,radius,c_strs[1],c_strs[2],c_strs[3]\n'
                        '1,1,2,2,2,1,0,0,-0.9\n'
                        '2,1,2,2,3.8,1,0,0,-0.9\n'
                        '3,2,8,2,8,nan,0,0,0\n')
CODEX_EVIDENCE = os.path.join(ROOT, 'docs', 'reviews', 'codex_rint_g1_lhs_network_review_evidence_20261005', 'evidence_g23')


def _fmt(v):
    return repr(float(v)) if isinstance(v, float) else str(v)


def write_atoms_csv(path, rows, cstr=True):
    """rows = (id, type, x, y, z, r[, (c1, c2, c3)]) — parse_liggghts 가 쓰는 atoms.csv 꼴 (c_strs = 응력 × 부피 · LIGGGHTS 단위)."""
    with open(path, 'w') as fh:
        fh.write('id,type,x,y,z,radius' + (',c_strs[1],c_strs[2],c_strs[3]' if cstr else '') + '\n')
        for r in rows:
            vals = list(r[:6]) + (list(r[6]) if cstr else [])
            fh.write(','.join(_fmt(v) for v in vals) + '\n')


def crow(i, j, f, cp, fn=None, ft=None):
    """접촉 행 — f = id1 이 받는 전체 힘 · fn 기본 = f · ft 기본 = f − fn (따로 주면 F ≠ Fn + Ft 인 깨진 열을 만들 수 있다)."""
    fn = f if fn is None else fn
    ft = tuple(f[k] - fn[k] for k in range(3)) if ft is None else ft
    return (i, j, f, fn, ft, cp)


def write_contacts_csv(path, rows):
    """rows = crow(…) — load_contacts_raw 가 읽는 열 (fx·fy·fz · cp_* 포함 = c_cpl 26 열 덤프의 CSV)."""
    with open(path, 'w') as fh:
        fh.write('id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta,fx,fy,fz,cp_x,cp_y,cp_z\n')
        for i, j, f, fn, ft, cp in rows:
            fh.write(','.join(_fmt(v) for v in [i, j, *fn, *ft, 1e-8, 1e-6, *f, *cp]) + '\n')


def load_pair(tmp, name, atoms, contacts, cstr=True):
    """atoms = 행 목록 또는 CSV 문자열 그대로 → (atoms_raw, contacts_raw) — 웹앱 접촉 단계와 같은 파서."""
    import analyze_contacts as AC
    d = os.path.join(tmp, name)
    os.makedirs(d, exist_ok=True)
    ap, cpth = os.path.join(d, 'atoms.csv'), os.path.join(d, 'contacts.csv')
    if isinstance(atoms, str):
        with open(ap, 'w') as fh:
            fh.write(atoms)
    else:
        write_atoms_csv(ap, atoms, cstr=cstr)
    write_contacts_csv(cpth, contacts)
    a, _ = AC.load_atoms_raw(ap)
    c, _ = AC.load_contacts_raw(cpth)
    return a, c


def dimer_atoms(i0, t, x, force, z0=2.0, r=1.0, cstr=True):
    """Codex dimer — 반경 r · 중심 간격 1.8 r · c_strs = 50/50 손값 (−0.9 · 힘 · r) — 아래 입자가 id i0."""
    c = (0.0, 0.0, -0.9 * force * r) if cstr else None
    return [(i0, t, x, 2.0, z0, r) + ((c,) if cstr else ()), (i0 + 1, t, x, 2.0, z0 + 1.8 * r, r) + ((c,) if cstr else ())]


def dimer_contact(i0, x, force, z0=2.0, r=1.0, **kw):
    """id1 = 아래 입자 (z0) 가 위 입자에게 아래로 밀린다 (F = (0, 0, −force)) · 접촉점 = 가운데."""
    return crow(i0, i0 + 1, (0.0, 0.0, -force), (x, 2.0, z0 + 0.9 * r), **kw)


def rgl06(D):
    """원장 RGL-06 (Codex 10-05 · P2) — 옛 코드는 아래 반례에서 거짓 OK · 거짓 0 · 거짓 FAILED 를 낸다."""
    TM = {1: 'AM_P', 2: 'SE'}
    st = lambda r: str(r.get('status', ''))           # noqa: E731
    nostats = lambda r: r.get('vm_cv') is None and not r.get('type_stress') and 'tensor' not in r   # noqa: E731
    tmp = tempfile.mkdtemp(prefix='lw_rgl06_')
    try:
        # R0 반례 입력이 Codex 증거 CSV 와 같은 바이트인지 (증거 묶음이 리포에 있을 때)
        ev = os.path.join(CODEX_EVIDENCE, 'atoms_nan_radius.csv')
        if os.path.exists(ev):
            with open(ev, encoding='utf-8') as fh:
                same_bytes = fh.read().replace('\r\n', '\n') == CODEX_NAN_RADIUS_CSV
            chk('R0 반례 CSV = Codex 증거 evidence_g23/atoms_nan_radius.csv 와 같은 내용', same_bytes)

        # R1 ★ 고립 SE 반경 NaN — 옛 코드: status OK · vm_cv 0 · AM_P mean 0.2149 인데 ratio 0 · SE mean NaN 인데 ratio 0
        a, c = load_pair(tmp, 'r1', CODEX_NAN_RADIUS_CSV, [dimer_contact(1, 2.0, 1.0)])
        res = lw(a, c, TM, plate_z=20.0, arrays=True)
        chk('R1 ★ 고립 입자 반경 NaN (실 load_atoms_raw) → FAILED (invalid_input …) · 사유에 반경 — 옛 코드 OK · vm_cv 0 · 비 0',
            st(res).startswith('FAILED (invalid_input') and 'radius' in st(res), st(res))
        chk('R1b 정상 통계 발행 안 함 — vm_cv None · type_stress 없음 · 텐서 없음 (NaN > 0 → "0" 분기 차단)', nostats(res),
            f"vm_cv {res.get('vm_cv')} · {res.get('type_stress')}")

        # R2 판 높이 — mesh 판이면 plate_z 는 유한 · 바닥 (z = 0) 위여야 한다 (옛 코드: NaN 이면 판 접촉 0 · 벽 제외 통계를 만들고 OK)
        a, c = load_pair(tmp, 'r2', dimer_atoms(1, 1, 2.0, 1.0), [dimer_contact(1, 2.0, 1.0)])
        res = lw(a, c, TM, plate_z=float('nan'), src='mesh')
        chk('R2 ★ plate_z NaN · source mesh → FAILED (invalid_input: plate_z …) · 값 없음 — 옛 코드 OK · 판 접촉 0 · 벽 제외 요약',
            st(res).startswith('FAILED (invalid_input') and 'plate_z' in st(res) and nostats(res)
            and res.get('vm_cv_nowall') is None, st(res))
        bad_pz = {pz: st(lw(a, c, TM, plate_z=pz, src='mesh')) for pz in (None, float('inf'), 0.0, -1.0)}
        chk('R2b plate_z None · inf · 0 · 음수 (mesh) → 전부 FAILED (invalid_input: plate_z …)',
            all(s.startswith('FAILED (invalid_input') and 'plate_z' in s for s in bad_pz.values()), str(bad_pz))
        res = lw(a, c, TM, plate_z=float('nan'), src='estimated_center')
        chk('R2c 판 높이를 안 쓰는 경로 (source = estimated_center) 는 plate_z 를 검사하지 않는다 → OK · 판 표지 unavailable',
            st(res) == 'OK' and 'unavailable' in str(res.get('wall', {}).get('plate_flag')), st(res))

        # R3 ★ 힘 분해의 영 척도 — F = 0 인데 Fn + Ft = (0, 0, −1): 옛 코드 오차 0 · OK
        a, c = load_pair(tmp, 'r3', dimer_atoms(1, 1, 2.0, 1.0, cstr=False),
                         [crow(1, 2, (0.0, 0.0, 0.0), (2.0, 2.0, 2.9), fn=(0.0, 0.0, -1.0), ft=(0.0, 0.0, 0.0))], cstr=False)
        res = lw(a, c, TM, plate_z=20.0)
        ck = res.get('checks', {})
        chk('R3 ★ F = 0 · Fn+Ft = (0, 0, −1) → FAILED (force_columns …) — 영 척도 분기 (척도 0 인데 잔차 > 0) · 옛 코드 오차 0 · OK',
            st(res).startswith('FAILED (force_columns') and nostats(res), st(res))
        chk('R3b 검사 기록 = 절대 잔차 1 · 상대 차 None (0 분모 — inf 를 JSON 에 안 쓴다) · zero_scale 표지',
            close(ck.get('force_decomp_abs'), 1.0) and ck.get('force_decomp_rel') is None and ck.get('force_decomp_zero_scale') is True, str(ck))

        # R4 ★ 진짜 무하중 — F = 0 ∧ c_strs = 0: 옛 코드 virial 오차 ∞ · FAILED (거짓 실패)
        a, c = load_pair(tmp, 'r4', dimer_atoms(1, 1, 2.0, 0.0), [dimer_contact(1, 2.0, 0.0)])
        res = lw(a, c, TM, plate_z=20.0)
        ck = res.get('checks', {})
        chk('R4 ★ F = 0 ∧ c_strs = 0 → virial 검사 통과 (두 합 모두 정확히 0 · 상대 차 0 · zero_scale) — 옛 코드 inf · FAILED',
            ck.get('virial_status') == 'checked' and ck.get('virial_total_rel') == 0.0 and ck.get('virial_zero_scale') is True, str(ck))
        chk('R4b 무하중 → status UNDEFINED (zero_load …) · CV · 상 비 = 0/0 미정의 → 값 없음 (0 · OK 로 위장 안 함)',
            st(res).startswith('UNDEFINED (zero_load') and nostats(res), st(res))
        a, c = load_pair(tmp, 'r4c', dimer_atoms(1, 1, 2.0, 0.0, cstr=False), [dimer_contact(1, 2.0, 0.0)], cstr=False)
        res = lw(a, c, TM, plate_z=20.0)
        chk('R4c c_strs 없는 무하중도 UNDEFINED (옛 코드: OK · vm_cv 0 · 비 0 = 거짓 0)', st(res).startswith('UNDEFINED (zero_load')
            and nostats(res) and res.get('checks', {}).get('virial_total_rel') is None, st(res))

        # R5 전역 virial 1 % 검사의 증명 범위 (Q3) — 같은 기하 AM_P · SE dimer 의 접촉 힘 1 · 3 을 맞바꿔도 합은 같다
        atoms = dimer_atoms(1, 1, 2.0, 1.0) + dimer_atoms(3, 2, 7.0, 3.0)
        a, c = load_pair(tmp, 'r5ok', atoms, [dimer_contact(1, 2.0, 1.0), dimer_contact(3, 7.0, 3.0)])
        good = lw(a, c, TM, plate_z=20.0)
        a, c = load_pair(tmp, 'r5sw', atoms, [dimer_contact(1, 2.0, 3.0), dimer_contact(3, 7.0, 1.0)])
        bad = lw(a, c, TM, plate_z=20.0)
        chk('R5 전역 검사는 맞바꾼 접촉 힘을 못 잡는다 (둘 다 OK · virial 1e-15 미만 · AM_P 비 0.5 ↔ 1.5) — 이 한계를 기록으로 남긴다',
            st(good) == 'OK' and st(bad) == 'OK' and bad['checks']['virial_total_rel'] < 1e-15
            and close(good['type_stress']['AM_P']['ratio'], 0.5) and close(bad['type_stress']['AM_P']['ratio'], 1.5),
            f"{st(good)} · {st(bad)}")
        vs = str(bad.get('checks', {}).get('virial_scope', ''))
        chk('R5b ★ 검사 범위 표기 — checks.virial_scope = 전역 대각 합 · 부호/척도 검사 · 프레임 대응 증명 아님',
            'global' in vs and '전역' in vs and '프레임' in vs and '아님' in vs, vs)
        q = str(bad.get('quantity', ''))
        chk('R5c ★ 이름 한정 — quantity = 입자 접촉력 기반 대칭 응력의 VM · kinetic · 벽 · couple 미포함 (전체 동적 응력 아님)',
            '입자 접촉력' in q and '대칭' in q and 'kinetic' in q and 'couple' in q and '아님' in q, q)
        au = str(bad.get('assumptions_unverified', ''))
        chk('R5d ★ 덱 가정 미검증 표기 — 바닥 z = 0 · 평면 mesh 판 · x·y 주기 · 함수가 덱을 읽지 않는다',
            'z = 0' in au and 'mesh' in au and '주기' in au and '검증' in au, au)
        chk('R5e 계약 표지 = love_weber_checks_v2 (입력 검증 · 영 척도 · UNDEFINED 이후 세대 — 옛 결과와 구별)',
            bad.get('contract') == 'love_weber_checks_v2', str(bad.get('contract')))

        # R6 주기 길이 — 주는 값은 유한 양수여야 한다 (옛 코드: NaN · inf 는 `if L:` 를 통과해 가지가 NaN → c_strs 없으면 OK · vm_cv 0)
        a, c = load_pair(tmp, 'r6', dimer_atoms(1, 1, 2.0, 1.0, cstr=False), [dimer_contact(1, 2.0, 1.0)], cstr=False)
        bad_box = {repr(b): st(lw(a, c, TM, plate_z=20.0, box=b)) for b in
                   ((float('nan'), 5.0), (5.0, float('inf')), (0.0, 5.0), (-5.0, 5.0))}
        chk('R6 ★ 주기 길이 NaN · inf · 0 · 음수 → FAILED (invalid_input: box …) — 옛 코드 NaN 은 OK · vm_cv 0',
            all(s.startswith('FAILED (invalid_input') and 'box_' in s for s in bad_box.values()), str(bad_box))
        chk('R6b 상자를 안 주면 (None) 검사하지 않는다 → OK (비주기 호출부 호환)', st(lw(a, c, TM, plate_z=20.0, box=(None, None))) == 'OK')

        # R7 · R8 원자 위치 · 반경 — 접촉 없는 입자도 모집단 · 벽 표지에 들어간다
        base = dimer_atoms(1, 1, 2.0, 1.0, cstr=False)
        for tag, extra, word in (('R7', (3, 2, float('nan'), 2.0, 8.0, 1.0), 'position'),
                                 ('R7b', (3, 2, 8.0, 2.0, float('inf'), 1.0), 'position'),
                                 ('R8', (3, 2, 8.0, 2.0, 8.0, 0.0), 'radius'),
                                 ('R8b', (3, 2, 8.0, 2.0, 8.0, -1.0), 'radius')):
            a, c = load_pair(tmp, tag, base + [extra], [dimer_contact(1, 2.0, 1.0)], cstr=False)
            res = lw(a, c, TM, plate_z=20.0)
            chk(f'{tag} 고립 입자 {word} 무효 ({extra[2:6]}) → FAILED (invalid_input: …{word}…) · 값 없음',
                st(res).startswith('FAILED (invalid_input') and word in st(res) and nostats(res), st(res))
        a, c = load_pair(tmp, 'r8c', [(1, 1, 2.0, 2.0, 2.0, -1.0), (2, 1, 2.0, 2.0, 3.8, -1.0)],
                         [dimer_contact(1, 2.0, 1.0)], cstr=False)
        res = lw(a, c, TM, plate_z=20.0)
        chk('R8c 접촉한 두 입자 반경 음수 → FAILED (invalid_input: radius) — 옛 코드는 |b|/r 가 음수라 접촉점 검사를 통과해 OK',
            st(res).startswith('FAILED (invalid_input') and 'radius' in st(res), st(res))

        # R9 c_strs 일부 결측 · 비유한 — 옛 코드: 한 입자의 c_strs 결측이 전 입자 virial 검사를 조용히 끈다 ("no c_strs" 로 위장)
        a, c = load_pair(tmp, 'r9', dimer_atoms(1, 1, 2.0, 1.0) + [(3, 2, 8.0, 2.0, 8.0, 1.0, (float('nan'), 0.0, 0.0))],
                         [dimer_contact(1, 2.0, 1.0)])
        res = lw(a, c, TM, plate_z=20.0)
        chk('R9 ★ 한 입자 c_strs NaN (반경 정상) → FAILED (invalid_input: c_strs …) — 옛 코드 virial unavailable · OK',
            st(res).startswith('FAILED (invalid_input') and 'c_strs' in st(res) and nostats(res), st(res))
        a, c = load_pair(tmp, 'r9b', [(1, 1, 2.0, 2.0, 2.0, 1.0, (0.0, float('nan'), -0.9)), (2, 1, 2.0, 2.0, 3.8, 1.0, (0.0, 0.0, -0.9))],
                         [dimer_contact(1, 2.0, 1.0)])
        res = lw(a, c, TM, plate_z=20.0)
        chk('R9b c_strs[2] 만 NaN → FAILED (invalid_input: c_strs …) — 옛 코드는 virial_mismatch 라는 틀린 사유',
            st(res).startswith('FAILED (invalid_input') and 'c_strs' in st(res), st(res))

        # R10 비유한 텐서/VM — 유한 입력이라도 넘침 (VM² overflow) 이면 정상 통계를 내지 않는다 (옛 코드: mean inf → cv NaN · OK)
        a, c = load_pair(tmp, 'r10', dimer_atoms(1, 1, 2.0, 1.0, cstr=False), [dimer_contact(1, 2.0, 1e308)], cstr=False)
        res = lw(a, c, TM, plate_z=20.0)
        chk('R10 ★ VM 넘침 (F 1e308) → FAILED (non_finite …) · 값 없음 — 옛 코드 OK · cv NaN', st(res).startswith('FAILED (non_finite')
            and nostats(res), st(res))

        # R11 벽 제외 모집단의 영 분모 — 전체는 하중이 있는데 벽 안 닿은 입자는 전부 VM 0 (옛 코드: vm_cv_nowall 0 · 비 0 = 거짓 0)
        atoms = [(1, 1, 2.0, 2.0, 0.9, 1.0), (2, 1, 3.8, 2.0, 0.9, 1.0), (3, 2, 8.0, 8.0, 5.0, 1.0)]   # 1 · 2 = 바닥 접촉 · 3 = 고립
        a, c = load_pair(tmp, 'r11', atoms, [crow(1, 2, (-1.0, 0.0, 0.0), (2.9, 2.0, 0.9))], cstr=False)
        res = lw(a, c, TM, plate_z=20.0)
        chk('R11 ★ 전체 OK · 벽 제외 모집단 평균 VM 0 → vm_cv_nowall None · 상 비 None · nowall_status UNDEFINED — 옛 코드 0 · 0',
            st(res) == 'OK' and res.get('vm_cv_nowall') is None and res.get('type_stress_nowall') is None
            and str(res.get('nowall_status', '')).startswith('UNDEFINED'), f"{st(res)} · {res.get('vm_cv_nowall')} · {res.get('nowall_status')}")
        a, c = load_pair(tmp, 'r11b', atoms[:2], [crow(1, 2, (-1.0, 0.0, 0.0), (2.9, 2.0, 0.9))], cstr=False)
        res = lw(a, c, TM, plate_z=20.0)
        chk('R11b 모든 입자가 벽 접촉 → nowall_status NOT_COMPUTED (empty_population) · 벽 제외 값 없음',
            st(res) == 'OK' and res.get('vm_cv_nowall') is None and 'empty_population' in str(res.get('nowall_status')), str(res.get('nowall_status')))

        # R12 정상 침대의 메타 — 벽 제외 = 선별 모집단 (결측 벽 힘 복원 아님) · nowall_status OK
        rP, rS = 0.006, 0.001
        zP = rP - 1e-5
        zS = [zP + rP + rS - 1e-5]
        zS += [zS[0] + 2 * rS - 1e-5, zS[0] + 4 * rS - 2e-5]
        pz = zS[2] + rS - 2e-5
        atoms = [(1, 1, 0.02, 0.02, zP, rP)] + [(2 + k, 2, 0.02, 0.02, zS[k], rS) for k in range(3)] + [(5, 2, 0.03, 0.03, 0.01, rS)]
        zz, rr_ = [zP] + zS, [rP, rS, rS, rS]
        cs = [crow(k + 1, k + 2, (0.0, 0.0, -1e-3 * (4 - k)), (0.02, 0.02, zz[k] + rr_[k] - 0.5e-5)) for k in range(3)]
        a, c = load_pair(tmp, 'r12', atoms, cs, cstr=False)
        res = lw(a, c, TM, plate_z=pz)
        ns = str(res.get('wall', {}).get('nowall_scope', ''))
        chk('R12 정상 벽 침대 — status OK · nowall_status OK · wall.nowall_scope = 선별 모집단 · 결측 벽 힘 복원 아님',
            st(res) == 'OK' and res.get('nowall_status') == 'OK' and '선별 모집단' in ns and '복원' in ns and '아님' in ns,
            f"{st(res)} · {res.get('nowall_status')} · {ns}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    try:
        import dem_analysis_core as D
    except Exception as e:                                # noqa: BLE001
        print('dem_analysis_core import 실패:', e)
        return 1
    if not hasattr(D, 'calc_love_weber_stress'):
        chk('L0 dem_analysis_core.calc_love_weber_stress 가 있다 (④b)', False, '함수 없음')
        print(f'\n{N[0] - len(FAILS)}/{N[0]} 통과')
        return 1
    chk('L0 dem_analysis_core.calc_love_weber_stress 가 있다 (④b)', True)
    chk('L0b 정의 문자열 = love_weber_branch_full_tensor_v1', getattr(D, 'LW_DEFINITION', None) == 'love_weber_branch_full_tensor_v1',
        str(getattr(D, 'LW_DEFINITION', None)))
    TM = {1: 'AM_P', 2: 'SE'}

    # ── L1 크기 다른 두 구 (r 6 : 1) · z 축 법선 접촉 · 손풀이 ──────────────────────────
    r1, r2, d = 0.006, 0.001, 0.0069                      # 겹침 δ = 1e-4
    z1, z2 = 0.02, 0.02 + d                               # 1 이 아래 · 2 가 위
    Fz = -2.0e-3                                          # 1 이 받는 힘 = 아래로 (밀어냄)
    cpz = z1 + (r1 - 0.5e-4)                              # 렌즈 가운데 (LIGGGHTS 와 같은 자리 · 손으로 준다)
    A2 = {1: atom(1, 0.02, 0.02, z1, r1), 2: atom(2, 0.02, 0.02, z2, r2)}
    C2 = [contact(1, 2, (0.0, 0.0, Fz), (0.02, 0.02, cpz))]
    res = lw(A2, C2, TM, arrays=True)
    V1, V2 = 4 / 3 * math.pi * r1 ** 3, 4 / 3 * math.pi * r2 ** 3
    s1_zz = (cpz - z1) * Fz / V1                          # σ_1 = (x_c − x_1) ⊗ f_1 / V_1
    s2_zz = (cpz - z2) * (-Fz) / V2                       # σ_2 = (x_c − x_2) ⊗ (−f_1) / V_2
    chk('L1 상태 OK · 정의 문자열', res.get('status') == 'OK' and res.get('definition') == 'love_weber_branch_full_tensor_v1', str(res.get('status')))
    T = res.get('tensor')
    ok = T is not None and close(T[0][2][2], s1_zz) and close(T[1][2][2], s2_zz)
    chk('L1 손풀이 σ_zz — 큰 입자 (x_c−x_1)·f/V_1 · 작은 입자 (x_c−x_2)·(−f)/V_2', ok,
        f'{None if T is None else (T[0][2][2], T[1][2][2])} vs {(s1_zz, s2_zz)}')
    chk('L1b 압축 = 음수 (인장 양수 · LIGGGHTS c_strs 와 같은 부호)', T is not None and T[0][2][2] < 0 and T[1][2][2] < 0)
    sym1 = -0.5 * (z1 - z2) * Fz / V1                    # 옛 규약 손값 = c_strs/V = −0.5 (x_1 − x_2) ⊗ f_1 / V (50/50) — 비교용
    sym2 = -0.5 * (z1 - z2) * Fz / V2
    chk('L1c 50/50 대비 — 큰 입자 LW/옛 = 2(x_c−x_1)/(x_1−x_2) ≈ 2r_1/(r_1+r_2) (1.71) · 작은 입자 ≈ 0.29',
        T is not None and close(T[0][2][2] / sym1, 2 * (cpz - z1) / (z2 - z1)) and close(T[1][2][2] / sym2, 2 * (z2 - cpz) / (z2 - z1))
        and 1.6 < T[0][2][2] / sym1 < 1.75 and 0.25 < T[1][2][2] / sym2 < 0.32)
    vm1, vm2 = abs(s1_zz), abs(s2_zz)                     # 단축 응력이면 VM = |σ_zz|
    mean = (vm1 + vm2) / 2
    cv = math.sqrt(((vm1 - mean) ** 2 + (vm2 - mean) ** 2) / 2) / mean * 100
    chk('L1d 요약 = 옛 정의와 같은 통계 (모집단 std/mean · 상 평균/전체 평균)',
        close(res.get('vm_cv'), cv) and close(res['type_stress']['AM_P']['ratio'], vm1 / mean)
        and close(res['type_stress']['SE']['ratio'], vm2 / mean), f"{res.get('vm_cv')} vs {cv}")

    # ── L2 비스듬한 접촉 → 전단 성분 · VM 에 3·s_xz² ─────────────────────────────────────
    c45 = math.sqrt(0.5)
    rr = 0.001
    dd = 2 * rr - 1e-5
    xa, za = 0.02, 0.02
    xb, zb = xa + dd * c45, za + dd * c45
    cpx, cpz2 = xa + (rr - 0.5e-5) * c45, za + (rr - 0.5e-5) * c45
    f = (-1e-3 * c45, 0.0, -1e-3 * c45)
    A3 = {1: atom(2, xa, 0.02, za, rr), 2: atom(2, xb, 0.02, zb, rr)}
    res = lw(A3, [contact(1, 2, f, (cpx, 0.02, cpz2))], {2: 'SE'}, arrays=True)
    V = 4 / 3 * math.pi * rr ** 3
    b = (cpx - xa, 0.0, cpz2 - za)
    full = [[b[i] * f[j] / V for j in range(3)] for i in range(3)]
    sym = [[0.5 * (full[i][j] + full[j][i]) for j in range(3)] for i in range(3)]
    T = res.get('tensor')
    chk('L2 비스듬한 접촉 — 전단 σ_xz ≠ 0 (대각만 보던 옛 VM 이 버리던 성분)', T is not None and abs(T[0][0][2]) > 0 and close(T[0][0][2], full[0][2]))
    vmh = vm_of(sym)
    chk('L2b VM = √(½Σ(σ_ii−σ_jj)² + 3Σσ_ij²) — 전체 텐서 (손값)', res.get('arrays_vm') is not None and close(res['arrays_vm'][0], vmh),
        f"{None if res.get('arrays_vm') is None else res['arrays_vm'][0]} vs {vmh}")
    vm_diag = math.sqrt(0.5 * ((sym[0][0] - sym[1][1]) ** 2 + (sym[1][1] - sym[2][2]) ** 2 + (sym[2][2] - sym[0][0]) ** 2))
    chk('L2c 전체 텐서 VM > 대각 VM (전단 포함 확인)', res.get('arrays_vm') is not None and res['arrays_vm'][0] > vm_diag * 1.01)

    # ── L3 비대칭 텐서 → 대칭부로 VM · 비대칭 진단 ───────────────────────────────────────
    f3 = (3e-4, 0.0, -1e-3)                               # 접선 성분 → b⊗f 가 비대칭
    A4 = {1: atom(2, 0.02, 0.02, 0.02, rr), 2: atom(2, 0.02, 0.02, 0.02 + dd, rr)}
    cp4 = (0.02, 0.02, 0.02 + rr - 0.5e-5)
    res = lw(A4, [contact(1, 2, f3, cp4, fn=(0.0, 0.0, -1e-3))], {2: 'SE'}, arrays=True)
    b4 = (0.0, 0.0, rr - 0.5e-5)
    full = [[b4[i] * f3[j] / V for j in range(3)] for i in range(3)]
    sym = [[0.5 * (full[i][j] + full[j][i]) for j in range(3)] for i in range(3)]
    chk('L3 비대칭 b⊗f — VM 은 대칭부 (손값)', res.get('arrays_vm') is not None and close(res['arrays_vm'][0], vm_of(sym)))
    chk('L3b 비대칭 진단 asym_frob_median > 0 (기록)', isinstance(res.get('asym_frob_median'), float) and res['asym_frob_median'] > 0,
        str(res.get('asym_frob_median')))

    # ── L4 주기 최소영상 — x 경계를 넘는 쌍 = 상자 안으로 옮긴 같은 쌍 ─────────────────────────
    L = 0.05
    xa, xb = 0.0004, L - 0.0004 - 0.00002                 # 거리 (최소영상) = 0.0008 + 0.00002 → 겹침 없음? 아래에서 r 를 맞춘다
    r4 = 0.00042
    dmi = (xa + L) - xb                                   # 0.00082 (2r = 0.00084 → 겹침 2e-5)
    cpx_unwrapped = xa - (r4 - 1e-5)                      # 1 (x=0.0004) 의 −x 쪽 (상자 밖 음수 좌표)
    f = (+1e-3, 0.0, 0.0)                                 # 1 이 받는 힘 = +x (2 의 영상이 −x 쪽)
    Aw = {1: atom(2, xa, 0.02, 0.02, r4), 2: atom(2, xb, 0.02, 0.02, r4)}
    res_u = lw(Aw, [contact(1, 2, f, (cpx_unwrapped, 0.02, 0.02))], {2: 'SE'}, box=(L, L), arrays=True)
    res_w = lw(Aw, [contact(1, 2, f, (cpx_unwrapped + L, 0.02, 0.02))], {2: 'SE'}, box=(L, L), arrays=True)
    shift = 0.02                                          # 같은 쌍을 상자 가운데로
    Ai = {1: atom(2, xa + shift, 0.02, 0.02, r4), 2: atom(2, xa + shift - dmi, 0.02, 0.02, r4)}
    res_i = lw(Ai, [contact(1, 2, f, (cpx_unwrapped + shift, 0.02, 0.02))], {2: 'SE'}, box=(L, L), arrays=True)
    ok = all(r.get('status') == 'OK' for r in (res_u, res_w, res_i)) and all(
        close(res_u['tensor'][k][0][0], res_i['tensor'][k][0][0]) and close(res_w['tensor'][k][0][0], res_i['tensor'][k][0][0]) for k in (0, 1))
    chk('L4 주기 x 경계 쌍 (접촉점 상자 밖 · 안으로 감싼 두 표기) = 상자 가운데 같은 쌍', ok,
        f"{[r.get('status') for r in (res_u, res_w, res_i)]}")
    res_nb = lw(Aw, [contact(1, 2, f, (cpx_unwrapped, 0.02, 0.02))], {2: 'SE'}, box=(None, None))
    chk('L4b 상자를 안 주면 경계 너머 접촉점이 입자 밖 → FAILED (조용히 틀린 값 대신 거부)',
        str(res_nb.get('status', '')).startswith('FAILED') and 'contact_point' in str(res_nb.get('status')), str(res_nb.get('status')))

    # ── L5 전체 virial 항등식 Σ V σ_LW = Σ c_strs (접촉점과 무관한 정확식) ─────────────────────
    #     c_strs_i = −Σ_c 0.5 (x_id1 − x_id2) ⊗ F_c  (LIGGGHTS stress/atom · 부호 = 인장 양수)
    def chain_bed(scale_c=1.0, flip=False):
        pts = [(1, 0.006, 0.006), (2, 0.001, 0.0130), (2, 0.001, 0.0149)]   # (type, r, z) — 바닥 위 사슬
        z = [p[2] for p in pts]
        cs, fz = [], [-3e-3, -1.5e-3]
        for k in range(2):
            lo, hi = k, k + 1
            cpz_ = z[lo] + (pts[lo][1] - 0.5 * (pts[lo][1] + pts[hi][1] - (z[hi] - z[lo])))
            ff = -fz[k] if flip else fz[k]
            cs.append(contact(lo + 1, hi + 1, (0.0, 0.0, ff), (0.02, 0.02, cpz_)))
        cstr = [[0.0, 0.0, 0.0] for _ in pts]
        for k, c in enumerate(cs):
            lo, hi = k, k + 1
            w = -0.5 * (z[lo] - z[hi]) * fz[k] * scale_c
            cstr[lo][2] += w
            cstr[hi][2] += w
        A = {k + 1: atom(p[0], 0.02, 0.02, p[2], p[1], cstr[k]) for k, p in enumerate(pts)}
        return A, cs
    A, cs = chain_bed()
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L5 c_strs 가 있으면 Σ V σ_LW (대각) = Σ c_strs — 상대 차 ≈ 0 기록', res.get('status') == 'OK'
        and isinstance(res.get('checks', {}).get('virial_total_rel'), float) and res['checks']['virial_total_rel'] < 1e-9,
        f"{res.get('status')} · {res.get('checks')}")
    A, cs = chain_bed(flip=True)
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L5b 힘 부호가 뒤집힌 접촉 열 (id2 가 받는 힘으로 잘못 읽음) → FAILED virial_mismatch',
        str(res.get('status', '')).startswith('FAILED') and 'virial' in str(res.get('status')), str(res.get('status')))
    A, cs = chain_bed(scale_c=1.5)
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L5c 프레임이 다른 원자 덤프 (c_strs 1.5 배) → FAILED virial_mismatch', str(res.get('status', '')).startswith('FAILED'), str(res.get('status')))
    A, cs = chain_bed()
    for a in A.values():
        for k in ('sigma_xx', 'sigma_yy', 'sigma_zz'):
            a.pop(k, None)
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L5d c_strs 없음 → OK 이되 virial 대조 = None (unavailable 로 기록 · 거부 아님)',
        res.get('status') == 'OK' and res.get('checks', {}).get('virial_total_rel') is None
        and 'unavailable' in str(res.get('checks', {}).get('virial_status', '')), str(res.get('checks')))

    # ── L6 · L7 · L8 · L9 열 결손 · 불일치 → 값 없이 상태 ─────────────────────────────────
    A, cs = chain_bed()
    cs[0]['fx'] += 5e-4                                   # f ≠ fn + ft
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L6 전체 힘 ≠ 법선 + 접선 (열 대응 어긋남) → FAILED force_columns', str(res.get('status', '')).startswith('FAILED')
        and 'force' in str(res.get('status')) and res.get('vm_cv') is None, str(res.get('status')))
    A, cs = chain_bed()
    cs[1]['cp_z'] += 0.003                                # 접촉점이 두 입자 밖
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L7 접촉점이 입자 밖 (|x_c − x_i| > 1.01 r_i) → FAILED contact_point', str(res.get('status', '')).startswith('FAILED')
        and 'contact_point' in str(res.get('status')) and res.get('vm_cv') is None, str(res.get('status')))
    A, cs = chain_bed()
    cs = [{k: v for k, v in c.items() if not k.startswith('cp_')} for c in cs]
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L8 접촉점 열 없음 (옛 덤프 · 손 픽스처) → NOT_COMPUTED (missing …) · 값 없음 (0 으로 안 채움)',
        str(res.get('status', '')).startswith('NOT_COMPUTED') and 'cp_x' in str(res.get('status')) and res.get('vm_cv') is None,
        str(res.get('status')))
    A, cs = chain_bed()
    cs[0]['cp_x'] = float('nan')
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L8b NaN 값 → FAILED non_finite', str(res.get('status', '')).startswith('FAILED') and 'non_finite' in str(res.get('status')), str(res.get('status')))
    A, cs = chain_bed()
    cs.append(contact(1, 99, (0.0, 0.0, -1e-3), (0.02, 0.02, 0.012)))
    res = lw(A, cs, TM, plate_z=0.03)
    chk('L9 원자 덤프에 없는 id 의 접촉 → FAILED contact_ids (두 덤프 짝 불일치)', str(res.get('status', '')).startswith('FAILED')
        and 'contact_ids' in str(res.get('status')), str(res.get('status')))
    res = lw(A, [], TM, plate_z=0.03)
    chk('L9b 접촉 0 → NOT_COMPUTED (no_contacts)', str(res.get('status', '')).startswith('NOT_COMPUTED'), str(res.get('status')))

    # ── L10 · L11 벽 표지 · 벽 제외 통계 · 무접촉 입자 ───────────────────────────────────
    #   바닥 (z − r < 0) 에 닿은 AM_P 1 · 판 (z + r > plate_z) 에 닿은 SE 1 · 내부 SE 2 · 접촉 없는 SE 1
    rP, rS = 0.006, 0.001
    zP = rP - 1e-5                                        # 바닥과 1e-5 겹침
    zS1 = zP + rP + rS - 1e-5
    zS2 = zS1 + 2 * rS - 1e-5
    zS3 = zS2 + 2 * rS - 1e-5
    pz = zS3 + rS - 2e-5                                  # 판이 맨 위 SE 와 2e-5 겹침
    A = {1: atom(1, 0.02, 0.02, zP, rP), 2: atom(2, 0.02, 0.02, zS1, rS), 3: atom(2, 0.02, 0.02, zS2, rS),
         4: atom(2, 0.02, 0.02, zS3, rS), 5: atom(2, 0.03, 0.03, 0.01, rS)}
    zs = [zP, zS1, zS2, zS3]
    rs = [rP, rS, rS, rS]
    fz = [-4e-3, -3e-3, -2e-3]
    cs = []
    for k in range(3):
        cpz_ = zs[k] + (rs[k] - 0.5e-5)
        cs.append(contact(k + 1, k + 2, (0.0, 0.0, fz[k]), (0.02, 0.02, cpz_)))
    res = lw(A, cs, TM, plate_z=pz, arrays=True)
    w = res.get('wall', {})
    chk('L10 벽 표지 — 바닥 1 (AM_P) · 판 1 (SE) · 범위 = 바닥 zplane 0 + 판 mesh (x·y 주기 가정)',
        w.get('n_floor') == 1 and w.get('n_plate') == 1 and 'floor' in str(w.get('scope')) and 'plate' in str(w.get('scope'))
        and w.get('plate_flag') == 'mesh', str(w))
    bt = w.get('by_type', {})
    chk('L10b 상별 벽 비율 — AM_P 1/1 · SE 1/4', close(bt.get('AM_P', {}).get('frac_wall'), 1.0) and close(bt.get('SE', {}).get('frac_wall'), 0.25),
        str(bt))
    chk('L10c 무접촉 입자 1 — VM 0 으로 모집단에 포함 (옛 열과 같은 모집단)', res.get('n_no_contact') == 1
        and res.get('n_particles') == 5 and res.get('arrays_vm') is not None and res['arrays_vm'][4] == 0.0, str(res.get('n_no_contact')))
    vm = res.get('arrays_vm')
    if vm is not None:
        keep = [1, 2, 4]                                  # 벽 제외 = 내부 SE (id 2 · 3) · 무접촉 SE (id 5) — 행 순서 = 원자 dict 순서
        m = sum(vm[k] for k in keep) / len(keep)
        cvn = math.sqrt(sum((vm[k] - m) ** 2 for k in keep) / len(keep)) / m * 100
        chk('L11 벽 제외 통계 = 벽 입자를 뺀 모집단의 CV · 상 비 (AM_P 는 전부 벽 → 비 없음)',
            close(res.get('vm_cv_nowall'), cvn) and 'AM_P' not in (res.get('type_stress_nowall') or {})
            and close((res.get('type_stress_nowall') or {}).get('SE', {}).get('ratio'), 1.0), f"{res.get('vm_cv_nowall')} vs {cvn}")
    else:
        chk('L11 벽 제외 통계', False, 'arrays_vm 없음')
    res = lw(A, cs, TM, plate_z=pz, src='estimated_center')
    chk('L11b 판 높이가 추정값 (mesh 없음) → 판 표지 unavailable · 벽 제외 통계 None (바닥 표지는 그대로)',
        res.get('status') == 'OK' and res.get('wall', {}).get('n_plate') is None and res.get('vm_cv_nowall') is None
        and 'unavailable' in str(res.get('wall', {}).get('plate_flag')) and res.get('wall', {}).get('n_floor') == 1,
        str(res.get('wall')))

    # ── R RGL-06 반례 (Codex 10-05) — 입력 검증 · 영 분모 · 영 척도 · 검사 범위 · 이름 한정 ─────────────────────
    rgl06(D)

    # ── L12 real_14 기준 상태 — 독립 구현 (lhs_stress_constriction_audit) 과 입자마다 대조 ─────────
    try:
        import lhs_stress_constriction_audit as AU
        import analyze_contacts as AC
        tmp = tempfile.mkdtemp(prefix='lw_real14_')
        try:
            AU.prepare_network_inputs(AU.REF_ATOMS, AU.REF_CONTACTS, AU.REF_MESH, tmp)   # 웹앱 파서 그대로
            atoms_raw, _ = AC.load_atoms_raw(os.path.join(tmp, 'atoms.csv'))
            contacts_raw, _ = AC.load_contacts_raw(os.path.join(tmp, 'contacts.csv'))
            pzr = json.load(open(os.path.join(tmp, 'mesh_info.json')))['plate_z']
            tm14 = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
            res = D.calc_love_weber_stress(atoms_raw, contacts_raw, tm14, pzr, box_x=0.05, box_y=0.05,
                                           plate_z_source='mesh', return_arrays=True)
            chk('L12 real_14 — 상태 OK (검사 셋 통과: 힘 분해 · 접촉점 · virial)', res.get('status') == 'OK',
                f"{res.get('status')} · {res.get('checks')}")
            ac, ad, box = AU.read_dump(AU.REF_ATOMS, 'ATOMS')
            cc, cd, _ = AU.read_dump(AU.REF_CONTACTS, 'ENTRIES')
            ix = {c: k for k, c in enumerate(ac)}
            ids = ad[:, ix['id']].astype(int)
            row = {a: k for k, a in enumerate(ids)}
            pos = ad[:, [ix['x'], ix['y'], ix['z']]]
            i1 = np.array([row[int(a)] for a in cd[:, 6]])
            i2 = np.array([row[int(a)] for a in cd[:, 7]])
            _sym, brch = AU.per_particle_virials(pos, i1, i2, cd[:, 9:12], cd[:, 23:26], (0.05, 0.05, None))
            if res.get('status') == 'OK':
                pid = list(res['ids'])
                Tm = np.asarray(res['tensor'])
                vol = 4.0 / 3.0 * np.pi * ad[:, ix['radius']] ** 3
                ref = np.array([brch[row[a]] / vol[row[a]] for a in pid])
                diag = np.stack([Tm[:, 0, 0], Tm[:, 1, 1], Tm[:, 2, 2]], 1)
                err = float(np.max(np.abs(diag - ref)) / np.max(np.abs(ref)))
                chk('L12b 입자마다 대각 σ_LW = 독립 구현 (branch) ÷ 부피 — 최대 상대 차 < 1e-9', err < 1e-9, f'{err:.3g}')
                chk('L12c virial 대조 (Σ V σ_LW ↔ Σ c_strs) < 1e-3 (실측 ≈ 1e-4 수준 · 허용 1e-2)',
                    isinstance(res['checks'].get('virial_total_rel'), float) and res['checks']['virial_total_rel'] < 1e-3, str(res['checks']))
                r = res['type_stress']
                chk('L12d 규약 차이 재현 — LW 에서 AM_P · AM_S 비 > 1 (옛 50/50 은 0.884 · 1.085) · SE ≈ 1',
                    r['AM_P']['ratio'] > 2.0 and r['AM_S']['ratio'] > 1.5 and 0.9 < r['SE']['ratio'] < 1.05,
                    f"{ {k: round(v['ratio'], 3) for k, v in r.items()} } · cv {res['vm_cv']:.1f}")
                wb = res['wall']
                chk('L12e 벽 표지 — 바닥 2214 · 판 1104 (z − r < 0 · z + r > plate_z · 실측)', wb.get('n_floor') == 2214 and wb.get('n_plate') == 1104,
                    f"{wb.get('n_floor')} · {wb.get('n_plate')}")
                rn = res.get('type_stress_nowall') or {}
                chk('L12f ★ RGL-06 수정 뒤에도 real_14 값 그대로 — cv 120.7 · AM_P 2.737 · AM_S 2.341 · SE 0.981 · 벽 제외 cv 122.9 · AM_P 3.016',
                    round(res['vm_cv'], 1) == 120.7 and round(r['AM_P']['ratio'], 3) == 2.737 and round(r['AM_S']['ratio'], 3) == 2.341
                    and round(r['SE']['ratio'], 3) == 0.981 and round(res.get('vm_cv_nowall') or -1, 1) == 122.9
                    and round((rn.get('AM_P') or {}).get('ratio', -1), 3) == 3.016,
                    f"cv {res['vm_cv']} · {r} · nowall {res.get('vm_cv_nowall')} · {rn}")
                chk('L12g real_14 메타 — 계약 v2 · nowall_status OK · 검사 범위 = 전역 (프레임 대응 증명 아님) · 영 척도 아님',
                    res.get('contract') == 'love_weber_checks_v2' and res.get('nowall_status') == 'OK'
                    and '전역' in str(res['checks'].get('virial_scope')) and res['checks'].get('virial_zero_scale') is False
                    and res['checks'].get('force_decomp_zero_scale') is False, f"{res.get('contract')} · {res.get('nowall_status')} · {res['checks']}")
                rs_ = ', '.join('%s %.3f' % (k, v['ratio']) for k, v in r.items())
                rn_ = ', '.join('%s %.3f' % (k, v['ratio']) for k, v in (res['type_stress_nowall'] or {}).items())
                wf_ = ', '.join('%s %.3f' % (k, v['frac_wall']) for k, v in wb['by_type'].items())
                print('     real_14 LW: cv %.1f %% · 비 %s · 벽 제외 cv %.1f %% · 비 %s · 벽 비율 %s · 비대칭 중앙 %.4f · virial %.2e'
                      % (res['vm_cv'], rs_, res['vm_cv_nowall'], rn_, wf_, res['asym_frob_median'], res['checks']['virial_total_rel']))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as e:                                # noqa: BLE001
        chk('L12 real_14 대조', False, repr(e)[:300])

    # ── L13 생산 CLI (analyze_contacts.py = 웹앱 cmd) — 새 키 · 표 · 옛 키 불변 ──────────────────
    tmp = tempfile.mkdtemp(prefix='lw_cli_')
    try:
        def bed(name, with_lw=True, cstr_scale=1.0, fz=-2e-3):
            dd_ = os.path.join(tmp, name)
            out = os.path.join(dd_, 'out')
            os.makedirs(out)
            rP_, rS_ = 0.006, 0.0005
            atoms_ = [(1, 1, 0.025, 0.025, rP_ - 1e-6, rP_)]          # 바닥에 닿은 AM_P
            zz = rP_ - 1e-6 + rP_ + rS_ - 1e-6
            for k in range(20):
                atoms_.append((2 + k, 2, 0.025, 0.025, zz + k * (2 * rS_ - 1e-6), rS_))
            plate = atoms_[-1][4] + rS_ - 2e-6
            rows_c, cstr = [], {a[0]: [0.0, 0.0, 0.0] for a in atoms_}
            for k in range(len(atoms_) - 1):
                lo, hi = atoms_[k], atoms_[k + 1]
                fzz = fz
                cpz_ = lo[4] + lo[5] - 0.5 * (lo[5] + hi[5] - (hi[4] - lo[4]))
                rows_c.append((lo[0], hi[0], fzz, cpz_))
                wv = -0.5 * (lo[4] - hi[4]) * fzz * cstr_scale
                cstr[lo[0]][2] += wv
                cstr[hi[0]][2] += wv
            with open(os.path.join(dd_, 'atoms.csv'), 'w') as fh:
                fh.write('id,type,x,y,z,radius,c_strs[1],c_strs[2],c_strs[3]\n')
                for a in atoms_:
                    s = cstr[a[0]]
                    fh.write(f'{a[0]},{a[1]},{a[2]!r},{a[3]!r},{a[4]!r},{a[5]!r},{s[0]!r},{s[1]!r},{s[2]!r}\n')
            with open(os.path.join(dd_, 'contacts.csv'), 'w') as fh:
                head = 'id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta'
                fh.write(head + (',fx,fy,fz,cp_x,cp_y,cp_z\n' if with_lw else '\n'))
                for i, j, fzz, cpz_ in rows_c:
                    base = f'{i},{j},0,0,{fzz!r},0,0,0,1e-08,1e-06'
                    fh.write(base + (f',0,0,{fzz!r},0.025,0.025,{cpz_!r}\n' if with_lw else '\n'))
            with open(os.path.join(out, 'mesh_info.json'), 'w') as fh:
                json.dump({'plate_z': plate}, fh)
            pr = subprocess.run([sys.executable, os.path.join(HERE, 'analyze_contacts_bimodal.py'), os.path.join(dd_, 'atoms.csv'),
                                 os.path.join(dd_, 'contacts.csv'), '-o', out, '-t', '1:AM_P,2:SE', '-s', '1000'],
                                capture_output=True, text=True, timeout=300)
            met = json.load(open(os.path.join(out, 'full_metrics.json'))) if os.path.exists(os.path.join(out, 'full_metrics.json')) else {}
            summ = open(os.path.join(out, 'network_summary.csv')).read() if os.path.exists(os.path.join(out, 'network_summary.csv')) else ''
            return pr, met, summ
        pr, met, summ = bed('lw')
        chk('L13 CLI rc 0 · full_metrics.json', pr.returncode == 0 and bool(met), (pr.stderr or '')[-400:])
        chk('L13b 새 키 — stress_lw_status OK · 정의 · stress_cv_lw · stress_ratio_AM_P_lw · stress_ratio_SE_lw',
            met.get('stress_lw_status') == 'OK' and met.get('stress_lw_definition') == 'love_weber_branch_full_tensor_v1'
            and all(isinstance(met.get(k), (int, float)) for k in ('stress_cv_lw', 'stress_ratio_AM_P_lw', 'stress_ratio_SE_lw')),
            str({k: v for k, v in met.items() if 'lw' in k}))
        chk('L13c 벽 키 — 바닥 1 · 판 1 · AM_P 벽 비율 1.0 · SE 1/20 · 벽 제외 CV · SE 비 (AM_P 는 벽뿐 → 키 없음)',
            met.get('stress_lw_n_wall_floor') == 1 and met.get('stress_lw_n_wall_plate') == 1
            and close(met.get('stress_lw_wall_frac_AM_P'), 1.0) and close(met.get('stress_lw_wall_frac_SE'), 0.05)
            and isinstance(met.get('stress_cv_lw_nowall'), (int, float)) and isinstance(met.get('stress_ratio_SE_lw_nowall'), (int, float))
            and 'stress_ratio_AM_P_lw_nowall' not in met,
            str({k: v for k, v in met.items() if 'wall' in k}))
        chk('L13d 검사 기록 — virial 상대 차 < 1e-9 · 접촉점/반지름 최대 ≤ 1.01',
            isinstance(met.get('stress_lw_check_virial_total_rel'), (int, float)) and met['stress_lw_check_virial_total_rel'] < 1e-9
            and isinstance(met.get('stress_lw_check_branch_over_r_max'), (int, float)) and met['stress_lw_check_branch_over_r_max'] <= 1.01,
            str({k: v for k, v in met.items() if 'check' in k}))
        import csv
        import io
        lines = [r[0] for r in csv.reader(io.StringIO(summ)) if r]
        need = ['Stress CV(%)', 'Stress CV — Love–Weber (%)', 'σ_AM_P/σ_mean — Love–Weber', 'σ_SE/σ_mean — Love–Weber',
                'Stress CV — Love–Weber · 벽 접촉 제외 (%)', 'σ_SE/σ_mean — Love–Weber · 벽 접촉 제외', '벽 접촉 입자 (%) — 바닥 · 판']
        chk('L13e 케이스 표 (network_summary.csv) — 옛 줄 뒤에 Love–Weber 줄 · 벽 제외 · 벽 접촉 비율',
            all(n in lines for n in need) and lines.index('Stress CV(%)') < lines.index('Stress CV — Love–Weber (%)'),
            str([l for l in lines if 'Stress' in l or 'σ_' in l or '벽' in l]))
        pr0, met0, summ0 = bed('old', with_lw=False)
        old_keys = ['stress_cv', 'stress_ratio_AM_P', 'stress_ratio_SE']
        chk('L13f 옛 키 값 불변 — 접촉점 열 유무와 무관 (같은 c_strs → 같은 stress_cv · 비)',
            pr0.returncode == 0 and all(met0.get(k) == met.get(k) and met.get(k) is not None for k in old_keys),
            str([(k, met0.get(k), met.get(k)) for k in old_keys]))
        chk('L13g 접촉점 열 없는 덤프 → stress_lw_status NOT_COMPUTED · LW 값 키 없음 · 표 줄 없음',
            str(met0.get('stress_lw_status', '')).startswith('NOT_COMPUTED') and 'stress_cv_lw' not in met0
            and 'Stress CV — Love–Weber (%)' not in summ0, str(met0.get('stress_lw_status')))
        pr2, met2, _ = bed('mismatch', cstr_scale=1.5)
        chk('L13h 원자 덤프 c_strs 와 접촉 덤프가 안 맞으면 (1.5 배) → FAILED 상태 · LW 값 없음 · 옛 키는 그대로',
            pr2.returncode == 0 and str(met2.get('stress_lw_status', '')).startswith('FAILED') and 'stress_cv_lw' not in met2
            and isinstance(met2.get('stress_cv'), (int, float)), str(met2.get('stress_lw_status')))
        # RGL-06 — 메타 키 · 입력 출처 · 무하중 상태가 CLI (웹앱 접촉 단계) 를 지나 full_metrics.json 에 그대로 남는다
        import hashlib

        def _dg(path):
            with open(path, 'rb') as fh:
                return hashlib.sha256(fh.read()).hexdigest()[:16]
        chk('L13i ★ RGL-06 메타 키 — 계약 v2 · quantity (입자 접촉력 대칭 응력 VM) · 덱 가정 미검증 · virial 범위 (전역) · nowall_status OK',
            met.get('stress_lw_contract') == 'love_weber_checks_v2' and '입자 접촉력' in str(met.get('stress_lw_quantity'))
            and '검증' in str(met.get('stress_lw_assumptions_unverified')) and '전역' in str(met.get('stress_lw_check_virial_scope'))
            and met.get('stress_lw_nowall_status') == 'OK' and '선별 모집단' in str(met.get('stress_lw_nowall_scope')),
            str({k: v for k, v in met.items() if k.startswith('stress_lw_') and 'frac' not in k}))
        dd_lw = os.path.join(tmp, 'lw')
        chk('L13j 입력 출처 — LW 가 읽은 CSV 의 sha256 앞 16 자 (망 단계 network_provenance.json input_digests 와 같은 꼴) · '
            'TIMESTEP 은 CSV 에 없음 표기',
            met.get('stress_lw_input_digest_atoms') == _dg(os.path.join(dd_lw, 'atoms.csv'))
            and met.get('stress_lw_input_digest_contacts') == _dg(os.path.join(dd_lw, 'contacts.csv'))
            and 'unavailable' in str(met.get('stress_lw_timestep')),
            str({k: met.get(k) for k in ('stress_lw_input_digest_atoms', 'stress_lw_input_digest_contacts', 'stress_lw_timestep')}))
        pr3, met3, summ3 = bed('zero', fz=0.0)
        chk('L13k ★ 무하중 침대 (접촉 힘 0 · c_strs 0) → stress_lw_status UNDEFINED (zero_load …) · LW 값 키 없음 · 표 줄 없음 · 옛 키 그대로',
            pr3.returncode == 0 and str(met3.get('stress_lw_status', '')).startswith('UNDEFINED (zero_load') and 'stress_cv_lw' not in met3
            and not any(k.startswith('stress_ratio_') and k.endswith('_lw') for k in met3)
            and 'Stress CV — Love–Weber (%)' not in summ3 and 'stress_cv' in met3,
            f"rc {pr3.returncode} · {met3.get('stress_lw_status')} · {(pr3.stderr or '')[-300:]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\n{N[0] - len(FAILS)}/{N[0]} 통과' + ('' if not FAILS else '  — 실패: ' + ' · '.join(FAILS)))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
