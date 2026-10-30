#!/usr/bin/env python3
"""50kg 4차년도 DEM 보고 초안 2 — 그림 (PNG 300 dpi · SVG 글자 그대로 · 그린 값 CSV) — 러너 출력 (data/<침대>/) 만 읽는다.

    python3 -P docs/50kg/report_y4/draft2/make_draft2_figs.py

- 침대 넷 자리 (0.7 · 1 · 2 · 3 µm) 를 모든 비교 그림에 둔다 — 결과가 없는 침대 = 빗금 빈 칸 + "결과 대기" (D1 이 오면 같은 명령으로 채워진다).
- 값 = `data/<침대>/metrics_<침대>.json` · `per_am_*.csv` · `zprof_*.csv` · `curve_*.csv` · `section_*.csv` (run_draft2_metrics.py 출력 · 웹앱
  망 정지 파이프라인 · 기존 함수) + 1쪽 덱 값 (kg50_y4_sources.load_all — 덱 · manifest 대조).  그림에서 새로 계산하는 값 = 정규화 (p7 = D3 대비 비) ·
  상자 그림 통계 (5 · 25 · 50 · 75 · 95 백분위) 뿐.
- 크기 = 양식 반쪽 칸 (README 표) · 100 % 로 붙인다 (모든 그림 같은 글자 크기 — 눈금 7 pt · 축 제목 8 pt).  범례 · 설명 = 축 밖 (그림 위 한 줄) ·
  캡션 · 한정어 = README (슬라이드 글로 따로 쓴다).  글꼴 = Aptos → (없으면) Carlito · 한글 = 맑은 고딕 → (없으면) WenQuanYi Zen Hei.
- 색: AM (NCM) #1A1A1A · SE #CDB650 (50kg 계획 덱) · 입도 = 한 색상 (파랑) 밝음 → 어두움 (0.7 → 3 µm · dataviz 서열 검사 통과) ·
  Physics (민감도) = 속 빈 표지.
- 결정적 출력: PNG 메타 Software 없음 (dpi 300 기록) · SVG 날짜 없음 · hashsalt 고정.
"""
from __future__ import annotations

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
REPO = HERE.parents[3]
for p in (HERE, HERE.parent, HERE.parent / 'figs', REPO / 'scripts'):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import kg50_y4_sources as src  # noqa: E402
import run_draft2_metrics as R  # noqa: E402

OUT = HERE / 'figs'
DPI = 300
TICK_PT, LABEL_PT, TITLE_PT, VAL_PT, NOTE_PT = 7, 8, 8, 6.5, 6
AM_C, SE_C = '#1A1A1A', '#CDB650'
SIZE_C = {'D0.7': '#86b6ef', 'D1': '#3987e5', 'D2': '#1c5cab', 'D3': '#0d366b'}
INK, INK2, GRID, PH = '#262626', '#595959', '#D9D9D9', '#A6A6A6'
WALL_C = '#7F7F7F'
WAIT = '결과 대기'
FONTS = ['Aptos', 'Malgun Gothic', 'Carlito', 'WenQuanYi Zen Hei', 'DejaVu Sans']
W_HALF = 4.50          # 양식 반쪽 칸 폭 (in) — 패널 안 폭 4.63 in 에서 여백
SEEDNOTE = '입도별 시드 1 (오차 막대 없음)'


def setup_fonts():
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
    known = {f.name for f in fm.fontManager.ttflist}
    latin = next((n for n in ('Aptos', 'Carlito', 'DejaVu Sans') if n in known), 'DejaVu Sans')
    plt.rcParams.update({
        'font.family': FONTS, 'font.size': TICK_PT, 'axes.linewidth': 0.8, 'axes.edgecolor': INK,
        'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
        'xtick.major.width': 0.7, 'ytick.major.width': 0.7, 'xtick.labelsize': TICK_PT, 'ytick.labelsize': TICK_PT,
        'xtick.color': INK, 'ytick.color': INK, 'axes.labelcolor': INK, 'text.color': INK,
        'axes.labelsize': LABEL_PT, 'axes.titlesize': TITLE_PT, 'svg.fonttype': 'none', 'svg.hashsalt': 'kg50-report-y4-draft2',
        'axes.unicode_minus': False, 'path.simplify': False, 'hatch.linewidth': 0.5,
        'axes.spines.top': False, 'axes.spines.right': False,
        'mathtext.fontset': 'custom', 'mathtext.rm': latin, 'mathtext.it': f'{latin}:italic', 'mathtext.bf': f'{latin}:bold',
    })
    return latin


# ───────────────────────────── 자료 ─────────────────────────────

def read_csv(p):
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def fnum(x):
    return None if x in (None, '') else float(x)


def load():
    beds = R.load_beds()
    decks = {src.bed_label(b): b for b in src.load_all(with_end=False)[0]}
    data = {}
    for bed in R.BED_ORDER:
        if bed not in beds:
            continue
        d = R.DATA / bed
        data[bed] = dict(rec=beds[bed], m=beds[bed]['metrics'], per_am=read_csv(d / f'per_am_{bed}.csv'),
                         zprof=read_csv(d / f'zprof_{bed}.csv'), section=read_csv(d / f'section_{bed}.csv'),
                         curve=read_csv(d / f'curve_{bed}.csv') if (d / f'curve_{bed}.csv').exists() else None)
    return data, decks


# ───────────────────────────── 공통 그리기 ─────────────────────────────

def fmt_v(v, sig=3):
    """값 글 = 유효숫자 sig 자리 (끝 0 유지 — 18.96 → "19.0" · 정수 자리가 넘치면 정수) · 0 은 "0"."""
    if v is None or (isinstance(v, float) and not math.isfinite(v)):
        return '—'
    if v == 0:
        return '0'
    d = max(0, sig - 1 - int(math.floor(math.log10(abs(v)))))
    return f'{v:.{d}f}'


def fmt_tick(v):
    """눈금 = 끝 0 없음 ("0.0" → "0" · 보고 원칙 §2)."""
    if v == 0:
        return '0'
    s = f'{v:.6f}'.rstrip('0').rstrip('.')
    return s


#: mathtext 이름 (아래첨자) — 글꼴 = Aptos/Carlito (mathtext.rm)
EPS = r'$\varepsilon_\mathrm{sphere}$'
SIG_EFF = r'$\sigma_\mathrm{eff}$'
TAU_TR = r'$\varphi_\mathrm{SE}\,\sigma_0/\sigma_\mathrm{eff}$'
F_ION = r'$f = \sigma_\mathrm{eff}/\sigma_0$'
SVM = r'$\sigma_\mathrm{VM}$'
RATIO = r'$D_\mathrm{AM}/D_\mathrm{SE}$'


def frame(fig, w, h, n, left=0.46, right=0.08, gap=0.46, bottom=0.42, top=0.34):
    """n 개 패널 가로 배치 → axes 목록 (in 단위 여백)."""
    aw = (w - left - right - (n - 1) * gap) / n
    ah = h - bottom - top
    return [fig.add_axes([(left + k * (aw + gap)) / w, bottom / h, aw / w, ah / h]) for k in range(n)]


def size_axis(ax, label=True):
    ax.set_xlim(-0.6, len(R.BED_ORDER) - 0.4)
    ax.set_xticks(range(len(R.BED_ORDER)))
    ax.set_xticklabels([b[1:] for b in R.BED_ORDER])
    ax.tick_params(axis='x', length=0)
    if label:
        ax.set_xlabel('SE D50 (µm)', labelpad=2)


def ygrid(ax):
    ax.yaxis.grid(True, color=GRID, lw=0.5)
    ax.set_axisbelow(True)


def placeholder(ax, x, width=0.62, text=WAIT, frac=0.97):
    y0, y1 = ax.get_ylim()
    ax.add_patch(Rectangle((x - width / 2, y0), width, (y1 - y0) * frac, facecolor='none', edgecolor=PH, hatch='////', lw=0.5,
                           zorder=1))
    ax.text(x, y0 + (y1 - y0) * frac * 0.5, text, rotation=90, ha='center', va='center', fontsize=VAL_PT, color=INK2, zorder=3,
            bbox=dict(boxstyle='square,pad=0.15', fc='white', ec='none'))


def bars(ax, data, key, ylim, phys_key=None, scale=1.0, sig=3, lab_dy=0.015):
    """입도 칸 막대 (Hertz · 주) + Physics 속 빈 표지 (민감도) — 값 글 = 막대 위 · Physics 값 글 = 표지 위 (표지가 막대 안이면 표지 아래 흰 글).
    반환 = CSV 행."""
    ax.set_ylim(*ylim)
    rows = []
    span = ylim[1] - ylim[0]
    for k, bed in enumerate(R.BED_ORDER):
        if bed not in data:
            placeholder(ax, k)
            rows.append(dict(bed=bed, status=WAIT))
            continue
        v = data[bed]['m'][key] * scale
        ax.bar(k, v, width=0.62, color=SIZE_C[bed], edgecolor='none', zorder=2)
        ax.text(k, v + span * lab_dy, fmt_v(v, sig), ha='center', va='bottom', fontsize=VAL_PT, color=INK, zorder=5)
        r = dict(bed=bed, status='ok', value=v)
        if phys_key:
            pv = data[bed]['m'][phys_key] * scale
            ax.plot([k], [pv], marker='o', ms=4.6, mfc='white', mec=INK, mew=0.9, ls='none', zorder=4)
            r['physics'] = pv
            if pv > v:
                ax.text(k, pv + span * 0.035, fmt_v(pv, sig), ha='center', va='bottom', fontsize=VAL_PT, color=INK2, zorder=5)
            else:
                ax.text(k, pv - span * 0.035, fmt_v(pv, sig), ha='center', va='top', fontsize=VAL_PT,
                        color='white' if bed != 'D0.7' else INK, zorder=5)
        rows.append(r)
    size_axis(ax)
    ygrid(ax)
    return rows


def top_legend(fig, items, y_in, h, x_in=0.46, w=W_HALF):
    """그림 위 한 줄 범례 (축 밖) — items = [(종류, 색, 글)] · 종류 = 'bar' | 'hollow' | 'line' | 'text'."""
    x = x_in
    sw, sh = 0.13, 0.08                       # 견본 크기 (in)
    for kind, color, text in items:
        yy = 1 - y_in / h
        if kind == 'bar':
            fig.patches.append(Rectangle((x / w, yy - sh / 2 / h), sw / w, sh / h, transform=fig.transFigure, facecolor=color, edgecolor='none'))
            x += sw + 0.04
        elif kind == 'hollow':
            fig.lines.append(matplotlib.lines.Line2D([(x + 0.06) / w], [yy], transform=fig.transFigure, marker='o', ms=4.6, mfc='white',
                                                     mec=INK, mew=0.9, ls='none'))
            x += 0.15
        elif kind == 'diamond':
            fig.lines.append(matplotlib.lines.Line2D([(x + 0.06) / w], [yy], transform=fig.transFigure, marker='D', ms=3.8, mfc='white',
                                                     mec=INK, mew=0.9, ls='none'))
            x += 0.15
        elif kind == 'line':
            fig.lines.append(matplotlib.lines.Line2D([x / w, (x + 0.20) / w], [yy, yy], transform=fig.transFigure, color=color, lw=1.4))
            x += 0.24
        elif kind == 'dotted':
            fig.lines.append(matplotlib.lines.Line2D([x / w, (x + 0.20) / w], [yy, yy], transform=fig.transFigure, color=color, lw=1.0,
                                                     ls=(0, (1.5, 1.2))))
            x += 0.24
        elif kind == 'hatch':
            fig.patches.append(Rectangle((x / w, yy - sh / 2 / h), sw / w, sh / h, transform=fig.transFigure, facecolor='none',
                                         edgecolor=PH, hatch='////', lw=0.5))
            x += sw + 0.04
        t = fig.text(x / w, yy, text, ha='left', va='center', fontsize=NOTE_PT + 0.5, color=INK2 if kind == 'text' else INK)
        fig.canvas.draw()
        bb = t.get_window_extent()
        x += bb.width / fig.dpi + 0.14


def save(fig, stem, rows, cols, meta):
    OUT.mkdir(parents=True, exist_ok=True)
    png, svg, cs = OUT / f'{stem}.png', OUT / f'{stem}.svg', OUT / f'{stem}.csv'
    fig.savefig(png, dpi=DPI, metadata={'Software': None})
    fig.savefig(svg, metadata={'Date': None, 'Creator': None})
    w, h = fig.get_size_inches()
    plt.close(fig)
    with open(cs, 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f, lineterminator='\n')
        wr.writerow(cols)
        for r in rows:
            wr.writerow(['' if r.get(c) is None else (fmt_csv(r[c])) for c in cols])
    from PIL import Image
    with Image.open(png) as im:
        dpi = im.info.get('dpi')
        px = im.size
    meta[stem] = dict(size_in=[round(float(w), 3), round(float(h), 3)], px=list(px), dpi=[round(float(v), 3) for v in dpi] if dpi else None,
                      files={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (png, svg, cs)}, csv_rows=len(rows))
    return meta[stem]


def fmt_csv(v):
    if isinstance(v, float):
        return f'{v:.9g}'
    return v


def pct(xs, q):
    return float(np.percentile(np.asarray(xs, dtype=float), q))


# ───────────────────────────── p1 — 침대 조건 띠 ─────────────────────────────

def fig_p1(data, decks, meta):
    w, h = W_HALF, 2.95
    fig = plt.figure(figsize=(w, h))
    z_max = 130.0
    for bed in data:
        pz = data[bed]['m']['plate_z_um']
        z_max = max(z_max, math.ceil(pz / 10.0) * 10.0)
    lx = 50.0
    top, lab_h, left = 0.08, 0.80, 0.40
    ah = h - top - lab_h
    aw = ah * lx / z_max
    gap = (w - left - 0.06 - 4 * aw) / 3
    rows = []
    for k, bed in enumerate(R.BED_ORDER):
        dv = decks[bed]['deck_vals']
        x0 = left + k * (aw + gap)
        ax = fig.add_axes([x0 / w, lab_h / h, aw / w, ah / h])
        ax.set_xlim(0, lx)
        ax.set_ylim(0, z_max)
        ax.set_aspect('equal', adjustable='box')
        for s in ('top', 'right'):
            ax.spines[s].set_visible(True)
        ax.set_xticks([0, 25, 50])
        ax.set_yticks([0, 40, 80, 120])
        if k:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        else:
            ax.set_xticklabels(['0', '25', '50 µm'])
            ax.set_ylabel('z (µm)', labelpad=2)
        ratio = dv['d_am_um'] / dv['d50_se_um']
        cx = (x0 + aw / 2) / w
        fig.text(cx, (lab_h - 0.30) / h, f'SE {src.fmt_g(dv["d50_se_um"])} µm', ha='center', va='center', fontsize=LABEL_PT, color=INK)
        fig.text(cx, (lab_h - 0.47) / h, f'SE {src.fmt_count(dv["n_se_plan"])} 개', ha='center', va='center', fontsize=NOTE_PT + 0.5,
                 color=INK2)
        fig.text(cx, (lab_h - 0.63) / h, f'{RATIO} = {src.fmt_g(ratio, 2)}', ha='center', va='center', fontsize=NOTE_PT + 0.5, color=INK2)
        row = dict(bed=bed, se_d50_um=dv['d50_se_um'], am_d_um=dv['d_am_um'], d_am_over_d_se=ratio, n_se_deck_plan=dv['n_se_plan'],
                   n_am_deck_plan=dv['n_am_plan'])
        if bed not in data:
            for s in ax.spines.values():
                s.set_linestyle((0, (3, 2)))
                s.set_edgecolor(PH)
            ax.add_patch(Rectangle((0, 0), lx, z_max, facecolor='none', edgecolor=PH, hatch='////', lw=0.4))
            ax.text(lx / 2, z_max / 2, WAIT, rotation=90, ha='center', va='center', fontsize=LABEL_PT, color=INK2,
                    bbox=dict(boxstyle='square,pad=0.2', fc='white', ec='none'))
            row.update(status=WAIT)
            rows.append(row)
            continue
        m = data[bed]['m']
        plate = m['plate_z_um']
        clip = Rectangle((0, 0), lx, plate, transform=ax.transData)
        sec = data[bed]['section']
        for ph, color in (('AM', AM_C), ('SE', SE_C)):
            circ = [Circle((float(r['x_um']), float(r['z_um'])), float(r['section_radius_um'])) for r in sec if r['phase'] == ph]
            pc = PatchCollection(circ, facecolor=color, edgecolor='none', linewidth=0)
            pc.set_clip_path(clip)
            ax.add_collection(pc)
        ax.plot([0, lx], [plate, plate], color=WALL_C, lw=1.2, solid_capstyle='butt', zorder=4)
        n_am_sec = len({r['particle_id'] for r in sec if r['phase'] == 'AM'})
        n_se_sec = len({r['particle_id'] for r in sec if r['phase'] == 'SE'})
        row.update(status='ok', end_step=data[bed]['rec']['frame']['end_step'], plate_z_um=plate, n_am_end=data[bed]['rec']['inventory']['n_am'],
                   n_se_end=data[bed]['rec']['inventory']['n_se'], n_am_in_section=n_am_sec, n_se_in_section=n_se_sec,
                   section_y_um=data[bed]['rec']['section']['y0_um'])
        rows.append(row)
    cols = ['bed', 'status', 'se_d50_um', 'am_d_um', 'd_am_over_d_se', 'n_se_deck_plan', 'n_am_deck_plan', 'end_step', 'plate_z_um',
            'n_am_end', 'n_se_end', 'section_y_um', 'n_am_in_section', 'n_se_in_section']
    return save(fig, 'p1_bed_strip', rows, cols, meta)


# ───────────────────────────── p2 — 압밀 곡선 + 끝 기공률 ─────────────────────────────

def fig_p2(data, meta):
    w, h = W_HALF, 2.70
    fig = plt.figure(figsize=(w, h))
    a1 = fig.add_axes([0.46 / w, 0.42 / h, 2.05 / w, (h - 0.86) / h])
    a2 = fig.add_axes([3.02 / w, 0.42 / h, 1.40 / w, (h - 0.86) / h])
    rows = []
    for bed in R.BED_ORDER:
        if bed not in data or not data[bed]['curve']:
            continue
        cv = data[bed]['curve']
        load = [(float(r['plate_pressure_MPa']), float(r['eps_sphere_pct'])) for r in cv if r['branch'] == 'loading'
                and float(r['plate_pressure_MPa']) > 1.0]
        P, E = np.array([p for p, _ in load]), np.array([e for _, e in load])
        a1.plot(P, E, color=SIZE_C[bed], lw=1.3, zorder=3)
        m = data[bed]['m']
        e_fix, p0, p_end = m['eps_sphere_pct'], m['p_t0minus_MPa'], m['p_end_MPa']
        a1.plot([p_end, p0], [e_fix, e_fix], color=SIZE_C[bed], lw=1.0, ls=(0, (1.5, 1.2)), zorder=3)
        a1.plot([p_end], [e_fix], marker='o', ms=3.6, mfc='white', mec=SIZE_C[bed], mew=0.9, zorder=4)
        a1.text(P[-1] + 6, E[-1], f'{src.fmt_g(float(bed[1:]))} µm', fontsize=VAL_PT, color=INK, ha='left', va='center')
        for p, e in load:
            rows.append(dict(panel='a_loading', bed=bed, plate_pressure_MPa=p, eps_sphere_pct=e))
        rows.append(dict(panel='a_relax_end', bed=bed, plate_pressure_MPa=p_end, eps_sphere_pct=e_fix))
        rows.append(dict(panel='a_t0minus', bed=bed, plate_pressure_MPa=p0, eps_sphere_pct=e_fix))
    a1.set_xlim(0, 350)
    a1.set_xticks([0, 100, 200, 300])
    a1.set_ylim(14, 40)
    a1.set_yticks([20, 30, 40])
    a1.set_xlabel('판 압력 (MPa · thermo 로그)', labelpad=2)
    a1.set_ylabel(f'기공률 {EPS} (%)', labelpad=2)
    a1.set_title('(a) 가압 가지 (p > 1 MPa)', loc='left', pad=3)
    ygrid(a1)
    # (b) 끝 상태 막대 (ε_sphere) + 정확 합집합 (속 빈 마름모)
    a2.set_ylim(0, 30)
    for k, bed in enumerate(R.BED_ORDER):
        if bed not in data:
            placeholder(a2, k)
            rows.append(dict(panel='b_end', bed=bed, status=WAIT))
            continue
        m = data[bed]['m']
        v, u = m['eps_sphere_pct'], m['eps_union_exact_pct']
        a2.bar(k, v, width=0.62, color=SIZE_C[bed], edgecolor='none', zorder=2)
        a2.text(k, v * 0.5, fmt_v(v, 4), ha='center', va='center', fontsize=VAL_PT, color='white', zorder=5, rotation=90)
        a2.plot([k], [u], marker='D', ms=3.8, mfc='white', mec=INK, mew=0.9, ls='none', zorder=4)
        a2.text(k, u + 1.0, fmt_v(u, 4), ha='center', va='bottom', fontsize=VAL_PT, color=INK2, zorder=5)
        rows.append(dict(panel='b_end', bed=bed, status='ok', eps_sphere_pct=v, eps_union_exact_pct=u,
                         plate_pressure_MPa=m['p_end_MPa'], end_step=data[bed]['rec']['frame']['end_step']))
    a2.set_yticks([0, 10, 20, 30])
    a2.set_ylabel('끝 기공률 (%)', labelpad=2)
    a2.set_title('(b) 판 고정 이완 끝', loc='left', pad=3)
    size_axis(a2)
    ygrid(a2)
    top_legend(fig, [('line', SIZE_C['D2'], '가압'), ('dotted', SIZE_C['D2'], '판 고정 이완'), ('hollow', None, '이완 끝')], 0.14, h)
    top_legend(fig, [('bar', SIZE_C['D2'], EPS), ('diamond', None, '정확 합집합')], 0.14, h, x_in=3.02)
    cols = ['panel', 'bed', 'status', 'plate_pressure_MPa', 'eps_sphere_pct', 'eps_union_exact_pct', 'end_step']
    return save(fig, 'p2_compaction', rows, cols, meta)


def fig_p2_relax(data, meta):
    """보조 — 판 고정 이완 가지 (정지 직전 t = 0⁻ 점 = 마지막 정상 압축 출력)."""
    w, h = W_HALF, 2.30
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0.52 / w, 0.42 / h, (w - 0.52 - 0.70) / w, (h - 0.72) / h])
    rows = []
    for bed in R.BED_ORDER:
        if bed not in data or not data[bed]['curve']:
            continue
        cv = data[bed]['curve']
        m = data[bed]['m']
        s_stop = data[bed]['rec']['compaction']['stop_step']
        rel = [((int(r['step']) - s_stop) / 1e3, float(r['plate_pressure_MPa'])) for r in cv if r['branch'] == 'fixed_height_relaxation']
        t = [0.0] + [a for a, _ in rel]
        p = [m['p_t0minus_MPa']] + [b for _, b in rel]
        ax.plot(t, p, color=SIZE_C[bed], lw=1.3, zorder=3)
        ax.plot([0.0], [m['p_t0minus_MPa']], marker='o', ms=3.8, mfc='white', mec=SIZE_C[bed], mew=0.9, zorder=4)
        ax.text(t[-1] + 2, p[-1], f'{src.fmt_g(float(bed[1:]))} µm  {fmt_v(p[-1], 4)} MPa', fontsize=VAL_PT, va='center', color=INK)
        rows.append(dict(bed=bed, point='t0minus_last_compression_output', steps_after_stop_k=0.0, plate_pressure_MPa=m['p_t0minus_MPa']))
        rows += [dict(bed=bed, point='relaxation', steps_after_stop_k=a, plate_pressure_MPa=b) for a, b in rel]
    ax.set_xlim(-3, 103)
    ax.set_xticks([0, 50, 100])
    ax.set_ylim(270, 305)
    ax.set_yticks([270, 280, 290, 300])
    ax.axhline(300, color=PH, lw=0.7, ls=(0, (3, 2)), zorder=1)
    ax.text(101, 300.6, '목표 300', fontsize=VAL_PT, color=INK2, ha='right', va='bottom')
    ax.set_xlabel('판 정지 뒤 step (× 10³)', labelpad=2)
    ax.set_ylabel('판 압력 (MPa)', labelpad=2)
    ygrid(ax)
    top_legend(fig, [('hollow', None, 't = 0⁻ (정지 직전 · 마지막 정상 압축 출력)'), ('text', None, f'0.7 · 1 µm {WAIT}')], 0.14, h, x_in=0.52)
    return save(fig, 'p2_relaxation', rows, ['bed', 'point', 'steps_after_stop_k', 'plate_pressure_MPa'], meta)


# ───────────────────────────── p3 — 접촉 · 피복 ─────────────────────────────

def fig_p3_contacts(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 3, left=0.40, gap=0.40, top=0.44)
    rows = []
    for r in bars(axs[0], data, 'am_se_cn_mean', (0, 30)):
        rows.append(dict(panel='a_am_se_cn', **r))
    axs[0].set_title('(a) AM–SE 접촉 수', loc='left', pad=3)
    axs[0].set_ylabel('AM 1개당 평균 (개)', labelpad=2)
    axs[0].set_yticks([0, 10, 20, 30])
    for r in bars(axs[1], data, 'se_se_cn_mean', (0, 6)):
        rows.append(dict(panel='b_se_se_cn', **r))
    axs[1].set_title('(b) SE–SE 접촉 수', loc='left', pad=3)
    axs[1].set_ylabel('SE 1개당 평균 (개)', labelpad=2)
    axs[1].set_yticks([0, 2, 4, 6])
    for r in bars(axs[2], data, 'coverage_hertz_pct', (0, 70), phys_key='coverage_physics_union_pct'):
        rows.append(dict(panel='c_am_coverage', **r))
    axs[2].set_title('(c) AM 피복률', loc='left', pad=3)
    axs[2].set_ylabel('SE 피복 (%)', labelpad=2)
    axs[2].set_yticks([0, 20, 40, 60])
    top_legend(fig, [('bar', SIZE_C['D2'], 'Hertz 계열 (주)'), ('hollow', None, 'Physics 합집합 cap (민감도)'),
                     ('hatch', None, WAIT)], 0.13, h, x_in=0.40)
    return save(fig, 'p3_contacts', rows, ['panel', 'bed', 'status', 'value', 'physics'], meta)


def fig_p3_overlap(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 2, left=0.46, gap=0.36, top=0.44)
    greys = ['#D9D9D9', '#A6A6A6', '#6E6E6E', '#262626']
    rows = []
    for ax, key, title in ((axs[0], 'am_frac_overlap_gt', '(a) δ / min(r₁, r₂)'), (axs[1], 'am_frac_overlap_card_gt', '(b) δ / (r₁ + r₂)')):
        ax.set_ylim(0, 110)
        bw = 0.15
        for k, bed in enumerate(R.BED_ORDER):
            if bed not in data:
                placeholder(ax, k, width=0.66, frac=0.9)
                rows.append(dict(panel=title[:3], bed=bed, status=WAIT))
                continue
            for j, T in enumerate(R.OVERLAP_THRESHOLDS):
                v = data[bed]['m'][f'{key}_{T:g}_pct']
                x = k + (j - 1.5) * bw
                ax.bar(x, v, width=bw * 0.92, color=greys[j], edgecolor='none', zorder=2)
                if v < 99.5:                  # 100 에 가까운 막대는 글 생략 (값 = CSV)
                    ax.text(x, v + 1.5, fmt_v(v, 3), ha='center', va='bottom', fontsize=NOTE_PT, color=INK, rotation=90, zorder=5)
                rows.append(dict(panel=title[:3], bed=bed, status='ok', threshold_pct=T, am_frac_pct=v))
        size_axis(ax)
        ygrid(ax)
        ax.set_yticks([0, 50, 100])
        ax.set_title(title, loc='left', pad=3)
    axs[0].set_ylabel('AM–SE 접촉 AM 비율 (%)', labelpad=2)
    items = [('text', None, '겹침 문턱 >')] + [('bar', g, f'{T:g} %') for g, T in zip(greys, R.OVERLAP_THRESHOLDS)]
    top_legend(fig, items, 0.13, h)
    return save(fig, 'p3_overlap_threshold', rows, ['panel', 'bed', 'status', 'threshold_pct', 'am_frac_pct'], meta)


def _box(ax, k, xs, color, width=0.30, hollow=False):
    q5, q25, q50, q75, q95 = (pct(xs, q) for q in (5, 25, 50, 75, 95))
    mean = float(np.mean(xs))
    fc = 'white' if hollow else color
    ec = INK if hollow else color
    ax.add_patch(Rectangle((k - width / 2, q25), width, q75 - q25, facecolor=fc, edgecolor=ec, lw=0.8, zorder=2))
    ax.plot([k - width / 2, k + width / 2], [q50, q50], color='white' if not hollow else INK, lw=1.0, zorder=3)
    ax.plot([k, k], [q5, q25], color=ec, lw=0.8, zorder=2)
    ax.plot([k, k], [q75, q95], color=ec, lw=0.8, zorder=2)
    ax.plot([k], [mean], marker='+', ms=4, color=INK if hollow else 'white', mew=0.9, zorder=4)
    return dict(n=len(xs), p5=q5, p25=q25, median=q50, p75=q75, p95=q95, mean=mean)


def fig_p3_per_am(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 2, left=0.46, gap=0.42, top=0.44)
    rows = []
    a, b = axs
    a.set_ylim(0, 45)
    b.set_ylim(0, 100)
    for k, bed in enumerate(R.BED_ORDER):
        if bed not in data:
            placeholder(a, k, width=0.5)
            placeholder(b, k, width=0.62)
            rows += [dict(panel='a_area_per_am', bed=bed, status=WAIT), dict(panel='b_coverage_per_am', bed=bed, status=WAIT)]
            continue
        pa = data[bed]['per_am']
        st = _box(a, k, [float(r['area_am_se_um2']) for r in pa], SIZE_C[bed], width=0.42)
        a.text(k, st['p95'] + 1.0, fmt_v(st['median'], 3), ha='center', va='bottom', fontsize=VAL_PT, color=INK)
        rows.append(dict(panel='a_area_per_am', bed=bed, status='ok', quantity='AM–SE contact area per AM (µm², c_cpl[22])', **st))
        sh = _box(b, k - 0.17, [float(r['coverage_hertz_pct']) for r in pa], SIZE_C[bed], width=0.28)
        sp = _box(b, k + 0.17, [float(r['coverage_physics_union_pct']) for r in pa if r['coverage_physics_union_pct'] != ''], SIZE_C[bed],
                  width=0.28, hollow=True)
        rows.append(dict(panel='b_coverage_per_am', bed=bed, status='ok', quantity='coverage Hertz-family per AM (%)', **sh))
        rows.append(dict(panel='b_coverage_per_am', bed=bed, status='ok', quantity='coverage Physics union cap per AM (%)', **sp))
    for ax in axs:
        size_axis(ax)
        ygrid(ax)
    a.set_yticks([0, 20, 40])
    b.set_yticks([0, 50, 100])
    a.set_ylabel('AM 1개당 AM–SE 접촉 면적 (µm²)', labelpad=2)
    b.set_ylabel('AM 1개 피복률 (%)', labelpad=2)
    a.set_title('(a) AM–SE 계면 면적 / AM', loc='left', pad=3)
    b.set_title('(b) AM 피복률 분포', loc='left', pad=3)
    top_legend(fig, [('bar', SIZE_C['D2'], 'Hertz 계열 (주)'), ('text', None, '□ Physics 합집합 cap (민감도)'),
                     ('text', None, '상자 25–75 · 선 5–95 % · + 평균')], 0.13, h)
    return save(fig, 'p3_per_am', rows, ['panel', 'bed', 'status', 'quantity', 'n', 'p5', 'p25', 'median', 'p75', 'p95', 'mean'], meta)


# ───────────────────────────── p4 — 수송 ─────────────────────────────

def fig_p4_tortuosity(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 2, left=0.46, gap=0.46, top=0.44)
    rows = [dict(panel='a_geometric', **r) for r in bars(axs[0], data, 'tau_geo_all', (0, 2.0))]
    axs[0].set_yticks([0, 1, 2])
    axs[0].set_ylabel('기하 tortuosity (최단 경로 / Δz)', labelpad=2)
    axs[0].set_title('(a) 기하 tortuosity', loc='left', pad=3)
    rows += [dict(panel='b_transport', **r) for r in bars(axs[1], data, 'tau2_ion_hertz', (0, 16), phys_key='tau2_ion_physics')]
    axs[1].set_yticks([0, 5, 10, 15])
    axs[1].set_ylabel(f'수송 tortuosity ({TAU_TR})', labelpad=2)
    axs[1].set_title('(b) 수송 tortuosity', loc='left', pad=3)
    top_legend(fig, [('bar', SIZE_C['D2'], 'Hertz (주)'), ('hollow', None, 'Physics (민감도)'), ('text', None, '두 양 = 다른 정의 · 비로 묶지 않음')],
               0.13, h)
    return save(fig, 'p4_tortuosity', rows, ['panel', 'bed', 'status', 'value', 'physics'], meta)


def fig_p4_f_connect(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 2, left=0.50, gap=0.46, top=0.44)
    rows = [dict(panel='a_f_ion', **r) for r in bars(axs[0], data, 'f_ion_hertz', (0, 0.08), phys_key='f_ion_physics')]
    axs[0].set_yticks([0, 0.04, 0.08])
    axs[0].set_yticklabels(['0', '0.04', '0.08'])
    axs[0].set_ylabel(F_ION, labelpad=2)
    axs[0].set_title('(a) 구조 전달계수 f', loc='left', pad=3)
    rows += [dict(panel='b_se_connected_am', **r) for r in bars(axs[1], data, 'se_connected_am_pct', (0, 110))]
    axs[1].set_yticks([0, 50, 100])
    axs[1].set_ylabel('SE 망과 연결된 AM (%)', labelpad=2)
    axs[1].set_title('(b) SE 망 연결 AM (연결성 기준)', loc='left', pad=3)
    top_legend(fig, [('bar', SIZE_C['D2'], 'Hertz (주)'), ('hollow', None, 'Physics (민감도)'), ('hatch', None, WAIT)], 0.13, h, x_in=0.50)
    return save(fig, 'p4_f_connect', rows, ['panel', 'bed', 'status', 'value', 'physics'], meta)


# ───────────────────────────── p6 — 두께 방향 ─────────────────────────────

def _zfig(data, specs, stem, meta, xlabels, xlims, xticks, legend_extra):
    w, h = W_HALF, 2.80
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, len(specs), left=0.50, gap=0.30, top=0.44)
    rows = []
    zmax = max([float(data[b]['zprof'][-1]['z_hi_um']) for b in data] + [130.0])
    for i, (ax, spec) in enumerate(zip(axs, specs)):
        for bed in R.BED_ORDER:
            if bed not in data:
                continue
            zp = data[bed]['zprof']
            z = [float(r['z_mid_um']) for r in zp]
            v = [fnum(r[spec['key']]) for r in zp]
            if spec.get('band'):
                lo = [fnum(r[spec['band'][0]]) for r in zp]
                hi = [fnum(r[spec['band'][1]]) for r in zp]
                ax.fill_betweenx(z, lo, hi, color=SIZE_C[bed], alpha=0.16, lw=0, zorder=1)
            ax.plot(v, z, color=SIZE_C[bed], lw=1.2, marker='o', ms=2.6, zorder=3)
            ax.axhline(float(zp[-1]['z_hi_um']), color=SIZE_C[bed], lw=0.6, ls=(0, (2, 2)), zorder=1)
            for r, vv in zip(zp, v):
                row = dict(panel=spec['panel'], bed=bed, z_lo_um=fnum(r['z_lo_um']), z_hi_um=fnum(r['z_hi_um']), z_mid_um=fnum(r['z_mid_um']),
                           value=vv)
                if spec.get('band'):
                    row.update(band_lo=fnum(r[spec['band'][0]]), band_hi=fnum(r[spec['band'][1]]))
                for extra in spec.get('extra', ()):
                    row[extra] = fnum(r[extra])
                rows.append(row)
        ax.set_ylim(0, zmax + 10)
        ax.set_yticks([0, 40, 80, 120])
        ax.set_xlim(*xlims[i])
        ax.set_xticks(xticks[i])
        ax.set_xticklabels([fmt_tick(t) for t in xticks[i]])
        ax.set_xlabel(xlabels[i], labelpad=2)
        ax.set_title(spec['title'], loc='left', pad=3)
        ax.xaxis.grid(True, color=GRID, lw=0.5)
        ax.set_axisbelow(True)
        if i:
            ax.set_yticklabels([])
        else:
            ax.set_ylabel('z (µm)', labelpad=2)
    items = [('line', SIZE_C[b], f'{b[1:]} µm') for b in R.BED_ORDER if b in data]
    items += [('text', None, f'{" · ".join(b[1:] for b in R.BED_ORDER if b not in data)} µm {WAIT}')] if len(data) < 4 else []
    items += [('dotted', INK2, '판 높이')] + legend_extra
    top_legend(fig, items, 0.13, h, x_in=0.50)
    cols = ['panel', 'bed', 'z_lo_um', 'z_hi_um', 'z_mid_um', 'value', 'band_lo', 'band_hi'] + sorted({e for s in specs for e in s.get('extra', ())})
    return save(fig, stem, rows, cols, meta)


def fig_p6(data, meta):
    s1 = _zfig(data, [dict(panel='a_local_porosity_union', key='por_union_pct', title='(a) 국소 기공률 (정확 합집합)',
                           extra=('por_union_se_pct', 'n_mc')),
                      dict(panel='b_se_connected_am', key='am_connected_pct', title='(b) SE 망 연결 AM', extra=('am_n',))],
               'p6_z_structure', meta, ['국소 기공률 (%)', 'SE 망과 연결된 AM (%)'], [(10, 30), (0, 105)], [[10, 20, 30], [0, 50, 100]],
               [('text', None, 'z 10 구간')])
    s2 = _zfig(data, [dict(panel='a_lw_am', key='lw_am_median_MPa', title='(a) AM 입자 응력', band=('lw_am_q25_MPa', 'lw_am_q75_MPa'),
                           extra=('lw_am_n', 'lw_am_wall_excluded')),
                      dict(panel='b_lw_se', key='lw_se_median_MPa', title='(b) SE 입자 응력', band=('lw_se_q25_MPa', 'lw_se_q75_MPa'),
                           extra=('lw_se_n', 'lw_se_wall_excluded'))],
               'p6_z_stress', meta, [f'{SVM} Love–Weber (MPa)', f'{SVM} Love–Weber (MPa)'], [(0, 600), (0, 300)],
               [[0, 300, 600], [0, 150, 300]], [('text', None, '선 중앙값 · 띠 25–75 %')])
    return s1, s2


# ───────────────────────────── p7 — 요약 · 문헌 방향 ─────────────────────────────

#: p7 요약 행 (키, 표시 이름) — 값 = metrics_<침대>.json (그대로) · 색 = D3 대비 비의 log₂
P7_ROWS = (
    ('eps_sphere_pct', f'기공률 {EPS} (%)'), ('eps_union_exact_pct', '기공률 정확 합집합 (%)'), ('am_se_cn_mean', 'AM–SE 접촉 수 (개)'),
    ('se_se_cn_mean', 'SE–SE 접촉 수 (개)'), ('area_am_se_per_am_mean_um2', 'AM–SE 접촉 면적 / AM (µm²)'),
    ('coverage_hertz_pct', 'AM 피복률 Hertz (%)'), ('coverage_physics_union_pct', 'AM 피복률 Physics (%)'),
    ('f_ion_hertz', f'{F_ION} (Hertz)'), ('tau2_ion_hertz', '수송 tortuosity (Hertz)'), ('tau_geo_all', '기하 tortuosity'),
    ('se_connected_am_pct', 'SE 망 연결 AM (%)'), ('constriction_power_share_ion_hertz', '협착 소산 몫 (이온 · Hertz)'),
    ('lw_am_nowall_median_MPa', 'AM 입자 응력 중앙값 (MPa)'), ('lw_se_nowall_median_MPa', 'SE 입자 응력 중앙값 (MPa)'),
)


def fig_p7_heat(data, meta):
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    w, h = W_HALF, 3.00
    fig = plt.figure(figsize=(w, h))
    left, top, bottom = 1.86, 0.40, 0.12
    cw = (w - left - 0.06) / 4
    n = len(P7_ROWS)
    rh = (h - top - bottom) / n
    ax = fig.add_axes([left / w, bottom / h, 4 * cw / w, n * rh / h])
    cmap = LinearSegmentedColormap.from_list('div', ['#1c5cab', '#86b6ef', '#F2F2F2', '#f2b48f', '#c4541f'])
    lim = math.log2(2.5)
    norm = Normalize(-lim, lim)
    ref = data.get('D3')
    rows = []
    for i, (key, name) in enumerate(P7_ROWS):
        y = n - 1 - i
        ax.text(-0.08, y + 0.5, name, ha='right', va='center', fontsize=NOTE_PT + 0.5, color=INK, transform=ax.transData)
        for k, bed in enumerate(R.BED_ORDER):
            if bed not in data:
                ax.add_patch(Rectangle((k, y), 1, 1, facecolor='white', edgecolor=PH, hatch='////', lw=0.4))
                rows.append(dict(metric=key, name=name, bed=bed, status=WAIT))
                continue
            v = data[bed]['m'][key]
            rv = ref['m'][key] if ref else None
            ratio = (v / rv) if (rv not in (None, 0) and v is not None) else None
            c = cmap(norm(math.log2(ratio))) if ratio and ratio > 0 else '#FFFFFF'
            ax.add_patch(Rectangle((k, y), 1, 1, facecolor=c, edgecolor='white', lw=0.8))
            ax.text(k + 0.5, y + 0.5, fmt_v(v, 3), ha='center', va='center', fontsize=NOTE_PT, color=INK)
            rows.append(dict(metric=key, name=name, bed=bed, status='ok', value=v, ratio_to_D3=ratio))
    for k, bed in enumerate(R.BED_ORDER):
        ax.text(k + 0.5, n + 0.15, f'SE {bed[1:]} µm', ha='center', va='bottom', fontsize=LABEL_PT, color=INK)
        if bed not in data:
            ax.text(k + 0.5, n / 2, WAIT, rotation=90, ha='center', va='center', fontsize=LABEL_PT, color=INK2,
                    bbox=dict(boxstyle='square,pad=0.2', fc='white', ec='none'))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, n)
    ax.axis('off')
    fig.text(0.06 / w, (h - 0.06) / h, '칸 글 = 값 · 색 = SE 3 µm 대비 비 (log₂ · 파랑 < 1 < 주황 · ±2.5 배에서 포화 · 좋고 나쁨 아님)',
             ha='left', va='top', fontsize=NOTE_PT, color=INK2)
    return save(fig, 'p7_summary_heat', rows, ['metric', 'name', 'bed', 'status', 'value', 'ratio_to_D3'], meta)


#: 문헌 방향 (작은 SE 쪽에서) — 카드 = 정본 litdb (origin/claude/friendly-meitner-lldvar) 에 있는 것만 · 값은 옮기지 않는다
LIT = (
    dict(key='eps_sphere_pct', name=f'기공률 {EPS} (%)', dir='↓', cards=(1, 2, 3)),
    dict(key='area_am_se_per_am_mean_um2', name='AM–SE 접촉 면적 / AM (µm²)', dir='↑', cards=(1, 2)),
    dict(key='coverage_hertz_pct', name='AM 피복률 Hertz (%)', dir='↑', cards=(2,)),
    dict(key='f_ion_hertz', name=f'{F_ION} (Hertz)', dir='↑', cards=(1, 2, 4, 5)),
    dict(key='tau2_ion_hertz', name='수송 tortuosity (Hertz)', dir='↓', cards=(1, 2, 4)),
    dict(key='se_connected_am_pct', name='SE 망 연결 AM (%)', dir='↑', cards=(6,)),
)
CARDS = {1: 'schlautmann2023_se_particle_size_composite_transport', 2: 'minnmann2024_microstructure_porosity_visualization',
         3: 'tailored_cathode_microstructure_low_pressure_assb', 4: 'minnmann2021_jes_charge_transport_bottlenecks',
         5: 'bazzoun2026_dem_fem_rnm_ionic', 6: 'shi2019_high_am_loading_particle_size_assb'}


def fig_p7_lit(data, meta):
    w, h = W_HALF, 3.00
    fig = plt.figure(figsize=(w, h))
    left, right, top, bottom, gx, gy = 0.16, 0.06, 0.20, 0.98, 0.22, 0.42
    nc, nr = 3, 2
    aw = (w - left - right - (nc - 1) * gx) / nc
    ah = (h - top - bottom - (nr - 1) * gy) / nr
    rows = []
    for i, spec in enumerate(LIT):
        r, c = divmod(i, nc)
        ax = fig.add_axes([(left + c * (aw + gx)) / w, (h - top - (r + 1) * ah - r * gy) / h, aw / w, ah / h])
        vals = [data[b]['m'][spec['key']] for b in R.BED_ORDER if b in data]
        vmax = max(vals) if vals else 1.0
        ax.set_ylim(0, vmax * 1.6)
        for k, bed in enumerate(R.BED_ORDER):
            if bed not in data:
                placeholder(ax, k, width=0.5, text='대기', frac=0.75)
                rows.append(dict(quantity=spec['key'], name=spec['name'], bed=bed, status=WAIT, literature_direction_small_se=spec['dir']))
                continue
            v = data[bed]['m'][spec['key']]
            ax.bar(k, v, width=0.5, color=SIZE_C[bed], edgecolor='none', zorder=2)
            ax.text(k, v + vmax * 0.04, fmt_v(v, 3), ha='center', va='bottom', fontsize=NOTE_PT, color=INK)
            rows.append(dict(quantity=spec['key'], name=spec['name'], bed=bed, status='ok', value=v, literature_direction_small_se=spec['dir'],
                             cards=' · '.join(CARDS[j] for j in spec['cards'])))
        size_axis(ax, label=False)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.set_title(spec['name'], loc='left', pad=2, fontsize=NOTE_PT + 0.5)
        refs = ','.join(str(j) for j in spec['cards'])
        ax.text(0.99, 0.99, f'문헌 {spec["dir"]} [{refs}]', transform=ax.transAxes, ha='right', va='top', fontsize=NOTE_PT, color=INK,
                bbox=dict(boxstyle='round,pad=0.22', fc='#F2F2F2', ec='#BFBFBF', lw=0.5))
    fig.text(0.5, 0.64 / h, 'SE D50 (µm)', ha='center', va='center', fontsize=LABEL_PT, color=INK)
    fig.text(left / w, 0.47 / h, '문헌 화살표 = 작은 SE 쪽의 방향 (정본 litdb 카드) · 우리 값은 나란히만 (일치 판정 아님) · 시드 1 · 단분산 (PSD 폭 그대로)',
             ha='left', va='center', fontsize=NOTE_PT - 0.5, color=INK2)
    items = [f'[{j}] {s}' for j, s in CARDS.items()]
    for li, k0 in enumerate(range(0, len(items), 2)):
        fig.text(left / w, (0.32 - 0.12 * li) / h, '   '.join(items[k0:k0 + 2]), ha='left', va='center', fontsize=NOTE_PT - 1.0, color=INK2)
    return save(fig, 'p7_lit_direction', rows, ['quantity', 'name', 'bed', 'status', 'value', 'literature_direction_small_se', 'cards'], meta)


def build_all():
    setup_fonts()
    data, decks = load()
    meta = {}
    fig_p1(data, decks, meta)
    fig_p2(data, meta)
    fig_p2_relax(data, meta)
    fig_p3_contacts(data, meta)
    fig_p3_overlap(data, meta)
    fig_p3_per_am(data, meta)
    fig_p4_tortuosity(data, meta)
    fig_p4_f_connect(data, meta)
    fig_p6(data, meta)
    fig_p7_heat(data, meta)
    fig_p7_lit(data, meta)
    beds = {b: ('ok' if b in data else WAIT) for b in R.BED_ORDER}
    out = dict(generator='docs/50kg/report_y4/draft2/make_draft2_figs.py', matplotlib=matplotlib.__version__, dpi=DPI, beds=beds,
               metrics_sha256={b: hashlib.sha256((R.DATA / b / f'metrics_{b}.json').read_bytes()).hexdigest() for b in data},
               colors=dict(AM=AM_C, SE=SE_C, size=SIZE_C, placeholder=PH), fonts=FONTS, figures=meta)
    (OUT / 'figs_meta.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for k, v in meta.items():
        print(f'{k:22s} {v["size_in"]} in · {v["px"]} px · dpi {v["dpi"]} · rows {v["csv_rows"]}')
    return out


if __name__ == '__main__':
    build_all()
