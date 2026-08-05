"""pytest 공통 설정 — repo root를 sys.path에 추가, slow 마커 등록."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: 실제 PyBaMM solve가 필요한 테스트 (Phase 게이트에서 실행)")


@pytest.fixture(scope="session")
def cfg():
    from src.config import load_config, validate_config

    c = load_config(ROOT / "configs" / "base.yaml")
    validate_config(c)
    return c


@pytest.fixture(scope="session")
def baseline(cfg):
    from src.modes import Baseline

    return Baseline.from_config(cfg)


@pytest.fixture(scope="session")
def d_orig():
    """원본 하드코딩 완방값 — modes 수식 구조 검증용 fixture.

    (실행 경로에서는 절대 사용 금지. 테스트에서는 원본 update_fn과의
    수식 일치를 확인하는 기준값으로만 쓴다.)
    """
    from src.baseline import DischargedState

    return DischargedState(ne_primary=36.7, ne_secondary=3446.3, pe=58439.9)
