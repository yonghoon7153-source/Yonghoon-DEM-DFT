#!/usr/bin/env python3
"""plot_cascade_synergy.py — CO-DOPING synergy HYPOTHESIS screen from single-dopant
data. Idea: a pair (A,B) is synergistic if it covers each other's weaknesses.
Primary metric = anode-cathode complementarity: one dopant guards the cathode
(high oxidation onset), the other guards the anode (low reduction limit), so the
mixed cell's effective window > either alone. Weighted by radius match (co-
solubility) and joint stability; antagonists (window-collapsing late-TM) score low.
4 panels + ranked CSV. UMA-relative, x=0.25.

*** HYPOTHESIS GENERATOR — NOT validated. Single-dopant proxy: assumes each
dopant's decomposition product dominates at its favorable electrode, the two
co-dissolve (radius match), and no chemical antagonism. Needs explicit co-doped
DFT to confirm. ***
"""
import csv, re, math, os, io
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}; MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
RAD={"Li":0.76,"Na":1.02,"Ag":1.15,"Mg":0.72,"Ca":1.00,"Sr":1.18,"Ba":1.35,"Mn":0.83,"Co":0.745,
"Ni":0.69,"Zn":0.74,"Al":0.535,"Ga":0.62,"In":0.80,"Sc":0.745,"Y":0.90,"Fe":0.645,"B":0.27,
"La":1.032,"Nd":0.983,"Sm":0.958,"Gd":0.938,"Ti":0.605,"Zr":0.72,"Hf":0.71,"Si":0.40,"Ge":0.53,
"Sn":0.69,"Nb":0.64,"Ta":0.64,"V":0.54,"Sb":0.60,"Cr":0.615,"Mo":0.59,"W":0.60,"Cu":0.77}
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

ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")):
    ch.setdefault(r["dopant"].split("+")[0],[]).append(r)
def agg(d,k,dn=False):
    vs=[fnum(r[k]) for r in ch[d] if not math.isnan(fnum(r[k])) and not(dn and fnum(r["elastic_poisson_nu"])<0)]
    return np.mean(vs) if vs else math.nan
esw={}
_raw=open("db/properties/oxidation_stability_cascade.csv").read().splitlines()
_h=next(i for i,l in enumerate(_raw) if l.startswith("dopant,"))
for r in csv.DictReader(io.StringIO("\n".join(_raw[_h:]))): esw[r["dopant"]]=(fnum(r["ox_V"]),fnum(r["red_V"]))
D=[]
for d in ch:
    if d not in esw: continue
    cat,an,val,grp=parse(d); ox,red=esw[d]
    D.append(dict(dop=d,cat=cat,an=an,grp=grp,ox=ox,red=red,win=ox-red,de=agg(d,"rerank_de_post_anneal"),
                  E=agg(d,"elastic_E_young_GPa",True),rad=RAD.get(cat,math.nan)))
D=[x for x in D if not math.isnan(x["de"])]
N=len(D)

# ---- pairwise synergy ----
def rmatch(a,b):
    if math.isnan(a["rad"]) or math.isnan(b["rad"]): return 0.5
    return math.exp(-((a["rad"]-b["rad"])/0.25)**2)
pairs=[]
for i in range(N):
    for j in range(i+1,N):
        a,b=D[i],D[j]
        jwin=max(a["ox"],b["ox"])-min(a["red"],b["red"])      # joint window (best edge each)
        gain=jwin-max(a["win"],b["win"])                       # widening vs best single
        rm=rmatch(a,b); stab=-(a["de"]+b["de"])/2
        sgate=min(1.0,max(0.0,(stab-0.5)/0.4))                 # need both ~stable
        syn=max(gain,0)*rm*sgate
        tags=[]
        if (a["ox"]>2.2 and b["red"]<1.45) or (b["ox"]>2.2 and a["red"]<1.45): tags.append("anode↔cathode")
        if a["an"]!=b["an"]: tags.append("oxyfluoride")
        if not math.isnan(a["E"]) and not math.isnan(b["E"]) and abs(a["E"]-b["E"])>15: tags.append("hard↔soft")
        if rm>0.8: tags.append("radius-match")
        pairs.append(dict(a=a,b=b,jwin=jwin,gain=gain,rm=rm,stab=stab,syn=syn,tags=tags))
pairs.sort(key=lambda p:-p["syn"])

fig=plt.figure(figsize=(18,12))
# (A) anode-cathode complementarity map with top pair links
ax=fig.add_subplot(2,2,1)
for x in D:
    ax.scatter(x["red"],x["ox"],c=GRPC[x["grp"]],s=40,edgecolor="white",lw=.5,zorder=3)
for p in pairs[:8]:
    a,b=p["a"],p["b"]
    ax.plot([a["red"],b["red"]],[a["ox"],b["ox"]],"-",color="#444",lw=1.1,alpha=.6,zorder=2)
for d in ("Sc2O3","Cr2O3","CaF2","Li2O","LiF","CaO","Gd2O3","Y2O3","B2O3","ScF3"):
    x=next((z for z in D if z["dop"]==d),None)
    if x: ax.annotate(d,(x["red"],x["ox"]),fontsize=6.5,xytext=(3,2),textcoords="offset points")
ax.axhline(2.14,ls="--",color="0.6",lw=1); ax.axvline(1.24,ls="--",color="0.6",lw=1)
ax.set_xlabel("reduction limit V (← low = anode-guarding partner)")
ax.set_ylabel("oxidation onset V (↑ high = cathode-guarding partner)")
ax.set_title("(A) Anode↔cathode complementarity — lines = top-8 synergy pairs\nideal pair spans low-red + high-ox",fontsize=10)
ax.legend(handles=[Patch(fc=GRPC[g],label=g) for g in GRPC],fontsize=7,loc="lower right"); ax.grid(alpha=.3)

# (B) top-15 synergy pairs
ax=fig.add_subplot(2,2,2)
top=pairs[:15]; y=np.arange(len(top))[::-1]
ax.barh(y,[p["syn"] for p in top],color="#2a9d8f",edgecolor="k",lw=.3)
for i,p in enumerate(top):
    ax.text(0.002,y[i],f"{p['a']['dop']}+{p['b']['dop']}  Δwin{p['gain']:+.2f} r{p['rm']:.2f} [{','.join(p['tags'][:2])}]",
            va="center",fontsize=7)
ax.set_yticks([]); ax.set_xlabel("synergy score (joint-window gain × radius-match × stability)")
ax.set_title("(B) Top-15 co-doping synergy candidates",fontsize=10); ax.grid(axis="x",alpha=.3)

# (C) synergy heatmap among top-16 individually-best dopants
best=sorted(D,key=lambda x:-(x["win"]-0.0)-(-x["de"]))[:16]
bi={x["dop"]:k for k,x in enumerate(best)}; nb=len(best)
H=np.full((nb,nb),np.nan)
for p in pairs:
    if p["a"]["dop"] in bi and p["b"]["dop"] in bi:
        H[bi[p["a"]["dop"]],bi[p["b"]["dop"]]]=p["syn"]; H[bi[p["b"]["dop"]],bi[p["a"]["dop"]]]=p["syn"]
ax=fig.add_subplot(2,2,3)
im=ax.imshow(H,cmap="YlGnBu",vmin=0)
ax.set_xticks(range(nb));ax.set_xticklabels([x["dop"] for x in best],rotation=90,fontsize=6.5)
ax.set_yticks(range(nb));ax.set_yticklabels([x["dop"] for x in best],fontsize=6.5)
plt.colorbar(im,ax=ax,fraction=.046)
ax.set_title("(C) Pairwise synergy among 16 best single dopants",fontsize=10)

# (D) oxyfluoride (O+F) synergy specifically
ax=fig.add_subplot(2,2,4)
of=[p for p in pairs if "oxyfluoride" in p["tags"]][:12]; y=np.arange(len(of))[::-1]
ax.barh(y,[p["syn"] for p in of],color="#e07a2a",edgecolor="k",lw=.3)
for i,p in enumerate(of):
    o=p["a"] if p["a"]["an"]=="O" else p["b"]; f=p["b"] if p["a"]["an"]=="O" else p["a"]
    ax.text(0.002,y[i],f"{o['dop']}(O)+{f['dop']}(F)  Δwin{p['gain']:+.2f}",va="center",fontsize=7)
ax.set_yticks([]); ax.set_xlabel("synergy score")
ax.set_title("(D) Oxyfluoride co-doping (oxide bulk-stability + fluoride LiF-SEI)",fontsize=10); ax.grid(axis="x",alpha=.3)

plt.suptitle("Cascade v23 — CO-DOPING SYNERGY hypotheses (single-dopant proxy; NOT validated — needs co-doped DFT)",fontsize=12.5,y=1.0)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_synergy.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_synergy.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_synergy.png")

with open("db/properties/cascade_v23_synergy_pairs.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["# co-doping synergy HYPOTHESES (single-dopant proxy, NOT validated).",
        "synergy = max(joint_window_gain,0) * radius_match * stability_gate. anode-cathode complementarity."])
    w.writerow(["rank","pairA","pairB","synergy","joint_window_V","gain_vs_best_single","radius_match","avg_stab","tags"])
    for k,p in enumerate(pairs[:40],1):
        w.writerow([k,p["a"]["dop"],p["b"]["dop"],f"{p['syn']:.3f}",f"{p['jwin']:.3f}",f"{p['gain']:+.3f}",
                    f"{p['rm']:.2f}",f"{p['stab']:.2f}","|".join(p["tags"])])
print("saved db/properties/cascade_v23_synergy_pairs.csv")
print("\n=== TOP-12 synergy pairs ===")
for p in pairs[:12]:
    print(f"  {p['a']['dop']:7s}+{p['b']['dop']:7s} syn={p['syn']:.3f} jointwin={p['jwin']:.2f} gain={p['gain']:+.2f} r={p['rm']:.2f} [{','.join(p['tags'])}]")
