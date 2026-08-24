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
    # 무엇이 없는지까지 말한다.  "no completed cycle yet" 만 있던 동안, 화면은
    # 온통 — 뿐이었고 그것은 파싱 실패로 읽혔다.
    assert report.no_complete_reason == "truncated"
    assert "stops part-way through a step" in report.state_summary


def test_a_charge_only_schedule_is_not_called_cut_off():
    """multi-step CCCV 처럼 방전이 아예 없는 프로토콜.

    실측 파일(260630_MJ1, 41,738행)이 이랬다: 3.5 → 3.75 → 4.0 → 4.25 V 를
    CC-CV 로 네 단 올리고 끝난다.  `cell_status` 에 4(방전)가 한 번도 안 나온다.

    예전에는 "1번 사이클이 스텝 도중에 잘렸습니다" 라고 했다.  거짓이다 --
    파일은 CV 홀드를 끝까지 마치고 정상 종료했다.  그리고 그 문장은 "기다리면
    된다" 로 읽히는데, 이 기록은 아무리 기다려도 사이클 용량을 내지 않는다.
    """
    samples = synthetic.make_cycles(1, 20)
    charge_only = [s for s in samples if s.current >= 0]
    # 실측 파일의 모양 그대로: 휴지 뒤에 CC-CV 충전 두 단, 방전 스텝은 없다.
    schedule = (
        synthetic.SchedStep("rest", control=7),
        synthetic.SchedStep("cc-1", control=0, value=0.00123),
        synthetic.SchedStep("cv-1", control=1, value=3.5),
        synthetic.SchedStep("cc-2", control=0, value=0.00123),
        synthetic.SchedStep("cv-2", control=1, value=4.25),
    )
    wrd = read_wrd_bytes(synthetic.build_wrd(charge_only, schedule=schedule))
    [cycle] = summarize_cycles(wrd)
    assert cycle.complete is False
    assert cycle.incomplete_reason == "no_discharge"

    report = build_report(summarize_cycles(wrd))
    assert report.no_complete_reason == "no_discharge"
    # 영영 안 올라갈 사이클 번호를 "진행 중" 으로 걸어 두지 않는다.
    assert report.in_progress_cycle is None
    assert "no discharge" in report.state_summary
    assert not any("cut off" in e.detail for e in report.evidence)
    assert any("has no discharge" in e.detail for e in report.evidence)


def test_a_missing_branch_the_schedule_asked_for_is_still_cut_off():
    """스케줄이 방전을 시켰는데 기록에 없으면, 그것은 아직 못 간 것이다.

    구동 중인 셀이 충전과 휴지를 마치고 방전 직전에 파일이 끊기면 숫자만으로는
    방전 없는 스케줄과 구분되지 않는다 -- 한쪽은 한 시간 뒤에 생기고 다른 쪽은
    영영 안 생기는데.  스케줄이 그 답을 갖고 있다.
    """
    report = build_report(_cycles(truncate=True), planned_cycles=100)
    assert report.state == CellState.RUNNING
    assert report.in_progress_cycle == 8


def test_the_summary_sentence_carries_the_headline_numbers():
    report = build_report(_cycles(truncate=True), planned_cycles=100)
    assert "running" in report.state_summary
    assert "discharge" in report.state_summary
    assert "retention" in report.state_summary


def test_a_reference_after_the_record_does_not_fall_back_to_formation():
    """요청한 기준 사이클 뒤에 데이터가 없으면 cycle 1 을 쓰지 않는다.

    `detect_knee` 는 이 경우 `indeterminate` 를 내도록 고쳤는데, `build_report`
    가 먼저 `complete[0]` 을 골라 그것을 요청값인 양 넘기고 있었다.  기준
    사이클이 존재하는 이유가 formation 을 빼는 것인데(ADR 0004), 그 되돌림이
    유지율의 분모와 knee 의 baseline 으로 다시 들어갔다.  core 테스트만으로는
    잡히지 않는 경로다 — 생산 보고서는 전부 여기를 지난다.
    """
    report = build_report(_cycles(8), reference_cycle=50)
    assert not report.reference_available
    assert report.reference is None
    assert report.retention_pct is None
    assert report.knee is not None
    assert report.knee.reference_cycle == 50
    assert report.knee.primary.status == "indeterminate", report.knee.primary.reason


def test_a_continuation_file_still_gets_a_baseline_after_the_request():
    """요청 뒤에 사이클이 있으면 그 첫 사이클을 쓴다 — 이어지는 파일을 위해서다."""
    report = build_report(_cycles(8), reference_cycle=0)
    assert not report.reference_available
    assert report.reference is not None
    assert report.reference.cycle == 1
    assert report.retention_pct is not None
