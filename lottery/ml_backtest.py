"""번호 예측 머신러닝 백테스트 — 어떤 모델이 무작위보다 잘 맞히나?

walk-forward: t회차를 예측할 때는 1..t-1회차만 본다. 특징 행렬 F[t] 는 t회차 이후를
바꿔도 변하지 않는다 (tests/test_ml.py 가 누수 검사로 고정). 모델은 100회차마다 그때까지의
자료로 다시 학습하고 다음 100회차를 예측한다.

귀무가설(모든 회차가 독립·균등)에서는 '과거만 보고 고른 6개'가 맞히는 개수가 어떤
전략이든 초기하분포(45, 6, 6) 를 따른다: 평균 0.8, 분산 0.6146. 그래서 모델의 평균
적중 수를 이 정확한 귀무분포와 비교하고, 모델이 여러 개이므로 Bonferroni 로 보정한다
(가장 좋은 모델만 골라 보고하면 우연히 좋은 것을 고르게 된다 — 선택 편향).

같은 파이프라인을 '진짜 무작위로 만든 가상 역사'에도 돌려 실제 데이터 결과와 나란히
보인다 (양쪽이 구분되지 않으면 모델이 찾은 건 패턴이 아니라 잡음이다).

모델 출처: 강의 '머신러닝'(로지스틱 회귀, SVM 소프트 마진·커널 트릭, 신경망, 나이브
베이즈) + 트리 앙상블. 특징에는 직전 회차 1~5등 당첨자 수(기대 대비 비율)와 판매량도
넣었다 — 사람들의 선택이 다음 추첨에 영향을 주는지 보려는 것이다.
"""
from __future__ import annotations

import time

import numpy as np
from scipy import stats
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC

from stats_tests import HYPER_VAR, P1, P2

SEED = 20261123
TIER_Q = {1: 1 / 8145060, 2: 6 / 8145060, 3: 228 / 8145060, 4: 11115 / 8145060, 5: 182780 / 8145060}

FEATURES = [
    "freq_all", "freq_5", "freq_10", "freq_20", "freq_50", "freq_100", "log_gap",
    "in_last", "bonus_last", "neighbor_last", "pair_aff", "lag_aff",
    "num", "birthday", "last_digit",
    "t1_last", "t2_last", "t3_last", "t4_last", "t5_last", "log_games_last", "t5_last_x_in_last",
]


def lotto_features(draws: np.ndarray, bonus: np.ndarray, winners: np.ndarray,
                   games: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """→ F (n,45,len(FEATURES)), W (n,45,55) 원본 창 입력, Y (n,45). F[t] 는 회차 < t 만 쓴다."""
    n = len(draws)
    X = np.zeros((n, 45))
    np.put_along_axis(X, draws.astype(int) - 1, 1.0, axis=1)
    C = np.vstack([np.zeros(45), np.cumsum(X, 0)[:-1]])  # C[t] = Σ_{s<t} X[s]
    t_idx = np.arange(n)[:, None]
    F = np.zeros((n, 45, len(FEATURES)))
    F[:, :, 0] = C / np.maximum(t_idx, 1)
    for k, w in enumerate((5, 10, 20, 50, 100)):
        lo = np.maximum(np.arange(n) - w, 0)
        F[:, :, 1 + k] = (C - C[lo]) / np.maximum(np.minimum(w, np.arange(n)), 1)[:, None]
    last = np.full(45, -1.0)
    Pc = np.zeros((45, 45))  # Σ_{s<t} X_sᵀX_s
    Lc = np.zeros((45, 45))  # Σ_{s+1<t} X_sᵀX_{s+1}
    prevc = np.zeros(45)  # Σ_{s+1<t} X_s
    # 직전 회차 당첨자 비율 (log 실측/기대; 1·2등은 0 명 대비 +0.5)
    tl = np.zeros((n, 5))
    for k in range(1, 6):
        tl[:, k - 1] = np.log((winners[:, k - 1] + (0.5 if k <= 2 else 0)) / (games * TIER_Q[k]))
    lg = np.log(games)
    for t in range(n):
        F[t, :, 6] = np.log1p(t - last)  # 마지막 출현 이후 회차 수
        if t >= 1:
            prev = draws[t - 1].astype(int) - 1
            F[t, :, 7] = X[t - 1]
            F[t, bonus[t - 1] - 1, 8] = 1.0
            nb = np.zeros(45)
            for p in prev:
                for q in (p - 1, p + 1):
                    if 0 <= q < 45:
                        nb[q] = 1.0
            nb[prev] = 0.0
            F[t, :, 9] = nb
            if t >= 2:
                Poff = Pc.copy()
                np.fill_diagonal(Poff, 0.0)  # 자기 자신과의 '쌍'(= 출현 횟수)은 궁합이 아니다
                F[t, :, 10] = Poff[:, prev].mean(1) / (t * P2)
                denom = np.maximum(prevc[prev] * P1, 1e-9)
                F[t, :, 11] = (Lc[prev, :] / denom[:, None]).mean(0)
            F[t, :, 15:20] = tl[t - 1]
            F[t, :, 20] = lg[t - 1] - lg[max(t - 2, 0)]
            F[t, :, 21] = tl[t - 1, 4] * X[t - 1]
        # t 회차를 본 뒤 누적 갱신 (다음 회차의 특징에만 쓰인다)
        Pc += np.outer(X[t], X[t])
        if t >= 1:
            Lc += np.outer(X[t - 1], X[t])
            prevc += X[t - 1]
        last[X[t] > 0] = t
    nums = np.arange(1, 46)
    F[:, :, 12] = nums / 45
    F[:, :, 13] = nums <= 31
    F[:, :, 14] = nums % 10
    # 원본 창 입력: 각 번호의 최근 10회 출현 여부 + 직전 회차 45칸
    W = np.zeros((n, 45, 55))
    for lag in range(1, 11):
        W[lag:, :, lag - 1] = X[:-lag]
    W[1:, :, 10:] = X[:-1][:, None, :]
    return F, W, X


def _models() -> dict:
    sc = StandardScaler
    return {
        "로지스틱 회귀": ("F", lambda: make_pipeline(sc(), LogisticRegression(C=1.0, max_iter=3000))),
        "선형 SVM (소프트 마진)": ("F", lambda: make_pipeline(sc(), LinearSVC(C=0.05, loss="hinge", max_iter=20000))),
        "커널 SVM (RBF)": ("F_sub", lambda: make_pipeline(sc(), SVC(C=1.0, kernel="rbf", gamma="scale"))),
        "나이브 베이즈": ("F", lambda: make_pipeline(sc(), GaussianNB())),
        "신경망 MLP": ("F", lambda: make_pipeline(sc(), MLPClassifier(
            hidden_layer_sizes=(32, 16), alpha=1e-3, early_stopping=True, max_iter=300, random_state=0))),
        "신경망 (최근 10회 원본 입력)": ("W", lambda: MLPClassifier(
            hidden_layer_sizes=(64, 32), alpha=1e-3, early_stopping=True, max_iter=300, random_state=0)),
        "그래디언트 부스팅": ("F", lambda: HistGradientBoostingClassifier(
            max_iter=200, learning_rate=0.05, random_state=0)),
        "랜덤 포레스트": ("F", lambda: RandomForestClassifier(
            n_estimators=200, max_depth=8, min_samples_leaf=50, n_jobs=-1, random_state=0)),
    }


BASELINES = {  # 이름 → F 의 특징 열 (점수 높을수록 선택), 부호
    "최다 출현 (전체)": (0, 1), "최다 출현 (최근 10회)": (2, 1), "최다 출현 (최근 50회)": (4, 1),
    "오래 안 나온 번호": (6, 1), "지난 회차 번호 그대로": (7, 1), "궁합수 점수": (10, 1),
    "직전→다음 연결 점수": (11, 1),
}


def _score(model, Z: np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(Z)[:, 1]
    return model.decision_function(Z)


def _top6(scores: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    jitter = rng.random(scores.shape) * 1e-9 * (np.abs(scores).max() + 1)
    return np.argsort(-(scores + jitter), axis=1)[:, :6]


def _prize(pred: np.ndarray, draw: np.ndarray, bonus: int, prize: np.ndarray) -> tuple[int, int]:
    m = len(set(pred.tolist()) & set(draw.tolist()))
    b = bonus in set(pred.tolist())
    tier = {6: 1, 5: 2 if b else 3, 4: 4, 3: 5}.get(m, 0)
    return m, (int(prize[tier - 1]) if tier else 0)


def _auc(y: np.ndarray, s: np.ndarray) -> float:
    r = stats.rankdata(s)
    pos = y > 0.5
    n1, n0 = pos.sum(), (~pos).sum()
    return float((r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def lotto_backtest(draws, bonus, winners, games, prizes, price, *, start=300, block=100,
                   train_from=100, svm_window=200, label="real") -> dict:
    n = len(draws)
    F, W, X = lotto_features(draws, bonus, winners, games)
    rng = np.random.default_rng(SEED)
    tests = np.arange(start, n)
    scores: dict[str, np.ndarray] = {}
    probs: dict[str, np.ndarray] = {}
    timing = {}
    scores["무작위 (기준선)"] = rng.random((len(tests), 45))
    for name, (col, sign) in BASELINES.items():
        scores[name] = sign * F[tests, :, col]
    for name, (src, make) in _models().items():
        t0 = time.time()
        out = np.zeros((len(tests), 45))
        pout = np.zeros((len(tests), 45)) if src != "F_sub" else None
        for b0 in range(start, n, block):
            b1 = min(b0 + block, n)
            lo = max(train_from, b0 - svm_window) if src == "F_sub" else train_from
            A = W if src == "W" else F
            Ztr = A[lo:b0].reshape(-1, A.shape[2])
            ytr = X[lo:b0].reshape(-1)
            m = make().fit(Ztr, ytr)
            Zte = A[b0:b1].reshape(-1, A.shape[2])
            out[b0 - start:b1 - start] = _score(m, Zte).reshape(-1, 45)
            if pout is not None and hasattr(m, "predict_proba"):
                pout[b0 - start:b1 - start] = m.predict_proba(Zte)[:, 1].reshape(-1, 45)
        scores[name] = out
        if pout is not None and hasattr(_models()[name][1](), "predict_proba"):
            probs[name] = np.clip(pout, 1e-6, 1 - 1e-6)
        timing[name] = round(time.time() - t0, 1)

    y = X[tests]
    base_ll = -(y * np.log(P1) + (1 - y) * np.log(1 - P1)).mean()
    T = len(tests)
    rows = []
    for name, s in scores.items():
        top = _top6(s, rng)
        hits, won = [], 0
        for k, t in enumerate(tests):
            m, w = _prize(top[k] + 1, draws[t], int(bonus[t]), prizes[t])
            hits.append(m)
            won += w
        hits = np.array(hits)
        z = (hits.sum() - 0.8 * T) / np.sqrt(HYPER_VAR * T)
        row = {"model": name, "mean_hits": float(hits.mean()),
               "ci95": [float(hits.mean() - 1.96 * np.sqrt(HYPER_VAR / T)),
                        float(hits.mean() + 1.96 * np.sqrt(HYPER_VAR / T))],
               "z": float(z), "p_better": float(stats.norm.sf(z)),
               "hit_hist": np.bincount(hits, minlength=7).astype(int).tolist(),
               "auc": _auc(y.ravel(), s.ravel()), "spent": int(price[tests].sum()), "won": int(won),
               "seconds": timing.get(name)}
        if name in probs:
            p = probs[name]
            row["dlogloss"] = float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean() - base_ll)
        rows.append(row)
    m = len(rows)
    for r in rows:
        r["p_bonferroni"] = min(1.0, r["p_better"] * m)
    pmf = [float(stats.hypergeom.pmf(k, 45, 6, 6)) for k in range(7)]
    return {"label": label, "test_rounds": [int(tests[0] + 1), int(tests[-1] + 1)], "n_test": int(T),
            "expected_hits": 0.8, "hit_pmf": pmf, "n_models": m, "rows": rows,
            "features": FEATURES}


# ───────────────────────── 연금복권 720+ ─────────────────────────

PEN_FEATURES = ["freq_all", "freq_10", "freq_30", "log_gap", "last_is_d", "pos", "digit"]
PEN_PRIZE = {6: 0, 5: 1_000_000, 4: 100_000, 3: 50_000, 2: 5_000, 1: 1_000}  # 끝자리 일치 개수 → 상금
# (6자리 전부 = 2등(조 불일치) 또는 1등 — 조까지 맞히는 건 따로 다루지 않는다)


def pension_features(first: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """first (n,6) 자리별 숫자 → F (n,6,10,k), Y (n,6,10). F[t] 는 회차 < t 만 쓴다."""
    n = len(first)
    Y = np.zeros((n, 6, 10))
    for p in range(6):
        Y[np.arange(n), p, first[:, p]] = 1.0
    C = np.concatenate([np.zeros((1, 6, 10)), np.cumsum(Y, 0)[:-1]])
    F = np.zeros((n, 6, 10, len(PEN_FEATURES)))
    t = np.arange(n)[:, None, None]
    F[..., 0] = C / np.maximum(t, 1)
    for k, w in ((1, 10), (2, 30)):
        lo = np.maximum(np.arange(n) - w, 0)
        F[..., k] = (C - C[lo]) / np.maximum(np.minimum(w, np.arange(n)), 1)[:, None, None]
    last = np.full((6, 10), -1.0)
    for i in range(n):
        F[i, :, :, 3] = np.log1p(i - last)
        if i >= 1:
            F[i, :, :, 4] = Y[i - 1]
        last[Y[i] > 0] = i
    F[..., 5] = np.arange(6)[None, :, None] / 5
    F[..., 6] = np.arange(10)[None, None, :] / 9
    return F, Y


def pension_backtest(first: np.ndarray, *, start=60, block=50, label="real") -> dict:
    n = len(first)
    F, Y = pension_features(first)
    rng = np.random.default_rng(SEED)
    tests = np.arange(start, n)
    sc = StandardScaler
    models = {
        "로지스틱 회귀": lambda: make_pipeline(sc(), LogisticRegression(max_iter=3000)),
        "선형 SVM (소프트 마진)": lambda: make_pipeline(sc(), LinearSVC(C=0.05, loss="hinge", max_iter=20000)),
        "커널 SVM (RBF)": lambda: make_pipeline(sc(), SVC(C=1.0, kernel="rbf", gamma="scale")),
        "나이브 베이즈": lambda: make_pipeline(sc(), GaussianNB()),
        "신경망 MLP": lambda: make_pipeline(sc(), MLPClassifier(hidden_layer_sizes=(16,), alpha=1e-3,
                                                              max_iter=500, random_state=0)),
        "그래디언트 부스팅": lambda: HistGradientBoostingClassifier(max_iter=100, learning_rate=0.05,
                                                                random_state=0),
    }
    scores = {"무작위 (기준선)": rng.random((len(tests), 6, 10)),
              "최다 출현 (전체)": F[tests, :, :, 0], "최다 출현 (최근 10회)": F[tests, :, :, 1],
              "오래 안 나온 숫자": F[tests, :, :, 3], "지난 회차 숫자 그대로": F[tests, :, :, 4]}
    for name, make in models.items():
        out = np.zeros((len(tests), 6, 10))
        for b0 in range(start, n, block):
            b1 = min(b0 + block, n)
            lo = max(10, b0 - 120) if "RBF" in name else 10  # 커널 SVM 은 O(n²) — 최근 120회만
            m = make().fit(F[lo:b0].reshape(-1, F.shape[3]), Y[lo:b0].reshape(-1))
            out[b0 - start:b1 - start] = _score(m, F[b0:b1].reshape(-1, F.shape[3])).reshape(-1, 6, 10)
        scores[name] = out
    T = len(tests)
    rows = []
    for name, s in scores.items():
        pick = np.argmax(s + rng.random(s.shape) * 1e-9, axis=2)  # (T, 6)
        correct = pick == first[tests]
        acc = correct.mean()
        k = correct.sum()
        z = (k - 0.1 * T * 6) / np.sqrt(T * 6 * 0.09)
        trail = np.array([next((j for j in range(6) if not correct[i, 5 - j]), 6) for i in range(T)])
        won = int(sum(PEN_PRIZE[j] for j in trail if j > 0))
        rows.append({"model": name, "accuracy": float(acc), "z": float(z),
                     "p_better": float(stats.norm.sf(z)), "spent": int(T * 1000), "won": won,
                     "trail_hist": np.bincount(trail, minlength=7).astype(int).tolist()})
    for r in rows:
        r["p_bonferroni"] = min(1.0, r["p_better"] * len(rows))
    return {"label": label, "test_rounds": [int(tests[0] + 1), int(tests[-1] + 1)], "n_test": int(T),
            "expected_accuracy": 0.1, "rows": rows}
