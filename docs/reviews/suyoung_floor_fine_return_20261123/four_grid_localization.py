"""Compare four saved setting-1 material-floor curves on the same displacement interval."""
import argparse
import bisect
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


COARSE_HASH = "aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65"
FINE_HASH = "c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673"
DIAMETER = .1
LOWER_PLATE = .15
REF_MPA = .6636991102836952
GRIDS = (8, 12, 16, 24)


def require(test, message):
    if not test:
        raise ValueError(message)


def load(path, expected, grids):
    with path.open("rb") as source:
        require(hashlib.file_digest(source, "sha256").hexdigest() == expected, "unexpected return")
        source.seek(0)
        with tarfile.open(fileobj=source, mode="r:gz") as archive:
            result = {}
            for n in grids:
                raw = archive.extractfile(f"run/F{n}/trace.csv").read()
                receipt = json.load(archive.extractfile(f"run/F{n}/result.json"))
                require(receipt["trace_sha256"] == hashlib.sha256(raw).hexdigest() and
                        receipt["status"] == "TARGET_BRACKETED" and receipt["cells"] == n, "arm identity")
                rows = list(csv.DictReader(io.StringIO(raw.decode("ascii"))))
                require(all(int(r["step"]) == i for i,r in enumerate(rows)), "step sequence")
                h0 = float(rows[0]["height"])
                u = [h0 - float(r["height"]) for r in rows]
                p = [10. * float(r["bottom_pressure_E"]) for r in rows]
                require(all(x<y for x,y in zip(u,u[1:])) and u[0]==p[0]==0 and
                        all(math.isfinite(x) and 0 <= x < 1.2 for x in p[:-1]) and p[-1]>=1.2,
                        "native endpoint")
                result[n] = u,p,h0
    return result


def at(arm, x):
    u,p,_ = arm
    j = bisect.bisect_left(u, x)
    if j < len(u) and u[j] == x:
        return p[j]
    require(0 < j < len(u),"extrapolation")
    return p[j-1] + (p[j]-p[j-1]) * ((x-u[j-1])/(u[j]-u[j-1]))


def compare(arms):
    common_end = min(arm[0][-1] for arm in arms.values())
    knots = sorted({x for u,_,_ in arms.values() for x in u if x <= common_end})
    press = {n:[at(arms[n],x) for x in knots] for n in GRIDS}
    pair_results = {}
    for a,b in ((8,16),(12,24),(8,12),(12,16),(16,24)):
        delta = [x-y for x,y in zip(press[a],press[b])]
        i = max(range(len(knots)), key=lambda j:abs(delta[j]))
        pair_results[f"F{a}-F{b}"] = dict(signed_at_peak_MPa=delta[i], u_at_peak_diameters=knots[i]/DIAMETER,
                                          fixed_reference_pct=100*abs(delta[i])/REF_MPA,
                                          signed_edge_MPa=delta[-1], edge_pressures_MPa=[press[a][-1],press[b][-1]])
    # Integrate only the existing piecewise-linear curves for a cumulative diagnostic.
    integrals = {n:math.fsum((x1-x0)*(p1+p0)/2 for x0,x1,p0,p1 in zip(
                    knots,knots[1:],pr,pr[1:]))/common_end for n,pr in press.items()}
    h0 = arms[8][2]
    require(all(a[2] == h0 for a in arms.values()), "initial height mismatch")
    target_pressures = {}
    for phi in (.84,.90,.95):
        u = h0*(1.-.78/phi)
        target_pressures[str(phi)] = dict(u_diameters=u/DIAMETER,pressure_MPa={
            str(n):at(arm,u) if u <= arm[0][-1] else None for n,arm in sorted(arms.items())})
    # Geometry alone: the pinned upper wall can act only on occupied nodes here
    # or higher, and only if moving toward the plate in its own frame.
    # Native trace returns have no per-node mass, velocity or wall impulses.
    fine_knots = sorted({x for n in (12,24) for x in arms[n][0] if x <= common_end})
    fine_gap = [abs(at(arms[12],x)-at(arms[24],x)) for x in fine_knots]
    observations = {"first_fixed_exceed":next(i for i,v in enumerate(fine_gap) if 20*v > REF_MPA),
                    "largest_in_four_grid_overlap":max(range(len(fine_gap)),key=fine_gap.__getitem__)}
    upper_rows = {}
    for k,i in observations.items():
        u = fine_knots[i]
        lid = LOWER_PLATE+(h0-u)
        grids = {}
        for n in (12,24):
            j = bisect.bisect_left(arms[n][0],u)
            grid = round(n/DIAMETER)
            first = next(j for j in range(grid+1) if j/grid >= lid)
            grids[str(n)] = dict(native_step=j if arms[n][0][j] == u else None,
                                 pressure_MPa=at(arms[n],u),first_geometrically_eligible_row=first,
                                 first_eligible_y=first/grid,offset_diameters=(first/grid-lid)/DIAMETER)
        upper_rows[k] = dict(u_diameters=u/DIAMETER, upper_plate_y=lid,grids=grids)
    return dict(full_tar_sha256=COARSE_HASH, fine_tar_sha256=FINE_HASH, label="DEVELOPMENT_ONLY",
        common_all=dict(samples=len(knots),end_displacement_diameters=common_end/DIAMETER,
                        pressures_at_end_MPa={str(n):press[n][-1] for n in GRIDS},
                        pair_maxima=pair_results, time_or_displacement_averaged_pressure_MPa=integrals),
        memo_reference_fractions=target_pressures,upper_geometric_row_at_candidate_snapshots=upper_rows)


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("coarse_tar",type=Path)
    p.add_argument("fine_tar",type=Path)
    a=p.parse_args()
    arms=load(a.coarse_tar,COARSE_HASH,(8,16)) | load(a.fine_tar,FINE_HASH,(12,24))
    print(json.dumps(compare(arms),indent=2,allow_nan=False))
