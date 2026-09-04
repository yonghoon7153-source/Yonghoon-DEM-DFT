#!/usr/bin/env python3
"""Phase 1g — 12.04° 의 **출처를 가른다**: 유한 전류인가, 창 모델 자체인가.

Phase 1c 는 우리 격자에서 `JᵀJ` 의 최소 고유벡터가 Lin 의 `(1,1,1)/√3` 과
**12.04°** 안에서 일치함을 쟀다 (`cos = 0.977999`). 그리고 그 틈이

  · **유한 전류**(우리 곡선은 PyBaMM DFN 이고 Lin 의 정리는 순수 열역학) 때문인지
  · **음극 제한**(창 모델 자체의 성질) 때문인지

**갈리지 않는다**고 한계로 적었다 (Phase 1c Gap 2, 통합 논지 Gap 2).
이 스크립트가 그것을 가른다.

## 세 판을 나란히 놓는다

`(1,1,1)` 과의 각도를 세 가지 방식으로 잰다. 셋의 차이가 곧 몫이다.

| 판 | 곡선의 출처 | 전류 | 창 변환 |
|---|---|---|---|
| **A** PyBaMM 직접 | 격자의 실제 시뮬 곡선 (Phase 1c 와 **같은 것**) | 유한 | — |
| **B** 창 재구성 · 격자 reference | reference 곡선 + `windowed_curve` | reference 에만 | 순수 |
| **C** 창 재구성 · **평형 OCP** | `.cache/halfcell` 의 무전류 반쪽전지 OCP | **없음** | 순수 |

- **A → B** 의 변화 = "모드가 곡선을 움직이는 방식" 을 실제 시뮬 대신 창 대수로
  바꾼 몫.
- **B → C** 의 변화 = **전류를 완전히 뺀** 몫. C 가 Lin 의 전제(순수 열역학)에
  가장 가깝다.
- **C 의 각도가 0 에 가까우면** 12.04° 는 유한 전류가 만든 것이고,
  **여전히 크면** 창 모델·음극 제한이 만든 구조적 기울기다.

## 무전류 OCP 는 어디서 오나

`degradation-degeneracy/.cache/halfcell/*.json` — `recipe.method = ocp`,
`branch = delithiation`, `parameter_set = Chen2020_composite`. 전류 없이 뽑은
평형 반쪽전지 곡선이고, production 이 `build_reference_interps("halfcell", hc=…)`
로 쓰는 바로 그 캐시다. **읽기만 한다.**

⚠ 이 캐시는 `source_digest ea35ff4f39b97489` 로 봉인돼 있다. 그 값이 현행 트리와
다르면 **읽기를 거부**한다 (fail-closed) — 다른 코드로 만든 곡선을 조용히 쓰면
비교가 거짓이 된다.

출력: results/phase1g/{angles.csv, jacobians.csv} + stdout. **CSV 가 정본이다.**
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
    build_reference_interps, extract_reference, modes_to_params, reconstruct)

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
HCDIR = DD / ".cache" / "halfcell"
OUT = HERE / "results" / "phase1g"
H = 0.02                      # Phase 1c 와 같은 전방차분 스텝 (= 격자 간격)
LO, HI = 0.02, 0.98           # Phase 1c 와 **같은** 관측 구간 (양 끝 수치 잡음 제외)
MODES = ["LLI", "LAM_PE", "LAM_NE"]
ONES = np.ones(3) / np.sqrt(3.0)


def angle_deg(u, v):
    c = float(np.clip(abs(np.dot(u, v)) / (np.linalg.norm(u) * np.linalg.norm(v)), -1, 1))
    return np.degrees(np.arccos(c)), c


def umin_of(J):
    w, V = np.linalg.eigh(J.T @ J)
    return V[:, 0] / np.linalg.norm(V[:, 0]), np.sqrt(np.maximum(w, 0.0))


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}\n  원자료는 gitignored 다.")
    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah",
        "x_norm", "v_pe", "v_ne", "v_full"])
    d0 = df[df.noise == 0]
    uniq = d0[["cond_id", "lli", "lam_pe", "lam_ne", "q_mah"]].drop_duplicates()

    def cid(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else r.cond_id.iloc[0]

    ref = extract_reference(d0)
    xs_all = ref.x_norm.to_numpy(float)
    keep = (xs_all >= LO) & (xs_all <= HI)      # A 판이 Phase 1c 와 같아야 한다
    xs = xs_all[keep]
    q0 = float(ref.q_mah.iloc[0])
    grid_ref = {"x": xs_all, "pe": ref.v_pe.to_numpy(float),
                "ne": ref.v_ne.to_numpy(float)}

    def sim_curve(c):
        g = d0[d0.cond_id == c].sort_values("x_norm")
        return np.interp(xs, g.x_norm.to_numpy(float), g.v_full.to_numpy(float))

    def q_of(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return float(r.q_mah.iloc[0])

    # ── 무전류 평형 OCP (봉인 확인 후 읽는다) ────────────────────────────
    metas = sorted(HCDIR.glob("*.meta.yaml"))
    if not metas:
        sys.exit(f"평형 OCP 캐시가 없다: {HCDIR}")
    meta = yaml.safe_load(metas[0].read_text(encoding="utf-8"))
    from src.io import source_digest
    now = source_digest()
    sealed = str(meta.get("source_digest"))
    if sealed != now:
        sys.exit(f"평형 OCP 캐시가 다른 코드로 만들어졌다 — 비교를 거부한다.\n"
                 f"  봉인 {sealed} ≠ 현행 {now}")
    hc = json.loads(metas[0].with_suffix("").with_suffix(".json").read_text()) \
        if metas[0].with_suffix("").with_suffix(".json").exists() \
        else json.loads(sorted(HCDIR.glob("*_ocp_*.json"))[0].read_text())

    print(f"입력 곡선 : {CURVES}")
    print(f"평형 OCP  : {sorted(HCDIR.glob('*_ocp_*.json'))[0].name}")
    print(f"            recipe {meta['recipe']} · parameter_set {meta['parameter_set']}")
    print(f"            봉인 source_digest {sealed} = 현행 ✓")
    print(f"스텝 H = {H} (Phase 1c 와 같다) · reference {len(xs)}점\n")

    f_pe_g, f_ne_g = build_reference_interps("grid", grid_ref)
    f_pe_h, f_ne_h = build_reference_interps("halfcell", grid_ref, hc=hc)

    def recon(f_pe, f_ne, l, p, n):
        r = q_of(l, p, n) / q0
        _, _, full = reconstruct(modes_to_params(p, n, l, r), f_pe, f_ne, xs)
        return full

    axes = [(H, 0, 0), (0, H, 0), (0, 0, H)]
    if any(cid(*a) is None for a in axes) or cid(0, 0, 0) is None:
        sys.exit("축 조건이 격자에 없다")

    panels = {}
    # A — PyBaMM 직접 (Phase 1c 재현)
    v00 = sim_curve(cid(0, 0, 0))
    panels["A · PyBaMM 직접 (유한 전류)"] = np.column_stack(
        [(sim_curve(cid(*a)) - v00) / H for a in axes])
    # B·C — 창 재구성
    for key, (fp, fn) in {"B · 창 재구성 · 격자 reference": (f_pe_g, f_ne_g),
                          "C · 창 재구성 · **평형 OCP (무전류)**": (f_pe_h, f_ne_h)}.items():
        base = recon(fp, fn, 0, 0, 0)
        cols = [(recon(fp, fn, *a) - base) / H for a in axes]
        M = np.column_stack(cols)
        ok = np.isfinite(M).all(axis=1) & np.isfinite(base)
        panels[key] = M[ok]

    OUT.mkdir(parents=True, exist_ok=True)
    arows, jrows = [], []
    for name, J in panels.items():
        u, sv = umin_of(J)
        if u.sum() < 0:
            u = -u
        ang, cos = angle_deg(u, ONES)
        cond = sv[-1] / sv[0] if sv[0] > 0 else np.inf
        print(f"══ {name} ══  유효점 {J.shape[0]}")
        print(f"   열 노름 (V/단위) {np.round(np.linalg.norm(J, axis=0), 4)}")
        print(f"   특이값           {np.round(sv, 4)}   조건수 {cond:8.2f}")
        print(f"   u_min            {np.round(u, 5)}")
        print(f"   ∠(u_min, (1,1,1)) = {ang:6.2f}°   cos = {cos:.6f}\n")
        arows.append({"panel": name, "n_points": int(J.shape[0]),
                      "angle_deg": ang, "cos": cos, "cond": cond,
                      **{f"u_min_{m}": u[i] for i, m in enumerate(MODES)},
                      **{f"sv{i+1}": sv[i] for i in range(3)}})
        jrows += [{"panel": name, "mode": m,
                   "col_norm_V_per_unit": float(np.linalg.norm(J[:, i]))}
                  for i, m in enumerate(MODES)]

    pd.DataFrame(arows).to_csv(OUT / "angles.csv", index=False)
    pd.DataFrame(jrows).to_csv(OUT / "jacobians.csv", index=False)

    a = {r["panel"][0]: r["angle_deg"] for r in arows}
    print("── 몫 나누기 ──")
    print(f"   A → B  (시뮬 → 창 대수)   {a['A']:6.2f}° → {a['B']:6.2f}°"
          f"   Δ {a['B']-a['A']:+.2f}°")
    print(f"   B → C  (**전류 제거**)     {a['B']:6.2f}° → {a['C']:6.2f}°"
          f"   Δ {a['C']-a['B']:+.2f}°")
    print(f"\n   C 가 0 에 가까우면 12° 는 유한 전류가 만든 것이고,")
    print(f"   여전히 크면 창 모델·음극 제한이 만든 구조적 기울기다.")
    print(f"\n산출물: {OUT}/  (angles.csv · jacobians.csv)")


if __name__ == "__main__":
    main()
