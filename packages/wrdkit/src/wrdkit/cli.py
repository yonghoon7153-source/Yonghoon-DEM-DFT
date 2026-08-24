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
from .health import DEFAULT_REFERENCE_CYCLE
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
        for cycle in (first, last):
            print(f"  cycle {cycle.cycle_number}: {cycle.discharge_capacity_mah:.4f} mAh "
                  f"discharge, CE {_ce(cycle.coulombic_efficiency)}")
        # ADR 0004: retention is anchored at cycle 3, because cycles 1-2 are
        # formation and lose several percent by design.  Anchoring at the first
        # complete cycle would report that formation loss as degradation and
        # disagree with what the web app shows for the same file.
        reference = next((c for c in complete
                          if c.cycle_number >= DEFAULT_REFERENCE_CYCLE), None)
        if reference is not None and reference.discharge_capacity_mah:
            keep = 100 * last.discharge_capacity_mah / reference.discharge_capacity_mah
            print(f"  retention {keep:.1f}% vs cycle {reference.cycle_number}"
                  f" ({len(complete)} complete cycles)")
        else:
            print(f"  retention n/a: no complete cycle {DEFAULT_REFERENCE_CYCLE}"
                  " or later in this file")
    return 0


def _ce(value: float | None) -> str:
    """Coulombic efficiency is ``None`` when a cycle charged nothing measurable."""
    return "n/a" if value is None else f"{value:.2f}%"


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
            write_cycles_csv(cycles, cell, handle, basis=args.basis,
                             include_incomplete=args.all_cycles)
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
    matched = [c for c in cycles if c.cycle_number in wanted]
    # A truncated cycle exports a curve that looks like a sudden capacity drop
    # and is indistinguishable from a finished one in the CSV, so an explicit
    # selection drops it too -- the API export does the same.
    skipped = [c.cycle_number for c in matched if not c.complete]
    if skipped:
        numbers = ", ".join(str(n) for n in skipped)
        print(f"wrdkit: cycle {numbers} is incomplete (truncated) and was skipped",
              file=sys.stderr)
    return [c for c in matched if c.complete]


def _cycles(args) -> int:
    wrd = read_wrd(Path(args.path))
    cell = _cell_from_args(args).resolve()
    cycles = summarize_cycles(wrd, cycle_offset=args.cycle_offset)
    write_cycles_csv(cycles, cell, sys.stdout, basis=args.basis,
                     include_incomplete=args.all_cycles)
    return 0


def _probe(path: Path) -> int:
    """Print what the file *says* it is, making no assumptions about layout.

    ``info`` cannot help with a file that fails the header check -- it raises
    before printing anything, so the only thing the user can report is the
    error message.  This walks the NRBF streams and prints the class names and
    member names as they are, which is the first question the
    extending-the-wrd-parser skill tells you to ask.

    Smart Interface 2.13 produced ``WbcsFile.Data.DataHeaderBase`` where we
    expected ``DataFileHeader``; whether that object carries the same members
    (a renamed/base class) or a different layout entirely can only be answered
    by looking.
    """
    from .nrbf import NrbfError, NrbfObject, read_stream

    buf = path.read_bytes()
    print(f"file           {path.name}")
    print(f"size           {len(buf)} bytes")
    print(f"first bytes    {buf[:16].hex(' ')}")
    offset = 0
    for index in range(1, 5):
        if offset >= len(buf):
            break
        try:
            stream = read_stream(buf, offset)
        except NrbfError as exc:
            if index > 2:
                # 두 스트림 뒤부터는 행 블록이다 — 스트림이 아니어서 못 읽는
                # 것이 정상이고, 그것을 오류로 찍으면 사람이 거기부터 의심한다.
                print(f"\nrow block      offset {offset} .. {len(buf)}"
                      f"  ({len(buf) - offset} bytes, not an NRBF stream)")
                return 0
            print(f"\nstream {index}      unreadable at offset {offset}: {exc}")
            return 1
        root = stream.root
        print(f"\nstream {index}      offset {offset} .. {stream.end_offset}"
              f"  ({len(stream.objects)} objects)")
        if isinstance(root, NrbfObject):
            print(f"  root class   {root.class_name}")
            for name, value in root.members.items():
                kind = type(value).__name__
                if isinstance(value, NrbfObject):
                    kind = f"NrbfObject {value.class_name}"
                shown = value if isinstance(value, (int, float, str, bool)) else ""
                text = f"    {name:<40} {kind}"
                if shown != "":
                    text += f" = {str(shown)[:60]}"
                print(text)
        else:
            print(f"  root         {type(root).__name__} (not an object)")
        offset = stream.end_offset
    print(f"\nafter streams  {len(buf) - offset} bytes (the row block, if the layout is the usual one)")
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
    convert.add_argument(
        "--all-cycles", action="store_true",
        help="keep the cut-off last cycle (its numbers come out blank)")
    _cell_arguments(convert)

    probe = subparsers.add_parser(
        "probe", help="print the NRBF streams as they are (for a file that will not parse)")
    probe.add_argument("path")

    cycles = subparsers.add_parser("cycles", help="print the cycle table as CSV on stdout")
    cycles.add_argument("path")
    cycles.add_argument("--basis", default=Basis.ABSOLUTE, choices=list(BASES))
    cycles.add_argument("--cycle-offset", type=int, default=0)
    cycles.add_argument(
        "--all-cycles", action="store_true",
        help="keep the cut-off last cycle (its numbers come out blank)")
    _cell_arguments(cycles)

    args = parser.parse_args(argv)
    try:
        if args.command == "info":
            return _print_info(Path(args.path))
        if args.command == "probe":
            return _probe(Path(args.path))
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
