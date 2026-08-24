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

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from tools.preserve import (FAULTS, CasBackend, Hooks, PlannedLeg, PreserveError,
                            canonical_bytes, digest, index_entries, publish,
                            run_transaction, seal_payload, verify_payload)

PLANNED = PlannedLeg(
    leg_id="hc22p_v6_armA_b20",
    protocol_generation="v6",
    design_id="p22_halfcell_2x2_v6",
    source_digest="deadbeefcafe0001",
    objectives=("pocv_dvdq", "pocv_dvdq_dqdv"),
    total_start_budget=20,
    candidate_mode="legacy_slot_replace",
)


def _make_run(tmp: Path) -> Path:
    """작은 hermetic run_dir. 실제 fits 를 흉내만 낸다."""
    d = tmp / "run"
    (d / "_inputs").mkdir(parents=True)
    (d / "fits.parquet").write_bytes(b"PAR1" + b"\x11" * 512 + b"PAR1")
    (d / "manifest.yaml").write_text("leg: hc22p_v6_armA_b20\n", encoding="utf-8")
    (d / "_inputs" / "base.yaml").write_text("noise: 0.001\n", encoding="utf-8")
    (d / "run_spec.json").write_text(json.dumps({
        "planned_id": PLANNED.planned_id(),
        "source_digest": PLANNED.source_digest,
    }), encoding="utf-8")
    return d


def _hooks(expected: str | None = None) -> Hooks:
    def restore(man, src_dir, dst_root):
        for m in man["members"]:
            src, dst = Path(src_dir) / m["path"], Path(dst_root) / m["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    def validate(root):
        # 복원본 **안에서만** 읽는다. 원본 경로를 보면 이 검증은 거짓말이 된다.
        need = ["fits.parquet", "manifest.yaml", "_inputs/base.yaml"]
        miss = [n for n in need if not (Path(root) / n).is_file()]
        return {"ok": not miss, "fail": miss, "checks": {n: True for n in need}}

    def rescore(root):
        data = (Path(root) / "fits.parquet").read_bytes()
        return {"role": "rescored_summary",
                "canonicalizer": "score-semantic/v1",
                "semantic_sha256": hashlib.sha256(data).hexdigest()}

    return Hooks(validate=validate, rescore=rescore, restore=restore,
                 min_retention_days=365, expected_semantic=expected)


@pytest.fixture()
def kit(tmp_path):
    run = _make_run(tmp_path)
    backend = CasBackend(root=tmp_path / "cas")
    index = tmp_path / "bundle_index.yaml"
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
                        "receipt_digest": "x", "payload_root_digest": "y",
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
    expected = None
    if fault == "wrong_semantic_digest":
        expected = hashlib.sha256(
            (run / "fits.parquet").read_bytes()).hexdigest()
    with pytest.raises(PreserveError) as ei:
        run_transaction(PLANNED, run, backend, index, _hooks(expected),
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
    # 재시도로 닫힌다
    assert run_transaction(PLANNED, run, backend, index, _hooks())["ok"]


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
                        Hooks(validate=None, rescore=None, restore=None))
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
    covered = {f for f, _ in _FAULT_STAGE} | {"crash_after_publish"}
    missing = sorted(FAULTS - covered)
    assert not missing, f"회귀가 없는 fault: {missing}"
    stray = sorted(covered - FAULTS)
    assert not stray, f"`FAULTS` 에 없는 이름을 검사한다: {stray}"
