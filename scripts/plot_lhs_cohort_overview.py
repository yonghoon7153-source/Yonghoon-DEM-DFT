#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LHS 코호트 개요 그림 (주간보고 2026-09-20 슬라이드용) — docs/figures/lhs_cohort_overview_20260920.{png,svg}

입력: docs/data/lhs_handover_20260919.csv (설계+측정 디스크립터) · docs/data/lhs_percolation_measured_20260915.csv (실측 이온 퍼콜레이션).
(a) 활물질 비율별 연결/끊김 케이스 수  (b) AM 표면 SE coverage(Hertz) vs 측정 φ_SE.  팔레트는 dataviz 검증 통과(파랑/주황).
⚠ porosity_sphere_pct 는 RECORD_ONLY 라 그리지 않는다.  리포 루트에서 실행한다.
"""
import csv, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, sys
sys.path.insert(0,'/home/user/Yonghoon-DEM-DFT/scripts')
try:
    from viz_mixer_bed import pick_cjk_font; f=pick_cjk_font(); plt.rcParams['font.family']=f if f else plt.rcParams['font.family']
except Exception: pass
def load(p): return [r for r in csv.DictReader(l for l in open(p,encoding='utf-8') if not l.startswith('#'))]
H=load('docs/data/lhs_handover_20260919.csv'); P={r['case_id']:r for r in load('docs/data/lhs_percolation_measured_20260915.csv')}
am=np.array([float(r['am_pct']) for r in H]); dse=np.array([float(r['d_se_um']) for r in H])
blk=np.array([r['block'] for r in H]); phise=np.array([float(r['phi_se']) for r in H])
cov=np.array([float(r['coverage_AM_total_hertz_pct']) for r in H])
perc=np.array([P.get(r['case_id'],{}).get('ionic_percolates','')=='True' for r in H])
BLUE,ORANGE='#2a78d6','#eb6834'
fig,ax=plt.subplots(1,2,figsize=(11,4.6))
xs=sorted(set(am)); w=3.2
n_ok=[int((perc&(am==x)).sum()) for x in xs]; n_no=[int(((~perc)&(am==x)).sum()) for x in xs]
ax[0].bar(xs,n_ok,w,color=BLUE,label=f'이온 경로 연결 ({perc.sum()})')
ax[0].bar(xs,n_no,w,bottom=n_ok,color=ORANGE,label=f'이온 경로 끊김 ({(~perc).sum()})')
for x,a,b in zip(xs,n_ok,n_no):
    ax[0].text(x,a+b+0.4,f'{a+b}',ha='center',fontsize=9,color='#333')
    if b: ax[0].text(x,a+b/2,f'{b}',ha='center',va='center',fontsize=8.5,color='white',fontweight='bold')
ax[0].set_xlabel('활물질 비율 am_pct (wt%)'); ax[0].set_ylabel('케이스 수'); ax[0].set_xticks(xs)
ax[0].set_title('(a) LHS 130 케이스 — 활물질 비율별 이온 경로 연결/끊김',fontsize=10.5)
ax[0].legend(fontsize=9,frameon=False,loc='upper left'); ax[0].grid(axis='y',alpha=.2); ax[0].set_ylim(0,max(n_ok[i]+n_no[i] for i in range(len(xs)))*1.18)
ax[1].scatter(phise[perc],cov[perc],s=44,c=BLUE,alpha=.8,edgecolor='white',lw=.6,label='연결')
ax[1].scatter(phise[~perc],cov[~perc],s=44,c=ORANGE,marker='X',alpha=.85,edgecolor='white',lw=.6,label='끊김')
ax[1].set_xlabel('측정 전해질 부피분율 φ_SE'); ax[1].set_ylabel('AM 표면 SE coverage (Hertz, %)')
ax[1].set_title('(b) 추출 디스크립터 — coverage vs φ_SE (130/130)',fontsize=10.5); ax[1].legend(fontsize=9,frameon=False); ax[1].grid(alpha=.2)
for a_ in ax:
    for s_ in ('top','right'): a_.spines[s_].set_visible(False)
plt.tight_layout(); import os; os.makedirs('docs/figures',exist_ok=True)
for ext in ('png','svg'): fig.savefig(f'docs/figures/lhs_cohort_overview_20260920.{ext}',dpi=140)
print('저장; 연결',perc.sum(),'끊김',(~perc).sum(),'| bimodal',(blk=='bimodal').sum(),'mono',(blk!='bimodal').sum())
print('φ_SE 범위',phise.min().round(3),phise.max().round(3),'| 피복률 범위',cov.min().round(1),cov.max().round(1))
