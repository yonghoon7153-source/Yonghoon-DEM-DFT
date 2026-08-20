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

import synthetic  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db import engine, init_db  # noqa: E402
from app.main import app  # noqa: E402
from sqlmodel import SQLModel  # noqa: E402


@pytest.fixture
def client():
    SQLModel.metadata.drop_all(engine)
    init_db()
    with TestClient(app) as test_client:
        yield test_client
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def wrd_bytes() -> bytes:
    """A synthetic 8-cycle file that ends mid-cycle, like a live one."""
    samples = synthetic.make_cycles(n_cycles=8, points_per_branch=30)
    return synthetic.build_wrd(samples[:-20])


@pytest.fixture
def finished_wrd_bytes() -> bytes:
    return synthetic.build_wrd(synthetic.make_cycles(n_cycles=8, points_per_branch=30))


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
