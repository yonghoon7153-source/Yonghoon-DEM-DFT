"""msc_sign_table 누설 단계 회귀.

PyBaMM 26.8 의 `CustomStepImplicit` 은 `hash_args=None` 이라 함수가 달라도 모든 사용자 정의 단계가 서로 같다(`==`)
— 실험이 첫 단계의 모델을 나머지 단계에 재사용해, 누설 휴지 뒤의 '충전' 단계도 휴지로 돌았다(2026-09-23 실측:
P1 의 충전·방전 뒤 드리프트가 전처리 휴지와 같은 값). 이 시험은 그 경로를 고정한다.
"""
import numpy as np
import pytest

pybamm = pytest.importorskip("pybamm")

from scripts.msc_sign_table import cc, cycle_arrays, simulate  # noqa: E402


def test_leak_steps_with_different_current_are_distinct():
    rest, chg = cc(0.0, 60, 100.0), cc(-1.0, 60, 100.0)
    assert rest != chg
    assert hash(rest) != hash(chg)


def test_leak_steps_differing_only_in_duration_keep_their_duration():
    sol = simulate("MSC", [cc(0.0, 60, 100.0), cc(0.0, 180, 100.0)], 0.5)
    spans = [float(np.ptp(cycle_arrays(sol, k)[0])) for k in (0, 1)]
    assert spans == pytest.approx([60.0, 180.0])


def test_leak_steps_with_huge_resistance_match_standard_steps():
    """R_s → ∞ 이면 누설 단계 실험이 표준 단계 실험과 같은 P1 을 내야 한다 (휴지 이완 부호 반대)."""
    from scripts.msc_sign_table import p1

    std, leak = p1("D_down", None), p1("D_down+MSC", 1e12)
    assert std["drift_after_charge_mV"] < -0.5 < 0.5 < std["drift_after_discharge_mV"]
    for k in ("drift_after_charge_mV", "drift_after_discharge_mV"):
        assert leak[k] == pytest.approx(std[k], abs=0.02)


def test_leak_step_applies_its_own_external_current():
    R = 100.0
    sol = simulate("MSC", [cc(0.0, 120, R), cc(-1.0, 120, R)], 0.5)
    _, v, i_cell = cycle_arrays(sol, 1)
    i_ext = i_cell - v / R
    assert np.allclose(i_ext[1:], -1.0, atol=1e-6)
