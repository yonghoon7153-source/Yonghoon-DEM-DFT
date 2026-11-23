"""Verify the registered two-control prefix from the two completed archives (no solver run)."""
import argparse
import csv
import hashlib
import io
import json
import math
import tarfile
from pathlib import Path


PIN = "ebba5037e29de3ca760de7fe3d1a85d43ff3f1e6"
CURRENT = "ea7ea6b8903529c20b2d5fdc350c4627bdd0a32a20fba154b543dade1d3eaf12"
PRIOR = "4bb6fe0cdff8964c6bf02cfbf3f9dd9f7bdec5199cfddce0e3d8160b0dd4f391"
SCREEN = "79248af4163283d21d7161585d0291a10b959c399af219df5662287d65e02d3c"
PEAK = 0.6636991102836952
ARMS = ("native8", "fine_dt_seed8", "fine_dt_seed16", "native16")


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def member(tar, name):
    entry, = [m for m in tar.getmembers() if m.name == "run/" + name]
    require(entry.isfile(), name)
    return tar.extractfile(entry).read()


def trace(raw, size):
    rows = list(csv.DictReader(io.StringIO(raw.decode("ascii"))))
    require(len(rows) == size and all(int(r["step"]) == i for i, r in enumerate(rows)), "step sequence")
    return [(float(r["time_code"]), float(r["height"]), 10 * float(r["bottom_pressure_E"])) for r in rows]


def verify(current, prior):
    for path, expected in ((current, CURRENT), (prior, PRIOR)):
        with path.open("rb") as stream:
            require(hashlib.file_digest(stream, "sha256").hexdigest() == expected, path.name)
    with tarfile.open(current, "r:gz") as new, tarfile.open(prior, "r:gz") as old:
        require(member(new, "RELEASE").decode().strip() == PIN, "release")
        require(member(new, "prior_sha256.txt").decode().strip() == PRIOR, "history")
        require(sha(member(new, "screen.txt")) == SCREEN, "operator screen")
        summary = json.loads(member(new, "summary.json"))
        data = {}
        for cells, arm in ((8, ARMS[1]), (16, ARMS[2])):
            receipt = json.loads(member(new, f"seed{cells}/receipt.json"))
            raw = member(new, f"seed{cells}/trace.csv")
            require(sha(raw) == receipt["trace_sha256"] and receipt["status"] == "PREFIX_COMPLETE"
                    and receipt["grid"] == 80 and receipt["seed_cells"] == cells
                    and receipt["step_count"] == receipt["kernel_calls"] == 540, arm)
            data[arm] = trace(raw, 541)
            original = member(old, f"F{cells}/trace.csv")
            require(sha(original) == receipt["native_trace_sha256"][str(cells)], "native trace")
            data[f"native{cells}"] = trace(original, 271 if cells == 8 else 541)
    require(summary["registered_fine_peak_MPa"] == PEAK and summary["shared_samples"] == 271
            and len(summary["samples"]) == 271 and not summary["qualification_computed"], "registered scope")
    primary = []
    max_residual = 0.0
    keys = ("dt_MPa", "seed_MPa", "grid_MPa", "native_gap_MPa")
    for i, saved in enumerate(summary["samples"]):
        j = 2 * i
        points = [data[arm][i if arm == "native8" else j] for arm in ARMS]
        require(all(point[:2] == points[0][:2] for point in points), "time or plate position")
        a, b, c, d = (p[2] for p in points)
        diffs = (a-b, b-c, c-d, a-d)
        require(saved["coarse_step"] == i and saved["fine_step"] == j
                and all(saved[k] == v for k, v in zip(keys, diffs)), "signed contrast")
        residual = abs(math.fsum(diffs[:3]) - diffs[3])
        max_residual = max(max_residual, residual)
        if i in (269, 270):
            primary.append(dict(coarse_step=i, fine_step=j, pressure_MPa=dict(zip(ARMS, (a,b,c,d))),
                                signed_difference_MPa=dict(zip(keys, diffs)),
                                difference_in_percent_of_reference={k: v / PEAK * 100 for k, v in zip(keys, diffs)}))
    require(max_residual <= 1e-12, "pressure identity")
    return dict(label="DEVELOPMENT_ONLY", release=PIN, return_sha256=CURRENT, prior_sha256=PRIOR,
                equal_time_and_height_pairs=271, pressure_reference_MPa=PEAK, threshold_MPa=.05*PEAK,
                max_additivity_residual_MPa=max_residual, primary=primary,
                full_curve_qualification_computed=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("current", type=Path)
    parser.add_argument("prior", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.current, args.prior), indent=2, allow_nan=False))
