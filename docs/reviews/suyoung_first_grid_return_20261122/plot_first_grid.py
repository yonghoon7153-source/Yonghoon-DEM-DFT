"""Verify two returned native traces and draw the first F8/F16 grid comparison."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import tarfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


SOURCE = "fc685932f4a1710fe944c5d2dafbcb56bf239f473184f009983a3ff4805dabea"
KERNEL = "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645"


def read_curves(path):
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=SOURCE:
        raise ValueError("archive identity")
    curves=[]
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for cells in (8,16):
            prefix=f"run/F{cells}/"
            read=lambda name:archive.extractfile(prefix+name).read()
            raw=read("trace.csv")
            native=json.loads(read("result.json"))
            record=json.loads(read("candidate.json"))
            if not (native["trace_sha256"]==record["trace_sha256"]==hashlib.sha256(raw).hexdigest()
                    and native["status"]==record["status"]=="TARGET_BRACKETED"
                    and record["cells"]==cells and record["mapping"]=="ORIGINAL" and record["kernel_sha256"]==KERNEL):
                raise ValueError("trace identity")
            rows=list(csv.DictReader(io.StringIO(raw.decode("ascii"))))
            width=float(rows[0]["height"])
            x=[width-float(r["height"]) for r in rows]
            p=[float(r["bottom_pressure_E"])*10 for r in rows]
            if (any(b<=a for a,b in zip(x,x[1:])) or any(not math.isfinite(v) for v in x+p)
                    or len(rows)!=native["steps"]+1 or [int(r["step"]) for r in rows] != list(range(len(rows)))):
                raise ValueError("trace coordinates")
            curves.append((x,p))
    return curves


def at(x,y,k):
    j=bisect_left(x,k)
    if j<len(x) and x[j]==k:
        return y[j]
    if j==0 or j==len(x):
        raise ValueError("outside common interval")
    return y[j-1] + (k-x[j-1])/(x[j]-x[j-1])*(y[j]-y[j-1])


def calculate(curves):
    lo=max(x[0] for x,_ in curves); hi=min(x[-1] for x,_ in curves)
    knots=sorted({k for x,_ in curves for k in x if lo<=k<=hi})
    coarse,fine=([at(x,y,k) for k in knots] for x,y in curves)
    delta=[a-b for a,b in zip(coarse,fine)]
    fine_max=max(map(abs,fine)); peak=max(map(abs,delta)); idx=next(i for i,d in enumerate(delta) if abs(d)==peak)
    exceed=[20*abs(d)>fine_max for d in delta]; first=exceed.index(True)
    def obs(i):
        return dict(index=i,u=knots[i],coarse_MPa=coarse[i],fine_MPa=fine[i],coarse_minus_fine_MPa=delta[i])
    runs=[]
    for high, indices in itertools.groupby(range(len(knots)),key=lambda i:exceed[i]):
        if high:
            ids=list(indices)
            runs.append(dict(from_index=ids[0],to_index=ids[-1],from_u=knots[ids[0]],to_u=knots[ids[-1]],
                             count=len(ids)))
    result=dict(samples=[len(x) for x,_ in curves],ends=[x[-1] for x,_ in curves],
                terminal_MPa=[y[-1] for _,y in curves],common_count=len(knots),common=[lo,hi],
                D_MPa=fine_max,N_MPa=peak,tolerance_MPa=fine_max/20,ratio=peak/fine_max,
                first_exceed=obs(first),preceding=obs(first-1),at_max=obs(idx),
                exceed_count=sum(exceed),exceed_intervals_at_observed_knots=runs,
                same_initial_packing_replicates_per_resolution=1)
    return knots,delta,result


def plot(curves,knots,delta,r,out):
    warm,cool,ink,muted="#a34818","#155b87","#173242","#465c67"
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":20,"axes.spines.top":False,
                         "axes.spines.right":False,"path.simplify":False,"axes.labelcolor":ink,
                         "xtick.color":muted,"ytick.color":muted,"axes.edgecolor":"#74848a"})
    fig,(left,right)=plt.subplots(1,2,figsize=(18.3,8.4))
    fig.subplots_adjust(left=.077,right=.974,bottom=.26,top=.775,wspace=.25)
    fig.text(.078,.923,"Plate reaction changes with grid resolution",fontsize=29,weight="bold",color=ink)
    fig.text(.078,.851,"F8 and F16 loading  /  Same contact kernel and physical IDs  /  Development calculation",
             fontsize=19,color=muted)
    for ax,title in ((left,"Observed bottom-plate pressure"),(right,"F8 minus F16 on the common interval")):
        ax.set_title(title,loc="left",fontsize=21,weight="semibold",color=ink,pad=12)
        ax.grid(axis="y",color="#dee4e7",linewidth=.8)
        ax.set_axisbelow(True)
        ax.xaxis.set_major_locator(MultipleLocator(.025))
        ax.set_xlabel("Plate displacement, $u$ (dimensionless)",labelpad=10)
    hi=r["common"][1]; fine_x,fine_p=curves[1]
    left.axvspan(hi,fine_x[-1],color="#edf1f3",zorder=0)
    left.axvline(hi,color="#85929b",lw=1,ls=":")
    left.plot(*curves[0],lw=2.3,color=warm,label="F8")
    left.plot(fine_x,fine_p,lw=2.3,color=cool,label="F16")
    left.scatter([x[-1] for x,_ in curves],[p[-1] for _,p in curves],c=[warm,cool],s=55,zorder=5)
    left.legend(frameon=False,loc="upper left")
    left.set(xlim=(-.002,.151),ylim=(-.04,1.26),ylabel="Bottom-plate pressure (MPa)")
    limit=r["tolerance_MPa"]
    right.axhspan(-limit,limit,color="#e6eee8",zorder=0)
    right.axhline(limit,ls="--",color="#48705b",lw=1.2)
    right.axhline(-limit,ls="--",color="#48705b",lw=1.2)
    right.axhline(0,color="#a7b3b8",lw=.6)
    right.plot(knots,delta,color=cool,lw=2.3)
    right.set(xlim=(-.002,.123),ylim=(-.12,.61),ylabel="Signed difference (MPa)")
    for name,label,xytext,align in (
            ("first_exceed","First >5%",(.009,.195),"left"),("at_max","Maximum difference",(.108,.57),"right")):
        d=r[name]; xy=(d["u"],d["coarse_minus_fine_MPa"])
        right.scatter(*xy,s=48,color=warm,zorder=5)
        right.annotate(label,xy=xy,xytext=xytext,ha=align,color=ink,fontsize=16,
                       arrowprops={"arrowstyle":"-","color":warm,"lw":1.1})
    fig.text(.078,.115,f"Common interval ends at $u$ = {hi:.6f}. Grey = F16 only.  Green = ±5% of the common F16 peak.",
             color=ink,fontsize=18)
    fig.text(.078,.048,f"Maximum gap {r['N_MPa']:.4f} / F16 peak {r['D_MPa']:.4f} MPa = {r['ratio']:.2%}.  "
             "One run per resolution; repeat uncertainty unmeasured.",color=muted,fontsize=17)
    with out.open("xb") as f:
        fig.savefig(f,format="png",dpi=145,facecolor="white")
    plt.close(fig)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    for key in ("archive","json","png"):
        ap.add_argument("--"+key,type=Path,required=True)
    args=ap.parse_args()
    curves=read_curves(args.archive)
    knots,delta,result=calculate(curves)
    with args.json.open("x",encoding="ascii",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True)
        f.write("\n")
    plot(curves,knots,delta,result,args.png)
