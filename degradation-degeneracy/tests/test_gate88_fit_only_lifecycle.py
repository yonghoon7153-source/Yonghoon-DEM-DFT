"""88차 — G87-N1 한정 보완: v6 fit-only claim 의 phase 계약 (고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` §14 · 원장 §129).

87차 리뷰어 G87-N1 (P1): 비-smoke v6 fit-only 새 claim 은 `phases={}` 로 시작하고, 밖 입력 (계획 `fit.in_digest` hex64) 의
묶음 검사는 grid 영수증 없이 통과한다. 그런데 fit 본체가 끝나면 `commit_run_outputs` 뒤 `_record_phase(claim, "fit")` →
`phase_done("fit")` 이 `CLAIM_PHASES = ("grid", "fit")` 의 순서 규칙으로 grid 선행을 요구해 거부하고, `finalize_leg` 도 두
phase 를 요구한다. 87차 시험은 발급까지 (s02_04 — 그것도 곡선 단독 sha) 와 smoke 완주 (s04_01 — claim None) 만 봤다.

§14 계약: claim 의 phase 집합은 **승인 spec 이 정한다** — v2 → (grid, fit) 그대로 · v3 + 밖 입력 hex64 → (fit,) · v3 + null →
계획 index 에서 거부. v3 claim 만 `phases_required: ["fit"]` 를 봉인 (v2 claim 키 · 바이트 불변). fit-only 의 fit receipt 는
실제로 읽은 staged 입력 묶음을 결속 (`input_package_digest` + 키별 `inputs` — 다시 계산한 값과 같아야) · finalize 가 계획
`fit.in_digest` 와 재대조 + 집합 재유도 · 실행 기록에 grid 를 적지 않는다.

node (§14-3): f00 대조 (처음부터 GREEN 이어야 한다 — v2 순서 · v2 finalize · v3 아래 grid gate · v2 claim 위조 · v2 완주) ·
f01 양성 (비-smoke 완주 → 기록 → 최종화) · f02 입력 · f03 소유 · 결속 · f04 재개. 입력 digest 는 곡선 단독 SHA 가 아니라
**실제 묶음 digest** (`fit_input_package_digest(_fit_input_digests(in))` — 리뷰어 주의). 수치 본체는 tiny curves 로 실제로
돈다 — lifecycle 함수 대체 · 선행 영수증 수동 삽입 없음. RED 에서 "통과" 하는 비-대조 node 는 fixture 가 진실을 가린 것이다.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from src import fitting as F
from tests import test_gate84_round2a as G84
from tests import test_gate87_round2b as G87
from tools import preserve as PV

LEG = G87.LEG
SRC = G87.SRC
EVIDENCE = {"leg_source_digest": SRC, "cohorts": ["g87"]}
CTX_SLOT = {"design": G87.DESIGN_REL, "provider_runs": {}}


# ─────────────────────────────────────────────────────────────────────────────
# 도구
# ─────────────────────────────────────────────────────────────────────────────
def _pkg(in_dir) -> str:
    """리뷰어가 요구한 **실제** 계약 — 입력 묶음 셋의 package digest."""
    return F.fit_input_package_digest(F._fit_input_digests(in_dir))


def _v3_setup(tmp_path, monkeypatch, name: str, *, in_digest="pkg"):
    """비-smoke 산출 자리 · 격리 원장 · v3 계획 항목 하나. `in_digest`: 'pkg' · 'curves' (곡선 단독 sha) · None · 임의 값."""
    out = G87._scratch(name)
    led = G87._isolated_authority(monkeypatch, out)
    in_dir, ctx, live, curves_sha = G87._live_pair(tmp_path, out)
    ind = {"pkg": _pkg(in_dir), "curves": curves_sha}.get(in_digest, in_digest) if isinstance(in_digest, str) else in_digest
    p = ctx["planned"]
    spec = PV.leg_run_spec_v3(LEG, G87._grid_for(live), dict(live, in_digest=ind), G87._axis(p.envelope()))
    G87._write(led, G87._doc(G87._entry(spec, envelope=p.envelope(), context=dict(CTX_SLOT))))
    return out, led, in_dir, ctx, spec, ind


def _fit_receipt(in_dir, **over) -> dict:
    """fit-only claim 의 fit receipt — `_record_phase` 가 쓰는 꼴 + 밖 입력 결속."""
    inputs = F._fit_input_digests(in_dir)
    r = {"out": "results/g88_unit", "n_rows": 3, "finished_at": "2026-10-03T00:00:00Z",
         "input_package_digest": F.fit_input_package_digest(inputs), "inputs": inputs}
    r.update(over)
    return r


def _v2_setup(tmp_path, monkeypatch, name: str):
    out = G87._scratch(name)
    led = G87._isolated_authority(monkeypatch, out)
    in_dir, ctx, live, curves_sha = G87._live_pair(tmp_path, out)
    spec = PV.leg_run_spec(LEG, G87._grid_for(live), dict(live, in_digest=_pkg(in_dir)))
    G87._write(led, G87._doc(G87._entry(spec)))
    return out, led, spec, in_dir


#: 변이 증인은 실행마다 같아야 한다 (G67-T1-b) — 입력 묶음 digest 는 실행마다 달라지므로 (tiny curves 의 서명 · 경로) 거부
#: 메시지 원문을 증인으로 쓰지 않고 **이유 범주**만 적는다. 원문은 RED 로그 (`gate88_evidence/01_red_test_gate88.log`) 에 있다.
_WHY = (("선행 phase", "grid 선행 요구 (G87-N1)"),
        ("밖 입력 묶음 결속 `input_package_digest`", "fit receipt 에 밖 입력 결속 없음"),
        ("`inputs` 가", "fit receipt inputs 닫힘 위반"),
        ("자기모순", "결속 자기모순"),
        ("계획 spec 에서 유도한", "phase 집합 재유도 불일치"),
        ("소비한 밖 입력", "소비한 입력이 계획과 다름"),
        ("claim schema", "claim 키 집합 위반"),
        ("phase 가 남았다", "남은 phase"),
        ("입력 묶음과 지금 읽는 묶음", "입력 묶음 대조"))


def _why(exc: BaseException) -> str:
    s = str(exc)
    return next((label for key, label in _WHY if key in s), f"기타 {type(exc).__name__}")


def _finalize_ok(led: Path, token=None) -> dict:
    try:
        return PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, **({} if token is None else {"token": token}))
    except PV.PreserveError as exc:
        pytest.fail(f"fit-only claim 을 executed 로 닫지 못했다 — {_why(exc)}")


def _leg_record(led: Path) -> dict:
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    return next(e for e in doc.get("legs") or [] if e["leg_id"] == LEG)


# ─────────────────────────────────────────────────────────────────────────────
# f00 — 대조 (처음부터 GREEN: v2 의 순서 · 최종화 규칙은 그대로다)
# ─────────────────────────────────────────────────────────────────────────────
def test_f00_01_a_v2_claim_still_refuses_fit_before_grid(tmp_path, monkeypatch):
    out, led, spec, _ = _v2_setup(tmp_path, monkeypatch, "f00a")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    with pytest.raises(PV.PreserveError) as ei:
        c.phase_done("fit", {"fits": 3})
    assert "선행" in str(ei.value) and "grid" in str(ei.value), "거부 이유가 v2 순서 규칙이 아니다"


def test_f00_02_a_v2_claim_still_refuses_to_finalize_with_grid_only(tmp_path, monkeypatch):
    out, led, spec, _ = _v2_setup(tmp_path, monkeypatch, "f00b")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    c.phase_done("grid", {"rows": 3})
    with pytest.raises(PV.PreserveError) as ei:
        PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, token=c.token)
    assert "phase" in str(ei.value) and "fit" in str(ei.value), "거부 이유가 남은 phase 규칙이 아니다"


def test_f00_03_the_grid_gate_under_a_v3_plan_is_refused(tmp_path, monkeypatch):
    """grid gate 는 v2 spec 만 만든다 → v3 계획의 주소와 다르다 → claim 0 (87차 판독 · '그냥 grid 를 먼저' 는 v6 경로가 아니다)."""
    from src import grid as G
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, "f00c")
    monkeypatch.setattr(G, "live_grid_axis", lambda cfg, conditions, out_dir: dict(spec["grid"]))
    with pytest.raises(PV.PreserveError):
        G._assert_grid_authorized({}, out, None, leg=LEG, may_open=True)
    assert not PV._claim_path(LEG, PV.claims_root_for_ledger(led)).exists(), "v3 계획 아래 grid claim 이 열렸다"
    assert PV.planned_index(ledger=led)[LEG]["status"] == "planned"


def test_f00_04_a_v2_claim_with_an_injected_phase_set_can_not_be_finalized_fit_only(tmp_path, monkeypatch):
    """v2 claim 파일에 `phases_required: ["fit"]` 를 끼워 넣고 결속된 fit receipt 를 줘도 fit 하나로 executed 가 되지 않는다
    — phase_done 에서 거부되든 (지금 코드 · 순서 규칙) finalize 의 집합 재유도에서 거부되든 (§14-2 d)."""
    out, led, spec, in_dir = _v2_setup(tmp_path, monkeypatch, "f00d")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    rec = json.loads(c.path.read_text(encoding="utf-8"))
    rec["phases_required"] = ["fit"]
    c.path.write_text(json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    with pytest.raises(PV.PreserveError):
        c.phase_done("fit", _fit_receipt(in_dir))
        PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, token=c.token)
    assert PV.planned_index(ledger=led)[LEG]["status"] == "running"
    assert not any(e.get("leg_id") == LEG
                   for e in yaml.safe_load(led.read_text(encoding="utf-8")).get("legs") or [])


def test_f00_05_a_v2_lifecycle_still_closes_grid_then_fit_with_the_consumed_binding(tmp_path, monkeypatch):
    out, led, spec, _ = _v2_setup(tmp_path, monkeypatch, "f00e")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    c.phase_done("grid", {"rows": 3})
    c.phase_done("fit", {"fits": 3})
    assert _finalize_ok(led, token=c.token)["status"] == "executed"
    ph = _leg_record(led)["evidence"]["phases"]
    assert set(ph) == {"grid", "fit"}, "v2 실행 기록의 phase 가 grid · fit 둘이 아니다"
    assert set(ph["fit"]["consumed"]) == {"grid"}, "v2 fit 의 소비 결속이 grid 하나가 아니다"


def test_f00_06_a_v2_fit_receipt_carries_no_external_input_binding(tmp_path, monkeypatch):
    """§14-2 c — 밖 입력 결속은 fit 전용 claim 만 싣는다. v2 claim 의 fit 완료 기록은 지금 바이트 그대로다
    (`out` · `n_rows` · `finished_at` — v2 의 생산자는 같은 claim 의 grid 이고 그 결속은 `consumed` 가 한다).
    발송 전 자체 점검으로 더한 node — 처음부터 GREEN 이고, `-g88` 변이가 "v2 에도 결속을 싣는" 사본에서 빨개짐을 증명한다."""
    out, led, spec, in_dir = _v2_setup(tmp_path, monkeypatch, "f00f")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    assert c.required_phases() == PV.CLAIM_PHASES
    binding = F._fit_input_binding(c, in_dir)
    assert binding is None, "v2 claim 의 fit 완료 기록에 밖 입력 결속이 실린다 (v2 receipt 바이트가 바뀐다)"
    seen = []

    class _Spy:
        def phase_done(self, phase, receipt):
            seen.append((phase, dict(receipt)))

    F._record_phase(_Spy(), "fit", {"n_rows": 3}, out, input_binding=binding)
    assert [p for p, _ in seen] == ["fit"]
    assert sorted(seen[0][1]) == ["finished_at", "n_rows", "out"], "v2 fit receipt 의 키가 바뀌었다"


# ─────────────────────────────────────────────────────────────────────────────
# f01 — 양성: 비-smoke v6 fit-only 의 승인 → 입력 대조 → 계산 → commit → 완료 기록 → 최종화
# ─────────────────────────────────────────────────────────────────────────────
def test_f01_01_a_v6_fit_only_leg_runs_records_and_finalizes(tmp_path, monkeypatch):
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, "f01a")
    try:
        G87._run_nonsmoke(in_dir, out, ctx)                   # 실물 lifecycle — 대체 · 수동 삽입 없음
    except PV.PreserveError as exc:
        pytest.fail(f"비-smoke fit-only 실행이 승인 · 입력 대조 · 완료 기록 중에 거부됐다 — {_why(exc)}")
    assert PV.inspect_leg_run(LEG, ledger=led)["phases_done"] == ["fit"], "상태 view 의 닫힌 phase 가 fit 하나가 아니다"
    assert _finalize_ok(led)["status"] == "executed"
    ph = _leg_record(led)["evidence"]["phases"]
    assert set(ph) == {"fit"}, "fit-only 실행 기록에 fit 밖의 phase 가 있다 (grid 를 적었다)"
    assert ph["fit"]["consumed"] == {"external_input": ind}, "fit 의 소비 결속이 계획의 밖 입력 묶음이 아니다"
    rec = ph["fit"]["receipt"]
    assert rec["input_package_digest"] == ind, "fit receipt 의 묶음 digest 가 계획과 다르다"
    assert F.fit_input_package_digest(rec["inputs"]) == ind, "fit receipt 의 inputs 로 다시 계산한 묶음이 다르다"
    assert PV.planned_index(ledger=led)[LEG]["status"] == "executed", "계획이 executed 로 닫히지 않았다"


# ─────────────────────────────────────────────────────────────────────────────
# f02 — 입력 음성
# ─────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("bad", ["other", "curves"], ids=["other_package", "curves_only_sha"])
def test_f02_01_inputs_other_than_the_approved_package_are_refused_before_fit_one(tmp_path, monkeypatch, bad):
    """대조: 다른 묶음 · 곡선 단독 sha 를 계획에 적으면 시작 전 거부 (`_fit_one` 0) — 처음부터 GREEN."""
    ind = "ab" * 32 if bad == "other" else "curves"
    out, led, in_dir, ctx, spec, _ = _v3_setup(tmp_path, monkeypatch, f"f02a_{bad}", in_digest=ind)
    calls = G84._sentinel(monkeypatch)
    with pytest.raises(PV.PreserveError) as ei:
        G87._run_nonsmoke(in_dir, out, ctx)
    assert "입력 묶음" in str(ei.value), "거부 이유가 입력 묶음 대조가 아니다"
    assert calls == [], "거부가 첫 수치 작업 뒤다"


def test_f02_02_a_v3_plan_without_an_external_input_digest_is_refused_by_the_index(tmp_path, monkeypatch):
    """v3 + `fit.in_digest: null` = '이 다리의 grid 가 입력을 만든다' — v6 에는 그 grid 가 없다 → 계획 index 에서 거부."""
    out, led, in_dir, ctx, spec, _ = _v3_setup(tmp_path, monkeypatch, "f02b", in_digest=None)
    with pytest.raises(PV.PreserveError) as ei:
        PV.planned_index(ledger=led)
    assert "in_digest" in str(ei.value), "거부 이유가 v6 밖 입력 (fit.in_digest) 규칙이 아니다"


# ─────────────────────────────────────────────────────────────────────────────
# f03 — 소유 · 결속 음성 (claim API 직접 — lifecycle 함수는 실물)
# ─────────────────────────────────────────────────────────────────────────────
def test_f03_01_a_fit_only_claim_refuses_a_grid_phase(tmp_path, monkeypatch):
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, "f03a")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    with pytest.raises(PV.PreserveError) as ei:
        c.phase_done("grid", {"rows": 3})
    assert "grid" in str(ei.value), "거부 이유가 claim phase 집합 규칙이 아니다"


@pytest.mark.parametrize("over", [{"input_package_digest": None}, {"inputs": None}, "mismatch"],
                         ids=["no_package", "no_inputs", "inputs_disagree"])
def test_f03_02_a_fit_receipt_without_a_consistent_input_binding_is_refused(tmp_path, monkeypatch, over):
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, "f03b")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    if over == "mismatch":
        r = _fit_receipt(in_dir)
        r["inputs"] = dict(r["inputs"], curves_sha256="cd" * 32)
    else:
        r = _fit_receipt(in_dir)
        for k, v in over.items():
            r.pop(k) if v is None else r.__setitem__(k, v)
    with pytest.raises(PV.PreserveError) as ei:
        c.phase_done("fit", r)
    assert "input_package_digest" in str(ei.value) or "inputs" in str(ei.value), "거부 이유가 밖 입력 결속 규칙이 아니다"


def test_f03_03_finalize_refuses_an_external_input_other_than_the_plan(tmp_path, monkeypatch):
    """claim 에 적힌 결속이 계획 `fit.in_digest` 와 다르면 executed 로 닫지 않는다 (durable state 변조 · 다른 바이트)."""
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, "f03c")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    c.phase_done("fit", _fit_receipt(in_dir))
    rec = json.loads(c.path.read_text(encoding="utf-8"))
    rec["phases"]["fit"]["consumed"]["external_input"] = "ef" * 32
    c.path.write_text(json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    with pytest.raises(PV.PreserveError) as ei:
        PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, token=c.token)
    assert "in_digest" in str(ei.value) or "external_input" in str(ei.value), "거부 이유가 계획 입력 재대조가 아니다"


def test_f03_04_another_attempt_can_not_record_or_finalize(tmp_path, monkeypatch):
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, "f03d")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    stranger = PV.LegClaim(LEG, c.cohort_id, c.attempt_id, c.run_spec_digest, c.source_digest, c.path,
                           token="0" * 64)
    with pytest.raises(PV.PreserveError):
        stranger.phase_done("fit", _fit_receipt(in_dir))
    c.phase_done("fit", _fit_receipt(in_dir))
    with pytest.raises(PV.PreserveError):
        PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, token="0" * 64)
    assert _finalize_ok(led, token=c.token)["status"] == "executed"


#: f03_05 · f03_06 — GREEN 이 더한 fail-closed 분기 가운데 f00–f04 가 닿지 않던 셋을 고정한다 (발송 전 자체 점검 · 요청문 §6).
#: 정상 lifecycle 은 이 값들을 만들지 않으므로 도달 경로는 durable 변조 · 손으로 만든 receipt 뿐이다 — 그래서 처음부터 GREEN 이고,
#: "무는가" 는 `-g88` 변이 (분기를 끈 사본에서 빨개지는가) 가 증명한다.
@pytest.mark.parametrize("tag,value", [("grid_fit", ["grid", "fit"]), ("fit_twice", ["fit", "fit"]),
                                       ("scalar", "fit"), ("empty", [])],
                         ids=["grid_fit", "fit_twice", "scalar", "empty"])
def test_f03_05_a_claim_phase_set_other_than_exactly_fit_is_refused_where_it_is_used(tmp_path, monkeypatch, tag, value):
    """claim 의 `phases_required` 값은 정확히 `["fit"]` 이다 (§14-2 b). 키 집합 검사 (`_claim_record_keys_ok`) 는 값을 보지
    않으므로, 다른 값은 집합을 쓰는 자리 (`phase_done` · `required_phases()` · `finalize_leg`) 에서 거부돼야 한다."""
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, f"f03e_{tag}")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    rec = json.loads(c.path.read_text(encoding="utf-8"))
    rec["phases_required"] = value
    c.path.write_text(json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    with pytest.raises(PV.PreserveError) as ei:
        c.phase_done("fit", _fit_receipt(in_dir))
    assert "phases_required" in str(ei.value), "거부 이유가 claim phase 집합 값 규칙이 아니다"
    with pytest.raises(PV.PreserveError) as ei:
        c.required_phases()
    assert "phases_required" in str(ei.value), "거부 이유가 claim phase 집합 값 규칙이 아니다"
    assert PV.planned_index(ledger=led)[LEG]["status"] == "running"


@pytest.mark.parametrize("how", ["inputs_extra_key", "inputs_not_hex", "receipt_package_tampered"])
def test_f03_06_a_self_consistent_binding_forgery_is_refused(tmp_path, monkeypatch, how):
    """결속을 **자기일관하게** 위조해도 닫히지 않는다 — `inputs` 는 `PHASE_INPUT_KEYS` 의 hex64 로 닫혀 있고 (§14-2 c),
    finalize 는 receipt 의 묶음 digest 와 `consumed.external_input` 을 서로 대조한다 (§14-2 d · 계획 대조와 별도)."""
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, f"f03f_{how}")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    r = _fit_receipt(in_dir)
    if how == "receipt_package_tampered":
        c.phase_done("fit", r)
        rec = json.loads(c.path.read_text(encoding="utf-8"))
        rec["phases"]["fit"]["receipt"]["input_package_digest"] = "cd" * 32    # consumed 는 그대로 (계획과 같다)
        c.path.write_text(json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n",
                          encoding="utf-8")
        with pytest.raises(PV.PreserveError) as ei:
            PV.finalize_leg(LEG, dict(EVIDENCE), ledger=led, token=c.token)
        assert "소비한 밖 입력" in str(ei.value), "거부 이유가 receipt 묶음 ↔ 소비 결속 대조가 아니다"
        return
    if how == "inputs_extra_key":
        r["inputs"] = dict(r["inputs"], extra_sha256="ab" * 32)
    else:
        r["inputs"] = dict(r["inputs"], curves_sha256="zz" * 32)
        r["input_package_digest"] = PV.input_package_digest(r["inputs"])         # 묶음 digest 는 위조한 inputs 와 일치
    with pytest.raises(PV.PreserveError) as ei:
        c.phase_done("fit", r)
    assert "`inputs` 가" in str(ei.value), "거부 이유가 inputs 닫힘 규칙이 아니다"


# ─────────────────────────────────────────────────────────────────────────────
# f04 — 재개 · 상태
# ─────────────────────────────────────────────────────────────────────────────
def test_f04_01_a_fit_only_claim_resumes_with_fit_as_its_only_phase(tmp_path, monkeypatch):
    out, led, in_dir, ctx, spec, ind = _v3_setup(tmp_path, monkeypatch, "f04a")
    c = PV.open_leg_run(LEG, spec, SRC, ledger=led)
    token = c.token
    del c                                                     # 실행이 죽었다
    r = PV.resume_claim(LEG, token=token, ledger=led)
    assert r.phases_done() == ()
    r.phase_done("fit", _fit_receipt(in_dir))
    assert PV.resume_claim(LEG, token=token, ledger=led).phases_done() == ("fit",)
    assert PV.inspect_leg_run(LEG, ledger=led)["phases_done"] == ["fit"], "상태 view 의 닫힌 phase 가 fit 하나가 아니다"
    assert _finalize_ok(led, token=token)["status"] == "executed"
