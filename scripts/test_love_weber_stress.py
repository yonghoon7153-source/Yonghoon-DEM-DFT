#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""④b Love–Weber 입자 응력 — 시험 (J20-s · 1저자 비준 10-04 *"권고대로"* · 원장 LHS-29).

옛 열 (`stress_cv` · `stress_ratio_<상>`) = LIGGGHTS `compute stress/atom` 의 입자 접촉 몫 (0.5 · (x_i − x_j) ⊗ F 를 두 입자에
똑같이 — 50/50 분할) · 대각 성분만.  새 열 = 접촉 덤프 (힘 · 접촉점) 로 계산한 **Love–Weber** 입자 평균 응력
σ_i = (1/V_i) Σ_c (x_c − x_i) ⊗ f_c  (f_c = 접촉 c 가 입자 i 에 주는 힘 · 인장 양수 = c_strs 와 같은 부호) — 전체 텐서의 대칭부로 VM.
벽 (바닥 zplane 0 · 판 mesh) 접촉은 두 규약 다 없다 → 벽에 닿은 입자 표지 · 벽 제외 통계.

  python3 scripts/test_love_weber_stress.py

기대값은 손으로 (또는 독립 구현 `lhs_stress_constriction_audit.per_particle_virials` 로) 셈한다 — 생산 함수를 다시 부르지 않는다.
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
        def bed(name, with_lw=True, cstr_scale=1.0):
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
                fzz = -2e-3
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
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\n{N[0] - len(FAILS)}/{N[0]} 통과' + ('' if not FAILS else '  — 실패: ' + ' · '.join(FAILS)))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
