"""65차 방어적 검토 (대상 HEAD `5e4cf103` · `source_digest e9ee7475dea7de1d`) — G65-N1a · N1b ·
N2b · T1, 그리고 E2-R 후속 (token 탐침의 음성).

64차 셋의 "종결" 을 리뷰어가 **부분 수용**했다: 원 사례는 닫혔지만 고치면서 세운 새 등식이
틀렸다. 넷 다 **정상 입력**에서 우리 층이 거부하거나 실패한 축이고 위조 성공이 아니다.

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| N1a (P1) | 부모가 user site 비활성이면 origin 을 보기도 전에 `usercustomize = <absent>`. 정상 `sitecustomize` 가 `import usercustomize` 를 하면 child 는 진짜 digest 를 낸다 → **정상 영수증 거부**. "자동 import 안 함" 을 "로드 안 됨" 으로 바꿔 읽었다 | `_parent_customization_view` |
| N1b (P1) | 부모가 상대 `PYTHONPATH` 를 **자기 cwd** 로 풀고, **자기 `sys.path`** 를 child 의 검색 경로로 쓴다. child 는 재생 cwd(sandbox) 에서 뜬다. 보조 user-site 탐침도 cwd=ROOT | `_parent_customization_view` · `_parent_user_site_enabled` |
| N2b (P1) | 표준 namespace package(`__file__ None`) 를 `<absent>` 로 접고, 이력이 "올렸다" 고 하니 **모순 → failed**. 뒤의 unfiled 분기와 부모 주석은 namespace 를 정상으로 적는데 앞의 검사에서 먼저 막힌다 | `_ENV_PROBE_BODY` cust · history 검사 |
| T1 (P2) | 활성 대조군이 활성을 **만들지 않는다** — 환경변수 하나 지우고 가정. `pyvenv.cfg` 로 꺼진 일반 venv 에서 시험이 자기 전제에서 죽었다 (리뷰어 실측 1 failed) | `test_gate64_defensive.py` |
| E2-R 후속 | 실제 lifecycle 이 쓰는 token 탐침 `_kernel_lock_held(tok)` 은 True 쪽만 시험된다. 상수 True 로 바꿔도 커밋된 대조군 둘이 통과 (이 기계 실측: 리뷰어 `repro_e2_linux_NOT_RUN.py` baseline/mutated 전부 PASS) | `test_gate63_defensive.py` |

**세 상태를 가른다** — N1a 의 한 줄 요약이다: 비활성+미로드 · 비활성+정상 명시 로드 · 활성+자동
로드. 부모가 아는 것은 조건(활성 여부)과 **후보 바이트**(재생 검색 경로에서 resolver 가 찾는
것)이고, 무엇이 실제로 올라왔는지는 startup 이력이 증언한다. child 가 준 digest 를 정답으로
쓰지 않는다 — 후보와 같아야 하고, 이력과 어긋나면 거부한다.

**전제는 만들고 잰다** — T1 의 한 줄 요약. `tests/interpreter_fixture.py` 가 활성/비활성
venv 를 만들고 `site.ENABLE_USER_SITE` 를 실측한 뒤에야 시험이 돈다.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
for _p in (REPO, REPO / "tests", REPO / "docs" / "22p_gap"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from interpreter_fixture import (build_interpreter, make_interpreter,  # noqa: E402
                                 measured_user_site, use_interpreter)


def _mr():
    import mutation_replay as mr

    return mr


def _receipt_in(env_extra: dict, cwd: Path, python) -> dict:
    """탐침 본문을 **그 인터프리터로, 그 cwd 에서** 돌려 `_receipt_facts` 를 한 번 잰다."""
    mr = _mr()
    src = mr._ENV_PROBE_BODY + (
        "\nimport json\n"
        f"print(json.dumps(_receipt_facts({mr._probe_names()!r}, [], "
        f"{str(cwd)!r}), sort_keys=True, ensure_ascii=False))\n")
    env = dict(os.environ)
    env.pop("PYTHONNOUSERSITE", None)          # 조건은 인터프리터(venv)가 정한다
    env.setdefault("PYTHONHASHSEED", "0")      # 완전성 검사의 `env 가 비었다` 를 피한다
    env.update(env_extra)
    r = subprocess.run([str(python), "-c", src], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def _pin_env(monkeypatch, extra: dict) -> None:
    """부모와 child 가 **같은 env** 를 보게 한다 — 둘 다 `replay_env()` 를 부른다."""
    mr = _mr()
    base = dict(mr.replay_env())
    base.pop("PYTHONNOUSERSITE", None)
    base.update(extra)
    monkeypatch.setattr(mr, "replay_env", lambda: dict(base))


def _digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


@pytest.fixture
def on(tmp_path_factory):
    """user site **활성** 인터프리터 — 만들고 실측한다 (T1)."""
    return make_interpreter(tmp_path_factory.mktemp("interp-on"), user_site=True)


@pytest.fixture
def off(tmp_path_factory):
    """user site **비활성** 인터프리터 — 일반 venv 와 같은 조건."""
    return make_interpreter(tmp_path_factory.mktemp("interp-off"), user_site=False)


# ── T1 · 전제는 만들고 잰다 ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("user_site", [True, False])
def test_the_interpreter_fixture_measures_its_own_premise(tmp_path, user_site):
    """★ T1 — fixture 가 **만든** 인터프리터의 `ENABLE_USER_SITE` 가 **실측으로** 기대와
    같다. 여기서는 검증 없는 `build_interpreter` 를 쓴다 — `make_interpreter` 의 skip 이
    "못 만들었다" 를 가리지 않게. venv 의 활성 조건(`--system-site-packages`)을 빼먹는
    변이는 [True] 가 `assert False is True` 로 빨개진다."""
    py = build_interpreter(tmp_path, user_site=user_site)
    assert measured_user_site(py) is user_site


def test_an_enabled_interpreter_compares_usercustomize_bytes(tmp_path, monkeypatch, on):
    """★ T1 — 64차의 활성 대조군을 **명시 fixture** 위에서. 활성이면 자동 import 된
    usercustomize 의 바이트를 계속 댄다 — 바꾸면 거부. 이 시험은 `on` 이 실제로 활성인
    인터프리터에서만 돈다 (fixture 가 전제를 못 만들면 skip 이유에 그렇게 적힌다)."""
    site = tmp_path / "site"
    site.mkdir()
    uc = site / "usercustomize.py"
    uc.write_text("# 진짜로 올라간다\n", encoding="utf-8")
    use_interpreter(monkeypatch, on)
    _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()

    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, on)
    child = got["startup"]["customization"]["usercustomize"]
    print("child usercustomize:", child)
    assert child == _digest(uc), (
        "활성 인터프리터인데 child 가 usercustomize 를 안 올렸다 — 전제가 깨졌다")
    mr._assert_customization_matches_parent(got)

    uc.write_text("# 다른 바이트\n", encoding="utf-8")     # 세탁을 흉내낸다
    with pytest.raises(mr._ReplayError, match="usercustomize"):
        mr._assert_customization_matches_parent(got)


# ── N1a · 자동 import 비활성 ≠ 명시 import 부재 ─────────────────────────────────────

def _explicit_import_site(tmp_path: Path) -> Path:
    """정상 `sitecustomize` 가 `usercustomize` 를 **평범하게** import 한다 (리뷰어 원문)."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text("import usercustomize\n", encoding="utf-8")
    (site / "usercustomize.py").write_text("# ordinary user customization\nVALUE = 42\n",
                                           encoding="utf-8")
    return site


def test_a_disabled_interpreter_with_an_explicit_import_is_accepted(tmp_path, monkeypatch, off):
    """★ N1a — 비활성 + 정상 명시 로드. child 는 진짜 digest 를 내고 이력도 올렸다고
    증언한다. 부모가 조건만 보고 `<absent>` 를 기대하면 정상 영수증을 거부한다."""
    site = _explicit_import_site(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()

    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, off)
    cust = got["startup"]["customization"]
    print("customization:", cust)
    assert cust["usercustomize"] == _digest(site / "usercustomize.py"), (
        "비활성인데 명시 import 가 안 올라갔다 — 전제가 깨졌다")
    assert "usercustomize" in got["startup"]["startup_history"]["modules"], (
        "이력이 명시 import 를 못 봤다")
    try:
        mr._assert_customization_matches_parent(got)
    except mr._ReplayError:
        raise AssertionError(
            "user site 가 꺼졌어도 정상 sitecustomize 의 `import usercustomize` 는 평범한 "
            "import 다 — 부모가 그 영수증을 거부했다 (G65-N1a)") from None


def test_a_disabled_explicit_import_with_changed_bytes_is_rejected(tmp_path, monkeypatch, off):
    """N1a 대조군 — 수용이 **무조건**이 아니다. 같은 상태에서 바이트를 바꾸면 거부."""
    site = _explicit_import_site(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, off)
    (site / "usercustomize.py").write_text("VALUE = 43\n", encoding="utf-8")
    with pytest.raises(mr._ReplayError, match="usercustomize"):
        mr._assert_customization_matches_parent(got)


def test_a_disabled_interpreter_that_did_not_load_usercustomize_stays_absent(
        tmp_path, monkeypatch, off):
    """N1a 대조군 — 비활성 + 미로드 (64차 N1 의 원 사례를 명시 fixture 위에서).
    후보는 있지만 아무도 import 하지 않았다 → 양쪽 `<absent>`, 수용."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "usercustomize.py").write_text("# 아무도 안 부른다\n", encoding="utf-8")
    use_interpreter(monkeypatch, off)
    _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, off)
    assert got["startup"]["customization"]["usercustomize"] == "<absent>"
    mr._assert_customization_matches_parent(got)


def test_a_disabled_receipt_claiming_absent_while_history_loaded_it_is_rejected(
        tmp_path, monkeypatch, off):
    """★ N1a 의 다른 쪽 — 세 상태를 가르면 **`<absent>` 도 무조건 수용이 아니다.**
    이력이 "usercustomize 를 올렸다" 고 증언하는데 customization 이 `<absent>` 인 영수증은
    어긋난 증거다. 부모가 "비활성 = absent" 등식으로 보면 이 세탁본을 받는다."""
    site = _explicit_import_site(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, off)
    assert "usercustomize" in got["startup"]["startup_history"]["modules"]
    got["startup"]["customization"]["usercustomize"] = "<absent>"          # 세탁본
    with pytest.raises(mr._ReplayError, match="usercustomize"):
        mr._assert_customization_matches_parent(got)


# ── N1b · 재생 문맥 (cwd · 검색 경로) 은 하나다 ─────────────────────────────────────

def _two_cwds(tmp_path: Path) -> tuple[Path, Path]:
    """재생 cwd 와 호출자 cwd 에 **서로 다른 정상 파일**을 같은 상대 경로로 둔다."""
    child = tmp_path / "child"
    (child / "startup").mkdir(parents=True)
    (child / "startup" / "sitecustomize.py").write_text(
        "# 재생 cwd 의 정상 startup\n", encoding="utf-8")
    caller = tmp_path / "caller"
    (caller / "startup").mkdir(parents=True)
    (caller / "startup" / "sitecustomize.py").write_text(
        "# 호출자 cwd 의 다른 정상 파일\n", encoding="utf-8")
    return child, caller


def test_a_relative_pythonpath_is_resolved_in_the_replay_cwd(tmp_path, monkeypatch, off):
    """★ N1b — `PYTHONPATH=startup` (상대). child 는 자기 cwd 로 푼다. 부모가 호출자
    cwd 로 풀면 다른 정상 파일의 digest 를 기대해 정상 영수증을 거부한다."""
    child, caller = _two_cwds(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin_env(monkeypatch, {"PYTHONPATH": "startup"})
    monkeypatch.chdir(caller)
    mr = _mr()

    got = _receipt_in({"PYTHONPATH": "startup"}, child, off)
    assert got["startup"]["customization"]["sitecustomize"] == _digest(
        child / "startup" / "sitecustomize.py"), "child 가 자기 cwd 로 풀지 않았다"
    ctx = mr._replay_context(child)
    try:
        mr._assert_customization_matches_parent(got, ctx)
    except mr._ReplayError:
        raise AssertionError(
            "부모가 상대 PYTHONPATH 를 호출자 cwd 로 풀었다 — 재생 문맥이 둘이다 (G65-N1b)"
        ) from None


def test_the_real_entry_point_accepts_a_relative_pythonpath_from_another_cwd(
        tmp_path, monkeypatch, off):
    """★ N1b — 같은 축을 **실제 진입점** `_execution_receipt()` 에서 (리뷰어는 여기서
    재현했다). 재생 root 는 child, 호출자 cwd 는 caller."""
    child, caller = _two_cwds(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin_env(monkeypatch, {"PYTHONPATH": "startup"})
    monkeypatch.chdir(caller)
    mr = _mr()
    monkeypatch.setattr(mr, "_sandboxed", lambda p: child)      # 재생 root = child
    try:
        rec = mr._execution_receipt()
    except mr._ReplayError:
        raise AssertionError(
            "실제 진입점이 상대 PYTHONPATH 의 정상 영수증을 거부했다 (G65-N1b)") from None
    assert rec["startup"]["customization"]["sitecustomize"] == _digest(
        child / "startup" / "sitecustomize.py")


def test_the_parents_sys_path_is_not_the_childs_search_path(tmp_path, monkeypatch, on):
    """★ N1b — 부모 pytest 가 `sys.path` 에 얹은 자리는 child 의 검색 경로가 아니다.
    거기에만 `usercustomize.py` 를 두면 child 는 `<absent>` 다 — 부모가 그것을 기대하면
    정상 영수증을 거부한다."""
    only_parent = tmp_path / "only-parent"
    only_parent.mkdir()
    (only_parent / "usercustomize.py").write_text("# 부모 pytest 만 보는 자리\n",
                                                  encoding="utf-8")
    monkeypatch.syspath_prepend(str(only_parent))
    empty = tmp_path / "empty"
    empty.mkdir()
    use_interpreter(monkeypatch, on)
    _pin_env(monkeypatch, {"PYTHONPATH": str(empty)})
    mr = _mr()

    got = _receipt_in({"PYTHONPATH": str(empty)}, tmp_path, on)
    print("customization:", got["startup"]["customization"])
    assert got["startup"]["customization"]["usercustomize"] == "<absent>", (
        "child 검색 경로에 없는 모듈이 올라왔다 — 이 기계의 user site 에 usercustomize 가 "
        "있다면 이 대조군은 잴 수 없다")
    try:
        mr._assert_customization_matches_parent(got)
    except mr._ReplayError:
        raise AssertionError(
            "부모가 자기 sys.path 의 usercustomize 를 child 것으로 기대했다 (G65-N1b)") from None


# ── N2b · 정상 namespace 는 미로드도 읽기 실패도 아니다 ────────────────────────────────

def _namespace_site(tmp_path: Path, name: str, tag: str = "site") -> Path:
    """`__init__.py` 없는 빈 디렉터리 — Python 은 표준 namespace package 로 import 한다."""
    site = tmp_path / tag
    site.mkdir()
    (site / name).mkdir()
    return site


def test_a_namespace_usercustomize_is_measured_and_accepted(tmp_path, monkeypatch, on):
    """★ N2b — 활성 인터프리터가 namespace `usercustomize` 를 올린다 (`__file__ None`).
    이것은 로드된 코드 없는 module 이다 — `<absent>` 도, `failed` 도 아니다.

    (이 기계에서 `sitecustomize` 는 stdlib 자리의 일반 파일이 namespace 를 가리므로 —
    Python 은 정규 module 을 먼저 찾는다 — 자유로운 이름 `usercustomize` 로 만든다.)"""
    site = _namespace_site(tmp_path, "usercustomize")
    use_interpreter(monkeypatch, on)
    _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()

    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, on)
    st = got["startup"]
    # 증인 문구는 **기계 독립**이어야 한다 — production 의 reason·digest 를 assert 문구에
    # 싣지 않는다 (64차 ① 회차의 교훈). 관측값은 stdout 으로만 남긴다.
    print("startup:", json.dumps(st.get("startup_history"), ensure_ascii=False)[:400])
    assert st.get("status") == "measured", "정상 namespace customization 이 startup 을 failed 로 만든다 (G65-N2b)"
    assert st["startup_history"].get("status") == "measured", (
        "정상 namespace customization 이 이력을 failed 로 만든다 (G65-N2b)")
    assert st["customization"]["usercustomize"].startswith("<namespace>"), (
        "namespace 가 <absent> 로 접혔다 (G65-N2b)")
    mr._assert_receipt_is_complete(got)
    mr._assert_customization_matches_parent(got)


def test_a_namespace_identity_is_bound_to_its_search_locations(tmp_path, monkeypatch, on):
    """★ N2b — namespace 의 identity 는 **종류 + 검색 위치**다 (리뷰어 최소 종결 조건).
    다른 자리의 빈 디렉터리는 다른 값이어야 한다 — 그렇지 않으면 "origin 없는 모듈은
    전부 같다" 가 되어 위치를 바꿔도 영수증이 안 움직인다."""
    a = _namespace_site(tmp_path, "usercustomize", "a")
    b = _namespace_site(tmp_path, "usercustomize", "b")
    use_interpreter(monkeypatch, on)
    mr = _mr()
    values = []
    for site in (a, b):
        _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
        got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, on)
        v = got["startup"]["customization"]["usercustomize"]
        assert v.startswith("<namespace>"), v
        mr._assert_customization_matches_parent(got)
        values.append(v)
    assert values[0] != values[1], ("두 자리의 namespace 가 같은 identity 다", values)


def test_a_loaded_customization_without_any_origin_is_failed_not_absent(
        tmp_path, monkeypatch, off):
    """★ N2b 의 금지 조건 — "origin 없는 module 은 전부 정상" 이 아니다. startup 코드가
    `sys.modules['usercustomize']` 에 빈 ModuleType 을 심으면 그것은 올라와 있는데
    파일도 검색 위치도 없다 — **못 잰 것**이고 typed `failed` 여야 한다."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(
        "import sys, types\n"
        "sys.modules['usercustomize'] = types.ModuleType('usercustomize')\n",
        encoding="utf-8")
    use_interpreter(monkeypatch, off)
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path, off)
    print("customization:", got["startup"].get("customization"))
    assert got["startup"].get("status") == "failed", (
        "origin 도 검색 위치도 없는 module 이 정상으로 통과했다 (G65-N2b 금지 조건)")


def test_a_zip_customization_and_an_unreadable_one_keep_their_own_reasons(
        tmp_path, monkeypatch, off):
    """N2b 대조군 — 네 축(일반 파일 · ZIP · namespace · 읽기 실패)이 **각자 자기 이유**로
    검사된다. ZIP 은 hex16 이고 읽기 실패는 여전히 `failed` 다 (64차 회귀와 같은 축을
    같은 fixture 인터프리터로 한 번 더)."""
    import zipfile

    z = tmp_path / "startup.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("sitecustomize/__init__.py", "# 주석 한 줄뿐\n")
    use_interpreter(monkeypatch, off)
    _pin_env(monkeypatch, {"PYTHONPATH": str(z)})
    mr = _mr()
    got = _receipt_in({"PYTHONPATH": str(z)}, tmp_path, off)
    assert got["startup"]["status"] == "measured", got["startup"]
    assert mr._HEX16.fullmatch(got["startup"]["customization"]["sitecustomize"]), (
        got["startup"]["customization"])
    mr._assert_customization_matches_parent(got)

    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "sitecustomize.py").write_text(
        "import sys\nsys.modules[__name__].__file__ = __file__ + '.사라진'\n",
        encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(bad)}, tmp_path, off)
    assert got["startup"].get("status") == "failed", got["startup"].get("status")


# ── E2-R 후속 · 실제로 쓰는 token 탐침의 음성 ─────────────────────────────────────────

linux_only = pytest.mark.skipif(sys.platform != "linux", reason="fcntl.flock 이 필요하다")


@linux_only
def test_the_token_probe_goes_false_on_the_same_live_token(tmp_path):
    """E2-R 후속 대조군 — 같은 token · 같은 inode 에서 `LOCK_UN` 하면 token 탐침이 False.
    (리뷰어 후속 스크립트의 baseline 과 같은 관측 — 이 기계 실측 `[true, false]`.)"""
    import fcntl

    import src.io as io
    from test_gate63_defensive import _kernel_lock_held

    d = tmp_path / "d"
    d.mkdir()
    tok = io.acquire_run_lock(d, ".fit.lock")
    try:
        assert _kernel_lock_held(tok) is True
        fcntl.flock(tok.fd, fcntl.LOCK_UN)
        assert _kernel_lock_held(tok) is False           # ★ token 판의 음성
        fcntl.flock(tok.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        assert _kernel_lock_held(tok) is True
    finally:
        io.release_run_lock(tok)


@linux_only
def test_a_constant_true_token_probe_is_caught_by_the_committed_control(tmp_path, monkeypatch):
    """★ E2-R 후속 — 실제 lifecycle 이 부르는 것은 `_kernel_lock_held(tok)` 이다. 그것을
    상수 True 로 바꾸면 **커밋된 대조군이 빨개져야** 한다. 리뷰어 실측(이 기계 재실행):
    바꿔도 대조군 둘이 PASS — 경로 판(`_at`)만 음성을 갖고 있었다."""
    import test_gate63_defensive as g63

    monkeypatch.setattr(g63, "_kernel_lock_held", lambda tok: True)
    (tmp_path / "a").mkdir()                      # 대조군은 자기 tmp_path 아래 d/ 를 만든다
    with pytest.raises(AssertionError):
        g63.test_the_kernel_lock_probe_itself_is_not_vacuous(tmp_path / "a")


def test_the_committed_control_asserts_the_token_probe_negative():
    """정적 대조 — 커밋된 대조군에 `_kernel_lock_held(tok) is False` 가 **있다**.
    64차 AST 시험은 `is True`/`is False` 의 존재만 봤고 어느 탐침의 것인지는 안 봤다."""
    src = (REPO / "tests" / "test_gate63_defensive.py").read_text(encoding="utf-8")
    fn = next((n for n in ast.walk(ast.parse(src))
               if isinstance(n, ast.FunctionDef)
               and n.name == "test_the_kernel_lock_probe_itself_is_not_vacuous"), None)
    assert fn is not None
    token_outcomes = []
    for node in ast.walk(fn):
        if (isinstance(node, ast.Compare) and isinstance(node.ops[0], ast.Is)
                and isinstance(node.left, ast.Call)
                and isinstance(node.left.func, ast.Name)
                and node.left.func.id == "_kernel_lock_held"):
            c = node.comparators[0]
            if isinstance(c, ast.Constant) and isinstance(c.value, bool):
                token_outcomes.append(c.value)
    assert False in token_outcomes, (
        "커밋된 대조군이 token 탐침의 음성을 고정하지 않는다 (E2-R 후속)", token_outcomes)
