#!/usr/bin/env python3
"""tools/backup.py 회귀 테스트 — 의존성 0, python3 만 있으면 된다.

백업이 조용히 실패하는 방식들을 못 박는다. 백업은 되돌아볼 일이 생겼을 때에야
틀린 것을 알게 되는 물건이라, "돌긴 돌았다" 는 아무 보증이 되지 않는다.

사용: python3 tools/tests/test_backup.py     (실패 0 이면 exit 0)
"""

from __future__ import annotations

import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from backup import Report, backup_database, backup_uploads, run  # noqa: E402

passed = 0
failed = 0


def check(what: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  ok   {what}")
    else:
        failed += 1
        print(f"  FAIL {what}" + (f"\n       {detail}" if detail else ""))


def _data_dir(root: Path, *names: str) -> Path:
    """A data directory with some originals and a database in it."""
    uploads = root / "uploads"
    uploads.mkdir(parents=True)
    for index, name in enumerate(names):
        (uploads / f"{name}.wrd").write_bytes(b"WRD" + bytes([index]) * 100)
    # The parse cache: bulky, rebuildable, and deliberately not backed up.
    runs = root / "runs" / "1"
    runs.mkdir(parents=True)
    (runs / "columns.npz").write_bytes(b"x" * 5000)
    database = root / "workbench.db"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE sample (id INTEGER, name TEXT)")
        connection.execute("INSERT INTO sample VALUES (1, 'No_1_dry')")
    return database


def check_originals_and_database_are_copied() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        data, destination = root / "data", root / "backup"
        database = _data_dir(data, "aaa", "bbb")

        report = run(destination, data, database)

        check("원본 .wrd 를 그대로 복사한다",
              (destination / "uploads/aaa.wrd").read_bytes()
              == (data / "uploads/aaa.wrd").read_bytes())
        check("두 개 다 복사했다고 센다", report.copied == 2, f"copied={report.copied}")

        with sqlite3.connect(destination / "workbench.db") as copy:
            rows = copy.execute("SELECT name FROM sample").fetchall()
        check("데이터베이스 내용이 살아 있다", rows == [("No_1_dry",)], f"{rows}")

        # 파싱 캐시는 원본에서 다시 만들어진다 (ADR 0003).  용량의 대부분이라
        # 같이 복사하면 백업이 몇 배 느려지고, 얻는 것이 없다.
        check("파싱 캐시는 복사하지 않는다", not (destination / "runs").exists())


def check_second_run_skips_what_is_already_there() -> None:
    """이름이 곧 해시라, 같은 이름이면 같은 바이트다.

    두 번째 백업이 싸야 사람이 실제로 돌린다.
    """
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        data, destination = root / "data", root / "backup"
        database = _data_dir(data, "aaa", "bbb")

        run(destination, data, database)
        again = run(destination, data, database)

        check("두 번째는 아무것도 새로 안 쓴다", again.copied == 0)
        check("건너뛴 것을 센다", again.skipped == 2, f"skipped={again.skipped}")


def check_a_half_copied_file_is_rewritten() -> None:
    """크기가 다르면 앞선 복사가 중간에 끊긴 것이다 — 믿지 않고 다시 쓴다."""
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        data, destination = root / "data", root / "backup"
        database = _data_dir(data, "aaa")
        run(destination, data, database)
        (destination / "uploads/aaa.wrd").write_bytes(b"WR")  # 잘린 복사본

        again = run(destination, data, database)

        check("잘린 복사본은 다시 쓴다", again.copied == 1)
        check("내용이 원본과 같아진다",
              (destination / "uploads/aaa.wrd").read_bytes()
              == (data / "uploads/aaa.wrd").read_bytes())


def check_a_partial_file_is_never_published_under_the_real_name() -> None:
    """복사가 중간에 죽어도 목적지에 반쪽짜리가 진짜 이름으로 남으면 안 된다.

    남으면 다음 백업이 크기를 보고 다시 쓰긴 하지만, 그 사이에 복원을 하면
    조용히 잘린 파일을 되돌려 받는다 — 잘린 .wrd 는 오류 없이 열리고 행 수만
    적다.

    디스크가 차는 상황을 만들 수 없으니 복사 함수가 반쯤 쓰고 죽게 한다.
    방아쇠는 인공이지만, 검사하는 것(임시 파일 정리와 이름 공개 시점)은
    실제 코드 경로 그대로다.
    """
    import backup as module

    def dies_halfway(source, target):
        Path(target).write_bytes(Path(source).read_bytes()[:2])
        raise OSError(28, "No space left on device")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        data, destination = root / "data", root / "backup"
        _data_dir(data, "aaa")
        original = module.shutil.copy2
        module.shutil.copy2 = dies_halfway
        try:
            report = Report(destination=destination)
            backup_uploads(data / "uploads", destination / "uploads", report)
        finally:
            module.shutil.copy2 = original

        leftovers = sorted(p.name for p in (destination / "uploads").glob("*"))
        check("실패한 복사는 흔적을 남기지 않는다", leftovers == [], f"{leftovers}")
        check("실패를 보고한다", len(report.problems) == 1, f"{report.problems}")
        check("복사했다고 세지 않는다", report.copied == 0, f"copied={report.copied}")


def check_every_original_is_copied_not_only_wrd() -> None:
    """EIS 원본도 uploads/ 에 산다 (ADR 0019).

    `*.wrd` 글롭이 `.mpr`·`.mpt`·`.mps` 를 지나쳐 놓고 "복사 2건" 을 보고했다.
    백업이 낼 수 있는 최악의 실패다 -- 성공한 것처럼 보이고, 사라진 것은
    복원할 때에야 안다.  확장자로 고르는 대신 uploads/ 안의 파일 전부를
    복사한다: 여기 들어오는 것은 정의상 전부 원본이고, 새 형식이 생겨도
    누가 알아채는 날이 아니라 도착하는 날부터 백업된다.
    """
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        data, destination = root / "data", root / "backup"
        database = _data_dir(data, "aaa")
        for name, blob in (("scan.mpr", b"BIO-LOGIC MODULAR FILE\x1a"),
                           ("scan.mps", b"EC-LAB SETTING FILE"),
                           ("export.mpt", b"EC-Lab ASCII FILE")):
            (data / "uploads" / name).write_bytes(blob)

        report = run(destination, data, database)

        copied = sorted(p.name for p in (destination / "uploads").iterdir())
        check("EIS 원본도 복사한다",
              copied == ["aaa.wrd", "export.mpt", "scan.mpr", "scan.mps"],
              f"{copied}")
        check("전부 복사했다고 센다", report.copied == 4, f"copied={report.copied}")
        for name in ("scan.mpr", "scan.mps", "export.mpt"):
            check(f"{name} 의 바이트가 그대로다",
                  (destination / "uploads" / name).read_bytes()
                  == (data / "uploads" / name).read_bytes())
        # 임시 이름이 원본의 형식을 잘못 말하면 안 된다 (`with_suffix` 는
        # 마지막 확장자를 갈아 끼워서 scan.mpr 을 scan.wrd.part 로 만든다).
        check("임시 파일을 남기지 않는다",
              not any(p.name.endswith(".part")
                      for p in (destination / "uploads").iterdir()))


def check_a_directory_in_uploads_does_not_stop_the_backup() -> None:
    """누가 폴더째 끌어다 놓아도 나머지 원본은 넘어가야 한다."""
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        data, destination = root / "data", root / "backup"
        database = _data_dir(data, "aaa")
        (data / "uploads" / "어쩌다폴더").mkdir()

        report = run(destination, data, database)

        check("폴더는 건너뛴다", not (destination / "uploads/어쩌다폴더").exists())
        check("나머지는 복사한다", (destination / "uploads/aaa.wrd").exists())
        check("실패로 세지 않는다", report.problems == [], f"{report.problems}")


def check_a_missing_database_is_reported_not_invented() -> None:
    """오타 난 경로가 빈 DB 파일을 만들어 놓고 성공했다고 하면 안 된다."""
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        missing = root / "nope.db"
        note = backup_database(missing, root / "out.db")

        check("없는 DB 는 없다고 말한다", "없음" in note, note)
        check("빈 DB 를 만들어 두지 않는다", not (root / "out.db").exists())


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("check_") and callable(function):
            function()
    print(f"\n=== BACKUP === 실패 {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
