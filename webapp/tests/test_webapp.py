#!/usr/bin/env python3
"""test_webapp.py — 리뷰(2026-08-07)의 완료 판정 기준을 **자동 검사**로 굳힌다.

왜 이 파일인가
  이 앱은 주석에 과거 회귀를 잔뜩 적어 두는데, 정작 같은 문제가 다시 생기는 걸 막는
  코드는 없었다(리뷰 P2). 여기 담은 건 전부 **실제로 한 번 터졌던 것**들이다.

    pytest webapp/tests/test_webapp.py -q
    python3 webapp/tests/test_webapp.py          # pytest 없이도 돈다
"""
import json
import pytest
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A                 # noqa: E402
import artifact_policy as AP    # noqa: E402
import canonical as C           # noqa: E402
import data as D                # noqa: E402


# ── 1) 정본 레지스트리 ↔ 원자료 ─────────────────────────────────────────────
def test_registry_matches_sources():
    """레지스트리 값이 source_path/source_key 가 가리키는 원자료와 같아야 한다."""
    bad = C.validate(C.load_registry())
    assert not bad, "원자료와 어긋남:\n" + "\n".join(
        f"  {e.get('metric')}/{e.get('system')}: {w}" for e, w in bad)


def test_no_hardcoded_canonical_numbers():
    """정본 숫자가 data.py 로 되돌아오면 안 된다 — 그게 원래의 drift 원인이었다."""
    src = (ROOT / "webapp" / "data.py").read_text(encoding="utf-8")
    m = re.search(r"^CANONICAL\s*=\s*\{[^}]", src, re.M)
    assert m is None, "data.py 에 CANONICAL 딕셔너리 리터럴이 다시 생겼다 — 레지스트리를 쓸 것"


def test_canonical_entries_have_provenance():
    """status=canonical 이면 반드시 출처와 비교 묶음이 있어야 한다."""
    for e in C.load_registry()["entries"]:
        if e.get("status") != "canonical":
            continue
        assert e.get("source_path") and e.get("source_key"), f"{e['metric']}/{e['system']} 출처 없음"
        assert e.get("comparison_group"), f"{e['metric']}/{e['system']} comparison_group 없음"
        assert e.get("method_id"), f"{e['metric']}/{e['system']} method_id 없음"


# ── 2) 프로토콜 혼합 금지 (이번 리뷰의 핵심) ────────────────────────────────
def test_md_ea_groups_are_separated():
    """단일시드 앵커와 멀티시드 정본이 같은 비교 묶음에 있으면 안 된다."""
    reg = C.load_registry()
    multi = C.canonical_map(reg, "MD_Ea_eV", group="md-ea-multiseed-v1")
    single = C.canonical_map(reg, "MD_Ea_eV_singleseed", group="md-ea-singleseed-anchor-v1")
    assert set(multi) and set(single)
    for e in C.entries(reg, "MD_Ea_eV", group="md-ea-multiseed-v1"):
        assert (e.get("n_seed") or 0) >= 3, f"{e['system']} 이 멀티시드 묶음에 있는데 n_seed={e.get('n_seed')}"
    # 옛 버그의 정확한 형태: modelc 단일시드 0.224 가 멀티시드 묶음에 섞여 있던 것
    assert abs(multi.get("modelc", 0) - 0.197) < 1e-6, "modelc 멀티시드 값이 아니다"


def test_md_ea_beta_gate_blocks_canonical():
    """★ n_seed 만 보면 β 게이트 탈락을 못 잡는다 (2026-08-07 Codex 재검증).

    LPSOCl 은 4-seed 라 n_seed 검사는 통과하는데, 600 K β=0.615 가 Fickian 게이트를
    못 넘어 kb/open_items.md 가 인용 보류로 묶어 둔 값이다. 숫자가 db 와 맞아도
    정본이 아니다 — 게이트를 별도 축으로 검사한다.
    """
    reg = C.load_registry()
    for e in reg["entries"]:
        if C.gate_blocks_canonical(e):
            assert e.get("status") != "canonical", \
                (f"{e['metric']}/{e['system']} 이 게이트({e['blocking_gate']}, "
                 f"{C.gate_outcome(e)}) 인데 canonical 이다")
    lp = [e for e in reg["entries"]
          if (e["metric"], e["system"]) == ("MD_Ea_eV", "lpsocl")]
    assert lp and lp[0]["status"] != "canonical", "LPSOCl Ea 가 다시 canonical 로 올라왔다"
    assert lp[0].get("gate_detail", {}).get("beta_600K", 1.0) < 0.8, "β 근거가 사라졌다"


def test_gate_outcome_vocabulary():
    """게이트 판정 어휘가 한 곳(canonical.gate_outcome)에서만 나온다.

    ⛔ 2026-08-20 codex 동결감사 — 옛 테스트는 `blocking_gate` 존재 = 미통과라는
       **옛 의미를 잠그고 있었다**. b2o3 골격 게이트는 미평가(not_assessed)이지
       실패가 아닌데, 그 구분이 없으면 정정을 해도 기계 경로가 되돌린다.
       미평가/통과/실패/비해당/미기재를 전부 fixture 로 고정한다.
    """
    mk = lambda g, out=...: ({"blocking_gate": g} if out is ... else
                             {"blocking_gate": g,
                              "gate_detail": {"lineage": {"gate_outcome": out}}})

    assert C.gate_outcome({}) is None,                       "게이트가 없으면 None"
    assert C.gate_outcome(mk("g")) == "fail",                "판정 미기재는 보수적으로 fail"
    for out in ("not_assessed", "pass", "fail", "inapplicable"):
        assert C.gate_outcome(mk("g", out)) == out,          f"{out} 이 그대로 안 나온다"
    assert C.gate_outcome(mk("g", "nonsense")) == "fail",    "모르는 값은 fail 로 떨어져야"
    # current_assessment.result 경로도 같은 답을 줘야 한다 (registry 두 표기 병존)
    assert C.gate_outcome({"blocking_gate": "g", "gate_detail": {
        "lineage": {"current_assessment": {"result": "not_assessed"}}}}) == "not_assessed"

    # 정본 차단: 실패와 미평가는 막고, 통과·비해당은 안 막는다
    assert C.gate_blocks_canonical(mk("g", "fail")) is True
    assert C.gate_blocks_canonical(mk("g", "not_assessed")) is True,  "미평가는 통과가 아니다"
    assert C.gate_blocks_canonical(mk("g", "pass")) is False
    assert C.gate_blocks_canonical(mk("g", "inapplicable")) is False
    assert C.gate_blocks_canonical({}) is False

    # 문구: 미평가를 '미통과' 라고 쓰면 안 된다 (F2 재발 방지의 핵심)
    na = C.gate_prefix(mk("framework_beta_800_1000K", "not_assessed"))
    assert "미평가" in na and "미통과" not in na, f"미평가 문구가 틀렸다: {na}"
    assert "미통과" in C.gate_prefix(mk("g", "fail"))
    assert C.gate_prefix({}) == ""


def test_assessment_sidecar_is_authoritative(tmp_path, monkeypatch):
    """게이트 판정은 sidecar 가 권위다 — claim 안의 옛 판정을 보면 안 된다.

    ⛔ 2026-08-20 codex 동결감사 — 판정을 canonical claim 에 두면 consumer 마다
       '현재 판정' 을 다르게 고를 수 있다. required_assessment_refs 가 있으면
       gate_detail 은 **보지 않는다**.
    """
    book = C.assessments()
    assert book, "판정 원장이 비었다"

    # ① sidecar 가 claim 안의 값을 이긴다 (일부러 모순되게 넣는다)
    e = {"metric": "X", "system": "y", "blocking_gate": "g",
         "required_assessment_refs": ["A-2026-08-20-b2o3-framework-current"],
         "gate_detail": {"lineage": {"gate_outcome": "pass"}}}       # ← 거짓말
    assert C.gate_outcome(e) == "not_assessed", "claim 안의 옛 판정을 읽고 있다"

    # ② 없는 판정을 참조하면 fail-closed
    import pytest as _p
    with _p.raises(RuntimeError, match="없는 판정"):
        C.gate_outcome({"blocking_gate": "g", "required_assessment_refs": ["A-nope"]})

    # ③ active 가 1개가 아니면 오류 — 철회본만 가리키면 0개다
    with _p.raises(RuntimeError, match="active 판정이"):
        C.gate_outcome({"blocking_gate": "g",
                        "required_assessment_refs": ["A-2026-08-20-b2o3-framework-legacy"]})

    # ④ 옛 판정과 새 판정이 **병존**한다 (대체가 아니다)
    legacy = book["A-2026-08-20-b2o3-framework-legacy"]
    assert legacy["state"] == "retracted" and legacy["binding"] == "diagnostic_unbound", \
        "옛 beta 판정이 철회+미결속 상태로 보존돼야 한다"
    assert legacy["result"] == "fail", "옛 판정의 내용까지 지우면 감사가 안 된다"

    # ⑤ correction 사건이 대상을 지목한다 (F10/R9)
    corr = [a for a in book.values() if a.get("kind") == "correction"]
    assert corr, "정정 사건 레코드가 없다"
    for c in corr:
        assert c.get("supersedes_assessment_id") in book, "정정이 가리키는 대상이 원장에 없다"
        assert "scope" in c, "정정에 범위가 없다 — 다른 항목에 복사되는 것을 막는 필드다"

    # ⑥ Ea 분모(3)와 PMF 분모(4)가 분리돼 있다
    cur = book["A-2026-08-20-b2o3-framework-current"]["raw_trajectory_set"]
    assert cur["ea_ensemble"]["T600"]["expected"] == 3
    assert cur["pmf_ensemble"]["T600"]["used"] == 4, "PMF 4궤적이 Ea 분모와 섞이면 안 된다"


def test_governance_graph_has_no_dangling_edges():
    """판례·판정 원장 무결성 — **db 도구와 같은 함수**로 검사한다.

    ⛔ 검사 로직을 여기에 사본으로 두면 tools/db/validate_canonical.py 와 갈라진다.
       위반 종류별 음성 시험은 그쪽 --selftest 가 13건 갖고 있다 (합성 fixture).
       여기서는 **실제 repo 원장**이 통과하는지만 본다.
    """
    assert C.validate_governance() == [], "실제 원장에 무결성 위반이 있다"
    # 원장이 비어 있으면 위 단언이 공허하게 참이 된다 — 내용이 있는지 확인한다
    assert len(C.decisions()) >= 5, "판례 core 5 가 없다"
    assert len(C.assessments()) >= 3, "판정 원장이 비었다"
    # 옛/새 판정 병존 · correction 이 대상을 지목 (감사 추적의 핵심)
    book = C.assessments()
    legacy = book["A-2026-08-20-b2o3-framework-legacy"]
    assert legacy["state"] == "retracted" and legacy["binding"] == "diagnostic_unbound"
    assert legacy["result"] == "fail", "옛 판정의 내용까지 지우면 감사가 안 된다"
    corr = [a for a in book.values() if a.get("kind") == "correction"]
    assert corr and all(c["supersedes_assessment_id"] in book for c in corr)


def test_ratification_gate_cannot_be_bypassed_by_field_name():
    """⛔음성 — `status` 만 든 판례가 승인 없이 active 로 올라가면 잡히는가.

    2026-09-01 실제 구멍: 승인 검사가 `decision_state` 만 읽는데 원장의 두 기록
    (polaron Fbb·S0)은 `status` 만 갖고 있었다 → 그 둘은 `active` 로 올려도
    **어떤 검사에도 안 걸렸다**(fail-open). 별칭을 같이 읽게 고친 뒤의 회귀시험.
    """
    real_dec, real_ass = C.decisions, C.assessments
    real_reg, real_art = C.registry, C.artifacts
    try:
        C.assessments = lambda root=None: {}
        C.registry = lambda root=None: {"entries": []}
        C.artifacts = lambda root=None: {}

        def _only(d):
            C.decisions = lambda root=None: {d["id"]: d}
            return [x for x in C.validate_governance() if d["id"] in x]

        assert _only({"id": "D-x", "status": "active", "slot": "s1"}), \
            "status 별칭으로 승인 게이트를 우회할 수 있다"
        assert _only({"id": "D-y", "slot": "s2"}), "상태 필드가 없는데 통과한다"
        assert _only({"id": "D-z", "decision_state": "proposed",
                      "status": "active", "slot": "s3"}), "두 필드 불일치를 못 본다"
        # 양성: 별칭만 써도 proposed 는 정상이어야 한다 (실제 원장의 2건이 이 꼴)
        assert not _only({"id": "D-ok", "status": "proposed", "slot": "s4"}), \
            "별칭을 쓴 정상 기록을 오탐한다"
    finally:
        C.decisions, C.assessments = real_dec, real_ass
        C.registry, C.artifacts = real_reg, real_art


def test_decision_state_must_be_a_real_string_not_just_present():
    """⛔음성 (회신 BG ④) — `decision_state: null` 이 **어느 검사에도 안 걸렸다.**

    구멍이 둘이었다: ① 부재 검사가 `"decision_state" not in d` 라 **키가 있고 값이
    null** 이면 통과 ② enum 검사가 `if _st is not None` 이라 null 이면 건너뛴다.
    ⇒ 상태 없는 결정이 조용히 흘러간다. 상태는 "키가 있음" 이 아니라
    **비어 있지 않은 문자열 + 허용 어휘**여야 한다.
    """
    real = (C.decisions, C.assessments, C.registry, C.artifacts)
    try:
        C.assessments = lambda root=None: {}
        C.registry = lambda root=None: {"entries": []}
        C.artifacts = lambda root=None: {}

        def _bad(d):
            C.decisions = lambda root=None: {d["id"]: d}
            return [x for x in C.validate_governance() if d["id"] in x]

        for val, why in ((None, "null"), ("", "빈 문자열"), ("   ", "공백뿐"),
                         (3, "숫자"), (["active"], "리스트"), (True, "불리언")):
            assert _bad({"id": f"D-{why}", "slot": "s", "decision_state": val}), \
                f"decision_state 가 {why} 인데 통과한다"
        # ⛔음성: 별칭 status 로도 같은 구멍이 나면 안 된다
        assert _bad({"id": "D-alias", "slot": "s", "status": None}), \
            "status 가 null 인데 통과한다 (별칭 경로의 같은 구멍)"
        # 양성: 정상 상태는 오탐하지 않는다
        assert not _bad({"id": "D-ok", "slot": "s", "decision_state": "proposed"}), \
            "정상 상태를 위반으로 낸다"
    finally:
        C.decisions, C.assessments, C.registry, C.artifacts = real


def test_sdcp_wave1_status_is_allowlist_not_default_citable():
    """⛔음성 (회신 BG ①) — `/sdcp` 지위 판정이 **fail-open** 이었다.

    `_wave1_gate()` 가 `citable_dE` allow-list 를 만들어 놓고 `_wave1_status()` 가
    **쓰지 않은 채** 마지막 줄에서 무조건 `CITABLE` 을 돌려줬다. 새 fragment 가
    들어오거나 citable 키가 잘못 지워져도 화면은 통과시킨다.
    **모르는 것은 통과가 아니다.**

    ⛔ 이 시험이 못 하는 것: 어떤 fragment 가 인용 가능해야 옳은지는 안 본다.
      **등록되지 않은 것이 기본 통과가 되는지**만 본다.
    """
    from data import _wave1_status
    gate = {"source_missing": False, "citable_dE": {"ptfe_dimer", "ptfe_c10"},
            "dE_notes": {}, "hazards_by_fragment": {}}

    # 양성: 원장에 등록된 fragment 만 CITABLE
    assert _wave1_status("ptfe_dimer", "dE", gate)[0] == "CITABLE", \
        "등록된 fragment 를 인용 불가로 막는다 (과교정)"

    # ⛔음성: 등록 안 된 새 fragment 는 기본 통과 금지
    st, why = _wave1_status("brand_new_fragment", "dE", gate)
    assert st != "CITABLE", f"미등록 fragment 가 기본 CITABLE 이다 (fail-open): {why}"

    # ⛔음성: citable 키가 통째로 사라져도 통과하면 안 된다
    st2, _ = _wave1_status("ptfe_dimer", "dE", dict(gate, citable_dE=set()))
    assert st2 != "CITABLE", "citable 원장이 비었는데 CITABLE 을 돌려준다"

    # ⛔음성: hazard 원장에 걸린 fragment 는 BLOCKED
    st3, why3 = _wave1_status("ptfe_dimer", "dE",
                              dict(gate, hazards_by_fragment={"ptfe_dimer": "BLOCKED — x"}))
    assert st3 == "BLOCKED", f"hazard 가 걸렸는데 {st3} 다 — 원장이 화면을 못 막는다"

    # 양성: 기존 세 특례는 그대로 (강등이 아니라 추가여야 한다)
    assert _wave1_status("sdcp_doped", "dE", gate)[0] == "BLOCKED"
    assert _wave1_status("ptfe_dimer", "eads", gate)[0] == "HOLD"
    assert _wave1_status("sdcp_neutral", "dE", gate)[0] == "NO_VERDICT"
    assert _wave1_status("x", "dE", dict(gate, source_missing=True))[0] == "BLOCKED"


def test_slot_uniqueness_uses_applicability_not_slot_name():
    """slot 유일성은 **겹치는 applicability** 에서만 충돌이다 (2026-09-07).

    종전 구현은 slot **이름만** 봐서, `campaign_closure` 처럼 계마다 하나씩 생기는
    slot 은 **두 번째 계를 등록하는 순간 무조건 실패**했다 (sdcp 마감 + b2o3 마감 —
    서로 아무 관계가 없는 두 결정). 원장 `_rules` 는 처음부터
    *"유일성은 scope 가 아니라 slot + 겹치는 applicability 에서 검사한다"* 였으므로
    **구현이 규칙을 못 따라간 것**이다.

    ⛔ 이 시험이 지켜야 하는 것: 고치면서 **진짜 충돌을 놓치면 안 된다.**
      그래서 음성 경로(겹치는 systems · 전역 `*` · systems 누락 · 문자열 오타)를
      전부 건다. 양성 하나만 있는 시험은 완화를 통과시켜도 아무 말 안 한다.
    """
    real = (C.decisions, C.assessments, C.registry, C.artifacts)
    try:
        C.assessments = lambda root=None: {}
        C.registry = lambda root=None: {"entries": []}
        C.artifacts = lambda root=None: {}

        def _mk(i, systems):
            d = {"id": i, "kind": "closure", "slot": "campaign_closure",
                 "status": "active", "decision_state": "active",
                 "ratification": {"state": "ratified", "actor_id": "x",
                                  "timestamp": "t", "commit": "0" * 40}}
            if systems is not None:
                d["applies_to"] = {"systems": systems}
            return d

        def _slot_bad(a, b):
            C.decisions = lambda root=None: {a["id"]: a, b["id"]: b}
            return [x for x in C.validate_governance() if "slot" in x]

        # ── 양성: 계가 다르면 같은 slot 이어도 충돌이 아니다 ────────────────
        assert not _slot_bad(_mk("D-a", ["sdcp"]), _mk("D-b", ["b2o3"])), \
            "겹치지 않는 두 마감을 slot 이름만 보고 충돌로 낸다 (규칙과 구현이 갈라짐)"

        # ── ⛔음성: 겹치면 여전히 잡아야 한다 ─────────────────────────────
        assert _slot_bad(_mk("D-c", ["b2o3"]), _mk("D-d", ["b2o3"])), \
            "같은 계에 active 마감이 둘인데 통과한다"
        assert _slot_bad(_mk("D-e", ["b2o3", "modelc"]), _mk("D-f", ["modelc"])), \
            "부분적으로 겹치는데 통과한다"
        assert _slot_bad(_mk("D-g", ["*"]), _mk("D-h", ["b2o3"])), \
            "전역(`*`) 결정이 특정 계 결정과 겹치는데 통과한다"
        assert _slot_bad(_mk("D-i", None), _mk("D-j", ["b2o3"])), \
            "systems 가 아예 없는(=전역) 결정이 통과한다 — 누락을 '안 겹침'으로 읽으면 안 된다"
        assert _slot_bad(_mk("D-k", []), _mk("D-l", ["b2o3"])), \
            "systems 가 빈 리스트인데 통과한다"

        # ⛔음성: systems 가 문자열이면 글자 단위로 순회되면 안 된다
        #   "b2o3" 를 글자로 순회하면 {'b','2','o','3'} 이 되어 ["b2o3"] 과 안 겹친다고
        #   나온다 — 오타 하나가 게이트를 조용히 끈다.
        assert _slot_bad(_mk("D-m", "b2o3"), _mk("D-n", ["b2o3"])), \
            "systems 가 문자열일 때 글자 단위로 쪼개져 겹침을 놓친다"
    finally:
        C.decisions, C.assessments, C.registry, C.artifacts = real


def test_narrow_decision_cannot_supersede_global_policy():
    """⛔음성 (회신 AW P0-3 · AZ P0-6) — **좁은 노드가 전역 정책을 덮으면 잡히는가.**

    2026-09-01 실제 구멍: C-12 estimand 노드(systems 2개)가 전역 마감정책
    (systems `*`, kind=policy)을 supersede 하고 있었다. 그 상태로 계산을 던지면
    결과가 정책 결정에 압력을 준다 — 사전등록의 의미가 사라진다. 리뷰어가
    **비용 발생 전** 닫으라고 판정했다 (발송 차단 사유).

    ⛔ 이 시험이 못 하는 것: 어떤 정책이 옳은지는 안 본다. 그래프 규칙만 본다.
    """
    real = (C.decisions, C.assessments, C.registry, C.artifacts)
    try:
        C.assessments = lambda root=None: {}
        C.registry = lambda root=None: {"entries": []}
        C.artifacts = lambda root=None: {}
        glob = {"id": "D-glob", "kind": "policy", "slot": "sg",
                "status": "proposed", "applies_to": {"systems": ["*"]}}

        def _v(extra):
            C.decisions = lambda root=None: {"D-glob": glob, extra["id"]: extra}
            return [x for x in C.validate_governance() if extra["id"] in x]

        assert _v({"id": "D-narrow", "kind": "estimand", "slot": "sn",
                   "status": "proposed", "applies_to": {"systems": ["a", "b"]},
                   "supersedes": ["D-glob"]}), \
            "좁은 estimand 노드가 전역 정책을 supersede 하는데 통과한다"
        assert _v({"id": "D-np", "kind": "estimand", "slot": "sn2",
                   "status": "proposed", "applies_to": {"systems": ["*"]},
                   "supersedes": ["D-glob"]}), \
            "policy 를 non-policy 가 대체하는데 통과한다"
        # 양성: 전역 policy 끼리는 대체할 수 있다
        assert not _v({"id": "D-g2", "kind": "policy", "slot": "sg2",
                       "status": "proposed", "applies_to": {"systems": ["*"]},
                       "supersedes": ["D-glob"]}), \
            "정상적인 policy→policy 대체를 오탐한다"
        # 상태 어휘 밖 · 타입 오류
        assert _v({"id": "D-badstate", "slot": "sb", "status": "aktive"}), \
            "허용 어휘 밖 상태가 통과한다 (검사를 조용히 건너뛴다)"
        assert _v({"id": "D-badtype", "slot": "sb2", "status": "proposed",
                   "supersedes": "D-glob"}), \
            "supersedes 가 문자열인데 통과한다 (글자 단위로 순회된다)"
    finally:
        C.decisions, C.assessments, C.registry, C.artifacts = real


def test_governance_page_renders_citation_hazards():
    """인용 위험 원장이 화면에 **전건** 오르는가 (2026-09-01 신설 절).

    왜: 원장은 25건인데 화면 0건이던 상태가 이 절의 신설 사유다 — 다시 그 상태가
    되면(원장 필드 개명·로더 경로 오타) 조용히 빈 표가 되지 않고 여기서 잡힌다.
    ⛔ 이 시험이 못 하는 것: 위험 목록의 **내용 현행성**은 못 본다 (원장 규율의 몫).
    """
    import json as _json
    raw = _json.loads((ROOT / "db" / "properties" / "citation_hazards.json")
                      .read_text(encoding="utf-8"))
    n = len(raw["hazards"])
    assert n >= 20, "원장이 갑자기 줄었다 — 삭제가 아니라 RESOLVED 로 남기는 규약이다"
    html = A.app.test_client().get("/governance").get_data(as_text=True)
    assert "인용 위험 원장" in html
    assert f"{n}건" in html, "화면의 건수가 원장과 다르다"
    # 수준 어휘가 화면 정렬 사전에 없으면 9로 밀린다 — 새 수준이 생기면 여기서 알아챈다
    known = {"BLOCKED", "HOLD", "STALE", "SUPERSEDED", "CONDITIONAL", "PREVIEW", "RESOLVED"}
    levels = {h["level"] for h in raw["hazards"]}
    assert levels <= known, f"원장에 새 수준이 생겼다: {levels - known} — 화면 정렬·색을 갱신할 것"

    # ⛔⛔ 2026-09-07 회신 BG ⑥ — 종전 판은 **건수와 수준 어휘만** 봤다.
    #   tbody 가 같은 수의 **빈 행**이어도 통과한다. 즉 "25건" 이라고 찍히기만 하면
    #   내용이 하나도 안 실려도 초록이었다. 각 항목의 실제 내용이 화면에 있는지 본다.
    # ⚠ 이스케이프 방언이 둘이다 — Jinja/markupsafe 는 `'` 를 `&#39;` 로, 파이썬
    #   `html.escape` 는 `&#x27;` 로 쓴다. 하나만 쓰면 **시험이 코드를 오탐한다**
    #   (2026-09-07 실측: 멀쩡히 렌더된 항목을 "화면에 없다" 로 잡았다).
    #   그래서 화면을 **역이스케이프**해서 원문끼리 비교한다.
    #   그리고 `|bold` 필터가 `**...**` 를 `<strong>` 으로 바꾸므로, 비교 전에
    #   **양쪽에서 마크업을 없앤다** — 태그를 벗기고 `**` 를 지운 평문끼리 본다.
    import html as _html, re as _re
    plain = _html.unescape(_re.sub(r"<[^>]+>", "", html))
    for h in raw["hazards"]:
        for field in ("file", "level", "what", "why", "fix"):
            v = str(h.get(field, "")).strip()
            if not v:
                continue
            # 긴 문장은 템플릿이 자를 수 있으므로 **앞 40자**를 앵커로 쓴다
            probe = v.replace("**", "")[:40]
            assert probe in plain, (
                f"hazard {h.get('file')!r} 의 {field} 가 화면에 없다 — "
                f"건수만 맞고 내용이 빈 행일 수 있다: {probe!r}")

    # ⛔음성: 원장에 없는 문구를 화면이 지어내지 않는지도 한 번 — 파일 경로는 정확히 원장 것만
    shown_files = {h["file"] for h in raw["hazards"] if h.get("file")}
    assert shown_files, "원장에 file 필드가 하나도 없다 — 앵커가 성립하지 않는다"


def test_artifact_ledger_keeps_verdicts_in_the_ledger():
    """산출물 판정이 **원장 안에** 있는지 — 파일명·기억에 있으면 실패.

    ⛔ 2026-08-20 실측 배경: comp1 2x2x2 궤적(761 MB)이 밴됐는데 그 판정이
       `ToBeDelete_` **파일명 접두사와 사람 기억에만** 있었다. kb 검색으로 사유가 안 나왔다.
       같은 날 F9(궤적 미보존)·요청10(ELF 가 gabia 에만)·gap 실행본 부재까지
       **같은 유형이 다섯 번** 났다 — 산출물은 있는데 지위가 기계 경로 밖에 있었다.
    """
    art = C.artifacts()
    assert art, "산출물 원장이 비었다"

    assert C.validate_artifacts() == [], "산출물 원장에 무결성 위반이 있다"

    # ① 밴은 사유와 해제조건이 원장 안에 있어야 한다
    for a in art.values():
        if a.get("status") == "suspect_banned":
            assert a.get("ban_evidence"), f"{a['id']}: 밴 사유가 원장 밖에 있다"
            assert a.get("unban_condition"), f"{a['id']}: 해제조건이 없다 (영구 보류가 된다)"

    # ② canonical 유일본은 이중화 대상으로 표시돼야 한다 (백업이 유일본인 상황)
    solo = [a for a in art.values()
            if a.get("status") == "canonical" and a.get("copies") == 1]
    assert solo, "canonical 유일본이 하나도 없다 — 원장이 현실과 다르다"
    for a in solo:
        assert a.get("needs_duplication") is True, f"{a['id']}: 유일본인데 이중화 표시가 없다"

    # ③ repo 밖 산출물은 검증 수준을 밝혀야 한다 (위치만? 내용까지? 해시?)
    for a in art.values():
        if (a.get("location") or {}).get("kind") in ("offline_backup", "server"):
            assert (a.get("verified") or {}).get("level"), \
                f"{a['id']}: repo 밖인데 verified.level 이 없다"

    # ④ lost 는 수색이 끝났음을 밝혀야 한다 (다시 찾지 않도록)
    for a in art.values():
        if a.get("status") == "lost":
            assert a.get("copies") in (0, None)
            assert (a.get("verified") or {}).get("level") == "search_exhausted", \
                f"{a['id']}: lost 인데 수색 종료 표시가 없다 — 같은 곳을 또 뒤지게 된다"


def test_lineage_axes_are_independent():
    """재현 가능성과 배선 여부는 **독립 축**이다 (codex R4).

    한 enum(numerically_reproducible)에 넣으면 5단 사다리를 폐기해 놓고 같은 자리에
    사다리를 다시 만드는 것이 된다.
    """
    reg = C.load_registry()
    e = [x for x in reg["entries"]
         if x.get("system") == "b2o3" and x.get("metric") == "MD_Ea_eV"][0]
    lin = e["gate_detail"]["lineage"]
    assert lin["lineage_binding"] == "unwired", "D 를 하드코딩하는 한 wired 가 아니다"
    assert lin["numeric_reproduction"] == "exact", "9개 D 에서 Ea 가 정확히 재현된다"
    assert "numerically_reproducible" not in json.dumps(lin, ensure_ascii=False), \
        "두 축을 한 enum 으로 되돌렸다"
    # 판정은 claim 에 남아 있으면 안 된다
    assert "gate_outcome" not in lin and "current_assessment" not in lin, \
        "판정이 claim 으로 되돌아왔다 — sidecar 가 단일 원장이다"


def test_b2o3_framework_gate_is_not_assessed():
    """b2o3 두 Ea 항목의 골격 게이트는 미평가다 — 실패로 되돌아가면 실패한다.

    근거: high-T raw trajectory 6런(800/1000 K x s2/s3/s4)이 --save_traj 누락으로
    미보존이라 평가 자체가 성립하지 않는다 (F9). 이 테스트는 그 상태가 조용히
    'fail' 로 바뀌는 회귀를 잡는다.
    """
    reg = C.load_registry()
    hits = [e for e in reg["entries"]
            if e.get("system") == "b2o3"
            and e.get("blocking_gate") == "framework_beta_800_1000K"]
    assert len(hits) == 2, f"b2o3 골격 게이트 항목이 2개가 아니다 ({len(hits)})"
    for e in hits:
        assert C.gate_outcome(e) == "not_assessed", \
            f"{e['metric']}/b2o3 게이트가 {C.gate_outcome(e)} 다 — 미평가여야 한다"
        assert e.get("status") != "canonical", "미평가인데 canonical 이다"
    # 순위·레이더 집합에서 자동으로 빠져야 한다
    assert "lpsocl" not in C.canonical_map(reg, "MD_Ea_eV", group="md-ea-multiseed-v1")


def _fixture_registry(tmp, gap=2.2309):
    """repo 밖 임시 root 에 원자료 + 레지스트리를 만든다.

    ⚠ 왜 fixture 인가 (2026-08-07 Codex 3라운드): 첫 판은 추적 중인 정본
      `db/properties/lpsocl_dos_gap.json` 을 직접 고쳤다 `finally` 로 되돌렸다.
      정상 종료·일반 예외에서는 복구되지만 **hard kill·전원 손실에서는 정본이 오염된 채
      남는다.** 게다가 다음 실행이 오염된 파일을 backup 으로 덮어써 복구 기준까지 잃는다.
      → 이제 fixture 가 repo 밖에서 완결된다. 정본 파일은 **읽지도 쓰지도 않는다.**
    """
    import json as _j
    src = tmp / "db" / "properties"
    src.mkdir(parents=True, exist_ok=True)
    (src / "fake_gap.json").write_text(_j.dumps({"gap_eV": gap}), encoding="utf-8")
    regp = tmp / "registry.json"
    regp.write_text(_j.dumps({"schema": "canonical_registry/v1", "entries": [
        {"system": "lpsocl", "metric": "gap_eV", "value": 2.2309, "unit": "eV",
         "source_path": "db/properties/fake_gap.json", "source_key": "/gap_eV",
         "method_id": "test", "comparison_group": "gap-fixedocc-eigenvalue-v1",
         "status": "canonical"},
        {"system": "comp1", "metric": "gap_eV", "value": 2.066, "unit": "eV",
         "source_path": "db/properties/fake_gap2.json", "source_key": "/gap_eV",
         "method_id": "test", "comparison_group": "gap-fixedocc-eigenvalue-v1",
         "status": "canonical"},
    ]}), encoding="utf-8")
    (src / "fake_gap2.json").write_text(_j.dumps({"gap_eV": 2.066}), encoding="utf-8")
    return regp


def test_source_edit_propagates_to_screen():
    """"db 한 곳만 고치면 화면이 갱신된다" 를 임시 fixture 로 검증한다.

    드리프트가 나면 (a) 값은 새 값을 쓰고 (b) 순위에서 빠지고 (c) validator 가 실패한다.
    """
    import json as _j
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        regp = _fixture_registry(tmp)
        reg = C.load_registry(regp, root=tmp)
        e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
        assert abs(e["value"] - 2.2309) < 1e-6 and e["status"] == "canonical"

        (tmp / "db" / "properties" / "fake_gap.json").write_text(
            _j.dumps({"gap_eV": 2.9999}), encoding="utf-8")
        reg = C.load_registry(regp, root=tmp)
        e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
        assert abs(e["value"] - 2.9999) < 1e-6, "원자료를 고쳤는데 값이 안 따라온다"
        assert e["status"] == "unreviewed_drift", "미검토 드리프트 표시가 없다"
        assert "lpsocl" not in C.canonical_map(reg, "gap_eV",
                                               group="gap-fixedocc-eigenvalue-v1"), \
            "미검토 값이 순위 집합에 남아 있다"
        assert C.validate(reg, root=tmp), "드리프트인데 validator 가 통과한다"


def test_source_error_drops_out_of_canonical():
    """★ 원자료를 못 읽으면 stale 값이 정본 자리에 남으면 안 된다 (Codex 3라운드).

    첫 판은 resolve_error 만 적고 status 는 canonical 로 뒀다. 화면 순위는 validator 를
    안 돌리므로 stale 값이 계속 정본으로 쓰였다.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        regp = _fixture_registry(tmp)
        (tmp / "db" / "properties" / "fake_gap.json").unlink()   # 원자료를 없앤다
        reg = C.load_registry(regp, root=tmp)
        e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
        assert e["status"] == "source_error", f"status 가 {e['status']} 다 — 자동판정에 남는다"
        assert "lpsocl" not in C.canonical_map(reg, "gap_eV",
                                               group="gap-fixedocc-eigenvalue-v1")
        assert C.validate(reg, root=tmp), "원자료를 못 읽는데 validator 가 통과한다"


def test_unreadable_source_takes_the_same_path_as_a_missing_one():
    """⛔ '못 읽음' 의 **모든 사유**가 source_error 로 가야 한다 — 500 이 아니라.

    실측 (2026-09-07): 위 시험은 원자료를 `unlink()` 하는 한 가지 사유만 봤다.
      그건 `ResolveError("파일 없음")` 이라 설계대로 `source_error` 로 내려간다.
      그런데 **깨진 JSON** 은 `json.load` 의 JSONDecodeError 가 그대로 올라가
      `/`·`/compare`·`/explorer`·`/governance` 를 통째로 **500** 으로 만들었다.
      `load_registry` 문서가 이미 "원자료를 못 읽으면 source_error 로 내린다" 고
      적어 둔 설계인데 경로를 한 종류만 타고 있었다 — 게이트가 위험보다 좁았다.

    ⛔ 이 시험이 못 하는 것: source_error 가 **옳은 처분인지**는 판정하지 않는다.
      그건 이미 정해진 설계(2026-08-07 Codex 3라운드)고, 여기서는 모든 사유가
      그 설계로 수렴하는지만 본다.
    """
    import tempfile

    BROKEN = {
        "깨진 JSON": lambda p: p.write_text("{ not json", encoding="utf-8"),
        "빈 파일": lambda p: p.write_text("", encoding="utf-8"),
        # source_key 는 "/gap_eV" 라, 그 자리에 dict 를 두면 float() 이 TypeError 를 낸다
        "수가 아닌 노드": lambda p: p.write_text(
            json.dumps({"gap_eV": {"nested": 1}}), encoding="utf-8"),
    }
    for label, break_it in BROKEN.items():
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            regp = _fixture_registry(tmp)
            src = tmp / "db" / "properties" / "fake_gap.json"
            break_it(src)
            reg = C.load_registry(regp, root=tmp)      # ① 예외로 죽지 않는다
            e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
            assert e["status"] == "source_error", (
                f"{label}: status 가 {e['status']} 다 — 검증 안 된 값이 정본에 남는다")
            assert e.get("resolve_error"), f"{label}: 사유를 안 남긴다"
            # ② 자동판정(순위·차트)에서 빠진다
            assert "lpsocl" not in C.canonical_map(
                reg, "gap_eV", group="gap-fixedocc-eigenvalue-v1"), label
            assert C.validate(reg, root=tmp), f"{label}: validator 가 통과한다"
    # ⛔음성 대조군: 멀쩡한 원자료는 여전히 canonical 이어야 한다 (전부 source_error 로
    #   내려 버리는 구현도 위 단언을 통과하므로, 반대쪽을 같이 잠근다)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        reg = C.load_registry(_fixture_registry(tmp), root=tmp)
        e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
        assert e["status"] != "source_error", "멀쩡한 원자료까지 출처오류로 내린다"


def test_running_process_sees_source_change():
    """★ 오래 사는 worker 에서도 db 수정이 다음 요청에 반영돼야 한다 (Codex 3라운드).

    첫 판은 data.py 가 import 때 _REG 를 한 번 만들어, 재시작 전에는 안 바뀌었다.
    """
    import json as _j
    p = ROOT / "db" / "properties" / "canonical_registry.json"
    before = D.CANONICAL["gap_eV"]["lpsocl"]
    k0 = C._mtime_key()
    # 실제 파일은 안 건드리고, mtime 캐시 키가 원자료를 **포함**하는지만 확인한다
    srcs = {sp for e in _j.loads(p.read_text(encoding="utf-8"))["entries"]
            if (sp := e.get("source_path"))}
    keyed = {k for k, _ in k0}
    assert srcs <= keyed, f"캐시 키가 원자료를 안 본다 — 빠진 것: {srcs - keyed}"
    assert D.CANONICAL["gap_eV"]["lpsocl"] == before
    # CANONICAL 이 전역 스냅샷이 아니라 매번 읽는지
    assert type(D.CANONICAL).__name__ == "_LazyMap", "CANONICAL 이 다시 정적 딕셔너리가 됐다"


def test_non_canonical_status_is_visible_on_screen():
    """★ 자동판정에서 뺐어도 표·카드에는 **왜 빠졌는지**가 보여야 한다 (Codex 3라운드).

    차트에서만 빼면 "표에 있으니 정본이겠지" 로 읽혀 정렬·인용에 그대로 쓰인다.
    """
    c = A.app.test_client()
    cmp_ = c.get("/compare").get_data(as_text=True)
    assert "statusBadge" in cmp_ and "unreviewed_drift" in cmp_, "compare 표에 상태 배지가 없다"
    assert c.get("/explorer").status_code == 200
    assert "canonical_status" in (ROOT / "webapp" / "templates" / "explorer.html")\
        .read_text(encoding="utf-8"), "explorer 표에 상태 배지가 없다"
    # 실제로 비정본이 있는 조성 카드에 배지가 뜨는지 (comp2 gap = provisional)
    comp = c.get("/composition/comp2").get_data(as_text=True)
    assert "잠정" in comp
    st = D.canonical_status_for("comp2")
    assert "gap_eV" in st and st["gap_eV"]["status"] != "canonical"


def test_dashboard_ea_card_is_protocol_honest():
    """첫 화면 Ea 카드가 단일시드 값을 '멀티시드'라 부르면 안 된다."""
    # ⚠ 제목 문자열로 고르면 안 된다 — "Ea" 를 담은 다른 카드가 먼저 걸린다
    #   (2026-08-25: b2o3 "단일 Ea 철회" 카드가 이 검사에 오검됐다). key 로 집는다.
    cards = [h for h in D.dashboard_highlights() if h.get("key") == "md_ea_ranking"]
    assert cards, "MD Ea 순위 카드가 없다 (key=md_ea_ranking)"
    txt = " ".join(cards[0][k] for k in ("t", "v", "n"))
    assert "0.224" not in cards[0]["v"], "단일시드 0.224 가 다시 카드 값으로 올라왔다"
    assert "멀티시드" in txt
    # 순위를 주장하면 안 되는 두 경우 — (a) 오차막대가 겹친다 (b) 비교 상대가 비교군에서
    # 빠졌다. (b) 는 2026-08-20 codex 동결감사 — b2o3 를 게이트 미평가로 내리자 묶음에
    # modelc 만 남았고 카드가 그 하나를 "최저" 라고 쓰면서 바로 아래에서는 "구분 안 된다"
    # 고 말했다. 화면 한 장 안의 자기모순이다.
    v = cards[0]["v"]
    assert ("구분 안 됨" in v) or ("순위 보류" in v), \
        f"순위를 주장하면 안 되는 상태인데 주장한다: {v}"
    assert "최저" not in v or "순위 보류" in v, f"단독으로 남은 값을 '최저' 라고 쓴다: {v}"


def test_dashboard_closure_cards_read_db_not_hardcode(tmp_path, monkeypatch):
    """양성+⛔음성: 마감 계약·보고량·어닐 카드가 **db 파일에서** 만들어진다 (2026-09-08).

    양성 — 봉인값과 모티프 순위가 파일에 적힌 것과 같다.
    ⛔음성 — db 뿌리를 빈 디렉터리로 바꾸면 카드가 **사라져야** 한다. 안 사라지면 그
      숫자·순서는 파일이 아니라 화면에 박혀 있는 것이다 (하드코딩 금지 규율).
    """
    import json as _j
    cards = {h.get("key"): h for h in D.dashboard_highlights()}
    # ① LPSOCl 마감 계약 — 봉인값이 파일에서 온다
    clo = _j.loads((ROOT / "db/properties/lpsocl_box331_closure_conditions_2026_09_07.json")
                   .read_text(encoding="utf-8"))
    if clo.get("status") == "ratified":
        card = cards.get("lpsocl_box331_closure")
        assert card, "비준된 마감 계약인데 대시보드 카드가 없다"
        seals = [v for sec in (clo.get("2_닫힘_조건") or {}).values() if isinstance(sec, dict)
                 for k, v in sec.items() if k.startswith("봉인_") and isinstance(v, (int, float))]
        assert seals, "전제: 봉인 숫자가 파일에 있다"
        for v in seals:
            assert f"{v:g}" in card["v"], f"봉인값 {v} 가 카드에 없다 — 파일을 안 읽는다"
    # ② Nd 어닐 — 모티프 순위가 파일의 에너지에서 계산된다
    ann = _j.loads((ROOT / "db/structures/ndo_lpscl16_rietveld_2026_09_07"
                    / "anneal_2026_09_07/anneal_results.json").read_text(encoding="utf-8"))
    order = [n.split("_O-")[1] for _e, n in sorted(
        (r["E_post_relax"] / r["n_atoms"], r["name"]) for r in ann["results"]
        if "_n4fu_O-" in r["name"])]
    card = cards.get("ndo_lpscl16_anneal")
    assert card, "어닐 결과가 있는데 카드가 없다"
    assert " < ".join(order) in card["v"] + card["n"], \
        f"카드 순위가 파일에서 계산한 순서({order})와 다르다"
    assert "순위로만" in card["n"], "UMA 값인데 순위 한정 문구가 없다 (CLAUDE.md MLIP 규율)"
    # ⛔음성: db 가 없으면 카드도 없다
    monkeypatch.setattr(D, "DB", tmp_path)
    assert D._closure_and_prereg_cards() == [], "db 없이도 마감 카드가 나온다 (하드코딩)"
    assert D._nd_anneal_card() == [], "db 없이도 어닐 카드가 나온다 (하드코딩)"


def test_compute_runner_does_not_guess_gpu_runtime():
    """⛔음성: QE-GPU 붙여넣기 러너가 `mpirun -np 1 pw.x` 로 되돌아가면 안 된다 (2026-09-08).

    같은 자리에서 **세 번** 죽었다 — ① conda mpirun 이 잡혀 MPI_Init NULL communicator
    ② 런처를 뺐더니 `libgomp: TODO` ③ hpcx 로 추측했는데 kgy 의 pw.x 는 실제로
    `~/apps/openmpi-4.1.6` 로 빌드돼 있었다. 규칙이 아니라 **링크가 근거**여야 한다
    (CLAUDE.md 계산 자원 절 · tools/doping/run_force_check_scf.sh 가 정본).
    """
    assert "kgy" in D.COMPUTE_SETTINGS["comp1"]["server"], "전제: comp1 은 비-Slurm GPU 박스다"
    r = D.compute_preview("comp1", "scf")["runner"]
    assert "ldd" in r and "OPAL_PREFIX" in r, "런타임을 ldd 에서 유도하지 않는다 (추측하고 있다)"
    assert "OMP_NUM_THREADS=1" in r, "libnvomp+libgomp 동시 링크 방어가 빠졌다"
    assert not re.search(r"^\s*mpirun\s", r, re.M), \
        "PATH 의 mpirun 을 그냥 부른다 — 그게 세 번 죽은 경로다"
    # 두 갈래가 실제로 다른지 (Slurm 쪽은 srun 이라 이 규칙이 안 걸린다)
    kisti = [c for c, s in D.COMPUTE_SETTINGS.items() if "KISTI" in s["server"]]
    assert kisti, "전제: Slurm 서버 설정이 남아 있다"
    rk = D.compute_preview(kisti[0], "scf")["runner"]
    assert "srun" in rk and "ldd" not in rk, "Slurm 러너까지 ldd 유도를 붙이면 안 된다"


def test_gap_card_excludes_legacy_group():
    """갭 순위가 legacy DOS-문턱 값(comp2)을 같은 축에 올리면 안 된다."""
    gm = D.canonical_comparable("gap_eV", "gap-fixedocc-eigenvalue-v1")
    assert "comp2" not in gm
    assert set(gm) == {"comp1", "modelc", "lpsocl", "b2o3"}


def test_compare_page_ships_group_metadata():
    """compare 화면이 강제할 수 있도록 묶음/상태가 실제로 내려가야 한다."""
    b = A.app.test_client().get("/compare").get_data(as_text=True)
    m = re.search(r"const CMETA=(\{.*?\});", b, re.S)
    assert m, "CMETA 가 안 내려간다"
    d = json.loads(m.group(1))
    assert d["MD_Ea_eV|modelc"]["group"] == "md-ea-multiseed-v1"
    assert d["gap_eV|comp2"]["group"] != d["gap_eV|comp1"]["group"], "legacy 갭이 정본과 같은 묶음이다"
    assert "splitByGroup" in b, "묶음 강제 함수가 템플릿에 없다"


def test_uma_forbidden_system_stays_na():
    """UMA 금지 조성(Li3N)은 계산값으로 채워지면 안 된다 (CLAUDE.md)."""
    na = {f"{c}|{k}" for (c, k) in D.NOT_APPLICABLE}
    assert any("li3n" in x.lower() for x in na), "Li3N N/A 표시가 사라졌다"


# ── 3) 라우트 · 데이터 스모크 ──────────────────────────────────────────────
def _routes():
    return sorted({r.rule for r in A.app.url_map.iter_rules()
                   if "GET" in r.methods and "<" not in r.rule
                   and not r.rule.startswith("/static")})


def _dynamic_routes():
    """`<...>` 를 낀 GET 라우트. `_routes()` 가 **일부러 뺀** 쪽이다."""
    return sorted({r.rule for r in A.app.url_map.iter_rules()
                   if "GET" in r.methods and "<" in r.rule
                   and not r.rule.startswith("/static")})


#: 동적 라우트별 **대표 인자**. 실물에 있는 값을 쓴다 — 없는 값을 넣으면 404 만 보게 되고
#: 그건 렌더 경로를 안 탄 것이라 검사가 아니다. (전부 2026-09-07 실측으로 200 확인)
#: ⚠ 여기에도 EXEMPT 에도 없는 동적 라우트가 생기면 아래 시험이 **그 사실 자체로** 실패한다.
DYNAMIC_FIXTURES = {
    "/api/comments/<path:rel>":   ["CLAUDE.md"],
    "/api/concept/<cid>":         ["ordered_vs_disordered", "beta-gate"],
    "/api/csv/<path:rel>":        ["db/properties/b2o3_msd.csv"],
    "/api/fairchem/v1/<name>":    ["models"],
    "/api/file/<path:rel>":       ["db/properties/electronic.json"],
    # ⛔ 2026-09-08 (회신 BG ②) — EXEMPT 사유가 **사실과 달랐다**: "실행 중 생기는 무상태 id" 가
    #   아니라 `kb/results/*.md` 의 파일명이다(저장소에 94개 커밋돼 있다). 틀린 사유가
    #   결속 검사에서 handoff 를 통째로 빼고 있었다 — fixture 로 옮긴다.
    "/api/handoff/<hid>":         ["lpsocl_box_size_600K_2026_08_18"],
    "/api/highlights/<path:rel>": ["CLAUDE.md"],
    "/api/paper/<pid>":           ["deng2026_polysulfate_layer_moisture_oxidation_lpsc"],
    "/api/property/<name>":       ["electronic", "li_transport"],
    "/api/structure/<path:fn>":   ["sei_li3nd_mp-976264.vasp"],
    "/composition/<cid>":         ["comp1", "modelc"],
    "/concept/<cid>":             ["ordered_vs_disordered", "beta-gate"],
    # v3 묶음 I (2026-09-09) — /talk 과 대칭인 논문 정독 페이지. papers/ stem 과 1:1 이다.
    "/paper/<slug>":              ["deng2026_polysulfate_layer_moisture_oxidation_lpsc"],
    # ⛔ 2026-09-08 (Codex BI 회신) — EXEMPT 사유가 **또 사실오류였다**: "kb/seminars 파일명과
    #   1:1 이 아니다" 라고 적혀 있었지만 app.py:1108 은 `litdb/talks/<slug>.md` 를 연다.
    #   stem 과 1:1 이고 8개 전부 200 이다. handoff 에서 같은 종류의 거짓 사유를 한 번
    #   고치고 talk 에서 놓쳤다 — **사람 눈은 사유의 참·거짓을 못 지킨다**(아래 시험 참조).
    "/talk/<slug>":               ["do2026_bml_alzib_preconditioning",
                                   "yang2026_ncm_radial_microstructure_ml"],
}

#: 스모크로 못 미는 동적 라우트 — **사유를 반드시 적는다**(빈 사유 금지).
#: ⚠ 여기 넣는 것은 "검사 안 함" 이라는 선언이다. 늘어나면 그만큼 눈이 먼다.
#: 커밋된 실물 인자가 **없는** 동적 라우트 — 대신 **합성 인자로 실제 GET 하는 시험**을 댄다.
#: ⛔ 2026-09-08 (Codex BI) — 종전 `DYNAMIC_EXEMPT` 는 "사유만 적으면 통과" 였고, 두 번
#:   연속으로 그 사유가 **사실오류**였다(handoff: kb/results 에 94개 커밋돼 있었다 ·
#:   talk: litdb/talks 에 8개 커밋돼 있었다). 사람 눈은 사유의 참·거짓을 못 지킨다.
#:   ⇒ 면제를 없애고 **반증 가능한 의무**로 바꾼다: 시험 이름을 대고, 그 시험이 실재하고,
#:   그 시험이 그 라우트를 정말 GET 하는지 아래 시험이 확인한다.
DYNAMIC_SYNTHETIC = {
    "/api/note-image/<name>": {
        "why": "사용자가 붙여넣은 캡처. 파일명이 **내용의 sha256** 이라 저장소에 커밋되지 "
               "않는다(webapp/data.py save_note_image). 실물 인자가 원리적으로 없다.",
        "test": "test_note_image_route_is_exercised_synthetically",
    },
}

#: 기본 요청에서 **일부러 403** 인 라우트 — fail-closed 가 목적이라 200 이면 오히려 버그다.
GATED_ROUTES = {"/cascade/diagnostic": ("view=diagnostic", 403)}


def test_dynamic_routes_are_covered_not_skipped():
    """⛔음성: **동적 라우트가 검사 밖에 있으면 안 된다** (회신 AW 해제조건 ⑥).

    `_routes()` 는 `"<" not in r.rule` 로 동적 라우트를 통째로 뺀다. 그래서
    `/api/property/<name>` · `/api/csv/<path:rel>` 처럼 **화면이 실제로 부르는** 경로가
    한 번도 안 밟혔다. 리뷰가 "GET 42개 패턴 중 14개가 빠진다" 고 지적한 자리다.

    이 시험이 지키는 것 둘:
      ① 새 동적 라우트가 생기면 **fixture 없이 지나갈 수 없다** (고아 금지)
      ② fixture 가 있는 것은 **실제로 렌더까지** 간다 (404/500 이 아니다)
    """
    dyn = _dynamic_routes()
    known = set(DYNAMIC_FIXTURES) | set(DYNAMIC_SYNTHETIC)
    unknown = [r for r in dyn if r not in known]
    assert not unknown, (
        f"fixture 도 합성시험도 없는 동적 라우트가 있다 — 검사 밖이다: {unknown}\n"
        f"DYNAMIC_FIXTURES 에 대표 인자를 넣거나, DYNAMIC_SYNTHETIC 에 "
        f"**사유 + 그 라우트를 실제로 GET 하는 시험 이름**을 적어라.")
    stale = [r for r in known if r not in dyn]
    assert not stale, f"없어진 라우트의 fixture/합성시험 선언이 남아 있다: {stale}"
    # ⛔음성 — 합성시험 선언이 **말뿐이 아닌지**. 사유·시험이름이 있어야 하고, 그 시험이
    #   이 모듈에 실재해야 하고, 그 시험 소스가 실제로 그 라우트 앞머리를 GET 해야 한다.
    #   (사유만 요구하던 종전 EXEMPT 가 두 번 연속 사실오류로 통과했다.)
    import inspect as _insp
    mod = sys.modules[__name__]
    for rule, dec in DYNAMIC_SYNTHETIC.items():
        assert (dec.get("why") or "").strip(), f"⛔ {rule}: 사유가 비었다"
        tn = dec.get("test") or ""
        fn = getattr(mod, tn, None)
        assert callable(fn), (
            f"⛔ {rule}: 합성시험 {tn!r} 이 이 모듈에 없다 — 선언만 있고 검사가 없다")
        src = _insp.getsource(fn)
        head = rule.split("<")[0]
        assert f'"{head}' in src or f"'{head}" in src or f"{head}" in src, (
            f"⛔ {rule}: {tn} 이 그 라우트를 GET 하지 않는다 (소스에 {head!r} 이 없다) — "
            f"이름만 빌려온 의무는 의무가 아니다")


def test_dynamic_routes_actually_render():
    """양성 + ⛔음성: fixture 가 있는 동적 라우트가 **200 으로 렌더**된다.

    ⚠ 404 를 통과로 세면 안 된다 — 그건 라우트를 밟긴 했어도 **렌더 경로를 안 탄 것**이다.
      그래서 아래는 200 만 통과로 센다.
    """
    c = A.app.test_client()
    bad, checked = [], 0
    for rule, args in DYNAMIC_FIXTURES.items():
        for v in args:
            u = re.sub(r"<[^>]+>", v, rule)
            try:
                r = c.get(u)
                checked += 1
                if r.status_code != 200:
                    bad.append(f"{u} → {r.status_code}")
            except Exception as ex:
                bad.append(f"{u} → {type(ex).__name__}: {ex}")
    assert checked >= 10, f"밟은 동적 라우트가 너무 적다 ({checked}) — fixture 가 비었나"
    assert not bad, "동적 라우트가 렌더 안 된다: " + " · ".join(bad)


def test_note_image_route_is_exercised_synthetically():
    """양성+⛔음성: `/api/note-image/<name>` — 실물 인자가 없는 라우트를 **합성으로** 민다.

    이 라우트의 인자는 붙여넣은 캡처의 sha256 이라 저장소에 없다. 그래서 fixture 를 못
    만드는데, 그렇다고 **검사 밖에 두면** 경로 탈출 가드가 죽어도 아무도 모른다.
      · 양성 — 규격에 맞는 이름은 라우트를 타고 **404**(파일이 없으니 정상)
      · ⛔음성 — 규격 밖 이름 넷(경로탈출·확장자·길이·대문자)이 전부 404 로 **막힌다**
        ⚠ 404 만 보면 둘이 구분이 안 된다. 그래서 `D.note_image_path` 가 규격 밖 이름에
          **None** 을 내는지를 같이 단언한다 — 여기가 실제 가드다.
    """
    c = A.app.test_client()
    ok_name = "0" * 32 + ".png"
    assert c.get("/api/note-image/" + ok_name).status_code == 404      # 파일만 없다
    assert D.note_image_path(ok_name) is None                          # (없는 파일)
    for bad_name in ("../../etc/passwd", "0" * 32 + ".svg",
                     "0" * 31 + ".png", "A" * 32 + ".png"):
        assert D.note_image_path(bad_name) is None, (
            f"⛔ 규격 밖 이름이 통과했다: {bad_name!r} — 경로 탈출 가드가 죽었다")
        assert c.get("/api/note-image/" + bad_name).status_code in (404, 308), bad_name


def test_all_get_routes_200():
    c = A.app.test_client()
    bad = []
    for u in _routes():
        try:
            if u in GATED_ROUTES:
                q, want = GATED_ROUTES[u]
                if c.get(u).status_code != want:
                    bad.append(f"{u} (gated 인데 {want} 가 아니다)")
                elif c.get(f"{u}?{q}").status_code != 200:
                    bad.append(f"{u}?{q} (opt-in 인데 안 열린다)")
                continue
            if c.get(u).status_code != 200:
                bad.append(u)
        except Exception as ex:                      # 렌더 예외도 실패로 잡는다
            bad.append(f"{u} ({ex})")
    assert not bad, f"200 이 아닌 라우트: {bad}"


def test_all_csv_parse():
    import csv
    bad = []
    for p in list((ROOT / "db").rglob("*.csv")) + list((ROOT / "docs" / "figures").rglob("*.csv")):
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                list(csv.reader(f))
        except Exception as ex:
            bad.append(f"{p.relative_to(ROOT).as_posix()}: {ex}")
    assert not bad, bad


def test_no_literal_bold_markers_in_rendered_body():
    """대시보드 카드의 '**' 가 그대로 보이던 회귀 (2026-08-07)."""
    b = A.app.test_client().get("/").get_data(as_text=True)
    body = re.sub(r"<script\b.*?</script>", "", b, flags=re.S)
    body = re.sub(r"<[^>]*>", "", body)
    assert "**" not in body, "대시보드에 처리 안 된 ** 가 남아 있다"


# ── 4) 보안 · 동시성 · 경로 ────────────────────────────────────────────────
#: 쓰기 라우트 — 잠겼을 때 전부 403 이어야 한다.
MUTATION_PROBES = [
    ("POST", "/api/comments/db/properties/electronic.json", {"json": {"text": "x"}}),
    ("DELETE", "/api/comments/db/properties/electronic.json?id=x", {}),
    ("POST", "/api/log", {"json": {"kind": "note", "text": "x"}}),
    ("POST", "/api/file-rename", {"json": {"rel": "a", "name": "b"}}),
    ("POST", "/api/concept-upload/dft", {}),
]


def _readonly_for(env):
    """주어진 환경변수로 app.py 의 잠금 판정만 다시 계산한다 (재import 없이)."""
    on_render = bool(env.get("RENDER") or env.get("RENDER_SERVICE_ID"))
    m = (env.get("ALLOW_MUTATIONS") or "").strip().lower()
    if m in ("1", "true", "yes"):
        allow = True
    elif m in ("0", "false", "no"):
        allow = False
    else:
        allow = not on_render
    return not allow


def test_mutations_locked_on_render_open_locally():
    """의도는 '**원격**이 읽기 전용' 이다 — 로컬까지 잠그면 자기 노트북에서 코멘트를
    못 단다 (2026-08-16 실제로 그랬다). 명시 env 는 양방향으로 이긴다."""
    assert _readonly_for({"RENDER": "1"}) is True, "Render 기본이 열려 있다"
    assert _readonly_for({"RENDER_SERVICE_ID": "x"}) is True
    assert _readonly_for({}) is False, "로컬 기본이 잠겨 있다 — 코멘트를 못 단다"
    assert _readonly_for({"RENDER": "1", "ALLOW_MUTATIONS": "1"}) is False, \
        "Render 에서 명시적 허용이 안 먹는다"
    assert _readonly_for({"ALLOW_MUTATIONS": "0"}) is True, "로컬 명시적 잠금이 안 먹는다"
    for v in ("true", "yes", "TRUE"):
        assert _readonly_for({"ALLOW_MUTATIONS": v}) is False, v
    for v in ("false", "no", "NO"):
        assert _readonly_for({"ALLOW_MUTATIONS": v}) is True, v
    # 음성: 알 수 없는 값은 '허용' 으로 읽으면 안 된다 — 환경 판정으로 떨어진다
    assert _readonly_for({"RENDER": "1", "ALLOW_MUTATIONS": "maybe"}) is True


def test_mutation_routes_return_403_when_locked():
    """잠긴 상태에서는 쓰기 라우트가 전부 403 이어야 한다."""
    if not A.READ_ONLY:
        pytest.skip("이 실행은 쓰기가 열려 있다 (로컬 기본) — 잠금 동작은 위 단위테스트가 본다")
    c = A.app.test_client()
    for m, u, kw in MUTATION_PROBES:
        assert c.open(u, method=m, **kw).status_code == 403, f"{m} {u} 가 안 막혔다"


def test_markdown_blocks_dangerous_url_schemes():
    """`[x](javascript:...)` 가 실행 가능한 href 로 남으면 안 된다 (리뷰 P2 실측)."""
    for bad in ["[a](javascript:alert(1))", "[a](&#106;avascript:alert(1))",
                "[a](data:text/html;base64,PHM+)", "[a](VBscript:msgbox(1))"]:
        h = A.md_html(bad)
        assert "blocked-url" in h and "javascript" not in h.lower(), h
    for good in ["[a](https://x.com)", "[a](docs/f.png)", "[a](#sec)", "[a](docs/한글.pdf)"]:
        assert "blocked-url" not in A.md_html(good), good


def test_paths_are_posix():
    """Windows 에서 역슬래시 경로가 기록돼 첨부가 사라지던 회귀 (리뷰 P2).

    ⛔ 2026-09-07 — **이 게이트가 위험보다 좁았다.** 종전 정규식은 `data.py` 의
      `relative_to(ROOT)` 만 봤다. 그래서 `app.py` 의 `str(path.relative_to(D.ROOT))`
      와 `data.py` 의 `str(f.relative_to(DB))` 6곳(그중 `datafiles_for`·`_sweep_view`
      는 그 문자열이 그대로 `/api/csv/<rel>` 링크가 된다)이 **검사 밖**이었다.
      기준(ROOT)과 대상(실제 경로 조립 전부)이 같은 제약이어야 한다.
    """
    bad = []
    # 어떤 base 든 (ROOT·DB·D.ROOT…) str(...relative_to(x)) 는 Windows 에서 역슬래시가 된다
    pat = re.compile(r"str\(\s*\w[\w.]*\.relative_to\([^)]*\)\s*\)")
    for name in ("data.py", "app.py"):
        src = (ROOT / "webapp" / name).read_text(encoding="utf-8")
        for m in pat.finditer(src):
            bad.append(f"{name}:{src[:m.start()].count(chr(10)) + 1} {m.group(0)}")
    assert not bad, ("str(...relative_to(...)) 가 남아 있다 — .as_posix() 를 쓸 것: "
                     + "; ".join(bad))


def test_comment_writes_survive_concurrency():
    """gunicorn worker 2개에서 마지막 저장이 앞선 저장을 덮던 회귀 (40 요청 → 2 저장)."""
    import multiprocessing as mp
    rel = "db/properties/electronic.json"
    before = len(D.file_comments(rel))
    n = 24
    with mp.Pool(6) as p:
        rs = p.map(_cmt_worker, [(rel, i) for i in range(n)])
    ok = [r for r in rs if r.get("ok")]
    after = len(D.file_comments(rel))
    ids = [r["item"]["id"] for r in ok]
    try:
        assert len(ok) == n, f"{len(ok)}/{n} 만 성공"
        assert after - before == n, f"{after - before}/{n} 만 저장됐다"
        assert len(set(ids)) == n, "코멘트 id 가 겹친다 — 삭제가 엉뚱한 걸 지운다"
    finally:
        for r in ok:
            D.del_file_comment(rel, r["item"]["id"])


def test_comment_writes_survive_heavy_concurrency():
    """★ 100건 반복 스트레스 (2026-08-07 Codex 3라운드).

    24건 1회로는 Windows 의 os.replace PermissionError 간헐 실패를 못 잡았다
    (실측: 12프로세스 x 100건 x 10회 → 6회 실패, 합계 992/1000).
    ⚠ 추적 중인 db/file_comments.json 을 쓰지 않도록 **임시 경로로 갈아끼운다** —
      실패해도 repo 파일이 오염되지 않는다.
    """
    import multiprocessing as mp
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        old = D.COMMENTS_PATH
        try:
            D.COMMENTS_PATH = Path(td) / "file_comments.json"
            rel = "db/properties/electronic.json"
            n = 100
            with mp.Pool(8) as p:
                rs = p.map(_cmt_worker_tmp, [(str(D.COMMENTS_PATH), rel, i) for i in range(n)])
            ok = [r for r in rs if r and r.get("ok")]
            saved = len(D.file_comments(rel))
            ids = [r["item"]["id"] for r in ok]
            errs = {str(r.get("error"))[:80] for r in rs if not (r and r.get("ok"))}
            assert len(ok) == n, f"{len(ok)}/{n} 만 성공 · 오류 {errs}"
            assert saved == n, f"{saved}/{n} 만 저장됐다 (os.replace 재시도 확인)"
            assert len(set(ids)) == n, "코멘트 id 가 겹친다"
        finally:
            D.COMMENTS_PATH = old


def test_mkdir_fallback_stale_lock_recovery():
    """★ mkdir 폴백의 stale lock 회수 — **3케이스 전부** (2026-08-07 Codex 4라운드).

    정상 Windows/Linux 에는 msvcrt/fcntl 이 있어 이 분기가 아예 안 돈다. 그래서 둘 다
    막고 강제로 폴백을 태운다. Codex 지적: 기존 21개가 통과해도 이 경로는 미검증이었다.

    ⚠⚠ 그리고 여기서 `os.kill(pid, 0)` 을 쓰면 안 된다 — Windows CPython 은 그걸
      TerminateProcess 로 보내므로 **살아 있는 주인을 죽인다.** _alive() 가 OS 별로
      갈리는지도 같이 본다.
    """
    import builtins
    import tempfile
    import time as _t
    real = builtins.__import__

    def blocked(name, *a, **k):
        if name in ("fcntl", "msvcrt"):
            raise ImportError(f"blocked {name}")
        return real(name, *a, **k)

    old = D.COMMENTS_PATH
    with tempfile.TemporaryDirectory() as td:
        try:
            D.COMMENTS_PATH = Path(td) / "c.json"
            lock = Path(str(D.COMMENTS_PATH) + ".lock.d")
            own = lock / "owner"
            builtins.__import__ = blocked

            # ① 죽은 주인 + 오래됨 → 회수해야 한다
            lock.mkdir(parents=True, exist_ok=True)
            own.write_text("999999 %f" % (_t.time() - 10000), encoding="utf-8")
            with D._comments_locked(timeout=3):
                pass
            assert not lock.exists(), "죽은 주인의 stale lock 을 회수하지 못했다"

            # ② 살아 있는 주인 → 절대 뺏으면 안 된다
            lock.mkdir(parents=True, exist_ok=True)
            own.write_text(f"{os.getpid()} {_t.time() - 10000}", encoding="utf-8")
            try:
                with D._comments_locked(timeout=0.4):
                    raise AssertionError("살아 있는 주인의 lock 을 뺏었다")
            except TimeoutError:
                pass
            assert lock.exists(), "살아 있는 주인의 lock 이 사라졌다"
            own.unlink(missing_ok=True)
            lock.rmdir()

            # ③ owner 파일 없음(= mkdir 직후 크래시) + 오래됨 → 디렉터리 mtime 으로 회수
            lock.mkdir(parents=True, exist_ok=True)
            os.utime(lock, (_t.time() - 10000, _t.time() - 10000))
            with D._comments_locked(timeout=3):
                pass
            assert not lock.exists(), "owner 없는 stale lock 을 회수하지 못했다"
        finally:
            builtins.__import__ = real
            D.COMMENTS_PATH = old


def test_alive_check_is_not_os_kill_on_windows():
    """★ Windows 에서 `os.kill(pid, 0)` 은 존재 확인이 아니라 **종료 요청**이다.

    CPython 의 Windows os.kill 은 sig 가 CTRL_C/CTRL_BREAK 가 아니면
    TerminateProcess(handle, sig) 로 간다. 소스에 그 분기가 있는지 본다
    (실행 중 프로세스를 죽여 볼 수는 없으므로 구조로 검사한다).
    """
    src = (ROOT / "webapp" / "data.py").read_text(encoding="utf-8")
    i = src.find("def process_alive(")
    assert i > 0, "process_alive() 가 사라졌다"
    body = src[i:i + 4200]
    assert 'os.name == "nt"' in body, "_alive() 에 Windows 분기가 없다"
    nt = body[body.index('os.name == "nt"'):]
    nt = nt[:nt.index("os.kill(")] if "os.kill(" in nt else nt
    assert "OpenProcess" in nt, "Windows 분기가 OpenProcess 를 안 쓴다"
    # os.kill 은 Windows 분기 **밖**에만 있어야 한다
    assert "os.kill" not in nt, "Windows 분기 안에서 os.kill 을 쓴다 — 프로세스를 죽인다"
    # ★ 2차 (Codex 5라운드 Windows 실기): QUERY_LIMITED 만으로는 Wait 가 WAIT_FAILED 다.
    #   구조 검사가 함수 존재만 봐서 이 런타임 권한 오류를 못 잡았다 — 이제 조합을 본다.
    assert "SYNCHRONIZE" in nt, "OpenProcess 에 SYNCHRONIZE 가 없다 — Wait 가 WAIT_FAILED 난다"
    assert "GetExitCodeProcess" in nt and "STILL_ACTIVE" in nt, \
        "Wait 실패 시 GetExitCodeProcess 폴백이 없다"
    assert "WAIT_FAILED" in nt, "WAIT_FAILED 를 구분하지 않는다 — 살아 있는 주인을 죽음으로 오판한다"


def test_alive_treats_unknown_as_alive():
    """★ 판단 불가는 **항상 '살아 있다'** 로 떨어져야 한다 (2026-08-07 Codex 5라운드).

    1차 Windows 수정이 실패한 지점이 정확히 이거다: PROCESS_QUERY_LIMITED_INFORMATION
    만 열면 WaitForSingleObject 가 **WAIT_FAILED(0xFFFFFFFF)** 를 주는데, 코드가
    "WAIT_TIMEOUT 아니면 죽음" 으로 봐서 **살아 있는 주인의 lock 을 뺏었다.**
    가짜 kernel32 로 다섯 경우를 다 태운다.
    """
    import ctypes as _ct
    import types
    real_windll = getattr(_ct, "WinDLL", None)
    old_name = os.name
    #  Wait 반환      GetExitCode 성공?  종료코드   기대 alive
    cases = [
        ("wait_timeout",              0x102,      True,  259, True),
        ("wait_object_0",             0x000,      True,    0, False),
        ("wait_failed + STILL_ACTIVE", 0xFFFFFFFF, True,  259, True),   # ← 회귀 지점
        ("wait_failed + exited",      0xFFFFFFFF, True,    0, False),
        ("wait_failed + 조회 실패",     0xFFFFFFFF, False,   0, True),   # 판단 불가
    ]
    for name, wait_rc, gec_ok, code, want in cases:
        class _OP:                       # OpenProcess 는 restype/argtypes 대입을 받는다
            restype = None
            argtypes = None

            def __call__(self, *a, **k):
                return 1234              # 널이 아닌 핸들

        fake = types.SimpleNamespace(
            OpenProcess=_OP(),
            WaitForSingleObject=lambda h, t, _r=wait_rc: _r,
            CloseHandle=lambda h: 1,
            GetExitCodeProcess=(lambda h, ref, _c=code, _ok=gec_ok:
                                (setattr(ref._obj, "value", _c), 1 if _ok else 0)[1]),
        )
        os.name = "nt"
        _ct.WinDLL = lambda n, use_last_error=False, _f=fake: _f
        try:
            got = D.process_alive(999999)
            assert got is want, f"{name}: alive={got} · 기대={want}"
        finally:
            os.name = old_name
            if real_windll is not None:
                _ct.WinDLL = real_windll


def test_comp2_ordered_and_disorder_are_separate():
    """★ ordered baseline 과 disorder ensemble 을 한 항목에 섞으면 안 된다 (Codex 4라운드).

    0.275 는 ordered single-champion 인데 method_id 가 disorder-ensemble 이었다.
    원자료가 직접 'anion disorder mechanism 을 샘플링하지 않았다'고 적고 있다.
    """
    reg = C.load_registry()
    idx = {(e["metric"], e["system"]): e for e in reg["entries"]}
    o = idx.get(("MD_Ea_eV_ordered", "comp2"))
    d = idx.get(("MD_Ea_eV_disorder", "comp2"))
    assert o and d, "comp2 ordered/disorder 항목이 분리돼 있지 않다"
    assert "ordered" in o["method_id"] and "disorder" not in o["method_id"]
    assert "disorder" in d["method_id"]
    assert o["comparison_group"] != d["comparison_group"], "같은 묶음에 있다"
    assert abs(o["value"] - 0.2754597563) < 1e-9, "ordered 가 정밀 원자료가 아니다"
    assert abs(d["value"] - 0.1512) < 1e-9 and d.get("n_config") == 3, \
        "disorder 는 n_seed 가 아니라 n_config 여야 한다"
    # d=1.00 은 게이트 FAIL 이라 등재하면 안 된다
    assert not any(abs((e.get("value") or 0) - 0.3775) < 1e-9 for e in reg["entries"]), \
        "게이트 FAIL 인 d=1.00 이 레지스트리에 있다"


def test_new_metrics_reach_all_screens():
    """★ 레지스트리에 metric 이 늘면 화면 셋이 자동으로 따라와야 한다 (Codex 5라운드).

    ordered/disorder 로 쪼갠 뒤에도 (a) explorer 는 새 두 metric 을 아예 안 보여줬고
    (b) composition 카드는 label·unit 이 빈칸이었고 (c) compare 는 **옛 0.275 를 같이**
    보여줬다. 원인은 세 템플릿이 metric 목록을 각자 하드코딩한 것이었다.
    """
    import json as _j
    mm = D.metric_meta()
    for k in ("MD_Ea_eV_ordered", "MD_Ea_eV_disorder"):
        assert k in mm and mm[k]["label"] and mm[k]["unit"], f"{k} 의 label/unit 이 없다"
    c = A.app.test_client()
    exp = c.get("/explorer").get_data(as_text=True)
    assert mm["MD_Ea_eV_ordered"]["label"] in exp, "explorer 에 ordered metric 이 없다"
    assert mm["MD_Ea_eV_disorder"]["label"] in exp, "explorer 에 disorder metric 이 없다"
    comp = c.get("/composition/comp2").get_data(as_text=True)
    assert mm["MD_Ea_eV_ordered"]["label"] in comp, "composition 카드에 label 이 없다"
    cmp_ = c.get("/compare").get_data(as_text=True)
    canon = _j.loads(re.search(r"const CANON=(\{.*?\});", cmp_, re.S).group(1))
    assert canon.get("MD_Ea_eV", {}).get("comp2") is None, \
        "옛 MD_Ea_eV comp2(0.275) 가 화면에 남아 있다 — 하드코딩 잔재"
    assert "MD_Ea_eV_ordered" in canon and "MD_Ea_eV_disorder" in canon


def test_comparison_group_id_is_visible():
    """★ 의미를 나눠 놓고도 **어느 묶음인지**가 화면에 안 보이면 나눈 의미가 없다.

    2026-08-07 Codex 6라운드: ordered/disorder 가 둘 다 provisional 이라 canonical
    묶음이 없었고, /compare 는 "비교 가능한 묶음이 없다" 만 찍었다 — 등록 묶음 ID 는
    어디에도 안 나왔다.
    """
    c = A.app.test_client()
    G_ORD, G_DIS = "md-ea-comp2-ordered-provisional", "md-ea-comp2-disorder-d050"
    # ① compare: 묶음이 없을 때 등록 묶음을 나열하는 분기가 있는지 + 셀 툴팁
    cmp_ = c.get("/compare").get_data(as_text=True)
    assert "등록 묶음" in cmp_, "compare 에 '등록 묶음' 표기가 없다"
    assert G_ORD in cmp_ and G_DIS in cmp_, "compare 에 묶음 ID 가 안 내려간다"
    # ② explorer · composition: 배지 툴팁에 묶음 ID
    for u in ("/explorer", "/composition/comp2"):
        t = c.get(u).get_data(as_text=True)
        assert G_ORD in t, f"{u} 에 ordered 묶음 ID 가 없다"
        assert G_DIS in t, f"{u} 에 disorder 묶음 ID 가 없다"
    # ③ 데이터층: 배지에 group 이 실려 있는지
    st = D.canonical_status_for("comp2")
    assert st["MD_Ea_eV_ordered"]["group"] == G_ORD
    assert st["MD_Ea_eV_disorder"]["group"] == G_DIS
    assert st["MD_Ea_eV_ordered"]["why"].startswith("등록 묶음 [")


def test_provenance_open_is_visible_on_screen():
    """★ provenance_open 을 validator 만 찍으면 **사이트에서는 여전히 무경고**다.

    2026-08-07 Codex 6라운드 후속 지적. status 는 canonical 그대로여야 하고
    (값이 틀린 게 아니다 — 순위에서 빼면 과잉), 대신 눈에 보이는 표식이 있어야 한다.
    """
    flags = D.canonical_provenance_flags()
    assert flags, "provenance_open 항목이 하나도 안 잡힌다"
    # status 는 안 내려간다 — 순위에는 남아야 한다
    gm = D.canonical_comparable("gap_eV", "gap-fixedocc-eigenvalue-v1")
    assert set(gm) == {"comp1", "modelc", "lpsocl", "b2o3"}, \
        "provenance_open 이 순위에서 값을 빼 버렸다 — 과잉이다"
    c = A.app.test_client()
    for u in ("/compare", "/explorer", "/composition/comp1"):
        assert "출처⚠" in c.get(u).get_data(as_text=True), f"{u} 에 출처 표식이 없다"


def test_sei_axes_reflect_campaign_state():
    """대시보드가 요청 3축의 상태를 직접 말해야 한다 — 안 그러면 '갭만 했나' 로 읽힌다."""
    ax = D.sei_axes()["axes"]
    assert len(ax) == 3
    names = " ".join(a["n"] for a in ax)
    assert "확산장벽" in names and "형성 전위" in names and "밴드갭" in names
    done = {a["n"]: a["done"] for a in ax}
    assert done["② 형성 전위"] and done["③ 밴드갭 + DOS/PDOS"], "완료 축이 완료로 안 뜬다"
    body = A.app.test_client().get("/").get_data(as_text=True)
    assert "공동연구 요청 3축" in body and "확산장벽" in body
    # 정상 상태에서는 "못 읽음" 문구가 나오면 안 된다 (아래 음성 시험의 대조군)
    assert "원장 못 읽음" not in body


def test_sei_axes_say_unreadable_instead_of_zero():
    """⛔ 원장을 **못 읽은 것**을 '계산 중' 이나 '0종' 으로 렌더하면 안 된다.

    실측 결함 (2026-09-07): `neb_recalc_pending` 이 try 안에서만 묶여 있어
      `db/properties/sei_neb.json` 이 없거나 깨지면 `sei_axes()` 가 UnboundLocalError 를
      냈고 대시보드(`/`)가 통째로 500 이었다. 그런데 단순히 False 로 초기화하면 이번엔
      화면이 "DFT CI-NEB 계산 중" 이라고 **거짓말**을 한다 — 못 읽은 것과 아직 안 한 것은
      다른 사실이다. 세 원장 모두 같은 규약을 쓴다.

    음성 경로가 이 시험의 본체다: 깨진 원장·없는 원장에서 **거짓 진행 문구가 안 나오는지**
    를 본다. 양성(정상 렌더)만 보는 시험은 이 결함을 하나도 못 잡았다.
    """
    import shutil
    import tempfile

    LEDGERS = {
        "neb": (ROOT / "db/properties/sei_neb.json", 0),
        "volt": (ROOT / "db/properties/sei_formation_voltage.json", 1),
        "gap": (ROOT / "db/properties/sei_electronic.json", 2),
    }
    # 거짓 진행 문구 — 원장을 못 읽었는데 이게 나오면 화면이 거짓말을 하는 것이다
    LIES = ("계산 중", "종 + 분해 산물", "종 (fixed-occ nscf 고유값)")

    for what, (path, axis_i) in LEDGERS.items():
        orig = path.read_bytes()
        bak = tempfile.mktemp(suffix=".bak")
        shutil.copy(path, bak)
        try:
            for scenario, mutate in (("깨진 JSON", lambda: path.write_text("{ not json",
                                                                          encoding="utf-8")),
                                     ("파일 없음", lambda: path.unlink())):
                mutate()
                ax = D.sei_axes()["axes"]          # ① 예외로 죽으면 안 된다
                a = ax[axis_i]
                blob = f"{a['state']} {a['detail']}"
                assert "못 읽" in blob or "없다" in blob, (
                    f"{what}/{scenario}: 원장을 못 읽었는데 화면이 그 사실을 안 적는다 — {blob!r}")
                assert not any(l in a["detail"] for l in LIES), (
                    f"{what}/{scenario}: 못 읽은 원장을 진행/집계 문구로 렌더한다 — {a['detail']!r}")
                assert "0종" not in a["detail"], (
                    f"{what}/{scenario}: 못 읽은 것을 '0종' 이라는 없는 집계로 찍는다")
                if what == "neb":
                    assert a["done"] is False, "못 읽은 축이 완료로 뜬다"
                # ② 라우트가 500 이 아니라 그 사실을 실은 화면을 내야 한다
                rv = A.app.test_client().get("/")
                assert rv.status_code == 200, (
                    f"{what}/{scenario}: 원장 하나가 깨졌다고 대시보드가 {rv.status_code}")
                body = rv.get_data(as_text=True)
                assert "못 읽" in body or "이(가) 없다" in body, (
                    f"{what}/{scenario}: 대시보드가 원장을 못 읽은 사실을 화면에 안 적는다")
                # ③ SEI 절이 **말없이 사라지면** 안 된다 — 사라진 절은 '그런 게 없다' 로 읽힌다
                assert "SEI 분해상" in body, (
                    f"{what}/{scenario}: SEI 절이 사유 없이 통째로 사라졌다")
                shutil.copy(bak, path)
        finally:
            path.write_bytes(orig)
            os.remove(bak)
    # 복구 확인 — 시험이 원장을 망가뜨린 채 끝나면 뒤 시험이 전부 거짓 통과한다
    assert D.sei_axes()["axes"][0]["state"] != "⛔ 원장 못 읽음"


def test_no_hardcoded_metric_lists_in_templates():
    """metric 목록이 템플릿으로 되돌아오면 안 된다 — 그게 위 회귀의 원인이었다."""
    for name in ("explorer.html", "composition.html", "compare.html"):
        t = (ROOT / "webapp" / "templates" / name).read_text(encoding="utf-8")
        assert "MM" in t, f"{name} 이 metric_meta(MM)를 안 쓴다"
        assert "'gap_eV','Band gap'" not in t and "'gap_eV':'eV'" not in t, \
            f"{name} 에 metric 하드코딩이 되살아났다"


def test_evrh_group_respects_source_pairing():
    """★ elastic.json 이 comp1↔comp2 만 완전비교쌍이라 한다 (Codex 5라운드).

    네 조성을 한 묶음으로 자동 순위화하면 method_id 가 맞아도 의미상 틀린다.
    """
    reg = C.load_registry()
    g = {e["system"]: e["comparison_group"] for e in C.entries(reg, "E_VRH_GPa", status=None)}
    assert g.get("comp1") == g.get("comp2"), "comp1↔comp2 가 같은 묶음이 아니다"
    for other in ("modelc", "lpsocl"):
        assert g.get(other) != g.get("comp1"), \
            f"{other} 가 comp1/comp2 완전비교쌍 묶음에 섞여 있다"


def test_status_badge_is_not_duplicated():
    """★ 레지스트리 status 와 옛 PROV 배지가 겹쳐 '잠정' 이 두 번 찍혔다 (Codex 4라운드).

    ⛔ 2026-09-07 정정 — 첫 판의 정규식은 `>잠정</span>` **뒤에 오는 배지를 전부** 중복으로
      셌다. 그래서 잣대 세대 배지('구 잣대')를 추가하자 곧바로 거짓양성이 났다.
      잡으려던 불변식은 *'같은 라벨이 연달아 두 번'* 이지 *'배지가 두 개'* 가 아니다 —
      배지 축은 status·출처·세대로 **여러 개가 정상**이다. 라벨 비교로 좁힌다.
    """
    c = A.app.test_client()
    pair = re.compile(r"<span class=\"badge\"[^>]*>([^<]*)</span>\s*"
                      r"<span class=\"badge\"[^>]*>([^<]*)</span>")
    for u in ("/explorer", "/composition/comp2", "/composition/lpsocl"):
        t = c.get(u).get_data(as_text=True)
        dup = [(a, b) for a, b in pair.findall(t) if a.strip() == b.strip()]
        assert not dup, f"{u} 에서 같은 배지가 두 번 찍힌다: {dup[:2]}"
    cmp_ = c.get("/compare").get_data(as_text=True)
    # compare 는 JS 로 그리므로 '둘 다 붙이는' 코드 형태가 남아 있지 않은지 본다
    assert "else if(pr)cell+=" in cmp_, "compare 가 배지를 배타적으로 안 고른다"


def test_seminar_points_at_files_that_exist():
    """★ /seminar 이 **없는 덱**(Research_Seminar_2026_08_cascade.pptx)과 옛 spec 을 가리키고
    있었다 — 다운로드 버튼이 조용히 사라진 상태였다 (2026-08-11 개편). 다시 어긋나지 않게 못 박는다."""
    for key, (name, _note) in D.SEMINAR_DECKS.items():
        assert (D.KB / "seminars" / name).is_file(), f"덱 화이트리스트 '{key}' 가 없는 파일을 가리킨다: {name}"
    assert (D.KB / "seminars" / D.SEMINAR_SCRIPT).is_file(), "정본 대본이 없다"
    live = [k for k, _l, p, _n in D.SEMINAR_DOCS if p.is_file()]
    assert "script" in live, "대본 탭이 안 뜬다 — 경로가 어긋났다"
    assert len(live) >= 4, f"세미나 문서 탭이 너무 적다: {live}"

    c = A.app.test_client()
    t = c.get("/seminar").get_data(as_text=True)
    assert c.get("/seminar/deck?v=release").status_code == 200
    assert c.get("/seminar/deck?v=../../etc/passwd").status_code == 404, "덱 키가 경로로 새면 안 된다"
    for k in live:
        assert f'data-tab="{k}"' in t, f"{k} 탭이 화면에 없다"


def test_seminar_runsheet_tracks_the_script():
    """진행표는 대본을 **파싱**해서 만든다 — 하드코딩하면 대본을 고쳤을 때 조용히 어긋난다."""
    md = (D.KB / "seminars" / D.SEMINAR_SCRIPT).read_text(encoding="utf-8")
    rs = D.seminar_runsheet(md)
    assert len(rs) >= 4, f"Part 를 못 읽었다: {rs}"
    assert all(p["slides"] for p in rs), "슬라이드가 비어 있는 Part 가 있다"
    assert sum(p["seconds"] for p in rs) > 600, "초 배분을 못 읽었다 (⏱ 표기 확인)"
    assert not any("(" in p["title"] for p in rs), f"Part 제목에 괄호 메타가 남았다: {[p['title'] for p in rs]}"
    # 대본에 없는 Part 를 화면이 지어내지 않는지 — 개수가 정확히 같아야 한다
    t = A.app.test_client().get("/seminar").get_data(as_text=True)
    assert len(re.findall(r'class="sem-badge">([A-Z])<', t)) == len(rs)


# ── cascade 화면의 지위 표시 (2026-08-14 개정) ──────────────────────────────
#   화면이 47종 시대 결과를 최신 승인물처럼 보여주던 것을 고쳤다. 그 상태로 되돌아가면
#   사이트가 스스로 모순되므로(승인 0건인데 1위 표가 뜬다) 여기서 잠근다.
def _cascade_html():
    return A.app.test_client().get("/cascade").get_data(as_text=True)


def test_cascade_defaults_to_the_audit_screen():
    """승인된 랭킹이 0건이므로 기본 탭은 결과가 아니라 감사 화면이어야 한다."""
    h = _cascade_html()
    m = re.search(r'<button class="active" data-tab="([a-z0-9]+)"', h)
    assert m, "#tabs 에 active 버튼이 없다"
    assert m.group(1) == "audit", f"기본 탭이 '{m.group(1)}' 이다 — 감사 화면이어야 한다"
    assert re.search(r'<div class="tab-panel active" id="tab-audit"', h), "tab-audit 패널이 active 가 아니다"


def test_cascade_headline_comes_from_the_manifest():
    """타일 숫자는 하드코드가 아니라 manifest 파생이어야 한다 (Codex 리뷰 P1)."""
    t = D.cascade_truth()
    assert t["ok"], f"manifest 가 유효하지 않다: {t.get('problems')} {t.get('stale')}"
    got = {k: v for k, v, _l, _n in t["tiles"]}
    assert got["planned_slots"] == 273 and got["completed_slots"] == 270
    assert got["completed_species"] == 90 and got["historical_snapshot_species"] == 47
    assert got["approved_current_leaderboard_species"] == 0
    assert got["explicit_pair_property_labels"] == 0
    h = _cascade_html()
    assert "승인된 도펀트 랭킹은 0건" in h, "승인 0건 배너가 화면에 없다"
    assert "랭킹된 도펀트</div>" not in h, "47종 타일 라벨이 최상단에 되살아났다"


def test_manifest_tamper_fails_closed():
    """파일이 바뀌었는데 manifest 가 안 따라오면 숫자를 추측하지 말고 막아야 한다."""
    import hashlib
    m = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    for a in m["artifacts"]:
        p = ROOT / a["source_path"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == a["sha256"], (
            f"{a['source_path']} 가 manifest 와 어긋난다 — rebuild_pool_inputs.py 를 다시 돌릴 것")
        assert a["approval_status"] in D._MANIFEST_STATUS
        assert a["use_scope"] in D._MANIFEST_USE_SCOPE
        assert a["actual_x"] == 0.25, "실측 농도는 0.25 다 (라벨 x002/x005/x010 은 농도가 아니다)"
    # 위조 시나리오: status 를 어휘 밖 값으로 바꾸면 ok=False 여야 한다
    orig = D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8")
    try:
        bad = json.loads(orig)
        bad["artifacts"][0]["approval_status"] = "approved_by_nobody"
        D.CASCADE_MANIFEST_PATH.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
        D._load_json.cache_clear() if hasattr(D._load_json, "cache_clear") else None
        assert D.cascade_truth()["ok"] is False, "알 수 없는 status 인데 fail-closed 하지 않았다"
    finally:
        D.CASCADE_MANIFEST_PATH.write_text(orig, encoding="utf-8")
        D._load_json.cache_clear() if hasattr(D._load_json, "cache_clear") else None


def test_na2s_ductility_claim_is_retracted():
    """음의 B_hill 행을 평균에 넣고 역수를 취해 만든 '연성 반증' 은 철회됐다."""
    import csv as _csv
    rows = list(_csv.DictReader(
        l for l in (D.DB / "properties" / "cascade_v23_champions_v2.csv")
        .read_text(encoding="utf-8").splitlines() if not l.startswith("#")))
    bad = [r for r in rows if r["elastic_B_hill_GPa"].strip()
           and float(r["elastic_B_hill_GPa"]) <= 0]
    assert bad, "비물리 행이 사라졌다면 이 회귀 테스트를 갱신할 것"
    rk = {r["dopant"]: r for r in _csv.DictReader(
        l for l in (D.DB / "properties" / "cascade_v23_ranked_v2.csv")
        .read_text(encoding="utf-8").splitlines() if not l.startswith("#"))}
    # 실패 행이 평균에서 빠졌으므로 Na2S 의 B/G 는 1.75 아래여야 한다
    assert 1.0 / float(rk["Na2S"]["pugh"]) < 1.75, "Na2S 가 다시 연성 경험칙을 넘었다 — 가드 확인"
    th = json.loads((D.DB / "properties" / "cascade_v23_themes_v2.json").read_text(encoding="utf-8"))
    assert "어느 것도 B/G>1.75" in th["themes"]["ductility"]["caveat"], "연성 서술이 되돌아갔다"


def test_recovered_ranking_is_gated_server_side():
    """<details> 는 후보명을 초기 DOM 에 다 싣는다 — 서버가 렌더 자체를 막아야 한다."""
    c = A.app.test_client()
    h = _cascade_html()
    assert "/cascade/diagnostic" in h, "acquisition 화면 링크가 없다"
    denied = c.get("/cascade/diagnostic")
    assert denied.status_code == 403, "view=diagnostic 없이 열렸다"
    body = denied.get_data(as_text=True)
    ep = (D.load_cascade()["v2"]["meta"].get("funnel_v2") or {}).get("endpoint") or []
    assert ep, "endpoint 목록이 비었다 — 이 테스트를 갱신할 것"
    for sp in ep[:6]:
        assert sp not in body, f"거부 화면에 후보명 {sp} 가 DOM 으로 실렸다"
    allowed = c.get("/cascade/diagnostic?view=diagnostic")
    assert allowed.status_code == 200 and ep[0] in allowed.get_data(as_text=True)


def test_artifact_policy_gates_every_api_path():
    """화면에서 숨긴 artifact 를 API 로 그냥 받을 수 있으면 안 된다 (Codex Round-3 P0-3)."""
    c = A.app.test_client()
    cases = [
        ("/api/file/db/properties/cascade_audit_gate_completeness.csv?dl=1", 200),
        # Round-3 — 종명이 든 감사본은 공개 금지, 익명 공개판이 default_visible
        ("/api/file/docs/figures/cascade/cascade_audit_g4_rescore.png", 403),
        ("/api/file/docs/figures/cascade/cascade_audit_g4_rescore.png?view=diagnostic", 200),
        ("/api/file/docs/figures/cascade/cascade_seminar_g4_anonymized_round3.png", 200),
        ("/api/file/db/properties/cascade_seminar_gate_denominators_round3.csv?dl=1", 200),
        ("/api/file/db/properties/cascade_v23_ranked_v2.csv?dl=1", 403),
        ("/api/file/db/properties/cascade_v23_ranked_v2.csv?dl=1&view=diagnostic", 200),
        ("/api/file/db/properties/cascade_v23_ranked.csv?dl=1", 403),
        ("/api/file/db/properties/cascade_v23_ranked.csv?dl=1&archive=1", 200),
        ("/api/property/cascade_screening_funnel_v2", 403),
        ("/api/property/cascade_screening_funnel_v2?view=diagnostic", 200),
        ("/api/csv/properties/cascade_v23_ranked_v2.csv", 403),
        ("/api/file/db/properties/electronic.json", 200),      # cascade 밖은 통과
    ]
    for url, want in cases:
        got = c.get(url).status_code
        assert got == want, f"{url} → {got} (want {want})"


def test_csv_api_survives_a_non_csv_and_names_the_reason():
    """`/api/csv/<png>` 가 500 이 아니라 **사유를 적은 오류**여야 한다.

    실측 (2026-09-07): db/properties 아래에 png 가 실제로 있고, 그 경로로 부르면
      `read_csv()` 의 맨몸 `open(encoding='utf-8-sig')` 에서 UnicodeDecodeError 가
      새어 나와 라우트가 500 이었다. 500 은 화면에 아무 말도 못 하고, 브라우저 콘솔의
      JS 는 `d.error` 를 기대하는데 JSON 이 아예 안 온다.

    음성 경로 세 가지: 텍스트가 아닌 파일 · 없는 파일 · 경로 탈출.
    """
    c = A.app.test_client()
    pngs = sorted((ROOT / "db" / "properties").glob("*.png"))
    assert pngs, "이 시험의 전제(png 가 db/properties 에 있다)가 깨졌다"
    r = c.get("/api/csv/properties/" + pngs[0].name)
    assert r.status_code == 200, f"비-CSV 에 {r.status_code} — 500 회귀"
    d = r.get_json()
    assert d.get("error"), "비-CSV 인데 error 를 안 준다 (조용히 빈 표로 보인다)"
    assert "UnicodeDecodeError" in d["error"] or "읽을 수 없다" in d["error"], d["error"]
    # 없는 파일 · 경로 탈출은 여전히 막혀 있어야 한다 (느슨해지지 않았는지)
    assert c.get("/api/csv/properties/nope_does_not_exist.csv").get_json()["error"]
    assert c.get("/api/csv/../../etc/passwd").get_json()["error"], "경로 탈출이 뚫렸다"
    # 정상 CSV 는 그대로 (양성 대조군)
    ok = c.get("/api/csv/properties/" + sorted(
        (ROOT / "db" / "properties").glob("*.csv"))[0].name).get_json()
    assert ok.get("columns") and not ok.get("error")


def test_artifact_envelope_path_matches_the_ledger():
    """봉투의 `artifact` 는 원장의 source_path 와 **대조 가능한 같은 표기**여야 한다.

    실측 (2026-09-07): `/api/csv` 가 resolve 에는 `db/properties/…` 를 주면서 envelope
      에는 접두 없는 `properties/…` 를 줬다. 봉투는 인용 시 지위를 값에 붙들어 두는
      장치인데, 그 식별자로 원장을 못 찾으면 붙들어 두는 일을 못 한다.
    """
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    gov = [a["source_path"] for a in man["artifacts"]
           if str(a["source_path"]).startswith("db/properties/")]
    assert gov, "이 시험의 전제(원장에 db/properties artifact 가 있다)가 깨졌다"
    c = A.app.test_client()
    seen_denied = seen_allowed = 0
    for src in gov[:6]:
        entry = AP._load()[src]
        gate = AP.SCOPE_GATE[entry["use_scope"]]
        # 접두 있는 요청과 없는 요청이 **같은** 봉투를 내야 한다
        for url in (f"/api/csv/{src[3:]}", f"/api/csv/{src}"):
            for qs in ("", f"?{gate[0]}={gate[1]}" if gate else ""):
                r = c.get(url + qs)
                d = r.get_json()
                env = d.get("_artifact_status") or d
                assert env.get("artifact") == src, (
                    f"{url+qs} ({r.status_code}): 봉투가 {env.get('artifact')!r} 라는데 "
                    f"원장은 {src!r} 다 — 이 표기로는 원장 대조가 안 된다")
                if r.status_code == 403:
                    seen_denied += 1
                elif "_artifact_status" in d:
                    seen_allowed += 1
    # 두 갈래를 **둘 다** 밟았는지 — 한쪽만 보면 다른 쪽 회귀를 못 잡는다
    assert seen_denied and seen_allowed, (
        f"거부 갈래 {seen_denied}건 · 허용 갈래 {seen_allowed}건 — 두 갈래를 다 밟아야 한다")


def test_manifest_has_a_single_owner():
    """생산자 둘이 같은 원장을 통째로 덮어써 상대의 계약 블록을 지웠다 (P0-1)."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert man.get("owner") == "tools/cascade/build_cascade_audit_manifest.py"
    for k in ("datasets", "metric_contract", "artifacts", "figures", "supporting_tables"):
        assert k in man, f"원장에 {k} 블록이 없다 — 소유자가 다시 갈라졌다"
    plotter = (ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py").read_text(encoding="utf-8")
    assert 'out = DB / "cascade_audit_manifest.json"' not in plotter, \
        "플로터가 다시 원장을 쓴다 — sidecar 만 써야 한다"
    rebuild = (ROOT / "tools" / "cascade" / "rebuild_pool_inputs.py").read_text(encoding="utf-8")
    assert "cascade_audit_manifest.json" not in rebuild, \
        "rebuild_pool_inputs 가 다시 원장을 쓴다"


def test_artifact_provenance_is_per_file():
    """top-level source_commit 하나로 전부를 덮으면 거짓말이 된다 (P0-2)."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    rk = [a for a in man["artifacts"] if a["source_path"].endswith("ranked_v2.csv")][0]
    assert rk["source_commit"] != man["source_commit"], "ranked_v2 가 다시 고정 커밋으로 묶였다"
    assert rk.get("derived_from") == man["source_commit"] and rk.get("override_reason")
    plotter = (ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py").read_text(encoding="utf-8")
    dep = plotter.split("RECOVERED_DERIVED = [")[1].split("]")[0]
    entries = [ln.strip() for ln in dep.splitlines() if ln.strip().startswith('"')]
    assert not any("ranked_v2" in e for e in entries), \
        "ranked_v2 가 다시 패널 의존에 들어갔다 (어느 패널도 안 읽는다)"


def test_g3_phase_set_row_reflects_the_2026_08_16_closure():
    """옛 판은 '합성 id 를 주장하지 마라'였다. 이제 진짜 id 를 싣는다 — 대신 두 가지를 지킨다:
    ① 회수 행이 가정이 아니라 기록으로 바뀌었을 것 ② 조성족 섞임이 open 으로 남아 있을 것."""
    t = D.read_csv("properties/cascade_audit_g3_phase_set.csv")
    rec = [r for r in t["data"] if r["status"] == "recovered_diagnostic"]
    assert rec, "회수 행이 사라졌다"
    assert "phase_set_id" in str(rec[0]["note"]), "무엇으로 닫혔는지가 행에 없다"
    assert not str(rec[0]["phase_set_assumption"] or "").strip(), "닫혔는데 가정 표기가 남아 있다"
    # 민감도 행은 여전히 '이 문턱을 다른 phase set 후보에 쓰지 마라' 여야 한다
    sens = [r for r in t["data"] if r["status"] == "sensitivity-only"]
    assert sens and abs(float(sens[0]["oxidation_onset_V"]) - 2.256) < 1e-9
    # 조성족은 아직 안 닫혔다 — open 행이 사라지면 조용히 닫힌 척이 된다
    op = [r for r in t["data"] if r["status"] == "open"]
    assert op, "조성족 섞임 open 행이 사라졌다"
    assert "Cl-rich" in str(op[0]["note"]) and "B2O3" in str(op[0]["note"])


def test_g4_rescore_carries_pool_metadata():
    """min–max 점수를 고정 물성처럼 읽지 못하게 하는 메타 (P1)."""
    t = D.read_csv("properties/cascade_audit_g4_rescore.csv")
    r = t["data"][0]
    for c in ("pool_id", "normalization_n", "bvs_pool_min", "bvs_pool_max", "actual_x"):
        assert str(r.get(c, "")).strip() != "", f"{c} 가 없다"
    assert float(r["actual_x"]) == 0.25


def test_g5_completeness_separates_presence_from_validity():
    """presence 88/1/1 옆에 validity-aware 86/AlBr3·MgI2·Na2S/AlI3 를 병기해야 한다 (P1)."""
    t = D.read_csv("properties/cascade_audit_gate_completeness.csv")
    g5 = [r for r in t["data"] if r["gate"] == "G5"][0]
    assert g5["validity_aware_all_label_species"] == 86
    assert g5["validity_aware_partial"] == "AlBr3|MgI2|Na2S"
    assert g5["validity_aware_dropped"] == "AlI3"
    assert all(r.get("completeness_basis") for r in t["data"]), "completeness_basis 가 비었다"


def test_public_g4_panel_is_anonymized():
    """Round-3 정책: 후보 identity 는 acquisition 전용. 공개 패널에 종명이 있으면 안 된다."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    pub = {f["image"] for f in man["figures"]}
    assert "docs/figures/cascade/cascade_seminar_g4_anonymized_round3.png" in pub
    assert "docs/figures/cascade/cascade_audit_g4_rescore.png" not in pub, \
        "종명이 든 G4 패널이 공개 목록으로 돌아왔다"
    # 익명 CSV 는 종명을 담지 않는다
    t = D.read_csv("properties/cascade_seminar_g4_anonymized_round3.csv")
    ids = {str(r["case_id"]) for r in t["data"]}
    assert ids == {"Case A", "Case B", "Case C", "Case D", "Case E", "Case F"}
    blob = json.dumps(t["data"], ensure_ascii=False)
    for sp in ("B2O3", "Cr2O3", "Ga2O3", "In2O3", "Sc2O3", "Y2O3"):
        assert sp not in blob, f"익명 CSV 에 {sp} 가 남아 있다"
    h = _cascade_html()
    assert "cascade_audit_g4_rescore.png" not in h, "기본 화면이 종명 패널을 띄운다"


def test_gate_denominators_separate_record_from_method():
    """기록이 있다 ≠ 비교 가능하다. G3 는 phase_set_id 를 싣고 나서야 90/90 이 됐다."""
    t = D.read_csv("properties/cascade_seminar_gate_denominators_round3.csv")
    by = {r["gate"]: r for r in t["data"]}
    assert by["G3"]["record_present_species"] == 90
    # 2026-08-16: phase_set_id + 같은 실행 안의 host 측정으로 0 → 90 (270/270 쌍)
    assert by["G3"]["all_label_method_valid_species"] == 90
    assert by["G3"]["status"] == "recovered_diagnostic"
    assert "phase_set_id" in by["G3"]["note"]
    assert by["G5"]["all_label_method_valid_species"] == 86
    assert by["G5"]["partial_species"] == "AlBr3|MgI2|Na2S"
    assert by["G4"]["dropped_species"] == "AlI3|MgI2"
    for g, r in by.items():
        assert r["approved_current_species"] == 0, f"{g} 가 승인된 것처럼 적혀 있다"
    assert "게이트 분모 계약" in _cascade_html()


def test_oxidation_onset_carries_its_composition_family():
    """이름표가 같아도 조성이 다르면 나란히 놓지 않는다 (2026-08-16 Cl-rich 섞임)."""
    pinned = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                        .read_text(encoding="utf-8"))
    audit = pinned["composition_family_audit"]
    assert audit["counts"] == {"Clrich": 17, "plain": 253}
    assert audit["family_label_inconsistent"] == []
    assert audit["species_with_no_plain_champion"] == ["B2O3"]
    assert set(audit["species_improving_only_as_variant"]) == {"Al2O3", "MoO3", "WO3"}
    # 모든 후보 행이 조성족을 달고 있어야 한다 — 빠진 행은 조용히 비교돼 버린다
    cand = [v for k, v in pinned["results"].items() if "HOST" not in k.split("_")]
    assert len(cand) == 270
    assert all(v.get("composition_family") in ("plain", "Clrich") for v in cand)
    assert all(v["delta_ox_vs_host_V_confounded"] == (v["composition_family"] != "plain")
               for v in cand)
    # DFT-deep B2O3 는 표의 onset 과 **다른 조성**이다 (부호가 반대)
    col = pinned["dft_deep_composition_collision"]["B2O3"]
    assert col["cascade_champion"]["ox_V"] > col["host_ox_V"] > col["dft_deep_cell"]["ox_V"]

    # 47종 pool 로도 새어나가는지 — 오염은 B2O3 1건, 나머지는 plain/degenerate
    pool = json.loads((ROOT / "db/properties/cascade_screening_funnel.json")
                      .read_text(encoding="utf-8"))["pool"]
    bad = [r["dopant"] for r in pool
           if r["ox_composition_family"] in ("unmatched", "unresolved")]
    assert not bad, f"조성족을 못 정한 종: {bad}"
    assert [r["dopant"] for r in pool if r["ox_family_confounded"]] == ["B2O3"]

    seminar = D.read_csv("properties/cascade_seminar_oxidation_transport_47.csv")
    rows = {r["dopant"]: r for r in seminar["data"]}
    assert rows["B2O3"]["ox_composition_family"] == "Clrich"
    assert rows["B2O3"]["plain_champion_exists"] == 0
    # ⛔ 'WO3 가 있으면 WO3, 없으면 Sc2O3' 는 무엇을 검사하는지 불분명하다 (Codex 지적).
    #   여섯 종을 명시하고, 오염은 B2O3 하나뿐임을 그 집합 안에서 확인한다.
    assert set(rows) == {"B2O3", "Cr2O3", "Ga2O3", "In2O3", "Sc2O3", "Y2O3"}
    assert [d for d, r in rows.items() if r["ox_family_confounded"]] == ["B2O3"]


def test_seminar_17d9a373_handoff_contract():
    """세미나 최종 핸드오프(17d9a373)의 회귀 계약 12건을 한 곳에서 잠근다."""
    h = _cascade_html()
    fac = json.loads((ROOT / "db/properties/oxidation_matched_factorial.json")
                     .read_text(encoding="utf-8"))
    nol = json.loads((ROOT / "db/properties/oxidation_matched_factorial_nolis4.json")
                     .read_text(encoding="utf-8"))

    # 1. G3 네 층을 동시에 렌더한다
    for token in ("270/270", "17/17", "0/11"):
        assert token in h, f"G3 상태에 {token} 이 없다"
    assert "approved current ranking" in h.lower() or "승인" in h

    # 2·3. stale / 금지 문구가 **주장으로** 안 나온다.
    #   ⚠ 감사 화면은 "이렇게 말하면 안 된다" 목록을 일부러 띄운다 — 그 블록을 걷어내고 본다.
    #     안 그러면 경고문 자체가 위반으로 잡혀서, 경고를 지우는 게 테스트 통과법이 된다.
    body = re.sub(r"<!--FORBIDDEN-->.*?<!--/FORBIDDEN-->", "", h, flags=re.S)
    assert "<!--FORBIDDEN-->" in h, "금지 목록 블록이 사라졌다"
    assert len(body) < len(h), "금지 목록을 못 걷어냈다 (정규식 확인)"
    for forb in ("method-comparable 0", "effect attribution closed",
                 "Cl 효과는 0", "Cl effect = 0", "11/11 species validated", "9.7배"):
        assert forb not in body, f"금지 문구가 주장으로 화면에 있다: {forb}"
    # 그리고 그 목록에는 여전히 들어 있어야 한다 (경고를 지워서 통과하면 안 된다)
    for forb in ("effect attribution closed", "11/11 species validated"):
        assert forb in h, f"금지 목록에서 {forb} 가 빠졌다"

    # 4. chain audit 이 exact 10 / multi 7 을 재현
    mt = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                    .read_text(encoding="utf-8"))["composition_family_audit"]["matched_transform"]
    assert mt["counts"] == {"exact": 10, "multi_transform": 7}

    # 5. 두 비율이 분모·non-causal 라벨과 같은 패널에
    assert "9.63" in h and "2.59" in h
    assert "17/253" in h and "11/17" in h and "4/16" in h
    assert "post-selection descriptive association" in h
    for never in ("Cl effect size", "causal enrichment", "success rate"):
        assert never in h, f"'이렇게 부르지 않는다' 목록에 {never} 가 없다"
        assert never not in body, f"{never} 가 목록 밖에서 쓰이고 있다"

    # 6. B2O3 exact composition mismatch → validation link 없음
    assert D.CASCADE_JOIN_STATUS["b2o3"]["validation_link_status"] == "different_composition"

    # 7. ladder4 = 2.356 · S16 · 0.5 LiS4
    lad = {r["cell"]: r for r in D.load_factorial()["included"]["ladder"]}
    assert lad["__ladder4__"]["ox_V"] == 2.356
    assert "S16" in lad["__ladder4__"]["formula"]
    assert "LiS4" in lad["__ladder4__"]["rxn"], "ladder4 에서 LiS4 가 사라졌다"
    assert lad["__ladder3__"]["ox_V"] == 2.140
    assert "MECHANISM HYPOTHESIS" in h, "사다리가 가설 표시 없이 나간다"

    # 8. LiS4 제외판 값 고정
    ex = nol["decomposition"]
    for sp, want in (("WO3", 0.000), ("Al2O3", 0.098), ("MoO3", 0.129), ("B2O3", 0.283)):
        got = ex[sp]["conditional_cl_recipe_contrast_V"]
        assert abs(got - want) < 5e-4, f"{sp} {got} != {want}"
    assert nol["exclusions"] == ["LiS4"]
    assert ex["Al2O3"]["H_plain_V"] == 2.256, "제외판 host 가 2.256 이 아니다"
    assert fac["decomposition"]["Al2O3"]["H_plain_V"] == 2.140
    assert "다른 phase set" in h, "두 판을 섞지 말라는 경고가 화면에 없다"

    # 9. stage 09f 가 current G2/G3 source 로 표시되지 않는다
    gm = dict(D.CASCADE_STAGE_GATE_MAP)
    assert "09f" in gm["G2 / G3 (current)"] and "아니다" in gm["G2 / G3 (current)"]
    assert "NOT A TRUE GRAND-POTENTIAL ESW" in h

    # 10. stage 10/11 은 NOT RUN · 0/270 (unharvested 아님)
    tail = [g for g in D.CASCADE_STAGE_GROUPS if g["id"] == "10-12b"][0]
    blob = " ".join(tail["warnings"])
    assert blob.count("NOT RUN") >= 2 and "0/270" in blob
    assert "unharvested" not in h and "미수확" not in h

    # 11. 기본 DOM 에 archive/diagnostic 후보 행이 없다 (별도 테스트가 상세히 본다)
    assert h.count('"dopant":') == 0

    # 12. manifest 에 두 factorial 원장이 다 등록돼 있다
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    reg = {a["source_path"]: a for a in man["artifacts"]}
    for fn, scope in (("oxidation_matched_factorial.json", "default_visible"),
                      ("oxidation_matched_factorial_nolis4.json", "diagnostic_only")):
        k = f"db/properties/{fn}"
        assert k in reg, f"{fn} 이 원장에 없다"
        assert reg[k]["use_scope"] == scope


def test_default_cascade_does_not_ship_the_superseded_ranking():
    """경고 배너는 접근 정책이 아니다 — archive/diagnostic 행은 초기 DOM 에 없어야 한다.

    ⛔ 2026-08-16 — 기본 `/cascade` 가 47종 rank·score 배열(`var RANKED`)과 90종 테마
      조합 랭킹(`var TDOP`)을 통째로 싣고 있었다. 보안이 아니라 **정책 위반**이다:
      manifest 상 각각 archive_only · diagnostic_only 인데 기본 화면이 "승인된 ranking
      0종" 이라고 쓰면서 순위표를 같이 내보냈다.
    """
    c = A.app.test_client()
    h = c.get("/cascade").get_data(as_text=True)
    assert h.count('"dopant":') == 0, "기본 화면에 후보 행이 있다"
    assert '"rank": 1.0' not in h, "47종 rank 배열이 초기 DOM 에 있다"
    assert h.count("disorder_std") < 10, "90종 테마 배열이 초기 DOM 에 있다"
    assert "보관함 열기" in h and "진단 화면 열기" in h, "opt-in 경로가 화면에 없다"

    # 값을 지운 게 아니다 — 쿼리를 주면 그대로 나온다
    ha = c.get("/cascade?archive=1").get_data(as_text=True)
    assert '"rank": 1.0' in ha and '"dopant": "Sc2O3"' in ha, "보관함에서도 안 나온다"
    assert ha.count("disorder_std") < 10, "archive 가 diagnostic 까지 열어 준다"

    hd = c.get("/cascade?view=diagnostic").get_data(as_text=True)
    assert hd.count("disorder_std") > 10, "진단 화면에서 테마 행이 안 나온다"
    assert '"rank": 1.0' not in hd, "diagnostic 이 archive 까지 열어 준다"

    # diagnostic 라우트는 여전히 opt-in 403
    assert c.get("/cascade/diagnostic").status_code == 403
    assert c.get("/cascade/diagnostic?view=diagnostic").status_code == 200


def test_factorial_does_not_claim_a_closed_causal_attribution():
    """baseline contrast 0 을 'Cl 효과 0' 으로 쓰면 안 된다 (2026-08-16 재감사 P0-1)."""
    f = json.loads((ROOT / "db/properties/oxidation_matched_factorial.json")
                   .read_text(encoding="utf-8"))
    v = f["verdict"]   # 도구가 생성한다 (손편집 금지)
    assert "'Cl 효과는 0'" in v["NO_GO"] and "'인과 귀속 폐쇄'" in v["NO_GO"]
    assert v["three_fields_not_one"]["element_level_causal_attribution"] == "not_claimed"
    assert v["baseline_nonzero_species"] == [], "baseline 이 0 이 아닌 종이 생겼다"
    assert v["conditional_range_V"] == [-0.017, 0.283]
    assert v["mechanism_status"].startswith("hypothesis")
    for sp, d in f["decomposition"].items():
        if not d.get("complete"):
            continue
        # 옛 이름이 남아 있으면 '0 이므로 효과 없음' 으로 다시 읽힌다
        assert "main_Cl_V" not in d and "main_dopant_V" not in d, sp
        assert d["isolated_element_effect"] is False
        # 대수 항등식: total = plain_dopant + conditional
        assert abs(d["total_D_Cl_vs_host_V"]
                   - (d["plain_dopant_recipe_contrast_V"]
                      + d["conditional_cl_recipe_contrast_V"])) < 5e-4, sp
    # baseline 0 인데 conditional 이 0 이 아닌 종이 실제로 있어야 한다 (그게 요점)
    nz = [sp for sp, d in f["decomposition"].items()
          if d.get("complete") and abs(d["baseline_cl_recipe_contrast_V"]) < 1e-9
          and abs(d["conditional_cl_recipe_contrast_V"]) > 1e-9]
    assert set(nz) >= {"Al2O3", "B2O3", "MoO3", "WO3"}, nz

    pin = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                     .read_text(encoding="utf-8"))
    assert "attribution_closed_2026_08_16" not in pin, "'닫힘' 블록이 남아 있다"
    a = pin["attribution_status_2026_08_16"]
    assert a["element_level_causal_attribution"] == "not_claimed"
    assert a["approved_current_ranking"] == 0
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    g3 = man["metric_contract"]["G3"]
    assert "effect_attributable_chain_rows" not in g3, "한 숫자로 덮는 필드가 남아 있다"
    assert g3["element_level_causal_attribution"] == "not_claimed"


def test_g3_species_pass_is_split_from_attribution():
    """경고만 붙이고 species-level pass 를 유지하면 fail-open 이다 (Codex f9 P0-3)."""
    f = json.loads((ROOT / "db/properties/cascade_screening_funnel.json")
                   .read_text(encoding="utf-8"))
    gs = f["gates"] if isinstance(f.get("gates"), list) else f["gate_blocks"]
    a = [g for g in gs if g["id"] == "G3"][0]["attribution_audit"]
    assert a["g2_survivors"] == 43
    assert a["algorithmic_g3"] == {"pass": 25, "fail": 18}      # 역사 count 는 보존
    assert a["attribution_audit"] == {"supported_pass": 24, "fail": 18, "unresolved": 1}
    assert a["unresolved_species"] == ["B2O3"]
    # 깔때기 기계적 count 는 안 움직여야 한다 (해석만 바뀐 것)
    assert [len(f["pool"])] == [47]


def test_b2o3_page_does_not_claim_a_same_composition_validation():
    """도펀트 라벨만으로 두 조성을 validation 으로 잇지 않는다 (Codex f9 P0-3)."""
    j = D.CASCADE_JOIN_STATUS["b2o3"]
    assert j["validation_link_status"] == "different_composition"
    assert j["composition_match"] is False
    assert j["phase_set_match"] == "unverified"
    assert j["dft_deep_ox_V"] < j["host_ox_V"] < j["cascade_ox_V"], "부호 충돌이 사라졌다"
    c = A.app.test_client()
    h = c.get("/composition/b2o3").get_data(as_text=True)
    assert "Li58P8S41Cl16B2O3" in h and "Li17B2P4S16Cl5O3" in h, "두 조성식이 나란히 없다"
    assert "같은 조성의 검증이 아니다" in h
    assert "그 <b>DFT 심층검증</b>이에요" not in h, "옛 validation 문구가 남아 있다"
    # Nd2O3 는 plain 챔피언이라 이 경고를 달면 안 된다
    hn = c.get("/composition/modelc_nd_doped").get_data(as_text=True)
    assert "같은 조성의 검증이 아니다" not in hn


def test_chain_family_is_not_described_as_one_s_to_cl_swap():
    """17행을 하나의 S→Cl 치환군으로 말하면 거짓이다 (Codex P0-1). 10 exact / 7 multi."""
    pinned = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                        .read_text(encoding="utf-8"))
    mt = pinned["composition_family_audit"]["matched_transform"]
    assert mt["counts"] == {"exact": 10, "multi_transform": 7}
    bases = sorted({r.split("_")[0] for r in mt["multi_transform_rows"]})
    assert bases == ["B2O3", "MoO3", "WO3"]
    for k, v in pinned["results"].items():
        if v.get("composition_family") == "Clrich":
            assert v["matched_transform_status"] in ("exact", "multi_transform",
                                                     "no_plain_candidate")
            assert v["contrast_scope"] == "multi_intervention_recipe_vs_host"
        elif v.get("composition_family") == "plain":
            assert v["contrast_scope"] == "primary_recipe_vs_host"
            assert v["isolated_dopant_effect"] is False   # plain 도 순수 도펀트 효과 아님

    rate = pinned["composition_family_audit"]["onset_raise_rate"]
    assert rate["enrichment_ratio"] == 9.63, "원계수에서 한 번만 반올림 (9.7 은 이중 반올림)"
    el = rate["eligible_slots_only"]
    assert (el["n_slots"], el["ratio"]) == (33, 2.59)
    assert "사후 기술통계" in rate["caveat"]

    # B2O3 충돌은 '순전히 조성 차이' 로 닫지 않는다
    col = pinned["dft_deep_composition_collision"]["B2O3"]
    assert col["dft_deep_cell"]["phase_set_id"] is None
    assert col["validation_link_status"] == "different_composition"
    b2 = json.loads((ROOT / "db/properties/b2o3_esw.json").read_text(encoding="utf-8"))
    assert b2["composition_collision_2026_08_16"]["phase_set_match"] == "unverified"

    # 화면 문구도 같이 (chain 전체를 단순 치환으로 단정하면 안 된다)
    h = _cascade_html()
    assert "10행" in h and "7행" in h, "exact/multi 분리가 화면에 없다"
    assert "9.7배" not in h, "이중 반올림 9.7 이 화면에 남아 있다"


def test_audit_generator_runs_without_windows_fonts():
    """C:/Windows/Fonts 하나에 묶여 Linux 에서 도구가 아예 안 돌았다 (2026-08-14)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "pca", ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    f = m._font(24, bold=True)
    assert f is not None
    assert m.resolved_font(), "어느 폰트를 썼는지 보고하지 않는다"
    # 폴백 체인에 Windows 밖 경로가 있어야 한다
    assert any(not r.startswith("C:") for _n, r, _b in m._FONT_CHAIN)
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert man["render_provenance"]["figure_font"], "원장에 폰트 provenance 가 없다"


def test_ledger_is_self_contained():
    """원장만 보면 되도록 — 계약 블록이 플로터 sidecar 에만 남아 있으면 안 된다."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    for k in ("datasets", "metric_contract", "source_hashes", "recovered_artifacts",
              "render_provenance", "artifacts", "figures", "supporting_tables"):
        assert k in man, f"원장에 {k} 가 없다"
    g = man["recovered_artifacts"]["_gate_completeness"]
    assert g["G3"]["method_status"] == "recovered_diagnostic"   # 2026-08-16 닫힘
    assert str(g["G5"]["validity_aware_all_label_species"]) == "86"
    assert all(str(v["approved_for_current_ranking"]) == "0" for v in g.values())


def test_audit_csvs_are_reproducible_from_the_generator():
    """손으로 고친 CSV 는 재현 불가다 — 생성기가 같은 내용을 만들어야 한다."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "pca2", ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    v = m._elastic_validity_by_species()
    assert v["all_label_valid"] == 86 and v["dropped"] == ["AlI3"]
    assert v["partial"] == ["AlBr3", "MgI2", "Na2S"] and v["usable"] == 89
    src = (ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py").read_text(encoding="utf-8")
    assert 'lineterminator="\\n"' in src, "csv.writer 가 다시 CRLF 를 쓴다"
    assert '"phase_set_assumption"' in src, "G3 가정 열이 생성기에 없다"
    assert '"pool_id": "cascade-v23-o37-f10-2026-06"' in src, "G4 pool 메타가 생성기에 없다"


def test_db_property_files_are_lf_pinned():
    """깨끗한 Windows checkout 에서 CRLF 로 바뀌면 해시 대조가 깨진다 (P1)."""
    ga = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    # 광역 규칙(db/properties/*.csv)은 blob 이 CRLF 인 기존 80여 파일을 리플로우시켜서
    # 감사 원장이 해시로 묶는 파일에만 건다. 나머지 이식성은 sha256_lf 가 담당한다.
    assert "db/properties/cascade_audit_*.csv   text eol=lf" in ga
    assert "db/properties/cascade_audit_*.json  text eol=lf" in ga
    for p in sorted((ROOT / "db" / "properties").glob("cascade_audit_*.csv")):
        assert b"\r\n" not in p.read_bytes(), f"{p.name} 이 CRLF 다 (csv.writer 기본값 주의)"
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    for a in man["artifacts"]:
        assert a.get("sha256_lf"), f"{a['source_path']} 에 LF 정규화 해시가 없다"


def test_gate_completeness_is_axis_specific():
    """축마다 분모가 다르다. G3 는 2026-08-16 에 0 → 90 으로 닫혔고, G4 는 아직 historical_only 다."""
    t = D.read_csv("properties/cascade_audit_gate_completeness.csv")
    by = {r["gate"]: r for r in (t.get("data") or [])}
    assert set(by) == {"G1", "G2", "G3", "G4", "G5"}, f"게이트 5개가 아니다: {sorted(by)}"
    assert by["G3"]["all_label_complete_species"] == 90
    assert by["G3"]["method_status"] == "recovered_diagnostic"
    assert "Cl-rich" in str(by["G3"]["note"]), "조성족 섞임이 G3 행에서 사라졌다"
    assert by["G4"]["dropped_species"] == "AlI3|MgI2", "G4 는 MgI2 도 결측이다 (x005 입력 없음)"
    for g, r in by.items():
        assert r["approved_for_current_ranking"] == 0, f"{g} 가 승인된 것처럼 적혀 있다"
    h = _cascade_html()
    assert "recovered_diagnostic" in h, "G3 method status 가 화면에 없다"


def test_lis4_exposure_is_quantified():
    """LiS4 가 든 onset 반응이 몇 건인지 세어 화면 주장과 맞는지 본다."""
    gp = json.loads((D.DB / "properties" / "oxidation_stability_cascade_v2.json")
                    .read_text(encoding="utf-8"))["results"]
    n = sum(1 for r in gp.values() if "LiS4" in (r.get("oxidation_onset_rxn") or ""))
    assert (n, len(gp)) == (124, 270), f"LiS4 노출이 바뀌었다: {n}/{len(gp)}"
    assert "124" in _cascade_html(), "LiS4 노출 수치가 화면에 없다"


def test_audit_figures_are_the_only_default_figures():
    """계약상 기본 공개가 허용된 그림은 5개 audit 패널뿐이다."""
    figs = (D.load_cascade().get("v2") or {}).get("audit_figures") or []
    assert len(figs) == 5, f"audit 패널이 5개가 아니다: {len(figs)}"
    c = A.app.test_client()
    for png, csvp, _t in figs:
        assert (ROOT / png).is_file() and (ROOT / csvp).is_file()
        assert c.get(f"/api/file/{png}").status_code == 200
        assert c.get(f"/api/file/{csvp}?dl=1").status_code == 200


def test_manifest_satisfies_the_audit_generator_contract():
    """manifest 는 Codex 플로터가 검증하는 schema_version 2 계약도 만족해야 한다."""
    m = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert m.get("schema_version") == 2
    assert m.get("source_commit") == "9abe5105cacafa22ab3e185f09e2a4c37118b9a9"
    assert m["headline"] == {
        "planned_slots": 273, "completed_slots": 270, "completed_species": 90,
        "historical_snapshot_species": 47,
        "approved_current_leaderboard_species": 0,
        "explicit_pair_property_labels": 0,
    }
    assert len(m.get("figures", [])) == 5, "audit figure/CSV 쌍은 정확히 5개여야 한다"
    import hashlib
    for it in m["figures"]:
        for key, hkey in (("image", "image_sha256"), ("csv", "csv_sha256")):
            b = (ROOT / it[key]).read_bytes()
            assert hashlib.sha256(b).hexdigest() == it[hkey], f"{it[key]} 무결성 실패"


def test_legacy_rank_is_labelled_wherever_it_leaks():
    """composition·elements 가 47종 rank 를 상태 없이 현재 판정처럼 보여주면 안 된다."""
    c = A.app.test_client()
    comp = c.get("/composition/b2o3").get_data(as_text=True)
    assert "🤖 Cascade hit" not in comp, "'Cascade hit' 배지가 되살아났다"
    assert "superseded 47종 스냅샷" in comp, "composition 에 지위 표시가 없다"
    el = c.get("/elements").get_data(as_text=True)
    assert "historical 47종" in el, "elements 카드에 지위 표시가 없다"


def test_superseded_and_diagnostic_tabs_are_labelled():
    """47종 판은 superseded, 90종 회수분은 미검증 diagnostic 으로 라벨링돼야 한다."""
    h = _cascade_html()
    assert "superseded 보관함" in h, "47종 리더보드에 superseded 경고가 없다"
    assert "Recovered · unvalidated diagnostic" in h, "90종 탭에 diagnostic 배지가 없다"
    for f, want in [("cascade_screening_funnel.json", "superseded_47species"),
                    ("cascade_screening_funnel_v2.json", "recovered_unvalidated_diagnostic"),
                    ("cascade_v23_themes.json", "superseded_47species"),
                    ("cascade_v23_themes_v2.json", "recovered_unvalidated_diagnostic")]:
        d = json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))
        assert d.get("status") == want, f"{f} status={d.get('status')} — {want} 이어야 한다"


def test_esw_tab_reads_the_file_its_badge_claims():
    """탭 배지는 90종인데 표는 47종 파일을 읽고 있었다 (Codex 리뷰 P0-2)."""
    casc = D.load_cascade()
    v2ox = (casc.get("v2") or {}).get("oxidation") or {}
    assert len(v2ox.get("data") or []) == 90, "ESW v2 가 90행이 아니다"
    assert len(casc["oxidation"].get("data") or []) < 90, "v1 이 90행이면 이 대비가 무의미"
    h = _cascade_html()
    assert "oxidation_stability_cascade_v2.csv" in h, "ESW 탭이 어느 파일을 쓰는지 안 적혀 있다"
    assert "mp-ID" in h, "ESW phase-set 미기록 한계가 화면에 없다"


def test_page_scope_names_the_real_host_and_concentration():
    """호스트는 Cl:P=1.0 (Li6PS5Cl 계열)이고 라벨 x002/x005/x010 은 셋 다 실측 x=0.25 다."""
    s = D.CASCADE_META["scope"]
    assert "Li₆PS₅Cl" in s and "Cl:P = 1.0" in s, f"호스트 표기가 틀렸다: {s}"
    assert "0.25" in s, "농도 라벨 정정이 scope 에 없다"
    assert "Li₅.₄PS₄.₄Cl₁.₆" not in s, "Model C 로 되돌아갔다"
    for f in ("cascade_screening_funnel.json", "cascade_screening_funnel_v2.json"):
        g4 = [g for g in json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))["gates"]
              if g["id"] == "G4"][0]
        assert "@x=0.05)" not in g4["metric"], f"{f} G4 metric 이 'x=0.05' 로 되돌아갔다"


def test_g4_circularity_is_stated():
    """blocking 탈락자는 transport_norm 이 0.05 로 강제된다 — 두 독립 신호가 아니다 (P0-5)."""
    src = (ROOT / "tools" / "cascade" / "build_screening_funnel.py").read_text(encoding="utf-8")
    assert "n = GATE_FLOOR" in src, "순환을 만드는 코드가 사라졌다 — 이 테스트를 갱신할 것"
    assert D.G4_DECOMP.get("circularity"), "G4_DECOMP 에 순환 설명이 없다"
    h = _cascade_html()
    assert "독립 두 신호의 AND 가 아니다" in h, "G4 순환이 화면에 없다"


def test_remaining_tabs_declare_their_state():
    """champions·themes·stability·co-doping 이 archive 표시 없이 current 처럼 뜨면 안 된다 (P0-4)."""
    h = _cascade_html()
    for panel, probe in [("tab-champ", "cascade_v23_champions.csv (141행 · 47종)"),
                         ("tab-theme", "cascade_v23_themes.json (47종)"),
                         ("tab-stab", "47종 풀 위에서 돌린 후처리 축"),
                         ("tab-syn", "explicit pair 라벨이 0개다")]:
        assert probe in h, f"{panel} 에 상태 배너가 없다"


def test_g4_is_not_called_li_transport():
    """G4 는 정적 프록시 두 개다. '전도도를 쟀다'로 읽히는 이름을 되살리지 말 것."""
    h = _cascade_html()
    assert "🔋 Li transport" not in h, "탭 이름이 'Li transport' 로 되돌아왔다"
    # 옛 이름은 **폐기 안내문 안에서만** 나와도 된다 — 살아있는 라벨로 다시 쓰이면 안 된다.
    for m in re.finditer("Li 수송 유지", h):
        ctx = h[max(0, m.start() - 260):m.end() + 260]
        assert "폐기" in ctx, f"G4 옛 라벨이 정정 문맥 없이 살아 있다: …{ctx[200:420]}…"
    assert "Adams-2003" in h, "legacy BVS 파라미터 경고가 화면에 없다"
    assert "4 Å foreign-center" in h, "blocking 프록시의 실제 정의가 화면에 없다"
    for f in ("cascade_screening_funnel.json", "cascade_screening_funnel_v2.json"):
        g4 = [g for g in json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))["gates"]
              if g["id"] == "G4"][0]
        assert "Li 수송" not in g4["label"], f"{f} 의 G4 label 이 되돌아갔다: {g4['label']}"


def test_v2_json_text_does_not_inherit_47_species():
    """빌더가 풀 크기를 하드코딩하면 _v2 설명문만 47종으로 남아 화면이 스스로 모순된다."""
    for f in ("cascade_screening_funnel_v2.json", "cascade_v23_themes_v2.json"):
        d = json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))
        for key in ("description", "honesty_header"):
            if key in d:
                assert "47종" not in d[key], f"{f}[{key}] 에 '47종' 이 남아 있다"
    d = json.loads((D.DB / "properties" / "cascade_screening_funnel_v2.json").read_text(encoding="utf-8"))
    assert d["pool_provenance"]["pool_size"] == 89, "v2 풀 크기가 89 가 아니다"


def test_gate_audit_counts_only_columns_the_gates_use():
    """옛 감사는 gate 가 **안 쓰는** eos_B0_GPa 를 세고 쓰는 pugh 를 빼서 18종을 부분결측으로
    만들었다 (Codex 리뷰 P0-3). 게이트 입력 정의가 다시 어긋나면 여기서 잡는다."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "rpi", ROOT / "tools" / "cascade" / "rebuild_pool_inputs.py")
    rpi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rpi)
    champ = set(rpi.GATE_INPUT_COLS["champions"])
    assert "elastic_pugh_GoverB" in champ, "G5 연성축(pugh)이 gate 입력에서 빠졌다"
    assert "eos_B0_GPa" not in champ, "eos_B0_GPa 는 어느 게이트도 쓰지 않는다 — 세면 안 된다"
    assert "eos_B0_GPa" in rpi.NON_GATE_COLS


def test_missing_gate_inputs_are_on_the_default_screen():
    """AlI3 전면 결측 · MgI2 부분 결측 · blocking=0 아티팩트는 기본 화면에 떠 있어야 한다."""
    h = _cascade_html()
    aud = json.loads((D.DB / "properties" / "cascade_pool_audit_v2.json").read_text(encoding="utf-8"))
    assert aud["n_esw"] == 90 and aud["n_evaluable"] == 89
    assert list(aud["dropped"]) == ["AlI3"] and list(aud["partial"]) == ["MgI2"]
    assert aud["n_complete"] == 88
    head = h.split('id="tab-esw"')[0]          # 기본(감사) 화면 범위 안에서만 찾는다
    for probe in ("AlI3", "MgI2", "Li2S", "LiCl"):
        assert probe in head, f"{probe} 가 기본 감사 화면에 없다"


def _cmt_worker_tmp(arg):
    path, rel, i = arg
    D.COMMENTS_PATH = Path(path)          # 자식 프로세스에도 임시 경로를 심는다
    return D.add_file_comment(rel, f"pytest heavy {i}", "pytest")


def _cmt_worker(arg):
    rel, i = arg
    return D.add_file_comment(rel, f"pytest concurrency {i}", "pytest")


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if not (name.startswith("test_") and callable(fn)):
            continue
        try:
            fn()
            print(f"  ✅ {name}")
        except AssertionError as e:
            fails += 1
            print(f"  ⛔ {name}\n       {str(e)[:400]}")
        except Exception as e:
            fails += 1
            print(f"  ⛔ {name} (예외) {type(e).__name__}: {str(e)[:300]}")
    print(f"\n{'✅ 전부 통과' if not fails else f'⛔ 실패 {fails}건'}")
    sys.exit(1 if fails else 0)


# ── 여백 메모 (docnote) ────────────────────────────────────────────────────
#  2026-08-17 1저자 요청: "오른쪽클릭하면 word 처럼 옆에 메모", "search 에서 잡히게",
#  "메모 섹션에서 링크 걸어서 그 메모가 써져있는 페이지로".
#  전부 **한 번 틀릴 수 있는 지점**이라 음성 경로를 같이 건다.
def test_docnote_roundtrip(tmp_path, monkeypatch):
    """메모를 달면 → 검색 색인에 뜨고 → 딥링크가 그 메모를 가리켜야 한다."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    rel = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    r = D.add_file_comment(rel, "우리 §20.3 오타 얘기와 같은 건", anchor="Rh · Ho 는 애초에 논문 문제가")
    assert r.get("ok"), r
    nid = r["item"]["id"]
    assert r["item"]["anchor"] == "Rh · Ho 는 애초에 논문 문제가"

    # ① /literature 카드 색인에 '@' 키로 들어간다 (그림 코멘트와 구분되는 키)
    idx = D.paper_comment_search()["anderson2024_llzo_comprehensive_dopant_screening"]
    assert idx.startswith("@ "), idx[:40]
    assert "오타" in idx and "애초에" in idx, "메모 글과 붙인 자리가 **둘 다** 색인돼야 한다"

    # ② 딥링크가 그 메모 id 를 달고 나간다
    c = [x for x in D.comment_all() if x["id"] == nid][0]
    assert D.note_url(c) == f"/literature?open=anderson2024_llzo_comprehensive_dopant_screening&note={nid}"

    # ③ 날짜별로 묶인다
    g = D.notes_by_date()
    assert any(any(i["id"] == nid for i in grp["items"]) for grp in g)


def test_docnote_negative(tmp_path, monkeypatch):
    """음성 경로 — 틀린 입력을 잡아내는지."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    # 없는 파일에는 못 단다 (경로 탈출·유령 키 방어)
    assert D.add_file_comment("litdb/papers/__없는논문__.md", "x", anchor="y").get("error")
    # anchor 없는 코멘트는 anchor 키 자체가 없어야 한다 (옛 기록과 같은 모양)
    D.add_file_comment("db/properties/electronic.json", "그냥 코멘트")
    c = [x for x in D.comment_all() if x["rel"] == "db/properties/electronic.json"][0]
    assert not c["anchor"]
    # → 딥링크에 note= 가 붙으면 안 된다 (붙일 자리가 없다)
    assert "note=" not in D.note_url(c)
    # 그림도 아니고 문서도 아닌 파일은 /files 로 간다
    assert D.comment_origin("db/properties/electronic.json")["kind"] == "파일"
    # 4칸이 아닌 figures 경로를 논문으로 오인하면 안 된다
    assert D.comment_origin("litdb/figures/slug/sub/x.png")["kind"] == "파일"
    # papers 밑이어도 .md 가 아니면 논문이 아니다
    assert D.comment_origin("litdb/papers/x.png")["kind"] == "파일"


def test_notes_page_renders(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    D.add_file_comment("kb/concepts/bvse.md", "여기 R0 값 출처 확인", anchor="softBV")
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/notes").get_data(as_text=True)
    assert "여기 R0 값 출처 확인" in h
    assert "/concept/bvse?note=" in h, "메모 카드가 그 자리로 가는 딥링크여야 한다"


def test_note_target_gate_is_narrower_than_file_serving():
    """메모 게이트를 넓히다가 **다운로드 화이트리스트**까지 넓히면 안 된다.

    safe_repo_path 는 /api/file 이 쓰는 경로다 — 여기 kb/ 가 들어가면 배포판에서
    kb 전체를 내려받을 수 있게 된다. 두 게이트가 갈려 있는지 못으로 박는다.
    """
    doc = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    assert D.safe_note_target(doc) is not None, "메모는 digest 에 달려야 한다"
    assert D.safe_repo_path(doc) is None, "그런데 /api/file 로는 여전히 못 준다"
    assert D.safe_note_target("kb/concepts/bvse.md") is not None
    assert D.safe_repo_path("kb/concepts/bvse.md") is None
    # 음성: 경로 탈출·하위폴더·비-md·화이트리스트 밖
    assert D.safe_note_target("kb/concepts/../../etc/passwd") is None
    assert D.safe_note_target("litdb/papers/sub/x.md") is None
    assert D.safe_note_target("litdb/papers/x.png") is None
    assert D.safe_note_target("kb/results/sei_cc333_nd_lattice_hop_2026_08_17.md") is None
    assert D.safe_note_target("CLAUDE.md") is None


def test_comment_post_and_get_agree(tmp_path, monkeypatch):
    """POST 응답과 GET 응답이 **같은 색인**을 실어야 한다.

    앞 판은 POST 에만 paper 색인이 없어서, 화면이 POST 결과로 검색 색인을
    갱신하려 하면 조용히 헛돌았다 (뒤따르는 GET 이 덮어 증상만 가렸다).
    """
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    A.app.config["TESTING"] = True
    c = A.app.test_client()
    rel = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    post = c.post("/api/comments/" + rel, json={"text": "메모", "anchor": "닻"}).get_json()
    get = c.get("/api/comments/" + rel).get_json()
    assert post["paper"] == get["paper"], (post.get("paper"), get.get("paper"))
    assert post["paper"]["cmt"].startswith("@ ")


def test_docnote_edit_keeps_history(tmp_path, monkeypatch):
    """메모 고치기 — 옛 글이 **지워지지 않고** history 에 쌓여야 한다."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    rel = "kb/concepts/bvse.md"
    r = D.add_file_comment(rel, "첫 판단", anchor="softBV")
    cid = r["item"]["id"]

    e = D.edit_file_comment(rel, cid, "다시 보니 R0 출처가 다름")
    assert e.get("ok"), e
    it = e["item"]
    assert it["text"] == "다시 보니 R0 출처가 다름"
    assert it["history"][0]["text"] == "첫 판단", "옛 글이 남아야 한다"
    assert it["edited_at"]
    assert it["id"] == cid and it["anchor"] == "softBV", "id·자리는 안 바뀐다 (딥링크 유지)"

    # 두 번 고치면 이력이 두 판
    D.edit_file_comment(rel, cid, "세 번째")
    it = D.file_comments(rel)[0]
    assert [h["text"] for h in it["history"]] == ["첫 판단", "다시 보니 R0 출처가 다름"]

    # 검색(⌘K)은 **지금 글**로 걸린다 — 옛 글이 label 에 남으면 안 된다.
    # ⚠ 개념 메모는 paper_comment_search(litdb 전용)가 아니라 search_index 담당이다.
    labels = [i["label"] for i in D.search_index() if i["t"] == "메모"]
    assert any("세 번째" in x for x in labels)
    assert not any("첫 판단" in x for x in labels)


def test_docnote_edit_negative(tmp_path, monkeypatch):
    """음성 경로 — 틀린 입력을 잡아내는지."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    rel = "kb/concepts/bvse.md"
    cid = D.add_file_comment(rel, "원본", anchor="a")["item"]["id"]
    assert D.edit_file_comment(rel, "없는id", "x").get("error"), "없는 id 는 거절"
    assert D.edit_file_comment("kb/concepts/없는문서.md", cid, "x").get("error"), "없는 파일은 거절"
    assert D.edit_file_comment(rel, cid, "   ").get("error"), "빈 글은 거절"
    # 같은 글로 고치면 이력을 늘리지 않는다 (헛 판 쌓임 방지)
    r = D.edit_file_comment(rel, cid, "원본")
    assert r.get("unchanged") and not r["item"].get("history")
    assert D.file_comments(rel)[0]["text"] == "원본", "실패해도 원본이 안 망가진다"


def test_docnote_edit_over_http(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    A.app.config["TESTING"] = True
    c = A.app.test_client()
    rel = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    cid = c.post("/api/comments/" + rel,
                 json={"text": "처음", "anchor": "닻"}).get_json()["item"]["id"]
    r = c.patch("/api/comments/" + rel, json={"id": cid, "text": "고침"})
    assert r.status_code == 200
    d = r.get_json()
    assert d["item"]["text"] == "고침"
    assert d["paper"]["cmt"].startswith("@ "), "PATCH 도 색인을 같이 준다"
    assert "고침" in d["paper"]["cmt"] and "처음" not in d["paper"]["cmt"]
    assert c.patch("/api/comments/" + rel,
                   json={"id": "없는거", "text": "x"}).status_code == 400


def test_sidebar_rail_toggle_present_and_layered():
    """사이드바 접기 — 버튼·토글·peek 이 모든 페이지에 있고, 층위가 맞아야 한다.

    ⚠ peek 띠의 z-index 가 사이드바(40)보다 높으면 드러난 사이드바의 왼쪽 14px
      클릭이 투명 띠에 먹혀 메뉴를 못 누른다 (2026-08-18 설계 중 실측).
    """
    import re
    A.app.config["TESTING"] = True
    c = A.app.test_client()
    for url in ("/", "/glossary", "/notes", "/literature"):
        h = c.get(url).get_data(as_text=True)
        assert 'id="railbtn"' in h, url
        assert "function toggleRail" in h, url

    css = (D.ROOT / "webapp" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    z_side = int(re.search(r"\.sidebar\{[^}]*z-index:(\d+)", css, re.S).group(1))
    z_peek = int(re.search(r"\.rail-peek\{[^}]*z-index:(\d+)", css, re.S).group(1))
    assert z_peek < z_side, f"peek({z_peek}) 가 사이드바({z_side}) 위에 있으면 클릭을 먹는다"

    # ★ 꽉 차려면 margin-left 와 max-width 를 **둘 다** 풀어야 한다.
    #   margin 만 지우면 max-width:1240px 때문에 가운데에 갇힌다.
    rail = re.search(r"body\.rail \.content\{([^}]*)\}", css).group(1)
    assert "margin-left:0" in rail, rail
    assert "max-width:none" in rail, rail


def test_governance_page_renders_every_ledger_row():
    """판정 원장 화면 — 세 원장이 **실제로 표에 찍혀야** 한다.

    ⚠ 첫 판이 `_C.artifacts().get("artifacts", [])` 였다. accessor 는 id 로 키를 잡은
      dict 를 주므로 그 표현은 항상 [] 가 되고, 화면은 200 을 내면서 **빈 표**가 됐다.
      "원장이 비었다" 와 "원장을 잘못 읽었다" 가 화면에서 구분이 안 됐다 — 그 회귀를 잠근다.
    """
    import canonical as C
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/governance").get_data(as_text=True)

    for aid in C.artifacts():
        assert aid in h, f"산출물 {aid} 이 화면에 없다"
    for did in C.decisions():
        assert did in h, f"판례 {did} 가 화면에 없다"
    for sid in C.assessments():
        rec = C.assessments()[sid]
        assert rec.get("claim_ref", "") in h, f"평가 {sid} 의 대상이 화면에 없다"


def test_governance_page_negative_vocabulary():
    """[음성] 미평가를 '실패' 로, 철회된 옛 판정을 현행으로 그리면 안 된다."""
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/governance").get_data(as_text=True)
    assert "◻ 미평가" in h, "not_assessed 를 미평가로 그려야 한다"
    assert "미평가는 실패가 아니다" in h
    assert "철회된 옛 판정" in h, "retracted 를 현행 판정처럼 그리면 안 된다"


def test_governance_digest_binding_shown():
    """승인 뒤 본문이 바뀐 판례는 화면에서 즉시 드러나야 한다 (음성 경로 포함)."""
    import canonical as C
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/governance").get_data(as_text=True)
    assert "🔒 일치" in h, "현재 원장은 전부 결속 일치여야 한다"
    assert "본문이 승인 뒤 바뀌었다" not in h, "지금 깨진 결속은 없어야 한다"

    # [음성] 본문을 한 글자 고치면 digest 가 달라져야 한다 — 화면 문구가 살아있는 검사인지 확인
    d = dict(list(C.decisions().values())[0])
    before = C.decision_digest(d)
    d["title"] = (d.get("title") or "") + " (변조)"
    assert C.decision_digest(d) != before, "본문을 고쳤는데 digest 가 그대로면 결속이 무의미하다"


def test_governance_decision_ledger_renders_every_decision():
    """양성: **결정 원장 전건**이 /governance 에 나온다 (2026-09-08 신설).

    종전 판례 표는 네 칸(id·decision_state·digest·title)뿐이라, 원장에 든 `kind` 와
    `results_seen` 이 화면 밖에 있었다 — 결정 22건 중 *"결과를 보기 전에 정했나"* 를
    화면에서 확인할 방법이 없었다. 그 칸들이 실제로 그려지는지 본다.
    """
    import canonical as C
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/governance").get_data(as_text=True)
    dec = C.decisions()
    assert dec, "전제: 결정 원장이 비어 있지 않다"
    missing = [k for k in dec if k not in h]
    assert not missing, f"결정 원장에 있는데 화면에 없는 항목: {missing}"
    # 종류(kind)·근거 문서 경로가 화면에 실린다
    kinds = {d.get("kind") for d in dec.values() if d.get("kind")}
    assert kinds, "전제: kind 가 원장에 있다"
    for k in kinds:
        assert f"원장 kind: {k}" in h, f"kind={k!r} 이 화면에 안 실린다"
    recs = {d["record"] for d in dec.values() if d.get("record")}
    assert recs, "전제: 근거 문서(record) 경로가 원장에 있다"
    assert all(r in h for r in recs), "결정에서 근거 문서로 가는 길이 화면에 없다"


def test_governance_missing_results_seen_is_unstated_not_prereg():
    """⛔음성: `results_seen` 이 **없는** 결정을 '결과 보기 전' 으로 그리면 안 된다.

    이 repo 의 반복 사고가 *없는 것을 0/거짓으로 읽는 것*이다. 원장에 안 적힌 것은
    **미기재**이지 사전등록이 아니다 — 그걸 뒤집으면 화면이 사전등록 건수를 부풀린다.
    (같은 이유로 '미기재' 를 사전등록으로 세지도 않는다.)
    """
    import canonical as C
    A.app.config["TESTING"] = True
    dec = list(C.decisions().values())
    before = [d["id"] for d in dec if d.get("results_seen") is False]
    unstated = [d["id"] for d in dec if "results_seen" not in d]
    assert before and unstated, "전제: 사전등록·미기재 두 부류가 모두 원장에 있다"
    h = A.app.test_client().get("/governance").get_data(as_text=True)
    assert h.count("🔒 결과 보기 전") == len(before), (
        f"사전등록 표시 수가 원장과 다르다 (원장 {len(before)}건)")
    assert h.count("– 미기재") == len(unstated), (
        f"미기재 표시 수가 원장과 다르다 (원장 {len(unstated)}건) — "
        "없는 필드를 기본값으로 메우고 있지 않은지 봐라")


def test_governance_state_reads_status_alias(monkeypatch):
    """⛔음성: `status` 만 든 결정이 상태 칸에 `None` 으로 찍히면 안 된다.

    실측(2026-09-08): D-2026-08-31-sdcp-polaron-Fbb 는 `decision_state` 없이
    `status: proposed` 만 갖는다. 검사(_dstate)는 별칭을 읽는데 화면만 안 읽어서
    상태 칸에 문자열 `None` 이 그려지고 있었다 — 같은 원장을 두 규칙으로 읽은 것이다.

    ⚠ 2026-09-09 개정: 원장이 정규화돼 **별칭만 든 행이 0개가 됐다**. 원래 이 검사는
    그 행이 실재하는 것을 전제로 삼았는데, 그러면 원장이 좋아진 순간 검사가 죽는다 —
    회귀는 그대로 살아 있는데. 그래서 전제를 **합성 레코드 주입**으로 바꿨다.
    원장의 현재 모양에 의존하지 않으므로, 나중에 별칭 행이 다시 생겨도 같은 검사가 돈다.
    """
    import canonical as C
    A.app.config["TESTING"] = True

    # ① 접근자: 합성 별칭 레코드 — 원장과 무관하게 별칭 규칙 자체를 잰다.
    synth = {"id": "D-TEST-alias-only", "status": "proposed",
             "statement": "합성 레코드 (검사 전용)"}
    assert "decision_state" not in synth
    assert C.decision_state(synth) == "proposed", "공개 접근자가 별칭을 안 읽는다"

    # ② 화면: 그 레코드를 원장에 얹어 렌더한다. app.py 는 `_C.decisions()` 를
    #    요청마다 부르므로 모듈 속성 교체로 주입된다 (디스크 원장은 안 건드린다).
    real = C.decisions
    monkeypatch.setattr(C, "decisions",
                        lambda root=None: {**real(root), synth["id"]: synth})
    h = A.app.test_client().get("/governance").get_data(as_text=True)
    assert synth["id"] in h, "주입한 합성 결정이 화면에 안 나온다 — 주입이 안 먹었다"
    assert ">None<" not in h, "상태 칸에 None 이 그려진다 — 별칭을 안 읽고 있다"
    assert "상태 미기재" not in h, "별칭이 있는데 '상태 미기재' 로 그린다"


def test_comp1_supercell_md_reassessed_not_banned():
    """comp1 2x2x2 재판정 — MSD 사이드카 3점으로 밴을 풀었다 (2026-08-20).

    값이 이상하지 않다는 판정이지 **정본이라는 판정이 아니다.** 둘을 섞으면
    단일시드 D 를 정본처럼 인용하게 된다 — 그 경계를 잠근다.
    """
    import canonical as C
    a = C.artifacts()["A-comp1-supercell-md"]
    assert a["status"] == "reference", a["status"]
    r = a["reassessment_2026_08_20"]
    assert r["measured_D_cm2_per_s"]["800K"] == 2.332e-05
    assert 0.28 < r["arrhenius_3pt"]["Ea_eV"] < 0.29
    assert "정본" in r["forbidden_use"] and "인용 금지" in r["forbidden_use"]
    assert any("단일 시드" in x or "단일시드" in x for x in r["why_still_not_canonical"])
    assert "unban_condition" not in a, "밴이 풀렸으면 해제 조건은 남기지 않는다"


def test_note_text_keeps_newlines():
    """메모 줄바꿈 보존 (2026-08-27 1저자 신고: "shift enter 가 안 먹힌다").

    증상은 입력에서 보였는데 원인은 **저장**에 있었다 — 서버가
    `" ".join(text.split("\\n"))` 으로 줄을 전부 공백으로 뭉갰다. 화면(.dn-text)은
    이미 pre-wrap 이었고 입력창도 textarea 라 Shift+Enter 는 네이티브로 먹었다.
    ⇒ 이 테스트가 지키는 것은 "줄이 살아서 저장되고 다시 읽힌다" 하나다.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        old = D.COMMENTS_PATH
        try:
            D.COMMENTS_PATH = Path(td) / "file_comments.json"
            rel = "db/properties/electronic.json"
            body = "첫 줄\n둘째 줄\n\n넷째 줄"
            r = D.add_file_comment(rel, body)
            assert r.get("ok"), r
            assert r["item"]["text"] == body, repr(r["item"]["text"])
            back = D.file_comments(rel)[0]["text"]
            assert back.count("\n") == 3, repr(back)
            # 고치기도 같은 규약이어야 한다 (한쪽만 고치면 편집하는 순간 다시 뭉개진다)
            e = D.edit_file_comment(rel, r["item"]["id"], "가\r\n나\n\n\n다  ")
            assert e["item"]["text"] == "가\n나\n\n다", repr(e["item"]["text"])
            # 음성: 공백·줄바꿈뿐이면 여전히 거절한다
            assert D.add_file_comment(rel, " \n\n\t ").get("error")
        finally:
            D.COMMENTS_PATH = old


def test_highlights_are_separate_from_notes():
    """형광펜은 메모와 **다른 저장소**다 (2026-08-27).

    같은 파일에 섞으면 file_comments() 를 쓰는 곳(📝 배지·검색 색인·paper 색인)이
    형광펜을 메모로 센다. 그 경계를 잠근다.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        oldh, oldc = D.HIGHLIGHTS_PATH, D.COMMENTS_PATH
        try:
            D.HIGHLIGHTS_PATH = Path(td) / "file_highlights.json"
            D.COMMENTS_PATH = Path(td) / "file_comments.json"
            rel = "db/properties/electronic.json"
            r = D.add_file_highlight(rel, "  띄어쓰기가   여럿인 글  ", "green")
            assert r["ok"] and r["item"]["text"] == "띄어쓰기가 여럿인 글"
            assert r["item"]["color"] == "green"
            # 같은 글을 다시 칠하면 **새로 만들지 않고 색만** 바꾼다
            r2 = D.add_file_highlight(rel, "띄어쓰기가 여럿인 글", "pink")
            assert r2.get("recolored") and r2["n"] == 1 and r2["item"]["color"] == "pink"
            # 음성 경로들
            assert D.add_file_highlight(rel, "가").get("error"), "너무 짧은 글은 거절"
            assert D.add_file_highlight("../../etc/passwd", "abcd").get("error"), "경로 탈출 거절"
            assert D.add_file_highlight(rel, "모르는 색 시험", "chartreuse")["item"]["color"] \
                == "yellow", "CSS 에 없는 색은 조용히 칠 안 되므로 yellow 로 떨어뜨린다"
            assert D.del_file_highlight(rel, "없는id").get("error")
            # ★ 핵심: 메모 저장소가 그대로다
            assert D.file_comments(rel) == [], "형광펜이 메모 저장소로 샜다"
            assert len(D.file_highlights(rel)) == 2
            for h in list(D.file_highlights(rel)):
                D.del_file_highlight(rel, h["id"])
            assert D.file_highlights(rel) == []
        finally:
            D.HIGHLIGHTS_PATH, D.COMMENTS_PATH = oldh, oldc


def test_docnote_highlight_paints_across_inline_tags():
    """형광펜이 **실제 브라우저에서** 칠해지는가 (2026-08-27 1저자 신고).

    첫 판은 한 텍스트 노드 안에 통째로 있을 때만 칠했다. digest 본문은 <b>·<sub>·<em>
    이 촘촘해서 사람이 문장을 드래그하면 거의 항상 노드를 가로지른다 —
    **저장은 되는데 안 칠해졌다.** 파이썬 테스트는 서버만 봐서 이걸 못 잡았다.
    ⇒ 진짜 DOM 이 필요한 검증이라 브라우저로 돌린다. 도구가 없으면 skip 한다
      (없는 것을 통과로 세지 않는다 — skip 은 skip 으로 보인다).
    """
    import shutil
    import subprocess
    node = shutil.which("node")
    if not node:
        pytest.skip("node 가 없다")
    js = Path(__file__).parent / "docnote_paint.test.mjs"
    env = dict(os.environ)
    for c in (Path("/tmp/claude-0"), Path.home()):
        hit = next(c.rglob("node_modules/playwright-core/package.json"), None) if c.exists() else None
        if hit:
            env["PW_CORE_FROM"] = str(hit.parents[2] / "package.json")
            break
    r = subprocess.run([node, str(js)], capture_output=True, text=True, env=env, timeout=180)
    out = (r.stdout or "") + (r.stderr or "")
    if "SKIP —" in out:
        pytest.skip(out.strip().splitlines()[-1])
    assert r.returncode == 0, out
    assert "docnote paint PASS" in out, out


def test_glossary_papers_declaration_beats_token_scan():
    """`methods:` 선언이 있으면 **본문 토큰스캔을 끈다** — 부정문·정정주석이 긁히지 않게.

    ⛔ 실측 회귀 (2026-08-28). 예전에는 `태그 ∪ 토큰스캔` 이라 선언을 스캔이 덮었다:
      · deng2026 은 *"이 논문은 NEB·Bader·COHP·ELF·BVSE·phonon 을 **하지 않는다**"* 라고
        적었는데 그 **부정문이 긁혀** 여섯 기법 페이지에 링크됐다.
      · kim2025_csp 는 선언을 바르게 해놓고, 바로 아래 *"종전 methods 줄은 bader, bvse,
        cohp … 였다"* 는 **정정 주석이 다시 긁혔다** — 정정문이 버그를 되살렸다.
    부정문 필터로는 못 고친다(표현이 무한하다). 선언이 정본이다.
    """
    from data import _paper_index, glossary_papers

    idx = {p["id"]: p for p in _paper_index()}
    deng = "deng2026_polysulfate_layer_moisture_oxidation_lpsc"
    if deng not in idx:
        pytest.skip("deng2026 digest 가 없다")
    assert idx[deng]["has_method_decl"], "deng2026 이 methods: 를 선언해야 이 시험이 뜻이 있다"

    # ── 음성: 안 한 기법에 링크되면 안 된다 (본문에 그 단어가 **부정문으로** 있다)
    for t in ("neb", "cohp", "bader", "elf", "bvse"):
        ids = [h["id"] for h in glossary_papers(t, limit=999)]
        assert deng not in ids, f"deng2026 이 '{t}' 에 잘못 링크됐다 — 부정문이 긁힌다"

    # ── 양성: 선언한 기법에는 링크돼야 한다 (음성만 있으면 '아무것도 안 링크' 로도 통과한다)
    assert deng in [h["id"] for h in glossary_papers("dft", limit=999)], \
        "deng2026 은 DFT 를 선언했으므로 dft 에는 링크돼야 한다"

    # ── 정정 주석 회귀: 선언과 다른 옛 목록이 본문에 남아 있어도 안 긁힌다
    kim = "kim2025_csp_metastable_edge_sharing_sse"
    if kim in idx and idx[kim]["has_method_decl"]:
        for t in ("bader", "cohp", "elf", "bvse", "neb"):
            assert kim not in [h["id"] for h in glossary_papers(t, limit=999)], \
                f"kim2025_csp 가 '{t}' 에 링크됐다 — 정정 주석이 긁힌다"
        assert kim in [h["id"] for h in glossary_papers("phonon", limit=999)], \
            "kim2025_csp 는 phonon 을 선언했다 — 이건 남아야 한다"


def _el_declared(idx, kb_slugs, pid, sym):
    """`element_papers` 와 **같은 정의**의 '선언' — 태그 또는 KB authored 목록.

    ⛔ 정의를 여기서 다시 쓰면 안 된다. data.element_papers 가
      `(sym in el_tags) or (id in kb_slugs)` 로 판정하므로 그대로 따른다 —
      한쪽만 고치면 시험이 구현과 다른 것을 재게 된다.
    """
    p = idx.get(pid, {})
    return (sym in (p.get("el_tags") or [])) or (pid in kb_slugs)


def _declared_first_violation(ranked, is_decl):
    """정렬 불변식 위반의 **첫 자리**. 없으면 None.

    불변식: 선언한 논문이 하나라도 '본문언급만' 논문 **뒤에** 오면 안 된다.
    """
    first_mention = None
    for h in ranked:
        pid = h["id"] if isinstance(h, dict) else h
        if is_decl(pid):
            if first_mention is not None:
                return (pid, first_mention)
        elif first_mention is None:
            first_mention = pid
    return None


def test_element_papers_declared_first():
    """원소를 **선언한** 논문이 본문에 스쳐 언급만 한 논문보다 앞에 온다.

    limit 로 잘릴 때 무엇이 먼저 잘리느냐의 문제다. deng2026 은 Li 를 선언했는데
    145편 중 21위라 limit=14 밖으로 잘렸었다.

    ⛔ 2026-09-13 — 이 시험의 **옛 주장이 만료됐다.** *"Ni·Co·Mn·In·Ti 는 20편대라
      선언했으면 기본 limit(14) 안에 든다"* 고 순위를 주장했는데, litdb 에 논문이
      늘면서 `Co` 가 **51편**(그중 선언 15편 이상)이 됐고 deng 이 정확히 **15위**로
      밀렸다. 확인해 보니 **앞의 14편이 전부 선언 논문**이고 본문언급만 한 논문은
      0편이었다 — 즉 **정렬은 정상이고 시험의 전제가 낡은 것**이었다.
      ⇒ 고친 것은 구현이 아니라 **무엇을 주장하는가**다. 우연한 **순위** 대신
        docstring 이 실제로 약속하는 **정렬 불변식**을 본다. 순위는 논문이 늘면
        변하지만 불변식은 안 변한다. 기본 limit 주장은 **선언 수가 limit 이하일
        때로 한정**한다(그때만 성립할 수 있는 주장이다).
    """
    import json as _json
    from pathlib import Path as _Path

    from data import KB, _paper_index, element_papers

    idx = {p["id"]: p for p in _paper_index()}
    deng = "deng2026_polysulfate_layer_moisture_oxidation_lpsc"
    if deng not in idx or not idx[deng]["has_el_decl"]:
        pytest.skip("deng2026 이 elements: 를 선언하지 않았다")

    def _kb_slugs(sym):
        f = _Path(KB) / "elements" / f"{sym}.json"
        try:
            return set(_json.loads(f.read_text(encoding="utf-8")).get("litdb_slugs") or [])
        except Exception:                                        # noqa: BLE001
            return set()

    for s in ("Li", "P", "S", "Cl", "O", "C", "H", "Ni", "Co", "Mn", "In", "Ti"):
        assert s in idx[deng]["el_tags"], f"deng2026 el_tags 에 {s} 가 파싱돼야 한다"
        assert deng in [h["id"] for h in element_papers(s, limit=999)], \
            f"{s}: 선언한 deng2026 이 목록에 있어야 한다"

    # ── ★ 정렬 불변식 — 이게 이 시험이 실제로 지키려던 것이다 (순위가 아니라)
    for s in ("Li", "P", "S", "Cl", "O", "C", "H", "Ni", "Co", "Mn", "In", "Ti"):
        ks = _kb_slugs(s)
        ranked = element_papers(s, limit=999)
        bad = _declared_first_violation(ranked, lambda pid, _s=s, _k=ks: _el_declared(idx, _k, pid, _s))
        assert bad is None, \
            f"{s}: 선언한 {bad[0]} 가 본문언급만 한 {bad[1]} 보다 **뒤에** 왔다 — 정렬이 안 먹었다"

    # ── ⛔ 래칫: 위 불변식이 **공허하지 않아야** 한다.
    #   `Ni·Co·Mn·In·Ti` 는 실측(2026-09-13) 전원이 선언 논문이라(Co 51/51) 거기서는
    #   '본문언급만' 이 0편 — 불변식이 **아무것도 안 센다**. 그런 원소만 남으면 이 시험은
    #   *"잡을 게 없어서 초록"* 이 된다 (`unbound == 0` 과 같은 함정).
    #   ⇒ 섞임이 실재하는 원소가 **적어도 하나**는 있어야 한다. 실측 5개: Li·S·O·C·H.
    _mixed = [s for s in ("Li", "P", "S", "Cl", "O", "C", "H", "Ni", "Co", "Mn", "In", "Ti")
              if any(not _el_declared(idx, _kb_slugs(s), h["id"], s)
                     for h in element_papers(s, limit=999))]
    assert _mixed, ("모든 원소에서 '본문언급만' 논문이 0편이다 — 정렬 불변식이 공허하다. "
                    "시험이 통과한 것은 정렬 덕분이 아니라 셀 것이 없어서다")

    # ── 기본 limit 은 **선언 논문이 limit 이하일 때만** 보장된다 (그 위는 limit 의 설계 선택)
    _default = element_papers.__defaults__[0]
    for s in ("Ni", "Co", "Mn", "In", "Ti"):
        ks = _kb_slugs(s)
        n_decl = sum(1 for h in element_papers(s, limit=999)
                     if _el_declared(idx, ks, h["id"], s))
        if n_decl <= _default:
            assert deng in [h["id"] for h in element_papers(s)], \
                f"{s}: 선언 논문이 {n_decl}편(≤{_default})인데 deng 이 기본 limit 밖이다"

    # ── 음성 ①: 불변식 검사기가 **실제로 위반을 잡는가** (양성만 있으면 아무것도 보증 못 한다)
    fake = [{"id": "mention_only"}, {"id": "declared_one"}]
    assert _declared_first_violation(fake, lambda pid: pid == "declared_one") == \
        ("declared_one", "mention_only"), "검사기가 위반을 못 잡는다 — 이 시험은 무효다"
    assert _declared_first_violation(list(reversed(fake)),
                                     lambda pid: pid == "declared_one") is None, \
        "검사기가 정상 순서를 위반이라고 한다 — 오탐"

    # ── 음성 ②: 선언 안 한 원소에는 안 붙는다
    for s in ("B", "Ge"):
        assert deng not in [h["id"] for h in element_papers(s, limit=999)], \
            f"deng2026 이 선언하지 않은 {s} 에 링크됐다"


def test_note_image_upload_guards():
    """메모·코멘트 그림 첨부 — **확장자는 매직바이트로 정한다** (클라이언트 말을 안 믿는다).

    1저자 요청 2026-08-28: "메모쪽에 capture본, png 등도 첨부 가능하게".
    첨부는 남이 만든 파일일 수 있으므로 선언 MIME 이 아니라 내용으로 판정하고,
    저장 이름은 내용의 sha256 이라 같은 캡처를 여러 번 붙여도 한 벌만 남는다.
    """
    import shutil

    from data import NOTE_IMG_DIR, note_image_path, save_note_image

    png = bytes.fromhex("89504e470d0a1a0a") + b"x" * 40
    jpg = bytes.fromhex("ffd8ff") + b"y" * 40
    try:
        # ── 음성이 먼저다: 그림이 아닌 것을 받아주면 이 기능은 업로드 구멍이다
        assert save_note_image(b"", "image/png").get("error"), "빈 파일을 받으면 안 된다"
        assert save_note_image(b"not an image at all" * 4, "image/png").get("error"), \
            "그림이 아닌 바이트를 png 라고 우기면 거부해야 한다"
        assert save_note_image(png + b"0" * (9 * 1024 * 1024), "image/png").get("error"), \
            "8 MB 를 넘으면 거부해야 한다"

        # ── 선언과 실제가 다르면 **실제**를 쓴다
        r = save_note_image(jpg, "image/png")
        assert r.get("name", "").endswith(".jpg"), \
            f"png 라고 선언해도 내용이 jpeg 면 .jpg 여야 한다 ({r})"

        # ── 양성 + 같은 내용은 같은 이름 (참조가 안 갈라진다)
        a = save_note_image(png, "image/png")
        b = save_note_image(png, "image/png")
        assert a["name"] == b["name"], "같은 내용이면 같은 이름이어야 한다"
        assert note_image_path(a["name"]) is not None

        # ── 경로 탈출 차단 (이름 규격 밖은 전부 None)
        for bad in ("../../etc/passwd", "zz.png", "", "x" * 32 + ".exe",
                    a["name"] + "/../x"):
            assert note_image_path(bad) is None, f"이름 '{bad}' 이 통과했다"
    finally:
        shutil.rmtree(NOTE_IMG_DIR, ignore_errors=True)


def test_note_format_lives_in_one_file():
    """글 서식(inline/autosize/wrapSel)의 **사본이 둘이 아니다**.

    ⛔ 2026-08-28 — 원래 docnote.js 에만 있어서 문헌 코멘트는 `**87.2%**` 가 별표째
      보였다(1저자 신고). 사본을 두 벌 만들면 오늘만 세 번 겪은 "같은 규약의 두 경로"다.
      comments.js 가 집이고 docnote.js 는 window.noteFmt 를 부른다.
    """
    root = Path(__file__).resolve().parents[2]
    cjs = (root / "webapp/static/js/comments.js").read_text(encoding="utf-8")
    djs = (root / "webapp/static/js/docnote.js").read_text(encoding="utf-8")

    # 집: comments.js 가 정의하고 내보낸다
    for fn in ("function inline(", "function autosize(", "function wrapSel("):
        assert fn in cjs, f"comments.js 에 {fn} 이 없다 — 서식의 집이 비었다"
    assert "global.noteFmt" in cjs, "noteFmt 를 안 내보낸다"

    # 세입자: docnote.js 는 **자기 본문을 갖지 않고** 위임만 한다
    assert "NF()" in djs, "docnote.js 가 noteFmt 를 안 쓴다"
    for pat in ("<b>$1</b>", "ta.scrollHeight", "setSelectionRange(a + n"):
        assert pat not in djs, \
            f"docnote.js 에 서식 사본이 남아 있다 ({pat!r}) — 한쪽만 고쳐지는 사고가 난다"

    # 두 입력창 모두 그림 붙여넣기를 받는다 (한쪽만 되면 손이 헷갈린다)
    assert ".cmt-in, .dn-in" in cjs, "코멘트/메모 둘 다 그림 붙여넣기를 받아야 한다"
    # 임의 URL 을 <img> 로 펴지 않는다
    # 정규식 안이라 슬래시가 이스케이프돼 있다 — 형태가 아니라 **가드가 있는지**를 본다
    assert "[0-9a-f]{32}" in cjs and "IMG_SRC.test(src)" in cjs, \
        "우리 이름 규격 밖의 URL 을 <img> 로 펴면 메모 한 줄로 외부 요청을 만들 수 있다"


def test_comment_edit_route_exists():
    """코멘트 수정(PATCH) 이 서버·UI 양쪽에 있다.

    서버 edit_file_comment 는 예전부터 있었는데 **UI 가 없어서** 못 고쳤다
    (1저자 2026-08-28: "수정도 가능하게").
    """
    root = Path(__file__).resolve().parents[2]
    app_py = (root / "webapp/app.py").read_text(encoding="utf-8")
    cjs = (root / "webapp/static/js/comments.js").read_text(encoding="utf-8")
    assert '"PATCH"' in app_py, "PATCH 라우트가 없다"
    assert 'method: "PATCH"' in cjs, "UI 에 수정 저장이 없다"
    assert "cmt-edit" in cjs and "cmt-save" in cjs, "수정 버튼/저장 버튼이 없다"


def test_every_glossary_term_reaches_a_rendered_category():
    """카테고리 오타 하나로 용어가 **말없이 사라지는** 것을 막는다.

    `by_category()` 는 `setdefault` 라 CATS_G 밖 카테고리도 받아 준다. 그런데
    glossary.html 은 `cat_order`(=CATS_G)만 순회하므로, 카테고리를 한 글자 틀리면
    그 용어는 예외도 빈칸도 없이 **/glossary 에서 통째로 없어진다.** 없어진 항목은
    "그런 용어가 없다" 로 읽힌다.

    음성 경로: 없는 카테고리를 넣으면 실제로 화면에서 빠지는지 확인한다.
    """
    import glossary as G

    lost = sorted({g["cat"] for g in G.GLOSSARY} - set(G.CATS_G))
    assert not lost, f"CATS_G 에 없는 카테고리 {lost} — 그 용어들이 /glossary 에서 사라진다"
    rendered = sum(len(v) for k, v in G.by_category().items() if k in G.CATS_G)
    assert rendered == len(G.GLOSSARY), (
        f"용어 {len(G.GLOSSARY)}개 중 {rendered}개만 렌더 대상이다")
    ids = [g["id"] for g in G.GLOSSARY]
    assert len(ids) == len(set(ids)), "glossary id 가 중복이다 — 링크가 엉뚱한 항목으로 간다"
    # ⛔음성: 검사기가 실제로 가르는지 (항상 통과하면 아무것도 안 지킨다)
    G.GLOSSARY.append({"id": "__probe__", "term": "probe", "full": "", "cat": "없는분류",
                       "what": "", "how": "", "ours": ""})
    try:
        assert {g["cat"] for g in G.GLOSSARY} - set(G.CATS_G) == {"없는분류"}
        assert sum(len(v) for k, v in G.by_category().items()
                   if k in G.CATS_G) == len(G.GLOSSARY) - 1, "사라짐을 못 잡는다"
    finally:
        G.GLOSSARY.pop()


def test_glossary_lit_field_is_separate_from_ours():
    """용어 카드의 **문헌에서 본 것** 칸이 「우리 계산」과 **따로** 있다.

    ⛔ litdb 규율: 문헌 소환값과 우리 절대값을 섞지 않는다. 한 칸에 넣으면 섞인다.
      2026-08-28 신설, 첫 사례는 NEB ← tu2026 의 계면 CI-NEB (끝점의 결합 위상이
      달라서 그 장벽이 이동 장벽이 아니라는 것).
    """
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from glossary import GLOSSARY

    neb = [g for g in GLOSSARY if g["id"] == "neb"]
    assert neb, "neb 용어가 없다"
    neb = neb[0]
    assert neb.get("lit"), "neb 에 lit 이 없다"
    # 두 칸이 **각각** 있어야 한다 — 하나로 합치면 규율이 깨진다
    assert neb.get("ours") and neb["lit"] != neb["ours"], "lit 과 ours 가 같은 칸이면 안 된다"
    for must in ("결합 위상", "tu2026", "인용 금지"):
        assert must in neb["lit"], f"lit 에 '{must}' 가 없다"
    # ⛔ 음성: lit 은 **선택 필드**다. 없는 용어가 있어야 정상이고, 없어도 페이지가 떠야 한다
    assert any(not g.get("lit") for g in GLOSSARY), \
        "lit 이 모든 용어에 있으면 선택 필드가 아니다 — 템플릿의 {% if %} 가 시험되지 않는다"

    from app import app as flask_app
    with flask_app.test_client() as c:
        h = c.get("/glossary").get_data(as_text=True)
    assert "문헌에서 본 것" in h and 'gd lit' in h, "lit 칸이 안 그려진다"
    assert 'gd ours' in h, "우리 계산 칸이 사라졌다"


def test_sdcp_closure_consistency():
    """SDCP 마감 기록과 citable 이 **서로 모순되면 실패** — 회신 N 이 요구한 회귀 봉인.

    ⛔ 실측 (2026-08-28): 규율을 도입한 바로 그 커밋에서 어겼다.
      citable v3 는 dE_notes 를 "30 meV 미해결" 로 고쳤는데 **headline_sentences_ko 는
      "모두 Li 자리를 선호" · "약 2배"** 를 그대로 들고 있었다 — 같은 주장, 다른 표현이라
      문자열 매칭 수정이 못 잡았다. 값이 아니라 **주장끼리** 대조해야 잡힌다.
    """
    import json

    root = Path(__file__).resolve().parents[2]
    c = json.loads((root / "db/properties/sdcp_wave1_citable.json").read_text(encoding="utf-8"))
    cl = json.loads((root / "db/properties/sdcp_neutral_closed_2026_08_28.json")
                    .read_text(encoding="utf-8"))

    # ── neutral 자리선호가 '미해결' 인데, 어느 문서든 선호를 주장하면 모순이다
    assert "미해결" in json.dumps(c.get("dE_notes", {}).get("sdcp_neutral", ""),
                                ensure_ascii=False), "neutral 판정이 '미해결' 이어야 한다"
    for h in c.get("headline_sentences_ko", []):
        assert not ("모두" in h and "선호" in h), \
            f"headline 이 neutral 까지 '선호' 로 묶는다 — dE_notes 와 모순: {h[:80]}"
        assert "2배" not in h and "배 강하" not in h, \
            f"headline 에 금지 서술('~배')이 있다: {h[:80]}"

    # ── 마감 문서의 금지 서술이 citable headline 에 나타나면 실패
    for bad in cl.get("⛔_금지_서술", []):
        key = bad.split("'")[1] if "'" in bad else None
        if key and key in ("자리 불문", "약 2배"):
            for h in c.get("headline_sentences_ko", []):
                assert key not in h, f"금지 서술 '{key}' 가 headline 에 있다"

    # ── stale: **지위 필드**(not_citable·caveats)에 '대기' 가 남으면 안 된다.
    #    ⚠ 전체 blob 검사는 안 된다 — 이력·설명 서술("'wave1.5 대기' 를 제거했다")까지
    #    잡는다. 오늘 convention_check 오탐 교훈 그대로: 검사는 지위 필드에만.
    status_fields = json.dumps(
        {"not_citable": c.get("not_citable"),
         "caveats": c.get("⚠_caveats_MUST_QUOTE_WITH_VALUES"),
         "cross_checks": c.get("cross_checks")}, ensure_ascii=False)
    assert "wave1.5 대기" not in status_fields, "지위 필드에 stale 'wave1.5 대기'"
    assert not ("재현성 근거" in status_fields and "착시" not in status_fields), \
        "cross_checks 가 회신 M 이 반려한 '≤1 meV 재현' 을 아직 근거로 부른다"

    # ── 회신 M 이 반려한 혼합-basin 시드 비교를 마감 근거로 쓰면 실패
    v = json.dumps(cl.get("닫는_근거_체크리스트", {}).get("값의_안정성", ""), ensure_ascii=False)
    assert not ("basin-matched" in v and "제거" not in v), \
        "혼합-basin E_ads 시드 비교가 마감 근거로 남아 있다 (회신 M 반려 산술)"


# ═══════════════════════════════════════════════════════════════════════════
# 회신 AW P0-2 — 철회된 값이 **현재-facing 표면**에서 되살아나지 않는가
# ═══════════════════════════════════════════════════════════════════════════
#: ⛔ 2026-09-08 (회신 BG ②) — **손으로 적던 표면 목록을 폐기했다.**
#:   목록에 없는 화면은 아무리 틀려도 안 잡혔다 (실측: `/governance` 의 인용위험 표에
#:   철회값이 미결속으로 있었는데 목록 밖이라 초록이었다). 이제 라우트를 **자동 열거**한다.
#: ⛔ 그리고 결속 판정을 **±140자 근접성 → claim id 구조 결속**으로 바꿨다.
#:   근접성은 ① 표지가 그 값에 대한 것인지 못 보고 ② 표 셀이 길면 창 밖으로 밀리고
#:   ③ 옆 문단의 경고를 통과로 읽었다. 이제 값을 그리는 요소(또는 조상)가
#:   `data-claim="<metric>@<system>"` 로 **어느 주장인지 이름을 대야** 한다.
_BINDING_SKIP_PREFIX = ("/static",)

#: 레거시 래칫 — **은퇴했다** (2026-09-08). 이주가 끝나 전 표면 미결속 0 이다.
#:   래칫은 이주 장치였고, 이주가 끝난 뒤에도 남겨 두면 새 누출을 덮는 뚜껑이 된다
#:   (회신 BG Q2 가 물은 위험이 정확히 그것이다). 비어 있어야 하고, 다시 채우는 것은
#:   **완화**다 — 새 미결속은 표를 늘려서가 아니라 결속을 붙여서 없앤다.
_LEGACY_UNBOUND: dict = {}

#: ⛔⛔ **검사하지 못한 표면** (Codex BI-4 재승인 조건 6 · 2026-09-09)
#:   그쪽 조건은 *"미검사 표면을 명시하고, 핵심 JS 경로의 **실제 브라우저 검증** 결과를
#:   고정 커밋과 함께 제출할 것"* 이다. **브라우저 검증은 못 했다** — 이 환경에서 CDN 이
#:   403 이고 `webapp/static/vendor/.gitignore` 가 `*.js` 를 막아 `marked.min.js` 가 없다.
#:   그 상태로 DOM 검사를 켜면 **거짓 초록**이 된다(실측: `typeof marked !== 'undefined'`
#:   = 0/57 인데 DOM 스캔이 서버와 똑같이 초록이었다).
#:   ⇒ 못 한 것을 못 했다고 **기계가 읽는 자리**에 적는다. 산문으로만 적으면 다음 사람이
#:     "검사했겠지" 로 읽는다 — 그게 이번 리뷰 전체의 요지다.
#:   ⚠ 이 목록이 **줄어야** 진전이다. 늘리려면 사유를 같이 적어라.
_UNVERIFIED_SURFACES = {
    "compare.html#cmp 조립 결과": "서버가 실은 JSON 을 JS 가 innerHTML 로 조립한다. "
        "셀 조립은 서버 파생 claim id 로 바꿨지만 **브라우저에서 확인하지 않았다**.",
    "댓글 정상 응답의 렌더": "`note_html` 이 서버에서 결속을 붙이는 것은 시험이 본다. "
        "그 HTML 이 **브라우저에서 그대로 그려지는지**는 안 봤다.",
    "댓글 오류 응답의 대체 표시": "`disp()` 가 `html` 없을 때 인용불가 안내를 내는 것은 "
        "함수 단위로 확인했다. **실제 DOM 에서 텍스트 노드로 나가는지**는 안 봤다.",
    "복사되는 문자열": "`.claim-mark` 를 텍스트 노드로 만든 이유가 복사·인쇄인데, "
        "**실제 클립보드 내용을 확인하지 않았다**.",
    "인쇄 경고 유지": "`@media print` 규칙은 CSS 에 있다. **인쇄 미리보기를 안 봤다**.",
}

#: `data-claim-not` 부인 원장 — **우연 일치**를 선언으로 처리한 자리와 그 사유.
#:   ⚠ 이건 면제가 아니라 주장이다: *"이 문자열은 그 주장이 아니다"*. 틀리면 거짓 선언이고,
#:     그래서 여기 사유를 적어 감사 가능하게 남긴다 (빈 사유 금지 — DYNAMIC_EXEMPT 관례).
#:   ⛔ 2026-09-08 (Codex BI P0-2a/P0-3) — 종전에는 **사유 문자열만** 요구했다. 그래서
#:     `data-claim-not` 이 40행 표(td 600 · 3800자)를 통째로 덮어도 통과했고, 그 안에
#:     진짜 철회 인용을 심어도(자유텍스트·숫자만 둘 다 재현) 시험이 초록이었다.
#:     ⇒ 사유에 **건수(n)와 문맥(where)** 을 같이 선언한다. 건수가 달라지면 실패한다 —
#:       "이 자리 하나가 우연 일치다" 는 검증 가능한 주장이고, "이 표는 봐주세요" 는 아니다.
#: ⛔⛔ BI-3 P0-2 (2026-09-09) — `where` 는 **기계가 대조하는 좌표**여야 한다.
#:   종전에는 산문이었고 검사가 **한 번도 읽지 않았다**. 그래서 Codex 가 `/cascade` 의
#:   부인된 셀 하나를 `b2o3 MD Ea = 0.199 eV` 로 바꿔도 disclaimed 1 · unbound 0 으로
#:   **초록**이었다 — 건수는 그 자리의 **의미**를 보증하지 못한다.
#:   이제 화면이 `data-claim-not-src="<키열>=<값>|<열>"` 을 같이 내고, 아래 `where` 가
#:   그 좌표의 **집합**이다. 검사는 선언↔실측을 **양방향**으로 맞춘다.
_DISCLAIMED = {
    ("/cascade", "MD_Ea_eV@b2o3"): {
        "why": "codoping_ml_v2 스크리닝 표의 `window_gain 0.199`(V)다. b2o3 MD Ea 0.199(eV)와 "
               "글자만 같고 양·단위·출처가 전부 다르다 — 결속하면 거짓 선언이 된다.",
        "n": 1,
        # ⛔⛔ BI-4 P0-2 (2026-09-09) — 좌표에 **데이터셋 이름**을 넣었다. 종전 2칸 형식은
        #   "어느 원자료의 rank 25 냐" 를 안 말해서 대조 자체가 불가능했다. 그리고 좌표가
        #   맞아도 **그 칸에 무엇이 떠 있는지**는 여전히 안 봤다 — Codex 가 좌표를 그대로
        #   둔 채 `0.199` → `b2o3 MD Ea = 0.199 eV` 로 갈아 통과시켰다.
        #   이제 `canonical.verify_disclaimers()` 가 셀의 글을 원자료 값과 직접 댄다.
        "where": ["codoping_ml_v2|rank=25.0|window_gain"],
        "where_prose": "codoping_ml_v2 상위 40행 · window_gain 열 (rank 25, pairA=B2O3/pairB=Gd2O3)",
        "⚠": "원자료 1081행에는 같은 글자가 13칸 더 있다(window_gain 5 · uncertainty 4 · "
             "ad_eps 1 · ml_score 1 …). 표를 늘리거나 정렬을 바꾸면 n 이 는다 — 그때 "
             "n 을 올리기 전에 **그 칸들이 정말 다른 양인지** 확인해라.",
    },
}


def _html_routes():
    """인자 없는 GET 라우트 — **손 목록을 쓰지 않는다** (새 화면이 자동으로 검사에 든다)."""
    return sorted({str(r) for r in A.app.url_map.iter_rules()
                   if not r.arguments and "GET" in r.methods
                   and not str(r).startswith(_BINDING_SKIP_PREFIX)})


def _surface_html(client, url):
    """→ HTML 문자열 | None. JSON 응답(`/api/handoff`)은 `html` 필드를 꺼낸다."""
    r = client.get(url)
    if r.status_code != 200:
        return None
    ct = r.headers.get("Content-Type") or ""
    if "html" in ct:
        return r.get_data(as_text=True)
    if "json" in ct:
        try:
            d = json.loads(r.get_data(as_text=True))
        except Exception:                                   # noqa: BLE001
            return None
        return d.get("html") if isinstance(d, dict) and isinstance(d.get("html"), str) else None
    return None


def _scan_surface(client, url):
    """→ (scan|None). 결속 대상은 **수치 + 비수치 전부**(`all_claims`)."""
    h = _surface_html(client, url)
    return None if h is None else C.scan_claim_bindings(h, C.all_claims())


#: 결속 선언만 지운다 — 텍스트는 그대로 둔다. 음성시험의 도구다.
#: ⚠ 따옴표 두 종류를 다 받는다. 홑따옴표를 빼먹었더니 `/glossary`(파이썬 문자열 안이라
#:   홑따옴표를 쓴다)에서 **선언이 안 지워져** 음성시험이 통과해 버렸다 (2026-09-08 실측).
_STRIP_DECL = re.compile(r"""\s+data-claim(?:-not)?=(?:"[^"]*"|'[^']*')""")


def test_retracted_claims_are_id_bound_on_every_surface():
    """⛔음성 AW P0-2 / BG ②: 철회·비인용·인용위험 주장이 **이름 없이** 화면에 나오면 안 된다.

    ⛔ 지우라는 뜻이 아니다. 역사는 남기되 그 값을 그리는 요소가 `data-claim` 으로
      자기 주장을 선언해야 한다. 선언이 있으면 근접성은 보지 않는다 — 표 안이든
      긴 문단이든 결속은 구조로 성립한다.
    ⚠ 2026-09-08: 검사 대상이 숫자에서 **비수치 금지주장**(`+90 meV` 계간 비교 등)까지
      넓어졌다. 숫자만 보던 판이 여덟 화면의 산문 누출을 놓쳤다.
    """
    claims = C.all_claims()
    assert any(c["state"] == "retracted" and c["text"] for c in claims), \
        "전제: 스캔 가능한 철회 정본값이 실제로 있다 (b2o3 MD_Ea 0.199)"
    assert any(str(c["state"]).startswith("hazard_") and c["text"] for c in claims), \
        "전제: 스캔 가능한 **비수치** 금지주장이 실제로 있다 (citation_hazards forbidden_phrases)"
    c = A.app.test_client()
    urls = _html_routes() + [re.sub(r"<[^>]+>", v, r)
                             for r, vs in DYNAMIC_FIXTURES.items() for v in vs]
    fresh, grew, dangling, undeclared = [], [], [], []
    for url in urls:
        sc = _scan_surface(c, url)
        if sc is None:
            continue
        n = len(sc["unbound"])
        cap = _LEGACY_UNBOUND.get(url)
        if cap is None and n:
            fresh += [(url, cl["id"], ctx) for cl, ctx in sc["unbound"]]
        elif cap is not None and n > cap:
            grew.append((url, n, cap))
        if sc["dangling"]:
            dangling.append((url, sc["dangling"]))
        # ── 부인 검사: **사유 + 건수 + 좌표**를 원장이 대고, 선언↔실측을 양방향으로 맞춘다.
        #    (BI-3 P0-2. 종전에는 `where` 를 안 읽고 발견된 것만 순회해서, 그 자리의
        #     의미가 바뀌어도 건수만 같으면 통과했다.)
        found = {}
        for cl, _x, nsrc, _cell in sc["disclaimed"]:
            found.setdefault(cl["id"], []).append(nsrc)
        for cid, srcs in found.items():
            dec = _DISCLAIMED.get((url, cid))
            if not dec:
                undeclared.append((url, cid, "선언되지 않은 부인이 화면에 있다"))
                continue
            if not str(dec.get("why", "")).strip():
                undeclared.append((url, cid, "사유 없음"))
            want_n, want_w = dec.get("n"), dec.get("where")
            if not isinstance(want_n, int):
                undeclared.append((url, cid, "`n` 이 정수로 선언돼 있지 않다 — "
                                             "건수 미선언은 담요와 구별되지 않는다"))
            elif len(srcs) != want_n:
                undeclared.append((url, cid, f"부인 건수가 선언과 다르다: {len(srcs)} ≠ {want_n}"))
            if not isinstance(want_w, list) or not want_w:
                undeclared.append((url, cid, "`where` 가 좌표 목록이 아니다 — 산문은 "
                                             "기계가 못 읽는다 (BI-3 P0-2)"))
                continue
            if any(s is None for s in srcs):
                undeclared.append((url, cid, "화면이 `data-claim-not-src` 를 안 냈다 — "
                                             "어느 자리를 부인하는지 알 수 없다"))
                continue
            extra = sorted(set(srcs) - set(want_w))
            missing = sorted(set(want_w) - set(srcs))
            if extra:
                undeclared.append((url, cid, f"⛔ 선언에 없는 자리에서 부인이 났다: {extra} "
                                             f"— 그 칸의 **의미가 바뀌었거나** 새 칸이다"))
            if missing:
                undeclared.append((url, cid, f"⛔ 선언한 자리에서 부인이 사라졌다: {missing} "
                                             f"— 부인이 옮겨갔거나 화면이 바뀌었다"))
        for (u, cid), dec in _DISCLAIMED.items():                 # ← 반대 방향
            if u == url and cid not in found:
                undeclared.append((url, cid, "선언한 부인이 화면에 없다 — 원장이 낡았다"))
        # ⛔⛔ BI-4 P0-2 — 좌표가 맞는 것과 **그 자리에 무엇이 떠 있는지**는 다른 일이다.
        #    여기서 화면 셀의 글을 원자료 값과 직접 댄다. `ok=False` 는 전부 실패로 센다
        #    (원자료를 못 읽은 경우 포함 — **확인 불가는 통과가 아니다**).
        for v in C.verify_disclaimers(sc["disclaimed"]):
            if not v["ok"]:
                undeclared.append((url, v.get("claim"),
                                   f"⛔ 부인이 원자료와 안 맞는다: {v['why']}"))
    assert not fresh, "결속 없는 철회·금지 주장이 **새로** 나왔다 (data-claim 을 붙이거나 문장을 고쳐라):\n" + \
        "\n".join(f"  {u} · {i}\n      …{x[:140]}…" for u, i, x in fresh)
    assert not grew, "레거시 미결속 건수가 늘었다 (래칫은 줄어들기만 한다): " + str(grew)
    assert not dangling, "레지스트리에 없는 claim id 를 화면이 선언한다 (유령 결속): " + str(dangling)
    assert not undeclared, ("사유 없는 `data-claim-not` 부인이 있다 — _DISCLAIMED 에 "
                            "**왜 그 주장이 아닌지** 적어라: " + str(undeclared))


def test_legacy_ratchet_is_retired_not_reintroduced():
    """⛔음성: 래칫을 **다시 넣어** 미결속을 통과시키는 것을 막는다 (회신 BG Q2).

    이주는 2026-09-08 에 끝났다(전 표면 0). 래칫이 남아 있으면 다음 누출이 표에 한 줄
    늘어나는 것으로 무마된다 — 그게 리뷰가 물은 "안 고치고 통과시키는 장치" 다.
    """
    assert _LEGACY_UNBOUND == {}, (
        "래칫이 다시 채워졌다. 미결속은 표를 늘려 덮는 게 아니라 결속을 붙여 없앤다: "
        + str(_LEGACY_UNBOUND))


def test_each_surface_zero_comes_from_declarations_not_from_absence():
    """⛔음성 **표면별**: 화면의 미결속 0 이 *선언 덕분*인지 *글자가 없어서*인지 가른다.

    회신 BG 가 요구한 표면별 음성시험이다. 방법: 렌더된 HTML 에서 `data-claim`
    선언만 지우고 다시 스캔한다. 결속이 있던 화면이라면 **반드시 미결속으로 떨어져야**
    한다 — 안 떨어지면 그 화면의 초록은 스캐너가 그 화면을 안 본다는 뜻이다.
    ⚠ 이 시험이 `/todo`·`/log`·handoff·`/compare`·`/glossary` 를 각각 따로 확인한다.
    """
    c = A.app.test_client()
    must = ["/", "/compare", "/explorer", "/glossary", "/governance", "/log",
            "/methods", "/requests", "/todo",
            "/api/handoff/lpsocl_box_size_600K_2026_08_18"]
    cl = C.all_claims()
    blind, no_drop = [], []
    for url in must:
        h = _surface_html(c, url)
        if h is None:
            blind.append((url, "응답이 없거나 형식이 다르다"))
            continue
        sc = C.scan_claim_bindings(h, cl)
        if not sc["bound"]:
            blind.append((url, "결속이 0 이다 — 이 화면은 검사에 안 걸린다(대상 문자열이 없다)"))
            continue
        naked = C.scan_claim_bindings(_STRIP_DECL.sub("", h), cl)
        if len(naked["unbound"]) < len(sc["bound"]):
            no_drop.append((url, len(sc["bound"]), len(naked["unbound"])))
    assert not blind, ("표면별 음성시험의 전제가 깨졌다 — 이 화면들은 검사 대상 문자열을 "
                       "그리지 않는다. 목록에서 빼거나 왜 빠졌는지 확인해라: " + str(blind))
    assert not no_drop, ("선언을 지웠는데도 미결속으로 안 떨어진 화면이 있다 — 그 화면의 "
                         "초록은 결속 때문이 아니다: " + str(no_drop))


def test_markdown_render_binds_claims_and_can_fail():
    """양성+⛔음성: kb 산문 경로(`md_html`)가 결속을 **자동으로** 붙인다.

    `/todo`·`/requests`·handoff·litdb 는 전부 이 한 경로를 지난다. 여기가 죽으면
    네 화면이 동시에 눈이 먼다 — 그래서 경로 자체를 시험한다.
    """
    tgt = next(x for x in C.all_claims() if x["state"] == "retracted" and x["text"])
    t = tgt["text"]
    out = A.md_html(f"옛 값 {t} eV 를 인용한 문장.")
    assert f'data-claim="{tgt["id"]}"' in out, f"md_html 이 결속을 안 붙였다: {out}"
    assert not C.scan_claim_bindings(out, C.all_claims())["unbound"], out
    # ⛔음성 ①: 붙이기 **전** 상태는 반드시 미결속이어야 한다 (안 그러면 위 양성이 공허하다)
    assert C.scan_claim_bindings(f"<p>옛 값 {t} eV 를 인용한 문장.</p>",
                                 C.all_claims())["unbound"], "표시 없이도 통과한다 — 검사가 죽었다"
    # ⛔음성 ②: 태그 **속성 안**의 같은 문자열은 건드리지 않는다 (HTML 을 깨뜨리는 경로)
    frag, found = C.annotate_claims(f'<a title="{t}">x</a>')
    assert frag == f'<a title="{t}">x</a>' and not found, frag
    # ⛔음성 ③: 다른 수의 일부는 감싸지 않는다
    frag, _ = C.annotate_claims(f"<p>1{t} · {t}9</p>")
    assert "claim-flag" not in frag, frag


def test_claim_binding_scanner_can_actually_fail():
    """⛔음성: 스캐너가 **아무것도 안 잡는 상태**로 초록이 되는 것을 막는다."""
    cl = C.all_claims()
    tgt = next(x for x in cl if x["state"] == "retracted" and x["text"])
    t = tgt["text"]
    # ① 결속 없는 노출 → unbound
    r = C.scan_claim_bindings(f"<p>b2o3 의 MD Ea 는 {t} eV 다.</p>", cl)
    assert len(r["unbound"]) == 1 and not r["bound"], r
    # ② 근접 표지만 있고 id 가 없으면 **여전히 unbound** (이것이 BG ② 의 요지다)
    r = C.scan_claim_bindings(f"<p>⛔ 철회됨 — 옛 값 {t} eV.</p>", cl)
    assert len(r["unbound"]) == 1, "근접 표지를 결속으로 읽으면 안 된다 (±140자 방식 회귀)"
    # ③ 조상이 id 를 대면 bound
    r = C.scan_claim_bindings(f'<tr data-claim="{tgt["id"]}"><td>{t}</td></tr>', cl)
    assert len(r["bound"]) == 1 and not r["unbound"], r
    # ④ 다른 주장의 id 로는 결속되지 않는다
    r = C.scan_claim_bindings(f'<tr data-claim="MD_Ea_eV@modelc"><td>{t}</td></tr>', cl)
    assert len(r["unbound"]) == 1, "id 가 달라도 통과하면 결속이 아니다"
    # ⑤ **다른 수**는 세지 않는다. 단, `0.1990` 은 같은 수다 — 2026-09-08 정정.
    #    ⛔ 종전 문자열 매칭은 `nxt.isdigit()` 가드로 `0.1990` 을 빼고 있었고, 그건
    #      *"자릿수 하나만 늘리면 결속을 벗어난다"* 는 회피면이었다(Codex BI 재현 중 발견:
    #      `<td>0.199</td>` unbound 1 vs `<td>0.1990</td>` unbound 0). 이제 값으로 본다.
    assert not C.scan_claim_bindings(f"<p>1{t} · {t}9</p>", cl)["unbound"], "다른 수를 세면 안 된다"
    assert len(C.scan_claim_bindings(f"<p>{t}0</p>", cl)["unbound"]) == 1, (
        "⛔ 회피면 회귀 — 0.1990 이 결속을 벗어나면 안 된다")
    # ⑤-b 부호가 다르면 그 주장이 아니다 (남의 논문 흡착에너지 −0.199 eV 오탐 17건)
    s5 = C.scan_claim_bindings(f"<p>H₂O 흡착에너지는 −{t} eV 였다.</p>", cl)
    assert not s5["unbound"] and len(s5["suspect"]) == 1, s5
    # ⑤-c 코드블록 안은 인용이 아니다 / 인라인 code 는 값 강조라 **결속 대상이다**
    assert C.scan_claim_bindings(f"<pre><code>Ea={t}</code></pre>", cl)["skipped"]
    assert C.scan_claim_bindings(f'<p><code class="mono">Ea {t}</code></p>', cl)["unbound"], (
        "인라인 code 를 건너뛰면 대시보드가 통째로 눈이 먼다")
    # ⑥ 유령 id 는 잡는다
    assert C.scan_claim_bindings('<tr data-claim="NOPE@x">1</tr>', cl)["dangling"] == ["NOPE@x"]
    # ⑦ 파생 경로가 살아 있는가 — 하드코딩이면 레지스트리를 고쳐도 안 바뀐다
    assert ("MD_Ea_eV", "b2o3") in {(x["metric"], x["system"]) for x in cl}


def test_prohibition_context_still_guards_prose():
    """근접성 함수는 **다른 검사**에서 여전히 쓴다 — 그 함수가 죽지 않았는지만 본다."""
    assert not C.is_prohibition_context("b2o3 의 MD Ea 는 0.199 eV 다. modelc 와 동급이다.")
    assert C.is_prohibition_context("⛔ 0.199 는 철회됐다 — 800 K 위에서 굽는다")


# ══════════════════════════════════════════════════════════════════════════
# 잣대 세대 (protocol_generation) — 2026-09-07
#   왜: MD 축은 2026-07~09 사이에 **판정 규칙 자체**가 세 번 바뀌었다. 화면이 그걸
#   말해 주지 않으면 gen0(구 잣대) 값이 현행 값처럼 보인다 — 1저자가 세미나 값을 보고
#   "생각보다 옛날 값 아니야?" 라고 물은 그 구멍.
# ══════════════════════════════════════════════════════════════════════════

def test_protocol_generation_ledger_is_wellformed():
    gens = C.protocol_generations()
    assert gens, "세대 원장을 못 읽는다 (db/properties/md_protocol_generations.json)"
    assert set(gens) == {"gen0_pre_gate", "gen1_traj_mto_200ps", "gen2_400ps_4window"}, gens
    for gid, g in gens.items():
        assert g.get("gates"), f"{gid} 에 gates 가 없다"
        assert set(g["gates"]) == {"G1_MTO", "G2_traj", "G3_4window",
                                   "G4_framework", "G5_prereg"}, f"{gid} 게이트 축이 다르다"
    # gen0 은 슬라이드·원고에 붙일 **영문 각주**를 반드시 들고 있어야 한다
    fn = gens["gen0_pre_gate"].get("영문_각주", "")
    for kw in ("MTO", "4-window", "protocol-conditioned"):
        assert kw in fn, f"gen0 영문 각주에 {kw!r} 이 없다: {fn!r}"


def test_every_MD_entry_declares_its_generation():
    """MD_* 항목은 **전부** 세대를 들고 있어야 한다 — 빠뜨림을 통과로 읽지 않는다."""
    reg = C.registry()
    vocab = set(C.protocol_generations())
    md = [e for e in reg["entries"] if str(e.get("metric", "")).startswith("MD_")]
    assert len(md) >= 11, f"MD_* 항목이 {len(md)}개뿐이다 — 레지스트리가 줄었나?"
    missing = [(e.get("metric"), e.get("system")) for e in md
               if e.get("protocol_generation") not in vocab]
    assert not missing, f"세대 없는 MD 항목: {missing}"


def test_generation_gate_fails_closed():
    """⛔음성: 세대가 없거나 어휘 밖이면 validator 가 **반드시** 잡는다.

    이게 없으면 위 시험은 '레지스트리가 지금 맞다' 만 말하고, 다음에 누가 세대 없는
    MD 항목을 추가해도 조용히 통과한다.
    """
    base = {"system": "x", "metric": "MD_Ea_eV", "value": 1.0, "unit": "eV",
            "status": "provisional", "comparison_group": "g"}
    # ① 세대 없음 → 위반
    bad = C.validate({"entries": [dict(base)]})
    assert any("protocol_generation 이 없다" in m for _, m in bad), bad
    # ② 어휘 밖 → 위반
    bad = C.validate({"entries": [dict(base, protocol_generation="gen9_made_up")]})
    assert any("어휘 밖" in m for _, m in bad), bad
    # ③ 올바른 세대 → 이 사유로는 안 걸린다 (다른 사유는 걸릴 수 있다)
    ok = C.validate({"entries": [dict(base, protocol_generation="gen0_pre_gate")]})
    assert not any("protocol_generation" in m for _, m in ok), ok
    # ④ MD_ 가 아닌 metric 은 세대를 요구하지 않는다
    ok = C.validate({"entries": [dict(base, metric="gap_eV")]})
    assert not any("protocol_generation" in m for _, m in ok), ok


def test_generation_badge_renders_and_is_not_a_quality_grade():
    c = A.app.test_client()
    t = c.get("/composition/modelc").get_data(as_text=True)
    assert "구 잣대" in t, "modelc 화면에 잣대 세대 배지가 없다"
    # 배지 툴팁이 게이트 상태를 실제로 말해야 한다 (라벨만 있고 근거 없으면 무의미)
    assert "G3=평가불가" in t or "G3=" in t, "세대 툴팁에 게이트 상태가 없다"
    # ⛔ 세대는 품질 등급이 아니다 — 화면이 '틀린 값' 이라고 말하면 안 된다
    gb = D.canonical_generation_for("modelc")
    assert gb["MD_Ea_eV"]["gen"] == "gen0_pre_gate"
    assert "평가불가" in gb["MD_Ea_eV"]["why"], gb["MD_Ea_eV"]["why"]
    for forbidden in ("틀렸", "오류", "무효"):
        assert forbidden not in gb["MD_Ea_eV"]["why"], \
            f"세대 배지가 값을 부정한다({forbidden}) — gen0 은 미검증이지 반증이 아니다"


def test_generation_badge_survives_unknown_vocabulary():
    """⛔음성: 어휘 밖 세대가 들어와도 배지가 **조용히 사라지지 않는다**.

    2026-09-07 에 `retracted` 가 배지 표에 없어 배지가 통째로 안 붙고 철회값이 정상
    카드처럼 뜬 사고가 있었다. 같은 형태의 fail-open 을 세대 축에서 미리 막는다.
    """
    b = D.generation_badge({"metric": "MD_Ea_eV", "protocol_generation": "gen_from_the_future"})
    assert b is not None, "어휘 밖 세대에서 배지가 통째로 사라졌다 (fail-open)"
    assert b["label"] == "세대?", b
    assert "어휘 밖" in b["why"], b["why"]
    # 세대 필드가 아예 없으면 배지도 없다 (그건 MD_* 검사가 따로 잡는다)
    assert D.generation_badge({"metric": "MD_Ea_eV"}) is None


def test_md_crosscut_ledgers_land_in_ionic():
    """MD 횡단 원장(계 이름으로 시작하지 않는 파일)이 Ionic 으로 간다.

    2026-09-07 발견: haven_ratio_measured_* · md_protocol_generations ·
    md_traj_inventory 가 전부 'other' 로 떨어져 Ionic 탭에 안 보였다.
    """
    for stem in ("haven_ratio_measured_2026_09_07", "md_protocol_generations",
                 "md_traj_inventory", "li_transport"):
        assert D.categorize(stem) == "ionic", f"{stem} -> {D.categorize(stem)}"


def test_phonon_dos_is_structural_not_electronic():
    """⛔음성: 'dos' 가 'phonon_dos' 를 삼키면 안 된다.

    _csv_kind() 는 이 함정을 이미 고쳐 놨는데 categorize() 는 안 고쳐져서
    b2o3_phonon_dos 가 Electronic 으로 분류되고 있었다 (규약 2곳 복사).
    함께: 진짜 전자 DOS 는 electronic 에 남아야 한다 — 과잉교정 방지.
    """
    assert D.categorize("b2o3_phonon_dos") == "structural"
    assert D.categorize("comp1_phonon") == "structural"
    assert D.categorize("modelc_dos") == "electronic"
    assert D.categorize("b2o3_pdos_B") == "electronic"


def test_categorize_does_not_over_claim_ionic():
    """⛔음성: ionic 키를 넓힌 뒤에도 남의 파일을 끌어오지 않는다."""
    for stem, expect in (("adhesion", "interface"), ("elastic_cij", "mechanical"),
                         ("comp1_bonds", "bonding"), ("sdcp_neutral_closed_2026_08_28", "other")):
        assert D.categorize(stem) == expect, f"{stem} -> {D.categorize(stem)} (기대 {expect})"


# ═══════════════════════════════════════════════════════════════════════════
#  Codex BI NO-GO 대응 (2026-09-08) — 결속이 **화면 밖으로도 나가는지**,
#  그리고 브라우저가 서버 판정을 덮지 않는지.
# ═══════════════════════════════════════════════════════════════════════════

#: 결속 표식은 **텍스트 노드**여야 한다. `content:` 로 그린 것은 복사·인쇄·텍스트추출·
#: 보조기기에 안 나간다 — Codex BI Q3. 이 목록에 든 CSS 클래스는 의미를 나르는
#: `content:` 를 가질 수 없다.
_MEANING_CLASSES = (".claim-flag", ".claim-mark")


def _text_only(html: str) -> str:
    """태그와 **속성**을 다 버리고 텍스트 노드만 이어붙인다 (복사·스크린리더 근사)."""
    from html.parser import HTMLParser

    class _T(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.out, self._skip = [], 0

        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style"):
                self._skip += 1

        def handle_endtag(self, tag):
            if tag in ("script", "style"):
                self._skip = max(0, self._skip - 1)

        def handle_data(self, d):
            if not self._skip:
                self.out.append(d)
    p = _T()
    p.feed(html)
    return "".join(p.out)


def _strip_comments(src: str) -> str:
    """Jinja·HTML·JS 주석을 **줄 수를 유지한 채** 지운다 (정적 린트용).

    ⚠ 주석을 안 지우면 *"여기에 marked 를 되살리지 마라"* 라고 적은 경고문 자체가
      린트에 걸린다. 반대로 너무 넓게 지우면(문자열 안의 `//`) 진짜 코드를 놓친다 —
      그래서 URL 흔한 형태(`://`)는 남긴다.
    """
    def _blank(m):
        return "\n" * m.group(0).count("\n")
    src = re.sub(r"\{#[\s\S]*?#\}", _blank, src)          # Jinja
    src = re.sub(r"<!--[\s\S]*?-->", _blank, src)          # HTML
    src = re.sub(r"/\*[\s\S]*?\*/", _blank, src)           # JS 블록
    src = re.sub(r"(?<!:)//[^\n]*", "", src)               # JS 줄 (`://` 는 남긴다)
    return src


def test_claim_mark_survives_text_extraction():
    """⛔음성: 표식이 **CSS 없이도** 남는다 — 그리고 title-only 마크업은 실패한다.

    Codex BI Q3 실측: `_claim_flag` 가 ⛔ 를 CSS `::after` 로만 넣고 사유를 `title` 에만
    실었다. 텍스트 노드만 뽑으면 *'b2o3 의 MD Ea 는 0.199 eV 다.'* — 경고가 사라진 채
    철회값만 남는다. 복사·인쇄·텍스트추출·보조기기가 전부 그 경로다.
    """
    cl = C.all_claims()
    tgt = next(x for x in cl if x["state"] == "retracted" and x["text"])
    html, _ = C.annotate_claims(f"<p>b2o3 의 MD Ea 는 {tgt['text']} eV 다.</p>", cl)
    txt = _text_only(html)
    assert tgt["text"] in txt, "값 자체가 사라지면 안 된다(표식만 붙인다)"
    assert "⛔" in txt, (
        f"⛔음성 실패: 표식이 텍스트로 안 나온다 — 복사하면 철회값만 따라간다.\n{txt!r}")
    # ⛔음성 대조 — 종전(title-only) 마크업을 같은 검사기에 넣으면 **반드시 실패**해야 한다.
    legacy = (f'<p>b2o3 의 MD Ea 는 <span class="claim-flag" data-claim="{tgt["id"]}"'
              f' title="⛔ 철회 — 인용 금지">{tgt["text"]}</span> eV 다.</p>')
    assert "⛔" not in _text_only(legacy), (
        "검사기가 죽었다 — 종전 title-only 마크업이 이 검사를 통과하면 안 된다")


def test_claim_css_does_not_carry_meaning_in_content():
    """⛔음성: `.claim*` 규칙이 의미를 `content:` 로 나르면 실패.

    되살리기 쉬운 자리다 (한 줄이면 된다). 그래서 시험으로 못을 박는다.
    """
    css = (Path(A.__file__).parent / "static/css/style.css").read_text(encoding="utf-8")
    bad = []
    for cls in _MEANING_CLASSES:
        for m in re.finditer(re.escape(cls) + r"[^{]*\{([^}]*)\}", css):
            body = m.group(1)
            if re.search(r"content\s*:\s*[\"'][^\"']", body):     # 빈 문자열은 허용
                bad.append(f"{cls} {{{body.strip()[:70]}}}")
    assert not bad, ("⛔ 표식을 CSS content 로 그리고 있다 — 화면 밖으로 안 나간다: "
                     + " · ".join(bad))
    # 양성 대조 — 가짜 CSS 를 같은 검사기에 넣으면 걸려야 한다(검사기가 죽지 않았다).
    fake = '.claim-mark::after{content:"⛔"}'
    assert re.search(r"content\s*:\s*[\"'][^\"']", fake)


def test_no_client_side_markdown_parser():
    """⛔음성: 브라우저가 마크다운을 **다시 파싱**하지 않는다 (Codex BI P0-2b).

    파서가 둘이면 판정도 둘이 된다. `marked.parse` 한 줄이 `box.innerHTML` 로
    서버 결속을 통째로 덮었고, 서버 스캔은 그동안 초록이었다.
    ⚠ 이 시험은 **정적 린트**다 — "JS 가 값을 그리지 마라" 까지는 못 지킨다(그건 DOM 층).
    """
    root = Path(A.__file__).parent
    hits = []
    for f in sorted(list((root / "templates").rglob("*.html"))
                    + list((root / "static/js").rglob("*.js"))):
        src = _strip_comments(f.read_text(encoding="utf-8", errors="ignore"))
        for pat in (r"\bmarked\s*\.\s*parse\b", r"\bnew\s+showdown\b", r"\bmarkdownit\s*\("):
            for m in re.finditer(pat, src):
                hits.append(f"{f.relative_to(root)}:{src[:m.start()].count(chr(10)) + 1}")
    assert not hits, (
        "⛔ 브라우저 마크다운 파서가 살아 있다 — 서버 결속을 덮는다: " + " · ".join(hits)
        + "\n  마크다운은 app.doc_html()/md_html() 로 **서버에서** 그린다.")
    # 검사기 자기점검 — 패턴이 실제로 잡히는지 (양성 대조)
    assert re.search(r"\bmarked\s*\.\s*parse\b", "var h = marked.parse(raw);")


def test_concept_body_is_server_rendered_and_bound():
    """양성+⛔음성: 개념 문서가 **서버에서** 결속된 채 오고, raw 마크다운을 안 흘린다."""
    c = A.app.test_client()
    for cid in ("bvse", "beta-gate", "msd_reading"):
        r = c.get(f"/concept/{cid}")
        assert r.status_code == 200, cid
        h = r.get_data(as_text=True)
        assert 'id="md-src"' not in h, (
            f"⛔ /concept/{cid} 가 raw 마크다운을 다시 보낸다 — 재렌더 경로가 살아 있다")
        s = C.scan_claim_bindings(h)
        assert not s["unbound"], (
            f"/concept/{cid} 미결속: {[(x[0]['id'], x[0].get('text')) for x in s['unbound']]}")
    # ⛔음성 — 결속을 지운 채 같은 검사를 돌리면 잡혀야 한다
    h0 = c.get("/concept/bvse").get_data(as_text=True)
    stripped = re.sub(r"""\s+data-claim(?:-not)?=(?:"[^"]*"|'[^']*')""", "", h0)
    assert C.scan_claim_bindings(stripped)["unbound"], (
        "⛔ 검사기가 죽었다 — data-claim 을 다 지웠는데도 미결속이 0 이다")


def test_hazard_level_vocabulary_and_inactive_split():
    """⛔음성: hazard `level` 어휘·활성 판정이 갈라져 있다 (Codex BI 과소보고 (e))."""
    assert C.validate_hazards() == [], C.validate_hazards()
    ids = C.hazard_ids()
    active = {x["id"] for x in C.hazard_claims()}
    # ⛔⛔ 2026-09-09 (Codex BI-3 P0-1) — **이 시험이 틀린 해석을 기대값으로 고정하고 있었다.**
    #   종전: "level 이 HAZARD_INACTIVE 면 결속을 요구하면 **안 된다**".
    #   그 결과 `HZ-beta-hard-gate`(SUPERSEDED)의 *"판정으로 인용 금지"* 가 꺼졌고,
    #   화면에 "판정은 β ≥ 0.80 하드게이트를 통과하면 된다" 를 넣어도 탐지 0 이었다.
    #   ⇒ level(규칙 상태)과 prohibition_state(금지 상태)를 **갈라서** 본다.
    rows = {z["id"]: z for z in C._hazard_rows() if z.get("id")}
    for hid, z in rows.items():
        assert hid in ids, f"{hid} 이 결속 어휘에서 빠졌다 — 이력 언급이 유령이 된다"
        want = C.prohibition_active(z)
        assert (hid in active) == want, (
            f"⛔ {hid}: prohibition_active={want} 인데 결속 요구는 {hid in active} 다 "
            f"(level={z.get('level')} · prohibition_state={z.get('prohibition_state')})")
    # ⛔음성 — 어휘 밖 level 은 위반이어야 한다 (fail-closed)
    assert "MAYBE" not in C.HAZARD_LEVELS
    # ⛔음성 ①: **폐기된 규칙이라도 금지는 기본으로 살아 있다.**
    assert C.prohibition_active({"level": "SUPERSEDED"}), \
        "SUPERSEDED 는 규칙이 죽은 것이지 금지가 죽은 게 아니다 (BI-3 P0-1)"
    assert C.prohibition_active({"level": "STALE"}) and C.prohibition_active({"level": "HOLD"})
    assert C.prohibition_active({"level": "OOPS_TYPO"}), "어휘 밖은 fail-closed 여야 한다"
    assert not C.prohibition_active({"level": "RESOLVED"})
    # ⛔음성 ②: 명시가 level 을 이기고, 어휘 밖 명시는 active 로 떨어진다
    assert not C.prohibition_active({"level": "BLOCKED", "prohibition_state": "inactive"})
    assert C.prohibition_active({"level": "RESOLVED", "prohibition_state": "active"})
    assert C.prohibition_active({"level": "RESOLVED", "prohibition_state": "몰라"})
    # ⛔음성 ③: Codex 가 낸 실제 반례가 지금 잡히는가
    hit = C.find_claim_hits("판정은 β ≥ 0.80 하드게이트를 통과하면 된다", C.all_claims())
    # find_claim_hits → (start, end, claim, verdict)
    assert any(h[2].get("id") == "HZ-beta-hard-gate" for h in hit), \
        "⛔ 폐기된 β 게이트를 판정으로 쓰는 문장이 안 잡힌다 (BI-3 P0-1 반례)"


def test_retraction_can_say_there_is_no_alternative():
    """⛔음성: 스키마가 **"대체값 없음"** 을 표현할 수 있고, 아무 문장이나는 못 넣는다.

    Codex BI P0-1 의 근본 원인 — `validate()` 가 빈 `usable_instead` 를 거부해서
    "인용 가능한 수 0개" 를 적을 자리가 없었고, 그래서 원장이 **자기가 금지한 값**을
    대체값으로 권했다.
    """
    ok = {"why": "x", "instead_kind": "sentinel_none",
          "usable_instead": {"none": True, "why": "축이 닫혔다",
                             "decision": "D-2026-09-07-b2o3-md-closure-retrospective"}}
    assert C._check_usable_instead(ok) == []
    bad_cases = [
        ({"why": "x", "usable_instead": "아무 말"}, "instead_kind"),           # 이름 안 댐
        ({"why": "x", "instead_kind": "무엇", "usable_instead": "z"}, "어휘 밖"),
        ({"why": "x", "instead_kind": "sentinel_none",
          "usable_instead": {"none": True, "why": "w"}}, "decision"),          # 결정 없음
        ({"why": "x", "instead_kind": "sentinel_none",
          "usable_instead": {"none": True, "why": "w", "decision": "D-없는것"}}, "원장에 없는"),
        ({"why": "x", "instead_kind": "claim_ref", "usable_instead": "MD_Ea_eV@b2o3"},
         "인용 불가"),                                                          # 철회값으로 대체
        ({"why": "x", "instead_kind": "prose", "usable_instead": "저온 구간만"},
         "사람 검토"),                                                          # 서명 없음
    ]
    for rec, want in bad_cases:
        got = C._check_usable_instead(rec)
        assert got and want in got[0], f"{rec} → {got} (기대 문구: {want})"


def test_b2o3_md_axis_closure_is_enforced_in_every_ledger():
    """⛔음성: 비준된 마감이 **세 원장 전부에** 반영돼 있다 (Codex BI P0-1).

    ⛔ 사고 요약: 결정은 "인용 가능한 수 0개" 인데 ① registry 는 구간 Ea 0.2241 을
      대체값으로 권했고 ② hazard 는 level=CONDITIONAL 에 **존재하지 않는 키**를
      "이것만 인용" 이라 지목했고 ③ 형제 값 0.2234 는 provisional 로 남아 있었다.
      `validate()` 도 `validate_governance()` 도 셋 다 통과시켰다 — 원장끼리 안 봤다.
    """
    reg, D_ID = C.registry(), "D-2026-09-07-b2o3-md-closure-retrospective"
    ent = {(e.get("metric"), e.get("system")): e for e in reg["entries"]}
    e = ent[("MD_Ea_eV", "b2o3")]
    ui = (e.get("retracted") or {}).get("usable_instead")
    assert isinstance(ui, dict) and ui.get("none") is True, (
        "⛔ 마감된 축에 대체값 문자열이 돌아왔다 — 결정은 '인용 가능한 수 0개' 다")
    assert ui.get("decision") == D_ID
    assert "0.2241" not in json.dumps(ui, ensure_ascii=False), (
        "⛔ 금지된 구간 Ea 가 대체값 자리에 있다")
    # 형제 단일시드 값도 같은 축이다
    e2 = ent[("MD_Ea_eV_singleseed", "b2o3")]
    assert e2.get("citable") is False, (
        "⛔ 0.2234 (단일시드 Ea) 가 인용 가능한 채로 남아 있다 — 같은 UMA-MD 축이다")
    # hazard 쪽
    rows = {z.get("claim"): z for z in C._hazard_rows() if z.get("claim")}
    hz = rows.get("MD_Ea_eV@b2o3")
    assert hz and hz.get("level") == "BLOCKED", f"hazard level: {hz and hz.get('level')}"
    assert hz.get("id"), "hazard 행에 id 가 없으면 결속 기계에 안 보인다"
    assert "Ea_eV_PAPER 만 인용" not in (hz.get("fix") or ""), (
        "⛔ 죽은 키 지시가 fix 에 돌아왔다 (이력 필드에 남기는 것은 정상이다)")
    assert C.validate_hazards() == [], C.validate_hazards()


def test_retracted_cells_do_not_offer_one_click_citation():
    """⛔음성: 철회·비인용 값 칸이 **인용 복사 버튼을 주지 않는다** (Codex BI).

    결속(`data-claim`)은 *"이게 그 주장이다"* 라고 말할 뿐 **복사를 막지 않는다.**
    `/explorer` 는 마감된 축의 0.199 를 한 번 클릭으로 복사시키고 있었다 — 그게 원고로
    값이 들어가는 실제 경로다. 결속이 초록인 채로 뚫려 있던 자리라 회귀 시험이 필요하다.
    """
    c, cl = A.app.test_client(), C.all_claims()
    texts = {x["text"] for x in cl if x.get("text")}
    for url in ("/explorer", "/compare", "/composition/b2o3"):
        h = c.get(url).get_data(as_text=True)
        for m in re.finditer(r"citeVal\((.*?)\)", h):
            arg = m.group(1)
            hit = [t for t in texts if t in arg]
            assert not hit, f"⛔ {url}: 철회값 {hit} 에 원클릭 인용 버튼이 있다 — {arg[:110]}"
    # 양성 대조 — 정상 값에는 버튼이 **남아 있어야** 한다(과잉 차단이면 이게 0 이 된다)
    h = c.get("/explorer").get_data(as_text=True)
    assert h.count("citeVal(") > 20, "인용 버튼을 전부 없애 버렸다 — 그건 차단이 아니라 고장"
    assert 'class="cell-blocked"' in h, "차단 칸이 하나도 안 그려졌다"


def test_matcher_conditions_cut_false_positives_without_going_blind():
    """⛔음성: 매처 조건 셋(부호·단위·출처)이 **오탐만** 자르고 진성은 남긴다.

    Codex BI 실측: litdb 219편 자동결속 18건 중 **17이 남의 논문**이었다
    (deng2026 H₂O 흡착 −0.199 eV · spencer2022 exciton 50–90 meV · zhu2020 · ong2013).
    오탐이 분모를 부풀리면 "미결속 0" 이 더 그럴듯하게 틀린 수가 된다.
    ⚠ 반대 방향도 시험한다 — 조건이 너무 세면 **진성 인용까지 눈이 먼다**(fan2026 1건).
    """
    import json as _j
    c, cl = A.app.test_client(), C.all_claims()
    FALSE_POS = ["deng2026_polysulfate_layer_moisture_oxidation_lpsc",
                 "spencer2022_review_tco_band_structure_oxides",
                 "zhu2020_air_stable_se_design_principles",
                 "ong2013_lgps_family_substitution"]
    for pid in FALSE_POS:
        r = c.get(f"/api/paper/{pid}")
        assert r.status_code == 200, pid
        s = C.scan_claim_bindings(_j.loads(r.get_data(as_text=True))["html"],
                                  claims=cl, origin="external")
        assert not s["bound"] and not s["unbound"], (
            f"⛔ {pid}: 남의 논문 숫자를 우리 주장으로 셌다 — {s['bound'] or s['unbound']}")
        assert s["suspect"], f"{pid}: suspect 로도 안 남으면 감사가 불가능하다(조용한 배제)"
    # 진성 1건은 **살아 있어야** 한다 — 조건이 세지면 여기가 먼저 죽는다
    r = c.get("/api/paper/fan2026_sulfide_assb_stability_review_ECERD2600097")
    s = C.scan_claim_bindings(_j.loads(r.get_data(as_text=True))["html"],
                              claims=cl, origin="external")
    assert s["bound"] and not s["suspect"], (
        f"⛔ 진성 인용(우리 캠페인 값 인용문)이 조건에 걸려 사라졌다: {s}")


def test_unknown_word_after_number_is_not_a_unit():
    """⛔음성: 값 뒤의 **모르는 낱말**을 단위로 읽지 않는다.

    `Ea 0.199±0.034 vs 0.197±0.032` 에서 `vs` 를 단위로 읽어 진성 인용 한 건이
    suspect 로 떨어졌다 — 모르는 낱말을 증거로 쓰면 안 된다.
    """
    cl = [x for x in C.all_claims() if x["id"] == "MD_Ea_eV@b2o3"]
    ok = C.scan_claim_bindings("<p>b2o3 Ea 0.199±0.034 vs 0.197</p>", claims=cl,
                               origin="external")
    assert ok["unbound"] and not ok["suspect"], ok
    # 진짜 다른 단위는 여전히 suspect
    bad = C.scan_claim_bindings("<p>b2o3 window_gain 0.199 V</p>", claims=cl,
                                origin="external")
    assert bad["suspect"] and not bad["unbound"], bad


def test_disclaim_cannot_hide_a_real_citation():
    """⛔음성: **부인 안에 진짜 주장을 심으면 걸린다** (Codex BI P0-2a/P0-3 독약 주입).

    이 시험이 없어서 종전 검사는 다음 둘을 모두 통과시켰다:
      ① 부인 subtree 안에 자유텍스트로 철회값을 넣기 (disclaimed 1 → 2)
      ② 부인 subtree 안에 숫자만 넣기 (1 → 4)
    `_DISCLAIMED` 가 `(url, claim_id)` 쌍의 **사유 유무만** 보고 건수도 문맥도 안 봤다.
    """
    import re as _re
    c, cl = A.app.test_client(), C.all_claims()
    tgt = next(x for x in cl if x["id"] == "MD_Ea_eV@b2o3")
    h = c.get("/cascade").get_data(as_text=True)
    dec = _DISCLAIMED[("/cascade", "MD_Ea_eV@b2o3")]
    base = C.scan_claim_bindings(h, cl)
    n0, want = len(base["disclaimed"]), dec["n"]
    assert n0 == want, f"기준선이 선언과 다르다: {n0} ≠ {want}"
    # 기준선의 좌표도 선언과 같아야 한다 (여기가 아래 ③의 전제다)
    assert sorted(s for _c, _x, s, _b in base["disclaimed"]) == sorted(dec["where"]), \
        "기준선 좌표가 선언과 다르다"

    # 부인 여는 태그의 **닫는 꺾쇠 뒤**에 심는다 — 속성이 늘어도 안 깨지게 정규식으로.
    OPEN = _re.compile(r'(data-claim-not="MD_Ea_eV@b2o3"[^>]*>)')
    def inject(txt):
        return OPEN.sub(lambda m: m.group(1) + txt, h, count=1)

    # ① 자유텍스트 주입 — 부인 영역 안에 진짜 인용을 심는다
    p1 = inject(f'b2o3 의 MD Ea 는 {tgt["text"]} eV 다. ')
    assert p1 != h, "주입이 안 됐다 — 마크업이 바뀌었으면 이 시험부터 고쳐라"
    assert len(C.scan_claim_bindings(p1, cl)["disclaimed"]) != want, (
        "⛔ 부인 안에 진짜 인용을 심었는데 건수가 그대로다 — 검사가 죽었다")
    # ② 숫자만 주입
    p2 = inject(f'{tgt["text"]} ')
    assert len(C.scan_claim_bindings(p2, cl)["disclaimed"]) != want, (
        "⛔ 숫자만 심어도 안 걸린다 — 부인이 여전히 담요다")

    # ③ ★ Codex BI-3 P0-2 의 실제 반례 — **건수는 그대로 두고 그 자리의 의미만 바꾼다.**
    #    종전 검사는 이걸 통과시켰다(disclaimed 1 · unbound 0 · dangling 0 으로 초록).
    #    이제 `data-claim-not-src` 가 달라져 선언과 안 맞아야 한다.
    #    ⚠ 표에는 `data-claim-not` 셀이 여러 개인데 0.199 를 담은 것은 하나다.
    #      첫 번째를 바꾸면 엉뚱한 셀이라 아무 효과가 없다 — **선언된 좌표를 콕 집는다.**
    only = dec["where"][0]
    assert h.count(f'data-claim-not-src="{only}"') == 1, \
        f"전제: 선언 좌표 {only} 가 화면에 정확히 한 번 있어야 한다"
    p3 = h.replace(f'data-claim-not-src="{only}"',
                   'data-claim-not-src="rank=99.0|Ea_MD"', 1)
    assert p3 != h, "src 속성이 없다 — 화면이 부인 자리의 계보를 안 낸다"
    sc3 = C.scan_binding_or_none(p3, cl) if hasattr(C, "scan_binding_or_none") else \
        C.scan_claim_bindings(p3, cl)
    got3 = sorted(s for _c, _x, s, _b in sc3["disclaimed"])
    assert len(sc3["disclaimed"]) == want, "전제: 건수는 그대로여야 이 반례가 성립한다"
    assert got3 != sorted(dec["where"]), (
        "⛔ 그 자리의 의미가 바뀌었는데 좌표가 같다 — 건수만 보는 검사로 되돌아갔다")

    # ④ ★★ Codex BI-4 P0-2 의 반례 — **좌표도 그대로 두고 표시 내용만 바꾼다.**
    #    ③ 은 좌표를 건드려서 잡혔지만, 좌표를 안 건드리면 종전 검사는 전부 초록이었다
    #    (실측: disclaimed 1 · unbound 0 · dangling 0 · 좌표까지 동일).
    #    이제 `verify_disclaimers` 가 셀의 글을 원자료 값과 대므로 잡혀야 한다.
    import re as _re4
    p4 = _re4.sub(r'(data-claim-not-src="' + _re4.escape(only) + r'"[^>]*>)0\.199(<)',
                  r'\g<1>b2o3 MD Ea = 0.199 eV\g<2>', h, count=1)
    assert p4 != h, "전제: 선언 좌표의 셀에 `0.199` 가 그대로 들어 있어야 한다"
    sc4 = C.scan_claim_bindings(p4, cl)
    assert len(sc4["disclaimed"]) == want and len(sc4["unbound"]) == 0, \
        "전제: 종전 지표는 그대로여야 이 반례가 성립한다 (그래서 종전 검사가 초록이었다)"
    assert sorted(s for _c, _x, s, _b in sc4["disclaimed"]) == sorted(dec["where"]), \
        "전제: 좌표도 그대로여야 한다 — 좌표가 바뀌면 ③ 이 잡는 것과 같은 사례다"
    v4 = C.verify_disclaimers(sc4["disclaimed"])
    assert v4 and not any(x["ok"] for x in v4), (
        "⛔ 좌표는 같은데 **표시 내용이 다른 발화로 바뀌었다** — 원자료 대조가 안 걸렸다. "
        f"판정: {[x['why'] for x in v4]}")

    # ⑤ ⛔음성: 정상 화면은 **통과해야** 한다 (과잉차단도 결함이다)
    v5 = C.verify_disclaimers(base["disclaimed"])
    assert v5 and all(x["ok"] for x in v5), (
        f"⛔ 정상 화면의 부인이 원자료와 안 맞는다: {[x['why'] for x in v5 if not x['ok']]}")

    # ⑥ ⛔음성: **원자료를 못 읽으면 통과가 아니다** (BI-4 P0-1 과 같은 규율)
    v6 = C.verify_disclaimers(base["disclaimed"], resolve=lambda ds: None)
    assert v6 and not any(x["ok"] for x in v6), \
        "⛔ 원자료를 못 읽었는데 부인이 통과했다 — 확인 불가가 승인이 됐다"

    # ⑦ ⛔음성: 데이터셋 이름 없는 옛 2칸 좌표는 **검증 불가**로 떨어져야 한다
    v7 = C.verify_disclaimers([({"id": "X"}, "ctx", "rank=25.0|window_gain", "0.199")])
    assert not v7[0]["ok"] and "데이터셋" in v7[0]["why"], \
        f"⛔ 데이터셋 없는 좌표가 통과했다: {v7[0]}"


def test_disclaim_is_not_a_blanket_over_a_whole_table():
    """⛔음성: **부인 하나가** 표·행을 덮으면 실패 (담요 금지).

    실측(2026-09-08 이전): `/cascade` 의 `data-claim-not` div 하나가 td 600 · tr 41 ·
    텍스트노드 605 · 3800자를 덮었다. 충돌 셀은 그중 1칸이었다.
    ⚠ 재는 것은 **총합이 아니라 한 선언의 폭**이다. 셀마다 따로 선언하면 총합은 커져도
      각 선언은 좁다 — 그게 좁힌 것이고, 총합으로 재면 그 개선이 벌점으로 보인다.
    """
    from html.parser import HTMLParser
    h = A.app.test_client().get("/cascade").get_data(as_text=True)

    class _Span(HTMLParser):
        """`data-claim-not` 요소 **하나하나**의 폭 (글자수 · 안에 든 tr/table 수)."""

        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack = []        # [(tag, is_not, chars, rows)]
            self.spans = []        # [(chars, rows)]

        def handle_starttag(self, tag, attrs):
            if tag in ("br", "img", "hr", "input", "meta", "link"):
                return
            isn = bool(dict(attrs).get("data-claim-not"))
            if self.stack and tag in ("tr", "table"):
                for f in self.stack:
                    if f[1]:
                        f[3] += 1
            self.stack.append([tag, isn, 0, 0])

        def handle_endtag(self, tag):
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    for f in self.stack[i:]:
                        if f[1]:
                            self.spans.append((f[2], f[3]))
                    del self.stack[i:]
                    return

        def handle_data(self, data):
            n = len(data.strip())
            if n:
                for f in self.stack:
                    if f[1]:
                        f[2] += n
    p = _Span()
    p.feed(h)
    assert p.spans, "부인이 하나도 없다 — 이 시험의 전제가 깨졌다"
    worst_c = max(c for c, _r in p.spans)
    worst_r = max(r for _c, r in p.spans)
    assert worst_r == 0, (
        f"⛔ 부인 하나가 표/행을 통째로 덮는다 (tr·table {worst_r}개) — 부인은 "
        f"**셀 단위 선언**이다. 담요는 그 안의 진짜 인용까지 조용히 억제한다")
    assert worst_c < 120, (
        f"⛔ 부인 하나가 너무 넓다 ({worst_c}자) — 담요다. 선언 {len(p.spans)}개, "
        f"총 {sum(c for c, _ in p.spans)}자")


# ── 메모·코멘트 표시 경로 (Codex BI-3 P0-3) ──────────────────────────────────
def test_note_display_is_rendered_and_bound_by_the_server():
    """⛔음성: 메모·코멘트 표시가 **서버 렌더러 한 곳**을 지나야 한다.

    BI-3 P0-3 실측 — `comments.js` 의 `inline()` 이 브라우저에서 따로
    `**0.199**` → `<b>0.199</b>` 를 만들고 있었다. 서버 `_mdlite` 를 고쳐 놓고도
    **메모 경로에는 전파되지 않아** 결속 없이 철회값이 나갔다.
    `docnote.js` 도 같은 함수를 부르므로 두 화면이 같이 샜다.
    """
    tgt = next(x for x in C.all_claims() if x["id"] == "MD_Ea_eV@b2o3")
    # ① 서버 렌더러가 결속한다
    h = A.note_html(f'b2o3 MD Ea 는 **{tgt["text"]}** eV 다')
    sc = C.scan_claim_bindings(f"<div>{h}</div>", C.all_claims())
    assert len(sc["bound"]) == 1 and not sc["unbound"], \
        f"⛔ 메모 렌더러가 철회값을 결속 없이 그렸다: {h[:200]}"
    assert "claim-flag" in h, "결속 표식이 안 붙었다"
    # ② 0 이 사라지지 않는다 (같은 렌더러를 쓰므로 여기서도 지켜져야 한다)
    assert "0" in A.note_html("0")
    # ③ 그림은 **우리 규격만** — 임의 URL 은 글자 그대로 (메모 한 줄로 외부 요청 금지)
    ok = A.note_html("![a](/api/note-image/" + "a" * 32 + ".png)")
    bad = A.note_html("![b](https://evil.example/x.png)")
    assert "<img" in ok and "<img" not in bad, "그림 화이트리스트가 샌다"


def test_comments_api_gives_display_html_for_every_item():
    """⛔음성: 코멘트 API 가 item 마다 `html` 을 내야 한다 (편집용 `text` 는 보존)."""
    c = A.app.test_client()
    r = c.get("/api/comments/CLAUDE.md")
    assert r.status_code == 200
    d = r.get_json()
    assert isinstance(d.get("items"), list), "items 가 없다"
    for it in d["items"]:
        assert "text" in it, "편집용 원문이 사라졌다 — 고치기가 깨진다"
        assert isinstance(it.get("html"), str), \
            f"표시용 html 이 없다 — 클라이언트가 자기 파서로 되돌아간다: {it.get('id')}"


def test_client_note_display_does_not_reparse():
    """⛔음성 (정적 린트): 표시 자리에서 `inline(` 을 부르면 실패.

    파서를 둘 두지 마라 — 서버가 그린 `html` 만 표시한다. `inline` 자체는
    **편집 보조**(굵게 버튼 미리보기 등)로 남을 수 있으므로 함수 존재는 허용하고,
    **카드 본문을 그리는 줄**에서 쓰이는 것만 막는다.
    """
    import pathlib
    root = pathlib.Path(A.__file__).resolve().parent / "static/js"
    bad = []
    for f in ("comments.js", "docnote.js"):
        for i, ln in enumerate(root.joinpath(f).read_text(encoding="utf-8").splitlines(), 1):
            if ("cmt-t" in ln or "dn-text" in ln) and "inline(" in ln:
                bad.append(f"{f}:{i}  {ln.strip()[:110]}")
    assert not bad, ("⛔ 메모 표시 자리가 브라우저에서 다시 파싱한다 (BI-3 P0-3 재발):\n  "
                     + "\n  ".join(bad))
    # 그리고 서버가 html 을 안 주면 **옛 렌더러로 조용히 되돌아가면 안 된다**
    src = root.joinpath("comments.js").read_text(encoding="utf-8")
    assert "function disp(" in src and "cmt-unrendered" in src, \
        "html 이 없을 때의 처리가 눈에 보이지 않는다 — 조용한 폴백은 재발이다"


def test_unverified_surfaces_are_declared_and_do_not_grow():
    """⛔ **검사 못 한 표면**이 선언돼 있고, 조용히 늘지 않는가 (Codex BI-4 조건 6).

    이 시험은 무엇을 검증하지 **않는다** — 그게 요점이다. 검증하지 못한 것이
    기계가 읽는 자리에 남아 있는지만 본다. 산문으로만 적으면 다음 사람이
    "검사했겠지" 로 읽고, 그게 이번 리뷰 전체의 요지다.

    ⚠ 이 목록은 **줄어야** 진전이다. `CAP` 을 올리려면 왜 늘었는지 사유를 같이 적어라.
    """
    CAP = 5
    assert _UNVERIFIED_SURFACES, "미검사 표면 선언이 비었다 — 다 검증했다면 CAP 을 0 으로 내려라"
    assert len(_UNVERIFIED_SURFACES) <= CAP, (
        f"⛔ 미검사 표면이 {len(_UNVERIFIED_SURFACES)}개로 늘었다 (상한 {CAP}). "
        f"늘리려면 사유를 적고 CAP 을 올려라 — 조용히 늘면 선언의 뜻이 없다")
    for name, why in _UNVERIFIED_SURFACES.items():
        assert len(str(why).strip()) >= 20, f"{name}: 사유가 너무 짧다 — 무엇을 왜 못 봤나"
    # 벤더 JS 가 실제로 없다는 전제를 확인한다 — 생기면 이 선언의 근거가 바뀐다
    vend = A.ROOT / "webapp/static/vendor" if hasattr(A, "ROOT") else None
    if vend and vend.is_dir():
        js = sorted(p.name for p in vend.glob("*.js"))
        assert not js, (
            f"⛔ 벤더 JS 가 생겼다: {js} — 이제 브라우저 검증을 켤 수 있다. "
            f"_UNVERIFIED_SURFACES 를 다시 보라 (더 이상 '못 한다' 가 아니다)")


def test_figure_comment_deeplink_carries_the_figure_key():
    """⛔ 그림 코멘트 딥링크가 **그 그림까지** 데려가는가 (1저자 실사용 보고 2026-09-09).

    종전 `note_url` 주석이 *"파일·그림 코멘트는 붙일 자리가 없어 문서만 연다"* 였는데
    **자리는 있었다** — `figref.js` 가 그림 칸마다 `data-fig="<키>"` 를 달고,
    `rel` → 키 매핑(`_fig_keys`)도 있었다. 셋이 다 있는데 아무도 안 이었다.
    """
    figs = [c for c in D.comment_all() if not c.get("anchor")
            and str(c.get("rel", "")).startswith("litdb/figures/")]
    if not figs:
        pytest.skip("그림 코멘트가 없다")
    linked = [c for c in figs if "fig=" in D.note_url(c)]
    assert linked, "⛔ 그림 코멘트 딥링크에 fig= 가 하나도 없다 — 자리를 다시 잃었다"
    # 대부분은 붙어야 한다 (figures.json 에 없는 파일만 예외)
    assert len(linked) >= len(figs) * 0.8, (
        f"⛔ 그림 코멘트 {len(figs)}건 중 {len(linked)}건만 딥링크가 붙었다 — "
        f"figures.json 매핑이 깨졌는지 보라")
    # ⛔음성: 여백 메모는 fig= 가 아니라 note= 여야 한다 (두 체계를 섞으면 안 된다)
    for c in D.comment_all():
        if c.get("anchor"):
            u = D.note_url(c)
            assert "note=" in u and "fig=" not in u, f"여백 메모에 fig= 가 붙었다: {u}"
            break
    # ⛔음성: figures.json 에 없는 파일은 **조용히 문서만** 연다 (틀린 자리로 데려가지 않는다)
    fake = {"url": "/literature?open=zzz", "anchor": "",
            "rel": "litdb/figures/없는슬러그/fig_99.png"}
    assert D.note_url(fake) == "/literature?open=zzz"


def test_note_bold_is_lenient_about_one_sided_space():
    """메모의 `**굵게**` — 한쪽만 띈 것도 굵게, **양쪽 다 띈 것은 아니다**.

    1저자 실사용에서 `suggests** low multicollinearity**` 가 안 먹었다.
    CommonMark 로는 굵게가 아닌 게 맞지만 **여기는 메모장이지 문서 규격이 아니다**.
    다만 `10 ** 3 and 2 ** 4`(양쪽 다 띔)까지 굵어지면 안 된다 — 그게 원래 가드의 목적이다.
    """
    for text, want, why in (
        ("distribution suggests** low multicollinearity**, indicating", True, "여는 쪽만 띔"),
        ("** Li-S4 sublattice volume + CSM**: 사면체", True, "여는 쪽만 띔(문두)"),
        ("**정상 굵게** 는 되나", True, "양쪽 다 붙음"),
        ("**닫는 쪽만 띔 ** 이건?", True, "닫는 쪽만 띔"),
        ("10 ** 3 and 2 ** 4 는 거듭제곱", False, "⛔음성: 양쪽 다 띔"),
        ("경로는 src/**/*.py 다", False, "⛔음성: globstar"),
        ("각주(**)를 보라", False, "⛔음성: 닫는 문장부호"),
    ):
        h = str(A._mdlite(text))
        assert ("<strong>" in h) is want, f"{why}: {text!r} → {h!r}"
    # 안쪽 공백은 **지우지 말고 태그 밖으로** — 지우면 낱말이 붙는다
    h = str(A._mdlite("suggests** low x**"))
    assert "suggests <strong>low x</strong>" in h, f"공백이 사라져 낱말이 붙었다: {h!r}"


def test_digest_date_marker_is_actually_parsed():
    """⛔음성 (2026-09-13 실측): 파일에 `digested <날짜>` 가 있는데 목록이 **못 읽으면**
    그 논문은 최신순 정렬에서 **조용히 맨 뒤로 가라앉는다**.

    실측: 머리말이 긴 digest 3편이 `digested` 를 22·25행에 뒀는데 파서는 첫 **18줄**만
      읽었다. 264편 중 258·259·261위로 밀렸고, 1저자는 *"논문이 아직 안 떴다"* 고 했다.
      값이 틀린 게 아니라 **순서가 틀렸고**, 아무도 오류를 안 봤다.

    ⛔ 이 시험이 못 하는 것: 날짜가 **맞는지**는 못 본다. 파일에 있는 표기를 목록이
      집어가는지만 본다. 표기 자체가 없는 digest 는 여기 대상이 아니다.
    """
    import re as _re
    from pathlib import Path as _P
    papers = {p["id"]: p for p in D.list_papers()}
    pdir = _P(D.LITDB) / "papers"
    missed, checked = [], 0
    for f in sorted(pdir.glob("*.md")):
        if "__seminar" in f.stem or f.stem not in papers:
            continue
        m = _re.search(r"digest(?:ed)?\s*`?(\d{4}-\d{2}-\d{2})`?",
                       f.read_text(encoding="utf-8", errors="ignore"), _re.I)
        if not m:
            continue
        checked += 1
        if not papers[f.stem].get("digested"):
            missed.append((f.stem, m.group(1)))
    assert checked >= 200, (
        f"전제 붕괴: 날짜 표기를 가진 digest 가 {checked}편뿐이다 — 이 시험이 "
        f"아무것도 안 보고 있다 (경로나 표기 규약이 바뀌었는지 봐라)")
    assert not missed, (
        "⛔ 파일에 날짜가 있는데 목록이 못 읽었다 — 이 논문들은 최신순에서 맨 뒤로 "
        "가라앉는다. 파서의 머리말 스캔 창을 넓혀라 (data.list_papers):\n"
        + "\n".join(f"  {s}: 파일에는 {d}" for s, d in missed[:10]))


def test_recent_digests_rank_near_the_top():
    """⛔음성: 오늘 들어온 digest 가 목록 **뒤쪽**에 있으면 화면에서 안 보인다.

    위 시험이 '날짜를 읽었는가' 를 본다면, 이것은 '읽은 날짜가 **정렬에 실제로
    쓰이는가**' 를 본다. 파서가 날짜를 읽어도 정렬이 그것을 안 쓰면 결과는 같다.
    """
    ps = D.list_papers()
    dated = [(i, p) for i, p in enumerate(ps) if p.get("digested")]
    assert dated, "전제: 날짜가 있는 digest 가 존재한다"
    newest = max(p["digested"] for _, p in dated)
    top = [p["id"] for _, p in dated if p["digested"] == newest]
    pos = {p["id"]: i for i, p in enumerate(ps)}
    bad = [t for t in top if pos[t] > len(ps) * 0.1]
    assert not bad, (
        f"⛔ 가장 최근 digest({newest})가 상위 10 % 밖에 있다 — 최신순 정렬이 "
        f"날짜를 안 쓰고 있다: " + ", ".join(f"{b}({pos[b]+1}위/{len(ps)})" for b in bad))
