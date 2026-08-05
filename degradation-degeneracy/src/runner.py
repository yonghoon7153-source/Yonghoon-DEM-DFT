"""runner.py — 단일 solve (순수 함수).

★ 02_CODE_AUDIT.md C2 해결:
전역 param을 변형하지 않는다. 매 호출마다 새 ParameterValues를 생성하므로
병렬 워커 간 오염이 없다. 실패는 예외 대신 (None, 사유)로 반환한다.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

log = logging.getLogger(__name__)

_SOLVER_CACHE: dict = {}


def build_param(cfg: dict, overrides: dict | None = None):
    """baseline + overrides가 적용된 *새* ParameterValues 객체.

    전역 상태 없음 — 병렬 안전. (원본의 param.update + initialization() 패턴 대체)
    """
    import pybamm

    from src.baseline import get_baseline_params

    p = pybamm.ParameterValues(cfg["parameter_set"])
    p.update(get_baseline_params(cfg))
    if overrides:
        p.update(dict(overrides))
    return p


def make_solver(cfg: dict, fresh: bool = False):
    """config 기반 solver. idaklu 우선, 실패 시 casadi fallback (로그 명시)."""
    import pybamm

    key = (cfg["solver"].get("type", "idaklu"), float(cfg["solver"].get("rtol", 1e-6)),
           float(cfg["solver"].get("atol", 1e-6)))
    if not fresh and key in _SOLVER_CACHE:
        return _SOLVER_CACHE[key]

    stype, rtol, atol = key
    solver = None
    if stype == "idaklu":
        try:
            solver = pybamm.IDAKLUSolver(rtol=rtol, atol=atol)
        except Exception as e:  # noqa: BLE001
            log.warning("IDAKLU 사용 불가(%s: %s) → CasadiSolver fallback (2~5배 느림)",
                        type(e).__name__, e)
    if solver is None:
        solver = pybamm.CasadiSolver(
            mode=cfg["solver"].get("casadi_mode", "safe"), rtol=rtol, atol=atol
        )
    _SOLVER_CACHE[key] = solver
    return solver


def solver_name(solver) -> str:
    return type(solver).__name__


@dataclass
class RunResult:
    """단일 solve 결과. solution은 곡선 추출 후 즉시 폐기할 것 (메모리)."""

    solution: Any | None
    elapsed_s: float
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.solution is not None


def run_one(cfg: dict, overrides: dict | None, protocol_name: str,
            solver=None) -> RunResult:
    """단일 조건 solve. 실패 시 죽지 않고 RunResult(error=...)를 반환한다.

    ★ 02_CODE_AUDIT.md M5 해결 — 발산 조건은 상위(grid)에서 failed.csv로 기록.
    """
    import pybamm

    from src.model import build_model
    from src.protocol import build_experiment

    t0 = time.perf_counter()
    try:
        model = build_model(cfg)  # 프로세스당 1회 빌드 (lru_cache)
        param = build_param(cfg, overrides)
        experiment = build_experiment(cfg, protocol_name)
        solver = solver or make_solver(cfg)
        sim = pybamm.Simulation(
            model, parameter_values=param, experiment=experiment, solver=solver
        )
        sol = sim.solve()
        if sol is None:
            return RunResult(None, time.perf_counter() - t0, "solve() returned None")
        # 일부 실패는 예외 없이 termination 문자열로만 드러난다
        term = getattr(sol, "termination", "")
        if term and "error" in str(term).lower():
            return RunResult(None, time.perf_counter() - t0, f"termination={term}")
        return RunResult(sol, time.perf_counter() - t0)
    except Exception as e:  # noqa: BLE001
        return RunResult(None, time.perf_counter() - t0, f"{type(e).__name__}: {e}")
