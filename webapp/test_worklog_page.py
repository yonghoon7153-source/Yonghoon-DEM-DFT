#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""작업일지(worklog) 페이지 회귀 — 인덱스·렌더·경로탈출 거부.

`/worklog` 은 docs/seminar/weekly_YYYYMMDD_slide_text.md 를 링크로 모아 HTML 로 렌더한다.
키는 **8자리 날짜만** 허용 → 파일명이 `weekly_<key>_slide_text.md` 로 완전히 결정되므로
임의 파일 열람으로 번지지 않는다.  인용 금지값 누수는 --ban-sweep 이 따로 막는다(여기 검사 아님).

  python3 webapp/test_worklog_page.py
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
    c = webapp.app.test_client()

    # ══ 1) 인덱스 ══
    r = c.get('/worklog')
    chk('① /worklog 200', r.status_code == 200)
    html = r.get_data(as_text=True)
    ents = webapp._worklog_entries()
    chk('② weekly 슬라이드텍스트가 하나 이상 잡힌다', len(ents) >= 1)
    chk('③ 최신순 정렬 (키 내림차순)',
        [e['key'] for e in ents] == sorted((e['key'] for e in ents), reverse=True))
    chk('④ 인덱스에 /worklog/<key> 링크가 렌더된다',
        all(f"/worklog/{e['key']}" in html for e in ents) and len(ents) >= 1)

    # ══ 2) 렌더 페이지 ══
    #  ⚠ markdown 라이브러리 유무로 렌더 경로가 갈린다: 있으면 리치 HTML(<table> 등),
    #    없으면 안전 폴백(<pre> 이스케이프).  둘 다 정상 — 테스트는 경로에 맞춰 단언한다.
    try:
        import markdown as _md  # noqa: F401
        has_md = True
    except ImportError:
        has_md = False
    if ents:
        key = ents[0]['key']
        r2 = c.get(f'/worklog/{key}')
        chk('⑤ /worklog/<key> 200', r2.status_code == 200)
        body = r2.get_data(as_text=True)
        chk('⑥ 슬라이드 항목(■)이 본문에 렌더된다', '■' in body)
        chk('⑦ 예상 질문 섹션이 본문에 있다', '예상 질문' in body)
        if has_md:
            chk('⑦b (markdown 있음) 표가 <table> 로 렌더된다', '<table>' in body)
            chk('⑦c (markdown 있음) 슬라이드 블록이 <pre> 로 렌더된다', '<pre>' in body)
        else:
            chk('⑦b (markdown 없음) 안전 폴백 <pre> 로 렌더된다', '<pre>' in body)
        chk('⑧ 날짜 메타가 YYYY-MM-DD 로 뜬다',
            f'{key[:4]}-{key[4:6]}-{key[6:8]}' in body)

    # ══ 3) 형식오류·경로탈출 거부 (8자리 날짜만) ══
    for bad in ('abcd', '2026-09-14', '2026091', '202609144', 'app', '__init__'):
        chk(f'⑨ 거부(형식): {bad!r} → 404', c.get(f'/worklog/{bad}').status_code == 404)
    chk('⑩ 유효 형식이나 파일 없음 → 404', c.get('/worklog/19990101').status_code == 404)

    print('worklog page SELFTEST', 'PASS' if not _fail else 'FAIL ' + repr(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
