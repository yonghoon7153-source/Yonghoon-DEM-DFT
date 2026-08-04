#!/usr/bin/env python3
"""restyle_elf_planes.py — ELF 평면 그림을 **cube 없이** 다시 렌더한다.

왜 있나 (2026-08-04)
  색 하나 바꾸려고 수십 MB cube 를 다시 읽고 서버를 왕복하던 걸 끊는다.
  elf_planes_lpsocl.py --save_npz 가 남긴 평면 캐시(npz)만 있으면
  컬러맵·라벨·몽타주 양식을 어디서든(로컬 포함) 다시 만들 수 있다.

  # 서버에서 한 번 (cube 있는 곳)
  python3 tools/figures/elf_planes_lpsocl.py --cube ... --out ... --save_npz
  # 그 뒤로는 어디서든
  python3 tools/figures/restyle_elf_planes.py --npz lpsocl_elf_planes.npz \\
      --out planes_jet --cmap jet

⚠ 이건 **표시 전용**이다. 정량(결합 위 central_min)은 CSV 가 정본이고 npz 는
  float16 캐시라 정량 인용에 쓰지 않는다.
⚠ 컬러맵 기본은 jet — 논문/슬라이드에 이미 나간 b2o3·LPSCl16 family 와 통일.
  (jet 은 지각 균일하지 않다. 값 판독은 0.30/0.70 등고선과 CSV 로 한다.)
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elf_planes_lpsocl import (TITLE, TITLE_COLOR, draw_marks, draw_montage,   # noqa: E402
                               get_cmap, load_planes_npz)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", required=True, help="elf_planes_lpsocl.py --save_npz 산출")
    ap.add_argument("--out", required=True, help="출력 디렉터리")
    ap.add_argument("--cmap", default="jet", help="jet(기본) · house · matplotlib 이름")
    ap.add_argument("--motifs", nargs="*", default=None, help="기본은 캐시에 있는 것 전부")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--no_clean", action="store_true", help="크롬 없는 판 생략")
    a = ap.parse_args()

    imgs, half, label, tag = load_planes_npz(a.npz)
    if a.motifs:
        imgs = {k: v for k, v in imgs.items() if k in a.motifs}
        if not imgs:
            raise SystemExit(f"--motifs 가 캐시에 없다. 있는 것: {list(imgs)}")
    CM = get_cmap(a.cmap)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    print(f"{len(imgs)} 개 평면 · half {half} Å · cmap {a.cmap} · {label}")

    for name, (img, us, marks) in imgs.items():
        if not a.no_clean:                       # 크롬 없는 논문판
            fig = plt.figure(figsize=(6, 6)); ax = fig.add_axes([0, 0, 1, 1])
            ax.axis("off")
            ax.imshow(img, origin="lower", extent=[-half, half, -half, half],
                      cmap=CM, vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
            fig.savefig(out / f"elf_plane_{tag}_{name}.png", dpi=a.dpi); plt.close(fig)

        fig, ax = plt.subplots(figsize=(7.4, 6.6))     # 라벨판
        im = ax.imshow(img, origin="lower", extent=[-half, half, -half, half],
                       cmap=CM, vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
        cb = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02); cb.set_label("ELF", fontsize=12)
        ax.contour(us, us, img, levels=[0.30, 0.70], colors=["white", "black"],
                   linewidths=[1.0, 1.2], linestyles=["--", "-"])
        draw_marks(ax, marks)
        ax.set_xlabel("in-plane x (Å)"); ax.set_ylabel("in-plane y (Å)")
        ax.set_title(f"{TITLE.get(name, name)} — {label}", fontsize=11.5,
                     color=TITLE_COLOR.get(name, "#1f2937"))
        ax.text(0.99, 0.015, "solid 0.70 (covalent) · dashed 0.30 (ionic)",
                transform=ax.transAxes, ha="right", fontsize=8, color="white")
        fig.tight_layout()
        fig.savefig(out / f"{tag}_elf_plane_{name}.png", dpi=220, facecolor="white",
                    bbox_inches="tight"); plt.close(fig)
        print(f"  {name}")

    draw_montage(imgs, half, CM, label, out / f"{tag}_elf_planes.png")
    print(f"→ {out}/  (몽타주 {tag}_elf_planes.png 포함)")


if __name__ == "__main__":
    main()
