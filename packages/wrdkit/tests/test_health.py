"""Running vs finished classification and the headline readout."""

from datetime import datetime, timedelta

import pytest

from wrdkit import read_wrd_bytes, summarize_cycles
from wrdkit.health import CellState, build_report

import synthetic


def _cycles(n_cycles=8, truncate=False):
    samples = synthetic.make_cycles(n_cycles, 20)
    if truncate:
        samples = samples[:-25]
    wrd = read_wrd_bytes(synthetic.build_wrd(samples))
    return summarize_cycles(wrd)


def test_a_partial_last_cycle_means_the_cell_is_running():
    report = build_report(_cycles(truncate=True), planned_cycles=100)
    assert report.state == CellState.RUNNING
    assert report.in_progress_cycle == 8


def test_a_running_cell_quotes_the_cycle_before_the_one_in_progress():
    report = build_report(_cycles(truncate=True), planned_cycles=100)
    assert report.reported.cycle == report.in_progress_cycle - 1
    assert report.reported.complete is True


def test_completing_the_planned_cycles_means_finished():
    report = build_report(_cycles(n_cycles=8), planned_cycles=8)
    assert report.state == CellState.FINISHED
    assert report.reported.cycle == 8


def test_the_schedule_reaching_its_end_means_finished():
    report = build_report(_cycles(n_cycles=8), schedule_finished=True)
    assert report.state == CellState.FINISHED


def test_a_manual_state_overrides_the_evidence():
    report = build_report(_cycles(truncate=True), planned_cycles=100,
                          declared_state=CellState.FINISHED)
    assert report.state == CellState.FINISHED
    assert report.state_confidence == "high"
    assert report.evidence[0].signal == "manual"


def test_state_evidence_is_always_explained():
    report = build_report(_cycles(truncate=True), planned_cycles=100)
    assert report.evidence
    assert all(e.detail for e in report.evidence)


def test_a_long_silence_argues_for_finished():
    cycles = _cycles(n_cycles=8)
    last = datetime(2026, 1, 1, 12, 0)
    report = build_report(cycles, last_sample_time=last,
                          now=last + timedelta(days=30))
    assert report.state == CellState.FINISHED
    assert any(e.signal == "recency" for e in report.evidence)


def test_retention_and_initial_ce_use_cycle_three():
    report = build_report(_cycles(n_cycles=8), planned_cycles=8, reference_cycle=3)
    assert report.reference_available is True
    assert report.reference.cycle == 3
    # 2% fade per cycle: cycle 8 vs cycle 3 is 0.86/0.96.
    assert report.retention_pct == pytest.approx(100 * 0.86 / 0.96, rel=1e-6)
    assert report.initial_coulombic_efficiency == pytest.approx(100.0)


def test_a_missing_reference_cycle_is_flagged_not_silently_swapped():
    cycles = _cycles(n_cycles=8)
    later = summarize_cycles(
        read_wrd_bytes(synthetic.build_wrd(synthetic.make_cycles(8, 20))),
        cycle_offset=200)
    del cycles
    report = build_report(later, reference_cycle=3)
    assert report.reference_available is False
    assert report.reference.cycle == 201
    assert "not in this record" in report.retention_note


def test_cycle_one_ce_is_kept_alongside_the_reference():
    report = build_report(_cycles(n_cycles=8), reference_cycle=3)
    assert report.first_cycle.cycle == 1


def test_no_completed_cycle_yields_an_honest_empty_report():
    samples = synthetic.make_cycles(1, 20)[:10]
    report = build_report(summarize_cycles(read_wrd_bytes(synthetic.build_wrd(samples))))
    assert report.reported is None
    assert report.state_summary == "no completed cycle yet"


def test_the_summary_sentence_carries_the_headline_numbers():
    report = build_report(_cycles(truncate=True), planned_cycles=100)
    assert "running" in report.state_summary
    assert "discharge" in report.state_summary
    assert "retention" in report.state_summary
