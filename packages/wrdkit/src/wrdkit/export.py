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
from .normalize import Basis, ResolvedCell, normalize_capacity
from .wrd import WrdFile

__all__ = [
    "write_raw_csv", "write_cycles_csv", "write_profiles_csv",
    "raw_csv_string", "cycles_csv_string", "profiles_csv_string", "write_xlsx",
]

_UNIX_OFFSET = 62_135_596_800.0


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
    header = derived + [n for n in names if n not in ("date_time", "test_time", "step_time", "cycle_time")]
    writer.writerow(header)

    timestamps = wrd.timestamps() if "date_time" in data else None
    test_s = wrd.seconds("test_time") if "test_time" in data else None
    step_s = wrd.seconds("step_time") if "step_time" in data else None
    cycle_s = wrd.seconds("cycle_time") if "cycle_time" in data else None

    body = [n for n in header if n not in derived]
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


def write_cycles_csv(cycles: Iterable[CycleSummary], cell: ResolvedCell,
                     stream: TextIO, *, basis: str = Basis.ABSOLUTE,
                     include_absolute: bool = True) -> None:
    """One row per cycle, capacities expressed in *basis*."""
    cycles = list(cycles)
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
        charge = normalize_capacity(cycle.charge_capacity_mah, cell, usable)
        discharge = normalize_capacity(cycle.discharge_capacity_mah, cell, usable)
        row = [cycle.cycle_number, f"{charge:.6g}", f"{discharge:.6g}",
               _fmt(cycle.coulombic_efficiency)]
        if include_absolute and usable != Basis.ABSOLUTE:
            row += [f"{cycle.charge_capacity_mah:.6g}", f"{cycle.discharge_capacity_mah:.6g}"]
        row += [
            f"{cycle.charge_energy_wh * 1000:.6g}",
            f"{cycle.discharge_energy_wh * 1000:.6g}",
            _fmt(cycle.energy_efficiency),
            _fmt(cycle.mean_charge_voltage), _fmt(cycle.mean_discharge_voltage),
            _fmt(cycle.voltage_hysteresis), _fmt(cycle.voltage_max), _fmt(cycle.voltage_min),
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
