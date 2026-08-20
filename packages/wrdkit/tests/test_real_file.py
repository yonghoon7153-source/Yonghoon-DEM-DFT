"""Checks that only run against a real instrument file.

    WRDKIT_SAMPLE=/path/to/file.wrd pytest

These assert on physics rather than on exact values, so they hold for any
WBCS3000 cycling file, not just the one used to reverse-engineer the format.
"""

import numpy as np
import pytest

from wrdkit import CellStatus, extract_profile, summarize_cycles
from wrdkit.health import build_report


def test_the_whole_file_is_consumed(sample_wrd):
    assert sample_wrd.metadata.trailing_bytes == 0
    assert len(sample_wrd) > 0


def test_cell_status_agrees_with_the_current_sign(sample_wrd):
    status = sample_wrd["cell_status"]
    current = sample_wrd["current"]
    assert np.all(current[status == CellStatus.CHARGE] > 0)
    assert np.all(current[status == CellStatus.DISCHARGE] < 0)
    assert np.all(current[status == CellStatus.REST] == 0)


def test_reported_capacity_matches_the_current_integral(sample_wrd):
    """Coulomb counting is computed independently of the reported column."""
    cycles = [c for c in summarize_cycles(sample_wrd) if c.complete]
    if len(cycles) < 3:
        pytest.skip("file has fewer than three complete cycles")
    cycle = cycles[len(cycles) // 2]
    seconds = sample_wrd.seconds("test_time")[cycle.start:cycle.stop]
    current = sample_wrd["current"][cycle.start:cycle.stop]
    discharging = current < 0
    integrated = np.trapezoid(-current[discharging], seconds[discharging]) / 3.6
    assert integrated == pytest.approx(cycle.discharge_capacity_mah, rel=0.02)


def test_time_advances_monotonically(sample_wrd):
    seconds = sample_wrd.seconds("test_time")
    assert np.all(np.diff(seconds) >= 0)


def test_schedule_cutoffs_bracket_the_measured_voltage(sample_wrd):
    schedule = sample_wrd.metadata.schedule
    if not schedule or schedule.upper_cutoff_v is None:
        pytest.skip("file carries no voltage cut-offs")
    voltage = sample_wrd["voltage"]
    assert voltage.max() <= schedule.upper_cutoff_v + 0.05
    assert voltage.min() >= schedule.lower_cutoff_v - 0.05


def test_profiles_span_the_cycle_capacity(sample_wrd):
    cycles = [c for c in summarize_cycles(sample_wrd) if c.complete]
    if not cycles:
        pytest.skip("no complete cycle")
    cycle = cycles[len(cycles) // 2]
    profile = extract_profile(sample_wrd, cycle, "discharge")
    assert profile.capacity_mah[0] == pytest.approx(0.0, abs=1e-9)
    assert profile.capacity_mah[-1] == pytest.approx(cycle.discharge_capacity_mah)


def test_a_report_can_be_built(sample_wrd):
    schedule = sample_wrd.metadata.schedule
    report = build_report(
        summarize_cycles(sample_wrd),
        planned_cycles=schedule.planned_cycles if schedule else None,
    )
    assert report.state in ("running", "finished", "unknown")
    assert report.state_summary
