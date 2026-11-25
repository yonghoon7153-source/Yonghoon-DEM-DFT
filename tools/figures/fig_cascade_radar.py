#!/usr/bin/env python3
"""fig_cascade_radar.py — 도펀트별 8축 레이더 (세미나용, 사용자 요청 2026-08-11).

축 8개 (전부 47종 풀 내 favorable percentile, 0=최악 1=최선):
  Oxidation ↑ox_V · ESW window ↑window_V · Li pathway ↑bvs_x005 · Low blocking ↓blocking
  Disorder ↑disorder_std · Lightweight ↓mass_per_cation · Low cost ↓cost_tier · Soft ↓E(UMA)

⚠ 방향 규약: 화살표는 "favorable 방향"이고 percentile 은 이미 favorable 로 뒤집어 계산한다.
⚠ air 축은 의도적으로 뺐다 — air_hsab 는 [Zhu20] 대조에서 체계 편향(9/35 전부 과소평가)이
  확인돼 provisional 이라, 레이더에 넣으면 그 편향을 그림으로 승격시키는 셈이다.
⚠ percentile 은 순위 표현이다 — 절대 물성 아님. 문헌 선례: duquesnoy2023 Fig.6 (radar 비교).

출력: docs/figures/cascade/cascade_radar_6panel.png  (2×3: PASS 대표 3 + 충돌/조합 3)
      docs/figures/cascade/cascade_radar_pair_CrHf.png (Cr₂O₃ vs HfO₂ 겹침 — 상보성 시각화)
      db/properties/cascade_radar_axes_origin.csv     (Origin-ready, 47종 전체)
"""
import csv
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ── 회수분(90종) 병렬 생성 shim (2026-08-14) ────────────────────────────────
#   CASCADE_SUFFIX=_v2 CASCADE_FIGDIR=docs/figures/cascade_v2 로 돌리면 정본을 안 건드리고
#   같은 그림을 회수 풀로 다시 그린다. 접미사가 비면 동작이 100% 이전과 같다.
import os as _os
_SUF = _os.environ.get("CASCADE_SUFFIX", "")
_FIGDIR = _os.environ.get("CASCADE_FIGDIR", "")
def _csv(name):
    """db/properties 상대 경로에 접미사를 끼운다. 'a/b/x.csv' → 'a/b/x_v2.csv'."""
    if not _SUF: return name
    root, ext = _os.path.splitext(name)
    cand = root + _SUF + ext
    return cand if _os.path.exists(cand) else name


INK, MUT = "#1f2937", "#6b7280"
NAVY, RED, TEAL, VIOLET, ORANGE, GREEN = "#1F4E79", "#9E2A2B", "#0d9488", "#7c3aed", "#c05621", "#65a30d"

D = json.load(open(_csv("db/properties/cascade_v23_themes.json")))["dopants"]
SC = {r["dopant"]: r for r in csv.DictReader(open("db/properties/cascade_seminar_scorecard_47.csv"))}

# (라벨, themes 필드, favorable 방향 +1=클수록 좋음)
AXES = [("Oxidation", "ox_V", +1), ("ESW window", "window_V", +1),
        ("Li pathway", "bvs_x005", +1), ("Low blocking", "blocking", -1),
        ("Disorder", "disorder_std", +1), ("Lightweight", "mass_per_cation", -1),
        ("Low cost", "cost_tier", -1), ("Soft", "E_scorecard", -1)]


def field(d, key):
    if key == "E_scorecard":
        return float(SC[d["dopant"]]["E_GPa_UMA_relative"])
    v = d.get(key)
    return float(v) if v is not None else None


def percentiles():
    out = {}
    for lab, key, sgn in AXES:
        vals = [(d["dopant"], field(d, key)) for d in D]
        ok = [(n, v) for n, v in vals if v is not None]
        arr = sorted(v for _, v in ok)
        n = len(arr)
        for name, v in ok:
            # favorable percentile: 낮을수록 좋은 축은 뒤집는다
            r = sum(1 for x in arr if x < v) / (n - 1) if n > 1 else 0.5
            out.setdefault(name, {})[lab] = r if sgn > 0 else 1 - r
        for name, v in vals:
            if v is None:
                out.setdefault(name, {})[lab] = None   # 결측 ≠ 0 — 그리지 않는다
    return out


P = percentiles()
LABS = [a[0] for a in AXES]
ANG = np.linspace(0, 2 * np.pi, len(LABS), endpoint=False)


def draw(ax, name, color, fill=True, lw=2.2, label=None):
    vals = [P[name][l] for l in LABS]
    v = [0 if x is None else x for x in vals]          # 표시용 0, 라벨로 결측 명시
    vv = np.array(v + v[:1]); aa = np.append(ANG, ANG[0])
    ax.plot(aa, vv, color=color, lw=lw, label=label or name)
    if fill:
        ax.fill(aa, vv, color=color, alpha=0.18)
    miss = [LABS[i] for i, x in enumerate(vals) if x is None]
    return miss


def polar_ax(ax, title=None):
    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
    ax.set_ylim(0, 1); ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_yticklabels([]); ax.set_xticks(ANG)
    ax.set_xticklabels(LABS, fontsize=7.5, color=INK)
    ax.grid(color="#d1d5db", lw=0.7); ax.spines["polar"].set_color("#d1d5db")
    if title:
        ax.set_title(title, fontsize=11, color=INK, pad=14, fontweight="bold")


PANEL = [("WO3", NAVY), ("CaO", TEAL), ("LiF", GREEN),
         ("B2O3", RED), ("Cr2O3", ORANGE), ("HfO2", VIOLET)]
SUB = {"WO3": "G5 top rank", "CaO": "through G4", "LiF": "through G4",
       "B2O3": "axis conflict", "Cr2O3": "pair half (cathode)", "HfO2": "pair half (anode)"}

fig, axs = plt.subplots(2, 3, figsize=(11, 7.6), dpi=300, subplot_kw={"polar": True})
for ax, (name, c) in zip(axs.flat, PANEL):
    polar_ax(ax)
    disp = name.replace("2", "$_2$").replace("3", "$_3$") if name != "LiF" else "LiF"
    ax.set_title(f"{disp}  ({SUB[name]})", fontsize=11, color=c, pad=14, fontweight="bold")
    draw(ax, name, c)
fig.suptitle("Eight-axis profiles: within-pool favorable percentiles (descriptive ranking, not absolute properties)",
             fontsize=11, color=INK, y=0.99)
fig.text(0.5, 0.015, "Axes follow the 14-theme registry; air axes excluded (provisional). BVSE/blocking are static proxies.",
         ha="center", fontsize=8, color=MUT)
fig.tight_layout(rect=[0, 0.03, 1, 0.96])
fig.savefig("docs/figures/cascade/cascade_radar_6panel.png")

fig2, ax = plt.subplots(figsize=(6.4, 6.2), dpi=300, subplot_kw={"polar": True})
polar_ax(ax)
draw(ax, "Cr2O3", ORANGE, label="Cr$_2$O$_3$ (oxidation-strong)")
draw(ax, "HfO2", VIOLET, label="HfO$_2$ (window/pathway-strong)")
ax.set_title("Complementarity, drawn: the two halves of the top pair hypothesis",
             fontsize=11.5, color=INK, pad=18, fontweight="bold")
ax.legend(loc="upper right", bbox_to_anchor=(1.32, 1.08), fontsize=9, frameon=False)
fig2.text(0.5, 0.02, "End-member profiles only — the pair itself is uncomputed (hypothesis, site competition unresolved)",
          ha="center", fontsize=8, color=RED)
fig2.tight_layout(rect=[0, 0.04, 1, 1])
fig2.savefig("docs/figures/cascade/cascade_radar_pair_CrHf.png")

with open("db/properties/cascade_radar_axes_origin.csv", "w", newline="") as f:
    w = csv.writer(f)
    f.write("# Eight-axis favorable percentiles (within 47-dopant pool) for radar charts.\n")
    f.write("# Direction already folded in (1 = most favorable). Missing left EMPTY - not zero.\n")
    f.write("# Sources: cascade_v23_themes.json + cascade_seminar_scorecard_47.csv (E axis). Air axes excluded (provisional).\n")
    w.writerow(["dopant"] + LABS)
    for d in sorted(P):
        w.writerow([d] + [("" if P[d][l] is None else round(P[d][l], 4)) for l in LABS])
print("wrote 6panel + pair + origin csv")
