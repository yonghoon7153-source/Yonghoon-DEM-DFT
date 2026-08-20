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
