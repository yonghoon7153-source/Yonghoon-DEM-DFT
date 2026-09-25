"""71차 게이트 (E3-R · E6 문구) — 영수증 소비자가 **PASS 주장을 읽지 말고 결과를 대조**해야 한다.

리뷰어(71차 §2, `READER_CHECKS.json` R04~R10)가 실물 영수증을 소유 복사본에서 변형하고 core sha 를 다시
맞춰 원래 `read_verification_receipt` 본문에 넣었다 — 생산자 `make_receipt._outputs_agree` 가 거부하는
입력을 소비자가 **수용**했다:

    R04 sealed_summary 제거 (outputs_agree=True 유지)      → reader 수용 · 생산자 거부 (짝 없음)
    R05 두 summary 의 semantic SHA 불일치 (True 유지)       → reader 수용 · 생산자 거부 (불일치)
    R06 rescored.source_file_sha256 ≠ bundle.fits_sha256    → reader 수용
    R07 restore.run_dir_relative = results/ANOTHER_RUN      → reader 수용
    R08 semantic_sha256 가 hex 가 아님                      → reader 수용
    R09 source_file_sha256 필드 제거                        → reader 수용
    R10 identity 값 null                                    → reader 수용 (넓은 typed 표현의 한계)

원인: 소비자가 `outputs_agree` 한 필드와 "비어 있지 않은 문자열" 만 봤고, 정상 fixture 자체가 산출 하나에
`outputs_agree=True` 를 얹은 — 생산자가 만들 수 없는 — 영수증이었다 (fixture 가 진실을 가리고 있었다, 규율 2).
여기의 fixture 는 생산 계약(두 산출 · 같은 semantic · source fits = bundle fits · 복원 지도) 그대로다.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import tools.preserve as P                                      # noqa: E402
from tests.test_gate70_defensive import (_fixture_repo, _production_outputs,   # noqa: E402
                                         _receipt_core, _sha, _write_receipt)

_REAL_LEDGER = REPO / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"


def _attach(root, led, rp):
    return P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)


def _refused(root, led, rp, why: str):
    before = led.read_bytes()
    with pytest.raises(P.PreserveError) as ei:
        _attach(root, led, rp)
    assert why in str(ei.value), str(ei.value)
    assert led.read_bytes() == before, "거부하면서 원장을 건드렸다"


# ── 양성: 생산 계약 그대로의 영수증은 올라간다 ───────────────────────────────
def test_g71_e3r_00_a_production_contract_receipt_is_consumed(tmp_path):
    root, led, ev = _fixture_repo(tmp_path)
    rp = _write_receipt(root, "L", _receipt_core(root, "L", ev))
    r = _attach(root, led, rp)
    assert r["preservation_status"] == "full_bundle"
    leg = yaml.safe_load(led.read_text(encoding="utf-8"))["legs"][0]
    assert leg["validation_status"] == "current_validated"
    assert leg["evidence"]["rescored_from_restored_fits"] is True


# ── R04 · R05: 비교 쌍과 실제 일치 ──────────────────────────────────────────
def test_g71_e3r_04_a_receipt_without_the_sealed_summary_pair_is_refused(tmp_path):
    """★ R04 — 산출이 하나뿐이면 '일치' 가 아니라 **비교 불가**다 (생산자 27차 P1-6 그대로)."""
    root, led, ev = _fixture_repo(tmp_path)
    core = _receipt_core(root, "L", ev)
    core["outputs"] = [o for o in core["outputs"] if o["role"] != "sealed_summary"]
    core["outputs_agree"] = True                       # 주장은 그대로 — 주장을 읽지 않는다
    _refused(root, led, _write_receipt(root, "L", core), "sealed_summary")


def test_g71_e3r_05_a_disagreeing_semantic_pair_is_refused_even_if_it_claims_agreement(tmp_path):
    """★ R05 — `outputs_agree=True` 는 주장이다. 두 semantic digest 를 **다시 비교**한다."""
    root, led, ev = _fixture_repo(tmp_path)
    core = _receipt_core(root, "L", ev, outputs=_production_outputs(root, ev, sem_sealed="c" * 64))
    core["outputs_agree"] = True
    _refused(root, led, _write_receipt(root, "L", core), "semantic")


def test_g71_e3r_05b_duplicate_roles_are_not_a_pair(tmp_path):
    """같은 역할 둘(rescored 둘)은 짝이 아니다 — 역할마다 정확히 하나."""
    root, led, ev = _fixture_repo(tmp_path)
    outs = _production_outputs(root, ev)
    core = _receipt_core(root, "L", ev, outputs=[outs[0], dict(outs[0])])
    _refused(root, led, _write_receipt(root, "L", core), "sealed_summary")


# ── R06 · R09: source fits 결속 ──────────────────────────────────────────────
def test_g71_e3r_06_rescored_source_fits_must_equal_the_bundle_fits(tmp_path):
    """★ R06 — 재채점이 읽은 fits 가 묶음의 fits 가 아니면 그 재채점은 이 묶음의 검증이 아니다."""
    root, led, ev = _fixture_repo(tmp_path)
    core = _receipt_core(root, "L", ev, outputs=_production_outputs(root, ev, source_fits="d" * 64))
    _refused(root, led, _write_receipt(root, "L", core), "source_file_sha256")


def test_g71_e3r_09_a_rescored_output_without_source_fits_is_refused(tmp_path):
    """★ R09 — 필드가 없으면 결속이 없다. 닫힌 키 집합."""
    root, led, ev = _fixture_repo(tmp_path)
    outs = _production_outputs(root, ev)
    del outs[0]["source_file_sha256"]
    core = _receipt_core(root, "L", ev, outputs=outs)
    _refused(root, led, _write_receipt(root, "L", core), "키 집합")


# ── R07: 복원 경로 ↔ 묶음의 복원 지도 ↔ 원장의 실행 자리 ───────────────────────
def test_g71_e3r_07_a_receipt_restored_into_another_run_dir_is_refused(tmp_path):
    """★ R07 — 영수증이 말하는 복원 자리가 묶음의 `restore_map.yaml` 과 다르면 다른 실행의 영수증이다."""
    root, led, ev = _fixture_repo(tmp_path)
    core = _receipt_core(root, "L", ev, run_dir_relative="results/ANOTHER_RUN")
    _refused(root, led, _write_receipt(root, "L", core), "run_dir")


def test_g71_e3r_07b_the_ledger_run_location_must_match_the_receipt(tmp_path):
    """원장 evidence.out (finalize 가 적은 실행 자리) 과도 맞아야 한다 — 다른 실행 기록에 묶음을 붙이지 않는다."""
    root, led, ev = _fixture_repo(tmp_path)
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    doc["legs"][0]["evidence"]["out"] = "results/OTHER"
    led.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    rp = _write_receipt(root, "L", _receipt_core(root, "L", ev))
    _refused(root, led, rp, "evidence.out")


def test_g71_e3r_07c_a_bundle_without_a_restore_map_cannot_bind_the_run(tmp_path):
    root, led, ev0 = _fixture_repo(tmp_path)
    (root / "artifacts" / "L" / "restore_map.yaml").unlink()
    # index 도 그에 맞춰 다시 (index 불일치로 먼저 죽지 않게 — 재는 것은 복원 지도 결속이다)
    d = root / "artifacts" / "L"
    idx = d / "payload_sha256.yaml"
    idx.write_text(yaml.safe_dump({n: _sha((d / n).read_bytes())
                                   for n in ("fits.parquet", "manifest.yaml", "degeneracy_summary.yaml")}),
                   encoding="utf-8")
    files = [x for x in sorted(d.rglob("*")) if x.is_file()]
    ev = dict(ev0, bundle_files=len(files), payload_bytes=sum(x.stat().st_size for x in files),
              payload_index_sha256=_sha(idx.read_bytes()))
    _refused(root, led, _write_receipt(root, "L", _receipt_core(root, "L", ev)), "restore_map")


# ── 봉인 summary 의 파일 identity 가 묶음 구성원과 같은가 ───────────────────────
def test_g71_e3r_11_the_sealed_summary_in_the_receipt_must_be_the_bundle_member(tmp_path):
    root, led, ev = _fixture_repo(tmp_path)
    outs = _production_outputs(root, ev)
    outs[1]["file_sha256"] = "e" * 64
    _refused(root, led, _write_receipt(root, "L", _receipt_core(root, "L", ev, outputs=outs)), "degeneracy_summary.yaml")


# ── R08 · R10: typed 값 ────────────────────────────────────────────────────────
def test_g71_e3r_08_non_hex_semantic_digests_are_refused(tmp_path):
    root, led, ev = _fixture_repo(tmp_path)
    outs = _production_outputs(root, ev, sem_rescored="not-a-digest", sem_sealed="not-a-digest")
    _refused(root, led, _write_receipt(root, "L", _receipt_core(root, "L", ev, outputs=outs)), "hex64")


def test_g71_e3r_10_null_identity_values_are_refused(tmp_path):
    root, led, ev = _fixture_repo(tmp_path)
    core = _receipt_core(root, "L", ev)
    core["identity"]["src_io_sha256"] = None
    _refused(root, led, _write_receipt(root, "L", core), "identity")


# ── 실물 양성 (읽기 전용) ─────────────────────────────────────────────────────
def test_g71_e3r_12_the_real_receipt_satisfies_the_production_contract_checks():
    """실물 `paired_fixed5_v4.validate.yaml` — 두 산출 · 같은 semantic · source fits = bundle fits · 복원 지도 일치."""
    doc = yaml.safe_load(_REAL_LEDGER.read_text(encoding="utf-8"))
    for e in doc["legs"]:
        if e.get("preservation_status") != "full_bundle":
            continue
        core = P.read_verification_receipt(e["evidence"]["verification_receipt"], e["leg_id"], repo_root=REPO)
        pair = P._receipt_output_pair(core)
        assert pair["rescored_summary"]["source_file_sha256"] == core["bundle"]["fits_sha256"]
        P._assert_receipt_bound_to_bundle(core, REPO / core["bundle"]["uri"], e["leg_id"])


# ── E6 문구: 격리 tree 는 requirements*.txt 까지 담아 source_digest 가 같다 ──────
def test_g71_e6_the_isolated_tree_has_the_same_source_digest_as_the_checkout():
    """리뷰어 §3: "격리 tree 는 root requirements*.txt 를 복사하지 않으므로 source_digest 동일 주장은 성립하지
    않는다" → 복사하고 **자식 프로세스로** 잰다 (in-process 값과 같은 함수를 격리 tree 의 위치에서)."""
    from tests.conftest import isolated_tree
    tree = isolated_tree()
    assert sorted(p.name for p in tree.glob("requirements*.txt")) == \
        sorted(p.name for p in REPO.glob("requirements*.txt"))
    from src.io import source_digest
    got = subprocess.run([sys.executable, "-c", "from src.io import source_digest; print(source_digest())"],
                         cwd=tree, capture_output=True, text=True, check=True).stdout.strip()
    assert got == source_digest(), (got, source_digest())
