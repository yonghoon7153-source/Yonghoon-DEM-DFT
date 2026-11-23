#!/usr/bin/env python3
"""freeze.py — 웹앱을 서버 없이 열리는 한 장짜리 사본으로 내보낸다 (claude.ai 아티팩트 · 파일 공유용).

    python lottery/webapp/freeze.py          # → lottery/webapp/export/

Flask test client 로 /all (모든 화면을 이어 붙인 한 장)을 렌더한 뒤:
  - /static 의 CSS·JS 를 문서 안으로 넣는다 (아티팩트는 같은 출처의 스크립트 파일을 못 쓴다)
  - 폰트는 export/fonts/ 로 복사하고 CSS 의 url(../fonts/…) 를 fonts/… 로 바꾼다
  - /api/score.json · /api/palette.json 은 export/api/ 에 파일로 쓰고 상대 경로로 부른다
만드는 것 두 개:
  index.html     — 완전한 문서. 로컬에서 `python -m http.server -d lottery/webapp/export` 로 연다
  artifact.html  — 같은 내용에서 <!doctype>·<html>·<head>·<body> 껍데기만 뺀 것 (아티팩트 규약:
                   게시할 때 플랫폼이 껍데기를 씌운다)
이 사본은 정본이 아니다 — 수치의 정본은 results/analysis.json, 화면 정의는 templates/ 다.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import app as A  # noqa: E402

OUT = HERE / "export"
STATIC = HERE / "static"


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


def main() -> int:
    c = A.app.test_client()
    page = c.get("/all")
    score = c.get("/api/score.json")
    pal = c.get("/api/palette.json?onepage=1")
    for name, r in (("/all", page), ("/api/score.json", score), ("/api/palette.json", pal)):
        if r.status_code != 200:
            raise SystemExit(f"{name} → HTTP {r.status_code}")
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "api").mkdir(parents=True)
    shutil.copytree(STATIC / "fonts", OUT / "fonts", ignore=shutil.ignore_patterns("*.md", "*.txt"))
    html = _inline(page.get_data(as_text=True))
    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / "artifact.html").write_text(_artifact(html), encoding="utf-8")
    (OUT / "api" / "score.json").write_bytes(score.data)
    (OUT / "api" / "palette.json").write_bytes(pal.data)
    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"export/ — index.html {len(html.encode()) / 1024:.0f} KB · artifact.html · api/ · fonts/ "
          f"(합계 {size / 1024 / 1024:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
