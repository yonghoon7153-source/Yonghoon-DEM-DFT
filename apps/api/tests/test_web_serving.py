"""Serving the built frontend and the API from one port.

`bml` runs a single process on 5003: the API under /api, the compiled web app
everywhere else.  These checks cover the three things that go wrong with that
arrangement -- deep links 404ing, API typos silently rendering the app, and a
path traversal escaping the build directory.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import mount_web


@pytest.fixture
def dist(tmp_path):
    """A minimal stand-in for `apps/web/dist`."""
    (tmp_path / "index.html").write_text("<!doctype html><title>app</title>")
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "index-abc123.js").write_text("console.log('built')")
    (tmp_path / "favicon.svg").write_text("<svg/>")

    outside = tmp_path.parent / "secret.txt"
    outside.write_text("do not serve me")
    return tmp_path


@pytest.fixture
def served(dist):
    app = FastAPI()

    @app.get("/api/health")
    def health() -> dict:
        return {"status": "ok"}

    assert mount_web(app, dist) is True
    with TestClient(app) as client:
        yield client


def test_the_root_serves_the_app(served):
    response = served.get("/")
    assert response.status_code == 200
    assert "<title>app</title>" in response.text


def test_a_deep_link_serves_the_app_not_a_404(served):
    """The browser routes /samples/1; the server has never heard of it."""
    response = served.get("/samples/1")
    assert response.status_code == 200
    assert "<title>app</title>" in response.text


def test_a_real_file_is_served_as_itself(served):
    assert served.get("/favicon.svg").text == "<svg/>"
    assert served.get("/assets/index-abc123.js").text == "console.log('built')"


def test_the_api_still_answers(served):
    assert served.get("/api/health").json() == {"status": "ok"}


def test_an_unknown_api_path_404s_instead_of_rendering_the_app(served):
    """A typo in an endpoint must not look like it worked."""
    response = served.get("/api/nope")
    assert response.status_code == 404
    assert "<title>app</title>" not in response.text


@pytest.mark.parametrize(
    "attack",
    ["../secret.txt", "..%2Fsecret.txt", "assets/../../secret.txt", "/../../etc/passwd"],
)
def test_a_path_traversal_cannot_escape_the_build_directory(served, attack):
    response = served.get(f"/{attack}")
    assert "do not serve me" not in response.text
    assert "root:" not in response.text


def test_without_a_build_the_root_explains_what_to_run(tmp_path):
    app = FastAPI()
    assert mount_web(app, tmp_path) is False
    with TestClient(app) as client:
        body = client.get("/").json()
    assert body["status"] == "api only"
    assert "bml" in body["detail"]
    assert body["port"] == 5003


def test_a_build_without_assets_still_serves(tmp_path):
    """A build with everything inlined has no assets/ directory."""
    (tmp_path / "index.html").write_text("<!doctype html><title>inline</title>")
    app = FastAPI()
    assert mount_web(app, tmp_path) is True
    with TestClient(app) as client:
        assert "<title>inline</title>" in client.get("/anything").text


def test_the_default_port_is_the_one_documented_everywhere():
    """5003 appears in the Makefile, vite.config.ts, bml and the README.

    A drift between them would send someone to a dead address, so the default
    is asserted here rather than only living in four places.
    """
    from app.settings import DEFAULT_PORT, settings

    assert DEFAULT_PORT == 5003
    assert settings.port == 5003
    assert any(f":{DEFAULT_PORT}" in origin for origin in settings.cors_origins)


# --- 캐시 헤더 ----------------------------------------------------------------
#
# 실제로 막힌 자리 (2026-08-24): 저장소도 최신, 서버도 최신 커밋, 번들도 새로
# 빌드돼 있는데 화면만 옛것이었다. 남은 것은 브라우저가 옛 `index.html` 을 들고
# 있는 경우뿐인데, 그 실패는 **서버를 다시 띄워도 사라지지 않고** 보고 있는
# 기계에 아무 흔적도 남기지 않는다. 다른 모든 설명(옛 체크아웃·옛 빌드·다른
# 브랜치)이 증거로 배제되고 나서야 남는다.

def _built(tmp_path, *, assets=True):
    from fastapi import FastAPI

    from app.main import mount_web

    (tmp_path / "index.html").write_text("<html></html>")
    if assets:
        (tmp_path / "assets").mkdir()
        (tmp_path / "assets" / "index-DqARYaLz.js").write_text("x")
    app = FastAPI()
    assert mount_web(app, tmp_path)
    return TestClient(app)


def test_the_shell_is_never_served_from_cache_without_asking(tmp_path):
    """`index.html` 은 해시 붙은 번들의 *이름* 을 들고 있는 파일이다.

    이게 캐시되면 브라우저는 옛 번들 이름을 계속 요청하고, 서버에는 새 빌드가
    있는데 화면은 옛것이다. `no-cache` 는 "저장하지 마라" 가 아니라 "쓰기 전에
    물어봐라" 이므로, 안 바뀐 껍데기는 304 한 번으로 끝난다.
    """
    client = _built(tmp_path)
    for path in ("/", "/samples/1"):
        assert client.get(path).headers["cache-control"] == "no-cache", path


def test_hashed_assets_may_be_cached_forever(tmp_path):
    """이름에 해시가 붙으면 내용이 바뀔 때 이름이 바뀐다 — 무효화할 것이 없다.

    헤더가 없으면 브라우저가 바뀔 수 없는 파일을 매번 재검증한다. 페이지를 열
    때마다 번들마다 왕복 한 번씩, 랩 와이파이에서, 아무 이유 없이.
    """
    header = _built(tmp_path).get("/assets/index-DqARYaLz.js").headers["cache-control"]
    assert "immutable" in header
    assert "max-age=31536000" in header


def test_an_unhashed_file_does_not_get_the_year(tmp_path):
    """해시가 없는 파일에 immutable 을 걸면 1년 동안 못 고친다.

    껍데기에 헤더를 안 거는 것과 같은 버그를, 한 폴더 아래에서 저지르는 것이다.
    """
    (tmp_path / "favicon.ico").write_text("x")
    (tmp_path / "manifest.json").write_text("{}")
    client = _built(tmp_path, assets=False)
    for name in ("favicon.ico", "manifest.json"):
        assert client.get(f"/{name}").headers["cache-control"] == "no-cache", name


def test_the_hash_pattern_does_not_fire_on_ordinary_names():
    """오탐 하나가 파일 하나를 1년 동안 브라우저에 얼린다.  좁게 잡는다."""
    from app.main import _cache_headers

    for name in ("index-DqARYaLz.js", "app-a1B2c3D4e5.css", "logo-ZZZZZZZZ.svg"):
        assert "immutable" in _cache_headers(name)["Cache-Control"], name
    for name in ("favicon.ico", "manifest.json", "logo-dark.svg",
                 "chart-v2.js", "index.html", "some-file.txt"):
        assert "immutable" not in _cache_headers(name)["Cache-Control"], name
