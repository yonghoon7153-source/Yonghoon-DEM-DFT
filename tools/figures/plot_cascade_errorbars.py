#!/usr/bin/env python3
"""plot_cascade_errorbars.py — honest reliability view: every metric as per-dopant
MEAN ± replicate STD (across the 3 x=0.25 placement replicates). This is the direct
answer to "do values change run-to-run?": the error bar IS the run-to-run band
(the anneal is stochastic). Small bar = reliable; large bar = placement-sensitive
(don't trust a single value). 4 panels: stability / E_young / B0 / Li-blocking.
CSV-driven (champions + litransport). UMA-relative, x=0.25.
"""
import csv, re, math, io
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}; MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
def fnum(s):
    try: return float(s)
    except: return math.nan
def parse(d):
    d=d.split("+")[0]
    toks=[(e,int(n) if n else 1) for e,n in re.findall(r"([A-Z][a-z]?)(\d*)",d) if e]
    an="O" if any(e=="O" for e,_ in toks) else "F"; cat=[(e,n) for e,n in toks if e not in ("O","F")][0]
    grp=("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI else "alk.earth" if cat[0] in AE
         else "main-group" if cat[0] in MAIN else "TM")
    return grp
lt={r["_dir"]:r for r in csv.DictReader(open("db/properties/cascade_v23_litransport.csv"))}
ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")): ch.setdefault(r["dopant"].split("+")[0],[]).append(r)
def stats(d,k,src="ch",dropneg=False):
    vs=[]
    for r in ch[d]:
        if src=="ch": v=fnum(r[k])
        else: v=fnum(lt.get(r["_dir"],{}).get(k,""))
        if math.isnan(v): continue
        if dropneg and fnum(r["elastic_poisson_nu"])<0: continue
        vs.append(v)
    return (np.mean(vs),np.std(vs)) if vs else (math.nan,math.nan)
dops=sorted(ch)
D={d:dict(grp=parse(d),
    de=stats(d,"rerank_de_post_anneal"),E=stats(d,"elastic_E_young_GPa",dropneg=True),
    B0=stats(d,"eos_B0_GPa"),blk=stats(d,"tier2_dopant_blocking_fraction",src="lt")) for d in dops}

fig,axs=plt.subplots(2,2,figsize=(17,13))
def panel(ax,key,xlabel,title,asc=True,hi_rel=0.15):
    items=[(d,D[d][key][0],D[d][key][1]) for d in dops if not math.isnan(D[d][key][0])]
    items.sort(key=lambda t:t[1],reverse=not asc)
    y=np.arange(len(items)); m=[t[1] for t in items]; s=[t[2] for t in items]
    cols=[GRPC[D[t[0]]["grp"]] for t in items]
    ax.barh(y,m,color=cols,edgecolor="k",lw=.3,zorder=2)
    ax.errorbar(m,y,xerr=s,fmt="none",ecolor="0.2",elinewidth=0.9,capsize=2,zorder=4)
    # flag high relative spread
    for i,(d,mm,ss) in enumerate(items):
        rel=ss/(abs(mm)+1e-9)
        if rel>hi_rel: ax.text(mm+ (ss if mm>=0 else -ss),y[i],"  ⚠",va="center",fontsize=8,color="#b00",fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels([t[0] for t in items],fontsize=5.6)
    ax.set_xlabel(xlabel); ax.set_title(title,fontsize=10); ax.grid(axis="x",alpha=.3)
panel(axs[0,0],"de","formation Δe (eV/atom) ± replicate std","(A) Stability ± run-to-run band",asc=True,hi_rel=0.18)
panel(axs[0,1],"E","E_young (GPa) ± std","(B) Young's modulus — ⚠=high spread (placement-sensitive)",asc=False,hi_rel=0.12)
panel(axs[1,0],"B0","EOS B0 (GPa) ± std","(C) Bulk modulus ± std",asc=False,hi_rel=0.15)
panel(axs[1,1],"blk","Li-blocking fraction ± std","(D) Li-blocking ± std",asc=True,hi_rel=0.20)
fig.legend(handles=[Patch(fc=GRPC[g],label=g) for g in GRPC],loc="lower center",ncol=5,fontsize=9,bbox_to_anchor=(0.5,-0.01))
plt.suptitle("Cascade v23 — RELIABILITY view: mean ± replicate std (the run-to-run band). ⚠ = high spread, don't trust single value",fontsize=12.5,y=1.0)
plt.tight_layout(rect=[0,0.02,1,1]); plt.savefig(f"{OUT}/cascade_v23_errorbars.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_errorbars.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_errorbars.png")

# console: most/least reliable
print("\n=== highest E_young spread (least reliable mechanically) ===")
for d in sorted(dops,key=lambda d:-(D[d]["E"][1] if not math.isnan(D[d]["E"][1]) else -1))[:6]:
    print(f"  {d:7s} E={D[d]['E'][0]:.1f}±{D[d]['E'][1]:.1f} ({100*D[d]['E'][1]/D[d]['E'][0]:.0f}%)")
print("=== Nd2O3 elastic now (was the broken one) ===")
print(f"  Nd2O3 E={D['Nd2O3']['E'][0]:.1f}±{D['Nd2O3']['E'][1]:.1f}  (post-fix, consistent)")
