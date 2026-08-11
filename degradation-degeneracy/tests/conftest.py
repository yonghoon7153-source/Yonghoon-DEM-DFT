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
def _isolated_discharged_cache(tmp_path_factory):
    """★ 12차 발견 8 — slow 테스트가 **작업 디렉터리의 ambient 캐시**에 의존하면
    안 된다. 옛 형식(solver·env 필드 없음) 캐시가 남아 있으면 fail-closed 로
    죽어서, `pytest` 만으로 전체를 재현한다는 주장이 성립하지 않았다
    (리뷰 실측: slow 3개 중 2개가 legacy 캐시 때문에 실패).
    세션 전용 캐시 디렉터리로 격리해 필요한 것은 그 안에서 계산한다.
    """
    import src.baseline as bl

    d = tmp_path_factory.mktemp("discharged_cache")
    orig = bl._cache_path

    def _patched(cfg, cache_dir=None):
        return orig(cfg, cache_dir if cache_dir is not None else d)

    bl._cache_path = _patched
    yield d
    bl._cache_path = orig


@pytest.fixture(scope="session")
def cfg(_isolated_discharged_cache):
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
