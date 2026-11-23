"""무작위성 검정 + 숫자 간 관계 분석 (로또 6/45 · 연금복권 720+).

질문 하나에 검정 하나를 대응시킨다:
  - 특정 번호가 더 잘 나오나?            → 빈도 카이제곱 (비복원 보정 44/39) + 몬테카를로
  - 같이 잘 나오는 번호 쌍(궁합수)이 있나? → 990쌍 정확 이항검정 + Holm/BH 다중비교 보정
  - 세 개 묶음은?                          → 14,190 삼중쌍 최댓값 vs 몬테카를로
  - 지난주 번호가 이번 주에 영향을 주나?  → 이월수(초기하분포) · 이웃수 · 45×45 시차 행렬
  - 오래 안 나온 번호는 '나올 때가 됐나'? → 출현 간격 vs 기하분포
  - 총합·홀짝·연번·AC값 '패턴'은?         → 8,145,060 조합 전수 분포와 적합도 검정
  - 과거에 잘 나온 번호가 계속 잘 나오나? → 전반기/후반기 빈도 상관 · 시대별 동질성

몬테카를로 귀무분포는 '같은 회차 수만큼 진짜 무작위로 뽑은 가상 역사'를 B번 만들어
같은 통계량을 잰 것이다 (seed 고정, 재현 가능). 다중비교는 '검정을 많이 하면 우연히
작은 p 가 나온다'는 착시를 막는 장치다 — 990쌍을 보면 p<0.05 인 쌍이 ~50개 나오는 게
정상이다.
"""
from __future__ import annotations

from math import comb

import numpy as np
from scipy import stats

import combos

SEED = 20261123
P1 = 6 / 45  # 한 번호가 한 회차에 나올 확률
P2 = (6 * 5) / (45 * 44)  # 특정 두 번호가 함께 나올 확률 = 1/66
P3 = (6 * 5 * 4) / (45 * 44 * 43)  # 특정 세 번호가 함께 나올 확률
FREQ_SCALE = 39 / 44  # 비복원 추출(한 회차 6개 중복 없음) 보정: X² ~ (39/44)·χ²(44)
HYPER_VAR = 6 * P1 * (39 / 45) * (39 / 44)  # 맞힌 개수 ~ 초기하(45,6,6) 의 분산 = 0.6146


# ───────────────────────── 공통 도구 ─────────────────────────

def holm(p: np.ndarray) -> np.ndarray:
    """Holm 보정 p (FWER). 단조성 유지."""
    p = np.asarray(p, float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (m - rank) * p[i]))
        adj[i] = run
    return adj


def bh(p: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg 보정 q (FDR)."""
    return stats.false_discovery_control(np.asarray(p, float), method="bh")


def binom_two_sided(k: np.ndarray, n: np.ndarray, p: float) -> np.ndarray:
    """정확 이항 양측 p (작은 쪽 꼬리 × 2, 1 로 자름)."""
    k, n = np.asarray(k), np.asarray(n)
    lo = stats.binom.cdf(k, n, p)
    hi = stats.binom.sf(k - 1, n, p)
    return np.minimum(1.0, 2 * np.minimum(lo, hi))


def chi2_gof(obs: np.ndarray, exp: np.ndarray, min_exp: float = 5.0) -> tuple[float, int, float]:
    """기대도수 < min_exp 인 꼬리 칸을 이웃에 합친 뒤 적합도 카이제곱 → (X², df, p)."""
    obs, exp = list(map(float, obs)), list(map(float, exp))
    # pop 을 먼저 하고 남은 끝 칸에 더한다. (`exp[1] += exp.pop(0)` 은 exp[1] 을 먼저 읽고
    # 리스트가 밀린 뒤 엉뚱한 칸에 써서 기대도수가 사라진다 — tests/test_stats.py 가 고정)
    while len(exp) > 2 and exp[0] < min_exp:
        e0, o0 = exp.pop(0), obs.pop(0)
        exp[0] += e0
        obs[0] += o0
    while len(exp) > 2 and exp[-1] < min_exp:
        e1, o1 = exp.pop(), obs.pop()
        exp[-1] += e1
        obs[-1] += o1
    o, e = np.array(obs), np.array(exp)
    x2 = float(((o - e) ** 2 / e).sum())
    df = len(o) - 1
    return x2, df, float(stats.chi2.sf(x2, df))


def mc_p(observed: float, null: np.ndarray) -> float:
    """몬테카를로 p (상측): (1 + #{null ≥ obs}) / (1 + B)."""
    null = np.asarray(null)
    return float((1 + (null >= observed).sum()) / (1 + len(null)))


def _indicator(draws: np.ndarray) -> np.ndarray:
    """(n, 6) 번호(1..45) → (n, 45) 0/1."""
    X = np.zeros((len(draws), 45), dtype=np.float64)
    np.put_along_axis(X, draws.astype(int) - 1, 1.0, axis=1)
    return X


_TRIPLE_POS = [(i, j, k) for i in range(6) for j in range(i + 1, 6) for k in range(j + 1, 6)]


def _triple_lut() -> np.ndarray:
    lut = np.full((45, 45, 45), -1, dtype=np.int32)
    for idx, (a, b, c) in enumerate((a, b, c) for a in range(45) for b in range(a + 1, 45)
                                    for c in range(b + 1, 45)):
        lut[a, b, c] = idx
    return lut


_LUT3 = None


def triple_counts(draws: np.ndarray) -> np.ndarray:
    """14,190 삼중쌍 각각이 몇 번 함께 나왔나 (사전순 인덱스)."""
    global _LUT3
    if _LUT3 is None:
        _LUT3 = _triple_lut()
    d = np.sort(draws.astype(int) - 1, axis=1)
    ids = np.stack([_LUT3[d[:, i], d[:, j], d[:, k]] for i, j, k in _TRIPLE_POS], axis=1)
    return np.bincount(ids.ravel(), minlength=comb(45, 3))


def _gap_hist(X: np.ndarray, cap: int) -> np.ndarray:
    """번호별 연속 출현 간격(회) 히스토그램, 1..cap-1 과 cap 이상."""
    col, row = np.nonzero(X.T)
    same = col[1:] == col[:-1]
    gaps = (row[1:] - row[:-1])[same]
    return np.bincount(np.minimum(gaps, cap), minlength=cap + 1)[1:]


def _stats_of_history(X: np.ndarray, draws: np.ndarray, eras: list[slice], gap_cap: int) -> dict:
    """관측 역사와 가상 역사에 똑같이 적용하는 통계량 묶음."""
    n = len(X)
    c = X.sum(0)
    e = n * P1
    freq_x2 = float(((c - e) ** 2 / e).sum())
    P = X.T @ X
    iu = np.triu_indices(45, 1)
    pc = P[iu]
    e2 = n * P2
    prev = X[:-1].sum(0)
    M = X[:-1].T @ X[1:]
    em = prev[:, None] * P1
    lag_x2 = float(((M - em) ** 2 / em).sum())
    era_x2 = 0.0
    for s in eras:
        ce = X[s].sum(0)
        ee = len(X[s]) * P1
        era_x2 += float(((ce - ee) ** 2 / ee).sum())
    era_x2 -= freq_x2  # 동질성 = 시대별 X² 합 − 전체 X² (시대 간 차이만 남긴다)
    h = n // 2
    half_r = float(np.corrcoef(X[:h].sum(0), X[h:].sum(0))[0, 1])
    gh = _gap_hist(X, gap_cap)
    tc = triple_counts(draws)
    return {"freq_x2": freq_x2, "pair_disp": float(((pc - e2) ** 2 / e2).sum()),
            "pair_max": float(pc.max()), "pair_min": float(pc.min()), "lag_x2": lag_x2,
            "era_x2": era_x2, "half_r": half_r, "gap_hist": gh, "triple_max": float(tc.max())}


def _simulate_draws(rng: np.random.Generator, n: int) -> np.ndarray:
    u = rng.random((n, 45))
    return np.sort(np.argpartition(u, 6, axis=1)[:, :6] + 1, axis=1)


# ───────────────────────── 로또 6/45 ─────────────────────────

def lotto_tests(draws: np.ndarray, bonus: np.ndarray, rounds: np.ndarray, b_mc: int = 2000) -> dict:
    """draws: (n,6) 오름차순, bonus: (n,), rounds: (n,) 회차 번호."""
    n = len(draws)
    X = _indicator(draws)
    counts = X.sum(0)
    e1 = n * P1
    gap_cap = 30
    n_eras = 5
    edges = np.linspace(0, n, n_eras + 1).astype(int)
    eras = [slice(edges[i], edges[i + 1]) for i in range(n_eras)]

    obs = _stats_of_history(X, draws, eras, gap_cap)
    rng = np.random.default_rng(SEED)
    null = {k: [] for k in obs if k != "gap_hist"}
    null_gap = []
    for _ in range(b_mc):
        d = _simulate_draws(rng, n)
        s = _stats_of_history(_indicator(d), d, eras, gap_cap)
        for k in null:
            null[k].append(s[k])
        null_gap.append(s["gap_hist"])
    null = {k: np.array(v) for k, v in null.items()}

    # 1) 번호별 빈도
    lo95, hi95 = stats.binom.ppf([0.025, 0.975], n, P1)
    lob, hib = stats.binom.ppf([0.025 / 45, 1 - 0.025 / 45], n, P1)
    recent = X[-100:].sum(0)
    last_seen = np.array([np.flatnonzero(X[:, i]).max() for i in range(45)])
    cur_gap = (n - 1) - last_seen  # 최근 회차 이후 몇 회 연속 안 나왔나
    freq = {
        "counts": counts.astype(int).tolist(), "expected": e1,
        "band95": [int(lo95), int(hi95)], "band_bonferroni": [int(lob), int(hib)],
        "chi2": obs["freq_x2"], "df": 44,
        "p_analytic": float(stats.chi2.sf(obs["freq_x2"] / FREQ_SCALE, 44)),
        "p_mc": mc_p(obs["freq_x2"], null["freq_x2"]),
        "most": [int(i + 1) for i in np.argsort(-counts)[:6]],
        "least": [int(i + 1) for i in np.argsort(counts)[:6]],
        "recent100": recent.astype(int).tolist(), "recent100_expected": 100 * P1,
        "current_gap": cur_gap.astype(int).tolist(),
        "current_gap_tail_p": ((1 - P1) ** cur_gap).tolist(),
        "half_split_r": obs["half_r"], "half_split_p_mc": float(
            (1 + (np.abs(null["half_r"]) >= abs(obs["half_r"])).sum()) / (1 + b_mc)),
    }

    # 2) 보너스 번호
    bc = np.bincount(bonus.astype(int), minlength=46)[1:]
    eb = n / 45
    bx2 = float(((bc - eb) ** 2 / eb).sum())
    bonus_out = {"counts": bc.astype(int).tolist(), "expected": eb, "chi2": bx2, "df": 44,
                 "p": float(stats.chi2.sf(bx2, 44))}

    # 3) 번호 쌍 (궁합수)
    P = X.T @ X
    iu = np.triu_indices(45, 1)
    pc = P[iu]
    e2 = n * P2
    p_raw = binom_two_sided(pc, n, P2)
    p_holm, q_bh = holm(p_raw), bh(p_raw)
    sd2 = np.sqrt(n * P2 * (1 - P2))
    z = (P - e2) / sd2
    np.fill_diagonal(z, 0.0)
    order = np.argsort(-pc)

    def _pair_rows(idx):
        return [{"pair": [int(iu[0][k] + 1), int(iu[1][k] + 1)], "count": int(pc[k]),
                 "p": float(p_raw[k]), "p_holm": float(p_holm[k]), "q_bh": float(q_bh[k])}
                for k in idx]

    pairs = {
        "expected": e2, "n_pairs": int(len(pc)),
        "z_matrix": np.round(z, 2).tolist(),
        "top": _pair_rows(order[:12]), "bottom": _pair_rows(order[::-1][:12]),
        "n_raw_p05": int((p_raw < 0.05).sum()), "n_raw_p05_expected": 0.05 * len(pc),
        "n_sig_holm": int((p_holm < 0.05).sum()), "n_sig_bh": int((q_bh < 0.05).sum()),
        "dispersion": obs["pair_disp"], "p_mc_dispersion": mc_p(obs["pair_disp"], null["pair_disp"]),
        "max_count": int(pc.max()), "p_mc_max": mc_p(obs["pair_max"], null["pair_max"]),
        "min_count": int(pc.min()),
        "p_mc_min": float((1 + (null["pair_min"] <= obs["pair_min"]).sum()) / (1 + b_mc)),
        "null_max_median": float(np.median(null["pair_max"])),
    }

    # 4) 세 개 묶음
    tc = triple_counts(draws)
    top3 = np.argsort(-tc)[:8]
    trip_list = [(a, b, c) for a in range(45) for b in range(a + 1, 45) for c in range(b + 1, 45)]
    triples = {
        "expected": n * P3, "n_triples": int(len(tc)), "max_count": int(tc.max()),
        "p_mc_max": mc_p(obs["triple_max"], null["triple_max"]),
        "null_max_median": float(np.median(null["triple_max"])),
        "top": [{"triple": [trip_list[k][0] + 1, trip_list[k][1] + 1, trip_list[k][2] + 1],
                 "count": int(tc[k])} for k in top3],
    }

    # 5) 직전 회차 → 다음 회차
    carry = (X[1:] * X[:-1]).sum(1).astype(int)
    pmf = np.array([stats.hypergeom.pmf(k, 45, 6, 6) for k in range(7)])
    ch = np.bincount(carry, minlength=7)
    cx2, cdf_, cp = chi2_gof(ch, (n - 1) * pmf)
    # 이웃수: 직전 회차 번호 ±1 (직전 번호 자체 제외) 중 이번에 나온 개수
    nb_obs, nb_exp, nb_var = 0.0, 0.0, 0.0
    for t in range(1, n):
        prevset = set(draws[t - 1].tolist())
        nb = {x + d for x in prevset for d in (-1, 1)} - prevset
        nb = {x for x in nb if 1 <= x <= 45}
        k = len(nb)
        nb_obs += len(nb & set(draws[t].tolist()))
        nb_exp += 6 * k / 45
        nb_var += 6 * (k / 45) * (1 - k / 45) * (39 / 44)
    nb_z = (nb_obs - nb_exp) / np.sqrt(nb_var)
    M = X[:-1].T @ X[1:]
    prev_n = X[:-1].sum(0)
    lag_p = binom_two_sided(M, prev_n[:, None], P1)
    lag_q = bh(lag_p.ravel()).reshape(45, 45)
    lag_z = (M - prev_n[:, None] * P1) / np.sqrt(prev_n[:, None] * P1 * (1 - P1))
    flat = np.argsort(-lag_z.ravel())[:8]
    lag = {
        "carry_hist": ch.astype(int).tolist(), "carry_expected": ((n - 1) * pmf).tolist(),
        "carry_mean": float(carry.mean()), "carry_mean_expected": 0.8,
        "carry_chi2": cx2, "carry_df": cdf_, "carry_p": cp,
        "neighbor_obs": nb_obs, "neighbor_exp": nb_exp, "neighbor_z": float(nb_z),
        "neighbor_p": float(2 * stats.norm.sf(abs(nb_z))),
        "matrix_chi2": obs["lag_x2"], "matrix_p_mc": mc_p(obs["lag_x2"], null["lag_x2"]),
        "matrix_n_sig_bh": int((lag_q < 0.05).sum()), "matrix_cells": 45 * 45,
        "matrix_min_p": float(lag_p.min()),
        "top_follow": [{"prev": int(k // 45 + 1), "next": int(k % 45 + 1),
                        "count": int(M.ravel()[k]),
                        "expected": float(prev_n[k // 45] * P1),
                        "q_bh": float(lag_q.ravel()[k])} for k in flat],
    }

    # 6) 출현 간격 vs 기하분포
    gh = obs["gap_hist"]
    g = np.arange(1, gap_cap)
    pg = np.append((1 - P1) ** (g - 1) * P1, (1 - P1) ** (gap_cap - 1))
    eg = pg * gh.sum()
    gx2 = float(((gh - eg) ** 2 / eg).sum())
    null_gx2 = np.array([(((h - pg * h.sum()) ** 2) / (pg * h.sum())).sum() for h in null_gap])
    gaps = {"hist": gh.astype(int).tolist(), "expected": eg.tolist(), "cap": gap_cap,
            "chi2": gx2, "p_mc": mc_p(gx2, null_gx2),
            "mean_gap": float((gh * np.arange(1, gap_cap + 1)).sum() / gh.sum()),
            "mean_gap_expected_uncapped": 45 / 6,
            "max_current_gap": int(cur_gap.max()),
            "max_current_gap_number": int(np.argmax(cur_gap) + 1)}

    # 7) 조합 지표 vs 전수 분포
    feats = feature_tests(draws)

    # 8) 시대별 동질성
    era_counts = [X[s].sum(0).astype(int).tolist() for s in eras]
    era_out = {"edges_round": [int(rounds[s.start]) for s in eras] + [int(rounds[-1])],
               "counts": era_counts, "chi2": obs["era_x2"],
               "p_mc": mc_p(obs["era_x2"], null["era_x2"]),
               "top_by_era": [[int(i + 1) for i in np.argsort(-np.array(c))[:6]] for c in era_counts]}

    # 전체 요약용 p 목록 (질문 → p)
    summary = [
        ("특정 번호가 더 잘 나오나", freq["p_mc"]),
        ("보너스 번호가 치우쳤나", bonus_out["p"]),
        ("같이 잘 나오는 번호 쌍(궁합수)이 있나 — 990쌍 전체 분산", pairs["p_mc_dispersion"]),
        ("가장 자주 함께 나온 쌍이 우연 이상인가", pairs["p_mc_max"]),
        ("세 개 묶음 최다 출현이 우연 이상인가", triples["p_mc_max"]),
        ("지난주 번호가 이번 주에 다시 나오나 (이월수)", lag["carry_p"]),
        ("지난주 번호의 ±1 이 잘 나오나 (이웃수)", lag["neighbor_p"]),
        ("특정 번호 다음에 특정 번호가 나오나 (45×45)", lag["matrix_p_mc"]),
        ("오래 안 나온 번호가 '나올 때가 되나' (간격 분포)", gaps["p_mc"]),
        ("과거 빈도가 미래 빈도를 예고하나 (전·후반 상관)", freq["half_split_p_mc"]),
        ("시대(약 250회)마다 잘 나오는 번호가 다른가", era_out["p_mc"]),
    ] + [(f"{v['label']} 분포가 무작위 조합과 다른가", v["p"]) for v in feats.values()]
    ps = np.array([p for _, p in summary])
    summary_rows = [{"question": q, "p": float(p), "p_holm": float(ph)}
                    for (q, p), ph in zip(summary, holm(ps))]

    return {"n_draws": n, "b_mc": b_mc, "frequency": freq, "bonus": bonus_out, "pairs": pairs,
            "triples": triples, "lag": lag, "gaps": gaps, "features": feats, "eras": era_out,
            "summary": summary_rows}


def feature_tests(draws: np.ndarray) -> dict:
    """조합 지표(총합·홀짝·연번·AC값 …)의 관측 분포 vs 8,145,060 조합 전수 분포."""
    n = len(draws)
    exact = combos.exact_distributions()
    fobs = combos.features(draws)
    feats = {}
    for name, (label, desc) in combos.FEATURES.items():
        dist = exact[name]
        width = 10 if name == "sum" else 1  # 총합은 10 단위 구간으로 묶는다 (값 235종)
        vals = sorted({x // width * width for x in dist})
        at = {v: i for i, v in enumerate(vals)}
        e = np.zeros(len(vals))
        for x, q in dist.items():
            e[at[x // width * width]] += q * n
        o = np.bincount([at[int(x) // width * width] for x in fobs[name]],
                        minlength=len(vals)).astype(float)
        x2, df, p = chi2_gof(o, e)
        feats[name] = {"label": label, "desc": desc, "values": vals, "obs": o.astype(int).tolist(),
                       "exp": e.tolist(), "obs_mean": float(fobs[name].mean()),
                       "exp_mean": float(sum(v * q for v, q in dist.items())),
                       "chi2": x2, "df": df, "p": p}
    return feats


# ───────────────────────── 연금복권 720+ ─────────────────────────

def pension_tests(groups: np.ndarray, first: np.ndarray, bonus: np.ndarray, b_mc: int = 2000) -> dict:
    """groups: (n,) 1..5, first/bonus: (n,6) 자리별 숫자 0..9."""
    n = len(groups)
    gc = np.bincount(groups, minlength=6)[1:]
    gx2 = float(((gc - n / 5) ** 2 / (n / 5)).sum())
    pos = []
    for label, arr in (("1등", first), ("보너스", bonus)):
        for k in range(6):
            c = np.bincount(arr[:, k], minlength=10)
            x2 = float(((c - n / 10) ** 2 / (n / 10)).sum())
            pos.append({"which": label, "pos": k + 1, "counts": c.astype(int).tolist(),
                        "chi2": x2, "p": float(stats.chi2.sf(x2, 9))})
    ph = holm(np.array([r["p"] for r in pos]))
    for r, h in zip(pos, ph):
        r["p_holm"] = float(h)
    alld = np.concatenate([first.ravel(), bonus.ravel()])
    dc = np.bincount(alld, minlength=10)
    dx2 = float(((dc - len(alld) / 10) ** 2 / (len(alld) / 10)).sum())

    def _adj_x2(arr):  # 인접 자리 10×10 독립성 X² 합 (5쌍)
        tot = 0.0
        for k in range(5):
            t = np.zeros((10, 10))
            np.add.at(t, (arr[:, k], arr[:, k + 1]), 1)
            e = np.outer(t.sum(1), t.sum(0)) / t.sum()
            m = e > 0
            tot += float(((t - e)[m] ** 2 / e[m]).sum())
        return tot

    adj_obs = _adj_x2(first) + _adj_x2(bonus)
    rng = np.random.default_rng(SEED)
    adj_null = np.array([_adj_x2(rng.integers(0, 10, (n, 6))) + _adj_x2(rng.integers(0, 10, (n, 6)))
                         for _ in range(b_mc)])
    rep = int((first[1:] == first[:-1]).sum())
    rep_n = (n - 1) * 6
    grp_rep = int((groups[1:] == groups[:-1]).sum())
    match_fb = int((first == bonus).sum())
    # 6자리 합 분포 vs 정확 분포 (0..9 균등 6개의 합성곱)
    pmf = np.array([1.0])
    for _ in range(6):
        pmf = np.convolve(pmf, np.full(10, 0.1))
    sums = first.sum(1)
    so = np.bincount(sums, minlength=55)
    sx2, sdf, sp = chi2_gof(so, pmf * n)
    summary = [
        ("1등 조(1~5)가 치우쳤나", float(stats.chi2.sf(gx2, 4))),
        ("자리별 숫자가 치우쳤나 (12자리 중 최소 p, Holm)", float(min(r["p_holm"] for r in pos))),
        ("전체 숫자 0~9 빈도가 치우쳤나", float(stats.chi2.sf(dx2, 9))),
        ("옆자리 숫자끼리 관계가 있나", mc_p(adj_obs, adj_null)),
        ("지난주 같은 자리 숫자가 반복되나",
         float(binom_two_sided(np.array([rep]), np.array([rep_n]), 0.1)[0])),
        ("지난주 1등 조가 반복되나",
         float(binom_two_sided(np.array([grp_rep]), np.array([n - 1]), 0.2)[0])),
        ("1등 번호와 보너스 번호가 같은 자리에서 겹치나",
         float(binom_two_sided(np.array([match_fb]), np.array([n * 6]), 0.1)[0])),
        ("1등 6자리 합 분포가 무작위와 다른가", sp),
    ]
    ps = np.array([p for _, p in summary])
    return {
        "n_draws": n, "b_mc": b_mc,
        "group": {"counts": gc.astype(int).tolist(), "expected": n / 5, "chi2": gx2,
                  "p": float(stats.chi2.sf(gx2, 4))},
        "positions": pos,
        "digits": {"counts": dc.astype(int).tolist(), "expected": len(alld) / 10, "chi2": dx2,
                   "p": float(stats.chi2.sf(dx2, 9))},
        "adjacent": {"chi2": adj_obs, "p_mc": mc_p(adj_obs, adj_null)},
        "repeat": {"same_pos_repeat": rep, "trials": rep_n, "expected": rep_n * 0.1,
                   "group_repeat": grp_rep, "group_expected": (n - 1) * 0.2,
                   "first_bonus_match": match_fb, "first_bonus_expected": n * 6 * 0.1},
        "digit_sum": {"obs": so.astype(int).tolist(), "exp": (pmf * n).tolist(),
                      "chi2": sx2, "df": sdf, "p": sp},
        "summary": [{"question": q, "p": float(p), "p_holm": float(h)}
                    for (q, p), h in zip(summary, holm(ps))],
    }
