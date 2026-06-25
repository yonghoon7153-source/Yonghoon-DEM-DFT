#!/usr/bin/env python3
"""plot_cascade_branches.py — explore the creative 'other branches':
 (A) TRADE-OFF ESCAPERS: residual of blocking~stability regression -> dopants that
     block Li LESS than their stability predicts = bulk-dopant hidden gems (HfO2-like).
 (B) DUAL-SUBLATTICE co-doping: P-site dopant ⊕ Li-site dopant -> no site competition
     (different sublattices) -> clean co-solubility; rank by combined stability+ox.
 (C) STABILIZER ⊕ CONDUCTOR co-doping: high-ox blocker ⊕ low-block conductor ->
     keep stability/oxidation while recovering Li mobility.
 (D) Bulk sweet-spot map (stability vs blocking) with escapers highlighted.
All single-dopant proxy HYPOTHESES (co-doping needs explicit DFT). CSV-driven.
"""
import csv, re, math, io
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

lt={r["_dir"]:r for r in csv.DictReader(open("db/properties/cascade_v23_litransport.csv"))}
ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")): ch.setdefault(r["dopant"].split("+")[0],[]).append(r)
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
    cat,an,val,grp=parse(d); ox,red=esw[d]; dirs=[r["_dir"] for r in ch[d]]
    blk=[fnum(lt[x]["tier2_dopant_blocking_fraction"]) for x in dirs if x in lt and lt[x]["tier2_dopant_blocking_fraction"]]
    cs=Counter(lt[x]["cation_site"] for x in dirs if x in lt).most_common(1)
    D.append(dict(dop=d,cat=cat,an=an,val=val,grp=grp,ox=ox,red=red,de=agg(d,"rerank_de_post_anneal"),
        E=agg(d,"elastic_E_young_GPa",True),blk=np.mean(blk) if blk else math.nan,csite=cs[0][0] if cs else "?"))
D=[x for x in D if not math.isnan(x["de"]) and not math.isnan(x["blk"])]

# (A) escaper residual: predict blk from de; residual<0 = blocks less than predicted
de=np.array([x["de"] for x in D]); blk=np.array([x["blk"] for x in D])
b=np.polyfit(de,blk,1); pred=np.polyval(b,de)
for i,x in enumerate(D): x["resid"]=blk[i]-pred[i]   # negative = escaper (low block for its stability)

fig=plt.figure(figsize=(18,12))
ax=fig.add_subplot(2,2,1)
esc=sorted(D,key=lambda x:x["resid"])[:16]
y=np.arange(len(esc))[::-1]
ax.barh(y,[x["resid"] for x in esc],color=[SITEC.get(x["csite"],"0.6") for x in esc],edgecolor="k",lw=.3)
ax.set_yticks(y);ax.set_yticklabels([f"{x['dop']} (de{x['de']:+.2f})" for x in esc],fontsize=6.5)
ax.set_xlabel("blocking residual (negative = blocks LESS than its stability predicts = bulk gem)")
ax.set_title("(A) Trade-off ESCAPERS — stable AND low-blocking (bulk-dopant gems)",fontsize=10)
ax.legend(handles=[Patch(fc=SITEC[s],label=s) for s in SITEC],fontsize=7.5,loc="lower left"); ax.grid(axis="x",alpha=.3)

# (B) dual-sublattice: P-site x Li-site (no site competition)
Psite=[x for x in D if x["csite"]=="P_4b"]; Lisite=[x for x in D if x["csite"].startswith("Li")]
pairsB=[]
for p in Psite:
    for l in Lisite:
        stab=-(p["de"]+l["de"])/2; oxc=max(p["ox"],l["ox"]); score=stab+0.3*(oxc-2.0)
        pairsB.append((p,l,score,stab,oxc))
pairsB.sort(key=lambda t:-t[2])
ax=fig.add_subplot(2,2,2)
top=pairsB[:12]; y=np.arange(len(top))[::-1]
ax.barh(y,[t[2] for t in top],color="#8e44ad",edgecolor="k",lw=.3)
for i,t in enumerate(top): ax.text(0.01,y[i],f"{t[0]['dop']}(P)⊕{t[1]['dop']}(Li)  stab{t[3]:.2f} ox{t[4]:.2f}",va="center",fontsize=7)
ax.set_yticks([]);ax.set_xlabel("dual-sublattice score (avg stability + ox coverage)")
ax.set_title("(B) DUAL-SUBLATTICE co-doping (P-site ⊕ Li-site, no site competition)",fontsize=10); ax.grid(axis="x",alpha=.3)

# (C) stabilizer + conductor (mobility-complementary)
pairsC=[]
for i in range(len(D)):
    for j in range(i+1,len(D)):
        a,c=D[i],D[j]
        # one high-ox stabilizer (blocks), one low-block conductor
        if not ((a["ox"]>2.2 and c["blk"]<0.45) or (c["ox"]>2.2 and a["blk"]<0.45)): continue
        oxc=max(a["ox"],c["ox"]); avgblk=(a["blk"]+c["blk"])/2; stab=-(a["de"]+c["de"])/2
        score=0.4*(oxc-2.0)/0.36+0.35*(1-avgblk)+0.25*max(0,(stab-0.5)/0.5)
        pairsC.append((a,c,score,oxc,avgblk))
pairsC.sort(key=lambda t:-t[2])
ax=fig.add_subplot(2,2,3)
top=pairsC[:12]; y=np.arange(len(top))[::-1]
ax.barh(y,[t[2] for t in top],color="#16a085",edgecolor="k",lw=.3)
for i,t in enumerate(top):
    s=t[0] if t[0]["ox"]>t[1]["ox"] else t[1]; cnd=t[1] if t[0]["ox"]>t[1]["ox"] else t[0]
    ax.text(0.01,y[i],f"{s['dop']}(ox{s['ox']:.2f})⊕{cnd['dop']}(blk{cnd['blk']:.2f})",va="center",fontsize=7)
ax.set_yticks([]);ax.set_xlabel("score (oxidation + low avg-block + stability)")
ax.set_title("(C) STABILIZER ⊕ CONDUCTOR co-doping (keep ox, recover σ_Li)",fontsize=10); ax.grid(axis="x",alpha=.3)

# (D) bulk sweet-spot map
ax=fig.add_subplot(2,2,4)
xf=np.linspace(de.min(),de.max(),40); ax.plot(xf,np.polyval(b,xf),"k--",lw=1.2,alpha=.6,label="trade-off line")
for x in D:
    esc_f = x["resid"]<-0.08
    ax.scatter(x["de"],x["blk"],c=GRPC[x["grp"]],s=55 if esc_f else 38,
               edgecolor=("#15a01a" if esc_f else "white"),lw=(2 if esc_f else .5),zorder=3)
    if esc_f or x["dop"] in ("Gd2O3","V2O5","Cr2O3"):
        ax.annotate(x["dop"],(x["de"],x["blk"]),fontsize=6.8,xytext=(3,2),textcoords="offset points")
ax.invert_xaxis()
ax.set_xlabel("formation Δe (← more stable)"); ax.set_ylabel("Li-blocking (↓ better conductivity)")
ax.set_title("(D) Bulk sweet-spot — green ring = escaper (stable + low-block)\nideal bulk dopant = lower-left, below the line",fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=.3)

plt.suptitle("Cascade v23 — creative branches (escapers · dual-sublattice · stabilizer⊕conductor)",fontsize=12.5,y=1.0)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_branches.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_branches.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_branches.png")

print("\n=== (A) trade-off ESCAPERS (stable + low-block bulk gems) ===")
for x in esc[:8]: print(f"  {x['dop']:7s} resid={x['resid']:+.2f} de={x['de']:+.2f} blk={x['blk']:.2f} ox={x['ox']} site={x['csite']} ({x['grp']})")
print("\n=== (B) dual-sublattice (P⊕Li) top-6 ===")
for t in pairsB[:6]: print(f"  {t[0]['dop']:6s}(P) ⊕ {t[1]['dop']:6s}(Li)  stab={t[3]:.2f} ox={t[4]:.2f}")
print("\n=== (C) stabilizer⊕conductor top-6 ===")
for t in pairsC[:6]:
    s=t[0] if t[0]['ox']>t[1]['ox'] else t[1]; cnd=t[1] if t[0]['ox']>t[1]['ox'] else t[0]
    print(f"  {s['dop']:6s}(ox{s['ox']:.2f},blk{s['blk']:.2f}) ⊕ {cnd['dop']:6s}(blk{cnd['blk']:.2f})  avgblk={t[4]:.2f}")
