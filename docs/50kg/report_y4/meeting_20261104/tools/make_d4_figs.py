"""50kg 4차년도 보고 초안 4 (7쪽 스토리판 · D1 · D2 · D3) 막대 그림 — metrics_all.csv · p5_breakeven_sigma.csv 값 그대로.
python3 make_d4_figs.py <repo> <outdir>
"""
import csv
import json
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
FW, FH = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (4.30, 2.75)
OUT.mkdir(parents=True, exist_ok=True)
D2 = REPO / 'docs/50kg/report_y4/draft2'
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
plt.rcParams.update({
    'font.family': ['Carlito', 'WenQuanYi Zen Hei', 'DejaVu Sans'], 'font.size': 10, 'axes.linewidth': 0.9,
    'axes.edgecolor': '#262626', 'axes.spines.top': False, 'axes.spines.right': False,
    'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.major.size': 3, 'ytick.major.size': 3,
    'xtick.labelsize': 10.5, 'ytick.labelsize': 10, 'axes.labelsize': 10.5, 'text.color': '#262626',
    'axes.labelcolor': '#262626', 'xtick.color': '#262626', 'ytick.color': '#262626', 'svg.fonttype': 'none',
    'svg.hashsalt': 'kg50-y4-d4', 'axes.unicode_minus': False, 'hatch.linewidth': 0.6,
})
INK, INK2 = '#262626', '#595959'
C = {'D3': '#0d366b', 'D2': '#1c5cab', 'D1': '#3987e5'}
ORDER = ('D3', 'D2', 'D1')
LAB = {'D3': '3', 'D2': '2', 'D1': '1'}

rows = {r['bed']: r for r in csv.DictReader(open(D2 / 'metrics_all.csv', encoding='utf-8'))}
be = list(csv.DictReader(open(D2 / 'figs/p5_breakeven_sigma.csv', encoding='utf-8')))
M = {b: {k: float(rows[b][k]) for k in ('eps_union_exact_pct', 'am_se_cn_mean', 'f_ion_hertz', 'p_end_MPa', 'area_am_se_per_am_mean_um2')}
     for b in ORDER}
band = {r['bed']: (float(r['band_lo_mScm']), float(r['band_hi_mScm'])) for r in be if r['kind'] == 'band'}
meas = {r['bed']: float(r['sigma_meas_mScm']) for r in be if r['kind'] == 'measured' and r['sigma_meas_mScm'] and r['bed'] in ORDER}
req_hertz = {r['bed']: float(r['sigma_req_mScm']) for r in be if r['kind'] == 'required' and r['basis'] == 'f_mc Hertz'}
meta = {'source': ['docs/50kg/report_y4/draft2/metrics_all.csv', 'docs/50kg/report_y4/draft2/figs/p5_breakeven_sigma.csv'],
        'values': {}, 'files': {}}


def axes(w=None, h=None, left=0.62, bottom=0.50, right=0.12, top=0.22):
    w, h = w or FW, h or FH
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([left / w, bottom / h, (w - left - right) / w, (h - bottom - top) / h])
    return fig, ax


def save(fig, stem):
    for ext in ('png', 'svg'):
        p = OUT / f'{stem}.{ext}'
        fig.savefig(p, dpi=300, transparent=True, metadata={'Date': None} if ext == 'svg' else {'Software': None})
    plt.close(fig)
    meta['files'][stem] = f'{stem}.png'


def bars(ax, vals, fmt, ymax, hatch_d1=False, label_dy=None):
    xs = range(len(ORDER))
    for x, b in zip(xs, ORDER):
        v = vals[b]
        light = hatch_d1 and b == 'D1'
        ax.bar(x, v, width=0.56, color='white' if light else C[b], edgecolor=C[b], linewidth=1.2,
               hatch='////' if light else None, zorder=3)
        ax.text(x, v + (label_dy if label_dy is not None else ymax * 0.025), fmt(v), ha='center', va='bottom', fontsize=11.5,
                color=INK, fontweight='bold')
    ax.set_xticks(list(xs))
    ax.set_xticklabels([LAB[b] for b in ORDER])
    ax.set_xlim(-0.6, len(ORDER) - 0.4)
    ax.set_ylim(0, ymax)
    ax.tick_params(axis='x', length=0, pad=5)
    ax.set_xlabel(r'$D_\mathrm{SE}$ (µm)', labelpad=3)


# 1) 기공률 (이완 끝 · ε_sphere) — 1 µm 는 빗금 (판 압력 156 MPa)
fig, ax = axes()
bars(ax, {b: M[b]['eps_union_exact_pct'] for b in ORDER}, lambda v: f'{v:.1f}%', 28, hatch_d1=True)
ax.set_yticks([0, 10, 20])
ax.set_ylabel('Porosity (%)')
save(fig, 'd4_porosity')
fig, ax = axes()
bars(ax, {b: M[b]['eps_union_exact_pct'] for b in ORDER}, lambda v: f'{v:.1f}%', 28)
ax.set_yticks([0, 10, 20])
ax.set_ylabel('Porosity (%)')
save(fig, 'd4_porosity_plain')
meta['values']['porosity_pct'] = {b: M[b]['eps_union_exact_pct'] for b in ORDER}
meta['values']['porosity_basis'] = 'eps_union_exact_pct (exact union · 1저자 11-02)'

# 2) 활물질 1개당 SE 접촉 수
fig, ax = axes()
bars(ax, {b: M[b]['am_se_cn_mean'] for b in ORDER}, lambda v: f'{v:.0f}', 120)
ax.set_yticks([0, 50, 100])
ax.set_ylabel('AM–SE contacts (per AM)')
save(fig, 'd4_contacts')
meta['values']['am_se_cn_mean'] = {b: M[b]['am_se_cn_mean'] for b in ORDER}

# 3) 이온 전달 (구조 전달계수 f, 3 µm 대비)
f3 = M['D3']['f_ion_hertz']
rel = {b: M[b]['f_ion_hertz'] / f3 for b in ORDER}
fig, ax = axes()
bars(ax, rel, lambda v: f'×{v:.1f}', 3.0)
ax.set_yticks([0, 1, 2, 3])
ax.axhline(1.0, color=INK2, lw=0.8, ls=(0, (3, 2)), zorder=2)
ax.set_ylabel(r'Normalized $\sigma_\mathrm{eff}$ (vs. 3 µm)')
save(fig, 'd4_ion_path')
meta['values']['f_rel_3um'] = rel
meta['values']['f_ion_hertz'] = {b: M[b]['f_ion_hertz'] for b in ORDER}

# 4) SE 펠릿 이온전도도 실측 (3차년도) — 3 µm · 1 µm 만 (2 µm 실측 없음)
fig, ax = axes()
pv = {'D3': meas['D3'], 'D1': meas['D1']}
for x, b in enumerate(('D3', 'D1')):
    ax.bar(x, pv[b], width=0.5, color=C[b], edgecolor=C[b], linewidth=1.2, zorder=3)
    ax.text(x, pv[b] + 0.15, f'{pv[b]:.1f}', ha='center', va='bottom', fontsize=11.5, fontweight='bold')
ax.set_xticks([0, 1])
ax.set_xticklabels(['3', '1'])
ax.set_xlim(-0.6, 1.6)
ax.set_ylim(0, 6.5)
ax.set_yticks([0, 2, 4, 6])
ax.tick_params(axis='x', length=0, pad=5)
ax.set_xlabel(r'$D_\mathrm{SE}$ (µm)', labelpad=3)
ax.set_ylabel(r'Pellet $\sigma$ (mS/cm)')   # 1저자 11-02 "italic 같은거 잘 지키고" — σ = 변수 이탤릭 (D_SE 와 같은 mathtext)
save(fig, 'd4_pellet_sigma')
meta['values']['pellet_sigma_mScm'] = pv

# 5) 필요한 SE 이온전도도 (3 µm 전극과 같아지는 값) vs 실측
fig, ax = axes()
for x, b in enumerate(ORDER):
    if b == 'D3':
        ax.bar(x, meas['D3'], width=0.56, color='#BFBFBF', edgecolor='#7F7F7F', linewidth=1.0, zorder=3)
        ax.text(x, meas['D3'] + 0.15, '5.1 (ref.)', ha='center', va='bottom', fontsize=10.5, fontweight='bold')
        continue
    lo, hi = band[b]
    ax.bar(x, hi - lo, bottom=lo, width=0.56, color='#BFBFBF', edgecolor='#7F7F7F', linewidth=1.0, zorder=3)
    ax.bar(x, lo, width=0.56, color='#F2F2F2', edgecolor='#BFBFBF', linewidth=0.8, zorder=2)
    ax.text(x, hi + 0.15, f'{lo:.1f}–{hi:.1f}', ha='center', va='bottom', fontsize=10.5, fontweight='bold')
    if b in meas:
        ax.plot([x + 0.40], [meas[b]], marker='D', ms=8, color='#C55A11', zorder=5, clip_on=False)
        ax.text(x + 0.52, meas[b], f'{meas[b]:.1f}', ha='left', va='center', fontsize=10.5, color='#C55A11', fontweight='bold')
ax.plot([0.40], [meas['D3']], marker='D', ms=8, color='#C55A11', zorder=5)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels([LAB[b] for b in ORDER])
ax.set_xlim(-0.6, 2.75)
ax.set_ylim(0, 6.5)
ax.set_yticks([0, 2, 4, 6])
ax.tick_params(axis='x', length=0, pad=5)
ax.set_xlabel(r'$D_\mathrm{SE}$ (µm)', labelpad=3)
ax.set_ylabel('SE ionic conductivity (mS/cm)')
save(fig, 'd4_breakeven')
meta['values']['breakeven_band_mScm'] = {b: band[b] for b in ('D2', 'D1')}
meta['values']['breakeven_req_hertz_mScm'] = {b: req_hertz[b] for b in ('D2', 'D1')}
meta['values']['net_ratio_1um_range'] = [meas['D1'] / band['D1'][1], meas['D1'] / band['D1'][0]]
meta['values']['net_ratio_1um_hertz'] = meas['D1'] / req_hertz['D1']
meta['values']['pellet_loss_ratio'] = meas['D3'] / meas['D1']
meta['values']['p_end_MPa'] = {b: M[b]['p_end_MPa'] for b in ORDER}
meta['values']['area_am_se_per_am_um2'] = {b: M[b]['area_am_se_per_am_mean_um2'] for b in ORDER}
(OUT / 'd4_figs_meta.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps(meta['values'], ensure_ascii=False, indent=1))

# 6) 접촉 면적 — (a) AM 1개당 면적 합 (b) 접촉 1개 면적
ar = {b: float(rows[b]['area_am_se_per_contact_mean_um2']) for b in ORDER}
fig = plt.figure(figsize=(FW, FH))
for k, (vals, lab, top, fmt) in enumerate(((M, 'Contact area per AM (µm²)', 30, '{:.1f}'), (ar, 'Area per contact (µm²)', 2.5, '{:.2f}'))):
    w = (FW - 0.62 - 0.12 - 0.55) / 2
    ax = fig.add_axes([(0.55 + k * (w + 0.62)) / FW, 0.50 / FH, w / FW, (FH - 0.72) / FH])
    v = {b: (vals[b]['area_am_se_per_am_mean_um2'] if k == 0 else vals[b]) for b in ORDER}
    for x, b in enumerate(ORDER):
        ax.bar(x, v[b], width=0.56, color=C[b], edgecolor=C[b], zorder=3)
        ax.text(x, v[b] + top * 0.025, fmt.format(v[b]), ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_xticks(range(3)); ax.set_xticklabels([LAB[b] for b in ORDER]); ax.set_xlim(-0.6, 2.6); ax.set_ylim(0, top)
    ax.tick_params(axis='x', length=0, pad=4); ax.set_xlabel(r'$D_\mathrm{SE}$ (µm)', labelpad=3); ax.set_ylabel(lab, fontsize=9.5)
save(fig, 'd4_contact_area')
meta['values']['area_per_contact_um2'] = ar

# 7) 수송 tortuosity (tau2, Hertz)
t2 = {b: float(rows[b]['tau2_ion_hertz']) for b in ORDER}
fig, ax = axes()
bars(ax, t2, lambda v: f'{v:.1f}', 16)
ax.set_yticks([0, 5, 10, 15])
ax.set_ylabel('Tortuosity')
save(fig, 'd4_tortuosity')
meta['values']['tau2_ion_hertz'] = t2
(OUT / 'd4_figs_meta.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# 8) 활물질 표면 피복률 (physics 합집합 기준 · 화면에는 이름 안 씀)
cov = {b: float(rows[b]['coverage_physics_union_pct']) for b in ORDER}
fig, ax = axes()
bars(ax, cov, lambda v: f'{v:.1f}%', 70)
ax.set_yticks([0, 20, 40, 60])
ax.set_ylabel('AM surface coverage (%)')
save(fig, 'd4_coverage')
meta['values']['coverage_physics_union_pct'] = cov

# 9) 손익분기 — hertz f_mc 하나 (단일 값)
fig, ax = axes()
for x, b in enumerate(ORDER):
    v = meas['D3'] if b == 'D3' else req_hertz[b]
    ax.bar(x, v, width=0.56, color='#BFBFBF', edgecolor='#7F7F7F', linewidth=1.0, zorder=3)
    ax.text(x, v + 0.15, ('5.1 (ref.)' if b == 'D3' else f'{v:.1f}'), ha='center', va='bottom', fontsize=10.5, fontweight='bold')
    if b in meas:
        ax.plot([x + 0.40], [meas[b]], marker='D', ms=8, color='#C55A11', zorder=5, clip_on=False)
        if b == 'D1':
            ax.text(x + 0.52, meas[b], f'{meas[b]:.1f}', ha='left', va='center', fontsize=10.5, color='#C55A11', fontweight='bold')
ax.set_xticks([0, 1, 2]); ax.set_xticklabels([LAB[b] for b in ORDER]); ax.set_xlim(-0.6, 2.75); ax.set_ylim(0, 6.5)
ax.set_yticks([0, 2, 4, 6]); ax.tick_params(axis='x', length=0, pad=5)
ax.set_xlabel(r'$D_\mathrm{SE}$ (µm)', labelpad=3); ax.set_ylabel('SE ionic conductivity (mS/cm)')
save(fig, 'd4_breakeven1')
meta['values']['breakeven_req_hertz_fmc'] = {b: req_hertz[b] for b in ('D2', 'D1')}
meta['values']['net_ratio_1um_hertz_fmc'] = meas['D1'] / req_hertz['D1']
meta['values']['threshold_ratio_1um_hertz_fmc'] = req_hertz['D1'] / meas['D3']
(OUT / 'd4_figs_meta.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
