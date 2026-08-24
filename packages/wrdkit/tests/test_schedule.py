"""Conditions inferred from the embedded schedule."""

import pytest

from wrdkit import Schedule, ScheduleStep


def _schedule(formation_a: float | None, cycling_a: float,
              loop_count: int = 50) -> Schedule:
    """Formation once, then a looped charge/discharge pair.

    Mirrors what the Schedule Editor writes: the loop's last step points back
    at the first step of the loop, which is how ``cycling_current_a`` and
    ``formation_current_a`` tell the two parts apart.
    """
    steps: list[ScheduleStep] = []
    if formation_a is not None:
        steps += [
            ScheduleStep(index=len(steps), name="form_chg", control="CC",
                         control_raw=0, current_a=formation_a),
            ScheduleStep(index=len(steps) + 1, name="form_dch", control="CC",
                         control_raw=0, current_a=-formation_a),
        ]
    steps += [
        ScheduleStep(index=len(steps), name="cyc_chg", control="CC",
                     control_raw=0, current_a=cycling_a),
        ScheduleStep(index=len(steps) + 1, name="cyc_dch", control="CC",
                     control_raw=0, current_a=-cycling_a,
                     loop_count=loop_count, loop_target="cyc_chg"),
    ]
    return Schedule(version="1.0", source_path=None, steps=steps)


def test_an_unambiguous_current_ratio_gives_the_c_rate():
    # 0.1C formation, 0.5C cycling -- ratio 5 matches only one pair.
    schedule = _schedule(formation_a=0.52e-3, cycling_a=2.6e-3)
    assert schedule.infer_c_rate() == pytest.approx(0.5)
    assert schedule.nominal_capacity_ah() == pytest.approx(5.2e-3)


def test_an_ambiguous_current_ratio_is_reported_as_unknown():
    """0.05C/0.1C and 0.1C/0.2C are both ratio 2 -- guessing halves the capacity."""
    schedule = _schedule(formation_a=0.26e-3, cycling_a=0.52e-3)
    assert schedule.infer_c_rate() is None
    assert schedule.nominal_capacity_ah() is None
    # An explicit rate still works: only the guess is withheld.
    assert schedule.nominal_capacity_ah(0.1) == pytest.approx(5.2e-3)


def test_a_schedule_without_formation_infers_nothing():
    schedule = _schedule(formation_a=None, cycling_a=2.6e-3)
    assert schedule.infer_c_rate() is None
    assert schedule.nominal_capacity_ah() is None


def test_an_unrecognised_ratio_infers_nothing():
    schedule = _schedule(formation_a=1.0e-3, cycling_a=7.3e-3)
    assert schedule.infer_c_rate() is None


def test_the_cycling_current_is_the_looped_one():
    schedule = _schedule(formation_a=0.52e-3, cycling_a=2.6e-3)
    assert schedule.cycling_current_a == pytest.approx(2.6e-3)
    assert schedule.formation_current_a == pytest.approx(0.52e-3)
    assert schedule.planned_cycles == 50


# --- formation 이 있나 (ADR 0018) -------------------------------------------
#
# 기준 사이클이 3인지 1인지가 여기서 갈린다.  틀리면 유지율이 조용히 몇 % 씩
# 달라지므로, 스케줄이 취할 수 있는 모양마다 답을 고정해 둔다.

def _with_prelude(prelude: list[ScheduleStep]) -> Schedule:
    """*prelude* 를 루프 앞에 두고 충방전 루프를 붙인다."""
    steps = list(prelude)
    steps += [
        ScheduleStep(index=len(steps), name="cyc_chg", control="CC",
                     control_raw=0, current_a=2.6e-3),
        ScheduleStep(index=len(steps) + 1, name="cyc_dch", control="CC",
                     control_raw=0, current_a=-2.6e-3,
                     loop_count=50, loop_target="cyc_chg"),
    ]
    return Schedule(version="1.0", source_path=None, steps=steps)


def test_a_charge_step_before_the_loop_is_formation():
    assert _schedule(formation_a=0.52e-3, cycling_a=2.6e-3).formation == "yes"


def test_a_loop_with_nothing_before_it_has_no_formation():
    assert _schedule(formation_a=None, cycling_a=2.6e-3).formation == "no"


def test_a_rest_before_the_loop_is_not_formation():
    """임피던스 재기 전의 안정화 휴지.  이 결정이 겨냥하는 프로토콜이다.

    휴지는 용량을 만들지도 잃지도 않으므로 1번 사이클을 기준선에서 뺄 이유가
    되지 못한다.
    """
    rest = ScheduleStep(index=0, name="eis_rest", control="REST",
                        control_raw=0, current_a=0.0)
    assert _with_prelude([rest]).formation == "no"


def test_a_constant_voltage_hold_before_the_loop_is_unclear():
    """물려받을 CC 가 앞에 없는 CV 는 충전인지 방전인지 알 수 없다 (§0.4)."""
    hold = ScheduleStep(index=0, name="cv_hold", control="CV",
                        control_raw=1, current_a=None, voltage_limit_v=4.3)
    assert _with_prelude([hold]).formation == "unclear"


def test_a_hold_after_a_charge_inherits_its_direction():
    """CC-CV formation 은 formation 이다 — CV 때문에 '모름' 이 되지 않는다."""
    prelude = [
        ScheduleStep(index=0, name="form_chg", control="CC",
                     control_raw=0, current_a=0.52e-3),
        ScheduleStep(index=1, name="form_cv", control="CV",
                     control_raw=1, current_a=None, voltage_limit_v=4.3),
    ]
    assert _with_prelude(prelude).formation == "yes"


def test_a_schedule_with_no_loop_cannot_say():
    """루프가 없으면 무엇이 formation 이고 무엇이 본 구동인지 가를 선이 없다."""
    steps = [
        ScheduleStep(index=0, name="chg", control="CC", control_raw=0, current_a=2.6e-3),
        ScheduleStep(index=1, name="dch", control="CC", control_raw=0, current_a=-2.6e-3),
    ]
    assert Schedule(version="1.0", source_path=None, steps=steps).formation == "unclear"


def test_an_empty_schedule_cannot_say():
    assert Schedule(version="1.0", source_path=None, steps=[]).formation == "unclear"
