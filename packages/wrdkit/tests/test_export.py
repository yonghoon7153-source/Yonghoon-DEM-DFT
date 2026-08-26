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
    done.charge_energy_wh = 0.019
    done.discharge_energy_wh = 0.018
    done.mean_charge_voltage = 3.9
    done.mean_discharge_voltage = 3.7
    done.voltage_max = 4.3
    done.voltage_min = 2.5
    done.complete = True

    # 잘린 사이클도 전압을 들고 있다.  파일이 끝난 순간까지의 평균이고, 아직
    # 도달하지 못한 극값이다 — 비우지 않으면 그대로 측정값처럼 나간다.
    cut = CycleSummary(cycle_index=1, cycle_number=2, start=10, stop=15)
    cut.charge_capacity_mah = 1.2      # 아직 쌓이는 중이었다
    cut.discharge_capacity_mah = 0.0
    cut.charge_energy_wh = 0.004
    cut.discharge_energy_wh = 0.0
    cut.mean_charge_voltage = 3.6
    cut.mean_discharge_voltage = 3.5
    cut.voltage_max = 3.7
    cut.voltage_min = 3.4
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
    """opt-in 해도 숫자는 비운다 — 숫자 칸의 부분값은 측정값으로 읽힌다.

    전압도 마찬가지다.  평균 전압은 E/Q 라 잘린 구간의 부분값이고, v_max/v_min
    은 아직 도달하지 못한 극값이며, 이력은 두 평균의 차다.  남는 것은 파일에
    무엇이 들어 있는지를 말하는 칸뿐이다 — 사이클 번호, 시간, 점 수, complete.
    """
    import csv
    import io

    from wrdkit.export import write_cycles_csv

    stream = io.StringIO()
    write_cycles_csv(_two_cycles(), CellSpec().resolve(), stream,
                     include_incomplete=True)
    rows = list(csv.DictReader(io.StringIO(stream.getvalue())))
    assert len(rows) == 2
    cut = rows[1]
    assert cut["cycle"] == "2"
    assert cut["complete"] == "no", "complete 칸은 남아 있어야 한다"

    keep = {"cycle", "duration (h)", "points", "complete"}
    filled = {name: value for name, value in cut.items()
              if name not in keep and value != ""}
    assert not filled, f"잘린 사이클의 값이 그대로 나갔다: {filled}"

    # 완료된 사이클은 손대지 않는다.
    assert rows[0]["cycle"] == "1"
    assert rows[0]["discharge_capacity (mAh)"] != ""


def test_the_csv_carries_the_value_not_a_rounded_one():
    """내보내는 숫자는 **원래 값**이다.  보기 좋게 자르는 것은 화면이 한다.

    실제로 일어난 일: 예전 서식이 `.6g` 였고, 그것이 값을 바꿨다.

      쿨롱효율 99.9999666...%  ->  `100`      (100 미만인데 100 으로 읽힌다)
      용량 1234.56789 mAh      ->  `1234.57`  (소수 둘째 자리에서 잘린다)

    다른 도구(Smart Interface 의 엑셀)와 맞춰 보다 어긋나면, 그 차이가 어디서
    왔는지 되짚을 수 없게 된다 -- 우리가 이미 지워 버린 자리이므로.
    """
    import io

    from wrdkit.cycles import CycleSummary
    from wrdkit.export import write_cycles_csv

    cycle = CycleSummary(cycle_index=0, cycle_number=1, start=0, stop=10)
    # 효율이 100 에 아주 가깝지만 100 은 아닌 값 (2.999999 / 3.0).
    cycle.charge_capacity_mah = 3.0
    cycle.discharge_capacity_mah = 2.999999
    cycle.charge_energy_wh = 1.23456789012
    cycle.discharge_energy_wh = 1.2
    cycle.mean_charge_voltage = 3.9
    cycle.mean_discharge_voltage = 3.7
    cycle.voltage_max = 4.3
    cycle.voltage_min = 2.5
    cycle.complete = True

    stream = io.StringIO()
    write_cycles_csv([cycle], CellSpec().resolve(), stream)
    header, row = stream.getvalue().strip().split("\n")
    # strict -- 열 수가 어긋나면 그것부터가 결함이다 (조용히 잘라 내지 않는다).
    cells = dict(zip(header.split(","), row.split(","), strict=True))

    efficiency = cells["coulombic_efficiency (%)"]
    assert efficiency != "100", "100 미만인 효율이 100 으로 나가면 안 된다"
    assert float(efficiency) == pytest.approx(99.9999666667, abs=1e-9)

    # 잘리지 않았는지: 12 유효숫자면 이 값이 그대로 돌아온다.
    assert float(cells["discharge_capacity (mAh)"]) == pytest.approx(2.999999, abs=1e-12)
    assert float(cells["charge_energy (mWh)"]) == pytest.approx(1234.56789012, abs=1e-8)

    # 그러면서 없던 자리는 지어내지 않는다 -- float 잡음이 새어 나오면 안 된다.
    assert "0000000000" not in row, f"부동소수 잡음이 새어 나왔다: {row}"
