#!/usr/bin/env python3
"""저장소 스냅샷 — 문서, 코드, 데이터 현황을 한 화면에."""

from __future__ import annotations

import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent


def count(pattern: str, root: pathlib.Path) -> int:
    return sum(1 for _ in root.rglob(pattern)) if root.exists() else 0


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, check=False).stdout.strip()
    except OSError:
        return ""


def main() -> int:
    print("=== 저장소 스냅샷 ===\n")

    adrs = sorted((ROOT / "docs/adr").glob("*.md"))
    print(f"ADR            {len(adrs)}건")
    for path in adrs:
        title = path.read_text().splitlines()[0].lstrip("# ").strip()
        status = re.search(r"^- 상태: ([^(]+)", path.read_text(), re.M)
        print(f"  {title}  [{status.group(1).strip() if status else '?'}]")

    wiki = sum(count("*.md", ROOT / "docs" / d) for d in
               ("concepts", "entities", "comparisons", "queries", "guides",
                "questions", "syntheses"))
    print(f"\n위키 페이지     {wiki}건")
    print(f"스펙 문서       {count('*.md', ROOT / 'docs/raw/specs')}건")

    print(f"\nwrdkit 모듈     {count('*.py', ROOT / 'packages/wrdkit/src')}개")
    print(f"wrdkit 테스트   {count('test_*.py', ROOT / 'packages/wrdkit/tests')}개")
    print(f"API 모듈        {count('*.py', ROOT / 'apps/api/app')}개")
    print(f"web 소스        {count('*.ts*', ROOT / 'apps/web/src')}개")

    uploads = ROOT / "data/uploads"
    runs = ROOT / "data/runs"
    print(f"\n업로드 원본     {count('*.wrd', uploads)}개")
    print(f"파싱 캐시       {sum(1 for _ in runs.iterdir() if _.is_dir()) if runs.exists() else 0}개")

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    dirty = git("status", "--porcelain")
    ahead = git("rev-list", "--count", "@{upstream}..HEAD") or "?"
    behind = git("rev-list", "--count", "HEAD..@{upstream}") or "?"
    print(f"\n브랜치          {branch}")
    print(f"미커밋 변경     {len(dirty.splitlines()) if dirty else 0}개")
    print(f"업스트림 대비   ahead {ahead} / behind {behind}")
    if behind not in ("0", "?"):
        print("  -> 'make sync' 를 먼저 실행하세요.")
    print("\n최근 커밋")
    for line in git("log", "--oneline", "-5").splitlines():
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
