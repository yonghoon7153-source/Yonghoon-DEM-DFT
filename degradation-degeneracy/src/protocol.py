"""protocol.py — 원본 experiment / experiment2 → charge_first / discharge_first.

★ 모드↔프로토콜 매핑은 원본 코드 기준으로 보존한다 (02_CODE_AUDIT.md 3절-4).
원본 run_sweep 호출 (reference/degrade_mode_sim_original.py):
    reference  : experiment   (discharge_first)  L129
    lli        : experiment   (discharge_first)  L134
    lam_pe_de  : experiment   (discharge_first)  L174  ← docs 표와 달리 원본은 discharge_first
    lam_ne_de  : experiment2  (charge_first)     L184
    lam_pe_li  : experiment2  (charge_first)     L197
    lam_ne_li  : experiment   (discharge_first)  L209
"""

from __future__ import annotations

MODES = ["reference", "lli", "lam_ne_li", "lam_ne_de", "lam_pe_li", "lam_pe_de"]


def protocol_steps(cfg: dict, name: str) -> list[str]:
    """'charge_first' | 'discharge_first' → experiment 스텝 리스트."""
    steps = cfg["protocol"].get(name)
    if steps is None:
        raise KeyError(f"protocol.{name} 이 config에 없음")
    return list(steps)


def protocol_name_for_mode(cfg: dict, mode: str) -> str:
    """모드 이름 → 프로토콜 이름. 원본 매핑을 config(mode_protocol)에서 읽는다."""
    mapping = cfg["mode_protocol"]
    if mode not in mapping:
        raise KeyError(f"mode_protocol에 정의되지 않은 모드: {mode}")
    return mapping[mode]


def build_experiment(cfg: dict, protocol_name: str):
    """pybamm.Experiment 생성."""
    import pybamm

    return pybamm.Experiment(protocol_steps(cfg, protocol_name))
