#!/usr/bin/env python3
"""Phase 1j — 두 `x` 정규화를 잇는 **환산을 세우고**, Phase 1g 의 C 판을 다시 짓는다.

## 무엇이 막혀 있었나

Phase 1f 와 1g 가 **같은 하나의 미제**로 수렴했다:

- **1f**: Birkl 식 (1)·Table 5 의 `x` 는 **전극 자신의 격자 점유율**(0~1)이고,
  식 (7)–(10) 의 `x` 는 `[인쇄]` "the active material originally **utilised within
  the capacity range of the full cell**" 기준이다. **둘을 잇는 환산이 인쇄돼 있지
  않다.**
- **1g**: `build_reference_interps("halfcell")` 은 **전극 전체**를 `[0,1]` 로
  정규화하고 `"grid"` 는 **셀이 실제로 쓰는 창**을 `[0,1]` 로 정규화한다.
  그래서 무전류 판(C)이 "전류를 뺀" 것이 아니라 **"좌표계를 바꾼"** 것이 되어
  **기각**했다 (`LAM_PE` 열 노름 8.38 → 50.17 V/단위).

## 환산은 이미 저장소 안에 있었다

`[해석]` Phase 1h 가 `src/inventory.py` 를 단서로 지목했는데, **더 곧바른 자리가
있었다** — 봉인된 두 캐시가 셀의 화학량론 창을 **양 끝에서** 못 박고 있다:

```
완충(100 % SOC)  configs/base.yaml  baseline.{pe_init_conc, ne_*_init_conc}
완방(0 % SOC)    .cache/discharged_state/<baseline_hash>.json  {pe, ne_primary, ne_secondary}
```

그 둘을 각 전극의 `*_max_conc` 로 나누면 **전극 전체 좌표에서 본 셀의 창**이 나온다:

```
y₁₀₀ = c_pe(완충)/c_pe,max          y₀ = c_pe(완방)/c_pe,max
z₁₀₀ = Σ vfᵢ c_neᵢ(완충) / Σ vfᵢ c_ne,maxᵢ      z₀ = 같은 식의 완방
```

(NE 는 복합이라 `src/halfcell.py:143` 의 **용량 가중 평균**과 같은 식을 쓴다 —
`z = (q_gr x_gr + q_si x_si)/(q_gr + q_si)`.)

그러면 환산은 아핀이다:

```
s_창_PE = (y − y₁₀₀) / (y₀ − y₁₀₀)
s_창_NE = (z₁₀₀ − z) / (z₁₀₀ − z₀)        (방전방향 정렬 — grid 규약과 같다)
```

## 무엇을 하나

1. 환산 상수를 뽑아 **인쇄**한다 (Phase 1f 가 필요로 하는 바로 그 수).
2. 그 환산으로 **평형 OCP 를 셀 창으로 다시 정규화**해 reference 를 만든다.
3. **검산** — 그 reference 로 재구성한 pristine full-cell 이 실제 reference 곡선과
   겹치는가. 겹치면 환산이 맞은 것이고, Phase 1g 의 C 판이 왜 튀었는지도 설명된다.
4. 겹치면 그 위에서 **null 방향**을 재서 Phase 1g 가 못 닫은 절반
   ("음극 제한이 12° 중 얼마인가")을 판정한다.

⚠ 봉인 확인: 두 캐시의 `source_digest` 가 현행 트리와 다르면 **읽기를 거부**한다.
⚠ `degradation-degeneracy/` 는 **읽기만** 한다.

출력: results/phase1j/{bridge.csv, angles.csv} + stdout. **CSV 가 정본이다.**
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
OUT = HERE / "results" / "phase1j"

H = 0.02
LO, HI = 0.02, 0.98
MODES = ["LLI", "LAM_PE", "LAM_NE"]
ONES = np.ones(3) / np.sqrt(3.0)


def angle_deg(u, v):
    c = float(np.clip(abs(np.dot(u, v)) / (np.linalg.norm(u) * np.linalg.norm(v)), -1, 1))
    return np.degrees(np.arccos(c)), c


def umin_of(J):
    w, V = np.linalg.eigh(J.T @ J)
    u = V[:, 0] / np.linalg.norm(V[:, 0])
    return (-u if u.sum() < 0 else u), np.sqrt(np.maximum(w, 0.0))


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n  원자료는 gitignored 다.")

    from src.io import source_digest
    now = source_digest()

    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    b = cfg["baseline"]

    metas = sorted(HCDIR.glob("*.meta.yaml"))
    if not metas:
        sys.exit(f"평형 OCP 캐시가 없다: {HCDIR}")
    meta = yaml.safe_load(metas[0].read_text(encoding="utf-8"))
    if str(meta.get("source_digest")) != now:
        sys.exit(f"평형 OCP 캐시가 다른 코드로 만들어졌다 — 거부한다.\n"
                 f"  봉인 {meta.get('source_digest')} ≠ 현행 {now}")
    hc = json.loads(sorted(HCDIR.glob("*_ocp_*.json"))[0].read_text())

    dsf = sorted(DSDIR.glob("*.json"))
    if not dsf:
        sys.exit(f"완방 상태 캐시가 없다: {DSDIR}")
    ds = json.loads(dsf[0].read_text())
    if str(ds.get("source_digest")) != now:
        sys.exit(f"완방 캐시가 다른 코드로 만들어졌다 — 거부한다.\n"
                 f"  봉인 {ds.get('source_digest')} ≠ 현행 {now}")

    print(f"봉인 확인  source_digest {now}  = 평형 OCP · 완방 상태 둘 다 ✓")
    print(f"완방 캐시  {dsf[0].name}   (baseline_hash {ds.get('baseline_hash')})\n")

    # ── ① 환산 상수 ────────────────────────────────────────────────────────
    y100 = b["pe_init_conc"] / b["pe_max_conc"]
    y0 = ds["pe"] / b["pe_max_conc"]

    q_gr = b["ne_primary_max_conc"] * b["ne_primary_vf"]
    q_si = b["ne_secondary_max_conc"] * b["ne_secondary_vf"]

    def zcomp(c_gr, c_si):
        return (c_gr * b["ne_primary_vf"] + c_si * b["ne_secondary_vf"]) / (q_gr + q_si)

    z100 = zcomp(b["ne_primary_init_conc"], b["ne_secondary_init_conc"])
    z0 = zcomp(ds["ne_primary"], ds["ne_secondary"])

    print("── ① 두 정규화를 잇는 환산 (전극 전체 좌표에서 본 셀의 창) ──")
    print(f"   PE  y₁₀₀ = {y100:.6f}   y₀ = {y0:.6f}   창 폭 {y0-y100:.6f}"
          f"   → 전극의 **{100*(y0-y100):.2f} %** 만 쓴다")
    print(f"   NE  z₁₀₀ = {z100:.6f}   z₀ = {z0:.6f}   창 폭 {z100-z0:.6f}"
          f"   → 전극의 **{100*(z100-z0):.2f} %** 만 쓴다")
    print(f"   환산  s_창_PE = (y − {y100:.6f}) / {y0-y100:.6f}")
    print(f"         s_창_NE = ({z100:.6f} − z) / {z100-z0:.6f}\n")

    # ── ② 셀 창으로 다시 정규화한 평형 OCP reference ────────────────────────
    y_t = np.asarray(hc["y_pe"], float)
    u_pe_t = np.asarray(hc["u_pe"], float)
    z_t = np.asarray(hc["z_ne"], float)
    u_ne_t = np.asarray(hc["u_ne"], float)

    s_pe = (y_t - y100) / (y0 - y100)
    s_ne = (z100 - z_t) / (z100 - z0)
    o_pe, o_ne = np.argsort(s_pe), np.argsort(s_ne)
    f_pe_w = make_ref_interp(s_pe[o_pe], u_pe_t[o_pe])
    f_ne_w = make_ref_interp(s_ne[o_ne], u_ne_t[o_ne])

    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah",
        "x_norm", "v_pe", "v_ne", "v_full"])
    d0 = df[df.noise == 0]
    ref = extract_reference(d0)
    xa = ref.x_norm.to_numpy(float)
    keep = (xa >= LO) & (xa <= HI)
    xs = xa[keep]
    q0 = float(ref.q_mah.iloc[0])
    grid_ref = {"x": xa, "pe": ref.v_pe.to_numpy(float), "ne": ref.v_ne.to_numpy(float)}
    f_pe_g, f_ne_g = build_reference_interps("grid", grid_ref)
    f_pe_h, f_ne_h = build_reference_interps("halfcell", grid_ref, hc=hc)

    uniq = d0[["cond_id", "lli", "lam_pe", "lam_ne", "q_mah"]].drop_duplicates()

    def q_of(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else float(r.q_mah.iloc[0])

    def recon(fp, fn, l, p, n):
        q = q_of(l, p, n)
        if q is None:
            return None
        _, _, full = reconstruct(modes_to_params(p, n, l, q / q0), fp, fn, xs)
        return full

    # ── ③ 검산 — 환산이 맞으면 pristine 재구성이 실제 곡선과 겹쳐야 한다 ────
    v_true = np.interp(xs, xa, ref.v_full.to_numpy(float))
    print("── ③ 검산: pristine 재구성 vs 실제 reference 곡선 ──")
    print("   남는 차이가 **과전압**이면 부호가 한쪽으로 몰려야 한다 (0.05 C 방전이므로")
    print("   측정 pOCV 가 평형 OCV 보다 낮다 → 재구성 − 실측 > 0 이 대부분).")
    print(f"   {'reference 판':<28}{'평균|Δ|':>9}{'최대|Δ|':>9}{'양수 비율':>10}  (mV)")
    rows = []
    for name, (fp, fn) in {
            "grid (창 정규화·유한전류)": (f_pe_g, f_ne_g),
            "halfcell (전극 전체) — 1g 의 C": (f_pe_h, f_ne_h),
            "★ 셀 창 재정규화 (이번 판)": (f_pe_w, f_ne_w)}.items():
        v = recon(fp, fn, 0, 0, 0)
        ok = np.isfinite(v) & np.isfinite(v_true)
        s = (v[ok] - v_true[ok]) * 1e3            # 부호 있는 차이
        d = np.abs(s)
        pos = float(np.mean(s > 0))
        print(f"   {name:<28}{d.mean():>9.1f}{d.max():>9.1f}{100*pos:>9.0f}%"
              f"   (유효 {ok.sum()}점)")
        rows.append({"reference": name, "mae_mV": float(d.mean()),
                     "max_abs_mV": float(d.max()),
                     "mean_signed_mV": float(s.mean()),
                     "frac_positive": pos, "n_valid": int(ok.sum())})
    print()

    # ── ④ null 방향 ────────────────────────────────────────────────────────
    axes = [(H, 0, 0), (0, H, 0), (0, 0, H)]
    print("── ④ null 방향 ──")
    arows = []
    for name, (fp, fn) in {
            "B · 창 대수 · 격자 reference (유한전류)": (f_pe_g, f_ne_g),
            "★ D · 창 대수 · **셀 창 평형 OCP (무전류)**": (f_pe_w, f_ne_w)}.items():
        base = recon(fp, fn, 0, 0, 0)
        cols = [(recon(fp, fn, *a) - base) / H for a in axes]
        M = np.column_stack(cols)
        okm = np.isfinite(M).all(axis=1) & np.isfinite(base)
        J = M[okm]
        u, sv = umin_of(J)
        a_deg, c = angle_deg(u, ONES)
        print(f"   {name}   유효 {J.shape[0]}점")
        print(f"      열 노름 {np.round(np.linalg.norm(J, axis=0), 4)} V/단위"
              f"   조건수 {sv[-1]/sv[0]:.2f}")
        print(f"      u_min {np.round(u, 5)}   ∠(u_min,(1,1,1)) = {a_deg:.2f}°"
              f"   cos = {c:.6f}")
        arows.append({"panel": name, "n_points": int(J.shape[0]),
                      "angle_deg": a_deg, "cos": c, "cond": float(sv[-1]/sv[0]),
                      **{f"col_norm_{m}": float(np.linalg.norm(J[:, i]))
                         for i, m in enumerate(MODES)},
                      **{f"u_min_{m}": u[i] for i, m in enumerate(MODES)}})

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{"y_100": y100, "y_0": y0, "pe_window": y0 - y100,
                   "z_100": z100, "z_0": z0, "ne_window": z100 - z0,
                   "source_digest": now}]).to_csv(OUT / "bridge.csv", index=False)
    pd.DataFrame(rows).to_csv(OUT / "reconstruction_check.csv", index=False)
    pd.DataFrame(arows).to_csv(OUT / "angles.csv", index=False)
    print(f"\n산출물: {OUT}/  (bridge.csv · reconstruction_check.csv · angles.csv)")


if __name__ == "__main__":
    main()
