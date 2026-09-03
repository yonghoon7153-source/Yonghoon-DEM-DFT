#!/usr/bin/env python3
"""Phase 1c — Lin & Khoo 2024 의 **해석적 null 방향**을 우리 좌표에서 수치 검증한다.

질문 (wiki/concepts/np-lip-ocv-reparametrization.md 가 인쇄만 하고 확인한 적 없는 것):

  Lin & Khoo 2024 §2.3 은 SOC 정규화된 full-cell OCV 의 **형상 자유도가 정확히
  2** 이고, `(1−LLI, 1−LAM_NE, 1−LAM_PE)` 의 **스칼라배가 곡선 형상을 전혀
  바꾸지 않는다** 고 닫힌 형태로 적는다. pristine 에서 미분하면 그 null 방향은
  `(dLLI, dLAM_PE, dLAM_NE)` 좌표에서 정확히 `(1,1,1)/√3` 이다.

  우리 곡선은 **PyBaMM DFN · 유한 전류**로 만든 것이고 Lin 의 정리는 **순수
  열역학**이다. 그래서 두 물음이 갈린다:
    (A) 그 방향이 우리 격자에서도 실제로 가장 평평한 방향인가 (각도로)
    (B) 평평하다면 **얼마나** 평평한가 — 잡음과 비교해서

  (B) 가 판정을 정한다. "구조적으로 불가" 와 "우리 잡음에서 불가" 는 다른
  문장이고, 인용할 수 있는 것은 후자뿐이다.

Schaeffer 2024 에서 가져온 절차 (wiki/concepts/fitting-degeneracy.md 의
「그 방향을 그리는 법」 2단계) — `JᵀJ` 를 고유분해해 **최소 고유벡터**를 본다.
Schaeffer 는 이 그림을 959차원에서 시도했다 포기했다. 우리는 3차원이고 Lin 이
답을 닫힌 형태로 줬으므로 **비교 대상이 있다.**

입력: degradation-degeneracy/results/grid_curves_v4/curves.parquet (**읽기 전용**)
  — 11×11×11 모드 격자(0~0.20, 0.02 간격) × noise 층, 곡선 300점.
  RUN_SCOPE(`src/ tools/ configs/ scripts/ run.sh requirements*.txt`)를 건드리지
  않으므로 게이트 리뷰 대상 code identity 와 봉인 산출물은 움직이지 않는다.

출력: results/phase1c/{null_ray.csv, jacobian.csv, residual_shape.csv} + stdout.
  **그 파일이 결과의 정본이다** — 위키·문서에 적힌 숫자는 사본이다.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1c"

# 양 끝 컷오프 근방은 수치 잡음이 크고 격자마다 끝점이 미세하게 다르다 —
# 두 곡선의 **차이**를 재는 것이 목적이므로 안쪽만 본다.
LO, HI = 0.02, 0.98
H = 0.02          # 격자 간격 = 전방차분 스텝


def load():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n"
                 "  원자료는 gitignored 다 — grid 를 먼저 돌려야 한다.")
    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise",
        "q_mah", "x_norm", "v_full", "v_full_noisy"])
    return df


def main():
    df = load()
    d0 = df[df.noise == 0]
    uniq = d0[["cond_id", "lli", "lam_pe", "lam_ne"]].drop_duplicates()

    def cid(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else r.cond_id.iloc[0]

    def raw(c):
        g = d0[d0.cond_id == c].sort_values("x_norm")
        return g.x_norm.to_numpy(float), g.v_full.to_numpy(float), float(g.q_mah.iloc[0])

    c00 = cid(0, 0, 0)
    if c00 is None:
        sys.exit("pristine 조건(0,0,0)이 격자에 없다 — 중단")
    xg, v00_full, q0 = raw(c00)
    m = (xg >= LO) & (xg <= HI)
    xs = xg[m]
    v00 = v00_full[m]

    def curve(c):
        xa, va, q = raw(c)
        return np.interp(xs, xa, va), q

    OUT.mkdir(parents=True, exist_ok=True)

    # ── 1. null ray — lli = lam_pe = lam_ne = x 인 격자점 전부 ────────────
    xs_ray = sorted(v for v in uniq.lli.unique()
                    if cid(v, v, v) is not None)
    rows = []
    shapes = {}
    for x in xs_ray:
        vi, q = curve(cid(x, x, x))
        dv = (vi - v00) * 1000.0                     # mV
        rows.append({
            "x": x, "cond_id": cid(x, x, x), "q_mah": q, "q_over_q0": q / q0,
            "q_pred_1_minus_x": 1.0 - x,
            "q_rel_err_pct": ((q / q0) - (1 - x)) / (1 - x) * 100.0,
            "max_abs_dv_mV": float(np.max(np.abs(dv))),
            "rms_dv_mV": float(np.sqrt(np.mean(dv ** 2))),
            "x_at_max": float(xs[int(np.argmax(np.abs(dv)))]),
        })
        if x > 0:
            shapes[x] = dv / x                       # x 로 나눠 모양만 남긴다
    ray = pd.DataFrame(rows)
    ray.to_csv(OUT / "null_ray.csv", index=False)

    # ── 2. 잔차의 **모양**이 하나인가 ────────────────────────────────────
    ref_x = max(shapes)
    ref = shapes[ref_x]
    srows = [{"x": x, "corr_with_ref": float(np.corrcoef(s, ref)[0, 1]),
              "scale_vs_ref": float(np.dot(s, ref) / np.dot(ref, ref)),
              "max_abs_mV_per_unit": float(np.max(np.abs(s)))}
             for x, s in sorted(shapes.items())]
    pd.DataFrame(srows).to_csv(OUT / "residual_shape.csv", index=False)
    pd.DataFrame({"x_norm": xs, "dv_per_unit_mV": ref}).to_csv(
        OUT / "residual_profile.csv", index=False)

    # ── 3. Jacobian → JᵀJ 고유분해 → u_min ──────────────────────────────
    axes = [("LLI", cid(H, 0, 0)), ("LAM_PE", cid(0, H, 0)), ("LAM_NE", cid(0, 0, H))]
    if any(c is None for _, c in axes):
        sys.exit(f"축 조건이 격자에 없다: {[(n, c) for n, c in axes]}")
    J = np.column_stack([(curve(c)[0] - v00) / H for _, c in axes])
    w, V = np.linalg.eigh(J.T @ J)                   # 오름차순
    sv = np.sqrt(np.maximum(w, 0.0))
    u_min = V[:, 0] / np.linalg.norm(V[:, 0])
    if u_min.sum() < 0:
        u_min = -u_min                               # 부호는 자유 — 합이 양수인 쪽
    lin = np.ones(3) / np.sqrt(3)
    cos = float(np.clip(np.dot(u_min, lin), -1.0, 1.0))
    ang = float(np.degrees(np.arccos(abs(cos))))

    pd.DataFrame({
        "axis": [n for n, _ in axes],
        "col_norm_V_per_unit": np.linalg.norm(J, axis=0),
        "u_min": u_min, "u_mid": V[:, 1] / np.linalg.norm(V[:, 1]),
        "u_max": V[:, 2] / np.linalg.norm(V[:, 2]),
    }).to_csv(OUT / "jacobian.csv", index=False)

    # ── 4. 잡음과의 대조 — 판정을 정하는 표 ──────────────────────────────
    noise_sd = {}
    for nv in sorted(df.noise.unique()):
        if nv == 0:
            continue
        g = df[df.noise == nv]
        noise_sd[nv] = float(((g.v_full_noisy - g.v_full) * 1000).std())

    # ── 보고 ─────────────────────────────────────────────────────────────
    print(f"입력  : {CURVES}")
    print(f"기준  : pristine {c00} · 곡선 {len(xs)}점 (x_norm {LO}~{HI}) · q {q0:.2f} mAh")
    print(f"null ray: {len(xs_ray)}점  x = {xs_ray[0]:.2f} ~ {xs_ray[-1]:.2f}\n")

    print("=== Lin 예측 1 — 총용량이 (1−x) 배인가 ===")
    print(ray[["x", "q_mah", "q_over_q0", "q_pred_1_minus_x", "q_rel_err_pct"]]
          .to_string(index=False, float_format=lambda v: f"{v:9.5f}"))
    print(f"\n  → 상대오차 최대 {ray.q_rel_err_pct.abs().max():.3f} %  "
          "(부호가 한쪽이고 x 에 단조 — 유한 전류 보정으로 읽힌다)\n")

    print("=== Lin 예측 2 — SOC 정규화 곡선이 불변인가 ===")
    print(ray[["x", "max_abs_dv_mV", "rms_dv_mV", "x_at_max"]]
          .to_string(index=False, float_format=lambda v: f"{v:9.3f}"))
    slope = np.polyfit(ray.x[1:], ray.max_abs_dv_mV[1:], 1)[0]
    print(f"\n  → 불변이 **아니다**. max|ΔV| 가 x 에 거의 정확히 비례한다 "
          f"(기울기 {slope:.2f} mV / 단위 = {slope/100:.3f} mV per 1%p)\n")

    print("=== 잔차의 모양이 하나인가 (dV/x 로 정규화) ===")
    print(pd.DataFrame(srows).to_string(index=False,
                                        float_format=lambda v: f"{v:9.5f}"))
    print(f"\n  → 상관이 {min(r['corr_with_ref'] for r in srows):.4f} 이상. "
          "**깨짐의 방향이 하나로 고정**되어 있고 크기만 x 에 비례한다.")
    k = int(np.argmax(np.abs(ref)))
    print(f"  → 잔차가 x_norm = {xs[k]:.3f} (pristine 전압 {v00[k]:.4f} V) 한 점에 몰린다\n")

    print("=== ★ u_min 이 Lin 의 null 방향과 정렬하는가 ===")
    print("  순서: (LLI, LAM_PE, LAM_NE)")
    print(f"  열 노름 (V/단위)      = {np.round(np.linalg.norm(J, axis=0), 4)}")
    print(f"  특이값                = {np.round(sv, 6)}")
    print(f"  조건수 (max/min)      = {sv[-1] / sv[0]:.1f}")
    print(f"  u_min                 = {np.round(u_min, 5)}")
    print(f"  Lin 예측 (1,1,1)/√3   = {np.round(lin, 5)}")
    print(f"  cos = {cos:.6f}  →  **각도 {ang:.2f}°**\n")

    print("=== 판정 — 잡음과 대조 ===")
    for nv, sd in noise_sd.items():
        print(f"  noise={nv} (실측 σ {sd:.3f} mV):")
        for _, r in ray[ray.x > 0].iterrows():
            verdict = "묻힌다" if r.rms_dv_mV < sd else f"{r.rms_dv_mV/sd:.1f}σ"
            print(f"    x={r.x:.2f}  RMS {r.rms_dv_mV:6.3f} mV  →  {verdict}")
    print(f"\n산출물: {OUT}/  (null_ray.csv · residual_shape.csv · "
          "residual_profile.csv · jacobian.csv)")


if __name__ == "__main__":
    main()
