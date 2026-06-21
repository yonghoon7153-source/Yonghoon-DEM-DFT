import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.patches as mp
NAMES=["LPSCl","LPSCl$_{1.6}$"]
# ---------- (1) window bar ----------
fig,ax=plt.subplots(figsize=(11,3.2))
for i,nm in enumerate(NAMES):
    yy=1-i
    ax.barh(yy,1.24,left=0,height=0.5,color="#aec7e8")
    ax.barh(yy,2.14-1.24,left=1.24,height=0.5,color="#5cb85c")
    ax.barh(yy,5-2.14,left=2.14,height=0.5,color="#f2a0a0")
    ax.text(-0.06,yy,nm,ha='right',va='center',fontsize=13,fontweight='bold')
for v in (1.24,2.14):
    ax.plot([v,v],[-0.35,1.35],'k--',lw=1.2)
ax.plot([1.72,1.72],[-0.35,1.35],color='0.5',ls=':',lw=1.2)
ax.text(1.24,1.55,"reduction limit\n1.24 V\n(→Li$_3$P, Li$_2$S)",ha='center',fontsize=9)
ax.text(2.14,1.55,"oxidation onset\n2.14 V\n(S$^{2-}$→polysulfide)",ha='center',fontsize=9,color='#b22')
ax.text(1.72,-0.5,"OCV 1.72 V",ha='center',fontsize=8,color='0.4')
ax.text(1.69,0.5,"stable",ha='center',fontsize=11,color='#2a7',fontweight='bold')
ax.set_xlim(-0.02,5); ax.set_ylim(-0.6,2.1); ax.set_yticks([]); ax.set_xlabel("V vs Li/Li$^+$",fontsize=12)
ax.set_title("Grand-potential ESW (MP hull) — LPSCl = LPSCl$_{1.6}$ (S$^{2-}$-limited, identical window)",fontsize=12)
for sp in ['top','right','left']: ax.spines[sp].set_visible(False)
ax.legend(handles=[mp.Patch(color="#aec7e8",label="reduced"),mp.Patch(color="#5cb85c",label="stable"),mp.Patch(color="#f2a0a0",label="oxidized")],loc='lower right',ncol=3,fontsize=9,frameon=False)
plt.tight_layout(); plt.savefig("/tmp/esw_bar_clean.png",dpi=200,bbox_inches='tight')
# ---------- (2) staircase ----------
data={"LPSCl":[(1.24,""),(2.14,"S$^{2-}$→S$_n^{2-}$"),(2.36,"P–S→P$_2$S$_7$"),(3.06,"→S$^0$"),(3.33,"Cl$^-$→SCl")],
      "LPSCl$_{1.6}$":[(1.24,""),(2.14,"S$^{2-}$→S$_n^{2-}$"),(2.36,"P–S→P$_2$S$_7$"),(3.06,"→S$^0$"),(3.33,"Cl$^-$→SCl"),(3.39,"→PCl$_5$")]}
fig,ax=plt.subplots(figsize=(11,3.6))
for i,nm in enumerate(NAMES):
    yy=1.0-i
    ax.barh(yy,1.24,left=0,height=0.5,color="#aec7e8")
    ax.barh(yy,2.14-1.24,left=1.24,height=0.5,color="#5cb85c")
    ax.barh(yy,3.6-2.14,left=2.14,height=0.5,color="#f2a0a0")
    for v,lab in data[nm]:
        ax.plot([v,v],[yy-0.25,yy+0.25],color='k',lw=1.1)
        if lab: ax.annotate(lab+f"\n{v:.2f}V",(v,yy+0.28),fontsize=8,ha='center',va='bottom')
    ax.text(-0.05,yy,nm,ha='right',va='center',fontsize=13,fontweight='bold')
    ax.text(1.69,yy,"OCV\n1.72",ha='center',va='center',fontsize=7,color='#333')
ax.text(1.69,1.62,"stable 1.24–2.14 V",ha='center',fontsize=9,color='#2a7')
ax.set_xlim(-0.02,3.62); ax.set_ylim(-0.6,2.0); ax.set_yticks([]); ax.set_xlabel("V vs Li/Li$^+$",fontsize=12)
ax.set_title("Grand-potential decomposition (MP Li-P-S-Cl hull): S$^{2-}$ oxidizes first (2.14 V), Cl$^-$ last (3.3 V)\n→ Cl-rich does NOT raise the oxidation onset (S$^{2-}$-limited in both)",fontsize=11)
for sp in ['top','right','left']: ax.spines[sp].set_visible(False)
ax.legend(handles=[mp.Patch(color="#aec7e8",label="reduced"),mp.Patch(color="#5cb85c",label="stable"),mp.Patch(color="#f2a0a0",label="oxidized")],loc='lower right',ncol=3,fontsize=8,frameon=False)
plt.tight_layout(); plt.savefig("/tmp/esw_staircase_clean.png",dpi=200,bbox_inches='tight')
print("ok")
