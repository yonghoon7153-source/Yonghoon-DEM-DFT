"""Run the Codex model-validation probes (read beforehand) against our tree.

Usage: python3 -I -B mv_run_probes.py RERUN_ROOT OUT_DIR
Each probe runs as `python3 -I -B probes/<name>` with cwd=RERUN_ROOT.
stdout/stderr go to OUT_DIR/<stem>.stdout.txt / .stderr.txt; stdout-only
probes get OUT_DIR/<stem>_result.json (same serialisation as the bundle's
run_review_checks.py); files a probe writes into RERUN_ROOT/evidence are
copied to OUT_DIR afterwards.  Never invokes a DEM engine.
"""
import json
import os
import shutil
import subprocess
import sys
import time

PROBES = [
    "mv_anchor_porosity.py",
    "mv_pressure_arithmetic.py",
    "mv_softening_scaling.py",
    "mv_softening_frozen_reweight.py",
    "mv_stress_probe.py",
    "mv_stress_core_probe.py",
    "mv_stress_portability.py",
]
STDOUT_RESULT = {"mv_pressure_arithmetic.py", "mv_softening_scaling.py",
                 "mv_softening_frozen_reweight.py"}
# Optional 3rd argv: launcher that adds the container user site (see mv_probe_launcher.py)
LAUNCHER = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else None


def main():
    root, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1",
               OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1",
               TEMP=os.path.join(root, "tmp"), TMP=os.path.join(root, "tmp"))
    runs = []
    for name in PROBES:
        stem = name[:-3]
        t0 = time.time()
        cmd = ["/usr/local/bin/python3", "-I", "-B"]
        if LAUNCHER:
            cmd.append(LAUNCHER)
        cmd.append(os.path.join(root, "probes", name))
        p = subprocess.run(cmd,
                           cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, encoding="utf-8", errors="replace")
        dt = time.time() - t0
        with open(os.path.join(out, f"{stem}.stdout.txt"), "w", encoding="utf-8") as fh:
            fh.write(p.stdout)
        with open(os.path.join(out, f"{stem}.stderr.txt"), "w", encoding="utf-8") as fh:
            fh.write(p.stderr)
        if name in STDOUT_RESULT and p.returncode == 0:
            obj = json.loads(p.stdout)
            with open(os.path.join(out, f"{stem}_result.json"), "w", encoding="utf-8") as fh:
                fh.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
        runs.append(dict(probe=name, returncode=p.returncode, seconds=round(dt, 2)))
        print(f"{name}: rc={p.returncode} ({dt:.1f}s)")
    for fn in sorted(os.listdir(os.path.join(root, "evidence"))):
        shutil.copyfile(os.path.join(root, "evidence", fn), os.path.join(out, fn))
    with open(os.path.join(out, "_runs.json"), "w", encoding="utf-8") as fh:
        json.dump(dict(python=sys.version,
                       interpreter="/usr/local/bin/python3 -I -B" + (" mv_probe_launcher.py (user site 추가)" if LAUNCHER else ""),
                       runs=runs), fh,
                  ensure_ascii=False, indent=2)
        fh.write("\n")
    sys.exit(0 if all(r["returncode"] == 0 for r in runs) else 1)


if __name__ == "__main__":
    main()
