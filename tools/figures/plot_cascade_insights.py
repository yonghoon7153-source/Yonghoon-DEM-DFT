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

# 경로는 env 로 갈아끼운다 — 정본을 덮지 않고 회수분(90종)으로 병렬 생성하기 위해.
#   CASCADE_CHAMP / CASCADE_ESW / CASCADE_RANKED / CASCADE_FIGDIR (2026-08-14)
OUT=os.environ.get("CASCADE_FIGDIR","docs/figures/cascade")
CHAMP=os.environ.get("CASCADE_CHAMP","db/properties/cascade_v23_champions.csv")
ESWCSV=os.environ.get("CASCADE_ESW","db/properties/oxidation_stability_cascade.csv")
RANKED=os.environ.get("CASCADE_RANKED","db/properties/cascade_v23_ranked.csv")
os.makedirs(OUT, exist_ok=True)
LANTH={"La","Nd","Sm","Gd"}; ALKALI={"Li","Na"}; AE={"Mg","Ca","Sr","Ba"}
MAIN={"B","Al","Ga","In","Si","Ge","Sn","Sb"}
GRPC={"lanthanide":"#ec407a","TM":"#5c6bc0","main-group":"#26a69a","alk.earth":"#7cb342","alkali":"#9e9e9e"}
def fnum(s):
    try: return float(s)
    except: return math.nan
#: 음이온별 형식 원자가. ⛔⛔ 2026-08-13 — 옛 판은 `anion = "O" if ... else "F"` 로
#:  **산화물/불화물만** 가정했다. 47종 풀에서는 참이었지만, 6/29 이후 등록되지 않았던
#:  염화물·황화물·브롬화물·요오드화물·질화물 43종을 회수해 넣으면 ZrCl4 가 "F" 로,
#:  Li3N 이 "F" 로 잡혀 **원자가가 조용히 틀린다** (ZrCl4 → val 1, 실제 4).
#:  터지지 않고 그림·랭킹만 틀리는 종류라 제일 위험하다.
ANION_VAL={"O":2,"S":2,"N":3,"F":1,"Cl":1,"Br":1,"I":1}
def parse(d):
    d=d.split("+")[0]
    toks=[(e,int(n) if n else 1) for e,n in re.findall(r"([A-Z][a-z]?)(\d*)",d) if e]
    # 뒤쪽 원소부터 음이온 후보를 찾는다 (LiCl 의 Cl, Li2S 의 S, Li3N 의 N).
    an=[e for e,_ in toks if e in ANION_VAL]
    if not an:
        raise ValueError(f"음이온을 못 찾았다: {d} — ANION_VAL 에 추가할 것")
    anion=an[-1]
    cats=[(e,n) for e,n in toks if e!=anion]
    if not cats:
        raise ValueError(f"양이온을 못 찾았다: {d}")
    cat=cats[0]
    av=ANION_VAL[anion]; bn=[n for e,n in toks if e==anion][0]
    val=round(av*bn/cat[1])
    grp=("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI
         else "alk.earth" if cat[0] in AE else "main-group" if cat[0] in MAIN else "TM")
    return cat[0],anion,val,grp


def _selftest_parse():
    """양성 + **음성**. 옛 판이 틀리던 입력을 반드시 포함한다."""
    ok=True
    cases=[("Al2O3",("Al","O",3)), ("MgO",("Mg","O",2)), ("Li2O",("Li","O",1)),
           ("LiF",("Li","F",1)),  ("ZrF4",("Zr","F",4)), ("CaF2",("Ca","F",2)),
           # ↓ 옛 판이 전부 "F" 로 오인하던 것들 (회수 43종)
           ("ZrCl4",("Zr","Cl",4)), ("LiBr",("Li","Br",1)), ("LiI",("Li","I",1)),
           ("Li2S",("Li","S",1)),   ("Al2S3",("Al","S",3)), ("Li3N",("Li","N",1)),
           ("Mg3N2",("Mg","N",2)),  ("Ga2S3",("Ga","S",3)), ("NbCl5",("Nb","Cl",5))]
    for d,(c,a,v) in cases:
        got=parse(d)[:3]
        good=got==(c,a,v)
        ok&=good
        print(("  ✓ " if good else "  ✗ ")+f"{d:7s} → {got}"+("" if good else f"  기대 {(c,a,v)}"))
    try:
        parse("Xx9"); print("  ✗ 미지 음이온을 통과시켰다"); ok=False
    except ValueError:
        print("  ✓ 음이온을 못 찾으면 예외 (조용한 오분류 금지)")
    print("selftest "+("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__" and "--selftest" in os.sys.argv:
    raise SystemExit(_selftest_parse())

# ---- merge champions (per-dopant mean) + ESW ----
ch={}
for r in csv.DictReader(open(CHAMP)):
    d=r["dopant"].split("+")[0]; ch.setdefault(d,[]).append(r)
def _elastic_ok(r):
    """탄성 행이 물리적인가. **음의 B_hill/G_hill 은 계산 실패**이지 연질이 아니다.

    2026-08-14: Na2S_x100 이 B_hill = -36.27 GPa 인데 nu 만 보던 옛 가드를 통과해
    3점 평균에 들어갔고, 그 평균의 역수(1/0.40 = 2.50)가 "Na2S 가 연성 경험칙을
    넘는다" 는 **틀린 발견**을 만들었다 (Codex 재감사에서 잡힘).
    """
    B,G = fnum(r.get("elastic_B_hill_GPa","")), fnum(r.get("elastic_G_hill_GPa",""))
    if not math.isnan(B) and B<=0: return False
    if not math.isnan(G) and G<=0: return False
    return not (fnum(r["elastic_poisson_nu"])<0)

def agg(d,key,elastic=False):
    vs=[]
    for r in ch[d]:
        v=fnum(r[key])
        if math.isnan(v): continue
        if elastic and not _elastic_ok(r): continue
        vs.append(v)
    return np.mean(vs) if vs else math.nan
esw={}
import io
_raw=open(ESWCSV).read().splitlines()
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
with open(RANKED,"w",newline="") as f:
    w=csv.writer(f); w.writerow(["# composite cathode-coating ranking. UMA relative. x=0.25.",
        "score=0.30*ox+0.25*stable+0.20*soft+0.15*ductile+0.10*window (min-max norm)."])
    w.writerow(["rank","dopant","group","score","de","ox_V","red_V","E_GPa","pugh","pareto"])
    for i,x in enumerate(sorted(D,key=lambda x:-x["score"]),1):
        w.writerow([i,x["dop"],x["grp"],f"{x['score']:.3f}",f"{x['de']:.3f}",x["ox"],x["red"],
                    f"{x['E']:.1f}",f"{x['pugh']:.2f}","Y" if x["dop"] in pareto else ""])
print(f"saved {RANKED}")

# insights
print(f"\nPareto-optimal ({len(pareto)}): {', '.join(pareto)}")
print("\nTop-8 composite:")
for x in sorted(D,key=lambda x:-x["score"])[:8]:
    print(f"  {x['dop']:7s} score={x['score']:.3f} de={x['de']:+.2f} ox={x['ox']} E={x['E']:.0f} pugh={x['pugh']:.2f} ({x['grp']})")
print("\nKey correlations:")
for i,a in enumerate(keys):
    for j,b in enumerate(keys):
        if i<j and abs(C[i,j])>0.55: print(f"  {a}-{b}: r={C[i,j]:+.2f}")
