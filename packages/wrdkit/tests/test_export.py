"""CSV / XLSX output shapes."""

import csv
import io

import pytest

from wrdkit import (
    Basis,
    CellSpec,
    cycles_csv_string,
    extract_profile,
    profiles_csv_string,
    raw_csv_string,
    summarize_cycles,
)


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


def test_raw_csv_labels_the_capacity_and_energy_units(synthetic_wrd):
    header = _rows(raw_csv_string(synthetic_wrd))[0]
    assert "charge_q (Ah)" in header
    assert "discharge_q (Ah)" in header
    assert "charge_e (Wh)" in header


def test_raw_csv_labels_a_coulomb_file_differently(synthetic_bytes):
    """UnitCoulomb decides the unit per file; identical headers hide a x3600."""
    from wrdkit import read_wrd_bytes

    coulomb = read_wrd_bytes(synthetic_bytes, source_name="coulomb.wrd")
    coulomb.metadata.unit_coulomb = True
    header = _rows(raw_csv_string(coulomb))[0]
    assert "charge_q (C)" in header
    assert "charge_e (J)" in header
    assert "charge_q (Ah)" not in header


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


# --- 미완료 사이클은 기본적으로 나가지 않는다 --------------------------------
#
# 구동 중인 셀의 마지막 사이클은 스텝 중간에서 잘려 있다. 그 용량은 파일이
# 쓰인 순간까지 쌓인 값이라, 측정값처럼 보이지만 측정값이 아니다. API 는 이미
# 빼고 있었는데 라이브러리 CSV 는 그대로 내보내, wrdkit convert 로 만든
# 스프레드시트의 마지막 줄이 셀을 실제보다 나쁘게 보이게 했다.

def _two_cycles():
    from wrdkit.cycles import CycleSummary

    done = CycleSummary(cycle_index=0, cycle_number=1, start=0, stop=10)
    done.charge_capacity_mah = 5.0
    done.discharge_capacity_mah = 4.9
    done.complete = True
    cut = CycleSummary(cycle_index=1, cycle_number=2, start=10, stop=15)
    cut.charge_capacity_mah = 1.2      # 아직 쌓이는 중이었다
    cut.discharge_capacity_mah = 0.0
    cut.complete = False
    return [done, cut]


def test_a_cut_off_cycle_is_left_out_by_default():
    import io

    from wrdkit.export import write_cycles_csv

    stream = io.StringIO()
    write_cycles_csv(_two_cycles(), CellSpec().resolve(), stream)
    rows = stream.getvalue().strip().split("\n")
    assert len(rows) == 2, "헤더 + 완료된 사이클 1줄이어야 한다"
    assert rows[1].startswith("1,")


def test_keeping_it_blanks_the_numbers_rather_than_publishing_them():
    """opt-in 해도 숫자는 비운다 — 숫자 칸의 부분값은 측정값으로 읽힌다."""
    import io

    from wrdkit.export import write_cycles_csv

    stream = io.StringIO()
    write_cycles_csv(_two_cycles(), CellSpec().resolve(), stream,
                     include_incomplete=True)
    rows = stream.getvalue().strip().split("\n")
    assert len(rows) == 3
    cut = rows[2].split(",")
    assert cut[0] == "2"
    assert cut[1] == "" and cut[2] == "", "잘린 사이클의 용량이 그대로 나갔다"
    assert cut[-1] == "no", "complete 칸은 남아 있어야 한다"
