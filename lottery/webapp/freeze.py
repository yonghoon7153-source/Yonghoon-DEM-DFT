#!/usr/bin/env python3
"""freeze.py — 웹앱을 서버 프로그램 없이 서빙되는 정적 사본으로 내보낸다.

    python lottery/webapp/freeze.py          # → dist/ (Cloudflare Pages) + export/ (claude.ai 아티팩트)

Flask test client 로 각 화면을 렌더해 파일로 쓴다. 앱은 계산하지 않고 results/analysis.json 을
읽기만 하므로, 정적 사본도 Flask 화면과 **같은 HTML** 이다. 필요한 것은 Flask 하나다
(Cloudflare Pages 빌드 이미지에서도 `pip install -r requirements.txt` 한 번이면 돈다).

dist/ — Cloudflare Pages 출력 (`lotto.bmlwork.kr`, nihonchizu 의 nihoncheese.bmlwork.kr 과 같은 방식)
  화면마다 한 파일 (`/make` → make.html — Pages 가 확장자 없는 주소로 서빙한다), 404.html,
  /static 그대로, /api/*.json, favicon.svg, `_headers` (app.py 의 보안 헤더와 **같은 CSP** —
  tests/test_webapp.py 가 둘이 갈라지지 않았는지 본다). 인라인 스크립트 없음.
export/ — claude.ai 아티팩트용 한 장 (/all). 아티팩트는 같은 출처의 스크립트 파일을 못 쓰므로
  CSS·JS 를 문서 안에 넣고, <!doctype>·<html>·<head>·<body> 껍데기를 뺀 artifact.html 도 만든다.
둘 다 파생물이라 git 에 넣지 않는다 (.gitignore). 정본은 results/analysis.json, 화면 정의는 templates/.
정적 호스팅(Pages · `python3 -m http.server`)으로 열어야 한다 — 파일을 file:// 로 바로 열면 브라우저가
api/*.json 을 가져오지 못해 번호 생성기 · 세금 계산기 · ⌘K 팔레트가 동작하지 않는다 (읽기 화면은 보인다).
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import app as A  # noqa: E402
import content as C  # noqa: E402

DIST = HERE / "dist"
OUT = HERE / "export"
STATIC = HERE / "static"

# 화면 경로 → 파일. Cloudflare Pages 는 /make 를 make.html 로 서빙한다 ("pretty URLs").
ROUTES = {path: ("index.html" if path == "/" else path.strip("/") + ".html")
          for _name, path, *_ in C.SECTIONS}
ROUTES["/all"] = "all.html"


def headers_file(csp: str) -> str:
    """Cloudflare Pages `_headers` — app.py `_sec_headers` 와 같은 값 + 캐시."""
    return (
        "# Cloudflare Pages headers — app.py _sec_headers 와 같은 값이어야 한다 (tests/test_webapp.py)\n"
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: same-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n"
        f"  Content-Security-Policy: {csp}\n"
        "# CSS·JS 는 ?v=<mtime> 를 달고 불린다 — 하루 캐시여도 고친 파일이 바로 보인다\n"
        "/static/*\n"
        "  Cache-Control: public, max-age=86400\n"
        "/static/fonts/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "# 분석 결과는 push 마다 바뀔 수 있다\n"
        "/api/*\n"
        "  Cache-Control: public, max-age=300\n"
    )


def build_site(c) -> Path:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    csp = None
    for path, name in ROUTES.items():
        r = c.get(path)
        if r.status_code != 200:
            raise SystemExit(f"{path} → HTTP {r.status_code}")
        csp = csp or r.headers["Content-Security-Policy"]
        (DIST / name).write_bytes(r.data)
    r = c.get("/__no_such_page__")
    if r.status_code != 404:
        raise SystemExit(f"404 화면이 404 를 주지 않는다: {r.status_code}")
    (DIST / "404.html").write_bytes(r.data)
    (DIST / "api").mkdir()
    for api in ("score.json", "palette.json"):
        r = c.get(f"/api/{api}")
        if r.status_code != 200:
            raise SystemExit(f"/api/{api} → HTTP {r.status_code}")
        (DIST / "api" / api).write_bytes(r.data)
    (DIST / "favicon.svg").write_bytes(c.get("/favicon.svg").data)
    shutil.copytree(STATIC, DIST / "static")  # 폰트 라이선스(OFL)도 같이 간다
    (DIST / "_headers").write_text(headers_file(csp), encoding="utf-8")
    for html in DIST.glob("*.html"):
        if re.search(r"<script(?![^>]*\bsrc=)[^>]*>", html.read_text(encoding="utf-8")):
            raise SystemExit(f"{html.name} 에 인라인 스크립트가 있다 — CSP script-src 'self' 에 막힌다")
    return DIST


def _inline(html: str) -> str:
    def css(m):
        text = (STATIC / "css" / m.group(1)).read_text(encoding="utf-8")
        text = text.replace("url(\"../fonts/", "url(\"fonts/")
        return f"<style>/* {m.group(1)} */\n{text}\n</style>"

    def js(m):
        text = (STATIC / "js" / m.group(1)).read_text(encoding="utf-8")
        if "</script" in text.lower():
            raise SystemExit(f"{m.group(1)} 안에 </script 가 있어 인라인할 수 없다")
        return f"<script>/* {m.group(1)} */\n{text}\n</script>"

    html, n_css = re.subn(r'<link rel="stylesheet" href="/static/css/([\w.-]+\.css)\?v=\d+">', css, html)
    html, n_js = re.subn(r'<script src="/static/js/([\w.-]+\.js)\?v=\d+"(?: defer)?></script>', js, html)
    if n_css != 2 or n_js != 3:
        raise SystemExit(f"인라인 대상 수가 예상과 다르다: css {n_css}/2, js {n_js}/3 — base.html 이 바뀌었나?")
    html = re.sub(r'<link rel="icon"[^>]*>\n?', "", html)
    for a, b in (('data-score-url="/api/score.json"', 'data-score-url="api/score.json"'),
                 ('data-src="/api/palette.json"', 'data-src="api/palette.json"')):
        if a not in html:
            raise SystemExit(f"치환 대상 없음: {a}")
        html = html.replace(a, b)
    return html


def _artifact(html: str) -> str:
    """아티팩트 규약: 껍데기(doctype·html·head·body)를 빼고 내용만 남긴다."""
    html = re.sub(r"<!doctype html>\s*", "", html, flags=re.I)
    html = re.sub(r"<html[^>]*>\s*|</html>\s*", "", html)
    html = re.sub(r"<head>\s*|</head>\s*", "", html)
    html = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', "", html)
    html = re.sub(r"<body[^>]*>\s*|</body>\s*", "", html)
    return html


def build_export(c) -> Path:
    page, score, pal = c.get("/all"), c.get("/api/score.json"), c.get("/api/palette.json?onepage=1")
    for name, r in (("/all", page), ("/api/score.json", score), ("/api/palette.json", pal)):
        if r.status_code != 200:
            raise SystemExit(f"{name} → HTTP {r.status_code}")
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "api").mkdir(parents=True)
    shutil.copytree(STATIC / "fonts", OUT / "fonts")
    html = _inline(page.get_data(as_text=True))
    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / "artifact.html").write_text(_artifact(html), encoding="utf-8")
    (OUT / "api" / "score.json").write_bytes(score.data)
    (OUT / "api" / "palette.json").write_bytes(pal.data)
    return OUT


def main() -> int:
    c = A.app.test_client()
    for d in (build_site(c), build_export(c)):
        files = [p for p in d.rglob("*") if p.is_file()]
        print(f"{d.name}/ — 파일 {len(files)}개, {sum(p.stat().st_size for p in files) / 1024 / 1024:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
