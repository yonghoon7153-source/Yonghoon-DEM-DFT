#!/usr/bin/env python3
"""50kg 4차년도 보고 — DEM 지배방정식 패널의 가운데 힘 그림, 단일 입도 (monomodal) 판 (10-30).

1저자 10-30: 2-1 장 (세라믹 catholyte 과제 2차년도) 의 지배방정식 패널을 50kg 덱에 넣되, 가운데 그림을
"monomodal 이니까 SE 랑 AM 의 크기 비율을 맞추고 (D 2 SE, D6 AM)" 로 바꾼다.

좌표 = i (AM) 반지름 R = 1 인 단위.  AM D 6 µm : SE D 2 µm → SE 반지름 1/3.
variant A = j 도 AM (D 6 µm, i 와 같은 크기 · 권고) · variant B = j 가 SE (D 2 µm).
배치 (판 · 가압 화살 · 점선 원 · 글자 자리) = 2-1 장 원 그림에서 잰 값 (원 그림의 i 반지름 0.571 in = 캡처 1300 px 를 쪽 폭으로 어림한 배율).
색 = 50kg 계획 덱 그림 (CAM 검정 · SE 노랑).  글꼴 = Carlito Bold Italic (Calibri 같은 폭).

    python3 -P make_fig_dem_eq_monomodal.py --out dem_eq_monomodal --export             # 단독 그림 A · B (글자 포함 · 없음 · PNG 300 dpi 투명 · SVG 윤곽선)
    python3 -P make_fig_dem_eq_monomodal.py --out <폴더> --export --preview <2-1 장 패널 2배 crop>   # 원 패널 위 비교 그림 (그 캡처는 리포 밖)
"""
import argparse, json, math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
from matplotlib import rcParams, font_manager

for _f in Path('/usr/share/fonts/truetype/crosextra').glob('Carlito-*.ttf'):
    font_manager.fontManager.addfont(str(_f))
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.it'] = 'Carlito:italic:bold'
rcParams['mathtext.rm'] = 'Carlito:bold'
rcParams['mathtext.bf'] = 'Carlito:bold'
rcParams['font.family'] = 'Carlito'
rcParams['svg.fonttype'] = 'path'           # SVG 글자 = 윤곽선 (Carlito 없는 PC 에서도 같은 모양)

R_AM, R_SE = 1.0, 1.0 / 3.0                       # D 6 : 2 µm
C = dict(am=(0.065, 0.065, 0.075), se=(0.80, 0.69, 0.29),        # 50kg 덱 CAM 검정 · SE 노랑 (#CDB650 계열)
         plate='#5B80B5', red='#8B1A1A', orange_arc='#C9622A', orange='#E07B39',
         green='#2E8B57', green_txt='#86E0A8', teal='#16A085', teal_txt='#43CDBB', navy='#34495E')

# 원 그림에서 잰 자리 (i 중심 = 0, R = 1)
PLATE = [(-2.96, 0.98), (-1.07, 1.52), (2.39, 1.31), (2.21, 0.50)]
RED_X = [(-1.15, 1.31), (-0.15, 1.20), (0.96, 1.12)]                 # (x, 화살 끝 y) · 시작 y = 2.20
MR = (-1.69, 0.33); FT = (0.74, 0.36); FN = (0.12, -0.32); MG = (-0.12, -1.66); LAB_R = 0.42


def layout(variant):
    u = np.array([math.cos(math.radians(-45)), math.sin(math.radians(-45))])
    if variant == 'A':
        rj, kj = R_AM, 'am'
    else:
        rj, kj = R_SE, 'se'
    j = (R_AM + rj) * u
    se = (R_AM + R_SE) * np.array([math.cos(math.radians(210)), math.sin(math.radians(210))])
    contact = R_AM * u
    # F_n 이음선: j 위를 지나 오른쪽으로 → 아래 (A = j 오른쪽 바깥, B = 원래 자리)
    fn_x = (j[0] + rj + 0.21) if variant == 'A' else 2.0
    return dict(j=(float(j[0]), float(j[1]), rj, kj), se=(float(se[0]), float(se[1]), R_SE, 'se'),
                contact=(float(contact[0]), float(contact[1])), u=(float(u[0]), float(u[1])), fn_x=float(fn_x))


def sphere(ax, cx, cy, r, kind, px_per_unit, z):
    n = max(64, int(2 * r * px_per_unit * 2))
    t = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(t, -t)                                       # 행 0 = 위
    d2 = X ** 2 + Y ** 2
    Z = np.sqrt(np.clip(1 - d2, 0, 1))
    L = np.array([-0.45, 0.55, 0.70]); L /= np.linalg.norm(L)
    H = L + np.array([0, 0, 1.0]); H /= np.linalg.norm(H)
    diff = np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1)
    spec = np.clip(X * H[0] + Y * H[1] + Z * H[2], 0, 1)
    base = np.array(C[kind])
    if kind == 'am':
        col = base[None, None, :] * (0.55 + 0.9 * diff[..., None]) + 0.24 * spec[..., None] ** 18 \
              + 0.10 * ((1 - Z) ** 3)[..., None]
    else:
        col = base[None, None, :] * (0.50 + 0.62 * diff[..., None]) + 0.22 * spec[..., None] ** 18
    col = np.clip(col, 0, 1)
    edge = 2.0 / (r * px_per_unit)                                  # 가장자리 2 px 부드럽게
    a = np.clip((1 - np.sqrt(d2)) / edge, 0, 1)
    rgba = np.dstack([col, a])
    ax.imshow(rgba, extent=(cx - r, cx + r, cy - r, cy + r), origin='upper', zorder=z, interpolation='antialiased')


def arrow(ax, p0, p1, color, shaft, head_w, head_l, z):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    v = p1 - p0; L = np.linalg.norm(v); e = v / L; nrm = np.array([-e[1], e[0]])
    b = p1 - e * head_l
    pts = [p0 + nrm * shaft / 2, b + nrm * shaft / 2, b + nrm * head_w / 2, p1, b - nrm * head_w / 2,
           b - nrm * shaft / 2, p0 - nrm * shaft / 2]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor='none', zorder=z))


def polyline_arrow(ax, pts, color, lw_pt, head_w, head_l, z):
    pts = [np.array(p, float) for p in pts]
    last = pts[-1]; prev = pts[-2]; e = (last - prev) / np.linalg.norm(last - prev)
    stop = last - e * head_l * 0.9
    xs = [p[0] for p in pts[:-1]] + [stop[0]]; ys = [p[1] for p in pts[:-1]] + [stop[1]]
    ax.plot(xs, ys, color=color, lw=lw_pt, solid_joinstyle='miter', solid_capstyle='butt', zorder=z)
    nrm = np.array([-e[1], e[0]]); b = last - e * head_l
    ax.add_patch(Polygon([last, b + nrm * head_w / 2, b - nrm * head_w / 2], closed=True, facecolor=color,
                         edgecolor='none', zorder=z))


def arc(ax, cx, cy, r, a0, a1, color, lw_pt, z, head=None):
    th = np.radians(np.linspace(a0, a1, 120))
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=color, lw=lw_pt, solid_capstyle='butt', zorder=z)
    if head:
        hw, hl = head
        t = th[-1]; p = np.array([cx + r * math.cos(t), cy + r * math.sin(t)])
        e = np.array([-math.sin(t), math.cos(t)]) * (1 if a1 > a0 else -1)
        nrm = np.array([-e[1], e[0]])
        ax.add_patch(Polygon([p + e * hl, p + nrm * hw / 2, p - nrm * hw / 2], closed=True, facecolor=color,
                             edgecolor='none', zorder=z))


def draw(ax, variant, pt_per_unit, px_per_unit, labels=True, connectors=True):
    lo = layout(variant)
    U = pt_per_unit
    jx, jy, rj, kj = lo['j']; sx, sy, rs, _ = lo['se']; cxn, cyn = lo['contact']; ux, uy = lo['u']
    # 입자 (j · SE 뒤 → i 앞)
    sphere(ax, jx, jy, rj, kj, px_per_unit, 2)
    sphere(ax, sx, sy, rs, 'se', px_per_unit, 2)
    sphere(ax, 0, 0, R_AM, 'am', px_per_unit, 3)
    # 판 (반투명) · 접점 표지
    ax.add_patch(Polygon(PLATE, closed=True, facecolor=C['plate'], alpha=0.68, edgecolor='none', zorder=4))
    ax.add_patch(Ellipse((-0.10, 1.10), 0.13, 0.05, facecolor='#0A0A0A', edgecolor='none', zorder=4.5))
    # 가압 화살 셋
    for x, yh in RED_X:
        arrow(ax, (x, 2.20), (x, yh), C['red'], 0.075, 0.21, 0.22, 6)
    # 회전 화살 (오른쪽 호 + 왼쪽 화살촉 호)
    arc(ax, 0, 0, 1.17, -80, 32, C['orange_arc'], 0.058 * U, 5)
    arc(ax, 0, 0, 1.17, 150, 188, C['orange_arc'], 0.058 * U, 5, head=(0.17, 0.17))
    # 접점 화살 (법선 = i 쪽 · 접선)
    cp = np.array([cxn, cyn]); un = np.array([ux, uy]); ut = np.array([-uy, ux]) * -1
    arrow(ax, cp, cp - un * 0.40, C['teal'], 0.045, 0.13, 0.12, 6)
    arrow(ax, cp, cp + np.array([-uy, ux]) * 0.30, '#27AE60', 0.045, 0.13, 0.12, 6)
    # 중력 화살
    gx = -0.06
    arrow(ax, (gx, -0.99), (gx, MG[1] + math.sqrt(LAB_R ** 2 - (gx - MG[0]) ** 2) + 0.01), C['navy'], 0.06, 0.17, 0.15, 6)
    # 점선 원 넷
    if not labels:
        return lo
    dash = (0, (2.2, 1.6))
    for (x, y), col in ((MR, C['orange']), (FT, C['green']), (FN, C['teal']), (MG, C['navy'])):
        ax.add_patch(Circle((x, y), LAB_R, facecolor='none', edgecolor=col, lw=0.024 * U, linestyle=dash, zorder=7))
    if labels:
        fs = 0.40 * U
        ax.text(-0.02, 0.43, r'$i$', color='white', fontsize=fs * 0.95, ha='center', va='center', zorder=8)
        jlx, jly = (jx - 0.02, jy + 0.10) if kj == 'am' else (jx, jy - 0.02)
        ax.text(jlx, jly, r'$j$', color='white' if kj == 'am' else '#2B2B2B', fontsize=fs * (0.95 if kj == 'am' else 0.62),
                ha='center', va='center', zorder=8)
        ax.text(FT[0], FT[1] - 0.02, r'$F_t$', color=C['green_txt'], fontsize=fs, ha='center', va='center', zorder=8)
        ax.text(FN[0], FN[1] - 0.02, r'$F_n$', color=C['teal_txt'], fontsize=fs, ha='center', va='center', zorder=8)
        ax.text(MR[0], MR[1] - 0.02, r'$M_r$', color=C['orange'], fontsize=fs, ha='center', va='center', zorder=8)
        ax.text(MG[0], MG[1], r'$m_i g$', color=C['navy'], fontsize=fs * 0.92, ha='center', va='center', zorder=8)
        ax.text(1.12, 1.86, 'Applied\npressure', color=C['red'], fontsize=0.30 * U, fontweight='bold', ha='left',
                va='center', linespacing=1.15, zorder=8)
    if connectors:
        lw = 0.036 * U; hw, hl = 0.15, 0.16
        polyline_arrow(ax, [(MR[0] - LAB_R, MR[1]), (-3.42, MR[1]), (-3.42, 2.27)], C['orange'], lw, hw, hl, 6)
        polyline_arrow(ax, [(FT[0] + LAB_R, FT[1] + 0.02), (2.96, FT[1] + 0.02), (2.96, 2.35)], C['green'], lw, hw, hl, 6)
        y0 = FN[1] + 0.07
        x_start = FN[0] + math.sqrt(LAB_R ** 2 - 0.07 ** 2)
        polyline_arrow(ax, [(x_start, y0), (lo['fn_x'], y0), (lo['fn_x'], -2.65)], C['teal'], lw, hw, hl, 6)
        polyline_arrow(ax, [(MG[0] - LAB_R, MG[1]), (-2.53, MG[1]), (-2.53, -2.69)], C['navy'], lw, hw, hl, 6)
    return lo


def preview(bg_png, variant, out_png, dpi=200):
    from PIL import Image
    im = np.asarray(Image.open(bg_png).convert('RGB')).astype(float) / 255
    H, W = im.shape[:2]
    cx, cy, s = 603, 537, 137                                         # 원 crop (2 배) 의 i 중심 · R (px)
    bg = im.copy()
    bg[208:912, 38:1138, :] = 1.0                                     # 원 그림 지우기 (식 · 머리글은 남김)
    ext = (-cx / s, (W - cx) / s, (cy - H) / s, cy / s)
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.imshow(bg, extent=ext, origin='upper', zorder=0, interpolation='antialiased')
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_aspect('equal')
    pt_per_unit = s / dpi * 72
    lo = draw(ax, variant, pt_per_unit, s)
    fig.savefig(out_png, dpi=dpi)
    plt.close(fig)
    return lo


def export(variant, out_dir, labeled, r_in=0.571, dpi=300):
    lo = layout(variant)
    jx, jy, rj, _ = lo['j']
    x0, x1 = -3.00, max(2.62, jx + rj + 0.06)
    y1 = 2.30
    y0 = min(jy - rj, MG[1] - LAB_R if labeled else -1.30) - 0.06
    W, H = (x1 - x0) * r_in, (y1 - y0) * r_in
    fig = plt.figure(figsize=(W, H), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect('equal')
    draw(ax, variant, r_in * 72, r_in * dpi, labels=labeled, connectors=False)
    tag = 'labeled' if labeled else 'nolabel'
    stem = Path(out_dir) / f'kg50_dem_force_{variant}_{tag}'
    fig.savefig(str(stem) + '.png', dpi=dpi, transparent=True)
    fig.savefig(str(stem) + '.svg', transparent=True)
    plt.close(fig)
    return dict(file=stem.name, size_in=[round(W, 3), round(H, 3)], size_cm=[round(W * 2.54, 2), round(H * 2.54, 2)],
                dpi=dpi, R_AM_in=r_in, R_SE_in=round(r_in / 3, 4), bounds_R=[x0, x1, y0, y1])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', help='원 패널 2배 crop (비교 그림용 · 없으면 단독 그림만)')
    ap.add_argument('--out', required=True)
    ap.add_argument('--export', action='store_true')
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    meta = {}
    for v in ('A', 'B'):
        meta[v] = preview(a.preview, v, out / f'preview_{v}.png') if a.preview else layout(v)
    if a.export:
        meta['export'] = [export(v, out, lab) for v in ('A', 'B') for lab in (True, False)]
    json.dump(meta, open(out / 'layout.json', 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(meta.get('export', meta), ensure_ascii=False))
