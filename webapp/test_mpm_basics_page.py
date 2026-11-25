#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MPM 쉬운 설명 + 우리 MPM Q&A 페이지 회귀 (1저자 11-16 *"이 내용 MPM으로 웹앱에 넣어줘용 잘 크롭해서"* ·
*"우리 누적되어 있던 Q 관련해서도 Q&A 형식으로 쌓아놓으면 좋을듯"*).

`webapp/app.py` 는 봉인 32 라 라우트를 새로 만들 수 없다 → 정적 페이지 (`webapp/static/explain/`) + 사이드바 링크
(`templates/base.html` · 봉인 밖).  이 시험이 지키는 것:

  ① 한 파일로 닫혀 있다 — 스크립트 · 외부 자원 없음 · 그림은 mpm_basics_figs/ 의 두 PNG 뿐
  ② 그림 두 장이 있고 PNG 실제 크기 = img 의 width · height · alt 글이 있다
  ③ 보이는 글에 천 단위 콤마가 없다 (보고자료 작성 원칙 · docs/report_making_principles.md)
  ④ 웹앱으로 돌아가는 링크 (href="/") · 페이지 안 #링크 = 실제 id
  ⑤ 1저자 원 설명의 개인 호칭이 없고, 원 설명의 출처 표기는 '확인하지 않았다' 표지와 함께 있다
  ⑥ Q&A — q1 … qN 이 빈틈 없이 차례로 · 질문마다 번호 · 질문 · 날짜 · 답 · 근거 줄
  ⑦ 핵심 수치가 기록 그대로 (R1 1.13 % · 14.5 %p · K 25.5 GPa · B₀ 26.23 · FAM 25.842 · 29.491 · f 0.6703 · 0.8085 ·
     d_h/dx 3.5 · 랩 표준 1.64 · 10–13 %)
  ⑧ 원장 (docs/reviews/claims.json) 인용 금지 목록의 글이 하나도 없다 · 'Minnmann' 이름도 없다 (CL-94 출처 철회)
  ⑨ 페이지가 가리키는 docs/ · scripts/ 경로가 리포에 실제로 있다
  ⑩ 색 토큰 = 밝은 :root · 어두운 (media · data-theme) 셋 다 · 두 어두운 같음 · 어두운 ≠ 밝은
  ⑪ 사이드바 (base.html) 에 링크 · 실제 앱이 200 · text/html 로 서빙 · 서빙 바이트 = 리포 파일 · 렌더된 화면에 링크

  python3 webapp/test_mpm_basics_page.py
"""
import json
import os
import re
import struct
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

PAGE_URL = '/static/explain/mpm_basics_20261116.html'
PAGE = os.path.join(HERE, 'static', 'explain', 'mpm_basics_20261116.html')
FIGDIR = os.path.join(HERE, 'static', 'explain', 'mpm_basics_figs')
FIGS = ('mpm_material_point_before_after.png', 'mpm_p2g_g2p_cycle.png')
BASE = os.path.join(HERE, 'templates', 'base.html')
CLAIMS = os.path.join(ROOT, 'docs', 'reviews', 'claims.json')

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


class _Scan(HTMLParser):
    """보이는 글 · 태그 · 속성을 한 번에 모은다 (style · head 안 글은 보이는 글에서 뺀다)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.tags = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag in ('style', 'script', 'title'):
            self._skip += 1

    def handle_startendtag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_endtag(self, tag):
        if tag in ('style', 'script', 'title') and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def _png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', head[16:24])


def _css_block(src, rx):
    m = re.search(rx, src, re.S)
    return m.group(1) if m else ''


def _tok(block, name):
    m = re.search(re.escape(name) + r'\s*:\s*([^;}]+)', block)
    return m.group(1).strip() if m else None


def main():
    print('── ① 한 파일 · 외부 자원 없음')
    exists = os.path.isfile(PAGE)
    chk('페이지 파일이 있다', exists)
    src = open(PAGE, encoding='utf-8').read() if exists else ''
    sc = _Scan()
    sc.feed(src)
    vis = re.sub(r'\s+', ' ', ''.join(sc.text))
    chk('<script> 없음', not any(t == 'script' for t, _ in sc.tags))
    ext = [a.get(k) for t, a in sc.tags for k in ('src', 'href')
           if a.get(k) and re.match(r'^(?:[a-z]+:)?//', a.get(k), re.I)]
    chk(f'외부 (http · //) 자원 · 링크 없음 {ext}', not ext)
    chk('<link> 태그 없음 (외부 글꼴 · 스타일 없음)', not any(t == 'link' for t, _ in sc.tags))
    imgs = [a for t, a in sc.tags if t == 'img']
    chk('img 는 둘이고 mpm_basics_figs/ 의 두 그림뿐',
        sorted(a.get('src', '') for a in imgs) == sorted(f'mpm_basics_figs/{f}' for f in FIGS))

    print('── ② 그림 두 장 · 크기 · alt')
    for f in FIGS:
        p = os.path.join(FIGDIR, f)
        sz = _png_size(p) if os.path.isfile(p) else None
        tag = next((a for a in imgs if a.get('src') == f'mpm_basics_figs/{f}'), {})
        chk(f'{f} 있음 · PNG', sz is not None)
        chk(f'{f} 실제 크기 {sz} = img width · height',
            sz is not None and (str(sz[0]), str(sz[1])) == (tag.get('width'), tag.get('height')))
        chk(f'{f} alt 글 (20 자 이상)', len((tag.get('alt') or '').strip()) >= 20)

    print('── ③ 천 단위 콤마 없음')
    commas = re.findall(r'\d,\d{3}', vis)
    chk(f'보이는 글에 1,234 꼴 없음 {commas[:5]}', not commas)

    print('── ④ 돌아가는 링크 · 페이지 안 링크')
    hrefs = [a.get('href') for t, a in sc.tags if t == 'a' and a.get('href')]
    chk('웹앱으로 돌아가는 링크 href="/"', '/' in hrefs)
    ids = {a.get('id') for _, a in sc.tags if a.get('id')}
    dangling = sorted({h[1:] for h in hrefs if h.startswith('#')} - ids)
    chk(f'#링크 대상 id 가 모두 있다 {dangling}', not dangling)

    print('── ⑤ 개인 호칭 없음 · 출처 표기 한정')
    chk('개인 호칭 ("용짱") 없음', '용짱' not in src)
    chk('원 설명 출처 표기 + "확인하지 않았다" 표지',
        '출처 표기' in vis and '확인하지 않았다' in vis and 'math.unm.edu' in vis)
    chk('그림 캡션 = 개념도 · 해석 결과 아님 (둘 다)', vis.count('해석 결과 아님') >= 2)

    print('── ⑥ Q&A 구조')
    qids = re.findall(r'<details class="qa" id="q(\d+)">', src)
    nums = [int(x) for x in qids]
    chk(f'Q&A {len(nums)} 개 (≥ 20) · q1 … qN 빈틈 없이 차례로', len(nums) >= 20 and nums == list(range(1, len(nums) + 1)))
    blocks = re.findall(r'<details class="qa" id="q\d+">(.*?)</details>', src, re.S)
    chk('Q&A 블록 수 = id 수', len(blocks) == len(nums))
    bad = []
    for i, b in enumerate(blocks, 1):
        ok = (f'<span class="qno">Q{i}</span>' in b and '<span class="qt">' in b
              and re.search(r'<span class="qd">\d\d-\d\d', b) and '<div class="ans">' in b
              and '<p class="src">근거:' in b)
        if not ok:
            bad.append(i)
    chk(f'질문마다 번호 · 질문 · 날짜 · 답 · 근거 줄 {bad}', not bad)
    chk('1저자 결정 기록표 (바. 묶음) 가 있다', 'id="qa-f"' in src and '1저자 결정 기록' in vis)

    print('── ⑦ 핵심 수치 = 기록 그대로')
    want = ('1.13 %', '14.5 %p', '25.5 GPa', '26.23', '25.842', '29.491', '0.6703', '0.8085',
            'd_h/dx ≳ 3.5', '1.64 g/cm³', '10–13 %', '1.53 GPa', 'ν 0.49', '0.30 GPa')
    miss = [w for w in want if w not in vis]
    chk(f'핵심 수치 전부 {miss}', not miss)

    print('── ⑧ 인용 금지 글 없음')
    claims = json.load(open(CLAIMS, encoding='utf-8'))
    pats = []
    for e in claims.get('quotation_ban') or []:
        p = (e.get('pattern') or e.get('text')) if isinstance(e, dict) else e
        if p:
            pats.append(p)
    hit = [p for p in pats if p in src]
    chk(f'claims.json 인용 금지 {len(pats)} 글 중 들어간 것 없음 {hit}', len(pats) >= 10 and not hit)
    chk("'Minnmann' 이름 없음 (CL-94 출처 철회)", 'Minnmann' not in src)

    print('── ⑨ 가리킨 경로가 리포에 있다')
    paths = sorted(set(re.findall(r'<code>((?:docs|scripts|webapp)/[^<\s]+)</code>', src)))
    missing = [p for p in paths if not os.path.exists(os.path.join(ROOT, p.rstrip('/')))]
    chk(f'경로 {len(paths)} 개 모두 있음 {missing}', len(paths) >= 10 and not missing)

    print('── ⑩ 색 토큰 (밝은 · 어두운 둘)')
    light = _css_block(src, r':root\{([^}]*)\}')
    dmed = _css_block(src, r'@media \(prefers-color-scheme: dark\)\{:root:not\(\[data-theme="light"\]\)\{([^}]*)\}')
    dattr = _css_block(src, r':root\[data-theme="dark"\]\{([^}]*)\}')
    toks = ('--bg', '--paper', '--ink', '--mut', '--acc', '--line', '--box', '--warn-bg', '--qa')
    trip = {n: (_tok(light, n), _tok(dmed, n), _tok(dattr, n)) for n in toks}
    chk(f'토큰 {len(toks)} 개 = 밝은 · 어두운 둘 다 정의 · 어두운 둘 같음 · 어두운 ≠ 밝은',
        all(l_ and m_ and a_ and m_ == a_ and m_ != l_ for l_, m_, a_ in trip.values()))
    chk('body 배경 = 토큰', re.search(r'body\{[^}]*background:var\(--bg\)', src) is not None)

    print('── ⑪ 사이드바 링크 · 실제 서빙')
    base = open(BASE, encoding='utf-8').read()
    #  11-25 — 사이드바 줄의 집이 base.html → 트랙 표 (webapp/track_pages.py · base.html 이 TRACK_NAV 로 그린다 · 시험 webapp/test_track_reports.py).
    #  지키는 것은 같다: 사이드바에 이 페이지 줄이 있다 · 그 줄의 출처 주석이 이 시험을 가리킨다 (주석도 표로 옮겼다).
    import track_pages as _tp
    tp_src = open(os.path.join(HERE, 'track_pages.py'), encoding='utf-8').read()
    chk('사이드바 (트랙 표 · base.html 이 그린다) 에 링크',
        'TRACK_NAV' in base and any(p['url'] == PAGE_URL for t in _tp.TRACKS for p in t['pages']))
    chk('사이드바 줄 주석 (트랙 표) 에 이 시험 이름', 'webapp/test_mpm_basics_page.py' in tp_src)
    import app as webapp
    c = webapp.app.test_client()
    r = c.get(PAGE_URL)
    chk(f'GET {PAGE_URL} → 200', r.status_code == 200)
    chk('text/html 로 서빙', r.status_code == 200 and (r.mimetype or '') == 'text/html')
    body = r.get_data(as_text=True) if r.status_code == 200 else ''
    chk('서빙된 바이트 = 리포 파일', exists and r.status_code == 200 and body == src)
    for f in FIGS:
        rf = c.get(f'/static/explain/mpm_basics_figs/{f}')
        chk(f'그림 서빙 200 · image/png ({f})', rf.status_code == 200 and (rf.mimetype or '') == 'image/png')
        rf.close()
    r2 = c.get('/seminar')
    page2 = r2.get_data(as_text=True)
    chk('렌더된 화면 (/seminar) 사이드바에 링크가 보인다', r2.status_code == 200 and f'href="{PAGE_URL}"' in page2)

    print(f'\n== test_mpm_basics_page: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('   실패: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
