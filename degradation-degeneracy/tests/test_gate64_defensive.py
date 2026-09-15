"""64차 방어적 검토 (대상 `743f65b` · 검토 HEAD `6f8dcc2`) — N1 · N2 · E2-R.

리뷰어 발견 셋. 전부 **정상 입력**에서 우리 층이 거부하거나 실패한 것이고, 위조 성공이
아니다 — 그래서 고칠 방향은 "덜 본다" 가 아니라 "같은 규칙으로 본다" 다.

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| N1 (P1) | 부모가 `usercustomize` 를 **무조건** 찾는다. Python 은 `site.ENABLE_USER_SITE` 가 참일 때만 그것을 자동 import 한다 — 정상 venv(user site 비활성)에서 child 는 `<absent>` 인데 부모는 digest 를 내서 정상 영수증이 거부된다 | `_parent_customization_view` |
| N2 (P1) | child 의 customization 해시가 `_hash_origin` 이 아니라 `_d(f)` 를 부른다 — ZIP 안의 정상 `sitecustomize` package 를 OS 파일로 열려다 `[Errno 20] Not a directory` 로 `failed` | `_env_facts_measured` |
| E2-R (P2) | 탐침 대조군이 `is True` 만 고정한다. 원장은 "잡으면 True · 놓으면 False" 라고 적었다 | `tests/test_gate63_defensive.py` |

**찾을 수 있는 모듈 ≠ startup 이 실행한 모듈.** N1 의 한 줄 요약이고, 고침도 그 문장대로다 —
부모가 **자기 인터프리터를 같은 env 로 띄워** 활성 조건을 재고, 그 조건을 판정에 반영한다.
child 의 자기 증언을 믿는 것이 아니다 (활성이면 바이트 대조는 그대로 산다).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO / "docs" / "22p_gap") not in sys.path:
    sys.path.insert(0, str(REPO / "docs" / "22p_gap"))


def _mr():
    import mutation_replay as mr

    return mr


def _receipt_in(env_extra: dict, cwd: Path) -> dict:
    """탐침 본문을 그대로 돌려 `_receipt_facts` 를 한 번 잰다 (62차 시험과 같은 헬퍼)."""
    mr = _mr()
    src = mr._ENV_PROBE_BODY + (
        "\nimport json\n"
        f"print(json.dumps(_receipt_facts({mr._probe_names()!r}, [], "
        f"{str(cwd)!r}), sort_keys=True, ensure_ascii=False))\n")
    env = dict(os.environ)
    env.update(env_extra)
    r = subprocess.run([sys.executable, "-c", src], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def _pin_env(monkeypatch, extra: dict) -> None:
    """부모와 child 가 **같은 env** 를 보게 한다 — 둘 다 `replay_env()` 를 부른다."""
    mr = _mr()
    base = dict(mr.replay_env())
    base.update(extra)
    monkeypatch.setattr(mr, "replay_env", lambda: dict(base))


# ── N1 · usercustomize 의 실행 활성 조건 ──────────────────────────────────────────────────

def test_a_child_with_user_site_disabled_matches_the_parent(tmp_path, monkeypatch):
    """★ N1 — user site 가 꺼진 정상 인터프리터에서 **양쪽이 `<absent>`** 여야 한다.

    Python 은 `site.ENABLE_USER_SITE` 가 참일 때만 `usercustomize` 를 자동 import 한다.
    부모가 그 조건을 안 보고 resolver 로만 찾으면, PYTHONPATH 에 놓인 정상 모듈 하나가
    **정상 영수증을 거부**하게 만든다 (리뷰어 실측: child `<absent>` · parent digest).
    """
    site = tmp_path / "site"
    site.mkdir()
    (site / "usercustomize.py").write_text("# 주석 한 줄뿐\n", encoding="utf-8")
    _pin_env(monkeypatch, {"PYTHONPATH": str(site), "PYTHONNOUSERSITE": "1"})
    mr = _mr()

    got = _receipt_in({"PYTHONPATH": str(site), "PYTHONNOUSERSITE": "1"}, tmp_path)
    assert got["startup"]["customization"]["usercustomize"] == "<absent>", (
        "child 가 안 올린 것을 올렸다고 적는다", got["startup"]["customization"])
    want = mr._parent_customization_view()
    # 증인 문구는 **기계 독립**이어야 한다 — digest 도 tmp 경로도 담지 않는다
    # (62차 ① 회차 · 63차 ① 회차가 같은 자리에서 조각 재생을 깨뜨렸다).
    assert want["usercustomize"] == "<absent>", (
        "부모가 startup 이 실행하지 않는 모듈의 digest 를 낸다 (N1)")


def test_a_disabled_user_site_receipt_passes_the_parent_assertion(tmp_path, monkeypatch):
    """같은 축을 **집행 지점**에서 — 정상 영수증이 거부되지 않아야 한다."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "usercustomize.py").write_text("# 주석 한 줄뿐\n", encoding="utf-8")
    _pin_env(monkeypatch, {"PYTHONPATH": str(site), "PYTHONNOUSERSITE": "1"})
    mr = _mr()
    got = _receipt_in({"PYTHONPATH": str(site), "PYTHONNOUSERSITE": "1"}, tmp_path)
    mr._assert_customization_matches_parent(got)          # 예외가 나면 그것이 발견이다


def test_an_enabled_user_site_still_compares_the_bytes(tmp_path, monkeypatch):
    """대조군 — **활성이면** 실제 바이트를 계속 댄다. usercustomize 를 통째로 무시하는
    수정이면 이 시험이 통과하지 못한다 (리뷰어 최소 종결 조건 3)."""
    site = tmp_path / "site"
    site.mkdir()
    uc = site / "usercustomize.py"
    uc.write_text("# 진짜로 올라간다\n", encoding="utf-8")
    env = {"PYTHONPATH": str(site)}
    env.pop("PYTHONNOUSERSITE", None)
    _pin_env(monkeypatch, env)
    monkeypatch.delenv("PYTHONNOUSERSITE", raising=False)
    mr = _mr()

    got = _receipt_in(env, tmp_path)
    child = got["startup"]["customization"]["usercustomize"]
    assert child != "<absent>", ("user site 가 켜진 환경인데 child 가 안 올렸다 — "
                                 "이 기계에서는 이 대조군을 잴 수 없다", child)
    assert mr._parent_customization_view()["usercustomize"] == child
    mr._assert_customization_matches_parent(got)

    uc.write_text("# 다른 바이트\n", encoding="utf-8")     # 세탁을 흉내낸다
    with pytest.raises(mr._ReplayError, match="customization"):
        mr._assert_customization_matches_parent(got)


# ── N2 · ZIP 안의 customization ───────────────────────────────────────────────────────────

def _zip_customization(tmp_path: Path) -> Path:
    z = tmp_path / "ordinary_startup.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("sitecustomize/__init__.py", "# 주석 한 줄뿐\n")
    return z


def test_a_zip_customization_is_measured_not_failed(tmp_path, monkeypatch):
    """★ N2 — 표준 zipimport 의 정상 package 가 `failed` 를 만든다.

    child 의 customization 루프만 `_d(f)` 를 부른다 — ZIP 안의 논리 경로를 OS 파일로
    열어 `[Errno 20] Not a directory`. 바로 위의 `loaded` 루프는 이미 `_hash_origin`
    으로 loader 에게 묻는다. **같은 origin 을 두 규칙으로 읽고 있었다.**
    """
    z = _zip_customization(tmp_path)
    _pin_env(monkeypatch, {"PYTHONPATH": str(z)})
    mr = _mr()

    got = _receipt_in({"PYTHONPATH": str(z)}, tmp_path)
    assert got["startup"]["status"] == "measured", (
        "정상 ZIP customization 이 영수증을 실패시킨다 (N2)", got["startup"]["status"])
    child = got["startup"]["customization"]["sitecustomize"]
    assert child != "<absent>", ("ZIP customization 이 없는 것으로 적혔다", child)
    assert mr._parent_customization_view()["sitecustomize"] == child, (
        "부모는 loader 로 읽고 child 는 파일로 읽는다 — 규칙이 두 벌이다")
    mr._assert_customization_matches_parent(got)


def test_a_plain_file_customization_still_works(tmp_path, monkeypatch):
    """대조군 셋 중 하나 — 일반 파일 customization (리뷰어 최소 종결 조건 2)."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text("# 일반 파일\n", encoding="utf-8")
    _pin_env(monkeypatch, {"PYTHONPATH": str(site)})
    mr = _mr()
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path)
    assert got["startup"]["status"] == "measured", got["startup"]
    mr._assert_customization_matches_parent(got)


def test_a_plain_customization_importing_a_zip_module_still_works(tmp_path, monkeypatch):
    """대조군 셋 중 둘 — 일반 customization 이 ZIP module 을 가져오는 축 (62차 P1-4 가
    이미 덮던 것). 이것만 통과해서 N2 가 안 드러났다."""
    site = tmp_path / "site"
    site.mkdir()
    z = tmp_path / "mods64.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("zipmod_64.py", "VALUE = 'FROM_ZIP'\n")
    (site / "sitecustomize.py").write_text("import zipmod_64\n", encoding="utf-8")
    pp = str(site) + os.pathsep + str(z)
    _pin_env(monkeypatch, {"PYTHONPATH": pp})
    got = _receipt_in({"PYTHONPATH": pp}, tmp_path)
    assert got["startup"]["status"] == "measured", got["startup"]
    assert "zipmod_64" in got["startup"]["startup_history"]["modules"]


def test_an_unreadable_customization_origin_is_still_failed(tmp_path, monkeypatch):
    """대조군 — **진짜 읽기 실패는 계속 typed `failed`** 다. 예외를 `<absent>` 로 바꿔
    정상으로 취급하는 수정이면 이 시험이 잡는다 (리뷰어 최소 종결 조건 3).

    startup 코드가 자기 `__file__` 을 없는 경로로 갈아 끼우면, 파일도 아니고 loader 도
    그 이름의 바이트를 못 준다 — 그것이 `_Unreadable` 이고 섹션 전체가 `failed` 다.
    """
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(
        "import sys\n"
        "sys.modules[__name__].__file__ = __file__ + '.사라진'\n", encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path)
    assert got["startup"].get("status") == "failed", got["startup"].get("status")
    assert "<absent>" not in json.dumps(got.get("startup", {}).get("customization", {})), got


# ── E2-R · 탐침 대조군의 음성 assertion ───────────────────────────────────────────────────

def test_the_committed_probe_control_asserts_both_directions():
    """★ E2-R — 원장은 "잡으면 True · 놓으면 False" 라고 적었는데 커밋된 시험에는
    True 만 있었다. 리뷰어의 정적 대조를 그대로 회귀로 고정한다 — 구현의 False 분기가
    이 기계에서 동작하는 것과 **커밋된 회귀가 그것을 강제하는 것**은 다른 문제다."""
    import ast

    src = (REPO / "tests" / "test_gate63_defensive.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef)
               and n.name == "test_the_kernel_lock_probe_itself_is_not_vacuous"), None)
    assert fn is not None, "탐침 대조군 시험이 없다"
    outcomes = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Compare) and isinstance(node.ops[0], ast.Is):
            c = node.comparators[0]
            if isinstance(c, ast.Constant) and isinstance(c.value, bool):
                outcomes.append(c.value)
    assert True in outcomes and False in outcomes, (
        "커밋된 대조군이 한쪽만 고정한다 — 원장 문구가 시험보다 강하다 (E2-R)", outcomes)


def test_the_kernel_lock_probe_control_actually_runs_both_directions(tmp_path):
    """정적 대조만으로는 부족하다 — 그 두 방향을 **실제로 관측**한다."""
    import src.io as io
    sys.path.insert(0, str(REPO / "tests"))
    from test_gate63_defensive import _kernel_lock_held, _kernel_lock_held_at

    d = tmp_path / "d"
    d.mkdir()
    p = d / ".fit.lock"
    tok = io.acquire_run_lock(d, ".fit.lock")
    held_tok, held_path = _kernel_lock_held(tok), _kernel_lock_held_at(p)
    io.release_run_lock(tok)                 # token 의 dir_fd 를 닫고 파일을 지운다
    gone = not p.exists()
    p.touch()                                # 같은 자리를 아무도 안 잡은 상태로
    unheld = _kernel_lock_held_at(p)
    assert (held_tok, held_path, gone, unheld) == (True, True, True, False), (
        held_tok, held_path, gone, unheld)


def test_the_outside_repo_xfail_names_its_error(tmp_path):
    """리뷰어의 후속 정리 제안 — `raises=Exception` 은 **다른 이유로 죽어도** xfail 로
    분류한다. §0 ⑦ 이 주장하는 오류는 `shutil.SameFileError` 하나다."""
    import ast

    src = (REPO / "tests" / "test_gate63_defensive.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef)
               and n.name.startswith("test_staging_an_input_outside_the_repo")), None)
    assert fn is not None, "§0 ⑦ 의 xfail 시험이 없다"
    raises = None
    for dec in fn.decorator_list:
        for kw in getattr(dec, "keywords", []):
            if kw.arg == "raises":
                raises = ast.unparse(kw.value)
    assert raises and "Exception" != raises, (
        "xfail 이 모든 예외를 §0 ⑦ 로 분류한다 — 축이 흐려진다", raises)
    assert "SameFileError" in raises, raises
