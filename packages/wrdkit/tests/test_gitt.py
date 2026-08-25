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
    """D = (4/(pi tau)) (m V_M / (M_B S))^2 (dE_s/dE_t)^2 를 **픽스처 참값**으로.

    처음 버전은 결과 자신의 ΔE_s/ΔE_t 로 기대값을 만들었다 — 순환 검증이라
    ΔE_t 가 2.14배 틀려도 통과했고, 리뷰가 그 구멍으로 들어왔다.  픽스처는
    ΔE_s=dv_per_pulse, ΔE_t=polarisation_v, τ=pulse_s 를 **설계값으로 알고
    있으므로** 기대값은 거기서만 만든다.
    """
    result = diffusion(gitt(n_pulses=4, pulse_s=60.0, dv_per_pulse=0.05,
                            polarisation_v=0.03, ir_v=0.01), **MATERIAL)
    assert result.missing == []
    usable = result.usable
    assert len(usable) == 3          # 첫 펄스는 ΔE_s 가 없다

    geometry = (MATERIAL["mass_g"] * MATERIAL["molar_volume_cm3"]) / (
        MATERIAL["molar_mass_g"] * MATERIAL["area_cm2"])
    expected = (4.0 / (math.pi * 60.0)) * geometry ** 2 * (0.05 / 0.03) ** 2
    for point in usable:
        assert point.delta_et_v == pytest.approx(0.03, rel=1e-6)
        assert point.d_cm2_s == pytest.approx(expected, rel=1e-6)


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
    ΔE_t 는 피팅된 √t 직선의 **전체 펄스 진폭**이다 — V(end)−V(skip) 으로 재면
    건너뛴 1/10 이 이미 과도의 √0.1=31.6% 를 담고 있어 모든 D 가 2.14배로
    부풀고, 그것을 rel=0.35 짜리 느슨한 허용치가 덮고 있었다.
    """
    result = diffusion(gitt(n_pulses=4, ir_v=0.05, polarisation_v=0.03), **MATERIAL)
    assert result.usable, "IR 강하를 빼지 않으면 여기서 전부 버려진다"
    for point in result.usable:
        assert point.sqrt_t_r_squared > 0.99
        # IR(0.05)이 조금이라도 새면 0.03 을 크게 벗어난다.
        assert point.delta_et_v == pytest.approx(0.03, rel=1e-3)


def test_a_cycle_reset_does_not_fold_the_capacity_axis():
    """CHARGE Q/DISCHARGE Q 는 사이클마다 0 으로 리셋된다 (CLAUDE.md §3).

    파일 전체 차분(C−C₀)은 그 리셋을 그대로 담아, 사이클 경계를 지나는 GITT 의
    용량축이 0, .5, 1.0, **0, .5, 1.0** 으로 접힌다 — 참값은 0..2.5 다.  리뷰가
    잡았다: 처음 구현(cumsum(diff))은 항등변환이라 "리셋 대응" 이 존재하지
    않았다.
    """
    curve = pseudo_ocv(gitt(n_pulses=6, capacity_per_pulse_mah=0.5,
                            pulses_per_cycle=3))
    capacities = [point.capacity_mah for point in curve.charge]
    assert capacities == pytest.approx([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], abs=1e-6)


def test_a_discharge_series_survives_a_cycle_reset_too():
    curve = pseudo_ocv(gitt(n_pulses=6, charging=False, v_start=3.4,
                            capacity_per_pulse_mah=0.5, pulses_per_cycle=2))
    capacities = [point.capacity_mah for point in curve.discharge]
    assert capacities == pytest.approx([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], abs=1e-6)


def test_a_direction_change_resets_the_delta_es_baseline():
    """충전 가지와 방전 가지 사이의 OCV 이력 간극은 한 펄스의 ΔE_s 가 아니다.

    리뷰 재현: 간극 0.1 V 가 ΔE_s 에 얹혀 첫 방전 점의 D 가 이웃의 9배였다.
    전환에서 기준선을 지우면 그 점은 '첫 펄스' 로 보고되고, 그 다음부터는
    한 계단(0.05 V)씩만 잰다.
    """
    charge = synthetic.make_gitt(n_pulses=2, trailing_rest=False)
    discharge = synthetic.make_gitt(n_pulses=3, charging=False, v_start=3.4)
    record = read_wrd_bytes(synthetic.build_wrd(charge + discharge))

    result = diffusion(record, **MATERIAL)
    usable = result.usable
    assert usable, "방전 두 번째 점부터는 나와야 한다"
    for point in usable:
        assert abs(point.delta_es_v) == pytest.approx(0.05, rel=1e-3)
    # 방전 시리즈의 용량은 자기 시리즈 기준으로 0 부터 센다 (pOCV 와 같은 규칙).
    first_discharge = result.points[-3]
    assert "첫 펄스" in first_discharge.reason
    assert first_discharge.capacity_mah == pytest.approx(0.0, abs=1e-3)
    assert result.points[-1].capacity_mah == pytest.approx(1.0, abs=1e-3)


def test_a_short_rest_invalidates_the_next_baseline_too():
    """짧은 휴지의 전압은 평형이 아니다 — 이 점에도, 다음 점의 기준선에도.

    리뷰 재현: 건너뛰기만 하면 다음 점의 ΔE_s 가 두 계단(0.1 V)이 되어 D 가
    정확히 4배가 됐다.  이제 그 점은 이유와 함께 남고, 그 다음 점은 기준선이
    없다고 말하며, 회복된 뒤의 점은 다시 정상 D 를 낸다.
    """
    record = gitt(n_pulses=5, rest_s=600.0, short_rest_index=2,
                  short_rest_s=60.0)
    result = diffusion(record, min_rest_s=100.0, **MATERIAL)
    assert len(result.points) == 5

    short = result.points[2]
    assert short.d_cm2_s is None
    assert "평형이 아닙니다" in short.reason

    after = result.points[3]
    assert after.d_cm2_s is None
    assert "첫 펄스이거나 직전 휴지가" in after.reason

    recovered = result.points[4]
    assert recovered.d_cm2_s is not None
    assert abs(recovered.delta_es_v) == pytest.approx(0.05, rel=1e-3)
    normal = result.points[1]
    assert recovered.d_cm2_s == pytest.approx(normal.d_cm2_s, rel=1e-6)


def test_a_rest_current_offset_does_not_merge_the_file():
    """휴지에 1 µA 오프셋이 있으면 p90 문턱이 그 오프셋에서 정해진다.

    그러면 문턱이 오프셋의 1/10 이 되어 모든 샘플이 "펄스" 가 되고, 파일
    전체가 한 덩어리 충전이 된다 (리뷰 #26).  계측기는 CELL STATUS 로 매
    샘플의 상태를 이미 적어 놨다 — 그것을 먼저 쓴다 (§0.3).
    """
    samples = synthetic.make_gitt(n_pulses=4)
    for sample in samples:
        if sample.cell_status == 1:          # rest
            sample.current = 1e-6
    wrd = read_wrd_bytes(synthetic.build_wrd(samples))
    blocks = segment_pulses(wrd)
    assert [block.mode for block in blocks] == ["charge", "rest"] * 4


def test_an_explicit_threshold_still_wins():
    """호출자가 문턱을 넘겨줬으면 기록을 보고 판단한 것이다 — 그쪽을 따른다."""
    samples = synthetic.make_gitt(n_pulses=2)
    wrd = read_wrd_bytes(synthetic.build_wrd(samples))
    # 문턱을 펄스 전류(1 mA)보다 높게 주면 전부 휴지로 읽혀야 한다.
    blocks = segment_pulses(wrd, rest_threshold_a=0.1)
    assert [block.mode for block in blocks] == ["rest"]


# --- 증거 보존과 행 보존 (리뷰 #17·#25) ---------------------------------------

def test_every_pulse_gets_a_row_even_without_a_rest():
    """마지막 휴지가 없는 파일 — 펄스 3개면 행도 3개다.

    행째 사라지면 화면의 "펄스 N개" 와 이유 목록이 함께 거짓이 된다.
    """
    wrd = gitt(n_pulses=3, trailing_rest=False)
    result = diffusion(wrd, **MATERIAL)
    assert len(result.points) == 3
    last = result.points[-1]
    assert last.d_cm2_s is None
    assert "휴지가 뒤따르지 않는" in last.reason
    assert last.rest_s is None


def test_diffusion_points_carry_their_rest_evidence():
    """D 는 휴지가 평형이라는 가정 위에 있다.  휴지 길이와 잔여 드리프트가
    같은 행에 실려야 표·클립보드에서 그 가정을 검증할 수 있다 (ADR 0020)."""
    wrd = gitt(n_pulses=3)
    result = diffusion(wrd, **MATERIAL)
    pocv = pseudo_ocv(wrd)
    for point, reference in zip(result.points, pocv.charge, strict=True):
        assert point.rest_s == pytest.approx(600.0, rel=0.05)
        assert point.drift_mv == pytest.approx(reference.drift_mv)


# --- 원본 전압 곡선 (pOCV 밑에 깔리는 선) --------------------------------------


def test_the_raw_trace_shares_the_curves_x_axis():
    """점과 선이 같은 자리를 말해야 한다.

    x 축은 그 갈래의 **첫 점**에서 0 이고 (`_from_baseline` 과 같은 규칙).
    선이 그 규칙을 안 따르면 곡선 **옆에** 그려지고, 그 어긋남이 두 값의 실제
    차이처럼 보인다.
    """
    curve = pseudo_ocv(gitt(n_pulses=3))
    assert curve.charge, "이 픽스처에는 충전 펄스가 있어야 한다"
    assert curve.charge_raw.capacity_mah, "곡선이 있으면 그 밑의 선도 있어야 한다"
    assert len(curve.charge_raw.capacity_mah) == len(curve.charge_raw.voltage_v)
    # 각 점은 제 구간의 **끝**이므로, 선의 끝 x 는 마지막 점의 x 와 같다.
    assert curve.charge_raw.capacity_mah[-1] == pytest.approx(
        curve.charge[-1].capacity_mah, rel=1e-9)
    # 그리고 선은 곡선보다 촘촘하다 -- 펄스와 완화를 다 담기 때문이다.
    assert len(curve.charge_raw.capacity_mah) > len(curve.charge)


def test_the_raw_trace_moves_the_same_way_as_its_branch():
    """방전 갈래도 왼쪽에서 오른쪽으로 간다 — 점과 같은 방향이다."""
    charge = synthetic.make_gitt(n_pulses=2, trailing_rest=False)
    discharge = synthetic.make_gitt(n_pulses=3, charging=False, v_start=3.4)
    curve = pseudo_ocv(read_wrd_bytes(synthetic.build_wrd(charge + discharge)))
    assert curve.discharge_raw.capacity_mah, "방전 점이 있으면 선도 있어야 한다"
    assert curve.discharge_raw.capacity_mah[-1] >= curve.discharge_raw.capacity_mah[0]


def test_a_skipped_pulse_leaves_no_raw_line():
    """점이 없는 구간에 선만 그리면, 곡선이 '없다' 고 한 자리에 선이 남는다."""
    curve = pseudo_ocv(gitt(n_pulses=3), min_rest_s=10 ** 9)
    assert not curve.charge and not curve.discharge
    assert not curve.charge_raw.capacity_mah
    assert not curve.discharge_raw.capacity_mah
