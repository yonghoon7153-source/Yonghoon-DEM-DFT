"""pytest 공통 설정 — repo root를 sys.path에 추가, slow 마커 등록."""

from __future__ import annotations

import re
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


#: ★ 48차 P0-8 — **실행 경로를 그대로 태우는** 시험 모듈.
#:
#:   `src.grid`·`src.fitting` 이 첫 부작용 전에 계획 gate 를 지나게 되면서, 이
#:   모듈들의 단위 시험이 계획을 요구받게 됐다. 그것들은 장난감 입력으로 도는
#:   것이지 production 실행이 아니다.
#:
#:   면제를 "지금 pytest 안인가" 같은 **caller label** 로 주지 않는다 — 46차가
#:   그 방식을 정확히 폐기했다(호출자가 스스로 신고하는 면제는 면제가 아니라
#:   우회로다). 대신 산출을 계약이 이미 면제로 선언한 **실제 경로**
#:   (`results/_smoke/`) 아래 둔다. 판정은 그대로 `is_inside_namespace()` 의
#:   실물 경로 포함 검사이고, 우리는 라벨이 아니라 위치를 바꾼다.
#:
#:   **전역으로 옮기지 않는다.** 초판은 `basetemp` 를 통째로 옮겼는데, 그러면
#:   승격 sink 회귀(`test_archive_bundle` 의 `bundle` 진입점 등)의 **입력까지**
#:   smoke 가 되어 "smoke 산출은 승격할 수 없다" 시험이 의미를 잃는다 — 실측으로
#:   깨졌다. 목록은 좁게 유지한다.
_GATED_ENTRYPOINT_MODULES = frozenset({
    "test_fitting", "tests.test_fitting",
    "test_smooth_cache", "tests.test_smooth_cache",
    "test_grid", "tests.test_grid",
})


@pytest.fixture
def tmp_path(request, tmp_path):
    """gated 진입점을 태우는 모듈에서는 `tmp_path` 를 smoke namespace 안으로."""
    if getattr(request.module, "__name__", "") not in _GATED_ENTRYPOINT_MODULES:
        # ★ generator fixture 는 어느 분기에서도 **반드시 yield 해야** 한다.
        #   `return tmp_path` 로 빠지면 pytest 가 "did not yield a value" 로
        #   118건을 error 로 냈다 (실측).
        yield tmp_path
        return
    import shutil
    import uuid as _uuid

    base = ROOT / "results" / "_smoke" / "_unit"
    base.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", request.node.name)[:40]
    d = base / f"{safe}_{_uuid.uuid4().hex[:8]}"
    d.mkdir()
    yield d
    shutil.rmtree(d, ignore_errors=True)
