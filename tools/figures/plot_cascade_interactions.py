#!/usr/bin/env python3
"""plot_cascade_interactions.py — does the effect of one cascade descriptor on a
property DEPEND on another descriptor (statistical interaction)? Focus: valence x
anion on stability (de) and oxidation onset (ox). Interaction plots + OLS with
interaction terms (numpy lstsq, t-tests). 47 dopants, x=0.25, UMA-relative.
NOTE unbalanced design: fluorides only at valence 1-4 (no F5+/F6+) -> the
valence:anion interaction is identifiable only over val 1-4; oxide-only 5/6 shown
for context. Cl-rich excluded (plain variant)."""
import csv, re, math, os, io
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}
MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
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

# merge per-dopant
ch={}
for r in csv.DictReader(open("db/properties/cascade_v23_champions.csv")):
    ch.setdefault(r["dopant"].split("+")[0],[]).append(r)
def agg(d,k,dropneg=False):
    vs=[fnum(r[k]) for r in ch[d] if not math.isnan(fnum(r[k])) and not (dropneg and fnum(r["elastic_poisson_nu"])<0)]
    return np.mean(vs) if vs else math.nan
esw={}
_raw=open("db/properties/oxidation_stability_cascade.csv").read().splitlines()
_h=next(i for i,l in enumerate(_raw) if l.startswith("dopant,"))
for r in csv.DictReader(io.StringIO("\n".join(_raw[_h:]))):
    esw[r["dopant"]]=(fnum(r["ox_V"]),fnum(r["red_V"]))
D=[]
for d in ch:
    if d not in esw: continue
    cat,an,val,grp=parse(d); ox,red=esw[d]
    D.append(dict(dop=d,anion=an,val=val,grp=grp,isF=1.0 if an=="F" else 0.0,
                  de=agg(d,"rerank_de_post_anneal"),E=agg(d,"elastic_E_young_GPa",True),ox=ox,red=red))
D=[x for x in D if not math.isnan(x["de"])]

def ols(X,y):
    X=np.asarray(X,float); y=np.asarray(y,float)
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    resid=y-X@beta; n,p=X.shape; dof=max(n-p,1)
    s2=(resid@resid)/dof
    cov=s2*np.linalg.pinv(X.T@X); se=np.sqrt(np.clip(np.diag(cov),0,None))
    t=beta/np.where(se>0,se,np.nan)
    r2=1-(resid@resid)/(((y-y.mean())**2).sum()+1e-12)
    return beta,se,t,r2

def model(prop):
    rows=[x for x in D if not math.isnan(x[prop])]
    X=[[1,x["val"],x["isF"],x["val"]*x["isF"]] for x in rows]
    return ols(X,[x[prop] for x in rows]),["intercept","valence","isF","valence:isF"]

fig,axs=plt.subplots(2,2,figsize=(16,11))
COL={"O":"#2a6fb0","F":"#e08a1e"}

# (A) interaction plot: de ~ valence x anion
ax=axs[0,0]
for an in ["O","F"]:
    xs,ms,ses=[],[],[]
    for v in sorted(set(x["val"] for x in D if x["anion"]==an)):
        de=[x["de"] for x in D if x["anion"]==an and x["val"]==v]
        xs.append(v); ms.append(np.mean(de)); ses.append(np.std(de)/max(len(de)**.5,1))
    ax.errorbar(xs,ms,yerr=ses,marker="o",color=COL[an],lw=2,capsize=3,label=f"{an} (n/val)")
    for x in [z for z in D if z["anion"]==an]:
        ax.scatter(x["val"]+(0.06 if an=="F" else -0.06),x["de"],c=COL[an],s=14,alpha=.4)
ax.set_xlabel("cation valence"); ax.set_ylabel("formation Δe (eV/atom)")
ax.set_title("(A) INTERACTION valence×anion → stability\nlines diverge at val 3 (oxide pulls ahead) = interaction",fontsize=10)
ax.legend(title="anion",fontsize=9); ax.grid(alpha=.3); ax.invert_yaxis()

# (B) interaction plot: ox ~ valence x anion
ax=axs[0,1]
for an in ["O","F"]:
    xs,ms,ses=[],[],[]
    for v in sorted(set(x["val"] for x in D if x["anion"]==an)):
        ox=[x["ox"] for x in D if x["anion"]==an and x["val"]==v]
        xs.append(v); ms.append(np.mean(ox)); ses.append(np.std(ox)/max(len(ox)**.5,1))
    ax.errorbar(xs,ms,yerr=ses,marker="s",color=COL[an],lw=2,capsize=3,label=an)
ax.axhline(2.14,ls="--",color="0.5",lw=1)
ax.set_xlabel("cation valence"); ax.set_ylabel("oxidation onset V")
ax.set_title("(B) INTERACTION valence×anion → oxidation onset",fontsize=10)
ax.legend(title="anion",fontsize=9); ax.grid(alpha=.3)

# (C) O–F gap per valence (the interaction, isolated)
ax=axs[1,0]
vals=sorted(set(x["val"] for x in D if x["isF"]==1))  # where both exist
gaps=[]
for v in vals:
    o=[x["de"] for x in D if x["anion"]=="O" and x["val"]==v]
    f=[x["de"] for x in D if x["anion"]=="F" and x["val"]==v]
    gaps.append(np.mean(o)-np.mean(f) if o and f else math.nan)
bars=ax.bar([str(v) for v in vals],gaps,color=["#c0392b" if g<0 else "#2980b9" for g in gaps],edgecolor="k")
ax.axhline(0,color="k",lw=.8)
ax.set_xlabel("cation valence"); ax.set_ylabel("Δe(oxide) − Δe(fluoride)  (<0 = oxide more stable)")
ax.set_title("(C) Anion effect is NOT constant across valence = the interaction\nval 3: oxide much more stable; val 4: fluoride edges ahead",fontsize=10)
ax.grid(axis="y",alpha=.3)

# (D) regression coefficients (de + ox models) with t-values
ax=axs[1,1]
(b1,se1,t1,r2de),names=model("de")
(b2,se2,t2,r2ox),_=model("ox")
x=np.arange(len(names)); w=0.38
ax.bar(x-w/2,b1[1:].tolist() if False else b1,w,yerr=se1,color="#e0541e",capsize=3,label=f"Δe model (R²={r2de:.2f})")
ax.bar(x+w/2,b2,w,yerr=se2,color="#2a6fb0",capsize=3,label=f"ox model (R²={r2ox:.2f})")
for i in range(len(names)):
    if abs(t1[i])>2: ax.text(i-w/2,b1[i],"*",ha="center",va="bottom",fontsize=13,color="#e0541e")
    if abs(t2[i])>2: ax.text(i+w/2,b2[i],"*",ha="center",va="bottom",fontsize=13,color="#2a6fb0")
ax.axhline(0,color="k",lw=.8); ax.set_xticks(x); ax.set_xticklabels(names,rotation=20,ha="right",fontsize=8)
ax.set_ylabel("OLS coefficient"); ax.set_title("(D) Regression w/ interaction term (* = |t|>2)\nvalence:isF = interaction strength",fontsize=10)
ax.legend(fontsize=8); ax.grid(axis="y",alpha=.3)

plt.suptitle("Cascade v23 — parameter INTERACTIONS (valence × anion on stability & oxidation)",fontsize=13,y=1.0)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_interactions.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_interactions.pdf",bbox_inches="tight")
print(f"saved {OUT}/cascade_v23_interactions.png")

print("\n=== Δe model: de ~ valence + isF + valence:isF ===")
for n,b,s,t in zip(names,b1,se1,t1): print(f"  {n:14s} b={b:+.4f}  se={s:.4f}  t={t:+.2f} {'*' if abs(t)>2 else ''}")
print(f"  R2={r2de:.3f}")
print("\n=== ox model ===")
for n,b,s,t in zip(names,b2,se2,t2): print(f"  {n:14s} b={b:+.4f}  se={s:.4f}  t={t:+.2f} {'*' if abs(t)>2 else ''}")
print(f"  R2={r2ox:.3f}")
print("\nO−F stability gap per valence:", {v:round(g,3) for v,g in zip(vals,gaps)})
