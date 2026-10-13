#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K6 — 관측자: σ_P (잡음 바닥) · 표면 지표 · S4 · ε_sphere · W_proxy · 회전 KE 기준.  표준 라이브러리만.

    python3 ul_observers.py --selftest

권고 기본값 (choice — docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md · 1저자 비준 대기 · CX2 §3-2 · §3-3 반례 그대로 fixture)
  σ_P (C3)   : 표본 = k* 의 마지막 두 창의 thermo **정규 줄** (setup 줄 · 겹친 경계 줄 제외 — ul_lib.parse_thermo) 의 보고 MPa (1000 · Ps — thermo 열 'ul_Ps' = v_ul_Ps 의 LIGGGHTS 머리 이름) ·
               창 범위 (시작, 끝] · ddof = 1 · 최소 표본 10 (모자라면 OBS_MISSING — NOISE_FLOOR 아님) · NOISE_FLOOR = P_meas < 3 σ_P.
               시간상관 표본 → ρ 신뢰구간 · 독립 반복으로 쓰지 않는다.
  표면 (C5)  : 고정 ID 집합 = S0 원자 − S0 에서 중심이 판 위 · 바닥 아래인 원자 (그 뒤 프레임마다 다시 자르지 않는다 — 들어 올린 판 아래로 돌아온 옛 이탈 입자를 다시 넣지 않는다) ·
               xy 를 [0, L) 로 감아 고정 원점 0 의 10 × 10 칸 · 칸 = 중심이 든 칸 · 칸 값 = max(z + r) · 지표 = 칸 값 평균 ·
               빈 칸 1 개라도 = NOT_COMPUTED (0 을 넣지도 빼지도 않는다) · p99.9 = nearest-rank (보조) · 비유한 = NOT_COMPUTED · 보고 µm.
  S4         : 창 끝 프레임 사이 표면 지표 변화 ≤ 0.002 µm / 창 (창 = 물리 시간 T_W — W(dt) = T_W / dt · §13-4).
  ε_sphere   : all = 고정 S0 ID · 반경 집합 (C_sphere = ΣV/A 일정) · inside = 그 프레임 판 안 중심 (별도 이름 · C 보존 요구 없음) · §12-9.
  W_proxy    : 정착 P(h) 사다리꼴 Σ ½(P̄_{k−1} + P̄_k) A Δh (덱 단위) × 1e-6 = 보고 J (판이 받은 일 아님 · §12-9).
  KE 기준 (C4): 회전 = UK (S0 무이동 3 창) 창 평균의 중앙값 · 병진 = 원 로그 (표) · KE_base = 합 · S2 문턱 = 10 × KE_base.
"""
from __future__ import annotations

import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _fin(*xs):
    return all(isinstance(x, (int, float)) and math.isfinite(x) for x in xs)


def sigma_P(regular, windows, ddof=1, min_n=10, col='ul_Ps', scale=1000.0):
    """regular = {step: thermo 정규 줄 dict} (ul_lib.parse_thermo) · windows = [(시작, 끝)] (창 범위 (시작, 끝]) → σ_P (보고 MPa)."""
    samples = [regular[s][col] * scale for s in sorted(regular) if col in regular[s] and any(lo < s <= hi for lo, hi in windows)]
    out = {'status': 'OBS_MISSING', 'sigma': None, 'n': len(samples), 'ddof': ddof, 'samples': samples}
    if len(samples) < max(min_n, 2) or not _fin(*samples):
        return out
    out['sigma'] = statistics.stdev(samples) if ddof == 1 else statistics.pstdev(samples)
    out['status'] = 'OK'
    return out


def noise_floor(sig, P_meas, factor=3.0):
    if sig is None or not _fin(sig, P_meas):
        return 'OBS_MISSING'
    return 'NOISE_FLOOR' if P_meas < factor * sig else 'OK'


def quantile(values, q, method='nearest_rank'):
    v = sorted(values)
    if not v:
        return None
    if method == 'nearest_rank':
        return v[max(1, math.ceil(q * len(v))) - 1]
    x = (len(v) - 1) * q
    lo = math.floor(x)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (x - lo) * (v[hi] - v[lo])


def s0_exclusion(atoms, plate_z):
    """S0 프레임에서 중심이 판 위 · 바닥 아래인 원자 id — 고정 목록 (그 뒤 프레임마다 다시 정하지 않는다)."""
    return {int(a['id']) for a in atoms if a['z'] > plate_z or a['z'] < 0.0}


def surface_index(atoms, excl, box, grid=10, q=0.999, method='nearest_rank', um=1000.0):
    out = {'status': 'NOT_COMPUTED', 'mean_um': None, 'p999_um': None, 'max_um': None, 'n_empty': None, 'n_cells': grid * grid, 'n_set': 0}
    (x0, x1), (y0, y1) = box[0], box[1]
    lx, ly = x1 - x0, y1 - y0
    cells, tops = {}, []
    for a in atoms:
        if int(a['id']) in excl:
            continue
        if not _fin(a['x'], a['y'], a['z'], a['radius']):
            out['why'] = f'비유한 값 (id {a["id"]})'
            return out
        ix = min(int(((a['x'] - x0) % lx) / lx * grid), grid - 1)
        iy = min(int(((a['y'] - y0) % ly) / ly * grid), grid - 1)
        t = a['z'] + a['radius']
        tops.append(t)
        cells[(ix, iy)] = max(cells.get((ix, iy), -math.inf), t)
    out['n_set'] = len(tops)
    out['n_empty'] = grid * grid - len(cells)
    if not tops:
        out['why'] = '집합이 비었다'
        return out
    if out['n_empty']:
        out['why'] = f'빈 칸 {out["n_empty"]} — 0 을 넣지도 빼지도 않는다'
        return out
    out['mean_um'] = sum(cells.values()) / len(cells) * um
    out['p999_um'] = quantile(tops, q, method) * um
    out['max_um'] = max(tops) * um
    out['status'] = 'OK'
    return out


def s4_check(h_prev_um, h_cur_um, limit=0.002):
    if h_prev_um is None or h_cur_um is None or not _fin(h_prev_um, h_cur_um):
        return 'NOT_COMPUTED'
    return 'PASS' if abs(h_cur_um - h_prev_um) <= limit else 'FAIL'


def eps_sphere(atoms, s0_ids, area, h):
    vol = {int(a['id']): 4.0 / 3.0 * math.pi * a['radius'] ** 3 for a in atoms if int(a['id']) in s0_ids}
    inside = [int(a['id']) for a in atoms if int(a['id']) in s0_ids and 0.0 <= a['z'] <= h]
    v_all = sum(vol.values())
    v_in = sum(vol[i] for i in inside)
    return {'C_all': v_all / area, 'eps_all': 1.0 - v_all / (area * h), 'eps_inside': 1.0 - v_in / (area * h), 'n_inside': len(inside),
            'n_all': len(vol)}


def w_proxy(steps, area, unit=1e-6):
    """steps = [(판 높이 덱 m, P̄ 덱 MPa)] (정상 단 · 순서대로) → 보고 J (W_deck × 1e-6 · 판이 받은 일 아님)."""
    w = 0.0
    for (h0, p0), (h1, p1) in zip(steps, steps[1:]):
        w += 0.5 * (p0 + p1) * 1e6 * area * (h1 - h0)
    return w * unit


def ke_base(trans, rot_window_means, factor=10.0):
    out = {'trans': trans, 'rot': None, 'base': None, 's2_limit': None}
    if trans is None or not rot_window_means or not _fin(trans, *rot_window_means):
        return out
    out['rot'] = statistics.median(rot_window_means)
    out['base'] = trans + out['rot']
    out['s2_limit'] = factor * out['base']
    return out


# ── selftest ─────────────────────────────────────────────────────────────────

def selftest():
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    # σ_P — CX2 §3-2: 0.67 · 1.33 번갈아 20 표본 (보고 MPa) → ddof 1 = NOISE_FLOOR · ddof 0 = 아님
    reg = {100000 + 500 * (i + 1): {'ul_Ps': (0.67 if i % 2 == 0 else 1.33) / 1000.0} for i in range(20)}
    win = [(100000, 105000), (105000, 110000)]
    chk('O1 σ_P ddof 1 (기본) = 0.3385728562 → 3σ 1.0157 > 1 MPa → NOISE_FLOOR',
        lambda: (lambda s: abs(s['sigma'] - 0.3385728562) < 1e-9 and s['n'] == 20 and noise_floor(s['sigma'], 1.0) == 'NOISE_FLOOR')(sigma_P(reg, win)))
    chk('O1 같은 표본 ddof 0 = 0.33 → 0.99 < 1 → 잡음 바닥 위 (ddof 가 판정을 가른다 — 고정이 필요한 까닭)',
        lambda: (lambda s: abs(s['sigma'] - 0.33) < 1e-12 and noise_floor(s['sigma'], 1.0) == 'OK')(sigma_P(reg, win, ddof=0)))
    chk('O2 표본 9 (< 최소 10) = OBS_MISSING (NOISE_FLOOR 아님)',
        lambda: (lambda s: s['status'] == 'OBS_MISSING' and noise_floor(s['sigma'], 1.0) == 'OBS_MISSING')(
            sigma_P({k: v for k, v in list(reg.items())[:9]}, win)))
    chk('O3 표본 0 = OBS_MISSING', lambda: sigma_P({}, win)['status'] == 'OBS_MISSING')
    chk('O4 창 범위 (시작, 끝] — 시작 step 줄 (앞 창 · setup 자리) 은 넣지 않는다',
        lambda: sigma_P({**reg, 100000: {'ul_Ps': 99.0}}, win)['n'] == 20)
    import inspect
    import json as _json
    cols = _json.load(open(os.path.join(HERE, 'unload_params.json'), encoding='utf-8'))['records']['thermo_cols']
    chk('O4b σ_P 기본 열 이름 = 덱 thermo 머리의 Ps 열 (표 thermo_cols · LIGGGHTS 는 v_ul_Ps 를 "ul_Ps" 로 찍는다 — "v_Ps" 면 실제 로그에서 표본 0)',
        lambda: inspect.signature(sigma_P).parameters['col'].default == 'ul_Ps' and 'ul_Ps' in cols)
    # 표면 — CX2 §3-3: 빈 칸 · 분위수 · 고정 ID
    full = [{'id': i + 1, 'x': (i % 10 + 0.5) * 0.005, 'y': (i // 10 + 0.5) * 0.005, 'z': 0.0995, 'radius': 0.0005} for i in range(100)]
    box = ((0.0, 0.05), (0.0, 0.05))
    chk('O5 100 칸 모두 100 µm = 평균 100 µm', lambda: abs(surface_index(full, set(), box)['mean_um'] - 100.0) < 1e-9)
    chk('O5 빈 칸 하나 = NOT_COMPUTED (100 도 99 도 아님 · 0 을 넣지 않는다)',
        lambda: (lambda s: s['status'] == 'NOT_COMPUTED' and s['n_empty'] == 1 and s['mean_um'] is None)(surface_index(full[:-1], set(), box)))
    chk('O6 p99.9 = nearest-rank: 99 개 100 · 1 개 200 → 200 (선형 보간이면 190.1)',
        lambda: quantile([100.0] * 99 + [200.0], 0.999) == 200.0 and abs(quantile([100.0] * 99 + [200.0], 0.999, 'linear') - 190.1) < 1e-9)
    s0 = [{'id': 1, 'x': 0.001, 'y': 0.001, 'z': 0.0995, 'radius': 0.0005}, {'id': 2, 'x': 0.001, 'y': 0.001, 'z': 0.0995, 'radius': 0.0005},
          {'id': 3, 'x': 0.001, 'y': 0.001, 'z': 0.1195, 'radius': 0.0005}]
    try:
        excl = s0_exclusion(s0, 0.110)
    except Exception:  # noqa: BLE001 — 빈 구현
        excl = None
    chk('O7 고정 ID: S0 판 (110) 위 입자 (120) 는 그 뒤 판이 130 이어도 집합 밖 — 지표 100 (프레임마다 자르면 106.67 · 거짓 회복)',
        lambda: excl == {3} and abs(surface_index(s0, excl, ((0.0, 0.05), (0.0, 0.05)), grid=1)['mean_um'] - 100.0) < 1e-9)
    wrap = [dict(a, x=a['x'] + 0.05) for a in full]
    chk('O8 xy 감기 (x + L) = 같은 칸 · 같은 지표', lambda: abs(surface_index(wrap, set(), box)['mean_um'] - 100.0) < 1e-9)
    chk('O9 비유한 z = NOT_COMPUTED', lambda: surface_index([dict(full[0], z=float('nan'))] + full[1:], set(), box)['status'] == 'NOT_COMPUTED')
    # S4 — CX2 ULR1-04: 일정 표면 속도 0.6 µm / 덱 s · 창 0.005 덱 s → 0.003 µm / 창 = FAIL · 옛 '모든 dt 에 5,000 step' (0.0025 s) → 0.0015 = 거짓 PASS
    v, T_W = 0.6, 0.005
    chk('O10 S4: 0.003 µm / 창 = FAIL (물리 창) · 같은 속도를 반 창으로 재면 0.0015 = PASS (창 정의가 판정을 바꾼다 — 덱은 W(dt) = T_W / dt)',
        lambda: s4_check(100.0, 100.0 + v * T_W) == 'FAIL' and s4_check(100.0, 100.0 + v * T_W / 2) == 'PASS')
    # ε_sphere — 고정 집합의 C 보존
    at = [{'id': i, 'z': 0.001 * i, 'radius': 0.0005} for i in range(1, 6)]
    try:
        e1, e2 = eps_sphere(at, {1, 2, 3, 4, 5}, 0.0025, 0.004), eps_sphere(at, {1, 2, 3, 4, 5}, 0.0025, 0.006)
    except Exception:  # noqa: BLE001 — 빈 구현
        e1 = e2 = {}
    chk('O11 ε_sphere,all: 고정 S0 집합 → C_sphere 같음 (h 가 달라도) · inside 는 판 안 중심만 (별도 이름)',
        lambda: e1['C_all'] == e2['C_all'] and e1['n_inside'] == 4 and e2['n_inside'] == 5 and e1['eps_inside'] != e1['eps_all'])
    # W_proxy — CX1 §6: 10 → 1 MPa (보고) · 1 µm · A = 2.5e-9 m² (실제) → 1.375e-8 J
    chk('O12 W_proxy (덱 A 0.0025 · Δh 1e-3 덱 m · P 0.01 → 0.001 덱 MPa) = 1.375e-8 J 보고',
        lambda: abs(w_proxy([(0.111052, 0.01), (0.112052, 0.001)], 0.0025) - 1.375e-8) < 1e-20)
    chk('O13 KE 기준: 회전 = UK 창 평균 중앙값 · S2 문턱 = 10 × (병진 + 회전)',
        lambda: (lambda k: k['rot'] == 2.0e-7 and abs(k['base'] - 4.04e-7) < 1e-20 and abs(k['s2_limit'] - 4.04e-6) < 1e-19)(
            ke_base(2.04e-7, [1.0e-7, 3.0e-7, 2.0e-7])))
    chk('O13 UK 창 결손 (0 개 · 비유한) = 기준 없음 (None — S2 판정 불가로 넘긴다)',
        lambda: ke_base(2.04e-7, [])['base'] is None and ke_base(2.04e-7, [float('nan'), 1e-7, 2e-7])['base'] is None)
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv[1:]:
        sys.exit(selftest())
    print(__doc__)
