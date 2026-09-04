#!/usr/bin/env python3
"""Phase 1m — `n₁` 을 격자에 심는다: **li ↔ de 축퇴를 직접 시뮬로 시험한다.**

## 무엇을 시험하나

`wiki/comparisons/halfcell-window-parametrization-lineage.md` 가 Marongiu 식
(2)–(5) 의 null 을 닫힌 형태로 풀었고 이 위키가 독립 검산했다:

```
(l,a,b,c,d) = (LLI, LAM_Pe,Li, LAM_Pe,De, LAM_Ne,Li, LAM_Ne,De)
n₁ = ( −N , 0 , 0 , +1 , −1 )        N = Q_Ne,BOL (로딩비)
```

곧 **`{LAM_Ne,Li = δ}` 와 `{LAM_Ne,De = δ, LLI = N·δ}` 가 같은 곡선을 낸다.**

같은 진술이 세 곳에 서로 다른 정밀도로 있다:
- `[인쇄]` **Dubarry 2012** 식 (8'): `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}`
- `[인쇄]` **Birkl 2017** §4.2: 산문으로 "같은 OCV 시그니처를 낸다" (정량 없음)
- **Marongiu 2016**: 축퇴를 **근거로 파라미터를 죽이면서** 이름을 안 붙인다

**세 편 중 아무도 수치로 확인하지 않았다.** 우리 격자도 `de` 만 돌렸다.
이 스크립트가 `li` 를 새로 돌려 **그 등가를 직접 잰다.**

## 왜 이제 할 수 있나

`src/modes.py:build_overrides(..., lam_ne_type="li")` 가 **이미 그 타입을
지원한다** (L211–215). 우리가 안 돌렸을 뿐이다. 한 조건이 **~2초**다.
`degradation-degeneracy/` 는 **import 만** 하고 아무것도 안 고친다.

## 로딩비 `N` 은 어디서

`N = Q_NE / Q_PE` 를 셀 기하에서 계산한다 (`F·A·c_max·vf·L/3600`).
복합 음극이므로 두 상을 더한다. **원전들은 이 값을 인쇄하지 않았고
(Marongiu `[인쇄]` "normally bigger than one" 뿐) 우리는 계산할 수 있다.**

출력: results/phase1m/{pairs.csv, curves_summary.csv} + stdout. **CSV 가 정본이다.**
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

from src.baseline import get_discharged_state  # noqa: E402
from src.curves import extract_curves  # noqa: E402
from src.modes import Baseline, InfeasibleConditionError, build_overrides  # noqa: E402
from src.runner import run_one  # noqa: E402

CFG = DD / "configs" / "base.yaml"
OUT = HERE / "results" / "phase1m"
PROTOCOL = "charge_first"          # 격자와 같은 프레임
F_CONST = 96485.0

# 시험할 δ (LAM_NE) — 격자 간격과 같은 눈금
DELTAS = [0.04, 0.08, 0.12]


def electrode_capacities(cfg):
    """전극 총용량 [Ah] — F·A·c_max·vf·L/3600. NE 는 두 상의 합."""
    import pybamm
    b = cfg["baseline"]
    p = pybamm.ParameterValues(cfg["parameter_set"])
    area = p["Electrode height [m]"] * p["Electrode width [m]"]
    k = F_CONST * area / 3600.0
    q_pe = k * b["pe_max_conc"] * b["pe_vf"] * p["Positive electrode thickness [m]"]
    q_ne = k * (b["ne_primary_max_conc"] * b["ne_primary_vf"]
                + b["ne_secondary_max_conc"] * b["ne_secondary_vf"]) \
        * p["Negative electrode thickness [m]"]
    return float(q_pe), float(q_ne)


def main():
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    b = Baseline.from_config(cfg)
    d = get_discharged_state(cfg)          # 이미 DischargedState 를 돌려준다

    q_pe, q_ne = electrode_capacities(cfg)
    N = q_ne / q_pe
    print(f"전극 총용량   PE {q_pe:.4f} Ah · NE {q_ne:.4f} Ah")
    print(f"★ 로딩비  N = Q_NE / Q_PE = **{N:.6f}**")
    print(f"  (Marongiu 는 `[인쇄]` \"normally bigger than one\" 이라고만 적었다.")
    print(f"   우리는 셀 기하에서 계산할 수 있다.)\n")

    def curve(lli, lam_pe, lam_ne, ne_type):
        try:
            ov = build_overrides(lli, lam_pe, lam_ne, "de", ne_type, b, d)
        except InfeasibleConditionError as e:
            return None, f"infeasible: {e}"
        r = run_one(cfg, ov, PROTOCOL)
        if not r.ok:
            return None, r.error
        c = extract_curves(r.solution)
        return c, None

    print("── n₁ 시험: {LAM_Ne,Li = δ}  vs  {LAM_Ne,De = δ, LLI = N·δ} ──")
    print("   (두 조건이 같은 곡선을 내면 n₁ 이 우리 셀에서도 성립한다)\n")
    rows, srows = [], []
    for delta in DELTAS:
        lli_eq = N * delta
        t0 = time.perf_counter()
        cA, eA = curve(0.0, 0.0, delta, "li")
        cB, eB = curve(lli_eq, 0.0, delta, "de")
        el = time.perf_counter() - t0
        tag = f"δ = {delta:.2f}"
        if cA is None or cB is None:
            print(f"   {tag}: 실패 — A={eA} · B={eB}")
            rows.append({"delta": delta, "lli_equiv": lli_eq,
                         "status": f"A:{eA} B:{eB}"})
            continue

        x = np.asarray(cA["x_norm"], float)
        vA = np.asarray(cA["v_full"], float)
        vB = np.interp(x, np.asarray(cB["x_norm"], float),
                       np.asarray(cB["v_full"], float))
        dv = np.abs(vA - vB) * 1e3
        qA, qB = float(cA["q_mah"]), float(cB["q_mah"])
        print(f"   {tag}  (LLI 등가 = {lli_eq:.5f})   [{el:.1f}s]")
        print(f"      용량   A(li) {qA:9.2f} mAh · B(de+LLI) {qB:9.2f} mAh"
              f"   상대차 {100*abs(qA-qB)/qA:7.4f} %")
        print(f"      곡선   평균|ΔV| {dv.mean():7.3f} mV · 최대|ΔV| {dv.max():7.3f} mV")
        rows.append({"delta": delta, "lli_equiv": lli_eq, "status": "ok",
                     "q_li_mah": qA, "q_de_lli_mah": qB,
                     "q_rel_diff_pct": 100 * abs(qA - qB) / qA,
                     "mean_abs_dv_mV": float(dv.mean()),
                     "max_abs_dv_mV": float(dv.max())})
        srows += [{"delta": delta, "x_norm": xx, "v_li": a, "v_de_lli": c}
                  for xx, a, c in zip(x, vA, vB)]

    # ── ★ 계수를 프레임에서 다시 유도한다 ─────────────────────────────────
    #   `li` 가 `de` 보다 더 빼는 리튬은 **재료가 제거되는 프레임에서 그 재료가
    #   쥐고 있던 양**이다. 우리 파이프라인은 열화를 **완방 프레임**에서 적용하고
    #   (`build_overrides` 의 "charge_first / 완방 프레임 통일"), 그 프레임에서
    #   음극은 사실상 비어 있다. 그래서 계수가 `N` 이 아니다.
    import pybamm
    bb = cfg["baseline"]
    pv = pybamm.ParameterValues(cfg["parameter_set"])
    A = pv["Electrode height [m]"] * pv["Electrode width [m]"]
    k = F_CONST * A / 3600.0
    L_ne, L_pe = pv["Negative electrode thickness [m]"], pv["Positive electrode thickness [m]"]
    li_ne_dis = k * L_ne * (d.ne_primary * bb["ne_primary_vf"]
                            + d.ne_secondary * bb["ne_secondary_vf"])
    n_tot = (k * L_ne * (bb["ne_primary_init_conc"] * bb["ne_primary_vf"]
                         + bb["ne_secondary_init_conc"] * bb["ne_secondary_vf"])
             + k * L_pe * bb["pe_init_conc"] * bb["pe_vf"])
    print("\n── ★ 계수를 프레임에서 다시 유도한다 ──")
    print(f"   완방 프레임에서 음극이 쥔 Li = {li_ne_dis:.6f} Ah")
    print(f"   총 재고 (완충 baseline)      = {n_tot:.4f} Ah")
    print(f"   z_gr(완방) = {d.ne_primary/bb['ne_primary_max_conc']:.6f}"
          f"   z_si(완방) = {d.ne_secondary/bb['ne_secondary_max_conc']:.6f}"
          f"   ← **음극이 거의 비어 있다**")
    for dd in DELTAS:
        eq = dd * li_ne_dis / n_tot
        print(f"   δ={dd:.2f}  올바른 LLI 등가 = **{eq:.6f}** ({100*eq:.4f} %)"
              f"   vs N·δ = {N*dd:.5f}   → **{N*dd/eq:.0f} 배 과대**")
        rows.append({"delta": dd, "status": "frame-corrected coefficient",
                     "lli_equiv": float(eq), "lli_equiv_N": float(N * dd),
                     "overestimate_factor": float(N * dd / eq)})

    # ── 대조군: n₁ 이 **아닌** 짝은 달라야 한다 (시험이 무의미하지 않다는 증거) ──
    print("\n── 대조군: LLI 등가를 바꿔 가며 (작을수록 맞다면 계수가 ≈0 이다) ──")
    delta = DELTAS[-1]
    cA, _ = curve(0.0, 0.0, delta, "li")
    for factor, tag in [(0.0, "LLI = 0"),
                        (delta * li_ne_dis / n_tot / (N * delta), "LLI = 프레임 보정값 ★"),
                        (0.5, "LLI = 0.5·N·δ"),
                        (1.0, "LLI = N·δ  (Dubarry 계수)")]:
        cB, eB = curve(N * delta * factor, 0.0, delta, "de")
        if cA is None or cB is None:
            print(f"   {tag}: 실패 {eB}")
            continue
        x = np.asarray(cA["x_norm"], float)
        dv = np.abs(np.asarray(cA["v_full"], float)
                    - np.interp(x, np.asarray(cB["x_norm"], float),
                                np.asarray(cB["v_full"], float))) * 1e3
        star = "  ← 가장 작다" if factor < 0.01 else ""
        print(f"   {tag:<22} 평균|ΔV| {dv.mean():8.3f} mV"
              f" · 최대 {dv.max():8.3f} mV{star}")
        rows.append({"delta": delta, "lli_equiv": N * delta * factor,
                     "status": f"control x{factor}",
                     "mean_abs_dv_mV": float(dv.mean()),
                     "max_abs_dv_mV": float(dv.max())})

    # ══ n₂ (PE 쪽) — 프레임 이론의 **예측 시험** ═══════════════════════════
    #   n₂ = (+1, −1, +1, 0, 0) ⟺ {LAM_Pe,li = ε} ≡ {LAM_Pe,de = ε, LLI = ε}
    #   Dubarry 의 계수는 **1** 이다 (로딩비가 아니라).
    #   프레임 이론의 예측: 완방 프레임에서 **양극은 거의 차 있으므로**
    #   (y₀ = 0.926) 계수가 1 에 가까울 것이다 — NE 와 정반대.
    li_pe_dis = k * L_pe * d.pe * bb["pe_vf"]
    coef_pe = li_pe_dis / n_tot
    print("\n══ n₂ (PE 쪽) — 프레임 이론의 예측 시험 ══")
    print(f"   완방 프레임에서 양극이 쥔 Li = {li_pe_dis:.4f} Ah / 총 재고 {n_tot:.4f} Ah")
    print(f"   y₀(완방) = {d.pe/bb['pe_max_conc']:.6f}  ← **양극은 거의 차 있다**")
    print(f"   ★ 예측 계수 = {coef_pe:.6f}   (Dubarry 의 n₂ 계수는 **1**)")
    print(f"   → NE 는 계수가 ~0 이었는데 PE 는 ~1 이어야 한다. 시험한다.\n")
    print(f"   {'ε':>6}{'LLI 등가':>12}{'평균|ΔV|':>12}{'최대|ΔV|':>12}")

    def curve_pe(lli, lam_pe, pe_type):
        try:
            ov = build_overrides(lli, lam_pe, 0.0, pe_type, "de", b, d)
        except InfeasibleConditionError as e:
            return None, f"infeasible: {e}"
        r = run_one(cfg, ov, PROTOCOL)
        if not r.ok:
            return None, r.error
        return extract_curves(r.solution), None

    for eps in DELTAS:
        cA, eA = curve_pe(0.0, eps, "li")
        if cA is None:
            print(f"   {eps:>6.2f}  A 실패: {eA}")
            continue
        xa_ = np.asarray(cA["x_norm"], float)
        va_ = np.asarray(cA["v_full"], float)
        for lli_eq, tag in [(0.0, "0 (보정 없음)"),
                            (coef_pe * eps, "프레임 예측 ★"),
                            (1.0 * eps, "Dubarry 계수 1")]:
            cB, eB = curve_pe(lli_eq, eps, "de")
            if cB is None:
                print(f"   {eps:>6.2f}{tag:>12}  B 실패: {eB}")
                continue
            dv = np.abs(va_ - np.interp(xa_, np.asarray(cB["x_norm"], float),
                                        np.asarray(cB["v_full"], float))) * 1e3
            print(f"   {eps:>6.2f}{tag:>14}{dv.mean():>12.3f}{dv.max():>12.3f}")
            rows.append({"delta": eps, "status": f"n2 PE · {tag}",
                         "lli_equiv": float(lli_eq),
                         "mean_abs_dv_mV": float(dv.mean()),
                         "max_abs_dv_mV": float(dv.max())})

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "pairs.csv", index=False)
    if srows:
        pd.DataFrame(srows).to_csv(OUT / "curves_summary.csv", index=False)
    print(f"\n산출물: {OUT}/  (pairs.csv · curves_summary.csv)")


if __name__ == "__main__":
    main()
