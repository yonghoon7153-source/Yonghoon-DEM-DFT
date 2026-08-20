"""Decode the WonATech test schedule embedded in a ``.wrd`` header.

The schedule is what the operator drew in Smart Interface's Schedule Editor:
an ordered list of steps (rest / CC / CCCV / ...) with cut-off conditions and
loop counts.  Reading it lets the app pre-fill the experiment conditions --
C-rate, cut-off voltages, nominal capacity -- instead of asking the user to
retype what the instrument already knows.

Enum values were established by decoding a reference file and cross-checking
each step against the measured current and voltage traces it produced; see
``docs/raw/specs/wrd-binary-format.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .nrbf import NrbfObject, NrbfStream, resolve

__all__ = [
    "ControlType", "CutoffType", "CutoffCondition", "Cutoff", "ScheduleStep",
    "Schedule", "TICKS_PER_SECOND", "read_schedule",
]

#: .NET stores durations as ticks of 100 ns.
TICKS_PER_SECOND = 10_000_000


class ControlType:
    """``WbcsFile.Sequence.eCtrlType`` values seen in the wild."""

    CC = 0
    CV = 1
    REST = 7
    CCCV = 13

    NAMES = {0: "CC", 1: "CV", 7: "Rest", 13: "CCCV"}

    @classmethod
    def name(cls, value: int) -> str:
        return cls.NAMES.get(value, f"Type{value}")


class CutoffType:
    """``WbcsFile.Sequence.eCutoffType`` values seen in the wild."""

    TIME = 0
    VOLTAGE = 1
    CURRENT = 15

    NAMES = {0: "time", 1: "voltage", 15: "current"}

    @classmethod
    def name(cls, value: int) -> str:
        return cls.NAMES.get(value, f"type{value}")


class CutoffCondition:
    """Comparison direction attached to a cut-off."""

    RISING = 0   # trigger when the signal reaches/exceeds the value
    FALLING = 1  # trigger when the signal drops to/below the value

    NAMES = {0: ">=", 1: "<="}

    @classmethod
    def name(cls, value: int) -> str:
        return cls.NAMES.get(value, "?")


@dataclass
class Cutoff:
    """One termination condition for a step."""

    kind: str
    condition: str
    value: float
    seconds: float

    def describe(self) -> str:
        if self.kind == "time":
            return f"time >= {self.seconds:g} s"
        unit = "V" if self.kind == "voltage" else "A"
        return f"{self.kind} {self.condition} {self.value:g} {unit}"


@dataclass
class ScheduleStep:
    """One row of the Schedule Editor table."""

    index: int
    name: str
    control: str
    control_raw: int
    current_a: float | None = None
    voltage_limit_v: float | None = None
    taper_current_a: float | None = None
    cutoffs: list[Cutoff] = field(default_factory=list)
    loop_count: int = 1
    loop_target: str | None = None
    sampling_interval_s: float | None = None

    @property
    def direction(self) -> str:
        """``charge``, ``discharge`` or ``rest`` inferred from the setpoint."""
        if self.control == "Rest":
            return "rest"
        if self.current_a is None:
            return "unknown"
        if self.current_a > 0:
            return "charge"
        if self.current_a < 0:
            return "discharge"
        return "rest"

    def describe(self) -> str:
        parts = [f"{self.index}: {self.control}"]
        if self.current_a:
            parts.append(f"{self.current_a * 1000:+.4g} mA")
        if self.voltage_limit_v:
            parts.append(f"-> {self.voltage_limit_v:g} V")
        if self.taper_current_a:
            parts.append(f"taper {self.taper_current_a * 1000:.4g} mA")
        if self.cutoffs:
            parts.append("[" + "; ".join(c.describe() for c in self.cutoffs) + "]")
        if self.loop_target and self.loop_count > 1:
            parts.append(f"loop -> {self.loop_target} x{self.loop_count}")
        return " ".join(parts)


@dataclass
class Schedule:
    """The decoded schedule plus the conditions we can infer from it."""

    version: str | None
    source_path: str | None
    steps: list[ScheduleStep] = field(default_factory=list)

    # -- inferred experiment conditions ------------------------------------
    @property
    def upper_cutoff_v(self) -> float | None:
        """Highest charge termination voltage in the schedule."""
        candidates = [s.voltage_limit_v for s in self.steps if s.voltage_limit_v]
        for step in self.steps:
            if step.direction != "charge":
                continue
            candidates += [c.value for c in step.cutoffs if c.kind == "voltage"]
        return max(candidates) if candidates else None

    @property
    def lower_cutoff_v(self) -> float | None:
        """Lowest discharge termination voltage in the schedule."""
        candidates: list[float] = []
        for step in self.steps:
            if step.direction != "discharge":
                continue
            candidates += [c.value for c in step.cutoffs if c.kind == "voltage"]
        return min(candidates) if candidates else None

    @property
    def cycling_current_a(self) -> float | None:
        """Charge current of the looped (i.e. long-run) part of the schedule.

        Formation steps run once; the cycling current is the one inside the
        loop, which is what the reported C-rate refers to.
        """
        looped = self._looped_step_names()
        currents = [
            abs(s.current_a) for s in self.steps
            if s.current_a and s.direction == "charge" and (not looped or s.name in looped)
        ]
        return max(currents) if currents else None

    @property
    def formation_current_a(self) -> float | None:
        looped = self._looped_step_names()
        currents = [
            abs(s.current_a) for s in self.steps
            if s.current_a and s.direction == "charge" and s.name not in looped
        ]
        return max(currents) if currents else None

    @property
    def planned_cycles(self) -> int | None:
        counts = [s.loop_count for s in self.steps if s.loop_count and s.loop_count > 1]
        return max(counts) if counts else None

    @property
    def sampling_interval_s(self) -> float | None:
        """Logging interval of the looped charge/discharge steps.

        Rest steps normally log far more slowly, so the overall minimum would
        misreport the resolution of the profile the user actually plots.
        """
        looped = self._looped_step_names()
        values = [
            s.sampling_interval_s for s in self.steps
            if s.sampling_interval_s and s.direction in ("charge", "discharge")
            and (not looped or s.name in looped)
        ]
        if not values:
            values = [s.sampling_interval_s for s in self.steps if s.sampling_interval_s]
        return min(values) if values else None

    def _looped_step_names(self) -> set[str]:
        """Names of the steps inside the largest loop of the schedule."""
        best: tuple[int, set[str]] = (0, set())
        by_name = {s.name: i for i, s in enumerate(self.steps)}
        for i, step in enumerate(self.steps):
            if not step.loop_target or step.loop_count <= 1:
                continue
            start = by_name.get(step.loop_target)
            if start is None or start > i:
                continue
            if step.loop_count > best[0]:
                best = (step.loop_count, {s.name for s in self.steps[start:i + 1]})
        return best[1]

    def nominal_capacity_ah(self, c_rate: float | None = None) -> float | None:
        """Capacity the operator dialled in, back-calculated from the current.

        The Schedule Editor computes step currents as ``C-rate x capacity``.
        With the C-rate known (or assumed to be a round number), the nominal
        capacity follows.
        """
        current = self.cycling_current_a
        if not current:
            return None
        if c_rate:
            return current / c_rate
        rate = self.infer_c_rate()
        return current / rate if rate else None

    def infer_c_rate(self) -> float | None:
        """Guess the cycling C-rate from the formation/cycling current ratio.

        Formation is conventionally run at a round fraction of the cycling
        rate.  When there is no formation step to compare against we cannot
        infer anything and return ``None`` rather than guessing.
        """
        cycling = self.cycling_current_a
        formation = self.formation_current_a
        if not cycling or not formation:
            return None
        ratio = cycling / formation
        for rate, form_rate in ((0.2, 0.1), (0.5, 0.1), (1.0, 0.1), (0.1, 0.05),
                                (0.33, 0.1), (2.0, 0.1)):
            if abs(ratio - rate / form_rate) < 0.05 * (rate / form_rate):
                return rate
        return None

    def describe(self) -> list[str]:
        return [s.describe() for s in self.steps]


def _member(stream: NrbfStream, obj: NrbfObject | None, name: str) -> Any:
    """Read a member by name, whether it is an auto-property or a plain field.

    C# auto-properties serialize as ``<Name>k__BackingField``; plain fields
    keep their own name.
    """
    if obj is None:
        return None
    members = obj.members
    key = f"<{name}>k__BackingField"
    if key not in members:
        key = name
    return resolve(stream, members.get(key))


def _list_items(stream: NrbfStream, obj: NrbfObject | None) -> list[Any]:
    """Unwrap ``System.Collections.Generic.List<T>`` to a Python list."""
    if obj is None:
        return []
    items = resolve(stream, obj.members.get("_items")) or []
    size = obj.members.get("_size") or 0
    return [resolve(stream, item) for item in items[:size]]


def _enum(stream: NrbfStream, obj: NrbfObject | None, name: str) -> int | None:
    value = _member(stream, obj, name)
    if isinstance(value, NrbfObject):
        return value.members.get("value__")
    return value if isinstance(value, int) else None


def _read_cutoff(stream: NrbfStream, obj: NrbfObject | None) -> Cutoff | None:
    if obj is None:
        return None
    kind = CutoffType.name(_enum(stream, obj, "Type") or 0)
    condition = CutoffCondition.name(_enum(stream, obj, "Condition") or 0)
    ticks = _member(stream, obj, "TimeValue") or 0
    return Cutoff(kind, condition, _member(stream, obj, "Value") or 0.0,
                  ticks / TICKS_PER_SECOND)


def read_schedule(stream: NrbfStream, header: NrbfObject) -> Schedule | None:
    """Extract the :class:`Schedule` from a parsed ``DataFileHeader``."""
    seq_set = _member(stream, header, "SeqDataSet")
    if seq_set is None:
        return None
    schedule = Schedule(
        version=_member(stream, seq_set, "Version"),
        source_path=_member(stream, seq_set, "FileName"),
    )
    sequences = _list_items(stream, _member(stream, seq_set, "SeqDataList"))
    if not sequences:
        return schedule
    sch_data = _member(stream, sequences[0], "SchData")
    steps = _list_items(stream, _member(stream, sch_data, "SchStepList"))

    for index, raw_step in enumerate(steps):
        control = _member(stream, raw_step, "Control")
        control_raw = _enum(stream, control, "Type") or 0
        control_name = ControlType.name(control_raw)
        value = _member(stream, control, "Value")
        step = ScheduleStep(
            index=index,
            name=_member(stream, raw_step, "Name") or f"step{index}",
            control=control_name,
            control_raw=control_raw,
        )
        if control_raw != ControlType.REST:
            step.current_a = value
        if control_raw == ControlType.CCCV:
            step.voltage_limit_v = _member(stream, control, "Value2") or None
            step.taper_current_a = _member(stream, control, "Value3") or None

        loop = _member(stream, control, "Loop")
        step.loop_count = _member(stream, loop, "Count") or 1

        for conds in _list_items(stream, _member(stream, raw_step, "CutOffCondsList")):
            turn = _member(stream, conds, "TurnStep")
            if turn and turn != "Next Step":
                step.loop_target = turn
            # The second slot is only armed when And2 is set; otherwise the
            # instrument leaves a stale 30 s time value in it.
            tags = ("CutOff1", "CutOff2") if _member(stream, conds, "And2") else ("CutOff1",)
            for tag in tags:
                cutoff = _read_cutoff(stream, _member(stream, conds, tag))
                if cutoff is None or (cutoff.kind == "time" and cutoff.seconds == 0):
                    continue
                # A CV taper cut-off records 0 A and defers to the control's
                # own taper setpoint.
                if cutoff.kind == "current" and not cutoff.value and step.taper_current_a:
                    cutoff.value = step.taper_current_a
                    cutoff.condition = "<="
                step.cutoffs.append(cutoff)

        for samp in _list_items(stream, _member(stream, raw_step, "SampCondList")):
            if _member(stream, samp, "Enable") and _enum(stream, samp, "Type") == 0:
                ticks = _member(stream, samp, "TimeValue") or 0
                step.sampling_interval_s = ticks / TICKS_PER_SECOND
                break

        schedule.steps.append(step)

    return schedule
