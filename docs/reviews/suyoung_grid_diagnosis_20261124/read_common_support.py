"""One read-only diagnostic on the two approved setting-2 development returns."""
import argparse
from contextlib import contextmanager
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import subprocess
import tarfile
import tempfile


OLD = ("eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112", "suyoung_u6a_setting2_result.tar.gz",
       "882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af",
       "711488b61bf077172335d60de019ca06f7004de4a118f8c15d70268c84b6758c")
NEW = ("182be9d50d5838e1dbfeb246eaf6e9c13dab4bc2", "suyoung_setting2_contact_result.tar.gz",
       "fc8e3d67a775eef6c67f171b64e382aba589949d5c8ece82e6a32c6d6546e669",
       "56b52d23a531baafc8ab93e8615a56039d6cddbd2769fd866d0b9f3308b6835d")
RULE = "suyoung_u6c_force_rule_20261122/force_rule.py"
NATIVE = "suyoung_floor_full_20261123/full_compare.py"
FILES = {RULE: "145b5fe6f456e8b66c2a8cc422ff88648c82d07c4420482f06bc6da7a5b1b6db",
         NATIVE: "f3eb1aa342e97e5accd9619230b695e523d9113035937daf676b29c88b498d3a",
         "suyoung_u6c_doubling_readback_20261122/doubling.py": "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda",
         "suyoung_u6c_force_rule_20261122/rule.json": "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4"}
TOL = 1e-12


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(repo, path):
    return subprocess.check_output(["git", "-c", "safe.directory=" + repo.resolve().as_posix(),
                                    "-C", str(repo), "show", NEW[0] + ":docs/reviews/" + path])


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextmanager
def official_readers(repo):
    with tempfile.TemporaryDirectory() as tmp:
        for path, checksum in FILES.items():
            data = blob(repo, path)
            require(sha(data) == checksum, "registered reader mismatch: " + path)
            dest = Path(tmp, path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        yield load_module(Path(tmp, RULE)), load_module(Path(tmp, NATIVE))


def manifest(data):
    result = {}
    for line in data.decode("ascii").splitlines():
        value, name = line.split("  ", 1)
        name = name.removeprefix("./")
        require(name not in result, "duplicate checksum: " + name)
        result[name] = value
    return result


def read_return(folder, identity):
    pin, name, checksum, screen_hash = identity
    raw = (folder / name).read_bytes()
    screen = (folder / "screen.txt").read_bytes()
    require(manifest((folder / "SHA256SUMS").read_bytes()) == {name: checksum, "screen.txt": screen_hash}
            and sha(raw) == checksum and sha(screen) == screen_hash, "return identity: " + name)
    files = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        for member in archive:
            if member.isdir():
                continue
            require(member.isfile() and member.name.startswith("run/") and member.name not in files,
                    "invalid return member")
            files[member.name] = archive.extractfile(member).read()
    require(files["run/RELEASE"].decode().strip() == pin and files["run/screen.txt"] == screen,
            "release or screen mismatch")
    if identity == NEW:
        checks = manifest(files["run/SHA256SUMS"])
        actual = {path[4:]: sha(data) for path, data in files.items() if path != "run/SHA256SUMS"}
        require(checks == actual, "candidate inner manifest")
    return files


def read_arm(files, identity, n, native):
    directory = f"run/F{n}/"
    rec = json.loads(files[directory + "target_receipt.json"])
    require(rec["release"] == identity[0] and rec["cells"] == n and rec["status"] == "TARGET_BRACKETED"
            and rec["setting"] == 2 and rec["gap_correction"] and not rec["distance_filter"], "arm identity")
    require(rec == json.loads(files["run/summary.json"])["arms"][str(n)], "arm/summary mismatch")
    manifest_key = "package_manifest_sha256" if identity == NEW else "source_manifest_sha256"
    require(rec[manifest_key] == sha(files["run/SOURCE_SHA256SUMS"]), "source manifest")
    for filename, key in (("trace.csv", "trace_sha256"), ("result.json", "result_sha256"),
                          ("observation.json", "observation_sha256")):
        require(sha(files[directory + filename]) == rec[key], f"F{n} {filename} hash")
    trace = files[directory + "trace.csv"]
    width = float(next(csv.DictReader(io.StringIO(trace.decode("ascii"))))["height"])
    u, pressure = native.read_native(trace, width, rec["wall_speed"], rec["dt"], rec["status"])
    require(rec["bracket_steps"] == [len(u)-2, len(u)-1], "wrong target bracket")
    return list(zip(u, pressure, strict=True)), rec


def common_metrics(grid, coarse, fine):
    delta = [a - b for a, b in zip(coarse, fine, strict=True)]
    err = max(range(len(grid)), key=lambda i: abs(delta[i]))
    ref = max(range(len(grid)), key=lambda i: abs(fine[i]))
    require(abs(fine[ref]) > 0, "zero common reference")
    return {"N_MPa": abs(delta[err]), "D_MPa": abs(fine[ref]), "first_u_N": grid[err],
            "first_u_D": grid[ref]}, err


def decompose(rule, old, new, registered=None):
    originals = [rule.compare(*old), rule.compare(*new)]
    if registered is not None:
        require(originals == registered, "native registered readback mismatch")
    require(all(r["comparison"] != "HOLD" for r in originals), "invalid native pair")
    curves = [*old, *new]
    end = min(c[-1][0] for c in curves)
    require(end > 0, "no positive common interval")
    grid = sorted({u for c in curves for u, _ in c if u <= end})
    pressures = []
    for c in curves:
        axis = [u for u, _ in c]
        pressures.append([rule.curves.interpolate(u, axis, c) for u in grid])
    om, oi = common_metrics(grid, *pressures[:2])
    nm, ni = common_metrics(grid, *pressures[2:])
    n0, d0, n1, d1 = om["N_MPa"], om["D_MPa"], nm["N_MPa"], nm["D_MPa"]
    r0, r1 = [r["ratio"] for r in originals]
    a = (n1 - n0) / d0
    b = n1 * (1/d1 - 1/d0)
    c = (r1 - n1/d1) - (r0 - n0/d0)
    residual = (a + b + c) - (r1 - r0)
    require(abs(residual) <= TOL, "A+B+C closure")
    points = []
    for i in sorted({oi, ni}):
        oc, of, nc, nf = [p[i] for p in pressures]
        dc, df = nc-oc, nf-of
        signed_delta = (nc-nf) - (oc-of)
        require(abs((dc-df) - signed_delta) <= TOL, "signed residual at fixed displacement")
        points.append(dict(u=grid[i], old_peak=i == oi, new_peak=i == ni, old_coarse_MPa=oc, old_fine_MPa=of,
                           new_coarse_MPa=nc, new_fine_MPa=nf, delta_coarse_MPa=dc, delta_fine_MPa=df,
                           delta_signed_gap_MPa=signed_delta))
    return dict(original_intervals=dict(old=originals[0], new=originals[1]),
                common_end_u=end, common_knots=len(grid), common_old=om, common_new=nm,
                A=a, B=b, C=c, delta_ratio=r1-r0, closure_residual=residual, matched_extrema=points)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "old_return", "new_return", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    require(not args.output.exists(), "output already exists")
    old, new = read_return(args.old_return, OLD), read_return(args.new_return, NEW)
    old_evidence = json.loads(blob(args.repo, "suyoung_u6c_setting2_readback_20261123/receipt.json"))
    new_pairs = json.loads(new["run/summary.json"])["pair_results"]
    result = dict(label="DEVELOPMENT_ONLY", diagnostic_pin="867c603da43cba4f1b9dcf2320cdaa733d949d99",
                  registered_reader_files=FILES, archive_sha256=dict(old=OLD[2], new=NEW[2]),
                  arms={}, pairs={}, new_loading_runs=0)
    with official_readers(args.repo) as (rule, native):
        for n in (8, 12):
            key = f"F{n}_F{2*n}"
            try:
                old_curves, new_curves = [], []
                for g in (n, 2*n):
                    oc, ore = read_arm(old, OLD, g, native)
                    nc, nre = read_arm(new, NEW, g, native)
                    require(all(ore[k] == nre[k] for k in ("geometry_sha256", "points", "wall_speed", "dt")),
                            "different seed or clock across models")
                    require(all(ore[k] == v for k,v in old_evidence["F_evidence_sha256"][f"F{g}"].items()),
                            "original receipt identity mismatch")
                    result["arms"][f"F{g}"] = dict(old_trace_sha256=ore["trace_sha256"],
                                                  new_trace_sha256=nre["trace_sha256"],
                                                  old_rows=len(oc), new_rows=len(nc))
                    old_curves.append(oc)
                    new_curves.append(nc)
                registered = [old_evidence["registered_pairs"][key], new_pairs[key]]
                result["pairs"][key] = decompose(rule, old_curves, new_curves, registered)
            except (ValueError, KeyError, ArithmeticError) as exc:
                result["pairs"][key] = {"status": "HOLD", "reason": str(exc)}
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, indent=2, allow_nan=False)
        output.write("\n")
    return int(any(p.get("status") == "HOLD" for p in result["pairs"].values()))


if __name__ == "__main__":
    raise SystemExit(main())
