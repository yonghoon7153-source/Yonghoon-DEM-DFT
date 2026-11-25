import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.patches as mp
data={"LPSCl":[(1.24,""),(2.14,"S$^{2-}$→S$_n^{2-}$"),(2.36,"P–S→P$_2$S$_7$"),(3.06,"→S$^0$"),(3.33,"Cl$^-$→SCl")],
      "LPSCl$_{1.6}$":[(1.24,""),(2.14,"S$^{2-}$→S$_n^{2-}$"),(2.36,"P–S→P$_2$S$_7$"),(3.06,"→S$^0$"),(3.33,"Cl$^-$→SCl"),(3.39,"→PCl$_5$")]}
rows={"LPSCl":2.0,"LPSCl$_{1.6}$":0.0}; barh=0.5
fig,ax=plt.subplots(figsize=(12,4.8))
for nm,yy in rows.items():
    ax.barh(yy,1.24,left=0,height=barh,color="#aec7e8")
    ax.barh(yy,2.14-1.24,left=1.24,height=barh,color="#5cb85c")
    ax.barh(yy,3.62-2.14,left=2.14,height=barh,color="#f2a0a0")
    for j,(v,lab) in enumerate(data[nm]):
        ax.plot([v,v],[yy-barh/2,yy+barh/2],'k',lw=1.0,zorder=3)
        if not lab: continue
        off=0.45+(j%2)*0.62
        ax.plot([v,v],[yy+barh/2,yy+off-0.04],color='0.65',lw=0.6,zorder=2)
        ax.annotate(f"{lab}\n{v:.2f} V",(v,yy+off),fontsize=8.5,ha='center',va='bottom',zorder=4)
    ax.text(-0.06,yy,nm,ha='right',va='center',fontsize=13,fontweight='bold')
    ax.text(1.69,yy,"OCV\n1.72",ha='center',va='center',fontsize=7,color='#333')
ax.axvspan(1.24,2.14,color='none')
ax.text(1.69,yy+1.55 if False else 2.0+0.92,"",ha='center')  # noop
ax.set_xlim(-0.02,3.7); ax.set_ylim(-0.55,3.75); ax.set_yticks([])
ax.set_xlabel("V vs Li/Li$^+$",fontsize=12)
ax.set_title("Grand-potential decomposition (MP Li-P-S-Cl hull): S$^{2-}$ oxidizes first (2.14 V), Cl$^-$ last (3.3 V)\n→ Cl-rich does NOT raise the oxidation onset (S$^{2-}$-limited in both)",fontsize=11)
for sp in ['top','right','left']: ax.spines[sp].set_visible(False)
ax.legend(handles=[mp.Patch(color="#aec7e8",label="reduced (<1.24 V)"),mp.Patch(color="#5cb85c",label="stable 1.24–2.14 V"),mp.Patch(color="#f2a0a0",label="oxidized (>2.14 V)")],loc='lower right',ncol=3,fontsize=8.5,frameon=False)
plt.tight_layout(); plt.savefig("/tmp/esw_staircase_clean.png",dpi=190,bbox_inches='tight'); print("ok")
