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


def _write(path, samples):
    path.write_bytes(synthetic.build_wrd(samples))
    return path


def test_info_prints_the_essentials(wrd_path, capsys):
    assert main(["info", str(wrd_path)]) == 0
    out = capsys.readouterr().out
    assert "WBCS3000S1" in out
    assert "cycles" in out
    assert "retention" in out


def test_retention_is_anchored_at_the_reference_cycle(wrd_path, capsys):
    """ADR 0004: cycles 1-2 are formation, so cycle 3 is the anchor."""
    assert main(["info", str(wrd_path)]) == 0
    out = capsys.readouterr().out
    assert "vs cycle 3" in out
    # make_cycles fades 2%/cycle: cycle 3 = 4.80 mAh, cycle 4 = 4.70 mAh.
    assert "retention 97.9%" in out
    assert "retention 94.0%" not in out  # what a cycle-1 anchor would print


def test_retention_is_withheld_when_the_reference_cycle_is_missing(tmp_path, capsys):
    path = _write(tmp_path / "short.wrd", synthetic.make_cycles(2, 25))
    assert main(["info", str(path)]) == 0
    out = capsys.readouterr().out
    assert "retention n/a" in out
    assert "vs cycle 1" not in out


def test_info_survives_a_cycle_with_no_measurable_charge(tmp_path, capsys):
    """A charge step below the current resolution leaves CE undefined."""
    samples = synthetic.make_cycles(2, 25)
    for sample in samples[:25]:  # cycle 1's charge step
        sample.charge_q = 0.0
    path = _write(tmp_path / "zero_charge.wrd", samples)
    assert main(["info", str(path)]) == 0
    assert "CE n/a" in capsys.readouterr().out


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


def test_convert_skips_an_incomplete_cycle_named_explicitly(tmp_path, capsys):
    """A truncated curve must not reach the CSV, selected by name or not."""
    samples = synthetic.make_cycles(5, 25)
    per_cycle = len(samples) // 5
    # Cut cycle 5 halfway through its discharge, as a file split mid-run does.
    truncated = samples[:4 * per_cycle + 25 + 3 + 12]
    path = _write(tmp_path / "running.wrd", truncated)

    out_dir = tmp_path / "csv"
    assert main(["convert", str(path), "--out-dir", str(out_dir),
                 "--tables", "profiles", "--cycles", "3,5"]) == 0
    header = next(csv.reader((out_dir / "running_profiles.csv").open(encoding="utf-8-sig")))
    assert any("cycle3_" in column for column in header)
    assert not any("cycle5_" in column for column in header)
    assert "cycle 5 is incomplete" in capsys.readouterr().err


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
