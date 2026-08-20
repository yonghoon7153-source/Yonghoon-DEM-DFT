"""CSV / XLSX output shapes."""

import csv
import io

import pytest

from wrdkit import (Basis, CellSpec, cycles_csv_string, extract_profile,
                    profiles_csv_string, raw_csv_string, summarize_cycles)


@pytest.fixture
def cell():
    return CellSpec(total_mass_mg=31.6, active_wt_percent=80, diameter_mm=13).resolve()


def _rows(text):
    return list(csv.reader(io.StringIO(text)))


def test_raw_csv_has_one_row_per_sample_plus_a_header(synthetic_wrd):
    rows = _rows(raw_csv_string(synthetic_wrd))
    assert len(rows) == len(synthetic_wrd) + 1
    assert rows[0][:4] == ["timestamp", "test_time_s", "step_time_s", "cycle_time_s"]


def test_raw_csv_converts_ticks_to_seconds(synthetic_wrd):
    rows = _rows(raw_csv_string(synthetic_wrd))
    assert float(rows[1][1]) == pytest.approx(0.0)
    assert float(rows[2][1]) == pytest.approx(10.0)


def test_raw_csv_drops_the_tick_columns_it_replaced(synthetic_wrd):
    header = _rows(raw_csv_string(synthetic_wrd))[0]
    assert "date_time" not in header
    assert "test_time" not in header
    assert "voltage" in header and "i_range" in header


def test_cycles_csv_labels_the_basis(synthetic_wrd, cell):
    rows = _rows(cycles_csv_string(summarize_cycles(synthetic_wrd), cell,
                                   basis=Basis.SPECIFIC))
    assert "discharge_capacity (mAh/g)" in rows[0]
    assert "discharge_capacity (mAh)" in rows[0]  # absolute kept alongside
    assert len(rows) == 4  # header + 3 cycles


def test_cycles_csv_values_are_normalised(synthetic_wrd, cell):
    rows = _rows(cycles_csv_string(summarize_cycles(synthetic_wrd), cell,
                                   basis=Basis.SPECIFIC))
    header, first = rows[0], rows[1]
    column = header.index("discharge_capacity (mAh/g)")
    assert float(first[column]) == pytest.approx(5.0 / 0.02528, rel=1e-4)


def test_cycles_csv_falls_back_to_mah_when_the_basis_is_unavailable(synthetic_wrd):
    bare = CellSpec().resolve()
    rows = _rows(cycles_csv_string(summarize_cycles(synthetic_wrd), bare,
                                   basis=Basis.SPECIFIC))
    assert "discharge_capacity (mAh)" in rows[0]
    assert "discharge_capacity (mAh/g)" not in rows[0]


def test_profiles_csv_puts_each_branch_in_its_own_column_pair(synthetic_wrd, cell):
    cycles = summarize_cycles(synthetic_wrd)
    profiles = [extract_profile(synthetic_wrd, cycles[0], "charge"),
                extract_profile(synthetic_wrd, cycles[0], "discharge")]
    rows = _rows(profiles_csv_string(profiles, cell, basis=Basis.SPECIFIC))
    assert rows[0] == [
        "cycle1_charge_capacity (mAh/g)", "cycle1_charge_voltage (V)",
        "cycle1_discharge_capacity (mAh/g)", "cycle1_discharge_voltage (V)",
    ]
    assert len(rows) == 41  # header + 40 points


def test_profiles_csv_pads_uneven_columns(synthetic_wrd, cell):
    cycles = summarize_cycles(synthetic_wrd)
    long_profile = extract_profile(synthetic_wrd, cycles[0], "charge")
    short = extract_profile(synthetic_wrd, cycles[0], "discharge")
    short.capacity_mah = short.capacity_mah[:5]
    short.voltage = short.voltage[:5]
    rows = _rows(profiles_csv_string([long_profile, short], cell))
    assert rows[10][2] == ""  # short column is blank past its end
    assert rows[10][0] != ""


def test_xlsx_export_writes_every_sheet(tmp_path, synthetic_wrd, cell):
    openpyxl = pytest.importorskip("openpyxl")
    from wrdkit import write_xlsx

    cycles = summarize_cycles(synthetic_wrd)
    profiles = [extract_profile(synthetic_wrd, cycles[0], "discharge")]
    target = tmp_path / "out.xlsx"
    write_xlsx(target, synthetic_wrd, cycles, profiles, cell, basis=Basis.SPECIFIC)

    book = openpyxl.load_workbook(target)
    assert book.sheetnames == ["metadata", "cycles", "profiles"]
    assert book["cycles"].max_row == 4
