"""Test harness: a throwaway data directory and an in-memory database.

Environment variables are set before the app is imported because
``settings`` is built at import time.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "packages/wrdkit/src"))
sys.path.insert(0, str(REPO / "packages/wrdkit/tests"))
sys.path.insert(0, str(REPO / "apps/api"))

_TMP = tempfile.mkdtemp(prefix="workbench-test-")
os.environ["WORKBENCH_DATA"] = _TMP
os.environ["WORKBENCH_DB"] = "sqlite://"

from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import SQLModel  # noqa: E402

from app import memo  # noqa: E402
from app.db import engine, init_db  # noqa: E402
from app.main import app  # noqa: E402

import synthetic  # noqa: E402


@pytest.fixture
def client():
    SQLModel.metadata.drop_all(engine)
    # 메모리 캐시도 데이터베이스와 같이 비운다.  테스트마다 run 1 이 새로
    # 생기고 픽스처가 같은 바이트를 올리므로, 안 비우면 앞 테스트의 컬럼이
    # 그대로 맞아 버려서 "캐시를 지웠는데도 복구된다" 를 확인하는 테스트가
    # 디스크를 아예 건드리지 않고 통과한다.
    memo.clear()
    init_db()
    with TestClient(app) as test_client:
        yield test_client
    SQLModel.metadata.drop_all(engine)


#: One synthetic cycle is 30+3+30+3 points at 10 s -- about 11 minutes.
_CYCLE_SECONDS = 66 * 10


@pytest.fixture
def wrd_bytes() -> bytes:
    """A synthetic 8-cycle file that ends mid-cycle, minutes ago.

    Recency is part of the running/finished evidence, so a fixture meant to
    look like a live cell has to carry fresh timestamps.
    """
    start = synthetic.ticks_ago(8 * _CYCLE_SECONDS)
    samples = synthetic.make_cycles(n_cycles=8, points_per_branch=30,
                                    start_ticks=start)
    return synthetic.build_wrd(samples[:-20], start_ticks=start)


@pytest.fixture
def finished_wrd_bytes() -> bytes:
    """A complete 8-cycle file that ran *before* ``wrd_bytes``.

    The two are used together as ``_011`` and ``_012`` of one experiment, so
    this one has to start earlier for the cycle numbering to continue.
    """
    start = synthetic.ticks_ago(20 * _CYCLE_SECONDS)
    return synthetic.build_wrd(
        synthetic.make_cycles(n_cycles=8, points_per_branch=30, start_ticks=start),
        start_ticks=start)


@pytest.fixture
def cv_wrd_bytes() -> bytes:
    """A file whose charge branch ends in a constant-voltage hold.

    Every real schedule has one, and it is the shape dQ/dV has to exclude:
    voltage flat while capacity keeps rising, so dV is zero and the quotient
    is not a peak but a division by nothing (ADR 0013).  Without a fixture
    that carries it, the drop path is only ever exercised by unit tests on
    hand-built arrays -- never through the parse-store-serve pipeline that
    actually runs.
    """
    start = synthetic.ticks_ago(12 * _CYCLE_SECONDS)
    return synthetic.build_wrd(
        synthetic.make_cycles(n_cycles=6, points_per_branch=60,
                              cv_points=25, start_ticks=start),
        start_ticks=start)


@pytest.fixture
def scheduled_wrd_bytes() -> bytes:
    """A file that carries its schedule, like every real one does.

    Without this the "instrument knows it, do not ask the human" path had no
    coverage at all: the only test named for it fed a schedule-less file and
    asserted that nothing was filled in, so deleting the feature outright
    would have kept the suite green.
    """
    start = synthetic.ticks_ago(30 * _CYCLE_SECONDS)
    return synthetic.build_wrd(
        synthetic.make_cycles(n_cycles=4, points_per_branch=30, start_ticks=start),
        start_ticks=start, schedule=synthetic.DEFAULT_SCHEDULE)


@pytest.fixture
def formationless_wrd_bytes() -> bytes:
    """임피던스를 재고 바로 메인 루프로 들어가는 계획을 담은 파일.

    기준 사이클이 3이 아니라 1이어야 하는 모양이다 (ADR 0018).  루프 앞에 있는
    것은 안정화 휴지 하나뿐이고, 휴지는 formation 이 아니다.
    """
    start = synthetic.ticks_ago(30 * _CYCLE_SECONDS)
    return synthetic.build_wrd(
        synthetic.make_cycles(n_cycles=4, points_per_branch=30, start_ticks=start),
        start_ticks=start, schedule=synthetic.FORMATIONLESS_SCHEDULE)


@pytest.fixture
def sample_id(client):
    response = client.post("/api/samples", json={
        "name": "TEST-01",
        "cathode_type": "High-Ni",
        "cathode_detail": "NCM811",
        "process": "dry",
        "total_mass_mg": 31.6,
        "active_wt_percent": 80,
        "diameter_mm": 13,
        "nominal_specific_capacity_mah_g": 205.9,
        "test_date": "2026-02-15",
    })
    assert response.status_code == 201, response.text
    return response.json()["id"]


@pytest.fixture
def real_wrd_path():
    path = os.environ.get("WRDKIT_SAMPLE")
    if not path or not Path(path).exists():
        pytest.skip("set WRDKIT_SAMPLE to a real .wrd file")
    return Path(path)
