import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
V=[2.5,3.0,3.5,4.0,4.3]
d={ "LiCoO$_2$":{"LPSCl":[-0.6662,-0.8101,-1.0108,-1.3150,-1.5438],"LPSCl$_{1.6}$":[-0.6238,-0.7300,-0.8859,-1.1655,-1.3459]},
    "LiNiO$_2$":{"LPSCl":[-0.8191,-0.9394,-1.1277,-1.4153,-1.6072],"LPSCl$_{1.6}$":[-0.7762,-0.8652,-1.0316,-1.2818,-1.4493]},
    "NMC811":{"LPSCl":[-0.7505,-0.8830,-1.0818,-1.3799,-1.5788],"LPSCl$_{1.6}$":[-0.7098,-0.8143,-0.9853,-1.2395,-1.4147]}}
col={"LiCoO$_2$":"#1f77b4","LiNiO$_2$":"#d62728","NMC811":"#2ca02c"}
fig,(ax,ax2)=plt.subplots(1,2,figsize=(13,5.2))
for cat,c in col.items():
    ax.plot(V,d[cat]["LPSCl"],'-o',color=c,lw=2,ms=5,label=f"{cat} · LPSCl")
    ax.plot(V,d[cat]["LPSCl$_{1.6}$"],'--s',color=c,lw=2,ms=5,mfc='white',label=f"{cat} · LPSCl$_{{1.6}}$")
    diff=np.array(d[cat]["LPSCl$_{1.6}$"])-np.array(d[cat]["LPSCl"])  # >0 means LPSCl1.6 less reactive
    ax2.plot(V,diff,'-o',color=c,lw=2,ms=5,label=cat)
ax.set_xlabel("V vs Li/Li$^+$"); ax.set_ylabel("interface reaction energy (eV/atom)")
ax.set_title("(a) SE/cathode reactivity vs voltage\nsolid=LPSCl, dashed=LPSCl$_{1.6}$ — LPSCl always more reactive (lower)")
ax.legend(fontsize=7.5,ncol=3,loc='lower left'); ax.grid(alpha=0.3); ax.invert_yaxis()
ax2.axhline(0,color='k',lw=0.8)
ax2.set_xlabel("V vs Li/Li$^+$"); ax2.set_ylabel("ΔE(LPSCl$_{1.6}$) − ΔE(LPSCl)  (eV/atom)")
ax2.set_title("(b) LPSCl$_{1.6}$ is LESS reactive (gap > 0)\nand the gap GROWS with voltage")
ax2.legend(fontsize=9); ax2.grid(alpha=0.3)
fig.suptitle("Voltage-resolved SE/cathode interface reactivity (GrandPotentialInterfacialReactivity, MP GGA+U)",fontsize=12,y=1.0)
plt.tight_layout(); plt.savefig("/tmp/interface_reactivity_v2.png",dpi=190,bbox_inches='tight'); print("ok")
