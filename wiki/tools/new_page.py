#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""새 위키 페이지 스캐폴더 (wiki/SCHEMA.md frontmatter).

사용: python3 wiki/tools/new_page.py <type> <slug> [--title "제목"] [--author agent|human|both]
타입: concept | entity | comparison | query | guide | research-question | synthesis

오늘 날짜 + explored: false + verificationStatus: unverified 로 만들고 덮어쓰기 거부.
★ 킷과 달리 model/effort 를 받지 않는다 (리포 모델-ID 금지 규칙 — author 만).
만든 뒤 해야 할 것을 상기시킨다: index.md 등록 · log.md append · [[링크]] 2개 · lint.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
FOLDER = {'concept': 'concepts', 'entity': 'entities', 'comparison': 'comparisons',
          'query': 'queries', 'guide': 'guides',
          'research-question': 'questions', 'synthesis': 'syntheses'}
EXTRA_FM = {'research-question': 'status: open\nfeedsInto:\n', 'synthesis': 'targetVenue:\n'}
SKELETON = {
    'concept': '## 정의\n\n\n## 왜 중요한가\n\n\n## 이 리포에서의 위치\n\n',
    'entity': '## 개요\n\n\n## 핵심 사실\n\n\n## 관련 페이지·경로\n\n',
    'comparison': '## 비교 이유\n\n\n## 비교표\n\n| 기준 | A | B |\n|---|---|---|\n\n## 결론\n\n\n## 불확실성\n\n',
    'query': '## 질문\n\n\n## 짧은 답\n\n\n## 근거\n\n\n## 다음 행동\n\n',
    'guide': '## 목적\n\n\n## 절차\n\n',
    'research-question': ('> [!question] 질문 한 문장\n\n## 왜 중요한가\n\n\n## 가설\n- H1:\n\n'
                          '## Evidence For\n\n\n## Evidence Against\n\n\n## Status Log\n- [YYYY-MM-DD] open —\n'),
    'synthesis': ('## Thesis\n(방어하는 한 문장)\n\n## Argument\n\n\n'
                  '## Counter-arguments\n(반론 보존 — 삭제 금지)\n\n## Gap\n\n'),
}


def render(ptype, slug, title, author, today):
    return (f'---\ntitle: {title}\ncreated: {today}\nupdated: {today}\ntype: {ptype}\n'
            f'tags: []\nsources: []\nconfidence: low\nexplored: false\n'
            f'verificationStatus: unverified\nauthor: {author}\nclaimType: mixed\n'
            f'evidenceScope: single-source\nanchored: n-a\nscope: n-a\n'
            f'{EXTRA_FM.get(ptype, "")}---\n\n# {title}\n\n{SKELETON[ptype]}')


def create(ptype, slug, title=None, author='agent', base=BASE, today=None):
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', slug):
        raise SystemExit(f'ABORT — slug 형식 위반: {slug!r} (lowercase-hyphens)')
    today = today or datetime.date.today().isoformat()
    path = base / FOLDER[ptype] / f'{slug}.md'
    if path.exists():
        raise SystemExit(f'ABORT — 이미 있음: {path} (덮어쓰기 거부)')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(ptype, slug, title or slug, author, today), encoding='utf-8')
    return path


def _selftest():
    import shutil
    import tempfile
    ok = fail = 0

    def chk(msg, cond):
        nonlocal ok, fail
        print(('  PASS  ' if cond else '  FAIL  ') + msg)
        ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)

    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        p = create('concept', 'test-slug', base=tmp, today='2026-08-11')
        t = p.read_text(encoding='utf-8')
        chk('1) 생성 + 폴더 규약', p.parent.name == 'concepts')
        chk('2) 필수 키 전부', all(k + ':' in t for k in
            ('title', 'created', 'updated', 'type', 'tags', 'sources', 'confidence',
             'explored', 'verificationStatus', 'author', 'claimType', 'evidenceScope')))
        chk('3) ★ model/effort 키 없음', 'model:' not in t and 'effort:' not in t)
        chk('4) 새 페이지 = unverified + explored false',
            'verificationStatus: unverified' in t and 'explored: false' in t)
        try:
            create('concept', 'test-slug', base=tmp)
            chk('5) 덮어쓰기 거부', False)
        except SystemExit:
            chk('5) 덮어쓰기 거부', True)
        try:
            create('concept', 'Bad_Slug', base=tmp)
            chk('6) slug 검증', False)
        except SystemExit:
            chk('6) slug 검증', True)
        rq = create('research-question', 'rq-x', base=tmp).read_text(encoding='utf-8')
        chk('7) RQ = status/feedsInto + Status Log', 'status: open' in rq and 'Status Log' in rq)
        sy = create('synthesis', 'sy-x', base=tmp).read_text(encoding='utf-8')
        chk('8) synthesis = targetVenue + Counter-arguments',
            'targetVenue:' in sy and 'Counter-arguments' in sy)
        # lint 와의 정합: 방금 만든 페이지가 lint frontmatter 검사를 통과하는가
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import lint as L
        fm = L.parse_fm(t.split('---')[1])
        chk('9) ★ lint REQ 와 정합', all(k in fm for k in L.REQ))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\nnew_page selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('type', nargs='?', choices=sorted(FOLDER))
    ap.add_argument('slug', nargs='?')
    ap.add_argument('--title')
    ap.add_argument('--author', default='agent', choices=('agent', 'human', 'both'))
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.type or not a.slug:
        ap.error('type 과 slug 필요 (또는 --selftest)')
    p = create(a.type, a.slug, a.title, a.author)
    print(f'created → {p.relative_to(BASE.parent)}')
    print('다음: ① 본문 채우기 (sources·[[링크]]≥2) ② index.md 등록 ③ log.md append '
          '④ python3 wiki/tools/lint.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
