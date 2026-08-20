"""Reading a .wrd into columns."""

import numpy as np
import pytest

import synthetic
from wrdkit import WrdError, read_wrd_bytes


def test_row_count_and_no_trailing_bytes(synthetic_wrd):
    # 3 cycles x (40 charge + 40 discharge + 3 rest)
    assert len(synthetic_wrd) == 3 * (40 + 40 + 3)
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
    # 1 mAh == 3.6 C, so a coulomb-valued column reads 1/3.6 of the amp-hour one.
    assert wrd.discharge_mah().max() == pytest.approx(5.0 / 3.6, rel=1e-9)


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


def test_metadata_records_a_content_hash(synthetic_bytes, synthetic_wrd):
    import hashlib

    assert synthetic_wrd.metadata.sha256 == hashlib.sha256(synthetic_bytes).hexdigest()
