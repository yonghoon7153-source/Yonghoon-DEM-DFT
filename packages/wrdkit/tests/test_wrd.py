"""Reading a .wrd into columns."""

import numpy as np
import pytest

from wrdkit import WrdError, read_wrd_bytes

import synthetic


def test_row_count_and_no_trailing_bytes(synthetic_wrd):
    # 3 cycles x (40 charge + 3 rest + 40 discharge + 3 rest)
    assert len(synthetic_wrd) == 3 * (40 + 3 + 40 + 3)
    assert synthetic_wrd.metadata.trailing_bytes == 0


def test_columns_keep_the_instrument_declared_order(synthetic_wrd):
    expected = [
        "date_time", "channel", "test_time", "step_time", "cycle_time",
        "step_index", "total_step", "cycle_index", "run_status",
        "running_status", "cell_status", "i_range_index", "i_range",
        "voltage", "current", "charge_q", "discharge_q", "charge_e",
        "discharge_e", "aux_voltage", "temperature", "ocp",
    ]
    assert synthetic_wrd.columns == expected


def test_variable_width_rows_are_read_correctly(synthetic_wrd):
    """The current-range column changes length mid-file, so rows resize."""
    ranges = synthetic_wrd["i_range"]
    assert set(ranges.tolist()) == {"1A", "10mA"}
    # Cycle 0 is logged on the 1A range, later cycles on 10mA.
    first_cycle = synthetic_wrd["cycle_index"] == 0
    assert set(ranges[first_cycle].tolist()) == {"1A"}
    assert set(ranges[~first_cycle].tolist()) == {"10mA"}


def test_voltage_and_current_survive_the_resize(synthetic_wrd):
    voltage = synthetic_wrd["voltage"]
    assert voltage.dtype == np.float64
    assert voltage.min() == pytest.approx(1.9)
    assert voltage.max() == pytest.approx(3.6)
    current = synthetic_wrd["current"]
    assert current.max() == pytest.approx(1e-3)
    assert current.min() == pytest.approx(-1e-3)


def test_ticks_convert_to_seconds(synthetic_wrd):
    seconds = synthetic_wrd.seconds("test_time")
    assert seconds[0] == pytest.approx(0.0)
    assert seconds[1] - seconds[0] == pytest.approx(10.0)


def test_capacity_is_reported_in_mah(synthetic_wrd):
    assert synthetic_wrd.discharge_mah().max() == pytest.approx(5.0)


def test_coulomb_files_are_converted_to_mah():
    data = synthetic.build_wrd(synthetic.make_cycles(1, 10))
    wrd = read_wrd_bytes(data)
    wrd.metadata.unit_coulomb = True
    # The column holds 0.005 (5 mAh as Ah).  Read as coulombs that is
    # 0.005 C = 0.005 / 3.6 mAh.
    assert wrd.discharge_mah().max() == pytest.approx(0.005 / 3.6, rel=1e-9)


def test_operator_cell_data_defaults_are_recognised_as_unset(synthetic_wrd):
    assert synthetic_wrd.metadata.has_operator_cell_data is False


def test_start_time_is_decoded(synthetic_wrd):
    assert synthetic_wrd.metadata.start_time.year == 2023


def test_rejects_a_non_wrd_file():
    with pytest.raises(WrdError, match="not a .wrd file"):
        read_wrd_bytes(b"PK\x03\x04" + b"\x00" * 64)


def test_rejects_a_truncated_header():
    with pytest.raises(WrdError):
        read_wrd_bytes(b"\x00" * 8)


def test_non_ascii_range_labels_survive_the_read():
    """The spec declares I RANGE as UTF-8; a µA label must not kill the parse."""
    samples = synthetic.make_cycles(1, 5)
    for sample in samples:
        sample.i_range = "100µA"
    wrd = read_wrd_bytes(synthetic.build_wrd(samples))
    assert set(wrd["i_range"].tolist()) == {"100µA"}


def test_truncated_file_raises_wrd_error_not_nrbf_error():
    data = synthetic.build_wrd(synthetic.make_cycles(1, 5))
    with pytest.raises(WrdError):
        read_wrd_bytes(data[:200])


def test_non_object_root_raises_wrd_error():
    """A valid NRBF stream whose root is a string is not a .wrd."""
    writer = synthetic.Writer()
    writer.u8(synthetic.HEADER).i32(1).i32(-1).i32(1).i32(0)
    writer.u8(synthetic.BINARY_OBJECT_STRING).i32(1).string("x" * 40)
    writer.u8(synthetic.MESSAGE_END)
    with pytest.raises(WrdError, match="unexpected root object"):
        read_wrd_bytes(writer.bytes())


class _NotedSample:
    """A row with a second String column appended after the declared 22."""

    def __init__(self, sample, note: str) -> None:
        self.sample = sample
        self.note = note

    def pack(self) -> bytes:
        return self.sample.pack() + synthetic.Writer().string(self.note).bytes()


def test_a_short_tail_stops_the_scan_with_two_string_columns():
    columns = synthetic.DEFAULT_COLUMNS + [("NOTE", "System.String")]
    rows = [_NotedSample(s, "ok") for s in synthetic.make_cycles(1, 5)]
    data = synthetic.build_wrd(rows, columns=columns)
    # Clip the last row to exactly fixed_size: the row-start guard still passes
    # but the NOTE length prefix now sits one byte past the buffer.
    fixed_size = 129
    data = data[:len(data) - (len(rows[-1].pack()) - fixed_size)]

    wrd = read_wrd_bytes(data)
    assert len(wrd) == len(rows) - 1
    assert wrd.metadata.trailing_bytes == fixed_size


def test_metadata_records_a_content_hash(synthetic_bytes, synthetic_wrd):
    import hashlib

    assert synthetic_wrd.metadata.sha256 == hashlib.sha256(synthetic_bytes).hexdigest()


def test_ticks_are_independent_of_the_machine_timezone():
    """계측기는 벽시계를 그대로 tick 으로 쓴다 — 변환에 시간대가 끼면 안 된다.

    `datetime.timestamp()` 를 쓰면 naive 값을 로컬로 읽고 UTC 로 바꾸므로,
    UTC+9 랩에서 픽스처가 9시간 과거로 기록된다. 그러면 running 으로 쓴
    셀이 finished 로 파싱되고, CI(UTC)는 통과하는데 연구자 기계에서만
    깨진다.
    """
    import datetime
    import os
    import time

    if not hasattr(time, "tzset"):
        pytest.skip("changing the process time zone needs a POSIX platform")

    moment = datetime.datetime(2026, 3, 4, 22, 47, 31)
    original = os.environ.get("TZ")
    seen = set()
    try:
        for zone in ("UTC", "Asia/Seoul", "America/Los_Angeles"):
            os.environ["TZ"] = zone
            time.tzset()
            seen.add(synthetic.ticks_at(moment))
    finally:
        if original is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = original
        time.tzset()

    assert len(seen) == 1, "같은 벽시계가 시간대마다 다른 tick 이 됐다"


def test_a_wall_clock_survives_the_round_trip_through_a_file():
    """파일에 쓴 시각이 파서를 거쳐 같은 벽시계로 돌아온다."""
    import datetime

    moment = datetime.datetime(2026, 3, 4, 22, 47, 31)
    ticks = synthetic.ticks_at(moment)
    raw = synthetic.build_wrd(
        synthetic.make_cycles(1, 5, start_ticks=ticks), start_ticks=ticks)
    parsed = read_wrd_bytes(raw)
    assert parsed.metadata.start_time.replace(microsecond=0) == moment


def test_a_cv_step_records_a_voltage_not_a_current():
    """CV 스텝의 Value 는 전압이다.

    오래 틀려 있었는데 드러날 파일이 없었다: multi-step CCCV 를 CC/CV 스텝으로
    번갈아 쓴 실측 파일(SIF 2.13)이 처음으로 `4.25` 를 **4.25 A** 로 만들었다.
    그 값은 화면의 C-rate 자동 채움까지 타고 들어가서, 사람이 입력하지도 않은
    숫자가 바뀐다.
    """
    steps = (synthetic.SchedStep(name="cc", control=0, value=0.35),
             synthetic.SchedStep(name="cv", control=1, value=4.25))
    data = synthetic.build_wrd(synthetic.make_cycles(1, 5), schedule=steps)
    schedule = read_wrd_bytes(data, source_name="a.wrd").metadata.schedule
    cc, cv = schedule.steps
    assert cc.current_a == pytest.approx(0.35)
    assert cc.voltage_limit_v is None
    # 여기가 요점이다 — 전압이 전류 칸에 들어가면 안 된다.
    assert cv.current_a is None
    assert cv.voltage_limit_v == pytest.approx(4.25)
