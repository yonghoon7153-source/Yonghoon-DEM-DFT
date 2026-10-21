#!/usr/bin/env python3
"""믹서 D3 설계 v2 — 규칙 검사 (v1 규칙의 반례 재현 → v2 규칙이 잡는가) + v2 표의 lab20261014 숫자 (읽기 전용).

    python3 -I docs/reviews/mixer_d3_design_v2_evidence_20261021/d3_v2_rule_checks.py

* 시뮬레이션 0 · 덱 생성 0 · 파일 쓰기 0 — 생성기 `scripts/make_mixer_deck.py` 와 접촉 계약 검사기
  `scripts/check_contact_validity.py` 의 **함수만** 부른다 (화면 출력만).
* 규칙 = 설계 문서의 규칙을 옮긴 **작은 참조 구현** (설계의 실행 가능한 명세) 이다 — DEM 결과가 아니다.
  반례 · 대조에 쓰는 수 중 [가정 예시] = 꼴을 보이는 예시값 (측정이 아니고 등록 숫자로 쓰지 않는다).
* 검사 C01–C17 (번호 = 원장 MXD3-NN = 요청서 D3K-NN · C16 = 문안이라 검사 없음) 마다
    (가) 반례 — v1 규칙은 잘못 받아들인다 (= 반례 재현) · v2 규칙은 잡아야 한다
    (나) 대조 — 옳은 경우를 v2 규칙도 받아들여야 한다 (전부 거부해서 '잡는' 판을 막는다)
* 대상 설계 v1 = `docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md` · v2 = `…_design_v2_20261021.md`.
* 종료 코드 0 = 모든 검사에서 v1 = 반례 재현 · v2 = 잡음 + 대조 통과.  v2 규칙이 없으면 (시험 먼저 단계) 1.
"""
import functools
import importlib.util
import math
import os
import random
import sys

sys.dont_write_bytecode = True        # 불러온 리포 모듈의 바이트코드 캐시 (`scripts/__pycache__`) 도 쓰지 않는다

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m = _load('mmd', 'scripts/make_mixer_deck.py')
ccv = _load('ccv', 'scripts/check_contact_validity.py')

LAB = 'lab20261014'                   # Q11 비준 세대 (v2 숫자 전부)
GEN1 = None                           # gen1 = 생성기 DENS 그 객체 (v1 숫자의 출처 · 이력 칸만)
CGF = 151.4
N_TOTAL = 100000
NU_SE = m.PHASE_MECH['SE'][0]
GRID = [m.BO_BASE * 10 ** (k / 2.0) for k in range(7)] + [3000.0 * m.BO_BASE]   # 설계 격자 8 수준 (Bo_code)
X = [math.log10(b) for b in GRID]


def lx(bo):
    return math.log10(bo)


# ───────────────────────── 생성기 산술 (SE–SE 동종 쌍 · 정적 · 점착 지배 · 고립 접촉 — 생성기 주석의 한정어) ─────────────────────────

def se_ced(bo, E_se, rho_se, d_se):
    return m.ced_for_bond(bo, d_se / 2.0, NU_SE, rho_se, E=E_se)


def se_overlap_pct(bo, E_se, rho_se, d_se):
    return m.overlap_for_ced(se_ced(bo, E_se, rho_se, d_se), d_se / 2.0, NU_SE, E=E_se) * 100.0


def v_stick_mm_s(bo, E_se, rho_se, d_se):
    """SE–SE 붙는 충돌 속도 상한 — 생성기 셀프테스트 U⑤ 의 식 (W = (1/5)π·CED·R*·δ_eq² · KE ≤ W(1−e²)/e²)."""
    ced = se_ced(bo, E_se, rho_se, d_se)
    r = d_se / 2.0
    es = E_se / (2.0 * (1.0 - NU_SE ** 2))
    rs = r / 2.0
    W = 0.2 * math.pi * ced * rs * (2.0 * math.pi * rs * ced / ((4.0 / 3.0) * es * math.sqrt(rs))) ** 4
    mstar = (4.0 / 3.0) * math.pi * r ** 3 * rho_se * 1000.0 / 2.0
    return math.sqrt(2.0 * W * (1.0 - m.COR ** 2) / (m.COR ** 2 * mstar)) * 1e3


def bo_at_ceiling(E_se, rho_se, d_se, ceil_pct=1.0):
    lo, hi = 1.0, 1e8
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if se_overlap_pct(mid, E_se, rho_se, d_se) > ceil_pct:
            hi = mid
        else:
            lo = mid
    return lo


def gen_numbers(gen, stiffen=1.0, cgf=CGF, n_total=N_TOTAL):
    p = m.plan(n_total, cgf=cgf, stiffen_se=stiffen, dens_gen=gen)
    rho_se, d_se, E_se = p['dens']['SE'], p['d']['SE'], p['E']['SE']
    rpm = m.rpm_for_fr(m.FR_ANCHOR, p['R'])
    wR = 2.0 * math.pi * rpm / 60.0 * p['R'] * 1e3
    vdrum = math.pi * p['R'] ** 2 * p['L']
    vpar = math.pi / 6.0 * d_se ** 3
    return dict(p=p, rho_se=rho_se, d_se=d_se, E_se=E_se, rpm=rpm, wR=wR, vdrum=vdrum, vpar=vpar,
                D_mm=2 * p['R'] * 1e3, L_mm=p['L'] * 1e3, dt=p['dt'], dt_by=p['dt_by'],
                se_vol=p['phi']['SE'] * 100, se_num=p['n']['SE'] / sum(p['n'].values()) * 100,
                n_per_fill=vdrum * 0.6 / vpar, amp_mm=p['d']['AM_P'] * 1e3,
                d_over_amp=2 * p['R'] / p['d']['AM_P'], d_over_se=2 * p['R'] / d_se,
                ceil=bo_at_ceiling(E_se, rho_se, d_se))


# ───────────────────────── 통계 (Student t — 정규화 불완전 베타 · 연분수) ─────────────────────────

def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for k in range(1, 400):
        k2 = 2 * k
        aa = k * (b - k) * x / ((qam + k2) * (a + k2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c
        c = c if abs(c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + k) * (qab + k) * x / ((a + k2) * (qap + k2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c
        c = c if abs(c) > 1e-300 else 1e-300
        de = d * c
        h *= de
        if abs(de - 1.0) < 3e-16:
            break
    return h


def _betainc(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_cdf(t, nu):
    p = 0.5 * _betainc(nu / 2.0, 0.5, nu / (nu + t * t))
    return 1.0 - p if t > 0 else p


@functools.lru_cache(maxsize=None)
def t975(nu):
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, nu) < 0.975:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def sd(v):
    mu = sum(v) / len(v)
    return math.sqrt(sum((a - mu) ** 2 for a in v) / (len(v) - 1))


# ───────────────────────── 곡선 역함수 공용 (x = log10 Bo) ─────────────────────────

def seg_within(xa, xb, ia, ib, mm, band):
    """칸 [xa, xb] 의 직선 보간 L 에서 |L − m| ≤ band 인 부분 구간 (없으면 None)."""
    if ib == ia:
        return (xa, xb) if abs(ia - mm) <= band else None
    t1, t2 = (mm - band - ia) / (ib - ia), (mm + band - ia) / (ib - ia)
    lo, hi = max(0.0, min(t1, t2)), min(1.0, max(t1, t2))
    if lo > hi:
        return None
    return (xa + lo * (xb - xa), xa + hi * (xb - xa))


def merge(segs, tol=1e-12):
    out = []
    for a, b in sorted(segs):
        if out and a <= out[-1][1] + tol:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def intersect(A, B):
    out = []
    for a0, a1 in A:
        for b0, b1 in B:
            lo, hi = max(a0, b0), min(a1, b1)
            if lo <= hi:
                out.append((lo, hi))
    return merge(out)


def inside(xv, comps):
    return any(a - 1e-12 <= xv <= b + 1e-12 for a, b in comps)


def side_of(xs, I, mm):
    """측정이 곡선 값 범위 밖이면 어느 Bo 끝 쪽인가 (가까운 끝값)."""
    return 'low_bo' if abs(mm - I[0]) <= abs(mm - I[-1]) else 'high_bo'


# ───────────────────────── v1 규칙 (설계 v1 문장 그대로 · `…_design_20261015.md`) ─────────────────────────

class RulesV1:
    name = 'v1'

    # §3-7 받아들일 범위 — "격자 평균 · 시드 SD → log10 Bo 에서 구간 선형 보간" · 띠 2√(u_exp² + u_DEM(Bo)²)
    #   u_DEM(Bo) 도 같은 직선 보간 (칸 끝 값이 같으면 정확히 풀고 · 다르면 칸마다 101 점으로 푼다)
    def accept(self, xs, I, u, mm, u_exp, **kw):
        segs = []
        for k in range(len(xs) - 1):
            if u[k] is None or u[k + 1] is None:
                return None                                   # u_DEM 정의 없음 = 구간을 못 낸다
            if u[k] == u[k + 1]:
                s = seg_within(xs[k], xs[k + 1], I[k], I[k + 1], mm, 2.0 * math.sqrt(u_exp ** 2 + u[k] ** 2))
                if s:
                    segs.append(s)
                continue
            run = None
            for j in range(101):
                t = j / 100.0
                xv = xs[k] + t * (xs[k + 1] - xs[k])
                L = I[k] + t * (I[k + 1] - I[k])
                uu = u[k] + t * (u[k + 1] - u[k])
                if abs(L - mm) <= 2.0 * math.sqrt(u_exp ** 2 + uu ** 2):
                    run = (xv, xv) if run is None else (run[0], xv)
                elif run is not None:
                    segs.append(run)
                    run = None
            if run is not None:
                segs.append(run)
        return dict(comps=merge(segs, tol=1e-9), side=None)

    # §3-7 Bo_SE* = (T1 구간 ∩ T2 구간) 의 기하 중심 · F5 = 안 겹침 (다른 분류 없음)
    def anchor(self, A1, A2):
        if not A1['comps'] or not A2['comps']:
            return dict(status='F5')
        C = intersect(A1['comps'], A2['comps'])
        if not C:
            return dict(status='F5')
        return dict(status='anchor', x=0.5 * (C[0][0] + C[-1][1]), comps=C)

    # §3-4 B — 교집합이 비면 기각 · 비지 않으면 통과 (검출력 개념 없음)
    def b_check(self, x1, w1, x2, w2, ratios, tol):
        nonempty = abs(x1 - x2) <= w1 + w2
        return dict(status='통과' if nonempty else 'F5', certifies_friction=nonempty)

    # §3-3 · §3-7 u_DEM = 그 수준의 시드 SD (시드 2 개 이상일 때만)
    def u_dem(self, seeds_by_level):
        return [sd(v) if len(v) >= 2 else None for v in seeds_by_level], 'per-level'

    def band_multiplier(self, nu):
        return 2.0

    def interp_error(self, dI):
        return 0.0

    # §3-2 T2 정상 상태 = 두 평균 창의 각이 u_DEM 안
    def steady(self, w1, w2, u_dem):
        return None if u_dem is None else abs(sum(w1) / len(w1) - sum(w2) / len(w2)) <= u_dem

    # NP 규칙 없음
    def run_np_ok(self, run_np, curve_np):
        return True

    # §3-2 벽 감도 = T2 를 γ_W/γ_SE 0.0256 × {0.31, 1}
    def wall_sensitivity(self):
        g = m.GM_WALL_HARE2026
        return dict(gammas=(g * 0.31, g * 1.0), tests={'T2'})

    # §3-2 T2 읽는 양 = 가운데 현의 직선 맞춤 (정의 가능성 기준 없음)
    def t2_angle(self, xs_pts, ys_pts, d, wrap_frac):
        ang, rms = line_fit(xs_pts, ys_pts)
        return dict(status='각', angle=ang)

    # §3-8 Bo_SE* 를 새 확인 블록 등록 (S6) 에 '값으로'
    def transfer(self):
        return dict(value='center', interval=False, G=None, convention=None)

    # §3-8 순서 (C0 → S3 등록 → C1 봉인 → 원자료 열람) · 실측 병행 허용 (봉인 전에 원자료를 열지 않으면) · 원자료 규칙 없음
    def order_ok(self, seq):
        idx = {e: i for i, e in enumerate(seq)}
        need = ('C0_end', 'S3_commit', 'curve_seal', 'raw_open')
        if any(e not in idx for e in need):
            return False
        return idx['C0_end'] < idx['S3_commit'] < idx['curve_seal'] < idx['raw_open']

    # §3-7 검증 = T3 예측 (Bo* 한 점) · 통과선 2u (이진이면 일치)
    def validation(self, preds, i_lo, i_hi, measured):
        c = (i_lo + i_hi) // 2
        return dict(status='통과' if preds[c] == measured else '실패', discriminating=None)

    # §3-3 · F7 계약 밖 (> 1 %) 만 뺀다
    def include_run(self, run, supported):
        return not (run['overlap'] is not None and run['overlap'] > 1.0)

    # §3-1 ① 시험 덱 = SE 만 · 드럼 = 믹서 드럼 STL 그대로 (= plan() 의 R)
    def test_deck(self):
        return dict(phases=('SE',), drum='plan')

    # §3-7 F3 = 한 번 확장 (×√10 · 위로는 천장까지) → 그래도 끝 = '표현 범위 밖'
    def f3(self, xs, I, f, mm, band, ceiling):
        if mm > max(I) + band:
            return dict(status='확장', level=GRID[-1] * math.sqrt(10.0))
        if mm < min(I) - band:
            lo = xs[0] - 0.5
            if abs(f(lo) - mm) <= band:
                return dict(status='확장', level=10 ** lo)
            return dict(status='표현 범위 밖', level=10 ** lo)
        return dict(status='안')

    # §2-0 · §2-3 u_exp = √(SD²/n + u_판독²) · ≥ 5 회 + 다른 날 1 회 (자료 = 날별 목록)
    def u_exp_band(self, days, u_read):
        v = [a for dd in days for a in dd]
        mm = sum(v) / len(v)
        return mm, 2.0 * math.sqrt(sd(v) ** 2 / len(v) + u_read ** 2)

    def exp_plan(self):
        return [5, 1]                                          # 날별 반복 수

    # §2-4 비코팅 NCM → 유동성 등가 ρ_flow (D4 · AFM 교차)
    def rho_flow(self, bo_aa_at_thesis_edge, bo_id):
        return '교차 값'

    # 결과 전 정의 (v1 에 적힌 것)
    def definitions(self):
        return dict(t2_primary=None, f1_pair=None, tap_match=None, ext_seeds=None,
                    raw_custody=None, policy_stage=None, f8_rule='파이프라인 G11 · D13 참조만')

    def doc_numbers(self):
        return DESIGN_V1_NUMBERS


#: 설계 v1 에 적힌 숫자 (그 문서의 표기 그대로 — 자릿수 = 그 표기의 반올림 단위) · 출처 세대 = gen1
DESIGN_V1_NUMBERS = {
    'drum_D_mm': '26.28', 'drum_L_mm': '5.26', 'rpm': '75', 'wR_mm_s': '103',
    'n_per_fill': '9.4e5', 'n_f011': '1.0e5', 'n_f030': '2.8e5', 'n_slice': '1.1e5',
    'dt_x20': '2.62e-7', 'ceiling_soft': '8.3e2', 'ov_637_soft': '0.837', 'ov_850_soft': '1.014',
    'ov_637_x20': '0.114', 'bo_1pct_x20': '1.7e4', 'vstick_0212_x20': '0.059', 'vstick_212_x20': '18.7',
    'vstick_637_x20': '46.6', 'vstick_ceil_x20': '58', 'vstick_ceil_over_wR': '0.6',
    'se_vol_pct': '35', 'se_num_pct': '99', 'd_over_amp': '19',
}


def line_fit(xs_pts, ys_pts):
    n = len(xs_pts)
    mx, my = sum(xs_pts) / n, sum(ys_pts) / n
    sxx = sum((a - mx) ** 2 for a in xs_pts)
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs_pts, ys_pts))
    k = sxy / sxx
    res = [b - (my + k * (a - mx)) for a, b in zip(xs_pts, ys_pts)]
    return math.degrees(math.atan(k)), math.sqrt(sum(r * r for r in res) / n)


EXT_FACTOR = 0.95                     # v2 R13 위쪽 확장 수준 = 세대 천장 × 0.95 (⬜ Qv2-8)
G_THINKY = 268.0                      # mixing_model_design §18-1 Thinky 표 (실험 혼합기 미확인 · MXD3-19)
T2_SIM_S = 1.6                        # T2 한 런 모사 시간 [추정 · v1 §3-2 그대로] = 정착 + 0.5 바퀴 버림 + 1.5 바퀴 측정
THRU = (70.0, 63.0)                   # step/s (10 만 parcel · NP 20 · dev-bo 실측 — v1 §3-2)
SLOTS = 3                             # ibb QOS 60 CPU = NP 20 세 슬롯


@functools.lru_cache(maxsize=None)
def computed_numbers(gen):
    g1, g20, g200 =gen_numbers(gen, 1.0), gen_numbers(gen, 20.0), gen_numbers(gen, 1.0, cgf=200.0)
    r20 = (g20['E_se'], g20['rho_se'], g20['d_se'])
    r1 = (g1['E_se'], g1['rho_se'], g1['d_se'])
    r200 = (g200['E_se'], g200['rho_se'], g200['d_se'])
    v_ceil = v_stick_mm_s(g1['ceil'], *r20)
    p = g1['p']
    dn, d = p['dens'], p['d']
    w = {k: math.pi / 6.0 * d[k] ** 3 * dn[m.PHASE_MECH[k][1]] for k in d}
    fac = {k: (d[k] / d['SE']) * (w['SE'] / w[k]) for k in ('AM_P', 'AM_S')}
    ext = EXT_FACTOR * g1['ceil']
    steps = 1.0 / g20['dt']
    rho_mix = 100.0 / sum(p['wt'][k] / p['dens'][m.PHASE_MECH[k][1]] for k in p['wt'])
    th, lo, hi = 0.0, 0.0, 2.0 * math.pi
    for _ in range(200):
        th = 0.5 * (lo + hi)
        if (th - math.sin(th)) / (2.0 * math.pi) > 0.30:
            hi = th
        else:
            lo = th
    depth = 1.0 - math.cos(lo / 2.0)
    vol_cm3 = g1['vdrum'] * 1e6
    out = {
        'drum_D_mm': g1['D_mm'], 'drum_L_mm': g1['L_mm'], 'rpm': g1['rpm'], 'wR_mm_s': g1['wR'],
        'n_per_fill': g1['n_per_fill'], 'n_f011': 0.11 * g1['n_per_fill'], 'n_f030': 0.30 * g1['n_per_fill'],
        'n_slice': 0.30 * math.pi * g1['p']['R'] ** 2 * 2e-3 * 0.6 / g1['vpar'],
        'dt_x20': g20['dt'], 'ceiling_soft': g1['ceil'], 'ov_637_soft': se_overlap_pct(GRID[-1], *r1),
        'ov_850_soft': se_overlap_pct(4000.0 * m.BO_BASE, *r1), 'ov_637_x20': se_overlap_pct(GRID[-1], *r20),
        'bo_1pct_x20': g20['ceil'], 'vstick_0212_x20': v_stick_mm_s(GRID[0], *r20),
        'vstick_212_x20': v_stick_mm_s(GRID[6], *r20), 'vstick_637_x20': v_stick_mm_s(GRID[7], *r20),
        'vstick_ceil_x20': v_ceil, 'vstick_ceil_over_wR': v_ceil / g20['wR'],
        'se_vol_pct': g1['se_vol'], 'se_num_pct': g1['se_num'], 'd_over_amp': g1['d_over_amp'],
        # ── 아래는 v2 문서에만 나오는 숫자 (v1 대조 없음) ──
        'd_over_se': g1['d_over_se'], 'real_d_over_se': g1['D_mm'] * 1e3 / m.D_REAL_UM['SE'],
        'vstick_0212_soft': v_stick_mm_s(GRID[0], *r1),
        'vstick_21_x20': v_stick_mm_s(GRID[4], *r20),
        'vstick_21_g': v_stick_mm_s(GRID[4] / G_THINKY, *r20), 'vstick_212_g': v_stick_mm_s(GRID[6] / G_THINKY, *r20),
        'vstick_637_g': v_stick_mm_s(GRID[7] / G_THINKY, *r20), 'vstick_637_g_over_wR': v_stick_mm_s(GRID[7] / G_THINKY, *r20) / g20['wR'],
        'ext_level': ext, 'ov_ext_soft': se_overlap_pct(ext, *r1), 'ext_ratio': ext / GRID[-1],
        'ceil_ratio': g1['ceil'] / GRID[-1], 'ov_1010_soft': se_overlap_pct(1010.0, *r1), 'ov_1020_soft': se_overlap_pct(1020.0, *r1),
        'ceiling_cgf200': g200['ceil'], 'ov_637_cgf200': se_overlap_pct(GRID[-1], *r200),
        'bo_aa_ratio_amp': 1.0 / fac['AM_P'], 'bo_aa_ratio_ams': 1.0 / fac['AM_S'],
        'boaa_amp_21_031': GRID[4] * 0.31 * fac['AM_P'], 'boaa_ams_21_031': GRID[4] * 0.31 * fac['AM_S'],
        'boaa_amp_21_1': GRID[4] * fac['AM_P'], 'boaa_ams_21_1': GRID[4] * fac['AM_S'],
        'boaa_amp_637_031': GRID[7] * 0.31 * fac['AM_P'], 'boaa_ams_637_031': GRID[7] * 0.31 * fac['AM_S'],
        'boaa_amp_ceil_031': g1['ceil'] * 0.31 * fac['AM_P'], 'boaa_ams_ceil_031': g1['ceil'] * 0.31 * fac['AM_S'],
        'steps_1s_x20': steps, 'h_1s_lo': steps / THRU[0] / 3600.0, 'h_1s_hi': steps / THRU[1] / 3600.0,
        't2_run_d_lo': T2_SIM_S * steps / THRU[0] / 86400.0, 't2_run_d_hi': T2_SIM_S * steps / THRU[1] / 86400.0,
        't5_pa': 0.6 * rho_mix * 1e3 * 9.81 * depth * p['R'], 'rho_mix': rho_mix, 'depth_over_R': depth,
        't2_cell_cm3': vol_cm3, 't2_mass_lo_g': 0.11 * vol_cm3 * 0.5, 't2_mass_hi_g': 0.30 * vol_cm3 * 0.9,
        'rpm_r13': m.rpm_for_fr(m.FR_ANCHOR, 0.013),
        't975_2': t975(2), 't975_4': t975(4), 't975_8': t975(8),
        'ext_low': GRID[0] / math.sqrt(10.0), 'per_decade_vstick': 10.0 ** (5.0 / 6.0),
    }
    # 계산 예산 [추정] — T2 = 위 식 · T1 · C2 런 = v1 §3-6 의 [추정] 값 × (이 세대 ×20 step/s ÷ gen1 ×20 step/s)
    sc = steps / (1.0 / gen_numbers(GEN1, 20.0)['dt'])
    t2 = (out['t2_run_d_lo'], out['t2_run_d_hi'])
    t1s, t1p, t1t, c2r = (0.2 * sc, 1.0 * sc), (0.1 * sc, 0.7 * sc), (0.5 * sc, 4.0 * sc), (0.5 * sc, 1.5 * sc)
    out.update({
        'dt_scale': sc, 't1_short_lo': t1s[0], 't1_short_hi': t1s[1], 't1_pour_lo': t1p[0], 't1_pour_hi': t1p[1],
        't1_tap_lo': t1t[0], 't1_tap_hi': t1t[1], 'c2_run_lo': c2r[0], 'c2_run_hi': c2r[1],
        'c0_lo': (9 * t2[0] + 6 * t1s[0]) / SLOTS, 'c0_hi': (9 * t2[1] + 6 * t1s[1]) / SLOTS,
        'c1_lo': (12 * t2[0] + 8 * t1t[0] + 4 * t1p[0]) / SLOTS, 'c1_hi': (12 * t2[1] + 8 * t1t[1] + 4 * t1p[1]) / SLOTS,
        # C2 (R09) = T3 (구간 안 1–3 수준 + 바깥 이웃 2 = 3–5 수준) × 2 시드 + T3 벽 끝 1 = 7–11 런
        #           + T2 다른 두 속도 × (3–5 수준) × 1 시드 = 6–10 T2 런 (v1 Q2 의 검증 둘 다 · v1 §3-6 은 T3 만 셌다)
        'c2_t3_runs_lo': 7, 'c2_t3_runs_hi': 11, 'c2_t2_runs_lo': 6, 'c2_t2_runs_hi': 10,
        'c2_lo': (7 * c2r[0] + 6 * t2[0]) / SLOTS, 'c2_hi': (11 * c2r[1] + 10 * t2[1]) / SLOTS,
    })
    out['sum_lo'] = out['c0_lo'] + out['c1_lo'] + out['c2_lo']
    out['sum_hi'] = out['c0_hi'] + out['c1_hi'] + out['c2_hi']
    return out


def matches(typed, val):
    """표기 (문자열) 의 반올림 단위 안에서 계산값과 같은가."""
    s = typed.lower()
    if 'e' in s:
        mant, ex = s.split('e')
        dec = len(mant.split('.')[1]) if '.' in mant else 0
        unit = 10 ** (int(ex) - dec)
    else:
        dec = len(s.split('.')[1]) if '.' in s else 0
        unit = 10 ** (-dec)
    return abs(float(typed) - val) <= 0.5 * unit * (1 + 1e-9)


# ───────────────────────── 검사 (C01 – C17) ─────────────────────────

def c01(R):
    """MXD3-01 — 교집합 검사 B 의 검출력 ([가정 예시] 선형화 I_k = a_k·x + b_k·μ_r)."""
    tol = 0.5 * m.MU_R                                         # 덱 μ_r ±50 % (C0 감도 범위)
    # 반례: b/a 같음 (8 decade/단위 μ_r) · 덱 μ_r 이 0.2 틀림 → 두 앵커가 같이 1.6 decade 비낀다
    a1 = a2 = 5.0
    b1 = b2 = 40.0
    w1 = w2 = 2 * 1.5 / 5.0
    dmu, xt = 0.2, 1.0
    x1, x2 = xt - b1 / a1 * dmu, xt - b2 / a2 * dmu
    r = R.b_check(x1, w1, x2, w2, (b1 / a1, b2 / a2), tol)
    caught = not r['certifies_friction']                       # 마찰 세트를 확인했다고 말하지 않아야 잡은 것
    # 대조: b/a 40 ↔ 0 (T2 각 a 5 °/decade · b 200 · T1 HR a 0.05 /decade · b 0 · u 0.015) · 덱 μ_r 이 맞음
    a1c, b1c, a2c, b2c = 5.0, 200.0, 0.05, 0.0
    w1c, w2c = 2 * 1.5 / a1c, 2 * 0.015 / a2c
    rc = R.b_check(xt, w1c, xt, w2c, (b1c / a1c, b2c / a2c), tol)
    rc2 = R.b_check(xt - b1c / a1c * 0.075, w1c, xt, w2c, (b1c / a1c, b2c / a2c), tol)
    ok = rc['status'] == '통과' and rc['certifies_friction'] and rc2['status'] == 'F5'
    return caught, ok, (f'반례 (b/a 같음 · Δμ_r 0.2): {r["status"]} · 마찰 확인 주장 {r["certifies_friction"]} · '
                        f'앵커 오차 {abs(x1 - xt):.2f} decade | 대조 (b/a 40 ↔ 0): Δμ_r 0 → {rc["status"]}'
                        f'{" · " + rc.get("note", "") if rc.get("note") else ""} · Δμ_r 0.075 → {rc2["status"]}')


def c02(R):
    """MXD3-02 — 반 decade 칸 안의 가파른 전이 ([가정 예시] jarray2019 꼴 35.0 → 48.9° · 폭 0.1 decade · u 1.5°)."""
    D_ANG, U, WID = 13.9, 1.5, 0.1
    s = WID / (2.0 * math.log(9.0))
    xs0 = X[:7]
    res = {}
    for refine in (False, True):
        tot = miss = 0
        widths = []
        for i in range(200):
            xstar = xs0[2] + 0.5 * (i + 0.5) / 200.0

            def f(x, xstar=xstar):
                return 35.0 + D_ANG / (1.0 + math.exp(-(x - xstar) / s))
            xs = R.refine(xs0, f, 2.0 * U) if (refine and hasattr(R, 'refine')) else list(xs0)
            gv = [f(x) for x in xs]
            for j in range(41):
                xt = xstar - 0.1 + 0.2 * j / 40.0
                mm = f(xt)
                if not (35.0 + 2 * U < mm < 35.0 + D_ANG - 2 * U):
                    continue                                   # 가파른 부분만 (v1 증거 [8] 과 같은 부분집합)
                A = R.accept(xs, gv, [U] * len(xs), mm, 0.0, nu=None)     # ν None = σ 를 안다고 보는 경우 (배수 2 · 증거 [8] 과 같은 띠)
                comps = A['comps'] if A else []
                if not comps:
                    continue
                tot += 1
                if R.name == 'v1':                             # v1 = 감싸는 구간 하나 (증거 [8] 그대로)
                    comps = [(comps[0][0], comps[-1][1])]
                widths.append(sum(b - a for a, b in comps))
                if not inside(xt, comps):
                    miss += 1
        res[refine] = (tot, miss, sorted(widths)[len(widths) // 2] if widths else float('nan'))
    tot, miss, wmed = res[False]
    # 대조: 완만한 직선 (40 + 5x) · 측정 = 참값 (잡음 0) — 포괄 100 % · 구간 폭이 격자 폭보다 좁아야 (전부 받아들이지 않음)
    cov = 0
    ws = []
    for j in range(101):
        xt = X[1] + (X[5] - X[1]) * j / 100.0
        gv = [40.0 + 5.0 * x for x in X[:7]]
        A = R.accept(X[:7], gv, [U] * 7, 40.0 + 5.0 * xt, 0.0, nu=None)
        comps = A['comps']
        if R.name == 'v1':
            comps = [(comps[0][0], comps[-1][1])]
        cov += inside(xt, comps)
        ws.append(sum(b - a for a, b in comps))
    wc = sorted(ws)[50]
    caught = miss == 0
    ok = cov == 101 and wc < (X[6] - X[0])
    t2, m2, w2 = res[True]
    return caught, ok, (f'반례: 가파른 부분 {tot} 건 중 참값이 구간 밖 {miss} ({miss / max(tot, 1) * 100:.1f} %) · 폭 중앙 {wmed:.3f} decade'
                        + (f' | 세분 (봉인 전) {t2} 건 중 {m2} · 폭 중앙 {w2:.3f} decade' if hasattr(R, 'refine') else '')
                        + f' | 대조 (완만 직선 5 °/decade): 포괄 {cov}/101 · 폭 중앙 {wc:.3f} decade (격자 폭 {X[6] - X[0]:.2f})')


def c03(R):
    """MXD3-03 — 끊긴 받아들일 집합 · 한 시험이 빈 집합."""
    S = [(lx(GRID[1]), lx(GRID[2])), (lx(GRID[5]), lx(GRID[6]))]
    full = [(X[0], X[-1])]
    r1 = R.anchor(dict(comps=S, side=None), dict(comps=full, side=None))
    bad1 = r1['status'] == 'anchor' and not inside(r1['x'], S)
    r2 = R.anchor(dict(comps=[], side='low_bo'), dict(comps=full, side=None))
    bad2 = r2['status'] == 'F5'                                # 두 시험 '불일치' 가 아니라 T1 표현 밖인데 F5 로 읽음
    Cc = R.anchor(dict(comps=[(0.0, lx(30.0))], side=None), dict(comps=[(lx(5.0), 2.0)], side=None))
    ok = Cc['status'] == 'anchor' and lx(5.0) <= Cc['x'] <= lx(30.0)
    caught = not bad1 and not bad2
    t1 = f'끊긴 집합 → {r1["status"]}'
    if r1['status'] == 'anchor':
        t1 += f' Bo {10 ** r1["x"]:.2f} (집합 안? {inside(r1["x"], S)})'
    t2 = f'T1 빈 집합 (측정이 낮은 Bo 끝 너머) → {r2["status"]}' + (f' ({r2["side"]})' if r2.get('side') else '')
    t3 = f'대조 [1, 30] ∩ [5, 100] → {Cc["status"]}' + (f' Bo {10 ** Cc["x"]:.2f}' if Cc['status'] == 'anchor' else '')
    return caught, ok, f'{t1} | {t2} | {t3}'


def c04(R):
    """MXD3-04 — u_DEM (시드 수 · 자유도) · T2 정상 상태 · NP."""
    rng = random.Random(20261021)
    # (a) 최소안 T1 = 모든 수준 시드 1 개 → u_DEM 이 정의되는가 (정의 안 되면 그 시험을 판정 밖으로 두는 규칙이 있는가)
    seeds_t1 = [[40.0] for _ in range(8)]
    u1, how1 = R.u_dem(seeds_t1)
    a_ok = all(v is not None for v in u1) or how1 == '판정 밖 (보조)'
    # (b) 포괄 (몬테카를로) — 참 곡선 40 + 5x · 8 수준 모두 시드 2 개 · σ_seed 1.5° · u_exp 0.3° · 참 x 는 x1–x6 균등
    sig, uexp, trials = 1.5, 0.3, 4000
    cov = cov_stat = 0
    for _ in range(trials):
        seeds = [[40.0 + 5.0 * x + rng.gauss(0, sig) for _ in range(2)] for x in X]
        u, how = R.u_dem(seeds)
        I = [sum(v) / len(v) for v in seeds]
        xt = X[1] + (X[6] - X[1]) * rng.random()
        mm = 40.0 + 5.0 * xt + rng.gauss(0, uexp)
        A = R.accept(X, I, u, mm, uexp, nu=8)
        cov += A is not None and inside(xt, A['comps'])
        if hasattr(R, 'accept_stat_only'):
            B = R.accept_stat_only(X, I, u, mm, uexp, nu=8)
            cov_stat += inside(xt, B['comps'])
    b_ok = cov / trials >= 0.95
    # (c) NP — 곡선 NP 20 · 재시도 NP 10
    c_ok = not R.run_np_ok(10, 20) and R.run_np_ok(20, 20)
    # (d) T2 정상 상태 — 시드 1 개 수준 (u_DEM 없음) · 두 창 (블록 4 개씩) 평균이 3° 차이 / 차이 0.05° (블록 값 고정)
    w1 = [40.6, 39.5, 40.3, 39.6]
    w2 = [43.4, 42.6, 43.3, 42.7]
    w3 = [40.4, 39.7, 40.5, 39.6]
    s_drift, s_flat = R.steady(w1, w2, None), R.steady(w1, w3, None)
    d_ok = s_drift is False and s_flat is True
    caught = a_ok and b_ok and c_ok and d_ok
    detail = (f'(a) 최소안 T1 u_DEM = {"정의" if all(v is not None for v in u1) else "없음"} ({how1}) · '
              f'(b) 포괄 {cov / trials:.3f}' + (f' (통계 띠만 {cov_stat / trials:.3f})' if hasattr(R, 'accept_stat_only') else '')
              + f' (목표 ≥ 0.95) · (c) NP 10 재시도 받음? {R.run_np_ok(10, 20)} · (d) 정상 상태 (3° 표류 / 표류 0) = {s_drift} / {s_flat}')
    return caught, True, detail


def c05(R):
    """MXD3-05 — 벽 감도가 ρ 구간 · 벽이 닿는 시험을 덮는가 (F_SW/F_SS = 2√(γ_W/γ_SE))."""
    ws = R.wall_sensitivity()
    lo, hi = (2.0 * math.sqrt(g) for g in ws['gammas'])
    need = {rho: 2.0 * math.sqrt(m.GM_WALL_HARE2026 * rho) for rho in (0.0, 0.01, 0.03, 0.1, 0.31, 1.0)}
    unc = [rho for rho, F in need.items() if not (lo - 1e-12 <= F <= hi + 1e-12)]
    tests_wall = {'T1', 'T2', 'T3'}
    miss_t = sorted(tests_wall - set(ws['tests']))
    caught = not unc and not miss_t
    return caught, True, (f'감도 비 범위 [{lo:.3f}, {hi:.3f}] · 덮지 못하는 ρ = {unc or "없음"} · 감도가 빠진 시험 = {miss_t or "없음"}')


def c06(R):
    """MXD3-06 — T2 자유표면 각의 정의 가능성 (합성 표면 · 단위 = 드럼 R · d = SE parcel / R (lab))."""
    rng = random.Random(6)
    g = gen_numbers(LAB)
    d = g['d_se'] / g['p']['R']
    xs_pts = [-0.4 + 0.8 * i / 40 for i in range(41)]
    ys_ok = [math.tan(math.radians(40.0)) * x - 0.2 + rng.gauss(0, 0.3 * d) for x in xs_pts]
    ys_wrap = [math.sqrt(1.0 - x * x) - d + rng.gauss(0, 0.3 * d) for x in xs_pts]
    r_ok = R.t2_angle(xs_pts, ys_ok, d, 0.0)
    r_wrap = R.t2_angle(xs_pts, ys_wrap, d, 0.30)
    caught = r_wrap['status'] != '각'
    ok = r_ok['status'] == '각' and abs(r_ok['angle'] - 40.0) < 0.5
    _, rms_w = line_fit(xs_pts, ys_wrap)
    _, rms_o = line_fit(xs_pts, ys_ok)
    return caught, ok, (f'벽 두름 표면 → {r_wrap["status"]}' + (f' {r_wrap["angle"]:.1f}°' if r_wrap['status'] == '각' else '')
                        + f' (맞춤 잔차 {rms_w / d:.2f} d · 두름 분율 0.30) | 대조 정상 침대 → {r_ok["status"]} '
                        + (f'{r_ok["angle"]:.2f}° (잔차 {rms_o / d:.2f} d)' if r_ok['status'] == '각' else ''))


def c07(R):
    """MXD3-07 — 확인 블록 이전 명세 (G · 규약 · 구간)."""
    t = R.transfer()
    caught = bool(t['interval']) and t['G'] is not None and t['convention'] is not None
    return caught, True, f'이전 명세 = {t}'


def c08(R):
    """MXD3-08 — 등록 · 측정 · 봉인 · 열람 순서 (사건 순서 모형)."""
    # 사건 이름 — v1 = S3_commit (등록 하나 · SOP 포함) · v2 = S3a_commit (규칙 · SOP) + S3b_commit (C0 뒤 확정값) — 두 판이 다
    #   읽도록 순서열마다 두 이름을 함께 둔다 (S3_commit = S3b 와 같은 자리).
    X1 = ['C0_start', 'measure_start', 'measure_end', 'raw_push_enc', 'C0_end', 'S3a_commit', 'S3_commit',
          'S3b_commit', 'curve_seal', 'key_commit', 'raw_open']           # 측정이 SOP 커밋보다 먼저 (그 밖은 다 지킴)
    X2 = ['S3a_commit', 'C0_start', 'C0_end', 'S3_commit', 'S3b_commit', 'measure_start', 'measure_end',
          'raw_push_enc', 'raw_push_plain', 'curve_seal', 'key_commit', 'raw_open']   # 원자료 평문 push 가 곡선 봉인보다 먼저
    Y = ['S3a_commit', 'C0_start', 'measure_start', 'measure_end', 'raw_push_enc', 'C0_end', 'S3_commit',
         'S3b_commit', 'curve_seal', 'key_commit', 'raw_open']
    a, b, c = R.order_ok(X1), R.order_ok(X2), R.order_ok(Y)
    caught = (not a) and (not b)
    return caught, c, (f'측정이 SOP 커밋보다 먼저 (X1) → 받음? {a} · 원자료 평문 push 가 곡선 봉인보다 먼저 (X2) → 받음? {b}'
                       f' | 대조 (S3a → 측정 → 암호화 push → S3b · 봉인 → 열쇠 → 열람) → 받음? {c}')


def c09(R):
    """MXD3-09 — T3 검증의 판별력 (이진 예측 · 8 수준)."""
    S, F = '멈춤', '흐름'
    p_nopow = [F] + [S] * 7
    r = R.validation(p_nopow, 3, 5, S)                         # 앵커 구간 = 6.718 – 67.18
    caught = r.get('discriminating') is False                  # '판별력 없음' 이라고 말해야 잡은 것 (v1 은 판별력을 묻지 않는다)
    p_pow = [F] * 5 + [S] * 3
    rc = R.validation(p_pow, 3, 4, F)                          # 앵커 구간 = 6.718 – 21.24 · 위 이웃 67.18 = 멈춤
    ok = rc['status'] == '통과' and rc.get('discriminating') is True
    return caught, ok, (f'판별력 없는 경우 (모든 이웃 = 멈춤) → {r["status"]} · 판별력 {r.get("discriminating")}'
                        f' | 대조 (위 이웃 = 멈춤) → {rc["status"]} · 판별력 {rc.get("discriminating")}')


def c10(R):
    """MXD3-10 — 계약 검사기 (실제 container_at) 가 지원하지 않는 기하의 런."""
    def supported(meshes):
        try:
            ccv.container_at('/nonexistent_run_dir', {'used': meshes, 'meshes': {}, 'moves': {}}, 0)
            return True
        except ValueError as e:
            return '지원하지 않는다' not in str(e)
        except Exception:                                      # noqa: BLE001 — 지원 메시는 STL 읽기에서 다른 예외 (검사 진입)
            return True
    runs = [dict(test='T2', meshes=['Drum', 'Front', 'Back'], overlap=0.4),
            dict(test='T1', meshes=['TapFloor'], overlap=None),
            dict(test='T3', meshes=['Funnel'], overlap=None)]
    inc = {r['test']: R.include_run(r, supported(r['meshes'])) for r in runs}
    caught = inc['T2'] and not inc['T1'] and not inc['T3']
    bad = dict(test='T2', meshes=['Drum', 'Front', 'Back'], overlap=1.3)
    ok = not R.include_run(bad, supported(bad['meshes']))
    sup = {r['test']: supported(r['meshes']) for r in runs}
    return caught, ok, f'검사기 지원 = {sup} · 앵커에 넣음 = {inc} | 대조 T2 겹침 1.3 % → 넣음? {R.include_run(bad, True)}'


def c11(R):
    """MXD3-11 — 시험 덱 물성 블록 · 드럼 치수의 출처 (실제 생성기)."""
    t = R.test_deck()
    try:
        m.set_phases(t['phases'])
        phases_ok = True
        why = '통과'
    except AssertionError as e:
        phases_ok, why = False, f'AssertionError: {e}'
    finally:
        m.set_phases(('AM_P', 'AM_S', 'SE'))
    Rs = {nt: m.plan(nt, cgf=CGF, dens_gen=LAB)['R'] * 1e3 for nt in (100000, 50000)}
    drum_fixed = t['drum'] != 'plan'
    caught = phases_ok and drum_fixed
    return caught, True, (f'상 집합 {t["phases"]} → {why} · 드럼 = {t["drum"]} (plan() R: N 10 만 {Rs[100000]:.3f} · 5 만 {Rs[50000]:.3f} mm)')


def c12(R):
    """MXD3-12 — 설계 문서 숫자 ↔ lab20261014 계산값 (표기 자릿수 안)."""
    lab, g1 = computed_numbers(LAB), computed_numbers(GEN1)
    doc = R.doc_numbers()
    bad = [k for k, v in doc.items() if not matches(v, lab[k])]
    lacking = sorted(set(DESIGN_V1_NUMBERS) - set(doc))           # 빈 표로 '통과' 하지 않게 — v1 숫자 자리를 전부 다시 적어야 한다
    bad += [f'{k} (없음)' for k in lacking]
    ctrl = [k for k, v in DESIGN_V1_NUMBERS.items() if not matches(v, g1[k])]
    caught = not bad
    ok = not ctrl                                              # 같은 비교가 v1 숫자를 gen1 계산값에는 받아들인다 (비교 장치 대조)
    return caught, ok, (f'lab 과 다른 문서 숫자 {len(bad)}/{len(doc)}' + (f' (예 {", ".join(bad[:6])})' if bad else '')
                        + f' | 대조: v1 숫자 ↔ gen1 계산값 어긋남 {len(ctrl)}/{len(DESIGN_V1_NUMBERS)}')


def c13(R):
    """MXD3-13 — F3 확장 (위 = 천장 · 아래 = 마찰 바닥)."""
    g = gen_numbers(LAB)
    ceil = g['ceil']
    up = R.f3(X, [35, 37, 40, 43, 46, 50, 55, 60], lambda x: 60.0, 64.0, 3.0, ceil)    # 위 끝이 아직 오르는 곡선 · 측정이 그 위
    up_ok = (up['status'] == '확장' and up['level'] is not None and up['level'] <= ceil
             and se_overlap_pct(up['level'], g['E_se'], g['rho_se'], g['d_se']) <= 1.0)
    flat = [35.0, 35.2, 36.0, 40.0, 44.0, 48.0, 50.0, 51.0]
    dn = R.f3(X, flat, lambda x: 35.0, 31.0, 3.0, ceil)
    dn_ok = dn['status'] == '마찰 바닥'
    steep = [35.0, 39.0, 42.0, 44.0, 46.0, 48.0, 50.0, 52.0]                # 바닥 칸 |ΔI| 4 > 띠 3 (평평하지 않음)
    dc = R.f3(X, steep, lambda x: 35.0 + 4.0 * (x - X[0]) / (X[1] - X[0]), 31.0, 3.0, ceil)
    ok = dc['status'] == '확장'
    caught = up_ok and dn_ok
    lev = up.get('level')
    return caught, ok, (f'위 확장 → {up["status"]}' + (f' 수준 {lev:.1f}' if lev is not None else '') + f' (천장 {ceil:.1f}) → 가능? {up_ok} · '
                        f'바닥 평평 + 측정이 아래 → {dn["status"]} | 대조 (바닥이 기울어짐) → {dc["status"]}')


def c14(R):
    """MXD3-14 — u_exp 의 날 성분 (몬테카를로 · [가정 예시] 날 안 SD 1° · 날 차 SD 3° · 판독 0.5°)."""
    rng = random.Random(14)
    res = {}
    for sday in (3.0, 0.0):
        cov = 0
        trials = 20000
        for _ in range(trials):
            r = rng.gauss(0, 0.5)
            days = []
            for n_rep in R.exp_plan():
                dd = rng.gauss(0, sday)
                days.append([r + dd + rng.gauss(0, 1.0) for _ in range(n_rep)])
            mm, band = R.u_exp_band(days, 0.5)
            cov += abs(mm) <= band
        res[sday] = cov / trials
    caught = res[3.0] >= 0.95
    ok = res[0.0] >= 0.95
    return caught, ok, f'날 계획 {R.exp_plan()} · 포괄 (날 차 3°) {res[3.0]:.3f} · (날 차 0) {res[0.0]:.3f} (목표 ≥ 0.95)'


def c15(R):
    """MXD3-15 — 선택 분말 ρ_flow 의 식별 (Bo_AA(ρ = 0.31) 가 격자 최소 Bo 아래면 값이 아니다)."""
    p = m.plan(N_TOTAL, cgf=CGF, dens_gen=LAB)
    dn, d = p['dens'], p['d']
    w = {k: math.pi / 6.0 * d[k] ** 3 * dn[m.PHASE_MECH[k][1]] for k in d}
    fac = {k: (d[k] / d['SE']) * (w['SE'] / w[k]) for k in ('AM_P', 'AM_S')}
    low = {k: 21.244 * 0.31 * fac[k] for k in fac}
    high = {k: 637.32 * 0.31 * fac[k] for k in fac}
    r_low = {k: R.rho_flow(low[k], m.BO_BASE) for k in fac}
    r_high = {k: R.rho_flow(high[k], m.BO_BASE) for k in fac}
    caught = all(v == '위쪽 한계만' for v in r_low.values())
    ok = all(v == '교차 가능' for v in r_high.values())
    return caught, ok, (f'Bo_SE* 21.24 · ρ 0.31 → Bo_AA {", ".join(f"{k} {v:.4f}" for k, v in low.items())} → {r_low}'
                        f' | 대조 Bo_SE* 637.3 → {", ".join(f"{k} {v:.3f}" for k, v in high.items())} → {r_high}')


def c17(R):
    """MXD3-17 — 결과 전에 정해야 할 정의가 다 있는가."""
    dfn = R.definitions()
    keys = set(RulesV1().definitions())                            # v1 이 비워 둔 자리 전부가 있어야 한다 (빈 dict 로 '통과' 방지)
    missing = sorted(k for k in keys if k not in dfn or dfn[k] is None or str(dfn[k]).endswith('참조만'))
    return not missing, True, f'빠진 정의 = {missing or "없음"}'


CHECKS = [('C01', c01), ('C02', c02), ('C03', c03), ('C04', c04), ('C05', c05), ('C06', c06), ('C07', c07),
          ('C08', c08), ('C09', c09), ('C10', c10), ('C11', c11), ('C12', c12), ('C13', c13), ('C14', c14),
          ('C15', c15), ('C17', c17)]


# ───────────────────────── v2 규칙 (설계 v2 `…_design_v2_20261021.md` 의 R01–R17 · 권고 기본값 = ⬜ 1저자 비준 대기) ─────────────────────────

class RulesV2(RulesV1):
    name = 'v2'
    KAPPA = 1.0              # R02 봉인 전 세분 문턱 = κ · 2 · u_ref (⬜ Qv2-1)
    R_MAX = 2                # R02 세분 최대 회수 (⬜ Qv2-1)
    TOL_MU_R = 0.5 * m.MU_R  # R01 검출 허용 |Δμ_r| = 덱 μ_r ±50 % (⬜ Qv2-6)
    EPS_FIT_D = 1.0          # R06 자유표면 맞춤 잔차 RMS 상한 (단위 = SE parcel 지름 d) (⬜ Qv2-7)
    F_WRAP = 0.05            # R06 벽 두름 분율 상한 (⬜ Qv2-7)

    # R02 — 봉인 전 세분 (DEM 곡선만 · 결과 무관): 이웃 |ΔI| > κ·2·u_ref 인 칸에 기하 중점 수준을 더한다 (최대 R_MAX 회)
    def refine(self, xs, f, u2):
        thr = self.KAPPA * u2
        for _ in range(self.R_MAX):
            new = [xs[0]]
            for a, b in zip(xs, xs[1:]):
                if abs(f(b) - f(a)) > thr:
                    new.append(0.5 * (a + b))
                new.append(b)
            if len(new) == len(xs):
                break
            xs = new
        return xs

    # R02 — 칸 포괄: 칸마다 띠 = √((t_exp·u_exp)² + (t_ν·u_칸)²) + |ΔI_칸| (칸 안 단조면 참 Bo 를 포함) · u_칸 = 두 끝 중 큰 쪽
    #      (ν = None = σ 를 안다고 보는 경우 → 배수 2) · 빈 집합이면 어느 Bo 끝 너머인지 (F10)
    def accept(self, xs, I, u, mm, u_exp, nu=None, t_exp=2.0, interp=True, **kw):
        if any(v is None for v in u):
            return None
        tD = 2.0 if nu is None else t975(nu)
        segs = []
        for k in range(len(xs) - 1):
            uc = max(u[k], u[k + 1])
            band = math.sqrt((t_exp * u_exp) ** 2 + (tD * uc) ** 2) + (abs(I[k + 1] - I[k]) if interp else 0.0)
            s = seg_within(xs[k], xs[k + 1], I[k], I[k + 1], mm, band)
            if s:
                segs.append(s)
        comps = merge(segs)
        return dict(comps=comps, side=None if comps else side_of(xs, I, mm))

    def accept_stat_only(self, xs, I, u, mm, u_exp, nu=None, **kw):
        return self.accept(xs, I, u, mm, u_exp, nu=nu, interp=False)

    # R03 — 연결 성분 하나일 때만 앵커 (그 성분의 log 중점) · 여럿 = F9 '모호' · 한 시험이 빔 = F10 '그 시험 표현 밖 (끝)'
    def anchor(self, A1, A2):
        for A, nm in ((A1, 'T1'), (A2, 'T2')):
            if not A['comps']:
                return dict(status='F10', side=f'{nm} {A.get("side") or "?"}')
        C = intersect(A1['comps'], A2['comps'])
        if not C:
            return dict(status='F5')
        if len(C) > 1:
            return dict(status='F9', comps=C)
        return dict(status='anchor', x=0.5 * (C[0][0] + C[0][1]), comps=C)

    # R01 — B 의 검출 한계 Δμ_r,min = (w₁ + w₂)/|b₁/a₁ − b₂/a₂| · 허용보다 크면 '일치 미검사' (비지 않은 교집합 ≠ 마찰 세트 확인)
    def b_check(self, x1, w1, x2, w2, ratios, tol):
        dr = abs(ratios[0] - ratios[1])
        dmin = (w1 + w2) / dr if dr > 0 else float('inf')
        if abs(x1 - x2) > w1 + w2:
            return dict(status='F5', certifies_friction=False, dmin=dmin)
        if dmin <= tol:
            return dict(status='통과', certifies_friction=True, dmin=dmin, note=f'검출 한계 {dmin:.3f}')
        return dict(status='일치 미검사', certifies_friction=False, dmin=dmin, note=f'검출 한계 {dmin:.3g} > 허용 {tol:.4g}')

    # R04 — u_DEM = 같은 시험 · 2 시드 이상 수준의 합동 SD / √(그 수준 시드 수) · 자유도 = Σ(n − 1) · 배수 = t(ν)
    #      2 시드 수준이 없으면 그 시험은 판정 밖 (보조)
    def u_dem(self, seeds_by_level):
        multi = [v for v in seeds_by_level if len(v) >= 2]
        if not multi:
            return [None] * len(seeds_by_level), '판정 밖 (보조)'
        dof = sum(len(v) - 1 for v in multi)
        s_pool = math.sqrt(sum(sum((a - sum(v) / len(v)) ** 2 for a in v) for v in multi) / dof)
        return [s_pool / math.sqrt(len(v)) for v in seeds_by_level], f'합동 (자유도 {dof})'

    def band_multiplier(self, nu):
        return 2.0 if nu is None else t975(nu)

    def interp_error(self, dI):
        return abs(dI)

    # R04 — T2 정상 상태 = 두 측정 창의 블록 평균 차 ≤ 2·SE (런 안 · u_DEM 과 무관 · 시드 1 개 수준에도 정의)
    def steady(self, w1, w2, u_dem):
        se = math.sqrt(sd(w1) ** 2 / len(w1) + sd(w2) ** 2 / len(w2))
        return abs(sum(w1) / len(w1) - sum(w2) / len(w2)) <= 2.0 * se

    # R04 — 곡선 · 재시도 · u_DEM 런은 같은 NP (D12 = NP 20) · 다르면 그 런 제외
    def run_np_ok(self, run_np, curve_np):
        return run_np == curve_np

    # R05 — 중심 곡선 = 벽 점착 0 · 감도 = 두 끝 (γ_W/γ_SE 0 ↔ 0.0256 = ρ 1) · 벽이 닿는 시험 전부
    def wall_sensitivity(self):
        return dict(gammas=(0.0, m.GM_WALL_HARE2026), tests={'T1', 'T2', 'T3'})

    # R06 — T2 각은 정의 가능할 때만: 맞춤 잔차 RMS ≤ 1 d · 벽 두름 분율 ≤ 5 % (결과 전) · 아니면 '관측 불가' (F2b)
    def t2_angle(self, xs_pts, ys_pts, d, wrap_frac):
        ang, rms = line_fit(xs_pts, ys_pts)
        if rms > self.EPS_FIT_D * d or wrap_frac > self.F_WRAP:
            return dict(status='관측 불가', angle=ang)
        return dict(status='각', angle=ang)

    # R07 — 넘기는 것 = 구간 (두 끝 · 중심) · Bo* ↔ Bo*/G 선택 = S6 등록 · G = 실험 혼합기 확인 뒤 (MXD3-19)
    def transfer(self):
        return dict(value='interval', interval=True, G='MXD3-19 (자료 대기)', convention='S6 등록: Bo* (1 g 그대로) 또는 Bo*/G (D10)')

    # R08 — S3a (규칙 · SOP) < 측정 시작 · 측정 직후 암호화 묶음 push · S3b (C0 뒤 확정값) < 곡선 봉인 < 열람
    #      · 평문 원자료 반입 = 열람 뒤 · 열쇠 커밋 = 봉인 뒤 ~ 열람 전
    def order_ok(self, seq):
        idx = {e: i for i, e in enumerate(seq)}
        need = ('S3a_commit', 'measure_start', 'measure_end', 'raw_push_enc', 'S3b_commit', 'curve_seal', 'raw_open')
        if any(e not in idx for e in need):
            return False
        ok = (idx['S3a_commit'] < idx['measure_start'] < idx['measure_end'] < idx['raw_push_enc'] < idx['raw_open']
              and idx['S3b_commit'] < idx['curve_seal'] < idx['raw_open'])
        if 'C0_end' in idx:
            ok = ok and idx['C0_end'] < idx['S3b_commit']
        if 'raw_push_plain' in idx:
            ok = ok and idx['raw_push_plain'] > idx['raw_open']
        if 'key_commit' in idx:
            ok = ok and idx['curve_seal'] < idx['key_commit'] < idx['raw_open']
        return ok

    # R09 — 예측 = 구간 안 수준 전부 · 이웃 밖 수준과 갈릴 때만 '판별력 있는 검증' · 구간 안에서 갈리면 '불확정'
    def validation(self, preds, i_lo, i_hi, measured):
        inner = {preds[i] for i in range(i_lo, i_hi + 1)}
        outs = [preds[i] for i in (i_lo - 1, i_hi + 1) if 0 <= i < len(preds)]
        if len(inner) > 1:
            return dict(status='불확정 (구간 안에서 갈림)', discriminating=False)
        v = next(iter(inner))
        disc = any(o != v for o in outs)
        return dict(status=('통과' if measured == v else '실패'), discriminating=disc)

    # R10 — 계약을 검사할 수 있는 기하 (지금 = 드럼 + 끝판) · 검사 결과 ≤ 1 % 인 런만 앵커 계산에
    def include_run(self, run, supported):
        return bool(supported) and run['overlap'] is not None and run['overlap'] <= 1.0

    # R11 — 시험 덱 = 상 셋 (AM 타입은 두되 개수 0) · 등록 ρ 팔 블록과 바이트 같음 · 드럼 = 실험 원통 치수 (등록)
    def test_deck(self):
        return dict(phases=('AM_P', 'AM_S', 'SE'), drum='registered')

    def doc_numbers(self):
        return V2_DOC_NUMBERS

    # R13 — F3′: 위 = 세대 천장 × 0.95 한 단계 · 아래 = 바닥 평평 (|ΔI₀₁| ≤ 띠) 이면 확장 없이 '마찰 바닥' (Q3 경로)
    def f3(self, xs, I, f, mm, band, ceiling):
        if mm > max(I) + band:
            if abs(I[-1] - I[-2]) <= band:
                return dict(status='위 포화', level=None)
            return dict(status='확장', level=EXT_FACTOR * ceiling)
        if mm < min(I) - band:
            if abs(I[1] - I[0]) <= band:
                return dict(status='마찰 바닥', level=None)
            lo = xs[0] - 0.5
            if abs(f(lo) - mm) <= band:
                return dict(status='확장', level=10 ** lo)
            return dict(status='표현 범위 밖', level=10 ** lo)
        return dict(status='안')

    # R14 — u_exp = 날 평균들의 표준오차 · 배수 t(날 − 1) · 판독 (계통) 은 2·u_판독 로 합성 · 날 ≥ 3 × 반복 ≥ 3 (⬜ Qv2-4)
    def u_exp_band(self, days, u_read):
        dm = [sum(dd) / len(dd) for dd in days]
        nd = len(dm)
        return sum(dm) / nd, math.sqrt((t975(nd - 1) * sd(dm) / math.sqrt(nd)) ** 2 + (2.0 * u_read) ** 2)

    def exp_plan(self):
        return [3, 3, 3]

    # R15 — ρ_flow 는 Bo_AA(ρ = 0.31) 가 식별 하한 (격자 최소 Bo) 이상일 때만 값 · 아니면 위쪽 한계만
    def rho_flow(self, bo_aa_at_thesis_edge, bo_id):
        return '교차 가능' if bo_aa_at_thesis_edge >= bo_id else '위쪽 한계만'

    # R17 — 결과 전 정의 (권고 기본값 = ⬜ Qv2-13)
    def definitions(self):
        return dict(t2_primary='측정 창 평균 동적 각 (사태 최대 · 최소 · 요동 = 보고)',
                    f1_pair='봉인 곡선의 이웃 차 |ΔI| 중앙값의 ½ (곡선과 함께 봉인)',
                    tap_match='손 탭 = 낙하 높이 · 횟수 맞춤 (Γ 미측정 한정어) · 측정기 = Γ · 횟수 맞춤',
                    ext_seeds='C1 과 같은 시드 규칙 (결과 전)',
                    raw_custody='측정 직후 암호화 묶음 push · 열쇠 = 곡선 봉인 뒤 커밋',
                    policy_stage='launch_policy v5 — d3-c0 · d3-c1 · d3-c2 (② 회차 코드)',
                    f8_rule='D13: 빠진 원자 ≤ 10 · id 1..N · 집합 불변 = TECH 아님 · 그 밖 = TECH → 같은 NP 재시도 1 회 → 결측')


#: 설계 v2 에 적힌 숫자 (그 문서 표기 그대로) — C12 가 lab20261014 계산값과 표기 자릿수 안에서 같은지 본다
#   (v1 자리 22 개 + v2 에만 나오는 숫자 · 문서에 숫자를 더하면 여기에도 더한다)
V2_DOC_NUMBERS = {
    # v1 자리 (같은 열쇠 · lab 값)
    'drum_D_mm': '25.17', 'drum_L_mm': '5.03', 'rpm': '76.68', 'wR_mm_s': '101.0',
    'n_per_fill': '8.27e5', 'n_f011': '9.09e4', 'n_f030': '2.48e5', 'n_slice': '9.86e4',
    'dt_x20': '2.373e-7', 'ceiling_soft': '1015.4', 'ov_637_soft': '0.733', 'ov_850_soft': '0.888',
    'ov_637_x20': '0.0995', 'bo_1pct_x20': '2.03e4', 'vstick_0212_x20': '0.055', 'vstick_212_x20': '17.47',
    'vstick_637_x20': '43.64', 'vstick_ceil_x20': '64.3', 'vstick_ceil_over_wR': '0.64',
    'se_vol_pct': '39.95', 'se_num_pct': '99.16', 'd_over_amp': '18.5',
    # v2 에만
    'd_over_se': '166', 'real_d_over_se': '2.5e4', 'vstick_0212_soft': '0.150', 'vstick_21_x20': '2.56',
    'vstick_21_g': '0.024', 'vstick_212_g': '0.166', 'vstick_637_g': '0.413', 'vstick_637_g_over_wR': '0.0041',
    'ext_level': '964.7', 'ov_ext_soft': '0.966', 'ext_ratio': '1.514', 'ceil_ratio': '1.593',
    'ov_1010_soft': '0.996', 'ov_1020_soft': '1.003', 'ceiling_cgf200': '768.7', 'ov_637_cgf200': '0.883',
    'bo_aa_ratio_amp': '239.5', 'bo_aa_ratio_ams': '47.3',
    'boaa_amp_21_031': '0.0275', 'boaa_ams_21_031': '0.139', 'boaa_amp_21_1': '0.0887', 'boaa_ams_21_1': '0.449',
    'boaa_amp_637_031': '0.825', 'boaa_ams_637_031': '4.18', 'boaa_amp_ceil_031': '1.31', 'boaa_ams_ceil_031': '6.65',
    'steps_1s_x20': '4.214e6', 'h_1s_lo': '16.7', 'h_1s_hi': '18.6', 't2_run_d_lo': '1.11', 't2_run_d_hi': '1.24',
    't5_pa': '179.8', 'rho_mix': '3.567', 'depth_over_R': '0.680',
    't2_cell_cm3': '2.50', 't2_mass_lo_g': '0.14', 't2_mass_hi_g': '0.68', 'rpm_r13': '75.4',
    't975_2': '4.303', 't975_4': '2.776', 't975_8': '2.306', 'ext_low': '0.0672', 'per_decade_vstick': '6.8',
    'dt_scale': '1.104', 't1_short_lo': '0.22', 't1_short_hi': '1.10', 't1_pour_lo': '0.11', 't1_pour_hi': '0.77',
    't1_tap_lo': '0.55', 't1_tap_hi': '4.42', 'c2_run_lo': '0.55', 'c2_run_hi': '1.66',
    'c0_lo': '3.8', 'c0_hi': '5.9', 'c1_lo': '6.1', 'c1_hi': '17.8',
    'c2_t3_runs_lo': '7', 'c2_t3_runs_hi': '11', 'c2_t2_runs_lo': '6', 'c2_t2_runs_hi': '10', 'c2_lo': '3.5', 'c2_hi': '10.2',
    'sum_lo': '13.4', 'sum_hi': '33.9',
}


def print_numbers():
    print('[N] 숫자 — lab20261014 (v2 문서) · gen1 (이력 칸) · CGF 151.4 · N 100000 · 생성기 함수 그대로')
    lab, g1 = computed_numbers(LAB), computed_numbers(GEN1)
    for k in lab:
        print(f'    {k:24s} lab {lab[k]:.6g}   gen1 {g1[k]:.6g}')
    print('    (예산 [추정] — T2 런 = 1.6 s 모사 × ×20 step/s ÷ 처리량 70–63 step/s · T1 · T3 런 = v1 §3-6 [추정] × dt_scale · '
          'C0 = T2 9 + T1 짧은 탭 6 · C1 기본 = T2 12 + T1 탭 8 + 붓기 4 · C2 = T3 7–11 + T2 다른 속도 6–10 · 3 슬롯)')
    print('    F_SW/F_SS = 2√(0.0256·ρ):', ' · '.join(f'ρ {r:g} {2 * math.sqrt(m.GM_WALL_HARE2026 * r):.3f}' for r in (0.0, 0.01, 0.1, 0.31, 1.0)))
    print('    격자 Bo_code:', ' · '.join(f'{b:.4g}' for b in GRID), '· Bo_po:', ' · '.join(f'{b / 6.75:.3g}' for b in GRID))


# ───────────────────────── 실행 ─────────────────────────

def main():
    print('[t] Student t 0.975 분위:', ' · '.join(f'ν {nu} {t975(nu):.3f}' for nu in (1, 2, 3, 4, 5, 6, 8)))
    print_numbers()
    print()
    rulesets = [RulesV1()] + ([RulesV2()] if RulesV2 else [])
    all_ok = True
    print('\n[C] 규칙 검사 — 반례: v1 = 잘못 받아들임 (재현) · v2 = 잡음 · 대조: v2 가 옳은 경우를 받아들임')
    for cid, fn in CHECKS:
        print(f'  {cid} (MXD3-{cid[1:]}) {fn.__doc__.split(chr(10))[0].split("— ", 1)[-1]}')
        got = {}
        for R in rulesets:
            caught, ok, det = fn(R)
            got[R.name] = (caught, ok)
            print(f'      {R.name}: {"잡음" if caught else "반례 통과 (잘못 받아들임)"} · 대조 {"통과" if ok else "실패"} — {det}')
        v1c = got['v1'][0]
        if 'v2' in got:
            v2c, v2ok = got['v2']
            verdict = (not v1c) and v2c and v2ok
            print(f'      ⇒ {"PASS" if verdict else "FAIL"} (v1 반례 재현 {not v1c} · v2 잡음 {v2c} · v2 대조 {v2ok})')
        else:
            verdict = False
            print(f'      ⇒ FAIL (v1 반례 재현 {not v1c} · v2 규칙 미구현 = 시험 먼저 단계)')
        all_ok = all_ok and verdict
    print(f'\n종합: {"PASS — 모든 검사에서 v1 반례 재현 · v2 잡음 · 대조 통과" if all_ok else "FAIL"}')
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
