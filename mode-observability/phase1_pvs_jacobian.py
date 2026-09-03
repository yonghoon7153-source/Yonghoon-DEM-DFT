#!/usr/bin/env python3
"""Phase 1 — 합성 truth 격자에서 PVS 를 계산하고 모드별 감도를 잰다.

질문 (wiki/questions/pvs-sev-lli-lampe-separability.md 의 판정 설계 1~3단계):
  PVS 의 모드별 부호/감도 구조가 우리 합성 truth 에서 세미나 p.8 (P2D 단독
  스윕)과 같은 형태로 나오는가 — 특히 ∂PVS/∂LLI 와 ∂PVS/∂LAM_PE 가 같은
  부호인가 (같으면 PVS 하나로는 LLI↔LAM_PE 방향이 안 갈린다).

입력: degradation-degeneracy/results/grid_curves_v4/curves.parquet (읽기 전용)
  — 11×11×11 모드 격자(0~0.20, 0.02 간격) × noise 층, 곡선 300점.
  noise=0 층의 v_full 만 쓴다 (feature 자체의 감도를 재는 것이므로).

PVS 정의 (세미나 p.7 을 우리 곡선에 옮긴 것):
  v∈[3.55, 3.72] 에서 dQ/dV(방전, |값|, Ah/V) 최대 = peak,
  v∈(v_peak, 3.90] 에서 최소 = valley,
  PVS = (dqdv_peak − dqdv_valley) / (v_peak − v_valley)   [Ah/V²]
  (peak 이 valley 보다 낮은 V 에 있어 분모가 음수 → pristine 에서 음수.
   실측 anchor: pristine −20.0 Ah/V², 세미나 p.8 pristine ≈ −20 과 일치.)

dQ/dV 는 degradation-degeneracy 의 src/curves.to_dqdv 를 그대로 재사용한다
(같은 savgol 창 21 — 평활화 의존성은 p.15 discussion point 3 이므로 Phase 1
말미에 창 11/31 로도 재계산해 민감도를 같이 적는다).

출력: results/phase1/pvs.csv + 요약 stdout. 이 파일이 결과의 정본이다 —
위키에는 참조만 적는다.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

from src.curves import to_dqdv  # noqa: E402  (읽기 전용 재사용)

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1"

PEAK_WIN = (3.55, 3.72)
VALLEY_HI = 3.90


def pvs_of(x_norm, v_full, q_ah, window=21):
    v, dq = to_dqdv(x_norm, v_full, window=window)
    dq = np.abs(dq) * q_ah                       # Ah/V
    pk = (v >= PEAK_WIN[0]) & (v <= PEAK_WIN[1])
    if not pk.any():
        return np.nan, np.nan, np.nan, np.nan, np.nan
    ip = np.flatnonzero(pk)[np.argmax(dq[pk])]
    vl = (v > v[ip]) & (v <= VALLEY_HI)
    if not vl.any():
        return np.nan, np.nan, np.nan, np.nan, np.nan
    iv = np.flatnonzero(vl)[np.argmin(dq[vl])]
    pvs = (dq[ip] - dq[iv]) / (v[ip] - v[iv])
    return pvs, v[ip], dq[ip], v[iv], dq[iv]


def main():
    df = pd.read_parquet(CURVES)
    df = df[df.noise == 0.0]
    rows = []
    for w in (21, 11, 31):
        for cid, c in df.groupby("cond_id"):
            c = c.sort_values("x_norm")
            pvs, vp, dp, vv, dv = pvs_of(c.x_norm.values, c.v_full.values,
                                         c.q_mah.iloc[0] / 1000.0, window=w)
            rows.append(dict(cond_id=cid, window=w,
                             lli=c.lli.iloc[0], lam_pe=c.lam_pe.iloc[0],
                             lam_ne=c.lam_ne.iloc[0], pvs=pvs,
                             v_peak=vp, dqdv_peak=dp, v_valley=vv, dqdv_valley=dv))
    out = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT / "pvs.csv", index=False)

    t = out[out.window == 21].set_index(["lli", "lam_pe", "lam_ne"]).pvs
    print(f"조건 {len(t)}개 (noise=0), NaN {int(t.isna().sum())}개")
    p0 = t.get((0.0, 0.0, 0.0), np.nan)
    print(f"pristine PVS = {p0:.2f} Ah/V^2  (세미나 p.8 pristine ≈ −20)")

    # 단독 모드 스윕 (세미나 p.8 우상 도표의 재현)
    print("\n단독 스윕 (loss 0→0.20, PVS):")
    for name, key in (("LLI", lambda s: (s, 0.0, 0.0)),
                      ("LAM_PE", lambda s: (0.0, s, 0.0)),
                      ("LAM_NE", lambda s: (0.0, 0.0, s))):
        vals = [t.get(key(round(s, 2)), np.nan) for s in np.arange(0, 0.21, 0.02)]
        arr = " ".join("nan" if np.isnan(x) else f"{x:6.1f}" for x in vals)
        print(f"  {name:7s} {arr}")

    # 유한차분 gradient (1×3 Jacobian) — pristine 근방과 22p 동작점 근방
    h = 0.02
    def grad_at(p):
        g = []
        for ax in range(3):
            lo = list(p); hi = list(p)
            hi[ax] = round(hi[ax] + h, 2)
            a, b = t.get(tuple(lo), np.nan), t.get(tuple(hi), np.nan)
            g.append((b - a) / h)
        return np.array(g)

    for label, p in (("pristine (0,0,0)→+h", (0.0, 0.0, 0.0)),
                     ("22p 근방 (0.16,0.12,0.12)→+h", (0.16, 0.12, 0.12))):
        g = grad_at(p)
        sgn = "".join("+" if x > 0 else "-" if x < 0 else "0" for x in g)
        print(f"\n∂PVS/∂(lli, lam_pe, lam_ne) @ {label}:")
        print(f"  [{g[0]:8.1f} {g[1]:8.1f} {g[2]:8.1f}]  부호 {sgn}")
        if not np.isnan(g).any():
            same = (g[0] * g[1]) > 0
            print(f"  LLI·LAM_PE 동부호: {same}  "
                  f"(동부호면 PVS 단독으로 그 방향은 안 갈린다)")

    # 평활화 민감도 (p.15 discussion point 3)
    print("\n평활화 창별 pristine PVS:")
    for w in (11, 21, 31):
        tw = out[out.window == w].set_index(["lli", "lam_pe", "lam_ne"]).pvs
        print(f"  window={w:2d}: {tw.get((0.0, 0.0, 0.0), np.nan):8.2f}")
    print(f"\n→ {OUT/'pvs.csv'}")


if __name__ == "__main__":
    main()
