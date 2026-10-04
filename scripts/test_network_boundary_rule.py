#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 솔버의 경계 띠 규칙 기록 — τ 결정 16 ② 안 A (1저자 비준 2026-10-04 *"권고대로"*).

  python3 scripts/test_network_boundary_rule.py

★ 반례 먼저 — 옛 코드는 L0 (입자 자기 반지름 × boundary_factor) → L1 (판 높이 15/85 %) → L2 (관측 z 범위 15/85 %)
  폴백을 **조용히** 하고 어느 규칙을 썼는지 남기지 않았다 (`LHS-17` · `TAU-14`).  인계 게이트 G1 (L0 일 때만 값) 은
  그 기록 없이는 판정할 수 없다.
★ 동작 중립 — 띠 선택을 함수 `boundary_sets` 로 옮기고 규칙 · 띠 폭을 **기록만** 더한다.  세 픽스처 × 두 면적 모드의
  σ · 경계 수 · 관통 분율을 **추출 전 코드로 뜬 기준값** (아래 GOLD — 2026-10-04 HEAD `eedada5d3` 의 network_conductivity) 과
  비트 단위로 대조한다.  기준값이 바뀌면 이 시험이 먼저 빨갛게 된다.
★ 봉인 — network_conductivity.py 는 S3 수치 모듈 (`seal_s3_prerun.NUMERIC_MODULES`) 이다.  봉인은 수정 금지가 아니라
  **재봉인 강제**다 (`run_s3_psi.verify_code_bundle`) — S3 를 돌리기 전에 다시 봉인한다 (결정 16 · 1저자 "재봉인은 나중").
"""
import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


def chain(zs, r):
    A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': float(r)} for i, z in enumerate(zs, 1)}
    C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1 * r * r, 'delta': 0.05 * r} for i in range(1, len(zs))]
    return A, C


#  (픽스처, plate_z, 기대 규칙, 기대 띠 폭 / plate_z)
#   L0: 21 구 사슬 z 0..20 · r 1 · 판 20 · 띠 z ≤ 2 · z ≥ 18 → 3 · 3 (≥ 3) → L0 · 폭 (2 + 2)/20
#   L1: 81 구 z 0..40 (0.5 간격) · r 0.4 · 판 40 · L0 바닥 z ≤ 0.8 → 2 개 (< 3) → L1 (z ≤ 6 · z ≥ 34 → 13 · 13) · 폭 (6 + 6)/40
#   L2: L0 사슬 · 판 100 (입자 범위 0..20 위로 멀리) → L0 · L1 위 띠 0 개 → L2 (관측 범위 15 %: z ≤ 3 · z ≥ 17 → 4 · 4) · 폭 (3 + 83)/100
FIX = {
    'L0': (chain(range(21), 1.0), 20.0, 'L0', 0.2),
    'L1': (chain([0.5 * k for k in range(81)], 0.4), 40.0, 'L1', 0.3),
    'L2': (chain(range(21), 1.0), 100.0, 'L2', 0.86),
}

#  추출 전 코드 (HEAD eedada5d3) 로 뜬 값 — run_decomposition(type_map={1: 'SE'}, mode='ionic', box 10 × 10, scale 1).
GOLD = {
    ('L0', 'hertzian'): dict(n_bottom=3, n_top=3, n_boundary_overlap=0, sigma_full=0.00400388, sigma_bulk_net=0.03925523,
                             sigma_constr_net=0.00445864, percolating_fraction=1.0, active_fraction=1.0, phi_se=0.044,
                             sigma_full_status='computed'),
    ('L0', 'physics'): dict(n_bottom=3, n_top=3, n_boundary_overlap=0, sigma_full=0.0039382, sigma_bulk_net=0.03925523,
                            sigma_constr_net=0.00437735, percolating_fraction=1.0, active_fraction=1.0, phi_se=0.044,
                            sigma_full_status='computed'),
    ('L1', 'hertzian'): dict(n_bottom=13, n_top=13, n_boundary_overlap=0, sigma_full=0.00089265, sigma_bulk_net=0.00717995,
                             sigma_constr_net=0.00101938, percolating_fraction=1.0, active_fraction=1.0, phi_se=0.0054,
                             sigma_full_status='computed'),
    ('L1', 'physics'): dict(n_bottom=13, n_top=13, n_boundary_overlap=0, sigma_full=0.00087836, sigma_bulk_net=0.00717995,
                            sigma_constr_net=0.00100079, percolating_fraction=1.0, active_fraction=1.0, phi_se=0.0054,
                            sigma_full_status='computed'),
    ('L2', 'hertzian'): dict(n_bottom=4, n_top=4, n_boundary_overlap=0, sigma_full=0.02287484, sigma_bulk_net=0.22427183,
                             sigma_constr_net=0.02547299, percolating_fraction=1.0, active_fraction=1.0, phi_se=0.0088,
                             sigma_full_status='computed'),
    ('L2', 'physics'): dict(n_bottom=4, n_top=4, n_boundary_overlap=0, sigma_full=0.02249961, sigma_bulk_net=0.22427183,
                            sigma_constr_net=0.02500854, percolating_fraction=1.0, active_fraction=1.0, phi_se=0.0088,
                            sigma_full_status='computed'),
}


def run(nc, A, C, pz, cm, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return nc.run_decomposition(A, C, [1], 1.0, pz, 10.0, 10.0, type_map={1: 'SE'}, contact_mode=cm, mode='ionic', **kw)


def main():
    import network_conductivity as nc

    # ── ① 동작 중립 (기준값과 비트 동일) ──
    neutral, rules, fracs = [], [], []
    for name, ((A, C), pz, rule, frac) in FIX.items():
        for cm in ('hertzian', 'physics'):
            r = run(nc, A, C, pz, cm)
            neutral.append(all(r.get(k) == v for k, v in GOLD[(name, cm)].items()))
            rules.append(r.get('boundary_rule') == rule)
            fracs.append(isinstance(r.get('boundary_band_frac'), float) and abs(r['boundary_band_frac'] - frac) < 1e-12)
    chk('① 동작 중립 — 세 픽스처 × 두 면적 모드의 σ · 경계 수 · 관통 분율 · 상태가 추출 전 기준값과 같다', all(neutral))
    chk('② 결과에 쓰인 띠 규칙 `boundary_rule` 이 남는다 — L0 · L1 · L2 픽스처가 각각 그 이름 (두 면적 모드)', all(rules))
    chk('③ `boundary_band_frac` = (바닥 띠 문턱 + (판 − 위 띠 문턱)) / 판 — L0 0.2 (= 2·bf·r_max/판) · L1 0.3 · L2 0.86', all(fracs))

    # ── ④ 함수 자체 — build_network 과 같은 집합 · 같은 규칙 ──
    A, C = FIX['L1'][0]
    ids = list(A)
    ok_fn = hasattr(nc, 'boundary_sets')
    if ok_fn:
        bot, top, rule, frac = nc.boundary_sets(A, ids, 40.0, 2.0)
        with contextlib.redirect_stdout(io.StringIO()):
            net = nc.build_network(A, C, [1], 1.0, 40.0, 10.0, 10.0, 2.0, type_map={1: 'SE'})
        ok_fn = (bot == net['bottom'] and top == net['top'] and rule == 'L1' == net.get('boundary_rule')
                 and abs(frac - 0.3) < 1e-12 and net.get('boundary_band_frac') == frac)
    chk('④ `boundary_sets(atoms, ids, plate_z, factor)` → (bottom, top, rule, band_frac) — build_network 이 그 함수를 쓴다 (같은 집합)', ok_fn)

    # ── ⑤ L1 로도 3 개 미만이면 L2 (짧은 사슬) ──
    tA, tC = chain([0., 2., 4., 6., 8.], 1.0)
    rt = run(nc, tA, tC, 8.0, 'hertzian')
    chk('⑤ L0 · L1 둘 다 3 개 미만 → L2 로 기록 (5 구 사슬 · 판 8)', rt.get('boundary_rule') == 'L2')

    # ── ⑥ 다분산 — L0 띠 폭은 가장 큰 반지름 (상한) ──
    pA = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': (1.5 if z == 10 else 1.0)} for i, z in enumerate(range(21), 1)}
    pC = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
    rp = run(nc, pA, pC, 20.0, 'hertzian')
    chk('⑥ 다분산 L0 — 띠 폭 = 2·bf·r_max / 판 = 2·2·1.5/20 = 0.3 (TAU-24 의 4r_SE/L 상한)',
        rp.get('boundary_rule') == 'L0' and abs((rp.get('boundary_band_frac') or 0) - 0.3) < 1e-12)

    # ── ⑦ boundary_factor 가 띠 폭에 실제로 들어간다 ──
    (A0, C0), pz0 = FIX['L0'][0], FIX['L0'][1]
    r3 = run(nc, A0, C0, pz0, 'hertzian', boundary_factor=3.0)
    chk('⑦ boundary_factor 3 → L0 · 띠 폭 2·3·1/20 = 0.3 (서명에만 있는 죽은 인자가 아니다)',
        r3.get('boundary_rule') == 'L0' and abs((r3.get('boundary_band_frac') or 0) - 0.3) < 1e-12 and r3.get('boundary_factor') == 3.0)

    # ── ⑧ 전자 · 열 채널도 같은 기록을 상위 결과로 올린다 (_run_all_networks 의 병합) ──
    mA = {}
    for i, z in enumerate(range(21), 1):
        mA[i] = {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0}            # SE 사슬
        mA[100 + i] = {'type': 2, 'x': 3.0, 'y': 0.0, 'z': float(z), 'radius': 1.0}      # AM 사슬 (떨어져 있음)
    mC = ([{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
          + [{'id1': 100 + i, 'id2': 101 + i, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)])
    with contextlib.redirect_stdout(io.StringIO()):
        ra = nc._run_all_networks(mA, mC, [1], [2], {1: 'SE', 2: 'AM_P'}, 1.0, 20.0, 10.0, 10.0, None)
    chk('⑧ 이온 (상위) · 전자 · 열 결과에 띠 규칙이 남는다 (boundary_rule · electronic_boundary_rule · thermal_boundary_rule)',
        ra.get('boundary_rule') == 'L0' and ra.get('electronic_boundary_rule') == 'L0'
        and ra.get('thermal_boundary_rule') == 'L0'
        and isinstance(ra.get('electronic_boundary_band_frac'), float) and isinstance(ra.get('thermal_boundary_band_frac'), float))

    print(f'\ntest_network_boundary_rule: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
