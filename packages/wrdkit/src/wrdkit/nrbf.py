"""Reader for the .NET Remoting Binary Format (MS-NRBF).

``.wrd`` files produced by WonATech / Zive ``Smart Interface`` (WBCS3000)
begin with one or more ``BinaryFormatter`` streams that carry the acquisition
metadata.  Nothing in the Python ecosystem reads that format, so this module
implements the subset of [MS-NRBF] the instrument actually emits.

Only the record types WonATech writes are supported; anything else raises
:class:`NrbfError` rather than silently mis-parsing.

Reference: [MS-NRBF] .NET Remoting: Binary Format Data Structure.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import Any

__all__ = ["NrbfError", "NrbfObject", "NrbfStream", "read_stream", "resolve"]


class NrbfError(ValueError):
    """Raised when a byte sequence is not valid MS-NRBF."""


# --- record type enumeration (MS-NRBF 2.1.2.1) -----------------------------
_SERIALIZED_STREAM_HEADER = 0
_CLASS_WITH_ID = 1
_SYSTEM_CLASS_WITH_MEMBERS = 2
_CLASS_WITH_MEMBERS = 3
_SYSTEM_CLASS_WITH_MEMBERS_AND_TYPES = 4
_CLASS_WITH_MEMBERS_AND_TYPES = 5
_BINARY_OBJECT_STRING = 6
_BINARY_ARRAY = 7
_MEMBER_PRIMITIVE_TYPED = 8
_MEMBER_REFERENCE = 9
_OBJECT_NULL = 10
_MESSAGE_END = 11
_BINARY_LIBRARY = 12
_OBJECT_NULL_MULTIPLE_256 = 13
_OBJECT_NULL_MULTIPLE = 14
_ARRAY_SINGLE_PRIMITIVE = 15
_ARRAY_SINGLE_OBJECT = 16
_ARRAY_SINGLE_STRING = 17

# --- primitive type enumeration (MS-NRBF 2.1.2.3) --------------------------
PRIMITIVE_NAMES = {
    1: "Boolean", 2: "Byte", 3: "Char", 5: "Decimal", 6: "Double", 7: "Int16",
    8: "Int32", 9: "Int64", 10: "SByte", 11: "Single", 12: "TimeSpan",
    13: "DateTime", 14: "UInt16", 15: "UInt32", 16: "UInt64", 18: "String",
}

_STRUCT_CHAR = {
    1: "?", 2: "B", 6: "d", 7: "h", 8: "i", 9: "q", 10: "b", 11: "f",
    12: "q", 14: "H", 15: "I", 16: "Q",
}

# .NET DateTime stores 62 bits of ticks plus a 2-bit DateTimeKind.
_TICK_MASK = (1 << 62) - 1


@dataclass
class ClassInfo:
    """Type metadata shared by every instance of one serialized class."""

    name: str
    members: list[str]
    member_types: list[tuple[str, Any]] | None
    library_id: int | None = None

    @property
    def short_name(self) -> str:
        """``WbcsFile.Data.DataHeader, WbcsFile, ...`` -> ``DataHeader``."""
        return self.name.split(",")[0].split("+")[-1].rsplit(".", 1)[-1]


@dataclass
class NrbfObject:
    """One deserialized .NET object: a class name plus its member values."""

    class_info: ClassInfo
    object_id: int
    members: dict[str, Any] = field(default_factory=dict)

    @property
    def class_name(self) -> str:
        return self.class_info.name

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<NrbfObject {self.class_info.short_name} id={self.object_id}>"


@dataclass
class Reference:
    """A forward or backward reference to another object in the same stream."""

    object_id: int


@dataclass
class NrbfStream:
    """One complete BinaryFormatter stream and everything it defined."""

    root_id: int
    objects: dict[int, Any]
    end_offset: int

    @property
    def root(self) -> Any:
        return self.objects.get(self.root_id)


class _Reader:
    """Cursor over a bytes buffer with the primitive readers MS-NRBF needs."""

    def __init__(self, buf: bytes, offset: int = 0) -> None:
        self.buf = buf
        self.pos = offset
        self.objects: dict[int, Any] = {}
        self.classes: dict[int, ClassInfo] = {}
        self.libraries: dict[int, str] = {}
        self.root_id: int = 0

    # -- primitives ---------------------------------------------------------
    def _unpack(self, fmt: str, size: int):
        try:
            value = struct.unpack_from(fmt, self.buf, self.pos)[0]
        except struct.error as exc:  # pragma: no cover - corrupt input
            raise NrbfError(f"truncated stream at offset {self.pos}") from exc
        self.pos += size
        return value

    def u8(self) -> int:
        if self.pos >= len(self.buf):
            raise NrbfError(f"truncated stream at offset {self.pos}")
        value = self.buf[self.pos]
        self.pos += 1
        return value

    def i32(self) -> int:
        return self._unpack("<i", 4)

    def u32(self) -> int:
        return self._unpack("<I", 4)

    def i64(self) -> int:
        return self._unpack("<q", 8)

    def u64(self) -> int:
        return self._unpack("<Q", 8)

    def string(self) -> str:
        """Length-prefixed UTF-8 string; the length is a 7-bit encoded int."""
        length = 0
        shift = 0
        while True:
            byte = self.u8()
            length |= (byte & 0x7F) << shift
            if not byte & 0x80:
                break
            shift += 7
            if shift > 35:
                raise NrbfError(f"bad 7-bit length prefix at offset {self.pos}")
        raw = self.buf[self.pos:self.pos + length]
        if len(raw) != length:
            raise NrbfError(f"truncated string at offset {self.pos}")
        self.pos += length
        return raw.decode("utf-8", "replace")

    def primitive(self, kind: int) -> Any:
        if kind == 3:  # Char, stored as 1-4 UTF-8 bytes
            first = self.buf[self.pos]
            width = 1 if first < 0x80 else 2 if first < 0xE0 else 3 if first < 0xF0 else 4
            raw = self.buf[self.pos:self.pos + width]
            self.pos += width
            return raw.decode("utf-8", "replace")
        if kind == 5:  # Decimal, serialized as its invariant string form
            return self.string()
        if kind == 18:
            return self.string()
        if kind == 13:  # DateTime -> ticks since 0001-01-01, plus a Kind
            raw = self.u64()
            return DotNetDateTime(raw & _TICK_MASK, raw >> 62)
        char = _STRUCT_CHAR.get(kind)
        if char is None:
            raise NrbfError(f"unsupported primitive type {kind} at offset {self.pos}")
        return self._unpack("<" + char, struct.calcsize("<" + char))

    def primitive_array(self, kind: int, count: int) -> list[Any]:
        char = _STRUCT_CHAR.get(kind)
        if char is None:
            return [self.primitive(kind) for _ in range(count)]
        size = struct.calcsize("<" + char)
        values = list(struct.unpack_from(f"<{count}{char}", self.buf, self.pos))
        self.pos += size * count
        return values

    # -- type metadata ------------------------------------------------------
    def _member_type(self, binary_type: int) -> tuple[str, Any]:
        if binary_type == 0:
            return ("primitive", self.u8())
        if binary_type == 1:
            return ("string", None)
        if binary_type == 2:
            return ("object", None)
        if binary_type == 3:
            return ("system_class", self.string())
        if binary_type == 4:
            return ("class", (self.string(), self.i32()))
        if binary_type == 5:
            return ("object_array", None)
        if binary_type == 6:
            return ("string_array", None)
        if binary_type == 7:
            return ("primitive_array", self.u8())
        raise NrbfError(f"unknown BinaryTypeEnum {binary_type} at offset {self.pos}")

    # -- records ------------------------------------------------------------
    def _class_values(self, obj: NrbfObject) -> None:
        info = obj.class_info
        types = info.member_types or [None] * len(info.members)
        # A mismatch means the member list and the type list disagree,
        # i.e. a malformed stream; strict makes that an error rather than
        # a silent truncation that shifts every following offset.
        for name, member_type in zip(info.members, types, strict=True):
            if member_type is not None and member_type[0] == "primitive":
                obj.members[name] = self.primitive(member_type[1])
            else:
                obj.members[name] = self.record()

    def _read_class(self, record_type: int) -> NrbfObject:
        object_id = self.i32()
        name = self.string()
        count = self.i32()
        members = [self.string() for _ in range(count)]
        member_types = None
        if record_type in (_SYSTEM_CLASS_WITH_MEMBERS_AND_TYPES, _CLASS_WITH_MEMBERS_AND_TYPES):
            binary_types = [self.u8() for _ in range(count)]
            member_types = [self._member_type(bt) for bt in binary_types]
        library_id = None
        if record_type in (_CLASS_WITH_MEMBERS, _CLASS_WITH_MEMBERS_AND_TYPES):
            library_id = self.i32()
        info = ClassInfo(name, members, member_types, library_id)
        self.classes[object_id] = info
        obj = NrbfObject(info, object_id)
        self.objects[object_id] = obj
        self._class_values(obj)
        return obj

    def _collect(self, out: list[Any], total: int) -> None:
        """Read array items, expanding the run-length null records."""
        while len(out) < total:
            value = self.record()
            if isinstance(value, _NullRun):
                out.extend([None] * value.count)
            else:
                out.append(value)

    def record(self) -> Any:
        record_type = self.u8()

        if record_type == _SERIALIZED_STREAM_HEADER:
            self.root_id = self.i32()
            self.i32()  # header id
            major, minor = self.i32(), self.i32()
            if (major, minor) != (1, 0):
                raise NrbfError(f"unsupported NRBF version {major}.{minor}")
            return _Skip

        if record_type == _BINARY_LIBRARY:
            library_id = self.i32()
            self.libraries[library_id] = self.string()
            return _Skip

        if record_type in (
            _SYSTEM_CLASS_WITH_MEMBERS, _CLASS_WITH_MEMBERS,
            _SYSTEM_CLASS_WITH_MEMBERS_AND_TYPES, _CLASS_WITH_MEMBERS_AND_TYPES,
        ):
            return self._read_class(record_type)

        if record_type == _CLASS_WITH_ID:
            object_id = self.i32()
            metadata_id = self.i32()
            info = self.classes.get(metadata_id)
            if info is None:
                raise NrbfError(f"ClassWithId references unknown metadata {metadata_id}")
            obj = NrbfObject(info, object_id)
            self.objects[object_id] = obj
            self._class_values(obj)
            return obj

        if record_type == _BINARY_OBJECT_STRING:
            object_id = self.i32()
            value = self.string()
            self.objects[object_id] = value
            return value

        if record_type == _BINARY_ARRAY:
            object_id = self.i32()
            array_kind = self.u8()
            rank = self.i32()
            lengths = [self.i32() for _ in range(rank)]
            if array_kind in (3, 4, 5):  # the *Offset variants carry lower bounds
                for _ in range(rank):
                    self.i32()
            member_type = self._member_type(self.u8())
            total = 1
            for length in lengths:
                total *= length
            if member_type[0] == "primitive":
                values = self.primitive_array(member_type[1], total)
            else:
                values = []
                self._collect(values, total)
            self.objects[object_id] = values
            return values

        if record_type == _MEMBER_PRIMITIVE_TYPED:
            return self.primitive(self.u8())

        if record_type == _MEMBER_REFERENCE:
            return Reference(self.i32())

        if record_type == _OBJECT_NULL:
            return None

        if record_type == _MESSAGE_END:
            return _MessageEnd

        if record_type == _OBJECT_NULL_MULTIPLE_256:
            return _NullRun(self.u8())

        if record_type == _OBJECT_NULL_MULTIPLE:
            return _NullRun(self.i32())

        if record_type == _ARRAY_SINGLE_PRIMITIVE:
            object_id = self.i32()
            length = self.i32()
            values = self.primitive_array(self.u8(), length)
            self.objects[object_id] = values
            return values

        if record_type in (_ARRAY_SINGLE_OBJECT, _ARRAY_SINGLE_STRING):
            object_id = self.i32()
            length = self.i32()
            values: list[Any] = []
            self._collect(values, length)
            self.objects[object_id] = values
            return values

        raise NrbfError(f"unknown record type {record_type} at offset {self.pos - 1}")


class _Sentinel:
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:  # pragma: no cover
        return self.name


_Skip = _Sentinel("<skip>")
_MessageEnd = _Sentinel("<message-end>")


@dataclass
class _NullRun:
    count: int


@dataclass(frozen=True)
class DotNetDateTime:
    """A .NET ``DateTime``: ticks of 100 ns since 0001-01-01 plus a Kind."""

    ticks: int
    kind: int

    def to_datetime(self):
        """Convert to :class:`datetime.datetime` (naive, as recorded)."""
        import datetime

        return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=self.ticks // 10)


def read_stream(buf: bytes, offset: int = 0) -> NrbfStream:
    """Read one BinaryFormatter stream starting at *offset*.

    Stops after the ``MessageEnd`` record so the caller can continue reading
    whatever follows in the same file.
    """
    reader = _Reader(buf, offset)
    while reader.pos < len(buf):
        value = reader.record()
        if value is _MessageEnd:
            break
    return NrbfStream(reader.root_id, reader.objects, reader.pos)


def resolve(stream: NrbfStream, value: Any, _depth: int = 0) -> Any:
    """Follow :class:`Reference` values until a concrete object is reached."""
    while isinstance(value, Reference):
        if _depth > 64:
            raise NrbfError("reference chain too deep")
        value = stream.objects.get(value.object_id)
        _depth += 1
    return value
