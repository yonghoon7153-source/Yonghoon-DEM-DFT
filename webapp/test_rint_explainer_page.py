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
  ⑧ (10-22 · 사전 리뷰 2 회차 · 1저자 *"잘 하이라이트로 저장해두고"* · PF2 F) 쉽게 말하면 상자 ① ② ③ 이 눈에 띄는 상자로 있고
     (하이라이트 색 토큰 = 밝은 · 어두운 화면 둘 다) · 상자 글 = 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` §6 원문 그대로 ·
     핵심 문장 · 날짜 (10-22 · "10-25 판정 목표" 없음 · 10-31 = 주 판정만 · 감도 미완료) · 용어 풀이 "SV 반사실 비" ·
     그림 6 의 남은 길 순서 = 상자 ② 의 바꾼 순서 (PRE2-design-09) · 6 절 목록 끝 항목 · 주석의 등록 R §10-4 문장이 그 자리에
     (PF2 H 변이 MF12 · MF13)

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
PLAN = os.path.join(HERE, '..', 'docs', 'reviews', 'rint2_design_fix_plan_20261021.md')
BOX_MARKS = ('①', '②', '③')

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


class _Boxes(HTMLParser):
    """상자 (`<div class="hl" id="easy-N">`) 마다 보이는 글 · 안쪽 div 는 깊이로 센다 · 블록 요소 경계 = 빈칸 하나 (인라인 경계는 그대로)."""
    BLOCK = {'div', 'p', 'li', 'ul', 'ol', 'h2', 'h3', 'table', 'tr', 'th', 'td', 'pre', 'br'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.boxes, self._cur, self._depth = {}, None, 0

    def handle_starttag(self, tag, attrs):
        if self._cur is not None and tag in self.BLOCK:
            self.boxes[self._cur].append(' ')
        if tag != 'div':
            return
        a = dict(attrs)
        if self._cur is None:
            if 'hl' in (a.get('class') or '').split() and re.fullmatch(r'easy-[123]', a.get('id') or ''):
                self._cur, self._depth = a['id'], 1
                self.boxes[self._cur] = []
            return
        self._depth += 1

    def handle_endtag(self, tag):
        if self._cur is not None and tag in self.BLOCK:
            self.boxes[self._cur].append(' ')
        if tag == 'div' and self._cur is not None:
            self._depth -= 1
            if self._depth == 0:
                self._cur = None

    def handle_data(self, data):
        if self._cur is not None:
            self.boxes[self._cur].append(data)


def _squash(s):
    return ' '.join(s.split())


def plan_box_text(mark):
    """수정 계획 §6 의 상자 (인용 블록 `> **★ 쉽게 말하면 ① …`) → 보이는 글 (markdown 표지 · 표 구분 줄 · 코드 울타리를 빼고 공백 하나로).
    없으면 None."""
    lines = open(PLAN, encoding='utf-8').read().split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith('> **★ 쉽게 말하면 ' + mark):
            out, j = [], i
            while j < len(lines) and lines[j].startswith('>'):
                s = lines[j][1:].strip()
                j += 1
                if s.startswith('```') or (s and re.fullmatch(r'\|?[\s\-:|]+\|?', s)):
                    continue
                if s.startswith('- '):
                    s = s[2:]
                if s.startswith('|'):
                    s = ' '.join(c.strip() for c in s.strip('|').split('|'))
                s = s.replace('**', '').replace('`', '')
                s = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])', r'\1', s)
                out.append(s)
            return _squash(' '.join(out))
    return None


def _css_block(src, rx):
    m = re.search(rx, src)
    return m.group(1) if m else ''


def _tok(block, name):
    m = re.search(r'(?:^|[;{\s])' + re.escape(name) + r'\s*:\s*([^;}]+)', block)
    return m.group(1).strip() if m else None


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

    print('── ⑧ 10-22 결정 상자 ① ② ③ · 날짜 · 다크 모드 · 용어 (PF2 F · PRE2-design-09)')
    bx = _Boxes()
    bx.feed(src)
    bx.close()
    boxes = {k: _squash(''.join(v)) for k, v in bx.boxes.items()}
    chk('상자 셋 — class="hl" 이 정확히 셋 (id easy-1 · easy-2 · easy-3)',
        len(re.findall(r'class="hl"', src)) == 3 and sorted(boxes) == ['easy-1', 'easy-2', 'easy-3'])
    for k, mark in enumerate(BOX_MARKS, 1):
        want, got = plan_box_text(mark), boxes.get(f'easy-{k}', '')
        chk(f'상자 {mark} 머리 = "★ 쉽게 말하면 {mark}"', got.startswith(f'★ 쉽게 말하면 {mark}'))
        chk(f'상자 {mark} 글 = 수정 계획 §6 원문 그대로 (markdown 표지 뺀 글 · 공백 하나로)',
            want is not None and got == want)
    b1, b2, b3 = (boxes.get(f'easy-{k}', '') for k in (1, 2, 3))
    for sent in ('아래 끝 > 문턱 → SV_DEPENDENT', '위 끝 ≤ 문턱 → 표지 없음', '걸치면 SV_UNCHECKED', '숫자는 예시',
                 '못 가른 덩어리가 없는 팔은 두 풀이가 같아 지금처럼 한 값이다'):
        chk(f'상자 ① 핵심 문장 — "{sent}"', sent in b1)
    for sent in ('⑥ 숫자 탐침 (SBE · σ 봉인)', '계획 하나 봉인', '사슬이 계획 해시를 대조 · 다르면 멈춤'):
        chk(f'상자 ② 핵심 문장 — "{sent}"', sent in b2)
    for sent in ('10-31 에는 진행 보고만 한다', '팔을 줄이지 않는 이유', '⑥ 실측 직후를 결정점으로'):
        chk(f'상자 ③ 핵심 문장 — "{sent}"', sent in b3)
    hsec = re.search(r'<section class="hl-sec"[^>]*>\s*<h2[^>]*>(.*?)</h2>', src, re.S)
    chk('상자 묶음 머리에 날짜 10-22', bool(hsec) and '10-22' in re.sub(r'<[^>]+>', '', hsec.group(1)))
    sub = re.search(r'<p class="sub">(.*?)</p>', src, re.S)
    chk('머리 줄 (.sub) 에 "10-22 갱신"', bool(sub) and '10-22 갱신' in sub.group(1))
    stale = [s for s in ('10-25 목표', '일요일 10-25', '(10-25) 목표', '목표: 일요일') if s in src]
    chk(f'"10-25 판정 목표" 낡은 날짜 없음 (보이는 글 · aria-label 모두 · 찾은 것 {stale})', exists and not stale)
    fig6 = re.findall(r'aria-label="(남은 길[^"]*)"', src)
    allt = text + ' ' + ' '.join(fig6)
    for sent in ('10-31', '진행 보고', '감도 미완료', '주 판정'):
        chk(f'남은 길에 등록 R §10-4 · 한정어 ⑰ 표지 — "{sent}"', sent in allt)
    #  ★ 같은 부류 (PF2 H 변이 MF12 · MF13 생존 — 위 검사는 페이지 어디든 그 낱말이 있으면 통과했다) — 6 절의 그 자리에 있는가
    s6 = re.search(r'<h2>6\. 남은 길[^<]*</h2>(.*?)<h2>7\.', src, re.S)
    s6t = s6.group(1) if s6 else ''
    ol6 = re.search(r'<ol>(.*?)</ol>', s6t, re.S)
    items6 = [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<li>(.*?)</li>', ol6.group(1), re.S)] if ol6 else []
    last6 = items6[-1] if items6 else ''
    chk('6 절 목록 끝 항목 (주 판정 자리) = 등록 R §10-4 · 한정어 ⑰ — "10-31 판정 = 주 판정만" · "감도 미완료"',
        '10-31 판정 = 주 판정만' in last6 and '감도 미완료' in last6)
    note6 = re.search(r'<p class="note">(.*?)</p>', s6t, re.S)
    nt6 = re.sub(r'<[^>]+>', '', note6.group(1)) if note6 else ''
    chk('6 절 주석 = 등록 R §10-4 결과 전 문장 — "진행 보고만 한다" · "등록 팔은 줄이지 않는다"',
        '진행 보고만 한다' in nt6 and '등록 팔은 줄이지 않는다' in nt6)
    order = ('S0 단계 1', '⑥ 숫자 탐침', 'Codex 요청', '계획 하나 봉인', 'S0 단계 2', '보정 사다리', '주 판정')
    pos_ok = len(fig6) == 2 and all(all(a in f for a in order) and [f.index(a) for a in order] == sorted(f.index(a) for a in order)
                                    for f in fig6)
    chk('그림 6 (넓은 · 좁은 판) 의 순서 = 상자 ② 바꾼 순서 (S0 1 → ⑥ → Codex → 계획 봉인 → S0 2 → 사다리 → 주 판정)', pos_ok)
    light = _css_block(src, r'(?m)^:root\{([^}]*)\}')
    dmed = _css_block(src, r'@media \(prefers-color-scheme: dark\)\{:root:not\(\[data-theme="light"\]\)\{([^}]*)\}\}')
    dattr = _css_block(src, r':root\[data-theme="dark"\]\{([^}]*)\}')
    toks = {nm: (_tok(light, nm), _tok(dmed, nm), _tok(dattr, nm)) for nm in ('--hl', '--hlb')}
    chk(f'하이라이트 색 토큰 --hl · --hlb = 밝은 :root · 어두운 (media · data-theme) 셋 다 정의 · 어두운 값 ≠ 밝은 값 · 두 어두운 판 같음 {toks}',
        all(l_ and m_ and a_ and m_ == a_ and m_ != l_ for l_, m_, a_ in toks.values()))
    hl_rule = _css_block(src, r'\.hl\{([^}]*)\}')
    chk('.hl 상자 = 하이라이트 배경 var(--hl) · 테두리 var(--hlb)', 'var(--hl)' in hl_rule and 'var(--hlb)' in hl_rule)
    chk('용어 풀이에 "SV 반사실 비"', bool(re.search(r'<td>SV 반사실 비</td><td>[^<]*G_전체 / G_끊음', src)))

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
