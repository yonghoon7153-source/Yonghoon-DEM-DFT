"""Assemble evidence_rerun/ for the repo import (our outputs only).

Usage: python3 -I -B mv_assemble_rerun.py SCRATCH_RERUN TOOLS_DIR BUNDLE_EVIDENCE DEST
"""
import json
import os
import platform
import shutil
import sys
import importlib.metadata as md


def main():
    rr, tools, bev, dest = sys.argv[1:5]
    if os.path.exists(dest) and os.listdir(dest):
        sys.exit(f"REFUSE non-empty {dest}")
    os.makedirs(dest, exist_ok=True)
    # 1) main rerun outputs
    out = os.path.join(rr, "out")
    for fn in sorted(os.listdir(out)):
        shutil.copyfile(os.path.join(out, fn), os.path.join(dest, fn))
    # 2) identity + comparison
    for fn in ("source_identity_check.json", "compare_vs_codex.json"):
        shutil.copyfile(os.path.join(rr, fn), os.path.join(dest, fn))
    # 3) first attempt (bare -I) — failure record only
    a1 = os.path.join(dest, "attempt1_isolated_no_usersite")
    os.makedirs(a1)
    src_a1 = os.path.join(rr, "out_attempt1_isolated")
    for fn in ("_runs.json", "mv_stress_core_probe.stderr.txt", "mv_stress_portability.stderr.txt"):
        shutil.copyfile(os.path.join(src_a1, fn), os.path.join(a1, fn))
    # 4) diagnostic: Python 3.12 sum() emulation
    diag_out = os.path.join(rr, "out_sum312")
    rows = []
    for fn in ("mv_anchor_porosity_result.json", "mv_pressure_arithmetic_result.json",
               "mv_softening_scaling_result.json", "mv_softening_frozen_reweight_result.json",
               "mv_stress_arithmetic.json", "mv_stress_core_controls.json"):
        a = json.load(open(os.path.join(bev, fn), encoding="utf-8"))
        b = json.load(open(os.path.join(diag_out, fn), encoding="utf-8"))
        rows.append(dict(file=fn, parsed_equal_to_codex=a == b))
    runs = json.load(open(os.path.join(diag_out, "_runs.json"), encoding="utf-8"))
    diag = dict(
        purpose="Python 3.11 재실행의 끝자리 차이가 Python 3.12 의 내장 sum() 보정 합산 (Neumaier) 때문인지 확인하는 진단 — 판정 증거 아님",
        launcher="tools/mv_probe_launcher_sum312.py (builtins.sum 을 CPython 3.12 sum() 흉내로 바꿈)",
        runs=runs["runs"],
        result_equality=rows,
        note=("mv_stress_portability 는 이 진단에서 rc 1 이 정상이다 — 그 탐침이 띄우는 자식 프로세스는 바꾼 sum 을 "
              "쓰지 않으므로 부모 (바꾼 sum) 결과와 다르다.  본 재실행 (바꾸지 않은 sum) 에서는 rc 0."),
    )
    with open(os.path.join(dest, "diag_py312_sum_emulation.json"), "w", encoding="utf-8") as fh:
        json.dump(diag, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    # 5) environment (same sys.path as the probe launcher: user site added)
    import site
    us = site.getusersitepackages()
    if us not in sys.path:
        try:
            pos = sys.path.index("/usr/local/lib/python3.11/dist-packages")
        except ValueError:
            pos = len(sys.path)
        sys.path.insert(pos, us)
    env = {"python": sys.version, "platform": platform.platform(), "interpreter_flags": "-I -B (+ user site 경로만 더한 실행기)"}
    for n in ("numpy", "pandas", "networkx", "scipy", "python-dateutil"):
        try:
            env[n] = md.version(n)
        except md.PackageNotFoundError:
            env[n] = "missing"
    with open(os.path.join(dest, "environment.json"), "w", encoding="utf-8") as fh:
        json.dump(env, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    # 6) our tools
    td = os.path.join(dest, "tools")
    os.makedirs(td)
    for fn in ("safe_extract_mv.py", "mv_source_identity.py", "mv_build_rerun_root.py", "mv_run_probes.py",
               "mv_probe_launcher.py", "mv_probe_launcher_sum312.py", "mv_compare.py", "mv_assemble_rerun.py"):
        shutil.copyfile(os.path.join(tools, fn), os.path.join(td, fn))
    print("assembled", sum(len(f) for _r, _d, f in os.walk(dest)), "files")
    print(json.dumps(rows, ensure_ascii=False))


if __name__ == "__main__":
    main()
