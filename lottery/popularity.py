"""사람들이 어떤 번호를 고르나 — 회차별 1~5등 당첨자 수로 '번호 선택 인기도'를 추정한다.

추첨기는 무작위다 (stats_tests.py 의 결론). 그런데 1등 당첨금은 당첨자끼리 나눈다.
그러니 번호를 고를 때 바꿀 수 있는 건 '당첨 확률'이 아니라 '당첨됐을 때 몇 명과
나누나' 하나뿐이다. 그 '몇 명'은 사람들의 번호 선택 습관에 달려 있고, 습관은 등수별
당첨자 수에 고스란히 남는다.

자연 실험 두 개:
  (1) k등 기대 당첨자 = 판매 게임 수 × q_k 는 '모두가 무작위로 샀다면' 정확히 정해진다.
      실측/기대 비율이 1 보다 크면 그 주 당첨번호(의 부분집합)를 사람들이 많이 고른 것.
      5등(3개 일치)은 매주 수십만~백만 건이라 포아송 잡음이 0.1~0.3% 뿐이다.
  (2) 1등 자동/수동 구분(262회~): 자동은 기계가 균등하게 뽑으므로 대조군이다.
      같은 조합에서 수동 당첨자가 자동보다 많으면 수동 구매자가 그 조합을 선호한 것.

모델:
  A  등수별 log(실측/기대) = Σ 번호효과 β_i + 모양효과 θ·f(C)       (3·4·5등, OLS·HAC)
  B  1등 당첨자 수 ~ Poisson(기대 × exp(γ0 + γ1·s(C)))              (s = A 의 OOF 예측)
  C  수동/(수동+자동) ~ Binomial(logit = δ0 + δ1·s(C) + 시간추세)    (B 와 독립인 검증)

1~87회는 제외한다: 게임 가격 2,000원 시기이고 4등 실측/기대가 1.12 로 어긋난다
(88회 이후는 1~5등 모두 0.97~1.03). 로또 용지가 한 줄에 7개(1~7, 8~14, …)라는 것은
가정이다 — 가정이 틀리면 해당 지표가 유의하지 않게 나올 뿐 다른 추정은 영향받지 않는다.
"""
from __future__ import annotations

import numpy as np
import statsmodels.api as sm
from scipy import stats

import combos
import dataset

N = dataset.N_COMB
Q = {1: 1 / N, 2: 6 / N, 3: 228 / N, 4: 11115 / N, 5: 182780 / N}  # k등 해당 조합 비율
FIRST_ROUND = 88
PATTERNS = {  # 이름 → (라벨, 설명)
    "consec": ("연번 쌍", "연속된 두 수 쌍의 개수"),
    "prev_overlap": ("지난 회차와 겹침", "직전 회차 당첨번호와 겹치는 개수"),
    "slip_col_max": ("용지 같은 세로줄", "용지(7열) 한 세로줄에 몰린 최대 개수"),
    "slip_row_max": ("용지 같은 가로줄", "용지(7열) 한 가로줄에 몰린 최대 개수"),
}


def pattern_features(c: np.ndarray, prev: np.ndarray) -> np.ndarray:
    """(k,6) 조합, (k,6) 또는 (6,) 직전 당첨번호 → (k, 4) [연번, 겹침, 세로줄, 가로줄]."""
    c = np.asarray(c, dtype=np.int16)
    prev = np.broadcast_to(np.asarray(prev, dtype=np.int16), c.shape)
    consec = (np.diff(c, axis=1) == 1).sum(1)
    overlap = (c[:, :, None] == prev[:, None, :]).any(2).sum(1)
    col, row = (c - 1) % 7, (c - 1) // 7
    col_max = np.max([(col == k).sum(1) for k in range(7)], axis=0)
    row_max = np.max([(row == k).sum(1) for k in range(7)], axis=0)
    return np.stack([consec, overlap, col_max, row_max], axis=1).astype(float)


def _design(draws: np.ndarray, prevs: np.ndarray) -> np.ndarray:
    X = np.zeros((len(draws), 45))
    np.put_along_axis(X, draws.astype(int) - 1, 1.0, axis=1)
    return np.hstack([X, pattern_features(draws, prevs)])


def tier_targets(lotto: list[dataset.LottoDraw]) -> dict[int, np.ndarray]:
    return {k: np.log(np.array([d.winners[k - 1] for d in lotto]) /
                      np.array([d.games * Q[k] for d in lotto])) for k in (3, 4, 5)}


def _fit_ols(X: np.ndarray, y: np.ndarray, hac_lags: int = 4):
    return sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": hac_lags})


def _centered_number_effects(res) -> tuple[np.ndarray, np.ndarray]:
    """번호 지표 45개 계수를 평균 0 으로 맞춘 β 와 표준오차 (공분산까지 변환)."""
    b = res.params[:45]
    V = res.cov_params()[:45, :45]
    H = np.eye(45) - 1 / 45
    return H @ b, np.sqrt(np.diag(H @ V @ H))


def _blocked_oof(X: np.ndarray, y: np.ndarray, k: int = 5) -> np.ndarray:
    """연속 블록 k-fold 의 out-of-fold 예측 (시간 순서를 섞지 않는다)."""
    edges = np.linspace(0, len(y), k + 1).astype(int)
    pred = np.empty_like(y)
    for i in range(k):
        te = np.arange(edges[i], edges[i + 1])
        tr = np.setdiff1d(np.arange(len(y)), te)
        beta = np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]
        pred[te] = X[te] @ beta
    return pred


def binomial_quasi(success: np.ndarray, failure: np.ndarray, X: np.ndarray):
    """이항 GLM (성공·실패 횟수) + 과분산 척도 φ = Pearson χ²/잔차 자유도 (quasi-binomial) — 모델 C.

    statsmodels 0.15 의 fit(scale="X2") 는 2열 응답에서 척도를 시행 수를 뺀 비율 잔차로 계산해, 순수 이항
    자료에서도 φ ≈ 0.12 (참값 1) 를 내고 표준오차를 약 3배 작게 만든다 (자체 리뷰 F1). 그래서 척도 1 로
    한 번 적합한 뒤 시행 수를 반영한 pearson_chi2 로 φ 를 구해, 그 척도로 다시 적합한다.
    """
    y, fam = np.column_stack([success, failure]), sm.families.Binomial()
    first = sm.GLM(y, X, family=fam).fit()
    return sm.GLM(y, X, family=fam).fit(scale=first.pearson_chi2 / first.df_resid)


def fit(lotto: list[dataset.LottoDraw]) -> dict:
    allL = lotto
    L = [d for d in allL if d.round >= FIRST_ROUND]
    draws = np.array([d.numbers for d in L])
    prevs = np.array([allL[d.round - 2].numbers for d in L])  # 직전 회차 (round-1)
    X = _design(draws, prevs)
    ys = tier_targets(L)
    games = np.array([d.games for d in L])

    # ── 모델 A: 등수별 log(실측/기대)
    tiers = {}
    for k, y in ys.items():
        res = _fit_ols(X, y)
        beta, se = _centered_number_effects(res)
        oof = _blocked_oof(X, y)
        r2_oof = 1 - ((y - oof) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        half = len(y) // 2
        b1 = _centered_number_effects(_fit_ols(X[:half], y[:half]))[0]
        b2 = _centered_number_effects(_fit_ols(X[half:], y[half:]))[0]
        tiers[k] = {
            "beta": beta, "se": se, "theta": res.params[45:], "theta_se": res.bse[45:],
            "theta_p": res.pvalues[45:], "r2_in": float(res.rsquared), "r2_oof": float(r2_oof),
            "oof": oof, "sd_y": float(y.std()), "era_beta_r": float(np.corrcoef(b1, b2)[0, 1]),
            "res": res,
        }

    # 번호효과 전체가 0 인가 (Wald, 중심화 후 44 자유도)
    t5 = tiers[5]
    R = np.hstack([np.eye(45) - 1 / 45, np.zeros((45, 4))])[:44]
    wald = t5["res"].wald_test(R, scalar=True)

    # ── 모델 B: 1등 당첨자 수 (포아송, quasi 척도)
    s = t5["oof"] - t5["oof"].mean()  # OOF: 해당 회차 자신은 학습에 안 쓰였다
    w1 = np.array([d.winners[0] for d in L])
    off = np.log(games * Q[1])
    glm_b = sm.GLM(w1, sm.add_constant(s), family=sm.families.Poisson(), offset=off).fit(scale="X2")
    null_b = sm.GLM(w1, np.ones((len(w1), 1)), family=sm.families.Poisson(), offset=off).fit(scale="X2")
    mu = glm_b.predict(sm.add_constant(s), offset=off)
    dec = np.quantile(s, np.linspace(0, 1, 11))
    bins = np.clip(np.searchsorted(dec, s, side="right") - 1, 0, 9)
    calib = [{"s_mid": float(s[bins == b].mean()), "obs": float(w1[bins == b].mean()),
              "pred": float(mu[bins == b].mean()),
              "exp_uniform": float((games * Q[1])[bins == b].mean())} for b in range(10)]

    # ── 모델 C: 1등 중 수동 비율 (자동 = 무작위 대조군)
    mask = np.array([d.first_auto is not None and (d.first_auto + d.first_manual) > 0 for d in L])
    man = np.array([d.first_manual or 0 for d in L])[mask]
    aut = np.array([d.first_auto or 0 for d in L])[mask]
    rr = np.array([d.round for d in L])[mask]
    tz = (rr - rr.mean()) / rr.std()
    Xc = np.column_stack([np.ones(mask.sum()), s[mask], tz, tz ** 2])
    glm_c = binomial_quasi(man, aut, Xc)
    qs = np.quantile(s[mask], [0, .2, .4, .6, .8, 1])
    qb = np.clip(np.searchsorted(qs, s[mask], side="right") - 1, 0, 4)
    manual_by_s = [{"s_mid": float(s[mask][qb == b].mean()),
                    "manual_share": float(man[qb == b].sum() / (man[qb == b].sum() + aut[qb == b].sum())),
                    "winners": int(man[qb == b].sum() + aut[qb == b].sum())} for b in range(5)]

    # ── 생성기용 점수: η(C) = γ0 + γ1 · s5(C),  s5(C) = Σβ5_i + θ5·f(C) − 중심
    beta5, theta5 = t5["beta"], t5["theta"]
    latest = np.array(allL[-1].numbers)
    A = combos.all_combos()
    s_all = np.zeros(len(A))
    for i in range(6):
        s_all += beta5[A[:, i].astype(int) - 1]
    s_all += pattern_features(A, latest) @ theta5
    center = float(s_all.mean())  # 모든 조합 평균 0 (추첨 조합 평균과 같은 기준)
    g0, g1 = float(glm_b.params[0]), float(glm_b.params[1])
    eta_all = g0 + g1 * (s_all - center)
    pct = np.linspace(0, 100, 201)
    eta_q = np.percentile(eta_all, pct)

    recent = allL[-52:]
    g_next = float(np.mean([d.games for d in recent]))
    pool1 = float(np.mean([d.prize[0] * d.winners[0] for d in recent if d.winners[0] > 0]))

    def share(m):
        m = np.asarray(m, float)
        return np.where(m > 1e-9, (1 - np.exp(-m)) / np.maximum(m, 1e-9), 1.0)

    mu_avg = g_next * Q[1]
    mu_q = mu_avg * np.exp(eta_q)
    return {
        "first_round": FIRST_ROUND, "n_draws": len(L),
        "tiers": {k: {"r2_in": v["r2_in"], "r2_oof": v["r2_oof"], "sd_log_ratio": v["sd_y"],
                      "era_beta_r": v["era_beta_r"],
                      "theta": dict(zip(PATTERNS, map(float, v["theta"]))),
                      "theta_se": dict(zip(PATTERNS, map(float, v["theta_se"]))),
                      "theta_p": dict(zip(PATTERNS, map(float, v["theta_p"])))}
                  for k, v in tiers.items()},
        "number_effect": {"beta": beta5.tolist(), "se": t5["se"].tolist(),
                          "wald_chi2": float(np.squeeze(wald.statistic)),
                          "wald_df": 44, "wald_p": float(np.squeeze(wald.pvalue))},
        "first_prize_model": {
            "gamma0": g0, "gamma1": g1, "gamma1_se": float(glm_b.bse[1]),
            "gamma1_p": float(glm_b.pvalues[1]), "scale": float(glm_b.scale),
            "deviance": float(glm_b.deviance), "null_deviance": float(null_b.deviance),
            "deviance_explained": float(1 - glm_b.deviance / null_b.deviance),
            "calibration": calib},
        "manual_model": {
            "n_draws": int(mask.sum()), "manual": int(man.sum()), "auto": int(aut.sum()),
            "delta1": float(glm_c.params[1]), "delta1_se": float(glm_c.bse[1]),
            "delta1_p": float(glm_c.pvalues[1]), "scale": float(glm_c.scale), "by_s": manual_by_s},
        "score": {  # 사이트 JS 가 그대로 쓴다
            "beta": beta5.tolist(), "theta": theta5.tolist(), "pattern_names": list(PATTERNS),
            "center": center, "gamma0": g0, "gamma1": g1, "latest_numbers": latest.tolist(),
            "latest_round": allL[-1].round, "eta_percentiles": eta_q.tolist(), "pct": pct.tolist(),
            "games_next": g_next, "pool1_recent_mean": pool1, "mu_avg": mu_avg,
            "share_avg": float(share(mu_avg)), "share_at_pct": share(mu_q).tolist()},
    }


def recovery_check(lotto: list[dataset.LottoDraw], n_draws: int = 240, seed: int = 5) -> dict:
    """양성 대조: 선호를 아는 가상 구매자를 만들어 모델 A 가 그 선호를 되찾는지 본다.

    구매 모델: 조합 C 를 고를 확률 ∝ Π_{i∈C} w_i (전수 8,145,060 조합에 정규화).
    log w_i = 0.25·[i≤31] + 0.15·[i==7] + N(0, 0.05²). 실제 당첨번호 n_draws 개에 대해
    k등 기대 당첨자를 정확히 계산하고 포아송 잡음을 얹은 뒤 모델 A 를 적합한다.
    """
    rng = np.random.default_rng(seed)
    logw = 0.25 * (np.arange(1, 46) <= 31) + 0.15 * (np.arange(1, 46) == 7) + rng.normal(0, .05, 45)
    A = combos.all_combos()
    lp = logw[A.astype(int) - 1].sum(1)
    pi = np.exp(lp - lp.max())
    pi /= pi.sum()
    L = [d for d in lotto if d.round >= FIRST_ROUND]
    idx = rng.choice(len(L), size=min(n_draws, len(L)), replace=False)
    idx.sort()
    sub = [L[i] for i in idx]
    G = 60e6
    y = []
    for d in sub:
        mask = np.zeros(46, bool)
        mask[list(d.numbers)] = True
        m = mask[A].sum(1)
        exp5 = G * pi[m == 3].sum()
        y.append(np.log(rng.poisson(exp5) / (G * Q[5])))
    draws = np.array([d.numbers for d in sub])
    prevs = np.array([lotto[d.round - 2].numbers for d in sub])
    res = _fit_ols(_design(draws, prevs), np.array(y))
    beta, _ = _centered_number_effects(res)
    truth = logw - logw.mean()
    return {"corr": float(np.corrcoef(beta, truth)[0, 1]),
            "slope": float(np.polyfit(truth, beta, 1)[0]), "n_draws": len(sub)}


def score_combos(c: np.ndarray, score: dict) -> tuple[np.ndarray, np.ndarray]:
    """fit()['score'] 로 임의 조합의 η(로그 상대 인기도)와 1등 시 기대 몫(당첨금 비율)을 계산.

    사이트(JS)의 계산이 이 함수와 같아야 한다 — tests/test_site_js.py 가 node 로 교차검증한다.
    """
    c = np.atleast_2d(np.asarray(c, dtype=int))
    beta, theta = np.array(score["beta"]), np.array(score["theta"])
    s = beta[c - 1].sum(1) + pattern_features(c, np.array(score["latest_numbers"])) @ theta
    eta = score["gamma0"] + score["gamma1"] * (s - score["center"])
    mu = score["mu_avg"] * np.exp(eta)
    share = (1 - np.exp(-mu)) / mu
    return eta, share


def svr_comparison(lotto: list[dataset.LottoDraw]) -> dict:
    """강의 'SVM' 의 커널 트릭을 회귀(SVR, RBF)로: 선형(번호효과 합) 모델보다 5등 비율을 잘 맞히나?

    같은 연속 블록 5-fold 로 out-of-fold R² 를 비교한다. 비슷하거나 낮으면 인기도는
    '번호별 효과의 합'으로 충분히 설명된다는 뜻이다 (생성기는 해석 가능한 선형 모델을 쓴다).
    """
    from sklearn.svm import SVR
    from sklearn.preprocessing import StandardScaler
    L = [d for d in lotto if d.round >= FIRST_ROUND]
    draws = np.array([d.numbers for d in L])
    prevs = np.array([lotto[d.round - 2].numbers for d in L])
    X = _design(draws, prevs)
    y = tier_targets(L)[5]
    edges = np.linspace(0, len(y), 6).astype(int)
    out = {}
    for name, make in {"OLS (번호효과 합)": None,
                       "SVR RBF C=1": lambda: SVR(kernel="rbf", C=1.0, epsilon=0.1, gamma="scale"),
                       "SVR RBF C=10": lambda: SVR(kernel="rbf", C=10.0, epsilon=0.1, gamma="scale"),
                       "SVR 선형": lambda: SVR(kernel="linear", C=1.0, epsilon=0.1)}.items():
        pred = np.empty_like(y)
        for i in range(5):
            te = np.arange(edges[i], edges[i + 1])
            tr = np.setdiff1d(np.arange(len(y)), te)
            if make is None:
                pred[te] = X[te] @ np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]
            else:
                sx, sy = StandardScaler().fit(X[tr]), StandardScaler().fit(y[tr, None])
                m = make().fit(sx.transform(X[tr]), sy.transform(y[tr, None]).ravel())
                pred[te] = sy.inverse_transform(m.predict(sx.transform(X[te]))[:, None]).ravel()
        out[name] = float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum())
    return {"r2_oof": out, "target": "5등 log(실측/기대)", "n_draws": len(y)}
