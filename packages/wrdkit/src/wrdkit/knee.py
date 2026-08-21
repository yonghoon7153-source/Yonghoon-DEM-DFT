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

from dataclasses import dataclass, field, replace

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


#: ``KneeResult.status`` values.
#:
#: ``detected``       a knee, and the record shows what it cost.
#: ``insufficient``   a break point that fits, but the record ends before the
#:                    evidence to confirm it exists.  NOT the same as "no knee":
#:                    reading it as one makes a cell that was unplugged early
#:                    look as healthy as a cell that never bent, and biases any
#:                    comparison between cells watched for different lengths.
#: ``none``           nothing bends.
#: ``indeterminate``  cannot be judged at all -- no usable cycle at or after the
#:                    reference, so there is no baseline to measure against.
STATUS_DETECTED = "detected"
STATUS_INSUFFICIENT = "insufficient"
STATUS_NONE = "none"
STATUS_INDETERMINATE = "indeterminate"


@dataclass
class KneeResult:
    """One criterion's answer."""

    method: str
    cycle: float | None
    detected: bool
    reason: str = ""
    detail: dict[str, float] = field(default_factory=dict)
    #: Which of the four outcomes above this is.
    status: str = ""
    #: The cycle this criterion is pointing at, confirmed or not.  ``cycle`` is
    #: None unless the knee is confirmed; this one survives so a screen can show
    #: "cycle 12, not yet confirmed" instead of a dash.
    candidate_cycle: float | None = None

    def __post_init__(self) -> None:
        if not self.status:
            self.status = STATUS_DETECTED if self.detected else STATUS_NONE
        if self.candidate_cycle is None:
            self.candidate_cycle = self.cycle


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


def _not_yet(method: str, breakpoint: float, drop: float,
             cycles: np.ndarray, detail: dict) -> KneeResult:
    """The curve bends here, but the record has not shown what it costs.

    Two very different cells reach this line.  One bent and then held: the fade
    after the break is real but tiny, and it is not a knee.  The other bent two
    cycles before somebody unplugged it, and would have lost 40 % if it had
    kept going.  Told apart by how much record is left after the break: with
    only a handful of cycles to look at, "less than 2 % lost" is a statement
    about the length of the file, not about the cell.

    Reporting both as "no knee" made the answer depend on when the operator
    stopped.  The same cell, cut at cycle 17 and at cycle 19, gave None and
    cycle 12.  So the short case is ``insufficient``: a candidate, and a reason
    that says the evidence is not in yet.
    """
    after = cycles[cycles > breakpoint]
    followup = int(len(after))
    detail = dict(detail)
    detail["followup_cycles"] = float(followup)
    # "Not yet" is a claim that something bent -- only the consequence is
    # missing.  Without that, a straight line whose noise happened to fit a
    # hinge gets deferred instead of dismissed, and 5 % of pure straight-line
    # fades came back as "cycle N, not confirmed".  No structural support, no
    # deferral.
    if float(detail.get("f_statistic", 0.0)) < MIN_FIT_GAIN_F:
        return KneeResult(
            method, None, False,
            f"only {drop:.1f}% is lost after cycle {breakpoint:.0f} "
            f"(needs {MIN_KNEE_DROP_PCT:g}%), and a line bent there fits no "
            f"better than a straight one",
            detail, candidate_cycle=float(breakpoint),
        )
    # Enough room to have lost 2 % at the *slowest* rate this module still
    # calls fading?  No -- that would be millions of cycles.  The question is
    # whether the fade actually measured after the break had room to add up,
    # so ask this cell's own post-break rate.
    rate = abs(float(detail.get("slope_after") or 0.0))
    needed = MIN_KNEE_DROP_PCT / rate if rate > MIN_FADE_RATE else float("inf")
    detail["cycles_needed_for_loss"] = needed if np.isfinite(needed) else -1.0
    # "Not yet" only while more of the same record would settle it.  Any fade
    # at all reaches 2 % eventually, so "it would get there in 658 more cycles"
    # is not censoring -- 299 cycles of follow-up measured that rate perfectly
    # well, and the answer is that the bend cost nothing.  Within a doubling of
    # what has already been watched, the operator's stopping point really is
    # what decided the answer.
    if followup < needed <= 2 * followup:
        return KneeResult(
            method, None, False,
            f"cycle {breakpoint:.0f} bends, but only {followup} cycles follow it and "
            f"{drop:.1f}% has been lost so far -- at this rate the {MIN_KNEE_DROP_PCT:g}% "
            f"that makes it a knee needs about {needed:.0f}",
            detail, status=STATUS_INSUFFICIENT, candidate_cycle=float(breakpoint),
        )
    return KneeResult(
        method, None, False,
        f"only {drop:.1f}% is lost after cycle {breakpoint:.0f} "
        f"(needs {MIN_KNEE_DROP_PCT:g}%)",
        detail, candidate_cycle=float(breakpoint),
    )


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
    # `under[c:c + 2].all()` is True for the final sample too -- the slice is
    # one long and numpy calls that "all below".  One reading at the end of a
    # record is exactly the glitch this guard exists to reject.
    sustained = [c for c in below
                 if c + SUSTAINED_CROSSING <= len(under)
                 and bool(under[c:c + SUSTAINED_CROSSING].all())]
    if not sustained:
        first = float(cycles[int(below[0])])
        shared = {"level": level, "min_retention": float(retention.min()),
                  "first_cycle_below": first}
        if int(below[-1]) + SUSTAINED_CROSSING > len(under):
            # The crossing is the last thing in the record.  It did not
            # recover -- nothing came after it to recover in.  Saying
            # "recovered" here was a statement about data that does not exist.
            return KneeResult("threshold", None, False,
                              f"fell below {level:g}% at cycle {first:.0f}, the last "
                              f"cycle in the record -- nothing follows to confirm it",
                              shared, status=STATUS_INSUFFICIENT, candidate_cycle=first)
        return KneeResult("threshold", None, False,
                          f"dipped below {level:g}% at cycle {first:.0f} but recovered",
                          shared)
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

    ``inf`` is a fine answer inside this module and a terrible one to put in
    ``detail``: a report carrying it serialises to a bare ``Infinity``, which
    ``json.dumps(allow_nan=False)`` and every standards-compliant client
    reject -- so a correctly detected knee returned a 500.  ``_record_ratio``
    is what writes it down.
    """
    if slope_after > -MIN_FADE_RATE:
        return 0.0
    if slope_before >= -MIN_FADE_RATE:
        return float("inf")
    return slope_after / slope_before


def _record_ratio(detail: dict, ratio: float) -> None:
    """Put an acceleration ratio into ``detail`` in a form JSON can carry.

    A fade that *begins* at the break has no finite ratio.  That is a fact
    about the cell, so it goes in as a flag rather than a float nobody can
    encode.
    """
    if np.isfinite(ratio):
        detail["slope_ratio"] = float(ratio)
        detail["fade_starts_here"] = 0.0
    else:
        detail.pop("slope_ratio", None)
        detail["fade_starts_here"] = 1.0


def _f_gain(rss_single: float, rss_model: float, n: int, extra: int) -> float:
    """How much residual the bent model removes, per residual it leaves."""
    if rss_model <= 0:
        return float("inf")
    return ((rss_single - rss_model) / extra) / (rss_model / max(n - 2 - extra, 1))


def _bend_gain(cycles: np.ndarray, values: np.ndarray, breakpoint: float) -> float:
    """Does a bend *here* explain the curve better than no bend here?

    The three acceleration criteria propose a cycle in three different ways,
    and all three can be talked into proposing one by noise: a window slope
    that wobbled, a curvature peak that is the sharpest ripple on a straight
    line.  Whatever the route, the claim is the same -- the curve bends here --
    so the same question settles it.

    A cell that collapses and then eases off is not two lines, so a second free
    break is allowed after the proposed one to describe what happened
    afterwards.  That nuisance break has to be a nuisance, not a witness: the
    first version compared a straight line against the *pair*, which let a real
    knee at cycle 80 certify any transient the noise put at cycle 34 -- gain
    66 against the straight line, 34,877 once cycle 79 was allowed in beside
    it, on a curve whose first "break" was a deceleration.

    So the second break is fitted under both hypotheses and only the candidate's
    own contribution is scored: how much residual does adding *this* cycle
    remove from a model that already has the later break in it.
    """
    n = len(cycles)
    single = _linear_fit(cycles, values)[2]
    alone, _ = _hinge_fit(cycles, values, (breakpoint,))
    gain = _f_gain(single, alone, n, 1)
    if gain >= MIN_FIT_GAIN_F:
        return gain

    after = np.flatnonzero(cycles > breakpoint)
    if not len(after) or len(after) < 2 * MIN_SEGMENT:
        return gain
    best = None
    for j in range(int(after[0]) + MIN_SEGMENT, n - MIN_SEGMENT):
        with_both, _ = _hinge_fit(cycles, values, (breakpoint, float(cycles[j])))
        without, _ = _hinge_fit(cycles, values, (float(cycles[j]),))
        # The nuisance break is chosen to help the *candidate*, so it is picked
        # on the incremental gain rather than on the joint fit -- otherwise the
        # best pair is simply the best two-break model, whoever it belongs to.
        incremental = _f_gain(without, with_both, n, 1)
        if best is None or incremental > best:
            best = incremental
    return max(gain, best if best is not None else gain)


def _suffix_sums(x: np.ndarray, y: np.ndarray) -> dict[str, np.ndarray]:
    """Suffix sums of everything a hinge fit needs, one pass.

    ``s[k]`` is the sum over points ``k..n-1``, with a trailing zero so that
    ``s[n]`` is the empty sum.  A hinge column ``(x - t)+`` is zero up to ``t``
    and linear after, so every entry of the normal equations is a polynomial in
    ``t`` with these as coefficients -- which turns one fit from O(n) into O(1)
    and an exhaustive two-break scan from unaffordable into a second.
    """
    def suffix(values):
        out = np.zeros(len(values) + 1)
        out[:-1] = np.cumsum(values[::-1])[::-1]
        return out

    return {"n": suffix(np.ones_like(x)), "x": suffix(x), "xx": suffix(x * x),
            "y": suffix(y), "xy": suffix(x * y)}


def _exact_three_break(cycles: np.ndarray, values: np.ndarray):
    """The best two break points, every pair tried, no grid.

    A thinned grid was tried first and had to go.  Thirty-two candidates per
    axis on a 1,000-cycle record puts the first break at cycles 7, 39, 71 ...,
    so a cell that crashed between cycle 10 and 25 was fitted at 27/31 -- and
    the second "transition" of that wrong fit passed every gate, which is worse
    than the miss it replaced.  Refining the best few grid pairs did not rescue
    it either: the residual surface has one basin and every start walked into
    it.

    Breaks are placed at the observed cycles, and ``x`` is centred so the
    quartic terms in the normal equations stay conditioned.
    """
    n = len(cycles)
    lowest, highest = MIN_SEGMENT, n - MIN_SEGMENT - 1
    if highest - lowest < MIN_SEGMENT:
        return None

    centre = float(np.mean(cycles))
    x = cycles - centre
    y = np.asarray(values, dtype=np.float64)
    s = _suffix_sums(x, y)
    total_yy = float(np.sum(y * y))

    def hinge_stats(index: np.ndarray, t: np.ndarray):
        """Σu, Σxu, Σu², Σuy for u = (x - t)+ at each break index."""
        count, sx, sxx = s["n"][index], s["x"][index], s["xx"][index]
        sy, sxy = s["y"][index], s["xy"][index]
        return (sx - t * count,
                sxx - t * sx,
                sxx - 2 * t * sx + t * t * count,
                sxy - t * sy)

    all_n, all_x, all_xx = s["n"][0], s["x"][0], s["xx"][0]
    all_y, all_xy = s["y"][0], s["xy"][0]

    best = None
    for i in range(lowest, highest - MIN_SEGMENT + 1):
        js = np.arange(i + MIN_SEGMENT, highest + 1)
        if not len(js):
            continue
        t1 = x[i]
        t2 = x[js]
        u1, xu1, u1u1, u1y = hinge_stats(np.full(len(js), i), np.full(len(js), t1))
        u2, xu2, u2u2, u2y = hinge_stats(js, t2)
        # Σ(x-t1)(x-t2) over x > t2, since (x-t1)+ = (x-t1) there.
        count2, sx2, sxx2 = s["n"][js], s["x"][js], s["xx"][js]
        u1u2 = sxx2 - (t1 + t2) * sx2 + t1 * t2 * count2

        m = len(js)
        # Upper triangle of X'X for the basis [1, x, (x-t1)+, (x-t2)+], then
        # mirrored -- it is symmetric and half the entries are free.
        gram = np.empty((m, 4, 4))
        upper = {
            (0, 0): np.full(m, all_n), (0, 1): np.full(m, all_x),
            (0, 2): u1, (0, 3): u2,
            (1, 1): np.full(m, all_xx), (1, 2): xu1, (1, 3): xu2,
            (2, 2): u1u1, (2, 3): u1u2,
            (3, 3): u2u2,
        }
        for (row, col), value in upper.items():
            gram[:, row, col] = value
            gram[:, col, row] = value
        moment = np.column_stack([np.full(m, all_y), np.full(m, all_xy), u1y, u2y])

        # A ridge far below the data scale: three collinear segments make the
        # gram singular, and those pairs simply must not win.
        gram[:, range(4), range(4)] += 1e-10
        beta = np.linalg.solve(gram, moment[..., None])[..., 0]
        rss = total_yy - np.einsum("ij,ij->i", beta, moment)
        k = int(np.argmin(rss))
        if best is None or rss[k] < best[0]:
            best = (float(rss[k]), i, int(js[k]),
                    [float(beta[k, 1]), float(beta[k, 1] + beta[k, 2]),
                     float(beta[k, 1] + beta[k, 2] + beta[k, 3])])
    if best is None:
        return None
    rss, i, j, slopes = best
    # Refit at the winning pair with the same solver the rest of the module
    # uses: the normal equations found the pair, least squares reports it.
    exact, exact_slopes = _hinge_fit(cycles, values,
                                     (float(cycles[i]), float(cycles[j])))
    del slopes
    return exact, float(cycles[i]), float(cycles[j]), exact_slopes


def _exact_level_shift(cycles: np.ndarray, values: np.ndarray):
    """The best "one straight line, plus a block that sits lower" fit.

    This is the competing story for a bend.  Degradation is permanent: the
    capacity a cell has lost, it has lost.  A block of cycles that sits below
    the trend and then rejoins it is something else -- a C-rate step, a
    temperature excursion, a diagnostic sweep -- and the cell was fading at the
    same rate throughout.

    A continuous hinge cannot say that, so it approximates the block with a
    steep drop and a recovery, and reports the drop as an onset of degradation
    several cycles *before* the block even starts.  Fitting the honest model
    and comparing residuals is how the two are told apart; the design is
    ``1, x, 1[t1 <= x < t2]`` and the search is exhaustive, on the same
    suffix sums.
    """
    n = len(cycles)
    if n < 3 * MIN_SEGMENT + 1:
        return None
    centre = float(np.mean(cycles))
    x = cycles - centre
    y = np.asarray(values, dtype=np.float64)
    s = _suffix_sums(x, y)
    total_yy = float(np.sum(y * y))
    all_n, all_x, all_xx = s["n"][0], s["x"][0], s["xx"][0]
    all_y, all_xy = s["y"][0], s["xy"][0]

    best = None
    for i in range(MIN_SEGMENT, n - 2 * MIN_SEGMENT + 1):
        js = np.arange(i + MIN_SEGMENT, n - MIN_SEGMENT + 1)
        if not len(js):
            continue
        # Indicator over [i, j): window sums are differences of suffix sums.
        block_n = s["n"][i] - s["n"][js]
        block_x = s["x"][i] - s["x"][js]
        block_y = s["y"][i] - s["y"][js]

        m = len(js)
        gram = np.empty((m, 3, 3))
        upper = {
            (0, 0): np.full(m, all_n), (0, 1): np.full(m, all_x), (0, 2): block_n,
            (1, 1): np.full(m, all_xx), (1, 2): block_x,
            (2, 2): block_n,
        }
        for (row, col), value in upper.items():
            gram[:, row, col] = value
            gram[:, col, row] = value
        moment = np.column_stack([np.full(m, all_y), np.full(m, all_xy), block_y])
        gram[:, range(3), range(3)] += 1e-10
        beta = np.linalg.solve(gram, moment[..., None])[..., 0]
        rss = total_yy - np.einsum("ij,ij->i", beta, moment)
        k = int(np.argmin(rss))
        if best is None or rss[k] < best[0]:
            best = (float(rss[k]), i, int(js[k]), float(beta[k, 2]), float(beta[k, 1]))
    if best is None:
        return None
    rss, i, j, offset, slope = best
    return rss, float(cycles[i]), float(cycles[min(j, n - 1)]), offset, slope


def _protocol_excursion(cycles: np.ndarray, values: np.ndarray,
                        rss_bend: float) -> tuple[float, float, float] | None:
    """A block of cycles that sat lower and then rejoined the trend.

    Returns ``(first cycle, last cycle, offset)`` when that story fits the
    curve better than any bend does, and None otherwise.

    Degradation is permanent.  A cell that drops 4 % for twenty cycles and then
    comes back did not degrade there -- something about how it was measured
    changed and changed back, which is what a C-rate block or a temperature
    excursion inside a cycling schedule looks like.  The continuous hinge has
    no way to say that, so it spends its two break points on a steep drop and a
    recovery and reports the drop as an onset of degradation, several cycles
    before the block even begins.

    The record does not carry the schedule down here, so the shape has to
    stand in for the metadata: the block must sit *below* the line, and it must
    end before the record does.  A step that never comes back is a real
    permanent loss, whatever caused it.
    """
    shift = _exact_level_shift(cycles, values)
    if shift is None:
        return None
    rss, start, end, offset, _ = shift
    if rss >= rss_bend:
        return None
    if offset >= 0.0:
        return None
    if end >= float(cycles[-1]):
        return None
    return start, end, offset


def _three_segment(cycles: np.ndarray, values: np.ndarray,
                   rss_single: float) -> KneeResult:
    """Flat, then steep, then something else -- what two lines cannot describe.

    This is the shape of a high-voltage or all-solid-state cell that sheds
    capacity over a few cycles and then settles into a slower fade.  The best
    two-line break lands in the *easing* part, where the fade is slower than
    before it, so the two-line criterion correctly reports no acceleration and
    the operator is told nothing about the bend they can plainly see.

    Both transitions are tested, not just the first.  "The knee is the first
    break" fits crash-then-ease and nothing else: a cell that recovers and then
    collapses has its knee at the *second* break, and checking only the first
    threw away a 55x acceleration because the first transition was a recovery.
    The earliest qualifying one wins, and the reason says what came after.
    """
    n = len(cycles)
    if n < 3 * MIN_SEGMENT + 1:
        return KneeResult("segmented", None, False,
                          f"a three-line fit needs at least {3 * MIN_SEGMENT + 1} "
                          f"cycles, has {n}")

    best = _exact_three_break(cycles, values)
    if best is None:                                    # pragma: no cover - n guard
        return KneeResult("segmented", None, False, "no three-line break point fits")

    rss, first, second, slopes = best
    gain = _f_gain(rss_single, rss, n, 2)
    shared = {"breakpoint": first, "second_breakpoint": second,
              "slope_before": slopes[0], "slope_after": slopes[1],
              "slope_late": slopes[2], "f_statistic": gain, "segments": 3.0,
              "rss_bend": rss}

    # Each transition is scored by what *it* adds, not by how well the pair
    # fits.  Scoring both with the joint gain repeats the mistake the nuisance
    # break was fixed for, one level up: on a cell fading in a nearly straight
    # line, a strong first break lent its evidence to a 1.6x second transition
    # and produced a knee where the two-line model had correctly found none.
    without_second, _ = _hinge_fit(cycles, values, (first,))
    without_first, _ = _hinge_fit(cycles, values, (second,))

    # (break cycle, slope before it, slope after it, what follows, own gain)
    transitions = [
        (first, slopes[0], slopes[1], slopes[2], _f_gain(without_first, rss, n, 1)),
        (second, slopes[1], slopes[2], None, _f_gain(without_second, rss, n, 1)),
    ]
    rejected = None
    for where, before, after, then, own_gain in transitions:
        ratio = _acceleration(before, after)
        if ratio < MIN_SLOPE_RATIO:
            continue
        # A knee is fade faster than this cell has ever faded -- not merely
        # faster than the lull in front of it.  A real 161-cycle cell fades at
        # -0.280, slows to -0.158 for ninety cycles, then returns to -0.259:
        # measured against the lull that is a 1.64x "acceleration" at cycle
        # 121, and measured against the cell it is the rate it started with.
        if _acceleration(slopes[0], after) < MIN_SLOPE_RATIO:
            continue
        detail = dict(shared)
        detail["knee_transition"] = 1.0 if where == first else 2.0
        detail["slope_before"], detail["slope_after"] = before, after
        detail["f_statistic"] = min(gain, own_gain)
        _record_ratio(detail, ratio)
        drop = float(values[cycles >= where][0] - values[-1])
        detail["drop_after_pct"] = drop
        if drop < MIN_KNEE_DROP_PCT:
            rejected = rejected or _not_yet("segmented", where, drop, cycles, detail)
            continue
        if min(gain, own_gain) < MIN_FIT_GAIN_F:
            rejected = rejected or KneeResult(
                "segmented", None, False,
                "a bent line fits no better than a straight one", detail,
                candidate_cycle=float(where))
            continue
        tail = (f" and eases off again from cycle {second:.0f} ({then:.3f} %/cycle)"
                if then is not None else "")
        return KneeResult(
            "segmented", where, True,
            f"fade steepens at cycle {where:.0f} "
            f"({before:.3f} -> {after:.3f} %/cycle){tail}",
            detail,
        )
    if rejected is not None:
        return rejected
    return KneeResult("segmented", None, False,
                      "neither of the two best break points accelerates the fade",
                      shared)


def _segmented_knee(cycles: np.ndarray, values: np.ndarray) -> KneeResult:
    """Two straight lines, and three when two do not describe the curve.

    Which model is asked used to depend on *why* two lines were rejected: only
    a break that decelerated escalated.  That made model selection conditional
    on the test's own outcome, and it lost curves that are exactly three lines
    -- a 30-cycle record whose true breaks are 7 and 12 fitted as two lines
    scored 77 against a straight line and was rejected, while the three-line
    fit recovered both breaks and every slope to the third decimal.

    So both are always fitted and the better-supported one answers.  Two lines
    first, because a curve that two lines describe should not be given three.
    """
    n = len(cycles)
    if n < 2 * MIN_SEGMENT + 1:
        return KneeResult("segmented", None, False,
                          f"needs at least {2 * MIN_SEGMENT + 1} cycles, has {n}")

    rss_single = _linear_fit(cycles, values)[2]

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
        "rss_bend": rss,
    }

    two_line = _judge_two_line(cycles, values, detail, breakpoint,
                               slope_before, slope_after, drop, gain)
    if two_line.detected:
        return two_line

    escalated = _three_segment(cycles, values, rss_single)
    if escalated.detected:
        return escalated
    # Neither model found a knee.  Prefer whichever rejection actually looked at
    # a break point: "not yet confirmed" says more than "no acceleration".
    for candidate in (two_line, escalated):
        if candidate.status == STATUS_INSUFFICIENT:
            return candidate
    merged = dict(detail)
    merged.update(escalated.detail)
    two_line.detail.update({k: v for k, v in merged.items()
                            if k not in two_line.detail})
    return two_line


def _judge_two_line(cycles: np.ndarray, values: np.ndarray, detail: dict,
                    breakpoint: float, slope_before: float, slope_after: float,
                    drop: float, gain: float) -> KneeResult:
    if slope_before > -MIN_FADE_RATE and slope_after > -MIN_FADE_RATE:
        return KneeResult("segmented", None, False, "capacity is not fading", detail)
    if slope_after >= slope_before:
        return KneeResult("segmented", None, False,
                          "fade does not accelerate after the best break point",
                          detail)

    ratio = _acceleration(slope_before, slope_after)
    _record_ratio(detail, ratio)
    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("segmented", None, False,
                          f"fade accelerates only {ratio:.2f}x "
                          f"(needs {MIN_SLOPE_RATIO:g}x)", detail)
    if drop < MIN_KNEE_DROP_PCT:
        # A ratio of two near-zero slopes is arithmetic, not degradation.
        return _not_yet("segmented", breakpoint, drop, cycles, detail)
    if gain < MIN_FIT_GAIN_F:
        return KneeResult("segmented", None, False,
                          "a bent line fits no better than a straight one", detail,
                          candidate_cycle=float(breakpoint))

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
    held: KneeResult | None = None
    for k in range(early, len(local) - SUSTAINED_WINDOWS + 1):
        if not bool(below[k:k + SUSTAINED_WINDOWS].all()):
            continue
        # The window is evidence about its middle, not about its first cycle:
        # reporting the start put the knee up to a whole window early.
        index = min(k + window // 2, n - 1)
        cycle = float(cycles[index])
        # From the cycle being reported, not from the window's first sample:
        # the claim is "after this cycle you lose 2 %", so that is where it has
        # to be measured.  Measured at the window start it over-counted by up
        # to half a window and reported knees that lost 1.8 %.
        drop = float(values[index] - values[-1])
        detail["slope_at_knee"] = float(local[k])
        detail["drop_after_pct"] = drop
        # Structure first, consequence second: `_not_yet` defers only when the
        # bend itself is supported, so it has to know the fit gain already.
        gain = _bend_gain(cycles, values, cycle)
        detail["f_statistic"] = gain
        if drop < MIN_KNEE_DROP_PCT:
            # Keep looking.  Returning here proved only that the *first*
            # candidate failed, while saying "the rate never stayed" -- a cell
            # with a transient at cycle 60 and its real knee at 95 was reported
            # as having none, because the transient got asked first.
            held = held or _not_yet("slope_ratio", cycle, drop, cycles, detail)
            continue
        if gain < MIN_FIT_GAIN_F:
            held = held or KneeResult(
                "slope_ratio", None, False,
                f"the rate steepens around cycle {cycle:.0f}, but a "
                f"line bent there fits no better than a straight one",
                detail, candidate_cycle=cycle)
            continue
        return KneeResult(
            "slope_ratio", cycle, True,
            f"fade rate reached {factor:g}x the early-life rate "
            f"({local[k]:.3f} vs {baseline:.3f} %/cycle) at cycle {cycle:.0f}",
            detail,
        )
    if held is not None:
        return held
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
    margin = max(MIN_SEGMENT, window // 2)
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
    _record_ratio(detail, ratio)
    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("curvature", None, False,
                          f"curvature peaks at cycle {cycle:.0f} but fade "
                          f"accelerates only {ratio:.2f}x there "
                          f"(needs {MIN_SLOPE_RATIO:g}x)", detail)
    if drop < MIN_KNEE_DROP_PCT:
        # Curvature is scale-free: the sharpest bend on a curve that never
        # goes anywhere is still the sharpest bend.  A cell that loses 0.5 %
        # after its "knee" did not have one.
        return _not_yet("curvature", cycle, drop, cycles, detail)
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
            if position >= n:
                # Nothing at or after the requested cycle.  Falling back to
                # index 0 put the baseline on cycle 1 -- a formation cycle, the
                # one thing the reference exists to exclude (ADR 0004), and it
                # said so in a note that read like an ordinary adjustment.
                # There is no baseline here; that is the answer.
                nothing = KneeResult(
                    "none", None, False,
                    f"no usable cycle at or after cycle {reference_cycle}; "
                    f"the record ends at cycle {int(cycles[-1])}",
                    status=STATUS_INDETERMINATE,
                )
                return KneeAnalysis(nothing, [nothing], reference_cycle, None, n,
                                    reference_note=nothing.reason)
            reference_index = position
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
        # `max(baseline_window, search_n // 4)` tied the definition of "early
        # life" to how long the cell was eventually watched.  The same cell,
        # analysed at cycle 150 and again at cycle 500, moved its baseline from
        # 37 cycles to 124 -- by then the median of that window was the *late*
        # rate, and the knee it had reported at cycle 51 disappeared.  A window
        # that grows with the record is not a baseline.
        _slope_ratio_knee(search_cycles, smoothed, factor=slope_factor,
                          baseline_window=baseline_window,
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
    #
    # Among the criteria that did detect, method order decides only while they
    # agree.  A knee is when accelerated fade *started*, so when they point to
    # genuinely different events the earliest one is the knee: on a cell that
    # bends at 50 and collapses again at 150, the method order reported 147 and
    # called that the knee, while the criterion that had found cycle 51 was
    # simply further down the list.
    #
    # "Genuinely different" is more than a smoothing window apart.  Inside one,
    # the criteria are measuring the same bend and swapping to whichever landed
    # a cycle earlier would make the reported method jump around on noise.
    # Before anything is called a knee: was the curve a straight line with a
    # block of cycles that sat lower and then came back?  One fit answers it
    # for every criterion at once, because it is a statement about the curve
    # rather than about how any one of them looked at it.
    bend_rss = next((r.detail.get("rss_bend") for r in results
                     if r.method == "segmented" and "rss_bend" in r.detail), None)
    if bend_rss is not None and any(r.detected for r in results
                                    if r.method != "threshold"):
        excursion = _protocol_excursion(search_cycles, smoothed, float(bend_rss))
        if excursion is not None:
            start, end, offset = excursion
            reason = (f"cycles {start:.0f}-{end:.0f} sat {abs(offset):.1f}% below the "
                      f"trend and rejoined it -- a change in how the cell was "
                      f"measured, not degradation")
            note = {"excursion_from": start, "excursion_to": end,
                    "excursion_offset_pct": offset}
            results = [
                r if r.method == "threshold"
                else KneeResult(r.method, None, False, reason,
                                {**r.detail, **note}, candidate_cycle=r.candidate_cycle)
                for r in results
            ]

    ranked = [r for name in ("segmented", "slope_ratio")
              for r in results if r.method == name and r.detected]
    primary = ranked[0] if ranked else results[1]
    if len(ranked) > 1:
        earliest = min(r.cycle for r in ranked)
        latest = max(r.cycle for r in ranked)
        if latest - earliest > smoothing_window:
            primary = min(ranked, key=lambda r: r.cycle)
            # One number on the panel, two criteria a hundred cycles apart: the
            # disagreement is the finding, not a rounding error.
            primary = replace(
                primary,
                detail={**primary.detail, "criteria_spread_cycles": float(latest - earliest)},
                reason=(f"{primary.reason}; another criterion puts it at "
                        f"cycle {latest:.0f}"),
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
