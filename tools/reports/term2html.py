#!/usr/bin/env python3
"""term2html.py — 터미널 출력 텍스트를 '터미널처럼 보이는' HTML 한 장으로 바꾼다 (월별 증빙 캡처용).

왜: 터미널에는 스크롤 캡처가 없어서 긴 출력 (증빙 결과지 · `last` 접속 기록) 을 여러 장으로 찍어야 했다 (9 월 4 · 5 번 PDF).
    HTML 한 장으로 만들면 브라우저에서 ① 전체 페이지 캡처 (Chrome/Edge: F12 → Ctrl+Shift+P → 'Capture full size screenshot')
    ② 인쇄 → 'PDF로 저장' (배경 그래픽 켬) 으로 한 번에 나온다.

    bash tools/reports/gabia_october_evidence.sh > ~/evid/evidence_2026_10.txt 2>&1
    python3 tools/reports/term2html.py ~/evid/evidence_2026_10.txt --cmd "bash tools/reports/gabia_october_evidence.sh" -o ~/evid/evidence_2026_10.html
    python3 tools/reports/term2html.py --selftest

모양: Ubuntu 기본 터미널 색 (배경 #300a24 · 글자 흰색 · 고정폭) — 9 월 캡처와 같은 색. 글꼴은 보는 쪽 (Windows) 글꼴을 쓴다
(한글은 브라우저가 맑은 고딕 등으로 채운다). --cmd 를 주면 맨 위에 프롬프트 줄을, 맨 아래에 만든 시각 · 원문 sha256 · 줄 수를 단다.

⛔ 못 하는 것: 색 코드 (ANSI) 를 색으로 바꾸지 않는다 — 지운다 (우리 증빙 스크립트는 색을 안 쓴다) · 원문을 고치거나 거르지 않는다
   (무엇을 찍을지는 원래 명령이 정한다) · 빈 입력은 거부한다 (빈 캡처는 거의 항상 실수다).
"""
import argparse
import datetime as dt
import hashlib
import html
import os
import re
import socket
import sys

ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
CSS = ("body{background:#300a24;color:#ffffff;margin:0;padding:18px 22px}"
       "pre{margin:0;white-space:pre;font:14px/1.28 'Ubuntu Mono','DejaVu Sans Mono','D2Coding',Consolas,'Malgun Gothic',monospace}"
       ".p{color:#8ae234;font-weight:bold}.d{color:#729fcf;font-weight:bold}.f{color:#ad7fa8}")


def render(text, cmd=None, host=None, user="root", cwd="~", when=None):
    if not text.strip():
        raise ValueError("빈 입력 — 캡처가 비었다 (명령이 실패했거나 출력이 다른 곳으로 갔다)")
    text = ANSI.sub("", text.replace("\r\n", "\n"))
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    lines = text.rstrip("\n").split("\n")
    host = host or socket.gethostname()
    when = when or dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z").strip()
    body = []
    if cmd:
        body.append(f'<span class="p">{html.escape(user)}@{html.escape(host)}</span>:<span class="d">{html.escape(cwd)}</span># {html.escape(cmd)}')
    body += [html.escape(ln) for ln in lines]
    if cmd:
        body.append(f'<span class="f">— {len(lines)} lines · sha256 {sha[:16]} · rendered {html.escape(when)} on {html.escape(host)}</span>')
    title = html.escape(cmd or "terminal output")
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{CSS}</style></head><body><pre>' + "\n".join(body) + "</pre></body></html>\n"), len(lines), sha


def _selftest():
    ok = bad = 0

    def ck(name, cond):
        nonlocal ok, bad
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok, bad = ok + bool(cond), bad + (not cond)

    h, n, sha = render("a < b & c\n  두 칸 들여쓰기\n\x1b[1;32mgreen\x1b[0m\n", cmd="echo x", host="h1", when="T")
    ck("[양성] <, & 를 이스케이프한다", "a &lt; b &amp; c" in h)
    ck("[양성] 앞 공백 · 한글을 그대로 둔다", "\n  두 칸 들여쓰기\n" in h)
    ck("[양성] ANSI 색 코드는 지운다", "\x1b" not in h and "\ngreen\n" in h)
    ck("[양성] 줄 수 = 원문 줄 수 (3) · 꼬리에 sha256 앞 16 자", n == 3 and sha[:16] in h)
    ck("[양성] 프롬프트 줄 (user@host:~# 명령)", "root</span>" not in h and "root@h1</span>" in h and "# echo x" in h)
    h2, _, _ = render("x\n")
    ck("[양성] --cmd 가 없으면 프롬프트 · 꼬리 줄을 달지 않는다", "lines · sha256" not in h2 and 'class="p"' not in h2)
    for nm, t in (("빈 문자열", ""), ("공백만", " \n\n\t\n")):
        try:
            render(t); refused = False
        except ValueError:
            refused = True
        ck(f"⛔[음성] {nm} 입력은 거부", refused)
    print(f"term2html selftest: ✓ {ok} · ✗ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("src", nargs="?", help="텍스트 파일 (없으면 표준 입력)")
    ap.add_argument("-o", "--out", help="쓸 HTML (없으면 src 옆에 .html)")
    ap.add_argument("--cmd", help="맨 위 프롬프트 줄에 적을 명령 (주면 꼬리 줄도 단다)")
    ap.add_argument("--host", help="프롬프트의 호스트 이름 (기본 이 기계)")
    ap.add_argument("--cwd", default="~", help="프롬프트의 현재 폴더 (기본 ~)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    text = open(a.src, encoding="utf-8", errors="replace").read() if a.src else sys.stdin.read()
    out = a.out or ((os.path.splitext(a.src)[0] + ".html") if a.src else None)
    if not out:
        ap.error("표준 입력이면 -o 가 필요하다")
    try:
        page, n, sha = render(text, a.cmd, a.host, cwd=a.cwd)
    except ValueError as e:
        print(f"⛔ {e}", file=sys.stderr); return 2
    open(out, "w", encoding="utf-8").write(page)
    print(f"→ {out} · {n} 줄 · sha256 {sha[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
