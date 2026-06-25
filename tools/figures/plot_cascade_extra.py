#!/usr/bin/env python3
"""plot_cascade_extra.py — 3 more cascade visuals:
 (1) RADAR fingerprints of 6 contrasting dopants (stable/ox/anode/soft/ductile/Li-mobile).
 (2) ANION-SITE analysis: does O go to S_16e (PS4 corner = phosphate-like) vs S_4a
     (free S2-)? and does S_16e preference correlate with stability (the nd O@PS4 story)?
 (3) 3D PARETO: stability x oxidation x Li-mobility, Pareto front marked.
CSV-driven. UMA-relative, x=0.25.
"""
import csv, re, math, io
import numpy as np
from collections import Counter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa
OUT="docs/figures/cascade"
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}; MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
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
    asites=[lt[x]["anion_site"] for x in dirs if x in lt]
    f16=sum(1 for s in asites if s=="S_16e")/len(asites) if asites else math.nan
    D.append(dict(dop=d,cat=cat,an=an,val=val,grp=grp,ox=ox,red=red,de=agg(d,"rerank_de_post_anneal"),
        E=agg(d,"elastic_E_young_GPa",True),pugh=agg(d,"elastic_pugh_GoverB",True),
        blk=np.mean(blk) if blk else math.nan,f16=f16,asites=asites))
D=[x for x in D if not math.isnan(x["de"])]
def nrm(key,hi=True):
    v=np.array([x[key] for x in D],float); v=np.where(np.isnan(v),np.nanmean(v),v)
    z=(v-np.nanmin(v))/(np.nanmax(v)-np.nanmin(v)+1e-9); return z if hi else 1-z
N={"stable":nrm("de",False),"ox":nrm("ox"),"anode":nrm("red",False),"soft":nrm("E",False),
   "ductile":nrm("pugh",False),"Li-mobile":nrm("blk",False)}
idx={x["dop"]:i for i,x in enumerate(D)}

# ---------- (1) RADAR ----------
axes=list(N); ang=np.linspace(0,2*np.pi,len(axes),endpoint=False).tolist(); ang+=ang[:1]
pick=["Sc2O3","Gd2O3","Li2O","Cr2O3","HfO2","Fe2O3"]
tags={"Sc2O3":"all-round winner","Gd2O3":"stability king","Li2O":"Li-mobility king",
      "Cr2O3":"ox+soft, blocks (coat)","HfO2":"anode+mobile gem","Fe2O3":"avoid (collapse)"}
fig=plt.figure(figsize=(15,9.5))
for k,dp in enumerate(pick):
    if dp not in idx: continue
    i=idx[dp]; vals=[N[a][i] for a in axes]; vals+=vals[:1]
    ax=fig.add_subplot(2,3,k+1,polar=True)
    ax.plot(ang,vals,color=GRPC[D[i]["grp"]],lw=2); ax.fill(ang,vals,color=GRPC[D[i]["grp"]],alpha=.25)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(axes,fontsize=8); ax.set_ylim(0,1); ax.set_yticklabels([])
    ax.set_title(f"{dp}\n{tags[dp]}",fontsize=10,pad=14)
plt.suptitle("Cascade v23 — multi-property RADAR fingerprints (1=best on each axis)",fontsize=13,y=1.0)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_radar.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_radar.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_radar.png")

# ---------- (2) ANION-SITE ----------
fig,axs=plt.subplots(1,2,figsize=(15,6))
ox_d=[x for x in D if x["an"]=="O" and not math.isnan(x["f16"])]
ax=axs[0]
cnt=Counter(s for x in D for s in x["asites"])
ax.bar(list(cnt),[cnt[k] for k in cnt],color=["#2a6fb0","#e0922a","#8e44ad"][:len(cnt)],edgecolor="k")
ax.set_ylabel("# champion-replicates"); ax.set_title("(A) Where the dopant anion sits\nS_16e=PS₄ corner, S_4a=free S²⁻, Cl_4d=halide",fontsize=10)
for i,k in enumerate(cnt): ax.text(i,cnt[k],cnt[k],ha="center",va="bottom",fontsize=9)
ax=axs[1]
xs=[x["f16"] for x in ox_d]; ys=[x["de"] for x in ox_d]
for x in ox_d:
    ax.scatter(x["f16"],x["de"],c=GRPC[x["grp"]],s=44,edgecolor="white",lw=.5,zorder=3)
    if x["dop"] in ("Sc2O3","Gd2O3","Nd2O3","Ta2O5","B2O3","Cr2O3","Ag2O"):
        ax.annotate(x["dop"],(x["f16"],x["de"]),fontsize=7,xytext=(3,2),textcoords="offset points")
if len(xs)>3:
    r=np.corrcoef(xs,ys)[0,1]; b=np.polyfit(xs,ys,1); xf=np.linspace(0,1,30)
    ax.plot(xf,np.polyval(b,xf),"k--",lw=1,alpha=.6); ax.text(.04,.06,f"r={r:+.2f}",transform=ax.transAxes,fontsize=11,fontweight="bold")
ax.invert_yaxis()
ax.set_xlabel("fraction of O at S_16e (PS₄ corner → phosphate-like)"); ax.set_ylabel("formation Δe (↓ stable)")
ax.set_title("(B) O@PS₄(16e) preference vs stability (tests nd O-effect generality)",fontsize=10); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_anionsite.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_anionsite.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_anionsite.png")

# ---------- (3) 3D PARETO ----------
P=[x for x in D if not math.isnan(x["blk"])]
def dom(a,b): return (b["de"]<=a["de"] and b["ox"]>=a["ox"] and b["blk"]<=a["blk"] and
                      (b["de"]<a["de"] or b["ox"]>a["ox"] or b["blk"]<a["blk"]))
front=[a["dop"] for a in P if not any(dom(a,b) for b in P if b is not a)]
fig=plt.figure(figsize=(12,10)); ax=fig.add_subplot(111,projection="3d")
for x in P:
    f=x["dop"] in front
    ax.scatter(x["de"],x["ox"],1-x["blk"],c=GRPC[x["grp"]],s=(90 if f else 38),
               edgecolor=("k" if f else "white"),lw=(1.5 if f else .4),depthshade=True)
    if f: ax.text(x["de"],x["ox"],1-x["blk"],x["dop"],fontsize=7)
ax.set_xlabel("formation Δe (← stable)"); ax.set_ylabel("oxidation onset V (↑)")
ax.set_zlabel("Li-mobility (1−block, ↑)")
ax.invert_xaxis(); ax.view_init(elev=22,azim=-60)
ax.set_title("Cascade v23 — 3D Pareto: stability × oxidation × Li-mobility\n(black-edge = Pareto-optimal, non-dominated)",fontsize=11)
plt.tight_layout(); plt.savefig(f"{OUT}/cascade_v23_3dpareto.png",dpi=150,bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_3dpareto.pdf",bbox_inches="tight"); print(f"saved {OUT}/cascade_v23_3dpareto.png")

print("\nO-site split:",dict(cnt))
print(f"S_16e-vs-stability r = {r:+.2f}  (n={len(ox_d)} oxides)")
print("3D Pareto-optimal:",", ".join(front))
