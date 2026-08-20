"""Knee detection on curves with a known shape."""

import numpy as np
import pytest

from wrdkit.knee import detect_knee, smooth_series


def _piecewise(n=60, knee=30, slope_before=-0.05, slope_after=-1.0, start=5.0):
    cycles = np.arange(1, n + 1)
    values = np.where(
        cycles <= knee,
        start + slope_before * (cycles - 1) / 100.0 * start,
        start + slope_before * (knee - 1) / 100.0 * start
        + slope_after * (cycles - knee) / 100.0 * start,
    )
    return cycles.tolist(), values.tolist()


def test_segmented_finds_a_planted_knee():
    cycles, values = _piecewise(knee=30)
    analysis = detect_knee(cycles, values, reference_cycle=1)
    segmented = analysis.by_method("segmented")
    assert segmented.detected
    assert segmented.cycle == pytest.approx(30, abs=2)


def test_primary_prefers_the_acceleration_criteria():
    cycles, values = _piecewise(knee=30)
    analysis = detect_knee(cycles, values, reference_cycle=1)
    assert analysis.primary.method == "segmented"


def test_a_linear_fade_reports_no_knee_and_says_why():
    cycles = list(range(1, 51))
    values = [5.0 - 0.01 * (c - 1) for c in cycles]
    analysis = detect_knee(cycles, values, reference_cycle=1)
    segmented = analysis.by_method("segmented")
    assert not segmented.detected
    assert "accelerates" in segmented.reason or "not fading" in segmented.reason


def test_a_flat_series_is_not_a_knee():
    cycles = list(range(1, 31))
    analysis = detect_knee(cycles, [5.0] * 30, reference_cycle=1)
    assert not analysis.by_method("segmented").detected
    assert not analysis.by_method("slope_ratio").detected


def test_a_flat_series_has_no_knee_by_any_criterion():
    """A cell that has not lost a thing must not be given a knee cycle."""
    cycles = list(range(1, 31))
    analysis = detect_knee(cycles, [5.0] * 30, reference_cycle=1)
    assert not analysis.by_method("curvature").detected
    assert not analysis.primary.detected


def test_a_linear_fade_has_no_curvature_knee():
    cycles = list(range(1, 51))
    values = [5.0 - 0.01 * (c - 1) for c in cycles]
    analysis = detect_knee(cycles, values, reference_cycle=1)
    assert not analysis.by_method("curvature").detected
    assert not analysis.primary.detected


def test_curvature_still_finds_a_planted_knee():
    """The guards above must not silence the criterion on a real bend."""
    cycles, values = _piecewise(knee=30)
    curvature = detect_knee(cycles, values, reference_cycle=1).by_method("curvature")
    assert curvature.detected
    assert curvature.cycle == pytest.approx(30, abs=4)


def test_a_rising_then_falling_series_is_a_knee():
    """Activation then collapse: fade begins at the break, so it accelerates."""
    cycles = list(range(1, 81))
    values = [5.0 * (1.0 + 0.002 * (c - 1)) if c <= 35
              else 5.0 * (1.0 + 0.002 * 34 - 0.016 * (c - 35)) for c in cycles]
    analysis = detect_knee(cycles, values, reference_cycle=1)
    segmented = analysis.by_method("segmented")
    assert segmented.detected
    assert segmented.cycle == pytest.approx(35, abs=3)
    assert analysis.primary.method == "segmented"


def test_a_missing_reference_cycle_does_not_fall_back_to_formation():
    """Cycle 3 unusable must promote cycle 4, never the formation cycle."""
    cycles = list(range(1, 41))
    values = [6.0, 5.2, float("nan")] + [5.0 - 0.01 * (c - 4) for c in range(4, 41)]
    analysis = detect_knee(cycles, values, reference_cycle=3)
    assert analysis.reference_cycle == 4
    assert analysis.reference_capacity_mah == pytest.approx(5.0)
    assert analysis.search_start_cycle == 4
    assert analysis.reference_note and "no usable capacity" in analysis.reference_note


def test_a_single_glitch_cycle_is_not_an_end_of_life_crossing():
    """One check-up cycle below 80 % that recovers is not end of life."""
    cycles = list(range(1, 101))
    values = [5.0 - 0.0025 * (c - 1) for c in cycles]
    values[49] = 3.9   # 78 % for one cycle, back to ~97 % the next
    analysis = detect_knee(cycles, values, reference_cycle=1)
    threshold = analysis.by_method("threshold")
    assert not threshold.detected
    assert "recovered" in threshold.reason
    assert not analysis.primary.detected


def test_threshold_interpolates_the_crossing():
    cycles = [1, 2, 3, 4, 5]
    values = [5.0, 5.0, 5.0, 4.0, 3.0]   # 80% of 5.0 is exactly 4.0
    result = detect_knee(cycles, values, reference_cycle=1).by_method("threshold")
    assert result.detected
    assert result.cycle == pytest.approx(4.0, abs=0.5)


def test_threshold_reports_when_it_never_crosses():
    result = detect_knee([1, 2, 3], [5.0, 4.9, 4.8],
                         reference_cycle=1).by_method("threshold")
    assert not result.detected
    assert "never fell below" in result.reason


def test_the_search_starts_at_the_reference_cycle():
    """Formation loss before the reference must not set the baseline rate."""
    cycles = list(range(1, 41))
    # A steep formation drop, then flat, then a real knee at cycle 25.
    values = [6.0, 5.2] + [5.0 - 0.002 * (c - 3) for c in range(3, 26)] \
        + [4.954 - 0.06 * (c - 25) for c in range(26, 41)]
    analysis = detect_knee(cycles, values, reference_cycle=3)
    assert analysis.search_start_cycle == 3
    assert analysis.reference_cycle == 3
    # Early-life fade must reflect cycles 3+, not the formation drop.
    assert analysis.fade_rate_early_pct_per_cycle == pytest.approx(-0.04, abs=0.05)
    assert analysis.by_method("segmented").cycle == pytest.approx(25, abs=3)


def test_too_few_cycles_is_reported_not_guessed():
    analysis = detect_knee([1, 2, 3], [5.0, 4.9, 4.8], reference_cycle=1)
    segmented = analysis.by_method("segmented")
    assert not segmented.detected
    assert "at least" in segmented.reason


def test_empty_series_is_handled():
    analysis = detect_knee([], [])
    assert analysis.n_points == 0
    assert not analysis.primary.detected


def test_smoothing_rejects_a_single_dropped_sample():
    values = np.array([5.0, 5.0, 0.1, 5.0, 5.0])
    assert smooth_series(values, 3)[2] == pytest.approx(5.0)


def test_projection_to_the_threshold_only_when_still_above_it():
    cycles = list(range(1, 21))
    values = [5.0 - 0.02 * (c - 1) for c in cycles]  # ends at 4.62, i.e. 92%
    analysis = detect_knee(cycles, values, reference_cycle=1)
    assert analysis.projected_cycle_at_80pct > 20


# --- 원형 곡선들 --------------------------------------------------------------
#
# 여기가 knee.py 의 상수들이 정해진 자리다.  기준마다 강한 곳과 약한 곳이 다르고
# 넷을 다 보여 주는 이유가 그것이므로, 판정은 곡선의 모양별로 고정한다.
#
# 정답은 구간으로 준다.  중앙값 평활(5점)이 꺾임을 1~2 사이클 앞으로 당기므로
# 한 사이클을 딱 집어 요구하면 평활 창을 못 건드리게 되는데, knee 를 그만한
# 해상도로 말할 수 있다고 주장하고 싶지도 않다.


def _curve(n, fn, *, noise=0.003, seed=0, q0=1.45):
    """유지율 함수를 실제 셀처럼 만든다 — formation 두 사이클 + 계측 잡음."""
    rng = np.random.default_rng(seed)
    cycles = np.arange(1, n + 1, dtype=float)
    q = q0 * np.array([fn(c) for c in cycles], float) / 100.0
    q = q * (1 + rng.normal(0, noise, n))
    q[0] = q[1] = q0 * 0.09          # formation 은 설계상 몇 % 를 잃는다
    return cycles, q


def _flat_then_crash_then_ease(c):
    """이 랩의 고전압 셀 모양: 평탄 → 며칠 만에 급감 → 다시 완만."""
    if c <= 23:
        return 100.0 - 0.16 * (c - 3)
    if c <= 32:
        return 96.8 - 4.9 * (c - 23)
    return 52.7 - 22.0 * (1 - np.exp(-(c - 32) / 14.0))


def _flat_then_accelerate(c):
    return 100.0 - 0.12 * (c - 3) if c <= 40 else 95.6 - 1.4 * (c - 40)


def _gentle(c):
    """0.05 → 0.16 %/cycle. 급감은 아니지만 200 사이클이면 20 % 차이다."""
    return 100.0 - 0.05 * (c - 3) if c <= 60 else 97.15 - 0.16 * (c - 60)


def _decelerating(c):
    return 100.0 - 30.0 * (1 - np.exp(-(c - 3) / 25.0))


def test_a_crash_that_eases_off_is_still_a_knee():
    """두 직선으로 못 그리는 모양 — 세 번째 직선을 물어봐야 한다.

    평탄→급감→감속 곡선에서 가장 잘 맞는 *두* 직선의 절점은 감속 구간에 놓인다.
    거기서는 열화가 이전보다 느리므로 두 직선 기준은 "가속하지 않는다" 는 옳은
    답을 내놓지만, 사람 눈에 뻔히 보이는 꺾임에 대해서는 아무 말도 못 한다.
    """
    cycles, q = _curve(62, _flat_then_crash_then_ease, seed=1, noise=0.004)
    segmented = detect_knee(cycles, q, reference_cycle=3).by_method("segmented")
    assert segmented.detected, segmented.reason
    # 평활 창이 꺾임을 1~2 사이클 앞으로 당긴다.  knee 를 그보다 정밀하게
    # 말할 수 있다고 주장하지 않는다.
    assert segmented.cycle == pytest.approx(23, abs=3)
    assert segmented.detail["segments"] == 3.0
    # 두 번째 절점(다시 완만해지는 곳)도 말해야 한다 — 그게 이 셀의 이야기다.
    assert segmented.detail["second_breakpoint"] > segmented.cycle
    assert "eases off" in segmented.reason


def test_every_criterion_agrees_on_the_crash_cell():
    cycles, q = _curve(62, _flat_then_crash_then_ease, seed=1, noise=0.004)
    analysis = detect_knee(cycles, q, reference_cycle=3)
    for method in ("segmented", "slope_ratio", "curvature"):
        result = analysis.by_method(method)
        assert result.detected, f"{method}: {result.reason}"
        assert result.cycle == pytest.approx(23, abs=3), method


def test_a_healthy_cell_is_not_given_a_knee_by_arithmetic():
    """비율만 보면 무열화 셀도 knee 를 얻는다.

    -0.021 → -0.116 %/cycle 은 5.55 배지만, 남은 사이클을 다 합쳐도 0.5 % 다.
    비율은 크기를 말해 주지 않는다.
    """
    cycles, q = _curve(90, lambda c: 100.0 - 0.02 * (c - 3), seed=4)
    analysis = detect_knee(cycles, q, reference_cycle=3)
    for method in ("segmented", "slope_ratio", "curvature"):
        result = analysis.by_method(method)
        assert not result.detected, f"{method} 가 건강한 셀에 knee 를 줬다: {result.reason}"
    assert not analysis.primary.detected


def test_end_of_life_is_not_reported_as_a_knee():
    """80 % 통과는 EOL 이지 급감이 아니다.

    threshold 는 셀이 늙기만 하면 언제나 답이 있으므로, primary 의 fallback 으로
    두면 완벽하게 직선으로 열화하는 셀에 "74번에서 용량 급감" 이 붙는다.
    """
    cycles, q = _curve(120, lambda c: 100.0 - 0.28 * (c - 3), seed=3, noise=0.004)
    analysis = detect_knee(cycles, q, reference_cycle=3)
    assert analysis.by_method("threshold").detected      # 80 % 는 실제로 지났다
    assert not analysis.primary.detected
    assert analysis.primary.method != "threshold"


def test_noise_is_not_a_knee():
    """창 하나의 기울기는 스스로 요동한다.

    기준의 2배는 -0.23 %/cycle 인데, 40번에서 꺾이는 셀의 24번 창이 잡음만으로
    -0.27 을 찍었다.  잡음 폭만큼 한도를 내려 잡지 않으면 그게 knee 가 된다.
    """
    cycles, q = _curve(80, _flat_then_accelerate, seed=2)
    result = detect_knee(cycles, q, reference_cycle=3).by_method("slope_ratio")
    assert result.detected, result.reason
    assert result.cycle == pytest.approx(40, abs=4), result.reason


def test_a_gentle_knee_is_found_by_the_two_line_fit():
    """완만한 knee 는 전역 적합만 잡는다 — 기준이 넷인 이유가 이것이다.

    0.05 → 0.16 %/cycle 은 창 하나로 보면 잡음에 묻히지만, 200 사이클을 한꺼번에
    쓰는 두 직선 적합에는 뚜렷하다.
    """
    cycles, q = _curve(200, _gentle, seed=11)
    segmented = detect_knee(cycles, q, reference_cycle=3).by_method("segmented")
    assert segmented.detected, segmented.reason
    assert segmented.cycle == pytest.approx(60, abs=6)


def test_a_decelerating_cell_has_no_knee():
    """처음이 가장 가파르고 점점 완만해지는 셀 — 역방향이다."""
    cycles, q = _curve(90, _decelerating, seed=9)
    analysis = detect_knee(cycles, q, reference_cycle=3)
    for method in ("segmented", "slope_ratio", "curvature"):
        assert not analysis.by_method(method).detected, method


def test_one_dropped_cycle_is_not_a_knee():
    cycles, q = _curve(90, lambda c: 100.0 - 0.25 * (c - 3), seed=8, noise=0.002)
    q[45] *= 0.55
    analysis = detect_knee(cycles, q, reference_cycle=3)
    for method in ("segmented", "slope_ratio", "curvature"):
        assert not analysis.by_method(method).detected, method


def test_the_three_line_escalation_stays_fast_on_a_long_record():
    """3선 스캔은 이차라 격자를 솎는다.  긴 기록에서도 요청 안에 끝나야 한다."""
    import time

    def shape(c):
        if c <= 200:
            return 100.0 - 0.02 * c
        if c <= 260:
            return 96.0 - 0.35 * (c - 200)
        return 75.0 - 0.03 * (c - 260)

    cycles, q = _curve(500, shape, seed=13)
    started = time.perf_counter()
    detect_knee(cycles, q, reference_cycle=3)
    assert time.perf_counter() - started < 2.0


def _noisy_linear(seed):
    """A straight-line fade with random length, rate and noise.

    One draw order, one seed: the sweep below and the single-curve tests have to
    produce the very same curve, or a case pinned here is not the case the sweep
    found.
    """
    rng = np.random.default_rng(seed)
    n = int(rng.integers(30, 200))
    rate = float(rng.uniform(0.0, 0.5))
    noise = float(rng.uniform(0.001, 0.02))
    cycles = np.arange(1, n + 1, dtype=float)
    q = 1.45 * (100 - rate * (cycles - 3)) / 100 * (1 + rng.normal(0, noise, n))
    q[0] = q[1] = 1.45 * 0.09
    return cycles, q


def test_a_bend_has_to_fit_better_than_no_bend():
    """비율도 손실도 통과하는데 적합은 나아지지 않는 경우가 있다.

    이 곡선은 그냥 직선 열화다.  가장 잘 맞는 절점에서 기울기가 1.50배가 되고
    이후 58 % 를 잃지만 (기록이 길어서), 꺾은 선은 곧은 선보다 나은 설명을
    못 한다.  F 게이트가 없으면 이 셀에 knee 가 붙는다.
    """
    cycles, q = _noisy_linear(19)
    segmented = detect_knee(cycles, q, reference_cycle=3).by_method("segmented")
    assert not segmented.detected, segmented.reason
    assert "fits no better" in segmented.reason
    assert segmented.detail["slope_ratio"] >= 1.5      # 비율 게이트는 통과했다
    assert segmented.detail["drop_after_pct"] >= 2.0   # 손실 게이트도 통과했다


def test_straight_line_fades_never_get_a_knee():
    """길이·속도·잡음을 무작위로 흩은 직선 열화 200개에 knee 가 하나도 없어야 한다.

    원형 곡선 몇 개로는 안 드러난다.  기준을 정할 때 이 sweep 이 slope_ratio 의
    17 % 오탐과 curvature 의 10 % 오탐을 잡아냈다.
    """
    false_positives = []
    for seed in range(200):
        cycles, q = _noisy_linear(seed)
        analysis = detect_knee(cycles, q, reference_cycle=3)
        for method in ("segmented", "slope_ratio", "curvature"):
            result = analysis.by_method(method)
            if result.detected:
                false_positives.append((seed, method, result.cycle, result.reason))
    assert not false_positives, false_positives[:5]


def test_the_early_life_rate_is_a_median_not_one_window():
    """첫 창의 기울기는 부호부터 틀릴 수 있다.

    이 곡선의 첫 5-사이클 창은 +0.35 %/cycle -- 열화하는 셀인데 오르고 있다.
    기준을 그 창으로 잡으면 '초기가 평탄하다' 로 읽혀 한도가 0 근처로 내려가고,
    이후 아무 창이나 knee 가 된다.
    """
    from wrdkit.knee import _linear_fit, smooth_series

    cycles, q = _noisy_linear(42)
    search = cycles[2:]
    values = smooth_series(100.0 * q[2:] / q[2], 5)
    window = 5
    local = np.array([_linear_fit(search[s:s + window], values[s:s + window])[0]
                      for s in range(len(search) - window + 1)])
    assert local[0] > 0, "이 픽스처의 전제: 첫 창이 오른다"
    assert float(np.median(local[:max(5, len(search) // 4)])) < 0

    result = detect_knee(cycles, q, reference_cycle=3).by_method("slope_ratio")
    assert not result.detected, result.reason


def test_the_window_speaks_for_its_middle_not_its_first_cycle():
    """창 기울기는 그 창의 가운데에 대한 근거다.

    시작 사이클을 답으로 적으면 knee 가 창 길이의 절반만큼 앞당겨진다.
    """
    def collapse(c):
        return 100.0 - 0.08 * (c - 3) if c <= 55 else 95.8 - 6.0 * (c - 55)

    cycles, q = _curve(68, collapse, seed=6)
    result = detect_knee(cycles, q, reference_cycle=3).by_method("slope_ratio")
    assert result.detected, result.reason
    assert result.cycle == pytest.approx(55, abs=2), result.reason


def test_curvature_is_never_the_primary_answer():
    """곡률은 교차 확인이지 판정이 아니다 -- argmax 는 언제나 존재한다."""
    cycles, q = _curve(80, _flat_then_accelerate, seed=2)
    analysis = detect_knee(cycles, q, reference_cycle=3)
    assert analysis.by_method("curvature").detected
    assert analysis.primary.method in ("segmented", "slope_ratio")


def test_curvature_needs_real_segments_on_both_sides():
    """세 점을 지나는 직선은 기울기가 아니다.

    가장자리 여유가 2 였을 때 곡률 정점이 5번 사이클에 놓이고, 그 '초기 수명'
    이란 것이 세 사이클짜리였다.  비율은 당연히 inf 가 나온다.
    """
    from wrdkit.knee import MIN_SEGMENT

    cycles, q = _noisy_linear(76)
    result = detect_knee(cycles, q, reference_cycle=3).by_method("curvature")
    if result.cycle is not None:
        assert result.cycle >= cycles[2] + MIN_SEGMENT
    assert not result.detected, result.reason


def test_a_real_bend_with_no_consequence_is_not_a_knee():
    """확실히 꺾이지만 그 뒤로 1 % 밖에 안 잃는 셀.

    적합으로만 보면 완벽한 knee 다 -- 두 직선이 곡선을 거의 그대로 지나가고,
    기울기는 무한대 배로 가팔라진다.  그런데 꺾인 뒤 50 사이클 동안 잃는 것이
    1 % 다.  이건 knee 가 아니라 측정 분해능이다.  손실 게이트만 이걸 막는다.
    """
    def bend_that_costs_nothing(c):
        return 100.0 if c <= 50 else 100.0 - 0.02 * (c - 50)

    cycles, q = _curve(100, bend_that_costs_nothing, seed=21, noise=0.0002)
    segmented = detect_knee(cycles, q, reference_cycle=3).by_method("segmented")
    assert not segmented.detected, segmented.reason
    assert "is lost" in segmented.reason
    # 전제: 적합도와 비율 게이트는 통과한다 -- 막은 것은 손실 게이트뿐이다.
    assert segmented.detail["f_statistic"] >= 100.0
    assert segmented.detail["slope_ratio"] >= 1.5
