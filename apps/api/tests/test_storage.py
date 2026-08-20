"""What lives on disk: the untouchable originals, and the expendable cache.

The database schema helper is exercised here too -- it is the other half of
"what a pull leaves on disk".
"""

import pytest
from sqlalchemy import create_engine, text
from sqlmodel import Session, SQLModel

from app import db, storage
from app.models import Run, Sample


@pytest.fixture
def loaded(client, sample_id, wrd_bytes):
    run = client.post("/api/runs/upload", params={"sample_id": sample_id},
                      files={"file": ("c_012.wrd", wrd_bytes,
                                      "application/octet-stream")}).json()
    return run


# --------------------------------------------------------------------------
# originals
# --------------------------------------------------------------------------
def test_a_half_written_original_is_rewritten_not_trusted(client, wrd_bytes):
    """A crash mid-write must not be confirmed forever by the hash name."""
    digest = "a" * 64
    target = storage.upload_path(digest)
    storage.settings.ensure_dirs()
    target.write_bytes(wrd_bytes[:100])

    storage.store_upload(wrd_bytes, digest)
    assert target.read_bytes() == wrd_bytes


def test_a_damaged_original_is_refused_rather_than_read_short(client, wrd_bytes):
    """A truncated .wrd parses happily with fewer rows; only the hash tells."""
    digest = "b" * 64
    storage.store_upload(wrd_bytes, digest)
    storage.upload_path(digest).write_bytes(wrd_bytes[:len(wrd_bytes) // 2])

    with pytest.raises(storage.StorageError):
        storage.reparse(digest)


# --------------------------------------------------------------------------
# column cache
# --------------------------------------------------------------------------
def test_a_corrupt_cache_is_rebuilt_instead_of_failing_forever(client, loaded):
    path = storage.columns_path(loaded["id"])
    path.write_bytes(path.read_bytes()[:200])

    response = client.get(f"/api/export/runs/{loaded['id']}/raw.csv")
    assert response.status_code == 200
    assert len(response.content.decode("utf-8-sig").splitlines()) > 100


def test_a_cache_left_behind_by_another_run_is_not_served(client, loaded):
    run_id = loaded["id"]
    assert storage.load_columns(run_id, expect_sha256=loaded["sha256"]) is not None
    # SQLite reuses row ids, so a stale directory can sit under a new run's id.
    assert storage.load_columns(run_id, expect_sha256="c" * 64) is None
    assert not storage.columns_path(run_id).exists()


# --------------------------------------------------------------------------
# additive schema migration
# --------------------------------------------------------------------------
def _legacy_engine(tmp_path, row, table: str, column: str):
    """A database on the previous schema: *table* is missing *column*."""
    engine = create_engine(f"sqlite:///{tmp_path}/legacy.db")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(row)
        session.commit()
    with engine.begin() as connection:
        connection.execute(text(f"ALTER TABLE {table} DROP COLUMN {column}"))
    return engine


def test_a_re_added_timestamp_column_is_filled_in_for_existing_rows(
        tmp_path, monkeypatch):
    """``default_factory`` compiles to no SQL default, so SQLite writes NULL."""
    engine = _legacy_engine(tmp_path, Sample(name="old"), "sample", "updated_at")
    monkeypatch.setattr(db, "engine", engine)

    db._add_missing_columns()

    with engine.begin() as connection:
        values = list(connection.execute(text("SELECT updated_at FROM sample")))
    assert values[0][0] is not None


def test_a_required_column_with_no_default_says_so(tmp_path, monkeypatch):
    engine = _legacy_engine(tmp_path, Run(original_name="x.wrd", sha256="d" * 64),
                            "run", "original_name")
    monkeypatch.setattr(db, "engine", engine)

    with pytest.raises(RuntimeError, match="run.original_name"):
        db._add_missing_columns()


# --- 갱신이 심은 회귀 -------------------------------------------------------

def test_two_writers_do_not_share_one_temporary_file(tmp_path, monkeypatch):
    """캐시 없는 run 에 동시 요청이 들어오면 각자 자기 임시 파일을 써야 한다.

    고정 이름(`.name.tmp`)을 쓰면 두 writer 가 같은 파일에 쓰고, 먼저 끝난
    쪽의 unlink 가 다른 쪽의 경로를 걷어가 FileNotFoundError 또는 뒤섞인
    내용이 게시된다.
    """
    import threading

    from app import storage

    target = tmp_path / "columns.npz"
    seen: list[str] = []
    barrier = threading.Barrier(2)

    def writer(payload: bytes):
        def write(handle):
            seen.append(handle.name)
            barrier.wait(timeout=5)
            handle.write(payload)
        storage._write_atomically(target, write)

    threads = [threading.Thread(target=writer, args=(b"a" * 64,)),
               threading.Thread(target=writer, args=(b"b" * 64,))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)

    assert len(set(seen)) == 2, "두 writer 가 같은 임시 파일을 공유했다"
    assert target.exists()
    assert target.read_bytes() in (b"a" * 64, b"b" * 64), "내용이 뒤섞였다"


def test_a_truncated_cache_is_dropped_and_the_handle_released(tmp_path, monkeypatch):
    """손상된 npz 는 버리고 재생성한다 — 열린 핸들이 삭제를 막으면 안 된다."""
    from app import storage

    monkeypatch.setattr(storage.settings, "data_dir", tmp_path)
    directory = storage.run_dir(1)
    directory.mkdir(parents=True, exist_ok=True)
    storage.columns_path(1).write_bytes(b"PK\x03\x04 truncated")

    assert storage.load_columns(1) is None
    assert not storage.columns_path(1).exists(), "손상 캐시가 남았다"


def test_a_cache_whose_row_count_disagrees_with_meta_is_dropped(tmp_path, monkeypatch):
    """같은 sha 인데 배열 길이가 meta 와 다르면 다른 구간을 보여준다."""
    import json

    import numpy as np

    from app import storage

    monkeypatch.setattr(storage.settings, "data_dir", tmp_path)
    directory = storage.run_dir(2)
    directory.mkdir(parents=True, exist_ok=True)
    with open(storage.columns_path(2), "wb") as handle:
        np.savez_compressed(handle, VOLTAGE=np.arange(5.0))
    (directory / "meta.json").write_text(json.dumps(
        {"sha256": "x" * 64, "row_count": 500, "columns": ["VOLTAGE"]}))

    assert storage.load_columns(2) is None
    assert not storage.columns_path(2).exists()


def test_a_cache_that_cannot_be_deleted_still_does_not_500(tmp_path, monkeypatch):
    """Windows 에서 열린 핸들이 unlink 를 막아도 재파싱으로 넘어가야 한다.

    Linux 는 열린 파일도 지워지므로 그 상황 자체는 재현되지 않는다. 대신
    삭제 실패를 직접 주입해, 실패가 예외로 새어 나가지 않는지 고정한다.
    """
    import numpy as np

    from app import storage

    monkeypatch.setattr(storage.settings, "data_dir", tmp_path)
    directory = storage.run_dir(3)
    directory.mkdir(parents=True, exist_ok=True)
    with open(storage.columns_path(3), "wb") as handle:
        np.savez_compressed(handle, VOLTAGE=np.arange(3.0))

    def refuse(self, *args, **kwargs):
        raise PermissionError("file in use by another process")

    monkeypatch.setattr(type(storage.columns_path(3)), "unlink", refuse)

    # 예외 대신 None 이어야 한다 — 호출자는 원본에서 다시 파싱하면 된다.
    assert storage.load_columns(3) is None


def test_a_cache_without_meta_is_not_trusted(tmp_path, monkeypatch):
    """어느 파일에서 왔는지 말하지 못하는 캐시는 근거가 아니다."""
    import numpy as np

    from app import storage

    monkeypatch.setattr(storage.settings, "data_dir", tmp_path)
    directory = storage.run_dir(4)
    directory.mkdir(parents=True, exist_ok=True)
    with open(storage.columns_path(4), "wb") as handle:
        np.savez_compressed(handle, VOLTAGE=np.arange(3.0))

    assert storage.load_columns(4) is None
