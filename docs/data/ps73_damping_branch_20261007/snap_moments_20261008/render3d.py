#!/usr/bin/env python3
"""네 시점 von Mises — 웹앱 'AM 만 — 입자 응력 (LW)' 화면과 같은 꼴의 3D 그림 (1저자 10-08 *"4개를 이 형식으로 줘"*).

입력: vm_moments.py 출력 폴더 (vm_am_<step>.csv · vm_moments.json).  색 = σ_VM (MPa · 절대) · jet · log · 네 장 **같은 범위** (vm_moments.json 의
colour_range_MPa — 2D 그림과 같은 값).  벽 (바닥 · 판) 에 닿은 입자도 칠한다 (1저자 10-08 "벽면 안칠하는거 없애주고" — 그 입자는 벽 힘이 빠진 값 · 웹앱 기본과 같다).
그리기 = numpy 구 임포스터 z-버퍼 — 웹앱 (three.js 0.160) 의 카메라 · 조명 · Phong 재질 · 색 관리를 식으로 옮김 (2 배 초표본 · 투명 배경 RGBA) — 계산 값은 바꾸지 않는다.

  python3 render3d.py <vm_moments 출력 폴더> <그림 폴더> [--px 1400]
  python3 render3d.py --selftest
출력: vm3d_<step>.png (투명 배경 · 네 장 같은 카메라 · 같은 축척) · vm3d_colorbar.png (세로 · 영문) · vm3d_4panel.png (미리보기 · 흰 바탕)
"""
import argparse
import csv
import json
import math
import os
import sys

import numpy as np

WALL_RGB = (0.72, 0.72, 0.72)                              # (옛 판 · 지금은 쓰지 않는다 — 1저자 10-08 "벽면 안칠하는거 없애주고")

# ── 웹앱 (webapp/static/js/viewer3d.js · three.js 0.160) 과 같은 색 · 조명 · 카메라 ──────────────────────────────
#  색 = jetColor(t) (8 비트 반올림 sRGB) → three.js 색 관리 (r152+): sRGB → 선형 → 조명 → 선형 → sRGB 출력.
#  재질 = MeshPhongMaterial (흰색 × 입자 색 · specular 0x111111 · shininess 30) · 물리 기준 조명 (r155+ 기본 · π 배율 없음):
#    diffuse = albedo × (I_amb + I_dir · max(0, n·L)) / π · specular = I_dir · max(0, n·L) · F_Schlick · 0.25 · D_BlinnPhong.
#  조명 = AmbientLight 0.4 + DirectionalLight 0.8 (위치 (1, 1.5, 1) → 원점 · 세계 고정) · 카메라 = 원근 50° ·
#  위치 = 상자 중심 + (1.2, 0.8, 1.2) × 최대 변 (THREE 좌표 = (data x, data z, data y)).
AMB_I, DIR_I = 0.4, 0.8
DIR_POS = np.array([1.0, 1.5, 1.0])
SPEC_HEX, SHININESS = 0x11, 30.0
FOV_DEG = 50.0


def jet8(t):
    """viewer3d.js jetColor(t) 그대로 — 8 비트 반올림 sRGB (0–1)."""
    t = np.clip(np.asarray(t, dtype=float), 0.0, 1.0)
    r = np.clip(1.5 - np.abs(4.0 * t - 3.0), 0.0, 1.0)
    g = np.clip(1.5 - np.abs(4.0 * t - 2.0), 0.0, 1.0)
    b = np.clip(1.5 - np.abs(4.0 * t - 1.0), 0.0, 1.0)
    return np.round(np.stack([r, g, b], axis=-1) * 255.0) / 255.0


jet = jet8                                                    # 옛 이름 (시험 · 호출 호환)


def srgb_to_lin(c):
    c = np.asarray(c, dtype=float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(np.asarray(c, dtype=float), 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1.0 / 2.4) - 0.055)


def colours(vm, wall, lo, hi, grey_wall=False, scale='log'):
    """σ_VM → jetColor.  scale 'log' = log 정규화 (웹앱 netCurrentT 와 같은 식) · 'linear' = (σ − lo) / (hi − lo) (1저자 10-08 "그냥 이등분").
    벽 입자도 칠한다 (grey_wall=False · 1저자 10-08)."""
    if scale == 'linear':
        t = (np.clip(vm, lo, hi) - lo) / (hi - lo)
    else:
        t = (np.log10(np.clip(vm, lo, hi)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    rgb = jet8(t)
    if grey_wall:
        rgb[wall] = WALL_RGB
    return rgb


def phong_r160(albedo_srgb, n, L, V):
    """three.js r160 MeshPhongMaterial 한 점의 출력 sRGB (0–1) — albedo · 법선 · 빛 · 시선 방향 (단위)."""
    alb = srgb_to_lin(albedo_srgb)
    dotNL = np.clip((n * L).sum(-1), 0.0, 1.0)
    Hh = L + V
    Hh = Hh / np.linalg.norm(Hh, axis=-1, keepdims=True)
    dotNH = np.clip((n * Hh).sum(-1), 0.0, 1.0)
    dotVH = np.clip((V * Hh).sum(-1), 0.0, 1.0)
    f0 = float(srgb_to_lin(SPEC_HEX / 255.0))
    fres = np.exp2((-5.55473 * dotVH - 6.98316) * dotVH)
    F = f0 * (1.0 - fres) + fres
    D = (1.0 / math.pi) * (SHININESS * 0.5 + 1.0) * np.power(dotNH, SHININESS)
    spec = DIR_I * dotNL * F * 0.25 * D
    diff = (AMB_I + DIR_I * dotNL)[..., None] * alb / math.pi
    return lin_to_srgb(diff + spec[..., None])


def webapp_camera(box_lo, box_hi):
    """웹앱 buildScene 의 기본 시점 — THREE 좌표 (x, z, y).  → (위치, 중심, 오른쪽, 위, 앞)."""
    lo = np.array([box_lo[0], box_lo[2], box_lo[1]], float)    # data → THREE
    hi = np.array([box_hi[0], box_hi[2], box_hi[1]], float)
    c = 0.5 * (lo + hi)
    md = float(np.max(hi - lo))
    pos = c + np.array([1.2, 0.8, 1.2]) * md
    fwd = (c - pos) / np.linalg.norm(c - pos)
    right = np.cross(fwd, [0.0, 1.0, 0.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return pos, c, right, up, fwd


def render(xyz, r, rgb, px=1400, ss=2, bounds=None, crop=None):
    """웹앱과 같은 카메라 · 조명 · 재질로 구들을 그린다 → RGBA (0–1).  xyz = data 좌표 (µm).  bounds = 카메라를 맞출 상자 (네 장 같게)."""
    xyz = np.asarray(xyz, float)
    r = np.asarray(r, float)
    lo_w = np.asarray(bounds[0] if bounds is not None else (xyz - r[:, None]).min(0), float)
    hi_w = np.asarray(bounds[1] if bounds is not None else (xyz + r[:, None]).max(0), float)
    pos, c, right, up, fwd = webapp_camera(lo_w, hi_w)
    P = np.stack([xyz[:, 0], xyz[:, 2], xyz[:, 1]], axis=1)    # data → THREE
    d = P - pos
    xc, yc, zc = d @ right, d @ up, d @ fwd                    # zc = 앞으로의 깊이 (양수)
    N = px * ss
    tanh = math.tan(math.radians(FOV_DEG) / 2.0)
    k = (N / 2.0) / tanh                                       # 정사각 화면 (가로세로비 1) — 자르기로 맞춘다
    X = N / 2.0 + k * xc / zc
    Y = N / 2.0 - k * yc / zc
    RR = k * r / zc
    zbuf = np.full((N, N), np.inf)
    img = np.zeros((N, N, 3))
    Ldir = DIR_POS / np.linalg.norm(DIR_POS)
    for i in np.argsort(-zc):
        x0, y0, rr = X[i], Y[i], RR[i]
        if rr < 0.5:
            continue
        i0, i1 = int(max(0, math.floor(x0 - rr))), int(min(N - 1, math.ceil(x0 + rr)))
        j0, j1 = int(max(0, math.floor(y0 - rr))), int(min(N - 1, math.ceil(y0 + rr)))
        if i0 > i1 or j0 > j1:
            continue
        gx, gy = np.meshgrid(np.arange(i0, i1 + 1) + 0.5, np.arange(j0, j1 + 1) + 0.5)
        u = (gx - x0) / rr
        v = -(gy - y0) / rr
        q = 1.0 - u * u - v * v
        m = q > 0
        if not m.any():
            continue
        w = np.sqrt(np.where(m, q, 0.0))
        depth = zc[i] - r[i] * w                               # 카메라에 가까울수록 작다
        sub = zbuf[j0:j1 + 1, i0:i1 + 1]
        win = m & (depth < sub)
        if not win.any():
            continue
        n = u[..., None] * right + v[..., None] * up - w[..., None] * fwd     # 세계 (THREE) 법선
        V = (pos - P[i]) / np.linalg.norm(pos - P[i])
        col = phong_r160(rgb[i][None, None, :], n, Ldir[None, None, :], V[None, None, :])
        sub[win] = depth[win]
        img[j0:j1 + 1, i0:i1 + 1][win] = col[win]
    alpha = np.isfinite(zbuf).astype(float)
    rgba = np.concatenate([img, alpha[..., None]], axis=-1)
    if ss > 1:
        rgba = rgba.reshape(px, ss, px, ss, 4).mean(axis=(1, 3))
        a = rgba[..., 3:4]
        rgba[..., :3] = np.where(a > 0, rgba[..., :3] / np.maximum(a, 1e-12), 0.0)
    if crop is not None:
        (ya, yb), (xa, xb) = crop
        rgba = rgba[ya:yb, xa:xb]
    return rgba


def bbox(rgba, pad=12):
    ys, xs = np.where(rgba[..., 3] > 0)
    return (max(0, ys.min() - pad), min(rgba.shape[0], ys.max() + 1 + pad)), (max(0, xs.min() - pad), min(rgba.shape[1], xs.max() + 1 + pad))


def save_png(path, rgba):
    from PIL import Image
    Image.fromarray(np.clip(np.round(rgba * 255), 0, 255).astype(np.uint8), 'RGBA').save(path)


def read_moment(d, step):
    rows = list(csv.DictReader(open(os.path.join(d, f'vm_am_{step}.csv'), encoding='utf-8')))
    xyz = np.array([[float(r['x_um']), float(r['y_um']), float(r['z_um'])] for r in rows])
    rad = np.array([float(r['r_um']) for r in rows])
    vm = np.array([float(r['vm_MPa']) for r in rows])
    wall = np.array([r['wall'] == '1' for r in rows])
    return xyz, rad, vm, wall


def colorbar_png(path, lo, hi, scale='log', labels=True):
    """범례 — 세 눈금 (아래 · 가운데 · 위).  선형 = 가운데 (lo + hi) / 2 (이등분) · log = 기하평균 √(lo · hi) (SDCP 때와 같은 규칙).
    labels=False = 숫자 없는 막대 (슬라이드에서 직접 적을 때)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm, Normalize, ListedColormap
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Liberation Sans', 'Arial', 'DejaVu Sans'], 'font.size': 9})
    cmap = ListedColormap(jet8(np.linspace(0.0, 1.0, 256)))              # 웹앱 jetColor 와 같은 색 (구의 바탕색 · 조명 전)
    norm = Normalize(lo, hi) if scale == 'linear' else LogNorm(lo, hi)
    mid = 0.5 * (lo + hi) if scale == 'linear' else math.sqrt(lo * hi)
    fig = plt.figure(figsize=(1.25, 4.2))
    ax = fig.add_axes([0.18, 0.05, 0.22, 0.9])
    cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax)
    cb.ax.minorticks_off()
    if labels:
        fmt = lambda v: '0' if v == 0 else f'{v:.3g}'
        cb.set_ticks([lo, mid, hi])
        cb.set_ticklabels([fmt(lo), fmt(mid), fmt(hi)])
        cb.set_label(r'von Mises stress, $\sigma_{\mathrm{VM}}$ (MPa)')
    else:
        cb.set_ticks([])
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)
    return mid


def run(src, out, px=1400, scale='log'):
    meta = json.load(open(os.path.join(src, 'vm_moments.json'), encoding='utf-8'))
    cr = meta['colour_range_MPa']
    lo, hi = float(cr['vmin']), float(cr['vmax'])
    if scale == 'linear':
        lo = 0.0                                               # 선형 = 0 … 모은 p95 (1저자 10-08 "그냥 이등분")
    os.makedirs(out, exist_ok=True)
    moms = meta['moments']
    data = {m['step']: read_moment(src, m['step']) for m in moms}
    bx, by = moms[0]['box_um']
    zmax = max(m['plate_z_um'] for m in moms)
    bounds = (np.array([0.0, 0.0, 0.0]), np.array([bx, by, zmax]))   # 네 장 같은 카메라 (가장 높은 판 기준 상자)
    full = []
    for m in moms:
        xyz, rad, vm, wall = data[m['step']]
        full.append(render(xyz, rad, colours(vm, wall, lo, hi, scale=scale), px, 2, bounds))
    boxes = [bbox(a) for a in full]                            # 네 장 같은 자르기 (합집합) — 나란히 놓으면 자리가 맞는다
    ya, yb = min(b[0][0] for b in boxes), max(b[0][1] for b in boxes)
    xa, xb = min(b[1][0] for b in boxes), max(b[1][1] for b in boxes)
    imgs = [a[ya:yb, xa:xb] for a in full]
    for m, rgba in zip(moms, imgs):
        save_png(os.path.join(out, f'vm3d_{m["step"]}.png'), rgba)
    colorbar_png(os.path.join(out, 'vm3d_colorbar.png'), lo, hi, scale)
    colorbar_png(os.path.join(out, 'vm3d_colorbar_bare.png'), lo, hi, scale, labels=False)
    from PIL import Image, ImageDraw
    tiles = []
    for k, (m, rgba) in enumerate(zip(moms, imgs)):
        im = Image.fromarray(np.clip(np.round(rgba * 255), 0, 255).astype(np.uint8), 'RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        ImageDraw.Draw(bg).text((10, 10), f'({chr(97 + k)}) step {m["step"]:,}', fill=(0, 0, 0, 255))
        tiles.append(bg.convert('RGB'))
    canvas = Image.new('RGB', (sum(t.size[0] for t in tiles), tiles[0].size[1]), (255, 255, 255))
    x = 0
    for t in tiles:
        canvas.paste(t, (x, 0))
        x += t.size[0]
    canvas.save(os.path.join(out, 'vm3d_4panel.png'))
    return lo, hi


def selftest():
    ok, fail = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
            print(f'  PASS  {name}')
        else:
            fail.append(name)
            print(f'  FAIL  {name}  {extra}')

    chk('R1 jet8 = viewer3d.js jetColor (8 비트 반올림: 0 → #000080 · 0.5 → #80FF80 · 1 → #800000)',
        np.allclose(jet8(0.0) * 255, [0, 0, 128]) and np.allclose(jet8(0.5) * 255, [128, 255, 128]) and np.allclose(jet8(1.0) * 255, [128, 0, 0]))
    c = colours(np.array([1.0, 10.0, 100.0, 50.0]), np.array([False, False, False, True]), 1.0, 100.0)
    chk('R2 색 = log 정규화 (1 → 0 · 10 → 0.5 · 100 → 1) · 벽 입자도 칠함 (회색 아님)',
        np.allclose(c[0], jet8(0.0)) and np.allclose(c[1], jet8(0.5)) and np.allclose(c[2], jet8(1.0))
        and np.allclose(c[3], jet8(math.log10(50.0) / 2.0)))
    cl = colours(np.array([0.0, 50.0, 100.0]), np.zeros(3, bool), 0.0, 100.0, scale='linear')
    chk('R2b 선형 눈금 — 0 → 0 · 50 → 0.5 · 100 → 1', np.allclose(cl[0], jet8(0.0)) and np.allclose(cl[1], jet8(0.5)) and np.allclose(cl[2], jet8(1.0)))
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td:
        m_lin = colorbar_png(os.path.join(td, 'a.png'), 0.0, 413.0, 'linear')
        m_log = colorbar_png(os.path.join(td, 'b.png'), 5.94, 413.0, 'log')
    chk(f'R2c 범례 가운데 — 선형 = (0 + 413) / 2 = {m_lin:.4g} · log = √(5.94 × 413) = {m_log:.4g}',
        abs(m_lin - 206.5) < 1e-9 and abs(m_log - math.sqrt(5.94 * 413.0)) < 1e-9)
    # three.js r160 Phong — n = L = V 인 점: 선형 albedo × (0.4 + 0.8) / π + 반사광 → sRGB
    n = np.array([[[0.0, 1.0, 0.0]]])
    out = phong_r160(np.array([[[1.0, 1.0, 1.0]]]), n, n, n)[0, 0]
    f0 = float(srgb_to_lin(0x11 / 255.0))
    fres = 2.0 ** ((-5.55473 - 6.98316) * 1.0)
    spec = 0.8 * (f0 * (1 - fres) + fres) * 0.25 * (16.0 / math.pi)
    want = float(lin_to_srgb(1.2 / math.pi + spec))
    chk(f'R3 Phong (three.js r160 · 물리 조명 · sRGB) 손 계산과 같음 ({out[0]:.6f} ↔ {want:.6f})', np.allclose(out, want, atol=1e-9))
    chk('R4 sRGB ↔ 선형 왕복', np.allclose(lin_to_srgb(srgb_to_lin(np.linspace(0, 1, 11))), np.linspace(0, 1, 11), atol=1e-9))
    # z-버퍼 — 카메라 시선 위에 두 구 · 카메라 쪽 (빨강) 이 앞 · 바깥 투명 · 순서 무관
    lo_b, hi_b = np.array([0.0, 0.0, 0.0]), np.array([10.0, 10.0, 10.0])
    pos, cc, right, up, fwd = webapp_camera(lo_b, hi_b)
    cdata = np.array([cc[0], cc[2], cc[1]])                    # THREE → data
    toward = -np.array([fwd[0], fwd[2], fwd[1]])               # data 좌표에서 카메라 쪽
    xyz = np.array([cdata + 1.0 * toward, cdata - 1.0 * toward])
    rad = np.array([1.5, 1.5])
    cols = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    rgba = render(xyz, rad, cols, 160, 1, (lo_b, hi_b))
    mid = rgba[80, 80]
    chk(f'R5 겹친 두 구 — 카메라 쪽 (빨강) 이 앞 ({np.round(mid, 3)})', mid[0] > 0.2 and mid[2] < 0.05 and mid[3] == 1.0)
    chk('R6 구 바깥 = 투명 (알파 0)', rgba[2, 2, 3] == 0.0 and rgba[-3, -3, 3] == 0.0)
    rgba2 = render(xyz[::-1], rad[::-1], cols[::-1], 160, 1, (lo_b, hi_b))
    chk('R7 그리는 순서를 뒤집어도 같은 그림 (z-버퍼)', np.allclose(rgba, rgba2))
    print(f'\n{ok} PASS · {len(fail)} FAIL')
    return 0 if not fail else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='네 시점 von Mises — 웹앱 꼴 3D 그림 (투명 배경 · 같은 색 범위 · 같은 카메라)')
    ap.add_argument('src', nargs='?', help='vm_moments.py 출력 폴더')
    ap.add_argument('out', nargs='?', help='그림 폴더')
    ap.add_argument('--px', type=int, default=1400)
    ap.add_argument('--scale', choices=('log', 'linear'), default='log', help='색 눈금 — linear = 0 … p95 · 범례 이등분')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.src and a.out):
        ap.error('src · out 이 필요하다 (또는 --selftest)')
    lo, hi = run(a.src, a.out, a.px, a.scale)
    print(f'색 범위 {lo:.3g} … {hi:.3g} MPa ({a.scale} · 위 = vm_moments.json 공동 p95) → {a.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
