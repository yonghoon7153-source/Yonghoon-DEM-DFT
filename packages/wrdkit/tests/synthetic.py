"""Build a minimal but structurally valid ``.wrd`` file in memory.

Committing a real 20 MB instrument file to the repository is not an option,
and a reader with no fixture is a reader nobody can refactor safely.  This
module writes the same MS-NRBF header pair and packed row block that Smart
Interface writes, so the tests exercise the real code path -- including the
variable-length current-range column that makes rows change size mid-file.

It doubles as executable documentation of the format.
"""

from __future__ import annotations

import math
import struct
import zlib
from dataclasses import dataclass

# --- NRBF record ids -------------------------------------------------------
HEADER = 0
CLASS_WITH_MEMBERS_AND_TYPES = 5
BINARY_OBJECT_STRING = 6
MESSAGE_END = 11
BINARY_LIBRARY = 12
ARRAY_SINGLE_OBJECT = 16
SYSTEM_CLASS_WITH_MEMBERS_AND_TYPES = 4
MEMBER_REFERENCE = 9
OBJECT_NULL = 10

# --- BinaryTypeEnum --------------------------------------------------------
BT_PRIMITIVE = 0
BT_PRIMITIVE_ARRAY = 7
BT_STRING = 1
BT_SYSTEM_CLASS = 3
BT_CLASS = 4

# --- PrimitiveTypeEnum -----------------------------------------------------
P_BOOLEAN, P_DOUBLE, P_INT32, P_INT64, P_UINT32, P_DATETIME = 1, 6, 8, 9, 15, 13

WBCS_LIBRARY = "WbcsFile, Version=1.0.3.0, Culture=neutral, PublicKeyToken=null"
MSCORLIB = "mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"

#: The 22 columns a WBCS3000 writes, in order, with their .NET types.
DEFAULT_COLUMNS: list[tuple[str, str]] = [
    ("DATE TIME", "System.Int64"),
    ("CHANNEL", "System.Int32"),
    ("TEST TIME", "System.Int64"),
    ("STEP TIME", "System.Int64"),
    ("CYCLE TIME", "System.Int64"),
    ("STEP INDEX", "System.Int32"),
    ("TOTAL STEP", "System.Int32"),
    ("CYCLE INDEX", "System.Int32"),
    ("RUN STATUS", "System.Byte"),
    ("RUNNING STATUS", "System.Byte"),
    ("CELL STATUS", "System.Byte"),
    ("I RANGE INDEX", "System.Int32"),
    ("I RANGE", "System.String"),
    ("VOLTAGE", "System.Double"),
    ("CURRENT", "System.Double"),
    ("CHARGE Q", "System.Double"),
    ("DISCHARGE Q", "System.Double"),
    ("CHARGE E", "System.Double"),
    ("DISCHARGE E", "System.Double"),
    ("AUX. VOLTAGE", "System.Double"),
    ("TEMPERATURE", "System.Double"),
    ("OCP", "System.Double"),
]

TICKS_PER_SECOND = 10_000_000
DOTNET_UNIX_EPOCH_TICKS = 621_355_968_000_000_000


def ticks_at(moment) -> int:
    """.NET ticks for a ``datetime``, read literally.

    Tests that exercise the running/finished classification need a file whose
    samples are *recent*, because a long silence is what tells the classifier
    a cell is no longer running.

    The conversion must not go through ``moment.timestamp()``.  That reads a
    naive value as *local* time and returns a UTC epoch, so in a UTC+9 lab the
    fixture lands nine hours in the past and a cell written as "running" parses
    as finished -- the suite then passes in CI (UTC) and fails on the
    researcher's own machine.  Smart Interface writes the instrument PC's wall
    clock, with no zone attached, so the honest conversion is the literal one:
    treat the naive value as the number it is.
    """
    import datetime as _datetime

    delta = moment - _datetime.datetime(1970, 1, 1)
    return DOTNET_UNIX_EPOCH_TICKS + int(delta.total_seconds() * TICKS_PER_SECOND)


def ticks_ago(seconds: float) -> int:
    """.NET ticks for a moment ``seconds`` in the past, on this machine's clock.

    ``datetime.now()`` rather than ``utcnow()``: the reader turns ticks back
    into a naive wall clock, and the API compares that against
    ``datetime.now()``.  Both sides have to be the same clock or the age is
    off by the UTC offset.
    """
    import datetime as _datetime

    return ticks_at(_datetime.datetime.now() - _datetime.timedelta(seconds=seconds))


class Writer:
    """Byte assembler with the MS-NRBF primitives."""

    def __init__(self) -> None:
        self.parts: list[bytes] = []

    def raw(self, data: bytes) -> Writer:
        self.parts.append(data)
        return self

    def u8(self, value: int) -> Writer:
        return self.raw(struct.pack("<B", value))

    def i32(self, value: int) -> Writer:
        return self.raw(struct.pack("<i", value))

    def u32(self, value: int) -> Writer:
        return self.raw(struct.pack("<I", value))

    def i64(self, value: int) -> Writer:
        return self.raw(struct.pack("<q", value))

    def f64(self, value: float) -> Writer:
        return self.raw(struct.pack("<d", value))

    def string(self, text: str) -> Writer:
        encoded = text.encode("utf-8")
        length = len(encoded)
        while True:
            byte = length & 0x7F
            length >>= 7
            self.u8(byte | (0x80 if length else 0))
            if not length:
                break
        return self.raw(encoded)

    def bytes(self) -> bytes:
        return b"".join(self.parts)


def _class_record(writer: Writer, object_id: int, name: str,
                  members: list[tuple[str, int, object]], library_id: int | None) -> None:
    """Emit a ClassWithMembersAndTypes / SystemClassWithMembersAndTypes header."""
    writer.u8(CLASS_WITH_MEMBERS_AND_TYPES if library_id is not None
              else SYSTEM_CLASS_WITH_MEMBERS_AND_TYPES)
    writer.i32(object_id)
    writer.string(name)
    writer.i32(len(members))
    for member_name, _, _ in members:
        writer.string(member_name)
    for _, binary_type, _ in members:
        writer.u8(binary_type)
    for _, binary_type, extra in members:
        if binary_type == BT_PRIMITIVE:
            writer.u8(extra)          # PrimitiveTypeEnum
        elif binary_type == BT_SYSTEM_CLASS:
            writer.string(extra)      # type name
        elif binary_type == BT_CLASS:
            writer.string(extra[0])
            writer.i32(extra[1])
        elif binary_type == BT_PRIMITIVE_ARRAY:
            writer.u8(extra)          # PrimitiveTypeEnum of the element
    if library_id is not None:
        writer.i32(library_id)


def _write_file_header(writer: Writer, *, start_ticks: int, base_tick: int,
                       file_name: str, unit_coulomb: bool = False,
                       schedule: tuple[SchedStep, ...] | None = None,
                       schedule_path: str = "") -> None:
    """Stream 1: WbcsFile.Data.DataFileHeader."""
    writer.u8(HEADER).i32(1).i32(-1).i32(1).i32(0)
    writer.u8(BINARY_LIBRARY).i32(2).string(WBCS_LIBRARY)

    members = [
        ("<Version>k__BackingField", BT_STRING, None),
        ("<Model>k__BackingField", BT_STRING, None),
        ("<SerialNo>k__BackingField", BT_STRING, None),
        ("<DeviceType>k__BackingField", BT_STRING, None),
        ("<AppVer>k__BackingField", BT_STRING, None),
        ("<FirmVer>k__BackingField", BT_STRING, None),
        ("<UnitCoulomb>k__BackingField", BT_PRIMITIVE, P_BOOLEAN),
        ("<BaseTick>k__BackingField", BT_PRIMITIVE, P_UINT32),
        ("<FileName>k__BackingField", BT_STRING, None),
        ("<StartTime>k__BackingField", BT_PRIMITIVE, P_DATETIME),
        ("<Format>k__BackingField", BT_CLASS, ("WbcsFile.Data.DataFile+eFormat", 2)),
    ]
    if schedule is not None:
        members.append(("<SeqDataSet>k__BackingField", BT_CLASS,
                        ("WbcsFile.Sch.SeqDataSet", 2)))
    _class_record(writer, 1, "WbcsFile.Data.DataFileHeader", members, library_id=2)

    # Member values, in declaration order.
    for object_id, text in ((3, "1.3.0.0"), (4, "WBCS3000S1"), (5, "TEST-SERIAL-0001"),
                            (6, "Potentiostat"), (7, "1.8.9.0"), (8, "1.3.3.0")):
        writer.u8(BINARY_OBJECT_STRING).i32(object_id).string(text)
    writer.u8(1 if unit_coulomb else 0)   # UnitCoulomb
    writer.u32(base_tick)              # BaseTick
    writer.u8(BINARY_OBJECT_STRING).i32(9).string(file_name)
    writer.raw(struct.pack("<Q", (2 << 62) | start_ticks))   # StartTime, Kind=Local

    # Format enum, serialized as its own class with a single value__ member.
    _class_record(writer, -11, "WbcsFile.Data.DataFile+eFormat",
                  [("value__", BT_PRIMITIVE, P_INT32)], library_id=2)
    writer.i32(0)

    if schedule is not None:
        _write_schedule(writer, schedule,
                        schedule_path or r"C:\Zive Data\Schedule\test.cyc")

    writer.u8(MESSAGE_END)


def _write_data_header(writer: Writer, columns: list[tuple[str, str]]) -> None:
    """Stream 2: WbcsFile.Data.DataHeader, carrying the column list."""
    writer.u8(HEADER).i32(1).i32(-1).i32(1).i32(0)
    writer.u8(BINARY_LIBRARY).i32(2).string(WBCS_LIBRARY)

    list_type = ("System.Collections.Generic.List`1[[WbcsFile.Data.UnitDataInfor, "
                 + WBCS_LIBRARY + "]]")
    _class_record(writer, 1, "WbcsFile.Data.DataHeader", [
        ("<DataCount>k__BackingField", BT_PRIMITIVE, P_INT64),
        ("<EndTime>k__BackingField", BT_PRIMITIVE, P_INT64),
        ("<ColumnList>k__BackingField", BT_SYSTEM_CLASS, list_type),
    ], library_id=2)
    writer.i64(-1)      # DataCount: the instrument leaves this unfinalized
    writer.i64(-1)      # EndTime: likewise
    writer.u8(MEMBER_REFERENCE).i32(3)

    # The List<T> itself, then its backing array.
    _class_record(writer, 3, list_type, [
        ("_items", BT_CLASS, ("WbcsFile.Data.UnitDataInfor[]", 2)),
        ("_size", BT_PRIMITIVE, P_INT32),
        ("_version", BT_PRIMITIVE, P_INT32),
    ], library_id=None)
    writer.u8(MEMBER_REFERENCE).i32(4)
    writer.i32(len(columns))
    writer.i32(len(columns))

    writer.u8(ARRAY_SINGLE_OBJECT).i32(4).i32(len(columns))
    next_id = 10
    for index, (label, dotnet_type) in enumerate(columns):
        object_id = next_id
        next_id += 1
        _class_record(writer, object_id, "WbcsFile.Data.UnitDataInfor", [
            ("<Name>k__BackingField", BT_STRING, None),
            ("<Unit>k__BackingField", BT_STRING, None),
            ("<DataType>k__BackingField", BT_SYSTEM_CLASS, "System.UnitySerializationHolder"),
        ], library_id=2 if index == 0 else 2)
        writer.u8(BINARY_OBJECT_STRING).i32(next_id).string(label)
        next_id += 1
        writer.u8(BINARY_OBJECT_STRING).i32(next_id).string("")
        next_id += 1
        _class_record(writer, next_id, "System.UnitySerializationHolder", [
            ("Data", BT_STRING, None),
            ("UnityType", BT_PRIMITIVE, P_INT32),
            ("AssemblyName", BT_STRING, None),
        ], library_id=None)
        next_id += 1
        writer.u8(BINARY_OBJECT_STRING).i32(next_id).string(dotnet_type)
        next_id += 1
        writer.i32(4)
        writer.u8(BINARY_OBJECT_STRING).i32(next_id).string(MSCORLIB)
        next_id += 1

    writer.u8(MESSAGE_END)


@dataclass
class Sample:
    """One packed data row."""

    date_ticks: int
    test_ticks: int
    step_ticks: int
    cycle_ticks: int
    step_index: int
    total_step: int
    cycle_index: int
    cell_status: int
    i_range: str
    voltage: float
    current: float
    charge_q: float
    discharge_q: float
    charge_e: float = 0.0
    discharge_e: float = 0.0
    channel: int = 1

    def pack(self) -> bytes:
        writer = Writer()
        writer.i64(self.date_ticks).i32(self.channel)
        writer.i64(self.test_ticks).i64(self.step_ticks).i64(self.cycle_ticks)
        writer.i32(self.step_index).i32(self.total_step).i32(self.cycle_index)
        writer.u8(5).u8(0).u8(self.cell_status)
        writer.i32(0)
        writer.string(self.i_range)
        for value in (self.voltage, self.current, self.charge_q, self.discharge_q,
                      self.charge_e, self.discharge_e, 0.0, 0.0, self.voltage):
            writer.f64(value)
        return writer.bytes()

    def pack_sif213(self, control_status: int = 1) -> bytes:
        """One row in the Smart Interface 2.13 layout (fixed, 128 bytes).

        2.13 declares no column list, so this **is** the contract: if the
        reader and this writer agree, the layout in the spec is right.  The
        differences from 1.x are all here — no DATE TIME, no I RANGE string,
        a fourth status byte (CC/CV), and twelve trailing bytes we have not
        identified.
        """
        writer = Writer()
        writer.i32(self.channel)
        writer.i64(self.test_ticks).i64(self.step_ticks).i64(self.cycle_ticks)
        writer.i32(self.step_index).i32(self.total_step).i32(self.cycle_index)
        writer.u8(5).u8(0).u8(self.cell_status).u8(control_status)
        for value in (self.voltage, self.current, self.charge_q, self.discharge_q,
                      self.charge_e, self.discharge_e, 0.0, 0.0, self.voltage):
            writer.f64(value)
        row = writer.bytes()
        assert len(row) == 116, len(row)
        return row + b"\x02\x00\x00\x00" + b"\x00" * 5 + b"\xa9\x9b\x93"


ARRAY_SINGLE_PRIMITIVE = 15
P_BYTE = 2
SIF_213_ROW_SIZE = 128


def _write_header_values(writer: Writer, *, start_ticks: int, base_tick: int,
                         file_name: str, unit_coulomb: bool, row_count: int,
                         end_ticks: int,
                         schedule: tuple[SchedStep, ...] | None,
                         schedule_path: str) -> None:
    """The 2.13 header: one stream, ``WbcsFile.Data.DataHeaderValues``.

    1.x split this across two streams (``DataFileHeader`` + ``DataHeader``).
    2.13 merges them, moves ``EndTime`` from a tick count to a ``DateTime``,
    and writes the schedule under the **private field** name ``_seqDataSet``
    instead of the auto-property ``SeqDataSet`` -- reading only one spelling
    meant a 2.13 file parsed with no schedule at all.
    """
    writer.u8(HEADER).i32(1).i32(-1).i32(1).i32(0)
    writer.u8(BINARY_LIBRARY).i32(2).string(WBCS_LIBRARY)

    members = [
        ("<Version>k__BackingField", BT_STRING, None),
        ("<Model>k__BackingField", BT_STRING, None),
        ("<SerialNo>k__BackingField", BT_STRING, None),
        ("<DeviceType>k__BackingField", BT_STRING, None),
        ("<AppVer>k__BackingField", BT_STRING, None),
        ("<FirmVer>k__BackingField", BT_STRING, None),
        ("<UnitCoulomb>k__BackingField", BT_PRIMITIVE, P_BOOLEAN),
        ("<BaseTick>k__BackingField", BT_PRIMITIVE, P_UINT32),
        ("<FileName>k__BackingField", BT_STRING, None),
        ("<StartTime>k__BackingField", BT_PRIMITIVE, P_DATETIME),
        ("<EndTime>k__BackingField", BT_PRIMITIVE, P_DATETIME),
        ("<DataCount>k__BackingField", BT_PRIMITIVE, P_INT32),
        ("<Format>k__BackingField", BT_CLASS, ("WbcsFile.Data.DataFile+eFormat", 2)),
    ]
    if schedule is not None:
        members.append(("_seqDataSet", BT_CLASS, ("WbcsFile.Sch.SeqDataSet", 2)))
    _class_record(writer, 1, "WbcsFile.Data.DataHeaderValues", members, library_id=2)

    for object_id, text in ((3, "2.1.3.1"), (4, "WBRS50"), (5, "W5K-TEST-0001"),
                            (6, "BatteryCycler"), (7, "2.1.3.1"), (8, "2.1.3.0")):
        writer.u8(BINARY_OBJECT_STRING).i32(object_id).string(text)
    writer.u8(1 if unit_coulomb else 0)
    writer.u32(base_tick)
    writer.u8(BINARY_OBJECT_STRING).i32(9).string(file_name)
    writer.raw(struct.pack("<Q", (2 << 62) | start_ticks))     # StartTime
    writer.raw(struct.pack("<Q", (2 << 62) | end_ticks))       # EndTime
    writer.i32(row_count)

    _class_record(writer, -11, "WbcsFile.Data.DataFile+eFormat",
                  [("value__", BT_PRIMITIVE, P_INT32)], library_id=2)
    writer.i32(0)

    if schedule is not None:
        _write_schedule(writer, schedule,
                        schedule_path or r"C:\Zive Data\Schedule\test.cyc")
    writer.u8(MESSAGE_END)


def build_wrd_sif213(samples: list[Sample], *, start_ticks: int | None = None,
                     base_tick: int = 50_000,
                     file_name: str = r"C:\Zive Data\Smart Interface\test.wrd",
                     unit_coulomb: bool = False,
                     schedule: tuple[SchedStep, ...] | None = None,
                     schedule_path: str = "",
                     version: str = "1.6.0.0",
                     gap: int = 64,
                     control_status: int = 1) -> bytes:
    """A Smart Interface 2.13 file: deflated header in an envelope.

    ``gap`` leaves unused bytes between the envelope and the first row, the
    way the real file does (its stream ended at 4770 but ``HeaderSize`` was
    6767).  A reader that starts the rows at "end of the last stream" instead
    of at ``HeaderSize`` reads garbage, and every number after that is wrong
    but plausible -- so the fixture makes that mistake fail loudly.
    """
    if start_ticks is None:
        start_ticks = DOTNET_UNIX_EPOCH_TICKS + 1_700_000_000 * TICKS_PER_SECOND
    end_ticks = start_ticks + (samples[-1].test_ticks if samples else 0)

    inner = Writer()
    _write_header_values(inner, start_ticks=start_ticks, base_tick=base_tick,
                         file_name=file_name, unit_coulomb=unit_coulomb,
                         row_count=len(samples), end_ticks=end_ticks,
                         schedule=schedule, schedule_path=schedule_path)
    # raw DEFLATE: .NET's DeflateStream writes no zlib/gzip wrapper.
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    blob = compressor.compress(inner.bytes()) + compressor.flush()

    envelope = Writer()
    envelope.u8(HEADER).i32(1).i32(-1).i32(1).i32(0)
    envelope.u8(BINARY_LIBRARY).i32(2).string(WBCS_LIBRARY)
    _class_record(envelope, 1, "WbcsFile.Data.DataHeaderBase", [
        ("Version", BT_STRING, None),
        ("HeaderSize", BT_PRIMITIVE, P_INT32),
        ("HeaderData", BT_PRIMITIVE_ARRAY, P_BYTE),
    ], library_id=2)
    envelope.u8(BINARY_OBJECT_STRING).i32(3).string(version)
    header_size_at = len(envelope.bytes())
    envelope.i32(0)                      # HeaderSize, patched below
    envelope.u8(MEMBER_REFERENCE).i32(4)
    envelope.u8(ARRAY_SINGLE_PRIMITIVE).i32(4).i32(len(blob)).u8(P_BYTE)
    envelope.raw(blob)
    envelope.u8(MESSAGE_END)

    body = bytearray(envelope.bytes())
    header_size = len(body) + gap
    body[header_size_at:header_size_at + 4] = struct.pack("<i", header_size)
    body.extend(b"\x00" * gap)
    for sample in samples:
        row = sample.pack_sif213(control_status)
        assert len(row) == SIF_213_ROW_SIZE, len(row)
        body.extend(row)
    return bytes(body)


def build_wrd(samples: list[Sample], *, start_ticks: int | None = None,
              base_tick: int = 50_000, file_name: str = r"C:\Zive Data\test.wrd",
              columns: list[tuple[str, str]] | None = None,
              unit_coulomb: bool = False,
              schedule: tuple[SchedStep, ...] | None = None,
              schedule_path: str = "") -> bytes:
    """Assemble a complete ``.wrd`` byte string.

    ``unit_coulomb`` flips the header flag that decides whether the capacity
    and energy columns are read as Ah/Wh or C/J, so the True branch of
    ``WrdFile._to_mah`` is reachable without a real coulomb-mode file.
    """
    if start_ticks is None:
        start_ticks = DOTNET_UNIX_EPOCH_TICKS + 1_700_000_000 * TICKS_PER_SECOND
    writer = Writer()
    _write_file_header(writer, start_ticks=start_ticks, base_tick=base_tick,
                       file_name=file_name, unit_coulomb=unit_coulomb,
                       schedule=schedule, schedule_path=schedule_path)
    _write_data_header(writer, columns or DEFAULT_COLUMNS)
    for sample in samples:
        writer.raw(sample.pack())
    return writer.bytes()


def make_cycles(n_cycles: int = 3, points_per_branch: int = 40, *,
                capacity_mah: float = 5.0, current_a: float = 1.0e-3,
                v_low: float = 1.9, v_high: float = 3.6,
                fade_per_cycle: float = 0.02,
                interval_s: float = 10.0, rest_points: int = 3,
                cv_points: int = 0, cv_capacity_fraction: float = 0.2,
                start_ticks: int | None = None) -> list[Sample]:
    """A synthetic CC charge/discharge run with a linear capacity fade.

    The current range label deliberately switches from ``1A`` to ``10mA`` after
    the first cycle so the variable row width is exercised.

    ``CHARGE Q`` / ``DISCHARGE Q`` follow the convention the reference file
    established (``docs/raw/specs/wrd-binary-format.md``): they are running
    totals that reset **once per cycle**, not once per step, and ``CHARGE Q``
    stays parked at the cycle's charge capacity while the cell discharges.
    Writing them per step instead would make "value at the end of the step"
    and "difference across the step" the same number, and the difference is
    the only one that survives a multi-step branch.

    ``cv_points`` appends a CV-like taper as a *second* charge step, so the
    charge branch spans two ``TOTAL STEP`` values sharing one running total --
    the shape that separates the two readings.  ``cv_capacity_fraction`` of the
    cycle's capacity is delivered during that hold, so the cycle total is
    unchanged by turning it on.
    """
    samples: list[Sample] = []
    date = (start_ticks if start_ticks is not None
            else DOTNET_UNIX_EPOCH_TICKS + 1_700_000_000 * TICKS_PER_SECOND)
    test_ticks = 0
    cycle_ticks = 0
    step_ticks = 0
    tick_step = int(interval_s * TICKS_PER_SECOND)
    total_step = 0
    cycle = 0
    i_range = "1A"

    def push(*, step_index: int, cell_status: int, voltage: float, current: float,
             charge_q: float, discharge_q: float) -> None:
        nonlocal date, test_ticks, cycle_ticks, step_ticks
        samples.append(Sample(
            date_ticks=date, test_ticks=test_ticks, step_ticks=step_ticks,
            cycle_ticks=cycle_ticks, step_index=step_index, total_step=total_step,
            cycle_index=cycle, cell_status=cell_status, i_range=i_range,
            voltage=voltage, current=current,
            charge_q=charge_q, discharge_q=discharge_q,
            charge_e=charge_q * 3.2, discharge_e=discharge_q * 3.1,
        ))
        date += tick_step
        test_ticks += tick_step
        cycle_ticks += tick_step
        step_ticks += tick_step

    for cycle in range(n_cycles):
        capacity = capacity_mah * (1.0 - fade_per_cycle * cycle)
        cycle_ticks = 0
        charge_q = discharge_q = 0.0
        i_range = "1A" if cycle == 0 else "10mA"
        cv_capacity = capacity * cv_capacity_fraction if cv_points else 0.0
        cc_capacity = capacity - cv_capacity

        total_step += 1
        step_ticks = 0
        for point in range(points_per_branch):
            fraction = point / (points_per_branch - 1)
            voltage = v_low + (v_high - v_low) * fraction
            charge_q = cc_capacity * fraction / 1000.0
            push(step_index=1, cell_status=3, voltage=voltage, current=current_a,
                 charge_q=charge_q, discharge_q=discharge_q)

        if cv_points:
            # The hold sits at the cut-off voltage while the current tapers;
            # the running total carries on from where CC left it.
            total_step += 1
            step_ticks = 0
            for point in range(cv_points):
                # Starts at the CC end value, not one increment past it: the
                # running total is continuous across the step boundary.
                fraction = point / max(cv_points - 1, 1)
                charge_q = (cc_capacity + cv_capacity * fraction) / 1000.0
                push(step_index=2, cell_status=3, voltage=v_high,
                     current=current_a * (1.0 - 0.9 * fraction),
                     charge_q=charge_q, discharge_q=discharge_q)
            voltage = v_high

        # Every real schedule rests between branches; without it the last
        # cycle of a file is indistinguishable from a truncated one.
        total_step += 1
        step_ticks = 0
        for _ in range(rest_points):
            push(step_index=3, cell_status=1, voltage=voltage, current=0.0,
                 charge_q=charge_q, discharge_q=discharge_q)

        total_step += 1
        step_ticks = 0
        for point in range(points_per_branch):
            fraction = point / (points_per_branch - 1)
            voltage = v_high - (v_high - v_low) * fraction
            discharge_q = capacity * fraction / 1000.0
            push(step_index=4, cell_status=4, voltage=voltage, current=-current_a,
                 charge_q=charge_q, discharge_q=discharge_q)

        total_step += 1
        step_ticks = 0
        for _ in range(rest_points):
            push(step_index=3, cell_status=1, voltage=voltage, current=0.0,
                 charge_q=charge_q, discharge_q=discharge_q)
    return samples

# --- 스케줄 ------------------------------------------------------------------
#
# 계측기가 아는 것(컷오프, C-rate, 계획 사이클 수, 샘플링 주기)은 파일 안의
# 스케줄에 있고, 워크벤치는 그것을 읽어 셀 조건을 채운다.  그 경로가 합성
# 픽스처로는 한 번도 실행되지 않았다 — 스케줄이 없는 파일로 "None 이 나온다" 만
# 확인하고 있었으니, apply_schedule_defaults 를 통째로 지워도 테스트는 통과했다.
#
# 중첩은 인라인으로 쓴다.  NrbfStream._class_values 가 비-primitive 멤버 자리에서
# record() 를 부르므로, 멤버 값 자리에 레코드를 그대로 놓을 수 있다.

SCH_LIBRARY = WBCS_LIBRARY


@dataclass
class SchedStep:
    """One row of the Schedule Editor table, as the fixture writes it."""

    name: str
    control: int                      # ControlType: 0=CC, 1=CV, 7=Rest, 13=CCCV
    value: float = 0.0                # current (A)
    value2: float = 0.0               # CCCV voltage limit (V)
    value3: float = 0.0               # CCCV taper current (A)
    loop_count: int = 1
    turn_step: str = "Next Step"
    and2: bool = False
    #: (type, condition, value, seconds) -- type 0=time, 1=voltage, 15=current
    cutoff1: tuple[int, int, float, float] | None = None
    cutoff2: tuple[int, int, float, float] | None = None
    sampling_s: float | None = None


#: formation 이 없는 계획: 임피던스 재기 전의 안정화 휴지 하나, 그리고 바로
#: 사이클링 루프.  기준 사이클이 3이 아니라 1이어야 하는 모양이다 (ADR 0018).
FORMATIONLESS_SCHEDULE: tuple[SchedStep, ...] = (
    SchedStep("eis-rest", control=7, value=0.0,
              cutoff1=(0, 1, 0.0, 1800.0), sampling_s=30.0),
    SchedStep("cyc-chg", control=13, value=0.00123, value2=3.78, value3=0.000615,
              cutoff1=(15, 1, 0.000615, 0.0), sampling_s=10.0),
    SchedStep("cyc-dch", control=0, value=-0.00123,
              cutoff1=(1, 1, 1.88, 0.0), loop_count=200, turn_step="cyc-chg",
              sampling_s=10.0),
)


#: 실측 파일에서 본 형태를 줄인 것: 화성 2사이클 뒤 사이클링 루프.
DEFAULT_SCHEDULE: tuple[SchedStep, ...] = (
    SchedStep("form-chg", control=13, value=0.00025, value2=3.18, value3=0.000125,
              cutoff1=(15, 1, 0.000125, 0.0), sampling_s=10.0),
    SchedStep("form-dch", control=0, value=-0.00025,
              cutoff1=(1, 1, 1.88, 0.0), sampling_s=10.0),
    SchedStep("cyc-chg", control=13, value=0.00123, value2=3.78, value3=0.000615,
              cutoff1=(15, 1, 0.000615, 0.0), sampling_s=10.0),
    SchedStep("cyc-dch", control=0, value=-0.00123,
              cutoff1=(1, 1, 1.88, 0.0), loop_count=200, turn_step="cyc-chg",
              sampling_s=10.0),
)


class _Ids:
    """NRBF object ids, handed out in order."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def take(self) -> int:
        value = self._next
        self._next += 1
        return value


def _write_list(writer: Writer, ids: _Ids, item_type: str,
                write_item, count: int) -> None:
    """A ``List<T>`` and its backing array, inline."""
    list_type = ("System.Collections.Generic.List`1[[" + item_type + ", "
                 + SCH_LIBRARY + "]]")
    _class_record(writer, ids.take(), list_type, [
        ("_items", BT_CLASS, (item_type + "[]", 2)),
        ("_size", BT_PRIMITIVE, P_INT32),
        ("_version", BT_PRIMITIVE, P_INT32),
    ], library_id=None)
    writer.u8(ARRAY_SINGLE_OBJECT).i32(ids.take()).i32(count)
    for index in range(count):
        write_item(index)
    writer.i32(count)      # _size
    writer.i32(count)      # _version


def _write_cutoff(writer: Writer, ids: _Ids,
                  spec: tuple[int, int, float, float] | None) -> None:
    kind, condition, value, seconds = spec or (0, 0, 0.0, 0.0)
    _class_record(writer, ids.take(), "WbcsFile.Sch.CutOff", [
        ("<Type>k__BackingField", BT_PRIMITIVE, P_INT32),
        ("<Condition>k__BackingField", BT_PRIMITIVE, P_INT32),
        ("<Value>k__BackingField", BT_PRIMITIVE, P_DOUBLE),
        ("<TimeValue>k__BackingField", BT_PRIMITIVE, P_INT64),
    ], library_id=2)
    writer.i32(kind).i32(condition).f64(value)
    writer.i64(int(seconds * TICKS_PER_SECOND))


def _write_schedule(writer: Writer, steps: tuple[SchedStep, ...],
                    source_path: str) -> None:
    """The ``SeqDataSet`` the reader walks, written inline."""
    ids = _Ids()

    _class_record(writer, ids.take(), "WbcsFile.Sch.SeqDataSet", [
        ("<Version>k__BackingField", BT_STRING, None),
        ("<FileName>k__BackingField", BT_STRING, None),
        ("<SeqDataList>k__BackingField", BT_CLASS,
         ("System.Collections.Generic.List`1[[WbcsFile.Sch.SeqData, "
          + SCH_LIBRARY + "]]", 2)),
    ], library_id=2)
    writer.u8(BINARY_OBJECT_STRING).i32(ids.take()).string("1.0")
    writer.u8(BINARY_OBJECT_STRING).i32(ids.take()).string(source_path)

    def write_sequence(_index: int) -> None:
        _class_record(writer, ids.take(), "WbcsFile.Sch.SeqData", [
            ("<SchData>k__BackingField", BT_CLASS, ("WbcsFile.Sch.SchData", 2)),
        ], library_id=2)
        _class_record(writer, ids.take(), "WbcsFile.Sch.SchData", [
            ("<SchStepList>k__BackingField", BT_CLASS,
             ("System.Collections.Generic.List`1[[WbcsFile.Sch.SchStep, "
              + SCH_LIBRARY + "]]", 2)),
        ], library_id=2)
        _write_list(writer, ids, "WbcsFile.Sch.SchStep", write_step, len(steps))

    def write_step(index: int) -> None:
        step = steps[index]
        _class_record(writer, ids.take(), "WbcsFile.Sch.SchStep", [
            ("<Name>k__BackingField", BT_STRING, None),
            ("<Control>k__BackingField", BT_CLASS, ("WbcsFile.Sch.Control", 2)),
            ("<CutOffCondsList>k__BackingField", BT_CLASS,
             ("System.Collections.Generic.List`1[[WbcsFile.Sch.CutOffConds, "
              + SCH_LIBRARY + "]]", 2)),
            ("<SampCondList>k__BackingField", BT_CLASS,
             ("System.Collections.Generic.List`1[[WbcsFile.Sch.SampCond, "
              + SCH_LIBRARY + "]]", 2)),
        ], library_id=2)
        writer.u8(BINARY_OBJECT_STRING).i32(ids.take()).string(step.name)

        # Control
        _class_record(writer, ids.take(), "WbcsFile.Sch.Control", [
            ("<Type>k__BackingField", BT_PRIMITIVE, P_INT32),
            ("<Value>k__BackingField", BT_PRIMITIVE, P_DOUBLE),
            ("<Value2>k__BackingField", BT_PRIMITIVE, P_DOUBLE),
            ("<Value3>k__BackingField", BT_PRIMITIVE, P_DOUBLE),
            ("<Loop>k__BackingField", BT_CLASS, ("WbcsFile.Sch.Loop", 2)),
        ], library_id=2)
        writer.i32(step.control).f64(step.value).f64(step.value2).f64(step.value3)
        _class_record(writer, ids.take(), "WbcsFile.Sch.Loop", [
            ("<Count>k__BackingField", BT_PRIMITIVE, P_INT32),
        ], library_id=2)
        writer.i32(step.loop_count)

        def write_conds(_i: int) -> None:
            _class_record(writer, ids.take(), "WbcsFile.Sch.CutOffConds", [
                ("<TurnStep>k__BackingField", BT_STRING, None),
                ("<And2>k__BackingField", BT_PRIMITIVE, P_BOOLEAN),
                ("<CutOff1>k__BackingField", BT_CLASS, ("WbcsFile.Sch.CutOff", 2)),
                ("<CutOff2>k__BackingField", BT_CLASS, ("WbcsFile.Sch.CutOff", 2)),
            ], library_id=2)
            writer.u8(BINARY_OBJECT_STRING).i32(ids.take()).string(step.turn_step)
            writer.u8(1 if step.and2 else 0)
            _write_cutoff(writer, ids, step.cutoff1)
            _write_cutoff(writer, ids, step.cutoff2)

        _write_list(writer, ids, "WbcsFile.Sch.CutOffConds", write_conds, 1)

        def write_samp(_i: int) -> None:
            _class_record(writer, ids.take(), "WbcsFile.Sch.SampCond", [
                ("<Enable>k__BackingField", BT_PRIMITIVE, P_BOOLEAN),
                ("<Type>k__BackingField", BT_PRIMITIVE, P_INT32),
                ("<TimeValue>k__BackingField", BT_PRIMITIVE, P_INT64),
            ], library_id=2)
            writer.u8(1).i32(0)
            writer.i64(int((step.sampling_s or 0.0) * TICKS_PER_SECOND))

        _write_list(writer, ids, "WbcsFile.Sch.SampCond", write_samp,
                    1 if step.sampling_s else 0)

    _write_list(writer, ids, "WbcsFile.Sch.SeqData", write_sequence, 1)



def make_gitt(n_pulses: int = 8, *, pulse_points: int = 20, rest_points: int = 30,
              pulse_s: float = 60.0, rest_s: float = 600.0,
              current_a: float = 1.0e-3, capacity_per_pulse_mah: float = 0.5,
              v_start: float = 3.0, dv_per_pulse: float = 0.05,
              polarisation_v: float = 0.03, ir_v: float = 0.01,
              charging: bool = True, trailing_rest: bool = True,
              pulses_per_cycle: int | None = None,
              start_ticks: int | None = None) -> list[Sample]:
    """A GITT series: pulse, rest, pulse, rest.

    Built so the two things GITT is for can be checked against known numbers.

    *The relaxed voltage steps by ``dv_per_pulse`` per pulse*, so the pOCV curve
    is a known straight line and a reader that took the polarised voltage
    instead lands ``polarisation_v`` away from it -- far outside any tolerance.

    *The pulse transient is linear in sqrt(t)*, which is what Weppner-Huggins
    assumes.  ``ir_v`` is an instantaneous ohmic jump on top of it, so a fitter
    that includes the first sample sees a curve that is not a line and the
    linearity check has something real to catch.

    ``trailing_rest=False`` ends on a pulse, which is what a truncated file
    looks like -- the case where a point has to be skipped and counted.

    ``pulses_per_cycle`` puts a cycle boundary after every N pulses: the
    cycle index steps and ``CHARGE Q`` / ``DISCHARGE Q`` reset to zero, the
    way the instrument writes them (CLAUDE.md §3).  This is the shape a
    multi-cycle GITT protocol produces, and the one a whole-file capacity
    difference silently folds on.
    """
    samples: list[Sample] = []
    date = (start_ticks if start_ticks is not None
            else DOTNET_UNIX_EPOCH_TICKS + 1_700_000_000 * TICKS_PER_SECOND)
    test_ticks = 0
    total_step = 0
    charge_q = 0.0
    discharge_q = 0.0
    cycle = 0
    sign = 1.0 if charging else -1.0

    def push(*, cell_status: int, voltage: float, current: float,
             seconds: float) -> None:
        nonlocal date, test_ticks
        samples.append(Sample(
            date_ticks=date, test_ticks=test_ticks, step_ticks=0,
            cycle_ticks=test_ticks, step_index=total_step % 2,
            total_step=total_step, cycle_index=cycle, cell_status=cell_status,
            i_range="10mA", voltage=voltage, current=current,
            charge_q=charge_q / 1000.0, discharge_q=discharge_q / 1000.0))
        date += int(seconds * TICKS_PER_SECOND)
        test_ticks += int(seconds * TICKS_PER_SECOND)

    relaxed = v_start
    #: 이 사이클이 시작된 시점까지 흘려보낸 용량.  카운터는 여기서부터 센다.
    cycle_base = 0.0
    for index in range(n_pulses):
        if pulses_per_cycle and index and index % pulses_per_cycle == 0:
            cycle += 1
            cycle_base = index * capacity_per_pulse_mah
            charge_q = 0.0
            discharge_q = 0.0

        # -- pulse ---------------------------------------------------------
        total_step += 1
        step = pulse_s / max(pulse_points - 1, 1)
        for i in range(pulse_points):
            fraction = i / max(pulse_points - 1, 1)
            # sqrt(t) transient plus an instantaneous ohmic jump.
            transient = polarisation_v * math.sqrt(fraction)
            voltage = relaxed + sign * (ir_v + transient)
            delivered = index * capacity_per_pulse_mah +                 capacity_per_pulse_mah * fraction - cycle_base
            if charging:
                charge_q = delivered
            else:
                discharge_q = delivered
            push(cell_status=3 if charging else 4,
                 voltage=voltage, current=sign * current_a, seconds=step)

        if index == n_pulses - 1 and not trailing_rest:
            break

        # -- rest ----------------------------------------------------------
        total_step += 1
        relaxed = v_start + sign * dv_per_pulse * (index + 1)
        step = rest_s / max(rest_points - 1, 1)
        for i in range(rest_points):
            fraction = i / max(rest_points - 1, 1)
            # Exponential relaxation onto the new equilibrium.
            voltage = relaxed + sign * polarisation_v * math.exp(-6.0 * fraction)
            push(cell_status=1, voltage=voltage, current=0.0, seconds=step)

    return samples
