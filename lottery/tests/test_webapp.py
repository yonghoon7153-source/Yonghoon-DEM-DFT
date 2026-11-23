"""웹앱: 모든 화면이 뜨고, 읽기 전용이고, CSP 를 지키는가 (인라인 스크립트가 없어야 한다)."""
import re
import sys

import pytest

import dataset

sys.path.insert(0, str(dataset.ROOT / "webapp"))
import app as A  # noqa: E402
import content as C  # noqa: E402

PAGES = ["/", "/make", "/random", "/ml", "/people", "/pension", "/data", "/all"]


@pytest.fixture(scope="module")
def client():
    A.app.config["PROPAGATE_EXCEPTIONS"] = True
    return A.app.test_client()


@pytest.mark.parametrize("path", PAGES)
def test_pages_render_without_inline_script(client, path):
    r = client.get(path)
    assert r.status_code == 200
    assert "default-src 'self'" in r.headers["Content-Security-Policy"]
    html = r.get_data(as_text=True)
    assert not re.search(r"<script(?![^>]*\bsrc=)[^>]*>", html), "CSP script-src 'self' 는 인라인 스크립트를 막는다"
    assert not re.search(r"\son[a-z]+=", html), "인라인 이벤트 핸들러도 막힌다"
    visible = re.sub(r"<(script|style)\b.*?</\1>|<[^>]+>", " ", html, flags=re.S)
    leaked = re.findall(r"\b(None|nan|NaN|Undefined)\b", visible)
    assert not leaked, f"빈 값이 화면에 새어 나왔다: {leaked[:5]}"


def test_read_only_and_404(client):
    assert client.post("/make").status_code == 405
    assert client.delete("/").status_code == 405
    assert client.get("/nope").status_code == 404


def test_score_api_has_what_make_js_reads(client):
    d = client.get("/api/score.json").get_json()
    for k in ("beta", "theta", "center", "gamma0", "gamma1", "eta_percentiles", "pct", "mu_avg",
              "share_avg", "latest_numbers", "pool1_recent_mean"):
        assert k in d["score"], k
    assert len(d["score"]["beta"]) == 45 and len(d["past"]) == len(dataset.load_lotto())
    assert all(len(c) == 6 for c in d["ddpm_pool"])


def test_bar_charts_start_at_zero():
    """막대그래프 축을 자르면 차이가 과장된다 — 모든 막대 차트의 눈금에 0 이 있어야 한다 (보정 비율 차트 제외)."""
    v = C.view()
    for key in ("freq_chart", "carry_chart", "gap_chart", "sum_chart", "ddpm_chart", "pop_chart", "manual_chart"):
        assert any(g["zero"] for g in v[key]["grid"]), key


def test_static_site_for_cloudflare_pages_matches_app(client, tmp_path, monkeypatch):
    """freeze.py 의 dist/ (Cloudflare Pages 출력): 화면 전부 + 404 + API, `_headers` CSP 가 app.py 와 같다."""
    import freeze
    monkeypatch.setattr(freeze, "DIST", tmp_path / "dist")
    out = freeze.build_site(client)
    names = {p.name for p in out.iterdir()}
    assert {"index.html", "make.html", "random.html", "ml.html", "people.html", "pension.html", "data.html",
            "all.html", "404.html", "favicon.svg", "_headers", "api", "static"} <= names
    csp = client.get("/").headers["Content-Security-Policy"]
    assert f"Content-Security-Policy: {csp}\n" in (out / "_headers").read_text(encoding="utf-8")
    assert (out / "static" / "fonts" / "OFL-Pretendard.txt").exists()  # OFL: 폰트와 라이선스를 같이 배포
    assert (out / "make.html").read_bytes() == client.get("/make").data
