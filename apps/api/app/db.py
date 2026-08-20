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


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
