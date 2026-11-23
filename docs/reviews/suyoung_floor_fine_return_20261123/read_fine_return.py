"""Verify both frozen wall runs and independently compare four grids at like displacements.

Inputs are the released F12/F24 author TXT, its completed return directory and the
earlier F8/F16 return TAR. Only the pinned receipt/readback routines are invoked.
The standalone curve cross-check below uses Python's standard library.
"""
import argparse
import base64
from bisect import bisect_left
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path, PurePosixPath
import tarfile
import tempfile


FINE_TAR = "c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673"
FINE_SCREEN = "4013a5e5d39bb06675d1427e5f4a67ca2cffeffd237f2a4c0cc06df23787b007"
PRIOR_TAR = "aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65"
BLOCK_SHA = "96270f3c4f37980436c23c72b86a238370e2dbcfe0eb3702407bc2b078f7ad3a"
PKG_SHA = "a6bdf77ce8d0562a141267519f6d747e278f2fc40e12f4ef4d970f5c8eca2c7f"
RELEASE = "e8e2f2535aa12b9fb089d714e1325d862cb1161b"
REF_MPA = .6636991102836952
DIAMETER = .1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def fixed(path, expected):
    raw = path.read_bytes()
    require(digest(raw) == expected, "unexpected input digest: " + path.name)
    return raw


def archive(raw):
    """Read only regular, unambiguously named members; no TAR-driven filesystem extraction."""
    result, seen = {}, set()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        for entry in tar:
            path = PurePosixPath(entry.name)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in entry.name
                    and path.as_posix() == entry.name and path not in seen, "invalid archive member")
            seen.add(path)
            if entry.isfile():
                result[entry.name] = tar.extractfile(entry).read()
            else:
                require(entry.isdir(), "nonregular archive member")
    return result


def project(dest, entries):
    for name, raw in entries.items():
        p = dest / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("xb") as f:
            f.write(raw)


def receipts(block, prior, fine):
    text = fixed(block, BLOCK_SHA)
    payload = text.split(b"FINE_FLOOR_SOURCES'\n", 1)[1].split(b"\nFINE_FLOOR_SOURCES\n", 1)[0]
    source = base64.b64decode(b"".join(payload.splitlines()), validate=True)
    require(digest(source) == PKG_SHA, "source archive")
    with tempfile.TemporaryDirectory() as scratch:
        pkg = Path(scratch) / "pkg"
        result = Path(scratch) / "return"
        project(pkg, archive(source))
        project(result, fine)
        modfile = pkg / "docs/reviews/suyoung_floor_fine_20261123/fine_floor.py"
        spec = importlib.util.spec_from_file_location("floor_receipt_module", modfile)
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
        ctx = native.context(pkg)
        prior_result = native.previous_pair(ctx, prior)
        repeated = native.summarize(ctx, prior_result, result / "run")
        require(repeated == json.loads(fine["run/summary.json"]), "complete summary/receipt mismatch")
        for name in ("RELEASE","SOURCE_SHA256SUMS"):
            require(fine["run/"+name] == (pkg/name).read_bytes(), name)
        return repeated


def curve(raw):
    rows = list(csv.DictReader(io.StringIO(raw.decode("ascii"),newline="")))
    x0 = float(rows[0]["height"])
    x, p = [], []
    for i, row in enumerate(rows):
        u, pressure = x0 - float(row["height"]), 10*float(row["bottom_pressure_E"])
        require(int(row["step"]) == i and math.isfinite(pressure) and pressure >= 0, "native sample")
        require(not x or u > x[-1], "step order")
        x.append(u)
        p.append(pressure)
    return x, p


def at(curve_data, u):
    x, p = curve_data
    j = bisect_left(x, u)
    if j < len(x) and x[j] == u:
        return p[j]
    require(0 < j < len(x), "common support interpolation")
    return p[j-1] + (p[j]-p[j-1])*((u-x[j-1])/(x[j]-x[j-1]))


def compare(curves, a, b, end):
    ca, cb = curves[a], curves[b]
    knots = sorted({u for x,p in (ca,cb) for u in x if u <= end} | {end})
    records = [(u, at(ca,u), at(cb,u)) for u in knots]
    fmax = max(r[2] for r in records)

    def point(r):
        if r is None:
            return None
        u, pa, pb = r
        return dict(displacement_code=u,displacement_diameters=u/DIAMETER,
                    coarse_MPa=pa,fine_MPa=pb,raw_gap_MPa=pa-pb)

    def summary(samples):
        worst = max(samples, key=lambda r:abs(r[1]-r[2]))
        gap = abs(worst[1] - worst[2])
        exceeds = [r for r in samples if abs(r[1]-r[2]) > REF_MPA/20]
        return dict(samples=len(samples), largest=point(worst), max_abs_MPa=gap,
                    fixed_percent=100*gap/REF_MPA, fine_peak_percent=100*gap/fmax,
                    first_above=point(next(iter(exceeds), None)), count_above=len(exceeds))
    return dict(pair=f"F{a}_F{b}", end_diameters=end/DIAMETER, fine_peak_MPa=fmax,
                common=summary(records), jointly_positive=summary([r for r in records if r[1]>0 and r[2]>0]))


def run(args):
    stem = "suyoung_floor_fine_result.tar.gz"
    fine = archive(fixed(args.result_dir/stem,FINE_TAR))
    screen = fixed(args.result_dir/"screen.txt",FINE_SCREEN)
    listed = dict((n,h) for h,n in (r.split("  ",1) for r in
                  (args.result_dir/"SHA256SUMS").read_text("ascii").splitlines()))
    require(listed == {stem:FINE_TAR,"screen.txt":FINE_SCREEN} and screen == fine["run/screen.txt"],
            "detached return manifest")
    lines = screen.decode("ascii").splitlines()
    require(all(lines.count(m) == 1 for m in ("F12_RC=0","F24_RC=0","COMMAND_RC=0")) and
            lines[-1] == "COMMAND_RC=0", "author run incomplete")
    prior = archive(fixed(args.prior,PRIOR_TAR))
    recorded = receipts(args.block, args.prior, fine)
    require(recorded["release"] == RELEASE and recorded["both_reached_target"] and
            not any(recorded[k] for k in ("u6_qualified","stage3_go","three_dimensional_go")), "scope")
    curves, arm_summary = {}, {}
    for n in (8,12,16,24):
        data = fine if n in (12,24) else prior
        name = f"run/F{n}/"
        trace = data[name+"trace.csv"]
        native = json.loads(data[name+"result.json"])
        require(native["trace_sha256"] == digest(trace) and native["status"] == "TARGET_BRACKETED","native trace")
        x,p = curves[n] = curve(trace)
        first = next(i for i,v in enumerate(p) if v>0)
        require(len(x) == native["steps"]+1 and p[-1]>=1.2 and max(p[:-1])<1.2, "terminal")
        arm_summary[f"F{n}"] = dict(samples=len(x),terminal_step=len(x)-1,terminal_MPa=p[-1],
                terminal_diameters=x[-1]/DIAMETER,first_positive_step=first,
                first_positive_MPa=p[first],first_positive_diameters=x[first]/DIAMETER,
                elapsed_seconds=native["elapsed_s"],trace_sha256=digest(trace))
    pair_detail = {}
    four_grid = {}
    four_end = min(c[0][-1] for c in curves.values())
    for a,b,authority in ((8,16,json.loads(prior["run/summary.json"])),(12,24,recorded)):
        detail = compare(curves,a,b,min(curves[a][0][-1],curves[b][0][-1]))
        for ours,theirs in (("common","common"), ("jointly_positive","both_positive_knots")):
            d, ref = detail[ours], authority["comparison"][theirs]
            require(d["samples"] == ref["samples"] and d["count_above"] == ref["fixed_reference_exceeding_samples"]
                    and d["first_above"]["displacement_code"] == ref["fixed_reference_first_exceedance"]["u"]
                    and d["largest"]["displacement_code"] == ref["first_worst"]["u"]
                    and math.isclose(d["max_abs_MPa"], ref["max_abs_difference_MPa"], rel_tol=1e-14)
                    and math.isclose(d["fine_peak_percent"]/100, ref["fine_peak_ratio"], rel_tol=1e-14), "gap readback")
        pair_detail[detail["pair"]] = detail
        four_grid[detail["pair"]] = compare(curves,a,b,four_end)
    return dict(release=RELEASE, prior_sha256=PRIOR_TAR, fine_sha256=FINE_TAR, screen_sha256=FINE_SCREEN,
                label="DEVELOPMENT_ONLY", receipt_replay="MATCH", native_curve_crosscheck="MATCH",
                reference_MPa=REF_MPA, threshold_MPa=REF_MPA/20, arms=arm_summary,
                pair_domains=pair_detail,four_grid_common_end_diameters=four_end/DIAMETER,
                pairs_on_four_grid_domain=four_grid,stage3_go=False,u6_qualified=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for n in ("result-dir","prior","block","out"):
        p.add_argument("--"+n,type=Path,required=True)
    args = p.parse_args()
    readback = run(args)
    with args.out.open("x",encoding="ascii",newline="\n") as file:
        json.dump(readback,file,sort_keys=True,indent=2,allow_nan=False)
        file.write("\n")
    print("FINE_RETURN_RAW_AND_RECEIPTS_MATCH")
