import json, os, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt

triv=json.load(open('db/properties/doping_cascade_trivalent_M3.json'))
ver =json.load(open('db/properties/doping_cascade_verified.json'))
g13={'Al2O3','Ga2O3','In2O3'}

# trivalent rows: (dop,x,dE,E,bvs,score,r,fam)
T=[]
for d,inf in triv['champions'].items():
    r=inf.get('r_A')
    for x in ('x002','x005','x010'):
        e=inf.get(x)
        if not isinstance(e,dict) or 'de_post_anneal_eV_atom' not in e: continue
        E=e.get('E_young_GPa');  E=np.nan if e.get('_FLAG') else E
        T.append((d,x,e['de_post_anneal_eV_atom'],E,e.get('bvs_li_proxy'),e.get('score_combined'),r,'g13' if d in g13 else 'RE'))
fam={d:('g13' if d in g13 else 'RE') for d in triv['champions']}

# di/monovalent rows: (dop,x,dE,E,val)
valmap={'MnO':2,'CoO':2,'NiO':2,'CaO':2,'BaO':2,'SrO':2,'MgO':2,'ZnO':2,'Li2O':1,'Cu2O':1,'Ag2O':1,'Na2O':1}
V=[]
for d,inf in ver['compounds'].items():
    if d in ('Sc2O3','Al2O3'): continue
    v=valmap.get(d)
    if v is None: continue
    for x,e in inf['concentrations'].items():
        V.append((d,x,e.get('de_post_anneal_eV_atom'),e.get('E_VRH_GPa'),v))

fig,ax=plt.subplots(1,3,figsize=(17,5.2))

# (a) coating map: E vs dE
a=ax[0]
a.fill_between([8,35],-1.45,-0.85,color='green',alpha=0.10,zorder=0)
a.text(33,-1.38,'soft + stable\n(coating sweet spot)',ha='right',va='bottom',fontsize=8,color='darkgreen')
for f,c,lab in [('RE','#1f77b4','M3+ rare-earth/Sc/Y'),('g13','#9467bd','M3+ group-13')]:
    xs=[t[3] for t in T if t[7]==f and t[3]==t[3]]; ys=[t[2] for t in T if t[7]==f and t[3]==t[3]]
    a.scatter(xs,ys,c=c,s=60,label=lab,edgecolor='k',lw=0.4,zorder=3)
for v,c,lab,m in [(2,'#ff7f0e','M2+ (MnO..ZnO)','s'),(1,'#7f7f7f','M1+ (Li/Cu/Ag/Na)2O','^')]:
    xs=[r[3] for r in V if r[4]==v and r[3]]; ys=[r[2] for r in V if r[4]==v and r[3]]
    a.scatter(xs,ys,c=c,s=45,label=lab,marker=m,edgecolor='k',lw=0.3,alpha=.85,zorder=2)
for d,x,dE,E,*_ in T:
    if (d,x) in [('Gd2O3','x010'),('Sc2O3','x010'),('In2O3','x005')] and E==E:
        a.annotate(f'{d} {x}',(E,dE),fontsize=7,xytext=(4,2),textcoords='offset points',weight='bold')
a.set_xlabel('Young modulus E_VRH (GPa)  <- softer'); a.set_ylabel('formation dE (eV/atom)  (down = more stable)')
a.set_title('(a) Cascade coating-screening map  [UMA]'); a.legend(fontsize=7.5,loc='upper right'); a.grid(alpha=.3)

# (b) M3+ radius vs dE
a=ax[1]
dops=sorted(triv['champions'], key=lambda d: triv['champions'][d]['r_A'])
for d in dops:
    r=triv['champions'][d]['r_A']; ys=[t[2] for t in T if t[0]==d]
    c='#9467bd' if fam[d]=='g13' else '#1f77b4'
    a.scatter([r]*len(ys),ys,c=c,s=42,zorder=3); a.plot([r-.015,r+.015],[np.mean(ys)]*2,c=c,lw=2.5,zorder=4)
    a.annotate(d.replace('2O3',''),(r,max(ys)),fontsize=8,xytext=(0,5),textcoords='offset points',ha='center')
a.scatter([],[],c='#1f77b4',label='rare-earth/Sc/Y'); a.scatter([],[],c='#9467bd',label='group-13')
a.set_xlabel('M3+ ionic radius (Angstrom)'); a.set_ylabel('formation dE (eV/atom)')
a.set_title('(b) M3+ trend: chemical family > radius'); a.legend(fontsize=8); a.grid(alpha=.3)

# (c) M3+ radius vs E
a=ax[2]
for d in dops:
    r=triv['champions'][d]['r_A']; ys=[t[3] for t in T if t[0]==d and t[3]==t[3]]
    c='#9467bd' if fam[d]=='g13' else '#1f77b4'
    a.scatter([r]*len(ys),ys,c=c,s=42)
    if ys: a.annotate(d.replace('2O3',''),(r,np.mean(ys)),fontsize=8,xytext=(4,0),textcoords='offset points')
a.set_xlabel('M3+ ionic radius (Angstrom)'); a.set_ylabel('Young modulus E_VRH (GPa)')
a.set_title('(c) M3+ radius vs modulus'); a.grid(alpha=.3)

plt.suptitle('Oxide coating-dopant cascade in LPSCl1.6 (UMA-s-1p1, v23) — DFT validation pending',fontsize=11,y=1.02)
plt.tight_layout()
plt.savefig('docs/figures/cascade/cascade_comparison.png',dpi=150,bbox_inches='tight')
print('saved -> docs/figures/cascade/cascade_comparison.png')
print(f'trivalent pts={len(T)}  di/mono pts={len(V)}')
