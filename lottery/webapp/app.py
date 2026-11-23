"""app.py — 복권 번호 연구소 webapp (로컬 · 읽기 전용).

뼈대는 본체 브랜치(`claude/14-gate-code-review-9qkx05`)의 `webapp/` 을 따랐다:
사이드바 · 아이콘 스프라이트 · 라이트/다크 토큰 · ⌘K 팔레트 · CSP `'self'` ·
쓰기 메서드 차단 · 서버가 계산하는 인라인 SVG 차트. 내용만 복권으로 바꿨다.

무엇을 서빙하나
  `lottery/results/analysis.json` — `lottery/build_results.py` 가 동행복권 원본
  (`lottery/data/raw/`, sha256 기록)으로 계산한 통계 검정·머신러닝 결과. **파일이 정본**이고
  이 앱은 그 위에 얹은 읽기 창이다. 번호 생성(무작위 추첨)은 브라우저에서 한다.

무엇을 안 하나
  쓰기. 사용자 번호를 저장하지 않고 바깥으로 아무것도 보내지 않는다
  (`_guard_mutation` 이 GET/HEAD/OPTIONS 외 모든 메서드를 405 로 막는다).

띄우기:  python3 lottery/webapp/app.py       (기본 http://127.0.0.1:5070)
         lottery/webapp/lotto.sh              (venv·의존성·빈 포트를 알아서 잡는다)
"""
from __future__ import annotations

import os

from flask import Flask, abort, jsonify, render_template, request

import content as C

app = Flask(__name__)

# 템플릿·정적파일을 매 요청마다 다시 읽는다 (본체 앱과 같은 이유: debug=False 에서
# Jinja 가 첫 렌더 결과를 쥐고 있으면 "고쳤는데 화면이 그대로" 가 된다).
# config 는 jinja_env 를 처음 건드리기 전에 넣어야 먹는다 — 순서를 지킨다.
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.filters.update(C.FILTERS)

# 기본 바인딩은 루프백. 본체 앱(5057)과 같이 띄울 수 있게 포트만 다르게 잡았다.
HOST = os.environ.get("WEBAPP_HOST", "127.0.0.1")
PORT = int(os.environ.get("WEBAPP_PORT", "5070"))

_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


@app.before_request
def _guard_mutation():
    """읽기 전용 게이트 — 쓰기 메서드는 라우트에 닿기 전에 거절한다 (fail-closed)."""
    if request.method not in _SAFE_METHODS:
        return jsonify({"error": "읽기 전용 앱입니다 — 쓰기 메서드를 받지 않습니다.",
                        "why": "분석 결과는 build_results.py 가 만든 파일이 정본이고, 사용자 번호는 저장하지 않습니다.",
                        "method": request.method}), 405
    return None


@app.after_request
def _sec_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    # 완전 로컬 앱이다 — 바깥으로 나가는 요청 경로 자체를 막는다 (본체 앱과 같은 정책).
    resp.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'none'; "
        "frame-ancestors 'self'")
    return resp


def _asset_version() -> str:
    try:
        paths = []
        for sub in ("css", "js"):
            d = os.path.join(app.static_folder, sub)
            if os.path.isdir(d):
                paths += [os.path.join(d, f) for f in os.listdir(d)]
        return str(int(max(os.path.getmtime(p) for p in paths)))
    except (OSError, ValueError):
        return "1"


@app.context_processor
def _inject():
    return {"asset_version": _asset_version(), "nav": C.SECTIONS, "onepage": False,
            "score_url": "/api/score.json", "palette_url": "/api/palette.json"}


def _page(names: list[str], active: str, title: str, onepage: bool = False):
    return render_template("page.html", sections=names, active=active, title=title,
                           onepage=onepage, V=C.view())


@app.route("/")
def home():
    return _page(["home"], "home", "한눈에 보기")


@app.route("/<name>")
def section(name):
    titles = {s[0]: s[2] for s in C.SECTIONS}
    if name not in titles or name == "home":
        abort(404)
    return _page([name], name, titles[name])


@app.route("/all")
def all_sections():
    """한 장짜리 — 모든 화면을 이어 붙인다 (freeze.py 가 정적 내보내기에 쓴다)."""
    return _page([s[0] for s in C.SECTIONS], "all", "전체", onepage=True)


@app.route("/api/score.json")
def api_score():
    return jsonify(C.generator_payload())


@app.route("/api/palette.json")
def api_palette():
    return jsonify({"items": C.palette_items(onepage=request.args.get("onepage") == "1")})


@app.route("/favicon.svg")
def favicon():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
           '<circle cx="16" cy="16" r="14" fill="#fbc400"/><circle cx="16" cy="16" r="8" fill="#fff"/>'
           '<text x="16" y="20.5" font-size="11" text-anchor="middle" font-family="monospace" '
           'font-weight="700" fill="#14161a">7</text></svg>')
    return app.response_class(svg, mimetype="image/svg+xml")


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html", active=None), 404


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
