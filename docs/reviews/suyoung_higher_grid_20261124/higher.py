"""Run only the two requested resolutions using the original setting-2 loading loop."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tarfile
from types import ModuleType, SimpleNamespace


PHYSICS = "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112"
RETURN = "882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af"
MANIFEST = "7d698c085e250be40fd7d2bfdad7ae84233ddaa847bed4939d69d0ac343834b3"
FLOOR = "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b"
PAIRS = {32:16, 48:24}
BUDGET = {32:14400, 48:57600}
DT = {32:.0005615917541198894, 48:.000374394502746593}
POINTS = {32:157241, 48:353437}
SEEDS = {
    32: ("db88719df5258e161d02eb6283107462aee72287c1f971012b5dcbd26c96ab15",
         "1eb7f65579e5f3ab21bf78b574bbd38cae32dddbdea0f1f0b0f975248ec3b656",
         "c62a544ec568939a74ae7b68e3a9b37ee7c94967e8698e0eeb5610937979c970"),
    48: ("6dd9b5663a31aaaf7999f54956103987b86450e1e58a40e4998f29a712128872",
         "7ea6a44d8e70c6a734e706f17ca1ff4a5e62488c6c3f39f562ea5969dea2ce25",
         "d519b618d6c3415d88a1c9e7d18c101a4aa46f0870e06cb59783b13968fcb3c1"),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prior_arms(path):
    with path.open("rb") as stream:
        need(hashlib.file_digest(stream, "sha256").hexdigest() == RETURN, "wrong original setting 2 return")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            def read(name):
                return archive.extractfile("run/" + name).read()
            s = json.loads(read("summary.json"))
            need(read("RELEASE").decode().strip() == s["release"] == PHYSICS
                 and sha(read("SOURCE_SHA256SUMS")) == s["source_manifest_sha256"] == MANIFEST
                 and read("screen.txt").splitlines()[-1] == b"COMMAND_RC=0"
                 and s["assessment"] == "PASS" and s["selected_setting"] == 2, "old gate identity")
            arms = {}
            for n in PAIRS.values():
                p = f"F{n}/"
                rec = json.loads(read(p+"target_receipt.json"))
                trace = read(p+"trace.csv")
                need(rec == s["arms"][str(n)] and rec["release"] == PHYSICS and rec["cells"] == n
                     and rec["setting"] == 2 and rec["gap_correction"] and not rec["distance_filter"]
                     and rec["floor_sha256"] == FLOOR and rec["status"] == "TARGET_BRACKETED"
                     and sha(trace) == rec["trace_sha256"] and sha(read(p+"result.json")) == rec["result_sha256"]
                     and sha(read(p+"observation.json")) == rec["observation_sha256"], "old arm receipt")
                arms[n] = rec, trace
            return arms


def expand_guard(raw):
    guard = b"cells not in (8, 12, 16, 24) or not"
    need(raw.count(guard) == 1, "unexpected grid guard")
    return raw.replace(guard, b"cells not in (8, 12, 16, 24, 32, 48) or not")


def setup(root, release):
    baseline = root/"baseline"
    need((baseline/"RELEASE").read_text().strip() == PHYSICS and
         sha((baseline/"SOURCE_SHA256SUMS").read_bytes()) == MANIFEST, "original package")
    folder = baseline/"docs/reviews/suyoung_u6a_gates_20261123"
    old = load(folder/"setting2_run.py")
    fine = load(baseline/"history"/old.FINE_PATH)
    ctx = fine.context(baseline/"history")
    raw = Path(ctx.floor.__file__).read_bytes()
    need(sha(raw) == FLOOR, "original nearest-owner floor")
    expanded = expand_guard(raw)
    # The pinned floor has a literal allowlist inside disk_boundary; execute the
    # same source with only that tuple extended, without changing the source file.
    floor = ModuleType("higher_grid_original_floor")
    floor.__file__ = ctx.floor.__file__
    exec(compile(expanded, floor.__file__, "exec"), floor.__dict__)
    ctx = ctx._replace(floor=floor)
    ctx.driver.GRIDS = (*ctx.driver.GRIDS, *PAIRS)
    fine.POINTS.update(POINTS)
    fine.DT.update(DT)
    fine.SEEDS.update(SEEDS)
    old.BUDGET.update(BUDGET)
    gap = load(folder/"gap_kernel.py")
    rule = load(baseline/old.REGISTERED_READER)
    force = load(root/"rule/suyoung_u6c_force_rule_20261122/force_rule.py")
    identity = dict(label="DEVELOPMENT_ONLY", release=release, physics_pin=PHYSICS, setting=2,
                    gap_correction=True, distance_filter=False, friction=.5, prior_return_sha256=RETURN,
                    original_floor_sha256=FLOOR, extended_floor_source_sha256=sha(expanded),
                    source_manifest_sha256=sha((root/"SOURCE_SHA256SUMS").read_bytes()),
                    u6_qualified=False, stage3_go=False, three_dimensional_go=False)
    return SimpleNamespace(old=old, fine=fine, ctx=ctx, gap=gap, rule=rule, force=force, identity=identity)


def native(env, receipt, trace):
    u, p = env.ctx.compare.read_native(trace, env.ctx.solver.WIDTH, receipt["wall_speed"], receipt["dt"],
                                       receipt["status"])
    need(receipt["bracket_steps"] == [len(u)-2,len(u)-1] and sha(trace) == receipt["trace_sha256"],
         "target steps or native trace")
    return list(zip(u, p, strict=True))


def read_pair(env, prior, run, n):
    folder = run/f"F{n}"
    need(not (folder/"incomplete.json").exists(), "incomplete arm")
    obs = json.loads((folder/"observation.json").read_bytes())
    _, dt, hashes = env.old.seed_and_clock(env, n)
    rec = env.old.target_receipt(env, n, folder, obs, dt, hashes, POINTS[n])
    need(rec == json.loads((folder/"target_receipt.json").read_bytes()), "new receipt mismatch")
    cr, ct = prior[PAIRS[n]]
    need(cr["dt"] == 2*dt and cr["wall_speed"] == rec["wall_speed"], "paired clocks or speed")
    pair = env.force.compare(native(env, cr, ct), native(env, rec, (folder/"trace.csv").read_bytes()))
    need(pair["comparison"] in ("WITHIN", "EXCEEDS") and math.isfinite(pair["ratio"]), "undefined pair")
    return dict(pair, coarse_trace_sha256=cr["trace_sha256"], fine_trace_sha256=rec["trace_sha256"],
                coarse_grid=PAIRS[n], fine_grid=n)


def outcome(pairs):
    need(pairs.keys() == PAIRS.keys(), "two complete higher pairs required")
    states = [p["comparison"] for p in pairs.values()]
    need(all(s in ("WITHIN","EXCEEDS") for s in states), "incomplete comparison")
    return dict(higher_pair_comparison="EXCEEDS" if "EXCEEDS" in states else "WITHIN",
                pairs={f"F{PAIRS[n]}_F{n}": p for n,p in pairs.items()},
                original_item6_pass=False, u6_qualified=False, stage3_go=False, three_dimensional_go=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("check","arm","summary"))
    parser.add_argument("root", type=Path)
    parser.add_argument("prior", type=Path)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--cells", type=int, choices=tuple(PAIRS))
    args = parser.parse_args()
    root = args.root.resolve()
    release = (root/"RELEASE").read_text().strip()
    prior = prior_arms(args.prior)
    env = setup(root, release)
    if args.mode == "check":
        # Exercise the packaged reader on an exact boundary before reserving a run.
        fine_check = [(0., 0.), (1., 20.), (2., 1000.)]
        for coarse_peak, expected in ((21., "WITHIN"), (21.01, "EXCEEDS")):
            check = env.force.compare([(0., 0.), (1., coarse_peak)], fine_check)
            need(check["comparison"] == expected and check["fine_peak_MPa"] == 20.
                 and check["union_knots"] == 2, "registered comparison boundary")
        for n, coarse in PAIRS.items():
            arrays, _, _ = env.old.seed_and_clock(env, n)
            boundary = env.ctx.floor.disk_boundary(env.ctx.solver, arrays[0], arrays[1], n)
            need(len(boundary.owners) == 49 * 256
                 and (boundary.groups == arrays[1][boundary.owners]).all(), "material surface ownership")
            rec, trace = prior[coarse]
            native(env, rec, trace)
            need(rec["dt"] == 2*DT[n], "coarse/fine clock")
        env.gap.GapProjector(env.ctx.kernel)
        print("ORIGINAL_SETTING2_AND_HIGHER_GRID_SEEDS_OK")
        return
    run = args.run
    need(run and (run/"RELEASE").read_bytes() == (root/"RELEASE").read_bytes()
         and (run/"SOURCE_SHA256SUMS").read_bytes() == (root/"SOURCE_SHA256SUMS").read_bytes(),
         "run release or manifest")
    if args.mode == "arm":
        n = args.cells
        need(n in PAIRS, "one higher arm required")
        env.old.run_arm(env, n, run/f"F{n}")
        env.old.write_json(run/f"pair_F{n}.json",read_pair(env, prior, run, n))
    else:
        pairs = {n:read_pair(env, prior, run, n) for n in PAIRS}
        need(all(p == json.loads((run/f"pair_F{n}.json").read_bytes()) for n,p in pairs.items()),
             "saved pair mismatch")
        summary = outcome(pairs)
        env.old.write_json(run/"summary.json", {**env.identity, "results": summary})
        for n,p in pairs.items():
            print(f"F{PAIRS[n]}_F{n} {p['comparison']} {100*p['ratio']:.8f}%")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ArithmeticError, RuntimeError, KeyError, TypeError, ValueError, tarfile.TarError) as exc:
        print("INCOMPLETE", type(exc).__name__, str(exc), file=sys.stderr)
        raise SystemExit(4)
