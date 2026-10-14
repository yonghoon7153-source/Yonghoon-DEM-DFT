#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K5 — S3 총힘 잔차 (REG §12-2 · §13 · CX1 §3 UL-02 · CX2 §3-1).  표준 라이브러리만.

    python3 ul_s3.py --selftest

정의 (권고 기본값 · choice C1 · C2 — 1저자 비준 대기 · docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md)
  입력 = 같은 step 의 두 덤프 (창 끝):
    ① 원자 덤프 (id · z · radius · mass · fx fy fz) — LIGGGHTS 의 f 는 출력 시점에 이미 **총힘** (쌍 접촉 + 바닥 · 판 벽 + 중력 + 감쇠 ·
       post_force 뒤).  ⇒ 여기서 중력 · 감쇠 · 벽력을 다시 더하지 않는다 (CX2 §3-1 "이중 가산 금지").
       출력 시점 = 이력 시험 정보 ⓑ (접촉 없는 입자 fz = −m g) 로 실제 바이너리에서 확인한다.
    ② 쌍 접촉 덤프 (cpl · id1 id2 · 쌍 힘) — 분모의 접촉 크기 합에만 쓴다.
  유효 집합 V = S0 ID 집합 ∩ 이 프레임 ∩ 중심이 [0, 판 높이] 안 (판 위로 이탈 · 바닥 아래 = 평형 대상이 아니다).
  R_S3 = Σ_{i∈V} ‖F_i‖ ÷ D   (입자마다 norm 을 먼저 · 그다음 합 — 전역 벡터 합 ‖Σ F‖ 는 진단 열만 · CX2 §3-1 반례 0.002 ↔ 0)
  D    = Σ_{i∈V} ( Σ_{c∋i} ‖f_c‖ + m_i g )   (접촉 크기 합 + 무게 = 저압 · 무접촉 floor — 무게 항이 늘 > 0)
  판정: R_S3 ≤ 1e-3 → PASS · > → FAIL · V 공집합 · 입력 결손 · 비유한 · step 다름 → NOT_COMPUTED (PASS 아님).
  진단 (판정 아님): 전역 벡터 합 ‖Σ_{i∈V} F_i‖ ÷ D · 옛 쌍 전용 잔차 (plane_load_share.balance_residual 과 같은 식 — 창 [2 r_max, h − 2 r_max] 안 ·
  쌍 힘만 · 힘 가중) — 관문이 아니다 (REG §12-2).
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
THRESHOLD = 1e-3
G = 9.81


def _finite(*xs):
    return all(isinstance(x, (int, float)) and math.isfinite(x) for x in xs)


def s3_residual(atoms, contacts, s0_ids, plate_z, *, atom_step=None, contact_step=None, g=G, threshold=THRESHOLD):
    """→ {'status': PASS | FAIL | NOT_COMPUTED, 'R', 'numerator', 'denominator', 'n_valid', 'global_norm_diag', 'why'}."""
    out = {'status': 'NOT_COMPUTED', 'R': None, 'numerator': None, 'denominator': None, 'n_valid': 0, 'global_norm_diag': None, 'why': []}
    if atom_step is None or contact_step is None or atom_step != contact_step:
        out['why'].append(f'두 덤프의 step 이 같지 않다 ({atom_step} ↔ {contact_step}) — 동일 시점 아님')
        return out
    if not (isinstance(plate_z, (int, float)) and math.isfinite(plate_z) and plate_z > 0):
        out['why'].append(f'판 높이 무효 {plate_z!r}')
        return out
    need = ('id', 'z', 'radius', 'mass', 'fx', 'fy', 'fz')
    for a in atoms:
        if any(k not in a for k in need):
            out['why'].append(f'원자 덤프 열 결손 {sorted(set(need) - set(a))}')
            return out
        if not _finite(*(a[k] for k in need)):
            out['why'].append(f'비유한 원자 값 (id {a["id"]})')
            return out
    valid = {}
    for a in atoms:
        i = int(a['id'])
        if i in valid:
            out['why'].append(f'원자 id 중복 {i}')
            return out
        if i in s0_ids and 0.0 <= a['z'] <= plate_z:
            valid[i] = a
    if not valid:
        out['why'].append('유효 집합 공집합 (S0 ID ∩ 프레임 ∩ 중심이 [0, 판] 안)')
        return out
    mag = {i: 0.0 for i in valid}
    for c in contacts:
        if any(k not in c for k in ('id1', 'id2', 'fx', 'fy', 'fz')) or not _finite(c['fx'], c['fy'], c['fz']):
            out['why'].append('쌍 접촉 덤프 열 결손 · 비유한')
            return out
        m = math.sqrt(c['fx'] ** 2 + c['fy'] ** 2 + c['fz'] ** 2)
        for k in ('id1', 'id2'):
            j = int(c[k])
            if j in mag:
                mag[j] += m
    num = sum(math.sqrt(a['fx'] ** 2 + a['fy'] ** 2 + a['fz'] ** 2) for a in valid.values())
    den = sum(mag[i] + valid[i]['mass'] * g for i in valid)
    gx = sum(a['fx'] for a in valid.values())
    gy = sum(a['fy'] for a in valid.values())
    gz = sum(a['fz'] for a in valid.values())
    if not den > 0:
        out['why'].append('분모 ≤ 0 (무게 · 접촉 크기 합 0)')
        return out
    R = num / den
    out.update(R=R, numerator=num, denominator=den, n_valid=len(valid), global_norm_diag=math.sqrt(gx * gx + gy * gy + gz * gz) / den,
               status='PASS' if R <= threshold else 'FAIL')
    return out


def pair_only_residual(atoms, contacts, plate_z):
    """진단 (관문 아님) — 옛 plane_load_share.balance_residual 과 같은 식: 창 [2 r_max, h − 2 r_max] 안 · 쌍 힘만 · 힘 가중."""
    r_max = max(a['radius'] for a in atoms)
    lo, hi = 2.0 * r_max, plate_z - 2.0 * r_max
    net = {int(a['id']): [0.0, 0.0, 0.0] for a in atoms}
    mag = {int(a['id']): 0.0 for a in atoms}
    for c in contacts:
        f = (c['fx'], c['fy'], c['fz'])
        m = math.sqrt(sum(x * x for x in f))
        i, j = int(c['id1']), int(c['id2'])
        if i in net:
            net[i] = [p + q for p, q in zip(net[i], f)]
            mag[i] += m
        if j in net:
            net[j] = [p - q for p, q in zip(net[j], f)]
            mag[j] += m
    inner = [int(a['id']) for a in atoms if lo <= a['z'] <= hi and mag[int(a['id'])] > 0]
    if not inner:
        return None
    return sum(math.sqrt(sum(x * x for x in net[i])) for i in inner) / sum(mag[i] for i in inner)


# ── selftest ─────────────────────────────────────────────────────────────────

def _chain(weight_factors=(14.0, 13.0, 12.0, 11.0), n=5, radius=0.00051, density=2000.0, g=G):
    """CX1 §3 반례 — 반경 0.00051 m · 밀도 2000 · 중력 9.81 인 구 다섯의 수직 사슬 · 접촉력 = 무게 × (14, 13, 12, 11).
    총힘 = 쌍 힘 + 중력 + (끝 둘은 벽 반력 — 바닥 = 아래 입자 · 판 = 위 입자) → 평형이면 전부 0."""
    m = density * 4.0 * math.pi * radius ** 3 / 3.0
    w = m * g
    atoms = [{'id': i + 1, 'type': 3, 'z': (i + 0.5) * 0.001, 'radius': radius, 'mass': m, 'fx': 0.0, 'fy': 0.0, 'fz': 0.0} for i in range(n)]
    contacts = []
    for j, k in enumerate(weight_factors):
        f = -k * w                                    # id1 (아래) 가 받는 z 힘 (아래 방향)
        contacts.append({'id1': j + 1, 'id2': j + 2, 'fx': 0.0, 'fy': 0.0, 'fz': f})
        atoms[j]['fz'] += f
        atoms[j + 1]['fz'] -= f
    for a in atoms:
        a['fz'] -= w                                  # 중력 (덤프 f 에는 이미 들어 있다)
    atoms[0]['fz'] += (weight_factors[0] + 1.0) * w   # 바닥 반력 (원 사슬 기준 15 w)
    atoms[-1]['fz'] -= (weight_factors[-1] - 1.0) * w # 판 반력 (위 입자 · 아래로 10 w)
    return atoms, contacts, w


def selftest():
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001 — 빈 구현 · 예외도 실패
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    A, C, w = _chain()
    ids = {a['id'] for a in A}
    pz = 0.005
    chk('F1 중력과 정확히 평형인 다섯 구 사슬 = PASS (총힘 잔차 ≈ 부동소수)',
        lambda: (lambda r: r['status'] == 'PASS' and r['R'] < 1e-12)(s3_residual(A, C, ids, pz, atom_step=1, contact_step=1)))
    chk('F1 같은 입력의 옛 쌍 전용 잔차 = 0.0400 (CX1 §3 · 진단 열 — 관문 아님)',
        lambda: abs(pair_only_residual(A, C, pz) - 0.04) < 1e-12)
    chk('F1 봉인 plane_load_share.compute 의 balance_residual 도 0.0400 (같은 식 · 리포 함수 그대로 부름 · 고치지 않음)',
        lambda: abs(_sealed_pair_only(A, C, pz) - 0.04) < 1e-12)
    B, CB, _ = _chain(weight_factors=(14.0, 13.5, 12.0, 11.0))   # 사슬 2–3 힘만 13.5 w — 2 · 3 번 입자 ±0.5 w 불평형 (벽 반력은 원래대로)
    chk('F2 힘 불균형 사슬 (13 → 13.5 w) = FAIL (R = 1 w / 106 w ≈ 0.0094)',
        lambda: (lambda r: r['status'] == 'FAIL' and abs(r['R'] - 1.0 / 106.0) < 1e-9)(s3_residual(B, CB, ids, pz, atom_step=1, contact_step=1)))
    two = [{'id': 1, 'z': 0.001, 'radius': 0.0005, 'mass': 0.0, 'fx': 0.0, 'fy': 0.0, 'fz': 1e-5},
           {'id': 2, 'z': 0.002, 'radius': 0.0005, 'mass': 0.0, 'fx': 0.0, 'fy': 0.0, 'fz': -1e-5}]
    cc = [{'id1': 1, 'id2': 2, 'fx': 0.0, 'fy': 0.0, 'fz': -0.005}]
    chk('F3 같은 크기 반대 힘 (+1e-5 · −1e-5 N · 분모 0.01 N) = 입자별 norm 합 0.002 → FAIL · 전역 합 0 은 진단 열로만',
        lambda: (lambda r: r['status'] == 'FAIL' and abs(r['R'] - 0.002) < 1e-15 and r['global_norm_diag'] == 0.0)(
            s3_residual(two, cc, {1, 2}, pz, atom_step=3, contact_step=3)))

    def scaled(k):
        t = [dict(a, fz=a['fz'] * k) for a in two]
        return s3_residual(t, cc, {1, 2}, pz, atom_step=1, contact_step=1)
    chk('F4 문턱 양옆: R 0.999e-3 PASS · 1.001e-3 FAIL (문턱 1e-3 그대로 · 넓히지 않는다)',
        lambda: scaled(0.999 / 2.0)['status'] == 'PASS' and scaled(1.001 / 2.0)['status'] == 'FAIL')
    low = [dict(a) for a in A]
    lowc = [dict(c, fz=c['fz'] * 1e-3) for c in C]
    for a in low:
        a['fz'] = 0.0
    chk('F5 저압 (접촉력 ≪ 무게) 평형 = PASS (분모 = 무게 floor)', lambda: s3_residual(low, lowc, ids, pz, atom_step=1, contact_step=1)['status'] == 'PASS')
    rest = [{'id': i, 'z': 0.0005, 'radius': 0.0005, 'mass': 1e-6, 'fx': 0.0, 'fy': 0.0, 'fz': 0.0} for i in (1, 2, 3)]
    chk('F6 무접촉 (바닥에 놓인 입자 · 총힘 0) = PASS · 분모 = Σ m g (중력을 다시 더하면 실패해야 — 이중 가산 금지)',
        lambda: (lambda r: r['status'] == 'PASS' and r['R'] == 0.0 and abs(r['denominator'] - 3e-6 * G) < 1e-18)(
            s3_residual(rest, [], {1, 2, 3}, pz, atom_step=1, contact_step=1)))
    chk('F7 유효 집합 공집합 (전부 판 위로 이탈) = NOT_COMPUTED (PASS 아님)',
        lambda: s3_residual([dict(a, z=0.01) for a in A], C, ids, pz, atom_step=1, contact_step=1)['status'] == 'NOT_COMPUTED')
    chk('F8 단위 환산 (힘 · 무게 × 1000) = 같은 R',
        lambda: abs(s3_residual([dict(a, fz=a['fz'] * 1e3, mass=a['mass'] * 1e3) for a in B], [dict(c, fz=c['fz'] * 1e3) for c in CB], ids, pz,
                                atom_step=1, contact_step=1)['R'] - 1.0 / 106.0) < 1e-9)
    chk('F9 누락 열 (fz 없음) = NOT_COMPUTED', lambda: s3_residual([{k: v for k, v in a.items() if k != 'fz'} for a in A], C, ids, pz,
                                                                     atom_step=1, contact_step=1)['status'] == 'NOT_COMPUTED')
    chk('F9 비유한 힘 (NaN) = NOT_COMPUTED (비교로 흘려보내지 않는다)',
        lambda: s3_residual([dict(a, fz=float('nan')) if a['id'] == 3 else a for a in A], C, ids, pz, atom_step=1, contact_step=1)['status'] == 'NOT_COMPUTED')
    chk('F10 두 덤프의 step 이 다름 (동일 시점 아님) = NOT_COMPUTED', lambda: s3_residual(A, C, ids, pz, atom_step=1, contact_step=2)['status'] == 'NOT_COMPUTED')
    esc = [dict(a) for a in B] + [{'id': 99, 'z': 0.009, 'radius': 0.0005, 'mass': 1.0, 'fx': 0.0, 'fy': 0.0, 'fz': -9.81}]
    chk('F11 판 위로 이탈한 입자 · S0 에 없던 id 는 집합 밖 (자유 낙하 −m g 가 잔차에 안 들어간다)',
        lambda: abs(s3_residual(esc, CB, ids | {99}, pz, atom_step=1, contact_step=1)['R'] - 1.0 / 106.0) < 1e-9
        and abs(s3_residual(esc[:-1] + [dict(esc[-1], z=0.004)], CB, ids, pz, atom_step=1, contact_step=1)['R'] - 1.0 / 106.0) < 1e-9)
    chk('F12 ULKRR-04 소수 원자 ID (2 → 2.5 — 정수 2 로 자르지 않는다) = NOT_COMPUTED',
        lambda: s3_residual([dict(a, id=2.5) if a['id'] == 2 else a for a in A], C, ids, pz, atom_step=1, contact_step=1)['status'] == 'NOT_COMPUTED')
    chk('F12 ULKRR-04 소수 쌍 참조 (id2 2 → 2.5) = NOT_COMPUTED · 대조: 정수 그대로 = PASS',
        lambda: s3_residual(A, [dict(c, id2=2.5) if c['id2'] == 2 else c for c in C], ids, pz, atom_step=1, contact_step=1)['status'] == 'NOT_COMPUTED'
        and s3_residual(A, C, ids, pz, atom_step=1, contact_step=1)['status'] == 'PASS')
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def _sealed_pair_only(atoms, contacts, plate_z):
    """리포 scripts/plane_load_share.py 의 compute() 를 그대로 부른다 (읽기 전용 import · 그 파일은 고치지 않는다)."""
    import importlib.util
    import numpy as np
    p = os.path.join(REPO, 'scripts', 'plane_load_share.py')
    spec = importlib.util.spec_from_file_location('plane_load_share_ro', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ids = np.array([a['id'] for a in atoms])
    at = {'id': ids, 'type': np.full(len(ids), 3), 'z': np.array([a['z'] for a in atoms]), 'radius': np.array([a['radius'] for a in atoms])}
    f = np.array([[c['fx'], c['fy'], c['fz']] for c in contacts])
    co = {'id1': np.array([c['id1'] for c in contacts]), 'id2': np.array([c['id2'] for c in contacts]), 'f': f, 'fn': f}
    r = m.compute(at, co, {3: 'SE'}, plate_z, (0.05, 0.05, 'input_params.json'), 1000)
    return r['balance_residual']


if __name__ == '__main__':
    if '--selftest' in sys.argv[1:]:
        sys.exit(selftest())
    print(__doc__)
