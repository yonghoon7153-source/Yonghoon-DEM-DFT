"""Observe signed native P2G momentum on the first bottom-wall mask at five saved steps."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tarfile

import numpy as np


PREFIX_PATH = "docs/reviews/suyoung_first_grid_return_20261122/observe_prefix.py"
PREFIX_SHA = "b257e8b8cbaf9c3e04e722cc3061b2119fb310b4ec07a7ace60e8c2b90a04f3e"
PREFIX_PIN = "e1db2841252d7f5babfbc4e55ad401540040ca24"
PRIOR = "0d415250759821b9db816e6a13d43ca190e983a7389914c5c3357b697399a5ae"
TARGETS = {8: (269, 270), 16: (538, 539, 540)}
TERMS = ("translation", "apic", "stress")
STATUS = "DEVELOPMENT_MOMENTUM_OBSERVED"
FACTOR = 2.0
ATOL_MPA = 1e-12
RTOL = 1e-12


def require(ok, issue):
    if not ok:
        raise ValueError(issue)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def sources(repo):
    path = repo / PREFIX_PATH
    require(sha(path.read_bytes()) == PREFIX_SHA, "PREFIX_OBSERVER_IDENTITY")
    spec = importlib.util.spec_from_file_location("prior_wall_observer", path)
    prefix = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prefix)
    pair, mods = prefix.sources(repo)
    return prefix, pair, mods


def history(prior, prefix, pair):
    traces, rows = {}, {}
    with prior.open("rb") as source:
        require(hashlib.file_digest(source, "sha256").hexdigest() == PRIOR, "WRONG_PRIOR")
        source.seek(0)
        with tarfile.open(fileobj=source, mode="r:gz") as archive:
            def read(name):
                member = archive.getmember("run/" + name)
                require(member.isfile(), "INVALID_PRIOR_MEMBER")
                return archive.extractfile(member).read()

            origin = dict(line.split("=", 1) for line in read("origin.txt").decode("ascii").splitlines())
            require(origin["release"] == PREFIX_PIN and origin["physics_pin"] == prefix.PIN
                    and origin["prior_sha256"] == prefix.PRIOR and origin["kernel_sha256"] == prefix.KERNEL,
                    "PRIOR_SOURCE_IDENTITY")
            for n in TARGETS:
                raw = traces[n] = read(f"F{n}/trace.csv")
                wall = read(f"F{n}/wall_observations.json")
                receipt = json.loads(read(f"F{n}/prefix_receipt.json"))
                require(receipt["status"] == prefix.STATUS and receipt["observer_sha256"] == PREFIX_SHA
                        and receipt["raw_prefix_sha256"] == sha(raw) and receipt["observations_sha256"] == sha(wall)
                        and receipt["geometry"] == pair.expected_geometry(n) and receipt["mapping"] == "ORIGINAL",
                        "PRIOR_RECORD_IDENTITY")
                rows[n] = json.loads(wall)
                prefix.validate_rows(rows[n], n, prefix.validate_prefix(raw, n, traces))
            require(json.loads(read("summary.json")) == prefix.summarize(rows[8], rows[16]), "PRIOR_SUMMARY")
    return traces, rows


def scatter(solver, x, v, affine, elastic, ids, volume, grid, dt, lid):
    """Observe incoming arrays without mutating them. Preserve the native fused sum separately."""
    nodes, weights, _, offset = solver.model.stencil(x, grid)
    key, slots = np.unique((ids[:, None] * (grid + 1)**2 + nodes).ravel(), return_inverse=True)
    flat = slots.ravel()
    wm = volume[:, None] * weights
    tau = solver.model.stress(elastic)
    transfer = volume[:, None, None] * (affine - dt * 4 * grid**2 * tau)

    def send(matrix):
        return weights[:, :, None] * np.einsum("pij,pqj->pqi", matrix, offset)

    def collect(data):
        return np.bincount(flat, weights=data.ravel(), minlength=len(key))

    translation = wm[:, :, None] * v[:, None, :]
    fused = translation + send(transfer)
    return dict(key=key, mass=collect(wm), grid=grid, native_y=collect(fused[:, :, 1]),
                translation=collect(translation[:, :, 1]),
                apic=collect(send(volume[:, None, None] * affine)[:, :, 1]),
                stress=collect(send(volume[:, None, None] * (-dt * 4 * grid**2 * tau))[:, :, 1]))


def capture_first(state, mass, xy, vel, lo):
    grid, key = state["grid"], state["key"]
    native_xy = np.column_stack(np.divmod(key % (grid + 1)**2, grid + 1)) / grid
    expected = np.divide(state["native_y"], mass, out=np.zeros_like(mass), where=mass > 0.)
    require(np.array_equal(mass, state["mass"]) and np.array_equal(xy, native_xy)
            and np.array_equal(vel[:, 1], expected), "NATIVE_P2G_ALIGNMENT")
    mask = (mass > 0.) & (xy[:, 1] <= lo) & (vel[:, 1] < 0.)
    return dict(grid=grid, keys=key[mask].tolist(), mass=mass[mask].tolist(), vy=vel[mask, 1].tolist(),
                **{name: state[name][mask].tolist() for name in TERMS})


def pressure_balance(delta, magnitude, factor):
    require(math.isfinite(delta) and math.isfinite(magnitude) and abs(delta) * factor
            <= ATOL_MPA + RTOL * factor * magnitude, "SIGNED_RECONSTRUCTION")


def reduce_mask(record, dt, width, lo):
    require(all(math.isfinite(z) and z > 0 for z in (dt, width)), "UNITS")
    grid, keys = record["grid"], record["keys"]
    require(type(grid) is int and grid > 0 and type(keys) is list and keys == sorted(set(keys)), "MASK_KEYS")
    nn = (grid + 1)**2
    require(all(type(k) is int and 0 <= k < 49 * nn and (k % nn) % (grid + 1) / grid <= lo for k in keys),
            "MASK_IDENTITY")
    columns = ("mass", "vy", *TERMS)
    require(all(len(record[k]) == len(keys) and all(math.isfinite(v) for v in record[k]) for k in columns),
            "MASK_COLUMNS")
    require(all(m > 0. and v < 0. for m, v in zip(record["mass"], record["vy"])), "MASK_DOMAIN")
    factor = 10. / (dt * width)
    terms = {k: -math.fsum(record[k]) for k in TERMS}
    native = [-m * v for m, v in zip(record["mass"], record["vy"])]
    triplets = list(zip(*(record[k] for k in TERMS)))
    for j, terms_y in zip(native, triplets):
        pressure_balance(j + math.fsum(terms_y), math.fsum(map(abs, terms_y)), factor)
    native_j = math.fsum(native)
    magnitude = math.fsum(abs(z) for row in triplets for z in row)
    pressure_balance(native_j - math.fsum(terms.values()), magnitude, factor)
    without = {}
    for i, name in enumerate(TERMS):
        without[name] = -math.fsum(value for row in triplets for k, value in enumerate(row) if k != i)
        pressure_balance(native_j - without[name] - terms[name], magnitude, factor)
    total_m = math.fsum(record["mass"])
    return dict(count=len(keys), M=total_m, mean_down=native_j / total_m if total_m else None,
                native_J=native_j, J=terms, without_J=without, p_MPa={k: v * factor for k, v in terms.items()},
                residual_MPa=(native_j - math.fsum(terms.values())) * factor,
                mask_sha256=sha(np.asarray(keys, dtype="<i8").tobytes()))


def direction(delta):
    translation_apic = math.fsum([delta["translation"], delta["apic"]])
    stress = delta["stress"]
    gap = math.fsum(delta.values())
    parts = sorted([("TRANSLATION_APIC", translation_apic), ("STRESS", stress)], key=lambda p: -abs(p[1]))
    (leader, high), (_, low) = parts
    cancellation = math.fsum(map(abs, delta.values())) / abs(gap) if gap else None
    separated = abs(high) >= FACTOR * abs(low)
    label = leader if gap > ATOL_MPA and high > 0 and cancellation < FACTOR and separated else "UNRESOLVED"
    return dict(label=label, descriptive_factor=FACTOR, translation_apic_MPa=translation_apic, stress_MPa=stress,
                signed_pre_MPa=gap, dominance_ratio=abs(high / low) if low else None, weaker_is_zero=low == 0.,
                cancellation_ratio=cancellation, total_is_zero=gap == 0.)


def compare_sample(prefix, row, raw, n, lo):
    require(raw["grid"] == 10 * n, "RESOLUTION")
    reduced = reduce_mask(raw, prefix.DT[n], prefix.WIDTH, lo)
    pre, post = row["pre"], row["post"]
    require(reduced["count"] == pre["count"] and reduced["M"] == pre["M"], "NATIVE_COUNT_MASS")
    require((reduced["mean_down"] is None and pre["mean_down"] is None)
            or (pre["mean_down"] is not None and reduced["mean_down"] is not None
                and math.isclose(reduced["mean_down"], pre["mean_down"], rel_tol=RTOL, abs_tol=0.)),
            "NATIVE_MEAN")
    factor = 10. / (prefix.DT[n] * prefix.WIDTH)
    pressure_balance(reduced["native_J"] - pre["J"], pre["J"], factor)
    post_p = post["J"] * factor
    reconstructed = math.fsum([*reduced["p_MPa"].values(), post_p])
    magnitude = math.fsum([*(abs(v) for v in reduced["p_MPa"].values()), post_p])
    pressure_balance(reconstructed - row["p_MPa"], magnitude, 1.)
    return dict(step=row["step"], u=row["u"], pre=pre, post=post, first_wall=reduced,
                post_MPa=post_p, native_total_MPa=row["p_MPa"], reconstructed_MPa=reconstructed)


def arm(prefix, pair, mods, hist, walls, n, folder):
    previous = prefix.Observer
    samples = []

    class MomentumObserver(previous):
        def advance(self, *args):
            step = len(self.rows) + 1
            self.incoming = scatter(self.solver, *args) if step in TARGETS[n] else None
            self.snapshot = None
            result = super().advance(*args)
            if self.incoming is not None:
                require(self.rows[-1] == walls[n][step - 1] and self.snapshot is not None, "PRIOR_WALL_PHASES")
                compare_sample(prefix, self.rows[-1], self.snapshot, n, self.solver.LO)
                samples.append(dict(step=step, mask=self.snapshot))
            return result

        def wall(self, mass, xy, vel, lid, speed):
            if not self.events and self.incoming is not None:
                self.snapshot = capture_first(self.incoming, mass, xy, vel, self.solver.LO)
            return super().wall(mass, xy, vel, lid, speed)

    prefix.Observer = MomentumObserver
    try:
        prefix.arm(pair, mods, hist, n, folder)
    finally:
        prefix.Observer = previous
    require(prefix.checked_records(pair, hist, n, folder) == walls[n], "PRIOR_WALL_PHASES")
    require([r["step"] for r in samples] == list(TARGETS[n]), "SAMPLES")
    prefix.write(folder / "momentum.json", samples)
    prefix.write(folder / "momentum_receipt.json", receipt(n, folder))


def receipt(n, folder):
    return dict(status=STATUS, samples=TARGETS[n], cells=n, prior_sha256=PRIOR,
                adapter_sha256=sha(Path(__file__).read_bytes()), prefix_observer_sha256=PREFIX_SHA,
                prefix_receipt_sha256=sha((folder / "prefix_receipt.json").read_bytes()),
                sample_record_sha256=sha((folder / "momentum.json").read_bytes()))


def checked(prefix, pair, hist, walls, n, folder, lo):
    require(prefix.checked_records(pair, hist, n, folder) == walls[n], "PRIOR_WALL_PHASES")
    rec = json.loads((folder / "momentum_receipt.json").read_bytes())
    require(json.dumps(rec, sort_keys=True) == json.dumps(receipt(n, folder), sort_keys=True), "SAMPLE_RECEIPT")
    raw = json.loads((folder / "momentum.json").read_bytes())
    require([r["step"] for r in raw] == list(TARGETS[n]), "SAMPLES")
    return {r["step"]: compare_sample(prefix, walls[n][r["step"] - 1], r["mask"], n, lo) for r in raw}


def summarize(prefix, walls, samples):
    pairs = []
    for coarse_step, fine_step in ((269, 538), (270, 540)):
        coarse, fine = samples[8][coarse_step], samples[16][fine_step]
        require(coarse["u"] == fine["u"], "NATIVE_PAIR_LOCATION")
        delta = {k: coarse["first_wall"]["p_MPa"][k] - fine["first_wall"]["p_MPa"][k] for k in TERMS}
        post = coarse["post_MPa"] - fine["post_MPa"]
        total = coarse["native_total_MPa"] - fine["native_total_MPa"]
        pressure_balance(math.fsum([*delta.values(), post]) - total,
                         math.fsum(abs(v) for r in (coarse, fine) for v in [*r["first_wall"]["p_MPa"].values(), r["post_MPa"]]), 1.)
        pairs.append(dict(u=coarse["u"], steps=[coarse_step, fine_step], signed_pre_delta_MPa=delta,
                          signed_post_delta_MPa=post, native_total_delta_MPa=total, description=direction(delta)))
    labels = [p["description"]["label"] for p in pairs]
    return dict(status=STATUS, label="DEVELOPMENT_ONLY", prior_sha256=PRIOR,
                signed_direction="F8_MINUS_F16; POSITIVE_WALL_IMPULSE_UPWARD",
                samples=samples, paired=pairs, first_crossing=prefix.summarize(walls[8], walls[16])["first_exceedance"],
                convention=dict(factor=FACTOR, positive_pre_gap_floor_MPa=ATOL_MPA,
                                dominance_at_least=FACTOR, cancellation_strictly_below=FACTOR),
                reconstruction_tolerance=dict(absolute_MPa=ATOL_MPA, relative=RTOL),
                descriptive_direction=labels[0] if labels[0] == labels[1] else "UNRESOLVED",
                assessment="INSTANTANEOUS_SIGNED_ACCOUNTING_ONLY", u6_qualified=False, stage3_go=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "arm", "read"):
        cmd = sub.add_parser(name)
        for key in ("repo", "prior"):
            cmd.add_argument("--" + key, required=True, type=Path)
        if name in ("arm", "read"):
            cmd.add_argument("--out", required=True, type=Path)
        if name == "arm":
            cmd.add_argument("--cells", required=True, type=int, choices=tuple(TARGETS))
        if name == "read":
            cmd.add_argument("--run", required=True, type=Path)
    args = parser.parse_args()
    try:
        prefix, pair, mods = sources(args.repo)
        hist, walls = history(args.prior, prefix, pair)
        if args.command == "check":
            for n in TARGETS:
                pair.setup_geometry(mods["driver"], mods["driver"].fixed_solver(), n)
            print("MOMENTUM_SOURCES_SEEDS_AND_PRIOR_BOUND")
        elif args.command == "arm":
            arm(prefix, pair, mods, hist, walls, args.cells, args.out)
            print(STATUS)
        else:
            lo = mods["driver"].fixed_solver().LO
            samples = {n: checked(prefix, pair, hist, walls, n, args.run / f"F{n}", lo) for n in TARGETS}
            prefix.write(args.out, summarize(prefix, walls, samples))
            print(STATUS)
    except (OSError, ValueError, RuntimeError, ArithmeticError, KeyError, IndexError, TypeError, tarfile.TarError) as exc:
        reason = str(exc) if str(exc).isupper() else type(exc).__name__
        print("HOLD", reason)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
