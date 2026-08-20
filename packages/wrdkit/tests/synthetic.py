"""Build a minimal but structurally valid ``.wrd`` file in memory.

Committing a real 20 MB instrument file to the repository is not an option,
and a reader with no fixture is a reader nobody can refactor safely.  This
module writes the same MS-NRBF header pair and packed row block that Smart
Interface writes, so the tests exercise the real code path -- including the
variable-length current-range column that makes rows change size mid-file.

It doubles as executable documentation of the format.
"""

from __future__ import annotations

import struct
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


class Writer:
    """Byte assembler with the MS-NRBF primitives."""

    def __init__(self) -> None:
        self.parts: list[bytes] = []

    def raw(self, data: bytes) -> "Writer":
        self.parts.append(data)
        return self

    def u8(self, value: int) -> "Writer":
        return self.raw(struct.pack("<B", value))

    def i32(self, value: int) -> "Writer":
        return self.raw(struct.pack("<i", value))

    def u32(self, value: int) -> "Writer":
        return self.raw(struct.pack("<I", value))

    def i64(self, value: int) -> "Writer":
        return self.raw(struct.pack("<q", value))

    def f64(self, value: float) -> "Writer":
        return self.raw(struct.pack("<d", value))

    def string(self, text: str) -> "Writer":
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
    if library_id is not None:
        writer.i32(library_id)


def _write_file_header(writer: Writer, *, start_ticks: int, base_tick: int,
                       file_name: str) -> None:
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
    _class_record(writer, 1, "WbcsFile.Data.DataFileHeader", members, library_id=2)

    # Member values, in declaration order.
    for object_id, text in ((3, "1.3.0.0"), (4, "WBCS3000S1"), (5, "TEST-SERIAL-0001"),
                            (6, "Potentiostat"), (7, "1.8.9.0"), (8, "1.3.3.0")):
        writer.u8(BINARY_OBJECT_STRING).i32(object_id).string(text)
    writer.u8(0)                       # UnitCoulomb = false
    writer.u32(base_tick)              # BaseTick
    writer.u8(BINARY_OBJECT_STRING).i32(9).string(file_name)
    writer.raw(struct.pack("<Q", (2 << 62) | start_ticks))   # StartTime, Kind=Local

    # Format enum, serialized as its own class with a single value__ member.
    _class_record(writer, -11, "WbcsFile.Data.DataFile+eFormat",
                  [("value__", BT_PRIMITIVE, P_INT32)], library_id=2)
    writer.i32(0)

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


def build_wrd(samples: list[Sample], *, start_ticks: int | None = None,
              base_tick: int = 50_000, file_name: str = r"C:\Zive Data\test.wrd",
              columns: list[tuple[str, str]] | None = None) -> bytes:
    """Assemble a complete ``.wrd`` byte string."""
    if start_ticks is None:
        start_ticks = DOTNET_UNIX_EPOCH_TICKS + 1_700_000_000 * TICKS_PER_SECOND
    writer = Writer()
    _write_file_header(writer, start_ticks=start_ticks, base_tick=base_tick,
                       file_name=file_name)
    _write_data_header(writer, columns or DEFAULT_COLUMNS)
    for sample in samples:
        writer.raw(sample.pack())
    return writer.bytes()


def make_cycles(n_cycles: int = 3, points_per_branch: int = 40, *,
                capacity_mah: float = 5.0, current_a: float = 1.0e-3,
                v_low: float = 1.9, v_high: float = 3.6,
                fade_per_cycle: float = 0.02,
                interval_s: float = 10.0, rest_points: int = 3) -> list[Sample]:
    """A synthetic CC charge/discharge run with a linear capacity fade.

    The current range label deliberately switches from ``1A`` to ``10mA`` after
    the first cycle so the variable row width is exercised.
    """
    samples: list[Sample] = []
    date = DOTNET_UNIX_EPOCH_TICKS + 1_700_000_000 * TICKS_PER_SECOND
    test_ticks = 0
    tick_step = int(interval_s * TICKS_PER_SECOND)
    total_step = 0

    for cycle in range(n_cycles):
        capacity = capacity_mah * (1.0 - fade_per_cycle * cycle)
        cycle_ticks = 0
        for branch, status, sign in (("charge", 3, 1.0), ("discharge", 4, -1.0)):
            total_step += 1
            step_ticks = 0
            charge_q = discharge_q = 0.0
            for point in range(points_per_branch):
                fraction = point / (points_per_branch - 1)
                if branch == "charge":
                    voltage = v_low + (v_high - v_low) * fraction
                    charge_q = capacity * fraction / 1000.0
                else:
                    voltage = v_high - (v_high - v_low) * fraction
                    discharge_q = capacity * fraction / 1000.0
                samples.append(Sample(
                    date_ticks=date, test_ticks=test_ticks, step_ticks=step_ticks,
                    cycle_ticks=cycle_ticks, step_index=1 if branch == "charge" else 2,
                    total_step=total_step, cycle_index=cycle, cell_status=status,
                    i_range="1A" if cycle == 0 else "10mA",
                    voltage=voltage, current=sign * current_a,
                    charge_q=charge_q, discharge_q=discharge_q,
                    charge_e=charge_q * 3.2, discharge_e=discharge_q * 3.1,
                ))
                date += tick_step
                test_ticks += tick_step
                step_ticks += tick_step
                cycle_ticks += tick_step

            # Every real schedule rests between branches; without it the last
            # cycle of a file is indistinguishable from a truncated one.
            total_step += 1
            for point in range(rest_points):
                samples.append(Sample(
                    date_ticks=date, test_ticks=test_ticks,
                    step_ticks=point * tick_step, cycle_ticks=cycle_ticks,
                    step_index=3, total_step=total_step, cycle_index=cycle,
                    cell_status=1, i_range="1A" if cycle == 0 else "10mA",
                    voltage=voltage, current=0.0,
                    charge_q=charge_q, discharge_q=discharge_q,
                    charge_e=charge_q * 3.2, discharge_e=discharge_q * 3.1,
                ))
                date += tick_step
                test_ticks += tick_step
                cycle_ticks += tick_step
    return samples
