"""``wrdkit`` command line: inspect a ``.wrd`` and convert it without a browser.

    wrdkit info cell.wrd
    wrdkit convert cell.wrd --out-dir ./csv --mass 31.6 --wt 80 --diameter 13
    wrdkit cycles cell.wrd --basis mAh/g --mass 31.6 --wt 80
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .cycles import extract_profile, summarize_cycles
from .export import write_cycles_csv, write_profiles_csv, write_raw_csv
from .normalize import BASES, Basis, CellSpec
from .wrd import WrdError, read_wrd


def _cell_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group("cell spec")
    group.add_argument("--mass", type=float, metavar="MG",
                       help="total electrode mass in mg")
    group.add_argument("--active-mass", type=float, metavar="MG",
                       help="active material mass in mg (overrides --mass/--wt)")
    group.add_argument("--wt", type=float, metavar="PCT", default=None,
                       help="active material content in wt%%")
    group.add_argument("--collector-mass", type=float, metavar="MG",
                       help="current collector mass in mg, subtracted from --mass")
    group.add_argument("--area", type=float, metavar="CM2", help="electrode area in cm2")
    group.add_argument("--diameter", type=float, metavar="MM",
                       help="electrode diameter in mm (e.g. 13 for a 13pi punch)")
    group.add_argument("--thickness", type=float, metavar="UM", help="electrode thickness in um")
    group.add_argument("--specific-capacity", type=float, metavar="MAH_G",
                       help="nominal specific capacity in mAh/g")


def _cell_from_args(args) -> CellSpec:
    return CellSpec(
        active_mass_mg=args.active_mass,
        total_mass_mg=args.mass,
        current_collector_mass_mg=args.collector_mass,
        active_wt_percent=args.wt,
        area_cm2=args.area,
        diameter_mm=args.diameter,
        thickness_um=args.thickness,
        nominal_specific_capacity_mah_g=args.specific_capacity,
    )


def _print_info(path: Path) -> int:
    wrd = read_wrd(path)
    metadata = wrd.metadata
    print(f"file        {metadata.source_name}  ({metadata.file_size / 1e6:.2f} MB)")
    print(f"instrument  {metadata.model} sn={metadata.serial_no} ch={metadata.channel}")
    print(f"software    app {metadata.app_version} / firmware {metadata.firmware_version}")
    print(f"started     {metadata.start_time}")
    print(f"ended       {metadata.end_time}")
    print(f"samples     {metadata.row_count:,} rows, {len(metadata.columns)} columns")
    if metadata.trailing_bytes:
        print(f"warning     {metadata.trailing_bytes} trailing bytes were not parsed")
    if metadata.instrument_path:
        print(f"saved as    {metadata.instrument_path}")

    schedule = metadata.schedule
    if schedule:
        print(f"\nschedule    {schedule.source_path or '(embedded)'}")
        for line in schedule.describe():
            print(f"  {line}")
        rate = schedule.infer_c_rate()
        nominal = schedule.nominal_capacity_ah()
        print(f"  cutoffs {schedule.lower_cutoff_v} - {schedule.upper_cutoff_v} V"
              f" | planned {schedule.planned_cycles} cycles"
              + (f" | {rate:g}C" if rate else "")
              + (f" | nominal {nominal * 1000:.4g} mAh" if nominal else ""))

    cycles = summarize_cycles(wrd)
    complete = [c for c in cycles if c.complete]
    print(f"\ncycles      {len(cycles)} in file ({len(complete)} complete)")
    if complete:
        first, last = complete[0], complete[-1]
        print(f"  cycle {first.cycle_number}: {first.discharge_capacity_mah:.4f} mAh "
              f"discharge, CE {first.coulombic_efficiency:.2f}%")
        print(f"  cycle {last.cycle_number}: {last.discharge_capacity_mah:.4f} mAh "
              f"discharge, CE {last.coulombic_efficiency:.2f}%")
        if first.discharge_capacity_mah:
            keep = 100 * last.discharge_capacity_mah / first.discharge_capacity_mah
            print(f"  retention {keep:.1f}% over {len(complete)} cycles")
    return 0


def _convert(args) -> int:
    path = Path(args.path)
    wrd = read_wrd(path)
    cell = _cell_from_args(args).resolve()
    cycles = summarize_cycles(wrd, cycle_offset=args.cycle_offset)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem

    targets = args.tables or ["raw", "cycles", "profiles"]
    written: list[Path] = []

    if "raw" in targets:
        target = out_dir / f"{stem}_raw.csv"
        with target.open("w", newline="", encoding="utf-8-sig") as handle:
            write_raw_csv(wrd, handle)
        written.append(target)

    if "cycles" in targets:
        target = out_dir / f"{stem}_cycles.csv"
        with target.open("w", newline="", encoding="utf-8-sig") as handle:
            write_cycles_csv(cycles, cell, handle, basis=args.basis)
        written.append(target)

    if "profiles" in targets:
        wanted = _select_cycles(cycles, args.cycles)
        profiles = []
        for cycle in wanted:
            for branch in ("charge", "discharge"):
                profile = extract_profile(wrd, cycle, branch)
                if len(profile):
                    profiles.append(profile)
        target = out_dir / f"{stem}_profiles.csv"
        with target.open("w", newline="", encoding="utf-8-sig") as handle:
            write_profiles_csv(profiles, cell, handle, basis=args.basis)
        written.append(target)

    for target in written:
        print(f"wrote {target}")
    if cell.active_mass_g:
        print(f"active mass {cell.active_mass_g * 1000:.4g} mg"
              + (f", area {cell.area_cm2:.4g} cm2" if cell.area_cm2 else "")
              + (f", loading {cell.loading_mg_cm2:.4g} mg/cm2" if cell.loading_mg_cm2 else ""))
    return 0


def _select_cycles(cycles, spec: str | None):
    if not spec or spec == "all":
        return [c for c in cycles if c.complete]
    wanted: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, stop = part.split("-", 1)
            wanted.update(range(int(start), int(stop) + 1))
        else:
            wanted.add(int(part))
    return [c for c in cycles if c.cycle_number in wanted]


def _cycles(args) -> int:
    wrd = read_wrd(Path(args.path))
    cell = _cell_from_args(args).resolve()
    cycles = summarize_cycles(wrd, cycle_offset=args.cycle_offset)
    write_cycles_csv(cycles, cell, sys.stdout, basis=args.basis)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="wrdkit", description=__doc__.splitlines()[0])
    parser.add_argument("--version", action="version", version=f"wrdkit {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser("info", help="print metadata, schedule and cycle summary")
    info.add_argument("path")

    convert = subparsers.add_parser("convert", help="write CSV tables next to the file")
    convert.add_argument("path")
    convert.add_argument("--out-dir", default=".", help="directory for the CSV files")
    convert.add_argument("--basis", default=Basis.ABSOLUTE, choices=list(BASES))
    convert.add_argument("--cycles", help="cycles for the profile table, e.g. 1,2,10-20")
    convert.add_argument("--cycle-offset", type=int, default=0,
                         help="add to cycle numbers when a run spans several files")
    convert.add_argument("--tables", nargs="*", choices=["raw", "cycles", "profiles"])
    _cell_arguments(convert)

    cycles = subparsers.add_parser("cycles", help="print the cycle table as CSV on stdout")
    cycles.add_argument("path")
    cycles.add_argument("--basis", default=Basis.ABSOLUTE, choices=list(BASES))
    cycles.add_argument("--cycle-offset", type=int, default=0)
    _cell_arguments(cycles)

    args = parser.parse_args(argv)
    try:
        if args.command == "info":
            return _print_info(Path(args.path))
        if args.command == "convert":
            return _convert(args)
        if args.command == "cycles":
            return _cycles(args)
    except (WrdError, FileNotFoundError, ValueError) as exc:
        print(f"wrdkit: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
