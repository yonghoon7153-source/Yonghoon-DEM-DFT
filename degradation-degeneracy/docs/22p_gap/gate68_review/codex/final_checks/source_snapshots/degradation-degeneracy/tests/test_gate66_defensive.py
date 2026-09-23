"""66차 방어적 검토 (대상 HEAD `fa947cc9` · `source_digest e9ee7475dea7de1d`) — G66-N1 · T1.

65차 대응(명시 import · 상대 cwd · namespace)의 원 반례는 닫혔다고 인정받았다. 그러나 고치면서
**새 등식**이 남았다: `_replay_context()` 가 주는 것은 **startup 이 끝난 뒤의 `sys.path`** 이고,
부모는 거기서 `PathFinder.find_spec()` 를 다시 해 **과거의 import 를 판정**한다.

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| G66-N1 | **사후 resolver 후보 ≠ startup 이 실제로 올린 origin.** `python -c` 는 초기화가 끝난 **뒤** `sys.path[0]=''`(cwd)를 넣으므로, startup 이 한 줄도 읽지 않은 cwd 파일이 "읽었어야 할 후보" 로 소급된다. 정상 `sitecustomize` 가 자기 경로를 정리하거나 다른 후보를 앞에 넣어도 같은 거부가 난다 | `mutation_replay.py:_replay_context` · `_parent_customization_view` |
| G66-T1 | 전제 시험이 `make_interpreter()` 의 skip 을 우회해 `build_interpreter()` 뒤 바로 assert 한다. 생성·측정 subprocess 가 **외부 env 를 물려받아** `PYTHONNOUSERSITE=1` 이면 skip 이 아니라 **실패**한다 | `tests/interpreter_fixture.py` · `test_gate65_defensive.py` |

**한 줄 요약**: *찾을 수 있는 후보* 와 *올렸던 origin* 은 같은 사건이 아니다 (N1) · 전제는 만들고
재되 **무엇을 못 만들었는지**까지 갈라야 한다 (T1).

리뷰어 재현기(`docs/22p_gap/gate66_review/codex/repro_startup.py`)를 이 Linux 에서 먼저 돌려
둘이 재현되는 것을 확인했다 — `remove_loaded_path` child `e4d83544…` vs parent `e3b0c442…`,
`cwd_only_candidate` child `e3b0c442…` vs parent `cb4c3880…`, 대조군 `plain`·`cwd_on_pythonpath`
는 ACCEPTED. 그 관측을 아래 회귀로 고정한다.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
for _p in (REPO, REPO / "tests", REPO / "docs" / "22p_gap"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from interpreter_fixture import build_interpreter, make_interpreter, use_interpreter  # noqa: E402


def _mr():
    import mutation_replay as mr

    return mr


def _digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _pin(monkeypatch, extra: dict) -> None:
    mr = _mr()
    base = dict(mr.replay_env())
    base.pop("PYTHONNOUSERSITE", None)
    base.update(extra)
    monkeypatch.setattr(mr, "replay_env", lambda: dict(base))


def _entry(monkeypatch, cwd: Path):
    """실제 진입점 `_execution_receipt()` 를 그 cwd 를 재생 root 로 삼아 부른다."""
    mr = _mr()
    monkeypatch.setattr(mr, "_sandboxed", lambda p: cwd)
    return mr._execution_receipt()


def _startup(dirpath: Path, body: str) -> Path:
    dirpath.mkdir(parents=True, exist_ok=True)
    f = dirpath / "sitecustomize.py"
    f.write_text(body, encoding="utf-8")
    return f


# ── G66-N1 — 사후 후보로 과거 import 를 판정하지 않는다 ─────────────────────────────

def test_g66_01_a_cwd_file_that_startup_never_imported_is_not_expected(tmp_path, monkeypatch, off):
    """★ G66-N1 A — replay cwd 에 정상 `sitecustomize.py` 가 있지만 **`PYTHONPATH` 에는 없다**.
    `python -c` 의 `sys.path[0]=''` 는 초기화가 **끝난 뒤** 붙으므로 startup 은 그 파일을 읽지
    않는다. 부모가 사후 경로로 그것을 찾아 "읽었어야 한다" 고 하면 정상 영수증이 거부된다."""
    cwd = tmp_path / "replay"
    cwd.mkdir()
    (cwd / "sitecustomize.py").write_text("# 아무도 안 읽는 cwd 파일\n", encoding="utf-8")
    empty = tmp_path / "empty"
    empty.mkdir()
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(empty)})
    mr = _mr()
    try:
        _entry(monkeypatch, cwd)
    except mr._ReplayError:
        raise AssertionError(
            "startup 이 읽지 않은 cwd 파일을 부모가 기대해 정상 영수증을 거부했다 (G66-N1 A)"
        ) from None


def test_g66_02_a_startup_that_cleans_its_own_path_is_still_accepted(tmp_path, monkeypatch, off):
    """★ G66-N1 B — 정상 `sitecustomize` 가 **자기 디렉터리를 `sys.path` 에서 지운다** (Python 이
    sitecustomize 에 허용하는 일이다). 파일도 `sys.modules` 도 그대로인데, 부모가 사후 경로에서
    다시 찾으면 그 후보가 없어 `<absent>` 를 기대한다."""
    start = tmp_path / "startup"
    _startup(start, "import os, sys\n"
                    "_here = os.path.dirname(__file__)\n"
                    "sys.path[:] = [p for p in sys.path if os.path.abspath(p) != _here]\n")
    cwd = tmp_path / "replay"
    cwd.mkdir()
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    try:
        rec = _entry(monkeypatch, cwd)
    except mr._ReplayError:
        raise AssertionError(
            "자기 검색 경로를 정리한 정상 startup 의 영수증을 거부했다 (G66-N1 B)") from None
    assert rec["startup"]["customization"]["sitecustomize"] == _digest(start / "sitecustomize.py")


def test_g66_03_a_startup_that_prepends_another_candidate_is_still_accepted(tmp_path, monkeypatch, off):
    """★ G66-N1 C — startup 이 다른 디렉터리를 `sys.path` **앞에** 넣고 그곳에 또 다른
    `sitecustomize.py` 가 있다. 이미 올라간 것은 원래 것인데 부모의 사후 탐색은 새 것을 고른다."""
    start = tmp_path / "startup"
    other = tmp_path / "other"
    other.mkdir()
    (other / "sitecustomize.py").write_text("# 한 번도 import 되지 않는 다른 후보\n", encoding="utf-8")
    _startup(start, f"import sys\nsys.path.insert(0, {str(other)!r})\n")
    cwd = tmp_path / "replay"
    cwd.mkdir()
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    try:
        rec = _entry(monkeypatch, cwd)
    except mr._ReplayError:
        raise AssertionError(
            "startup 이 앞에 넣은 다른 후보를 부모가 로드된 것으로 봤다 (G66-N1 C)") from None
    assert rec["startup"]["customization"]["sitecustomize"] == _digest(start / "sitecustomize.py")


def test_g66_04_changed_bytes_are_still_rejected(tmp_path, monkeypatch, off):
    """대조군 — **바이트가 바뀌면 여전히 거부**한다. N1 을 고치면서 "부모 대조를 통째로 허용" 하면
    이 시험이 잡는다 (리뷰어의 금지 조건)."""
    start = tmp_path / "startup"
    f = _startup(start, "# 원래 바이트\n")
    cwd = tmp_path / "replay"
    cwd.mkdir()
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    rec = _entry(monkeypatch, cwd)                     # 정상은 통과해야 한다
    f.write_text("# 실행 뒤에 갈아 끼운 바이트\n", encoding="utf-8")
    ctx = mr._replay_context(cwd)
    with pytest.raises(mr._ReplayError, match="customization"):
        mr._assert_customization_matches_parent(rec, ctx)


def test_g66_05_a_forged_absent_is_still_rejected(tmp_path, monkeypatch, off):
    """대조군 — 이력이 올렸다고 하는데 customization 이 `<absent>` 인 **세탁본**은 계속 거부."""
    start = tmp_path / "startup"
    _startup(start, "# 평범한 startup\n")
    cwd = tmp_path / "replay"
    cwd.mkdir()
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    rec = _entry(monkeypatch, cwd)
    rec["startup"]["customization"]["sitecustomize"] = "<absent>"
    with pytest.raises(mr._ReplayError, match="sitecustomize"):
        mr._assert_customization_matches_parent(rec, mr._replay_context(cwd))


def test_g66_05b_a_forged_absent_namespace_is_still_rejected(tmp_path, monkeypatch, on):
    """대조군 — **이력에 파일로 잡히지 않는** customization(표준 namespace)을 child 가
    `<absent>` 라 적으면 거부해야 한다.

    이력(`-X importtime -v` → 파일 있는 module) 은 namespace 를 `unfiled` 로 세므로 첫 분기
    (`loaded_file`)가 안 잡는다. 부모가 **올라와 있다고 잰** 이름을 child 가 없다고 적는 것을
    막는 두 번째 분기가 그 자리다 — 66차에서 `auto` 축이 옮겨 온 곳이다.
    (`sitecustomize` 는 이 기계의 stdlib 자리 파일이 가리므로 자유로운 이름 `usercustomize` 로 만든다.)
    """
    site = tmp_path / "site"
    (site / "usercustomize").mkdir(parents=True)
    use_interpreter(monkeypatch, on)
    _pin(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()
    cwd = tmp_path / "replay"
    cwd.mkdir()
    rec = _entry(monkeypatch, cwd)
    assert rec["startup"]["customization"]["usercustomize"].startswith("<namespace>"), \
        rec["startup"]["customization"]
    rec["startup"]["customization"]["usercustomize"] = "<absent>"          # 세탁본
    with pytest.raises(mr._ReplayError, match="usercustomize"):
        mr._assert_customization_matches_parent(rec, mr._replay_context(cwd))


def test_g66_06_an_origin_less_module_is_still_failed(tmp_path, monkeypatch, off):
    """대조군 — origin 도 검색 위치도 없는 module 은 계속 typed `failed` 다 (G65-N2b 금지 조건)."""
    start = tmp_path / "startup"
    _startup(start, "import sys, types\n"
                    "sys.modules['usercustomize'] = types.ModuleType('usercustomize')\n")
    cwd = tmp_path / "replay"
    cwd.mkdir()
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    src = mr._ENV_PROBE_BODY + (
        "\nimport json\n"
        f"print(json.dumps(_receipt_facts({mr._probe_names()!r}, [], {str(cwd)!r}), "
        f"sort_keys=True, ensure_ascii=False))\n")
    env = dict(os.environ)
    env.pop("PYTHONNOUSERSITE", None)
    env.update({"PYTHONPATH": str(start), "PYTHONHASHSEED": "0"})
    r = subprocess.run([str(off), "-c", src], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr[-800:]
    got = json.loads(r.stdout.strip().splitlines()[-1])
    assert got["startup"].get("status") == "failed", got["startup"].get("customization")


def test_g66_07_the_replay_context_is_measured_once(tmp_path, monkeypatch, off):
    """리뷰어의 정적 관측 — `ctx` 를 생략한 경로가 보조 인터프리터를 **두 번** 띄운다
    (`_parent_customization_view(None)` 가 한 번, 그 다음 줄이 또 한 번). "한 번 측정한 하나의
    문맥" 이라고 적었으므로 그대로 만든다. 별도 finding 으로 세지 않겠다고 했지만 고친다."""
    start = tmp_path / "startup"
    _startup(start, "# 평범한 startup\n")
    cwd = tmp_path / "replay"
    cwd.mkdir()
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    calls = []
    real = mr._replay_context

    def counted(c=None):
        calls.append(c)
        return real(c)

    monkeypatch.setattr(mr, "_replay_context", counted)
    _entry(monkeypatch, cwd)
    assert len(calls) == 1, ("한 번의 진입점 호출이 재생 문맥을 여러 번 쟀다", len(calls))


# ── G66-T1 — 전제의 환경 의존 ────────────────────────────────────────────────────

#: child pytest 의 **입력 경계** — 바깥이 얹는 옵션·plugin 정책은 이 시험의 자료가 아니다.
#: ★ 67차 G67-T1: 전 판은 `dict(os.environ)` 을 그대로 물려줬다. 바깥
#:   `PYTEST_ADDOPTS=--g67-option-does-not-exist` 면 child 가 **사용법 오류(rc 4)** 로 끝나고
#:   `PYTEST_ADDOPTS=--collect-only` 면 **수집만 하고 실행 0건**인데, 이 시험은 둘 다 초록이었다
#:   (리뷰어 실측). 옵션은 우리가 정한다.
_PYTEST_ENV_KNOBS = ("PYTEST_ADDOPTS", "PYTEST_PLUGINS", "PYTEST_DISABLE_PLUGIN_AUTOLOAD",
                     "PYTEST_CURRENT_TEST")
#: 이 전제 시험이 **반드시 돌아야 하는** 두 node (True=활성 · False=비활성).
_PREMISE_NODES = frozenset({"test_the_interpreter_fixture_measures_its_own_premise[True]",
                            "test_the_interpreter_fixture_measures_its_own_premise[False]"})


def _premise_run(python, env_extra: dict, junit: Path | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    for k in _PYTEST_ENV_KNOBS:
        env.pop(k, None)
    env.update(env_extra)
    cmd = [str(python), "-m", "pytest", str(REPO / "tests" / "test_gate65_defensive.py"),
           "--noconftest", "-q", "-p", "no:cacheprovider",
           "-k", "the_interpreter_fixture_measures_its_own_premise"]
    if junit is not None:
        cmd.append(f"--junitxml={junit}")
    return subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True, timeout=900)


def _premise_outcomes(junit: Path) -> dict:
    """JUnit XML → `{node: 'passed'|'skipped'|'failed'|'error'}`.

    ★ 67차 G67-T1 — `"failed" not in stdout` 은 *시험이 돌았다*를 말하지 않는다. 기계가 읽는
      결과를 쓰고, **수집만 된 것·사용법 오류·node 누락**을 전부 PASS 가 아닌 것으로 가른다.
      `--junitxml` 은 pytest 내장이라 plugin 을 더 요구하지 않는다.
    """
    import xml.etree.ElementTree as ET

    out = {}
    for case in ET.parse(junit).getroot().iter("testcase"):
        if case.find("error") is not None:
            state = "error"
        elif case.find("failure") is not None:
            state = "failed"
        elif case.find("skipped") is not None:
            state = "skipped"
        else:
            state = "passed"
        out[case.get("name")] = state
    return out


def assert_premise_actually_ran(r: subprocess.CompletedProcess, junit: Path) -> list:
    """child pytest 가 **정말 돌았고** 두 전제 node 가 call 단계를 지났는가 → 미측정 node 목록.

    ★ 67차 G67-T1 — 전 판의 증거는 `"failed" not in stdout` 하나였다. 그래서 child 가 사용법
      오류(rc 4)로 끝나거나 수집만 하고 실행 0건이어도 초록이었다 (리뷰어 실측 4 case).
      리뷰어가 짚은 대로 **`rc 0` 만 더해도 `--collect-only` 는 남는다** — 그래서 넷을 본다:
      rc 0 · 결과 파일 존재 · **정확히 그 두 node** · 각 node 가 `passed`/`skipped`.
      `skipped` 는 통과가 아니라 **미측정**이므로 돌려주고 호출자가 따로 적는다.

      이 helper 가 따로 있는 이유: 이것을 **실제 child 로** 적대적으로 묻는 회귀
      (`test_gate67_defensive.py::test_g67_11`)가 fake subprocess 없이 돌 수 있어야 한다.
    """
    tail = ((r.stdout or "")[-600:], (r.stderr or "")[-400:])
    # ⚠ 순서가 **사유의 정확도**를 정한다. rc 를 먼저 보면 어떤 고장이든 "정상 종료하지 않았다"
    #   하나로 뭉개지고, 그러면 변이 증인도 그 뭉갠 문장이 된다. 구체적인 것부터 본다:
    #   결과 파일 → 정확한 node 집합 → 각 node 의 결말 → 그 밖의 rc (남은 것을 잡는 그물).
    assert junit.is_file(), (
        "child pytest 가 결과 파일을 남기지 않았다 — 무엇이 돌았는지 말할 수 없다 (G67-T1)", tail)
    outcomes = _premise_outcomes(junit)
    assert set(outcomes) == set(_PREMISE_NODES), (
        "기대한 두 전제 node 가 실제로 돌지 않았다 — 수집만 했거나 선택이 어긋났다 (G67-T1)",
        sorted(outcomes), sorted(_PREMISE_NODES))
    broken = {k: v for k, v in outcomes.items() if v not in ("passed", "skipped")}
    assert not broken, (
        "물려받은 env 때문에 전제 시험이 실패했다 — 환경의 비활성을 fixture 구현 실패로 오판한다 "
        "(G66-T1)", broken, tail)
    assert r.returncode == 0, (
        "전제 시험을 돌린 child pytest 가 정상 종료하지 않았다 — 사용법·수집·setup 오류는 "
        "통과가 아니다 (G67-T1)", r.returncode, tail)
    return sorted(k for k, v in outcomes.items() if v == "skipped")


@pytest.mark.parametrize("env_extra", [{}, {"PYTHONNOUSERSITE": "1"}], ids=["clean", "nousersite"])
def test_g66_08_the_premise_test_does_not_fail_on_an_inherited_env(env_extra):
    """★ G66-T1 — 외부 `PYTHONNOUSERSITE=1` 은 **환경이 user site 를 끈 것**이지 fixture 가
    `--system-site-packages` 를 빠뜨린 것이 아니다. 전제 시험은 그 둘을 갈라야 하고, 앞의 경우는
    **실패가 아니라 skip(미측정)** 이어야 한다.

    리뷰어 실측(Windows): `PYTHONNOUSERSITE=1` 에서 `1 failed · 1 passed`.

    ★ 67차 G67-T1 — 증거의 모양을 바꿨다. 전 판은 `"failed" not in stdout` 하나였고, 그래서
    child 가 **아예 안 돌아도**(rc 4 · 수집 0건) 초록이었다. 이제 넷을 요구한다:
    rc 0 · JUnit 산출 존재 · **정확히 그 두 node** · 각 node 가 `passed` 또는 `skipped`.
    `skipped` 는 통과가 아니라 **미측정**이므로 따로 적는다.
    """
    # ⚠ 67차 — **`tmp_path` fixture 를 쓰지 않는다.** 외부 검토 스크립트가 이 시험 함수를
    #   `(env_extra)` 하나로 **직접** 부르기 때문이다 (리뷰어 `repro_boundaries.py`). 인자를
    #   늘리면 그쪽 관측이 `TypeError` 가 되고, **그 거부는 우리 수정의 증거가 아니다** —
    #   실제로 한 번 그렇게 나왔고 그것을 통과로 세지 않았다. (기본값을 주는 방법은
    #   pytest 가 fixture 를 안 넣어 임시 디렉터리가 새어 나가므로 쓰지 않는다 — 실측.)
    with tempfile.TemporaryDirectory(prefix="g66t1-") as _d:
        junit = Path(_d) / "premise.xml"
        r = _premise_run(sys.executable, env_extra, junit)
        unmeasured = assert_premise_actually_ran(r, junit)
    if unmeasured:
        print(f"[G66-T1] 이 기계의 정책으로 **미측정**(skip)된 전제 node: {unmeasured}")


def test_g66_09_the_fixture_still_catches_a_missing_activation_option(tmp_path, monkeypatch):
    """대조군 — 활성 옵션(`--system-site-packages`)을 빼는 **변이는 여전히 실패**해야 한다.
    "전부 skip" 으로 숨기면 T1 축이 사라진다 (리뷰어의 금지 조건)."""
    import interpreter_fixture as IF

    real = subprocess.run

    def no_system_site(cmd, *a, **k):
        cmd = [c for c in cmd if c != "--system-site-packages"]
        return real(cmd, *a, **k)

    monkeypatch.setattr(IF.subprocess, "run", no_system_site)
    py = IF.build_interpreter(tmp_path, user_site=True)
    assert IF.measured_user_site(py) is False, "활성 옵션을 빼도 활성으로 측정됐다 — 변이가 안 물린다"


# ── fixture ──────────────────────────────────────────────────────────────────────

@pytest.fixture
def off(tmp_path_factory):
    """user site **비활성** 인터프리터 (일반 venv 와 같은 조건)."""
    return make_interpreter(tmp_path_factory.mktemp("g66-off"), user_site=False)


@pytest.fixture
def on(tmp_path_factory):
    """user site **활성** 인터프리터 — `usercustomize` 가 실제로 올라오는 조건."""
    return make_interpreter(tmp_path_factory.mktemp("g66-on"), user_site=True)
