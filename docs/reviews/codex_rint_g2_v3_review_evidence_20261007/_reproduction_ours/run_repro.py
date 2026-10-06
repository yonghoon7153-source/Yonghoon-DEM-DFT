"""Set up and run the two Codex probes (byte-for-byte copies) on our tree.

Usage: python3 -I -B run_repro.py <probe_dir> <repo_root> <runs_dir> <empty_cwd>
  <probe_dir>  folder holding probe_v3.py · probe_prior.py · source_manifest.json
               (the Codex zip extract, or this evidence folder)
  <runs_dir>   must not contain checkout/ headcopy/ negctl/ yet (outside the repo)

Runs (each in its own new empty folder under <runs_dir>):
  checkout : source -> symlink to our worktree root (clean checkout at HEAD)
  headcopy : source/ = copies of the 9 manifest files read from our worktree
  negctl   : like headcopy, but the v3 draft copy gets one extra byte -> the probe's
             own Git-blob check must stop it (AssertionError, rc != 0, no evidence)

The probes are executed with `python3 -I -B <run>/<probe>.py` from <empty_cwd>.
Nothing from the package other than probe_v3.py / probe_prior.py is executed.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROBES = ("probe_v3.py", "probe_prior.py")


def blob_id(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def listing(d):
    out = {}
    for p in sorted(Path(d).rglob("*")):
        if p.is_symlink():
            out[str(p.relative_to(d))] = "symlink->" + os.readlink(p)
            continue
        if p.is_file():
            b = p.read_bytes()
            out[str(p.relative_to(d))] = hashlib.sha256(b).hexdigest()
    return out


def setup(run, extract, worktree, mode, manifest):
    run.mkdir(parents=True, exist_ok=False)
    for name in PROBES + ("source_manifest.json",):
        shutil.copyfile(extract / name, run / name)
    if mode == "checkout":
        os.symlink(worktree, run / "source")
        return
    for row in manifest["files"]:
        dst = run / "source" / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        b = (worktree / row["path"]).read_bytes()
        if mode == "negctl" and row["path"].endswith("contact_resistance_pipeline_draft_v3_20261006.md"):
            b = b + b"\n"
        dst.write_bytes(b)


def main():
    extract, worktree, runs, cwd = (Path(a).resolve() for a in sys.argv[1:5])
    manifest = json.loads((extract / "source_manifest.json").read_text(encoding="utf8"))
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/root"),
           "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
           "LC_ALL": "C.UTF-8"}
    summary = {"worktree_blobs": {}, "runs": {}}
    for row in manifest["files"]:
        b = (worktree / row["path"]).read_bytes()
        summary["worktree_blobs"][row["path"]] = {"worktree_blob": blob_id(b),
                                                   "pin_blob": row["git_blob"],
                                                   "same": blob_id(b) == row["git_blob"]}
    for mode in ("checkout", "headcopy", "negctl"):
        run = runs / mode
        setup(run, extract, worktree, mode, manifest)
        before = listing(run)
        res = {}
        for probe in PROBES:
            p = subprocess.run([sys.executable, "-I", "-B", str(run / probe)], cwd=str(cwd), env=env,
                               capture_output=True, text=True)
            (run / (probe + ".stdout.txt")).write_text(p.stdout, encoding="utf8")
            (run / (probe + ".stderr.txt")).write_text(p.stderr, encoding="utf8")
            res[probe] = {"rc": p.returncode, "stderr_tail": p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else []}
        after = listing(run)
        new = sorted(set(after) - set(before))
        changed = sorted(k for k in before if k in after and before[k] != after[k])
        summary["runs"][mode] = {"probes": res, "new_files": new, "changed_files": changed}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    (runs / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf8")


if __name__ == "__main__":
    main()
