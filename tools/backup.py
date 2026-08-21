#!/usr/bin/env python3
"""Copy the parts of ``data/`` that cannot be recreated.

Two of the three things in there are irreplaceable and one is not:

* ``uploads/`` — the original ``.wrd`` files.  Irreplaceable, and the reason
  this script exists.  A file lost here is a measurement lost.
* ``workbench.db`` — every mass, composition, group and preset anybody typed.
  Small, and hours of work.
* ``runs/`` — the parsed-column cache.  **Skipped.**  It rebuilds itself from
  the originals (ADR 0003) and it is the bulk of the directory; copying it
  would multiply the time and the space for something the app throws away on
  its own when it looks doubtful.

The database is copied through SQLite's own backup API, not as a file.  A live
SQLite database has pages in flight, and ``cp`` of one while the server is
writing produces a copy that opens without complaint and is missing rows --
the worst possible failure for a backup, because it looks like it worked.

Uploads are content-addressed by SHA-256 (CLAUDE.md §0.2), so a name that is
already at the destination holds the same bytes by construction.  Skipping
those makes the second and every later backup cheap, which is what makes it
something you will actually run.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "packages/wrdkit/src"))
sys.path.insert(0, str(REPO / "apps/api"))


@dataclass
class Report:
    """What a run of the backup actually did."""

    destination: Path
    copied: int = 0
    skipped: int = 0
    copied_bytes: int = 0
    database: str = ""
    problems: list[str] = field(default_factory=list)

    def lines(self) -> list[str]:
        out = [f"대상        {self.destination}"]
        if self.database:
            out.append(f"데이터베이스 {self.database}")
        out.append(
            f"원본 .wrd   새로 {self.copied}개 ({_human(self.copied_bytes)})"
            f" · 이미 있던 것 {self.skipped}개"
        )
        out.extend(f"! {problem}" for problem in self.problems)
        return out


def _human(size: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def backup_database(source: Path, destination: Path) -> str:
    """Copy a SQLite file safely, even with the server writing to it."""
    if not source.exists():
        return "없음 (아직 아무것도 저장하지 않았습니다)"
    destination.parent.mkdir(parents=True, exist_ok=True)
    # `file:...?mode=ro` so a backup can never be the thing that creates or
    # migrates a database; a typo in the path should come back empty-handed
    # rather than leave a new empty file behind.
    with sqlite3.connect(f"file:{source}?mode=ro", uri=True) as live, \
            sqlite3.connect(destination) as copy:
        live.backup(copy)
    return f"{_human(destination.stat().st_size)} → {destination.name}"


def backup_uploads(source: Path, destination: Path, report: Report) -> None:
    """Copy every original that is not already at the destination."""
    if not source.is_dir():
        report.problems.append(f"업로드 폴더가 없습니다: {source}")
        return
    destination.mkdir(parents=True, exist_ok=True)
    for item in sorted(source.glob("*.wrd")):
        target = destination / item.name
        size = item.stat().st_size
        # Same name means same bytes -- the name *is* the hash.  A size
        # mismatch can then only be a half-finished earlier copy, so it is
        # rewritten rather than trusted.
        if target.exists() and target.stat().st_size == size:
            report.skipped += 1
            continue
        temporary = target.with_suffix(".wrd.part")
        try:
            shutil.copy2(item, temporary)
            os.replace(temporary, target)
        except OSError as cause:
            temporary.unlink(missing_ok=True)
            report.problems.append(f"{item.name}: {cause}")
            continue
        report.copied += 1
        report.copied_bytes += size


def run(destination: Path, data_dir: Path, database: Path) -> Report:
    report = Report(destination=destination)
    destination.mkdir(parents=True, exist_ok=True)
    report.database = backup_database(database, destination / "workbench.db")
    backup_uploads(data_dir / "uploads", destination / "uploads", report)
    return report


def _locations() -> tuple[Path, Path]:
    """Where the workbench keeps its data, according to the app itself.

    Read from `settings` rather than rebuilt here, so `WORKBENCH_DATA` and
    `WORKBENCH_DB` cannot mean one thing to the server and another to its
    backup -- which would back up an empty directory and report success.
    """
    from app.settings import settings  # noqa: PLC0415 -- needs sys.path above

    url = settings.database_url
    database = Path(url[len("sqlite:///"):]) if url.startswith("sqlite:///") \
        else settings.data_dir / "workbench.db"
    return settings.data_dir, database


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path,
                        help="복사해 둘 폴더 (예: /mnt/e/bml-backup)")
    arguments = parser.parse_args(argv)

    data_dir, database = _locations()
    if not data_dir.is_dir():
        print(f"데이터 폴더가 없습니다: {data_dir}", file=sys.stderr)
        return 1
    destination = arguments.destination.expanduser().resolve()
    if destination == data_dir.resolve():
        print("원본과 같은 폴더입니다.", file=sys.stderr)
        return 1

    print(f"출처        {data_dir}")
    report = run(destination, data_dir, database)
    for line in report.lines():
        print(line)
    return 1 if report.problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
