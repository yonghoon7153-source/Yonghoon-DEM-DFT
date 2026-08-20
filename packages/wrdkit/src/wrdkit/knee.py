"""Find where a capacity-fade curve bends -- the "knee".

There is no single accepted definition of a knee, so this module implements
four defensible criteria and reports all of them rather than hiding the
choice.  They answer subtly different questions:

``threshold``    when did the cell cross an end-of-life line (e.g. 80 %)?
                 Unambiguous, but says nothing about *acceleration*.
``segmented``    where do two straight lines fit the curve best?  This is the
                 continuous piecewise-linear regression that the Bacon-Watts
                 knee model approximates, solved exactly by scanning every
                 candidate break point.  When two lines say the fade *slowed*
                 at their best break -- what a cell that collapses and then
                 eases off looks like to a model with one bend in it -- a
                 three-line fit is asked instead and the first break reported.
``slope_ratio``  at which cycle does the local fade rate first exceed the
                 early-life rate by a factor k?  Closest to what an operator
                 means by "it started dropping here".
``curvature``    where is the geometric curvature of the smoothed curve
                 greatest?  Sensitive to noise, useful as a cross-check, and
                 never the primary answer for that reason.

A knee is only reported when the fade actually accelerates; a cell fading
linearly gets ``None`` and a stated reason instead of a spurious cycle
number.  Three things have to hold, and each rejected real cells before it
was there: the fade must steepen by ``MIN_SLOPE_RATIO``; the cell must
actually lose ``MIN_KNEE_DROP_PCT`` after the break, because a ratio of two
near-zero slopes is arithmetic and not degradation; and a line bent at the
proposed cycle must fit better than a straight one, which is what stops a
window that wobbled or the sharpest ripple on a straight line from being
reported as a knee.

The numbers in those tests are calibrated in ``tests/test_knee.py``, against
archetype curves with a planted knee and 200 straight-line fades of random
length, rate and noise.  Before the calibration the criteria found a knee in
17 % (``slope_ratio``) and 10 % (``curvature``) of curves that had none; now
none of them do, and every planted knee is still found.
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
# Layered on purpose.  ``_bend_gain`` below turned out to catch, on its own,
# every straight-line fade that the guards above it were written for -- so on
# the 400-curve sweep in the tests they are redundant.  They stay because each
# is right in its own terms (a slope through three points is not a slope; a
# first-window baseline can have the wrong sign) and because each says
# something true and specific in its reason line, which "a bent line fits no
# better" does not.  Only ``MIN_KNEE_DROP_PCT`` still decides a case alone.

#: A knee has to cost something.  Past the break point the cell must actually
#: lose this much retention, in percentage points, over the cycles that were
#: recorded.  Without it the ratio test compares two near-zero slopes and calls
#: a healthy cell degraded: a measured 5.55x steepening of -0.021 -> -0.116
#: %/cycle is 0.5 % lost over the rest of the run, which is nothing.  A span
#: rather than a rate, so a slow cell watched for 500 cycles still qualifies.
MIN_KNEE_DROP_PCT = 2.0
#: How much better the bent model has to fit than a single straight line,
#: as an F-like ratio of the residual it removes to the residual it leaves.
#: This is a screen, not a significance test -- the series is median-smoothed,
#: so its residuals are correlated and no p-value would be honest.
#:
#: Calibrated by measurement, not taste.  On 400 straight-line fades with
#: random length, rate and noise, plus the archetype curves in
#: ``tests/test_knee.py``: every planted knee scored above 1500, and the
#: highest-scoring curve with no knee reached 63.  A gate at 50 let nine of
#: those through; 100 lets none, and still leaves a 15x margin below the
#: weakest real knee.
MIN_FIT_GAIN_F = 100.0
#: A window slope wobbles on its own.  Where early life is a straight line that
#: wobble is the measurement noise, so the slope-ratio limit is lowered by this
#: many robust standard deviations of it.  Without the allowance a 1.6-sigma
#: excursion at cycle 24 was reported as the knee of a cell that bends at 40.
SLOPE_NOISE_SIGMAS = 2.0
#: The local rate must stay past the limit for this many consecutive windows.
#: One window is a glitch; two overlapping ones mean the curve moved.
SUSTAINED_WINDOWS = 2
#: Break-point candidates tried per axis when the two-line model is escalated
#: to three.  The scan is quadratic, so the grid is thinned on a long record:
#: 32 x 32 is at most ~500 fits, and a knee is never located to better than a
#: cycle or two anyway.
THREE_SEGMENT_GRID = 32


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


def _hinge_fit(cycles: np.ndarray, values: np.ndarray,
               breaks: tuple[float, ...]) -> tuple[float, list[float]]:
    """Continuous piecewise-linear fit at fixed break points.

    Returns the residual sum of squares and the slope of each segment.  The
    basis is ``1, x, max(x - t1, 0), max(x - t2, 0) ...``, so the pieces join
    by construction -- a capacity curve does not jump.
    """
    columns = [np.ones(len(cycles)), cycles]
    columns += [np.maximum(cycles - t, 0.0) for t in breaks]
    design = np.column_stack(columns)
    coefficients, *_ = np.linalg.lstsq(design, values, rcond=None)
    residual = values - design @ coefficients
    slopes = np.cumsum(coefficients[1:]).tolist()
    return float(np.sum(residual ** 2)), [float(s) for s in slopes]


def _acceleration(slope_before: float, slope_after: float) -> float:
    """How much steeper the fade got, as a ratio.

    ``inf`` when the earlier segment is flat or rising: the guards leave
    ``slope_after`` fading, so fade *begins* at the break -- activation then
    collapse, common in all-solid-state cells.  Dividing would give a negative
    ratio and reject the clearest knee shape there is.
    """
    if slope_after > -MIN_FADE_RATE:
        return 0.0
    if slope_before >= -MIN_FADE_RATE:
        return float("inf")
    return slope_after / slope_before


def _f_gain(rss_single: float, rss_model: float, n: int, extra: int) -> float:
    """How much residual the bent model removes, per residual it leaves."""
    if rss_model <= 0:
        return float("inf")
    return ((rss_single - rss_model) / extra) / (rss_model / max(n - 2 - extra, 1))


def _bend_gain(cycles: np.ndarray, values: np.ndarray, breakpoint: float) -> float:
    """Does a bend *here* explain the curve better than no bend at all?

    The three acceleration criteria propose a cycle in three different ways, and
    all three can be talked into proposing one by noise: a window slope that
    wobbled, a curvature peak that is the sharpest ripple on a straight line.
    Whatever the route, the claim is the same -- the curve bends here -- so the
    same question settles it, and the fit is one line of algebra either way.
    """
    single = _linear_fit(cycles, values)[2]
    rss, _ = _hinge_fit(cycles, values, (breakpoint,))
    gain = _f_gain(single, rss, len(cycles), 1)
    if gain >= MIN_FIT_GAIN_F:
        return gain

    # A cell that collapses and then eases off is not two lines, and asking it
    # to be rejected the very bend it plainly has -- the criteria that found
    # cycle 23 on the lab's own 4.6 V cell both went silent.  Let the curve keep
    # a second break *after* the proposed one: that break describes what the
    # cell did afterwards, not where it bent, so the claim under test is
    # unchanged and only the nuisance is fitted.
    n = len(cycles)
    after = np.flatnonzero(cycles > breakpoint)
    if len(after) < 2 * MIN_SEGMENT:
        return gain
    best = None
    for j in _grid(range(int(after[0]) + MIN_SEGMENT, n - MIN_SEGMENT),
                   THREE_SEGMENT_GRID):
        rss2, _ = _hinge_fit(cycles, values, (breakpoint, float(cycles[j])))
        if best is None or rss2 < best:
            best = rss2
    if best is None:
        return gain
    return max(gain, _f_gain(single, best, n, 2))


def _grid(candidates: range | list[int], size: int) -> list[int]:
    """Thin a candidate list to at most *size* evenly spaced entries."""
    items = list(candidates)
    if len(items) <= size:
        return items
    return [items[round(k * (len(items) - 1) / (size - 1))] for k in range(size)]


def _three_segment(cycles: np.ndarray, values: np.ndarray,
                   rss_single: float) -> KneeResult:
    """Flat, then steep, then easing off -- what two lines cannot describe.

    This is the shape of a high-voltage or all-solid-state cell that sheds
    capacity over a few cycles and then settles into a slower fade.  The best
    two-line break lands in the *easing* part, where the fade is slower than
    before it, so the two-line criterion correctly reports no acceleration and
    the operator is told nothing about the bend they can plainly see.  A third
    segment lets the model hold the collapse and the recovery apart; the knee
    is the first break, and the second is reported with it so the reason says
    what the cell did afterwards.
    """
    n = len(cycles)
    if n < 3 * MIN_SEGMENT + 1:
        return KneeResult("segmented", None, False,
                          f"a three-line fit needs at least {3 * MIN_SEGMENT + 1} "
                          f"cycles, has {n}")

    best = None
    for i in _grid(range(MIN_SEGMENT, n - 2 * MIN_SEGMENT), THREE_SEGMENT_GRID):
        for j in _grid(range(i + MIN_SEGMENT, n - MIN_SEGMENT), THREE_SEGMENT_GRID):
            rss, slopes = _hinge_fit(cycles, values,
                                     (float(cycles[i]), float(cycles[j])))
            if best is None or rss < best[0]:
                best = (rss, float(cycles[i]), float(cycles[j]), slopes)
    if best is None:                                    # pragma: no cover - n guard
        return KneeResult("segmented", None, False, "no three-line break point fits")

    rss, first, second, slopes = best
    ratio = _acceleration(slopes[0], slopes[1])
    fade = _linear_fit(cycles[cycles >= first], values[cycles >= first])[0]
    drop = float(values[cycles >= first][0] - values[-1])
    gain = _f_gain(rss_single, rss, n, 2)
    detail = {"breakpoint": first, "second_breakpoint": second,
              "slope_before": slopes[0], "slope_after": slopes[1],
              "slope_late": slopes[2], "slope_ratio": float(ratio),
              "drop_after_pct": drop, "f_statistic": gain, "segments": 3.0}

    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("segmented", None, False,
                          "neither of the two best break points accelerates the fade",
                          detail)
    if drop < MIN_KNEE_DROP_PCT:
        return KneeResult("segmented", None, False,
                          f"only {drop:.1f}% is lost after cycle {first:.0f} "
                          f"(needs {MIN_KNEE_DROP_PCT:g}%)", detail)
    if gain < MIN_FIT_GAIN_F:
        return KneeResult("segmented", None, False,
                          "a bent line fits no better than a straight one", detail)
    del fade
    return KneeResult(
        "segmented", first, True,
        f"fade steepens at cycle {first:.0f} "
        f"({slopes[0]:.3f} -> {slopes[1]:.3f} %/cycle) and eases off again "
        f"from cycle {second:.0f} ({slopes[2]:.3f} %/cycle)",
        detail,
    )


def _segmented_knee(cycles: np.ndarray, values: np.ndarray) -> KneeResult:
    """Exact continuous two-segment regression by scanning break points."""
    n = len(cycles)
    if n < 2 * MIN_SEGMENT + 1:
        return KneeResult("segmented", None, False,
                          f"needs at least {2 * MIN_SEGMENT + 1} cycles, has {n}")

    single_slope, _, rss_single = _linear_fit(cycles, values)
    del single_slope

    best = None
    for split in range(MIN_SEGMENT, n - MIN_SEGMENT):
        breakpoint = float(cycles[split])
        rss, slopes = _hinge_fit(cycles, values, (breakpoint,))
        if best is None or rss < best[0]:
            best = (rss, breakpoint, slopes)

    rss, breakpoint, slopes = best
    slope_before, slope_after = slopes
    drop = float(values[cycles >= breakpoint][0] - values[-1])
    gain = _f_gain(rss_single, rss, n, 1)

    detail = {
        "breakpoint": breakpoint,
        "slope_before": slope_before,
        "slope_after": slope_after,
        "rss_segmented": rss,
        "rss_single_line": rss_single,
        "drop_after_pct": drop,
        "f_statistic": gain,
        "segments": 2.0,
    }

    if slope_before > -MIN_FADE_RATE and slope_after > -MIN_FADE_RATE:
        return KneeResult("segmented", None, False, "capacity is not fading", detail)
    if slope_after >= slope_before:
        # The best two-line break says the fade *slowed* there.  That is the
        # honest answer for a cell that is easing off -- and also what a
        # flat-then-collapse-then-ease curve looks like to a model with only
        # one bend in it.  Ask a three-line model before giving up.
        escalated = _three_segment(cycles, values, rss_single)
        if escalated.detected:
            return escalated
        merged = dict(detail)
        merged.update(escalated.detail)
        return KneeResult("segmented", None, False,
                          "fade does not accelerate after the best break point",
                          merged)

    ratio = _acceleration(slope_before, slope_after)
    detail["slope_ratio"] = float(ratio)
    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("segmented", None, False,
                          f"fade accelerates only {ratio:.2f}x "
                          f"(needs {MIN_SLOPE_RATIO:g}x)", detail)
    if drop < MIN_KNEE_DROP_PCT:
        # A ratio of two near-zero slopes is arithmetic, not degradation.
        return KneeResult("segmented", None, False,
                          f"only {drop:.1f}% is lost after cycle {breakpoint:.0f} "
                          f"(needs {MIN_KNEE_DROP_PCT:g}%)", detail)
    if gain < MIN_FIT_GAIN_F:
        return KneeResult("segmented", None, False,
                          "a bent line fits no better than a straight one", detail)

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


def _slope_noise(local: np.ndarray, window: int) -> float:
    """How much a window slope wobbles on its own.

    Two wrong ways to measure this, both tried:

    The spread of the *early* window slopes underestimates it whenever early
    life happens to be quiet, and the limit it sets is then reached by ordinary
    scatter further along -- 17 % of 400 straight-line fades were handed a knee.

    Successive differences of *every* window are worse still: neighbouring
    windows share all but one point, so they barely disagree, and the noise
    comes out near zero.

    What works is successive differences of *non-overlapping* windows, which
    share no points and so disagree by the full measurement noise.  Differences
    rather than a spread because a real knee changes the slope once: it adds a
    single large step that a median ignores, while it would inflate a spread.
    """
    apart = local[::max(window, 1)]
    if len(apart) < 4:
        # Too short to have independent windows; fall back to the spread, which
        # is at worst conservative on a series this short.
        centre = float(np.median(local))
        return 1.4826 * float(np.median(np.abs(local - centre)))
    return float(1.4826 * np.median(np.abs(np.diff(apart))) / np.sqrt(2.0))


def _slope_ratio_knee(cycles: np.ndarray, values: np.ndarray, *,
                      factor: float, baseline_window: int,
                      window: int) -> KneeResult:
    """Where the local fade rate leaves the early-life rate and stays away.

    Three things this has to survive, all of them found by measurement:

    *A five-point fit on a flat curve measures noise, not fade.*  On one
    archetype it came out at +0.181 %/cycle -- the wrong sign -- and every
    later window then "exceeded" it.  The baseline is the *median* of the
    early window slopes instead, which a single wobble cannot move.

    *A window slope wobbles even where the curve is straight.*  Two times a
    baseline of -0.115 %/cycle is -0.23, and a 1.6-sigma window at cycle 24
    reached it on a cell that bends at 40.  Where early life is a straight
    line the spread of those window slopes *is* the noise, so the limit is
    lowered by ``SLOPE_NOISE_SIGMAS`` robust standard deviations of it.

    *One steep window is a glitch.*  The rate has to stay past the limit for
    ``SUSTAINED_WINDOWS`` of them.
    """
    n = len(cycles)
    if n < baseline_window + window + 1:
        return KneeResult("slope_ratio", None, False,
                          f"needs at least {baseline_window + window + 1} cycles, has {n}")

    starts = range(0, n - window + 1)
    local = np.array([_linear_fit(cycles[s:s + window], values[s:s + window])[0]
                      for s in starts])
    early = max(1, min(len(local), baseline_window))
    baseline = float(np.median(local[:early]))
    spread = _slope_noise(local, window)

    detail = {"baseline_slope": baseline, "factor": factor,
              "baseline_window": float(baseline_window),
              "slope_noise": spread}
    if baseline <= -MIN_FADE_RATE:
        limit = baseline * factor - SLOPE_NOISE_SIGMAS * spread
    else:
        # Flat or rising early life gives no rate to multiply.  Look for where
        # fade *starts* instead, and let the loss gate decide whether it counts.
        limit = -MIN_FADE_RATE - SLOPE_NOISE_SIGMAS * spread
        detail["baseline_source"] = 1.0
    detail["slope_limit"] = float(limit)

    below = local <= limit
    for k in range(early, len(local) - SUSTAINED_WINDOWS + 1):
        if not bool(below[k:k + SUSTAINED_WINDOWS].all()):
            continue
        # The window is evidence about its middle, not about its first cycle:
        # reporting the start put the knee up to a whole window early.
        index = min(k + window // 2, n - 1)
        cycle = float(cycles[index])
        drop = float(values[k] - values[-1])
        detail["slope_at_knee"] = float(local[k])
        detail["drop_after_pct"] = drop
        if drop < MIN_KNEE_DROP_PCT:
            return KneeResult("slope_ratio", None, False,
                              f"the rate does steepen, but only {drop:.1f}% is lost "
                              f"afterwards (needs {MIN_KNEE_DROP_PCT:g}%)", detail)
        gain = _bend_gain(cycles, values, cycle)
        detail["f_statistic"] = gain
        if gain < MIN_FIT_GAIN_F:
            return KneeResult("slope_ratio", None, False,
                              f"the rate steepens around cycle {cycle:.0f}, but a "
                              f"line bent there fits no better than a straight one",
                              detail)
        return KneeResult(
            "slope_ratio", cycle, True,
            f"fade rate reached {factor:g}x the early-life rate "
            f"({local[k]:.3f} vs {baseline:.3f} %/cycle) at cycle {cycle:.0f}",
            detail,
        )
    return KneeResult("slope_ratio", None, False,
                      f"fade rate never stayed at {factor:g}x the early-life rate",
                      detail)


def _curvature_knee(cycles: np.ndarray, values: np.ndarray, window: int) -> KneeResult:
    n = len(cycles)
    if n < 7:
        return KneeResult("curvature", None, False, f"needs at least 7 cycles, has {n}")
    smoothed = smooth_series(values, window)
    first = np.gradient(smoothed, cycles)
    second = np.gradient(first, cycles)
    curvature = np.abs(second) / np.power(1.0 + first ** 2, 1.5)
    # Ignore the edges, where gradient's one-sided differences dominate.
    # A slope fitted through three points is noise, not a slope: with a
    # two-point margin the peak landed at cycle 5 and the "early life" it
    # was compared against was three cycles long.
    margin = max(2, window // 2)
    interior = curvature[margin:n - margin]
    if not len(interior):
        return KneeResult("curvature", None, False, "series too short after edge trimming")
    index = margin + int(np.argmax(interior))
    cycle = float(cycles[index])
    slope_before, _, _ = _linear_fit(cycles[:index + 1], smoothed[:index + 1])
    slope_after, _, _ = _linear_fit(cycles[index:], smoothed[index:])
    drop = float(smoothed[index] - smoothed[-1])
    detail = {"curvature": float(curvature[index]),
              "median_curvature": float(np.median(interior)),
              "slope_before": slope_before, "slope_after": slope_after,
              "drop_after_pct": drop}
    # An argmax always exists, so without these guards the criterion the other
    # three fall back to hands a healthy cell a knee cycle -- the largest
    # rounding ripple on a flat line, or the kink a single glitch leaves behind.
    if slope_before > -MIN_FADE_RATE and slope_after > -MIN_FADE_RATE:
        return KneeResult("curvature", None, False, "capacity is not fading", detail)
    ratio = _acceleration(slope_before, slope_after)
    detail["slope_ratio"] = float(ratio)
    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("curvature", None, False,
                          f"curvature peaks at cycle {cycle:.0f} but fade "
                          f"accelerates only {ratio:.2f}x there "
                          f"(needs {MIN_SLOPE_RATIO:g}x)", detail)
    if drop < MIN_KNEE_DROP_PCT:
        # Curvature is scale-free: the sharpest bend on a curve that never
        # goes anywhere is still the sharpest bend.  A cell that loses 0.5 %
        # after its "knee" did not have one.
        return KneeResult("curvature", None, False,
                          f"curvature peaks at cycle {cycle:.0f} but only "
                          f"{drop:.1f}% is lost afterwards "
                          f"(needs {MIN_KNEE_DROP_PCT:g}%)", detail)
    gain = _bend_gain(cycles, smoothed, cycle)
    detail["f_statistic"] = gain
    if gain < MIN_FIT_GAIN_F:
        return KneeResult("curvature", None, False,
                          f"curvature peaks at cycle {cycle:.0f}, but a line "
                          f"bent there fits no better than a straight one", detail)
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
                          baseline_window=max(baseline_window, search_n // 4),
                          window=min(slope_window, max(search_n // 3, 2))),
        _curvature_knee(search_cycles, search_retention, smoothing_window),
    ]

    # Preference order among the criteria that answer "did the fade
    # accelerate".  ``threshold`` is deliberately not in it: crossing 80 % is
    # end of life, not a knee, and it always has an answer once a cell is old
    # enough -- so it used to hand a "capacity collapse at cycle 74" to a cell
    # fading in a perfectly straight line.  When nothing accelerates, the
    # primary answer is the two-line criterion's None and its reason.
    #
    # ``curvature`` is not in it either.  An argmax always exists and the
    # sharpest ripple on a straight line is still the sharpest ripple: on 400
    # straight-line fades it claimed a knee 40 times where the two-line fit
    # claimed none.  It stays in the panel as the cross-check the docstring
    # says it is, and never speaks for the cell on its own.
    primary = next(
        (r for name in ("segmented", "slope_ratio")
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
