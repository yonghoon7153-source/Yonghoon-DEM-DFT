"""62차 η′ (P2-2) — **계약이 인용하는 이름은 실재해야 한다.**

리뷰어: `STAGE3_CONTRACT.md:1077` 이 `row_projection.py` 의 `_canon_*` 을
인용하지만 그런 이름은 없다 (실제는 `_keep_docstrings()` → `_ast_normal_node()`
→ `_ast_canon()`). 그리고 `_ast_normal_node` 의 docstring 은 "`ast.unparse` 로
찍는다" 고 적었지만 실제 렌더링은 `_ast_canon()` 이 직접 한다 (48차 P0-2 가
`ast.unparse` 의 버전 의존을 이유로 **버린** 방식이다).

61차 P2 정정이 "문서도 실측 대상" 이라 적어 놓고 같은 문단에서 없는 이름을
인용했다. 그래서 lint 를 둔다: 계약 본문에서 `row_projection.py` 와 같은 줄에
백틱으로 인용된 `_이름` 은 전부 그 module 의 실제 정의여야 하고, `*` 같은
glob 은 인용이 아니다.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_CONTRACT = REPO / "docs" / "22p_gap" / "STAGE3_CONTRACT.md"
_RP = REPO / "docs" / "22p_gap" / "row_projection.py"


def _module_level_names(path: Path) -> set:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set = set()
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(n.name)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    out.add(t.id)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            out.add(n.target.id)
    return out


def _cited_identifiers(doc: str) -> list:
    """`row_projection.py` 를 말하는 줄에서 백틱 인용된 `_이름` 전부 (줄번호와)."""
    out = []
    for i, line in enumerate(doc.splitlines(), 1):
        if "row_projection.py" not in line:
            continue
        for m in re.finditer(r"`(_[A-Za-z0-9_*]+)(?:\(\))?`", line):
            out.append((i, m.group(1)))
    return out


def test_contract_citations_of_row_projection_resolve():
    doc = _CONTRACT.read_text(encoding="utf-8")
    names = _module_level_names(_RP)
    cited = _cited_identifiers(doc)
    assert cited, "계약이 row_projection.py 의 이름을 하나도 인용하지 않는다 — lint 전제가 깨졌다"
    bad = [(ln, nm) for ln, nm in cited if "*" in nm or nm not in names]
    assert not bad, (
        f"계약이 row_projection.py 에 없는 이름을 인용한다: {bad} (62차 P2-2)")


def test_the_normal_form_docstring_does_not_claim_ast_unparse():
    """`_ast_normal_node` 의 docstring 이 실제 렌더러(`_ast_canon`)를 말해야 한다."""
    import sys

    if str(REPO / "docs" / "22p_gap") not in sys.path:
        sys.path.insert(0, str(REPO / "docs" / "22p_gap"))
    import row_projection as rp

    doc = rp._ast_normal_node.__doc__ or ""
    assert "`ast.unparse` 로 찍는다" not in doc, (
        "_ast_normal_node 의 docstring 이 아직 ast.unparse 로 찍는다고 적는다 "
        "(62차 P2-2)")
    assert "_ast_canon" in doc, "docstring 이 실제 렌더러 `_ast_canon` 을 말하지 않는다"
