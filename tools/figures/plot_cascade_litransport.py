#!/usr/bin/env python3
"""plot_cascade_litransport.py — the missing Li-mobility dimension + site
preference. blocking_fraction (Li-channel blocking; high=worse sigma), migration
volume, BVS proxy, and cation/anion site. Key story: (1) site preference =
doping mechanism (valence>=4 -> P_4b substitute P5+; <=3 -> Li site), (2)
STABILITY <-> MOBILITY trade-off (stabilizing high-valence dopants block Li more),
(3) TRUE 4-objective score (stable+oxidation+soft+Li-mobile). CSV-driven.
"""
import csv, re, math, os, io
import numpy as np
from collections import Counter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}; MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
SITEC={"P_4b":"#c0392b","Li_24g":"#2980b9","Li_48h":"#27ae60"}
def fnum(s):
    try: return float(s)
    except: return math.nan
def parse(d):
    d=d.split("+")[0]
    toks=[(e,int(n) if n else 1) for e,n in re.findall(r"([A-Z][a-z]?)(\d*)",d) if e]
    an="O" if any(e=="O" for e,_ in toks) else "F"
    cat=[(e,n) for e,n in toks if e not in ("O","F")][0]
    av=2 if an=="O" else 1; bn=[n for e,n in toks if e==an][0]; val=round(av*bn/cat[1])
    grp=("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI else "alk.earth" if cat[0] in AE
         else "main-group" if cat[0] in MAIN else "TM")
    return cat[0],an,val,grp

# litransport per _dir -> per dopant
lt={}
for r in csv.DictReader(open("db/properties/cascade_v23_litransport.csv")):
    lt[r["_dir"]]=r
# champions for de/E
ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")):
    ch.setdefault(r["dopant"].split("+")[0],[]).append(r)
esw={}
_raw=open("db/properties/oxidation_stability_cascade.csv").read().splitlines()
_h=next(i for i,l in enumerate(_raw) if l.startswith("dopant,"))
for r in csv.DictReader(io.StringIO("\n".join(_raw[_h:]))): esw[r["dopant"]]=(fnum(r["ox_V"]),fnum(r["red_V"]))
def agg(d,k,dn=False):
    vs=[fnum(r[k]) for r in ch[d] if not math.isnan(fnum(r[k])) and not(dn and fnum(r["elastic_poisson_nu"])<0)]
    return np.mean(vs) if vs else math.nan
D=[]
for d in ch:
    if d not in esw: continue
    cat,an,val,grp=parse(d); ox,red=esw[d]
    dirs=[r["_dir"] for r in ch[d]]
    blk=[fnum(lt[x]["tier2_dopant_blocking_fraction"]) for x in dirs if x in lt and lt[x]["tier2_dopant_blocking_fraction"]]
    mig=[fnum(lt[x]["migration_volume_fraction"]) for x in dirs if x in lt and lt[x]["migration_volume_fraction"]]
    csite=Counter(lt[x]["cation_site"] for x in dirs if x in lt).most_common(1)
    asite=Counter(lt[x]["anion_site"] for x in dirs if x in lt).most_common(1)
    D.append(dict(dop=d,cat=cat,an=an,val=val,grp=grp,ox=ox,red=red,
        de=agg(d,"rerank_de_post_anneal"),E=agg(d,"elastic_E_young_GPa",True),
        blk=np.mean(blk) if blk else math.nan,mig=np.mean(mig) if mig else math.nan,
        csite=csite[0][0] if csite else "?",asite=asite[0][0] if asite else "?"))
D=[x for x in D if not math.isnan(x["de"])]

fig=plt.figure(figsize=(18,12))
# (A) blocking ranking
ax=fig.add_subplot(2,2,1)
order=sorted([x for x in D if not math.isnan(x["blk"])],key=lambda x:x["blk"])
y=np.arange(len(order))
ax.barh(y,[x["blk"] for x in order],color=[SITEC.get(x["csite"],"0.6") for x in order],edgecolor="k",lw=.3)
ax.set_yticks(y);ax.set_yticklabels([x["dop"] for x in order],fontsize=5.5)
ax.set_xlabel("dopant Li-channel blocking fraction (← low = preserves σ_Li)")
ax.set_title("(A) Li-blocking ranking — low=good conductor. color=cation site",fontsize=10)
ax.legend(handles=[Patch(fc=SITEC[s],label=s) for s in SITEC],fontsize=8,loc="lower right"); ax.grid(axis="x",alpha=.3)

# (B) STABILITY <-> MOBILITY trade-off
ax=fig.add_subplot(2,2,2)
xs=[x["blk"] for x in D if not math.isnan(x["blk"])]; ys=[x["de"] for x in D if not math.isnan(x["blk"])]
for x in D:
    if math.isnan(x["blk"]): continue
    ax.scatter(x["blk"],x["de"],c=GRPC[x["grp"]],s=44,edgecolor="white",lw=.5,zorder=3)
for d in ("Gd2O3","Sc2O3","Ta2O5","V2O5","Li2O","HfO2","SrO","Cr2O3"):
    x=next((z for z in D if z["dop"]==d),None)
    if x and not math.isnan(x["blk"]): ax.annotate(d,(x["blk"],x["de"]),fontsize=7,xytext=(3,2),textcoords="offset points")
r=np.corrcoef(xs,ys)[0,1]; b=np.polyfit(xs,ys,1); xf=np.linspace(min(xs),max(xs),40)
ax.plot(xf,np.polyval(b,xf),"k--",lw=1,alpha=.6); ax.text(.04,.06,f"r={r:+.2f}",transform=ax.transAxes,fontsize=11,fontweight="bold")
ax.invert_yaxis()
ax.set_xlabel("Li-blocking fraction (→ worse conductivity)"); ax.set_ylabel("formation Δe (↓ more stable)")
ax.set_title("(B) ★ Stability ↔ Mobility TRADE-OFF\nmost-stabilizing dopants block Li most (lower-right tension); HfO2 escapes it",fontsize=10)
ax.grid(alpha=.3)

# (C) site preference = doping mechanism
ax=fig.add_subplot(2,2,3)
vals=sorted(set(x["val"] for x in D))
sites=["Li_24g","Li_48h","P_4b"]
bottom=np.zeros(len(vals))
for s in sites:
    cnt=[sum(1 for x in D if x["val"]==v and x["csite"]==s) for v in vals]
    ax.bar([str(v) for v in vals],cnt,bottom=bottom,color=SITEC[s],label=s,edgecolor="white")
    bottom+=cnt
ax.set_xlabel("cation valence"); ax.set_ylabel("# dopants")
ax.set_title("(C) Site preference = doping mechanism\nvalence≥4 → P_4b (substitute P⁵⁺); ≤3 → Li site",fontsize=10)
ax.legend(fontsize=8)

# (D) 4-objective final score
ax=fig.add_subplot(2,2,4); ax.axis("off")
def nrm(key,hi=True):
    v=np.array([x[key] for x in D],float); v=np.where(np.isnan(v),np.nanmean(v),v)
    z=(v-v.min())/(v.max()-v.min()+1e-9); return z if hi else 1-z
score=0.30*nrm("de",False)+0.25*nrm("ox")+0.25*nrm("blk",False)+0.20*nrm("E",False)
for i,x in enumerate(D): x["score4"]=score[i]
top=sorted(D,key=lambda x:-x["score4"])[:14]
txt="4-objective score = 0.30 stable + 0.25 oxidation + 0.25 Li-mobile(low-block) + 0.20 soft\n\n"
txt+=f"{'rank dopant':16s}{'score':>6s}  {'de':>6s}{'ox':>6s}{'blk':>6s}{'E':>5s}  site\n"
for i,x in enumerate(top,1):
    txt+=f"{i:2d}  {x['dop']:9s}{x['score4']:6.2f}  {x['de']:+6.2f}{x['ox']:6.2f}{x['blk']:6.2f}{x['E']:5.0f}  {x['csite']}\n"
ax.text(0,1,txt,va="top",ha="left",fontsize=8.4,family="monospace")
ax.set_title("(D) TRUE 4-objective ranking (now incl. Li-mobility)",fontsize=10,loc="left")

plt.suptitle("Cascade v23 — Li-mobility + site preference (the SE-critical dimension)",fontsize=13,y=1.0)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_litransport.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_litransport.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_litransport.png")

print("\n=== lowest blocking (best for σ_Li) ===")
for x in sorted([z for z in D if not math.isnan(z["blk"])],key=lambda z:z["blk"])[:8]:
    print(f"  {x['dop']:7s} blk={x['blk']:.2f} de={x['de']:+.2f} ox={x['ox']} site={x['csite']} ({x['grp']})")
print("=== highest blocking (kills σ_Li) ===")
for x in sorted([z for z in D if not math.isnan(z["blk"])],key=lambda z:-z["blk"])[:6]:
    print(f"  {x['dop']:7s} blk={x['blk']:.2f} de={x['de']:+.2f} site={x['csite']}")
print(f"\nblocking-vs-stability r = {r:+.2f}  (negative de = stable; positive r => stable dopants block more)")
print("P_4b (P-site) dopants:",", ".join(sorted(x["dop"] for x in D if x["csite"]=="P_4b")))
print("\n=== 4-objective top-8 (incl Li-mobility) ===")
for x in sorted(D,key=lambda x:-x["score4"])[:8]: print(f"  {x['dop']:7s} {x['score4']:.2f}  de{x['de']:+.2f} ox{x['ox']} blk{x['blk']:.2f} E{x['E']:.0f} {x['csite']}")
