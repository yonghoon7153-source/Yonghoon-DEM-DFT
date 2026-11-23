"""누수 검사: t회차 특징은 t회차 이후를 바꿔도 변하지 않아야 한다 (walk-forward 의 전제)."""
import numpy as np

import dataset
import ml_backtest as mb

L = dataset.load_lotto()
DRAWS = np.array([d.numbers for d in L])
BONUS = np.array([d.bonus for d in L])
WIN = np.array([d.winners for d in L], float)
GAMES = np.array([d.games for d in L])


def _future_scrambled(t):
    rng = np.random.default_rng(t)
    d, b, w, g = DRAWS.copy(), BONUS.copy(), WIN.copy(), GAMES.copy()
    d[t:] = np.sort(np.argpartition(rng.random((len(d) - t, 45)), 6, axis=1)[:, :6] + 1, axis=1)
    b[t:] = rng.integers(1, 46, len(d) - t)
    w[t:] = rng.integers(1, 10 ** 6, (len(d) - t, 5))
    g[t:] = rng.integers(10 ** 7, 10 ** 8, len(d) - t)
    return d, b, w, g


def test_lotto_features_do_not_see_the_drawn_round_or_later():
    F0, W0, _ = mb.lotto_features(DRAWS, BONUS, WIN, GAMES)
    for t in (5, 300, 900, len(L) - 1):
        F1, W1, _ = mb.lotto_features(*_future_scrambled(t))
        assert np.array_equal(F0[: t + 1], F1[: t + 1]), f"t={t} 특징이 t회차 이후 값에 의존"
        assert np.array_equal(W0[: t + 1], W1[: t + 1]), f"t={t} 창 입력이 t회차 이후 값에 의존"


def test_pension_features_do_not_see_the_drawn_round_or_later():
    first = np.array([[int(c) for c in d.number] for d in dataset.load_pension()])
    F0, _ = mb.pension_features(first)
    for t in (3, 100, len(first) - 1):
        f2 = first.copy()
        f2[t:] = np.random.default_rng(t).integers(0, 10, f2[t:].shape)
        F1, _ = mb.pension_features(f2)
        assert np.array_equal(F0[: t + 1], F1[: t + 1])


def test_prize_tiers():
    draw, bonus = np.array([1, 2, 3, 4, 5, 6]), 7
    prize = np.array([2_000_000_000, 50_000_000, 1_500_000, 50_000, 5_000])
    assert mb._prize(np.array([1, 2, 3, 4, 5, 6]), draw, bonus, prize) == (6, 2_000_000_000)
    assert mb._prize(np.array([1, 2, 3, 4, 5, 7]), draw, bonus, prize) == (5, 50_000_000)
    assert mb._prize(np.array([1, 2, 3, 4, 5, 8]), draw, bonus, prize) == (5, 1_500_000)
    assert mb._prize(np.array([1, 2, 3, 4, 9, 8]), draw, bonus, prize) == (4, 50_000)
    assert mb._prize(np.array([1, 2, 3, 10, 9, 8]), draw, bonus, prize) == (3, 5_000)
    assert mb._prize(np.array([1, 2, 7, 10, 9, 8]), draw, bonus, prize) == (2, 0)


def test_models_are_deterministic_on_real_features():
    """같은 입력이면 같은 결과. 2026-11-23 weekly_update --force 재실행 비교에서 선형 SVM(liblinear 는
    random_state 가 없으면 좌표 하강 순서를 매번 다르게 섞는다)만 적중 수가 달랐다 (0.7897 vs 0.7886)."""
    F, W, X = mb.lotto_features(DRAWS, BONUS, WIN, GAMES)
    tr, te = slice(100, 400), slice(400, 450)
    for name, (src, make) in mb._models().items():
        if src == "F_sub":
            continue  # RBF SVC(libsvm)는 결정적이고 느리다 — 다른 모델로 충분
        A = W if src == "W" else F
        Z, y, Zt = A[tr].reshape(-1, A.shape[2]), X[tr].reshape(-1), A[te].reshape(-1, A.shape[2])
        s1 = mb._score(make().fit(Z, y), Zt)
        s2 = mb._score(make().fit(Z, y), Zt)
        assert np.array_equal(s1, s2), f"{name}: 같은 입력인데 결과가 다르다 (random_state?)"
