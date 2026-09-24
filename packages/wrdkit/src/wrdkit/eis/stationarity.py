"""Was the cell at rest while it was measured? -- the DC side of a sweep
(ADR 0043, 보완 7).

The linear Kramers–Kronig test finds a spectrum no linear, time-invariant
system could give.  A cell that changes *smoothly* under the sweep can still
give one: on the lab's full-cell shapes a drift of 10 % per decade below
0.05 Hz went unflagged on three shapes of four.  The instrument, though, wrote the
cell's state down as it went.  For every frequency point EC-Lab keeps the mean
current ``<I>`` and potential ``<Ewe>`` over that point's measurement -- the DC
level the sine rides on.  In a potentiostatic sweep the potential is held, so
a cell still settling shows up as a DC current that keeps changing; in a
galvanostatic one the current is held and the potential moves.  A cell at rest
does neither.

**The number** is how far that DC level moved during one period of each
point's frequency, as a share of the AC amplitude there::

    share = |d<I>/dt| · (1/f) / |I|        (or <Ewe> and |Ewe|)

A lock-in that integrates whole periods reads a linear ramp of slope ``a`` as
an extra first harmonic of size ``2|a|/ω``, so with no drift correction in
the instrument the point's impedance is off by about ``share / π``.
``test_eis_stationarity`` measures a sweep the way a lock-in does and finds the
error ~10 % above that: the slope is taken between the points' time stamps,
the ends of windows that lengthen point by point.  With a correction the ramp
is taken out, but the cell still changed between the points.

Only what the file says: no column, no number, and ``reason`` names what is
missing.  An ``<I>`` column of zeros is read as "not recorded", the way an
all-zero temperature is (``electrochem-invariants`` §9).

Numpy only.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .spectrum import Spectrum

__all__ = ["DCRecord", "STILL_SHARE", "current_pair", "dc_record", "potential_pair"]

#: Fewer points than this and there is no slope to take.
FEWEST_POINTS = 3
#: Below this the level did not move: a hundredth of a percent of the AC
#: amplitude in a period.  A cell measured at rest reads ~0 here, and the one
#: of the two levels the instrument held reads ~0 whatever the cell does.
STILL_SHARE = 1e-4
#: The start and the end of the sweep are the median of this many points --
#: one glitch at either end should not be the headline.
ENDS = 3

_CURRENT = ("<I>/mA", "I/mA")
_POTENTIAL = ("<Ewe>/V", "Ewe/V")


@dataclass(frozen=True)
class DCRecord:
    """The DC level of one sweep, in the order it was measured.

    ``judged`` is ``False`` when the file does not carry what it takes, and
    then ``reason`` says what is missing.
    """

    judged: bool
    reason: str = ""
    #: Seconds from the first point.
    time_s: np.ndarray = field(default_factory=lambda: np.empty(0))
    frequency_hz: np.ndarray = field(default_factory=lambda: np.empty(0))
    #: ``<I>`` in amperes, ``None`` when not recorded.
    current_a: np.ndarray | None = None
    #: ``<Ewe>`` in volts, ``None`` when not recorded.
    potential_v: np.ndarray | None = None
    #: Per point, the share in the module docstring.  ``None`` when the file
    #: carries no AC amplitude (``|I|/A`` or ``|Ewe|/V``) to compare with.
    share: np.ndarray | None = None
    #: The DC level ``share`` follows: ``"current"`` or ``"potential"``.  The
    #: current, unless the potential moved more (and moved at all) -- the
    #: level the instrument held barely moves, and the lab measures at a held
    #: potential.
    source: str = ""

    @property
    def duration_s(self) -> float:
        return float(self.time_s[-1] - self.time_s[0]) if self.time_s.size else 0.0

    @property
    def current_ends_a(self) -> tuple[float, float] | None:
        return _ends(self.current_a)

    @property
    def potential_ends_v(self) -> tuple[float, float] | None:
        return _ends(self.potential_v)

    @property
    def max_share(self) -> float | None:
        if self.share is None or not self.share.size:
            return None
        return float(np.max(self.share))

    @property
    def at_hz(self) -> float | None:
        """Where the share is largest."""
        if self.share is None or not self.share.size:
            return None
        return float(self.frequency_hz[int(np.argmax(self.share))])


def _ends(values: np.ndarray | None) -> tuple[float, float] | None:
    if values is None or not values.size:
        return None
    count = min(ENDS, values.size)
    return float(np.median(values[:count])), float(np.median(values[-count:]))


def _column(columns: dict, names: tuple[str, ...], size: int) -> np.ndarray | None:
    for name in names:
        values = columns.get(name)
        if values is None:
            continue
        values = np.asarray(values, dtype=np.float64)
        if values.shape == (size,) and np.all(np.isfinite(values)):
            return values
    return None


def dc_record(spectrum: Spectrum | None) -> DCRecord:
    """The DC level of ``spectrum`` from the columns its file carried."""
    if spectrum is None or len(spectrum) < FEWEST_POINTS:
        return DCRecord(False, "점이 모자랍니다")
    columns = spectrum.columns or {}
    size = len(spectrum)
    clock = _column(columns, ("time/s",), size)
    if clock is None:
        return DCRecord(False, "파일에 점마다의 시각이 없습니다")
    current = _column(columns, _CURRENT, size)
    if current is not None and not np.any(current):
        current = None                              # 0 만 적힌 열 = 안 잰 것
    potential = _column(columns, _POTENTIAL, size)
    if potential is not None and not np.any(potential):
        potential = None
    if current is None and potential is None:
        return DCRecord(False, "파일에 직류 전류·전위 기록이 없습니다")

    # 잰 순서대로, 같은 시각이 둘이면 앞의 것만 — 기울기를 나눌 수 없다.
    _, keep = np.unique(clock, return_index=True)
    if keep.size < FEWEST_POINTS:
        return DCRecord(False, "시각이 다른 점이 모자랍니다")
    time = clock[keep] - clock[keep][0]
    frequency = np.asarray(spectrum.frequency_hz, dtype=np.float64)[keep]
    current = current[keep] * 1e-3 if current is not None else None
    potential = potential[keep] if potential is not None else None

    ac_current = _column(columns, ("|I|/A",), size)
    ac_potential = _column(columns, ("|Ewe|/V",), size)
    if ac_current is None and ac_potential is not None:
        ac_current = ac_potential / np.abs(spectrum.z)
    if ac_potential is None and ac_current is not None:
        ac_potential = ac_current * np.abs(spectrum.z)

    shares: dict[str, np.ndarray] = {}
    for level, amplitude, name in ((current, ac_current, "current"),
                                   (potential, ac_potential, "potential")):
        if level is None or amplitude is None:
            continue
        amplitude = amplitude[keep]
        if not np.all(amplitude > 0) or not np.all(frequency > 0):
            continue
        share = np.abs(np.gradient(level, time)) / (frequency * amplitude)
        if np.all(np.isfinite(share)):
            shares[name] = share
    source = ""
    if shares:
        source = "current" if "current" in shares else "potential"
        if "current" in shares and "potential" in shares and (
                float(np.max(shares["potential"]))
                > max(float(np.max(shares["current"])), STILL_SHARE)):
            source = "potential"
    return DCRecord(
        judged=True, time_s=time, frequency_hz=frequency,
        current_a=current, potential_v=potential,
        share=shares.get(source), source=source)


def _amperes(value: float) -> tuple[float, str]:
    """µA, or nA below a microampere -- a pellet's current at the end of its
    sweep is a few nA and read ``-0.0017 µA`` (열네 번째 검수)."""
    if value == 0 or abs(value) >= 1e-6:
        return value * 1e6, "µA"
    return value * 1e9, "nA"


def current_pair(start_a: float, end_a: float) -> str:
    """``34.6 → 2.46 µA``, or ``-2.65 µA → -1.7 nA`` when the units differ."""
    (start, unit), (end, other) = _amperes(start_a), _amperes(end_a)
    if unit == other:
        return f"{start:.3g} → {end:.3g} {unit}"
    return f"{start:.3g} {unit} → {end:.3g} {other}"


def potential_pair(start_v: float, end_v: float) -> tuple[str, str | None]:
    """``("3.7012 → 3.6921 V", "-9.1 mV")`` -- the change apart, since four
    decimals of a volt hide it.  Near 0 V (a symmetric cell) the pair itself
    is in mV and there is no second part: ``0.0004 → 0.0002 V`` said nothing
    (열네 번째 검수, #142)."""
    if max(abs(start_v), abs(end_v)) < 0.1:
        return f"{start_v * 1e3:.3g} → {end_v * 1e3:.3g} mV", None
    return f"{start_v:.4f} → {end_v:.4f} V", f"{(end_v - start_v) * 1e3:+.1f} mV"
