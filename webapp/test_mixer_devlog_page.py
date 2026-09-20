#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 개발 이력(/mixer) 페이지 회귀 — 인덱스·버전 순서·두 절·redact 관문.

  python3 webapp/test_mixer_devlog_page.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


def main():
    import app as webapp
    import ledger_view
    c = webapp.app.test_client()
    r = c.get('/mixer')
    chk('① /mixer 200', r.status_code == 200)
    html = r.get_data(as_text=True)
    ents = webapp._mixer_devlog_entries()
    chk('② 버전이 하나 이상 잡힌다', len(ents) >= 1)
    chk('③ 최신 버전이 앞 (키 내림차순)',
        [e['key'] for e in ents] == sorted((e['key'] for e in ents), reverse=True))
    chk('④ 모든 버전에 쉬운 판·자세한 판이 둘 다 비어 있지 않다',
        all(e['easy_html'].strip() and e['detail_html'].strip() for e in ents))
    chk('⑤ 그림이 /static/mixer/ 경로로 들어 있고 실제 파일이 있다',
        any('/static/mixer/' in e['easy_html'] for e in ents)
        and all(os.path.exists(webapp._repo_path('webapp/static/mixer/' + fn))
                for fn in {p.split('/static/mixer/')[1].split('"')[0]
                           for e in ents for p in e['easy_html'].split('src=')[1:] if '/static/mixer/' in p}))
    chk('⑥ 페이지에 토글과 타임라인이 있다', 'mx-toggle' in html and 'mx-timeline' in html)
    chk('⑦ 메뉴에 /mixer 링크', 'href="/mixer"' in html)
    #  redact 관문 — markdown 변환 전에 실제로 호출되는가 (표지 문자열 주입)
    _orig = ledger_view.redact
    ledger_view.redact = lambda t: _orig(t) + '\n\nMXREDACTMARK\n'
    try:
        ents2 = webapp._mixer_devlog_entries()
        chk('⑧ 렌더 직전 ledger_view.redact 를 통과한다', all('MXREDACTMARK' in e['detail_html'] for e in ents2))
    finally:
        ledger_view.redact = _orig
    chk('⑨ 파일명 정규식 밖은 무시된다 (vNN_YYYYMMDD.md 만)',
        all(len(e['key']) == 2 and len(e['date']) == 10 for e in ents))
    print(f'\ntest_mixer_devlog_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 1 if _fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
