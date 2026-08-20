#!/usr/bin/env python3
"""tools/wiki_lint.py 회귀 테스트 — 의존성 0, python3 만 있으면 된다.

검사 대상은 index 등재 판정이다. 예전 구현은 index.md 전체 텍스트에 대한
부분 문자열 검사라, 미등재 페이지의 stem 이 다른 항목 안에 우연히 들어 있기만
하면(`wsl` ⊂ `wsl-setup`) 통과했다.

트리를 통째로 임시 폴더에 복사해서 돌린다 — 작업 트리에 흔적을 남기지 않고,
다른 사람이 동시에 편집 중이어도 서로를 건드리지 않는다.

사용: python3 tools/tests/test_wiki_lint.py     (실패 0 이면 exit 0)
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

PAGE = """---
title: temp page
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [tooling]
sources: []
confidence: low
explored: false
verificationStatus: unverified
---

# 임시

[[bml-command]] 와 [[wsl-setup]] 참조.
"""

ADR = """# ADR 0010 — 임시

- 상태: 채택 (2026-08-20)

## 결정

임시.

## 결과

임시.
"""


def _run(tree: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(tree / "tools/wiki_lint.py")],
        capture_output=True, text=True,
    )


def _fixture(base: str) -> pathlib.Path:
    tree = pathlib.Path(base) / "repo"
    (tree / "tools").mkdir(parents=True)
    shutil.copy(ROOT / "tools/wiki_lint.py", tree / "tools/wiki_lint.py")
    shutil.copytree(ROOT / "docs", tree / "docs")
    shutil.copy(ROOT / "CLAUDE.md", tree / "CLAUDE.md")
    shutil.copy(ROOT / "AGENTS.md", tree / "AGENTS.md")
    return tree


def check_clean_tree_passes() -> list[str]:
    with tempfile.TemporaryDirectory() as base:
        tree = _fixture(base)
        result = _run(tree)
        if result.returncode != 0:
            return [f"복사한 트리에서 lint 가 실패함: {result.stdout[-400:]}"]
    return []


def check_unregistered_page_is_caught() -> list[str]:
    """stem 이 기존 항목의 부분 문자열인 미등재 페이지 (`wsl` ⊂ `wsl-setup`)."""
    with tempfile.TemporaryDirectory() as base:
        tree = _fixture(base)
        (tree / "docs/guides/wsl.md").write_text(PAGE)
        result = _run(tree)
        if result.returncode == 0:
            return ["미등재 위키 페이지 `wsl` 를 lint 가 통과시킴"]
        if "미등재 wsl" not in result.stdout:
            return [f"미등재 오류 메시지가 없음: {result.stdout[-400:]}"]
    return []


def check_unregistered_adr_is_caught() -> list[str]:
    """파일명이 index 의 다른 토큰 안에 부분 문자열로만 들어 있는 ADR."""
    with tempfile.TemporaryDirectory() as base:
        tree = _fixture(base)
        (tree / "docs/adr/0010-temp.md").write_text(ADR)
        index = tree / "docs/index.md"
        index.write_text(index.read_text() + "\n<!-- x0010-temp.mdx -->\n")
        result = _run(tree)
        if result.returncode == 0:
            return ["미등재 ADR `0010-temp.md` 를 lint 가 통과시킴"]
        if "ADR 미등재 0010-temp.md" not in result.stdout:
            return [f"ADR 미등재 오류 메시지가 없음: {result.stdout[-400:]}"]
    return []


def check_registered_adr_passes() -> list[str]:
    """등재된 ADR 은 경로 접두사(`adr/`)가 붙어도 인정해야 한다."""
    with tempfile.TemporaryDirectory() as base:
        tree = _fixture(base)
        (tree / "docs/adr/0010-temp.md").write_text(ADR)
        index = tree / "docs/index.md"
        index.write_text(index.read_text() + "\n- [0010](adr/0010-temp.md)\n")
        result = _run(tree)
        if "0010-temp.md" in result.stdout and "미등재" in result.stdout:
            return [f"등재된 ADR 을 미등재로 오판함: {result.stdout[-400:]}"]
    return []


def main() -> int:
    failures: list[str] = []
    for check in (check_clean_tree_passes,
                  check_unregistered_page_is_caught,
                  check_unregistered_adr_is_caught,
                  check_registered_adr_passes):
        found = check()
        if found:
            failures.extend(f"{check.__name__}: {message}" for message in found)
        print(("  ok " if not found else "  x  ") + check.__name__)

    print(f"\n=== WIKI LINT REGRESSION === 실패 {len(failures)}")
    for message in failures:
        print("  x", message)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
