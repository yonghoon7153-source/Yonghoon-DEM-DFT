#!/usr/bin/env python3
"""주간보고 그림 2장 — 2026-08-31 (문구는 `weekly_20260831_slide_text.md`).

  python3 docs/seminar/mk_weekly_figs.py [OUTDIR]

Fig 4b 는 별도다: `python3 scripts/fig4b_sigma_conventions.py --out <OUTDIR>/fig4b.png`
⚠ 각주 문구를 지우지 말 것 — "복제가 아니다 / 표준오차가 아니다 / 방향 미결정" 이
  이 그림들이 과잉해석되는 것을 막는 유일한 장치다.
"""
import sys, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.linewidth':0.9})

# ── ① A2 factorial 주효과 ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)
labs = ['PTFE representation\nconvention',
        'Voxel size\n+ diameter-preserving\n$\\sigma_{VGCF}$ rescaling',
        'SDCP contact\nbridge']
eff  = [0.189307, 0.021544, 0.009028]
lo   = [0.184148, 0.015776, 0.005941]
hi   = [0.194100, 0.027678, 0.012481]
y = np.arange(len(labs))[::-1]
err = [[e-l for e,l in zip(eff,lo)], [h-e for e,h in zip(eff,hi)]]
ax.barh(y, eff, height=.55, color=['#8FA9C4','#C9C2B0','#C9C2B0'],
        edgecolor='#333', linewidth=.8)
ax.errorbar(eff, y, xerr=err, fmt='none', ecolor='#333', elinewidth=1.1, capsize=4)
for yy, e, l, h in zip(y, eff, lo, hi):
    ax.text(h+0.006, yy, f'{e:+.3f}   ({100*(h-l)/e:.0f} % span)',
            va='center', fontsize=9.5, color='#222')
ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=9.5)
ax.set_xlabel('Main effect on $\\sigma_e$ ratio (DBE/SBE)')
ax.set_xlim(0, 0.28); ax.spines[['top','right']].set_visible(False)
ax.set_title('$2^3$ factorial — PTFE convention dominates', fontsize=11.5, pad=8, loc='left')
fig.text(.01,-.02,'Bars = mean effect over the other two axes; whiskers = observed range. '
                  'Not replicates — a complete factorial of one bed.',fontsize=7.6,color='#666')
fig.tight_layout(); fig.savefig(OUT+'/a2_factorial.png', bbox_inches='tight', facecolor='w')
print('a2_factorial.png')

# ── ② 이온 r-민감도 4점 ───────────────────────────────────────────
fig,(a1,a2)=plt.subplots(1,2,figsize=(9.0,3.6),dpi=300,gridspec_kw={'width_ratios':[1.25,1]})
sbe=0.6585636; dbe=np.array([0.6437437,0.6455487,0.6566943,0.6640011])
nm=['inert\n(r = 0)','MG-inverted\n(0.0184)','RSA-inverted\n(0.1737)','production\n(0.3333)']
x=np.arange(4)
a1.axhline(sbe,color='#8FA9C4',lw=2.4,zorder=1)
a1.text(3.42,sbe,'SBE 0.6586\n(independent of $r$)',va='center',ha='left',
        fontsize=8.5,color='#4a6785')
a1.plot(x,dbe,'o',ms=10,mfc='none',mec='#C98A6B',mew=2.3,zorder=3)
a1.text(-0.42,0.6648,'DBE',fontsize=9.5,color='#8a5a3b',fontweight='bold')
for xi,d in zip(x,dbe):
    a1.annotate(f'{d:.4f}',(xi,d),textcoords='offset points',
                xytext=(0,13 if xi<2 else -19),ha='center',fontsize=8.8,color='#8a5a3b')
a1.set_xticks(x); a1.set_xticklabels(nm,fontsize=8.6)
a1.set_xlim(-0.55,4.55); a1.set_ylim(0.6415,0.6672)
a1.set_ylabel('$\\sigma_{ion,eff}$  (mS cm$^{-1}$)')
a1.set_xlabel('SDCP-phase ionic conductivity scenario')
a1.spines[['top','right']].set_visible(False)
a1.set_title('Absolute values',fontsize=10.5,loc='left')
r=dbe/sbe
a2.axhline(1.0,color='#999',lw=1.0,ls='--',zorder=1)
a2.plot(x,r,'s-',ms=8,mfc='none',mec='#4a6785',color='#4a6785',mew=2.0,lw=1.5)
for xi,rr in zip(x,r):
    a2.annotate(f'{rr:.4f}',(xi,rr),textcoords='offset points',
                xytext=(6 if xi==0 else 0, 11 if rr<1 else -18),
                ha='left' if xi==0 else 'center',fontsize=8.8,color='#33506e')
a2.set_xticks(x); a2.set_xticklabels(['0','0.018','0.174','0.333'],fontsize=9)
a2.set_xlim(-0.4,3.5); a2.set_ylim(0.9705,1.0145)
a2.set_xlabel('$r = \\sigma_{ion}$(SDCP) / $\\sigma_{ion}$(SE)')
a2.set_ylabel('$\\sigma_{ion}$ ratio   DBE / SBE')
a2.spines[['top','right']].set_visible(False)
a2.set_title('Ratio crosses unity',fontsize=10.5,loc='left')
fig.text(.01,-.04,'Deterministic model-form scenarios at one prescribed grid origin — not replicates, '
                  'not an uncertainty band.  The direction is not resolved.',fontsize=7.8,color='#666')
fig.tight_layout(); fig.savefig(OUT+'/ion_r_sensitivity.png',bbox_inches='tight',facecolor='w')
print('ion_r_sensitivity.png')
