"""Draw the original F8/F16 common loading interval from three fixed returns."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
from pathlib import Path
import tarfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def members(path, digest, *names):
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != digest:
            raise ValueError("Unexpected return file")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            return [archive.extractfile("run/" + name).read() for name in names]


def curve(raw):
    rows = list(csv.DictReader(io.StringIO(raw.decode("ascii"), newline="")))
    width = float(rows[0]["height"])
    x = [width - float(r["height"]) for r in rows]
    p = [10 * float(r["bottom_pressure_E"]) for r in rows]
    return x, p


def linear(curve, u):
    x, p = curve
    i = bisect_left(x, u)
    if i >= len(x) or u < x[0]:
        raise ValueError("Requested displacement outside measured support")
    if x[i] == u:
        return p[i]
    t = (u-x[i-1])/(x[i]-x[i-1])
    return p[i-1] + t*(p[i]-p[i-1])


def render(wall, half, dense, output):
    c, f = members(wall, "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90",
                   "arms/F8/trace.csv", "arms/F16/trace.csv")
    h, = members(half, "e574396d010514b3cd77f57d2e06d0c25227c88a7b6e985577f2981aa8c154e4",
                 "F8_HALF/trace.csv")
    d, summary = members(dense, "96205a44f9bf5eaa4439a536d4044570337b3f88362b30ff281b4fa0e8d0a409",
                         "F8_DENSE/trace.csv", "seed_summary.json")
    curves = [curve(raw) for raw in (c,h,d,f)]
    anchor = json.loads(summary)["comparison"]["fixed_u"]
    if anchor != min(end[-1] for end, _ in curves):
        raise ValueError("Original common loading interval changed")
    u = sorted({x for axis, _ in curves for x in axis if x <= anchor})
    if len(u) != 5157:
        raise ValueError("Unexpected native displacement set")
    signals = [[linear(s, knot) for knot in u] for s in curves]
    contrasts = [[a-b for a,b in zip(first,second)] for first,second in zip(signals,signals[1:])]

    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":17, "axes.labelsize":21,
                         "xtick.labelsize":17, "ytick.labelsize":17, "axes.linewidth":1.1,
                         "axes.spines.top":False, "axes.spines.right":False, "path.simplify":False})
    fig, (left, right) = plt.subplots(1, 2, figsize=(16.5,8.6))
    fig.subplots_adjust(left=.073,right=.975,top=.77,bottom=.23,wspace=.29)
    fig.text(.073,.94,"Grid, material-point sampling and time step",fontsize=30,weight="bold")
    fig.text(.073,.885,"F loading   /   One development trajectory per configuration",fontsize=19,color="#34444b")
    left.set_title("Bottom-plate pressure",loc="left",fontsize=22,weight="bold",pad=12)
    right.set_title("Signed pressure differences",loc="left",fontsize=22,weight="bold",pad=12)
    specs = [
        ("8 / sparse / full step", "#754392","-"),
        ("8 / sparse / half step", "#d27919","--"),
        ("8 / dense / half step", "#007676","-."),
        ("16 / dense / half step","#314c8c","-"),
    ]
    for series,(label,col,style) in zip(signals,specs):
        left.plot(u,series,label=label,color=col,linestyle=style,linewidth=2.0)
        left.plot(anchor,series[-1],"o",ms=4.5,color=col)
    differences = [
        ("Time step   (full − half)", "#754392","--"),
        ("Sampling   (sparse − dense)", "#d27919","-."),
        ("Grid   (8 − 16)", "#007676","-"),
    ]
    for series,(label,col,style) in zip(contrasts,differences):
        right.plot(u,series,label=label,color=col,linestyle=style,linewidth=2.0)
        right.plot(anchor,series[-1],"o",ms=4.5,color=col)
    left.legend(loc="upper left",title="Cells per diameter / seed / time step",title_fontsize=15,
                fontsize=15,frameon=False,handlelength=2.4,borderpad=.12)
    right.legend(loc="upper left",fontsize=16,frameon=False,handlelength=2.4,borderpad=.12)
    for ax in (left,right):
        ax.axhline(0,color="#7d8589",lw=.9,zorder=0)
        ax.grid(axis="y",color="#c4cbce",lw=.6,alpha=.7)
        ax.set_axisbelow(True)
        ax.xaxis.set_major_locator(MultipleLocator(.025))
        ax.set_xlim(0,anchor*1.03)
        ax.set_xlabel("Plate displacement, $u$ (dimensionless)",labelpad=9)
        ax.set_ylabel("Pressure (MPa)" if ax is left else "Pressure difference (MPa)",labelpad=6)
    fig.text(.073,.096,"Sparse seed: 9,653 points    ·    Dense seed: 39,053 points    ·    49 disks in all four cases",fontsize=16)
    fig.text(.073,.049,"Original shared interval ends at $u$ = 0.115623.  Lines use native samples and linear interpolation at matched displacements.",fontsize=15)
    with output.open("xb") as stream:
        fig.savefig(stream,format="png",dpi=160,facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for item in ("wall","half","dense","output"):
        parser.add_argument(item, type=Path)
    opts = parser.parse_args()
    render(opts.wall, opts.half, opts.dense, opts.output)
