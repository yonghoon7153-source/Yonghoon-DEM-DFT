"""MS-NRBF reader behaviour, exercised through a written-then-read stream."""

import pytest

from wrdkit.nrbf import NrbfError, read_stream, resolve

import synthetic


def test_reads_the_file_header_stream(synthetic_bytes):
    stream = read_stream(synthetic_bytes, 0)
    header = stream.root
    assert "DataFileHeader" in header.class_name
    assert header.members["<Model>k__BackingField"] == "WBCS3000S1"
    assert header.members["<BaseTick>k__BackingField"] == 50_000
    assert header.members["<UnitCoulomb>k__BackingField"] is False


def test_stops_at_message_end_so_the_next_stream_can_follow(synthetic_bytes):
    first = read_stream(synthetic_bytes, 0)
    assert 0 < first.end_offset < len(synthetic_bytes)
    second = read_stream(synthetic_bytes, first.end_offset)
    assert "DataHeader" in second.root.class_name
    assert second.end_offset > first.end_offset


def test_resolves_forward_references(synthetic_bytes):
    first = read_stream(synthetic_bytes, 0)
    stream = read_stream(synthetic_bytes, first.end_offset)
    # ColumnList is written as a MemberReference to an object defined later.
    column_list = resolve(stream, stream.root.members["<ColumnList>k__BackingField"])
    assert column_list.members["_size"] == len(synthetic.DEFAULT_COLUMNS)


def test_rejects_an_unknown_record_type():
    with pytest.raises(NrbfError, match="unknown record type"):
        read_stream(bytes([99, 0, 0, 0, 0]))


def test_rejects_a_truncated_stream():
    with pytest.raises(NrbfError, match="truncated"):
        read_stream(bytes([0, 1, 0]))


def _stream_header(writer, root_id=1):
    return writer.u8(synthetic.HEADER).i32(root_id).i32(-1).i32(1).i32(0)


def test_binary_library_in_a_member_value_position_is_not_the_value():
    """BinaryFormatter emits libraries lazily, so one can precede a member value."""
    writer = synthetic.Writer()
    _stream_header(writer)
    writer.u8(synthetic.BINARY_LIBRARY).i32(2).string(synthetic.WBCS_LIBRARY)
    synthetic._class_record(writer, 1, "Outer", [
        ("Child", synthetic.BT_CLASS, ("Inner", 3)),
        ("Tag", synthetic.BT_PRIMITIVE, synthetic.P_INT32),
    ], library_id=2)
    # The Inner class lives in a second assembly, declared right before it.
    writer.u8(synthetic.BINARY_LIBRARY).i32(3).string("Other, Version=1.0.0.0")
    synthetic._class_record(writer, 4, "Inner", [
        ("N", synthetic.BT_PRIMITIVE, synthetic.P_INT32),
    ], library_id=3)
    writer.i32(7)
    writer.i32(42)
    writer.u8(synthetic.MESSAGE_END)

    root = read_stream(writer.bytes()).root
    assert root.members["Child"].members["N"] == 7
    assert root.members["Tag"] == 42


def test_binary_library_between_array_items_is_not_an_item():
    writer = synthetic.Writer()
    _stream_header(writer)
    writer.u8(synthetic.BINARY_LIBRARY).i32(2).string(synthetic.WBCS_LIBRARY)
    writer.u8(synthetic.ARRAY_SINGLE_OBJECT).i32(1).i32(2)
    writer.u8(synthetic.BINARY_LIBRARY).i32(3).string("Other, Version=1.0.0.0")
    writer.u8(synthetic.BINARY_OBJECT_STRING).i32(5).string("hello")
    writer.u8(synthetic.BINARY_OBJECT_STRING).i32(6).string("world")
    writer.u8(synthetic.MESSAGE_END)

    assert read_stream(writer.bytes()).root == ["hello", "world"]


def test_rejects_a_truncated_primitive_array():
    writer = synthetic.Writer()
    _stream_header(writer)
    writer.u8(15).i32(1).i32(100).u8(synthetic.P_DOUBLE)  # ArraySinglePrimitive
    writer.f64(1.0)                                       # ...but only one item
    with pytest.raises(NrbfError, match="truncated"):
        read_stream(writer.bytes())


@pytest.mark.parametrize("tail", [b"", b"\xc2"])
def test_rejects_a_char_truncated_at_the_buffer_end(tail):
    writer = synthetic.Writer()
    _stream_header(writer)
    writer.u8(8).u8(3)  # MemberPrimitiveTyped, Char
    writer.raw(tail)
    with pytest.raises(NrbfError, match="truncated"):
        read_stream(writer.bytes())


def test_seven_bit_length_prefix_handles_long_strings():
    from wrdkit.nrbf import _Reader

    text = "x" * 300
    writer = synthetic.Writer().string(text)
    assert _Reader(writer.bytes()).string() == text
