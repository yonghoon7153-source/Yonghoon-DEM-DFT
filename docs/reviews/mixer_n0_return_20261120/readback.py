"""Read one pinned N0 return locally with the approved B observer and E0 reference."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

CASE = "PRECAL_N0"
INTERVAL = 32976
FULL = "71c14f4b3946921222b087f2d0f61edc07b932c382ea993f23e56c3185511262"
DECK = "adbbc8fa8f46730779fbf4f028f95a7aaf90c27ef2697c0dbe21a9ae1b5c6de3"
META = "cc5b3e4d45cdc3859541b8dcc8b76c54dcdcec057fc40e130b5ba74c70752c90"
ALL = {f"post/mix_{i*INTERVAL}.liggghts" for i in range(1, 235)}
SELECTED = {f"post/mix_{i*INTERVAL}.liggghts" for i in [34, *range(134,234)]}
CONTROL = {"in.mixer", "deck_meta.json", "log.liggghts", "n_expected", "job_end.json"}
BASE = Path(__file__).resolve().parent


def require(value, reason):
    if not value:
        raise ValueError(reason)


def hash_file(f):
    h = hashlib.sha256()
    for part in iter(lambda: f.read(1048576), b""):
        h.update(part)
    return h.hexdigest()


def verify_packet(base):
    for line in (base / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        expected, name = line.split("  ", 1)
        path = base / name
        require(re.fullmatch(r"[a-f0-9]{64}", expected) and path.is_file(), "packet member missing")
        with path.open("rb") as f:
            require(hash_file(f) == expected, f"packet hash mismatch: {name}")


def stage(tar, case, reserve=256 * 1024**2):
    names = set()
    frame_names = set()
    for m in tar:
        pieces = m.name.split("/")
        require(m.isfile() and pieces[0] == CASE and len(pieces) >= 2
                and all(p not in ("", ".", "..") and "\\" not in p for p in pieces)
                and m.name not in names, "invalid or duplicate archive member")
        names.add(m.name)
        relative = "/".join(pieces[1:])
        if relative.startswith("post/mix_") and relative.endswith(".liggghts"):
            frame_names.add(relative)
        if relative not in CONTROL | SELECTED:
            continue
        require(shutil.disk_usage(case).free >= reserve + m.size, "insufficient local scratch space")
        target = case / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with tar.extractfile(m) as src, target.open("xb") as dst:
            shutil.copyfileobj(src, dst, 1024**2)
        require(target.stat().st_size == m.size, "incomplete staged member")
    require(frame_names == ALL, "234 exact frame names required")
    require(all((case / p).is_file() for p in CONTROL - {"n_expected"}), "missing case metadata")
    return len(frame_names)


def main(archive, destination, scratch):
    import numpy
    import scipy
    require(not destination.exists(), "return file exists")
    verify_packet(BASE)
    receipt = {"case": CASE, "job_id": "367547", "status": "TECH", "development_only": True,
               "scientific_runtime": {"python": sys.version.split()[0], "numpy": numpy.__version__,
                                      "scipy": scipy.__version__}}
    try:
        with tempfile.TemporaryDirectory(prefix="n0_", dir=scratch) as tmp, archive.open("rb") as src:
            # Read and unpack from the same open file, never the source path a second time.
            key = lambda: (os.fstat(src.fileno()).st_size, os.fstat(src.fileno()).st_mtime_ns)
            before = key()
            require(hash_file(src) == FULL, "full archive hash mismatch")
            receipt["full_sha256"] = FULL
            src.seek(0)
            case = Path(tmp) / CASE
            case.mkdir()
            with tarfile.open(fileobj=src, mode="r|gz") as tar:
                receipt["exact_frame_names"] = stage(tar, case)
            require(key() == before, "archive changed during staging")
            for name, digest in [("in.mixer", DECK), ("deck_meta.json", META)]:
                with (case / name).open("rb") as f:
                    require(hash_file(f) == digest, "N0 approved metadata mismatch")
            end = json.loads((case / "job_end.json").read_bytes())
            require(type(end.get("returncode")) is int and end["returncode"] == 0, "runner rc mismatch")
            command = [sys.executable, "-I", "-X", "utf8", "-B",
                       str(BASE / "scripts/mixer_precal_observe.py"), "--case", CASE,
                       "--run", str(case), "--reference", str(BASE / "E0")]
            observed = subprocess.run(command, capture_output=True, check=False)
            receipt["observer_rc"] = observed.returncode
            if not observed.stdout:
                raise ValueError(f"observer returned no JSON (rc {observed.returncode})")
            obs = json.loads(observed.stdout)
            receipt["observer_status"] = obs["status"]
            if obs["status"] != "OK":
                require(obs["status"] in ("UNDEFINED", "TECH"), "unknown observer status")
                receipt.update(status=obs["status"], reasons=obs.get("reasons", []))
            else:
                require(observed.returncode == 0, "observer rc/status mismatch")
                prov = obs["provenance"]
                used = {f"post/mix_{x['step']}.liggghts" for x in prov["frames"]}
                require(used == SELECTED and len(prov["frames"]) == 101, "frozen bin membership mismatch")
                ref = prov["reference_frames"]
                require(len(ref) == 1 and ref[0]["step"] == 1121000, "reference t0 mismatch")
                expected = json.loads((BASE / "e0_reference_variance.json").read_bytes())
                grids = obs["mixing"]["grids"]
                require([g["grid"] for g in grids] == [g["grid"] for g in expected], "grid mismatch")
                require(all(math.isclose(g["SR"], e["raw_variance"], rel_tol=1e-12, abs_tol=1e-14)
                            for g, e in zip(grids, expected)), "E0 variance cross-check mismatch")
                receipt.update(status="OK", source_sha256={k:v["sha256"] for k,v in prov["module_sha256"].items()},
                               n0_frames=[{"step": x["step"], "sha256": x["sha256"]} for x in prov["frames"]],
                               e0_frame={"step":ref[0]["step"], "sha256":ref[0]["sha256"]},
                               counts=obs["counts"], reference_counts=obs["reference_counts"],
                               contact=obs["contact"], mixing=obs["mixing"], reference_variance_crosscheck=True)
    except (OSError, ValueError, KeyError, tarfile.TarError, EOFError) as exc:
        receipt.update(status="TECH", reasons=[str(exc)])
    with destination.open("x", encoding="utf-8") as out:
        json.dump(receipt, out, indent=2, ensure_ascii=False, allow_nan=False)
        out.write("\n")
    print("DEVELOPMENT_READBACK=" + receipt["status"])
    return 0 if receipt["status"] == "OK" else 2


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: readback.py FULL_ARCHIVE NEW_JSON SCRATCH_DIRECTORY")
    raise SystemExit(main(*(Path(x) for x in sys.argv[1:])))
