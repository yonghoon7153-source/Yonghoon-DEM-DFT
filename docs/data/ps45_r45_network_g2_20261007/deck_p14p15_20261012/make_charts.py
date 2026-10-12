#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2차년도 보고 최종 덱 p14 · p15 작은 막대그래프 갱신 — ps45 r4.5 다섯 조성 · 접촉망 세대 2 · Hertz = 주 값.

    cd <이 폴더> && python3 make_charts.py

입력 (읽기만): ../network_cases.tsv (= docs/data/ps45_r45_network_g2_20261007/network_cases.tsv)
출력 (이 폴더):
  p15_sigmaLi_hertz_s0_1p5.{csv,png,svg}     σLi+ · Hertz · σ0 = 1.5 mS/cm (= sigma_full_mScm_hertz × 0.5)
  p14_tortuosity_hertz.{csv,png,svg}          수송 tortuosity · Hertz (= tau2_ion_hertz)
  p14_tortuosity_hertz_tabor.{csv,png,svg}    위 + Tabor (= tau2_ion_physics) 를 막대 위 표지 (○) 로
  preview_p14a_hertz.png · preview_p14b_hertz_tabor.png · preview_p15.png   덱 배치 그대로의 짝 미리보기
서식 = 최종 덱 p14/p15 작은 막대그래프를 PDF 벡터에서 판독한 값 (_inspect/ · NOTES.md §3):
  막대 색 #FDE724 #B4DD2B #6BCD58 #35B778 #1E9C88 · 검은 테두리 0.34 pt · 축 0.68 pt (왼쪽 · 아래만) · 바깥 틱 2.03 / 1.01 pt ·
  눈금 글자 9.22 pt · 축 제목 11.25 pt (Origin 28 / 34 의 비) · 그림 영역 119.5 × 119.6 pt · 막대 폭 = 간격의 50 % · x 범위 = 범주 ± 0.8.
미리보기 글꼴 = Liberation Sans (Aptos 없음 · Arial 과 글자 폭 같음) · 한글 = NanumGothic (맑은 고딕 없음).  Origin 본 그림은 Aptos.
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.legend_handler import HandlerBase
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea
from matplotlib.patches import Rectangle
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

HERE = Path(__file__).resolve().parent
TSV = HERE.parent / 'network_cases.tsv'
ORDER = ['0:10', '3:7', '5:5', '7:3', '10:0']
COLORS = ['#FDE724', '#B4DD2B', '#6BCD58', '#35B778', '#1E9C88']      # 덱 p14/p15 막대 채움 (PDF 벡터 · 0:10 → 10:0)
SIGMA0_SOLVER = 3.0          # mS/cm — 솔버 입력 (se_material.py · TSV ion_sigma0_mScm)
SIGMA0_REPORT = 1.5          # mS/cm — 보고 기준 (1저자 10-12 · README §σ₀)
EXPECT = {'sigma_li_1p5': ([0.0587, 0.0730, 0.0814, 0.0893, 0.0838], 4),
          'tau2_hertz': ([7.24, 5.97, 5.45, 5.03, 5.29], 2),
          'tau2_tabor': ([4.12, 3.35, 3.05, 2.78, 3.13], 2)}

# ── 덱 판독 기하 (슬라이드 pt) ──
PLOT_W, PLOT_H = 119.50, 119.64
AX_LW, BAR_LW = 0.678, 0.341
TICK_MAJ, TICK_MIN = 2.03, 1.01
FS_TICK, FS_TITLE = 9.22, 11.25
BAR_W, XLIM = 0.5, (-0.8, 4.8)
FS_NOTE = 6.6                # 미리보기 각주 · 자리표시 글

YLAB_SIGMA = r'$\sigma_{\mathregular{Li{+}}}$ (mS cm$^{\mathregular{-1}}$)'
YLAB_SIGMA_E = r'$\sigma_{\mathregular{e{-}}}$ (mS cm$^{\mathregular{-1}}$)'
YLAB_TORT = 'Transport tortuosity'

CHARTS = {
    'p15_sigmaLi_hertz_s0_1p5': dict(series='sigma_li_1p5', ylabel=YLAB_SIGMA, ylim=(0.04, 0.10),
                                     yticks=[0.04, 0.06, 0.08, 0.10], yminor=[0.05, 0.07, 0.09], fmt='{:.2f}'),
    'p14_tortuosity_hertz': dict(series='tau2_hertz', ylabel=YLAB_TORT, ylim=(4.5, 7.5),
                                 yticks=[4.5, 5.5, 6.5, 7.5], yminor=[5.0, 6.0, 7.0], fmt='{:.1f}'),
    'p14_tortuosity_hertz_tabor': dict(series='tau2_hertz', marker='tau2_tabor', ylabel=YLAB_TORT, ylim=(2.0, 8.0),
                                       yticks=[2, 4, 6, 8], yminor=[3, 5, 7], fmt='{:.0f}'),
}


def write_origin_csv(path, head, units, rows):
    """리포 규약 (docs/data/ps73_compaction_curve_20261006/make_fig_ms.py) — 1 줄 Long Name · 2 줄 Units · 그 뒤 자료 · utf-8-sig."""
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        w.writerow(units)
        w.writerows(rows)


def load_and_verify():
    rows = {r['P_S']: r for r in csv.DictReader(open(TSV, encoding='utf-8'), delimiter='\t')}
    missing = [x for x in ORDER if x not in rows]
    if missing or len(rows) != 5:
        sys.exit(f'⛔ TSV 조성 결손 · 개수 {len(rows)} · 없음 {missing}')
    prob = []
    for x in ORDER:
        r = rows[x]
        need = {'run_status': 'done', 'ion_net_status_hertz': 'OK', 'ion_net_status_physics': 'OK',
                'sigma_full_status_hertz': 'computed', 'psi_placement_physics': 'multiply', 'ion_net_generation': 'g2'}
        prob += [f'{x} {k}={r[k]!r}' for k, v in need.items() if r[k] != v]
        if abs(float(r['ion_sigma0_mScm']) - SIGMA0_SOLVER) > 1e-12 or abs(float(r['sigma_grain_S_cm']) - SIGMA0_SOLVER * 1e-3) > 1e-15:
            prob.append(f'{x} σ0 ≠ {SIGMA0_SOLVER}')
    if prob:
        sys.exit('⛔ ' + ' | '.join(prob))
    sig30 = [float(rows[x]['sigma_full_mScm_hertz']) for x in ORDER]
    s = {'sigma_li_3p0': sig30,
         'sigma_li_1p5': [v * SIGMA0_REPORT / SIGMA0_SOLVER for v in sig30],      # 망 σ ∝ σ0 (README §σ₀)
         'sigma_li_tabor_1p5': [float(rows[x]['sigma_full_mScm_physics']) * SIGMA0_REPORT / SIGMA0_SOLVER for x in ORDER],
         'tau2_hertz': [float(rows[x]['tau2_ion_hertz']) for x in ORDER],
         'tau2_tabor': [float(rows[x]['tau2_ion_physics']) for x in ORDER]}
    for key, (exp, nd) in EXPECT.items():
        got = [round(v, nd) for v in s[key]]
        if got != exp:
            sys.exit(f'⛔ {key} 기대 {exp} ↔ 계산 {got}')
    # 항등식 tau2 = φ_SE·σ0/σ_eff — 판 간격 틀 (phi_se · sigma_full) 과 질량 보존 틀 (phi_se_mass_conserving / f_ion) 두 길
    chk = {}
    for mode, scol in (('hertz', 'sigma_full_mScm_hertz'), ('physics', 'sigma_full_mScm_physics')):
        t2 = [float(rows[x][f'tau2_ion_{mode}']) for x in ORDER]
        gap = [float(rows[x]['phi_se']) * SIGMA0_SOLVER / float(rows[x][scol]) for x in ORDER]
        gap15 = [float(rows[x]['phi_se']) * SIGMA0_REPORT / (float(rows[x][scol]) * SIGMA0_REPORT / SIGMA0_SOLVER) for x in ORDER]
        mc = [float(rows[x]['phi_se_mass_conserving']) / float(rows[x][f'f_ion_{mode}']) for x in ORDER]
        chk[mode] = {'gap_frame_max_rel': max(abs(a / b - 1) for a, b in zip(gap, t2)),
                     'gap_frame_sigma0_1p5_max_rel': max(abs(a / b - 1) for a, b in zip(gap15, t2)),
                     'mass_conserving_frame_max_rel': max(abs(a / b - 1) for a, b in zip(mc, t2))}
        if max(chk[mode].values()) > 1e-5:
            sys.exit(f'⛔ tau2 항등식 어긋남 {mode} {chk[mode]}')
    return s, chk


def setup_style():
    fm.fontManager.addfont('/usr/share/fonts/truetype/nanum/NanumGothic.ttf')   # 미리보기 한글 (맑은 고딕 대용)
    plt.rcParams.update({
        'font.family': ['Liberation Sans', 'NanumGothic'], 'font.size': FS_TICK,
        'mathtext.fontset': 'custom', 'mathtext.rm': 'Liberation Sans', 'mathtext.it': 'Liberation Sans:italic',
        'mathtext.bf': 'Liberation Sans:bold',
        'text.color': 'black', 'axes.edgecolor': 'black', 'axes.labelcolor': 'black', 'xtick.color': 'black', 'ytick.color': 'black',
        'axes.linewidth': AX_LW, 'xtick.direction': 'out', 'ytick.direction': 'out',
        'xtick.major.size': TICK_MAJ, 'ytick.major.size': TICK_MAJ, 'ytick.minor.size': TICK_MIN,
        'xtick.major.width': AX_LW, 'ytick.major.width': AX_LW, 'ytick.minor.width': AX_LW,
        'xtick.major.pad': 1.6, 'ytick.major.pad': 1.6,
        'xtick.labelsize': FS_TICK, 'ytick.labelsize': FS_TICK, 'axes.labelsize': FS_TITLE,
        'axes.unicode_minus': True, 'svg.fonttype': 'none', 'svg.hashsalt': 'deck-p14p15-20261012',
    })


class _Ramp:
    """범례 대리 — '이 색 막대들' (조성마다 색이 달라 단색 칸이 틀린 신호가 된다)."""


class _RampHandler(HandlerBase):
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        w = width / len(COLORS)
        arts = [Rectangle((-xdescent + i * w, -ydescent), w, height, facecolor=c, edgecolor='none', lw=0, transform=trans)
                for i, c in enumerate(COLORS)]
        arts.append(Rectangle((-xdescent, -ydescent), width, height, facecolor='none', edgecolor='black', lw=BAR_LW, transform=trans))
        return arts


def draw_chart(ax, spec, s):
    base = spec['ylim'][0]
    vals = s[spec['series']]
    ax.bar(range(5), [v - base for v in vals], bottom=base, width=BAR_W, color=COLORS, edgecolor='black', linewidth=BAR_LW, zorder=2)
    if spec.get('marker'):
        ax.plot(range(5), s[spec['marker']], ls='none', marker='o', ms=5.0, mfc='white', mec='black', mew=AX_LW, zorder=3)
    ax.set_xlim(*XLIM)
    ax.set_ylim(*spec['ylim'])
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_linewidth(AX_LW)
        ax.spines[side].set_capstyle('projecting')
    ax.xaxis.set_major_locator(FixedLocator(range(5)))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels(ORDER)
    ax.yaxis.set_major_locator(FixedLocator(spec['yticks']))
    ax.yaxis.set_minor_locator(FixedLocator(spec['yminor']))
    fmt = spec['fmt']
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt.format(v)))
    ax.tick_params(axis='y', which='minor', length=TICK_MIN, width=AX_LW)
    ax.set_xlabel('PC:SC mass ratio', labelpad=0.8)
    ax.set_ylabel(spec['ylabel'], labelpad=1.6)
    if spec.get('marker'):
        ax.legend([_Ramp(), Line2D([], [], ls='none', marker='o', ms=5.0, mfc='white', mec='black', mew=AX_LW)],
                  ['Hertz', 'Tabor'], handler_map={_Ramp: _RampHandler()}, loc='lower left', bbox_to_anchor=(0.0, 1.015),
                  ncol=2, frameon=False, fontsize=FS_TICK, handlelength=1.7, handleheight=0.75, handletextpad=0.45,
                  columnspacing=1.3, borderaxespad=0.0, borderpad=0.0)


def placeholder(ax, lines, top=1.0):
    """덱 원본을 그대로 두는 자리 — 같은 그림 영역 크기의 점선 칸 + 안내 글 (top < 1 = 위 그림의 x 축 제목과 겹치지 않게 내림)."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 1, top, transform=ax.transAxes, facecolor='#F4F4F4', edgecolor='#8A8A8A', lw=0.6, ls=(0, (3, 2))))
    n = len(lines)
    for i, (t, size, color) in enumerate(lines):
        ax.text(0.5, top / 2 + (n / 2 - i - 0.5) * 0.14, t, ha='center', va='center', fontsize=size, color=color, transform=ax.transAxes)


def svg_font_fallback(path):
    """SVG 글자는 글자로 둔다 (편집 가능) — Liberation Sans 가 없는 PC (Windows) 에서는 글자 폭이 같은 Arial 로 그려지게 대체 목록을 붙인다."""
    s = path.read_text(encoding='utf-8')
    s = s.replace("font-family: 'Liberation Sans', 'NanumGothic'", "font-family: 'Liberation Sans', Arial, 'NanumGothic', 'Malgun Gothic', sans-serif")
    s = s.replace("font-family: 'Liberation Sans'\"", "font-family: 'Liberation Sans', Arial, sans-serif\"")
    s = s.replace("font-family: 'Liberation Sans';", "font-family: 'Liberation Sans', Arial, sans-serif;")
    path.write_text(s, encoding='utf-8')


def rich_line(fig, x, y, parts, size=FS_NOTE, color='#404040'):
    """한글 (보통 글) + 수식 조각을 기준선 맞춰 한 줄로 — matplotlib 수식 안에서는 한글 글리프 대체가 안 된다."""
    box = HPacker(children=[TextArea(t, textprops=dict(fontsize=size, color=color)) for t in parts], align='baseline', pad=0, sep=0)
    fig.add_artist(AnchoredOffsetbox(loc='lower left', child=box, pad=0, borderpad=0, frameon=False,
                                     bbox_to_anchor=(x, y), bbox_transform=fig.transFigure))


def save_single(name, spec, s):
    top = 24.0 if spec.get('marker') else 8.0
    L, R, B = 46.0, 6.0, 30.0
    fw, fh = L + PLOT_W + R, top + PLOT_H + B
    fig = plt.figure(figsize=(fw / 72, fh / 72))
    ax = fig.add_axes([L / fw, B / fh, PLOT_W / fw, PLOT_H / fh])
    draw_chart(ax, spec, s)
    fig.savefig(HERE / f'{name}.png', dpi=300, bbox_inches='tight', pad_inches=3 / 72)
    fig.savefig(HERE / f'{name}.svg', bbox_inches='tight', pad_inches=3 / 72, metadata={'Date': None})
    plt.close(fig)
    svg_font_fallback(HERE / f'{name}.svg')


def deck_figure(region):
    X0, Y0, X1, Y1 = region
    fw, fh = X1 - X0, Y1 - Y0
    fig = plt.figure(figsize=(fw / 72, fh / 72))

    def axes_at(x_left, y_top):          # 덱 좌표 (pt · 위에서 아래로) 의 그림 영역 왼쪽 위 → figure 비율
        return fig.add_axes([(x_left - X0) / fw, 1 - (y_top + PLOT_H - Y0) / fh, PLOT_W / fw, PLOT_H / fh])

    def fy(y):
        return 1 - (y - Y0) / fh

    def fx(x):
        return (x - X0) / fw

    return fig, axes_at, fx, fy


TORT_NOTE = ['수송 tortuosity = ', r'$\varphi_{\mathregular{SE}}\cdot\sigma_{0}/\sigma_{\mathregular{eff}}$', ' — ', r'$\sigma_{0}$', ' 와 무관']


def save_p14(name, spec, s, tabor):
    # 덱 p14 배치: Tortuosity 그림 영역 왼쪽 x 75.19 · Coverage 236.08 · 둘 다 위 y 375.80 (pt)
    fig, axes_at, fx, fy = deck_figure((28, 334, 372, 562))
    draw_chart(axes_at(75.19, 375.80), spec, s)
    placeholder(axes_at(236.08, 375.80), [('Coverage (%)', FS_TICK, 'black'),
                                          ('덱 원본 그대로 (변경 없음)', FS_NOTE, '#404040'),
                                          ('이 TSV 에 coverage 열 없음', FS_NOTE, '#404040'),
                                          ("x 눈금 '5:7' → '5:5' 오타만", FS_NOTE, '#B00020')])
    fig.text(fx(31), fy(340), 'p14 미리보기 — 왼쪽 = 새 Transport tortuosity (Hertz' + (' + Tabor 표지)' if tabor else ')') +
             ' · 오른쪽 = Coverage 덱 그대로 (자리표시)', fontsize=FS_NOTE, color='#7A7A7A', va='top')
    rich_line(fig, fx(40), fy(535), TORT_NOTE)
    if tabor:
        rich_line(fig, fx(40), fy(546), ['막대 = Hertz 접촉 면적 기준 (주 값) · ○ = Tabor = 접촉 면적 규약 민감도'])
    else:
        rich_line(fig, fx(40), fy(546), ['Hertz 접촉 면적 기준 (주 값)'])
    fig.savefig(HERE / f'{name}.png', dpi=300)
    plt.close(fig)


def save_p15(name, s):
    # 덱 p15 배치: σLi+ 그림 영역 왼쪽 x 605.15 · 위 y 230.60 / σe− 위 y 372.20 (pt) — 위아래 짝
    fig, axes_at, fx, fy = deck_figure((540, 200, 748, 566))
    draw_chart(axes_at(605.15, 230.60), CHARTS['p15_sigmaLi_hertz_s0_1p5'], s)
    ax_e = axes_at(605.15, 372.20)
    placeholder(ax_e, [(YLAB_SIGMA_E, FS_TICK, 'black'),
                       ('덱 원본 그대로 — 새로 그리지 않음', FS_NOTE, '#404040'),
                       ('기준 (σAM · 면적 규약) 검토 중', FS_NOTE, '#404040'),
                       ("x 눈금 '5:7' → '5:5' 오타만", FS_NOTE, '#B00020')], top=0.90)
    fig.text(fx(543), fy(206), 'p15 미리보기 — 위 = 새 σLi+ (Hertz · σ₀ 1.5)', fontsize=FS_NOTE, color='#7A7A7A', va='top')
    fig.text(fx(543), fy(214), '아래 = σe− 덱 그대로 (자리표시)', fontsize=FS_NOTE, color='#7A7A7A', va='top')
    rich_line(fig, fx(560), fy(536), [r'$\sigma_{0}$', ' = 1.5 mS cm', r'$^{\mathregular{-1}}$', ' (LPSCl 펠릿 문헌 범위)'])
    rich_line(fig, fx(560), fy(547), ['Hertz 접촉 면적 기준 (주 값)'])
    rich_line(fig, fx(560), fy(558), ['Tabor = 접촉 면적 규약 민감도'])
    fig.savefig(HERE / f'{name}.png', dpi=300)
    plt.close(fig)


def main():
    s, chk = load_and_verify()
    setup_style()
    f7 = lambda v: f'{v:.7g}'
    f10 = lambda v: f'{v:.10g}'
    write_origin_csv(HERE / 'p15_sigmaLi_hertz_s0_1p5.csv', ['PC:SC mass ratio', 'σLi+', 'Basis'], ['', 'mS cm-1', ''],
                     [(x, f7(v), 'Hertz · σ0 = 1.5 mS/cm (TSV sigma_full_mScm_hertz × 0.5)') for x, v in zip(ORDER, s['sigma_li_1p5'])])
    write_origin_csv(HERE / 'p14_tortuosity_hertz.csv', ['PC:SC mass ratio', 'Transport tortuosity', 'Basis'], ['', '', ''],
                     [(x, f10(v), 'Hertz · tau2 = φSE·σ0/σeff (TSV tau2_ion_hertz)') for x, v in zip(ORDER, s['tau2_hertz'])])
    write_origin_csv(HERE / 'p14_tortuosity_hertz_tabor.csv',
                     ['PC:SC mass ratio', 'Transport tortuosity (Hertz)', 'Transport tortuosity (Tabor)', 'Basis'], ['', '', '', ''],
                     [(x, f10(a), f10(b), 'Hertz = main (TSV tau2_ion_hertz) · Tabor = sensitivity (TSV tau2_ion_physics)')
                      for x, a, b in zip(ORDER, s['tau2_hertz'], s['tau2_tabor'])])
    for name, spec in CHARTS.items():
        save_single(name, spec, s)
    save_p14('preview_p14a_hertz', CHARTS['p14_tortuosity_hertz'], s, tabor=False)
    save_p14('preview_p14b_hertz_tabor', CHARTS['p14_tortuosity_hertz_tabor'], s, tabor=True)
    save_p15('preview_p15', s)
    print('조성            ', ORDER)
    print('σLi+ Hertz σ0 3.0', [round(v, 6) for v in s['sigma_li_3p0']])
    print('σLi+ Hertz σ0 1.5', [round(v, 7) for v in s['sigma_li_1p5']], '→', [round(v, 4) for v in s['sigma_li_1p5']])
    print('σLi+ Tabor σ0 1.5', [round(v, 4) for v in s['sigma_li_tabor_1p5']])
    print('tau2 Hertz       ', [round(v, 4) for v in s['tau2_hertz']])
    print('tau2 Tabor       ', [round(v, 4) for v in s['tau2_tabor']])
    print('Tabor/Hertz tau2 ', [round(b / a, 3) for a, b in zip(s['tau2_hertz'], s['tau2_tabor'])])
    print('항등식 (최대 상대차)', {m: {k: f'{v:.1e}' for k, v in d.items()} for m, d in chk.items()})


if __name__ == '__main__':
    main()
