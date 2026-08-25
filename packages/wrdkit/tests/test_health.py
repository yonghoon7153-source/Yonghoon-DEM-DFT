"""Running vs finished classification and the headline readout."""

from datetime import datetime, timedelta

import pytest

from wrdkit import read_wrd_bytes, summarize_cycles
from wrdkit.health import (
    DEFAULT_REFERENCE_CYCLE,
    FORMATIONLESS_REFERENCE_CYCLE,
    CellState,
    build_report,
    resolve_reference_cycle,
)
from wrdkit.knee import detect_knee

import synthetic


def _cycles(n_cycles=8, truncate=False, cut=20, schedule=None):
    """*cut* 은 뒤에서 몇 표본을 지울지.

    기본 20 은 방전 **도중**에서 끊는다 -- 전류가 흐르는 중이라 파일만 보고도
    잘렸음을 알 수 있는, 이 테스트들이 실제로 뜻하는 상태다.  25 로 하면 방전이
    끝난 뒤 휴지에서 끊겨서 파일만으로는 구분되지 않는다 (아래 별도 테스트).
    """
    samples = synthetic.make_cycles(n_cycles, 20)
    if truncate:
        samples = samples[:-cut]
    wrd = read_wrd_bytes(synthetic.build_wrd(samples, schedule=schedule))
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


#: 충전과 방전을 모두 시키는 최소 스케줄 (루프 없음).
_CHARGE_AND_DISCHARGE = (
    synthetic.SchedStep("chg", control=0, value=0.00123),
    synthetic.SchedStep("dch", control=0, value=-0.00123),
)


def test_a_missing_branch_the_schedule_asked_for_is_still_cut_off():
    """스케줄이 방전을 시켰는데 기록에 없으면, 그것은 아직 못 간 것이다.

    구동 중인 셀이 충전과 휴지를 마치고 방전 직전에 파일이 끊기면 숫자만으로는
    방전 없는 스케줄과 구분되지 않는다 -- 한쪽은 한 시간 뒤에 생기고 다른 쪽은
    영영 안 생기는데.  스케줄이 그 답을 갖고 있다.

    끊는 자리를 25 로 두는 것이 이 테스트의 전부다: 전류가 이미 0 이라
    `_ends_mid_step` 은 아무 말도 못 하고, 답은 스케줄에서만 나온다.
    """
    cycles = _cycles(truncate=True, cut=25, schedule=_CHARGE_AND_DISCHARGE)
    assert cycles[-1].incomplete_reason == "truncated"
    report = build_report(cycles, planned_cycles=100)
    assert report.state == CellState.RUNNING
    assert report.in_progress_cycle == 8


def test_no_schedule_and_no_current_is_unknown_not_cut_off():
    """스케줄이 없으면 그 답을 낼 근거가 없다 (§0.4).

    예전에는 마지막 사이클이면 무조건 "잘렸다" 였다.  전류 0 에서 정상 종료한
    `charge → rest` 기록도 그렇게 읽혀서, 화면은 오지 않을 방전을 기다리라고
    했다.  근거가 없으면 모른다고 해야 한다.
    """
    cycles = _cycles(truncate=True, cut=25)          # 스케줄 없음
    assert cycles[-1].incomplete_reason == "unknown"

    report = build_report(cycles, planned_cycles=100)
    # 구동 중이라는 표를 주지 않는다 -- 번호를 걸면 곧 올라간다는 약속이 된다.
    assert report.in_progress_cycle is None
    assert not any("cut off" in e.detail for e in report.evidence)
    assert any("cannot be told" in e.detail for e in report.evidence)


def test_formation_only_discharge_does_not_speak_for_the_loop():
    """화성에만 방전이 있고 루프는 충전만 하는 스케줄.

    스케줄 전체를 `any()` 로 훑으면 "방전을 선언했다" 가 나온다.  그러면 루프
    안의 사이클이 **영원히 오지 않을 방전을 기다리는 것**으로 보고된다.  어느
    구간의 사이클인지 모르는 채로는 둘 중 하나를 고를 수 없다.
    """
    schedule = (
        synthetic.SchedStep("form-chg", control=0, value=0.00025),
        synthetic.SchedStep("form-dch", control=0, value=-0.00025),
        synthetic.SchedStep("cyc-chg", control=0, value=0.00123,
                            loop_count=200, turn_step="cyc-chg"),
    )
    cycles = _cycles(truncate=True, cut=25, schedule=schedule)
    assert cycles[-1].incomplete_reason == "unknown"
    assert build_report(cycles, planned_cycles=100).in_progress_cycle is None


def test_a_cv_only_discharge_is_not_read_as_no_discharge():
    """부호 없는 정전압 스텝을 "방전이 없다" 로 읽으면 안 된다.

    CV 스텝은 전류 부호가 없어 방향이 `unknown` 이다.  대개 앞선 CC 의 연장이라
    그 방향을 물려받지만, 물려받을 CC 가 앞에 없으면 충전인지 방전인지 알 수
    없다.  정전압만으로 방전하는 프로토콜은 실재한다 -- 없는 것으로 단정하면
    화면이 "영원히 방전하지 않을 프로토콜" 이라고 말한다.
    """
    schedule = (
        synthetic.SchedStep("cv-only", control=1, value2=1.88),   # 앞에 CC 가 없다
        synthetic.SchedStep("chg", control=0, value=0.00123),
    )
    cycles = _cycles(truncate=True, cut=25, schedule=schedule)
    assert cycles[-1].incomplete_reason == "unknown"


def test_a_cv_hold_after_a_cc_leg_inherits_its_direction():
    """반대로, 앞에 CC 가 있는 CV 홀드는 판단을 흐리면 안 된다.

    이것까지 unknown 으로 두면 CCCV 충전만 하는 흔한 스케줄이 전부 "모름" 이
    되어, 방금 고친 것이 다른 쪽으로 똑같이 쓸모없어진다.
    """
    schedule = (
        synthetic.SchedStep("cc-chg", control=0, value=0.00123),
        synthetic.SchedStep("cv-chg", control=1, value2=4.25),
    )
    cycles = _cycles(truncate=True, cut=25, schedule=schedule)
    assert cycles[-1].incomplete_reason == "no_discharge"


def test_an_old_row_without_a_reason_is_not_called_running():
    """이유가 안 적힌 옛 기록.

    사이클 표는 "이유 미상 -- 재파싱하세요" 라고 하는데 보고서는 "잘렸으니 구동
    중" 이라고 말했다.  한 화면 안에서 두 말을 하면 사람은 둘 다 안 믿는다.
    """
    cycles = _cycles(truncate=True)
    cycles[-1].incomplete_reason = ""
    report = build_report(cycles, planned_cycles=100)
    assert report.in_progress_cycle is None
    assert any("re-parse" in e.detail for e in report.evidence)


def test_a_rest_only_record_is_not_called_running():
    """충·방전 스텝이 아예 없는 기록(no_steps)도 잘린 것이 아니다."""
    cycles = _cycles(truncate=True)
    cycles[-1].incomplete_reason = "no_steps"
    report = build_report(cycles, planned_cycles=100)
    assert report.in_progress_cycle is None
    assert not any("cut off" in e.detail for e in report.evidence)


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


# --- 기준 사이클을 누가 정하나 (ADR 0018) ------------------------------------
#
# 3 과 1 사이에서 조용히 움직이면 화면의 유지율이 전부 달라진다.  그래서 답과
# 함께 '누가 정했는지' 를 돌려주고, 그 문자열까지 여기서 고정한다.

def test_formation_makes_the_default_cycle_three():
    assert resolve_reference_cycle(3, formation="yes") == (DEFAULT_REFERENCE_CYCLE,
                                                           "default")


def test_no_formation_anchors_at_cycle_one():
    assert resolve_reference_cycle(3, formation="no") == (FORMATIONLESS_REFERENCE_CYCLE,
                                                          "formationless")


def test_an_unclear_schedule_keeps_cycle_three():
    """모르면 기본값을 그대로 둔다 (§0.4).  1 로 내리는 것도 추측이다."""
    assert resolve_reference_cycle(3, formation="unclear") == (3, "default")


def test_a_typed_value_wins_over_the_schedule():
    """사용자 입력은 덮어쓰기(override)다 (§0.3) — 스케줄이 이기지 못한다."""
    assert resolve_reference_cycle(3, formation="no", by_user=True) == (3, "user")
    assert resolve_reference_cycle(7, formation="yes", by_user=True) == (7, "user")


def test_an_old_row_that_is_not_three_is_read_as_typed():
    """`reference_cycle_source` 가 생기기 전 행이다.

    3 은 기본값이라 누가 넣었는지 알 수 없지만, 3 이 아닌 값은 기본값일 수
    없으므로 사람이 친 것이다.  그것을 스케줄이 덮으면 입력을 잃는다.
    """
    assert resolve_reference_cycle(5, formation="no") == (5, "user")


def test_an_old_row_that_is_three_follows_the_schedule():
    """ADR 0018 이 유일하게 추측하는 자리.  대신 이유를 함께 낸다."""
    assert resolve_reference_cycle(3, formation="no") == (1, "formationless")


def test_nothing_stored_still_answers():
    assert resolve_reference_cycle(None, formation="unclear") == (3, "default")
    assert resolve_reference_cycle(None, formation="no") == (1, "formationless")


# --------------------------------------------------------------------------
# knee_fn -- 계산을 아끼려는 호출자를 위한 이음매
# --------------------------------------------------------------------------
def test_the_knee_is_asked_for_with_the_reference_this_module_resolved():
    """이음매가 함수인 이유.

    기준 사이클은 여기서 정해진다 -- 요청한 사이클이 기록에 없으면 그 뒤
    가장 이른 사이클로 물러나는 규칙이 있고, 호출자가 답을 미리 계산해서
    넘기려면 그 규칙을 베껴야 한다.  베낀 사본은 언젠가 갈라진다.
    """
    asked = {}

    def spy(cycles, capacities, **options):
        asked.update(options)
        asked["n"] = len(list(cycles))
        return None

    report = build_report(_cycles(n_cycles=8), reference_cycle=3, knee_fn=spy)
    assert asked["reference_cycle"] == 3
    assert asked["n"] == report.cycles_complete
    assert report.knee is None


def test_without_a_knee_fn_the_answer_is_the_ordinary_one():
    """기본값이 곧 `detect_knee` 다.  이음매가 답을 바꾸지 않는다."""
    cycles = _cycles(n_cycles=8)
    assert build_report(cycles).state_summary == build_report(
        cycles, knee_fn=detect_knee).state_summary
