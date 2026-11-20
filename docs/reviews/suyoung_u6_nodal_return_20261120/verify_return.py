"""Read the nodal F12/F16 receipts, recompute endpoints, and compare source bytes."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import tarfile
import zipfile


PIN = "00f0a1758349079a10d9c3fe9d1424620117dd27"
SOURCE_SHA = "e1f5c488dff9b35e23b5658a707e872f5733400ff664cec1ee1e3d85e7b85fe6"
RESULT = "suyoung_u6_nodal_result.tar.gz"
AREA = 49 * math.pi * .05**2
WIDTH = math.sqrt(AREA / .78)
TARGET = .12
PROTOCOL = "development-mode-1-nodal-gradient"
SOURCES = {"dem_suyoung_sf2d_dev.py", "suyoung_u6_first_dev.py",
           "test_suyoung_u6_first_dev.py", "test_suyoung_contact_direction.py"}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def require(ok, name):
    if not ok:
        raise ValueError(name)


def manifest(raw):
    rows = [line.split("  ", 1) for line in raw.decode("ascii").splitlines()]
    require(len(rows) == len({name for _, name in rows}), "duplicate manifest member")
    return {name: sha for sha, name in rows}


def read_arm(tar, n):
    result = json.load(tar.extractfile(f"data/F{n}/result.json"))
    raw = tar.extractfile(f"data/F{n}/trace.csv").read()
    rows = list(csv.DictReader(io.StringIO(raw.decode("ascii"))))
    require(result["cells"] == n and result["protocol"] == PROTOCOL
            and result["disks"] == 49 and result["target_E"] == TARGET
            and result["friction"] == .5 and result["qualified"] is False
            and result["contact"] == "shared_node_approach", "arm identity")
    dof = result["steps_attempted"]
    require(len(rows) == dof + 1 and rows[0]["step"] == "0", "row count")
    p_prev, h_prev, bracket, phi = None, None, None, None
    peak = float("-inf")
    for step, row in enumerate(rows):
        p, h, t = (float(row[key]) for key in ("bottom_pressure_E", "height", "time_code"))
        require(int(row["step"]) == step and math.isclose(t, step*result["dt"], abs_tol=1e-13)
                and math.isfinite(p) and math.isclose(h, WIDTH - t*result["wall_speed"], abs_tol=1e-13)
                and math.isclose(float(row["phi_m"]), AREA/(WIDTH*h), rel_tol=1e-12),
                "time/geometry/solid-area consistency")
        if p_prev is not None and p_prev < TARGET <= p and bracket is None:
            h_target = h_prev + (TARGET-p_prev)/(p-p_prev) * (h-h_prev)
            bracket = [step-1, step]
            phi = AREA/(WIDTH*h_target)
        peak = max(peak,p)
        p_prev,h_prev = p,h
    if bracket is None:
        require(result["status"] == "TIME_LIMIT" and result["phi_m"] is None
                and result["elapsed_s"] >= 570, "unfinished arm disposition")
    else:
        require(result["status"] == "TARGET_BRACKETED" and dof == bracket[1]
                and math.isclose(phi, result["phi_m"], rel_tol=1e-12), "interpolated endpoint")
    return dict(status=result["status"], steps=dof, trace_rows=len(rows), points=result["points"],
                elapsed_s=result["elapsed_s"], highest_bottom_pressure_over_E=peak,
                last_height_ratio=h_prev/WIDTH, bracket_steps=bracket, recomputed_phi=phi,
                reported_phi=result["phi_m"], trace_sha256=digest(raw))


def audit(package, source, repo):
    with zipfile.ZipFile(package) as z:
        directories = [s.rsplit("/", 1)[0] for s in z.namelist() if s.endswith("/"+RESULT)]
        require(len(directories)==1, "single nodal return")
        prefix = directories[0] + "/"
        names = [name for name in z.namelist() if name.startswith(prefix) and not name.endswith("/")]
        require(sorted(names)==sorted(prefix+i for i in (RESULT, "screen.txt", "SHA256SUMS")), "outer members")
        tar_bytes, screen_bytes = z.read(prefix+RESULT), z.read(prefix+"screen.txt")
        expected = manifest(z.read(prefix+"SHA256SUMS"))
        require(expected=={RESULT:digest(tar_bytes),"screen.txt":digest(screen_bytes)}, "outer digests")
    require(digest(source.read_bytes())==SOURCE_SHA, "pinned source tar")
    with tarfile.open(fileobj=io.BytesIO(tar_bytes),mode="r:gz") as tar, tarfile.open(source) as src:
        stored_files = [m.name for m in tar.getmembers() if m.isfile()]
        whitelist = {"data/SOURCE_SHA256SUMS","data/origin.txt","data/comparison.json","data/screen.txt"}
        for n in (12,16):
            whitelist.update([f"data/F{n}.log",f"data/F{n}/trace.csv",f"data/F{n}/result.json"])
        require(sorted(stored_files)==sorted(whitelist), "result member set")
        source_list = tar.extractfile("data/SOURCE_SHA256SUMS").read()
        require(source_list==src.extractfile("SHA256SUMS").read(), "source lists")
        origin = tar.extractfile("data/origin.txt").read().decode("ascii").splitlines()
        require({"source_pin="+PIN,"source_tar_sha256="+SOURCE_SHA,"release_bound=YES",
                 "auto_retry=0","base=7253d5e6095dc765de81904157a8556f3badb5e6"} <= set(origin),
                "source/execution identity")
        hashes = manifest(source_list)
        require(hashes.keys()==SOURCES|{"SOURCE_PIN.txt"}, "source file set")
        for name, sha in hashes.items():
            raw = src.extractfile(name).read()
            known = ((PIN+"\n").encode() if name=="SOURCE_PIN.txt" else
                     subprocess.check_output(["git","-c","safe.directory="+repo.as_posix(),
                                              "-C",str(repo),"show",PIN+":scripts/"+name]))
            require(raw==known and digest(raw)==sha, "source bytes: "+name)
        require(screen_bytes==tar.extractfile("data/screen.txt").read()+b"ARCHIVE_RC=0\n"
                and b"COMMAND_RC=4\n" in screen_bytes, "screen and return codes")
        arms = {f"F{n}":read_arm(tar,n) for n in (12,16)}
        comparison = json.load(tar.extractfile("data/comparison.json"))
        require(comparison["assessment"]=="INCOMPLETE" and comparison["setting"]==1
                and comparison["selected_setting"] is None and comparison["u6_qualified"] is False,
                "pair disposition")
    return dict(source_pin=PIN, source_tar_sha256=SOURCE_SHA,
                source_files_verified=len(hashes), result_sha256=expected[RESULT],
                screen_sha256=expected["screen.txt"], arms=arms, comparison=comparison)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package",type=Path)
    parser.add_argument("source",type=Path)
    parser.add_argument("repo",type=Path)
    args=parser.parse_args()
    print(json.dumps(audit(args.package,args.source,args.repo.resolve()),indent=2))
