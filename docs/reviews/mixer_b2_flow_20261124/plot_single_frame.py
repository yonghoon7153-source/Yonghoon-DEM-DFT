"""One native B2-U cross-section; check the quantile line against dense surface columns."""
import argparse
import gzip
import hashlib
import io
import json
import re
import tarfile
from math import atan, degrees, hypot
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


R = .01258325
STRIDE = 32976
PATTERN = re.compile(r"PRECAL_R1_B2_U/post/mix_([0-9]+)\.liggghts")


def first_native(archive_path, provenance, subset):
    hashes = {item["step"]: item["sha256"] for item in provenance["observed_steps_sha256"]}
    with gzip.open(archive_path, "rb") as raw:
        with tarfile.open(fileobj=raw, mode="r|", bufsize=1024**2) as tar:
            for member in tar:
                m = PATTERN.fullmatch(member.name)
                if not m or int(m[1]) not in subset:
                    continue
                step = int(m[1])
                if not member.isfile() or member.size > 256 * 1024**2:
                    raise ValueError("Invalid native member")
                content = tar.extractfile(member).read()
                digest = hashlib.sha256(content).hexdigest()
                if digest != hashes[step]:
                    raise ValueError("Single frame changed")
                return step, digest, content
    raise ValueError("No second-turn native frame")


def lines(data):
    mid = abs(data[:,2]) <= .001258325
    y, z, radius = (data[mid, i] / R for i in [3, 4, 11])
    columns = []
    zedges = np.arange(-1.10,1.101,.035)
    yedges = np.linspace(-.6,.6,16)
    for lo, hi in zip(yedges,yedges[1:]):
        select = (y >= lo) & (y < hi)
        if np.sum(select) < 8:
            continue
        zz, rr = z[select], radius[select]
        area = np.histogram(zz, zedges, weights=rr**2)[0]
        count = np.histogram(zz, zedges)[0]
        nonempty = area[area > 0]
        dense = (count >= 3) & (area >= .15 * np.percentile(nonempty, 90))
        run_ends = np.where(dense[:-2] & dense[1:-1] & dense[2:])[0] + 2
        dense_top = zedges[run_ends[-1] + 1] if len(run_ends) else None
        tops = np.quantile(zz+rr, [.985,.99,.995])
        columns.append(((lo+hi)/2,*tops,dense_top))
    return mid, columns


def fit(points):
    p = np.asarray(points)
    i,j = np.triu_indices(len(p),1)
    slope = np.median((p[j,1]-p[i,1])/(p[j,0]-p[i,0]))
    intercept = np.median(p[:,1] - slope*p[:,0])
    return float(slope), float(intercept)


def draw_figure(data, mid, cols, fit_line, dense_line, rec, path):
    s,b = fit_line
    img = Image.new("RGB", (1500,1050), "white")
    d=ImageDraw.Draw(img)
    def font(size, bold=False):
        for filename in (("arialbd.ttf" if bold else "arial.ttf"),
                         ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")):
            try:
                return ImageFont.truetype(filename, size)
            except OSError:
                pass
        return ImageFont.load_default(size=size)
    def text(x,y,t,size=24,color="#192936",bold=False):
        d.text((x,y),t,font=font(size,bold),fill=color)
    def xy(y,z):
        return 506+390*y,536-390*z
    text(45,20,"B2-U   |   Cross-section during the second turn",43,bold=True)
    text(47,83,f"Frame {rec['frame_index']}   /   Step {rec['step']:,}   /   {rec['turns_since_rotation']:.3f} revolutions",25)
    for tick in (-1,-.5,0,.5,1):
        x, y = xy(tick,-1.05); d.line((x,y,x,y+9),fill="#617181",width=2)
        d.text((x,y+28),f"{tick:g}",fill="#405466",font=font(19),anchor="mm")
        x,y=xy(-1.05,tick); d.line((x-9,y,x,y),fill="#617181",width=2)
        d.text((x-14,y),f"{tick:g}",fill="#405466",font=font(19),anchor="rm")
    d.line((xy(-1.05,1.03),xy(-1.05,-1.05),xy(1.03,-1.05)),fill="#617181",width=2)
    d.ellipse((xy(-1,1),xy(1,-1)),outline="#304555",width=3)
    # Draw full physical radii in x order so nearer particle disks occlude farther ones.
    colors = {1:"#8798A6",2:"#9EADB6",3:"#607684"}
    particles = data[mid]
    for p in particles[np.argsort(particles[:,2])]:
        x,y=xy(p[3]/R,p[4]/R); rr=390*p[11]/R
        d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=colors[int(p[1])])
    d.line((xy(-.60,b-.60*s),xy(.60,b+.60*s)),fill="#BB4C00",width=5)
    for yc,_,zt,_,zc in cols:
        x,y=xy(yc,zt); d.ellipse((x-4,y-4,x+4,y+4),fill="#FFB169",outline="#823500",width=2)
        if zc is not None:
            x,y=xy(yc,zc); d.line((x-5,y,x+5,y),fill="#163EB6",width=3)
    norm=hypot(1,s)
    uu=rec["delta_over_R"]
    start=np.array(xy(0,b))
    finish=np.array(xy(uu*s/norm,b-uu/norm))
    d.line((tuple(start),tuple(finish)),fill="#5A1359",width=5)
    v=(finish-start)/np.linalg.norm(finish-start); n=np.array([-v[1],v[0]])
    d.polygon([tuple(finish),tuple(finish-18*v+8*n),tuple(finish-18*v-8*n)],fill="#5A1359")
    text(396,1000,"Horizontal position y/R",24)
    text(52,117,"Height z/R",22)
    text(955,190,"Fitted surface",31,bold=True)
    text(955,242,"Orange: 99th percentile of",23);text(955,273,"sphere tops in each column.",23)
    text(955,335,f"Signed angle  {rec['theta_signed_deg']:+.2f} degrees",26,color="#9C470A",bold=True)
    text(955,390,"Blue: upper edge of dense rows",23); text(955,421,"in a separate occupancy screen.",23)
    text(955,477,f"Dense-edge angle  {degrees(atan(dense_line[0])):+.2f} degrees",24,color="#163EB6",bold=True)
    text(955,567,"Depth into moving layer",31,bold=True)
    text(955,625,f"Purple arrow  {uu:.3f} R  /  {uu*R*1000:.2f} mm",23,color="#5A1359",bold=True)
    text(955,680,"Velocity is averaged within",23);text(955,711,"a central span along the surface.",23)
    text(955,820,"Projection of particle disks in the",22); text(955,852,"middle half of the drum width.",22)
    img.save(path)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("archive",type=Path); ap.add_argument("readback",type=Path); ap.add_argument("outdir",type=Path)
    a=ap.parse_args()
    if a.outdir.exists():
        raise ValueError("Choose a new output directory")
    provenance=json.loads((a.readback/"provenance.json").read_text(encoding="utf-8"))
    records=[json.loads(s) for s in (a.readback/"frames.jsonl").read_text(encoding="utf-8").splitlines()]
    eligible={r["step"]:r for r in records if r["phase"]=="TURN_1_TO_2" and r["layer_status"]=="RESOLVED"}
    step,sha,content=first_native(a.archive,provenance,eligible)
    rec=eligible[step]
    if int(content.split(b"\n",2)[1])!=step:
        raise ValueError("Wrong native step")
    data=np.loadtxt(io.BytesIO(content),skiprows=9,comments=None)
    if len(data)!=rec["atom_count"]:
        raise ValueError("Wrong native atom count")
    mid,cols=lines(data)
    s,b=fit([(v[0],v[2]) for v in cols])
    dense=[(v[0],v[4]) for v in cols if v[4] is not None]
    sd,bd=fit(dense)
    if abs(degrees(atan(s))-rec["theta_signed_deg"])>1e-9:
        raise ValueError("Observer angle mismatch")
    offsets=[v[2]-v[4] for v in cols if v[4] is not None]
    nums=dict(step=step,frame_index=rec["frame_index"],sha256=sha,N=len(data),mid_slab=int(mid.sum()),
              turn=rec["turns_since_rotation"],theta_degrees=degrees(atan(s)),
              dense_edge_theta_degrees=degrees(atan(sd)),delta_over_R=rec["delta_over_R"],
              qminusdense_median_R=float(np.median(offsets)),qminusdense_absmax_R=float(np.max(np.abs(offsets))),
              quantile_angles=rec["surface_q_sensitivity_deg"],dense_columns=len(dense),
              q99_columns=len(cols),native_threshold_bracket_R=rec["layer_sensitivity"][1]["bracket_over_R"])
    a.outdir.mkdir(parents=True)
    draw_figure(data,mid,cols,(s,b),(sd,bd),rec,a.outdir/"b2_u_cross_section.png")
    (a.outdir/"frame_check.json").write_text(json.dumps(nums,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(nums))


if __name__=="__main__":
    main()
