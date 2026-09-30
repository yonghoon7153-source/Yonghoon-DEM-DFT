#!/usr/bin/env python3
"""
환경 검증 스크립트.

Phase 0에서 가장 먼저 실행한다. 결과를 docs/ENV_REPORT.md에 저장하며,
IDAKLU 가용 여부와 composite DFN 빌드 성공 여부가 이후 성능·실행 가능성을 좌우한다.

실패해도 종료 코드 0을 반환한다 (진단이 목적이지 게이트가 아님).
단, composite DFN 빌드 실패는 치명적이므로 명확히 경고한다.

사용:
    python scripts/verify_env.py
    python scripts/verify_env.py --out docs/ENV_REPORT.md
"""

from __future__ import annotations

import argparse
import multiprocessing
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPORT: list[str] = []


def log(msg: str, level: str = "INFO") -> None:
    mark = {"INFO": "  ", "OK": "OK", "WARN": "!!", "FAIL": "XX"}.get(level, "  ")
    line = f"[{mark}] {msg}"
    print(line)
    REPORT.append(line)


def section(title: str) -> None:
    print()
    print(f"=== {title} ===")
    REPORT.append("")
    REPORT.append(f"### {title}")


# ---------------------------------------------------------------- system

def check_system() -> dict:
    section("System")
    info = {
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "nproc": multiprocessing.cpu_count(),
    }
    log(f"platform : {info['platform']}")
    log(f"python   : {info['python']}")
    log(f"nproc    : {info['nproc']}  -> run.sh --nproc 기본값 후보")

    if sys.version_info < (3, 10):
        log("Python 3.10 이상 권장", "WARN")

    # memory
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    gb = int(line.split()[1]) / 1024 / 1024
                    info["mem_gb"] = round(gb, 1)
                    log(f"memory   : {gb:.1f} GB")
                    break
    except FileNotFoundError:
        log("memory   : 확인 불가 (non-Linux)")

    # disk
    total, used, free = shutil.disk_usage(".")
    info["disk_free_gb"] = round(free / 1024**3, 1)
    log(f"disk free: {info['disk_free_gb']} GB  -> fine 격자는 수 GB 필요")
    if free / 1024**3 < 10:
        log("여유 공간 10 GB 미만. grid 실행 전 확보 필요", "WARN")

    return info


# ---------------------------------------------------------------- gpu

def check_gpu() -> dict:
    section("GPU")
    info = {"has_gpu": False, "jax": None}

    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total",
                 "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10,
            )
            if out.returncode == 0 and out.stdout.strip():
                info["has_gpu"] = True
                for line in out.stdout.strip().splitlines():
                    log(f"GPU: {line.strip()}", "OK")
            else:
                log("nvidia-smi는 있으나 GPU 미검출")
        except Exception as e:  # noqa: BLE001
            log(f"nvidia-smi 실행 실패: {e}", "WARN")
    else:
        log("nvidia-smi 없음 -> CPU 전용 경로로 진행")

    try:
        import jax  # noqa: PLC0415
        devs = jax.devices()
        info["jax"] = str(devs)
        log(f"jax devices: {devs}", "OK")
    except ImportError:
        log("jax 미설치 (Phase 7에서만 필요)")
    except Exception as e:  # noqa: BLE001
        log(f"jax import 실패: {e}", "WARN")

    log("주의: PyBaMM DFN 단일 solve는 GPU로 빨라지지 않는다. "
        "docs/03_ARCHITECTURE.md 6절 참조")
    return info


# ---------------------------------------------------------------- pybamm

def check_pybamm() -> dict:
    section("PyBaMM")
    info: dict = {}

    try:
        import pybamm  # noqa: PLC0415
    except ImportError as e:
        log(f"pybamm import 실패: {e}", "FAIL")
        log("pip install 'pybamm[all]' 필요", "FAIL")
        return {"ok": False}

    info["version"] = pybamm.__version__
    log(f"pybamm {pybamm.__version__}", "OK")

    # --- solver ---
    solver = None
    try:
        solver = pybamm.IDAKLUSolver()
        info["solver"] = "idaklu"
        log("IDAKLU: 사용 가능 (권장)", "OK")
    except Exception as e:  # noqa: BLE001
        info["solver"] = "casadi"
        log(f"IDAKLU 사용 불가 -> {type(e).__name__}: {e}", "WARN")
        log("CasadiSolver로 fallback (통상 2~5배 느림)", "WARN")
        log("해결: pip install 'pybamm[all]' 또는 pip install pybamm-idaklu", "WARN")
        solver = pybamm.CasadiSolver(mode="safe")

    # --- composite DFN (이게 실패하면 프로젝트 진행 불가) ---
    try:
        model = pybamm.lithium_ion.DFN({
            "particle phases": ("2", "1"),
            "open-circuit potential": (("single", "current sigmoid"), "single"),
        })
        info["composite_dfn"] = True
        log("composite DFN 빌드 성공 (particle phases 2,1)", "OK")
    except Exception as e:  # noqa: BLE001
        info["composite_dfn"] = False
        log(f"composite DFN 빌드 실패: {type(e).__name__}: {e}", "FAIL")
        log("PyBaMM 버전 또는 옵션 문법 확인 필요. 이 단계 통과 없이는 진행 불가", "FAIL")
        return info

    # --- parameter set ---
    try:
        param = pybamm.ParameterValues("Chen2020_composite")
        info["param_set"] = True
        log("Chen2020_composite 파라미터셋 로드 성공", "OK")
        cap = param["Nominal cell capacity [A.h]"]
        log(f"Nominal cell capacity: {cap} A.h")
    except Exception as e:  # noqa: BLE001
        info["param_set"] = False
        log(f"파라미터셋 로드 실패: {e}", "FAIL")
        return info

    # --- 실제 solve 벤치마크 (grid 소요시간 추정용) ---
    section("Benchmark")
    try:
        param.update({
            "Upper voltage cut-off [V]": 4.2,
            "Lower voltage cut-off [V]": 2.5,
            "Primary: Initial concentration in negative electrode [mol.m-3]": 27700.0,
            "Primary: Maximum concentration in negative electrode [mol.m-3]": 28700.0,
            "Secondary: Initial concentration in negative electrode [mol.m-3]": 276610.0,
            "Secondary: Maximum concentration in negative electrode [mol.m-3]": 278000.0,
            "Initial concentration in positive electrode [mol.m-3]": 17038.0,
            "Negative electrode porosity": 0.25,
            "Primary: Negative electrode active material volume fraction": 0.735,
            "Secondary: Negative electrode active material volume fraction": 0.015,
            "Positive electrode porosity": 0.335,
            "Positive electrode active material volume fraction": 0.665,
        })
        exp = pybamm.Experiment([
            "Charge at 0.05 C until 4.2 V",
            "Rest for 10 minutes",
            "Discharge at 0.05 C until 2.5 V",
        ])
        sim = pybamm.Simulation(model, parameter_values=param,
                                experiment=exp, solver=solver)
        t0 = time.perf_counter()
        sim.solve()
        dt = time.perf_counter() - t0
        info["solve_seconds"] = round(dt, 2)
        log(f"1회 solve 소요: {dt:.2f} s", "OK")

        nproc = multiprocessing.cpu_count()
        for n, label in [(125, "coarse (step 0.05)"), (9261, "fine (step 0.02)")]:
            est = dt * n / nproc / 60
            log(f"  {label:22s} {n:>5d} cond / {nproc} proc  ≈ {est:.1f} min")
    except Exception as e:  # noqa: BLE001
        log(f"벤치마크 solve 실패: {type(e).__name__}: {e}", "WARN")
        log("파라미터 조합 문제일 수 있음. Phase 1에서 재확인", "WARN")

    return info


# ---------------------------------------------------------------- deps

def check_deps() -> dict:
    section("Dependencies")
    info = {}
    required = ["numpy", "scipy", "pandas", "matplotlib", "yaml",
                "openpyxl", "joblib", "tqdm"]
    optional = ["pyarrow", "pytest", "jax", "torch"]

    for name in required:
        try:
            mod = __import__(name)
            ver = getattr(mod, "__version__", "?")
            info[name] = ver
            log(f"{name:14s} {ver}", "OK")
        except ImportError:
            log(f"{name:14s} 미설치 — requirements.txt 확인", "FAIL")

    for name in optional:
        try:
            mod = __import__(name)
            log(f"{name:14s} {getattr(mod, '__version__', '?')} (optional)")
        except ImportError:
            log(f"{name:14s} 미설치 (optional)")

    return info


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="환경 검증")
    ap.add_argument("--out", default="docs/ENV_REPORT.md",
                    help="보고서 저장 경로")
    args = ap.parse_args()

    print("=" * 60)
    print(" degradation-degeneracy — 환경 검증")
    print("=" * 60)

    sysinfo = check_system()
    check_deps()
    gpu = check_gpu()
    pb = check_pybamm()

    # ---- 요약 ----
    section("Summary")
    ok = pb.get("composite_dfn", False) and pb.get("param_set", False)
    if ok:
        log("진행 가능", "OK")
        log(f"권장 실행: ./run.sh --mode grid --nproc {sysinfo['nproc']} "
            f"--solver {pb.get('solver', 'casadi')}")
        if not gpu["has_gpu"]:
            log("GPU 없음 — 문제되지 않음. CPU 병렬이 1차 경로")
    else:
        log("진행 불가 — 위 FAIL 항목 해결 필요", "FAIL")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "# 환경 검증 보고서\n\n"
        f"생성: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "```\n" + "\n".join(REPORT) + "\n```\n",
        encoding="utf-8",
    )
    print(f"\n보고서 저장: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
