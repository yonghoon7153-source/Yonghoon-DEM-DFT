"""Describe the two F resolution-doubling pairs in the fixed 11-21 return."""
import argparse
from bisect import bisect_left, bisect_right
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


ARCHIVE_DIGEST = "a3877d077b56d74877a04215e06135bc3217b5c0f055bf0061a9ba93fcf49f00"
SOURCE = "6bdfac91520c868b5036071e6d60464972727f49"
COLUMNS = ["step", "time_code", "height", "bottom_pressure_E", "phi_m"]
E_MPA = 10.0


def validate(samples):
    if len(samples) < 2 or samples[0][0] != 0:
        raise ValueError("curve must start at zero displacement and have two or more samples")
    previous_u = -1.
    for u, pressure in samples:
        if not (math.isfinite(u) and u > previous_u and math.isfinite(pressure) and pressure >= 0):
            raise ValueError("invalid displacement or compression reaction")
        previous_u = u


def interpolate(u, axis, samples):
    j = bisect_left(axis, u)
    if j < len(axis) and axis[j] == u:
        return samples[j][1]
    if j == 0 or j == len(axis):
        raise ValueError("extrapolation forbidden")
    u0, y0 = samples[j-1]
    u1, y1 = samples[j]
    return y0 + (y1-y0) * ((u-u0)/(u1-u0))


def compare(coarse, fine):
    validate(coarse)
    validate(fine)
    a = [u for u, _ in coarse]
    b = [u for u, _ in fine]
    end = min(a[-1], b[-1])
    ac, bc = bisect_right(a, end), bisect_right(b, end)
    knots = sorted(set(a[:ac]).union(b[:bc]))
    delta = [interpolate(u, a, coarse) - interpolate(u, b, fine) for u in knots]
    j = max(range(len(delta)), key=lambda i: abs(delta[i]))
    return {
        "common_start_u": 0., "common_end_u": end,
        "end_u_coarse": a[-1], "end_u_fine": b[-1],
        "end_u_coarse_minus_fine": a[-1] - b[-1],
        "coarse_samples": len(a), "fine_samples": len(b),
        "coarse_samples_in_common": ac, "fine_samples_in_common": bc,
        "union_knots": len(knots),
        "min_coarse_minus_fine_MPa": min(delta), "max_coarse_minus_fine_MPa": max(delta),
        "max_abs_difference_MPa": abs(delta[j]), "u_at_first_max_abs": knots[j],
        "coarse_minus_fine_at_first_max_abs_MPa": delta[j],
        "coarse_minus_fine_at_common_end_MPa": delta[-1],
    }


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_curve(archive, summary, cells):
    arm = f"F{cells}"
    folder = f"run/arms/{arm}/"
    raw = archive.extractfile(folder+"trace.csv").read()
    receipt_raw = archive.extractfile(folder+"result.json").read()
    receipt = json.loads(receipt_raw)
    old = summary["inputs"][arm]
    sha = digest(raw)
    if (receipt["setting"] != 1 or receipt["arm"] != "F" or receipt["cells"] != cells
            or receipt["protocol"] != summary["protocol"] or receipt["label"] != "DEVELOPMENT_ONLY"
            or sha != receipt["trace_sha256"] or sha != old["trace_sha256"]
            or any(receipt[k] != old[k] for k in ("steps", "status", "origin"))
            or receipt["status"] not in ("TARGET_BRACKETED", "GEOMETRY_LIMIT")):
        raise ValueError(f"receipt binding failed for {arm}")
    rows = csv.DictReader(io.StringIO(raw.decode("ascii"), newline=""))
    if rows.fieldnames != COLUMNS:
        raise ValueError(f"unexpected columns for {arm}")
    data = []
    for step, row in enumerate(rows):
        if row["step"] != str(step):
            raise ValueError(f"step gap in {arm}")
        h = float(row["height"])
        p = E_MPA * float(row["bottom_pressure_E"])
        if step == 0:
            h0 = h
        data.append((h0 - h, p))
    if len(data) != receipt["steps"] + 1:
        raise ValueError(f"trace length differs for {arm}")
    return data, h0, {"trace_sha256": sha, "result_sha256": digest(receipt_raw),
                       "steps": receipt["steps"], "origin": receipt["origin"]}


def readback(path):
    with path.open("rb") as src:
        if hashlib.file_digest(src, "sha256").hexdigest() != ARCHIVE_DIGEST:
            raise ValueError("expected the original 11-21 dense return")
        src.seek(0)
        with tarfile.open(fileobj=src, mode="r:gz") as archive:
            original = archive.extractfile("run/summary.json").read()
            if "release="+SOURCE not in archive.extractfile("run/origin.txt").read().decode("ascii").splitlines():
                raise ValueError("wrong release")
            summary = json.loads(original)
            curves = {c: read_curve(archive, summary, c) for c in (8, 12, 16, 24)}
    if len({row[1] for row in curves.values()}) != 1:
        raise ValueError("initial height differs across paired arms")
    results = {f"F{c}_F{2*c}": compare(curves[c][0], curves[2*c][0]) for c in (8,12)}
    return {"label": "DEVELOPMENT_DESCRIPTIVE", "u6c_status": "HOLD", "qualification_tested": False,
            "archive_sha256": ARCHIVE_DIGEST, "summary_sha256": digest(original), "release": SOURCE,
            "setting": 1, "initial_height_code": curves[8][1], "E_MPa": E_MPA,
            "displacement": "initial_height_minus_current_height_code",
            "pressure": "bottom_pressure_E_times_E_MPa",
            "receipts": {f"F{c}": row[2] for c,row in curves.items()}, "pairs": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = readback(args.archive)
    with args.output.open("x", encoding="ascii", newline="\n") as out:
        json.dump(result, out, sort_keys=True, indent=2, allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
