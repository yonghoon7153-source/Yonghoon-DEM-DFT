#!/usr/bin/env python3
"""믹서 D3 설계 사전 공격 리뷰 — 숫자 대조 · 해석 반례 재현 (읽기 전용).

    python3 docs/reviews/codex_mixer_d3_design_request_evidence_20261021/d3_precheck_numbers.py

* 시뮬레이션 0 · 덱 생성 0 · 파일 쓰기 0 — 생성기 `scripts/make_mixer_deck.py` 와 검사기 `scripts/check_contact_validity.py`
  의 **함수만** 불러 값을 낸다 (화면 출력만).  같은 판의 출력 = 옆 파일 `d3_precheck_numbers_output.txt`.
* 대상 설계 = `docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md` (커밋 `add01968f` · 비준 표지 `4b1d67f62`).
* 절 번호 [1]–[14] = 요청서 `docs/reviews/codex_mixer_d3_design_request_20261021.md` §2-1 · §2-3 표의 '근거' 칸.
* 기준 판 = 커밋 `a76f59d0d` (생성기 · 검사기 그 판) · 출력은 같은 판에서 두 번 돌려 바이트가 같다.
* [가정 예시] 가 붙은 수 (기울기 · u · 전이 폭) 는 **반례의 꼴을 보이기 위한 예시값**이지 측정이 아니다.
"""
import importlib.util
import math
import os
import random
import sys

sys.dont_write_bytecode = True        # 불러온 리포 모듈의 바이트코드 캐시 (`scripts/__pycache__`) 도 쓰지 않는다 — '파일 쓰기 0' 을 글자 그대로

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m = _load('mmd', 'scripts/make_mixer_deck.py')
GENS = (None, 'lab20261014')          # None = gen1 (DENS 그 객체) — 설계 숫자의 출처 세대 · lab = Q11 비준 세대
GNAME = {None: 'gen1', 'lab20261014': 'lab20261014'}
NU_SE = m.PHASE_MECH['SE'][0]
CGF = 151.4
N_TOTAL = 100000


def se_ced(bo, E_se, rho_se, d_se):
    return m.ced_for_bond(bo, d_se / 2.0, NU_SE, rho_se, E=E_se)


def se_overlap_pct(bo, E_se, rho_se, d_se):
    return m.overlap_for_ced(se_ced(bo, E_se, rho_se, d_se), d_se / 2.0, NU_SE, E=E_se) * 100.0


def v_stick_mm_s(bo, E_se, rho_se, d_se):
    """SE–SE 붙는 충돌 속도 상한 — 생성기 셀프테스트 U⑤ 의 식 그대로 (W = (1/5)π·CED·R*·δ_eq² · KE ≤ W(1−e²)/e²)."""
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


def phi_norm(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


print('[1] 생성기 상수 · 설계 §3-3 격자')
print(f'    BO_BASE {m.BO_BASE} · MU_S {m.MU_S} · MU_R {m.MU_R} · COR {m.COR} · FR_ANCHOR {m.FR_ANCHOR} · GM_WALL_HARE2026 {m.GM_WALL_HARE2026:.4f}')
print(f'    E_PHASE {m.E_PHASE}')
grid = [m.BO_BASE * 10 ** (k / 2.0) for k in range(7)] + [3000.0 * m.BO_BASE]
print('    격자 = BO_BASE·10^(k/2) (k 0–6) + 3000·BO_BASE:', ' · '.join(f'{x:.4g}' for x in grid))
print(f'    마지막 간격 637.32/212.44 = {grid[-1] / grid[-2]:.4f} (√10 = {math.sqrt(10):.4f})')
print(f'    Bo_po = Bo_code/6.75 (원장 HB-02): {grid[0] / 6.75:.4f} … {grid[-1] / 6.75:.2f}')

print('\n[2] 세대별 (설계 숫자 = gen1 · Q11 비준 = lab20261014) · CGF 151.4 · N 100000')
rows = {}
for gen in GENS:
    for F in (1.0, 20.0):
        p = m.plan(N_TOTAL, cgf=CGF, stiffen_se=F, dens_gen=gen)
        rho_se, d_se, E_se = p['dens']['SE'], p['d']['SE'], p['E']['SE']
        rpm = m.rpm_for_fr(m.FR_ANCHOR, p['R'])
        wR = 2.0 * math.pi * rpm / 60.0 * p['R'] * 1e3
        vdrum = math.pi * p['R'] ** 2 * p['L']
        vpar = math.pi / 6.0 * d_se ** 3
        ceil = bo_at_ceiling(E_se, rho_se, d_se)
        steps = 1.0 / p['dt']
        rows[(gen, F)] = dict(ceil=ceil, wR=wR, R=p['R'], d_se=d_se, rho_se=rho_se, E_se=E_se)
        print(f'    {GNAME[gen]:12s} ×{F:<4g} 드럼 D {2 * p["R"] * 1e3:.3f} · L {p["L"] * 1e3:.3f} mm · rpm(Fr) {rpm:.2f} · ωR {wR:.1f} mm/s · '
              f'dt {p["dt"]:.4e} s ({p["dt_by"]}) · SE 고체 부피 {p["phi"]["SE"] * 100:.2f} % · SE 수 {p["n"]["SE"] / sum(p["n"].values()) * 100:.2f} %')
        print(f'    {"":12s}       N/충진 (pack 0.6) {vdrum * 0.6 / vpar:.4e} · AM_P parcel {p["d"]["AM_P"] * 1e3:.4f} mm · D/d_AMP {2 * p["R"] / p["d"]["AM_P"]:.1f} · '
              f'1 s 모사 = {steps:.4e} step = {steps / 70 / 3600:.2f}–{steps / 63 / 3600:.2f} h (70–63 step/s)')
        for bo in (m.BO_BASE, 1000.0 * m.BO_BASE, 3000.0 * m.BO_BASE):
            print(f'    {"":12s}       Bo {bo:8.3f}: SE–SE δ₀/r {se_overlap_pct(bo, E_se, rho_se, d_se):.4f} % · 붙는 속도 {v_stick_mm_s(bo, E_se, rho_se, d_se):.3f} mm/s')
        print(f'    {"":12s}       SE–SE 정적 1 % 천장 Bo = {ceil:.1f} · 그 Bo 의 붙는 속도 {v_stick_mm_s(ceil, E_se, rho_se, d_se):.1f} mm/s '
              f'(= ωR 의 {v_stick_mm_s(ceil, E_se, rho_se, d_se) / wR:.2f})')
for gen in GENS:
    r1, r20 = rows[(gen, 1.0)], rows[(gen, 20.0)]
    v = v_stick_mm_s(r1['ceil'], r20['E_se'], r20['rho_se'], r20['d_se'])
    print(f'    {GNAME[gen]:12s} 설계 §1-1 "천장에서 ×20 붙는 속도": soft 천장 Bo {r1["ceil"]:.1f} 을 ×20 덱에 → {v:.1f} mm/s (ωR 의 {v / r20["wR"]:.2f})')
for gen in GENS:
    p = m.plan(N_TOTAL, cgf=CGF, dens_gen=gen)
    vd = math.pi * p['R'] ** 2 * p['L']
    vp = math.pi / 6.0 * p['d']['SE'] ** 3
    print(f'    {GNAME[gen]:12s} T2 parcel 수: f 0.11 → {0.11 * vd * 0.6 / vp:.3e} · f 0.30 → {0.30 * vd * 0.6 / vp:.3e} · '
          f'2 mm 주기 조각 f 0.30 → {0.30 * math.pi * p["R"] ** 2 * 2e-3 * 0.6 / vp:.3e}')

print('\n[3] 벽 — γ_W/γ_SE = 0.0256·ρ (D2 · --gm-wall-ncm) 일 때 SE–벽 / SE–SE 당김힘 비 = 2·√(0.0256·ρ) (R*_SW = r · R*_SS = r/2)')
for rho in (1.0, 0.31, 0.1, 0.03, 0.01):
    gw = m.GM_WALL_HARE2026 * rho
    print(f'    ρ {rho:<5g} γ_W/γ_SE {gw:.5f} · F_SW/F_SS {2.0 * math.sqrt(gw):.4f}')
print('    설계 C0 두 값 = ρ {0.31, 1} → F_SW/F_SS [0.178, 0.320] · 논지 구간 ρ < 0.31 → (0, 0.178)')

print('\n[4] (선택) NCM 자기 Bo — 결합 규칙 아래 Bo_AA / Bo_SS = ρ · (R*_AA/R*_SS) · (W_SE/W_AM)')
for gen in GENS:
    p = m.plan(N_TOTAL, cgf=CGF, dens_gen=gen)
    dn, d = p['dens'], p['d']
    w = {k: math.pi / 6.0 * d[k] ** 3 * dn[m.PHASE_MECH[k][1]] for k in d}
    for k in ('AM_P', 'AM_S'):
        fac = (d[k] / d['SE']) * (w['SE'] / w[k])
        print(f'    {GNAME[gen]:12s} Bo_{k}–{k} / Bo_SE–SE = ρ / {1.0 / fac:.1f}  → ρ 0.31 · Bo_SE 21.24 이면 {0.31 * 21.244 * fac:.3f} · 코팅 (ρ 1) 이면 {21.244 * fac:.3f}')

print('\n[5] u_DEM — 시드 2 개의 표본 SD s (자유도 1) 가 참 σ 보다 작게 나올 확률 = 2Φ(k) − 1')
for k in (0.3, 0.5):
    print(f'    P(s < {k}σ) = {2.0 * phi_norm(k) - 1.0:.4f}')
random.seed(20261021)
n = 200000
cnt = sum(1 for _ in range(n) if abs(random.gauss(0, 1) - random.gauss(0, 1)) / math.sqrt(2.0) < 0.5)
print(f'    몬테카를로 확인 (n {n}): P(s < 0.5σ) ≈ {cnt / n:.4f}')

print('\n[6] 받아들일 범위가 끊긴 집합이면 "기하 중심" 이 그 집합 밖에 떨어진다 (비단조 곡선 · grey1969 꼴)')
S = [(grid[1], grid[2]), (grid[5], grid[6])]
c = math.sqrt(S[0][0] * S[1][1])
inside = any(a <= c <= b for a, b in S)
print(f'    S = [{S[0][0]:.3f}, {S[0][1]:.3f}] ∪ [{S[1][0]:.2f}, {S[1][1]:.2f}] → 감싸는 구간의 기하 중심 {c:.2f} · S 안? {inside}')

print('\n[7] 두 시험 교집합 검사의 검출력 (선형화 · [가정 예시]) — I_k = a_k·x + b_k·μ_r (x = log10 Bo)')
print('    덱 μ_r 이 Δ 만큼 틀리면 시험 k 의 앵커 x_k = x_true − (b_k/a_k)·Δ · 반폭 w_k = 2u_k/|a_k|')
print('    ⇒ 교집합이 빈다 ⟺ |b_1/a_1 − b_2/a_2|·|Δ| > w_1 + w_2  ⇒  검출 가능한 최소 |Δ| = (w_1 + w_2)/|b_1/a_1 − b_2/a_2|')
for (k1, k2) in ((40.0, 40.0), (40.0, 10.0)):
    a1, a2 = 5.0, 5.0                     # [가정 예시] °/decade (nase2001 평균 기울기 25°/5 decade 꼴)
    u1 = u2 = 1.5                         # [가정 예시] °
    w = 2 * u1 / a1 + 2 * u2 / a2
    dk = abs(k1 / a1 - k2 / a2)
    dmin = (w / dk) if dk > 0 else float('inf')
    print(f'    b1 {k1:g} · b2 {k2:g} °/단위 μ_r (a1 = a2 = 5 °/decade · u = 1.5 °) → 최소 검출 |Δμ_r| = {dmin:.4g}'
          + ('  (b/a 가 같으면 어떤 Δ 도 못 잡는다)' if dk == 0 else ''))

print('\n[8] 가파른 전이를 반 decade 격자의 직선 보간으로 읽을 때 구간이 참값을 놓치는 비율 ([가정 예시] · jarray2019 꼴)')
D_ANG, U = 13.9, 1.5                     # 35.0 → 48.9° (jarray2019 카드) · u = 1.5° [가정 예시]
WID = 0.1                                 # 10–90 % 전이 폭 0.1 decade [가정 예시 — jarray 0.06 → 0.075 mN (×1.25) 에 +7.3°]
s = WID / (2.0 * math.log(9.0))
xs = [math.log10(g) for g in grid[:7]]


def accept_hull(gv, mm, band):
    """구간 선형 보간 곡선에서 |I − m| ≤ band 인 x 의 집합 → 감싸는 구간 (없으면 None) — 조각마다 정확히 푼다."""
    lo_ = hi_ = None
    for a in range(len(xs) - 1):
        ga, gb = gv[a], gv[a + 1]
        if gb == ga:
            if abs(ga - mm) > band:
                continue
            t_lo, t_hi = 0.0, 1.0
        else:
            t1, t2 = (mm - band - ga) / (gb - ga), (mm + band - ga) / (gb - ga)
            t_lo, t_hi = max(0.0, min(t1, t2)), min(1.0, max(t1, t2))
            if t_lo > t_hi:
                continue
        xa, xb = xs[a] + t_lo * (xs[a + 1] - xs[a]), xs[a] + t_hi * (xs[a + 1] - xs[a])
        lo_ = xa if lo_ is None else min(lo_, xa)
        hi_ = xb if hi_ is None else max(hi_, xb)
    return None if lo_ is None else (lo_, hi_)


stats = {'전부': [0, 0, []], '가파른 부분 (두 평탄값에서 2u 넘게 떨어진 m)': [0, 0, []]}
for i in range(200):
    xstar = xs[2] + 0.5 * (i + 0.5) / 200.0                      # 전이 중심이 2.12 ↔ 6.72 칸 안 어디든 (균등)
    gv = [35.0 + D_ANG / (1.0 + math.exp(-(x - xstar) / s)) for x in xs]
    for j in range(41):
        xt = xstar - 0.1 + 0.2 * j / 40.0                         # 실측 분말이 전이 근처 (±0.1 decade)
        mm = 35.0 + D_ANG / (1.0 + math.exp(-(xt - xstar) / s))
        h = accept_hull(gv, mm, 2.0 * U)
        if h is None:
            continue
        keys = ['전부'] + (['가파른 부분 (두 평탄값에서 2u 넘게 떨어진 m)'] if 35.0 + 2 * U < mm < 35.0 + D_ANG - 2 * U else [])
        for k in keys:
            st = stats[k]
            st[0] += 1
            st[2].append(h[1] - h[0])
            if not (h[0] <= xt <= h[1]):
                st[1] += 1
for k, (tot, miss, widths) in stats.items():
    print(f'    {k}: {tot} 건 중 참 log10 Bo 가 보고 구간 (감싸는 구간) 밖 = {miss} ({miss / tot * 100:.1f} %) · 보고 구간 폭 중앙 '
          f'{sorted(widths)[len(widths) // 2]:.3f} decade')
print(f'    (이웃 격자 차 ≈ {D_ANG:.1f}° ≫ 2u = {2 * U:.1f}° 라 설계 §3-7 의 식별 검사는 통과한다 · 보간 오차는 u 에 없다)')

print('\n[9] F3 위쪽 "한 번 확장 (×√10 · 위로는 천장까지)" — 실제로 열리는 배수 = 천장 / 637.32')
for gen in GENS:
    print(f'    {GNAME[gen]:12s} soft 천장 {rows[(gen, 1.0)]["ceil"]:.1f} → ×{rows[(gen, 1.0)]["ceil"] / (3000 * m.BO_BASE):.3f} (√10 = 3.162)')

print('\n[10] 생성기 — SE 만의 상 집합 · 드럼 치수의 출처')
try:
    m.set_phases(('SE',))
    print('    set_phases((\'SE\',)) 통과 — 예상과 다름')
except AssertionError as e:
    print(f'    set_phases((\'SE\',)) → AssertionError: {e}')
finally:
    m.set_phases(('AM_P', 'AM_S', 'SE'))
for nt in (100000, 50000):
    p = m.plan(nt, cgf=CGF, dens_gen='lab20261014')
    print(f'    plan(n_total {nt}) 드럼 R {p["R"] * 1e3:.3f} mm (R = (2.5·V_drum/π)^(1/3) · V_drum = AM_P 고체 부피/φ_AMP/(fill·pack))')

print('\n[11] 접촉 계약 검사기 — 드럼 + 끝판 밖의 벽 메시')
ccv = _load('ccv', 'scripts/check_contact_validity.py')
for meshes in (['Drum', 'Front', 'Back'], ['Funnel'], ['TapFloor']):
    try:
        ccv.container_at('/nonexistent_run_dir', {'used': meshes, 'meshes': {}, 'moves': {}}, 0)
        print(f'    {meshes}: 예외 없음')
    except ValueError as e:
        print(f'    {meshes}: ValueError — {e}')
    except Exception as e:                       # noqa: BLE001 — 지원 메시는 STL 을 읽으려다 다른 예외로 간다 (계약 검사 자체는 진입)
        print(f'    {meshes}: {type(e).__name__} (지원 메시 — STL 읽기 단계까지 진입)')

print('\n[12] T5 침대 바닥 압력 어림 (깊이 0.68 R = 충진 0.30 · 겉보기 0.6 × 평균 고체 밀도)')
f, lo, hi = 0.30, 0.0, 2.0 * math.pi
for _ in range(200):
    th = 0.5 * (lo + hi)
    if (th - math.sin(th)) / (2.0 * math.pi) > f:
        hi = th
    else:
        lo = th
dep = 1.0 - math.cos(lo / 2.0)
for gen in GENS:
    p = m.plan(N_TOTAL, cgf=CGF, dens_gen=gen)
    rho_mix = 100.0 / sum(p['wt'][k] / p['dens'][m.PHASE_MECH[k][1]] for k in p['wt'])
    print(f'    {GNAME[gen]:12s} 깊이/R {dep:.4f} · R {p["R"] * 1e3:.3f} mm · 평균 고체 밀도 {rho_mix:.4f} g/cm³ → {0.6 * rho_mix * 1e3 * 9.81 * dep * p["R"]:.1f} Pa')
p1 = m.plan(N_TOTAL, cgf=CGF)
print(f'    설계의 조합 (gen1 R {p1["R"] * 1e3:.2f} mm × 3.57 g/cm³) → {0.6 * 3570 * 9.81 * dep * p1["R"]:.1f} Pa')

print('\n[13] D10 "강도 = Bo/G" (파이프라인 §4 · 1저자 10-20) 를 앵커에 곱하면 — G 268 (mixing_model_design §18-1 Thinky 표 · 실험 혼합기 미확인)')
r20 = rows[('lab20261014', 20.0)]
for bo in (21.244, 212.44, 637.32):
    bg = bo / 268.0
    v = v_stick_mm_s(bg, r20['E_se'], r20['rho_se'], r20['d_se'])
    print(f'    Bo* {bo:7.2f} → Bo*/268 = {bg:.4f} · ×20 (lab) SE–SE 붙는 속도 {v:.3f} mm/s (ωR {r20["wR"]:.1f} mm/s 의 {v / r20["wR"]:.4f})')

print('\n[14] 천장 — 두 세대 나란히 (D2 사전 리뷰 PRE-MIXD2-07 대조) · soft E (생성기 천장 검사 = soft) · δ₀/r 은 SE–SE 동종 쌍 식')
import re as _re
for gen in GENS:
    for cg in (151.4, 200.0):
        p = m.plan(N_TOTAL, cgf=cg, dens_gen=gen)
        rho_se, d_se, E_se = p['dens']['SE'], p['d']['SE'], p['E']['SE']
        vals = ' · '.join(f'{bo:g} → {se_overlap_pct(bo, E_se, rho_se, d_se):.3f} %'
                          for bo in (3000.0 * m.BO_BASE, 4000.0 * m.BO_BASE, 1010.0, 1020.0))
        print(f'    {GNAME[gen]:12s} CGF {cg:5.1f}: {vals} · 1 % 천장 Bo {bo_at_ceiling(E_se, rho_se, d_se):.1f}')


def d2_ceiling(gen, rho):
    """D2 결합 규칙 팔 (γ_AM = ρ · 벽 = 비코팅 NCM 에 묶음) 을 생성기 `ced_matrix_geomean` (모든 쌍 δ₀/min r 천장 단언) 에 넣어
    받아들여지는 가장 큰 Bo_SE 를 이분 탐색 — 덱 경로와 같은 호출 (E = soft · dens = 그 세대)."""
    p = m.plan(N_TOTAL, cgf=CGF, dens_gen=gen)
    gw = m.gm_wall_from_ncm(rho)

    def ok(bo):
        a = m.gm_arm({'AM_P': rho, 'AM_S': rho, 'SE': 1.0}, gamma_wall=gw, bo_se=bo, rho_uncoated_ncm=rho)
        try:
            m.ced_matrix_geomean(a, p['d'], dens=p['dens'])
            return True, ''
        except SystemExit as e:
            hit = _re.search(r'(AM_P|AM_S|SE|WALL)–(AM_P|AM_S|SE|WALL) 겹침 ([0-9.]+) %', str(e))
            return False, (f'{hit.group(1)}–{hit.group(2)} {hit.group(3)} %' if hit else str(e)[:80])
    lo, hi = 100.0, 1.0e5
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if ok(mid)[0]:
            lo = mid
        else:
            hi = mid
    return lo, ok(hi * 1.0001)[1], ok(849.76)[0], ok(1010.0)[0], ok(1020.0)[0]


for gen in GENS:
    for rho in (1.0, 0.3):
        lo, why, a850, a1010, a1020 = d2_ceiling(gen, rho)
        print(f'    {GNAME[gen]:12s} D2 팔 ρ {rho}: 받아들여지는 최대 Bo_SE {lo:.1f} (넘으면 막는 쌍 = {why}) · 849.76 {"받음" if a850 else "거부"}'
              f' · 1010 {"받음" if a1010 else "거부"} · 1020 {"받음" if a1020 else "거부"}')
