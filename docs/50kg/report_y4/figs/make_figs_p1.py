#!/usr/bin/env python3
"""50kg 4차년도 DEM 보고 1쪽 그림 둘 — 같은 배율 x–z 단면 넷 · 크기비 축 (png · svg · csv · meta json).

    python3 -P docs/50kg/report_y4/figs/make_figs_p1.py [--out docs/50kg/report_y4/figs]

- 값은 전부 `kg50_y4_sources.load_all()` 이 빌드 때 덱 · manifest · 끝 상태 묶음에서 읽은 것 (손으로 적은 숫자 없음).
- 단면 = 끝 상태 (판 고정 이완 끝) atom 덤프 · y = 상자 가운데 평면 · 구와 평면의 교차 원 (x 주기 상 = 이웃 상까지 그림) ·
  벽 (z = 0) · 판 (끝 mesh z) 에서 자른다 · SE = 주황 · AM = 회색 · 기공 = 흰색.  네 칸 = 같은 배율 (x 0–50 µm · z 0–Z_MAX µm · 칸 폭 같음).
  자료가 없는 침대 (D1 · D0.7) = 빈 칸 (점선 틀) — 상태 글은 덱 생성기가 칸 위에 얹는다 (그림 안 글 = 영어만 · 보고 원칙 §4).
- 크기비 축 = SE D50 (로그) · 위 눈금 = D_AM/D_SE · 점선 = 세 AM 이 맞닿은 평면 목의 내접원 지름 (2/√3 − 1)·D_AM (이상화 기준선 ·
  실제 침대 문턱 아님 — 덱의 캡션이 말한다) · 왼쪽 작은 그림 = 그 목의 모식도.
- 범례 · 설명 글 = 그림 밖 (덱의 편집 가능한 글 · 보고 원칙 §2).  그림 글꼴 = Aptos (없으면 Carlito → DejaVu Sans) · SVG 는 글자 그대로.
- 결정적 출력: PNG 메타 없음 · SVG 날짜 없음 · hashsalt 고정 (같은 환경 · 같은 글꼴에서 같은 바이트).
"""
import argparse
import csv
import hashlib
import json
import logging
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.collections import PatchCollection  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import kg50_y4_sources as src  # noqa: E402

SE_COLOR, AM_COLOR, WALL_COLOR, PH_COLOR = '#D2642A', '#9A9A9A', '#000000', '#B0B0B0'
WALL_LW = 1.6                         # 판 · 바닥 벽 선 (틀 선 0.8 보다 굵게)
DPI = 300
Z_MAX_UM = 130.0                      # 단면 z 범위 (네 칸 같음) — 끝 판 높이가 이보다 높으면 멈춘다
TICK_PT, LABEL_PT, TITLE_PT = 7, 8, 8
#: 단면 그림 배치 (in) — 덱에 100 % 로 놓는다 (덱 생성기가 크기 대조)
SEC_W, SEC_H = 4.40, 2.95
SEC_LEFT, SEC_RIGHT, SEC_TOP, SEC_BOTTOM = 0.42, 0.04, 0.22, 0.36
RAT_W, RAT_H = 4.40, 0.86
FONT_CANDIDATES = {'Aptos': (), 'Carlito': ('/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf',),
                   'DejaVu Sans': ()}


def setup_fonts():
    """Aptos 우선 · 없으면 Carlito (Calibri 폭) · DejaVu Sans.  matplotlib 글꼴 캐시가 Carlito 를 모르면 파일을 메모리에만 더한다."""
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
    known = {f.name for f in fm.fontManager.ttflist}
    for name, paths in FONT_CANDIDATES.items():
        if name not in known:
            for p in paths:
                if Path(p).exists():
                    fm.fontManager.addfont(p)
    known = {f.name for f in fm.fontManager.ttflist}
    used = next(n for n in FONT_CANDIDATES if n in known)
    plt.rcParams.update({
        'font.family': list(FONT_CANDIDATES), 'font.size': TICK_PT, 'axes.linewidth': 0.8,
        'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
        'xtick.major.width': 0.7, 'ytick.major.width': 0.7, 'xtick.labelsize': TICK_PT, 'ytick.labelsize': TICK_PT,
        'axes.labelsize': LABEL_PT, 'svg.fonttype': 'none', 'svg.hashsalt': 'kg50-report-y4-draft1',
        'axes.unicode_minus': False, 'path.simplify': False,
        'mathtext.fontset': 'custom', 'mathtext.rm': used, 'mathtext.it': f'{used}:italic', 'mathtext.bf': f'{used}:bold',
    })
    return used


def save(fig, out, stem):
    png, svg = out / f'{stem}.png', out / f'{stem}.svg'
    fig.savefig(png, dpi=DPI, metadata={'Software': None})
    fig.savefig(svg, metadata={'Date': None, 'Creator': None})
    plt.close(fig)
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (png, svg)}


def section_circles(atoms, y0_sim, Lx_sim, Ly_sim):
    """구 · 평면 y = y0 의 교차 원 (최소 상 거리) — x 주기 상은 상자를 넘는 원만 ±Lx 로 하나 더."""
    dy = atoms['y'] - y0_sim
    dy -= Ly_sim * np.round(dy / Ly_sim)
    hit = np.abs(dy) < atoms['r']
    rho = np.sqrt(np.clip(atoms['r'][hit] ** 2 - dy[hit] ** 2, 0.0, None))
    rows = []
    for pid, ty, x, z, rr in zip(atoms['id'][hit], atoms['type'][hit], atoms['x'][hit], atoms['z'][hit], rho):
        rows.append((int(pid), int(ty), x, z, rr, 0.0))
        if x - rr < 0:
            rows.append((int(pid), int(ty), x + Lx_sim, z, rr, Lx_sim))
        if x + rr > Lx_sim:
            rows.append((int(pid), int(ty), x - Lx_sim, z, rr, -Lx_sim))
    return rows


def make_sections(beds, common, out):
    n = len(beds)
    Lx, Ly = common['box_x_um'], common['box_y_um']
    ax_h = SEC_H - SEC_TOP - SEC_BOTTOM
    ax_w = ax_h * Lx / Z_MAX_UM
    gap = (SEC_W - SEC_LEFT - SEC_RIGHT - n * ax_w) / (n - 1)
    src.need(gap > 0.05, f'단면 칸 사이 간격 {gap:.3f} in — 너무 좁다')
    fig = plt.figure(figsize=(SEC_W, SEC_H))
    y0_um = Ly / 2
    meta_axes, csv_rows, panels = {}, [], []
    for k, b in enumerate(beds):
        left = SEC_LEFT + k * (ax_w + gap)
        ax = fig.add_axes([left / SEC_W, SEC_BOTTOM / SEC_H, ax_w / SEC_W, ax_h / SEC_H])
        ax.set_xlim(0, Lx)
        ax.set_ylim(0, Z_MAX_UM)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks([0, Lx / 2, Lx])
        ax.set_yticks([0, 40, 80, 120])
        if k:                                      # 같은 축 · 같은 배율 — 눈금 글은 첫 칸에만 (칸 사이 글 겹침 없음)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        else:
            ax.set_xticklabels([src.fmt_g(v) for v in (0, Lx / 2, Lx)])
            ax.set_xlabel('x (µm)', labelpad=1)
            ax.set_ylabel('z (µm)', labelpad=2)
        label = src.bed_label(b)
        ax.set_title(f'SE {src.fmt_g(b["deck_vals"]["d50_se_um"])} µm', fontsize=TITLE_PT, pad=3)
        es = b['endstate']
        box_in = [round(left, 4), round(SEC_TOP, 4), round(ax_w, 4), round(ax_h, 4)]     # (left, top, w, h) in · 그림 왼쪽 위 기준
        if es is None:
            for s in ax.spines.values():
                s.set_linestyle((0, (3, 2)))
                s.set_edgecolor(PH_COLOR)
            ax.tick_params(colors='#000000')
            meta_axes[label] = dict(box_in=box_in, status=b['status'], data=False)
            panels.append(dict(label=label, data=False))
            continue
        a = es['atoms']
        plate = es['plate_z_um']
        src.need(plate <= Z_MAX_UM, f'{label}: 판 높이 {plate} > Z_MAX {Z_MAX_UM}')
        rows = section_circles(a, y0_um / src.LEN_SIM_TO_UM, Lx / src.LEN_SIM_TO_UM, Ly / src.LEN_SIM_TO_UM)
        clip = Rectangle((0, 0), Lx, plate, transform=ax.transData)
        for ty, color in ((src.TYPE_AM, AM_COLOR), (src.TYPE_SE, SE_COLOR)):
            circ = [Circle((x * src.LEN_SIM_TO_UM, z * src.LEN_SIM_TO_UM), rr * src.LEN_SIM_TO_UM) for _, t, x, z, rr, _ in rows if t == ty]
            pc = PatchCollection(circ, facecolor=color, edgecolor='none', linewidth=0)
            pc.set_clip_path(clip)
            ax.add_collection(pc)
        ax.plot([0, Lx], [plate, plate], color=WALL_COLOR, lw=WALL_LW, solid_capstyle='butt')
        ax.plot([0, Lx], [0, 0], color=WALL_COLOR, lw=WALL_LW, solid_capstyle='butt', clip_on=False)
        n_am_sec = len({r[0] for r in rows if r[1] == src.TYPE_AM})
        n_se_sec = len({r[0] for r in rows if r[1] == src.TYPE_SE})
        # 벽 · 판 겹침 (끝 덤프 · 단면 그림이 벽 · 판 선에서 자르는 몫) — 상별 최대 (µm)
        zr, rr_um = a['z'] * src.LEN_SIM_TO_UM, a['r'] * src.LEN_SIM_TO_UM
        wall_pen = {ph: dict(bottom_max_um=round(float(np.max(rr_um[m_] - zr[m_])), 4), top_max_um=round(float(np.max(zr[m_] + rr_um[m_] - plate)), 4))
                    for ph, m_ in (('AM', a['type'] == src.TYPE_AM), ('SE', a['type'] == src.TYPE_SE))}
        for pid, t, x, z, rr, sh in rows:
            csv_rows.append([label, src.fmt_g(b['deck_vals']['d50_se_um']), 'AM' if t == src.TYPE_AM else 'SE', pid,
                             f'{x * src.LEN_SIM_TO_UM:.6f}', f'{z * src.LEN_SIM_TO_UM:.6f}', f'{rr * src.LEN_SIM_TO_UM:.6f}',
                             f'{sh * src.LEN_SIM_TO_UM:.1f}'])
        meta_axes[label] = dict(box_in=box_in, status=None, data=True, step=es['step'], plate_z_um=round(plate, 6),
                                n_am=es['n_am'], n_se=es['n_se'], n_am_in_section=n_am_sec, n_se_in_section=n_se_sec,
                                wall_overlap=wall_pen, tgz=es['tgz'], tgz_sha256=es['tgz_sha256'], members=es['members'])
        panels.append(dict(label=label, data=True))
    fig.canvas.draw()
    for ax, (label, m) in zip(fig.axes, meta_axes.items()):     # 실제 칸 자리 (그린 뒤) — 덱의 상태 글 자리 · 같은 배율 검사
        p = ax.get_position()
        m['box_in'] = [round(p.x0 * SEC_W, 4), round((1 - p.y1) * SEC_H, 4), round(p.width * SEC_W, 4), round(p.height * SEC_H, 4)]
    shas = save(fig, out, 'p1_sections')
    with open(out / 'p1_sections.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['bed', 'se_d50_um', 'phase', 'particle_id', 'x_um', 'z_um', 'section_radius_um', 'periodic_shift_um'])
        w.writerows(csv_rows)
    return dict(size_in=[SEC_W, SEC_H], dpi=DPI, axes=meta_axes, y0_um=y0_um, x_range_um=[0, Lx], z_range_um=[0, Z_MAX_UM],
                um_per_in=round(Lx / ax_w, 6), colors=dict(SE=SE_COLOR, AM=AM_COLOR, wall=WALL_COLOR, placeholder_frame=PH_COLOR),
                files=shas, csv_rows=len(csv_rows))


def make_size_ratio(beds, common, out):
    d_am = common['d_am_um']
    t = common['throat_um']
    fig = plt.figure(figsize=(RAT_W, RAT_H))
    # 왼쪽 모식도 — 세 AM (반지름 1) 이 맞닿은 평면 · 가운데 = 내접원 (반지름 2/√3 − 1)
    s = RAT_H - 0.06
    axs = fig.add_axes([0.02 / RAT_W, 0.03 / RAT_H, s / RAT_W, s / RAT_H])
    axs.set_aspect('equal')
    axs.axis('off')
    R = 1.0
    cs = [(0.0, 2 / math.sqrt(3)), (-1.0, -1 / math.sqrt(3)), (1.0, -1 / math.sqrt(3))]
    for cx, cy in cs:
        axs.add_patch(Circle((cx, cy), R, facecolor=AM_COLOR, edgecolor='none'))
    axs.add_patch(Circle((0, 0), R * src.throat_factor(), facecolor='white', edgecolor=SE_COLOR, lw=0.9, linestyle=(0, (2, 1.2))))
    axs.set_xlim(-2.05, 2.05)
    axs.set_ylim(-1.62, 2.2)
    # 오른쪽 축
    x0, x1 = 1.12, RAT_W - 0.10
    yb, yt = 0.30, RAT_H - 0.30
    ax = fig.add_axes([x0 / RAT_W, yb / RAT_H, (x1 - x0) / RAT_W, (yt - yb) / RAT_H])
    ax.set_xscale('log')
    ax.set_xlim(0.5, 4.2)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    d50 = [b['deck_vals']['d50_se_um'] for b in beds]
    ratios = [d_am / v for v in d50]
    ax.set_xticks(d50)
    ax.set_xticklabels([src.fmt_g(v) for v in d50])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xlabel('SE D50 (µm)', labelpad=1)
    top = ax.secondary_xaxis('top')
    top.set_xticks(d50)
    top.set_xticklabels([src.fmt_g(r, 2) for r in ratios])
    top.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    top.set_xlabel(r'$D_\mathrm{AM}\,/\,D_\mathrm{SE}$', labelpad=2)
    top.tick_params(direction='in', length=2.5, width=0.7)
    ax.axvline(t, color=SE_COLOR, lw=0.9, linestyle=(0, (3, 2)))
    ax.scatter(d50, [0.5] * len(d50), s=16, color=SE_COLOR, zorder=3, linewidths=0)
    shas = save(fig, out, 'p1_size_ratio')
    with open(out / 'p1_size_ratio.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['bed', 'se_d50_um', 'am_d_um', 'd_am_over_d_se', 'idealized_throat_um', 'se_d50_below_throat'])
        for b, v, r in zip(beds, d50, ratios):
            w.writerow([src.bed_label(b), src.fmt_g(v), src.fmt_g(d_am), f'{r:.6f}', f'{t:.6f}', v < t])
    return dict(size_in=[RAT_W, RAT_H], dpi=DPI, d50_um=d50, ratios=[round(r, 6) for r in ratios], throat_um=round(t, 6),
                throat_factor=round(src.throat_factor(), 9), files=shas,
                axis_box_in=[x0, RAT_H - yt, x1 - x0, yt - yb], schematic_box_in=[0.02, 0.03, s, s])


def build_all(out=HERE):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    font = setup_fonts()
    beds, common = src.load_all()
    sec = make_sections(beds, common, out)
    rat = make_size_ratio(beds, common, out)
    meta = dict(generator='docs/50kg/report_y4/figs/make_figs_p1.py', matplotlib=matplotlib.__version__, png_font=font,
                svg_font_family=list(FONT_CANDIDATES), decks={src.bed_label(b): dict(path=b['deck'], sha256=b['sha256']) for b in beds},
                sections=sec, size_ratio=rat)
    (out / 'p1_figs_meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE))
    a = ap.parse_args()
    meta = build_all(a.out)
    print('p1 figures:', {k: v['files'] for k, v in (('sections', meta['sections']), ('size_ratio', meta['size_ratio']))})
    print('png font:', meta['png_font'], '· section rows:', meta['sections']['csv_rows'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
