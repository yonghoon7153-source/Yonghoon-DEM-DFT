"""59차 β (M5·M8·M9) — **판정한 대상과 쓴 대상이 같아야 한다.**

리뷰어의 세 반례는 같은 병이다:

    M5  smoke 판정 직후 그 이름 아래를 bind 로 바꾸면, 판정은 옛 실물을 보고
        쓰기는 새 실물로 간다. 판정과 쓰기 사이가 **창**이다.
    M8  `_verify_declared_bundle()` 이 `is_file()` 로 걷는다 — symlink 를
        따라가므로 저장소 밖 바이트가 묶음 크기에 들어간다.
    M9  `finalize_leg()` 은 caller 의 dict 를 진입에서 검증하고, lock 을 잡고
        원장을 읽은 **한참 뒤에** 얕은 복사로 봉인한다. 그 사이에 dict 가
        바뀌면 검증한 것과 봉인한 것이 다르다.

`[해석]` 이름은 시점의 성질이고 handle 은 대상의 성질이다. 그러므로 판정한
**대상**을 끝까지 들고 가고(M5), 걸을 때는 이름을 따라가지 않으며(M8), 검증한
**값**을 그 자리에서 바이트로 굳힌다(M9).

M6(clean clone frozen authority)은 `row_projection.py` 쪽이라
`tests/test_frozen_clean_clone_59.py` 에 따로 둔다.
"""
from __future__ import annotations

import os
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
    # ★ 60차 P0-2 — class 는 **자리가 정한다.** 시험이 smoke 자리라고 부르는
    #   곳이 실제로 smoke namespace 안이어야 한다 (발급 인자로 강제하던 것이
    #   리뷰어가 지목한 우회로였다).
    if monkeypatch is not None:
        monkeypatch.setattr(P, "SMOKE_NAMESPACE", tmp_path / "results" / "_smoke")
    return led


def _manifest(d: Path, *, curves: str = "aa") -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "curves_manifest.yaml").write_text(f"curves_sha256: {curves}\n",
                                            encoding="utf-8")


# ── M5 ────────────────────────────────────────────────────────────────────
def test_the_capability_is_bound_to_the_directory_the_gate_judged(tmp_path, monkeypatch):
    """★ M5 — gate 가 본 **실물**과 산출을 굳히는 실물이 같아야 한다.

    리뷰어는 bind mount 로 바꿨다. 여기서는 mount 권한 없이 같은 성질을
    시험한다 — 판정한 디렉터리를 치우고 **같은 이름에 다른 실물**을 놓는다.
    커널이 보기에 둘은 다른 대상이고, 이름만 같다. bind swap 이 만드는 상태와
    같은 것이며, 이 시험은 mount 권한이 없는 기계에서도 돈다.

    (mount 를 실제로 쓰는 축은 `test_frozen_coordinate_seal_58.py` 가 이미
     갖고 있다 — 그쪽은 skipif 로 환경을 가린다. 이 성질은 가리지 않는다.)
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    _manifest(out)
    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)

    # 판정 뒤 — 같은 이름, 다른 실물
    moved = tmp_path / "carried-away"
    out.rename(moved)
    _manifest(out, curves="bb")

    with pytest.raises(P.PreserveError) as ei:
        P.commit_run_outputs(cap, [out])
    msg = str(ei.value)
    assert "대상" in msg or "handle" in msg or "실물" in msg, msg

    # 그리고 **아무것도 등록되지 않았다** — 거부하면서 기록하면 그것이 오염이다
    assert P.read_execution_class(P.run_content_id(out), ledger=led) is None


def test_the_capability_reads_the_manifest_through_the_carried_handle(tmp_path, monkeypatch):
    """★ M5 — 등록하는 identity 는 **들고 온 handle 로 읽은** 바이트여야 한다.

    이름으로 다시 열면, 그 순간의 이름이 무엇을 가리키든 그것이 identity 가
    된다. 그러면 "판정한 대상의 class" 가 아니라 "지금 이 이름의 class" 다.

    치우지 않고 **내용만** 바꾼 경우는 정상 거부가 아니다 (산출이 도중에 자라는
    것은 정상이다). 여기서 보는 것은 handle 로 읽는가 하나다.
    """
    led = _ledger(tmp_path, monkeypatch)
    out = tmp_path / "results" / "_smoke" / "run"
    _manifest(out)
    cap = P.issue_execution_class(out, "L", "grid",
                                  ledger=led)
    assert cap.dir_fd is not None, (
        "권한이 판정한 디렉터리의 handle 을 안 들고 있다 (M5)")
    st_fd = os.fstat(cap.dir_fd)
    st_path = out.stat()
    assert (st_fd.st_dev, st_fd.st_ino) == (st_path.st_dev, st_path.st_ino), (
        "권한이 든 handle 이 판정한 디렉터리가 아니다 (M5)")

    P.commit_run_outputs(cap, [out])
    rec = P.read_execution_class(P.run_content_id(out), ledger=led)
    assert rec and rec["execution_class"] == P.EXEC_CLASS_SMOKE


# ── M8 ────────────────────────────────────────────────────────────────────
def test_a_bundle_member_symlink_can_not_smuggle_bytes_from_outside(tmp_path, monkeypatch):
    """★ M8 — 묶음 구성원을 걸을 때 **이름을 따라가지 않는다**.

    `files = sorted(x for x in d.rglob("*") if x.is_file())` 의 `is_file()` 은
    symlink 를 따라간다. 그래서 저장소 밖 파일을 가리키는 link 하나가 개수에도
    바이트 합계에도 들어간다 — `full_bundle` 의 뜻은 "clone 한 사람이 이 결과를
    검증할 수 있는 묶음이 실재한다" 인데, clone 에는 그 바이트가 없다.

    58차 L7 이 `bundle_uri` 자신에 대해 고친 것과 **같은 흡수**다. 그때 뿌리만
    고치고 구성원은 안 고쳤다.
    """
    root = tmp_path / "repo"
    bundle = root / "bundle"
    bundle.mkdir(parents=True)
    (bundle / "real.txt").write_text("in-repo\n", encoding="utf-8")

    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.bin").write_bytes(b"x" * 4096)
    (bundle / "link.bin").symlink_to(outside / "secret.bin")

    # ★ 60차 P0-8 이후 index 는 **묶음 안**에 있어야 한다. 밖에 두면 이 시험이
    #   재는 것(link 를 따라가는가)이 아니라 index 위치 검사가 먼저 걸려서,
    #   변이를 심어도 같은 이유로 빨개진다 — 즉 아무것도 안 재게 된다.
    idx = bundle / "index.json"
    idx.write_text("{}\n", encoding="utf-8")
    import hashlib
    ev = {
        "bundle_uri": "bundle",
        # link 를 파일로 세면 real.txt · link.bin · index.json = 3 이다
        "bundle_files": 3,
        "payload_bytes": len("in-repo\n") + 4096 + len("{}\n"),
        "payload_index": "bundle/index.json",
        "payload_index_sha256": hashlib.sha256(idx.read_bytes()).hexdigest(),
    }
    bad = P._verify_declared_bundle(ev, repo_root=root)
    assert bad, (
        "저장소 밖을 가리키는 link 가 묶음 구성원으로 통과했다 — clone 에는 "
        "그 바이트가 없다 (M8)")
    assert any("link.bin" in b for b in bad), bad


def test_a_bundle_of_plain_files_still_passes(tmp_path, monkeypatch):
    """M8 의 반대 방향 — 정상 묶음까지 막으면 그것은 경계가 아니라 마비다."""
    import hashlib

    root = tmp_path / "repo"
    bundle = root / "bundle"
    (bundle / "sub").mkdir(parents=True)
    (bundle / "a.txt").write_text("a\n", encoding="utf-8")
    (bundle / "sub" / "b.txt").write_text("bb\n", encoding="utf-8")
    # ★ 60차 P0-8 — index 는 **묶음 안**에 있어야 한다. 밖에 두면 묶음만 받은
    #   사람에게 그것을 인증한다는 목록이 없다 (`full_bundle` 의 뜻이 성립하지
    #   않는다). 그래서 이 정상 묶음도 index 를 안에 둔다.
    # ★ 70차 E3 — 초판 index 는 `{}` 였다. 60차 reader 는 그것을 "구성원을 열거하지
    #   않는 형식" 으로 보고 대조를 **건너뛰어** 통과시켰다 — 실물 `payload_sha256.yaml`
    #   (YAML) 도 같은 경로로 빠졋다. 이제 열거하지 않는 index 는 거부이므로, 정상
    #   묶음은 production 형식(`경로: sha256`)의 index 를 가진다. `{}` 로 초록이던
    #   것은 fixture 가 진실을 가리고 있었다는 뜻이다.
    import yaml
    idx = bundle / "payload_sha256.yaml"
    members = {"a.txt": hashlib.sha256(b"a\n").hexdigest(),
               "sub/b.txt": hashlib.sha256(b"bb\n").hexdigest()}
    idx.write_text(yaml.safe_dump(members, sort_keys=True), encoding="utf-8")
    ev = {
        "bundle_uri": "bundle",
        "bundle_files": 3,
        "payload_bytes": 2 + 3 + idx.stat().st_size,
        "payload_index": "bundle/payload_sha256.yaml",
        "payload_index_sha256": hashlib.sha256(idx.read_bytes()).hexdigest(),
    }
    assert P._verify_declared_bundle(ev, repo_root=root) == []


# ── M9 ────────────────────────────────────────────────────────────────────
def test_finalize_seals_the_evidence_it_verified(tmp_path, monkeypatch):
    """★ M9 — 검증한 evidence 와 봉인한 evidence 가 **같은 값**이어야 한다.

    `finalize_leg()` 은 진입에서 caller dict 를 검증하고 (도메인·묶음·JSON),
    lock 을 잡고 원장을 읽은 **한참 뒤에** `dict(evidence)` 로 봉인한다. 그
    복사는 얕으므로 중첩 값은 여전히 공유되고, 애초에 그 사이에 dict 자체가
    바뀔 수 있다.

    이 시험은 그 사이를 결정적으로 재현한다 — lock 을 기다리는 동안 다른
    스레드가 고친 것과 같은 상태를, 그 구간에서 불리는 함수로 만든다.
    """
    import tests.test_preserve as TP
    from tools.preserve import (CLAIM_PHASES, open_leg_run, finalize_leg)
    import yaml

    led = TP._lifecycle_ledger(tmp_path)
    claim = open_leg_run("L", TP._RUN_SPEC_L, "0123456789abcdef",
                              ledger=led)
    for ph in CLAIM_PHASES:
        claim.phase_done(ph, {"n": ph})

    evidence = {"leg_source_digest": "0123456789abcdef",
                "cohorts": ["gA"],
                "note": {"seen": "before"}}
    real = P.assert_planned_index_consistent

    def _mutating(*a, **k):
        # lock 을 잡고 원장을 읽는 구간 — 검증은 이미 끝났고 봉인은 아직이다
        evidence["note"]["seen"] = "after"
        evidence["injected"] = "late"
        return real(*a, **k)

    monkeypatch.setattr(P, "assert_planned_index_consistent", _mutating)
    finalize_leg("L", evidence, ledger=led, token=claim.token)
    monkeypatch.undo()

    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    sealed = next(e for e in doc["legs"] if e["leg_id"] == "L")["evidence"]
    assert sealed["note"]["seen"] == "before", (
        f"검증한 뒤 바뀐 값이 원장에 봉인됐다: {sealed['note']!r} — 검증한 것과 "
        "기록한 것이 다르면 검증은 아무것도 보장하지 않는다 (M9)")
    assert "injected" not in sealed, (
        f"검증 뒤에 끼워 넣은 키가 원장에 들어갔다: {sorted(sealed)} (M9)")
