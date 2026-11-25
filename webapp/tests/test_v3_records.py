"""v3 묶음 H — 기록 화면(/log · /todo · /requests · /notes · /files).

⚠ 검사마다 **음성 경로**를 같이 둔다. 양성만 있는 검사는 통과해도 아무것도 보증하지
   못한다 — 이 repo 가 이미 겪은 실패형이다(vasp 번들 v2 selftest).
⛔ 이 파일이 **못 하는 것**: 값의 타당성을 판정하지 않는다. 화면이 원장과 어긋나는지만 본다.
"""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A                                          # noqa: E402
import canonical as C                                    # noqa: E402
import data as D                                         # noqa: E402
import records_view as RV                                # noqa: E402


@pytest.fixture()
def cl():
    A.app.config["TESTING"] = True
    return A.app.test_client()


def _text(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


# ── ① 마감된 축 표식 (P0 — 살아 있는 누출) ──────────────────────────────────


def test_records_view_selftest_passes():
    """도구 자체의 selftest(음성 경로 포함)가 통과한다."""
    assert RV._selftest() == 0


def test_closed_axis_vocabulary_is_derived_not_typed():
    """어휘가 **원장에서** 나온다: 결속 id 는 인용위험 원장 어휘 안에 있어야 한다."""
    claims = RV.closed_axis_claims()
    assert claims, "비준된 마감 카드가 있는데 어휘가 비었다"
    vocab = C.hazard_ids()
    assert all(c["id"] in vocab for c in claims), "원장에 없는 id 로 결속하면 유령 결속이다"


def test_closed_axis_marks_the_requests_leak(cl):
    """/requests 의 '✅ 쓸 수 있는 것: 저온 구간 Ea = 0.2241' 에 표식이 붙는다.

    이게 이 묶음의 P0 다 — 마감 결정이 축 전체를 닫았는데(“0.222 eV 포함”) 스캐너
    어휘는 레지스트리 수 둘뿐이라 화면이 **초록인 채로** 금지된 수를 권했다.
    """
    html = cl.get("/requests").data.decode()
    assert "0.2241" in html, "전제: 원문에 그 수가 아직 있다 (없어졌으면 이 검사를 옮겨라)"
    # 0.2241 이 나오는 자리마다 결속 span 안이어야 한다
    for m in re.finditer(r"0\.2241", html):
        head = html[max(0, m.start() - 400):m.start()]
        assert "claim-flag" in head.rsplit("</span>", 1)[-1] or "claim-flag" in head[-400:], \
            "0.2241 이 결속 밖에서 렌더된다"


@pytest.mark.parametrize("url,needle", [
    ("/requests", "0.2241"),
    ("/todo", "0.222"),
    ("/api/handoff/b2o3_arrhenius_curvature_2026_08_23", "0.222"),
])
def test_closed_axis_surfaces_name_the_hazard(cl, url, needle):
    """세 표면 전부 마감 축의 위험 id 를 **화면에서 이름 댄다**."""
    r = cl.get(url)
    assert r.status_code == 200
    body = r.data.decode()
    if url.startswith("/api/"):
        body = json.loads(body)["html"]
    assert needle in body, "전제: 그 수가 아직 화면에 있다"
    assert "HZ-b2o3-md-ea" in body, f"{url} 이 마감 축을 이름 대지 않는다"


def test_closed_axis_does_not_mark_other_systems():
    """⛔음성: **다른 계**의 같은 수에는 표식을 안 붙인다.

    실측 오탐 셋을 픽스처로 박는다 — 값만 보면 못 가른다.
    """
    for frag in ('<h3>Nd σ-drop</h3><p>Ea 0.224 불변</p>',
                 '<h3>[Zhu20] 규약 불일치</h3><p>LiCl 본문 +0.977 vs 엑셀 1.335</p>',
                 '<h3>LPSOCl β 표</h3><p>600 K β 0.371</p>'):
        assert "claim-flag" not in RV.mark_closed_axis(frag), frag


def test_closed_axis_fails_closed_without_ledger(tmp_path):
    """⛔음성: 원장이 없으면 **조용히 통과하지 않고** 어휘가 0 이 된다(원문 그대로)."""
    assert RV.closed_axis_claims(root=str(tmp_path)) == []
    frag = "<h3>b2o3</h3><p>0.222 eV</p>"
    assert RV.mark_closed_axis(frag, root=str(tmp_path)) == frag


def test_closed_axis_never_marks_a_live_canonical_value():
    """⛔음성: 살아있는 정본(b2o3 밴드갭 1.9671 등)은 어휘에 들어가지 않는다."""
    reg = C.registry()
    live = {round(float(e["value"]), 12) for e in reg.get("entries", [])
            if e.get("status") == "canonical" and e.get("citable") is not False
            and isinstance(e.get("value"), (int, float))}
    got = {round(float(c["text"]), 12) for c in RV.closed_axis_claims()}
    assert not (got & live), f"살아있는 정본에 마감 표식이 붙는다: {sorted(got & live)}"


# ── ② /log SDCP 카드 — 원본 explainer 의 금지 표현 ──────────────────────────

#: explainer(kb/results/sdcp_wave1_explainer_2026_08_25.md)가 **쓰지 말라고 적은** 말.
SDCP_FORBIDDEN = ("게이트 오탐 30→0", "basin 벌점", "0.1 meV 일치", "0.1 meV 정확도")


def test_log_sdcp_card_uses_the_source_verdict(cl):
    """카드가 원본 판정문을 쓴다 — 30→0 은 게이트가 아니라 INCAR 불일치다."""
    body = _text(cl.get("/log").data.decode())
    for bad in SDCP_FORBIDDEN:
        assert bad not in body, f"explainer 가 금지한 표현이 화면에 있다: {bad}"
    assert "0/30 → 17/30" in body, "게이트 실제 판정(0/30 → 17/30)이 없다"
    assert "진단값" in body and "측정 아님" in body, "basin ~50 meV 는 진단값이지 측정이 아니다"


# ── ③ 저널 타임라인 — 정렬·묶음·갭 ─────────────────────────────────────────


def test_journal_sorted_by_ts_not_file_order():
    """파일 줄 순서가 아니라 `ts` 로 정렬한다 (journal.jsonl 자체가 시간순이 아니다)."""
    groups = RV.journal_groups(A._load_journal(), A.JOURNAL_GAPS)
    dates = [g["date"] for g in groups if g["date"]]
    assert dates == sorted(dates, reverse=True)
    for g in groups:
        ts = [str(e.get("ts") or "") for e in g["items"]]
        assert ts == sorted(ts, reverse=True), g["date"]


def test_journal_keeps_entries_without_ts():
    """⛔음성: 시각이 없는 줄을 **버리지 않는다** (없는 값을 지우면 기록이 준다)."""
    ent = [{"ts": "2026-09-08T10:00", "text": "a"}, {"ts": "", "text": "b"},
           {"text": "c"}]
    groups = RV.journal_groups(ent)
    assert sum(g["n"] for g in groups) == 3
    assert groups[-1]["date"] == "" and groups[-1]["n"] == 2


def test_journal_gap_is_shown_and_not_invented():
    """빈 구간은 화면에 나오고, **주석이 없는 구간은 수를 지어내지 않는다.**"""
    body = _text(cl_html := A.app.test_client().get("/log").data.decode())
    assert "기록 없음" in body, "빈 구간이 화면에 없다"
    assert "커밋 806" in body, "실측 주석이 붙은 구간이 있다"
    # ⛔음성: 갭 줄 개수 == journal_groups 가 낸 gap 개수 (화면이 더 만들지 않는다)
    n_screen = cl_html.count('class="jgap')
    n_data = sum(1 for g in RV.journal_groups(A._load_journal(), A.JOURNAL_GAPS) if g["gap"])
    assert n_screen == n_data


def test_journal_kind_vocabulary_folds_display_only():
    """⛔음성: 모르는 kind 는 표시층이 **원문 그대로** 낸다 (임의로 '기타' 로 접지 않는다)."""
    assert RV.kind_label("webapp") == "도구"
    assert RV.kind_label("전혀-모르는-종류") == "전혀-모르는-종류"
    # 원문 journal.jsonl 은 안 고친다 — 파일 안 kind 어휘가 표시 어휘보다 넓어야 정상
    raw = {str(e.get("kind") or "") for e in A._load_journal()}
    assert len(raw) > len(RV.KIND_ORDER)


# ── ④ handoff 격자 ──────────────────────────────────────────────────────────


def test_handoffs_sorted_by_date_and_none_dropped():
    hs = A._handoffs()
    n_files = len(list((D.KB / "results").glob("*.md")))
    assert len(hs) == n_files, "handoff 문서를 화면에서 빠뜨렸다 (접는 것과 지우는 것은 다르다)"
    keys = [h["date"] or "0000-00-00" for h in hs]
    assert keys == sorted(keys, reverse=True)


def test_handoff_missing_id_returns_json_not_html(cl):
    """⛔음성: 없는 hid 도 **JSON** 으로 답한다 (모달의 r.json() 이 던져 굳던 자리)."""
    r = cl.get("/api/handoff/does-not-exist-2026")
    assert r.status_code == 404
    assert r.is_json and "error" in r.get_json()


# ── ⑤ /files — 인용위험·정책·날짜 ───────────────────────────────────────────


def test_gallery_carries_hazard_and_policy():
    """갤러리 항목이 인용위험·정책 판정을 **같이** 싣는다."""
    fs = D.gallery_files()
    haz = {f["rel"] for f in fs if f.get("hazard")}
    assert haz, "인용위험 원장에 있는 파일이 갤러리에 하나도 표시되지 않는다"
    blocked = {f["rel"] for f in fs if f.get("policy")}
    assert blocked, "artifact_policy 가 막는 파일이 갤러리에 표시되지 않는다"
    # ⛔음성: 정책이 허용하는 평범한 파일에는 policy 가 붙지 않는다
    # "평범한 파일" 의 경계는 정책 모듈 자신의 판정(`is_governed`)을 쓴다. 2026-09-23 까지는
    # 접두어 두 개를 여기 복사해 두었는데 정책 쪽 `GOVERNED_PREFIXES` 는 셋이었다
    # (`db/properties/oxidation_stability_cascade` 누락). 그 파일들이 최근 수정돼 갤러리 앞 50개에
    # 들어오자, **정상적으로 막힌** cascade 파일을 "평범한데 막혔다" 로 읽어 빨간불이 났다.
    import artifact_policy as AP
    plain = [f for f in fs if not AP.is_governed(f["rel"])]
    assert plain and all(f["policy"] is None for f in plain[:50]), \
        [f["rel"] for f in plain[:50] if f["policy"] is not None]


def test_hazard_badge_reaches_the_screen(cl):
    body = cl.get("/files").data.decode()
    assert 'class="hzb' in body and 'class="polb' in body


def test_superseded_files_are_folded_not_deleted(cl):
    """옛 판은 기본 목록에서 빠지되 `?old=yes` 에 **그대로 있다** (지운 게 아니다)."""
    default = {f["rel"] for f in D.gallery_files()}
    old = {f["rel"] for f in D.gallery_files(old="yes")}
    assert old, "SUPERSEDED/RETRACT 파일이 하나도 안 잡힌다"
    assert not (default & old), "옛 판이 기본 목록에 섞여 있다"
    # 디스크에는 그대로 있어야 한다
    for rel in old:
        assert (D.ROOT / rel).exists()
    assert cl.get("/files?old=yes").status_code == 200


def test_gallery_day_comes_from_git_not_checkout():
    """날짜 출처가 **git 커밋일**이다 — 체크아웃일(mtime)이면 한 날짜에 뭉친다."""
    fs = D.gallery_files()
    days = {f["day"] for f in fs if f["day"]}
    assert len(days) > 5, f"날짜가 {len(days)}종 — 체크아웃일로 뭉쳐 있다"
    gm = D._git_commit_days()
    for f in fs[:80]:
        assert f["day"] == gm.get(f["rel"], ""), f["rel"]


def test_gallery_day_unknown_is_not_filled_with_today():
    """⛔음성: 커밋 이력에 없는 파일을 **오늘로 채우지 않는다**."""
    fake = [{"rel": "x", "day": ""}, {"rel": "y", "day": "2026-09-08"}]
    out = D.gallery_days(fake)
    assert out[-1]["day"] == "날짜 미상"
    assert out[-1]["n"] == 1


def test_files_facets_survive_each_other(cl):
    """탭을 눌러도 다른 조건이 조용히 사라지지 않는다 (qs 매크로 한 곳에서 만든다)."""
    body = cl.get("/files?kind=image&folder=db/structures&used=yes").data.decode()
    links = re.findall(r'href="(/files\?[^"]+)"', body)
    assert links
    for h in links:
        assert "kind=" in h and "folder=" in h and "used=" in h and "cmt=" in h and "old=" in h


# ── ⑥ 결속 계약 (BG ②) — 재편으로 떨어뜨리지 않았는지 ───────────────────────


@pytest.mark.parametrize("url", ["/log", "/todo", "/requests", "/notes", "/files"])
def test_records_surfaces_have_no_unbound_claims(cl, url):
    """기록 화면 다섯이 결속 검사를 통과한다 (재편 뒤에도)."""
    html = cl.get(url).data.decode()
    res = C.scan_claim_bindings(html)
    unbound = res.get("unbound") if isinstance(res, dict) else res
    assert not unbound, f"{url}: {unbound}"
