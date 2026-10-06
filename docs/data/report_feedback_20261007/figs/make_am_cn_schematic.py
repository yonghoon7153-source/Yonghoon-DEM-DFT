#!/usr/bin/env python3
"""2-1 장 ③ 칸 도식 — '활물질 배위수' (활물질 하나에 닿은 SE 수 · AM–AM 접촉 · 떨어진 SE 는 세지 않는다).
옛 'SE 배위수' 도식과 같은 꼴: 음영 구 · 번호 · 가운데 테두리 · 떨어진 입자 ×.  산출: PNG (투명 · 600 dpi) + SVG.
  python3 make_am_cn_schematic.py <out_dir>
"""
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT.mkdir(parents=True, exist_ok=True)
LIGHT = np.array([-0.45, 0.55, 0.70]); LIGHT /= np.linalg.norm(LIGHT)
SE_RGB, SE_DET_RGB = (0.76, 0.71, 0.50), (0.96, 0.93, 0.86)   # 옛 도식 질감 (무광 올리브-황토 · 연한 크림)
PC_RGB, SC_RGB, AM2_RGB = (0.16, 0.16, 0.17), (0.56, 0.56, 0.57), (0.62, 0.62, 0.63)
NAVY, RING, RED = '#1F3A68', '#2F4F8F', '#D33A2C'
plt.rcParams.update({'font.family': 'Liberation Sans', 'svg.hashsalt': 'amcn'})


def sphere(ax, cx, cy, r, rgb, z=2, n=400):
    """Lambert + 반사광으로 음영을 넣은 구 하나 (가장자리 안티에일리어싱)."""
    t = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(t, -t)
    R2 = X * X + Y * Y
    Z = np.sqrt(np.clip(1 - R2, 0, 1))
    N = np.stack([X, Y, Z], -1)
    diff = np.clip(N @ LIGHT, 0, 1)
    H = LIGHT + np.array([0, 0, 1.0]); H /= np.linalg.norm(H)
    spec = np.clip(N @ H, 0, 1) ** 8                         # 옛 도식처럼 무광 — 은은한 윤기만
    base = np.array(rgb)
    col = base * (0.66 + 0.48 * diff[..., None]) + 0.06 * spec[..., None]
    edge = np.clip((1 - np.sqrt(R2)) * n / 3, 0, 1)
    img = np.dstack([np.clip(col, 0, 1), edge])
    ax.imshow(img, extent=[cx - r, cx + r, cy - r, cy + r], zorder=z, interpolation='bilinear')
    ax.add_patch(Circle((cx, cy), r * 0.995, fill=False, lw=1.1, ec=tuple(np.array(rgb) * 0.62), zorder=z + 0.1))   # 가는 테두리 (옛 도식)


def draw(ax, am_r, am_rgb, am_label, angles, se_r=0.32, overlap=0.03, neighbor=None, detached=None, label_color='white', label_size=13):
    ext = [(0, 0, am_r)]
    sphere(ax, 0, 0, am_r, am_rgb, z=3)
    ax.add_patch(Circle((0, 0), am_r * 1.01, fill=False, lw=2.6, ec=RING, zorder=6))
    ax.text(0, 0, am_label, ha='center', va='center', fontsize=label_size, fontweight='bold', color=label_color, zorder=7)   # Coverage 칸 그림과 같은 글자 (굵은 · 같은 크기)
    d = am_r + se_r - overlap
    for i, a in enumerate(angles, 1):
        x, y = d * math.cos(math.radians(a)), d * math.sin(math.radians(a))
        sphere(ax, x, y, se_r, SE_RGB, z=4); ext.append((x, y, se_r))
        ax.text(x, y, str(i), ha='center', va='center', fontsize=15, fontweight='bold', color=NAVY, zorder=7)
    if neighbor:                                    # 다른 활물질 (AM–AM 접촉 — 세지 않음)
        a, r2 = neighbor
        dd = am_r + r2 - overlap
        nx, ny = dd * math.cos(math.radians(a)), dd * math.sin(math.radians(a))
        sphere(ax, nx, ny, r2, AM2_RGB, z=2); ext.append((nx, ny, r2))
        ax.text(nx, ny, 'AM', ha='center', va='center', fontsize=label_size, fontweight='bold', color='#333333', zorder=7)   # 붙어 있는 활물질도 AM
    if detached:                                    # 떨어진 SE (닿지 않음 — 세지 않음)
        a, gap = detached
        dd = am_r + se_r + gap
        x, y = dd * math.cos(math.radians(a)), dd * math.sin(math.radians(a))
        sphere(ax, x, y, se_r * 0.9, SE_DET_RGB, z=4); ext.append((x, y, se_r * 0.9))
        ax.text(x, y, '×', ha='center', va='center', fontsize=16, fontweight='bold', color=RED, zorder=7)
    xs0 = min(x - r for x, y, r in ext); xs1 = max(x + r for x, y, r in ext)
    ys0 = min(y - r for x, y, r in ext); ys1 = max(y + r for x, y, r in ext)
    m = 0.08
    ax.set_xlim(xs0 - m, xs1 + m); ax.set_ylim(ys0 - m, ys1 + m); ax.set_aspect('equal'); ax.axis('off')
    return len(angles)


def finish(fig, ax, name):
    fig.savefig(OUT / f'{name}.png', dpi=600, transparent=True, bbox_inches='tight', pad_inches=0.02)
    fig.savefig(OUT / f'{name}.svg', transparent=True, bbox_inches='tight', pad_inches=0.02, metadata={'Date': None})
    plt.close(fig)


# ① 단일 판 (PC · 검정 활물질) — 옛 'SE 배위수' 칸을 그대로 바꿔 넣는 그림
fig, ax = plt.subplots(figsize=(3.0, 3.0))
n_pc = draw(ax, 1.0, PC_RGB, 'AM', angles=[0, 45, 90, 135, 180, 225], neighbor=(-60, 0.60), detached=(67.5, 0.45))
finish(fig, ax, 'am_cn_schematic_PC')

# ② PC · SC 나란히 — 큰 다결정 (PC) 은 SE 가 많이, 작은 단결정 (SC) 은 적게
fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.9), gridspec_kw={'wspace': 0.02})
draw(axs[0], 1.0, PC_RGB, 'AM', angles=[0, 40, 80, 120, 160, 200, 240], neighbor=(-60, 0.60), detached=(100, 0.45))
draw(axs[1], 0.55, SC_RGB, 'AM', angles=[20, 110, 200, 290], detached=(65, 0.45), label_color='#333333')   # 회색 구 = 진회색 글자 (Coverage 칸과 같음)
#  두 판 같은 축척 — 각 판 bbox 중심 ± 공통 반폭 (SE 크기가 두 판에서 같게)
S = max(max(a.get_xlim()[1] - a.get_xlim()[0], a.get_ylim()[1] - a.get_ylim()[0]) for a in axs)
for a in axs:
    cx, cy = sum(a.get_xlim()) / 2, sum(a.get_ylim()) / 2
    a.set_xlim(cx - S / 2, cx + S / 2); a.set_ylim(cy - S / 2, cy + S / 2)
fig.savefig(OUT / 'am_cn_schematic_PC_SC.png', dpi=600, transparent=True, bbox_inches='tight', pad_inches=0.02)
fig.savefig(OUT / 'am_cn_schematic_PC_SC.svg', transparent=True, bbox_inches='tight', pad_inches=0.02, metadata={'Date': None})
plt.close(fig)
print('PC 단일 판 배위수 =', n_pc, '· PC/SC 판 = 7 · 4')
