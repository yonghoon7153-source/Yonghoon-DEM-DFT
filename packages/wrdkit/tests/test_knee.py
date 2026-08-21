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
    cycles = [1, 2, 3, 4, 5, 6]
    values = [5.0, 5.0, 5.0, 4.0, 3.0, 2.5]   # 80% of 5.0 is exactly 4.0
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
        return 100.0 if c <= 50 else 100.0 - 0.003 * (c - 50)

    cycles, q = _curve(340, bend_that_costs_nothing, seed=21, noise=0.0002)
    segmented = detect_knee(cycles, q, reference_cycle=3).by_method("segmented")
    assert not segmented.detected, segmented.reason
    # 전제: 적합도와 비율 게이트는 통과한다 -- 막은 것은 손실 게이트뿐이다.
    assert segmented.detail["fit_gain_score"] >= 100.0
    # 평탄하다 꺾이므로 비율은 무한대다 — detail 은 그걸 플래그로 적는다
    # (JSON 에 Infinity 를 넣으면 표준을 지키는 클라이언트가 전부 거부한다).
    assert segmented.detail["fade_starts_here"] == 1.0
    assert "slope_ratio" not in segmented.detail
    # 꺾인 뒤로 290 사이클을 더 봤는데 1 % 다.  기록이 짧아서가 아니라 그
    # 꺾임이 아무 대가도 치르지 않은 것이므로 "모른다" 가 아니라 "없다" 다.
    assert segmented.status == "none", segmented.reason
    assert "is lost" in segmented.reason
    assert segmented.candidate_cycle == pytest.approx(50, abs=4)


# --- 판정 네 가지 --------------------------------------------------------------
#
# `detected=False` 하나로 "knee 없음" 과 "아직 모른다" 를 같이 표현하면, 일찍
# 뽑은 셀이 안 꺾인 셀과 똑같아 보인다.  기록 길이가 다른 셀끼리 knee 비율을
# 비교하는 순간 그 혼동이 결론이 된다.


def test_the_same_cell_cut_two_cycles_earlier_is_not_a_healthy_cell():
    """같은 파일을 17번에서 자르면 None, 19번까지 있으면 12번 knee 였다.

    바뀐 것은 셀이 아니라 언제 멈췄는가다.  둘 다 '12번에서 꺾였다' 로 답하되,
    짧은 쪽은 확정이 아니라 근거 부족이어야 한다.
    """
    def planted(c):
        return 100 - 0.03 * (min(c, 12) - 3) - 0.35 * max(c - 12, 0)

    # 잡음 없이 — 이 테스트가 고정하려는 것은 "언제 멈췄나" 하나다.  0.3 % 잡음을
    # 얹으면 6 사이클짜리 후속 구간의 적합도가 문턱 근처에서 흔들려, 검열 문제
    # 대신 문턱 보정 문제를 재는 테스트가 된다.
    short = detect_knee(*_curve(17, planted, noise=0.0),
                        reference_cycle=3).by_method("segmented")
    longer = detect_knee(*_curve(19, planted, noise=0.0),
                         reference_cycle=3).by_method("segmented")

    assert longer.detected and longer.cycle == pytest.approx(12, abs=1)
    assert not short.detected
    assert short.status == "insufficient", short.reason
    assert short.candidate_cycle == pytest.approx(12, abs=1)
    # 두 답이 가리키는 사이클은 같아야 한다 — 셀은 하나다.
    assert short.candidate_cycle == pytest.approx(longer.cycle, abs=1)


def test_a_slow_cell_watched_long_enough_is_answered_not_deferred():
    """느린 셀도 충분히 오래 보면 답이 나와야 한다.

    "언젠가는 2 % 에 도달한다" 는 모든 열화가 참이므로, 그걸로 판단을 미루면
    `insufficient` 가 모든 것을 삼킨다.  이미 본 만큼을 한 번 더 봐서 판가름
    날 때에만 미룬다.
    """
    def slow(c):
        return 100 - 0.005 * (min(c, 101) - 3) - 0.012 * max(c - 101, 0)


    # 전체 열화가 2 % 대인 셀이라 0.3 % 잡음이면 신호가 잡음에 묻힌다.
    early = detect_knee(*_curve(250, slow, noise=0.0002),
                        reference_cycle=3).by_method("segmented")
    later = detect_knee(*_curve(400, slow, noise=0.0002),
                        reference_cycle=3).by_method("segmented")
    # 400 이면 확정된다.  250 은 아직 2 % 에 못 미치지만 "없다" 가 아니라 "아직" 이다.
    assert later.detected, later.reason
    assert early.status == "insufficient", early.reason
    assert early.candidate_cycle == pytest.approx(later.cycle, rel=0.15)


def test_a_crossing_on_the_last_cycle_did_not_recover():
    """마지막 한 점이 80 % 를 넘은 것은 '회복했다' 가 아니다.

    `under[c:c+2].all()` 은 슬라이스가 하나짜리여도 참이라, 기록의 마지막
    측정만 아래로 내려가도 EOL 통과로 인정됐다.  반대로 무조건 거부하면 이번엔
    "회복했다" 는 없는 데이터에 대한 주장이 된다.
    """
    cycles = np.arange(3, 13, dtype=float)
    values = np.array([100.0] * 9 + [79.0])
    result = detect_knee(cycles, values, reference_cycle=3).by_method("threshold")
    assert not result.detected
    assert result.status == "insufficient", result.reason
    assert "recover" not in result.reason
    assert result.candidate_cycle == pytest.approx(12, abs=1)


def test_a_dip_that_really_did_recover_still_says_so():
    cycles = np.arange(3, 15, dtype=float)
    values = np.array([100.0] * 5 + [79.0] + [100.0] * 6)
    result = detect_knee(cycles, values, reference_cycle=3).by_method("threshold")
    assert not result.detected
    assert result.status == "none"
    assert "recovered" in result.reason


# --- Codex 리뷰가 찾아낸 것들 ---------------------------------------------------
#
# 각 테스트는 리뷰의 재현을 그대로 굳힌 것이다.  이름은 증상이 아니라 계약을
# 말한다 — 같은 실수를 다른 모양으로 다시 하지 않기 위해서다.


def test_a_bend_is_certified_by_its_own_contribution_not_by_a_later_one():
    """뒤의 진짜 knee 가 앞의 아무 transient 나 인증해서는 안 된다.

    급감 후 감속하는 셀을 살리려고 후보 절점 뒤에 자유 절점 하나를 허용했는데,
    비교 대상이 '직선 대 두 절점 전체' 였다.  그래서 80번의 진짜 knee 가
    34번의 잡음을 통과시켰다 — 혼자서는 66점이던 것이 79번을 옆에 두자
    34,877점이 됐다.  게다가 그 곡선의 첫 '절점' 은 가속이 아니라 감속이다.
    """
    def dip_then_knee(c):
        base = 100 - 0.04 * (min(c, 80) - 3) - 0.70 * max(c - 80, 0)
        return base - (1.0 if 35 <= c < 38 else 0.0)

    analysis = detect_knee(*_curve(120, dip_then_knee, noise=0.0005), reference_cycle=3)
    # 어느 기준도 35~37번의 dip 을 knee 로 보고해서는 안 된다.  80번을 짚는
    # 것은 옳다 — 거기가 진짜 knee 다.
    for method in ("segmented", "slope_ratio", "curvature"):
        result = analysis.by_method(method)
        if result.detected:
            assert result.cycle == pytest.approx(80, abs=4), f"{method}: {result.reason}"


def test_three_lines_are_tried_whatever_rejected_two():
    """세 선을 '두 선이 감속으로 거부될 때만' 열면 정확히 세 선인 곡선을 놓친다.

    절점 7/12, 기울기 -0.10 → -0.30 → -0.25 인 30 사이클 곡선.  두 선으로는
    77점이라 거부되고, 세 선은 절점과 기울기를 소수점 셋째 자리까지 복원한다.
    """
    def exact_three(c):
        return (100
                - 0.10 * (min(c, 7) - 3)
                - 0.30 * max(min(c, 12) - 7, 0)
                - 0.25 * max(c - 12, 0))

    result = detect_knee(*_curve(30, exact_three, noise=0.0), reference_cycle=3)
    segmented = result.by_method("segmented")
    assert segmented.detected, segmented.reason
    assert segmented.cycle == pytest.approx(7, abs=1)
    assert segmented.detail["second_breakpoint"] == pytest.approx(12, abs=1)


def test_the_second_transition_can_be_the_knee():
    """급감 후 회복, 그 다음 붕괴 — knee 는 두 번째 절점이다.

    '첫 절점이 곧 knee' 는 급감→감속이라는 한 원형에만 맞는다.  첫 전이만
    보던 판정은 두 번째 절점의 45배 가속을 통째로 버리고 None 을 냈다.
    """
    def recover_then_collapse(c):
        return (100
                - 0.55 * (min(c, 22) - 3)
                - 0.02 * max(min(c, 88) - 22, 0)
                - 0.90 * max(c - 88, 0))

    segmented = detect_knee(*_curve(100, recover_then_collapse, noise=0.0),
                            reference_cycle=3).by_method("segmented")
    assert segmented.detected, segmented.reason
    assert segmented.cycle == pytest.approx(88, abs=2)
    assert segmented.detail["knee_transition"] == 2.0


def test_break_points_are_found_at_cycle_resolution_on_a_long_record():
    """긴 기록에서도 절점은 사이클 단위로 찾는다.

    격자를 축마다 32점으로 솎았더니 1,000 사이클짜리에서 첫 절점 후보가
    7, 39, 71, ... 뿐이었다.  10~25번에 급감한 셀은 27/31 로 적합되고, 그
    잘못된 적합의 두 번째 전이가 모든 게이트를 통과했다 — 놓치는 것보다 나쁘다.
    """
    def early_crash(c):
        return (100
                - 0.02 * (min(c, 10) - 3)
                - 1.00 * max(min(c, 25) - 10, 0)
                - 0.02 * max(c - 25, 0))

    segmented = detect_knee(*_curve(1000, early_crash, noise=0.0),
                            reference_cycle=3).by_method("segmented")
    assert segmented.detected, segmented.reason
    assert segmented.cycle == pytest.approx(10, abs=2), segmented.reason
    assert segmented.detail["second_breakpoint"] == pytest.approx(25, abs=2)


def test_the_exhaustive_break_search_matches_brute_force():
    """전수 탐색은 prefix 합으로 계산한다 — 브루트포스와 같은 답이어야 한다."""
    from wrdkit.knee import MIN_SEGMENT, _exact_three_break, _hinge_fit

    rng = np.random.default_rng(0)
    for _ in range(5):
        n = int(rng.integers(15, 40))
        x = np.arange(1, n + 1, dtype=float)
        y = 100 - rng.uniform(0, 0.2) * x + rng.normal(0, 0.3, n)
        got = _exact_three_break(x, y)
        brute = min(
            (_hinge_fit(x, y, (x[i], x[j]))[0], x[i], x[j])
            for i in range(MIN_SEGMENT, n - MIN_SEGMENT)
            for j in range(i + MIN_SEGMENT, n - MIN_SEGMENT)
        )
        assert got[0] == pytest.approx(brute[0], rel=1e-9)
        assert (got[1], got[2]) == (brute[1], brute[2])


def test_early_life_does_not_grow_with_the_record():
    """같은 셀을 더 오래 봤다고 초기 수명의 정의가 바뀌면 안 된다.

    baseline 창이 `max(5, n // 4)` 였다.  150 사이클에서 37 사이클이던 창이
    500 사이클에서는 124 사이클이 되고, 그 중앙값은 이미 *후기* 기울기다 —
    51번에 보고했던 knee 가 데이터를 더 넣자 사라졌다.
    """
    def early_knee(c):
        return 100 - 0.03 * (min(c, 50) - 3) - 0.08 * max(c - 50, 0)

    short = detect_knee(*_curve(150, early_knee, noise=0.0),
                        reference_cycle=3).by_method("slope_ratio")
    longer = detect_knee(*_curve(500, early_knee, noise=0.0),
                         reference_cycle=3).by_method("slope_ratio")
    assert short.detected, short.reason
    assert longer.detected, longer.reason
    assert longer.cycle == pytest.approx(short.cycle, abs=5)


def test_a_failing_first_candidate_does_not_hide_a_later_knee():
    """첫 후보가 게이트에서 져도 뒤 후보를 계속 본다.

    60~71번의 일시적인 5 %p 낙차가 첫 후보로 잡히고 gain 96.8 로 아깝게
    떨어지면, 95번의 진짜 영구 knee 는 검사조차 되지 않았다.  그러면서
    이유는 "한 번도 넘은 적 없다" 였다.
    """
    def transient_then_real(c):
        base = 100 - 0.04 * (min(c, 95) - 3) - 1.0 * max(c - 95, 0)
        return base - (5.0 if 60 <= c < 72 else 0.0)

    result = detect_knee(*_curve(108, transient_then_real, noise=0.0),
                         reference_cycle=3).by_method("slope_ratio")
    assert result.detected, result.reason
    assert result.cycle == pytest.approx(95, abs=4)


def test_the_loss_is_measured_from_the_cycle_that_gets_reported():
    """보고 cycle 부터의 손실이 2 % 여야 한다 — 창 시작부터가 아니라.

    창의 가운데를 답으로 적도록 고쳤는데 손실은 창 시작에서 재고 있었다.
    그래서 '13번 이후로 2 % 를 잃는다' 고 보고하면서 실제로는 1.8 % 였다.
    """
    def shape(c):
        return 100 - 0.02 * (min(c, 12) - 3) - 0.30 * max(c - 12, 0)

    cycles, q = _curve(19, shape, noise=0.0)
    result = detect_knee(cycles, q, reference_cycle=3).by_method("slope_ratio")
    if result.detected:
        search = cycles[2:]
        values = smooth_series(100.0 * q[2:] / q[2], 5)
        index = int(np.flatnonzero(search == result.cycle)[0])
        assert values[index] - values[-1] >= 2.0, result.reason


def test_curvature_will_not_compare_a_three_point_slope():
    """세 점을 지나는 직선은 기울기가 아니다.

    가장자리 여유가 2 라 곡률 정점이 기준 사이클 바로 옆(5번)에 놓이고,
    비교 대상이 된 '초기 수명' 이 세 사이클짜리였다.  이 수정은 한 번
    들어갔다가 mutation 하네스가 오래된 백업으로 되돌리면서 날아갔는데,
    테스트가 `cycle is None` 이면 단언을 건너뛰는 바람에 통과했다.
    """
    from wrdkit.knee import MIN_SEGMENT

    def too_early(c):
        return 100.0 if c <= 5 else 100.0 - 2.0 * (c - 5)

    cycles, q = _curve(30, too_early, noise=0.0)
    result = detect_knee(cycles, q, reference_cycle=3).by_method("curvature")
    # 검출이든 아니든 후보 자체가 가장자리에서 MIN_SEGMENT 만큼 떨어져 있어야 한다.
    assert result.candidate_cycle is None or result.candidate_cycle >= 3 + MIN_SEGMENT


def test_no_usable_cycle_after_the_reference_is_indeterminate():
    """요청한 기준 이후에 데이터가 없으면 formation 으로 되돌아가지 않는다.

    `searchsorted` 가 n 을 반환하면 index 0 으로 떨어져 cycle 1 — 기준
    사이클이 존재하는 이유가 바로 그 사이클을 빼는 것인데(ADR 0004),
    그 되돌림이 평범한 조정처럼 적혀 나갔다.
    """
    analysis = detect_knee(np.arange(1, 6, dtype=float), np.linspace(1.0, 0.96, 5),
                           reference_cycle=50)
    assert analysis.primary.status == "indeterminate", analysis.primary.reason
    assert analysis.reference_cycle == 50
    assert "no usable cycle" in analysis.primary.reason


def test_the_earliest_event_comes_from_the_model_not_from_a_minimum():
    """knee 는 가속이 *시작된* 지점이고, 그건 모형이 찾는다.

    50번에 꺾이고 150번에 다시 붕괴하는 셀에서 두 직선은 147번을 짚는다 — 가장
    강한 절점 하나이지 onset 이 아니다.  세 직선이 두 절점을 다 놓으면 이른
    전이가 답이 되고, 방법들 사이에서 최솟값을 고를 일이 없다.
    """
    def two_knees(c):
        return (100
                - 0.03 * (min(c, 50) - 3)
                - 0.18 * max(min(c, 150) - 50, 0)
                - 0.90 * max(c - 150, 0))

    analysis = detect_knee(*_curve(180, two_knees, seed=1, noise=0.002), reference_cycle=3)
    segmented = analysis.by_method("segmented")
    assert segmented.detected, segmented.reason
    assert segmented.cycle == pytest.approx(50, abs=4), segmented.reason
    assert segmented.detail["second_breakpoint"] == pytest.approx(150, abs=6)
    assert analysis.primary.cycle == pytest.approx(50, abs=4)


def test_primary_is_not_the_minimum_of_two_noisy_estimates():
    """단일 knee 에서 방법들의 최솟값을 고르면 체계적으로 이르다.

    두 답이 두 사건인지 한 사건을 두 번 잰 것인지 먼저 가리지 않고 min 을 쓰면,
    knee 가 하나뿐인 셀에서도 잡음이 만든 이른 후보가 이긴다.  200개 기록에서
    두 직선 적합의 평균 오차는 +0.02 사이클인데 최솟값 규칙은 -8.2 였다.
    """
    cycles = np.arange(3, 163, dtype=float)
    truth = 80.0
    mean = (100
            - 0.05 * (np.minimum(cycles, truth) - 3)
            - 0.30 * np.maximum(cycles - truth, 0))

    errors = []
    for seed in range(40):
        values = mean * (1 + np.random.default_rng(seed).normal(0, 0.005, len(cycles)))
        primary = detect_knee(cycles, values, reference_cycle=3).primary
        if primary.detected:
            errors.append(primary.cycle - truth)
    assert errors
    assert abs(float(np.mean(errors))) < 1.0, float(np.mean(errors))

    # Codex 가 든 개별 예: slope_ratio 가 잡음으로 28번을 짚어도 답은 80번이다.
    values = mean * (1 + np.random.default_rng(2).normal(0, 0.005, len(cycles)))
    analysis = detect_knee(cycles, values, reference_cycle=3)
    assert analysis.primary.cycle == pytest.approx(80, abs=3), analysis.primary.reason


def test_every_detail_number_is_json_safe():
    """detail 에 Infinity 가 들어가면 표준을 지키는 클라이언트가 전부 거부한다.

    평탄하다 무너지는 셀은 비율이 무한대다 — 과학적으로는 옳고 JSON 으로는
    불가능하다.  플래그로 적는다.
    """
    import json

    cycles = list(range(1, 81))
    q = [5 * (1 + 0.002 * (x - 1)) if x <= 35
         else 5 * (1 + 0.002 * 34 - 0.016 * (x - 35)) for x in cycles]
    analysis = detect_knee(cycles, q, reference_cycle=1)
    segmented = analysis.by_method("segmented")
    assert segmented.detected
    assert segmented.detail["fade_starts_here"] == 1.0
    for result in analysis.results:
        json.dumps(result.detail, allow_nan=False)


def test_a_block_that_sat_lower_and_came_back_is_not_a_knee():
    """가역적인 C-rate/온도 구간을 열화 onset 으로 보고하면 안 된다.

    열화율은 처음부터 끝까지 -0.08 %/cycle 로 일정하고, 35~54 번만 측정 조건
    때문에 용량이 낮았다가 완전히 회복하는 셀.  연속 hinge 는 계단을 "급감 +
    회복" 으로 근사하므로 절점 두 개를 거기 쓰고, 이벤트가 시작하기도 *전인*
    33번을 knee 라고 보고했다.  계단 크기를 1 → 8 %p 로 바꿔도 33번 고정이었다.

    2 % 손실 게이트로는 못 막는다.  계단의 비가역 결과가 아니라 그 뒤 정상적인
    배경 열화를 끝까지 합산하기 때문이다.
    """
    for size in (1.0, 4.0, 8.0):
        def rate_block(c, step=size):
            return 100 - 0.08 * (c - 3) - (step if 35 <= c < 55 else 0.0)

        analysis = detect_knee(*_curve(80, rate_block), reference_cycle=3)
        for method in ("segmented", "slope_ratio", "curvature"):
            result = analysis.by_method(method)
            assert not result.detected, f"{size}%p {method}: {result.reason}"
        assert not analysis.primary.detected


def test_the_excursion_is_named_with_the_cycles_it_covers():
    """그냥 거부하지 말고 무엇이었는지 말한다 — 실험 노트와 대조할 수 있게."""
    def rate_block(c):
        return 100 - 0.08 * (c - 3) - (4.0 if 35 <= c < 55 else 0.0)

    primary = detect_knee(*_curve(80, rate_block), reference_cycle=3).primary
    assert "sat" in primary.reason and "rejoined" in primary.reason
    assert primary.detail["excursion_from"] == pytest.approx(35, abs=2)
    assert primary.detail["excursion_to"] == pytest.approx(55, abs=2)


def test_a_permanent_step_is_still_a_real_loss():
    """돌아오지 않는 계단은 측정 아티팩트가 아니다 — 무엇이 원인이든 진짜 손실이다."""
    def permanent_step(c):
        return 100 - 0.08 * (c - 3) - (6.0 if c >= 40 else 0.0)

    analysis = detect_knee(*_curve(80, permanent_step), reference_cycle=3)
    assert "rejoined" not in analysis.primary.reason


def test_real_knees_survive_the_excursion_check():
    """계단 모형이 진짜 꺾임을 삼키면 안 된다.  적합 잔차 차이가 30~370 배다."""
    shapes = {
        "textbook": (80, lambda c: (100 - 0.12 * (c - 3)) if c <= 40
                     else 95.6 - 1.4 * (c - 40), 40),
        "crash then ease": (62, _flat_then_crash_then_ease, 23),
        "sudden death": (68, lambda c: (100 - 0.08 * (c - 3)) if c <= 55
                         else 95.8 - 6.0 * (c - 55), 55),
    }
    for label, (n, shape, expected) in shapes.items():
        analysis = detect_knee(*_curve(n, shape, noise=0.003), reference_cycle=3)
        assert analysis.primary.detected, f"{label}: {analysis.primary.reason}"
        assert analysis.primary.cycle == pytest.approx(expected, abs=4), label


def test_a_lull_followed_by_the_original_rate_is_not_a_knee():
    """느려졌다 원래 속도로 돌아온 것은 가속이 아니다.

    실측 161 사이클 셀이 -0.280 으로 열화하다 90 사이클 동안 -0.158 로 느려진
    뒤 -0.259 로 돌아왔다.  직전 구간과 견주면 121번에서 1.64배 "가속" 이고,
    셀 자신과 견주면 처음 속도로 돌아온 것뿐이다.  세 선의 두 번째 전이를
    직전 구간하고만 비교하던 것이 이 셀에 knee 를 붙였다.
    """
    def lull(c):
        return (100
                - 0.280 * (min(c, 32) - 3)
                - 0.158 * max(min(c, 121) - 32, 0)
                - 0.259 * max(c - 121, 0))

    analysis = detect_knee(*_curve(161, lull, noise=0.002), reference_cycle=3)
    for method in ("segmented", "slope_ratio", "curvature"):
        result = analysis.by_method(method)
        assert not result.detected, f"{method}: {result.reason}"


def test_a_second_transition_still_counts_when_it_beats_the_first_rate():
    """단, 처음 속도보다도 빨라졌으면 그것은 진짜 두 번째 knee 다."""
    def recover_then_collapse(c):
        return (100
                - 0.55 * (min(c, 22) - 3)
                - 0.02 * max(min(c, 88) - 22, 0)
                - 0.90 * max(c - 88, 0))

    result = detect_knee(*_curve(100, recover_then_collapse, noise=0.0),
                         reference_cycle=3).by_method("segmented")
    assert result.detected, result.reason
    assert result.cycle == pytest.approx(88, abs=2)


def test_all_three_criteria_agree_on_whether_the_evidence_is_in():
    """같은 저손실 bend 를 세 기준이 다른 상태로 말하면 안 된다.

    `slope_ratio` 의 detail 에는 `_not_yet` 이 읽는 값이 없었고 `curvature` 는
    적합도를 그 뒤에 계산했다.  둘 다 `insufficient` 가 될 수 없어서, 그 상태는
    사실상 segmented 전용이었다.
    """
    def planted(c):
        return 100 - 0.03 * (min(c, 12) - 3) - 0.35 * max(c - 12, 0)

    analysis = detect_knee(*_curve(17, planted, noise=0.0), reference_cycle=3)
    statuses = {m: analysis.by_method(m).status
                for m in ("segmented", "slope_ratio", "curvature")}
    assert set(statuses.values()) == {"insufficient"}, statuses
    for method, _ in statuses.items():
        assert analysis.by_method(method).candidate_cycle == pytest.approx(12, abs=2)


def test_the_answer_does_not_move_backwards_as_the_record_grows():
    """기록이 길어지면서 상태가 되돌아가면 안 된다.

    "절반은 왔다" 로 미루던 규칙은 같은 느린 셀을 60 사이클에서 insufficient,
    70~150 에서 none, 160 에서 다시 insufficient, 217 에서 detected 로 만들었다.
    70번 사이클에 셀에 일어난 일은 없다.
    """
    def slow(c):
        return 100 - 0.005 * (min(c, 50) - 3) - 0.012 * max(c - 50, 0)

    order = {"none": 0, "insufficient": 1, "detected": 2}
    seen = []
    for n in range(60, 261, 10):
        result = detect_knee(*_curve(n, slow, noise=0.0),
                             reference_cycle=3).by_method("segmented")
        seen.append((n, result.status))
    ranks = [order[status] for _, status in seen]
    assert ranks == sorted(ranks), seen


def test_a_bend_with_too_little_after_it_is_never_dismissed():
    """후속이 짧으면 "대가가 없다" 는 셀이 아니라 파일에 대한 진술이다."""
    def planted(c):
        return 100 - 0.03 * (min(c, 12) - 3) - 0.35 * max(c - 12, 0)

    result = detect_knee(*_curve(17, planted, noise=0.0),
                         reference_cycle=3).by_method("segmented")
    assert result.status == "insufficient"
    assert result.detail["followup_cycles"] < 20
