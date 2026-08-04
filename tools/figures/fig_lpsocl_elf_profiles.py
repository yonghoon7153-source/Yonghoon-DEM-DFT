#!/usr/bin/env python3
"""fig_lpsocl_elf_profiles.py — LPSOCl 결합별 ELF 프로파일 (bond path 를 따라간 곡선).

왜 곡선인가
  결합 중점값(midpoint) 한 점만 보면 **짧은 결합에서 상대 원자의 lone-pair 에 걸려**
  실제보다 높게 읽힌다. Li–O 가 중점 0.784 인데 central min 0.163 인 것이 그 실증.
  곡선을 그려야 골이 어디에 있고 얼마나 깊은지가 눈에 보인다.

⚠⚠ **판정 창은 [0.40, 0.60] 이다 — 곡선 전체의 최솟값이 아니다.**
  Li 계열 결합은 frac 0.6~0.7 근처에서 ELF 가 0.03~0.08 까지 떨어지는데, 이건 결합이
  아니라 **Li 의 1s|2s 코어 노드**다 (Li.pbe-sl-kjpaw 는 1s 가 valence 라 Li 핵에서
  ELF→1.0 이 되고 그 안쪽에 노드가 생긴다). 원자 성질이지 결합 성질이 아니다.
  실제로 그 깊은 골로 줄을 세우면 Li–Cl 0.034 < Li–O 0.066 < Li–S 0.077 로
  **순서가 뒤집힌다** — Li–X 세 결합의 Li 코어 노드 깊이를 비교한 것뿐이라 의미가 없다.
  db/properties/lpsocl_elf_bond_midpoint.csv 의 ELF_central_min 은 [0.40,0.60] 최솟값이고
  (tools/figures/sample_elf_bonds.py:103), 이 그림도 **같은 창**으로 주석을 단다.

⚠ 프로파일 CSV 는 결합종마다 **대표 1개** 결합, 중점 CSV 의 central_min 은 **n개 평균**이다.
  인용 표준은 평균 쪽. 그림에는 둘 다 적어 어느 쪽인지 분명히 한다.

  python3 tools/figures/fig_lpsocl_elf_profiles.py
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT, apply_axes                        # noqa: E402

SRC = ROOT / "db/properties/lpsocl_elf_profiles_origin.csv"
MID = ROOT / "db/properties/lpsocl_elf_bond_midpoint.csv"
OUT = ROOT / "docs/figures/icohp/lpsocl_elf_profiles.png"
CSVOUT = ROOT / "db/properties/lpsocl_elf_profile_minima.csv"

CLO, CHI = 0.40, 0.60        # 판정 창 — sample_elf_bonds.py 와 동일해야 한다
COV, ION = 0.70, 0.30        # 공유/이온 판정선 (문헌 관례)

# 열 이름 → (표시명, 왼쪽원자, 오른쪽원자, 색, 굵기, 선모양, 중점 CSV 키, Li 코어 유무)
#   O 를 낀 결합만 crimson (도판트 강조), 둘은 실선/파선으로 구분.
BONDS = [
    ("ELF_P-S_2.05A",        "P–S",           "P",  "S",  "#7c3aed", 2.0, "-",  "P-S",   False),
    ("ELF_P-O_1.56A",        "P–O",           "P",  "O",  "#be123c", 2.6, "-",  "O-P",   False),
    ("ELF_S(free)-Li_2.34A", "Li–S (free S)", "S",  "Li", "#c05621", 2.0, "-",  "Li-S",  True),
    ("ELF_Cl-Li_2.56A",      "Li–Cl",         "Cl", "Li", "#65a30d", 2.0, "-",  "Cl-Li", True),
    ("ELF_O-Li_1.95A",       "Li–O",          "O",  "Li", "#be123c", 2.6, "--", "Li-O",  True),
]


def load_profiles():
    with open(SRC, encoding="utf-8-sig") as f:
        lines = [l for l in f if not l.lstrip("﻿").startswith("#")]
    r = csv.DictReader(lines)
    cols = {k: [] for k in r.fieldnames}
    for row in r:
        for k, v in row.items():
            cols[k].append(float(v))
    return {k: np.asarray(v) for k, v in cols.items()}


def load_midpoint():
    if not MID.exists():
        return {}
    return {row["bond"]: row for row in csv.DictReader(open(MID, encoding="utf-8-sig"))}


def win_min(frac, y, lo, hi):
    m = (frac >= lo - 1e-9) & (frac <= hi + 1e-9)
    i = int(np.argmin(y[m]))
    return float(frac[m][i]), float(y[m][i])


def core_node(frac, y):
    """Li 쪽 코어 노드: frac 0.6~0.9 구간의 최솟값 (결합 성질 아님 — 표시만)."""
    return win_min(frac, y, 0.60, 0.90)


def main():
    P = load_profiles()
    MIDR = load_midpoint()
    frac = P["frac"]

    fig, axes = plt.subplots(2, 3, figsize=(14.6, 8.2))
    axes = axes.ravel()
    rows = []

    for ax, (col, name, a1, a2, color, lw, ls, midkey, has_core) in zip(axes, BONDS):
        y = P[col]
        d = float(col.rsplit("_", 1)[-1].rstrip("A"))
        xm, ym = win_min(frac, y, CLO, CHI)
        m = MIDR.get(midkey, {})
        mean_cmin = float(m["ELF_central_min"]) if m.get("ELF_central_min") else float("nan")

        # ⚠ ylim 을 1.32 로 띄워 **곡선이 절대 안 닿는 머리 공간**을 만든다.
        #   Li 결합은 Li 핵에서 ELF=1.0 까지 올라가므로 1.06 으로 두면 주석이 곡선에 겹친다.
        ax.axvspan(CLO, CHI, color="#fef9c3", zorder=0)
        ax.axhline(COV, color="#0d9488", ls=":", lw=1.1, zorder=1)
        ax.axhline(ION, color="#be123c", ls=":", lw=1.1, zorder=1)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.32)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.plot(frac, y, color=color, lw=lw, ls=ls, zorder=3)
        ax.plot([xm], [ym], "o", ms=7.5, mfc="white", mec=color, mew=2.2, zorder=5)

        verdict = ("covalent" if ym > COV else "ionic" if ym < ION else "polar / intermediate")
        vcol = "#0d9488" if ym > COV else "#be123c" if ym < ION else MUT
        ax.text(0.5, 0.945, f"central min {ym:.3f}", transform=ax.transAxes,
                ha="center", fontsize=10.5, color=color, fontweight="bold")
        ax.text(0.5, 0.868, verdict, transform=ax.transAxes, ha="center",
                fontsize=10, color=vcol, fontweight="bold")

        # 끝점 원자 이름 — 어느 방향으로 읽는지 헷갈리지 않게
        for xx, lab, ha in ((0.012, a1, "left"), (0.988, a2, "right")):
            ax.text(xx, 0.035, lab, transform=ax.transAxes, ha=ha, fontsize=11,
                    color=INK, fontweight="bold")

        if has_core:
            cx, cy = core_node(frac, y)
            ax.plot([cx], [cy], "v", ms=6.5, mfc="none", mec=MUT, mew=1.4, zorder=5)
            ax.annotate(f"Li 1s|2s core node {cy:.3f}\natomic — not the bond",
                        (cx, cy), xycoords="data", xytext=(0.985, 0.205),
                        textcoords="axes fraction", ha="right", va="center",
                        fontsize=8, color=MUT,
                        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=MUT, lw=0.6),
                        arrowprops=dict(arrowstyle="-", color=MUT, lw=0.7,
                                        shrinkA=2, shrinkB=4))
        if m:
            ax.text(0.5, -0.235, f"n = {m['n_bonds']} bonds · mean central min "
                                 f"{mean_cmin:.3f} · mean midpoint {float(m['ELF_midpoint']):.3f}",
                    transform=ax.transAxes, ha="center", fontsize=8.5, color=MUT)

        apply_axes(ax, xlabel="fraction along bond path", ylabel="ELF",
                   title=f"{name}   ({d:.2f} Å, this bond)", fontsize=11)
        rows.append((name, d, xm, ym, midkey, has_core,
                     core_node(frac, y)[1] if has_core else None))

    # ── 6번째 패널: 전부 겹쳐 그려 순서를 한눈에 ──────────────────────────────
    ax = axes[5]
    ax.axvspan(CLO, CHI, color="#fef9c3", zorder=0)
    ax.axhline(COV, color="#0d9488", ls=":", lw=1.1, zorder=1)
    ax.axhline(ION, color="#be123c", ls=":", lw=1.1, zorder=1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.32)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    for col, name, *_rest in BONDS:
        color, lw, ls = _rest[2], _rest[3], _rest[4]
        ax.plot(frac, P[col], color=color, lw=lw, ls=ls, label=name, zorder=3)
    for yy, txt, cc in ((COV + 0.02, "covalent  > 0.70", "#0d9488"),
                        (ION - 0.075, "ionic  < 0.30", "#be123c")):
        ax.text(0.995, yy, txt, ha="right", fontsize=9, color=cc,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    ax.text(0.50, 0.022, "judging window [0.40, 0.60]", transform=ax.transAxes,
            ha="center", fontsize=8.5, color="#92400e")
    ax.legend(frameon=False, fontsize=8.5, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, 1.02), columnspacing=1.1, handlelength=1.8)
    apply_axes(ax, xlabel="fraction along bond path", ylabel="ELF",
               title="all bonds overlaid", fontsize=11)

    fig.suptitle("LPSOCl1.6 (Li₂₇P₅S₂₁OCl₈) — ELF along each bond path.  "
                 "Host P–S / P–O stay covalent; Li–O is the most ionic Li bond.",
                 fontsize=12.5, color=INK, y=0.995)
    fig.text(0.5, 0.004,
             "Yellow band = the [0.40, 0.60] window the descriptor is taken from. "
             "On Li bonds the deep dip near 0.65 is the Li 1s|2s core node "
             "(Li 1s is in valence), an atomic feature — ranking by it would be meaningless.",
             ha="center", fontsize=9, color=MUT)
    fig.tight_layout(rect=[0, 0.022, 1, 0.972], h_pad=3.4)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {OUT}")

    with open(CSVOUT, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# LPSOCl ELF bond-path minima — annotations of docs/figures/icohp/lpsocl_elf_profiles.png\n")
        f.write("# descriptor = min of ELF over frac [0.40,0.60] (sample_elf_bonds.py 와 동일 규약)\n")
        f.write("# this_bond_* = 대표 1개 결합(프로파일 곡선). mean_* = n개 평균 = **인용 표준**.\n")
        f.write("# li_core_node = Li 1s|2s 노드 깊이. 원자 성질이라 **결합 순위에 쓰면 안 된다**.\n")
        f.write("# 곡선 원본: db/properties/lpsocl_elf_profiles_origin.csv\n")
        w = csv.writer(f)
        w.writerow(["bond", "this_bond_dist_A", "central_min_frac", "this_bond_central_min",
                    "n_bonds", "mean_central_min", "mean_midpoint", "li_core_node", "verdict"])
        for name, d, xm, ym, midkey, has_core, cnode in rows:
            m = MIDR.get(midkey, {})
            w.writerow([name, f"{d:.2f}", f"{xm:.3f}", f"{ym:.4f}",
                        m.get("n_bonds", ""), m.get("ELF_central_min", ""),
                        m.get("ELF_midpoint", ""),
                        f"{cnode:.4f}" if cnode is not None else "",
                        "covalent" if ym > COV else "ionic" if ym < ION else "intermediate"])
    print(f"→ {CSVOUT}")

    print("\n결합별 central min ([0.40,0.60]) — 대표 1결합 vs n개 평균:")
    worst = 0.0
    for name, d, xm, ym, midkey, has_core, cnode in rows:
        m = MIDR.get(midkey, {})
        mm = float(m["ELF_central_min"]) if m.get("ELF_central_min") else float("nan")
        worst = max(worst, 0.0 if np.isnan(mm) else abs(mm - ym))
        core = f"   [Li core node {cnode:.3f} — 무시]" if cnode is not None else ""
        print(f"  {name:14s} {d:.2f} Å  {ym:.3f} @ frac {xm:.2f}"
              f"   (mean over {m.get('n_bonds','?'):>2s}: {mm:.3f}){core}")
    print(f"\n대표결합 vs 평균 최대 편차 {worst:.3f} — "
          + ("규약 일치 ✓" if worst < 0.05 else "⚠ 0.05 초과, 대표결합 선택 확인 필요"))


if __name__ == "__main__":
    main()
