"""Read-only Gate65 checks. All output/fixtures stay under this review directory."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
WORK = OUT.parent.parent
REPO = WORK / "work/gate65-head/degradation-degeneracy"
PY = WORK / "work/gate65-venv/Scripts/python.exe"
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")

def run(name, argv, *, env=None, timeout=180):
    start = time.monotonic()
    r = subprocess.run(list(map(str, argv)), cwd=REPO, env=env or ENV,
                       capture_output=True, encoding="utf-8", errors="replace", timeout=timeout)
    (OUT / (name + ".stdout.txt")).write_text(r.stdout, encoding="utf-8")
    (OUT / (name + ".stderr.txt")).write_text(r.stderr, encoding="utf-8")
    rec = dict(argv=list(map(str, argv)), cwd=str(REPO), rc=r.returncode,
               seconds=round(time.monotonic()-start, 3),
               stdout_sha256=hashlib.sha256(r.stdout.encode()).hexdigest())
    (OUT / (name + ".json")).write_text(json.dumps(rec, indent=2), encoding="utf-8")
    print(name, r.returncode, r.stdout[-1400:], r.stderr[-1000:], flush=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["basic", "targets", "independent", "mutation"])
    args = p.parse_args()
    if args.mode == "basic":
        run("identity", [PY, "-c", "import sys,site; from src.io import source_digest; print(sys.version); print('user_site',site.ENABLE_USER_SITE); print('source_digest',source_digest())"])
        run("preimages", [PY, "docs/22p_gap/mutation_replay.py", "--check-preimages"])
    if args.mode in ("basic", "targets"):
        # No repository conftest: it bootstraps filesystem-specific Linux seals.
        # Selected nine tests do not use any fixture defined in that conftest.
        run("target_enabled", [PY, "-m", "pytest", "tests/test_gate64_defensive.py", "--noconftest", "-p", "no:cacheprovider", "-q", "-k", "not kernel_lock_probe_control_actually", "--basetemp", OUT/"tmp_enabled", "--json-report", "--json-report-file", OUT/"target_enabled.report.json"])
        run("target_disabled_venv", [WORK/"work/r17-venv/Scripts/python.exe", "-m", "pytest", "tests/test_gate64_defensive.py", "--noconftest", "-p", "no:cacheprovider", "-q", "-k", "not kernel_lock_probe_control_actually", "--basetemp", OUT/"tmp_disabled"])
    elif args.mode == "independent":
        run("independent", [PY, OUT/"repro_imports.py", "--repo", REPO, "--out", OUT/"import_cases"], timeout=240)
    else:
        # Keep the runner's private sandbox for audit; no recursive deletion.
        run("g64_replay", [PY, "docs/22p_gap/mutation_replay.py", "-k", "g64", "--keep-sandbox"], timeout=240)

if __name__ == "__main__":
    main()
