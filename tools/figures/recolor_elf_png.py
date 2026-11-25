#!/usr/bin/env python3
"""recolor_elf_png.py — 이미 렌더된 **crom 없는(clean)** 스칼라장 PNG 의 컬러맵만 바꾼다.

왜 있나 (2026-08-04)
  cube 가 서버에만 있는데 색만 바꾸고 싶을 때가 있다. clean PNG 는 값→색의
  **순수 매핑**이라, 컬러맵 LUT 로 최근접 역변환하면 값을 되찾을 수 있다.
  (npz 캐시가 있으면 restyle_elf_planes.py 를 써라 — 이건 캐시조차 없을 때의 길이다.)

  python3 tools/figures/recolor_elf_png.py --png elf_plane_lpsocl_PS4.png \\
      --from house --to jet --out elf_plane_lpsocl_PS4_jet.png

⚠ **표시 전용이다.** 역변환 값은 8비트 양자화 + 안티에일리어싱을 거친 근사라
  정량(central_min 등)에 쓰면 안 된다 — 정량은 언제나 cube/CSV 가 정본.
⚠ clean 판에만 쓴다. 축·컬러바·글자가 있는 그림은 그 픽셀도 같이 역변환돼 망가진다.
⚠ 원본과 목표 컬러맵을 **정확히** 알아야 한다. 모르면 --from 을 바꿔가며
  --report 로 잔차를 보고 가장 작은 것을 고른다 (맞으면 보통 < 0.01).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elf_planes_lpsocl import get_cmap                                  # noqa: E402

LUT_N = 1024


def lut(cmap):
    return cmap(np.linspace(0, 1, LUT_N))[:, :3]


def invert(rgb, cmap):
    """RGB(…,3 in [0,1]) → 값 [0,1] + 잔차. LUT 최근접 (색공간 유클리드)."""
    L = lut(cmap)
    flat = rgb.reshape(-1, 3)
    # 청크로 나눠 메모리 폭주 방지 (1800² × 1024 는 통째로 못 잡는다)
    idx = np.empty(len(flat), dtype=np.int32)
    res = np.empty(len(flat), dtype=np.float32)
    step = 200_000
    for i in range(0, len(flat), step):
        d = ((flat[i:i + step, None, :] - L[None, :, :]) ** 2).sum(-1)
        j = d.argmin(1)
        idx[i:i + step] = j
        res[i:i + step] = np.sqrt(d[np.arange(len(j)), j])
    return (idx / (LUT_N - 1)).reshape(rgb.shape[:2]), res.reshape(rgb.shape[:2])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", required=True, help="clean(크롬 없는) 스칼라장 PNG")
    ap.add_argument("--out", required=True)
    ap.add_argument("--from", dest="src", default="house", help="원본 컬러맵 (house/jet/…)")
    ap.add_argument("--to", dest="dst", default="jet", help="바꿀 컬러맵")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--report", action="store_true", help="역변환 잔차만 보고 끝낸다")
    a = ap.parse_args()

    im = np.asarray(Image.open(a.png).convert("RGB")).astype(np.float32) / 255.0
    val, res = invert(im, get_cmap(a.src))
    print(f"{Path(a.png).name}  {im.shape[1]}×{im.shape[0]}px")
    print(f"  역변환 잔차 (--from {a.src}): 평균 {res.mean():.4f} · 95% {np.percentile(res, 95):.4f} "
          f"· 최대 {res.max():.4f}")
    if res.mean() > 0.05:
        print("  ⚠ 잔차가 크다 — --from 컬러맵이 틀렸을 수 있다 (다른 이름으로 --report 비교)")
    print(f"  복원 값 범위 {val.min():.3f} – {val.max():.3f} · 평균 {val.mean():.3f}")
    if a.report:
        return

    h, w = im.shape[:2]                      # 비정사각 입력도 왜곡 없이 (리뷰 nit)
    fig = plt.figure(figsize=(w / a.dpi, h / a.dpi))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.imshow(val, cmap=get_cmap(a.dst), vmin=0, vmax=1, interpolation="nearest")
    fig.savefig(a.out, dpi=a.dpi); plt.close(fig)
    print(f"→ {a.out}  ({a.src} → {a.dst})")


if __name__ == "__main__":
    main()
