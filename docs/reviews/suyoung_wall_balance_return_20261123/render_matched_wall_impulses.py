"""Export four native, matched F12/F24 impulse rows and a weekly figure (Pillow >=10.1)."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin


RETURN = "1f680f4f255910bb2c93ce7e2edea004c89b4177fb3a4b8af93bd59edeab209e"
FINE_RETURN = "c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673"
RELEASE = "0c4eb97d447f9afa984303425e1c5ab221ae9cec"
SCREEN = "e05244fe0c345853234928466b9ae40756cdba54c4408391c39e5141c930cd80"
DIAMETER = .1
STAGES = ("floor", "lid", "contact", "grid_change", "particle_change")
SCOPES = ("all", "bottom_row")
IMPULSES = ("native_floor_impulse", *(f"{s}_{z}" for s in STAGES for z in SCOPES))
BALANCES = ("stage_sum_minus_grid", "grid_minus_particles")
RESIDUALS = tuple(f"{b}_{s}" for b in BALANCES for s in SCOPES)
OBS_COLS = ("step", "displacement_code", "top_gap_before", "floor_gap_before", *IMPULSES)
SNAPSHOTS = (("first_exceedance", (465, 930)), ("early_peak", (569, 1138)))
PLOT_NAME = "weekly_matched_wall_impulses.png"
TABLE_NAME = "matched_wall_impulses.csv"


def check(test, message):
    if not test:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_tar(path, expected):
    raw = path.read_bytes()
    check(sha(raw) == expected, f"input TAR identity: {path}")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as t:
        check(len(t.getnames()) == len(set(t.getnames())), "duplicate TAR path")
        return {m.name: t.extractfile(m).read() for m in t if m.isfile()}


def csv_rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("ascii"), newline="")))


def confirmed_rows(path, fine_path):
    data = read_tar(path, RETURN)
    old = read_tar(fine_path, FINE_RETURN)
    summary = json.loads(data["run/summary.json"])
    prior = json.loads(old["run/summary.json"])
    check(data["run/RELEASE"] == (RELEASE + "\n").encode() and sha(data["run/screen.txt"]) == SCREEN
          and data["run/screen.txt"].splitlines()[-1] == b"COMMAND_RC=0"
          and summary["release"] == RELEASE and summary["previous_tar_sha256"] == FINE_RETURN
          and summary["status"] == "DEVELOPMENT_MATCHED_PREFIX_BALANCE"
          and all(summary[key] is False for key in ("u6_qualified", "stage3_go", "three_dimensional_go")), "scope")
    points = {}
    for arm_i, cells in enumerate((12, 24)):
        prefix = f"run/F{cells}/"
        r = json.loads(data[prefix + "balance_receipt.json"])
        old_r = json.loads(old[prefix + "fine_receipt.json"])
        obs = data[prefix + "wall_impulses.csv"]
        trace = data[prefix + "trace.csv"]
        old_trace = old[prefix + "trace.csv"]
        check(r == summary["arms"][str(cells)] and r["cells"] == cells and r["release"] == RELEASE
              and sha(obs) == r["observer_table_sha256"] and sha(trace) == r["trace_sha256"],
              "balance source receipts")
        check(old_r == prior["arms"][f"F{cells}"] and old_r["trace_sha256"] == sha(old_trace)
              and old_r["result_sha256"] == sha(old[prefix + "result.json"]) and old_r["reached_target"]
              and trace == b"".join(old_trace.splitlines(keepends=True)[:r["steps"] + 2]), "prior trace prefix")
        rows, trajectory = csv_rows(obs), csv_rows(trace)
        check(tuple(rows[0]) == OBS_COLS and len(rows) == r["steps"] == len(trajectory)-1, "observation table")
        width, dt = r["width"], r["dt"]
        scale = 10. / (width * dt)
        for index, (event, steps) in enumerate(SNAPSHOTS):
            step = steps[arm_i]
            native = rows[step-1]
            tr = trajectory[step]
            vals = {k: float(v) for k, v in native.items()}
            check(vals == r["snapshots"][index] and native["step"] == tr["step"] == str(step)
                  and vals["displacement_code"] == width - float(tr["height"]), "matched native row")
            p = 10. * float(tr["bottom_pressure_E"])
            check(math.isclose(scale * vals["native_floor_impulse"], p, abs_tol=1e-14, rel_tol=1e-14),
                  "independent pressure readback")
            row = dict(event=event, cells=cells, step=step, time_code=tr["time_code"], dt_code=dt,
                       width_code=width, displacement_code=native["displacement_code"],
                       displacement_diameters=vals["displacement_code"]/DIAMETER, top_gap_before_code=native["top_gap_before"],
                       floor_gap_before_code=native["floor_gap_before"], native_trace_floor_MPa=p)
            for name in IMPULSES:
                row[name + "_code"] = native[name]
                row[name + "_MPa"] = scale * vals[name]
            for scope in SCOPES:
                # Evaluate the signed residual in native units once, then scale. Stage totals use accurate summation.
                stage_sum = math.fsum(vals[f"{stage}_{scope}"] for stage in ("floor", "lid", "contact"))
                residual1 = stage_sum - vals[f"grid_change_{scope}"]
                residual2 = vals[f"grid_change_{scope}"] - vals[f"particle_change_{scope}"]
                for name, value in zip(BALANCES, (residual1, residual2)):
                    row[f"{name}_{scope}_code"] = value
                    row[f"{name}_{scope}_MPa"] = scale * value
                check(max(abs(residual1), abs(residual2)) <= 2.e-12, "step closure")
            points[event, cells] = row
    for event, _ in SNAPSHOTS:
        a, b = (points[event, g] for g in (12, 24))
        check(float(a["time_code"]) == float(b["time_code"]) and
              a["displacement_code"] == b["displacement_code"], "matched time and displacement")
    return [points[event, g] for event, _ in SNAPSHOTS for g in (12, 24)]


def table(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    raw = stream.getvalue().encode("ascii")
    check(csv_rows(raw) == [{k: str(v) for k, v in row.items()} for row in rows], "CSV round trip")
    return raw


def figure(rows, signature):
    width, height, factor = 1880, 1160, 2
    canvas = Image.new("RGB", (width*factor, height*factor), "white")
    d = ImageDraw.Draw(canvas)
    ink, muted, light = "#152E3D", "#4E6370", "#DBE4E8"
    colors = ("#126D78", "#A24E18")
    fonts = {}

    def xy(point):
        return tuple(round(v*factor) for v in point)

    def text(x, y, s, size=23, fill=ink, anchor="lm", bold=False):
        if size not in fonts:
            fonts[size] = ImageFont.load_default(size=size*factor)
        d.text(xy((x,y)), s, font=fonts[size], fill=fill, anchor=anchor,
               stroke_width=int(bold), stroke_fill=fill)

    def line(x1, y1, x2, y2, color, weight=1):
        d.line((xy((x1,y1)),xy((x2,y2))), fill=color, width=round(weight*factor))

    text(61,62,"Vertical impulse at two matched plate positions",49,bold=True)
    text(64,125,"One native time step per grid. Positive values act upward on the material.",28,muted)
    for index, grid in enumerate(("F12", "F24")):
        x = 65 + 142*index
        line(x,182,x+37,182,colors[index],10)
        text(x+48,182,grid,24,bold=True)
    text(420,182,"Signed impulse per step, expressed as equivalent pressure (MPa)",24,muted)
    headings = ("First 5% exceedance", "Early peak in the four-grid common range")
    terms = (("Floor reaction", "whole material", "native_floor_impulse"),
             ("Lid reaction", "whole material", "lid_all"),
             ("Interbody contact", "bottom row", "contact_bottom_row"),
             ("Momentum change", "bottom-row particles", "particle_change_bottom_row"),
             ("Momentum change", "all particles", "particle_change_all"))
    for j, (label, scope, key) in enumerate(terms):
        y = 358 + j*79
        text(64,y-10,label,26,bold=True)
        text(65,y+19,scope,22,muted)
    for i,title in enumerate(headings):
        selected = rows[i*2:i*2+2]
        left, right = (332, 1000) if i==0 else (1118,1786)
        x = lambda v: left + (v+.2)/.47*(right-left)
        text(left,241,title,29,bold=True)
        value = selected[0]["displacement_diameters"]
        text(left,285,f"{value:.5f} D   |   F12 step {selected[0]['step']:,}   ·   F24 step {selected[1]['step']:,}",22,muted)
        for tick in (-.2, -.1, 0, .1, .2):
            line(x(tick),321,x(tick),720,muted if tick==0 else light,1.5 if tick==0 else 1)
            text(x(tick),744,f"{tick:+.1f}" if tick else "0",22,muted,"mm")
        for j, (_, _, key) in enumerate(terms):
            for k,row in enumerate(selected):
                val = row[key+"_MPa"]
                y = 358+j*79+(-15 if k==0 else 15)
                line(x(0),y,x(val),y,colors[k],9)
                text(x(val)+(8 if val>=0 else -8),y,f"{val:+.3f}",21,colors[k],"lm" if val>=0 else "rm")
        gap = selected[0]["native_trace_floor_MPa"]-selected[1]["native_trace_floor_MPa"]
        text(left,793,f"Floor pressure difference, F12 minus F24   {gap:+.5f} MPa",23,bold=True)
    line(62,831,1818,831,light,2)
    text(64,867,"Momentum closure",30,bold=True)
    text(340,869,"Signed round-off residuals (MPa equivalent)",22,muted)
    colx = (795,1085,1410,1700)
    for j,row in enumerate(rows):
        text(colx[j],909,f"F{row['cells']}  ·  step {row['step']:,}",21,colors[j%2],"mm",True)
    for i,(key,label) in enumerate((
        ("stage_sum_minus_grid_all","Floor + lid + contact minus grid change, all"),
        ("stage_sum_minus_grid_bottom_row","Floor + lid + contact minus grid change, bottom row"),
        ("grid_minus_particles_all","Grid minus particle change, all"),
        ("grid_minus_particles_bottom_row","Grid minus particle change, bottom row"))):
        y=948+i*36
        text(65,y,label,21)
        for j,row in enumerate(rows):
            val=row[key+"_MPa"]
            text(colx[j],y,f"{val:+.2e}" if val else "0",21,ink,"mm")
    line(63,1087,1818,1087,light)
    text(64,1121,"D is the initial disk diameter. Each impulse is multiplied by 10 and divided by its time step and plate width. The bottom row follows the seven initially lowest disks.",21,muted)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("CSV_SHA256", signature)
    meta.add_text("RETURN_SHA256", RETURN)
    out=io.BytesIO()
    canvas.resize((width,height),Image.Resampling.LANCZOS).save(out,format="PNG",pnginfo=meta,dpi=(300,300))
    raw=out.getvalue()
    with Image.open(io.BytesIO(raw)) as image:
        check(image.size == (width,height) and image.info["CSV_SHA256"] == signature and
              image.info["RETURN_SHA256"] == RETURN, "figure proof")
        image.verify()
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("balance_tar","fine_tar","out"):
        parser.add_argument(name,type=Path)
    a = parser.parse_args()
    rows = confirmed_rows(a.balance_tar,a.fine_tar)
    raw = table(rows)
    png = figure(rows,sha(raw))
    a.out.mkdir(parents=True,exist_ok=True)
    for name, data in ((TABLE_NAME,raw),(PLOT_NAME,png)):
        path = a.out/name
        if path.exists():
            check(path.read_bytes()==data,"existing output differs: "+name)
        else:
            with path.open("xb") as f:
                f.write(data)
        print(sha(data),name)


if __name__=="__main__":
    main()
