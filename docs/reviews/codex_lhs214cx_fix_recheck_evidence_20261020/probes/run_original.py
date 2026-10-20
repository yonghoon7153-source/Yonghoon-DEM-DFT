"""Run unmodified baseline/current tests in the same isolated Windows runtime."""
from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
label = sys.argv[1]
kind = sys.argv[2] if len(sys.argv) > 2 else "boundary"
source = ROOT / "source" if label == "current" else WORK / "lhs214s_recheck_20261019/source"
tmp = ROOT / "tmp" / f"original_{label}_{kind}"
tmp.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    env[key] = "1"
env["TEMP"] = env["TMP"] = str(tmp)
env["PYTHONDONTWRITEBYTECODE"] = "1"
for key in ("UPLOAD", "RESULTS", "ARCHIVE", "MPM_LAB", "EIS"):
    env[f"WEBAPP_{key}_FOLDER"] = str(tmp / key.lower())
env["MPLCONFIGDIR"] = str(tmp / "matplotlib")
env["PYTHONPATH"] = os.pathsep.join(map(str, (
    source / "scripts", source / "webapp",
    WORK / "lhs_coverage_review_20260930/deps",
    WORK / "gen2_network_reverify3_20261007/deps",
)))
targets = {
    "boundary": ("scripts/test_l214r_r01_restored_full.py", []),
    "receipt_selftest": ("scripts/supp20_input_receipt.py", ["--selftest"]),
}
rel, args = targets[kind]
target = source / rel
before = hashlib.sha256(target.read_bytes()).hexdigest()
cmd = [sys.executable, "-X", "utf8", "-B", str(target), *args]
version_cmd = [sys.executable, "-X", "utf8", "-B", "-c",
               "import json,numpy,scipy; print(json.dumps({'numpy':numpy.__version__,'scipy':scipy.__version__}))"]
versions = subprocess.run(version_cmd, env=env, capture_output=True, text=True, encoding="utf8")
start = time.perf_counter()
p = subprocess.run(cmd, cwd=source, env=env, capture_output=True, text=True, encoding="utf8")
elapsed = time.perf_counter() - start
after = hashlib.sha256(target.read_bytes()).hexdigest()
out = ROOT / "evidence" / f"original_{label}_{kind}"
out.with_suffix(".log").write_text(p.stdout + "\n--- STDERR ---\n" + p.stderr, encoding="utf8")
meta = dict(label=label, kind=kind, source=str(source), sha256_before=before, sha256_after=after,
            unchanged=before == after, command=cmd, cwd=str(source), python=sys.version,
            platform=platform.platform(), dependencies=versions.stdout.strip(), returncode=p.returncode,
            seconds=elapsed, stdout_tail=p.stdout.splitlines()[-4:],
            environment={k: env[k] for k in env if k.startswith("WEBAPP_") or k in
                         ("TMP", "TEMP", "PYTHONPATH", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                          "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")})
out.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps(meta, ensure_ascii=False))
sys.exit(p.returncode)
