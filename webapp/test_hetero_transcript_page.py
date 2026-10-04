#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이종기술 회의록 해체 페이지 회귀 — 회의 둘 (09-18 · 10-02) 을 고를 수 있는가 · 회의 종합이 보이는가.

`/hetero/transcript` 는 원래 09-18 회의 하나만 보였다 (경로 상수 하나).  10-02 회의 (음성 336 · 1저자 10-05
*"낱낱이 정리해서 이종기술 관련 원장에"*) 를 넣으면서 회의 키 (8 자리 날짜) 로 고르게 했다 — 키는 등록부
(`app.HETERO_TRANSCRIPTS`) 에 있는 것만 받는다 (모르는 키 = 404 · 조용히 다른 회의를 보이지 않는다).

  python3 webapp/test_hetero_transcript_page.py
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
    reg = getattr(webapp, 'HETERO_TRANSCRIPTS', None)
    chk('① 회의 등록부 HETERO_TRANSCRIPTS 에 09-18 · 10-02 둘', isinstance(reg, dict) and {'20260918', '20261002'} <= set(reg or {}))

    r = c.get('/hetero/transcript?m=20261002')
    h = r.get_data(as_text=True)
    chk('② ?m=20261002 → 200 · 음성 336 · 발화 90 · 계약 통과 문구', r.status_code == 200 and '음성 336' in h
        and '발화 90' in h and '계약 여섯 통과' in h)
    chk('③ 10-02 회의 종합이 화면에 보인다 (논문 둘로 분리 · 정합도 지시 · 논지 물음)',
        '논문 둘로 분리' in h and '정합도 지시' in h and '논지 물음' in h)

    r = c.get('/hetero/transcript?m=20260918')
    h = r.get_data(as_text=True)
    chk('④ ?m=20260918 → 200 · 발화 61 (옛 회의 그대로)', r.status_code == 200 and '발화 61' in h)

    r = c.get('/hetero/transcript')
    h = r.get_data(as_text=True)
    chk('⑤ 키 없음 → 최신 회의 (10-02)', r.status_code == 200 and '음성 336' in h and '발화 90' in h)
    chk('⑥ 회의 고르기 링크 둘 (?m=20260918 · ?m=20261002)', '?m=20260918' in h and '?m=20261002' in h)

    bad = [k for k in ('20991231', '../etc', 'x', '2026100') if c.get('/hetero/transcript?m=' + k).status_code != 404]
    chk(f'⑦ 등록부 밖 키는 404 (조용히 다른 회의를 보이지 않는다) {bad or ""}', not bad)

    r = c.get('/hetero')
    h = r.get_data(as_text=True)
    chk('⑧ /hetero 에 두 회의 링크', r.status_code == 200 and '/hetero/transcript?m=20260918' in h
        and '/hetero/transcript?m=20261002' in h)

    print(f'\ntest_hetero_transcript_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
