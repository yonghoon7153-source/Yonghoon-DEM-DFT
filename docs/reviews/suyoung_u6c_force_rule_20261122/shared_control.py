"""Compare paired S/F coarse-to-fine differences on the common loading path."""
import argparse
from bisect import bisect_left, bisect_right
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


ARCHIVE_SHA = "a3877d077b56d74877a04215e06135bc3217b5c0f055bf0061a9ba93fcf49f00"
SOURCE_PIN = "6bdfac91520c868b5036071e6d60464972727f49"
TRACE_COLUMNS = ["step", "time_code", "height", "bottom_pressure_E", "phi_m"]


def control(curves):
    if set(curves) != {"Sc", "Sf", "Fc", "Ff"}:
        raise ValueError("four matched curves required")
    axes = {}
    for label, rows in curves.items():
        if len(rows) < 2 or rows[0][0] != 0:
            raise ValueError("common loading origin missing")
        last = -1.
        for u, pressure in rows:
            if not (math.isfinite(u) and last < u and math.isfinite(pressure) and pressure >= 0):
                raise ValueError("invalid loading sample")
            last = u
        axes[label] = [u for u, _ in rows]

    end_by_arm = {label: axis[-1] for label, axis in axes.items()}
    end = min(end_by_arm.values())
    knots = sorted({u for axis in axes.values() for u in axis[:bisect_right(axis, end)]})

    def pressure(label, u):
        axis = axes[label]
        j = bisect_left(axis, u)
        if j < len(axis) and axis[j] == u:
            return curves[label][j][1]
        if not 0 < j < len(axis):
            raise ValueError("extrapolation outside trace")
        u0, p0 = curves[label][j-1]
        u1, p1 = curves[label][j]
        return p0 + (p1-p0) * ((u-u0)/(u1-u0))

    gaps = {model: [pressure(model+"c", u)-pressure(model+"f", u) for u in knots]
            for model in ("S", "F")}
    gaps["F_minus_S_grid_difference"] = [f-s for f, s in zip(gaps["F"], gaps["S"])]
    peaks = {}
    for label, values in gaps.items():
        index = max(range(len(knots)), key=lambda j: abs(values[j]))
        peaks[label] = {"absolute_MPa": abs(values[index]), "signed_MPa": values[index],
                        "first_u": knots[index]}
    f_peak = bisect_left(knots, peaks["F"]["first_u"])
    return {
        "four_way_start_u": 0., "four_way_end_u": end, "union_knots": len(knots),
        "end_u_by_arm": end_by_arm,
        "two_way_end_u": {m: min(end_by_arm[m+"c"], end_by_arm[m+"f"]) for m in ("S", "F")},
        "peaks": peaks, "at_F_abs_peak": {"u": knots[f_peak], "S_grid_difference_MPa": gaps["S"][f_peak],
                                         "F_grid_difference_MPa": gaps["F"][f_peak]},
    }


def curve(archive, identifiers, model, cells):
    name = model+str(cells)
    prefix = "run/arms/"+name+"/"
    raw = archive.extractfile(prefix+"trace.csv").read()
    receipt = json.loads(archive.extractfile(prefix+"result.json").read())
    digest = hashlib.sha256(raw).hexdigest()
    original = identifiers[name]
    if (receipt["arm"] != model or receipt["cells"] != cells or receipt["setting"] != 1
            or receipt["trace_sha256"] != digest or original["trace_sha256"] != digest
            or receipt["status"] != original["status"] or receipt["steps"] != original["steps"]
            or receipt["status"] not in ("TARGET_BRACKETED", "GEOMETRY_LIMIT")):
        raise ValueError("trace and receipt differ: " + name)
    reader = csv.DictReader(io.StringIO(raw.decode("ascii")))
    if reader.fieldnames != TRACE_COLUMNS:
        raise ValueError("trace header mismatch")
    samples = []
    initial_height = None
    for step, row in enumerate(reader):
        if row["step"] != str(step):
            raise ValueError("missing loading sample")
        height = float(row["height"])
        if initial_height is None:
            initial_height = height
        samples.append((initial_height-height, 10.0 * float(row["bottom_pressure_E"])))
    if len(samples) != receipt["steps"] + 1:
        raise ValueError("terminal step differs from receipt")
    return initial_height, samples, digest


def readback(archive_path):
    with archive_path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != ARCHIVE_SHA:
            raise ValueError("prior development archive mismatch")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            if "release="+SOURCE_PIN not in archive.extractfile("run/origin.txt").read().decode("ascii").splitlines():
                raise ValueError("source release mismatch")
            identifiers = json.load(archive.extractfile("run/summary.json"))["inputs"]
            all_curves = {(m, n): curve(archive, identifiers, m, n)
                          for m in ("S", "F") for n in (8, 12, 16, 24)}
    if len({entry[0] for entry in all_curves.values()}) != 1:
        raise ValueError("initial plate heights differ")
    pairs = {}
    for n in (8, 12):
        curves = {m+k: all_curves[(m, cells)][1] for m in ("S", "F") for k,cells in (("c",n),("f",2*n))}
        pairs[f"{n}_{2*n}"] = control(curves)
    return {"label": "DEVELOPMENT_CONTROL", "qualification_tested": False, "source_pin": SOURCE_PIN,
            "archive_sha256": ARCHIVE_SHA, "displacement_unit": "code_length", "pressure_unit": "MPa",
            "trace_sha256": {m+str(n): rec[2] for (m,n), rec in all_curves.items()}, "pairs": pairs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("new_output", type=Path)
    args = parser.parse_args()
    result = readback(args.archive)
    with args.new_output.open("x", encoding="ascii", newline="\n") as out:
        json.dump(result, out, sort_keys=True, indent=2, allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
