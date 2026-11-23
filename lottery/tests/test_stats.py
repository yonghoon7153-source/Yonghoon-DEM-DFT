"""통계 검정 도구의 정확성 + 귀무 보정(calibration).

귀무 보정 테스트의 뜻: 진짜 무작위로 만든 가상 추첨을 넣으면 p 가 극단값(≈0)이 나오면
안 된다. 2026-11-23 실제 데이터에서 총합·연번·AC값이 p≈0 으로 나왔는데, 원인은 추첨기가
아니라 chi2_gof 의 꼬리 칸 합치기 버그였다 (`exp[1] += exp.pop(0)` — 파이썬은 exp[1] 을
먼저 읽고 pop 으로 리스트를 민 뒤 엉뚱한 칸에 쓴다 → 기대도수가 사라진다).
"""
import numpy as np
import pytest

import stats_tests


def test_chi2_gof_merges_tail_bins_into_their_neighbours():
    # 꼬리 두 칸(기대 0.5)은 이웃 칸에 합쳐져야 하고, 합친 뒤 관측=기대 이므로 X²=0
    x2, df, p = stats_tests.chi2_gof([1, 10, 20, 10, 1], [0.5, 10.5, 20, 10.5, 0.5])
    assert df == 2
    assert x2 == pytest.approx(0.0, abs=1e-12)


def test_chi2_gof_preserves_totals_when_merging_many_tail_bins():
    obs = [0, 0, 1, 3, 50, 100, 50, 3, 1, 0]
    exp = [0.1, 0.4, 1.5, 3.0, 49.0, 100.0, 49.0, 3.0, 1.5, 0.5]
    x2, df, p = stats_tests.chi2_gof(obs, exp)
    # 끝 칸 기대도수가 5 이상이 될 때까지만 합친다: 왼쪽 0.1+0.4+1.5+3.0 = 5.0,
    # 오른쪽 0.5+1.5+3.0 = 5.0 → 칸 [5, 49, 100, 49, 5], 관측 [4, 50, 100, 50, 4]
    o = np.array([4, 50, 100, 50, 4.0]); e = np.array([5.0, 49, 100, 49, 5.0])
    assert df == 4
    assert x2 == pytest.approx(float(((o - e) ** 2 / e).sum()), abs=1e-12)


def test_feature_tests_are_calibrated_on_truly_random_draws():
    rng = np.random.default_rng(7)
    u = rng.random((1251, 45))
    draws = np.sort(np.argpartition(u, 6, axis=1)[:, :6] + 1, axis=1)
    res = stats_tests.feature_tests(draws)
    worst = min((v["p"], k) for k, v in res.items())
    assert worst[0] > 1e-3, f"무작위 추첨인데 {worst[1]} p={worst[0]:.2e} — 검정 도구가 틀렸다"


def test_all_lotto_tests_are_calibrated_on_truly_random_history():
    rng = np.random.default_rng(11)
    n = 1251
    draws = np.sort(np.argpartition(rng.random((n, 45)), 6, axis=1)[:, :6] + 1, axis=1)
    bonus = np.array([rng.choice(sorted(set(range(1, 46)) - set(d.tolist()))) for d in draws])
    res = stats_tests.lotto_tests(draws, bonus, np.arange(1, n + 1), b_mc=150)
    worst = min(res["summary"], key=lambda r: r["p"])
    assert worst["p"] > 1e-3, f"무작위 역사인데 '{worst['question']}' p={worst['p']:.2e}"


def test_all_pension_tests_are_calibrated_on_truly_random_history():
    rng = np.random.default_rng(13)
    n = 342
    res = stats_tests.pension_tests(rng.integers(1, 6, n), rng.integers(0, 10, (n, 6)),
                                    rng.integers(0, 10, (n, 6)), b_mc=150)
    worst = min(res["summary"], key=lambda r: r["p"])
    assert worst["p"] > 1e-3, f"무작위 역사인데 '{worst['question']}' p={worst['p']:.2e}"
