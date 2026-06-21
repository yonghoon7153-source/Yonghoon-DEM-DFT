import numpy as np, glob, re, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
def grp(elem,idx,wfc='2(p)'):
    E=None;t=None
    for f in glob.glob(f'comp1.pdos_atm#*({elem})_wfc#{wfc}'):
        n=int(re.search(r'atm#(\d+)',f).group(1))
        if n not in idx: continue
        d=np.loadtxt(f); E=d[:,0] if E is None else E; t=d[:,1] if t is None else t+d[:,1]
    return E,t
free=set(range(49,53)); ps4=set(range(5,21))
E,fS=grp('S',free); _,pS=grp('S',ps4)
allCl={int(re.search(r'atm#(\d+)',f).group(1)) for f in glob.glob('comp1.pdos_atm#*(Cl)_wfc#2(p)')}
_,Clp=grp('Cl',allCl)
vbm,cbm=2.130,4.190; Es=E-vbm; occ=Es<=0.05
mf=(Es*fS)[occ].sum()/fS[occ].sum(); mp=(Es*pS)[occ].sum()/pS[occ].sum()
fig,axs=plt.subplots(1,2,figsize=(14,5.6),sharex=True)
ax=axs[0]
ax.fill_between(Es,fS,color="#d62728",alpha=0.75,label="free S$^{2-}$ 3p (4a, 4 atoms)")
ax.plot(Es,pS,color="#1f77b4",lw=2,label="PS$_4$ S 3p (16e, 16 atoms)")
ax.plot(Es,Clp,color="#2ca02c",lw=1.3,ls='--',label="Cl 3p")
ax.set_title("(a) TOTAL per site type\n(PS$_4$-S larger — just 4x more atoms)")
ax.legend(fontsize=9,loc='upper left')
ax=axs[1]
ax.fill_between(Es,fS/4,color="#d62728",alpha=0.75,label="free S$^{2-}$ 3p / atom")
ax.plot(Es,pS/16,color="#1f77b4",lw=2,label="PS$_4$ S 3p / atom")
ax.axvline(mf,color="#d62728",lw=1.6,ls=':'); ax.axvline(mp,color="#1f77b4",lw=1.6,ls=':')
ax.annotate(f"mean 3p\nfree-S {mf:.2f} eV",(mf,0.92),xycoords=('data','axes fraction'),
            color="#d62728",fontsize=9,ha='center')
ax.annotate(f"PS$_4$-S {mp:.2f} eV",(mp,0.82),xycoords=('data','axes fraction'),
            color="#1f77b4",fontsize=9,ha='center')
ax.annotate("", xy=(mf,0.5),xytext=(mp,0.5),xycoords=('data','axes fraction'),
            arrowprops=dict(arrowstyle="<->",color='k'))
ax.annotate(f"{mp-mf:+.2f} eV\n(free-S shallower)",xy=((mf+mp)/2,0.55),xycoords=('data','axes fraction'),
        ha='center',fontsize=9)
ax.set_title("(b) PER-ATOM (fair)\nfree S$^{2-}$ 3p centered 1.3 eV closer to VBM")
ax.legend(fontsize=9,loc='upper left')
for ax in axs:
    ax.axvline(0,color='k',lw=1.2); ax.axvspan(0,cbm-vbm,color='0.92',zorder=0)
    ax.text(0.015,0.99,"VBM",transform=ax.transAxes,fontsize=9,va='top')
    ax.set_xlim(-7,5); ax.set_ylim(0,None); ax.set_xlabel("E − E$_{VBM}$ (eV)")
axs[0].set_ylabel("PDOS (states/eV)")
fig.suptitle("comp1 (LPSCl): free S$^{2-}$ (4a) 3p is the shallowest, least-bound S → oxidation-prone (S$^{2-}$→S$^0$); PS$_4$-S pulled down by P–S covalency",fontsize=12)
plt.tight_layout(rect=[0,0,1,0.95]); plt.savefig("comp1_pdos_site.png",dpi=200); print("-> updated comp1_pdos_site.png")
