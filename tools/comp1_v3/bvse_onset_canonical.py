#!/usr/bin/env python3
"""bvse_onset_canonical.py — BVSE 침투 onset 의 **정본 정의 한 개**.

왜 이게 필요한가 — 같은 맵에서 세 값이 나왔다
------------------------------------------------
2026-07-29 감사에서 modelc onset 이 파일마다 달랐다:
  db/properties/bvse_modelc/modelc_bvse_summary.json      a/b/c = 0.55 / 0.55 / 1.65
  db/properties/bvse_cubic_approx/bvse_orig_vs_cubic.json         0.40 / 0.35 / 1.40
  감사 재계산                                                      0.65 / 0.40 / 1.40

**연결성 알고리즘은 셋 다 같다** (축 방향 2× 타일 → ndimage.label →
한 라벨의 축방향 span ≥ N 이면 그 축으로 침투). 채널 부피 %도 셋 다 일치한다
(1.23 / 3.32 / 8.36 / 13.44 / 17.85). 즉 **맵은 같고 onset 만 갈렸다.**

원인은 **레벨 격자**다:
  bvse_faithful_cubic.py   levels = np.arange(0.05, 3.01, 0.05)      # 고정 0.05 step
  bvse_standalone.py       levels = np.linspace(min, p60, 60)        # 데이터 의존 step
  bvse_percolation_analysis.py  levels = np.linspace(Emin, hi, 80)   # 또 다름
onset 은 "침투가 처음 성립하는 격자점" 이라 **격자 해상도만큼 위로 튄다**.
0.55 vs 0.40 은 물리 차이가 아니라 양자화 차이다.

정본 규약 (이 파일이 유일한 출처)
---------------------------------
1. **above-min**: m = BVSE − BVSE.min() (CLAUDE.md aboveMin 관례)
2. **연결성**: ndimage.label 기본(6-이웃 face connectivity), 축 방향 2× 타일 span 검사
3. **격자**: LEVELS = arange(0.05, 3.00+, 0.05) val² — **고정**. 데이터 의존 격자 금지.
4. onset 은 **격자 상한값**이므로 항상 `±0.05 val²` 를 달고 인용한다.

⚠ **onset 차이는 격자 칸 수로 판정한다.**
   onset 은 격자 상한값이라 ±1칸(0.05)은 정보가 아니다. 규칙:
     ≤ 1칸  → 동등. 인용 금지.
     ≥ 3칸  → 양자화 훨씬 초과. 인용 가능하되 격자를 함께 밝힌다.
   적용 예 (2026-07-29): modelc 0.40/0.35/1.40 vs LPSOCl 0.55/0.35/2.05
     → a +3칸(악화) · b 0칸(동등) · **c +13칸(악화)**.
     즉 **LPSOCl 은 채널 부피는 더 열리는데(4.74 vs 3.32 %) c축 침투 문턱은 더 높다**
     = 빈 공간은 늘었지만 c축으로 연결된 길이 더 어려워졌다. 기존 static-channel
     paradox 와 같은 계열이고, 13칸이라 양자화로 설명되지 않는다.
   **정량·순위의 1순위 축은 여전히 채널 부피 %** (격자 무관, 세 파일 완전 일치).

  python3 tools/comp1_v3/bvse_onset_canonical.py db/properties/bvse_modelc/modelc_bvse_map.npy
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

LEVELS = np.arange(0.05, 3.001, 0.05)      # ⚠ 고정 격자 — 바꾸면 정본이 아니다
ISOS = (0.25, 0.5, 1.0, 1.5, 2.0)
STEP = 0.05


def perc_axis(mask, ax):
    """축 ax 방향으로 한 주기를 관통하는 연결 성분이 있나 (PBC)."""
    N = mask.shape[ax]
    big = np.concatenate([mask, mask], axis=ax)
    lbl, nlab = ndimage.label(big)
    for k in range(1, nlab + 1):
        idx = np.where(lbl == k)[ax]
        if idx.size and (idx.max() - idx.min()) >= N:
            return True
    return False


def onsets(bvse):
    m0 = bvse - float(bvse.min())
    out = {}
    for ax, name in enumerate("abc"):
        out[name] = None
        for E in LEVELS:
            if perc_axis(m0 <= E, ax):
                out[name] = round(float(E), 2)
                break
    return out


def iso_fractions(bvse):
    m0 = bvse - float(bvse.min())
    return {str(i): round(100.0 * float((m0 <= i).mean()), 2) for i in ISOS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("map_npy")
    ap.add_argument("--label", default="")
    ap.add_argument("--out_json", default=None)
    a = ap.parse_args()

    bv = np.load(a.map_npy)
    o, fr = onsets(bv), iso_fractions(bv)
    print(f"map {a.map_npy}  shape {bv.shape}  min {bv.min():.4f}")
    print(f"  onset (above-min, val², 고정격자 step {STEP}):  "
          + " · ".join(f"{k} {v if v is not None else '침투 없음'}" for k, v in o.items())
          + f"   [±{STEP}]")
    print("  채널 부피 % (정량·순위의 정본 축): "
          + " · ".join(f"iso{k} {v}" for k, v in fr.items()))
    print(f"\n⚠ onset 차이는 **격자 칸 수**로 판정한다 (1칸 = {STEP}): ≤1칸 동등(인용 금지) / ≥3칸 인용 가능.")
    print("  1순위 정량축은 채널 부피 % (격자 무관). 감사 2026-07-29: 같은 맵에서 onset 세 값이 나왔다.")

    res = {"property": "bvse_percolation_onset_CANONICAL",
           "system": a.label or Path(a.map_npy).stem,
           "source_map": a.map_npy,
           "convention": {
               "reference": "above-min (BVSE - global min)",
               "connectivity": "ndimage.label default (6-neighbour face), 2x tile per axis, span >= N",
               "level_grid": f"arange(0.05, 3.00, {STEP}) val^2 — FIXED",
               "quantization": f"±{STEP} val^2",
           },
           "perc_onset_val2": o,
           "iso_volume_frac_pct": fr,
           "⚠_onset_quantization_rule": (
               f"onset 은 격자 상한값이라 해상도만큼 위로 튄다(같은 맵에서 0.55/0.55/1.65 · "
               f"0.40/0.35/1.40 · 0.65/0.40/1.40 세 값이 나온 것이 그 증거). 판정은 **칸 수**로: "
               f"≤1칸({STEP}) 동등·인용 금지 / ≥3칸 인용 가능(격자 병기). "
               f"1순위 정량축은 채널 부피 % (격자 무관)."),
           "_supersedes": ["db/properties/bvse_modelc/modelc_bvse_summary.json perc_onset_val2",
                           "db/properties/bvse_cubic_approx/bvse_orig_vs_cubic.json perc_orig"]}
    if a.out_json:
        Path(a.out_json).write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
        print(f"\n→ {a.out_json}")
    return res


if __name__ == "__main__":
    main()
