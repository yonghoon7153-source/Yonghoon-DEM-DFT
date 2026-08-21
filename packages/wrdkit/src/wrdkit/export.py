"""Write parsed data out in the shapes a battery lab pastes into Origin.

Three tables, because three different questions get asked of the same file:

``raw``       every sample, with ticks converted to seconds and a readable
              timestamp -- the direct replacement for hand-exporting from
              Smart Interface;
``cycles``    one row per cycle with capacities in the chosen basis -- what
              goes into a retention or coulombic-efficiency plot;
``profiles``  capacity/voltage column pairs per selected cycle, side by side
              -- the layout Origin wants for an overlay plot.
"""

from __future__ import annotations

import csv
import datetime
import io
from collections.abc import Iterable, Sequence
from typing import TextIO

import numpy as np

from .cycles import CycleSummary, Profile
from .ica import DifferentialCapacity
from .normalize import Basis, ResolvedCell, normalize_capacity
from .wrd import WrdFile

__all__ = [
    "write_raw_csv", "write_cycles_csv", "write_profiles_csv", "write_dqdv_csv",
    "raw_csv_string", "cycles_csv_string", "profiles_csv_string",
    "dqdv_csv_string", "write_xlsx",
]

_UNIX_OFFSET = 62_135_596_800.0

#: Raw columns whose unit is decided per file by the ``UnitCoulomb`` flag,
#: as ``(flag off, flag on)``.  The raw table dumps them in the file's own
#: units, so without a tag an Ah file and a C file produce identical headers
#: and a reader who assumes Ah is off by 3600.
_FILE_DEPENDENT_UNITS = {
    "charge_q": ("Ah", "C"),
    "discharge_q": ("Ah", "C"),
    "charge_e": ("Wh", "J"),
    "discharge_e": ("Wh", "J"),
}


def _format_timestamp(seconds: float) -> str:
    try:
        return datetime.datetime.utcfromtimestamp(seconds).isoformat(sep=" ", timespec="milliseconds")
    except (OverflowError, OSError, ValueError):
        return ""


def write_raw_csv(wrd: WrdFile, stream: TextIO, *, columns: Sequence[str] | None = None) -> None:
    """Every sample, one row per line, with derived time columns up front."""
    data = wrd.data
    names = list(columns) if columns else list(data)
    writer = csv.writer(stream, lineterminator="\n")

    derived = ["timestamp", "test_time_s", "step_time_s", "cycle_time_s"]
    body = [n for n in names if n not in ("date_time", "test_time", "step_time", "cycle_time")]
    header = derived + [_raw_label(n, wrd) for n in body]
    writer.writerow(header)

    timestamps = wrd.timestamps() if "date_time" in data else None
    test_s = wrd.seconds("test_time") if "test_time" in data else None
    step_s = wrd.seconds("step_time") if "step_time" in data else None
    cycle_s = wrd.seconds("cycle_time") if "cycle_time" in data else None

    columns_out = [data[n] for n in body]

    for i in range(len(wrd)):
        row = [
            _format_timestamp(float(timestamps[i])) if timestamps is not None else "",
            f"{test_s[i]:.4f}" if test_s is not None else "",
            f"{step_s[i]:.4f}" if step_s is not None else "",
            f"{cycle_s[i]:.4f}" if cycle_s is not None else "",
        ]
        for values in columns_out:
            value = values[i]
            row.append(f"{value:.10g}" if isinstance(value, (float, np.floating)) else value)
        writer.writerow(row)


def _raw_label(name: str, wrd: WrdFile) -> str:
    """Column header for the raw table, carrying the unit when it can vary."""
    choices = _FILE_DEPENDENT_UNITS.get(name)
    if choices is None:
        return name
    declared = next((c.unit for c in wrd.metadata.columns if c.name == name and c.unit), "")
    return f"{name} ({declared or choices[1 if wrd.metadata.unit_coulomb else 0]})"


def write_cycles_csv(cycles: Iterable[CycleSummary], cell: ResolvedCell,
                     stream: TextIO, *, basis: str = Basis.ABSOLUTE,
                     include_absolute: bool = True,
                     include_incomplete: bool = False) -> None:
    """One row per cycle, capacities expressed in *basis*.

    Incomplete cycles are left out by default.  The last cycle of a running
    cell is cut off mid-step, so its capacity is whatever had accumulated when
    the file was written -- a number that looks like a measurement and is not
    one (non-negotiable: never report it).  The API already excluded them; this
    writer did not, so `wrdkit convert` and the Python API handed out a
    spreadsheet whose final row understates the cell.

    Pass ``include_incomplete=True`` to keep those rows for inspection.  They
    come back with their capacity, energy and efficiency columns blank rather
    than filled, because a partial number in a numeric column is read as a
    measurement no matter what the ``complete`` column says.
    """
    cycles = list(cycles)
    if not include_incomplete:
        cycles = [c for c in cycles if c.complete]
    writer = csv.writer(stream, lineterminator="\n")

    usable = basis if cell.divisor(basis) else Basis.ABSOLUTE
    unit = usable.replace("mAh", "").strip("/") or ""
    suffix = f" ({usable})"

    header = ["cycle", "charge_capacity" + suffix, "discharge_capacity" + suffix,
              "coulombic_efficiency (%)"]
    if include_absolute and usable != Basis.ABSOLUTE:
        header += ["charge_capacity (mAh)", "discharge_capacity (mAh)"]
    header += ["charge_energy (mWh)", "discharge_energy (mWh)", "energy_efficiency (%)",
               "mean_charge_voltage (V)", "mean_discharge_voltage (V)",
               "voltage_hysteresis (V)", "v_max (V)", "v_min (V)",
               "duration (h)", "points", "complete"]
    writer.writerow(header)
    del unit

    for cycle in cycles:
        # 무엇을 비우는가.  잘린 사이클에서 *측정처럼 보이는* 값은 전부 비운다:
        # 용량과 에너지는 파일이 끝난 순간까지 쌓인 부분값이고, 효율은 그 둘의
        # 비이며, 평균 전압은 E/Q 라 마찬가지다.  이력은 두 평균의 차라 역시
        # 부분값이고, v_max/v_min 은 아직 도달하지 못한 극값이다.
        #
        # 남기는 것: 사이클 번호, 시간, 점 수, complete 칸.  이것들은 파일에
        # 무엇이 들어 있는지를 정직하게 말할 뿐 셀의 성능을 주장하지 않는다 —
        # 진단하려고 opt-in 한 사람이 보려는 것이 바로 그것이다.
        blank = not cycle.complete
        charge = normalize_capacity(cycle.charge_capacity_mah, cell, usable)
        discharge = normalize_capacity(cycle.discharge_capacity_mah, cell, usable)
        row = [cycle.cycle_number,
               "" if blank else f"{charge:.6g}",
               "" if blank else f"{discharge:.6g}",
               "" if blank else _fmt(cycle.coulombic_efficiency)]
        if include_absolute and usable != Basis.ABSOLUTE:
            row += ["", ""] if blank else [
                f"{cycle.charge_capacity_mah:.6g}",
                f"{cycle.discharge_capacity_mah:.6g}"]
        row += [
            "" if blank else f"{cycle.charge_energy_wh * 1000:.6g}",
            "" if blank else f"{cycle.discharge_energy_wh * 1000:.6g}",
            "" if blank else _fmt(cycle.energy_efficiency),
            "" if blank else _fmt(cycle.mean_charge_voltage),
            "" if blank else _fmt(cycle.mean_discharge_voltage),
            "" if blank else _fmt(cycle.voltage_hysteresis),
            "" if blank else _fmt(cycle.voltage_max),
            "" if blank else _fmt(cycle.voltage_min),
            f"{cycle.duration_s / 3600:.4f}", cycle.n_points,
            "yes" if cycle.complete else "no",
        ]
        writer.writerow(row)


def write_profiles_csv(profiles: Sequence[Profile], cell: ResolvedCell,
                       stream: TextIO, *, basis: str = Basis.ABSOLUTE) -> None:
    """Capacity/voltage column pairs, one pair per profile, side by side."""
    writer = csv.writer(stream, lineterminator="\n")
    usable = basis if cell.divisor(basis) else Basis.ABSOLUTE

    header: list[str] = []
    columns: list[np.ndarray] = []
    for profile in profiles:
        tag = f"cycle{profile.cycle_number}_{profile.branch}"
        header += [f"{tag}_capacity ({usable})", f"{tag}_voltage (V)"]
        columns += [normalize_capacity(profile.capacity_mah, cell, usable), profile.voltage]

    writer.writerow(header or ["capacity", "voltage"])
    depth = max((len(c) for c in columns), default=0)
    for i in range(depth):
        row = []
        for values in columns:
            row.append(f"{values[i]:.6g}" if i < len(values) else "")
        writer.writerow(row)


def write_dqdv_csv(curves: Sequence[DifferentialCapacity], cell: ResolvedCell,
                   stream: TextIO, *, basis: str = Basis.ABSOLUTE) -> None:
    """Voltage/dQdV column pairs, one pair per curve, side by side.

    Laid out like the profile CSV so the two open the same way in the same
    spreadsheet -- somebody comparing a capacity curve against its derivative
    should not have to learn a second layout.

    Unusable curves are written as an empty pair rather than skipped.  A
    reader counting columns against the cycles they asked for would otherwise
    silently line up cycle 51's data under cycle 30's header.
    """
    writer = csv.writer(stream, lineterminator="\n")
    usable = basis if cell.divisor(basis) else Basis.ABSOLUTE
    # mAh/V divided by grams is (mAh/g)/V.  The same divisor, one more slash.
    unit = f"{usable}/V"

    header: list[str] = []
    columns: list[np.ndarray] = []
    for curve in curves:
        tag = f"cycle{curve.cycle_number}_{curve.branch}"
        header += [f"{tag}_voltage (V)", f"{tag}_dQdV ({unit})"]
        columns += [curve.voltage, normalize_capacity(curve.dq_dv, cell, usable)]

    writer.writerow(header or ["voltage", "dQdV"])
    depth = max((len(c) for c in columns), default=0)
    for i in range(depth):
        row = []
        for values in columns:
            row.append(f"{values[i]:.6g}" if i < len(values) else "")
        writer.writerow(row)


def _fmt(value: float | None) -> str:
    return "" if value is None else f"{value:.6g}"


def raw_csv_string(wrd: WrdFile, **kwargs) -> str:
    buffer = io.StringIO()
    write_raw_csv(wrd, buffer, **kwargs)
    return buffer.getvalue()


def cycles_csv_string(cycles, cell, **kwargs) -> str:
    buffer = io.StringIO()
    write_cycles_csv(cycles, cell, buffer, **kwargs)
    return buffer.getvalue()


def profiles_csv_string(profiles, cell, **kwargs) -> str:
    buffer = io.StringIO()
    write_profiles_csv(profiles, cell, buffer, **kwargs)
    return buffer.getvalue()


def dqdv_csv_string(curves, cell, **kwargs) -> str:
    buffer = io.StringIO()
    write_dqdv_csv(curves, cell, buffer, **kwargs)
    return buffer.getvalue()


def write_xlsx(path, wrd: WrdFile, cycles: Sequence[CycleSummary],
               profiles: Sequence[Profile], cell: ResolvedCell, *,
               basis: str = Basis.ABSOLUTE, include_raw: bool = False) -> None:
    """Write a multi-sheet workbook (metadata / cycles / profiles [/ raw]).

    Requires ``openpyxl``; CSV export has no third-party dependency and stays
    the guaranteed path.
    """
    try:
        from openpyxl import Workbook
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("xlsx export needs openpyxl (pip install openpyxl)") from exc

    book = Workbook()
    meta_sheet = book.active
    meta_sheet.title = "metadata"
    metadata = wrd.metadata
    rows = [
        ("source file", metadata.source_name),
        ("instrument", f"{metadata.model} ({metadata.serial_no})"),
        ("channel", metadata.channel),
        ("start time", metadata.start_time.isoformat(sep=" ") if metadata.start_time else ""),
        ("end time", metadata.end_time.isoformat(sep=" ") if metadata.end_time else ""),
        ("samples", metadata.row_count),
        ("cycles in file", len(cycles)),
        ("active mass (mg)", (cell.active_mass_g or 0) * 1000 or ""),
        ("electrode area (cm2)", cell.area_cm2 or ""),
        ("loading (mg/cm2)", cell.loading_mg_cm2 or ""),
        ("nominal capacity (mAh)", cell.nominal_capacity_mah or ""),
        ("capacity basis", basis),
        # The raw sheet keeps the file's own units; say which they are.
        ("raw capacity unit", "C" if metadata.unit_coulomb else "Ah"),
    ]
    if metadata.schedule:
        schedule = metadata.schedule
        rows += [
            ("schedule", schedule.source_path or ""),
            ("upper cutoff (V)", schedule.upper_cutoff_v or ""),
            ("lower cutoff (V)", schedule.lower_cutoff_v or ""),
            ("planned cycles", schedule.planned_cycles or ""),
        ]
        rows += [(f"step {step.index}", step.describe()) for step in schedule.steps]
    for row in rows:
        meta_sheet.append(list(row))

    _sheet_from_csv(book, "cycles", cycles_csv_string(cycles, cell, basis=basis))
    if profiles:
        _sheet_from_csv(book, "profiles", profiles_csv_string(profiles, cell, basis=basis))
    if include_raw:
        _sheet_from_csv(book, "raw", raw_csv_string(wrd))

    book.save(path)


def _sheet_from_csv(book, title: str, text: str) -> None:
    sheet = book.create_sheet(title)
    for row in csv.reader(io.StringIO(text)):
        sheet.append([_maybe_number(v) for v in row])


def _maybe_number(value: str):
    if value in ("", "yes", "no"):
        return value
    try:
        return float(value) if ("." in value or "e" in value.lower()) else int(value)
    except ValueError:
        return value
