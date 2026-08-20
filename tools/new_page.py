#!/usr/bin/env python3
"""위키 페이지 스캐폴더.  사용: python3 tools/new_page.py <type> <slug>"""

from __future__ import annotations

import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DIR_BY_TYPE = {"concept": "concepts", "entity": "entities",
               "comparison": "comparisons", "query": "queries",
               "guide": "guides", "research-question": "questions",
               "synthesis": "syntheses"}

TEMPLATE = """---
title: {title}
created: {today}
updated: {today}
type: {page_type}
tags: []
sources: []
confidence: low
explored: false
verificationStatus: unverified
---

# {title}

<!-- 한 문단으로 요약. 그다음 근거. -->

## 관련

- [[]]
- [[]]
"""


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] not in DIR_BY_TYPE:
        print(f"사용: new_page.py <{' | '.join(DIR_BY_TYPE)}> <slug>", file=sys.stderr)
        return 1
    page_type, slug = argv
    path = DOCS / DIR_BY_TYPE[page_type] / f"{slug}.md"
    if path.exists():
        print(f"이미 있음: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    path.write_text(TEMPLATE.format(
        title=slug.replace("-", " "), today=today, page_type=page_type))
    print(f"생성: {path.relative_to(ROOT)}")
    print("다음: docs/index.md 에 등재하고 docs/log.md 에 한 줄 남기세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
