"""Cycle-to-cycle differences — what one cycle lost against the one before it.

Retention answers "how much is left against cycle 3".  This answers "how much
went *this* cycle", and the two are not interchangeable: a cell can hold a
flat 92 % retention for forty cycles and then drop 4 % in one, and on a
retention column that shows as 92, 92, 92, 88 -- the same four-point step that
formation makes at the start, and easy to read past.  As a per-cycle column the
one bad cycle is the only non-trivial number on the page.

Three rules decide every value here, and all three exist because breaking them
produces a plausible wrong number rather than an error.

**Never differ against an incomplete cycle.**  A running cell's newest cycle is
truncated mid-branch, so its capacity is whatever had accumulated when the file
was written (CLAUDE.md §3).  Subtracting that gives a large negative step that
looks like sudden death.  Incomplete cycles get no delta *and* are never used
as somebody else's base.

**Say how far back the base is.**  Cycles go missing -- a rate test skips, a
continuation file starts at 201, an incomplete cycle is excluded by the rule
above.  Then "the previous complete cycle" is five cycles back and the step is
five cycles' worth of fade presented as one.  ``span`` carries that distance so
a reader (and a CSV) can tell 1 from 5, and ``per_cycle`` divides by it.

**A percentage needs a non-zero base.**  A cycle whose base is 0 mAh has an
infinite relative change, not a large one.  That comes back as ``None``.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["CycleDelta", "previous_cycle_deltas"]


@dataclass
class CycleDelta:
    """One cycle's step against the most recent complete cycle before it."""

    cycle_number: int
    #: Which cycle this was measured against; None when there is no base yet.
    previous_cycle: int | None = None
    #: value(this) - value(previous), in whatever unit went in.
    delta: float | None = None
    #: The same step as a percentage of the base.  None when the base is zero.
    delta_pct: float | None = None
    #: Cycle numbers between this one and its base.  1 when adjacent.
    span: int = 0
    #: ``delta / span`` -- the honest per-cycle rate when cycles are missing.
    per_cycle: float | None = None
    #: Why there is no delta, when there is none.  Empty when there is one.
    reason: str = ""

    @property
    def usable(self) -> bool:
        return self.delta is not None


def previous_cycle_deltas(
    cycle_numbers,
    values,
    complete=None,
) -> list[CycleDelta]:
    """Step from each cycle to the most recent complete cycle before it.

    Takes plain sequences rather than records so the database never reaches
    this far down (the same boundary ``knee`` and ``health`` keep).  Order is
    preserved: result[i] describes cycle_numbers[i].

    ``values`` may contain ``None`` -- a cycle with no discharge branch, say.
    Those neither receive a delta nor become a base, exactly like an incomplete
    cycle, because a missing measurement is not a measurement of zero.
    """
    numbers = list(cycle_numbers)
    data = list(values)
    if len(numbers) != len(data):
        raise ValueError(
            f"{len(numbers)} cycle numbers but {len(data)} values")
    flags = [True] * len(numbers) if complete is None else list(complete)
    if len(flags) != len(numbers):
        raise ValueError(
            f"{len(numbers)} cycle numbers but {len(flags)} complete flags")

    out: list[CycleDelta] = []
    base_number: int | None = None
    base_value: float | None = None

    # strict=True 는 여기서 불필요하다 — 길이는 위에서 이미 맞췄고,
    # 안 맞으면 어느 행이 밀렸는지 말해 주는 위쪽 오류가 낫다.
    for number, value, is_complete in zip(numbers, data, flags):  # noqa: B905
        entry = CycleDelta(cycle_number=number)
        if not is_complete:
            entry.reason = "cycle is still running"
        elif value is None:
            entry.reason = "no value for this cycle"
        elif base_value is None:
            entry.reason = "no earlier complete cycle to compare with"
        else:
            entry.previous_cycle = base_number
            entry.delta = value - base_value
            # Distance in *cycle numbers*, not in list positions: the rows in
            # between may simply be absent from the file, and the reader needs
            # to know the step covers that gap.
            entry.span = max(1, number - (base_number or number))
            entry.per_cycle = entry.delta / entry.span
            if base_value:
                entry.delta_pct = 100.0 * entry.delta / base_value
            # base_value == 0 leaves delta_pct None on purpose: the relative
            # change from nothing is undefined, not enormous.
        out.append(entry)

        # Only a complete cycle carrying a real value may anchor the next step.
        if is_complete and value is not None:
            base_number, base_value = number, value
    return out
