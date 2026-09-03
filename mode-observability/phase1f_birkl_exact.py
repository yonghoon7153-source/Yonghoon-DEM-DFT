#!/usr/bin/env python3
"""Phase 1f — Birkl 2017 의 **실제** 등식을 우리 좌표에 옮겨 3-파라미터 판을 만든다.

Phase 1e 는 컷오프 제약을 **대리물**로 놓고 (재구성 곡선이 관측 창 양 끝에서
정해진 전압) 판정했고, 그 대리성을 한계로 신고했다. 이 스크립트가 그것을 닫는다.

## 먼저 — 대리물이 아니었다

Birkl 식 (11)(12) 을 그대로 옮기면:

    E_high − Ê_PE(x_PE,EoC) + Ê_NE(x_NE,EoC) = 0        … (11)
    E_low  − Ê_PE(x_PE,EoD) + Ê_NE(x_NE,EoD) = 0        … (12)

full-cell = PE − NE 이므로 이 둘은 글자 그대로 **`U_full(EoC) = E_high`,
`U_full(EoD) = E_low`** 다. Phase 1e 가 쓴 제약과 **형태가 같다.** 즉 그 한계
신고는 과했고, Phase 1e 의 주각 판정은 그대로 유효하다.

## 그러면 새로 물을 것은 하나 남는다

Birkl 은 그 등식을 **제약으로 얹지 않는다.** 미지수 5개
`(LLI, LAM_PE, LAM_NE, Δx_EoC, Δx_EoD)` 중 **뒤 둘을 등식으로 풀어 소거**해
**자유 파라미터 3개**짜리 역문제를 만든다 (식 7–10 + 11–12). 그것은 우리
4-파라미터 창 문제와 **다른 문제**다.

    우리   : p = [α_PE, β_PE, α_NE, β_NE]         자유 4 · 제약 0
    Birkl : θ = [LLI, LAM_PE, LAM_NE]            자유 3 · Δx 둘은 등식으로 소거

이 스크립트는 **Birkl 판을 실제로 구성해** 그 Jacobian 스펙트럼을 재고, 우리
4-파라미터 판(Phase 1d)·모드 좌표 판(Phase 1c)과 나란히 놓는다. 위키가
`[해석]` "Birkl 의 3-파라미터 컷오프 제약 버전을 그 격자에 얹으면 논문이 비워둔
자리가 채워진다" 고 적어 둔 그 계산이다.

## 좌표 대응

우리 재구성은 `U_PE(x) = f_PE_ref((x − β_PE)/α_PE)`, `x ∈ [0,1]` 이 셀 용량축이고
`x = 0` 이 EoC(만충), `x = 1` 이 EoD 다. Birkl 의 전극 화학량론 `x_PE,·` 는 곧
우리 `s = (x − β)/α` 이므로:

    x_PE,EoC = −β_PE/α_PE          x_PE,EoD = (1 − β_PE)/α_PE
    → α_PE = 1/(x_PE,EoD − x_PE,EoC),  β_PE = −x_PE,EoC · α_PE     (NE 도 같음)

pristine 에서 식 (7)–(10) 은 `Δx = 0` 일 때 `x_PE,EoC = 0`, `x_PE,EoD = 1` 을
주므로 `α = 1, β = 0` 이 되어 우리 규약과 정확히 맞는다 (검산으로 확인한다).

`E_high`·`E_low` 는 4.2/2.7 V 를 쓰지 않는다 — 화학이 다르다. **우리 reference
곡선 자신의 양 끝 전압**을 쓴다. 그래야 pristine 이 `Δx = 0` 으로 풀린다.

## 등식이 분리된다

식 (11) 에는 `Δx_EoC` 만, (12) 에는 `Δx_EoD` 만 들어간다. 그래서 2×2 연립이
아니라 **1차원 근찾기 두 번**이다 (Birkl 은 "linear system" 이라 적지만, 반쪽셀
OCP 가 비선형이므로 실제로는 비선형 스칼라 방정식 둘이다 — 이것도 확인한다).

입력: degradation-degeneracy/results/grid_curves_v4/curves.parquet (**읽기 전용**)
출력: results/phase1f/{spectrum.csv, delta_x.csv} + stdout. **CSV 가 정본이다.**
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

from src.fitting import (  # noqa: E402
    build_reference_interps, extract_reference, modes_to_params, reconstruct)

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1f"
MODES = ["LLI", "LAM_PE", "LAM_NE"]


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n  원자료는 gitignored 다.")
    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah",
        "x_norm", "v_pe", "v_ne", "v_full"])
    ref = extract_reference(df)
    x = ref.x_norm.to_numpy(float)
    f_pe, f_ne = build_reference_interps("grid", {
        "x": x, "pe": ref.v_pe.to_numpy(float), "ne": ref.v_ne.to_numpy(float)})
    q0 = float(ref.q_mah.iloc[0])

    # 컷오프 상수 = reference 곡선 자신의 양 끝 (4.2/2.7 V 아님 — 화학이 다르다)
    v_full_ref = ref.v_full.to_numpy(float)
    E_high, E_low = float(v_full_ref[0]), float(v_full_ref[-1])
    print(f"입력: {CURVES}")
    print(f"reference {len(x)}점 · q0 {q0:.2f} mAh")
    print(f"컷오프 상수 (reference 자신의 양 끝): E_high {E_high:.4f} V · "
          f"E_low {E_low:.4f} V\n")

    # ── Birkl 식 (7)–(10) ────────────────────────────────────────────────
    def stoich(lli, lam_pe, lam_ne, dx_eoc, dx_eod):
        return (dx_eoc / (1 - lam_pe),                                  # (7)
                (dx_eod + 1 - lli + lam_pe) / (1 - lam_pe),             # (8)
                (dx_eoc + lli - lam_ne) / (1 - lam_ne),                 # (9)
                dx_eod / (1 - lam_ne))                                  # (10)

    def g_eoc(dx, lli, lam_pe, lam_ne):
        p, _, n, _ = stoich(lli, lam_pe, lam_ne, dx, 0.0)
        return E_high - (float(f_pe(p)) - float(f_ne(n)))               # (11)

    def g_eod(dx, lli, lam_pe, lam_ne):
        _, p, _, n = stoich(lli, lam_pe, lam_ne, 0.0, dx)
        return E_low - (float(f_pe(p)) - float(f_ne(n)))                # (12)

    def solve_dx(lli, lam_pe, lam_ne, lo=-0.45, hi=0.45):
        """식 (11)(12) 를 각각 1차원으로 푼다 — 두 식이 분리되기 때문."""
        out = []
        for g in (g_eoc, g_eod):
            a, b = lo, hi
            fa, fb = g(a, lli, lam_pe, lam_ne), g(b, lli, lam_pe, lam_ne)
            if fa * fb > 0:
                return None                       # 부호 변화 없음 → 해 없음
            out.append(brentq(g, a, b, args=(lli, lam_pe, lam_ne), xtol=1e-12))
        return tuple(out)

    def birkl_params(theta):
        """θ = (LLI, LAM_PE, LAM_NE) → 우리 창 좌표 p (등식으로 Δx 를 소거한 뒤)."""
        lli, lam_pe, lam_ne = theta
        dx = solve_dx(lli, lam_pe, lam_ne)
        if dx is None:
            return None, None
        pe_c, pe_d, ne_c, ne_d = stoich(lli, lam_pe, lam_ne, *dx)
        a_pe = 1.0 / (pe_d - pe_c)
        a_ne = 1.0 / (ne_d - ne_c)
        return np.array([a_pe, -pe_c * a_pe, a_ne, -ne_c * a_ne]), dx

    def vfull(p):
        _, _, full = reconstruct(np.asarray(p, float), f_pe, f_ne, x)
        return full

    # ── 검산 1: pristine 이 Δx = 0 · α = 1 · β = 0 으로 풀리는가 ────────────
    p_pris, dx_pris = birkl_params((0.0, 0.0, 0.0))
    print("검산 — pristine 이 우리 규약과 맞는가")
    print(f"   Δx = ({dx_pris[0]:+.3e}, {dx_pris[1]:+.3e})   (0 이어야 한다)")
    print(f"   p  = {np.array2string(p_pris, precision=6)}   "
          f"([1,0,1,0] 이어야 한다)\n")

    # ── 검산 2: 두 식이 정말 분리되는가 (Birkl 은 'linear system' 이라 적는다) ──
    d = 0.02
    base = solve_dx(0.05, 0.05, 0.05)
    only_c = brentq(g_eoc, -0.45, 0.45, args=(0.05, 0.05, 0.05), xtol=1e-12)
    print("검산 — 식 (11) 이 Δx_EoD 와 무관한가 (분리 확인)")
    print(f"   연립으로 푼 Δx_EoC {base[0]:+.9f} · 단독으로 푼 것 {only_c:+.9f}"
          f"  차이 {abs(base[0]-only_c):.2e}\n")

    # ── 스펙트럼 ──────────────────────────────────────────────────────────
    OUT.mkdir(parents=True, exist_ok=True)
    srows, drows = [], []
    uniq = df[df.noise == 0][["lli", "lam_pe", "lam_ne", "q_mah"]].drop_duplicates()

    def q_at(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else float(r.q_mah.iloc[0])

    for label, lli, lam_pe, lam_ne in [("pristine", 0.0, 0.0, 0.0),
                                       ("22p 근방", 0.16, 0.12, 0.12)]:
        th = np.array([lli, lam_pe, lam_ne])
        p_b, dx = birkl_params(tuple(th))
        if p_b is None:
            print(f"[건너뜀] {label} — 컷오프 등식에 해가 없다")
            continue

        # Birkl 판: U_full 을 θ 로 미분 (Δx 는 매번 다시 푼다 = 제약이 살아 있다)
        h, cols, ok = 2e-3, [], np.isfinite(vfull(p_b))
        for i in range(3):
            tp, tm = th.copy(), th.copy()
            tp[i] += h
            tm[i] -= h
            pp, _ = birkl_params(tuple(tp))
            pm, _ = birkl_params(tuple(tm))
            vp, vm = vfull(pp), vfull(pm)
            ok &= np.isfinite(vp) & np.isfinite(vm)
            cols.append((vp - vm) / (2 * h))
        Jb = np.column_stack(cols)[ok]
        Sb = np.linalg.svd(Jb, compute_uv=False)

        # 대조: 같은 동작점의 우리 4-파라미터 판 (Phase 1d 와 같은 스텝)
        q = q_at(lli, lam_pe, lam_ne)
        p_us = modes_to_params(lam_pe, lam_ne, lli, q / q0)
        h2, cols2, ok2 = 5e-3, [], np.isfinite(vfull(p_us))
        for i in range(4):
            pp, pm = p_us.copy(), p_us.copy()
            pp[i] += h2
            pm[i] -= h2
            vp, vm = vfull(pp), vfull(pm)
            ok2 &= np.isfinite(vp) & np.isfinite(vm)
            cols2.append((vp - vm) / (2 * h2))
        Su = np.linalg.svd(np.column_stack(cols2)[ok2], compute_uv=False)

        print(f"══ {label} ══")
        print(f"   Birkl 이 푼 Δx = ({dx[0]:+.6f}, {dx[1]:+.6f})")
        print(f"   그 θ 가 주는 창 p = {np.array2string(p_b, precision=5)}")
        print(f"   우리 규약의 창  p = {np.array2string(p_us, precision=5)}")
        print(f"   Birkl 3-파라미터 특이값 {np.array2string(Sb, precision=4)}"
              f"  cond {Sb[0]/Sb[-1]:8.2f}")
        print(f"   우리 4-파라미터 특이값  {np.array2string(Su, precision=4)}"
              f"  cond {Su[0]/Su[-1]:8.2f}")
        print()

        srows.append({"point": label,
                      **{f"birkl_sv{i+1}": Sb[i] for i in range(3)},
                      "birkl_cond": Sb[0] / Sb[-1],
                      **{f"ours_sv{i+1}": Su[i] for i in range(4)},
                      "ours_cond": Su[0] / Su[-1]})
        drows.append({"point": label, "LLI": lli, "LAM_PE": lam_pe,
                      "LAM_NE": lam_ne, "dx_eoc": dx[0], "dx_eod": dx[1],
                      **dict(zip(["a_pe", "b_pe", "a_ne", "b_ne"], p_b)),
                      **dict(zip(["us_a_pe", "us_b_pe", "us_a_ne", "us_b_ne"], p_us))})

    pd.DataFrame(srows).to_csv(OUT / "spectrum.csv", index=False)
    pd.DataFrame(drows).to_csv(OUT / "delta_x.csv", index=False)
    print("대조 — Phase 1c 의 모드 좌표(제약 없음) 특이값 0.689 / 2.786 / 12.571 · cond 18.2")
    print(f"\n산출물: {OUT}/  (spectrum.csv · delta_x.csv)")


if __name__ == "__main__":
    main()
