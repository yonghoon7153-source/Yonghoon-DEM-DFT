"""Engine and session plumbing."""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from . import models  # noqa: F401  -- registers the tables on SQLModel.metadata
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
    a real migration, and will surface as a clear error rather than silently
    losing data.
    """
    from sqlalchemy import inspect, text

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
                ddl = f"{column.name} {column.type.compile(engine.dialect)}"
                default = _sql_default(column)
                if default is not None:
                    ddl += f" DEFAULT {default}"
                connection.execute(text(f"ALTER TABLE {table.name} ADD COLUMN {ddl}"))


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
