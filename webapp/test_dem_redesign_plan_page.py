#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 재설계 계획서: 웹앱 정적 페이지 둘 + docx 정본 회귀 (1저자 11-10
*"계획 브리핑 이것도 웹앱에서 주간보고 처럼 구리게 말고 좀더 계획서 같은 느낌으로 마감성있게 웹앱에 별도 페이지"* ·
*"docx 는 처음 보는 사람 입장에서 써 줘"* · *"이 형식으로도 잘 받아들여서 이걸 웹앱으로도 만들어주고"*).

`webapp/app.py` 는 봉인 32 (`scripts/run_network_194_parallel.py` CODE_FILES) 라 라우트를 새로 만들 수 없다.
그래서 두 페이지는 Flask 기본 정적 폴더 (`webapp/static/explain/`) 에 두고 사이드바 (`templates/base.html` · 봉인 밖)
에서 링크한다.  글은 손으로 베끼지 않는다: 생성기 `scripts/build_dem_redesign_plan.py` 가 원문 둘에서 만든다.

  (a) 계획서      원문 docs/reviews/dem_redesign_direction_20261109/briefing_ko.md
                  → webapp/static/explain/dem_redesign_plan_20261110.html
  (b) 처음 보는 분 원문 docs/reviews/dem_redesign_direction_20261109/plan_newcomer_ko.md
                  → webapp/static/explain/dem_redesign_plan_newcomer_20261110.html
  (c) docx        정본 docs/reviews/dem_redesign_direction_20261109/DEM_redesign_plan_for_newcomers_20261110.docx
                  (1저자가 올린 파일 그대로 · sha256 고정) · 빌더 scripts/build_dem_redesign_plan_docx.js 가 읽는
                  JSON = docs/reviews/dem_redesign_direction_20261109/plan_newcomer_docx_model.json

이 시험이 지키는 것:

  ① 생성기 `--check` 통과 (프로세스 안) · 두 번 만들면 같은 바이트 · 원문을 한 글자 바꾼 사본이면 rc 1 (그 원문의 출력만 바뀜) ·
     낯선 구성 (### · 인용 블록 · 코드 울타리 · 링크 · 3 단 목록 · 표 칸 수 · 마커 … · 수식 · 그림의 어긋난 꼴) 은 줄 번호와 함께
     rc 2 · 수식 캐시와 그림의 한살이 (캐시에 없는 식 = rc 2 · pandoc 이 없으면 --write 도 rc 2 · 낡은 캐시 = rc 1 · 그림 바이트가
     바뀌면 rc 1): 변환기를 가짜로 바꿔 끼워 pandoc 없이 본다
  ② ④ 두 페이지가 한 파일로 닫혀 있다 (script · link · 외부 URL · 이벤트 속성 없음 · 그림은 PNG 를 data URI 로 실은 <img> 뿐 ·
     href 는 "/" · 서로 · #자리 뿐) · 색 토큰 세 블록 (:root · prefers-color-scheme dark · data-theme dark) 이 같은 이름 ·
     body 배경 명시 · 표는 가로 스크롤 상자 · @media print A4 · 처음 링크 · 글꼴 스택 · 보이는 글에 천 단위 콤마 · em dash ·
     모델 이름 · 주소 · 절대 경로 없음
  ③ (a) 계획서 꼴: 표지 머리 (제목 · 원문 부제 · 날짜 · 배지 셋) · 한 줄로 상자 · 번호 절 머리 9 + 참고문헌 · 로드맵 카드 8 (단계 0–7) ·
     일정 · 갈림 칩 (가) (나) (마) (라) (다) · 강조 / 경고 / "하지 않는 말" 상자 · 질문 표 (답 = 원문 "답:" 뒤 글) · Codex 판정 상자
     (DRD-01 · DRD-02) · 번호 서지 10 (litdb slug 10 · DOI) · 원문 줄 전수 포함
  ⑤ (b) docx 꼴: 제목 블록 네 줄 · 지위 · 한 줄로 · 절 12 · 표 6 (머리 행) · 용어 14 · 참고문헌 10 · 원고 줄 전수 포함
  ⑥ docx 정본 = 올린 바이트 (sha256) · 형식 (A4 · 글꼴 · 제목 블록 · Heading1 12 · 목록 문단 46 · 표 6 · 음영 · 바닥글) ·
     원고 줄이 정본 글에 전수 포함 (한 글자 바꾼 사본은 실패) · JSON 의 문단 순서 = 정본의 문단 순서
  ⑦ (a) ↔ (b) 서로 링크 · base.html 사이드바 링크 · 실제 앱이 두 경로를 200 · text/html · 파일과 같은 바이트로 서빙 ·
     렌더된 /seminar 에 링크가 보인다
  ⑧ (node · docx 가 있을 때만) 빌더 출력의 본문 · 스타일 · 번호 · 바닥글 XML 이 정본과 같다 (요소 · 속성 · 글)
  ⑨ 수식 · 그림 고정물 (webapp/test_fixtures/dem_redesign_plan/: 줄 수식 둘 · 글 안 수식 · 분수 · 첨자 · 합 기호 · 작은 PNG):
     그 원고 조각으로 페이지 · JSON 을 만들면 (pandoc 없이 · 커밋된 수식 캐시에서) 페이지에 <math> (MathML · LaTeX 주석 = 원고) 와
     <figure> (PNG 바이트 = 파일 · 캡션 아래 가운데) 가 있고, (node · docx 가 있을 때) docx 의 document.xml 에 Word 수식
     (m:oMath · m:oMathPara · m:f · m:sSub · m:nary) 과 그림 관계 (media/…png · 크기 = 본문 폭의 60 %) 가 있다 ·
     수식 아닌 것이 섞인 변환은 생성기가 거부한다 · (pandoc 3.1.3 이 있을 때) 캐시를 처음부터 다시 만들면 같은 바이트

원고가 바뀌면 고칠 곳: 원고 (b) 를 고쳐 쓰고 정본 docx 를 바꾸면 (절차 = 빌더 머리 주석) 이 파일의 DOCX_SHA256 과 SHAPE 묶음
(절 · 표 · 용어 · 참고문헌 · DOI · 정본 문단 수) 을 같이 고친다.  ⑤ ⑥ 의 "원고 핵심" 줄들 (제목 블록 글 · 첫 문장 · 낱말) 은 지금
원고의 못이다: 그 글을 바꿨다면 같이 고친다.  수식 · 그림을 더하면 정본과 SHAPE 의 문단 수가 바뀔 뿐, 수식 · 그림의 수는
적어 둘 곳이 없다 (원고에서 세어 페이지 · 정본 · JSON 과 견준다).

  python3 webapp/test_dem_redesign_plan_page.py
"""
import base64
import contextlib
import hashlib
import html as html_lib
import importlib
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

SRC_PLAN = 'docs/reviews/dem_redesign_direction_20261109/briefing_ko.md'
SRC_NEW = 'docs/reviews/dem_redesign_direction_20261109/plan_newcomer_ko.md'
OUT_PLAN = 'webapp/static/explain/dem_redesign_plan_20261110.html'
OUT_NEW = 'webapp/static/explain/dem_redesign_plan_newcomer_20261110.html'
OUT_MODEL = 'docs/reviews/dem_redesign_direction_20261109/plan_newcomer_docx_model.json'
DOCX = 'docs/reviews/dem_redesign_direction_20261109/DEM_redesign_plan_for_newcomers_20261110.docx'
#: 1저자가 11-10 에 올린 docx 그대로 (형식 기준 · 고치지 않는다).  원고가 바뀌어 빌더로 다시 만들어 정본을 바꾸면 이 값도 같이 바꾼다
#: (절차 = scripts/build_dem_redesign_plan_docx.js 머리 주석).
DOCX_SHA256 = '2d7a34d2d9c5bf78333f9f7e01aa6ac63663bd200065017991ab44d2c4e61b91'
#: 원고에 수식이 있을 때만 생기는 생성물 (LaTeX → MathML · OMML 변환 캐시 · 원고 옆)
NEW_MATH = SRC_NEW[:-3] + '_math.json'
#: 수식 · 그림 고정물 (짧은 원고 조각 · 작은 PNG · 그 수식 캐시).  고정물로 만든 HTML · docx 는 커밋하지 않고 시험이 그때 만든다.
FIX_MD = 'webapp/test_fixtures/dem_redesign_plan/fixture_ko.md'
FIX_PNG = 'webapp/test_fixtures/dem_redesign_plan/fig_grid.png'
FIX_MATH = FIX_MD[:-3] + '_math.json'
#: 수식 캐시를 만든 pandoc 의 판.  이 판이 깔려 있을 때만 "캐시를 처음부터 다시 만들면 같은 바이트" 를 본다 (다른 판은 건너뜀).
PANDOC_VERSION = '3.1.3'
#: 지금 원고 (plan_newcomer_ko.md) 와 정본 docx 의 수.  원고를 고쳐 정본을 바꾸면 (절차 = 빌더 머리 주석) DOCX_SHA256 과 이 묶음을
#: 같이 고친다.  절 · 표 · 수식 · 그림이 페이지 · 정본에 그대로 실렸는지는 아래 검사가 원고에서 직접 세어 견준다: 이 수들은
#: "지금 몇 개인가" 의 못이다 (원고가 뜻하지 않게 줄어든 것을 잡는다).
SHAPE = {
    'sections': 12,             # 절 제목 (1–11 + 참고문헌)
    'tables': 6,
    'glossary_rows': 14,
    'ref_rows': 10,
    'dois': 7,
    'docx_paragraphs': 212,     # 정본 본문의 글 있는 문단 (표 안 포함)
    'docx_list_paragraphs': 46,
}
GEN = 'scripts/build_dem_redesign_plan.py'
BUILDER = 'scripts/build_dem_redesign_plan_docx.js'
URL_PLAN = '/static/explain/dem_redesign_plan_20261110.html'
URL_NEW = '/static/explain/dem_redesign_plan_newcomer_20261110.html'
BASE = 'webapp/templates/base.html'
TITLE = 'DEM 재설계 (수영) 계획서'
FONT_STACK = '"Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif'

#: 모델 이름 · ID (커밋 꼬리 밖에서는 쓰지 않는다) · 주소 · 포트 · user@host · 절대 경로 (리포에 적지 않는다)
RE_MODEL = re.compile(r'\b(?:opus|sonnet|haiku|fable)\b|claude-[a-z0-9]|anthropic', re.I)
RE_ADDR = re.compile(r'(?<![\d.])\d{1,3}(?:\.\d{1,3}){3}(?![\d.])|\blocalhost\b'
                     r'|(?<![0-9]):\d{4,5}(?![0-9])|\b[\w.-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b')
RE_ABS = re.compile(r'(?:/home/|/root/|/tmp/|/mnt/|/Users/|[A-Za-z]:\\)')
EM_DASH = chr(0x2014)
NEW_DIR = posixpath.dirname(SRC_NEW)
#: PNG 의 머리 (서명 + IHDR 의 앞 · 10 x 10): 그림 크기 상한 반례에 쓴다 (그 뒤에 바이트를 덧붙여 상한을 넘긴다)
PNG_HEAD = bytes([0x89]) + b'PNG' + bytes([13, 10, 26, 10, 0, 0, 0, 13]) + b'IHDR' + bytes([0, 0, 0, 10, 0, 0, 0, 10])
#: PNG 가 아닌 파일 (GIF 서명).  크기 자리 (16–24 번째 바이트) 는 멀쩡한 값 (10 x 10) 이라, 서명을 보지 않는 검사는 이것을 통과시킨다
NOT_PNG = b'GIF89a' + bytes(10) + bytes([0, 0, 0, 10, 0, 0, 0, 10]) + b'0' * 40

_ok, _fail = 0, []


def chk(name, cond):
    """cond 가 함수면 여기서 부른다 (예외 = 실패): 생성물이 아직 없어도 끝까지 세기 위해."""
    global _ok
    try:
        good = bool(cond() if callable(cond) else cond)
    except Exception as e:      # noqa: BLE001: 시험 계수기: 어떤 예외든 그 검사의 실패다
        good = False
        name = f'{name}  [예외 {type(e).__name__}: {str(e)[:80]}]'
    if good:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')
    return good


def _p(rel, root=ROOT):
    return os.path.join(root, *rel.split('/'))


def _read(rel, root=ROOT):
    try:
        with open(_p(rel, root), encoding='utf-8', newline='') as f:
            return f.read()
    except OSError:
        return ''


def _bytes(rel, root=ROOT):
    try:
        with open(_p(rel, root), 'rb') as f:
            return f.read()
    except OSError:
        return b''


def _norm(s):
    return ' '.join(s.split())


# ───────────────────────────── HTML 읽기 ─────────────────────────────
_VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
_BLOCK = {'address', 'article', 'aside', 'blockquote', 'body', 'br', 'caption', 'colgroup', 'dd', 'div', 'dl', 'dt', 'figcaption',
          'figure', 'footer', 'h1', 'h2', 'h3', 'h4', 'head', 'header', 'hr', 'html', 'li', 'main', 'nav', 'ol', 'p', 'section',
          'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'title', 'tr', 'ul'}
#: <img> 는 금지 요소가 아니다: 그림은 PNG 를 data URI 로 페이지 안에 실을 때만 받는다 (그 밖의 src 는 "외부 자원" 으로 잡힌다).
_BANNED_TAGS = {'script', 'link', 'iframe', 'object', 'embed', 'form', 'input', 'button', 'video', 'audio', 'source',
                'base', 'svg', 'canvas', 'picture', 'frame', 'frameset', 'applet'}
_RE_DATA_PNG = re.compile(r'data:image/png;base64,([A-Za-z0-9+/]+=*)')
#: 보이는 글에서 건너뛰는 요소.  수식 (<math>) 은 글이 아니라 식이다: 안의 글자 (식 · LaTeX 주석) 를 보이는 글에 섞지 않고 빈칸 하나로 둔다.
_SKIP_TAGS = ('style', 'script', 'math')


class _Scan(HTMLParser):
    """태그 짝 · 보이는 글 (블록 경계 = 빈칸 · 인라인 경계는 그대로 · 수식 = 빈칸) · 금지 요소 · 링크 · 그림 · 수식을 한 번에 본다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.unbalanced, self.text = [], [], []
        self.banned, self.ext, self.hrefs, self.events, self.ids = [], [], [], [], []
        self.imgs = []          # <img> 마다 속성 dict
        self.styles = self.maths = 0
        self._skip = 0

    def _attrs(self, tag, attrs):
        for k, v in attrs:
            v = (v or '').strip()
            if k.lower().startswith('on'):
                self.events.append(f'{tag} {k}')
            if k in ('src', 'href', 'action', 'data', 'poster', 'srcset'):
                low = v.lower()
                if tag == 'img' and k == 'src':
                    if not _RE_DATA_PNG.fullmatch(v):       # 페이지 안에 실은 PNG 가 아니면 (파일 · 주소) 닫힌 파일이 아니다
                        self.ext.append(f'{tag} {k}={v[:60]}')
                elif low.startswith(('http:', 'https:', '//', 'javascript:', 'data:', 'file:', 'ftp:', 'mailto:')):
                    self.ext.append(f'{tag} {k}={v[:60]}')
            if k == 'href':
                self.hrefs.append(v)
            if k == 'id':
                self.ids.append(v)
        if tag == 'img':
            self.imgs.append(dict((k, (v or '')) for k, v in attrs))

    def handle_starttag(self, tag, attrs):
        if tag in _BANNED_TAGS:
            self.banned.append(tag)
        if tag == 'style':
            self.styles += 1
        if tag == 'math':
            self.maths += 1
        self._attrs(tag, attrs)
        if tag in _BLOCK or tag == 'math':
            self.text.append(' ')
        if tag in _SKIP_TAGS:
            self._skip += 1
        if tag not in _VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        if tag in _BANNED_TAGS:
            self.banned.append(tag)
        self._attrs(tag, attrs)
        if tag in _BLOCK:
            self.text.append(' ')

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
        if tag in _BLOCK or tag == 'math':
            self.text.append(' ')
        if tag in _VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.unbalanced.append(tag)

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def scan(src):
    sc = _Scan()
    sc.feed(src)
    sc.close()
    sc.visible = _norm(''.join(sc.text))
    return sc


def _vis(fragment):
    """HTML 조각의 보이는 글 (블록 경계 = 빈칸 · 공백 하나로)."""
    return scan(fragment).visible


def _section(src, sid):
    m = re.search(r'<section id="%s"[^>]*>(.*?)</section>' % re.escape(sid), src, re.S)
    return m.group(1) if m else ''


def _css(src):
    m = re.search(r'<style>(.*?)</style>', src, re.S)
    return m.group(1) if m else ''


def _css_block(css, rx):
    m = re.search(rx, css)
    return m.group(1) if m else ''


def _toks(block):
    return dict((m.group(1), m.group(2).strip()) for m in re.finditer(r'(--[a-z0-9-]+)\s*:\s*([^;}]+)', block))


# ───────────────────────────── 원문 (markdown) 읽기: 생성기와 따로 ─────────────────────────────
def _md_strip(s):
    """markdown 표지 (** · ` · *기울임*) 를 뺀 글: `σ_y*` 같은 맨 별표는 그대로."""
    s = s.replace('**', '').replace('`', '')
    return re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])', r'\1', s)


def _md_cell(s):
    """표 칸 · 줄의 원문 → 화면 · docx 의 글과 견줄 꼴 (수식 자리는 빈칸 · 표지를 빼고 · 공백 하나로)."""
    return _norm(_md_strip(_RE_INLINE_MATH.sub(' ', s)))


_RE_STEP = re.compile(r'^- \*\*단계 (\d+) (.+?)\*\*(?: \(([^()]+)\))?(?:: (.*)|\.)?$')
_RE_SCHED =re.compile(r'^- \*\*일정\*\* (\[[^\]]+\]): (.*)$')
_RE_Q = re.compile(r'^- \*\*(Q\d+\.)\*\* (.*?)  권고: (.*?)  답: (.*)$')
_RE_LEAD = re.compile(r'^(\s*)(?:- )?\*\*(.+?)\*\*: (.*)$')


#: 글 안 수식 `$…$` (여는 $ 뒤에 빈칸 없음 · 수식 안의 "\$" 는 닫는 표지가 아니다).  그룹 1 = LaTeX.
_RE_INLINE_MATH = re.compile(r'\$(?!\s)((?:\\.|[^$\\])+?)\$')
_RE_FIG_LINE = re.compile(r'^!\[(.*)\]\(([^()\s]+)\)(?:\{width=(\d{1,3})%\})?$')
_MATH_MARK = chr(0)         # 조각 안에서 수식이 있던 자리 (원문에 없는 글자)
_DOLLAR_MARK = chr(1)       # 고정폭 안의 달러 기호를 잠깐 가려 두는 글자


def _mask_code(raw):
    """고정폭 (`…`) 안의 달러 기호는 수식 표지가 아니다 → 수식을 찾기 전에 가려 둔다 (찾은 뒤 되돌린다)."""
    return re.sub(r'`[^`]*`', lambda m: m.group(0).replace('$', _DOLLAR_MARK), raw)


def md_pieces(text, h1_tag=True, ext=False):
    """원문 줄 → 페이지 · docx 에 그대로 있어야 하는 글 조각 [(줄 번호, 조각)] (원문 순서).

    한 줄 = 한 조각이 기본이다.  페이지가 줄을 나눠 싣는 꼴만 조각으로 나눈다:
    제목 줄 ([꼬리표] + 부제) · 표 줄 (칸마다) · 단계 줄 (번호 · 이름 · 괄호 안 · 문장마다) · 일정 줄 · 질문 줄 (질문 · 권고 · 답) ·
    굵은 머리 + ":" 줄 (머리 · 나머지).
    h1_tag=False = 제목 줄의 [꼬리표] 를 뺀다: (b) 와 docx 의 제목 블록은 형식 기준 docx 대로 부제만 싣는다.
    ext=True = 수식 · 그림을 받는 원고 (처음 보는 분용): 줄 수식 블록은 글이 아니라 건너뛰고 (수식은 md_math 로 따로 본다) ·
    그림 줄은 캡션만 글이고 · 글 안 수식 `$…$` 자리에서 조각을 나눈다 (수식은 화면 · docx 에서 글자가 아니라 식이다)."""
    out, in_eq = [], False
    for i, raw in enumerate(text.split('\n'), 1):
        if ext:
            if raw == '$$':
                in_eq = not in_eq
                continue
            if in_eq or (raw.startswith('$$') and raw.endswith('$$') and len(raw) >= 5):
                continue
            mfig = _RE_FIG_LINE.match(raw)
            if mfig:
                raw = mfig.group(1)
            raw = _RE_INLINE_MATH.sub(_MATH_MARK, _mask_code(raw)).replace(_DOLLAR_MARK, '$')
        s = raw.strip()
        if not s or s.startswith('<!--'):
            continue
        if s.startswith('|'):
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                continue
            out.extend((i, _md_strip(c)) for c in cells)
            continue
        if s.startswith('# '):
            m = re.match(r'^# (\[[^\]]+\]) (.+)$', s)
            out.extend(([(i, m.group(1))] if h1_tag else []) + [(i, m.group(2))] if m else [(i, s[2:])])
            continue
        if s.startswith('## '):
            out.append((i, s[3:]))
            continue
        m = _RE_STEP.match(raw)
        if m:
            out.append((i, '단계 ' + m.group(1)))
            out.append((i, _md_strip(m.group(2))))
            if m.group(3):
                out.extend((i, _md_strip(x)) for x in m.group(3).split(' · '))
            if m.group(4):
                out.extend((i, _md_strip(x)) for x in m.group(4).split('  '))
            continue
        m = _RE_SCHED.match(raw)
        if m:
            out.extend([(i, '일정'), (i, m.group(1)), (i, _md_strip(m.group(2)))])
            continue
        m = _RE_Q.match(raw)
        if m:
            out.extend((i, _md_strip(g)) for g in m.groups())
            continue
        m = _RE_LEAD.match(raw)
        if m:
            out.extend([(i, _md_strip(m.group(2))), (i, _md_strip(m.group(3)))])
            continue
        s = re.sub(r'^(?:- |\d+\. )', '', s)
        out.append((i, _md_strip(s)))
    # 수식 자리에서 한 번 더 나눈다 (ext 가 아니면 표지가 없어 그대로) · 한 글자 조각은 버린다 (어디에나 있다)
    cut = [(i, _norm(seg)) for i, p in out for seg in p.split(_MATH_MARK)]
    return [(i, p) for i, p in cut if len(p) >= 2]


def md_math(text):
    """원고의 수식을 원고 순서대로 [(줄 수식인가, LaTeX)] (겹치는 식도 나오는 만큼).  생성기와 따로 읽는다."""
    out, block = [], None
    for raw in text.split('\n'):
        if raw == '$$':
            if block is None:
                block = []
            else:
                out.append((True, '\n'.join(block)))
                block = None
            continue
        if block is not None:
            block.append(raw)
            continue
        if raw.startswith('$$') and raw.endswith('$$') and len(raw) >= 5:
            out.append((True, raw[2:-2].strip()))
            continue
        out.extend((False, m.group(1)) for m in _RE_INLINE_MATH.finditer(_mask_code(raw)))
    return out


def md_figures(text):
    """원고의 그림 줄을 원고 순서대로 [(캡션 (원문 표지 그대로), 경로, 폭 % 또는 None)]."""
    out = []
    for raw in text.split('\n'):
        m = _RE_FIG_LINE.match(raw)
        if m:
            out.append((m.group(1), m.group(2), int(m.group(3)) if m.group(3) else None))
    return out


def _tex_shown(display, tex):
    """페이지의 수식 주석 (LaTeX) 과 견줄 꼴: 줄 수식의 식 번호 \\tag{n} 은 식 끝의 글자 "(n)" 으로 바뀌어 실린다."""
    return re.sub(r'\\tag\{([^{}]*)\}', lambda m: '\\qquad\\text{(%s)}' % m.group(1), tex).strip() if display else tex.strip()


def html_math(src):
    """페이지의 수식을 문서 순서대로 [(줄 수식인가, 주석의 LaTeX, <math> 안쪽 HTML)]."""
    out = []
    for kind, body in re.findall(r'<math display="(block|inline)"[^>]*>(.*?)</math>', src, re.S):
        m = re.search(r'<annotation encoding="application/x-tex">(.*?)</annotation>', body, re.S)
        out.append((kind == 'block', html_lib.unescape(m.group(1)).strip() if m else None, body))
    return out


def _no_data(src):
    """페이지 글에서 data URI 의 바이트 (base64) 를 뺀 것: 금지 글자열 검사가 그림의 바이트에 우연히 걸리지 않게."""
    return _RE_DATA_PNG.sub('data:image/png;base64,', src)


def _in_order(pieces, hay):
    """조각들을 hay (공백 하나로 맞춘 글) 에서 차례대로 찾는다 (앞 조각이 끝난 자리 뒤에서만).  못 찾은 조각을 돌려준다.
    차례대로 찾으므로 한 조각이 페이지의 다른 자리에 우연히 있는 것으로는 통과하지 못한다."""
    out, pos = [], 0
    for i, p in pieces:
        k = hay.find(p, pos)
        if k < 0:
            out.append((i, p))
        else:
            pos = k + len(p)
    return out


def missing_pieces(md_text, hay, h1_tag=True, skip_lines=(), ext=False):
    """원문 조각 가운데 hay 에 원문 순서대로 있지 않은 것.  skip_lines = 페이지가 싣지 않기로 한 줄 (까닭은 부르는 쪽에 적는다)."""
    return _in_order([(i, p) for i, p in md_pieces(md_text, h1_tag, ext) if i not in skip_lines], hay)


def undetected_mutations(md_text, hay, h1_tag=True, skip_lines=(), ext=False):
    """조각마다 한 글자를 바꿔 본다: 바꿨는데도 검사가 통과하면 (못 잡으면) 그 조각을 돌려준다."""
    out = []
    odd, odd2 = chr(0x9F98), chr(0x9F96)        # 원문에 없는 글자 둘
    pieces = [(i, p) for i, p in md_pieces(md_text, h1_tag, ext) if i not in skip_lines]
    for j, (i, p) in enumerate(pieces):
        k = len(p) // 2
        q = p[:k] + (odd if p[k] != odd else odd2) + p[k + 1:]
        if not _in_order(pieces[:j] + [(i, q)] + pieces[j + 1:], hay):
            out.append((i, p))
    return out


def md_date(text):
    m = re.match(r'<!-- BRIEFING:UPDATED (\d{4}-\d{2}-\d{2}) -->\n', text)
    return m.group(1) if m else None


def md_table_after(text, heading):
    """`## heading` 절의 첫 표 → 줄 (칸 목록) 들 (머리 행 포함 · 구분 줄 제외)."""
    rows, on = [], False
    for ln in text.split('\n'):
        if ln.startswith('## '):
            if on and rows:
                break
            on = ln[3:].strip() == heading or re.sub(r'^\d+\.\s+', '', ln[3:].strip()) == heading
            continue
        if on and ln.startswith('|'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                rows.append(cells)
        elif on and rows and not ln.startswith('|'):
            break
    return rows


def md_headings(text):
    return [ln[3:].strip() for ln in text.split('\n') if ln.startswith('## ')]


def md_dois(text):
    return sorted(set(re.findall(r'doi:(10\.\d{4,9}/[^\s|]+)', text)))


# ───────────────────────────── docx 읽기 ─────────────────────────────
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def docx_part(path, name):
    with zipfile.ZipFile(path) as z:
        return z.read(name)


def docx_body(path):
    return ET.fromstring(docx_part(path, 'word/document.xml')).find(W + 'body')


def para_text(p):
    return ''.join(t.text or '' for t in p.iter(W + 't'))


def docx_paragraphs(path):
    """본문 문단 글 (표 안 문단 포함 · 문서 순서 · 빈 문단 제외)."""
    return [s for s in (para_text(p) for p in docx_body(path).iter(W + 'p')) if s]


def model_paragraphs(model):
    """빌더 JSON → 문단 글 (문서 순서): 빌더를 돌리지 않고 정본과 순서까지 견준다.
    수식 런 ({math}) · 줄 수식 블록 (eq) 은 글이 아니다 (docx 에서 w:t 가 아니라 m:t) · 그림 블록 (fig) 은 캡션 문단만 글이다."""
    def runs(rs):
        return ''.join(r['text'] for r in rs if 'math' not in r)
    out = [model['title'], model['subtitle'], model['audience'], model['status_line']]
    out.extend(runs(x['runs']) for x in model['lead'])
    for b in model['blocks']:
        if b['t'] == 'h1':
            out.append(b['text'])
        elif b['t'] in ('p', 'li', 'ol'):
            out.append(runs(b['runs']))
        elif b['t'] == 'table':
            for row in b['rows']:
                out.extend(runs(c) for c in row)
        elif b['t'] == 'fig':
            out.append(runs(b['caption']))
        elif b['t'] != 'eq':
            raise ValueError('모르는 블록 ' + repr(b['t']))
    return [s for s in out if s]


def model_math(model):
    """빌더 JSON 의 수식 (OMML) 을 문서 순서대로 [(줄 수식인가, OMML)]."""
    out = []

    def runs(rs):
        out.extend((False, r['math']) for r in rs if 'math' in r)
    for x in model['lead']:
        runs(x['runs'])
    for b in model['blocks']:
        if b['t'] in ('p', 'li', 'ol'):
            runs(b['runs'])
        elif b['t'] == 'table':
            for row in b['rows']:
                for c in row:
                    runs(c)
        elif b['t'] == 'eq':
            out.append((True, b['omml']))
        elif b['t'] == 'fig':
            runs(b['caption'])
    return out


M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
MM = '{%s}' % M_NS


def docx_math_counts(path):
    """docx 본문의 수식 수 (m:oMath 전체 · 그 가운데 줄 수식 m:oMathPara)."""
    body = docx_body(path)
    return len(list(body.iter(MM + 'oMath'))), len(list(body.iter(MM + 'oMathPara')))


#: 정본 docx 를 만든 docx 모듈 (npm) 의 판.  이 판에서는 빌더 출력의 XML 이 정본과 요소 · 속성까지 같다 (2026-11-10 확인: 본문 ·
#: 스타일 · 번호 · 바닥글 · 설정이 바이트까지 같았다).  다른 판에서는 글 · 순서만 본다.
DOCX_JS_VERSION = '9.7.1'
_JS_DOCX_VERSION = ("const p=require('path'),fs=require('fs');const d=p.dirname(require.resolve('docx'));"
                    "process.stdout.write(JSON.parse(fs.readFileSync(p.join(d,'..','package.json'),'utf8')).version)")


def core_props(data):
    """docProps/core.xml → (제목 · 만든 이 · 설명) (만든 시각은 보지 않는다)."""
    root = ET.fromstring(data)
    dc = '{http://purl.org/dc/elements/1.1/}'
    return tuple((root.find(dc + k).text if root.find(dc + k) is not None else None) for k in ('title', 'creator', 'description'))


def xml_canon(data):
    """XML → 비교용 꼴 (요소 이름 · 정렬한 속성 · 글 · 자식 순서): 속성 순서 · 네임스페이스 접두 차이는 보지 않는다."""
    def walk(e):
        return (e.tag, tuple(sorted(e.attrib.items())), (e.text or ''), tuple(walk(c) for c in e), (e.tail or ''))
    return walk(ET.fromstring(data))


# ───────────────────────────── 공통 검사 묶음 ─────────────────────────────
def closed_file_checks(label, rel, sib_url, page=None, images=None):
    """닫힌 파일 규칙 · 색 토큰 · 인쇄 · 링크: 페이지마다 같은 규칙.
    page = 리포 파일 대신 볼 바이트 (고정물처럼 커밋하지 않는 페이지) · images = 있어야 하는 <img> 수 (None = 세지 않는다)."""
    raw = _bytes(rel) if page is None else page
    src = raw.decode('utf-8', 'replace') if page is not None else _read(rel)
    exists = bool(src)
    sc = scan(src)
    css = _css(src)
    text = _no_data(src)        # 금지 글자열은 그림의 바이트 (base64) 를 뺀 글에서 찾는다
    if page is None:
        chk(f'{label} 정적 파일이 webapp/static/explain/ 에 있다', exists)
    chk(f'{label} UTF-8 · LF 만 · BOM 없음 · 끝 줄바꿈 하나',
        exists and b'\r' not in raw and not raw.startswith(b'\xef\xbb\xbf') and raw.endswith(b'\n') and not raw.endswith(b'\n\n'))
    chk(f'{label} <!doctype html> · lang="ko" · charset · viewport',
        src.startswith('<!doctype html>\n<html lang="ko">') and '<meta charset="utf-8">' in src
        and '<meta name="viewport" content="width=device-width, initial-scale=1">' in src)
    chk(f'{label} <title> = "{TITLE}" 로 시작', bool(re.search(r'<title>%s[^<]*</title>' % re.escape(TITLE), src)))
    chk(f'{label} 태그 짝이 맞다 (닫히지 않은 · 엇갈린 태그 0)', exists and not sc.stack and not sc.unbalanced)
    chk(f'{label} 금지 요소 없음 (script · link · iframe · form · svg … 찾은 것 {sorted(set(sc.banned))})', exists and not sc.banned)
    chk(f'{label} 외부 자원 · 스킴 없음: 그림은 페이지 안에 실은 PNG (data URI) 뿐 (찾은 것 {sc.ext})', exists and not sc.ext)
    bad_img = [im for im in sc.imgs if not (im.get('alt', '').strip() and re.fullmatch(r'[1-9]\d*', im.get('width', ''))
                                             and re.fullmatch(r'[1-9]\d*', im.get('height', '')))]
    chk(f'{label} <img> {len(sc.imgs)} 개{"" if images is None else " (기대 " + str(images) + ")"}: 모두 alt · width · height 가 있다',
        exists and not bad_img and (images is None or len(sc.imgs) == images))
    chk(f'{label} 이벤트 속성 (on…) 없음 (찾은 것 {sc.events})', exists and not sc.events)
    chk(f'{label} <style> 하나 (인라인) · @import · url( 없음',
        exists and sc.styles == 1 and '@import' not in css and 'url(' not in css)
    chk(f'{label} "http" 글자열이 파일 어디에도 없음 (DOI 는 글자로)', exists and 'http' not in text.lower())
    allowed = {'/', sib_url}
    bad_href = [h for h in sc.hrefs if h not in allowed and not re.fullmatch(r'#[a-z0-9-]+', h)]
    chk(f'{label} href 는 "/" · 짝 페이지 · #자리 뿐 (그 밖 {bad_href})', exists and not bad_href)
    dangling = sorted(set(h[1:] for h in sc.hrefs if h.startswith('#')) - set(sc.ids))
    chk(f'{label} #자리 링크가 모두 실제 id 를 가리킨다 (없는 것 {dangling})', exists and not dangling)
    chk(f'{label} id 중복 없음', exists and len(sc.ids) == len(set(sc.ids)))
    chk(f'{label} 처음 링크 <a … href="/">', bool(re.search(r'<a [^>]*href="/"', src)))
    chk(f'{label} 짝 페이지 링크 (머리 nav.top 안)',
        bool(re.search(r'<nav class="top"[^>]*>.*?href="%s".*?</nav>' % re.escape(sib_url), src, re.S)))
    light = _css_block(css, r'(?m)^:root\{([^}]*)\}')
    dmed = _css_block(css, r'@media \(prefers-color-scheme: dark\)\{:root:not\(\[data-theme="light"\]\)\{([^}]*)\}\}')
    dattr = _css_block(css, r'(?m)^:root\[data-theme="dark"\]\{([^}]*)\}')
    tl, tm, ta = _toks(light), _toks(dmed), _toks(dattr)
    chk(f'{label} 색 토큰 세 블록 (:root · prefers-color-scheme dark · data-theme dark) 이 있고 토큰 이름이 같다 ({len(tl)} 개)',
        len(tl) >= 8 and set(tl) == set(tm) == set(ta))
    chk(f'{label} 어두운 두 블록의 값이 같고 · 밝은 값과 다르다 (바탕 · 글자)',
        bool(tm) and tm == ta and tm.get('--bg') != tl.get('--bg') and tm.get('--ink') != tl.get('--ink'))
    used = set(re.findall(r'var\((--[a-z0-9-]+)\)', css))
    chk(f'{label} 쓰는 토큰이 모두 정의돼 있다 (정의 안 된 것 {sorted(used - set(tl))})', bool(used) and used <= set(tl))
    chk(f'{label} 어두운 블록에 color-scheme:dark', 'color-scheme:dark' in dmed and 'color-scheme:dark' in dattr)
    chk(f'{label} body 배경 명시 (var(--bg))', bool(re.search(r'(?m)^body\{[^}]*background:var\(--bg\)', css)))
    chk(f'{label} 글꼴 = 시스템 스택만', FONT_STACK in css and '@font-face' not in css)
    n_tables = len(re.findall(r'<table\b', src))
    n_wrapped = len(re.findall(r'<div class="wrap">\s*<table\b', src))
    chk(f'{label} 표는 모두 가로 스크롤 상자 안 (표 {n_tables} · 상자 안 {n_wrapped})',
        n_tables >= 1 and n_tables == n_wrapped and bool(re.search(r'\.wrap\{[^}]*overflow-x:auto', css)))
    pm = re.search(r'@media print\{(.*)\}\s*$', css, re.S)
    pr = pm.group(1) if pm else ''
    chk(f'{label} @media print = A4 · 흰 바탕 · 그림자 없음 · 쪽 나눔 규칙',
        '@page{size:A4' in pr and '--bg:#fff' in pr.replace('#ffffff', '#fff') and 'box-shadow:none' in pr
        and 'break-before:page' in pr and 'break-inside:avoid' in pr)
    commas = sorted(set(re.findall(r'\d{1,3}(?:,\d{3})+(?![\d])', sc.visible)))
    chk(f'{label} 보이는 글의 천 단위 콤마 0 (찾은 것 {commas})', exists and not commas)
    chk(f'{label} em dash 없음 (파일 전체)', exists and EM_DASH not in src)
    m_model = RE_MODEL.search(text)
    chk(f'{label} 모델 이름 · ID 없음 ({m_model.group(0) if m_model else "-"})', exists and not m_model)
    m_addr = RE_ADDR.search(sc.visible)
    chk(f'{label} 보이는 글에 주소 · 포트 · user@host 없음 ({m_addr.group(0) if m_addr else "-"})', exists and not m_addr)
    m_abs = RE_ABS.search(text)
    chk(f'{label} 절대 경로 없음 ({m_abs.group(0) if m_abs else "-"})', exists and not m_abs)
    chk(f'{label} 생성물 표지 (생성기 이름 · 손으로 고치지 않는다) 가 머리 주석에', GEN in src[:600] and '손으로 고치지 않는다' in src[:600])
    return src, sc


def main():
    plan_md, new_md = _read(SRC_PLAN), _read(SRC_NEW)
    date_a, date_b = md_date(plan_md), md_date(new_md)

    print('── ⓪ 원문 둘 · 정본 docx 가 제자리에')
    chk('원문 (a) briefing_ko.md 가 있고 마커 날짜가 첫 줄에 하나', bool(date_a) and plan_md.count('BRIEFING:UPDATED') == 1)
    chk('원고 (b) plan_newcomer_ko.md 가 있고 마커 날짜가 첫 줄에 하나', bool(date_b) and new_md.count('BRIEFING:UPDATED') == 1)
    chk('정본 docx 가 제자리에 있다', os.path.isfile(_p(DOCX)))
    chk('정본 docx = 1저자가 올린 바이트 그대로 (sha256)', lambda: hashlib.sha256(_bytes(DOCX)).hexdigest() == DOCX_SHA256)

    print('── ① 생성기: --check · 결정적 · 원문이 바뀌면 출력이 바뀜 · 낯선 구성 거부')
    gen = None
    try:
        gen = importlib.import_module('build_dem_redesign_plan')
    except Exception as e:      # noqa: BLE001
        print(f'        (생성기 import 실패: {type(e).__name__}: {e})')
    chk('생성기 scripts/build_dem_redesign_plan.py 가 있고 import 된다', gen is not None)
    said = []

    def gmain(argv, root=None):
        """생성기 main 을 프로세스 안에서 부른다.  그 출력은 삼켜 said 에 모은다 (반례의 실패 줄이 이 시험의 출력에 섞이지 않게)."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = gen.main(argv, root=root)
        said.append(buf.getvalue())
        return rc
    chk('생성기의 경로 상수 = 이 시험의 경로',
        lambda: (gen.SRC_PLAN, gen.SRC_NEWCOMER, gen.OUT_PLAN, gen.OUT_NEWCOMER, gen.OUT_MODEL, gen.URL_PLAN, gen.URL_NEWCOMER)
        == (SRC_PLAN, SRC_NEW, OUT_PLAN, OUT_NEW, OUT_MODEL, URL_PLAN, URL_NEW))
    chk('--check (프로세스 안 · 리포 루트) → rc 0', lambda: gmain(['--check']) == 0)
    chk('인자 없이 = --check (rc 0 · 파일을 쓰지 않는다)', lambda: gmain([]) == 0)
    built = {}
    try:
        built = gen.build_all(ROOT)
    except Exception as e:      # noqa: BLE001
        print(f'        (build_all 실패: {type(e).__name__}: {e})')
    #  원고에 수식이 있으면 그 변환 캐시도 생성물이다 (없으면 캐시 파일을 두지 않는다)
    has_math = bool(md_math(new_md))
    want_built = sorted([OUT_PLAN, OUT_NEW, OUT_MODEL] + ([NEW_MATH] if has_math else []))
    chk(f'build_all 이 생성물 {len(want_built)} 개 (HTML 둘 · JSON{" · 수식 캐시" if has_math else ""}) 를 낸다', sorted(built) == want_built)
    for rel, what in ((OUT_PLAN, 'HTML (a)'), (OUT_NEW, 'HTML (b)'), (OUT_MODEL, 'JSON')) + (((NEW_MATH, '수식 캐시'),) if has_math else ()):
        chk(f'메모리에서 다시 만든 {what} = 커밋된 파일 바이트', lambda rel=rel: bool(built[rel]) and built[rel] == _bytes(rel))
    chk('원고에 수식이 없으면 수식 캐시 파일도 없다 (있으면 낡은 것)', has_math or not os.path.exists(_p(NEW_MATH)))
    chk('두 번 만들면 같은 바이트 (결정적 · 시각 없음)', lambda: gen.build_all(ROOT) == built and len(built) == len(want_built))
    chk('생성물에 CR · BOM 없음 · 끝 줄바꿈 하나',
        lambda: all(b'\r' not in v and not v.startswith(b'\xef\xbb\xbf') and v.endswith(b'\n') and not v.endswith(b'\n\n')
                    for v in built.values()) and len(built) == len(want_built))
    chk('JSON 이 원고의 sha256 을 싣는다 (어느 원고로 만든 것인지)',
        lambda: json.loads(built[OUT_MODEL].decode('utf-8'))['source_sha256'] == hashlib.sha256(_bytes(SRC_NEW)).hexdigest())

    tmp = tempfile.mkdtemp(prefix='dem_plan_test_')
    try:
        def fresh():
            """리포의 원문 둘 · 생성물 (· 원고의 수식 캐시 · 그림) 만 든 임시 루트."""
            root = tempfile.mkdtemp(dir=tmp)
            rels = [SRC_PLAN, SRC_NEW, OUT_PLAN, OUT_NEW, OUT_MODEL] + ([NEW_MATH] if os.path.isfile(_p(NEW_MATH)) else [])
            rels += [posixpath.normpath(posixpath.join(posixpath.dirname(SRC_NEW), f[1])) for f in md_figures(new_md)]
            for rel in rels:
                os.makedirs(os.path.dirname(_p(rel, root)), exist_ok=True)
                shutil.copyfile(_p(rel), _p(rel, root))
            return root

        def put(root, rel, text):
            with open(_p(rel, root), 'w', encoding='utf-8', newline='') as f:
                f.write(text)

        def put_bytes(root, rel, data):
            os.makedirs(os.path.dirname(_p(rel, root)), exist_ok=True)
            with open(_p(rel, root), 'wb') as f:
                f.write(data)

        r0 = None
        try:
            r0 = fresh()
        except Exception as e:      # noqa: BLE001
            print(f'        (임시 사본 실패: {type(e).__name__}: {e})')
        chk('임시 루트 사본 (그대로) → --check rc 0', lambda: gmain(['--check'], root=r0) == 0)

        def changed(root):
            """그 루트의 원문으로 다시 만든 것 가운데, 리포 원문으로 만든 것 (built) 과 다른 생성물."""
            b = gen.build_all(root)
            return sorted(rel for rel in b if b[rel] != built[rel])

        def mutated(rel, old, new):
            root = fresh()
            text = _read(rel, root)
            assert text.count(old) >= 1, old
            put(root, rel, text.replace(old, new, 1))
            return root

        ra = None
        try:
            ra = mutated(SRC_PLAN, '값싼 2D 시험', '값싼 2D 실험')
        except Exception as e:      # noqa: BLE001
            print(f'        (사본 변이 실패: {type(e).__name__}: {e})')
        chk('briefing 한 글자 바꾼 사본 → --check rc 1', lambda: gmain(['--check'], root=ra) == 1)
        chk('  그때 바뀌는 것은 HTML (a) 뿐', lambda: changed(ra) == [OUT_PLAN])
        rb = None
        try:
            rb = mutated(SRC_NEW, '무른 알갱이입니다', '무른 알갱이입니당')
        except Exception as e:      # noqa: BLE001
            print(f'        (사본 변이 실패: {type(e).__name__}: {e})')
        chk('원고 한 글자 바꾼 사본 → --check rc 1', lambda: gmain(['--check'], root=rb) == 1)
        chk('  그때 바뀌는 것은 HTML (b) 와 JSON', lambda: changed(rb) == sorted([OUT_NEW, OUT_MODEL]))
        rw = None
        try:
            rw = mutated(SRC_NEW, '무른 알갱이입니다', '무른 알갱이입니당')
        except Exception as e:      # noqa: BLE001
            print(f'        (사본 변이 실패: {type(e).__name__}: {e})')
        chk('--write 는 세 파일을 다시 쓰고 (rc 0) 그 뒤 --check 가 rc 0',
            lambda: gmain(['--write'], root=rw) == 0 and gmain(['--check'], root=rw) == 0
            and '무른 알갱이입니당' in _read(OUT_NEW, rw) and '무른 알갱이입니당' in _read(OUT_MODEL, rw))
        rd = None
        try:
            rd = fresh()
            os.remove(_p(OUT_PLAN, rd))
        except Exception as e:      # noqa: BLE001
            print(f'        (사본 준비 실패: {type(e).__name__}: {e})')
        chk('커밋된 생성물이 없으면 --check rc 1', lambda: gmain(['--check'], root=rd) == 1)

        # 낯선 구성: (이름, 원문, 바꿀 글, 넣을 글, 기대 줄 번호 또는 None = 줄 번호만 있으면 됨)
        def strange(rel, old, new, want_line=None, files=None):
            """old → new 로 바꾼 원문이면 생성기가 ParseError (그 원문 이름 · 줄 번호 · want_line 이면 그 줄) 를 내고 --check 는 rc 2.
            files = 그 루트에 먼저 둘 파일 {리포 상대 경로: 바이트} (그림 반례)."""
            root = fresh()
            text = _read(rel, root)
            assert old in text, old
            put(root, rel, text.replace(old, new, 1))
            for frel, data in (files or {}).items():
                put_bytes(root, frel, data)
            try:
                gen.build_all(root)
            except gen.ParseError as e:
                ok_line = isinstance(e.line, int) and e.line >= 1 and (want_line is None or e.line == want_line)
                return (ok_line and e.name == rel and gmain(['--check'], root=root) == 2
                        and '%s:%d: ' % (rel, e.line) in said[-1])
            return False

        def ln(needle, text=new_md):
            return next(i for i, s in enumerate(text.split('\n'), 1) if needle in s)

        cases = [
            ('### 3 단 머리', SRC_NEW, '\n## 2. 지금까지는', '\n### 곁가지\n\n## 2. 지금까지는', lambda: ln('## 2. 지금까지는') - 0),
            ('인용 블록 (>)', SRC_NEW, '\n두 가지 계산 방법을 이어서 썼습니다.', '\n> 두 가지 계산 방법을 이어서 썼습니다.', lambda: ln('두 가지 계산 방법')),
            ('코드 울타리 (```)', SRC_NEW, '\n두 가지 계산 방법을 이어서 썼습니다.', '\n```\n두 가지 계산 방법을 이어서 썼습니다.', lambda: ln('두 가지 계산 방법')),
            ('링크 [글](주소)', SRC_NEW, '두 가지 계산 방법을', '두 가지 [계산](x.md) 방법을', lambda: ln('두 가지 계산 방법')),
            ('그림 ![글](주소)', SRC_NEW, '두 가지 계산 방법을', '두 가지 ![계산](x.png) 방법을', lambda: ln('두 가지 계산 방법')),
            ('HTML 태그', SRC_NEW, '두 가지 계산 방법을', '두 가지 <b>계산</b> 방법을', lambda: ln('두 가지 계산 방법')),
            ('둘째 HTML 주석', SRC_NEW, '\n두 가지 계산 방법을', '\n<!-- 메모 -->\n\n두 가지 계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('3 단 목록', SRC_NEW, '  - 활물질 (AM):', '    - 활물질 (AM):', lambda: ln('활물질 (AM):')),
            ('홀수 들여쓰기 목록', SRC_NEW, '  - 활물질 (AM):', ' - 활물질 (AM):', lambda: ln('활물질 (AM):')),
            ('표 칸 수가 머리와 다름', SRC_NEW, '| 0 | 기공률을 세는 방법', '| 0 | 덤 | 기공률을 세는 방법', lambda: ln('| 0 | 기공률을 세는 방법')),
            ('표 구분 줄 없음', SRC_NEW, '|---|---|---|---|\n| DEM (이산요소법)', '| DEM (이산요소법)', lambda: ln('| DEM (이산요소법)') - 1),
            ('짝 없는 **', SRC_NEW, '두 가지 계산 방법을', '두 가지 **계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('짝 없는 `', SRC_NEW, '두 가지 계산 방법을', '두 가지 `계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('짝 없는 *기울임', SRC_NEW, '두 가지 계산 방법을', '두 가지 *계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('낱말 가운데 별표', SRC_NEW, '두 가지 계산 방법을', '두 가지 계*산 방법을', lambda: ln('두 가지 계산 방법')),
            ('역슬래시', SRC_NEW, '두 가지 계산 방법을', '두 가지 \\*계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('HTML 문자 참조', SRC_NEW, '두 가지 계산 방법을', '두 가지 &amp; 계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('줄 끝 빈칸', SRC_NEW, '두 가지 계산 방법을 이어서 썼습니다.\n', '두 가지 계산 방법을 이어서 썼습니다. \n', lambda: ln('두 가지 계산 방법')),
            ('두 줄 문단', SRC_NEW, '두 가지 계산 방법을 이어서 썼습니다.\n', '두 가지 계산 방법을\n이어서 썼습니다.\n', lambda: ln('두 가지 계산 방법') + 1),
            ('번호 목록이 1 에서 시작하지 않음', SRC_NEW, '\n1. 지금 DEM 에서', '\n3. 지금 DEM 에서', lambda: ln('1. 지금 DEM 에서')),
            ('절 번호 건너뜀', SRC_NEW, '## 2. 지금까지는', '## 3. 지금까지는', lambda: ln('## 2. 지금까지는')),
            ('마커 없음', SRC_NEW, '<!-- BRIEFING:UPDATED 2026-11-10 -->\n', '', lambda: 1),
            ('마커 날짜 꼴이 다름', SRC_NEW, 'BRIEFING:UPDATED 2026-11-10', 'BRIEFING:UPDATED 11-10', lambda: 1),
            ('제목 (#) 둘', SRC_NEW, '\n**지위**:', '\n# 또 하나의 제목\n\n**지위**:', lambda: ln('**지위**:')),
            ('"한 줄로" 없음', SRC_NEW, '**한 줄로**: ', '**요약**: ', lambda: ln('**한 줄로**:')),
            ('탭 문자', SRC_NEW, '두 가지 계산 방법을', '두 가지\t계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('원고에 열 너비 규칙이 없는 표 (docx)', SRC_NEW, '| 용어 | 뜻 |', '| 낱말 | 뜻 |', lambda: ln('| 용어 | 뜻 |')),
            # ── 수식 · 그림 (처음 보는 분용 원고만 받는다) ──
            ('짝 없는 $ (글 안 수식)', SRC_NEW, '두 가지 계산 방법을', '두 가지 $x 계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('수식을 여는 $ 뒤의 빈칸', SRC_NEW, '두 가지 계산 방법을', '두 가지 $ x$ 계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('수식을 닫는 $ 바로 뒤의 숫자', SRC_NEW, '두 가지 계산 방법을', '두 가지 $x$2 계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('글 안의 $$', SRC_NEW, '두 가지 계산 방법을', '두 가지 $$x$$ 계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('머리 줄 안의 수식', SRC_NEW, '## 2. 지금까지는', '## 2. $x$ 지금까지는', lambda: ln('## 2. 지금까지는')),
            ('캐시에 없는 수식 (--check 는 pandoc 을 부르지 않는다)', SRC_NEW, '두 가지 계산 방법을', '두 가지 $q_9$ 계산 방법을',
             lambda: ln('두 가지 계산 방법')),
            ('줄 수식을 닫는 $$ 가 없다 (빈 줄에서 끊김)', SRC_NEW, '\n두 가지 계산 방법을', '\n$$\nx = 1\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법') + 2),
            ('한 줄 수식이 $$ 로 닫히지 않는다', SRC_NEW, '\n두 가지 계산 방법을', '\n$$ x = 1\n\n두 가지 계산 방법을', lambda: ln('두 가지 계산 방법')),
            ('줄 수식 뒤에 빈 줄이 없다', SRC_NEW, '\n두 가지 계산 방법을', '\n$$ x = 1 $$\n두 가지 계산 방법을', lambda: ln('두 가지 계산 방법') + 1),
            ('그림 파일이 없다', SRC_NEW, '\n두 가지 계산 방법을', '\n![그림 1. 없는 그림](nofile.png)\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법')),
            ('그림이 PNG 가 아니다 (이름만 .png)', SRC_NEW, '\n두 가지 계산 방법을', '\n![그림 1. 글자 파일](notpng.png)\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법'), {NEW_DIR + '/notpng.png': NOT_PNG}),
            ('그림이 너무 크다 (상한 넘음)', SRC_NEW, '\n두 가지 계산 방법을', '\n![그림 1. 큰 그림](big.png)\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법'), {NEW_DIR + '/big.png': PNG_HEAD + b'0' * (gen.FIG_MAX_BYTES if gen else 1)}),
            ('그림 경로에 ".." (원고 폴더 밖)', SRC_NEW, '\n두 가지 계산 방법을', '\n![그림 1. 밖](../x.png)\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법')),
            ('그림 확장자가 png 가 아니다', SRC_NEW, '\n두 가지 계산 방법을', '\n![그림 1. 사진](x.jpg)\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법')),
            ('그림 폭이 범위 밖 (5 %)', SRC_NEW, '\n두 가지 계산 방법을', '\n![그림 1. 폭](x.png){width=5%}\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법')),
            ('그림 줄 뒤에 붙은 글', SRC_NEW, '\n두 가지 계산 방법을', '\n![그림 1. 글](x.png) 뒤 글\n\n두 가지 계산 방법을',
             lambda: ln('두 가지 계산 방법')),
            ('캡션 없는 그림', SRC_NEW, '\n두 가지 계산 방법을', '\n![](x.png)\n\n두 가지 계산 방법을', lambda: ln('두 가지 계산 방법'),
             {NEW_DIR + '/x.png': _bytes(FIX_PNG)}),
            ('(a) 원문의 달러 기호 (수식은 처음 보는 분용 원고에서만 받는다)', SRC_PLAN, '값싼 2D 시험', '값싼 $x$ 2D 시험',
             lambda: ln('값싼 2D 시험', plan_md)),
            ('(a) 단계 번호 건너뜀', SRC_PLAN, '- **단계 1 셈**', '- **단계 2 셈**', lambda: ln('- **단계 1 셈**', plan_md)),
            ('(a) 질문에 "답:" 없음', SRC_PLAN, '  답: 권고대로 (예).', '  회신: 권고대로 (예).', lambda: ln('- **Q1.**', plan_md)),
            ('(a) 갈림 표에 모르는 칩', SRC_PLAN, '| (가) 같음 |', '| (바) 같음 |', lambda: ln('| (가) 같음 |', plan_md)),
            ('(a) 배지를 만들 지위 글이 없음', SRC_PLAN, '결과 0 건 · ', '', lambda: ln('**지위**:', plan_md)),
            ('(a) 계획서 꼴 절이 없음 (하지 않는 말)', SRC_PLAN, '## 6. 하지 않는 말', '## 6. 삼가는 말', lambda: None),
            ('(a) 논문 표의 인용 번호가 참고문헌에 없음', SRC_PLAN, '| [7] Cárdenas-Barrantes 2022 |', '| [17] Cárdenas-Barrantes 2022 |',
             lambda: ln('| [7] Cárdenas-Barrantes 2022 |', plan_md)),
            ('(a) 참고문헌 표의 머리 행이 다름 (싣지 않는 칸의 글이 바뀜)', SRC_PLAN, '| # | 서지 | litdb 카드 (slug) |', '| 번호 | 서지 | litdb 카드 (slug) |',
             lambda: ln('| # | 서지 | litdb 카드 (slug) |', plan_md)),
            ('(a) 참고문헌 번호가 차례가 아님', SRC_PLAN, '| 2 | S.G. Bardenhagen, J.E. Guilkey', '| 3 | S.G. Bardenhagen, J.E. Guilkey',
             lambda: ln('| 2 | S.G. Bardenhagen, J.E. Guilkey', plan_md)),
            ('(a) 큰 지적 (P1) 줄이 ID 로 시작하지 않음', SRC_PLAN, '  - `DRD-01` 격자를', '  - 격자를', lambda: ln('  - `DRD-01` 격자를', plan_md)),
            ('(a) 단계 줄 끝에 버려질 글 (":" 없이 덧붙은 글)', SRC_PLAN, '- **단계 7 구조 · 수송**.', '- **단계 7 구조 · 수송** 나중에.',
             lambda: ln('- **단계 7 구조 · 수송**.', plan_md)),
        ]
        for case in cases:
            name, rel, old, new, want = case[:5]
            files = case[5] if len(case) > 5 else None
            chk(f'낯선 구성 거부 (rc 2 · 줄 번호): {name}',
                lambda rel=rel, old=old, new=new, want=want, files=files: strange(rel, old, new, want(), files))
        chk('ParseError 글 = "파일:줄: 까닭" 꼴',
            lambda: bool(re.match(r'^x\.md:3: \S', str(_raises(gen, '<!-- BRIEFING:UPDATED 2026-11-10 -->\n# 제목\n> 인용\n', 'x.md')))))
        tiny = ('<!-- BRIEFING:UPDATED 2026-11-10 -->\n# 제목\n\n**지위**: 가나.\n\n**한 줄로**: 다라.\n\n## 1. 절\n\n'
                '고정폭 `a$b` 와 `$HOME` 은 글자이고 $x_1$ 과 $y$ 는 수식이다.\n')
        chk('고정폭 안의 달러 기호는 수식이 아니다: 생성기와 이 시험의 원고 읽개가 같은 답 (수식 둘 · 글 조각은 고정폭 글자 그대로)',
            lambda: [v for k, v in gen.parse(tiny, 't.md', extended=True).sections[0].blocks[0].inl if k == 'm'] == ['x_1', 'y']
            and [t for _d, t in md_math(tiny)] == ['x_1', 'y']
            and [p for _i, p in md_pieces(tiny, False, True)][-2:] == ['고정폭 a$b 와 $HOME 은 글자이고', '는 수식이다.'])


        # ── 수식 캐시 · 그림의 한살이 (임시 루트 · pandoc 을 부르지 않는다: 변환기를 가짜로 바꿔 끼운다) ──
        anchor = '두 가지 계산 방법을 이어서 썼습니다.'
        with_math = new_md.replace(anchor, anchor.replace('계산 방법을', '$q_9$ 계산 방법을') + '\n\n$$\nq_9 = 1 \\tag{7}\n$$', 1)
        added = [(False, 'q_9'), (True, 'q_9 = 1 \\tag{7}')]
        n_uniq = len(set(md_math(with_math)))
        bogus = '{"schema": "x", "entries": []}\n'

        def fake_convert(items, name):
            return [{'latex': t, 'display': d, 'pandoc': 'fake',
                     'mathml': '<math display="%s"><mi>q</mi></math>' % ('block' if d else 'inline'),
                     'omml': ('<m:oMathPara><m:oMath><m:r><m:t>q</m:t></m:r></m:oMath></m:oMathPara>' if d
                              else '<m:oMath><m:r><m:t>q</m:t></m:r></m:oMath>')} for d, t, _no in items]

        def cache_keys(root):
            return [(e['display'], e['latex']) for e in json.loads(_read(NEW_MATH, root))['entries']]
        rm = None
        try:
            rm = fresh()
            put(rm, SRC_NEW, with_math)
        except Exception as e:      # noqa: BLE001
            print(f'        (사본 준비 실패: {type(e).__name__}: {e})')
        chk('수식을 더한 원고 (그 식이 캐시에 없음) → --check rc 2 · 까닭에 캐시 경로와 --write',
            lambda: [k for k in md_math(with_math) if k in added] == added and gmain(['--check'], root=rm) == 2
            and NEW_MATH in said[-1] and '--write' in said[-1])
        keep = (getattr(gen, 'pandoc_version', None), getattr(gen, 'pandoc_convert', None))
        try:
            if gen is not None:
                gen.pandoc_version = lambda: None
            chk('  pandoc 이 없는 기계의 --write → rc 2 (조용히 빼고 싣지 않는다) · 캐시에 그 식을 쓰지 않는다',
                lambda: gmain(['--write'], root=rm) == 2 and 'pandoc' in said[-1]
                and (not [k for k in cache_keys(rm) if k in added] if has_math else not os.path.exists(_p(NEW_MATH, rm))))
            if gen is not None:
                gen.pandoc_convert = fake_convert
            chk('  변환기가 있으면 --write → rc 0 · 캐시가 원고의 식을 모두 (겹치는 식은 한 번 · 원고 순서) 싣고 · 그 뒤 --check 는 변환기 없이 rc 0',
                lambda: gmain(['--write'], root=rm) == 0 and len(cache_keys(rm)) == n_uniq
                and [k for k in cache_keys(rm) if k in added] == added and gmain(['--check'], root=rm) == 0)
            chk('  그 페이지 (b) 에 더한 수식 둘 (글 안 · 줄) · JSON 의 수식 (글 안 / 줄 · 순서) = 원고의 수식',
                lambda: '<math display="inline"><mi>q</mi></math> 계산 방법을' in _read(OUT_NEW, rm)
                and '<div class="eq"><math display="block"><mi>q</mi></math></div>' in _read(OUT_NEW, rm)
                and [k for k, _o in model_math(json.loads(_read(OUT_MODEL, rm)))] == [k for k, _t in md_math(with_math)])
            chk('  캐시의 꼴이 다르면 (손으로 망가뜨림) → --check rc 2 (캐시 파일 이름을 짚는다)',
                lambda: (put(rm, NEW_MATH, bogus), gmain(['--check'], root=rm))[1] == 2 and NEW_MATH + ':1: ' in said[-1])
            chk('  망가진 캐시는 --write 가 처음부터 다시 만든다 (rc 0 · 식 수 그대로 · 그 뒤 --check rc 0)',
                lambda: gmain(['--write'], root=rm) == 0 and len(cache_keys(rm)) == n_uniq and gmain(['--check'], root=rm) == 0)
        finally:
            if gen is not None:
                gen.pandoc_version, gen.pandoc_convert = keep
        chk('  원고에서 그 수식을 다시 빼면 → --check rc 1 (낡은 캐시) · --write 가 캐시를 줄이거나 지우고 · 다시 rc 0',
            lambda: (put(rm, SRC_NEW, new_md), gmain(['--check'], root=rm))[1] == 1 and gmain(['--write'], root=rm) == 0
            and os.path.exists(_p(NEW_MATH, rm)) == has_math and gmain(['--check'], root=rm) == 0)
        rf = None
        fig_line = '![그림 9. 격자 마디와 물질점 (모식도)](fig_grid.png){width=50%}'
        try:
            rf = fresh()
            put(rf, SRC_NEW, new_md.replace(anchor, anchor + '\n\n' + fig_line, 1))
            put_bytes(rf, NEW_DIR + '/fig_grid.png', _bytes(FIX_PNG))
        except Exception as e:      # noqa: BLE001
            print(f'        (사본 준비 실패: {type(e).__name__}: {e})')
        chk('그림을 더한 원고 → --check rc 1 · --write rc 0 · 다시 --check rc 0 (pandoc 없이)',
            lambda: gmain(['--check'], root=rf) == 1 and gmain(['--write'], root=rf) == 0 and gmain(['--check'], root=rf) == 0)
        chk('  그 페이지 (b) 에 그 그림 (PNG 를 data URI 로 · 폭 50 %) 과 캡션 · JSON 에 그림 블록 (경로 · sha256)',
            lambda: (lambda page, model: len(_RE_DATA_PNG.findall(page)) == 1 + len(md_figures(new_md))
                     and any(base64.b64decode(x) == _bytes(FIX_PNG) for x in _RE_DATA_PNG.findall(page))
                     and 'style="width:50%"' in page and '<figcaption>그림 9. 격자 마디와 물질점 (모식도)</figcaption>' in page
                     and (NEW_DIR + '/fig_grid.png', hashlib.sha256(_bytes(FIX_PNG)).hexdigest())
                     in [(b['path'], b['sha256']) for b in model['blocks'] if b['t'] == 'fig'])
            (_read(OUT_NEW, rf), json.loads(_read(OUT_MODEL, rf))))
        chk('  그림 파일이 바뀌면 (한 바이트) → --check rc 1 (페이지가 그림의 바이트를, JSON 이 그 sha256 을 싣는다)',
            lambda: (put_bytes(rf, NEW_DIR + '/fig_grid.png', _bytes(FIX_PNG) + b'0'), gmain(['--check'], root=rf))[1] == 1)
        rg = None
        try:
            rg = fresh()
            put(rg, SRC_NEW, new_md.replace(anchor, anchor + '\n\n' + fig_line.replace('{width=50%}', ''), 1))
            put_bytes(rg, NEW_DIR + '/fig_grid.png', _bytes(FIX_PNG))
        except Exception as e:      # noqa: BLE001
            print(f'        (사본 준비 실패: {type(e).__name__}: {e})')
        chk('폭을 적지 않은 그림은 본문 폭에 맞춘다 (페이지 width:100% · JSON 601 x 367 px)',
            lambda: (lambda b: 'style="width:100%"' in b[OUT_NEW].decode('utf-8')
                     and (601, 367) in [(x['width'], x['height']) for x in json.loads(b[OUT_MODEL].decode('utf-8'))['blocks'] if x['t'] == 'fig'])
            (gen.build_all(rg)))
        chk('그림 크기 규칙 (figure_display): 폭 없음 = 본문 폭 601 px · {width=60%} = 361 px · 키 큰 그림은 한 쪽에 들어가게 줄인다 (키 860 px 까지)',
            lambda: gen.figure_display((360, 220), None) == (601, 367, 100.0) and gen.figure_display((360, 220), 60)[:2] == (361, 221)
            and gen.figure_display((100, 1000), None)[:2] == (86, 860) and 14 < gen.figure_display((100, 1000), None)[2] < 15)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print('── ② 페이지 (a) 계획서: 한 파일로 닫힘 · 색 토큰 · 인쇄 · 문체')
    src_a, sc_a = closed_file_checks('(a)', OUT_PLAN, URL_NEW, images=0)
    chk('(a) 수식 · 그림 없음: 계획서 원문은 수식 · 그림을 받지 않는다 (달러 기호는 rc 2)', bool(src_a) and sc_a.maths == 0 and not sc_a.imgs)
    text_a = sc_a.visible

    print('── ③ 페이지 (a) 계획서 꼴 · 원문 핵심')
    cover = re.search(r'<header class="cover">(.*?)</header>', src_a, re.S)
    cov = cover.group(1) if cover else ''
    chk('표지 머리: 제목 <h1> = "DEM 재설계 (수영) 계획서" (하나뿐)',
        bool(re.search(r'<h1>%s</h1>' % re.escape(TITLE), cov)) and src_a.count('<h1') == 1)
    chk('표지 머리: 원문 제목 줄의 꼬리표 · 부제가 그대로',
        '[DEM 우선 (수영)]' in _vis(cov) and '재설계 계획 브리핑 (쉬운 말 · 논문 기준)' in _vis(cov))
    chk(f'표지 머리: 날짜 = 원문 마커 날짜 ({date_a})', bool(date_a) and bool(re.search(r'<span class="date">%s</span>' % date_a, cov)))
    badges = [_vis(b) for b in re.findall(r'<span class="badge[^"]*">(.*?)</span>', cov, re.S)]
    chk(f'표지 머리: 배지 셋 = 결과 0 건 · 실행 GO 요청 아님 · Codex 판정 = 방향 지지 · 규칙 수정 필요 (HOLD) (지금 {badges})',
        badges == ['결과 0 건', '실행 GO 요청 아님', 'Codex 판정 = 방향 지지 · 규칙 수정 필요 (HOLD)'])
    status_src = next((s for s in plan_md.split('\n') if s.startswith('**지위**:')), '')
    chk('배지 글이 원문 "지위" 줄에서 나온다 (원문에 그 글이 있다)',
        all(w in status_src for w in ('결과 0 건', '실행 GO 요청 아님', '방향 지지 · 규칙 수정 필요 (HOLD)')))
    chk('"지위" 문단 (p.status) · "한 줄로" 요약 상자 (div.oneline)',
        bool(re.search(r'<p class="status"><strong>지위</strong>: ', src_a))
        and bool(re.search(r'<div class="oneline"><strong>한 줄로</strong>: 3D 를 새로 짜기 전에', src_a)))
    heads_a = md_headings(plan_md)
    h2s_a = [_vis(h) for h in re.findall(r'<h2[^>]*>(.*?)</h2>', src_a, re.S)]
    chk(f'번호 붙은 절 머리: 원문의 절 {len(heads_a)} 개가 순서대로 (<h2>)', len(heads_a) == 10 and h2s_a == heads_a)
    chk('절마다 section id (s1 … s9 · refs) · 차례 (nav.toc) 가 그 자리를 가리킨다',
        all(f'<section id="s{i}"' in src_a for i in range(1, 10)) and '<section id="refs"' in src_a
        and re.findall(r'href="#(s\d|refs)"', (re.search(r'<nav class="toc"[^>]*>(.*?)</nav>', src_a, re.S) or [None, ''])[1])
        == [f's{i}' for i in range(1, 10)] + ['refs'])
    s3 = _section(src_a, 's3')
    steps = re.findall(r'<li class="step[^"]*" id="step-(\d)">(.*?)</li>', s3, re.S)
    chk('§3 로드맵: 순서 있는 목록 (ol.road) 에 카드 8 장 (단계 0–7 · 순서대로)',
        '<ol class="road">' in s3 and [n for n, _b in steps] == [str(i) for i in range(8)])
    step_src = [m for m in (_RE_STEP.match(s) for s in plan_md.split('\n')) if m]
    chk('§3 로드맵: 카드마다 단계 번호 · 이름 · 괄호 안 (기계 · 기간) 칩 · 내용이 원문 그대로',
        len(step_src) == 8 and len(steps) == 8 and all(
            f'단계 {m.group(1)}' in _vis(b) and _md_strip(m.group(2)) in _vis(b)
            and all(x in [_vis(c) for c in re.findall(r'<span class="chip[^"]*">(.*?)</span>', b, re.S)]
                    for x in (m.group(3).split(' · ') if m.group(3) else []))
            and all(_norm(_md_strip(x)) in _vis(b) for x in (m.group(4).split('  ') if m.group(4) else []))
            for m, (_n, b) in zip(step_src, steps)))
    chk('§3 로드맵: "다음 단계의 문" 문장이 문 줄 (p.gate) 로 · 핵심 단계 (단계 3) 카드 강조 (step key)',
        bool(re.search(r'<p class="gate">.*?통과가 다음 단계의 문이다\.</p>', s3, re.S))
        and bool(re.search(r'<li class="step key" id="step-3">', s3)) and s3.count('class="step key"') == 1)
    chk('§3 일정: 따로 띠 (div.sched) · [추정] 표지 · 원문 글',
        lambda: '[추정]' in _vis(re.search(r'<div class="sched">(.*?)</div>', s3, re.S).group(1))
        and '2D 4–6 주를 CPU 로 (Rint 일정 그대로) · 단계 3 결과 12 월 중순–말 · 3D 는 R 런 뒤.'
        in _vis(re.search(r'<div class="sched">(.*?)</div>', s3, re.S).group(1)))
    fork = re.search(r'<table class="fork">(.*?)</table>', s3, re.S)
    fk = fork.group(1) if fork else ''
    chips = re.findall(r'<span class="chip (k-[a-z]+)">(\([가-힣]\))</span>', fk)
    chk(f'§3 갈림: 결정표 (table.fork) 의 결과 칩 다섯 = (가) (나) (마) (라) (다) · 칩마다 다른 색 클래스 (지금 {chips})',
        [c for _k, c in chips] == ['(가)', '(나)', '(마)', '(라)', '(다)'] and len(set(k for k, _c in chips)) == 5)
    css_a = _css(src_a)
    chk('§3 갈림: 칩 색 클래스마다 CSS 규칙 (바탕 · 글자 토큰)',
        all(re.search(r'\.%s\{[^}]*background:var\(--[a-z0-9-]+\)[^}]*color:var\(--[a-z0-9-]+\)' % k, css_a) for k, _c in chips)
        and len(chips) == 5)
    chk('§3 갈림: 머리 글 "갈림 (결과 전에 정함)" · 표 머리 = 원문', '갈림 (결과 전에 정함)' in _vis(s3) and '2D 결과' in _vis(fk) and '3D 길' in _vis(fk))
    for sid, cls, what, must in (('s4', 'emph', '강조 상자', '1.64 는 고정이고 손잡이가 아니다.'),
                                 ('s5', 'warn', '경고 상자', '둘 다 틀렸다.'),
                                 ('s6', 'dont', '"하지 않는 말" 테두리 상자', '2D 숫자를 3D 로 옮기지 않는다.')):
        body = _section(src_a, sid)
        box = re.search(r'<div class="box %s">(.*)</div>\s*$' % cls, body.strip(), re.S)
        chk(f'§{sid[1:]} = {what} (div.box.{cls}) · 절의 본문이 모두 그 안에 · "{must}"',
            bool(box) and must in _vis(box.group(1)) and src_a.count(f'<div class="box {cls}">') == 1
            and bool(re.search(r'\.box\.%s\{' % cls, css_a)))
    chk('§6 상자 테두리 = 네 변 (border) · 목록 여섯 줄', lambda: bool(re.search(r'\.box\.dont\{[^}]*border:2px solid', css_a))
        and len(re.findall(r'<li>', _section(src_a, 's6'))) == 6)
    s8 = _section(src_a, 's8')
    qa = re.search(r'<table class="qa[^"]*">(.*?)</table>', s8, re.S)
    qrows = re.findall(r'<tr id="q(\d)">(.*?)</tr>', qa.group(1) if qa else '', re.S)
    q_src = [m for m in (_RE_Q.match(s) for s in plan_md.split('\n')) if m]
    chk('§8 질문 표 (table.qa): 머리 = 질문 · 권고 · 1저자 답 · 줄 다섯 (Q1.–Q5.)',
        bool(qa) and [_vis(h) for h in re.findall(r'<th[^>]*>(.*?)</th>', qa.group(1), re.S)] == ['질문', '권고', '1저자 답']
        and [n for n, _r in qrows] == ['1', '2', '3', '4', '5'])

    def _cell(row, cls):
        m = re.search(r'<td class="%s"[^>]*>(.*?)</td>' % cls, row, re.S)
        return _vis(m.group(1)) if m else None
    chk('§8 질문 표: 줄마다 질문 · 권고 · 답 (= 원문의 "답:" 뒤 글) 이 원문 그대로',
        len(q_src) == 5 and len(qrows) == 5 and all(
            _cell(r, 'q') == _norm(m.group(1) + ' ' + _md_strip(m.group(2))) and _cell(r, 'rec') == _norm(_md_strip(m.group(3)))
            and _cell(r, 'ans') == _norm(_md_strip(m.group(4))) for m, (_n, r) in zip(q_src, qrows)))
    s9 = _section(src_a, 's9')
    chk('§9 Codex 판정 상자 (div.verdict) · 판정 줄 (p.vline) = "방향은 지지한다 … HOLD 다"',
        lambda: '방향은 지지한다.' in _vis(re.search(r'<p class="vline">(.*?)</p>', s9, re.S).group(1))
        and 'HOLD 다.' in _vis(re.search(r'<p class="vline">(.*?)</p>', s9, re.S).group(1)) and '<div class="verdict">' in s9)
    finds = re.findall(r'<div class="finding" id="(drd-\d\d)">(.*?)</div>\s*(?=<div class="finding"|</div>)', s9, re.S)
    chk(f'§9 큰 지적 둘 = 눈에 띄는 카드 (div.finding · id drd-01 · drd-02 · P1 표지 · "고침" 줄) (지금 {[k for k, _b in finds]})',
        [k for k, _b in finds] == ['drd-01', 'drd-02']
        and all('<code>DRD-0%d</code>' % (i + 1) in b and 'P1' in _vis(b) and bool(re.search(r'<p class="fix"><b>고침</b>: ', b))
                for i, (_k, b) in enumerate(finds)))
    chk('§9 그 밖 지적 ID (DRD-03 … DRD-13) 가 고정폭으로', all(f'<code>DRD-{i:02d}</code>' in s9 for i in (3, 4, 6, 7, 8, 9, 12, 13)))
    refs_a = _section(src_a, 'refs')
    ref_rows = md_table_after(plan_md, '참고문헌')[1:]
    lis = re.findall(r'<li id="ref-(\d+)">(.*?)</li>', refs_a, re.S)
    chk('참고문헌: 번호 붙은 서지 (ol.refs) 10 행 · id ref-1 … ref-10', '<ol class="refs">' in refs_a and [n for n, _b in lis] == [str(i) for i in range(1, 11)])
    chk('참고문헌: 행마다 서지 글이 원문 그대로 · litdb slug 는 작은 고정폭 (code.slug)',
        len(ref_rows) == 10 and len(lis) == 10 and all(
            _norm(_md_strip(r[1])) in _vis(b) and re.findall(r'<code class="slug">(.*?)</code>', b) == [_md_strip(r[2])]
            for r, (_n, b) in zip(ref_rows, lis)))
    slugs = [_md_strip(r[2]) for r in ref_rows]
    chk('litdb slug 10 개 (서로 다름 · 원문 그대로)', len(set(slugs)) == 10 and all(s in text_a for s in slugs)
        and bool(re.search(r'\.slug\{[^}]*font-family:[^;}]*monospace', css_a)))
    dois_a = md_dois(plan_md)
    chk(f'원문의 DOI {len(dois_a)} 개가 글자로 남아 있다', len(dois_a) == 7 and all('doi:' + d in text_a for d in dois_a))
    s2 = _section(src_a, 's2')
    chk('§2 논문 표: 일곱 줄 · 첫 칸의 [n] 이 참고문헌 자리 (#ref-n) 로 가는 링크',
        re.findall(r'<a class="cite" href="#ref-(\d+)">\[(\d+)\]</a>', s2)[:7] == [(str(i), str(i)) for i in range(1, 8)]
        and len(re.findall(r'<tr>', s2)) >= 8)
    for w in ('진밀도 1.64', '10–13 %', '하지 않는 말', 'SELF-161', 'SELF-160', 'DRD-01', 'DRD-02', 'Q1.', 'Q2.', 'Q3.', 'Q4.', 'Q5.',
              '11.5 %', '15.6 %', '13eb293cd'):
        chk(f'원문 핵심이 남아 있다: "{w}"', w in plan_md and w in text_a)
    #  (a) 는 참고문헌 표를 번호 서지로 싣는다: 머리 행 ("# | 서지 | litdb 카드 (slug)") 은 따로 없고 셋째 칸 머리는 행마다 이름표다
    #  → 그 한 줄만 순서 검사에서 빼고, 이름표가 행마다 있는지는 따로 본다.
    ref_head_a = tuple(i for i, s in enumerate(plan_md.split('\n'), 1) if s.startswith('| # | 서지 |'))
    chk('참고문헌: 표의 셋째 칸 머리 ("litdb 카드 (slug)") 가 행마다 이름표로 (10 번)',
        len(ref_head_a) == 1 and len(re.findall(r'<span class="slugline">litdb 카드 \(slug\) <code class="slug">', refs_a)) == 10)
    miss_a = missing_pieces(plan_md, text_a, skip_lines=ref_head_a) if plan_md and text_a else [(0, '(없음)')]
    chk(f'원문 줄 전수 포함: briefing 의 줄 (목록 · 문단 · 표 칸 · 머리) 이 모두 · 원문 순서대로 페이지에 있다 (조각 {len(md_pieces(plan_md))} · 없는 것 {len(miss_a)}'
        f'{" · 첫 줄 " + str(miss_a[0][0]) + " " + miss_a[0][1][:40] if miss_a else ""})', bool(plan_md) and not miss_a)
    und_a = undetected_mutations(plan_md, text_a, skip_lines=ref_head_a) if plan_md and text_a else [(0, '')]
    chk(f'  그 검사는 조각마다 한 글자를 바꾸면 모두 잡는다 (못 잡은 것 {len(und_a)})', bool(plan_md) and not und_a)

    print('── ④ 페이지 (b) 처음 보는 분: 한 파일로 닫힘 · 색 토큰 · 인쇄 · 문체')
    math_b, figs_b = md_math(new_md), md_figures(new_md)
    src_b, sc_b = closed_file_checks('(b)', OUT_NEW, URL_PLAN, images=len(figs_b))
    text_b = sc_b.visible
    chk('(a) 와 (b) 의 색 토큰 (밝은 · 어두운) 이 같다: 한 벌',
        lambda: _toks(_css_block(_css(src_a), r'(?m)^:root\{([^}]*)\}')) == _toks(_css_block(_css(src_b), r'(?m)^:root\{([^}]*)\}'))
        and len(_toks(_css_block(_css(src_b), r'(?m)^:root\{([^}]*)\}'))) >= 8)

    print('── ⑤ 페이지 (b) docx 꼴 · 원고 핵심')
    head = re.search(r'<header class="doc-head">(.*?)</header>', src_b, re.S)
    hd = head.group(1) if head else ''
    chk('제목 블록 네 줄: 제목 · 부제 (원고 제목 줄에서 꼬리표를 뺀 글) · "처음 보는 분을 위한 설명" · 날짜 · 지위 줄',
        [_vis(x) for x in re.findall(r'<(?:h1|p)[^>]*>(.*?)</(?:h1|p)>', hd, re.S)]
        == [TITLE, '가압부터 탈압까지 한 모델로 계산하기', '처음 보는 분을 위한 설명',
            f'{date_b} · 계획 문서 · 계산 결과는 아직 없음 · 외부 검토 = 방향은 맞음, 판정 규칙은 고치는 중'])
    chk('제목 블록: 클래스 (subtitle · audience · statusline) · <h1> 하나뿐',
        all(f'<p class="{c}">' in hd for c in ('subtitle', 'audience', 'statusline')) and src_b.count('<h1') == 1)
    chk('"지위" 문단 (p.status) · "한 줄로" 상자 (div.oneline)',
        bool(re.search(r'<p class="status"><strong>지위</strong>: 계획 문서입니다\.', src_b))
        and bool(re.search(r'<div class="oneline"><strong>한 줄로</strong>: 전극을 누르는 과정을', src_b)))
    heads_b = md_headings(new_md)
    h2s_b = [_vis(h) for h in re.findall(r'<h2[^>]*>(.*?)</h2>', src_b, re.S)]
    n_sec, n_tab, n_gl, n_ref = SHAPE['sections'], SHAPE['tables'], SHAPE['glossary_rows'], SHAPE['ref_rows']
    chk(f'절 제목 {n_sec} 개 (1–{n_sec - 1} + 참고문헌) 가 순서대로 (<h2>)', len(heads_b) == n_sec and h2s_b == heads_b)
    chk(f'절마다 section id (s1 … s{n_sec - 1} · refs)',
        all(f'<section id="s{i}"' in src_b for i in range(1, n_sec)) and '<section id="refs"' in src_b)

    def sid_b(title):
        """원고의 "## N. title…" 절 → 페이지의 section id (sN).  없으면 '-' (그런 절은 페이지에 없다)."""
        return next(('s' + h.split('.', 1)[0] for h in heads_b if re.match(r'^\d+\. %s' % re.escape(title), h)), '-')
    tables_b = re.findall(r'<table[^>]*>(.*?)</table>', src_b, re.S)
    chk(f'표 {n_tab} 개 (= 원고의 표 수) · 표마다 머리 행 (<thead> · th scope="col") · 열 너비 (<col>)',
        len(tables_b) == n_tab == len(re.findall(r'(?m)^\|(?:\s*:?-{3,}:?\s*\|)+$', new_md))
        and all('<thead>' in t and '<th scope="col">' in t and '<col style="width:' in t for t in tables_b))
    chk('표 머리 행 음영 = 토큰 (--th) · 테두리 = 토큰 (--line)',
        lambda: bool(re.search(r'(?m)^th\{[^}]*background:var\(--th\)', _css(src_b))) and bool(re.search(r'th,td\{[^}]*border:1px solid var\(--line\)', _css(src_b))))
    chk('색 계열 = docx 의 음영 (머리 행 E6EDF3 · 상자 EAF2FA · 제목 1F4E79 · 글자 1F2933 · 흐린 글 5B6770 · 테두리 B8C4CE)',
        lambda: (lambda t: (t['--th'], t['--box'], t['--acc'], t['--ink'], t['--mut'], t['--line']))
        (dict((k, v.lower()) for k, v in _toks(_css_block(_css(src_b), r'(?m)^:root\{([^}]*)\}')).items()))
        == ('#e6edf3', '#eaf2fa', '#1f4e79', '#1f2933', '#5b6770', '#b8c4ce'))
    s6b = _section(src_b, sid_b('계획: 싼 시험부터'))
    chk('"계획: 싼 시험부터 차례로" 절: 단계 표 (단계 0–7) 와 결과별 갈림 표 (네 줄) · 사이의 굵은 문장',
        len(re.findall(r'<table', s6b)) == 2 and [_vis(x) for x in re.findall(r'<tr><td>(\d)</td>', s6b)] == [str(i) for i in range(8)]
        and '단계 3 의 결과에 따라 3D 를 다르게 짭니다.' in _vis(s6b) and '두 방식의 힘이 뚜렷이 다르다' in _vis(s6b)
        and '이상한 결과가 나왔다' in _vis(s6b))
    gloss_src = md_table_after(new_md, '용어 풀이')[1:]
    s11 = _section(src_b, sid_b('용어 풀이'))
    chk(f'"용어 풀이" 절의 표 {n_gl} 행: 용어 · 뜻이 원고 그대로',
        len(gloss_src) == n_gl and [(_vis(a), _vis(b)) for a, b in re.findall(r'<tr><td>(.*?)</td><td>(.*?)</td></tr>', s11, re.S)]
        == [(_md_cell(r[0]), _md_cell(r[1])) for r in gloss_src])
    refs_b = _section(src_b, 'refs')
    refs_src_b = md_table_after(new_md, '참고문헌')[1:]
    rrows = re.findall(r'<tr id="ref-(\d+)">(.*?)</tr>', refs_b, re.S)
    chk(f'참고문헌 표 {n_ref} 행 (tr id ref-1 … ref-{n_ref}): 번호 · 서지 · 비고가 원고 그대로',
        len(refs_src_b) == n_ref and [n for n, _r in rrows] == [str(i) for i in range(1, n_ref + 1)]
        and all([_vis(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)] == [_md_cell(x) for x in src_r]
                for src_r, (_n, r) in zip(refs_src_b, rrows)))
    dois_b = md_dois(new_md)
    chk(f'원고의 DOI {len(dois_b)} 개가 글자로 남아 있다', len(dois_b) == SHAPE['dois'] and all('doi:' + d in text_b for d in dois_b))
    chk('목록: 글머리 두 단 (ul 안 ul) · 번호 목록 (ol) 이 원고대로',
        bool(re.search(r'<ul>\s*<li>전고체전지의 복합 양극은.*?<ul>\s*<li>활물질 \(AM\):', src_b, re.S))
        and bool(re.search(r'<ol>\s*<li>지금 DEM 에서 MPM 으로 넘기는 것은', src_b)))
    for w in ('진밀도', '1.64', '10–13 %', '하지 않는 말', '11.5 %', '15–18 배', '[8]', '[9]', '[10]'):
        chk(f'원고 핵심이 남아 있다: "{w}"', w in new_md and w in text_b)
    chk(f'마커 날짜 ({date_b}) 가 제목 블록에', bool(date_b) and date_b in _vis(hd))
    #  (b) 와 docx 의 제목 블록은 형식 기준 docx 대로 원고 제목 줄의 부제만 싣는다 ([꼬리표] 는 싣지 않는다) → h1_tag=False
    miss_b = missing_pieces(new_md, text_b, h1_tag=False, ext=True) if new_md and text_b else [(0, '(없음)')]
    chk(f'원고 줄 전수 포함: 원고의 줄 (목록 · 문단 · 표 칸 · 머리 · 그림 캡션) 이 모두 · 원고 순서대로 페이지에 있다 (조각 {len(md_pieces(new_md, False, True))} · 없는 것 {len(miss_b)}'
        f'{" · 첫 줄 " + str(miss_b[0][0]) + " " + miss_b[0][1][:40] if miss_b else ""})', bool(new_md) and not miss_b)
    und_b = undetected_mutations(new_md, text_b, h1_tag=False, ext=True) if new_md and text_b else [(0, '')]
    chk(f'  그 검사는 조각마다 한 글자를 바꾸면 모두 잡는다 (못 잡은 것 {len(und_b)})', bool(new_md) and not und_b)
    chk(f'수식: 페이지의 <math> {sc_b.maths} 개 = 원고의 수식 {len(math_b)} 개 (글 안 / 줄 · LaTeX 주석 · 원고 순서대로)',
        bool(src_b) and [(d, t) for d, t, _b in html_math(src_b)] == [(d, _tex_shown(d, t)) for d, t in math_b] and sc_b.maths == len(math_b))
    chk(f'그림: 페이지의 <figure> {src_b.count("<figure")} 개 = 원고의 그림 줄 {len(figs_b)} 개 (그림 바이트 = 원고 옆 PNG 파일 · 순서대로)',
        bool(src_b) and src_b.count('<figure class="fig">') == len(figs_b)
        and [base64.b64decode(x) for x in _RE_DATA_PNG.findall(src_b)]
        == [_bytes(posixpath.normpath(posixpath.join(NEW_DIR, f[1]))) for f in figs_b])

    print('── ⑥ docx 정본 (형식 기준) · 빌더 JSON')
    dpath = _p(DOCX)
    have = os.path.isfile(dpath)
    paras = docx_paragraphs(dpath) if have else []
    dtext = _norm(' '.join(paras))
    body = docx_body(dpath) if have else None
    chk('정본: A4 · 여백 (위 1440 · 좌우 1440 · 아래 1300)',
        lambda: (lambda s: (s.find(W + 'pgSz').get(W + 'w'), s.find(W + 'pgSz').get(W + 'h'), s.find(W + 'pgMar').get(W + 'top'),
                            s.find(W + 'pgMar').get(W + 'left'), s.find(W + 'pgMar').get(W + 'right'), s.find(W + 'pgMar').get(W + 'bottom')))
        (body.find(W + 'sectPr')) == ('11906', '16838', '1440', '1440', '1440', '1300'))
    chk('정본: 글꼴 = 맑은 고딕 (한글) + Calibri (라틴) · 본문 10.5 pt',
        lambda: (lambda r: (r.find(W + 'rFonts').get(W + 'eastAsia'), r.find(W + 'rFonts').get(W + 'ascii'), r.find(W + 'sz').get(W + 'val')))
        (ET.fromstring(docx_part(dpath, 'word/styles.xml')).find(W + 'docDefaults').find(W + 'rPrDefault').find(W + 'rPr'))
        == ('Malgun Gothic', 'Calibri', '21'))
    chk('정본: 제목 블록 네 줄 (제목 · 부제 · "처음 보는 분을 위한 설명" · 날짜 · 지위 줄)',
        paras[:4] == [TITLE, '가압부터 탈압까지 한 모델로 계산하기', '처음 보는 분을 위한 설명',
                      f'{date_b}  ·  계획 문서  ·  계산 결과는 아직 없음  ·  외부 검토 = 방향은 맞음, 판정 규칙은 고치는 중'])
    chk('정본: "지위:" 문단 · "한 줄로:" 상자 (음영 EAF2FA · 왼쪽 띠)',
        lambda: paras[4].startswith('지위: 계획 문서입니다.') and paras[5].startswith('한 줄로: 전극을 누르는 과정을')
        and [p for p in body.findall(W + 'p') if para_text(p).startswith('한 줄로')][0].find(W + 'pPr').find(W + 'shd').get(W + 'fill') == 'EAF2FA'
        and [p for p in body.findall(W + 'p') if para_text(p).startswith('한 줄로')][0].find(W + 'pPr').find(W + 'pBdr').find(W + 'left') is not None)

    def _styled(style):
        return [p for p in body.iter(W + 'p') if p.find(W + 'pPr') is not None and p.find(W + 'pPr').find(W + 'pStyle') is not None
                and p.find(W + 'pPr').find(W + 'pStyle').get(W + 'val') == style]
    chk(f'정본: Heading1 {n_sec} 개 = 원고의 절 제목 {n_sec} 개 (순서대로)',
        lambda: [para_text(p) for p in _styled('Heading1')] == heads_b and len(heads_b) == n_sec)
    chk(f'정본: 목록 문단 {SHAPE["docx_list_paragraphs"]} (= 원고의 목록 줄 수)',
        lambda: len(_styled('ListParagraph')) == SHAPE['docx_list_paragraphs'] == len(re.findall(r'(?m)^ *(?:- |\d+\. )', new_md)))
    chk(f'정본: 표 {n_tab} · 머리 행 음영 E6EDF3 · 머리 행 반복 (tblHeader)',
        lambda: len(body.findall(W + 'tbl')) == n_tab and all(
            all(tc.find(W + 'tcPr').find(W + 'shd').get(W + 'fill') == 'E6EDF3' for tc in t.find(W + 'tr').findall(W + 'tc'))
            and t.find(W + 'tr').find(W + 'trPr').find(W + 'tblHeader') is not None for t in body.findall(W + 'tbl')))

    def _tbl(first_head):
        """정본의 표 가운데 머리 행 첫 칸의 글이 first_head 인 것 (하나여야 한다)."""
        hits = [t for t in body.findall(W + 'tbl') if para_text(t.find(W + 'tr').find(W + 'tc')) == first_head]
        return hits[0] if len(hits) == 1 else None
    chk(f'정본: 용어 풀이 표 {n_gl} 행 (+ 머리) · 참고문헌 표 {n_ref} 행 (+ 머리)',
        lambda: (len(_tbl('용어').findall(W + 'tr')), len(_tbl('#').findall(W + 'tr'))) == (n_gl + 1, n_ref + 1))
    chk(f'정본: 용어 풀이 {n_gl} 행의 용어가 원고 그대로',
        lambda: [para_text(tr.find(W + 'tc')) for tr in _tbl('용어').findall(W + 'tr')[1:]] == [_md_cell(r[0]) for r in gloss_src]
        and len(gloss_src) == n_gl)
    chk('정본: 바닥글 = 제목 · 쪽 번호 (PAGE / NUMPAGES)',
        lambda: (lambda f: TITLE in f and '>PAGE<' in f and '>NUMPAGES<' in f)(docx_part(dpath, 'word/footer1.xml').decode('utf-8')))
    for w in ('진밀도', '1.64', '10–13 %', '하지 않는 말'):
        chk(f'정본: 원고 핵심 "{w}"', w in new_md and w in dtext)
    chk(f'정본: 원고의 DOI {len(dois_b)} 개 전부 · 참고문헌 {n_ref} 행의 서지', len(dois_b) == SHAPE['dois'] and all('doi:' + d in dtext for d in dois_b)
        and len(refs_src_b) == n_ref and all(_md_cell(r[1]) in dtext for r in refs_src_b))
    chk(f'정본: 마커 날짜 ({date_b})', bool(date_b) and date_b in dtext)
    miss_d = missing_pieces(new_md, dtext, h1_tag=False, ext=True) if new_md and dtext else [(0, '(없음)')]
    chk(f'정본: 원고의 본문 줄 (목록 · 문단 · 표 칸 · 머리 · 그림 캡션) 이 정본 글과 어긋나지 않는다: 모두 · 원고 순서대로 (조각 {len(md_pieces(new_md, False, True))} · 없는 것 {len(miss_d)}'
        f'{" · 첫 줄 " + str(miss_d[0][0]) + " " + miss_d[0][1][:40] if miss_d else ""})', bool(new_md) and not miss_d)
    one = new_md.replace('무른 알갱이입니다', '무른 알갱이입니당', 1)
    chk('  원고를 한 글자 바꾼 사본이면 그 검사가 실패한다 (바꾼 줄을 짚는다)',
        bool(dtext) and one != new_md and [i for i, _p2 in missing_pieces(one, dtext, h1_tag=False, ext=True)]
        == [next(i for i, s in enumerate(new_md.split('\n'), 1) if '무른 알갱이입니다' in s)])
    und_d = undetected_mutations(new_md, dtext, h1_tag=False, ext=True) if new_md and dtext else [(0, '')]
    chk(f'  조각마다 한 글자를 바꿔도 모두 잡는다 (못 잡은 것 {len(und_d)})', bool(new_md) and not und_d)
    chk(f'정본: 수식 (m:oMath) · 줄 수식 (m:oMathPara) · 그림 (w:drawing) 의 수 = 원고의 수식 {len(math_b)} · 그림 {len(figs_b)}',
        lambda: docx_math_counts(dpath) == (len(math_b), len([1 for d, _t in math_b if d]))
        and len(list(body.iter(W + 'drawing'))) == len(figs_b))
    model = {}
    try:
        model = json.loads(_read(OUT_MODEL))
    except Exception as e:      # noqa: BLE001
        print(f'        (JSON 읽기 실패: {type(e).__name__}: {e})')
    chk('JSON: 커밋돼 있고 원고 경로 · sha256 · 마커 날짜를 싣는다',
        lambda: model['source'] == SRC_NEW and model['source_sha256'] == hashlib.sha256(_bytes(SRC_NEW)).hexdigest() and model['date'] == date_b)
    chk('JSON 의 문단 글 · 순서 = 정본 docx 의 문단 글 · 순서 (전수)',
        lambda: model_paragraphs(model) == paras and len(paras) == SHAPE['docx_paragraphs'])
    chk('JSON 의 수식 (글 안 / 줄 · 순서) · 그림 (경로 · 순서) = 원고의 수식 · 그림',
        lambda: [k for k, _o in model_math(model)] == [d for d, _t in math_b]
        and [b['path'] for b in model['blocks'] if b['t'] == 'fig'] == [posixpath.normpath(posixpath.join(NEW_DIR, f[1])) for f in figs_b])
    chk(f'JSON: 표 {n_tab} · 열 너비 합 = 본문 너비 9026 · 정본의 열 너비와 같다',
        lambda: [b['widths'] for b in model['blocks'] if b['t'] == 'table']
        == [[int(g.get(W + 'w')) for g in t.find(W + 'tblGrid')] for t in body.findall(W + 'tbl')]
        and all(sum(b['widths']) == 9026 for b in model['blocks'] if b['t'] == 'table'))
    chk('JSON · 생성기 · 빌더에 em dash · 모델 이름 · 절대 경로 없음 (이 시험 파일 = em dash 만: 금지 낱말의 정규식을 싣고 있다)',
        lambda: all(bool(t) and EM_DASH not in t and not RE_MODEL.search(t) and not RE_ABS.search(t)
                    for t in (_read(OUT_MODEL), _read(GEN), _read(BUILDER)))
        and EM_DASH not in _read('webapp/test_dem_redesign_plan_page.py'))

    print('── ⑦ 서로 링크 · 사이드바 · 실제 서빙')
    chk('(a) 머리에서 (b) 로: 링크 글 "처음 보는 분을 위한 설명"',
        bool(re.search(r'<a class="sib" href="%s">처음 보는 분을 위한 설명</a>' % re.escape(URL_NEW), src_a)))
    chk('(b) 머리에서 (a) 로: 링크 글 "자세한 계획서"',
        bool(re.search(r'<a class="sib" href="%s">자세한 계획서</a>' % re.escape(URL_PLAN), src_b)))
    base = _read(BASE)
    li = re.search(r'<li><a href="%s"\s+title="([^"]+)">\s*<span class="icon">[^<]+</span> DEM 재설계 계획서 \(수영\)\s*</a></li>' % re.escape(URL_PLAN), base)
    chk('base.html 사이드바에 <li> 하나: 링크 = 페이지 (a) · 글 "DEM 재설계 계획서 (수영)" · 짧은 한국어 title',
        bool(li) and base.count(URL_PLAN) == 1 and bool(re.search(r'[가-힣]', li.group(1))) and len(li.group(1)) <= 90)
    chk('  그 <li> 는 "Rint 설명" 바로 뒤 · "DEM 방법 그림" 앞 · 이웃과 같은 꼴의 Jinja 주석 (이 시험 이름)',
        lambda: base.index('/static/explain/rint_overview_20261021.html') < base.index(URL_PLAN) < base.index('/static/dem_method_figs/index.html')
        and bool(re.search(r'Rint 설명\s*</a></li>\s*\{#[^#]*webapp/test_dem_redesign_plan_page\.py[^#]*#\}\s*<li><a href="%s"' % re.escape(URL_PLAN), base)))
    mine = re.search(r'\{# 11-10: DEM 재설계[^#]*#\}\s*<li><a href="%s".*?</a></li>' % re.escape(URL_PLAN), base, re.S)
    chk('  base.html 의 새 줄 (주석 + <li>) 에 em dash · 모델 이름 · 절대 경로 없음',
        bool(mine) and EM_DASH not in mine.group(0) and not RE_MODEL.search(mine.group(0)) and not RE_ABS.search(mine.group(0)))
    try:
        import app as webapp
        c = webapp.app.test_client()
    except Exception as e:      # noqa: BLE001
        c = None
        print(f'        (앱 import 실패: {type(e).__name__}: {e})')
    for label, url, rel in (('(a)', URL_PLAN, OUT_PLAN), ('(b)', URL_NEW, OUT_NEW)):
        r = c.get(url) if c else None
        chk(f'GET {url} → 200', r is not None and r.status_code == 200)
        chk(f'{label} text/html 로 서빙', r is not None and r.status_code == 200 and (r.mimetype or '') == 'text/html')
        chk(f'{label} 서빙된 바이트 = 리포 파일', r is not None and r.status_code == 200 and bool(_bytes(rel)) and r.get_data() == _bytes(rel))
    r2 = c.get('/seminar') if c else None
    chk('렌더된 화면 (/seminar) 사이드바에 링크가 보인다',
        r2 is not None and r2.status_code == 200 and f'href="{URL_PLAN}"' in r2.get_data(as_text=True)
        and 'DEM 재설계 계획서 (수영)' in r2.get_data(as_text=True))
    gate = _read('scripts/check_all.sh')
    chk('게이트 (scripts/check_all.sh) 에 이 시험 단계 한 줄', len(re.findall(r"(?m)^run 'webapp: dem_redesign_plan[^']*'\s+python3 webapp/test_dem_redesign_plan_page\.py\s*$", gate)) == 1)

    print('── ⑧ docx 빌더 (node · docx 모듈이 있을 때만)')
    node = shutil.which('node')
    have_docx = bool(node) and subprocess.run([node, '-e', "require('docx')"], capture_output=True).returncode == 0
    chk('빌더 scripts/build_dem_redesign_plan_docx.js 가 있고 머리 주석에 정본을 바꾸는 절차가 있다',
        lambda: all(w in _read(BUILDER)[:4000] for w in ('정본', 'sha256', '--write', OUT_MODEL.split('/')[-1])))
    if not have_docx:
        print('  SKIP  node 또는 docx 모듈이 없다: 빌더 실행 검사를 건너뜀 (세지 않는다)')
    else:
        ver = subprocess.run([node, '-e', _JS_DOCX_VERSION], capture_output=True, text=True).stdout.strip()
        tmp2 = tempfile.mkdtemp(prefix='dem_plan_docx_')
        try:
            out = os.path.join(tmp2, 'built.docx')
            pr = subprocess.run([node, _p(BUILDER), '--json', _p(OUT_MODEL), '--out', out], capture_output=True, text=True, cwd=tmp2)
            chk(f'빌더 실행 rc 0 · docx 를 쓴다 (docx 모듈 {ver or "?"}{" · " + pr.stderr.strip()[:100] if pr.returncode else ""})',
                pr.returncode == 0 and os.path.isfile(out))
            chk('빌더 출력의 문단 글 · 순서 = 정본 (빈 문단까지)',
                lambda: [para_text(p) for p in docx_body(out).iter(W + 'p')] == [para_text(p) for p in docx_body(dpath).iter(W + 'p')])
            chk('빌더 출력의 문서 속성 (제목 · 만든 이 · 설명) = 정본',
                lambda: core_props(docx_part(out, 'docProps/core.xml')) == core_props(docx_part(dpath, 'docProps/core.xml'))
                and core_props(docx_part(dpath, 'docProps/core.xml'))[0] == TITLE)
            if ver != DOCX_JS_VERSION:
                #  다른 판의 docx 모듈은 같은 문서를 자잘하게 다른 XML 로 적을 수 있다 (리포 결함이 아니다) → 엄격 대조는 그 판에서만.
                print(f'  SKIP  docx 모듈이 {ver or "?"} (정본을 만든 판 {DOCX_JS_VERSION} 아님): XML 엄격 대조를 건너뜀 (세지 않는다)')
            else:
                for part in ('word/document.xml', 'word/styles.xml', 'word/numbering.xml', 'word/footer1.xml', 'word/settings.xml'):
                    chk(f'빌더 출력의 {part} = 정본 (요소 · 속성 · 글 · 순서)',
                        lambda part=part: xml_canon(docx_part(out, part)) == xml_canon(docx_part(dpath, part)))
            chk(f'빌더 출력의 수식 · 줄 수식 · 그림 수 = 원고의 수 ({len(math_b)} · {len([1 for d, _t in math_b if d])} · {len(figs_b)})',
                lambda: docx_math_counts(out) == (len(math_b), len([1 for d, _t in math_b if d]))
                and len(list(docx_body(out).iter(W + 'drawing'))) == len(figs_b))
            chk('빌더 출력 ZIP 에 폴더 항목이 없다 (Word 클라우드 공동 편집이 거부한 꼴)',
                lambda: not [n for n in zipfile.ZipFile(out).namelist() if n.endswith('/')])
            chk('빌더는 --out 없이 돌리면 쓰지 않고 rc 2 (정본을 실수로 덮지 않는다)',
                lambda: subprocess.run([node, _p(BUILDER)], capture_output=True, text=True, cwd=tmp2).returncode == 2
                and os.listdir(tmp2) == ['built.docx'])
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)

    print('── ⑨ 수식 · 그림 고정물 (짧은 원고 조각 → 페이지 · JSON · docx)')
    fix_md, fix_png = _read(FIX_MD), _bytes(FIX_PNG)
    fmath, ffigs = md_math(fix_md), md_figures(fix_md)
    n_disp = len([1 for d, _t in fmath if d])
    chk('고정물 셋이 제자리에 (원고 조각 · PNG · 수식 캐시) · PNG 는 작다 (4 KB 아래)',
        bool(fix_md) and fix_png[:8] == PNG_HEAD[:8] and 0 < len(fix_png) < 4096 and bool(_bytes(FIX_MATH)))
    chk(f'고정물 원고: 줄 수식 둘 · 글 안 수식 · 그림 하나 · 분수 · 첨자 · 합 기호 · 식 번호가 있다 (수식 {len(fmath)} · 그림 {len(ffigs)})',
        n_disp == 2 and len(fmath) - n_disp >= 5 and len(ffigs) == 1
        and all(any(w in t for _d, t in fmath) for w in ('\\frac', '\\sum', '_', '^', '\\tag')))
    fx = None
    try:
        fx = gen.build_newcomer(ROOT, FIX_MD)       # 변환기 없이 부른다: 수식은 커밋된 캐시에서만 읽는다 (pandoc 을 부르지 않는다)
    except Exception as e:      # noqa: BLE001
        print(f'        (고정물 빌드 실패: {type(e).__name__}: {e})')
    fpage, fmodel_b, fcache = fx if fx else (b'', b'', None)
    chk('고정물 → 페이지 · JSON 을 pandoc 없이 만든다 · 다시 낸 수식 캐시 = 커밋된 캐시 바이트',
        bool(fpage) and bool(fmodel_b) and fcache is not None and fcache == _bytes(FIX_MATH))
    chk('  두 번 만들면 같은 바이트', lambda: fx is not None and gen.build_newcomer(ROOT, FIX_MD) == fx)
    fsrc, fsc = closed_file_checks('(고정물)', None, URL_PLAN, page=fpage, images=1)
    fcss = _css(fsrc)
    fmaths = html_math(fsrc)
    fblocks = [b for d, _t, b in fmaths if d]
    chk(f'고정물 페이지: 수식 {len(fmaths)} 개 = 원고의 수식 {len(fmath)} 개 (글 안 / 줄 · LaTeX 주석 · 원고 순서대로)',
        bool(fmath) and [(d, t) for d, t, _b in fmaths] == [(d, _tex_shown(d, t)) for d, t in fmath] and fsc.maths == len(fmath))
    chk('고정물 페이지: 줄 수식 = <div class="eq"> 안의 <math display="block"> · 분수 (mfrac) · 아래첨자 (msub) · 위아래 끝을 단 합 기호 (munderover · ∑)',
        lambda: fsrc.count('<div class="eq"><math display="block"') == len(fblocks) == 2
        and all(w in fblocks[0] for w in ('<mfrac>', '<msub>', '<munderover>', '∑')))
    chk('고정물 페이지: 식 번호 (원고의 \\tag{1}) 가 식 끝의 글자 "(1)" 로 · 위첨자 (msup) 가 든 글 안 수식',
        lambda: bool(re.search(r'<mtext[^>]*>\(1\)</mtext>', fblocks[0])) and any('<msup>' in b for d, _t, b in fmaths if not d))
    chk('고정물 페이지: 수식 안에 바깥 것이 없다 (script · 링크 · 그림 0) · 수식 글꼴 · 줄 수식 가로 스크롤 규칙이 CSS 에',
        bool(fmaths) and all('<script' not in b and 'href' not in b and 'src=' not in b for _d, _t, b in fmaths)
        and bool(re.search(r'(?m)^math\{[^}]*font-family:', fcss)) and bool(re.search(r'(?m)^\.eq\{[^}]*overflow-x:auto', fcss)))
    fig = re.search(r'<figure class="fig">\s*<img ([^>]*)>\s*<figcaption>(.*?)</figcaption>\s*</figure>', fsrc, re.S)
    chk('고정물 페이지: 그림 = <figure> 안의 <img> (PNG 를 data URI 로: 바이트 = 고정물 PNG) 와 그 아래 <figcaption>',
        bool(fig) and [base64.b64decode(x) for x in _RE_DATA_PNG.findall(fsrc)] == [fix_png])
    chk('고정물 페이지: 그림 폭 = 원고의 {width=60%} · width · height 속성 = PNG 의 가로 · 세로 (360 x 220) · alt = 캡션 글',
        bool(fig) and 'style="width:60%"' in fig.group(1) and 'width="360" height="220"' in fig.group(1)
        and 'alt="그림 1. 격자 마디와 물질점' in fig.group(1))
    chk('고정물 페이지: 캡션은 그림 아래 · 가운데 · 작은 흐린 글 (CSS) · 캡션 안의 글 안 수식 셋',
        bool(fig) and fig.group(2).count('<math display="inline"') == 3 and bool(re.search(r'(?m)^\.fig\{[^}]*text-align:center', fcss))
        and bool(re.search(r'\.fig figcaption\{[^}]*color:var\(--mut\)', fcss)) and bool(re.search(r'\.fig img\{[^}]*max-width:100%', fcss)))
    chk('고정물 페이지: 표 칸 · 번호 목록 · "한 줄로" 상자 안의 글 안 수식',
        bool(re.search(r'<td>기공률 <math display="inline"', fsrc)) and bool(re.search(r'<ol>\s*<li>원의 넓이는 <math display="inline"', fsrc))
        and bool(re.search(r'<div class="oneline">[^\n]*<math display="inline"', fsrc)))
    chk('고정물 페이지: 인쇄할 때 수식 · 그림이 쪽 끝에서 갈리지 않는다 (.fig · .eq break-inside:avoid)',
        bool(re.search(r'[,}]\.fig,\.eq\{break-inside:avoid\}', fcss)))
    fmiss = missing_pieces(fix_md, fsc.visible, h1_tag=False, ext=True) if fix_md and fsrc else [(0, '(없음)')]
    chk(f'고정물 페이지: 원고 조각의 글 (문단 · 목록 · 표 칸 · 머리 · 캡션) 이 모두 · 순서대로 (조각 {len(md_pieces(fix_md, False, True))} · 없는 것 {len(fmiss)}'
        f'{" · 첫 줄 " + str(fmiss[0][0]) + " " + fmiss[0][1][:40] if fmiss else ""})', bool(fix_md) and not fmiss)
    fund = undetected_mutations(fix_md, fsc.visible, h1_tag=False, ext=True) if fix_md and fsrc else [(0, '')]
    chk(f'  조각마다 한 글자를 바꾸면 모두 잡는다 (못 잡은 것 {len(fund)})', bool(fix_md) and not fund)

    fmodel = {}
    try:
        fmodel = json.loads(fmodel_b.decode('utf-8'))
    except Exception as e:      # noqa: BLE001
        print(f'        (고정물 JSON 읽기 실패: {type(e).__name__}: {e})')
    fomml = model_math(fmodel) if fmodel else []
    chk('고정물 JSON: 수식 (글 안 / 줄 · 순서) = 원고 · 줄 수식 블록은 m:oMathPara · 글 안 수식 런은 m:oMath',
        bool(fomml) and [k for k, _o in fomml] == [d for d, _t in fmath]
        and all(o.startswith('<m:oMathPara>') == k and o.startswith('<m:oMath') for k, o in fomml))
    chk('고정물 JSON: 그림 블록 = 경로 · sha256 · 제 크기 · docx 에 실을 크기 (본문 폭 601 px 의 60 % = 361 x 221) · alt · 캡션 런',
        lambda: [(b['path'], b['sha256'], b['px'], b['width'], b['height'], bool(b['caption'])) for b in fmodel['blocks'] if b['t'] == 'fig']
        == [(FIX_PNG, hashlib.sha256(fix_png).hexdigest(), [360, 220], 361, 221, True)]
        and all(b['alt'].startswith('그림 1. 격자 마디와 물질점') and 'w_{ip}' in b['alt'] for b in fmodel['blocks'] if b['t'] == 'fig'))
    chk('고정물 JSON 의 문단 글 = 원고 조각의 글 (순서대로 · 수식 자리는 글이 아니다)',
        lambda: not missing_pieces(fix_md, _norm(' '.join(model_paragraphs(fmodel))), h1_tag=False, ext=True) and len(model_paragraphs(fmodel)) >= 12)
    fcache_obj = {}
    try:
        fcache_obj = json.loads(_read(FIX_MATH))
    except Exception as e:      # noqa: BLE001
        print(f'        (고정물 수식 캐시 읽기 실패: {type(e).__name__}: {e})')
    chk('고정물 수식 캐시: schema · 식마다 latex · display · mathml · omml · pandoc 판 · 겹치는 식은 한 번 (원고에 처음 나온 순서)',
        lambda: fcache_obj['schema'] == 'dem_redesign_plan_math/1'
        and [(e['display'], e['latex']) for e in fcache_obj['entries']] == list(dict.fromkeys(fmath))
        and all(e['mathml'].startswith('<math display="') and e['omml'].startswith('<m:oMath') and e['pandoc'] for e in fcache_obj['entries']))

    def _omml_ok(omml):
        """OMML 조각이 온전한 XML 이고 (m: 요소만) Word 스키마 순서를 지킨다 (괄호 속성: sepChr 가 endChr 앞 · 보통 글 런에 sty 없음)."""
        root = ET.fromstring('<r xmlns:m="%s">%s</r>' % (M_NS, omml))
        for el in root.iter():
            kids = [c.tag for c in el]
            if el is not root and not el.tag.startswith(MM):
                return False
            if el.tag == MM + 'dPr' and MM + 'sepChr' in kids and MM + 'endChr' in kids and kids.index(MM + 'sepChr') > kids.index(MM + 'endChr'):
                return False
            if el.tag == MM + 'rPr' and MM + 'nor' in kids and MM + 'sty' in kids:
                return False
            if el.tag == MM + 'mcPr' and MM + 'count' in kids and MM + 'mcJc' in kids and kids.index(MM + 'count') > kids.index(MM + 'mcJc'):
                return False
        return True
    chk('OMML 스키마 순서 고침 (_omml_fix): 괄호 속성 (sepChr 가 endChr 앞) · 보통 글 런의 겹친 글자 꼴 · 행렬 열 속성 (count 가 mcJc 앞) · 그 밖은 그대로',
        lambda: gen._omml_fix('<m:dPr><m:begChr m:val="(" /><m:endChr m:val=")" /><m:sepChr m:val="" /><m:grow /></m:dPr>')
        == '<m:dPr><m:begChr m:val="(" /><m:sepChr m:val="" /><m:endChr m:val=")" /><m:grow /></m:dPr>'
        and gen._omml_fix('<m:rPr><m:nor /><m:sty m:val="p" /></m:rPr>') == '<m:rPr><m:nor /></m:rPr>'
        and gen._omml_fix('<m:mcPr><m:mcJc m:val="center" /><m:count m:val="2" /></m:mcPr>')
        == '<m:mcPr><m:count m:val="2" /><m:mcJc m:val="center" /></m:mcPr>'
        and gen._omml_fix('<m:r><m:rPr><m:sty m:val="b" /></m:rPr><m:t>v</m:t></m:r>') == '<m:r><m:rPr><m:sty m:val="b" /></m:rPr><m:t>v</m:t></m:r>'
        and all(_omml_ok(gen._omml_fix(x)) and not _omml_ok(x) for x in (
            '<m:d><m:dPr><m:begChr m:val="(" /><m:endChr m:val=")" /><m:sepChr m:val="" /></m:dPr><m:e><m:r><m:t>x</m:t></m:r></m:e></m:d>',
            '<m:r><m:rPr><m:nor /><m:sty m:val="p" /></m:rPr><m:t>x</m:t></m:r>',
            '<m:m><m:mPr><m:mcs><m:mc><m:mcPr><m:mcJc m:val="center" /><m:count m:val="2" /></m:mcPr></m:mc></m:mcs></m:mPr></m:m>')))
    chk('고정물 수식 캐시: OMML 이 온전한 XML (m: 요소만 · xmlns 선언 없음) · Word 스키마 순서 · MathML 도 온전한 XML',
        lambda: len(fcache_obj['entries']) >= 7 and all(_omml_ok(e['omml']) and 'xmlns' not in e['omml']
                                                        and ET.fromstring(e['mathml']).tag == 'math' for e in fcache_obj['entries']))
    good = (fcache_obj.get('entries') or [{}])[0]
    gm, go = good.get('mathml', ''), good.get('omml', '')
    #  페이지 · docx 는 변환을 바이트 그대로 싣는다 → 수식 아닌 것이 섞인 변환은 생성기가 받지 않아야 한다 (pandoc 이 낸 것도 · 캐시도)
    bads = (
        ('MathML 안의 script', dict(good, mathml=gm.replace('<mi>', '<script>x</script><mi>', 1))),
        ('MathML 안의 그림', dict(good, mathml=gm.replace('<mi>', '<img src="x.png"><mi>', 1))),
        ('MathML 의 링크 속성', dict(good, mathml=gm.replace('<mi>', '<mi href="x">', 1))),
        ('MathML 의 이벤트 속성', dict(good, mathml=gm.replace('<mi>', '<mi onclick="x">', 1))),
        ('MathML 안의 주소 글', dict(good, mathml=gm.replace('<mi>', '<mtext>http</mtext><mi>', 1))),
        ('MathML 둘', dict(good, mathml=gm + gm)),
        ('줄 수식 / 글 안 수식이 뒤바뀜', dict(good, display=not good.get('display', False))),
        ('OMML 안의 w: 요소', dict(good, omml=go.replace('<m:r>', '<w:r></w:r><m:r>', 1))),
        ('OMML 의 r:id 속성', dict(good, omml=go.replace('<m:r>', '<m:r r:id="rId9">', 1))),
        ('OMML 의 xmlns 선언', dict(good, omml=go.replace('<m:r>', '<m:r xmlns:x="y">', 1))),
        ('OMML 둘', dict(good, omml=go + go)),
        ('latex 가 글이 아님', dict(good, latex=3)),
    )
    chk(f'수식 변환 검사 (math_entry_problem): 고정물 캐시의 식은 모두 받고 · 수식 아닌 것이 섞인 변환 {len(bads)} 가지는 모두 거부한다',
        lambda: bool(gm) and bool(go) and all(gen.math_entry_problem(e) is None for e in fcache_obj['entries'])
        and all(b != good and isinstance(gen.math_entry_problem(b), str) for _n, b in bads))
    tmp4 = tempfile.mkdtemp(prefix='dem_plan_fix_')
    try:
        for rel in (FIX_MD, FIX_PNG, FIX_MATH):
            os.makedirs(os.path.dirname(_p(rel, tmp4)), exist_ok=True)
            shutil.copyfile(_p(rel), _p(rel, tmp4))

        def _cache_refused(entry):
            """고정물 캐시의 첫 식을 entry 로 바꾸면 (변환기 없이) 생성기가 캐시 파일을 짚고 멈춘다."""
            obj = json.loads(_read(FIX_MATH))
            obj['entries'][0] = entry
            with open(_p(FIX_MATH, tmp4), 'w', encoding='utf-8', newline='') as f:
                f.write(json.dumps(obj, ensure_ascii=False, indent=1) + '\n')
            try:
                gen.build_newcomer(tmp4, FIX_MD)
            except gen.ParseError as e:
                return e.name == FIX_MATH and e.line == 1
            finally:
                shutil.copyfile(_p(FIX_MATH), _p(FIX_MATH, tmp4))
            return False
        chk('  캐시 파일에 그런 변환이 들어 있으면 페이지를 만들지 않고 멈춘다 (캐시 파일 이름 · 줄 1)',
            lambda: all(_cache_refused(b) for _n, b in bads) and len(bads) == 12)
        keep2 = getattr(gen, 'pandoc_version', None)
        try:
            if gen is not None:
                gen.pandoc_version = lambda: None       # pandoc 이 없는 기계처럼
            chk('--write-math-cache <고정물>: 캐시가 다 있으면 pandoc 없이도 같은 바이트를 쓴다 (rc 0)',
                lambda: gmain(['--write-math-cache', FIX_MD], root=tmp4) == 0 and _bytes(FIX_MATH, tmp4) == _bytes(FIX_MATH))
            chk('  캐시가 없으면 (pandoc 도 없으면) rc 2 · 캐시 파일을 만들지 않는다',
                lambda: (os.remove(_p(FIX_MATH, tmp4)), gmain(['--write-math-cache', FIX_MD], root=tmp4))[1] == 2
                and not os.path.exists(_p(FIX_MATH, tmp4)))
        finally:
            if gen is not None:
                gen.pandoc_version = keep2
        pv = gen.pandoc_version() if gen is not None else None
        if pv != PANDOC_VERSION:
            print(f'  SKIP  pandoc 이 {pv or "없다"} (캐시를 만든 판 {PANDOC_VERSION} 이 아니다): 캐시 재현 검사를 건너뜀 (세지 않는다)')
        else:
            chk(f'pandoc {PANDOC_VERSION} 으로 캐시를 처음부터 다시 만들면 커밋된 캐시와 같은 바이트 (--write-math-cache)',
                lambda: gmain(['--write-math-cache', FIX_MD], root=tmp4) == 0 and _bytes(FIX_MATH, tmp4) == _bytes(FIX_MATH))

        if not have_docx:
            print('  SKIP  node 또는 docx 모듈이 없다: 고정물 docx 검사를 건너뜀 (세지 않는다)')
        else:
            mjson, fout = os.path.join(tmp4, 'fixture_model.json'), os.path.join(tmp4, 'fixture.docx')
            with open(mjson, 'wb') as f:
                f.write(fmodel_b)
            pr = subprocess.run([node, _p(BUILDER), '--json', mjson, '--root', ROOT, '--out', fout], capture_output=True, text=True, cwd=tmp4)
            chk(f'고정물 docx: 빌더 실행 rc 0{" · " + pr.stderr.strip()[:100] if pr.returncode else ""}', pr.returncode == 0 and os.path.isfile(fout))
            dxml, fbody, fps = '', None, []
            try:
                dxml = docx_part(fout, 'word/document.xml').decode('utf-8')
                fbody = docx_body(fout)
                fps = list(fbody.iter(W + 'p'))
            except Exception as e:      # noqa: BLE001
                print(f'        (고정물 docx 읽기 실패: {type(e).__name__}: {e})')
            chk('고정물 docx: document.xml 이 온전한 XML · 수식 자리 표지가 남지 않았다', fbody is not None and '@@DEMPLAN' not in dxml)
            chk(f'고정물 docx: Word 수식 (m:oMath) = 원고의 수식 {len(fmath)} 개 · 줄 수식 (m:oMathPara) = {n_disp} 개',
                lambda: docx_math_counts(fout) == (len(fmath), n_disp) and len(fmath) >= 7)
            chk('고정물 docx: 분수 (m:f) · 아래첨자 (m:sSub) · 위첨자 (m:sSup) · 합 기호 (m:nary · ∑) 가 OMML 요소로',
                lambda: all(next(fbody.iter(MM + t), None) is not None for t in ('f', 'sSub', 'sSup', 'nary'))
                and any(e.get(MM + 'val') == '∑' for e in fbody.iter(MM + 'chr')))
            chk('고정물 docx: 끼워 넣은 OMML = JSON 이 실은 OMML (바이트 그대로 · 문서 순서)',
                lambda: bool(fomml) and re.findall(r'<m:oMathPara>.*?</m:oMathPara>|<m:oMath>.*?</m:oMath>', dxml, re.S) == [o for _k, o in fomml])
            chk('고정물 docx: 줄 수식은 문단 바로 아래의 m:oMathPara · 가운데 맞춤 (m:jc center)',
                lambda: sum(len(p.findall(MM + 'oMathPara')) for p in fps) == n_disp == len(list(fbody.iter(MM + 'jc')))
                and all(e.get(MM + 'val') == 'center' for e in fbody.iter(MM + 'jc')))

            def _spacing(p):
                ppr = p.find(W + 'pPr')
                sp = ppr.find(W + 'spacing') if ppr is not None else None
                return (sp.get(W + 'line'), sp.get(W + 'lineRule')) if sp is not None else (None, None)

            def _jc(p):
                ppr = p.find(W + 'pPr')
                jc = ppr.find(W + 'jc') if ppr is not None else None
                return jc.get(W + 'val') if jc is not None else None
            with_m = [p for p in fps if next(p.iter(MM + 'oMath'), None) is not None and _spacing(p)[0]]
            without = [p for p in fps if next(p.iter(MM + 'oMath'), None) is None]
            chk(f'고정물 docx: 글 안 수식이 든 문단 ({len(with_m)}) 은 줄 간격 규칙 "auto" 를 적는다 (키 큰 수식에 줄이 늘어난다) · 수식이 없는 문단은 정본처럼 적지 않는다',
                lambda: len(with_m) >= 6 and all(_spacing(p)[1] == 'auto' for p in with_m) and bool(without) and all(_spacing(p)[1] is None for p in without))
            media = [n for n in zipfile.ZipFile(fout).namelist() if n.startswith('word/media/')] if os.path.isfile(fout) else []
            chk('고정물 docx: 그림 관계 하나 (…/relationships/image → media/….png) · 그 파일의 바이트 = 고정물 PNG · w:drawing 하나',
                lambda: len(re.findall(r'Type="[^"]*/relationships/image"\s+Target="media/[^"]+\.png"',
                                       docx_part(fout, 'word/_rels/document.xml.rels').decode('utf-8'))) == 1
                and len(media) == 1 and docx_part(fout, media[0]) == fix_png and len(list(fbody.iter(W + 'drawing'))) == 1)
            wp = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'
            chk('고정물 docx: 그림 크기 = 본문 폭의 60 % (361 x 221 px · 1 px = 9525 EMU) · 본문 폭 (9026 DXA = 5731510 EMU) 안',
                lambda: [(e.get('cx'), e.get('cy')) for e in fbody.iter(wp + 'extent')] == [(str(361 * 9525), str(221 * 9525))]
                and 361 * 9525 <= 9026 * 635)
            idx = next((i for i, p in enumerate(fps) if next(p.iter(W + 'drawing'), None) is not None), None)
            chk('고정물 docx: 그림 문단은 가운데 · 바로 다음 문단이 캡션 (가운데 · "그림 1." 로 시작 · 글 안 수식 셋)',
                lambda: _jc(fps[idx]) == 'center' and _jc(fps[idx + 1]) == 'center'
                and para_text(fps[idx + 1]).startswith('그림 1. 격자 마디와 물질점') and len(list(fps[idx + 1].iter(MM + 'oMath'))) == 3)
            chk('고정물 docx: 문단 글 · 순서 = JSON 의 문단 글 · 순서',
                lambda: [s for s in (para_text(p) for p in fps) if s] == model_paragraphs(fmodel) and len(fps) >= 12)
            chk('고정물 docx: ZIP 에 폴더 항목 없음 · [Content_Types].xml 에 png',
                lambda: not [n for n in zipfile.ZipFile(fout).namelist() if n.endswith('/')]
                and 'image/png' in docx_part(fout, '[Content_Types].xml').decode('utf-8'))
            bad_json, bad_out = os.path.join(tmp4, 'bad_model.json'), os.path.join(tmp4, 'bad.docx')

            def _builder_refuses(change):
                """모델을 change 로 망가뜨리면 빌더가 쓰지 않고 멈춘다 (rc 1 · 출력 파일 없음)."""
                m2 = json.loads(fmodel_b.decode('utf-8'))
                change(m2)
                with open(bad_json, 'w', encoding='utf-8') as f:
                    json.dump(m2, f, ensure_ascii=False)
                if os.path.exists(bad_out):
                    os.remove(bad_out)
                rc = subprocess.run([node, _p(BUILDER), '--json', bad_json, '--root', ROOT, '--out', bad_out], capture_output=True, text=True, cwd=tmp4).returncode
                return rc == 1 and not os.path.exists(bad_out)
            chk('빌더: 그림 파일이 JSON 의 sha256 과 다르면 쓰지 않고 멈춘다',
                lambda: _builder_refuses(lambda m2: [b.update(sha256='0' * 64) for b in m2['blocks'] if b['t'] == 'fig']))
            chk('빌더: 그림 경로가 리포 밖을 가리키면 (..) 쓰지 않고 멈춘다',
                lambda: _builder_refuses(lambda m2: [b.update(path='../' + b['path']) for b in m2['blocks'] if b['t'] == 'fig']))
            chk('빌더: 수식이 OMML 꼴이 아니면 쓰지 않고 멈춘다',
                lambda: _builder_refuses(lambda m2: [b.update(omml='<w:r><w:t>x</w:t></w:r>') for b in m2['blocks'] if b['t'] == 'eq']))
    finally:
        shutil.rmtree(tmp4, ignore_errors=True)

    print(f'\n== test_dem_redesign_plan_page: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('   실패: ' + ' · '.join(f[:70] for f in _fail))
    return 0 if not _fail else 1


def _raises(gen, text, name):
    try:
        gen.parse(text, name)
    except gen.ParseError as e:
        return e
    return ''


if __name__ == '__main__':
    sys.exit(main())
