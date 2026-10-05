"""194 망 배치 (11fcf91e8) 미리보기 그림 · 값 요약 (python3 plot_overview.py — 이 폴더에 png · svg · csv · tsv 를 쓴다) — merged/<cohort>/metrics_flat.csv 만 읽는다 (계산 0 · 인계표 재생성 전).

τ² = φ_mc / f_mc ,  f_mc = σ_ratio · L_gap / L_mc   (scripts/tau_flux.ion_columns 와 같은 식 · G1 띠 규칙은 metrics_flat 에 없어 미적용)
a  = ln f_mc / ln φ_mc  (τ² = φ^(1−a))
"""
import csv, math, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

OUT = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.dirname(OUT), 'merged')          # 같은 배치 폴더의 merged/<코호트>/metrics_flat.csv

plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 10, 'axes.linewidth': 1.0,
                     'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True,
                     'svg.fonttype': 'none'})


def num(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


rows = []
for coh in ('lhs', 'lhsx'):
    for r in csv.DictReader(open(f'{D}/{coh}/metrics_flat.csv', encoding='utf-8')):
        phi_mc, phi_am = num(r['phi_se_mass_conserving']), num(r['phi_am_mass_conserving'])
        Lg, Lm = num(r['thickness_um']), num(r['thickness_mass_conserving_um'])
        sr = num(r['network_dual.hertzian.sigma_full'])          # σ_ratio (무차원) · Hertz
        st = r['network_dual.hertzian.sigma_full_status']
        f = sr * Lg / Lm if (sr and Lg and Lm) else None
        t2 = phi_mc / f if f else None
        a = math.log(f) / math.log(phi_mc) if f else None
        phi_net = num(r['phi_se'])
        basis = abs(phi_net - phi_mc * Lm / Lg) if None not in (phi_net, phi_mc, Lm, Lg) else None
        rows.append(dict(case=r['case'], cohort=coh, status=st, phi_se=phi_mc, phi_am=phi_am,
                         s_ion=num(r['sigma_full_mScm']), s_ion_ph=num(r['sigma_full_mScm_physics']),
                         s_e=num(r['electronic_sigma_full_mScm']), e_pf=num(r['electronic_percolating_fraction']),
                         f_mc=f, tau2=t2, a=a, basis_dev=basis,
                         share_ion=num(r['constriction_power_share_ion_hertz']),
                         ratio_ph=num(r['network_dual.ratio_physics_over_hertzian.sigma_full']),
                         r_SE=num(r['inp.r_SE']), r_AM_P=num(r['inp.r_AM_P']), r_AM_S=num(r['inp.r_AM_S'])))

# ---- 수치 요약 (그림 밖 · 채팅용) -------------------------------------------------------------------------------
def med(v):
    v = sorted(x for x in v if x is not None)
    if not v:
        return None
    n = len(v)
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])

summ = {}
for coh in ('lhs', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    P = [r for r in R if r['status'] == 'computed']
    summ[coh] = dict(n=len(R), perc=len(P), noperc=sum(r['status'] == 'valid_zero' for r in R),
                     e_none=sum(r['s_e'] is None for r in R),
                     s_ion=(min(r['s_ion'] for r in P), med([r['s_ion'] for r in P]), max(r['s_ion'] for r in P)),
                     s_e=(min(r['s_e'] for r in R if r['s_e']), med([r['s_e'] for r in R]), max(r['s_e'] for r in R if r['s_e'])),
                     tau2=(min(r['tau2'] for r in P), med([r['tau2'] for r in P]), max(r['tau2'] for r in P)),
                     a=(min(r['a'] for r in P), med([r['a'] for r in P]), max(r['a'] for r in P)),
                     below1=sum(r['tau2'] < 1 for r in P),
                     ratio_ph=(min(r['ratio_ph'] for r in P), med([r['ratio_ph'] for r in P]), max(r['ratio_ph'] for r in P)),
                     share=(min(r['share_ion'] for r in P), med([r['share_ion'] for r in P]), max(r['share_ion'] for r in P)),
                     basis_max=max(r['basis_dev'] for r in R))
for k, v in summ.items():
    print(k, v)

# ---- 그림 --------------------------------------------------------------------------------------------------------
C = {'lhs': '#1f4e9c', 'lhsx': '#e07b1a'}
MK = {'lhs': 'o', 'lhsx': 's'}
LBL = {'lhs': 'LHS (130)', 'lhsx': 'LHSx, SE-rich (64)'}
plain = FuncFormatter(lambda x, _: f'{x:g}')

fig, axs = plt.subplots(2, 3, figsize=(13.4, 8.0))
(a1, a2, a3), (a4, a5, a6) = axs


def sc(ax, coh, xs, ys, **kw):
    ax.scatter(xs, ys, s=22, marker=MK[coh], facecolor='none', edgecolor=C[coh], linewidth=1.0, **kw)


# (a) σ_ion vs φ_SE
FLOOR_I = 4e-5
for coh in ('lhs', 'lhsx'):
    P = [r for r in rows if r['cohort'] == coh and r['status'] == 'computed']
    sc(a1, coh, [r['phi_se'] for r in P], [r['s_ion'] for r in P], label=LBL[coh])
NP = [r for r in rows if r['status'] == 'valid_zero']
a1.scatter([r['phi_se'] for r in NP], [FLOOR_I] * len(NP), s=26, marker='x', color='0.45', linewidth=1.0,
           label=f'No SE through path ({len(NP)}, σ = 0)')
a1.set_yscale('log'); a1.set_ylim(2.5e-5, 6)
a1.set_xlabel('φ$_{SE}$'); a1.set_ylabel('σ$_{ion}$ (mS cm$^{-1}$)')

# (b) σ_e vs φ_AM
FLOOR_E = 4e-3
for coh in ('lhs', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh and r['s_e']]
    sc(a2, coh, [r['phi_am'] for r in R], [r['s_e'] for r in R])
NE = [r for r in rows if r['s_e'] is None]
a2.scatter([r['phi_am'] for r in NE], [FLOOR_E] * len(NE), s=26, marker='+', color='0.45', linewidth=1.0,
           label=f'No AM through path ({len(NE)}, σ = 0)')
a2.set_yscale('log'); a2.set_ylim(2.5e-3, 40)
a2.set_xlabel('φ$_{AM}$'); a2.set_ylabel('σ$_{e}$ (mS cm$^{-1}$)')

# (c) τ² vs φ_SE + Bruggeman 등지수선
xs = [0.06 + i * 0.0025 for i in range(int((0.85 - 0.06) / 0.0025) + 1)]
for aa in (1.5, 2, 3, 4):
    a3.plot(xs, [x ** (1 - aa) for x in xs], ls='--', lw=0.8, color='0.6', zorder=0)
for coh in ('lhs', 'lhsx'):
    P = [r for r in rows if r['cohort'] == coh and r['status'] == 'computed']
    sc(a3, coh, [r['phi_se'] for r in P], [r['tau2'] for r in P])
a3.set_yscale('log'); a3.set_ylim(0.7, 3000)
a3.set_xlabel('φ$_{SE}$'); a3.set_ylabel('Transport tortuosity (ion)')

# (d) a 분포
import numpy as np
bins = np.arange(1.4, 5.01, 0.1)
for coh in ('lhs', 'lhsx'):
    v = [r['a'] for r in rows if r['cohort'] == coh and r['status'] == 'computed']
    a4.hist(v, bins=bins, histtype='stepfilled', alpha=0.25, color=C[coh])
    a4.hist(v, bins=bins, histtype='step', lw=1.2, color=C[coh])
a4.axvline(1.5, ls='--', lw=0.8, color='0.5')
a4.set_xlabel('Bruggeman exponent a (ion)'); a4.set_ylabel('Cases')
a4.set_xlim(1.4, 5.0)

# (e) Physics / Hertz σ_ion
for coh in ('lhs', 'lhsx'):
    P = [r for r in rows if r['cohort'] == coh and r['status'] == 'computed']
    sc(a5, coh, [r['phi_se'] for r in P], [r['ratio_ph'] for r in P])
a5.axhline(1, ls='--', lw=0.8, color='0.5')
a5.set_ylim(0, 1.6)
a5.set_xlabel('φ$_{SE}$'); a5.set_ylabel('σ$_{ion}$ Physics / Hertz')

# (f) 협착 전력 몫 (ion · Hertz)
for coh in ('lhs', 'lhsx'):
    P = [r for r in rows if r['cohort'] == coh and r['status'] == 'computed']
    sc(a6, coh, [r['phi_se'] for r in P], [100 * r['share_ion'] for r in P])
a6.set_ylim(60, 95)
a6.set_xlabel('φ$_{SE}$'); a6.set_ylabel('Constriction power share, ion (%)')

for ax in (a1, a3, a5, a6):
    ax.set_xlim(0.05, 0.85)
for ax in axs.flat:
    if ax.get_xscale() == 'linear':
        ax.xaxis.set_major_formatter(plain)
    if ax.get_yscale() == 'linear':
        ax.yaxis.set_major_formatter(plain)
    else:
        ax.yaxis.set_major_locator(LogLocator(base=10, numticks=8))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}' if 1e-2 <= y <= 1e3 else f'10$^{{{int(round(math.log10(y)))}}}$'))
a2.set_xlim(0.1, 0.8)
for ax, t in zip(axs.flat, 'abcdef'):
    ax.text(-0.16, 1.02, f'({t})', transform=ax.transAxes, fontsize=11, fontweight='bold', va='bottom')

h1, l1 = a1.get_legend_handles_labels()
h2, l2 = a2.get_legend_handles_labels()
fig.legend(h1 + h2, l1 + l2, loc='upper center', ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.0), fontsize=9.5)
fig.text(0.5, 0.004,
         'Network solver, Hertz mode unless noted · φ = mass-conserving volume fraction · f = σ$_{ion}$/σ$_0$ (σ$_0$ = 3.0 mS cm$^{-1}$) · '
         'transport tortuosity = φ$_{SE}$/f (not square-rooted) · a = ln f / ln φ$_{SE}$ (transport tortuosity = φ$^{1-a}$)\n'
         '(c) dashed, bottom to top: a = 1.5, 2, 3, 4 · (d) dashed: a = 1.5 (Bruggeman) · (f) ΣI²R over contact constrictions / total ΣI²R',
         ha='center', va='bottom', fontsize=8, color='0.3', linespacing=1.5)
fig.tight_layout(rect=(0, 0.045, 1, 0.95), w_pad=2.2, h_pad=2.0)
for ext in ('png', 'svg'):
    fig.savefig(f'{OUT}/net194_overview.{ext}', dpi=200)

with open(f'{OUT}/net194_overview_data.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    keys = ['case', 'cohort', 'status', 'phi_se', 'phi_am', 's_ion', 's_ion_ph', 's_e', 'f_mc', 'tau2', 'a', 'ratio_ph', 'share_ion',
            'r_SE', 'r_AM_P', 'r_AM_S']
    w.writerow(keys)
    for r in rows:
        w.writerow([r[k] for k in keys])

# ---- 코호트별 요약 (두 모드 · 망 출력) ------------------------------------------------------------------------------
def _summ():
    out = []
    for coh in ('lhs', 'lhsx'):
        for r in csv.DictReader(open(f'{D}/{coh}/metrics_flat.csv', encoding='utf-8')):
            phi = num(r['phi_se_mass_conserving']); Lg = num(r['thickness_um']); Lm = num(r['thickness_mass_conserving_um'])
            d = {'cohort': coh}
            for m, key in (('hertz', 'network_dual.hertzian.sigma_full'), ('physics', 'network_dual.physics.sigma_full')):
                sr = num(r[key]); f = sr * Lg / Lm if sr else None
                d[f'f_{m}'] = f; d[f'transport_tortuosity_{m}'] = phi / f if f else None
                d[f'a_{m}'] = math.log(f) / math.log(phi) if f else None
            d['s_ion_hertz'] = num(r['sigma_full_mScm']); d['s_ion_physics'] = num(r['sigma_full_mScm_physics'])
            d['s_e_hertz'] = num(r['electronic_sigma_full_mScm']); d['s_e_physics'] = num(r['electronic_sigma_full_mScm_physics'])
            d['s_th_hertz'] = num(r['thermal_sigma_full_mScm']); d['s_th_physics'] = num(r['thermal_sigma_full_mScm_physics'])
            d['ratio_ion_physics_over_hertz'] = num(r['network_dual.ratio_physics_over_hertzian.sigma_full'])
            d['ratio_e_physics_over_hertz'] = num(r['network_dual.ratio_physics_over_hertzian.electronic_sigma_full'])
            for ch in ('ion', 'el', 'th'):
                for m in ('hertz', 'physics'):
                    d[f'constriction_power_share_{ch}_{m}'] = num(r[f'constriction_power_share_{ch}_{m}'])
            out.append(d)
    keys = [k for k in out[0] if k != 'cohort']
    with open(f'{OUT}/net194_value_summary.tsv', 'w', encoding='utf-8') as fh:
        fh.write('quantity\tcohort\tn_values\tn_blank\tmin\tmedian\tmax\n')
        for k in keys:
            for coh in ('lhs', 'lhsx'):
                v = [x[k] for x in out if x['cohort'] == coh]
                x = sorted(a for a in v if a is not None)
                row = f'{k}\t{coh}\t{len(x)}\t{len(v) - len(x)}\t'
                row += '\t'.join(f'{q:.6g}' for q in (x[0], med(x), x[-1])) if x else '\t\t'
                fh.write(row + '\n')


_summ()
print('written', OUT)
