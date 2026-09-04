"""58차 P0-8 — 실행 class 를 **경로가 아니라 내용**으로 정한다.

48~57차의 승격 금지는 `is_inside_namespace()` 하나였다. 경로는 산출의 성질이
아니라 "지금 어디 놓여 있는가" 이므로, 바이트를 옮기면 그만이었다.

`[재현]` 이 파일의 첫 시험이 그 구멍을 재현한다 — 고치기 전에는 통과했다
(같은 run dir 를 namespace 밖으로 복사하면 승격 sink 가 받아들였다).
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tools.preserve import (EXEC_CLASS_CANONICAL, EXEC_CLASS_SMOKE,
                            PreserveError, assert_not_smoke_provenance,
                            classify_legacy_run, read_execution_class,
                            record_execution_class, run_content_id)


def _run_dir(root: Path, name: str, body: str = "source_digest: abc\n") -> Path:
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "curves_manifest.yaml").write_text(body, encoding="utf-8")
    return d


@pytest.fixture
def ledger(tmp_path) -> Path:
    """격리된 원장 — 등록부는 그 옆에 생긴다."""
    led = tmp_path / "authority" / "LEG_PRESERVATION.yaml"
    led.parent.mkdir(parents=True)
    led.write_text("planned: []\nlegs: []\n", encoding="utf-8")
    return led


def test_moving_a_smoke_run_out_of_the_namespace_does_not_make_it_promotable(
        tmp_path, ledger, monkeypatch):
    """★ P0-8 의 본체 — 같은 바이트가 경로만 바꿔 정본이 되면 안 된다."""
    import tools.preserve as P
    ns = tmp_path / "results" / "_smoke"
    monkeypatch.setattr(P, "SMOKE_NAMESPACE", ns)
    monkeypatch.setattr(P, "canonical_ledger", lambda _=None: ledger)

    inside = _run_dir(ns, "run1")
    P.record_execution_class(inside, EXEC_CLASS_SMOKE, evidence="시험", ledger=ledger)

    # 제자리에서는 예전에도 막혔다
    with pytest.raises(PreserveError, match="승격 대상이 아니다"):
        P.assert_not_smoke_provenance([inside], "보고서", dest=tmp_path / "OUT.md")

    # ★ 바이트를 통째로 밖으로 옮긴다 — 경로 판정은 여기서 통과한다
    moved = tmp_path / "looks_canonical"
    shutil.copytree(inside, moved)
    assert not P.is_inside_namespace(moved, ns), "전제: 이제 namespace 밖이다"

    with pytest.raises(PreserveError, match="내용.*smoke 로 등록"):
        P.assert_not_smoke_provenance([moved], "보고서", dest=tmp_path / "OUT.md")


def test_an_unregistered_run_is_refused_rather_than_assumed_canonical(
        tmp_path, ledger, monkeypatch):
    """등록이 없으면 **모른다** 이고, 모르면 거부다 (fail-closed).

    "등록 없음 = 정본" 으로 두면 등록부가 smoke 블랙리스트가 되고, 그러면
    블랙리스트를 늘리는 일이 다시 시작된다 — 리뷰어가 56차에 종결이 아니라고
    한 바로 그 형태다.
    """
    import tools.preserve as P
    monkeypatch.setattr(P, "SMOKE_NAMESPACE", tmp_path / "results" / "_smoke")
    monkeypatch.setattr(P, "canonical_ledger", lambda _=None: ledger)
    d = _run_dir(tmp_path, "unknown_run")
    with pytest.raises(PreserveError, match="등록돼 있지 않다"):
        P.assert_not_smoke_provenance([d], "보고서", dest=tmp_path / "OUT.md")


def test_a_run_without_a_manifest_has_no_identity_and_is_refused(
        tmp_path, ledger, monkeypatch):
    """identity 를 못 만들면 판정할 수 없다 — 통과가 아니라 거부다."""
    import tools.preserve as P
    monkeypatch.setattr(P, "SMOKE_NAMESPACE", tmp_path / "results" / "_smoke")
    monkeypatch.setattr(P, "canonical_ledger", lambda _=None: ledger)
    empty = tmp_path / "no_manifest"
    empty.mkdir()
    with pytest.raises(PreserveError, match="내용 identity"):
        P.assert_not_smoke_provenance([empty], "보고서", dest=tmp_path / "OUT.md")


def test_content_id_follows_the_bytes_not_the_path(tmp_path):
    a = _run_dir(tmp_path / "x", "run")
    b = tmp_path / "y" / "run"
    b.parent.mkdir(parents=True)
    shutil.copytree(a, b)
    assert run_content_id(a) == run_content_id(b), "복사본은 같은 identity 여야 한다"
    (b / "curves_manifest.yaml").write_text("source_digest: CHANGED\n",
                                            encoding="utf-8")
    assert run_content_id(a) != run_content_id(b), "내용이 바뀌면 identity 도 바뀐다"


def test_classification_is_one_time_and_records_what_it_looked_at(
        tmp_path, ledger, monkeypatch):
    """legacy 분류는 **한 번**이고, 경로를 봤다는 사실이 영수증에 남는다."""
    import tools.preserve as P
    ns = tmp_path / "results" / "_smoke"
    monkeypatch.setattr(P, "SMOKE_NAMESPACE", ns)
    monkeypatch.setattr(P, "canonical_ledger", lambda _=None: ledger)

    old = _run_dir(ns, "legacy")
    rec = P.classify_legacy_run(old, ledger=ledger)
    assert rec["execution_class"] == EXEC_CLASS_SMOKE
    assert "분류 시점 경로" in rec["evidence"], rec
    assert str(ns) in rec["evidence"], "무엇과 비교했는지가 남아야 한다"

    # 옮긴 뒤 다시 분류해도 **첫 판정이 이긴다** (재분류 없음)
    moved = tmp_path / "moved_legacy"
    shutil.copytree(old, moved)
    again = P.classify_legacy_run(moved, ledger=ledger)
    assert again["execution_class"] == EXEC_CLASS_SMOKE, \
        "옮긴 뒤 재분류로 정본이 되면 migration 이 곧 우회로다"


def test_a_content_cannot_hold_two_classes(tmp_path, ledger, monkeypatch):
    import tools.preserve as P
    monkeypatch.setattr(P, "canonical_ledger", lambda _=None: ledger)
    d = _run_dir(tmp_path, "run")
    P.record_execution_class(d, EXEC_CLASS_SMOKE, evidence="첫 등록", ledger=ledger)
    with pytest.raises(PreserveError, match="이미 .*로 등록"):
        P.record_execution_class(d, EXEC_CLASS_CANONICAL, evidence="뒤집기",
                                 ledger=ledger)


def test_a_canonical_registration_lets_promotion_through(
        tmp_path, ledger, monkeypatch):
    """정본으로 등록된 산출은 통과한다 — 이 검사가 마비가 아님을 못 박는다."""
    import tools.preserve as P
    monkeypatch.setattr(P, "SMOKE_NAMESPACE", tmp_path / "results" / "_smoke")
    monkeypatch.setattr(P, "canonical_ledger", lambda _=None: ledger)
    d = _run_dir(tmp_path, "good_run")
    P.record_execution_class(d, EXEC_CLASS_CANONICAL, evidence="계획 gate 통과",
                             ledger=ledger)
    P.assert_not_smoke_provenance([d], "보고서", dest=tmp_path / "OUT.md")
