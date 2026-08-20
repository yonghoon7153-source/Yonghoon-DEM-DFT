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
