"""5 쪽 교체 그림 미리보기 (PNG · SVG) — 값 = 리포 CSV 그대로 · 1저자 기존 그림 틀 (검정 · 회색 · 주황 · 7:3 빨강 점 · 점마다 값)."""
import csv, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo, out = sys.argv[1], sys.argv[2]
def rows(p):
    with open(p, encoding='utf-8') as f:
        r = list(csv.reader(f))
    return r[0], [x for x in r[3:] if x]
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 9, 'axes.linewidth': 1.0,
                     'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True,
                     'mathtext.default': 'regular'})
COL = {'k': '#000000', 'g': '#7f7f7f', 'o': '#ed7d31'}; RED = '#e00000'; INK = '#404040'

def panel(fname, x, series, ylab, ylim, yticks, fmt, ref=None, legend_kw=None, special=None):
    fig, ax = plt.subplots(figsize=(4.4, 2.9), dpi=220)
    xi = list(range(len(x)))
    for lab, ys, c, mk, off in series:
        pts = [(i, y) for i, y in zip(xi, ys) if y is not None]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], '-', color=c, lw=1.3, marker=mk, ms=5,
                mfc=c, mec=c, label=lab, zorder=3)
        for i, y in pts:
            if x[i] == '7:3':
                ax.plot([i], [y], marker=mk, ms=5.5, mfc=RED, mec=RED, zorder=4)
            dx, dy, ha = (special or {}).get((lab, x[i]), (0, off, 'center'))
            ax.annotate(fmt(y), (i, y), xytext=(dx, dy), textcoords='offset points', ha=ha,
                        va=('center' if ha != 'center' else ('bottom' if dy > 0 else 'top')), fontsize=7, color=INK)
    if ref is not None:
        ax.axhline(ref[0], ls=':', lw=1.0, color='#000000', zorder=1)
        ax.text(len(x) - 0.65, ref[0] - 0.03 * (ylim[1] - ylim[0]), ref[1], ha='right', va='top', fontsize=7.5, color=INK)
    ax.set_xticks(xi, x); ax.set_xlim(-0.4, len(x) - 0.6)
    ax.set_ylim(*ylim); ax.set_yticks(yticks, [('0' if t == 0 else (f'{t:g}' if float(t).is_integer() else f'{t:.1f}')) for t in yticks])
    ax.set_xlabel('PC:SC (wt%)'); ax.set_ylabel(ylab)
    ax.legend(frameon=False, fontsize=7.5, handlelength=1.8, **(legend_kw or {}))
    fig.tight_layout()
    for ext in ('png', 'svg'):
        fig.savefig(f'{out}/{fname}.{ext}', dpi=220)
    plt.close(fig)

# ① 힘 그림 교체 = Contribution to σ_zz (%) — 21 수평 단면 평균
h, r = rows(f'{repo}/docs/data/ps45_plane_load_20261007/ps45_v2/plane_load_share_slide.csv')
x = [a[0] for a in r]; col = lambda j: [float(a[j]) if a[j] else None for a in r]
panel('contribution_sigma_zz', x,
      [('AM–AM', col(1), COL['k'], 's', 5), ('AM–SE', col(2), COL['g'], 'o', 5), ('SE–SE', col(3), COL['o'], '^', -6)],
      r'Contribution to $\sigma_{zz}$ (%)', (0, 75), [0, 20, 40, 60], lambda v: f'{v:.1f}',
      legend_kw=dict(loc='upper center', ncol=3, columnspacing=1.2))
# ② 응력 비 그림 교체 = α (부피 가중 σ_zz ÷ 전극 평균)
h, r = rows(f'{repo}/docs/data/ps45_plane_load_20261007/ps45_v2/stress_reduction_slide.csv')
x = [a[0] for a in r]; col = lambda j: [float(a[j]) if a[j] else None for a in r]
panel('alpha_sigma_zz', x,
      [('PC', col(1), COL['k'], 's', 5), ('SC', col(2), COL['g'], 'o', -6), ('SE', col(3), COL['o'], '^', -6)],
      r'$\alpha$ ($\sigma_{zz,phase}$ / $\sigma_{zz,bed}$)', (0, 1.8), [0, 0.5, 1.0, 1.5], lambda v: f'{v:.2f}',
      ref=(1.0, r'Bed average ($\alpha$ = 1)'), legend_kw=dict(loc='upper center', ncol=3, columnspacing=1.5),
      special={('SC', '7:3'): (8, 0, 'left')})
print('ok')
