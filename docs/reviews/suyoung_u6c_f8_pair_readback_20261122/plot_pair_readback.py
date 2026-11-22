"""Draw four recorded F8 curves and compare the two ID effects on their common grid."""
import argparse
import csv
import hashlib
import io
import tarfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator


WALL = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
ORDER = "8e76ec686e8f384c28c42b5c5304d25256096f0568fe999d602bdec307991e17"
PAIR = "9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b"


def curves(path, expected, members):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("input archive mismatch")
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        answer = []
        for member in members:
            text = archive.extractfile(member).read().decode("ascii")
            rows = list(csv.DictReader(io.StringIO(text)))
            height = np.array([float(row["height"]) for row in rows])
            pressure = 10.0 * np.array([float(row["bottom_pressure_E"]) for row in rows])
            answer.append((height[0] - height, pressure))
    return answer


def render(wall, order, pair, png):
    old_orig, = curves(wall, WALL, ["run/arms/F8/trace.csv"])
    old_rev, = curves(order, ORDER, ["run/F8_RELABEL/trace.csv"])
    orig, rev = curves(pair, PAIR, ["run/ORIGINAL/trace.csv", "run/REVERSED/trace.csv"])
    n = min(len(u) for u, _ in (old_orig, old_rev, orig, rev))
    u = old_orig[0][:n]
    if any(not np.array_equal(x[:n], u) for x, _ in (old_rev, orig, rev)):
        raise ValueError("not a common displacement grid")
    old_delta = old_orig[1][:n] - old_rev[1][:n]
    new_delta = orig[1][:n] - rev[1][:n]
    warm, light, cool, ink, muted = "#a34818", "#c47a43", "#155b87", "#173242", "#465c67"
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":20,
                         "axes.spines.top":False, "axes.spines.right":False,
                         "axes.labelcolor":ink, "xtick.color":muted, "ytick.color":muted,
                         "axes.edgecolor":"#74848a", "path.simplify":False})
    fig, (left, right) = plt.subplots(1,2, figsize=(18.4,8.1))
    fig.subplots_adjust(left=.079, right=.982, bottom=.232, top=.765, wspace=.32)
    fig.text(.079,.924,"Particle ID order in F8 compression",size=29,weight="bold",color=ink)
    fig.text(.079,.855,"One initial packing   /   Two contact solvers   /   Development calculation",
             color=muted,size=20)
    for ax, title in ((left,"Bottom-plate pressure"),(right,"Original minus reversed IDs")):
        ax.set_title(title,loc="left",fontsize=22,color=ink,pad=15,weight="semibold")
        ax.set_axisbelow(True)
        ax.grid(axis="y",linewidth=.8,color="#dae0e3")
        ax.xaxis.set_major_locator(MultipleLocator(.025))
        ax.set_xlabel("Plate displacement, $u$ (dimensionless)",labelpad=10)
    left.set_ylabel("Pressure (MPa)")
    left.axvspan(u[-1],orig[0][-1],color="#eef2f4",zorder=0)
    left.axvline(u[-1],color="#819099",lw=1.3,ls=":")
    for (x,y),color,style,width,label in (
        (old_orig,warm,"-",2.7,"Previous · original"),
        (old_rev,light,"--",2.7,"Previous · reversed"),
        (orig,cool,"-",4.0,"Updated · original"),
        (rev,"#a6cbdc",(0,(3,5)),1.9,"Updated · reversed")):
        left.plot(x,y,color=color,linestyle=style,lw=width,label=label)
    left.set_xlim(-.001,.121)
    left.set_ylim(-.04,1.26)
    left.legend(loc="upper left",fontsize=16.5,frameon=False,labelcolor=ink)
    right.set_ylabel("Pressure difference (MPa)")
    right.plot(u,new_delta,color=cool,lw=3.2)
    right.plot(u,old_delta,color=warm,lw=2.4)
    right.set_xlim(-.001,u[-1]+.003)
    right.set_ylim(-.103,.022)
    right.yaxis.set_major_locator(MultipleLocator(.025))
    right.annotate("Previous", xy=(u[-1],old_delta[-1]),xytext=(.070,-.086),
                   arrowprops={"arrowstyle":"-","color":warm},color=warm,fontsize=18)
    right.text(.046,.006,"Updated",color=cool,fontsize=18)
    fig.text(.079,.090,f"Common interval: {n:,} native samples to $u$ = {u[-1]:.6f}.  "
             "Shading marks later observations.",fontsize=18,color=ink)
    peak_new = np.max(abs(new_delta))
    mantissa, exponent = f"{peak_new:.2e}".split("e")
    fig.text(.079,.032,"Maximum absolute ID difference in that interval:  "
             +f"{np.max(abs(old_delta)):.5f} MPa (previous)  /  "
             +rf"${mantissa}\,\times\,10^{{{int(exponent)}}}$ MPa (updated).",fontsize=18,color=ink)
    with png.open("xb") as stream:
        fig.savefig(stream,format="png",dpi=145,facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("wall","order","pair","png"):
        parser.add_argument(name,type=Path)
    a = parser.parse_args()
    render(a.wall,a.order,a.pair,a.png)
