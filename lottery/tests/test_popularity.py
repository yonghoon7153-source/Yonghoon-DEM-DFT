import json

import numpy as np

import dataset
import popularity

RESULTS = json.loads((dataset.ROOT / "results" / "analysis.json").read_text(encoding="utf-8"))


def test_tier_probabilities_sum_to_three_or_more_matches():
    assert abs(sum(popularity.Q.values()) - sum(dataset.P_MATCH[k] for k in (3, 4, 5, 6))) < 1e-15


def test_pattern_features_known_values():
    f = popularity.pattern_features(np.array([[1, 8, 15, 22, 29, 36], [1, 2, 3, 10, 20, 30]]),
                                    np.array([1, 2, 3, 4, 5, 6]))
    # 1·8·15·22·29·36 은 용지(7열) 첫 세로줄 6개 / 1·2·3 은 같은 가로줄
    assert f.tolist() == [[0, 1, 6, 1], [2, 3, 2, 3]]


def test_recovery_positive_control_finds_planted_preferences():
    rc = popularity.recovery_check(dataset.load_lotto(), n_draws=60)
    assert rc["corr"] > 0.95, rc


def test_score_matches_stored_percentiles():
    S = RESULTS["lotto"]["popularity"]["score"]
    rng = np.random.default_rng(1)
    c = np.sort(np.argpartition(rng.random((20000, 45)), 6, axis=1)[:, :6] + 1, axis=1)
    eta, share = popularity.score_combos(c, S)
    # 무작위 조합의 백분위는 대략 균등해야 한다 (저장된 백분위표가 이 점수와 같은 기준인지 확인)
    pct = np.interp(eta, S["eta_percentiles"], S["pct"])
    assert abs(np.median(pct) - 50) < 3 and abs(np.mean(pct < 10) - 0.10) < 0.02
    assert np.all((share > 0) & (share <= 1))
