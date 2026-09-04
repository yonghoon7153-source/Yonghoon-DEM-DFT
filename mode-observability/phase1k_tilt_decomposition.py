#!/usr/bin/env python3
"""Phase 1k — 12° 를 **두 사상으로 쪼갠다**: 모드→창(M) 과 창→곡선(W).

## 물음

Phase 1j 가 "12° 는 전류와 무관하고 **창 모델의 구조**에서 온다" 까지 좁혔다.
남은 물음은 그 구조의 **어느 층**이냐다. 우리 파이프라인은 두 사상의 합성이다:

```
(LLI, LAM_PE, LAM_NE)  --M-->  (α_PE, β_PE, α_NE, β_NE)  --W-->  U_full(x)
        3차원                          4차원                      288점
```

`J = W · M` 이므로 12° 의 출처도 둘 중 하나다:

| 가설 | 뜻 | 판정 방법 |
|---|---|---|
| **M 탓** | Lin 방향 `(1,1,1)` 이 창 좌표에서 이미 "특별하지 않은" 방향으로 간다 | `d = M·(1,1,1)` 이 `W` 의 **약한 부분공간**에 얼마나 들어가나 |
| **W 탓** | 창 좌표에서는 잘 겨눴는데 곡선이 그 방향을 유독 잘 본다 | 같은 각을 창 좌표에서 재고 비교 |

**실측 결과는 M 쪽이다** — `cond(M) = 2337` 대 `cond(W) = 31.5`.

## ⚠ 먼저 — 이 `M` 은 우리 파이프라인의 사상이 **아니다**

`modes_to_params()` 는 `src/fitting.py` 헤더가 **"역함수 — 테스트·진단용,
'paper' 규약"** 이라 못 박은 함수다. 그 규약의 합성 격자 평균 |오차| 는
**0.128** 이고 production 이 쓰는 `"derived"` 규약은 **0.012** 다 (10배 차이).

더 근본적으로 — **우리 production 파이프라인에는 모드→창 사상이 없다.**
창 좌표 4개를 직접 맞추고 모드는 **사후 변환**으로 얻는다
(`wiki/comparisons/halfcell-window-parametrization-lineage.md` 의 처방 3번).
그러므로 여기 `M` 은 **진단용 허구**이고 그 성질을 우리 추정기의 성질로 옮겨
읽으면 안 된다. 이 스크립트가 답하는 것은 **"창 대수로 지은 판(Phase 1g B/C,
1j D)이 무엇을 물려받았나"** 이지 production 의 축퇴가 아니다.

## 곁들이는 반사실 탐침

Phase 1j 가 **PE 는 전극의 65.61 %, NE 는 96.70 %** 만 쓴다는 비대칭을 쟀다.
그 비대칭이 12° 의 원인이라는 가설을 **반사실**로 찔러 본다 — 평형 OCP 를
더 넓은 가짜 창으로 다시 정규화해 각을 재본다.
⚠ 이것은 **다른 셀**이지 우리 셀이 아니다. 인과가 아니라 **민감도**만 읽는다.

출력: results/phase1k/{decomposition.csv, counterfactual.csv} + stdout.
**CSV 가 정본이다.**
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

from src.fitting import (  # noqa: E402
    build_reference_interps, extract_reference, make_ref_interp,
    modes_to_params, reconstruct)

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
HCDIR = DD / ".cache" / "halfcell"
DSDIR = DD / ".cache" / "discharged_state"
CFG = DD / "configs" / "base.yaml"
OUT = HERE / "results" / "phase1k"

H = 0.02
HW = 5e-3                      # 창 좌표 미분 스텝 (Phase 1d·1e 대표 스텝)
LO, HI = 0.02, 0.98
MODES = ["LLI", "LAM_PE", "LAM_NE"]
WIN = ["a_pe", "b_pe", "a_ne", "b_ne"]
ONES = np.ones(3) / np.sqrt(3.0)


def ang(u, v):
    c = abs(float(u @ v)) / (np.linalg.norm(u) * np.linalg.norm(v))
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def ang_to_span(d, B):
    """벡터 d 와 부분공간 span(B) 사이의 각 (B 는 정규직교 열)."""
    p = B @ (B.T @ d)
    r = np.linalg.norm(p) / np.linalg.norm(d)
    return float(np.degrees(np.arccos(np.clip(r, 0.0, 1.0))))


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}")

    from src.io import source_digest
    now = source_digest()
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    b = cfg["baseline"]

    metas = sorted(HCDIR.glob("*.meta.yaml"))
    meta = yaml.safe_load(metas[0].read_text(encoding="utf-8"))
    ds = json.loads(sorted(DSDIR.glob("*.json"))[0].read_text())
    for nm, got in (("평형 OCP", meta.get("source_digest")),
                    ("완방 상태", ds.get("source_digest"))):
        if str(got) != now:
            sys.exit(f"{nm} 캐시가 다른 코드로 만들어졌다 — 거부한다 ({got} ≠ {now})")
    hc = json.loads(sorted(HCDIR.glob("*_ocp_*.json"))[0].read_text())
    print(f"봉인 확인 source_digest {now} ✓\n")

    # Phase 1j 의 환산
    y100 = b["pe_init_conc"] / b["pe_max_conc"]
    y0 = ds["pe"] / b["pe_max_conc"]
    q_gr = b["ne_primary_max_conc"] * b["ne_primary_vf"]
    q_si = b["ne_secondary_max_conc"] * b["ne_secondary_vf"]

    def zc(cg, cs):
        return (cg * b["ne_primary_vf"] + cs * b["ne_secondary_vf"]) / (q_gr + q_si)

    z100 = zc(b["ne_primary_init_conc"], b["ne_secondary_init_conc"])
    z0 = zc(ds["ne_primary"], ds["ne_secondary"])
    print(f"환산 (Phase 1j)  PE 창 {y0-y100:.6f} ({100*(y0-y100):.2f} %)"
          f"   NE 창 {z100-z0:.6f} ({100*(z100-z0):.2f} %)\n")

    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah",
        "x_norm", "v_pe", "v_ne", "v_full"])
    d0 = df[df.noise == 0]
    ref = extract_reference(d0)
    xa = ref.x_norm.to_numpy(float)
    xs = xa[(xa >= LO) & (xa <= HI)]
    q0 = float(ref.q_mah.iloc[0])
    grid_ref = {"x": xa, "pe": ref.v_pe.to_numpy(float), "ne": ref.v_ne.to_numpy(float)}
    uniq = d0[["cond_id", "lli", "lam_pe", "lam_ne", "q_mah"]].drop_duplicates()

    def q_of(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else float(r.q_mah.iloc[0])

    def make_window_ref(pe_frac, ne_frac):
        """평형 OCP 를 주어진 창 폭으로 정규화한 reference (Phase 1j 방식).

        ⚠ 창을 **넓힐 때는 완방 끝(y₀)을 고정하고 뒤로 늘린다.** 앞 끝(y₁₀₀)을
        고정한 채 넓히면 `s = 1` 이 `y = y₁₀₀ + 폭 > 1` 로 **표 밖**으로 나가
        보간자가 끝값에서 평평해진다 — 그러면 반사실이 물리가 아니라 포화
        artifact 를 재게 된다 (2026-09-04 실측: 폭 0.80 → y = 1.07).
        """
        yt = np.asarray(hc["y_pe"], float)
        zt = np.asarray(hc["z_ne"], float)
        y_start = y0 - pe_frac
        z_start = z0 + ne_frac
        if y_start < -1e-9 or z_start > 1 + 1e-9:
            raise ValueError(f"창 폭이 표를 벗어난다 (y_start={y_start:.4f}, "
                             f"z_start={z_start:.4f})")
        s_pe = (yt - y_start) / pe_frac
        s_ne = (z_start - zt) / ne_frac
        op, on = np.argsort(s_pe), np.argsort(s_ne)
        return (make_ref_interp(s_pe[op], np.asarray(hc["u_pe"], float)[op]),
                make_ref_interp(s_ne[on], np.asarray(hc["u_ne"], float)[on]))

    # ★ 동작점을 22p 로 잡는다 — pristine 에서는 모드가 0 이라 `−H` 조건이 없어
    #   J·M 을 **전방차분**으로만 만들 수 있고, W 는 중심차분이라 두 방식이
    #   섞인다. 그 불일치가 곧 `J = W·M` 검산의 잔차로 나온다 (실측 0.18).
    #   22p 근방은 ±H 가 모두 격자에 있어 **셋 다 중심차분**으로 맞출 수 있다.
    OP = (0.16, 0.12, 0.12)

    def spectra(fp, fn, op=OP, h=H):
        """(J: 모드 3열, W: 창 4열, M: 3→4 사상 Jacobian) — 셋 다 중심차분."""
        def curve_from_p(p):
            _, _, full = reconstruct(p, fp, fn, xs)
            return full

        def p_of(l, pe, ne):
            q = q_of(l, pe, ne)
            return None if q is None else modes_to_params(pe, ne, l, q / q0)

        p0 = p_of(*op)
        if p0 is None:
            sys.exit(f"동작점 {op} 이 격자에 없다")
        base = curve_from_p(p0)

        Mcols, Jcols = [], []
        for k in range(3):
            up = list(op); up[k] += h
            dn = list(op); dn[k] -= h
            pu, pd = p_of(*up), p_of(*dn)
            if pu is None or pd is None:
                sys.exit(f"중심차분에 필요한 조건이 없다: {up} 또는 {dn}")
            Mcols.append((pu - pd) / (2 * h))
            Jcols.append((curve_from_p(pu) - curve_from_p(pd)) / (2 * h))
        M = np.column_stack(Mcols)                       # 4×3
        J = np.column_stack(Jcols)

        Wcols = []
        for i in range(4):
            pp = np.array(p0, float); pp[i] += HW
            pm = np.array(p0, float); pm[i] -= HW
            Wcols.append((curve_from_p(pp) - curve_from_p(pm)) / (2 * HW))
        W = np.column_stack(Wcols)                       # n×4

        ok = np.isfinite(J).all(axis=1) & np.isfinite(W).all(axis=1) & np.isfinite(base)
        return J[ok], W[ok], M

    f_pe_w, f_ne_w = make_window_ref(y0 - y100, z100 - z0)
    J, W, M = spectra(f_pe_w, f_ne_w)
    print(f"동작점 {OP} (22p 근방) · 유효점 {J.shape[0]} · 셋 다 중심차분\n")

    # ── ① 합성이 실제로 성립하나 (J ≈ W·M) ────────────────────────────────
    #   성립하지 않으면 아래 ②③ 은 **아무 뜻이 없다.** 스텝을 줄이며 수렴도 본다.
    print("── ① 검산: J = W·M 인가 (이게 깨지면 아래는 못 쓴다) ──")
    print(f"   {'모드 스텝':>10}{'‖J−W·M‖/‖J‖':>16}")
    conv = []
    for h in (0.04, 0.02):
        try:
            Jh, Wh, Mh = spectra(f_pe_w, f_ne_w, h=h)
        except SystemExit:
            print(f"   {h:>10}{'격자에 없음':>16}")
            continue
        r = float(np.linalg.norm(Jh - Wh @ Mh) / np.linalg.norm(Jh))
        conv.append({"mode_step": h, "rel_residual": r})
        print(f"   {h:>10}{r:>16.5f}")
    rel = conv[-1]["rel_residual"] if conv else float("nan")
    ratio = conv[0]["rel_residual"] / rel if len(conv) > 1 and rel else float("nan")
    print(f"   스텝을 반으로 줄이면 잔차가 {conv[0]['rel_residual']:.5f} → {rel:.5f}"
          f" (비 {ratio:.2f})")
    print(f"   {'✓ 비가 ≈2 → **1차 수렴** → 잔차는 이산화 오차이고 합성은 성립한다.' if 1.6 < ratio < 2.6 else '✗ 1차 수렴이 아니다 — 아래 분해를 믿으면 안 된다.'}")
    print(f"   (모드 스텝 0.02 가 격자 간격이라 **더 줄일 수 없다** — 잔차 {rel:.3f} 은"
          f" 남는다.)\n")

    # ── ② 두 층의 조건수 — 축퇴가 **어느 층에 있나** ──────────────────────
    sm = np.linalg.svd(M, compute_uv=False)
    sw = np.linalg.svd(W, compute_uv=False)
    w, V = np.linalg.eigh(J.T @ J)
    sj = np.sqrt(np.maximum(w, 0.0))
    u = V[:, 0] / np.linalg.norm(V[:, 0])
    u = -u if u.sum() < 0 else u
    a_mode = ang(u, ONES)

    print("── ② 축퇴가 어느 층에 있나 (조건수) ──")
    print(f"   M (모드→창)  특이값 {np.round(sm, 6)}   조건수 **{sm[0]/sm[-1]:8.1f}**")
    print(f"   W (창→곡선)  특이값 {np.round(sw, 4)}   조건수 {sw[0]/sw[-1]:8.1f}")
    print(f"   J (합성·실측) 특이값 {np.round(sj, 4)}   조건수 {sj[-1]/sj[0]:8.1f}")
    print(f"   → **축퇴는 압도적으로 M 쪽이다** (2000배 대 30배).\n")

    print("── ②' 그런데 `M·(1,1,1)` 의 *방향*은 못 읽는다 ──")
    nm_ones = float(np.linalg.norm(M @ ONES))
    nm_u = float(np.linalg.norm(M @ u))
    print(f"   ‖M·(1,1,1)/√3‖ = {nm_ones:.6f}   = σ_min(M) 의 {nm_ones/sm[-1]:.1f} 배")
    print(f"   ‖M·u_min‖      = {nm_u:.6f}   = σ_min(M) 의 {nm_u/sm[-1]:.1f} 배")
    print(f"   `[해석]` 둘 다 M 의 null 근처로 **거의 상쇄돼 사라진다.** 그래서 그")
    print(f"   상(image)을 정규화한 방향은 **남은 잔여가 정하는 잡음**이다 —")
    print(f"   실제로 u_min 과 (1,1,1) 은 모드 좌표에서 {a_mode:.2f}° 인데 그 상은")
    print(f"   {ang(M @ u, M @ ONES):.1f}° 떨어져 있다. **방향 비교는 여기서 하면 안 된다.**\n")

    print("── ③ 모드 좌표에서 실제로 잰 각 ──")
    print(f"   u_min {np.round(u, 5)}   ∠(u_min,(1,1,1)) = **{a_mode:.2f}°**")
    print(f"   (Phase 1h 는 같은 동작점을 **전방차분·시뮬 곡선**으로 4.61° 로 쟀다.")
    print(f"    여기는 **중심차분·무전류 창 대수** 라 판이 다르다 — 아래 경계 참조.)\n")

    rows = [{"rel_residual_J_minus_WM": rel,
             "angle_mode_deg": a_mode,
             "cond_M": float(sm[0] / sm[-1]), "cond_W": float(sw[0] / sw[-1]),
             "cond_J": float(sj[-1] / sj[0]),
             "sigma_min_M": float(sm[-1]),
             "norm_M_ones": nm_ones, "norm_M_umin": nm_u,
             "norm_M_ones_over_sigmin": float(nm_ones / sm[-1]),
             "norm_M_umin_over_sigmin": float(nm_u / sm[-1]),
             **{f"u_min_{m}": u[i] for i, m in enumerate(MODES)}}]

    # ── ④ 반사실 — PE 창을 NE 만큼 넓히면 각이 움직이나 ────────────────────
    print("── ④ 반사실 탐침: PE 창 폭을 바꾸면 각이 어떻게 움직이나 ──")
    print("   ⚠ 이것은 **다른 셀**이다. 인과가 아니라 민감도만 읽는다.")
    print("   완방 끝(y₀)을 고정하고 **뒤로** 넓힌다 — 앞으로 넓히면 표 밖으로 나간다.")
    print(f"   {'PE 창':>9}{'∠(u_min,(1,1,1))':>19}{'조건수':>9}   u_min")
    crows = []
    for frac, tag in [(y0 - y100, "실제 65.61 %"),
                      (0.75, "가짜 75 %"),
                      (0.90, "가짜 90 % (y₀ 고정 상한 근처)")]:
        try:
            fp, fn = make_window_ref(frac, z100 - z0)
        except ValueError as e:
            print(f"   {100*frac:>8.2f}%   건너뜀 — {e}")
            continue
        Jc, _, _ = spectra(fp, fn)
        wc, Vc = np.linalg.eigh(Jc.T @ Jc)
        uc = Vc[:, 0] / np.linalg.norm(Vc[:, 0])
        uc = -uc if uc.sum() < 0 else uc
        sc = np.sqrt(np.maximum(wc, 0.0))
        print(f"   {100*frac:>8.2f}%{ang(uc, ONES):>18.2f}°{sc[-1]/sc[0]:>9.2f}"
              f"   {np.round(uc, 4)}   {tag}")
        crows.append({"pe_window_frac": float(frac), "tag": tag,
                      "angle_deg": ang(uc, ONES), "cond": float(sc[-1] / sc[0]),
                      **{f"u_min_{m}": uc[i] for i, m in enumerate(MODES)}})

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "decomposition.csv", index=False)
    pd.DataFrame(crows).to_csv(OUT / "counterfactual.csv", index=False)
    print(f"\n산출물: {OUT}/  (decomposition.csv · counterfactual.csv)")


if __name__ == "__main__":
    main()
