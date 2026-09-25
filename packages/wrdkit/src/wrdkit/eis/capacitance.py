"""What an arc's capacitance says it can be (ADR 0040).

A fit gives ``R``, ``Q`` and ``n`` for every arc.  The resistance is what gets
reported; the capacitance is what says **which process** the arc is -- and it
is the number the screen never showed.  On 2026-09-23 a symmetric cell's two
arcs were called bulk and grain boundary while their capacitances were
4.66e-7 F and 3.00e-4 F: the first cannot be a bulk arc in any pellet, and the
second is an electrode, not a boundary.

**Effective capacitance.**  For ``R ∥ CPE`` the apex of the arc sits at
``ω₀ = (R·Q)^{-1/n}``; the capacitance that puts an ideal ``R ∥ C`` apex at the
same place is::

    C = (Q · R^{1-n})^{1/n}

(Hsu & Mansfeld, *Corrosion* 57, 747 (2001) -- Hirschorn et al.,
*Electrochim. Acta* 55, 6218 (2010), Eq. (18),
``HIRSCHORN2010.hsu-mansfeld-normal-eq18``).  ``n = 1`` gives ``C = Q``, as it
must.

That formula assumes the time constants are spread **through the thickness**
(a "normal" distribution) -- right for a bulk or a grain-boundary arc, and the
reading under which "can this arc be the bulk?" is asked.  An interface whose
time constants are spread **along the surface** takes Brug's formula with the
ohmic resistance instead, and Eq. (18) is then off by −70 % to +100 %
(``HIRSCHORN2010.eq18-on-surface-distribution-wrong``).  That is why a side is
only named when it survives ``DETERMINED_SPREAD`` (below), and why a blocking
tail's capacitance is Brug's (`audit._blocking_capacitance`).

**Which process.**  Irvine, Sinclair & West, *Adv. Mater.* 2, 132 (1990),
tabulated the capacitances that identify each process in a ceramic
(``ISW1990.table1-capacitance-interpretation``: a column of farads, derived
for a cell constant ``l/A = 1 cm⁻¹``, so ``C·l/A`` is in F·cm⁻¹).  A real
pellet is not that cell, and the two kinds of process scale **differently**:

* bulk and grain boundary are capacitors *across the thickness* -- they go as
  ``A/l``, so the comparable number is ``C · l/A``;
* a surface layer, an electrode interface and a reaction live *on a face* --
  they go as ``A`` alone, so the comparable number is ``C / A``.

Scaling both by ``l/A`` (the first version of this) reads a 60 µm pellet's
1 µF/cm² double layer as a grain boundary **only** -- the electrode interface,
which is what it is, falls off the list.

A capacitance can fall in more than one range -- ``C·l/A`` and ``C/A`` differ
by the thickness in cm, and a 60 µm pellet's ``3.6e-9`` and ``5.9e-7`` are a
boundary *and* an interface.  So this module returns **candidates** and never
a single answer.  What it can say firmly is what an arc **cannot** be.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from .circuit import Circuit, parse_circuit

__all__ = ["AREA", "ArcCapacitance", "BOUNDARY", "BULK", "DETERMINED_SPREAD",
           "FACE", "LOWEST_N", "PROCESSES", "Process", "THICKNESS",
           "UNDETERMINED_SPREAD", "arc_capacitances", "candidate_processes",
           "effective_capacitance", "peak_frequency", "process", "reachable",
           "size_class", "spread_for"]

#: ``C · l/A`` -- a capacitor across the whole thickness (bulk, boundary).
THICKNESS = "thickness"
#: ``C / A`` -- a capacitor on a face (layer, interface, reaction).
AREA = "area"

#: Below this ``n`` a CPE is not an arc any more -- ``n = 0.5`` is a Warburg
#: line, and an effective capacitance of a diffusion tail names nothing.
LOWEST_N = 0.6


@dataclass(frozen=True)
class Process:
    """One row of the Irvine–Sinclair–West table."""

    key: str
    label: str
    scaling: str
    #: Half-open ``[low, high)``; ``None`` is unbounded.  F·cm⁻¹ for
    #: ``THICKNESS`` (numerically the capacitance at ``l/A = 1 cm⁻¹``), F/cm²
    #: for ``AREA``.
    low: float | None
    high: float | None

    def holds(self, value: float) -> bool:
        return ((self.low is None or value >= self.low)
                and (self.high is None or value < self.high))


#: The table, with the overlapping ranges of the original cut where the next
#: row starts.  ~1e-12 for a bulk of εr ≈ 10; 1e-4 for a reaction.
PROCESSES: tuple[Process, ...] = (
    Process("bulk", "벌크", THICKNESS, None, 1e-11),
    Process("grain_boundary", "입계", THICKNESS, 1e-11, 1e-8),
    Process("surface_layer", "표면층", AREA, 1e-9, 1e-7),
    Process("interface", "전극 계면", AREA, 1e-7, 1e-5),
    Process("reaction", "전기화학 반응", AREA, 1e-5, None),
)

_BY_KEY = {one.key: one for one in PROCESSES}


def process(key: str) -> Process:
    """The table row for ``key``.  Raises ``KeyError`` for an unknown one."""
    return _BY_KEY[key]


def _positive(*values: float) -> bool:
    return all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0
               for v in values)


def effective_capacitance(resistance_ohm: float, q: float,
                          n: float = 1.0) -> float | None:
    """``(Q · R^{1-n})^{1/n}`` in F, or ``None`` for numbers that are not an arc.

    Worked in logarithms: ``Q`` spans fifteen decades between arcs and a direct
    power of a tiny number loses digits the log does not.
    """
    if not _positive(resistance_ohm, q, n) or n > 1.0:
        return None
    return math.exp((math.log(q) + (1.0 - n) * math.log(resistance_ohm)) / n)


def peak_frequency(resistance_ohm: float, q: float, n: float = 1.0) -> float | None:
    """Where the arc's apex sits: ``1 / (2π (R·Q)^{1/n})`` in Hz.

    If this is outside the frequencies that were fitted, the arc's resistance
    was extrapolated -- the sweep never saw its top.
    """
    if not _positive(resistance_ohm, q, n) or n > 1.0:
        return None
    tau = math.exp(math.log(resistance_ohm * q) / n)
    return 1.0 / (2.0 * math.pi * tau)


def candidate_processes(capacitance_f: float | None, *,
                        thickness_cm: float | None,
                        area_cm2: float | None) -> list[Process] | None:
    """Every process whose range holds this capacitance, or ``None``.

    ``None`` means *could not judge* -- no capacitance, or the geometry that
    turns it into a comparable number is missing.  Not a guess at a typical
    pellet: a 10 µm film and a 1 mm pellet differ by a hundred in ``l/A``,
    which is two rows of the table (§0.4).
    """
    if capacitance_f is None or not _positive(capacitance_f):
        return None
    if not thickness_cm or not area_cm2 or not _positive(thickness_cm, area_cm2):
        return None
    per_length = capacitance_f * thickness_cm / area_cm2
    per_area = capacitance_f / area_cm2
    return [one for one in PROCESSES
            if one.holds(per_length if one.scaling == THICKNESS else per_area)]


@dataclass(frozen=True)
class ArcCapacitance:
    """One ``R ∥ CPE`` (or ``R ∥ C``) arc, read as a capacitor."""

    resistor: str
    element: str
    element_kind: str
    resistance_ohm: float
    #: ``Q`` for a CPE, ``C`` itself for a capacitor.
    q: float
    #: ``1.0`` for a capacitor.
    n: float
    capacitance_f: float | None
    peak_hz: float | None
    #: ``C · l/A`` -- the capacitance at a cell constant of 1 cm⁻¹.
    per_length: float | None
    #: ``C / A`` in F/cm².
    per_area: float | None
    #: Process keys the capacitance allows, high-frequency processes first.
    #: ``None`` is *could not judge*, and then ``reason`` says why.
    candidates: tuple[str, ...] | None
    reason: str = ""


def arc_capacitances(circuit: str | Circuit, values: Mapping[str, float], *,
                     thickness_cm: float | None = None,
                     area_cm2: float | None = None) -> list[ArcCapacitance]:
    """Every capacitive arc of a fitted circuit, in circuit order.

    Circuit order is frequency order after a fit (``fit_circuit`` sorts the
    arcs, highest frequency first), so the first entry is the arc a symmetric
    cell calls bulk.  Arcs whose numbers are missing from ``values`` are
    skipped rather than invented.
    """
    model = parse_circuit(circuit) if isinstance(circuit, str) else circuit
    out: list[ArcCapacitance] = []
    for resistor, element, kind in model.capacitive_arcs():
        if kind == "CPE":
            q, n = values.get(f"{element}_Q"), values.get(f"{element}_n")
        else:
            q, n = values.get(element), 1.0
        r = values.get(resistor)
        if r is None or q is None or n is None:
            continue
        r, q, n = float(r), float(q), float(n)
        capacitance = effective_capacitance(r, q, n)
        peak = peak_frequency(r, q, n)
        per_length = per_area = None
        if capacitance is not None and thickness_cm and area_cm2 \
                and _positive(thickness_cm, area_cm2):
            per_length = capacitance * thickness_cm / area_cm2
            per_area = capacitance / area_cm2
        reason = ""
        candidates: tuple[str, ...] | None = None
        if capacitance is None:
            reason = "R·Q·n 가 아크의 값이 아닙니다"
        elif n < LOWEST_N:
            reason = (f"n = {n:.2f} 는 반원이 아니라 확산에 가깝습니다 — "
                      f"커패시턴스로 읽지 않습니다")
        else:
            found = candidate_processes(capacitance, thickness_cm=thickness_cm,
                                        area_cm2=area_cm2)
            if found is None:
                reason = "두께·면적이 없어 어느 과정의 커패시턴스인지 못 봅니다"
            else:
                candidates = tuple(one.key for one in found)
        out.append(ArcCapacitance(
            resistor=resistor, element=element, element_kind=kind,
            resistance_ohm=r, q=q, n=n, capacitance_f=capacitance,
            peak_hz=peak, per_length=per_length, per_area=per_area,
            candidates=candidates, reason=reason))
    return out


# --------------------------------------------------------------------------
# which side of the pellet
# --------------------------------------------------------------------------

#: 두께를 가로지르는 과정 — 벌크.
BULK = "bulk"
#: 두께를 가로지르는 과정 — 입계.  면 위의 과정과 크기를 나눠 가질 수 있다
#: (얇은 펠릿의 1 µF/cm² 는 입계이자 전극 계면이다) — 그때도 이쪽이다: 모르는
#: 아크를 전해질에서 빼지 않는다 (ADR 0041).
BOUNDARY = "boundary"
#: 면 위의 과정**뿐** — 표면층, 전극 계면, 전기화학 반응.
FACE = "face"

#: 결정된 값도 표의 경계에서 이 배수 안쪽이면 어느 쪽인지 가르지 않는다.
#: 유효 커패시턴스 식 자체가 분포 가정이 틀리면 0.3–2 배 틀리고 (Hirschorn
#: 외, 2010: 표면 분포에 식 (18) 을 쓰면 −70 % ~ +100 %), 표의 범위는 자릿수
#: 규칙이다 (Irvine–Sinclair–West 의 표 1 은 "possible interpretation").
DETERMINED_SPREAD = 3.0
#: R 이나 Q 가 미결정이면 값이 몇 배 흔들린다 — Q 가 세 배면 C 는 3^{1/n} 배
#: (n = 0.87 에서 3.5 배).  식의 흔들림까지 더해 한 자릿수.
UNDETERMINED_SPREAD = 10.0


def _side(per_length: float, per_area: float) -> str | None:
    keys = {one.key for one in PROCESSES
            if one.holds(per_length if one.scaling == THICKNESS else per_area)}
    if "bulk" in keys:
        return BULK
    if "grain_boundary" in keys:
        return BOUNDARY
    return FACE if keys else None


def size_class(arc: ArcCapacitance, *, spread: float = 1.0) -> str | None:
    """Which side of the pellet an arc's capacitance puts it on.

    :data:`BULK` / :data:`BOUNDARY` -- across the thickness, the electrolyte;
    :data:`FACE` -- only processes on a face (surface layer, electrode
    interface, reaction), not the electrolyte.  ``None`` is *not judged*: no
    candidates, or the side changes when the capacitance moves ``spread``
    times either way (:func:`spread_for`).

    Coarser than :func:`candidate_processes` on purpose.  What a conductivity
    needs is not "grain boundary or interface" but "is this arc the
    electrolyte, and can it be the bulk" -- and those answers survive
    overlapping ranges that the name does not.
    """
    if arc.candidates is None or arc.per_length is None or arc.per_area is None:
        return None
    sides = {_side(arc.per_length * k, arc.per_area * k)
             for k in (1.0 / spread, 1.0, spread)}
    side = sides.pop()
    return side if not sides else None


def reachable(arc: ArcCapacitance, *, spread: float = 1.0) -> tuple[str, ...] | None:
    """Every process the arc's capacitance reaches when it moves up to
    ``spread`` times either way -- the processes it **can** be.  ``None`` is
    *not judged*, as in :func:`size_class`.

    A name outside this set is ruled out even by the formula's own
    uncertainty, which is when ADR 0047 renames the arc.  An interval, not
    three samples: a range narrower than the spread could fall between them.
    """
    if arc.candidates is None or arc.per_length is None or arc.per_area is None:
        return None
    out: list[str] = []
    for one in PROCESSES:
        value = arc.per_length if one.scaling == THICKNESS else arc.per_area
        low, high = value / spread, value * spread
        if (one.high is None or low < one.high) and (one.low is None or high >= one.low):
            out.append(one.key)
    return tuple(out)


def spread_for(arc: ArcCapacitance, undetermined: Iterable[str]) -> float:
    """:data:`UNDETERMINED_SPREAD` when the arc's ``R`` or ``Q`` (``C``) was
    not determined, else :data:`DETERMINED_SPREAD`.

    An undetermined ``n`` alone does not widen it: at the upper bound it is an
    ideal capacitor (``C = Q``), and ±0.05 on ``n`` moves ``C`` by at most
    about two times.  실측 B14 #9: "입계" 아크는 n 만 미결정(상한)인 이상적
    축전기였다.
    """
    shaky = set(undetermined)
    names = (arc.resistor, f"{arc.element}_Q", arc.element)
    return UNDETERMINED_SPREAD if shaky.intersection(names) else DETERMINED_SPREAD
