#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""주간보고 10-26 ~ 11-01 — 웹앱 `/worklog` 에 뜨는지 · 사이드바 · 거부 (1저자 11-01 "주간보고하고 웹앱 추가하자").

주간보고는 새 라우트를 만들지 않는다 — `webapp/app.py` 는 봉인 32 (`scripts/run_network_194_parallel.py` CODE_FILES) 라
고치면 봉인 지문이 바뀐다.  이미 있는 `/worklog` 창구가 `docs/worklog/weekly_YYYYMMDD.md` 를 최신순으로 모아 렌더한다
(`_worklog_scan` · 키 = 8 자리 날짜만).  그래서 이 시험은 그 창구에 이번 주 리포트가 실제로 뜨는지와 사이드바 이름,
모르는 이름 · 경로 탈출 거부를 본다.  (일반 회귀 = `webapp/test_worklog_page.py`.)

  python3 webapp/test_worklog_weekly_20261101.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

KEY = '20261101'
TITLE = '주간 정리 2026-10-26 ~ 11-01'
#: 리포트 본문에 그대로 있어야 하는 숫자 (출처 = git · 원장 · 진행 기록 — 리포트 실행 요약 표)
NUMBERS = ('232', '820 → 923', '103', '317')
#: 경로 탈출 · 모르는 이름 — 전부 404 여야 한다
BAD_PATHS = (
    '/worklog/20261108',                      # 형식은 맞지만 파일 없음
    '/worklog/weekly_report_20261101',        # 날짜 키가 아닌 이름
    '/worklog/weekly_20261101',
    '/worklog/20261101.md',
    '/worklog/2026-11-01',
    '/worklog/..%2F..%2FCLAUDE.md',
    '/worklog/%2e%2e%2f%2e%2e%2fCLAUDE.md',
    '/worklog/..%2f..%2fwebapp%2fapp.py',
    '/worklog/20261101%2F..%2F..%2FCLAUDE.md',
    '/worklog/../../CLAUDE.md',
    '/worklog/20261101/../../../CLAUDE.md',
    '/worklog/%00',
)
#: 탈출이 성공했다면 보일 글 (CLAUDE.md 첫 줄 · app.py 의 Flask 객체 줄)
LEAK_MARKERS = ('# Project conventions for Claude Code sessions', 'app = Flask(')

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


def _sidebar_worklog_text(html):
    """base.html 사이드바의 /worklog 링크 글 (없으면 None)."""
    m = re.search(r'<a href="/worklog"[^>]*>(.*?)</a>', html, re.S)
    return m.group(1) if m else None


def main():
    import app as webapp
    c = webapp.app.test_client()

    # ══ 1) 목록 — 이번 주 리포트가 최신으로 뜬다 ══
    r = c.get('/worklog')
    chk('① /worklog 200', r.status_code == 200)
    html = r.get_data(as_text=True)
    ents = webapp._worklog_entries()
    #  ⚠ "맨 위" 가 아니라 "목록에 있다" 로 본다 — 다음 주 리포트가 들어오면 이 주는 둘째가 된다 (순서는 ⑥ 이 본다)
    me = next((e for e in ents if e.get('key') == KEY), {})
    chk('② 이번 주 (20261101) 가 목록에 있다', me.get('key') == KEY)
    chk('③ 종류 = 주간 리포트 (docs/worklog)', me.get('kind') == '주간 리포트')
    chk('④ 목록 제목 = 리포트 머리 # 줄', me.get('title') == TITLE)
    chk('⑤ 목록에 /worklog/20261101 링크 · 제목', f'/worklog/{KEY}' in html and TITLE in html)
    chk('⑥ 목록 순서 = 날짜 키 내림차순 (앞으로 오는 주차도 자동으로 위에)',
        [e['key'] for e in ents] == sorted((e['key'] for e in ents), reverse=True))

    # ══ 2) 본문 ══
    r2 = c.get(f'/worklog/{KEY}')
    chk('⑦ /worklog/20261101 200', r2.status_code == 200)
    body = r2.get_data(as_text=True)
    chk('⑧ 제목이 본문에', TITLE in body)
    for n in NUMBERS:
        chk(f'⑨ 숫자 {n!r} 가 본문에', n in body)
    for sec in ('다음 주', '사용자가 정할 것', '예상 질문'):
        chk(f'⑩ 절 {sec!r} 가 본문에', sec in body)
    chk('⑪ 그림 = 인라인 SVG (<figure> · <svg>)', '<figure' in body and '<svg' in body)
    chk('⑫ 날짜 메타 2026-11-01', '2026-11-01' in body)

    # ══ 3) 사이드바 — 주간보고 이름으로 찾을 수 있다 ══
    side = _sidebar_worklog_text(body)
    chk('⑬ 사이드바에 /worklog 링크', side is not None)
    chk('⑭ 그 링크 글에 "주간보고"', side is not None and '주간보고' in side)
    side_idx = _sidebar_worklog_text(html)
    chk('⑮ 목록 페이지에서도 같은 링크 · 활성 표시',
        side_idx is not None and '주간보고' in side_idx
        and re.search(r'<a href="/worklog" class="active"', html) is not None)

    # ══ 4) 모르는 이름 · 경로 탈출 = 404 · 새는 글 없음 ══
    for p in BAD_PATHS:
        rr = c.get(p)
        txt = rr.get_data(as_text=True)
        chk(f'⑯ 거부 {p} → 404', rr.status_code == 404)
        chk(f'⑰ 새는 글 없음 {p}', not any(m in txt for m in LEAK_MARKERS))

    # ══ 5) 창구가 고르는 파일 = 8 자리 키 · 두 폴더 안 ══
    roots = [os.path.realpath(webapp._repo_path(d)) for d in ('docs/worklog', 'docs/seminar')]
    scan = webapp._worklog_scan()
    chk('⑱ 모든 키 = 8 자리 숫자', all(re.fullmatch(r'\d{8}', k) for k in scan))
    chk('⑲ 모든 파일 = docs/worklog · docs/seminar 안',
        all(any(os.path.realpath(p).startswith(rt + os.sep) for rt in roots) for p, _k in scan.values()))

    # ══ 6) 원문 — 렌더가 |safe 라 스크립트 · 이벤트 속성이 없어야 한다 ══
    src_path = os.path.join(webapp._repo_path('docs/worklog'), f'weekly_{KEY}.md')
    src = ''
    if os.path.isfile(src_path):
        with open(src_path, encoding='utf-8') as f:
            src = f.read()
    chk('⑳ 원문 파일 있음', bool(src))
    chk('㉑ 원문에 <script · javascript: · 태그 안 on*= 속성 없음',
        bool(src) and not re.search(r'<\s*script|javascript:|<[a-z][^<>\n]*\son[a-z]+\s*=', src, re.I))

    print(f'worklog weekly 20261101 SELFTEST {_ok}/{_ok + len(_fail)}',
          'PASS' if not _fail else 'FAIL ' + repr(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
