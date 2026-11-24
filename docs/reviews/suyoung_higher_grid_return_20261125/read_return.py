"""Read two fixed local returns and recompute grid differences from native CSVs."""
import argparse
import csv
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile

import numpy as np


PRIOR = "882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af"
RETURN = "596dbdae8524f20778b21f4bf5ffba12c7f50a0fa25730288ca95dc5697f28cb"
SCREEN = "df023c20b4c6ea1810fcfceefc7daf7746cb58fb98f069d1a8ad0c0b38ec5da2"
SOURCE = "e1678150e218f07f3269cfb78ad7e1e51e0a98b8"
PHYSICS = "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def contents(path, expected):
    raw = path.read_bytes()
    need(sha(raw) == expected, "return TAR identity")
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        files = {}
        for member in tar:
            if member.isdir():
                continue
            need(member.isfile() and member.name.startswith("run/") and member.name not in files, "TAR member")
            files[member.name] = tar.extractfile(member).read()
    if expected == RETURN:
        manifest = files.pop("run/SHA256SUMS").decode("ascii").splitlines()
        checks = sorted(f"{sha(data)}  ./{name[4:]}" for name, data in files.items())
        need(checks == sorted(manifest), "internal SHA256SUMS")
    return files


def curve(files, grid, release):
    prefix = f"run/F{grid}/"
    rec = json.loads(files[prefix+"target_receipt.json"])
    need(rec["status"] == "TARGET_BRACKETED" and rec["release"] == release and rec["cells"] == grid
         and rec["setting"] == 2 and rec["gap_correction"] and not rec["distance_filter"], "arm identity")
    for name, key in [("trace.csv","trace_sha256"), ("result.json","result_sha256"), ("observation.json","observation_sha256")]:
        need(sha(files[prefix+name]) == rec[key], "arm evidence " + name)
    rows = list(csv.DictReader(io.StringIO(files[prefix+"trace.csv"].decode("ascii"))))
    initial = float(rows[0]["height"])
    times = np.array([float(r["time_code"]) for r in rows])
    h = np.array([float(r["height"]) for r in rows])
    p = np.array([float(r["bottom_pressure_E"]) * 10 for r in rows])
    steps = np.arange(len(rows))
    need(np.array_equal([int(r["step"]) for r in rows], steps)
         and np.array_equal(times, steps * rec["dt"])
         and np.array_equal(h, initial - times * rec["wall_speed"]), "native step, clock or height")
    need(all(np.diff(h) < 0) and p[0] == 0 and np.all(np.isfinite(p)) and np.min(p) >= 0
         and max(p[:-1]) < 1.2 <= p[-1] and len(rows)-1 == rec["bracket_steps"][-1], "native support or target")
    return initial - h, p, rec


def compare(coarse, fine):
    x, y, cr = coarse
    z, w, fr = fine
    need(cr["dt"] == 2 * fr["dt"] and cr["wall_speed"] == fr["wall_speed"], "unequal paired conditions")
    end = min(x[-1], z[-1])
    u = np.union1d(x[x <= end], z[z <= end])
    fp = np.interp(u, z, w)
    diff = np.interp(u, x, y) - fp
    peak = float(np.max(np.abs(fp)))
    need(peak > 0, "zero reference")
    i = int(np.argmax(np.abs(diff)))
    abs_diff = float(abs(diff[i]))
    cutoff = Fraction(peak) / 20
    exceed = [j for j, val in enumerate(diff) if Fraction(float(abs(val))) > cutoff]
    return dict(union_knots=len(u), common_end_u=float(end), max_abs_difference_MPa=abs_diff,
                coarse_minus_fine_at_first_max_MPa=float(diff[i]), u_at_first_max_abs=float(u[i]),
                fine_peak_MPa=peak, ratio=abs_diff/peak, exceeding_knots=len(exceed),
                first_exceedance_u=float(u[exceed[0]]) if exceed else None,
                comparison="EXCEEDS" if exceed else "WITHIN")


def verify(prior_tar, directory):
    clean = contents(prior_tar, PRIOR)
    new = contents(directory/"suyoung_highgrid_result.tar.gz", RETURN)
    screen = (directory/"screen.txt").read_bytes()
    expected = [f"{RETURN}  suyoung_highgrid_result.tar.gz", f"{SCREEN}  screen.txt"]
    need((directory/"SHA256SUMS").read_text().splitlines() == expected and sha(screen) == SCREEN
         and screen == new["run/screen.txt"] and screen.splitlines()[-1] == b"COMMAND_RC=0", "screen or outer sums")
    old = json.loads(clean["run/summary.json"])
    high = json.loads(new["run/summary.json"])
    need(old["release"] == PHYSICS and old["assessment"] == "PASS" and old["selected_setting"] == 2
         and high["release"] == SOURCE and high["physics_pin"] == PHYSICS and high["prior_return_sha256"] == PRIOR,
         "source or selection")
    for blob, summary in [(clean, old), (new, high)]:
        need(blob["run/RELEASE"].decode().strip() == summary["release"]
             and sha(blob["run/SOURCE_SHA256SUMS"]) == summary["source_manifest_sha256"], "source manifest")
    curves = {n:curve(clean,n,PHYSICS) for n in (8,12,16,24)}
    curves.update({n:curve(new,n,SOURCE) for n in (32,48)})
    pairs = {}
    for n in (8,12,16,24):
        key = f"F{n}_F{2*n}"
        found = pairs[key] = compare(curves[n],curves[2*n])
        if n in (16,24):
            saved = high["results"]["pairs"][key]
            need(saved == json.loads(new[f"run/pair_F{2*n}.json"])
                 and saved["coarse_trace_sha256"] == curves[n][2]["trace_sha256"]
                 and saved["fine_trace_sha256"] == curves[2*n][2]["trace_sha256"], "pair receipt")
            for k,value in found.items():
                same = math.isclose(value,saved[k],rel_tol=0,abs_tol=1e-12) if isinstance(value,float) else value == saved[k]
                need(same, f"{key} {k} mismatch")
    times = list(csv.DictReader(io.StringIO(new["run/arm_status.tsv"].decode()),delimiter="\t"))
    need([int(r["grid"]) for r in times] == [32,48] and all(r["rc"] == "0" for r in times), "arm status")
    need(not any(high["results"][k] for k in ["u6_qualified","original_item6_pass","stage3_go","three_dimensional_go"]),
         "reported scope")
    return dict(label="DEVELOPMENT_ONLY", release=SOURCE, physics=PHYSICS, prior_tar_sha256=PRIOR,
                return_tar_sha256=RETURN, outer_screen_sha256=SCREEN, prior_trace_receipts=4,
                return_inner_hashes=len(new), original_u6a_abs_delta=old["absolute_delta"],
                threshold=0.05, displacement_unit="code length", arm_times=times, pairs=pairs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prior_tar",type=Path)
    parser.add_argument("return_directory",type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.prior_tar,args.return_directory),indent=2,allow_nan=False))
