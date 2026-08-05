"""baseline / 완방상태 테스트.

빠른 테스트: 캐시 동작, 하드코딩 미사용 보장.
slow 테스트: 완방상태 재현성 (2회 계산 동일 — C1 검증).
"""

from __future__ import annotations

import pytest

from src.baseline import (PARAM_NAMES, DischargedState, compute_discharged_state,
                          get_baseline_params, get_discharged_state)


def test_baseline_params_match_original_initialization(cfg):
    """get_baseline_params가 원본 initialization()의 10개 값 + cutoff와 일치."""
    p = get_baseline_params(cfg)
    assert p["Upper voltage cut-off [V]"] == 4.2
    assert p["Lower voltage cut-off [V]"] == 2.5
    expected = {
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
    }
    for k, v in expected.items():
        assert p[k] == v, k
    # pe_max_conc는 pybamm 파라미터로 넘기지 않는다 (참고값)
    assert len(p) == len(PARAM_NAMES) + 2


def test_cache_roundtrip(cfg, tmp_path, monkeypatch):
    """캐시에 저장된 값이 그대로 재로드되는지 (시뮬레이션 없이)."""
    import src.baseline as bl

    fake = DischargedState(ne_primary=1.0, ne_secondary=2.0, pe=3.0)
    monkeypatch.setattr(bl, "compute_discharged_state", lambda c, solver=None: fake)

    cfg2 = {**cfg, "discharged_state": {**cfg["discharged_state"],
                                        "cache": True, "cache_dir": str(tmp_path)}}
    s1 = get_discharged_state(cfg2, cache_dir=tmp_path)
    assert s1 == fake

    # 두 번째 호출은 compute 없이 캐시에서 읽어야 함
    monkeypatch.setattr(bl, "compute_discharged_state",
                        lambda c, solver=None: (_ for _ in ()).throw(AssertionError))
    s2 = get_discharged_state(cfg2, cache_dir=tmp_path)
    assert s2 == fake


@pytest.mark.slow
def test_discharged_state_reproducible(cfg):
    """★ C1 검증: 완방상태 2회 계산이 동일해야 한다 (전역 오염 없음)."""
    s1 = compute_discharged_state(cfg)
    s2 = compute_discharged_state(cfg)
    assert s1.ne_primary == pytest.approx(s2.ne_primary, rel=1e-8)
    assert s1.ne_secondary == pytest.approx(s2.ne_secondary, rel=1e-8)
    assert s1.pe == pytest.approx(s2.pe, rel=1e-8)
    # 원본 하드코딩과의 정합성 확인(참고): 크게 어긋나면 baseline이 바뀐 것
    assert s1.pe == pytest.approx(58439.9, rel=0.05)
