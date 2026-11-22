"""Compare old and new F8/F16 native pressures on their shared displacement interval."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
from pathlib import Path
import tarfile

OLD_SHA = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
NEW_SHA = "fc685932f4a1710fe944c5d2dafbcb56bf239f473184f009983a3ff4805dabea"


def read_pair(archive, expected_sha, folder):
    with archive.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != expected_sha:
            raise ValueError("Return archive SHA256 mismatch")
        stream.seek(0)
        curves = []
        with tarfile.open(fileobj=stream, mode="r:gz") as bundle:
            for cells in (8, 16):
                row_bytes = bundle.extractfile(f"{folder}/F{cells}/trace.csv").read()
                rows = list(csv.DictReader(io.StringIO(row_bytes.decode("ascii"))))
                height0 = float(rows[0]["height"])
                grid = [height0 - float(row["height"]) for row in rows]
                pressure = [10 * float(row["bottom_pressure_E"]) for row in rows]
                if grid[0] != 0 or any(a >= b for a, b in zip(grid, grid[1:])):
                    raise ValueError("Displacement order")
                curves.append((grid, pressure))
        return curves


def interpolate(curve, u):
    grid, pressure = curve
    i = bisect_left(grid, u)
    if i < len(grid) and grid[i] == u:
        return pressure[i]
    if i == 0 or i == len(grid):
        raise ValueError("Outside native support")
    fraction = (u - grid[i-1]) / (grid[i] - grid[i-1])
    return pressure[i-1] + fraction * (pressure[i] - pressure[i-1])


def compare(curves):
    end = min(u[-1] for u, _ in curves)
    knots = sorted({u for grid, _ in curves for u in grid if u <= end})
    old8, old16, new8, new16 = [[interpolate(curve, u) for u in knots] for curve in curves]

    def peak_difference(left, right):
        signed = [a - b for a, b in zip(left, right)]
        i = max(range(len(knots)), key=lambda k: abs(signed[k]))
        return {"signed_MPa": signed[i], "u": knots[i]}

    return {
        "common_end": end, "common_count": len(knots),
        "at_end": {"old8": old8[-1], "old16": old16[-1], "new8": new8[-1], "new16": new16[-1],
                   "old_gap": old8[-1] - old16[-1], "new_gap": new8[-1] - new16[-1]},
        "peak_gap_old": peak_difference(old8, old16), "peak_gap_new": peak_difference(new8, new16),
        "coarse_shift": peak_difference(new8, old8), "fine_shift": peak_difference(new16, old16),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("old", "new", "out"):
        p.add_argument("--" + name, type=Path, required=True)
    args = p.parse_args()
    curves = read_pair(args.old, OLD_SHA, "run/arms") + read_pair(args.new, NEW_SHA, "run")
    with args.out.open("x", encoding="ascii", newline="\n") as file:
        json.dump(compare(curves), file, indent=2, allow_nan=False)
        file.write("\n")
