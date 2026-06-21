import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.image as mpimg
im=mpimg.imread("/home/user/Yonghoon-DEM-DFT/docs/figures/elf_licl/Li_density_core_spread_comp1_modelc.png")[110:,:,:]
H,W=im.shape[:2]
fig=plt.figure(figsize=(13,6.6)); ax=fig.add_axes([0,0,1,1]); ax.imshow(im); ax.axis('off')
# work in pixel coords (0..W, 0..H), y down
def tx(fx): return fx*W
def ty(fy): return fy*H
A=dict(arrowstyle='-|>',lw=2.4)
# ---- comp1 (left panel ~ x 0.04-0.47) ----
ax.annotate("intra-cage core\n(Li localized, fast LOCAL)",
            xy=(tx0:=tx(0.20),ty0:=ty(0.42)), xytext=(tx(0.02),ty(0.12)),
            fontsize=12,color='#b8860b',fontweight='bold',
            arrowprops=dict(color='#b8860b',**A),
            bbox=dict(fc='white',ec='#b8860b',alpha=0.9))
ax.annotate("inter-cage gap = DARK\n(low Li density → high barrier)\n→ cages ISOLATED",
            xy=(tx(0.30),ty(0.60)), xytext=(tx(0.02),ty(0.80)),
            fontsize=12,color='#444',fontweight='bold',
            arrowprops=dict(color='#444',ls='--',**A),
            bbox=dict(fc='white',ec='#444',alpha=0.9))
# ---- modelc (right panel ~ x 0.53-0.96) ----
ax.annotate("inter-cage BRIDGE\n(Li spreads toward Cl)",
            xy=(tx(0.70),ty(0.40)), xytext=(tx(0.55),ty(0.10)),
            fontsize=12,color='#1b5a9c',fontweight='bold',
            arrowprops=dict(color='#1b5a9c',**A),
            bbox=dict(fc='white',ec='#1b5a9c',alpha=0.9))
# hopping arrows (cage -> cage) on modelc
for (x1,y1,x2,y2) in [(0.66,0.55,0.78,0.45),(0.72,0.68,0.82,0.58)]:
    ax.annotate("",xy=(tx(x2),ty(y2)),xytext=(tx(x1),ty(y1)),
                arrowprops=dict(color='#d62728',lw=2.2,arrowstyle='-|>'))
ax.annotate("→ PERCOLATING Li network\n(E$_a$↓, σ↑)",
            xy=(tx(0.80),ty(0.62)), xytext=(tx(0.60),ty(0.86)),
            fontsize=12.5,color='#d62728',fontweight='bold',
            arrowprops=dict(color='#d62728',**A),
            bbox=dict(fc='#fff3bf',ec='#d62728',alpha=0.95))
fig.text(0.25,0.99,"LPSCl — isolated cages",ha='center',fontsize=14,fontweight='bold',color='#b8860b')
fig.text(0.75,0.99,"LPSCl$_{1.6}$ — connected (inter-cage)",ha='center',fontsize=14,fontweight='bold',color='#1b5a9c')
plt.savefig('/tmp/intercage_annotated.png',dpi=150,bbox_inches='tight'); print("ok",W,H)
