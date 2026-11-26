"""Read the preregistered single-disk plate diagnostic from a fixed local return."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile

RELEASE = "63e104b0774402ab0d11fc2c1c997fc331ba4555"
ARCHIVE = "2eeab4d53c1db8633c8eb16dc969d814ab25a7d13cb2f00fcc8a8979e10e0f4d"
GROUPS = ("G1-PLATE-P-V4", "G1-PLATE-E-V4", "G1-PLATE-P-V0")
CELLS = (8, 16, 24, 32, 48)
D = 0.1
THRESHOLD = 0.008


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def crossing(pressure, axis, times):
    for i, value in enumerate(pressure):
        if value > THRESHOLD:
            require(i > 0, "initial state exceeds the force threshold")
            return dict(step=i, previous_step=i-1, time=times[i], previous_time=times[i-1],
                        u=axis[i], previous_u=axis[i-1], MPa=value, previous_MPa=pressure[i-1])
    return None


def at(u, axis, values):
    i = bisect_left(axis, u)
    if i < len(axis) and axis[i] == u:
        return values[i]
    require(0 < i < len(axis), "extrapolation")
    return values[i-1] + (values[i]-values[i-1]) * ((u-axis[i-1]) / (axis[i]-axis[i-1]))


def peak(samples, denominator):
    if not samples:
        return None
    magnitude = max(abs(difference) for _, difference in samples)
    locations = [dict(u=u, coarse_minus_fine_MPa=d) for u, d in samples if abs(d) == magnitude]
    return dict(n=len(samples), max_abs_MPa=magnitude, percent=100*(magnitude/denominator),
                first_u=locations[0]["u"], ties=locations)


def compare(coarse, fine, boundary):
    a, p = coarse
    b, q = fine
    end = min(a[-1], b[-1])
    knots = sorted({u for u in a+b if u <= end})
    fine_values = [at(u, b, q) for u in knots]
    denom = max(map(abs, fine_values))
    require(denom > 0, "zero fine reference")
    samples = [(u, at(u, a, p)-v) for u, v in zip(knots, fine_values)]
    total = peak(samples, denom)
    report = dict(support=[knots[0], end], fine_peak_MPa=denom, overall=total, common_detection_u=boundary,
                  before=None, after=None, location="HOLD")
    if boundary is not None and knots[0] <= boundary <= end:
        parts = {s["u"] >= boundary for s in total["ties"]}
        report.update(before=peak([(u,d) for u,d in samples if u < boundary], denom),
                      after=peak([(u,d) for u,d in samples if u >= boundary], denom),
                      location="MIXED" if len(parts) > 1 else ("AFTER" if True in parts else "BEFORE"))
    return report


def arm_read(raw, native, first):
    dt = native["dt"]
    require(native["status"] == "COMPLETE" and native["disks"] == 1 and dt > 0, "incorrect arm")
    axis, times, bottom, top = [], [], [], []
    max_residual, max_delta, max_fraction = 0., 0., 0.
    worst_step, momentum_old = 0, 0.
    for i, row in enumerate(csv.DictReader(io.StringIO(raw.decode("ascii")))):
        require(int(row["step"]) == i and row["phase"] == ("LOAD" if i else "INITIAL"), "step or phase")
        u,t,fb,ft,pb,pt,momentum,stored,side = [float(row[k]) for k in (
            "u","time_code","bottom_force","top_force","bottom_MPa","top_MPa",
            "momentum_y","momentum_residual","side_wall_hits")]
        require(all(map(math.isfinite,(u,t,fb,ft,pb,pt,momentum,stored,side))), "nonfinite field")
        require(side == 0 and min(pb,pt,fb,ft) >= 0, "side wall or force sign")
        require(math.isclose(pb,fb / D * 10.,rel_tol=2e-15) and
                math.isclose(pt,ft / D * 10.,rel_tol=2e-15), "force/pressure units")
        if i:
            require(u > axis[-1] and t > times[-1] and math.isclose(t, i*dt, rel_tol=1e-11), "native clock")
            residual = (momentum-momentum_old)-dt*(fb-ft)
            scale = max(1., abs(momentum_old), abs(momentum), abs(dt*fb), abs(dt*ft))
            fraction = abs(residual)/(2e-12*scale)
            delta = abs(residual-stored)
            # Alternate arithmetic order and force-to-impulse round trips.
            ulp = math.ulp(max(abs(momentum-momentum_old), abs(dt*fb), abs(dt*ft)))
            require(delta <= 16 * ulp, "stored and rebuilt residual differ beyond native precision")
            require(fraction <= 1., "registered momentum tolerance exceeded")
            if abs(residual) > max_residual:
                max_residual, worst_step = abs(residual), i
            max_delta, max_fraction = max(max_delta, delta), max(max_fraction, fraction)
        else:
            require((u,t,fb,ft,momentum,stored) == (0.,)*6, "initial row")
        momentum_old = momentum
        axis.append(u)
        times.append(t)
        bottom.append(pb)
        top.append(pt)
    require(len(axis) == native["steps_done"]+1 and native["monitors"]["side_wall_hits_total"] == 0, "arm length or side wall")
    bc, tc = crossing(bottom,axis,times), crossing(top,axis,times)
    geo = first["u_geo"]
    require(first["threshold_MPa"] == THRESHOLD and (bc["step"] if bc else None) == first["step_on"]
            and (bc["u"] if bc else None) == first["u_on"], "native first crossing")
    decomposition = None
    if bc and tc:
        x, y, z = (tc["u"]-geo)/D, (bc["u"]-tc["u"])/D, (bc["u"]-geo)/D
        require(abs(x+y-z) <= 8*math.ulp(max(abs(x),abs(y),abs(z))), "delay decomposition")
        decomposition = dict(geometric_reference_to_top_D=x, top_to_bottom_D=y, total_D=z)
    return (axis,bottom),dict(steps=len(axis)-1, dt=dt, trace_sha256=digest(raw), max_abs_residual=max_residual,
        max_residual_step=worst_step, max_abs_disagreement_with_stored=max_delta, max_fraction_of_tolerance=max_fraction,
        u_geo=geo, actual_first_geometric_contact_time=None, bottom_first=bc, top_first=tc,
        signed_delay=decomposition, side_wall_hits=0)


def run(archive):
    arms = [f"R1-{g}-{n:02d}" for g in GROUPS for n in CELLS]
    wanted = {"run/RELEASE","run/summary.json"} | {
        f"run/arms/{a}/{f}" for a in arms for f in ("result.json","receipt.json","trace.csv")}
    blobs = {}
    with archive.open("rb") as source:
        require(hashlib.file_digest(source,"sha256").hexdigest() == ARCHIVE, "archive identity")
        source.seek(0)
        with tarfile.open(fileobj=source, mode="r|gz") as tar:
            for m in tar:
                if m.name in wanted:
                    require(m.isfile() and m.name not in blobs, "invalid member")
                    blobs[m.name] = tar.extractfile(m).read()
    require(blobs.keys() == wanted and blobs["run/RELEASE"].decode().strip() == RELEASE, "incomplete release")
    original = json.loads(blobs["run/summary.json"])
    require(original["release"] == RELEASE and original["decision"] == "MINI_PLATE_NOT_CONVERGED", "original decision")
    results, curves, pairs = {}, {}, {}
    for arm in arms:
        prefix = f"run/arms/{arm}/"
        raw = blobs[prefix+"trace.csv"]
        result_raw = blobs[prefix+"result.json"]
        native, receipt = json.loads(result_raw), json.loads(blobs[prefix+"receipt.json"])
        require(native["arm"]["name"] == arm and digest(result_raw) == receipt["result_sha256"] and
                digest(raw) == native["trace_sha256"] == original["trace_sha256"][arm], "arm identity "+arm)
        require(receipt["trace_sha256"] == digest(raw), "receipt trace")
        curves[arm], results[arm] = arm_read(raw, native, original["first_force"][arm])
    for group in GROUPS:
        pairs[group] = {}
        for coarse, fine in ((16,32),(24,48)):
            key = f"{coarse}_{fine}"
            arm, other = (f"R1-{group}-{n:02d}" for n in (coarse,fine))
            crossings = [results[n]["bottom_first"] for n in (arm,other)]
            limit = max(c["u"] for c in crossings) if all(crossings) else None
            report = compare(curves[arm], curves[other], limit)
            prev = original["J1"][group]["pairs"][key]
            total = report["overall"]
            require((total["n"],total["max_abs_MPa"],total["first_u"],report["fine_peak_MPa"],
                     total["ties"][0]["coarse_minus_fine_MPa"]) ==
                    (prev["union_knots"],prev["max_abs_difference_MPa"],prev["u_at_first_max_abs"],
                     prev["fine_peak_MPa"],prev["coarse_minus_fine_at_first_max_MPa"]), "J1 replay "+group+" "+key)
            pairs[group][key] = report
    locations = {pair["location"] for pair in pairs[GROUPS[0]].values()}
    decision = ("HOLD" if "HOLD" in locations else next(iter(locations)) if len(locations)==1 else "MIXED")
    return dict(label="DEVELOPMENT_ONLY",archive_sha256=ARCHIVE,release=RELEASE,
                original_decision=original["decision"],primary_group=GROUPS[0],location_decision=decision,
                arms=results,pairs=pairs,solver_calls=0)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive",type=Path)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    result=run(args.archive)
    with args.output.open("x",encoding="utf8",newline="\n") as stream:
        json.dump(result,stream,indent=2,allow_nan=False)
        stream.write("\n")
    print(result["location_decision"],"ARMS",len(result["arms"]),"STEPS",sum(a["steps"] for a in result["arms"].values()))
