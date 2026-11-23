#!/usr/bin/env python3
"""모든 분석을 돌려 results/analysis.json (웹앱이 읽는 정본) 과 RESULTS.md (사람용 요약) 를 만든다.

    python lottery/build_results.py            # 전체 — 약 6~8분
    python lottery/build_results.py --quick    # 점검용 — 몬테카를로·학습을 줄인다 (이 결과는 인용 금지)

입력은 data/raw/ (fetch_data.py 가 받은 원본) 뿐이다. 결과에는 원본 sha256 과 받은 시각을
같이 적는다 — 숫자를 인용할 때는 그 스냅샷 기준이라는 뜻이다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import time
import warnings

import numpy as np
from scipy import optimize, stats

import combos
import dataset
import generative
import ml_backtest
import popularity
import stats_tests

RESULTS_DIR = dataset.ROOT / "results"
RESULTS_MD = dataset.ROOT / "RESULTS.md"

COURSE_MAP = [  # 분석 ↔ 강의 (사이트 카드에 표시)
    ("번호별 출현 빈도", "확률과통계", "5주 이항분포 · 14주 카이제곱 적합도"),
    ("궁합수 (번호 쌍)", "확률과통계", "4주 이변량 확률변수·공분산 · 14주 다중비교(Bonferroni/Holm)"),
    ("이월수 (지난주 번호 재출현)", "확률과통계", "5주 초기하분포"),
    ("미출현 간격", "확률과통계", "5주 기하분포 (연속형 대응: 지수분포)"),
    ("총합 분포", "확률과통계", "5·6주 중심극한정리"),
    ("1등 당첨자 수", "확률과통계", "5주 포아송분포"),
    ("시대별 동질성", "확률과통계", "13주 실험계획법(요인=시대) · 14주 카이제곱"),
    ("검출력 (얼마나 작은 편향까지 잡나)", "확률과통계", "10주 제2종 오류 · 검정력"),
    ("예측 모델 성능 구간", "확률과통계", "9주 구간추정"),
    ("번호 선택 인기도", "확률과통계", "11·12주 (다중)회귀분석"),
    ("예측 모델", "머신러닝", "7 로지스틱 회귀 · 7 SVM(소프트 마진, 커널 트릭) · 4-1 신경망 · 12 나이브 베이즈"),
    ("인기도 비선형 모델", "머신러닝", "7 SVM — 커널 트릭을 회귀(SVR)에 적용"),
    ("숨은 유형(군집)", "머신러닝", "13 EM — 베르누이 혼합"),
    ("번호 생성 AI", "머신러닝", "15 확산 모델(DDPM)"),
]


def _clean(o):
    """numpy → JSON. 실수는 유효숫자 6자리로 줄여 파일 크기를 줄인다."""
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        x = float(o)
        return None if not np.isfinite(x) else float(f"{x:.6g}")
    return o


# 분석 숫자를 정하는 파일 — 결과 파일에 이 파일들의 지문과 라이브러리 판본을 남긴다 (자체 리뷰: 전에는 어떤 코드로
# 만들었는지 기록이 없었고, 실행마다 다른 실행 시간이 정본 안에 있었다 — 실행 시간은 화면 출력에만 남긴다).
ANALYSIS_FILES = ("build_results.py", "combos.py", "dataset.py", "generative.py", "ml_backtest.py",
                  "popularity.py", "stats_tests.py", "requirements.txt")


def source_digest() -> str:
    h = hashlib.sha256()
    for name in ANALYSIS_FILES:
        h.update(name.encode() + b"\0" + hashlib.sha256((dataset.ROOT / name).read_bytes()).digest())
    return h.hexdigest()


def code_identity() -> dict:
    import platform
    import scipy
    import sklearn
    import statsmodels
    return {"source_sha256": source_digest(), "files": list(ANALYSIS_FILES),
            "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                         "sklearn": sklearn.__version__, "statsmodels": statsmodels.__version__}}


def power_summary(n_lotto: int, n_questions: int) -> dict:
    """10주 '검정력': 이 회차 수로 번호 하나의 편향을 80% 확률로 잡으려면 몇 % 여야 하나.

    single_number_rel_bias — 화면의 판정 그대로: 빈도 X²/(39/44) ~ χ²(44) 의 p 가 Holm 첫 단계 α/질문 수
      아래. 번호 하나가 (1+δ) 배 나오면 비중심도 λ = n · p1 · δ² · 45/39 (tests/test_numbers.py 가 편향을
      심은 시뮬레이션으로 80% 를 확인한다). 전에는 아래 띠 기준만 내서 판정보다 훨씬 작은 편향을 잡는 것처럼
      보였다 (자체 리뷰 G1: 29.6% 를 심으면 판정은 16% 만 잡는다).
    single_number_rel_bias_band — 빈도 차트의 띠: 번호 하나가 45개 동시 보정(Bonferroni) 범위를 벗어남.
    pair_rel_bias — 쌍 하나가 990쌍 동시 보정 범위를 벗어남 (화면의 '보정 후 유의한 쌍' 기준).
    """
    zb = stats.norm.isf(0.2)
    p1, p2 = 6 / 45, 1 / 66
    za1, za2 = stats.norm.isf(0.025 / 45), stats.norm.isf(0.025 / 990)
    band1 = (za1 + zb) * np.sqrt(n_lotto * p1 * (1 - p1)) / (n_lotto * p1)
    rel2 = (za2 + zb) * np.sqrt(n_lotto * p2 * (1 - p2)) / (n_lotto * p2)
    band_need5 = ((za1 + zb) / 0.05) ** 2 * (1 - p1) / p1
    crit = stats.chi2.isf(dataset.ALPHA / n_questions, 44)
    lam = optimize.brentq(lambda x: stats.ncx2.sf(crit, 44, x) - 0.8, 1e-6, 1e4)
    k = p1 * 45 / 39  # λ = n · k · δ²
    need5 = lam / (k * 0.05 ** 2)
    return {"single_number_rel_bias": float(np.sqrt(lam / (n_lotto * k))),
            "draws_needed_for_5pct": float(need5), "years_needed_for_5pct": float(need5 / 52.18),
            "n_questions": n_questions, "alpha": dataset.ALPHA,
            "single_number_rel_bias_band": float(band1), "band_years_needed_for_5pct": float(band_need5 / 52.18),
            "pair_rel_bias": float(rel2)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    warnings.filterwarnings("ignore")  # sklearn 수렴 경고 — DDPM 은 loss 곡선으로 따로 본다
    B = 200 if args.quick else 2000
    E = 15 if args.quick else 80
    t_all = time.time()
    tm: dict[str, float] = {}

    def step(name, f):
        t = time.time()
        out = f()
        tm[name] = round(time.time() - t, 1)
        print(f"  {name}: {tm[name]}s", flush=True)
        return out

    L, P = dataset.load_lotto(), dataset.load_pension()
    manifest = json.loads((dataset.RAW_DIR / "MANIFEST.json").read_text(encoding="utf-8"))
    draws = np.array([d.numbers for d in L])
    bonus = np.array([d.bonus for d in L])
    rounds = np.array([d.round for d in L])
    winners = np.array([d.winners for d in L], float)
    games = np.array([d.games for d in L])
    prizes = np.array([d.prize for d in L])
    price = np.array([d.price for d in L])
    grp = np.array([d.group for d in P])
    first = np.array([[int(c) for c in d.number] for d in P])
    pbon = np.array([[int(c) for c in d.bonus] for d in P])
    rng = np.random.default_rng(stats_tests.SEED + 7)
    syn = np.sort(np.argpartition(rng.random((len(L), 45)), 6, axis=1)[:, :6] + 1, axis=1)
    syn_b = np.array([rng.choice(sorted(set(range(1, 46)) - set(d.tolist()))) for d in syn])
    syn_p = rng.integers(0, 10, first.shape)

    print("분석 실행", "(quick — 인용 금지)" if args.quick else "", flush=True)
    lotto_stats = step("로또 검정", lambda: stats_tests.lotto_tests(draws, bonus, rounds, b_mc=B))
    pension_stats = step("연금 검정", lambda: stats_tests.pension_tests(grp, first, pbon, b_mc=B))
    pop = step("인기도 모델", lambda: popularity.fit(L))
    recovery = step("인기도 양성대조", lambda: popularity.recovery_check(L, n_draws=60 if args.quick else 200))
    svr = step("SVR 비교", lambda: popularity.svr_comparison(L))
    ml_real = step("로또 ML (실제)", lambda: ml_backtest.lotto_backtest(
        draws, bonus, winners, games, prizes, price, label="실제 당첨번호"))
    ml_null = step("로또 ML (가상 무작위)", lambda: ml_backtest.lotto_backtest(
        syn, syn_b, winners, games, prizes, price, label="가상 무작위 역사"))
    pen_ml = step("연금 ML (실제)", lambda: ml_backtest.pension_backtest(first, label="실제 당첨번호"))
    pen_ml_null = step("연금 ML (가상 무작위)", lambda: ml_backtest.pension_backtest(
        syn_p, label="가상 무작위 역사"))
    ddpm = step("확산 모델 평가", lambda: generative.evaluate_ddpm(draws, epochs=E))
    pool = step("확산 모델 번호 풀", lambda: generative.train_generator_pool(draws, epochs=E))
    em = step("EM 군집 검정", lambda: generative.em_cluster_test(draws, b_null=10 if args.quick else 30))
    backtest = step("백테스트 분포 (814만 조합 전수)", lambda: combos.backtest_distribution(L))

    # 확산 모델 번호의 인기도 vs 균등 무작위 번호 (1등 시 기대 몫)
    gen = ddpm.pop("generated")
    uni = np.sort(np.argpartition(rng.random((len(gen), 45)), 6, axis=1)[:, :6] + 1, axis=1)
    _, sh_gen = popularity.score_combos(gen, pop["score"])
    _, sh_uni = popularity.score_combos(uni, pop["score"])
    ddpm["share_vs_uniform"] = {"generated_mean_share": float(sh_gen.mean()),
                                "uniform_mean_share": float(sh_uni.mean()),
                                "ratio": float(sh_gen.mean() / sh_uni.mean())}

    data = {
        "meta": {
            "built_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
            "quick": args.quick, "code": code_identity(),
            "source": manifest, "b_mc": B, "ddpm_epochs": E,
            "lotto_range": [L[0].round, L[-1].round, L[0].date.isoformat(), L[-1].date.isoformat()],
            "pension_range": [P[0].round, P[-1].round, P[0].date.isoformat(), P[-1].date.isoformat()],
            "total_games": float(games.sum()), "total_sales": int(sum(d.sales for d in L)),
            "total_winners": winners.sum(0).astype(int).tolist(),
        },
        "course_map": [{"analysis": a, "course": c, "where": w} for a, c, w in COURSE_MAP],
        "lotto": {
            "draws": [[d.round, d.date.isoformat(), *d.numbers, d.bonus, *d.winners, d.prize[0],
                       int(round(d.games)), d.first_auto, d.first_manual, d.first_semi] for d in L],
            "draw_columns": ["round", "date", "n1", "n2", "n3", "n4", "n5", "n6", "bonus",
                             "w1", "w2", "w3", "w4", "w5", "prize1", "games", "auto", "manual", "semi"],
            "stats": lotto_stats, "power": power_summary(len(L), len(lotto_stats["summary"])),
            "exact": {k: {str(v): p for v, p in d.items()} for k, d in combos.exact_distributions().items()},
            "ml": {"real": ml_real, "null": ml_null},
            "popularity": pop, "popularity_recovery": recovery, "svr": svr,
            "ddpm": ddpm, "ddpm_pool": pool, "em": em, "backtest": backtest,
        },
        "pension": {
            "draws": [[d.round, d.date.isoformat(), d.group, d.number, d.bonus] for d in P],
            "stats": pension_stats, "ml": {"real": pen_ml, "null": pen_ml_null},
        },
    }
    data = _clean(data)
    RESULTS_DIR.mkdir(exist_ok=True)
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
    (RESULTS_DIR / "analysis.json").write_text(js, encoding="utf-8")  # webapp/content.py 가 읽는다
    write_results_md(data)
    print(f"results/analysis.json {len(js.encode()) / 1024:.0f} KB · RESULTS.md · 총 {time.time() - t_all:.0f}s")
    return 0


def write_results_md(d: dict) -> None:
    m, lo, pe = d["meta"], d["lotto"], d["pension"]
    src = m["source"]["files"]
    pop, ml = lo["popularity"], lo["ml"]
    best = max(ml["real"]["rows"], key=lambda r: r["mean_hits"])
    # 판정 줄은 보정 p 에서 나온다 — 고정 해석은 결과가 바뀌어도 남는다 (자체 리뷰 K1)
    sig_lo = [r["question"] for r in lo["stats"]["summary"] if r["p_holm"] < dataset.ALPHA]
    sig_pe = [f"(연금) {r['question']}" for r in pe["stats"]["summary"] if r["p_holm"] < dataset.ALPHA]
    sig_ml = [r["model"] for r in ml["real"]["rows"] if r["p_bonferroni"] < dataset.ALPHA]
    sc = pop["score"]
    lines = [
        "# 로또·연금복권 분석 결과 (자동 생성 — `build_results.py`)",
        "",
        f"- 데이터: 로또 6/45 {lo['draws'][0][0]}~{lo['draws'][-1][0]}회, 연금복권720+ "
        f"{pe['draws'][0][0]}~{pe['draws'][-1][0]}회 — 동행복권 공식, 받은 시각 "
        f"{m['source']['fetched_at_utc']}",
        f"- 원본 sha256: lotto645.json `{src['lotto645.json']['sha256'][:16]}…`, "
        f"pension720.json `{src['pension720.json']['sha256'][:16]}…`",
        f"- 생성 {m['built_at_utc']} · 몬테카를로 {m['b_mc']}회 · 확산 모델 {m['ddpm_epochs']} epoch"
        + (" · **quick 모드 — 인용 금지**" if m["quick"] else ""),
        "",
        "## 1. 추첨기는 무작위인가",
        "",
        "| 질문 | p | Holm 보정 p |",
        "|---|---|---|",
        *[f"| {r['question']} | {r['p']:.3f} | {r['p_holm']:.3f} |" for r in lo["stats"]["summary"]],
        *[f"| (연금) {r['question']} | {r['p']:.3f} | {r['p_holm']:.3f} |" for r in pe["stats"]["summary"]],
        "",
        f"- 판정: Holm 보정 p < {dataset.ALPHA} 인 질문 — 로또 {len(sig_lo)}개, 연금 {len(sig_pe)}개"
        + (" (" + " · ".join(sig_lo + sig_pe) + ")" if sig_lo + sig_pe else ""),
        f"- 궁합수: 990쌍 중 보정 전 p<0.05 {lo['stats']['pairs']['n_raw_p05']}쌍 (우연 기대 "
        f"{lo['stats']['pairs']['n_raw_p05_expected']:.1f}), Holm 유의 {lo['stats']['pairs']['n_sig_holm']}쌍",
        f"- 검출력 (이 판정 — 빈도 X² + 로또 질문 {lo['power']['n_questions']}개 Holm): 번호 하나가 "
        f"{lo['power']['single_number_rel_bias'] * 100:.0f}% 더 잘 나와야 80% 확률로 잡힌다 (빈도 차트의 띠 — 45개 "
        f"동시 보정 — 를 벗어나는 데는 {lo['power']['single_number_rel_bias_band'] * 100:.0f}%). 5% 편향을 이 판정으로 "
        f"잡으려면 약 {lo['power']['years_needed_for_5pct']:,.0f}년치 추첨이 필요하다. 쌍 하나는 990쌍 동시 보정 기준 "
        f"{lo['power']['pair_rel_bias'] * 100:.0f}%.",
        "",
        "## 2. 머신러닝으로 다음 번호를 맞힐 수 있나 (walk-forward)",
        "",
        f"검증 {ml['real']['test_rounds'][0]}~{ml['real']['test_rounds'][1]}회 ({ml['real']['n_test']}회차), "
        "무작위 기대 적중 0.8개.",
        "",
        "| 모델 | 평균 적중 (실제) | z | Bonferroni p | 평균 적중 (가상 무작위 역사) | 회수율 |",
        "|---|---|---|---|---|---|",
        *[f"| {r['model']} | {r['mean_hits']:.3f} | {r['z']:+.2f} | {r['p_bonferroni']:.2f} | "
          f"{n['mean_hits']:.3f} | {r['won'] / r['spent'] * 100:.0f}% |"
          for r, n in zip(ml["real"]["rows"], ml["null"]["rows"])],
        "",
        f"- 판정: Bonferroni p < {dataset.ALPHA} 인 전략 {len(sig_ml)}개" + (" (" + " · ".join(sig_ml) + ")" if sig_ml else ""),
        f"- 가장 높아 보인 모델: {best['model']} {best['mean_hits']:.3f}개 (보정 전 p={best['p_better']:.3f}, "
        f"보정 후 {best['p_bonferroni']:.2f})"
        + (" — 보정 후에도 유의한 전략이 있다. 다른 기간에서 재현되기 전에는 예측력으로 보지 않는다." if sig_ml
           else " — 여러 모델 중 최고를 고르면 생기는 선택 편향 범위."),
        "",
        "## 3. 사람들은 어떤 번호를 고르나 (등수별 당첨자 수)",
        "",
        *[f"- {k}등 log(실측/기대): 학습 R² {v['r2_in']:.3f}, 시간 블록 교차검증 R² {v['r2_oof']:.3f}, "
          f"전·후반 번호효과 상관 {v['era_beta_r']:.3f}" for k, v in pop["tiers"].items()],
        f"- 번호효과 Wald χ²={pop['number_effect']['wald_chi2']:.0f} (44 df)",
        f"- 1등 당첨자 수 ← 인기도 점수: γ1={pop['first_prize_model']['gamma1']:.2f} ± "
        f"{pop['first_prize_model']['gamma1_se']:.2f} (p={pop['first_prize_model']['gamma1_p']:.1e})",
        f"- 1등 중 수동 비율 ← 인기도 점수: δ1={pop['manual_model']['delta1']:.2f} ± "
        f"{pop['manual_model']['delta1_se']:.2f} (p={pop['manual_model']['delta1_p']:.1e}) — "
        "자동(기계 무작위)이 대조군",
        f"- 양성 대조(선호를 아는 가상 구매자) 복원 상관 {lo['popularity_recovery']['corr']:.4f}",
        f"- SVR(커널) vs 선형: " + ", ".join(f"{k} {v:.3f}" for k, v in lo["svr"]["r2_oof"].items()),
        "- 생성기 효과 (1등 시 기대 수령액, 자동·무작위 구매 대비 — make.js 규칙 그대로 814만 조합 전수의 구간 평균): "
        + " · ".join(f"하위 {q}% {sc['bucket_gain'][str(q)]:.3f}배" for q in (30, 20, 10, 1))
        + " (당첨 확률은 모든 조합이 같다)",
        "",
        "## 4. 생성 모델",
        "",
        f"- 확산 모델(DDPM): 학습 당첨번호 완전 복제 {lo['ddpm']['memorization']['exact_copy_rate'] * 100:.2f}%, "
        f"번호 사용 편중 (학습 빈도와 상관 {lo['ddpm']['corr_with_train_freq']:+.2f}), "
        f"1001회~ 평균 적중 {lo['ddpm']['hits_one_per_draw']['mean']:.3f}개 (z={lo['ddpm']['hits_one_per_draw']['z']:+.2f}), "
        f"1등 시 기대 몫 균등 무작위 대비 {lo['ddpm']['share_vs_uniform']['ratio']:.3f}배",
        f"- EM 베르누이 혼합: BIC 최적 K={lo['em']['best_k_bic']}, K=2 로그우도 증가의 몬테카를로 p={lo['em']['p_mc']:.2f}",
        "",
    ]
    RESULTS_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
