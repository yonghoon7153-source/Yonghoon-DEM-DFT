"""59차 α (M1·M3·M4) — 실행 class 가 **산출 commit 까지** 흘러야 한다.

리뷰어 반례 셋을 그대로 옮긴다.

    M1  {"class_after_output": null,
         "class_after_move_and_migration": "canonical",
         "promotion_guard": "PASSED"}
    M3  첫 등록이 성공 경로로 반환하고 final 파일은 `{` 한 바이트
    M4  {"local_class":"smoke", "shared_class":"canonical",
         "resolved_class":"canonical", "conflict_was_reported":false}

`[해석]` 58차는 **면제를 말하는 함수**(`note_smoke_exemption()`)를 만들고 조기
return 자리가 그것을 거치게 했다. 거기까지는 맞다. 그런데 그 함수는 manifest 가
아직 없어 "기록 못 한 자리" 목록을 돌려주고, **그 목록을 아무도 안 받는다.**
산출이 굳는 순간 기록한다던 `record_run_outputs()` 는 저장소에 실호출이 0곳이다.
우리 docstring 이 "호출자는 이 목록을 무시해도 된다" 고 스스로 적어 놓았다.

그러므로 물음을 한 번 더 바꾼다: **gate 는 목록이 아니라 권한을 발행하고,
산출을 굳히는 함수는 그 권한 없이는 굳힐 수 없다.** class 는 권한이 나르므로
호출자가 raw `cls` 를 다시 줄 자리가 없다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import tools.preserve as P                                      # noqa: E402


def _ledger(tmp_path: Path, monkeypatch=None) -> Path:
    led = tmp_path / "authority" / "LEG_PRESERVATION.yaml"
    led.parent.mkdir(parents=True, exist_ok=True)
    led.write_text("planned: []\nlegs: []\n", encoding="utf-8")
    # ★ 60차 P0-2 — class 는 이제 **자리가 정한다.** 그러므로 시험이
    #   `results/_smoke/...` 라고 부르는 자리가 실제로 smoke namespace 안이어야
    #   한다. 59차까지는 발급 인자로 class 를 강제했고, 그 인자가 바로
    #   리뷰어가 지목한 우회로였다.
    if monkeypatch is not None:
        monkeypatch.setattr(P, "SMOKE_NAMESPACE", tmp_path / "results" / "_smoke")
    return led


def _manifest(d: Path, *, curves: str = "aa") -> None:
    """production 이 굳히는 것과 같은 이름의 manifest 를 놓는다."""
    d.mkdir(parents=True, exist_ok=True)
    (d / "curves_manifest.yaml").write_text(f"curves_sha256: {curves}\n",
                                            encoding="utf-8")


# ── M1 ────────────────────────────────────────────────────────────────────
def test_the_gate_issues_a_capability_and_the_commit_requires_it(tmp_path, monkeypatch):
    """★ M1 — gate 는 **권한**을 발행한다 (무시할 수 있는 목록이 아니라).

    58차판은 `note_smoke_exemption()` 이 pending 목록을 돌려주고 호출자가 그것을
    버려도 됐다. 권한이면 버릴 수 없다 — 산출을 굳히는 함수가 그것을 요구한다.
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    out.mkdir(parents=True)

    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    assert cap is not None, "gate 가 권한을 발행하지 않는다"

    # 산출이 굳는 순간 — 권한을 소비해야 기록된다
    _manifest(out)
    P.commit_run_outputs(cap, [out])
    rec = P.read_execution_class(P.run_content_id(out), ledger=led)
    assert rec and rec["execution_class"] == P.EXEC_CLASS_SMOKE, (
        f"산출을 굳혔는데 class 가 등록부에 없다: {rec!r} (M1)")


def test_committing_an_output_without_a_capability_is_refused(tmp_path, monkeypatch):
    """★ M1 — 권한 없이 굳히는 경로가 **없어야** 한다.

    최소 조건이 명시한다: "완료 함수가 caller 에게 raw `cls` 를 다시 받으면 같은
    우회가 남는다." 그러므로 raw class 를 받는 공개 완료 함수는 존재하면 안 된다.
    """
    assert not hasattr(P, "record_run_outputs"), (
        "raw class 를 받는 완료 함수가 아직 공개돼 있다 — 권한을 우회하는 "
        "같은 길이 남는다 (M1)")

    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    _manifest(out)
    # ★ 59차 마감 — 받아들이는 예외를 **`PreserveError` 하나로** 좁혔다.
    #
    #   처음에는 `(PreserveError, TypeError, AttributeError)` 였다. 그러면
    #   guard 를 지워도 그 다음 줄이 `None.nonce` 로 터져 `AttributeError` 가
    #   나고 시험이 그대로 통과한다 — 실제로 이 축의 변이가 안 물었다(실측:
    #   `변이 rc 0`). **crash 는 거부가 아니다**: 어디까지 진행됐는지 말하지
    #   않고, 부분 상태를 남길 수 있다. 거부는 그 자리에서 이유를 말하는
    #   것이어야 한다.
    for forged in (None, "smoke", {"cls": "smoke"},
                   P.ExecutionClassCapability):
        with pytest.raises(P.PreserveError):
            P.commit_run_outputs(forged, [out])
    assert P.read_execution_class(P.run_content_id(out), ledger=led) is None


def test_a_smoke_output_moved_outside_is_not_relabelled_canonical(tmp_path, monkeypatch):
    """★ M1 — 리뷰어 반례 그대로: 등록 → 이동 → legacy migration.

    58차판은 gate 시점에 manifest 가 없어 등록이 pending 이었고, 그것을 버린 채
    산출을 밖으로 옮기면 `classify_legacy_run()` 이 **지금 경로**를 보고
    canonical 을 발급했다. 권한이 산출 commit 에서 class 를 굳히면, 이동 뒤
    분류는 이미 등록된 것을 읽을 뿐 새로 정하지 않는다.
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    out.mkdir(parents=True)
    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    _manifest(out)
    P.commit_run_outputs(cap, [out])

    moved = tmp_path / "elsewhere" / "run"
    moved.parent.mkdir(parents=True)
    out.rename(moved)

    rec = P.classify_legacy_run(moved, ledger=led)
    assert rec["execution_class"] == P.EXEC_CLASS_SMOKE, (
        f"밖으로 옮겼더니 canonical 이 됐다: {rec!r} — 내용 identity 는 그대로다 "
        "(M1)")
    with pytest.raises(P.PreserveError):
        P.assert_not_smoke_provenance([moved], sink="promote")


def test_legacy_migration_only_applies_to_a_declared_roster(tmp_path, monkeypatch):
    """★ M1 — legacy 분류는 **배선 전 산출의 명시적 roster** 에만.

    최소 조건: "legacy migration 은 배선 전 산출의 명시적 roster 에만 허용해야
    한다." 그렇지 않으면 새 산출을 등록 없이 만든 뒤 migration 으로 세탁하는
    길이 계속 열려 있다.
    """
    led = _ledger(tmp_path, monkeypatch)
    fresh = tmp_path / "brand-new" / "run"
    _manifest(fresh, curves="bb")
    with pytest.raises(P.PreserveError) as ei:
        P.classify_legacy_run(fresh, ledger=led)
    assert "roster" in str(ei.value) or "legacy" in str(ei.value), ei.value


def test_the_legacy_roster_is_repo_relative():
    """★ M1 — roster 항목이 **상대 경로**라는 것 자체가 불변식이다.

    `classify_legacy_run()` 은 항목을 `REPO_ROOT` 에 붙여 해석하고, pathlib 은
    우변이 absolute 면 좌변을 버린다. 그러므로 절대 경로 항목 하나면 저장소
    **밖**의 산출이 roster 에 오른다 — roster 가 경계인 이유가 사라진다.
    (58차가 `bundle_uri` 와 `SMOKE_NAMESPACE` 에서 두 번 만난 같은 흡수다.)
    """
    from pathlib import PurePosixPath
    for entry in P.LEGACY_EXEC_CLASS_ROSTER:
        assert not PurePosixPath(entry).is_absolute(), (
            f"roster 항목이 절대 경로다: {entry!r} — REPO_ROOT 밖을 분류할 수 "
            "있게 된다 (M1)")
        assert ".." not in PurePosixPath(entry).parts, (
            f"roster 항목이 상위로 올라간다: {entry!r} (M1)")


# ── M3 ────────────────────────────────────────────────────────────────────
def test_a_short_write_never_publishes_a_partial_record(tmp_path, monkeypatch):
    """★ M3 — final 이름에 **부분 바이트**가 공개되면 안 된다.

    리뷰어 반례: 첫 `os.write()` 를 한 바이트 short write 로 만들면 등록이
    성공 경로로 반환하고 final 파일은 `{` 하나였다. `read_execution_class()` 는
    `None`, 같은 class 재시도는 "이미 있는데 못 읽는 파일" 때문에 영구 거부.

    `O_EXCL` 은 writer **사이의 이름 배타**를 줄 뿐 내용 완전성을 주지 않는다.
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    _manifest(out)
    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)

    # ★ 이 시험이 겨누는 층은 **read-back** 이다.
    #
    #   `os.write` 를 한 바이트로 줄이는 리뷰어 반례는 `_write_all()` 의 loop 가
    #   이미 이어서 쓴다 (실측: 그대로는 예외가 안 난다). 그러므로 그 반례가
    #   드러낸 진짜 구멍은 "loop 가 없다" 가 아니라 **"쓴 것을 다시 읽지 않고
    #   final 이름을 붙인다"** 이다. loop 를 통째로 우회해 부분 바이트를 만들고,
    #   그 상태로 이름이 붙는지 본다.
    # ★ 60차 — **겨누는 writer 를 이름으로 고른다.** P0-1 이 굳히는 자리 앞에
    #   내용 봉인 writer 를 하나 더 놓았으므로, `_write_all` 을 통째로 바꾸면
    #   이 시험은 자기 축(등록 레코드의 read-back)이 아니라 봉인의 read-back 을
    #   보게 된다. 그러면 이름이 약속한 축을 한 번도 안 실행한다 (L13 형태).
    _real_write_all = P._write_all

    def _truncated(fd, data, where):
        if where != "execution-class-register":
            return _real_write_all(fd, data, where)
        P.os.write(fd, data[:1])                     # loop 없이 한 바이트만

    monkeypatch.setattr(P, "_write_all", _truncated)
    with pytest.raises(P.PreserveError):
        P.commit_run_outputs(cap, [out])
    # `monkeypatch.undo()` 는 이 시험의 **모든** patch 를 되돌린다 — smoke
    # namespace 까지 되돌아가면 아래 재시도가 canonical 이 된다. 겨눈 것 하나만
    # 되돌린다.
    monkeypatch.setattr(P, "_write_all", _real_write_all)

    cid = P.run_content_id(out)
    assert P.read_execution_class(cid, ledger=led) is None, (
        "부분 바이트가 final 이름으로 공개됐다 (M3)")
    # 그리고 그 자리가 poison 되지 않았다 — 정상 재시도가 된다
    cap2 = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    P.commit_run_outputs(cap2, [out])
    rec = P.read_execution_class(cid, ledger=led)
    assert rec and rec["execution_class"] == P.EXEC_CLASS_SMOKE, (
        f"short write 가 final key 를 poison 했다: {rec!r} (M3)")


# ── M4 ────────────────────────────────────────────────────────────────────
def test_a_shared_local_class_conflict_is_fail_closed(tmp_path, monkeypatch):
    """★ M4 — 두 authority 가 반대말을 하면 **거부**한다.

    리뷰어 반례: clone A 는 같은 내용을 local smoke 로, clone B 는 tracked
    canonical 로 각각 합법 등록한다. B 의 tracked record 가 평범한 VCS 동기화로
    A 에 들어오면 두 valid record 가 공존하고, reader 는 shared 를 먼저 찾아
    canonical 을 돌려주며 local 의 반대 class 를 **안 읽는다**.

    content lock 은 clone 지역이라 Git 으로 들어오는 record 를 직렬화하지 못한다.
    그러므로 reader 가 둘 다 읽고 충돌이면 멈춰야 한다.
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    _manifest(out)
    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    P.commit_run_outputs(cap, [out])
    cid = P.run_content_id(out)

    # 다른 clone 에서 온 tracked canonical record 를 손으로 놓는다 (VCS 동기화)
    # ★ 70차 E5 — 초판은 `"schema": "execution-class/v1"` 키를 하나 더 달았고, 원래
    #   reader 는 그것을 그대로 읽었다 (키 집합을 안 봤다). typed reader 는 닫힌
    #   variant 밖을 거부하므로, 이 시험이 재는 **충돌** 에 닿으려면 레코드가
    #   authority 형식(legacy 4키 — 다른 clone 의 58~61차 레코드가 그 형태다)이어야
    #   한다. 형식 위조를 시험이 기대하고 있었다 — fixture 가 진실을 가리고 있었다.
    shared = P.exec_class_root_for_ledger(led)
    shared.mkdir(parents=True, exist_ok=True)
    (shared / f"{cid}.json").write_text(json.dumps({
        "content_id": cid,
        "execution_class": P.EXEC_CLASS_CANONICAL,
        "evidence": "다른 clone 에서 온 tracked record",
        "recorded_at": "2026-09-08T00:00:00Z"}), encoding="utf-8")

    with pytest.raises(P.PreserveError) as ei:
        P.read_execution_class(cid, ledger=led)
    msg = str(ei.value)
    assert "충돌" in msg or "conflict" in msg, msg
    assert P.EXEC_CLASS_SMOKE in msg and P.EXEC_CLASS_CANONICAL in msg, (
        f"어느 두 class 가 부딪혔는지 말하지 않는다: {msg}")


# ── M13 ───────────────────────────────────────────────────────────────────
def _flaky_fsync(monkeypatch, target: Path, boom: dict, seen: list):
    """`target` 디렉터리의 entry fsync 만 골라 실패시키는 감시자."""
    real = P._fsync_dir_strict

    def _f(d, stage):
        seen.append((Path(d), stage))
        if boom["on"] and Path(d) == target:
            raise P.PreserveError(stage, "directory fsync 가 실패했다 (모의)")
        real(d, stage)

    monkeypatch.setattr(P, "_fsync_dir_strict", _f)


def test_a_retry_after_a_failed_parent_fsync_redoes_the_durability_step(
        tmp_path, monkeypatch):
    """★ M13 — 실패한 parent fsync 를 **재시도가 고쳐야** 한다.

    32차 P0-3 이 `_mkdir_durable()` 에서 이미 배운 문장이다: "mkdir 은 성공했는데
    parent fsync 가 실패한" 상태와 "이미 durable" 한 상태는 **구별할 방법이
    없다**. 그러면 항상 굳혀야 한다 — fsync 는 멱등이고 비용은 재시도 때만 든다.

    실행 class 등록부는 그 교훈을 안 썼다. `os.link()` 는 성공하고 그 뒤
    `_fsync_dir_strict()` 가 실패하면 호출자는 오류를 받는다. 그런데 **같은
    class 로 재시도하면** 함수 머리의 "이미 등록돼 있다" 분기가 파일을 발견하고
    곧장 반환한다 — 이름은 여전히 비내구적인 채로 성공이 보고된다. crash 뒤
    등록이 사라지고, 등록이 없으면 승격은 거부(fail-closed)이므로 **정본 산출이
    되살릴 수 없게 막힌다**.
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    _manifest(out)
    reg = P._exec_class_root_for_class(P.EXEC_CLASS_SMOKE, led)
    cid = P.run_content_id(out)

    seen: list = []
    boom = {"on": True}
    _flaky_fsync(monkeypatch, reg, boom, seen)

    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    with pytest.raises(P.PreserveError):
        P.commit_run_outputs(cap, [out])
    assert (reg / f"{cid}.json").is_file(), (
        "이 시험의 전제가 깨졌다 — 이름이 붙은 뒤 durability 만 실패해야 한다 "
        f"(실패 자리: {[s for _, s in seen]})")

    # 재시도 — 이제 fsync 는 된다. 그런데 굳히러 **가기는** 하는가?
    boom["on"] = False
    seen.clear()
    cap2 = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    P.commit_run_outputs(cap2, [out])
    assert (reg, "execution-class-register") in seen, (
        "같은 class 재시도가 등록부 이름을 다시 굳히지 않았다 — 첫 시도의 "
        f"실패한 parent fsync 가 영원히 안 고쳐진다 (본 fsync: {seen}) (M13)")


def test_the_registry_hierarchy_itself_is_created_durably(tmp_path,
                                                          monkeypatch):
    """★ M13 의 둘째 절반 — 등록부 **디렉터리**도 durable 해야 한다.

    레코드 이름만 굳히고 그 이름을 담는 `_exec_class/`·`_exec_class/local/` 을
    안 굳히면 crash 뒤 층째로 사라진다. 30차 P0-3 이 CAS·pin 에서 고친 것과
    같은 형태이고, 그때 만든 `_mkdir_durable()` 이 답이다.
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    _manifest(out)
    shared = P.exec_class_root_for_ledger(led)
    reg = P._exec_class_root_for_class(P.EXEC_CLASS_SMOKE, led)
    assert not shared.exists(), "이 시험은 등록부가 **없는** 상태에서 시작한다"

    seen: list = []
    _flaky_fsync(monkeypatch, tmp_path / "없는자리", {"on": False}, seen)

    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    P.commit_run_outputs(cap, [out])

    dirs = {d for d, _ in seen}
    assert shared.parent in dirs, (
        f"`_exec_class/` 를 담는 자리를 안 굳혔다 — 층이 통째로 사라질 수 있다 "
        f"(본 자리: {sorted(map(str, dirs))}) (M13)")
    assert shared in dirs, (
        f"`{reg.name}/` 를 담는 자리(`_exec_class/`)를 안 굳혔다 (M13)")
