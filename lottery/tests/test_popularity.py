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


# ── 모델 C(1등 중 수동 비율) 의 과분산 척도 — 자체 리뷰 1차 F1.
# 리뷰 반례: statsmodels 0.15 의 fit(scale="X2") 는 2열(성공·실패) 응답에서 척도를 시행 수를 뺀 비율 잔차로
# 계산한다. 실제 데이터에서 0.187 (시행 수를 반영한 Pearson χ²/df 는 1.675), 순수 이항 합성에서도
# 0.12~0.15 (참값 1) → δ1 표준오차가 약 3배 작게 보고됐다 (공개 ±0.26, p 1.4e-178 → 정정 ±0.76, p 1.7e-21).

def _binomial_data(seed: int, n: int = 900, precision: float | None = None):
    """회차당 시행 수가 1등 당첨자 수처럼 작은(평균 약 9) 이항 자료. precision 을 주면 베타-이항(과분산)."""
    rng = np.random.default_rng(seed)
    trials = rng.poisson(8, n) + 1
    X = np.column_stack([np.ones(n), rng.normal(size=n), rng.normal(size=n), rng.normal(size=n) ** 2])
    p = 1 / (1 + np.exp(-(X @ np.array([-0.5, 0.4, 0.1, 0.0]))))
    if precision:  # 평균은 같고 회차마다 비율이 흔들린다: 분산 배수 ≈ 1 + (시행 수 − 1)/(precision + 1)
        p = rng.beta(p * precision, (1 - p) * precision)
    succ = rng.binomial(trials, p)
    return succ, trials - succ, X


def test_manual_model_scale_is_one_on_pure_binomial_data():
    import statsmodels.api as sm
    for seed in (1, 2, 3):
        man, aut, X = _binomial_data(seed)
        res = popularity.binomial_quasi(man, aut, X)
        exact = sm.GLM(np.column_stack([man, aut]), X, family=sm.families.Binomial()).fit()  # 참 척도 1
        assert 0.8 < res.scale < 1.25, (seed, res.scale)
        assert 0.88 < res.bse[1] / exact.bse[1] < 1.13, (seed, res.bse[1], exact.bse[1])


def test_manual_model_scale_detects_overdispersion():
    """척도를 1 로 고정해서 통과하는 수정이 아니어야 한다 — 과분산이면 φ > 1 로 표준오차를 넓힌다."""
    man, aut, X = _binomial_data(4, precision=4.0)  # 분산 배수 ≈ 1 + 8/5 = 2.6
    res = popularity.binomial_quasi(man, aut, X)
    assert 1.8 < res.scale < 3.5, res.scale
