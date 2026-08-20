#!/usr/bin/env python3
"""docs/ 정합성 검사 — 의존성 0, python3 만 있으면 된다.

검사 항목
  1. CLAUDE.md / AGENTS.md parity (제목 줄과 미러 문장만 다를 것)
  2. ADR: 번호 중복 없음, 상태와 날짜 존재, index 에 등재
  3. docs/index.md 가 모든 문서를 나열하고, 없는 문서를 나열하지 않음
  4. docs/log.md 가 append-only 형식(`## [YYYY-MM-DD] action | subject`)
  5. 위키 페이지 frontmatter 필수 키
  6. [[wikilink]] 가 실재하는 페이지를 가리킴

사용: python3 tools/wiki_lint.py     (오류 0 이면 exit 0)
"""

from __future__ import annotations

import difflib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
WIKI_DIRS = ["concepts", "entities", "comparisons", "queries", "guides",
             "questions", "syntheses"]
REQUIRED_FRONTMATTER = ["title", "created", "updated", "type", "tags",
                        "sources", "confidence", "explored", "verificationStatus"]
TYPE_BY_DIR = {"concepts": "concept", "entities": "entity",
               "comparisons": "comparison", "queries": "query",
               "guides": "guide", "questions": "research-question",
               "syntheses": "synthesis"}
LOG_PATTERN = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] [a-z-]+ \| .+")

errors: list[str] = []
warnings: list[str] = []


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        entry = re.match(r"^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$", line)
        if entry:
            fields[entry.group(1)] = entry.group(2).strip()
    return fields


def check_parity() -> None:
    claude = (ROOT / "CLAUDE.md").read_text().splitlines()
    agents_path = ROOT / "AGENTS.md"
    if not agents_path.exists():
        errors.append("AGENTS.md 없음 (CLAUDE.md 의 미러여야 함)")
        return
    agents = agents_path.read_text().splitlines()

    diff = [
        line for line in difflib.unified_diff(claude, agents, lineterm="", n=0)
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
    ]
    # 제목 줄과 Parity Contract 문장만 달라야 한다.
    allowed = re.compile(r"^[+-](# (CLAUDE|AGENTS)\.md —|`(CLAUDE|AGENTS)\.md` 와)")
    unexpected = [line for line in diff if not allowed.match(line)]
    if unexpected:
        errors.append(
            f"CLAUDE.md / AGENTS.md parity 깨짐 ({len(unexpected)}줄): "
            + unexpected[0][:80]
        )


def check_adrs() -> tuple[list[pathlib.Path], set[str]]:
    adr_dir = DOCS / "adr"
    files = sorted(adr_dir.glob("*.md")) if adr_dir.exists() else []
    seen: dict[str, pathlib.Path] = {}
    for path in files:
        number = path.name.split("-", 1)[0]
        if not number.isdigit():
            errors.append(f"{path.name}: ADR 파일명이 번호로 시작하지 않음")
            continue
        if number in seen:
            errors.append(f"ADR 번호 {number} 중복: {seen[number].name}, {path.name}")
        seen[number] = path

        text = path.read_text()
        if not re.search(r"^- 상태: .+ \(\d{4}-\d{2}-\d{2}\)", text, re.M):
            errors.append(f"{path.name}: `- 상태: <상태> (YYYY-MM-DD)` 줄이 없음")
        if "## 결정" not in text:
            errors.append(f"{path.name}: `## 결정` 절이 없음")
        if "## 결과" not in text:
            warnings.append(f"{path.name}: `## 결과` 절이 없음 (권장)")
    return files, set(seen)


def check_wiki_pages() -> dict[str, pathlib.Path]:
    pages: dict[str, pathlib.Path] = {}
    for directory in WIKI_DIRS:
        for path in sorted((DOCS / directory).glob("*.md")):
            pages[path.stem] = path

    for stem, path in pages.items():
        text = path.read_text()
        fields = parse_frontmatter(text)
        if fields is None:
            errors.append(f"{path.name}: frontmatter 없음")
            continue
        for key in REQUIRED_FRONTMATTER:
            if key not in fields:
                errors.append(f"{path.name}: frontmatter 키 `{key}` 누락")
        expected = TYPE_BY_DIR[path.parent.name]
        if fields.get("type") != expected:
            errors.append(
                f"{path.name}: type `{fields.get('type')}` (폴더는 {expected} 를 기대)")
        if fields.get("verificationStatus") == "verified" and not fields.get("verifiedAt"):
            errors.append(f"{path.name}: verified 인데 verifiedAt 없음")

        body = re.sub(r"```.*?```", "", text, flags=re.S)
        body = re.sub(r"`[^`\n]*`", "", body)
        links = re.findall(r"\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]", body)
        for link in links:
            if link.strip() not in pages:
                errors.append(f"{path.name}: 깨진 wikilink [[{link}]]")
        if len(set(links)) < 2:
            warnings.append(f"{path.name}: 서로 다른 wikilink 가 2개 미만")
    return pages


def check_index(adr_files: list[pathlib.Path], pages: dict[str, pathlib.Path]) -> None:
    index_path = DOCS / "index.md"
    if not index_path.exists():
        errors.append("docs/index.md 없음")
        return
    index = index_path.read_text()
    # 부분 문자열 검사는 등재를 흉내낸다: 미등재 `wsl.md` 가 기존 `wsl-setup`
    # 항목 안에 묻혀 통과한다. 이름 경계와 [[wikilink]] 로만 등재를 인정한다.
    for path in adr_files:
        if not re.search(rf"(?<![\w-]){re.escape(path.name)}(?![\w-])", index):
            errors.append(f"docs/index.md: ADR 미등재 {path.name}")
    index_links = set(re.findall(r"\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]", index))
    index_links = {link.strip() for link in index_links}
    for stem in pages:
        if stem not in index_links:
            errors.append(f"docs/index.md: 위키 페이지 미등재 {stem}")

    for link in index_links:
        if link not in pages:
            errors.append(f"docs/index.md: 없는 페이지를 나열 [[{link}]]")


def check_log() -> None:
    log_path = DOCS / "log.md"
    if not log_path.exists():
        errors.append("docs/log.md 없음")
        return
    entries = [line for line in log_path.read_text().splitlines()
               if line.startswith("## ")]
    bad = [line for line in entries if not LOG_PATTERN.match(line)]
    for line in bad[:5]:
        errors.append(f"docs/log.md: 형식 위반 `{line[:60]}` "
                      "(`## [YYYY-MM-DD] action | subject`)")
    dates = [re.match(r"^## \[(\d{4}-\d{2}-\d{2})\]", line).group(1)
             for line in entries if LOG_PATTERN.match(line)]
    if dates != sorted(dates):
        warnings.append("docs/log.md: 날짜가 오름차순이 아님 (append-only 위반 가능)")


def check_spec_reachable() -> None:
    spec = DOCS / "raw/specs/wrd-binary-format.md"
    if not spec.exists():
        errors.append("docs/raw/specs/wrd-binary-format.md 없음 — 파서의 근거 문서")


def main() -> int:
    check_parity()
    adr_files, _ = check_adrs()
    pages = check_wiki_pages()
    check_index(adr_files, pages)
    check_log()
    check_spec_reachable()

    print("=== DOCS LINT ===")
    print(f"ADR {len(adr_files)}건 | 위키 페이지 {len(pages)}건")
    print(f"\n오류 ({len(errors)}):")
    for message in errors:
        print("  x", message)
    print(f"\n경고 ({len(warnings)}):")
    for message in warnings:
        print("  !", message)
    if not errors:
        print("\n결과: 오류 0")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
