"""보존 트랜잭션 회귀 (계약 v4 묶음 9) — 25차 리뷰의 acceptance 목록.

이 파일의 핵심 불변식은 하나다:

    **어느 단계에서 멈추든 public index 는 오염되지 않는다.**

8월 20일 사고의 원인은 도구 부재가 아니라 강제 부재였다 — 다리를 만들고 보존을
안 해도 아무 일도 일어나지 않았다. 그래서 여기서 보는 것은 "성공했을 때 잘
되는가" 가 아니라 **"실패했을 때 등록이 안 되는가"** 다.

리뷰가 준 실패 목록을 그대로 fixture 로 고정한다. 새 실패 모드를 추가하면
`tools.preserve.FAULTS` 와 이 파일이 함께 늘어야 하고, 아래
`test_every_declared_fault_has_a_regression` 이 그것을 강제한다.

hermetic 이다 — 실제 산출물·`results/`·network 를 쓰지 않는다.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import tempfile
import uuid
from pathlib import Path
from unittest import mock

import pytest

from tools.preserve import (FAULTS, CasBackend, Hooks, PlannedLeg, PreserveError,
                            canonical_bytes, digest, finalize_only, index_entries,
                            is_registered, load_canonical, publish, restore_from_cas,
                            run_transaction, seal_payload, verify_payload,
                            verify_registered_receipt, check_receipt,
                            check_manifest, load_canonical,
                            assert_durable_retention, has_registration_journal,
                            check_envelope, check_output, check_output_claim, check_hook_validation,
                            pin_set_digest, ENFORCEMENT_OBJECT_LOCK, ENFORCEMENT_ADVISORY, registration,
                            MIN_RETENTION_DAYS, ObjectLockBackend, LockedCasBackend)
from tools.preserve import _is_hex64 as _is_hex64_str
from tools.preserve import RETENTION_SCHEMA as P_RETENTION_SCHEMA
from tools.preserve import STORE_SCHEMA as P_STORE_SCHEMA
from tools.preserve import _reg_file as _reg_path

#: 저장소 루트 (`tests/` 의 부모) — 소스를 읽어 계약을 대조하는 시험이 쓴다.
ROOT = Path(__file__).resolve().parents[1]

#: 고정 fixture 바이트 — 여기서 기대 semantic digest 가 결정된다.
_FITS = b"PAR1" + b"\x11" * 512 + b"PAR1"
_EXPECTED_SEM = hashlib.sha256(_FITS).hexdigest()

#: ★ 26차 P1-7 — 정본은 자유문자 label 이 아니라 design digest 다.
_DESIGN_SHA = hashlib.sha256(b"p22_halfcell_2x2_v6/fixture").hexdigest()

PLANNED = PlannedLeg(
    leg_id="hc22p_v6_armA_b20",
    protocol_generation="v6",
    pairing_design_sha256=_DESIGN_SHA,
    design_label="p22_halfcell_2x2_v6",          # hash 밖
    source_digest="deadbeefcafe0001",
    objectives=("pocv_dvdq", "pocv_dvdq_dqdv"),
    total_start_budget=20,
    candidate_mode="legacy_slot_replace",
)


def _nonempty(v) -> bool:
    return isinstance(v, str) and v != ""


def _make_run(tmp: Path) -> Path:
    """작은 hermetic run_dir. 실제 fits 를 흉내만 낸다."""
    d = tmp / "run"
    (d / "_inputs").mkdir(parents=True)
    (d / "fits.parquet").write_bytes(_FITS)
    (d / "manifest.yaml").write_text("leg: hc22p_v6_armA_b20\n", encoding="utf-8")
    (d / "_inputs" / "base.yaml").write_text("noise: 0.001\n", encoding="utf-8")
    (d / "run_spec.json").write_text(json.dumps({
        "planned_id": PLANNED.planned_id(),
        "source_digest": PLANNED.source_digest,
    }), encoding="utf-8")
    return d


def _hooks(expected: str | None = _EXPECTED_SEM) -> Hooks:
    def validate(root):
        # 복원본 **안에서만** 읽는다. 원본 경로를 보면 이 검증은 거짓말이 된다.
        need = ["fits.parquet", "manifest.yaml", "_inputs/base.yaml"]
        miss = [n for n in need if not (Path(root) / n).is_file()]
        return {"ok": not miss, "fail": miss, "checks": {n: True for n in need}}

    def rescore(root):
        data = (Path(root) / "fits.parquet").read_bytes()
        # 실제 산출 파일을 만든다 — byte 축이 없으면 "무엇을 만들었는가" 가
        # receipt 어디에도 없다 (27차 P1-5).
        out = Path(root) / "_rescored.json"
        out.write_bytes(canonical_bytes({"n": len(data)}))
        return {"role": "rescored_summary",
                "canonicalizer": "score-semantic/v1",
                "semantic_schema": "degeneracy-summary/v6",
                "semantic_sha256": hashlib.sha256(data).hexdigest(),
                "relative_path": "_rescored.json",
                "byte_size": out.stat().st_size,
                "file_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                "producer": "test-fixture/v1",
                # ★ 30차 P1-2 — role 별 필수 필드. 초판은 이 다섯이 optional
                #   이라 "무엇으로부터 만들었는가" 가 receipt 에 없었다.
                "produced_from": "fits.parquet",
                "source_file_sha256": hashlib.sha256(data).hexdigest(),
                "n_rows": 1,
                "semantic_view_drops": ["_채점원본"]}

    return Hooks(validate=validate, rescore=rescore,
                 min_retention_days=365, expected_semantic=expected)


@pytest.fixture()
def kit(tmp_path):
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    return run, backend, index


# ─────────────────────────────────────────────────────────────────────────────
# 성공 경로
# ─────────────────────────────────────────────────────────────────────────────

def test_happy_path_publishes_exactly_one_immutable_entry(kit):
    run, backend, index = kit
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    assert res["ok"]
    entries = index_entries(index)
    assert list(entries) == [PLANNED.leg_id]
    e = entries[PLANNED.leg_id]
    assert e["planned_id"] == PLANNED.planned_id()
    assert e["payload_root_digest"] == res["payload_root_digest"]
    assert not backend.orphans(), "성공했는데 staging 에 찌꺼기가 남았다"
    # 영수증이 계획·payload·backend 를 전부 들고 있다
    r = res["receipt"]
    for k in ("planned_envelope", "payload_root_digest", "backend_uri",
              "payload_manifest_digest", "receipt_digest", "outputs"):
        assert r.get(k), k


def test_rerunning_the_same_transaction_is_idempotent(kit):
    """같은 digest · 같은 바이트 → 재시도가 안전해야 한다 (crash 후 복구)."""
    run, backend, index = kit
    a = run_transaction(PLANNED, run, backend, index, _hooks())
    b = run_transaction(PLANNED, run, backend, index, _hooks())
    assert a["payload_root_digest"] == b["payload_root_digest"]
    assert list(index_entries(index)) == [PLANNED.leg_id]


def test_same_leg_id_with_different_bytes_is_refused(kit):
    """같은 ID 를 다른 내용으로 덮으려 하면 immutable index 가 거부한다."""
    run, backend, index = kit
    run_transaction(PLANNED, run, backend, index, _hooks())
    with pytest.raises(PreserveError) as ei:
        publish(index, {"leg_id": PLANNED.leg_id, "planned_id": "다른",
                        "receipt_digest": "x", "receipt_object": "o",
                        "payload_root_digest": "y",
                        "payload_manifest_digest": "m",
                        "backend_uri": backend.uri})
    assert "immutable" in str(ei.value)


def test_canonical_bytes_are_stable_under_key_order(kit):
    a = {"b": 2, "a": [3, {"z": 1, "y": 2}]}
    b = {"a": [3, {"y": 2, "z": 1}], "b": 2}
    assert canonical_bytes(a) == canonical_bytes(b)
    assert digest(a) == digest(b)
    assert b"\n" not in canonical_bytes(a), "후행 개행·들여쓰기가 섞이면 안 된다"


# ─────────────────────────────────────────────────────────────────────────────
# 실패 경로 — 전부 "public index 가 비어 있어야 한다"
# ─────────────────────────────────────────────────────────────────────────────

#: (fault, 멈춰야 할 단계). 단계 이름이 바뀌면 여기서 걸린다.
_FAULT_STAGE = [
    ("member_bit_flip",       "payload_seal"),
    ("member_missing",        "payload_seal"),
    ("member_extra",          "payload_seal"),
    ("stale_payload_index",   "payload_seal"),
    ("partial_upload",        "cas_put"),
    ("read_back_corrupt",     "read_back"),
    ("no_read_access",        "read_back"),
    ("restore_incomplete",    "empty_root_restore"),
    ("cas_drop_member",       "cas_restore"),
    ("cas_drop_manifest",     "cas_restore"),
    ("cas_drop_all",          "cas_restore"),
    ("cas_mutate_member",     "cas_restore"),
    ("validator_raises",      "validate"),
    ("validator_fails",       "validate"),
    ("score_raises",          "rescore"),
    ("wrong_semantic_digest", "rescore"),
    ("wrong_planned_id",      "planned_seal"),
    ("wrong_source_digest",   "planned_seal"),
    ("retention_too_short",   "capability"),
    ("crash_before_publish",  "publish"),
]


@pytest.mark.parametrize("fault,stage", _FAULT_STAGE)
def test_a_failed_transaction_never_reaches_the_public_index(kit, fault, stage):
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({fault}))
    assert ei.value.stage == stage, (
        f"{fault}: {ei.value.stage!r} 에서 멈췄다 — {stage!r} 를 기대했다")
    assert index_entries(index) == {}, (
        f"{fault}: 실패했는데 public index 에 항목이 생겼다")


def test_crash_after_publish_leaves_the_entry_but_not_a_registration(kit):
    """publish 뒤 등록 전에 죽으면 — index 는 남고 등록은 안 된 상태.

    이것이 two-phase 의 유일한 "중간" 상태다. 재시도가 idempotent 하므로
    다시 돌리면 닫힌다. 조용히 성공으로 치면 안 된다.
    """
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({"crash_after_publish"}))
    assert ei.value.stage == "register"
    assert list(index_entries(index)) == [PLANNED.leg_id]
    assert not is_registered(index, PLANNED.leg_id, backend)
    # 재시도로 닫힌다 — 계산을 다시 돌리지 않는다 (`finalize_only`)
    assert finalize_only(PLANNED.leg_id, backend, index)["ok"]


def test_partial_upload_leaves_an_orphan_not_an_object(kit):
    """중간에 끊긴 업로드는 `objects/` 에 나타나지 않는다."""
    run, backend, index = kit
    with pytest.raises(PreserveError):
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({"partial_upload"}))
    objs = list((backend.root / "objects").rglob("*")) if (backend.root / "objects").is_dir() else []
    assert not [p for p in objs if p.is_file()], "끊긴 업로드가 object 로 승격됐다"
    assert backend.orphans(), "orphan 이 남아야 GC 대상이 된다"


def test_transaction_refuses_to_run_without_verification_hooks(kit):
    """검증 hook 이 없으면 시작조차 하지 않는다 — 검증 없는 통과 경로 금지."""
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index,
                        Hooks(validate=None, rescore=None))
    assert ei.value.stage == "hooks"
    assert index_entries(index) == {}


def test_restore_target_must_be_a_truly_empty_root(kit):
    """복원본 검증이 원본 경로를 보면 그 검증은 거짓말이다.

    `restore_incomplete` 로 복원본에서 파일 하나를 지웠을 때 실패해야 한다.
    실패하지 않는다면 검증기가 원본을 보고 있다는 뜻이다.
    """
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({"restore_incomplete"}))
    assert ei.value.stage == "empty_root_restore"
    assert (run / "fits.parquet").is_file(), "원본은 손대지 않아야 한다"


def test_payload_verification_catches_all_three_shapes(tmp_path):
    """누락·추가·변조 — manifest 대 실물 대조가 셋 다 잡는가."""
    run = _make_run(tmp_path)
    man = seal_payload(run)
    assert verify_payload(run, man) == []

    (run / "__extra__").write_bytes(b"x")
    assert any("manifest 에 없는" in m for m in verify_payload(run, man))
    (run / "__extra__").unlink()

    b = bytearray((run / "fits.parquet").read_bytes())
    b[10] ^= 0x01
    (run / "fits.parquet").write_bytes(bytes(b))
    assert any("바이트 불일치" in m for m in verify_payload(run, man))

    (run / "fits.parquet").unlink()
    assert any("실물이 없는" in m for m in verify_payload(run, man))


def test_every_declared_fault_has_a_regression():
    """`FAULTS` 에 이름을 더하고 회귀를 안 쓰는 것을 막는다.

    이것이 없으면 실패 모드 목록이 문서처럼 늘어나기만 하고 아무도 검사하지
    않는다 — 이 저장소가 여러 번 겪은 형태다.
    """
    covered = ({f for f, _ in _FAULT_STAGE} | {"crash_after_publish"}
               | {"receipt_drop_after_readback", "receipt_mutate_after_readback",
                  "receipt_drop_after_publish"})
    missing = sorted(FAULTS - covered)
    assert not missing, f"회귀가 없는 fault: {missing}"
    stray = sorted(covered - FAULTS)
    assert not stray, f"`FAULTS` 에 없는 이름을 검사한다: {stray}"


# ─────────────────────────────────────────────────────────────────────────────
# 26차 P0 — 복원은 **CAS 에서만** 나와야 한다
# ─────────────────────────────────────────────────────────────────────────────

def test_restore_reads_the_backend_not_the_original_run_dir(kit):
    """★ 26차 P0-1 — 초판은 원본 `run_dir` 를 복사했다. false-green 이었다.

    member 와 manifest 를 CAS 에 넣고 되읽기까지 했지만, 되읽은 bytes 는 해시만
    확인하고 **버렸다**. 실제 복원은 `hooks.restore(man, run_dir, root)` 로
    보존 전 원본에서 왔다. 즉 "빈 root 로 복원해 검증했다" 는 주장이 거짓이었다.

    리뷰가 준 반례 그대로 검사한다: **업로드 뒤 원본을 지운다.** 보존 체계가
    제 일을 한다면 그래도 전부 성공해야 한다.
    """
    run, backend, index = kit
    res = run_transaction(PLANNED, run, backend, index, _hooks(),
                          drop_source_after_seal=True)
    assert res["ok"]
    assert not run.exists(), "원본이 지워진 채로 끝나야 이 시험이 의미가 있다"
    assert list(index_entries(index)) == [PLANNED.leg_id]


@pytest.mark.parametrize("what", ["member", "manifest", "all"])
def test_deleting_cas_objects_fails_before_publish(kit, what):
    """★ 26차 P0-1 — CAS object 를 지우면 publish 전에 멈춰야 한다.

    초판은 read-back 직후 CAS 를 통째로 비워도 publish 까지 성공했다.
    복원이 backend 를 안 봤기 때문이다.
    """
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({f"cas_drop_{what}"}))
    assert ei.value.stage in ("cas_restore", "read_back"), ei.value.stage
    assert index_entries(index) == {}


def test_mutating_a_cas_object_fails_before_publish(kit):
    """CAS 안의 바이트를 바꾸면 content address 와 어긋나 실패한다."""
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({"cas_mutate_member"}))
    assert ei.value.stage in ("cas_restore", "read_back")
    assert index_entries(index) == {}


# ─────────────────────────────────────────────────────────────────────────────
# 26차 P0-2 — 영수증은 저장돼야 하고, 등록은 상태 변경이어야 한다
# ─────────────────────────────────────────────────────────────────────────────

def test_the_receipt_itself_is_stored_and_retrievable(kit):
    """★ 26차 P0-2 — 초판은 receipt 를 메모리에서 만들고 digest 만 기록했다.

    public index 가 **회수할 수 없는** digest 를 가리켰다. 그 digest 로 무엇도
    되찾을 수 없으니 감사가 불가능하다.
    """
    run, backend, index = kit
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    e = index_entries(index)[PLANNED.leg_id]
    raw = backend.read_back(e["receipt_object"])          # 회수된다
    got = load_canonical(raw)
    assert got["leg_id"] == PLANNED.leg_id
    assert got["payload_root_digest"] == res["payload_root_digest"]


def test_crash_after_publish_resumes_with_finalize_only(kit):
    """★ 26차 P0-2 — 재시도가 **계산 전체를 다시 돌리는 것**이면 안 된다.

    초판 시험은 같은 결정론 hook 으로 transaction 을 통째로 다시 실행했다.
    실제 사고에서는 원본 계산이 12시간짜리고, crash 뒤 남은 것은 CAS 와 index
    뿐이다. 그 상태에서 **원본 없이** 이어서 끝낼 수 있어야 한다.
    """
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({"crash_after_publish"}))
    assert ei.value.stage == "register"
    assert list(index_entries(index)) == [PLANNED.leg_id]
    assert not is_registered(index, PLANNED.leg_id, backend), "등록은 아직 아니다"

    shutil.rmtree(run)                                    # 원본이 없다
    out = finalize_only(PLANNED.leg_id, backend, index)
    assert out["ok"] and is_registered(index, PLANNED.leg_id, backend)


def test_registration_is_a_durable_state_change_not_a_return(kit):
    """등록이 단순 `return` 이면 프로세스가 죽는 순간 사라진다."""
    run, backend, index = kit
    assert not is_registered(index, PLANNED.leg_id, backend)
    run_transaction(PLANNED, run, backend, index, _hooks())
    assert is_registered(index, PLANNED.leg_id, backend)


# ─────────────────────────────────────────────────────────────────────────────
# 26차 P1-3 — 계획·semantic 결속은 optional 이면 안 된다
# ─────────────────────────────────────────────────────────────────────────────

def test_missing_run_spec_is_fail_closed(kit):
    """★ 초판은 `run_spec.json` 이 없으면 봉인값을 default 로 채워 통과시켰다.

    그것은 "실행이 계획을 기록했다" 의 증명이 아니라 그 반대다.
    """
    run, backend, index = kit
    (run / "run_spec.json").unlink()
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks())
    assert ei.value.stage == "planned_seal"
    assert index_entries(index) == {}


def test_expected_semantic_is_mandatory(kit):
    """`expected_semantic=None` 이면 재채점 결과를 아무 것도 대조하지 않는다."""
    run, backend, index = kit
    h = _hooks()
    h.expected_semantic = None
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, h)
    assert ei.value.stage in ("hooks", "rescore")
    assert index_entries(index) == {}


@pytest.mark.parametrize("bad", [
    {},                                           # 비었다
    {"semantic_sha256": None},                    # null
    {"semantic_sha256": "x" * 64},                # schema/role 누락
    {"role": "r", "semantic_sha256": "short"},    # 64-hex 아님
])
def test_malformed_output_manifest_is_refused(kit, bad):
    """산출 manifest 는 role · canonicalizer · schema · 64-hex digest 를 갖춰야 한다."""
    run, backend, index = kit
    h = _hooks()
    h.rescore = lambda root: dict(bad)
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, h)
    assert ei.value.stage == "rescore"
    assert index_entries(index) == {}


# ─────────────────────────────────────────────────────────────────────────────
# 26차 P1-4 — publish 는 동시 writer 에서 항목을 잃으면 안 된다
# ─────────────────────────────────────────────────────────────────────────────

def test_concurrent_publish_of_different_legs_loses_nothing(tmp_path):
    """★ 26차 P1-4 — read-modify-write 는 원자적이지 않았다.

    두 writer 가 같은 옛 index 를 읽으면 마지막 쓰기가 앞을 덮어 항목이
    사라진다. 초판 회귀는 **순차** publish 만 봤으므로 이 race 를 놓쳤다.
    """
    index = tmp_path / "index"
    import threading

    errs: list[BaseException] = []

    def w(i: int):
        try:
            publish(index, {"leg_id": f"leg_{i}", "planned_id": f"p{i}",
                            "receipt_digest": "d" * 64, "receipt_object": "o" * 64,
                            "payload_root_digest": "r" * 64,
                            "payload_manifest_digest": "m" * 64,
                            "backend_uri": "x"})
        except BaseException as e:                        # noqa: BLE001
            errs.append(e)

    ts = [threading.Thread(target=w, args=(i,)) for i in range(16)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not errs, errs
    assert len(index_entries(index)) == 16, "동시 publish 에서 항목이 사라졌다"


def test_concurrent_publish_of_the_same_leg_admits_exactly_one(tmp_path):
    """같은 leg 를 서로 다른 내용으로 동시에 쓰면 정확히 하나만 성공한다."""
    index = tmp_path / "index"
    import threading

    ok, refused = [], []

    def w(i: int):
        try:
            publish(index, {"leg_id": "same", "planned_id": f"p{i}",
                            "receipt_digest": "d" * 64, "receipt_object": "o" * 64,
                            "payload_root_digest": "r" * 64,
                            "payload_manifest_digest": "m" * 64,
                            "backend_uri": "x"})
            ok.append(i)
        except PreserveError:
            refused.append(i)

    ts = [threading.Thread(target=w, args=(i,)) for i in range(12)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert len(ok) == 1, f"성공 {len(ok)}건 — 정확히 하나여야 한다"
    assert len(refused) == 11
    assert len(index_entries(index)) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 27차 P0 — receipt lifecycle 과 등록이 다시 false-green 이었다
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("fault", ["receipt_drop_after_readback",
                                   "receipt_mutate_after_readback",
                                   "receipt_drop_after_publish"])
def test_losing_the_receipt_after_readback_stops_the_transaction(kit, fault):
    """★ 27차 P0-1 — 한 번의 read-back 은 회수 가능성 불변식이 아니다.

    `_drop_from_cas()` 는 receipt 가 만들어지기 **전에만** 돌았다. 그래서
    receipt 를 되읽은 직후 지워도 트랜잭션이 성공하고 등록까지 됐다 —
    index 가 다시 **회수 불가능한** receipt 를 가리켰다. 26차 P0-2 의 결과가
    그대로 재현된 것이다.

    등록 직전에 index 가 가리키는 receipt 를 **다시 회수해** 대조한다.
    """
    run, backend, index = kit
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({fault}))
    assert ei.value.stage in ("receipt", "verify_before_register"), ei.value.stage
    assert not is_registered(index, PLANNED.leg_id, backend), "등록되면 안 된다"


def test_finalize_only_never_recomputes(kit):
    """★ 27차 P0-2 — `finalize_only()` 가 validate/rescore 를 다시 돌렸다.

    `_finalize()` 를 다시 호출했으므로 CAS payload restore → validate →
    rescore → **새 receipt 생성**까지 반복했다. "재계산 없이 CAS 만으로" 는
    사실이 아니었고, analyzer 환경이 조금만 달라도 새 receipt 가 달라져
    immutable publish 에서 복구가 실패한다.

    이제 hook 을 **인자로 받지 않는다** — 구조적으로 재계산이 불가능하다.
    """
    run, backend, index = kit
    calls = {"validate": 0, "rescore": 0}
    h = _hooks()
    v0, r0 = h.validate, h.rescore
    h.validate = lambda root: (calls.__setitem__("validate", calls["validate"] + 1)
                               or v0(root))
    h.rescore = lambda root: (calls.__setitem__("rescore", calls["rescore"] + 1)
                              or r0(root))

    with pytest.raises(PreserveError):
        run_transaction(PLANNED, run, backend, index, h,
                        faults=frozenset({"crash_after_publish"}))
    before = dict(calls)
    shutil.rmtree(run)

    out = finalize_only(PLANNED.leg_id, backend, index)      # ← hooks 없음
    assert out["ok"] and is_registered(index, PLANNED.leg_id, backend)
    assert calls == before, (
        f"finalize_only 가 다시 계산했다: {before} → {calls}")


def test_finalize_only_fails_closed_without_a_retrievable_receipt(kit):
    """indexed receipt 가 없거나 다르면 **재생성하지 말고 멈춘다**."""
    run, backend, index = kit
    with pytest.raises(PreserveError):
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({"crash_after_publish"}))
    e = index_entries(index)[PLANNED.leg_id]
    backend._obj(e["receipt_object"]).unlink()               # receipt 를 잃는다

    with pytest.raises(PreserveError) as ei:
        finalize_only(PLANNED.leg_id, backend, index)
    assert ei.value.stage in ("finalize_only", "read_back",
                              "verify_before_register")
    assert not is_registered(index, PLANNED.leg_id, backend)


def test_a_foreign_registration_journal_is_refused(kit):
    """★ 27차 P0-2 — journal 이 "파일이 있다" 만으로 등록 완료였다.

    `_register()` 는 `_exclusive_write` 가 False 를 돌려줘도 기존 내용을
    비교하지 않았고, `is_registered()` 는 JSON 을 읽지도 않았다. 다른
    `receipt_object` 를 가진 journal 을 미리 심어 두면 트랜잭션이 `ok=True` 를
    돌려주면서 등록은 남의 것을 가리켰다.
    """
    run, backend, index = kit
    j = index / "registered" / f"{PLANNED.leg_id}.json"
    j.parent.mkdir(parents=True, exist_ok=True)
    j.write_bytes(canonical_bytes({"leg_id": PLANNED.leg_id,
                                   "receipt_object": "f" * 64}))
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks())
    assert ei.value.stage == "register"


@pytest.mark.parametrize("blob", [b"", b"{oops", b"null"])
def test_a_truncated_registration_journal_is_not_a_registration(kit, blob):
    """잘린 파일·빈 파일·JSON 아닌 것은 등록이 아니다."""
    run, backend, index = kit
    j = index / "registered" / f"{PLANNED.leg_id}.json"
    j.parent.mkdir(parents=True, exist_ok=True)
    j.write_bytes(blob)
    assert not is_registered(index, PLANNED.leg_id, backend)


# ─────────────────────────────────────────────────────────────────────────────
# 27차 P1-3 — 배타 생성은 crash-atomic durable record 가 아니었다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_partially_written_index_entry_is_never_visible(tmp_path):
    """★ 27차 P1-3 — final pathname 을 먼저 만들고 한 번 `os.write` 했다.

    부분 쓰기를 확인하지 않고 parent directory 도 fsync 하지 않았다. 5 bytes 만
    쓰이면 `publish_created=True` 인데 다음 `index_entries()` 는
    `JSONDecodeError` 였고, immutable 파일 때문에 재시도로도 복구가 안 됐다.

    final name 은 **완성된 파일**에만 붙어야 한다.
    """
    index = tmp_path / "index"
    entry = {"leg_id": "x", "planned_id": "p", "receipt_digest": "d" * 64,
             "receipt_object": "o" * 64, "payload_root_digest": "r" * 64,
             "payload_manifest_digest": "m" * 64, "backend_uri": "u"}
    publish(index, entry)
    assert index_entries(index)["x"] == entry

    # 중간에 죽은 흔적(temp)이 남아도 index 는 읽힌다
    (index / "legs" / "x.json.tmp.deadbeef").write_bytes(b"{trunc")
    assert index_entries(index)["x"] == entry


def test_publish_requires_the_fields_finalize_only_will_use(tmp_path):
    """`publish()` 가 안 받는 키를 `finalize_only()` 가 무조건 쓰면 KeyError 다."""
    index = tmp_path / "index"
    with pytest.raises(PreserveError):
        publish(index, {"leg_id": "x", "planned_id": "p",
                        "receipt_digest": "d" * 64, "backend_uri": "u",
                        "payload_root_digest": "r" * 64})   # receipt_object 없음
    assert index_entries(index) == {}


# ─────────────────────────────────────────────────────────────────────────────
# 27차 P1-4 — manifest·ID 가 closed schema 로 결속되지 않았다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_manifest_member_cannot_escape_the_restore_root(kit):
    """★ 27차 P1-4 — `../escaped.bin` 이 restore root **밖에** 파일을 썼다."""
    run, backend, index = kit
    man = seal_payload(run)
    man["members"][0]["path"] = "../escaped.bin"
    man["root_digest"] = digest({k: v for k, v in man.items() if k != "root_digest"})
    dg = backend.put_if_absent(canonical_bytes(man))["digest"]

    root = Path(tempfile.mkdtemp())
    with pytest.raises(PreserveError) as ei:
        restore_from_cas(backend, dg, root)
    assert ei.value.stage == "cas_restore"
    assert not (root.parent / "escaped.bin").exists()


@pytest.mark.parametrize("mut", [
    ("schema", "bogus/v9"),
    ("n_members", 999),
    ("total_bytes", 1),
    ("root_digest", "0" * 64),
])
def test_a_manifest_that_lies_about_itself_is_refused(kit, mut):
    """schema·집계·root digest 가 실물과 어긋나면 거부한다."""
    run, backend, index = kit
    man = dict(seal_payload(run))
    man[mut[0]] = mut[1]
    dg = backend.put_if_absent(canonical_bytes(man))["digest"]
    with pytest.raises(PreserveError) as ei:
        restore_from_cas(backend, dg, Path(tempfile.mkdtemp()))
    assert ei.value.stage == "cas_restore"


def test_duplicate_member_paths_are_refused(kit):
    run, backend, index = kit
    man = seal_payload(run)
    man["members"].append(dict(man["members"][0]))
    man["n_members"] = len(man["members"])
    man["total_bytes"] = sum(m["bytes"] for m in man["members"])
    man["root_digest"] = digest({k: v for k, v in man.items() if k != "root_digest"})
    dg = backend.put_if_absent(canonical_bytes(man))["digest"]
    with pytest.raises(PreserveError):
        restore_from_cas(backend, dg, Path(tempfile.mkdtemp()))


@pytest.mark.parametrize("bad", ["../../escaped", "a/b", ".", "..", "", "x" * 200,
                                 "CON", "with space"])
def test_a_leg_id_cannot_escape_the_index_directory(tmp_path, bad):
    """★ 27차 P1-4 — `leg_id` 가 path component 로 그대로 보간됐다.

    `leg_id='../../escaped'` publish 가 `index/` **밖에** 파일을 만들고
    `index_entries()` 에는 아무 항목도 남기지 않았다.
    """
    index = tmp_path / "index"
    with pytest.raises(PreserveError) as ei:
        publish(index, {"leg_id": bad, "planned_id": "p",
                        "receipt_digest": "d" * 64, "receipt_object": "o" * 64,
                        "payload_root_digest": "r" * 64,
                        "payload_manifest_digest": "m" * 64, "backend_uri": "u"})
    assert "leg_id" in str(ei.value)
    assert not list(tmp_path.rglob("*escaped*"))


# ─────────────────────────────────────────────────────────────────────────────
# 27차 P1-5 — 산출 manifest 가 byte output 을 증명하지 않았다
# ─────────────────────────────────────────────────────────────────────────────

def test_output_manifest_must_bind_real_bytes(kit):
    """`relative_path`·`byte_size`·`file_sha256`·producer 없이 publish 되면 안 된다."""
    run, backend, index = kit
    h = _hooks()
    h.rescore = lambda root: {"role": "r", "canonicalizer": "c",
                              "semantic_schema": "s",
                              "semantic_sha256": _EXPECTED_SEM}
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, h)
    assert ei.value.stage == "rescore"
    assert index_entries(index) == {}


# ─────────────────────────────────────────────────────────────────────────────
# 28차 P0 — 등록은 **object graph retention commit** 이어야 한다
# ─────────────────────────────────────────────────────────────────────────────

class _DropAfterRead(CasBackend):
    """읽은 직후 object 를 지우는 backend — TOCTOU 를 구조로 재현한다.

    ★ 28차 P0-1 — "등록 직전 한 번 더 읽는다" 는 **또 하나의 검사 시점**일 뿐
      retention 구조가 아니다. 마지막 read 가 bytes 를 돌려준 직후 지우면
      초판은 `ok=True · is_registered=True` 인데 receipt 가 없었다.
    """

    def __init__(self, *a, victims=(), **kw):
        super().__init__(*a, **kw)
        object.__setattr__(self, "_victims", set(victims))
        object.__setattr__(self, "_armed", False)

    def arm(self):
        object.__setattr__(self, "_armed", True)

    def read_back(self, dg, *, faults=frozenset()):
        data = super().read_back(dg, faults=faults)
        if self._armed and (not self._victims or dg in self._victims):
            self._obj(dg).unlink(missing_ok=True)
        return data


def test_registration_requires_the_whole_graph_to_survive_deletion(tmp_path):
    """★ 28차 P0-1 — `registered ⇒ 도달 가능한 graph 전체가 회수 가능하다`.

    receipt 만이 아니다. manifest·member·산출까지 **pin** 아래 있어야 한다.
    읽은 직후 `objects/` 에서 지워도 등록이 살아 있어야 하고, pin 까지 지우면
    등록이 죽어야 한다.
    """
    run = _make_run(tmp_path)
    backend = _DropAfterRead(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    assert res["ok"]

    # pin 이 있으므로 `objects/` 를 통째로 비워도 등록은 유효하다
    shutil.rmtree(backend.root / "objects")
    assert is_registered(index, PLANNED.leg_id, backend), (
        "pin 이 graph 를 붙들지 못했다")

    # pin 까지 지우면 등록이 죽는다 — 존재만으로 완료가 아니다
    shutil.rmtree(backend.root / "pins")
    assert not is_registered(index, PLANNED.leg_id, backend)


def test_deleting_an_object_right_after_the_final_read_blocks_registration(tmp_path):
    """마지막 read 직후 삭제되는 backend 에서는 등록이 성립하면 안 된다."""
    run = _make_run(tmp_path)
    backend = _DropAfterRead(root=tmp_path / "cas")
    index = tmp_path / "index"
    backend.arm()                                   # 모든 read 뒤 삭제
    with pytest.raises(PreserveError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    assert not is_registered(index, PLANNED.leg_id, backend)


def test_finalize_only_rechecks_the_graph_even_when_already_registered(tmp_path):
    """★ 28차 P0-1 — `already=True` 를 backend 를 안 보고 돌려줬다.

    등록된 뒤에 receipt·member·산출을 하나씩 잃으면 fail-closed 여야 한다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    assert finalize_only(PLANNED.leg_id, backend, index)["already"] is True

    # pin 안의 object 하나를 잃으면 더는 등록 상태가 아니다
    pins = sorted((backend.root / "pins" / PLANNED.leg_id).iterdir())
    assert pins, "pin 이 하나도 없다"
    pins[0].unlink()
    shutil.rmtree(backend.root / "objects", ignore_errors=True)
    assert not is_registered(index, PLANNED.leg_id, backend)
    with pytest.raises(PreserveError):
        finalize_only(PLANNED.leg_id, backend, index)


# ─────────────────────────────────────────────────────────────────────────────
# 28차 P0-2 — receipt validator 가 닫혀 있지 않았다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_forged_seven_key_receipt_is_refused(tmp_path):
    """★ 28차 P0-2 — self-consistent 한 일곱 키 receipt 가 등록됐다.

    `verify_registered_receipt()` 는 exact key set, `planned_id ==
    H(planned_envelope)`, 실제 backend URI, outputs schema 를 보지 않았다.
    """
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    forged = {"schema": "execution-receipt/v1", "leg_id": "x",
              "planned_id": "p" * 64, "payload_root_digest": "r" * 64,
              "payload_manifest_digest": "m" * 64,
              "backend_uri": "file+cas:///foreign"}
    forged["receipt_digest"] = digest(forged)
    obj = backend.put_if_absent(canonical_bytes(forged))["digest"]
    publish(index, {"leg_id": "x", "planned_id": forged["planned_id"],
                    "receipt_digest": forged["receipt_digest"],
                    "receipt_object": obj,
                    "payload_root_digest": forged["payload_root_digest"],
                    "payload_manifest_digest": forged["payload_manifest_digest"],
                    "backend_uri": "file+cas:///foreign"})
    with pytest.raises(PreserveError) as ei:
        finalize_only("x", backend, index)
    assert ei.value.stage in ("verify_before_register", "receipt_schema")
    assert not is_registered(index, "x", backend)


def test_a_receipt_naming_another_backend_is_refused(tmp_path):
    """receipt 와 index 가 서로 같은 문자열만 가지면 통과하면 안 된다.

    **실제로 손에 든 backend 의 URI** 와 대조해야 한다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    other = CasBackend(root=tmp_path / "cas2")
    shutil.copytree(backend.root, other.root, dirs_exist_ok=True)
    with pytest.raises(PreserveError) as ei:
        verify_registered_receipt(other, index, PLANNED.leg_id)
    assert "backend" in str(ei.value)


# ─────────────────────────────────────────────────────────────────────────────
# 28차 P1-1 — 산출은 자기신고가 아니라 측정·보존돼야 한다
# ─────────────────────────────────────────────────────────────────────────────

def test_output_bytes_are_measured_by_the_wrapper_and_kept_in_cas(tmp_path):
    """★ 28차 P1-1 — hook 이 자기 파일의 SHA 와 producer 를 자기신고했다.

    `check_output()` 은 root 를 받지 않아 파일을 열지 않았고, 산출 파일은
    restore temp root 와 함께 삭제됐다. descriptor 는 "있는 필드" 일 뿐
    회수 가능한 증거가 아니었다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    out = res["receipt"]["outputs"][0]
    assert _is_hex64_str(out["object_digest"]), out
    got = backend.read_back(out["object_digest"])       # temp root 삭제 뒤에도
    assert hashlib.sha256(got).hexdigest() == out["file_sha256"]
    assert out["byte_size"] == len(got)


def test_a_lying_output_descriptor_is_overruled_by_measurement(tmp_path):
    """자기신고 size/SHA 가 실물과 다르면 실패해야 한다."""
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    h = _hooks()
    base = h.rescore

    def lying(root):
        d = dict(base(root))
        d["file_sha256"] = "b" * 64
        d["byte_size"] = 999
        return d

    h.rescore = lying
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, h)
    assert ei.value.stage == "rescore"
    assert index_entries(index) == {}


@pytest.mark.parametrize("rel", ["../escape.bin", "/abs/x", "C:\\x", "", "."])
def test_an_output_path_cannot_escape_the_restore_root(tmp_path, rel):
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    h = _hooks()
    base = h.rescore
    h.rescore = lambda root: dict(base(root), relative_path=rel)
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, h)
    assert ei.value.stage == "rescore"


# ─────────────────────────────────────────────────────────────────────────────
# 28차 P1-3 — manifest 집계 타입 · 빈 root
# ─────────────────────────────────────────────────────────────────────────────

def test_boolean_aggregates_are_not_integers(kit):
    """`True == 1` 이므로 한 member 짜리 manifest 의 집계를 bool 로 바꿔도 통과했다."""
    run, backend, index = kit
    man = seal_payload(run)
    man = dict(man, members=man["members"][:1])
    man["n_members"] = True
    man["total_bytes"] = True
    man["root_digest"] = digest({k: v for k, v in man.items() if k != "root_digest"})
    dg = backend.put_if_absent(canonical_bytes(man))["digest"]
    with pytest.raises(PreserveError):
        restore_from_cas(backend, dg, Path(tempfile.mkdtemp()))


def test_restore_refuses_a_root_that_is_not_empty(kit):
    """이름이 `truly empty root` 인데 기존 파일이 있어도 성공했다."""
    run, backend, index = kit
    man = seal_payload(run)
    dg = backend.put_if_absent(canonical_bytes(man))["digest"]
    for m in man["members"]:
        backend.put_if_absent((run / m["path"]).read_bytes())
    root = Path(tempfile.mkdtemp())
    (root / "stowaway.bin").write_bytes(b"x")
    with pytest.raises(PreserveError) as ei:
        restore_from_cas(backend, dg, root)
    assert ei.value.stage == "cas_restore"
    assert (root / "stowaway.bin").exists(), "남의 파일을 지우지도 않는다"


# ─────────────────────────────────────────────────────────────────────────────
# 29차 P0 — 정본은 journal 자기신고가 아니라 **pinned receipt graph** 다
# ─────────────────────────────────────────────────────────────────────────────

def test_pinning_twice_never_truncates_the_cas_original(tmp_path):
    """★ 29차 P0-4 — pin fallback 이 CAS 원본을 **파괴**했다.

    `os.link` 의 모든 `OSError` 를 잡아 `dst.write_bytes(src.read_bytes())` 로
    떨어졌다. `EEXIST` 도 그리로 갔고, `dst` 는 CAS `src` 와 **같은 inode** 라
    `O_TRUNC` 로 열리는 순간 content-addressed 원본까지 잘렸다.

    보존 체계가 보존 대상을 지우는 경로였다.
    """
    backend = CasBackend(root=tmp_path / "cas")
    dg = backend.put_if_absent(b"abc")["digest"]
    backend.pin("legx", [dg])
    backend.pin("legx", [dg])                       # 두 번째 — EEXIST 경로
    assert backend.read_back(dg) == b"abc", "CAS 원본이 손상됐다"
    assert backend.read_pinned("legx", dg) == b"abc"

    # 미리 심어 둔 **다른 내용**의 pin 은 거부돼야 한다
    other = backend._pin("legy", dg)
    other.parent.mkdir(parents=True, exist_ok=True)
    other.write_bytes(b"not abc")
    with pytest.raises(PreserveError):
        backend.pin("legy", [dg])
    assert backend.read_back(dg) == b"abc"


def test_a_journal_that_declares_a_subset_is_not_a_registration(tmp_path):
    """★ 29차 P0-1 — 등록 graph 의 정본이 journal 자기신고였다.

    `is_registered()` 는 journal 의 `objects` 목록과 그것으로 다시 계산한
    `pin_set_digest` 만 봤다. pinned receipt 를 열어 graph 를 **재유도**하지
    않으므로, receipt 하나만 적은 journal 도 스스로 일관되면 "등록 완료" 였다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    assert is_registered(index, PLANNED.leg_id, backend)

    e = index_entries(index)[PLANNED.leg_id]
    j = index / "registered" / f"{PLANNED.leg_id}.json"
    subset = [e["receipt_object"]]
    j.unlink()
    j.write_bytes(canonical_bytes({
        "leg_id": PLANNED.leg_id, "receipt_object": e["receipt_object"],
        "objects": subset,
        "pin_set_digest": digest({"leg_id": PLANNED.leg_id, "objects": subset})}))
    assert not is_registered(index, PLANNED.leg_id, backend), (
        "journal 이 스스로 적은 subset 을 그대로 믿었다")
    with pytest.raises(PreserveError):
        finalize_only(PLANNED.leg_id, backend, index)


def test_a_registration_copied_to_another_backend_is_not_registered(tmp_path):
    """★ 29차 P0-1 — already-registered 경로가 actual backend 를 우회했다.

    CAS 와 pins 를 다른 backend root 로 복사하면 `is_registered` 도
    `finalize_only` 도 통과했다 — receipt 의 `backend_uri` 는 옛 backend 인데도.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas1")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())

    other = CasBackend(root=tmp_path / "cas2")
    shutil.copytree(backend.root, other.root, dirs_exist_ok=True)
    assert not is_registered(index, PLANNED.leg_id, other), (
        "다른 backend 인데 등록됐다고 한다")
    with pytest.raises(PreserveError) as ei:
        finalize_only(PLANNED.leg_id, other, index)
    assert "backend" in str(ei.value)


def test_deleting_a_pin_after_commit_makes_the_leg_unregistered(tmp_path):
    """★ 29차 P0-2 — `verify_pins()` 와 `_register()` 사이 TOCTOU.

    성공 반환과 journal 존재가 retention 을 뜻할 수 없다. **`registered` 는
    저장된 비트가 아니라 backend 에 대고 지금 평가하는 술어**여야 한다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    assert is_registered(index, PLANNED.leg_id, backend)

    e = index_entries(index)[PLANNED.leg_id]
    backend._pin(PLANNED.leg_id, e["receipt_object"]).unlink()
    shutil.rmtree(backend.root / "objects", ignore_errors=True)
    assert not is_registered(index, PLANNED.leg_id, backend)


# ─────────────────────────────────────────────────────────────────────────────
# 29차 P0-3 — receipt validator 가 바깥 키만 닫혔다
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mut", [
    {"planned_envelope": {"anything": "goes"}},
    {"validation": {"ok": True, "n_checks": True}},
    {"validation": {"ok": True, "n_checks": 3, "surplus": "x"}},
    {"n_members": 999},
    {"total_bytes": 999},
    {"payload_root_digest": "b" * 64},
    {"retention_days": 0},
])
def test_nested_receipt_contract_is_closed(tmp_path, mut):
    """★ 29차 P0-3 — nested 값이 무엇이든 통과했다.

    `planned_envelope` 가 exact `planned-leg/v2` 인지, `validation` 의 키가
    닫혔는지, receipt 의 집계·root 가 **실제 manifest** 와 같은지, retention 이
    정책을 넘는지 — 전부 안 봤다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())

    rec = dict(res["receipt"], **mut)
    rec.pop("receipt_digest", None)
    rec["receipt_digest"] = digest(rec)
    e = dict(index_entries(index)[PLANNED.leg_id])
    for k in ("payload_root_digest", "receipt_digest"):
        if k in rec:
            e[k] = rec[k]
    bad = check_receipt(rec, e, backend, manifest=load_canonical(
        backend.read_back(rec["payload_manifest_digest"])))
    assert bad, f"{mut} 가 통과했다"


def test_an_output_descriptor_must_match_its_cas_object(tmp_path):
    """산출 descriptor 의 `file_sha256` 이 `object_digest` 와 달라도 통과했다."""
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    rec = dict(res["receipt"])
    rec["outputs"] = [dict(rec["outputs"][0], object_digest="c" * 64)]
    rec.pop("receipt_digest")
    rec["receipt_digest"] = digest(rec)
    e = dict(index_entries(index)[PLANNED.leg_id], receipt_digest=rec["receipt_digest"])
    bad = check_receipt(rec, e, backend, manifest=load_canonical(
        backend.read_back(rec["payload_manifest_digest"])))
    assert bad


# ─────────────────────────────────────────────────────────────────────────────
# 29차 P1-1 — Windows 에서 CAS 가 바이트를 바꿨다
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("blob", [
    b"a\nb", b"a\r\nb", b"\x00\x01\x02", bytes(range(256)), b"", b"\x1a",
])
def test_cas_round_trips_arbitrary_bytes(tmp_path, blob):
    """★ 29차 P1-1 — `os.open` 에 `O_BINARY` 가 없어 newline 이 번역됐다.

    리뷰 실측: `b'a\\nb'` → 저장된 것이 `b'a\\r\\nb'`. digest 가 어긋나
    happy path 부터 무너졌다 (native Windows 44건 실패).
    """
    backend = CasBackend(root=tmp_path / "cas")
    dg = backend.put_if_absent(blob)["digest"]
    assert backend.read_back(dg) == blob
    backend.pin("legx", [dg])
    assert backend.read_pinned("legx", dg) == blob


def test_manifest_paths_cannot_collide_by_case_or_unicode(kit):
    """★ 29차 P1-3 — exact 문자열 중복만 봤다.

    `A.txt`/`a.txt` 와 NFC/NFD 짝이 같은 대상 파일이 되는 filesystem 이 있다.
    """
    import unicodedata

    run, backend, index = kit
    base = seal_payload(run)
    for a, b in (("A.txt", "a.txt"),
                 (unicodedata.normalize("NFC", "é.txt"),
                  unicodedata.normalize("NFD", "é.txt"))):
        man = dict(base)
        m0 = dict(base["members"][0])
        man["members"] = [dict(m0, path=a), dict(m0, path=b)]
        man["n_members"] = 2
        man["total_bytes"] = 2 * m0["bytes"]
        man["root_digest"] = digest({k: v for k, v in man.items()
                                     if k != "root_digest"})
        assert check_manifest(man), f"{a!r}/{b!r} 충돌을 놓쳤다"


# ─────────────────────────────────────────────────────────────────────────────
# 30차 P0 — 등록 성공의 **마지막 창**과 backend identity
# ─────────────────────────────────────────────────────────────────────────────

class _DropPinAfterRead(CasBackend):
    """`read_pinned()` 가 bytes 를 돌려준 **직후** 그 pin 을 지우는 backend.

    ★ 30차 P0-1 — 29차의 `_DropAfterRead` 는 `read_back()` 의 `objects/` 만
      건드렸다. 리뷰가 준 반례는 그 다음 창이다: post-commit
      `verify_registered_graph()` 가 전수 읽기를 마친 뒤 **비-output** pin
      (receipt·manifest·member) 을 지우면,

        · `on_disk` snapshot 은 삭제 **전**이라 통과하고
        · `verify_pins()` 는 이미 bytes 를 받았으므로 `pbad=[]` 이고
        · 두 번째로 읽는 것은 output 뿐이라 지워진 셋을 다시 보지 않는다

      → 함수가 성공을 반환하는 순간 receipt·manifest·member pin 이 없다.
    """

    def __init__(self, *a, victims=(), **kw):
        super().__init__(*a, **kw)
        object.__setattr__(self, "_victims", set(victims))

    def arm(self, victims):
        object.__setattr__(self, "_victims", set(victims))

    def read_pinned(self, leg_id, dg, *, version=None):
        data = super().read_pinned(leg_id, dg, version=version)
        if dg in self._victims:
            self._pin(leg_id, dg).unlink(missing_ok=True)
        return data


def test_registration_fails_when_pins_vanish_during_the_final_sweep(tmp_path):
    """★ 30차 P0-1 — 전수 읽기 **도중** 사라진 graph 로 성공하면 안 된다.

    member pin 을 겨냥한다. member 는 마지막 전수 읽기(`verify_pins`) 에서
    **딱 한 번** 읽히므로, 그 직후 지우면 리뷰가 지목한 창이 정확히 열린다:
    앞의 `on_disk` snapshot 은 삭제 전이고, 뒤의 두 번째 읽기는 output 뿐이다.

    성공의 뜻이 "그 순간 한 번 읽혔다" 로 남으면 검사 지점을 뒤로 옮긴 것일
    뿐이다. 성공은 **retention 상태**여야 한다.
    """
    run = _make_run(tmp_path)
    backend = _DropPinAfterRead(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    assert res["ok"]

    man = load_canonical(backend.read_pinned(
        PLANNED.leg_id, res["receipt"]["payload_manifest_digest"]))
    members = {m["sha256"] for m in man["members"]}
    outs = {o["object_digest"] for o in res["receipt"]["outputs"]}
    victims = members - outs
    assert victims, "member 가 전부 산출과 겹치면 이 반례가 성립하지 않는다"
    backend.arm(victims)

    with pytest.raises(PreserveError):
        finalize_only(PLANNED.leg_id, backend, index)


def test_a_local_backend_never_claims_enforced_retention(tmp_path):
    """★ 30차 P0-1 — `ok=True` 가 durable retention 을 뜻하면 안 된다.

    local filesystem 은 object-lock 을 강제하지 못한다 (이 저장소의 실행
    환경은 uid 0 이라 mode bit 조차 잠금이 아니다). 그러면 성공을 durable
    retention 이라고 부르는 대신 **강제 수준을 값으로 신고**해야 한다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())

    lease = res["retention"]
    assert lease["enforcement"] == "advisory_local"
    assert res["durable"] is False
    with pytest.raises(PreserveError) as ei:
        assert_durable_retention(backend, index, PLANNED.leg_id)
    assert "advisory" in ei.value.msg


def test_is_registered_without_a_backend_is_not_available(tmp_path):
    """★ 30차 P0-2 — 이름 하나가 "journal 주장" 과 "보존 완료" 를 겸했다.

    정상 등록 뒤 `pins/` 와 `objects/` 를 모두 지워도 backend 없는 호출은
    참이었다. 판정 API 에서 backend 를 **필수**로 만들고, journal 존재는
    다른 이름으로 분리한다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())

    shutil.rmtree(backend.root / "pins")
    shutil.rmtree(backend.root / "objects")

    assert has_registration_journal(index, PLANNED.leg_id) is True
    assert is_registered(index, PLANNED.leg_id, backend) is False
    with pytest.raises(TypeError):
        is_registered(index, PLANNED.leg_id)          # backend 생략 불가


def test_a_relative_root_does_not_make_two_stores_the_same(tmp_path, monkeypatch):
    """★ 30차 P0-2 — identity 가 `file+cas://{self.root}` 문자열뿐이었다.

    `root=Path("cas")` 로 등록한 뒤 cwd 를 바꾸면 **다른** `cas/` 를 가리키면서
    URI 는 계속 `file+cas://cas` 다. 기존 foreign-backend 회귀는 서로 다른
    절대 tmp path 만 시험하므로 이 반례를 놓친다.

    store 를 `store.json` 까지 통째로 복사해 **store_id 축을 일부러 무력화**
    한다. 그래야 이 시험이 URI 정규화 하나만을 시험한다 — 두 축이 함께 있으면
    한쪽을 지워도 초록이라 어느 것도 시험하지 못한다.
    """
    a, b = tmp_path / "a", tmp_path / "b"
    (a / "cas").mkdir(parents=True)
    b.mkdir(parents=True)
    run = _make_run(tmp_path)

    monkeypatch.chdir(a)
    backend = CasBackend(root=Path("cas"))
    index = a / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    assert is_registered(index, PLANNED.leg_id, backend)

    # 같은 상대 경로, **같은 store_id**, 다른 실제 store
    shutil.copytree(a / "cas", b / "cas")
    monkeypatch.chdir(b)
    other = CasBackend(root=Path("cas"))
    assert other.store_id == backend.store_id, "이 시험은 URI 축만 봐야 한다"
    assert is_registered(index, PLANNED.leg_id, other) is False


def test_a_recreated_store_at_the_same_path_is_not_the_same_store(tmp_path):
    """★ 30차 P0-2 — 경로는 재사용·재마운트·bind mount 로 겹칠 수 있다.

    URI 축을 일부러 무력화한다 (경로가 **같다**). 남는 것은 생성 시각에
    고정되는 store UUID 하나다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    assert is_registered(index, PLANNED.leg_id, backend)

    old_id = backend.store_id
    (backend.root / "store.json").unlink()                # store 를 다시 만든다
    assert backend.store_id != old_id
    assert is_registered(index, PLANNED.leg_id, backend) is False


def test_a_receipt_must_name_the_store_it_was_written_to(tmp_path):
    """★ 30차 P0-2 — receipt 자체도 store 를 이름해야 한다.

    lease 축과 별개다. lease 가 통과해도 receipt 가 다른 store 를 이름하면
    거부돼야 하므로, validator 를 직접 시험한다 (end-to-end 로는 lease 검사가
    먼저 걸려 이 축이 한 번도 실행되지 않는다).
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    e = index_entries(index)[PLANNED.leg_id]
    man = load_canonical(backend.read_back(res["receipt"]["payload_manifest_digest"]))

    assert check_receipt(res["receipt"], e, backend, manifest=man) == []
    forged = dict(res["receipt"], backend_store_id="0" * 32)
    bad = check_receipt(forged, e, backend, manifest=man)
    assert any("backend_store_id" in x for x in bad), bad


def test_the_retention_primitive_checks_store_identity_on_its_own(tmp_path):
    """★ 30차 P0-2 — `verify_retention()` 은 **혼자서도** store 를 봐야 한다.

    end-to-end 로는 receipt 의 `backend_store_id` 검사가 먼저 걸려 이 축이
    한 번도 실행되지 않는다 (변이로 확인했다 — lease 의 store 검사를 지워도
    전체는 초록이었다). primitive 를 직접 시험한다: 리뷰가 요구한
    `verify_retention(receipt, actual_backend)` 은 receipt graph 와 무관하게
    "이 lease 가 이 store 의 것인가" 에 답할 수 있어야 한다.
    """
    backend = CasBackend(root=tmp_path / "cas")
    blob = b"retained-bytes"
    dg = backend.put_if_absent(blob)["digest"]
    lease = backend.retain("legX", [dg], min_retention_days=MIN_RETENTION_DAYS)

    assert backend.verify_retention("legX", lease["lease_digest"])["objects"] == [dg]
    assert backend.retrieve_retained(lease, dg) == blob
    with pytest.raises(PreserveError) as ei:
        backend.retrieve_retained(lease, "0" * 64)
    assert "담보하지 않은" in ei.value.msg

    # 같은 경로에서 store 를 다시 만들면 같은 store 가 아니다
    (backend.root / "store.json").unlink()
    with pytest.raises(PreserveError) as ei:
        backend.verify_retention("legX", lease["lease_digest"])
    assert "store" in ei.value.msg


def test_a_lease_below_the_policy_floor_is_refused(tmp_path):
    """★ 30차 P1-3 — retention 하한이 receipt 의 **자기신고 숫자**였다.

    리뷰의 반례: 3650일로 만든 뒤 같은 root 를 `retention_days=1` 로 다시
    열면 URI·pin 이 같으므로 통과했다. lease 검증이 **지금 backend** 를 본다.
    """
    backend = CasBackend(root=tmp_path / "cas")
    dg = backend.put_if_absent(b"x")["digest"]
    lease = backend.retain("legX", [dg], min_retention_days=3650)

    reopened = CasBackend(root=tmp_path / "cas", retention_days=1)
    with pytest.raises(PreserveError) as ei:
        reopened.verify_retention("legX", lease["lease_digest"])
    assert "retention" in ei.value.msg

    # 정책 하한 미만은 애초에 만들 수 없다
    with pytest.raises(PreserveError):
        backend.retain("legY", [dg], min_retention_days=MIN_RETENTION_DAYS - 1)


def test_the_registration_journal_is_an_exact_typed_graph(tmp_path):
    """★ 30차 P1-1 — duplicate·surplus·거짓 `pin_set_digest` 가 통과했다.

    `set(journal.objects) == expected` 만 봤으므로 정상 목록의 digest 하나를
    **한 번 더** 넣어도 통과했고, `pin_set_digest` 는 64-hex 모양만 봤다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    j = index / "registered" / f"{PLANNED.leg_id}.json"
    good = load_canonical(j.read_bytes())

    def rewrite(rec):
        j.unlink()
        j.write_bytes(canonical_bytes(rec))
        return is_registered(index, PLANNED.leg_id, backend)

    assert rewrite(good) is True
    # 1. duplicate — set 비교로는 안 잡힌다
    assert rewrite(dict(good, objects=good["objects"] + [good["objects"][0]])) is False
    # 2. surplus key
    assert rewrite(dict(good, surplus="x")) is False
    # 3. pin_set_digest 를 다른 leg 이름으로 계산 — 모양은 64-hex 다
    assert rewrite(dict(good, pin_set_digest=pin_set_digest("other", good["objects"]))) is False
    # 4. 정렬을 깬 목록
    assert rewrite(dict(good, objects=list(reversed(good["objects"])))) is False
    # 5. lease_digest 누락
    broken = {k: v for k, v in good.items() if k != "lease_digest"}
    assert rewrite(broken) is False


# ─────────────────────────────────────────────────────────────────────────────
# 30차 P1-2 — nested domain. 리뷰가 그대로 적어준 값들이 통과했다.
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("field,value", [
    ("protocol_generation", 7),
    ("protocol_generation", "generation-six"),
    ("source_digest", 7),
    ("source_digest", "deadbeef"),                 # 16-hex 가 아니다
    ("objectives", [7]),
    ("objectives", []),
    ("objectives", ["b", "a"]),                    # 정렬되지 않음
    ("objectives", ["a", "a"]),                    # 중복
    ("total_start_budget", -1),
    ("total_start_budget", 0),
    ("total_start_budget", True),                  # `True == 1`
    ("candidate_mode", 7),
    ("candidate_mode", "whatever"),
    ("min_retention_days", 1),
    ("leg_id", ""),
    ("pairing_design_sha256", "not-hex"),
])
def test_the_planned_envelope_has_value_domains_not_just_keys(field, value):
    """★ 30차 P1-2 — 초판은 design SHA 하나만 검사했다.

    리뷰가 적은 값들이 domain 오류 없이 transaction 에 도달했다:

        protocol_generation = 7 · source_digest = 7 · objectives = [7]
        total_start_budget = -1 · candidate_mode = 7

    seal 시점(`PlannedLeg.__post_init__`)과 복구 시점(`check_receipt`)이
    **같은 함수**를 쓴다.
    """
    good = PLANNED.envelope()
    assert check_envelope(good) == []
    bad = check_envelope(dict(good, **{field: value}))
    assert bad, f"{field}={value!r} 가 통과했다"

    kw = {"leg_id": PLANNED.leg_id, "protocol_generation": PLANNED.protocol_generation,
          "pairing_design_sha256": PLANNED.pairing_design_sha256,
          "source_digest": PLANNED.source_digest,
          "objectives": PLANNED.objectives,
          "total_start_budget": PLANNED.total_start_budget,
          "candidate_mode": PLANNED.candidate_mode}
    if field in kw:
        kw[field] = value
        with pytest.raises(PreserveError) as ei:
            PlannedLeg(**kw)
        assert ei.value.stage == "planned_seal"


@pytest.mark.parametrize("v", [
    {"ok": "yes", "fail": [], "checks": {"a": True}},      # truthiness
    {"ok": 1, "fail": [], "checks": {"a": True}},
    {"ok": True, "fail": [], "checks": "x"},               # checks 가 dict 아님
    {"ok": True, "fail": [], "checks": {}},                # 빈 checks
    {"ok": True, "fail": ["실패했다"], "checks": {"a": True}},   # ok 와 모순
    {"ok": False, "fail": [], "checks": {"a": True}},            # 반대 모순
    {"ok": True, "fail": [], "checks": {"a": True}, "surplus": 1},
])
def test_the_validator_hook_result_has_a_domain(v):
    """★ 30차 P1-2 — hook 결과의 `ok` 를 truthiness 로 봤다.

    `{"ok":"yes","checks":"x"}` 가 통과한 뒤 receipt 에는
    `{"ok":true,"n_checks":1}` 로 **정규화**됐다. 저장된 nested object 가
    exact 하더라도 그 값이 실제 validator 결과를 증명하지 못했다는 뜻이다.
    """
    assert check_hook_validation({"ok": True, "fail": [], "checks": {"a": True}}) == []
    assert check_hook_validation(v), f"{v!r} 가 통과했다"


def test_a_hook_returning_a_lying_result_stops_the_transaction(tmp_path):
    """위 domain 이 **실제 트랜잭션 경로**에서도 걸리는가."""
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    h = _hooks()
    h.validate = lambda root: {"ok": "yes", "fail": [], "checks": "x"}
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, h)
    assert ei.value.stage == "validate"
    assert index_entries(index) == {}


@pytest.mark.parametrize("field,value", [
    ("role", 7),
    ("role", "invented_role"),
    ("canonicalizer", {}),
    ("semantic_schema", [1]),
    ("producer", False),
    ("n_rows", -1),
    ("n_rows", True),
    ("semantic_view_drops", "not-a-list"),
    ("source_file_sha256", "short"),
    ("produced_from", ""),
])
def test_output_descriptors_are_a_tagged_union_not_a_bag_of_nonempty(field, value):
    """★ 30차 P1-2 — 8개 키의 nonempty 여부만 봤다.

    리뷰가 적은 조합이 실제 path/hash/size 와 함께 등록 가능했다:

        role = 7 · canonicalizer = {} · semantic_schema = [1] · producer = False

    `measured_by`·`produced_from`·`source_file_sha256`·`n_rows`·
    `semantic_view_drops` 의 role 별 필수 여부와 타입은 정의조차 없었다.
    """
    good = {"role": "rescored_summary", "canonicalizer": "score-semantic/v1",
            "semantic_schema": "degeneracy-summary/v6",
            "semantic_sha256": "a" * 64, "relative_path": "out.json",
            "byte_size": 12, "file_sha256": "b" * 64, "producer": "p/v1",
            "object_digest": "b" * 64, "measured_by": "tools.preserve",
            "produced_from": "fits.parquet", "source_file_sha256": "c" * 64,
            "n_rows": 3, "semantic_view_drops": ["_채점원본"]}
    assert check_output(good) == []
    assert check_output(dict(good, **{field: value})), f"{field}={value!r} 가 통과했다"


def test_a_hook_cannot_self_report_the_fields_the_wrapper_measures():
    """★ 28차 P1-1 의 구조화 — 증명과 주장의 주체를 이름으로 가른다."""
    claim = {"role": "rescored_rows", "canonicalizer": "score-semantic/v1",
             "semantic_schema": "rows/v1", "semantic_sha256": "a" * 64,
             "relative_path": "out.tsv", "byte_size": 12,
             "file_sha256": "b" * 64, "producer": "p/v1",
             "produced_from": "fits.parquet", "source_file_sha256": "c" * 64,
             "n_rows": 3}
    assert check_output_claim(claim) == []
    bad = check_output_claim(dict(claim, object_digest="b" * 64))
    assert any("wrapper 측정 필드" in x for x in bad), bad


@pytest.mark.parametrize("path", [7, "../escape.bin", "/abs/x", "a\\b", "C:x",
                                  "a//b", "./x", ""])
def test_manifest_member_paths_have_a_domain_at_seal_time(path):
    """★ 30차 P1-2 — `check_manifest()` 가 member path 를 안 봤다.

    `path=7`·`../x`·absolute·backslash·colon 을 가진 self-consistent manifest
    가 graph 검증을 통과하고 **실제 복원에서만** 실패했다.
    """
    man = {"schema": "payload-manifest/v1", "n_members": 1, "total_bytes": 3,
           "members": [{"path": path, "bytes": 3, "sha256": "a" * 64}]}
    man["root_digest"] = digest({k: v for k, v in man.items()})
    bad = check_manifest(man)
    assert any("path" in b for b in bad), (path, bad)


# ─────────────────────────────────────────────────────────────────────────────
# 30차 P0-3 — fsync fail-closed · 상위 directory edge · crash/reopen drill
# ─────────────────────────────────────────────────────────────────────────────

def test_a_failing_directory_fsync_is_an_error_not_a_shrug(tmp_path, monkeypatch):
    """★ 30차 P0-3 — `_fsync_dir()` 실패를 `False` 로 돌리고 **무시**했다.

    object publish 도 pin 도 반환값을 안 봤다. CAS 와 index 가 다른
    filesystem 이면 power loss 뒤 journal 만 남는 ordering 이 그대로 가능했다.
    """
    import tools.preserve as P

    backend = CasBackend(root=tmp_path / "cas")
    backend.put_if_absent(b"warmup")                  # capability 를 먼저 캐시

    monkeypatch.setattr(P, "_fsync_dir", lambda d: False)
    with pytest.raises(PreserveError) as ei:
        backend.put_if_absent(b"payload-that-needs-a-new-prefix-dir")
    assert "fsync" in ei.value.msg


def test_directory_fsync_capability_is_cached_per_device_not_per_anchor(tmp_path,
                                                                       monkeypatch):
    """★ 30차 P0-3 — 캐시 키가 `resolve().anchor` 였다.

    POSIX 에서는 서로 다른 ext4/NFS/FUSE mount 가 전부 `/` 하나로 합쳐져,
    한 mount 의 capability 가 다른 mount 의 답이 됐다. 두 경로에 서로 다른
    `st_dev` 를 주고, 한쪽의 답이 다른 쪽으로 새는지 **동작으로** 본다.
    """
    import tools.preserve as P

    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    monkeypatch.setattr(P, "_DIR_FSYNC", {})

    real_stat = os.stat

    class _Fake:
        def __init__(self, st, dev):
            self._st, self.st_dev = st, dev

        def __getattr__(self, k):
            return getattr(self._st, k)

    def fake_stat(path, *args, **kw):
        st = real_stat(path, *args, **kw)
        return _Fake(st, 111 if str(path) == str(a) else
                     (222 if str(path) == str(b) else st.st_dev))

    calls: list[str] = []
    real_open = os.open

    def counting_open(path, *args, **kw):
        if str(path) in (str(a), str(b)):
            calls.append(str(path))
        return real_open(path, *args, **kw)

    monkeypatch.setattr(os, "stat", fake_stat)
    monkeypatch.setattr(os, "open", counting_open)

    assert P.dir_fsync_supported(a) is True
    assert P.dir_fsync_supported(a) is True          # 캐시 적중 — 다시 안 연다
    assert calls.count(str(a)) == 1
    assert P.dir_fsync_supported(b) is True
    assert calls.count(str(b)) == 1, "다른 device 인데 a 의 답을 재사용했다"
    assert set(P._DIR_FSYNC) == {"dev:111", "dev:222"}


def test_new_directory_levels_flush_their_parent_entry(tmp_path, monkeypatch):
    """★ 30차 P0-3 — `objects/<prefix>` 와 `pins/<leg>` 만 flush 했다.

    그 이름을 **담는** `objects/` · `pins/` entry 는 flush 되지 않아, crash 뒤
    상위 directory 에서 이름이 사라질 수 있었다.
    """
    import tools.preserve as P

    seen: list[str] = []
    real = P._fsync_dir
    monkeypatch.setattr(P, "_fsync_dir", lambda d: (seen.append(str(d)), real(d))[1])

    backend = CasBackend(root=tmp_path / "cas")
    dg = backend.put_if_absent(b"first-object-in-this-store")["digest"]
    backend.pin("legX", [dg])

    root = str(tmp_path / "cas")
    assert f"{root}/objects" in seen, "objects/ entry 를 굳히지 않았다"
    assert f"{root}/objects/{dg[:2]}" in seen
    assert f"{root}/pins" in seen, "pins/ entry 를 굳히지 않았다"
    assert f"{root}/pins/legX" in seen


#: crash/reopen drill 의 자식 프로세스. 등록 직전에 **프로세스를 죽인다**
#: (`os._exit` — atexit·버퍼 flush 없음. 예외 주입과 달리 finally 도 안 돈다).
_CRASH_CHILD = r'''
import os, sys, json, hashlib
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from tools.preserve import CasBackend, Hooks, PlannedLeg, run_transaction
import tools.preserve as P

where_ = sys.argv[2]
stage = sys.argv[3]
run = Path(where_) / "run"
(run / "_inputs").mkdir(parents=True)
(run / "fits.parquet").write_bytes(b"PAR1" + b"\x11" * 512 + b"PAR1")
(run / "manifest.yaml").write_text("leg: crashleg\n", encoding="utf-8")
(run / "_inputs" / "base.yaml").write_text("noise: 0.001\n", encoding="utf-8")

data = (run / "fits.parquet").read_bytes()
planned = PlannedLeg(leg_id="crashleg", protocol_generation="v6",
                     pairing_design_sha256=hashlib.sha256(b"d").hexdigest(),
                     source_digest="deadbeefcafe0001",
                     objectives=("pocv_dvdq",), total_start_budget=20,
                     candidate_mode="legacy_slot_replace")
(run / "run_spec.json").write_text(json.dumps(
    {"planned_id": planned.planned_id(), "source_digest": planned.source_digest}),
    encoding="utf-8")

def validate(root):
    need = ["fits.parquet", "manifest.yaml", "_inputs/base.yaml"]
    miss = [n for n in need if not (Path(root) / n).is_file()]
    return {"ok": not miss, "fail": miss, "checks": {n: True for n in need}}

def rescore(root):
    d = (Path(root) / "fits.parquet").read_bytes()
    o = Path(root) / "_rescored.json"
    o.write_bytes(json.dumps({"n": len(d)}, sort_keys=True,
                             separators=(",", ":")).encode())
    return {"role": "rescored_summary", "canonicalizer": "score-semantic/v1",
            "semantic_schema": "degeneracy-summary/v6",
            "semantic_sha256": hashlib.sha256(d).hexdigest(),
            "relative_path": "_rescored.json", "byte_size": o.stat().st_size,
            "file_sha256": hashlib.sha256(o.read_bytes()).hexdigest(),
            "producer": "crash-child/v1", "produced_from": "fits.parquet",
            "source_file_sha256": hashlib.sha256(d).hexdigest(), "n_rows": 1,
            "semantic_view_drops": ["x"]}

backend = CasBackend(root=Path(where_) / "cas")
index = Path(where_) / "index"

# 지정한 지점에서 **프로세스를 죽인다**
if stage == "after_pin":
    real_retain = CasBackend.retain
    def killer(self, leg_id, digests, *, min_retention_days):
        lease = real_retain(self, leg_id, digests,
                            min_retention_days=min_retention_days)
        os._exit(9)                       # lease 는 만들었고 journal 은 없다
    CasBackend.retain = killer
elif stage == "after_publish":
    real_publish = P.publish
    def killer2(index_path, entry):
        out = real_publish(index_path, entry)
        os._exit(9)                       # index 는 있고 pin·journal 이 없다
        return out
    P.publish = killer2
elif stage == "after_register":
    # ★ 31차 P0-3 — journal 이 **보이는** 상태에서 죽는다. 30차 drill 의 두
    #   지점은 둘 다 `_register()` 앞이라 `journal visible` 양성 branch 가
    #   한 번도 실행되지 않았다.
    real_register = P._register
    def killer3(*a, **kw):
        real_register(*a, **kw)
        os._exit(9)                       # journal 은 있고 post-commit 검증 전
    P._register = killer3
elif stage == "during_journal_fsync":
    # journal link 는 됐는데 그 directory 를 굳히기 **직전**에 죽는다
    real_strict = P._fsync_dir_strict
    def killer4(d, stage_name):
        if d.name == "registered":
            os._exit(9)
        return real_strict(d, stage_name)
    P._fsync_dir_strict = killer4

run_transaction(planned, run, backend, index,
                Hooks(validate=validate, rescore=rescore,
                      min_retention_days=365,
                      expected_semantic=hashlib.sha256(data).hexdigest()))
'''


#: crash drill 이 각 지점에서 journal 양성 상태를 만들었는가 (★ 31차 P0-3)
_CRASH_POSITIVE: dict[str, bool] = {}


@pytest.mark.parametrize("stage", ["after_pin", "after_publish",
                                   "after_register", "during_journal_fsync"])
def test_a_killed_process_never_leaves_a_journal_without_its_graph(tmp_path, stage):
    """★ 30차 P0-3 — 요청문이 "drill 이 없다" 고 신고했던 자리다.

    예외 주입은 `finally` 를 돌지만 **kill 은 아무 것도 돌지 않는다.** 자식
    프로세스를 `os._exit(9)` 로 죽이고 부모가 다시 열어 확인하는 것이
    리뷰가 요구한 `journal visible ⇒ full graph retrievable` 이다.
    """
    import subprocess
    import sys as _sys

    where = tmp_path / "w"
    where.mkdir()
    repo = str(Path(__file__).resolve().parents[1])
    script = where / "child.py"
    script.write_text(_CRASH_CHILD, encoding="utf-8")
    p = subprocess.run([_sys.executable, str(script), repo, str(where), stage],
                       capture_output=True, text=True)
    assert p.returncode == 9, (p.returncode, p.stdout[-2000:], p.stderr[-2000:])

    # ── 재개방 — 죽은 자리에서 무엇이 남았는가 ────────────────────────────
    backend = CasBackend(root=where / "cas")
    index = where / "index"

    # 불변식: journal 이 보이면 graph 전체가 회수 가능하다
    positive = has_registration_journal(index, "crashleg")
    if positive:
        assert is_registered(index, "crashleg", backend), (
            "journal 은 남았는데 graph 를 회수할 수 없다")
    else:
        assert not is_registered(index, "crashleg", backend)

    # ★ 31차 P0-3 — 양성 상태를 **실제로 만든 적이 있는지** 기록한다.
    #   30차 drill 은 두 지점 모두 `_register()` 앞이라 위 양성 branch 가 한
    #   번도 실행되지 않았다. 아래 집계 시험이 그것을 강제한다.
    _CRASH_POSITIVE[stage] = positive

    # 그리고 재개는 **재계산 없이** 끝나야 한다 (hooks 를 받지 않는다)
    if index_entries(index):
        import tools.preserve as P

        seen: list[str] = []
        real = P._fsync_dir
        P._fsync_dir = lambda d: (seen.append(d.name), real(d))[1]
        try:
            out = finalize_only("crashleg", backend, index)
        finally:
            P._fsync_dir = real
        assert out["ok"] and is_registered(index, "crashleg", backend)
        if positive:
            # ★ 32차 P0-3 — journal 이 **보이지만 durable 하지 않을 수 있는**
            #   상태에서 재개했다. `already` 로 빠져나가면 interrupted commit
            #   을 완료하지 않은 것이다. 복구가 journal directory 를 다시
            #   굳혔는지 직접 본다.
            assert "registered" in seen, (
                "journal 이 보이는 상태로 재개했는데 registered/ 를 다시 "
                "굳히지 않았다 — interrupted commit 이 완료되지 않았다")


def test_re_running_a_registered_leg_does_not_mint_a_second_lease(tmp_path,
                                                                 monkeypatch):
    """★ 30차 자체 발견 — lease 에 시각이 들어가 재실행이 pin 을 늘렸다.

    `retain()` 이 부를 때마다 `retain_until_utc` 를 새로 찍으므로, 두 번째
    실행이 **초 경계를 넘으면** 다른 바이트의 lease 가 하나 더 CAS 에 들어가고
    pin 집합에 여분이 생겨 `verify_retention` 이 실패했다. 전체 시험을 열두 번
    돌려 두 번 빨갛던 자리이고, 원인이 시계라 재현이 확률적이었다.

    시계를 강제로 전진시켜 **결정적으로** 고정한다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 25, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 10000, 37))            # 부를 때마다 초가 흐른다

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)

    a = run_transaction(PLANNED, run, backend, index, _hooks())
    b = run_transaction(PLANNED, run, backend, index, _hooks())
    assert a["retention"]["lease_digest"] == b["retention"]["lease_digest"], (
        "재실행이 lease 를 새로 만들었다")
    assert is_registered(index, PLANNED.leg_id, backend)

    leases = [d for d in backend.pinned(PLANNED.leg_id)
              if d not in set(a["retention"]["objects"])]
    assert leases == [a["retention"]["lease_digest"]], (
        f"pin 에 lease 가 {len(leases)}개다 — 여분이 생겼다")


# ─────────────────────────────────────────────────────────────────────────────
# 31차 P0-1 — enforcement 는 **backend capability** 이지 caller label 이 아니다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_local_backend_cannot_be_labelled_object_lock(tmp_path):
    """★ 31차 P0-1 — 리뷰가 준 정적 반례를 그대로 돌린다.

        b = CasBackend(root=cas, enforcement="object_lock")   # 구현은 local pin
        r = run_transaction(..., backend=b, ...)
        assert r["durable"] is True                            # 통과했다
        assert_durable_retention(b, index, leg)                # 통과했다
        b._pin(leg, receipt_digest).unlink()                   # local 에서 가능

    30차에 만든 "durable 의 뜻을 좁혔다" 는 경계가 **문자열 하나로 무너졌다.**
    `enforcement` 는 생성자로 바꿀 수 있는 dataclass field 였다.
    """
    with pytest.raises(TypeError):
        CasBackend(root=tmp_path / "cas", enforcement=ENFORCEMENT_OBJECT_LOCK)

    b = CasBackend(root=tmp_path / "cas")
    with pytest.raises(PreserveError) as ei:
        b.enforcement = ENFORCEMENT_OBJECT_LOCK      # 사후 대입도 막는다
    assert "capability" in ei.value.msg


def test_verify_retention_compares_the_lease_label_to_live_capability(tmp_path):
    """★ 31차 P0-1 — lease 에 적힌 문자열을 **지금 backend** 와 대조한다.

    초판은 lease 의 `enforcement` 를 저장만 하고 다시 보지 않았다. 그래서
    lease 를 위조하거나, 강한 backend 에서 만든 lease 를 약한 backend 에서
    열어도 아무 일이 없었다.
    """
    backend = CasBackend(root=tmp_path / "cas")
    dg = backend.put_if_absent(b"x")["digest"]
    lease = backend.retain("legX", [dg], min_retention_days=MIN_RETENTION_DAYS)
    assert backend.verify_retention("legX", lease["lease_digest"])

    # lease 만 `object_lock` 으로 바꿔 CAS 에 넣고 pin 한다 — 위조 시나리오
    forged = dict({k: v for k, v in lease.items() if k != "lease_digest"},
                  enforcement=ENFORCEMENT_OBJECT_LOCK)
    f_obj = backend.put_if_absent(canonical_bytes(forged))["digest"]
    backend.pin("legX", [f_obj])
    with pytest.raises(PreserveError) as ei:
        backend.verify_retention("legX", f_obj)
    assert "enforcement" in ei.value.msg


def test_durable_retention_needs_a_live_capability_probe(tmp_path):
    """★ 31차 P0-1 — `assert_durable_retention` 이 저장된 문자열만 믿었다.

    강제를 **지금 조회해** 확인해야 한다. local backend 는 그 조회를
    통과할 수 없다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    assert res["durable"] is False
    assert res["retention"]["enforcement"] == ENFORCEMENT_ADVISORY

    with pytest.raises(PreserveError) as ei:
        assert_durable_retention(backend, index, PLANNED.leg_id)
    assert "advisory" in ei.value.msg


def test_finalize_only_returns_the_same_typed_retention_result(tmp_path):
    """★ 31차 P0-1 — `finalize_only()` 는 `ok=True` 만 돌려줬다.

    "`ok=True` 의 뜻을 좁혔다" 가 **모든 public 성공 경로**에 적용되지
    않았다는 뜻이다. 신규 등록 경로와 `already` 경로 둘 다 본다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    with pytest.raises(PreserveError):
        run_transaction(PLANNED, run, backend, index, _hooks(),
                        faults=frozenset({"crash_after_publish"}))
    shutil.rmtree(run)

    fresh = finalize_only(PLANNED.leg_id, backend, index)
    assert fresh["already"] is False
    assert fresh["durable"] is False
    assert fresh["retention"]["enforcement"] == ENFORCEMENT_ADVISORY

    again = finalize_only(PLANNED.leg_id, backend, index)
    assert again["already"] is True
    assert again["durable"] is False
    assert again["retention"]["lease_digest"] == fresh["retention"]["lease_digest"]


def test_an_object_lock_backend_can_claim_durable_retention(tmp_path):
    """강제가 **있으면** durable 이 성립한다 — 경계가 한쪽으로만 닫히면 안 된다."""
    run = _make_run(tmp_path)
    backend = _lockstore(tmp_path)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())

    assert res["durable"] is True
    assert res["retention"]["enforcement"] == ENFORCEMENT_OBJECT_LOCK
    assert res["retention"]["lock_mode"] == "COMPLIANCE"
    versions = res["retention"]["object_versions"]
    assert set(versions) == set(res["retention"]["objects"])
    assert all(_nonempty(v) for v in versions.values())
    assert assert_durable_retention(backend, index, PLANNED.leg_id)


def test_a_provider_that_stops_enforcing_loses_durable_retention(tmp_path):
    """★ 31차 P0-1 — 강제는 **지금** 조회해야 한다.

    등록 시점에 강제됐다는 사실이 지금도 강제된다는 뜻이 아니다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    assert run_transaction(PLANNED, run, backend, index, _hooks())["durable"]

    store.min_retain_days = 1                     # 정책이 내려갔다
    with pytest.raises(PreserveError):
        assert_durable_retention(backend, index, PLANNED.leg_id)
    assert not is_registered(index, PLANNED.leg_id, backend)


def test_an_object_lock_backend_without_a_provider_is_advisory(tmp_path):
    """★ 31차 P0-1 — 클래스 이름만으로는 강제가 아니다."""
    backend = LockedCasBackend(root=tmp_path / "cas")     # provider 없음
    assert backend.enforcement == ENFORCEMENT_OBJECT_LOCK
    assert backend.probe_enforcement() == ENFORCEMENT_ADVISORY


# ─────────────────────────────────────────────────────────────────────────────
# 31차 P0-3 — durability edge 가 CAS 쪽에만 닫혔다
# ─────────────────────────────────────────────────────────────────────────────

def test_index_and_journal_levels_flush_their_parent_entry(tmp_path, monkeypatch):
    """★ 31차 P0-3 — `_exclusive_write()` 는 `mkdir(parents=True)` 뒤 **자기
    부모만** flush 했다.

    새 `index/legs`·`index/registered` 를 담는 `index/` edge 와, 새 `index/`
    를 담는 그 부모 edge 는 굳히지 않았다. 30차의 "모든 새 directory parent
    edge" 주장이 이 경로에는 적용되지 않았다 — 30차 회귀가 CAS 네 경로만
    셌기 때문에 잡히지 않았다.
    """
    import tools.preserve as P

    seen: list[str] = []
    real = P._fsync_dir
    monkeypatch.setattr(P, "_fsync_dir", lambda d: (seen.append(str(d)), real(d))[1])

    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())

    for want in (str(index), f"{index}/legs", f"{index}/registered"):
        assert want in seen, f"{want} entry 를 굳히지 않았다"


def test_a_backend_without_directory_fsync_cannot_publish_a_graph(tmp_path,
                                                                  monkeypatch):
    """★ 31차 P0-3 — `_fsync_dir_strict()` 가 capability false 면 **return** 했다.

    "publish 가 이미 막는다" 는 주석은 CAS 와 index 가 **같은 filesystem**
    일 때만 성립한다. CAS 에서 directory fsync 가 안 되고 index 에서는 되는
    구성이면 graph 이름은 비내구적으로 진행하고 journal 만 durable 하게
    commit 된다. 두 계층의 capability 를 따로 주입해 그 상황을 만든다.
    """
    import tools.preserve as P

    monkeypatch.setattr(P, "_DIR_FSYNC", {})
    cas_root = (tmp_path / "cas").resolve()

    real = P.dir_fsync_supported

    def split(where):
        # CAS 아래만 capability 없음 — index 는 정상
        return False if str(Path(where).resolve()).startswith(str(cas_root)) \
            else real(where)

    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    backend.store_id                     # store 를 **먼저** 만든다 (전제)
    monkeypatch.setattr(P, "dir_fsync_supported", split)

    # CAS 쓰기가 그 자리에서 멈춰야 한다. `store.json` 은 이미 있으므로
    # `_exclusive_write` 의 capability 검사에 업히지 않는다 — 이 시험이
    # 실제로 보는 것은 `_fsync_dir_strict()` 하나다.
    with pytest.raises(PreserveError) as ei:
        backend.put_if_absent(b"graph-object-that-needs-a-new-prefix")
    assert ei.value.stage == "cas_put", ei.value.stage

    with pytest.raises(PreserveError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    assert index_entries(index) == {}, "graph 가 비내구적인데 index 가 생겼다"


def test_a_retry_after_a_failed_directory_fsync_must_fsync_again(tmp_path,
                                                                 monkeypatch):
    """★ 31차 P0-3 — 실패 전파가 **재시도까지** fail-closed 가 아니었다.

    `_exclusive_write()` 는 final link 뒤 directory fsync 가 실패하면 예외를
    던지지만 final pathname 은 **이미 존재한다**. 재시도는
    `EEXIST → created=False` 가 되어 fsync 를 건너뛰고, 상위
    `publish()`/`_register()` 는 "같은 바이트" 라는 이유로 성공했다.
    """
    import tools.preserve as P

    index = tmp_path / "index"
    entry = {"leg_id": "legX", "planned_id": "p", "receipt_digest": "r",
             "receipt_object": "o", "payload_root_digest": "d",
             "payload_manifest_digest": "m", "backend_uri": "file+cas:///x"}

    calls = {"n": 0, "legs": 0}
    real = P._fsync_dir

    def flaky(d):
        calls["n"] += 1
        if d.name == "legs":
            calls["legs"] += 1
            if calls["legs"] == 1:
                return False        # 첫 시도의 최종 fsync 만 실패시킨다
        return real(d)

    monkeypatch.setattr(P, "_fsync_dir", flaky)

    with pytest.raises(PreserveError):
        publish(index, entry)
    assert (index / "legs" / "legX.json").is_file(), "이름은 이미 생겼다 — 전제"

    # 재시도는 durable 해질 때까지 성공이라고 말하면 안 된다
    before = calls["legs"]
    publish(index, entry)
    assert calls["legs"] > before, "재시도가 directory fsync 를 건너뛰었다"


def test_the_crash_drill_actually_reaches_a_visible_journal():
    """★ 31차 P0-3 — drill 이 **양성 상태를 만든 적이 있어야** 한다.

    30차 drill 은 `after_pin`·`after_publish` 둘뿐이었고 둘 다 `_register()`
    앞이라, `journal visible ⇒ full graph retrievable` 의 전건이 한 번도
    참이 되지 않았다. 시험 이름은 그 불변식을 말하는데 실제로는 공허하게
    참이었던 것이다 — 35.7 이 적은 형태의 또 다른 얼굴이다.
    """
    assert set(_CRASH_POSITIVE) == {"after_pin", "after_publish",
                                    "after_register", "during_journal_fsync"}, (
        f"drill 이 다 돌지 않았다: {sorted(_CRASH_POSITIVE)}")
    # ★ 32차 P0-3 — `any`/`not all` 은 너무 약하다. `during_journal_fsync` 가
    #   다시 음성이 되어도 `after_register` 하나만 양성이면 통과했다.
    #   요청문에 적은 **exact vector** 를 고정한다.
    assert _CRASH_POSITIVE == {"after_pin": False, "after_publish": False,
                               "after_register": True,
                               "during_journal_fsync": True}, _CRASH_POSITIVE


# ─────────────────────────────────────────────────────────────────────────────
# 31차 P1 — validator check 값 · output variant · candidate mode
# ─────────────────────────────────────────────────────────────────────────────

def test_a_false_subcheck_cannot_hide_inside_a_successful_receipt(tmp_path):
    """★ 31차 P1-1 — `checks` 의 **값**을 아무도 안 봤다.

        {"ok": True, "fail": [], "checks": {"payload": False}}

    가 통과하고, receipt 는 이것을 `{"ok": true, "n_checks": 1}` 로 축약해
    false subcheck 를 **지웠다**. 30차 7-case 회귀는 `checks` 자체의 타입과
    공백만 바꿨지 check 값을 변이하지 않았다.
    """
    assert check_hook_validation(
        {"ok": True, "fail": [], "checks": {"a": True, "b": True}}) == []
    bad = check_hook_validation(
        {"ok": True, "fail": [], "checks": {"a": True, "payload": False}})
    assert any("payload" in x for x in bad), bad

    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    h = _hooks()
    h.validate = lambda root: {"ok": True, "fail": [],
                               "checks": {"payload": False}}
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, h)
    assert ei.value.stage == "validate"
    assert index_entries(index) == {}


def test_the_receipt_seals_the_check_names_not_just_a_count(tmp_path):
    """★ 31차 P1-1 — `n_checks` 숫자 하나로 축약하면 무엇을 봤는지 사라진다.

    검사 **이름 집합**을 receipt 에 봉인해, 검사를 바꿔치기해도 숫자가 같으면
    통과하던 자리를 막는다.
    """
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    v = res["receipt"]["validation"]
    assert v["ok"] is True
    assert v["checks"] == ["_inputs/base.yaml", "fits.parquet", "manifest.yaml"], v
    assert v["n_checks"] == len(v["checks"])


def test_output_variants_reject_fields_from_another_variant():
    """★ 31차 P1-2 — role 별 **exact key set** 이 아니라 subset 검사였다.

    `rescored_rows` 에 summary 전용 `semantic_view_drops` 를 넣어도 통과했다.
    30차 회귀는 정상 summary 의 **기존 필드 값**만 바꿔서 cross-variant
    surplus 를 넣어 보지 않았다.
    """
    rows = {"role": "rescored_rows", "canonicalizer": "score-semantic/v1",
            "semantic_schema": "rows/v1", "semantic_sha256": "a" * 64,
            "relative_path": "out.tsv", "byte_size": 12,
            "file_sha256": "b" * 64, "producer": "p/v1",
            "object_digest": "b" * 64, "measured_by": "tools.preserve",
            "produced_from": "fits.parquet", "source_file_sha256": "c" * 64,
            "n_rows": 3}
    assert check_output(rows) == []
    # 다른 variant 의 필드가 남으면 거부 (subset 검사로도 잡히는 축)
    bad = check_output(dict(rows, semantic_view_drops=["_채점원본"]))
    assert any("semantic_view_drops" in x for x in bad), bad
    # **모자라도** 거부 — 이쪽이 exact set 이 아니면 못 잡는 축이다.
    for k in sorted(rows):
        missing = {x: v for x, v in rows.items() if x != k}
        assert check_output(missing), f"{k} 를 빼도 통과했다"
    # summary 는 자기 필드를 요구한다
    summary = dict(rows, role="rescored_summary")
    assert check_output(summary), "summary 인데 semantic_view_drops 가 없다"
    assert check_output(dict(summary, semantic_view_drops=["_채점원본"])) == []


@pytest.mark.parametrize("path", ["a\\b", "C:x", "a//b", "./x", " x", "x "])
def test_output_paths_use_the_same_validator_as_manifest_members(path):
    """★ 31차 P1-2 — 생성·복구의 path domain 이 **달랐다**.

    `_safe_member_path()` 는 backslash·colon·빈/`.` segment 를 거부하는데
    `check_output()` 은 leading slash 와 `..` 만 봤다. 저장된 receipt 를
    검증하는 쪽이, 만드는 쪽이라면 거부했을 경로를 받아들였다.
    """
    good = {"role": "rescored_rows", "canonicalizer": "score-semantic/v1",
            "semantic_schema": "rows/v1", "semantic_sha256": "a" * 64,
            "relative_path": "out.tsv", "byte_size": 12,
            "file_sha256": "b" * 64, "producer": "p/v1",
            "object_digest": "b" * 64, "measured_by": "tools.preserve",
            "produced_from": "fits.parquet", "source_file_sha256": "c" * 64,
            "n_rows": 3}
    assert check_output(good) == []
    bad = check_output(dict(good, relative_path=path))
    assert any("relative_path" in x or "경로" in x for x in bad), (path, bad)


def test_candidate_mode_enum_comes_from_the_contract_not_a_second_list():
    """★ 31차 P1-3 — validator 의 enum 이 **계약과 달랐다**.

    validator: `legacy_slot_replace · warm_slot_replace · random_only ·
    base_init_only`
    계약 §3:  `legacy_slot_replace · equal_start_count_base_retained · union`

    계약상 유효한 두 mode 를 거부하고 계약에 없는 세 mode 를 허용했다.
    30차 회귀는 `whatever` 하나만 넣어 봤으므로 이 불일치를 못 잡았다.
    값을 두 곳에 두지 않는다 — 계약에서 파싱한다.
    """
    from tools.preserve import candidate_modes

    modes = candidate_modes()
    assert modes == {"legacy_slot_replace", "equal_start_count_base_retained",
                     "union"}, modes
    good = PLANNED.envelope()
    for m in sorted(modes):
        assert check_envelope(dict(good, candidate_mode=m)) == [], m
    for m in ("warm_slot_replace", "random_only", "base_init_only", "whatever"):
        assert check_envelope(dict(good, candidate_mode=m)), m


def test_a_backend_object_keeps_pointing_at_the_store_it_was_made_for(tmp_path,
                                                                     monkeypatch):
    """★ 31차 P0-2 hardening — `root` 가 생성 시 고정되지 않았다.

    `uri` property 가 호출 때마다 cwd 기준으로 다시 계산해, **같은 backend
    객체**가 cwd 변경만으로 다른 store 를 가리켰다. 30차의 상대경로 반례는
    두 객체를 만들었으므로 이 축을 보지 못했다.
    """
    a, b = tmp_path / "a", tmp_path / "b"
    (a / "cas").mkdir(parents=True)
    (b / "cas").mkdir(parents=True)

    monkeypatch.chdir(a)
    backend = CasBackend(root=Path("cas"))
    before = backend.uri
    sid = backend.store_id

    monkeypatch.chdir(b)
    assert backend.uri == before, "cwd 를 바꿨더니 같은 객체가 다른 store 를 가리킨다"
    assert backend.store_id == sid
    assert backend.uri.startswith("file+cas:///"), backend.uri


# ─────────────────────────────────────────────────────────────────────────────
# 32차 P0-1 — provider 가 **바이트를 소유하고 삭제를 거부**해야 한다
# ─────────────────────────────────────────────────────────────────────────────

class _LockingStore:
    """실제로 강제하는 in-process object store.

    ★ 32차 P0-1 — 31차의 `_FakeLockProvider` 는 **바이트를 보관하지 않고**
      version/until dict 만 만들었다. 그래서 `durable=True` 뒤에도 local pin 을
      지울 수 있었고 provider 장부는 그대로였다. 리뷰의 문장 그대로다 —
      "강제가 있는 쪽이 아니라 local bytes 와 독립된 metadata 장부가 있는 쪽".

      이 store 는 바이트를 **자기가 들고**, lock 이 걸린 동안 delete/overwrite
      를 실제로 **거부**한다. 실제 provider(S3 Object Lock)의 성질을 그대로
      흉내낸 것이고, adapter 를 붙일 때 이 계약을 만족하면 된다.
    """

    MODE = "COMPLIANCE"
    #: 이름 → 백킹 상태. 같은 이름의 새 instance 는 **같은 store 를 다시 연
    #: 것**이다 (새 process 흉내). 실제 provider 의 bucket 에 해당한다.
    _BACKING: dict = {}

    #: GOVERNANCE 우회 삭제를 허용하는가. 실제 S3 에서는 principal 이
    #: `s3:BypassGovernanceRetention` 을 들고 있는지에 해당한다.
    BYPASS = False

    def __init__(self, min_retain_days=MIN_RETENTION_DAYS, mode=None,
                 name="canary-store", bypass=None):
        st = _LockingStore._BACKING.setdefault(
            name, {"obj": {}, "head": {}, "lock": {}, "n": [0], "ver": {},
                   "marker": set(), "vmode": {}})
        self._obj: dict[tuple[str, str], bytes] = st["obj"]
        self._head: dict[str, str] = st["head"]
        self._lock: dict[tuple[str, str], str] = st["lock"]
        self._ver: dict[str, list] = st["ver"]
        self._marker: set = st["marker"]
        self._mode: dict = st["vmode"]
        self._counter = st["n"]
        self.name = name
        self.min_retain_days = min_retain_days
        self.mode = mode or self.MODE
        self.bypass = self.BYPASS if bypass is None else bypass

    def store_uri(self) -> str:
        """★ 33차 P0-1 — provider 가 주는 **안정 식별자**. 재시작을 견딘다."""
        return f"canary://{self.name}"

    # ── 실제 provider 가 제공하는 연산 ──────────────────────────────────
    def put(self, key: str, data: bytes) -> str:
        """★ 36차 P0-1 — **언제나 새 version 을 만든다.**

        35차까지 이 fake 는 head 가 잠겨 있으면 `put` 을 거부했다. 실제
        Object Lock 은 그러지 않는다 — retention 은 **그 version** 을 지키는
        것이지 key 를 지키는 것이 아니다. 그래서 실물에서는 잠긴 v1 위에
        잠기지 않은 v2 가 얼마든지 올라가고, `head_version` 을 보는 코드는
        전부 그 v2 를 본다. fake 가 그 창을 가리고 있었다.

        ★ 37차 P0-1 — **같은 바이트 shortcut 을 없앴다.** 36차판은 head 가
        잠겼고 bytes 가 같으면 기존 version ID 를 재사용했다. 실물
        `PutObject` 는 요청마다 version ID 를 부여한다. 그 shortcut 때문에
        `repair_lease_locks()` 반복이 fake 에서만 멱등해 보였고, 실물에서는
        재시도마다 새 version 이 생겨 WORM-lock 될 수 있다.
        """
        self._counter[0] += 1
        vid = f"v{self._counter[0]:05d}"
        self._obj[(key, vid)] = bytes(data)
        self._head[key] = vid
        self._ver.setdefault(key, []).insert(0, vid)
        return vid

    def get(self, key: str, version: str | None = None) -> bytes:
        v = version or self._head.get(key)
        # delete marker 가 head 면 실물처럼 "없다" 로 답한다 (version 은 살아 있다)
        if v is None or (key, v) in self._marker or (key, v) not in self._obj:
            raise KeyError(key)
        return self._obj[(key, v)]

    def versions(self, key: str) -> list:
        """최신순 version 목록. per-version 잠금의 locator (marker 는 뺀다)."""
        return [v for v in self._ver.get(key, []) if (key, v) in self._obj]

    def delete(self, key: str, version: str | None = None,
               bypass: bool = False) -> None:
        """★ 37차 P0-1 — version 없는 delete 는 **delete marker** 다.

        36차판은 version 없는 delete 가 locked head 를 직접 지운다고 봤다.
        실물 versioned S3 에서 version 없는 DELETE 는 delete marker 를 얹고
        보호된 version 은 **남긴다**. 그래서 36차 canary 의 "`delete(key)` 가
        거부된다" 는 기대 자체가 실물 의미와 달랐다 — 실물에서는 거부되지
        않고 **성공하며**, 대신 담보 version 이 살아남는다.
        """
        if version is None:
            self._counter[0] += 1
            mk = f"d{self._counter[0]:05d}"       # delete marker 도 version 이다
            self._marker.add((key, mk))
            self._head[key] = mk
            self._ver.setdefault(key, []).insert(0, mk)
            return
        v = version
        if (key, v) in self._lock:
            # ★ 39차 P0-1 — **봉인된 per-version mode** 와 **그 version 의 기한**
            #   으로 판단한다. 38차판은 mutable 한 현재 `self.mode` 를 봐서,
            #   COMPLIANCE 로 잠근 version 도 전역 mode 를 GOVERNANCE 로 바꾼 뒤
            #   bypass 삭제할 수 있었다. 반대로 만료된 잠금도 영구 잠금처럼
            #   취급했다.
            mode = self._mode.get((key, v), self.mode)
            now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            expired = str(self._lock[(key, v)]) <= now
            if not expired:
                if not (bypass and mode == "GOVERNANCE" and self.bypass):
                    raise PermissionError(f"object lock 이 삭제를 막았다: {key}@{v}")
            self._lock.pop((key, v), None)
        self._obj.pop((key, v), None)
        self._marker.discard((key, v))
        if self._head.get(key) == v:
            live = [x for x in self._ver.get(key, [])
                    if (key, x) in self._obj or (key, x) in self._marker]
            if live:
                self._head[key] = live[0]
            else:
                self._head.pop(key, None)

    def lock(self, key: str, version: str, until: str) -> None:
        """★ 38차 P0-1 — 잠금은 **version 별**이고 Compliance 는 단조롭다.

        37차판은 `until` 을 단순 대입하고 mode 를 아예 저장하지 않았다. 그래서
        (a) Compliance retention 을 **짧게** 덮을 수 있었고 (b) 전역
        `self.mode` 를 바꾸면 과거 모든 version 의 mode 가 소급 변경됐다.
        실물 Compliance 는 둘 다 거부한다.
        """
        # ★ 40차 P0-1 — canary 도 계약을 지킨다. 잘못된 timestamp 를 받아
        #   두면 그 위의 모든 horizon proof 가 그만큼 약해진다.
        if not isinstance(until, str):
            raise TypeError(f"retain_until 이 문자열이 아니다: {until!r}")
        dt.datetime.strptime(until, "%Y-%m-%dT%H:%M:%SZ")   # 아니면 ValueError
        cur = self._lock.get((key, version))
        if cur is not None:
            mode = self._mode.get((key, version), self.mode)
            if mode == "COMPLIANCE" and until < cur:
                raise PermissionError(
                    f"COMPLIANCE 는 retain-until 을 줄일 수 없다: {key}@{version} "
                    f"{cur} → {until}")
        self._lock[(key, version)] = until
        # mode 는 **잠글 때** 봉인된다 — 나중에 store mode 를 바꿔도 안 변한다
        self._mode.setdefault((key, version), self.mode)

    def describe(self) -> dict:
        return {"mode": self.mode, "min_retain_days": self.min_retain_days}

    def describe_object(self, key: str, version: str) -> dict | None:
        if (key, version) not in self._obj:
            return None
        u = self._lock.get((key, version))
        if u is None:
            return None
        # ★ 38차 P0-1 — 그 version 이 **잠길 때** 봉인된 mode 를 돌려준다.
        return {"version_id": version,
                "mode": self._mode.get((key, version), self.mode),
                "retain_until": u}

    def head_version(self, key: str):
        """★ 34차 P0-1 — digest 로 현재 version 을 재조회하는 계약."""
        return self._head.get(key)

    def list_versions(self, prefix: str) -> list:
        """★ 37차 P0-1 — `ListObjectVersions` 다: delete marker 도 넘는다.

        `keys_under()`(= ListObjectsV2)만으로 pin 을 열거하면 marker 하나로
        graph 가 "없는" 것이 된다. 담보 version 은 살아 있으므로 열거도
        version 층에서 해야 한다.
        """
        return sorted((k, v) for (k, v) in self._obj if k.startswith(prefix))

    def keys_under(self, prefix: str) -> list[str]:
        """★ 37차 P0-1 — head 가 delete marker 면 열거되지 않는다.

        실물 `ListObjectsV2` 의 의미다. 보호된 version 은 남아 있지만 목록
        에서는 사라지므로, pin 열거를 이것에만 의존하면 delete marker 하나로
        graph 가 "없는" 것이 된다.
        """
        return sorted(k for k in self._head
                      if k.startswith(prefix)
                      and (k, self._head[k]) not in self._marker)


def _lockstore(tmp_path, store=None, retention_days=3650):
    b = LockedCasBackend(root=tmp_path / "cas", retention_days=retention_days)
    object.__setattr__(b, "provider",
                       store or _LockingStore(name=str(tmp_path)))
    return b


def test_a_locked_graph_survives_wiping_the_local_root(tmp_path):
    """★ 32차 P0-1 — provider 가 **바이트를 소유**한다.

    리뷰가 요구한 canary 다: local CAS/pins 를 통째로 없앤 뒤에도 provider
    에서 receipt·manifest·member·산출 graph 전부를 회수할 수 있어야 한다.
    31차 canary 는 local 이 바이트를 들고 있었으므로 이것을 못 보였다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    assert res["durable"] is True

    # local 을 통째로 지운다 — provider 가 진짜 소유자라면 아무 일도 없다
    shutil.rmtree(backend.root, ignore_errors=True)
    assert is_registered(index, PLANNED.leg_id, backend), (
        "local root 를 지웠더니 등록이 죽었다 — 바이트를 provider 가 들고 있지 않다")
    assert assert_durable_retention(backend, index, PLANNED.leg_id)


def test_the_provider_actually_refuses_to_delete_a_locked_object(tmp_path):
    """★ 32차 P0-1 — 잠금이 **삭제를 실제로 막아야** 한다.

    31차 canary 는 삭제를 시도조차 하지 않았다. "반환 직후 삭제 자체가
    성공한 순간 durable retention 의 약속이 깨진다" 는 지적 그대로다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())

    leg, lease = PLANNED.leg_id, res["retention"]
    for dg in res["retention"]["objects"]:
        key = backend._provider_key(leg, dg)
        # ★ 37차 P0-1 — version 없는 DELETE 는 실물에서 **거부되지 않는다.**
        #   delete marker 를 얹을 뿐이고 담보 version 은 남는다. 거부되어야
        #   하는 것은 **그 version 을 겨눈** 삭제다.
        pv = backend.protected_version(key)
        assert pv, f"담보 version 이 없다: {key}"
        with pytest.raises(PermissionError):
            store.delete(key, pv)
        # ★ 36차 P0-1 — 실물 Object Lock 은 **새 version 을 막지 않는다.**
        #   적대적 put 은 성공하고 잠기지 않은 head 가 잠긴 version 을 가린다.
        #   깨지면 안 되는 것은 "put 이 실패한다" 가 아니라 **담보한 바이트를
        #   그래도 회수할 수 있다** 이다.
        store.put(key, b"overwritten")
        assert store.get(key) == b"overwritten", "전제: head 가 오염됐다"
        assert hashlib.sha256(
            backend.retrieve_retained(lease, dg)).hexdigest() == dg, (
            f"적대적 head 가 담보 바이트를 가렸다: {dg[:16]}")
    assert is_registered(index, leg, backend)
    assert assert_durable_retention(backend, index, leg)


@pytest.mark.parametrize("axis", ["empty_version", "foreign_version",
                                  "mode_changed", "until_shortened",
                                  "lock_released"])
def test_each_lock_axis_independently_loses_durable_retention(tmp_path, axis):
    """★ 32차 P0-1 — verifier 의 세 구멍을 축마다 따로 물린다.

    리뷰가 적은 그대로:
      1. `object_versions` 값이 nonempty provider version 인지 안 봤다
      2. lease 의 `lock_mode` 를 **현재** provider mode 와 비교하지 않았다
      3. version 별 현재 `retain_until` 을 재조회하지 않았다
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg = PLANNED.leg_id
    victim = sorted(res["retention"]["objects"])[0]
    key = backend._provider_key(leg, victim)
    vid = res["retention"]["object_versions"][victim]

    if axis == "empty_version":
        # lease 가 version 을 **안 적은** 경우 — provider 에 묻기 전에 걸린다
        res["retention"]["object_versions"][victim] = ""
        with pytest.raises(PreserveError) as ei:
            backend.verify_retention(leg, res["retention"]["lease_digest"],
                                     lease=res["retention"])
        assert "비었다" in ei.value.msg, ei.value.msg
        return
    if axis == "foreign_version":
        # 값은 있는데 provider 에 그런 version 이 **없는** 경우 — 조회가 잡는다
        res["retention"]["object_versions"][victim] = "v99999"
        with pytest.raises(PreserveError) as ei:
            backend.verify_retention(leg, res["retention"]["lease_digest"],
                                     lease=res["retention"])
        assert "잠긴 version 이 없다" in ei.value.msg, ei.value.msg
        return
    if axis == "mode_changed":
        store.mode = "GOVERNANCE"
    elif axis == "until_shortened":
        store._lock[(key, vid)] = "2026-08-28T00:00:00Z"
    elif axis == "lock_released":
        store._lock.pop((key, vid))

    with pytest.raises(PreserveError):
        assert_durable_retention(backend, index, leg)
    assert not is_registered(index, leg, backend)


# ─────────────────────────────────────────────────────────────────────────────
# 32차 P0-3 — retry 재-fsync 가 index 한 경로에만 들어갔다
# ─────────────────────────────────────────────────────────────────────────────

def _flaky_fsync(monkeypatch, victim_name):
    """`victim_name` directory 의 **첫** fsync 만 실패시킨다."""
    import tools.preserve as P

    n = {"hit": 0, "total": 0}
    real = P._fsync_dir

    def flaky(d):
        n["total"] += 1
        if d.name == victim_name:
            n["hit"] += 1
            if n["hit"] == 1:
                return False
        return real(d)

    monkeypatch.setattr(P, "_fsync_dir", flaky)
    return n


def test_a_cas_object_retry_must_fsync_the_prefix_again(tmp_path, monkeypatch):
    """★ 32차 P0-3 — `put_if_absent()` 의 기존-name branch 가 fsync 를 건너뛴다.

    `os.replace` 성공 뒤 `objects/<prefix>` fsync 가 실패하면 final object
    name 은 남은 채 예외가 나간다. 재시도는 `dst.exists()` 로 들어가 bytes 만
    확인하고 즉시 return 했다 — 다시 굳히지 않았다. 31차에 이 형태를
    `_exclusive_write()` **한 경로에서만** 고쳤다.
    """
    backend = CasBackend(root=tmp_path / "cas")
    backend.store_id                                   # store 를 먼저 만든다
    data = b"object-that-needs-a-new-prefix-directory"
    n = _flaky_fsync(monkeypatch, hashlib.sha256(data).hexdigest()[:2])

    with pytest.raises(PreserveError):
        backend.put_if_absent(data)
    assert backend.has(hashlib.sha256(data).hexdigest()), "이름은 이미 생겼다 — 전제"

    before = n["hit"]
    backend.put_if_absent(data)                        # 재시도
    assert n["hit"] > before, "재시도가 object prefix 를 다시 굳히지 않았다"


def test_a_pin_retry_must_fsync_the_pin_directory_again(tmp_path, monkeypatch):
    """★ 32차 P0-3 — `pin()` 의 기존-pin branch 도 같은 형태였다."""
    backend = CasBackend(root=tmp_path / "cas")
    backend.store_id
    dg = backend.put_if_absent(b"pin-me")["digest"]
    n = _flaky_fsync(monkeypatch, "legX")

    with pytest.raises(PreserveError):
        backend.pin("legX", [dg])
    assert backend.pinned("legX") == {dg}, "pin 이름은 이미 생겼다 — 전제"

    before = n["hit"]
    backend.pin("legX", [dg])                          # 재시도
    assert n["hit"] > before, "재시도가 pin directory 를 다시 굳히지 않았다"


def test_a_directory_that_exists_is_still_re_fsynced_on_retry(tmp_path,
                                                              monkeypatch):
    """★ 32차 P0-3 — `_mkdir_durable()` 이 "보이면 즉시 return" 했다.

    `mkdir` 은 성공했지만 parent fsync 가 실패한 상태와 이미 durable 한
    상태를 **구별하지 못한다**. 재시도가 parent edge 를 다시 굳히지 않았다.
    """
    import tools.preserve as P

    seen: list[str] = []
    real = P._fsync_dir
    monkeypatch.setattr(P, "_fsync_dir",
                        lambda d: (seen.append(d.name), real(d))[1])

    d = tmp_path / "a" / "b"
    P._mkdir_durable(d, "t")
    first = list(seen)
    assert first, "처음에는 굳혔다 — 전제"

    seen.clear()
    P._mkdir_durable(d, "t")            # 이미 있다
    assert seen, "이미 있는 directory 라고 parent edge 를 건너뛰었다"


def test_a_fresh_store_root_flushes_its_own_parent_entry(tmp_path, monkeypatch):
    """★ 32차 P0-3 — `store_id` 가 CAS root **이름**을 안 굳혔다.

    `backend.store_id` 는 `root.mkdir(parents=True)` 만 하고 `root.parent` 를
    fsync 하지 않았다. 그 뒤 `_mkdir_durable(staging/objects/pins)` 도 root 가
    이미 보인다는 이유로 그 edge 를 건너뛰었다. CAS 와 index 가 다른
    filesystem 이면 power loss 뒤 CAS root 전체가 사라지고 journal 만 남는
    ordering 이 가능하다.
    """
    import tools.preserve as P

    seen: list[str] = []
    real = P._fsync_dir
    monkeypatch.setattr(P, "_fsync_dir",
                        lambda d: (seen.append(str(d)), real(d))[1])

    root = tmp_path / "deep" / "cas"
    CasBackend(root=root).store_id
    assert str(root.parent) in seen, "CAS root 이름을 담은 entry 를 안 굳혔다"
    assert str(tmp_path) in seen, "그 위 층도 굳혀야 한다"


# ─────────────────────────────────────────────────────────────────────────────
# 33차 P0-1 — durable graph 의 **증거**인 lease 가 잠금 밖이었다
# ─────────────────────────────────────────────────────────────────────────────

def test_the_lease_object_is_locked_too(tmp_path):
    """★ 33차 P0-1 — `retain()` 의 순서가 lease 를 잠금 밖에 뒀다.

        graph objects pin → lock_objects(graph) → lease 생성 → lease put/pin

    정확한 lease digest 와 version 은 `lock_objects()` **뒤에야** 존재하므로
    `retention.objects` 만 보호받고 lease 는 지울 수 있었다. verifier 는
    lease 를 retention graph 의 일부로 취급하는데, graph 가 durable 하다는
    **증거만 mutable** 인 모순이다. 32차 canary 도 `objects` 만 공격했다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg, lease = PLANNED.leg_id, res["retention"]["lease_digest"]

    # lease 의 pin 도 content object 도 잠겨 있어야 한다
    for key in (backend._provider_key(leg, lease),
                backend._provider_obj_key(lease)):
        pv = backend.protected_version(key)
        assert pv, f"담보 version 이 없다: {key}"
        with pytest.raises(PermissionError):
            store.delete(key, pv)                 # 그 version 은 못 지운다
        store.delete(key)                         # marker 는 얹힌다 (실물 의미)
        # ★ 36차 P0-1 — 적대적 새 version 은 실물에서 성공한다. 잠긴 version
        #   이 남아 있어야 하고 lease 는 그것으로 읽혀야 한다.
        store.put(key, b"overwritten")
        assert backend.protected_version(key) == pv, (
            f"marker·덮어쓰기가 담보 version 을 바꿨다: {key}")
    assert assert_durable_retention(backend, index, leg), (
        "적대적 head 가 lease 증명을 가렸다")

    # journal 이 lease version proof 를 들고 있어야 한다 — lease 는 자기
    # digest 를 담을 수 없으므로 그 증거는 밖에 있어야 한다
    j = registration(index, leg)
    assert _is_hex64_str(j["lease_digest"])
    assert _nonempty(j["lease_version"])
    assert assert_durable_retention(backend, index, leg)


def test_a_forged_lease_version_proof_is_refused(tmp_path):
    """journal 의 lease version proof 도 provider 와 대조한다."""
    run = _make_run(tmp_path)
    backend = _lockstore(tmp_path)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg = PLANNED.leg_id

    j = registration(index, leg)
    path = index / "registered" / f"{leg}.json"
    path.unlink()
    path.write_bytes(canonical_bytes(dict(j, lease_version="v99999")))
    assert not is_registered(index, leg, backend)


def test_a_reopened_backend_finds_the_same_registration(tmp_path):
    """★ 33차 P0-1 — `uri` 기본값이 `id(provider)` 였다.

    process-local 객체 주소라 재시작 뒤 값이 달라지고 재사용될 수도 있다.
    receipt·lease 가 backend URI 를 봉인해 대조하므로 이 기본 계약으로는
    reopen/recovery locator 가 될 수 없다. provider 가 **안정 식별자**를 준다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())

    # 새 process 를 흉내낸다 — 같은 store 이름, **다른 provider·backend 객체**
    fresh = _LockingStore(name=store.name)
    assert fresh is not store and id(fresh) != id(store)
    reopened = _lockstore(tmp_path, fresh)
    assert reopened.uri == backend.uri, "재시작 뒤 URI 가 달라졌다"
    assert reopened.store_id == backend.store_id
    assert is_registered(index, PLANNED.leg_id, reopened)
    assert assert_durable_retention(reopened, index, PLANNED.leg_id)


def test_a_provider_without_a_stable_identity_cannot_be_used(tmp_path):
    """안정 식별자를 못 주는 provider 는 durable 을 주장할 수 없다."""

    class _Anon(_LockingStore):
        def store_uri(self):
            return None

    backend = _lockstore(tmp_path, _Anon(name=str(tmp_path)))
    with pytest.raises(PreserveError) as ei:
        backend.uri
    assert "식별자" in ei.value.msg


# ─────────────────────────────────────────────────────────────────────────────
# 34차 P0-1 — lease version proof 가 journal 전에는 회수 불가였다
# ─────────────────────────────────────────────────────────────────────────────

def test_rerunning_an_object_lock_transaction_reuses_the_same_lease(tmp_path,
                                                                    monkeypatch):
    """★ 34차 P0-1 반례 A — 완료 뒤 같은 트랜잭션 재실행.

    `_existing_lease()` 는 기존 lease 를 읽고 `verify_retention()` 을 부르는데
    `lease_version` 을 넘기지 않는다. object-lock verifier 는 proof 가 없으면
    **반드시 실패**하고, `_existing_lease()` 는 그 예외를 "기존 lease 없음"
    으로 바꿔 `None` 을 돌려준다.

    → 초 경계를 넘으면 두 번째 WORM lease 가 생기고 exact pin set 이 오염돼
      **기존 정상 등록까지 거짓이 된다** (WORM 이라 지울 수도 없다).
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)

    a = run_transaction(PLANNED, run, backend, index, _hooks())
    assert a["durable"] is True
    b = run_transaction(PLANNED, run, backend, index, _hooks())

    assert b["retention"]["lease_digest"] == a["retention"]["lease_digest"], (
        "재실행이 두 번째 WORM lease 를 만들었다")
    leases = backend.pinned(PLANNED.leg_id) - set(a["retention"]["objects"])
    assert leases == {a["retention"]["lease_digest"]}, f"lease 가 {len(leases)}개다"
    assert is_registered(index, PLANNED.leg_id, backend)
    assert assert_durable_retention(backend, index, PLANNED.leg_id)


def test_a_crash_between_lease_lock_and_journal_can_be_finalized(tmp_path):
    """★ 34차 P0-1 반례 B — lease 를 잠근 직후 journal 전에 죽는다.

    L0/V0 는 provider 에 잠겼는데 V0 를 기록한 journal 이 없다. 재개가 L0 를
    재사용하지 못하면 L1 을 만들고, exact pin-set 검증이 L0 를 여분으로 보아
    journal 조차 못 만든다. L0 는 WORM 이라 약속 기간 전 삭제도 안 된다 —
    "재계산 없이 CAS 로 닫는다" 가 가장 필요한 상태가 장기 복구 불가가 된다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    # ★ 시계를 전진시킨다. 같은 초 안에서는 lease 바이트가 같아 우연히
    #   재사용되므로, 그러면 이 시험이 아무 것도 시험하지 않는다.
    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    _real_dt = P.dt.datetime
    P.dt.datetime = _Clock

    # retain() 직후 죽는다 (journal 전)
    real = P.verify_graph_before_registration

    def die(*a, **kw):
        raise RuntimeError("lease lock 뒤 journal 전에 죽었다 (주입)")

    P.verify_graph_before_registration = die
    try:
        with pytest.raises(RuntimeError):
            run_transaction(PLANNED, run, backend, index, _hooks())
    finally:
        P.verify_graph_before_registration = real

    assert not has_registration_journal(index, PLANNED.leg_id)
    leased = backend.pinned(PLANNED.leg_id)
    assert leased, "lease/graph 가 잠겼어야 한다 — 전제"

    # 새 process 를 흉내낸다 — 새 provider·backend 객체로 재개
    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(PLANNED.leg_id, fresh, index)
    assert out["ok"] and out["durable"] is True
    assert is_registered(index, PLANNED.leg_id, fresh)

    after = fresh.pinned(PLANNED.leg_id)
    leases = after - set(out["retention"]["objects"])
    P.dt.datetime = _real_dt
    assert leases == {out["retention"]["lease_digest"]}, (
        f"재개가 lease 를 하나 더 만들었다: {sorted(leases)}")


def test_the_provider_control_plane_is_locked_too(tmp_path):
    """★ 34차 P0-1 — `store.json` 이 잠기지 않은 control-plane object 였다.

    지우면 새 UUID 가 발급돼, content 와 lease 가 모두 남아 있어도 기존
    receipt 가 복구 불가가 된다. false durable 은 아니지만 "12시간 계산을
    재실행하지 않는다" 는 목적에 직접 영향을 준다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())

    sid = backend.store_id
    pv = backend.protected_version("store.json")
    assert pv, "store.json 담보 version 이 없다"
    with pytest.raises(PermissionError):
        store.delete("store.json", pv)
    store.delete("store.json")                    # marker 는 얹힌다
    # ★ 36차 P0-1 — 적대적 put 은 실물에서 성공한다 (per-version 잠금).
    #   identity 는 **잠긴 version** 에서 읽혀야 하고, head 오염이 새 UUID
    #   발급으로 이어지면 안 된다 — 그 순간 기존 receipt 의 locator 를 잃는다.
    store.put("store.json", b"{}")
    assert _lockstore(tmp_path, _LockingStore(name=store.name)).store_id == sid, (
        "적대적 head 가 store identity 를 갈아치웠다")


# ─────────────────────────────────────────────────────────────────────────────
# 35차 P0-1 — `retain()` 내부 네 단계를 원자 단계처럼 다뤘다
# ─────────────────────────────────────────────────────────────────────────────

def _phase_kill(monkeypatch, phase: str):
    """`retain()` 의 네 durable 단계 **사이**에서 죽인다.

    ★ 35차 P0-1 — 34차 drill 은 `retain()` 이 **전부 반환된 뒤**에서만 죽였다.
      실제 순서는 네 단계다:

          lease CAS content put → lease pin → lease pin lock → lease content lock

      앞 경계는 두 번째 WORM lease 를 만들고, 뒤 경계는 lease content 가
      삭제 가능한데도 재개가 `durable=True` 까지 간다.

    호출 순서로 지점을 고른다 — lease digest 는 store 마다 다르므로
    (lease 가 `store_id`·`backend_uri` 를 담는다) 미리 알 수 없다.

        pin 1회차 = graph · 2회차 = lease
        lock_objects 1회차 = graph · 2회차 = lease
        lock_content_object 1회차 = lease
    """
    import tools.preserve as P

    boom = RuntimeError(f"{phase} 직후에 죽었다 (주입)")
    n = {"pin": 0, "lock": 0, "content": 0}
    cls = P.ObjectLockBackend

    real_pin, real_lock = cls.pin, cls.lock_objects
    real_content = cls.lock_content_object

    def pin(self, leg_id, digests):
        n["pin"] += 1
        if phase == "after_lease_put" and n["pin"] == 2:
            raise boom                      # lease content 는 있고 pin 은 없다
        return real_pin(self, leg_id, digests)

    def lock(self, leg_id, digests, until):
        n["lock"] += 1
        if phase == "after_lease_pin" and n["lock"] == 2:
            raise boom                      # lease pin 은 있고 잠금은 없다
        return real_lock(self, leg_id, digests, until)

    def content(self, dg, until, **kw):
        n["content"] += 1
        if phase == "after_pin_lock" and n["content"] == 1:
            raise boom                      # pin 은 잠겼고 content 는 안 잠겼다
        return real_content(self, dg, until, **kw)

    monkeypatch.setattr(cls, "pin", pin)
    monkeypatch.setattr(cls, "lock_objects", lock)
    monkeypatch.setattr(cls, "lock_content_object", content)


@pytest.mark.parametrize("phase", ["after_lease_put", "after_lease_pin",
                                   "after_pin_lock"])
def test_a_crash_inside_retain_leaves_exactly_one_repairable_lease(tmp_path,
                                                                   monkeypatch,
                                                                   phase):
    """★ 35차 P0-1 — 네 단계 **사이**에서 죽어도 lease 는 하나이고 복구된다.

    허용되는 결과는 둘 중 하나다:
      · 기존 lease 의 누락 잠금을 **repair** 하고 같은 digest 로 완료
      · 명시적 fail-closed — 단, **두 번째 WORM lease 를 만들지 않는다**

    성공 판정에는 lease **pin** 과 lease **CAS content** 의 live proof 가
    모두 포함돼야 한다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    # 시계를 전진시킨다 — 같은 초 안에서는 우연히 같은 lease digest 가 된다
    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, phase)
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())

    # 주입을 걷고 새 process 를 흉내낸다 (시계는 계속 전진)
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)
    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(PLANNED.leg_id, fresh, index)
    assert out["ok"] and out["durable"] is True

    lease = out["retention"]
    extra = fresh.pinned(PLANNED.leg_id) - set(lease["objects"])
    assert extra == {lease["lease_digest"]}, (
        f"{phase}: lease 가 {len(extra)}개다 — 두 번째 WORM lease 가 생겼다")

    # 두 잠금이 **모두** 살아 있어야 한다
    leg, ld = PLANNED.leg_id, lease["lease_digest"]
    for key in (fresh._provider_key(leg, ld), fresh._provider_obj_key(ld)):
        pv = fresh.protected_version(key)
        assert pv, f"{phase}: 담보 version 이 없다 — {key}"
        with pytest.raises(PermissionError):
            store.delete(key, pv)


def test_an_unlocked_store_record_is_repaired_or_refused(tmp_path):
    """★ 35차 P0-1 — `put` 뒤 `lock` 전 crash 가 남긴 record 를 그냥 믿었다.

    `store_id` 는 valid UUID record 가 보이면 **즉시 반환**하고, 다시 잠그지도
    현재 lock 을 조회하지도 않았다. 그 상태에서 정상 트랜잭션이 `durable=True`
    를 돌려주고, 이후 `store.json` 삭제가 성공해 다음 reopen 이 새 UUID 를
    발급하면 기존 receipt 의 locator 를 잃는다.
    """
    store = _LockingStore(name=str(tmp_path))
    # put 은 됐고 lock 은 안 된 상태를 그대로 만든다 (crash 잔여)
    store.put("store.json", canonical_bytes(
        {"schema": "cas-store/v1", "store_id": "0" * 32}))
    assert ("store.json", store._head["store.json"]) not in store._lock, "전제"

    backend = _lockstore(tmp_path, store)
    sid = backend.store_id                      # reopen — repair 하거나 거부
    assert sid == "0" * 32, "기존 identity 를 버리면 안 된다"
    pv = backend.protected_version("store.json")
    assert pv, "수리가 잠그지 않았다"
    with pytest.raises(PermissionError):
        store.delete("store.json", pv)


def test_the_store_lock_horizon_covers_every_lease(tmp_path, monkeypatch):
    """★ 35차 P0-1 — store 잠금 기한이 graph 와 결속되지 않았다.

    store 는 생성 시 고정 기한으로 한 번 잠기고 후속 lease 기한과 대조·연장
    하지 않았다. 오래된 store 에 새 lease 를 만들면 담보 기간 대부분에
    control-plane identity 가 삭제 가능해진다.
    """
    import tools.preserve as P

    store = _LockingStore(name=str(tmp_path))
    # ★ 아래에서 기본 지평보다 긴 lease 를 요구하므로 backend 담보 상한도
    #   그만큼 열어 둔다 (retain 은 retention_days 를 넘는 요구를 거절한다).
    long_days = MIN_RETENTION_DAYS * 20
    backend = _lockstore(tmp_path, store, retention_days=long_days * 2)

    base = dt.datetime(2026, 8, 27, tzinfo=dt.timezone.utc)
    now = {"t": base}

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return now["t"]

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    backend.store_id                                     # T0 에 store 생성
    first = store._lock[("store.json", store._head["store.json"])]

    # ★ store 의 기본 지평(생성 시각 + 10×정책)보다 **긴** lease 를 만든다.
    #   짧은 lease 는 기본 지평에 이미 덮이므로 이 축을 시험하지 못한다
    #   (변이로 확인했다 — retain 쪽 연장을 지워도 초록이었다).
    dg = backend.put_if_absent(b"late-graph")["digest"]
    lease = backend.retain("legLate", [dg], min_retention_days=long_days)

    after = store._lock[("store.json", store._head["store.json"])]
    assert after >= lease["retain_until_utc"], (
        f"store 잠금({after})이 lease 기한({lease['retain_until_utc']})보다 짧다 — "
        "담보 기간 안에 identity 가 삭제 가능하다")
    assert after > first, "기한이 연장되지 않았다"


# ─────────────────────────────────────────────────────────────────────────────
# 36차 P0-1 — adapter 계약이 **한 authority** 가 아니었다
# ─────────────────────────────────────────────────────────────────────────────

def _provider_ops_called() -> set:
    """`tools/preserve.py` 가 provider 에게 실제로 거는 연산 이름을 뽑는다.

    문서가 아니라 **소스**에서 뽑는다 — 계약과 호출이 갈라지는 것을 사람이
    지키게 두지 않는다.
    """
    import ast
    src = (ROOT / "tools" / "preserve.py").read_text(encoding="utf-8")
    ops: set[str] = set()

    def _is_provider(node) -> bool:
        return (isinstance(node, ast.Attribute) and node.attr == "provider"
                and isinstance(node.value, ast.Name) and node.value.id == "self")

    for n in ast.walk(ast.parse(src)):
        # self.provider.<op>
        if isinstance(n, ast.Attribute) and _is_provider(n.value):
            ops.add(n.attr)
        # getattr(self.provider, "<op>", ...)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                and n.func.id == "getattr" and n.args and _is_provider(n.args[0]) \
                and len(n.args) >= 2 and isinstance(n.args[1], ast.Constant) \
                and isinstance(n.args[1].value, str):
            ops.add(n.args[1].value)
    return ops


def test_the_provider_contract_is_the_only_authority(tmp_path):
    """★ 36차 P0-1 — 계약 docstring 이 코드가 부르는 연산보다 적었다.

    docstring 은 7개(put/get/delete/lock/describe/describe_object/keys_under)
    를 열거했는데 코드는 `store_uri`·`head_version` 도 불렀다. 그 문서만 보고
    adapter 를 쓰면 실물에서 `PreserveError("capability")` 로 죽는다. 계약을
    **기계가 읽는 상수 하나**로 만들고, 소스가 부르는 이름과 대조한다.
    """
    from tools.preserve import PROVIDER_CONTRACT, ObjectLockBackend

    called = _provider_ops_called()
    named = set(PROVIDER_CONTRACT)
    assert called <= named, (
        f"계약에 없는 연산을 부른다: {sorted(called - named)} — "
        "adapter 작성자는 이 호출을 알 수 없다")
    assert named <= called, (
        f"계약이 안 쓰는 연산을 요구한다: {sorted(named - called)}")

    doc = ObjectLockBackend.__doc__ or ""
    missing = [op for op in named if op not in doc]
    assert not missing, f"계약 docstring 에 없는 연산: {missing}"


def test_a_provider_missing_a_contract_op_cannot_claim_durable(tmp_path):
    """계약의 **어느 한 연산**이라도 없으면 durable 을 주장할 수 없다."""
    from tools.preserve import PROVIDER_CONTRACT

    for op in sorted(PROVIDER_CONTRACT):
        store = _LockingStore(name=f"{tmp_path}-{op}")
        setattr(store, op, None)                       # 그 연산만 없앤다
        backend = _lockstore(tmp_path / op, store)
        # ★ 실제 durable 판정 경로로 간다 — helper 를 직접 부르면 그것이
        #   배선돼 있는지 시험하지 못한다 (33차의 교훈).
        assert backend.probe_enforcement() == "advisory_local", (
            f"{op} 가 없는데 담보라고 답했다")
        with pytest.raises(PreserveError) as ex:
            backend.assert_provider_contract()
        assert op in str(ex.value), f"{op} 가 빠졌는데 이름이 안 나온다"


# ─────────────────────────────────────────────────────────────────────────────
# 36차 P0-1 — GOVERNANCE 는 신고이지 강제가 아니다
# ─────────────────────────────────────────────────────────────────────────────

def test_governance_is_never_durable_however_the_probe_answers(tmp_path):
    """★ 37차 P0-1 — GOVERNANCE 는 **어떤 probe 결과로도** 담보가 아니다.

    36차는 우회 삭제를 실측해 거부되면 GOVERNANCE 를 `object_lock` 으로
    승격했다. 리뷰의 반례: 한 principal 이 retention 을 **단축·제거**할
    권한은 가지되 version delete 권한은 없는 구성이 가능하다. 그러면 delete
    probe 는 거부돼 양성이 되는데 같은 principal 이 담보를 지울 수 있다.
    다른 principal 과 이후 IAM 변경은 애초에 현재 credential 의 한 요청으로
    관측되지 않는다.

    31차에 local mode bit 를 uid 0 이 우회할 수 있다는 이유로 durable 에서
    뺐다. 현재 credential 의 delete 한 번이 거부됐다는 GOVERNANCE 증거를
    그보다 강하게 취급할 근거가 없다 — **같은 잣대를 쓴다.**
    """
    for bypass in (True, False):
        store = _LockingStore(name=f"{tmp_path}-{bypass}", mode="GOVERNANCE",
                              bypass=bypass)
        backend = _lockstore(tmp_path / str(bypass), store)
        assert backend.probe_enforcement() == "advisory_local", (
            f"bypass={bypass}: GOVERNANCE 를 담보로 받았다 — 이 주장은 저장소가 "
            "아니라 IAM 설정에 대한 것이다")


def test_compliance_is_still_durable(tmp_path):
    """반대 축 — GOVERNANCE 를 뺀 것이 mode 전체를 뺀 것이 되면 안 된다."""
    store = _LockingStore(name=str(tmp_path), mode="COMPLIANCE")
    backend = _lockstore(tmp_path, store)
    assert backend.probe_enforcement() == "object_lock"



# ─────────────────────────────────────────────────────────────────────────────
# 37차 P0-1 — fake 가 실물 versioning 을 거꾸로 모형하고 있었다
# ─────────────────────────────────────────────────────────────────────────────

def _version_census(store, prefix="") -> dict:
    """key 별 version 수. **key 수가 아니라 이것을 센다** (37차 P0-1)."""
    out: dict[str, int] = {}
    for k, _v in store.list_versions(prefix):
        out[k] = out.get(k, 0) + 1
    return out


def test_repeated_repair_never_inflates_locked_versions(tmp_path):
    """★ 37차 P0-1 — 재시도가 provider version 을 늘리면 안 된다.

    36차 fake 는 `put` 이 같은 바이트면 기존 version ID 를 재사용해서
    `repair_lease_locks()` 반복이 멱등해 **보였다**. 실물 `PutObject` 는
    요청마다 version 을 부여하므로, 무조건 put 하는 구현은 재시도마다 같은
    바이트의 WORM version 을 쌓는다. 지울 수 없는 쓰레기가 무한히 는다.

    "lease 가 하나다" 는 key 만 세므로 이 축을 못 본다 — **version 을 센다.**
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    assert res["durable"] is True

    before = _version_census(store)
    leg, ld = PLANNED.leg_id, res["retention"]["lease_digest"]
    until = res["retention"]["retain_until_utc"]
    for _ in range(4):
        backend.repair_lease_locks(leg, ld, until)
        backend.ensure_store_lock(until)
    after = _version_census(store)

    grew = {k: (before.get(k, 0), n) for k, n in after.items()
            if n > before.get(k, 0)}
    assert not grew, f"재시도가 version 을 늘렸다: {grew}"


def test_a_delete_marker_cannot_hide_the_retained_graph(tmp_path):
    """★ 37차 P0-1 — version 없는 DELETE 는 marker 이고, 열거를 가린다.

    실물 `ListObjectsV2` 는 head 가 delete marker 인 key 를 안 보여준다.
    pin 열거가 그것에만 의존하면 marker 하나로 graph 가 "없는" 것이 된다 —
    담보 version 은 멀쩡히 살아 있는데도. 열거는 version 층에서 해야 한다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg = PLANNED.leg_id
    full = backend.pinned(leg)
    assert full, "전제: pin 이 있다"

    for dg in sorted(full):
        store.delete(backend._provider_key(leg, dg))     # marker 를 얹는다
    assert store.keys_under(f"pins/{leg}/") == [], "전제: 목록에서 사라졌다"

    assert backend.pinned(leg) == full, (
        "delete marker 가 pin 열거를 가렸다 — 담보 version 은 살아 있다")
    assert assert_durable_retention(backend, index, leg), (
        "marker 뒤에서 담보 증명이 무너졌다")
    for dg in sorted(res["retention"]["objects"]):
        assert hashlib.sha256(
            backend.retrieve_retained(res["retention"], dg)).hexdigest() == dg


def _crashed_lease_digest(store, backend, leg: str) -> str | None:
    """crash 직후 상태에서 lease digest 를 찾는다 (journal 이 아직 없다).

    pin 에 있으면 그 바이트가 lease schema 인지로 고르고, 아직 pin 이 없으면
    (`after_lease_put`) `objects/` 에만 있고 pin 에는 없는 것이 lease 다.
    """
    pins = backend.pinned(leg)
    for dg in sorted(pins):
        try:
            rec = load_canonical(backend.read_pinned(leg, dg))
        except (PreserveError, ValueError, UnicodeDecodeError):
            continue
        if isinstance(rec, dict) and rec.get("schema") == P_RETENTION_SCHEMA:
            return dg
    only = {k.split("/", 1)[1] for k, _v in store.list_versions("objects/")} - pins
    return sorted(only)[0] if len(only) == 1 else None


@pytest.mark.parametrize("phase", ["after_lease_put", "after_lease_pin",
                                   "after_pin_lock"])
def test_a_deletion_inside_the_unlocked_window_never_mints_a_second_lease(
        tmp_path, monkeypatch, phase):
    """★ 37차 P0-1 — 36차 drill 은 **삭제를 복구가 끝난 뒤에** 했다.

    `after_lease_put`·`after_lease_pin`·`after_pin_lock` 시점에는 lease CAS
    content 가 아직 잠기지 않았다. 리뷰가 준 반례 그대로다:

        T0  lease L0 content 를 put 하고 pin 을 만든다
        T1  그 사이에서 죽는다
        T2  **아직 unlocked 인 objects/<L0> 를 지운다**
        T3  fresh backend 로 재개한다

    재개는 pin 에서 L0 를 발견하지만, `repair_lease_locks()` 가 살아남은 pin
    바이트를 읽지 않고 `pin()` 부터 부른다. `pin()` 은 `read_back(L0)` 로
    **지워진 content** 를 읽다가 실패하고, `_existing_lease()` 는 그 실패를
    "기존 lease 없음" 과 구별하지 않고 `None` 으로 바꾼다. 두 번째 WORM
    lease 가 생기고 옛 pin 은 남는다 — `after_pin_lock` 의 옛 pin 은 이미
    WORM 이라 정상 API 로 치울 수도 없다.

    허용되는 결과는 둘뿐이다:
      · 살아남은 pin 바이트로 content 를 되살리고 **같은 lease** 로 완료
      · 명시적 fail-closed — 단, **새 lease 를 만들지 않는다**
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, phase)
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)

    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, f"{phase}: lease 후보를 못 찾았다 (전제)"

    # ── T2: 아직 잠기지 않은 lease content 를 **실제로** 지운다 ──────────
    key = backend._provider_obj_key(ld)
    live = store.versions(key)
    assert live, f"{phase}: lease content 가 없다 (전제)"
    for v in live:
        assert (key, v) not in store._lock, (
            f"{phase}: 이 창에서는 lease content 가 잠겨 있으면 안 된다 (전제)")
        store.delete(key, v)
    assert not store.versions(key), f"{phase}: 삭제가 실패했다 (전제)"

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    before = _version_census(store, "pins/")
    try:
        out = finalize_only(leg, fresh, index)
    except PreserveError:
        out = None                            # fail-closed 도 허용되는 결과다
    if phase != "after_lease_put":
        # ★ pin 이 살아남았으면 바이트가 남아 있다는 뜻이다. 그러면
        #   fail-closed 는 **불필요한 손실**이다 — 살아남은 pin 으로 content 를
        #   되살려 같은 lease 로 끝내야 한다. (이 줄이 없으면 "복원 안 하고
        #   그냥 거부" 변이가 초록이다 — 실측했다.)
        assert out is not None, (
            f"{phase}: pin 이 살아 있는데 복구하지 못하고 거부했다")

    leases = {dg for dg in fresh.pinned(leg)
              if _looks_like_lease(fresh, leg, dg)}
    assert len(leases) <= 1, (
        f"{phase}: lease pin 이 {len(leases)}개다 — 두 번째 WORM lease 가 "
        f"생겼다: {sorted(leases)}")

    if out is not None:
        assert out["ok"] and out["durable"] is True
        assert leases == {out["retention"]["lease_digest"]}
        if phase != "after_lease_put":
            # pin 이 살아남은 창에서는 **그 pin 바이트로** 같은 lease 를
            # 되살려야 한다. `after_lease_put` 은 pin 자체가 없으므로
            # (content 도 지웠다) 새 lease 가 유일한 정답이고, 그때는 지울 수
            # 없는 WORM 잔여가 남지 않는다는 것이 불변식이다.
            assert out["retention"]["lease_digest"] == ld, (
                f"{phase}: 살아남은 pin 으로 같은 lease 를 복구하지 않았다")
        got = out["retention"]["lease_digest"]
        for k in (fresh._provider_key(leg, got), fresh._provider_obj_key(got)):
            assert fresh.protected_version(k), f"{phase}: 잠기지 않았다 — {k}"
    else:
        after = _version_census(store, "pins/")
        grew = {k: (before.get(k, 0), n) for k, n in after.items()
                if n > before.get(k, 0)}
        assert not grew, f"{phase}: 실패했는데 pin version 이 늘었다: {grew}"


def _looks_like_lease(backend, leg: str, dg: str) -> bool:
    try:
        rec = load_canonical(backend.read_pinned(leg, dg))
    except (PreserveError, ValueError, UnicodeDecodeError):
        return False
    return isinstance(rec, dict) and rec.get("schema") == P_RETENTION_SCHEMA


def test_an_unpinned_lease_residue_is_adopted_not_multiplied(tmp_path,
                                                             monkeypatch):
    """★ 37차 P0-1 — `after_lease_put` 잔여를 discovery 가 못 봤다.

    그 창에서는 lease content 가 put 됐고 pin 은 아직 없다. 재개는 pin 만
    보므로 잔여를 못 보고 새 lease 를 만든다. lease 바이트는 `retain_until_utc`
    때문에 초마다 달라져 CAS dedup 도 안 걸리므로, 그 창을 지날 때마다
    orphan content 와 provider version 이 **하나씩 쌓인다**.

    35·36차 시험은 pin 된 extra 만 세어 이 누적을 통째로 놓쳤다 — key 가 아니라
    **version 을 센다**.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, "after_lease_put")
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)

    leg = PLANNED.leg_id
    orphan = _crashed_lease_digest(store, backend, leg)
    assert orphan, "전제: pin 없는 lease content 잔여가 있다"
    assert orphan not in backend.pinned(leg), "전제: 아직 pin 이 아니다"

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    assert out["ok"] and out["durable"] is True
    assert out["retention"]["lease_digest"] == orphan, (
        "잔여를 입양하지 않고 새 lease 를 만들었다 — 재시도마다 지워지지 않는 "
        "content 가 쌓인다")

    census = _version_census(store, "objects/")
    leases = [k for k in census
              if k.split("/", 1)[1] not in set(out["retention"]["objects"])]
    assert len(leases) == 1, f"lease content 가 {len(leases)}개다: {leases}"
    assert census[leases[0]] == 1, (
        f"같은 lease 의 version 이 {census[leases[0]]}개다 — 재시도가 늘렸다")


def _crash_at_lease_pin(tmp_path, monkeypatch):
    """`after_lease_pin` 상태를 만들고 (store, backend, index) 를 돌려준다."""
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, "after_lease_pin")
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)
    return store, backend, index
def test_a_repair_failure_is_not_the_same_as_no_candidate(tmp_path, monkeypatch):
    """★ 37차 P0-1 — 수리 실패를 `None` 으로 접으면 새 WORM lease 가 생긴다.

    36차판은 `repair_lease_locks()` 의 예외를 삼켜 "기존 lease 없음" 과 같이
    취급했다. 후보가 눈앞에 있는데 손댈 수 없는 상태라면, 그 위에 되돌릴 수
    없는 것을 하나 더 얹는 것이 조용한 기본값이면 안 된다.

    `after_lease_pin` 창에서는 lease pin 이 **아직 안 잠겼다.** 그 pin 바이트가
    오염되면 수리는 digest 대조에서 실패한다 — 실제로 일어날 수 있는 상태다.
    """
    store, backend, index = _crash_at_lease_pin(tmp_path, monkeypatch)
    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: lease 후보가 있다"
    key = backend._provider_key(leg, ld)
    assert backend.protected_version(key) is None, "전제: pin 이 안 잠겼다"

    # ★ 40차 P1 — 원본 version 을 **지우고** 오염된 것만 남긴다. `put` 은
    #   언제나 새 version 을 만들므로, 그냥 덮기만 하면 원본이 살아남아
    #   수리가 성공한다 (그것이 옳은 동작이다 — 실측했다). 여기서 보려는 것은
    #   "정말로 복구 불가일 때 fail-closed 인가" 이다.
    for v in list(store.versions(key)):
        store.delete(key, v)
    store.put(key, b"corrupted-pin-bytes")

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    with pytest.raises(PreserveError):
        finalize_only(leg, fresh, index)

    leases = {dg for dg in fresh.pinned(leg) if _looks_like_lease(fresh, leg, dg)}
    assert not leases - {ld}, f"수리 실패 뒤 lease 가 늘었다: {sorted(leases)}"


def test_a_live_lease_that_fails_verification_is_refused_not_replaced(
        tmp_path, monkeypatch):
    """★ 37차 P0-1 — 만료와 불일치를 같은 `None` 으로 접었다.

    만료된 lease 를 새로 만드는 것은 맞다. 그러나 **만료 전인데** 검증에
    실패하는 것은 다른 사건이고, 그 위에 새 lease 를 얹으면 이상을 덮어쓴다.

    재진입점인 `retain()` 을 직접 부른다 — `finalize_only()` 로 들어가면 이미
    등록된 journal 검증에서 먼저 죽어 `_existing_lease()` 까지 오지도 않는다
    (실측했다: 그 경로로는 이 분기를 지우는 변이가 초록이었다).
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg, ld = PLANNED.leg_id, res["retention"]["lease_digest"]
    lease = res["retention"]
    assert not _lease_expired_t(lease), "전제: 만료 전이다"

    def failing(self, *a, **kw):
        raise PreserveError("retention", "검증이 어긋났다 (주입)")

    monkeypatch.setattr(P.ObjectLockBackend, "verify_retention", failing)
    with pytest.raises(PreserveError):
        backend.retain(leg, lease["objects"],
                       min_retention_days=lease["min_retention_days"])
    monkeypatch.undo()

    leases = {dg for dg in backend.pinned(leg)
              if _looks_like_lease(backend, leg, dg)}
    assert leases == {ld}, (
        f"만료 전 불일치 위에 새 lease 를 얹었다: {sorted(leases)}")


def test_a_repair_that_raises_is_refused_not_replaced(tmp_path, monkeypatch):
    """★ 37차 P0-1 — 수리 실패는 **후보 부재가 아니다.**

    후보를 읽는 데 실패하는 축은 위 `..._not_the_same_as_no_candidate` 가
    본다. 여기는 그 다음 단계다 — 후보는 잘 읽혔는데 **수리가** 실패하는
    경우. 36차판은 둘 다 `None` 으로 접었다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg, ld = PLANNED.leg_id, res["retention"]["lease_digest"]
    lease = res["retention"]

    def failing(self, *a, **kw):
        raise PreserveError("retention", "수리가 실패했다 (주입)")

    monkeypatch.setattr(P.ObjectLockBackend, "repair_lease_locks", failing)
    with pytest.raises(PreserveError) as ex:
        backend.retain(leg, lease["objects"],
                       min_retention_days=lease["min_retention_days"])
    monkeypatch.undo()
    assert "수리" in str(ex.value), str(ex.value)

    leases = {dg for dg in backend.pinned(leg)
              if _looks_like_lease(backend, leg, dg)}
    assert leases == {ld}, f"수리 실패 위에 새 lease 를 얹었다: {sorted(leases)}"


def _lease_expired_t(lease) -> bool:
    from tools.preserve import _lease_expired
    return _lease_expired(lease)


def test_two_lease_candidates_are_refused_not_resolved_by_guessing(tmp_path,
                                                                   monkeypatch):
    """★ 37차 P0-1 — 후보가 둘이면 `None` 이 아니라 **거부**다.

    36차판은 `len(extra) != 1` 이면 조용히 `None` 을 돌려 세 번째 lease 를
    만들었다. 이미 오염된 상태에 되돌릴 수 없는 것을 하나 더 얹는 것이
    기본값이면 안 된다.
    """
    store, backend, index = _crash_at_lease_pin(tmp_path, monkeypatch)
    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: lease 후보가 하나 있다"

    # graph 에 없는 두 번째 object 를 pin 한다 — 후보가 둘이 된다
    other = backend.put_if_absent(b"second-non-graph-object")["digest"]
    backend.pin(leg, [other])
    assert len({d for d in backend.pinned(leg)} ) >= 2, "전제"

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    with pytest.raises(PreserveError) as ex:
        finalize_only(leg, fresh, index)
    assert "정할 수 없다" in str(ex.value) or "2개" in str(ex.value), str(ex.value)

    leases = {dg for dg in fresh.pinned(leg) if _looks_like_lease(fresh, leg, dg)}
    assert leases == {ld}, f"모호한 상태에 lease 를 더 만들었다: {sorted(leases)}"


def test_an_expired_lease_is_refused_and_says_why(tmp_path, monkeypatch):
    """★ 38차 P0-1 — 37차의 **자동 갱신은 가짜 기능이었다.**

    37차판은 만료된 lease 를 만나면 새 L1 을 만들었고, 시험은 `retain()`
    반환값의 digest 와 날짜만 봤다. production 은 다르다 — `retain()` 직후
    `verify_graph_before_registration()` 이 exact pin set 을 요구하는데,
    `pinned()` 은 historical WORM L0 를 active 로 세므로 `graph ∪ {L0, L1}` 이
    되어 **같은 호출 안에서** 실패한다. `delete` 는 계약에 없으므로 L0 를
    퇴역시킬 수단도 없다.

    그래서 기능을 뺐다. 담보 기간이 지난 것은 사람이 판단할 사건이고,
    조용한 재발급은 지울 수 없는 WORM 잔여만 남긴다. 거부는 **이유를 말한다.**
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease = res["retention"]

    far = (dt.datetime.now(dt.timezone.utc)
           + dt.timedelta(days=lease["min_retention_days"] + 10))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return far

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    with pytest.raises(PreserveError) as ex:
        backend.retain(PLANNED.leg_id, lease["objects"],
                       min_retention_days=lease["min_retention_days"])
    monkeypatch.undo()
    assert "자동 갱신은 지원하지 않는다" in str(ex.value), str(ex.value)

    leases = {dg for dg in backend.pinned(PLANNED.leg_id)
              if _looks_like_lease(backend, PLANNED.leg_id, dg)}
    assert leases == {lease["lease_digest"]}, (
        f"거부해야 하는데 lease 를 더 만들었다: {sorted(leases)}")


# ─────────────────────────────────────────────────────────────────────────────
# 37차 P0-1 — store.json 은 잠겼지만 **어느 version 이 정본인지**는 안 잠겼다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_newer_locked_store_record_cannot_switch_the_identity(tmp_path):
    """★ 37차 P0-1 — `protected_version()` 은 "최신 잠긴 version" 이다.

    canonical identity 를 특정 immutable version 에 결속하지 않으므로, 계약
    **안에서** 다음이 성립한다:

        1. store.json vA = {store_id: A} 를 만들고 잠근다
        2. graph 와 receipt 를 A 에 결속해 정상 등록한다
        3. 더 최신 vB = {store_id: B} 를 put 하고 같은 지평까지 잠근다
        4. fresh backend 로 reopen 한다
        5. protected_version() 이 vB 를 골라 store_id 가 B 가 된다

    vA 도 예전 graph 의 모든 object version 도 그대로 잠겨 있다. 잃은 것은
    바이트가 아니라 **locator** 다 — 예전 receipt 전부가 foreign store 가
    되어 검증도 finalize 도 막힌다.

    36차 회귀는 `{}` 라는 **잠기지 않은** invalid head 만 올렸다. 그러면
    locator 가 예전 vA 로 돌아가는 것이 당연해서 이 축을 못 물었다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    a_id = backend.store_id
    assert _is_hex64_str(a_id) or len(a_id) == 32

    # ── 더 최신이고 **유효하며 잠긴** 두 번째 record ────────────────────
    vb = store.put("store.json", canonical_bytes(
        {"schema": "cas-store/v1", "store_id": "b" * 32}))
    store.lock("store.json", vb, res["retention"]["retain_until_utc"])
    assert store.versions("store.json")[0] == vb, "전제: 더 최신이다"

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    try:
        got = fresh.store_id
    except PreserveError:
        return                       # ambiguity 로 fail-closed 도 정답이다
    assert got == a_id, (
        f"더 최신 잠긴 record 가 identity 를 갈아치웠다: {got} ≠ {a_id} — "
        "예전 receipt 전부가 foreign store 가 된다")


def test_the_store_record_must_be_an_exact_schema_not_just_a_uuid(tmp_path):
    """★ 37차 P0-1 — parser 가 mapping 과 32-hex `store_id` 만 봤다.

    exact key set 도 schema 값도 안 봐서, 남는 key 를 단 record 나 다른
    schema 의 record 도 잠겨서 canonical identity 로 받아들여졌다.
    """
    for i, bad in enumerate([
            {"store_id": "c" * 32},                                # schema 없음
            {"schema": "other/v9", "store_id": "c" * 32},          # 다른 schema
            {"schema": "cas-store/v1", "store_id": "c" * 32, "x": 1},  # 남는 key
    ]):
        store = _LockingStore(name=f"{tmp_path}-bad{i}")
        store.put("store.json", canonical_bytes(bad))
        backend = _lockstore(tmp_path / f"b{i}", store)
        sid = None
        try:
            sid = backend.store_id
        except PreserveError:
            continue                 # 거부가 정답이다
        assert sid != "c" * 32, (
            f"계약이 아닌 record 를 canonical identity 로 받았다: {bad}")


def test_a_locked_non_contract_store_record_is_refused_not_reissued(tmp_path):
    """★ 37차 P0-1 — 담보 version 이 계약 record 가 아니면 **거부**다.

    위 schema 시험은 잠기지 않은 record 를 쓰므로 이 분기를 안 지난다.
    잠긴 쓰레기는 지울 수 없으므로, 그 위에 새 UUID 를 발급하면 두 개의
    영구 record 가 남고 다음 reopen 이 어느 것을 고를지 알 수 없게 된다.
    """
    store = _LockingStore(name=str(tmp_path))
    v = store.put("store.json", canonical_bytes({"schema": "junk/v1", "x": 1}))
    store.lock("store.json", v, "2099-01-01T00:00:00Z")

    backend = _lockstore(tmp_path, store)
    with pytest.raises(PreserveError) as ex:
        backend.store_id
    assert "계약" in str(ex.value), str(ex.value)
    assert len(store.versions("store.json")) == 1, (
        "거부해야 하는데 새 record 를 발급했다")


# ─────────────────────────────────────────────────────────────────────────────
# 37차 P0-1 — 회수가 lease 가 봉인한 exact version 을 쓰지 않았다
# ─────────────────────────────────────────────────────────────────────────────

def test_retrieval_reads_the_sealed_version_not_the_newest_locked_one(tmp_path):
    """★ 37차 P0-1 — `retrieve_retained()` 이 locator 를 **재탐색**했다.

    `retrieve_retained → read_pinned → _read_protected` 는 lease 의
    `object_versions[digest]` 를 받지 않고 "가장 최신 잠긴 version" 을 다시
    골랐다. 정상 lease 가 v1 을 봉인한 뒤 같은 pin key 에 **다른 바이트**의
    v2 를 put 하고 잠그면, v1 은 그대로 durable 하고 exact version read 도
    가능한데 회수는 v2 를 골라 digest mismatch 로 실패한다.

    retention receipt 의 목적은 locator 를 재발견하는 것이 아니라 **exact
    immutable version 을 회수**하는 것이다.

    36차 회귀는 새 version 을 **잠그지 않아서** v1 fallback 만 확인했다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease, leg = res["retention"], PLANNED.leg_id

    victim = sorted(lease["objects"])[0]
    key = backend._provider_key(leg, victim)
    sealed = lease["object_versions"][victim]
    assert store.get(key, sealed), "전제: 봉인 version 이 읽힌다"

    # 적대적(또는 사고성) 새 version 을 올리고 **그것도 잠근다**
    v2 = store.put(key, b"different-bytes-entirely")
    store.lock(key, v2, lease["retain_until_utc"])
    assert backend.protected_version(key) == v2, "전제: 최신 담보가 v2 다"

    got = backend.retrieve_retained(lease, victim)
    assert hashlib.sha256(got).hexdigest() == victim, (
        "회수가 봉인 version 이 아니라 최신 잠긴 version 을 읽었다")


def test_an_expired_lease_fails_closed_in_the_production_path(tmp_path,
                                                              monkeypatch):
    """★ 38차 P0-1 — production 경로가 **무엇을 하는지** 확인한다.

    37차 갱신 시험은 `retain()` 반환값만 봤다. 실제 재개 경로
    (`finalize_only()`)는 journal 의 lease 를 검증하고, 그것이 만료면 거기서
    멈춘다. 갱신은 애초에 도달하지도 않았다 — "갱신이 된다" 는 주장이
    production 을 한 번도 지나지 않았다는 뜻이다.

    지금은 그것이 **의도된 동작**이다. 거부하고 이유를 말한다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    days = res["retention"]["min_retention_days"]

    far = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=days + 10)

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return far

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    with pytest.raises(PreserveError) as ex:
        finalize_only(PLANNED.leg_id, fresh, index)
    monkeypatch.undo()
    assert "만료" in str(ex.value), str(ex.value)

    # 그리고 **아무것도 늘지 않았다** — 실패가 상태를 만들면 안 된다
    leases = {dg for dg in fresh.pinned(PLANNED.leg_id)
              if _looks_like_lease(fresh, PLANNED.leg_id, dg)}
    assert leases == {res["retention"]["lease_digest"]}


# ─────────────────────────────────────────────────────────────────────────────
# 38차 P0-1 — candidate 가 눈앞에 있는데 `None` 으로 접히는 구멍
# ─────────────────────────────────────────────────────────────────────────────

def test_a_stronger_policy_request_does_not_mint_a_second_lease(tmp_path):
    """★ 38차 P0-1 — metadata mismatch 가 아직 `return None` 이었다.

    37차는 "후보가 하나라도 있으면 새 state 를 만들지 않는다" 고 선언했지만,
    candidate 를 읽은 뒤 `objects`·정책 일수·store ID·URI·enforcement 중
    하나가 다르면 여전히 `None` 이었고 `retain()` 은 그것을 후보 부재와 같이
    취급했다.

    가장 작은 정상 입력 반례 — 같은 graph 에 **더 강한** 담보를 요청한다:

        L0: graph G, 365일, 만료 전
        retry: graph G, 730일
        → metadata 불일치 → None → L1 생성 → pinned = G ∪ {L0, L1} → exact 실패
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store, retention_days=MIN_RETENTION_DAYS * 10)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg, l0 = PLANNED.leg_id, res["retention"]["lease_digest"]

    with pytest.raises(PreserveError):
        backend.retain(leg, res["retention"]["objects"],
                       min_retention_days=MIN_RETENTION_DAYS * 2)

    leases = {dg for dg in backend.pinned(leg) if _looks_like_lease(backend, leg, dg)}
    assert leases == {l0}, (
        f"정책 강화 요청이 두 번째 WORM lease 를 만들었다: {sorted(leases)}")


def test_a_forged_candidate_is_refused_before_anything_is_made_worm(tmp_path,
                                                                   monkeypatch):
    """★ 38차 P0-1 — 수리가 **검증보다 먼저** 상태를 바꿨다.

    `repair_lease_locks()` 는 strict verifier 앞에 있고, exact key/schema
    검사는 `verify_retention()` **안**에 있다. 그래서 부분적으로만 맞는
    forged candidate 를 먼저 pin·content WORM 으로 만든 다음 "schema 가
    틀렸다" 고 거부할 수 있다. 거부는 맞지만 **되돌릴 수 없는 상태 변경이
    검증보다 앞섰다.**
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    objs = sorted(backend.put_if_absent(b"g%d" % i)["digest"] for i in range(2))
    leg = "hc22p_v6_armA_b20"
    backend.pin(leg, objs)

    # 남는 key 를 단 forged lease — 필드 대부분은 맞다
    forged = {
        "schema": P_RETENTION_SCHEMA, "leg_id": leg, "objects": objs,
        "min_retention_days": MIN_RETENTION_DAYS,
        "retain_until_utc": "2099-01-01T00:00:00Z",
        "store_id": backend.store_id, "backend_uri": backend.uri,
        "enforcement": backend.probe_enforcement(), "lock_mode": "COMPLIANCE",
        "object_versions": {}, "pin_set_digest": pin_set_digest(leg, objs),
        "surplus_key": "이것이 계약을 깬다",
    }
    fd = backend.put_if_absent(canonical_bytes(forged))["digest"]
    backend.pin(leg, [fd])
    before = _version_census(store)

    with pytest.raises(PreserveError):
        backend.retain(leg, objs, min_retention_days=MIN_RETENTION_DAYS)

    after = _version_census(store)
    grew = {k: (before.get(k, 0), n) for k, n in after.items()
            if n > before.get(k, 0)}
    assert not grew, f"거부하기 전에 상태를 바꿨다: {grew}"
    assert backend.protected_version(backend._provider_key(leg, fd)) is None, (
        "forged candidate 를 WORM 으로 만든 뒤 거부했다 — 되돌릴 수 없다")


def test_an_orphan_from_a_foreign_store_is_not_adopted(tmp_path):
    """★ 38차 P0-1 — `_matches_lease()` 가 store·URI·enforcement 를 안 봤다.

    schema·leg·objects·정책일수·만료만 봐서, 다른 store 의 lease 나 남는 key 가
    있는 record 도 orphan 으로 **입양**됐다. 입양은 pin 을 만드는 mutation 이다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    objs = sorted(backend.put_if_absent(b"h%d" % i)["digest"] for i in range(2))
    leg = "hc22p_v6_armA_b20"
    backend.pin(leg, objs)

    alien = {
        "schema": P_RETENTION_SCHEMA, "leg_id": leg, "objects": objs,
        "min_retention_days": MIN_RETENTION_DAYS,
        "retain_until_utc": "2099-01-01T00:00:00Z",
        "store_id": "f" * 32,                       # ← 남의 store
        "backend_uri": "objectlock+cas://elsewhere",
        "enforcement": "object_lock", "lock_mode": "COMPLIANCE",
        "object_versions": {dg: "v00001" for dg in objs},
        "pin_set_digest": pin_set_digest(leg, objs),
    }
    ad = backend.put_if_absent(canonical_bytes(alien))["digest"]

    got = backend._orphan_lease(leg, objs, MIN_RETENTION_DAYS)
    assert got is None, "남의 store 의 lease 를 입양 후보로 봤다"
    assert ad not in backend.pinned(leg), "입양하면서 pin 을 만들었다"


def test_an_orphan_with_a_forged_pin_set_digest_is_not_adopted(tmp_path):
    """★ 38차 P0-1 — 입양 경로에서는 `_matches_lease()` 가 **유일한 관문**이다.

    pin 된 후보는 `verify_retention()` 이 `pin_set_digest` 를 한 번 더 보지만,
    orphan 입양은 그 앞에서 pin 을 만든다 (mutation). 여기가 느슨하면 위조된
    record 를 먼저 pin 으로 만든 다음 거부하게 된다.

    (변이로 확인했다 — 이 축을 지워도 나머지 시험은 전부 초록이었다.)
    """
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    objs = sorted(backend.put_if_absent(b"k%d" % i)["digest"] for i in range(2))
    leg = "hc22p_v6_armA_b20"
    backend.pin(leg, objs)

    forged = {
        "schema": P_RETENTION_SCHEMA, "leg_id": leg, "objects": objs,
        "min_retention_days": MIN_RETENTION_DAYS,
        "retain_until_utc": "2099-01-01T00:00:00Z",
        "store_id": backend.store_id, "backend_uri": backend.uri,
        "enforcement": backend.probe_enforcement(), "lock_mode": "COMPLIANCE",
        "object_versions": {dg: "v00001" for dg in objs},
        "pin_set_digest": "0" * 64,                 # ← 위조
    }
    fd = backend.put_if_absent(canonical_bytes(forged))["digest"]

    assert backend._orphan_lease(leg, objs, MIN_RETENTION_DAYS) is None, (
        "pin_set_digest 가 위조된 record 를 입양 후보로 봤다")
    assert fd not in backend.pinned(leg), "입양하면서 pin 을 만들었다"


# ─────────────────────────────────────────────────────────────────────────────
# 38차 P0-1 — exact-version 이 lifecycle 전체로 이어지지 않았다
# ─────────────────────────────────────────────────────────────────────────────

def test_the_registered_verifier_reads_the_lease_at_its_sealed_version(tmp_path):
    """★ 38차 P0-1 — journal 의 `lease_version` 을 **bytes 읽기에 안 썼다.**

    `verify_registered_graph()` 는 journal 의 `lease_version` 을 verifier 에
    넘기지만, verifier 는 먼저 `read_lease()` 를 부르고 그것은 version 없이
    `read_pinned()` 한다. `lease_version` 은 바이트를 읽은 **뒤** live lock
    describe 에만 쓰였다.

    그래서 같은 lease pin key 에 더 최신 locked hostile bytes 가 있으면,
    journal 이 exact v1 을 들고 있고 v1 이 온전해도 verifier 는 newest locked
    v2 를 읽다 digest mismatch 로 실패한다. receipt 의 exact locator 가 있는데
    lifecycle 이 그것을 못 쓴다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg, ld = PLANNED.leg_id, res["retention"]["lease_digest"]

    key = backend._provider_key(leg, ld)
    v2 = store.put(key, b"hostile-lease-bytes")
    store.lock(key, v2, res["retention"]["retain_until_utc"])
    assert backend.protected_version(key) == v2, "전제: 최신 담보가 v2 다"

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    assert assert_durable_retention(fresh, index, leg), (
        "journal 의 exact lease version 이 있는데 verifier 가 v2 를 읽었다")


def test_pin_verification_uses_the_sealed_graph_versions(tmp_path):
    """★ 38차 P0-1 — `verify_pins()` 가 lease 의 version map 을 버렸다.

    등록 verifier 는 exact receipt·manifest 를 회수한 뒤 `verify_pins()` 를
    부르는데, 기본 구현은 각 digest 를 version 없이 읽는다. 37차 회귀는
    `retrieve_retained()` 만 봐서 이 경로를 안 지났다 — 같은 상태에서
    `verify_registered_graph()` 는 실패한다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg = PLANNED.leg_id

    victim = sorted(res["retention"]["objects"])[0]
    key = backend._provider_key(leg, victim)
    v2 = store.put(key, b"hostile-graph-bytes")
    store.lock(key, v2, res["retention"]["retain_until_utc"])

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    assert assert_durable_retention(fresh, index, leg), (
        "봉인된 graph pin version 이 있는데 verifier 가 최신을 읽었다")


def test_the_lease_content_version_is_sealed_too(tmp_path):
    """★ 38차 P0-1 — lease **CAS content** version 은 어디에도 안 봉인됐다.

    journal 의 `lease_version` 은 lease **pin** version 이다. content version
    proof 가 없으므로 `describe_content_lock()` 은 `objects/<lease>` 에서 newest
    live locked version 을 다시 고른다. 올바른 v1 content 를 지우고 wrong bytes
    v2 를 올려 잠그면, lease pin v1 이 올바르게 남아 있어도 "lease CAS content
    가 잠겼다" 는 검사가 v2 의 mode·date 만 보고 통과할 수 있다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg, ld = PLANNED.leg_id, res["retention"]["lease_digest"]

    key = backend._provider_obj_key(ld)
    v2 = store.put(key, b"wrong-content-bytes")
    store.lock(key, v2, res["retention"]["retain_until_utc"])

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    assert assert_durable_retention(fresh, index, leg), (
        "lease content version proof 가 없어 아무 잠긴 version 이나 받는다")

    # ★ **어느 version 이 proof 인가** 를 본다. "통과했다" 만 보면 hostile v2 를
    #   받아들이는 구현도 초록이다 (변이로 확인했다).
    st = fresh.describe_content_lock(ld)
    assert isinstance(st, dict), "content proof 를 못 찾았다"
    assert st["version_id"] != v2, (
        f"바이트가 다른 hostile version 을 content proof 로 받았다: {v2}")
    assert hashlib.sha256(
        store.get(key, st["version_id"])).hexdigest() == ld, (
        "proof version 의 바이트가 lease digest 와 다르다")


def test_the_canonical_store_version_is_sealed_in_the_lease(tmp_path):
    """★ 38차 P0-1 — store authority 가 **live-lock census** 였다.

    `_canonical_store_version()` 은 "지금 잠겨 있는 것 중 가장 오래된 것" 이라
    시간이 지나면 선택 결과가 바뀐다:

        vA = store_id A, lock until T1
        vB = store_id B, lock until T2 (T2 > T1)
        T1 이전: canonical = vA   ·   T1 이후: canonical = vB

    바이트가 다 남아 있어도 reopen 시점의 census 때문에 identity 가 바뀐다.
    proof 가 아니라 heuristic 이다. lease 에 **exact version ID 와 mode** 를
    봉인하고 그것으로 조회해야 한다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())

    lease = res["retention"]
    assert lease.get("store_version_id"), "lease 에 store version proof 가 없다"
    assert lease.get("store_lock_mode") == "COMPLIANCE", (
        f"store version 의 mode 가 안 봉인됐다: {lease.get('store_lock_mode')!r}")

    # 그 version 이 실제 canonical 이어야 한다
    assert backend._canonical_store_version() == lease["store_version_id"]


def test_a_governance_store_version_is_not_a_canonical_candidate(tmp_path):
    """★ 38차 P0-1 — Governance 제외가 store selector 까지 안 갔다.

    `DURABLE_MODES` 는 Compliance 뿐인데 `_canonical_store_version()` 은
    `LOCK_MODES`(Governance 포함)로 후보를 골랐다. 오래된 record 가
    Governance 이고 provider 의 현재 mode 가 Compliance 이면, 전체 probe 는
    durable 인데 identity root 는 우회 가능한 version 일 수 있다.
    """
    store = _LockingStore(name=str(tmp_path), mode="GOVERNANCE")
    backend = _lockstore(tmp_path, store)
    v_gov = store.put("store.json", canonical_bytes(
        {"schema": "cas-store/v1", "store_id": "a" * 32}))
    store.lock("store.json", v_gov, "2099-01-01T00:00:00Z")
    assert store.describe_object("store.json", v_gov)["mode"] == "GOVERNANCE"

    store.mode = "COMPLIANCE"          # 이후 record 는 Compliance 로 잠긴다
    v_comp = store.put("store.json", canonical_bytes(
        {"schema": "cas-store/v1", "store_id": "b" * 32}))
    store.lock("store.json", v_comp, "2099-01-01T00:00:00Z")
    assert store.describe_object("store.json", v_comp)["mode"] == "COMPLIANCE"

    got = backend._canonical_store_version()
    assert got != v_gov, (
        "우회 가능한 GOVERNANCE version 을 identity root 로 골랐다 — "
        "durable 에서 뺀 mode 가 identity root 로는 들어왔다")
    assert got == v_comp, f"Compliance 후보를 못 골랐다: {got!r}"


def test_a_tampered_store_version_seal_is_refused(tmp_path):
    """★ 38차 P0-1 — 봉인한 store version 을 **실제로 조회**해야 한다.

    lease 에 `store_version_id` 를 적어 두고 검증이 그것을 안 보면 그냥 주석
    이다. 봉인된 version 의 잠금이 풀리면 거부해야 한다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease = res["retention"]
    sv = lease["store_version_id"]
    assert sv, "전제: 봉인돼 있다"

    store._lock.pop(("store.json", sv))          # 봉인 version 의 담보가 풀렸다

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    with pytest.raises(PreserveError) as ex:
        fresh.verify_retention(PLANNED.leg_id, lease["lease_digest"],
                               lease=dict(lease),
                               lease_version=lease["lease_version"])
    assert "store version" in str(ex.value), str(ex.value)


def test_the_fake_enforces_per_version_mode_and_monotonic_compliance(tmp_path):
    """★ 38차 P0-1 — fake 의 lock 이 실물 Compliance 의미를 갖는가.

    37차판은 `until` 을 단순 대입하고 mode 를 저장하지 않았다. 그래서
    Compliance retention 을 **짧게** 덮을 수 있었고, 전역 mode 를 바꾸면 과거
    모든 version 의 mode 가 소급 변경됐다. canary 가 실물보다 약하면 그 위의
    모든 durable 주장이 그만큼 약하다 — 이 저장소에서 세 번 나온 실수다
    (31·32·37차).
    """
    store = _LockingStore(name=str(tmp_path), mode="COMPLIANCE")
    v = store.put("k", b"payload")
    store.lock("k", v, "2099-01-01T00:00:00Z")

    with pytest.raises(PermissionError):
        store.lock("k", v, "2027-01-01T00:00:00Z")     # 단축 시도
    assert store.describe_object("k", v)["retain_until"] == "2099-01-01T00:00:00Z"

    store.lock("k", v, "2100-01-01T00:00:00Z")         # 연장은 된다
    assert store.describe_object("k", v)["retain_until"] == "2100-01-01T00:00:00Z"

    store.mode = "GOVERNANCE"                          # 나중에 store mode 를 바꿔도
    assert store.describe_object("k", v)["mode"] == "COMPLIANCE", (
        "잠글 때 봉인된 mode 가 소급 변경됐다")


# ─────────────────────────────────────────────────────────────────────────────
# 39차 P0-1 — validator 가 **새 locator 의미**를 보기 전에 WORM 을 만든다
# ─────────────────────────────────────────────────────────────────────────────

def _valid_candidate(tmp_path, name, **over):
    """**실제로 유효한** candidate 상태를 만들고, `over` 로 한 축만 위조한다.

    ★ 40차 P0-1 — 이 fixture 를 두 번 고쳤다. 둘 다 시험이 자기 이름의 축을
      실행하지 못하게 만들고 있었다:

        1판: pin 을 안 잠그고 `object_versions` 에 가짜 값 → 어느 축을
             위조하든 거절 (locator 실존 검사를 지워도 초록이었다)
        2판: `retain()` 을 불러 **진짜 lease 가 이미 pin** → 후보가 둘이 되어
             ambiguity 가 먼저 물었다 (같은 변이가 여전히 초록이었다)

    이제 graph 만 pin·잠그고 **lease 는 만들지 않는다.** 그 위에 위조 candidate
    하나만 얹으므로 후보가 정확히 하나다. 위조가 없으면 `_matches_lease()` 는
    **True** 다 (그 반대 축도 아래 시험이 확인한다).
    """
    store = _LockingStore(name=name)
    backend = _lockstore(tmp_path, store)
    leg = "hc22p_v6_armA_b20"
    objs = sorted(backend.put_if_absent(b"g%d" % i)["digest"] for i in range(2))
    backend.pin(leg, objs)

    until = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    backend.store_id                      # record 를 만들고 잠근다 (먼저)
    backend.ensure_store_lock(until)
    versions = backend.lock_objects(leg, objs, until)

    rec = {
        "schema": P_RETENTION_SCHEMA, "leg_id": leg, "objects": objs,
        "min_retention_days": MIN_RETENTION_DAYS, "retain_until_utc": until,
        "store_id": backend.store_id,
        "store_version_id": backend.store_version_id,
        "store_lock_mode": backend.store_lock_mode,
        "backend_uri": backend.uri,
        "enforcement": backend.probe_enforcement(),
        "lock_mode": "COMPLIANCE",
        "object_versions": dict(versions),
        "pin_set_digest": pin_set_digest(leg, objs),
    }
    rec.update(over)
    return store, backend, leg, objs, rec


def _lease_like(backend, leg, objs, **over) -> dict:
    """계약 key 를 정확히 갖춘 lease record. `over` 로 한 축만 위조한다."""
    rec = {
        "schema": P_RETENTION_SCHEMA, "leg_id": leg, "objects": objs,
        "min_retention_days": MIN_RETENTION_DAYS,
        "retain_until_utc": "2099-01-01T00:00:00Z",
        "store_id": backend.store_id,
        "store_version_id": backend.store_version_id or "",
        "store_lock_mode": backend.store_lock_mode or "",
        "backend_uri": backend.uri,
        "enforcement": backend.probe_enforcement(),
        "lock_mode": "COMPLIANCE",
        "object_versions": {dg: "v00001" for dg in objs},
        "pin_set_digest": pin_set_digest(leg, objs),
    }
    rec.update(over)
    return rec


@pytest.mark.parametrize("axis,over", [
    ("store_version_id", {"store_version_id": ""}),
    ("store_lock_mode", {"store_lock_mode": "GOVERNANCE"}),
    ("lock_mode", {"lock_mode": "GOVERNANCE"}),
    ("object_versions_missing", {"object_versions": {}}),
    ("timestamp", {"retain_until_utc": "not-a-date"}),
    ("store_version_absent", {"store_version_id": "v-does-not-exist"}),
    ("graph_version_absent", {"object_versions": "ABSENT"}),
    ("graph_version_wrong_bytes", {"object_versions": "WRONG_BYTES"}),
    ("graph_version_short_horizon", {"object_versions": "SHORT"}),
    ("graph_version_wrong_mode", {"object_versions": "MODE"}),
    # ★ 41차 P0-1 — store locator 는 **bytes 를 아예 안 봤다**
    ("store_version_other_store", {"store_version_id": "OTHER_STORE"}),
    ("store_version_not_a_record", {"store_version_id": "NOT_A_RECORD"}),
])
def test_a_forged_candidate_axis_is_refused_without_touching_anything(
        tmp_path, axis, over):
    """★ 39·40차 P0-1 — 위조 축마다 **거부 전에 아무것도 안 바뀌어야** 한다.

    39차판 fixture 는 pin 을 잠그지 않고 `object_versions` 에 가짜 값을 넣어
    두었다. 그러면 candidate 가 어느 축을 위조하든 거절되므로 시험이 자기
    이름의 축을 한 번도 실행하지 못한다 — locator 실존 검사를 지우는 변이가
    넷 다 초록이었다. 이제 **실제로 유효한** candidate 에서 한 축만 위조한다.

    축 여덟: 빈 store locator · Governance store mode · Governance lock_mode ·
    빈 object_versions · 잘못된 timestamp 문법 · **존재하지 않는** store
    version · **존재하지 않는** graph version · **바이트가 다른** graph version.
    """
    store2, backend2, leg, objs, clean = _valid_candidate(
        tmp_path, f"{tmp_path}-{axis}")
    assert backend2._matches_lease(leg, objs, MIN_RETENTION_DAYS, clean), (
        "전제: 위조 없는 candidate 는 통과한다")

    if over.get("object_versions") == "ABSENT":
        over = {"object_versions": {d: "v-does-not-exist" for d in objs}}
    elif over.get("object_versions") in ("WRONG_BYTES", "SHORT", "MODE"):
        kind = over["object_versions"]
        dg = objs[0]
        key = backend2._provider_key(leg, dg)
        if kind == "WRONG_BYTES":
            # 같은 key 에 **다른 바이트**의 version 을 올리고 잠근다 —
            # 존재하고 잠겨 있으므로 bytes 대조만이 잡는다
            v = store2.put(key, b"different-bytes-entirely")
            store2.lock(key, v, clean["retain_until_utc"])
        elif kind == "SHORT":
            # 존재·mode·bytes 는 맞고 **기한만 짧다**
            v = store2.put(key, store2.get(key, clean["object_versions"][dg]))
            store2.lock(key, v, "2027-01-01T00:00:00Z")
        else:
            # 존재·bytes·기한 은 맞고 **mode 만 다르다**
            v = store2.put(key, store2.get(key, clean["object_versions"][dg]))
            store2.lock(key, v, clean["retain_until_utc"])
            store2._mode[(key, v)] = "GOVERNANCE"
        over = {"object_versions": dict(clean["object_versions"], **{dg: v})}
    elif over.get("store_version_id") in ("OTHER_STORE", "NOT_A_RECORD"):
        # ★ 41차 P0-1 — 존재·mode·기한은 **전부 맞고** 그 version 의 record 만
        #   다르다. 40차 `_locator_holds()` 는 store 를 `dg=None` 으로 불러
        #   bytes 분기를 통째로 건너뛰었으므로 이 둘이 모두 통과했다.
        payload = (canonical_bytes({"schema": P_STORE_SCHEMA,
                                    "store_id": uuid.uuid4().hex})
                   if over["store_version_id"] == "OTHER_STORE"
                   else b"not-a-store-record-at-all")
        v = store2.put("store.json", payload)
        store2.lock("store.json", v, clean["retain_until_utc"])
        over = {"store_version_id": v}
    rec = dict(clean, **over)

    fd = backend2.put_if_absent(canonical_bytes(rec))["digest"]
    backend2.pin(leg, [fd])

    before_v = _version_census(store2)
    before_lock = dict(store2._lock)
    before_pins = set(backend2.pinned(leg))
    before_store = store2.get("store.json")

    with pytest.raises(PreserveError):
        backend2.retain(leg, objs, min_retention_days=MIN_RETENTION_DAYS)

    grew = {k: (before_v.get(k, 0), n)
            for k, n in _version_census(store2).items() if n > before_v.get(k, 0)}
    assert not grew, f"{axis}: 거부 전에 version 을 늘렸다: {grew}"
    assert dict(store2._lock) == before_lock, f"{axis}: 거부 전에 잠금이 바뀌었다"
    assert set(backend2.pinned(leg)) == before_pins, f"{axis}: pin 집합이 변했다"
    assert store2.get("store.json") == before_store, f"{axis}: store record 가 변했다"


def test_validating_a_candidate_never_creates_the_store_record(tmp_path):
    """★ 39차 P0-1 — "순수 validator" 가 `self.store_id` 를 불렀다.

    `store_id` 는 record 가 없으면 **만들고 잠그며**, 있으면
    `ensure_store_lock()` 으로 기한을 연장한다. 둘 다 mutation 이다. 검증이
    상태를 바꾸면 "거부 전에 아무것도 안 바꿨다" 는 주장이 성립하지 않는다.

    가장 관측하기 쉬운 형태로 본다 — store record 가 **아직 없는** backend 에서
    validator 를 부르고, 그래도 안 생기는지 확인한다.
    """
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    assert store.versions("store.json") == [], "전제: 아직 없다"

    rec = {"schema": P_RETENTION_SCHEMA, "leg_id": "hc22p_v6_armA_b20",
           "objects": ["a" * 64], "min_retention_days": MIN_RETENTION_DAYS,
           "retain_until_utc": "2099-01-01T00:00:00Z", "store_id": "0" * 32,
           "store_version_id": "v1", "store_lock_mode": "COMPLIANCE",
           "backend_uri": backend.uri, "enforcement": "object_lock",
           "lock_mode": "COMPLIANCE", "object_versions": {"a" * 64: "v1"},
           "pin_set_digest": pin_set_digest("hc22p_v6_armA_b20", ["a" * 64])}
    assert backend._matches_lease("hc22p_v6_armA_b20", ["a" * 64],
                                  MIN_RETENTION_DAYS, rec) is False

    assert store.versions("store.json") == [], (
        "validator 가 store record 를 만들었다 — 검증이 상태를 바꿨다")


# ─────────────────────────────────────────────────────────────────────────────
# 39차 P0-1 — proof 를 더했지만 **빈 값이면 옛 live-search 로 돌아갔다**
# ─────────────────────────────────────────────────────────────────────────────

def test_an_object_lock_lease_without_a_store_version_proof_is_refused(tmp_path):
    """★ 39차 P0-1 — `store_version_id == ""` 이면 검증을 **통째로 건너뛰었다.**

    `if sv and prov is not None:` 이라 빈 값은 조용히 넘어갔다. field 를
    더했지만 **optional** 이면 sealed locator 가 아니라 hint 다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    # ★ `store_lock_mode` 는 **정상으로 둔다** — 그래야 "빈 locator" 축만
    #   실행된다 (둘 다 비우면 mode 검사가 먼저 물어 축이 갈린다).
    lease = dict(res["retention"], store_version_id="")

    with pytest.raises(PreserveError) as ex:
        backend.verify_retention(PLANNED.leg_id, lease["lease_digest"],
                                 lease=lease,
                                 lease_version=lease["lease_version"])
    assert "store" in str(ex.value), str(ex.value)


def test_a_store_version_that_expires_before_the_graph_is_refused(tmp_path):
    """★ 39차 P0-1 — exact store version 의 **기한**을 안 봤다.

    bytes 와 mode 는 봤지만 `retain_until` 이 graph lease 보다 짧은지는 안 봤다.
    identity root 가 graph 보다 먼저 삭제 가능해지면, exact graph version 이
    살아 있어도 reopen locator 를 잃는다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease = res["retention"]
    sv = lease["store_version_id"]

    # store 담보를 graph 보다 **짧게** 만든다 (fake 는 단축을 거부하므로 직접).
    # 검증이 수리하지 않아야 이 상태가 보인다.
    store._lock[("store.json", sv)] = "2027-01-01T00:00:00Z"
    assert store._lock[("store.json", sv)] < lease["retain_until_utc"], "전제"

    with pytest.raises(PreserveError) as ex:
        backend.verify_retention(PLANNED.leg_id, lease["lease_digest"],
                                 lease=dict(lease),
                                 lease_version=lease["lease_version"])
    assert "기한" in str(ex.value) or "짧" in str(ex.value), str(ex.value)


def test_a_governance_only_store_cannot_reach_durable(tmp_path):
    """★ 39차 P0-1 — Compliance selector 를 `store_id` fallback 이 우회했다.

        1. store.json vG 를 valid record 로 GOVERNANCE 잠금
        2. provider 의 현재 default mode 를 COMPLIANCE 로
        3. `_canonical_store_version()` 은 vG 를 빼고 None
        4. `store_id` 는 `_read_protected()` fallback 으로 vG bytes 를 읽는다
        5. `probe_enforcement()` 는 현재 describe 가 Compliance 라 object_lock
        6. lease 에 빈 proof 가 실리고 durable=True 까지 간다
    """
    store = _LockingStore(name=str(tmp_path), mode="GOVERNANCE")
    v = store.put("store.json", canonical_bytes(
        {"schema": "cas-store/v1", "store_id": "a" * 32}))
    store.lock("store.json", v, "2099-01-01T00:00:00Z")
    store.mode = "COMPLIANCE"

    backend = _lockstore(tmp_path, store)
    with pytest.raises(PreserveError) as ex:
        backend.store_id
    assert "COMPLIANCE" in str(ex.value) or "담보" in str(ex.value), str(ex.value)


def test_an_object_lock_journal_without_a_content_proof_is_refused(tmp_path):
    """★ 39차 P0-1 — `lease_content_version` 도 optional 이었다.

    journal parser 가 type·nonempty 를 안 보고, 등록 verifier 는
    `or None` 으로 빈 값을 **의도적으로 지워** live search 로 돌아갔다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    leg = PLANNED.leg_id

    j = registration(index, leg)
    bad = dict(j, lease_content_version="")
    _reg_path(index, leg).write_bytes(canonical_bytes(bad))

    with pytest.raises(PreserveError):
        assert_durable_retention(backend, index, leg)


def test_a_governance_locked_lease_content_is_not_a_compliance_proof(tmp_path):
    """★ 39차 P0-1 — content lock 의 **mode** 를 대조하지 않았다.

    bytes 와 날짜만 보고 dict 존재로 통과시켰다. 같은 lease bytes 의 content
    version 을 GOVERNANCE 로 길게 잠그면 Compliance durable proof 처럼 지나간다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease, leg = res["retention"], PLANNED.leg_id
    key = backend._provider_obj_key(lease["lease_digest"])
    cv = lease["lease_content_version"]

    store._mode[(key, cv)] = "GOVERNANCE"      # 그 version 만 mode 를 바꾼다
    with pytest.raises(PreserveError) as ex:
        assert_durable_retention(backend, index, leg)
    assert "mode" in str(ex.value) or "COMPLIANCE" in str(ex.value), str(ex.value)


@pytest.mark.parametrize("bad", [None, 123, ["v1"], {"v": 1}])
def test_a_journal_locator_that_is_not_a_string_is_not_a_journal(tmp_path, bad):
    """★ 39차 P0-1 — journal parser 가 content locator 의 **type** 을 안 봤다.

    38차판은 `lease_version` 의 type 만 봤다. `lease_content_version` 은
    아무것도 안 봐서 `None`·정수·목록·dict 가 journal 을 통과했다. 빈 문자열은
    `verify_retention()` 이 잡지만, **문자열이 아닌 값**은 거기까지 가기 전에
    구조가 깨진다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    run_transaction(PLANNED, run, backend, index, _hooks())
    leg = PLANNED.leg_id

    j = registration(index, leg)
    _reg_path(index, leg).write_bytes(
        canonical_bytes(dict(j, lease_content_version=bad)))

    assert registration(index, leg) is None, (
        f"journal 이 {type(bad).__name__} locator 를 받아들였다")


# ─────────────────────────────────────────────────────────────────────────────
# 39차 P0-1 — journal 전 재개가 lease pin 의 exact version 을 모른다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_hostile_newer_lease_pin_version_does_not_block_resume(tmp_path,
                                                                 monkeypatch):
    """★ 39차 P0-1 — 재개가 **newest protected** version 을 골랐다.

    등록 뒤에는 journal 의 `lease_version` 을 쓰도록 고쳤지만, journal 전
    crash 에서는 그 proof 가 메모리에서 사라진다. `_existing_lease()` 는 proof
    를 복구하기 **전에** version 없이 읽고, `recover_lease_version()` 은 그
    version 의 바이트가 lease digest 와 같은지 보지 않는다.

        올바른 lease pin v1 을 잠금 → journal 전 crash
        → 같은 pin key 에 wrong-bytes locked v2 삽입
        → 재개가 newest v2 를 읽어 실패 (v1 과 graph 는 온전한데도)

    content 쪽은 `_bytes_match()` 로 고쳤는데 pin 쪽엔 같은 결속이 없었다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, "after_pin_lock")
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)

    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: lease 후보가 있다"
    key = backend._provider_key(leg, ld)
    v1 = backend.protected_version(key)
    assert v1, "전제: 올바른 v1 이 잠겨 있다"

    v2 = store.put(key, b"hostile-newer-lease-pin")
    store.lock(key, v2, "2099-01-01T00:00:00Z")
    assert store.versions(key)[0] == v2, "전제: v2 가 더 최신이다"

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    monkeypatch.undo()

    assert out["ok"] and out["durable"] is True
    assert out["retention"]["lease_digest"] == ld, "같은 lease 로 재개하지 못했다"
    assert out["retention"]["lease_version"] == v1, (
        "바이트가 다른 최신 version 을 lease proof 로 골랐다")


def test_the_fake_refuses_a_bypass_delete_of_a_compliance_version(tmp_path):
    """★ 39차 P0-1 — fake `delete()` 가 **봉인된 mode 를 안 봤다.**

    `lock()` 은 `(key, version)` 별 mode 를 저장하는데 `delete()` 는 mutable 한
    현재 `self.mode` 로 Governance bypass 를 판단했다:

        v1 을 COMPLIANCE 로 잠금 → store.mode = GOVERNANCE
        → delete(key, v1, bypass=True) 가 **성공**

    canary 가 실물보다 약하면 그 위의 durable 판정도 그만큼 약하다.
    """
    store = _LockingStore(name=str(tmp_path), mode="COMPLIANCE", bypass=True)
    v = store.put("k", b"payload")
    store.lock("k", v, "2099-01-01T00:00:00Z")

    store.mode = "GOVERNANCE"                       # 나중에 store mode 를 바꾼다
    with pytest.raises(PermissionError):
        store.delete("k", v, bypass=True)
    assert store.get("k", v) == b"payload", "COMPLIANCE version 이 지워졌다"


def test_the_fake_lets_an_expired_lock_be_deleted(tmp_path, monkeypatch):
    """반대 축 — 만료된 잠금을 **영구 잠금처럼** 취급하면 안 된다.

    이 시험이 없으면 위 시험은 "언제나 거부" 로도 통과한다.
    """
    store = _LockingStore(name=str(tmp_path), mode="GOVERNANCE", bypass=True)
    v = store.put("k", b"payload")
    store.lock("k", v, "2020-01-01T00:00:00Z")      # 이미 지난 기한

    store.delete("k", v)                            # 만료됐으므로 지워진다
    assert store.versions("k") == [], "만료된 잠금이 삭제를 막았다"


# ─────────────────────────────────────────────────────────────────────────────
# 40차 P0-1 — "서로 같다" 와 "허용된 값이다" 는 다른 축이다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_governance_graph_and_lease_pin_are_not_durable(tmp_path):
    """★ 40차 P0-1 — strict verifier 가 mode **membership** 을 안 봤다.

    graph pin 과 lease pin 은 `version.mode == lease.lock_mode` 만 봤다. 그
    값 자체가 Compliance 인지는 안 봤으므로 다음 self-consistent state 가
    통과한다:

        provider 현재 probe = Compliance   (그래서 enforcement=object_lock)
        store exact version = Compliance
        lease content       = Compliance
        lease.lock_mode     = GOVERNANCE
        graph pin · lease pin = GOVERNANCE

    Governance 를 durable policy 에서 뺀 결정과 정면으로 모순된다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease, leg = res["retention"], PLANNED.leg_id

    # ★ **일관되게** Governance 로 만든다. 한 곳만 바꾸면 동등성 검사가 먼저
    #   물어서 membership 축이 실행되지 않는다 (실측했다 — 처음 판은 content
    #   의 동등성이 잡고 있었고, 시험 이름이 실제 predicate 보다 강했다).
    for dg in list(lease["objects"]) + [lease["lease_digest"]]:
        key = backend._provider_key(leg, dg)
        for v in store.versions(key):
            if (key, v) in store._lock:
                store._mode[(key, v)] = "GOVERNANCE"
    ck = backend._provider_obj_key(lease["lease_digest"])
    store._mode[(ck, lease["lease_content_version"])] = "GOVERNANCE"

    bad = dict(lease, lock_mode="GOVERNANCE")
    with pytest.raises(PreserveError) as ex:
        backend.verify_retention(leg, lease["lease_digest"], lease=bad,
                                 lease_version=lease["lease_version"])
    assert "COMPLIANCE" in str(ex.value) or "담보" in str(ex.value), str(ex.value)


@pytest.mark.parametrize("key_kind", ["store", "graph", "lease_pin", "content"])
def test_a_malformed_provider_horizon_is_not_a_future_proof(tmp_path, key_kind):
    """★ 40차 P0-1 — provider 의 `retain_until` 을 **문자열로** 비교했다.

        str(state.get("retain_until") or "") < lease["retain_until_utc"]

    `"zzzz"` 는 어떤 ISO 문자열보다 사전식으로 크므로 "충분한 미래 horizon"
    으로 통과한다. lease record 쪽에는 `_is_utc_stamp()` 를 넣었으면서
    **provider 응답**은 열어 뒀다. 실제 adapter 가 아직 없다는 것은 검사를
    생략할 이유가 아니라 계약을 fail-closed 로 고정할 이유다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease, leg = res["retention"], PLANNED.leg_id

    if key_kind == "store":
        keys = [("store.json", lease["store_version_id"])]
    elif key_kind == "graph":
        dg = sorted(lease["objects"])[0]
        keys = [(backend._provider_key(leg, dg), lease["object_versions"][dg])]
    elif key_kind == "lease_pin":
        keys = [(backend._provider_key(leg, lease["lease_digest"]),
                 lease["lease_version"])]
    else:
        keys = [(backend._provider_obj_key(lease["lease_digest"]),
                 lease["lease_content_version"])]

    for k, v in keys:
        assert (k, v) in store._lock, f"전제: {key_kind} 가 잠겨 있다"
        store._lock[(k, v)] = "zzzz"          # timestamp 가 아니다

    with pytest.raises(PreserveError):
        backend.verify_retention(leg, lease["lease_digest"], lease=dict(lease),
                                 lease_version=lease["lease_version"])


def test_the_fake_refuses_a_malformed_retain_until(tmp_path):
    """canary 도 계약을 지켜야 한다 — 잘못된 timestamp 를 받지 않는다."""
    store = _LockingStore(name=str(tmp_path))
    v = store.put("k", b"payload")
    for bad in ("zzzz", "2099-01-01", None, 12345):
        with pytest.raises((ValueError, TypeError)):
            store.lock("k", v, bad)
    store.lock("k", v, "2099-01-01T00:00:00Z")     # 정상은 된다


def test_a_governance_store_lock_mode_is_not_durable_even_when_consistent(tmp_path):
    """★ 40차 P0-1 — `store_lock_mode` 도 **값 자체**가 담보 mode 여야 한다.

    lease 와 provider version 이 서로 같기만 하면 통과하던 축을 store 쪽에서
    따로 본다: graph·lease·content 는 전부 Compliance 로 두고 **store 만**
    일관되게 Governance 로 만든다. 동등성은 맞으므로 membership 만이 잡는다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease, leg = res["retention"], PLANNED.leg_id

    store._mode[("store.json", lease["store_version_id"])] = "GOVERNANCE"
    bad = dict(lease, store_lock_mode="GOVERNANCE")

    with pytest.raises(PreserveError) as ex:
        backend.verify_retention(leg, lease["lease_digest"], lease=bad,
                                 lease_version=lease["lease_version"])
    assert "store" in str(ex.value), str(ex.value)


# ─────────────────────────────────────────────────────────────────────────────
# 40차 P0-1 — locator 가 "모양" 만 검증되고 실제 proof 인지 확인되지 않았다
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("axis", ["store_version", "graph_version"])
def test_a_nonexistent_locator_changes_nothing_before_refusal(tmp_path, axis):
    """★ 40차 P0-1 — nonempty 는 "존재한다" 가 아니다.

    39차 `_matches_lease()` 는 `store_version_id` 와 `object_versions` 가
    nonempty 인지만 봤다. 그 ID 가 provider 에 **실제로 있는지**, 그 version 의
    bytes·mode·기한이 candidate 를 지지하는지는 안 봤다.

    그래서 나머지를 전부 정상 candidate 와 같게 두고 locator 하나만 존재하지
    않는 값으로 바꾸면 앞단을 통과하고, `repair_lease_locks()` 가 pin·content
    를 WORM 으로 만든 **뒤** strict verifier 가 거부한다. 38차의
    validate-after-mutate 반례와 같은 불변식이다.

    **호출 전후로 provider version·lock·pin 집합·store bytes 가 같아야 한다.**
    """
    store = _LockingStore(name=f"{tmp_path}-{axis}")
    backend = _lockstore(tmp_path / axis, store)
    leg = "hc22p_v6_armA_b20"
    objs = sorted(backend.put_if_absent(b"g%d" % i)["digest"] for i in range(2))
    backend.pin(leg, objs)

    over = ({"store_version_id": "v-does-not-exist"} if axis == "store_version"
            else {"object_versions": {d: "v-does-not-exist" for d in objs}})
    fd = backend.put_if_absent(canonical_bytes(
        _lease_like(backend, leg, objs, **over)))["digest"]
    backend.pin(leg, [fd])

    before_v = _version_census(store)
    before_lock = dict(store._lock)
    before_pins = set(backend.pinned(leg))
    before_store = store.get("store.json")

    with pytest.raises(PreserveError):
        backend.retain(leg, objs, min_retention_days=MIN_RETENTION_DAYS)

    grew = {k: (before_v.get(k, 0), n) for k, n in _version_census(store).items()
            if n > before_v.get(k, 0)}
    assert not grew, f"{axis}: 거부 전에 version 을 늘렸다: {grew}"
    assert dict(store._lock) == before_lock, f"{axis}: 거부 전에 잠금이 바뀌었다"
    assert set(backend.pinned(leg)) == before_pins, f"{axis}: pin 집합이 변했다"
    assert store.get("store.json") == before_store, f"{axis}: store record 가 변했다"


def test_an_orphan_with_a_nonexistent_locator_is_not_adopted(tmp_path):
    """orphan 입양도 같은 관문을 지나야 한다 — 입양은 pin 을 만드는 mutation 이다."""
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    leg = "hc22p_v6_armA_b20"
    objs = sorted(backend.put_if_absent(b"h%d" % i)["digest"] for i in range(2))
    backend.pin(leg, objs)

    ad = backend.put_if_absent(canonical_bytes(_lease_like(
        backend, leg, objs,
        object_versions={d: "v-does-not-exist" for d in objs})))["digest"]

    assert backend._orphan_lease(leg, objs, MIN_RETENTION_DAYS) is None, (
        "존재하지 않는 locator 를 가진 record 를 입양 후보로 봤다")
    assert ad not in backend.pinned(leg), "입양하면서 pin 을 만들었다"


# ─────────────────────────────────────────────────────────────────────────────
# 40차 P1 — proof lookup 과 repair source 는 phase contract 가 다르다
# ─────────────────────────────────────────────────────────────────────────────

def test_repair_recovers_from_an_unlocked_exact_version(tmp_path, monkeypatch):
    """★ 40차 P1 — 39차는 셋을 `_version_for()` 하나로 접었다.

    `after_lease_pin` 창에서는 올바른 v1 이 **아직 안 잠겼다.** 그 위에
    wrong-bytes locked v2 가 생기면 `_version_for()` 는 잠긴 것만 보므로 v1 을
    못 찾고 `None` 을 돌린다. 수리는 version 없는 fallback 으로 hostile v2 를
    읽어 digest mismatch 로 끝난다 — 복구 가능한 v1 이 provider 에 그대로
    남아 있는데도.

    proof lookup 은 "잠긴 담보" 를 찾아야 하고, repair source 는 "아직 안
    잠긴 exact bytes" 도 후보로 삼아 **잠근 뒤** proof 로 승격해야 한다.
    중복이 아니라 phase contract 가 다르다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, "after_lease_pin")
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)

    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: lease 후보가 있다"
    key = backend._provider_key(leg, ld)
    assert backend.protected_version(key) is None, "전제: v1 이 아직 안 잠겼다"

    v2 = store.put(key, b"hostile-newer-unlocked-window")
    store.lock(key, v2, "2099-01-01T00:00:00Z")

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    monkeypatch.undo()

    assert out["ok"] and out["durable"] is True
    assert out["retention"]["lease_digest"] == ld, (
        "잠기지 않은 exact version 을 못 찾아 같은 lease 로 재개하지 못했다")


def test_a_same_bytes_governance_version_does_not_hide_the_compliance_proof(
        tmp_path):
    """★ 40차 P1 — `_locked_versions()` 가 Governance 도 후보로 삼았다.

    같은 바이트의 newer Governance v2 가 older Compliance v1 을 가릴 수 있다.
    proof lookup 은 **담보 mode** 만 후보로 삼아야 한다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease, leg = res["retention"], PLANNED.leg_id
    ld = lease["lease_digest"]
    key = backend._provider_key(leg, ld)
    v1 = lease["lease_version"]

    v2 = store.put(key, store.get(key, v1))        # **같은 바이트**
    store.lock(key, v2, lease["retain_until_utc"])
    store._mode[(key, v2)] = "GOVERNANCE"

    got = backend.recover_lease_version(leg, ld)
    assert got == v1, (
        f"같은 바이트의 Governance version 이 Compliance proof 를 가렸다: {got}")


# ─────────────────────────────────────────────────────────────────────────────
# 41차 P1 — read-only 라는 **이름**과 실제 동작이 아직 달랐다
# ─────────────────────────────────────────────────────────────────────────────

def test_the_local_backend_inspect_never_creates_or_extends_the_store(tmp_path):
    """★ 41차 P1 — base `CasBackend.inspect_store_id()` 가 `self.store_id` 였다.

    39차에 "검증은 수리하지 않는다" 며 inspect 를 갈랐는데, base 구현은
    한 줄짜리 위임이었다::

        def inspect_store_id(self): return self.store_id     # ← 만든다

    `store_id` 는 record 가 없으면 UUID 를 발급하고 CAS root 를 durable 하게
    굳힌다. object-lock backend 만 순수했고 **local backend 의 candidate
    validation 은 순수하지 않았다.** 이름이 predicate 보다 강한 그 형태다.

    store record 를 지운 상태에서 두 검증 경로를 부른다 — 어느 쪽도
    record·pin·lock 을 새로 만들면 안 된다.
    """
    backend = CasBackend(root=tmp_path / "cas", retention_days=MIN_RETENTION_DAYS)
    leg = "hc22p_v6_armA_b20"
    objs = sorted(backend.put_if_absent(b"g%d" % i)["digest"] for i in range(2))
    backend.pin(leg, objs)
    sid = backend.store_id                       # 여기서 한 번 만든다
    rec_path = Path(backend.root) / "store.json"
    assert rec_path.is_file() and sid
    rec_path.unlink()                            # 그리고 지운다

    lease = _lease_like(_StoreIdStub(sid, backend), leg, objs,
                        store_version_id="", store_lock_mode="",
                        object_versions={})
    assert backend.inspect_store_id() is None, (
        "record 가 없는데 store identity 를 만들어 냈다")
    assert not backend._matches_lease(leg, objs, MIN_RETENTION_DAYS, lease), (
        "store record 가 없는데 candidate 가 통과했다")
    assert not rec_path.exists(), "candidate 검증이 store record 를 만들었다"

    with pytest.raises(PreserveError):
        backend.verify_retention(leg, "0" * 64, lease=dict(lease))
    assert not rec_path.exists(), (
        "strict verifier 가 불일치를 설명하다가 store record 를 만들었다")


class _StoreIdStub:
    """`_lease_like()` 가 읽는 세 속성만 흉내낸다 (backend 를 만들지 않는다)."""

    def __init__(self, sid, backend):
        self.store_id = sid
        self.store_version_id = ""
        self.store_lock_mode = ""
        self.uri = backend.uri
        self._backend = backend

    def probe_enforcement(self):
        return self._backend.probe_enforcement()


# ─────────────────────────────────────────────────────────────────────────────
# 41차 P1 — repair **source** 를 찾은 것과 repair **target** 을 찾은 것은 다르다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_same_bytes_governance_head_does_not_block_repair(tmp_path, monkeypatch):
    """★ 41차 P1 — 40차는 두 성분을 **따로** 시험하고 결합을 안 봤다.

    40차가 닫은 둘::

        (a) unlocked v1 + newer **wrong-bytes** locked v2   → repair source 로 해결
        (b) 이미 Compliance 인 v1 + newer same-bytes Governance v2 → proof lookup

    결합하면 다시 열린다::

        after_lease_pin crash
        v1 = correct bytes, **unlocked**
        v2 = same correct bytes, **Governance**, newer

    `_version_for()` 에는 담보 proof 가 없고, 수리는 `_existing_version()` 으로
    **최신 same-bytes** 인 v2 를 target 으로 골라 잠근다. 이미 Governance 인
    version 은 Compliance 로 승격되지 않으므로 수리가 영영 실패하고, 수리 가능한
    unlocked v1 은 provider 에 그대로 남는다.

    repair target 은 **담보로 만들 수 있는** version 이어야 한다 (안 잠겼거나
    이미 담보) — 없으면 새 version 을 만든다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 27, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, "after_lease_pin")
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)

    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: lease 후보가 있다"
    key = backend._provider_key(leg, ld)
    assert backend.protected_version(key) is None, "전제: v1 이 아직 안 잠겼다"

    v1 = store.versions(key)[0]
    v2 = store.put(key, store.get(key, v1))            # **같은 바이트**
    store.lock(key, v2, "2099-01-01T00:00:00Z")
    store._mode[(key, v2)] = "GOVERNANCE"               # 승격 불가능한 head

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    monkeypatch.undo()

    assert out["ok"] and out["durable"] is True
    assert out["retention"]["lease_digest"] == ld, (
        "같은 바이트의 Governance head 가 수리 target 을 가로막았다")
    proof = out["retention"]["lease_version"]
    st = store.describe_object(key, proof)
    assert st and st["mode"] == "COMPLIANCE", (
        f"수리가 담보되지 않은 version 을 proof 로 돌려줬다: {st}")


def test_a_lock_that_does_not_produce_a_durable_version_fails_closed(tmp_path):
    """★ 41차 P1 — 수리가 고른 target ID 를 **proof 로 믿지 않는다.**

    target selector 는 "담보로 만들 수 있는가" 를 묻고, proof selector 는
    "지금 담보인가" 를 묻는다. 둘은 다른 질문이므로, `lock()` 이 끝났다는 것이
    proof 가 생겼다는 뜻은 아니다 — provider 가 우회 가능한 mode 로 잠그면
    (실물에서 bucket 기본 설정이 GOVERNANCE 인 경우가 그렇다) 잠금은 성공하고
    담보는 없다.

    40차는 `lock()` 뒤 그 version ID 를 그대로 돌려줬다. 이제 proof selector 를
    다시 돌리고, 없으면 **거부**한다.
    """
    class _GovernanceOnly(_LockingStore):
        def lock(self, key, version, until):
            super().lock(key, version, until)
            self._mode[(key, version)] = "GOVERNANCE"

    store = _GovernanceOnly(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    dg = backend.put_if_absent(b"payload")["digest"]
    until = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")

    with pytest.raises(PreserveError) as ei:
        backend.lock_content_object(dg, until)
    assert "담보" in str(ei.value), str(ei.value)


# ─────────────────────────────────────────────────────────────────────────────
# 41차 P1 — 검증한 exact locator·bytes 가 phase 경계에서 버려진다
# ─────────────────────────────────────────────────────────────────────────────

def _crash_at(tmp_path, monkeypatch, phase):
    """`retain()` 의 그 창에서 죽인 상태를 만들고 (store, backend, index, clock).

    시계를 monkeypatch 한 채로 돌려준다 — 호출자가 `monkeypatch.undo()` 뒤
    다시 붙여야 재개 경로가 같은 시계를 본다 (기존 창 시험들과 같은 방식).
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 28, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, phase)
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)
    return store, backend, index


def test_an_orphan_lease_is_adopted_by_its_exact_version(tmp_path, monkeypatch):
    """★ 41차 P1 — orphan 검증이 exact version 을 읽고 **버린다.**

    `_orphan_lease()` 는 `(key, version)` 을 돌며 **그 exact version bytes** 로
    후보를 검증한다. 그런데 돌려주는 것은 digest 문자열 하나다. 호출자는
    `pin(leg, [digest])` 를 부르고, `pin()` 은 `read_back(digest)` 로 **다시**
    namespace 를 읽는다 — 그것은 최신 담보 version 을 고른다.

        after_lease_put:
          objects/<D> v1 = 올바른 orphan lease bytes, unlocked
          objects/<D> v2 = wrong bytes, Compliance locked, newer

        `_orphan_lease()`  → exact v1 을 읽고 유효 판정 · version 은 버리고 D 반환
        `_existing_lease()`→ pin(D)
        `pin()`            → read_back(D) → protected v2 → digest mismatch

    올바른 v1 이 provider 에 그대로 있는데 hostile head 하나 때문에 재개가
    막힌다. 검증 결과가 phase 를 넘어가면 digest/bool 로는 부족하다 —
    **검증한 바로 그 version 과 bytes** 를 들고 가야 한다.
    """
    store, backend, index = _crash_at(tmp_path, monkeypatch, "after_lease_put")
    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: orphan lease content 가 있다"
    assert ld not in backend.pinned(leg), "전제: 아직 pin 이 없다 (orphan)"

    key = backend._provider_obj_key(ld)
    v2 = store.put(key, b"hostile-newer-locked-content")
    store.lock(key, v2, "2099-01-01T00:00:00Z")

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    monkeypatch.undo()

    assert out["ok"] and out["durable"] is True
    assert out["retention"]["lease_digest"] == ld, (
        "hostile locked head 때문에 온전한 orphan 을 입양하지 못했다")


def test_content_repair_uses_the_bytes_it_already_verified(tmp_path, monkeypatch):
    """★ 41차 P1 — 수리가 **이미 검증한 pin bytes 를 버리고** `has()` 를 믿는다.

    `repair_lease_locks()` 는 pin 의 exact repair source 에서 올바른 lease
    bytes 를 읽어 `data` 에 담는다. 그런데 content 존재 여부는 `has()` 에
    묻는다 — `has()` 는 protected version 을 **읽을 수 있으면** True 이고
    바이트 hash 를 안 본다.

        after_lease_pin:
          pins/<leg>/<D>      = 올바른 lease bytes
          objects/<D> 의 올바른 unlocked v1 = **삭제**
          objects/<D> v2      = wrong bytes, Compliance locked

        has(D)                → v2 를 읽을 수 있으므로 True → 복원 생략
        lock_content_object() → namespace 를 다시 읽다가 v2 hash mismatch

    `has()` 만 strict 하게 고쳐도 끝나지 않는다: 뒤이어 부를
    `put_if_absent()` 도 version 없는 protected read 로 v2 를 보고 collision 을
    낸다. 검증된 bytes 를 그대로 들고 가서 **새 exact version** 을 만들어야 한다.
    """
    store, backend, index = _crash_at(tmp_path, monkeypatch, "after_lease_pin")
    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: lease 후보가 있다"

    key = backend._provider_obj_key(ld)
    v1 = store.versions(key)[0]
    good = store.get(key, v1)                   # 올바른 content bytes
    # ★ version 없는 delete 는 marker 만 얹고 v1 을 남긴다 (실물 S3 의미).
    #   이 창의 v1 은 아직 안 잠겼으므로 **exact version delete** 가 통한다.
    store.delete(key, version=v1)
    v2 = store.put(key, b"hostile-locked-content-head")
    store.lock(key, v2, "2099-01-01T00:00:00Z")
    assert hashlib.sha256(good).hexdigest() == ld, "전제: pin 바이트가 정본이다"

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    monkeypatch.undo()

    assert out["ok"] and out["durable"] is True
    assert out["retention"]["lease_digest"] == ld
    cv = out["retention"]["lease_content_version"]
    assert store.get(key, cv) == good, (
        "content proof 가 검증된 바이트를 담고 있지 않다")


def test_locking_an_already_durable_object_adds_no_version(tmp_path):
    """★ 41차 P1 — `_lock_to_proof()` 가 **existing proof 를 먼저 안 찾는다.**

    지금 순서는 무조건 `repair target → lock → proof 재탐색` 이다. 그래서
    충분한 Compliance proof v1 이 이미 있는데 그 위에 exact same-bytes
    **unlocked** v2 가 생기면, `_repair_target()` 이 최신 v2 를 골라 새로
    WORM-lock 한다. v1 만으로 이미 담보였고 아무 수리도 필요 없었다 —
    이 상태를 반복하면 되돌릴 수 없는 version 이 계속 쌓인다.

    올바른 순서는 **proof lookup 이 먼저**다 (요청 기한을 덮는가).
    """
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    dg = backend.put_if_absent(b"already-durable")["digest"]
    until = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    v1 = backend.lock_content_object(dg, until)

    key = backend._provider_obj_key(dg)
    store.put(key, store.get(key, v1))          # 같은 바이트의 unlocked head

    before_v = _version_census(store)
    before_lock = dict(store._lock)
    got = backend.lock_content_object(dg, until)

    assert got == v1, f"이미 담보인 proof 대신 다른 version 을 돌려줬다: {got}"
    assert _version_census(store) == before_v, (
        "이미 담보인데 version 이 늘었다 (되돌릴 수 없는 WORM 잔여)")
    assert dict(store._lock) == before_lock, "이미 담보인데 새 잠금이 생겼다"


def test_an_orphan_locator_never_carries_bytes_from_another_key(tmp_path):
    """★ 42차 P1 — locator 는 **자기 안에서 일관**해야 한다.

    `_orphan_lease()` 는 이제 `(key, version, digest, bytes)` 를 다음 phase 로
    넘긴다. 그 bytes 가 key 가 말하는 digest 와 다르면, 입양이 그 바이트를
    `pins/<leg>/<그 digest>` 에 넣고 뒤이은 `read_pinned()` 가 digest mismatch
    로 죽는다 — 검증이 통과한 뒤에 깨지는 형태다.

    유효한 lease record 의 바이트를 **다른 digest 의 key** 에 올려 둔다.
    locator 를 만들기 전에 걸러야 한다.
    """
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    leg = "hc22p_v6_armA_b20"
    objs = sorted(backend.put_if_absent(b"g%d" % i)["digest"] for i in range(2))
    backend.pin(leg, objs)
    until = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    backend.store_id
    backend.ensure_store_lock(until)
    versions = backend.lock_objects(leg, objs, until)
    rec = {
        "schema": P_RETENTION_SCHEMA, "leg_id": leg, "objects": objs,
        "min_retention_days": MIN_RETENTION_DAYS, "retain_until_utc": until,
        "store_id": backend.store_id,
        "store_version_id": backend.store_version_id,
        "store_lock_mode": backend.store_lock_mode,
        "backend_uri": backend.uri,
        "enforcement": backend.probe_enforcement(),
        "lock_mode": "COMPLIANCE",
        "object_versions": dict(versions),
        "pin_set_digest": pin_set_digest(leg, objs),
    }
    payload = canonical_bytes(rec)
    assert backend._matches_lease(leg, objs, MIN_RETENTION_DAYS, rec), (
        "전제: 이 record 자체는 유효한 lease 다")

    wrong = hashlib.sha256(b"a-different-object-entirely").hexdigest()
    store.put(backend._provider_obj_key(wrong), payload)   # key ≠ bytes

    got = backend._orphan_lease(leg, objs, MIN_RETENTION_DAYS)
    assert got is None, (
        f"key 가 말하는 digest 와 다른 바이트로 locator 를 만들었다: {got}")
    assert wrong not in backend.pinned(leg), "그 위조 위에 pin 을 만들었다"


def test_a_short_horizon_proof_is_not_accepted_and_gets_extended(tmp_path):
    """★ 42차 P1 — proof lookup 은 **요청 기한을 덮는가**를 물어야 한다.

    `_lock_to_proof()` 가 proof 를 먼저 찾도록 고쳤는데, 그 lookup 이 "지금
    잠겨 있다" 만 보면 **기한이 짧은** version 을 proof 로 받아들이고 요청한
    기한까지 연장하지 않는다. 그러면 lease 가 신고한 기한보다 짧은 담보로
    `durable=True` 가 된다.

    짧은 기한으로 먼저 잠근 뒤 더 긴 기한을 요청한다.
    """
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    dg = backend.put_if_absent(b"short-then-long")["digest"]
    now = dt.datetime.now(dt.timezone.utc)
    short = (now + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    long = (now + dt.timedelta(days=MIN_RETENTION_DAYS * 3)).strftime("%Y-%m-%dT%H:%M:%SZ")

    v1 = backend.lock_content_object(dg, short)
    got = backend.lock_content_object(dg, long)
    st = store.describe_object(backend._provider_obj_key(dg), got)
    assert st and st["retain_until"] >= long, (
        f"기한이 짧은 version 을 proof 로 받아들였다: {st} (요청 {long})")
    assert got == v1, "같은 version 을 연장하면 되는데 새 version 을 만들었다"


# ─────────────────────────────────────────────────────────────────────────────
# 43차 P1 — 수리가 찾은 proof 를 버리고 기한 없는 live search 를 다시 한다
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("where", ["pin", "content"])
def test_the_repaired_proof_is_handed_to_verify_not_researched(tmp_path, where):
    """★ 43차 P1 — `repair_lease_locks()` 가 wrapper 가 돌려준 proof ID 둘을
    버리고 `None` 을 반환한다. 그 뒤 `_existing_lease()` 는 **기한 인자 없는**
    `recover_lease_version()` · `recover_content_version()` 으로 다시 찾는다.

        v1: exact same bytes · Compliance · lease 기한을 **충분히 덮는다**
        v2: exact same bytes · Compliance · 아직 유효하지만 **lease 기한보다 짧다** · newer

        repair : v1 을 정확히 찾는다 → ID 를 버린다
        recover: 기한을 안 물으므로 최신인 v2 를 고른다
        verify : v2 가 기한을 못 덮어 실패

    온전한 v1 이 그대로 있는데 재개가 막힌다. 42차 시험은 wrapper 반환만
    따로 봤으므로 이 결합을 못 봤다.
    """
    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"
    res = run_transaction(PLANNED, run, backend, index, _hooks())
    lease, leg = res["retention"], PLANNED.leg_id
    ld = lease["lease_digest"]

    key = (backend._provider_key(leg, ld) if where == "pin"
           else backend._provider_obj_key(ld))
    v1 = (lease["lease_version"] if where == "pin"
          else lease["lease_content_version"])
    st1 = store.describe_object(key, v1)
    assert st1 and st1["mode"] == "COMPLIANCE", "전제: v1 이 담보다"
    assert st1["retain_until"] >= lease["retain_until_utc"], (
        "전제: v1 이 lease 기한을 덮는다")

    # **같은 바이트**의 더 최신 Compliance version — 다만 기한이 짧다
    short = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS - 1)
             ).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert short < lease["retain_until_utc"], "전제: 더 짧은 기한이다"
    v2 = store.put(key, store.get(key, v1))
    store.lock(key, v2, short)

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    proof = fresh.repair_lease_locks(leg, ld, lease["retain_until_utc"])
    got = proof.lease_version if where == "pin" else proof.content_version
    assert got == v1, (
        f"기한을 덮는 v1 이 있는데 짧은 v2 를 proof 로 골랐다: {got}")
    assert proof.until == lease["retain_until_utc"], "proof 가 기한을 안 든다"
    # 그리고 **기한 없는** live search 는 실제로 v2 를 고른다 — 이 시험이
    # 보는 것이 "찾은 것을 버리고 다시 찾으면 달라진다" 임을 못 박는다.
    live = (fresh.recover_lease_version(leg, ld) if where == "pin"
            else fresh.recover_content_version(ld))
    assert live == v2, f"전제: 기한 없는 재탐색은 v2 를 고른다 (got {live})"


# ─────────────────────────────────────────────────────────────────────────────
# 43차 P2 — 되돌릴 수 없는 lock 보다 검증이 먼저다
# ─────────────────────────────────────────────────────────────────────────────

def test_wrong_bytes_are_never_locked(tmp_path):
    """★ 43차 — `_lock_to_proof()` 의 새-version 경로는 `put` 한 뒤 **곧바로**
    `lock` 한다. caller 가 준 bytes 가 digest 와 다르면 되돌릴 수 없는 WORM
    version 이 먼저 생기고 그 다음에야 proof 재탐색이 실패한다.

    lock 은 되돌릴 수 없다 — 검증이 먼저다.
    """
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    dg = backend.put_if_absent(b"the-real-payload")["digest"]
    until = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    key = backend._provider_obj_key(dg)
    store.delete(key, version=store.versions(key)[0])      # exact bytes 를 없앤다

    before_lock = dict(store._lock)
    before_v = _version_census(store)
    with pytest.raises(PreserveError):
        backend.lock_content_object(dg, until, data=b"not-the-payload")
    assert dict(store._lock) == before_lock, (
        "digest 와 다른 바이트를 WORM 으로 잠갔다")
    # ★ 43차 — 잠그지 않는 것만으로는 부족하다. digest 와 다른 바이트를 CAS
    #   namespace 에 **올리는 것 자체**가 잔여다 (읽기 경로가 그 head 를
    #   protected 로 오인할 수 있고, 그것이 42차 hostile head 반례의 재료다).
    assert _version_census(store) == before_v, (
        "digest 와 다른 바이트로 version 을 만들었다")


def test_a_provider_that_returns_the_wrong_version_locks_nothing(tmp_path):
    """★ 43차 — provider 가 `put` 에서 **다른 version ID** 를 돌려주면?

    adapter 계약 위반이지만, 그 경우 우리는 남의 version 을 잠근다. 되돌릴 수
    없는 연산이므로 계약을 믿지 말고 **그 exact version 을 읽어 확인한 뒤**
    잠근다.
    """
    class _LyingPut(_LockingStore):
        lie = False

        def put(self, key, data):
            v = super().put(key, data)
            if self.lie and key.startswith("objects/"):
                other = super().put(key, b"someone-elses-bytes")
                return other                      # 계약 위반: 다른 version 을 신고
            return v

    store = _LyingPut(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    dg = backend.put_if_absent(b"honest-payload")["digest"]
    until = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    key = backend._provider_obj_key(dg)
    data = store.get(key, store.versions(key)[0])
    store.delete(key, version=store.versions(key)[0])

    store.lie = True
    before_lock = dict(store._lock)
    with pytest.raises(PreserveError):
        backend.lock_content_object(dg, until, data=data)
    assert dict(store._lock) == before_lock, (
        "provider 가 신고한 version 을 확인 없이 잠갔다")


def test_a_pre_journal_finalize_uses_the_repaired_pin_proof(tmp_path, monkeypatch):
    """★ 43차 P1 — journal **이전** 창이 handoff 가 실제로 쓰이는 자리다.

    journal 이 생긴 뒤에는 runtime verifier 가 봉인된 exact ID 를 쓰므로
    (그 배선은 맞다) 이 축이 안 보인다. `after_pin_lock` 창은 pin 이 긴 기한
    으로 잠겨 있고 content 는 아직 안 잠긴 상태이며 journal 이 없다.

        pin v1: exact bytes · Compliance · lease 기한을 덮는다
        pin v2: exact bytes · Compliance · **더 짧은** 기한 · newer

    수리는 v1 을 정확히 찾는다. 그 ID 를 버리고 기한 없는 `recover_*()` 로
    다시 찾으면 v2 가 나오고 검증이 실패한다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 29, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, "after_pin_lock")
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)

    leg = PLANNED.leg_id
    ld = _crashed_lease_digest(store, backend, leg)
    assert ld, "전제: lease 후보가 있다"
    key = backend._provider_key(leg, ld)
    v1 = backend.protected_version(key)
    assert v1, "전제: pin 이 이미 잠겨 있다 (after_pin_lock)"
    st1 = store.describe_object(key, v1)
    want = st1["retain_until"]

    short = (_Clock.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS - 1)
             ).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert short < want, "전제: 더 짧은 기한이다"
    v2 = store.put(key, store.get(key, v1))
    store.lock(key, v2, short)

    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    monkeypatch.undo()

    assert out["ok"] and out["durable"] is True
    assert out["retention"]["lease_version"] == v1, (
        "수리가 찾은 긴-기한 proof 대신 짧은 v2 를 봉인했다: "
        f"{out['retention']['lease_version']}")


def test_the_journal_seals_the_content_proof_the_repair_produced(tmp_path,
                                                                 monkeypatch):
    """★ 44차 P2 — 43차 증거는 content exact-ID 가 **journal 까지** 가는지를
    직접 보지 않았다 (pin 축만 end-to-end 였다).

    `after_pin_lock` 창에서 재개하면 수리가 content 를 잠그고 그 exact ID 가
    journal 에 봉인돼야 한다. 그리고 journal 이 적은 ID 로 provider 를 조회한
    것이 실제 담보 상태여야 한다.
    """
    import tools.preserve as P

    run = _make_run(tmp_path)
    store = _LockingStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    index = tmp_path / "index"

    base = dt.datetime(2026, 8, 30, 12, 0, 0, tzinfo=dt.timezone.utc)
    ticks = iter(range(0, 100000, 37))

    class _Clock(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return base + dt.timedelta(seconds=next(ticks))

    monkeypatch.setattr(P.dt, "datetime", _Clock)
    _phase_kill(monkeypatch, "after_pin_lock")
    with pytest.raises(RuntimeError):
        run_transaction(PLANNED, run, backend, index, _hooks())
    monkeypatch.undo()
    monkeypatch.setattr(P.dt, "datetime", _Clock)

    leg = PLANNED.leg_id
    fresh = _lockstore(tmp_path, _LockingStore(name=store.name))
    out = finalize_only(leg, fresh, index)
    monkeypatch.undo()
    assert out["ok"] and out["durable"] is True

    ld = out["retention"]["lease_digest"]
    cv = out["retention"]["lease_content_version"]
    assert cv, "content proof 가 비었다"

    # journal 이 그 exact ID 를 봉인했는가
    jrn = load_canonical(_reg_path(index, leg).read_bytes())
    assert jrn.get("lease_content_version") == cv, (
        f"journal 의 content proof 가 수리 결과와 다르다: "
        f"{jrn.get('lease_content_version')} ≠ {cv}")
    assert jrn.get("lease_version") == out["retention"]["lease_version"]

    # 그 ID 가 실제로 담보 상태인가 (journal 이 적은 것을 provider 에 묻는다)
    st = store.describe_object(fresh._provider_obj_key(ld), cv)
    assert st and st["mode"] == "COMPLIANCE", f"봉인 ID 가 담보가 아니다: {st}"
    assert st["retain_until"] >= out["retention"]["retain_until_utc"]


@pytest.mark.parametrize("bogus", [None, "", 0])
def test_a_falsy_version_id_from_put_is_refused(tmp_path, bogus):
    """★ 45차 — provider 가 falsy·비문자열 VersionId 를 주면 read-back 이
    **exact version 이 아니라 head** 를 읽는다.

        put(correct v1) → adapter 결함으로 None 반환
        get(key, None)  → 지금의 head v1 을 읽어 digest 통과
        다른 writer 가 wrong-bytes v2 를 head 로 올린다
        lock(key, None) → **현재 head(v2)** 에 retention 이 걸린다

    44차 회귀는 **다른 nonempty ID** 만 봤다. exact version ID 가 아니면
    read-back 앞에서 거부한다.
    """
    class _FalsyPut(_LockingStore):
        lie = False

        def put(self, key, data):
            v = super().put(key, data)
            return bogus if (self.lie and key.startswith("objects/")) else v

    store = _FalsyPut(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    dg = backend.put_if_absent(b"honest-payload")["digest"]
    until = (dt.datetime.now(dt.timezone.utc)
             + dt.timedelta(days=MIN_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    key = backend._provider_obj_key(dg)
    data = store.get(key, store.versions(key)[0])
    store.delete(key, version=store.versions(key)[0])

    store.lie = True
    before_lock = dict(store._lock)
    with pytest.raises(PreserveError) as ei:
        backend.lock_content_object(dg, until, data=data)
    assert "version" in str(ei.value), str(ei.value)
    assert dict(store._lock) == before_lock, "falsy version ID 로 잠갔다"


# ─────────────────────────────────────────────────────────────────────────────
# 46차 P0-8 — provider 가 주는 version 후보는 **전부** 검증한다
#
# 45차까지 `put()` 이 돌려준 VersionId 만 "비어 있지 않은 문자열" 로 봤다.
# 그런데 담보 version 은 `versions(key)` 열거에서도 온다 (`protected_version`
# · `_locked_versions` · store.json 정본 선택). 거기서 falsy·비문자열 후보가
# 들어오면 `lock(key, "", until)` 을 부르고, 그 빈 문자열이 lease proof·
# receipt locator 로 그대로 굳는다 — "정확히 이 version 을 담보했다" 가
# 아무것도 가리키지 않는 값이 된다.
# ─────────────────────────────────────────────────────────────────────────────

class _WeakVersionStore(_LockingStore):
    """실물 SDK 가 그럴 수 있듯 열거에 falsy·비문자열 후보를 섞는다."""

    JUNK = ("", None, 0, b"v1", ["v1"])

    def versions(self, key: str) -> list:
        real = super().versions(key)
        return list(self.JUNK) + real

    def describe_object(self, key: str, version=None):
        # junk 후보도 "잠긴 것처럼" 보이게 만든다 — 검증이 없으면 그대로 통과한다
        if version in self.JUNK or (isinstance(version, (bytes, list))):
            return {"mode": "COMPLIANCE",
                    "retain_until": "2099-01-01T00:00:00Z"}
        return super().describe_object(key, version)


def test_every_enumerated_version_candidate_must_be_a_nonempty_string(tmp_path):
    """★ 46차 P0-8 — 열거 후보를 검증하지 않으면 빈 locator 를 담보라고 부른다."""
    store = _WeakVersionStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    store.put("objects/x", b"payload")

    with pytest.raises(PreserveError) as ei:
        backend.protected_version("objects/x")
    assert "version" in str(ei.value), str(ei.value)

    with pytest.raises(PreserveError):
        backend._locked_versions("objects/x")


def test_a_falsy_version_never_reaches_lock(tmp_path):
    """★ 46차 P0-8 — 거부는 `lock()` **앞**에서 일어나야 한다.

    뒤에서 걸러도 이미 실물에 WORM 잠금이 걸린 뒤다 (되돌릴 수 없다).
    """
    store = _WeakVersionStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    store.put("store.json", b"{}")

    locked: list = []
    real_lock = store.lock

    def _spy(key, version, until, **kw):
        locked.append((key, version))
        return real_lock(key, version, until, **kw)

    store.lock = _spy
    with pytest.raises(PreserveError):
        backend.ensure_store_lock("2099-01-01T00:00:00Z")
    assert not locked, f"거부 전에 이미 잠갔다: {locked}"


# ─────────────────────────────────────────────────────────────────────────────
# 46차 P0-11 — planned leg index 를 **실행 전** gate 로 (묶음 9 의 남은 절반)
#
# 계약 §13.4 가 스스로 신고하던 구멍이다: 보존 원장의 coverage 기준이 **커밋된
# 투영**이라, 새 다리를 돌려도 투영을 만들기 전에는 아무 회귀도 깨지지 않는다.
# 2026-08-20 에 warm 7다리를 그렇게 돌렸고 보존 없이 잃었다.
# ─────────────────────────────────────────────────────────────────────────────

import textwrap

_PLAN_LEDGER = textwrap.dedent('''\
    schema_version: 4
    cohorts:
      - cohort_id: gA
        dir: docs/22p_gap/coh
        status: active
        legs: ["ran"]
        prospective_legs: ["L"]
        cross_leg_comparison: not_applicable_single_leg
        pin:
          schema_version: 3
          compute_sha256: "aaaaaaaaaaaaaaaa"
          row_projection_py_sha256: "bbbbbbbbbbbbbbbb"
          src_scoring_py_sha256: "cccccccccccccccc"
          analysis_spec_sha256: "dddddddddddddddd"
      - cohort_id: gF
        dir: docs/22p_gap/frz
        status: frozen
        legs: ["Z"]
        cross_leg_comparison: allowed_within_cohort
        pin:
          schema_version: 3
          compute_sha256: "aaaaaaaaaaaaaaaa"
          row_projection_py_sha256: "bbbbbbbbbbbbbbbb"
          src_scoring_py_sha256: "cccccccccccccccc"
          analysis_spec_sha256: "dddddddddddddddd"
    planned:
      - leg_id: L
        cohort_id: gA
        status: planned
        authorization_kind: prospective
        authorized_source_digest: "0123456789abcdef"
        run_spec_digest: "aa11bb22cc33dd44ee55ff66aa77bb88cc99dd00ee11ff22aa33bb44cc55dd66"
        recorded_on: "2026-08-28"
        근거: "시험용"
      - leg_id: ran
        cohort_id: gA
        status: executed
        authorization_kind: retrospective
        authorized_source_digest: "aabbccddeeff0011"
        run_spec_digest: "retrospective:no-preauthorization"
        recorded_on: "2026-08-20"
        근거: "시험용 — active cohort 의 끝난 다리"
      - leg_id: Z
        cohort_id: gF
        status: executed
        authorization_kind: retrospective
        authorized_source_digest: "fedcba9876543210"
        run_spec_digest: "retrospective:no-preauthorization"
        recorded_on: "2026-08-20"
        근거: "시험용 — 소급 기록"
    legs:
      - leg_id: ran
        preservation_status: full_bundle
        evidence:
          leg_source_digest: "aabbccddeeff0011"
          cohorts: ["gA"]
      - leg_id: Z
        preservation_status: full_bundle
        evidence:
          leg_source_digest: "fedcba9876543210"
          cohorts: ["gF"]
    ''')


def _with_run_spec(body: str) -> str:
    """★ 48차 P0-5 — prospective 계획 항목에 `run_spec:` 을 채운다.

    계약이 "승인은 이름이 아니라 **무엇을 실행할지**" 로 바뀌었으므로 fixture 도
    그것을 담아야 한다. `run_spec` 없이도 통과하던 fixture 가 바로 47차의
    구멍이었다 — 계획이 불투명 64hex 하나만 들고 있으면 gate 는 "그 digest 를
    내는 dict 이면 무엇이든 통과" 가 된다.
    """
    import yaml
    from tools.preserve import run_spec_digest

    doc = yaml.safe_load(body)
    for e in doc.get("planned") or []:
        if e.get("authorization_kind") != "prospective":
            continue
        e.setdefault("run_spec", {"leg_id": e["leg_id"], "mode": "fit",
                                  "objective": "pocv_dvdq", "n_restarts": 3,
                                  "reference": "grid"})
        e["run_spec_digest"] = run_spec_digest(e["run_spec"])
    return yaml.safe_dump(doc, allow_unicode=True, sort_keys=False)


def _plan_ledger(tmp_path, body=None) -> pathlib.Path:
    p = tmp_path / "LEG_PRESERVATION.yaml"
    p.write_text(_with_run_spec(body if body is not None else _PLAN_LEDGER),
                 encoding="utf-8")
    return p


def test_an_unplanned_leg_cannot_start_an_expensive_run(tmp_path):
    """★ 46차 P0-11 — 계획에 없는 다리는 **실행 전에** 막힌다."""
    from tools.preserve import assert_planned_leg

    led = _plan_ledger(tmp_path)
    assert assert_planned_leg("L", "0123456789abcdef", ledger=led)
    with pytest.raises(PreserveError) as ei:
        assert_planned_leg("ghost", "0123456789abcdef", ledger=led)
    assert "계획" in str(ei.value) or "planned" in str(ei.value), str(ei.value)


def test_the_gate_binds_the_plan_to_the_code_identity(tmp_path):
    """★ 46차 P0-11 — 승인 뒤 RUN_SCOPE 가 바뀌면 승인이 만료된다.

    "이 다리를 돌려도 좋다" 는 **어떤 코드로** 돌려도 좋다는 뜻이 아니다.
    승인 시점의 `source_digest` 와 다르면 사람이 다시 승인해야 한다.
    """
    from tools.preserve import assert_planned_leg

    led = _plan_ledger(tmp_path)
    with pytest.raises(PreserveError) as ei:
        assert_planned_leg("L", "ffffffffffffffff", ledger=led)
    assert "source_digest" in str(ei.value), str(ei.value)


def test_an_already_executed_leg_is_not_a_standing_authorization(tmp_path):
    """★ 46차 P0-11 — `executed` 기록은 다음 실행의 승인이 아니다."""
    from tools.preserve import assert_planned_leg

    led = _plan_ledger(tmp_path)
    # ★ 47차 — **active** cohort 의 executed leg 를 쓴다. 46차는 frozen cohort
    #   의 leg 였고, status 검사를 지워도 frozen guard 가 대신 거부해서 변이가
    #   "물었다" 로 계상됐다 (리뷰어 지적, 실측했다).
    with pytest.raises(PreserveError) as ei:
        assert_planned_leg("ran", "aabbccddeeff0011", ledger=led)
    assert "executed" in str(ei.value) or "이미 실행" in str(ei.value), str(ei.value)


def test_the_plan_must_name_an_active_cohort(tmp_path):
    """★ 46차 P0-11 — frozen cohort 로는 새 다리를 돌릴 수 없다."""
    from tools.preserve import assert_planned_leg

    # gF 로 옮기면서 그 cohort 의 계획 roster 에도 넣는다 — 그래야 이 시험이
    # **frozen 이라서** 거부되는지 (roster 누락이 아니라) 확인된다.
    body = (_PLAN_LEDGER
            .replace("    cohort_id: gA\n", "    cohort_id: gF\n", 1)
            .replace('    legs: ["Z"]\n',
                     '    legs: ["Z"]\n    prospective_legs: ["L"]\n', 1))
    led = _plan_ledger(tmp_path, body)
    with pytest.raises(PreserveError) as ei:
        assert_planned_leg("L", "0123456789abcdef", ledger=led)
    assert "frozen" in str(ei.value) or "active" in str(ei.value), str(ei.value)


def test_every_executed_leg_must_appear_in_the_planned_index(tmp_path):
    """★ 46차 P0-11 — 반대 방향. 실행 기록이 계획 index 를 **덮어야** 한다.

    이것이 없으면 index 는 장식이다: 계획에 없이 돌린 다리가 나중에 `legs:`
    에만 나타나도 아무 검사도 깨지지 않는다 (§13.4 가 신고하던 그 구멍).
    """
    from tools.preserve import assert_planned_index_consistent

    led = _plan_ledger(tmp_path)
    assert assert_planned_index_consistent(ledger=led)

    body = _PLAN_LEDGER + "  - leg_id: 유령\n    preservation_status: full_bundle\n"
    other = tmp_path / "b"
    other.mkdir()
    with pytest.raises(PreserveError) as ei:
        assert_planned_index_consistent(ledger=_plan_ledger(other, body))
    assert "유령" in str(ei.value), str(ei.value)


@pytest.mark.parametrize("break_it", [
    ("    status: planned\n", "    status: 계획중\n"),                 # enum 밖
    ('    authorized_source_digest: "0123456789abcdef"\n', ""),         # key 누락
    ('    recorded_on: "2026-08-28"\n',
     '    recorded_on: "2026-08-28"\n    extra: x\n'),                 # 남는 key
])
def test_the_planned_index_has_a_closed_schema(tmp_path, break_it):
    """★ 46차 P0-11 — 계획 항목도 닫힌 schema 다 (빠진 key 의 `None` 금지)."""
    from tools.preserve import assert_planned_index_consistent

    old, new = break_it
    body = _PLAN_LEDGER.replace(old, new, 1)
    assert body != _PLAN_LEDGER, "전제: 변형 지점을 찾았다"
    with pytest.raises(PreserveError):
        assert_planned_index_consistent(ledger=_plan_ledger(tmp_path, body))


def test_the_planned_index_is_bound_to_the_real_execution_record(tmp_path):
    """★ 46차 P0-11 — 계획 항목은 **실물 원장 기록**을 가리켜야 한다.

    이것이 없으면 `planned:` 는 자기 자신만 참조하는 목록이다 — 아무 digest 나
    적어도 내부적으로 일관되고, "실행 전 gate" 가 아니라 장식이 된다.
    """
    from tools.preserve import assert_planned_index_consistent

    assert assert_planned_index_consistent(ledger=_plan_ledger(tmp_path))

    liar = _PLAN_LEDGER.replace('  leg_source_digest: "fedcba9876543210"\n',
                                '  leg_source_digest: "0000000000000000"\n')
    assert liar != _PLAN_LEDGER, "전제"
    d2 = tmp_path / "d2"
    d2.mkdir()
    with pytest.raises(PreserveError) as ei:
        assert_planned_index_consistent(ledger=_plan_ledger(d2, liar))
    assert "실행 기록과 다르다" in str(ei.value), str(ei.value)


def test_the_committed_ledger_passes_the_planned_index_gate():
    """실제 `LEG_PRESERVATION.yaml` 이 계획 index 계약을 만족한다."""
    from tools.preserve import assert_planned_index_consistent

    assert assert_planned_index_consistent()


# ─────────────────────────────────────────────────────────────────────────────
# 47차 P0-5 — "versions() 의 유일한 통로" 가 코드상 사실이 아니었다
#
# 46차는 `_version_candidates()` 를 만들고 요청문에 "유일한 통로" 라고 적었다.
# 그런데 `_repair_source()` 와 `_repair_target()` 는 `provider.versions()` 를
# **직접 다시** 부른다. provider 가 호출마다 다른 목록을 주면 (실물 SDK 의
# 재시도·eventual consistency 에서 실제로 일어난다) 검증되지 않은 후보가
# 되돌릴 수 없는 `lock()` 에 도달한다.
# ─────────────────────────────────────────────────────────────────────────────

class _AlternatingVersionStore(_LockingStore):
    """첫 호출은 정상 목록, 그 다음부터 falsy locator 를 섞는다."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.calls = 0
        self.locked_with: list = []

    def versions(self, key: str) -> list:
        self.calls += 1
        real = super().versions(key)
        return real if self.calls <= 1 else ([""] + real)

    def get(self, key: str, version=None) -> bytes:
        # falsy locator 를 head lookup 으로 해석하는 adapter 를 흉내낸다
        return super().get(key, version or None)

    def describe_object(self, key: str, version=None):
        if version == "":
            return {"mode": None, "retain_until": None}      # "아직 안 잠겼다"
        return super().describe_object(key, version)

    def lock(self, key: str, version=None, until=None, **kw):
        self.locked_with.append((key, version))
        return super().lock(key, version, until, **kw)


def test_repair_lookups_go_through_the_validated_version_snapshot(tmp_path):
    """★ 47차 P0-5 — 수리 경로도 검증된 후보만 본다."""
    store = _AlternatingVersionStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    key, data = "objects/x", b"payload"
    dg = hashlib.sha256(data).hexdigest()
    store.put(key, data)

    store.calls = 1          # 다음 열거부터 falsy 후보가 섞이게 한다
    with pytest.raises(PreserveError) as ei:
        backend._repair_source(key, dg)
    assert "version" in str(ei.value), str(ei.value)

    store.calls = 1
    with pytest.raises(PreserveError):
        backend._repair_target(key, dg)
    assert not store.locked_with, f"거부 전에 이미 잠갔다: {store.locked_with}"


def test_a_falsy_locator_never_reaches_lock_through_repair(tmp_path):
    """★ 47차 P0-5 — alternating 응답에서 `lock()` 호출이 **0** 이어야 한다.

    되돌릴 수 없는 WORM lock 이 잘못된 version 에 걸리면 사후 proof 재유도가
    실패해도 되돌릴 수 없다.
    """
    store = _AlternatingVersionStore(name=str(tmp_path))
    backend = _lockstore(tmp_path, store)
    key, data = "objects/y", b"payload-y"
    dg = hashlib.sha256(data).hexdigest()
    store.put(key, data)
    before = dict(store._lock)

    store.calls = 1
    with pytest.raises(PreserveError):
        backend._lock_to_proof(key, dg, "2099-01-01T00:00:00Z", lambda: data)
    assert not store.locked_with, f"lock 이 불렸다: {store.locked_with}"
    assert dict(store._lock) == before, "lock map 이 바뀌었다"


def test_no_version_enumeration_bypasses_the_helper():
    """★ 47차 P0-5 — 구조로 못 박는다: `provider.versions(` 직접 호출 금지.

    46차 요청문은 "유일한 통로" 라고 주장했지만 코드에는 우회 둘이 있었다.
    주장 대신 검사를 둔다.
    """
    import re

    src = (pathlib.Path(__file__).resolve().parents[1]
           / "tools" / "preserve.py").read_text(encoding="utf-8")
    body = src.split("def _version_candidates", 1)
    assert len(body) == 2, "전제: 검증 helper 가 있다"
    # helper 정의 앞뒤 어디서든 provider.versions( 를 직접 부르면 안 된다.
    # helper 자신은 `vs(key)` 로 부르므로 이 패턴에 걸리지 않는다.
    # 두 철자를 다 막는다. 46차 우회는 `getattr(self.provider, "versions")`
    # 였으므로 `self.provider.versions(` 만 보는 검사는 통과했다 (실측).
    direct = [m.group(0) for m in
              re.finditer(r"self\.provider\.versions\(", src)]
    indirect = [m.group(0) for m in
                re.finditer(r'getattr\(\s*self\.provider\s*,\s*["\']versions["\']',
                            src)]
    outside = direct + [x for x in indirect]
    # helper 자신은 capability 확인을 위해 한 번 getattr 을 쓴다 — 그 하나만 허용.
    assert len(outside) <= 1, (
        f"version 열거 우회가 {len(outside)}곳 있다 ({outside}) — 모든 열거는 "
        "`_version_candidates()` 를 지나야 한다")


# ─────────────────────────────────────────────────────────────────────────────
# 47차 P0-1 · P0-2 — prospective lifecycle (조건 11 의 본체)
#
# 46차 판정: "정상적인 prospective leg 가 gate·원장 lint·publisher 를 동시에
# 통과할 상태가 없다." 실제로 그렇다 —
#
#   L 이 roster 밖 · plan=planned          → gate 통과, publisher 가 undeclared 로 거부
#   L 을 roster 에만 추가 · plan=planned   → roster ↔ 실행 legs exact 불변식 실패
#   L 을 실행 legs 에도 추가 · plan=planned → planned-index consistency 실패
#   plan=executed 로 변경                   → gate 가 거부 (실행 전에 실행됨으로 기록)
#
# 즉 46차의 gate 는 read-only predicate 였고 lifecycle 이 아니었다.
# ─────────────────────────────────────────────────────────────────────────────

_LIFECYCLE_LEDGER = textwrap.dedent('''\
    schema_version: 4
    cohorts:
      - cohort_id: gA
        dir: docs/22p_gap/coh
        status: active
        legs: ["done"]
        prospective_legs: ["L"]
        cross_leg_comparison: allowed_within_cohort
        pin:
          schema_version: 3
          compute_sha256: "aaaaaaaaaaaaaaaa"
          row_projection_py_sha256: "bbbbbbbbbbbbbbbb"
          src_scoring_py_sha256: "cccccccccccccccc"
          analysis_spec_sha256: "dddddddddddddddd"
          producer_semantic_sha256: "eeeeeeeeeeeeeeee"
    planned:
      - leg_id: done
        cohort_id: gA
        status: executed
        authorization_kind: retrospective
        authorized_source_digest: "fedcba9876543210"
        run_spec_digest: "%s"
        recorded_on: "2026-08-20"
        근거: "시험용 — 소급 기록"
      - leg_id: L
        cohort_id: gA
        status: planned
        authorization_kind: prospective
        authorized_source_digest: "0123456789abcdef"
        run_spec_digest: "%s"
        run_spec:
          leg_id: L
          mode: fit
          objective: pocv_dvdq
          n_restarts: 3
          reference: grid
        recorded_on: "2026-08-28"
        근거: "시험용 — 계획"
    legs:
      - leg_id: done
        preservation_status: full_bundle
        evidence:
          leg_source_digest: "fedcba9876543210"
          cohorts: ["gA"]
    ''')

_RUN_SPEC_L = {"leg_id": "L", "mode": "fit", "objective": "pocv_dvdq",
               "n_restarts": 3, "reference": "grid"}


def _spec_digest(spec: dict) -> str:
    return hashlib.sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def _lifecycle_ledger(tmp_path) -> pathlib.Path:
    body = _LIFECYCLE_LEDGER % ("retrospective:no-preauthorization",
                               _spec_digest(_RUN_SPEC_L))
    p = tmp_path / "LEG_PRESERVATION.yaml"
    p.write_text(body, encoding="utf-8")
    return p


def test_a_prospective_leg_has_a_state_that_passes_every_gate(tmp_path):
    """★ 47차 P0-1 — 계획된 leg 가 **실행 전에** 존재할 수 있어야 한다.

    prospective roster 를 executed roster 와 분리한다. 그러지 않으면 어떤
    배치를 해도 gate·lint·publisher 중 하나가 반드시 실패한다.
    """
    from tools.preserve import (assert_planned_index_consistent, planned_index)

    led = _lifecycle_ledger(tmp_path)
    assert assert_planned_index_consistent(ledger=led)
    idx = planned_index(ledger=led)
    assert idx["L"]["status"] == "planned"
    assert idx["done"]["status"] == "executed"


def test_exactly_one_attempt_enters_compute(tmp_path):
    """★ 47차 P0-2 — 승인은 read-only predicate 가 아니라 **원자적 claim** 이다.

    46차 `assert_planned_leg()` 는 같은 row 로 몇 번이고 통과했고 동시 실행도
    둘 다 계산에 들어갔다.
    """
    from tools.preserve import claim_planned_leg, PreserveError

    led = _lifecycle_ledger(tmp_path)
    root = tmp_path / "claims"
    c1 = claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                           ledger=led, claims_root=root)
    assert c1.attempt_id and len(c1.attempt_id) >= 16

    with pytest.raises(PreserveError) as ei:
        claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                          ledger=led, claims_root=root)
    assert "이미" in str(ei.value) or "claim" in str(ei.value), str(ei.value)


def test_the_claim_seals_the_exact_run_spec(tmp_path):
    """★ 47차 P0-2 — 같은 이름이 아무 실행이나 승인하면 allowlist 지 계획이 아니다.

    46차 planned row 는 leg·cohort·source digest 만 담아
    `--objective A --n-restarts 1` 과 `--objective B --n-restarts 999` 를
    똑같이 승인했다.
    """
    from tools.preserve import claim_planned_leg, PreserveError

    led = _lifecycle_ledger(tmp_path)
    root = tmp_path / "claims"
    other = dict(_RUN_SPEC_L, objective="pocv", n_restarts=999)
    with pytest.raises(PreserveError) as ei:
        claim_planned_leg("L", other, "0123456789abcdef",
                          ledger=led, claims_root=root)
    assert "run_spec" in str(ei.value), str(ei.value)
    assert not root.exists() or not any(root.rglob("*.claim")), (
        "거부하면서 claim 을 만들었다")


def test_the_whole_index_must_be_consistent_before_any_leg_is_claimed(tmp_path):
    """★ 47차 — target predicate 만 보면 다른 leg 때문에 깨진 원장으로도 시작한다."""
    from tools.preserve import claim_planned_leg, PreserveError

    body = (_LIFECYCLE_LEDGER % ("retrospective:no-preauthorization",
                                _spec_digest(_RUN_SPEC_L))).replace(
        'leg_source_digest: "fedcba9876543210"',
        'leg_source_digest: "0000000000000000"')
    led = tmp_path / "LEG_PRESERVATION.yaml"
    led.write_text(body, encoding="utf-8")
    with pytest.raises(PreserveError) as ei:
        claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                          ledger=led, claims_root=tmp_path / "claims")
    assert "실행 기록과 다르다" in str(ei.value), str(ei.value)


def test_a_crashed_attempt_finalizes_without_recomputing(tmp_path):
    """★ 47차 P0-1 — 중단 뒤 **재계산 없이** finalize 할 수 있어야 한다.

    phase receipt 를 남긴 뒤 process 가 죽어도, 같은 claim 을 재개해 남은
    phase 만 하고 executed 로 닫는다.
    """
    from tools.preserve import (claim_planned_leg, resume_claim, finalize_leg,
                                planned_index, PreserveError)

    led = _lifecycle_ledger(tmp_path)
    root = tmp_path / "claims"
    c = claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                          ledger=led, claims_root=root)
    c.phase_done("grid", {"rows": 10})
    token = c.token
    del c                                            # process 가 죽었다

    # finalize 는 아직 안 된다 — fit phase 가 없다
    with pytest.raises(PreserveError) as ei:
        finalize_leg("L", ledger=led, claims_root=root, token=token,
                     evidence={"leg_source_digest": "0123456789abcdef",
                               "cohorts": ["gA"]})
    assert "phase" in str(ei.value), str(ei.value)

    # ★ 48차 P0-3 — 재개는 **소유 증명**을 든 실행만 한다.
    r = resume_claim("L", claims_root=root, token=token, ledger=led)
    assert r.token == token, "재개가 새 attempt 를 만들었다"
    assert r.phases_done() == ("grid",)
    r.phase_done("fit", {"fits": 4})

    finalize_leg("L", ledger=led, claims_root=root, token=token,
                 evidence={"leg_source_digest": "0123456789abcdef",
                           "cohorts": ["gA"]})
    idx = planned_index(ledger=led)
    assert idx["L"]["status"] == "executed", "executed 로 닫히지 않았다"


def test_finalizing_moves_the_leg_from_prospective_to_executed_roster(tmp_path):
    """★ 47차 P0-1 — executed 전이는 roster·실행 기록까지 한 번에 옮긴다."""
    import yaml

    from tools.preserve import (claim_planned_leg, finalize_leg,
                                assert_planned_index_consistent)

    led = _lifecycle_ledger(tmp_path)
    root = tmp_path / "claims"
    c = claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                          ledger=led, claims_root=root)
    c.phase_done("grid", {})
    c.phase_done("fit", {})
    finalize_leg("L", ledger=led, claims_root=root, token=c.token,
                 evidence={"leg_source_digest": "0123456789abcdef",
                           "cohorts": ["gA"]})

    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    coh = doc["cohorts"][0]
    assert "L" in coh["legs"], "실행 roster 에 안 들어갔다"
    assert "L" not in (coh.get("prospective_legs") or []), "계획 roster 에 남았다"
    assert any(l["leg_id"] == "L" for l in doc["legs"]), "실행 기록이 없다"
    assert assert_planned_index_consistent(ledger=led)


def test_an_executed_leg_cannot_be_reclaimed(tmp_path):
    """★ 47차 P0-2 — executed 기록은 다음 실행의 승인이 아니다 (46차 규칙 유지)."""
    from tools.preserve import claim_planned_leg, PreserveError

    led = _lifecycle_ledger(tmp_path)
    with pytest.raises(PreserveError) as ei:
        claim_planned_leg("done", _RUN_SPEC_L, "fedcba9876543210",
                          ledger=led, claims_root=tmp_path / "claims")
    assert "executed" in str(ei.value) or "이미 실행" in str(ei.value), str(ei.value)


# ─────────────────────────────────────────────────────────────────────────────
# 47차 — 계획 parser 가 publisher 와 **같은 authority** 를 봐야 한다
#
# 46차 진단(리뷰어 in-memory probe): 계획 parser 는 cohort 목록을 따로 약하게
# 읽었다. 그래서 저장소 밖 `dir` 을 가진 cohort 를 승인했고, 반대 방향
# consistency 도 exact equality 가 아니라 phantom executed 항목을 통과시켰다.
# ─────────────────────────────────────────────────────────────────────────────

def test_the_plan_parser_refuses_a_cohort_dir_outside_the_repository(tmp_path):
    """★ 47차 — `dir` 위생을 publisher 와 **같은 규칙**으로 본다."""
    from tools.preserve import planned_index, PreserveError

    body = _PLAN_LEDGER.replace("    dir: docs/22p_gap/coh\n",
                                "    dir: ../../outside\n", 1)
    with pytest.raises(PreserveError) as ei:
        planned_index(ledger=_plan_ledger(tmp_path, body))
    assert "dir" in str(ei.value) or "저장소" in str(ei.value), str(ei.value)


@pytest.mark.parametrize("bad", ["/etc", "docs//22p_gap/coh", "./docs/22p_gap/coh"])
def test_the_plan_parser_requires_a_canonical_relative_dir(tmp_path, bad):
    from tools.preserve import planned_index, PreserveError

    body = _PLAN_LEDGER.replace("    dir: docs/22p_gap/coh\n", f"    dir: {bad}\n", 1)
    with pytest.raises(PreserveError):
        planned_index(ledger=_plan_ledger(tmp_path, body))


@pytest.mark.parametrize("bad", ["Active", "retired", ""])
def test_the_plan_parser_requires_the_exact_cohort_status_enum(tmp_path, bad):
    from tools.preserve import planned_index, PreserveError

    body = _PLAN_LEDGER.replace("    status: active\n", f"    status: {bad}\n", 1)
    with pytest.raises(PreserveError):
        planned_index(ledger=_plan_ledger(tmp_path, body))


def test_a_phantom_executed_plan_without_an_execution_record_is_refused(tmp_path):
    """★ 47차 — 반대 방향도 **exact equality** 다.

    46차는 "실행 기록 ⊆ 계획" 만 봤으므로, 실행 기록이 없는 executed 계획
    항목(phantom)이 조용히 통과했다.
    """
    from tools.preserve import assert_planned_index_consistent, PreserveError

    # 유령을 cohort 의 **실행 roster 에도** 넣는다 — 그래야 roster 검사가
    # 아니라 **exact equality** 로 죽는지 확인된다 (처음 썼을 때 roster 검사가
    # 가려서 false green 이었다).
    body = _PLAN_LEDGER.replace('    legs: ["Z"]\n',
                                '    legs: ["Z", "유령"]\n', 1)
    assert '"유령"' in body, "전제: gF 실행 roster 에 유령을 넣었다"
    body = body.replace("legs:\n  - leg_id: ran\n", (
        "  - leg_id: 유령\n"
        "    cohort_id: gF\n"
        "    status: executed\n"
        "    authorization_kind: retrospective\n"
        '    authorized_source_digest: "1111111111111111"\n'
        '    run_spec_digest: "retrospective:no-preauthorization"\n'
        '    recorded_on: "2026-08-28"\n'
        "    근거: 유령\n"
        "legs:\n  - leg_id: Z\n"), 1)
    with pytest.raises(PreserveError) as ei:
        assert_planned_index_consistent(ledger=_plan_ledger(tmp_path, body))
    assert "유령" in str(ei.value), str(ei.value)


def test_the_committed_ledger_reports_no_gate_backed_execution_yet():
    """★ 47차 — 소급 기록을 **실행 gate 증거로 세지 않는다**.

    지금 원장의 8건은 전부 소급이다. 그 사실을 기계가 답할 수 있어야 한다
    (자유문자 근거를 사람이 읽고 세는 것이 아니라).
    """
    from tools.preserve import planned_coverage

    cov = planned_coverage()
    assert cov["retrospective"] == 8, cov
    assert cov["prospective"] == 0, cov
    assert cov["gate_backed_executions"] == 0, (
        "실행 전 gate 를 실제로 지난 실행이 있다고 셌다 — 지금은 하나도 없다")


# ─────────────────────────────────────────────────────────────────────────────
# 47차 P0-3 — smoke 경계는 문자열 prefix 가 아니라 **정규 격리**여야 한다
#
# 46차 `plan_gate()` 는 shell `case` pattern 으로만 `results/_smoke` 를 봤다.
# `results/_smoke/../grid_fit_v4` 는 두 문자열이 prefix 에 맞아 gate 를
# 면제받지만 실제 출력은 `results/grid_fit_v4` 다. symlink 도 같다.
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("bad", [
    "results/_smoke/../grid_fit_v4",       # 어휘적으로는 안, 실제로는 밖
    "results/_smoke/./../x",               # 같은 축
])
def test_a_traversing_path_is_not_inside_the_smoke_namespace(tmp_path, bad):
    from tools.preserve import is_inside_namespace

    root = tmp_path / "repo"
    (root / "results" / "_smoke").mkdir(parents=True)
    assert not is_inside_namespace(root / bad, root / "results" / "_smoke"), (
        f"{bad} 가 smoke namespace 안이라고 판정됐다")


def test_a_symlinked_path_is_not_inside_the_smoke_namespace(tmp_path):
    from tools.preserve import is_inside_namespace

    root = tmp_path / "repo"
    ns = root / "results" / "_smoke"
    ns.mkdir(parents=True)
    outside = root / "outside"
    outside.mkdir()
    (ns / "link").symlink_to(outside, target_is_directory=True)
    assert not is_inside_namespace(ns / "link" / "run", ns), (
        "symlink 을 지나 밖으로 나가는 경로가 안이라고 판정됐다")
    assert is_inside_namespace(ns / "real" / "run", ns), (
        "아직 없는 실제 하위 경로가 밖이라고 판정됐다")


def test_the_namespace_check_is_fail_closed_on_a_symlinked_component(tmp_path):
    """중간 성분이 symlink 면 그 자체로 '안' 이 아니다 — 뒤에 뭐가 오든."""
    from tools.preserve import is_inside_namespace

    root = tmp_path / "repo"
    ns = root / "results" / "_smoke"
    ns.mkdir(parents=True)
    (ns / "self").symlink_to(ns, target_is_directory=True)
    assert not is_inside_namespace(ns / "self" / "run", ns), (
        "symlink 성분을 지난 경로를 안으로 봤다 — 나중에 target 을 바꾸면 밖이다")


def test_the_module_entrypoint_is_gated_not_just_the_wrapper(tmp_path, monkeypatch):
    """★ 47차 조건 11-c — `python -m src.grid` 직접 호출도 계획을 본다.

    46차 gate 는 `run.sh` 안에만 있었다. `--leg` 는 shell 이 소비했고 모듈
    직접 호출은 계획을 전혀 보지 않았다. gate 가 wrapper 에 있으면 wrapper 를
    안 쓰면 그만이다.
    """
    import src.grid as G

    monkeypatch.setenv("LEG", "__계획에없는다리__")
    with pytest.raises(PreserveError) as ei:
        G._assert_grid_authorized({"x": 1}, tmp_path / "outside_run")
    assert "계획" in str(ei.value), str(ei.value)


def test_the_module_gate_is_exempt_only_inside_the_smoke_namespace(monkeypatch,
                                                                   tmp_path):
    """면제는 정규 격리로 판정한 smoke namespace 하나뿐이다."""
    import src.grid as G
    from tools.preserve import SMOKE_NAMESPACE

    monkeypatch.setenv("LEG", "__계획에없는다리__")
    SMOKE_NAMESPACE.mkdir(parents=True, exist_ok=True)
    assert G._assert_grid_authorized({"x": 1}, SMOKE_NAMESPACE / "probe") is None

    # 어휘적으로만 안인 경로는 면제되지 않는다
    with pytest.raises(PreserveError):
        G._assert_grid_authorized({"x": 1}, SMOKE_NAMESPACE / ".." / "escaped")


def test_a_dry_run_still_needs_authorization(tmp_path, monkeypatch):
    """★ 47차 조건 11-e — `--dry-run` 은 두 번째 flag 면제였다.

    `run_grid(dry_run=True)` 는 출력 디렉터리를 만들고 완방상태·baseline 을
    계산한 뒤 최대 세 조건에 solver 를 실제로 부른다. 계산이 있으면 gate 도
    있어야 한다.
    """
    import src.grid as G

    monkeypatch.setenv("LEG", "__계획에없는다리__")
    with pytest.raises(PreserveError):
        G._assert_grid_authorized({"x": 1}, tmp_path / "probe", dry_run=True)


def test_run_sh_has_no_flag_exemption_for_the_plan_gate():
    """구조로 못 박는다 — `plan_gate` 를 조건부로 부르지 않는다."""
    import re

    src = (pathlib.Path(__file__).resolve().parents[1] / "run.sh").read_text(
        encoding="utf-8")
    calls = [l.strip() for l in src.splitlines()
             if re.search(r"(^|\s)plan_gate\s*$", l)]
    assert calls, "plan_gate 호출이 없다"
    for c in calls:
        assert c == "plan_gate", (
            f"plan_gate 호출에 조건이 붙어 있다: {c!r} — flag 면제는 두지 않는다")


def test_run_grid_calls_the_gate_before_its_first_side_effect(tmp_path,
                                                              monkeypatch):
    """★ 47차 조건 11-c — gate 함수가 있는 것과 **불리는** 것은 다르다.

    `_assert_grid_authorized()` 를 직접 부르는 시험만 두면 호출 지점을 지워도
    초록이다. `run_grid()` 가 mkdir 보다 **먼저** 부르는지 본다.
    """
    import src.grid as G

    monkeypatch.setenv("LEG", "__계획에없는다리__")
    out = tmp_path / "never_created"
    # ★ 48차 P1 — **순서를 먼저 본다.** 47차는 `pytest.raises(PreserveError)`
    #   가 바깥이라, 호출 지점을 지우면 실행이 계속 흘러가 한참 뒤 다른 이유로
    #   (`KeyError: 'discharged_state'`) 죽었고 그 KeyError 가 증인이 됐다.
    #   그것은 "gate 가 mkdir 보다 먼저 불렸다" 를 증명하지 않는다 — 그냥
    #   나중에 뭔가 터졌다는 뜻이다.
    with pytest.raises(BaseException) as ei:
        G.run_grid({"x": 1}, [], nproc=1, chunk_size=1, out_dir=out)
    assert not out.exists(), (
        "gate 가 거부하기 전에 출력 디렉터리를 만들었다 — 첫 부작용보다 "
        "먼저 불려야 한다")
    assert isinstance(ei.value, PreserveError), (
        f"거부한 것이 계획 gate 가 아니다: "
        f"{type(ei.value).__name__}: {ei.value}")


def test_a_retrospective_row_cannot_be_claimed(tmp_path):
    """★ 47차 — 소급 기록은 **실행 승인이 아니다**.

    `authorization_kind` 를 도입만 하고 claim 이 그것을 보지 않으면, 소급 8건이
    그대로 실행 승인으로 재사용된다 (46차가 `executed` 로 막던 것을 종류
    축에서 다시 열어 주는 셈이다).
    """
    from tools.preserve import claim_planned_leg, PreserveError

    body = _LIFECYCLE_LEDGER % ("retrospective:no-preauthorization",
                               _spec_digest(_RUN_SPEC_L))
    # L 을 소급으로 바꾼다 (상태는 planned 그대로 — 종류 축만 본다).
    # ★ 48차 P0-5 — 소급 항목은 `run_spec:` 을 담을 수 **없으므로** 그것도
    #   함께 뗀다. 안 그러면 schema 검사가 먼저 거부해 이 시험이 보려는
    #   **종류 축**이 아니라 key 집합 축을 보게 된다 (약한 증인).
    import yaml as _y
    _d = _y.safe_load(body)
    _row = next(e for e in _d["planned"] if e["leg_id"] == "L")
    _row["authorization_kind"] = "retrospective"
    _row["run_spec_digest"] = "retrospective:no-preauthorization"
    _row.pop("run_spec", None)
    body = _y.safe_dump(_d, allow_unicode=True, sort_keys=False)
    led = tmp_path / "LEG_PRESERVATION.yaml"
    led.write_text(body, encoding="utf-8")
    with pytest.raises(PreserveError) as ei:
        claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                          ledger=led, claims_root=tmp_path / "claims")
    assert "소급" in str(ei.value) or "retrospective" in str(ei.value), str(ei.value)


# ─────────────────────────────────────────────────────────────────────────────
# 48차 P0-3 — public gate 가 `O_EXCL` 의 배타성을 되돌렸다
#
# 47차 `assert_run_is_authorized()` 는 claim 파일이 보이면 caller credential
# 없이 `resume_claim()` 하고 같은 spec/source 면 그 claim 을 돌려줬다. 그래서
# 같은 public 호출 둘이 **모두** 같은 attempt 로 compute 에 들어갔다.
# `O_EXCL` 은 파일 최초 생성만 배타적이었지 **실행권**은 배타적이지 않았다.
#
# 공식 회귀는 production gate 가 아니라 low-level `claim_planned_leg()` 를 두 번
# 부르고 있었으므로 이 우회를 보지 못했다.
# ─────────────────────────────────────────────────────────────────────────────

def _authorize(leg, spec, src, led, claims, **kw):
    from tools.preserve import assert_run_is_authorized
    return assert_run_is_authorized(leg, "grid", [Path("/nonsmoke/out")], spec,
                                    src, ledger=led, claims_root=claims, **kw)


def test_two_public_authorizations_do_not_both_enter_compute(tmp_path):
    """★ 48차 P0-3 — 두 번째 public start 는 거부돼야 한다."""
    from tools.preserve import PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    a = _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims)
    assert a is not None and a.attempt_id

    with pytest.raises(PreserveError) as ei:
        _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims)
    assert "이미" in str(ei.value) or "token" in str(ei.value), str(ei.value)


def test_resuming_requires_the_owner_token(tmp_path):
    """★ 48차 P0-3 — 재개는 **소유 증명**이 있어야 한다.

    이름과 spec 만으로 재개할 수 있으면 그것은 재개가 아니라 두 번째 발급이다.
    """
    from tools.preserve import PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    a = _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims)

    with pytest.raises(PreserveError):
        _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims,
                   token="0" * 32)
    same = _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims,
                      token=a.token)
    assert same.attempt_id == a.attempt_id, "올바른 token 으로도 재개하지 못했다"


def test_a_revoked_plan_stops_a_live_claim(tmp_path):
    """★ 48차 P0-3 — 재개는 **살아 있는 원장 authority** 를 다시 본다.

    47차 existing-claim 분기는 원장을 읽지 않았다. claim 을 얻은 뒤 계획에서
    L 을 지우거나 cohort 를 frozen 으로 바꿔도 authorization 이 계속 성공했다.
    """
    from tools.preserve import PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    a = _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims)

    # ★ 48차 — 원장은 이제 claim 시점에 `yaml.safe_dump` 로 다시 쓰이므로
    #   들여쓰기에 기대는 문자열 치환은 대상을 놓친다. 구조로 고친다.
    import yaml
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    doc["cohorts"][0]["status"] = "frozen"
    led.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
                   encoding="utf-8")
    with pytest.raises(PreserveError) as ei:
        _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims,
                   token=a.token)
    assert "frozen" in str(ei.value) or "active" in str(ei.value), str(ei.value)


def test_a_phase_cannot_be_recorded_without_the_owner_token(tmp_path):
    """phase 도 소유 증명이 있어야 한다 — claim 파일이 보이는 것만으로는 안 된다."""
    from tools.preserve import resume_claim, PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims)
    with pytest.raises(PreserveError):
        resume_claim("L", claims_root=claims, token="0" * 32)


# ─────────────────────────────────────────────────────────────────────────────
# 48차 P0-6 — 원장 전이가 원자적이지 않았다
# ─────────────────────────────────────────────────────────────────────────────

def _finish(claim):
    """두 phase 를 닫아 finalize 가능한 claim 으로 만든다."""
    for ph in ("grid", "fit"):
        claim.phase_done(ph, {"ok": True})


def test_two_concurrent_finalizations_lose_no_leg(tmp_path):
    """★ 48차 P0-6 — `finalize_leg()` 은 원장을 **read-modify-write** 했다.

    두 다리를 동시에 닫으면 둘 다 같은 `doc` 을 읽고 각자 통째로 덮어썼다 —
    나중 쓰기가 먼저 쓰기를 지운다. 실행 기록 하나가 조용히 사라지는데
    두 호출 모두 성공을 돌려준다. 원장은 **실행이 있었다는 유일한 증거**이므로
    lost update 는 증거 소실이다.
    """
    import yaml
    from tools import preserve as P

    led = _lifecycle_ledger(tmp_path)
    # 계획에 두 다리를 둔다
    body = led.read_text(encoding="utf-8")
    spec_m = dict(_RUN_SPEC_L, leg_id="M")
    body = body.replace('    prospective_legs: ["L"]\n',
                        '    prospective_legs: ["L", "M"]\n')
    body += textwrap.dedent(f'''\
        planned_extra_marker: 0
        ''')
    doc = yaml.safe_load(body)
    doc["planned"].append({
        "leg_id": "M", "cohort_id": "gA", "status": "planned",
        "authorization_kind": "prospective",
        "authorized_source_digest": "0123456789abcdef",
        "run_spec_digest": _spec_digest(spec_m), "run_spec": dict(spec_m),
        "recorded_on": "2026-08-28", "근거": "시험용 — 계획 2"})
    doc.pop("planned_extra_marker", None)
    led.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
                   encoding="utf-8")

    claims = tmp_path / "claims"
    cL = P.claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                             ledger=led, claims_root=claims)
    cM = P.claim_planned_leg("M", spec_m, "0123456789abcdef",
                             ledger=led, claims_root=claims)
    _finish(cL)
    _finish(cM)

    import threading
    barrier = threading.Barrier(2)

    def _go(leg, token, q):
        try:
            barrier.wait(timeout=30)
            P.finalize_leg(leg, {"leg_source_digest": "0123456789abcdef",
                                 "cohorts": ["gA"]},
                           ledger=led, claims_root=claims, token=token)
            q.put((leg, None))
        except Exception as e:                              # noqa: BLE001
            q.put((leg, f"{type(e).__name__}: {e}"))

    import threading
    q: "queue.Queue" = __import__("queue").Queue()
    ts = [threading.Thread(target=_go, args=("L", cL.token, q)),
          threading.Thread(target=_go, args=("M", cM.token, q))]
    for t in ts:
        t.start()
    for t in ts:
        t.join(timeout=60)
    outcome = dict(q.get() for _ in range(2))

    final = yaml.safe_load(led.read_text(encoding="utf-8"))
    recorded = {e["leg_id"] for e in final.get("legs") or []}
    ok = {leg for leg, err in outcome.items() if err is None}
    assert ok, f"둘 다 거부됐다 — 진행 불가도 고장이다: {outcome}"
    missing = ok - recorded
    assert not missing, (
        f"성공을 돌려준 다리가 원장에 없다: {sorted(missing)} — lost update "
        f"(원장 legs={sorted(recorded)}, 결과={outcome})")
    coh = final["cohorts"][0]
    for leg in ok:
        assert leg in coh["legs"], f"{leg} 이 실행 roster 에 없다"
        assert leg not in (coh.get("prospective_legs") or []), (
            f"{leg} 이 계획 roster 에 남아 있다")


def test_a_claim_marks_the_plan_running(tmp_path):
    """★ 48차 P0-6 — `planned → running` 이 **한 번도 쓰이지 않았다.**

    `PLANNED_STATUS` 에 `running` 을 선언해 놓고 어떤 코드도 그 값을 쓰지
    않았다. 그러면 원장만 보고 "지금 도는 다리가 있는가" 를 답할 수 없고,
    claim 파일이 사라진 crash 뒤에 계획은 여전히 `planned` 이라 다른 실행이
    태연히 새 claim 을 딴다. 선언만 있고 전이가 없는 상태는 상태 기계가 아니다.
    """
    import yaml
    from tools import preserve as P

    led = _lifecycle_ledger(tmp_path)
    P.claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                        ledger=led, claims_root=tmp_path / "claims")
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    row = next(e for e in doc["planned"] if e["leg_id"] == "L")
    assert row["status"] == "running", (
        f"claim 을 땄는데 계획 상태가 {row['status']!r} 이다 — 원장만 보고 "
        "실행 중인 다리를 알 수 없다")


def test_two_phase_records_do_not_overwrite_each_other(tmp_path):
    """★ 48차 P0-6 — `phase_done()` 도 read-modify-write 였다.

    `grid` 와 `fit` 을 동시에 닫으면 둘 다 `phases` 가 빈 record 를 읽고 각자
    자기 phase 하나만 담아 덮어쓴다. 하나가 사라지면 `finalize_leg()` 이
    "phase 가 남았다" 며 거부하고, 이미 끝난 계산을 다시 돌리게 된다.
    """
    import threading
    from tools import preserve as P

    led = _lifecycle_ledger(tmp_path)
    claim = P.claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                                ledger=led, claims_root=tmp_path / "claims")
    barrier = threading.Barrier(2)

    def _go(ph):
        barrier.wait(timeout=30)
        claim.phase_done(ph, {"ok": ph})

    ts = [threading.Thread(target=_go, args=(p,)) for p in ("grid", "fit")]
    for t in ts:
        t.start()
    for t in ts:
        t.join(timeout=60)
    assert set(claim.phases_done()) == {"grid", "fit"}, (
        f"동시에 닫은 phase 하나가 사라졌다: {claim.phases_done()}")


def test_a_leg_id_cannot_escape_the_claims_root(tmp_path):
    """★ 48차 P0-6 — claim 경로가 `check_id()` 를 안 썼다.

    `_claim_path()` 는 `"/" in leg_id` 만 봤다. Windows separator 는 통과하고,
    이 저장소는 이미 그 정확한 반례를 위해 `check_id()` 를 갖고 있었다
    (27차 P1-4). 같은 도메인 검사가 두 곳에서 다르면 약한 쪽이 실효 규칙이다.
    """
    from tools import preserve as P

    for bad in ("..\\..\\outside", "../escape", ".", "..", "nul", "a b",
                "x" * 70):
        with pytest.raises(P.PreserveError) as ei:
            P._claim_path(bad, tmp_path / "claims")
        assert ei.value.stage in ("id", "plan"), (bad, ei.value.stage)


# ─────────────────────────────────────────────────────────────────────────────
# 48차 P0-5 — 승인한 것과 실행한 것이 같다는 보장이 없었다
# ─────────────────────────────────────────────────────────────────────────────

def test_the_leg_run_spec_seals_what_actually_gets_computed():
    """★ 48차 P0-5 — 47차 gate 가 승인한 spec 은 실행을 고정하지 못했다.

    `_assert_grid_authorized()` 의 spec 은 `{leg_id, mode, dry_run,
    config_digest}` 넷뿐이었다. 그런데 `--lli` · `--lam-pe` · `--noise` 는
    **조건 집합 자체**를 바꾸고 `--out` 은 결과가 어디 놓일지를 바꾼다. 승인한
    뒤 그 축들을 통째로 갈아도 같은 digest 가 나온다 — 그러면 승인은 다리
    **이름**을 승인한 것이지 실행을 승인한 것이 아니다.

    한 다리의 spec 은 두 phase 가 **같은 값**을 내야 한다 (그래야 하나의 claim
    아래 grid 와 fit 이 묶인다). 그래서 phase 별 자원 축(nproc·chunk)은 넣지
    않는다 — 그것은 결과를 바꾸지 않는다.
    """
    from tools.preserve import leg_run_spec, run_spec_digest

    g = {"config_digest": "a" * 16, "condition_ids_sha256": "b" * 16,
         "n_conditions": 12, "discharged_cache_sha256": None, "out": "results/grid_fit_v4"}
    # ★ 49차 P0-5 — fit 축이 넓어졌다 (아래 `_F49` 와 같은 계약)
    f = dict(_F49, out="results/grid_fit_v4", **{"in": "results/grid_fit_v4"})
    base = run_spec_digest(leg_run_spec("L", g, f))

    # 두 phase 가 같은 spec 을 만든다 (하나의 claim 아래 묶이는 조건)
    assert leg_run_spec("L", g, f) == leg_run_spec("L", dict(g), dict(f))

    # 결과를 바꾸는 축은 전부 digest 를 움직인다
    for name, gg, ff in (
            ("조건 집합", dict(g, condition_ids_sha256="0" * 16), f),
            ("조건 수", dict(g, n_conditions=13), f),
            ("grid config", dict(g, config_digest="0" * 16), f),
            ("grid 산출 위치", dict(g, out="results/elsewhere"), f),
            ("fit config", g, dict(f, config_digest="0" * 16)),
            ("목적함수 집합", g, dict(f, objective_order=["pocv_dvdq", "other"])),
            ("fit 산출 위치", g, dict(f, out="results/elsewhere"))):
        assert run_spec_digest(leg_run_spec("L", gg, ff)) != base, (
            f"{name} 을 바꿨는데 승인 digest 가 그대로다")

    # 다리 이름도 축이다
    assert run_spec_digest(leg_run_spec("M", g, f)) != base


def test_the_leg_run_spec_refuses_an_undeclared_axis():
    """★ 48차 P0-5 — spec 은 **닫힌** key 집합이다.

    열려 있으면 새 CLI 축이 생겨도 아무도 모른다 — 조용히 승인 밖으로 나간다.
    """
    from tools.preserve import leg_run_spec, PreserveError

    g = {"config_digest": "a" * 16, "condition_ids_sha256": "b" * 16,
         "n_conditions": 12, "discharged_cache_sha256": None, "out": "results/x"}
    f = dict(_F49, out="results/x", **{"in": "results/x"})
    with pytest.raises(PreserveError):
        leg_run_spec("L", dict(g, nproc=8), f)
    with pytest.raises(PreserveError):
        leg_run_spec("L", g, dict(f, seed=1))
    with pytest.raises(PreserveError):
        leg_run_spec("L", {k: v for k, v in g.items() if k != "out"}, f)


# ─────────────────────────────────────────────────────────────────────────────
# 48차 P0-4 — lifecycle 이 production 에 배선되지 않았다
# ─────────────────────────────────────────────────────────────────────────────

def test_finalize_does_not_fabricate_a_full_bundle(tmp_path):
    """★ 48차 P0-4 — `finalize_leg()` 이 `full_bundle` 을 **지어냈다.**

    47차는 caller 가 준 `evidence` 를 그대로 옮겨 적고 `preservation_status:
    full_bundle` 을 붙였다. 그 상태의 뜻은 "clone 한 사람이 이 결과를 검증할 수
    있는 묶음이 실재한다" 인데(계약 §8), `finalize_leg()` 은 디스크를 보지
    않았다 — 아무 dict 나 주면 원장에 완전 묶음이 생겼다.

    원장은 이 저장소에서 **증거의 정본**이다. 거기에 검증되지 않은 주장을
    쓰는 함수는 증거를 만드는 것이 아니라 증거를 오염시킨다.
    """
    import yaml
    from tools.preserve import PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    c = _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims)
    for ph in ("grid", "fit"):
        c.phase_done(ph, {"ok": True})

    # 실재하지 않는 묶음을 주장한다
    with pytest.raises(PreserveError) as ei:
        from tools.preserve import finalize_leg
        finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                           "bundle_uri": "artifacts/없는묶음",
                           "bundle_files": 26, "payload_bytes": 23863555,
                           "payload_index": "artifacts/없는묶음/payload_sha256.yaml",
                           "payload_index_sha256": "0" * 64},
                     ledger=led, claims_root=claims, token=c.token)
    assert "묶음" in str(ei.value), str(ei.value)

    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    assert not any(e["leg_id"] == "L" for e in doc.get("legs") or []), (
        "거부하면서 실행 기록을 남겼다")


def test_finalize_records_what_it_could_verify(tmp_path):
    """★ 48차 P0-4 — 묶음이 없으면 **없다고 적는다** (있는 척하지 않는다).

    묶음 없이 끝난 다리도 실행 기록은 남아야 한다 — 그것이 `running` 을
    영원히 붙들지 않게 하는 유일한 길이다. 다만 상태는 `full_bundle` 이 아니라
    검증된 만큼이다.
    """
    import yaml
    from tools.preserve import finalize_leg

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    c = _authorize("L", _RUN_SPEC_L, "0123456789abcdef", led, claims)
    for ph in ("grid", "fit"):
        c.phase_done(ph, {"ok": True})
    finalize_leg("L", {"leg_source_digest": "0123456789abcdef"},
                 ledger=led, claims_root=claims, token=c.token)

    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    rec = next(e for e in doc["legs"] if e["leg_id"] == "L")
    assert rec["preservation_status"] != "full_bundle", (
        "묶음을 확인하지 않고 full_bundle 이라고 적었다")
    # phase receipt 가 기록에 남는다 — 무엇이 실제로 돌았는지의 근거다
    assert set((rec.get("evidence") or {}).get("phases") or {}) == {"grid", "fit"}, (
        "실행 기록이 phase receipt 를 담지 않는다 — lifecycle 이 남긴 유일한 "
        "실측 증거인데 finalize 에서 버려진다")


# ─────────────────────────────────────────────────────────────────────────────
# 49차 P0-3/P0-4 — **정상 lifecycle 이 완주하지 못했다**
#
# 48차가 붙인 두 규칙은 각각 옳았지만 함께 두면 production 을 막았다:
#   · claim 을 따면 계획이 `planned → running` 으로 간다 (48차 P0-6)
#   · claim 이 이미 있으면 소유 증명 없이는 이어받을 수 없다 (48차 P0-3)
# 그런데 grid 가 딴 실행권을 **fit 에 전달할 경로가 없었다.** 그래서
# `run.sh --mode all --leg L` 은 grid 직후 fit 에서 반드시 거부된다.
# 두 규칙 사이에 **coordinator** 가 있어야 한다.
# ─────────────────────────────────────────────────────────────────────────────

def _nonsmoke(tmp_path, name="out"):
    d = tmp_path / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def test_the_normal_pipeline_runs_grid_then_fit_under_one_claim(tmp_path):
    """★ 49차 P0-3 — coordinator 가 실행권을 **한 번** 내고 끝까지 넘긴다.

    48차 실측(리뷰어 probe): grid 가 claim 을 따고 계획을 `running` 으로 옮긴
    직후, 같은 pipeline 의 fit 이 `"L 은 이미 실행 중이다"` 로 거부됐다.
    두 phase 는 별도 process 이고 attempt 를 넘길 CLI/API 경로가 없었다.
    """
    from tools.preserve import (open_leg_run, attach_leg_run, finalize_leg,
                                planned_index)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    out = _nonsmoke(tmp_path)

    # ① coordinator — 한 번만 발급하고 소유 증명을 파일로 넘긴다
    run = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                       ledger=led, claims_root=claims)
    assert planned_index(ledger=led)["L"]["status"] == "running"

    # ② grid process — 넘겨받은 증명으로 붙는다
    g = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    assert g.attempt_id == run.attempt_id, "붙었는데 다른 실행이 됐다"
    g.phase_done("grid", {"rows": 10, "out": str(out)})

    # ③ fit process — **여기가 48차에서 거부되던 지점이다**
    f = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    assert f.attempt_id == run.attempt_id
    f.phase_done("fit", {"fits": 4, "out": str(out)})

    # ④ coordinator — 같은 증명으로 닫는다
    finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                       "cohorts": ["gA"]},
                 ledger=led, claims_root=claims, token_file=tok)
    assert planned_index(ledger=led)["L"]["status"] == "executed"
    assert not tok.exists(), "닫은 뒤에도 소유 증명 파일이 남았다"


def test_a_crash_after_grid_resumes_and_finalizes(tmp_path):
    """★ 49차 P0-3 — grid 뒤 죽어도 **재계산 없이** 이어서 닫힌다.

    소유 증명이 파일에 남아 있으므로 새 process 가 같은 실행에 붙는다. 소유
    증명이 없으면 붙을 수 없다 — 그것이 두 번째 발급을 막는 유일한 장치다.
    """
    from tools.preserve import (open_leg_run, attach_leg_run, finalize_leg,
                                planned_index, PreserveError)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    run = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                       ledger=led, claims_root=claims)
    attach_leg_run("L", tok, ledger=led, claims_root=claims).phase_done(
        "grid", {"rows": 10})
    del run                                           # process 가 죽었다

    # 소유 증명 없는 제3자는 붙지 못한다
    other = tmp_path / "other.token"
    other.write_text("0" * 32, encoding="utf-8")
    with pytest.raises(PreserveError):
        attach_leg_run("L", other, ledger=led, claims_root=claims)

    r = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    assert r.phases_done() == ("grid",), "재개가 grid receipt 를 잃었다"
    r.phase_done("fit", {"fits": 4})
    finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                       "cohorts": ["gA"]},
                 ledger=led, claims_root=claims, token=r.token)
    assert planned_index(ledger=led)["L"]["status"] == "executed"


def test_the_claim_file_never_stores_the_resume_credential(tmp_path):
    """★ 49차 P0-3 — 48차 claim 파일은 재개 credential 을 **평문**으로 담았다.

    claims root 를 읽을 수 있으면 누구든 `attempt` 를 그대로 읽어 소유 증명을
    만들 수 있었다 — 즉 credential 이 곧 파일 내용이었다. 저장하는 것은
    verifier 여야 한다.
    """
    from tools.preserve import open_leg_run

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    run = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                       ledger=led, claims_root=claims)

    raw = (claims / "L.claim").read_text(encoding="utf-8")
    assert run.token not in raw, "claim 파일이 재개 credential 을 평문으로 담았다"
    assert hashlib.sha256(run.token.encode()).hexdigest() in raw, (
        "verifier 가 없다 — 그러면 소유 증명을 확인할 수 없다")


def test_the_diagnostic_reader_never_hands_out_the_credential(tmp_path):
    """★ 49차 P0-3 — 진단용 읽기는 `attempt_id` 만 준다.

    48차 `resume_claim(attempt=None)` 은 readonly claim 을 돌려주면서 그
    객체의 `.attempt` 에 **평문 credential** 을 실어 보냈다. 쓰기를 막아도
    credential 을 내주면 그 다음 호출에서 쓰기가 열린다.
    """
    from tools.preserve import open_leg_run, inspect_leg_run

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    run = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef",
                       tmp_path / "L.token", ledger=led, claims_root=claims)

    view = inspect_leg_run("L", claims_root=claims)
    assert view["attempt_id"] == run.attempt_id
    assert run.token not in json.dumps(view, ensure_ascii=False), (
        "진단 API 가 재개 credential 을 노출했다")

    # 진단용으로 연 claim 객체에서도 credential 을 **꺼낼 수 없다** — 조용히
    # `None` 을 돌려주면 그 값이 그대로 다음 호출로 흘러 들어간다.
    from tools.preserve import resume_claim

    ro = resume_claim("L", claims_root=claims)
    assert ro.readonly and ro.attempt_id == run.attempt_id
    with pytest.raises(PreserveError, match="소유 증명"):
        ro.token


def test_finalize_requires_the_owner_credential(tmp_path):
    """★ 49차 P0-3 — `finalize_leg()` 의 소유 증명은 **필수**다.

    48차 `attempt` 는 기본값 `None` 이었고, 그러면 `resume_claim()` 이 readonly
    claim 을 돌려주는데 finalize 는 그것으로도 원장을 닫았다 — 즉 이름만 알면
    남의 실행을 executed 로 닫을 수 있었다.
    """
    from tools.preserve import open_leg_run, attach_leg_run, finalize_leg

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    c = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    for ph in ("grid", "fit"):
        c.phase_done(ph, {"ok": True})

    # ★ 49차 — 타입만 보면 **다른 이유의** TypeError 가 시험을 초록으로 만든다.
    #   실측: 이 검사를 지워도 `read_token_file(None)` 안의 `Path(None)` 이
    #   TypeError 를 내서 시험이 통과했다 (변이가 안 물었다). 이유까지 본다.
    with pytest.raises(TypeError, match="소유 증명"):
        finalize_leg("L", {"leg_source_digest": "0123456789abcdef"},
                     ledger=led, claims_root=claims)
    with pytest.raises(TypeError, match="소유 증명"):        # 둘 다 준 경우도
        finalize_leg("L", {"leg_source_digest": "0123456789abcdef"},
                     ledger=led, claims_root=claims,
                     token=c.token, token_file=tok)


def test_the_precheck_tells_a_new_run_from_an_owned_resume(tmp_path):
    """★ 49차 P0-3 — shell 사전검사가 두 경우를 **구분해야** 한다.

    48차 `plan_gate()` 는 `assert_planned_leg()` 만 불렀고 그것은 `planned` 만
    통과시켰다. 그래서 grid 가 계획을 `running` 으로 옮긴 뒤 같은 pipeline 의
    fit 사전검사가 **자기 자신 때문에** 거부됐다.
    """
    from tools.preserve import open_leg_run, precheck_leg_run, PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    first = precheck_leg_run("L", "0123456789abcdef", token_file=tok,
                             ledger=led, claims_root=claims)
    assert first["kind"] == "new", first

    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    again = precheck_leg_run("L", "0123456789abcdef", token_file=tok,
                             ledger=led, claims_root=claims)
    assert again["kind"] == "resume", again

    # 소유 증명이 없으면 재개가 아니라 **두 번째 시작**이다 — 거부한다
    with pytest.raises(PreserveError):
        precheck_leg_run("L", "0123456789abcdef", token_file=None,
                         ledger=led, claims_root=claims)


# ─────────────────────────────────────────────────────────────────────────────
# 49차 P0-3 — `--dry-run` 이 계획을 `running` 에 **영구히** 남긴다
#
# 47차 P0-3 이 dry-run 면제를 없앤 것은 옳았다 (`run_grid(dry_run=True)` 는
# 최대 세 조건에 solver 를 실제로 부른다). 그런데 48차가 claim 에 원장 전이를
# 붙이면서, dry-run 은 계획을 `planned → running` 으로 옮기고 **아무 것도 닫지
# 않은 채** 끝나게 됐다. phase 가 하나도 없으므로 finalize 도 못 한다 —
# 그 다리는 다시 시작할 수도 닫을 수도 없는 terminal 상태로 굳는다.
# ─────────────────────────────────────────────────────────────────────────────

def test_a_released_run_returns_the_plan_to_planned(tmp_path):
    """★ 49차 P0-3 — 되돌릴 수 있는 실행권이 있어야 한다."""
    from tools.preserve import (open_leg_run, release_leg_run, planned_index,
                                claim_planned_leg)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    run = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                       ledger=led, claims_root=claims)
    assert planned_index(ledger=led)["L"]["status"] == "running"

    release_leg_run("L", token_file=tok, ledger=led, claims_root=claims)
    assert planned_index(ledger=led)["L"]["status"] == "planned", (
        "되돌렸는데 계획이 running 에 남았다 — 그 다리는 영영 못 돌린다")
    assert not tok.exists() and not (claims / "L.claim").exists()

    # 되돌린 뒤에는 **다시 딸 수 있다** — 그것이 되돌림의 유일한 증명이다
    claim_planned_leg("L", _RUN_SPEC_L, "0123456789abcdef",
                      ledger=led, claims_root=claims)


def test_releasing_needs_the_owner_credential(tmp_path):
    """되돌림도 소유 증명이 있어야 한다 — 남의 실행을 취소할 수 없다."""
    from tools.preserve import open_leg_run, release_leg_run, PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)

    bad = tmp_path / "bad.token"
    bad.write_text("0" * 32, encoding="utf-8")
    with pytest.raises(PreserveError):
        release_leg_run("L", token_file=bad, ledger=led, claims_root=claims)
    assert (claims / "L.claim").exists(), "틀린 증명으로 claim 이 지워졌다"


# ─────────────────────────────────────────────────────────────────────────────
# 49차 P0-4 — `no_bundle` 은 계약 §8 enum 밖이다
#
# `finalize_leg()` 은 묶음이 없으면 `preservation_status: no_bundle` 을 적는데
# 계약 §8 의 축 enum 은 `full_bundle | recorded_projection | missing` 이다.
# 즉 production lifecycle 이 원장에 쓰는 값이 **이 저장소 자신의 lint 를
# 통과하지 못한다.** 상태 어휘의 정본이 둘이면 약한 쪽이 실효 규칙이 된다.
# ─────────────────────────────────────────────────────────────────────────────

def _contract_preservation_enum() -> set:
    txt = (pathlib.Path(__file__).resolve().parents[1] / "docs" / "22p_gap"
           / "STAGE3_CONTRACT.md").read_text(encoding="utf-8")
    m = re.search(r"(?m)^preservation_status:\s*(.+)$", txt)
    assert m, "계약 §8 에 preservation_status 축 정의가 없다"
    return {v.strip() for v in m.group(1).split("|") if v.strip()}


def test_the_runtime_preservation_enum_is_inside_the_contract():
    """★ 49차 P0-4 — runtime enum ⊆ 계약 §8 enum."""
    from tools.preserve import PRESERVATION_STATUS

    outside = sorted(set(PRESERVATION_STATUS) - _contract_preservation_enum())
    assert not outside, (
        f"계약 §8 에 없는 보존 상태를 runtime 이 쓴다: {outside} — 어휘의 "
        "정본이 둘이면 원장이 자기 lint 를 통과하지 못한다")


def test_finalize_writes_a_complete_contract_status_tuple(tmp_path):
    """★ 49차 P0-4 — 묶음 없이 닫은 다리도 **계약이 정의한** 튜플을 남긴다.

    48차 기록은 `preservation_status` 하나만 적고 나머지 두 축을 비웠다.
    `test_registry_rejects_impossible_status_tuples` 는 세 축의 튜플을 계약
    허용 집합과 대조하므로, production finalize 가 쓴 기록은 그 회귀를
    통과할 수 없다.
    """
    import yaml
    from tools.preserve import open_leg_run, attach_leg_run, finalize_leg

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    c = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    for ph in ("grid", "fit"):
        c.phase_done(ph, {"ok": True})
    finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                       "cohorts": ["gA"]},
                 ledger=led, claims_root=claims, token_file=tok)

    rec = next(e for e in yaml.safe_load(led.read_text(encoding="utf-8"))["legs"]
               if e["leg_id"] == "L")
    assert rec["preservation_status"] in _contract_preservation_enum(), (
        f"계약 §8 밖의 보존 상태를 원장에 썼다: {rec['preservation_status']!r}")
    for axis in ("validation_status", "inference_role"):
        assert rec.get(axis), f"계약 §8 의 {axis} 축이 비었다 — 튜플이 불완전하다"
    assert rec["validation_status"] == "unvalidated", (
        "묶음도 검증도 없이 검증됐다고 적었다")


# ─────────────────────────────────────────────────────────────────────────────
# 49차 P0-5 — 승인 spec 이 **fit 이 실제로 하는 일**을 담지 않았다
#
# 48차 fit 축은 `{config_digest, objectives, out}` 셋뿐이었다. 그런데
# `src/fitting.py` 의 실제 F67 run_spec 은 목적함수 **순서**(warm 연쇄가 그 순서를
# 따른다) · bounds 실값 · reference · half-cell recipe(왜곡 인자) · optimizer
# 정책(method·restart·adaptive·warm) · noise 사용 여부 · 행 선택(limit/subset) ·
# 입력 위치를 전부 쓴다. 승인이 그것을 안 담으면 `--reference halfcell
# --halfcell-arg pe_offset_mv=10 --clean --no-adaptive --n-restarts 1` 로 갈아도
# 같은 digest 가 나온다 — 그러면 승인한 것은 실행이 아니라 다리 **이름**이다.
# ─────────────────────────────────────────────────────────────────────────────

_G49 = {"config_digest": "a" * 16, "condition_ids_sha256": "b" * 16,
        "n_conditions": 12, "discharged_cache_sha256": None, "out": "results/v4"}
_F49 = {"config_digest": "c" * 16,
        "objective_order": ["pocv", "pocv_dvdq"],
        "objectives_digest": "0123456789abcdef",
        "reference": "grid",
        "halfcell_recipe": {"method": "ocp", "kw": {}},
        "halfcell_cache_sha256": None,
        "base_config_digest": "e" * 16,
        "bounds_preset": "expanded",
        "bounds_digest": "d" * 16,
        "optimizer": {"method": "Nelder-Mead", "n_restarts": 5,
                      "adaptive": True, "warm_start": True},
        "use_noisy": True,
        "row_selection": {"mode": "full", "limit": None,
                          "subset_sha256": None},
        "in": "results/v4",
        "in_digest": None,
        "out": "results/v4"}


def test_the_fit_axis_seals_every_intent_that_changes_the_answer():
    """★ 49차 P0-5 — fit 쪽 승인이 실제 실행 정책을 고정한다."""
    from tools.preserve import leg_run_spec, run_spec_digest

    base = run_spec_digest(leg_run_spec("L", _G49, _F49))
    for name, ff in (
            ("목적함수 **순서**", dict(_F49, objective_order=["pocv_dvdq", "pocv"])),
            ("기준 곡선", dict(_F49, reference="halfcell")),
            ("half-cell recipe", dict(_F49, halfcell_recipe={
                "method": "ocpbias", "kw": {"pe_offset_mv": 10}})),
            ("bounds preset", dict(_F49, bounds_preset="original_33p")),
            ("bounds 실값", dict(_F49, bounds_digest="0" * 16)),
            ("optimizer", dict(_F49, optimizer=dict(
                _F49["optimizer"], n_restarts=1))),
            ("adaptive", dict(_F49, optimizer=dict(
                _F49["optimizer"], adaptive=False))),
            ("warm start", dict(_F49, optimizer=dict(
                _F49["optimizer"], warm_start=False))),
            ("noise 사용", dict(_F49, use_noisy=False)),
            ("행 선택", dict(_F49, row_selection={"mode": "limit", "limit": 8,
                                                "subset_sha256": None})),
            ("기준 캐시 바이트", dict(_F49, halfcell_cache_sha256="a" * 64)),
            ("base config", dict(_F49, base_config_digest="0" * 16)),
            ("입력 위치", dict(_F49, **{"in": "results/elsewhere"})),
            ("산출 위치", dict(_F49, out="results/elsewhere"))):
        assert run_spec_digest(leg_run_spec("L", _G49, ff)) != base, (
            f"{name} 을 바꿨는데 승인 digest 가 그대로다 — 승인이 실행을 "
            "고정하지 못한다")


def test_the_fit_axis_is_still_a_closed_key_set():
    """새 축이 생기면 여기 적히거나 거부되거나 둘 중 하나다."""
    from tools.preserve import leg_run_spec, PreserveError

    with pytest.raises(PreserveError):
        leg_run_spec("L", _G49, dict(_F49, nproc=8))
    with pytest.raises(PreserveError):
        leg_run_spec("L", _G49,
                     {k: v for k, v in _F49.items() if k != "optimizer"})


def test_the_fit_axis_pins_the_input_content_not_just_its_path(tmp_path):
    """★ 49차 P0-5 — 입력의 **내용 identity** 를 승인이 담는다.

    경로만 봉인하면 같은 이름 아래 다른 바이트가 들어와도 승인은 그대로다.
    두 경우를 타입으로 가른다:

      · `in_digest: <hex64>` — 이 다리 **밖**에서 온 입력 (F70 의 분리 producer
        구조). 계획을 적는 시점에 이미 실재하므로 사람이 그 digest 를 적는다.
      · `in_digest: null`    — 이 다리의 grid 가 만든다. 계획 시점에는 알 수
        없으므로, 런타임에 **grid phase receipt** 가 봉인한 값과 맞춘다.
    """
    from tools.preserve import (leg_run_spec, run_spec_digest,
                                LEG_SPEC_FIT_KEYS, PreserveError)

    assert "in_digest" in LEG_SPEC_FIT_KEYS, (
        "승인이 입력의 내용 identity 를 담지 않는다 — 같은 경로에 다른 바이트가 "
        "들어와도 승인이 그대로다")
    base = run_spec_digest(leg_run_spec("L", _G49, _F49))
    moved = run_spec_digest(
        leg_run_spec("L", _G49, dict(_F49, in_digest="f" * 64)))
    assert moved != base, "입력 내용을 바꿨는데 승인 digest 가 그대로다"

    with pytest.raises(PreserveError):           # hex64 도 null 도 아니다
        leg_run_spec("L", _G49, dict(_F49, in_digest="짧다"))


def test_fit_refuses_curves_that_its_grid_phase_did_not_produce(tmp_path):
    """★ 49차 P0-5 — `in_digest: null` 이면 grid phase receipt 가 정본이다.

    같은 claim 아래 grid 가 만든 곡선이 아닌 것을 fit 이 읽으면 그 다리의
    결과는 계획이 승인한 실행이 아니다. 48차에는 두 phase 를 잇는 내용
    결속이 전혀 없었다 — grid 가 무엇을 만들었든 fit 은 `--in` 이 가리키는
    아무 것이나 읽었다.
    """
    from tools.preserve import (open_leg_run, attach_leg_run,
                                assert_phase_input_binding, PreserveError)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    c = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    sealed = {"curves_sha256": "a" * 64,
              "curves_manifest_sha256": "b" * 64,
              "curves_manifest_start_sha256": "c" * 64}
    c.phase_done("grid", dict(sealed, out="results/x"))

    assert c.phase_receipt("grid")["curves_sha256"] == "a" * 64
    assert_phase_input_binding(c, dict(sealed))      # 같은 바이트 — 통과

    with pytest.raises(PreserveError) as ei:
        assert_phase_input_binding(c, dict(sealed, curves_sha256="f" * 64))
    assert "grid" in str(ei.value), str(ei.value)


def test_fit_refuses_when_its_grid_phase_is_missing(tmp_path):
    """`in_digest: null` 인데 grid receipt 가 없으면 대조할 정본이 없다 — 거부한다."""
    from tools.preserve import (open_leg_run, attach_leg_run,
                                assert_phase_input_binding, PreserveError)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    c = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    with pytest.raises(PreserveError):
        assert_phase_input_binding(c, {"curves_sha256": "a" * 64})


# ─────────────────────────────────────────────────────────────────────────────
# 49차 P0-6 — lock 순서와 finalize 의 임계 구역
#
# 48차 `finalize_leg()` 은 claim 을 **잠그지 않고** 두 번 읽었다: 한 번은
# `phases_done()` 으로 검사하고, 한 번은 원장 lock 안에서 receipt 를 옮겨 적었다.
# 그 사이에 phase 가 바뀌면 **검사한 것과 기록한 것이 다르다.** 그리고 원장
# authority 는 lock **밖에서** 한 번 보고 말았으므로, 그 뒤 cohort 가 얼어도
# 이미 통과한 finalize 는 그대로 썼다. 마지막으로 원장을 쓴 뒤 claim 을 지우기
# 전에 죽으면 그 다리는 **다시 닫을 수도 지울 수도 없는** 상태로 남았다.
# ─────────────────────────────────────────────────────────────────────────────

def _ready_claim(tmp_path):
    from tools.preserve import open_leg_run, attach_leg_run

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"
    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    c = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    for ph in ("grid", "fit"):
        c.phase_done(ph, {"ok": True})
    return led, claims, tok, c


def test_the_canonical_lock_order_is_declared_and_finalize_holds_the_claim(tmp_path):
    """★ 49차 P0-6 — finalize 는 claim lock 을 **쥐고** 원장으로 내려간다.

    잠금 순서가 한 곳에 선언돼 있어야 서로 다른 경로가 반대로 잡아 deadlock 이
    나지 않는다. 그리고 claim 을 쥐지 않으면 검사한 receipt 와 기록한 receipt 가
    다를 수 있다 (48차는 잠그지 않고 두 번 읽었다).
    """
    import threading

    from tools import preserve as P

    assert P.LOCK_ORDER == ("claim", "ledger"), (
        "정본 잠금 순서가 선언돼 있지 않다 — 두 경로가 반대로 잡으면 deadlock 이다")

    led, claims, tok, c = _ready_claim(tmp_path)
    done = threading.Event()

    def _go():
        try:
            P.finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                                 "cohorts": ["gA"]},
                           ledger=led, claims_root=claims, token_file=tok)
        finally:
            done.set()

    with P._ledger_lock(c.path):              # claim lock 을 테스트가 쥔다
        t = threading.Thread(target=_go, daemon=True)
        t.start()
        assert not done.wait(1.5), (
            "finalize 가 claim lock 을 쥐지 않고 지나갔다 — 검사한 receipt 와 "
            "기록한 receipt 가 다를 수 있다")
    t.join(timeout=30)
    assert done.is_set(), "lock 을 놓았는데 finalize 가 끝나지 않았다"
    assert P.planned_index(ledger=led)["L"]["status"] == "executed"


def test_finalize_rechecks_the_whole_authority_inside_the_ledger_lock(tmp_path):
    """★ 49차 P0-6 — 원장 lock **안에서** authority 를 다시 본다.

    48차는 `resume_claim()` 이 lock 밖에서 한 번 보고 말았다. 그 뒤 사람이
    cohort 를 얼려도 이미 통과한 finalize 는 그대로 원장을 썼다 — frozen cohort
    에 실행 기록이 새로 생긴다.

    잠금 순서(claim → 원장)를 이용해 정확히 그 창을 만든다: 원장 lock 을 테스트가
    쥐고 있으면 finalize 는 claim lock 을 잡은 채 거기서 멈춘다. 그 사이에
    원장을 바꾸고 놓아 준다.
    """
    import threading

    import yaml

    from tools import preserve as P

    led, claims, tok, c = _ready_claim(tmp_path)
    out: dict = {}

    def _go():
        try:
            P.finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                                 "cohorts": ["gA"]},
                           ledger=led, claims_root=claims, token_file=tok)
            out["rc"] = "ok"
        except Exception as e:                             # noqa: BLE001
            out["rc"] = f"{type(e).__name__}: {e}"

    with P._ledger_lock(led):
        t = threading.Thread(target=_go, daemon=True)
        t.start()
        t.join(timeout=1.5)
        assert t.is_alive(), "finalize 가 원장 lock 을 기다리지 않았다"
        doc = yaml.safe_load(led.read_text(encoding="utf-8"))
        doc["cohorts"][0]["status"] = "frozen"             # 창 안에서 얼린다
        P._atomic_write_text(led, yaml.safe_dump(doc, allow_unicode=True,
                                                 sort_keys=False))
    t.join(timeout=30)
    assert out.get("rc", "").startswith("PreserveError"), (
        f"얼어붙은 cohort 에 실행 기록을 썼다: {out.get('rc')!r}")
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    assert not any(e["leg_id"] == "L" for e in doc.get("legs") or []), (
        "거부하면서 실행 기록을 남겼다")


def test_finalize_is_idempotent_after_a_crash_before_cleanup(tmp_path):
    """★ 49차 P0-6 — 원장을 쓴 **뒤** 죽어도 다시 닫을 수 있다.

    48차는 원장 write 와 claim 삭제 사이에 죽으면 그 다리가 갇혔다: 계획은
    `executed` 라 `resume_claim()` 이 거부하고, claim 파일이 남아 있으니 새
    실행도 거부된다 — 지울 수도 닫을 수도 없다.

    복구의 근거는 **원장 자신**이다 (별도 journal 파일을 두지 않는다 — 그러면
    "닫혔다" 의 정본이 둘이 된다).
    """
    import yaml

    from tools import preserve as P

    led, claims, tok, c = _ready_claim(tmp_path)
    before = c.path.read_bytes()
    token = tok.read_text(encoding="utf-8").strip()

    P.finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                         "cohorts": ["gA"]},
                   ledger=led, claims_root=claims, token=token)
    # crash 재현 — 원장은 이미 닫혔는데 claim 파일이 살아남았다
    c.path.write_bytes(before)

    again = P.finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                                 "cohorts": ["gA"]},
                           ledger=led, claims_root=claims, token=token)
    assert again["status"] == "executed"
    assert not c.path.exists(), "복구가 남은 claim 을 치우지 않았다"
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    assert sum(1 for e in doc["legs"] if e["leg_id"] == "L") == 1, (
        "복구가 실행 기록을 두 번 적었다")


def test_the_crash_recovery_needs_the_owner_credential(tmp_path):
    """복구도 소유 증명이 필요하다 — 남의 claim 을 아무나 치울 수 없다."""
    from tools import preserve as P

    led, claims, tok, c = _ready_claim(tmp_path)
    before = c.path.read_bytes()
    token = tok.read_text(encoding="utf-8").strip()
    P.finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                         "cohorts": ["gA"]},
                   ledger=led, claims_root=claims, token=token)
    c.path.write_bytes(before)

    with pytest.raises(P.PreserveError):
        P.finalize_leg("L", {"leg_source_digest": "0123456789abcdef"},
                       ledger=led, claims_root=claims, token="0" * 32)
    assert c.path.exists(), "틀린 증명으로 claim 이 치워졌다"


# ─────────────────────────────────────────────────────────────────────────────
# 49차 — 승격 금지가 **namespace 안의 이동**까지 막아 smoke 를 반토막 냈다
#
# 48차 P0-8 은 "smoke 산출은 승격 대상이 아니다" 를 넣었다. 옳다. 그런데 판정이
# **입력만** 봤다. 그래서 smoke 자신이 `results/_smoke/x` 를
# `results/_smoke/arch/x` 로 묶는 것도 거부됐고, `scripts/smoke_e2e.sh` 의 9단계
# 이후(보관 → 격리 복원 → 검증 → 재채점)가 통째로 죽었다 — 실측: 실패 11건.
#
# 승격은 "인용되는 자리로 나가는 것" 이다. namespace **안**에 머무는 이동은
# 승격이 아니다. 그 구분이 없으면 경계가 아니라 마비다: smoke 가 검증하던
# 구간이 사라지고, 그 손실이 막은 위험보다 크다.
# ─────────────────────────────────────────────────────────────────────────────

def test_promotion_out_of_the_smoke_namespace_is_still_refused(tmp_path):
    """밖으로 나가는 것은 여전히 거부한다 (48차 P0-8 유지)."""
    from tools.preserve import (assert_not_smoke_provenance, SMOKE_NAMESPACE,
                                SMOKE_REFUSAL, PreserveError)

    src = SMOKE_NAMESPACE / "grid_fit"
    with pytest.raises(PreserveError) as ei:
        assert_not_smoke_provenance([src], "보관 묶음")
    assert SMOKE_REFUSAL in str(ei.value)

    with pytest.raises(PreserveError):            # 목적지가 밖이면 승격이다
        assert_not_smoke_provenance([src], "보관 묶음",
                                    dest="artifacts/grid_fit_v4")


def test_moving_within_the_smoke_namespace_is_not_promotion(tmp_path):
    """★ 49차 — namespace **안**의 이동은 승격이 아니다.

    smoke 는 자기 산출을 자기 namespace 안에서 묶고 복원하고 재채점한다.
    그것을 막으면 pipeline 의 뒷절반을 아무도 검사하지 않게 된다.
    """
    from tools.preserve import assert_not_smoke_provenance, SMOKE_NAMESPACE

    src = SMOKE_NAMESPACE / "grid_fit"
    assert_not_smoke_provenance([src], "보관 묶음",
                                dest=SMOKE_NAMESPACE / "arch" / "grid_fit")


def test_a_report_written_inside_the_smoke_namespace_is_not_promotion(tmp_path):
    """★ 49차 — smoke 안에 쓰는 보고서도 승격이 아니다.

    48차 `make_results.py` 는 목적지를 안 보고 입력만 봤다. 그래서 smoke 가
    자기 보고서(`results/_smoke/R_hess.md`)를 만드는 것도 거부됐고, 8단계의
    `score → hessian → report` 회귀가 죽었다 (실측). 정본 자리
    (`docs/RESULTS.md`)로 나가는 것은 그대로 거부한다.
    """
    from tools.preserve import (assert_not_smoke_provenance, SMOKE_NAMESPACE,
                                SMOKE_REFUSAL, PreserveError)

    src = SMOKE_NAMESPACE / "hess"
    assert_not_smoke_provenance([src], "보고서",
                                dest=SMOKE_NAMESPACE / "R_hess.md")
    with pytest.raises(PreserveError) as ei:
        assert_not_smoke_provenance([src], "보고서", dest="docs/RESULTS.md")
    assert SMOKE_REFUSAL in str(ei.value)


# ─────────────────────────────────────────────────────────────────────────────
# 50차 — 49차 게이트 리뷰가 실행권 lifecycle 에서 찾은 셋
#
# 49차는 "소유 증명 없이는 이어받지 못한다" 를 `resume_claim()` 에 넣었다. 그런데
# **쓰는 지점**은 그 검사를 하지 않았다. 자격을 읽기 함수에만 두면, 그 함수를
# 지나지 않고 객체를 만드는 것만으로 우회된다 — 이 저장소가 반복해서 고쳐 온
# "검사와 사용이 다른 자리에 있다" 의 또 다른 판이다.
# ─────────────────────────────────────────────────────────────────────────────

def _live_ledger(tmp_path):
    """계획 하나짜리 살아 있는 원장 + claims root."""
    return _lifecycle_ledger(tmp_path), tmp_path / "claims", tmp_path / "L.token"


def test_a_forged_claim_object_cannot_write_a_phase(tmp_path):
    """★ 50차 P0 — phase 를 **쓰는 지점**이 소유 증명을 확인한다.

    49차 반례(리뷰어 실측): claim 파일에서 공개 `attempt_id` 를 읽어
    `LegClaim(..., token="0"*32)` 를 직접 만들면 `phase_done()` 이 그대로
    기록했다. 자격 검사가 `resume_claim()` 에만 있었기 때문이다 — 생성자는
    언제든 부를 수 있으므로 읽기 함수에 둔 검사는 검사가 아니다.
    """
    import json as _j

    from tools import preserve as P

    led, claims, tok = _live_ledger(tmp_path)
    P.open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                   ledger=led, claims_root=claims)
    rec = _j.loads((claims / "L.claim").read_text(encoding="utf-8"))
    assert "attempt_verifier" in rec and rec.get("attempt_id")

    forged = P.LegClaim("L", rec["cohort_id"], rec["attempt_id"],
                        rec["run_spec_digest"], rec["source_digest"],
                        claims / "L.claim", token="0" * 32)
    with pytest.raises(P.PreserveError, match="소유 증명"):
        forged.phase_done("grid", {"공격자가": "썼다"})
    assert not (_j.loads((claims / "L.claim").read_text(encoding="utf-8"))
                .get("phases")), "거부하면서 phase 를 남겼다"


def test_a_crash_between_the_claim_and_the_token_leaves_nothing_stranded(tmp_path):
    """★ 50차 P0 — 발급 순서가 뒤집혀 있었다.

    49차 반례: `open_leg_run()` 이 claim 을 먼저 굳히고 token 을 나중에 썼다.
    그 사이에 죽으면 **아무도 갖고 있지 않은** verifier 만 남고 계획은
    `running` 이다 — 이어받을 수도, 되돌릴 수도, 닫을 수도 없다. crash 창은
    "정상 경로" 안에 있으므로 이것은 운영 사고 하나에 다리 하나를 잃는 설계다.

    순서를 뒤집으면 그 상태가 **표현 불가능**해진다: token 이 먼저 있으므로,
    claim 이 있는 모든 시점에 그 claim 의 소유 증명도 디스크에 있다.
    """
    from tools import preserve as P

    led, claims, tok = _live_ledger(tmp_path)
    boom = RuntimeError("claim 을 굳힌 직후 죽었다")
    real = P.claim_planned_leg

    def _die(*a, **k):
        real(*a, **k)                      # claim 파일을 실제로 굳히고
        raise boom                         # 그 다음 죽는다

    P.claim_planned_leg = _die
    try:
        with pytest.raises(RuntimeError):
            P.open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                           ledger=led, claims_root=claims)
    finally:
        P.claim_planned_leg = real

    # 남은 상태가 무엇이든 **회수 가능**해야 한다: claim 이 남았다면 그 소유
    # 증명도 남아 있어야 하고, 그러면 되돌릴 수 있다.
    if (claims / "L.claim").is_file():
        assert tok.is_file(), (
            "claim 은 남았는데 소유 증명이 없다 — 이어받을 수도 되돌릴 수도 "
            "닫을 수도 없는 다리가 생겼다")
        P.release_leg_run("L", token_file=tok, ledger=led, claims_root=claims)
    assert P.planned_index(ledger=led)["L"]["status"] == "planned"
    P.open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                   ledger=led, claims_root=claims)     # 다시 시작된다


def test_a_closed_run_cannot_be_resurrected_by_a_late_phase(tmp_path):
    """★ 50차 P0 — 닫힌 실행에는 아무 것도 쓸 수 없다.

    49차 반례: `finalize_leg()` 이 claim 파일을 **임계 구역 밖에서** 지웠다.
    그래서 이미 닫힌 뒤에 살아 있던 `LegClaim` 이 `phase_done()` 을 부르면
    파일이 되살아났다 — 계획은 `executed` 인데 실행 중인 claim 이 있는,
    어느 검사도 예상하지 않는 상태가 만들어진다. `release_leg_run()` 도 같다.
    """
    from tools import preserve as P

    led, claims, tok = _live_ledger(tmp_path)
    P.open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                   ledger=led, claims_root=claims)
    live = P.attach_leg_run("L", tok, ledger=led, claims_root=claims)
    for ph in ("grid", "fit"):
        live.phase_done(ph, {"ok": True})
    P.finalize_leg("L", {"leg_source_digest": "0123456789abcdef",
                         "cohorts": ["gA"]},
                   ledger=led, claims_root=claims, token_file=tok)
    assert not (claims / "L.claim").exists()

    with pytest.raises(P.PreserveError):
        live.phase_done("grid", {"늦게": "왔다"})
    assert not (claims / "L.claim").exists(), "닫힌 실행의 claim 이 부활했다"


def test_a_released_run_cannot_be_resurrected_by_a_late_phase(tmp_path):
    """되돌린 실행도 같다 — 계획은 `planned` 인데 claim 이 살아나면 안 된다."""
    from tools import preserve as P

    led, claims, tok = _live_ledger(tmp_path)
    P.open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                   ledger=led, claims_root=claims)
    live = P.attach_leg_run("L", tok, ledger=led, claims_root=claims)
    live.phase_done("grid", {"ok": True})
    P.release_leg_run("L", token_file=tok, ledger=led, claims_root=claims)

    with pytest.raises(P.PreserveError):
        live.phase_done("fit", {"늦게": "왔다"})
    assert not (claims / "L.claim").exists(), "되돌린 실행의 claim 이 부활했다"
    assert P.planned_index(ledger=led)["L"]["status"] == "planned"


# ─────────────────────────────────────────────────────────────────────────────
# 50차 P0 — 승인 축이 결과를 바꾸는 축 셋을 빠뜨렸다 (49차 반례)
#
#   · `row_selection` 이 mode/limit 만 담아 **어느 조건을 골랐는지**가 빠졌다
#   · `base_config`(재고 분배 상수)는 축 자체가 없었다
#   · half-cell 기준 캐시의 **바이트**가 빠졌다 — recipe(method+kw)만 담겼으므로
#     같은 recipe 로 만든 다른 캐시를 놓으면 승인 digest 가 그대로다
#
# 셋 다 "경로·이름은 같은데 계산이 달라진다" 형태다. 승인이 그것을 못 보면
# 승인한 A 대신 유효한 B 가 돌아도 gate 는 통과한다.
# ─────────────────────────────────────────────────────────────────────────────

def test_the_fit_axis_seals_the_row_selection_content(tmp_path):
    """어느 조건을 골랐는지가 digest 를 움직인다 (개수·모드만이 아니라)."""
    from tools.preserve import leg_run_spec, run_spec_digest, LEG_SPEC_SELECTION_KEYS

    assert "subset_sha256" in LEG_SPEC_SELECTION_KEYS, (
        "행 선택의 **내용**이 승인 밖이다 — 다른 표본으로 돌려도 같은 digest 다")
    a = dict(_F49, row_selection={"mode": "subset", "limit": None,
                                  "subset_sha256": "a" * 16})
    b = dict(_F49, row_selection={"mode": "subset", "limit": None,
                                  "subset_sha256": "b" * 16})
    assert run_spec_digest(leg_run_spec("L", _G49, a)) \
        != run_spec_digest(leg_run_spec("L", _G49, b))


@pytest.mark.parametrize("axis,alt", [
    ("base_config_digest", "0" * 16),
    ("halfcell_cache_sha256", "0" * 64),
])
def test_the_fit_axis_seals_the_input_content_axes(axis, alt):
    """★ 50차 P0 — 입력 **내용**이 승인에 들어간다.

    49차 반례: production fit 이 승인한 A 대신 교체된 유효 package B 를
    계산·게시했다. recipe·경로만 봉인하면 같은 이름 아래 다른 바이트가 들어와도
    승인이 그대로이기 때문이다.
    """
    from tools.preserve import (leg_run_spec, run_spec_digest,
                                LEG_SPEC_FIT_KEYS)

    assert axis in LEG_SPEC_FIT_KEYS, f"{axis} 가 승인 축에 없다"
    base = run_spec_digest(leg_run_spec("L", _G49, _F49))
    moved = run_spec_digest(leg_run_spec("L", _G49, dict(_F49, **{axis: alt})))
    assert moved != base, f"{axis} 를 바꿨는데 승인 digest 가 그대로다"


def test_the_grid_receipt_binds_every_curve_input_not_just_the_parquet(tmp_path):
    """★ 50차 P0 — fit 이 읽는 것은 `curves.parquet` 하나가 아니다.

    producer 기록(`curves_manifest.yaml`·`curves_manifest_start.yaml`)도 fit 이
    봉인해 읽는다. 결속이 parquet 하나만 덮으면 나머지를 갈아 끼울 수 있다.
    """
    from tools.preserve import (open_leg_run, attach_leg_run,
                                assert_phase_input_binding, PHASE_INPUT_KEYS,
                                PreserveError)

    # ★ 50차 — 이름을 **글자로** 적는다. `PHASE_INPUT_KEYS` 에서 유도하면
    #   그 상수를 좁히는 변이에 시험이 함께 좁아져 초록으로 남는다 (실측:
    #   `PHASE_INPUT_KEYS = ("curves_sha256",)` 변이가 안 물었다). 시험이
    #   대상 상수를 읽으면 그 상수를 고정하지 못한다.
    want = ("curves_sha256", "curves_manifest_sha256",
            "curves_manifest_start_sha256")
    assert set(PHASE_INPUT_KEYS) == set(want), (
        f"결속 대상이 바뀌었다: {sorted(PHASE_INPUT_KEYS)} — fit 이 읽는 입력이 "
        "늘거나 줄었다면 그 사실이 여기 보여야 한다")

    led, claims, tok = _live_ledger(tmp_path)
    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    c = attach_leg_run("L", tok, ledger=led, claims_root=claims)
    sealed = {k: f"{i}" * 64 for i, k in enumerate(want)}
    c.phase_done("grid", dict(sealed, out="results/x"))

    assert_phase_input_binding(c, dict(sealed))            # 같은 바이트 — 통과
    for k in want:
        with pytest.raises(PreserveError):
            assert_phase_input_binding(c, dict(sealed, **{k: "f" * 64}))


# ─────────────────────────────────────────────────────────────────────────────
# 51차 P0-L1 · P0-L2 · P0-L3 · P1-P — lifecycle generation 이 없다
#
# 50차는 "token 을 먼저 쓴다" 로 발급 순서를 고쳤다. 그것은 **순서**였지
# compare-and-swap 이 아니었다. 리뷰어 실측:
#   · 두 번째 정상 open 이 살아 있는 owner 의 token 을 먼저 덮는다
#   · 옛 release 의 늦은 cleanup 이 새 attempt 의 token 을 지운다
#   · stale `LegClaim` 이 새 attempt 의 claim 을 지운다
#   · 소유 증명 없는 진단 claim 으로 남의 실행을 취소할 수 있다
#   · release crash 와 post-replace fsync 오류가 회수 불가능한 orphan 을 만든다
#   · caller 가 준 token 경로가 claim authority 경로와 alias 될 수 있다
#
# 공통 원인 하나: **자격 검사와 쓰기가 같은 임계 구역에 없고, 쓰기가 자기가
# 쓴 generation 인지 확인하지 않는다.**
# ─────────────────────────────────────────────────────────────────────────────

def test_a_second_open_never_touches_the_live_owners_token(tmp_path):
    """★ 51차 P0-L1 — 중복 발급이 정상 owner 의 소유 증명을 파괴하면 안 된다.

    리뷰어 반례: A 를 정상 발급한 뒤 같은 public 함수를 같은 token 경로로 다시
    부르면, B 는 계획 대조로 거부되기 **전에** token 파일을 자기 것으로 덮는다.
    거부된 뒤 rollback 은 "claim 이 있다" 는 이유로 B 의 token 을 남긴다.
    결과: claim 의 verifier 는 A, 파일은 B → A 도 이어갈 수 없다.
    """
    from tools.preserve import (open_leg_run, attach_leg_run, release_leg_run,
                                finalize_leg, read_token_file, PreserveError)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    a = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                     ledger=led, claims_root=claims)
    mine = read_token_file(tok)

    with pytest.raises(PreserveError):
        open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                     ledger=led, claims_root=claims)

    assert read_token_file(tok) == mine, (
        "두 번째 발급이 살아 있는 owner 의 소유 증명을 덮었다")
    # 그리고 A 는 여전히 붙고·닫고·되돌릴 수 있다
    assert attach_leg_run("L", tok, ledger=led,
                          claims_root=claims).attempt_id == a.attempt_id
    release_leg_run("L", token_file=tok, ledger=led, claims_root=claims)


def test_a_late_release_cleanup_cannot_delete_the_next_attempts_token(tmp_path):
    """★ 51차 P0-L2 — token 삭제는 **자기가 쓴 generation** 에만 적용된다.

    리뷰어 반례: release A 가 claim·원장을 되돌린 뒤 token unlink 직전에 멈춘다.
    정상 B 가 같은 다리를 다시 열어 B 의 token 을 쓴다. 그 뒤 A 가 재개하면
    A 의 unlink 가 **B 의** 소유 증명을 지운다.
    """
    from tools.preserve import (open_leg_run, attach_leg_run, read_token_file,
                                _unlink_token_generation)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    stale = read_token_file(tok)                      # A 의 소유 증명
    from tools.preserve import release_leg_run
    release_leg_run("L", token=stale, ledger=led, claims_root=claims)

    b = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                     ledger=led, claims_root=claims)
    # ── 여기서 A 의 늦은 cleanup 이 재개한다 ──
    _unlink_token_generation(tok, stale)

    assert tok.is_file(), "옛 release 의 cleanup 이 새 attempt 의 token 을 지웠다"
    assert attach_leg_run("L", tok, ledger=led,
                          claims_root=claims).attempt_id == b.attempt_id


def test_a_stale_claim_handle_cannot_cancel_the_next_attempt(tmp_path):
    """★ 51차 P0-L2 — mutator 가 **쓰기 지점에서** live attempt 를 다시 본다.

    리뷰어 반례: release R1 이 `resume_claim()` 으로 A 를 검증한 뒤 멈춘다.
    그 사이 A 가 정상 release 되고 B 가 열린다. R1 이 재개해 stale
    `LegClaim(A)` 로 `_abandon_claim()` 을 부르면 **B 의** claim 이 지워지고
    원장도 planned 로 돌아간다.
    """
    from tools.preserve import (open_leg_run, release_leg_run, resume_claim,
                                _abandon_claim, planned_index, _claim_path,
                                read_token_file, PreserveError)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    ta = read_token_file(tok)
    stale = resume_claim("L", claims_root=claims, token=ta, ledger=led)

    release_leg_run("L", token=ta, ledger=led, claims_root=claims)
    b = open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                     ledger=led, claims_root=claims)

    with pytest.raises(PreserveError):
        _abandon_claim(stale, ledger=led)

    assert _claim_path("L", claims).is_file(), (
        "stale handle 이 새 attempt 의 claim 을 지웠다")
    assert planned_index(ledger=led)["L"]["status"] == "running"
    assert resume_claim("L", claims_root=claims, token=read_token_file(tok),
                        ledger=led).attempt_id == b.attempt_id


def test_a_readonly_claim_cannot_abandon_the_live_owner(tmp_path):
    """★ 51차 P0-L2 — 소유 증명 없는 진단 handle 은 **쓰기 경로에 못 들어간다**.

    리뷰어 반례: 공개 진단 필드와 claim 경로만으로 `LegClaim(..., token=None)`
    을 만들어 `_abandon_claim()` 에 주면 실제 owner 가 취소된다. 50차가
    `phase_done()` 에 넣은 verifier 검사는 이 쓰기 경로에는 없었다.
    """
    from tools.preserve import (open_leg_run, inspect_leg_run, LegClaim,
                                _abandon_claim, _claim_path, planned_index,
                                PreserveError)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    pub = inspect_leg_run("L", claims_root=claims)
    forged = LegClaim(pub["leg_id"], pub["cohort_id"], pub["attempt_id"],
                      pub["run_spec_digest"], pub["source_digest"],
                      _claim_path("L", claims), token=None)

    with pytest.raises(PreserveError):
        _abandon_claim(forged, ledger=led)

    assert _claim_path("L", claims).is_file(), "위조 handle 이 owner 를 취소했다"
    assert planned_index(ledger=led)["L"]["status"] == "running"


def test_a_crash_inside_release_leaves_a_recoverable_state(tmp_path):
    """★ 51차 P0-L3 — release 중 crash 가 **회수 불가능한 orphan** 을 만들면 안 된다.

    리뷰어 반례: `_abandon_claim()` 이 claim 을 먼저 지우고 원장 전이를 나중에
    한다. 그 사이 죽으면 claim 은 없고 계획은 `running` 이라 새 발급도
    (`planned` 아님) 재개도 (claim 없음) 되돌림도 안 된다.

    두 순서 중 **회수 가능한 쪽**은 원장 먼저다: claim 이 남고 계획이 `planned`
    면 소유 증명으로 그냥 다시 되돌리면 된다.
    """
    from tools.preserve import (open_leg_run, release_leg_run, _claim_path,
                                planned_index, read_token_file, precheck_leg_run)

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                 ledger=led, claims_root=claims)
    token = read_token_file(tok)

    # release 의 두 쓰기 **사이**에서 죽는다 — 원장 전이를 굳히는 순간
    import tools.preserve as P

    class _Boom(BaseException):
        pass

    with mock.patch.object(P, "_atomic_write_text",
                           side_effect=_Boom("crash between the two writes")):
        with pytest.raises(_Boom):
            release_leg_run("L", token=token, ledger=led, claims_root=claims)

    # 회수 가능해야 한다: 같은 소유 증명으로 다시 되돌린다
    assert _claim_path("L", claims).is_file()
    release_leg_run("L", token=token, ledger=led, claims_root=claims)
    assert planned_index(ledger=led)["L"]["status"] == "planned"
    assert not _claim_path("L", claims).is_file()
    assert precheck_leg_run("L", "0123456789abcdef",
                            ledger=led, claims_root=claims)["kind"] == "new"


def test_a_durability_error_after_the_ledger_commit_keeps_the_claim(tmp_path):
    """★ 51차 P0-L3 — `os.replace` **뒤**의 오류는 미커밋이 아니다.

    리뷰어 반례: `_atomic_write_text()` 가 새 `running` 원장을 `os.replace` 한
    뒤 parent fsync 에서 오류를 보고하면 새 값은 이미 보인다. 그런데 caller 는
    전부 미커밋으로 보고 claim 을 지우고 token 도 지운다 → 계획은 `running`,
    소유자는 없음. 회수 불가.

    rollback 은 같은 lock 아래 **실제 상태를 다시 읽고** 결정해야 한다.
    """
    import tools.preserve as P

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    tok = tmp_path / "L.token"

    real_fsync = os.fsync
    state = {"replaced": False}
    real_replace = os.replace

    def _replace(a, b, *args, **kw):
        r = real_replace(a, b, *args, **kw)
        if str(b) == str(led):
            state["replaced"] = True
        return r

    def _fsync(fd):
        if state["replaced"]:
            state["replaced"] = False
            raise OSError(5, "parent fsync failure after os.replace")
        return real_fsync(fd)

    with mock.patch.object(os, "replace", _replace), \
         mock.patch.object(os, "fsync", _fsync):
        with pytest.raises(OSError):
            P.open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", tok,
                           ledger=led, claims_root=claims)

    # 원장이 이미 running 이면 claim 과 token 은 살아 있어야 한다
    if P.planned_index(ledger=led)["L"]["status"] == "running":
        assert P._claim_path("L", claims).is_file(), (
            "커밋된 전이인데 claim 을 지웠다 — 회수 불가능한 running orphan")
        assert tok.is_file(), "커밋된 전이인데 소유 증명을 지웠다"
        P.release_leg_run("L", token_file=tok, ledger=led, claims_root=claims)
    assert P.planned_index(ledger=led)["L"]["status"] == "planned"


def test_the_token_path_cannot_alias_the_claim_authority(tmp_path):
    """★ 51차 P1-P — caller 가 준 token 경로가 claim·원장 namespace 와 겹치면 거부.

    리뷰어 반례: `token_file == claims_root/L.claim` 이면 token-first 쓰기가
    claim authority 경로를 먼저 점유한다. claim 발급은 `O_EXCL` 에서 실패하지만
    rollback 은 "경로가 있다" 는 이유로 token 문자열을 남긴다. 그 뒤 모든 claim
    reader 가 malformed JSON 을 만나고 정상 cleanup 도 막힌다.
    """
    from tools.preserve import open_leg_run, _claim_path, PreserveError

    led = _lifecycle_ledger(tmp_path)
    claims = tmp_path / "claims"
    for alias in (_claim_path("L", claims),
                  Path(str(_claim_path("L", claims)) + ".lock"),
                  led, Path(str(led) + ".lock")):
        with pytest.raises(PreserveError):
            open_leg_run("L", _RUN_SPEC_L, "0123456789abcdef", alias,
                         ledger=led, claims_root=claims)
        assert not _claim_path("L", claims).is_file()
