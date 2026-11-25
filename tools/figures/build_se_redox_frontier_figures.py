#!/usr/bin/env python3
"""산화 · 환원은 어디서 먼저 일어나나 — 설명 그림 6 장 (SVG) · webapp 용어집 '더보기' (kb/concepts/se_redox_frontier.md) 용.

    python3 tools/figures/build_se_redox_frontier_figures.py            # docs/figures/se_redox_frontier/*.svg + Origin CSV 둘
    python3 tools/figures/build_se_redox_frontier_figures.py --selftest # 양성 + 음성 (파일을 안 쓴다)
    python3 tools/figures/build_se_redox_frontier_figures.py --png DIR  # 눈으로 볼 PNG 미리보기 (저장소 밖에 둔다)

  01 frontier map (모식도) · 02 자리별 p-PDOS (데이터: db/properties/b2o3_pdos_site_smooth.csv)
  03 결합 차수 (모식도) · 04 결합당 COHP 빈 쪽 (데이터: docs/figures/icohp/b2o3_COHP_ext.csv)
  05 O 의 집 vs 전압 (데이터: db/properties/cei_esw_Li_controls_2026_09_16.json · o_only_03) · 06 매몰 vs 접촉 (모식도)
데이터 그림 04 · 05 는 Origin CSV 를 db/properties/ 에 낸다 (02 는 원본 CSV 가 이미 db/properties 에 있다).
색은 tools/figures/house_style.py · 그림 안 글자는 영어만 (하우스 규약 · 사용자 뷰어 한글 깨짐).

검사 (selftest · 그림을 쓸 때마다도 돈다):
  ① SVG 가 XML 로 읽힌다 ② 글자 노드에 한글이 없다
  ③ 02: 그림에 찍힌 자리별 평균 (−8..0 eV 창) 이 CSV 에서 다시 낸 값과 같고 site_pdos_mean3p_summary.csv (b2o3 열) 와 0.01 eV 안 ·
     순서 free S > PS4 S > Cl > O
  ④ 04: 띠 가장자리부터 0.5 · 2.5 eV 안의 결합당 반결합 무게가 P–S 에서 가장 크고, 2.5 eV 에서 다른 둘의 3 배 이상
  ⑤ 05: 그림 눈금 전압이 원장 행 값 (소수 둘째 자리) 과 같고, 띠의 O 상 순서가 원장 반응식과 같다 (Li2O → Li3PO4 → Li4P2O7 → LiPO3 → P2O5) ·
     우리 셀 작동창 2.5–4.25 V vs Li 표시가 있다 (사용자 2026-11-09: 양극 쪽은 이 창에서 판단)
음성: 한글 라벨 · 02 찍힌 숫자 바꿈 · 04 열 바꿔치기 (P–S ↔ P–O) · 05 찍힌 전압 바꿈 · 깨진 XML — 다섯 다 잡혀야 한다.

이 도구가 못 하는 것:
  · σ* 시작점 숫자 (+0.10 / +0.75 / +1.61 eV · 2026-07-08 분석) 를 다시 내지 않는다 — 그 정의가 도구로 남아 있지 않고,
    다시 내 보면 B–S 와 P–O 의 앞뒤가 문턱에 따라 바뀐다 (P–S 가 맨 앞인 것은 문턱과 상관없다). 04 는 곡선과 누적 무게만 그린다.
  · 04 의 에너지 0 은 LOBSTER 의 E_F 이고 띠 가장자리는 σ = 0.1 eV 가우시안으로 번져 있다 — 띠틈 숫자를 여기서 읽지 않는다
    (띠틈 정본은 fixed-occupation nscf 고유값 · canonical_registry).
  · 05 는 0 K MP hull grand-potential (Li 열림) · 한 조성 (O 단독 대조 Li5.4PS4.1O0.3Cl1.6) 이다 — 동역학 없음 · Kang 의 LPSOC
    (Li6PS4OCl) 가 아니다. 원장 행의 전압은 그 반응 구간의 **아래 끝**이다 (HZ-esw-reduction-limit-label) — 그래서 Li 흡수는
    1.72 V 아래에서 시작하고, 1.24 V 행은 '환원 한계' 가 아니다 (그림에 그 눈금을 찍지 않는다).
  · 01 · 03 · 06 은 개념 모식도다 — 축에 값이 없다. 06 의 MD 결과는 MLIP · 시드 2 (kb/results/redox_orbital_control_PS4_vs_BS3_2026_07_08.md).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.figures.house_style import ELEM, INK, MUT  # noqa: E402

OUT = ROOT / "docs" / "figures" / "se_redox_frontier"
PDOS_CSV = ROOT / "db/properties/b2o3_pdos_site_smooth.csv"
MEAN_CSV = ROOT / "db/properties/site_pdos_mean3p_summary.csv"
COHP_CSV = ROOT / "docs/figures/icohp/b2o3_COHP_ext.csv"
NBOND_CSV = ROOT / "docs/figures/icohp/b2o3_icohp_summary.csv"
LEDGER = ROOT / "db/properties/cei_esw_Li_controls_2026_09_16.json"
ORIGIN_COHP = ROOT / "db/properties/se_redox_frontier_cohp_per_bond_origin.csv"
ORIGIN_PROFILE = ROOT / "db/properties/se_redox_frontier_o_only_profile_origin.csv"

GAPBAND, GAPLINE = "#fef9c3", "#2563eb"
FILL, LINE = "#eef2f7", "#d3dcdc"
BOND = {"P-S": ELEM["P"], "B-S": ELEM["B"], "P-O": ELEM["O"]}
SITE = [("free_S", "free S²⁻ (4a/4d)", ELEM["S"]), ("PS4_S", "S in PS₄", ELEM["P"]),
        ("B_S", "S in BS₃", ELEM["B"]), ("Cl", "Cl", ELEM["Cl"]), ("O", "O (bonded to P)", ELEM["O"])]
HANGUL = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
WIN = (-8.0, 0.0)          # mean-3p 창 = 그림 표시 창 (CLAUDE.md 데이터 규율)
CYCLE = (2.5, 4.25)        # 우리 셀 작동창 V vs Li/Li+ (사용자 2026-11-09 "우리 cycle 은 저렇게 돌아가니까")

plt.rcParams.update({"svg.fonttype": "none", "font.family": "DejaVu Sans", "font.size": 12.5,
                     "axes.edgecolor": MUT, "axes.labelcolor": INK, "xtick.color": MUT, "ytick.color": MUT,
                     "text.color": INK, "axes.spines.top": False, "axes.spines.right": False})


def _minus(x: float, nd: int = 2) -> str:
    return f"{x:.{nd}f}".replace("-", "−")


def _svg(fig) -> str:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    return buf.getvalue()


def _arrow(ax, xy0, xy1, color=INK, lw=1.6, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(xy0, xy1, arrowstyle=style, mutation_scale=13, color=color, lw=lw, linestyle=ls))


def _level(ax, x0, x1, y, color, lw=3.0):
    ax.plot([x0, x1], [y, y], color=color, lw=lw, solid_capstyle="butt")


def _electrons(ax, x, y, n=2, color=INK, dy=0.22):
    for k in range(n):
        dx = -0.09 if k == 0 else 0.09
        if k == 0:
            _arrow(ax, (x + dx, y - dy), (x + dx, y + dy), color=color, lw=1.4)
        else:
            _arrow(ax, (x + dx, y + dy), (x + dx, y - dy), color=color, lw=1.4)


# ── 데이터 읽기 ──────────────────────────────────────────────────────────
def load_pdos():
    rows = list(csv.DictReader(open(PDOS_CSV)))
    E = [float(r["E_minus_VBM"]) for r in rows]
    cols = {k: [float(r[k]) for r in rows] for k, _, _ in SITE}
    return E, cols


def site_means(E, cols):
    out = {}
    for k, v in cols.items():
        w = [(e, y) for e, y in zip(E, v) if WIN[0] <= e <= WIN[1]]
        s = sum(y for _, y in w)
        out[k] = sum(e * y for e, y in w) / s
    return out


def load_mean_summary():
    m = {}
    for line in open(MEAN_CSV):
        if line.startswith("#") or line.startswith("site,"):
            continue
        p = line.split(",")
        if p[1].strip():
            m[{"B_S_BS3": "B_S"}.get(p[0], p[0])] = float(p[1])
    return m


def load_cohp(swap=False):
    rows = list(csv.reader(open(COHP_CSV)))
    hdr = rows[1]
    data = [[float(x) for x in r] for r in rows[2:]]
    idx = {h.replace("-pCOHP_", ""): i for i, h in enumerate(hdr)}
    nb = {r["bond"]: int(r["N"]) for r in csv.DictReader(open(NBOND_CSV))}
    E = [r[0] for r in data]
    per = {k: [r[idx[k]] / nb[k] for r in data] for k in BOND}
    if swap:                                           # 음성 시험: 열 바꿔치기
        per["P-S"], per["P-O"] = per["P-O"], per["P-S"]
    tot = [sum(abs(v) for v in r[1:]) for r in data]
    cb = next(e for e, t in zip(E, tot) if e > 0 and t >= 1e-3)
    vb = max(e for e, t in zip(E, tot) if e < 0 and t >= 1e-3)
    return E, per, vb, cb


def cumulative_antibonding(E, per, cb, upto=2.5):
    dE = E[1] - E[0]
    xs = [e - cb for e in E if cb <= e <= cb + upto]
    cum = {}
    for k, v in per.items():
        acc, c = 0.0, []
        for e, y in zip(E, v):
            if cb <= e <= cb + upto:
                acc += -min(0.0, y) * dE
                c.append(acc)
        cum[k] = c
    return xs, cum


def _phases(side: str):
    toks = [t.strip() for t in side.split(" + ")]
    out = []
    for t in toks:
        m = re.match(r"^([0-9.]+)\s+(\S+)$", t)
        out.append((float(m.group(1)), m.group(2)) if m else (1.0, t))
    return out


def load_profile():
    r = json.load(open(LEDGER))["results"]["o_only_03"]
    rows = []
    for s in sorted(r["profile"], key=lambda x: x["V_vs_Li"]):
        lhs, rhs = s["reaction"].split("->")
        prod = _phases(rhs)
        uptake = " Li" in lhs.replace("Li5.4", "")
        release = any(f == "Li" for _, f in prod)
        o_host = next(f for _, f in prod if "O" in re.sub(r"Cl", "", f))
        p_ph = [(c, f) for c, f in prod if "P" in f and "O" not in re.sub(r"Cl", "", f)]
        s_ph = [(c, f) for c, f in prod if "S" in f and "P" not in f]
        rows.append({"V": s["V_vs_Li"], "evolution_Li": s["evolution_Li"], "reaction": s["reaction"],
                     "Li": "uptake" if uptake else ("release" if release else "none"), "O_host": o_host,
                     "P_phase": max(p_ph)[1] if p_ph else "", "S_phase": max(s_ph)[1] if s_ph else ""})
    return rows


def tick_rows(rows):
    """눈금 = O 상이 바뀌는 행 + Li 교환이 바뀌는 행 (+ 0 V). 1.24 V 행은 둘 다 아니라 안 찍힌다."""
    keep = [rows[0]]
    for a, b in zip(rows, rows[1:]):
        if b["O_host"] != a["O_host"] or b["Li"] != a["Li"]:
            keep.append(b)
    return keep


# ── 그림 ────────────────────────────────────────────────────────────────
def fig_frontier():
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    ax.set_xlim(-1.6, 10.6)
    ax.set_ylim(-1.3, 8.4)
    ax.axis("off")
    ax.add_patch(Rectangle((3.0, 0.0), 4.0, 3.0, fc=FILL, ec=LINE))
    ax.add_patch(Rectangle((3.0, 3.0), 4.0, 1.6, fc=GAPBAND, ec="none"))
    ax.add_patch(Rectangle((3.0, 4.6), 4.0, 3.2, fc=FILL, ec=LINE))
    for y, lab in ((3.0, "VBM"), (4.6, "CBM")):
        ax.plot([2.7, 7.3], [y, y], color=GAPLINE, ls="--", lw=1.2)
        ax.text(7.4, y, lab, color=GAPLINE, va="center", fontsize=12)
    ax.text(5.0, 3.8, "band gap", ha="center", va="center", color=MUT, fontsize=12)
    ax.text(3.0, -0.38, "valence band (filled)", color=MUT, fontsize=11)
    ax.text(3.0, 7.95, "conduction band (empty)", color=MUT, fontsize=11)
    occ = [(2.72, "free S²⁻ lone pairs (4a/4d)", ELEM["S"]), (2.0, "P–S bonding (PS₄)", ELEM["P"]),
           (1.35, "Cl 3p", ELEM["Cl"]), (0.65, "O 2p (P–O bonding)", ELEM["O"])]
    for y, lab, c in occ:
        _level(ax, 3.4, 4.6, y, c, lw=4)
        ax.text(4.75, y, lab, va="center", fontsize=12, color=c)
    emp = [(5.1, "P–S σ* (antibonding)", ELEM["P"]), (5.9, "B–S σ*", ELEM["B"]),
           (7.0, "P–O σ*", ELEM["O"])]
    for y, lab, c in emp:
        _level(ax, 3.4, 4.6, y, c, lw=4)
        ax.text(4.75, y, lab, va="center", fontsize=12, color=c)
    _arrow(ax, (3.3, 2.72), (1.0, 3.75), color=ELEM["S"], lw=2.0)
    ax.text(-1.55, 4.0, "Oxidation:\ntake one electron out\nfrom the top (free S²⁻)", fontsize=12, color=INK)
    _arrow(ax, (1.2, 5.95), (3.35, 5.12), color=ELEM["P"], lw=2.0)
    ax.text(-1.55, 6.15, "Reduction:\nput one electron in\nat the bottom (P–S σ*)", fontsize=12, color=INK)
    ax.text(5.0, -1.25, "Ordering only (schematic). Voltages come from thermodynamics\n(grand potential), not from the gap.",
            ha="center", fontsize=11, color=MUT)
    return _svg(fig)


def fig_site_pdos(printed=None):
    E, cols = load_pdos()
    means = site_means(E, cols)
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    lo = 0.0
    for k, lab, c in SITE:
        y = cols[k]
        lw = 2.6 if k == "O" else 1.8
        ax.plot(E, y, color=c, lw=lw, label=lab)
    ymax = max(max(v[i] for i, e in enumerate(E) if WIN[0] <= e <= 0.2) for v in cols.values())
    ax.set_xlim(-8.0, 0.6)
    ax.set_ylim(lo, ymax * 1.42)
    ax.axvspan(0.0, 0.6, color=GAPBAND, lw=0)
    ax.axvline(0.0, color=GAPLINE, ls="--", lw=1.2)
    ax.text(0.06, ymax * 1.36, "gap", color=MUT, fontsize=11)
    order = sorted(SITE, key=lambda t: -means[t[0]])
    for j, (k, lab, c) in enumerate(order):
        m = means[k]
        txt = (printed or {}).get(k, _minus(m))
        yy = ymax * (1.30 - 0.105 * j)
        ax.plot([m, m], [0, yy - ymax * 0.03], color=c, lw=1.0, ls=":")
        ax.plot([m], [yy - ymax * 0.03], marker="v", color=c, ms=6)
        ax.text(m + 0.08, yy, f"{lab}: {txt} eV", color=c, fontsize=11.5, va="center")
    ax.set_xlabel("E − VBM (eV)")
    ax.set_ylabel("p-PDOS per atom (arb.)")
    ax.set_title("B₂O₃-doped LPSCl1.6 (PBE): site-resolved p-states, mean over −8..0 eV",
                 fontsize=12.5, color=INK, loc="left")
    ax.text(-7.9, ymax * 1.36, "shallower = oxidized first →", color=INK, fontsize=12)
    return _svg(fig), means


def fig_bond_order():
    fig, axs = plt.subplots(1, 3, figsize=(9.2, 5.0))
    cfg = [("P–S bond", -0.6, 1.6, 0, "bond order = (2 − 0)/2 = 1"),
           ("After reduction (+2 e⁻ in σ*)", -0.6, 1.6, 2, "bond order = (2 − 2)/2 = 0\n→ P–S breaks, S²⁻ leaves (Li₂S)"),
           ("Stronger bond: P–O", -1.45, 3.0, 0, "σ* far above the CBM:\nelectrons fill P–S σ* first")]
    for ax, (title, ys, ya, n_anti, note) in zip(axs, cfg):
        ax.set_xlim(0, 3)
        ax.set_ylim(-3.3, 3.6)
        ax.axis("off")
        ax.set_title(title, fontsize=12.5, color=INK)
        _level(ax, 0.15, 0.75, 0.55, ELEM["P"], lw=2.5)
        _level(ax, 2.25, 2.85, 0.25 if "O" not in title else -0.25, ELEM["O"] if "O" in title.split(":")[-1] else ELEM["S"], lw=2.5)
        ax.text(0.45, 0.8, "P", ha="center", color=ELEM["P"])
        ax.text(2.55, 0.5 if "O" not in title else 0.0, "O" if "O" in title.split(":")[-1] else "S", ha="center",
                color=ELEM["O"] if "O" in title.split(":")[-1] else ELEM["S"])
        _level(ax, 1.15, 1.85, ys, INK, lw=2.5)
        _level(ax, 1.15, 1.85, ya, ELEM["O"] if n_anti == 0 and "O" in title.split(":")[-1] else ELEM["P"], lw=2.5)
        for (x0, y0), (x1, y1) in (((0.75, 0.55), (1.15, ys)), ((0.75, 0.55), (1.15, ya)),
                                   ((2.25, 0.25 if "O" not in title else -0.25), (1.85, ys)),
                                   ((2.25, 0.25 if "O" not in title else -0.25), (1.85, ya))):
            ax.plot([x0, x1], [y0, y1], color=MUT, lw=0.8, ls=":")
        ax.text(1.95, ys, "σ", va="center", fontsize=13)
        ax.text(1.95, ya, "σ*", va="center", fontsize=13)
        _electrons(ax, 1.5, ys, 2)
        if n_anti:
            _electrons(ax, 1.5, ya, 2, color=ELEM["O"])
        ax.text(1.5, -2.05, note, ha="center", va="top", fontsize=11.5, color=INK)
    axs[2].plot([0.05, 2.95], [1.6, 1.6], color=GAPLINE, ls="--", lw=1.2)
    axs[2].text(0.05, 1.75, "CBM (= P–S σ*)", color=GAPLINE, fontsize=11)
    fig.text(0.5, -0.02, "Antibonding σ* has a node between the atoms: filling it cancels the bond.\nStronger overlap → larger σ/σ* split.", ha="center", fontsize=11, color=MUT)
    return _svg(fig)


def fig_cohp(swap=False):
    E, per, vb, cb = load_cohp(swap=swap)
    xs, cum = cumulative_antibonding(E, per, cb)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 4.8), gridspec_kw={"width_ratios": [1.45, 1]})
    a1.axvspan(vb, cb, color=GAPBAND, lw=0)
    for x, lab in ((vb, "VB edge"), (cb, "CB edge")):
        a1.axvline(x, color=GAPLINE, ls="--", lw=1.1)
    a1.axhline(0, color=MUT, lw=0.8)
    for k, c in BOND.items():
        a1.plot(E, per[k], color=c, lw=2.6 if k == "P-O" else 1.8, label=k.replace("-", "–"))
    a1.set_xlim(-1.5, 3.6)
    sel = [v for e, row in zip(E, zip(*per.values())) if -1.5 <= e <= 3.6 for v in row]
    a1.set_ylim(min(sel) * 1.1, 0.55)
    a1.text(-1.45, 0.22, "↑ bonding", fontsize=11, color=MUT)
    a1.text(-1.45, -0.6, "↓ antibonding (σ*)", fontsize=11, color=MUT)
    a1.set_xlabel("E − E_F (eV, LOBSTER; 0.1 eV smoothing)")
    a1.set_ylabel("−pCOHP per bond (bonding > 0)")
    a1.legend(frameon=False, loc="lower left", fontsize=11.5)
    a1.set_title("Who owns the empty states (B₂O₃-doped)", fontsize=12.5, loc="left")
    for k, c in BOND.items():
        a2.plot(xs, cum[k], color=c, lw=2.6 if k == "P-O" else 1.8, label=k.replace("-", "–"))
    a2.set_xlim(0, 2.5)
    a2.set_xlabel("E − CB edge (eV)")
    a2.set_ylabel("cumulative σ* weight per bond")
    a2.set_title("σ* weight a bond can accept", fontsize=12.5, loc="left")
    a2.legend(frameon=False, loc="upper left", fontsize=11.5)
    return _svg(fig), (E, per, vb, cb, xs, cum)


PH_COLOR = {"Li2O": "#fda4af", "Li3PO4": ELEM["O"], "Li4P2O7": "#e11d48", "LiPO3": "#9f1239", "P2O5": "#4c0519",
            "Li3P": "#c4b5fd", "Li-P": "#a78bfa", "P": "#8b5cf6", "Li3PS4": ELEM["P"], "P2S7": "#5b21b6",
            "Li2S": "#fdba74", "LiS4": ELEM["S"], "S": "#9a3412", "SCl": "#7c2d12"}


def _pretty(f):
    return re.sub(r"(\d+)", lambda m: "".join("₀₁₂₃₄₅₆₇₈₉"[int(d)] for d in m.group(1)), f)


def fig_o_host(printed=None):
    rows = load_profile()
    vmax = 4.45
    segs = {"O_host": [], "P_phase": [], "S_phase": []}
    for i, r in enumerate(rows):
        v0, v1 = r["V"], rows[i + 1]["V"] if i + 1 < len(rows) else vmax
        for key in segs:
            lab = r[key]
            if key == "P_phase" and lab in ("LiP", "Li3P7", "LiP7"):
                lab = "Li-P"
            if segs[key] and segs[key][-1][2] == lab:
                segs[key][-1][1] = v1
            else:
                segs[key].append([v0, v1, lab])
    fig, ax = plt.subplots(figsize=(9.6, 6.0))
    ax.set_xlim(0, vmax)
    ax.set_ylim(-0.2, 4.95)
    for spine in ("left",):
        ax.spines[spine].set_visible(False)
    ax.set_yticks([])
    tracks = [("O_host", 2.9, "O ends up in"), ("P_phase", 1.75, "P (from PS₄) becomes"), ("S_phase", 0.6, "S becomes")]
    for key, y, lab in tracks:
        ax.text(-0.03, y + 0.42, lab, ha="left", fontsize=11.5, color=MUT, transform=ax.transData)
        for v0, v1, ph in segs[key]:
            c = PH_COLOR.get(ph, MUT)
            ax.add_patch(Rectangle((v0, y), v1 - v0, 0.32, fc=c, ec="white", lw=1.2))
            if v1 - v0 >= 0.25:
                light = ph in ("Li2O", "Li3P", "Li-P", "Li2S")
                ax.text((v0 + v1) / 2, y + 0.16, "Li–P" if ph == "Li-P" else _pretty(ph), ha="center", va="center",
                        fontsize=11, color=INK if light else "white", fontweight="bold" if ph == "Li3PO4" else "normal")
            elif key == "O_host":
                ax.text((v0 + v1) / 2, y + 0.40, _pretty(ph), ha="center", va="bottom", fontsize=9.5, color=PH_COLOR.get(ph, MUT))
    li_up = max(r["V"] for r in rows if r["Li"] == "uptake")
    neutral = [r["V"] for r in rows if r["Li"] == "none"]
    rel0 = min(r["V"] for r in rows if r["Li"] == "release")
    lo_none = min(neutral)
    ax.axvspan(lo_none, rel0, color=GAPBAND, lw=0, zorder=0)
    ax.text(lo_none / 2, 4.45, "Li uptake (reduction):\nP is reduced", ha="center", va="center", fontsize=12, color=ELEM["P"])
    ax.text((lo_none + rel0) / 2, 4.45, "no Li\nexchange", ha="center", fontsize=11, color=MUT, va="center")
    ax.text((rel0 + vmax) / 2, 4.45, "Li release (oxidation):\nS (then Cl) is oxidized", ha="center", va="center", fontsize=12, color=ELEM["S"])
    ticks = tick_rows(rows)
    labels = printed or [("0" if t["V"] == 0 else f"{t['V']:.2f}") for t in ticks]
    ax.set_xticks([t["V"] for t in ticks])
    ax.set_xticklabels(labels, fontsize=10.5)
    for t in ticks[1:]:
        ax.axvline(t["V"], color=MUT, lw=0.6, ls=":", zorder=0)
    ax.set_xlabel("Voltage vs Li/Li⁺ (V) — grand potential (MP hull, 0 K, Li open)")
    ax.set_title("O-only control Li₅.₄PS₄.₁O₀.₃Cl₁.₆: Li₃PO₄ is the same "
                 "P⁵⁺–O²⁻ unit on both sides", fontsize=12.5, loc="left")
    ax.text(0.02, 3.86, "below 0.69 V: Li₃PO₄ + 8 Li → Li₃P + 4 Li₂O", fontsize=10.5, color=INK)
    ax.add_patch(Rectangle((CYCLE[0], 0.3), CYCLE[1] - CYCLE[0], 3.42, fc="#e0f2fe", ec="none", zorder=0))
    for x in CYCLE:
        ax.plot([x, x], [0.3, 3.72], color=ELEM["N"], ls="--", lw=1.3, zorder=1)
    ax.text(sum(CYCLE) / 2, 3.86, f"our cycling window {CYCLE[0]}–{CYCLE[1]} V vs Li/Li⁺", ha="center",
            fontsize=11, color=ELEM["N"], fontweight="bold")
    _ = li_up
    return _svg(fig), rows, ticks, labels


def fig_buried_contact():
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.9))
    titles = ("Inside the SE (buried):\nelectrons arrive slowly", "Direct contact with Li metal:\nelectron flood")
    fills = ({"P-S": 2, "B-S": 0, "P-O": 0}, {"P-S": 2, "B-S": 2, "P-O": 1})
    results = ("P–S cut · B–S kept · P–O kept",
               "P–S cut · B–S cut · P–O cut in 1 of 2 seeds")
    for ax, title, fill, res in zip(axs, titles, fills, results):
        ax.set_xlim(0, 4)
        ax.set_ylim(-0.6, 4.4)
        ax.axis("off")
        ax.set_title(title, fontsize=12.5, color=INK)
        for (k, y) in (("P-S", 1.0), ("B-S", 2.0), ("P-O", 3.1)):
            _level(ax, 1.6, 2.6, y, BOND[k], lw=3)
            ax.text(2.75, y, k.replace("-", "–") + " σ*" + (" (= CBM)" if k == "P-S" else ""), va="center", color=BOND[k], fontsize=12)
            if fill[k]:
                _electrons(ax, 2.1, y, fill[k], color=ELEM["O"] if fill[k] == 2 else MUT)
        if "metal" in title:
            ax.add_patch(Rectangle((0.05, 0.3), 0.75, 3.2, fc="#d1d5db", ec=MUT))
            ax.text(0.42, 1.9, "Li\nmetal", ha="center", va="center", fontsize=12)
            for y in (1.0, 2.0, 3.1):
                _arrow(ax, (0.85, y), (1.55, y), color=ELEM["Li"], lw=1.8)
        else:
            _arrow(ax, (0.6, 1.0), (1.55, 1.0), color=ELEM["Li"], lw=1.8)
            ax.text(0.05, 1.25, "e⁻ one by one", fontsize=11, color=ELEM["Li"])
        ax.text(2.0, -0.45, res, ha="center", fontsize=12, color=INK)
    fig.text(0.5, -0.04, "Interface MD (MLIP/UMA, B₂O₃-doped model, 2 seeds).\nAt contact, what decides is whether the products block electrons and stay as a wall.", ha="center", fontsize=10.5, color=MUT)
    return _svg(fig)


# ── 검사 ────────────────────────────────────────────────────────────────
def _texts(svg: str) -> list[str]:
    root = ET.fromstring(svg)
    return ["".join(el.itertext()) for el in root.iter() if el.tag.endswith("text")]


def check(svgs: dict, extra: dict) -> list[str]:
    fails = []
    for name, svg in svgs.items():
        try:
            txt = _texts(svg)
        except ET.ParseError as e:
            fails.append(f"{name}: XML 깨짐 ({e})")
            continue
        bad = [t for t in txt if HANGUL.search(t)]
        if bad:
            fails.append(f"{name}: 글자 노드에 한글 {bad[:2]}")
    if "02" in extra:
        means, svg = extra["02"]
        summ = load_mean_summary()
        joined = " ".join(_texts(svg)).replace("−", "-")
        for k, m in means.items():
            if f"{m:.2f}" not in joined:
                fails.append(f"02: {k} 평균 {m:.2f} 가 그림 글자에 없다")
            if k in summ and abs(summ[k] - m) > 0.01:
                fails.append(f"02: {k} 평균 {m:.3f} 이 원장 요약 {summ[k]} 와 다르다")
        if not (means["free_S"] > means["PS4_S"] > means["Cl"] > means["O"]):
            fails.append("02: 순서 free S > PS4 S > Cl > O 가 아니다")
    if "04" in extra:
        E, per, vb, cb, xs, cum = extra["04"]
        i05 = max(i for i, x in enumerate(xs) if x <= 0.5)
        if not (cum["P-S"][i05] > cum["B-S"][i05] and cum["P-S"][i05] > cum["P-O"][i05]):
            fails.append("04: 띠 가장자리 +0.5 eV 안에서 P–S 반결합 무게가 가장 크지 않다")
        if not (cum["P-S"][-1] >= 3 * cum["B-S"][-1] and cum["P-S"][-1] >= 3 * cum["P-O"][-1]):
            fails.append("04: +2.5 eV 안 P–S 무게가 다른 둘의 3 배 미만")
    if "05" in extra:
        rows, ticks, labels, svg = extra["05"]
        want = ["0" if t["V"] == 0 else f"{t['V']:.2f}" for t in ticks]
        if list(labels) != want:
            fails.append(f"05: 찍힌 눈금 {list(labels)} ≠ 원장 {want}")
        joined = " ".join(_texts(svg))
        for w in want:
            if w not in joined:
                fails.append(f"05: 눈금 {w} 가 그림 글자에 없다")
        seq = []
        for r in rows:
            if not seq or seq[-1] != r["O_host"]:
                seq.append(r["O_host"])
        if seq != ["Li2O", "Li3PO4", "Li4P2O7", "LiPO3", "P2O5"]:
            fails.append(f"05: O 상 순서 {seq}")
        if f"{CYCLE[0]}–{CYCLE[1]} V" not in joined:
            fails.append("05: 작동창 표시가 그림 글자에 없다")
        if any(abs(t["V"] - 1.242) < 1e-3 for t in ticks):
            fails.append("05: 1.24 V 행이 눈금에 들어갔다 (환원 한계로 읽힌다)")
    return fails


def build(**neg) -> tuple[dict, dict]:
    s02, means = fig_site_pdos(printed=neg.get("printed02"))
    s04, d04 = fig_cohp(swap=neg.get("swap04", False))
    s05, rows, ticks, labels = fig_o_host(printed=neg.get("printed05"))
    svgs = {"rf_01_frontier_map": fig_frontier(), "rf_02_site_pdos": s02, "rf_03_bond_order": fig_bond_order(),
            "rf_04_cohp_unoccupied": s04, "rf_05_o_host_vs_voltage": s05, "rf_06_buried_vs_contact": fig_buried_contact()}
    if neg.get("hangul"):
        svgs["rf_01_frontier_map"] = svgs["rf_01_frontier_map"].replace(">Oxidation:", ">산화 Oxidation:")
    if neg.get("broken"):
        svgs["rf_03_bond_order"] = svgs["rf_03_bond_order"][:-40]
    return svgs, {"02": (means, s02), "04": d04, "05": (rows, ticks, labels, s05)}


def selftest() -> int:
    fails = []
    svgs, extra = build()
    pos = check(svgs, extra)
    if pos:
        fails.append(f"양성 실패: {pos}")
    cases = {"한글 라벨": {"hangul": True}, "02 숫자 바꿈": {"printed02": {"free_S": "−1.40"}},
             "04 열 바꿔치기": {"swap04": True}, "깨진 XML": {"broken": True}}
    rows = load_profile()
    t = tick_rows(rows)
    lab = ["0" if x["V"] == 0 else f"{x['V']:.2f}" for x in t]
    lab[3] = "2.10"
    cases["05 전압 바꿈"] = {"printed05": lab}
    for name, kw in cases.items():
        s, e = build(**kw)
        if not check(s, e):
            fails.append(f"음성 '{name}' 을 못 잡았다")
    for f in fails:
        print("✗", f)
    print(f"selftest {'PASS' if not fails else 'FAIL'} ({len(fails)} 실패 · 양성 1 · 음성 {len(cases)})")
    return 1 if fails else 0


def write_origin(extra: dict) -> None:
    E, per, vb, cb, xs, cum = extra["04"]
    with open(ORIGIN_COHP, "w", newline="") as f:
        f.write(f"# per-bond -pCOHP (bonding>0), B2O3-doped LPSCl1.6, LOBSTER, Gaussian 0.1 eV; source {COHP_CSV.relative_to(ROOT)}"
                f" divided by bond counts in {NBOND_CSV.relative_to(ROOT)}; band edges (sum|COHP|>=1e-3): VB {vb:.4f} CB {cb:.4f} eV\n")
        w = csv.writer(f)
        w.writerow(["E_minus_EF_eV", "mpCOHP_per_bond_PS", "mpCOHP_per_bond_BS", "mpCOHP_per_bond_PO"])
        for i, e in enumerate(E):
            w.writerow([f"{e:.4f}"] + [f"{per[k][i]:.6f}" for k in ("P-S", "B-S", "P-O")])
    rows, ticks, labels, _ = extra["05"]
    with open(ORIGIN_PROFILE, "w", newline="") as f:
        f.write(f"# O-only control Li5.4PS4.1O0.3Cl1.6, grand potential (Li open), source {LEDGER.relative_to(ROOT)} results.o_only_03;"
                " V = lower edge of the interval where the reaction holds (HZ-esw-reduction-limit-label)\n")
        w = csv.writer(f)
        w.writerow(["V_vs_Li", "evolution_Li_per_fu", "Li_exchange", "O_host_phase", "P_phase", "S_phase", "reaction"])
        for r in rows:
            w.writerow([f"{r['V']:.3f}", r["evolution_Li"], r["Li"], r["O_host"], r["P_phase"], r["S_phase"], r["reaction"]])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--png", help="PNG 미리보기를 쓸 폴더 (저장소 밖)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    svgs, extra = build()
    fails = check(svgs, extra)
    if fails:
        for f in fails:
            print("✗", f)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in svgs.items():
        (OUT / f"{name}.svg").write_text(svg)
    write_origin(extra)
    print(f"그림 {len(svgs)} 장 → {OUT.relative_to(ROOT)} · Origin CSV 2 → {ORIGIN_COHP.name} · {ORIGIN_PROFILE.name}")
    if a.png:
        try:
            import cairosvg  # noqa: F401
        except ImportError:
            print("PNG 미리보기: cairosvg 없음 — 건너뜀")
            return 0
        for name, svg in svgs.items():
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(Path(a.png) / f"{name}.png"), dpi=110)
        print(f"PNG 미리보기 → {a.png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
