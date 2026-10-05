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

P 묶음 = 원장 RGLR-03 (Codex 10-05 재검증 · P2) — 존재하지만 손상된 c_strs (NaN · 문자열 · 일부 열) 가 파서에서 "없음" 으로 바뀌어
LW 전역 virial 검사가 꺼지던 것.  디스크의 실제 CSV → 실제 `load_atoms_raw` → `calc_love_weber_stress` (Codex `lw_replay.py` dimer
그대로: 반경 1 · 중심 간격 1.8 · 힘 1 · 참 z virial −0.9) · 직접 dict 의 "세 키 중 일부만" (any-present ↔ all-complete).
S 묶음 = 원장 LHS-33 (좁은 개정 · 1저자 비준 10-05 · Codex 재검증 Q7) — 옛 σ_VM 열 (`stress_cv` · `stress_ratio_<상>` ·
`stress_z_layer_cv`) 의 무효 · 미정의 입력이 0 (거짓 최고 등급) 이던 것 → None + 상태 (computed · unavailable_no_c_strs ·
invalid_input · undefined_zero_mean) + 계약 표지 v2-invalid-null.  정상 입력은 옛 함수 (아래 `_old_*` — 옛 판 그대로 옮긴 대조용) 와
정의 · 수치 · 키가 비트 동일.  소비자 (등급 · 표 재생성 · 그룹 그림 · 내보내기 · CLI) 가 상태를 따른다.
V 묶음 = RGLR2-03 (Codex 3차 재검증 10-05 · P2 · Q4 · 1저자 비준 "권고대로" = 안정식 · 혼합) — 거의 정수압 입자에서 전개식 근호가
부호까지 잃어 (Codex 반례: 정확 1.15e-14 ↔ 계산 −4.66e-10) v2 의 0 clamp 가 정확히 같은 두 VM 의 CV 를 100 % 로 지어냈다 → 근호가 엄밀 오차
상한의 2^20 배 안이면 (분해 안 됨) 같은 양의 소거 없는 꼴 ½Σ(σ_i − σ_j)² 로 다시 센다 · 분해된 입자는 옛 식 값 그대로 (비트 동일) · 계약
v3-invalid-null-stable-vm.  기대값 = 입력 float 를 유리수 (fractions.Fraction) 로 정확히 바꾼 불변량의 제곱근 (decimal 60 자리) — 생산 함수 미사용.
"""
import decimal
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction

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


# ── 옛 판 그대로 (대조용 · 10-05 fde4a812c 의 analyze_contacts.load_atoms_raw · dem_analysis_core.calc_von_mises_stress) ─────────
#   정상 입력에서 새 판이 이 둘과 dict 내용 · 수치가 **비트 동일**해야 한다 (RGLR-03 · LHS-33 계약 — 정상 입력 불변).
def _old_load_atoms_raw(csv_path):
    import pandas as pd
    df = pd.read_csv(csv_path)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['id'] = df['id'].astype(int)
    df['type'] = df['type'].astype(int)
    atoms = {}
    for _, row in df.iterrows():
        atom = {
            'type': int(row['type']),
            'x': row['x'], 'y': row['y'], 'z': row['z'],
            'radius': row['radius'],
        }
        if 'c_strs[1]' in row and not pd.isna(row['c_strs[1]']):
            vol = (4.0 / 3.0) * np.pi * row['radius']**3
            if vol > 0:
                atom['sigma_xx'] = row['c_strs[1]'] / vol
                atom['sigma_yy'] = row['c_strs[2]'] / vol
                atom['sigma_zz'] = row['c_strs[3]'] / vol
        atoms[int(row['id'])] = atom
    return atoms, df


def _old_von_mises(atoms_raw, type_map, scale, plate_z, n_layers=10):
    sample = next(iter(atoms_raw.values()))
    if 'sigma_xx' not in sample:
        return None
    vm_data = {}
    for aid, a in atoms_raw.items():
        sxx = a.get('sigma_xx', 0)
        syy = a.get('sigma_yy', 0)
        szz = a.get('sigma_zz', 0)
        vm = np.sqrt(sxx**2 + syy**2 + szz**2 - sxx*syy - syy*szz - sxx*szz)
        vm_data[aid] = vm
    all_vm = np.array(list(vm_data.values()))
    vm_mean = float(np.mean(all_vm))
    vm_std = float(np.std(all_vm))
    vm_cv = (vm_std / vm_mean * 100) if vm_mean > 0 else 0
    type_stress = {}
    for t_name in set(type_map.values()):
        t_ids = [aid for aid, a in atoms_raw.items() if type_map.get(a['type']) == t_name]
        if t_ids:
            t_vm = np.array([vm_data[aid] for aid in t_ids])
            type_stress[t_name] = {
                'mean': float(np.mean(t_vm)),
                'ratio': float(np.mean(t_vm) / vm_mean) if vm_mean > 0 else 0,
            }
    z_layer_cv = []
    z_min, z_max = 0.0, plate_z
    layer_edges = np.linspace(z_min, z_max, n_layers + 1)
    atom_ids = list(atoms_raw.keys())
    atom_z = np.array([atoms_raw[aid]['z'] for aid in atom_ids])
    atom_vm = np.array([vm_data[aid] for aid in atom_ids])
    for i in range(n_layers):
        mask = (atom_z >= layer_edges[i]) & (atom_z < layer_edges[i+1])
        if mask.sum() > 1:
            layer_vm = atom_vm[mask]
            layer_mean = np.mean(layer_vm)
            layer_cv = (np.std(layer_vm) / layer_mean * 100) if layer_mean > 0 else 0
            z_mid = (layer_edges[i] + layer_edges[i+1]) / 2 * scale
            z_layer_cv.append({
                'z_mid_um': float(z_mid),
                'cv': float(layer_cv),
                'mean_normalized': float(layer_mean / vm_mean) if vm_mean > 0 else 0,
            })
    return {'vm_cv': vm_cv, 'vm_mean': vm_mean, 'type_stress': type_stress, 'z_layer_cv': z_layer_cv}


def _same_vm(new, old):
    """정상 입력 대조 — 옛 네 키 (vm_cv · vm_mean · type_stress · z_layer_cv) 가 정확히 같다 (float == · 키 순서 무관)."""
    return (isinstance(new, dict) and isinstance(old, dict)
            and all(new.get(k) == old.get(k) for k in ('vm_cv', 'vm_mean', 'type_stress', 'z_layer_cv')))


# ── RGLR2-03 (옛 σ_VM 근호의 수치 분해) — 시험이 독립으로 다시 적는 규칙 · 정확 산술 ─────────────────────────────────────
VM_CONTRACT = 'v3-invalid-null-stable-vm'      # 옛 σ_VM 열 계약 — v2 (LHS-33 · 음수 근호 0 clamp) 의 다음 세대 (안정식 혼합)
_VM_EPS = 2.0 ** -52                            # binary64 ε (= sys.float_info.epsilon)
_VM_C, _VM_ABS, _VM_K = 16, 2.0 ** -1071, 2 ** 20   # 엄밀 상한 B = 16·ε·Ŝ + 2^-1071 · 분해됨 ⇔ 근호 > 2^20·B (dem_analysis_core ★ RGLR2-03 유도)


def _rad_old(t):
    """옛 전개식 근호 그대로 (생산 · v2 와 같은 연산 · 같은 순서)."""
    x, y, z = t
    return x**2 + y**2 + z**2 - x*y - y*z - x*z


def _sq_sum(t):
    x, y, z = t
    return x**2 + y**2 + z**2


def _rad_exact(t):
    """입력 float 그대로를 유리수로 — 정확한 불변량 ½[(σxx−σyy)² + (σyy−σzz)² + (σzz−σxx)²] (Fraction)."""
    x, y, z = (Fraction(float(v)) for v in t)
    return ((x - y) ** 2 + (y - z) ** 2 + (z - x) ** 2) / 2


def _vm_exact(t):
    """정확 VM = √(정확 불변량) — decimal 60 자리 (생산 함수를 부르지 않는다)."""
    r = _rad_exact(t)
    with decimal.localcontext() as ctx:
        ctx.prec = 60
        return (decimal.Decimal(r.numerator) / decimal.Decimal(r.denominator)).sqrt()


def _ulps(x, ex):
    """|x − 정확| / ulp(x) — 정확이 0 이면 x 도 0 일 때만 0."""
    try:
        x = float(x)
    except (TypeError, ValueError):
        return math.inf
    if not math.isfinite(x):
        return math.inf
    if ex == 0:
        return 0.0 if x == 0 else math.inf
    with decimal.localcontext() as ctx:
        ctx.prec = 60
        return float(abs(decimal.Decimal(x) - ex) / decimal.Decimal(math.ulp(x)))


def _v2_vm(t):
    """v2 (LHS-33 · af9e6b15f) 의 한 입자 규칙 그대로 — 근호 음수면 0 clamp · 양의 쓰레기는 그대로 (반례 확인 전용)."""
    v = _rad_old(t)
    return np.sqrt(v) if not v < 0 else np.float64(0.0)


def _cv_pct(vms):
    """생산과 같은 통계 — 모집단 std / mean × 100."""
    a = np.array(vms, dtype=float)
    return float(np.std(a)) / float(np.mean(a)) * 100 if float(np.mean(a)) > 0 else float('nan')


def _vm_rule_stable(t):
    """판정 규칙을 시험이 독립으로 — 유한 · 영 텐서 아님 · 근호 ≤ 2^20 · (16 ε Ŝ + 2^-1071) 이면 안정식."""
    v = _rad_old(t)
    if v != v or v in (math.inf, -math.inf) or all(float(c) == 0.0 for c in t):
        return False
    return not v > _VM_K * (_VM_C * _VM_EPS * _sq_sum(t) + _VM_ABS)


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


def rglr03(D):
    """원장 RGLR-03 (Codex 10-05 재검증 · P2) — 옛 파서는 c_strs 첫 성분이 NaN (문자열 → coerce NaN 포함) 이면 세 sigma 키를 모두 안 써서
    "손상" 을 "c_strs 없음" 으로 바꿨다 → LW 가 virial unavailable 로 OK (틀린 virial −2.7 도 통과).  함수도 has_cs = all(세 키) 라
    "아무 키 없음" ↔ "불완전 튜플" 을 못 갈랐다.  ⇒ 세 원천 열이 **전부** 없을 때만 미제공 (OK · unavailable — 옛 입력 호환) ·
    일부 열 · 비유한 · 파싱 실패 · 일부 키 = FAILED (invalid_input …)."""
    import analyze_contacts as AC
    TM = {1: 'AM_P', 2: 'SE'}
    st = lambda r: str(r.get('status', ''))           # noqa: E731
    FULL = ('c_strs[1]', 'c_strs[2]', 'c_strs[3]')
    tmp = tempfile.mkdtemp(prefix='lw_rglr03_')

    def csv_txt(head, first, zz=-0.9, second='0'):
        """Codex dimer atoms.csv — head = 있는 c_strs 열 (빈 튜플 = 열 전무) · first = c_strs[1] 칸의 글자 그대로."""
        val = {'c_strs[1]': first, 'c_strs[2]': second, 'c_strs[3]': repr(zz)}
        rows = [f'{i},1,2,2,{z!r},1' + ''.join(',' + val[c] for c in head) for i, z in ((1, 2.0), (2, 3.8))]
        return ','.join(('id', 'type', 'x', 'y', 'z', 'radius') + tuple(head)) + '\n' + '\n'.join(rows) + '\n'

    def run(name, head=FULL, first='0', zz=-0.9, second='0'):
        try:
            a, c = load_pair(tmp, name, csv_txt(head, first, zz, second), [dimer_contact(1, 2.0, 1.0)])
            return a, lw(a, c, TM, plate_z=20.0)
        except Exception as e:                            # noqa: BLE001 — 옛 파서는 일부 열 덤프에서 KeyError 로 죽었다
            return {}, {'status': f'EXC {type(e).__name__}: {e}'}
    try:
        a, r = run('p1')
        ck = r.get('checks', {})
        chk('P1 정상 (0, 0, −0.9) 실 CSV → 실 파서 → OK · virial 검사됨 · 상대 잔차 ≈ 1e-16',
            st(r) == 'OK' and ck.get('virial_status') == 'checked' and isinstance(ck.get('virial_total_rel'), float)
            and ck['virial_total_rel'] < 1e-12, f"{st(r)} · {ck}")
        V = (4.0 / 3.0) * np.pi * 1.0 ** 3
        chk('P1b 정상 행 dict 는 옛 꼴 그대로 — 키 8 개 (type · x · y · z · radius · sigma 셋) · sigma_zz = −0.9 ÷ (4/3 π r³) 비트 동일',
            all(set(x) == {'type', 'x', 'y', 'z', 'radius', 'sigma_xx', 'sigma_yy', 'sigma_zz'} for x in a.values())
            and all(x['sigma_zz'] == -0.9 / V and x['sigma_xx'] == 0.0 for x in a.values()), repr(a)[:300])
        a, r = run('p2', head=())
        chk('P2 c_strs 세 열 전무 (옛 덱 · 손 픽스처) → OK · virial unavailable (옛 입력 호환 — 거부 아님) · sigma 키 없음',
            st(r) == 'OK' and 'unavailable' in str(r.get('checks', {}).get('virial_status'))
            and not any(k.startswith('sigma_') for x in a.values() for k in x), f"{st(r)} · {r.get('checks')}")
        a, r = run('p3', head=('c_strs[1]', 'c_strs[3]'))
        chk('P3 ★ 열 일부만 (c_strs[2] 없음) → FAILED (invalid_input …) — 옛 파서는 KeyError 로 죽었다',
            st(r).startswith('FAILED (invalid_input') and 'c_strs' in st(r), st(r))
        a, r = run('p3b', head=('c_strs[2]', 'c_strs[3]'))
        chk('P3b ★ 첫 열만 없음 (c_strs[2] · [3] 만) → FAILED (invalid_input …) — 옛 파서는 조용히 "c_strs 없음" · OK',
            st(r).startswith('FAILED (invalid_input') and 'c_strs' in st(r), st(r))
        a, r = run('p4', first='nan')
        chk('P4 ★ 첫 열 NaN → FAILED (invalid_input …) — 옛 코드 OK · virial unavailable',
            st(r).startswith('FAILED (invalid_input') and 'c_strs' in st(r), st(r))
        chk('P4b 파서가 존재를 보존 — 세 sigma 키가 있고 sigma_xx 는 NaN · 손상 사유 (c_strs[1]) 를 입자에 남긴다',
            bool(a) and all(all(k in x for k in ('sigma_xx', 'sigma_yy', 'sigma_zz')) and x['sigma_xx'] != x['sigma_xx']
                            and 'c_strs[1]' in str(x.get('c_strs_invalid', '')) for x in a.values()), repr(a)[:300])
        a, r = run('p5', first='invalid')
        chk('P5 ★ 첫 열 문자열 → FAILED (invalid_input …) · 사유에 파싱 실패 열 (c_strs[1]) — 옛 코드 OK',
            st(r).startswith('FAILED (invalid_input') and 'c_strs[1]' in st(r), st(r))
        a, r = run('p6', first='inf')
        chk('P6 첫 열 Inf → FAILED (invalid_input …) (옛 코드도 FAILED — 같은 범주 유지)',
            st(r).startswith('FAILED (invalid_input') and 'c_strs' in st(r), st(r))
        a, r = run('p7', zz=-2.7)
        chk('P7 유한한 틀린 virial (−2.7) → FAILED (virial_mismatch …) · 상대 0.667', st(r).startswith('FAILED (virial_mismatch')
            and close(r.get('checks', {}).get('virial_total_rel'), 2.0 / 3.0, rel=1e-9), f"{st(r)} · {r.get('checks')}")
        a, r = run('p8', first='nan', zz=-2.7)
        chk('P8 ★ NaN 한 칸이 틀린 virial 을 숨기지 않는다 (NaN, 0, −2.7) → FAILED (invalid_input …) — 옛 코드 OK',
            st(r).startswith('FAILED (invalid_input'), st(r))
        a, r = run('p8b', second='')
        chk('P8b 한 칸 빈칸 (c_strs[2] 비움) → FAILED (invalid_input …)', st(r).startswith('FAILED (invalid_input'), st(r))
        c = [contact(1, 2, (0.0, 0.0, -1.0), (2.0, 2.0, 2.9))]
        a = {1: atom(1, 2.0, 2.0, 2.0, 1.0, (0.0, 0.0, -0.9)), 2: atom(1, 2.0, 2.0, 3.8, 1.0, (0.0, 0.0, -0.9))}
        for x in a.values():
            x.pop('sigma_xx')
        r = lw(a, c, TM, plate_z=20.0)
        chk('P9 ★ 직접 dict — 모든 입자에서 sigma_xx 만 없음 (나머지 둘 있음) → FAILED (invalid_input: c_strs …) — 옛 코드 unavailable · OK',
            st(r).startswith('FAILED (invalid_input') and 'c_strs' in st(r), st(r))
        a = {1: atom(1, 2.0, 2.0, 2.0, 1.0), 2: atom(1, 2.0, 2.0, 3.8, 1.0)}
        r = lw(a, c, TM, plate_z=20.0)
        chk('P9b 직접 dict — 세 키 모두 전무 → OK · unavailable (옛 호환)', st(r) == 'OK'
            and 'unavailable' in str(r.get('checks', {}).get('virial_status')), st(r))
        rad_nan = 'id,type,x,y,z,radius,c_strs[1],c_strs[2],c_strs[3]\n1,1,2,2,2.0,1,0,0,-0.9\n2,1,2,2,3.8,nan,0,0,-0.9\n'
        a2, _ = AC.load_atoms_raw(os.path.join(tmp, 'p1', 'atoms.csv'))
        p = os.path.join(tmp, 'p10.csv')
        with open(p, 'w') as fh:
            fh.write(rad_nan)
        a10, _ = AC.load_atoms_raw(p)
        chk('P10 c_strs 는 있는데 반경 NaN → 그 입자는 sigma 키를 NaN 으로 남긴다 (옛 파서는 키를 빼 "c_strs 없음" 과 섞었다) · 사유 기록',
            all(k in a10[2] for k in ('sigma_xx', 'sigma_yy', 'sigma_zz')) and a10[2]['sigma_zz'] != a10[2]['sigma_zz']
            and str(a10[2].get('c_strs_invalid', '')) != '' and a10[1] == a2[1], repr(a10)[:300])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def lhs33(D):
    """원장 LHS-33 (좁은 개정 · 1저자 비준 10-05 · Codex 재검증 Q7) — 옛 σ_VM 열의 무효 · 미정의 입력이 0 (`mean > 0 else 0` ·
    `a.get(…, 0)` · NaN 하나가 평균을 NaN 으로 → `NaN > 0` 이 False → CV 0) → 등급 축 '기계적 안정성' (낮을수록 좋음) 거짓 최고 등급.
    정상 입력 = 정의 · 수치 · 키 그대로 (옛 함수 `_old_von_mises` 와 비트 동일) · 균일한 양의 VM 이면 0.0 (정상 0) 그대로."""
    TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    cvf = getattr(D, 'calc_von_mises_stress')

    def vm(atoms, pz=1.0):
        try:
            return cvf(atoms, TM, 1000.0, pz)
        except Exception as e:                            # noqa: BLE001 — 옛 판은 빈 입력에서 StopIteration
            return {'status': f'EXC {type(e).__name__}: {e}'}

    def sat(t, z, s):
        return {'type': t, 'x': 0.0, 'y': 0.0, 'z': z, 'radius': 1e-3, 'sigma_xx': s[0], 'sigma_yy': s[1], 'sigma_zz': s[2]}
    bad = lambda r: (isinstance(r, dict) and r.get('vm_cv', 0) is None and r.get('z_layer_cv', 0) is None      # noqa: E731
                     and all(v.get('ratio', 0) is None for v in (r.get('type_stress') or {}).values()))
    gen = lambda r: isinstance(r, dict) and r.get('contract') == VM_CONTRACT                                    # noqa: E731
    #  S1 c_strs 전무 — 옛 판: None (그래서 analyze_contacts 가 키를 안 썼고 소비자 `_get(…, 0)` 이 0 으로 읽었다)
    r = vm({1: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': 0.1, 'radius': 1e-3}, 2: {'type': 3, 'x': 0.0, 'y': 0.0, 'z': 0.2, 'radius': 1e-3}})
    chk(f'S1 ★ c_strs 전무 → status unavailable_no_c_strs · vm_cv · 상 비 · z 층 None · 계약 {VM_CONTRACT} (옛 판 None — 소비자가 0 으로 읽었다)',
        bad(r) and r.get('status') == 'unavailable_no_c_strs' and gen(r), repr(r)[:300])
    #  S2 한 입자 NaN — 옛 판: 평균 NaN → `NaN > 0` False → CV 0 · 비 0 (거짓 최고 등급)
    r = vm({1: sat(1, 0.1, (1.0, 0.0, 0.0)), 2: sat(3, 0.2, (float('nan'), 0.0, 0.0)), 3: sat(3, 0.3, (2.0, 0.0, 0.0))})
    chk('S2 ★ 한 입자 sigma NaN → status invalid_input · 값 None (옛 판 CV 0 · 비 0)', bad(r) and r.get('status') == 'invalid_input'
        and gen(r) and r.get('reason'), repr(r)[:300])
    #  S3 무하중 — 0/0
    r = vm({k: sat(1 + k % 3, 0.1 * k, (0.0, 0.0, 0.0)) for k in range(1, 7)})
    chk('S3 ★ 무하중 (σ 전부 0) → status undefined_zero_mean · CV · 상 비 · z 층 None (옛 판 0 · 0 = 거짓 0)',
        bad(r) and r.get('status') == 'undefined_zero_mean' and gen(r) and r.get('reason'), repr(r)[:300])
    r = vm({k: sat(1 + k % 3, 0.1 * k, (-2.0 * k, -2.0 * k, -2.0 * k)) for k in range(1, 7)})
    chk('S3b 전 입자 정수압 (σxx = σyy = σzz ≠ 0) → VM 0 → undefined_zero_mean (옛 판: 근호 안 반올림 음수 → NaN → CV 0)',
        bad(r) and r.get('status') == 'undefined_zero_mean', repr(r)[:300])
    #  S4 한 입자만 sigma 키 없음 — 옛 판: `a.get(…, 0)` → 0 으로 읽어 정상 값처럼 계산
    r = vm({1: sat(1, 0.1, (1.0, 0.0, 0.0)), 2: {'type': 3, 'x': 0.0, 'y': 0.0, 'z': 0.2, 'radius': 1e-3}, 3: sat(3, 0.3, (2.0, 0.0, 0.0))})
    chk('S4 ★ 한 입자만 c_strs 결측 → invalid_input · 값 None (옛 판: 0 으로 읽어 CV 를 냈다)', bad(r) and r.get('status') == 'invalid_input', repr(r)[:300])
    #  S5 정상 0 — 균일한 양의 VM
    r = vm({k: sat(1 + k % 3, 0.1 * k, (3.0, 1.0, 1.0)) for k in range(1, 7)})
    chk('S5 균일한 양의 VM (모든 입자 같은 σ) → vm_cv 0.0 · status computed (정상 0 은 그대로 0)',
        isinstance(r, dict) and r.get('vm_cv') == 0.0 and r.get('status') == 'computed' and gen(r)
        and all(v.get('ratio') == 1.0 for v in r.get('type_stress', {}).values()), repr(r)[:300])
    #  S6 정상 침대 (현실적 소형 · 3 상 · 같은 시드) — 옛 함수와 비트 동일 + 상태 표지
    rng = np.random.RandomState(20261005)
    at = {}
    for k in range(1, 91):
        t = 1 + k % 3
        rr = (6e-3, 2e-3, 5e-4)[t - 1]
        cs_ = rng.normal(-1.0, 0.6, 3) * 10.0 ** rng.uniform(-6, -3)
        v_ = (4.0 / 3.0) * np.pi * rr ** 3
        at[k] = {'type': t, 'x': float(rng.uniform(0, 0.05)), 'y': float(rng.uniform(0, 0.05)), 'z': float(rng.uniform(0, 0.03)),
                 'radius': rr, 'sigma_xx': np.float64(cs_[0]) / v_, 'sigma_yy': np.float64(cs_[1]) / v_, 'sigma_zz': np.float64(cs_[2]) / v_}
    at[91] = dict(at[3], sigma_xx=np.float64(0.0), sigma_yy=np.float64(0.0), sigma_zz=np.float64(0.0))   # 접촉 없는 입자 (c_strs 0)
    r_new, r_old = vm(at, pz=0.03), _old_von_mises(at, TM, 1000.0, 0.03)
    chk('S6 ★ 정상 침대 (3 상 91 입자 · 무접촉 하나) — vm_cv · vm_mean · 상 mean/ratio · z 층 전부 옛 함수와 비트 동일 · status computed · 계약 표지 · '
        '안정식으로 다시 센 입자 0 (RGLR2-03 — 무접촉 영 텐서도 옛 값 0 그대로)',
        _same_vm(r_new, r_old) and r_new.get('status') == 'computed' and gen(r_new) and len(r_old['z_layer_cv']) >= 5
        and r_new.get('vm_stable_recomputed_n') == 0,
        f"{repr(r_new)[:200]} vs {repr(r_old)[:200]} · 다시 셈 {r_new.get('vm_stable_recomputed_n')}")
    #  S7 정수압 한 입자 — 근호 안이 반올림으로 음수가 되는 값 (해석적으로 0) · 옛 판: 그 입자 NaN → 평균 NaN → CV 0
    xh = next(v for v in (1.0 + 0.0731 * k for k in range(1, 500)) if v ** 2 + v ** 2 + v ** 2 - v * v - v * v - v * v < 0)
    r = vm({1: sat(1, 0.1, (xh, xh, xh)), 2: sat(3, 0.2, (1.0, 0.0, 0.0)), 3: sat(3, 0.3, (2.0, 0.0, 0.0))})
    chk(f'S7 ★ 정수압 입자 (σ = {xh:.4f} 셋 — 근호 안 반올림 음수) 가 섞인 정상 침대 → computed · CV = 손값 √(2/3)·100 (그 입자 VM 0) — '
        '옛 판 NaN → CV 0 (거짓 최고 등급)', isinstance(r, dict) and r.get('status') == 'computed'
        and close(r.get('vm_cv'), math.sqrt(2.0 / 3.0) * 100, rel=1e-12), repr(r)[:300])
    chk('S7b (반례 확인) 옛 판은 같은 입력에서 CV 0 을 냈다',
        _old_von_mises({1: sat(1, 0.1, (xh, xh, xh)), 2: sat(3, 0.2, (1.0, 0.0, 0.0)), 3: sat(3, 0.3, (2.0, 0.0, 0.0))},
                       TM, 1000.0, 1.0)['vm_cv'] == 0)
    r = vm({})
    chk('S8 원자 0 → invalid_input · 값 None (옛 판 StopIteration 예외)', isinstance(r, dict) and r.get('status') == 'invalid_input'
        and r.get('vm_cv', 0) is None, repr(r)[:200])
    r = vm({1: sat(1, 0.1, (1e200, -1e200, 0.0)), 2: sat(3, 0.2, (1.0, 0.0, 0.0))})
    chk('S8b σ² 넘침 (1e200) → invalid_input · 값 None (넘친 평균을 정상 통계로 내지 않는다)', bad(r) and r.get('status') == 'invalid_input', repr(r)[:200])

    #  S9 등급 소비자 — 무효 · 미정의는 등급 안 매김 (최고 등급 아님) · 정상 · 옛 세대는 그대로
    import grade_engine as G
    lab = next(ax['label'] for ax in G.AXES if ax.get('key') == '__sigma_vm_cv_pct')
    m_bad = {'stress_cv': None, 'stress_cv_status': 'invalid_input', 'stress_cv_reason': 'c_strs 비유한 1 / 2 입자',
             'stress_cv_contract': 'v2-invalid-null'}
    m_zero = {'stress_cv': 0.0, 'stress_cv_status': 'undefined_zero_mean', 'stress_cv_contract': 'v2-invalid-null'}
    m_ok = {'stress_cv': 213.1, 'stress_cv_status': 'computed', 'stress_cv_contract': 'v2-invalid-null'}
    v_bad, v_zero = G.axis_values(dict(m_bad)).get(lab), G.axis_values(dict(m_zero)).get(lab)
    v_ok, v_old = G.axis_values(dict(m_ok)).get(lab), G.axis_values({'stress_cv': 213.1}).get(lab)
    chk('S9 ★ 등급 축 값 — 무효 None · 상태가 미정의인데 저장된 0 도 None (최고 등급 아님) · 정상 213.1 · 옛 세대 (상태 키 없음) 213.1',
        v_bad is None and v_zero is None and v_ok == 213.1 and v_old == 213.1, repr((v_bad, v_zero, v_ok, v_old)))
    row = next((a_ for a_ in G.build_overall_grade(dict(m_bad))['axes'] if a_['label'] == lab), {})
    chk('S9b 등급 행 — 점수 없음 · 등급 "—" · basis 에 사유 (LHS-33 · 0 으로 읽지 않음)',
        row.get('score') is None and row.get('grade') == '—' and 'LHS-33' in str(row.get('basis')) and 'invalid_input' in str(row.get('basis')),
        repr(row)[:300])
    row = next((a_ for a_ in G.build_overall_grade(dict(m_ok))['axes'] if a_['label'] == lab), {})
    chk('S9c 정상 → 점수 있음 (값 213.1 그대로)', row.get('value') == 213.1 and row.get('score') is not None, repr(row)[:200])

    #  S10 표 재생성 (rebuild_tables_from_metrics) — 무효면 0 줄 없이 상태 줄 (사유) · 정상은 옛 줄 그대로
    import rebuild_tables_from_metrics as RB
    ROW = 'Stress CV 상태 (50/50 · LHS-33)'
    rows = RB.network_summary(dict(m_bad, stress_ratio_SE=None, stress_ratio_AM_P=None))
    d_ = {x['지표']: x['값'] for x in (rows or [])}
    chk('S10 ★ 표 재생성 — 무효면 상태 줄 (상태 · 사유) · "Stress CV(%)" 숫자 줄 없음 (0 으로 안 채움)',
        ROW in d_ and 'invalid_input' in str(d_[ROW]) and 'c_strs 비유한' in str(d_[ROW]) and 'Stress CV(%)' not in d_
        and '── 응력 ──' in d_, repr(d_)[:300])
    rows = RB.network_summary(dict(m_ok, stress_ratio_SE=0.999))
    d_ = {x['지표']: x['값'] for x in (rows or [])}
    chk('S10b 정상 — 옛 줄 그대로 (Stress CV 213.1 · σ_SE 0.999) · 상태 줄 없음', d_.get('Stress CV(%)') == 213.1
        and d_.get('σ_SE/σ_mean') == 0.999 and ROW not in d_, repr(d_)[:300])
    import metrics_json as MJ
    chk(f'S10c 상태 줄 이름 · 계약 표지 = metrics_json 한 곳 (analyze_contacts · 표 재생성 · 웹앱이 같은 상수) · 현재 세대 {VM_CONTRACT} · '
        '이전 세대 v2-invalid-null 도 알려진 세대 (저장된 결과 그대로 읽는다)',
        getattr(MJ, 'STRESS_CV_STATUS_ROW', None) == ROW and getattr(MJ, 'STRESS_CV_CONTRACT', None) == VM_CONTRACT
        and getattr(D, 'STRESS_CV_CONTRACT', None) == VM_CONTRACT
        and tuple(getattr(MJ, 'STRESS_CV_CONTRACTS', ())) == ('v2-invalid-null', VM_CONTRACT))

    #  S11 그룹 그림 · 내보내기 · 잔차 상관 — None 을 0 으로 바꾸지 않는다
    import matplotlib
    matplotlib.use('Agg')
    import generate_comparison_plots as GP
    data = [dict(m_ok), dict(m_bad), dict(m_zero), {'stress_cv': 150.0}]
    ax = GP.plot_stress_cv(data, ['a', 'b', 'c', 'd'], ax=matplotlib.pyplot.subplots()[1])
    old_line = [list(l.get_xdata()) for l in ax.get_lines() if l.get_linestyle() in ('--', 'dashed')]
    chk('S11 Stress CV 그림 (옛 규약 선) — 무효 · 미정의 케이스는 점이 없다 (저장된 0 도 상태를 따른다) · 정상 · 옛 세대만',
        old_line and sorted(old_line[0]) == [0, 3], repr(old_line))
    fx = getattr(GP, '_stress_cv_feature', None)
    chk('S11b 잔차 상관 특징 — 무효 · 미정의 = NaN (옛 판 `_get(d, "stress_cv", 0)` = 0) · 정상 = 값',
        callable(fx) and fx(m_bad) != fx(m_bad) and fx(m_zero) != fx(m_zero) and fx(m_ok) == 213.1 and fx({}) != fx({}))
    ex = getattr(GP, '_stress_export_cells', None)
    cells = ex(m_bad) if callable(ex) else {}
    chk('S11c 내보내기 칸 — 무효면 빈칸 (0 아님) + 상태 열에 사유 · 정상은 값',
        callable(ex) and cells.get('stress_cv') == '' and 'invalid_input' in str(cells.get('status'))
        and ex(m_ok).get('stress_cv') == 213.1 and ex(m_ok).get('status') == 'computed', repr(cells))


def rglr2_03(D):
    """원장 RGLR2-03 (Codex 3차 재검증 10-05 · P2 · Q4 · 1저자 비준 "권고대로" = 안정식 · 혼합) — 옛 σ_VM 전개식 근호
    σxx² + σyy² + σzz² − σxx·σyy − σyy·σzz − σxx·σzz 가 거의 정수압에서 부호까지 잃고 (정확 1.15e-14 ↔ 계산 −4.66e-10), v2 의 0 clamp ·
    양의 쓰레기가 그대로 computed 통계가 되던 것.  기대값 = 입력 float 의 정확한 유리수 불변량 (생산 함수 미사용)."""
    TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    cvf = getattr(D, 'calc_von_mises_stress')

    def sat(t, z, s):
        return {'type': t, 'x': 0.0, 'y': 0.0, 'z': z, 'radius': 1e-3, 'sigma_xx': s[0], 'sigma_yy': s[1], 'sigma_zz': s[2]}

    def run(atoms, pz=1.0):
        try:
            return cvf(atoms, TM, 1000.0, pz)
        except Exception as e:                            # noqa: BLE001
            return {'status': f'EXC {type(e).__name__}: {e}'}

    def m_(r, ph):
        return ((r.get('type_stress') or {}).get(ph) or {}).get('mean')

    # ── V1 Codex 반례 그대로 (판정문 §2 · evidence/vm_boundary.json) — 두 입자의 정확 VM 이 같다 (정확 CV 0 %) ──────────
    BAD = (1073.1, 1073.1, 1073.1000001073098)
    d = BAD[2] - BAD[0]                                   # Sterbenz — 정확한 차 (1.0730991562013514e-07)
    GOOD = (0.0, 0.0, d)                                  # 같은 정수압 성분을 뺀 쌍둥이
    pre = (Fraction(BAD[2]) - Fraction(BAD[0]) == Fraction(d) and _rad_exact(BAD) == _rad_exact(GOOD) == Fraction(d) ** 2
           and _rad_old(BAD) == -4.656612873077393e-10 and d == 1.0730991562013514e-07)
    chk('V0 (전제) Codex 반례 재현 — 전개식 근호 −4.656612873077393e-10 · 정확 불변량 둘 다 d² (d = 1.0730991562013514e-07 · 차가 정확)',
        pre, repr((_rad_old(BAD), float(_rad_exact(BAD)), d)))
    chk('V0b (반례 확인) v2 판 규칙 (음수 근호 → 0 clamp) 은 같은 두 입자에서 CV 100.0 을 냈다',
        _cv_pct([_v2_vm(BAD), _v2_vm(GOOD)]) == 100.0, repr(_cv_pct([_v2_vm(BAD), _v2_vm(GOOD)])))
    for kind, conv in (('파이썬 float', float), ('numpy float64 (파서의 형)', np.float64)):
        r = run({1: sat(1, 0.1, tuple(map(conv, BAD))), 2: sat(3, 0.2, tuple(map(conv, GOOD)))})
        chk(f'V1 ★ Codex 반례 ({kind}) → computed · vm_cv 0.0 (정확) · 두 상 평균 = 정확 VM |d| (비트) · 다시 센 입자 1 · 계약 {VM_CONTRACT} '
            '(v2 판: vm_cv 100.0)',
            r.get('status') == 'computed' and r.get('vm_cv') == 0.0 and m_(r, 'AM_P') == abs(d) and m_(r, 'SE') == abs(d)
            and r.get('vm_stable_recomputed_n') == 1 and r.get('contract') == VM_CONTRACT,
            repr({k: r.get(k) for k in ('status', 'vm_cv', 'vm_mean', 'type_stress', 'vm_stable_recomputed_n', 'contract')})[:400])
    r = run({1: sat(1, 0.1, GOOD), 2: sat(3, 0.2, GOOD)})
    chk('V1b 양성 대조 (Codex) — 쌍둥이 둘 → computed · vm_cv 0.0 · 다시 센 입자 0 (정수압 성분 없는 입력은 옛 식 그대로)',
        r.get('status') == 'computed' and r.get('vm_cv') == 0.0 and r.get('vm_stable_recomputed_n') == 0, repr(r)[:300])

    # ── V2 양의 쓰레기 (음수만이 아니다) — 정확한 정수압 σxx = σyy = σzz 인데 전개식 근호 > 0 ───────────────────────────
    XP = next(v for v in (1.0 + 0.0731 * k for k in range(1, 500)) if _rad_old((v, v, v)) > 0)       # 1.1462 → +4.44e-16
    XN = next(v for v in (1.0 + 0.0731 * k for k in range(1, 500)) if _rad_old((v, v, v)) < 0)       # 1.0731 (S7) → −4.44e-16
    v2_hyd = [_v2_vm((XP, XP, XP))] * 3
    r = run({k: sat(1 + k % 3, 0.1 * k, (XP, XP, XP)) for k in range(1, 4)})
    chk(f'V2 ★ 정확한 정수압 침대 (σ = {XP!r} 셋 — 전개식 근호 {_rad_old((XP, XP, XP)):.3g} = 양의 쓰레기 · 정확 0) → VM 0 → '
        f'undefined_zero_mean · 다시 센 입자 3 (v2 판: VM {float(v2_hyd[0]):.3g} 셋 → computed CV {_cv_pct(v2_hyd)} = 정수압이 정상 0 으로 둔갑)',
        r.get('status') == 'undefined_zero_mean' and r.get('vm_cv', 0) is None and r.get('vm_stable_recomputed_n') == 3,
        repr(r)[:300])
    r = run({1: sat(1, 0.1, (XP, XP, XP)), 2: sat(3, 0.2, (XN, XN, XN))})
    chk(f'V2b ★ 양의 쓰레기 정수압 + 음수 근호 정수압 → 둘 다 VM 0 → undefined_zero_mean (v2 판: '
        f'{float(_v2_vm((XP, XP, XP))):.3g} ↔ 0 → computed CV {_cv_pct([_v2_vm((XP, XP, XP)), _v2_vm((XN, XN, XN))])})',
        r.get('status') == 'undefined_zero_mean' and r.get('vm_stable_recomputed_n') == 2, repr(r)[:300])
    r = run({1: sat(1, 0.1, (XP, XP, XP)), 2: sat(3, 0.2, (1.0, 0.0, 0.0)), 3: sat(3, 0.3, (2.0, 0.0, 0.0))})
    chk('V2c 양의 쓰레기 정수압이 섞인 정상 침대 → computed · CV = 손값 √(2/3)·100 (정수압 입자 VM 정확히 0 · v2 판은 2.1e-8 이 섞였다)',
        r.get('status') == 'computed' and close(r.get('vm_cv'), math.sqrt(2.0 / 3.0) * 100, rel=1e-12) and m_(r, 'AM_P') == 0.0
        and r.get('vm_stable_recomputed_n') == 1, repr(r)[:300])
    dvm = getattr(D, 'diag_von_mises', None)
    chk('V2d 한 입자 도우미 diag_von_mises — 정확한 정수압 (양의 쓰레기 · 음수 근호) → (0.0, 다시 셈) · 영 텐서 → (0.0, 옛 값 그대로)',
        callable(dvm) and dvm(XP, XP, XP) == (0.0, True) and dvm(XN, XN, XN) == (0.0, True) and dvm(0.0, 0.0, 0.0) == (0.0, False)
        and dvm(np.float64(XP), np.float64(XP), np.float64(XP)) == (0.0, True),
        repr([dvm(XP, XP, XP), dvm(XN, XN, XN), dvm(0.0, 0.0, 0.0)]) if callable(dvm) else '도우미 없음')

    # ── V3 거의 정수압의 양의 쓰레기 — 근호가 양수인데 정확값의 400 배 (부호만 보는 검사로는 못 잡는다) ──────────────────
    BP = next((p, p, p * (1 + f)) for p in (1000.0 * (1.0 + 0.0731 * k) for k in range(1, 500))
              for f in (1e-8, 2e-8, 5e-8, 1e-9, 1e-10) if _rad_old((p, p, p * (1 + f))) > 0
              and Fraction(_rad_old((p, p, p * (1 + f)))) > 100 * _rad_exact((p, p, p * (1 + f))))
    dP = BP[2] - BP[0]
    GP = (0.0, 0.0, dP)
    pre3 = _rad_exact(BP) == _rad_exact(GP) == Fraction(dP) ** 2
    v2_cv3 = _cv_pct([_v2_vm(BP), _v2_vm(GP)])
    for kind, conv in (('파이썬 float', float), ('numpy float64', np.float64)):
        r = run({1: sat(1, 0.1, tuple(map(conv, BP))), 2: sat(3, 0.2, tuple(map(conv, GP)))})
        chk(f'V3 ★ 거의 정수압 · 양의 쓰레기 ({kind} · σ = {BP!r} · 근호 {_rad_old(BP):.3g} ↔ 정확 {float(_rad_exact(BP)):.3g}) + 쌍둥이 → '
            f'computed · vm_cv 0.0 · 두 평균 = |d| · 다시 센 입자 1 (v2 판: CV {v2_cv3:.1f} %)',
            pre3 and r.get('status') == 'computed' and r.get('vm_cv') == 0.0 and m_(r, 'AM_P') == abs(dP) and m_(r, 'SE') == abs(dP)
            and r.get('vm_stable_recomputed_n') == 1, repr(r)[:300])

    # ── V4 거의 정수압 fuzz — 편차/압력 1e-12 … 1e-6 (로그 균일) · |p| 1e-2 … 1e8 · ± · 파이썬 float / numpy float64 ───────────
    rng = random.Random(20261005)
    worst_u, fail1, failp, viol, n_tot, v2_bad, v2_max = 0.0, [], [], [], 0, 0, 0.0
    worst_b = 0.0
    for i in range(600):
        conv = float if i % 2 == 0 else np.float64
        p = 10.0 ** rng.uniform(-2, 8) * rng.choice((-1.0, 1.0))
        dl = 10.0 ** rng.uniform(-12, -6)
        t = tuple(conv(p * (1.0 + dl * rng.uniform(-1.0, 1.0))) for _ in range(3))
        ex = _vm_exact(t)
        n_tot += 1
        r = run({1: sat(1, 0.5, t)})
        if ex == 0:                                       # 반올림으로 셋이 같아진 표본 — 정확 VM 0 → 미정의
            if not (r.get('status') == 'undefined_zero_mean'):
                fail1.append((t, r.get('status')))
        else:
            u = _ulps(r.get('vm_mean'), ex) if r.get('status') == 'computed' else math.inf
            worst_u = max(worst_u, u)
            if not (r.get('status') == 'computed' and u <= 4 and r.get('vm_stable_recomputed_n') == 1):
                fail1.append((t, r.get('status'), r.get('vm_mean'), str(ex)[:20], u, r.get('vm_stable_recomputed_n')))
            tw = (conv(0.0), conv(t[1] - t[0]), conv(t[2] - t[0]))   # 오프셋 없는 쌍둥이 — 차 셋이 같다 (Sterbenz · 정확)
            if _rad_exact(tw) != _rad_exact(t):
                failp.append((t, '쌍둥이 전제 깨짐'))
            else:
                r2 = run({1: sat(1, 0.1, t), 2: sat(3, 0.2, tw)})
                if not (r2.get('status') == 'computed' and r2.get('vm_cv') is not None and r2['vm_cv'] <= 1e-11):
                    failp.append((t, r2.get('status'), r2.get('vm_cv')))
                cv2 = _cv_pct([_v2_vm(t), _v2_vm(tw)])
                v2_max = max(v2_max, cv2 if cv2 == cv2 else 0.0)
                v2_bad += (not cv2 <= 1e-11)
        e_abs = abs(Fraction(float(_rad_old(t))) - _rad_exact(t))           # 유도한 엄밀 상한 B 가 실제 오차를 덮는가
        b = _VM_C * _VM_EPS * float(_sq_sum(t)) + _VM_ABS
        worst_b = max(worst_b, float(e_abs) / (_VM_EPS * float(_sq_sum(t))))
        if e_abs > Fraction(b):
            viol.append(t)
    chk(f'V4 ★ 거의 정수압 fuzz {n_tot} 표본 (편차/압력 1e-12…1e-6 · |p| 1e-2…1e8 · ± · float/np.float64 반반) — 1-입자 침대 vm_mean = '
        f'정확 불변량의 √ 와 ≤ 4 ulp (실측 최대 {worst_u:.2f} ulp) · computed · 다시 센 입자 1',
        not fail1, repr(fail1[:3])[:400])
    chk(f'V4b ★ 같은 fuzz — 오프셋 없는 쌍둥이 (0 · σyy−σxx · σzz−σxx: 정확 불변량 같음) 와 한 침대 → vm_cv ≤ 1e-11 % '
        f'(v2 판: {v2_bad}/{n_tot} 가 넘고 최대 {v2_max:.3g} %)',
        not failp, repr(failp[:3])[:400])
    chk(f'V4c 유도한 엄밀 상한 B = 16 ε Ŝ + 2^-1071 이 fuzz 전부에서 |전개식 근호 − 정확 불변량| 을 덮는다 (실측 최대 {worst_b:.2f} ε·Ŝ · 최악 유도 7.0001 ε·S)',
        not viol, repr(viol[:3]))

    # ── V5 판정 규칙 · 남긴 값 — 일반 응력 (부호 섞임 · 크기 섞임) + 편차/압력 1e-5 … 1e-1 ───────────────────────────
    rng = random.Random(20261006)
    mism, keep_bad, stab_bad, n_keep, n_stab, worst_rel, worst_su = [], [], [], 0, 0, 0.0, 0.0
    real_range_recomputed = []
    for i in range(1200):
        conv = float if i % 2 == 0 else np.float64
        if i % 3 == 0:
            t = tuple(conv(rng.gauss(0.0, 1.0) * 10.0 ** rng.uniform(-3, 8)) for _ in range(3))
        else:
            p = 10.0 ** rng.uniform(-2, 8) * rng.choice((-1.0, 1.0))
            dl = 10.0 ** rng.uniform(-5, -1)
            t = tuple(conv(p * (1.0 + dl * rng.uniform(-1.0, 1.0))) for _ in range(3))
        want = _vm_rule_stable(t)
        r = run({1: sat(1, 0.5, t)})
        got = r.get('vm_stable_recomputed_n')
        if got != (1 if want else 0):
            mism.append((t, want, got))
            continue
        ex = _vm_exact(t)
        R = _rad_exact(t)
        if R >= Fraction(1, 10 ** 8) * Fraction(float(_sq_sum(t))) and want:        # 정확 R/S ≥ 1e-8 (실 침대 범위) 인데 다시 셈
            real_range_recomputed.append(t)
        if want:
            n_stab += 1
            u = _ulps(r.get('vm_mean'), ex)
            worst_su = max(worst_su, u)
            if not u <= 4:
                stab_bad.append((t, u))
        else:
            n_keep += 1
            old = np.sqrt(_rad_old(t))
            rel = float(abs(decimal.Decimal(float(r.get('vm_mean'))) - ex) / ex) if ex else 0.0
            worst_rel = max(worst_rel, rel)
            if not (r.get('vm_mean') == float(old) and rel < 1.0 / (_VM_K - 1) + 2 * _VM_EPS):
                keep_bad.append((t, r.get('vm_mean'), float(old), rel))
    chk(f'V5 ★ 판정 = 유도한 규칙 (근호 ≤ 2^20·(16 ε Ŝ + 2^-1071) 일 때만 안정식 · 영 텐서 · NaN 제외) — 1,200 표본 (일반 400 · 편차/압력 '
        f'1e-5…1e-1 800) 의 다시 센 입자 수가 전부 규칙과 같다 (남김 {n_keep} · 다시 셈 {n_stab})',
        not mism, repr(mism[:3])[:400])
    chk(f'V5b ★ 남긴 값 = 옛 식 np.sqrt(근호) 비트 동일 · 정확 VM 대비 상대 오차 < 1/(2^20 − 1) (엄밀 한도 · 실측 최대 {worst_rel:.2g})',
        not keep_bad and n_keep > 300, repr(keep_bad[:3])[:400])
    chk(f'V5c 다시 센 값 ≤ 4 ulp (실측 최대 {worst_su:.2f}) · 정확 R/S ≥ 1e-8 (편차/압력 ≳ 1.4e-4 — real_14 최소 R/S 6.3e-5) 인 입자는 하나도 '
        '다시 세지 않는다 (옛 값 그대로)',
        not stab_bad and not real_range_recomputed and n_stab > 0, repr((stab_bad[:2], real_range_recomputed[:2]))[:400])

    # ── V6 binary64 보다 거친 입력 (numpy float32) — 그 형의 ε 로 상한을 잡는다 (판정이 엄밀한 범위) ─────────────────────
    t32 = (np.float32(1073.1), np.float32(1073.1), np.float32(1073.1) * np.float32(1.0000001))
    if callable(dvm):
        v32, st32 = dvm(*t32)
        ex32 = _vm_exact(t32)
        rel32 = float(abs(decimal.Decimal(float(v32)) - ex32) / ex32) if ex32 else float(v32)
        chk('V6 numpy float32 거의 정수압 → 그 형의 ε 로 판정 → 안정식 (다시 셈) · 정확 대비 ≤ 4·2^-24',
            st32 is True and rel32 <= 4 * 2.0 ** -24, repr((v32, st32, rel32)))
    else:
        chk('V6 numpy float32 거의 정수압 → 그 형의 ε 로 판정', False, '도우미 diag_von_mises 없음')

    # ── V7 무효 · 미정의 처리 그대로 (LHS-33) + 다시 센 수 필드 ─────────────────────────────────────────────────────
    r_none = run({1: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': 0.1, 'radius': 1e-3}, 2: {'type': 3, 'x': 0.0, 'y': 0.0, 'z': 0.2, 'radius': 1e-3}})
    r_nan = run({1: sat(1, 0.1, (1.0, 0.0, 0.0)), 2: sat(3, 0.2, (float('nan'), 0.0, 0.0))})
    r_zero = run({k: sat(1 + k % 3, 0.1 * k, (0.0, 0.0, 0.0)) for k in range(1, 7)})
    r_hyd = run({k: sat(1 + k % 3, 0.1 * k, (-2.0 * k, -2.0 * k, -2.0 * k)) for k in range(1, 7)})
    r_ovf = run({1: sat(1, 0.1, (1e200, -1e200, 0.0)), 2: sat(3, 0.2, (1.0, 0.0, 0.0))})
    chk('V7 ★ LHS-33 무효 · 미정의 그대로 — c_strs 없음 · NaN = 상태 그대로 · 다시 센 수 None (계산 전) · 무하중 (영 텐서) undefined · 다시 셈 0 · '
        '전 입자 정확한 정수압 undefined · 다시 셈 6 · σ² 넘침 invalid_input · 다시 셈 0',
        r_none.get('status') == 'unavailable_no_c_strs' and r_none.get('vm_stable_recomputed_n', 0) is None
        and r_nan.get('status') == 'invalid_input' and r_nan.get('vm_stable_recomputed_n', 0) is None
        and r_zero.get('status') == 'undefined_zero_mean' and r_zero.get('vm_stable_recomputed_n') == 0
        and r_hyd.get('status') == 'undefined_zero_mean' and r_hyd.get('vm_stable_recomputed_n') == 6
        and r_ovf.get('status') == 'invalid_input' and r_ovf.get('vm_stable_recomputed_n') == 0
        and all(x.get('contract') == VM_CONTRACT for x in (r_none, r_nan, r_zero, r_hyd, r_ovf)),
        repr([(x.get('status'), x.get('vm_stable_recomputed_n'), x.get('contract')) for x in (r_none, r_nan, r_zero, r_hyd, r_ovf)]))


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
    # ── P RGLR-03 (Codex 10-05 재검증) — 실 CSV → 실 파서 → LW: 미제공 · 일부 열 · NaN · 문자열 · Inf · 일부 키 ─────────────
    try:
        rglr03(D)
    except Exception as e:                                # noqa: BLE001
        chk('P 묶음 (RGLR-03) 실행', False, f'{type(e).__name__}: {e}'[:300])
    # ── S LHS-33 (좁은 개정 · 1저자 비준 10-05) — 옛 σ_VM 열: 무효 · 미정의 = None + 상태 · 정상 = 옛 함수와 비트 동일 · 소비자 ────
    try:
        lhs33(D)
    except Exception as e:                                # noqa: BLE001
        chk('S 묶음 (LHS-33) 실행', False, f'{type(e).__name__}: {e}'[:300])
    # ── V RGLR2-03 (Codex 3차 재검증 10-05 · Q4) — 옛 σ_VM 근호의 수치 분해 · 분해 안 된 입자만 안정식 · 정확 불변량 대조 ──────
    try:
        rglr2_03(D)
    except Exception as e:                                # noqa: BLE001
        chk('V 묶음 (RGLR2-03) 실행', False, f'{type(e).__name__}: {e}'[:300])

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
            #  RGLR-03 · LHS-33 — 정상 입력 (real_14 · 32,832 + 457 입자) 에서 새 파서 · 새 σ_VM 이 옛 판과 dict 내용 · 수치 비트 동일
            old_atoms, _ = _old_load_atoms_raw(os.path.join(tmp, 'atoms.csv'))
            chk('L12p ★ real_14 — 새 파서 dict = 옛 파서 dict (입자마다 키 · 값 비트 동일 · 손상 사유 키 없음)',
                len(old_atoms) == len(atoms_raw) and all(atoms_raw[k] == old_atoms[k] for k in old_atoms),
                f"{len(old_atoms)} vs {len(atoms_raw)}")
            vm_new = D.calc_von_mises_stress(atoms_raw, tm14, 1000.0, pzr)
            vm_old = _old_von_mises(old_atoms, tm14, 1000.0, pzr)
            chk('L12q ★ real_14 — 새 σ_VM (stress_cv · 상 비 · z 층) = 옛 함수 비트 동일 · status computed (stress_cv 213.1 · AM_P 0.884) · '
                '안정식으로 다시 센 입자 0 (RGLR2-03 — 33,289 입자 전부 옛 식 값 그대로)',
                _same_vm(vm_new, vm_old) and (vm_new or {}).get('status') == 'computed'
                and round(vm_old['vm_cv'], 1) == 213.1 and round(vm_old['type_stress']['AM_P']['ratio'], 3) == 0.884
                and (vm_new or {}).get('vm_stable_recomputed_n') == 0,
                f"{(vm_new or {}).get('status')} · 다시 셈 {(vm_new or {}).get('vm_stable_recomputed_n')} · "
                f"{None if vm_old is None else (vm_old['vm_cv'], vm_old['type_stress'])}")
            #  RGLR2-03 — real_14 의 입자마다 정확 R/S (유리수) 최소값: 판정 경계 (≈ 2^-28 = 3.7e-9) 와의 거리
            _rs = min(float(_rad_exact((a_['sigma_xx'], a_['sigma_yy'], a_['sigma_zz'])))
                      / float(_sq_sum((a_['sigma_xx'], a_['sigma_yy'], a_['sigma_zz']))) for a_ in atoms_raw.values()
                      if _sq_sum((a_['sigma_xx'], a_['sigma_yy'], a_['sigma_zz'])) > 0)
            chk(f'L12r real_14 — 입자마다 정확 근호/Σσ² 의 최소 {_rs:.3g} (판정 경계 2^-28 ≈ 3.7e-9 의 {_rs / 2.0 ** -28:,.0f} 배 — 거의 정수압 입자 없음)',
                _rs > 1e3 * 2.0 ** -28, f'{_rs}')
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
        def bed(name, with_lw=True, cstr_scale=1.0, fz=-2e-3, first_tok=None, cstr_override=None):
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
            for k_, v_ in (cstr_override or {}).items():          # RGLR2-03 — 한 입자의 c_strs 를 거의 정수압으로 (LW virial 대조는 깨진다)
                cstr[k_] = list(v_)
            with open(os.path.join(dd_, 'atoms.csv'), 'w') as fh:
                fh.write('id,type,x,y,z,radius,c_strs[1],c_strs[2],c_strs[3]\n')
                for a in atoms_:
                    s = cstr[a[0]]
                    c1 = repr(s[0]) if first_tok is None else first_tok        # RGLR-03 — 첫 c_strs 칸을 손상 (NaN · 문자열)
                    fh.write(f'{a[0]},{a[1]},{a[2]!r},{a[3]!r},{a[4]!r},{a[5]!r},{c1},{s[1]!r},{s[2]!r}\n')
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
        # LHS-33 — 옛 σ_VM 열의 상태 계약이 CLI (웹앱 접촉 단계) 를 지나 full_metrics.json · network_summary.csv 에 남는다
        lines3 = {r[0]: (r[1] if len(r) > 1 else '') for r in csv.reader(io.StringIO(summ3)) if r}
        chk(f'L13l ★ LHS-33 무하중 침대 → stress_cv null · 상 비 null · z 층 null · stress_cv_status undefined_zero_mean · 계약 {VM_CONTRACT} · '
            '사유 · 다시 센 입자 0 (영 텐서) (옛 판: stress_cv 0 · 비 0 = 거짓 최고 등급)',
            'stress_cv' in met3 and met3['stress_cv'] is None and met3.get('stress_ratio_AM_P', 0) is None
            and met3.get('stress_ratio_SE', 0) is None and met3.get('stress_z_layer_cv', 0) is None
            and met3.get('stress_cv_status') == 'undefined_zero_mean' and met3.get('stress_cv_contract') == VM_CONTRACT
            and bool(met3.get('stress_cv_reason')) and met3.get('stress_cv_vm_stable_n') == 0,
            str({k: met3.get(k) for k in ('stress_cv', 'stress_ratio_AM_P', 'stress_cv_status', 'stress_cv_contract', 'stress_cv_reason',
                                          'stress_cv_vm_stable_n')}))
        chk('L13m ★ LHS-33 케이스 표 (network_summary.csv) — 무하중이면 "Stress CV(%)" = "—" · 상 비 "—" · 상태 줄 (상태 — 사유)',
            lines3.get('Stress CV(%)') == '—' and lines3.get('σ_SE/σ_mean') == '—'
            and 'undefined_zero_mean' in lines3.get('Stress CV 상태 (50/50 · LHS-33)', ''), repr(lines3)[:400])
        chk('L13n 정상 침대 → stress_cv_status computed · 계약 표지 · 값은 숫자 (L13f = 옛 정의 그대로) · 표에 상태 줄 없음 · '
            'stress_cv_vm_stable_n 0 (RGLR2-03 출처 — 안정식으로 다시 센 입자 없음)',
            met.get('stress_cv_status') == 'computed' and met.get('stress_cv_contract') == VM_CONTRACT
            and isinstance(met.get('stress_cv'), float) and 'Stress CV 상태 (50/50 · LHS-33)' not in summ
            and met.get('stress_cv_vm_stable_n') == 0,
            str({k: met.get(k) for k in ('stress_cv', 'stress_cv_status', 'stress_cv_contract', 'stress_cv_vm_stable_n')}))
        #  RGLR2-03 — 거의 정수압 입자 하나 (c_strs = (q, q, q·(1 + 1e-10))) 가 CLI (웹앱 접촉 단계) 를 지나 full_metrics 에 출처로 남는다
        qh = -1.2e-5
        prh, meth, _ = bed('nearhyd', cstr_override={1: (qh, qh, qh * (1.0 + 1e-10))})
        chk('L13q ★ RGLR2-03 CLI — 거의 정수압 입자 하나 (c_strs q · q · q(1+1e-10)) → stress_cv_status computed · stress_cv_vm_stable_n 1 · '
            f'계약 {VM_CONTRACT} (나머지 20 입자 = 옛 식 그대로)',
            prh.returncode == 0 and meth.get('stress_cv_status') == 'computed' and meth.get('stress_cv_vm_stable_n') == 1
            and meth.get('stress_cv_contract') == VM_CONTRACT and isinstance(meth.get('stress_cv'), float),
            f"rc {prh.returncode} · {({k: meth.get(k) for k in ('stress_cv', 'stress_cv_status', 'stress_cv_vm_stable_n', 'stress_cv_contract')})} · "
            f"{(prh.stderr or '')[-300:]}")
        pr4, met4, summ4 = bed('nanfirst', first_tok='nan')
        chk('L13o ★ RGLR-03 CLI — 첫 c_strs 칸 NaN 침대 → stress_lw_status FAILED (invalid_input …) · LW 값 없음 · stress_cv null · '
            'stress_cv_status invalid_input (옛 판: LW OK virial unavailable · stress 키 없음)',
            pr4.returncode == 0 and str(met4.get('stress_lw_status', '')).startswith('FAILED (invalid_input') and 'stress_cv_lw' not in met4
            and 'stress_cv' in met4 and met4['stress_cv'] is None and met4.get('stress_cv_status') == 'invalid_input',
            f"rc {pr4.returncode} · {met4.get('stress_lw_status')} · {met4.get('stress_cv_status')} · {(pr4.stderr or '')[-300:]}")
        pr5, met5, summ5 = bed('textfirst', first_tok='invalid')
        chk('L13p ★ RGLR-03 CLI — 첫 c_strs 칸 문자열 침대 → stress_lw_status FAILED (invalid_input …) · stress_cv_status invalid_input',
            pr5.returncode == 0 and str(met5.get('stress_lw_status', '')).startswith('FAILED (invalid_input')
            and met5.get('stress_cv_status') == 'invalid_input' and met5.get('stress_cv', 0) is None,
            f"rc {pr5.returncode} · {met5.get('stress_lw_status')} · {met5.get('stress_cv_status')} · {(pr5.stderr or '')[-300:]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\n{N[0] - len(FAILS)}/{N[0]} 통과' + ('' if not FAILS else '  — 실패: ' + ' · '.join(FAILS)))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
