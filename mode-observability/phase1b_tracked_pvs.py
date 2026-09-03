#!/usr/bin/env python3
"""Phase 1b — PVS 를 **연속 추적**으로 다시 잰다 (Phase 1 의 비단조 원인 제거).

Phase 1 의 발견 (docs/PHASE1_NOTES.md):
  창 고정 + 창내 전역 극값 방식은 곡선이 밀리면 **다른 극값을 잡는다.**
  LLI 단독 스윕에서 valley 가 3.859 → 3.900(창 상한) → 3.736 으로 점프했고,
  peak 도 lli 0.12→0.14 에서 dq 5.54→8.25 로 갈아탔다. 그래서 PVS 스윕이
  비단조로 보였다 — 물리가 아니라 **feature identity 가 바뀐 것**이다.

이 스크립트가 하는 일:
  pristine 에서 peak/valley 를 한 번 고정하고, 격자를 BFS 로 퍼지며 **이전
  격자점의 극값 전압에 가장 가까운 극값**을 따라간다 (continuation). 한 걸음의
  전압 이동이 MAX_STEP 을 넘으면 추적 실패로 표시하고 그 가지를 끊는다 —
  조용히 다른 극값으로 갈아타지 않는다 (fail-closed).

이렇게 하면 두 가지가 분리된다:
  ① 추적이 유지되는 영역의 **진짜** 모드 감도 (물리)
  ② 추적이 깨지는 영역 (feature 의 구조적 한계 — 그 자체가 결과다)

출력: results/phase1b/pvs_tracked.csv (정본) + 요약 stdout.
"""
import sys
from collections import deque
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

from src.curves import to_dqdv  # noqa: E402

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1b"

STEP = 0.02                 # 격자 간격
MAX_STEP = 0.060            # 한 걸음에 허용하는 극값 전압 이동 [V]
SEED_PEAK_WIN = (3.55, 3.72)
ORDER = 5                   # argrelextrema 이웃 폭


def extrema(x_norm, v_full, q_ah, window=21):
    """(v, dqdv[Ah/V], 극대 인덱스, 극소 인덱스)."""
    v, dq = to_dqdv(x_norm, v_full, window=window)
    dq = np.abs(dq) * q_ah
    return v, dq, argrelextrema(dq, np.greater, order=ORDER)[0], \
        argrelextrema(dq, np.less, order=ORDER)[0]


def nearest(v, idx, target):
    """target 전압에 가장 가까운 극값. (index, |Δv|) 또는 (None, inf)."""
    if len(idx) == 0:
        return None, np.inf
    d = np.abs(v[idx] - target)
    j = int(np.argmin(d))
    return int(idx[j]), float(d[j])


def main():
    df = pd.read_parquet(CURVES)
    df = df[df.noise == 0.0]

    # ── 1. 모든 격자점의 극값을 한 번만 계산 ──────────────────────────
    cache = {}
    for _, c in df.groupby("cond_id"):
        c = c.sort_values("x_norm")
        key = (round(c.lli.iloc[0], 2), round(c.lam_pe.iloc[0], 2),
               round(c.lam_ne.iloc[0], 2))
        cache[key] = extrema(c.x_norm.values, c.v_full.values,
                             c.q_mah.iloc[0] / 1000.0)
    print(f"격자점 {len(cache)}개의 극값 계산 완료")

    # ── 2. pristine 에서 seed ─────────────────────────────────────────
    root = (0.0, 0.0, 0.0)
    v, dq, mx, mn = cache[root]
    win = mx[(v[mx] >= SEED_PEAK_WIN[0]) & (v[mx] <= SEED_PEAK_WIN[1])]
    ip = int(win[np.argmax(dq[win])])
    after = mn[v[mn] > v[ip]]
    iv = int(after[0])                       # peak 바로 다음 국소 최소
    print(f"seed: peak {v[ip]:.3f} V ({dq[ip]:.2f} Ah/V) · "
          f"valley {v[iv]:.3f} V ({dq[iv]:.2f} Ah/V) · "
          f"PVS {(dq[ip]-dq[iv])/(v[ip]-v[iv]):.2f} Ah/V^2")

    # ── 3. BFS continuation ───────────────────────────────────────────
    got = {root: dict(v_peak=v[ip], dqdv_peak=dq[ip],
                      v_valley=v[iv], dqdv_valley=dq[iv],
                      pvs=(dq[ip] - dq[iv]) / (v[ip] - v[iv]),
                      hops=0, jump_peak=0.0, jump_valley=0.0)}
    broken = {}
    q = deque([root])
    while q:
        cur = q.popleft()
        st = got[cur]
        for ax in range(3):
            for sgn in (+1, -1):
                nb = list(cur)
                nb[ax] = round(nb[ax] + sgn * STEP, 2)
                nb = tuple(nb)
                if nb in got or nb in broken or nb not in cache:
                    continue
                v2, dq2, mx2, mn2 = cache[nb]
                jp, dp = nearest(v2, mx2, st["v_peak"])
                jv, dv = nearest(v2, mn2, st["v_valley"])
                if jp is None or jv is None or dp > MAX_STEP or dv > MAX_STEP:
                    broken[nb] = dict(from_=cur, d_peak=dp, d_valley=dv)
                    continue
                if not v2[jv] > v2[jp]:       # 순서가 뒤집히면 같은 짝이 아니다
                    broken[nb] = dict(from_=cur, d_peak=dp, d_valley=dv)
                    continue
                got[nb] = dict(
                    v_peak=v2[jp], dqdv_peak=dq2[jp],
                    v_valley=v2[jv], dqdv_valley=dq2[jv],
                    pvs=(dq2[jp] - dq2[jv]) / (v2[jp] - v2[jv]),
                    hops=st["hops"] + 1, jump_peak=dp, jump_valley=dv)
                q.append(nb)

    print(f"추적 성공 {len(got)} / 격자 {len(cache)} "
          f"({100*len(got)/len(cache):.0f}%) · 끊긴 가지 {len(broken)}")

    rows = [dict(lli=k[0], lam_pe=k[1], lam_ne=k[2], **s) for k, s in got.items()]
    out = pd.DataFrame(rows).sort_values(["lli", "lam_pe", "lam_ne"])
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT / "pvs_tracked.csv", index=False)

    t = out.set_index(["lli", "lam_pe", "lam_ne"])

    print("\n단독 스윕 (추적 유지, PVS · v_peak · v_valley):")
    for name, key in (("LLI", lambda s: (s, 0.0, 0.0)),
                      ("LAM_PE", lambda s: (0.0, s, 0.0)),
                      ("LAM_NE", lambda s: (0.0, 0.0, s))):
        print(f"  {name}:")
        for s in np.arange(0, 0.21, 0.02):
            k = key(round(s, 2))
            if k not in t.index:
                print(f"    {s:.2f}  — 추적 끊김")
                continue
            r = t.loc[k]
            print(f"    {s:.2f} {r.pvs:8.1f}   pk {r.v_peak:.3f}  vl {r.v_valley:.3f}")

    h = STEP
    print("\n유한차분 감도 ∂PVS/∂mode:")
    for label, p in (("pristine (0,0,0)", (0.0, 0.0, 0.0)),
                     ("22p 근방 (0.16,0.12,0.12)", (0.16, 0.12, 0.12)),
                     ("중간 (0.08,0.06,0.06)", (0.08, 0.06, 0.06))):
        if p not in t.index:
            print(f"  {label}: 기준점이 추적 밖")
            continue
        g, ok = [], True
        for ax in range(3):
            hi = list(p); hi[ax] = round(hi[ax] + h, 2); hi = tuple(hi)
            if hi not in t.index:
                ok = False; g.append(np.nan); continue
            g.append((t.loc[hi].pvs - t.loc[p].pvs) / h)
        g = np.array(g)
        sgn = "".join("?" if np.isnan(x) else "+" if x > 0 else "-" for x in g)
        print(f"  {label}: [{g[0]:8.1f} {g[1]:8.1f} {g[2]:8.1f}]  부호 {sgn}"
              f"{'' if ok else '  (일부 이웃이 추적 밖)'}")
        if not np.isnan(g[0]) and not np.isnan(g[1]):
            print(f"      LLI·LAM_PE 동부호: {(g[0]*g[1])>0}")

    print(f"\n→ {OUT/'pvs_tracked.csv'}")


if __name__ == "__main__":
    main()
