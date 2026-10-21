#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint 설명 페이지 회귀 — 웹앱 정적 페이지 + 사이드바 링크 (1저자 10-21 *"이것도 dem webapp에 추가해줭"*).

`webapp/app.py` 는 봉인 32 (`scripts/run_network_194_parallel.py` CODE_FILES) 라 라우트를 새로 만들 수 없다.
그래서 설명 페이지는 Flask 기본 정적 폴더 (`webapp/static/`) 에 두고, 사이드바 (`templates/base.html` · 봉인 밖)
에서 링크한다.  이 시험이 지키는 것:

  ① 파일이 그 자리에 있고 한 파일로 닫혀 있다 (스크립트 · 외부 자원 없음 — 오프라인 · 인증 면제 경로라도 새는 것 없음)
  ② 그림 6 장 · "처음 보는 분께" · CONTACT_FREE · "독립 holdout 검증 아님" 표지가 남아 있다
  ③ α = **열린 면적 비율 (개구율)** — v1 의 거꾸로 쓴 문장 ("가리는 비율 α") 이 다시 들어오지 않는다
  ④ 보이는 글에 천 단위 콤마가 없다 (보고자료 작성 원칙 · `docs/report_making_principles.md`)
  ⑤ 웹앱으로 돌아가는 링크 (`href="/"`)
  ⑥ 사이드바 (base.html) 에 링크가 있고, 실제 앱이 그 경로를 200 · text/html 로 서빙하며 렌더된 화면에 링크가 보인다
  ⑦ 핵심 수치가 정본 그대로 (SBE 1.63 · DBE 4.68 mS/cm · σ* 0.347 · DBE 단독 2.618 S/cm)

  python3 webapp/test_rint_explainer_page.py
"""
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PAGE_URL = '/static/explain/rint_overview_20261021.html'
PAGE = os.path.join(HERE, 'static', 'explain', 'rint_overview_20261021.html')
BASE = os.path.join(HERE, 'templates', 'base.html')

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


_VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
         'source', 'track', 'wbr'}


class _Scan(HTMLParser):
    """태그 짝 · 보이는 글 · 금지 요소를 한 번에 본다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.unbalanced, self.text = [], [], []
        self.scripts, self.ext = 0, []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script':
            self.scripts += 1
        for k in ('src', 'href'):
            v = (a.get(k) or '').strip().lower()
            if v.startswith(('http:', 'https:', '//')):
                self.ext.append(f'{tag} {k}={v}')
        if tag in ('style', 'script'):
            self._skip += 1
        if tag not in _VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        for k in ('src', 'href'):
            v = (a.get(k) or '').strip().lower()
            if v.startswith(('http:', 'https:', '//')):
                self.ext.append(f'{tag} {k}={v}')

    def handle_endtag(self, tag):
        if tag in ('style', 'script'):
            self._skip = max(0, self._skip - 1)
        if tag in _VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.unbalanced.append(tag)

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def main():
    print('── ① 파일 · 한 파일로 닫힘')
    exists = os.path.isfile(PAGE)
    chk('정적 파일이 webapp/static/explain/ 에 있다', exists)
    src = open(PAGE, encoding='utf-8').read() if exists else ''
    sc = _Scan()
    sc.feed(src)
    sc.close()
    chk('<title> 이 있다', bool(re.search(r'<title>[^<]+</title>', src)))
    chk('태그 짝이 맞다 (닫히지 않은 · 엇갈린 태그 0)', exists and not sc.stack and not sc.unbalanced)
    chk('<script> 없음', exists and sc.scripts == 0)
    chk('외부 자원 (http · https · //) 없음', exists and not sc.ext)
    text = ' '.join(sc.text)

    print('── ② 내용 표지')
    chk('그림 6 장 (<figure>)', src.count('<figure') == 6)
    chk('그림마다 설명 (svg role="img" + aria-label)',
        src.count('<svg') >= 6 and src.count('role="img"') >= 6 and src.count('aria-label=') >= 6)
    chk('"처음 보는 분께" 상자', '처음 보는 분께' in text)
    chk('CONTACT_FREE (지금 복셀 σ 의 빈틈) 설명', 'CONTACT_FREE' in text)
    chk('DBE 비교는 "독립 holdout 검증 아님" 표지', 'holdout' in text and '아님' in text)
    chk('용어 칸 holdout 풀이 = DBE 4.68 은 현 세대 보정에 쓰였으므로 여기서 holdout 이 아니다 (사전 리뷰 10-21 PRE-design-07)',
        bool(re.search(r'<td>holdout</td><td>[^<]*DBE 4\.68[^<]*현 세대 보정[^<]*holdout 이 아니다', src)))

    print('── ③ α = 열린 면적 비율 (개구율)')
    chk('거꾸로 쓴 문장 ("가리는 비율 α") 없음', exists and '가리는 비율 α' not in text)
    chk('α 를 열린 비율 · 개구율로 적는다', '열린 비율 α' in text and '개구율' in text)

    print('── ④ 천 단위 콤마 없음 (보이는 글)')
    commas = sorted(set(re.findall(r'\d{1,3}(?:,\d{3})+(?![\d])', text)))
    chk(f'보이는 글의 천 단위 콤마 0 (찾은 것 {commas})', exists and not commas)

    print('── ⑤ 웹앱으로 돌아가는 링크')
    chk('href="/" (DEM/MPM Analyzer 로)', 'href="/"' in src)

    print('── ⑦ 핵심 수치 (정본 그대로)')
    for num, what in (('1.63', 'SBE 실측 mS/cm'), ('4.68', 'DBE 실측 mS/cm'),
                      ('0.347', '현 세대 σ* S/cm'), ('2.618', 'DBE 단독 보정 S/cm')):
        chk(f'{what} {num}', num in text)

    print('── ⑥ 사이드바 링크 · 실제 서빙')
    base = open(BASE, encoding='utf-8').read()
    chk('base.html 사이드바에 링크', f'href="{PAGE_URL}"' in base)
    import app as webapp
    c = webapp.app.test_client()
    r = c.get(PAGE_URL)
    chk(f'GET {PAGE_URL} → 200', r.status_code == 200)
    chk('text/html 로 서빙', r.status_code == 200 and (r.mimetype or '') == 'text/html')
    body = r.get_data(as_text=True) if r.status_code == 200 else ''
    chk('서빙된 바이트 = 리포 파일', exists and r.status_code == 200 and body == src)
    r2 = c.get('/seminar')
    page2 = r2.get_data(as_text=True)
    chk('렌더된 화면 (/seminar) 사이드바에 링크가 보인다',
        r2.status_code == 200 and f'href="{PAGE_URL}"' in page2)

    print(f'\n== test_rint_explainer_page: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('   실패: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
