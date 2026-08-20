"""Find where a capacity-fade curve bends -- the "knee".

There is no single accepted definition of a knee, so this module implements
four defensible criteria and reports all of them rather than hiding the
choice.  They answer subtly different questions:

``threshold``    when did the cell cross an end-of-life line (e.g. 80 %)?
                 Unambiguous, but says nothing about *acceleration*.
``segmented``    where do two straight lines fit the curve best?  This is the
                 continuous piecewise-linear regression that the Bacon-Watts
                 knee model approximates, solved exactly by scanning every
                 candidate break point.
``slope_ratio``  at which cycle does the local fade rate first exceed the
                 early-life rate by a factor k?  Closest to what an operator
                 means by "it started dropping here".
``curvature``    where is the geometric curvature of the smoothed curve
                 greatest?  Sensitive to noise, useful as a cross-check.

A knee is only reported when the fade actually accelerates; a cell fading
linearly gets ``None`` and a stated reason instead of a spurious cycle
number.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

__all__ = ["KneeResult", "KneeAnalysis", "detect_knee", "smooth_series"]

#: A knee must be at least this many cycles from either end to be meaningful.
MIN_SEGMENT = 4
#: Fade must accelerate by at least this factor to count as a knee.
MIN_SLOPE_RATIO = 1.5
#: Slopes below this, in %/cycle, are floating-point noise on a flat curve --
#: 1e-6 %/cycle is 1 % lost over a million cycles.  Without this floor a
#: perfectly flat series produces a slope of ~1e-15 and every criterion finds
#: a "knee" where its neighbour's noise happens to be twice as large.
MIN_FADE_RATE = 1e-6
#: An end-of-life crossing must hold for this many consecutive cycles.  One
#: cycle below the line is a check-up or a temperature excursion, not EOL.
SUSTAINED_CROSSING = 2


@dataclass
class KneeResult:
    """One criterion's answer."""

    method: str
    cycle: float | None
    detected: bool
    reason: str = ""
    detail: dict[str, float] = field(default_factory=dict)


@dataclass
class KneeAnalysis:
    """Every criterion's answer, plus the one chosen as primary."""

    primary: KneeResult
    results: list[KneeResult]
    reference_cycle: int
    reference_capacity_mah: float | None
    n_points: int
    #: Cycle the knee search started from -- the reference cycle, so that
    #: formation losses never count as degradation.
    search_start_cycle: int = 0
    #: Set when the requested reference cycle had no usable capacity and the
    #: baseline moved to a later cycle -- never reported silently.
    reference_note: str | None = None
    fade_rate_early_pct_per_cycle: float | None = None
    fade_rate_late_pct_per_cycle: float | None = None
    projected_cycle_at_80pct: float | None = None

    def by_method(self, method: str) -> KneeResult | None:
        return next((r for r in self.results if r.method == method), None)


def smooth_series(values: np.ndarray, window: int = 5) -> np.ndarray:
    """Centred moving median, which rejects single-point instrument glitches.

    A mean would drag the curve towards an outlier; a median ignores it, and
    a dropped sample in a cycler log is far more common than genuine noise of
    that size.
    """
    n = len(values)
    if window <= 1 or n < 3:
        return values.astype(np.float64)
    window = min(window, n if n % 2 else n - 1)
    if window % 2 == 0:
        window -= 1
    if window < 3:
        return values.astype(np.float64)
    half = window // 2
    padded = np.pad(values.astype(np.float64), half, mode="edge")
    strided = np.lib.stride_tricks.sliding_window_view(padded, window)
    return np.median(strided, axis=1)


def _linear_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """Least-squares line; returns (slope, intercept, residual sum of squares)."""
    if len(x) < 2:
        return 0.0, float(y[0]) if len(y) else 0.0, 0.0
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return float(slope), float(intercept), float(np.sum(residual ** 2))


def _threshold_knee(cycles: np.ndarray, retention: np.ndarray,
                    level: float) -> KneeResult:
    under = retention < level
    below = np.flatnonzero(under)
    if not len(below):
        return KneeResult("threshold", None, False,
                          f"capacity never fell below {level:g}% "
                          f"(lowest {retention.min():.1f}%)",
                          {"level": level, "min_retention": float(retention.min())})
    # This is the only criterion fed the raw series, so the moving median never
    # gets to reject a one-cycle glitch for it; require the crossing to hold.
    sustained = [c for c in below if bool(under[c:c + SUSTAINED_CROSSING].all())]
    if not sustained:
        first = float(cycles[int(below[0])])
        return KneeResult("threshold", None, False,
                          f"dipped below {level:g}% at cycle {first:.0f} but recovered",
                          {"level": level, "min_retention": float(retention.min()),
                           "first_cycle_below": first})
    index = int(sustained[0])
    if index == 0:
        crossing = float(cycles[0])
    else:
        # Linear interpolation between the straddling cycles.
        x0, x1 = float(cycles[index - 1]), float(cycles[index])
        y0, y1 = float(retention[index - 1]), float(retention[index])
        crossing = x0 + (level - y0) * (x1 - x0) / (y1 - y0) if y1 != y0 else x1
    return KneeResult("threshold", crossing, True,
                      f"retention crossed {level:g}% at cycle {crossing:.1f}",
                      {"level": level, "first_cycle_below": float(cycles[index])})


def _segmented_knee(cycles: np.ndarray, values: np.ndarray) -> KneeResult:
    """Exact continuous two-segment regression by scanning break points."""
    n = len(cycles)
    if n < 2 * MIN_SEGMENT + 1:
        return KneeResult("segmented", None, False,
                          f"needs at least {2 * MIN_SEGMENT + 1} cycles, has {n}")

    single_slope, _, rss_single = _linear_fit(cycles, values)

    best = None
    for split in range(MIN_SEGMENT, n - MIN_SEGMENT):
        breakpoint = float(cycles[split])
        # Continuous hinge basis: y = a + b*x + c*max(x - breakpoint, 0)
        hinge = np.maximum(cycles - breakpoint, 0.0)
        design = np.column_stack([np.ones(n), cycles, hinge])
        coefficients, *_ = np.linalg.lstsq(design, values, rcond=None)
        residual = values - design @ coefficients
        rss = float(np.sum(residual ** 2))
        if best is None or rss < best[0]:
            best = (rss, breakpoint, coefficients)

    rss, breakpoint, coefficients = best
    slope_before = float(coefficients[1])
    slope_after = float(coefficients[1] + coefficients[2])

    detail = {
        "breakpoint": breakpoint,
        "slope_before": slope_before,
        "slope_after": slope_after,
        "rss_segmented": rss,
        "rss_single_line": rss_single,
    }
    if rss_single > 0:
        # F-like statistic comparing 3 parameters against 2.
        detail["f_statistic"] = float(
            ((rss_single - rss) / 1.0) / (rss / max(n - 3, 1))
        ) if rss > 0 else float("inf")

    if slope_before > -MIN_FADE_RATE and slope_after > -MIN_FADE_RATE:
        return KneeResult("segmented", None, False, "capacity is not fading", detail)
    if slope_after >= slope_before:
        return KneeResult("segmented", None, False,
                          "fade does not accelerate after the best break point", detail)

    if slope_before >= -MIN_FADE_RATE:
        # The guards above leave slope_after fading here, so a flat or rising
        # pre-break segment means fade *begins* at the break point -- activation
        # then collapse, common in all-solid-state cells.  Dividing would give a
        # negative ratio and reject the clearest knee shape there is.
        ratio = float("inf")
    else:
        ratio = slope_after / slope_before
    detail["slope_ratio"] = float(ratio)
    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("segmented", None, False,
                          f"fade accelerates only {ratio:.2f}x "
                          f"(needs {MIN_SLOPE_RATIO:g}x)", detail)

    if not np.isfinite(ratio):
        return KneeResult(
            "segmented", breakpoint, True,
            f"fade begins at cycle {breakpoint:.0f} "
            f"({slope_before:+.3f} -> {slope_after:.3f} %/cycle)",
            detail,
        )

    return KneeResult(
        "segmented", breakpoint, True,
        f"fade rate steepens {ratio:.2f}x at cycle {breakpoint:.0f} "
        f"({slope_before:.3f} -> {slope_after:.3f} %/cycle)",
        detail,
    )


def _slope_ratio_knee(cycles: np.ndarray, values: np.ndarray, *,
                      factor: float, baseline_window: int,
                      window: int) -> KneeResult:
    n = len(cycles)
    if n < baseline_window + window + 1:
        return KneeResult("slope_ratio", None, False,
                          f"needs at least {baseline_window + window + 1} cycles, has {n}")

    baseline_slope, _, _ = _linear_fit(cycles[:baseline_window], values[:baseline_window])
    detail = {"baseline_slope": baseline_slope, "factor": factor,
              "baseline_window": float(baseline_window)}
    if baseline_slope > -MIN_FADE_RATE:
        # A flat or rising early life gives no rate to compare against; fall
        # back to the fade of the whole series.
        overall, _, _ = _linear_fit(cycles, values)
        if overall > -MIN_FADE_RATE:
            return KneeResult("slope_ratio", None, False, "capacity is not fading", detail)
        baseline_slope = overall
        detail["baseline_slope"] = overall
        detail["baseline_source"] = 1.0

    limit = baseline_slope * factor
    detail["slope_limit"] = float(limit)
    for start in range(baseline_window, n - window + 1):
        local, _, _ = _linear_fit(cycles[start:start + window], values[start:start + window])
        if local <= limit:
            cycle = float(cycles[start])
            detail["slope_at_knee"] = float(local)
            return KneeResult(
                "slope_ratio", cycle, True,
                f"fade rate reached {factor:g}x the early-life rate "
                f"({local:.3f} vs {baseline_slope:.3f} %/cycle) at cycle {cycle:.0f}",
                detail,
            )
    return KneeResult("slope_ratio", None, False,
                      f"fade rate never reached {factor:g}x the early-life rate", detail)


def _curvature_knee(cycles: np.ndarray, values: np.ndarray, window: int) -> KneeResult:
    n = len(cycles)
    if n < 7:
        return KneeResult("curvature", None, False, f"needs at least 7 cycles, has {n}")
    smoothed = smooth_series(values, window)
    first = np.gradient(smoothed, cycles)
    second = np.gradient(first, cycles)
    curvature = np.abs(second) / np.power(1.0 + first ** 2, 1.5)
    # Ignore the edges, where gradient's one-sided differences dominate.
    margin = max(2, window // 2)
    interior = curvature[margin:n - margin]
    if not len(interior):
        return KneeResult("curvature", None, False, "series too short after edge trimming")
    index = margin + int(np.argmax(interior))
    cycle = float(cycles[index])
    slope_before, _, _ = _linear_fit(cycles[:index + 1], smoothed[:index + 1])
    slope_after, _, _ = _linear_fit(cycles[index:], smoothed[index:])
    detail = {"curvature": float(curvature[index]),
              "median_curvature": float(np.median(interior)),
              "slope_before": slope_before, "slope_after": slope_after}
    # An argmax always exists, so without these guards the criterion the other
    # three fall back to hands a healthy cell a knee cycle -- the largest
    # rounding ripple on a flat line, or the kink a single glitch leaves behind.
    if slope_before > -MIN_FADE_RATE and slope_after > -MIN_FADE_RATE:
        return KneeResult("curvature", None, False, "capacity is not fading", detail)
    ratio = (float("inf") if slope_before >= -MIN_FADE_RATE
             else slope_after / slope_before)
    detail["slope_ratio"] = float(ratio)
    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("curvature", None, False,
                          f"curvature peaks at cycle {cycle:.0f} but fade "
                          f"accelerates only {ratio:.2f}x there "
                          f"(needs {MIN_SLOPE_RATIO:g}x)", detail)
    return KneeResult("curvature", cycle, True,
                      f"maximum curvature at cycle {cycle:.0f}", detail)


def detect_knee(cycles, capacities, *, reference_cycle: int | None = None,
                threshold_pct: float = 80.0, slope_factor: float = 2.0,
                baseline_window: int = 5, slope_window: int = 5,
                smoothing_window: int = 5) -> KneeAnalysis:
    """Analyse a discharge-capacity series for a fade knee.

    ``cycles`` and ``capacities`` must be same-length sequences covering only
    complete cycles.  Capacities are converted to retention against
    ``reference_cycle``, and the knee search starts *at* that cycle: formation
    cycles lose several percent by design, and including them would set an
    early-life fade rate no later degradation could ever exceed.
    """
    cycles = np.asarray(list(cycles), dtype=np.float64)
    capacities = np.asarray(list(capacities), dtype=np.float64)
    order = np.argsort(cycles)
    cycles, capacities = cycles[order], capacities[order]

    valid = np.isfinite(capacities) & (capacities > 0)
    cycles, capacities = cycles[valid], capacities[valid]
    n = len(cycles)

    if n == 0:
        empty = KneeResult("none", None, False, "no complete cycles")
        return KneeAnalysis(empty, [empty], reference_cycle or 0, None, 0)

    reference_note: str | None = None
    reference_index = 0
    if reference_cycle is not None:
        integer_cycles = cycles.astype(int)
        matches = np.flatnonzero(integer_cycles == reference_cycle)
        if len(matches):
            reference_index = int(matches[0])
        else:
            # The requested cycle carried no usable capacity (NaN, or zero), and
            # index 0 would quietly make a formation cycle the baseline -- every
            # retention then measured against an inflated denominator.  Mirror
            # health.py: the earliest surviving cycle at or after the request.
            position = int(np.searchsorted(integer_cycles, reference_cycle))
            reference_index = position if position < n else 0
            reference_note = (
                f"cycle {reference_cycle} has no usable capacity; "
                f"using cycle {int(cycles[reference_index])} as the reference"
            )
    reference_capacity = float(capacities[reference_index])
    retention = 100.0 * capacities / reference_capacity

    # Degradation is measured from the reference cycle onwards; anything
    # before it is formation and belongs to a different physical process.
    search_cycles = cycles[reference_index:]
    search_retention = retention[reference_index:]
    search_n = len(search_cycles)
    smoothed = smooth_series(search_retention, smoothing_window)

    results = [
        _threshold_knee(search_cycles, search_retention, threshold_pct),
        _segmented_knee(search_cycles, smoothed),
        _slope_ratio_knee(search_cycles, smoothed, factor=slope_factor,
                          baseline_window=min(baseline_window, max(search_n // 3, 2)),
                          window=min(slope_window, max(search_n // 3, 2))),
        _curvature_knee(search_cycles, search_retention, smoothing_window),
    ]

    # Preference order: the acceleration-based criteria answer the question the
    # operator is actually asking; the threshold is a fallback that always has
    # an answer once the cell is old enough.
    primary = next(
        (r for name in ("segmented", "slope_ratio", "threshold", "curvature")
         for r in results if r.method == name and r.detected),
        results[1],
    )

    analysis = KneeAnalysis(
        primary=primary,
        results=results,
        reference_cycle=int(cycles[reference_index]),
        reference_capacity_mah=reference_capacity,
        n_points=n,
        search_start_cycle=int(search_cycles[0]) if search_n else 0,
        reference_note=reference_note,
    )

    early = min(max(search_n // 4, 3), search_n)
    if search_n >= 4:
        analysis.fade_rate_early_pct_per_cycle = _linear_fit(
            search_cycles[:early], search_retention[:early])[0]
        analysis.fade_rate_late_pct_per_cycle = _linear_fit(
            search_cycles[-early:], search_retention[-early:])[0]

        late_slope = analysis.fade_rate_late_pct_per_cycle
        if late_slope and late_slope < -MIN_FADE_RATE and search_retention[-1] > threshold_pct:
            analysis.projected_cycle_at_80pct = float(
                search_cycles[-1] + (threshold_pct - search_retention[-1]) / late_slope
            )
    return analysis
