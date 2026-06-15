import json,os,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
triv=json.load(open('db/properties/doping_cascade_trivalent_M3.json'))
ver =json.load(open('db/properties/doping_cascade_verified.json'))
g13={'Al2O3','Ga2O3','In2O3'}
valmap={'MnO':2,'CoO':2,'NiO':2,'CaO':2,'BaO':2,'SrO':2,'MgO':2,'ZnO':2,'Li2O':1,'Cu2O':1,'Ag2O':1,'Na2O':1}
reps={}
def best_by_dE(items):
    b=None
    for e in items:
        if not isinstance(e,dict) or 'de_post_anneal_eV_atom' not in e: continue
        if b is None or e['de_post_anneal_eV_atom']<b['de_post_anneal_eV_atom']: b=e
    return b
for d,inf in triv['champions'].items():
    b=best_by_dE([inf.get(x) for x in ('x002','x005','x010')])
    if b: reps[d.replace('2O3','')]=dict(dE=b['de_post_anneal_eV_atom'],E=(np.nan if b.get('_FLAG') else b.get('E_young_GPa')),
        B0=b.get('B0_GPa'),bvs=b.get('bvs_li_proxy'),score=b.get('score_combined'),val=3,fam=('g13' if d in g13 else 'RE'),dV=None)
for d,inf in ver['compounds'].items():
    if d in ('Sc2O3','Al2O3'): continue
    v=valmap.get(d);
    if v is None: continue
    b=best_by_dE(list(inf['concentrations'].values()))
    if b: reps[d]=dict(dE=b['de_post_anneal_eV_atom'],E=b.get('E_VRH_GPa'),B0=b.get('EOS_B0_GPa'),
        bvs=None,score=None,val=v,fam='m',dV=b.get('dV_anneal_pct'))

colv={3:'#1f77b4',2:'#ff7f0e',1:'#7f7f7f'}
fig,ax=plt.subplots(2,2,figsize=(15,11))

# (a) full dE ranking
a=ax[0,0]; order=sorted(reps,key=lambda d:reps[d]['dE'])
y=np.arange(len(order)); a.barh(y,[reps[d]['dE'] for d in order],color=[colv[reps[d]['val']] for d in order],edgecolor='k',lw=.4)
a.set_yticks(y); a.set_yticklabels(order,fontsize=8); a.invert_yaxis()
a.set_xlabel('formation dE (eV/atom)  (more negative = more stable)'); a.set_title('(a) Full dopant stability ranking (best conc)')
for v,l in [(3,'M3+'),(2,'M2+'),(1,'M1+')]: a.barh([],[],color=colv[v],label=l)
a.legend(fontsize=8); a.grid(alpha=.3,axis='x')

# (b) M3+ multi-axis heatmap (higher=better)
a=ax[0,1]; M3=sorted([d for d in reps if reps[d]['val']==3],key=lambda d:reps[d]['dE'])
cols=['stability\n(-dE)','softness\n(-E)','mobility\n(bvs)','score']
raw=np.array([[-reps[d]['dE'],-(reps[d]['E'] if reps[d]['E']==reps[d]['E'] else np.nan),reps[d]['bvs'],reps[d]['score']] for d in M3])
N=raw.copy()
for j in range(4):
    c=raw[:,j]; lo,hi=np.nanmin(c),np.nanmax(c); N[:,j]=(c-lo)/(hi-lo)
im=a.imshow(N,cmap='YlGn',aspect='auto',vmin=0,vmax=1)
a.set_xticks(range(4)); a.set_xticklabels(cols,fontsize=8); a.set_yticks(range(len(M3))); a.set_yticklabels(M3,fontsize=8)
for i in range(len(M3)):
    for j in range(4):
        v=raw[i,j]; a.text(j,i,'-' if v!=v else f'{abs(v):.2f}' if j<2 else f'{v:.2f}',ha='center',va='center',fontsize=7)
a.set_title('(b) M3+ multi-axis (greener = better)'); fig.colorbar(im,ax=a,fraction=.04)

# (c) bvs vs dE (M3+), color=E
a=ax[1,0]
xs=[reps[d]['dE'] for d in M3]; ys=[reps[d]['bvs'] for d in M3]; cs=[reps[d]['E'] for d in M3]
sc=a.scatter(xs,ys,c=cs,cmap='viridis_r',s=120,edgecolor='k')
for d in M3: a.annotate(d,(reps[d]['dE'],reps[d]['bvs']),fontsize=8,xytext=(4,3),textcoords='offset points')
a.set_xlabel('formation dE (eV/atom)'); a.set_ylabel('Li mobility proxy (BVS)'); a.set_title('(c) M3+ stability vs mobility (color=E_VRH)')
fig.colorbar(sc,ax=a,label='E_VRH (GPa)'); a.grid(alpha=.3)

# (d) lattice strain dV (di/mono have it)
a=ax[1,1]; dd=[d for d in reps if reps[d]['dV'] is not None]
dd=sorted(dd,key=lambda d:abs(reps[d]['dV']))
a.barh(range(len(dd)),[abs(reps[d]['dV']) for d in dd],color=[colv[reps[d]['val']] for d in dd],edgecolor='k',lw=.4)
a.set_yticks(range(len(dd))); a.set_yticklabels(dd,fontsize=8); a.invert_yaxis()
a.set_xlabel('|lattice strain| dV on doping (%)  (smaller = gentler)'); a.set_title('(d) Lattice strain (M2+/M1+ subset)'); a.grid(alpha=.3,axis='x')

plt.suptitle('Cascade quantitative comparison II  (LPSCl1.6 oxide dopants, UMA-s-1p1, v23)',fontsize=12,y=1.0)
plt.tight_layout()
plt.savefig('docs/figures/cascade/cascade_comparison2.png',dpi=150,bbox_inches='tight')
print('saved -> cascade_comparison2.png ; dopants:',len(reps),'M3+ heatmap:',len(M3))
