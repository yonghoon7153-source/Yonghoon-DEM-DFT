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

__all__ = ["KneeResult", "KneeAnalysis", "dbw_confidence_interval",
           "detect_knee", "smooth_series"]

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

#: How many cycles have to follow a break before "it cost nothing" is a
#: statement about the cell rather than about the file.  Below this the
#: post-break rate is not measured well enough to dismiss the bend, so the
#: answer is `insufficient` and not `none`.
#:
#: A stated convention, not a measured constant: twenty cycles is roughly where
#: a fade rate stops being dominated by where the record happened to stop.  It
#: is the number most likely to be wrong in this module and it is deliberately
#: in one place.
MIN_FOLLOWUP_CYCLES = 20

#: How far ahead "it costs nothing" is allowed to look.  A bend whose measured
#: rate would not lose ``MIN_KNEE_DROP_PCT`` within this many further cycles is
#: dismissed; one that would is deferred until it does.  Projecting rather than
#: waiting is what keeps the answer from moving backwards as a record grows.
#:
#: A stated convention like ``MIN_FOLLOWUP_CYCLES``: 200 cycles is the far end
#: of what this lab runs, so a bend that would not matter within one is a bend
#: that does not matter.
MATERIAL_HORIZON_CYCLES = 200

#: How much of a block may be left behind and still count as "rejoined".
#: A block that recovers only half of what it lost is a permanent step with a
#: dip in front of it, and that is degradation whatever caused it.
REJOIN_TOLERANCE = 0.25
#: How deep a block has to be, in residual scales, before it is called an event
#: rather than a wobble.  Calibrated against the deepest block an exhaustive
#: two-break search can extract from a straight line -- see ``_protocol_excursion``.
EXCURSION_DEPTH_SIGMAS = 5.0

#: A knee has to cost something.  Past the break point the cell must actually
#: lose this much retention, in percentage points, over the cycles that were
#: recorded.  Without it the ratio test compares two near-zero slopes and calls
#: a healthy cell degraded: a measured 5.55x steepening of -0.021 -> -0.116
#: %/cycle is 0.5 % lost over the rest of the run, which is nothing.  A span
#: rather than a rate, so a slow cell watched for 500 cycles still qualifies.
MIN_KNEE_DROP_PCT = 2.0
#: How much better the bent model has to fit than a single straight line,
#: as a ratio of the residual it removes to the residual it leaves.  Shaped
#: like an F ratio and not one: the break point is chosen by looking at the
#: data and the series is median-smoothed first, so no tabulated distribution
#: applies and this is a screen, not a significance test.
#:
#: Calibrated by measurement.  On 400 straight-line fades with random length,
#: rate and noise, plus the archetype curves in ``tests/test_knee.py``: every
#: planted knee scored above 1500, and the highest-scoring curve with no knee
#: reached 63.  A gate at 50 let nine of those through; 100 lets none, and
#: still leaves a 15x margin below the weakest real knee.
#:
#: Two limits, written down rather than papered over.
#:
#: One number cannot mean one thing at every record length.  Simulating the
#: null -- straight lines with normal noise, through the same smoothing and the
#: same exhaustive search, 1,500 records per length -- puts 100 near the 98th
#: percentile of the largest score at 15 cycles and past the 99.9th at 200.  On
#: a short record ``detected=False`` therefore means closer to "not at this
#: length" than to "no knee".
#:
#: And it assumes each residual is its own piece of evidence.  Where they
#: wander together -- a slow temperature drift, a cell still settling -- a bent
#: line fits that wander, and on 500 straight-line records with AR(1) or
#: random-walk residuals a knee was reported in one in ten.
#:
#: Both were attacked and the attempt was reverted: a length- and
#: correlation-aware bar cut the correlated false knees by a third and cost a
#: third of the power on planted ones.  Doing it properly means bootstrapping
#: the whole selection under the null and validating on held-out real cells,
#: not another constant.  ``docs/reviews/2026-08-21-codex-knee-review.md`` has
#: the measurements to start from.
MIN_FIT_GAIN_F = 100.0
#: A window slope wobbles on its own.  Where early life is a straight line that
#: wobble is the measurement noise, so the slope-ratio limit is lowered by this
#: many robust standard deviations of it.  Without the allowance a 1.6-sigma
#: excursion at cycle 24 was reported as the knee of a cell that bends at 40.
SLOPE_NOISE_SIGMAS = 2.0
#: The local rate must stay past the limit for this many consecutive windows.
#: One window is a glitch; two overlapping ones mean the curve moved.
SUSTAINED_WINDOWS = 2

#: Double Bacon-Watts (ADR 0021; Fermin-Cueto et al. 2020).  Eight parameters;
#: below this many cycles the residual degrees of freedom (n-8) stop meaning
#: anything, and the two transitions have nowhere distinct to sit.
DBW_MIN_POINTS = 12
#: Initial-value grid resolution for (x1, x2).  The fit is sensitive to where
#: it starts -- one curve_fit from one guess lands in local minima -- so
#: candidate transition pairs are scanned (the supplied procedure's 15x15).
DBW_GRID = 15
#: How many of the best-scoring grid seeds get the full nonlinear refinement.
#: The grid itself is scored by *exact* linear least squares (the model is
#: linear in the alphas once x1, x2 and the gammas are fixed), so only the
#: winners need scipy.
DBW_REFINE_SEEDS = 3
#: Transition sharpness bounds, in cycles, from the supplied procedure.
DBW_GAMMA_BOUNDS = (0.1, 20.0)
#: Convergence tolerance for the Bacon-Watts fits.  The solver's default 1e-8
#: polishes transition estimates to a millionth of a cycle -- three orders
#: below the data's own resolution -- and on a knee-less record it wanders a
#: flat likelihood 2.6x longer doing it.  1e-6 moves the answers by under
#: 0.05 cycles on every archetype.
DBW_FIT_TOL = 1e-6


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
    #: Where the fade first leaves its early trend -- the knee-onset (ADR 0021).
    #: Only the ``dbw`` criterion estimates it; everywhere else it stays None.
    #: ``cycle`` is the knee-point, the later of the two.
    onset_cycle: float | None = None

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


def _weak_bend(method: str, breakpoint: float, detail: dict) -> KneeResult:
    """Bent, but not more than a straight line manages by accident."""
    return KneeResult(
        method, None, False,
        "a bent line fits no better than a straight one", detail,
        candidate_cycle=float(breakpoint),
    )


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
    if float(detail.get("fit_gain_score", 0.0)) < MIN_FIT_GAIN_F:
        return KneeResult(
            method, None, False,
            f"only {drop:.1f}% is lost after cycle {breakpoint:.0f} "
            f"(needs {MIN_KNEE_DROP_PCT:g}%), and a line bent there fits no "
            f"better than a straight one",
            detail, candidate_cycle=float(breakpoint),
        )

    # Everything below is in observed terms.  Working out how long the loss
    # "would" take from a fitted slope mixed units -- %/cycle against a count
    # of rows -- so a record with gaps got a different answer from the same
    # cell densely sampled, and the comparison sat exactly on a floating-point
    # boundary for round numbers.  The realised rate is drop/followup and the
    # units cancel.
    if followup < MIN_FOLLOWUP_CYCLES:
        return KneeResult(
            method, None, False,
            f"cycle {breakpoint:.0f} bends, but only {followup} cycles follow it -- "
            f"too few to say whether it costs anything ({drop:.1f}% so far)",
            detail, status=STATUS_INSUFFICIENT, candidate_cycle=float(breakpoint),
        )
    # "It cost nothing" has to be a claim that more cycling would not change the
    # answer, so it is made by projection rather than by how far along the
    # record happens to be.  A halfway rule looked reasonable and made the state
    # move backwards in time: the same slow cell read `insufficient` at 60
    # cycles, `none` from 70 to 150, `insufficient` again at 160 and `detected`
    # at 217.  Nothing about the cell changed at cycle 70.
    rate = drop / followup
    projected = rate * MATERIAL_HORIZON_CYCLES
    detail["projected_loss_pct"] = projected
    if projected >= MIN_KNEE_DROP_PCT:
        return KneeResult(
            method, None, False,
            f"cycle {breakpoint:.0f} bends and has cost {drop:.1f}% over {followup} "
            f"cycles -- at this rate it reaches {MIN_KNEE_DROP_PCT:g}% within "
            f"{MATERIAL_HORIZON_CYCLES} cycles, so more record would settle it",
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


def _f_gain(rss_single: float, rss_model: float, n: int, extra: int,
            parameters: int | None = None) -> float:
    """How much residual the bent model removes, per residual it leaves.

    Shaped like an F ratio and deliberately not called one: the break point was
    chosen by looking at the data and the series was median-smoothed first, so
    no tabulated distribution applies.  What it is compared against is measured
    instead -- see ``_fit_gain_threshold``.
    """
    if rss_model <= 0:
        return float("inf")
    # ``parameters`` is how many the *fuller* model has, which is not always
    # ``2 + extra``: an incremental comparison against a model that already
    # carries a nuisance break is one break against two, so the residual
    # degrees of freedom are n-4 and not n-3.  Left implicit it inflated short
    # records by (n-3)/(n-4).
    full = parameters if parameters is not None else 2 + extra
    return ((rss_single - rss_model) / extra) / (rss_model / max(n - full, 1))


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
        incremental = _f_gain(without, with_both, n, 1, parameters=4)
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


def _column_fit(design: np.ndarray, values: np.ndarray) -> float:
    """Residual sum of squares of a least-squares fit to given columns."""
    coefficients, *_ = np.linalg.lstsq(design, values, rcond=None)
    residual = values - design @ coefficients
    return float(np.dot(residual, residual))


def _exact_level_shift(cycles: np.ndarray, values: np.ndarray):
    """Best fit of "one straight line, a block, and whatever the block left".

    The design is ``1, x, 1[t1 <= x < t2], 1[x >= t2]``.  Three things follow
    from that fourth column, and each of them was a wrong answer without it:

    *A block can leave something behind.*  With only the block term, a cell
    that dropped 5 % for twenty cycles and stayed 2.5 % down afterwards was
    described as having "rejoined the trend".  The permanent part now has
    somewhere to go, and its size is what decides whether anything rejoined.

    *Two permanent steps are not a block.*  Cycles 30 and 60 each losing
    capacity and never recovering was fitted as one block from 30 to 86 that
    "rejoined", because a tilted baseline absorbed the tail.

    *Blocks go both ways.*  A gentler diagnostic reads *higher*, not lower, and
    excluding positive offsets meant a cell that spent twenty cycles 4 % above
    its own trend and came back was handed a knee.

    Returns ``(rss, first cycle, last cycle, block offset, residual offset)``.
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
        block_n = s["n"][i] - s["n"][js]
        block_x = s["x"][i] - s["x"][js]
        block_y = s["y"][i] - s["y"][js]
        tail_n, tail_x, tail_y = s["n"][js], s["x"][js], s["y"][js]

        m = len(js)
        gram = np.empty((m, 4, 4))
        upper = {
            (0, 0): np.full(m, all_n), (0, 1): np.full(m, all_x),
            (0, 2): block_n, (0, 3): tail_n,
            (1, 1): np.full(m, all_xx), (1, 2): block_x, (1, 3): tail_x,
            (2, 2): block_n, (2, 3): np.zeros(m),   # the two blocks never overlap
            (3, 3): tail_n,
        }
        for (row, col), value in upper.items():
            gram[:, row, col] = value
            gram[:, col, row] = value
        moment = np.column_stack([np.full(m, all_y), np.full(m, all_xy),
                                  block_y, tail_y])
        gram[:, range(4), range(4)] += 1e-10
        beta = np.linalg.solve(gram, moment[..., None])[..., 0]
        rss = total_yy - np.einsum("ij,ij->i", beta, moment)
        k = int(np.argmin(rss))
        if best is None or rss[k] < best[0]:
            best = (float(rss[k]), i, int(js[k]),
                    float(beta[k, 2]), float(beta[k, 3]))
    if best is None:
        return None
    rss, i, j, offset, residual = best
    # The block column covers [i, j) and the tail covers [j, n), so the last
    # cycle *in* the block is j-1.  Returning j made every reported block one
    # cycle too long and pushed the end-of-record check over by one, which
    # rejected a block with four clear cycles behind it.
    return rss, i, max(j - 1, i), offset, residual


def _protocol_excursion(cycles: np.ndarray, values: np.ndarray,
                        rss_bend: float):
    """A block of cycles that sat off the trend and then rejoined it.

    Returns ``(first cycle, last cycle, offset, first index, last index)`` when
    that story fits the curve better than any bend does, and None otherwise.

    Degradation is permanent.  A cell that drops 4 % for twenty cycles and then
    comes back did not degrade there -- something about how it was measured
    changed and changed back, which is what a C-rate block or a temperature
    excursion inside a cycling schedule looks like.  The continuous hinge has
    no way to say that, so it spends its two break points on a steep drop and a
    recovery and reports the drop as an onset of degradation, several cycles
    before the block even begins.

    The record does not carry the schedule down here, so the shape has to stand
    in for the metadata, and four things have to hold at once.
    """
    n = len(cycles)
    shift = _exact_level_shift(cycles, values)
    if shift is None:
        return None
    rss, start, end, offset, residual = shift
    # Clearly better than a bend, not better by a nose.  On a straight line both
    # models are fitting noise and the block model wins by a couple of percent
    # about half the time; naming an "excursion" there would be inventing an
    # event.  A real block leaves a third of the residual or less (2.3 against
    # 44 on a 4 %p step).
    #
    # Known limit: this competition is line-versus-line-with-a-block, so a cell
    # that has a real knee *and* a block has no straight line to offer and the
    # block search chases the knee's residual instead.  On an adversarial grid
    # of block position, length, sign and post-knee rate, a third of the cells
    # come back with the wrong cycle -- usually the block's trailing edge.
    # Searching the block in the bend's residual was tried and did not find it
    # either; telling the two apart needs them fitted together, which is the
    # joint event model this module does not have yet.
    if rss >= 0.7 * rss_bend:
        return None

    # Seen rejoining, counted in observations.  Comparing cycle *numbers*
    # against `last - MIN_SEGMENT` rejected a block that ended at cycle 96 of a
    # 100-cycle record even though four full cycles followed it, and accepted
    # one that ended at 97 with three.
    if end > n - 1 - MIN_SEGMENT:
        return None
    # Deep enough to be an event rather than a wobble.  The two break points
    # are chosen by looking at every pair, so the deepest block a *straight*
    # line can be made to yield is what has to be cleared: on 100 records each,
    # white noise reached 4.3 residual scales and AR(1) noise 6.8, while a real
    # 1 %p block sits at 7.4 and a 4 %p block at 32.  Five buys most of the
    # separation; a 0.5 %p block lands at 3.3 and is lost, which is honest --
    # that is a block inside the noise.
    #
    # AR(1) noise still crosses this about one record in eight.  That is the
    # same uncorrected-selection-under-dependence problem as ``MIN_FIT_GAIN_F``
    # and it is not fixed here either.
    scale = np.sqrt(rss / max(n - 4, 1))
    if abs(offset) < EXCURSION_DEPTH_SIGMAS * scale:
        return None
    # And it has to have actually rejoined.  What the block left behind is
    # fitted alongside it, so a partial recovery or a second permanent step
    # shows up as a residual offset that is a real fraction of the block.
    if abs(residual) > REJOIN_TOLERANCE * abs(offset):
        # Unless what it is absorbing is not a step at all.  A cell with a
        # C-rate block at 20-38 *and* a real knee at 50 leaves the post-block
        # cycles far from the original line, and a step term will happily take
        # that up -- the block then reads as a partial recovery and the knee
        # disappears.  A step and a slope change are different shapes, so ask
        # which one fits: if a hinge does at least as well, the leftover is the
        # knee and the block itself did rejoin.
        block = np.zeros(n)
        block[start:end + 1] = 1.0
        tail = np.zeros(n)
        tail[end + 1:] = 1.0
        ones, xs = np.ones(n), cycles
        step_rss = _column_fit(np.column_stack([ones, xs, block, tail]), values)
        best_hinge = None
        for k in range(end + 1 + MIN_SEGMENT, n - MIN_SEGMENT):
            hinge = np.maximum(cycles - float(cycles[k]), 0.0)
            rss_k = _column_fit(np.column_stack([ones, xs, block, hinge]), values)
            if best_hinge is None or rss_k < best_hinge:
                best_hinge = rss_k
        if best_hinge is None or best_hinge > step_rss:
            return None
    return float(cycles[start]), float(cycles[end]), offset, start, end


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
              "slope_late": slopes[2], "fit_gain_score": gain, "segments": 3.0,
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
        (first, slopes[0], slopes[1], slopes[2],
         _f_gain(without_first, rss, n, 1, parameters=4)),
        (second, slopes[1], slopes[2], None,
         _f_gain(without_second, rss, n, 1, parameters=4)),
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
        detail["fit_gain_score"] = min(gain, own_gain)
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
        if then is None:
            tail = ""
        elif then < after - MIN_FADE_RATE:
            tail = f" and steepens again from cycle {second:.0f} ({then:.3f} %/cycle)"
        else:
            tail = f" and eases off again from cycle {second:.0f} ({then:.3f} %/cycle)"
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
        "fit_gain_score": gain,
        "segments": 2.0,
        "rss_bend": rss,
    }

    two_line = _judge_two_line(cycles, values, detail, breakpoint,
                               slope_before, slope_after, drop, gain)

    # Both models, always -- the docstring said so and the code did not.  A
    # cell with breaks at 50 and 150 fitted as two lines lands at 147 with a
    # residual of 247; three lines put the breaks where they are and leave
    # 5e-25.  Returning the two-line answer because it happened to be
    # *detected* threw that away, and with it the earlier of the two events.
    #
    # The second break has to earn itself: preferred only when adding it to the
    # best two-line model removes as much residual as a break has to.  Without
    # that a third segment always fits a little better and every cell would get
    # one.
    three = _exact_three_break(cycles, values)
    escalate = (three is not None
                and _f_gain(rss, three[0], n, 1, parameters=4) >= MIN_FIT_GAIN_F)
    if escalate:
        escalated = _three_segment(cycles, values, rss_single)
        if escalated.detected:
            return escalated
    if two_line.detected:
        return two_line

    if not escalate:
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
        return _weak_bend("segmented", breakpoint, detail)

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
              "slope_noise": spread,
              }
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
        # `_not_yet` reads `slope_after` to work out how long the loss would
        # take at this rate.  Without it the rate came out 0, the answer was
        # "needs infinitely many cycles", and this criterion could never say
        # `insufficient` -- the state existed for segmented only.
        detail["slope_after"] = float(local[k])
        detail["drop_after_pct"] = drop
        # Structure first, consequence second: `_not_yet` defers only when the
        # bend itself is supported, so it has to know the fit gain already.
        gain = _bend_gain(cycles, values, cycle)
        detail["fit_gain_score"] = gain
        if drop < MIN_KNEE_DROP_PCT:
            # Keep looking.  Returning here proved only that the *first*
            # candidate failed, while saying "the rate never stayed" -- a cell
            # with a transient at cycle 60 and its real knee at 95 was reported
            # as having none, because the transient got asked first.
            held = held or _not_yet("slope_ratio", cycle, drop, cycles, dict(detail))
            continue
        if gain < MIN_FIT_GAIN_F:
            held = held or _weak_bend("slope_ratio", cycle, dict(detail))
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
    # Structure first, consequence second: `_not_yet` defers only when the bend
    # itself is supported, so the score has to exist before it is asked.
    # Computed after, it read a missing key as zero and this criterion could
    # never say `insufficient` either.
    gain = _bend_gain(cycles, smoothed, cycle)
    detail["fit_gain_score"] = gain
    if drop < MIN_KNEE_DROP_PCT:
        # Curvature is scale-free: the sharpest bend on a curve that never
        # goes anywhere is still the sharpest bend.  A cell that loses 0.5 %
        # after its "knee" did not have one.
        return _not_yet("curvature", cycle, drop, cycles, detail)
    if gain < MIN_FIT_GAIN_F:
        return _weak_bend("curvature", cycle, detail)
    return KneeResult("curvature", cycle, True,
                      f"maximum curvature at cycle {cycle:.0f}", detail)


def _dbw_model(x, a0, a1, a2, a3, x1, x2, g1, g2):
    """Double Bacon-Watts (Fermin-Cueto et al. 2020, eq. as supplied).

    ``x1`` is the knee-onset, ``x2`` the knee-point, the gammas the sharpness
    of each transition.  Symmetric under swapping (a2, x1, g1) with
    (a3, x2, g2) -- the a1*(x-x1) term only moves a constant into the
    intercept -- so a fit that converges with the labels crossed is the same
    curve and gets relabelled, not rejected.
    """
    u = x - x1
    v = x - x2
    return a0 + a1 * u + a2 * u * np.tanh(u / g1) + a3 * v * np.tanh(v / g2)


def _dbw_jacobian(x, a0, a1, a2, a3, x1, x2, g1, g2):
    """Analytic derivatives of ``_dbw_model`` for the solver.

    Finite differencing costs one model evaluation per parameter per
    iteration, and on a knee-less record the optimiser wanders a flat
    likelihood for hundreds of iterations -- the fit ran 3x slower without
    this, and the dashboard pays it once per cell.
    """
    u = x - x1
    v = x - x2
    tu = np.tanh(u / g1)
    tv = np.tanh(v / g2)
    du = 1.0 - tu * tu          # d tanh
    dv = 1.0 - tv * tv
    return np.column_stack((
        np.ones_like(x),                          # a0
        u,                                        # a1
        u * tu,                                   # a2
        v * tv,                                   # a3
        -a1 - a2 * (tu + u * du / g1),            # x1
        -a3 * (tv + v * dv / g2),                 # x2  (a1 rides on u only)
        -a2 * u * u * du / (g1 * g1),             # g1
        -a3 * v * v * dv / (g2 * g2),             # g2
    ))


def _bw_model(x, a0, a1, a2, x1, g1):
    """Single Bacon-Watts -- one smooth transition (Bacon & Watts 1971)."""
    u = x - x1
    return a0 + a1 * u + a2 * u * np.tanh(u / g1)


def _bw_jacobian(x, a0, a1, a2, x1, g1):
    u = x - x1
    tu = np.tanh(u / g1)
    du = 1.0 - tu * tu
    return np.column_stack((
        np.ones_like(x),
        u,
        u * tu,
        -a1 - a2 * (tu + u * du / g1),
        -a2 * u * u * du / (g1 * g1),
    ))


def _transition_seeds(cycles, values, columns):
    """Score an initial-value grid by exact linear least squares.

    The supplied procedure runs a full ``curve_fit`` from every grid point
    because one start lands in local minima.  The same grid can be scored
    without the nonlinear solver: with the transitions and gammas held fixed
    both models are linear in their alphas, so each candidate's best SSE is
    one ``lstsq``.  Only the best few seeds get the real fit -- the same
    search with exact inner solutions (ADR 0021).

    ``columns(x1, x2, gamma)`` builds the design matrix; for the single-
    transition model it ignores ``x2`` and the grid collapses to one axis.
    """
    lo, hi = float(cycles[0]), float(cycles[-1])
    x1_grid = np.linspace(lo + 2, hi - 4, DBW_GRID)
    x2_grid = np.linspace(lo + 4, hi - 1, DBW_GRID)
    scored = []
    # Two sharpness seeds: gamma=1 (the procedure's start) finds cliff knees,
    # gamma=5 keeps a gentle bend from scoring as noise on the grid pass.
    for gamma in (1.0, 5.0):
        for x1 in x1_grid:
            for x2 in x2_grid:
                if x2 <= x1:
                    continue
                design = columns(x1, x2, gamma)
                if design is None:
                    continue
                coef, *_ = np.linalg.lstsq(design, values, rcond=None)
                sse = float(np.sum((design @ coef - values) ** 2))
                scored.append((sse, float(x1), float(x2), gamma, coef))
    scored.sort(key=lambda item: item[0])
    return scored[:DBW_REFINE_SEEDS]


def _dbw_fit(cycles, values):
    """Best double-transition fit over the seeded starts; ``None`` if nothing
    converges.  Bounds are the supplied procedure's: alphas free, both
    transitions inside the record, gammas in ``DBW_GAMMA_BOUNDS``."""
    from scipy.optimize import curve_fit

    lo, hi = float(cycles[0]), float(cycles[-1])
    gamma_lo, gamma_hi = DBW_GAMMA_BOUNDS

    def columns(x1, x2, gamma):
        u = cycles - x1
        v = cycles - x2
        return np.column_stack((np.ones_like(cycles), u,
                                u * np.tanh(u / gamma), v * np.tanh(v / gamma)))

    bounds = ([-np.inf] * 4 + [lo, lo, gamma_lo, gamma_lo],
              [np.inf] * 4 + [hi, hi, gamma_hi, gamma_hi])
    best = None
    for _, x1, x2, gamma, coef in _transition_seeds(cycles, values, columns):
        try:
            popt, _ = curve_fit(_dbw_model, cycles, values,
                                p0=[*coef, x1, x2, gamma, gamma],
                                jac=_dbw_jacobian, bounds=bounds,
                                ftol=DBW_FIT_TOL, xtol=DBW_FIT_TOL,
                                maxfev=20000)
        except (RuntimeError, ValueError):
            continue
        sse = float(np.sum((_dbw_model(cycles, *popt) - values) ** 2))
        if best is None or sse < best[0]:
            best = (sse, popt)
    return best


def _bw_fit(cycles, values):
    """Best single-transition fit, same seeding and bounds discipline."""
    from scipy.optimize import curve_fit

    lo, hi = float(cycles[0]), float(cycles[-1])
    gamma_lo, gamma_hi = DBW_GAMMA_BOUNDS

    seen = set()

    def columns(x1, x2, gamma):
        # One transition: the x2 axis of the shared grid is meaningless, so
        # each (x1, gamma) is scored once and the rest are skipped.
        if (x1, gamma) in seen:
            return None
        seen.add((x1, gamma))
        u = cycles - x1
        return np.column_stack((np.ones_like(cycles), u, u * np.tanh(u / gamma)))

    bounds = ([-np.inf] * 3 + [lo, gamma_lo],
              [np.inf] * 3 + [hi, gamma_hi])
    best = None
    for _, x1, _x2, gamma, coef in _transition_seeds(cycles, values, columns):
        try:
            popt, _ = curve_fit(_bw_model, cycles, values,
                                p0=[*coef, x1, gamma],
                                jac=_bw_jacobian, bounds=bounds,
                                ftol=DBW_FIT_TOL, xtol=DBW_FIT_TOL,
                                maxfev=20000)
        except (RuntimeError, ValueError):
            continue
        sse = float(np.sum((_bw_model(cycles, *popt) - values) ** 2))
        if best is None or sse < best[0]:
            best = (sse, popt)
    return best


def _judge_bacon_watts(cycles, values, detail, point, onset, slope_before,
                       slope_after, gain) -> KneeResult:
    """The same gates the two-line fit passes, with Bacon-Watts wording.

    ``curve_fit`` always converges to something, so like ``curvature`` this
    family would name a cycle on every curve it sees; nothing here is a knee
    until the fade accelerates, costs something, and fits better bent.
    """
    if slope_before > -MIN_FADE_RATE and slope_after > -MIN_FADE_RATE:
        return KneeResult("dbw", None, False, "capacity is not fading", detail)
    if slope_after >= slope_before:
        return KneeResult("dbw", None, False,
                          "fade does not accelerate across the fitted "
                          "transition", detail)
    ratio = _acceleration(slope_before, slope_after)
    _record_ratio(detail, ratio)
    if ratio < MIN_SLOPE_RATIO:
        return KneeResult("dbw", None, False,
                          f"fade accelerates only {ratio:.2f}x "
                          f"(needs {MIN_SLOPE_RATIO:g}x)", detail)
    # The documented failure shape (ADR 0021): on sub-linear records DBW
    # pushes the knee-point past the data, which under bounds means onto the
    # last few cycles or the boundary itself.  A genuine bend that late is
    # also unconfirmable -- either way the record ends before the evidence.
    n = len(cycles)
    if point >= float(cycles[max(n - MIN_SEGMENT, 0)]):
        # "Not yet" is a claim that something bent (see _not_yet).  Without
        # structural support this is a straight line whose fit wandered to
        # the boundary -- ten of the 200 null-sweep curves did exactly that --
        # and deferring it would make a healthy cell read "unconfirmed".
        if gain < MIN_FIT_GAIN_F:
            return _weak_bend("dbw", point, detail)
        return KneeResult(
            "dbw", None, False,
            f"the fitted knee-point sits at cycle {point:.0f}, within the "
            f"last {MIN_SEGMENT} cycles of the record -- either the bend is "
            f"too recent to confirm, or the fit pushed it to the edge, which "
            f"is what this model does on sub-linear fades",
            detail, status=STATUS_INSUFFICIENT, candidate_cycle=point,
        )
    drop = float(values[cycles >= point][0] - values[-1])
    detail["drop_after_pct"] = drop
    if drop < MIN_KNEE_DROP_PCT:
        return _not_yet("dbw", point, drop, cycles, detail)
    if gain < MIN_FIT_GAIN_F:
        return _weak_bend("dbw", point, detail)

    if onset is None:
        where = f"at cycle {point:.0f} (one transition; no separate onset resolved)"
    else:
        where = (f"at cycle {onset:.0f} (onset) and settles in "
                 f"by cycle {point:.0f}")
    if not np.isfinite(ratio):
        return KneeResult(
            "dbw", point, True,
            f"fade begins {where} ({slope_before:+.3f} -> {slope_after:.3f} "
            f"%/cycle)",
            detail, onset_cycle=onset,
        )
    return KneeResult(
        "dbw", point, True,
        f"fade leaves its early trend {where}, steepening {ratio:.2f}x "
        f"({slope_before:.3f} -> {slope_after:.3f} %/cycle)",
        detail, onset_cycle=onset,
    )


def _dbw_knee(cycles: np.ndarray, values: np.ndarray) -> KneeResult:
    """Knee-onset and knee-point from a Double Bacon-Watts fit (ADR 0021).

    One fit estimates both ends of the same event: where the fade first
    leaves its early trend (x1, the onset) and where the rapid loss settles
    in (x2, the point).  The other criteria answer only the second question.

    The second transition has to earn itself, exactly as the third line does
    in ``_segmented_knee``: on a curve that one transition describes -- a
    plain hinge -- the double model's x2 carries no slope change and lands
    wherever the noise leans, so it would report a confident knee-point at a
    cycle where nothing happened.  The single Bacon-Watts fit is therefore
    taken first, and the double fit speaks only when adding its transition
    removes as much residual as a break has to.  When it does not, the knee
    has no resolvable onset and the result says so instead of inventing one.
    """
    n = len(cycles)
    if n < DBW_MIN_POINTS:
        return KneeResult("dbw", None, False,
                          f"needs at least {DBW_MIN_POINTS} cycles, has {n}")
    try:
        import scipy.optimize  # noqa: F401  -- deferred; wrdkit core is numpy-only
    except ImportError:
        return KneeResult(
            "dbw", None, False,
            "scipy is not installed, so the Bacon-Watts fits were skipped "
            "(pip install 'wrdkit[eis]')",
            status=STATUS_INDETERMINATE,
        )
    rss_single = _linear_fit(cycles, values)[2]

    single = _bw_fit(cycles, values)
    double = _dbw_fit(cycles, values)
    if single is None and double is None:
        return KneeResult("dbw", None, False,
                          "the fit converged from none of the seeded starts")

    judged_double = None
    if double is not None:
        sse, popt = double
        a0, a1, a2, a3, x1, x2, g1, g2 = (float(value) for value in popt)
        if x2 < x1:
            # Same curve, labels crossed (see _dbw_model).  The onset is the
            # earlier transition by definition.
            x1, x2, g1, g2, a2, a3 = x2, x1, g2, g1, a3, a2
        escalate = (single is None
                    or _f_gain(single[0], sse, n, 2, parameters=8)
                    >= MIN_FIT_GAIN_F)
        if escalate:
            detail = {
                "knee_onset": x1, "breakpoint": x2,
                "gamma_onset": g1, "gamma_point": g2,
                "slope_before": a1 - a2 - a3, "slope_after": a1 + a2 + a3,
                "rss_dbw": sse, "rss_single_line": rss_single,
                "fit_gain_score": _f_gain(rss_single, sse, n, 6, parameters=8),
                "transitions": 2.0,
            }
            # The double fit earned both transitions, but "onset then point"
            # is a claim about their *shape*, not just their existence.  Each
            # transition changes the slope by twice its alpha, so:
            #
            # A closing transition that eases (a3 >= 0) is a crash levelling
            # off or a lull ending -- there is no cycle where rapid loss
            # settles in, and the fitted x2 marks where the fade *slowed*.
            # Reporting it as the knee-point put the answer at the crash's
            # exit instead of its entry.
            if a3 >= 0:
                return KneeResult(
                    "dbw", None, False,
                    f"the later transition (cycle {x2:.0f}) eases the fade "
                    f"rather than steepening it -- a crash that eases off or "
                    f"a lull, not an onset-to-point knee; the segmented "
                    f"criterion handles that shape", detail)
            # Transitions that do not overlap are two events with a straight
            # stretch between them, not one event's onset and point.  tanh is
            # 96 % saturated two gammas out, so the zones touch only while
            # the gap is within twice the summed widths.  Without this a cell
            # that bends at 50 and collapses at 150 reported "onset 50,
            # point 150" -- two knees wearing one knee's labels.
            if a2 < 0 and (x2 - x1) > 2.0 * (g1 + g2):
                detail["separation_cycles"] = x2 - x1
                return KneeResult(
                    "dbw", None, False,
                    f"the two fitted transitions ({x1:.0f} and {x2:.0f}) are "
                    f"separate events, not one knee's onset and point -- the "
                    f"stretch between them is straight; the segmented "
                    f"criterion reports the earliest",
                    detail)
            # An opening transition that eases (a2 >= 0) is the end of a lull,
            # not the onset of the fade; the knee is the closing transition
            # alone.
            onset = x1 if a2 < 0 else None
            judged_double = _judge_bacon_watts(
                cycles, values, detail, x2, onset,
                a1 - a2 - a3, a1 + a2 + a3, detail["fit_gain_score"],
            )
            if judged_double.detected:
                return judged_double

    judged_single = None
    if single is not None:
        sse, popt = single
        a0, a1, a2, x1, g1 = (float(value) for value in popt)
        detail = {
            "breakpoint": x1, "gamma_point": g1,
            "slope_before": a1 - a2, "slope_after": a1 + a2,
            "rss_bw": sse, "rss_single_line": rss_single,
            "fit_gain_score": _f_gain(rss_single, sse, n, 4, parameters=6),
            "transitions": 1.0,
        }
        judged_single = _judge_bacon_watts(
            cycles, values, detail, x1, None,
            a1 - a2, a1 + a2, detail["fit_gain_score"],
        )
        if judged_single.detected:
            return judged_single

    # Neither model found a knee.  Prefer whichever rejection actually looked
    # at a break point: "not yet confirmed" says more than "no acceleration".
    for candidate in (judged_double, judged_single):
        if candidate is not None and candidate.status == STATUS_INSUFFICIENT:
            return candidate
    return judged_double or judged_single


def dbw_confidence_interval(cycles, values, *, n_boot: int = 200,
                            seed: int = 0) -> dict | None:
    """Case-resampling bootstrap 95 % CI for (onset, point) -- Fermin-Cueto 2020.

    ``values`` is the same series the criterion fitted: retention from the
    reference cycle on.  Each resample refits from the full fit's optimum, as
    the supplied procedure does.  **Not called on the request path**: one
    resample is one fit, and 200 of them belong in a report script, not in
    every dashboard render (ADR 0021).

    ``None`` when the base fit fails or fewer than half the resamples
    converge -- an interval built from the surviving quarter would look exact
    and mean nothing (0.4).
    """
    cycles = np.asarray(cycles, dtype=np.float64)
    values = np.asarray(values, dtype=np.float64)
    fit = _dbw_fit(cycles, values)
    if fit is None:
        return None
    from scipy.optimize import curve_fit

    _, popt = fit
    rng = np.random.default_rng(seed)
    onsets, points = [], []
    n = len(cycles)
    for _ in range(n_boot):
        index = rng.choice(n, size=n, replace=True)
        try:
            resampled, _ = curve_fit(_dbw_model, cycles[index], values[index],
                                     p0=popt, jac=_dbw_jacobian,
                                     ftol=DBW_FIT_TOL, xtol=DBW_FIT_TOL,
                                     maxfev=20000)
        except RuntimeError:
            continue
        low, high = sorted((float(resampled[4]), float(resampled[5])))
        onsets.append(low)
        points.append(high)
    if len(onsets) < n_boot // 2:
        return None
    onset_lo, onset_hi = np.percentile(onsets, [2.5, 97.5])
    point_lo, point_hi = np.percentile(points, [2.5, 97.5])
    return {
        "onset_low": float(onset_lo), "onset_high": float(onset_hi),
        "point_low": float(point_lo), "point_high": float(point_hi),
        "n_resamples_used": len(onsets),
    }


def _criteria(cycles: np.ndarray, retention: np.ndarray, smoothed: np.ndarray, *,
              threshold_pct: float, slope_factor: float, baseline_window: int,
              slope_window: int, smoothing_window: int) -> list[KneeResult]:
    """All five criteria over one stretch of cycles, in a fixed order.

    Pulled out so the same four can be re-run on a record with a
    protocol block taken out of it, and stay index-comparable with the first
    pass.
    """
    n = len(cycles)
    return [
        _threshold_knee(cycles, retention, threshold_pct),
        _segmented_knee(cycles, smoothed),
        # `max(baseline_window, n // 4)` tied the definition of "early life" to
        # how long the cell was eventually watched.  The same cell, analysed at
        # cycle 150 and again at cycle 500, moved its baseline from 37 cycles to
        # 124 -- by then the median of that window was the *late* rate, and the
        # knee it had reported at cycle 51 disappeared.  A window that grows
        # with the record is not a baseline.
        _slope_ratio_knee(cycles, smoothed, factor=slope_factor,
                          baseline_window=baseline_window,
                          window=min(slope_window, max(n // 3, 2))),
        _curvature_knee(cycles, retention, smoothing_window),
        # Appended last on purpose: detect_knee falls back to results[1] (the
        # two-line fit) and the excursion rebuild pairs results by index.
        _dbw_knee(cycles, smoothed),
    ]


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

    results = _criteria(search_cycles, search_retention, smoothed,
                        threshold_pct=threshold_pct, slope_factor=slope_factor,
                        baseline_window=baseline_window, slope_window=slope_window,
                        smoothing_window=smoothing_window)

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
    # Run it whether or not a knee was reported: "cycles 35-55 sat 3.8 % below
    # the trend and rejoined it" is worth saying to somebody holding the run
    # sheet, and it is a better answer than "no acceleration after the best
    # break point" even when both end in the same verdict.
    if bend_rss is not None:
        excursion = _protocol_excursion(search_cycles, smoothed, float(bend_rss))
        if excursion is not None:
            start, end, offset, first_index, last_index = excursion
            note = {"excursion_from": start, "excursion_to": end,
                    "excursion_offset_pct": offset}
            where = "below" if offset < 0 else "above"
            # Take the block out and look again, rather than declaring the cell
            # explained.  Blanking every criterion erased real knees that
            # happened to share a record with a C-rate block: the same cell
            # reported cycle 50 without the block and "no knee" with it.
            keep = np.ones(len(search_cycles), dtype=bool)
            keep[first_index:last_index + 1] = False
            masked_results = None
            if int(keep.sum()) >= 2 * MIN_SEGMENT + 1:
                masked_results = _criteria(
                    search_cycles[keep], search_retention[keep],
                    smooth_series(search_retention[keep], smoothing_window),
                    threshold_pct=threshold_pct, slope_factor=slope_factor,
                    baseline_window=baseline_window, slope_window=slope_window,
                    smoothing_window=smoothing_window,
                )
            outside = (f"cycles {start:.0f}-{end:.0f} sat {abs(offset):.1f}% {where} the "
                       f"trend and rejoined it -- a change in how the cell was "
                       f"measured, not degradation")
            rebuilt = []
            for index, r in enumerate(results):
                if r.method == "threshold":
                    # An EOL crossing inside the block is a crossing of the
                    # block, not of the cell.  Saying "measurement change, not
                    # degradation" and "end of life at cycle 35" about the same
                    # twenty cycles is one report contradicting itself.
                    # The crossing is interpolated between the last cycle above
                    # the line and the first below, so it lands just *before*
                    # the block that caused it.  What has to be inside the
                    # block is the first cycle actually measured below.
                    crossed = float(r.detail.get("first_cycle_below", r.cycle or 0.0))
                    if r.detected and start <= crossed <= end:
                        rebuilt.append(KneeResult(
                            r.method, None, False,
                            f"the {threshold_pct:g}% crossing at cycle {r.cycle:.1f} is "
                            f"inside cycles {start:.0f}-{end:.0f}, where the cell was "
                            f"measured differently",
                            {**r.detail, **note},
                            status=STATUS_INDETERMINATE, candidate_cycle=r.cycle))
                    else:
                        rebuilt.append(r)
                    continue
                found = masked_results[index] if masked_results else None
                if found is not None and found.detected:
                    rebuilt.append(replace(
                        found,
                        detail={**found.detail, **note},
                        reason=(f"{found.reason}; cycles {start:.0f}-{end:.0f} were "
                                f"measured differently and were left out"),
                    ))
                else:
                    rebuilt.append(KneeResult(r.method, None, False, outside,
                                              {**r.detail, **note},
                                              candidate_cycle=r.candidate_cycle))
            results = rebuilt

    # ``dbw`` first (ADR 0021): one fit that estimates the onset and the
    # point of the same event outranks the criteria that only see the point.
    # The rest of the order is ADR 0005's.
    ranked = [r for name in ("dbw", "segmented", "slope_ratio")
              for r in results if r.method == name and r.detected]
    primary = ranked[0] if ranked else results[1]
    if len(ranked) > 1:
        earliest = min(r.cycle for r in ranked)
        latest = max(r.cycle for r in ranked)
        if latest - earliest > smoothing_window:
            # Say that they disagree; do not pick the earlier one.
            #
            # Picking the minimum was a plausible reading of "a knee is where
            # accelerated fade started" and it is not an estimator.  Nothing
            # decides first whether two answers are two events or one event
            # measured twice, so on a cell with a single knee at cycle 80 the
            # minimum of two noisy estimates is systematically early: over 200
            # records the two-line fit averaged +0.02 cycles of error and the
            # minimum averaged -8.2, from 88 records where the rule fired at
            # all.  Several real events are what the three-line model is for --
            # it returns the earliest qualifying transition of one fit, which
            # is an estimate of one thing.
            primary = replace(
                primary,
                detail={**primary.detail, "criteria_spread_cycles": float(latest - earliest)},
                reason=(f"{primary.reason}; another criterion puts it at "
                        f"cycle {(latest if primary.cycle == earliest else earliest):.0f}"),
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
