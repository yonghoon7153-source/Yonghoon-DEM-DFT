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
