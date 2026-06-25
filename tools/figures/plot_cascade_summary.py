#!/usr/bin/env python3
"""plot_cascade_summary.py — two deck-grade summary visuals:
 (1) MASTER SCORECARD heatmap: every dopant x every normalized property (good=green),
     sorted by 4-objective composite, with verdict tags.
 (2) PERIODIC-TABLE performance map: cation element colored by best composite score.
All CSV-driven (champions + esw + litransport). UMA-relative, x=0.25 (over-doped regime).
"""
import csv, re, math, io
import numpy as np
from collections import Counter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}; MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
def fnum(s):
    try: return float(s)
    except: return math.nan
def parse(d):
    d=d.split("+")[0]
    toks=[(e,int(n) if n else 1) for e,n in re.findall(r"([A-Z][a-z]?)(\d*)",d) if e]
    an="O" if any(e=="O" for e,_ in toks) else "F"
    cat=[(e,n) for e,n in toks if e not in ("O","F")][0]
    av=2 if an=="O" else 1; bn=[n for e,n in toks if e==an][0]; val=round(av*bn/cat[1])
    return cat[0],an,val
lt={r["_dir"]:r for r in csv.DictReader(open("db/properties/cascade_v23_litransport.csv"))}
ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")): ch.setdefault(r["dopant"].split("+")[0],[]).append(r)
esw={}
_raw=open("db/properties/oxidation_stability_cascade.csv").read().splitlines()
_h=next(i for i,l in enumerate(_raw) if l.startswith("dopant,"))
for r in csv.DictReader(io.StringIO("\n".join(_raw[_h:]))): esw[r["dopant"]]=(fnum(r["ox_V"]),fnum(r["red_V"]),fnum(r["window_V"]))
def agg(d,k,dn=False):
    vs=[fnum(r[k]) for r in ch[d] if not math.isnan(fnum(r[k])) and not(dn and fnum(r["elastic_poisson_nu"])<0)]
    return np.mean(vs) if vs else math.nan
D=[]
for d in ch:
    if d not in esw: continue
    cat,an,val=parse(d); ox,red,win=esw[d]; dirs=[r["_dir"] for r in ch[d]]
    blk=[fnum(lt[x]["tier2_dopant_blocking_fraction"]) for x in dirs if x in lt and lt[x]["tier2_dopant_blocking_fraction"]]
    mig=[fnum(lt[x]["migration_volume_fraction"]) for x in dirs if x in lt and lt[x]["migration_volume_fraction"]]
    D.append(dict(dop=d,cat=cat,an=an,val=val,de=agg(d,"rerank_de_post_anneal"),
        E=agg(d,"elastic_E_young_GPa",True),pugh=agg(d,"elastic_pugh_GoverB",True),
        ox=ox,red=red,win=win,blk=np.mean(blk) if blk else math.nan,mig=np.mean(mig) if mig else math.nan))
D=[x for x in D if not math.isnan(x["de"])]
def nrm(key,hi=True):
    v=np.array([x[key] for x in D],float); v=np.where(np.isnan(v),np.nanmean(v),v)
    z=(v-np.nanmin(v))/(np.nanmax(v)-np.nanmin(v)+1e-9); return z if hi else 1-z
cols=[("stable",nrm("de",False)),("oxidation",nrm("ox")),("reduction",nrm("red",False)),
      ("soft",nrm("E",False)),("ductile",nrm("pugh",False)),("Li-mobile",nrm("blk",False)),("Li-volume",nrm("mig"))]
comp=0.22*nrm("de",False)+0.20*nrm("ox")+0.18*nrm("blk",False)+0.15*nrm("E",False)+0.13*nrm("red",False)+0.12*nrm("win")
for i,x in enumerate(D): x["comp"]=comp[i]

# ---------- (1) scorecard heatmap ----------
order=sorted(range(len(D)),key=lambda i:-comp[i])
M=np.array([[c[1][i] for _,c in [(n,(n,z)) for n,z in cols]] for i in order])
fig,ax=plt.subplots(figsize=(10,13))
im=ax.imshow(M,cmap="RdYlGn",vmin=0,vmax=1,aspect="auto")
ax.set_xticks(range(len(cols)));ax.set_xticklabels([c[0] for c in cols],rotation=40,ha="right",fontsize=9)
ax.set_yticks(range(len(order)));ax.set_yticklabels([f"{D[i]['dop']}" for i in order],fontsize=7)
for r,i in enumerate(order):
    x=D[i]
    vd="winner" if x["comp"]>0.62 else ("coat:Li-block" if x["blk"]>0.82 else ("avoid:window" if x["win"]<0.1 else ""))
    ax.text(len(cols)-0.3,r,f" {x['comp']:.2f} {vd}",va="center",fontsize=6.2,
            color=("#1a7a1a" if x["comp"]>0.6 else "#b00" if vd.startswith("avoid") else "0.3"))
ax.set_title("Cascade v23 MASTER SCORECARD — dopant × property (green=good), sorted by composite\n"
             "[x=0.25 over-doped regime; Li-mobile is high-x trend — see lit grounding]",fontsize=10)
plt.colorbar(im,ax=ax,fraction=0.03,pad=0.18,label="normalized (1=best)")
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_scorecard.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_scorecard.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_scorecard.png")

# ---------- (2) periodic-table performance map ----------
POS={"Li":(1,0),"B":(1,12),"Na":(2,0),"Mg":(2,1),"Al":(2,12),"Si":(2,13),
"Ca":(3,1),"Sc":(3,2),"Ti":(3,3),"V":(3,4),"Cr":(3,5),"Mn":(3,6),"Fe":(3,7),"Co":(3,8),"Ni":(3,9),
"Cu":(3,10),"Zn":(3,11),"Ga":(3,12),"Ge":(3,13),
"Sr":(4,1),"Y":(4,2),"Zr":(4,3),"Nb":(4,4),"Mo":(4,5),"Ag":(4,10),"In":(4,12),"Sn":(4,13),"Sb":(4,14),
"Ba":(5,1),"Hf":(5,3),"Ta":(5,4),"W":(5,5),
"La":(7,2),"Nd":(7,5),"Sm":(7,7),"Gd":(7,9)}
best={}
for x in D:
    if x["cat"] not in best or x["comp"]>best[x["cat"]]["comp"]: best[x["cat"]]=x
fig,ax=plt.subplots(figsize=(15,7.5))
cmap=plt.cm.RdYlGn
for el,(r,c) in POS.items():
    if el in best:
        x=best[el]; col=cmap(x["comp"])
        ax.add_patch(Rectangle((c,-r),0.92,0.92,facecolor=col,edgecolor="k",lw=.6))
        ax.text(c+0.46,-r+0.62,el,ha="center",fontsize=10,fontweight="bold")
        ax.text(c+0.46,-r+0.30,f"{x['comp']:.2f}",ha="center",fontsize=7)
        ax.text(c+0.46,-r+0.10,f"de{x['de']:+.1f}",ha="center",fontsize=5.5,color="0.25")
    else:
        ax.add_patch(Rectangle((c,-r),0.92,0.92,facecolor="0.92",edgecolor="0.7",lw=.4))
        ax.text(c+0.46,-r+0.46,el,ha="center",fontsize=9,color="0.6")
ax.set_xlim(-0.3,15.3);ax.set_ylim(-7.6,-0.4);ax.axis("off")
ax.set_title("Cascade v23 — best-dopant composite score on the periodic table\n"
             "(green=best all-round dopant; number=composite, deX=stability). Lanthanides bottom strip.",fontsize=12)
sm=plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(min(x["comp"] for x in D),max(x["comp"] for x in D)))
plt.colorbar(sm,ax=ax,fraction=0.025,label="composite score")
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_ptable.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_ptable.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_ptable.png")
print("\ntop-6 composite:",", ".join(f"{D[i]['dop']}({comp[i]:.2f})" for i in order[:6]))
print("periodic hotspots:",", ".join(f"{e}({best[e]['comp']:.2f})" for e in sorted(best,key=lambda e:-best[e]['comp'])[:6]))
