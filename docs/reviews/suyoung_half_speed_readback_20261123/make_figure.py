"""Generate a plate-pressure comparison from the two recorded WSL tarballs."""
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


ORIGINAL = "cdd3ff1dcdbe02dcb6493a4112a0136076883f2179c33f322e2287c0ffdfb14e"
HALF = "ddcf2fd738430c40246d177d1e1dea73de24883c07218e4f07c0dcf6de90f863"
DENOMINATOR = .6636991102836952
DIAMETER = .1


def check(ok, msg):
    if not ok:
        raise ValueError(msg)


def read_native(tarfile_path, digest, steps):
    raw = tarfile_path.read_bytes()
    check(hashlib.sha256(raw).hexdigest() == digest, "return digest")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        names = tar.getnames()
        def read(name):
            fullname = "run/" + name
            check(names.count(fullname) == 1 and tar.getmember(fullname).isfile(), fullname)
            return tar.extractfile(fullname).read()
        summary = json.loads(read("summary.json"))
        check(summary["reference_MPa"] == DENOMINATOR, "reference pressure")
        rows = {}
        for n in (12,24):
            trace = read(f"F{n}/trace.csv")
            check(hashlib.sha256(trace).hexdigest()==summary["arms"][str(n)]["trace_sha256"], "arm trace digest")
            items = list(csv.DictReader(io.StringIO(trace.decode("ascii"))))
            check([int(r["step"]) for r in items] == list(range(steps*n//12 + 1)), "native clock")
            rows[n] = items
    width = float(rows[24][0]["height"])
    knots = []
    for i, b in enumerate(rows[24]):
        a = rows[12][i//2]
        h = float(b["height"])
        p = float(a["bottom_pressure_E"])
        if i % 2:
            a2 = rows[12][i//2+1]
            h1, h2 = float(a["height"]), float(a2["height"])
            check(h1 > h > h2, "F12 bracket")
            p += (h1-h)/(h1-h2) * (float(a2["bottom_pressure_E"])-p)
        else:
            check(b["height"] == a["height"], "even F24/F12 position")
        p12, p24 = 10*p, 10*float(b["bottom_pressure_E"])
        knots.append(dict(step=i, movement=(width-h)/DIAMETER, F12=p12, F24=p24,
                          kind="interpolated" if i%2 else "native", gap=p12-p24))
    check(all(math.isfinite(row[k]) for row in knots for k in ("movement","F12","F24","gap")), "finite pressures")
    return knots, summary


def verify_peak(knots, comparison):
    peak = max(knots, key=lambda row:abs(row["gap"]))
    check(len(knots) == comparison["samples"] and
          comparison["peak"]["displacement_diameters"] == peak["movement"] and
          comparison["peak"]["signed_gap_MPa"] == peak["gap"] and
          comparison["fixed_reference_percent"] == 100*abs(peak["gap"])/DENOMINATOR, "peak verification")


def create(original, half, output, rscript):
    ref, ref_summary = read_native(original, ORIGINAL, 569)
    slow, summary = read_native(half, HALF, 1138)
    check(summary["original_speed_material_lid_sha256"] == ORIGINAL, "history binding")
    expected = summary["pressure_union"]
    verify_peak(ref, ref_summary["new_material_lid"])
    verify_peak(ref, expected["original_native_1139"])
    verify_peak(slow, expected["half_native_2277"])
    verify_peak(slow[::2], expected["half_on_original_1139"])
    stream = io.StringIO(newline="")
    w = csv.writer(stream, lineterminator="\n")
    w.writerow(["plate_travel_D","original_F24_step","original_F12_sample","original_F12_MPa","original_F24_MPa",
                "original_delta_MPa","half_F24_step","half_F12_sample","half_F12_MPa","half_F24_MPa","half_delta_MPa"])
    for i,row in enumerate(slow):
        fixed = [""]*5
        if i%2==0:
            old = ref[i//2]
            check(row["movement"] == old["movement"], "common displacement")
            fixed = [old[k] for k in ("step","kind","F12","F24","gap")]
        w.writerow([row["movement"], *fixed, *[row[k] for k in ("step","kind","F12","F24","gap")]])
    csv_bytes = stream.getvalue().encode("ascii")
    with tempfile.TemporaryDirectory() as scratch:
        tmp = Path(scratch)
        (tmp/"data.csv").write_bytes(csv_bytes)
        subprocess.run([rscript, "--vanilla", str(Path(__file__).with_name("plot.R")),
                        str(tmp/"data.csv"), str(tmp/"plot.png"), str(DENOMINATOR)], check=True)
        tag = PngImagePlugin.PngInfo()
        for key,val in {"CSV_SHA256":hashlib.sha256(csv_bytes).hexdigest(),"ORIGINAL_TAR_SHA256":ORIGINAL,
                        "HALF_TAR_SHA256":HALF,"FIXED_REFERENCE_MPA":str(DENOMINATOR)}.items():
            tag.add_text(key, val)
        image_data = io.BytesIO()
        with Image.open(tmp/"plot.png") as png:
            png.convert("RGB").save(image_data, format="PNG", pnginfo=tag, dpi=(210,210))
        image = image_data.getvalue()
    with Image.open(io.BytesIO(image)) as fig:
        check(fig.size == (1800,1180) and fig.info["CSV_SHA256"] == hashlib.sha256(csv_bytes).hexdigest(), "PNG")
        fig.verify()
    for name, data in (("half_speed_pressure.csv",csv_bytes),("half_speed_pressure.png",image)):
        (output/name).write_bytes(data)
    print("validated 1139 common and 2277 native points")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("original",type=Path)
    ap.add_argument("half",type=Path)
    ap.add_argument("output",type=Path)
    ap.add_argument("--rscript",default="Rscript")
    create(**vars(ap.parse_args()))
