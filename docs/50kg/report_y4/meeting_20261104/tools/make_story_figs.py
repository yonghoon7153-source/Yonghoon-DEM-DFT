"""진도점검 덱 이야기 보강 그림 넷 (1저자 11-02 "story로도 잘 넣어봐요" · "다 권고대로" · σzz = 부록 표만) — 값 = metrics_all.csv · p5_breakeven_sigma.csv 그대로.
  s6_cn_network  : 입자 1개당 배위수 — SE–SE (SE 1개당) · AM–AM (AM 1개당) 두 칸 (같은 y 축 · 범례 없음)
  s6_disconnected: 위아래로 이어진 SE 망에 들지 않은 SE 비율 = 100 − percolation_pct
  s7_sigma_li    : 유효 이온전도도 = f_ion_hertz × σ0 1.5 mS/cm (보고 기준 · 전해질 물성 동일 가정)
  s8_net         : 1 µm ÷ 3 µm — 구조 (정규화 유효 이온전도도 비) × pellet 이온전도도 비 = 곱
python3 -I make_story_figs.py <repo> <outdir>   (크기 = 덱 그림 칸 4.30 × 2.70 in · 300 dpi · 투명 · make_d4_figs_wqy.py 와 같은 꼴)
"""
import csv
import json
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
FW, FH = 4.30, 2.70
SIGMA0 = 1.5
OUT.mkdir(parents=True, exist_ok=True)
D2 = REPO / 'docs/50kg/report_y4/draft2'
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
plt.rcParams.update({
    'font.family': ['WenQuanYi Zen Hei', 'DejaVu Sans'], 'font.size': 10, 'axes.linewidth': 0.9,
    'axes.edgecolor': '#262626', 'axes.spines.top': False, 'axes.spines.right': False,
    'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.major.size': 3, 'ytick.major.size': 3,
    'xtick.labelsize': 10.5, 'ytick.labelsize': 10, 'axes.labelsize': 10.5, 'text.color': '#262626',
    'axes.labelcolor': '#262626', 'xtick.color': '#262626', 'ytick.color': '#262626', 'svg.fonttype': 'none',
    'svg.hashsalt': 'kg50-y4-story', 'axes.unicode_minus': False,
})
INK, INK2, RED = '#262626', '#595959', '#FF5050'
C = {'D3': '#0d366b', 'D2': '#1c5cab', 'D1': '#3987e5'}
ORDER = ('D3', 'D2', 'D1')
LAB = {'D3': '3', 'D2': '2', 'D1': '1'}
rows = {r['bed']: r for r in csv.DictReader(open(D2 / 'metrics_all.csv', encoding='utf-8'))}
be = list(csv.DictReader(open(D2 / 'figs/p5_breakeven_sigma.csv', encoding='utf-8')))
meas = {r['bed']: float(r['sigma_meas_mScm']) for r in be if r['kind'] == 'measured' and r['sigma_meas_mScm'] and r['bed'] in ORDER}
v = lambda b, k: float(rows[b][k])
meta = {'source': ['docs/50kg/report_y4/draft2/metrics_all.csv', 'docs/50kg/report_y4/draft2/figs/p5_breakeven_sigma.csv'],
        'sigma0_report_mScm': SIGMA0, 'values': {}, 'files': {}}


def save(fig, stem):
    for ext in ('png', 'svg'):
        fig.savefig(OUT / f'{stem}.{ext}', dpi=300, transparent=True, metadata={'Date': None} if ext == 'svg' else {'Software': None})
    plt.close(fig)
    meta['files'][stem] = f'{stem}.png'


def bars(ax, vals, fmt, ymax, xlabel=True):
    for x, b in enumerate(ORDER):
        ax.bar(x, vals[b], width=0.56, color=C[b], edgecolor=C[b], linewidth=1.2, zorder=3)
        ax.text(x, vals[b] + ymax * 0.025, fmt(vals[b]), ha='center', va='bottom', fontsize=11, color=INK, fontweight='bold')
    ax.set_xticks(range(len(ORDER)))
    ax.set_xticklabels([LAB[b] for b in ORDER])
    ax.set_xlim(-0.6, len(ORDER) - 0.4)
    ax.set_ylim(0, ymax)
    ax.tick_params(axis='x', length=0, pad=5)
    if xlabel:
        ax.set_xlabel(r'$D_\mathrm{SE}$ (µm)', labelpad=3)


# s6 — 배위수 두 칸 (같은 y 축)
cn_se = {b: v(b, 'se_se_cn_mean') for b in ORDER}
cn_am = {b: v(b, 'am_am_cn_mean') for b in ORDER}
fig = plt.figure(figsize=(FW, FH))
for k, (vals, lab) in enumerate(((cn_se, 'SE–SE CN (per SE)'), (cn_am, 'AM–AM CN (per AM)'))):
    left = 0.55 + k * 2.00
    ax = fig.add_axes([left / FW, 0.50 / FH, 1.55 / FW, (FH - 0.50 - 0.22) / FH])
    bars(ax, vals, lambda x: f'{x:.1f}', 6.6)
    ax.set_yticks([0, 2, 4, 6])
    ax.set_ylabel(lab, fontsize=10)
save(fig, 's6_cn_network')
meta['values']['se_se_cn_mean'] = cn_se
meta['values']['am_am_cn_mean'] = cn_am

# s6 — 망에 들지 않은 SE 비율
disc = {b: 100.0 - v(b, 'percolation_pct') for b in ORDER}
fig = plt.figure(figsize=(FW, FH))
ax = fig.add_axes([0.62 / FW, 0.50 / FH, (FW - 0.62 - 0.12) / FW, (FH - 0.50 - 0.22) / FH])
bars(ax, disc, lambda x: f'{x:.1f}%', 6.0)
ax.set_yticks([0, 2, 4, 6])
ax.set_ylabel('SE outside spanning network (%)', fontsize=9.5)
save(fig, 's6_disconnected')
meta['values']['se_outside_spanning_pct'] = disc
meta['values']['se_outside_spanning_definition'] = '100 − percolation_pct (calc_percolation · 위아래 판 쪽에 모두 닿는 SE 덩어리에 들지 않은 SE 입자 비율)'

# s7 — 유효 이온전도도 (σ0 1.5 기준)
sig = {b: SIGMA0 * v(b, 'f_ion_hertz') for b in ORDER}
fig = plt.figure(figsize=(FW, FH))
ax = fig.add_axes([0.70 / FW, 0.50 / FH, (FW - 0.70 - 0.12) / FW, (FH - 0.50 - 0.22) / FH])
bars(ax, sig, lambda x: f'{x:.3f}', 0.09)
ax.set_yticks([0, 0.03, 0.06, 0.09])
ax.set_yticklabels(['0', '0.03', '0.06', '0.09'])
ax.set_ylabel(r'$\sigma_\mathrm{Li^+}$ (mS cm$^{-1}$)')
save(fig, 's7_sigma_li')
meta['values']['sigma_li_mScm'] = sig
meta['values']['sigma_li_basis'] = 'f_ion_hertz × σ0 1.5 mS/cm (보고 기준 · 1저자 10-12)'

# s8 — 1 µm ÷ 3 µm: 구조 × pellet = 곱
gain = v('D1', 'f_ion_hertz') / v('D3', 'f_ion_hertz')
loss = meas['D1'] / meas['D3']
net = gain * loss
fig = plt.figure(figsize=(FW, FH))
ax = fig.add_axes([0.62 / FW, 0.62 / FH, (FW - 0.62 - 0.12) / FW, (FH - 0.62 - 0.22) / FH])
items = [('Structure', gain, C['D2']), ('Pellet σ', loss, RED), ('Net', net, INK2)]
for x, (lab, val, col) in enumerate(items):
    ax.bar(x, val, width=0.56, color=col, edgecolor=col, linewidth=1.2, zorder=3)
    ax.text(x, val + 0.07, f'{val:.2f}' if lab == 'Pellet σ' else f'{val:.1f}', ha='center', va='bottom', fontsize=11, color=INK,
            fontweight='bold')
ax.axhline(1.0, color=INK2, lw=0.8, ls=(0, (3, 2)), zorder=2)
ax.set_xticks(range(3))
ax.set_xticklabels([r'Structure' '\n' r'($\sigma_\mathrm{eff}/\sigma_\mathrm{0}$)', r'Pellet $\sigma$', r'Net'])
ax.set_xlim(-0.6, 2.6)
ax.set_ylim(0, 3.0)
ax.set_yticks([0, 1, 2, 3])
ax.tick_params(axis='x', length=0, pad=4)
ax.set_ylabel('1 µm / 3 µm')
save(fig, 's8_net')
meta['values']['net'] = {'structure_gain': gain, 'pellet_ratio': loss, 'net': net, 'pellet_mScm': meas}
(OUT / 'story_figs_meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(json.dumps(meta['values'], ensure_ascii=False, default=lambda o: round(o, 4))[:900])
