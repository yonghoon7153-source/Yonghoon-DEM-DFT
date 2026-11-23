"""Build the matched-endpoint depth figure from the frozen return, without a model import."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import tarfile
import tempfile

from PIL import Image, PngImagePlugin


SOURCE = "cd9b0e6b9ce31719716b3ae4b9f97734a7a4ba3614c7de7bd3d93d44f3be83e6"
PIN = "9638542795ed98edf8b1c9ac52d88c3a0e2f8f3b"
REFERENCE = 0.6636991102836952
NAMES = ("lower", "middle", "upper", "whole")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    check(digest(raw) == SOURCE, "unexpected return digest")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        def file(name):
            key = "run/" + name
            check(archive.getnames().count(key) == 1 and archive.getmember(key).isfile(), key)
            return archive.extractfile(key).read()

        report = json.loads(file("summary.json"))
        check(file("RELEASE").decode().strip() == report["release"] == PIN, "release")
        check(report["status"] == "DEPTH_PREFIX_COMPLETE" and report["u6_qualified"] is False, "scope")
        grids = {}
        for cell, steps in ((12,555), (24,1110)):
            arm = report["arms"][str(cell)]
            data = {}
            for filename, field in (("trace","trace_sha256"), ("layer_steps","layer_sha256")):
                content = file(f"F{cell}/{filename}.csv")
                check(digest(content) == arm[field], filename)
                data[filename] = list(csv.DictReader(io.StringIO(content.decode("ascii"))))
            traces = data["trace"]
            layers = data["layer_steps"]
            check(len(traces) == steps + 1 and len(layers) == steps, "incomplete grid")
            width = float(traces[0]["height"])
            dt = float(traces[1]["time_code"])
            series = {}
            for step, (trace, layer) in enumerate(zip(traces[1:],layers,strict=True), 1):
                check(trace["step"] == layer["step"] == str(step), "step")
                height = float(trace["height"])
                check(float(trace["time_code"]) == step*dt, "time")
                factor = 10/(width*dt)
                values = {name:factor*float(layer[name+"_delta"]) for name in NAMES}
                check(math.isclose(sum(values[name] for name in NAMES[:3]), values["whole"], abs_tol=2e-12), "layer balance")
                values["pressure"] = 10*float(trace["bottom_pressure_E"])
                check(math.isclose(values["pressure"], factor*float(layer["floor_J"]), abs_tol=2e-12), "floor pressure")
                series[step] = (height, (width-height)/0.1, values)
            grids[cell] = series
    rows = []
    for i, (ha, movement, a) in grids[12].items():
        hb, _, b = grids[24][2*i]
        check(ha == hb, "plate displacement")
        row = {"F12_step":i, "F24_step":2*i, "travel_D":movement}
        row.update({name:a[name]-b[name] for name in (*NAMES,"pressure")})
        rows.append(row)
    crossed = next(row for row in rows if abs(row["pressure"]) > .05*REFERENCE)
    peak = max(rows,key=lambda r:abs(r["pressure"]))
    for point, reference in zip((crossed,peak), report["observations"], strict=True):
        check([point["F12_step"],point["F24_step"]] == reference["steps_F12_F24"], "reference positions")
        for name in NAMES:
            check(math.isclose(point[name], reference["F12_minus_F24"][name+"_delta_MPa"],
                               rel_tol=1e-12, abs_tol=2e-12), "event momentum")
    return rows, crossed["F12_step"], peak["F12_step"]


def draw(path, output, rscript):
    rows, first, peak = read(path)
    tmp_csv = io.StringIO(newline="")
    writer = csv.DictWriter(tmp_csv, rows[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    data = tmp_csv.getvalue().encode("ascii")
    with tempfile.TemporaryDirectory() as scratch:
        directory = Path(scratch)
        data_path = directory/"data.csv"
        data_path.write_bytes(data)
        image_path = directory/"plot.png"
        cmd = [rscript, "--vanilla", str(Path(__file__).with_name("plot_depth.R")),
               str(data_path), str(image_path), str(first), str(peak)]
        subprocess.run(cmd, check=True)
        tags = PngImagePlugin.PngInfo()
        tags.add_text("RETURN_SHA256", SOURCE)
        tags.add_text("PLOT_DATA_SHA256", digest(data))
        tags.add_text("DESCRIPTION", "F12 minus F24 momentum-rate differences (MPa equivalent), matched step ends")
        with Image.open(image_path) as image:
            check(image.size == (1800,1200), "dimensions")
            image.convert("RGB").save(output, format="PNG", dpi=(200,200), pnginfo=tags)
    with Image.open(output) as image:
        check(image.info["RETURN_SHA256"] == SOURCE, "figure provenance")
        image.verify()
    print(digest(output.read_bytes()), output.name, first, peak)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("--rscript",default="Rscript")
    args = parser.parse_args()
    draw(args.source,args.output,args.rscript)
