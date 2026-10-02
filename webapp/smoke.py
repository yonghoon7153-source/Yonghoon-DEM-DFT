#!/usr/bin/env python3
"""smoke.py — webapp 라우트 전수 점검 (서버·포트 없이 Flask test_client 로).

왜 있나
  2026-09-11 전수조사 전까지 `webapp/` 은 **자동 검사가 0** 이었다. wiki-lint CI 가
  `paths: ["wiki/**"]` 로만 걸려 있어 9만 자 파이썬 + 11만 자 CSS 가 아무 게이트 없이
  올라갔다. 이 파일이 그 게이트다.

무엇을 보나 (전부 실행 결과로 — 목록을 손으로 적지 않는다)
  1. content.py 등록부가 아는 **모든** 페이지 URL → 200        (위키가 자라도 따라온다)
  2. 고정 화면·API → 200
  3. figures.json 에 등록된 **모든** 그림이 `/api/file/` 로 서빙되나
  4. 정적 자산(css/js/fonts) → 200
  5. 읽기 전용 게이트: 허용 밖 쓰기 메서드 → 405
  6. 경로 탈출·허용 뿌리 밖 파일 → 404
  7. 보안 헤더(CSP·nosniff·X-Frame) 존재
  8. `/api/md` 가 raw HTML 을 이스케이프하나 (XSS)

쓰기:  python3 webapp/smoke.py        (0 = 통과, 1 = 실패)
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
# chat 은 키 없이도 import 되어야 한다 (앱은 뜨고 /chat 만 비활성) — 그것도 검사의 일부다.
os.environ.setdefault("LI2S_CHAT_FAKE", "0")

import app as A          # noqa: E402
import content as C      # noqa: E402

fails: list[str] = []
checked = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global checked
    checked += 1
    if not cond:
        fails.append(f"{name}{(' — ' + detail) if detail else ''}")


def main() -> int:
    global checked
    cl = A.app.test_client()

    def get(url):
        return cl.get(url)

    # 1. 등록부가 아는 모든 페이지
    pages = C.scan_pages()
    check("registry non-empty", len(pages) > 0, f"scan_pages() -> {len(pages)}")
    for slug, p in sorted(pages.items()):
        r = get(p["url"])
        check(f"page {p['url']}", r.status_code == 200, f"status {r.status_code}")

    # 1-b. 홈이 **열린 질문 카드 전부**를 싣는가 (2026-10-02 신설).
    #      홈 라우트가 `questions[:4]` 로 잘려 있어서 카드가 5장이 된 순간 하나가
    #      조용히 사라졌다. 갯수가 아니라 **슬러그 전수**를 본다 — 카드가 늘어도 따라온다.
    #      ⚠ 페이지 전체를 보면 안 된다: 홈은 `index.md` 본문을 함께 렌더링하고 그 안에
    #      모든 질문 슬러그가 wikilink 로 들어 있어서, 패널이 잘려도 검사가 통과한다
    #      (2026-10-02 에 실제로 그렇게 헛돌았다 — 읽기 전용 게이트와 같은 함정).
    #      그래서 **"지금 열려 있는 질문" 패널 구간만** 잘라서 본다.
    home_full = get("/").get_data(as_text=True)
    _h = home_full.find("지금 열려 있는 질문")
    home = home_full[_h:home_full.find("</section>", _h)] if _h >= 0 else ""
    check("home has open-question panel", _h >= 0 and len(home) > 0,
          "홈에 '지금 열려 있는 질문' 패널이 없다")
    n_open = 0
    for slug, p in sorted(pages.items()):
        if p["kind"] != "question":
            continue
        if str(p["meta"].get("status", "open")).strip().lower() not in ("open", "active"):
            continue
        n_open += 1
        check(f"home lists open question {slug}", slug in home,
              "열린 질문 카드가 홈에 없다 — index.html/app.py home() 의 잘림을 확인")
    check("open questions found", n_open > 0, "열린 질문 카드가 하나도 없다")

    # 2. 고정 화면 · API
    for url in ("/", "/roadmap", "/papers", "/compare", "/questions", "/concepts",
                "/entities", "/chat", "/notes", "/search?q=Li2S", "/favicon.svg",
                "/api/palette.json", "/api/chat/status"):
        r = get(url)
        check(f"route {url}", r.status_code == 200, f"status {r.status_code}")

    pal = get("/api/palette.json").get_json()
    check("palette lists pages", len(pal.get("items", [])) >= len(pages))

    # 3. figures.json 에 등록된 모든 그림이 실제로 서빙되나
    figroot = C.WIKI / "raw" / "figures"
    n_fig = 0
    for j in sorted(figroot.glob("*/figures.json")):
        meta = json.loads(j.read_text(encoding="utf-8"))
        slug = meta.get("slug", j.parent.name)
        api = get(f"/api/figures/{slug}.json")
        check(f"figures api {slug}", api.status_code == 200, f"status {api.status_code}")
        for f in meta.get("figures", []):
            rel = f.get("rel") or f"{slug}/{f.get('file', '')}"
            r = get(f"/api/file/{rel}")
            check(f"figure {rel}", r.status_code == 200, f"status {r.status_code}")
            n_fig += 1
    check("figures found", n_fig > 0, "figures.json 에 그림이 하나도 없다")

    # 4. 정적 자산
    static = pathlib.Path(A.app.static_folder)
    n_static = 0
    for sub in ("css", "js", "fonts"):
        d = static / sub
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix in (".css", ".js", ".woff2"):
                r = get(f"/static/{sub}/{f.name}")
                check(f"static {sub}/{f.name}", r.status_code == 200, f"status {r.status_code}")
                n_static += 1
    check("static found", n_static > 0)

    # 5. 읽기 전용 게이트 — 허용 목록(/api/chat, /api/md) 밖의 쓰기는 405.
    #    ⚠ status 405 만 보면 안 된다: 그 라우트들은 GET 전용이라 게이트를 **꺼도**
    #      Flask 자체 라우팅이 405 를 낸다 (이 검사를 처음 썼을 때 게이트를 열어 놓고도
    #      통과했다 — 2026-09-11). `_guard_mutation` 이 돌려주는 JSON 본문까지 본다.
    for meth, url in (("POST", "/"), ("DELETE", "/roadmap"), ("PUT", "/api/chat"),
                      ("POST", "/api/palette.json"), ("POST", "/api/figures/x.json")):
        r = cl.open(url, method=meth)
        body = r.get_json(silent=True) or {}
        check(f"guard {meth} {url}",
              r.status_code == 405 and "읽기 전용" in str(body.get("error", "")),
              f"status {r.status_code} body {str(body)[:60]!r}")
    # 허용된 둘은 405 가 아니어야 한다 (400/503 등 라우트가 실제로 받는다)
    r = cl.post("/api/md", json={"text": "x"})
    check("allow POST /api/md", r.status_code == 200, f"status {r.status_code}")

    # 6. 경로 탈출 · 허용 뿌리 밖
    for url in ("/api/file/../../etc/passwd",
                "/api/file/wiki/raw/papers/anything.md",
                "/concept/../../etc/passwd",
                "/doc/../CLAUDE.md",
                "/concept/does-not-exist"):
        r = get(url)
        check(f"deny {url}", r.status_code == 404, f"status {r.status_code}")

    # 7. 보안 헤더
    h = get("/").headers
    for key, must in (("Content-Security-Policy", "default-src 'self'"),
                      ("X-Content-Type-Options", "nosniff"),
                      ("X-Frame-Options", "SAMEORIGIN"),
                      ("Referrer-Policy", "same-origin")):
        check(f"header {key}", must in h.get(key, ""), f"got {h.get(key)!r}")

    # 8. /api/md 는 raw HTML 을 이스케이프한다
    r = cl.post("/api/md", json={"text": "<script>alert(1)</script>"})
    html = r.get_json().get("html", "")
    check("md escapes script", "<script>" not in html, f"got {html[:80]!r}")
    r = cl.post("/api/md", json={"text": "[[li2s-activation-first-charge]]"})
    check("md resolves wikilink", "/concept/li2s-activation-first-charge" in r.get_json().get("html", ""))

    print(f"=== WEBAPP SMOKE ===\n검사 {checked}건 "
          f"(페이지 {len(pages)} · 그림 {n_fig} · 정적 {n_static})")
    if fails:
        print(f"\nFAILURES ({len(fails)}):")
        for f in fails:
            print(" ✗", f)
        return 1
    print("\nRESULT: 0 failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
