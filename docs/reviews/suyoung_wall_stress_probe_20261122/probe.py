"""Measure the signed yy/yx stress transfer and its unit-tensor response on the native first-wall mask."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tarfile
import tempfile

import numpy as np


MOMENTUM_PATH = "docs/reviews/suyoung_wall_momentum_20261122/observe_momentum.py"
MOMENTUM_SHA = "1c9c25bc2fa6283473214d8bd15c6283792421576642fa191d732b123c1c3e50"
MOMENTUM_PIN = "2390d2a1e7a6663c8c8c32eb9a1cdda65aff4b06"
RETURN_SHA = "bd50c34c882866a39c5a94a511b855017cff3c5921437e60151074ed473bf77b"
STATUS = "DEVELOPMENT_STRESS_PROBE_OBSERVED"
STEPS = {8: (269, 270), 16: (538, 540)}
COLS = ("yy", "yx", "unit_yy", "unit_yx")
FILES = ("momentum.json", "momentum_receipt.json", "wall_observations.json", "trace.csv", "prefix_receipt.json")


def require(ok, issue):
    if not ok:
        raise ValueError(issue)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sources(repo):
    path = repo / MOMENTUM_PATH
    require(digest(path.read_bytes()) == MOMENTUM_SHA, "MOMENTUM_OBSERVER_IDENTITY")
    spec = importlib.util.spec_from_file_location("fixed_wall_momentum", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, *m.sources(repo)


def history(momentum, m, prefix, pair, hist, walls, lo):
    """Recheck each pinned input receipt and the previous aggregate; retain exact replay bytes."""
    with momentum.open("rb") as source:
        require(hashlib.file_digest(source, "sha256").hexdigest() == RETURN_SHA, "MOMENTUM_RETURN_IDENTITY")
        source.seek(0)
        with tarfile.open(fileobj=source, mode="r:gz") as archive:
            def read(name):
                member = archive.getmember("run/" + name)
                require(member.isfile(), "PRIOR_MEMBER")
                return archive.extractfile(member).read()

            origin = dict(line.split("=", 1) for line in read("origin.txt").decode("ascii").splitlines())
            require(origin["release"] == MOMENTUM_PIN and origin["physics_pin"] == prefix.PIN
                    and origin["prior_sha256"] == m.PRIOR and origin["kernel_sha256"] == prefix.KERNEL,
                    "MOMENTUM_SOURCE_IDENTITY")
            old = {n: {k: read(f"F{n}/{k}") for k in FILES} for n in STEPS}
            with tempfile.TemporaryDirectory() as temp:
                samples = {}
                for n, records in old.items():
                    folder = Path(temp) / f"F{n}"
                    folder.mkdir()
                    for name, data in records.items():
                        (folder/name).write_bytes(data)
                    samples[n] = m.checked(prefix,pair,hist,walls,n,folder,lo)
            expected = json.loads(json.dumps(m.summarize(prefix,walls,samples), allow_nan=False))
            require(expected == json.loads(read("summary.json")), "MOMENTUM_SUMMARY")
            return old


def project(solver, x, elastic, ids, volume, grid, width):
    """Wall pressure contributions in MPa on all field-node keys, before selecting original wall rows.

    Native P2G sends -4 dt g² V w tau @ offset. The lower-wall impulse has the
    opposite sign; the pressure conversion 10/(dt width) cancels dt.
    """
    require(math.isfinite(width) and width > 0. and grid > 0, "UNITS")
    nodes, weights, _, offset = solver.model.stencil(x, grid)
    keys, inverse = np.unique((ids[:,None] * (grid+1)**2 + nodes).ravel(), return_inverse=True)
    slots = inverse.ravel()
    tau = solver.model.stress(elastic)
    weight = (40.*grid**2 / width) * volume[:,None] * weights
    yy = weight * offset[:,:,1]
    yx = weight * offset[:,:,0]
    def accumulate(values):
        return np.bincount(slots, weights=values.ravel(), minlength=len(keys))
    columns = dict(yy=accumulate(yy*tau[:,1,1,None]), yx=accumulate(yx*tau[:,1,0,None]),
                   unit_yy=accumulate(yy), unit_yx=accumulate(yx))
    require(all(np.isfinite(a).all() for a in columns.values()), "NONFINITE_PROJECTION")
    return dict(key=keys, **columns)


def subset(projection, native):
    keys = native["keys"]
    indices = np.searchsorted(projection["key"], np.asarray(keys, dtype=np.int64))
    require((indices < len(projection["key"])).all() and projection["key"][indices].tolist() == keys, "MASK_MISSING_KEY")
    return dict(keys=keys, **{c:projection[c][indices].tolist() for c in COLS})


def reduce_record(raw, mask, dt, width):
    keys = mask["keys"]
    require(set(raw) == {"keys", *COLS} and raw["keys"] == keys and keys == sorted(set(keys)), "MASK_KEYS")
    require(math.isfinite(dt) and math.isfinite(width) and dt > 0 and width > 0, "UNITS")
    require(all(len(raw[c]) == len(keys) and all(math.isfinite(a) for a in raw[c]) for c in COLS), "NONFINITE_COLUMNS")
    factor = -10. / (dt * width)
    require(len(mask["stress"]) == len(keys), "NATIVE_ROWS")
    def compare(measured, expected, scale):
        require(math.isfinite(measured) and math.isfinite(expected) and math.isfinite(scale)
                and abs(measured-expected) <= 1e-12 + 1e-12 * scale, "NATIVE_STRESS_RECONSTRUCTION")
    for yy, yx, old in zip(raw["yy"], raw["yx"], mask["stress"]):
        compare(yy+yx, factor*old, abs(yy)+abs(yx))
    totals = {c: math.fsum(raw[c]) for c in COLS}
    compare(totals["yy"]+totals["yx"], factor*math.fsum(mask["stress"]),
            math.fsum(abs(v) for c in ("yy","yx") for v in raw[c]))
    return totals


def match_old(folder, old):
    for name, expected in old.items():
        require((folder/name).read_bytes() == expected, "PREVIOUS_FILE_MISMATCH_" + name)


def original_masks(old):
    return {r["step"]: r["mask"] for r in json.loads(old["momentum.json"])}


def receipt(n, folder):
    return dict(status=STATUS, cells=n, steps=list(STEPS[n]), observer_sha256=digest(Path(__file__).read_bytes()),
                old_momentum_return_sha256=RETURN_SHA, basis_record_sha256=digest((folder/"probe.json").read_bytes()),
                regenerated={k:digest((folder/k).read_bytes()) for k in FILES})


def arm(m, prefix, pair, mods, hist, walls, old, n, folder):
    # m.arm installs its own subclass around this one. Before the native wall it
    # stores the selected rows in self.snapshot, as pinned by MOMENTUM_SHA.
    previous = prefix.Observer
    masks = original_masks(old)
    samples = []

    class StressObserver(previous):
        def advance(self, *args):
            step = len(self.rows)+1
            if step not in STEPS[n]:
                return super().advance(*args)
            x, _, _, elastic, ids, volume, grid, dt, _ = args
            projected = project(self.solver,x,elastic,ids,volume,grid,prefix.WIDTH)
            native_result = super().advance(*args)
            require(self.snapshot == masks[step], "PRIOR_NATIVE_MASK")
            row = subset(projected, self.snapshot)
            reduce_record(row,self.snapshot,dt,prefix.WIDTH)
            samples.append(dict(step=step, projection=row))
            return native_result

    prefix.Observer = StressObserver
    try:
        m.arm(prefix,pair,mods,hist,walls,n,folder)
    finally:
        prefix.Observer = previous
    match_old(folder,old)
    require([r["step"] for r in samples] == list(STEPS[n]), "SAMPLE_STEPS")
    prefix.write(folder/"probe.json",samples)
    prefix.write(folder/"probe_receipt.json",receipt(n,folder))


def read_arm(n, folder, old, prefix):
    match_old(folder,old)
    require(json.loads((folder/"probe_receipt.json").read_bytes()) == receipt(n,folder), "PROBE_RECEIPT")
    masks = original_masks(old)
    rows = json.loads((folder/"probe.json").read_bytes())
    require([r["step"] for r in rows] == list(STEPS[n]), "SAMPLE_STEPS")
    return {r["step"]:reduce_record(r["projection"],masks[r["step"]],prefix.DT[n],prefix.WIDTH) for r in rows}


def summarize(prefix, walls, totals):
    pairs = []
    for i,j in zip(STEPS[8],STEPS[16]):
        require(walls[8][i-1]["u"] == walls[16][j-1]["u"],"COMMON_DISPLACEMENT")
        delta = {k:totals[8][i][k]-totals[16][j][k] for k in COLS}
        pairs.append(dict(steps=[i,j], u=walls[8][i-1]["u"], delta_F8_minus_F16=delta,
                          compression_minus_one_MPa=-delta["unit_yy"], native_stress_MPa=delta["yy"]+delta["yx"]))
    return dict(status=STATUS, label="DEVELOPMENT_ONLY", samples=totals, paired=pairs,
                field_unit="one solver stress unit; tensile positive; symmetric unit shear",
                unit_response="MPa of positive upward wall pressure per +1 solver stress",
                scope="OBSERVED_NATIVE_MASK_ONLY", momentum_return_sha256=RETURN_SHA,
                u6_qualified=False, stage3_go=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command",required=True)
    for name in ("check","arm","read"):
        cmd = sub.add_parser(name)
        for key in ("repo","prior","momentum"):
            cmd.add_argument("--"+key,type=Path,required=True)
        if name in ("arm","read"):
            cmd.add_argument("--out",type=Path,required=True)
        if name == "arm":
            cmd.add_argument("--cells",type=int,choices=tuple(STEPS),required=True)
        if name == "read":
            cmd.add_argument("--run",type=Path,required=True)
    args = parser.parse_args()
    try:
        m,prefix,pair,mods = sources(args.repo)
        hist,walls = m.history(args.prior,prefix,pair)
        old = history(args.momentum,m,prefix,pair,hist,walls,mods["driver"].fixed_solver().LO)
        if args.command == "check":
            for n in STEPS:
                pair.setup_geometry(mods["driver"],mods["driver"].fixed_solver(),n)
            print("STRESS_PROBE_SOURCES_SEEDS_AND_HISTORIES_BOUND")
        elif args.command == "arm":
            arm(m,prefix,pair,mods,hist,walls,old[args.cells],args.cells,args.out)
            print(STATUS)
        else:
            totals = {n:read_arm(n,args.run/f"F{n}",old[n],prefix) for n in STEPS}
            prefix.write(args.out,summarize(prefix,walls,totals))
            print(STATUS)
    except (ArithmeticError,OSError,ValueError,RuntimeError,TypeError,KeyError,IndexError,tarfile.TarError) as exc:
        print("HOLD", str(exc) if str(exc).isupper() else type(exc).__name__)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
