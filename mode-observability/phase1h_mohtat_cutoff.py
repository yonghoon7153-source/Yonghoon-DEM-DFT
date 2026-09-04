#!/usr/bin/env python3
"""Phase 1h — Mohtat 의 컷오프 등식을 **모드 좌표**에서, **우리 참값**으로 잰다.

## 왜 이 계산인가

Lin & Khoo 2024 는 `[11] Mohtat et al. 2019` (*J. Power Sources* 427, 101–111)
를 **Fisher 로 식별 가능성을 정량한 선행자**로 인정하고, 그 모델이 `[인쇄]`
"has been incorporated in PyBaMM" 이라고 적는다. 그 구현이 우리 환경 안에 있다
(PyBaMM 26.7.1.0 `models/full_battery_models/lithium_ion/electrode_soh.py`,
`pybamm.citations.register("Mohtat2019")`). 거기 docstring 이 모델을 그대로 적는다:

    Q_Li  = y_100·Q_p + x_100·Q_n
    V_max = U_p(y_100) − U_n(x_100)
    V_min = U_p(y_0)   − U_n(x_0)
    x_0   = x_100 − Q/Q_n
    y_0   = y_100 + Q/Q_p

⚠ **원전 PDF 는 아직 못 읽었다** (유료 + 이 환경의 egress 차단). 여기서 대조하는
것은 **그 모델의 구현본**이다. 그래서 이 스크립트가 인용하는 것은 논문이 아니라
`pybamm` 패키지의 소스이고, 그 버전을 출력에 박는다.

## 무엇을 묻나

우리 창 좌표 `[α_PE, β_PE, α_NE, β_NE]` 는 Mohtat 의 네 화학량론 한계
`(y_100, y_0, x_100, x_0)` 와 **일대일**이다 (reference 창 단위에서):

    y_0 − y_100 = 1/α_PE = Q/Q_p        x_100 − x_0 = 1/α_NE = Q/Q_n
    y_100 = −β_PE/α_PE                  x_100 = −β_NE/α_NE

그리고 Mohtat 의 두 전압 등식은 우리 x 축에서 글자 그대로

    g₁ : U_full(x_norm = 0) = V_max          g₂ : U_full(x_norm = 1) = V_min

이다. Phase 1e 는 이 둘을 **창 좌표**에서 재구성 대수로 재서 "강한 쌍과
1.5°·2.0° — 여분이 아니라 정보를 지운다" 를 얻었다.

여기서는 좌표를 바꿔 **모드 좌표 (LLI, LAM_PE, LAM_NE)** 에서, 재구성 대수가
아니라 **PyBaMM 참값 곡선**으로 같은 것을 잰다. 물음은 하나다:

    컷오프 전압은 우리가 못 보는 방향(u_min)에 대해 무엇을 말하는가?

Lin 의 정리가 답을 **예언**한다. `LLI = LAM_PE = LAM_NE = x` 를 따라가면 세 비
`(1−LLI):(1−LAM_NE):(1−LAM_PE)` 가 pristine 과 같으므로 SOC 정규화 곡선이
**통째로 불변**이다 — 양 끝점도 포함해서. 그러므로 이상적인 셀에서는

    ∇g · (1,1,1)/√3 = 0   (정확히)

이어야 한다. 우리 셀은 유한 전류 + 복합 음극이라 정확히 0 은 아닐 것이다.
**그 편차의 크기가 곧 "우리 셀이 Lin 의 이상에서 얼마나 떨어져 있는가" 다.**

## 곁들여 닫는 것 — Phase 1c 의 한계 (a)

Mohtat 의 도구는 **Fisher 정보**, 즉 본성상 **동작점에 매인 국소량**이다.
그러니 그 계보를 대조하는 이 자리에서 Phase 1c 가 스스로 신고한 한계 (a)
`[인용]` "22p 동작점에서 `J` 를 다시 잡으면 방향이 회전할 수 있다 — 국소 분석의
한계" 를 같이 잰다. 동작점 여러 개 × 스텝 두 개로 `∠(u_min, (1,1,1))` 를 훑는다.

출력: results/phase1h/{gradients.csv, augmented.csv, sweep.csv, endpoint_voltages.csv}
+ stdout. **CSV 가 정본이다.**
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1h"

H = 0.02                      # Phase 1c/1g 와 같은 전방차분 스텝 (= 격자 간격)
LO, HI = 0.02, 0.98           # Phase 1c/1g 와 같은 관측 구간
MODES = ["LLI", "LAM_PE", "LAM_NE"]
ONES = np.ones(3) / np.sqrt(3.0)

# Phase 1e 와 같은 두 동작점
OPS = [("pristine", 0.00, 0.00, 0.00),
       ("22p 근방", 0.16, 0.12, 0.12)]

# Phase 1c 한계 (a) 를 재는 훑기 — 대각선 + 비대각 동작점
SWEEP = [(0.00, 0.00, 0.00), (0.04, 0.04, 0.04), (0.08, 0.08, 0.08),
         (0.12, 0.12, 0.12), (0.16, 0.16, 0.16),
         (0.16, 0.12, 0.12), (0.12, 0.16, 0.08), (0.08, 0.12, 0.16)]
STEPS = (0.02, 0.04)


def ang(u, v):
    c = abs(float(u @ v)) / (np.linalg.norm(u) * np.linalg.norm(v))
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n  원자료는 gitignored 다.")

    try:
        import pybamm
        soh_src = Path(pybamm.__file__).parent / (
            "models/full_battery_models/lithium_ion/electrode_soh.py")
        src_ok = "Mohtat2019" in soh_src.read_text(encoding="utf-8")
        print(f"대조 대상 : pybamm {pybamm.__version__} · {soh_src.name}"
              f" · Mohtat2019 인용 {'✓' if src_ok else '✗'}")
    except Exception as e:                       # pragma: no cover - 진단용
        print(f"대조 대상 : pybamm 확인 실패 ({e})")
    print("            ⚠ 원전 PDF 미확보 — 구현본 대조다\n")

    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah", "x_norm", "v_full"])
    d0 = df[df.noise == 0]

    # 조건별 요약: 관측 구간 양 끝의 full-cell 전압
    recs = []
    for c, g in d0.groupby("cond_id", sort=False):
        g = g.sort_values("x_norm")
        x = g.x_norm.to_numpy(float)
        v = g.v_full.to_numpy(float)
        recs.append({"cond_id": c, "lli": g.lli.iloc[0], "lam_pe": g.lam_pe.iloc[0],
                     "lam_ne": g.lam_ne.iloc[0], "q_mah": g.q_mah.iloc[0],
                     "v_hi": float(np.interp(0.0, x, v)),      # g₁ · 만충단
                     "v_lo": float(np.interp(1.0, x, v))})     # g₂ · 만방단
    tab = pd.DataFrame(recs)

    print(f"격자 조건 {len(tab)}개 (noise=0)")
    print(f"  g₁ = U_full(x=0)  {tab.v_hi.min():.4f} ~ {tab.v_hi.max():.4f} V"
          f"   (폭 {1e3*(tab.v_hi.max()-tab.v_hi.min()):.1f} mV)")
    print(f"  g₂ = U_full(x=1)  {tab.v_lo.min():.4f} ~ {tab.v_lo.max():.4f} V"
          f"   (폭 {1e3*(tab.v_lo.max()-tab.v_lo.min()):.1f} mV)")
    print("  → 컷오프 등식은 참값에서 **정확히는 성립하지 않는다**"
          " (유한 전류 · 복합 음극).\n")

    def at(l, p, n):
        r = tab[np.isclose(tab.lli, l) & np.isclose(tab.lam_pe, p)
                & np.isclose(tab.lam_ne, n)]
        return None if r.empty else r.iloc[0]

    def curve(l, p, n, xs):
        r = tab[np.isclose(tab.lli, l) & np.isclose(tab.lam_pe, p)
                & np.isclose(tab.lam_ne, n)]
        if r.empty:
            return None
        g = d0[d0.cond_id == r.cond_id.iloc[0]].sort_values("x_norm")
        return np.interp(xs, g.x_norm.to_numpy(float), g.v_full.to_numpy(float))

    # 관측 격자 — Phase 1c/1g 와 같은 x 축
    ref_x = d0[d0.cond_id == tab.cond_id.iloc[0]].sort_values("x_norm").x_norm.to_numpy(float)
    xs = ref_x[(ref_x >= LO) & (ref_x <= HI)]

    def spectrum(l0, p0, n0, h):
        """곡선 Jacobian → (J, 특이값, u_min). 축 조건이 없으면 None."""
        v0 = curve(l0, p0, n0, xs)
        if v0 is None:
            return None
        cols = []
        for a in ((l0 + h, p0, n0), (l0, p0 + h, n0), (l0, p0, n0 + h)):
            va = curve(*a, xs)
            if va is None:
                return None
            cols.append((va - v0) / h)
        J = np.column_stack(cols)
        w, V = np.linalg.eigh(J.T @ J)
        sv = np.sqrt(np.maximum(w, 0.0))
        u = V[:, 0] / np.linalg.norm(V[:, 0])
        return J, sv, (-u if u.sum() < 0 else u)

    # ── Phase 1c 한계 (a): null 방향이 동작점·스텝에 얼마나 매여 있나 ──────
    print("── 훑기: ∠(u_min, (1,1,1)) 의 동작점·스텝 의존성 "
          "(Phase 1c 한계 (a)) ──")
    print(f"{'(LLI, LAM_PE, LAM_NE)':>22} {'H':>5} {'∠':>8} {'조건수':>8}   u_min")
    srows = []
    for pt in SWEEP:
        for h in STEPS:
            r = spectrum(*pt, h)
            if r is None:
                print(f"{str(pt):>22} {h:>5} {'— 격자에 없다':>8}")
                continue
            _, sv, u = r
            a = ang(u, ONES)
            print(f"{str(pt):>22} {h:>5} {a:>7.2f}° {sv[-1]/sv[0]:>8.2f}"
                  f"   {np.round(u, 4)}")
            srows.append({"lli": pt[0], "lam_pe": pt[1], "lam_ne": pt[2], "step": h,
                          "angle_ones_deg": a, "cond": float(sv[-1] / sv[0]),
                          **{f"u_min_{m}": u[k] for k, m in enumerate(MODES)},
                          **{f"sv{k+1}": float(sv[k]) for k in range(3)}})
    if srows:
        s = pd.DataFrame(srows)
        for h in STEPS:
            q = s[s.step == h]
            if len(q):
                print(f"   H = {h}: ∠ 범위 {q.angle_ones_deg.min():.2f}°"
                      f" ~ {q.angle_ones_deg.max():.2f}°"
                      f"  (중앙 {q.angle_ones_deg.median():.2f}°)")
        print()

    grows, arows = [], []
    for label, l0, p0, n0 in OPS:
        base = at(l0, p0, n0)
        if base is None:
            print(f"[건너뜀] {label}: 격자에 없다")
            continue
        axes = [(l0 + H, p0, n0), (l0, p0 + H, n0), (l0, p0, n0 + H)]
        if any(at(*a) is None for a in axes):
            print(f"[건너뜀] {label}: 축 조건이 격자에 없다")
            continue

        # ── 컷오프 등식의 gradient (2×3) ────────────────────────────────
        G = np.array([[(at(*a).v_hi - base.v_hi) / H for a in axes],
                      [(at(*a).v_lo - base.v_lo) / H for a in axes]])

        # ── 곡선 Jacobian (Phase 1c/1g A 판과 같은 구성) ────────────────
        J, sv, u_min = spectrum(l0, p0, n0, H)

        print(f"══ {label} (LLI {l0} · LAM_PE {p0} · LAM_NE {n0}) ══")
        print(f"   곡선 Jacobian  특이값 {np.round(sv, 4)}"
              f"   조건수 {sv[-1]/sv[0]:.2f}")
        print(f"   u_min {np.round(u_min, 5)}   ∠(u_min,(1,1,1)) = {ang(u_min, ONES):.2f}°")
        for i, nm in enumerate(("g₁ = U_full(x=0)", "g₂ = U_full(x=1)")):
            gi = G[i]
            d_ones = float(gi @ ONES)
            d_umin = float(gi @ u_min)
            print(f"   {nm}")
            print(f"      ∇g {np.round(gi, 4)} V/단위   |∇g| = {np.linalg.norm(gi):.4f}")
            print(f"      ∇g·(1,1,1)/√3 = {d_ones:+.5f}   ∠ = {ang(gi, ONES):6.2f}°"
                  f"   (이상적 셀이면 90.00°)")
            print(f"      ∇g·u_min      = {d_umin:+.5f}   ∠ = {ang(gi, u_min):6.2f}°")
            grows.append({"op": label, "constraint": nm,
                          **{f"grad_{m}": gi[k] for k, m in enumerate(MODES)},
                          "norm": float(np.linalg.norm(gi)),
                          "dot_ones": d_ones, "angle_ones_deg": ang(gi, ONES),
                          "dot_umin": d_umin, "angle_umin_deg": ang(gi, u_min)})

        # ── 두 끝점을 관측에 **더하면** 최소 감도가 얼마나 오르나 ────────
        # 곡선 fit 은 이미 xs 위 전 점을 쓴다. 여기서 재는 것은 "끝점 두 개를
        # 같은 무게로 하나씩 더 얹었을 때" 의 상한 — 즉 낙관적 상계다.
        sv_aug = np.linalg.svd(np.vstack([J, G]), compute_uv=False)
        rms_per_point = sv[0] / np.sqrt(J.shape[0])
        print(f"   최소 감도 σ_min  {sv[0]:.4f}  →  {sv_aug[-1]:.4f} "
              f"(끝점 2개 추가 · {100*(sv_aug[-1]/sv[0]-1):+.2f} %)")
        print(f"   조건수          {sv[-1]/sv[0]:.2f}  →  {sv_aug[0]/sv_aug[-1]:.2f}")
        print(f"   참고: 곡선 1점당 평균 감도 {rms_per_point:.4f} V/단위\n")
        arows.append({"op": label, "sigma_min": float(sv[0]),
                      "sigma_min_augmented": float(sv_aug[-1]),
                      "rel_gain_pct": float(100 * (sv_aug[-1] / sv[0] - 1)),
                      "cond": float(sv[-1] / sv[0]),
                      "cond_augmented": float(sv_aug[0] / sv_aug[-1]),
                      "n_curve_points": int(J.shape[0]),
                      "mean_sensitivity_per_point": float(rms_per_point)})

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(grows).to_csv(OUT / "gradients.csv", index=False)
    pd.DataFrame(arows).to_csv(OUT / "augmented.csv", index=False)
    pd.DataFrame(srows).to_csv(OUT / "sweep.csv", index=False)
    tab.to_csv(OUT / "endpoint_voltages.csv", index=False)
    print(f"산출물: {OUT}/  (gradients.csv · augmented.csv · sweep.csv"
          f" · endpoint_voltages.csv)")


if __name__ == "__main__":
    main()
