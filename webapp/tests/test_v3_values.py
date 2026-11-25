"""test_v3_values.py — v3 묶음 C (값 표면 + 인용 안전) 회귀시험.

무엇을 지키나
  ① `/api/element` 가 `/cascade` 와 **같은** archive 게이트를 탄다 (P0-02)
  ② 폐기된 β ≥ 0.80 하드게이트가 `/compare` 에서 **판정**으로 안 쓰인다 (P0-06)
  ③ 비인용 축(citable:false)이 TODO 와 **같은 기호**로 안 그려진다
  ④ `/explorer` 의 '값 있는 조성만' 이 분석 파일도 자료로 센다
  ⑤ `not_assessed` 를 fail 로 렌더하지 않는다 (P0-17)
  ⑥ `/compare` 가 **브라우저에서 조립하는** 셀에도 서버 파생 claim id 가 붙는다

⛔ 이 파일이 **못 하는 것**
  · 브라우저를 띄우지 않는다. `/compare` 표는 JS 가 조립하므로 여기서 검사하는 것은
    **조립 원천**(서버가 내려보낸 CANON·CBIND·CBLOCK)이지 최종 DOM 이 아니다.
    조립 코드가 CBIND 를 안 쓰도록 바뀌면 이 시험은 그걸 못 본다 —
    그래서 `test_compare_assembly_uses_the_binding` 이 템플릿 문자열도 같이 본다.
  · 값이 물리적으로 맞는지는 보지 않는다. 지위·표기만 본다.

⚠ 음성 경로(틀린 입력을 잡아내는지)를 반드시 같이 시험한다 — 양성만 있는 검사는
  통과해도 아무것도 보증하지 못한다.
"""
import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as A                       # noqa: E402
import canonical as C                 # noqa: E402
import data as D                      # noqa: E402


@pytest.fixture()
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


# ══════════════════════════════════════════════════════════════════════════
# ① /api/element 의 archive 게이트 (P0-02)
# ══════════════════════════════════════════════════════════════════════════
def test_api_element_hides_ranking_without_archive(client):
    """⛔ 사이트가 '승인 랭킹 0종' 이라 쓰면서 순위를 배포하면 안 된다."""
    d = json.loads(client.get("/api/element?syms=Ti").get_data(as_text=True))
    rows = [r for e in d["elements"] for r in (e.get("cascade") or [])]
    assert rows, "전제: Ti 는 스크리닝 스냅샷에 나온다 (없어졌으면 이 검사를 옮겨라)"
    for r in rows:
        for f in A.CASCADE_ARCHIVE_FIELDS:
            assert f not in r, f"게이트 없이 {f} 가 나갔다: {r}"
        assert r.get("archive_gated") is True, "가려졌다는 사실을 응답이 말하지 않는다"
        assert r.get("dopant"), "이름까지 지우면 주기율표 강조가 근거를 잃는다"
    assert d.get("cascade_archive_gated") is True


def test_api_element_archive_query_still_serves(client):
    """⛔음성: 게이트가 '값이 없다' 를 가리키면 안 된다 — `?archive=1` 이면 나와야 한다.

    이게 없으면 위 시험은 "원자료가 비었다" 로도 통과한다.
    """
    d = json.loads(client.get("/api/element?syms=Ti&archive=1").get_data(as_text=True))
    rows = [r for e in d["elements"] for r in (e.get("cascade") or [])]
    assert any("rank" in r for r in rows), "보관함에서도 순위가 안 나온다 — 게이트가 아니라 결측이다"
    assert d.get("cascade_archive_gated") is False


def test_gate_cascade_rows_negative_paths():
    """게이트 함수 자체 — 양성/음성 둘 다."""
    row = {"dopant": "TiO2", "group": "TM", "rank": 41.0, "score": 0.351,
           "ox_V": 2.0, "E_GPa": 46.2, "pugh": 0.96}
    out = A._gate_cascade_rows([row], archive=False)[0]
    assert out == {"dopant": "TiO2", "group": "TM", "archive_gated": True}
    # ⛔음성 ①: 가려진 자리를 0 이나 None 으로 **메우면 안 된다** (없는 것과 가린 것은 다르다)
    assert "rank" not in out and "score" not in out
    # ⛔음성 ②: archive=True 면 그대로 나와야 한다 — 아니면 이건 게이트가 아니라 삭제다
    assert A._gate_cascade_rows([row], archive=True)[0]["rank"] == 41.0
    # ⛔음성 ③: 원본을 **고치면** 안 된다 (dict 를 그대로 돌려주면 캐시가 오염된다)
    assert row["rank"] == 41.0


def test_elements_legend_says_superseded_before_the_click(client):
    """주기율표 33칸이 '살아 있는 결과' 처럼 보이면 안 된다."""
    h = client.get("/elements").get_data(as_text=True)
    assert "historical 스크리닝 <b>(superseded)</b>" in h, "범례가 지위를 안 말한다"
    assert "승인된 랭킹 0종" in h or "승인 랭킹 0종" in h
    # 지위 없이 부르던 옛 범례 문구가 남아 있으면 실패
    assert "<i class=\"lg-casc\"></i> 도핑 스크리닝 도펀트" not in h
    # 딥링크는 보관함으로 — 기본 /cascade 의 #board-tbl 은 비어 있어서 빈 표에 떨어졌다
    assert "/cascade?archive=1#" in h


# ══════════════════════════════════════════════════════════════════════════
# ⑤ not_assessed 는 fail 이 아니다 (P0-17)
# ══════════════════════════════════════════════════════════════════════════
def test_gate_outcome_reads_verdict_when_lineage_is_missing():
    """항목이 자기 말로 `verdict: not_assessed` 라고 적었으면 그걸 읽는다."""
    e = {"metric": "X", "system": "y", "blocking_gate": "g",
         "gate_detail": {"verdict": "not_assessed"}}
    assert C.gate_outcome(e) == "not_assessed"
    assert "미평가" in C.gate_prefix(e) and "미통과" not in C.gate_prefix(e)


def test_gate_outcome_negative_paths():
    """⛔음성: 완화가 아니라는 것을 시험한다."""
    # ① 아무 판정 기록도 없으면 여전히 fail (보수적)
    assert C.gate_outcome({"blocking_gate": "g"}) == "fail"
    # ② 어휘 밖 verdict 는 통과로 봐주지 않는다 — fail-closed
    assert C.gate_outcome({"blocking_gate": "g",
                           "gate_detail": {"verdict": "사실상 통과"}}) == "fail"
    # ③ 게이트가 없으면 None (게이트 문구도 빈 문자열)
    assert C.gate_outcome({"metric": "X"}) is None
    # ④ 미평가는 **여전히 정본을 막는다** — 문구만 달라진 것이지 판정을 바꾼 게 아니다
    assert C.gate_blocks_canonical({"blocking_gate": "g",
                                    "gate_detail": {"verdict": "not_assessed"}}) is True
    # ⑤ lineage 가 있으면 그쪽이 이긴다 (우선순위 유지)
    assert C.gate_outcome({"blocking_gate": "g",
                           "gate_detail": {"verdict": "not_assessed",
                                           "lineage": {"gate_outcome": "pass"}}}) == "pass"


def test_sigma_ratio_entries_render_as_not_assessed():
    """실물 원장: σ 비 3항목이 '미통과' 로 그려지면 안 된다."""
    reg = C.registry()
    rows = [e for e in reg["entries"]
            if str(e.get("metric", "")).startswith("MD_sigma_ratio")]
    assert len(rows) == 3, f"전제: σ 비 3항목 (실측 {len(rows)})"
    for e in rows:
        assert C.gate_outcome(e) == "not_assessed"
        assert "미통과" not in C.gate_prefix(e)


# ══════════════════════════════════════════════════════════════════════════
# ③ 비인용 축은 TODO 가 아니다
# ══════════════════════════════════════════════════════════════════════════
def test_noncitable_metrics_is_all_or_nothing():
    """축 전체가 비인용일 때만 든다 — 한 칸이라도 쓸 수 있으면 열을 접으면 안 된다."""
    reg = {"entries": [
        {"metric": "M1", "system": "a", "citable": False, "why_non_citable": "왜"},
        {"metric": "M1", "system": "b", "citable": False},
        {"metric": "M2", "system": "a", "citable": False},
        {"metric": "M2", "system": "b"},                    # ← 하나가 인용 가능
        {"metric": "M3", "system": "a", "status": "retracted"},
    ]}
    out = C.noncitable_metrics(reg=reg)
    assert "M1" in out and out["M1"]["why"] == "왜"
    assert sorted(out["M1"]["systems"]) == ["a", "b"]
    # ⛔음성 ①: 섞인 축은 통째로 접히면 안 된다 (그 값이 화면에서 사라진다)
    assert "M2" not in out
    # ⛔음성 ②: 철회는 비인용 축이 아니다 — 취소선·결속으로 **보여야** 한다
    assert "M3" not in out
    # ⛔음성 ③: 빈 원장이면 빈 결과 (없는 축을 만들어 내지 않는다)
    assert C.noncitable_metrics(reg={"entries": []}) == {}


def _exp_thead(html):
    """`/explorer` **본 표**의 thead 만. (방법검증 앵커 표가 위에 있어 위치로 자르면 틀린다)"""
    i = html.index('id="exp-table"')
    return html[i:html.index("<tbody>", i)]


def test_explorer_moves_noncitable_axes_out_of_the_main_table(client):
    """σ 비 3열이 14행 TODO 로 찍히던 자리 — 이제 사유와 함께 별도 절이다."""
    nc = C.noncitable_metrics()
    assert nc, "전제: 원장에 비인용 축이 있다"
    h = client.get("/explorer").get_data(as_text=True)
    assert "비인용 축" in h
    head = _exp_thead(h)                      # 본 표의 thead
    for k in nc:
        assert k not in head, f"비인용 축 {k} 가 아직 본 표 열이다 (TODO 로 읽힌다)"
        assert k in h, f"비인용 축 {k} 가 화면에서 **사라졌다** — 접는 것이지 지우는 게 아니다"
    # 사유가 화면에 있어야 한다. 없으면 "왜 못 쓰는지" 를 아무도 모른다
    assert "why_non_citable" in h or "원자료" in h


def test_explorer_shows_the_three_kinds_of_empty(client):
    """TODO / N/A / 비인용 — 셋을 갈라 가르치는 범례가 표 위에 있어야 한다."""
    h = client.get("/explorer").get_data(as_text=True)
    above = h[:h.index('id="exp-table"')]     # 표 **위**에 있어야 뜻이 먼저 읽힌다
    for word in ("TODO", "N/A", "비인용"):
        assert word in above, f"표 위 범례에 {word} 구분이 없다"
    # 방법 검증 앵커도 표 위 (표의 숫자를 믿을지 말지 정하는 정보다)
    assert "방법 검증 앵커" in above


# ══════════════════════════════════════════════════════════════════════════
# ④ '값 있는 조성만' 이 분석 파일도 센다
# ══════════════════════════════════════════════════════════════════════════
def test_explorer_hasval_counts_analysis_files(client):
    """⛔ 자료가 있는데 없다고 말하면 안 된다 (vgcf_hbn·li3n)."""
    am = D.analysis_matrix()
    have = [cid for cid in D.COMPOSITIONS
            if am.get(cid) and not any(
                D.canonical_table().get(k, {}).get(cid) is not None
                for k in D.canonical_table())]
    assert have, "전제: canonical 값 0 인데 분석 파일은 있는 조성이 있다"
    h = client.get("/explorer").get_data(as_text=True)
    for cid in have:
        m = re.search(r'<tr data-fam="[^"]*" data-hasval="(\d)" data-s="[^"]*%s"' % re.escape(cid), h)
        assert m, f"{cid} 행을 못 찾았다"
        assert m.group(1) == "1", f"{cid} 는 분석 자료가 있는데 hasval=0 이라 첫 화면에서 숨는다"


# ══════════════════════════════════════════════════════════════════════════
# ② 폐기된 β 하드게이트 (P0-06)
# ══════════════════════════════════════════════════════════════════════════
#: 화면이 β 를 **판정**으로 쓸 때 나오던 문장들. 원장(HZ-beta-hard-gate)이 폐기했다.
_BETA_VERDICT_PHRASES = (
    "β가 낮으면 확산이 아니다",
    "그 D는 인용 금지",
    "0.61 ⛔",
    "유일한 탈락은 LPSOCl 600 K",
)


def test_compare_does_not_use_beta_as_a_verdict(client):
    h = client.get("/compare").get_data(as_text=True)
    for p in _BETA_VERDICT_PHRASES:
        assert p not in h, f"폐기된 β 하드게이트 판정 문구가 남아 있다: {p!r}"
    # 새 판정축이 화면에 있어야 한다 (문구를 지우기만 하면 판정이 사라진다)
    assert "plateau" in h and "홉" in h
    # 그리고 그 자리는 원장 이름을 대야 한다
    assert 'data-claim="HZ-beta-hard-gate"' in h
    assert "HZ-beta-hard-gate" in C.hazard_ids(), "결속 이름이 원장에 없다 (유령 결속)"


def test_compare_keeps_the_superseded_beta_history(client):
    """⛔ 삭제가 아니라 접기다 — 이력이 사라지면 왜 폐기됐는지 알 수 없다."""
    h = client.get("/compare").get_data(as_text=True)
    assert "superseded" in h.lower()
    for v in ("0.87", "0.61", "0.81"):     # 200 ps β 표의 실측값
        assert v in h, f"이력 β 표의 {v} 가 화면에서 사라졌다"


# ══════════════════════════════════════════════════════════════════════════
# ⑥ /compare 의 클라이언트 조립에도 서버 파생 결속 (Codex 회신에 우리가 적은 사각)
# ══════════════════════════════════════════════════════════════════════════
def _js_obj(html, name):
    """`const NAME={...};` 한 줄에서 JSON 객체를 꺼낸다."""
    m = re.search(r"const %s=(\{.*?\});\n" % re.escape(name), html, re.S)
    assert m, f"{name} 이 /compare 에 없다"
    return json.loads(m.group(1))


def _unnamed_blocked_cells(html):
    """조립 원천에서 **이름을 못 대는 금지 칸**을 센다 → [(metric, cid) ...]."""
    canon = _js_obj(html, "CANON")
    bind = _js_obj(html, "CBIND")
    block = _js_obj(html, "CBLOCK")
    bad = []
    for k, row in canon.items():
        for cid, v in (row or {}).items():
            if v is None:
                continue
            key = f"{k}|{cid}"
            if key in block and key not in bind:
                bad.append((k, cid))
    return bad


def test_compare_blocked_cells_carry_a_claim_id(client):
    """⛔ 철회값이 이름 없이 셀로 조립되면 안 된다."""
    h = client.get("/compare").get_data(as_text=True)
    block = _js_obj(h, "CBLOCK")
    canon = _js_obj(h, "CANON")
    live = [k for k in block
            if canon.get(k.split("|")[0], {}).get(k.split("|")[1]) is not None]
    assert live, "전제: /compare 표에 금지 칸이 실제로 그려진다 (b2o3 MD Ea 0.199)"
    assert _unnamed_blocked_cells(h) == []


def test_compare_binding_check_catches_a_missing_binding(client):
    """⛔음성: 결속을 지우면 위 검사가 **반드시** 잡아야 한다.

    이게 없으면 `_unnamed_blocked_cells` 가 늘 빈 목록을 내도 통과한다.
    """
    h = client.get("/compare").get_data(as_text=True)
    broken = re.sub(r"const CBIND=\{.*?\};\n", "const CBIND={};\n", h, count=1, flags=re.S)
    assert _js_obj(broken, "CBIND") == {}
    assert _unnamed_blocked_cells(broken), "결속을 통째로 지웠는데 검사가 통과했다"


def test_compare_assembly_uses_the_binding(client):
    """조립 코드가 실제로 CBIND 를 td 에 쓰는가 — 원천만 보면 놓치는 자리다."""
    h = client.get("/compare").get_data(as_text=True)
    assert re.search(r"CBIND\[k\+'\|'\+id\]", h), "CBIND 를 셀 조립에서 안 쓴다"
    assert 'data-claim="' in h.split("function upd()")[1][:2500], \
        "upd() 가 만드는 td 에 data-claim 이 없다"
    # 금지 칸은 복사 버튼이 아니라 표식 붙은 칸으로 그린다
    assert "cell-blocked" in h and "claim-mark" in h


def test_compare_default_axis_actually_draws(client):
    """첫 로드에서 그림이 반쪽이면 안 된다 — **기본 선택**만 고친다(강제는 그대로)."""
    h = client.get("/compare").get_data(as_text=True)
    m = re.search(r"let activeKey='([^']+)';", h)
    assert m, "activeKey 기본값을 못 찾았다"
    key = m.group(1)
    sel = ["comp1", "comp2", "modelc", "lpsocl"]          # 템플릿 기본 체크
    ent = D.CANONICAL_ENTRY
    cnt = {}
    for cid in sel:
        e = ent.get((key, cid)) or {}
        if e.get("comparison_group") and e.get("status") == "canonical":
            cnt[e["comparison_group"]] = cnt.get(e["comparison_group"], 0) + 1
    assert cnt, f"기본 축 {key} 에 canonical 묶음이 없다"
    keep = max(cnt.values())
    assert keep >= 3, f"기본 축 {key} 는 기본 선택에서 {keep}/4 만 남는다 — 첫 그림이 반쪽이다"
    # ⛔ 강제 장치는 그대로여야 한다 (완화 금지)
    assert "splitByGroup" in h and "domGroup" in h


# ══════════════════════════════════════════════════════════════════════════
# metric 라벨·단위는 원장에서 온다
# ══════════════════════════════════════════════════════════════════════════
def test_metric_meta_takes_units_from_the_registry():
    mm = D.metric_meta()
    reg_units = {e["metric"]: e.get("unit") for e in C.registry()["entries"]
                 if e.get("metric") and e.get("unit")}
    missing = [m for m, u in reg_units.items() if not mm.get(m, {}).get("unit")]
    assert not missing, f"원장에 단위가 있는데 화면이 빈칸으로 둔다: {missing}"
    # SDCP 원시 키가 라벨로 풀려야 한다
    k = "SDCP_Eads_eV__ptfe_c10_Nitop"
    assert mm[k]["label"] != k and mm[k]["unit"] == "eV"


def test_metric_meta_does_not_invent_metrics():
    """⛔음성: 레지스트리에 없는 metric 이 화면 열로 생기면 안 된다."""
    mm = D.metric_meta()
    known = {e.get("metric") for e in C.registry()["entries"]}
    assert set(mm) <= known
    # 규칙 밖 키는 **꾸며내지 않고** 키를 그대로 돌려준다
    assert D._derive_metric_label("WHATEVER_key", "") == ("WHATEVER_key", "", "WHATEVER_key")
