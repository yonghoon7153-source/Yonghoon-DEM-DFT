"""67차 방어적 검토 (대상 HEAD `cdc49e91` · `source_digest e9ee7475dea7de1d`) — G67-N1 · N2 · T1.

66차의 원 반례 셋(A 읽지 않은 cwd 파일 · B 자기 경로 정리 · C 후보 재정렬)은 **닫혔다고
인정받았다**. 그런데 고치면서 세 자리가 남았다 — 전부 *이미 측정한 사실을 실제 판정과 실행
증거에 끝까지 연결하지 않은* 종류다.

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| G67-N1 (P1) | **부재 위조의 마지막 방어가 `auto` 다.** user site 가 꺼져 있으면 `auto=False` 이고, 표준 namespace 는 파일 이력(`modules`)에도 안 잡힌다 → 부모가 **올라와 있다고 잰** 이름을 child 가 `<absent>` 라 적어도 통과한다. 자동 import 정책과 "실제로 올라왔는가" 는 다른 사실이다 | `mutation_replay.py` `_assert_customization_matches_parent` |
| G67-N2 (P1) | **ZIP 분기에는 사후 `sys.path` 재탐색이 남아 있다.** 파일 아닌 origin 을 `PathFinder.find_spec(n, [dirname(origin)] + search_path)` 로 다시 찾는데, ZIP **package** 의 `dirname(origin)` 은 archive root 가 아니라 `archive.zip/sitecustomize` 다. 정상 startup 이 자기 archive 를 경로에서 빼면 **정상 영수증이 거부**된다 (fail-open 이 아니라 false rejection) | `mutation_replay.py` `_parent_customization_view` |
| G67-T1 (P2) | 전제 회귀의 assertion 이 `"failed" not in stdout` 하나다 → child pytest 가 **사용법 오류(rc 4)** 로 끝나거나 **수집만 하고 실행 0건**이어도 초록이다. `rc 0` 만 더해도 두 번째는 남는다 | `tests/test_gate66_defensive.py::_premise_run` |
| G67-T1-b (P2) | 등록 변이 `the-premise-uses-a-controlled-env-g66` 의 witness 에 `stdout[-600:]` 에서 **우연히 잘린 꼬리**(`도 기대와 다르면 그때는`)가 들어 있다 — 기계가 바뀌면 안 맞는다 | `mutation_replay.py` MUTANTS |

**한 줄 요약**: *잰 것*과 *판정하는 것*을 잇지 않았다 (N1 `auto` · N2 사후 재탐색) · *시험이
돌았다는 것*과 *초록이라는 것*을 잇지 않았다 (T1 · T1-b).

리뷰어 재현기(`docs/22p_gap/gate67_review/codex/repro_boundaries.py` ·
`repro_premise_no_execution.py`)를 이 Linux 에서 **수정 없이** 먼저 돌려 셋이 모두 재현되는
것을 확인했다:

```
namespace_explicit_off   honest ACCEPTED · forged_actual_entry **ACCEPTED**   ← N1
namespace_explicit_on    honest ACCEPTED · forged REJECTED                     (대조군)
zip_package_remove_path  complete ACCEPTED · entry **REJECTED**               ← N2
zip_package_plain · zip_module_remove_path   entry ACCEPTED                    (대조군)
premise_pytest_usage_error   child rc 4 · stdout "" · committed test ACCEPTED ← T1
premise_collection_only      child rc 0 · call 0건 · committed test ACCEPTED  ← T1
```

그 관측을 아래 회귀로 고정한다.
"""
from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
for _p in (REPO, REPO / "tests", REPO / "docs" / "22p_gap"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from interpreter_fixture import make_interpreter, use_interpreter          # noqa: E402


def _mr():
    import mutation_replay as mr

    return mr


def _pin(monkeypatch, extra: dict) -> None:
    mr = _mr()
    base = dict(mr.replay_env())
    base.pop("PYTHONNOUSERSITE", None)
    base.update(extra)
    monkeypatch.setattr(mr, "replay_env", lambda: dict(base))


def _entry(monkeypatch, cwd: Path):
    mr = _mr()
    monkeypatch.setattr(mr, "_sandboxed", lambda p: cwd)
    return mr._execution_receipt()


def _replay_cwd(tmp_path: Path) -> Path:
    cwd = tmp_path / "replay"
    cwd.mkdir()
    return cwd


# ══════════════════════════════════════════════════════════════════════════════════
# G67-N1 — 부재 위조의 근거는 `auto` 가 아니라 **부모가 잰 loaded** 다
# ══════════════════════════════════════════════════════════════════════════════════

def _explicit_namespace(tmp_path: Path) -> Path:
    """리뷰어 fixture 그대로 — `sitecustomize.py` 가 빈 namespace `usercustomize/` 를 **명시 import**.

    `__init__.py` 가 없으므로 표준 namespace package 이고, origin 이 없으므로 startup 이력의
    파일 목록(`modules`)에도 잡히지 않는다. user site 가 꺼져 있어도 이것은 **평범한 import** 라
    실제로 올라온다 — 65차 N1a 가 가른 그 세 상태의 하나다.
    """
    start = tmp_path / "explicit-namespace"
    (start / "usercustomize").mkdir(parents=True)
    (start / "sitecustomize.py").write_text("import usercustomize\n", encoding="utf-8")
    return start


def test_g67_01_a_forged_absent_namespace_is_rejected_with_user_site_off(tmp_path, monkeypatch, off):
    """★ G67-N1 — **이번 라운드의 P1.** user site 가 꺼져 있고 namespace 가 명시 import 로
    올라온 상태에서, child 영수증의 `startup.customization.usercustomize` **한 칸만**
    `<absent>` 로 바꾼다. 부모는 그것이 올라와 있다고 **이미 쟀는데**, 마지막 방어가
    `elif auto and …` 라서 `auto=False` 인 이 조합을 빠져나간다 (리뷰어 실측 ACCEPTED).

    `auto` 는 "startup 이 자동으로 import 하는가" 이고, 지금 묻는 것은 "실제로 올라왔는가" 다.
    """
    start = _explicit_namespace(tmp_path)
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    ctx = mr._replay_context(cwd)
    rec = _entry(monkeypatch, cwd)
    assert rec["startup"]["customization"]["usercustomize"].startswith("<namespace>"), \
        ("전제가 깨졌다 — user site OFF 에서 명시 import 한 namespace 가 안 올라왔다",
         rec["startup"]["customization"])
    forged = copy.deepcopy(rec)
    forged["startup"]["customization"]["usercustomize"] = "<absent>"
    with pytest.raises(mr._ReplayError, match="usercustomize"):
        mr._assert_customization_matches_parent(forged, ctx)


def test_g67_02_the_honest_namespace_receipt_is_accepted_with_user_site_off(tmp_path, monkeypatch, off):
    """대조군(양성) — 같은 fixture 의 **정직한** 영수증은 계속 받아야 한다. "모든 OFF 를
    거부" 나 "namespace 전부 금지" 로 닫으면 여기서 잡힌다 (리뷰어의 금지 조건)."""
    start = _explicit_namespace(tmp_path)
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    _entry(monkeypatch, cwd)          # 예외가 없으면 통과다 (진입점 전체를 그대로 탄다)


def test_g67_03_a_genuinely_absent_name_is_still_accepted_with_user_site_off(tmp_path, monkeypatch, off):
    """대조군(양성) — OFF 이고 `usercustomize` 가 **정말로 없는** 정상 실행. 이때의 `<absent>`
    는 참이므로 계속 받아야 한다. N1 수정이 "OFF 면 무조건 거부" 로 가지 않았는지."""
    start = tmp_path / "plain"
    start.mkdir()
    (start / "sitecustomize.py").write_text("# 평범한 startup\n", encoding="utf-8")
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    rec = _entry(monkeypatch, cwd)
    assert rec["startup"]["customization"]["usercustomize"] == "<absent>", \
        rec["startup"]["customization"]


def test_g67_04_the_same_forgery_is_rejected_with_user_site_on(tmp_path, monkeypatch, on):
    """대조군 — ON 에서는 전 판도 거부했다 (`auto=True`). 수정이 이 축을 잃지 않았는지."""
    start = _explicit_namespace(tmp_path)
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, on)
    _pin(monkeypatch, {"PYTHONPATH": str(start)})
    mr = _mr()
    ctx = mr._replay_context(cwd)
    rec = _entry(monkeypatch, cwd)
    forged = copy.deepcopy(rec)
    forged["startup"]["customization"]["usercustomize"] = "<absent>"
    with pytest.raises(mr._ReplayError, match="usercustomize"):
        mr._assert_customization_matches_parent(forged, ctx)


# ══════════════════════════════════════════════════════════════════════════════════
# G67-N2 — ZIP 은 archive·member 로 읽는다 (사후 `sys.path` 재탐색 금지)
# ══════════════════════════════════════════════════════════════════════════════════

_CLEAN_PKG = ("import os, sys\n"
              "_arc = os.path.dirname(os.path.dirname(__file__))\n"
              "sys.path[:] = [p for p in sys.path\n"
              "               if os.path.normcase(os.path.normpath(p))\n"
              "               != os.path.normcase(os.path.normpath(_arc))]\n")
_CLEAN_MOD = ("import os, sys\n"
              "_arc = os.path.dirname(__file__)\n"
              "sys.path[:] = [p for p in sys.path\n"
              "               if os.path.normcase(os.path.normpath(p))\n"
              "               != os.path.normcase(os.path.normpath(_arc))]\n")


def _zip_startup(tmp_path: Path, name: str, member: str, body: str) -> Path:
    archive = tmp_path / (name + ".zip")
    with zipfile.ZipFile(archive, "x") as z:
        z.writestr(member, body)
    return archive


def test_g67_05_a_zip_package_that_removes_its_archive_is_accepted(tmp_path, monkeypatch, off):
    """★ G67-N2 — **이번 라운드의 두 번째 P1.** 표준 ZIP *package* 가 정상 로드된 뒤 자기
    archive 만 `sys.path` 에서 뺀다. 원본·archive·member 를 지우지 않았고 커스텀 loader 도 없다.
    child 는 그 바이트를 읽어 영수증을 만들었는데 부모가 거부한다 (리뷰어 실측 REJECTED).

    원인: `dirname(origin)` 은 archive root 가 아니라 `archive.zip/sitecustomize` 이고, 거기서
    top-level 이름 `sitecustomize` 를 다시 찾으면 그 package 가 아니다. archive root 는 이미
    final path 에서 빠졌다. **일반 파일 분기를 고친 것이 ZIP package 분기까지 고친 것은 아니다.**
    """
    archive = _zip_startup(tmp_path, "pkg_clean", "sitecustomize/__init__.py", _CLEAN_PKG)
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(archive)})
    _entry(monkeypatch, cwd)          # 예외가 없으면 통과다


def test_g67_06_a_zip_package_on_the_path_is_accepted(tmp_path, monkeypatch, off):
    """대조군 — 경로를 유지한 ZIP package 는 전 판도 받았다. 수정이 그것을 깨지 않았는지."""
    archive = _zip_startup(tmp_path, "pkg_plain", "sitecustomize/__init__.py",
                           "# standard ZIP startup\n")
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(archive)})
    _entry(monkeypatch, cwd)


def test_g67_07_a_zip_module_that_removes_its_archive_is_accepted(tmp_path, monkeypatch, off):
    """대조군 — 단일 module ZIP 은 `dirname(origin)` 이 우연히 archive root 라 전 판도 받았다.
    그 우연에 기대지 않는지 확인한다 (package 와 같은 경로로 통과해야 한다)."""
    archive = _zip_startup(tmp_path, "mod_clean", "sitecustomize.py", _CLEAN_MOD)
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(archive)})
    _entry(monkeypatch, cwd)


def test_g67_08_a_zip_whose_member_changed_after_the_run_is_rejected(tmp_path, monkeypatch, off):
    """대조군(음성) — **바이트 재확인은 유지**한다. 실행 뒤 archive 안의 member 를 갈아 끼우면
    부모가 읽는 바이트가 달라지므로 거부돼야 한다 (63차 F3 이 세운 성질)."""
    archive = _zip_startup(tmp_path, "pkg_tamper", "sitecustomize/__init__.py",
                           "# standard ZIP startup\n")
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(archive)})
    mr = _mr()
    ctx = mr._replay_context(cwd)
    rec = _entry(monkeypatch, cwd)
    with zipfile.ZipFile(archive, "w") as z:                 # 같은 이름, 다른 바이트
        z.writestr("sitecustomize/__init__.py", "# 갈아 끼운 바이트\n")
    with pytest.raises(mr._ReplayError, match="sitecustomize"):
        mr._assert_customization_matches_parent(rec, ctx)


def test_g67_09_a_zip_origin_whose_member_is_gone_is_rejected(tmp_path, monkeypatch, off):
    """대조군(음성) — archive 는 있는데 **그 member 가 없어지면** 읽을 수 없다 → 거부.
    "읽기 실패 거부" 를 유지하는지 (N2 수정이 fail-open 으로 가지 않았는지)."""
    archive = _zip_startup(tmp_path, "pkg_gone", "sitecustomize/__init__.py",
                           "# standard ZIP startup\n")
    cwd = _replay_cwd(tmp_path)
    use_interpreter(monkeypatch, off)
    _pin(monkeypatch, {"PYTHONPATH": str(archive)})
    mr = _mr()
    ctx = mr._replay_context(cwd)
    rec = _entry(monkeypatch, cwd)
    with zipfile.ZipFile(archive, "w") as z:                 # member 이름을 바꿔 버린다
        z.writestr("something_else.py", "# member 가 사라졌다\n")
    with pytest.raises(mr._ReplayError):
        mr._assert_customization_matches_parent(rec, ctx)


def test_g67_10_a_non_zip_unreadable_origin_is_still_rejected(tmp_path, monkeypatch, off):
    """대조군(음성) — 파일도 아니고 표준 archive 도 아닌 origin 은 계속 거부한다
    ("지원하는 표준 loader" 밖은 받지 않는다 — 임의 loader 를 부모가 실행하지 않는다)."""
    import site as _site

    mr = _mr()
    ctx = {"customization": {"site": {"loaded": True, "origin": _site.__file__, "locations": None},
                             "sitecustomize": {"loaded": True,
                                               "origin": "/nowhere/not-an-archive/sitecustomize.py",
                                               "locations": None},
                             "usercustomize": {"loaded": False, "origin": None, "locations": None}},
           "site_file": _site.__file__, "search_path": [], "user_site": False}
    with pytest.raises(mr._ReplayError, match="sitecustomize"):
        mr._parent_customization_view(ctx)


# ══════════════════════════════════════════════════════════════════════════════════
# G67-T1 — 시험이 **돌았다**는 증거 (rc·정확 node·call 단계)
# ══════════════════════════════════════════════════════════════════════════════════

def _committed_premise(env_extra: dict):
    """커밋된 전제 회귀를 **리뷰어와 똑같이** `(env_extra)` 하나로 부른다 — 그 호출 모양이
    외부 검토의 통로이므로 회귀가 그것을 고정한다 (인자를 늘리면 그쪽이 `TypeError` 가 된다)."""
    import test_gate66_defensive as tm

    return tm.test_g66_08_the_premise_test_does_not_fail_on_an_inherited_env(env_extra)


@pytest.mark.parametrize("addopts,why", [
    ("--g67-option-does-not-exist", "사용법 오류 — pytest rc 4 · stdout 빈 문자열"),
    ("--collect-only", "수집만 하고 실행 0건 — rc 0 이지만 call 단계가 없다"),
], ids=["usage_error", "collect_only"])
def test_g67_11_the_premise_regression_refuses_an_unrun_child(tmp_path, addopts, why):
    """★ G67-T1 — **실제 child pytest** 를 안 돌게 만들고, 전제 회귀의 검증부가 그것을 거부하는지
    묻는다. `subprocess` 를 가짜로 만들지 않는다 — 리뷰어가 그렇게 재현했고 우리도 그렇게 고정한다.

    전 판의 검증은 `"failed" not in stdout` 하나였고 두 경우 모두 초록이었다. 리뷰어가 짚은 대로
    **`rc 0` 검사만 더해도 `--collect-only` 는 남는다** — 그래서 정확한 두 node 가 call 단계를
    지났다는 기계 판독 증거를 요구한다.

    옵션을 `env_extra` 로 주는 이유: 고친 `_premise_run` 은 바깥 `PYTEST_ADDOPTS` 를 **걷어낸다**
    (그것이 G67-T1 의 다른 절반이고 `test_g67_13` 이 지킨다). 그래서 "안 돈 child" 를 만들려면
    우리가 **명시적으로** 그 env 를 넘겨야 한다 — 통로가 하나뿐이라는 것 자체가 경계의 증거다.
    """
    import test_gate66_defensive as tm

    junit = tmp_path / "premise.xml"
    r = tm._premise_run(sys.executable, {"PYTEST_ADDOPTS": addopts}, junit)
    with pytest.raises(AssertionError):
        tm.assert_premise_actually_ran(r, junit)


@pytest.mark.parametrize("env_extra", [{}, {"PYTHONNOUSERSITE": "1"}], ids=["clean", "nousersite"])
def test_g67_12_the_premise_regression_still_passes_in_a_clean_env(monkeypatch, env_extra):
    """대조군(양성) — 바깥이 깨끗하면 전제 회귀는 계속 통과해야 한다. T1 수정이 "전부 실패" 로
    가면 여기서 잡힌다."""
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)
    _committed_premise(env_extra)


@pytest.mark.parametrize("addopts", ["--collect-only", "--g67-option-does-not-exist"])
def test_g67_13_an_inherited_addopts_does_not_reach_the_child(monkeypatch, tmp_path, addopts):
    """★ G67-T1 의 나머지 절반 — **바깥이 child 의 옵션을 정하지 못한다.** 전 판은
    `dict(os.environ)` 을 그대로 물려줬다. 통제한 뒤에는 같은 바깥 env 로도 두 node 가 실제로
    돈다 (리뷰어 Q4: "env 이름을 하나씩 지우는 것만으로는 안 닫힌다" — 그래서 둘 다 본다)."""
    import test_gate66_defensive as tm

    monkeypatch.setenv("PYTEST_ADDOPTS", addopts)
    junit = tmp_path / "premise.xml"
    r = tm._premise_run(sys.executable, {}, junit)
    tm.assert_premise_actually_ran(r, junit)          # 예외가 없으면 경계가 샌 적이 없다


# ── T1-b — witness 는 **고정된 이유**여야 한다 ──────────────────────────────────

_WITNESS_SCAFFOLD = re.compile(r"^(AssertionError|Failed|_ReplayError):\s*")


def _unclosed_tail(body: str) -> str | None:
    """witness 안에서 **닫히지 않은 따옴표 뒤에 남은 글자** — 있으면 가변 값의 조각이다.

    이 저장소는 예전부터 "임시 경로처럼 실행마다 다른 값 **직전까지만** 적는다" 는 관행을
    쓴다 (`mountinfo-octal-escape-is-decoded` 의 주석). 그 관행은 따옴표에서 **끊는** 것이고
    (`… No such file or directory: '`), 끊은 뒤에 값의 일부를 **담는** 것은 다른 일이다.
    """
    quote = body.rfind("'")
    if quote < 0 or body.count("'") % 2 == 0:
        return None                                   # 균형이 맞으면 잘린 자리가 없다
    tail = body[quote + 1:]
    return tail or None


def test_g67_14_every_registered_witness_is_a_fixed_reason():
    """★ G67-T1-b — 등록 변이의 witness 가 **가변 출력의 꼬리**를 담으면 안 된다.

    리뷰어 실측: `the-premise-uses-a-controlled-env-g66` 의 witness 에 `stdout[-600:]` 에서
    우연히 잘린 `도 기대와 다르면 그때는` 이 들어 있어 그 기계에서는 `call_witness_matches=false`
    였다. **실패 집합과 call 단계는 맞았고 이유의 문자열만** 안 맞았다 — 그것을 "변이가 안
    물었다" 로도 "전수 인증됐다" 로도 쓰면 안 된다 (리뷰어가 양쪽 다 금지했다).

    규칙은 리뷰어 조건 그대로 좁혔다: **값 직전에서 끊는 것은 허용**하고(이 저장소의 기존
    관행 — 임시 경로가 실행마다 다르다), 끊은 뒤에 그 값의 **일부를 담는 것**을 금지한다.

    ⚠ 한 번 더 넓은 규칙("닫힌 따옴표 조각은 시험 소스에 있어야 한다")도 재 봤는데 **버렸다**:
    `'NoneType'`·`'ok:canonical'`·`'src.scoring:MODES'` 처럼 시험이 **결정적으로** 만드는
    repr 이 19건 걸린다. 그것은 가변 꼬리가 아니므로 그 규칙은 축을 잘못 겨냥한 것이다.
    """
    mr = _mr()
    bad = []
    for axis, spec in mr.EXPECT.items():
        for node, w in (spec.get("witness") or {}).items():
            tail = _unclosed_tail(_WITNESS_SCAFFOLD.sub("", str(w)))
            if tail:
                bad.append(f"{axis} · {node.rsplit('::', 1)[-1]}: 열린 따옴표 뒤에 "
                           f"{tail[:40]!r} 가 남아 있다")
    assert not bad, ("witness 에 가변 출력의 꼬리가 있다 — 고정된 이유여야 한다 (G67-T1-b)",
                     bad)


# ── fixture ──────────────────────────────────────────────────────────────────────

@pytest.fixture
def off(tmp_path_factory):
    """user site **비활성** 인터프리터."""
    return make_interpreter(tmp_path_factory.mktemp("g67-off"), user_site=False)


@pytest.fixture
def on(tmp_path_factory):
    """user site **활성** 인터프리터."""
    return make_interpreter(tmp_path_factory.mktemp("g67-on"), user_site=True)
