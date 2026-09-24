"""68차 게이트 리뷰 방어 — G68-T1 (P2) 회귀.

리뷰어 판정: 부분 수용 / 종결 NO-GO. G67-N1 · N2 · T1-b 는 수용, G67-T1 은 **call 실행 증거가 불충분**.
원문 `docs/22p_gap/gate68_review/codex/GATE68_REVIEW_KO.md`.

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| G68-T1 (P2) | `_premise_outcomes()` 는 JUnit testcase 에 error/failure/skipped 자식이 없으면 **passed** 로 읽는다. `--setup-only` child 는 fixture 만 준비하고 **call 단계를 생략**하면서도 testcase 를 자식 없이 적는다 → rc 0 · 정확한 두 testcase · 자식 없음 — 셋 다 맞는데 시험 본문은 한 줄도 안 돈 child 가 **ACCEPTED, 미측정 []** | `tests/test_gate66_defensive.py` `_premise_outcomes` `:284` · `assert_premise_actually_ran` |

리뷰어의 최소 종결 조건 (그대로 옮긴다): exact full node ID 별 **실제 call-phase report** 를 검증한다 —
정상 측정은 `when=call, outcome=passed`; setup/teardown 오류 · skip/미측정 · 중복/누락을 **따로** 가른다.
`rc=0` · JUnit testcase 수 · 요약의 passed 수 · 특정 옵션 문자열 차단으로 **대체하지 않는다**. 외부 plugin 을
필수화하지 않는다 (내장 hook 기반의 작은 증거 기록으로 충분). 회귀는 정상 / usage error / collect-only /
**setup-only** / 상속 옵션 제거 대조를 유지하고, **실제 child 와 같은 소비 경로**를 쓴다. 임의 예외나 서명
`TypeError` 를 기대 거부로 세지 않는다.

여기서의 규율 (67차와 같다): `subprocess` 를 가짜로 만들지 않는다. 합성 사례가 필요하면 **실제 clean child 의
산출을 한 번 만들고 그 파일을 고쳐서** 소비자에게 준다 — 소비 경로는 실제와 같다.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_gate66_defensive as tm                                      # noqa: E402


# ── 실제 child ───────────────────────────────────────────────────────────────

def test_g68_01_the_premise_regression_refuses_a_setup_only_child(tmp_path):
    """★ G68-T1 — 리뷰어 반례 그대로. 원본 `_premise_run` 의 명시 `env_extra` 로 `PYTEST_ADDOPTS=--setup-only`
    를 준다. child 는 rc 0, JUnit 에는 정확한 두 testcase 가 failure/error/skipped 없이 적힌다. 실제 단계 관측에는
    setup/teardown 만 있고 **call 0 개**다. 전 판의 `assert_premise_actually_ran` 은 이것을 ACCEPTED / 미측정 [] 로
    돌려줬다 (리뷰어 `t1_setup_only/RESULTS.json`). 이제 **거부**해야 한다 — 그리고 그 거부는 `AssertionError`
    여야 한다 (임의 예외는 증거가 아니다)."""
    junit = tmp_path / "premise.xml"
    r = tm._premise_run(sys.executable, {"PYTEST_ADDOPTS": "--setup-only"}, junit)
    assert r.returncode == 0, ("반례의 전제가 깨졌다 — setup-only child 가 rc 0 이 아니다", r.returncode,
                               (r.stdout or "")[-400:], (r.stderr or "")[-400:])
    with pytest.raises(AssertionError) as ei:
        tm.assert_premise_actually_ran(r, junit)
    assert "G68-T1" in str(ei.value), ("거부했지만 사유가 call 단계 부재가 아니다", str(ei.value)[:300])


@pytest.mark.parametrize("env_extra", [{}, {"PYTHONNOUSERSITE": "1"}], ids=["clean", "nousersite"])
def test_g68_02_a_clean_child_is_still_accepted_on_the_same_path(monkeypatch, env_extra):
    """대조군(양성) — 같은 소비 경로에서 정상 child 는 계속 통과한다. call 증거를 요구한 뒤 "전부 거부" 로 가면
    여기서 잡힌다. skip 은 통과가 아니라 미측정이므로 목록으로 돌아온다."""
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)
    with tempfile.TemporaryDirectory(prefix="g68-") as d:
        junit = Path(d) / "premise.xml"
        r = tm._premise_run(sys.executable, env_extra, junit)
        unmeasured = tm.assert_premise_actually_ran(r, junit)
    assert isinstance(unmeasured, list)


@pytest.mark.parametrize("addopts", ["--collect-only", "--g68-option-does-not-exist", "--setup-only"],
                         ids=["collect_only", "usage_error", "setup_only"])
def test_g68_03_the_three_unrun_shapes_are_all_refused_with_a_reason(tmp_path, addopts):
    """G67-T1 의 두 모양(수집만 · 사용법 오류)에 **setup-only** 를 더해 셋을 한 자리에서 본다. 셋 다 `AssertionError`
    이고, 사유 문장이 서로 다르다 — "안 돌았다" 하나로 뭉개면 변이 증인이 뭉개진다 (67차 T1-b 교훈)."""
    junit = tmp_path / "premise.xml"
    r = tm._premise_run(sys.executable, {"PYTEST_ADDOPTS": addopts}, junit)
    with pytest.raises(AssertionError) as ei:
        tm.assert_premise_actually_ran(r, junit)
    msg = str(ei.value)
    assert ("G67-T1" in msg) or ("G68-T1" in msg), msg[:300]


# ── 소비자 — 실제 clean child 의 산출을 고쳐서 묻는다 ───────────────────────────

@pytest.fixture(scope="module")
def clean_child():
    """실제 clean child 한 번. 산출(JUnit + 단계 증거)을 module 안에서 나눠 쓴다."""
    d = tempfile.mkdtemp(prefix="g68-clean-")
    junit = Path(d) / "premise.xml"
    r = tm._premise_run(sys.executable, {}, junit)
    tm.assert_premise_actually_ran(r, junit)          # 전제: 이 기계에서 정상 child 는 통과한다
    yield r, junit
    import shutil
    shutil.rmtree(d, ignore_errors=True)


def _copy_outputs(clean, dst: Path) -> tuple:
    r, junit = clean
    j2 = dst / "premise.xml"
    j2.write_bytes(junit.read_bytes())
    tm._phase_witness_path(j2).write_bytes(tm._phase_witness_path(junit).read_bytes())
    return r, j2


def _records(junit: Path) -> list:
    return [json.loads(l) for l in tm._phase_witness_path(junit).read_text(encoding="utf-8").splitlines() if l.strip()]


def _write(junit: Path, recs: list) -> None:
    tm._phase_witness_path(junit).write_text("".join(json.dumps(x) + "\n" for x in recs), encoding="utf-8")


def test_g68_04_a_node_without_a_call_record_is_unrun(tmp_path, clean_child):
    """★ 핵심 — 한 node 의 `when=call` 줄만 지우면(setup/teardown 은 남긴다) 그 node 는 "돌지 않았다" 다.
    JUnit 은 그대로 passed 라 **JUnit 만 보는 소비자는 못 잡는다** — 그것이 G68-T1 이다."""
    r, junit = _copy_outputs(clean_child, tmp_path)
    recs = _records(junit)
    victim = next(x["nodeid"] for x in recs if x["when"] == "call")
    _write(junit, [x for x in recs if not (x["nodeid"] == victim and x["when"] == "call")])
    with pytest.raises(AssertionError, match="G68-T1"):
        tm.assert_premise_actually_ran(r, junit)


def test_g68_05_a_duplicated_call_record_is_not_two_measurements(tmp_path, clean_child):
    """중복 — 같은 node 의 call 이 둘이면 어느 것이 측정인지 알 수 없다. 거부."""
    r, junit = _copy_outputs(clean_child, tmp_path)
    recs = _records(junit)
    dup = next(x for x in recs if x["when"] == "call")
    _write(junit, recs + [dup])
    with pytest.raises(AssertionError, match="G68-T1"):
        tm.assert_premise_actually_ran(r, junit)


def test_g68_06_a_setup_error_is_not_a_measurement(tmp_path, clean_child):
    """setup/teardown 오류 — call 이 있어도 그 node 의 setup 이 failed 면 측정이 아니다 (별도 사유)."""
    r, junit = _copy_outputs(clean_child, tmp_path)
    recs = _records(junit)
    for x in recs:
        if x["when"] == "setup":
            x["outcome"] = "failed"
            break
    _write(junit, recs)
    with pytest.raises(AssertionError, match="G68-T1"):
        tm.assert_premise_actually_ran(r, junit)


def test_g68_07_a_skipped_call_is_unmeasured_not_passed(tmp_path, clean_child):
    """skip — call 결말이 skipped 면 통과가 아니라 **미측정** 이고, 그 node 이름이 목록으로 돌아온다.
    (JUnit 도 같이 skipped 로 맞춘다 — 두 증거가 어긋나면 그것대로 거부다, `test_g68_09`.)"""
    r, junit = _copy_outputs(clean_child, tmp_path)
    recs = _records(junit)
    victim = None
    for x in recs:
        if x["when"] == "call":
            x["outcome"] = "skipped"; victim = x["nodeid"]; break
    _write(junit, recs)
    _mark_junit_skipped(junit, victim.split("::")[-1])
    out = tm.assert_premise_actually_ran(r, junit)
    assert out == [victim.split("::")[-1]], out


def test_g68_08_an_extra_or_missing_node_id_is_a_wrong_selection(tmp_path, clean_child):
    """exact full node ID — 다른 파일의 같은 이름이나 세 번째 node 는 "선택이 어긋났다" 다."""
    r, junit = _copy_outputs(clean_child, tmp_path)
    recs = _records(junit)
    alien = dict(recs[0], nodeid="tests/test_other.py::" + recs[0]["nodeid"].split("::", 1)[1])
    _write(junit, [alien if i == 0 else x for i, x in enumerate(recs)])
    with pytest.raises(AssertionError):
        tm.assert_premise_actually_ran(r, junit)


def test_g68_09_junit_and_phase_evidence_must_agree(tmp_path, clean_child):
    """두 증거가 어긋나면 거부 — 단계 증거는 passed 인데 JUnit 이 skipped 면 어느 쪽이 child 의 진실인지 모른다."""
    r, junit = _copy_outputs(clean_child, tmp_path)
    name = next(x["nodeid"] for x in _records(junit) if x["when"] == "call").split("::")[-1]
    _mark_junit_skipped(junit, name)
    with pytest.raises(AssertionError):
        tm.assert_premise_actually_ran(r, junit)


def test_g68_10_the_witness_is_a_builtin_hook_not_an_external_plugin():
    """리뷰어 조건 — 외부 plugin 을 필수화하지 않는다. 증거 기록은 저장소 안의 작은 모듈이고 pytest 내장 hook
    (`pytest_runtest_logreport`) 만 쓴다. `_premise_run` 이 그것을 `-p` 로 명시해 싣는다."""
    src = (Path(__file__).with_name("phase_witness.py")).read_text(encoding="utf-8")
    assert "def pytest_runtest_logreport" in src
    assert "json_report" not in src and "pytest_jsonreport" not in src
    import inspect
    body = inspect.getsource(tm._premise_run)
    assert "tests.phase_witness" in body and "--phase-witness" in body


def _mark_junit_skipped(junit: Path, name: str) -> None:
    import xml.etree.ElementTree as ET
    tree = ET.parse(junit)
    for case in tree.getroot().iter("testcase"):
        if case.get("name") == name:
            ET.SubElement(case, "skipped", {"message": "g68 synthetic"})
    tree.write(junit, encoding="utf-8", xml_declaration=True)
