"""baseline.py — 완충 baseline 파라미터 + 완방(discharged) 상태 자동 산출.

★ 02_CODE_AUDIT.md C1 해결:
원본의 완방상태 하드코딩(36.7 / 3446.3 / 58439.9)은 사용하지 않는다.
매 실행 시 0.05C 방전 시뮬레이션으로 산출하고, baseline 해시를 키로 캐시한다.
산출값과 원본 하드코딩 값의 차이를 로그에 경고로 출력한다.
"""

from __future__ import annotations

import json
import math
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

from src.config import baseline_hash

log = logging.getLogger(__name__)

# 원본 코드의 하드코딩 값 — 비교 경고 출력 전용. 절대 계산에 사용 금지.
_ORIGINAL_HARDCODED = {"ne_primary": 36.7, "ne_secondary": 3446.3, "pe": 58439.9}

# pybamm 파라미터 이름 매핑 (원본 initialization() 과 1:1)
PARAM_NAMES = {
    "ne_primary_init_conc": "Primary: Initial concentration in negative electrode [mol.m-3]",
    "ne_primary_max_conc": "Primary: Maximum concentration in negative electrode [mol.m-3]",
    "ne_secondary_init_conc": "Secondary: Initial concentration in negative electrode [mol.m-3]",
    "ne_secondary_max_conc": "Secondary: Maximum concentration in negative electrode [mol.m-3]",
    "pe_init_conc": "Initial concentration in positive electrode [mol.m-3]",
    "ne_porosity": "Negative electrode porosity",
    "ne_primary_vf": "Primary: Negative electrode active material volume fraction",
    "ne_secondary_vf": "Secondary: Negative electrode active material volume fraction",
    "pe_porosity": "Positive electrode porosity",
    "pe_vf": "Positive electrode active material volume fraction",
}

# config baseline 키 중 pybamm 파라미터로 직접 넘기지 않는 것
_NON_PARAM_KEYS = {"pe_max_conc"}


@dataclass(frozen=True)
class DischargedState:
    """완방 상태의 상평균 농도 [mol.m-3]."""

    ne_primary: float
    ne_secondary: float
    pe: float


def get_baseline_params(cfg: dict) -> dict:
    """완충 baseline을 pybamm 파라미터 dict로 변환 (전압 cutoff 포함)."""
    b = cfg["baseline"]
    out = {
        "Upper voltage cut-off [V]": float(cfg["cell"]["upper_voltage_cutoff"]),
        "Lower voltage cut-off [V]": float(cfg["cell"]["lower_voltage_cutoff"]),
    }
    for key, pybamm_name in PARAM_NAMES.items():
        out[pybamm_name] = float(b[key])
    return out


def _cache_path(cfg: dict, cache_dir: str | Path | None) -> Path:
    root = Path(cfg.get("_config_path", ".")).resolve().parent.parent
    d = Path(cache_dir) if cache_dir else root / cfg["discharged_state"].get(
        "cache_dir", ".cache/discharged_state"
    )
    return Path(d) / f"{baseline_hash(cfg)}.json"


def compute_discharged_state(cfg: dict, solver=None) -> DischargedState:
    """0.05C 방전 시뮬레이션으로 완방상태 농도를 산출 (캐시 미사용 강제 계산)."""
    import pybamm

    from src.model import build_model
    from src.runner import build_param, make_solver

    model = build_model(cfg)
    param = build_param(cfg, overrides=None)
    protocol = list(cfg["discharged_state"]["protocol"])
    experiment = pybamm.Experiment(protocol)
    solver = solver or make_solver(cfg)

    sim = pybamm.Simulation(
        model, parameter_values=param, experiment=experiment, solver=solver
    )
    sol = sim.solve()

    state = DischargedState(
        ne_primary=float(
            sol["Average negative primary particle concentration [mol.m-3]"].entries[-1]
        ),
        ne_secondary=float(
            sol["Average negative secondary particle concentration [mol.m-3]"].entries[-1]
        ),
        pe=float(sol["Average positive particle concentration [mol.m-3]"].entries[-1]),
    )

    b = cfg["baseline"]
    log.info(
        "완방상태 산출: Gr=%.1f mol/m3 (x=%.4f), Si=%.1f (x=%.4f), PE=%.1f (y=%.4f)",
        state.ne_primary, state.ne_primary / b["ne_primary_max_conc"],
        state.ne_secondary, state.ne_secondary / b["ne_secondary_max_conc"],
        state.pe, state.pe / b["pe_max_conc"],
    )
    for key, new in asdict(state).items():
        old = _ORIGINAL_HARDCODED[key]
        rel = abs(new - old) / max(abs(old), 1e-12)
        log.warning(
            "  vs 원본 하드코딩 %s: %.1f -> %.1f (차이 %.1f%%) — 하드코딩은 사용하지 않음",
            key, old, new, rel * 100,
        )
    return state


def get_discharged_state(
    cfg: dict, cache_dir: str | Path | None = None, force: bool = False
) -> DischargedState:
    """완방상태 조회. baseline 해시 키 캐시 → 미스 시 시뮬레이션 산출.

    원본 하드코딩(36.7/3446.3/58439.9)은 절대 반환하지 않는다.
    """
    use_cache = bool(cfg["discharged_state"].get("cache", True))
    path = _cache_path(cfg, cache_dir)

    if use_cache and not force and path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        # ★ F82/9차 발견 1 — 캐시가 **이 baseline 의 것인지** 읽기 전에 확인한다.
        #   예전에는 파일 존재만 보고 그대로 신뢰해서, 다른 baseline 의 상태나
        #   손상된 값이 그대로 격자 truth 의 기준이 됐다.
        want = baseline_hash(cfg)
        got = data.get("baseline_hash")
        if got is not None and got != want:
            raise RuntimeError(
                f"완방상태 캐시가 다른 baseline 의 것입니다: {path}\n"
                f"  캐시 {got} ≠ 현재 {want}. --force 로 다시 계산하세요 (F82).")
        vals = {k: data.get(k) for k in ("ne_primary", "ne_secondary", "pe")}
        bad = [k for k, v in vals.items()
               if not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0]
        if bad:
            raise RuntimeError(
                f"완방상태 캐시의 {bad} 값이 유효하지 않습니다: {path} (F82)")
        log.info("완방상태 캐시 적중: %s", path)
        return DischargedState(**vals)

    state = compute_discharged_state(cfg)

    if use_cache:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {**asdict(state), "baseline_hash": baseline_hash(cfg)}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        log.info("완방상태 캐시 저장: %s", path)
    return state


def main() -> None:
    """CLI: python -m src.baseline --config configs/base.yaml [--force]"""
    import argparse

    from src.config import load_config, validate_config

    ap = argparse.ArgumentParser(description="완방상태 산출 및 캐시")
    ap.add_argument("--config", default="configs/base.yaml")
    ap.add_argument("--force", action="store_true", help="캐시 무시하고 재계산")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.config)
    validate_config(cfg)
    state = get_discharged_state(cfg, force=args.force)
    print(json.dumps(asdict(state), indent=2))


if __name__ == "__main__":
    main()
