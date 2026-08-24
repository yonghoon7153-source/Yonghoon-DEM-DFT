"""Build BioLogic files byte by byte.

Same bargain as ``synthetic.py``: if we can write the format we understand it,
and the tests then cover the whole read path without a real instrument file.
The lab's real spectra are megabytes and live outside the repository.
"""

from __future__ import annotations

import struct

import numpy as np

MAGIC = b"BIO-LOGIC MODULAR FILE\x1a"

#: name -> (id, struct format).  Mirrors wrdkit.eis.biologic.COLUMNS; kept
#: separate so a wrong width in the reader cannot be "verified" by the same
#: wrong width in the writer.
IDS = {
    "freq/Hz": (32, "<f"),
    "Re(Z)/Ohm": (37, "<f"),
    "-Im(Z)/Ohm": (38, "<f"),
    "|Z|/Ohm": (36, "<f"),
    "Phase(Z)/deg": (35, "<f"),
    "time/s": (4, "<d"),
    "<Ewe>/V": (77, "<f"),
    "<I>/mA": (76, "<f"),
    "cycle number": (24, "<d"),
    "I Range": (39, "<H"),
    "Ns": (131, "<H"),
}


def module(short: str, long: str, payload: bytes, version: int = 10,
           date: bytes = b"07/19/26") -> bytes:
    """One ``MODULE`` block: 65-byte header then the payload."""
    head = b"MODULE" + short.encode().ljust(10) + long.encode().ljust(25)
    head += struct.pack("<IIII", 0xFFFFFFFF, len(payload), 0, version)
    head += date.ljust(8)[:8]
    assert len(head) == 65, len(head)
    return head + payload


def data_module(columns: dict[str, np.ndarray], preamble: int = 1007) -> bytes:
    """A ``VMP data`` payload.

    ``preamble`` is the run of bytes between the column list and the rows.  Its
    length varies with the module version in real files, which is exactly why
    the reader anchors the rows on the **end** of the payload -- pass a
    different value here and the reader must still find them.
    """
    names = list(columns)
    n = len(columns[names[0]])
    header = struct.pack("<IH", n, len(names))
    header += struct.pack(f"<{len(names)}H", *(IDS[name][0] for name in names))
    filler = b"\x00" * max(0, preamble - len(header))

    rows = bytearray()
    for i in range(n):
        for name in names:
            fmt = IDS[name][1]
            value = columns[name][i]
            rows += struct.pack(fmt, int(value) if fmt == "<H" else float(value))
    return header + filler + bytes(rows)


def build_mpr(columns: dict[str, np.ndarray], *, with_log: bool = True,
              preamble: int = 1007) -> bytes:
    """A whole ``.mpr``: magic, a settings module, the data, and a log."""
    out = bytearray(MAGIC)
    out += b" " * (52 - len(out))
    out += module("VMP Set", "VMP settings", b"\x1d\x00\x08K\x03" + b"\x00" * 600)
    out += module("VMP data", "VMP data", data_module(columns, preamble),
                  version=11)
    if with_log:
        out += module("VMP LOG", "VMP LOG", b"\x00" * 128)
    return bytes(out)


def randles(frequency_hz: np.ndarray, *, rs: float = 5.0, r1: float = 20.0,
            q1: float = 1e-5, n1: float = 0.9, r2: float = 40.0,
            q2: float = 1e-3, n2: float = 0.8) -> np.ndarray:
    """``Rs - p(R1,CPE1) - p(R2,CPE2)`` -- the circuit the lab fits.

    Written out longhand rather than driven by the fitting code so a fit test
    is measuring the fitter, not comparing a function against itself.
    """
    w = 2 * np.pi * frequency_hz
    z = np.full_like(w, rs, dtype=complex)
    for r, q, n in ((r1, q1, n1), (r2, q2, n2)):
        y_cpe = q * (1j * w) ** n
        z = z + 1.0 / (1.0 / r + y_cpe)
    return z


def spectrum_columns(frequency_hz: np.ndarray, z: np.ndarray) -> dict:
    """Every column EC-Lab writes for a PEIS run, from one complex spectrum."""
    n = len(frequency_hz)
    return {
        "freq/Hz": frequency_hz,
        "Re(Z)/Ohm": z.real,
        # The file carries -Im(Z), which is what makes the sign a real risk.
        "-Im(Z)/Ohm": -z.imag,
        "|Z|/Ohm": np.abs(z),
        "Phase(Z)/deg": np.degrees(np.angle(z)),
        "time/s": np.arange(n, dtype=float) * 0.5,
        "<Ewe>/V": np.full(n, 3.7),
        "<I>/mA": np.zeros(n),
        "cycle number": np.ones(n),
        "I Range": np.full(n, 37),
        "Ns": np.zeros(n),
    }


def log_sweep(start_hz: float = 1e6, end_hz: float = 1e-2,
              per_decade: int = 10) -> np.ndarray:
    """High to low, the order EC-Lab sweeps in."""
    decades = np.log10(start_hz / end_hz)
    count = int(round(decades * per_decade)) + 1
    return np.logspace(np.log10(start_hz), np.log10(end_hz), count)


def build_mpt(columns: dict[str, np.ndarray], *, comma_decimal: bool = False,
              technique: str = "Potentio Electrochemical Impedance Spectroscopy"
              ) -> str:
    """The ASCII export, header count and all."""
    names = list(columns)
    preamble = [
        "EC-Lab ASCII FILE",
        "Nb header lines : 5",
        "",
        technique,
        "\t".join(names),
    ]
    rows = []
    n = len(columns[names[0]])
    for i in range(n):
        cells = []
        for name in names:
            text = f"{float(columns[name][i]):.6E}"
            cells.append(text.replace(".", ",") if comma_decimal else text)
        rows.append("\t".join(cells))
    return "\r\n".join(preamble + rows) + "\r\n"
