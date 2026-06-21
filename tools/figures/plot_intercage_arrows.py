import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyArrowPatch, Patch
im=mpimg.imread('/home/user/Yonghoon-DEM-DFT/docs/figures/elf_licl/Li_density_core_spread_comp1_modelc.png')[110:,:,:]
H,W=im.shape[:2]
fig=plt.figure(figsize=(13,6.4)); ax=fig.add_axes([0,0,1,1]); ax.imshow(im); ax.axis('off')
def X(f): return f*W
def Y(f): return f*H
def arr(x1,y1,x2,y2,c,lw=3.0,ls='-'):
    ax.add_patch(FancyArrowPatch((X(x1),Y(y1)),(X(x2),Y(y2)),arrowstyle='-|>',
        mutation_scale=22,lw=lw,color=c,linestyle=ls,shrinkA=0,shrinkB=0))
# ---- LPSCl (left): blue intra (local), red inter BLOCKED ----
arr(0.155,0.34,0.205,0.34,'#1f77b4',2.6)          # intra-cage local
arr(0.155,0.62,0.205,0.62,'#1f77b4',2.6)
arr(0.22,0.46,0.30,0.46,'#d62728',3.4,'--')        # inter-cage blocked (across dark gap)
ax.text(X(0.26),Y(0.40),"✗",color='#d62728',fontsize=22,ha='center',va='center',fontweight='bold')
arr(0.30,0.62,0.225,0.62,'#d62728',3.4,'--')
ax.text(X(0.265),Y(0.56),"✗",color='#d62728',fontsize=22,ha='center',va='center',fontweight='bold')
# ---- LPSCl1.6 (right): blue intra, green inter OPEN ----
arr(0.62,0.36,0.665,0.36,'#1f77b4',2.6)
arr(0.66,0.50,0.79,0.44,'#2ca02c',3.6)             # inter-cage open (along bridge)
arr(0.70,0.66,0.83,0.58,'#2ca02c',3.6)
arr(0.60,0.60,0.70,0.66,'#2ca02c',3.6)
fig.text(0.25,0.985,"LPSCl",ha='center',fontsize=15,fontweight='bold',color='#b8860b')
fig.text(0.75,0.985,"LPSCl$_{1.6}$",ha='center',fontsize=15,fontweight='bold',color='#1b5a9c')
leg=[Patch(color='#1f77b4',label='intra-cage hop (local, fast)'),
     Patch(color='#d62728',label='inter-cage BLOCKED (high barrier)'),
     Patch(color='#2ca02c',label='inter-cage OPEN (percolating)')]
ax.legend(handles=leg,loc='lower center',ncol=3,fontsize=11,framealpha=0.95,bbox_to_anchor=(0.5,-0.02))
plt.savefig('/tmp/bvse_arrows.png',dpi=150,bbox_inches='tight'); print("ok")
