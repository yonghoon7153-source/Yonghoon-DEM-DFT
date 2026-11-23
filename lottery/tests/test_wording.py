"""값을 따라가야 할 문장 · 작은 결함 — 자체 리뷰 1차 L1 · M1 · 소 (docs/SELF_REVIEW_R1.md).

L1 반례: analysis.json 사본의 값을 바꿔 렌더해도 옛 문장('7 이 1위다', 'K = …(유형 없음)', 'R² 가 나아지지
않았다', '로그손실이 나빴다' …)이 그대로였다. '학습을 4배로 늘려도 …3배 이상' 은 analysis.json 에 기록이 없는
일회성 실험이었다. M1: 홈의 '회차별 당첨번호' 카드에 /data 설명이 붙었다.
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

import dataset

sys.path.insert(0, str(dataset.ROOT / "webapp"))
import app as A  # noqa: E402
import content as C  # noqa: E402

REAL = json.loads(C.RESULTS.read_text(encoding="utf-8"))


def changed() -> dict:
    """문장이 기대는 값을 반대로 바꾼 사본."""
    D = copy.deepcopy(REAL)
    lo = D["lotto"]
    ne = lo["popularity"]["number_effect"]
    b = ne["beta"]
    ne["beta"] = [-abs(x) - 0.01 for x in b[:31]] + [abs(x) + 0.01 for x in b[31:]]
    ne["beta"][32] = max(ne["beta"]) + 0.05  # 33 이 1위, 31 이하는 덜 고름
    t5 = lo["popularity"]["tiers"]["5"]
    t5["theta"]["prev_overlap"], t5["theta_p"]["prev_overlap"] = 0.01, 0.001  # 지난주 번호를 더 고름
    lo["em"]["best_k_bic"] = 2
    lo["svr"]["r2_oof"]["SVR RBF C=1"] = 0.9
    for r in lo["ml"]["real"]["rows"]:
        if r.get("dlogloss") is not None:
            r["dlogloss"] = -0.001
    dd = lo["ddpm"]
    dd["memorization"]["exact_copy_rate"] = 0.01
    dd["corr_with_train_freq"] = 0.01
    dd["six_clear_rate"] = 0.9
    dd["number_counts"] = [round(dd["n_generated"] * 6 / 45)] * 45
    lo["stats"]["eras"]["top_by_era"] = [[7, 1, 2, 3, 4, 5]] * len(lo["stats"]["eras"]["top_by_era"])
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
        return re.sub(r"\s+", " ", r.get_data(as_text=True))
    return go


STALE = {
    "/people": ["7 이 1위다", "31 이하가 대체로 인기", "지난주 번호는 피한다", "7 선호, 지난주 번호 회피"],
    "/": ["7·생일 번호가 인기고 지난주 번호는 피한다"],
    "/ml": ["(유형 없음)", "R² 가 나아지지 않았다", "로그손실이 나빴다", "외우지 않음", "없는 패턴을 만들어 냈다",
            "'6개' 구조를 덜 배움", "잡음을 '핫 번호'로 과장"],
    "/random": ["가장 많이 나온 번호도 매번 달랐다"],
}


@pytest.mark.parametrize("path", list(STALE))
def test_sentences_follow_the_values(render, path):
    html = render(changed(), path)
    for s in STALE[path]:
        assert s not in html, (path, s)


def test_sentences_still_read_the_same_on_real_results(render):
    """대조: 실제 결과에서는 같은 뜻의 문장이 나온다 (값에서 만든 문장)."""
    assert "7 이 1위다" in render(REAL, "/people")
    ml = render(REAL, "/ml")
    assert "(유형 없음)" in ml and "R² 가 나아지지 않았다" in ml and "없는 패턴을 만들어 냈다" in ml
    assert "33 이 1위다" in render(changed(), "/people")


def test_no_unrecorded_experiment_is_cited(render):
    assert "학습을 4배로 늘려도" not in render(REAL, "/ml")


def test_home_history_card_describes_history(render):
    """M1: 홈 카드 '회차별 당첨번호' 에 /data 설명(원본 URL · sha256 …)이 붙어 있었다."""
    home = render(REAL, "/")
    card = re.search(r'card-history.*?<p class="card-d">(.*?)</p>', home).group(1)
    assert "sha256" not in card and "회차" in card


def test_palette_has_no_dead_search_link():
    """소: ⌘K 팔레트의 '전문 검색' 이 본체 앱의 /search 로 가서 이 앱에서는 404 였다."""
    js = (dataset.ROOT / "webapp" / "static" / "js" / "app.js").read_text(encoding="utf-8")
    assert '"/search?q="' not in js
    assert A.app.test_client().get("/search?q=7").status_code == 404  # 없는 주소 — 그러니 링크도 없어야 한다


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash 없음")
def test_lotto_sh_port_without_value_fails_fast():
    """소: `lotto.sh --port` (값 없음) 에서 shift 2 가 실패해 같은 인자를 영원히 돌았다."""
    r = subprocess.run(["bash", str(dataset.ROOT / "webapp" / "lotto.sh"), "--port"],
                       capture_output=True, text=True, timeout=20)
    assert r.returncode == 2 and "--port" in (r.stdout + r.stderr)


def test_view_follows_raw_data_changes(tmp_path, monkeypatch):
    """소: view() 가 원본(data/raw) 변경을 확인하지 않아, 받기만 하고 분석을 안 돌리면 /history 가 옛 원본을 보였다."""
    raw = tmp_path / "raw"
    shutil.copytree(dataset.RAW_DIR, raw)
    monkeypatch.setattr(dataset, "RAW_DIR", raw)
    monkeypatch.setattr(C, "_cache", {"mtime": None, "data": None, "view": None})
    monkeypatch.setattr(C, "_raw", {"mtime": None, "lotto": None, "pension": None, "manifest": None})
    C.raw()
    before = C.view()["phistory"][0]["round"]
    obj = json.loads((raw / "pension720.json").read_bytes())
    obj["data"]["result"] = sorted(obj["data"]["result"], key=lambda r: int(r["psltEpsd"]))[:-1]
    (raw / "pension720.json").write_bytes(json.dumps(obj).encode())
    lot = raw / "lotto645.json"
    os.utime(lot, (lot.stat().st_atime, lot.stat().st_mtime + 5))  # 원본이 바뀌었다 (mtime)
    assert C.view()["phistory"][0]["round"] == before - 1


def test_readme_conclusions_carry_no_stale_numbers():
    """L1: README 결론에 손으로 적은 숫자(19·8개, 951회차, 66%)가 결과와 따로 놀았다 — 숫자는 RESULTS.md 와 화면에."""
    readme = (dataset.ROOT / "README.md").read_text(encoding="utf-8")
    concl = readme.split("## 결론", 1)[1].split("\n## ", 1)[0]
    assert not re.search(r"\d+\s*(%|회차|개 질문|개 ·)", concl), concl
