"""GITT — 준평형 전압 곡선과 확산계수.

pOCV 는 **두 다른 샘플**을 짝짓는 일이라 조용히 틀리기 쉽다: 펄스 끝의 용량과
휴지 끝의 전압이다.  한 샘플에서 둘 다 가져오면 분극된 전압이 나오는데, 곡선
모양이 그럴듯해서 눈으로는 안 걸린다.  그래서 합성 픽스처의 완화 전압을 알려진
직선으로 만들어 두고 그 직선과 맞는지를 본다.
"""

import math

import numpy as np
import pytest

from wrdkit import read_wrd_bytes
from wrdkit.gitt import diffusion, pseudo_ocv, segment_pulses

import synthetic

MATERIAL = {"molar_volume_cm3": 20.0, "molar_mass_g": 96.0,
            "mass_g": 0.02, "area_cm2": 1.33}


def gitt(**overrides):
    return read_wrd_bytes(synthetic.build_wrd(synthetic.make_gitt(**overrides)))


# --- 펄스와 휴지 나누기 -----------------------------------------------------

def test_pulses_and_rests_alternate():
    blocks = segment_pulses(gitt(n_pulses=4))
    assert [block.mode for block in blocks] == ["charge", "rest"] * 4


def test_a_direction_change_without_a_rest_is_still_two_blocks():
    """부호까지 보고 나눈다.  `|I| > 문턱` 만 보면 충전에서 방전으로 바로
    넘어가는 구간이 한 펄스로 붙어, 그 사이의 용량이 통째로 사라진다."""
    charge = synthetic.make_gitt(n_pulses=2, trailing_rest=False)
    discharge = synthetic.make_gitt(n_pulses=2, charging=False,
                                    v_start=3.4, start_ticks=None)
    blocks = segment_pulses(read_wrd_bytes(synthetic.build_wrd(charge + discharge)))
    modes = [block.mode for block in blocks]
    # 휴지를 사이에 두지 않고 충전 바로 뒤에 방전이 오는 자리가 있어야 한다.
    adjacent = [(a, b) for a, b in zip(modes, modes[1:], strict=False)]
    assert ("charge", "discharge") in adjacent, modes


def test_the_rest_threshold_is_relative_to_this_file():
    """5 mA 펄스와 5 A 펄스는 모양만 같다.  절대 문턱은 둘 중 하나를 틀린다."""
    small = segment_pulses(gitt(n_pulses=3, current_a=1e-5))
    large = segment_pulses(gitt(n_pulses=3, current_a=1.0))
    assert [b.mode for b in small] == [b.mode for b in large]


# --- pseudo-OCV -------------------------------------------------------------

def test_the_voltage_is_the_relaxed_one_not_the_polarised_one():
    """이 시험 하나가 이 모듈의 이유다.

    픽스처의 완화 전압은 펄스마다 정확히 `dv_per_pulse` 씩 오르고, 펄스 중에는
    거기서 `polarisation_v + ir_v` 만큼 떨어져 있다.  한 샘플에서 용량과 전압을
    함께 읽으면 그 차이만큼 통째로 어긋난다 — 곡선 모양은 그대로라서 눈으로는
    안 걸린다.
    """
    curve = pseudo_ocv(gitt(n_pulses=5, v_start=3.0, dv_per_pulse=0.05,
                            polarisation_v=0.03, ir_v=0.01))
    assert len(curve.charge) == 5
    for index, point in enumerate(curve.charge):
        assert point.voltage_v == pytest.approx(3.0 + 0.05 * (index + 1), abs=2e-3)


def test_capacity_is_measured_from_the_first_pulse_of_the_series():
    curve = pseudo_ocv(gitt(n_pulses=5, capacity_per_pulse_mah=0.5))
    capacities = [point.capacity_mah for point in curve.charge]
    assert capacities[0] == pytest.approx(0.0, abs=1e-6)
    assert np.allclose(np.diff(capacities), 0.5, atol=1e-3)


def test_a_pulse_with_no_rest_after_it_is_skipped_and_counted():
    """잘린 파일은 펄스로 끝난다.  마지막 휴지를 빼먹은 프로토콜도 그렇다.

    조용히 버리면 곡선에서 그 둘이 구분되지 않는다.
    """
    curve = pseudo_ocv(gitt(n_pulses=4, trailing_rest=False))
    assert len(curve.charge) == 3
    assert curve.skipped_charge == 1
    assert curve.skipped_reasons


def test_a_discharge_series_also_increases_from_zero():
    curve = pseudo_ocv(gitt(n_pulses=4, charging=False, v_start=3.4))
    assert len(curve.discharge) == 4
    capacities = [point.capacity_mah for point in curve.discharge]
    assert capacities[0] == pytest.approx(0.0, abs=1e-6)
    assert all(later > earlier
               for earlier, later in zip(capacities, capacities[1:], strict=False))
    # 방전이므로 완화 전압은 내려간다.
    voltages = [point.voltage_v for point in curve.discharge]
    assert all(later < earlier
               for earlier, later in zip(voltages, voltages[1:], strict=False))


def test_each_point_carries_how_far_from_equilibrium_it_still_was():
    """휴지가 짧으면 그 전압은 OCV 가 아니다.  얼마나 아닌지를 함께 낸다."""
    long_rest = pseudo_ocv(gitt(n_pulses=3, rest_s=3600.0))
    short_rest = pseudo_ocv(gitt(n_pulses=3, rest_s=30.0))
    assert long_rest.charge[0].rest_s > short_rest.charge[0].rest_s
    assert all(point.drift_mv >= 0 for point in long_rest.charge)


def test_a_minimum_rest_drops_points_and_says_why():
    curve = pseudo_ocv(gitt(n_pulses=4, rest_s=60.0), min_rest_s=600.0)
    assert curve.charge == []
    assert curve.skipped_charge == 4
    assert "휴지가" in curve.skipped_reasons[0]


# --- 확산계수 ---------------------------------------------------------------

def test_the_diffusion_coefficient_matches_the_closed_form():
    """D = (4/(pi tau)) (m V_M / (M_B S))^2 (dE_s/dE_t)^2 를 손으로 확인한다."""
    result = diffusion(gitt(n_pulses=4, pulse_s=60.0, dv_per_pulse=0.05,
                            polarisation_v=0.03, ir_v=0.01), **MATERIAL)
    assert result.missing == []
    usable = result.usable
    assert len(usable) == 3          # 첫 펄스는 ΔE_s 가 없다

    point = usable[0]
    geometry = (MATERIAL["mass_g"] * MATERIAL["molar_volume_cm3"]) / (
        MATERIAL["molar_mass_g"] * MATERIAL["area_cm2"])
    expected = ((4.0 / (math.pi * point.pulse_s)) * geometry ** 2
                * (point.delta_es_v / point.delta_et_v) ** 2)
    assert point.d_cm2_s == pytest.approx(expected, rel=1e-9)


def test_the_first_pulse_of_a_series_gets_no_number():
    """ΔE_s 는 두 휴지 사이의 차이라 첫 펄스에는 없다."""
    result = diffusion(gitt(n_pulses=3), **MATERIAL)
    assert result.points[0].d_cm2_s is None
    assert "첫 펄스" in result.points[0].reason


def test_missing_material_constants_are_named_not_assumed():
    """추정한 몰부피로 계산한 D 는 그 추정의 세제곱만큼 틀린다 (§0.4)."""
    result = diffusion(gitt(n_pulses=3), molar_volume_cm3=20.0)
    assert result.usable == []
    assert "몰질량 M_B" in result.missing
    assert "활물질 질량" in result.missing
    assert "계면 면적 S" in result.missing


def test_a_transient_that_is_not_a_line_in_sqrt_t_is_refused():
    """Weppner-Huggins 는 그 직선성이 곧 가정이다.

    가정이 깨진 펄스는 '조금 나쁜 측정' 이 아니라 **다른 식**이다.
    """
    # 펄스 안의 전압이 sqrt(t) 가 아니라 지수로 움직이는 기록을 만든다.
    samples = synthetic.make_gitt(n_pulses=3)
    data = read_wrd_bytes(synthetic.build_wrd(samples))
    bent = data.data["voltage"].copy()
    blocks = segment_pulses(data)
    for block in blocks:
        if block.mode != "charge":
            continue
        span = block.stop - block.start
        for offset in range(span):
            fraction = offset / max(span - 1, 1)
            bent[block.start + offset] = (bent[block.start]
                                          + 0.03 * (1 - math.exp(-8 * fraction)))
    data.data["voltage"] = bent

    result = diffusion(data, **MATERIAL)
    assert result.usable == []
    assert any("√t" in point.reason for point in result.points)


def test_the_ohmic_jump_is_left_out_of_the_transient():
    """IR 강하는 순간이고 확산 과도가 아니다.

    포함하면 시작점이 꺾여 R² 가 떨어지고, 멀쩡한 펄스가 가정 위반으로 버려진다.
    """
    result = diffusion(gitt(n_pulses=4, ir_v=0.05, polarisation_v=0.03), **MATERIAL)
    assert result.usable, "IR 강하를 빼지 않으면 여기서 전부 버려진다"
    for point in result.usable:
        assert point.sqrt_t_r_squared > 0.99
        # ΔE_t 에 IR 이 남아 있으면 0.03 이 아니라 0.08 근처가 된다.
        assert point.delta_et_v == pytest.approx(0.03, rel=0.35)
