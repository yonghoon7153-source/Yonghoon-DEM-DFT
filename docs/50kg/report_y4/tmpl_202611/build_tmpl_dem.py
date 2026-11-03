#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""50kg 4차년도 보고 덱 (2026.11 양식) — DEM 장 생성기.

1저자 양식 pptx (리포 밖 · 읽기 전용) 에 DEM 장을 채운다.  양식의 글꼴 · 스타일 · 이야기는 그대로 두고 값만 바꾼다.
  6      새 장 (양식 5장 뒤) : D_SE = 1 µm 가압 거동 — 3단 시간 그림 + 기공 렌더 4 칸 (마지막 칸 = 빈 칸)
  7      양식 6장            : 입도 1 / 2 / 3 µm — 렌더 · 경로 그림 칸 비움 · 막대 (Origin OLE → PNG) · 기하 tortuosity
  8–11   새 장 (입도 묶음)    : 미세구조 비교 / 지표 변화 / 응력 분포 (이완 후) / 이온전도도 변화
  12     양식 7장            : E_SE = 11 / 22 / 33 GPa — 렌더 칸 비움 · 두께 + 기공도 막대 · 수송 tortuosity
  13–16  새 장 (영률 묶음)    : 같은 네 장
이미지 칸 (점선 사각형) = 1저자가 웹앱 렌더를 붙이는 자리.  막대 그림마다 Origin 용 CSV 를 함께 쓴다.

사용:
  python3 build_tmpl_dem.py --template T.pptx --d1-fig D1_3panel.png \
      --render-init 25.webp --render-50 24.webp --render-300 23.webp \
      --skill-dir <pptx skill dir> --work-dir W --out-dir O \
      [--values-csv values_D123.csv] [--metrics-modulus metrics_modulus.csv]
값 = 아래 SIZE · MOD (출처 주석).  --values-csv · --metrics-modulus 를 주면 원자료와 대조하고 어긋나면 멈춘다.
"""
import argparse
import csv
import random
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle, Patch  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from lxml import etree  # noqa: E402

# --------------------------------------------------------------------------- values
# 입도 절 (D_SE = 1 / 2 / 3 µm) — docs/50kg/report_y4/meeting_20261104/values/values_D123.csv
#   + docs/50kg/report_y4/draft2/metrics_all.csv (같은 침대 · 같은 값)
SIZE = dict(
    key='DSE', sym=('D', 'SE'), unit='µm', cats=['1', '2', '3'],
    thickness=[124.57, 126.83, 131.50],      # 질량 보존 두께 (µm)
    porosity=[18.1, 19.6, 22.4],             # 기공도 (정확 합집합, %)
    coverage=[46.8, 54.2, 52.6],             # AM coverage (Physics 합집합, %)
    tau2=[6.00, 8.26, 13.63],                # 수송 tortuosity = φ_SE·σ₀/σ_eff (제곱근 아님)
    tau_geo=[1.22, 1.28, 1.37],              # 기하 tortuosity (최단 경로 / 두께)
    sigma=[0.0702, 0.0501, 0.0293],          # σ_Li+ (σ₀ = 1.5 mS/cm, Hertz) mS/cm
    p_end=[156, 280, 291],                   # 이완 끝 가압판 압력 (MPa)
    am_med=[172, 335, 355], se_med=[76, 126, 149],   # 이완 후 von Mises 중앙값 (벽 접촉 제외, MPa)
)
# 영률 절 (2 µm SE · E_SE = 11 / 22 / 33 GPa = 22 GPa 의 ×0.5 / ×1 / ×1.5 · DEM 유효 입력 0.675 / 1.35 / 2.025 GPa)
#   — draft2 metrics (D2) + 영률 침대 기록 metrics_D2E05.json · metrics_D2E15.json (metrics_modulus.csv)
MOD = dict(
    key='ESE', sym=('E', 'SE'), unit='GPa', cats=['11', '22', '33'],
    thickness=[123.61, 126.83, 129.39],
    porosity=[17.5, 19.6, 21.2],
    coverage=[61.3, 54.2, 48.1],
    tau2=[7.80, 8.26, 9.05],
    tau_geo=[1.28, 1.28, 1.30],              # tau_geo_all (metrics_D2E05 · metrics_D2 · metrics_D2E15)
    sigma=[0.0544, 0.0501, 0.0448],
    p_end=[278, 280, 280],
    am_med=[353, 335, 326], se_med=[85, 126, 152],
    dem_E=['0.675', '1.35', '2.025'],
)
D1 = dict(z0=145.45, z1=122.60, v=10, p_peak=300.6, t_peak=2685, p_relax=156.2, t_relax=2785, p_dump50=53)


def verify(values_csv, metrics_modulus, tau_geo_json=None):
    """원자료와 대조 (반올림 자리까지)."""
    bad = []
    if values_csv:
        rows = list(csv.reader(open(values_csv, encoding='utf-8-sig')))
        rowmap = {r[1].strip(): r for r in rows[1:]}

        def col(label):          # 파일 열 순서 = 3 µm, 2 µm, 1 µm → 1, 2, 3 으로
            r = rowmap[label]
            return [r[5], r[4], r[3]]
        checks = [('질량 보존 두께', SIZE['thickness'], 2), ('기공도 (정확 합집합)', SIZE['porosity'], 1),
                  ('AM coverage', SIZE['coverage'], 1), ('수송 tortuosity', SIZE['tau2'], 2),
                  ('기하 tortuosity (최단 경로 / 두께)', SIZE['tau_geo'], 2),
                  ('유효 이온전도도 σ_Li+ (σ₀ = 1.5 mS/cm)', SIZE['sigma'], 4),
                  ('이완 끝 판 압력', SIZE['p_end'], 0),
                  ('NCM von Mises 응력 중앙값 (벽 접촉 제외)', SIZE['am_med'], 0),
                  ('SE von Mises 응력 중앙값 (벽 접촉 제외)', SIZE['se_med'], 0)]
        for label, want, nd in checks:
            got = [round(float(x), nd) for x in col(label)]
            if [round(float(w), nd) for w in want] != got:
                bad.append((label, want, got))
    if metrics_modulus:
        rows = {r['bed']: r for r in csv.DictReader(open(metrics_modulus, encoding='utf-8-sig'))}
        order = ['D2E05', 'D2', 'D2E15']
        def g(k, nd, f=1.0):
            return [round(float(rows[b][k]) * f, nd) for b in order]
        for k, want, nd, f in (('eps_union_exact_pct', MOD['porosity'], 1, 1.0),
                               ('coverage_physics_union_pct', MOD['coverage'], 1, 1.0),
                               ('tau2_ion_hertz', MOD['tau2'], 2, 1.0),
                               ('f_ion_hertz', MOD['sigma'], 4, 1.5),
                               ('p_end_MPa', MOD['p_end'], 0, 1.0),
                               ('lw_am_nowall_median_MPa', MOD['am_med'], 0, 1.0),
                               ('lw_se_nowall_median_MPa', MOD['se_med'], 0, 1.0)):
            got = g(k, nd, f)
            if [round(w, nd) for w in want] != got:
                bad.append((k, want, got))
    if tau_geo_json:              # 영률 절 기하 tortuosity — E05 · D2 · E15 순서
        import json
        got = [round(float(json.load(open(f))['metrics']['tau_geo_all']), 2) for f in tau_geo_json]
        if got != [round(v, 2) for v in MOD['tau_geo']]:
            bad.append(('tau_geo_all', MOD['tau_geo'], got))
    if bad:
        for b in bad:
            print('VALUE MISMATCH', b, file=sys.stderr)
        sys.exit(2)
    print('values verified' if (values_csv or metrics_modulus or tau_geo_json) else
          'values not verified (no source files given)')


# --------------------------------------------------------------------------- charts
BLUE_TOP, BLUE_BOT, BLUE_STUB = '#4493C7', '#9CC6E1', '#86B9DA'     # 양식 Origin 두께 막대
PINK_TOP, PINK_BOT, PINK_STUB = '#FE8F8E', '#FFCCCC', '#FEA3A3'     # 양식 Origin 기공도 막대
RAMP = ['#F3E04C', '#A9D65A', '#5DBB63']                           # 노랑 → 초록
SIM_BLUE = '#4A8FCB'


def mpl_setup():
    plt.rcParams.update({
        'font.family': 'Liberation Sans', 'mathtext.fontset': 'custom', 'mathtext.rm': 'Liberation Sans',
        'mathtext.it': 'Liberation Sans:italic', 'mathtext.bf': 'Liberation Sans:bold',
        'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
        'xtick.minor.width': 0.5, 'ytick.minor.width': 0.5, 'xtick.direction': 'out', 'ytick.direction': 'out',
        'xtick.major.size': 2.5, 'ytick.major.size': 2.5, 'ytick.minor.size': 1.5, 'xtick.minor.size': 1.5,
    })


def xlabel_math(sec):
    return r'$%s_{\mathrm{%s}}$ (%s)' % (sec['sym'][0], sec['sym'][1], sec['unit'])


def write_csv(path, xname, xunit, yname, yunit, cats, vals, fmt):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow([xname, yname])
        w.writerow([xunit, yunit])
        for c, v in zip(cats, vals):
            w.writerow([c, fmt.format(v)])


def _grad_bar(ax, x, w, y0, y1, c_bot, c_top):
    cmap = LinearSegmentedColormap.from_list('g', [c_bot, c_top])
    t = np.linspace(0, 1, 256)
    t = 0.5 - 0.5 * np.cos(np.pi * t)
    ax.imshow(cmap(t)[:, None, :], extent=[x - w / 2, x + w / 2, y0, y1], origin='lower',
              aspect='auto', interpolation='bilinear', zorder=2)


def break_chart(path, size, margins, cats, vals, lo, hi, ticks, minor, ylabel, xlabel, ctop, cbot, cstub):
    """양식 Origin 막대 모양 (축 끊김 · 세로 그라데이션 · 틀 네 변)."""
    fw, fh = size
    l, r, t, b = margins
    W, H = fw - l - r, fh - t - b
    stub, gap = 0.07, 0.03
    fig = plt.figure(figsize=(fw, fh), dpi=300)
    axb = fig.add_axes([l / fw, b / fh, W / fw, stub / fh])
    axt = fig.add_axes([l / fw, (b + stub + gap) / fh, W / fw, (H - stub - gap) / fh])
    xs = np.arange(1, len(cats) + 1)
    bw = 0.6
    for x, v in zip(xs, vals):
        _grad_bar(axt, x, bw, lo, v, cbot, ctop)
        axb.add_patch(Rectangle((x - bw / 2, 0), bw, 1, facecolor=cstub, lw=0, zorder=2))
    for ax in (axt, axb):
        ax.set_xlim(0.4, len(cats) + 0.6)
    axt.set_ylim(lo, hi)
    axb.set_ylim(0, 1)
    axt.spines['bottom'].set_visible(False)
    axb.spines['top'].set_visible(False)
    for _ax in (axt, axb):                                   # 1저자 11-03 '우측, 위측 테두리는 없애줘 그게 우리 표준이야'
        _ax.spines['right'].set_visible(False)
    axt.spines['top'].set_visible(False)
    axt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axt.set_yticks(ticks)
    axt.set_yticks(minor, minor=True)
    axt.tick_params(axis='y', which='both', right=False, labelsize=7, pad=1.5)
    axb.set_yticks([0.0])
    axb.set_yticklabels(['0'])
    axb.tick_params(axis='y', which='both', right=False, labelsize=7, pad=1.5)
    axb.set_xticks(xs)
    axb.set_xticklabels(cats)
    axb.tick_params(axis='x', which='both', top=False, labelsize=7, pad=1.5)
    # 끊김 표시 (왼쪽 축만 — 1저자 11-03 표준 = 오른쪽 축선 없음)
    y_lo, y_hi = (b + stub) / fh, (b + stub + gap) / fh
    dx, dy = 0.035 / fw, 0.022 / fh
    for xa in (l / fw,):                                     # 오른쪽 축선이 없으니 끊김 표시도 왼쪽만 (1저자 11-03 표준)
        for yy in (y_lo, y_hi):
            fig.add_artist(Line2D([xa - dx, xa + dx], [yy - dy, yy + dy], transform=fig.transFigure,
                                  color='black', lw=0.6))
    fig.text((l - 0.36) / fw, (b + H / 2) / fh, ylabel, rotation=90, ha='center', va='center', fontsize=8)
    if xlabel:
        fig.text((l + W / 2) / fw, (b - 0.33) / fh, xlabel, ha='center', va='center', fontsize=8)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def simple_chart(path, size, cats, vals, colors, ylabel, xlabel, ylim, ticks, minor, fmt, legend=None,
                 tickfmt=None):
    fw, fh = size
    l, r, t, b = 0.66, 0.14, 0.30, 0.55
    fig = plt.figure(figsize=(fw, fh), dpi=300)
    ax = fig.add_axes([l / fw, b / fh, (fw - l - r) / fw, (fh - t - b) / fh])
    xs = np.arange(1, len(cats) + 1)
    ax.bar(xs, vals, 0.6, color=colors, edgecolor='#333333', linewidth=0.6, zorder=2, label=legend)
    span = ylim[1] - ylim[0]
    for x, v in zip(xs, vals):
        ax.text(x, v + 0.015 * span, fmt.format(v), ha='center', va='bottom', fontsize=7.5)
    ax.set_xlim(0.4, len(cats) + 0.6)
    ax.set_ylim(*ylim)
    ax.set_xticks(xs)
    ax.set_xticklabels(cats)
    ax.set_yticks(ticks)
    ax.set_yticks(minor, minor=True)
    if tickfmt:
        ax.yaxis.set_major_formatter(FuncFormatter(tickfmt))
    ax.tick_params(axis='both', which='both', top=False, right=False, labelsize=8, pad=2)
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.spines['top'].set_visible(False)                       # 1저자 11-03 표준 (위 · 오른쪽 축선 없음)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel(ylabel, fontsize=9, labelpad=3)
    ax.set_xlabel(xlabel, fontsize=9, labelpad=2)
    if legend:
        ax.legend(handles=[Patch(facecolor=colors[0], edgecolor='#333333', linewidth=0.6, label=legend)],
                  loc='upper left', frameon=False, fontsize=8, handlelength=1.0, handleheight=0.8,
                  borderaxespad=0.4)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def zero_fmt(v, _pos=None):
    return '0' if abs(v) < 1e-12 else ('%g' % v)


def make_charts(fig_dir):
    mpl_setup()
    fig_dir.mkdir(parents=True, exist_ok=True)
    out = {}
    s, m = SIZE, MOD
    # B · C 오른쪽 열 (양식 OLE 자리 크기 그대로)
    TH_SIZE, TH_M = (2.290, 1.604), (0.697, 0.17, 0.10, 0.27)
    PO_SIZE, PO_M = (2.213, 1.846), (0.62, 0.17, 0.10, 0.50)
    for sec, tag, slide in ((s, 'DSE', 'p07'), (m, 'ESE', 'p12')):
        name = '%s_thickness_%s' % (slide, tag)
        break_chart(fig_dir / (name + '.png'), TH_SIZE, TH_M, sec['cats'], sec['thickness'], 118, 135,
                    [120, 125, 130, 135], [122.5, 127.5, 132.5], 'Thickness (µm)', None,
                    BLUE_TOP, BLUE_BOT, BLUE_STUB)
        write_csv(fig_dir / (name + '.csv'), '%s_%s' % sec['sym'], sec['unit'], 'Thickness', 'µm',
                  sec['cats'], sec['thickness'], '{:.2f}')
        out[name] = fig_dir / (name + '.png')
        name = '%s_porosity_%s' % (slide, tag)
        break_chart(fig_dir / (name + '.png'), PO_SIZE, PO_M, sec['cats'], sec['porosity'], 10, 24,
                    [12, 16, 20, 24], [14, 18, 22], 'Porosity (%)', xlabel_math(sec),
                    PINK_TOP, PINK_BOT, PINK_STUB)
        write_csv(fig_dir / (name + '.csv'), '%s_%s' % sec['sym'], sec['unit'], 'Porosity', '%',
                  sec['cats'], sec['porosity'], '{:.1f}')
        out[name] = fig_dir / (name + '.png')
    # E 장 (지표 변화) · G 장 (이온전도도)
    E_SIZE, G_SIZE = (2.95, 3.40), (3.20, 3.40)
    for sec, tag, pe, pg in ((s, 'DSE', 'p09', 'p11'), (m, 'ESE', 'p14', 'p16')):
        xl = xlabel_math(sec)
        x0 = '%s_%s' % sec['sym']
        name = '%s_porosity_%s' % (pe, tag)
        simple_chart(fig_dir / (name + '.png'), E_SIZE, sec['cats'], sec['porosity'], [SIM_BLUE] * 3,
                     'Porosity (%)', xl, (0, 30), [0, 10, 20, 30], [5, 15, 25], '{:.1f}', legend='Simulation')
        write_csv(fig_dir / (name + '.csv'), x0, sec['unit'], 'Porosity (Simulation)', '%',
                  sec['cats'], sec['porosity'], '{:.1f}')
        out[name] = fig_dir / (name + '.png')
        name = '%s_tortuosity_%s' % (pe, tag)
        simple_chart(fig_dir / (name + '.png'), E_SIZE, sec['cats'], sec['tau2'], RAMP,
                     'Tortuosity', xl, (0, 16), [0, 4, 8, 12, 16], [2, 6, 10, 14], '{:.2f}')   # 1저자 11-03: 수송 tortuosity 를 'Tortuosity' 로만
        write_csv(fig_dir / (name + '.csv'), x0, sec['unit'], 'Tortuosity', '-',
                  sec['cats'], sec['tau2'], '{:.2f}')
        out[name] = fig_dir / (name + '.png')
        name = '%s_coverage_%s' % (pe, tag)
        simple_chart(fig_dir / (name + '.png'), E_SIZE, sec['cats'], sec['coverage'], RAMP,
                     'Coverage (%)', xl, (0, 80), [0, 20, 40, 60, 80], [10, 30, 50, 70], '{:.1f}')
        write_csv(fig_dir / (name + '.csv'), x0, sec['unit'], 'Coverage', '%',
                  sec['cats'], sec['coverage'], '{:.1f}')
        out[name] = fig_dir / (name + '.png')
        name = '%s_sigma_%s' % (pg, tag)
        simple_chart(fig_dir / (name + '.png'), G_SIZE, sec['cats'], sec['sigma'], RAMP,
                     r'$\sigma_{\mathrm{Li^{+}}}$ (mS cm$^{-1}$)', xl, (0, 0.08), [0, 0.02, 0.04, 0.06, 0.08],
                     [0.01, 0.03, 0.05, 0.07], '{:.4f}', tickfmt=zero_fmt)
        write_csv(fig_dir / (name + '.csv'), x0, sec['unit'], 'sigma_Li+', 'mS cm-1',
                  sec['cats'], sec['sigma'], '{:.4f}')
        out[name] = fig_dir / (name + '.png')
    return out


def colorbar_png(path, horizontal):
    t = np.linspace(0, 1, 512)
    rgb = (plt.get_cmap('jet')(t)[:, :3] * 255).astype(np.uint8)
    img = np.repeat(rgb[None, :, :], 28, axis=0) if horizontal else np.repeat(rgb[::-1][:, None, :], 28, axis=1)
    img[0, :] = img[-1, :] = 60
    img[:, 0] = img[:, -1] = 60
    Image.fromarray(img).save(path)


# 기공 렌더 시점 — docs/50kg/report_y4/figs/d1_compaction/stage_frames_d1.csv 의 recommended 줄 (--stage-frames 로 다시 읽음)
STAGES = [dict(stage='initial_compression', step=450000, pressure=0.0, plate=144.9457),
          dict(stage='p50', step=1250000, pressure=53.107941, plate=136.9457),
          dict(stage='p300_stop', step=2650000, pressure=294.26469, plate=122.9457),
          dict(stage='after_relaxation', step=2785002, pressure=156.15118, plate=122.5957)]


def read_stages(path):
    rows = [r for r in csv.DictReader(open(path, encoding='utf-8-sig')) if 'recommended' in r['role']]
    by = {r['stage']: r for r in rows}
    return [dict(stage=k, step=int(by[k]['dump_step']), pressure=float(by[k]['pressure_MPa']),
                 plate=float(by[k]['plate_um'])) for k in [st['stage'] for st in STAGES]]


def measure_crop_renders(paths, dst_dir, pad=8, prefix='pore_render'):
    """렌더마다 침대 bbox (흰 · 투명 아닌 픽셀 · 외톨이 줄 / 열 무시) 를 재고 그 bbox + 여백으로 자른다.
    웹앱 렌더는 침대마다 화면에 맞춰 확대돼 있어서 (높이 785 / 769 / 769 px) 장에서 가압판 높이에 비례하게 다시 맞춘다."""
    out = []
    for k, p in enumerate(paths):
        im = Image.open(p).convert('RGBA')
        a = np.array(im)
        mask = (a[..., :3].min(axis=2) < 245) & (a[..., 3] > 10)
        rows, cols = mask.sum(axis=1), mask.sum(axis=0)
        ys = np.where(rows >= max(3, 0.005 * rows.max()))[0]
        xs = np.where(cols >= max(3, 0.005 * cols.max()))[0]
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        cx0, cy0 = max(x0 - pad, 0), max(y0 - pad, 0)
        cx1, cy1 = min(x1 + pad + 1, im.size[0]), min(y1 + pad + 1, im.size[1])
        d = dst_dir / ('%s_%d.png' % (prefix, k))
        im.crop((cx0, cy0, cx1, cy1)).save(d)
        out.append(dict(path=d, crop_w=cx1 - cx0, crop_h=cy1 - cy0, bed_w=x1 - x0 + 1, bed_h=y1 - y0 + 1,
                        pad_left=x0 - cx0, pad_top=y0 - cy0))
        print('render %d: bed bbox %d x %d px (x %d-%d, y %d-%d)' % (k, x1 - x0 + 1, y1 - y0 + 1, x0, x1, y0, y1))
    return out


def fit_box(aspect, max_w, max_h):
    w = min(max_w, max_h * aspect)
    return w, w / aspect


# --------------------------------------------------------------------------- pptx XML helpers
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
REL_IMG = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
REL_NOTES = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide'
WRAP = '<w xmlns:a="%s" xmlns:r="%s" xmlns:p="%s">%%s</w>' % (NS['a'], NS['r'], NS['p'])


def E(x):
    return int(round(x * 914400))


def frag(xml):
    return etree.fromstring(WRAP % xml)[0]


def qn(tag):
    pre, loc = tag.split(':')
    return '{%s}%s' % (NS[pre], loc)


F_MED = ('<a:latin typeface="KoPubWorld돋움체 Medium" panose="00000600000000000000" pitchFamily="2" charset="-127"/>'
         '<a:ea typeface="KoPubWorld돋움체 Medium" panose="00000600000000000000" pitchFamily="2" charset="-127"/>'
         '<a:cs typeface="KoPubWorld돋움체 Medium" panose="00000600000000000000" pitchFamily="2" charset="-127"/>')
F_BODY = ('<a:latin typeface="KoPubWorldDotum Medium" pitchFamily="2" charset="-127"/>'
          '<a:ea typeface="KoPubWorldDotum Medium" pitchFamily="2" charset="-127"/>'
          '<a:cs typeface="KoPubWorld돋움체 Medium" panose="00000600000000000000" pitchFamily="2" charset="-127"/>')
F_BOLD = ('<a:latin typeface="KoPubWorldDotum Bold" pitchFamily="2" charset="-127"/>'
          '<a:ea typeface="KoPubWorldDotum Bold" pitchFamily="2" charset="-127"/>'
          '<a:cs typeface="KoPubWorld돋움체 Bold" panose="00000800000000000000" pitchFamily="2" charset="-127"/>')
GRAY = '<a:solidFill><a:prstClr val="black"><a:lumMod val="75000"/><a:lumOff val="25000"/></a:prstClr></a:solidFill>'
BLUE = '<a:solidFill><a:srgbClr val="0070C0"/></a:solidFill>'
BLACK = '<a:solidFill><a:prstClr val="black"/></a:solidFill>'
INK = '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
MUTED = '<a:solidFill><a:srgbClr val="595959"/></a:solidFill>'

SUB, SUP = -25000, 30000


def R(text, sz=1600, color=GRAY, font=F_BODY, b=0, i=0, base=0, lang='ko-KR'):
    return ('<a:r><a:rPr kumimoji="0" lang="%s" altLang="en-US" sz="%d" b="%d" i="%d" u="none" strike="noStrike" '
            'kern="1200" cap="none" spc="0" normalizeH="0" baseline="%d" noProof="0" dirty="0"><a:ln><a:noFill/></a:ln>'
            '%s<a:effectLst/><a:uLnTx/><a:uFillTx/>%s</a:rPr><a:t>%s</a:t></a:r>'
            % (lang, sz, b, i, base, color, font, escape(text)))


def SYM(sec, sz=1600, color=GRAY, font=F_BODY, b=0):
    """이탤릭 기호 + 바로 선 아래 첨자 (D_SE · E_SE)."""
    return [R(sec['sym'][0], sz, color, font, b=b, i=1, lang='en-US'),
            R(sec['sym'][1], sz, color, font, b=b, base=SUB, lang='en-US')]


def UNIT_INV(sz=1600, color=GRAY, font=F_BODY):
    """mS cm⁻¹."""
    return [R(' mS cm', sz, color, font, lang='en-US'), R('−1', sz, color, font, base=SUP, lang='en-US')]


# 장 머리 상자 (Rectangle 23) 문단 — 양식 6장 문단 속성 그대로
PPR_HEAD = ('<a:pPr marL="0" marR="0" lvl="0" indent="0" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" '
            'fontAlgn="base" latinLnBrk="1" hangingPunct="1"><a:lnSpc><a:spcPct val="150000"/></a:lnSpc>'
            '<a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPct val="0"/></a:spcAft><a:buClrTx/>'
            '<a:buSzTx/><a:buFontTx/><a:buBlip><a:blip r:embed="%s"/></a:buBlip><a:tabLst/><a:defRPr/></a:pPr>')
PPR_BUL = ('<a:pPr marL="541338" marR="0" lvl="0" indent="-185738" algn="just" defTabSz="914400" rtl="0" '
           'eaLnBrk="1" fontAlgn="auto" latinLnBrk="1" hangingPunct="1"><a:lnSpc><a:spcPct val="150000"/></a:lnSpc>'
           '<a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buClrTx/><a:buSzTx/>'
           '<a:buFont typeface="Arial" panose="020B0604020202020204" pitchFamily="34" charset="0"/>'
           '<a:buChar char="•"/><a:tabLst/><a:defRPr/></a:pPr>')


def HEAD(parts):
    """parts = [(text, blue?)]  — 머리 줄 (KoPubWorldDotum Bold 18pt)."""
    out = []
    for p in parts:
        if isinstance(p, list):
            out.extend(p)
        else:
            text, blue = p
            out.append(R(text, 1800, BLUE if blue else BLACK, F_BOLD, b=1))
    return out


def BUL(parts):
    out = []
    for p in parts:
        if isinstance(p, list):
            out.extend(p)
        else:
            text, blue = p
            out.append(R(text, 1600, BLUE if blue else GRAY, F_BODY))
    return out


def LP(runs, algn='ctr', lnspc=100000):
    return ('<a:p><a:pPr marL="0" marR="0" lvl="0" indent="0" algn="%s" defTabSz="914400" rtl="0" eaLnBrk="1" '
            'fontAlgn="auto" latinLnBrk="1" hangingPunct="1"><a:lnSpc><a:spcPct val="%d"/></a:lnSpc>'
            '<a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buClrTx/>'
            '<a:buSzTx/><a:buFontTx/><a:buNone/><a:tabLst/><a:defRPr/></a:pPr>%s</a:p>' % (algn, lnspc, ''.join(runs)))


def LAB(text, sz=1100, color=INK, i=0, base=0):
    return R(text, sz, color, F_MED, i=i, base=base, lang='en-US')


def TB(sid, name, x, y, w, h, paras, anchor='ctr', rot=0):
    rot_attr = ' rot="%d"' % rot if rot else ''
    return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>'
            '<a:xfrm%s><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/>'
            '</a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" '
            'rtlCol="0" anchor="%s"><a:noAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody></p:sp>'
            % (sid, escape(name), rot_attr, E(x), E(y), E(w), E(h), anchor, paras))


def FRAME(sid, name, x, y, w, h):
    """양식 그림 틀 (연회색 선) — 양식 6장 '직사각형 261' 과 같은 꼴."""
    return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm>'
            '<a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            '<a:noFill/><a:ln><a:solidFill><a:schemeClr val="bg1"><a:lumMod val="85000"/></a:schemeClr></a:solidFill>'
            '</a:ln></p:spPr><p:style><a:lnRef idx="2"><a:schemeClr val="accent1"><a:shade val="15000"/></a:schemeClr>'
            '</a:lnRef><a:fillRef idx="1"><a:schemeClr val="accent1"/></a:fillRef><a:effectRef idx="0">'
            '<a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef>'
            '</p:style><p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/>'
            '<a:endParaRPr lang="ko-KR" altLang="en-US"/></a:p></p:txBody></p:sp>'
            % (sid, escape(name), E(x), E(y), E(w), E(h)))


def SLOT(sid, name, x, y, w, h):
    """이미지 칸 — 점선 빈 사각형 (1저자가 렌더를 붙인다)."""
    return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm>'
            '<a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            '<a:noFill/><a:ln w="9525"><a:solidFill><a:schemeClr val="bg1"><a:lumMod val="65000"/></a:schemeClr>'
            '</a:solidFill><a:prstDash val="dash"/></a:ln></p:spPr><p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/>'
            '<a:lstStyle/><a:p><a:pPr algn="ctr"/><a:endParaRPr lang="ko-KR" altLang="en-US" sz="1000"/></a:p>'
            '</p:txBody></p:sp>' % (sid, escape(name), E(x), E(y), E(w), E(h)))


def PIC(sid, name, rid, x, y, w, h):
    return ('<p:pic><p:nvPicPr><p:cNvPr id="%d" name="%s"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/>'
            '</p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/>'
            '</a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'
            % (sid, escape(name), rid, E(x), E(y), E(w), E(h)))


def DOTARROW(sid, name, x1, y, x2):
    return ('<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="%d" name="%s"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>'
            '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="0"/></a:xfrm><a:prstGeom prst="straightConnector1">'
            '<a:avLst/></a:prstGeom><a:ln w="12700"><a:solidFill><a:srgbClr val="7F7F7F"/></a:solidFill>'
            '<a:prstDash val="sysDot"/><a:tailEnd type="triangle" w="med" len="med"/></a:ln></p:spPr></p:cxnSp>'
            % (sid, escape(name), E(x1), E(y), E(x2 - x1)))


class Slide:
    def __init__(self, root, fname):
        self.root = root
        self.fname = fname
        self.path = root / 'ppt' / 'slides' / fname
        self.rels_path = root / 'ppt' / 'slides' / '_rels' / (fname + '.rels')
        self.tree = etree.parse(str(self.path))
        self.rtree = etree.parse(str(self.rels_path))
        self.sptree = self.tree.getroot().find('.//p:cSld/p:spTree', NS)
        self._nid = 0

    def shapes(self):
        return [c for c in self.sptree
                if etree.QName(c).localname in ('sp', 'pic', 'grpSp', 'graphicFrame', 'cxnSp')]

    @staticmethod
    def name_of(el):
        return el.find('.//p:cNvPr', NS).get('name')

    def get(self, name):
        for el in self.shapes():
            if self.name_of(el) == name:
                return el
        raise KeyError('%s: no shape %r' % (self.fname, name))

    def nid(self):
        ids = [int(e.get('id')) for e in self.tree.getroot().iter(qn('p:cNvPr'))]
        self._nid = max(ids + [self._nid]) + 1
        return self._nid

    def add(self, xml):
        el = frag(xml)
        ext = self.sptree.find('p:extLst', NS)
        if ext is not None:
            ext.addprevious(el)
        else:
            self.sptree.append(el)
        return el

    def remove(self, name):
        el = self.get(name)
        el.getparent().remove(el)

    def keep_only(self, names):
        for el in self.shapes():
            if self.name_of(el) not in names:
                el.getparent().remove(el)

    def media(self, src, media_name):
        dst = self.root / 'ppt' / 'media' / media_name
        if not dst.exists():
            shutil.copyfile(src, dst)
        rels = self.rtree.getroot()
        for r in rels:
            if r.get('Target') == '../media/' + media_name:
                return r.get('Id')
        nums = [int(r.get('Id')[3:]) for r in rels if re.fullmatch(r'rId\d+', r.get('Id'))]
        rid = 'rId%d' % (max(nums) + 1)
        etree.SubElement(rels, '{%s}Relationship' % PKG, Id=rid, Type=REL_IMG, Target='../media/' + media_name)
        return rid

    def set_xfrm(self, el, x=None, y=None, w=None, h=None):
        xf = el.find('./p:spPr/a:xfrm', NS)
        if xf is None:
            xf = el.find('./p:grpSpPr/a:xfrm', NS)
        off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
        if x is not None:
            off.set('x', str(E(x)))
        if y is not None:
            off.set('y', str(E(y)))
        if w is not None:
            ext.set('cx', str(E(w)))
        if h is not None:
            ext.set('cy', str(E(h)))

    def xfrm(self, el):
        xf = el.find('./p:spPr/a:xfrm', NS)
        if xf is None:
            xf = el.find('./p:grpSpPr/a:xfrm', NS)
        if xf is None:
            xf = el.find('./p:xfrm', NS)
        off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
        return (int(off.get('x')) / 914400, int(off.get('y')) / 914400,
                int(ext.get('cx')) / 914400, int(ext.get('cy')) / 914400)

    def rect_text(self, head_runs, bullets, line_count=None):
        """장 머리 상자: 머리 + 글머리 (양식 문단 속성 · 사진 글머리표 그대로)."""
        rect = self.get('Rectangle 23')
        blip = rect.find('.//a:buBlip/a:blip', NS).get(qn('r:embed'))
        body = rect.find('./p:txBody', NS)
        for p in body.findall('a:p', NS):
            body.remove(p)
        body.append(frag('<a:p>%s%s</a:p>' % (PPR_HEAD % blip, ''.join(head_runs))))
        for b in bullets:
            body.append(frag('<a:p>%s%s</a:p>' % (PPR_BUL, ''.join(b))))
        n = 1 + len(bullets) if line_count is None else line_count
        self.set_xfrm(rect, h=1.330 + 0.403 * (n - 3))

    def caption(self, text):
        cap = self.get('Text Box 36')
        p = cap.find('.//a:p', NS)
        runs = p.findall('a:r', NS)
        runs[0].find('a:t', NS).text = text
        for r in runs[1:]:
            p.remove(r)

    def replace_with_pic(self, name, src, media_name):
        el = self.get(name)
        x, y, w, h = self.xfrm(el)
        rid = self.media(src, media_name)
        new = frag(PIC(self.nid(), media_name.rsplit('.', 1)[0], rid, x, y, w, h))
        el.addprevious(new)
        el.getparent().remove(el)

    def new_creation_id(self):
        for el in self.tree.getroot().iter('{http://schemas.microsoft.com/office/powerpoint/2010/main}creationId'):
            el.set('val', str(random.randint(10 ** 8, 4 * 10 ** 9)))

    def save(self):
        text = etree.tostring(self.tree.getroot(), encoding='unicode')
        rels = self.rtree.getroot()
        for r in list(rels):
            t = r.get('Type').rsplit('/', 1)[-1]
            if t in ('image', 'oleObject') and ('"%s"' % r.get('Id')) not in text:
                rels.remove(r)
        hdr = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        self.path.write_bytes(hdr + etree.tostring(self.tree.getroot(), encoding='UTF-8'))
        self.rels_path.write_bytes(hdr + etree.tostring(rels, encoding='UTF-8'))


HEADER_KEEP = {'TextBox 10', 'Rectangle 23', 'TextBox 2', 'TextBox 4', 'Text Box 36', '슬라이드 번호 개체 틀 2'}


# --------------------------------------------------------------------------- notes
def notes_paras(text):
    return ''.join('<a:p><a:r><a:rPr lang="ko-KR" altLang="en-US" dirty="0"/><a:t>%s</a:t></a:r></a:p>'
                   % escape(line) for line in text.split('\n'))


def set_notes_body(notes_path, text):
    t = etree.parse(str(notes_path))
    for sp in t.getroot().iter(qn('p:sp')):
        ph = sp.find('.//p:nvPr/p:ph', NS)
        if ph is not None and ph.get('type') == 'body':
            body = sp.find('p:txBody', NS)
            for p in body.findall('a:p', NS):
                body.remove(p)
            for p in etree.fromstring(WRAP % notes_paras(text)):
                body.append(p)
    hdr = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    notes_path.write_bytes(hdr + etree.tostring(t.getroot(), encoding='UTF-8'))


def ensure_notes(root, slide_fname, text):
    """있으면 본문 교체 · 없으면 notesSlide5.xml 꼴로 새로 만든다 (rels · content types 등록)."""
    srels = root / 'ppt' / 'slides' / '_rels' / (slide_fname + '.rels')
    rt = etree.parse(str(srels))
    for r in rt.getroot():
        if r.get('Type') == REL_NOTES:
            set_notes_body((root / 'ppt' / 'slides' / r.get('Target')).resolve(), text)
            return
    ndir = root / 'ppt' / 'notesSlides'
    nums = [int(m.group(1)) for f in ndir.glob('notesSlide*.xml') if (m := re.match(r'notesSlide(\d+)\.xml', f.name))]
    n = max(nums) + 1
    new = ndir / ('notesSlide%d.xml' % n)
    xml = (ndir / 'notesSlide5.xml').read_text(encoding='utf-8')
    xml = re.sub(r'(<p14:creationId [^>]*val=")\d+', lambda m: m.group(1) + str(random.randint(10 ** 8, 4 * 10 ** 9)), xml)
    new.write_text(xml, encoding='utf-8')
    set_notes_body(new, text)
    (ndir / '_rels' / ('notesSlide%d.xml.rels' % n)).write_text(
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Relationships xmlns="%s">'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
        'Target="../slides/%s"/><Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" '
        'Target="../notesMasters/notesMaster1.xml"/></Relationships>' % (PKG, slide_fname), encoding='utf-8')
    ct = root / '[Content_Types].xml'
    s = ct.read_text(encoding='utf-8')
    s = s.replace('</Types>', '<Override PartName="/ppt/notesSlides/notesSlide%d.xml" ContentType="application/'
                  'vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/></Types>' % n)
    ct.write_text(s, encoding='utf-8')
    nums = [int(r.get('Id')[3:]) for r in rt.getroot() if re.fullmatch(r'rId\d+', r.get('Id'))]
    etree.SubElement(rt.getroot(), '{%s}Relationship' % PKG, Id='rId%d' % (max(nums) + 1), Type=REL_NOTES,
                     Target='../notesSlides/notesSlide%d.xml' % n)
    hdr = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    srels.write_bytes(hdr + etree.tostring(rt.getroot(), encoding='UTF-8'))


# --------------------------------------------------------------------------- slides
def bed_label(sec, k, sz=1200):
    return LP(SYM(sec, sz, INK, F_MED) + [LAB(' = %s %s' % (sec['cats'][k], sec['unit']), sz)])


def build_A(s, a):
    s.keep_only(HEADER_KEEP)
    s.new_creation_id()
    s.rect_text(
        HEAD([(' DEM 기반 복합양극 ', 0), ('가압 거동', 1), (' (', 0),
              [R('D', 1800, BLACK, F_BOLD, b=1, i=1, lang='en-US'), R('SE', 1800, BLACK, F_BOLD, b=1, base=SUB, lang='en-US')],
              (' = 1 µm)', 0)]),
        [BUL([('가압판 속도 제어에 따른 ', 0), ('전극 두께 및 측정 압력', 1), (' 변화, ', 0), ('응력 완화', 1), ('로 압력 감소', 0)]),
         BUL([('가압에 따른 입자 재배열로 ', 0), ('기공 공간 축소', 1), (', 응력 완화 후에도 기공 분포 유지', 0)])])   # 1저자 11-03 글머리 두 줄
    s.caption('【 고체전해질 입도 1 µm 복합양극의 가압 거동 및 기공 분포 】')
    # 1저자 11-03: 왼쪽 그래프 칸 = 3.50 × 3.85 in (그래프를 이 크기로 그려 1:1 로 붙임 · 글씨 9 pt) · 오른쪽 기공 그림 약간 축소
    fw, fh = fit_box(a['d1_aspect'], 3.50, 3.85)
    s.add(PIC(s.nid(), 'D1 compaction curves', s.media(a['d1fig'], 'kg50t_d1_compaction.png'), 0.55, 2.62, fw, fh))
    x0, x1 = 4.20, 9.45
    s.add(TB(s.nid(), 'Pore distribution title', x0, 2.75, x1 - x0, 0.22, LP([LAB('[ Pore distribution ]', 1100)])))
    sw = 1.16
    g = ((x1 - x0) - 4 * sw) / 3
    yb, hb0 = 6.10, 2.25                                  # 집전체 쪽 바닥선 · 가압 초기 침대 높이 (in)
    st = a['stages']
    labels = [('Initial', 'compression'), ('50 MPa',), ('300 MPa',), ('After', 'relaxation')]
    half = [0.42, 0.27, 0.31, 0.37]
    cxs = []
    bed_w = None
    for i, lab in enumerate(labels):
        cx = x0 + i * (sw + g) + sw / 2
        cxs.append(cx)
        s.add(TB(s.nid(), 'Stage %d' % (i + 1), cx - 0.60, 3.02, 1.20, 0.40, ''.join(LP([LAB(w, 1050)]) for w in lab)))
        hb = hb0 * st[i]['plate'] / st[0]['plate']        # 침대 높이 ∝ 가압판 높이 (가압 초기 기준)
        if True:                                          # After relaxation = 300 MPa 원본 그림 (1저자 파일 이름 '300MPa, after relaxation')
            r = a['renders'][min(i, 2)]
            ipp = hb / r['bed_h']
            w, h = r['crop_w'] * ipp, r['crop_h'] * ipp
            x = cx - (r['pad_left'] + r['bed_w'] / 2) * ipp
            y = yb - (r['pad_top'] + r['bed_h']) * ipp
            rid = s.media(r['path'], 'kg50t_pore_stage%d.png' % (min(i, 2) + 1))
            s.add(PIC(s.nid(), 'Pore render %d' % (i + 1), rid, x, y, w, h))
            bed_w = r['bed_w'] * ipp
        else:
            s.add(SLOT(s.nid(), 'Image slot After relaxation', cx - bed_w / 2, yb - hb, bed_w, hb))
    for i in range(3):
        s.add(DOTARROW(s.nid(), 'Stage arrow %d' % (i + 1), cxs[i] + half[i] + 0.06, 3.22,
                       cxs[i + 1] - half[i + 1] - 0.06))
    s.add(TB(s.nid(), 'Current collector', cxs[0] - 0.85, yb + 0.06, 1.70, 0.20,
             LP([LAB('< Current collector >', 1000, MUTED)])))


def _relabel_two_lines(s, name, words, dy=-0.17):
    el = s.get(name)
    x, y, w, h = s.xfrm(el)
    p = el.find('.//a:p', NS)
    ppr = p.find('a:pPr', NS)
    ln = ppr.find('a:lnSpc/a:spcPct', NS)
    if ln is not None:
        ln.set('val', '100000')
    sa = ppr.find('a:spcAft/a:spcPts', NS)
    if sa is not None:
        sa.set('val', '0')
    runs = p.findall('a:r', NS)
    runs[0].find('a:t', NS).text = words[0]
    for r in runs[1:]:
        p.remove(r)
    p2 = etree.fromstring(etree.tostring(p))
    p2.findall('a:r', NS)[0].find('a:t', NS).text = words[1]
    p.addnext(p2)
    s.set_xfrm(el, y=y + dy, h=0.36)


def _set_run_text(el, text):
    p = el.find('.//a:p', NS)
    runs = p.findall('a:r', NS)
    runs[0].find('a:t', NS).text = text
    for r in runs[1:]:
        p.remove(r)


def build_B(s, ch, size_renders=None, path_renders=None):
    sec = SIZE
    rect = s.get('Rectangle 23')
    paras = rect.findall('.//a:p', NS)
    ppr = etree.tostring(paras[2].find('a:pPr', NS), encoding='unicode')
    ppr = re.sub(r' xmlns:\w+="[^"]+"', '', ppr)
    b2 = frag('<a:p>%s%s</a:p>' % (ppr, ''.join(BUL([('입도 감소에 따른 ', 0), ('수송 tortuosity 감소', 1),
                                                        (' 확인 (13.6 → 6.0)', 0)]))))
    b3 = frag('<a:p>%s%s</a:p>' % (ppr, ''.join(BUL([('유효 이온전도도 증가 (0.029 → 0.070', 0)]) + UNIT_INV()
                                                  + BUL([(')', 0)]))))
    paras[2].addprevious(b2)
    paras[2].addprevious(b3)
    paras[2].getparent().remove(paras[2])
    s.set_xfrm(rect, h=1.733)
    for name, v in zip(('TextBox 16', 'TextBox 19', 'TextBox 20'), sec['tau2']):      # 1저자 11-02: 수송 tortuosity
        _set_run_text(s.get(name), '%.2f' % v)
    # 1저자 11-03: 라벨 = 템플릿 그대로 'Tortuosity' · 그림 묶음 · 범례 · 값 = 템플릿 자리 · 크기 그대로 (글머리 내용만 다름)
    el = s.get('TextBox 19')                                   # 2 µm 값만 경로 선과 겹쳐 0.10 in 오른쪽
    s.set_xfrm(el, x=s.xfrm(el)[0] + 0.10)
    el = s.get('그룹 260')                                     # 글머리 셋째 줄과 겹쳐 범례만 0.10 in 아래 (틀 위)
    s.set_xfrm(el, y=s.xfrm(el)[1] + 0.10)
    # 렌더 셋 · 경로 그림 셋 = 옛 자료 그림 → 같은 자리 · 크기의 빈 칸 (점선)
    rboxes = [s.xfrm(s.get(nm)) for nm in ('그림 2', '그림 6', '그림 9')]       # 렌더 칸 (지우기 전에 잼)
    for name, slot in (('그림 2', 'Image slot render D1'), ('그림 3', 'Image slot path D1'),
                       ('그림 6', 'Image slot render D2'), ('그림 7', 'Image slot path D2'),
                       ('그림 9', 'Image slot render D3'), ('그림 11', 'Image slot path D3')):
        el = s.get(name)
        x, y, w, h = s.xfrm(el)
        k = {'Image slot render D1': 0, 'Image slot render D2': 1, 'Image slot render D3': 2}.get(slot)
        if size_renders and k is not None:
            # 1저자 11-02 렌더 · 높이 ∝ 이완 끝 판 높이 (D1 122.60 · D2 122.47 · D3 125.88 µm) · 칸 바닥 맞춤 · 칸 가운데
            plate = [122.60, 122.47, 125.88]
            # 1저자 11-03: 템플릿 렌더와 같은 크기 — 가장 큰 침대 (D3) 그림 높이 = 템플릿 D3 칸 높이 · 나머지 ∝ 판 높이 ·
            #   바닥 = 템플릿 D1 · D2 칸 바닥 (공통) · 오른쪽 끝 = 템플릿 칸 오른쪽 끝 (경로 그림을 덮지 않게 남는 폭은 왼쪽으로)
            r = size_renders[k]
            r3 = size_renders[2]
            H3 = rboxes[2][3]                                   # 템플릿 D3 렌더 칸 높이 (그림 전체 높이)
            ip3 = H3 / r3['crop_h']                             # D3 의 in/px
            hb = r3['bed_h'] * ip3 * plate[k] / max(plate)      # 이 침대의 침대 높이 (in)
            ipp = hb / r['bed_h']
            pw, ph = r['crop_w'] * ipp, r['crop_h'] * ipp
            base = rboxes[0][1] + rboxes[0][3]                  # 공통 바닥
            px = x + w - pw
            py = base - (r['pad_top'] + r['bed_h']) * ipp
            rid = s.media(r['path'], 'kg50t_size_render_D%d.png' % (k + 1))
            el.addprevious(frag(PIC(s.nid(), 'Size render D%d' % (k + 1), rid, px, py, pw, ph)))
        elif path_renders and slot.startswith('Image slot path D'):
            kp = int(slot[-1]) - 1                         # 1저자 11-02 경로 그림 · 칸 안에 맞춤 (비율 유지 · 가운데)
            r = path_renders[kp]
            sc = h / r['crop_h']                           # 1저자 11-03: 템플릿 경로 그림과 같은 높이 · 칸 가운데
            pw, ph = r['crop_w'] * sc, r['crop_h'] * sc
            rid = s.media(r['path'], 'kg50t_size_path_D%d.png' % (kp + 1))
            el.addprevious(frag(PIC(s.nid(), 'Size path D%d' % (kp + 1), rid, x + (w - pw) / 2, y + (h - ph) / 2, pw, ph)))
        else:
            el.addprevious(frag(SLOT(s.nid(), slot, x, y, w, h)))
        el.getparent().remove(el)
    s.replace_with_pic('개체 29', ch['p07_thickness_DSE'], 'kg50t_p07_thickness_DSE.png')
    s.replace_with_pic('개체 225', ch['p07_porosity_DSE'], 'kg50t_p07_porosity_DSE.png')


def build_C(s, ch):
    sec = MOD
    for name, old, new in (('TextBox 7', ' = 12 ', ' = 11 '), ('TextBox 18', ' = 24 ', ' = 22 '),
                           ('TextBox 9', ' = 36 ', ' = 33 ')):
        hit = 0
        for t in s.get(name).iter(qn('a:t')):
            if t.text == old:
                t.text = new
                hit += 1
        assert hit == 1, (name, old)
    rect = s.get('Rectangle 23')
    done = set()
    for r in rect.iter(qn('a:r')):
        t = r.find('a:t', NS)
        if t.text == ' 전극 내 기공도 증가 ':
            t.text = ' 전극 내 기공도 및 '
            gray = etree.tostring(r, encoding='unicode')
            gray = re.sub(r' xmlns:\w+="[^"]+"', '', gray)
            blue = re.sub(r'<a:solidFill>.*?</a:solidFill>', BLUE, gray, count=1)
            r1 = frag(re.sub(r'<a:t>[^<]*</a:t>', '<a:t>수송 tortuosity 증가</a:t>', blue))
            r2 = frag(re.sub(r'<a:t>[^<]*</a:t>', '<a:t> (7.80 → 9.05) </a:t>', gray))
            r.addnext(r1)
            r1.addnext(r2)
            done.add('tau')
        elif t.text == '이 이 복합양극 치밀화 및 ':
            t.text = '이 복합양극 치밀화 및 '
            done.add('typo')
    assert done == {'tau', 'typo'}, done
    # 렌더 자리 = 빈 칸 · 틀은 양식 6장과 같은 폭
    for name in ('그림 30', '그림 12', '그림 14'):
        s.remove(name)
    s.set_xfrm(s.get('직사각형 28'), x=0.542, y=3.310, w=6.281, h=3.250)
    pitch = 6.281 / 3
    sw, sh, sy = 1.20, 2.45, 3.86
    for i, name in enumerate(('TextBox 7', 'TextBox 18', 'TextBox 9')):
        sx = 0.542 + i * pitch + 0.10
        s.add(SLOT(s.nid(), 'Image slot E%s' % sec['cats'][i], sx, sy, sw, sh))
        lab = s.get(name)
        _, ly, lw, _ = s.xfrm(lab)
        s.set_xfrm(lab, x=sx + sw / 2 - lw / 2)
        cx = sx + sw + 0.38
        s.add(TB(s.nid(), 'Transport tortuosity label %d' % (i + 1), cx - 0.5, sy + 0.08, 1.0, 0.36,
                 LP([LAB('Tortuosity', 1050)])))   # 1저자 11-03: 'Transport tortuosity' → 'Tortuosity'
        s.add(TB(s.nid(), 'Transport tortuosity value %d' % (i + 1), cx - 0.3, sy + 0.50, 0.6, 0.22,
                 LP([LAB('%.2f' % sec['tau2'][i], 1100)])))
    s.set_xfrm(s.get('그룹 23'), x=5.30)
    oxs = s.get('개체 22')
    x, y, w, h = s.xfrm(oxs)
    s.add(PIC(s.nid(), 'kg50t_p12_thickness_ESE', s.media(ch['p12_thickness_ESE'], 'kg50t_p12_thickness_ESE.png'),
              7.042, 3.10, 2.290, 1.604))
    s.add(PIC(s.nid(), 'kg50t_p12_porosity_ESE', s.media(ch['p12_porosity_ESE'], 'kg50t_p12_porosity_ESE.png'),
              7.120, 4.726, 2.213, 1.846))
    s.remove('개체 22')


def _frame_grid(s, sec, top, bot, rows, values, slot_label_sz=950):
    """세 침대 열 · 열마다 이미지 칸 (rows = [[이름, 이름], …]) + 칸 아래 값."""
    x0, colw, gap = 0.45, 2.953, 0.12
    sw = (colw - 0.30) / 2
    n = len(rows)
    fixed = 0.52 + (n - 1) * 0.46 + 0.22 + 0.03
    h = (bot - top - fixed) / n
    for c in range(3):
        cx0 = x0 + c * (colw + gap)
        s.add(FRAME(s.nid(), 'Bed frame %d' % (c + 1), cx0, top, colw, bot - top))
        s.add(TB(s.nid(), 'Bed label %d' % (c + 1), cx0, top + 0.04, colw, 0.26, bed_label(sec, c)))
        for r, names in enumerate(rows):
            yy = top + 0.52 + r * (h + 0.46)
            for k, nm in enumerate(names):
                sx = cx0 + 0.10 + k * (sw + 0.10)
                s.add(TB(s.nid(), 'Slot label %s %d' % (nm, c + 1), sx, yy - 0.20, sw, 0.18,
                         LP([LAB(nm, slot_label_sz)])))
                s.add(SLOT(s.nid(), 'Image slot %s %d' % (nm, c + 1), sx, yy, sw, h))
                v = values(nm, c)
                if v:
                    s.add(TB(s.nid(), 'Value %s %d' % (nm, c + 1), sx, yy + h + 0.02, sw, 0.20, LP([LAB(v, 1100)])))
    return h


def build_D(s, sec):
    s.keep_only(HEADER_KEEP)
    s.new_creation_id()
    size = sec is SIZE
    head = (' 고체전해질 입도에 따른 복합양극 ' if size else ' 고체전해질 기계적 물성에 따른 복합양극 ')
    lead = '입도별 복합양극 ' if size else 'modulus별 복합양극 '
    s.rect_text(HEAD([(head, 0), ('미세구조 비교', 1)]),
                [BUL([(lead, 0), ('구조, coverage, 기공 및 이온 이동 경로', 1), (' 비교', 0)])])
    s.caption('【 고체전해질 %s에 따른 복합양극 미세구조 비교 】' % ('입자 크기' if size else 'modulus'))

    def values(nm, c):
        return {'Coverage': '%.1f %%' % sec['coverage'][c], 'Pore': '%.1f %%' % sec['porosity'][c],
                'Geometric tortuosity': '%.2f' % sec['tau_geo'][c]}.get(nm)
    _frame_grid(s, sec, 2.28, 6.42, [['Structure', 'Coverage'], ['Pore', 'Geometric tortuosity']], values)


def build_E(s, sec, ch, tag, pe):
    s.keep_only(HEADER_KEEP)
    s.new_creation_id()
    size = sec is SIZE
    p, t, c = sec['porosity'], sec['tau2'], sec['coverage']
    if size:
        b1 = BUL([('입도 감소 시 ', 0), ('기공도 감소', 1), (' (%.1f → %.1f %%) 및 ' % (p[2], p[0]), 0),
                  ('수송 tortuosity 감소', 1), (' (%.2f → %.2f)' % (t[2], t[0]), 0)])
        b2 = BUL([('활물질 coverage는 2 µm에서 최대 (%.1f %%), 1 µm에서 최소 (%.1f %%)' % (c[1], c[0]), 0)])
        head = ' 고체전해질 입도에 따른 '
    else:
        b1 = SYM(sec) + BUL([(' 감소 시 ', 0), ('기공도 감소', 1), (' (%.1f → %.1f %%) 및 ' % (p[2], p[0]), 0),
                             ('수송 tortuosity 감소', 1), (' (%.2f → %.2f)' % (t[2], t[0]), 0)])
        b2 = SYM(sec) + BUL([(' 감소 시 ', 0), ('활물질 coverage 증가', 1), (' (%.1f → %.1f %%)' % (c[2], c[0]), 0)])
        head = ' 고체전해질 기계적 물성에 따른 '
    s.rect_text(HEAD([(head, 0), ('미세구조 지표 변화', 1)]), [b1, b2])
    s.caption('【 고체전해질 %s에 따른 미세구조 지표 변화 】' % ('입자 크기' if size else 'modulus'))
    w, h, y = 2.95, 3.40, 2.72
    for i, key in enumerate(('porosity', 'tortuosity', 'coverage')):
        name = '%s_%s_%s' % (pe, key, tag)
        s.add(PIC(s.nid(), name, s.media(ch[name], 'kg50t_%s.png' % name), 0.45 + i * (w + 0.13), y, w, h))


def build_F(s, sec, a):
    s.keep_only(HEADER_KEEP)
    s.new_creation_id()
    size = sec is SIZE
    head = ' 고체전해질 입도에 따른 ' if size else ' 고체전해질 기계적 물성에 따른 '
    s.rect_text(HEAD([(head, 0), ('활물질·고체전해질 응력 분포', 1), (' (이완 후)', 0)]),
                [BUL([('이완 후 활물질 von Mises 응력 중앙값 %s MPa' % ' / '.join(str(v) for v in sec['am_med']), 0)]),
                 BUL([('이완 후 고체전해질 von Mises 응력 중앙값 %s MPa' % ' / '.join(str(v) for v in sec['se_med']), 0)])])
    s.caption('【 고체전해질 %s에 따른 활물질·고체전해질 응력 분포 (이완 후) 】' % ('입자 크기' if size else 'modulus'))
    top, bot = 2.70, 5.62
    x0, colw, gap = 0.45, 2.953, 0.12
    sw = (colw - 0.30) / 2
    sy = top + 0.52
    sh = bot - 0.05 - 0.20 - 0.04 - sy
    for c in range(3):
        cx0 = x0 + c * (colw + gap)
        s.add(FRAME(s.nid(), 'Bed frame %d' % (c + 1), cx0, top, colw, bot - top))
        s.add(TB(s.nid(), 'Bed label %d' % (c + 1), cx0, top + 0.04, colw, 0.26, bed_label(sec, c)))
        for k, nm in enumerate(('NCM', 'SE')):
            sx = cx0 + 0.10 + k * (sw + 0.10)
            s.add(TB(s.nid(), 'Slot label %s %d' % (nm, c + 1), sx, sy - 0.20, sw, 0.18, LP([LAB(nm, 1000)])))
            s.add(SLOT(s.nid(), 'Image slot %s %d' % (nm, c + 1), sx, sy, sw, sh))
        s.add(TB(s.nid(), 'Plate pressure %d' % (c + 1), cx0, sy + sh + 0.04, colw, 0.20,
                 LP([R('가압판 압력 %d MPa' % sec['p_end'][c], 1000, INK, F_MED)])))
    rid = s.media(a['cbar_h'], 'kg50t_colorbar_jet_h.png')
    for j, (lab, vmax, cx) in enumerate((('von Mises stress in NCM (MPa)', '600', 2.75),
                                         ('von Mises stress in SE (MPa)', '300', 7.25))):
        bw = 2.2
        bx = cx - bw / 2
        s.add(TB(s.nid(), 'Colorbar label %d' % (j + 1), cx - 1.4, 5.70, 2.8, 0.20, LP([LAB(lab, 1000)])))
        s.add(PIC(s.nid(), 'Colorbar %d' % (j + 1), rid, bx, 5.94, bw, 0.12))
        s.add(TB(s.nid(), 'Colorbar min %d' % (j + 1), bx - 0.26, 5.90, 0.20, 0.20, LP([LAB('0', 1000)], algn='r')))
        s.add(TB(s.nid(), 'Colorbar max %d' % (j + 1), bx + bw + 0.06, 5.90, 0.40, 0.20, LP([LAB(vmax, 1000)], algn='l')))


def build_G(s, sec, ch, tag, pg, a):
    s.keep_only(HEADER_KEEP)
    s.new_creation_id()
    size = sec is SIZE
    sg = sec['sigma']
    li = [R('Li', 1600, GRAY, F_BODY, lang='en-US'), R('+', 1600, GRAY, F_BODY, base=SUP, lang='en-US')]
    if size:
        b1 = BUL([('고체전해질 입도에 따른 ', 0)]) + li + BUL([(' 전류 밀도 분포 및 유효 이온전도도 계산', 0)])
        b2 = BUL([('입도 감소에 따라 ', 0), ('유효 이온전도도 증가', 1), (' (%.3f → %.3f' % (sg[2], sg[0]), 0)]) \
            + UNIT_INV() + BUL([(')', 0)])
        head = ' 고체전해질 입도에 따른 '
    else:
        b1 = BUL([('고체전해질 modulus에 따른 ', 0)]) + li + BUL([(' 전류 밀도 분포 및 유효 이온전도도 계산', 0)])
        b2 = SYM(sec) + BUL([(' 감소에 따라 ', 0), ('유효 이온전도도 증가', 1), (' (%.4f → %.4f' % (sg[2], sg[0]), 0)]) \
            + UNIT_INV() + BUL([(')', 0)])
        head = ' 고체전해질 기계적 물성에 따른 '
    s.rect_text(HEAD([(head, 0), ('이온전도도 변화', 1)]), [b1, b2])
    s.caption('【 고체전해질 %s에 따른 유효 이온전도도 변화 】' % ('입자 크기' if size else 'modulus'))
    s.add(FRAME(s.nid(), 'Render frame', 0.68, 2.72, 5.19, 3.62))
    sw, gap, sx0, sy, sh = 1.30, 0.12, 0.80, 3.12, 3.05
    for c in range(3):
        sx = sx0 + c * (sw + gap)
        s.add(TB(s.nid(), 'Bed label %d' % (c + 1), sx - 0.15, 2.80, sw + 0.30, 0.26, bed_label(sec, c)))
        s.add(SLOT(s.nid(), 'Image slot current density %d' % (c + 1), sx, sy, sw, sh))
    bx, by, bw, bh = 5.10, 3.32, 0.11, 2.62
    s.add(PIC(s.nid(), 'Colorbar jet', s.media(a['cbar_v'], 'kg50t_colorbar_jet_v.png'), bx, by, bw, bh))
    s.add(TB(s.nid(), 'Colorbar max (edit)', bx - 0.20, by - 0.24, bw + 0.40, 0.20,
             '<a:p><a:pPr algn="ctr"/><a:endParaRPr lang="en-US" altLang="ko-KR" sz="1000" dirty="0">%s%s</a:endParaRPr></a:p>'
             % (INK, F_MED)))
    s.add(TB(s.nid(), 'Colorbar min', bx - 0.20, by + bh + 0.04, bw + 0.40, 0.20, LP([LAB('0', 1000)])))
    cx, cy, lw = 5.50, by + bh / 2, 2.9
    s.add(TB(s.nid(), 'Colorbar label', cx - lw / 2, cy - 0.11, lw, 0.22,
             LP([LAB('[ Li', 950), LAB('+', 950, base=SUP), LAB(' current density (A cm', 950),
                 LAB('−2', 950, base=SUP), LAB(') ]', 950)]), rot=5400000))
    name = '%s_sigma_%s' % (pg, tag)
    s.add(PIC(s.nid(), name, s.media(ch[name], 'kg50t_%s.png' % name), 6.10, 2.80, 3.20, 3.40))


NOTES = {
    'B': ('D_SE = 1 / 2 / 3 µm: 질량 보존 두께 124.57 / 126.83 / 131.50 µm, 기공도 18.1 / 19.6 / 22.4 %, '
          '경로 그림 칸 옆 값 = 기하 tortuosity 1.22 / 1.28 / 1.37.\n'
          '수송 tortuosity 6.00 / 8.26 / 13.63, 유효 이온전도도 0.070 / 0.050 / 0.029 mS/cm (σ₀ = 1.5 mS/cm 기준).'),
    'C': ('E_SE = 11 / 22 / 33 GPa (22 GPa 의 ×0.5 / ×1 / ×1.5), DEM 유효 입력 0.675 · 1.35 · 2.025 GPa.\n'
          '질량 보존 두께 123.61 / 126.83 / 129.39 µm, 기공도 17.5 / 19.6 / 21.2 %, 수송 tortuosity 7.80 / 8.26 / 9.05.'),
    'SD': ('D_SE = 1 / 2 / 3 µm: coverage 46.8 / 54.2 / 52.6 %, 기공도 18.1 / 19.6 / 22.4 %, '
           '기하 tortuosity (최단 경로 / 두께) 1.22 / 1.28 / 1.37.\n수송 tortuosity 는 다음 장 (미세구조 지표 변화).'),
    'SE': 'D_SE = 1 / 2 / 3 µm: 기공도 (시뮬레이션) 18.1 / 19.6 / 22.4 %, 수송 tortuosity 6.00 / 8.26 / 13.63, coverage 46.8 / 54.2 / 52.6 %.',
    'SF': ('이완 후 von Mises 응력 중앙값 (벽 접촉 입자 제외): 활물질 172 / 335 / 355 MPa, 고체전해질 76 / 126 / 149 MPa.\n'
           '이완 끝 가압판 압력 156 / 280 / 291 MPa (D_SE = 1 / 2 / 3 µm).'),
    'SG': '유효 이온전도도 0.0702 / 0.0501 / 0.0293 mS/cm (σ₀ = 1.5 mS/cm 기준, D_SE = 1 / 2 / 3 µm).',
    'MD': ('E_SE = 11 / 22 / 33 GPa (DEM 유효 입력 0.675 · 1.35 · 2.025 GPa): coverage 61.3 / 54.2 / 48.1 %, '
           '기공도 17.5 / 19.6 / 21.2 %, 기하 tortuosity (최단 경로 / 두께) 1.28 / 1.28 / 1.30.\n'
           '수송 tortuosity 는 다음 장 (미세구조 지표 변화).'),
    'ME': 'E_SE = 11 / 22 / 33 GPa: 기공도 (시뮬레이션) 17.5 / 19.6 / 21.2 %, 수송 tortuosity 7.80 / 8.26 / 9.05, coverage 61.3 / 54.2 / 48.1 %.',
    'MF': ('이완 후 von Mises 응력 중앙값 (벽 접촉 입자 제외): 활물질 353 / 335 / 326 MPa, 고체전해질 85 / 126 / 152 MPa.\n'
           '이완 끝 가압판 압력 278 / 280 / 280 MPa (E_SE = 11 / 22 / 33 GPa).'),
    'MG': '유효 이온전도도 0.0544 / 0.0501 / 0.0448 mS/cm (σ₀ = 1.5 mS/cm 기준, E_SE = 11 / 22 / 33 GPa).',
}


def note_A(stages):
    n = ('D_SE = 1 µm 복합양극: 가압판 높이 {z0:.2f} → {z1:.2f} µm, 가압판 속도 {v} µm/s, 측정 압력은 {t_peak} ms 에 '
         '{p_peak} MPa 에 도달한 뒤 이완 끝 ({t_relax} ms) {p_relax} MPa.').format(**D1)
    names = ['가압 초기', '50 MPa', '300 MPa', '이완 후']
    parts = ['%s step %d · 가압판 %.2f µm · %.0f MPa' % (nm, st['step'], st['plate'], st['pressure'])
             for nm, st in zip(names, stages)]
    return n + '\n기공 렌더 시점: ' + ' / '.join(parts) + '.\n렌더 높이 = 가압판 높이에 비례 (가압 초기 기준) · 바닥 = 집전체 쪽.'


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stdout, r.stderr, file=sys.stderr)
        raise SystemExit('command failed: %s' % ' '.join(map(str, cmd)))
    return r.stdout


def zip_dir(src, dst):
    if dst.exists():
        dst.unlink()
    files = sorted(p for p in src.rglob('*') if p.is_file())
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        ct = src / '[Content_Types].xml'
        z.write(ct, '[Content_Types].xml')
        for p in files:
            if p != ct:
                z.write(p, p.relative_to(src).as_posix())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--template', required=True)
    ap.add_argument('--d1-fig', required=True, help='D1 가압 3단 그림 (다시 만든 그림 경로를 주면 그대로 바뀐다)')
    ap.add_argument('--stage-frames', help='stage_frames_d1.csv (기공 렌더 시점 · 가압판 높이 · recommended 줄)')
    ap.add_argument('--render-init', required=True)
    ap.add_argument('--render-50', required=True)
    ap.add_argument('--render-300', required=True)
    ap.add_argument('--render-d1')
    ap.add_argument('--render-d2')
    ap.add_argument('--render-d3')
    ap.add_argument('--path-d1')
    ap.add_argument('--path-d2')
    ap.add_argument('--path-d3')
    ap.add_argument('--skill-dir', required=True, help='pptx skill folder (scripts/add_slide.py · clean.py)')
    ap.add_argument('--work-dir', required=True)
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--out-name', default='50kg_report_DEM_slides.pptx')
    ap.add_argument('--values-csv')
    ap.add_argument('--metrics-modulus')
    ap.add_argument('--tau-geo-json', nargs=3, metavar=('E05', 'D2', 'E15'),
                    help='metrics_D2E05.json metrics_D2.json metrics_D2E15.json (영률 절 기하 tortuosity 대조)')
    args = ap.parse_args()
    random.seed(20261102)
    verify(args.values_csv, args.metrics_modulus, args.tau_geo_json)
    work, out = Path(args.work_dir), Path(args.out_dir)
    skill = Path(args.skill_dir)
    un = work / 'unpacked'
    if un.exists():
        shutil.rmtree(un)
    un.mkdir(parents=True)
    out.mkdir(parents=True, exist_ok=True)
    assets = work / 'assets'
    assets.mkdir(exist_ok=True)
    with zipfile.ZipFile(args.template) as z:
        z.extractall(un)
    charts = make_charts(out / 'figs')
    stages = read_stages(args.stage_frames) if args.stage_frames else STAGES
    NOTES['A'] = note_A(stages)
    renders = measure_crop_renders([args.render_init, args.render_50, args.render_300], assets)
    size_renders = (measure_crop_renders([args.render_d1, args.render_d2, args.render_d3], assets, prefix='size_render')
                    if (args.render_d1 and args.render_d2 and args.render_d3) else None)
    path_renders = (measure_crop_renders([args.path_d1, args.path_d2, args.path_d3], assets, prefix='size_path')
                    if (args.path_d1 and args.path_d2 and args.path_d3) else None)
    colorbar_png(assets / 'colorbar_jet_h.png', True)
    colorbar_png(assets / 'colorbar_jet_v.png', False)
    d1 = Image.open(args.d1_fig)
    a = dict(d1fig=args.d1_fig, d1_aspect=d1.size[0] / d1.size[1], renders=renders, stages=stages,
             cbar_h=assets / 'colorbar_jet_h.png', cbar_v=assets / 'colorbar_jet_v.png')

    # 구조 먼저 (복제 · 순서) — 내용 편집 전에
    def dup(after):
        o = run([sys.executable, str(skill / 'scripts' / 'add_slide.py'), str(un), 'slide5.xml', '--after', after])
        m = re.search(r'Created ppt/slides/(slide\d+\.xml)', o)
        return m.group(1)
    new = {'A': dup('slide5.xml')}
    for first, keys in (('slide6.xml', ('SD', 'SE', 'SF', 'SG')), ('slide7.xml', ('MD', 'ME', 'MF', 'MG'))):
        prev = first          # 입도 묶음 = 양식 6장 뒤 · 영률 묶음 = 양식 7장 뒤
        for k in keys:
            new[k] = dup(prev)
            prev = new[k]

    jobs = [('A', new['A'], lambda s: build_A(s, a)),
            ('B', 'slide6.xml', lambda s: build_B(s, charts, size_renders, path_renders)),
            ('C', 'slide7.xml', lambda s: build_C(s, charts)),
            ('SD', new['SD'], lambda s: build_D(s, SIZE)),
            ('SE', new['SE'], lambda s: build_E(s, SIZE, charts, 'DSE', 'p09')),
            ('SF', new['SF'], lambda s: build_F(s, SIZE, a)),
            ('SG', new['SG'], lambda s: build_G(s, SIZE, charts, 'DSE', 'p11', a)),
            ('MD', new['MD'], lambda s: build_D(s, MOD)),
            ('ME', new['ME'], lambda s: build_E(s, MOD, charts, 'ESE', 'p14')),
            ('MF', new['MF'], lambda s: build_F(s, MOD, a)),
            ('MG', new['MG'], lambda s: build_G(s, MOD, charts, 'ESE', 'p16', a))]
    for key, fname, fn in jobs:
        s = Slide(un, fname)
        fn(s)
        s.save()
        ensure_notes(un, fname, NOTES[key])
        print('built', key, fname)
    run([sys.executable, str(skill / 'scripts' / 'clean.py'), str(un)])
    dst = out / args.out_name
    zip_dir(un, dst)
    print('wrote', dst)


if __name__ == '__main__':
    main()
