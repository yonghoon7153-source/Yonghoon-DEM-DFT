import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
C1,CM='#d62728','#1f77b4'  # comp1 red, modelc blue
def load_csv(p):
    rows=[]
    for l in open(p):
        t=l.strip().split(',')
        try: rows.append([float(x) for x in t])
        except: pass
    return np.array(rows)

fig,ax=plt.subplots(2,3,figsize=(18,10.5))

# (a) master ratio modelc/comp1
a=ax[0,0]
P=[('gap',1.82/1.76,'inv'),('ICOHP\nP-S',6.000/5.944,'inv'),
   ('B0\n(EOS)',21.71/26.23,'chg'),('Ea',0.224/0.2532,'chg'),('ICOHP\nLi-Cl',2.103/1.855,'chg'),
   ('E_VRH\n(relaxed)',27.66/22.06,'chg'),('G_VRH\n(relaxed)',10.61/8.13,'chg'),
   ('D\n(600K)',7.90/3.09,'chg'),('sigma\n(300K)',13.96/3.35,'chg')]
labs=[p[0] for p in P]; vals=[p[1] for p in P]
cols=['#2ca02c' if p[2]=='inv' else (CM if p[1]>=1 else C1) for p in P]
x=np.arange(len(P)); a.bar(x,vals,color=cols,edgecolor='k',lw=.5)
a.axhline(1,color='k',lw=1,ls='--'); a.set_yscale('log')
a.axvspan(-0.5,1.5,color='#2ca02c',alpha=.07)
a.text(0.5,a.get_ylim()[1]*0.7,'INVARIANT',ha='center',color='green',fontsize=8,weight='bold')
a.text(5.5,a.get_ylim()[1]*0.7,'CHANGED',ha='center',color='navy',fontsize=8,weight='bold')
for i,v in enumerate(vals): a.text(i,v*(1.05 if v>=1 else .9),f'{v:.2f}x',ha='center',fontsize=7,va='bottom' if v>=1 else 'top')
a.set_xticks(x); a.set_xticklabels(labs,fontsize=7.5); a.set_ylabel('modelc / comp1 ratio (log)')
a.set_title('(a) LPSCl1.6 vs LPSCl: what changes',weight='bold'); a.grid(alpha=.3,axis='y')

# (b) EOS E-V (dE vs V/V0)
a=ax[1,0]
for f,V0,c,lab,B in [('paper_figures/comp1_eos_fit.csv',1016.62,C1,'LPSCl (B0 26.2)',26.2),
                     ('paper_figures/modelc_eos_fit.csv',1216.44,CM,'LPSCl1.6 (B0 21.7)',21.7)]:
    d=load_csv(f); V,E=d[:,0],d[:,1]; a.plot(V/V0,(E-E.min())*1000,c=c,lw=2,label=lab)
    try:
        pp=load_csv(f.replace('_fit','_points')); a.scatter(pp[:,0]/V0,(pp[:,1]-E.min())*1000,c=c,s=25,zorder=5,edgecolor='k',lw=.3)
    except: pass
a.set_xlabel('V / V0'); a.set_ylabel('E - E0 (meV)'); a.set_title('(b) EOS: Cl-rich softer bulk (B0 down)'); a.legend(fontsize=8); a.grid(alpha=.3)

# (c) elastic 3-regime E_VRH
a=ax[0,1]
reg=['clamped-ion\n0K (QE)','relaxed-ion\n0K (QE)','MLIP\n600K (UMA)']
e1=[52.31,22.06,59.71]; em=[52.30,27.66,52.72]; x=np.arange(3); w=.36
a.bar(x-w/2,e1,w,color=C1,label='LPSCl',edgecolor='k',lw=.4); a.bar(x+w/2,em,w,color=CM,label='LPSCl1.6',edgecolor='k',lw=.4)
for i,(p,q) in enumerate(zip(e1,em)):
    a.text(i-w/2,p+1,f'{p:.0f}',ha='center',fontsize=7); a.text(i+w/2,q+1,f'{q:.0f}',ha='center',fontsize=7)
a.set_xticks(x); a.set_xticklabels(reg,fontsize=8); a.set_ylabel('E_VRH (GPa)')
a.set_title('(c) Elastic regimes: clamped=identical -> relaxed inverts'); a.legend(fontsize=8); a.grid(alpha=.3,axis='y')
a.annotate('+25%\n(vacancy\nparadox\nresolved)',(1,27.66),xytext=(1.35,40),fontsize=7,color='navy',ha='center',arrowprops=dict(arrowstyle='->',color='navy'))

# (d) ICOHP bonding
a=ax[1,1]
bonds=['P-S','Li-Cl','Li-S','S-S']; b1=[5.944,1.855,1.592,0.107]; bm=[6.000,2.103,1.717,0.110]
x=np.arange(4); a.bar(x-w/2,b1,w,color=C1,label='LPSCl',edgecolor='k',lw=.4); a.bar(x+w/2,bm,w,color=CM,label='LPSCl1.6',edgecolor='k',lw=.4)
for i,(p,q) in enumerate(zip(b1,bm)): a.text(i,max(p,q)+0.1,f'{(q/p-1)*100:+.0f}%',ha='center',fontsize=7.5,weight='bold')
a.set_xticks(x); a.set_xticklabels(bonds); a.set_ylabel('-ICOHP (eV/bond)  (bond strength)')
a.set_title('(d) Bonding: PS4 framework fixed, Li-anion strengthens'); a.legend(fontsize=8); a.grid(alpha=.3,axis='y')

# (e) Voronoi disorder fingerprint
a=ax[0,2]
els=['P','Cl','Li','S']; v1=[0.00,0.00,0.21,3.41]; vm=[0.37,0.74,1.15,2.05]
x=np.arange(4); a.bar(x-w/2,v1,w,color=C1,label='LPSCl',edgecolor='k',lw=.4); a.bar(x+w/2,vm,w,color=CM,label='LPSCl1.6',edgecolor='k',lw=.4)
a.set_xticks(x); a.set_xticklabels(els); a.set_ylabel('Voronoi volume std (A^3)')
a.set_title('(e) Disorder fingerprint: Li x5.5, S paradox-down, P~fixed'); a.legend(fontsize=8); a.grid(alpha=.3,axis='y')
a.annotate('Li x5.5',(2,1.15),xytext=(2.2,2.5),fontsize=7,color='navy',arrowprops=dict(arrowstyle='->'))

# (f) Arrhenius
a=ax[1,2]
d=load_csv('docs/figures/slide09_arrhenius/arrhenius_fit_origin.csv')
dat=d[~np.isnan(d[:,1])]; fit=d[~np.isnan(d[:,4])]
a.scatter(dat[:,0],dat[:,1],c=C1,s=45,zorder=5,edgecolor='k'); a.scatter(dat[:,0],dat[:,2],c=CM,s=45,zorder=5,edgecolor='k')
a.plot(fit[:,3],fit[:,4],c=C1,lw=1.8,label='LPSCl (Ea 0.253)'); a.plot(fit[:,3],fit[:,5],c=CM,lw=1.8,label='LPSCl1.6 (Ea 0.224)')
a.set_xlabel('1000/T (1/K)'); a.set_ylabel('ln D (cm2/s)'); a.set_title('(f) Arrhenius: Cl-rich lower Ea + higher D'); a.legend(fontsize=8); a.grid(alpha=.3)

plt.suptitle('Paper #1: Li6PS5Cl (LPSCl) vs Li5.4PS4.4Cl1.6 (LPSCl1.6) — disorder, not electronics, drives the differences',fontsize=13,y=1.01,weight='bold')
plt.tight_layout(); plt.savefig('docs/figures/paper1_master_comparison.png',dpi=150,bbox_inches='tight')
print('saved -> docs/figures/paper1_master_comparison.png')
