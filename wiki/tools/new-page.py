#!/usr/bin/env python3
"""Scaffold a new wiki page with correct frontmatter (SCHEMA.md).

Usage:
  python3 tools/new-page.py <type> <slug> [--title "Display Title"]

  type: concept | entity | comparison | query | guide | research-question | synthesis
  slug: lowercase-hyphens (becomes the filename and [[wikilink]] target)

Creates the file with today's dates, explored: false, verificationStatus:
unverified, and a body skeleton for the type. Refuses to overwrite.
Reminds you of the SCHEMA follow-ups (index/log/links).
"""
import argparse, datetime, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
FOLDER = {'concept': 'concepts', 'entity': 'entities', 'comparison': 'comparisons',
          'query': 'queries', 'guide': 'guides',
          'research-question': 'questions', 'synthesis': 'syntheses'}

# type-specific frontmatter lines (SCHEMA.md 타입별 추가 키)
EXTRA_FM = {
    'research-question': 'status: open\nfeedsInto:\n',
    'synthesis': 'targetVenue:\n',
}

SKELETON = {
    'concept': "## 정의\n\n\n## 왜 중요한가\n\n\n## 이 위키에서의 적용\n\n",
    'entity': "## 개요\n\n\n## 핵심 사실\n\n\n## 이 위키와의 관계\n\n",
    'comparison': "## 비교 이유\n\n\n## 비교표\n\n| 기준 | A | B |\n|---|---|---|\n\n## 결론\n\n\n## 불확실성\n\n",
    'query': "## 질문\n\n\n## 짧은 답\n\n\n## 근거\n\n\n## 다음 행동\n\n",
    'guide': "## 목적\n\n\n## 절차\n\n",
    'research-question': ("> [!question] 질문 한 문장\n>\n\n## 왜 중요한가\n\n\n"
                          "## 가설\n- H1:\n\n## Evidence For\n\n\n## Evidence Against\n\n\n"
                          "## Status Log\n- [YYYY-MM-DD] open —\n"),
    'synthesis': ("## Thesis\n(방어하는 한 문장 주장)\n\n## Argument\n\n\n"
                  "## Counter-arguments\n(경쟁 가설·반론 — 삭제하지 않고 보존)\n\n"
                  "## Gap\n(아직 빈 근거, 추가 조사 지점)\n\n"),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('type', choices=FOLDER)
    ap.add_argument('slug')
    ap.add_argument('--title', default=None)
    ap.add_argument('--model', default='', help='작성 에이전트 모델 ID (사람 작성이면 생략)')
    ap.add_argument('--effort', default='', help='low|medium|high|max')
    args = ap.parse_args()

    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', args.slug):
        sys.exit(f'slug must be lowercase-hyphens: {args.slug!r}')

    path = BASE / FOLDER[args.type] / f'{args.slug}.md'
    if path.exists():
        sys.exit(f'refusing to overwrite existing page: {path}')

    title = args.title or args.slug.replace('-', ' ').title()
    today = datetime.date.today().isoformat()
    prov = ''
    if args.model:
        prov = f'model: {args.model}\neffort: {args.effort or "medium"}\n'
    fm = f"""---
title: {title}
created: {today}
updated: {today}
type: {args.type}
tags: []
sources: []
confidence: medium
explored: false
verificationStatus: unverified
{prov}claimType:
evidenceScope:
{EXTRA_FM.get(args.type, '')}---

# {title}

{SKELETON[args.type]}
## 관련
-
-
"""
    path.write_text(fm)
    print(f'created {path.relative_to(BASE)}')
    print('SCHEMA follow-ups:')
    print('  1. tags 를 SCHEMA.md taxonomy 에서 채우기')
    print('  2. sources 에 근거 raw 파일 경로 넣기')
    print('  3. [[wikilink]] 2개 이상 + 관련 페이지에 역링크')
    print(f'  4. index.md 에 [[{args.slug}]] 등록 (Total pages +1)')
    print(f'  5. log.md 에 `## [{today}] create | {title}` append')
    print('  6. python3 tools/lint.py')

if __name__ == '__main__':
    main()
