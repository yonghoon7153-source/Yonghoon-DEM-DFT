import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
s0=3.4; fEa=3.2; fcar=1.41
s1=s0*fEa; s2=s1*fcar
fig,ax=plt.subplots(figsize=(9,5.2))
xs=[0,1,2]; ys=[s0,s1,s2]; labs=["LPSCl\nσ=3.4","×3.2 (E$_a$↓)\n→ 10.9","×1.41 (carrier↑)\n→ 15.3"]
cols=["#bbbbbb","#e7a13d","#2e86de"]
ax.bar(xs,ys,color=cols,width=0.55,zorder=3)
for x,y,l in zip(xs,ys,labs):
    ax.text(x,y+0.4,f"{y:.1f}",ha='center',fontsize=12,fontweight='bold')
ax.axhline(14,color='#16a085',ls='--',lw=1.6)
ax.text(2.45,14,"observed\nLPSCl$_{1.6}$\nσ≈14",color='#16a085',va='center',fontsize=10)
# factor arrows + mechanism labels
ax.annotate("",xy=(1,s1*0.5),xytext=(0,s0*0.5),arrowprops=dict(arrowstyle="-|>",color='#e7a13d',lw=2))
ax.text(0.5,s1*0.52,"×3.2\nanti-site\ndisorder",ha='center',fontsize=9,color='#c47d1a')
ax.annotate("",xy=(2,s2*0.55),xytext=(1,s1*0.55),arrowprops=dict(arrowstyle="-|>",color='#2e86de',lw=2))
ax.text(1.5,s2*0.58,"×1.41\nLi vacancy\n(carrier↑)",ha='center',fontsize=9,color='#1b5a9c')
ax.set_xticks(xs); ax.set_xticklabels(["LPSCl","+ E$_a$↓","+ carrier↑\n= LPSCl$_{1.6}$"],fontsize=10)
ax.set_ylabel("σ (300 K)  (mS/cm)",fontsize=12); ax.set_ylim(0,17)
ax.set_title("Dual-mechanism decomposition of σ↑ (×4)\nσ ratio ×4.5 = E$_a$ factor ×3.2 (disorder) × carrier factor ×1.41 (vacancy)  ≈ observed ×4.1",fontsize=11.5)
ax.grid(axis='y',alpha=0.3)
plt.tight_layout(); plt.savefig("/tmp/dual_mechanism.png",dpi=200,bbox_inches='tight'); print("ok")
