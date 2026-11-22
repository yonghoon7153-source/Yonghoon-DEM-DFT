"""Recalculate the two matched-displacement pressure splits from the author return."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory

RETURN_SHA = "0d415250759821b9db816e6a13d43ca190e983a7389914c5c3357b697399a5ae"
SCREEN_SHA = "0d90a74810dab7a0f6a1d074e878c7e03fce9562d6f6031d4b706bcf3cc79f33"
MANIFEST_SHA = "413f06a1e2496d6c5bff75a0b4fe28a10be265d546f742f39b9da1d6ec11682b"
RELEASE = "e1db2841252d7f5babfbc4e55ad401540040ca24"
PHYSICS = "99938d3bd4cb1cbba0e1377be2ff9dac9b228d2f"
OBSERVER = "docs/reviews/suyoung_first_grid_return_20261122/observe_prefix.py"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def analyze(repo, delivery, prior):
    archive = delivery / "suyoung_wall_prefix_result.tar.gz"
    screen = (delivery / "screen.txt").read_bytes()
    checklist = dict(line.split("  ", 1)[::-1] for line in (delivery / "SHA256SUMS").read_text("ascii").splitlines())
    require(checklist == {archive.name: RETURN_SHA, "screen.txt": SCREEN_SHA}, "Delivery checklist mismatch")
    require(digest(screen) == SCREEN_SHA, "External screen mismatch")

    with archive.open("rb") as fp, TemporaryDirectory() as scratch:
        require(hashlib.file_digest(fp, "sha256").hexdigest() == RETURN_SHA, "Return mismatch")
        fp.seek(0)
        run = Path(scratch)
        with tarfile.open(fileobj=fp, mode="r:gz") as tar:
            def member(name):
                item = tar.getmember("run/" + name)
                require(item.isfile(), "Expected regular file")
                return tar.extractfile(item).read()
            require(member("screen.txt") == screen, "Internal screen mismatch")
            manifest = member("SOURCE_SHA256SUMS")
            require(digest(manifest) == MANIFEST_SHA, "Source manifest mismatch")
            for line in manifest.decode("ascii").splitlines():
                expected, name = line.split("  ", 1)
                data = ((RELEASE + "\n" + PHYSICS + "\n").encode("ascii")
                        if name == "RELEASE" else (repo / name).read_bytes())
                require(digest(data) == expected, "Source identity mismatch for " + name)
            origin = dict(line.split("=", 1) for line in member("origin.txt").decode("ascii").splitlines())
            require(origin["release"] == RELEASE and origin["physics_pin"] == PHYSICS
                    and origin["source_sums"] == MANIFEST_SHA, "Run origin mismatch")
            saved_summary = member("summary.json")
            for grid in ("F8", "F16"):
                folder = run / grid
                folder.mkdir()
                for name in ("prefix_receipt.json", "wall_observations.json", "trace.csv"):
                    (folder / name).write_bytes(member(grid + "/" + name))

        observer = module(repo / OBSERVER)
        pair, _ = observer.sources(repo)
        history = observer.history(prior)
        rows = {n: observer.checked_records(pair, history, n, run / f"F{n}") for n in (8, 16)}
        summary = observer.summarize(rows[8], rows[16])
        require(summary == json.loads(saved_summary), "Recomputed native summary mismatch")
        factors = module(Path(__file__).with_name("pressure_factors.py"))
        result = factors.report(rows[8], rows[16], observer.DT[8], observer.DT[16], observer.WIDTH, summary)
        result.update(release=RELEASE, physics_pin=PHYSICS, return_sha256=RETURN_SHA, screen_sha256=SCREEN_SHA,
                      prior_return_sha256=observer.PRIOR, observation_steps={n: len(r) for n, r in rows.items()},
                      u6_qualified=False, stage3_go=False, label="DEVELOPMENT_ONLY")
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "return-dir", "prior", "out"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.repo, args.return_dir, args.prior)
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, allow_nan=False, sort_keys=True, indent=2)
        stream.write("\n")
