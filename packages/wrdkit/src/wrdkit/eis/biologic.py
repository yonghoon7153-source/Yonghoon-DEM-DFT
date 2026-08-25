"""Readers for the three files EC-Lab leaves behind.

``.mpr``  the binary record.  What the instrument actually wrote.
``.mpt``  the ASCII export.  What the lab has been producing by hand so far,
          because ZView reads only csv / text / mpt.
``.mps``  the settings file.  Human-readable; carries the frequency sweep, the
          amplitude and the technique.

Reading ``.mpr`` directly is the point (ADR 0019 §4): the EC-Lab export is the
one step in the current workflow that needs a person, and a person who forgets
it has no data.  ``.mpt`` stays supported because there are folders full of it.

The ``.mpr`` container is self-describing.  A file is a run of modules::

    BIO-LOGIC MODULAR FILE\\x1a<padding>
    MODULE VMP Set    ... <header 65 bytes> <payload>
    MODULE VMP data   ... <header 65 bytes> <payload>
    MODULE VMP LOG    ... <header 65 bytes> <payload>

and the data module names its own columns by id, so the column list is read
from the file rather than assumed (CLAUDE.md §0.6).
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass

import numpy as np

from .spectrum import Spectrum

__all__ = ["read_mpr_bytes", "read_mpr_sweeps", "read_mpt_text", "read_mpt_sweeps",
           "read_mps_text", "MPR_MAGIC", "COLUMNS", "Sweep", "UnknownColumn"]

MPR_MAGIC = b"BIO-LOGIC MODULAR FILE"

#: Bytes of module header before the payload.  ``MODULE`` (6) + short name (10)
#: + long name (25) + four uint32 + an 8-byte date.
_HEADER = 65
_SHORT_AT, _LONG_AT, _NUMBERS_AT, _DATE_AT = 6, 16, 41, 57


class UnknownColumn(ValueError):
    """A column id this reader has no width for.

    Fatal on purpose.  Every column is packed back-to-back with no padding, so
    one unknown width shifts every column after it -- the frequencies would
    still look plausible and the impedances would be garbage.  Better to name
    the id and stop (§0.4).
    """


#: Column id -> (name, struct format).  BioLogic's own numbering; the widths
#: are what make the record size, so a wrong one is not a wrong label but a
#: wrong file.  Only ids seen in this lab's files are listed -- an id we have
#: never met raises rather than being guessed at.
COLUMNS: dict[int, tuple[str, str]] = {
    # Per-sample flags.  One byte each; confirmed by what follows them --
    # ``Ns`` and ``I Range`` land on their own values only at this width, and
    # the whole row block validates from there (ADR 0022).
    1: ("mode", "<B"),
    2: ("ox/red", "<B"),
    3: ("error", "<B"),
    21: ("control changes", "<B"),
    31: ("Ns changes", "<B"),
    65: ("counter inc.", "<B"),
    4: ("time/s", "<d"),
    5: ("control/V/mA", "<f"),
    6: ("Ewe/V", "<f"),
    7: ("dq/mA.h", "<d"),
    8: ("I/mA", "<f"),
    9: ("Ece/V", "<f"),
    11: ("<I>/mA", "<d"),
    13: ("(Q-Qo)/mA.h", "<d"),
    19: ("control/V", "<f"),
    20: ("control/mA", "<f"),
    23: ("dQ/mA.h", "<d"),
    24: ("cycle number", "<d"),
    32: ("freq/Hz", "<f"),
    33: ("|Ewe|/V", "<f"),
    34: ("|I|/A", "<f"),
    35: ("Phase(Z)/deg", "<f"),
    36: ("|Z|/Ohm", "<f"),
    37: ("Re(Z)/Ohm", "<f"),
    38: ("-Im(Z)/Ohm", "<f"),
    39: ("I Range", "<H"),
    69: ("R/Ohm", "<f"),
    70: ("P/W", "<f"),
    74: ("|Energy|/W.h", "<d"),
    76: ("<I>/mA", "<f"),
    77: ("<Ewe>/V", "<f"),
    96: ("|Ece|/V", "<f"),
    98: ("Phase(Zce)/deg", "<f"),
    99: ("|Zce|/Ohm", "<f"),
    100: ("Re(Zce)/Ohm", "<f"),
    101: ("-Im(Zce)/Ohm", "<f"),
    102: ("<Ece>/V", "<f"),
    131: ("Ns", "<H"),
    168: ("Rcmp/Ohm", "<f"),
    169: ("Cs/µF", "<f"),
    172: ("Cp/µF", "<f"),
    467: ("Q charge/discharge/mA.h", "<d"),
    468: ("half cycle", "<I"),
}

_WIDTH = {"<d": 8, "<f": 4, "<H": 2, "<I": 4, "<B": 1}


def _modules(data: bytes) -> list[tuple[str, int, int, int]]:
    """``(short name, payload offset, payload length, version)`` for each."""
    out = []
    for match in re.finditer(b"MODULE", data):
        at = match.start()
        if len(data) < at + _HEADER:
            continue
        short = data[at + _SHORT_AT:at + _LONG_AT].decode("latin-1").strip()
        if not short.startswith("VMP"):
            continue          # the word appearing inside a payload by chance
        _, length, _, version = struct.unpack_from("<IIII", data, at + _NUMBERS_AT)
        out.append((short, at + _HEADER, length, version))
    return out


@dataclass
class Sweep:
    """One impedance sweep, and the cell state it was measured at.

    A SOC scan puts sixteen of these in one file (ADR 0022).  The potential
    and the capacity are what tells them apart, so they travel with the
    spectrum rather than beside it -- separated, the plot cannot be redrawn.
    """

    spectrum: Spectrum
    #: 1-based position in the file.
    index: int
    #: The instrument's sequence number (``Ns``), when the file carries one.
    sequence: int | None = None
    #: Cell potential during the sweep, V.
    potential_v: float | None = None
    #: Accumulated capacity at the sweep, mA.h -- the SOC axis.
    capacity_mah: float | None = None
    #: Seconds from the start of the record.
    start_time_s: float | None = None


def _row_layout(data: bytes, start: int, end: int, n_points: int,
                ids: tuple[int, ...]) -> tuple[int, int]:
    """Record size and where the rows begin -- solved from the file.

    Two assumptions used to be baked in and both are false on real files
    (ADR 0022): that every column id is known, and that the row block ends
    exactly at the module boundary.  A lab file ends five bytes short of it,
    and five bytes of shift turns every float into a different float that is
    still a float.

    So the record size is the smallest one that leaves a plausible preamble,
    and the row offset is chosen by **physical validation** rather than
    arithmetic.  Searching without validating is what makes this dangerous:
    while reverse-engineering these files, "time increases" alone accepted a
    wrong offset twice -- both times a zero-filled preamble read as data.
    """
    header = 6 + 2 * len(ids)
    unknown_at = [k for k, cid in enumerate(ids) if cid not in COLUMNS]
    if unknown_at:
        first = unknown_at[0]
        stranded = [cid for cid in ids[first:] if cid in COLUMNS]
        if stranded:
            listed = ", ".join(str(i) for i in sorted(set(ids[first:]) - set(COLUMNS)))
            raise UnknownColumn(
                f"column id {listed} is not in the table and columns we read "
                f"come after it; add it to wrdkit.eis.biologic.COLUMNS with "
                f"its width before this file can be read")
        known_ids = ids[:first]
        spare = len(ids) - first          # at least one byte per unknown column
    else:
        known_ids, spare = ids, 0
    known_width = sum(_WIDTH[COLUMNS[i][1]] for i in known_ids)
    if known_width <= 0:
        raise ValueError("this .mpr declares no readable columns")

    length = end - start
    candidates = ([known_width] if not spare
                  else range(known_width + spare, known_width + spare + 64))
    for record in candidates:
        leftover = length - n_points * record
        if leftover < header:
            break
        if leftover > _MAX_PREAMBLE:
            continue
        for shift in range(record):
            rows_at = end - n_points * record - shift
            if rows_at < start + header:
                break
            if _layout_is_sound(data, rows_at, n_points, record, known_ids):
                return record, rows_at
    if not spare:
        # Every column width is known, so the record size is not in doubt and
        # only the anchor was.  Fall back to the conventional one (rows ending
        # at the module boundary) so the column validators downstream can say
        # precisely what is wrong -- "|Z| does not match its parts" is a far
        # better answer than "no layout reads as measurements", and a file
        # corrupted in the values rather than the framing lands here.
        return known_width, end - n_points * known_width
    raise ValueError(
        f"could not place the {n_points} rows of this .mpr -- the module is "
        f"{length} bytes and no row layout in it reads as measurements")


#: How much zero padding may sit between the column list and the rows.  Both
#: real files carry about 1 kB; the bound only has to exclude the absurd.
_MAX_PREAMBLE = 4096


def _offsets(ids) -> dict[str, int]:
    out, at = {}, 0
    for cid in ids:
        name, fmt = COLUMNS[cid]
        out[name] = at
        at += _WIDTH[fmt]
    return out


def _column_at(data: bytes, rows_at: int, n: int, record: int,
               offset: int, fmt: str) -> np.ndarray:
    dtype = {"<d": "<f8", "<f": "<f4", "<H": "<u2", "<I": "<u4", "<B": "u1"}[fmt]
    width = _WIDTH[fmt]
    raw = np.frombuffer(data, dtype=np.uint8, count=n * record, offset=rows_at)
    block = raw.reshape(n, record)[:, offset:offset + width]
    return np.frombuffer(block.copy().tobytes(), dtype=dtype).astype(np.float64)


def _layout_is_sound(data: bytes, rows_at: int, n: int, record: int,
                     ids) -> bool:
    """Does this alignment read as measurements rather than as padding?

    Several independent properties at once, because any one of them alone has
    a false positive: a zero-filled preamble passes "time never decreases",
    and any record-aligned window passes the ``|Z|`` identity.
    """
    offsets = _offsets(ids)
    fmt = {COLUMNS[i][0]: COLUMNS[i][1] for i in ids}
    col = lambda name: _column_at(data, rows_at, n, record,
                                  offsets[name], fmt[name])   # noqa: E731

    if "time/s" in offsets:
        t = col("time/s")
        if not np.all(np.isfinite(t)) or t[0] < 0 or np.any(np.diff(t) < 0):
            return False
        if not 0 < t[-1] < 1e9:
            return False
    if "freq/Hz" in offsets:
        f = col("freq/Hz")
        if not np.all(np.isfinite(f)) or np.any(f < 0) or not np.any(f > 0):
            return False
        positive = f[f > 0]
        # No instrument sweeps outside this; a misaligned float readily does.
        if positive.min() < 1e-6 or positive.max() > 1e9:
            return False
        # A sweep is many decades wide; a block of padding is not.
        if positive.max() / positive.min() < 10.0:
            return False
    if "|Z|/Ohm" in offsets and "Phase(Z)/deg" in offsets:
        # The polar pair is the only redundancy a file without Re/Im carries,
        # and it is a strong one: a phase is an angle, so a misaligned float
        # almost never lands inside +-180 for every row.  Without this check
        # a wrong record size passed the search and failed downstream with
        # "phase does not match" -- the right complaint from the wrong place.
        magnitude, phase = col("|Z|/Ohm"), col("Phase(Z)/deg")
        if not np.all(np.isfinite(magnitude)) or np.any(magnitude < 0):
            return False
        if not np.all(np.isfinite(phase)) or np.any(np.abs(phase) > 180.0):
            return False
    if "Ewe/V" in offsets or "<Ewe>/V" in offsets:
        e = col("Ewe/V" if "Ewe/V" in offsets else "<Ewe>/V")
        # Padding reads as exact zeros; a cell sits somewhere real.
        if not np.all(np.isfinite(e)) or np.all(e == 0) or np.max(np.abs(e)) > 100:
            return False
    if {"Re(Z)/Ohm", "-Im(Z)/Ohm", "|Z|/Ohm"} <= set(offsets):
        re_z, neg_im, mag = col("Re(Z)/Ohm"), col("-Im(Z)/Ohm"), col("|Z|/Ohm")
        with np.errstate(invalid="ignore", divide="ignore"):
            rel = np.abs(np.hypot(re_z, neg_im) - mag) / np.maximum(np.abs(mag), 1e-30)
        if not np.isfinite(np.median(rel)) or np.median(rel) > 1e-3:
            return False
    return True


def _read_mpr_columns(data: bytes) -> tuple[dict[str, np.ndarray], dict]:
    """Every column the data module declares, as float64 arrays."""
    if not data.startswith(MPR_MAGIC):
        raise ValueError("not a BioLogic .mpr file (magic missing)")

    found = _modules(data)
    modules = {short: (start, length, version) for short, start, length, version in found}
    if "VMP data" not in modules:
        raise ValueError(
            "no data module in this .mpr -- found " + (", ".join(modules) or "nothing"))
    start, length, _version = modules["VMP data"]
    end = start + length
    # The rows are anchored on this end, so the end has to be *right*: one
    # corrupted byte in the length field shifts every row by one and the
    # numbers still look like floats -- the review fed a length of N+1 and got
    # a 31-point spectrum of garbage accepted.  A correct length lands exactly
    # on the next module header or on the end of the file; anything else is a
    # truncated or corrupted container.
    if end > len(data) or (end != len(data) and data[end:end + 6] != b"MODULE"):
        raise ValueError(
            f"the data module claims {length} bytes but does not end on a "
            f"module boundary -- the file is truncated or corrupted")

    n_points, n_columns = struct.unpack_from("<IH", data, start)
    ids = struct.unpack_from(f"<{n_columns}H", data, start + 6)
    record, rows_at = _row_layout(data, start, end, n_points, ids)

    columns: dict[str, np.ndarray] = {}
    offset = 0
    for column_id in ids:
        if column_id not in COLUMNS:
            break                      # the opaque tail (ADR 0022)
        name, fmt = COLUMNS[column_id]
        columns[name] = _column_at(data, rows_at, n_points, record, offset, fmt)
        offset += _WIDTH[fmt]
    return columns, {"source_format": "mpr", "n_points": int(n_points)}


def read_mpr_sweeps(data: bytes) -> list[Sweep]:
    """Every impedance sweep in a BioLogic ``.mpr``, in file order.

    A SOC scan holds one sweep per state of charge, with cycling in between
    (ADR 0022); a single-technique file holds exactly one.
    """
    columns, metadata = _read_mpr_columns(data)
    return _sweeps_from_columns(columns, metadata)


def read_mpr_bytes(data: bytes) -> Spectrum:
    """The one impedance sweep in a ``.mpr``.

    Refuses a file that holds several rather than silently returning the
    first: a SOC scan's sixteen sweeps are the measurement, not a detail.
    """
    sweeps = read_mpr_sweeps(data)
    return _only_sweep(sweeps, "mpr")


def _only_sweep(sweeps: list[Sweep], kind: str) -> Spectrum:
    if not sweeps:
        raise ValueError("this record is not an impedance sweep -- no "
                         "frequency column with positive frequencies")
    if len(sweeps) > 1:
        raise ValueError(
            f"this .{kind} holds {len(sweeps)} impedance sweeps; use "
            f"read_{kind}_sweeps() to get all of them (ADR 0022)")
    return sweeps[0].spectrum


def _sweep_pieces(frequency: np.ndarray) -> list[np.ndarray]:
    """Row indices of each sweep.

    Impedance rows come in contiguous runs -- the cycling rows between them
    are the natural divider -- and one run can hold a sweep repeated nine
    times, so a run is cut again wherever the frequency reverses direction.
    """
    usable = np.isfinite(frequency) & (frequency > 0)
    index = np.flatnonzero(usable)
    if not len(index):
        return []
    runs = np.split(index, np.flatnonzero(np.diff(index) != 1) + 1)
    pieces: list[np.ndarray] = []
    for run in runs:
        if len(run) < 3:
            pieces.append(run)
            continue
        steps = np.diff(frequency[run])
        direction = -1.0 if np.median(steps) < 0 else 1.0
        breaks = np.flatnonzero(steps * direction < 0) + 1
        pieces.extend(piece for piece in np.split(run, breaks) if len(piece))
    return pieces


def _mean_of(columns: dict[str, np.ndarray], names: tuple[str, ...],
             rows: np.ndarray) -> float | None:
    for name in names:
        if name in columns:
            value = float(np.mean(columns[name][rows]))
            if np.isfinite(value):
                return value
    return None


def _sweeps_from_columns(columns: dict[str, np.ndarray],
                         metadata: dict) -> list[Sweep]:
    if "freq/Hz" not in columns:
        raise ValueError("this record is not an impedance sweep -- no "
                         "freq/Hz column")
    # Zero means "this row is not an impedance point" -- a SOC scan is mostly
    # cycling rows (ADR 0022).  Not-a-number means the row *is* one and is
    # damaged, and dropping it silently would hide a blank cell in an export.
    frequency = columns["freq/Hz"]
    bad = np.flatnonzero(~np.isfinite(frequency))
    if len(bad):
        raise ValueError(f"freq/Hz is not a number at row {int(bad[0]) + 1} "
                         f"({len(bad)} rows in total)")
    out: list[Sweep] = []
    for number, rows in enumerate(_sweep_pieces(columns["freq/Hz"]), start=1):
        piece = {name: values[rows] for name, values in columns.items()}
        info = dict(metadata)
        info["n_points"] = int(len(rows))
        info["sweep_index"] = number
        sequence = None
        if "Ns" in piece and len(rows):
            sequence = int(np.median(piece["Ns"]))
            info["sequence"] = sequence
        out.append(Sweep(
            spectrum=_spectrum_from_columns(piece, info),
            index=number,
            sequence=sequence,
            potential_v=_mean_of(columns, ("<Ewe>/V", "Ewe/V"), rows),
            capacity_mah=_mean_of(columns, ("(Q-Qo)/mA.h", "Q charge/discharge/mA.h",
                                            "dq/mA.h"), rows),
            start_time_s=(float(columns["time/s"][rows][0])
                          if "time/s" in columns and len(rows) else None),
        ))
    return out


def _with_rectangular(columns: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Fill in ``Re(Z)`` / ``-Im(Z)`` from ``|Z|`` and the phase when the file
    carries only the polar pair.

    The lab's half-cell files do exactly that (ADR 0022).  ``Re = |Z| cos phi``
    and ``Im = |Z| sin phi`` is what the phase *means*, not an estimate -- and
    the reader already checks the same identity in reverse wherever the file
    carries both forms.
    """
    if "Re(Z)/Ohm" in columns and "-Im(Z)/Ohm" in columns:
        return columns
    if "|Z|/Ohm" not in columns or "Phase(Z)/deg" not in columns:
        return columns
    magnitude = columns["|Z|/Ohm"]
    phase = np.radians(columns["Phase(Z)/deg"])
    filled = dict(columns)
    filled["Re(Z)/Ohm"] = magnitude * np.cos(phase)
    # The file stores -Im(Z), so the stored form is the negated imaginary part.
    filled["-Im(Z)/Ohm"] = -(magnitude * np.sin(phase))
    return filled


def _spectrum_from_columns(columns: dict[str, np.ndarray],
                           metadata: dict) -> Spectrum:
    """Turn named columns into a Spectrum, refusing to guess a missing one.

    The essential three columns must also be *numbers*: a blank cell in an
    export parses to NaN, and a NaN frequency used to ride through upload and
    save, failing only later inside a fit with no mention of the file.  And
    where the record carries its own |Z| and phase, they are checked against
    Re/Im -- redundancy the instrument wrote, and the strongest alignment
    check there is: misplaced row bytes do not stay on the circle.
    """
    columns = _with_rectangular(columns)
    missing = [name for name in ("freq/Hz", "Re(Z)/Ohm", "-Im(Z)/Ohm")
               if name not in columns]
    if missing:
        raise ValueError("this record is not an impedance sweep -- no "
                         + ", ".join(missing) + " column")
    frequency = columns["freq/Hz"]
    re_z = columns["Re(Z)/Ohm"]
    im_stored = columns["-Im(Z)/Ohm"]
    for name, series in (("freq/Hz", frequency), ("Re(Z)/Ohm", re_z),
                         ("-Im(Z)/Ohm", im_stored)):
        bad = np.flatnonzero(~np.isfinite(series))
        if len(bad):
            raise ValueError(f"{name} is not a number at row {int(bad[0]) + 1} "
                             f"({len(bad)} rows in total)")
    non_positive = np.flatnonzero(frequency <= 0)
    if len(non_positive):
        raise ValueError(f"freq/Hz is not positive at row "
                         f"{int(non_positive[0]) + 1} -- not a frequency sweep")
    if "|Z|/Ohm" in columns:
        stored = columns["|Z|/Ohm"]
        magnitude = np.hypot(re_z, im_stored)
        with np.errstate(invalid="ignore", divide="ignore"):
            relative = np.abs(magnitude - stored) / np.maximum(np.abs(stored),
                                                               1e-30)
        median = float(np.median(relative))
        if np.isfinite(median) and median > 1e-3:
            raise ValueError(
                f"|Z| does not match sqrt(Re^2+Im^2) (median relative error "
                f"{median:.3g}) -- the rows are misaligned or corrupted")
    if "Phase(Z)/deg" in columns:
        # The file stores -Im(Z); the phase matches angle(Re - j*(-Im)).
        computed = np.degrees(np.arctan2(-im_stored, re_z))
        difference = float(np.median(np.abs(computed
                                            - columns["Phase(Z)/deg"])))
        if np.isfinite(difference) and difference > 0.1:
            raise ValueError(
                f"Phase(Z) does not match atan2(Im, Re) (median difference "
                f"{difference:.3g} deg) -- the rows are misaligned or corrupted")
    return Spectrum(
        frequency_hz=columns["freq/Hz"],
        z_re=columns["Re(Z)/Ohm"],
        # The file stores -Im(Z); the physics convention is Im(Z).
        z_im=-columns["-Im(Z)/Ohm"],
        metadata=metadata,
        columns=columns,
    )


_HEADER_LINES = re.compile(r"Nb header lines\s*:\s*(\d+)")


def read_mpt_text(text: str) -> Spectrum:
    """The one impedance sweep in an EC-Lab ASCII export."""
    columns, metadata = _mpt_columns(text)
    return _only_sweep(_sweeps_from_columns(columns, metadata), "mpt")


def _mpt_columns(text: str) -> tuple[dict[str, np.ndarray], dict]:
    """Parse an EC-Lab ASCII export (``.mpt``).

    ``Nb header lines`` counts the whole preamble **including** the column-name
    row, so the names are the last header line -- reading them from the line
    after it lands on the first data row instead.
    """
    lines = text.splitlines()
    match = _HEADER_LINES.search(text)
    if not match:
        raise ValueError("not an EC-Lab .mpt export (no 'Nb header lines')")
    count = int(match.group(1))
    if count < 2 or count > len(lines):
        raise ValueError(f"header line count {count} does not fit the file")

    names = [name.strip() for name in lines[count - 1].split("\t")]
    values: list[list[float]] = []
    for line_number, line in enumerate(lines[count:], start=count + 1):
        if not line.strip():
            continue
        cells = line.split("\t")
        # A trailing tab makes one empty cell; that is formatting, not data.
        while cells and not cells[-1].strip():
            cells.pop()
        # Anything else is misalignment.  Dropping a short row silently loses
        # a point; reading a long row left-to-right puts the extra cell in
        # ``freq`` and every later value one column to the right -- the review
        # fed one inserted cell and got Re(Z)=123 accepted as a measurement.
        if len(cells) != len(names):
            raise ValueError(
                f"line {line_number} has {len(cells)} columns where the "
                f"header names {len(names)} -- the export is damaged")
        values.append([_number(cell) for cell in cells])
    if not values:
        raise ValueError(f"no data rows after {count} header lines")

    table = np.array(values, dtype=np.float64)
    columns = {name: table[:, i] for i, name in enumerate(names) if name}
    metadata = {"source_format": "mpt", "n_points": table.shape[0]}
    for key, pattern in (("technique", r"^(Potentio|Galvano) Electrochemical"
                                       r" Impedance Spectroscopy"),):
        found = re.search(pattern, text, re.MULTILINE)
        if found:
            metadata[key] = found.group(0)
    return columns, metadata


def read_mpt_sweeps(text: str) -> list[Sweep]:
    """Every impedance sweep in an EC-Lab ASCII export (ADR 0022).

    An export of a SOC scan carries the same shape the binary does: cycling
    rows with impedance rows among them.
    """
    columns, metadata = _mpt_columns(text)
    return _sweeps_from_columns(columns, metadata)


def _number(cell: str) -> float:
    """EC-Lab writes the decimal separator of the PC's locale."""
    cell = cell.strip()
    if not cell:
        return float("nan")
    try:
        return float(cell)
    except ValueError:
        return float(cell.replace(",", "."))


def read_mps_text(text: str) -> dict:
    """The settings file, as the flat dict the screen can print.

    Deliberately shallow: EC-Lab's technique block is a two-column layout with
    the value at a fixed offset, and every technique has different rows.  We
    lift the ones that describe the sweep and keep the rest verbatim, rather
    than inventing a schema for techniques nobody here runs yet (§0.4).
    """
    lines = [line.rstrip() for line in text.splitlines()]
    out: dict = {"raw_lines": len(lines)}
    for line in lines:
        if " : " in line:
            key, _, value = line.partition(" : ")
            key, value = key.strip(), value.strip()
            if key and value and key not in out:
                out[key] = value
    technique = None
    for i, line in enumerate(lines):
        if line.startswith("Technique :"):
            technique = lines[i + 1].strip() if i + 1 < len(lines) else ""
            break
    if technique:
        out["technique"] = technique

    fields: dict[str, str] = {}
    for line in lines:
        # ``fi                  7.000`` -- name, run of spaces, value.
        found = re.match(r"^([A-Za-z][^\s].*?)\s{2,}(\S.*)$", line)
        if found:
            fields.setdefault(found.group(1).strip(), found.group(2).strip())
    for name, key in (("fi", "frequency_start"), ("ff", "frequency_end"),
                      ("unit fi", "frequency_start_unit"),
                      ("unit ff", "frequency_end_unit"),
                      ("Va (mV)", "amplitude_mv"), ("Nd", "points_per_decade"),
                      ("Na", "averages")):
        if name in fields:
            out[key] = fields[name]
    start = _with_unit(out.get("frequency_start"), out.get("frequency_start_unit"))
    end = _with_unit(out.get("frequency_end"), out.get("frequency_end_unit"))
    if start is not None:
        out["frequency_start_hz"] = start
    if end is not None:
        out["frequency_end_hz"] = end
    return out


_UNITS = {"MHz": 1e6, "kHz": 1e3, "Hz": 1.0, "mHz": 1e-3, "µHz": 1e-6, "uHz": 1e-6}


def _with_unit(value: str | None, unit: str | None) -> float | None:
    if not value or not unit or unit not in _UNITS:
        return None
    try:
        return float(value) * _UNITS[unit]
    except ValueError:
        return None
