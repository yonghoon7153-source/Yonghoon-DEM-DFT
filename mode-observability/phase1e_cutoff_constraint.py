#!/usr/bin/env python3
"""Phase 1e — 컷오프 등식 제약이 **약한 방향을 죽이는가, 강한 방향을 죽이는가**.

이것이 `syntheses/mode-identifiability-unmeasured-lineage.md` 의 Gap 5 이고,
Counter-argument (d) 의 판정이다.

배경. Lin & Khoo 2024 는 Birkl/Mohtat 식 4-파라미터 창 매개화를 `[인쇄]`
"non-independent parameters, of which the **redundancy** complicates their
estimation" 이라고 비판하고, 컷오프 등식으로 자유도를 소거하는 쪽을 지지한다.
그런데 우리 Phase 1d 실측은 유효 rank 가 **2 가 아니라 4** 였다 (σ3/σ1 ≈ 0.05,
σ4/σ1 ≈ 0.03 — 작지만 0 이 아니다).

그러면 물음이 하나 남는다: **그 제약을 걸면 무엇이 사라지는가.**

  · 제약이 σ3·σ4 방향을 겨냥한다  →  Lin 이 옳다. 여분을 지우는 것이다.
  · 제약이 σ1·σ2 방향을 건드린다  →  제약은 여분이 아니라 **정보**를 버린다.

판정 방법. 컷오프 등식 둘의 gradient `G = [∇g₁; ∇g₂]` 를 구하고,

  1. `span{∇g₁,∇g₂}` 와 `span{v₃,v₄}` 사이의 **주각(principal angle)** 을 잰다.
     작으면 제약이 약한 방향을 정조준한 것이다.
  2. 제약의 **접공간**(`null(G)`, 2차원)으로 `J` 를 제한해 특이값을 다시 본다.
     남는 둘이 원래의 σ1·σ2 에 가까우면 "여분만 지웠다" 가 성립한다.

제약의 정의. 우리 좌표에서 컷오프는 관측 구간의 양 끝이다 — 재구성 곡선이
`x_min`·`x_max` 에서 정해진 전압을 갖는다는 등식. 그래서
`g₁(p) = U_full(p; x_min)`, `g₂(p) = U_full(p; x_max)` 의 gradient 를 쓴다
(등식의 우변은 상수이므로 gradient 에 안 들어간다).

입력: degradation-degeneracy/results/grid_curves_v4/curves.parquet (**읽기 전용**)
출력: results/phase1e/{angles.csv, constrained_spectrum.csv} + stdout.
  **그 파일이 정본이다** — 문서에 적힌 숫자는 사본이다.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

from src.fitting import (  # noqa: E402  (읽기 전용 재사용)
    build_reference_interps, extract_reference, modes_to_params, reconstruct)

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1e"
PNAMES = ["alpha_PE", "beta_PE", "alpha_NE", "beta_NE"]
STEP = 5e-3          # Phase 1d 의 대표 스텝과 같게 (그 표와 직접 대조하려고)


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n  원자료는 gitignored 다.")
    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah",
        "x_norm", "v_pe", "v_ne", "v_full"])
    ref = extract_reference(df)
    f_pe, f_ne = build_reference_interps("grid", {
        "x": ref.x_norm.to_numpy(float),
        "pe": ref.v_pe.to_numpy(float),
        "ne": ref.v_ne.to_numpy(float)})
    x = ref.x_norm.to_numpy(float)
    q0 = float(ref.q_mah.iloc[0])

    def vfull(p):
        _, _, full = reconstruct(np.asarray(p, float), f_pe, f_ne, x)
        return full

    def jac(p0, h=STEP):
        cols, ok = [], np.isfinite(vfull(p0))
        for i in range(4):
            pp, pm = np.array(p0, float), np.array(p0, float)
            pp[i] += h
            pm[i] -= h
            vp, vm = vfull(pp), vfull(pm)
            ok &= np.isfinite(vp) & np.isfinite(vm)
            cols.append((vp - vm) / (2 * h))
        return np.column_stack(cols), ok

    uniq = df[df.noise == 0][["lli", "lam_pe", "lam_ne", "q_mah"]].drop_duplicates()

    def q_at(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else float(r.q_mah.iloc[0])

    OUT.mkdir(parents=True, exist_ok=True)
    arows, srows = [], []
    print(f"입력: {CURVES}\nreference {len(x)}점 · q0 {q0:.2f} mAh · 스텝 {STEP:.0e}\n")

    for label, lli, lam_pe, lam_ne in [("pristine", 0.0, 0.0, 0.0),
                                       ("22p 근방", 0.16, 0.12, 0.12)]:
        q = q_at(lli, lam_pe, lam_ne)
        if q is None:
            print(f"[건너뜀] {label} 격자에 없음")
            continue
        p0 = modes_to_params(lam_pe, lam_ne, lli, q / q0)
        J, ok = jac(p0)
        idx = np.flatnonzero(ok)
        Jv = J[ok]
        U, S, Vt = np.linalg.svd(Jv, full_matrices=False)

        # 컷오프 = 관측 창의 양 끝. 그 두 점에서의 gradient 가 등식 제약의 gradient 다.
        G = np.vstack([J[idx[0]], J[idx[-1]]])           # 2×4
        Qg, _ = np.linalg.qr(G.T)                        # span{∇g₁,∇g₂} 정규직교 기저
        Qw, _ = np.linalg.qr(Vt[2:].T)                   # span{v₃,v₄}
        Qs, _ = np.linalg.qr(Vt[:2].T)                   # span{v₁,v₂}
        ang_weak = np.degrees(np.arccos(np.clip(
            np.linalg.svd(Qg.T @ Qw, compute_uv=False), -1, 1)))
        ang_strong = np.degrees(np.arccos(np.clip(
            np.linalg.svd(Qg.T @ Qs, compute_uv=False), -1, 1)))

        # 제약의 접공간으로 제한했을 때 남는 특이값
        Nt = np.linalg.svd(G)[2][2:].T                    # null(G), 4×2
        Sc = np.linalg.svd(Jv @ Nt, compute_uv=False)

        print(f"══ {label} ══  유효점 {int(ok.sum())}")
        print(f"   자유 특이값      {np.array2string(S, precision=4)}  (cond {S[0]/S[-1]:.1f})")
        print(f"   v₃ = {np.array2string(Vt[2], precision=3)}")
        print(f"   v₄ = {np.array2string(Vt[3], precision=3)}   ← 가장 약한 방향")
        print(f"   주각: 제약 vs 약한쌍{{v₃,v₄}}  {np.round(ang_weak,1)}°")
        print(f"         제약 vs 강한쌍{{v₁,v₂}}  {np.round(ang_strong,1)}°")
        print(f"   제약 접공간에 제한한 특이값 {np.array2string(Sc, precision=4)}"
              f"  → 원래 σ1·σ2 대비 {Sc[0]/S[0]:.3f} · {Sc[1]/S[1]:.3f}")
        print()

        arows.append({"point": label,
                      **{f"v3_{n}": v for n, v in zip(PNAMES, Vt[2])},
                      **{f"v4_{n}": v for n, v in zip(PNAMES, Vt[3])},
                      "angle_weak_1": ang_weak[0], "angle_weak_2": ang_weak[1],
                      "angle_strong_1": ang_strong[0], "angle_strong_2": ang_strong[1]})
        srows.append({"point": label,
                      **{f"sv{i+1}": S[i] for i in range(4)},
                      "cons_sv1": Sc[0], "cons_sv2": Sc[1],
                      "cons_sv1_over_sv1": Sc[0]/S[0], "cons_sv2_over_sv2": Sc[1]/S[1]})

    pd.DataFrame(arows).to_csv(OUT / "angles.csv", index=False)
    pd.DataFrame(srows).to_csv(OUT / "constrained_spectrum.csv", index=False)
    print("판정 규칙 — 제약이 **약한 쌍**에 가까우면(주각 작음) 여분을 지운 것이고,")
    print("            **강한 쌍**에 가까우면 정보를 버린 것이다.")
    print(f"\n산출물: {OUT}/  (angles.csv · constrained_spectrum.csv)")


if __name__ == "__main__":
    main()
