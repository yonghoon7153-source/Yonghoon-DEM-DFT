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

#: ★ 11차 발견 1 / 12차 발견 2 — 완방상태 값을 바꿀 수 있는 runtime 축.
#: solver backend 는 pybamm 과 별도 배포판이라 반드시 포함해야 하고(12차),
#: platform 도 리뷰 요청대로 결정축에 넣는다 (libm/커널 차이).
_ENV_KEYS = ("python", "platform", "machine", "pybamm", "pybammsolvers",
             "casadi", "scipy", "numpy")


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
    cfg: dict, cache_dir: str | Path | None = None, force: bool = False,
    cache_bytes: bytes | None = None,
) -> DischargedState:
    """완방상태 조회. baseline 해시 키 캐시 → 미스 시 시뮬레이션 산출.

    원본 하드코딩(36.7/3446.3/58439.9)은 절대 반환하지 않는다.
    """
    use_cache = bool(cfg["discharged_state"].get("cache", True))
    path = _cache_path(cfg, cache_dir)

    # ★ 51차 P0-A4 — 호출자가 **승인한 바이트**를 그대로 넘길 수 있다.
    #   경로를 다시 여는 대신 그 바이트를 파싱하면, "승인 축이 해시한 것" 과
    #   "격자 truth 가 읽은 것" 이 같은 바이트임이 구조적으로 보장된다. 리뷰어
    #   반례는 두 캐시 모두 reader 의 identity 검사를 통과했다 — 검사를 더
    #   붙이는 것이 아니라 읽는 대상을 고정하는 것이 답이다.
    if cache_bytes is not None:
        if force or not use_cache:
            raise RuntimeError(
                "완방상태: 캐시 바이트를 주면서 동시에 재계산을 요구할 수 없다 "
                "— 승인이 가리키는 대상이 둘이 된다")
        data = json.loads(cache_bytes.decode("utf-8"))
    elif use_cache and not force and path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = None
    if data is not None:
        # ★ F82/9차 발견 1 — 캐시가 **이 baseline 의 것인지** 읽기 전에 확인한다.
        #   예전에는 파일 존재만 보고 그대로 신뢰해서, 다른 baseline 의 상태나
        #   손상된 값이 그대로 격자 truth 의 기준이 됐다.
        want = baseline_hash(cfg)
        got = data.get("baseline_hash")
        # ★ F82b/10차 발견 2-a — hash 가 **없는** 캐시도 거부한다. `is not None`
        #   조건이면 identity 필드가 아예 없는 옛/수제 캐시가 값 검사만으로
        #   통과했다 (리뷰 실측: ACCEPTED_WITHOUT_BASELINE_HASH=True).
        if got != want:
            raise RuntimeError(
                f"완방상태 캐시의 baseline identity 가 없거나 다릅니다: {path}\n"
                f"  캐시 {got} ≠ 현재 {want}. --force 로 다시 계산하세요 (F82).")
        # ★ F82b/발견 2-b — baseline_hash 에는 solver 가 없다. IDAKLU rtol=1e-6
        #   과 Casadi rtol=1e-3 이 같은 키를 가져, 다른 solver 로 계산한 상태를
        #   현재 solver 의 결과처럼 재사용할 수 있었다. 계산 recipe(solver 설정)를
        #   payload 에 넣고 읽을 때 대조한다.
        if data.get("solver") != cfg.get("solver"):
            raise RuntimeError(
                f"완방상태 캐시가 다른 solver 설정으로 계산됐습니다: {path}\n"
                f"  캐시 {data.get('solver')} ≠ 현재 {cfg.get('solver')}. "
                f"--force 로 다시 계산하세요 (F82b).")
        # ★ 10차 자체 리뷰 — 계산 **코드** identity 도 대조한다. solver 설정이
        #   같아도 모델/파라미터 코드가 바뀌면 다른 물리값이 나온다. 완방상태는
        #   격자 전체의 truth 기준점이라, stale 이면 모든 조건이 조용히 이동한다.
        #   baseline/solver 불일치(위 raise)는 "다른 실험의 캐시"라 조사가 필요
        #   하지만, 코드 변경은 일상이므로 **미스로 취급해 재계산**한다 — stale
        #   값이 쓰이는 일은 없고, resume 중이면 격자 서명 가드(F82)가 잡는다.
        # ★ 11차 발견 1 — runtime identity 도 같은 이유로 대조한다. 같은 코드·
        #   config·solver dict 라도 PyBaMM/SciPy/solver backend 버전이 바뀌면
        #   완방상태 값이 달라질 수 있는데, 그 캐시가 hit 되면 격자 manifest 는
        #   **현재** env 를 기록해 "이 env 에서 만든 truth" 라는 주장이 거짓이
        #   된다. 결정에 쓰는 축만 본다 (platform 문자열 등은 제외).
        # ★ 12차 발견 2 — 요청 solver 가 같아도 **실제로 쓰인** solver 가 다를 수
        #   있다 (IDAKLU 생성 실패 시 Casadi fallback). 실제 클래스와 backend
        #   패키지 버전도 대조한다.
        from src.io import env_fingerprint as _ef
        from src.io import source_digest as _sd
        from src.runner import effective_solver as _eff
        _env_now = {k: _ef().get(k) for k in _ENV_KEYS}
        _env_old = {k: (data.get("env") or {}).get(k) for k in _ENV_KEYS}
        _eff_now = _eff(cfg)
        # ★ 52차 P0-5 — **authoritative mode 에서는 미스로 접지 않는다.**
        #   호출자가 승인한 바이트를 줬다면 그 바이트를 쓰거나 거부해야 한다.
        #   "stale 이면 다시 계산한다" 는 캐시 정책으로는 옳지만, 승인이 그
        #   바이트를 가리킬 때는 승인 밖의 값을 만드는 **셋째 길**이 된다
        #   (리뷰어 실측: 승인 (1.0,2.0,3.0) · 소비 (101.0,202.0,303.0)).
        _mismatch = None
        if _env_old != _env_now:
            _mismatch = ("runtime", _env_old, _env_now)
        elif data.get("effective_solver") != _eff_now:
            _mismatch = ("solver backend", data.get("effective_solver"), _eff_now)
        elif data.get("source_digest") != _sd():
            _mismatch = ("코드", data.get("source_digest"), _sd())
        if _mismatch is not None and cache_bytes is not None:
            raise RuntimeError(
                f"승인한 완방상태 캐시가 이 실행과 다른 {_mismatch[0]} 로 "
                f"계산됐습니다 ({_mismatch[1]} ≠ {_mismatch[2]}).\n"
                f"  승인이 이 바이트를 가리키므로 재계산으로 넘어갈 수 없습니다 "
                f"(52차 P0-5). 준비 단계를 다시 돌려 캐시를 만들고 계획의 "
                f"`discharged_cache_sha256` 을 갱신하세요.")
        if _mismatch is not None:
            log.warning("완방상태 캐시가 다른 %s 로 계산됨 (%s ≠ %s) — 미스로 "
                        "취급해 재계산: %s", *_mismatch, path)
        else:
            vals = {k: data.get(k) for k in ("ne_primary", "ne_secondary", "pe")}
            bad = [k for k, v in vals.items()
                   if not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0]
            if bad:
                raise RuntimeError(
                    f"완방상태 캐시의 {bad} 값이 유효하지 않습니다: {path} (F82)")
            log.info("완방상태 캐시 적중: %s", path)
            return DischargedState(**vals)

    # ★ 52차 P0-5 — authoritative mode 는 여기까지 오면 안 된다. 위 분기가
    #   모두 raise 하므로 도달 불가지만, 도달했다면 그것이 곧 결함이다.
    if cache_bytes is not None:
        raise RuntimeError(
            "승인한 완방상태 바이트를 받고도 재계산 경로에 도달했습니다 — "
            "승인과 소비가 갈렸습니다 (52차 P0-5)")
    state = compute_discharged_state(cfg)

    if use_cache:
        path.parent.mkdir(parents=True, exist_ok=True)
        from src.io import env_fingerprint, source_digest
        from src.runner import effective_solver
        payload = {**asdict(state), "baseline_hash": baseline_hash(cfg),
                   "solver": cfg.get("solver"),          # F82b: 요청 recipe
                   # ★ 12차 발견 2 — 실제로 쓰인 solver 클래스·backend 버전
                   "effective_solver": effective_solver(cfg),
                   "source_digest": source_digest(),
                   # ★ 11차 발견 1 — 생성 runtime. hit 판정에 쓰인다.
                   "env": env_fingerprint()}
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
