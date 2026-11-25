import numpy as np, glob, re, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
def grp(pre,elem,idx,wfc='2(p)'):
    E=None;t=None
    for f in glob.glob(f'{pre}.pdos_atm#*({elem})_wfc#{wfc}'):
        n=int(re.search(r'atm#(\d+)',f).group(1))
        if n not in idx: continue
        d=np.loadtxt(f); E=d[:,0] if E is None else E; t=d[:,1] if t is None else t+d[:,1]
    return E,t
def allidx(pre,elem):
    return {int(re.search(r'atm#(\d+)',f).group(1)) for f in glob.glob(f'{pre}.pdos_atm#*({elem})_wfc#2(p)')}
sys=[("comp1","comp1",set(range(49,53)),set(range(5,21)),2.130,4.190,"comp1 (LPSCl): 4 free-S"),
     ("mc/modelc","modelc",set([54,57]),set(range(33,53)),2.445,4.544,"modelc (LPSCl$_{1.6}$): 2 free-S")]
fig,axs=plt.subplots(1,2,figsize=(14,5.6),sharey=True)
for k,(pre,nm,free,ps4,vbm,cbm,lab) in enumerate(sys):
    E,fS=grp(pre,"S",free); _,pS=grp(pre,"S",ps4); _,Clp=grp(pre,"Cl",allidx(pre,"Cl"))
    Es=E-vbm; o=Es<=0.05
    mf=(Es*fS)[o].sum()/fS[o].sum(); mp=(Es*pS)[o].sum()/pS[o].sum()
    mc=(Es*Clp)[o].sum()/Clp[o].sum()
    ax=axs[k]
    ax.fill_between(Es,fS/len(free),color="#d62728",alpha=0.75,label=f"free S$^{{2-}}$/atom (×{len(free)})")
    ax.plot(Es,pS/len(ps4),color="#1f77b4",lw=2,label=f"PS$_4$-S/atom (×{len(ps4)})")
    ax.plot(Es,Clp/max(1,len(allidx(pre,'Cl'))),color="#2ca02c",lw=1.4,ls='--',label=f"Cl 3p/atom (×{len(allidx(pre,'Cl'))})")
    for mm,c in [(mf,"#d62728"),(mp,"#1f77b4"),(mc,"#2ca02c")]:
        ax.axvline(mm,color=c,lw=1.2,ls=':')
    ax.axvline(0,color='k',lw=1.2); ax.axvspan(0,cbm-vbm,color='0.92',zorder=0)
    ax.text(0.02,0.99,"VBM",transform=ax.transAxes,va='top',fontsize=9)
    ax.set_title(f"{lab}\nmean 3p: free-S {mf:.2f}, PS$_4$-S {mp:.2f}, Cl {mc:.2f} eV",fontsize=11)
    ax.set_xlim(-7,5); ax.set_ylim(0,None); ax.set_xlabel("E − E$_{VBM}$ (eV)")
    ax.legend(fontsize=8.5,loc='upper left')
    print(f"{nm}: free-S/atom mean {mf:.2f}, PS4 {mp:.2f}, Cl {mc:.2f}; free shallower {mp-mf:+.2f}")
axs[0].set_ylabel("per-atom PDOS (states/eV)")
fig.suptitle("Site-projected 3p PDOS: free S$^{2-}$ is the shallowest (oxidation-prone) S in BOTH — Cl-rich just has fewer of them (4→2)",fontsize=12)
plt.tight_layout(rect=[0,0,1,0.95]); plt.savefig("comp1_vs_modelc_pdos.png",dpi=200); print("-> comp1_vs_modelc_pdos.png")
