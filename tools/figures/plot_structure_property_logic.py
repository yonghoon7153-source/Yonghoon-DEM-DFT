import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig,ax=plt.subplots(figsize=(13,8.2)); ax.set_xlim(0,13); ax.set_ylim(0,10); ax.axis('off')
def box(x,y,w,h,txt,fc,fs=10,bold=False):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.08",fc=fc,ec='k',lw=1.4))
    ax.text(x,y,txt,ha='center',va='center',fontsize=fs,fontweight='bold' if bold else 'normal')
def arr(x1,y1,x2,y2,lab='',c='#444',lx=0,ly=0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=16,lw=1.6,color=c,shrinkA=2,shrinkB=2))
    if lab: ax.text((x1+x2)/2+lx,(y1+y2)/2+ly,lab,fontsize=8.5,color=c,ha='center',style='italic',
                    bbox=dict(fc='white',ec='none',alpha=0.9,pad=0.5))
box(6.5,9.2,8.4,1.0,"Cl enrichment  (LPSCl → LPSCl$_{1.6}$):   2 Cl$^-$ → S$^{2-}$ + V$_{Li}$  (aliovalent)","#ffe8cc",12,True)
box(2.2,6.7,3.0,1.1,"Li vacancies\n(3 / 5 f.u.)","#cfe3f7",10,True)
box(6.3,6.7,3.2,1.1,"anti-site Cl/S\ndisorder (SOF)","#cfe3f7",10,True)
box(10.7,6.7,3.6,1.1,"bonding UNCHANGED\n(ELF·Bader·CDD = control)","#e7e7e7",9.5,True)
arr(5.0,8.7,2.5,7.3); arr(6.4,8.7,6.3,7.3); arr(8.0,8.7,10.3,7.3)
box(2.2,3.5,3.0,1.15,"σ ×4\n(3.4 → 14 mS/cm)","#cdeccd",10.5,True)
box(6.0,3.5,3.0,1.15,"E$_{VRH}$ +25%\n(22 → 28 GPa)","#cdeccd",10.5,True)
box(10.6,3.5,4.0,1.2,"oxidation onset SAME\n2.14 V (free S$^{2-}$-limited)\ncathode reactivity Cl-rich↓","#f7d6d6",9.3,True)
arr(2.2,6.1,2.2,4.1,"carrier ↑ ×1.41",lx=-0.95,ly=0)
arr(5.7,6.1,2.9,4.15,"E$_a$ ↓ ×3.2",lx=0.55,ly=0.35)
arr(2.9,6.1,5.5,4.15,"relaxed-ion\n(paradox solved)",lx=0.6,ly=-0.15)
arr(10.7,6.1,10.6,4.15,"gap same · VBM=S 3p",lx=1.25,ly=0)
box(6.5,1.05,12.4,1.0,"Bonding fixed; vacancies + disorder alone raise σ & stiffness, preserve the oxidation window, and lower cathode reactivity  →  remaining downsides are kinetic / electronic","#fff3bf",9.8,True)
arr(2.2,2.9,5.2,1.6); arr(6.0,2.9,6.4,1.6); arr(10.6,2.9,8.0,1.6)
ax.text(6.5,9.95,"Structure–Property Logic of Argyrodite SEs",ha='center',fontsize=14,fontweight='bold')
plt.tight_layout(); plt.savefig("/tmp/structure_property_logic.png",dpi=190,bbox_inches='tight'); print("ok")
