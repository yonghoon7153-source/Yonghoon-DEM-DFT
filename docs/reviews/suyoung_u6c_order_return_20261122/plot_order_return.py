"""Plot the recorded F8 original and reversed-ID loading traces at native steps."""
import argparse
import csv
import hashlib
import io
from pathlib import Path
import tarfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def trace(path, digest, member):
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != digest:
            raise ValueError("Return archive SHA256 mismatch")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            raw = archive.extractfile(member).read().decode("ascii")
    rows = list(csv.DictReader(io.StringIO(raw, newline="")))
    reference_height = float(rows[0]["height"])
    u = [reference_height - float(r["height"]) for r in rows]
    pressure = [10 * float(r["bottom_pressure_E"]) for r in rows]
    return u, pressure


def render(wall_path, reverse_path, png):
    x, p = trace(wall_path, "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90",
                 "run/arms/F8/trace.csv")
    xr, pr = trace(reverse_path, "8e76ec686e8f384c28c42b5c5304d25256096f0568fe999d602bdec307991e17",
                   "run/F8_RELABEL/trace.csv")
    if x[:len(xr)] != xr or len(x) <= len(xr):
        raise ValueError("Expected the reversed trace on the exact prefix of the native grid")
    difference = [a-b for a, b in zip(p, pr)]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16, "axes.labelsize": 19,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.linewidth": 1.0, "path.simplify": False})
    fig, (ax, dx) = plt.subplots(1, 2, sharex=True, figsize=(15.6, 7.3))
    fig.subplots_adjust(left=.079, right=.982, bottom=.23, top=.775, wspace=.29)
    fig.text(.079, .926, "Changing particle ID order in F8 loading", fontsize=29, weight="bold")
    fig.text(.079, .86, "Development calculation   /   Same seed and grid, two ID orders",
             fontsize=18, color="#37494d")
    blue, red, ink = "#146797", "#b24c23", "#293c50"
    for panel in (ax, dx):
        panel.set_axisbelow(True)
        panel.grid(axis="y", color="#d1d7da", linewidth=.7)
        panel.axvspan(xr[-1], x[-1], facecolor="#e4e9ec", zorder=0)
        panel.axvline(xr[-1], linestyle=(0,(3,3)), color="#67747c", linewidth=1.2)
        panel.set_xlim(0, .1185)
        panel.xaxis.set_major_locator(MultipleLocator(.025))
        panel.set_xlabel("Plate displacement, $u$ (dimensionless)")
    ax.set_title("Bottom-plate pressure", loc="left", fontsize=21, weight="bold", pad=10)
    ax.plot(x, p, color=blue, label="Original IDs", lw=2.8)
    ax.plot(xr, pr, color=red, label="Reversed IDs", ls="--", lw=2.3)
    ax.plot(x[-1], p[-1], "o", color=blue, ms=6)
    ax.plot(xr[-1], pr[-1], "o", color=red, ms=6)
    ax.set_ylabel("Pressure (MPa)")
    ax.set_ylim(-.023, 1.27)
    ax.legend(loc="upper left", frameon=False, fontsize=16)
    dx.set_title("Original minus reversed", loc="left", fontsize=21, weight="bold", pad=10)
    dx.axhline(0,color="#728187",lw=.9)
    dx.plot(xr, difference, lw=2.1, color=ink)
    dx.plot(xr[-1], difference[-1], "o", color=ink, ms=6)
    dx.annotate(f"{difference[-1]:.4f} MPa".replace("-", "−"),
                xy=(xr[-1], difference[-1]), xycoords="data",
                xytext=(.047,-.08), textcoords="data",
                arrowprops={"arrowstyle":"->","color":ink,"lw":1.1},
                fontsize=17, color=ink)
    dx.set_ylabel("Pressure difference (MPa)")
    dx.set_ylim(-.101, .009)
    dx.yaxis.set_major_locator(MultipleLocator(.025))
    fig.text(.079, .097,
             f"Reversed IDs end at $u$ = {xr[-1]:.6f} (step {len(xr)-1:,}).  "
             f"Original IDs reach the fixed point at $u$ = {x[-1]:.6f} (step {len(x)-1:,}).",
             fontsize=15)
    fig.text(.079, .045, "The shaded interval contains observations from the original run alone.",
             fontsize=15, color="#37494d")
    with png.open("xb") as stream:
        fig.savefig(stream, format="png", dpi=160, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("wall", "reverse", "png"):
        parser.add_argument(argument, type=Path)
    args = parser.parse_args()
    render(args.wall, args.reverse, args.png)
