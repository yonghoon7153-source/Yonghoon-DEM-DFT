"""GITT: pulse, rest, repeat -- and the two things that come out of it.

A GITT run is a long series of short current pulses separated by long rests.
Two different measurements live in that one record.

**Pseudo-OCV.**  At the end of each rest the cell has relaxed, so the voltage
there is (nearly) the equilibrium voltage at the capacity the pulse just
reached.  Plotting those against capacity gives the quasi-equilibrium curve
that a slow constant-current discharge only approximates -- and that
degradation-mode analysis wants, because it separates what the electrode is
from how hard it was pushed.

**Chemical diffusion coefficient.**  Weppner and Huggins showed that if the
pulse is short compared with the diffusion time, the voltage transient goes as
the square root of time, and the ratio of the steady-state step to the
transient step gives D.  "If" is the operative word: the derivation needs the
transient to be linear in sqrt(t), and this module checks that rather than
assuming it (§0.4).

The segmentation follows the lab's own extractor: blocks are runs of constant
*signed* state -- charge pulse, rest, discharge pulse -- so a charge that runs
straight into a discharge with no rest between them is still two blocks.  The
rest threshold is relative to the pulse current in that file, because a 0.1C
pulse on a 5 mAh cell and one on a 50 Ah cell have nothing in common but
shape.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .wrd import WrdFile

__all__ = ["PulseBlock", "PseudoOcvPoint", "PseudoOcv", "DiffusionPoint",
           "DiffusionResult", "segment_pulses", "pseudo_ocv", "diffusion",
           "FARADAY"]

#: C/mol.  Only needed when a molar volume is given.
FARADAY = 96485.332

#: Fraction of the typical pulse current below which a sample counts as rest.
#: The lab's extractor uses five per cent of the 90th percentile; keeping the
#: same numbers means the same file gives the same blocks in both tools.
_REST_RATIO = 0.05
#: A, so that a file whose "pulse" current is itself noise does not make every
#: sample a pulse.
_REST_FLOOR = 1e-7


@dataclass
class PulseBlock:
    """One run of samples at one state: charge pulse, discharge pulse, or rest."""

    #: ``charge`` | ``discharge`` | ``rest``
    mode: str
    start: int
    stop: int          # exclusive
    duration_s: float
    current_mean_a: float
    voltage_start: float
    voltage_end: float
    #: Signed accumulated capacity at the block's last sample, in mAh.
    capacity_end_mah: float

    @property
    def n_points(self) -> int:
        return self.stop - self.start


@dataclass
class PseudoOcvPoint:
    capacity_mah: float
    voltage_v: float
    #: Where in the record this came from, so a suspicious point can be found.
    pulse_start: int
    rest_end: int
    #: How long the cell was allowed to relax.  A short rest is not equilibrium,
    #: and the number that comes out of it is not an OCV.
    rest_s: float
    #: mV over the last tenth of the rest.  Near zero is relaxed; large is not.
    drift_mv: float


@dataclass
class PseudoOcv:
    charge: list[PseudoOcvPoint] = field(default_factory=list)
    discharge: list[PseudoOcvPoint] = field(default_factory=list)
    #: Pulses with no rest after them.  Counted, never silently dropped: a
    #: truncated file ends on a pulse, and so does a protocol that forgot the
    #: last rest, and the two look identical in the curve.
    skipped_charge: int = 0
    skipped_discharge: int = 0
    #: Why a pulse was skipped, in the order they were found.
    skipped_reasons: list[str] = field(default_factory=list)


def _rest_threshold(current: np.ndarray) -> float:
    absolute = np.abs(current)
    nonzero = absolute[absolute > 0]
    if nonzero.size == 0:
        return _REST_FLOOR
    typical = float(np.percentile(nonzero, 90))
    return max(typical * _REST_RATIO, _REST_FLOOR)


def _signed_capacity_mah(wrd: WrdFile) -> np.ndarray:
    """Accumulated capacity across the whole file: charge up, discharge down.

    ``CHARGE Q`` / ``DISCHARGE Q`` are per-cycle running totals -- they reset
    to zero at every cycle boundary (CLAUDE.md §3).  A plain difference across
    the file (``C - C[0]``) therefore *contains* the resets: the counter drops
    by a whole cycle's capacity in one sample, the capacity axis folds back on
    itself, and a six-pulse discharge across a cycle boundary reads
    0, .5, 1.0, 0, .5, 1.0 instead of 0..2.5.  (The first version here was
    ``cumsum(diff(...))``, which is that identity with extra steps.)

    So the sum is built from per-sample **increments**.  Within a cycle the
    counters only grow, so a negative difference can only be a reset; the
    increment at a reset is the counter's own value after it, because the
    counter restarted from zero.
    """
    total = None
    for column, sign in ((wrd.charge_mah(), 1.0), (wrd.discharge_mah(), -1.0)):
        column = np.asarray(column, dtype=float)
        increments = np.diff(column, prepend=column[:1])
        reset = increments < 0
        increments[reset] = column[reset]
        contribution = sign * increments
        total = contribution if total is None else total + contribution
    return np.cumsum(total)


def segment_pulses(wrd: WrdFile, *, rest_threshold_a: float | None = None
                   ) -> list[PulseBlock]:
    """Split a record into pulse and rest blocks.

    Uses the current, not the step counter.  The step counter is the right tool
    for cycling (CLAUDE.md §3) because a schedule step is what a cycle is made
    of, but a GITT schedule often writes one *looped* step pair for hundreds of
    pulses -- the counter then changes at every pulse, which is the same
    answer, or does not, which is the wrong one.  The current says what the
    cell was doing either way.
    """
    if not len(wrd):
        return []
    current = np.asarray(wrd.data["current"], dtype=float)
    voltage = np.asarray(wrd.data["voltage"], dtype=float)
    seconds = wrd.seconds("test_time")
    signed = _signed_capacity_mah(wrd)

    threshold = (rest_threshold_a if rest_threshold_a is not None
                 else _rest_threshold(current))
    state = np.where(np.abs(current) > threshold, np.sign(current), 0.0)

    blocks: list[PulseBlock] = []
    changes = np.flatnonzero(np.diff(state)) + 1
    starts = np.concatenate(([0], changes))
    stops = np.concatenate((changes, [len(state)]))
    for start, stop in zip(starts, stops, strict=True):
        sign = state[start]
        mode = "rest" if sign == 0 else ("charge" if sign > 0 else "discharge")
        blocks.append(PulseBlock(
            mode=mode,
            start=int(start),
            stop=int(stop),
            duration_s=float(seconds[stop - 1] - seconds[start]),
            current_mean_a=float(np.mean(current[start:stop])),
            voltage_start=float(voltage[start]),
            voltage_end=float(voltage[stop - 1]),
            capacity_end_mah=float(signed[stop - 1]),
        ))
    return blocks


def _drift_mv(voltage: np.ndarray, block: PulseBlock) -> float:
    """How much the voltage still moved over the last tenth of the rest."""
    span = block.stop - block.start
    if span < 3:
        return 0.0
    tail = max(block.stop - max(span // 10, 2), block.start)
    window = voltage[tail:block.stop]
    return float(abs(window[-1] - window[0]) * 1000.0)


def pseudo_ocv(wrd: WrdFile, *, min_rest_s: float = 0.0,
               rest_threshold_a: float | None = None) -> PseudoOcv:
    """Quasi-equilibrium voltage against capacity, one point per pulse.

    Each point pairs **the capacity at the end of a pulse** with **the voltage
    at the end of the rest that follows it**.  Those are two different samples
    on purpose: the capacity is what the pulse delivered, and the voltage is
    what the cell settled to afterwards.  Taking both from the same sample
    would give the polarised voltage, which is the curve GITT exists to avoid.

    Capacity is measured from the first pulse of each series, so charge and
    discharge both start at zero and both increase.

    ``min_rest_s`` drops points whose rest was too short to call equilibrium.
    Zero by default -- the drift is reported per point instead, because how
    long is long enough depends on the cell and guessing it here would throw
    away data on one cell and keep noise on another.
    """
    blocks = segment_pulses(wrd, rest_threshold_a=rest_threshold_a)
    voltage = np.asarray(wrd.data["voltage"], dtype=float)
    out = PseudoOcv()

    charge_points: list[PseudoOcvPoint] = []
    discharge_points: list[PseudoOcvPoint] = []
    for i, block in enumerate(blocks):
        if block.mode == "rest":
            continue
        following = blocks[i + 1] if i + 1 < len(blocks) else None
        if following is None or following.mode != "rest":
            reason = ("휴지가 뒤따르지 않는 펄스 (파일 끝이거나 곧바로 방향이 "
                      "바뀝니다)")
            out.skipped_reasons.append(reason)
            if block.mode == "charge":
                out.skipped_charge += 1
            else:
                out.skipped_discharge += 1
            continue
        if min_rest_s and following.duration_s < min_rest_s:
            out.skipped_reasons.append(
                f"휴지가 {following.duration_s:.0f} s 뿐입니다")
            if block.mode == "charge":
                out.skipped_charge += 1
            else:
                out.skipped_discharge += 1
            continue

        point = PseudoOcvPoint(
            capacity_mah=block.capacity_end_mah,
            voltage_v=float(voltage[following.stop - 1]),
            pulse_start=block.start,
            rest_end=following.stop - 1,
            rest_s=following.duration_s,
            drift_mv=_drift_mv(voltage, following),
        )
        (charge_points if block.mode == "charge" else discharge_points).append(point)

    out.charge = _from_baseline(charge_points, charging=True)
    out.discharge = _from_baseline(discharge_points, charging=False)
    return out


def _from_baseline(points: list[PseudoOcvPoint], *, charging: bool
                   ) -> list[PseudoOcvPoint]:
    """Re-zero a series on its own first point, increasing in both directions."""
    if not points:
        return []
    baseline = points[0].capacity_mah
    out = []
    for point in points:
        delta = (point.capacity_mah - baseline if charging
                 else baseline - point.capacity_mah)
        out.append(PseudoOcvPoint(
            capacity_mah=delta,
            voltage_v=point.voltage_v,
            pulse_start=point.pulse_start,
            rest_end=point.rest_end,
            rest_s=point.rest_s,
            drift_mv=point.drift_mv,
        ))
    return out


# --------------------------------------------------------------------------
# Weppner-Huggins
# --------------------------------------------------------------------------
@dataclass
class DiffusionPoint:
    """One pulse's worth of diffusion coefficient, with its own evidence."""

    #: Capacity at the end of the pulse, re-zeroed like the pOCV series.
    capacity_mah: float
    #: Voltage at the end of the following rest -- the same point pOCV plots.
    voltage_v: float
    #: cm²/s, or ``None`` when the pulse did not earn a number.
    d_cm2_s: float | None
    #: Steady-state voltage step between this rest and the previous one, V.
    delta_es_v: float
    #: Transient voltage step during the pulse, IR drop removed, V.
    delta_et_v: float
    pulse_s: float
    #: How straight the transient was against sqrt(t).  The derivation needs
    #: this to be a line; 1.0 is perfect.
    sqrt_t_r_squared: float
    #: Empty when the point is usable.
    reason: str = ""
    pulse_start: int = 0


@dataclass
class DiffusionResult:
    points: list[DiffusionPoint] = field(default_factory=list)
    #: What was missing, when nothing could be computed.
    missing: list[str] = field(default_factory=list)
    #: The geometry the numbers rest on, echoed back so a report can carry it.
    molar_volume_cm3: float | None = None
    molar_mass_g: float | None = None
    mass_g: float | None = None
    area_cm2: float | None = None

    @property
    def usable(self) -> list[DiffusionPoint]:
        return [point for point in self.points if point.d_cm2_s is not None]


def _sqrt_t_fit(seconds: np.ndarray, voltage: np.ndarray,
                origin_s: float) -> tuple[float, float]:
    """Slope and R² of voltage against sqrt(t).

    ``origin_s`` is when the **pulse** started, which is not where the fit
    starts: the first tenth is skipped to leave the ohmic jump behind.  Taking
    the origin from the first fitted sample instead would measure
    ``sqrt(t - t_skip)``, and a transient that is a perfect line in ``sqrt(t)``
    is a curve in that -- so a valid pulse fails the linearity check and the
    method reports that its own assumption does not hold.
    """
    if len(seconds) < 4:
        return 0.0, 0.0
    root = np.sqrt(np.maximum(seconds - origin_s, 0.0))
    if np.ptp(root) == 0:
        return 0.0, 0.0
    slope, intercept = np.polyfit(root, voltage, 1)
    predicted = slope * root + intercept
    total = float(np.sum((voltage - np.mean(voltage)) ** 2))
    if total == 0:
        return float(slope), 0.0
    residual = float(np.sum((voltage - predicted) ** 2))
    return float(slope), float(1.0 - residual / total)


def _transient_step_v(slope: float, duration_s: float) -> float:
    """ΔE_t: the amplitude of the fitted sqrt(t) line over the whole pulse.

    Not ``V(end) - V(skip)``.  The skipped tenth removes the ohmic jump, but
    ``V(skip)`` already contains ``sqrt(0.1) = 31.6 %`` of the diffusion
    transient itself -- a pure sqrt(t) transient has covered that much of its
    amplitude by a tenth of the pulse.  Subtracting from there under-reads
    ΔE_t by the factor ``1 - sqrt(0.1)`` and, since D goes as ``1/ΔE_t²``,
    over-reads **every** D by ``(1 - sqrt(0.1))⁻² = 2.14`` -- with R² = 1 and
    no reason, so nothing on screen says so.  The review caught it because the
    closed-form test was circular: it built its expectation from the result's
    own ΔE_t.

    The fitted line already knows the answer: ``V(t) = a + b·sqrt(t)`` with
    the origin at the pulse start, so the transient from 0⁺ to the end of the
    pulse is exactly ``b·sqrt(tau)``.
    """
    if duration_s <= 0:
        return 0.0
    return float(slope * np.sqrt(duration_s))


#: Below this the transient is not a line against sqrt(t), and the
#: Weppner-Huggins derivation does not hold for it.  0.98 is strict on purpose:
#: the whole method is the assumption, so a point that fails it is not a
#: slightly worse measurement, it is a different equation.
_LINEARITY_FLOOR = 0.98

#: Fraction of a pulse skipped before fitting, to leave the IR drop behind.
#: The ohmic jump is instantaneous and is not part of the diffusion transient;
#: including it bends the first points and lowers R² on a perfectly good pulse.
_IR_SKIP = 0.1


def diffusion(wrd: WrdFile, *, molar_volume_cm3: float | None = None,
              molar_mass_g: float | None = None, mass_g: float | None = None,
              area_cm2: float | None = None,
              rest_threshold_a: float | None = None,
              min_rest_s: float = 0.0) -> DiffusionResult:
    """Chemical diffusion coefficient per pulse (Weppner-Huggins).

        D = (4 / (pi * tau)) * (m * V_M / (M_B * S))^2 * (dE_s / dE_t)^2

    Every symbol outside the record has to be supplied: the molar volume and
    molar mass of the active material, the electrode mass, and the interfacial
    area.  None of them is in a ``.wrd``, and none of them can be guessed --
    a D computed from an assumed molar volume is off by the cube of the
    assumption.  Missing ones come back named, with no numbers (§0.4).

    ``dE_s`` is the change in relaxed voltage from one rest to the next, and
    ``dE_t`` is the voltage swing during the pulse with the ohmic jump removed.
    Both are needed, so the first pulse of a series has no ``dE_s`` and is
    reported without a D.
    """
    result = DiffusionResult(molar_volume_cm3=molar_volume_cm3,
                             molar_mass_g=molar_mass_g, mass_g=mass_g,
                             area_cm2=area_cm2)
    for name, value in (("몰부피 V_M", molar_volume_cm3), ("몰질량 M_B", molar_mass_g),
                        ("활물질 질량", mass_g), ("계면 면적 S", area_cm2)):
        if not value or value <= 0:
            result.missing.append(name)

    blocks = segment_pulses(wrd, rest_threshold_a=rest_threshold_a)
    voltage = np.asarray(wrd.data["voltage"], dtype=float)
    seconds = wrd.seconds("test_time")

    previous_relaxed: float | None = None
    points: list[DiffusionPoint] = []
    for i, block in enumerate(blocks):
        if block.mode == "rest":
            continue
        following = blocks[i + 1] if i + 1 < len(blocks) else None
        if following is None or following.mode != "rest":
            continue
        if min_rest_s and following.duration_s < min_rest_s:
            continue

        relaxed = float(voltage[following.stop - 1])
        span = block.stop - block.start
        skip = block.start + max(int(span * _IR_SKIP), 1)
        window = slice(skip, block.stop)
        slope, r_squared = _sqrt_t_fit(seconds[window], voltage[window],
                                       float(seconds[block.start]))

        delta_es = 0.0 if previous_relaxed is None else relaxed - previous_relaxed
        delta_et = _transient_step_v(slope, block.duration_s)

        reason = ""
        value: float | None = None
        if previous_relaxed is None:
            reason = "직전 휴지가 없어 ΔE_s 를 잴 수 없습니다 (시리즈의 첫 펄스)"
        elif result.missing:
            reason = "재료 상수가 없습니다: " + ", ".join(result.missing)
        elif delta_et == 0 or block.duration_s <= 0:
            reason = "펄스 중 전압이 움직이지 않았습니다"
        elif r_squared < _LINEARITY_FLOOR:
            reason = (f"√t 에 대해 직선이 아닙니다 (R²={r_squared:.3f}) — "
                      "Weppner-Huggins 가정이 성립하지 않습니다")
        else:
            geometry = (mass_g * molar_volume_cm3) / (molar_mass_g * area_cm2)
            value = float((4.0 / (np.pi * block.duration_s))
                          * geometry ** 2 * (delta_es / delta_et) ** 2)

        points.append(DiffusionPoint(
            capacity_mah=block.capacity_end_mah,
            voltage_v=relaxed,
            d_cm2_s=value,
            delta_es_v=delta_es,
            delta_et_v=delta_et,
            pulse_s=block.duration_s,
            sqrt_t_r_squared=r_squared,
            reason=reason,
            pulse_start=block.start,
        ))
        previous_relaxed = relaxed

    if points:
        baseline = points[0].capacity_mah
        for point in points:
            point.capacity_mah -= baseline
    result.points = points
    return result
