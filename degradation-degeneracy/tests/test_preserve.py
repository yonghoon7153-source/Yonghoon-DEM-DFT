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
import shutil
import tempfile
from pathlib import Path

import pytest

from tools.preserve import (FAULTS, CasBackend, Hooks, PlannedLeg, PreserveError,
                            canonical_bytes, digest, finalize_only, index_entries,
                            is_registered, load_canonical, publish, restore_from_cas,
                            run_transaction, seal_payload, verify_payload,
                            verify_registered_receipt, check_receipt,
                            check_manifest, load_canonical,
                            assert_durable_retention, has_registration_journal,
                            check_envelope, check_output, check_output_claim, check_hook_validation,
                            pin_set_digest, ENFORCEMENT_OBJECT_LOCK,
                            MIN_RETENTION_DAYS)
from tools.preserve import _is_hex64 as _is_hex64_str

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

    def read_pinned(self, leg_id, dg):
        data = super().read_pinned(leg_id, dg)
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

run_transaction(planned, run, backend, index,
                Hooks(validate=validate, rescore=rescore,
                      min_retention_days=365,
                      expected_semantic=hashlib.sha256(data).hexdigest()))
'''


@pytest.mark.parametrize("stage", ["after_pin", "after_publish"])
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
    if has_registration_journal(index, "crashleg"):
        assert is_registered(index, "crashleg", backend), (
            "journal 은 남았는데 graph 를 회수할 수 없다")
    else:
        assert not is_registered(index, "crashleg", backend)

    # 그리고 재개는 **재계산 없이** 끝나야 한다 (hooks 를 받지 않는다)
    if index_entries(index):
        out = finalize_only("crashleg", backend, index)
        assert out["ok"] and is_registered(index, "crashleg", backend)


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
