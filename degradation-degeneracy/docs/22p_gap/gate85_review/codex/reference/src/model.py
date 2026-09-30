"""model.py — DFN + composite(음극 2상) 모델 빌드.

원본:
    model = pybamm.lithium_ion.DFN({
        "particle phases": ("2", "1"),
        "open-circuit potential": (("single", "current sigmoid"), "single"),
    })

모델 객체는 프로세스당 1회만 빌드해 재사용한다 (discretisation 비용 회피,
02_CODE_AUDIT.md "조건마다 모델 재빌드로 느림" 항목).
"""

from __future__ import annotations

from functools import lru_cache

import pybamm


def _options_key(cfg: dict) -> tuple:
    m = cfg["model"]
    ocp = m["open_circuit_potential"]
    return (
        tuple(m["particle_phases"]),
        tuple(ocp["negative"]),
        str(ocp["positive"]),
    )


@lru_cache(maxsize=4)
def _build_model_cached(phases: tuple, ocp_neg: tuple, ocp_pos: str):
    return pybamm.lithium_ion.DFN(
        {
            "particle phases": phases,
            "open-circuit potential": (ocp_neg, ocp_pos),
        }
    )


def build_model(cfg: dict):
    """config 기반 DFN 모델. 동일 옵션이면 캐시된 객체를 반환한다.

    주의: pybamm.Simulation은 model을 내부에서 복사하므로 캐시 재사용은 안전.
    """
    phases, ocp_neg, ocp_pos = _options_key(cfg)
    return _build_model_cached(phases, ocp_neg, ocp_pos)
