"""Read WonATech / Zive ``.wrd`` battery cycler files.

Layout of a ``.wrd`` file (established by decoding reference files; see
``docs/raw/specs/wrd-binary-format.md``)::

    [ NRBF stream 1 ]  WbcsFile.Data.DataFileHeader  - device, schedule, report
    [ NRBF stream 2 ]  WbcsFile.Data.DataHeader      - column list
    [ raw rows ]       one packed record per sample, no framing

Each raw row is a struct whose field layout is *declared by the column list*
in stream 2, so this reader builds its numpy dtype from the file rather than
hard-coding it.  Rows are variable length because the current-range column is
a length-prefixed string, so the reader scans row starts once and then reads
each run of equally sized rows with a single vectorised numpy call.
"""

from __future__ import annotations

import datetime
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from .nrbf import NrbfError, NrbfObject, NrbfStream, read_stream, resolve
from .schedule import TICKS_PER_SECOND, Schedule, read_schedule

__all__ = ["WrdError", "WrdColumn", "WrdMetadata", "WrdFile", "read_wrd", "CellStatus"]


class WrdError(ValueError):
    """Raised when a file is not a readable ``.wrd``."""


class CellStatus:
    """``CELL STATUS`` column values, confirmed against the current sign."""

    REST = 1
    CHARGE = 3
    DISCHARGE = 4

    NAMES = {1: "rest", 3: "charge", 4: "discharge"}

    @classmethod
    def name(cls, value: int) -> str:
        return cls.NAMES.get(int(value), f"status{int(value)}")


#: .NET type name -> numpy dtype string.
_DOTNET_DTYPES = {
    "System.Boolean": "?",
    "System.Byte": "u1",
    "System.SByte": "i1",
    "System.Int16": "<i2",
    "System.UInt16": "<u2",
    "System.Int32": "<i4",
    "System.UInt32": "<u4",
    "System.Int64": "<i8",
    "System.UInt64": "<u8",
    "System.Single": "<f4",
    "System.Double": "<f8",
}

#: Instrument column labels -> stable snake_case names used everywhere else.
_COLUMN_ALIASES = {
    "date_time": "date_time",
    "channel": "channel",
    "test_time": "test_time",
    "step_time": "step_time",
    "cycle_time": "cycle_time",
    "step_index": "step_index",
    "total_step": "total_step",
    "cycle_index": "cycle_index",
    "run_status": "run_status",
    "running_status": "running_status",
    "cell_status": "cell_status",
    "i_range_index": "i_range_index",
    "i_range": "i_range",
    "voltage": "voltage",
    "current": "current",
    "charge_q": "charge_q",
    "discharge_q": "discharge_q",
    "charge_e": "charge_e",
    "discharge_e": "discharge_e",
    "aux_voltage": "aux_voltage",
    "temperature": "temperature",
    "ocp": "ocp",
}

# .NET ticks are 100 ns since 0001-01-01; Unix time starts 62135596800 s later.
_DOTNET_EPOCH = datetime.datetime(1, 1, 1)


def _slug(label: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", label.strip().lower()).strip("_")
    return _COLUMN_ALIASES.get(slug, slug)


@dataclass
class WrdColumn:
    """One declared column of the raw data block."""

    name: str
    label: str
    dotnet_type: str
    unit: str = ""

    @property
    def is_string(self) -> bool:
        return self.dotnet_type == "System.String"

    @property
    def numpy_dtype(self) -> str | None:
        return _DOTNET_DTYPES.get(self.dotnet_type)


@dataclass
class WrdMetadata:
    """Everything the file knows about itself, before any user input."""

    source_name: str
    sha256: str
    file_size: int
    wrd_version: str | None = None
    model: str | None = None
    serial_no: str | None = None
    order_no: str | None = None
    device_type: str | None = None
    app_version: str | None = None
    firmware_version: str | None = None
    base_tick: int | None = None
    unit_coulomb: bool = False
    data_format: int = 0
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None
    instrument_path: str | None = None
    schedule_path: str | None = None
    declared_row_count: int | None = None
    # Values from the instrument's own Test Report tab.  Operators routinely
    # leave these at the 1.0 defaults, which is why the app asks again.
    cell_weight_g: float | None = None
    electrode_area_cm2: float | None = None
    cell_capacity_ah: float | None = None
    cell_type: str | None = None
    memo: str | None = None
    channel: int | None = None
    schedule: Schedule | None = None
    columns: list[WrdColumn] = field(default_factory=list)
    row_count: int = 0
    trailing_bytes: int = 0

    @property
    def has_operator_cell_data(self) -> bool:
        """True when the operator actually filled in mass/area on the cycler."""
        return bool(
            (self.cell_weight_g and self.cell_weight_g != 1.0)
            or (self.electrode_area_cm2 and self.electrode_area_cm2 != 1.0)
        )


@dataclass
class WrdFile:
    """A parsed ``.wrd``: metadata plus one numpy array per column."""

    metadata: WrdMetadata
    data: dict[str, np.ndarray]

    def __len__(self) -> int:
        return self.metadata.row_count

    @property
    def columns(self) -> list[str]:
        return list(self.data)

    def __getitem__(self, name: str) -> np.ndarray:
        return self.data[name]

    def get(self, name: str, default: Any = None) -> Any:
        return self.data.get(name, default)

    # -- derived, unit-corrected views -------------------------------------
    def seconds(self, column: str = "test_time") -> np.ndarray:
        """A tick column converted to seconds."""
        return self.data[column].astype(np.float64) / TICKS_PER_SECOND

    def timestamps(self) -> np.ndarray:
        """``date_time`` as float seconds since the Unix epoch."""
        ticks = self.data["date_time"].astype(np.float64)
        return ticks / TICKS_PER_SECOND - 62_135_596_800.0

    def charge_mah(self) -> np.ndarray:
        """``charge_q`` in mAh regardless of how the instrument stored it."""
        return self._to_mah(self.data["charge_q"])

    def discharge_mah(self) -> np.ndarray:
        return self._to_mah(self.data["discharge_q"])

    def _to_mah(self, values: np.ndarray) -> np.ndarray:
        # UnitCoulomb selects coulombs over amp-hours in the acquisition file.
        factor = 1000.0 / 3600.0 if self.metadata.unit_coulomb else 1000.0
        return values * factor

    def energy_wh(self, column: str) -> np.ndarray:
        values = self.data[column]
        return values / 3600.0 if self.metadata.unit_coulomb else values


def _member(stream: NrbfStream, obj: NrbfObject | None, name: str) -> Any:
    """Read a member by name, whether it is an auto-property or a plain field.

    C# auto-properties serialize as ``<Name>k__BackingField``; plain fields
    (e.g. on ``System.UnitySerializationHolder``) keep their own name.
    """
    if not isinstance(obj, NrbfObject):
        return None
    members = obj.members
    key = f"<{name}>k__BackingField"
    if key not in members:
        key = name
    return resolve(stream, members.get(key))


def _list_items(stream: NrbfStream, obj: NrbfObject | None) -> list[Any]:
    if not isinstance(obj, NrbfObject):
        return []
    items = resolve(stream, obj.members.get("_items")) or []
    size = obj.members.get("_size") or 0
    return [resolve(stream, item) for item in items[:size]]


def _ticks_to_datetime(ticks: int | None) -> datetime.datetime | None:
    if ticks is None or ticks <= 0:
        return None
    try:
        return _DOTNET_EPOCH + datetime.timedelta(microseconds=ticks // 10)
    except OverflowError:
        return None


def _read_columns(stream: NrbfStream, header: NrbfObject) -> list[WrdColumn]:
    columns: list[WrdColumn] = []
    for info in _list_items(stream, _member(stream, header, "ColumnList")):
        label = _member(stream, info, "Name") or ""
        unit = _member(stream, info, "Unit") or ""
        type_obj = _member(stream, info, "DataType")
        dotnet_type = _member(stream, type_obj, "Data") or ""
        columns.append(WrdColumn(_slug(label), label, dotnet_type, unit))
    return columns


@dataclass
class _Layout:
    """Byte layout of one raw data row."""

    fields: list[tuple[str, str, int]]  # (name, numpy dtype, offset)
    string_fields: list[tuple[str, int]]  # (name, offset of the length prefix)
    fixed_size: int  # row size with every string empty

    @classmethod
    def build(cls, columns: list[WrdColumn]) -> _Layout:
        fields: list[tuple[str, str, int]] = []
        strings: list[tuple[str, int]] = []
        offset = 0
        for column in columns:
            if column.is_string:
                strings.append((column.name, offset))
                offset += 1  # the length prefix, assuming a one-byte length
                continue
            dtype = column.numpy_dtype
            if dtype is None:
                raise WrdError(
                    f"column {column.label!r} has unsupported type {column.dotnet_type!r}"
                )
            fields.append((column.name, dtype, offset))
            offset += np.dtype(dtype).itemsize
        return cls(fields, strings, offset)


def _scan_rows(buf: bytes, start: int, layout: _Layout
               ) -> tuple[list[int], list[tuple[int, ...]], int]:
    """Walk the data block once, recording where every row starts.

    Returns ``(offsets, shapes, end)`` where a *shape* is the tuple of string
    lengths in that row -- rows sharing a shape share a byte layout.  Scanning
    stops at the first row that cannot be a valid record, so a trailing footer
    is never misread as data.
    """
    offsets: list[int] = []
    shapes: list[tuple[int, ...]] = []
    total = len(buf)
    pos = start
    string_offsets = [off for _, off in layout.string_fields]

    while pos + layout.fixed_size <= total:
        size = layout.fixed_size
        lengths: list[int] = []
        ok = True
        for str_off in string_offsets:
            # With more than one string column the earlier strings push this
            # prefix past ``fixed_size``, so the loop guard above does not
            # cover it; a short tail must stop the scan, not raise IndexError.
            prefix = pos + str_off + (size - layout.fixed_size)
            if prefix >= total:
                ok = False
                break
            length = buf[prefix]
            if length & 0x80:
                # A multi-byte 7-bit prefix means >=128 chars: far longer than
                # any current-range label, so this is not a data row.
                ok = False
                break
            lengths.append(length)
            size += length
        if not ok or pos + size > total:
            break
        offsets.append(pos)
        shapes.append(tuple(lengths))
        pos += size

    return offsets, shapes, pos


def _run_dtype(layout: _Layout, shape: tuple[int, ...]) -> tuple[np.dtype, dict[str, int]]:
    """Build the numpy record dtype for rows whose strings have *shape* lengths."""
    names, formats, offsets = [], [], []
    string_starts: dict[str, int] = {}
    shift = 0
    string_index = 0
    cursor = 0
    for name, dtype, offset in layout.fields:
        # Absorb every string column that precedes this field.
        while (string_index < len(layout.string_fields)
               and layout.string_fields[string_index][1] < offset):
            string_starts[layout.string_fields[string_index][0]] = (
                layout.string_fields[string_index][1] + shift + 1
            )
            shift += shape[string_index]
            string_index += 1
        names.append(name)
        formats.append(dtype)
        offsets.append(offset + shift)
        cursor = offset + shift + np.dtype(dtype).itemsize
    while string_index < len(layout.string_fields):
        string_starts[layout.string_fields[string_index][0]] = (
            layout.string_fields[string_index][1] + shift + 1
        )
        shift += shape[string_index]
        string_index += 1
    itemsize = max(cursor, layout.fixed_size + sum(shape))

    for name, length in zip(
            (n for n, _ in layout.string_fields), shape, strict=True):
        if length:
            names.append(name)
            formats.append(f"S{length}")
            offsets.append(string_starts[name])

    record = np.dtype({"names": names, "formats": formats,
                       "offsets": offsets, "itemsize": itemsize})
    return record, string_starts


def _decode_utf8(values: np.ndarray) -> list[str]:
    """Decode one fixed-width bytes column of a run.

    numpy's ``S`` -> ``U`` cast is ASCII-only, so a perfectly legal label such
    as ``100µA`` would crash the whole parse; it also drops trailing ``NUL``
    bytes, which here are content rather than padding because the field width
    comes from the row's own 7-bit length prefix.
    """
    width = values.dtype.itemsize
    raw = values.tobytes()
    try:
        return [raw[i:i + width].decode("utf-8") for i in range(0, len(raw), width)]
    except UnicodeDecodeError as exc:
        raise WrdError(f"string column is not valid UTF-8: {exc}") from exc


def _read_block(buf: bytes, offsets: list[int], shapes: list[tuple[int, ...]],
                layout: _Layout, columns: list[WrdColumn]) -> dict[str, np.ndarray]:
    """Materialise the scanned rows into one numpy array per column."""
    count = len(offsets)
    out: dict[str, np.ndarray] = {}
    for column in columns:  # keep the instrument's declared column order
        if column.is_string:
            out[column.name] = np.empty(count, dtype=object)
        else:
            out[column.name] = np.empty(count, dtype=np.dtype(column.numpy_dtype))
    if not count:
        return {name: (arr.astype(str) if arr.dtype == object else arr)
                for name, arr in out.items()}

    # Rows of one shape sit in contiguous runs -- the current range only
    # changes when the instrument switches range -- so a single structured
    # read per run replaces a per-row Python loop.
    start = 0
    while start < count:
        shape = shapes[start]
        end = start + 1
        while end < count and shapes[end] == shape:
            end += 1

        record, _ = _run_dtype(layout, shape)
        block = np.frombuffer(buf, dtype=record, count=end - start, offset=offsets[start])
        for name in record.names:
            values = block[name]
            if values.dtype.kind == "S":
                out[name][start:end] = _decode_utf8(values)
            else:
                out[name][start:end] = values
        # A zero-length string column has no field in the record dtype.
        for (name, _), length in zip(layout.string_fields, shape, strict=True):
            if not length:
                out[name][start:end] = ""

        start = end

    for name, _ in layout.string_fields:
        out[name] = out[name].astype(str)
    return out


def read_wrd(path: str | Path, *, load_data: bool = True) -> WrdFile:
    """Parse a ``.wrd`` file into metadata plus per-column numpy arrays."""
    path = Path(path)
    buf = path.read_bytes()
    return read_wrd_bytes(buf, source_name=path.name, load_data=load_data)


def read_wrd_bytes(buf: bytes, *, source_name: str = "<bytes>",
                   load_data: bool = True) -> WrdFile:
    """Parse ``.wrd`` content already held in memory."""
    if len(buf) < 32 or buf[0] != 0:
        raise WrdError("not a .wrd file: missing NRBF serialization header")

    # NrbfError is a sibling of WrdError, not a subclass, so an unwrapped one
    # escapes every caller that guards the library boundary on "unreadable
    # .wrd" -- a truncated upload became a 500 instead of a 422.
    try:
        file_stream = read_stream(buf, 0)
    except NrbfError as exc:
        raise WrdError(f"not a readable .wrd: {exc}") from exc
    file_header = file_stream.root
    if not isinstance(file_header, NrbfObject):
        raise WrdError(
            f"unexpected root object of type {type(file_header).__name__}; "
            "expected WbcsFile.Data.DataFileHeader"
        )
    if "DataFileHeader" not in file_header.class_name:
        raise WrdError(
            f"unexpected root object {file_header.class_name!r}; "
            "expected WbcsFile.Data.DataFileHeader"
        )

    try:
        data_stream = read_stream(buf, file_stream.end_offset)
    except NrbfError as exc:
        raise WrdError(f"not a readable .wrd: {exc}") from exc
    data_header = data_stream.root
    if not isinstance(data_header, NrbfObject) or "DataHeader" not in data_header.class_name:
        raise WrdError("missing WbcsFile.Data.DataHeader stream")

    report = _member(file_stream, file_header, "StartReport")
    format_obj = _member(file_stream, file_header, "Format")
    data_format = (format_obj.members.get("value__", 0)
                   if isinstance(format_obj, NrbfObject) else 0)

    start_dt = _member(file_stream, file_header, "StartTime")
    declared_rows = data_header.members.get("<DataCount>k__BackingField")
    end_ticks = data_header.members.get("<EndTime>k__BackingField")

    columns = _read_columns(data_stream, data_header)
    if not columns:
        raise WrdError("file declares no data columns")

    metadata = WrdMetadata(
        source_name=source_name,
        sha256=hashlib.sha256(buf).hexdigest(),
        file_size=len(buf),
        wrd_version=_member(file_stream, file_header, "Version"),
        model=_member(file_stream, file_header, "Model"),
        serial_no=_member(file_stream, file_header, "SerialNo"),
        order_no=_member(file_stream, file_header, "OrderNo"),
        device_type=_member(file_stream, file_header, "DeviceType"),
        app_version=_member(file_stream, file_header, "AppVer"),
        firmware_version=_member(file_stream, file_header, "FirmVer"),
        base_tick=_member(file_stream, file_header, "BaseTick"),
        unit_coulomb=bool(_member(file_stream, file_header, "UnitCoulomb")),
        data_format=data_format,
        start_time=start_dt.to_datetime() if start_dt is not None else None,
        end_time=_ticks_to_datetime(end_ticks if isinstance(end_ticks, int) else None),
        instrument_path=_member(file_stream, file_header, "FileName"),
        declared_row_count=declared_rows if isinstance(declared_rows, int) and declared_rows >= 0 else None,
        cell_weight_g=_member(file_stream, report, "CellWeight"),
        electrode_area_cm2=_member(file_stream, report, "ElectrodeArea"),
        cell_capacity_ah=_member(file_stream, report, "CellCapacity"),
        cell_type=_member(file_stream, report, "CellType") or None,
        memo=_member(file_stream, report, "Memo") or None,
        schedule=read_schedule(file_stream, file_header),
        columns=columns,
    )
    if metadata.schedule:
        metadata.schedule_path = metadata.schedule.source_path

    layout = _Layout.build(columns)
    offsets, shapes, end = _scan_rows(buf, data_stream.end_offset, layout)
    metadata.row_count = len(offsets)
    metadata.trailing_bytes = len(buf) - end

    data: dict[str, np.ndarray] = {}
    if load_data:
        data = _read_block(buf, offsets, shapes, layout, columns)
        if "channel" in data and len(data["channel"]):
            metadata.channel = int(data["channel"][0])
        if metadata.end_time is None and "date_time" in data and len(data["date_time"]):
            metadata.end_time = _ticks_to_datetime(int(data["date_time"][-1]))

    return WrdFile(metadata, data)
