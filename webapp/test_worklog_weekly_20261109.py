#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""주간보고 11-02 ~ 11-09 — 웹앱 `/worklog` 에 뜨는지 · 트랙 순서 · 거부 (1저자 11-09 "일주일동안 한거 다시 주간보고하게 webapp 갱신해줘").

주간보고는 새 라우트를 만들지 않는다 — `webapp/app.py` 는 봉인 32 (`scripts/run_network_194_parallel.py` CODE_FILES) 라
고치면 봉인 지문이 바뀐다.  이미 있는 `/worklog` 창구가 `docs/worklog/weekly_YYYYMMDD.md` 를 최신순으로 모아 렌더한다
(`_worklog_scan` · 키 = 8 자리 날짜만).  그래서 이 시험은 그 창구에 이번 주 리포트가 실제로 뜨는지 · 본문 숫자 · 절 ·
용훈 포메이션 트랙 순서 ([Rint ②] → [DEM 우선] Ⓐ Ⓑ Ⓒ → 나머지) · 인용 금지값 · 모델 이름 · 주소 없음 ·
모르는 이름 · 경로 탈출 거부를 본다.  (일반 회귀 = `webapp/test_worklog_page.py` · 앞 주 = `webapp/test_worklog_weekly_20261101.py`.)

  python3 webapp/test_worklog_weekly_20261109.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

KEY = '20261109'
PREV_KEY = '20261101'
TITLE = '주간 정리 2026-11-02 ~ 11-09'
#: 리포트 본문에 그대로 있어야 하는 숫자 (출처 = git · 원장 — 리포트 실행 요약 표 · 원장 표)
#:  커밋 237 = `git rev-list --count b1161dd02..dc85907c8` · 원장 923 → 1030 (새 107) · 주말 열림 342 · 검증 312
NUMBERS = ('237', '923 → 1030', '107', '342', '312')
#: 절 — 앞 주와 같은 이름 + 집계 창 각주
SECTIONS = ('다음 주', '사용자가 정할 것', '예상 질문', '집계 창', '실행 요약', '한눈에 보기', '용어 풀이')
#: 트랙 절 머리 — 용훈 포메이션 순서 ([Rint ②] 1순위 → [DEM 우선] Ⓐ Ⓑ Ⓒ → 나머지 트랙)
TRACK_HEADS = ('## 1. Rint ②', '## 2. DEM 우선 Ⓐ', '## 3. DEM 우선 Ⓑ', '## 4. DEM 우선 Ⓒ',
               '## 5. LHS', '## 6. 50kg')
#: 트랙 표 머리 (용훈 포메이션 열)
TRACK_TABLE_HEAD = '| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |'
#: 경로 탈출 · 모르는 이름 — 전부 404 여야 한다
BAD_PATHS = (
    '/worklog/20261131',                      # 형식은 맞지만 없는 날짜 (파일 없음)
    '/worklog/weekly_report_20261109',        # 날짜 키가 아닌 이름
    '/worklog/weekly_20261109',
    '/worklog/20261109.md',
    '/worklog/2026-11-09',
    '/worklog/..%2F..%2FCLAUDE.md',
    '/worklog/%2e%2e%2f%2e%2e%2fCLAUDE.md',
    '/worklog/..%2f..%2fwebapp%2fapp.py',
    '/worklog/20261109%2F..%2F..%2FCLAUDE.md',
    '/worklog/../../CLAUDE.md',
    '/worklog/20261109/../../../CLAUDE.md',
    '/worklog/%00',
)
#: 탈출이 성공했다면 보일 글 (CLAUDE.md 첫 줄 · app.py 의 Flask 객체 줄)
LEAK_MARKERS = ('# Project conventions for Claude Code sessions', 'app = Flask(')
#: 모델 이름 · ID (커밋 꼬리 밖에서는 쓰지 않는다)
RE_MODEL = re.compile(r'\b(?:opus|sonnet|haiku)\b|claude-[a-z0-9]', re.I)
#: 주소 · 포트 · user@host (리포에 적지 않는다)
RE_ADDR = re.compile(r'(?<![\d.])\d{1,3}(?:\.\d{1,3}){3}(?![\d.])|\blocalhost\b'
                     r'|(?<![0-9]):\d{4,5}(?![0-9])|\b[\w.-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b')
#: 근거 칸의 백틱 리포 경로 (docs/ · scripts/ · webapp/ 로 시작)
RE_REPO_PATH = re.compile(r'`((?:docs|scripts|webapp)/[^`\s]+)`')

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


def _quotation_ban(repo_root):
    """claims.json 의 인용 금지 패턴 (문자열) — 읽지 못하면 빈 목록이 아니라 None (시험 실패)."""
    try:
        with open(os.path.join(repo_root, 'docs/reviews/claims.json'), encoding='utf-8') as f:
            d = json.load(f)
    except (OSError, ValueError):
        return None
    pats = []
    for q in d.get('quotation_ban') or []:
        p = q.get('pattern') if isinstance(q, dict) else q
        if isinstance(p, str) and p:
            pats.append(p)
    return pats or None


def main():
    import app as webapp
    c = webapp.app.test_client()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ══ 1) 목록 — 이번 주 리포트가 뜬다 ══
    r = c.get('/worklog')
    chk('① /worklog 200', r.status_code == 200)
    html = r.get_data(as_text=True)
    ents = webapp._worklog_entries()
    #  ⚠ "맨 위" 가 아니라 "목록에 있다" 로 본다 — 다음 주 리포트가 들어오면 이 주는 둘째가 된다 (순서는 ⑥ 이 본다)
    me = next((e for e in ents if e.get('key') == KEY), {})
    chk('② 이번 주 (20261109) 가 목록에 있다', me.get('key') == KEY)
    chk('③ 종류 = 주간 리포트 (docs/worklog)', me.get('kind') == '주간 리포트')
    chk('④ 목록 제목 = 리포트 머리 # 줄', me.get('title') == TITLE)
    chk('⑤ 목록에 /worklog/20261109 링크 · 제목', f'/worklog/{KEY}' in html and TITLE in html)
    chk('⑥ 목록 순서 = 날짜 키 내림차순 (앞으로 오는 주차도 자동으로 위에)',
        [e['key'] for e in ents] == sorted((e['key'] for e in ents), reverse=True))
    chk('⑥b 앞 주 (20261101) 도 그대로 목록에 · 이번 주가 그 위',
        any(e.get('key') == PREV_KEY for e in ents)
        and [e['key'] for e in ents].index(KEY) < [e['key'] for e in ents].index(PREV_KEY)
        if me.get('key') == KEY and any(e.get('key') == PREV_KEY for e in ents) else False)

    # ══ 2) 본문 ══
    r2 = c.get(f'/worklog/{KEY}')
    chk('⑦ /worklog/20261109 200', r2.status_code == 200)
    body = r2.get_data(as_text=True)
    chk('⑧ 제목이 본문에', TITLE in body)
    for n in NUMBERS:
        chk(f'⑨ 숫자 {n!r} 가 본문에', n in body)
    for sec in SECTIONS:
        chk(f'⑩ 절 {sec!r} 가 본문에', sec in body)
    chk('⑪ 그림 = 인라인 SVG (<figure> · <svg>)', '<figure' in body and '<svg' in body)
    chk('⑫ 날짜 메타 2026-11-09', '2026-11-09' in body)
    chk('⑫b 렌더 본문에 인용 금지 자리 표시 없음 (redact 가 바꾼 글 0)', '⟨인용금지' not in body)

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

    # ══ 6) 원문 — 렌더가 |safe 라 스크립트 · 이벤트 속성이 없어야 한다 · 금지값 · 모델 이름 · 주소 없음 ══
    src_path = os.path.join(webapp._repo_path('docs/worklog'), f'weekly_{KEY}.md')
    src = ''
    if os.path.isfile(src_path):
        with open(src_path, encoding='utf-8') as f:
            src = f.read()
    chk('⑳ 원문 파일 있음', bool(src))
    chk('㉑ 원문에 <script · javascript: · 태그 안 on*= 속성 없음',
        bool(src) and not re.search(r'<\s*script|javascript:|<[a-z][^<>\n]*\son[a-z]+\s*=', src, re.I))

    #  트랙 순서 — 용훈 포메이션 ([Rint ②] → [DEM 우선] Ⓐ Ⓑ Ⓒ → 나머지)
    pos = [src.find(h) for h in TRACK_HEADS]
    chk('㉒ 트랙 절 머리 여섯이 다 있다', bool(src) and all(p >= 0 for p in pos))
    chk('㉓ 트랙 절 순서 = Rint ② → Ⓐ → Ⓑ → Ⓒ → LHS → 50kg',
        bool(src) and all(p >= 0 for p in pos) and pos == sorted(pos))
    chk('㉔ 트랙 표 머리 (항목 | 상태 | 근거 | 다음 / 사용자 결정) ≥ 6',
        src.count(TRACK_TABLE_HEAD) >= 6)

    bans = _quotation_ban(repo_root)
    chk('㉕ claims.json 인용 금지 패턴을 읽었다', bans is not None)
    hits = [p for p in (bans or []) if p in src]
    chk(f'㉖ 원문에 인용 금지 패턴 없음 (등록 {len(bans or [])} · 걸림 {hits!r})', bool(src) and not hits)
    chk('㉗ 원문에 모델 이름 · ID 없음', bool(src) and not RE_MODEL.search(src))
    m_addr = RE_ADDR.search(src) if src else None
    chk(f'㉘ 원문에 주소 · 포트 · user@host 없음 ({m_addr.group(0) if m_addr else "-"})',
        bool(src) and m_addr is None)
    missing = sorted({p for p in RE_REPO_PATH.findall(src)
                      if not os.path.exists(os.path.join(repo_root, p.rstrip('/')))})
    chk(f'㉙ 백틱 리포 경로 전부 실재 (없음 {missing!r})', bool(src) and not missing)

    print(f'worklog weekly 20261109 SELFTEST {_ok}/{_ok + len(_fail)}',
          'PASS' if not _fail else 'FAIL ' + repr(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
