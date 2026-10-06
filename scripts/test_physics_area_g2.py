#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 접촉면적 세대 2 (`physics_g2`) — C2 ①–⑤ (1저자 비준 10-06 *"권고대로"*) · L1-01 · L1-02 · L1-03 · L1-08 · DESC-03 · DESC-10 · SELF-28.

  python3 scripts/test_physics_area_g2.py

★ 시험 먼저 — 옛 코드 (HEAD 50de4e806) 에는 `plastic_coverage.film_area_g2` 가 없고 build_network 의 physics 면적이 세대 1 (sim 단위 ·
  옛 V · 하한 max + 탄성 가지 · 전역 AM–SE E*) 이라 T1–T9 의 생산 판정이 빨갛다.  반례 팔 셋은 이 파일 안에서 따로 계산한다 (생산 코드와 무관):
    · G1   — 옛 생산 경로 그대로 (`film_area_from_overlap(mode='physics')` · 단위 무시 = build_network 가 sim 단위로 부르던 것)
    · U    — 단위만 고친 팔 (DESC-03 만 — h 를 같은 길이 단위로 · 옛 V · 옛 규칙 + 탄성 가지) = "unit-only arm"
    · A    — 규칙 A (cap 이 이긴다 = `film_area_physics_v2` · 정확 lens · 단위 교정 · 쌍 E* 없음 · 탄성 가지)
  ⇒ 판별력: U 는 T1 (옛 V) · T4 (항복 개시 불연속) 에서, A 는 T4 (항복 개시에서 면적이 떨어진다 · 비단조) · T3 (원판 아래) 에서 실패해야 한다.
★ 규칙 B (비준 ②): A = max(A_disc, min(A_Tabor, V_lens/(h·length_scale), cap)) · floor A_disc = c_cpl[22] 기하 원판 (= Hertz 모드 면적) ·
  모든 δ 에서 같은 floor (탄성 가지 없음) ⇒ 간선마다 R_c(physics) ≤ R_c(hertz) (T8 불변식).
  상수는 **동결 oracle** 로 따로 둔다 (솔버 · plastic_coverage 에서 빌리면 상수 변이가 기대값과 같이 움직인다 — test_psi_default_switch 와 같은 규약).
⚠ 범위 — 면적 규칙 · 단위 · 쌍 · 기록의 식 시험과 실침대 (real_14 커밋 덤프) 의 간선 불변식이다.  σ 값 · 물리 정확도 · Coverage (⑥ 합집합 피복 ·
  커밋 B) 로 확대하지 않는다 (h_film 5 nm 는 [미확인] — L1-08).
"""
import contextlib
import gzip
import io
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
_ok, _fail = 0, []

#  ── 동결 oracle 상수 (plastic_coverage 의 값 · 여기서 다시 적는다 — import 하지 않는다) ──
E_SE, E_AM, NU_SE, NU_AM = 24.0e9, 140.0e9, 0.30, 0.25
H_SE, SIGMA_Y = 0.85e9, 0.30e9
H_FILM_M = 5.0e-9
ESTAR = {'AM_SE': 1.0 / ((1.0 - NU_AM ** 2) / E_AM + (1.0 - NU_SE ** 2) / E_SE),
         'SE_SE': 1.0 / (2.0 * (1.0 - NU_SE ** 2) / E_SE)}               # 22.4149 · 13.1868 GPa (L1-03)
DR_YIELD = (0.8 * math.pi * SIGMA_Y / ESTAR['AM_SE']) ** 2               # 옛 탄성 가지 문턱 (반례 팔 U · A 만 쓴다)
PSI_EXP, PSI_FLOOR = 1.5, 1e-4
UM = 1e6                                                                 # µm 단위: 1 m = 1e6 µm


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {extra}' if extra else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {extra}' if extra else ''))


def _guard(label, fn):
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001 — 옛 코드 = 없는 함수 · 인자도 FAIL 로 센다
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


def disc(r1, r2, delta):
    """두 구의 교차 원판 (c_cpl[22] 기하) — 독립 구현 (lens_geometry 를 빌리지 않는다)."""
    d = r1 + r2 - delta
    if d <= 0 or delta <= 0:
        return 0.0
    a2 = (4.0 * d * d * r1 * r1 - (d * d - r2 * r2 + r1 * r1) ** 2) / (4.0 * d * d)
    return math.pi * max(a2, 0.0)


def lens_closed(r1, r2, delta):
    """정확 lens 부피 — 독립 닫힌 식 (πδ²(d² + 2d(r₁+r₂) − 3(r₁−r₂)²)/(12d))."""
    d = r1 + r2 - delta
    if delta <= 0:
        return 0.0
    if d <= abs(r1 - r2):
        return 4.0 / 3.0 * math.pi * min(r1, r2) ** 3
    return math.pi * delta * delta * (d * d + 2.0 * d * (r1 + r2) - 3.0 * (r1 - r2) ** 2) / (12.0 * d)


def lens_quad(r1, r2, delta, n=200001):
    """정확 lens 부피 — 독립 수치적분 (x 단면 원 면적 적분 · 닫힌 식과 다른 경로)."""
    import numpy as np
    d = r1 + r2 - delta
    lo, hi = max(-r1, d - r2), min(r1, d + r2)
    x = np.linspace(lo, hi, n)
    a = np.minimum(np.sqrt(np.maximum(r1 * r1 - x * x, 0.0)), np.sqrt(np.maximum(r2 * r2 - (x - d) ** 2, 0.0)))
    return float(np.trapezoid(np.pi * a * a, x)) if hasattr(np, 'trapezoid') else float(np.trapz(np.pi * a * a, x))


def oracle_b(delta, r1, r2, pair, ligg, L, consumer='transport'):
    """규칙 B 의 독립 구현 → (A, binding).  길이 단위 = 1 m 가 L 단위."""
    floor = ligg if (ligg is not None and ligg > 0) else disc(r1, r2, delta)
    if delta <= 0:
        return floor, 'none'
    if pair == 'AM_AM':
        return floor, 'native_unsupported_pair'
    Rs = r1 * r2 / (r1 + r2)
    caps = {'tabor': (4.0 / 3.0) * ESTAR[pair] * math.sqrt(Rs) * delta ** 1.5 / H_SE,
            'volume': lens_closed(r1, r2, delta) / (H_FILM_M * L),
            'cap': (math.pi if consumer == 'transport' else 2.0 * math.pi) * min(r1, r2) ** 2}
    U = min(caps.values())
    if floor >= U:
        return floor, 'floor'
    return U, next(k for k in ('tabor', 'volume', 'cap') if caps[k] == U)


# ── 반례 팔 (생산 코드와 무관 · 판별력 증명용) ──────────────────────────────────────────────────────────
def arm_g1(delta, r1, r2, pair, ligg, L):
    """옛 생산 경로 — build_network 가 sim 단위 그대로 부르던 legacy physics (단위 · 쌍 무시)."""
    import plastic_coverage as pc
    Rs = r1 * r2 / (r1 + r2)
    A, _rg, c = pc.film_area_from_overlap(delta, Rs, R_min=min(r1, r2), ligg_area=ligg, mode='physics', return_components=True)
    return A, c.get('binding') or _rg


def arm_unit_only(delta, r1, r2, pair, ligg, L):
    """DESC-03 만 고친 팔 — h = 5 nm 를 같은 단위로 · 옛 V (π/6 δ²(3R*−δ)) · 옛 하한 max + 탄성 가지 · 전역 AM–SE E* · cap 2π r²."""
    Rs = r1 * r2 / (r1 + r2)
    if delta <= 0:
        return 0.0, 'none'
    A_h = math.pi * Rs * delta
    if delta / Rs < DR_YIELD:
        return A_h, 'elastic'
    U = min((4.0 / 3.0) * ESTAR['AM_SE'] * math.sqrt(Rs) * delta ** 1.5 / H_SE,
            math.pi / 6.0 * delta * delta * (3.0 * Rs - delta) / (H_FILM_M * L), 2.0 * math.pi * min(r1, r2) ** 2)
    return max(A_h, ligg or 0.0, U), 'max'


def arm_rule_a(delta, r1, r2, pair, ligg, L):
    """규칙 A (cap 이 이긴다) — `film_area_physics_v2` (정확 lens · 단위 교정 · 탄성 가지 · 쌍 E* 없음 · cap 2π r²)."""
    import plastic_coverage as pc
    A, c = pc.film_area_physics_v2(delta, r1, r2, length_scale=L, ligg_area=ligg)
    return A, c['binding']


def prod(delta, r1, r2, pair, ligg, L, consumer='transport'):
    """생산 함수 (세대 2) — 없으면 AttributeError (옛 코드 = 시험 먼저의 빨간불)."""
    import plastic_coverage as pc
    A, b = pc.film_area_g2(delta, r1, r2, pair=pair, ligg_area=ligg, length_scale=L, consumer=consumer)
    return A, b


# ── 판정 (팔을 인자로 받는다 — 생산 · 반례에 같은 판정을 건다) ──────────────────────────────────────────
GEOMS = (((0.5, 0.5), 'SE_SE'), ((1.0, 1.0), 'SE_SE'), ((0.5, 6.0), 'AM_SE'), ((2.0, 0.5), 'AM_SE'), ((6.0, 2.0), 'AM_SE'))


def _sweep(r1, r2, n=240):
    """δ 격자 — 1e-5·R* … 0.9·min(r) (원판이 δ 에 단조인 범위) + 옛 항복 개시 ±1e-9 · ±1e-6."""
    Rs = r1 * r2 / (r1 + r2)
    lo, hi = math.log(1e-5 * Rs), math.log(0.9 * min(r1, r2))
    ds = [math.exp(lo + (hi - lo) * i / (n - 1)) for i in range(n)]
    dy = DR_YIELD * Rs
    ds += [dy * (1 - 1e-6), dy * (1 - 1e-9), dy * (1 + 1e-9), dy * (1 + 1e-6)]
    return sorted(ds), dy


def t3_floor(arm):
    """T3 — 규칙 B: 모든 δ 에서 A ≥ A_disc (c_cpl[22] 원판 = Hertz 모드 면적) · 위반 (기하, δ) 목록."""
    bad = []
    for (r1, r2), pair in GEOMS:
        for d in _sweep(r1, r2, 60)[0]:
            lg = disc(r1, r2, d)
            A, _b = arm(d, r1, r2, pair, lg, UM)
            if A < lg * (1 - 1e-12):
                bad.append((r1, r2, pair, d, A / lg))
    return bad


def t4_mono(arm):
    """T4 — A(δ) 가 δ 에 단조 비감소 · 옛 항복 개시 ±1e-9 에서 연속 (상대 점프 ≤ 1e-6) · 위반 목록."""
    bad = []
    for (r1, r2), pair in GEOMS:
        ds, dy = _sweep(r1, r2)
        As = [arm(d, r1, r2, pair, disc(r1, r2, d), UM)[0] for d in ds]
        for i in range(len(ds) - 1):
            if As[i + 1] < As[i] * (1 - 1e-12):
                bad.append(('비단조', r1, r2, pair, ds[i], As[i + 1] / As[i]))
                break
        lo = arm(dy * (1 - 1e-9), r1, r2, pair, disc(r1, r2, dy * (1 - 1e-9)), UM)[0]
        hi = arm(dy * (1 + 1e-9), r1, r2, pair, disc(r1, r2, dy * (1 + 1e-9)), UM)[0]
        if abs(hi / lo - 1.0) > 1e-6:
            bad.append(('불연속', r1, r2, pair, dy, hi / lo))
    return bad


def t1_lens(arm):
    """T1 — 부피 cap 이 결속하는 접촉 (작은 반경 0.1–0.15 µm · δ 12–18 nm — 실침대 반경 ≥ 0.5 µm 에서는 부피가 원판 · Tabor 보다 크지
    않아 결속하지 않는다) 에서 A = V_lens/(h·L) (정확 lens · 독립 수치적분 대조 · 상대 1e-5) · 위반 목록."""
    bad = []
    for r1, r2, d, pair in ((0.1, 0.1, 0.015, 'SE_SE'), (0.1, 0.3, 0.015, 'AM_SE'), (0.1, 0.12, 0.018, 'SE_SE'), (0.15, 0.15, 0.012, 'SE_SE')):
        want = lens_quad(r1, r2, d) / (H_FILM_M * UM)
        got, b = arm(d, r1, r2, pair, disc(r1, r2, d), UM)
        if abs(got / want - 1.0) > 1e-5:
            bad.append((r1, r2, d, pair, got, want, b))
    return bad


def _gz_items(path, tag):
    with gzip.open(path, 'rt') as fh:
        lines = fh.read().splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(tag):
            head = ln.replace(tag, '').split()
            return head, [ln_.split() for ln_ in lines[i + 1:] if ln_ and not ln_.startswith('ITEM')]
    raise ValueError(path)


def load_real14():
    """커밋된 real_14 기준 덤프 (docs/data/real14_reference_20260928) → (atoms, contacts, type_map, plate_z, box)."""
    d = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
    ha, ra = _gz_items(os.path.join(d, 'atom_2060000.liggghts.gz'), 'ITEM: ATOMS')
    ia = {k: ha.index(k) for k in ('id', 'type', 'x', 'y', 'z', 'radius')}
    A = {int(r[ia['id']]): {'type': int(r[ia['type']]), 'x': float(r[ia['x']]), 'y': float(r[ia['y']]),
                            'z': float(r[ia['z']]), 'radius': float(r[ia['radius']])} for r in ra}
    hc, rc = _gz_items(os.path.join(d, 'contact_2060000.liggghts.gz'), 'ITEM: ENTRIES')
    j1, j2, jA, jD = (hc.index('c_cpl[7]'), hc.index('c_cpl[8]'), hc.index('c_cpl[22]'), hc.index('c_cpl[23]'))
    C = [{'id1': int(float(r[j1])), 'id2': int(float(r[j2])), 'contact_area': float(r[jA]), 'delta': float(r[jD])} for r in rc]
    return A, C, {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, 0.0302845, 0.05


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def main():
    import network_conductivity as nc
    import plastic_coverage as pc

    # ── T1 L1-02 정확 lens (옛 V 경로 없음 · DESC-10) ──
    def s1():
        bad_u = t1_lens(arm_unit_only)                              # 반례 먼저 (생산 함수가 없는 옛 코드에서도 돈다)
        chk('T1b 판별력: 단위만 고친 팔 (옛 V = π/6 δ²(3R*−δ) · 정확 lens 의 ≈ 0.49 배 · 옛 하한 max) 은 T1 에서 실패한다', bool(bad_u), str(bad_u[:1]))
        bad_p = t1_lens(prod)
        bind = [prod(d, r1, r2, p, disc(r1, r2, d), UM)[1] for r1, r2, d, p in ((0.1, 0.1, 0.015, 'SE_SE'), (0.1, 0.3, 0.015, 'AM_SE'))]
        chk('T1 ★ 부피 결속 접촉의 생산 면적 = 정확 lens / (h·length_scale) (독립 수치적분 · 상대 1e-5 · 결속 이름 volume) — 옛 V 경로가 없다 (DESC-10)',
            not bad_p and bind == ['volume', 'volume'], str(bad_p[:2]) + repr(bind))
        _A, _b, c = pc.film_area_g2(0.95, 0.5, 0.5, pair='SE_SE', ligg_area=disc(0.5, 0.5, 0.95), length_scale=UM, consumer='transport',
                                    return_components=True)
        chk('T1c 깊은 겹침 (r 0.5 · δ 0.95 µm) — 성분 V_lens = 정확 lens 양수 (옛 식은 음수) = 닫힌 식 (상대 1e-12)',
            c.get('V_lens', -1) > 0 and abs(c['V_lens'] / lens_closed(0.5, 0.5, 0.95) - 1.0) < 1e-12, repr(c.get('V_lens')))
    _guard('T1', s1)

    # ── T2 DESC-03 단위 공변 — 같은 접촉을 m · mm · µm 로 ──
    def s2():
        def cov(arm):
            bad = []
            for (r1, r2), pair in GEOMS:
                for fr in (0.002, 0.01, 0.05, 0.2):
                    d_m, r1m, r2m = fr * min(r1, r2) / UM, r1 / UM, r2 / UM
                    ref = None
                    for L in (1.0, 1e3, 1e6):
                        A, b = arm(d_m * L, r1m * L, r2m * L, pair, disc(r1m * L, r2m * L, d_m * L), L)
                        cur = (b, A / (L * L))
                        if ref is None:
                            ref = cur
                        elif cur[0] != ref[0] or abs(cur[1] / ref[1] - 1.0) > 1e-9:
                            bad.append((r1, r2, pair, fr, L, ref, cur))
                            break
            return bad
        bg = cov(arm_g1)                                            # 반례 먼저
        chk('T2b 판별력: 옛 생산 경로 (sim 단위 그대로 · h 는 SI) 는 단위에 따라 결속이 뒤집힌다', bool(bg), str(bg[:1]))
        bp = cov(prod)
        chk('T2 ★ 단위 공변 (DESC-03) — m · mm · µm 로 같은 접촉: 결속 같고 면적 = (단위)² 배 (상대 1e-9) · 5 기하 × 4 겹침', not bp, str(bp[:1]))
        A_sc = {}
        for scale in (1000.0, 1.0):                                  # sim = mm (scale 1000) · sim = µm (scale 1)
            atoms = {1: {'type': 1, 'radius': 0.5 / scale, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                     2: {'type': 1, 'radius': 0.5 / scale, 'x': (1.0 - 0.01) / scale, 'y': 0.0, 'z': 0.0}}
            rows = [{'id1': 1, 'id2': 2, 'contact_area': disc(0.5, 0.5, 0.01) / scale ** 2, 'delta': 0.01 / scale}]
            n = quiet(nc.build_network, atoms, rows, {1}, scale, 10.0, box_x=1e3, box_y=1e3, mode='ionic', type_map={1: 'SE'},
                      contact_mode='physics')
            A_sc[scale] = n['edges'][0]['A_physics']
        want = prod(0.01, 0.5, 0.5, 'SE_SE', disc(0.5, 0.5, 0.01), UM)[0]
        chk('T2c build_network 은 µm 값 + length_scale 1e6 으로 부른다 — sim 척도 (mm · µm) 와 무관하게 A_physics (µm²) = film_area_g2(µm) (상대 1e-12)',
            all(abs(v / want - 1.0) < 1e-12 for v in A_sc.values()), f'{A_sc} vs {want}')
    _guard('T2', s2)

    # ── T3 L1-01 규칙 B — floor = 원판 · 상한 셋의 min 은 연장분만 ──
    def s3():
        chk('T3b 판별력: 규칙 A (cap 이 이긴다) 는 원판 아래로 내려간다 (T3 floor 위반)', bool(t3_floor(arm_rule_a)))   # 반례 먼저
        bad = []
        for (r1, r2), pair in GEOMS + (((2.0, 6.0), 'AM_AM'),):
            for d in _sweep(r1, r2, 50)[0]:
                for lg in (disc(r1, r2, d), None, 0.0, 1.7 * disc(r1, r2, d)):
                    A, b = prod(d, r1, r2, pair, lg, UM)
                    wA, wb = oracle_b(d, r1, r2, pair, lg, UM)
                    if b != wb or abs(A / wA - 1.0) > 1e-12:
                        bad.append((r1, r2, pair, d, lg, (A, b), (wA, wb)))
        chk('T3 ★ 규칙 B (독립 oracle) — A = max(A_disc, min(A_Tabor, V_lens/(h·L), π r_min²)) · 결속 이름 · ligg 없음 · 0 → 기하 원판 · '
            '원판보다 큰 ligg 도 floor (6 기하 × 50 δ × 4 ligg)', not bad, str(bad[:2]))
        chk('T3c 생산 = 모든 δ 에서 A ≥ 원판 (floor 위반 0)', not t3_floor(prod))
    _guard('T3', s3)

    # ── T4 단조 · 연속 (규칙 A 의 반례) ──
    def s4():
        ba, bu = t4_mono(arm_rule_a), t4_mono(arm_unit_only)        # 반례 먼저
        chk('T4b ★ 판별력: 규칙 A 는 T4 에서 실패한다 (항복 개시에서 면적이 떨어진다 · 비단조)', bool(ba), str(ba[:2]))
        chk('T4c 판별력: 단위만 고친 팔도 T4 에서 실패한다 (항복 개시에서 πR*δ → ≥ 원판 으로 뛴다)', bool(bu), str(bu[:2]))
        bp = t4_mono(prod)
        chk('T4 ★ 생산 A(δ) 단조 비감소 · 옛 항복 개시 (DR_YIELD_ONSET) 에서 연속 (탄성 가지 없음) — 5 기하 × 244 δ', not bp, str(bp[:2]))
    _guard('T4', s4)

    # ── T5 L1-03 쌍별 E* ──
    def s5():
        a_se, b_se = prod(0.05, 1.0, 1.0, 'SE_SE', disc(1.0, 1.0, 0.05), UM)
        a_am, b_am = prod(0.05, 1.0, 1.0, 'AM_SE', disc(1.0, 1.0, 0.05), UM)
        chk('T5 ★ SE–SE / AM–SE 의 Tabor 면적 비 = E*_SESE/E*_AMSE = 0.5883 (동결 oracle · 두 쪽 다 tabor 결속)',
            b_se == b_am == 'tabor' and abs((a_se / a_am) / (ESTAR['SE_SE'] / ESTAR['AM_SE']) - 1.0) < 1e-12,
            f'{b_se}/{b_am} {a_se / a_am:.6f}')
        A_aa, b_aa = prod(0.3, 2.0, 6.0, 'AM_AM', disc(2.0, 6.0, 0.3), UM)
        chk("T5b AM–AM = 원판 그대로 · 결속 'native_unsupported_pair' (NCM 경도 앵커 없음)",
            b_aa == 'native_unsupported_pair' and A_aa == disc(2.0, 6.0, 0.3))
        raised = []
        for p in ('XX', None, 'SE_AM', 'am_se'):
            try:
                prod(0.05, 1.0, 1.0, p, None, UM)
            except ValueError:
                raised.append(p)
        chk('T5c 모르는 쌍 → ValueError (조용히 AM–SE 로 떨어지지 않는다)', raised == ['XX', None, 'SE_AM', 'am_se'], repr(raised))
        #  build_network 의 쌍 분류 — 열 망 (전 접촉) 에서 SE–SE · AM–SE · AM–AM 이 각각 그 이름
        atoms = {1: {'type': 3, 'radius': 0.5, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                 2: {'type': 3, 'radius': 0.5, 'x': 0.98, 'y': 0.0, 'z': 0.0},
                 3: {'type': 1, 'radius': 2.0, 'x': 0.0, 'y': 2.48, 'z': 0.0},
                 4: {'type': 2, 'radius': 1.0, 'x': 0.0, 'y': 2.48 + 2.98, 'z': 0.0}}
        rows = [{'id1': 1, 'id2': 2, 'contact_area': disc(0.5, 0.5, 0.02), 'delta': 0.02},
                {'id1': 1, 'id2': 3, 'contact_area': disc(0.5, 2.0, 0.02), 'delta': 0.02},
                {'id1': 3, 'id2': 4, 'contact_area': disc(2.0, 1.0, 0.02), 'delta': 0.02}]
        tm = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
        n = quiet(nc.build_network, atoms, rows, [1, 2, 3], 1.0, 10.0, box_x=1e3, box_y=1e3, mode='thermal', type_map=tm,
                  contact_mode='physics')
        got = {tuple(sorted((e['id1'], e['id2']))): (e['A_components'] or {}).get('pair') for e in n['edges']}
        chk('T5d build_network 쌍 분류 (type_map) — SE–SE · AM_P–SE → AM_SE · AM_P–AM_S → AM_AM', got == {(1, 2): 'SE_SE', (1, 3): 'AM_SE', (3, 4): 'AM_AM'},
            repr(got))
        errs = []
        for tmx in (None, {1: 'AM_P', 2: 'AM_S', 3: 'VGCF'}):
            try:
                quiet(nc.build_network, atoms, rows, [1, 2, 3], 1.0, 10.0, box_x=1e3, box_y=1e3, mode='thermal', type_map=tmx,
                      contact_mode='physics')
            except ValueError as e:
                errs.append(str(e)[:40])
        chk('T5e physics 모드 — type_map 없음 · 모르는 상 이름 → ValueError (거부 · fail-closed)', len(errs) == 2, repr(errs))
    _guard('T5', s5)

    # ── T6 L1-08 h_film 5 nm — 값 유지 + [미확인] 표지 + 기록 ──
    def s6():
        _A, _b, c = pc.film_area_g2(0.003, 0.5, 0.5, pair='SE_SE', ligg_area=disc(0.5, 0.5, 0.003), length_scale=UM, consumer='transport',
                                    return_components=True)
        chk('T6 h_film = 5 nm × length_scale (µm 값 0.005) · 성분에 실린다', abs(c.get('h_film', 0) - 0.005) < 1e-15, repr(c.get('h_film')))
        A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
        C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
        r = quiet(nc.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='physics', mode='ionic')
        chk("T6b 결과에 h_film_nm = 5.0 · h_film_status 가 '[미확인]' 로 시작 (L1-08 — 앵커 Sakuda 2013 이 이 상수를 주지 않는다)",
            r.get('h_film_nm') == 5.0 and str(r.get('h_film_status', '')).startswith('[미확인]'), repr((r.get('h_film_nm'), r.get('h_film_status'))))
    _guard('T6', s6)

    # ── T7 SELF-28 ψ floor 동결 (ψ ≤ 1e-4 → R_c = 0) — g2 · 곱셈 망 ──
    def s7():
        s_star = 1.0 - PSI_FLOOR ** (1.0 / PSI_EXP)                  # 0.99784556531 (ψ = (1 − s)^1.5 = 1e-4)
        out = {}
        for lbl, s in (('floor 위 (s*·(1−1e-4))', s_star * (1 - 1e-4)), ('floor 아래 (s* 와 1 사이)', 0.5 * (s_star + 1.0)),
                       ('clamp (ligg > π r²)', 1.02)):
            ligg = math.pi * (s * 1.0) ** 2
            atoms = {1: {'type': 1, 'radius': 1.0, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                     2: {'type': 1, 'radius': 1.0, 'x': 2.0 - 1e-4, 'y': 0.0, 'z': 0.0}}
            r = quiet(nc.build_network, atoms, [{'id1': 1, 'id2': 2, 'contact_area': ligg, 'delta': 1e-4}], {1}, 1.0, 10.0,
                      box_x=1e4, box_y=1e4, mode='ionic', type_map={1: 'SE'}, contact_mode='physics')
            e = r['edges'][0]
            a_eff = min(math.sqrt(e['A_contact'] / math.pi), 1.0)
            psi = max(1.0 - a_eff, 0.0) ** PSI_EXP
            out[lbl] = (e['R_constriction'], psi, r.get('n_floor_only'), r.get('n_clamp_zero'),
                        (e['A_components'] or {}).get('binding'))
        f_up, f_dn, f_cl = out.values()
        chk('T7 ★ floor 위 — R_c = ψ/(2a_eff) > 0 (곱셈) · floor 아래 (s < 1) → R_c = 0 (n_floor_only 1) · clamp (a ≥ r_min) → 0 (n_clamp_zero 1) · '
            '면적 = floor (ligg) 결속', f_up[0] > 0 and abs(f_up[0] - f_up[1] / (2.0 * math.sqrt(math.pi * (s_star * (1 - 1e-4)) ** 2 / math.pi))) < 1e-9
            and f_dn[0] == 0.0 and f_dn[2] == 1 and f_dn[3] == 0 and f_cl[0] == 0.0 and f_cl[3] == 1 and f_cl[2] == 0
            and f_up[4] == f_dn[4] == f_cl[4] == 'floor', repr(out))
    _guard('T7', s7)

    # ── T8 ★ 불변식 R_c(physics) ≤ R_c(hertz) 간선마다 — 실침대 real_14 (커밋 덤프) ──
    def s8():
        A, C, tm, pz, box = load_real14()
        worst, n_cmp, n_viol, n_rcA = 0.0, 0, 0, 0
        for mode, tt in (('thermal', [1, 2, 3]), ('electronic', [1, 2])):
            nets = {cm: quiet(nc.build_network, A, C, tt, 1000.0, pz, box, box, 2.0, mode=mode, type_map=tm, contact_mode=cm)
                    for cm in ('hertzian', 'physics')}
            eh = {(e['id1'], e['id2']): e for e in nets['hertzian']['edges']}
            for e in nets['physics']['edges']:
                h = eh[(e['id1'], e['id2'])]
                n_cmp += 1
                if e['R_constriction'] > h['R_constriction'] * (1 + 1e-12):
                    n_viol += 1
                    worst = max(worst, e['R_constriction'] / h['R_constriction'])
                #  반례: 같은 간선에 규칙 A 면적 (film_area_physics_v2 · µm) 을 넣고 같은 ψ 곱셈식으로 R_c — 원판 아래면 Hertz 보다 커질 수 있다
                if mode == 'thermal' and e['delta'] > 0:
                    a_A, _bA = arm_rule_a(e['delta'] * 1000.0, e['r1'], e['r2'], None, e['A_hertzian'], UM)
                    r_min = min(e['r1'], e['r2'])
                    aa = min(math.sqrt(a_A / math.pi), r_min) if a_A > 0 else 0.0
                    if aa > 0:
                        ps = max(1.0 - aa / r_min, 0.0) ** PSI_EXP
                        rcA = (ps / (2.0 * aa)) if ps > PSI_FLOOR else 0.0
                        k_w = h['R_Maxwell'] * 2.0 * math.sqrt(h['A_hertzian'] / math.pi) if h['A_hertzian'] > 0 else 1.0   # = 1/(σ_rel·k)
                        if h['A_hertzian'] > 0 and rcA * k_w > h['R_constriction'] * (1 + 1e-12):
                            n_rcA += 1
        chk(f'T8 ★ 불변식 — real_14 (커밋 덤프) 열 · 전자 망 {n_cmp} 간선: R_c(physics g2) ≤ R_c(hertz) 위반 {n_viol} (floor = c_cpl[22] 원판 = Hertz 면적 · ψ ≤ 1)',
            n_cmp > 100000 and n_viol == 0, f'최대 비 {worst:.6g}')
        chk(f'T8b 판별력: 같은 간선에 규칙 A 면적을 넣으면 R_c > R_c(hertz) 가 생긴다 ({n_rcA} 간선)', n_rcA > 0)
    _guard('T8', s8)

    # ── T9 배선 · 기록 — build_network physics 기본 = g2 (µm + 쌍) · area_rule_physics · 결속 수 · 세대 1 명시 재현 ──
    def s9():
        atoms = {1: {'type': 3, 'radius': 0.5e-3, 'x': 0.0, 'y': 0.0, 'z': 0.0005},
                 2: {'type': 3, 'radius': 0.5e-3, 'x': 0.98e-3, 'y': 0.0, 'z': 0.0005},
                 3: {'type': 1, 'radius': 6.0e-3, 'x': 0.0, 'y': 6.45e-3, 'z': 0.0005}}
        rows = [{'id1': 1, 'id2': 2, 'contact_area': disc(0.5, 0.5, 0.02) * 1e-6, 'delta': 0.02e-3},
                {'id1': 1, 'id2': 3, 'contact_area': disc(0.5, 6.0, 0.05) * 1e-6, 'delta': 0.05e-3}]
        tm = {1: 'AM_P', 3: 'SE'}
        n2 = quiet(nc.build_network, atoms, rows, [1, 3], 1000.0, 10.0, box_x=1.0, box_y=1.0, mode='thermal', type_map=tm,
                   contact_mode='physics')
        bad = []
        for e in n2['edges']:
            pair = (e['A_components'] or {}).get('pair')
            want = prod(e['delta'] * 1000.0, e['r1'], e['r2'], pair, e['A_hertzian'], UM)[0]
            if e['A_physics'] != want:
                bad.append((e['id1'], e['id2'], e['A_physics'], want))
        chk('T9 ★ build_network physics 기본 = film_area_g2 (µm · length_scale 1e6 · 쌍 · ligg = c_cpl[22]) — 간선 A_physics 비트 동일', not bad, repr(bad))
        n1 = quiet(nc.build_network, atoms, rows, [1, 3], 1000.0, 10.0, box_x=1.0, box_y=1.0, mode='thermal', type_map=tm,
                   contact_mode='physics', area_rule='physics_g1')
        bad1 = []
        ca_sim = {tuple(sorted((c_['id1'], c_['id2']))): c_['contact_area'] for c_ in rows}
        for e in n1['edges']:
            r1s, r2s = atoms[e['id1']]['radius'], atoms[e['id2']]['radius']           # sim 반경 그대로 (옛 경로의 입력)
            Rs = (r1s * r2s) / (r1s + r2s)
            A0, _rg = pc.film_area_from_overlap(e['delta'], Rs, R_min=min(r1s, r2s), ligg_area=ca_sim[(e['id1'], e['id2'])],
                                                mode='physics')
            if e['A_physics'] != A0 * 1000.0 ** 2:
                bad1.append((e['id1'], e['id2'], e['A_physics'], A0 * 1e6))
        chk("T9b 세대 1 은 명시 area_rule='physics_g1' 로 그대로 — 옛 sim 단위 경로 (film_area_from_overlap) 와 비트 동일",
            not bad1 and n1.get('area_rule_physics') == 'physics_g1' and n2.get('area_rule_physics') == 'physics_g2', repr(bad1))
        try:
            quiet(nc.build_network, atoms, rows, [1, 3], 1000.0, 10.0, mode='thermal', type_map=tm, contact_mode='physics', area_rule='g3')
            r_unk = False
        except ValueError:
            r_unk = True
        chk('T9c 모르는 area_rule → ValueError', r_unk)
        A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
        A.update({100 + i: {'type': 2, 'x': 5.0, 'y': 0.0, 'z': float(z), 'radius': 2.0} for i, z in enumerate(range(0, 21, 4), 1)})
        C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
        C += [{'id1': 100 + i, 'id2': 101 + i, 'contact_area': 0.3, 'delta': 0.1} for i in range(1, 6)]
        out = {cm: quiet(nc._run_all_networks, A, C, [1], [2], {1: 'SE', 2: 'AM_P'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
               for cm in ('physics', 'hertzian')}
        rp, rh = out['physics'], out['hertzian']
        keys_ok = all(isinstance(rp.get(k), dict) for k in ('area_binding_counts_physics', 'electronic_area_binding_counts_physics',
                                                             'thermal_area_binding_counts_physics'))
        chk("T9d 결과 기록 — area_rule_physics = physics_g2 (이온 · 전자 · 열) · area_rule (physics = physics_g2 · hertz = hertz_ccpl22) · "
            "결속 수 dict · n_clamp_zero · n_floor_only (세 채널)",
            rp.get('area_rule_physics') == rp.get('electronic_area_rule_physics') == rp.get('thermal_area_rule_physics') == 'physics_g2'
            and rp.get('area_rule') == 'physics_g2' and rh.get('area_rule') == 'hertz_ccpl22' and keys_ok
            and all(isinstance(rp.get(k), int) for k in ('n_clamp_zero', 'n_floor_only', 'electronic_n_clamp_zero', 'electronic_n_floor_only',
                                                          'thermal_n_clamp_zero', 'thermal_n_floor_only'))
            and sum(rp['area_binding_counts_physics'].values()) == rp.get('n_edges'),
            repr({k: rp.get(k) for k in ('area_rule_physics', 'area_rule', 'area_binding_counts_physics', 'n_clamp_zero', 'n_floor_only')}))
        nh = quiet(nc.build_network, A, C, [1], 1.0, 20.0, 10.0, 10.0, mode='ionic', type_map=None, contact_mode='hertzian')
        chk('T9e hertzian 모드는 type_map 이 없어도 돈다 (physics 면적은 진단 칸 — None) · R_c 는 Maxwell 그대로',
            nh is not None and all(e['A_physics'] is None for e in nh['edges'])
            and all(e['R_constriction'] == e['R_Maxwell'] for e in nh['edges']))
    _guard('T9', s9)

    print(f'\ntest_physics_area_g2: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
