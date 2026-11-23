"""Render the two material-floor grid pairs from pinned development returns (Pillow >=10.1)."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
import math
import tarfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin


RETURNS = {
    (8, 16): ("aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65", "full_receipt.json"),
    (12, 24): ("c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673", "fine_receipt.json"),
}
DIAMETER = .1
ELASTIC_SCALE_MPA = 10.
FIXED_REFERENCE_MPA = .6636991102836952
TOLERANCE_MPA = FIXED_REFERENCE_MPA / 20.
COLUMNS = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_pair(path, grids):
    expected_hash, receipt_name = RETURNS[grids]
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == expected_hash, "return TAR identity")
    with tarfile.open(path, "r:gz") as tar:
        require(len(tar.getnames()) == len(set(tar.getnames())), "duplicate archive member")
        def get(name):
            item = tar.getmember("run/" + name)
            require(item.isfile(), name)
            return tar.extractfile(item).read()

        summary = json.loads(get("summary.json"))
        saved = summary["comparison"]
        require(saved["fixed_reference_MPa"] == FIXED_REFERENCE_MPA and not summary["u6_qualified"],
                "reference or scope")
        arms = {}
        for cells in grids:
            tag = "F" + str(cells)
            raw = get(tag + "/trace.csv")
            result = get(tag + "/result.json")
            native = json.loads(result)
            receipt = json.loads(get(tag + "/" + receipt_name))
            require(digest(raw) == receipt["trace_sha256"] == native["trace_sha256"]
                    and receipt["result_sha256"] == digest(result) and receipt == summary["arms"][tag]
                    and receipt["cells"] == native["cells"] == cells, "trace-to-receipt binding")
            reader = csv.DictReader(io.StringIO(raw.decode("ascii"), newline=""))
            require(tuple(reader.fieldnames or ()) == COLUMNS, "native columns")
            rows = []
            for i, row in enumerate(reader):
                t, h, p0, phi = (float(row[n]) for n in COLUMNS[1:])
                if i == 0:
                    width = h
                u = width-h
                p = p0*ELASTIC_SCALE_MPA
                require(row["step"] == str(i) and all(math.isfinite(a) for a in (t,h,p,phi))
                        and h > 0. and p >= 0., "invalid native row")
                if i:
                    require(t > rows[-1][1] and u > rows[-1][3] and rows[-1][5] < 1.2, "invalid row sequence")
                else:
                    require(u == t == p == 0., "native origin")
                rows.append((i, t, h, u, u/DIAMETER, p, phi))
            require(len(rows)-1 == native["steps"] and
                    (native["status"] == "TARGET_BRACKETED" and rows[-1][5] >= 1.2 or
                     native["status"] == "GEOMETRY_LIMIT" and rows[-1][5] < 1.2), "native terminal")
            arms[cells] = rows
    return arms, saved


def pair_gap(arms, grids, saved):
    a, b = grids
    travel = {c:[row[3] for row in arms[c]] for c in grids}
    end = min(d[-1] for d in travel.values())
    knots = sorted({v for d in travel.values() for v in d if v <= end})
    def at(c, u):
        xx = travel[c]
        i = bisect_left(xx, u)
        if xx[i] == u:
            return arms[c][i][5]
        w = (u-xx[i-1]) / (xx[i]-xx[i-1])
        p0, p1 = arms[c][i-1][5], arms[c][i][5]
        return p0+w*(p1-p0)
    worst = max(((u,at(a,u),at(b,u)) for u in knots), key=lambda k: abs(k[1]-k[2]))
    gap = abs(worst[1]-worst[2])
    require(saved["common"]["samples"] == len(knots) and math.isclose(
        saved["common"]["max_abs_difference_MPa"], gap, rel_tol=1e-13), "raw gap vs saved readback")
    return (worst[0]/DIAMETER,*worst[1:]), gap, [(u/DIAMETER,at(b,u)) for u in knots]


def table(sets):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(("cells_per_disk_diameter", "step", "time_code", "platen_height_code",
                     "displacement_code", "displacement_disk_diameters", "bottom_pressure_MPa", "phi_m"))
    for pair, arms in sets.items():
        for c in pair:
            writer.writerows((c,*r) for r in arms[c])
    return stream.getvalue().encode("ascii")


def draw_plot(sets, diagnostics, table_sha, out):
    width, height, scale = 1840, 920, 2
    canvas = Image.new("RGB", (width*scale,height*scale), "white")
    draw = ImageDraw.Draw(canvas)
    ink, muted, rule, coarse, fine, band = "#142F3B", "#435962", "#DFE5E7", "#066A73", "#BA4F20", "#F8DFBD"
    def xy(point):
        return tuple(v*scale for v in point)
    def line(points, color, weight=1):
        draw.line([xy(p) for p in points], fill=color, width=round(weight*scale), joint="curve")
    def dash(points, color, weight=3, pattern=(13., 7.)):
        remaining, paint = pattern[0], True
        for a,b in zip(points,points[1:]):
            dx, dy = b[0]-a[0], b[1]-a[1]
            length, offset = math.hypot(dx,dy), 0.
            while offset < length:
                chunk = min(remaining, length-offset)
                if paint:
                    line([(a[0]+dx*offset/length,a[1]+dy*offset/length),
                          (a[0]+dx*(offset+chunk)/length,a[1]+dy*(offset+chunk)/length)],color,weight)
                remaining -= chunk
                offset += chunk
                if remaining < 1e-10:
                    paint = not paint
                    remaining = pattern[0] if paint else pattern[1]
    def txt(point,s,size,anchor="la",color=ink,bold=False):
        draw.text(xy(point), s, font=ImageFont.load_default(size=scale*size), anchor=anchor,
                  fill=color, stroke_width=int(bold), stroke_fill=color)
    txt((72,32), "Bottom pressure across four grid resolutions", 47, bold=True)
    txt((74,96), "Material-surface floor rule  |  One development run per grid", 26,color=muted)
    line([(76,159),(134,159)],coarse,3.5)
    txt((149,159),"Coarser grid",26,"lm")
    dash([(435,159),(493,159)],fine)
    txt((508,159),"Finer grid",26,"lm")
    draw.rectangle([xy((803,149)),xy((850,169))], fill=band)
    txt((864,159),"Fixed 5% band around the finer curve",26,"lm")
    xmax = math.ceil(4.*max(r[-1][4] for arms in sets.values() for r in arms.values()))/4.
    ymax = max(1.26, max(row[5] for arms in sets.values() for r in arms.values() for row in r)+.04)
    top, bottom, span = 308, 715, 699
    for left, (grids, arms) in zip((145,1035), sets.items()):
        a,b = grids
        (uu,pa,pb), gap, fine_common = diagnostics[grids]
        right = left+span
        x = lambda u: left+u/xmax*span
        y = lambda p: bottom-p/ymax*(bottom-top)
        txt((left,216),f"{a} vs {b} cells per disk diameter",32,bold=True)
        txt((left,262),f"Largest grid gap: {gap:.3f} MPa  ({gap/FIXED_REFERENCE_MPA:.1%} of reference)",24,color=muted)
        for i in range(int(xmax*4)+1):
            v = i/4.
            line([(x(v),bottom),(x(v),bottom+8)],muted)
            txt((x(v),bottom+15),f"{v:.2f}",23,"ma",muted)
        for i in range(6):
            v=i/4.
            if i:
                line([(left,y(v)),(right,y(v))],rule)
            line([(left-7,y(v)),(left,y(v))],muted)
            txt((left-17,y(v)),f"{v:.2f}",23,"rm",muted)
        polygon = [(x(u),y(p+TOLERANCE_MPA)) for u,p in fine_common]
        polygon += [(x(u),y(max(0.,p-TOLERANCE_MPA))) for u,p in reversed(fine_common)]
        draw.polygon([xy(p) for p in polygon],fill=band)
        line([(left,top),(left,bottom),(right,bottom)],muted,1.5)
        for c,color in ((a,coarse),(b,fine)):
            pts = [(x(r[4]),y(r[5])) for r in arms[c]]
            (line if c==a else dash)(pts,color,3.2)
            px,py=pts[-1]
            draw.ellipse([xy((px-4,py-4)),xy((px+4,py+4))],fill=color)
        dash([(x(uu),y(pa)),(x(uu),y(pb))],ink,1.8,(5.,5.))
        txt(((left+right)/2,772),"Plate displacement (disk diameters)",27,"ma")
        axis=Image.new("RGBA",(410*scale,55*scale))
        ImageDraw.Draw(axis).text((3*scale,2*scale),"Bottom pressure (MPa)",font=ImageFont.load_default(size=27*scale),fill=ink)
        axis=axis.crop(axis.getbbox()).rotate(90,expand=True)
        canvas.paste(axis,(round((left-106)*scale),round((top+bottom)*scale/2-axis.height/2)),axis)
    txt((74,850),"The band spans ±0.03318 MPa across each pair's shared range. Dotted bars mark the largest difference at the same plate displacement.",23,color=muted)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("CSV_SHA256",table_sha)
    canvas.resize((width,height),Image.Resampling.LANCZOS).save(out,pnginfo=meta,dpi=(300,300))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for n in ("coarse_tar","fine_tar","out"):
        parser.add_argument(n,type=Path)
    args = parser.parse_args()
    sets, diagnostics = {}, {}
    for grids, path in zip(RETURNS,(args.coarse_tar,args.fine_tar)):
        arms, saved = read_pair(path,grids)
        sets[grids] = arms
        diagnostics[grids] = pair_gap(arms,grids,saved)
    args.out.mkdir(parents=True,exist_ok=True)
    raw=table(sets)
    csv_path=args.out/"four_grids_pressure_displacement.csv"
    if csv_path.exists():
        require(csv_path.read_bytes()==raw,"existing CSV mismatch")
    else:
        csv_path.write_bytes(raw)
    png=args.out/"weekly_four_grids_pressure_displacement.png"
    draw_plot(sets,diagnostics,digest(raw),png)
    with Image.open(png) as img:
        require(img.info["CSV_SHA256"]==digest(raw),"PNG metadata")
        img.verify()
    for grids, arms in sets.items():
        print(grids,[len(arms[c]) for c in grids],diagnostics[grids][:2])
    print("CSV",digest(raw),"PNG",digest(png.read_bytes()))


if __name__ == "__main__":
    main()
