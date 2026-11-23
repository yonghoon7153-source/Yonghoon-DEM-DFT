"""판정 문구가 p 값을 따르는가 — 자체 리뷰 1차 K1 (docs/SELF_REVIEW_R1.md).

리뷰 반례: analysis.json 사본에서 lotto.stats.summary[9].p_holm = 0.0076, lotto.ml.real.rows[12].p_bonferroni
= 0.016 으로 바꿔 렌더하면 /random 머리는 '○ 무작위와 구분 안 됨' 인데 같은 화면 표는 '● 차이 있음',
/ml 은 '보정 후 모두 1.00', 홈은 '19개 질문 모두 무작위와 구분되지 않는다' 가 그대로였다.
주간 갱신은 사람 검토 없이 분석을 다시 돌려 배포하므로, 결과가 바뀌면 문구도 따라 바뀌어야 한다.

여기서는 p 값만 바꾼 사본을 렌더한다 (다른 숫자는 실제 값 그대로) — 리뷰 반례와 같은 방식이다.
"""
import copy
import json
import re
import sys

import pytest

import build_results
import dataset

sys.path.insert(0, str(dataset.ROOT / "webapp"))
import app as A  # noqa: E402
import content as C  # noqa: E402

REAL = json.loads(C.RESULTS.read_text(encoding="utf-8"))


def flipped() -> dict:
    """리뷰 반례 두 개 + 연금·사람 쪽도 반대로 — 판정 하나하나가 숫자를 따라가는지 본다."""
    D = copy.deepcopy(REAL)
    lo, pe = D["lotto"], D["pension"]
    assert lo["stats"]["summary"][9]["question"].startswith("과거 빈도가 미래 빈도를 예고하나")
    lo["stats"]["summary"][9]["p_holm"] = 0.0076
    lo["stats"]["summary"][8]["p_holm"] = 0.03  # 간격 분포
    lo["stats"]["summary"][12]["p_holm"] = 0.02  # 홀수 개수 분포
    assert lo["ml"]["real"]["rows"][12]["model"] == "신경망 MLP"
    lo["ml"]["real"]["rows"][12]["p_bonferroni"] = 0.016
    pe["stats"]["summary"][0]["p_holm"] = 0.01  # 1등 조
    for r in pe["stats"]["positions"]:
        r["p_holm"] = min(r["p_holm"], 0.04)  # 자리별 숫자
    pe["ml"]["real"]["rows"][0]["p_bonferroni"] = 0.02
    lo["popularity"]["number_effect"]["wald_p"] = 0.4
    lo["popularity"]["tiers"]["5"]["r2_oof"] = -0.02
    return D


@pytest.fixture
def render(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "_cache", {"mtime": None, "data": None, "view": None})

    def go(D: dict, path: str) -> str:
        p = tmp_path / "analysis.json"
        p.write_text(json.dumps(D, ensure_ascii=False), encoding="utf-8")
        monkeypatch.setattr(C, "RESULTS", p)
        C._cache["mtime"] = None
        r = A.app.test_client().get(path)
        assert r.status_code == 200, path
        return r.get_data(as_text=True)
    return go


def head(html: str) -> tuple[str, str]:
    """화면 머리의 판정 칩 (종류, 머리 전체 글)."""
    h = re.search(r'<header class="phead">(.*?)</header>', html, re.S).group(1)
    kind = re.search(r'<p class="verdict">\s*<span class="chip v-(\w+)"', h).group(1)
    return kind, re.sub(r"<[^>]+>", "", h)


def myths(html: str) -> dict[str, str]:
    return dict(re.findall(r'<td class="rowh">([^<]+)</td>\s*<td><span class="chip [^"]*">([^<]+)</span>', html))


def test_real_results_keep_todays_wording(render):
    """대조: 실제 결과에서는 오늘 문구 그대로다."""
    assert head(render(REAL, "/random"))[0] == "same"
    assert head(render(REAL, "/ml"))[0] == "same"
    assert head(render(REAL, "/pension"))[0] == "same"
    assert head(render(REAL, "/people"))[0] == "diff"
    home = render(REAL, "/")
    assert "추첨기에는 패턴이 없고, 사람에게는 있다" in home
    m = myths(home)
    assert m["AI·머신러닝 번호 예측"] == "못 맞힘"
    assert m["핫·콜드 번호 (많이 나온 번호가 또 나온다)"] == "다르지 않음"


def test_flipped_p_values_flip_the_headlines(render):
    F = flipped()
    kind, text = head(render(F, "/random"))
    assert kind == "diff" and "과거 빈도가 미래 빈도를 예고하나" in text
    ml = render(F, "/ml")
    kind, text = head(ml)
    assert kind == "diff" and "신경망 MLP" in text
    assert "모두 1.00" not in ml
    assert head(render(F, "/pension"))[0] == "diff"
    assert head(render(F, "/people"))[0] == "same"


def test_flipped_p_values_flip_home_and_myths(render):
    home = render(flipped(), "/")
    for stale in ("추첨기에는 패턴이 없고", "질문 모두 무작위와 구분되지 않는다", "전부 무작위 수준", "개 통과",
                  "고르게 나온다"):
        assert stale not in home, stale
    m = myths(home)
    assert m["AI·머신러닝 번호 예측"] != "못 맞힘"
    assert m["핫·콜드 번호 (많이 나온 번호가 또 나온다)"] != "다르지 않음"
    assert m["오래 안 나온 번호는 나올 때가 됐다"] != "다르지 않음"


def test_flipped_p_values_flip_the_captions(render):
    """그림 설명의 '무작위와 같다' 류 문장도 해당 질문의 보정 p 를 따른다."""
    rnd = render(flipped(), "/random")
    for stale in ("과거에 많이 나온 번호가 이후에도 많이 나오지 않았다", "기하분포를 그대로 따른다",
                  "모두 전수 분포와 같다"):
        assert stale not in rnd, stale
    assert "보정 후에도 전수 분포와 다른 지표: 홀수 개수 분포가 무작위 조합과 다른가" in rnd
    pen = render(flipped(), "/pension")
    assert "고르게 나왔다" not in pen and "보정 후에도 숫자가 치우친 자리가 있다" in pen
    real = render(REAL, "/random")
    assert "과거에 많이 나온 번호가 이후에도 많이 나오지 않았다" in real
    assert "모두 전수 분포와 구분되지 않는다" in real


def test_results_md_ml_line_follows_p(tmp_path, monkeypatch):
    out = tmp_path / "RESULTS.md"
    monkeypatch.setattr(build_results, "RESULTS_MD", out)
    build_results.write_results_md(REAL)
    assert "선택 편향 범위" in out.read_text(encoding="utf-8")
    build_results.write_results_md(flipped())
    text = out.read_text(encoding="utf-8")
    assert "선택 편향 범위" not in text
    assert "Holm 보정 p < 0.05" in text and "Bonferroni p < 0.05" in text
