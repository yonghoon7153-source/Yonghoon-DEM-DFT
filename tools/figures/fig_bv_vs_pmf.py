#!/usr/bin/env python3
"""fig_bv_vs_pmf.py — **BV 프록시 vs MD PMF** 를 한 장에 (LPSCl1.6).

1저자 요청(2026-08-05): "프록시 vs 실제"를 나란히.

  ① BV 경로 프로파일 (0 K, 빈 격자, Li 프로브 1개) — E_perc
  ② MD PMF 경로 프로파일 (600 K, Li 27개 전부, 골격 진동 포함) — F*
  ③ 최대 연결 성분 곡선 — **첫-관통 vs 전이점** 두 정의와 블록 수렴 산포

두 프로파일은 **같은 관례**(26-연결 감김 판정 · 선적분 최소 경로 · 랩해제 mesh metric)로
뽑혔기 때문에 축이 같고 나란히 읽을 수 있다.

  python3 tools/figures/fig_bv_vs_pmf.py --pmf_dir <pmf 산출 폴더> --tag modelc_T600
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT, SYS                                   # noqa: E402

BV_CSV = ROOT / "db/properties/bv_path_profile_origin.csv"


def load_bv(system="modelc"):
    with open(BV_CSV, encoding="utf-8-sig") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].lstrip('"﻿').startswith("#")]
    hdr = rows[0]
    ix, iy = hdr.index(f"{system}_d_A"), hdr.index(f"{system}_E_eV")
    d, e = [], []
    for r in rows[1:]:
        if r[ix].strip():
            d.append(float(r[ix])); e.append(float(r[iy]))
    return np.array(d), np.array(e)


def load_csv2(path):
    with open(path, encoding="utf-8-sig") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].lstrip('"﻿').startswith("#")]
    return (np.array([float(r[0]) for r in rows[1:]]),
            np.array([float(r[1]) for r in rows[1:]]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmf_dir", required=True)
    ap.add_argument("--tag", default="modelc_T600")
    ap.add_argument("--system", default="modelc")
    ap.add_argument("--disp", default="LPSCl1.6")
    ap.add_argument("--T", type=float, default=600)
    ap.add_argument("--E_perc", type=float, default=0.2283)
    ap.add_argument("--blocks", default="0.1875,0.1675,0.1825",
                    help="블록 수렴 검사 F* 들 (half1,half2,quarter)")
    ap.add_argument("--out", default="docs/figures/bv_vs_pmf_modelc.png")
    a = ap.parse_args()

    P = Path(a.pmf_dir)
    dbv, ebv = load_bv(a.system)
    dpm, epm = load_csv2(P / f"{a.tag}_pmf_profile.csv")
    lv, pct = load_csv2(P / f"{a.tag}_pmf_cluster.csv")
    dp = np.diff(pct) / np.diff(lv)
    k = int(np.argmax(dp)); F_trans = 0.5 * (lv[k] + lv[k + 1])
    span = float(lv[np.argmax(pct > 0.5 * pct.max())])          # 참고용
    blocks = [float(x) for x in a.blocks.split(",") if x.strip()]

    fig, axes = plt.subplots(1, 3, figsize=(16.4, 4.9))

    ax = axes[0]
    ax.axhspan(0, a.E_perc, color="#f1f5f9", zorder=0)
    ax.plot(dbv, ebv, color=SYS[a.system], lw=2.0)
    ax.axhline(a.E_perc, ls="--", lw=1.2, color=INK)
    ax.text(dbv[-1], a.E_perc + 0.005, f"$E_{{perc}}$ = {a.E_perc:.3f} eV",
            ha="right", fontsize=10, color=INK, fontweight="bold")
    ax.set_title("① BV proxy — 0 K, empty lattice, one Li probe",
                 fontsize=11.5, color=INK)
    ax.set_ylabel("Energy (eV)", fontsize=11)

    ax = axes[1]
    ax.axhspan(0, F_trans, color="#eef6ff", zorder=0)
    ax.plot(dpm, epm, color="#0284c7", lw=2.0)
    ax.axhline(F_trans, ls="--", lw=1.2, color=INK)
    ax.text(dpm[-1], F_trans + 0.005, f"$F^*$ = {F_trans:.3f} eV",
            ha="right", fontsize=10, color=INK, fontweight="bold")
    ax.set_title(f"② MD PMF — {a.T:.0f} K, all 27 Li, vibrating framework",
                 fontsize=11.5, color=INK)
    ax.set_ylabel(f"Free energy at {a.T:.0f} K (eV)", fontsize=11)

    for ax in axes[:2]:
        ax.set_xlabel("Reaction coordinate (Å)", fontsize=11)
        ax.set_ylim(-0.02, max(a.E_perc, F_trans) * 1.45)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    ax = axes[2]
    ax.plot(lv, pct, color="#0284c7", lw=2.0)
    ax.axvline(F_trans, ls="--", lw=1.2, color="#dc2626")
    ax.text(F_trans + 0.006, pct.max() * 0.55,
            f"transition (adopted)\n$F^*$ = {F_trans:.3f} eV", fontsize=9.5,
            color="#dc2626", fontweight="bold")
    if blocks:
        ax.axvspan(min(blocks), max(blocks), color="#dc2626", alpha=0.10, zorder=0)
        ax.text(np.mean(blocks), pct.max() * 0.30,
                f"block scatter\n±{(max(blocks)-min(blocks))/2*1000:.0f} meV",
                fontsize=8.5, color="#dc2626", ha="center")
    ax.set_xlabel("PMF level F (eV)", fontsize=11)
    ax.set_ylabel("largest connected Li cluster (% of cell)", fontsize=11)
    ax.set_title("③ percolation transition + convergence", fontsize=11.5, color=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.suptitle(f"{a.disp} — bond-valence proxy vs MD free-energy landscape "
                 f"(same percolation conventions)", fontsize=13.5, color=INK,
                 fontweight="bold")
    fig.text(0.5, -0.03,
             "Both profiles use the identical pipeline (26-connectivity winding percolation, "
             "minimum-energy-line-integral path, PBC-unwrapped mesh metric); only the input "
             "field differs.\nThe BV map knows no Li, no vacancies and no temperature; the PMF "
             "is built from the time-averaged Li density of the MD trajectory. "
             "F* is a free energy at this temperature — not an activation energy.",
             ha="center", fontsize=8.8, color=MUT)
    fig.tight_layout()
    fig.savefig(ROOT / a.out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {a.out}")
    print(f"   BV E_perc {a.E_perc:.4f} · PMF F* {F_trans:.4f} eV · 차이 "
          f"{(a.E_perc - F_trans)*1000:+.0f} meV")


if __name__ == "__main__":
    main()
