"""Render four native pressure curves from two completed, pinned author returns.

Run with Python and Pillow >= 10.1. The bundled default scalable typeface is used.
The CSV contains native samples only. Interpolation is limited to calculating and
displaying the grid discrepancy on the common interval within each model.
"""
import argparse
from bisect import bisect_left
import csv
from hashlib import sha256
import io
import json
import math
from pathlib import Path
import tarfile

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

OLD_HASH = "fc685932f4a1710fe944c5d2dafbcb56bf239f473184f009983a3ff4805dabea"
NEW_HASH = "aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65"
DIAMETER = 0.1
ELASTIC_SCALE_MPA = 10.0
REFERENCE_MPA = 0.6636991102836952
THRESHOLD = REFERENCE_MPA / 20
COLUMNS = ["step", "time_code", "height", "bottom_pressure_E", "phi_m"]
MODELS = ("previous", "revised")
GRIDS = (8, 16)


def require(ok, text):
    if not ok:
        raise ValueError(text)


def read_return(path, expected_hash, model):
    require(sha256(path.read_bytes()).hexdigest() == expected_hash, f"{model} outer hash")
    result = {}
    with tarfile.open(path, "r:gz") as tar:
        def member(name):
            entry = tar.getmember("run/" + name)
            require(entry.isfile(), name)
            return tar.extractfile(entry).read()

        require(len(tar.getnames()) == len(set(tar.getnames())), "duplicate TAR member")
        for cells in GRIDS:
            folder = f"F{cells}/"
            raw = member(folder + "trace.csv")
            native = json.loads(member(folder + "result.json"))
            require(native["cells"] == cells and native["status"] == "TARGET_BRACKETED" and
                    native["trace_sha256"] == sha256(raw).hexdigest(), "native receipt")
            if model == "revised":
                cert = json.loads(member(folder + "full_receipt.json"))
                require(cert["result_sha256"] == sha256(member(folder + "result.json")).hexdigest()
                        and cert["trace_sha256"] == sha256(raw).hexdigest() and cert["reached_target"],
                        "revised receipt")
            reader = csv.DictReader(io.StringIO(raw.decode("ascii"), newline=""))
            require(reader.fieldnames == COLUMNS, "native columns")
            arm = []
            for step, row in enumerate(reader):
                t, h, p_e, phi = (float(row[k]) for k in COLUMNS[1:])
                if step == 0:
                    h0 = h
                u = h0 - h
                p = ELASTIC_SCALE_MPA * p_e
                require(step == int(row["step"]) and all(math.isfinite(v) for v in (t,h,p,phi))
                        and h > 0.0 and p >= 0.0, "nonfinite or invalid native point")
                if step:
                    require(t > arm[-1][1] and u > arm[-1][3] and arm[-1][5] < 1.2, "native bounds")
                else:
                    require(t == u == p == 0.0, "native origin")
                arm.append((step, t, h, u, u / DIAMETER, p, phi))
            require(len(arm) == native["steps"] + 1 and arm[-1][5] >= 1.2, "native terminal")
            result[cells] = arm
    return result


def readout(arms, end=None):
    x = {k: [r[3] for r in rows] for k, rows in arms.items()}
    own_end = min(a[-1] for a in x.values())
    if end is None:
        end = own_end
    require(0 < end <= own_end and any(end in points for points in x.values()), "comparison endpoint")
    knots = sorted({v for a in x.values() for v in a if v <= end})

    def pressure(cells, u):
        xs = x[cells]
        j = bisect_left(xs, u)
        if xs[j] == u:
            return arms[cells][j][5]
        fraction = (u - xs[j-1]) / (xs[j] - xs[j-1])
        return arms[cells][j-1][5] + fraction * (arms[cells][j][5] - arms[cells][j-1][5])

    gaps = [(u / DIAMETER, pressure(8, u), pressure(16, u)) for u in knots]
    worst = max(gaps, key=lambda v: abs(v[1] - v[2]))
    gap = abs(worst[1] - worst[2])
    return worst, gap, gap / REFERENCE_MPA


def native_csv(sets):
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(("floor_model", "cells_per_disk_diameter", "step", "time_code", "platen_height_code",
                     "displacement_code", "displacement_disk_diameters", "bottom_pressure_MPa", "phi_m"))
    for model, arms in sets.items():
        for cells, arm in arms.items():
            writer.writerows((model, cells, *row) for row in arm)
    return out.getvalue().encode("ascii")


def dashed(draw, points, fill, width, pattern=(13, 7)):
    paint, remaining = True, pattern[0]
    for a, b in zip(points, points[1:]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        length, offset = math.hypot(dx, dy), 0.
        while offset < length:
            take = min(remaining, length - offset)
            if paint:
                draw.line([(a[0]+dx*offset/length, a[1]+dy*offset/length),
                           (a[0]+dx*(offset+take)/length, a[1]+dy*(offset+take)/length)],
                          fill=fill, width=width)
            remaining -= take
            offset += take
            if remaining < 1e-10:
                paint = not paint
                remaining = pattern[0] if paint else pattern[1]


def figure(sets, table, destination):
    # Coordinates are in pixels on the final 1840 x 908 image.
    w, h = 1840, 908
    scale = 2
    canvas = Image.new("RGB", (w*scale, h*scale), "white")
    draw = ImageDraw.Draw(canvas)
    ink, muted, grid = "#142F3B", "#435962", "#DFE5E7"
    teal, orange, band = "#066A73", "#BA4F20", "#F8DFBD"

    def xy(p):
        return tuple(v*scale for v in p)

    def line(points, color, width=1):
        draw.line([xy(p) for p in points], fill=color, width=round(width*scale), joint="curve")

    def txt(point, content, size, *, color=ink, anchor="la", bold=False):
        draw.text(xy(point), content, fill=color, anchor=anchor,
                  font=ImageFont.load_default(size=size*scale),
                  stroke_width=1 if bold else 0, stroke_fill=color)

    def dash(points, color, width):
        dashed(draw, list(map(xy, points)), color, round(width*scale), pattern=(14*scale, 7*scale))

    txt((73, 36), "Bottom pressure during compression", 48, bold=True)
    txt((75, 97), "Each curve ends when that grid first reaches 1.2 MPa.", 27, color=muted)
    line([(78, 161), (131, 161)], teal, 4)
    txt((145, 160), "8 cells per disk diameter", 25, anchor="lm")
    dash([(477, 161), (534, 161)], orange, 4)
    txt((548, 160), "16 cells per disk diameter", 25, anchor="lm")
    draw.rectangle([xy((927, 150)), xy((975, 170))], fill=band)
    txt((989, 161), "5% band around the 16-cell curve", 25, anchor="lm")

    top, bottom, panel_width = 314, 719, 704
    xstep, xmax = .25, 1.5
    ymax = 1.26
    for model, left in zip(MODELS, (140, 1033)):
        right = left + panel_width
        arms = sets[model]
        worst, gap, fraction = readout(arms)
        x = lambda u: left + u/xmax*panel_width
        y = lambda p: bottom - p/ymax*(bottom-top)
        txt((left, 217), "Previous floor rule" if model == "previous" else "Revised floor rule", 35, bold=True)
        txt((left, 265), f"Largest grid gap: {gap:.3f} MPa  ({fraction:.1%} of reference)",
            25, color=muted)
        for i in range(6):
            v = i*.25
            yy = y(v)
            if i:
                line([(left, yy), (right, yy)], grid)
            line([(left-7, yy), (left, yy)], muted)
            txt((left-17, yy), f"{v:.2f}", 23, color=muted, anchor="rm")
        for i in range(7):
            v = i*xstep
            xx = x(v)
            line([(xx, bottom), (xx, bottom+8)], muted)
            txt((xx, bottom+15), f"{v:.2f}", 23, color=muted, anchor="ma")
        line([(left, top), (left, bottom), (right, bottom)], muted, 1.5)
        # Draw only the part of the 5% band for which there is a coarse observation.
        endpoint = min(arms[8][-1][4], arms[16][-1][4])
        fine = [(r[4], r[5]) for r in arms[16] if r[4] <= endpoint]
        require(fine[-1][0] == endpoint, "unpinned interpolation endpoint")
        polygon = [(x(u), y(p+THRESHOLD)) for u,p in fine]
        polygon.extend((x(u), y(max(0.,p-THRESHOLD))) for u,p in reversed(fine))
        draw.polygon([xy(p) for p in polygon], fill=band)
        for c, color in ((8, teal), (16, orange)):
            points = [(x(r[4]), y(r[5])) for r in arms[c]]
            require(all(left <= px <= right and top <= py <= bottom for px,py in points), "plot bounds")
            if c == 8:
                line(points, color, 3.2)
            else:
                dash(points, color, 3.2)
            xx, yy = points[-1]
            draw.ellipse([xy((xx-4.5,yy-4.5)),xy((xx+4.5,yy+4.5))],fill=color)
        wx, pa, pb = worst
        xx = x(wx)
        dashed(draw,[xy((xx,y(pa)-2)),xy((xx,y(pb)))],ink,3,pattern=(6,6))
        line([(xx-7, y(pb)), (xx+7, y(pb))], ink, 1.3)
        txt(((left+right)/2, 773), "Platen displacement (disk diameters)", 27, anchor="ma")
        axis = Image.new("RGBA", (410*scale, 55*scale), (255,255,255,0))
        ad = ImageDraw.Draw(axis)
        ad.text((3*scale,2*scale), "Bottom pressure (MPa)", font=ImageFont.load_default(size=27*scale), fill=ink)
        axis = axis.crop(axis.getbbox()).rotate(90, expand=True)
        canvas.paste(axis, (round((left-104)*scale), round((top+bottom)*scale/2-axis.height/2)), axis)
    txt((74, 847), "The 5% tolerance is fixed at 0.03318 MPa. Vertical dotted bars mark the largest gap within each pair's shared displacement range.",
        23, color=muted)
    meta=PngImagePlugin.PngInfo()
    meta.add_text("CSV_SHA256", sha256(table).hexdigest())
    canvas.resize((w,h),Image.Resampling.LANCZOS).save(destination, pnginfo=meta, dpi=(300,300))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("previous_tar", "revised_tar", "out"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    curves = {m:read_return(path, digest, m) for m,path,digest in
              zip(MODELS,(args.previous_tar,args.revised_tar),(OLD_HASH,NEW_HASH))}
    args.out.mkdir(parents=True,exist_ok=True)
    table = native_csv(curves)
    path=args.out/"full_pressure_displacement.csv"
    if path.exists():
        require(path.read_bytes() == table,"existing CSV differs")
    else:
        path.write_bytes(table)
    figure(curves,table,args.out/"weekly_full_pressure_displacement.png")
    four_curve_end = min(arm[-1][3] for arms in curves.values() for arm in arms.values())
    for model,arms in curves.items():
        print(model, [len(a) for a in arms.values()], "pair support", readout(arms))
        print(model, "common four-curve support", readout(arms, four_curve_end))


if __name__ == "__main__":
    main()
