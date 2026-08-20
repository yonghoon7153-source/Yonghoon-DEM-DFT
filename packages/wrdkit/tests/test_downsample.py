"""LTTB downsampling."""

import numpy as np
import pytest

from wrdkit import lttb, lttb_indices


def test_a_short_curve_is_returned_unchanged():
    x = np.arange(10.0)
    out_x, out_y = lttb(x, x * 2, 100)
    assert np.array_equal(out_x, x)


def test_endpoints_are_always_kept():
    x = np.arange(1000.0)
    y = np.sin(x / 50)
    out_x, _ = lttb(x, y, 50)
    assert out_x[0] == x[0]
    assert out_x[-1] == x[-1]


def test_the_result_respects_the_threshold():
    x = np.arange(5000.0)
    y = np.random.default_rng(0).normal(size=5000)
    out_x, out_y = lttb(x, y, 200)
    assert len(out_x) <= 200
    assert len(out_x) == len(out_y)


def test_a_sharp_feature_survives():
    """A voltage plateau knee must not be smoothed away."""
    x = np.arange(2000.0)
    y = np.where(x < 1000, 3.0, 4.2)
    _, out_y = lttb(x, y, 100)
    assert out_y.min() == pytest.approx(3.0)
    assert out_y.max() == pytest.approx(4.2)


def test_indices_are_sorted_and_unique():
    x = np.arange(1000.0)
    keep = lttb_indices(x, np.sin(x / 30), 100)
    assert np.array_equal(keep, np.unique(keep))
