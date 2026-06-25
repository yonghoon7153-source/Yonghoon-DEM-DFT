#!/usr/bin/env python3
"""plot_cascade_deep.py — deeper insight squeeze on the v23 cascade.
Adds FUNDAMENTAL descriptors (Shannon ionic radius, ionic potential z/r, Pauling
EN) to explain WHY the trends exist, PCA family map, application-specific rankings
(cathode / anode / bulk), and replicate robustness. All CSV-driven -> re-run after
the 4 recomputes land. 6 panels. UMA-relative, x=0.25.
"""
import csv, re, math, os, io
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}; MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
# Shannon ionic radius (A, 6-coord, the oxidation state used) & Pauling EN
RAD={"Li":0.76,"Na":1.02,"Ag":1.15,"Cu1":0.77,"Mg":0.72,"Ca":1.00,"Sr":1.18,"Ba":1.35,"Mn":0.83,
"Fe2":0.78,"Co":0.745,"Ni":0.69,"Zn":0.74,"Al":0.535,"Ga":0.62,"In":0.80,"Sc":0.745,"Y":0.90,
"Cr3":0.615,"Fe":0.645,"B":0.27,"La":1.032,"Nd":0.983,"Sm":0.958,"Gd":0.938,"Ti":0.605,"Zr":0.72,
"Hf":0.71,"Si":0.40,"Ge":0.53,"Sn":0.69,"Nb":0.64,"Ta":0.64,"V":0.54,"Sb":0.60,"Cr":0.44,"Mo":0.59,"W":0.60}
EN={"Li":0.98,"Na":0.93,"Ag":1.93,"Cu":1.90,"Mg":1.31,"Ca":1.00,"Sr":0.95,"Ba":0.89,"Mn":1.55,
"Fe":1.83,"Co":1.88,"Ni":1.91,"Zn":1.65,"Al":1.61,"Ga":1.81,"In":1.78,"Sc":1.36,"Y":1.22,"Cr":1.66,
"B":2.04,"La":1.10,"Nd":1.14,"Sm":1.17,"Gd":1.20,"Ti":1.54,"Zr":1.33,"Hf":1.30,"Si":1.90,"Ge":2.01,
"Sn":1.96,"Nb":1.6,"Ta":1.5,"V":1.63,"Sb":2.05,"Mo":2.16,"W":2.36}
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
def radius(cat,val):
    for k in (f"{cat}{val}",cat):
        if k in RAD: return RAD[k]
    return math.nan

# merge
ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")):
    ch.setdefault(r["dopant"].split("+")[0],[]).append(r)
def agg(d,k,dropneg=False):
    vs=[fnum(r[k]) for r in ch[d] if not math.isnan(fnum(r[k])) and not(dropneg and fnum(r["elastic_poisson_nu"])<0)]
    return (np.mean(vs),np.std(vs)) if vs else (math.nan,math.nan)
esw={}
_raw=open("db/properties/oxidation_stability_cascade.csv").read().splitlines()
_h=next(i for i,l in enumerate(_raw) if l.startswith("dopant,"))
for r in csv.DictReader(io.StringIO("\n".join(_raw[_h:]))): esw[r["dopant"]]=(fnum(r["ox_V"]),fnum(r["red_V"]))
D=[]
for d in ch:
    if d not in esw: continue
    cat,an,val,grp=parse(d); ox,red=esw[d]; rad=radius(cat,val)
    de,des=agg(d,"rerank_de_post_anneal"); E,_=agg(d,"elastic_E_young_GPa",True); B0,_=agg(d,"eos_B0_GPa")
    pugh,_=agg(d,"elastic_pugh_GoverB",True); dV,_=agg(d,"anneal_dV_pct")
    if math.isnan(de): continue
    D.append(dict(dop=d,cat=cat,an=an,val=val,grp=grp,de=de,de_std=des,E=E,B0=B0,pugh=pugh,dV=dV,
                  ox=ox,red=red,rad=rad,zr=val/rad if rad==rad else math.nan,en=EN.get(cat,math.nan)))

fig=plt.figure(figsize=(18,12))
def sc(ax,xk,yk,inv=False,ann=()):
    for x in D:
        if math.isnan(x[xk]) or math.isnan(x[yk]): continue
        ax.scatter(x[xk],x[yk],c=GRPC[x["grp"]],s=42,edgecolor="white",lw=.5,zorder=3)
        if x["dop"] in ann: ax.annotate(x["dop"],(x[xk],x[yk]),fontsize=6.5,xytext=(3,2),textcoords="offset points")
    xs=[x[xk] for x in D if not math.isnan(x[xk]) and not math.isnan(x[yk])]
    ys=[x[yk] for x in D if not math.isnan(x[xk]) and not math.isnan(x[yk])]
    if len(xs)>3:
        r=np.corrcoef(xs,ys)[0,1]; b=np.polyfit(xs,ys,1)
        xf=np.linspace(min(xs),max(xs),50); ax.plot(xf,np.polyval(b,xf),"k--",lw=1,alpha=.6)
        ax.text(.04,.93,f"r={r:+.2f}",transform=ax.transAxes,fontsize=10,fontweight="bold")
    if inv: ax.invert_yaxis()

# (A) de vs z/r (ionic potential)
ax=fig.add_subplot(2,3,1); sc(ax,"zr","de",inv=True,ann=("Gd2O3","Ta2O5","Sc2O3","B2O3","Ag2O"))
ax.set_xlabel("ionic potential z/r  (valence / radius)"); ax.set_ylabel("formation Δe (↓ stable)")
ax.set_title("(A) Stability mechanism: higher charge-density → more stable",fontsize=10)
ax.legend(handles=[Patch(fc=GRPC[g],label=g) for g in GRPC],fontsize=7,loc="lower right")

# (B) ox vs EN
ax=fig.add_subplot(2,3,2); sc(ax,"en","ox",ann=("Sc2O3","Cr2O3","Fe2O3","CoO","WO3","B2O3"))
ax.axhline(2.14,ls="--",color="0.5",lw=1)
ax.set_xlabel("cation Pauling electronegativity"); ax.set_ylabel("oxidation onset V")
ax.set_title("(B) Oxidation: high-EN (noble/late-TM) cations collapse window",fontsize=10)

# (C) descriptor -> property correlations
ax=fig.add_subplot(2,3,3)
desc=["val","rad","zr","en"]; prop=["de","ox","red","E","B0","pugh"]
C=np.zeros((len(desc),len(prop)))
for i,a in enumerate(desc):
    for j,b in enumerate(prop):
        xs=[x[a] for x in D if not math.isnan(x[a]) and not math.isnan(x[b])]
        ys=[x[b] for x in D if not math.isnan(x[a]) and not math.isnan(x[b])]
        C[i,j]=np.corrcoef(xs,ys)[0,1] if len(xs)>3 else 0
im=ax.imshow(C,cmap="RdBu_r",vmin=-1,vmax=1,aspect="auto")
ax.set_xticks(range(len(prop)));ax.set_xticklabels(prop,fontsize=8)
ax.set_yticks(range(len(desc)));ax.set_yticklabels(["valence","radius","z/r","EN"],fontsize=8)
for i in range(len(desc)):
    for j in range(len(prop)): ax.text(j,i,f"{C[i,j]:.2f}",ha="center",va="center",fontsize=7,color="white" if abs(C[i,j])>.5 else "k")
plt.colorbar(im,ax=ax,fraction=.046)
ax.set_title("(C) Fundamental descriptor → property (Pearson r)",fontsize=10)

# (D) PCA family map
ax=fig.add_subplot(2,3,4)
keys=["de","ox","red","E","B0","pugh","zr","en"]
M=np.array([[x[k] for k in keys] for x in D],float)
M=np.where(np.isnan(M),np.nanmean(M,axis=0),M)
Z=(M-M.mean(0))/(M.std(0)+1e-9); U,S,Vt=np.linalg.svd(Z,full_matrices=False)
PC=U[:,:2]*S[:2]; ev=(S**2/np.sum(S**2))[:2]
for i,x in enumerate(D):
    ax.scatter(PC[i,0],PC[i,1],c=GRPC[x["grp"]],s=45,edgecolor="white",lw=.5,zorder=3)
    if x["dop"] in ("Sc2O3","Gd2O3","Fe2O3","CoO","LiF","B2O3","Ta2O5","MnO"):
        ax.annotate(x["dop"],(PC[i,0],PC[i,1]),fontsize=6.5,xytext=(3,2),textcoords="offset points")
ax.set_xlabel(f"PC1 ({ev[0]*100:.0f}%)"); ax.set_ylabel(f"PC2 ({ev[1]*100:.0f}%)")
ax.set_title("(D) PCA family map — natural dopant groupings",fontsize=10); ax.grid(alpha=.3)

# (E) application-specific top-6
ax=fig.add_subplot(2,3,5); ax.axis("off")
def nrm(key,hi=True):
    v=np.array([x[key] for x in D],float); v=np.where(np.isnan(v),np.nanmean(v),v)
    z=(v-v.min())/(v.max()-v.min()+1e-9); return z if hi else 1-z
apps={
 "CATHODE coat":0.40*nrm("ox")+0.30*nrm("E",False)+0.20*nrm("de",False)+0.10*nrm("pugh",False),
 "ANODE coat":  0.40*nrm("red",False)+0.30*nrm("E",False)+0.20*nrm("de",False)+0.10*nrm("pugh",False),
 "BULK dopant": 0.45*nrm("de",False)+0.30*nrm("dV" ,False)+0.25*nrm("E",False),  # +mobility when avail
}
txt="Top-6 per use-case (normalized weighted sum)\n"
for app,s in apps.items():
    rank=sorted(range(len(D)),key=lambda i:-s[i])[:6]
    txt+=f"\n[{app}]\n  "+"  ".join(f"{D[i]['dop']}({s[i]:.2f})" for i in rank)+"\n"
ax.text(0,1,txt,va="top",ha="left",fontsize=8.6,family="monospace")
ax.set_title("(E) Application-specific rankings",fontsize=10,loc="left")

# (F) replicate robustness
ax=fig.add_subplot(2,3,6)
ds=sorted([x for x in D if not math.isnan(x["de_std"])],key=lambda x:-x["de_std"])[:18]
y=np.arange(len(ds))
ax.barh(y,[x["de_std"] for x in ds],color=[GRPC[x["grp"]] for x in ds],edgecolor="k",lw=.3)
ax.set_yticks(y);ax.set_yticklabels([x["dop"] for x in ds],fontsize=7)
ax.set_xlabel("Δe std across 3 placement replicates (eV/atom)")
ax.set_title("(F) Champion robustness — high std = placement-sensitive (less reliable)",fontsize=10)
ax.grid(axis="x",alpha=.3)

plt.suptitle("Cascade v23 — DEEP insights (descriptors · PCA · application rankings · robustness)",fontsize=13,y=1.0)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_deep.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_deep.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_deep.png")

print("\n=== descriptor→property strongest (|r|>0.45) ===")
for i,a in enumerate(["valence","radius","z/r","EN"]):
    for j,b in enumerate(prop):
        if abs(C[i,j])>0.45: print(f"  {a:8s} -> {b:5s}: r={C[i,j]:+.2f}")
print("\n=== application winners ===")
for app,s in apps.items():
    print(f"  {app:13s}: "+", ".join(D[i]["dop"] for i in sorted(range(len(D)),key=lambda i:-s[i])[:5]))
print("\n=== least robust (high replicate std) ===",", ".join(x["dop"] for x in ds[:6]))
