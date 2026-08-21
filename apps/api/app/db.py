"""Engine and session plumbing."""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import event, insert
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.orm import Session as SASession
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from . import models  # noqa: F401  -- registers the tables on SQLModel.metadata
from .actor import current_actor
from .settings import settings

_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
_kwargs = {}
if settings.database_url == "sqlite://":  # in-memory, used by the tests
    _kwargs["poolclass"] = StaticPool

engine = create_engine(settings.database_url, connect_args=_connect_args, **_kwargs)


def init_db() -> None:
    settings.ensure_dirs()
    SQLModel.metadata.create_all(engine)
    _add_missing_columns()


def _add_missing_columns() -> None:
    """Add columns that exist in the models but not yet in the database.

    Two people share this repository and pull each other's schema changes, so
    an existing SQLite file will be missing whatever the other person added.
    ``create_all`` only creates whole tables, so without this a pull turns into
    "delete your database and re-upload everything".

    Only additive changes are handled -- a rename or a type change still needs
    a real migration.  A new column the model requires but SQLite cannot fill
    on its own raises here, by name, rather than being added as NULL: the
    response models declare those fields required, so a NULL-filled column
    turns every list and detail endpoint into a 500 the next time somebody
    pulls.
    """
    from sqlalchemy import bindparam, inspect, text

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        for table in SQLModel.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue
            present = {c["name"] for c in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name in present:
                    continue
                backfill = _backfill_value(table.name, column)
                ddl = f"{column.name} {column.type.compile(engine.dialect)}"
                default = _sql_default(column)
                if default is not None:
                    ddl += f" DEFAULT {default}"
                connection.execute(text(f"ALTER TABLE {table.name} ADD COLUMN {ddl}"))
                if backfill is not None:
                    # Bound with the column's own type so a datetime is stored
                    # the way SQLAlchemy stores every other one.
                    statement = text(
                        f"UPDATE {table.name} SET {column.name} = :value "
                        f"WHERE {column.name} IS NULL"
                    ).bindparams(bindparam("value", type_=column.type))
                    connection.execute(statement, {"value": backfill})


def _backfill_value(table_name: str, column):
    """What to write into the existing rows of a newly added column.

    ``created_at``-style fields are the house pattern and they are the ones
    SQLite cannot fill: a ``default_factory`` is a Python callable, so it
    compiles to no SQL DEFAULT and every existing row gets NULL.  Evaluating
    it once here dates the old rows to the migration, which is at least a real
    datetime -- the alternative is a required field arriving as None and
    breaking the response model for every row written before the pull.
    """
    if column.default is not None and column.default.is_callable:
        return column.default.arg(None)
    if column.nullable or column.default is not None or column.primary_key:
        return None
    raise RuntimeError(
        f"{table_name}.{column.name} is required and has no default, so the "
        f"rows already in the database cannot be filled in automatically; "
        f"give the field a default or write a migration for it")


def _sql_default(column) -> str | None:
    """A literal DEFAULT for a newly added column, when one is safe to infer."""
    if column.default is None or column.default.is_callable:
        return None
    value = column.default.arg
    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    return None


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


# --------------------------------------------------------------------------
# 누가 무엇을 바꿨는지 — 자동으로
#
# 라우터가 아니라 flush 리스너에 둔다.  새 엔드포인트는 생기는 순간부터 기록되고,
# 아무도 "여기서도 기록해야 한다" 를 기억할 필요가 없다.  기억에 맡기면 언젠가
# 한 종류의 편집만 기록에서 빠지는데, 그 구멍은 보이지 않는다 — 목록은 멀쩡해
# 보이고 그 한 줄만 없다.
# --------------------------------------------------------------------------

#: 사람이 이야기하는 것들만 기록한다.  CycleRecord 는 사람이 한 편집이 아니고,
#: 업로드 한 번에 만 개가 생긴다 — 사건은 업로드 쪽이다.
_LOGGED: dict[str, str] = {
    "Sample": "sample",
    "ExperimentGroup": "group",
    "CompositionPreset": "preset",
    "Run": "run",
}

#: 감사 기록 자체는 감사하지 않는다.  하면 flush 안에서 끝없이 자란다.
_NEVER_LOGGED = {"Activity"}

#: 사람이 고친 것이 아닌 필드.  이것만 바뀐 것은 편집이 아니라 부기다.
_BOOKKEEPING = {"updated_at", "created_at", "updated_by", "created_by"}

#: Run 에서 사람이 바꾸는 것은 이 셋뿐이다.  나머지 — 장비 모델, 펌웨어,
#: 타임스탬프, 디코딩한 스케줄, 행 수 — 는 파서가 파일에서 읽어 채운다.
#: 그것까지 세면 업로드 한 번이 두 사건으로 읽히고, 두 번째 줄은 아무도
#: 건드리지 않은 필드 아홉 개를 나열한다.
_HUMAN_FIELDS: dict[str, set[str]] = {
    "Run": {"sample_id", "cycle_offset", "cycle_offset_source"},
}


def _label(instance) -> str:
    for attribute in ("name", "original_name"):
        value = getattr(instance, attribute, None)
        if value:
            return str(value)[:120]
    return ""


def _changed_fields(instance) -> list[str]:
    """Which columns this flush is actually changing.

    Asked of SQLAlchemy rather than compared by hand: a PATCH that sets a
    field to the value it already had is not a change, and logging it would
    fill the feed with edits nobody made.
    """
    state = sa_inspect(instance)
    changed = []
    for attribute in state.attrs:
        history = attribute.history
        if history.has_changes() and attribute.key not in _BOOKKEEPING:
            changed.append(attribute.key)
    return sorted(changed)


@event.listens_for(SASession, "before_flush")
def _stamp_and_collect(session, _flush_context, _instances) -> None:
    """Write the actor onto every row, and note what this flush is changing.

    Two halves, and they have to be two.  The change history is only readable
    *before* the flush, and a new row's primary key only exists *after* it --
    so what changed is worked out here and the log lines are written in
    ``_write_activity`` below.  Recording both here gave every "create" a null
    id, which the per-cell history then silently could not find.
    """
    actor = current_actor()
    pending = session.info.setdefault("workbench_activity", [])

    for instance in session.new:
        if type(instance).__name__ in _NEVER_LOGGED:
            continue
        if hasattr(instance, "created_by") and not instance.created_by:
            instance.created_by = actor
        if hasattr(instance, "updated_by"):
            instance.updated_by = actor
        if _LOGGED.get(type(instance).__name__):
            pending.append((actor, "create", instance, ""))

    for instance in session.dirty:
        if type(instance).__name__ in _NEVER_LOGGED:
            continue
        if not session.is_modified(instance, include_collections=False):
            continue
        fields = _changed_fields(instance)
        allowed = _HUMAN_FIELDS.get(type(instance).__name__)
        if allowed is not None:
            fields = [field for field in fields if field in allowed]
        if not fields:
            continue
        if hasattr(instance, "updated_by"):
            instance.updated_by = actor
        if _LOGGED.get(type(instance).__name__):
            pending.append((actor, "update", instance, ",".join(fields)))

    for instance in session.deleted:
        if _LOGGED.get(type(instance).__name__):
            pending.append((actor, "delete", instance, ""))


@event.listens_for(SASession, "after_flush")
def _write_activity(session, _flush_context) -> None:
    """Insert the log lines now that the rows they describe have their ids.

    A Core ``insert`` rather than ``session.add``: an object added during
    ``after_flush`` is not part of the flush that is finishing, so it would
    sit unwritten until something else happened to flush -- which for a
    read-only request is never.
    """
    pending = session.info.pop("workbench_activity", None)
    if not pending:
        return
    now = _now_utc()
    rows = [
        {
            "at": now,
            "actor": actor,
            "action": action,
            "entity": _LOGGED[type(instance).__name__],
            "entity_id": getattr(instance, "id", None),
            "label": _label(instance),
            "fields": fields[:400],
        }
        for actor, action, instance, fields in pending
    ]
    session.execute(insert(models.Activity), rows)


def _now_utc():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).replace(tzinfo=None)
