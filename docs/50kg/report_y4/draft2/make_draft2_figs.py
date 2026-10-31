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
- 축 범위 = 전부 자료 + 값 글 · 표지 자리 (fit_axis — 고정 범위 없음) · 그릴 때마다 check_figure (자료 · 글이 축 안 · 제목 · 다른 글과
  안 겹침 · '결과 대기' 글 = 자료 없는 침대만) — `--check` = 그리고 검사만 (파일 안 씀 · 문제 있으면 rc 1).
- 진단 diag_relax_drop_vs_N = 이완 강하 ↔ 판 정지 때 입자 수 + 어림 γNv/(2A) (affine 가정 · 덱 값) — 원장 DEMP-01 관계만.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import math
import re
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


# ───────────────────────────── 자료로 정하는 축 범위 ─────────────────────────────

LAB_PAD_PT = 2.0                    # 글 · 표지 둘레 여유 (pt)
MS_PHYS = 4.6                       # Physics 속 빈 표지 크기 (pt)


def ax_len_in(ax, axis='y'):
    """축 길이 (in) — 'y' = 높이 · 'x' = 폭."""
    pos, (fw, fh) = ax.get_position(), ax.figure.get_size_inches()
    return pos.height * fh if axis == 'y' else pos.width * fw


def text_w_pt(fig, s, size):
    """글 가로 길이 (pt) — 이 그림의 그리개로 잰다 (글꼴 대체 · 수식 포함)."""
    r = fig.canvas.get_renderer()
    w, _, _ = r.get_text_width_height_descent(s, fm.FontProperties(size=size), ismath=('$' in s))
    return w * 72.0 / fig.dpi


def lab_h_pt(size):
    """가로 글 한 줄 높이 + 여유 (pt) — 실측 (Carlito 숫자 6.5 pt 글 상자 = 6.5 pt) 보다 넉넉히."""
    return 1.25 * size + LAB_PAD_PT


def nice_axis(need_lo, need_hi, min_n=3, max_n=5, zero=False, snap=True):
    """[need_lo, need_hi] 를 덮는 축 끝 + 눈금 — 간격 s ∈ {1, 2, 5} × 10ⁿ · 눈금 = s 배수 min_n–max_n 개.
    snap = 끝을 s/4 배수로 바깥 올림 (남는 자리가 가장 적은 s · 같으면 큰 s) · snap=False = 끝 = 필요 범위 그대로 (눈금 수가 맞는 가장 큰 s).
    zero = 아래끝 0 고정 (막대 · 상자)."""
    if zero:
        need_lo = 0.0
    span = max(need_hi - need_lo, abs(need_hi) * 1e-9, 1e-12)
    best = None
    e0 = math.floor(math.log10(span)) - 2
    for e in range(e0, e0 + 4):
        for m in (1, 2, 5):
            s = m * 10.0 ** e
            g = s / 4.0
            if snap:
                lo = 0.0 if zero else math.floor(need_lo / g + 1e-9) * g
                hi = math.ceil(need_hi / g - 1e-9) * g
            else:
                lo, hi = need_lo, need_hi
            ticks = [k * s for k in range(math.ceil(lo / s - 1e-9), math.floor(hi / s + 1e-9) + 1)]
            if min_n <= len(ticks) <= max_n:
                key = ((need_lo - lo) + (hi - need_hi), -s)
                if best is None or key < best[0]:
                    best = (key, lo, hi, [round(t, 12) for t in ticks])
    if best is None:
        raise ValueError(f'눈금을 고르지 못했다 ({need_lo}, {need_hi})')
    return best[1], best[2], best[3]


def fit_axis(ax, axis, hi_items, lo_items=(), zero=False, snap=True, min_n=3, max_n=5):
    """축 범위 · 눈금을 자료로 — hi_items = [(값, 띄움 몫, 자리 pt)] : 값 + 띄움 몫 × 축 범위 + 자리 (pt → 축 길이로 환산) 가 위끝 안 ·
    lo_items = 같은 꼴 (값 아래로).  자리가 축 범위에 비례하므로 끝이 정해질 때까지 되풀이 (필요 범위는 늘기만 한다)."""
    L = ax_len_in(ax, axis) * 72.0
    vals = [v for v, _, _ in list(hi_items) + list(lo_items)]
    lo, hi = (0.0 if zero else min(vals)), max(vals)
    if hi - lo <= 0:
        hi = lo + max(abs(lo) * 0.1, 1.0)
    need_lo, need_hi = (0.0 if zero else min(vals)), max(vals)
    for _ in range(30):
        span = hi - lo
        need_hi = max([need_hi] + [v + (f + p / L) * span for v, f, p in hi_items])
        if not zero:
            need_lo = min([need_lo] + [v - (f + p / L) * span for v, f, p in lo_items])
        lo, hi, ticks = nice_axis(need_lo, need_hi, min_n, max_n, zero=zero, snap=snap)
        span = hi - lo
        if all(v + (f + p / L) * span <= hi + 1e-9 * span for v, f, p in hi_items) and \
                all(v - (f + p / L) * span >= lo - 1e-9 * span for v, f, p in lo_items):
            return lo, hi, ticks
    raise ValueError(f'축 범위가 정해지지 않았다 ({axis} · 자리 몫이 너무 크다)')


def set_axis(ax, axis, lo, hi, ticks):
    (ax.set_ylim if axis == 'y' else ax.set_xlim)(lo, hi)
    (ax.set_yticks if axis == 'y' else ax.set_xticks)(ticks)
    (ax.set_yticklabels if axis == 'y' else ax.set_xticklabels)([fmt_tick(t) for t in ticks])


def end_labels(ax, items, dx_pt=3.0, size=VAL_PT, gap_pt=0.8):
    """곡선 끝 글 — items = [(x, y, 글, 색)] → 끝점 오른쪽 (dx_pt) 에 두고 세로로 겹치지 않게 민다 (축 안) ·
    옮겨진 글은 끝점과 가는 선으로 잇는다.  끝점 오른쪽 자리 (x 범위) 는 부르는 쪽이 먼저 잡는다."""
    if not items:
        return
    fig = ax.figure
    k = fig.dpi / 72.0
    box = ax.bbox
    h = lab_h_pt(size) * k - LAB_PAD_PT * k + gap_pt * k   # 글 줄 간격 (px)
    disp = [ax.transData.transform((x, y)) for x, y, _, _ in items]
    order = sorted(range(len(items)), key=lambda i: (disp[i][1], i))
    ys = [disp[i][1] for i in order]
    lo_lim, hi_lim = box.y0 + h / 2, box.y1 - h / 2
    for _ in range(50):                        # 아래 → 위 밀기 · 위 → 아래 밀기 (축 안) · 겹침 없을 때까지
        for j in range(len(ys)):
            ys[j] = min(max(ys[j], lo_lim), hi_lim)
        for j in range(1, len(ys)):
            ys[j] = max(ys[j], ys[j - 1] + h)
        for j in range(len(ys) - 2, -1, -1):
            ys[j] = min(ys[j], ys[j + 1] - h)
        if all(ys[j + 1] - ys[j] >= h - 1e-6 for j in range(len(ys) - 1)) and ys[0] >= lo_lim - 1e-6 and ys[-1] <= hi_lim + 1e-6:
            break
    for j, i in enumerate(order):
        x, y, s, c = items[i]
        dy_pt = (ys[j] - disp[i][1]) / k
        moved = abs(dy_pt) > 0.5
        ax.annotate(s, xy=(x, y), xytext=(dx_pt, dy_pt), textcoords='offset points', ha='left', va='center', fontsize=size, color=INK,
                    zorder=5, arrowprops=(dict(arrowstyle='-', color=c, lw=0.5, shrinkA=0, shrinkB=0) if moved else None))


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


def bars(ax, data, key, phys_key=None, scale=1.0, sig=3, lab_dy=0.015):
    """입도 칸 막대 (Hertz · 주) + Physics 속 빈 표지 (민감도) — 값 글 = 막대 위 · Physics 값 글 = 표지 위 (표지가 막대 안이면 표지 아래 흰 글).
    세로 범위 · 눈금 = 자료 + 값 글 · 표지 자리 (fit_axis — 고정 범위 없음).  반환 = CSV 행."""
    vals = {b: (data[b]['m'][key] * scale, data[b]['m'][phys_key] * scale if phys_key else None) for b in R.BED_ORDER if b in data}
    items = [(0.0, 0.0, 0.0)]
    for v, pv in vals.values():
        items.append((v, lab_dy, lab_h_pt(VAL_PT)))
        if pv is not None:
            items.append((pv, 0.0, MS_PHYS / 2 + LAB_PAD_PT))
            if pv > v:
                items.append((pv, 0.035, lab_h_pt(VAL_PT)))
    lo, hi, ticks = fit_axis(ax, 'y', items, zero=True)
    set_axis(ax, 'y', lo, hi, ticks)
    rows = []
    span = hi - lo
    for k, bed in enumerate(R.BED_ORDER):
        if bed not in data:
            placeholder(ax, k)
            rows.append(dict(bed=bed, status=WAIT))
            continue
        v, pv = vals[bed]
        ax.bar(k, v, width=0.62, color=SIZE_C[bed], edgecolor='none', zorder=2)
        ax.text(k, v + span * lab_dy, fmt_v(v, sig), ha='center', va='bottom', fontsize=VAL_PT, color=INK, zorder=5)
        r = dict(bed=bed, status='ok', value=v)
        if phys_key:
            ax.plot([k], [pv], marker='o', ms=MS_PHYS, mfc='white', mec=INK, mew=0.9, ls='none', zorder=4)
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


def top_legend(fig, items, y_in, h, x_in=0.46, w=W_HALF, gap=0.14, right_in=0.06):
    """그림 위 한 줄 범례 (축 밖) — items = [(종류, 색, 글)] · 종류 = 'bar' | 'hollow' | 'diamond' | 'dot' | 'line' | 'dotted' | 'hatch' | 'text' ·
    gap = 항목 사이 (in) — 한 줄이 그림 폭 (오른쪽 여백 right_in) 을 넘으면 사이만 줄인다 (최소 0.05 in · 글은 줄이지 않는다)."""
    x = x_in
    sw, sh = 0.13, 0.08                       # 견본 크기 (in)
    adv = {'bar': sw + 0.04, 'hatch': sw + 0.04, 'hollow': 0.15, 'diamond': 0.15, 'dot': 0.15, 'line': 0.24, 'dotted': 0.24, 'text': 0.0}
    need = sum(adv[k] + text_w_pt(fig, t, NOTE_PT + 0.5) / 72.0 for k, _, t in items)
    if len(items) > 1 and need + gap * (len(items) - 1) > w - x_in - right_in:
        gap = max(0.05, (w - x_in - right_in - need) / (len(items) - 1))
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
        elif kind == 'dot':
            fig.lines.append(matplotlib.lines.Line2D([(x + 0.06) / w], [yy], transform=fig.transFigure, marker='o', ms=4.0, mfc=color,
                                                     mec=color, mew=0.0, ls='none'))
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
        x += bb.width / fig.dpi + gap


# ───────────────────────────── 검사 (그릴 때마다 · --check = 그리고 검사만) ─────────────────────────────

#: 축 밖에 일부러 두는 축 글 (열지도 행 이름 · 열 머리) — 이 표지가 없는 축 글은 전부 '값 글' 규칙
#: (축 안 · 그 축 제목과 겹치지 않음 · 같은 축 글끼리 겹치지 않음)
GID_OUTSIDE_OK = 'outside-ok'
#: 일부러 자른 기하 모음 (1쪽 단면 원 = 벽 · 판에서 자름) — 범위 검사 밖 · 대신 자르기가 실제로 걸렸는지 검사
GID_SECTION_CROP = 'section-crop'
TOL_PX = 0.5                       # 화면 px (그림 dpi) — 경계 위 = 안
CHECK = dict(write=True, results={}, beds_with_data=())


def _wait_text_problem(s):
    """'결과 대기' 글이 자료 있는 침대를 적으면 문제 — 글 안 'µm' 앞 수 = 침대 D50 (침대 목록은 자료에서 나와야 한다)."""
    if WAIT not in s or 'µm' not in s:
        return None
    named = {f'D{tok}' for tok in re.findall(r'\d+(?:\.\d+)?', s.split(WAIT)[0])} & set(R.BED_ORDER)
    stale = sorted(named & set(CHECK['beds_with_data']), key=R.BED_ORDER.index)
    return f'"{s}" 이 자료 있는 침대 {", ".join(stale)} 를 결과 대기로 적음' if stale else None


def _text_bb(t, renderer):
    """글 상자 = 글 + (있으면) 테두리 상자 — 화면 좌표 (끝 글 이음선 (annotate 화살) 은 빼고 글만)."""
    from matplotlib.text import Text
    from matplotlib.transforms import Bbox
    bbs = [Text.get_window_extent(t, renderer)]
    if t.get_bbox_patch() is not None:
        bbs.append(t.get_bbox_patch().get_window_extent(renderer))
    return Bbox.union(bbs)


def _sticks_out(bb, box, tol=TOL_PX):
    return bb.x0 < box.x0 - tol or bb.x1 > box.x1 + tol or bb.y0 < box.y0 - tol or bb.y1 > box.y1 + tol


def _overlap(a, b, tol=TOL_PX):
    return min(a.x1, b.x1) - max(a.x0, b.x0) > tol and min(a.y1, b.y1) - max(a.y0, b.y0) > tol


def _ax_name(fig, ax):
    titles = [t.get_text() for t in (ax._left_title, ax.title, ax._right_title) if t.get_text()]
    return f'축 {fig.axes.index(ax)}' + (f' "{titles[0]}"' if titles else '')


def _deliberate_crop(a, ax):
    """일부러 자른 모음인가 — 축 기본 클립 (= 축 상자) 이 아닌 클립 상자 · 클립 경로 (matplotlib 은 사각 클립을 클립 상자로 바꾼다)."""
    if a.get_clip_path() is not None:
        return True
    cb = a.get_clip_box()
    return cb is not None and not np.allclose(cb.bounds, ax.bbox.bounds, atol=TOL_PX)


def _lim_txt(ax):
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    return f'xlim {x0:.6g}–{x1:.6g} · ylim {y0:.6g}–{y1:.6g}'


def check_figure(fig, stem):
    """그림 하나 검사 → (문제 목록, 센 수).
    축마다: ① 그린 자료 (선 · 곡선 점 · 표지 (표지 반지름 포함) · 막대 · 상자 · 수염 · 띠 · 빈 칸 빗금) 가 축 범위 안
    ② 축 글 (값 글 · 끝 글 · 주석) 이 축 안 (GID_OUTSIDE_OK 빼고) ③ 축 글이 그 축 제목과 안 겹침 ④ 같은 축 글끼리 안 겹침.
    그림 글 (머리 줄 · 아래 글) = 그림 안 · 서로 안 겹침 · 축 제목과 안 겹침 · 머리 줄 견본 (선 · 상자) = 그림 안.
    클립 경로를 일부러 건 모음 (1쪽 단면 원 = 판 · 벽에서 자름) 은 범위 검사에서 빼고 수만 센다."""
    fig.canvas.draw()
    rnd = fig.canvas.get_renderer()
    probs = []
    n = dict(points=0, patches=0, band_vertices=0, texts=0, fig_texts=0, cropped_collections=0)
    for ax in fig.axes:
        box, name = ax.bbox, _ax_name(fig, ax)
        inv = ax.transData.inverted()
        for ln in ax.lines:
            if not ln.get_visible():
                continue
            xy = np.asarray(ln.get_xydata(), dtype=float)
            if not len(xy):
                continue
            pts = ln.get_transform().transform(xy)
            ok = np.all(np.isfinite(pts), axis=1)
            mk = ln.get_marker()
            r = 0.0 if mk in (None, 'None', '', ' ', 'none') else 0.5 * ln.get_markersize() * fig.dpi / 72.0
            for (x, y), (dx, dy) in zip(pts[ok], xy[ok]):
                n['points'] += 1
                if x - r < box.x0 - TOL_PX or x + r > box.x1 + TOL_PX or y - r < box.y0 - TOL_PX or y + r > box.y1 + TOL_PX:
                    what = '표지' if r else '선 점'
                    probs.append(f'{stem} · {name} · {what} (x {dx:.6g}, y {dy:.6g}) 축 밖 ({_lim_txt(ax)})')
        for p in ax.patches:
            if not p.get_visible():
                continue
            v = p.get_transform().transform(p.get_path().vertices)
            v = v[np.all(np.isfinite(v), axis=1)]
            n['patches'] += 1
            if len(v) and (v[:, 0].min() < box.x0 - TOL_PX or v[:, 0].max() > box.x1 + TOL_PX
                           or v[:, 1].min() < box.y0 - TOL_PX or v[:, 1].max() > box.y1 + TOL_PX):
                d = inv.transform(v)
                probs.append(f'{stem} · {name} · 막대/상자 (x {d[:, 0].min():.6g}–{d[:, 0].max():.6g}, '
                             f'y {d[:, 1].min():.6g}–{d[:, 1].max():.6g}) 축 밖 ({_lim_txt(ax)})')
        for c in ax.collections:
            if not c.get_visible():
                continue
            if c.get_gid() == GID_SECTION_CROP:
                n['cropped_collections'] += 1
                if not _deliberate_crop(c, ax):
                    probs.append(f'{stem} · {name} · 단면 모음 (자른다고 표시) 에 자르기가 안 걸림 — 축 기본 클립뿐 (판 위로 나온 원이 그려진다)')
                continue
            for path in c.get_paths():
                v = c.get_transform().transform(path.vertices)
                v = v[np.all(np.isfinite(v), axis=1)]
                n['band_vertices'] += len(v)
                if len(v) and (v[:, 0].min() < box.x0 - TOL_PX or v[:, 0].max() > box.x1 + TOL_PX
                               or v[:, 1].min() < box.y0 - TOL_PX or v[:, 1].max() > box.y1 + TOL_PX):
                    d = inv.transform(v)
                    probs.append(f'{stem} · {name} · 띠 (x {d[:, 0].min():.6g}–{d[:, 0].max():.6g}, '
                                 f'y {d[:, 1].min():.6g}–{d[:, 1].max():.6g}) 축 밖 ({_lim_txt(ax)})')
        titles = [t for t in (ax._left_title, ax.title, ax._right_title) if t.get_text()]
        texts = [t for t in ax.texts if t.get_visible() and t.get_text()]
        bbs = [_text_bb(t, rnd) for t in texts]
        for t, bb in zip(texts, bbs):
            n['texts'] += 1
            s = t.get_text().replace('\n', ' ')
            if t.get_gid() != GID_OUTSIDE_OK and _sticks_out(bb, box):
                probs.append(f'{stem} · {name} · 글 "{s}" 축 밖 (위 {bb.y1 - box.y1:+.1f} px · 오른쪽 {bb.x1 - box.x1:+.1f} px · '
                             f'아래 {box.y0 - bb.y0:+.1f} px · 왼쪽 {box.x0 - bb.x0:+.1f} px · {_lim_txt(ax)})')
            for tt in titles:
                if _overlap(bb, tt.get_window_extent(rnd)):
                    probs.append(f'{stem} · {name} · 글 "{s}" 이 제목 "{tt.get_text()}" 과 겹침')
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if _overlap(bbs[i], bbs[j]):
                    probs.append(f'{stem} · {name} · 글 "{texts[i].get_text()}" ↔ "{texts[j].get_text()}" 겹침')
        for t in texts:
            w = _wait_text_problem(t.get_text())
            if w:
                probs.append(f'{stem} · {name} · 글 {w}')
    fbox = fig.bbox
    ftexts = [t for t in fig.texts if t.get_visible() and t.get_text()]
    for t in ftexts:
        w = _wait_text_problem(t.get_text())
        if w:
            probs.append(f'{stem} · 그림 글 {w}')
    fbbs = [_text_bb(t, rnd) for t in ftexts]
    all_titles = [t for ax in fig.axes for t in (ax._left_title, ax.title, ax._right_title) if t.get_text()]
    for t, bb in zip(ftexts, fbbs):
        n['fig_texts'] += 1
        if _sticks_out(bb, fbox):
            probs.append(f'{stem} · 그림 글 "{t.get_text()}" 그림 밖 (오른쪽 {bb.x1 - fbox.x1:+.1f} px · 위 {bb.y1 - fbox.y1:+.1f} px)')
        for tt in all_titles:
            if _overlap(bb, tt.get_window_extent(rnd)):
                probs.append(f'{stem} · 그림 글 "{t.get_text()}" 이 축 제목 "{tt.get_text()}" 과 겹침')
    for i in range(len(ftexts)):
        for j in range(i + 1, len(ftexts)):
            if _overlap(fbbs[i], fbbs[j]):
                probs.append(f'{stem} · 그림 글 "{ftexts[i].get_text()}" ↔ "{ftexts[j].get_text()}" 겹침')
    for a in list(fig.lines) + list(fig.patches):
        if isinstance(a, matplotlib.lines.Line2D):
            v = a.get_transform().transform(np.asarray(a.get_xydata(), dtype=float))
        else:
            v = a.get_transform().transform(a.get_path().vertices)
        if len(v) and (v[:, 0].min() < fbox.x0 - TOL_PX or v[:, 0].max() > fbox.x1 + TOL_PX
                       or v[:, 1].min() < fbox.y0 - TOL_PX or v[:, 1].max() > fbox.y1 + TOL_PX):
            probs.append(f'{stem} · 머리 줄 견본 그림 밖')
    return probs, n


def save(fig, stem, rows, cols, meta):
    probs, counts = check_figure(fig, stem)
    CHECK['results'][stem] = dict(problems=probs, counts=counts)
    if not CHECK['write']:
        plt.close(fig)
        return None
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
    widths = {decks[b]['deck_vals']['box_x_um'] for b in R.BED_ORDER}       # 단면 가로 = 덱 상자 x (침대마다 같아야)
    src.need(len(widths) == 1, f'덱 상자 x 가 침대마다 다르다: {widths}')
    lx = float(widths.pop())
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
        ax.set_xticks([0, lx / 2, lx])
        ax.set_yticks(list(range(0, int(z_max) + 1, 40)))
        if k:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        else:
            ax.set_xticklabels([fmt_tick(0), fmt_tick(lx / 2), f'{fmt_tick(lx)} µm'])
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
            pc.set_gid(GID_SECTION_CROP)
            ax.add_collection(pc)
            pc.set_clip_path(clip)        # add_collection 뒤에 — 앞에 걸면 축 클립으로 덮인다 (사각 클립 = 클립 상자)
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
    curves = {}
    for bed in R.BED_ORDER:
        if bed not in data or not data[bed]['curve']:
            continue
        cv = data[bed]['curve']
        load = [(float(r['plate_pressure_MPa']), float(r['eps_sphere_pct'])) for r in cv if r['branch'] == 'loading'
                and float(r['plate_pressure_MPa']) > 1.0]
        curves[bed] = (np.array([p for p, _ in load]), np.array([e for _, e in load]), load)
    # (a) 범위 = 자료 (가압 곡선 · 이완 점선 · 이완 끝 표지) + 곡선 끝 글 자리 (오른쪽) — 고정 범위 없음
    labs = {b: f'{src.fmt_g(float(b[1:]))} µm' for b in curves}
    x_items, y_hi, y_lo = [(0.0, 0.0, 0.0)], [], []
    for b, (P, E, _) in curves.items():
        m = data[b]['m']
        x_items.append((max(P.max(), m['p_t0minus_MPa']), 0.0, 3.0 + text_w_pt(fig, labs[b], VAL_PT) + LAB_PAD_PT))
        y_hi.append((float(E.max()), 0.0, LAB_PAD_PT))
        y_lo.append((min(float(E.min()), m['eps_sphere_pct']), 0.0, 1.8 + LAB_PAD_PT))
    if curves:
        set_axis(a1, 'x', *fit_axis(a1, 'x', x_items, zero=True))
        set_axis(a1, 'y', *fit_axis(a1, 'y', y_hi, y_lo))
    ends = []
    for bed, (P, E, load) in curves.items():
        a1.plot(P, E, color=SIZE_C[bed], lw=1.3, zorder=3)
        m = data[bed]['m']
        e_fix, p0, p_end = m['eps_sphere_pct'], m['p_t0minus_MPa'], m['p_end_MPa']
        a1.plot([p_end, p0], [e_fix, e_fix], color=SIZE_C[bed], lw=1.0, ls=(0, (1.5, 1.2)), zorder=3)
        a1.plot([p_end], [e_fix], marker='o', ms=3.6, mfc='white', mec=SIZE_C[bed], mew=0.9, zorder=4)
        ends.append((float(P[-1]), float(E[-1]), labs[bed], SIZE_C[bed]))
        for p, e in load:
            rows.append(dict(panel='a_loading', bed=bed, plate_pressure_MPa=p, eps_sphere_pct=e))
        rows.append(dict(panel='a_relax_end', bed=bed, plate_pressure_MPa=p_end, eps_sphere_pct=e_fix))
        rows.append(dict(panel='a_t0minus', bed=bed, plate_pressure_MPa=p0, eps_sphere_pct=e_fix))
    end_labels(a1, ends)
    a1.set_xlabel('판 압력 (MPa · thermo 로그)', labelpad=2)
    a1.set_ylabel(f'기공률 {EPS} (%)', labelpad=2)
    a1.set_title('(a) 가압 가지 (p > 1 MPa)', loc='left', pad=3)
    ygrid(a1)
    # (b) 끝 상태 막대 (ε_sphere) + 정확 합집합 (속 빈 마름모) — 범위 = 자료 + 마름모 · 값 글 자리
    b_items = [(0.0, 0.0, 0.0)]
    for bed in R.BED_ORDER:
        if bed in data:
            m = data[bed]['m']
            b_items += [(m['eps_sphere_pct'], 0.0, LAB_PAD_PT), (m['eps_union_exact_pct'], 0.0, 1.9 + LAB_PAD_PT),
                        (m['eps_union_exact_pct'], 0.035, lab_h_pt(VAL_PT))]
    b_lo, b_hi, b_ticks = fit_axis(a2, 'y', b_items, zero=True)
    set_axis(a2, 'y', b_lo, b_hi, b_ticks)
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
        a2.text(k, u + (b_hi - b_lo) * 0.035, fmt_v(u, 4), ha='center', va='bottom', fontsize=VAL_PT, color=INK2, zorder=5)
        rows.append(dict(panel='b_end', bed=bed, status='ok', eps_sphere_pct=v, eps_union_exact_pct=u,
                         plate_pressure_MPa=m['p_end_MPa'], end_step=data[bed]['rec']['frame']['end_step']))
    a2.set_ylabel('끝 기공률 (%)', labelpad=2)
    a2.set_title('(b) 판 고정 이완 끝', loc='left', pad=3)
    size_axis(a2)
    ygrid(a2)
    top_legend(fig, [('line', SIZE_C['D2'], '가압'), ('dotted', SIZE_C['D2'], '판 고정 이완'), ('hollow', None, '이완 끝')], 0.14, h)
    top_legend(fig, [('bar', SIZE_C['D2'], EPS), ('diamond', None, '정확 합집합')], 0.14, h, x_in=3.02)
    cols = ['panel', 'bed', 'status', 'plate_pressure_MPa', 'eps_sphere_pct', 'eps_union_exact_pct', 'end_step']
    return save(fig, 'p2_compaction', rows, cols, meta)


#: p2_relaxation (b) 확대 칸 규칙 — 이완 폭 (t = 0⁻ 포함 최대 − 최소) 이 (a) 전체 칸 자료 폭의 이 몫보다 작은 침대를 (b) 에 크게 다시 그린다
#: (침대 목록을 적지 않는다 · 그런 침대가 없거나 전부면 (a) 한 칸)
ZOOM_FRAC = 0.25
MS_T0 = 3.8                         # t = 0⁻ 속 빈 표지 크기 (pt)


def target_mpa(data):
    """가압 목표 (MPa) — 침대 기록 (metrics frame.target_pressure_MPa) · 침대마다 같아야 한다."""
    vals = {data[b]['rec']['frame']['target_pressure_MPa'] for b in data}
    if len(vals) != 1:
        raise ValueError(f'가압 목표가 침대마다 다르다: {vals}')
    return float(vals.pop())


def waiting_beds(have):
    """자료 없는 침대 (BED_ORDER 순) → '0.7 · 1 µm 결과 대기' 꼴 글 · 없으면 None (침대 목록 = 자료에서)."""
    w = [b for b in R.BED_ORDER if b not in have]
    return f'{" · ".join(b[1:] for b in w)} µm {WAIT}' if w else None


def _relax_panel(ax, beds, rel, target, labeled):
    """이완 한 칸 — beds 의 곡선 · t = 0⁻ 표지 · 목표 점선 + 글 · labeled 침대의 끝 값 글 · 범위 · 눈금 = 자료 (고정 범위 없음)."""
    fig = ax.figure
    t_end = max(rel[b][0][-1] for b in beds)
    tgt_lab = f'목표 {src.fmt_g(target)}'
    x_hi = [(t_end, 0.0, LAB_PAD_PT)] + [(rel[b][0][-1], 0.0, 3.0 + text_w_pt(fig, fmt_v(rel[b][1][-1], 4), VAL_PT) + LAB_PAD_PT)
                                         for b in beds if b in labeled]
    set_axis(ax, 'x', *fit_axis(ax, 'x', x_hi, [(0.0, 0.0, MS_T0 / 2 + LAB_PAD_PT)], snap=False))
    y_hi = [(max(rel[b][1]), 0.0, MS_T0 / 2 + LAB_PAD_PT) for b in beds] + [(target, 0.0, 1.0 + lab_h_pt(VAL_PT))]
    y_lo = [(min(rel[b][1]), 0.0, LAB_PAD_PT) for b in beds]
    set_axis(ax, 'y', *fit_axis(ax, 'y', y_hi, y_lo))
    ax.axhline(target, color=PH, lw=0.7, ls=(0, (3, 2)), zorder=1)
    ax.annotate(tgt_lab, xy=(t_end, target), xytext=(0, 1.0), textcoords='offset points', fontsize=VAL_PT, color=INK2, ha='right',
                va='bottom')
    for b in beds:
        t, p = rel[b]
        ax.plot(t, p, color=SIZE_C[b], lw=1.3, zorder=3)
        ax.plot([0.0], [p[0]], marker='o', ms=MS_T0, mfc='white', mec=SIZE_C[b], mew=0.9, zorder=4)
    end_labels(ax, [(rel[b][0][-1], rel[b][1][-1], fmt_v(rel[b][1][-1], 4), SIZE_C[b]) for b in beds if b in labeled])
    ax.set_xlabel('판 정지 뒤 step (× 10³)', labelpad=2)
    ygrid(ax)


def fig_p2_relax(data, meta):
    """보조 — 판 고정 이완 가지 (정지 직전 t = 0⁻ 점 = 마지막 정상 압축 출력) · (a) 자료 있는 침대 전부 (b) 이완 폭이 작은 침대 확대 (ZOOM_FRAC)."""
    rel = {}
    for bed in R.BED_ORDER:
        if bed not in data or not data[bed]['curve']:
            continue
        cv = data[bed]['curve']
        m = data[bed]['m']
        s_stop = data[bed]['rec']['compaction']['stop_step']
        pts = [((int(r['step']) - s_stop) / 1e3, float(r['plate_pressure_MPa'])) for r in cv if r['branch'] == 'fixed_height_relaxation']
        rel[bed] = ([0.0] + [a for a, _ in pts], [m['p_t0minus_MPa']] + [b for _, b in pts])
    target = target_mpa(data)
    full = max(max(p) for _, p in rel.values()) - min(min(p) for _, p in rel.values())
    zoom = [b for b in rel if max(rel[b][1]) - min(rel[b][1]) < ZOOM_FRAC * full]
    two = 0 < len(zoom) < len(rel)
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 2 if two else 1, left=0.50, gap=0.40, right=0.08, top=0.44)
    _relax_panel(axs[0], list(rel), rel, target, labeled=[b for b in rel if not two or b not in zoom])
    axs[0].set_ylabel('판 압력 (MPa)', labelpad=2)
    if two:
        axs[0].set_title('(a) 전체', loc='left', pad=3)
        _relax_panel(axs[1], zoom, rel, target, labeled=zoom)
        axs[1].set_title(f'(b) 확대 — {" · ".join(b[1:] for b in zoom)} µm', loc='left', pad=3)
    rows = []
    for bed, (t, p) in rel.items():
        pan = 'a+b' if two and bed in zoom else 'a'
        rows.append(dict(bed=bed, point='t0minus_last_compression_output', panel=pan, steps_after_stop_k=0.0, plate_pressure_MPa=p[0]))
        rows += [dict(bed=bed, point='relaxation', panel=pan, steps_after_stop_k=a, plate_pressure_MPa=b) for a, b in zip(t[1:], p[1:])]
    items = [('hollow', None, 't = 0⁻ (정지 직전)')] + [('line', SIZE_C[b], f'{b[1:]} µm') for b in rel]
    wt = waiting_beds(rel)
    top_legend(fig, items + ([('text', None, wt)] if wt else []), 0.14, h, x_in=0.50)
    return save(fig, 'p2_relaxation', rows, ['bed', 'point', 'panel', 'steps_after_stop_k', 'plate_pressure_MPa'], meta)


# ───────────────────────────── p3 — 접촉 · 피복 ─────────────────────────────

def fig_p3_contacts(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 3, left=0.40, gap=0.40, top=0.44)
    rows = []
    for r in bars(axs[0], data, 'am_se_cn_mean'):
        rows.append(dict(panel='a_am_se_cn', **r))
    axs[0].set_title('(a) AM–SE 접촉 수', loc='left', pad=3)
    axs[0].set_ylabel('AM 1개당 평균 (개)', labelpad=2)
    for r in bars(axs[1], data, 'se_se_cn_mean'):
        rows.append(dict(panel='b_se_se_cn', **r))
    axs[1].set_title('(b) SE–SE 접촉 수', loc='left', pad=3)
    axs[1].set_ylabel('SE 1개당 평균 (개)', labelpad=2)
    for r in bars(axs[2], data, 'coverage_hertz_pct', phys_key='coverage_physics_union_pct'):
        rows.append(dict(panel='c_am_coverage', **r))
    axs[2].set_title('(c) AM 피복률', loc='left', pad=3)
    axs[2].set_ylabel('SE 피복 (%)', labelpad=2)
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
        bw = 0.15
        lab_dy = 0.015
        # 범위 = 막대 위끝 + (100 에 가깝지 않은 막대의) 세운 값 글 길이 — 고정 범위 없음
        items = [(0.0, 0.0, 0.0)]
        for bed in R.BED_ORDER:
            if bed in data:
                for T in R.OVERLAP_THRESHOLDS:
                    v = data[bed]['m'][f'{key}_{T:g}_pct']
                    items.append((v, 0.0, LAB_PAD_PT))
                    if v < 99.5:
                        items.append((v, lab_dy, text_w_pt(fig, fmt_v(v, 3), NOTE_PT) + LAB_PAD_PT))
        lo, hi, ticks = fit_axis(ax, 'y', items, zero=True)
        set_axis(ax, 'y', lo, hi, ticks)
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
                    ax.text(x, v + (hi - lo) * lab_dy, fmt_v(v, 3), ha='center', va='bottom', fontsize=NOTE_PT, color=INK, rotation=90,
                            zorder=5)
                rows.append(dict(panel=title[:3], bed=bed, status='ok', threshold_pct=T, am_frac_pct=v))
        size_axis(ax)
        ygrid(ax)
        ax.set_title(title, loc='left', pad=3)
    axs[0].set_ylabel('AM–SE 접촉 AM 비율 (%)', labelpad=2)
    items = [('text', None, '겹침 문턱 >')] + [('bar', g, f'{T:g} %') for g, T in zip(greys, R.OVERLAP_THRESHOLDS)]
    top_legend(fig, items, 0.13, h)
    return save(fig, 'p3_overlap_threshold', rows, ['panel', 'bed', 'status', 'threshold_pct', 'am_frac_pct'], meta)


def _box_stats(xs):
    q5, q25, q50, q75, q95 = (pct(xs, q) for q in (5, 25, 50, 75, 95))
    return dict(n=len(xs), p5=q5, p25=q25, median=q50, p75=q75, p95=q95, mean=float(np.mean(xs)))


def _box(ax, k, xs, color, width=0.30, hollow=False):
    st = _box_stats(xs)
    q5, q25, q50, q75, q95, mean = (st[c] for c in ('p5', 'p25', 'median', 'p75', 'p95', 'mean'))
    fc = 'white' if hollow else color
    ec = INK if hollow else color
    ax.add_patch(Rectangle((k - width / 2, q25), width, q75 - q25, facecolor=fc, edgecolor=ec, lw=0.8, zorder=2))
    ax.plot([k - width / 2, k + width / 2], [q50, q50], color='white' if not hollow else INK, lw=1.0, zorder=3)
    ax.plot([k, k], [q5, q25], color=ec, lw=0.8, zorder=2)
    ax.plot([k, k], [q75, q95], color=ec, lw=0.8, zorder=2)
    ax.plot([k], [mean], marker='+', ms=4, color=INK if hollow else 'white', mew=0.9, zorder=4)
    return st


def fig_p3_per_am(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 2, left=0.46, gap=0.42, top=0.44)
    rows = []
    a, b = axs
    lab_dy = 0.022
    area = {bed: [float(r['area_am_se_um2']) for r in data[bed]['per_am']] for bed in R.BED_ORDER if bed in data}
    cov_h = {bed: [float(r['coverage_hertz_pct']) for r in data[bed]['per_am']] for bed in area}
    cov_p = {bed: [float(r['coverage_physics_union_pct']) for r in data[bed]['per_am'] if r['coverage_physics_union_pct'] != '']
             for bed in area}
    # 범위 = 수염 위끝 (95 %) · 평균 표지 + (a) 중앙값 글 자리 — 고정 범위 없음
    a_items, b_items = [(0.0, 0.0, 0.0)], [(0.0, 0.0, 0.0)]
    for bed in area:
        st = _box_stats(area[bed])
        a_items += [(st['p95'], 0.0, LAB_PAD_PT), (st['mean'], 0.0, 2.0 + LAB_PAD_PT), (st['p95'], lab_dy, lab_h_pt(VAL_PT))]
        for xs in (cov_h[bed], cov_p[bed]):
            st = _box_stats(xs)
            b_items += [(st['p95'], 0.0, LAB_PAD_PT), (st['mean'], 0.0, 2.0 + LAB_PAD_PT)]
    a_lo, a_hi, a_ticks = fit_axis(a, 'y', a_items, zero=True)
    set_axis(a, 'y', a_lo, a_hi, a_ticks)
    set_axis(b, 'y', *fit_axis(b, 'y', b_items, zero=True))
    for k, bed in enumerate(R.BED_ORDER):
        if bed not in data:
            placeholder(a, k, width=0.5)
            placeholder(b, k, width=0.62)
            rows += [dict(panel='a_area_per_am', bed=bed, status=WAIT), dict(panel='b_coverage_per_am', bed=bed, status=WAIT)]
            continue
        st = _box(a, k, area[bed], SIZE_C[bed], width=0.42)
        a.text(k, st['p95'] + (a_hi - a_lo) * lab_dy, fmt_v(st['median'], 3), ha='center', va='bottom', fontsize=VAL_PT, color=INK)
        rows.append(dict(panel='a_area_per_am', bed=bed, status='ok', quantity='AM–SE contact area per AM (µm², c_cpl[22])', **st))
        sh = _box(b, k - 0.17, cov_h[bed], SIZE_C[bed], width=0.28)
        sp = _box(b, k + 0.17, cov_p[bed], SIZE_C[bed], width=0.28, hollow=True)
        rows.append(dict(panel='b_coverage_per_am', bed=bed, status='ok', quantity='coverage Hertz-family per AM (%)', **sh))
        rows.append(dict(panel='b_coverage_per_am', bed=bed, status='ok', quantity='coverage Physics union cap per AM (%)', **sp))
    for ax in axs:
        size_axis(ax)
        ygrid(ax)
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
    rows = [dict(panel='a_geometric', **r) for r in bars(axs[0], data, 'tau_geo_all')]
    axs[0].set_ylabel('기하 tortuosity (최단 경로 / Δz)', labelpad=2)
    axs[0].set_title('(a) 기하 tortuosity', loc='left', pad=3)
    rows += [dict(panel='b_transport', **r) for r in bars(axs[1], data, 'tau2_ion_hertz', phys_key='tau2_ion_physics')]
    axs[1].set_ylabel(f'수송 tortuosity ({TAU_TR})', labelpad=2)
    axs[1].set_title('(b) 수송 tortuosity', loc='left', pad=3)
    top_legend(fig, [('bar', SIZE_C['D2'], 'Hertz (주)'), ('hollow', None, 'Physics (민감도)'), ('text', None, '두 양 = 다른 정의 · 비로 묶지 않음')],
               0.13, h)
    return save(fig, 'p4_tortuosity', rows, ['panel', 'bed', 'status', 'value', 'physics'], meta)


def fig_p4_f_connect(data, meta):
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, 2, left=0.50, gap=0.46, top=0.44)
    rows = [dict(panel='a_f_ion', **r) for r in bars(axs[0], data, 'f_ion_hertz', phys_key='f_ion_physics')]
    axs[0].set_ylabel(F_ION, labelpad=2)
    axs[0].set_title('(a) 구조 전달계수 f', loc='left', pad=3)
    rows += [dict(panel='b_se_connected_am', **r) for r in bars(axs[1], data, 'se_connected_am_pct')]
    axs[1].set_ylabel('SE 망과 연결된 AM (%)', labelpad=2)
    axs[1].set_title('(b) SE 망 연결 AM (연결성 기준)', loc='left', pad=3)
    top_legend(fig, [('bar', SIZE_C['D2'], 'Hertz (주)'), ('hollow', None, 'Physics (민감도)'), ('hatch', None, WAIT)], 0.13, h, x_in=0.50)
    return save(fig, 'p4_f_connect', rows, ['panel', 'bed', 'status', 'value', 'physics'], meta)


# ───────────────────────────── p6 — 두께 방향 ─────────────────────────────

MS_Z = 2.6                          # z 구간 표지 크기 (pt)


def _zfig(data, specs, stem, meta, xlabels, legend_extra):
    """z 구간 그림 — 가로 범위 · 눈금 = 자료 (값 + 띠 + 표지 자리 · spec['zero'] = 0 부터) · 세로 = 0 → 가장 높은 판 + 10 µm."""
    w, h = W_HALF, 2.80
    fig = plt.figure(figsize=(w, h))
    axs = frame(fig, w, h, len(specs), left=0.50, gap=0.30, top=0.44)
    rows = []
    zmax = max([float(data[b]['zprof'][-1]['z_hi_um']) for b in data] + [130.0])
    for i, (ax, spec) in enumerate(zip(axs, specs)):
        xs = [fnum(r[c]) for b in data for r in data[b]['zprof'] for c in (spec['key'],) + tuple(spec.get('band', ()))]
        xs = [x for x in xs if x is not None and math.isfinite(x)]
        pad = MS_Z / 2 + LAB_PAD_PT
        set_axis(ax, 'x', *fit_axis(ax, 'x', [(max(xs), 0.0, pad)], [(min(xs), 0.0, pad)], zero=spec.get('zero', False)))
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
            ax.plot(v, z, color=SIZE_C[bed], lw=1.2, marker='o', ms=MS_Z, zorder=3)
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
        ax.set_yticks([t for t in range(0, int(zmax + 10) + 1, 40)])      # 1쪽 띠 그림과 같은 z 눈금 간격
        ax.set_xlabel(xlabels[i], labelpad=2)
        ax.set_title(spec['title'], loc='left', pad=3)
        ax.xaxis.grid(True, color=GRID, lw=0.5)
        ax.set_axisbelow(True)
        if i:
            ax.set_yticklabels([])
        else:
            ax.set_ylabel('z (µm)', labelpad=2)
    items = [('line', SIZE_C[b], f'{b[1:]} µm') for b in R.BED_ORDER if b in data]
    wt = waiting_beds(data)
    items += [('text', None, wt)] if wt else []
    items += [('dotted', INK2, '판 높이')] + legend_extra
    top_legend(fig, items, 0.13, h, x_in=0.50)
    cols = ['panel', 'bed', 'z_lo_um', 'z_hi_um', 'z_mid_um', 'value', 'band_lo', 'band_hi'] + sorted({e for s in specs for e in s.get('extra', ())})
    return save(fig, stem, rows, cols, meta)


def fig_p6(data, meta):
    s1 = _zfig(data, [dict(panel='a_local_porosity_union', key='por_union_pct', title='(a) 국소 기공률 (정확 합집합)',
                           extra=('por_union_se_pct', 'n_mc')),
                      dict(panel='b_se_connected_am', key='am_connected_pct', title='(b) SE 망 연결 AM', extra=('am_n',), zero=True)],
               'p6_z_structure', meta, ['국소 기공률 (%)', 'SE 망과 연결된 AM (%)'], [('text', None, 'z 10 구간')])
    s2 = _zfig(data, [dict(panel='a_lw_am', key='lw_am_median_MPa', title='(a) AM 입자 응력', band=('lw_am_q25_MPa', 'lw_am_q75_MPa'),
                           extra=('lw_am_n', 'lw_am_wall_excluded'), zero=True),
                      dict(panel='b_lw_se', key='lw_se_median_MPa', title='(b) SE 입자 응력', band=('lw_se_q25_MPa', 'lw_se_q75_MPa'),
                           extra=('lw_se_n', 'lw_se_wall_excluded'), zero=True)],
               'p6_z_stress', meta, [f'{SVM} Love–Weber (MPa)', f'{SVM} Love–Weber (MPa)'], [('text', None, '선 중앙값 · 띠 25–75 %')])
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
        ax.text(-0.08, y + 0.5, name, ha='right', va='center', fontsize=NOTE_PT + 0.5, color=INK, transform=ax.transData,
                gid=GID_OUTSIDE_OK)
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
        ax.text(k + 0.5, n + 0.15, f'SE {bed[1:]} µm', ha='center', va='bottom', fontsize=LABEL_PT, color=INK, gid=GID_OUTSIDE_OK)
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
        # 둥근 상자 (pad 0.22 × 6 pt ≈ 1.3 pt + 선 0.5) 가 축 안에 들도록 오른쪽 위 모서리에서 2.5 pt 안쪽
        ax.annotate(f'문헌 {spec["dir"]} [{refs}]', xy=(1, 1), xycoords='axes fraction', xytext=(-2.5, -2.5), textcoords='offset points',
                    ha='right', va='top', fontsize=NOTE_PT, color=INK,
                    bbox=dict(boxstyle='round,pad=0.22', fc='#F2F2F2', ec='#BFBFBF', lw=0.5))
    fig.text(0.5, 0.64 / h, 'SE D50 (µm)', ha='center', va='center', fontsize=LABEL_PT, color=INK)
    fig.text(left / w, 0.47 / h, '문헌 화살표 = 작은 SE 쪽의 방향 (정본 litdb 카드) · 우리 값은 나란히만 (일치 판정 아님) · 시드 1 · 단분산 (PSD 폭 그대로)',
             ha='left', va='center', fontsize=NOTE_PT - 0.5, color=INK2)
    items = [f'[{j}] {s}' for j, s in CARDS.items()]
    for li, k0 in enumerate(range(0, len(items), 2)):
        fig.text(left / w, (0.32 - 0.12 * li) / h, '   '.join(items[k0:k0 + 2]), ha='left', va='center', fontsize=NOTE_PT - 1.0, color=INK2)
    return save(fig, 'p7_lit_direction', rows, ['quantity', 'name', 'bed', 'status', 'value', 'literature_direction_small_se', 'cards'], meta)


# ───────────────────────────── 진단 — 이완 강하 ↔ 입자 수 (원장 DEMP-01 관계) ─────────────────────────────

_NUM = r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)'
_THERMO5 = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$')
DIAG_EST_LABEL = '어림 γNv/(2A) (affine 가정)'


def _one_idx(L, pattern, what, case):
    hits = [i for i, l in enumerate(L) if re.fullmatch(pattern, l.strip())]
    src.need(len(hits) == 1, f'deck {case}: {what} — 실행 줄 {len(hits)} 개 (정확히 하나여야 한다)')
    return hits[0]


def deck_drag(text, case):
    """덱 실행 줄 → 압축 중 감쇠 γ · 판 속도 v · 압력 면적 A · 압력 나눗수 (덱 단위) — 단계 위치 · 줄 수 대조 (어긋나면 멈춘다).
    γ = 압축 (PHASE 3 시작 → 판 정지) 앞의 마지막 `fix damp all viscous` (PHASE 2 안) · 압축 구간에 감쇠를 바꾸는 줄 없음 ·
    A · 나눗수 = 판 정지 판정 식 `current_press = abs(f_top_mesh[3]) / A / 나눗수` (PHASE 2 `pressMPa` 와 같아야 · A = 상자 x × y)."""
    L = src.exec_lines(text)
    i2 = _one_idx(L, r'print\s+"====== PHASE 2: STABILIZE ======"', 'PHASE 2 표지', case)
    i3 = _one_idx(L, r'print\s+"====== PHASE 3: COMPRESSION \(Speed [0-9.eE+-]+\) ======"', 'PHASE 3 표지', case)
    i_loop = _one_idx(L, r'label\s+loop_press', 'label loop_press', case)
    i_stop = _one_idx(L, r'unfix\s+move_press', 'unfix move_press', case)
    i4 = _one_idx(L, r'print\s+"====== PHASE 4: RELAXATION ======"', 'PHASE 4 표지', case)
    src.need(i2 < i3 < i_loop < i_stop < i4, f'deck {case}: 단계 순서 (PHASE 2 < 3 < loop < 판 정지 < 4) 가 아니다')
    damp = []
    for i, l in enumerate(L):
        m = re.fullmatch(rf'fix\s+damp\s+all\s+viscous\s+{_NUM}', l.strip())
        if m:
            damp.append((i, float(m.group(1))))
        elif re.fullmatch(r'unfix\s+damp', l.strip()) or re.fullmatch(r'fix\s+damp\s+.*', l.strip()):
            damp.append((i, None))
    src.need(all(not (i3 <= i <= i_stop) for i, _ in damp), f'deck {case}: 압축 구간 안에 감쇠를 바꾸는 줄이 있다')
    before = [(i, g) for i, g in damp if i < i3]
    src.need(before and before[-1][0] > i2 and before[-1][1] is not None,
             f'deck {case}: 압축 앞 마지막 감쇠 줄이 PHASE 2 의 `fix damp all viscous` 가 아니다')
    after = [(i, g) for i, g in damp if i > i_stop and g is not None]
    src.need(len(after) == 1 and after[0][0] > i4, f'deck {case}: PHASE 4 감쇠 줄이 하나가 아니다')
    v = float(re.fullmatch(rf'variable\s+press_speed\s+equal\s+{_NUM}', L[_one_idx(L, rf'variable\s+press_speed\s+equal\s+{_NUM}', 'press_speed', case)].strip()).group(1))
    _one_idx(L, r'fix\s+move_press\s+all\s+move/mesh\s+mesh\s+top_mesh\s+linear\s+0\.0\s+0\.0\s+-\$\{press_speed\}', 'move_press (−press_speed)', case)
    pat_cp = rf'variable\s+current_press\s+equal\s+"abs\(f_top_mesh\[3\]\)\s*/\s*{_NUM}\s*/\s*{_NUM}"'
    i_cp = _one_idx(L, pat_cp, 'current_press 식', case)
    src.need(i_loop < i_cp < i_stop, f'deck {case}: current_press 식이 압축 고리 밖')
    A, div = (float(x) for x in re.fullmatch(pat_cp, L[i_cp].strip()).groups())
    pat_pm = rf'variable\s+pressMPa\s+equal\s+abs\(f_top_mesh\[3\]\)\s*/\s*{_NUM}\s*/\s*{_NUM}'
    pm = tuple(float(x) for x in re.fullmatch(pat_pm, L[_one_idx(L, pat_pm, 'pressMPa 식', case)].strip()).groups())
    src.need(pm == (A, div), f'deck {case}: pressMPa 식 {pm} ≠ current_press 식 {(A, div)}')
    bx = src.parse_deck(text, case)['box_sim']
    src.need(abs((bx[1] - bx[0]) * (bx[3] - bx[2]) - A) <= 1e-12 * A, f'deck {case}: 압력 면적 {A} ≠ 상자 x × y')
    return dict(gamma=before[-1][1], gamma_relax=after[0][1], v=v, A=A, div=div)


def deck_plan_n(text, case):
    """덱 머리 줄 '예상 입자 수 (질량분율 규약): AM_P a · SE b (합 N)' → (AM, SE, 합) — 합 = AM + SE = 삽입 검사 줄의 계획 수 (parse_deck)."""
    m = re.findall(r'^#\s*예상 입자 수 \(질량분율 규약\): AM_P ([\d,]+) · SE ([\d,]+) \(합 ([\d,]+)\)', text, flags=re.M)
    src.need(len(m) == 1, f'deck {case}: "예상 입자 수 … (합 N)" 머리 줄 {len(m)} 개')
    am, se, tot = (int(x.replace(',', '')) for x in m[0])
    d = src.parse_deck(text, case)
    src.need(am + se == tot and (tot, am, se) == (d['n_total_plan'], d['n_am_plan'], d['n_se_plan']),
             f'deck {case}: 머리 줄 ({am} · {se} · 합 {tot}) ≠ 삽입 검사 줄 ({d["n_am_plan"]} · {d["n_se_plan"]} · {d["n_total_plan"]})')
    return dict(n_plan=tot, n_am_plan=am, n_se_plan=se, am_gate=d['am_gate'], se_gate=d['se_gate'])


def stop_line(text, case, stop_step, p_t0minus_mpa):
    """압축 로그의 정지 줄 = PHASE 3 마지막 run 의 마지막 정규 thermo 줄 (step atoms ke cpu pressMPa · run 첫 setup 줄 뺌 ·
    make_fig_p2_aux.parse_log 과 같은 run 나눔) → (atoms, 줄 글).  step = 기록 정지 step · 압력 × 1000 = 기록 t = 0⁻ 이어야 한다."""
    src.need(f'====== Simulation Finished! ({case.upper()}:' in text, f'log: {case} 끝 줄이 없다 (다른 침대 로그?)')
    lines = text.split('\n')
    i3 = lines.index('====== PHASE 3: COMPRESSION (Speed 0.01) ======')
    i4 = lines.index('====== PHASE 4: RELAXATION ======')
    last, in_run, setup_seen = None, False, False
    for l in lines[i3:i4]:
        if l.lstrip().startswith('Step') and 'pressMPa' in l:
            in_run, setup_seen = True, False
            continue
        if l.startswith('Loop time of'):
            in_run = False
            continue
        m = _THERMO5.match(l) if in_run else None
        if m:
            if not setup_seen:
                setup_seen = True
            else:
                last = (int(m.group(1)), int(m.group(2)), float(m.group(5)), l.strip())
    src.need(last is not None, f'log {case}: PHASE 3 정규 thermo 줄이 없다')
    step, atoms, p_sim, txt = last
    src.need(step == stop_step, f'log {case}: 정지 줄 step {step} ≠ 기록 정지 step {stop_step}')
    src.need(abs(p_sim * src.P_SIM_TO_MPA - p_t0minus_mpa) <= 1e-9 * p_t0minus_mpa, f'log {case}: 정지 줄 압력 ≠ 기록 t = 0⁻')
    return atoms, txt


def stop_n(bed, rec, plan):
    """판 정지 때 입자 수 N — ① 압축 로그 정지 줄의 atoms (로그가 리포 안에 있고 sha256 = metrics 기록일 때) ② 아니면 끝 덤프의 AM + SE
    (덱: 이완 중 입자를 넣거나 빼는 줄 없음 · 로그 있는 침대에서 ① = ② 를 따로 적는다).  N 은 덱 머리 줄 계획과 맞아야 한다 (덱 삽입 구간)."""
    comp, inv = rec['compaction'], rec['inventory']
    n_end = inv['n_am'] + inv['n_se']
    log = comp.get('log') or ''
    p = REPO / log
    got = None
    if log and not Path(log).is_absolute() and p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == comp['log_sha256']:
        atoms, txt = stop_line(p.read_text(encoding='utf-8', errors='strict'), R.CASE[bed], comp['stop_step'], rec['metrics']['p_t0minus_MPa'])
        got = dict(n=atoms, source=f'압축 로그 정지 줄 ({log} · step {comp["stop_step"]})', stop_line=txt, log_sha256=comp['log_sha256'])
    else:
        got = dict(n=n_end, source='끝 덤프 AM + SE (압축 로그가 리포에 없음 — metrics 기록 경로 리포 밖)', stop_line='', log_sha256=comp.get('log_sha256'))
    lo_g = plan['am_gate'][0] + plan['se_gate'][0]
    hi_g = plan['am_gate'][1] + plan['se_gate'][1]
    src.need(lo_g <= got['n'] <= hi_g, f'{bed}: N {got["n"]} 이 덱 계획 {plan["n_plan"]} 의 삽입 구간 [{lo_g}, {hi_g}] 밖')
    src.need(plan['am_gate'][0] <= inv['n_am'] <= plan['am_gate'][1] and plan['se_gate'][0] <= inv['n_se'] <= plan['se_gate'][1],
             f'{bed}: 끝 덤프 상별 수가 덱 삽입 구간 밖')
    got['n_end_dump'] = n_end
    return got


def fig_diag_relax_drop(data, decks, meta):
    """진단 — 판 고정 이완 강하 Δp = p(t = 0⁻) − p(이완 끝) ↔ 판 정지 때 입자 수 N (로그 · 로그) + 어림 γNv/(2A) (affine 가정 · 덱 값) ·
    D0.7 덱 계획 N (세로 점선) · 가압 목표 (가로 점선).  원장 DEMP-01 관계 (감쇠 저항 몫 ≈ N/300,000) — 그 이상은 주장하지 않는다."""
    w, h = W_HALF, 2.55
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0.58 / w, 0.42 / h, (w - 0.58 - 0.10) / w, (h - 0.42 - 0.34) / h])
    ax.set_xscale('log')
    ax.set_yscale('log')
    target = target_mpa(data)
    drag, plans = {}, {}
    for bed in R.BED_ORDER:
        rec = decks[bed]
        text = src.rp(rec['deck']).read_text(encoding='utf-8')
        src.need(src.sha256_bytes(text.encode('utf-8')) == rec['sha256'], f'{bed}: 덱 sha256 ≠ manifest (load_all 대조와 다르다)')
        drag[bed], plans[bed] = deck_drag(text, rec['case']), deck_plan_n(text, rec['case'])
    par = {(d['gamma'], d['v'], d['A'], d['div']) for d in drag.values()}
    src.need(len(par) == 1, f'덱마다 γ · v · A · 나눗수가 다르다 ({par}) — 한 직선으로 그릴 수 없다')
    g, v, A, div = par.pop()
    c = g * v / (2.0 * A) / div * src.P_SIM_TO_MPA          # MPa (보고) / 입자
    pts = {}
    for bed in R.BED_ORDER:
        if bed in data:
            m = data[bed]['m']
            sn = stop_n(bed, data[bed]['rec'], plans[bed])
            pts[bed] = dict(n=sn['n'], dp=m['p_t0minus_MPa'] - m['p_end_MPa'], sn=sn)
    plan_beds = [b for b in R.BED_ORDER if b not in data]
    # 범위 (log10) = 점 · 점 글 · 어림 직선의 계획 점 · 목표 + 글 자리 — 고정 범위 없음
    labs = {b: f'{b[1:]} µm {fmt_v(p["dp"], 3)}' for b, p in pts.items()}
    above = {b: p['dp'] > c * p['n'] for b, p in pts.items()}          # 직선 위 점 = 글 왼쪽 위 · 아래 점 = 오른쪽 아래
    x_hi, x_lo, y_hi, y_lo = [], [], [], []
    for b, p in pts.items():
        lw = 4.0 + text_w_pt(fig, labs[b], VAL_PT) + LAB_PAD_PT
        x, y = math.log10(p['n']), math.log10(p['dp'])
        (x_lo if above[b] else x_hi).append((x, 0.0, lw))
        (y_hi if above[b] else y_lo).append((y, 0.0, 3.0 + lab_h_pt(VAL_PT)))
        x_lo.append((x, 0.0, 2.5 + LAB_PAD_PT))
        x_hi.append((x, 0.0, 2.5 + LAB_PAD_PT))
        y_lo.append((min(y, math.log10(c * p['n'])), 0.0, 2.5 + LAB_PAD_PT))
    for b in plan_beds:
        n_plan = plans[b]['n_plan']
        x_hi.append((math.log10(n_plan), 0.0, MS_PHYS / 2 + LAB_PAD_PT))
        y_hi.append((math.log10(c * n_plan), 0.0, 3.0 + lab_h_pt(VAL_PT)))
        x_lo.append((math.log10(n_plan), 0.0, 3.0 + text_w_pt(fig, f'{b} 덱 계획 N', VAL_PT) + LAB_PAD_PT))
    y_hi.append((math.log10(target), 0.0, 1.0 + lab_h_pt(VAL_PT)))
    xl0, xl1, _ = fit_axis(ax, 'x', x_hi, x_lo, snap=False, min_n=1, max_n=99)
    yl0, yl1, _ = fit_axis(ax, 'y', y_hi, y_lo, snap=False, min_n=1, max_n=99)
    ax.set_xlim(10 ** xl0, 10 ** xl1)
    ax.set_ylim(10 ** yl0, 10 ** yl1)
    # 어림 직선 = 축 안 구간만 (끝점이 축 경계)
    n0, n1 = max(10 ** xl0, 10 ** yl0 / c), min(10 ** xl1, 10 ** yl1 / c)
    ax.plot([n0, n1], [c * n0, c * n1], color=INK2, lw=1.0, zorder=2)
    ax.axhline(target, color=PH, lw=0.8, ls=(0, (1.5, 1.2)), zorder=1)
    ax.annotate(f'목표 {src.fmt_g(target)} MPa', xy=(10 ** xl0, target), xytext=(3.0, 1.0), textcoords='offset points', fontsize=VAL_PT,
                color=INK2, ha='left', va='bottom')
    rows = []
    for b in plan_beds:
        n_plan = plans[b]['n_plan']
        ax.axvline(n_plan, color=INK2, lw=0.7, ls=(0, (3, 2)), zorder=1)
        ax.annotate(f'{b} 덱 계획 N', xy=(n_plan, 10 ** yl0), xytext=(-3.0, 3.0), textcoords='offset points', fontsize=VAL_PT, color=INK2,
                    ha='right', va='bottom')
        ax.plot([n_plan], [c * n_plan], marker='o', ms=MS_PHYS, mfc='white', mec=INK2, mew=0.9, ls='none', zorder=4)
        ax.annotate(f'어림 {fmt_v(c * n_plan, 3)}', xy=(n_plan, c * n_plan), xytext=(-4.0, 3.0), textcoords='offset points', fontsize=VAL_PT,
                    color=INK2, ha='right', va='bottom')
        rows.append(dict(bed=b, status=WAIT, n_deck_plan=n_plan, dp_est_MPa=c * n_plan, n_source='덱 머리 줄 계획 (합 N)'))
    for b, p in pts.items():
        ax.plot([p['n']], [p['dp']], marker='o', ms=4.5, mfc=SIZE_C[b], mec=SIZE_C[b], mew=0.0, ls='none', zorder=4)
        xt, ha, va = ((-4.0, 3.0), 'right', 'bottom') if above[b] else ((4.0, -3.0), 'left', 'top')
        ax.annotate(labs[b], xy=(p['n'], p['dp']), xytext=xt, textcoords='offset points', fontsize=VAL_PT, color=INK, ha=ha, va=va)
        m = data[b]['m']
        rows.append(dict(bed=b, status='ok', n_particles=p['n'], n_source=p['sn']['source'], stop_line=p['sn']['stop_line'],
                         n_end_dump=p['sn']['n_end_dump'], n_deck_plan=plans[b]['n_plan'], n_minus_plan=p['n'] - plans[b]['n_plan'],
                         stop_step=data[b]['rec']['compaction']['stop_step'], log_sha256=p['sn']['log_sha256'],
                         p_t0minus_MPa=m['p_t0minus_MPa'], p_end_MPa=m['p_end_MPa'], dp_MPa=p['dp'], dp_est_MPa=c * p['n'],
                         dp_over_est=p['dp'] / (c * p['n'])))
    for r in rows:
        r.update(gamma_deck=g, gamma_relax_deck=drag[r['bed']]['gamma_relax'], press_speed_deck=v, area_deck=A, press_divisor_deck=div,
                 report_MPa_per_deck_MPa=src.P_SIM_TO_MPA, est_MPa_per_particle=c, deck=decks[r['bed']]['deck'], deck_sha256=decks[r['bed']]['sha256'])
    rows.sort(key=lambda r: R.BED_ORDER.index(r['bed']))
    ax.set_xlabel('판 정지 때 입자 수 N', labelpad=2)
    ax.set_ylabel('이완 강하 Δp (MPa)', labelpad=2)
    ax.yaxis.grid(True, which='major', color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    top_legend(fig, [('dot', SIZE_C['D2'], '측정 Δp = p(t = 0⁻) − p(이완 끝)'), ('line', INK2, DIAG_EST_LABEL)], 0.14, h, x_in=0.58)
    cols = ['bed', 'status', 'n_particles', 'n_source', 'stop_step', 'stop_line', 'log_sha256', 'n_end_dump', 'n_deck_plan', 'n_minus_plan',
            'p_t0minus_MPa', 'p_end_MPa', 'dp_MPa', 'dp_est_MPa', 'dp_over_est', 'gamma_deck', 'gamma_relax_deck', 'press_speed_deck',
            'area_deck', 'press_divisor_deck', 'report_MPa_per_deck_MPa', 'est_MPa_per_particle', 'deck', 'deck_sha256']
    return save(fig, 'diag_relax_drop_vs_N', rows, cols, meta)


def check_report():
    """검사 결과 → (줄 목록, 문제 수)."""
    res = CHECK['results']
    out, n_bad = [], 0
    for stem, r in res.items():
        c = r['counts']
        tag = 'PASS' if not r['problems'] else f'FAIL {len(r["problems"])}'
        out.append(f'{stem:24s} {tag:8s} 점 {c["points"]} · 막대/상자 {c["patches"]} · 띠 꼭짓점 {c["band_vertices"]} · '
                   f'축 글 {c["texts"]} · 그림 글 {c["fig_texts"]} · 자른 모음 (검사 밖) {c["cropped_collections"]}')
        out += [f'    ✗ {p}' for p in r['problems']]
        n_bad += len(r['problems'])
    out.append(f'검사: 그림 {len(res)} · 문제 {n_bad} → {"PASS" if not n_bad else "FAIL"}')
    return out, n_bad


def build_all(write=True):
    CHECK['write'] = write
    CHECK['results'] = {}
    setup_fonts()
    data, decks = load()
    CHECK['beds_with_data'] = tuple(b for b in R.BED_ORDER if b in data)
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
    fig_diag_relax_drop(data, decks, meta)
    lines, n_bad = check_report()
    if not write:
        return dict(check_lines=lines, n_problems=n_bad)
    beds = {b: ('ok' if b in data else WAIT) for b in R.BED_ORDER}
    out = dict(generator='docs/50kg/report_y4/draft2/make_draft2_figs.py', matplotlib=matplotlib.__version__, dpi=DPI, beds=beds,
               metrics_sha256={b: hashlib.sha256((R.DATA / b / f'metrics_{b}.json').read_bytes()).hexdigest() for b in data},
               colors=dict(AM=AM_C, SE=SE_C, size=SIZE_C, placeholder=PH), fonts=FONTS, figures=meta,
               check=dict(status='PASS' if not n_bad else 'FAIL', n_problems=n_bad,
                          counts={k: v['counts'] for k, v in CHECK['results'].items()}))
    (OUT / 'figs_meta.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for k, v in meta.items():
        print(f'{k:22s} {v["size_in"]} in · {v["px"]} px · dpi {v["dpi"]} · rows {v["csv_rows"]}')
    return dict(out, check_lines=lines, n_problems=n_bad)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description='50kg 4차년도 초안 2 그림 (PNG · SVG · CSV · figs_meta.json) + 그림 검사')
    ap.add_argument('--check', action='store_true',
                    help='그림을 그려 검사만 한다 (파일을 쓰지 않음) — 자료가 축 범위 안 · 축 글이 축 안 · 제목 · 다른 글과 안 겹침 · 문제 있으면 rc 1')
    a = ap.parse_args(argv)
    res = build_all(write=not a.check)
    print('\n'.join(res['check_lines']))
    return 1 if res['n_problems'] else 0


if __name__ == '__main__':
    sys.exit(main())
