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
