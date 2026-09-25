"""60차 β (P0-2·P0-3) — **발급과 소비의 authority 를 닫는다.**

리뷰어 반례 세 줄 (한 재현기에서 같이 나왔다):

    {"raw_record_api_without_capability":"canonical",
     "public_issuer_without_gate":"canonical",
     "genuine_smoke_capability_mutated_in_place":
       {"issued_as":"smoke","committed_as":"canonical"}}

그리고 소비 쪽 두 줄:

    {"reused_capability":{"nonce_still_registered_after_commit":true,
                          "unjudged_second_class":"canonical"},
     "retry_after_binding_refusal":{"first_call_refused":true,
                                    "nonce_still_registered":true,
                                    "replacement_class_after_second_call":"canonical"}}

`[해석]` 59차는 "권한이 없으면 못 굳힌다" 를 만들었다. 그런데 **권한을 얻는
경로**와 **권한이 죽는 시점**을 안 닫았다.

  - 발급: 공개 sink 가 raw `cls` 를 받고, 공개 mint 가 caller 가 고른 class 를
    그대로 찍는다. 그러면 gate 는 여러 문 중 하나일 뿐이다.
  - 증인: 등록부가 caller 가 든 **같은 mutable object** 를 저장했다. 같은
    객체를 대조하는 것은 봉인이 아니다 — caller 가 고치면 증인도 같이 바뀐다.
  - 소비: 굳힌 뒤에도 nonce 가 살아 있고 `dir_fd` 만 사라졌다. 그래서 두 번째
    호출이 **판정하지 않은 자리**를 canonical 로 굳혔다.

그러므로 이 라운드의 규칙: **class 는 gate 가 정하고, 권한은 서버 쪽 기록이
정본이며, 소비는 일회성 상태 전이다.**
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import tools.preserve as P                                      # noqa: E402


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    led = tmp_path / "authority" / "LEG_PRESERVATION.yaml"
    led.parent.mkdir(parents=True)
    led.write_text("planned: []\nlegs: []\ncohorts: []\n", encoding="utf-8")
    monkeypatch.setattr(P, "canonical_ledger", lambda x=None: led)
    monkeypatch.setattr(P, "SMOKE_NAMESPACE", tmp_path / "results" / "_smoke")
    return led


def _run_dir(d: Path) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    (d / "curves_manifest.yaml").write_text(f"curves_sha256: {d.name}\n",
                                            encoding="utf-8")
    return d


# ── P0-2 발급 표면 ─────────────────────────────────────────────────────────
def test_no_public_name_records_a_raw_execution_class():
    """★ P0-2 — raw class 를 받는 sink 가 **공개 이름으로 남아 있으면 안 된다.**

    계약 §13.3.4 는 "공개 API 를 지나는 호출은 전부 범위 안" 이라고 적었다.
    그러므로 "같은 프로세스의 적대적 writer 는 범위 밖" 이라는 변명으로 이
    표면을 남길 수 없다.
    """
    assert not hasattr(P, "record_execution_class"), (
        "raw class 를 받는 공개 sink 가 그대로 있다 — 권한을 지나지 않는 문이 "
        "열려 있다 (P0-2)")


def test_every_callsite_of_the_raw_sink_is_inside_the_publisher():
    """★ P0-2 — 최소 조건이 요구한 **callsite 열거** 회귀.

    이름을 비공개로 바꾸는 것만으로는 부족하다. 저장소 전체에서 그 이름을
    부르는 자리가 publisher 안에만 있어야 하고, 그 사실이 기계로 확인돼야 한다.
    """
    bad = []
    for py in sorted(REPO.rglob("*.py")):
        if "__pycache__" in str(py) or py.name.startswith("test_"):
            continue
        rel = py.relative_to(REPO).as_posix()
        if rel == "tools/preserve.py":
            continue
        # ★ 72차 — 보존한 리뷰 패키지(`docs/22p_gap/gate*_review/`)는 **증거의 바이트 사본**이지 이 저장소의
        #   코드가 아니다. 72차 패키지가 `codex/reference/tools/preserve.py` 전문을 담아 오자 그 안의 sink
        #   정의·호출이 "publisher 밖의 callsite" 로 잡혔다 (실측: 54d50763 전체 회귀 1 failed). 패키지는
        #   `-text !eol` 로 바이트를 굳혀 두는 자료이므로 고치지 않고, 여기서 코드 검사 대상에서 뺀다.
        #   RUN_SCOPE(`src tools configs scripts run.sh`) 는 그대로 전부 본다.
        if rel.startswith("docs/22p_gap/gate") and "_review/" in rel:
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):       # pragma: no cover
            continue
        for node in ast.walk(tree):
            name = None
            if isinstance(node, ast.Call):
                f = node.func
                name = (f.id if isinstance(f, ast.Name)
                        else f.attr if isinstance(f, ast.Attribute) else None)
            elif isinstance(node, ast.ImportFrom):
                for a in node.names:
                    if a.name == "_record_execution_class":
                        bad.append(f"{rel}: import {a.name}")
            if name == "_record_execution_class":
                bad.append(f"{rel}:{node.lineno}")
    assert not bad, ("raw sink 를 publisher 밖에서 부른다: " + ", ".join(bad))


def test_the_gate_decides_the_class_and_the_caller_cannot_choose_it(tmp_path,
                                                                     ledger):
    """★ P0-2 — mint 에 `cls` 인자가 없다. class 는 **자리가 정한다.**

    계획 gate 의 면제를 정하는 것과 **같은 함수**(`is_inside_namespace()`)로
    정한다 — 두 규칙이 갈리면 어느 쪽이 경계인지 정할 수 없다.
    """
    import inspect

    sig = inspect.signature(P.issue_execution_class)
    assert "cls" not in sig.parameters, (
        f"mint 가 여전히 class 를 받는다: {sig} — caller 가 고르면 gate 는 여러 "
        "문 중 하나일 뿐이다 (P0-2)")

    smoke = _run_dir(tmp_path / "results" / "_smoke" / "s")
    canon = _run_dir(tmp_path / "results" / "c")
    assert P.issue_execution_class(smoke, "L", "grid",
                                   ledger=ledger).execution_class \
        == P.EXEC_CLASS_SMOKE
    assert P.issue_execution_class(canon, "L", "grid",
                                   ledger=ledger).execution_class \
        == P.EXEC_CLASS_CANONICAL


def test_mutating_the_capability_in_place_does_not_change_what_is_committed(
        tmp_path, ledger):
    """★ P0-2 — 증인은 caller 가 든 **그 객체**여서는 안 된다.

    리뷰어 실측: 진짜로 발행된 smoke 권한의 필드를 제자리에서 고쳤더니
    `issued_as smoke → committed_as canonical` 이었다. 등록부가 같은 객체를
    저장했으므로 identity 대조가 아무것도 안 막았다.
    """
    smoke = _run_dir(tmp_path / "results" / "_smoke" / "s")
    cap = P.issue_execution_class(smoke, "L", "grid", ledger=ledger)
    assert cap.execution_class == P.EXEC_CLASS_SMOKE

    try:
        object.__setattr__(cap, "execution_class", P.EXEC_CLASS_CANONICAL)
    except AttributeError:
        pass                        # 필드 자체가 없으면 그것으로 충분하다

    P.commit_run_outputs(cap, [smoke])
    rec = P.read_execution_class(P.run_content_id(smoke), ledger=ledger)
    assert rec["execution_class"] == P.EXEC_CLASS_SMOKE, (
        "권한 객체를 제자리에서 고쳤더니 굳은 class 가 바뀌었다 — 증인이 "
        "독립적이지 않다 (P0-2)")


# ── P0-3 소비의 일회성 ────────────────────────────────────────────────────
def test_a_capability_is_spent_by_a_successful_commit(tmp_path, ledger):
    """★ P0-3 — 성공한 소비는 권한을 **영구히 폐기**한다.

    리뷰어 실측: 굳힌 뒤에도 nonce 가 등록부에 남아 있었고 `dir_fd` 만
    `None` 이 됐다. 그래서 두 번째 호출은 identity 검사를 다시 통과하고,
    `_assert_still_the_judged_dir()` 는 `dir_fd is None` 이면 곧바로 반환하므로
    **판정하지 않은 자리**가 canonical 로 굳었다.
    """
    first = _run_dir(tmp_path / "results" / "first")
    cap = P.issue_execution_class(first, "L", "grid", ledger=ledger)
    P.commit_run_outputs(cap, [first])

    assert cap.nonce not in P._ISSUED_EXEC_CAPS, (
        "소비한 권한의 일련번호가 살아 있다 (P0-3)")

    second = _run_dir(tmp_path / "results" / "second")
    with pytest.raises(P.PreserveError) as ei:
        P.commit_run_outputs(cap, [second])
    assert P.read_execution_class(P.run_content_id(second),
                                  ledger=ledger) is None, (
        "판정하지 않은 자리가 굳었다 — 권한이 재사용됐다 (P0-3)\n"
        + str(ei.value))


def test_a_binding_refusal_does_not_turn_a_bound_capability_into_a_loose_one(
        tmp_path, ledger):
    """★ P0-3 — 거부 뒤에도 **결속은 그대로**여야 한다.

    "bound live nonce 를 unbound live nonce 로 바꾸는 상태는 없어야 한다."
    거부는 재시도를 허용할 수 있지만, 재시도가 보는 결속은 처음 그대로다.
    """
    judged = _run_dir(tmp_path / "results" / "judged")
    cap = P.issue_execution_class(judged, "L", "grid", ledger=ledger)

    other = _run_dir(tmp_path / "results" / "other")
    with pytest.raises(P.PreserveError):
        P.commit_run_outputs(cap, [other])          # 판정한 대상이 아니다

    with pytest.raises(P.PreserveError):
        P.commit_run_outputs(cap, [other])          # 두 번째도 같아야 한다
    assert P.read_execution_class(P.run_content_id(other),
                                  ledger=ledger) is None, (
        "거부 뒤 재시도가 다른 자리를 굳혔다 — 거부가 결속을 풀었다 (P0-3)")

    # 그리고 **원래 대상**으로는 여전히 굳을 수 있어야 한다 (거부가 마비가
    # 되면 그것은 경계가 아니다 — 49차에 같은 실수를 했다)
    P.commit_run_outputs(cap, [judged])
    assert P.read_execution_class(P.run_content_id(judged),
                                  ledger=ledger) is not None
