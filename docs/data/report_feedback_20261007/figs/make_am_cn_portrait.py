#!/usr/bin/env python3
"""덱 칸 (그림 상자 981710 × 1276350 EMU = 세로 비 0.7692) 에 맞춘 '활물질 배위수' 세로 판 — SE 5 개 (아래 설명 '배위수 = 5 (AM·떨어진 SE 제외)' 그대로 맞음).
질감 = make_am_cn_schematic.py 와 같은 무광 음영 · 가는 테두리.  python3 make_am_cn_portrait.py <out.png>"""
import math, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
LIGHT = np.array([-0.45, 0.55, 0.70]); LIGHT /= np.linalg.norm(LIGHT)
SE_RGB, SE_DET_RGB, PC_RGB, AM2_RGB = (0.76, 0.71, 0.50), (0.96, 0.93, 0.86), (0.16, 0.16, 0.17), (0.62, 0.62, 0.63)
NAVY, RING, RED = '#1F3A68', '#2F4F8F', '#D33A2C'
plt.rcParams.update({'font.family': 'Liberation Sans'})
ASPECT = 981710 / 1276350

def sphere(ax, cx, cy, r, rgb, z=2, n=400):
    t = np.linspace(-1, 1, n); X, Y = np.meshgrid(t, -t); R2 = X * X + Y * Y
    Z = np.sqrt(np.clip(1 - R2, 0, 1)); N = np.stack([X, Y, Z], -1)
    diff = np.clip(N @ LIGHT, 0, 1); H = LIGHT + np.array([0, 0, 1.0]); H /= np.linalg.norm(H)
    spec = np.clip(N @ H, 0, 1) ** 8
    col = np.array(rgb) * (0.66 + 0.48 * diff[..., None]) + 0.06 * spec[..., None]
    edge = np.clip((1 - np.sqrt(R2)) * n / 3, 0, 1)
    ax.imshow(np.dstack([np.clip(col, 0, 1), edge]), extent=[cx - r, cx + r, cy - r, cy + r], zorder=z, interpolation='bilinear')
    ax.add_patch(Circle((cx, cy), r * 0.995, fill=False, lw=1.1, ec=tuple(np.array(rgb) * 0.62), zorder=z + 0.1))
    return (cx, cy, r)

fig, ax = plt.subplots(figsize=(3.0 * ASPECT, 3.0))
ext = [sphere(ax, 0, 0, 1.0, PC_RGB, z=3)]
ax.add_patch(Circle((0, 0), 1.01, fill=False, lw=2.6, ec=RING, zorder=6))
ax.text(0, 0, 'AM', ha='center', va='center', fontsize=13, fontweight='bold', color='white', zorder=7)
se_r, d = 0.32, 1.0 + 0.32 - 0.03
for i, a in enumerate([10, 55, 100, 145, 190], 1):          # 1 = 오른쪽 · 시계 반대 방향
    x, y = d * math.cos(math.radians(a)), d * math.sin(math.radians(a))
    ext.append(sphere(ax, x, y, se_r, SE_RGB, z=4))
    ax.text(x, y, str(i), ha='center', va='center', fontsize=13, fontweight='bold', color=NAVY, zorder=7)
dd = 1.0 + 0.85 - 0.03                                       # 다른 활물질 (AM끼리 접촉 — 세지 않음)
ext.append(sphere(ax, dd * math.cos(math.radians(-95)), dd * math.sin(math.radians(-95)), 0.85, AM2_RGB, z=2))
ax.text(dd * math.cos(math.radians(-95)), dd * math.sin(math.radians(-95)), 'AM', ha='center', va='center', fontsize=13, fontweight='bold', color='#333333', zorder=7)
dx = 1.0 + se_r + 0.45                                       # 떨어진 SE (세지 않음)
x, y = dx * math.cos(math.radians(32)), dx * math.sin(math.radians(32))
ext.append(sphere(ax, x, y, se_r * 0.9, SE_DET_RGB, z=4))
ax.text(x, y, '×', ha='center', va='center', fontsize=14, fontweight='bold', color=RED, zorder=7)
x0 = min(a - r for a, b, r in ext); x1 = max(a + r for a, b, r in ext)
y0 = min(b - r for a, b, r in ext); y1 = max(b + r for a, b, r in ext)
m = 0.06; W, Hh = (x1 - x0) + 2 * m, (y1 - y0) + 2 * m
if W / Hh < ASPECT: W = Hh * ASPECT
else: Hh = W / ASPECT
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
ax.set_xlim(cx - W / 2, cx + W / 2); ax.set_ylim(cy - Hh / 2, cy + Hh / 2); ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(0, 0, 1, 1)
fig.savefig(sys.argv[1], dpi=600, transparent=True)
print('saved', sys.argv[1])
