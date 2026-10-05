#!/usr/bin/env python3
"""10-06 보고 6-2 장 그림 — ps45 r4.5 다섯 조성의 접촉 네트워크 σ_ion · σ_e (Hertz · Physics 두 선 · 7:3 빨간 점).
값 = docs/data/ps45_r45_network_webapp_20261005/network_5comp.tsv (웹앱 케이스 페이지 전사 · 업로드 때 계산).
그래프 양식 = 4 장 Coverage 그래프와 같게 (파랑 = 기하 / Hertz · 주황 = Tabor 보정 / Physics · 7:3 빨강 · 점마다 값).
Origin 용 CSV 도 같이 쓴다 (랩 규약: 최종 그래프는 Origin)."""
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.transforms
import matplotlib.ticker
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'data', 'ps45_r45_network_webapp_20261005', 'network_5comp.tsv')
OUT = os.path.join(HERE, 'figs'); os.makedirs(OUT, exist_ok=True)
names = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams['font.family'] = next((f for f in ('Aptos', 'Arial', 'Liberation Sans', 'DejaVu Sans') if f in names), 'sans-serif')
plt.rcParams.update({'font.size': 11, 'axes.linewidth': 1.2, 'xtick.direction': 'in', 'ytick.direction': 'in'})

rows = list(csv.DictReader(open(SRC, encoding='utf-8'), delimiter='\t'))
lab = [r['PC_SC'] for r in rows]
x = list(range(len(rows)))
i73 = lab.index('7:3')
BLUE, ORANGE, RED = '#1f3fff', '#ff8c1a', '#e41a1c'

def fig(kh, kp, ylab, fn, dec):
    yh = [float(r[kh]) for r in rows]; yp = [float(r[kp]) for r in rows]
    f, ax = plt.subplots(figsize=(12 / 2.54, 9 / 2.54), dpi=300)
    for y, c, name, dy in ((yh, BLUE, 'Hertz', 7), (yp, ORANGE, 'Physics (Tabor)', -15)):
        ax.plot(x, y, '-', color=c, lw=1.4)
        ax.plot([i for i in x if i != i73], [v for i, v in enumerate(y) if i != i73], 's', color=c, ms=5)
        ax.plot([i73], [y[i73]], 's', color=RED, ms=6, zorder=5)
        for i, v in enumerate(y):
            ax.annotate(f'{v:.{dec}f}', (i, v), textcoords='offset points', xytext=(0, dy), ha='center', fontsize=8.5)
        ax.text(1.03, y[-1], name, transform=matplotlib.transforms.blended_transform_factory(ax.transAxes, ax.transData),
                fontsize=9, color=c, va='center', clip_on=False)
    ax.set_xticks(x); ax.set_xticklabels(lab)
    ax.set_xlabel('PC:SC (wt%)'); ax.set_ylabel(ylab)
    ax.set_xlim(-0.4, len(x) - 0.6)
    lo = 0; hi = max(yh + yp) * 1.18
    ax.set_ylim(lo, hi)
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: ('0' if abs(v) < 1e-12 else f'{v:g}')))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(True)
    f.subplots_adjust(left=0.17, right=0.76, bottom=0.17, top=0.95)
    for ext in ('png', 'svg'):
        f.savefig(os.path.join(OUT, f'{fn}.{ext}'))
    plt.close(f)

fig('sigma_ion_hertz_mScm', 'sigma_ion_physics_mScm', r'$\sigma_{\mathrm{ion}}$ (mS/cm)', 'fig_sigma_ion', 3)
fig('sigma_e_hertz_mScm', 'sigma_e_physics_mScm', r'$\sigma_{\mathrm{e}}$ (mS/cm)', 'fig_sigma_e', 2)
with open(os.path.join(OUT, 'network_5comp_for_origin.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['PC:SC (wt%)', 'sigma_ion Hertz (mS/cm)', 'sigma_ion Physics (mS/cm)', 'sigma_e Hertz (mS/cm)', 'sigma_e Physics (mS/cm)',
                'tau2 Hertz', 'tau2 Physics'])
    for r in rows:
        w.writerow([r['PC_SC'], r['sigma_ion_hertz_mScm'], r['sigma_ion_physics_mScm'], r['sigma_e_hertz_mScm'], r['sigma_e_physics_mScm'],
                    r['tau2_hertz'], r['tau2_physics']])
print('ok', plt.rcParams['font.family'], sorted(os.listdir(OUT)))
