import numpy as np, glob, re, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
def grp_sum(prefix, elem, idxset, wfc='2(p)'):
    E=None; tot=None
    for f in glob.glob(f"{prefix}.pdos_atm#*({elem})_wfc#{wfc}"):
        n=int(re.search(r'atm#(\d+)',f).group(1))
        if n not in idxset: continue
        d=np.loadtxt(f)
        if E is None: E=d[:,0]; tot=np.zeros_like(E)
        tot=tot+d[:,1]
    return E,tot
pre="comp1"; freeS=set(range(49,53)); ps4S=set(range(5,21))
E,fS=grp_sum(pre,"S",freeS); _,pS=grp_sum(pre,"S",ps4S)
allCl={int(re.search(r'atm#(\d+)',f).group(1)) for f in glob.glob(f"{pre}.pdos_atm#*(Cl)_wfc#2(p)")}
_,Clp=grp_sum(pre,"Cl",allCl)
vbm,cbm=2.130,4.190; Es=E-vbm
fig,axs=plt.subplots(1,2,figsize=(14,5.5),sharex=True)
# (a) total site-projected
ax=axs[0]
ax.fill_between(Es,fS,color="#d62728",alpha=0.75,label="free S$^{2-}$ 3p (4a, 4 atoms)")
ax.plot(Es,pS,color="#1f77b4",lw=2,label="PS$_4$ S 3p (16e, 16 atoms)")
ax.plot(Es,Clp,color="#2ca02c",lw=1.4,ls='--',label="Cl 3p (4 atoms)")
ax.set_title("(a) total per site type"); ax.legend(fontsize=9,loc='upper left')
# (b) per-atom normalized
ax=axs[1]
ax.fill_between(Es,fS/len(freeS),color="#d62728",alpha=0.75,label="free S$^{2-}$ 3p / atom")
ax.plot(Es,pS/len(ps4S),color="#1f77b4",lw=2,label="PS$_4$ S 3p / atom")
ax.plot(Es,Clp/max(1,len(allCl)),color="#2ca02c",lw=1.4,ls='--',label="Cl 3p / atom")
ax.set_title("(b) per-atom (fair compare)  →  free S$^{2-}$ ~2x at VBM"); ax.legend(fontsize=9,loc='upper left')
for ax in axs:
    ax.axvline(0,color='k',lw=1.2); ax.axvspan(0,cbm-vbm,color='0.92',zorder=0)
    ax.text(0.03,0.96,"VBM",transform=ax.transAxes,fontsize=10,va='top')
    ax.set_xlim(-7,5); ax.set_ylim(0,None); ax.set_xlabel("E − E$_{VBM}$ (eV)")
axs[0].set_ylabel("PDOS (states/eV)")
fig.suptitle("comp1 (LPSCl) site-projected S 3p PDOS — free S$^{2-}$ (4a) dominates the VBM = oxidation-prone site",fontsize=13)
plt.tight_layout(rect=[0,0,1,0.96]); plt.savefig("comp1_pdos_site.png",dpi=200); print("-> comp1_pdos_site.png")
