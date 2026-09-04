#!/usr/bin/env python3
"""Phase 1i — Mohtat 의 `Σ` 를 **모드 좌표로 전파한다**: 22p 삼중항의 오차막대.

## 왜 이 계산인가 — 한 줄이 비어 있다

Mohtat 2019 (*J. Power Sources* 427, 101–111) 는 이 계보에서 **유일하게** 제약
Cramér–Rao 하한을 세운다:

    𝓘_f = Sᵀ E⁻¹ S                              … (29)
    Σ ≥ 𝒪 (𝒪ᵀ 𝓘_f 𝒪)⁻¹ 𝒪ᵀ                       … (32)   𝒪 = null(∂f/∂θ)
    σ_θ = sqrt(diag[Σ])                         … (33)

그런데 **(33) 에서 `diag` 를 취하는 순간 비대각이 버려진다.** 그리고 그의 파라미터는
`θ = [x₁₀₀, y₁₀₀, C_n, C_p]` 이라 모드가 아니다 — `LLI`·`LAM` 은 그 논문 §5·§6·§7
에 **한 번도 안 나온다** (우리 위키가 두 번 독립으로 전수).

모드 사상은 같은 논문 식 (16)(20) 에 있으므로 전파는 **한 줄**이다:

    σ²_mode = ∇gᵀ Σ ∇g

**인쇄돼 있지 않다.** 그 한 줄이 이 스크립트다. 다만 우리는 그의 `θ` 대신 **우리
모드 좌표에서 직접** 잰다 — Phase 1c/1h 의 Jacobian `J` 가 이미 `∂V/∂(LLI, LAM_PE,
LAM_NE)` 이므로, 모드가 **파라미터 자리에 직접** 있다. 그래서 전파가 필요 없고
`Σ` 를 바로 모드 좌표에서 얻는다. (전파식이 필요한 것은 Mohtat 의 좌표이지
우리 좌표가 아니다 — 그것이 우리 매개화가 이 물음에 더 곧바로 닿는 이유다.)

## 무엇을 내나

등분산 가우시안 잡음 `σ` 아래에서

    𝓘 = JᵀJ / σ²        Σ = σ² (JᵀJ)⁻¹        σ_i = sqrt(Σ_ii)

네 판:

| 판 | 뜻 |
|---|---|
| **자유** | 곡선만 관측. 제약 없음 (지금 우리 파이프라인의 자리) |
| **관측추가** | Mohtat 식 처방 — 끝점 2개를 관측에 더한다 `[J; G]` |
| **제약** | Birkl/Lin 식 처방 — 컷오프 등식을 **제약**으로 (식 32, `𝒪 = null(G)`) |
| **상관** | 위 셋 각각의 **비대각**. 이 계보가 한 번도 인쇄하지 않은 것 |

⚠ **이것은 하한이지 우리 추정기의 성능이 아니다.** `degradation-degeneracy` 의
복원 실패율과 **섞어 인용하면 안 된다** (Phase 1c 한계 (d) 와 같은 경계).

출력: results/phase1i/{errorbars.csv, correlation.csv} + stdout. **CSV 가 정본이다.**
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1i"

H = 0.02                       # Phase 1c/1g/1h 와 같은 전방차분 스텝
LO, HI = 0.02, 0.98            # Phase 1c/1g/1h 와 같은 관측 구간
MODES = ["LLI", "LAM_PE", "LAM_NE"]
ONES = np.ones(3) / np.sqrt(3.0)

# 우리 격자가 실제로 쓰는 잡음층 (Phase 1c 가 실측한 σ)
SIGMAS = {"σ = 1 mV": 1.002e-3, "σ = 5 mV": 5.006e-3}

OPS = [("pristine", 0.00, 0.00, 0.00),
       ("22p 근방", 0.16, 0.12, 0.12)]


def ang(u, v):
    c = abs(float(u @ v)) / (np.linalg.norm(u) * np.linalg.norm(v))
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n  원자료는 gitignored 다.")

    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "x_norm", "v_full"])
    d0 = df[df.noise == 0]

    key, endp = {}, {}
    for c, g in d0.groupby("cond_id", sort=False):
        k = (round(g.lli.iloc[0], 4), round(g.lam_pe.iloc[0], 4),
             round(g.lam_ne.iloc[0], 4))
        key[k] = c
        gs = g.sort_values("x_norm")
        x, v = gs.x_norm.to_numpy(float), gs.v_full.to_numpy(float)
        endp[k] = (float(np.interp(0.0, x, v)), float(np.interp(1.0, x, v)))

    ref = d0[d0.cond_id == next(iter(key.values()))].sort_values("x_norm")
    xa = ref.x_norm.to_numpy(float)
    xs = xa[(xa >= LO) & (xa <= HI)]

    cache = {}

    def curve(k):
        if k not in key:
            return None
        if k not in cache:
            g = d0[d0.cond_id == key[k]].sort_values("x_norm")
            cache[k] = np.interp(xs, g.x_norm.to_numpy(float),
                                 g.v_full.to_numpy(float))
        return cache[k]

    def rk(l, p, n):
        return (round(l, 4), round(p, 4), round(n, 4))

    rows, crows = [], []
    for label, l0, p0, n0 in OPS:
        base = curve(rk(l0, p0, n0))
        axes = [(l0 + H, p0, n0), (l0, p0 + H, n0), (l0, p0, n0 + H)]
        if base is None or any(curve(rk(*a)) is None for a in axes):
            print(f"[건너뜀] {label}: 격자에 없다")
            continue

        J = np.column_stack([(curve(rk(*a)) - base) / H for a in axes])
        e0 = endp[rk(l0, p0, n0)]
        G = np.array([[(endp[rk(*a)][i] - e0[i]) / H for a in axes]
                      for i in range(2)])                      # 2×3

        # 제약 접공간 (3 − 2 = 1 차원)
        _, _, Vt = np.linalg.svd(G)
        O = Vt[2:].T                                           # 3×1

        A = J.T @ J
        A_aug = A + G.T @ G                                    # 끝점 2개를 관측에 추가
        print(f"══ {label} (LLI {l0} · LAM_PE {p0} · LAM_NE {n0}) ══"
              f"   관측 {J.shape[0]}점")
        print(f"   제약 접공간 방향 𝒪 = {np.round(O[:, 0], 4)}"
              f"   ∠ to (1,1,1) = {ang(O[:, 0], ONES):.2f}°")

        for sname, sig in SIGMAS.items():
            S_free = sig ** 2 * np.linalg.inv(A)
            S_aug = sig ** 2 * np.linalg.inv(A_aug)
            # Mohtat 식 (32) — 제약 CRB. 여기서는 1차원이라 스칼라 역수.
            S_con = sig ** 2 * (O @ np.linalg.inv(O.T @ A @ O) @ O.T)

            print(f"\n   ── {sname} ──")
            print(f"   {'':<9}{'자유':>12}{'관측추가':>12}{'제약':>12}   (%p, 1σ)")
            for i, m in enumerate(MODES):
                print(f"   {m:<9}{100*np.sqrt(S_free[i,i]):>12.3f}"
                      f"{100*np.sqrt(S_aug[i,i]):>12.3f}"
                      f"{100*np.sqrt(S_con[i,i]):>12.3f}")

            # ── 비대각 — 이 계보가 인쇄하지 않은 것 ──────────────────────
            d = np.sqrt(np.diag(S_free))
            R = S_free / np.outer(d, d)
            # 자릿수 주의: 두 동작점의 ρ(LLI,LAM_PE) 가 4자리까지 같다
            # (0.986028 vs 0.986004). 4자리로 찍으면 같은 값처럼 보여 버그로
            # 오해하게 된다 — 6자리로 찍는다. (ρ 는 σ 에 무관하다: 약분된다.)
            print(f"   상관 (자유·σ 무관)  ρ(LLI,LAM_PE) = {R[0,1]:+.6f}"
                  f"   ρ(LLI,LAM_NE) = {R[0,2]:+.6f}"
                  f"   ρ(LAM_PE,LAM_NE) = {R[1,2]:+.6f}")

            # 오차 타원체의 최장축 — 가장 못 정하는 조합
            w, V = np.linalg.eigh(S_free)
            ax = V[:, -1] / np.linalg.norm(V[:, -1])
            if ax.sum() < 0:
                ax = -ax
            frac = w[-1] / w.sum()
            print(f"   최장축 {np.round(ax,4)}  길이 {100*np.sqrt(w[-1]):.3f} %p"
                  f"   ∠ to (1,1,1) = {ang(ax, ONES):.2f}°")
            print(f"   축 길이 (%p)  {100*np.sqrt(w[-1]):.3f} / "
                  f"{100*np.sqrt(w[1]):.3f} / {100*np.sqrt(w[0]):.3f}"
                  f"   → 총 분산의 **{100*frac:.2f} %** 가 최장축 하나에 있다")
            print(f"   `[해석]` 그래서 위 세 오차막대는 독립한 셋이 아니라"
                  f" **한 방향의 그림자 셋**이다.")

            for i, m in enumerate(MODES):
                rows.append({"op": label, "sigma": sname, "mode": m,
                             "sd_free_pp": 100 * np.sqrt(S_free[i, i]),
                             "sd_augmented_pp": 100 * np.sqrt(S_aug[i, i]),
                             "sd_constrained_pp": 100 * np.sqrt(S_con[i, i])})
            crows.append({"op": label, "sigma": sname,
                          "rho_LLI_LAM_PE": R[0, 1], "rho_LLI_LAM_NE": R[0, 2],
                          "rho_LAM_PE_LAM_NE": R[1, 2],
                          "major_axis_len_pp": 100 * np.sqrt(w[-1]),
                          "minor_axis_len_pp": 100 * np.sqrt(w[0]),
                          **{f"major_axis_{m}": ax[i] for i, m in enumerate(MODES)},
                          "major_axis_angle_ones_deg": ang(ax, ONES),
                          "major_axis_variance_frac": float(frac)})

        # ── 제약을 걸었을 때의 **편향** — 정밀도와 맞바꾸는 것 ─────────────
        # Phase 1h: 컷오프 등식은 참값에서 성립하지 않는다 (끝점 전압이 조건에
        # 따라 127 mV / 54 mV 흔들린다). 컷오프 상수를 pristine 에서 잡고 이
        # 동작점에 그대로 얹으면 잔차 r 이 남고, 제약 추정기는 그것을 **모드로**
        # 떠넘긴다: 최소노름 해 Δθ = G⁺ r.
        e_ref = endp[rk(0.0, 0.0, 0.0)]
        r = np.array([endp[rk(l0, p0, n0)][i] - e_ref[i] for i in range(2)])
        bias = np.linalg.pinv(G) @ r
        print(f"   ── 제약의 대가 (편향) ──")
        print(f"   컷오프 상수를 pristine 에서 잡으면 이 동작점의 잔차는"
              f" {1e3*r[0]:+.1f} mV · {1e3*r[1]:+.1f} mV")
        print(f"   제약 추정기가 그것을 모드로 떠넘긴 양 (최소노름)"
              f" {np.round(100*bias, 3)} %p  ‖·‖ = {100*np.linalg.norm(bias):.3f} %p")
        for sname, sig in SIGMAS.items():
            S_con = sig ** 2 * (O @ np.linalg.inv(O.T @ A @ O) @ O.T)
            sd = 100 * np.sqrt(np.max(np.diag(S_con)))
            if sd > 0:
                print(f"     {sname}: 편향/최대 σ = "
                      f"**{100*np.linalg.norm(bias)/sd:.0f} 배**")
        rows.append({"op": label, "sigma": "—", "mode": "(제약 편향 ‖Δθ‖)",
                     "sd_free_pp": np.nan, "sd_augmented_pp": np.nan,
                     "sd_constrained_pp": 100 * float(np.linalg.norm(bias))})
        print()

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "errorbars.csv", index=False)
    pd.DataFrame(crows).to_csv(OUT / "correlation.csv", index=False)
    print(f"산출물: {OUT}/  (errorbars.csv · correlation.csv)")
    print("\n⚠ 이것은 **하한**이다. 추정기가 이 값을 달성한다는 뜻이 아니고,")
    print("  degradation-degeneracy 의 복원 결과와 **섞어 인용하면 안 된다**.")


if __name__ == "__main__":
    main()
