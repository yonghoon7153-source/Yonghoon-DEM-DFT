#!/usr/bin/env python3
"""style.css 에 셀렉터 없는 고아 선언이 남았는지 검사 (ux-1 재발 방지).

왜 이 검사인가: 고아 선언은 파서 에러를 내지 않는다. CSS Syntax 스펙상 qualified rule 은
첫 '{' 까지를 프렐류드로 삼으므로, 고아 줄 + 뒤따르는 진짜 셀렉터가 통째로 하나의 '유효한
qualified-rule + 쓰레기 프렐류드' 로 파싱되고 그 규칙 전체가 조용히 drop 된다.
그래서 `r.type == 'error'` 검사는 0건을 반환한다 — 프렐류드에 '{', '}', ';' 가 섞였는지를 봐야 한다.

실제로 이 검사가 잡았던 것: .pt-legend .lg-off 뒤의 고아 2줄이 .exp-controls 규칙을 삼켜
Property Explorer 컨트롤바가 flex/gap 을 잃고 세로로 쌓이던 문제.

    python3 tools/check_css_orphans.py     # 0 = clean, 1 = 고아 발견
"""
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parents[1] / "webapp" / "static" / "css" / "style.css"


def main() -> int:
    try:
        import tinycss2
    except ImportError:
        print("SKIP: tinycss2 미설치 (pip install tinycss2)")
        return 0
    css = CSS.read_text(encoding="utf-8")
    rules = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
    bad = [r for r in rules
           if r.type == "qualified-rule"
           and any(ch in tinycss2.serialize(r.prelude) for ch in "{};")]
    for r in bad:
        prelude = tinycss2.serialize(r.prelude).strip().replace("\n", " ")[:160]
        print(f"ORPHAN at line {r.source_line}: prelude contains {{ }} or ; → 규칙이 통째로 drop 됨")
        print(f"  prelude: {prelude}")
    if bad:
        print(f"\n{len(bad)}건 — 셀렉터 없는 선언 줄을 삭제하세요.")
        return 1
    print(f"OK: {len(rules)} rules, 고아 선언 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
