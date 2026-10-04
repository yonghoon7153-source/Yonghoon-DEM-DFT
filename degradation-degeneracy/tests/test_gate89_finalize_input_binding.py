"""89차 — G88-N1 한정 보완: fit 전용 최종화가 원장에 옮길 receipt 의 입력 결속을 다시 검사한다 (고정 표
`STAGE3_IMPL_ROUND1_SPEC.md` §15 · 원장 §132).

88차 리뷰어 G88-N1 (P1): `phase_done` 은 기록 때 `_assert_external_input_binding` 으로 fit receipt 의 `inputs` (닫힌 키 · hex64 ·
묶음 재계산) 를 검사하지만, `finalize_leg` 의 fit 전용 분기는 `consumed.external_input` · 계획 `fit.in_digest` · receipt
`input_package_digest` 세 문자열만 비교한다. 그래서 기록 **뒤** 저장 claim 의 `phases.fit.receipt.inputs` 만 지우거나 바꾸면 세
문자열이 그대로라 그 snapshot 이 `executed` 기록으로 옮겨진다. 88차 시험은 `phase_done` 에 처음 주는 receipt (f03_02 · f03_06
inputs 둘) 와 최종화의 문자열 대조 (f03_03 · f03_06 receipt package) 를 따로 묶었다 — 그 사이가 빈칸이었다.

§15 계약: 최종화는 위에서 한 번 읽은 snapshot 의 fit receipt 에 같은 공통 검사를 **기존 세 비교 뒤 · 원장 · claim 변경 전**에
적용한다. node: d01 양성 (durable receipt 가 그대로 원장으로) · d02 음성 넷 (실제 `finalize_leg` 거부 · 결속 이유 · 원장 · claim
바이트 불변) · d03 대조 (새 검사를 통과하는 자기일관 위조는 기존 receipt ↔ consumed 비교가 잡는다 — 그 비교가 G88-N1 뒤에도
필요하다). v2 대조는 88차 f00_05 가 한다 (v2 fit receipt 에 `inputs` 없음 → executed). RED 에서 d02 넷만 빨개야 한다 — d01 · d03 은
처음부터 GREEN 이어야 하는 대조다. scratch 이름은 `g89_` 접두 (88차 · 87차 모듈의 고정 경로와 겹치지 않는다 — 그래도 같은 모듈을
동시에 두 번 돌리는 것은 안전하지 않다 · 88차 §6-f).
"""
from __future__ import annotations

import json

import pytest

from tests import test_gate88_fit_only_lifecycle as G88
from tools import preserve as PV

LEG = G88.LEG
SRC = G88.SRC
EVIDENCE = G88.EVIDENCE


def _rewrite_claim(c, change) -> None:
    """저장된 claim 을 읽어 `change(rec)` 로 바꾼 뒤 같은 정규형으로 다시 쓴다 (durable state 변조 — 88차 f03_03 · f03_06 과 같은 꼴)."""
    rec = json.loads(c.path.read_text(encoding="utf-8"))
    change(rec)
    c.path.write_text(json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")


def _other_hex64(v: str) -> str:
    """같은 길이 · 다른 값의 유효 hex64 (첫 글자만 바꾼다)."""
    return ("1" if v[0] == "0" else "0") + v[1:]


# ─────────────────────────────────────────────────────────────────────────────
# d01 — 양성 (처음부터 GREEN: 정상 durable receipt 는 그대로 닫힌다)
# ─────────────────────────────────────────────────────────────────────────────
def test_d01_a_durable_fit_receipt_is_carried_into_the_ledger_record_as_recorded(tmp_path, monkeypatch):
    """기록한 receipt 를 재개 (token) 뒤 최종화하면 executed 이고, 원장 기록의 fit receipt 는 claim 에 기록된 것 그대로다 (`inputs` 포함)."""
    out, led, in_dir, ctx, spec, ind = G88._v3_setup(tmp_path, monkeypatch, "g89_d01")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    token = c.token
    r = G88._fit_receipt(in_dir)
    c.phase_done("fit", r)
    stored = json.loads(c.path.read_text(encoding="utf-8"))["phases"]["fit"]["receipt"]
    del c                                                     # 실행이 죽었다 — durable 기록만 남는다
    assert PV.resume_claim(LEG, token=token, ledger=led).phases_done() == ("fit",)
    assert G88._finalize_ok(led, token=token)["status"] == "executed"
    got = G88._leg_record(led)["evidence"]["phases"]["fit"]["receipt"]
    assert got == stored, "원장에 옮긴 fit receipt 가 claim 에 기록된 것과 다르다"
    assert got["inputs"] == r["inputs"] and got["input_package_digest"] == r["input_package_digest"], \
        "원장에 옮긴 fit receipt 의 입력 결속이 기록한 값과 다르다"


# ─────────────────────────────────────────────────────────────────────────────
# d02 — 음성 (G88-N1: 기록 뒤 바뀐 inputs 를 최종화가 소비하면 안 된다)
# ─────────────────────────────────────────────────────────────────────────────
#: 바꾸는 법 → 기대 거부 이유 (`_assert_external_input_binding` 의 문장 — 키 닫힘 · hex64 는 "`inputs` 가" · 재계산 불일치는 "자기모순").
_D02 = {
    "inputs_deleted": (lambda r: r.pop("inputs"), "`inputs` 가"),
    "inputs_value_other_hex64": (
        lambda r: r["inputs"].__setitem__("curves_sha256", _other_hex64(r["inputs"]["curves_sha256"])), "자기모순"),
    "inputs_extra_key": (lambda r: r["inputs"].__setitem__("extra_sha256", "ab" * 32), "`inputs` 가"),
    "inputs_value_not_hex": (lambda r: r["inputs"].__setitem__("curves_sha256", "zz" * 32), "`inputs` 가"),
}


@pytest.mark.parametrize("how", sorted(_D02))
def test_d02_finalize_refuses_a_fit_receipt_whose_inputs_changed_after_recording(tmp_path, monkeypatch, how):
    """G88-N1 — `phase_done` 뒤 저장 claim 의 `phases.fit.receipt.inputs` 만 바꾼다 (`input_package_digest` · `consumed` · 계획은
    그대로 — 세 문자열 비교는 통과한다). 실제 `finalize_leg` 가 결속 이유로 거부하고 원장 · claim 바이트를 바꾸지 않는다."""
    change, why = _D02[how]
    out, led, in_dir, ctx, spec, ind = G88._v3_setup(tmp_path, monkeypatch, f"g89_d02_{how}")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    c.phase_done("fit", G88._fit_receipt(in_dir))
    _rewrite_claim(c, lambda rec: change(rec["phases"]["fit"]["receipt"]))
    led_before, claim_before = led.read_bytes(), c.path.read_bytes()
    with pytest.raises(PV.PreserveError) as ei:
        PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, token=c.token)
    assert why in str(ei.value), "거부 이유가 receipt 의 입력 결속 (키 닫힘 · hex64 · 묶음 재계산) 이 아니다"
    assert led.read_bytes() == led_before, "거부했는데 원장 바이트가 바뀌었다"
    assert c.path.read_bytes() == claim_before, "거부했는데 claim 파일 바이트가 바뀌었다"


# ─────────────────────────────────────────────────────────────────────────────
# d03 — 대조 (처음부터 GREEN: 기존 receipt ↔ consumed 비교가 여전히 필요하다)
# ─────────────────────────────────────────────────────────────────────────────
def test_d03_a_self_consistent_receipt_forgery_after_recording_is_refused_by_the_consumer_binding(tmp_path, monkeypatch):
    """기록 뒤 `inputs` 값 하나와 `input_package_digest` 를 **함께** (자기일관하게) 바꾸면 새 공통 검사는 통과한다. 그 위조는 기존
    receipt 묶음 ↔ `consumed.external_input` 비교가 잡는다 (이유 "소비한 밖 입력") — G88-N1 뒤에도 그 비교가 필요하다는 고정."""
    out, led, in_dir, ctx, spec, ind = G88._v3_setup(tmp_path, monkeypatch, "g89_d03")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    c.phase_done("fit", G88._fit_receipt(in_dir))

    def forge(rec):
        r = rec["phases"]["fit"]["receipt"]
        r["inputs"]["curves_sha256"] = _other_hex64(r["inputs"]["curves_sha256"])
        r["input_package_digest"] = PV.input_package_digest(r["inputs"])      # 자기일관 — 공통 검사는 통과한다

    _rewrite_claim(c, forge)
    led_before = led.read_bytes()
    with pytest.raises(PV.PreserveError) as ei:
        PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, token=c.token)
    assert "소비한 밖 입력" in str(ei.value), "거부 이유가 receipt 묶음 ↔ 소비 결속 대조가 아니다"
    assert led.read_bytes() == led_before, "거부했는데 원장 바이트가 바뀌었다"
