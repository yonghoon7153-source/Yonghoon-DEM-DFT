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
from elf_planes_lpsocl import (TITLE, draw_labeled, draw_montage,             # noqa: E402
                               get_cmap, load_planes_npz)


def crop(img, us, marks, half_new):
    """캐시된 창(half)보다 좁게 잘라낸다 — b2o3 라벨판(±3.2 Å)에 창까지 맞출 때.

    ⚠ 넓히는 건 불가능하다(없는 데이터다). 넓히려면 cube 에서 다시 샘플링해야 한다.
    """
    m = np.abs(us) <= half_new + 1e-9
    if m.sum() < 8:
        raise SystemExit(f"--half_crop {half_new} 가 너무 작다")
    img2 = img[np.ix_(m, m)]
    us2 = us[m]
    marks2 = [(s, u, v) for s, u, v in marks if abs(u) <= half_new and abs(v) <= half_new]
    return img2, us2, marks2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", required=True, help="elf_planes_lpsocl.py --save_npz 산출")
    ap.add_argument("--out", required=True, help="출력 디렉터리")
    ap.add_argument("--cmap", default="jet", help="jet(기본) · house · matplotlib 이름")
    ap.add_argument("--motifs", nargs="*", default=None, help="기본은 캐시에 있는 것 전부")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--no_clean", action="store_true", help="크롬 없는 판 생략")
    ap.add_argument("--half_crop", type=float, default=None,
                    help="창을 이 반폭(Å)으로 잘라낸다. b2o3 라벨판과 맞추려면 3.2")
    ap.add_argument("--contours", action="store_true",
                    help="라벨판에 0.30/0.70 판정선 (기본 꺼짐 = b2o3 라벨판과 동일)")
    a = ap.parse_args()

    imgs, half, label, tag, titles = load_planes_npz(a.npz)
    if a.motifs:
        imgs = {k: v for k, v in imgs.items() if k in a.motifs}
        if not imgs:
            raise SystemExit("--motifs 가 캐시에 없다")
    CM = get_cmap(a.cmap)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    H = a.half_crop if a.half_crop else half
    print(f"{len(imgs)} 개 평면 · half {half} → {H} Å · cmap {a.cmap} · {label}")
    if not titles:
        print("  (옛 캐시 — 제목이 안 들어있어 TITLE 표로 대체한다)")

    shown = {}
    for name, (img, us, marks) in imgs.items():
        if a.half_crop:
            img, us, marks = crop(img, us, marks, a.half_crop)
        shown[name] = (img, us, marks)

        if not a.no_clean:                       # 크롬 없는 논문판
            fig = plt.figure(figsize=(6, 6)); ax = fig.add_axes([0, 0, 1, 1])
            ax.axis("off")
            ax.imshow(img, origin="lower", extent=[-H, H, -H, H],
                      cmap=CM, vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
            fig.savefig(out / f"elf_plane_{tag}_{name}.png", dpi=a.dpi); plt.close(fig)

        title = titles.get(name) or f"{label} — {TITLE.get(name, name)}"
        draw_labeled(img, us, marks, H, title, CM,
                     out / f"{tag}_elf_plane_{name}.png", contours=a.contours)
        print(f"  {name}")

    draw_montage(shown, H, CM, label, out / f"{tag}_elf_planes.png")
    print(f"→ {out}/  (몽타주 {tag}_elf_planes.png 포함)")


if __name__ == "__main__":
    main()
