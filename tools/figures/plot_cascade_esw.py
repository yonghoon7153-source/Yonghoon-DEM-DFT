#!/usr/bin/env python3
"""plot_cascade_esw.py — grand-potential ESW (oxidation/reduction window) per
cascade dopant, from esw_cascade_batch.py (gabia, MP GGA_GGA+U). Per-dopant PLAIN
variant; +Cl-rich shifts noted separately. Writes CSV + window-bar figure.
Cross-check: Nd2O3 ox=1.92 matches our dedicated nd ESW (oxidation_stability.json).
"""
import re, math, os, csv
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUT = "docs/figures/cascade"; os.makedirs(OUT, exist_ok=True)
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}
MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
# dopant: (ox_V, red_V, ocv_V, win_V) — PLAIN variant
ESW = {
"Ag2O":(2.14,1.723,1.914,0.417),"Al2O3":(2.14,1.372,1.717,0.768),"AlF3":(2.14,1.372,1.717,0.768),
"B2O3":(2.317,2.043,2.091,0.274),"BaO":(2.071,1.717,1.938,0.354),"CaF2":(2.14,1.242,1.717,0.898),
"CaO":(2.14,1.242,1.717,0.898),"CoO":(1.873,1.861,None,0.012),"Cr2O3":(2.356,1.723,1.729,0.633),
"CrO3":(2.14,1.729,None,0.411),"Cu2O":(1.864,1.751,1.757,0.113),"Fe2O3":(1.808,1.804,None,0.004),
"Ga2O3":(2.356,1.578,1.717,0.778),"Gd2O3":(2.118,1.398,1.717,0.72),"GeO2":(2.14,1.622,1.717,0.518),
"HfO2":(1.996,1.242,1.717,0.754),"In2O3":(2.356,1.565,1.717,0.791),"La2O3":(1.893,1.523,1.717,0.37),
"LaF3":(1.893,1.475,1.717,0.418),"Li2O":(2.14,1.242,1.717,0.898),"LiF":(2.14,1.242,1.717,0.898),
"MgF2":(2.14,1.343,1.717,0.797),"MgO":(2.14,1.405,1.717,0.735),"MnO":(1.794,1.755,None,0.039),
"MoO3":(2.14,1.726,None,0.414),"Na2O":(2.06,1.717,1.721,0.343),"Nb2O5":(2.061,1.738,None,0.323),
"Nd2O3":(1.92,1.518,1.717,0.402),"NdF3":(1.92,1.518,1.717,0.402),"NiO":(1.838,1.816,None,0.022),
"Sb2O5":(2.14,1.777,1.957,0.363),"Sc2O3":(2.356,1.386,1.717,0.97),"ScF3":(2.14,1.306,1.717,0.834),
"SiO2":(2.14,1.414,1.717,0.726),"Sm2O3":(1.989,1.488,1.717,0.501),"SnO2":(2.14,1.717,1.72,0.423),
"SrO":(2.06,1.717,1.917,0.343),"Ta2O5":(2.027,1.717,None,0.31),"TiF4":(2.024,1.717,1.942,0.307),
"TiO2":(2.024,1.717,1.942,0.307),"V2O5":(2.042,1.736,1.791,0.306),"WO3":(2.14,1.717,None,0.423),
"Y2O3":(2.282,1.391,1.717,0.891),"YF3":(2.14,1.292,1.717,0.848),"ZnO":(2.14,1.565,1.717,0.575),
"ZrF4":(1.878,1.713,1.717,0.165),"ZrO2":(1.878,1.713,1.717,0.165),
}
# +Cl-rich variant pushes oxidation onset UP (more LiCl buffer, S diluted)
CLRICH_OX = {"Al2O3":2.354,"MoO3":2.356,"WO3":2.356}  # plain ox -> clrich ox

def parse(d):
    toks=[(e,int(n) if n else 1) for e,n in re.findall(r"([A-Z][a-z]?)(\d*)",d) if e]
    anion="O" if any(e=="O" for e,_ in toks) else "F"
    cat=[(e,n) for e,n in toks if e not in ("O","F")][0]
    av=2 if anion=="O" else 1; bn=[n for e,n in toks if e==anion][0]; val=round(av*bn/cat[1])
    grp=("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI
         else "alk.earth" if cat[0] in AE else "main-group" if cat[0] in MAIN else "TM")
    return cat[0],anion,val,grp
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}

# ---- write CSV ----
with open("db/properties/oxidation_stability_cascade.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["# grand-potential ESW per cascade dopant (UMA champion composition, MP GGA_GGA+U hull).",
                "esw_cascade_batch.py @ gabia. PLAIN variant; clrich_ox = +Cl-rich oxidation onset (higher)."])
    w.writerow(["# ref undoped: comp1/modelc ox=2.14 red=1.24 ocv=1.72 ; nd ox=1.92 (matches Nd2O3 here)."])
    w.writerow(["dopant","anion","valence","group","ox_V","red_V","ocv_V","window_V","clrich_ox_V"])
    for d in sorted(ESW):
        ox,red,ocv,win=ESW[d]; cat,an,val,grp=parse(d)
        w.writerow([d,an,val,grp,ox,red,ocv if ocv else "",win,CLRICH_OX.get(d,"")])
print("saved db/properties/oxidation_stability_cascade.csv")

# ================= figure =================
fig,axs=plt.subplots(1,2,figsize=(16,11),gridspec_kw={"width_ratios":[2.2,1]})
# (A) window bars sorted by ox_V
order=sorted(ESW,key=lambda d:(ESW[d][0],ESW[d][3]))
ax=axs[0]; y=np.arange(len(order))
for i,d in enumerate(order):
    ox,red,ocv,win=ESW[d]; cat,an,val,grp=parse(d)
    ax.plot([red,ox],[i,i],color=GRPC[grp],lw=5,solid_capstyle="round",zorder=3)
    ax.plot(ox,i,">",color=GRPC[grp],ms=7,zorder=4)
    if d in CLRICH_OX:  # show clrich oxidation boost
        ax.plot([ox,CLRICH_OX[d]],[i,i],color=GRPC[grp],lw=1.5,ls=":",zorder=2)
        ax.plot(CLRICH_OX[d],i,">",mfc="none",mec=GRPC[grp],ms=7,zorder=4)
    if win<0.05: ax.plot(ox,i,"x",color="red",ms=9,mew=2,zorder=5)  # collapsed window
ax.axvline(2.14,ls="--",color="0.4",lw=1.2); ax.text(2.14,len(order),"undoped ox 2.14",fontsize=8,color="0.4",va="bottom",ha="center")
ax.axvline(1.24,ls=":",color="0.6",lw=1); ax.text(1.24,len(order),"undoped red 1.24",fontsize=7.5,color="0.6",va="bottom",ha="center")
ax.set_yticks(y); ax.set_yticklabels(order,fontsize=6.5)
ax.set_xlabel("V vs Li/Li$^+$  (bar = stable window [red→ox]; dotted = +Cl-rich ox boost)")
ax.set_title("(A) Grand-potential stability window per dopant (sorted by ox onset)\n"
             "red × = collapsed window (M-redox eats it: Fe/Co/Ni/Mn)",fontsize=10)
ax.legend(handles=[Patch(fc=GRPC[g],label=g) for g in GRPC],fontsize=8,loc="lower right"); ax.grid(axis="x",alpha=.3)
ax.set_xlim(1.1,2.5)

# (B) ox_V by group
ax=axs[1]
grps=["main-group","TM","lanthanide","alk.earth","alkali"]
for i,g in enumerate(grps):
    ox=[ESW[d][0] for d in ESW if parse(d)[3]==g]
    ax.scatter(np.random.default_rng(i).normal(i,0.08,len(ox)),ox,c=GRPC[g],s=40,edgecolor="white",lw=.5)
    ax.plot([i-.25,i+.25],[np.mean(ox)]*2,color="k",lw=2,zorder=5)
ax.axhline(2.14,ls="--",color="0.4",lw=1)
ax.set_xticks(range(len(grps))); ax.set_xticklabels(grps,rotation=30,ha="right",fontsize=8)
ax.set_ylabel("oxidation onset V (vs Li/Li$^+$)")
ax.set_title("(B) Oxidation onset by cation group\nmain-group/early-TM push it up; late-TM collapse it",fontsize=10)
ax.grid(axis="y",alpha=.3)

plt.suptitle("Cascade v23 — grand-potential oxidation stability of doped LPSCl (47 dopants, MP GGA_GGA+U)",fontsize=13,y=1.0)
plt.tight_layout()
plt.savefig(f"{OUT}/cascade_v23_esw.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_esw.pdf",bbox_inches="tight")
print(f"saved {OUT}/cascade_v23_esw.png")

# console highlights
print("\n=== widest ox onset (oxidatively stable) ===")
for d in sorted(ESW,key=lambda d:-ESW[d][0])[:8]: print(f"  {d:7s} ox={ESW[d][0]} win={ESW[d][3]} ({parse(d)[3]})")
print("=== collapsed window (avoid) ===")
for d in sorted(ESW,key=lambda d:ESW[d][3])[:6]: print(f"  {d:7s} win={ESW[d][3]} ox={ESW[d][0]} red={ESW[d][1]} ({parse(d)[3]})")
print(f"\n+Cl-rich ox boost: " + ", ".join(f"{d} {ESW[d][0]}->{CLRICH_OX[d]}" for d in CLRICH_OX))
