"""pytest 공통 설정 — repo root를 sys.path에 추가, slow 마커 등록."""

from __future__ import annotations

import hashlib
import re
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

#: ★ 70차 E6 — 운영 authority (tracked). 시험 세션은 여기에 **아무것도 쓰지 않고**, 끝날 때 불변을 확인한다.
_REAL_LEDGER = ROOT / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
_REAL_AUTHORITY_DIRS = (ROOT / "docs" / "22p_gap" / "_exec_class",
                        ROOT / "docs" / "22p_gap" / "_frozen_coords")
_TEST_AUTHORITY: dict = {}


def _isolate_test_authority() -> Path:
    """시험 세션의 기본 원장을 **바이트 복사본**으로 바꾼다 (70차 E6).

    리뷰어(70차 §4 E6): 시험이 운영 등록부에 synthetic canonical 을 만들 수 있고
    (`tests/test_compare.py::_complete_artifact` 가 `ledger=None` 으로 등록), session cleanup 은
    시작 때 없던 JSON 을 **소유권 구분 없이** 지웠다 — 다른 실행이 그 사이 합법적으로 만든 기록도
    삭제 대상이었다. 62차 §0-⑥ 이 "다른 시험의 오염은 그대로다" 라고 신고한 그 항목이다.

    `[해석]` 지우는 것으로는 못 닫는다 — 누가 만들었는지 파일이 말하지 않기 때문이다. 대신 **쓰는 자리를
    옮긴다**: `tools.preserve.DEFAULT_LEDGER` 는 모듈 전역이고 `canonical_ledger(None)` 이 호출 시점에
    읽으므로, 세션 시작(`pytest_configure`, 좌표 봉인 bootstrap **앞**)에 원장 사본을 세우면 기본
    인자로 가는 모든 파생 root(`_exec_class`·`_frozen_coords`·`_claims`·`_attempts`)가 그 옆으로 간다.
    환경변수 우회를 두지 않는다 — 그런 문은 gate 의 구멍이다 (`test_lifecycle_e2e.py` 머리의 이유와 같다).
    명시적 `ledger=` 를 쓰는 시험(대다수)은 영향받지 않는다.

    범위: **in-process** 호출. 시험이 띄우는 자식(`run.sh`·`python -m src.grid`)은 자기 `tools.preserve`
    를 새로 import 하므로 운영 authority 를 본다 — 그것들은 smoke namespace 안에서 돌고 `_exec_class/local/`
    (gitignored 운용 상태)에만 쓴다. 그 사실을 세션 끝의 불변 검사(`_the_real_authority_is_untouched`)가
    확인한다: 최상위 `_exec_class/*.json` 과 `_frozen_coords/*.json` 은 이름도 바이트도 안 움직여야 한다.
    """
    import tools.preserve as P

    # ★ 자식 진입점까지 같은 authority 를 보게 하는 방법은 **tree 복사** 하나다 (`test_lifecycle_e2e.py`
    #   가 49차부터 쓰는 방식). 자식(`scripts/archive_results.sh` · `python -m tools.archive_bundle` …)은
    #   자기 `tools/preserve.py` 의 **위치**에서 `DEFAULT_LEDGER` 를 유도하므로, RUN_SCOPE 를 바이트
    #   그대로 복사한 tree 안의 스크립트를 부르면 in-process 와 자식이 같은 사본 원장을 본다 — 환경변수
    #   같은 override 문을 production 에 뚫지 않고도 격리된다. `source_digest()` 도 같은 값을 낸다 (RUN_SCOPE 의 `requirements*.txt` 까지 복사한다 — 71차).
    #   자식을 띄우는 시험은 `isolated_tree()` 의 스크립트를 부른다 (`test_compare.py` 의 archive wrapper 회귀).
    tmp = Path(tempfile.mkdtemp(prefix="dd-test-authority-"))
    for name in ("src", "tools", "configs", "scripts"):
        shutil.copytree(ROOT / name, tmp / name, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy2(ROOT / "run.sh", tmp / "run.sh")
    # ★ 71차 리뷰어 §3 — RUN_SCOPE 에는 `requirements*.txt` 도 든다 (`src/io.py::_SCOPE_FILE_GLOBS`).
    #   70차 초판은 그것을 빼놓고 "격리 tree 의 source_digest 도 같다" 고 적었다 — 성립하지 않는 문장이었다.
    #   이제 복사하고, `test_gate71_defensive.py::test_g71_e6_*` 가 자식 프로세스로 같은 값을 잰다.
    for q in ROOT.glob("requirements*.txt"):
        shutil.copy2(q, tmp / q.name)
    gap = tmp / "docs" / "22p_gap"
    gap.mkdir(parents=True)
    for q in (ROOT / "docs" / "22p_gap").glob("*.py"):       # row_projection 등 — 자식이 import 할 수 있다
        shutil.copy2(q, gap / q.name)
    led = gap / "LEG_PRESERVATION.yaml"
    shutil.copyfile(_REAL_LEDGER, led)          # 계획·cohort·실행 기록은 그대로 보인다 (바이트 동일)
    P.DEFAULT_LEDGER = led
    _TEST_AUTHORITY.update(tmp=tmp, tree=tmp, ledger=led, real=_REAL_LEDGER)
    return led


def isolated_tree() -> Path:
    """자식 프로세스를 띄우는 시험이 부를 **격리 tree** 의 뿌리 (70차 E6). RUN_SCOPE 바이트 동일 사본."""
    tree = _TEST_AUTHORITY.get("tree")
    assert tree is not None, "시험 authority 가 세워지지 않았다 (pytest_configure 앞에서 불렀는가)"
    return Path(tree)


def _authority_snapshot() -> dict:
    out = {}
    for d in _REAL_AUTHORITY_DIRS:
        if not d.is_dir():
            continue
        for q in d.glob("*.json"):                # 최상위만 — `local/` 은 운용 scratch
            out[str(q.relative_to(ROOT))] = hashlib.sha256(q.read_bytes()).hexdigest()
    return out


def _bootstrap_frozen_coordinate_seals() -> list:
    """이 **checkout 이 놓인 자리**의 얼린 좌표를 처음 한 번 봉인한다 (59차 자체 발견).

    59차 M6 은 "봉인 없는 frozen cohort 가 하나라도 있으면 아무 데도 안 쓴다" 를
    게시 경로에 넣었다. 그런데 좌표 봉인(`_frozen_coords/`)의 이름은 **좌표**이고
    좌표에는 그 filesystem 안의 경로가 들어간다 — 그래서 트리를 복사하면 봉인
    파일이 **함께 복사돼 있어도** 새 자리에 대해서는 없는 것이다.

    실측: 변이 재생 1/12 조각의 baseline 이 `_assert_writable()` 의 그 거부로
    3건 빨갛게 죽었다 (sandbox 는 복사본이다). 시험이 쓰는 자리는 pytest 의
    tmp 디렉터리이고 얼린 cohort 와 아무 관계가 없는데도 막혔다. fresh clone 의
    `pytest tests/` 도 같은 이유로 빨갛다.

    `[해석]` 봉인 파일은 지역 파일이고 그것을 쓸 수 있는 자는 다시 쓸 수도
    있다. 그러므로 이 층이 실제로 막는 것은 **"봉인한 뒤에 대상이 바뀌는 것"**
    이지 "처음 본 것이 남의 것인 경우" 가 아니다. 사람에게 명령 한 줄을
    요구해도 그 사실은 안 바뀌고, 바뀌는 것은 새 checkout 의 시험이 빨갛다는
    것뿐이다. 그래서 **시험 세션은 자기 자리를 처음 한 번 봉인하고, 무엇을
    봉인했는지 출력한다** (조용히 하지 않는다 — 조용한 bootstrap 은 없는 층을
    있는 척하는 것과 구별되지 않는다).

    게시 경로의 거부는 **그대로 둔다**: 사람이 `--seal-frozen` 없이 새 세대를
    게시하려 하면 여전히 멈춘다 (`test_frozen_clean_clone_59.py` 의 앞 두 시험).
    """
    gap = ROOT / "docs" / "22p_gap"
    if str(gap) not in sys.path:
        sys.path.insert(0, str(gap))
    import row_projection as R

    return R.seal_frozen_cohorts()


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: 실제 PyBaMM solve가 필요한 테스트 (Phase 게이트에서 실행)")
    # ★ 70차 E6 — 좌표 봉인 bootstrap 보다 **먼저**. 그래야 봉인도 시험 authority 로 간다.
    led = _isolate_test_authority()
    print(f"\n[conftest] 시험 authority: {led} (운영 원장의 바이트 복사본 — 70차 E6)")
    sealed = _bootstrap_frozen_coordinate_seals()
    if sealed:
        print(f"\n[conftest] 이 checkout 을 처음 보았다 — 얼린 cohort "
              f"{len(sealed)}개의 좌표를 시험 authority 에 봉인했다: {sealed}")


def pytest_unconfigure(config):
    tmp = _TEST_AUTHORITY.get("tmp")
    if tmp is not None:
        shutil.rmtree(tmp, ignore_errors=True)
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
    # ★ 61차 β — production `run_fit()` 을 **끝까지** 태워서 굳은 기록의
    #   경로를 보는 회귀다. gated 진입점을 지나므로 여기 적는다.
    "test_logical_paths_61", "tests.test_logical_paths_61",
    # ★ 62차 β′·γ′ — lock 수명·capability 폐기·run_sig 를 production `run_fit()`
    #   `run_grid()` 로 잰다. 같은 이유로 gated.
    "test_lock_lifetime_62", "tests.test_lock_lifetime_62",
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


@pytest.fixture(scope="session", autouse=True)
def _the_real_authority_is_untouched():
    """★ 70차 E6 — 운영 authority 의 **불변을 확인한다. 지우지 않는다.**

    58차 P0-8 후속의 이 fixture(`_exec_class_registry_is_not_polluted_by_tests`)는 세션 시작 때 없던
    JSON 을 끝에서 전부 지웠다. 리뷰어(70차 E6): 그 삭제는 소유권을 보지 않으므로 다른 실행이 그 사이
    합법적으로 만든 기록도 지운다 — archive/report 가 같은 권한 기록을 소비하므로 계산 후 증거·승격
    경로의 실제 간섭 위험이다.

    이제 쓰는 자리가 시험 authority 로 옮겨졌으므로(`_isolate_test_authority`) 운영 쪽에는 새 레코드가
    생기지 **않아야** 한다. 생겼다면 어느 시험(또는 자식 진입점)이 격리 밖으로 썼다는 뜻이고, 그것은
    지울 일이 아니라 **빨갛게 보고할 일**이다 — 이름을 전부 적고 사람이 본다. 바뀐 바이트·사라진
    이름도 같다 (등록부는 authority 데이터다).
    """
    before = _authority_snapshot()
    yield
    after = _authority_snapshot()
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if before[k] != after[k])
    assert not (added or removed or changed), (
        "시험 세션이 운영 authority 를 건드렸다 (70차 E6) — 지우지 않았다, 사람이 본다:\n"
        f"  새로 생김 {len(added)}: {added[:8]}{' …' if len(added) > 8 else ''}\n"
        f"  사라짐   {len(removed)}: {removed[:8]}\n"
        f"  바뀜     {len(changed)}: {changed[:8]}")


@pytest.fixture(scope="session", autouse=True)
def _exec_class_registry_is_not_polluted_by_tests():
    """★ 58차 P0-8 후속 — **시험이 저장소의 실행 class 등록부를 늘리지 않는다.**

    P0-8 이 등록부를 만들자마자 이 결함이 생겼다: `_complete_artifact()` 가
    산출을 합성할 때마다 **실물** `docs/22p_gap/_exec_class/` 에 파일을 하나씩
    남겼고, 한 번의 전체 회귀로 93건이 쌓여 그대로 커밋됐다 (실측).

    `[해석]` 등록부는 **authority 데이터**다. 시험이 그것을 늘릴 수 있으면
    "등록돼 있다" 는 사실의 값이 떨어진다 — 누가 언제 왜 넣었는지 모르는
    항목이 섞이기 때문이다. 그래서 이 저장소에서 등록부에 남을 자격이 있는
    것은 둘뿐이다: **실제 실행이 게이트를 지난 기록**과 **사람이 한 legacy 분류**.

    세션 시작 때 이름을 찍어 두고 끝나면 **새로 생긴 것을 지운다.** 시험을
    고치는 대신 여기서 쓸어 담는 이유는, 이 pollution 이 fixture 하나의 문제가
    아니라 **"시험이 production authority 를 만진다"** 는 부류이기 때문이다 —
    새 시험이 같은 실수를 해도 여기서 걸린다.

    ★ 58차 L5 후속 — **authority 를 새로 만들면 이 목록에 같이 적는다.**
      L5 가 얼린 좌표 봉인(`_frozen_coords/`)을 만들자마자 똑같은 일이
      벌어졌다: 한 번의 회귀로 19건이 쌓였고 전부 `/tmp/pytest-of-root/...`
      였다. 등록부가 하나 늘 때마다 이 목록도 늘어야 한다 — 그 사실을 여기
      적어 두지 않으면 다음 authority 에서 또 반복된다.

    ★ 70차 E6 — 이 fixture 는 이제 **시험 authority**(`_isolate_test_authority` 가 세운 사본 옆)만
      정리한다. 운영 등록부는 건드리지 않는다 — 거기의 불변은 `_the_real_authority_is_untouched` 가
      **확인**한다(삭제 아님). 시험 authority 는 세션마다 새 tempdir 이므로 이 정리는 사실상 멱등
      안전망이고, `pytest_unconfigure` 가 디렉터리째 지운다.
    """
    led = Path(_TEST_AUTHORITY.get("ledger") or _REAL_LEDGER)
    assert led.resolve() != _REAL_LEDGER.resolve(), (
        "시험 authority 가 세워지지 않았다 — 운영 등록부를 정리 대상으로 삼지 않는다 (70차 E6)")
    regs = [led.parent / "_exec_class", led.parent / "_frozen_coords"]
    before = {r: ({q.name for q in r.glob("*.json")} if r.is_dir() else set())
              for r in regs}
    yield
    for r in regs:
        if not r.is_dir():
            continue
        for q in r.glob("*.json"):
            if q.name not in before[r]:
                q.unlink(missing_ok=True)
