#!/usr/bin/env python3
"""50kg 4차년도 보고 0쪽 (DEM 해석 방법) 그림 둘 — 2D 모식 계산 (그림용 · 실제 3D 덱 결과 아님).

  p0_process_{labeled,nolabel}       : 해석 절차 네 단계 (1 × 4 띠 · p0_process_grid_* = 같은 그림 2 × 2 배치) (입자 생성 → 중력 침강 → 가압 → 판 고정 · 이완) · 빨간 선 = 접촉 힘 사슬 (굵기 ∝ 법선력 · 가압 단계 최대로 정규화)
  p0_contact_model_{labeled,nolabel} : 접촉 모델 (가압 중 접촉 i–j 의 힘 · 겹침 δ 와 접촉 요소 · 법선 이력 k1/k2 · 접선 마찰 한계 μF_n)

2D 모식 계산: 단일 입도 활물질 (지름 6) 20 개 + 고체전해질 (지름 2) 94 개 (85:15 wt% 를 면적비로 · 진밀도 4.85 · 1.64) · 다이 폭 48 ·
  삽입 영역 높이 45 (면적 분율 0.40) · 선형 스프링 (AM 강성 = SE 의 50 배) · 마찰 상한 μ 0.5 · 회전 생략 · 판 일정 속도 → 판 힘 목표에서 정지 → 판 고정 이완.
  그림 모양을 위한 계산이다 — 값 (힘 · 길이 · 시간) 은 임의 단위이고 3D 덱 값이 아니다.  씨앗 = 23 (판 정지 뒤 판 힘 하락이 보이는 예 · 같은 계산 네 씨앗 중 둘은 오름 — README).

사용:
  python3 -P make_fig_p0_dem_method.py            # 저장된 모식 계산 상태로 그림만
  python3 -P make_fig_p0_dem_method.py --sim      # 모식 계산 다시 (씨앗 23 · 약 70 초) → 상태 JSON 덮어씀
  python3 -P make_fig_p0_dem_method.py --scan     # 씨앗 11 · 13 · 17 · 23 판 힘 (정지 · 이완 끝) 만 출력
  python3 -P make_fig_p0_dem_method.py --check    # 저장 상태 · 그림 검사 (모식 계산 안 돌림)
"""
import argparse, hashlib, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'p0_dem_method')
SEED = 23
STATE = os.path.join(OUT, 'toy2d_seed23.json')

R_AM, R_SE = 3.0, 1.0
RHO_AM, RHO_SE = 4.85, 1.64
W = 48.0
N_AM, N_SE = 20, 94
INS_Y0, INS_Y1 = 1.0, 46.0
K_AM, K_SE = 30000.0, 600.0
MU = 0.5
G = 0.01
DT = 0.01

def setup(seed):
    rng = np.random.default_rng(seed)
    pos, rad = [], []
    order = [R_AM] * N_AM + [R_SE] * N_SE
    for r in order:
        for _ in range(200000):
            x = rng.uniform(r, W - r); y = rng.uniform(INS_Y0 + r, INS_Y1 - r)
            if all((x - px) ** 2 + (y - py) ** 2 >= (r + pr) ** 2 for (px, py), pr in zip(pos, rad)):
                pos.append((x, y)); rad.append(r); break
        else:
            raise SystemExit('placement failed')
    x = np.array(pos); r = np.array(rad)
    am = r > 2
    m = np.where(am, RHO_AM, RHO_SE) * np.pi * r ** 2
    k = np.where(am, K_AM, K_SE)
    return x, r, am, m, k

def forces(x, v, r, m, k, plate_y, plate_v, gamma, want=False):
    n_ = len(r)
    F = np.zeros_like(x)
    F[:, 1] -= m * G
    F -= gamma * m[:, None] * v
    d = x[:, None, :] - x[None, :, :]
    dist = np.sqrt((d ** 2).sum(-1)) + np.eye(n_)
    ov = r[:, None] + r[None, :] - dist
    iu, ju = np.where(np.triu(ov > 0, 1))
    contacts = []
    if len(iu):
        nvec = d[iu, ju] / dist[iu, ju][:, None]
        kij = k[iu] * k[ju] / (k[iu] + k[ju])
        meff = m[iu] * m[ju] / (m[iu] + m[ju])
        cn = 2 * 0.3 * np.sqrt(meff * kij)
        rel = v[iu] - v[ju]
        vn = (rel * nvec).sum(1)
        fn = np.maximum(kij * ov[iu, ju] - cn * vn, 0.0)
        vt = rel - vn[:, None] * nvec
        vtm = np.linalg.norm(vt, axis=1) + 1e-12
        ftm = np.minimum(cn * vtm, MU * fn)
        ft = -ftm[:, None] * vt / vtm[:, None]
        f = fn[:, None] * nvec + ft
        np.add.at(F, iu, f); np.add.at(F, ju, -f)
        if want:
            contacts = [(int(a), int(b), float(c), float(e)) for a, b, c, e in zip(iu, ju, fn, ftm)]
    walls = []
    # left · right · floor · plate (평면 벽 = 입자 강성 그대로)
    for axis, side, pos in ((0, +1, 0.0), (0, -1, W), (1, +1, 0.0)):
        ovw = r - side * (x[:, axis] - pos)
        idx = np.where(ovw > 0)[0]
        if len(idx):
            vn = side * v[idx, axis]
            cn = 2 * 0.3 * np.sqrt(m[idx] * k[idx])
            fn = np.maximum(k[idx] * ovw[idx] - cn * vn, 0.0)
            F[idx, axis] += side * fn
            if want: walls += [(int(i), 'wall', float(f)) for i, f in zip(idx, fn)]
    fplate = 0.0
    if plate_y is not None:
        ovp = x[:, 1] + r - plate_y
        idx = np.where(ovp > 0)[0]
        if len(idx):
            vrel = v[idx, 1] - plate_v
            cn = 2 * 0.3 * np.sqrt(m[idx] * k[idx])
            fn = np.maximum(k[idx] * ovp[idx] + cn * vrel, 0.0)
            F[idx, 1] -= fn
            fplate = float(fn.sum())
            if want: walls += [(int(i), 'plate', float(f)) for i, f in zip(idx, fn)]
    return F, contacts, walls, fplate

F_TARGET = 30.0


def run(seed=SEED, f_target=F_TARGET, verbose=True):
    x, r, am, m, k = setup(seed)
    v = np.zeros_like(x); v[:, 1] = -0.5
    snaps = {}
    def snap(name, plate_y, extra=None):
        F, c, w, fp = forces(x, v, r, m, k, plate_y, 0.0, 0.0, want=True)
        snaps[name] = dict(x=x.copy().tolist(), plate_y=plate_y, contacts=c, walls=w, fplate=fp, **(extra or {}))
    snap('insert', None)
    # 침강 (중력 · 감쇠)
    for s in range(60000):
        F, *_ = forces(x, v, r, m, k, None, 0.0, 0.02 if s < 20000 else 0.3)
        v += F / m[:, None] * DT; x += v * DT
        if s > 20000 and s % 500 == 0 and (0.5 * m * (v ** 2).sum(1)).sum() < 1e-6: break
    top = float((x[:, 1] + r).max())
    snap('settle', top + 1.0, dict(steps=s))
    # 판 설치 + 안정화
    plate = top + 1.0
    for s in range(3000):
        F, *_ = forces(x, v, r, m, k, plate, 0.0, 0.5)
        v += F / m[:, None] * DT; x += v * DT
    h0 = float((x[:, 1] + r).max())
    # 가압 (판 일정 속도 · 판 힘 ≥ 목표에서 정지)
    vp = -0.05
    for s in range(200000):
        plate += vp * DT
        F, _, _, fp = forces(x, v, r, m, k, plate, vp, 0.5)
        v += F / m[:, None] * DT; x += v * DT
        if s % 10000 == 0 and verbose: print('  c', s, round(plate, 3), round(fp / W, 3), flush=True)
        if fp / W >= f_target: break
    snap('compress', plate, dict(steps=s, f_stop=fp))
    # 판 고정 이완 (감쇠 작게)
    for s2 in range(20000):
        F, _, _, fp = forces(x, v, r, m, k, plate, 0.0, 0.01)
        v += F / m[:, None] * DT; x += v * DT
    snap('relax', plate, dict(steps=s2, f_end=fp))
    meta = dict(seed=seed, f_target=f_target, h_settle_top=top, h_after_stab=h0, plate_stop=plate,
                f_stop=snaps['compress']['fplate'], f_relax=snaps['relax']['fplate'], r=r.tolist(), am=am.tolist())
    if verbose:
        print(json.dumps({kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in meta.items() if kk not in ('r', 'am')}))
    return snaps, meta



# ───────────────────────── 그림 ─────────────────────────
def _mpl():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': ['Carlito', 'WenQuanYi Zen Hei', 'DejaVu Sans'], 'svg.fonttype': 'none', 'svg.hashsalt': 'kg50p0',
                         'mathtext.fontset': 'custom', 'mathtext.it': 'Carlito:italic', 'mathtext.rm': 'Carlito', 'mathtext.bf': 'Carlito:bold'})
    return plt

_mpl()

from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Polygon, Arc
from matplotlib.collections import PatchCollection, LineCollection
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.4, foreground='white')]
AM_C, SE_C, WALL_C, INK, INK2 = '#1A1A1A', '#CDB650', '#8C8C8C', '#262626', '#595959'
PLATE_C, CHAIN_C, PRESS_C = '#6F8FB8', '#B03A2E', '#8B1A1A'
TEAL, GREEN, NAVY, ORANGE = '#138D75', '#2E8B57', '#34495E', '#C9622A'
TEAL_T, GREEN_T, NAVY_T = '#5FE0CC', '#9BE8B6', '#C9D8EA'
CTX = {}

def draw_bed(ax, sn, fmax=None, chains=True, alpha_bg=1.0, lw_scale=1.0):
    r, am = CTX['r'], CTX['am']
    x = np.array(sn['x'])
    pats_se = [Circle(p, rr) for p, rr, a in zip(x, r, am) if not a]
    pats_am = [Circle(p, rr) for p, rr, a in zip(x, r, am) if a]
    ax.add_collection(PatchCollection(pats_se, facecolor=SE_C, edgecolor='#9C8A3A', linewidth=0.25, alpha=alpha_bg, zorder=2))
    ax.add_collection(PatchCollection(pats_am, facecolor=AM_C, edgecolor='#000000', linewidth=0.25, alpha=alpha_bg, zorder=3))
    if chains and fmax:
        segs, lws = [], []
        for i, j, fn, ft in sn['contacts']:
            if fn < 0.12 * fmax: continue
            segs.append([x[i], x[j]]); lws.append((0.3 + 1.8 * fn / fmax) * lw_scale)
        ax.add_collection(LineCollection(segs, colors=CHAIN_C, linewidths=lws, alpha=0.9, capstyle='round', zorder=4))
    return x

def die(ax, top=48.5, t=1.3):
    for rect in (Rectangle((-t, -t), t, top + t), Rectangle((W, -t), t, top + t), Rectangle((-t, -t), W + 2 * t, t)):
        rect.set(facecolor=WALL_C, edgecolor='none', zorder=1); ax.add_patch(rect)

def plate(ax, y, h=1.6, fixed=False):
    ax.add_patch(Rectangle((0, y), W, h, facecolor=PLATE_C, edgecolor='none', zorder=5))
    if fixed:
        for xx in (-1.3, W):
            ax.add_patch(Rectangle((xx, y - 0.4), 1.3, h + 0.8, facecolor='#404040', edgecolor='none', zorder=6))

def press_arrows(ax, y, n=3, L=9.0):
    for xx in np.linspace(W * 0.2, W * 0.8, n):
        ax.add_patch(FancyArrowPatch((xx, y + L + 1.0), (xx, y + 1.9), arrowstyle='-|>', mutation_scale=6, lw=1.1, color=PRESS_C, zorder=6))

def process(out, labeled):
    plt = _mpl(); snaps = CTX['snaps']
    fig = plt.figure(figsize=(4.50, 1.55 if labeled else 1.22), dpi=300)
    fmax = max(c[2] for c in snaps['compress']['contacts'])
    left, gap, pw = 0.03, 0.045, (1 - 0.06 - 3 * 0.045) / 4
    bottom, ph = (0.04, 0.92) if not labeled else (0.03, 0.74)
    titles = ['① 입자 생성', '② 중력 침강', '③ 가압', '④ 판 고정 · 이완']
    for k, name in enumerate(['insert', 'settle', 'compress', 'relax']):
        ax = fig.add_axes([left + k * (pw + gap), bottom, pw, ph]); ax.set_xlim(-1.6, W + 1.6); ax.set_ylim(-1.6, 50.0); ax.set_aspect('equal'); ax.axis('off')
        die(ax)
        sn = snaps[name]
        draw_bed(ax, sn, fmax=fmax, chains=name in ('compress', 'relax'))
        if name == 'insert':
            ax.add_patch(Rectangle((0, 1.0), W, 45.0, fill=False, edgecolor=INK2, linestyle=(0, (2, 2)), linewidth=0.5, zorder=6))
        if name == 'settle':
            plate(ax, sn['plate_y'])
        if name == 'compress':
            plate(ax, sn['plate_y']); press_arrows(ax, sn['plate_y'])
        if name == 'relax':
            plate(ax, sn['plate_y'], fixed=True)
        if labeled:
            fig.text(left + k * (pw + gap) + pw / 2, bottom + ph + 0.04, titles[k], ha='center', va='bottom', fontsize=7.5, color=INK)
        if k < 3:
            xa = left + (k + 1) * (pw + gap) - gap / 2
            fig.patches.append(FancyArrowPatch((xa - 0.012, bottom + ph * 0.35), (xa + 0.012, bottom + ph * 0.35), transform=fig.transFigure,
                                               arrowstyle='-|>', mutation_scale=8, lw=1.2, color='#A6A6A6'))
    fig.savefig(out + '.png', dpi=300, transparent=True); fig.savefig(out + '.svg', transparent=True); plt.close(fig)


def process_grid(out, labeled):
    """해석 절차 네 단계 2 × 2 배치 (같은 배율)."""
    plt = _mpl(); snaps = CTX['snaps']
    fig = plt.figure(figsize=(4.50, 4.10 if labeled else 3.70), dpi=300)
    fmax = max(c[2] for c in snaps['compress']['contacts'])
    titles = ['① 입자 생성 — 겹치지 않게 무작위 배치', '② 중력 침강 — 쌓인 뒤 가압판 설치',
              '③ 가압 — 목표 판 압력에서 판 정지', '④ 판 고정 · 이완 — 응력 완화 → 비교 상태']
    pw, gx = 0.44, 0.06
    ph = 0.40 if labeled else 0.455
    for k, name in enumerate(['insert', 'settle', 'compress', 'relax']):
        col, row = k % 2, k // 2
        x0 = 0.03 + col * (pw + gx); y0 = (0.52 if row == 0 else 0.03) if labeled else (0.53 if row == 0 else 0.02)
        ax = fig.add_axes([x0, y0, pw, ph]); ax.set_xlim(-1.6, W + 1.6); ax.set_ylim(-1.6, 50.0); ax.set_aspect('equal'); ax.axis('off')
        die(ax)
        sn = snaps[name]
        draw_bed(ax, sn, fmax=fmax, chains=name in ('compress', 'relax'))
        if name == 'insert':
            ax.add_patch(Rectangle((0, 1.0), W, 45.0, fill=False, edgecolor=INK2, linestyle=(0, (2, 2)), linewidth=0.5, zorder=6))
        if name == 'settle':
            plate(ax, sn['plate_y'])
        if name == 'compress':
            plate(ax, sn['plate_y']); press_arrows(ax, sn['plate_y'])
        if name == 'relax':
            plate(ax, sn['plate_y'], fixed=True)
        if labeled:
            fig.text(x0 + pw / 2, y0 + ph + 0.012, titles[k], ha='center', va='bottom', fontsize=7.2, color=INK)
    fig.savefig(out + '.png', dpi=300, transparent=True); fig.savefig(out + '.svg', transparent=True); plt.close(fig)


def arrow(ax, p0, p1, color, lw=1.3, ms=7, z=8):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=ms, lw=lw, color=color, zorder=z, shrinkA=0, shrinkB=0))

def spring(ax, p0, p1, n=6, amp=0.10, color=INK, lw=1.0, z=9):
    p0, p1 = np.array(p0, float), np.array(p1, float); L = np.linalg.norm(p1 - p0); e = (p1 - p0) / L; q = np.array([-e[1], e[0]])
    pts = [p0, p0 + e * L * 0.15]
    for k in range(1, 2 * n):
        pts.append(p0 + e * L * (0.15 + 0.7 * k / (2 * n)) + q * amp * (1 if k % 2 else -1))
    pts += [p0 + e * L * 0.85, p1]
    pts = np.array(pts); ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, zorder=z, solid_joinstyle='round')

def panel_a(ax, labeled=True):
    x, r, am, C, fmax, py, I, J = (CTX[k] for k in ('x', 'r', 'am', 'C', 'fmax', 'py', 'I', 'J'))
    xi, yi = x[I]; x0, x1 = xi - 8.6, xi + 9.4; y0, y1 = yi - 7.6, py + 5.2
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect('equal'); ax.axis('off')
    vis = [k for k in range(len(r)) if x0 - r[k] < x[k, 0] < x1 + r[k] and y0 - r[k] < x[k, 1] < y1 + r[k]]
    for k in vis:
        if k in (I, J): continue
        fc = AM_C if am[k] else SE_C; ec = '#000000' if am[k] else '#9C8A3A'
        ax.add_patch(Circle(x[k], r[k], facecolor=fc, edgecolor=ec, lw=0.3, alpha=0.20 if am[k] else 0.33, zorder=2))
    for k in (I, J):
        ax.add_patch(Circle(x[k], r[k], facecolor=AM_C, edgecolor='#000000', lw=0.4, zorder=3))
    ax.add_patch(Rectangle((x0 - 2, py), x1 - x0 + 4, 1.2, facecolor=PLATE_C, edgecolor='none', zorder=5))
    for xx in np.linspace(x0 + 3.0, x1 - 3.0, 3):
        arrow(ax, (xx, py + 4.8), (xx, py + 1.35), PRESS_C, lw=1.1, ms=6)
    n = (x[I] - x[J]) / np.linalg.norm(x[I] - x[J]); t = np.array([n[1], -n[0]])
    cp = x[J] + n * r[J]
    arrow(ax, cp, cp + n * 2.0, TEAL_T, lw=1.7)                                          # F_n (j → i)
    arrow(ax, cp, cp + t * 2.2, GREEN, lw=1.7)                                           # F_t
    gx = xi - 1.0
    arrow(ax, (gx, yi + 0.4), (gx, yi - 3.2), NAVY_T, lw=1.7)                            # m_i g
    ax.add_patch(Arc(x[I], 7.4, 7.4, angle=0, theta1=125, theta2=215, color=ORANGE, lw=1.4, zorder=8))
    th = math.radians(215); tip = x[I] + 3.7 * np.array([math.cos(th), math.sin(th)]); tg = np.array([math.sin(th), -math.cos(th)])
    nr = np.array([-tg[1], tg[0]])
    ax.add_patch(Polygon([tip + tg * 0.75, tip + nr * 0.38, tip - nr * 0.38], closed=True, color=ORANGE, zorder=8))
    if labeled:
        fs = 8.5
        ax.text(xi - 0.9, yi + 1.7, r'$i$', color='white', fontsize=fs + 1.5, ha='center', va='center', zorder=9)
        ax.text(x[J][0] + 0.9, x[J][1] - 0.6, r'$j$', color='white', fontsize=fs + 1.5, ha='center', va='center', zorder=9)
        ax.text(*(cp + n * 1.3 + t * 0.62), r'$F_{n,ij}$', color=TEAL_T, fontsize=fs, ha='center', va='center', zorder=9)
        ax.text(*(cp + t * 2.45 + n * 0.25), r'$F_{t,ij}$', color=GREEN, fontsize=fs, ha='left', va='bottom', zorder=9, path_effects=HALO)
        ax.text(gx + 0.28, yi - 1.95, r'$m_i g$', color=NAVY_T, fontsize=fs, ha='left', va='center', zorder=9)
        ax.text(*(x[I] + 4.1 * np.array([math.cos(math.radians(170)), math.sin(math.radians(170))])), r'$M_{r,ij}$', color=ORANGE, fontsize=fs,
                ha='right', va='center', zorder=9, path_effects=HALO)
    return n, t

def panel_b(ax, n, labeled=True):
    R = 1.0; dl = 0.28
    ax.set_aspect('equal'); ax.axis('off')
    ci = np.zeros(2); cj = ci - n * (2 * R - dl)
    for c, lab in ((ci, 'i'), (cj, 'j')):
        ax.add_patch(Circle(c, R, facecolor='#E6E6E6', edgecolor=INK, lw=1.0, zorder=2))
    # 겹침 렌즈
    th = np.linspace(0, 2 * np.pi, 400)
    pi_ = ci + R * np.c_[np.cos(th), np.sin(th)]; ins = np.linalg.norm(pi_ - cj, axis=1) <= R
    pj_ = cj + R * np.c_[np.cos(th), np.sin(th)]; ins2 = np.linalg.norm(pj_ - ci, axis=1) <= R
    lens = np.r_[pi_[ins], pj_[ins2]]
    ang = np.arctan2(*(lens - (ci + cj) / 2).T[::-1]); lens = lens[np.argsort(ang)]
    ax.add_patch(Polygon(lens, closed=True, facecolor=CHAIN_C, alpha=0.55, edgecolor='none', zorder=3))
    cpt = (ci + cj) / 2; t = np.array([n[1], -n[0]])
    ax.plot([cj[0], ci[0]], [cj[1], ci[1]], color=INK2, lw=0.6, ls=(0, (3, 2)), zorder=4)
    spring(ax, cj + n * 0.25, ci - n * 0.25, n=5, amp=0.07, color='#1F3A5F', lw=1.1)
    # 접선 스프링 + 미끄럼 요소 (원 밖 · 접선 방향)
    e = t; qq = n
    a0 = cpt + e * 0.20; a1 = cpt + e * 0.56; a2 = cpt + e * 0.98; b0 = cpt + e * 1.02; b1 = cpt + e * 1.24
    ax.plot(*np.c_[a0, a1], color=GREEN, lw=1.0, zorder=9)
    spring(ax, a1, a2, n=3, amp=0.06, color=GREEN, lw=1.0)
    ax.add_patch(Polygon([b0 + qq * 0.0, b1 + qq * 0.0, b1 + qq * 0.13, b0 + qq * 0.13], closed=True, facecolor='white', edgecolor=GREEN, lw=1.0, zorder=9))
    ax.plot(*np.c_[b0 - e * 0.10 - qq * 0.015, b1 + e * 0.14 - qq * 0.015], color=GREEN, lw=1.2, zorder=9)
    for k in range(5):
        h0 = b0 - e * 0.08 + e * 0.09 * k - qq * 0.015
        ax.plot(*np.c_[h0, h0 - e * 0.05 - qq * 0.06], color=GREEN, lw=0.6, zorder=9)
    arrow(ax, cpt, cpt + n * 0.55, TEAL, lw=1.2, ms=6)
    if labeled:
        fs = 7.5
        ax.text(*(ci + n * 0.35 + t * -0.25), r'$i$', fontsize=9, ha='center', va='center', color=INK, zorder=9)
        ax.text(*(cj - n * 0.35 + t * 0.25), r'$j$', fontsize=9, ha='center', va='center', color=INK, zorder=9)
        ax.text(*(cpt - t * 0.42 - n * 0.05), r'$\delta$', fontsize=fs + 1, ha='center', va='center', color=CHAIN_C, zorder=9)
        ax.text(*(cpt + n * 0.62 + t * 0.20), r'$\mathbf{n}_{ij}$', fontsize=fs, ha='center', va='center', color=TEAL, zorder=9, path_effects=HALO)
        ax.text(*((cj + ci) / 2 - t * 0.0 + n * -0.55 + t * -0.32), r'$k_1,\ k_2$', fontsize=fs, ha='center', va='center', color='#1F3A5F', zorder=9)
        ax.text(*(cpt + t * 0.80 - n * 0.24), r'$k_t$', fontsize=fs, ha='center', va='center', color=GREEN, zorder=9)
        ax.text(*(cpt + t * 1.13 + n * 0.30), r'$\mu$', fontsize=fs + 0.5, ha='center', va='center', color=GREEN, zorder=9)
    xs = [ci[0] - 1.15, ci[0] + 1.15, cj[0] - 1.15, cj[0] + 1.15, (cpt + t * 1.45)[0]]
    ys = [ci[1] - 1.15, ci[1] + 1.15, cj[1] - 1.15, cj[1] + 1.15, (cpt + t * 1.45)[1]]
    ax.set_xlim(min(xs), max(xs)); ax.set_ylim(min(ys), max(ys))

def panel_c(ax, labeled=True):
    k1, k2, dm = 1.0, 2.5, 1.0; d0 = (1 - k1 / k2) * dm
    ax.plot([0, dm], [0, k1 * dm], color='#1F3A5F', lw=1.3)
    ax.plot([dm, d0], [k1 * dm, 0], color='#1F3A5F', lw=1.3, ls=(0, (4, 2)))
    arrow(ax, (0.30, 0.30), (0.52, 0.52), '#1F3A5F', lw=0.9, ms=5)
    arrow(ax, (0.93, 0.83), (0.80, 0.50), '#1F3A5F', lw=0.9, ms=5)
    ax.set_xlim(0, 1.15); ax.set_ylim(0, 1.15)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.set_xticks([d0, dm]); ax.set_yticks([])
    ax.set_xticklabels([r'$\delta_0$', r'$\delta_{max}$'] if labeled else ['', ''], fontsize=7)
    ax.tick_params(length=2, width=0.6)
    for s in ('left', 'bottom'): ax.spines[s].set_linewidth(0.7)
    if labeled:
        ax.text(1.17, 0.0, r'$\delta$', fontsize=8, ha='left', va='center', clip_on=False); ax.text(0.0, 1.18, r'$F_n$', fontsize=8, ha='center', va='bottom', clip_on=False)
        ax.text(0.22, 0.42, r'$k_1$', fontsize=7.5, color='#1F3A5F'); ax.text(0.86, 0.38, r'$k_2$', fontsize=7.5, color='#1F3A5F')

def panel_d(ax, labeled=True):
    ax.plot([0, 0.5], [0, 0.8], color=GREEN, lw=1.3); ax.plot([0.5, 1.05], [0.8, 0.8], color=GREEN, lw=1.3)
    ax.axhline(0.8, xmin=0, xmax=1, color=INK2, lw=0.5, ls=(0, (2, 2)))
    ax.set_xlim(0, 1.15); ax.set_ylim(0, 1.15)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([0.8]); ax.set_yticklabels([r'$\mu F_n$'] if labeled else [''], fontsize=7)
    ax.tick_params(length=2, width=0.6)
    for s in ('left', 'bottom'): ax.spines[s].set_linewidth(0.7)
    if labeled:
        ax.text(1.17, 0.0, r'$\delta_t$', fontsize=8, ha='left', va='center', clip_on=False); ax.text(0.0, 1.18, r'$|F_t|$', fontsize=8, ha='center', va='bottom', clip_on=False)
        ax.text(0.78, 0.86, '미끄럼', fontsize=6.5, color=INK2, ha='center', va='bottom')
        ax.text(0.12, 0.42, r'$k_t$', fontsize=7.5, color=GREEN)

def combined(out, labeled):
    plt = _mpl()
    fig = plt.figure(figsize=(4.50, 2.75), dpi=300)
    axa = fig.add_axes([0.0, 0.30, 0.52, 0.70]); n, t = panel_a(axa, labeled)
    axb = fig.add_axes([0.55, 0.36, 0.43, 0.60]); panel_b(axb, n, labeled)
    axc = fig.add_axes([0.10, 0.06, 0.32, 0.22]); panel_c(axc, labeled)
    axd = fig.add_axes([0.62, 0.06, 0.32, 0.22]); panel_d(axd, labeled)
    fig.savefig(out + '.png', dpi=300, transparent=True); fig.savefig(out + '.svg', transparent=True); plt.close(fig)



def pick_pair(snaps, meta):
    """가압 상태에서 판에 닿은 활물질 i 와 아래 오른쪽 활물질 이웃 j (법선력 가장 큰 쌍)."""
    sn = snaps['compress']; r = np.array(meta['r']); am = np.array(meta['am']); x = np.array(sn['x']); py = sn['plate_y']
    best = None
    for i, j, fn, ft in sn['contacts']:
        for a, b in ((i, j), (j, i)):
            if not (am[a] and am[b]): continue
            if x[a, 1] + r[a] < py - 2.0 or not (12 < x[a, 0] < 36): continue
            d = x[b] - x[a]; ang = math.degrees(math.atan2(d[1], d[0]))
            if -80 <= ang <= -15 and (best is None or fn > best[2]): best = (a, b, fn, ang)
    if best is None: raise SystemExit('접촉 쌍 없음')
    return best


def render_all(state):
    snaps, meta = state['snaps'], state['meta']
    CTX.update(snaps=snaps, r=np.array(meta['r']), am=np.array(meta['am']))
    I, J, FN, ANG = pick_pair(snaps, meta)
    sn = snaps['compress']
    CTX.update(x=np.array(sn['x']), py=sn['plate_y'], C=sn['contacts'], fmax=max(c[2] for c in sn['contacts']), I=I, J=J)
    os.makedirs(OUT, exist_ok=True)
    for lab in (True, False):
        process(os.path.join(OUT, 'p0_process_' + ('labeled' if lab else 'nolabel')), lab)
        process_grid(os.path.join(OUT, 'p0_process_grid_' + ('labeled' if lab else 'nolabel')), lab)
        combined(os.path.join(OUT, 'p0_contact_model_' + ('labeled' if lab else 'nolabel')), lab)
    return dict(pair=[int(I), int(J)], pair_fn=FN, pair_angle_deg=ANG)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


FIGS = ['p0_process_labeled', 'p0_process_nolabel', 'p0_process_grid_labeled', 'p0_process_grid_nolabel',
        'p0_contact_model_labeled', 'p0_contact_model_nolabel']


def check(state):
    """저장 상태 · 그림 검사 (모식 계산은 다시 안 돌림)."""
    snaps, meta = state['snaps'], state['meta']; prob = []
    r = np.array(meta['r']); am = np.array(meta['am'])
    if (int(am.sum()), int((~am).sum())) != (N_AM, N_SE): prob.append('입자 수')
    x0 = np.array(snaps['insert']['x']); d = np.sqrt(((x0[:, None] - x0[None]) ** 2).sum(-1)) + np.eye(len(r)) * 1e9
    if (d - r[:, None] - r[None, :]).min() < -1e-9: prob.append('삽입 겹침')
    if not (snaps['insert']['x'] and max(p[1] + rr for p, rr in zip(x0.tolist(), r)) <= INS_Y1 + 1e-9): prob.append('삽입 영역')
    if not (snaps['compress']['f_stop'] / W >= meta['f_target']): prob.append('가압 목표 미도달 (정지 판정 힘 = 판 이동 중 값)')
    if not (meta['plate_stop'] < meta['h_after_stab']): prob.append('판이 내려가지 않음')
    if not (meta['f_relax'] < meta['f_stop']): prob.append('판 정지 뒤 판 힘 하락 아님 (그림 4 단계 설명과 어긋남)')
    if snaps['relax']['plate_y'] != snaps['compress']['plate_y']: prob.append('이완 중 판 높이 바뀜')
    for f in FIGS:
        for ext in ('.png', '.svg'):
            if not os.path.isfile(os.path.join(OUT, f + ext)): prob.append('없음 ' + f + ext)
    return prob


def main():
    ap = argparse.ArgumentParser(description='50kg 보고 0쪽 그림 (2D 모식 계산 · 그림용)')
    ap.add_argument('--sim', action='store_true', help='모식 계산을 다시 돌려 상태 JSON 을 덮어쓴다 (씨앗 23)')
    ap.add_argument('--scan', action='store_true', help='씨앗 11 13 17 23 의 판 힘 (정지 · 이완 끝) 만 출력')
    ap.add_argument('--check', action='store_true', help='저장 상태 · 그림 검사만')
    a = ap.parse_args()
    if a.scan:
        for sd in (11, 13, 17, 23):
            _, m = run(seed=sd, f_target=F_TARGET, verbose=False)
            print(json.dumps(dict(seed=sd, f_stop=round(m['f_stop'], 3), f_relax=round(m['f_relax'], 3),
                                  drop=bool(m['f_relax'] < m['f_stop']))))
        return 0
    if a.sim:
        snaps, meta = run(seed=SEED, f_target=F_TARGET, verbose=True)
        os.makedirs(OUT, exist_ok=True)
        json.dump(dict(snaps=snaps, meta=meta), open(STATE, 'w'), separators=(',', ':'))
    state = json.load(open(STATE))
    if a.check:
        prob = check(state)
        print('검사:', '문제 없음 → PASS' if not prob else 'FAIL ' + '; '.join(prob))
        return 1 if prob else 0
    info = render_all(state)
    meta = state['meta']
    out = dict(seed=SEED, f_target_per_width=F_TARGET, f_stop_criterion=state['snaps']['compress']['f_stop'],
               f_plate_at_stop=meta['f_stop'], f_plate_relax_end=meta['f_relax'], h_settle_top=meta['h_settle_top'],
               h_after_stab=meta['h_after_stab'], plate_stop=meta['plate_stop'], n_am=N_AM, n_se=N_SE, width=W, insert_height=INS_Y1 - INS_Y0,
               k_am=K_AM, k_se=K_SE, mu=MU, state_sha256=sha(STATE), **info,
               files={f + ext: sha(os.path.join(OUT, f + ext)) for f in FIGS for ext in ('.png', '.svg')},
               note='2D 모식 계산 (그림용) — 힘 · 길이 · 시간 = 임의 단위 · 실제 3D 덱 결과 아님')
    json.dump(out, open(os.path.join(OUT, 'p0_figs_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    prob = check(state)
    print('그림 6 × (PNG · SVG) · 검사:', '문제 없음 → PASS' if not prob else 'FAIL ' + '; '.join(prob))
    return 1 if prob else 0


if __name__ == '__main__':
    sys.exit(main())
