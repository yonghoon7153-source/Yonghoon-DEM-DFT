"""사이클 간 단차 — 조용히 틀리는 세 가지를 고정한다.

여기 있는 검사는 전부 "그럴듯한 잘못된 숫자" 를 막는 것이다. 예외가 나는
경우가 아니라 화면에 멀쩡히 찍히는 경우라서, 검사가 없으면 아무도 눈치채지
못한다.
"""

from __future__ import annotations

import pytest

from wrdkit.deltas import previous_cycle_deltas


def test_the_step_is_this_cycle_minus_the_one_before():
    rows = previous_cycle_deltas([1, 2, 3], [5.0, 4.8, 4.5])
    assert rows[0].delta is None                  # 기준이 없다
    assert rows[1].delta == pytest.approx(-0.2)
    assert rows[2].delta == pytest.approx(-0.3)
    assert rows[1].previous_cycle == 1
    assert rows[2].previous_cycle == 2


def test_the_first_cycle_says_why_it_has_no_step():
    rows = previous_cycle_deltas([1], [5.0])
    assert rows[0].delta is None
    assert "earlier" in rows[0].reason


def test_a_running_cycle_gets_no_step_and_gives_none():
    """구동 중인 마지막 사이클은 잘려 있다 (CLAUDE.md §3).

    그 값을 빼면 큰 음수가 나오고, 화면에서는 급사(急死)로 읽힌다. 그리고
    그 사이클이 다음 사이클의 기준이 되면 잘못이 뒤로 전파된다.
    """
    rows = previous_cycle_deltas([1, 2, 3], [5.0, 2.1, 4.9],
                                 [True, False, True])
    assert rows[1].delta is None
    assert "running" in rows[1].reason
    # 3번은 잘린 2번이 아니라 1번을 기준으로 삼아야 한다.
    assert rows[2].previous_cycle == 1
    assert rows[2].delta == pytest.approx(-0.1)


def test_a_missing_value_is_not_a_zero():
    """방전 가지가 없는 사이클은 '0 mAh 를 방전했다' 가 아니다."""
    rows = previous_cycle_deltas([1, 2, 3], [5.0, None, 4.9])
    assert rows[1].delta is None
    assert "no value" in rows[1].reason
    assert rows[2].previous_cycle == 1
    assert rows[2].delta == pytest.approx(-0.1)


def test_a_gap_is_reported_not_hidden():
    """3번 → 8번은 다섯 사이클치 열화다. 한 사이클치처럼 보이면 안 된다."""
    rows = previous_cycle_deltas([1, 3, 8], [5.0, 4.9, 4.4])
    assert rows[2].previous_cycle == 3
    assert rows[2].span == 5
    assert rows[2].delta == pytest.approx(-0.5)
    assert rows[2].per_cycle == pytest.approx(-0.1)


def test_adjacent_cycles_have_span_one_and_per_cycle_equal_to_delta():
    rows = previous_cycle_deltas([10, 11], [4.0, 3.8])
    assert rows[1].span == 1
    assert rows[1].per_cycle == pytest.approx(rows[1].delta)


def test_the_percentage_is_against_the_base_not_the_first_cycle():
    """유지율과 다른 질문이다. 분모는 직전 사이클이다."""
    rows = previous_cycle_deltas([1, 2, 3], [100.0, 50.0, 25.0])
    assert rows[1].delta_pct == pytest.approx(-50.0)
    assert rows[2].delta_pct == pytest.approx(-50.0)   # 25 는 50 의 절반


def test_a_zero_base_has_no_percentage_rather_than_a_huge_one():
    """0 에서의 상대 변화는 큰 것이 아니라 정의되지 않는다."""
    rows = previous_cycle_deltas([1, 2], [0.0, 3.0])
    assert rows[1].delta == pytest.approx(3.0)
    assert rows[1].delta_pct is None


def test_a_gain_is_positive():
    """활성화로 용량이 오르는 초기 사이클이 실제로 있다. 부호를 지운 절대값을
    내보내면 그것을 열화와 구분할 수 없다."""
    rows = previous_cycle_deltas([1, 2], [4.0, 4.3])
    assert rows[1].delta == pytest.approx(0.3)
    assert rows[1].delta_pct == pytest.approx(7.5)


def test_every_row_comes_back_in_order():
    """행 수와 순서가 입력과 같아야 표에 그대로 붙는다."""
    numbers = [1, 2, 3, 4, 5]
    rows = previous_cycle_deltas(numbers, [1.0, None, 3.0, 4.0, 5.0],
                                 [True, True, True, False, True])
    assert [r.cycle_number for r in rows] == numbers


def test_mismatched_lengths_are_refused_loudly():
    """길이가 어긋나면 조용히 짧은 쪽에 맞추면 안 된다 — 행이 밀린다."""
    with pytest.raises(ValueError, match="values"):
        previous_cycle_deltas([1, 2, 3], [1.0, 2.0])
    with pytest.raises(ValueError, match="complete"):
        previous_cycle_deltas([1, 2], [1.0, 2.0], [True])


def test_all_incomplete_gives_all_reasons_and_no_numbers():
    rows = previous_cycle_deltas([1, 2], [1.0, 2.0], [False, False])
    assert all(r.delta is None and r.reason for r in rows)


def test_nothing_in_nothing_out():
    assert previous_cycle_deltas([], []) == []


def test_usable_says_whether_there_is_a_number():
    rows = previous_cycle_deltas([1, 2], [4.0, 3.9])
    assert not rows[0].usable
    assert rows[1].usable
