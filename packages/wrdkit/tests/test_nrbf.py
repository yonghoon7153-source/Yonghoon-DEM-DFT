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


def test_seven_bit_length_prefix_handles_long_strings():
    from wrdkit.nrbf import _Reader

    text = "x" * 300
    writer = synthetic.Writer().string(text)
    assert _Reader(writer.bytes()).string() == text
