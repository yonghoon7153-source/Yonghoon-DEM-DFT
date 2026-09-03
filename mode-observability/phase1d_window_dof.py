#!/usr/bin/env python3
"""Phase 1d — 우리 4-파라미터 창 모델의 **유효 자유도**를 잰다 (점검 B1).

질문:

  Lin & Khoo 2024 은 SOC 정규화 곡선의 **형상 자유도가 정확히 2** 라고 하고,
  그래서 Birkl/Mohtat 처럼 전극 창을 **4개 파라미터 + 제약**으로 매개화하는
  방식을 `[인쇄]` "non-independent parameters, of which the **redundancy**
  complicates their estimation" 이라고 지목한다.

  우리 fitting 은 `p = [α_PE, β_PE, α_NE, β_NE]` **4개**를 맞추고
  (`degradation-degeneracy/src/fitting.py`), 컷오프 등식 제약이 **없다.**
  그러면 우리가 관측한 degeneracy 의 일부는 **물리가 아니라 좌표 선택**일 수
  있다. Phase 1c 는 모드 좌표(3개)에서 조건수 18.2 를 실측했다 — 같은 곡선을
  창 좌표(4개)에서 보면 얼마인가.

  이것이 `wiki/questions/22p-physics-or-degeneracy.md` 의 점검 B1 이고,
  대답은 `∂v_full/∂p` 의 **특이값 스펙트럼**이다.

왜 이 계산이 값싼가: 정방향이 PyBaMM 이 아니라 **보간뿐**이다
(`fitting.reconstruct` = `windowed_curve` 두 번 + 뺄셈). 시뮬레이션이 없다.

입력: degradation-degeneracy/results/grid_curves_v4/curves.parquet (**읽기 전용**)
  — reference 조건(모든 모드 0, noise 0)의 반쪽전지 곡선으로 보간자를 만들고,
  `src.fitting` 의 production 함수를 그대로 import 해서 쓴다. RUN_SCOPE 를
  건드리지 않으므로 봉인 산출물과 게이트 대상 code identity 는 안 움직인다.

출력: results/phase1d/{spectrum.csv, vectors.csv} + stdout.
  **그 파일이 정본이다** — 문서·위키에 적힌 숫자는 사본이다.
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
OUT = HERE / "results" / "phase1d"

PNAMES = ["alpha_PE", "beta_PE", "alpha_NE", "beta_NE"]
# 창 좌표는 스케일이 서로 다르다 (α ≈ 1, β ≈ 0). 같은 절대 스텝을 주면
# 특이값 비교가 스텝 선택의 산물이 되므로 **네 축에 같은 스텝**을 쓰고,
# 그 스텝이 결론을 바꾸지 않는지 아래에서 세 값으로 확인한다.
STEPS = [2e-3, 5e-3, 1e-2]


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n  원자료는 gitignored 다.")
    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah",
        "x_norm", "v_pe", "v_ne", "v_full"])

    ref = extract_reference(df)
    grid_ref = {"x": ref.x_norm.to_numpy(float),
                "pe": ref.v_pe.to_numpy(float),
                "ne": ref.v_ne.to_numpy(float)}
    f_pe, f_ne = build_reference_interps("grid", grid_ref)
    x = grid_ref["x"]
    q0 = float(ref.q_mah.iloc[0])

    def vfull(p):
        _, _, full = reconstruct(np.asarray(p, float), f_pe, f_ne, x)
        return full

    def jac(p0, h):
        """전방/후방 중앙차분. 창 밖 NaN 이 생기는 점은 **전 열에서** 버린다."""
        cols, ok = [], np.isfinite(vfull(p0))
        for i in range(4):
            pp, pm = np.array(p0, float), np.array(p0, float)
            pp[i] += h
            pm[i] -= h
            vp, vm = vfull(pp), vfull(pm)
            ok &= np.isfinite(vp) & np.isfinite(vm)
            cols.append((vp - vm) / (2 * h))
        J = np.column_stack(cols)[ok]
        return J, int(ok.sum())

    # 동작점 둘 — pristine 과 22p 근방 (Phase 1 이 쓴 것과 같은 격자점)
    uniq = df[df.noise == 0][["cond_id", "lli", "lam_pe", "lam_ne", "q_mah"]].drop_duplicates()

    def q_at(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else float(r.q_mah.iloc[0])

    points = [("pristine", 0.0, 0.0, 0.0), ("22p 근방", 0.16, 0.12, 0.12)]
    OUT.mkdir(parents=True, exist_ok=True)
    srows, vrows = [], []

    print(f"입력: {CURVES}")
    print(f"reference: {len(x)}점 · q0 {q0:.2f} mAh")
    print("정방향은 보간뿐이다 (src.fitting.reconstruct) — 시뮬레이션 없음\n")

    for label, lli, lam_pe, lam_ne in points:
        q = q_at(lli, lam_pe, lam_ne)
        if q is None:
            print(f"[건너뜀] {label} ({lli},{lam_pe},{lam_ne}) 격자에 없음")
            continue
        r = q / q0
        p0 = modes_to_params(lam_pe, lam_ne, lli, r)
        print(f"══ {label}  (LLI {lli}, LAM_PE {lam_pe}, LAM_NE {lam_ne}) ══")
        print(f"   r = q/q0 = {r:.6f}")
        print(f"   p0 = [α_PE {p0[0]:.5f}, β_PE {p0[1]:.5f}, "
              f"α_NE {p0[2]:.5f}, β_NE {p0[3]:.5f}]")

        for h in STEPS:
            J, n = jac(p0, h)
            if n < 20:
                print(f"   [스텝 {h}] 창 안 유효점 {n}개 — 건너뜀")
                continue
            sv = np.linalg.svd(J, compute_uv=False)
            cond = sv[0] / sv[-1]
            print(f"   [스텝 {h:.0e}] 유효점 {n:4d} · 특이값 "
                  f"{np.array2string(sv, precision=4)}")
            print(f"                 조건수 {cond:10.1f} · "
                  f"σ2/σ1 {sv[1]/sv[0]:.4f} · σ3/σ1 {sv[2]/sv[0]:.5f} · "
                  f"σ4/σ1 {sv[3]/sv[0]:.6f}")
            srows.append({"point": label, "step": h, "n_valid": n,
                          **{f"sv{i+1}": sv[i] for i in range(4)},
                          "cond": cond,
                          **{f"sv{i+1}_over_sv1": sv[i] / sv[0] for i in range(4)}})
            if h == STEPS[1]:                     # 대표 스텝의 고유벡터만 남긴다
                U, S, Vt = np.linalg.svd(J, full_matrices=False)
                for k in range(4):
                    v = Vt[k]
                    if v.sum() < 0:
                        v = -v
                    vrows.append({"point": label, "rank": k + 1, "sv": S[k],
                                  **dict(zip(PNAMES, v))})
        print()

    pd.DataFrame(srows).to_csv(OUT / "spectrum.csv", index=False)
    pd.DataFrame(vrows).to_csv(OUT / "vectors.csv", index=False)

    print("=== 대조 — Phase 1c 의 모드 좌표(3개) ===")
    print("   특이값 0.689 / 2.786 / 12.571 · 조건수 18.2")
    print("   같은 곡선을 창 좌표(4개)에서 보면 위 표다. 두 값의 차이가 곧")
    print("   **좌표 선택이 만든 몫**이다 (점검 B1).\n")
    print(f"산출물: {OUT}/  (spectrum.csv · vectors.csv)")


if __name__ == "__main__":
    main()
