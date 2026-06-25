#!/usr/bin/env python3
"""plot_cascade_insights.py — multi-dimensional synthesis of the v23 cascade,
merging stability (de), mechanics (B0/E/G/nu/pugh, recovered-B0 CSV) and
grand-potential oxidation window (ox/red/win). 4 panels:
 (A) cathode-coating map: ox onset vs de, bubble=softness, Pareto front marked
 (B) property correlation heatmap (what moves together)
 (C) composite cathode-coating score, top-15 with stacked contributions
 (D) anode(red_V) vs cathode(ox_V) stability map
Writes a ranked CSV. UMA-vs-UMA relative; x=0.25 champions.
"""
import csv, re, math, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}
MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
def fnum(s):
    try: return float(s)
    except: return math.nan
def parse(d):
    d=d.split("+")[0]
    toks=[(e,int(n) if n else 1) for e,n in re.findall(r"([A-Z][a-z]?)(\d*)",d) if e]
    anion="O" if any(e=="O" for e,_ in toks) else "F"
    cat=[(e,n) for e,n in toks if e not in ("O","F")][0]
    av=2 if anion=="O" else 1; bn=[n for e,n in toks if e==anion][0]; val=round(av*bn/cat[1])
    grp=("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI
         else "alk.earth" if cat[0] in AE else "main-group" if cat[0] in MAIN else "TM")
    return cat[0],anion,val,grp

# ---- merge champions (per-dopant mean) + ESW ----
ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")):
    d=r["dopant"].split("+")[0]; ch.setdefault(d,[]).append(r)
def agg(d,key,drop_nu_neg=False):
    vs=[]
    for r in ch[d]:
        v=fnum(r[key])
        if math.isnan(v): continue
        if drop_nu_neg and fnum(r["elastic_poisson_nu"])<0: continue
        vs.append(v)
    return np.mean(vs) if vs else math.nan
esw={}
import io
_raw=open("db/properties/oxidation_stability_cascade.csv").read().splitlines()
_h=next(i for i,l in enumerate(_raw) if l.startswith("dopant,"))
for r in csv.DictReader(io.StringIO("\n".join(_raw[_h:]))):
    esw[r["dopant"]]=(fnum(r["ox_V"]),fnum(r["red_V"]),fnum(r["window_V"]))

D=[]
for d in ch:
    if d not in esw: continue
    cat,an,val,grp=parse(d)
    ox,red,win=esw[d]
    D.append(dict(dop=d,cat=cat,anion=an,val=val,grp=grp,
        de=agg(d,"rerank_de_post_anneal"),E=agg(d,"elastic_E_young_GPa",True),
        B0=agg(d,"eos_B0_GPa"),G=agg(d,"elastic_G_hill_GPa",True),
        nu=agg(d,"elastic_poisson_nu",True),pugh=agg(d,"elastic_pugh_GoverB",True),
        ox=ox,red=red,win=win))
D=[x for x in D if not math.isnan(x["de"])]

# ---- composite cathode-coating score (transparent min-max norm) ----
def norm(key,better_hi=True):
    v=np.array([x[key] for x in D],float); v=np.where(np.isnan(v),np.nanmean(v),v)
    z=(v-v.min())/(v.max()-v.min()+1e-9); return z if better_hi else 1-z
comp={"ox":(norm("ox",True),0.30),"de":(norm("de",False),0.25),
      "soft":(norm("E",False),0.20),"ductile":(norm("pugh",False),0.15),"win":(norm("win",True),0.10)}
score=np.zeros(len(D))
for k,(z,w) in comp.items(): score+=z*w
for i,x in enumerate(D): x["score"]=score[i]

# ---- Pareto front on (de min, ox max, E min) ----
def dominated(a,b): return (b["de"]<=a["de"] and b["ox"]>=a["ox"] and b["E"]<=a["E"]
                            and (b["de"]<a["de"] or b["ox"]>a["ox"] or b["E"]<a["E"]))
pareto=[a["dop"] for a in D if not any(dominated(a,b) for b in D if b is not a)]

fig=plt.figure(figsize=(18,12))
# (A) coating map
ax=fig.add_subplot(2,2,1)
for x in D:
    s=600/max(x["E"],20)
    ax.scatter(x["ox"],x["de"],s=s*8,c=GRPC[x["grp"]],edgecolor=("red" if x["dop"] in pareto else "white"),
               lw=(1.8 if x["dop"] in pareto else .5),alpha=.85,zorder=3)
    if x["dop"] in pareto or x["dop"] in ("Sc2O3","Gd2O3","Cr2O3","Nd2O3"):
        ax.annotate(x["dop"],(x["ox"],x["de"]),fontsize=7,ha="center",va="bottom",xytext=(0,5),textcoords="offset points")
ax.axvline(2.14,ls="--",color="0.5",lw=1); ax.text(2.145,ax.get_ylim()[1],"undoped ox",fontsize=7,color="0.5",va="top")
ax.set_xlabel("oxidation onset V (→ more oxidatively stable)")
ax.set_ylabel("formation Δe (↓ more stable)"); ax.invert_yaxis()
ax.set_title("(A) Cathode-coating map — ideal = right(ox-stable)+down(stable)+big(soft)\nred ring = Pareto-optimal",fontsize=10)
ax.legend(handles=[Patch(fc=GRPC[g],label=g) for g in GRPC],fontsize=7.5,loc="lower left"); ax.grid(alpha=.3)

# (B) correlation heatmap
ax=fig.add_subplot(2,2,2)
keys=["de","ox","red","win","B0","E","G","nu","pugh"]
M=np.array([[x[k] for k in keys] for x in D],float)
M=np.where(np.isnan(M),np.nanmean(M,axis=0),M)
C=np.corrcoef(M.T)
im=ax.imshow(C,cmap="RdBu_r",vmin=-1,vmax=1)
ax.set_xticks(range(len(keys)));ax.set_xticklabels(keys,rotation=45,ha="right",fontsize=8)
ax.set_yticks(range(len(keys)));ax.set_yticklabels(keys,fontsize=8)
for i in range(len(keys)):
    for j in range(len(keys)):
        ax.text(j,i,f"{C[i,j]:.2f}",ha="center",va="center",fontsize=7,
                color="white" if abs(C[i,j])>0.5 else "black")
plt.colorbar(im,ax=ax,fraction=0.046)
ax.set_title("(B) Property correlations (Pearson r) — what moves together",fontsize=10)

# (C) composite score top-15 stacked
ax=fig.add_subplot(2,2,3)
top=sorted(D,key=lambda x:-x["score"])[:15]
labels=[x["dop"] for x in top]; y=np.arange(len(top))[::-1]
left=np.zeros(len(top))
cc={"ox":"#2a6fb0","de":"#e0541e","soft":"#2a9d8f","ductile":"#9b59b6","win":"#f1c40f"}
for k,(z,w) in comp.items():
    vals=np.array([z[D.index(x)]*w for x in top])
    ax.barh(y,vals,left=left,color=cc[k],label=k,edgecolor="white",lw=.3)
    left+=vals
ax.set_yticks(y);ax.set_yticklabels(labels,fontsize=8)
ax.set_xlabel("composite cathode-coating score (stacked contributions)")
ax.set_title("(C) Top-15 coating candidates (weights: ox.30 de.25 soft.20 duct.15 win.10)",fontsize=10)
ax.legend(fontsize=7.5,ncol=5,loc="lower right"); ax.grid(axis="x",alpha=.3)

# (D) anode vs cathode stability
ax=fig.add_subplot(2,2,4)
for x in D:
    ax.scatter(x["red"],x["ox"],c=GRPC[x["grp"]],s=45,edgecolor="white",lw=.5,zorder=3)
    if x["dop"] in ("Sc2O3","CaF2","Li2O","Fe2O3","CoO","Cr2O3","ScF3","Gd2O3"):
        ax.annotate(x["dop"],(x["red"],x["ox"]),fontsize=7,xytext=(3,2),textcoords="offset points")
ax.axhline(2.14,ls="--",color="0.5",lw=1);ax.axvline(1.24,ls="--",color="0.5",lw=1)
ax.text(1.245,1.83,"←reductively stable",fontsize=7,color="0.5",rotation=90,va="bottom")
ax.set_xlabel("reduction limit V (← lower = better anode side)")
ax.set_ylabel("oxidation onset V (↑ higher = better cathode side)")
ax.set_title("(D) Anode vs cathode stability — late-TM (top-right cluster) bad on both",fontsize=10)
ax.grid(alpha=.3)

plt.suptitle("Cascade v23 — multi-dimensional synthesis (stability × mechanics × oxidation window), 47 dopants",fontsize=13,y=1.0)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_insights.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_insights.pdf",bbox_inches="tight")
print(f"saved {OUT}/cascade_v23_insights.png")

# ranked CSV
with open("db/properties/cascade_v23_ranked.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["# composite cathode-coating ranking. UMA relative. x=0.25.",
        "score=0.30*ox+0.25*stable+0.20*soft+0.15*ductile+0.10*window (min-max norm)."])
    w.writerow(["rank","dopant","group","score","de","ox_V","red_V","E_GPa","pugh","pareto"])
    for i,x in enumerate(sorted(D,key=lambda x:-x["score"]),1):
        w.writerow([i,x["dop"],x["grp"],f"{x['score']:.3f}",f"{x['de']:.3f}",x["ox"],x["red"],
                    f"{x['E']:.1f}",f"{x['pugh']:.2f}","Y" if x["dop"] in pareto else ""])
print("saved db/properties/cascade_v23_ranked.csv")

# insights
print(f"\nPareto-optimal ({len(pareto)}): {', '.join(pareto)}")
print("\nTop-8 composite:")
for x in sorted(D,key=lambda x:-x["score"])[:8]:
    print(f"  {x['dop']:7s} score={x['score']:.3f} de={x['de']:+.2f} ox={x['ox']} E={x['E']:.0f} pugh={x['pugh']:.2f} ({x['grp']})")
print("\nKey correlations:")
for i,a in enumerate(keys):
    for j,b in enumerate(keys):
        if i<j and abs(C[i,j])>0.55: print(f"  {a}-{b}: r={C[i,j]:+.2f}")
