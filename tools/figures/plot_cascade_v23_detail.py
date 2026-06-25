#!/usr/bin/env python3
"""plot_cascade_v23_detail.py — finer-grained breakdowns of the v23 cascade.
6 panels: (A) B0 ranking, (B) cation-group de/E, (C) fluoride vs oxide head-to-head
(same cation), (D) ductility map (Pugh G/B vs E), (E) +Clrich effect, (F) dV vs de.
Source db/properties/cascade_v23_champions.csv. Drops the Nd2O3_x002 elastic
outlier (nu<0) from modulus panels. UMA-vs-UMA relative only.
"""
import csv, re, math, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

CSV = "db/properties/cascade_v23_champions.csv"; OUT = "docs/figures/cascade"
LANTH = {"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}
MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
def fnum(s):
    try: return float(s)
    except: return math.nan
def parse(d):
    base=d.split("+")[0]; clrich="Clrich" in d
    toks=[(e,int(n) if n else 1) for e,n in re.findall(r"([A-Z][a-z]?)(\d*)",base) if e]
    anion="O" if any(e=="O" for e,_ in toks) else "F"
    cat=[(e,n) for e,n in toks if e not in ("O","F")][0]
    av=2 if anion=="O" else 1; bn=[n for e,n in toks if e==anion][0]
    val=round(av*bn/cat[1])
    grp=("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI
         else "alk.earth" if cat[0] in AE else "main-group" if cat[0] in MAIN else "TM")
    return cat[0],anion,val,grp,clrich

rows=[]
for r in csv.DictReader(open(CSV)):
    cat,anion,val,grp,clr=parse(r["dopant"])
    rows.append(dict(dir=r["_dir"],dopant=r["dopant"].split("+")[0],cation=cat,anion=anion,
        valence=val,group=grp,clrich=clr,de=fnum(r["rerank_de_post_anneal"]),
        dV=fnum(r["anneal_dV_pct"]),B0=fnum(r["eos_B0_GPa"]),E=fnum(r["elastic_E_young_GPa"]),
        B=fnum(r["elastic_B_hill_GPa"]),G=fnum(r["elastic_G_hill_GPa"]),
        nu=fnum(r["elastic_poisson_nu"]),pugh=fnum(r["elastic_pugh_GoverB"])))
def ok_el(r): return not math.isnan(r["E"]) and (math.isnan(r["nu"]) or r["nu"]>=0)

ANC={"O":"#2a6fb0","F":"#e08a1e"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
dops=sorted(set(r["dopant"] for r in rows))
def dmean(d,key,filt=lambda r:True):
    v=[r[key] for r in rows if r["dopant"]==d and filt(r) and not math.isnan(r[key])]
    return np.mean(v) if v else math.nan

fig=plt.figure(figsize=(18,11))

# (A) B0 ranking
ax=fig.add_subplot(2,3,1)
b0={d:dmean(d,"B0",lambda r:r["B0"]==r["B0"]) for d in dops}
order=sorted([d for d in dops if not math.isnan(b0[d])],key=lambda d:b0[d])
y=np.arange(len(order))
ax.barh(y,[b0[d] for d in order],color=[ANC[parse(d)[1]] for d in order],edgecolor="k",lw=.3)
ax.set_yticks(y);ax.set_yticklabels(order,fontsize=6)
ax.set_xlabel("EOS B0 (GPa, UMA — relative)")
ax.set_title("(A) Bulk modulus ranking (soft↓ for coating)",fontsize=10)
ax.legend(handles=[Patch(fc=ANC['O'],label='oxide'),Patch(fc=ANC['F'],label='fluoride')],fontsize=8,loc="lower right")
ax.grid(axis="x",alpha=.3)

# (B) cation-group: de (x) vs E (y), group-colored
ax=fig.add_subplot(2,3,2)
for r in rows:
    if math.isnan(r["de"]) or not ok_el(r): continue
    ax.scatter(r["de"],r["E"],c=GRPC[r["group"]],s=32,edgecolor="white",lw=.4)
ax.set_xlabel("formation Δe (eV/atom)");ax.set_ylabel("E_young (GPa, UMA)")
ax.set_title("(B) Cation chemistry — lanthanide cluster = stable",fontsize=10)
ax.legend(handles=[Patch(fc=GRPC[g],label=g) for g in GRPC],fontsize=7.5,loc="upper left");ax.grid(alpha=.3)

# (C) fluoride vs oxide head-to-head (same cation)
ax=fig.add_subplot(2,3,3)
pairs=[]
for cat in sorted(set(r["cation"] for r in rows)):
    ox=[d for d in dops if parse(d)[0]==cat and parse(d)[1]=="O"]
    fl=[d for d in dops if parse(d)[0]==cat and parse(d)[1]=="F"]
    if ox and fl:
        pairs.append((cat,dmean(ox[0],"de"),dmean(fl[0],"de")))
pairs=[p for p in pairs if not math.isnan(p[1]) and not math.isnan(p[2])]
cats=[p[0] for p in pairs];x=np.arange(len(cats))
ax.bar(x-0.2,[p[1] for p in pairs],0.4,color=ANC["O"],label="oxide",edgecolor="k",lw=.3)
ax.bar(x+0.2,[p[2] for p in pairs],0.4,color=ANC["F"],label="fluoride",edgecolor="k",lw=.3)
ax.set_xticks(x);ax.set_xticklabels(cats);ax.set_ylabel("formation Δe (eV/atom)")
ax.set_title("(C) Oxide vs Fluoride (same cation) — oxide stabilizes more",fontsize=10)
ax.legend(fontsize=8);ax.grid(axis="y",alpha=.3)

# (D) ductility map: Pugh G/B vs E (coating wants ductile=low G/B + soft=low E)
ax=fig.add_subplot(2,3,4)
for r in rows:
    if not ok_el(r) or math.isnan(r["pugh"]): continue
    ax.scatter(r["pugh"],r["E"],c=ANC[r["anion"]],s=32,edgecolor="white",lw=.4)
ax.axvline(0.571,ls="--",color="0.4",lw=1)  # Pugh brittle/ductile ~0.57 (G/B)
ax.text(0.571,ax.get_ylim()[1],"  brittle→ / ←ductile",fontsize=7,va="top",color="0.4",rotation=90)
ax.set_xlabel("Pugh ratio G/B (lower = more ductile)");ax.set_ylabel("E_young (GPa)")
ax.set_title("(D) Ductility map — ductile+soft (lower-left) best for coating",fontsize=10);ax.grid(alpha=.3)

# (E) +Clrich effect on de (box)
ax=fig.add_subplot(2,3,5)
de_cl=[r["de"] for r in rows if r["clrich"] and not math.isnan(r["de"])]
de_no=[r["de"] for r in rows if not r["clrich"] and not math.isnan(r["de"])]
bp=ax.boxplot([de_no,de_cl],labels=[f"plain\n(n={len(de_no)})",f"+Clrich\n(n={len(de_cl)})"],
              patch_artist=True,widths=.5)
for p,c in zip(bp["boxes"],["#bbbbbb","#2a9d8f"]): p.set_facecolor(c)
for i,dat in enumerate([de_no,de_cl],1):
    ax.scatter(np.random.default_rng(i).normal(i,0.05,len(dat)),dat,s=12,c="0.25",alpha=.5,zorder=3)
ax.set_ylabel("formation Δe (eV/atom)")
ax.set_title("(E) +Cl-rich variant effect on stability",fontsize=10);ax.grid(axis="y",alpha=.3)

# (F) dV vs de
ax=fig.add_subplot(2,3,6)
for r in rows:
    if math.isnan(r["dV"]) or math.isnan(r["de"]): continue
    ax.scatter(r["dV"],r["de"],c=GRPC[r["group"]],s=30,edgecolor="white",lw=.4)
ax.set_xlabel("anneal ΔV (%)");ax.set_ylabel("formation Δe (eV/atom)")
ax.set_title("(F) Lattice strain vs stability (|ΔV| small = less misfit)",fontsize=10)
ax.axvline(0,color="0.6",lw=.8);ax.grid(alpha=.3)

plt.suptitle("Doping cascade v23 — detailed breakdowns (B0 · cation-group · O-vs-F · ductility · Cl-rich · strain)",
             fontsize=13,y=1.0)
plt.tight_layout()
plt.savefig(f"{OUT}/cascade_v23_detail.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_detail.pdf",bbox_inches="tight")
print(f"saved {OUT}/cascade_v23_detail.png")

# console: O vs F summary + group means
print("\n=== Oxide vs Fluoride Δe (same cation) ===")
for cat,o,f in pairs: print(f"  {cat:3s}  oxide {o:+.3f}   fluoride {f:+.3f}   Δ(O-F) {o-f:+.3f}")
print("\n=== group mean Δe / E ===")
for g in GRPC:
    de=[r["de"] for r in rows if r["group"]==g and not math.isnan(r["de"])]
    E=[r["E"] for r in rows if r["group"]==g and ok_el(r)]
    print(f"  {g:11s} n={len(de):2d}  de={np.mean(de):+.3f}  E={np.mean(E):.1f}")
print(f"\nClrich de mean {np.mean(de_cl):+.3f} (n{len(de_cl)}) vs plain {np.mean(de_no):+.3f} (n{len(de_no)})")
