#!/usr/bin/env python3
"""fig_bv_path_annotated.py — BV 경로 프로파일 **자리 라벨 + 구간별 장벽** 판.

1저자 질문(2026-08-05): 외부 발표자료(POSCO)의 "경로별 energy barrier" 그림처럼
우리도 되나? → 된다. 그 그림에 있고 우리 4계 판에 없던 두 가지를 채운다:
  ① 골짜기/봉우리마다 **결정학적 정체**를 붙인다 (어느 Li 자리인가 · 어느 음이온 창인가)
  ② **구간별 장벽**(직전 골짜기 → 그 봉우리)을 각각 표기한다 — 전체 문턱 하나가 아니라

우리가 그쪽보다 더 하는 것:
  - 병목을 만드는 **음이온 3개(창)** 를 이름과 반지름으로 명시 (그쪽은 s1/s2/s3 라벨만)
  - E_perc 와 **MD Eₐ 를 같은 그림에** — 프록시 한계를 그림이 스스로 말하게
  - E_1D/2D/3D 를 함께 표기 (차원별 문턱)
⚠ 그쪽 슬라이드의 σ(T) 표는 **모델 생성값**으로 판정됐다(kb/concepts/bvse.md §9).
  우리는 σ 표를 BV 로 만들지 않는다 — σ·Eₐ 는 MD 담당.

  python3 tools/figures/fig_bv_path_annotated.py --system modelc
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
import fig_bv_path_profile as bvp                                       # noqa: E402

ANION = ("S", "Cl", "O")
MD_EA = {"comp1": "0.253", "modelc": "0.197±0.032",
         "lpsocl": "0.287±0.024", "b2o3": "0.199±0.034"}


def mic_fn(cell):
    inv = np.linalg.inv(cell.T)

    def mic(v):
        f = inv @ v
        f -= np.round(f)
        return cell.T @ f
    return mic


def label_valley(r, atoms, mic):
    """골짜기 = Li 후보 자리. 가장 가까운 Li 와 음이온 배위로 정체를 쓴다."""
    dLi = sorted((float(np.linalg.norm(mic(p - r))), i)
                 for i, (s, p) in enumerate(atoms) if s == "Li")
    shell = sorted((float(np.linalg.norm(mic(p - r))), s)
                   for s, p in atoms if s in ANION)
    coord = {}
    for dist, s in shell:
        if dist <= 3.2:
            coord[s] = coord.get(s, 0) + 1
    cstr = "+".join(f"{n}{s}" for s, n in sorted(coord.items())) or "—"
    kind = "on Li" if dLi and dLi[0][0] < 0.6 else "vacant"
    return f"{kind}\n{cstr}", dLi[0][0] if dLi else np.nan


def label_saddle(r, atoms, mic):
    """봉우리 = 병목. 이온이 실제로 통과하는 **음이온 창**(가장 가까운 3개)."""
    near = sorted((float(np.linalg.norm(mic(p - r))), s)
                  for s, p in atoms if s in ANION)[:3]
    names = "".join(s for _, s in near)
    return f"{names}\nwindow {near[0][0]:.2f} Å", near[0][0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="modelc", choices=list(bvp.SYSTEMS))
    ap.add_argument("--out_png", default=None)
    ap.add_argument("--out_csv", default=None)
    ap.add_argument("--min_prom", type=float, default=0.02,
                    help="봉우리 프로미넌스 컷 (eV) — 잔물결 제외")
    a = ap.parse_args()

    cif, disp = bvp.SYSTEMS[a.system]
    r = bvp.profile_for(a.system, str(ROOT / cif))
    d, e, cart, atoms = r["d"], r["e"], r["cart"], r["atoms"]
    mic = mic_fn(r["cell"])

    # 봉우리/골짜기 (프로미넌스 컷) ─────────────────────────────────────
    pk = [i for i in range(1, len(e) - 1) if e[i] > e[i - 1] and e[i] >= e[i + 1]]
    pk = [i for i in pk if e[i] - min(e[:i].min(), e[i:].min()) >= a.min_prom]
    seg, prev = [], 0
    for i in pk:                              # 구간 = 직전 골짜기 → 이 봉우리
        j = int(np.argmin(e[prev:i + 1])) + prev
        seg.append((j, i, float(e[i] - e[j])))
        prev = i

    print(f"\n{disp} · {r['axis']} · {len(seg)} 구간 (프로미넌스 ≥ {a.min_prom} eV)")
    rows = []
    for k, (j, i, db) in enumerate(seg, 1):
        vl, dli = label_valley(cart[j], atoms, mic)
        sd, wr = label_saddle(cart[i], atoms, mic)
        print(f"  {k}: {d[j]:5.2f}→{d[i]:5.2f} Å  ΔE {db:.3f} eV  "
              f"| valley {vl.replace(chr(10), ' ')} (Li {dli:.2f} Å)"
              f" | saddle {sd.replace(chr(10), ' ')}")
        rows.append({"segment": k, "s_valley_A": f"{d[j]:.3f}", "s_saddle_A": f"{d[i]:.3f}",
                     "E_valley_eV": f"{e[j]:.4f}", "E_saddle_eV": f"{e[i]:.4f}",
                     "barrier_eV": f"{db:.4f}",
                     "valley_site": vl.replace("\n", " "), "nearest_Li_A": f"{dli:.2f}",
                     "saddle_window": sd.replace("\n", " "), "window_r_A": f"{wr:.3f}"})

    # ── 그림 ───────────────────────────────────────────────────────────
    col = SYS[a.system]
    fig, ax = plt.subplots(figsize=(11.4, 5.8))
    ax.axhspan(0, r["E_perc"], color="#f1f5f9", zorder=0)
    ax.plot(d, e, color=col, lw=2.0, zorder=3)
    ax.axhline(r["E_perc"], ls="--", lw=1.2, color=INK, zorder=2)
    ax.text(d[-1], r["E_perc"] + 0.004, f"$E_{{perc}}$ = {r['E_perc']:.3f} eV",
            ha="right", fontsize=10, color=INK, fontweight="bold")

    top = e.max() + 0.135
    for k, (j, i, db) in enumerate(seg, 1):
        ax.plot([d[i], d[i]], [e[j], e[i]], color=MUT, lw=0.9, ls=":", zorder=2)
        ax.annotate("", xy=(d[i], e[i]), xytext=(d[i], e[j]),
                    arrowprops=dict(arrowstyle="<->", color=MUT, lw=0.9))
        ax.text(d[i] + 0.12, (e[i] + e[j]) / 2, f"{db:.3f}", fontsize=8.5,
                color=INK, va="center", fontweight="bold")
        sd, _ = label_saddle(cart[i], atoms, mic)
        ax.text(d[i], top - 0.006 - 0.030 * (k % 2), sd, fontsize=7.5, color=MUT,
                ha="center", va="top", linespacing=1.15)
        ax.plot(d[i], e[i], "o", ms=5, mfc="white", mec=col, mew=1.4, zorder=4)
        vl, _ = label_valley(cart[j], atoms, mic)
        ax.text(d[j], e[j] - 0.018, vl, fontsize=7.5, color=MUT, ha="center",
                va="top", linespacing=1.15)

    ax.set_xlabel("Reaction coordinate (Å)", fontsize=11.5)
    ax.set_ylabel("Bond-valence energy (eV)", fontsize=11.5)
    ref = r["ref"]
    ax.set_title(f"BV percolation path, segment barriers — {disp}  axis {r['axis']}\n"
                 f"$E_{{1D}}$/$E_{{2D}}$/$E_{{3D}}$ = {ref['E_1D']:.3f} / {ref['E_2D']:.3f} / "
                 f"{ref['E_3D']:.3f} eV      MD $E_a$ = {MD_EA[a.system]} eV",
                 fontsize=12.5, color=INK, fontweight="bold")
    ax.set_xlim(-0.5, d[-1] + 0.9)
    ax.set_ylim(-0.062, top)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.text(0.5, -0.03,
             "Empty-lattice proxy: one Li probe in a frozen lattice. Segment barriers describe "
             "the landscape shape, not measured activation energies —\nthe Ea/σ ranking between "
             "compositions is determined by seed-ensemble MLIP-MD.",
             ha="center", fontsize=9, color=MUT)
    fig.tight_layout()
    out = a.out_png or f"docs/figures/bv_path_annotated_{a.system}.png"
    fig.savefig(ROOT / out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {out}")

    outc = a.out_csv or f"db/properties/bv_path_segments_{a.system}.csv"
    with open(ROOT / outc, "w", newline="", encoding="utf-8-sig") as f:
        f.write(f"# BV percolation path segment barriers - {disp}, axis {r['axis']}, "
                f"E_perc {r['E_perc']:.4f} eV.\n")
        f.write("# barrier_eV = E(saddle) - E(preceding valley) along the min-energy-line-integral "
                "path under the percolation ceiling.\n")
        f.write("# valley_site: 'on Li' if a framework Li sits within 0.6 A, else 'vacant' "
                "(empty-lattice map: valleys are CANDIDATE sites); coordination = anions within 3.2 A.\n")
        f.write("# saddle_window: the three nearest anions forming the bottleneck; window_r_A = "
                "distance to the closest of them.\n")
        f.write("# EMPTY-LATTICE PROXY - not a measured barrier. Ea/sigma ranking is decided by MD "
                f"(MD Ea = {MD_EA[a.system]} eV). See kb/concepts/bvse.md sec 8-10.\n")
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"→ {outc}")


if __name__ == "__main__":
    main()
