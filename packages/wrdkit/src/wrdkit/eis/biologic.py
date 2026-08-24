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

import numpy as np

from .spectrum import Spectrum

__all__ = ["read_mpr_bytes", "read_mpt_text", "read_mps_text", "MPR_MAGIC",
           "COLUMNS", "UnknownColumn"]

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
}

_WIDTH = {"<d": 8, "<f": 4, "<H": 2, "<I": 4}


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


def read_mpr_bytes(data: bytes) -> Spectrum:
    """Parse a BioLogic ``.mpr``.

    The row block sits at the **end** of the data module: the module carries a
    preamble whose length varies with the module version, and anchoring on the
    end sidesteps having to know it.  That is not a guess -- it is checked,
    because ``n_points x record_size`` has to land exactly on the module
    boundary, and a wrong column width makes it miss.
    """
    if not data.startswith(MPR_MAGIC):
        raise ValueError("not a BioLogic .mpr file (magic missing)")

    found = _modules(data)
    modules = {short: (start, length, version) for short, start, length, version in found}
    if "VMP data" not in modules:
        raise ValueError(
            "no data module in this .mpr -- found " + (", ".join(modules) or "nothing"))
    start, length, _version = modules["VMP data"]
    end = start + length

    n_points, n_columns = struct.unpack_from("<IH", data, start)
    ids = struct.unpack_from(f"<{n_columns}H", data, start + 6)

    unknown = sorted({i for i in ids if i not in COLUMNS})
    if unknown:
        listed = ", ".join(str(i) for i in unknown)
        raise UnknownColumn(
            f"column id {listed} is not in the table; add it to "
            "wrdkit.eis.biologic.COLUMNS with its width before this file "
            "can be read")

    record = sum(_WIDTH[COLUMNS[i][1]] for i in ids)
    rows_at = end - n_points * record
    if rows_at < start + 6 + 2 * n_columns:
        raise ValueError(
            f"{n_points} rows x {record} bytes do not fit in the data module "
            f"({length} bytes)")

    columns: dict[str, np.ndarray] = {}
    offset = 0
    for column_id in ids:
        name, fmt = COLUMNS[column_id]
        width = _WIDTH[fmt]
        raw = np.frombuffer(data, dtype=np.uint8,
                            count=n_points * record, offset=rows_at)
        block = raw.reshape(n_points, record)[:, offset:offset + width]
        dtype = {"<d": "<f8", "<f": "<f4", "<H": "<u2", "<I": "<u4"}[fmt]
        # ``.copy()`` because the slice is a view into a non-contiguous buffer
        # and ``frombuffer`` on it would read the neighbouring column.
        columns[name] = np.frombuffer(block.copy().tobytes(),
                                      dtype=dtype).astype(np.float64)
        offset += width

    return _spectrum_from_columns(columns, {"source_format": "mpr",
                                            "n_points": int(n_points)})


def _spectrum_from_columns(columns: dict[str, np.ndarray],
                           metadata: dict) -> Spectrum:
    """Turn named columns into a Spectrum, refusing to guess a missing one."""
    missing = [name for name in ("freq/Hz", "Re(Z)/Ohm", "-Im(Z)/Ohm")
               if name not in columns]
    if missing:
        raise ValueError("this record is not an impedance sweep -- no "
                         + ", ".join(missing) + " column")
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
    body = [line for line in lines[count:] if line.strip()]
    values: list[list[float]] = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(names):
            continue
        values.append([_number(cell) for cell in cells[:len(names)]])
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
    return _spectrum_from_columns(columns, metadata)


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
