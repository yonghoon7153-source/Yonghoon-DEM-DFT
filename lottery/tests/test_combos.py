import itertools
import random

import numpy as np

import combos


def test_enumeration_order_matches_rank_of():
    A = combos.all_combos()
    assert A.shape == (8_145_060, 6)
    rng = random.Random(3)
    for _ in range(200):
        c = tuple(sorted(rng.sample(range(1, 46), 6)))
        assert tuple(A[combos.rank_of(c)]) == c
    assert combos.rank_of((1, 2, 3, 4, 5, 6)) == 0 and combos.rank_of((40, 41, 42, 43, 44, 45)) == 8_145_059


def test_features_of_known_combos():
    f = combos.features(np.array([[1, 2, 3, 4, 5, 6], [7, 14, 21, 28, 35, 42]]))
    assert f["sum"].tolist() == [21, 147]
    assert f["odd"].tolist() == [3, 3] and f["low"].tolist() == [6, 3]
    assert f["consec"].tolist() == [5, 0]
    assert f["ac"].tolist() == [0, 0]           # 같은 간격 수열은 차이값이 5종 → AC 0
    assert f["decades"].tolist() == [1, 5] and f["birthday"].tolist() == [6, 4]


def test_exact_distributions_are_probabilities_with_known_values():
    ex = combos.exact_distributions()
    for name, d in ex.items():
        assert abs(sum(d.values()) - 1) < 1e-12, name
    assert ex["sum"][21] * combos.N_COMB == 1 and ex["sum"][255] * combos.N_COMB == 1
    # 홀수 개수 ~ 초기하(45, 23, 6)
    from math import comb
    for k in range(7):
        assert abs(ex["odd"][k] - comb(23, k) * comb(22, 6 - k) / combos.N_COMB) < 1e-15
