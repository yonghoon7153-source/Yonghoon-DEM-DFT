#!/usr/bin/env python3
"""fig_sei_neb_paths.py — SEI/음극상 CI-NEB 경로 그림 (색 · 무채색 두 판) + Origin CSV.

입력은 gabia 에서 회수한 QE neb.x 원본이다 (runs/sei_neb_paths_2026_09_01/):
  <case>.dat  = 7 NEB 이미지  (반응좌표, E−E_first [eV], 힘/오차)
  <case>.int  = 251점 보간 MEP (반응좌표, E−E_first [eV])
hBN 판(fig_vgcf_hbn_neb.py)과 같은 구성이라 두 그림을 나란히 놓을 수 있다.

산출:
  docs/figures/sei_neb_paths.png            색 판
  docs/figures/sei_neb_paths_mono.png       무채색 판 (흑백 인쇄·저널 대비)
  db/properties/sei_neb_mep_origin.csv      보간 MEP (곡선용)
  db/properties/sei_neb_images_origin.csv   7 이미지 점
  db/properties/sei_neb_barriers_origin.csv 장벽 막대

⛔ 이 도구가 **못 하는 것**
  · 값의 인용 자격을 만들지 않는다. 세 경로 전부 `citable: false` 다
    (`db/properties/sei_neb.json` — 셀 수렴 미시험). 그림에 그 사실을 각주로 박는다.
  · li3nd c→b 는 **이동 장벽이 아니다** — 끝점이 시작점보다 2.07 eV 높은 진단용 홉이라
    막대 패널에서 제외하고 곡선에만 남긴다. 전도 장벽으로 읽으면 틀린다.
  · 셀 크기 효과를 보정하지 않는다. 서로 다른 셀의 값을 같은 축에 놓지 않는다.
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from house_style import INK, MUT, ELEM, apply_axes            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "runs", "sei_neb_paths_2026_09_01")
FIGD = os.path.join(ROOT, "docs", "figures")
PROP = os.path.join(ROOT, "db", "properties")

#: (디렉토리, 파일 접두어, 표시명, 셀, λ₁ Å, 색, 막대에 넣나)
#:   ⚠ li3nd c→b 는 bars=False — 끝점이 2.07 eV 높은 진단용 홉이다.
#:   ⚠ 표시명은 **영어만** 쓴다 — 하우스 규칙(뷰어 한글 폰트 깨짐, 2026-09-01 실측).
CASES = [
    ("li2s",      "li2s",  "Li2S  c->c",        "3×3×3", 12.10, ELEM.get("S", "#c05621"), True),
    ("li3nd_ccc", "li3nd", "Li3Nd  c->c",       "2×2×2", 10.37, ELEM.get("Li", "#0d9488"), True),
    ("li3nd_ccb", "li3nd", "Li3Nd  c->b (diagnostic)", "2×2×2", 10.37, MUT, False),
]


def _read(path, ncol):
    """공백 구분 수치표. → (N, ncol) 배열. 빈 줄·주석은 버린다."""
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith(("#", "!")):
                continue
            p = ln.split()
            if len(p) < ncol:
                continue
            try:
                rows.append([float(x) for x in p[:ncol]])
            except ValueError:
                continue
    if not rows:
        raise SystemExit(f"⛔ {path} 에서 수치를 못 읽었다")
    return np.array(rows)


def load():
    out = []
    for d, pre, label, cell, lam, col, bars in CASES:
        base = os.path.join(RAW, d)
        img = _read(os.path.join(base, f"{pre}.dat"), 3)
        mep = _read(os.path.join(base, f"{pre}.int"), 2)
        # ⛔ 장벽은 **이미지**에서 낸다. `.int` 는 스플라인이라 안장점이 이미지 사이에
        #   있으면 **오버슛한다** — li3nd c→c 에서 실측 +3.3 meV (2026-09-01 selftest
        #   가 db 값 0.228981 과의 불일치로 잡았다). CI-NEB 이 보고하는 값은 이미지
        #   최댓값이고, 곡선은 그리기용이다. 둘을 섞으면 그림과 표가 어긋난다.
        ef = float(img[:, 1].max())                    # forward: 이미지 최대 − 시작
        dE = float(img[-1, 1])
        eb = ef - dE                                   # backward: 최대 − 끝점
        over = float(mep[:, 1].max() - ef)             # 스플라인 오버슛 (진단)
        out.append(dict(dir=d, label=label, cell=cell, lam=lam, color=col,
                        bars=bars, img=img, mep=mep, ef=ef, eb=eb, dE=dE,
                        spline_overshoot=over))
    return out


def draw(data, mono=False):
    fig, (ax, bx) = plt.subplots(
        1, 2, figsize=(11.2, 4.3), gridspec_kw=dict(width_ratios=[2.15, 1]))

    for i, c in enumerate(data):
        col = INK if mono else c["color"]
        ls = ["-", "--", ":"][i % 3] if mono else "-"
        ax.plot(c["mep"][:, 0], c["mep"][:, 1], color=col, lw=2.0, ls=ls, zorder=3,
                label=f'{c["label"]}   ({c["cell"]} · λ₁ {c["lam"]:.1f} Å)')
        ax.plot(c["img"][:, 0], c["img"][:, 1], "o", ms=4.6, color=col,
                mfc="white" if mono else col, mew=1.4, zorder=4)

    ax.axhline(0.0, color=MUT, lw=0.8, ls=(0, (2, 3)), alpha=0.6, zorder=1)
    apply_axes(ax, xlabel="Reaction coordinate (normalized)",
               ylabel="Energy relative to initial state (eV)")
    ax.legend(frameon=False, fontsize=9.4, loc="upper left", labelcolor=INK)
    ax.set_xlim(-0.02, 1.02)

    # ── 막대: 정방향/역방향 (진단 홉은 뺀다) ──────────────────────────────
    bar = [c for c in data if c["bars"]]
    xb = np.arange(len(bar), dtype=float)
    W = 0.34
    for i, c in enumerate(bar):
        col = INK if mono else c["color"]
        bx.bar(xb[i] - W / 2, c["ef"], W, color=col, alpha=0.92, zorder=3)
        bx.bar(xb[i] + W / 2, c["eb"], W, color=col, alpha=0.34,
               edgecolor=col, lw=1.3, zorder=3)
        bx.text(xb[i] - W / 2, c["ef"] + 0.012, f'{c["ef"]:.3f}', ha="center",
                va="bottom", fontsize=9.6, fontweight="bold", color=col)
        bx.text(xb[i] + W / 2, c["eb"] + 0.012, f'{c["eb"]:.3f}', ha="center",
                va="bottom", fontsize=9.6, color=col, alpha=0.85)
    bx.set_xticks(xb)
    bx.set_xticklabels([c["label"].split("  ")[0] for c in bar], fontsize=10)
    apply_axes(bx, ylabel="Barrier (eV)")
    bx.set_ylim(0, max(c["ef"] for c in bar) * 1.28)
    bx.text(0.98, 0.96, "forward / backward", transform=bx.transAxes,
            ha="right", va="top", fontsize=8.8, color=MUT)

    fig.text(0.008, 0.038,
             "CI-NEB, 7 images - charged vacancy (V$_{Li}^{-}$ + jellium), same-cell protocol.  "
             "Barriers are read from the images, not the spline.",
             fontsize=7.6, color=MUT, ha="left", va="bottom")
    fig.text(0.008, 0.008,
             "Absolute barriers are NOT cell-converged (second cell untested) - within-protocol "
             "comparison only.  Li3Nd c->b is a diagnostic hop (final state 2.07 eV above "
             "initial), excluded from the bar panel.",
             fontsize=7.6, color=MUT, ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.085, 1, 1))
    os.makedirs(FIGD, exist_ok=True)
    out = os.path.join(FIGD, "sei_neb_paths_mono.png" if mono else "sei_neb_paths.png")
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def write_csv(data):
    os.makedirs(PROP, exist_ok=True)
    p1 = os.path.join(PROP, "sei_neb_mep_origin.csv")
    with open(p1, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# Interpolated MEP from QE neb.x <case>.int (251 pts). "
                "E relative to initial image [eV].\n")
        f.write("# NOT cell-converged — see db/properties/sei_neb.json "
                "(citable=false, cell_convergence_status=untested).\n")
        w = csv.writer(f)
        w.writerow(["reaction_coord"] + [f"E_eV__{c['dir']}" for c in data])
        n = min(len(c["mep"]) for c in data)
        for i in range(n):
            w.writerow([f"{data[0]['mep'][i,0]:.6f}"]
                       + [f"{c['mep'][i,1]:.6f}" for c in data])

    p2 = os.path.join(PROP, "sei_neb_images_origin.csv")
    with open(p2, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# 7 NEB images from <case>.dat: coord, E-E_first [eV], force/err.\n")
        w = csv.writer(f)
        w.writerow(["case", "image", "reaction_coord", "E_eV", "force_err"])
        for c in data:
            for j, r in enumerate(c["img"]):
                w.writerow([c["dir"], j + 1, f"{r[0]:.6f}", f"{r[1]:.6f}", f"{r[2]:.6f}"])

    p3 = os.path.join(PROP, "sei_neb_barriers_origin.csv")
    with open(p3, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# Forward/backward barriers **from the 7 NEB images** "
                "(not from the spline).\n"
                "# spline_overshoot_eV = max(.int) - max(.dat): the plotted curve can "
                "overshoot when the saddle falls between images.\n"
                "# citable=false for ALL rows (cell convergence untested).\n")
        w = csv.writer(f)
        w.writerow(["case", "label", "supercell", "lambda1_A",
                    "Ea_forward_eV", "Ea_backward_eV", "dE_endpoint_eV",
                    "spline_overshoot_eV", "in_bar_panel", "citable"])
        for c in data:
            w.writerow([c["dir"], c["label"], c["cell"], f"{c['lam']:.2f}",
                        f"{c['ef']:.6f}", f"{c['eb']:.6f}", f"{c['dE']:.6f}",
                        f"{c['spline_overshoot']:.6f}",
                        "yes" if c["bars"] else "no (diagnostic hop)", "no"])
    return p1, p2, p3


def selftest():
    """⛔음성 포함 — 파일이 아니라 **계약**을 시험한다."""
    ok = [0, 0]

    def chk(c, m):
        print(("  ✔ " if c else "  ⛔ ") + m)
        ok[0 if c else 1] += 1

    d = load()
    chk(len(d) == 3, "세 경로를 읽는다")
    chk(all(len(c["img"]) == 7 for c in d), "각 경로가 7 이미지다")
    chk(all(len(c["mep"]) == 251 for c in d), "보간 MEP 가 251점이다")

    li2s = next(c for c in d if c["dir"] == "li2s")
    chk(abs(li2s["ef"] - 0.305025) < 5e-4,
        "li2s 정방향 장벽이 db 값 0.305025 와 일치 (%.6f)" % li2s["ef"])
    chk(abs(li2s["dE"]) < 1e-3,
        "⛔음성 li2s 끝점이 시작점과 같다 — 대칭 등가 홉이어야 한다 (%.2e)" % li2s["dE"])

    ccb = next(c for c in d if c["dir"] == "li3nd_ccb")
    chk(ccb["dE"] > 1.5,
        "⛔음성 li3nd c→b 는 끝점이 %.2f eV 높다 — 대칭 홉이 아니다" % ccb["dE"])
    chk(not ccb["bars"],
        "⛔음성 그 진단 홉은 막대 패널에서 **제외**된다 (전도 장벽으로 읽히면 안 된다)")
    chk(abs(ccb["eb"] - (ccb["ef"] - ccb["dE"])) < 1e-6,
        "역방향 = 최대 − 끝점 (정의 일관)")

    ccc = next(c for c in d if c["dir"] == "li3nd_ccc")
    chk(abs(ccc["ef"] - 0.228981) < 5e-4,
        "li3nd c→c 가 db 값 0.228981 과 일치 (%.6f)" % ccc["ef"])
    chk(ccc["mep"][:, 1].argmax() != len(ccc["mep"]) // 2,
        "⛔음성 li3nd c→c 는 중점이 최댓값이 아니다 — 중간 극소가 있는 이중 봉우리다")
    chk(ccc["spline_overshoot"] > 0.002,
        "⛔음성 그 경로에서 **스플라인이 이미지보다 %.1f meV 높게 튄다** — 장벽을 "
        "`.int` 에서 읽으면 db 와 어긋난다 (그래서 이미지에서 읽는다)"
        % (ccc["spline_overshoot"] * 1000))
    chk(li2s["spline_overshoot"] < 0.001,
        "[양성] 안장점에 이미지가 놓인 li2s 는 오버슛이 없다 (%.1e eV)"
        % li2s["spline_overshoot"])

    chk(all(c["lam"] >= 10.0 for c in d),
        "표시한 셀이 전부 λ₁ ≥ 10 Å 게이트를 통과한다")
    print("selftest: %d 통과 / %d 실패" % (ok[0], ok[1]))
    return 0 if ok[1] == 0 else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    d = load()
    a = draw(d, mono=False)
    b = draw(d, mono=True)
    cs = write_csv(d)
    for p in (a, b) + cs:
        print("→", os.path.relpath(p, ROOT))
    print("\n⚠ 세 값 전부 citable=false — 셀 수렴 미시험. 그림 각주에 박혀 있다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
