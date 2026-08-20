"""Command-line surface."""

import csv

import pytest

from wrdkit.cli import main

import synthetic


@pytest.fixture
def wrd_path(tmp_path):
    path = tmp_path / "cell.wrd"
    path.write_bytes(synthetic.build_wrd(synthetic.make_cycles(4, 25)))
    return path


def test_info_prints_the_essentials(wrd_path, capsys):
    assert main(["info", str(wrd_path)]) == 0
    out = capsys.readouterr().out
    assert "WBCS3000S1" in out
    assert "cycles" in out
    assert "retention" in out


def test_convert_writes_three_tables(wrd_path, tmp_path):
    out_dir = tmp_path / "csv"
    code = main(["convert", str(wrd_path), "--out-dir", str(out_dir),
                 "--mass", "31.6", "--wt", "80", "--diameter", "13",
                 "--basis", "mAh/g"])
    assert code == 0
    names = sorted(p.name for p in out_dir.iterdir())
    assert names == ["cell_cycles.csv", "cell_profiles.csv", "cell_raw.csv"]


def test_convert_honours_a_cycle_selection(wrd_path, tmp_path):
    out_dir = tmp_path / "csv"
    main(["convert", str(wrd_path), "--out-dir", str(out_dir),
          "--tables", "profiles", "--cycles", "2,4"])
    header = next(csv.reader((out_dir / "cell_profiles.csv").open(encoding="utf-8-sig")))
    assert any("cycle2_" in column for column in header)
    assert any("cycle4_" in column for column in header)
    assert not any("cycle1_" in column for column in header)


def test_cycles_writes_csv_to_stdout(wrd_path, capsys):
    assert main(["cycles", str(wrd_path), "--mass", "31.6", "--wt", "80",
                 "--basis", "mAh/g"]) == 0
    out = capsys.readouterr().out
    assert "discharge_capacity (mAh/g)" in out.splitlines()[0]


def test_a_missing_file_is_reported_not_traced(tmp_path, capsys):
    assert main(["info", str(tmp_path / "nope.wrd")]) == 1
    assert "wrdkit:" in capsys.readouterr().err


def test_a_non_wrd_file_is_reported(tmp_path, capsys):
    bad = tmp_path / "bad.wrd"
    bad.write_bytes(b"not a wrd file at all, definitely not" * 4)
    assert main(["info", str(bad)]) == 1
    assert "not a .wrd" in capsys.readouterr().err
