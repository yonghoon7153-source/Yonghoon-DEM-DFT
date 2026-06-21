import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig,ax=plt.subplots(figsize=(13,8.4)); ax.set_xlim(0,13); ax.set_ylim(0,10); ax.axis('off')
def box(x,y,w,h,txt,fc,fs=10,bold=False):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.08",fc=fc,ec='k',lw=1.4))
    ax.text(x,y,txt,ha='center',va='center',fontsize=fs,fontweight='bold' if bold else 'normal')
def arr(x1,y1,x2,y2,c='#555'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=15,lw=1.5,color=c,shrinkA=2,shrinkB=2))
box(6.5,9.2,8.4,1.0,"Cl enrichment  (LPSCl → LPSCl$_{1.6}$):   2 Cl$^-$ → S$^{2-}$ + V$_{Li}$  (aliovalent)","#ffe8cc",12,True)
box(2.2,6.7,3.0,1.1,"Li vacancies\n(3 / 5 f.u.)","#cfe3f7",10,True)
box(6.3,6.7,3.2,1.1,"anti-site Cl/S\ndisorder (SOF)","#cfe3f7",10,True)
box(10.7,6.7,3.6,1.1,"bonding UNCHANGED\n(ELF·Bader·CDD = control)","#e7e7e7",9.5,True)
arr(5.0,8.7,2.5,7.3); arr(6.4,8.7,6.3,7.3); arr(8.0,8.7,10.3,7.3)
# property boxes with attribution inside (BOTH structural effects feed BOTH)
box(2.5,3.4,3.6,1.45,"σ ×4  (3.4→14 mS/cm)\n— E$_a$↓ ×3.2 (disorder)\n× carrier ×1.41 (vacancy)","#cdeccd",9.3,True)
box(6.6,3.4,3.6,1.45,"E$_{VRH}$ +25%  (22→28 GPa)\n— C$_{44}$↑, Zener A↑ (disorder)\n+ vacancy (relaxed-ion)","#cdeccd",9.3,True)
box(10.7,3.4,3.8,1.45,"oxidation onset SAME 2.14 V\n(free S$^{2-}$-limited; Cl inert)\ncathode reactivity Cl-rich↓","#f7d6d6",9.0,True)
# 4 cross arrows: each structural box -> sigma AND E
arr(2.2,6.1,2.3,4.2); arr(2.6,6.1,5.9,4.2)          # vacancy -> sigma, E
arr(6.0,6.1,3.1,4.2); arr(6.4,6.1,6.5,4.2)          # disorder -> sigma, E
arr(10.7,6.1,10.7,4.2)                                # bonding -> oxidation
ax.text(4.15,5.15,"vacancy + disorder\nBOTH drive σ AND E",fontsize=8,color='#367',ha='center',style='italic')
box(6.5,1.05,12.4,1.0,"Bonding fixed; vacancies + disorder jointly raise σ AND stiffness, preserve the oxidation window, lower cathode reactivity  →  remaining downsides are kinetic / electronic","#fff3bf",9.6,True)
arr(2.5,2.65,5.2,1.6); arr(6.6,2.65,6.5,1.6); arr(10.7,2.65,8.2,1.6)
ax.text(6.5,9.95,"Structure–Property Logic of Argyrodite SEs",ha='center',fontsize=14,fontweight='bold')
plt.tight_layout(); plt.savefig("/tmp/structure_property_logic.png",dpi=190,bbox_inches='tight'); print("ok")
