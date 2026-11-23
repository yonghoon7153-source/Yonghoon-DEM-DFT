"""공개 숫자가 그 숫자가 말하는 것과 같은가 — 자체 리뷰 1차 I1 · G1 · J1·J2 (docs/SELF_REVIEW_R1.md).

각 숫자를 독립 계산(무작위 역사 시뮬레이션 · 814만 조합 전수 열거)과 대조한다:
  I1 궁합수 '보정 전 p<0.05 쌍의 우연 기대' 49.5 — 이산 이항검정의 실제 크기는 5% 보다 작다 (기대 약 36).
  G1 검출력 '번호 하나가 30% 더 나와야 80% 로 잡힌다' — 빈도 차트 띠(45개 동시 보정) 기준이었다. 이 화면의
     판정(빈도 X² + 로또 질문 19개 Holm 보정)으로는 48~50% 가 필요하다.
  J  홈 '+14%' — 백분위 격자의 평균(근사)이고 기준이 '인기도 0 인 조합' 이었다. 생성기 규칙 그대로 전 조합을
     열거한 평균은 하위 20% 1.131배(그 기준) / 자동(무작위) 대비 약 1.12배. RESULTS 의 하위 10%·1% 배수는
     구간 평균이 아니라 경계값이었다.
"""
import json
import sys

import numpy as np
from scipy import stats

import build_results
import combos
import dataset
import popularity
import stats_tests

sys.path.insert(0, str(dataset.ROOT / "webapp"))
import content as C  # noqa: E402

REAL = json.loads((dataset.ROOT / "results" / "analysis.json").read_text(encoding="utf-8"))
L = dataset.load_lotto()
N = len(L)


def _random_draws(rng, rows: int) -> tuple[np.ndarray, np.ndarray]:
    """균등 무작위 회차들 — (번호 위치 rows×6, 0/1 행렬 rows×45)."""
    idx = np.argpartition(rng.random((rows, 45)), 6, axis=1)[:, :6]
    X = np.zeros((rows, 45), bool)
    np.put_along_axis(X, idx, True, axis=1)
    return idx, X


def test_pair_chance_expectation_matches_random_histories():
    """I1: 진짜 무작위 역사 300개에서 '보정 전 p<0.05 쌍' 개수의 평균 = 화면의 '우연 기대'."""
    expected = stats_tests.pair_null_rejections(N, 990)
    rng = np.random.default_rng(13)
    iu = np.triu_indices(45, 1)
    counts = []
    for _ in range(300):
        X = _random_draws(rng, N)[1].astype(float)
        pc = (X.T @ X)[iu]
        counts.append(int((stats_tests.binom_two_sided(pc, N, stats_tests.P2) < 0.05).sum()))
    m, se = np.mean(counts), np.std(counts) / np.sqrt(len(counts))
    assert abs(m - expected) < 4 * se + 0.3, (m, se, expected)


def test_reported_detectable_bias_is_detected_80pct_by_the_verdict_rule():
    """G1: 화면이 '80% 확률로 잡힌다'고 한 편향을 실제로 심으면, 이 화면의 판정 방식으로 80% 잡히는가.

    번호 1 의 회차당 출현 확률을 (6/45)(1+δ) 로 올린다 (1 이 없는 회차에서 확률 q 로 6개 중 하나를 1 로
    바꾼다 → 나머지 44개는 고르게 줄어든다). 판정: 빈도 X²/(39/44) ~ χ²(44) 의 p 가 Holm 첫 단계 α/19 아래.
    """
    m = len(REAL["lotto"]["stats"]["summary"])
    pw = build_results.power_summary(N, n_questions=m)
    delta = pw["single_number_rel_bias"]
    rng = np.random.default_rng(12)
    q = stats_tests.P1 * delta / (1 - stats_tests.P1)
    hits, reps = 0, 0
    for _ in range(6):
        idx, X = _random_draws(rng, 100 * N)
        rows = np.nonzero(~X[:, 0] & (rng.random(len(X)) < q))[0]
        X[rows, idx[rows, rng.integers(0, 6, len(rows))]] = False
        X[rows, 0] = True
        c = X.reshape(100, N, 45).sum(1)
        x2 = ((c - N * stats_tests.P1) ** 2 / (N * stats_tests.P1)).sum(1)
        hits += int((stats.chi2.sf(x2 / stats_tests.FREQ_SCALE, 44) < dataset.ALPHA / m).sum())
        reps += 100
    assert 0.74 < hits / reps < 0.86, (delta, hits / reps)


def _generator_bucket_gains(S: dict) -> dict[int, float]:
    """make.js '비인기 조합' 규칙 그대로 전 조합 열거: 과거 당첨 조합 · 같은 간격 수열 · 4개 이상 연속은 빼고,
    인기 백분위 ≤ q 안에서 균등하게 고른다. 값 = 그 평균 1등 몫 / 전 조합 평균 몫 (= 자동·무작위 대비)."""
    A = combos.all_combos()
    eta, share = popularity.score_combos(A, S)
    pct = np.interp(eta, S["eta_percentiles"], S["pct"])
    d = np.diff(A.astype(np.int16), axis=1)
    one = d == 1
    bad = (d == d[:, :1]).all(1) | (one[:, :-2] & one[:, 1:-1] & one[:, 2:]).any(1)
    bad[[combos.rank_of(x.numbers) for x in L]] = True
    auto = share.mean()
    return {q: float(share[(pct <= q) & ~bad].mean() / auto) for q in (1, 10, 20, 30)}


def test_generator_gain_is_the_bucket_mean_over_all_combos(tmp_path, monkeypatch):
    """J1·J2: 홈 타일과 RESULTS.md 의 '생성기 효과' 가 생성기 규칙 그대로 열거한 구간 평균(자동 대비)인가."""
    gain = _generator_bucket_gains(REAL["lotto"]["popularity"]["score"])
    monkeypatch.setattr(C, "_cache", {"mtime": None, "data": None, "view": None})
    assert abs(C.view()["facts"]["gain20"] - (gain[20] - 1)) < 0.002, (C.view()["facts"]["gain20"], gain)
    out = tmp_path / "RESULTS.md"
    monkeypatch.setattr(build_results, "RESULTS_MD", out)
    build_results.write_results_md(REAL)
    text = out.read_text(encoding="utf-8")
    for q in (1, 10, 20, 30):
        assert f"하위 {q}% {gain[q]:.3f}배" in text, (q, gain[q])


def test_published_rankings_break_ties_by_number():
    """N1: 같은 값의 순위가 CPU 의 SIMD 정렬에 따라 바뀌었다 (궁합수 상위 11~12위 등). 안정 정렬 → 동점은 번호 순."""
    st = REAL["lotto"]["stats"]
    for name, rows, key, item in (("pairs.top", st["pairs"]["top"], "count", "pair"),
                                  ("pairs.bottom", st["pairs"]["bottom"], "count", "pair")):
        for a, b in zip(rows, rows[1:]):
            if a[key] == b[key]:
                assert a[item] < b[item], (name, a, b)
    fq = st["frequency"]
    for name, nums, sign in (("most", fq["most"], -1), ("least", fq["least"], 1)):
        for a, b in zip(nums, nums[1:]):
            if fq["counts"][a - 1] == fq["counts"][b - 1]:
                assert a < b, (name, a, b)


def test_results_record_code_and_library_versions_not_timings():
    """소: 결과 파일에 어떤 코드·라이브러리로 만들었는지가 없었고, 실행마다 다른 실행 시간이 정본 안에 있었다."""
    meta = REAL["meta"]
    assert "timings" not in meta and "seconds" not in meta
    code = meta["code"]
    assert len(code["source_sha256"]) == 64 and code["source_sha256"] == build_results.source_digest()
    for lib in ("python", "numpy", "scipy", "sklearn", "statsmodels"):
        assert code["versions"][lib], lib
