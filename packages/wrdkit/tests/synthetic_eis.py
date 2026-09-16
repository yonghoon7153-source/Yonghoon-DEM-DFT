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
              trailing_tab: bool = False,
              technique: str = "Potentio Electrochemical Impedance Spectroscopy"
              ) -> str:
    """The ASCII export, header count and all.

    ``trailing_tab`` 은 EC-Lab 이 실제로 하는 짓이다 -- 머리글 줄 끝에 탭을
    하나 더 찍는다 (`...\tRwe/Ohm\t\r\n`).  실측 `Dry_1.mpt` (v11.63).
    """
    names = list(columns)
    header = "\t".join(names) + ("\t" if trailing_tab else "")
    preamble = [
        "EC-Lab ASCII FILE",
        "Nb header lines : 5",
        "",
        technique,
        header,
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


# --- SOC 스캔 파일 (ADR 0022) ------------------------------------------------
#
# 실측 반쪽셀 파일의 모양을 그대로 흉내낸다: 앞에 1바이트 플래그들, Re/Im 없이
# |Z|·위상만, 사이클링 행 사이에 끼어 있는 EIS 스윕 여럿, 목록 끝의 모르는
# 컬럼, 그리고 모듈 끝에서 몇 바이트 앞에서 끝나는 행 블록.

SCAN_FLAGS = [(1, "<B"), (2, "<B"), (3, "<B"), (21, "<B"), (31, "<B"), (65, "<B")]
#: 목록 맨 뒤의 모르는 id 와 그 합계 폭 (실측 파일은 880·469 가 7바이트다).
SCAN_TAIL = [(880, 3), (469, 4)]


def build_mpr_soc_scan(*, sweeps: int = 3, points: int = 8, cycling_rows: int = 25,
                       trailer: int = 5, preamble: int = 1007) -> bytes:
    """A GCPL record with ``sweeps`` impedance sweeps measured along the way.

    ``trailer`` is how many bytes follow the row block inside the module -- the
    lab's file leaves five, and five bytes of shift turns every float into a
    different float that is still a float.
    """
    layout = ([(i, f) for i, f in SCAN_FLAGS]
              + [(131, "<H"), (39, "<H"), (4, "<d"), (6, "<f"), (13, "<d"),
                 (32, "<f"), (36, "<f"), (35, "<f")])
    record = sum({"<B": 1, "<H": 2, "<d": 8, "<f": 4}[f] for _, f in layout)
    record += sum(width for _, width in SCAN_TAIL)

    rows = bytearray()
    n = 0
    clock = 0.0
    frequency = np.logspace(5, -1, points)
    for sweep in range(sweeps):
        for _ in range(cycling_rows):          # 사이클링: 주파수 0
            rows += _scan_row(clock, 3.6 + 0.1 * sweep, 0.0, 0.0, 0.0,
                              ns=2 * sweep, capacity=0.5 * sweep)
            clock += 1.0
            n += 1
        for f in frequency:                    # 스윕: 7 MHz → 0.1 Hz 하강
            z = 5.0 + 20.0 / (1.0 + 1j * 2 * np.pi * f * 1e-3)
            rows += _scan_row(clock, 3.6 + 0.1 * sweep, f, abs(z),
                              np.degrees(np.angle(z)), ns=2 * sweep + 1,
                              capacity=0.5 * sweep)
            clock += 1.0
            n += 1

    header = struct.pack("<IH", n, len(layout) + len(SCAN_TAIL))
    header += struct.pack(f"<{len(layout) + len(SCAN_TAIL)}H",
                          *[i for i, _ in layout], *[i for i, _ in SCAN_TAIL])
    payload = header + b"\x00" * (preamble - len(header)) + bytes(rows) + b"\x00" * trailer

    out = bytearray(MAGIC)
    out += b" " * (52 - len(out))
    out += module("VMP Set", "VMP settings", b"\x1d\x00\x08K\x03" + b"\x00" * 600)
    out += module("VMP data", "VMP data", payload, version=11)
    out += module("VMP LOG", "VMP LOG", b"\x00" * 128)
    return bytes(out)


def _scan_row(t: float, ewe: float, freq: float, magnitude: float,
              phase_deg: float, *, ns: int, capacity: float = 0.0) -> bytes:
    row = struct.pack("<BBBBBB", 0, 0, 0, 0, 0, 0)
    row += struct.pack("<HH", ns, 39)
    row += struct.pack("<d", t)
    row += struct.pack("<f", ewe)
    row += struct.pack("<d", capacity)
    row += struct.pack("<fff", freq, magnitude, phase_deg)
    row += b"\x00" * sum(width for _, width in SCAN_TAIL)
    return row


# --- 온도 스윕 .mpt (대칭셀 이온전도도) --------------------------------------
#
# 실측 `B12_activationE_C02.mpt` 의 모양: 한 파일 안에 Rest 와 PEIS 가 번갈아
# 들어 있고, PEIS 는 7 MHz 에서 10 Hz 로 **내려간다**.  온도는 어느 열에도
# 없다 -- 챔버를 돌린 것은 사람이라 계측기가 모른다.

def build_mpt_temperature_scan(*, resistances: list[float] | None = None,
                               points: int = 12, rest_rows: int = 4,
                               with_rest_rows: bool = True,
                               inductance_h: float = 2e-6) -> str:
    """온도마다 PEIS 를 한 번씩 건 `.mpt`.

    ``resistances`` 는 온도마다의 전해질 저항(Ω)이다 -- 첫 항목이 첫 스윕.
    나이퀴스트는 ``Rs`` 를 0 으로 둔 반원 하나라, 저주파 실수축 절편이 곧 그
    저항이 된다.

    ``with_rest_rows`` 가 거짓이면 PEIS 행만 이어 붙인다.  EC-Lab 은 내보내기
    설정에 따라 둘 중 하나를 내는데, **스윕을 가르는 근거가 둘 다 달라서**
    (주파수 0 인 행이냐, 주파수가 되짚는 자리냐) 두 모양을 다 시험해야 한다.

    ``inductance_h`` 는 배선 인덕턴스다.  실측 파일의 7 MHz 에서 ``-Im`` 이
    -82.9 Ω 인 것이 이것이고, 넣지 않으면 나이퀴스트가 실수축을 **지나지 않아**
    교점을 찾는 코드가 시험되지 않는다.  2 µH 가 7 MHz 에서 88 Ω 이라 실측과
    같은 자리에 온다.
    """
    resistances = resistances or [9.69, 14.56, 34.66, 94.30, 300.0]
    frequency = np.logspace(np.log10(7e6), 1.0, points)   # 7 MHz → 10 Hz
    columns: dict[str, list[float]] = {
        "freq/Hz": [], "Re(Z)/Ohm": [], "-Im(Z)/Ohm": [], "|Z|/Ohm": [],
        "Phase(Z)/deg": [], "time/s": [], "Ewe/V": [], "Ns": [],
    }
    clock = 0.0
    sequence = 0
    for resistance in resistances:
        if with_rest_rows:
            for _ in range(rest_rows):         # 온도 평형을 잡는 휴지 구간
                _mpt_row(columns, clock, 0.0, 0.0 + 0.0j, sequence)
                clock += 3600.0
            sequence += 1
        for f in frequency:
            omega = 2 * np.pi * f
            z = resistance / (1.0 + 1j * omega * 1e-6) + 1j * omega * inductance_h
            _mpt_row(columns, clock, f, z, sequence)
            clock += 1.0
        sequence += 1
    return build_mpt({name: np.array(values, dtype=float)
                      for name, values in columns.items()},
                     technique="Potentio Electrochemical Impedance Spectroscopy")


def _mpt_row(columns: dict[str, list[float]], t: float, freq: float,
             z: complex, sequence: int) -> None:
    columns["freq/Hz"].append(freq)
    columns["Re(Z)/Ohm"].append(z.real)
    # 파일이 담는 것은 -Im(Z) 다 (물리 규약의 Im(Z) 가 아니다).
    columns["-Im(Z)/Ohm"].append(-z.imag)
    columns["|Z|/Ohm"].append(abs(z))
    columns["Phase(Z)/deg"].append(np.degrees(np.angle(z)) if z != 0 else 0.0)
    columns["time/s"].append(t)
    columns["Ewe/V"].append(0.0)
    columns["Ns"].append(float(sequence))
