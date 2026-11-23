"""웹앱 생성기(make.js)의 인기도 계산이 분석 코드(popularity.score_combos)와 같은 값을 내는가.

make.js 의 `// <core>` 구간만 잘라 node 로 돌린다. 화면에 뜨는 '인기 하위 n%'·'1등 시 기대 금액'이
분석과 다르면 생성기가 엉뚱한 조합을 고른다 — 그래서 두 구현을 직접 대조한다.
"""
import json
import re
import shutil
import subprocess

import numpy as np
import pytest

import dataset
import popularity

MAKE_JS = dataset.ROOT / "webapp" / "static" / "js" / "make.js"
S = json.loads((dataset.ROOT / "results" / "analysis.json").read_text(encoding="utf-8"))["lotto"]["popularity"]["score"]


@pytest.mark.skipif(shutil.which("node") is None, reason="node 없음")
def test_js_core_matches_python():
    core = re.search(r"// <core>\n(.*?)// </core>", MAKE_JS.read_text(encoding="utf-8"), re.S).group(1)
    rng = np.random.default_rng(9)
    combos = np.sort(np.argpartition(rng.random((300, 45)), 6, axis=1)[:, :6] + 1, axis=1).tolist()
    combos += [[1, 2, 3, 4, 5, 6], [7, 14, 21, 28, 35, 42], list(S["latest_numbers"])]
    prog = core + f"""
const S = {json.dumps(S)};
const C = {json.dumps(combos)};
console.log(JSON.stringify(C.map(c => {{ const p = popularity(c, S); const sh = comboShape(c);
  return [p.eta, p.share, p.pct, sh.arithmetic, sh.maxRun]; }})));
"""
    out = _node(prog)
    eta, share = popularity.score_combos(np.array(combos), S)
    pct = np.interp(eta, S["eta_percentiles"], S["pct"])
    js = np.array([o[:3] for o in out])
    assert np.allclose(js[:, 0], eta, atol=1e-12) and np.allclose(js[:, 1], share, atol=1e-12)
    assert np.allclose(js[:, 2], pct, atol=1e-9)
    assert out[-3][3] is True and out[-3][4] == 6        # 1..6: 같은 간격, 6개 연속
    assert out[-2][3] is True and out[-2][4] == 1        # 7·14·…·42: 같은 간격


def _node(prog: str):
    """프로그램을 표준입력으로 넘긴다 — `node -e` 인자는 128 KiB 한도라 전 회차 데이터가 자라면 깨진다 (자체 리뷰 소)."""
    return json.loads(subprocess.run(["node"], input=prog, capture_output=True, text=True, check=True).stdout)


def _core() -> str:
    return re.search(r"// <core>\n(.*?)// </core>", MAKE_JS.read_text(encoding="utf-8"), re.S).group(1)


@pytest.mark.skipif(shutil.which("node") is None, reason="node 없음")
def test_after_tax_follows_withholding_rates():
    cases = [1_500_000, 2_000_000, 2_000_001, 50_000_000, 300_000_000, 300_001_000, 2_000_000_000]
    got = _node(_core() + f"console.log(JSON.stringify({cases}.map(v => afterTax(v).tax)));")
    assert got == [0, 0, 439_780, 10_999_780, 65_999_780, 66_000_000, 626_999_670]


# ── 백테스트 ('1회부터 매주 샀다면') — 자체 리뷰 1차 H1.
# 이 대조의 옛 파이썬 기준은 make.js 와 같은 규칙(1~3등도 공개 1인당 금액 그대로)을 베껴 썼다 — 기준이 진실을
# 가렸다. 1~3등은 당첨자끼리 나누므로, 그 회차에 내가 샀다면 나는 한 명 더 → 1인당 × w/(w+1) 이다 (리뷰: 1등
# +24% 과대). 그 등수 당첨자가 없던 회차(1등 이월 14회, 2등 2회)는 내가 받았을 금액이 기록에 없다.

def ref_backtest(L, c):
    """옳은 규칙의 파이썬 기준: (등수별 횟수, 받은 돈, 쓴 돈, 금액 미상 당첨 수)."""
    counts, won, spent, unknown = [0] * 5, 0.0, 0, 0
    for d in L:
        m, b = len(set(d.numbers) & set(c)), d.bonus in c
        tier = {6: 1, 5: 2 if b else 3, 4: 4, 3: 5}.get(m, 0)
        if tier:
            counts[tier - 1] += 1
            w = d.winners[tier - 1]
            if tier > 3:
                won += d.prize[tier - 1]          # 4·5등은 정액
            elif w == 0:
                unknown += 1                      # 당첨자가 없던 회차 — 금액 미상
            else:
                won += d.prize[tier - 1] * w / (w + 1)
        spent += d.price
    return counts, won, spent, unknown


def payload_rounds(L):
    return [[d.round, *d.numbers, d.bonus, *d.prize, d.price, *d.winners[:3]] for d in L]


@pytest.mark.skipif(shutil.which("node") is None, reason="node 없음")
def test_backtest_matches_python_reference():
    L = dataset.load_lotto()
    combos = [list(L[0].numbers), list(L[-1].numbers), [1, 2, 3, 4, 5, 6], [7, 11, 19, 27, 33, 42]]
    got = _node(_core() + f"const R = {json.dumps(payload_rounds(L))};"
                f"console.log(JSON.stringify({json.dumps(combos)}.map(c => simulate(c, R))));")
    for c, g in zip(combos, got):
        counts, won, spent, unknown = ref_backtest(L, c)
        assert g["counts"] == counts and g["spent"] == spent and g["unknown"] == unknown, c
        assert abs(g["won"] - won) < 1e-6 * max(won, 1), (c, g["won"], won)
    assert got[0]["counts"][0] >= 1 and got[0]["unknown"] >= 1   # 1회 번호: 1회는 1등이 없어 이월된 회차
    last = L[-1]
    w1 = last.winners[0]
    assert w1 >= 1 and got[1]["counts"][0] >= 1
    # 최신 회차 번호 그대로: 그 회차 1등을 w1 명과 나눈다 → 1인당 금액의 w1/(w1+1) (공개 금액 그대로가 아니다)
    assert got[1]["won"] < ref_backtest(L, list(last.numbers))[1] + 1 and \
        abs(ref_backtest(L, list(last.numbers))[1] - ref_backtest(L[:-1], list(last.numbers))[1]
            - last.prize[0] * w1 / (w1 + 1)) < 1e-6 * last.prize[0]


def _sample_returns(L, C: np.ndarray) -> np.ndarray:
    """조합 표본(k×6) 의 백테스트 회수율 — ref_backtest 와 같은 규칙을 행렬로."""
    Xc = np.zeros((len(C), 45), bool)
    np.put_along_axis(Xc, C - 1, True, axis=1)
    W = np.zeros((len(L), 45), bool)
    np.put_along_axis(W, np.array([d.numbers for d in L]) - 1, True, axis=1)
    m = Xc.astype(np.int16) @ W.T.astype(np.int16)
    b = Xc[:, np.array([d.bonus for d in L]) - 1]
    prize = np.array([d.prize for d in L], float)
    w = np.array([d.winners for d in L], float)
    split = np.where(w[:, :3] > 0, prize[:, :3] * w[:, :3] / np.maximum(w[:, :3] + 1, 1), 0.0)
    pay = ((m == 6) * split[:, 0] + ((m == 5) & b) * split[:, 1] + ((m == 5) & ~b) * split[:, 2]
           + (m == 4) * prize[:, 3] + (m == 3) * prize[:, 4]).sum(1)
    return pay / sum(d.price for d in L)


@pytest.mark.skipif(shutil.which("node") is None, reason="node 없음")
def test_backtest_yardstick_is_the_distribution_over_all_combos():
    """비교 기준은 '평균적인 번호' 하나(평균 57%, 조합의 96% 가 그보다 적게 받음)가 아니라 전 조합의 분포다.

    저장된 분포(build_results 가 814만 조합 전수로 계산)를 (1) 정확한 평균식 — Σ회차 Σ등수 (그 등수 조합 수 ×
    1인당 몫) / 814만 / 쓴 돈 — 과, (2) 무작위 조합 20,000개 표본의 백분위와, (3) make.js 의 순위 함수와 대조한다.
    """
    D = json.loads((dataset.ROOT / "results" / "analysis.json").read_text(encoding="utf-8"))["lotto"]["backtest"]
    L = dataset.load_lotto()
    assert D["rounds"] == [L[0].round, L[-1].round]
    K = [1, 6, 228, 11115, 182780]
    spent = sum(d.price for d in L)
    mean = sum(K[0] * (d.prize[0] * d.winners[0] / (d.winners[0] + 1) if d.winners[0] else 0)
               + K[1] * (d.prize[1] * d.winners[1] / (d.winners[1] + 1) if d.winners[1] else 0)
               + K[2] * d.prize[2] * d.winners[2] / (d.winners[2] + 1) + K[3] * d.prize[3] + K[4] * d.prize[4]
               for d in L) / 8145060 / spent
    assert abs(D["mean"] / mean - 1) < 1e-5, (D["mean"], mean)   # 저장값은 유효숫자 6자리 (build_results._clean)
    rng = np.random.default_rng(21)
    C = np.sort(np.argpartition(rng.random((20000, 45)), 6, axis=1)[:, :6] + 1, axis=1)
    r = _sample_returns(L, C)
    for q in (10, 25, 50, 75, 90):
        assert abs(np.percentile(r, q) - np.interp(q, D["pct"], D["ret"])) < 0.012, q
    assert abs(np.median(r) - D["median"]) < 0.012
    assert D["below_mean"] > 0.9   # 평균보다 적게 받는 조합 비율 — 평균은 기준으로 쓰기 어렵다
    pick = r[:300].tolist()
    got = _node(_core() + f"const D = {json.dumps(D)}; console.log(JSON.stringify({json.dumps(pick)}.map(x => returnPercentile(x, D))));")
    emp = [100 * float(np.mean(r <= x)) for x in pick]
    assert np.max(np.abs(np.array(got) - np.array(emp))) < 3.0
