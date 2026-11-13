#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""DEM 재설계 계획서: 원문 둘 → 웹앱 정적 페이지 둘 + docx 빌더용 JSON (+ 원고에 수식이 있으면 수식 캐시).

    python3 scripts/build_dem_redesign_plan.py            # = --check (기본 · 파일을 쓰지 않는다)
    python3 scripts/build_dem_redesign_plan.py --check    # 메모리에서 다시 만들어 커밋된 파일과 바이트 대조
    python3 scripts/build_dem_redesign_plan.py --write    # 생성물을 다시 쓴다 (새 수식이 있으면 pandoc 이 있는 기계에서)
    python3 scripts/build_dem_redesign_plan.py --write-math-cache <원고.md>   # 그 원고 (시험 고정물 등) 의 수식 캐시만 다시 쓴다

계기 (1저자 2026-11-10): "계획 브리핑 이것도 웹앱에서 주간보고 처럼 구리게 말고 좀더 계획서 같은 느낌으로
마감성있게 웹앱에 별도 페이지" · "docx 는 처음 보는 사람 입장에서 써 줘" · "이 형식으로도 잘 받아들여서 이걸
웹앱으로도 만들어주고" · "docx에 MPM에 대한 설명, 지배방정식등을 이런식으로 그림으로도 표현해서 넣어줘 / 한 docx로
이해가 모두 될 수 있게".  사양 = docs/reviews/dem_redesign_direction_20261109/plan_page_brief.md.

무엇을 무엇에서 만드나 (글은 손으로 베끼지 않는다 · 원문 문장을 바꾸지 않는다):

  (a) 계획서       docs/reviews/dem_redesign_direction_20261109/briefing_ko.md
                   → webapp/static/explain/dem_redesign_plan_20261110.html
                   표지 머리 · 배지 · 한 줄로 상자 · 차례 · 로드맵 카드 (단계 0-7) · 갈림 결정표 · 강조 / 경고 /
                   "하지 않는 말" 상자 · 질문 표 · Codex 판정 상자 · 번호 서지
  (b) 처음 보는 분 docs/reviews/dem_redesign_direction_20261109/plan_newcomer_ko.md
                   → webapp/static/explain/dem_redesign_plan_newcomer_20261110.html
                   1저자가 받아들인 docx (같은 폴더 DEM_redesign_plan_for_newcomers_20261110.docx) 의 꼴을 화면으로
                   옮긴 것: 제목 블록 네 줄 · 지위 · 한 줄로 상자 · 번호 절 머리 · 목록 · 머리 행 음영 표
  (c) JSON         같은 원고 → docs/reviews/dem_redesign_direction_20261109/plan_newcomer_docx_model.json
                   docx 빌더 scripts/build_dem_redesign_plan_docx.js 가 읽는다 (열 너비 · 쪽 붙임 표지 · 수식의 OMML ·
                   그림의 경로와 크기 포함)
  (d) 수식 캐시    원고 (b) 에 수식이 있을 때만: 원고 옆 plan_newcomer_ko_math.json (LaTeX → MathML · OMML · 아래 "수식")

지키는 것:

  - 생성물은 바이트 결정적이다 (시각 없음 · LF · UTF-8 · 끝 줄바꿈 하나).
  - 쓰는 문법만 받는다.  낯선 구성은 "파일:줄: 까닭" 을 내고 rc 2 로 멈춘다 (조용히 틀리게 싣지 않는다).
    받는 것: 첫 줄 마커 하나 · "# 제목" 하나 · "**지위**: …" · "**한 줄로**: …" · "## N. 절" 과 "## 참고문헌" ·
    한 줄 문단 · "- " 목록 (0 · 2 칸 들여쓰기) · "1. " 번호 목록 · "| 표 |" · 글 안의 **굵게** · `고정폭` · *기울임*.
    원고 (b) 는 여기에 수식과 그림을 더 받는다 (아래).  원문 (a) 는 받지 않는다 (달러 기호가 있으면 rc 2).
  - 페이지는 한 파일로 닫힌다 (script · link · 외부 URL 없음 · DOI 는 글자로 · 그림은 PNG 를 data URI 로 페이지 안에).
    webapp/app.py 는 봉인이라 라우트를 만들지 않고 정적 폴더에 둔다.  사이드바 링크 = webapp/templates/base.html.
  - (a) 의 계획서 꼴은 원문의 구조에 기대므로, 그 구조 (단계 줄 · 질문 줄 · 갈림 칩 · 배지를 만들 지위 글 · 판정 줄) 가
    없으면 역시 rc 2 로 멈춘다.

수식 · 그림 (원고 (b) 만 · 쓰는 법):

  글 안 수식   $\phi = 1 - \frac{V_s}{A\,h}$          여는 $ 뒤와 닫는 $ 앞에 빈칸 없이 · LaTeX
  줄 수식      $$ 줄 · LaTeX 줄들 · $$ 줄  (또는 한 줄 "$$ … $$")   앞뒤에 빈 줄 · 식 번호는 식 끝에 \tag{1}
  그림         ![그림 1. 캡션](fig1.png)  또는  ![그림 1. 캡션](fig1.png){width=60%}
               앞뒤에 빈 줄 · 캡션은 꼭 (그림 아래 가운데에 실린다 · 캡션 안에 글 안 수식 가능) · PNG 만 · 경로 = 원고 폴더 기준 ·
               폭을 적지 않으면 본문 폭에 맞춘다 · 그림 하나 2 MB 까지 (페이지 안에 통째로 싣는다)

  - 화면 (b) 에는 수식을 MathML 로 싣는다 (바깥 스크립트 없이 브라우저가 그린다).  docx 에는 Word 수식 (OMML) 으로 싣는다.
  - LaTeX → MathML · OMML 변환은 pandoc 이 한다 (--write 때만).  결과는 수식 캐시 (d) 에 적어 커밋한다: --check 와 시험은
    캐시만 읽으므로 pandoc 이 없는 기계에서도 같은 바이트가 나온다.  캐시에 없는 식이 원고에 있으면 --check 는 rc 2 로
    "pandoc 이 있는 기계에서 --write" 를 알린다.  원고에서 뺀 식은 --write 가 캐시에서도 뺀다 (수식이 다 없어지면 파일을 지운다).
  - pandoc 이 내는 것을 그대로 싣되, 수식 아닌 것 (다른 요소 · 주소 · 링크 · 이벤트 속성 · m: 아닌 OMML) 이 섞이면 멈춘다
    (math_entry_problem · 캐시에서 읽은 것도 같은 검사).
  - 표 칸 안의 수식에는 "|" 를 쓸 수 없다 (칸을 가르는 글자다).  머리 줄 (#, ##) 안에는 수식을 쓸 수 없다.

rc: 0 = 같다 (또는 썼다) · 1 = 커밋된 파일과 다르다 (--write 를 돌릴 것) · 2 = 원문을 읽을 수 없다 (받지 않는 구성 ·
캐시에 없는 수식 · 없는 그림 파일).
시험 = webapp/test_dem_redesign_plan_page.py (게이트 scripts/check_all.sh 의 한 단계 · 수식 · 그림 고정물 =
webapp/test_fixtures/dem_redesign_plan/).

"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import os
import posixpath
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

SRC_PLAN = 'docs/reviews/dem_redesign_direction_20261109/briefing_ko.md'
SRC_NEWCOMER = 'docs/reviews/dem_redesign_direction_20261109/plan_newcomer_ko.md'
OUT_PLAN = 'webapp/static/explain/dem_redesign_plan_20261110.html'
OUT_NEWCOMER = 'webapp/static/explain/dem_redesign_plan_newcomer_20261110.html'
OUT_MODEL = 'docs/reviews/dem_redesign_direction_20261109/plan_newcomer_docx_model.json'
DOCX_CANON = 'docs/reviews/dem_redesign_direction_20261109/DEM_redesign_plan_for_newcomers_20261110.docx'
URL_PLAN = '/static/explain/dem_redesign_plan_20261110.html'
URL_NEWCOMER = '/static/explain/dem_redesign_plan_newcomer_20261110.html'
SELF = 'scripts/build_dem_redesign_plan.py'
TEST = 'webapp/test_dem_redesign_plan_page.py'

#: 두 결과물이 같이 쓰는 제목 (사양 · 형식 기준 docx 의 첫 줄).  원문 "# [꼬리표] 부제" 의 부제는 그 아래 줄이 된다.
TITLE = 'DEM 재설계 (수영) 계획서'
#: (b) 제목 블록의 셋째 · 넷째 줄 = 형식 기준 docx 의 글.  원고에 없는 줄이라 상수로 두되, 그 줄을 뒷받침하는 글이
#: 원고에 있을 때만 싣는다 (없으면 rc 2: 낡은 지위를 조용히 싣지 않는다).  (줄에 실을 글, 원고에 있어야 하는 글들)
NEWCOMER_AUDIENCE = ('처음 보는 분을 위한 설명', ('처음 보는 분',))
NEWCOMER_STATUS = (
    ('계획 문서', ('계획 문서입니다',)),
    ('계산 결과는 아직 없음', ('아직 계산 결과는 없습니다',)),
    ('원 메모 = 문서 잔여 종결 가능, 전체 HOLD', ('원 메모', '문서 범위 종결 가능', '전체 HOLD')),
)
# 과거 원고·수식/그림 고정물은 당시 지위를 유지한다. 새 종결 문구가 있는
# 원고는 반드시 새 표지의 근거를 모두 갖춰야 하며 옛 표지로 돌아가지 않는다.
NEWCOMER_STATUS_LEGACY = NEWCOMER_STATUS[:2] + (
    ('외부 검토 = 방향은 맞음, 판정 규칙은 고치는 중', ('방향은 맞다', '판정 규칙 몇 개는 고쳐야 한다')),
)
NEWCOMER_CREATOR = 'DEM 재설계 (수영) 트랙'
#: docx 본문 너비 (A4 · 좌우 여백 1440 DXA) 와 표마다의 열 너비 · "한 쪽에 붙여 두기" 표지 = 형식 기준 docx 그대로.
#: 머리 행의 글로 찾는다.  원고에 새 표가 생기면 여기에 한 줄을 더해야 한다 (없으면 rc 2).
DOCX_TEXT_WIDTH = 9026
NEWCOMER_TABLES = {
    ('방법', '알갱이를 어떻게 보는가', '잘하는 것', '못하는 것'): ((1750, 2250, 2600, 2426), True),
    ('논문', '보여 준 것', '우리 계획에 쓰는 곳'): ((2050, 3850, 3126), False),
    ('단계', '하는 일', '필요한 것'): ((760, 5540, 2726), False),
    ('2D 결과', '뜻', '3D 에서 하는 일'): ((2500, 2600, 3926), True),
    ('용어', '뜻'): ((2100, 6926), True),
    ('#', '서지', '비고'): ((480, 6046, 2500), False),
}
#: (a) 갈림 표의 결과 칩 = 원문 첫 칸 머리의 괄호 글자 → 색 클래스.  모르는 글자는 rc 2.
FORK_CHIPS = {'가': 'k-ga', '나': 'k-na', '마': 'k-ma', '라': 'k-ra', '다': 'k-da'}
#: 인쇄할 때 새 쪽에서 시작하는 절 (큰 절).  (a) = 계획서 꼴의 종류로 (로드맵 · 판정 상자 · 참고문헌) ·
#: (b) = 형식 기준 docx 와 같이 참고문헌만 (절 id).
PLAN_PAGE_BREAK_KINDS = ('roadmap', 'verdict', 'refs')
NEWCOMER_PAGE_BREAKS = ('refs',)


class ParseError(Exception):
    """원문에 받지 않는 구성이 있다.  str() = "파일:줄: 까닭"."""

    def __init__(self, name, line, msg):
        super().__init__('%s:%d: %s' % (name, line, msg))
        self.name, self.line, self.msg = name, line, msg


# ═════════════════════════════ 원문 읽기 ═════════════════════════════
class Para(object):
    __slots__ = ('inl', 'line', 'bold_only')

    def __init__(self, inl, line):
        self.inl, self.line = inl, line
        #: 문단 전체가 굵은 글 하나 = 작은 머리 (예: "**갈림 (결과 전에 정함)**")
        self.bold_only = len(inl) == 1 and inl[0][0] == 'b'


class Item(object):
    __slots__ = ('inl', 'line', 'children')

    def __init__(self, inl, line):
        self.inl, self.line, self.children = inl, line, []


class List(object):
    __slots__ = ('ordered', 'items', 'line')

    def __init__(self, ordered, line):
        self.ordered, self.items, self.line = ordered, [], line


class Table(object):
    __slots__ = ('header', 'rows', 'line', 'row_lines')

    def __init__(self, header, line):
        self.header, self.rows, self.line, self.row_lines = header, [], line, []


class DisplayMath(object):
    """줄 수식 ("$$ … $$").  latex = 원고에 적힌 LaTeX 그대로."""
    __slots__ = ('latex', 'line')

    def __init__(self, latex, line):
        self.latex, self.line = latex, line


class Figure(object):
    """그림 ("![캡션](경로.png)").  path = 원고 폴더 기준 상대 경로 · width_pct = 본문 폭의 몇 % 로 실을지 (없으면 None = 본문 폭)."""
    __slots__ = ('caption', 'path', 'width_pct', 'line')

    def __init__(self, caption, path, width_pct, line):
        self.caption, self.path, self.width_pct, self.line = caption, path, width_pct, line


class Section(object):
    __slots__ = ('num', 'title', 'line', 'blocks', 'sid')

    def __init__(self, num, title, line):
        self.num, self.title, self.line, self.blocks = num, title, line, []
        self.sid = 'refs' if num is None else 's%d' % num

    @property
    def heading(self):
        return self.title if self.num is None else '%d. %s' % (self.num, self.title)


class Doc(object):
    __slots__ = ('name', 'date', 'tag', 'subtitle', 'h1_line', 'status', 'status_line', 'oneline', 'oneline_line',
                 'sections', 'n_lines', 'sha256')


_RE_MARKER = re.compile(r'^<!-- BRIEFING:UPDATED (\d{4}-\d{2}-\d{2}) -->$')
_RE_BULLET = re.compile(r'^( *)- (.*)$')
_RE_ORDERED = re.compile(r'^(\d+)\. (.*)$')
_RE_SEP_CELL = re.compile(r'^:?-{3,}:?$')
_RE_H2 = re.compile(r'^(?:(\d+)\. )?(\S.*)$')
_RE_H1 = re.compile(r'^(?:(\[[^\[\]]+\]) )?(\S.*)$')
_RE_CITE = re.compile(r'\[(\d+)\]')
_RE_FIGURE = re.compile(r'^!\[(.*)\]\(([^()\s]+)\)(?:\{width=(\d{1,3})%\})?$')
_RE_FIG_PATH = re.compile(r'^[A-Za-z0-9_][A-Za-z0-9_./-]*\.png$')
_OPENERS = ' ([{"\'' + chr(0x201C) + chr(0x2018)


def parse_inline(s, name, line, ext=False):
    """글 안의 표지 → 노드 목록.  ('t', 글) · ('b', 노드들) · ('i', 노드들) · ('c', 글) · ('m', LaTeX).

    `σ_y*` 처럼 낱말 뒤에 붙고 빈칸이 따르는 별표는 글자 그대로다.  기울임은 빈칸 · 여는 괄호 · 따옴표 뒤에서만 열리고,
    그 밖의 자리에서 글자에 붙은 별표 (낱말 가운데) 는 받지 않는다.
    ext = 글 안 수식 `$…$` 을 받는다 (LaTeX · 여는 $ 뒤와 닫는 $ 앞에 빈칸 없음 · 닫는 $ 바로 뒤에 숫자 없음 = pandoc 의 규칙).
    그때 달러 기호는 글자로 쓸 수 없다.  수식 안의 역슬래시 · 별표 · 밑줄은 LaTeX 그대로 둔다.
    """
    out, buf, i, n = [], [], 0, len(s)

    def flush():
        if buf:
            out.append(('t', ''.join(buf)))
            del buf[:]

    def bad(msg):
        raise ParseError(name, line, msg)

    while i < n:
        ch = s[i]
        if ext and ch == '$':
            if s.startswith('$$', i):
                bad('글 안의 $$ 는 받지 않는다 (줄 수식은 앞뒤에 빈 줄을 둔 따로 줄에 쓴다)')
            if i + 1 >= n or s[i + 1].isspace():
                bad('수식을 여는 $ 바로 뒤에는 식이 와야 한다 (달러 기호는 글자로 쓸 수 없다)')
            j = i + 1
            while True:
                j = s.find('$', j + 1)
                if j < 0:
                    bad('짝 없는 $ (글 안 수식)')
                if s[j - 1] != '\\':
                    break
            if s[j - 1].isspace() or (j + 1 < n and s[j + 1].isdigit()) or s.startswith('$$', j):
                bad('수식을 닫는 $ 앞에는 빈칸이, 바로 뒤에는 숫자 · $ 가 올 수 없다')
            flush()
            out.append(('m', s[i + 1:j]))
            i = j + 1
            continue
        if ch == '$':
            # ext 가 아닌 원문 (계획서 briefing) 은 수식을 받지 않는다: 달러 기호를 글자로 실으면 "$x$" 가 조용히 글자로 나간다
            bad('달러 기호 ($) 는 받지 않는다 (수식 · 그림은 처음 보는 분용 원고에서만 받는다)')
        if ch == '\\':
            bad('역슬래시는 받지 않는다 (글자 그대로인지 이스케이프인지 갈리는 구성)')
        if ch == '&' and re.match(r'&(?:#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);', s[i:]):
            bad('HTML 문자 참조 (&…;) 는 받지 않는다')
        if ch == '<' and re.match(r'<(?:[A-Za-z/!?])', s[i:]):
            bad('HTML 태그 · 주석은 받지 않는다 (첫 줄 마커 하나만)')
        if ch == '!' and s.startswith('![', i):
            bad('글 안의 그림은 받지 않는다 (그림은 앞뒤에 빈 줄을 둔 따로 줄 "![캡션](경로.png)" 로만)' if ext
                else '그림 (![…](…)) 은 받지 않는다')
        if ch == ']' and s.startswith('](', i):
            bad('링크 ([글](주소)) 는 받지 않는다 (DOI · 경로는 글자로 적는다)')
        if ch == '`':
            j = s.find('`', i + 1)
            if j < 0:
                bad('짝 없는 ` (고정폭)')
            code = s[i + 1:j]
            if not code or code != code.strip():
                bad('빈 고정폭 또는 앞뒤 빈칸이 있는 고정폭')
            flush()
            out.append(('c', code))
            i = j + 1
            continue
        if s.startswith('**', i):
            j = s.find('**', i + 2)
            if j < 0:
                bad('짝 없는 ** (굵게)')
            inner = s[i + 2:j]
            if not inner or inner != inner.strip() or s.startswith('*', j + 2):
                bad('빈 굵은 글 · 앞뒤 빈칸이 있는 굵은 글 · 별표 셋 이상')
            flush()
            out.append(('b', parse_inline(inner, name, line, ext)))
            i = j + 2
            continue
        if ch == '*':
            prev = s[i - 1] if i else ' '
            nxt = s[i + 1] if i + 1 < n else ' '
            if not nxt.isspace() and prev in _OPENERS:
                j = i + 1
                while True:
                    j = s.find('*', j + 1)
                    if j < 0:
                        bad('짝 없는 * (기울임)')
                    if not s[j - 1].isspace() and not s.startswith('**', j) and s[j - 1] != '*':
                        break
                flush()
                out.append(('i', parse_inline(s[i + 1:j], name, line, ext)))
                i = j + 1
                continue
            if not nxt.isspace():
                bad('낱말 가운데의 별표 (*) 는 받지 않는다 (글자 그대로인지 기울임인지 갈리는 구성)')
        buf.append(ch)
        i += 1
    flush()
    return out


def plain(nodes):
    """노드 목록 → 표지를 뺀 글 (수식은 LaTeX 글 그대로)."""
    return ''.join(v if k in ('t', 'c', 'm') else plain(v) for k, v in nodes)


def _cells(ln, name, no):
    if not ln.endswith('|') or len(ln) < 2:
        raise ParseError(name, no, '표 줄은 | 로 시작하고 | 로 끝나야 한다')
    if ln.count('`') % 2:
        raise ParseError(name, no, '표 줄에 짝 없는 `')
    return [c.strip() for c in ln[1:-1].split('|')]


def parse(text, name, extended=False):
    """원문 → Doc.  받지 않는 구성은 ParseError (줄 번호).

    extended = 수식 · 그림을 받는다 (처음 보는 분용 원고):
      글 안 수식  `$…$`
      줄 수식     "$$" 줄 · LaTeX 줄 (하나 이상 · 빈 줄 없이) · "$$" 줄,  또는 한 줄 "$$ … $$"
      그림        "![캡션](경로.png)" 한 줄 (캡션은 꼭 · 뒤에 "{width=NN%}" 를 붙일 수 있다 · 경로 = 원고 폴더 기준 · PNG 만)
    줄 수식 · 그림은 앞뒤에 빈 줄을 둔 따로 블록이고 절 (##) 안에서만 받는다.  머리 줄 안의 수식 · "|" 가 든 표 칸의 수식은 받지 않는다.
    extended 가 아니면 (계획서 briefing) 달러 기호 자체를 받지 않는다.
    """
    def pin(s2, no2):
        return parse_inline(s2, name, no2, extended)

    if text.startswith(chr(0xFEFF)):
        raise ParseError(name, 1, 'BOM 은 받지 않는다')
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    for k, ln in enumerate(lines, 1):
        if '\r' in ln:
            raise ParseError(name, k, 'CR 줄바꿈은 받지 않는다 (LF 만)')
        if '\t' in ln:
            raise ParseError(name, k, '탭 문자는 받지 않는다')
    m = _RE_MARKER.match(lines[0]) if lines else None
    if not m:
        raise ParseError(name, 1, '첫 줄은 마커 <!-- BRIEFING:UPDATED YYYY-MM-DD --> 여야 한다')
    doc = Doc()
    doc.name, doc.date, doc.n_lines = name, m.group(1), len(lines)
    doc.sha256 = hashlib.sha256(text.encode('utf-8')).hexdigest()
    doc.tag = doc.subtitle = doc.status = doc.oneline = None
    doc.h1_line = doc.status_line = doc.oneline_line = 0
    doc.sections = []
    cur, next_num = None, 1
    i, n = 1, len(lines)

    def need_blank_after(j):
        if j < n and lines[j] != '':
            raise ParseError(name, j + 1, '블록 뒤에는 빈 줄이 있어야 한다 (여러 줄 문단 · 붙여 쓴 블록은 받지 않는다)')

    def add(block):
        if cur is None:
            raise ParseError(name, block.line, '첫 절 (##) 앞에는 제목 · "**지위**:" · "**한 줄로**:" 만 올 수 있다')
        cur.blocks.append(block)

    while i < n:
        ln, no = lines[i], i + 1
        if ln == '':
            i += 1
            continue
        if ln != ln.rstrip() or not ln.strip():
            raise ParseError(name, no, '줄 끝 빈칸 · 빈칸뿐인 줄은 받지 않는다')
        if ln.startswith('#'):
            mh = re.match(r'^(#{1,6}) (\S.*)$', ln)
            if not mh:
                raise ParseError(name, no, '머리 줄 꼴이 아니다 ("# 제목" · "## N. 절")')
            level, rest = len(mh.group(1)), mh.group(2)
            if any(k != 't' for k, _v in pin(rest, no)):
                raise ParseError(name, no, '머리 줄 안의 표지 (굵게 · 고정폭 · 기울임 · 수식) 는 받지 않는다')
            if level == 1:
                if doc.subtitle is not None or doc.sections or doc.status is not None:
                    raise ParseError(name, no, '제목 (#) 은 맨 위에 하나만 올 수 있다')
                m1 = _RE_H1.match(rest)
                doc.tag, doc.subtitle, doc.h1_line = m1.group(1), m1.group(2), no
            elif level == 2:
                if doc.subtitle is None or doc.status is None or doc.oneline is None:
                    raise ParseError(name, no, '첫 절 앞에 제목 (#) · "**지위**:" · "**한 줄로**:" 가 차례로 있어야 한다')
                m2 = _RE_H2.match(rest)
                num = int(m2.group(1)) if m2.group(1) else None
                if num is None:
                    if m2.group(2) != '참고문헌':
                        raise ParseError(name, no, '번호 없는 절은 "참고문헌" 만 받는다')
                    if any(s.num is None for s in doc.sections):
                        raise ParseError(name, no, '"참고문헌" 절이 둘이다')
                else:
                    if num != next_num:
                        raise ParseError(name, no, '절 번호가 차례가 아니다 (기대 %d · 지금 %d)' % (next_num, num))
                    next_num += 1
                cur = Section(num, m2.group(2), no)
                doc.sections.append(cur)
            else:
                raise ParseError(name, no, '### 이하의 머리는 받지 않는다')
            need_blank_after(i + 1)
            i += 1
            continue
        if ln.startswith('|'):
            header = _cells(ln, name, no)
            if i + 1 >= n or not lines[i + 1].startswith('|'):
                raise ParseError(name, no + 1 if i + 1 < n else no, '표 머리 줄 다음에 구분 줄 (|---|---|) 이 없다')
            sep = _cells(lines[i + 1], name, no + 1)
            if len(sep) != len(header) or not all(_RE_SEP_CELL.match(c) for c in sep):
                raise ParseError(name, no + 1, '표 머리 줄 다음은 칸 수가 같은 구분 줄 (|---|---|) 이어야 한다')
            tb = Table([pin(c, no) for c in header], no)
            j = i + 2
            while j < n and lines[j].startswith('|'):
                row = _cells(lines[j], name, j + 1)
                if len(row) != len(header):
                    raise ParseError(name, j + 1, '표 줄의 칸 수 (%d) 가 머리 줄 (%d) 과 다르다' % (len(row), len(header)))
                tb.rows.append([pin(c, j + 1) for c in row])
                tb.row_lines.append(j + 1)
                j += 1
            if not tb.rows:
                raise ParseError(name, no, '줄이 없는 표')
            need_blank_after(j)
            add(tb)
            i = j
            continue
        mb, mo = _RE_BULLET.match(ln), _RE_ORDERED.match(ln)
        if mb or mo:
            lst = List(bool(mo), no)
            j = i
            while j < n and lines[j] != '':
                lj, nj = lines[j], j + 1
                if lj != lj.rstrip():
                    raise ParseError(name, nj, '줄 끝 빈칸은 받지 않는다')
                if lst.ordered:
                    mj = _RE_ORDERED.match(lj)
                    if not mj:
                        raise ParseError(name, nj, '번호 목록 안에는 "N. " 줄만 올 수 있다 (딸린 목록 · 이어 쓴 줄은 받지 않는다)')
                    if int(mj.group(1)) != len(lst.items) + 1:
                        raise ParseError(name, nj, '번호 목록의 번호가 차례가 아니다 (기대 %d)' % (len(lst.items) + 1))
                    lst.items.append(Item(pin(mj.group(2), nj), nj))
                else:
                    mj = _RE_BULLET.match(lj)
                    if not mj:
                        raise ParseError(name, nj, '목록 안에는 "- " 줄만 올 수 있다 (이어 쓴 줄은 받지 않는다)')
                    ind = len(mj.group(1))
                    if not mj.group(2).strip():
                        raise ParseError(name, nj, '빈 목록 줄')
                    if ind == 0:
                        lst.items.append(Item(pin(mj.group(2), nj), nj))
                    elif ind == 2 and lst.items:
                        lst.items[-1].children.append(Item(pin(mj.group(2), nj), nj))
                    else:
                        raise ParseError(name, nj, '목록 들여쓰기는 0 칸 · 2 칸 (한 단 아래) 만 받는다')
                j += 1
            add(lst)
            i = j
            continue
        if ln[0] == ' ':
            raise ParseError(name, no, '들여쓴 줄은 목록 ("  - ") 일 때만 받는다')
        if extended and ln.startswith('$$'):
            if ln == '$$':
                j = i + 1
                while j < n and lines[j] != '$$':
                    if not lines[j].strip():
                        raise ParseError(name, j + 1, '줄 수식 안에는 빈 줄을 둘 수 없다 (닫는 $$ 가 없다)')
                    j += 1
                if j >= n:
                    raise ParseError(name, no, '줄 수식을 닫는 $$ 줄이 없다')
                latex, end = '\n'.join(lines[i + 1:j]), j + 1
            else:
                if not ln.endswith('$$') or len(ln) < 5:
                    raise ParseError(name, no, '한 줄 수식은 "$$ … $$" 꼴이어야 한다 (여러 줄이면 $$ 를 따로 줄에)')
                latex, end = ln[2:-2].strip(), i + 1
            if not latex.strip() or '$$' in latex:
                raise ParseError(name, no, '빈 줄 수식 · 수식 안의 $$ 는 받지 않는다')
            need_blank_after(end)
            add(DisplayMath(latex, no))
            i = end
            continue
        if extended and ln.startswith('!['):
            mf = _RE_FIGURE.match(ln)
            if not mf:
                raise ParseError(name, no, '그림 줄은 "![캡션](경로.png)" 또는 "![캡션](경로.png){width=NN%}" 꼴이어야 한다')
            path, pct = mf.group(2), (int(mf.group(3)) if mf.group(3) else None)
            if not _RE_FIG_PATH.match(path) or '..' in path.split('/') or '//' in path:
                raise ParseError(name, no, '그림 경로는 원고 폴더 기준 상대 경로의 PNG 여야 한다 (영문 · 숫자 · _ - . / 만 · ".." 없이)')
            if pct is not None and not 10 <= pct <= 100:
                raise ParseError(name, no, '그림 폭은 본문 폭의 10–100 % 로 적는다')
            if not mf.group(1).strip():
                raise ParseError(name, no, '그림에는 캡션이 있어야 한다 ("![캡션](경로.png)" · 캡션은 그림 아래에 실린다)')
            need_blank_after(i + 1)
            add(Figure(pin(mf.group(1), no), path, pct, no))
            i += 1
            continue
        if ln.startswith('>'):
            raise ParseError(name, no, '인용 블록 (>) 은 받지 않는다')
        if ln.startswith('```') or ln.startswith('~~~'):
            raise ParseError(name, no, '코드 울타리는 받지 않는다')
        if ln.startswith('<'):
            raise ParseError(name, no, 'HTML 태그 · 주석은 받지 않는다 (첫 줄 마커 하나만)')
        if re.match(r'^(?:[-*_] ?){3,}$', ln) or re.match(r'^[*+] ', ln) or re.match(r'^\d+\) ', ln):
            raise ParseError(name, no, '가로줄 · "* " "+ " "1) " 목록은 받지 않는다 ("- " · "1. " 만)')
        inl = pin(ln, no)
        need_blank_after(i + 1)
        i += 1
        if cur is None:
            if doc.subtitle is None:
                raise ParseError(name, no, '마커 다음에는 제목 (# …) 이 와야 한다')
            ml = re.match(r'^\*\*(.+?)\*\*: \S', ln)
            label = ml.group(1) if ml else None
            if label == '지위' and doc.status is None and doc.oneline is None:
                doc.status, doc.status_line = inl, no
            elif label == '한 줄로' and doc.status is not None and doc.oneline is None:
                doc.oneline, doc.oneline_line = inl, no
            else:
                raise ParseError(name, no, '첫 절 앞에는 "**지위**: …" 다음 "**한 줄로**: …" 문단만 올 수 있다')
            continue
        add(Para(inl, no))
    if doc.subtitle is None:
        raise ParseError(name, min(2, max(1, n)), '제목 (# …) 이 없다')
    if doc.status is None or doc.oneline is None:
        raise ParseError(name, max(1, n), '"**지위**:" · "**한 줄로**:" 문단이 없다')
    if not doc.sections:
        raise ParseError(name, max(1, n), '절 (## …) 이 하나도 없다')
    for s in doc.sections:
        if not s.blocks:
            raise ParseError(name, s.line, '빈 절')
    return doc


# ═════════════════════════════ 수식 (pandoc · 캐시) · 그림 ═════════════════════════════
MATH_SCHEMA = 'dem_redesign_plan_math/1'
#: 그림 하나의 상한.  그림은 data URI 로 페이지 한 파일 안에 싣는다 → 너무 크면 조용히 싣지 않고 멈춘다.
FIG_MAX_BYTES = 2 * 1024 * 1024
#: 그림 하나의 키 상한 (px · 96 dpi).  docx 본문의 키 (A4 · 위 1440 · 아래 1300 DXA = 940 px) 에서 캡션 자리를 뺀 값.
FIG_MAX_HEIGHT_PX = 860
_PNG_MAGIC = b'\x89PNG\r\n\x1a\n'
_RE_TAG = re.compile(r'\\tag\{([^{}]*)\}')
_RE_MATHML = re.compile(r'<math\b[^>]*>.*?</math>', re.S)
_RE_OMML = re.compile(r'<m:oMathPara>.*?</m:oMathPara>|<m:oMath>.*?</m:oMath>', re.S)
_RE_OMML_DPR = re.compile(r'(<m:endChr m:val="[^"]*" />)(<m:sepChr m:val="[^"]*" />)')
_RE_OMML_NOR = re.compile(r'(<m:nor />)<m:sty m:val="[^"]*" />')
_RE_OMML_MCPR = re.compile(r'(<m:mcJc m:val="[^"]*" />)(<m:count m:val="[^"]*" />)')


def _omml_fix(omml):
    """pandoc (3.1.3 에서 확인) 이 내는 OMML 의 스키마 어긋남 셋을 바로잡는다 (뜻은 그대로 · Word 스키마 검사 통과용):
    괄호 속성의 순서 (m:sepChr 는 m:endChr 앞) · 보통 글 런 (m:nor) 에 겹쳐 붙은 글자 꼴 (m:sty) ·
    행렬 열 속성의 순서 (m:count 는 m:mcJc 앞)."""
    return _RE_OMML_MCPR.sub(r'\2\1', _RE_OMML_NOR.sub(r'\1', _RE_OMML_DPR.sub(r'\2\1', omml)))



_RE_TAGS = re.compile(r'<[^>]*>')
_RE_MATHML_TAG = re.compile(r'<(?!/?(?:math|semantics|annotation|m[a-z]+)[\s/>])')
_RE_OMML_TAG = re.compile(r'<(?!/?m:[A-Za-z]+[\s/>])')
_RE_OMML_ATTR = re.compile(r'\s(?!m:|xml:space=)[A-Za-z_:][\w:.-]*=')


def math_entry_problem(e):
    """수식 변환 하나 (캐시 항목) 가 받을 수 있는 꼴인지 본다.  문제가 있으면 그 까닭 (글), 없으면 None.

    페이지는 MathML 을, docx 는 OMML 을 바이트 그대로 싣는다 → 수식 아닌 것 (다른 요소 · 주소 · 링크 · 이벤트 속성 ·
    다른 네임스페이스) 이 섞여 들지 못하게 여기서 막는다 (pandoc 이 낸 것도 · 캐시 파일에서 읽은 것도 같은 검사)."""
    if not isinstance(e, dict) or not isinstance(e.get('latex'), str) or not isinstance(e.get('display'), bool) \
            or not isinstance(e.get('mathml'), str) or not isinstance(e.get('omml'), str):
        return '항목은 latex (글) · display (참 / 거짓) · mathml (글) · omml (글) 을 실어야 한다'
    mathml, omml = e['mathml'], e['omml']
    head = '<math display="%s">' % ('block' if e['display'] else 'inline')
    if not mathml.startswith(head) or not mathml.endswith('</math>') or mathml.count('<math') != 1:
        return 'MathML 은 %s 로 시작하는 <math> 하나여야 한다' % head
    tags = ''.join(_RE_TAGS.findall(mathml)).lower()
    if _RE_MATHML_TAG.search(mathml) or 'http' in mathml.lower() or 'href' in tags or 'src=' in tags or re.search(r'\son[a-z]+\s*=', tags):
        return 'MathML 에 받지 않는 것 (수식 아닌 요소 · 주소 · 링크 · 이벤트 속성) 이 있다'
    wrap = 'm:oMathPara' if e['display'] else 'm:oMath'
    if not omml.startswith('<%s>' % wrap) or not omml.endswith('</%s>' % wrap) or omml.count('<m:oMath>') != 1:
        return 'OMML 은 <%s> 하나여야 한다' % wrap
    if _RE_OMML_TAG.search(omml) or _RE_OMML_ATTR.search(''.join(_RE_TAGS.findall(omml))) or 'xmlns' in omml:
        return 'OMML 에 받지 않는 것 (m: 아닌 요소 · 속성 · xmlns) 이 있다'
    return None


def math_cache_rel(src_rel):
    """원고 경로 → 그 원고의 수식 변환 캐시 경로 (같은 폴더의 "<원고 이름>_math.json")."""
    return src_rel[:-3] + '_math.json'


def collect_math(doc):
    """원고의 수식을 처음 나온 순서대로 [(줄 수식인가, LaTeX, 줄 번호)] (같은 식은 한 번)."""
    seen, out = set(), []

    def put(display, latex, no):
        if (display, latex) not in seen:
            seen.add((display, latex))
            out.append((display, latex, no))

    def walk(nodes, no):
        for k, v in nodes:
            if k == 'm':
                put(False, v, no)
            elif k in ('b', 'i'):
                walk(v, no)
    walk(doc.status, doc.status_line)
    walk(doc.oneline, doc.oneline_line)
    for s in doc.sections:
        for b in s.blocks:
            if isinstance(b, Para):
                walk(b.inl, b.line)
            elif isinstance(b, List):
                for it in b.items:
                    walk(it.inl, it.line)
                    for ch in it.children:
                        walk(ch.inl, ch.line)
            elif isinstance(b, Table):
                for c in b.header:
                    walk(c, b.line)
                for row, no in zip(b.rows, b.row_lines):
                    for c in row:
                        walk(c, no)
            elif isinstance(b, DisplayMath):
                put(True, b.latex, b.line)
            else:
                walk(b.caption, b.line)
    return out


def pandoc_version():
    """설치된 pandoc 의 판 ("3.1.3").  없으면 None."""
    try:
        pr = subprocess.run(['pandoc', '--version'], capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.match(r'pandoc(?:\.exe)? (\S+)', pr.stdout.decode('utf-8', 'replace'))
    return m.group(1) if m and pr.returncode == 0 else None


def _tex_for_pandoc(display, latex):
    """pandoc 의 TeX 읽개는 \\tag 를 모른다 → 줄 수식의 식 번호는 식 끝의 글자 "(n)" 으로 바꿔 넘긴다
    (DEM 지배방정식 보고서 docs/data/dem_governing_equations_report_20261011/build.sh 와 같은 규칙)."""
    return _RE_TAG.sub(lambda m: '\\qquad\\text{(%s)}' % m.group(1), latex) if display else latex


def _pandoc_run(md, to, extra):
    pr = subprocess.run(['pandoc', '-f', 'markdown', '-t', to, '--fail-if-warnings', '--wrap=none'] + extra,
                        input=md.encode('utf-8'), capture_output=True, timeout=600)
    err = pr.stderr.decode('utf-8', 'replace').strip()
    return pr.returncode, pr.stdout.decode('utf-8', 'replace'), (err.split('\n')[0] if err else '')


def _pandoc_pair(items):
    """수식 목록을 pandoc 으로 한꺼번에 바꾼다 → ([MathML …], [OMML …]) 또는 (None, 까닭)."""
    md = '\n\n'.join(('$$\n%s\n$$' % _tex_for_pandoc(True, t)) if d else ('$%s$' % t) for d, t, _no in items) + '\n'
    rc, out, err = _pandoc_run(md, 'html', ['--mathml'])
    if rc != 0:
        return None, err or 'pandoc rc %d' % rc
    maths = _RE_MATHML.findall(out)
    tmp = tempfile.mkdtemp(prefix='dem_plan_math_')
    try:
        path = os.path.join(tmp, 'eq.docx')
        rc, _out, err = _pandoc_run(md, 'docx', ['-o', path])
        if rc != 0:
            return None, err or 'pandoc rc %d' % rc
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/document.xml').decode('utf-8')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ommls = _RE_OMML.findall(xml)
    if len(maths) != len(items) or len(ommls) != len(items):
        return None, 'pandoc 이 낸 수식 수가 다르다 (MathML %d · OMML %d · 기대 %d)' % (len(maths), len(ommls), len(items))
    return maths, ommls


def pandoc_convert(items, name):
    """[(줄 수식인가, LaTeX, 줄)] → 캐시 항목들 (LaTeX → 화면용 MathML · Word 용 OMML).  못 바꾸는 식은 그 줄을 짚어 멈춘다."""
    ver = pandoc_version()
    if ver is None:
        raise ParseError(name, items[0][2], '수식을 바꿀 pandoc 을 찾을 수 없다 (pandoc 이 있는 기계에서 --write 를 돌릴 것)')
    maths, ommls = _pandoc_pair(items)
    if maths is None:
        why_all = ommls
        for it in items:        # 어느 식인지 짚는다
            one, why = _pandoc_pair([it])
            if one is None:
                raise ParseError(name, it[2], 'pandoc 이 이 수식을 읽지 못했다: %s' % why)
        raise ParseError(name, items[0][2], 'pandoc 수식 변환 실패: %s' % why_all)
    out = []
    for (d, t, no), mathml, omml in zip(items, maths, ommls):
        entry = {'latex': t, 'display': d, 'mathml': mathml.replace(' xmlns="http://www.w3.org/1998/Math/MathML"', ''),
                 'omml': _omml_fix(omml), 'pandoc': ver}
        why = math_entry_problem(entry)
        if why:
            raise ParseError(name, no, 'pandoc 이 낸 이 수식의 변환을 실을 수 없다: %s' % why)
        out.append(entry)
    return out


class MathStore(object):
    """수식 변환 (LaTeX → 화면용 MathML · Word 용 OMML) 저장소.

    변환은 pandoc 이 하고, 결과는 원고 옆 캐시 파일에 커밋해 둔다.  --check 와 시험은 캐시만 읽는다 (pandoc 이 없거나 판이
    달라도 생성물이 같은 바이트).  캐시에 없는 식은 --write 가 pandoc 으로 바꿔 캐시에 더하고, 안 쓰는 식은 캐시에서 뺀다."""

    def __init__(self, entries=()):
        self._by_key = dict(((bool(e['display']), e['latex']), e) for e in entries)
        self.used = []

    @classmethod
    def load(cls, data, cache_rel):
        """캐시 파일의 바이트 (없으면 None) → 저장소.  꼴이 다르면 ParseError (줄 1)."""
        if data is None:
            return cls()
        try:
            obj = json.loads(data.decode('utf-8'))
            entries = obj['entries']
            why = None if obj.get('schema') == MATH_SCHEMA and isinstance(entries, list) else 'schema 가 %s 가 아니거나 entries 가 목록이 아니다' % MATH_SCHEMA
        except (ValueError, KeyError, TypeError, AttributeError):
            why, entries = 'JSON 이 아니거나 schema · entries 가 없다', ()
        if why is None:
            for k, e in enumerate(entries):
                bad = math_entry_problem(e)
                if bad:
                    why = '항목 %d: %s' % (k + 1, bad)
                    break
        if why:
            raise ParseError(cache_rel, 1, '수식 캐시의 꼴이 다르다: %s' % why)
        return cls(entries)


    def ensure(self, items, name, cache_rel, convert=None):
        """원고의 수식이 모두 저장소에 있게 한다.  없는 식은 convert 로 바꾸고, convert 가 없으면 그 줄을 짚어 멈춘다."""
        miss = [it for it in items if (it[0], it[1]) not in self._by_key]
        if miss and convert is None:
            raise ParseError(name, miss[0][2], '이 수식의 변환이 캐시 %s 에 없다: pandoc 이 있는 기계에서 python3 %s --write' % (cache_rel, SELF))
        if miss:
            for it, e in zip(miss, convert(miss, name)):
                self._by_key[(it[0], it[1])] = e
        self.used = [self._by_key[(d, t)] for d, t, _no in items]

    def get(self, display, latex):
        return self._by_key[(display, latex)]

    def dumps(self):
        return json.dumps({
            'schema': MATH_SCHEMA,
            'note': '생성물: 손으로 고치지 않는다.  %s --write 가 원고의 수식을 pandoc 으로 바꿔 적는다 (LaTeX → MathML · OMML).' % SELF,
            'entries': [dict((k, e[k]) for k in ('latex', 'display', 'mathml', 'omml', 'pandoc') if k in e) for e in self.used],
        }, ensure_ascii=False, indent=1) + '\n'


def load_figure(root, doc_name, fig):
    """그림 파일을 읽는다 → {rel (리포 상대 경로) · data · px (가로, 세로) · sha256}.  없거나 PNG 가 아니면 그 줄을 짚어 멈춘다."""
    rel = posixpath.normpath(posixpath.join(posixpath.dirname(doc_name), fig.path))
    try:
        with open(os.path.join(root, *rel.split('/')), 'rb') as f:
            data = f.read()
    except OSError:
        raise ParseError(doc_name, fig.line, '그림 파일이 없다: %s' % rel)
    if len(data) > FIG_MAX_BYTES:
        raise ParseError(doc_name, fig.line, '그림이 너무 크다 (%d B · 상한 %d B): 페이지 한 파일 안에 싣는다 → 줄여서 넣을 것'
                         % (len(data), FIG_MAX_BYTES))
    if len(data) < 33 or data[:8] != _PNG_MAGIC or data[12:16] != b'IHDR':
        raise ParseError(doc_name, fig.line, 'PNG 파일이 아니다: %s' % rel)
    w, h = struct.unpack('>II', data[16:24])
    if not (0 < w <= 20000 and 0 < h <= 20000):
        raise ParseError(doc_name, fig.line, 'PNG 의 크기 (%d x %d) 를 받을 수 없다' % (w, h))
    return {'rel': rel, 'data': data, 'px': (w, h), 'sha256': hashlib.sha256(data).hexdigest()}


def figure_display(px, width_pct):
    """그림을 싣는 크기 → (가로 px, 세로 px, 본문 폭의 몇 %).  px 는 96 dpi 기준 (docx 본문 폭 = DOCX_TEXT_WIDTH / 15 = 601 px).

    폭 지정 ("{width=NN%}") 이 없으면 본문 폭에 맞춘다 (100 %).  그렇게 놓았을 때 키가 한 쪽에 들어가지 않으면 (FIG_MAX_HEIGHT_PX)
    키를 그 값으로 줄이고 폭을 따라 줄인다 (그때 % 는 줄어든 값)."""
    full = DOCX_TEXT_WIDTH // 15
    pct = float(width_pct or 100)
    w = max(1, int(round(full * pct / 100.0)))
    h = max(1, int(round(w * px[1] / float(px[0]))))
    if h > FIG_MAX_HEIGHT_PX:
        h = FIG_MAX_HEIGHT_PX
        w = max(1, int(round(h * px[0] / float(px[1]))))
        pct = 100.0 * w / full
    return w, h, pct


# ═════════════════════════════ HTML 조각 ═════════════════════════════
def esc(s):
    return html.escape(s, quote=True)


class Ctx(object):
    """렌더 맥락: 원문 이름 (오류 글) · 링크로 바꿀 인용 번호 · 페이지 종류 · 수식 저장소 · 그림 읽개 (Figure → load_figure 의 값)."""

    def __init__(self, name, cites, kind, math=None, figure=None):
        self.name, self.cites, self.kind, self.math, self.figure = name, cites, kind, math, figure


def _text(s, ctx):
    """글 → HTML.  [n] 이 참고문헌에 있는 번호면 그 자리 (#ref-n) 로 가는 링크."""
    out, pos = [], 0
    for m in _RE_CITE.finditer(s):
        if int(m.group(1)) not in ctx.cites:
            continue
        out.append(esc(s[pos:m.start()]))
        out.append('<a class="cite" href="#ref-%s">[%s]</a>' % (m.group(1), m.group(1)))
        pos = m.end()
    out.append(esc(s[pos:]))
    return ''.join(out)


def _code(v):
    """고정폭.  짧은 ID (DRD-01 · SELF-160) 는 줄 끝에서 갈리지 않게 두고, 경로 ("/" 가 있는 것) 만 어디서든 줄을 바꾼다."""
    return '<code%s>%s</code>' % (' class="path"' if '/' in v else '', esc(v))


def inline(nodes, ctx):
    out = []
    for k, v in nodes:
        if k == 't':
            out.append(_text(v, ctx))
        elif k == 'c':
            out.append(_code(v))
        elif k == 'm':
            out.append(ctx.math.get(False, v)['mathml'])
        elif k == 'b':
            out.append('<strong>%s</strong>' % inline(v, ctx))
        else:
            out.append('<em>%s</em>' % inline(v, ctx))
    return ''.join(out)


def split_nodes(nodes, sep):
    """맨 바깥 글 노드에서 sep 이 처음 나오는 자리로 둘로 가른다.  없으면 None."""
    for idx, (k, v) in enumerate(nodes):
        if k == 't' and sep in v:
            a, b = v.split(sep, 1)
            left = nodes[:idx] + ([('t', a)] if a else [])
            right = ([('t', b)] if b else []) + nodes[idx + 1:]
            return left, right
    return None


def sentences(nodes):
    """노드 목록을 문장 (빈칸 둘로 가른 것) 마다의 노드 목록으로."""
    out, cur = [], []
    for k, v in nodes:
        if k != 't':
            cur.append((k, v))
            continue
        parts = v.split('  ')
        for pi, part in enumerate(parts):
            if pi:
                out.append(cur)
                cur = []
            if part:
                cur.append(('t', part))
    out.append(cur)
    return [s for s in out if s]


def r_list(lst, ctx):
    tag = 'ol' if lst.ordered else 'ul'
    out = ['<%s>' % tag]
    for it in lst.items:
        if it.children:
            out.append('<li>%s' % inline(it.inl, ctx))
            out.append('<ul>')
            out.extend('<li>%s</li>' % inline(ch.inl, ctx) for ch in it.children)
            out.append('</ul>')
            out.append('</li>')
        else:
            out.append('<li>%s</li>' % inline(it.inl, ctx))
    out.append('</%s>' % tag)
    return '\n'.join(out)


def r_table(tb, ctx, cls='', widths=None, row_ids=None, labels=False):
    """표 → 가로 스크롤 상자 안의 <table>.  labels = 칸마다 머리 글을 data-k 로 (폰 폭에서 줄을 쌓을 때 쓰는 이름표)."""
    ncol = len(tb.header)
    classes = ' '.join(x for x in (cls, 'c%d' % ncol) if x)
    out = ['<div class="wrap">', '<table class="%s">' % classes]
    if widths:
        total = float(sum(widths))
        out.append('<colgroup>%s</colgroup>' % ''.join('<col style="width:%.2f%%">' % (100.0 * w / total) for w in widths))
    out.append('<thead><tr>%s</tr></thead>' % ''.join('<th scope="col">%s</th>' % inline(c, ctx) for c in tb.header))
    out.append('<tbody>')
    heads = [plain(c) for c in tb.header]
    for ri, row in enumerate(tb.rows):
        tds = []
        for ci, c in enumerate(row):
            attrs = ' data-k="%s"' % esc(heads[ci]) if labels and ci else ''
            tds.append('<td%s>%s</td>' % (attrs, inline(c, ctx)))
        out.append('<tr%s>%s</tr>' % (' id="%s"' % row_ids[ri] if row_ids else '', ''.join(tds)))
    out.append('</tbody>')
    out.append('</table>')
    out.append('</div>')
    return '\n'.join(out)


def r_block(b, ctx):
    if isinstance(b, Para):
        if b.bold_only:
            if ctx.kind == 'plan':
                return '<h3 class="sub">%s</h3>' % inline(b.inl[0][1], ctx)
            return '<p class="leadin"><strong>%s</strong></p>' % inline(b.inl[0][1], ctx)
        return '<p>%s</p>' % inline(b.inl, ctx)
    if isinstance(b, List):
        return r_list(b, ctx)
    if isinstance(b, DisplayMath):
        return '<div class="eq">%s</div>' % ctx.math.get(True, b.latex)['mathml']
    if isinstance(b, Figure):
        return r_figure(b, ctx)
    return r_table(b, ctx)


def r_figure(fig, ctx):
    """그림 → <figure> (PNG 를 data URI 로 페이지 안에 싣는다 · 캡션은 그림 아래 가운데)."""
    f = ctx.figure(fig)
    pct = ('%.1f' % figure_display(f['px'], fig.width_pct)[2]).rstrip('0').rstrip('.')
    return '\n'.join([
        '<figure class="fig">',
        '<img src="data:image/png;base64,%s" alt="%s" width="%d" height="%d" style="width:%s%%">' % (
            base64.b64encode(f['data']).decode('ascii'), esc(plain(fig.caption)), f['px'][0], f['px'][1], pct),
        '<figcaption>%s</figcaption>' % inline(fig.caption, ctx),
        '</figure>'])


def r_blocks(blocks, ctx):
    return '\n'.join(r_block(b, ctx) for b in blocks)


def _ref_numbers(doc):
    """참고문헌 절의 표 첫 칸 번호들 (1 … n 차례여야 한다)."""
    sec = next((s for s in doc.sections if s.num is None), None)
    if sec is None:
        return sec, None, []
    tb = next((b for b in sec.blocks if isinstance(b, Table)), None)
    if tb is None:
        raise ParseError(doc.name, sec.line, '"참고문헌" 절에 표가 없다')
    nums = []
    for row, no in zip(tb.rows, tb.row_lines):
        cell = plain(row[0])
        if cell != str(len(nums) + 1):
            raise ParseError(doc.name, no, '참고문헌 표의 첫 칸은 1 부터 차례인 번호여야 한다 (기대 %d · 지금 "%s")' % (len(nums) + 1, cell))
        nums.append(len(nums) + 1)
    return sec, tb, nums


def _check_cites(doc, cites):
    """글 안의 [n] 이 참고문헌에 없는 번호면 멈춘다 (숫자뿐인 대괄호 = 인용 번호로 읽는다)."""
    def walk(nodes, no):
        for k, v in nodes:
            if k == 't':
                for m in _RE_CITE.finditer(v):
                    if int(m.group(1)) not in cites:
                        raise ParseError(doc.name, no, '인용 번호 [%s] 가 참고문헌 표에 없다' % m.group(1))
            elif k in ('b', 'i'):
                walk(v, no)
    walk(doc.status, doc.status_line)
    walk(doc.oneline, doc.oneline_line)
    for s in doc.sections:
        for b in s.blocks:
            if isinstance(b, Para):
                walk(b.inl, b.line)
            elif isinstance(b, List):
                for it in b.items:
                    walk(it.inl, it.line)
                    for ch in it.children:
                        walk(ch.inl, ch.line)
            elif isinstance(b, Table):
                for c in b.header:
                    walk(c, b.line)
                for row, no in zip(b.rows, b.row_lines):
                    for c in row:
                        walk(c, no)
            elif isinstance(b, Figure):
                walk(b.caption, b.line)


# ═════════════════════════════ 색 · CSS ═════════════════════════════
#: 색 계열 = 형식 기준 docx 의 음영 (글자 1F2933 · 제목 1F4E79 · 흐린 글 5B6770 · 머리 행 E6EDF3 · 상자 EAF2FA · 테두리 B8C4CE).
_LIGHT = (('--bg', '#eef2f6'), ('--paper', '#ffffff'), ('--ink', '#1f2933'), ('--mut', '#5b6770'), ('--acc', '#1f4e79'),
          ('--line', '#b8c4ce'), ('--hair', '#dce3ea'), ('--th', '#e6edf3'), ('--box', '#eaf2fa'), ('--code', '#eef2f6'),
          ('--ok', '#2a6a3a'), ('--ok-bg', '#e5f3e8'), ('--warn', '#85570a'), ('--warn-bg', '#fff5dc'), ('--warn-line', '#d6a548'),
          ('--bad', '#a1342b'), ('--bad-bg', '#fcefed'), ('--bad-line', '#dba29a'))
_DARK = (('--bg', '#11161b'), ('--paper', '#1a2028'), ('--ink', '#e4e9ee'), ('--mut', '#a0acb8'), ('--acc', '#8fb8e3'),
         ('--line', '#3d4956'), ('--hair', '#2b343f'), ('--th', '#242f3b'), ('--box', '#1b2b3d'), ('--code', '#252e38'),
         ('--ok', '#86c795'), ('--ok-bg', '#18281d'), ('--warn', '#e3b055'), ('--warn-bg', '#2c2414'), ('--warn-line', '#7d6126'),
         ('--bad', '#e58d83'), ('--bad-bg', '#2e1c1a'), ('--bad-line', '#7f4640'))
_FONT = '"Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif'
_MONO = 'Consolas,"D2Coding",monospace'


def _decl(pairs):
    return ';'.join('%s:%s' % kv for kv in pairs)


def _css_tokens():
    dark = _decl(_DARK) + ';color-scheme:dark'
    return [
        ':root{%s;color-scheme:light}' % _decl(_LIGHT),
        '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){%s}}' % dark,
        ':root[data-theme="dark"]{%s}' % dark,
    ]


_CSS_BASE = r'''
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:1rem/1.75 @FONT@;word-break:keep-all;overflow-wrap:break-word}
a{color:var(--acc)}
a:focus-visible{outline:2px solid var(--acc);outline-offset:2px;border-radius:2px}
.top{max-width:880px;margin:0 auto;padding:16px 8px 0;display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 20px;font-size:14px}
.top a{text-decoration:none}
.top a:hover{text-decoration:underline}
.top .sib::after{content:" \2192"}
.sheet{max-width:880px;margin:12px auto 0;padding:56px 64px 60px;background:var(--paper);border:1px solid var(--hair);border-radius:10px;box-shadow:0 1px 2px rgba(15,23,42,.04),0 12px 32px rgba(15,23,42,.06)}
.foot{max-width:880px;margin:0 auto;padding:14px 8px 44px;color:var(--mut);font-size:12.5px;line-height:1.7}
.foot p{margin:0}
h1{margin:0;font-size:33px;line-height:1.25;letter-spacing:-.01em;color:var(--acc);text-wrap:balance}
.subtitle{margin:8px 0 0;font-size:18px;line-height:1.5;font-weight:600}
.status{margin:16px 0 0;font-size:13px;line-height:1.75;color:var(--mut)}
.oneline{margin:16px 0 0;padding:13px 18px;border-left:5px solid var(--acc);border-radius:0 6px 6px 0;background:var(--box);font-size:16.5px;line-height:1.7}
h2{margin:44px 0 12px;font-size:21px;line-height:1.4;color:var(--acc);text-wrap:balance}
h2 .no{font-variant-numeric:tabular-nums}
p{margin:10px 0}
ul,ol{margin:10px 0;padding-left:1.35em}
ol{padding-left:1.6em}
li{margin:5px 0}
li>ul{margin:5px 0 7px;padding-left:1.25em;list-style:none}
li>ul>li{position:relative}
li>ul>li::before{content:"\2013";position:absolute;left:-1.15em;color:var(--mut)}
strong,b{font-weight:700}
em{font-style:normal;color:var(--acc)}
code{font-family:@MONO@;font-size:.86em;padding:1px 5px;border-radius:4px;background:var(--code);white-space:nowrap}
code.path{white-space:normal;overflow-wrap:anywhere}
.cite{text-decoration:none;font-variant-numeric:tabular-nums}
.cite:hover{text-decoration:underline}
.wrap{overflow-x:auto;margin:12px 0 16px}
table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.6}
th,td{border:1px solid var(--line);padding:7px 10px;vertical-align:top;text-align:left}
th{background:var(--th);font-weight:700}
:target{scroll-margin-top:16px}
tr:target>td,.refs li:target{background:var(--box)}
'''

_CSS_PLAN = r'''
.eyebrow{margin:0 0 8px;font-size:13px;font-weight:700;letter-spacing:.06em;color:var(--mut)}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:18px 0 0;padding:0 0 16px;border-bottom:2px solid var(--acc)}
.date{margin-right:6px;font-size:13.5px;color:var(--mut);font-variant-numeric:tabular-nums}
.badge{display:inline-block;padding:2px 11px;border:1px solid var(--line);border-radius:999px;font-size:12.5px;line-height:1.6;color:var(--ink)}
.badge.hold{border-color:var(--warn-line);background:var(--warn-bg);color:var(--warn);font-weight:700}
.toc{margin:22px 0 0;padding:14px 20px 12px;border:1px solid var(--hair);border-radius:8px}
.toc b{display:block;margin:0 0 4px;font-size:12.5px;letter-spacing:.08em;color:var(--mut)}
.toc ol{margin:0;padding:0;list-style:none;columns:2;column-gap:32px;font-size:14px}
.toc li{margin:0;padding:2px 0;break-inside:avoid}
.toc a{display:grid;grid-template-columns:1.9em minmax(0,1fr);color:var(--ink);text-decoration:none}
.toc a:hover{color:var(--acc);text-decoration:underline}
.toc .no{color:var(--acc);font-weight:700}
h2{padding-bottom:8px;border-bottom:1px solid var(--hair)}
.sub{margin:28px 0 8px;font-size:16.5px;line-height:1.5}
.road{margin:16px 0 0;padding:0;list-style:none}
.step{position:relative;display:grid;grid-template-columns:76px minmax(0,1fr);gap:0 14px;margin:0;padding:0 0 12px}
.step::before{content:"";position:absolute;left:37px;top:30px;bottom:0;width:2px;background:var(--hair)}
.step:last-child::before{display:none}
.node{position:relative;align-self:start;margin-top:10px;padding:2px 0;border-radius:999px;background:var(--acc);color:var(--paper);font-size:12.5px;line-height:1.7;text-align:center;font-variant-numeric:tabular-nums}
.node b{font-size:14px}
.card{min-width:0;padding:11px 16px 12px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.step.key .card{border:2px solid var(--acc);padding:10px 15px 11px}
.shead{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px}
.shead h3{margin:0 4px 0 0;font-size:16.5px;line-height:1.5}
.chip{display:inline-block;padding:1px 9px;border-radius:999px;background:var(--th);color:var(--mut);font-size:12.5px;font-weight:700;line-height:1.6;white-space:nowrap}
.chip.key{background:var(--acc);color:var(--paper)}
.card p{margin:6px 0 0;font-size:15px}
.gate{padding:7px 12px;border-left:3px solid var(--acc);border-radius:0 6px 6px 0;background:var(--box)}
.gk{display:inline-block;margin-right:8px;padding:0 7px;border-radius:4px;background:var(--acc);color:var(--paper);font-size:12px;font-weight:700;line-height:1.7}
.sched{margin:4px 0 0 90px;padding:9px 14px;border:1px dashed var(--line);border-radius:8px;font-size:14.5px}
.sched b{margin-right:6px}
.tag{margin-right:8px;color:var(--mut);font-size:13px}
.fork td:first-child{width:27%;font-weight:700}
.fork .chip{margin-right:6px}
.k-ga{background:var(--ok-bg);color:var(--ok)}
.k-na{background:var(--box);color:var(--acc)}
.k-ma{background:var(--warn-bg);color:var(--warn)}
.k-ra{background:var(--bad-bg);color:var(--bad)}
.k-da{background:var(--th);color:var(--mut)}
.papers td:first-child{width:17%;font-weight:700}
.papers td:nth-child(2){width:32%}
.papers td:nth-child(3){width:31%}
.box{margin:14px 0 4px;padding:14px 20px 12px;border-radius:8px}
.box>:first-child{margin-top:0}
.box>:last-child{margin-bottom:0}
.box.emph{border-left:5px solid var(--acc);background:var(--box)}
.box.warn{border-left:5px solid var(--warn-line);background:var(--warn-bg)}
.box.dont{border:2px solid var(--bad-line);padding:12px 20px 10px}
.box.dont ul{padding-left:0;list-style:none}
.box.dont li{position:relative;padding-left:1.7em}
.box.dont li::before{content:"\00d7";position:absolute;left:.25em;color:var(--bad);font-weight:700}
.qa td.q{width:42%}
.qa td.rec{width:25%}
.qa td.ans{font-weight:700}
.qn{margin-right:4px;color:var(--acc)}
.vsrc{font-size:13.5px;color:var(--mut)}
.verdict{margin:14px 0 4px;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.vline{margin:0;padding:14px 20px;border-bottom:1px solid var(--line);background:var(--box);font-size:16px;line-height:1.7}
.vk{display:inline-block;margin-right:10px;padding:0 9px;border-radius:4px;background:var(--acc);color:var(--paper);font-size:13px;font-weight:700;line-height:1.75}
.vbody{padding:4px 20px 12px}
.vh{margin:14px 0 6px;font-size:15.5px;line-height:1.5}
.findings{display:grid;gap:10px;margin:8px 0 4px}
.finding{padding:10px 16px 11px;border:1px solid var(--bad-line);border-left:5px solid var(--bad);border-radius:8px;background:var(--bad-bg)}
.finding p{margin:5px 0 0;font-size:15px}
.finding .fhead{margin:0;font-size:14px}
.ptag{display:inline-block;margin-right:6px;padding:0 7px;border-radius:4px;background:var(--bad);color:var(--paper);font-size:12px;font-weight:700;line-height:1.7}
.fhead code{background:none;padding:0;font-size:14px;font-weight:700;color:var(--bad)}
.finding .fix{margin-top:8px;padding-top:8px;border-top:1px dashed var(--bad-line)}
.fix b{color:var(--ok)}
.vbody ul{font-size:15px}
.refs{margin:12px 0 0;padding:0;list-style:none;font-size:14.5px;line-height:1.65}
.refs li{display:grid;grid-template-columns:2.6em minmax(0,1fr);gap:0 8px;margin:0;padding:9px 6px;border-top:1px solid var(--hair)}
.refs li:first-child{border-top:0}
.rn{color:var(--acc);font-weight:700;text-align:right;font-variant-numeric:tabular-nums}
.slugline{display:block;margin-top:2px;font-size:12px;color:var(--mut)}
.slug{padding:0;background:none;font-family:@MONO@;font-size:12px;color:var(--mut);white-space:normal;overflow-wrap:anywhere}
'''

_CSS_NEWCOMER = r'''
h1{font-size:31px}
.subtitle{margin:6px 0 0;font-weight:400}
.audience{margin:4px 0 0;font-size:14px;color:var(--mut)}
.statusline{margin:6px 0 0;padding:0 0 12px;border-bottom:2px solid var(--acc);font-size:13px;color:var(--mut)}
.leadin{margin:22px 0 8px}
math{font-family:"Cambria Math","STIX Two Math","Latin Modern Math",math;font-size:1.06em}
.eq{margin:14px 0;padding:2px 0;overflow-x:auto;text-align:center}
.fig{margin:20px 0;text-align:center}
.fig img{max-width:100%;height:auto;border-radius:4px;background:#fff}
.fig figcaption{margin-top:6px;font-size:13px;line-height:1.6;color:var(--mut)}
'''

_CSS_PHONE = r'''
@media (max-width:640px){
body{font-size:15px}
.top{padding:12px 16px 0}
.sheet{margin:10px 0 0;padding:28px 16px 34px;border-left:0;border-right:0;border-radius:0;box-shadow:none}
.foot{padding:12px 16px 36px}
h1{font-size:26px}
.subtitle{font-size:16px}
.oneline{padding:11px 14px;font-size:15.5px}
h2{margin-top:34px;font-size:19px}
table{font-size:13.5px}
table.c3{min-width:520px}
table.c4{min-width:640px}
.toc ol{columns:1}
.step{grid-template-columns:minmax(0,1fr);padding-bottom:14px}
.step::before{display:none}
.node{justify-self:start;margin:0 0 6px;padding:1px 12px}
.sched{margin-left:0}
.fork td:first-child{width:32%}
.fork .chip{display:block;width:max-content;margin:0 0 3px}
.box{padding:12px 14px 10px}
.box.dont{padding:10px 14px 8px}
.vline{padding:12px 14px}
.vbody{padding:2px 14px 10px}
.finding{padding:9px 12px 10px}
table.stack{min-width:0}
.stack thead{display:none}
.stack,.stack tbody,.stack tr,.stack td{display:block;width:auto}
.stack tr{margin:0 0 10px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.stack td{width:auto !important;border:0;border-top:1px solid var(--hair);padding:8px 12px}
.stack td:first-child{border-top:0;background:var(--th)}
.stack td[data-k]::before{content:attr(data-k);display:block;font-size:12px;font-weight:700;color:var(--mut)}
}
'''


def _css_print(page_title):
    light = dict(_LIGHT)
    light['--bg'] = '#fff'
    light['--paper'] = '#fff'
    forced = _decl((k, light[k]) for k, _v in _LIGHT)
    return '\n'.join([
        '@media print{',
        ':root:root{%s;color-scheme:light}' % forced,
        '@page{size:A4;margin:20mm 18mm 18mm;@bottom-center{content:"%s  ·  " counter(page) " / " counter(pages);'
        'font-family:%s;font-size:8pt;color:#5b6770}}' % (page_title, _FONT),
        # 글자 크기는 모두 rem 이라 뿌리 크기 하나로 본문 10.5 pt (형식 기준 docx 의 본문) 에 맞춰 같이 줄어든다
        'html{font-size:10.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}',
        'body{line-height:1.62}',
        '.top,.foot{display:none}',
        '.sheet{max-width:none;margin:0;padding:0;border:0;border-radius:0;box-shadow:none}',
        'a{color:inherit;text-decoration:none}',
        '.refs{line-height:1.5}',
        '.refs li{padding:6px 4px}',
        'h2{margin-top:20pt;break-after:avoid}',
        '.sub,.vh,.leadin,.shead,.vsrc{break-after:avoid}',
        '.wrap,.verdict{overflow:visible}',
        '.pb{break-before:page}',
        '.pb>h2:first-child{margin-top:0}',
        'tr,.step,.finding,.box,.oneline,.sched,.refs li,.vline,.toc,table.keep,.fig,.eq{break-inside:avoid}',
        '}',
    ])


def _rem(m):
    """font-size:Npx → rem (뿌리 16 px 기준 · N 은 0.5 단위라 값이 정확히 떨어진다)."""
    s = ('%.5f' % (float(m.group(1)) / 16.0)).rstrip('0').rstrip('.')
    return 'font-size:%srem' % (s[1:] if s.startswith('0.') else s)


def _style(kind, page_title):
    parts = _css_tokens()
    parts.append(_CSS_BASE.strip('\n'))
    parts.append((_CSS_PLAN if kind == 'plan' else _CSS_NEWCOMER).strip('\n'))
    parts.append(_CSS_PHONE.strip('\n'))
    css = re.sub(r'font-size:([0-9.]+)px', _rem, '\n'.join(parts))
    return (css + '\n' + _css_print(page_title)).replace('@FONT@', _FONT).replace('@MONO@', _MONO)


def _page(kind, doc, page_title, sib_url, sib_text, body, foot):
    out = [
        '<!doctype html>',
        '<html lang="ko">',
        '<!-- 생성물: 손으로 고치지 않는다.  원문 %s (sha256 %s) 을 %s 가 옮겼다.  고치려면 원문을 고친 뒤 --write.  시험 %s -->'
        % (doc.name, doc.sha256[:16], SELF, TEST),
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % esc(page_title),
        '<style>',
        _style(kind, TITLE),
        '</style>',
        '</head>',
        '<body>',
        '<nav class="top" aria-label="이동"><a class="home" href="/">← DEM/MPM Analyzer 처음으로</a>'
        '<a class="sib" href="%s">%s</a></nav>' % (sib_url, esc(sib_text)),
        '<main class="sheet">',
        body,
        '</main>',
        '<footer class="foot">',
        foot,
        '</footer>',
        '</body>',
        '</html>',
    ]
    return '\n'.join(out) + '\n'


def _lead_html(doc, ctx):
    return ['<p class="status">%s</p>' % inline(doc.status, ctx), '<div class="oneline">%s</div>' % inline(doc.oneline, ctx)]


def _h2(sec):
    if sec.num is None:
        return '<h2>%s</h2>' % esc(sec.title)
    return '<h2><span class="no">%d.</span> %s</h2>' % (sec.num, esc(sec.title))


def _section_html(sec, inner, page_break):
    cls = ' class="pb"' if page_break else ''
    return '<section id="%s"%s>\n%s\n%s\n</section>' % (sec.sid, cls, _h2(sec), inner)


# ═════════════════════════════ (a) 계획서 ═════════════════════════════
_PLAN_KINDS = (
    ('papers', re.compile(r'^논문 .*계획의 어디에'), '논문이 계획의 어디에 들어갔나 (논문 표)'),
    ('roadmap', re.compile(r'^단계$'), '단계 (로드맵)'),
    ('emph', re.compile(r'^진밀도 '), '진밀도 … (강조 상자)'),
    ('warn', re.compile(r'빈 곳$'), '… 빈 곳 (경고 상자)'),
    ('dont', re.compile(r'^하지 않는 말$'), '하지 않는 말 (테두리 상자)'),
    ('qa', re.compile(r'^1저자 결정'), '1저자 결정 (질문 표)'),
    ('verdict', re.compile(r'^Codex 반박 판정'), 'Codex 반박 판정 (판정 상자)'),
    ('refs', re.compile(r'^참고문헌$'), '참고문헌 (번호 서지)'),
)
_RE_STEP_HEAD = re.compile(r'^단계 (\d+) (\S.*)$')
_RE_STEP_REST = re.compile(r'^(?: \(([^()]+)\))?(?:(: )|\.?$)')
_RE_SCHED_REST = re.compile(r'^ (\[[^\[\]]+\]): ')
_RE_FORK = re.compile(r'^\((.)\) (\S.*)$')
_RE_QN = re.compile(r'^Q(\d+)\.$')
_RE_FINDING_ID = re.compile(r'^[A-Z]+-\d+$')


def _plan_badges(doc):
    """표지 머리의 배지 셋 = 원문 "지위" 줄의 글 (없으면 rc 2: 지위가 바뀐 것을 조용히 넘기지 않는다)."""
    text, no = plain(doc.status), doc.status_line
    out = []
    for lit in ('결과 0 건', '실행 GO 요청 아님'):
        if lit not in text:
            raise ParseError(doc.name, no, '표지 배지를 만들 글 "%s" 이 "지위" 줄에 없다' % lit)
        out.append((lit, ''))
    m = re.search(r'Codex .*판정 \d\d-\d\d = (.+?) · 아래 §\d', text)
    if not m:
        raise ParseError(doc.name, no, '표지 배지를 만들 글 "Codex … 판정 MM-DD = … · 아래 §N" 이 "지위" 줄에 없다')
    out.append(('Codex 판정 = ' + m.group(1), 'hold' if '(HOLD)' in m.group(1) else ''))
    return out


def _roadmap(sec, ctx):
    name = ctx.name
    if len(sec.blocks) != 3 or not isinstance(sec.blocks[0], List) or sec.blocks[0].ordered \
            or not isinstance(sec.blocks[1], Para) or not sec.blocks[1].bold_only or not isinstance(sec.blocks[2], Table):
        raise ParseError(name, sec.line, '"단계" 절은 단계 목록 · 굵은 갈림 머리 · 갈림 표의 차례여야 한다')
    lst, sub, tb = sec.blocks
    out = ['<ol class="road">']
    sched, k = None, 0
    for it in lst.items:
        if it.children:
            raise ParseError(name, it.children[0].line, '단계 줄 아래의 딸린 목록은 받지 않는다')
        if not it.inl or it.inl[0][0] != 'b':
            raise ParseError(name, it.line, '단계 줄은 "**단계 N 이름**" 또는 "**일정**" 으로 시작해야 한다')
        head, rest = plain(it.inl[0][1]), it.inl[1:]
        first = rest[0][1] if rest and rest[0][0] == 't' else ''
        if head == '일정':
            ms = _RE_SCHED_REST.match(first)
            if not ms or sched is not None or it is not lst.items[-1]:
                raise ParseError(name, it.line, '일정 줄은 목록의 끝에 하나 · "**일정** [표지]: 글" 꼴이어야 한다')
            body = ([('t', first[ms.end():])] if first[ms.end():] else []) + rest[1:]
            sched = '<div class="sched"><b>일정</b> <span class="tag">%s</span> %s</div>' % (esc(ms.group(1)), inline(body, ctx))
            continue
        mh = _RE_STEP_HEAD.match(head)
        if not mh:
            raise ParseError(name, it.line, '단계 줄은 "**단계 N 이름**" 으로 시작해야 한다')
        if int(mh.group(1)) != k:
            raise ParseError(name, it.line, '단계 번호가 차례가 아니다 (기대 %d · 지금 %s)' % (k, mh.group(1)))
        mr = _RE_STEP_REST.match(first)
        if not mr:
            raise ParseError(name, it.line, '단계 줄은 "**단계 N 이름** (괄호): 내용" 꼴이어야 한다')
        if mr.group(2):
            body = ([('t', first[mr.end():])] if first[mr.end():] else []) + rest[1:]
            if not body:
                raise ParseError(name, it.line, '단계 줄의 ":" 뒤에 내용이 없다')
        else:
            # ":" 없이 끝나는 줄 ("**단계 7 구조 · 수송**." · 괄호만) 뒤에 다른 글 · 표지가 남으면 버리지 않고 멈춘다
            if rest and (len(rest) > 1 or rest[0][0] != 't' or mr.end() != len(first)):
                raise ParseError(name, it.line, '단계 줄은 "**단계 N 이름** (괄호): 내용" 꼴이어야 한다')
            body = []
        chips = mr.group(1).split(' · ') if mr.group(1) else []
        key = '핵심' in chips
        out.append('<li class="step%s" id="step-%d">' % (' key' if key else '', k))
        out.append('<span class="node"><span>단계</span> <b>%d</b></span>' % k)
        out.append('<div class="card">')
        out.append('<div class="shead"><h3>%s</h3>%s</div>' % (
            esc(mh.group(2)), ' '.join('<span class="chip%s">%s</span>' % (' key' if c == '핵심' else '', esc(c)) for c in chips)))
        group = []

        def flush_group():
            if group:
                out.append('<p>%s</p>' % '  '.join(group))
                del group[:]
        for sent in sentences(body):
            if plain(sent).endswith('문이다.'):
                flush_group()
                out.append('<p class="gate"><span class="gk">문</span> %s</p>' % inline(sent, ctx))
            else:
                group.append(inline(sent, ctx))
        flush_group()
        out.append('</div>')
        out.append('</li>')
        k += 1
    if k == 0:
        raise ParseError(name, lst.line, '단계 줄이 하나도 없다')
    out.append('</ol>')
    if sched:
        out.append(sched)
    out.append('<h3 class="sub">%s</h3>' % inline(sub.inl[0][1], ctx))
    if len(tb.header) != 2:
        raise ParseError(name, tb.line, '갈림 표는 두 칸 (결과 · 길) 이어야 한다')
    out.append('<div class="wrap">')
    out.append('<table class="fork">')
    out.append('<thead><tr>%s</tr></thead>' % ''.join('<th scope="col">%s</th>' % inline(c, ctx) for c in tb.header))
    out.append('<tbody>')
    seen = set()
    for row, no in zip(tb.rows, tb.row_lines):
        mf = _RE_FORK.match(plain(row[0])) if all(kk == 't' for kk, _v in row[0]) else None
        if not mf or mf.group(1) not in FORK_CHIPS or mf.group(1) in seen:
            raise ParseError(name, no, '갈림 표의 첫 칸은 "(가|나|마|라|다) 이름" 꼴이고 글자가 겹치지 않아야 한다')
        seen.add(mf.group(1))
        out.append('<tr><td><span class="chip %s">(%s)</span> %s</td><td>%s</td></tr>' % (
            FORK_CHIPS[mf.group(1)], mf.group(1), esc(mf.group(2)), inline(row[1], ctx)))
    out.append('</tbody>')
    out.append('</table>')
    out.append('</div>')
    return '\n'.join(out)


def _papers(sec, ctx):
    tb = next((b for b in sec.blocks if isinstance(b, Table)), None)
    if tb is None or plain(tb.header[0]) != '논문':
        raise ParseError(ctx.name, sec.line, '이 절에는 첫 칸 머리가 "논문" 인 표가 있어야 한다')
    for row, no in zip(tb.rows, tb.row_lines):
        m = re.match(r'^\[(\d+)\] \S', plain(row[0]))
        if not m:
            raise ParseError(ctx.name, no, '논문 표의 첫 칸은 "[n] 저자 연도" 꼴이어야 한다')
    out = []
    for b in sec.blocks:
        out.append(r_table(b, ctx, cls='papers stack', labels=True) if b is tb else r_block(b, ctx))
    return '\n'.join(out)


def _qa(sec, ctx):
    if len(sec.blocks) != 1 or not isinstance(sec.blocks[0], List) or sec.blocks[0].ordered:
        raise ParseError(ctx.name, sec.line, '"1저자 결정" 절은 질문 목록 하나여야 한다')
    out = ['<div class="wrap">', '<table class="qa stack">',
           '<thead><tr><th scope="col">질문</th><th scope="col">권고</th><th scope="col">1저자 답</th></tr></thead>', '<tbody>']
    for k, it in enumerate(sec.blocks[0].items, 1):
        bad = ParseError(ctx.name, it.line, '질문 줄은 "**Q%d.** 질문  권고: …  답: …" 꼴이어야 한다 (빈칸 둘로 가른다)' % k)
        if it.children or not it.inl or it.inl[0][0] != 'b':
            raise bad
        mq = _RE_QN.match(plain(it.inl[0][1]))
        if not mq or int(mq.group(1)) != k:
            raise bad
        rest = it.inl[1:]
        if not rest or rest[0][0] != 't' or not rest[0][1].startswith(' '):
            raise bad
        rest = [('t', rest[0][1][1:])] + rest[1:] if rest[0][1][1:] else rest[1:]
        a = split_nodes(rest, '  권고: ')
        b = split_nodes(a[1], '  답: ') if a else None
        if not a or not b or not a[0] or not b[0] or not b[1]:
            raise bad
        out.append('<tr id="q%d"><td class="q"><b class="qn">Q%d.</b> %s</td><td class="rec" data-k="권고">%s</td>'
                   '<td class="ans" data-k="1저자 답">%s</td></tr>' % (k, k, inline(a[0], ctx), inline(b[0], ctx), inline(b[1], ctx)))
    out.extend(['</tbody>', '</table>', '</div>'])
    return '\n'.join(out)


def _verdict(sec, ctx):
    name = ctx.name
    lists = [b for b in sec.blocks if isinstance(b, List)]
    if len(lists) != 1 or lists[0].ordered or sec.blocks[-1] is not lists[0] or any(not isinstance(b, Para) for b in sec.blocks[:-1]):
        raise ParseError(name, sec.line, '"Codex 반박 판정" 절은 문단 (근거 문서) 다음에 판정 목록 하나여야 한다')
    out = ['<p class="vsrc">%s</p>' % inline(b.inl, ctx) for b in sec.blocks[:-1]]
    items = lists[0].items

    def lead_of(it):
        if not it.inl or it.inl[0][0] != 'b':
            raise ParseError(name, it.line, '판정 목록의 줄은 굵은 머리 ("**판정**: …") 로 시작해야 한다')
        return plain(it.inl[0][1])
    first = items[0]
    rest = first.inl[1:]
    if lead_of(first) != '판정' or first.children or not rest or rest[0][0] != 't' or not rest[0][1].startswith(': '):
        raise ParseError(name, first.line, '판정 목록의 첫 줄은 "**판정**: 글" 이어야 한다')
    body = ([('t', rest[0][1][2:])] if rest[0][1][2:] else []) + rest[1:]
    out.append('<div class="verdict">')
    out.append('<p class="vline"><span class="vk">판정</span> %s</p>' % inline(body, ctx))
    out.append('<div class="vbody">')
    n_p1, leaf, seen_ids = 0, [], set()

    def flush_leaf():
        if leaf:
            out.append('<ul>')
            out.extend(leaf)
            out.append('</ul>')
            del leaf[:]
    for it in items[1:]:
        lead = lead_of(it)
        if not it.children:
            leaf.append('<li>%s</li>' % inline(it.inl, ctx))
            continue
        flush_leaf()
        if len(it.inl) != 1:
            raise ParseError(name, it.line, '딸린 목록이 있는 판정 줄은 굵은 머리만 있어야 한다')
        out.append('<h3 class="vh">%s</h3>' % inline(it.inl[0][1], ctx))
        if '(P1)' not in lead:
            out.append('<ul>')
            out.extend('<li>%s</li>' % inline(ch.inl, ctx) for ch in it.children)
            out.append('</ul>')
            continue
        n_p1 += 1
        out.append('<div class="findings">')
        for ch in it.children:
            if not ch.inl or ch.inl[0][0] != 'c' or not _RE_FINDING_ID.match(ch.inl[0][1]) or len(ch.inl) < 2 \
                    or ch.inl[1][0] != 't' or not ch.inl[1][1].startswith(' '):
                raise ParseError(name, ch.line, '큰 지적 (P1) 줄은 "`ID` 글" 꼴이어야 한다')
            fid = ch.inl[0][1]
            #  지적 ID 는 그 카드의 자리 (id) 가 된다 → 겹치거나 다른 자리 이름 (ref-N · step-N) 과 부딪치면 멈춘다
            if fid.lower() in seen_ids or fid.lower().startswith(('ref-', 'step-')):
                raise ParseError(name, ch.line, '큰 지적 (P1) 의 ID "%s" 가 겹치거나 다른 자리 이름과 부딪친다' % fid)
            seen_ids.add(fid.lower())
            text = [('t', ch.inl[1][1][1:])] + ch.inl[2:]
            parts = split_nodes(text, '  고침: ')
            out.append('<div class="finding" id="%s">' % fid.lower())
            out.append('<p class="fhead"><span class="ptag">P1</span> <code>%s</code></p>' % esc(fid))
            if parts:
                out.append('<p>%s</p>' % inline(parts[0], ctx))
                out.append('<p class="fix"><b>고침</b>: %s</p>' % inline(parts[1], ctx))
            else:
                out.append('<p>%s</p>' % inline(text, ctx))
            out.append('</div>')
        out.append('</div>')
    flush_leaf()
    if n_p1 != 1:
        raise ParseError(name, lists[0].line, '판정 목록에 "(P1)" 머리 (큰 지적) 가 하나 있어야 한다')
    out.append('</div>')
    out.append('</div>')
    return '\n'.join(out)


def _refs_plan(sec, tb, ctx):
    #  번호 서지로 실으면 머리 행의 앞 두 칸 글은 화면에 없다 (셋째 칸 머리는 행마다 이름표) → 그 두 칸이 "#" · "서지" 일 때만 받는다
    if len(tb.header) != 3 or [plain(c) for c in tb.header[:2]] != ['#', '서지']:
        raise ParseError(ctx.name, tb.line, '참고문헌 표의 머리 행은 "# | 서지 | (slug 칸 이름)" 세 칸이어야 한다')
    out = [r_block(b, ctx) for b in sec.blocks if b is not tb]
    if sec.blocks[-1] is not tb:
        raise ParseError(ctx.name, tb.line, '참고문헌 표는 절의 끝에 있어야 한다')
    label = inline(tb.header[2], ctx)
    plain_ctx = Ctx(ctx.name, frozenset(), ctx.kind)
    out.append('<ol class="refs">')
    for k, (row, no) in enumerate(zip(tb.rows, tb.row_lines), 1):
        if len(row[2]) != 1 or row[2][0][0] != 'c':
            raise ParseError(ctx.name, no, '참고문헌 표의 셋째 칸은 고정폭 slug 하나여야 한다')
        out.append('<li id="ref-%d"><span class="rn">[%d]</span> <span class="rc">%s <span class="slugline">%s <code class="slug">%s</code></span></span></li>'
                   % (k, k, inline(row[1], plain_ctx), label, esc(row[2][0][1])))
    out.append('</ol>')
    return '\n'.join(out)


def render_plan(doc):
    """(a) 계획서 페이지."""
    name = doc.name
    _refsec, reftb, nums = _ref_numbers(doc)
    cites = frozenset(nums)
    _check_cites(doc, cites)
    ctx = Ctx(name, cites, 'plan')

    kinds = {}
    for kind, rx, label in _PLAN_KINDS:
        hits = [s for s in doc.sections if rx.search(s.title)]
        if len(hits) != 1:
            raise ParseError(name, hits[1].line if len(hits) > 1 else doc.n_lines,
                             '계획서 꼴에 필요한 절 "%s" 이 %d 개다 (하나여야 한다)' % (label, len(hits)))
        if hits[0].sid in kinds:
            raise ParseError(name, hits[0].line, '한 절이 계획서 꼴 둘에 걸린다')
        kinds[hits[0].sid] = kind
    if doc.tag is None:
        raise ParseError(name, doc.h1_line, '제목 줄은 "# [꼬리표] 부제" 꼴이어야 한다')
    body = ['<header class="cover">',
            '<p class="eyebrow">%s</p>' % esc(doc.tag),
            '<h1>%s</h1>' % esc(TITLE),
            '<p class="subtitle">%s</p>' % esc(doc.subtitle),
            '<div class="meta"><span class="date">%s</span> %s</div>' % (
                doc.date, ' '.join('<span class="badge%s">%s</span>' % (' ' + c if c else '', esc(t)) for t, c in _plan_badges(doc))),
            '</header>']
    body.extend(_lead_html(doc, ctx))
    body.append('<nav class="toc" aria-label="차례"><b>차례</b><ol>%s</ol></nav>' % ''.join(
        '<li><a href="#%s"><span class="no">%s</span> %s</a></li>' % (s.sid, '%d.' % s.num if s.num is not None else '', esc(s.title))
        for s in doc.sections))
    for sec in doc.sections:
        kind = kinds.get(sec.sid)
        if kind == 'roadmap':
            inner = _roadmap(sec, ctx)
        elif kind == 'papers':
            inner = _papers(sec, ctx)
        elif kind in ('emph', 'warn', 'dont'):
            if kind == 'dont' and (len(sec.blocks) != 1 or not isinstance(sec.blocks[0], List)):
                raise ParseError(name, sec.line, '"하지 않는 말" 절은 목록 하나여야 한다')
            inner = '<div class="box %s">\n%s\n</div>' % (kind, r_blocks(sec.blocks, ctx))
        elif kind == 'qa':
            inner = _qa(sec, ctx)
        elif kind == 'verdict':
            inner = _verdict(sec, ctx)
        elif kind == 'refs':
            inner = _refs_plan(sec, reftb, ctx)
        else:
            inner = r_blocks(sec.blocks, ctx)
        body.append(_section_html(sec, inner, kind in PLAN_PAGE_BREAK_KINDS))
    foot = ('<p>원문 %s 을 생성기 %s 가 옮긴 페이지입니다.  글을 고치려면 원문을 고친 뒤 다시 만듭니다.</p>'
            % (_code(name), _code(SELF)))
    return _page('plan', doc, TITLE, URL_NEWCOMER, NEWCOMER_AUDIENCE[0], '\n'.join(body), foot)


# ═════════════════════════════ (b) 처음 보는 분 · (c) docx JSON ═════════════════════════════
def _newcomer_status_line(doc):
    """제목 블록의 넷째 줄 조각들 (날짜 · 지위 셋).  뒷받침하는 글이 원고에 없으면 멈춘다."""
    whole = '\n'.join([plain(doc.status), plain(doc.oneline)] + [_section_text(s) for s in doc.sections])
    status = NEWCOMER_STATUS if '종결 가능' in whole else NEWCOMER_STATUS_LEGACY
    for text, needs in (NEWCOMER_AUDIENCE,) + status:
        for need in needs:
            if need not in whole:
                raise ParseError(doc.name, doc.status_line, '제목 블록의 줄 "%s" 을 뒷받침하는 글 "%s" 이 원고에 없다' % (text, need))
    return [doc.date] + [t for t, _n in status]


def _section_text(sec):
    out = [sec.heading]
    for b in sec.blocks:
        if isinstance(b, Para):
            out.append(plain(b.inl))
        elif isinstance(b, List):
            for it in b.items:
                out.append(plain(it.inl))
                out.extend(plain(ch.inl) for ch in it.children)
        elif isinstance(b, Table):
            out.append(' '.join(plain(c) for c in b.header))
            out.extend(' '.join(plain(c) for c in row) for row in b.rows)
        elif isinstance(b, Figure):
            out.append(plain(b.caption))
    return '\n'.join(out)


def _table_layout(doc, tb):
    key = tuple(plain(c) for c in tb.header)
    if key not in NEWCOMER_TABLES:
        raise ParseError(doc.name, tb.line, '이 표 (머리 %s) 의 열 너비 규칙이 없다: %s 의 NEWCOMER_TABLES 에 한 줄을 더할 것'
                         % (' | '.join(key), SELF))
    widths, keep = NEWCOMER_TABLES[key]
    if len(widths) != len(key) or sum(widths) != DOCX_TEXT_WIDTH:
        raise ParseError(doc.name, tb.line, '열 너비 규칙의 칸 수 또는 합 (%d) 이 맞지 않는다' % DOCX_TEXT_WIDTH)
    return widths, keep


def render_newcomer(doc, math=None, figure=None):
    """(b) 처음 보는 분을 위한 설명 페이지 (형식 기준 docx 의 꼴).  math = 수식 저장소 · figure = 그림 읽개 (수식 · 그림이 있을 때)."""
    name = doc.name
    _refsec, reftb, nums = _ref_numbers(doc)
    cites = frozenset(nums)
    _check_cites(doc, cites)
    ctx = Ctx(name, cites, 'newcomer', math, figure)
    status = _newcomer_status_line(doc)
    body = ['<header class="doc-head">',
            '<h1>%s</h1>' % esc(TITLE),
            '<p class="subtitle">%s</p>' % esc(doc.subtitle),
            '<p class="audience">%s</p>' % esc(NEWCOMER_AUDIENCE[0]),
            '<p class="statusline">%s</p>' % esc('  ·  '.join(status)),
            '</header>']
    body.extend(_lead_html(doc, ctx))
    for sec in doc.sections:
        parts = []
        for b in sec.blocks:
            if isinstance(b, Table):
                widths, keep = _table_layout(doc, b)
                ids = ['ref-%d' % k for k in nums] if b is reftb else None
                parts.append(r_table(b, ctx, cls='keep' if keep else '', widths=widths, row_ids=ids))
            else:
                parts.append(r_block(b, ctx))
        body.append(_section_html(sec, '\n'.join(parts), sec.sid in NEWCOMER_PAGE_BREAKS))
    foot = ('<p>원고 %s 를 생성기 %s 가 옮긴 페이지입니다.  같은 글의 Word 문서는 %s 입니다.</p>'
            % (_code(name), _code(SELF), _code(DOCX_CANON)))
    return _page('newcomer', doc, TITLE + ' · ' + NEWCOMER_AUDIENCE[0], URL_PLAN, '자세한 계획서', '\n'.join(body), foot)


def _runs(nodes, math=None, b=False, i=False):
    """노드 → docx 런 목록 [{text, b?, i?, code?} 또는 {math: OMML}] (서식이 같은 이웃 글은 합친다 · 수식은 따로)."""
    out = []

    def put(text, bb, ii, cc):
        run = {'text': text}
        if bb:
            run['b'] = True
        if ii:
            run['i'] = True
        if cc:
            run['code'] = True
        if out and 'text' in out[-1] and [kv for kv in sorted(out[-1].items()) if kv[0] != 'text'] \
                == [kv for kv in sorted(run.items()) if kv[0] != 'text']:
            out[-1]['text'] += text
        else:
            out.append(run)
    for k, v in nodes:
        if k == 't':
            put(v, b, i, False)
        elif k == 'c':
            put(v, b, i, True)
        elif k == 'm':
            out.append({'math': math.get(False, v)['omml']})
        else:
            for r in _runs(v, math, b or k == 'b', i or k == 'i'):
                if 'math' in r:
                    out.append(r)
                else:
                    put(r['text'], r.get('b', False), r.get('i', False), r.get('code', False))
    return out


def docx_model(doc, math=None, figure=None):
    """(c) docx 빌더가 읽는 모델 (dict · 키 순서 고정).  math · figure = render_newcomer 와 같다."""
    _refsec, _reftb, nums = _ref_numbers(doc)
    _check_cites(doc, frozenset(nums))
    status = _newcomer_status_line(doc)

    def runs(nodes):
        return _runs(nodes, math)
    blocks = []
    for sec in doc.sections:
        head = {'t': 'h1', 'text': sec.heading}
        if sec.sid in NEWCOMER_PAGE_BREAKS:
            head['pageBreakBefore'] = True
        blocks.append(head)
        for bi, b in enumerate(sec.blocks):
            if isinstance(b, Para):
                p = {'t': 'p', 'runs': runs(b.inl)}
                if bi + 1 < len(sec.blocks) and isinstance(sec.blocks[bi + 1], Table):
                    p['keepNext'] = True
                blocks.append(p)
            elif isinstance(b, List):
                for it in b.items:
                    if b.ordered:
                        blocks.append({'t': 'ol', 'runs': runs(it.inl)})
                    else:
                        blocks.append({'t': 'li', 'level': 0, 'runs': runs(it.inl)})
                        blocks.extend({'t': 'li', 'level': 1, 'runs': runs(ch.inl)} for ch in it.children)
            elif isinstance(b, DisplayMath):
                blocks.append({'t': 'eq', 'omml': math.get(True, b.latex)['omml']})
            elif isinstance(b, Figure):
                f = figure(b)
                w, h, _pct = figure_display(f['px'], b.width_pct)
                blocks.append({'t': 'fig', 'path': f['rel'], 'sha256': f['sha256'], 'px': list(f['px']),
                               'width': w, 'height': h, 'alt': plain(b.caption), 'caption': runs(b.caption)})
            else:
                widths, keep = _table_layout(doc, b)
                blocks.append({'t': 'table', 'widths': list(widths), 'keep': keep,
                               'rows': [[runs(c) for c in b.header]] + [[runs(c) for c in row] for row in b.rows]})
    return {
        'schema': 'dem_redesign_plan_docx/1',
        'note': '생성물: 손으로 고치지 않는다.  %s --write 가 원고에서 만든다.  읽는 쪽 = scripts/build_dem_redesign_plan_docx.js' % SELF,
        'source': doc.name,
        'source_sha256': doc.sha256,
        'date': doc.date,
        'title': TITLE,
        'subtitle': doc.subtitle,
        'audience': NEWCOMER_AUDIENCE[0],
        'status_line': '  ·  '.join(status),
        'footer': TITLE,
        'creator': NEWCOMER_CREATOR,
        'text_width': DOCX_TEXT_WIDTH,
        'lead': [{'kind': 'status', 'runs': runs(doc.status)}, {'kind': 'oneline', 'runs': runs(doc.oneline)}],
        'blocks': blocks,
    }


def dumps_model(model):
    return json.dumps(model, ensure_ascii=False, indent=1) + '\n'


# ═════════════════════════════ 묶음 · 명령줄 ═════════════════════════════
def _read_text(root, rel):
    with open(os.path.join(root, *rel.split('/')), encoding='utf-8', newline='') as f:
        return f.read()


def _read_bytes(root, rel):
    try:
        with open(os.path.join(root, *rel.split('/')), 'rb') as f:
            return f.read()
    except OSError:
        return None


def build_newcomer(root, src_rel, convert=None):
    """처음 보는 분용 원고 하나 → (HTML, docx 모델 JSON, 수식 캐시 JSON 또는 None) 의 바이트.

    수식은 원고 옆 캐시 (math_cache_rel) 에서 읽는다.  캐시에 없는 식은 convert (= pandoc_convert) 가 있을 때만 바꾼다.
    수식이 하나도 없으면 캐시는 None 이다 (파일을 두지 않는다)."""
    doc = parse(_read_text(root, src_rel), src_rel, extended=True)
    cache_rel = math_cache_rel(src_rel)
    items = collect_math(doc)
    store = MathStore()
    if items:       # 수식이 없는 원고는 캐시를 읽지 않는다 (옆에 남은 캐시 파일은 "낡은 것" 으로 따로 잡힌다)
        try:
            store = MathStore.load(_read_bytes(root, cache_rel), cache_rel)
        except ParseError:
            if convert is None:
                raise
            # 변환기가 있을 때 (--write) 꼴이 다른 캐시는 버리고 처음부터 다시 만든다
        store.ensure(items, src_rel, cache_rel, convert)

    def figure(fig):
        return load_figure(root, src_rel, fig)
    page = render_newcomer(doc, store, figure).encode('utf-8')
    model = dumps_model(docx_model(doc, store, figure)).encode('utf-8')
    return page, model, (store.dumps().encode('utf-8') if store.used else None)


def build_all(root=None, convert=None):
    """원문 둘 → {리포 상대 경로: 바이트}.  ParseError = 받지 않는 구성 (또는 캐시에 없는 수식).

    원고에 수식이 있으면 그 수식 캐시 (math_cache_rel(SRC_NEWCOMER)) 도 생성물에 든다."""
    root = root or ROOT
    plan = parse(_read_text(root, SRC_PLAN), SRC_PLAN)
    page, model, cache = build_newcomer(root, SRC_NEWCOMER, convert)
    out = {OUT_PLAN: render_plan(plan).encode('utf-8'), OUT_NEWCOMER: page, OUT_MODEL: model}
    if cache is not None:
        out[math_cache_rel(SRC_NEWCOMER)] = cache
    return out


def main(argv=None, root=None):
    ap = argparse.ArgumentParser(description='DEM 재설계 계획서: 원문 둘에서 웹앱 정적 페이지 둘과 docx 빌더용 JSON 을 만든다.')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--write', action='store_true', help='생성물을 다시 쓴다 (캐시에 없는 수식은 pandoc 으로 바꾼다)')
    g.add_argument('--check', action='store_true', help='다시 만들어 커밋된 파일과 바이트를 견준다 (기본 · 쓰지 않는다 · pandoc 을 부르지 않는다)')
    g.add_argument('--write-math-cache', metavar='원고', default=None,
                   help='그 원고 (리포 상대 경로 · 시험 고정물 등) 의 수식 캐시만 pandoc 으로 다시 만들어 쓴다')
    args = ap.parse_args(argv)
    root = root or ROOT
    if args.write_math_cache:
        rel = args.write_math_cache.replace(os.sep, '/')
        try:
            _page_b, _model_b, cache = build_newcomer(root, rel, pandoc_convert)
        except ParseError as e:
            print('✗ %s' % e, file=sys.stderr)
            return 2
        except (OSError, UnicodeDecodeError, subprocess.SubprocessError) as e:
            print('✗ 원고를 읽을 수 없다: %s' % e, file=sys.stderr)
            return 2
        path = os.path.join(root, *math_cache_rel(rel).split('/'))
        if cache is None:
            if os.path.exists(path):
                os.remove(path)
            print('  수식이 없다: 캐시 파일을 두지 않는다 (%s)' % math_cache_rel(rel))
            return 0
        with open(path, 'wb') as f:
            f.write(cache)
        print('  쓴 파일 %s (%d B)' % (math_cache_rel(rel), len(cache)))
        return 0
    try:
        built = build_all(root, pandoc_convert if args.write else None)
    except ParseError as e:
        print('✗ %s' % e, file=sys.stderr)
        return 2
    except (OSError, UnicodeDecodeError, subprocess.SubprocessError) as e:
        print('✗ 원문을 읽을 수 없다: %s' % e, file=sys.stderr)
        return 2
    #  수식이 없는 원고 옆에 남은 캐시 파일 = 낡은 것 (생성물에 들지 않는다)
    stale = [rel for rel in (math_cache_rel(SRC_NEWCOMER),) if rel not in built and _read_bytes(root, rel) is not None]
    if args.write:
        for rel in sorted(built):
            path = os.path.join(root, *rel.split('/'))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(built[rel])
            print('  쓴 파일 %s (%d B)' % (rel, len(built[rel])))
        for rel in stale:
            os.remove(os.path.join(root, *rel.split('/')))
            print('  지운 파일 %s (원고에 수식이 없다)' % rel)
        return 0
    diff = []
    for rel in sorted(built):
        try:
            with open(os.path.join(root, *rel.split('/')), 'rb') as f:
                same = f.read() == built[rel]
        except OSError:
            same = False
        if not same:
            diff.append(rel)
    diff.extend(stale)
    if diff:
        for rel in diff:
            print('✗ 커밋된 파일이 원문에서 다시 만든 것과 다르다: %s' % rel, file=sys.stderr)
        print('  → python3 %s --write' % SELF, file=sys.stderr)
        return 1
    print('✓ 생성물 %d 개가 원문에서 다시 만든 것과 같다' % len(built))
    return 0


if __name__ == '__main__':
    sys.exit(main())
