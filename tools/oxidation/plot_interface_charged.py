import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
V=[3.5,4.0,4.3,4.5]
d={"CoO$_2$":{"LPSCl":[-1.0505,-1.2867,-1.5438,-1.7153],"LPSCl$_{1.6}$":[-0.9273,-1.1342,-1.2798,-1.4249]},
   "NiO$_2$":{"LPSCl":[-1.1369,-1.3526,-1.5438,-1.7153],"LPSCl$_{1.6}$":[-1.0411,-1.2099,-1.3465,-1.4435]},
   "NMC811(chg)":{"LPSCl":[-1.0813,-1.3487,-1.5438,-1.7153],"LPSCl$_{1.6}$":[-0.9848,-1.2033,-1.3611,-1.4705]}}
col={"CoO$_2$":"#1f77b4","NiO$_2$":"#d62728","NMC811(chg)":"#2ca02c"}
fig,(ax,ax2)=plt.subplots(1,2,figsize=(13,5.2))
for c,k in col.items():
    ax.plot(V,d[c]["LPSCl"],'-o',color=k,lw=2,ms=5,label=f"{c}·LPSCl")
    ax.plot(V,d[c]["LPSCl$_{1.6}$"],'--s',color=k,lw=2,ms=5,mfc='white',label=f"{c}·LPSCl$_{{1.6}}$")
    ax2.plot(V,np.array(d[c]["LPSCl$_{1.6}$"])-np.array(d[c]["LPSCl"]),'-o',color=k,lw=2,ms=5,label=c)
ax.invert_yaxis(); ax.grid(alpha=0.3); ax.set_xlabel("V vs Li/Li$^+$"); ax.set_ylabel("interface reaction energy (eV/atom)")
ax.set_title("(a) SE / CHARGED(delithiated) cathode reactivity\nsolid=LPSCl, dashed=LPSCl$_{1.6}$ — LPSCl always more reactive")
ax.legend(fontsize=7.5,ncol=3,loc='lower left')
ax.annotate("LPSCl cathode-independent\nat high V (= SE oxidation)",(4.3,-1.5438),xytext=(3.6,-1.65),
            fontsize=8,arrowprops=dict(arrowstyle='->',color='k'))
ax2.axhline(0,color='k',lw=0.8); ax2.grid(alpha=0.3); ax2.legend(fontsize=9)
ax2.set_xlabel("V vs Li/Li$^+$"); ax2.set_ylabel("ΔE(LPSCl$_{1.6}$)−ΔE(LPSCl) (eV/atom)")
ax2.set_title("(b) Cl-rich LESS reactive (gap>0), grows with V\n(charged cathodes, up to +0.29 @4.5V)")
fig.suptitle("Charged(delithiated)-cathode interface reactivity — confirms & strengthens v2: Cl-rich thermodynamically LESS reactive",fontsize=12,y=1.0)
plt.tight_layout(); plt.savefig("/tmp/interface_charged.png",dpi=190,bbox_inches='tight'); print("ok")
