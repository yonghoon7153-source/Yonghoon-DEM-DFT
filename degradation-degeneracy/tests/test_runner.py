"""runner 테스트 — C2(전역 오염 없음) 검증.

slow: 동일 overrides 2회 실행 결과가 완전 일치해야 하며,
      사이에 다른 조건을 끼워도 오염되지 않아야 한다.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.curves import extract_curves
from src.modes import Baseline, single_mode_overrides
from src.runner import build_param, run_one


def test_build_param_is_fresh_each_time(cfg):
    """build_param은 매번 새 객체 — 한쪽을 변형해도 다른 쪽 불변 (병렬 안전의 전제)."""
    p1 = build_param(cfg)
    p2 = build_param(cfg)
    assert p1 is not p2
    key = "Negative electrode porosity"
    p1.update({key: 0.5})
    assert p2[key] == 0.25


def test_run_one_failure_is_isolated(cfg):
    """말이 안 되는 override로도 예외가 밖으로 새지 않고 error로 반환."""
    res = run_one(cfg, {"Negative electrode porosity": -1.0}, "charge_first")
    assert not res.ok
    assert res.error


@pytest.mark.slow
def test_no_global_pollution(cfg, baseline):
    """A → B(LLI=0.2) → A 순서 실행 시 A 두 번의 곡선이 완전 일치해야 한다.

    원본 코드에서 initialization() 누락 시 발생하던 오염(C2)의 회귀 테스트.
    """
    from src.baseline import get_discharged_state

    d = get_discharged_state(cfg)
    n_trim = cfg["postprocess"]["n_trim"]
    n_interp = cfg["postprocess"]["n_interp"]

    a1 = run_one(cfg, None, "charge_first")
    assert a1.ok, a1.error
    b = run_one(cfg, single_mode_overrides("lli", 0.2, baseline, d), "discharge_first")
    assert b.ok, b.error
    a2 = run_one(cfg, None, "charge_first")
    assert a2.ok, a2.error

    c1 = extract_curves(a1.solution, n_trim, n_interp)
    c2 = extract_curves(a2.solution, n_trim, n_interp)
    assert c1["q_mah"] == pytest.approx(c2["q_mah"], abs=1e-6)
    np.testing.assert_allclose(c1["v_full"], c2["v_full"], rtol=0, atol=1e-9)
