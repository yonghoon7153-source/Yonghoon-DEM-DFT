"""생성 모델로 '당첨번호 같은' 번호를 만들 수 있나 — 확산 모델(DDPM) · EM 혼합모형.

확산 모델 (강의 '15 Diffusion models' = Ho et al. 2020 DDPM 그대로):
  전방 과정 q(x_t | x_{t-1}) = N(√(1-β_t)·x_{t-1}, β_t·I),  β_t: 1e-4 → 0.02 선형, T = 1000
  한 번에 점프 x_t = √ᾱ_t·x_0 + √(1-ᾱ_t)·ε,  학습 목표: 신경망이 ε 을 맞히도록 (MSE)
  역방향 x_{t-1} = (x_t − β_t/√(1-ᾱ_t)·ε̂) / √α_t + σ_t·z,  σ_t² = β_t
  데이터 표현: 당첨번호 6개 → 45칸 벡터 (뽑힌 칸 +1, 나머지 −1). 생성 결과는 값이 큰 6칸.
  잡음 예측망 ε_θ(x_t, t): sklearn MLPRegressor (입력 = x_t 45칸 + 시간 임베딩 17칸).
  매 epoch 새 (t, ε) 를 뽑아 partial_fit — DDPM 학습 루프와 같다.

평가 (1~1000회로 학습, 1001회~ 로 검증):
  - 외우기(memorization): 생성 번호가 학습 당첨번호와 똑같은 비율 (균등 무작위면 1000/8,145,060)
  - 분포 재현: 생성 번호의 총합·홀짝·연번… 분포가 '모든 조합' 분포와 얼마나 가까운가
  - 적중: 생성 번호로 1001회~ 를 샀다면 평균 몇 개 맞혔나 (귀무 = 0.8)

EM 혼합모형 (강의 '13 Expectation Maximization'):
  당첨번호에 숨은 '유형'(군집)이 있나? 베르누이 혼합을 K=1..4 로 EM 적합하고 BIC 와
  로그우도 증가를 '진짜 무작위 가상 역사' 의 같은 값과 비교한다.
"""
from __future__ import annotations

import numpy as np
from sklearn.neural_network import MLPRegressor

import combos

SEED = 20261123


class DDPM:
    def __init__(self, T: int = 1000, beta_1: float = 1e-4, beta_T: float = 0.02,
                 hidden=(256, 256), seed: int = SEED):
        self.T = T
        self.beta = np.linspace(beta_1, beta_T, T)  # 인덱스 t-1 ↔ 시간 t
        self.alpha = 1.0 - self.beta
        self.abar = np.cumprod(self.alpha)
        self.rng = np.random.default_rng(seed)
        self.net = MLPRegressor(hidden_layer_sizes=hidden, activation="relu", solver="adam",
                                learning_rate_init=1e-3, batch_size=256, random_state=seed)
        self.losses: list[float] = []

    def _emb(self, t: np.ndarray) -> np.ndarray:
        k = np.arange(8)
        w = np.exp(-np.log(1000.0) * k / 8)  # 1 ~ 1/1000 주파수
        ang = t[:, None] * w[None, :]
        return np.hstack([np.sin(ang), np.cos(ang), (t / self.T)[:, None]])

    def fit(self, x0: np.ndarray, epochs: int = 80, rows: int = 40000) -> "DDPM":
        for _ in range(epochs):
            idx = self.rng.integers(0, len(x0), rows)
            t = self.rng.integers(1, self.T + 1, rows)
            eps = self.rng.standard_normal((rows, x0.shape[1]))
            ab = self.abar[t - 1][:, None]
            xt = np.sqrt(ab) * x0[idx] + np.sqrt(1 - ab) * eps
            self.net.partial_fit(np.hstack([xt, self._emb(t.astype(float))]), eps)
            self.losses.append(float(self.net.loss_))
        return self

    def sample(self, n: int) -> np.ndarray:
        x = self.rng.standard_normal((n, self.net.n_outputs_))
        for t in range(self.T, 0, -1):
            eps_hat = self.net.predict(np.hstack([x, self._emb(np.full(n, float(t)))]))
            mean = (x - self.beta[t - 1] / np.sqrt(1 - self.abar[t - 1]) * eps_hat) / np.sqrt(self.alpha[t - 1])
            x = mean + (np.sqrt(self.beta[t - 1]) * self.rng.standard_normal(x.shape) if t > 1 else 0.0)
        return x


def to_vec(draws: np.ndarray) -> np.ndarray:
    v = -np.ones((len(draws), 45))
    np.put_along_axis(v, draws.astype(int) - 1, 1.0, axis=1)
    return v


def decode(x: np.ndarray) -> np.ndarray:
    return np.sort(np.argsort(-x, axis=1)[:, :6] + 1, axis=1)


def _tv(p: dict, q: dict) -> float:
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def _emp(v: np.ndarray) -> dict:
    vals, cnt = np.unique(v, return_counts=True)
    return {int(a): b / len(v) for a, b in zip(vals, cnt)}


def evaluate_ddpm(draws: np.ndarray, n_train: int = 1000, n_gen: int = 3000, epochs: int = 80) -> dict:
    rng = np.random.default_rng(SEED)
    train, test = draws[:n_train], draws[n_train:]
    model = DDPM().fit(to_vec(train), epochs=epochs)
    raw = model.sample(n_gen)
    gen = decode(raw)
    srt = np.sort(raw, axis=1)[:, ::-1]
    six_clear = float(((srt[:, 5] > 0) & (srt[:, 6] < 0)).mean())  # 정확히 6칸만 양수
    uni = np.sort(np.argpartition(rng.random((n_gen, 45)), 6, axis=1)[:, :6] + 1, axis=1)

    def overlap_stats(c):
        Xc = np.zeros((len(c), 45)); np.put_along_axis(Xc, c - 1, 1, axis=1)
        Xt = np.zeros((len(train), 45)); np.put_along_axis(Xt, train - 1, 1, axis=1)
        ov = (Xc @ Xt.T).max(1)
        return {"exact_copy_rate": float((ov == 6).mean()), "max_overlap_hist": np.bincount(
            ov.astype(int), minlength=7).astype(int).tolist(), "mean_max_overlap": float(ov.mean())}

    exact = combos.exact_distributions()
    fg, fu, ft = combos.features(gen), combos.features(uni), combos.features(train)
    fidelity = {k: {"label": combos.FEATURES[k][0], "tv_generated": _tv(_emp(fg[k]), exact[k]),
                    "tv_uniform_same_n": _tv(_emp(fu[k]), exact[k]),
                    "tv_training_draws": _tv(_emp(ft[k]), exact[k])} for k in exact}
    # 적중: 생성 번호 k 번째로 1001+k 회차를 샀다고 치면
    T = len(test)
    hits = np.array([len(set(gen[k % n_gen]) & set(test[k])) for k in range(T)])
    allhits = (to_vec(gen) > 0).astype(float) @ (to_vec(test) > 0).astype(float).T
    z = (hits.sum() - 0.8 * T) / np.sqrt(0.6146 * T)
    counts = np.bincount(gen.ravel(), minlength=46)[1:]
    return {
        "train_rounds": [1, n_train], "test_rounds": [n_train + 1, len(draws)],
        "n_generated": n_gen, "epochs": epochs, "final_loss": model.losses[-1],
        "loss_curve": model.losses, "six_clear_rate": six_clear,
        "memorization": overlap_stats(gen), "memorization_uniform": overlap_stats(uni),
        "exact_copy_rate_expected_uniform": n_train / combos.N_COMB,
        "fidelity": fidelity,
        "hits_one_per_draw": {"mean": float(hits.mean()), "z": float(z), "n": T},
        "hits_all_pairs_mean": float(allhits.mean()),
        "number_counts": counts.astype(int).tolist(),
        "examples": gen[:12].tolist(),
        "generated": gen,  # build 가 인기도 비교에 쓰고 data.js 에는 넣지 않는다
        "corr_with_train_freq": float(np.corrcoef(
            counts, np.bincount(train.ravel(), minlength=46)[1:])[0, 1]),
    }


def train_generator_pool(draws: np.ndarray, n_pool: int = 600, epochs: int = 80) -> list[list[int]]:
    """사이트의 '확산 모델' 버튼용: 전체 회차로 학습한 모델이 만든 번호 묶음 (과거 1등 조합 제외)."""
    model = DDPM(seed=SEED + 1).fit(to_vec(draws), epochs=epochs)
    gen = decode(model.sample(n_pool))
    past = {tuple(d) for d in draws.tolist()}
    return [list(map(int, g)) for g in gen.tolist() if tuple(g) not in past]


# ───────────────────────── EM: 베르누이 혼합 ─────────────────────────

def bernoulli_mixture(X: np.ndarray, K: int, n_init: int = 4, iters: int = 300, seed: int = SEED):
    """EM. 반환 (로그우도, 혼합비, θ)."""
    rng = np.random.default_rng(seed)
    n, d = X.shape
    best = (-np.inf, None, None)
    for _ in range(n_init):
        pi = np.full(K, 1 / K)
        th = np.clip(X.mean(0) + rng.normal(0, 0.03, (K, d)), 0.02, 0.98)
        prev = -np.inf
        for _ in range(iters):
            logp = X @ np.log(th).T + (1 - X) @ np.log(1 - th).T + np.log(pi)
            mx = logp.max(1, keepdims=True)
            ll = float((mx[:, 0] + np.log(np.exp(logp - mx).sum(1))).sum())
            r = np.exp(logp - mx)
            r /= r.sum(1, keepdims=True)  # E-step: 책임도
            nk = r.sum(0) + 1e-9
            pi = nk / n  # M-step
            th = np.clip((r.T @ X + 1) / (nk[:, None] + 2), 1e-4, 1 - 1e-4)
            if ll - prev < 1e-6:
                break
            prev = ll
        if ll > best[0]:
            best = (ll, pi, th)
    return best


def em_cluster_test(draws: np.ndarray, Ks=(1, 2, 3, 4), b_null: int = 30) -> dict:
    X = (to_vec(draws) > 0).astype(float)
    n = len(X)

    def fit_all(Z):
        return {K: bernoulli_mixture(Z, K)[0] for K in Ks}

    ll = fit_all(X)
    bic = {K: -2 * ll[K] + (K * 45 + K - 1) * np.log(n) for K in Ks}
    rng = np.random.default_rng(SEED)
    null_gain = []
    for _ in range(b_null):
        d = np.sort(np.argpartition(rng.random((n, 45)), 6, axis=1)[:, :6] + 1, axis=1)
        Z = (to_vec(d) > 0).astype(float)
        l1, l2 = bernoulli_mixture(Z, 1)[0], bernoulli_mixture(Z, 2)[0]
        null_gain.append(l2 - l1)
    gain = ll[2] - ll[1]
    null_gain = np.array(null_gain)
    return {"loglik": {int(k): float(v) for k, v in ll.items()},
            "bic": {int(k): float(v) for k, v in bic.items()},
            "best_k_bic": int(min(bic, key=bic.get)),
            "gain_k2_vs_k1": float(gain), "null_gain_mean": float(null_gain.mean()),
            "null_gain_sd": float(null_gain.std()),
            "p_mc": float((1 + (null_gain >= gain).sum()) / (1 + len(null_gain)))}
