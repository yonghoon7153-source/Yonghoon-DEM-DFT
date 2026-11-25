#!/usr/bin/env python3
"""test_sdcp_wave1.py — /sdcp 화면의 **필수 회귀**.

전부 음성 경로가 있다 — "표가 그려진다" 가 아니라 **틀린 값을 내보내는지**를 본다.
이 화면의 위험은 하나로 모인다: *basin 이 어긋난 값을 멀쩡한 값처럼 보이게 하는 것.*

    pytest webapp/tests/test_sdcp_wave1.py -q

⛔ 이 파일이 보증하지 못하는 것
  · 계산 자체의 정확성 (VASP 결과의 참·거짓).
  · basin 벌점 50 meV 의 물리적 타당성 — 그건 4점 추정이고 카드에 한계가 적혀 있다.
  · 화면 디자인.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import data as D  # noqa: E402
from app import app  # noqa: E402

RAW = json.loads((ROOT / "db" / "properties" / "sdcp_wave1_results.json")
                 .read_text(encoding="utf-8"))


#: 화면에 **단정형으로** 나오면 안 되는 철회된 주장들.
#:   ⚠ 부호 규약("음수일수록 잘 붙는다")은 교과서라 넣지 않는다 — 금지 대상은 단정이다.
FORBIDDEN_CLAIMS = (
    "초기조건과 무관하게 재현",   # 회신 P 5번 — 입력 INCAR 미회수라 독립재현 증명 불가
    "무선호",                     # 마감문서 금지어 — 판정바닥(30 meV) 아래는 판정이 아니다
    "O···Li 2.09", "2.09 Å",      # 2026-08-29 철회 (실측 4.88–5.39 Å)
    "술포네이트가 앵커링",        # 마감문서 금지어 — 기전 근거 없음
)

#: 금지 문맥 표지. 이 중 하나가 주변에 있으면 그 출현은 **주장이 아니라 금지**다.
#:
#: ⚠ 2026-09-07 — 이 목록은 `canonical.PROHIBITION_MARKS` 의 **사본**이고, 지금은
#:   그보다 **좁다**(⚠ · "가/이 아니라" · "쓸 수 없다" · RETRACTED · "무효" ·
#:   "인용 불가" 등이 여기 없다). 즉 같은 문장이 /sdcp 에서는 금지로 안 읽히고 다른
#:   화면에서는 읽힌다 — 회신 AW P0-2(2026-09-05)가 "여러 화면이 같은 어휘를 써야
#:   의미가 있다" 며 canonical 로 모으라고 한 바로 그 상황이다.
#:   ⛔ 여기서 임의로 합치지 않는다. 합치면 이 화면의 검사가 **느슨해지고**(표지가
#:   늘어나 금지로 읽히는 문맥이 많아진다), 어느 쪽이 /sdcp 마감문서에 맞는지는
#:   과학·편집 판정이라 사람이 정할 일이다. 대신 아래 시험이 **위험한 방향의
#:   드리프트**(여기에만 표지가 늘어 다른 화면보다 느슨해지는 것)를 막는다.
#: ✅ 2026-09-07 해소 — 사본을 없앴다. 정본이 `canonical` 에 **두 벌 나란히** 있고
#:   (`PROHIBITION_MARKS` 넓음 · `PROHIBITION_MARKS_STRICT` 좁음), 좁다는 사실은
#:   아래 `test_strict_marks_stay_a_proper_subset` 가 지킨다.
from webapp.canonical import (PROHIBITION_MARKS,          # noqa: E402
                              PROHIBITION_MARKS_STRICT)
_PROHIBITION_MARKS = PROHIBITION_MARKS_STRICT


def _is_prohibition(ctx: str) -> bool:
    """문맥에 금지 표지가 있나. 없으면 그 문장은 주장으로 읽힌다."""
    return any(m in ctx for m in _PROHIBITION_MARKS)


def test_strict_marks_stay_a_proper_subset():
    """⛔음성: `/sdcp` 의 좁은 표지 집합이 **넓은 쪽과 같아지면 안 된다.**

    검사는 "숫자 주변에 표지가 없으면 그 출현은 **주장**" 으로 돈다 ⇒ 표지가 **늘면
    검사가 느슨해진다.** 마감문서인 `/sdcp` 는 제일 엄격해야 하므로 좁은 쪽을 쓴다.
    사본을 없애면서 생긴 새 위험이 **"정리하다 하나로 합치는 것"** 이라 그것만 막는다.
    """
    strict, broad = set(PROHIBITION_MARKS_STRICT), set(PROHIBITION_MARKS)
    assert strict < broad, (
        "좁은 표지 집합이 넓은 쪽의 **진부분집합**이 아니다. 같아졌다면 /sdcp 검사가 "
        f"느슨해진 것이다. strict−broad={sorted(strict - broad)} · "
        f"broad−strict={sorted(broad - strict)}")
    # 넓은 쪽에만 있는 대표 표지가 /sdcp 에서 금지로 안 읽히는지 실물로 확인
    assert not _is_prohibition("이 값은 RETRACTED 다"), \
        "RETRACTED 는 넓은 쪽 전용인데 /sdcp 가 금지로 읽었다 — 두 집합이 새고 있다"
    assert _is_prohibition("⛔ 인용 금지"), "양성: 좁은 집합도 제 일은 한다"


def _html():
    return app.test_client().get("/sdcp").data.decode()


def test_route_renders():
    assert app.test_client().get("/sdcp").status_code == 200


def test_shared_doc_routes_unaffected():
    """doc.html 에 표를 얹었다 — data 를 안 넘기는 라우트가 깨지면 안 된다."""
    c = app.test_client()
    for url in ("/methods", "/todo"):
        assert c.get(url).status_code == 200


def test_delta_e_matches_raw_energies():
    """ΔE 는 화면에서 계산된다 — 원자료 총에너지와 어긋나면 안 된다."""
    rows = D.sdcp_wave1_rows()["dE"]
    by = {}
    for j in RAW["jobs"]:
        by.setdefault((j["fragment"], j["seed"]), {})[j["pose"]] = j
    for r in rows:
        d = by[(r["fragment"], r["seed"])]
        want = (d["Nitop"]["E_total_eV"] - d["Litop"]["E_total_eV"]) * 1000
        assert abs(r["dE_meV"] - want) < 0.051, r


def test_ptfe_dimer_two_seeds_agree():
    """★ 이 데이터셋의 신뢰 근거 — 두 시드가 0.1 meV 로 일치한다."""
    v = {r["seed"]: r["dE_meV"] for r in D.sdcp_wave1_rows()["dE"]
         if r["fragment"] == "ptfe_dimer"}
    assert set(v) == {"pm1", "net4"}
    assert abs(v["pm1"] - v["net4"]) <= 0.5, v


def test_basin_mismatch_is_flagged_not_hidden():
    """⛔음성: basin 이 어긋난 잡을 **지우면** 안 된다 — 경고와 함께 보여야 한다.

    지우면 "안 돌린 계산" 으로 보여 3일짜리 배치를 다시 돌리게 된다.
    """
    bad = [j for j in RAW["jobs"] if not j["basin_consistent"]]
    assert bad, "전제: 어긋난 잡이 실제로 있다"
    html = _html()
    for j in bad:
        assert j["job"] in html, f"어긋난 잡이 화면에서 사라졌다: {j['job']}"
    assert "다른 basin" in html


def test_no_basin_correction_applied():
    """⛔음성: 50 meV 벌점을 **빼서** 값을 고치면 안 된다 (측정이 아니라 가정이 된다).

    ⛔⛔ 2026-09-05 회신 AW P0-1(3/3) — 종전 이 시험은 `for j in RAW["jobs"]:
      assert f"{E_ads:.3f}" in html` 로 **raw E_ads 전건 노출을 강제**했다.
      그런데 `sdcp_wave1_citable.json` 은 절대 E_ads 를 HOLD 로, doped 를 전항
      비인용으로 잠근다 — 즉 **시험이 정본의 인용 금지와 정면충돌했고**, 화면을
      고치면 시험이 깨지는 구조였다.
      ⇒ 지금 시험하는 것은 "전부 보여라" 가 아니라 **"보여준 값은 원자료 그대로여야
        한다"** 다. 무엇을 보여줄지는 지위가 정하고, 이 시험은 관여하지 않는다.
    """
    html = _html()
    shown = [j for j in RAW["jobs"] if f"{j['E_ads_eV']:.3f}" in html]
    assert shown, "전제: 감사 추적을 위해 최소 일부는 (접힌 절에라도) 남아 있다"
    for j in shown:
        # 화면에 있다면 원자료와 한 글자도 달라선 안 된다 — 보정·반올림 금지
        assert f"{j['E_ads_eV']:.3f}" in html, j["job"]


def test_status_is_shown_per_row_not_only_in_a_banner():
    """★ AW P0-1(2/3)·P0-2 — 지위가 **행마다** 붙어야 한다.

    상단 배너 하나로는 부족하다: 스크롤하면 배너는 사라지고 값만 남는다.
    """
    html = _html()
    r = D.sdcp_wave1_rows()
    for x in r["dE"]:
        assert x["status"] in html, f"ΔE 행의 지위가 화면에 없다: {x}"
    for j in r["jobs"]:
        assert j["status"] in html, f"E_ads 행의 지위가 화면에 없다: {j['job']}"


def test_retracted_claims_are_not_present_tense():
    """⛔음성 AW P0-1 — 철회된 주장이 현재형으로 되살아나면 안 된다.

    이 셋은 마감문서의 금지 서술이거나 그 직접 파생이다. 화면 문장이 이것을
    단정형으로 쓰면, 배너를 아무리 붙여도 독자는 주장을 읽는다.

    ⚠ 부호 규약 자체("E_ads 는 음수일수록 잘 붙는다")는 교과서라 금지하지 않는다.
    금지하는 것은 **철회된 단정**이다 — 정의를 지위와 묶지 않고 값 옆에 두면
    독자는 그것을 그 값에 대한 주장으로 읽는다(AW P0-1 실측).

    ⛔ 그리고 **부정문을 주장으로 세면 안 된다.** 화면이 "'무선호' 가 아니다" 라고
    금지하는 문장도 substring 검사에는 걸린다 — 그러면 올바른 문장을 지우게 된다.
    ⇒ 금지어 **주변 문맥**(앞뒤 각 110자)에 금지 표지가 있으면 그 출현은
      주장이 아니라 금지로 본다. 실물 편집 관행이 그렇다 — 철회된 주장은 언제나
      ⛔ 블록이나 "…라고 쓰지 않는다" 문장 안에서만 등장한다.
    ⚠ 뒤쪽 24자만 보는 좁은 창은 부족했다 (실측: "('무선호' **포함**) · n=1 외삽"
      처럼 금지 표지가 앞에 오는 경우를 놓친다).
    """
    html = _html()
    for bad in FORBIDDEN_CLAIMS:
        i = 0
        while (i := html.find(bad, i)) != -1:
            ctx = html[max(0, i - 110): i + len(bad) + 110]
            assert _is_prohibition(ctx), (
                f"철회된 주장이 **단정형으로** 화면에 있다: {bad!r}\n   문맥: {ctx!r}")
            i += len(bad)


def test_negation_guard_itself_works():
    """⛔음성: 문맥 판정기가 주장과 금지를 실제로 **가르는지** 본다.

    이게 없으면 `_is_prohibition` 이 항상 True 를 돌려줘도 위 시험이 통과한다 —
    즉 아무것도 안 잡는 시험이 초록으로 남는다.
    """
    assert not _is_prohibition("이 계는 무선호 다. 값은 +9.3 meV.")
    assert _is_prohibition("⛔ '무선호' 라고 쓰지 않는다 — 판정바닥 아래는 판정이 아니다")
    assert _is_prohibition("철회된 표현('무선호' 포함) · n=1 외삽")


def test_prohibition_vocabulary_does_not_drift_looser_than_the_shared_one():
    """⛔음성: 이 파일의 표지 사본이 **공용 어휘보다 느슨해지지** 않게 막는다.

    회신 AW P0-2(2026-09-05)는 표지 목록을 `canonical.PROHIBITION_MARKS` 한 곳으로
    모으라고 했다. 이 파일에는 아직 사본이 남아 있고 지금은 공용 어휘보다 **좁다**
    (= 이 화면이 더 엄격하다). 좁은 건 안전한 방향이라 그대로 두되, 반대 방향
    — 여기에만 표지를 더해 /sdcp 만 통과시키는 드리프트 — 는 막아야 한다.

    ⛔ 이 시험이 못 하는 것: 두 어휘가 **같아야 하는지**는 판정하지 않는다.
      그건 사람이 정할 마감문서 판정이다. 여기서는 방향만 잠근다.
    """
    import canonical as C

    local, shared = set(_PROHIBITION_MARKS), set(C.PROHIBITION_MARKS)
    extra = sorted(local - shared)
    assert not extra, (
        f"이 파일에만 있는 금지 표지 {extra} — /sdcp 에서만 금지로 읽히고 다른 화면에서는 "
        "주장으로 읽힌다. 표지를 늘릴 거면 canonical.PROHIBITION_MARKS 에 넣을 것 "
        "(회신 AW P0-2).")
    # 사본이 정말 좁은 상태인지도 기록해 둔다 — 좁힘이 사라지면(=같아지면) 사람이
    # 사본을 지우고 canonical 을 쓰면 된다는 신호다.
    assert local <= shared


def test_doped_is_blocked_everywhere():
    """⛔음성: doped 는 마감(2026-08-28)이라 **어느 표에서도** CITABLE 이 아니다."""
    r = D.sdcp_wave1_rows()
    for x in r["dE"]:
        if x["fragment"] == "sdcp_doped":
            assert x["status"] == "BLOCKED", x
    for j in r["jobs"]:
        if j.get("fragment") == "sdcp_doped":
            assert j["status"] == "BLOCKED", j["job"]


def test_absolute_eads_never_citable():
    """⛔음성: 절대 E_ads 는 회신 O 로 보류 — 어떤 조각도 CITABLE 이 될 수 없다."""
    for j in D.sdcp_wave1_rows()["jobs"]:
        assert j["status"] in ("HOLD", "BLOCKED"), (j["job"], j["status"])


def test_missing_ledger_locks_everything(monkeypatch):
    """⛔음성 fail-closed: 인용 원장을 못 읽으면 **전부 BLOCKED** 다.

    "판정 못 함" 이 "통과" 로 바뀌면 게이트가 없는 것과 같다.
    """
    monkeypatch.setattr(D, "DB", ROOT / "db" / "__no_such_dir__")
    r = D.sdcp_wave1_rows()
    assert r["gate"]["source_missing"] is True
    assert all(x["status"] == "BLOCKED" for x in r["dE"]), r["dE"]
    assert all(j["status"] == "BLOCKED" for j in r["jobs"])


def test_basin_mismatch_outranks_the_fragment_level_reason():
    """⛔음성: basin 이 갈린 행에 **조각 단위 사유**가 그대로 붙으면 안 된다.

    실측 (2026-09-05): `sdcp_neutral / net4` 는 −40.7 meV 인데 사유가
    "판정바닥 30 meV 아래" 였다 — **40.7 > 30 이다.** 그 행이 못 쓰이는 진짜 이유는
    basin 이 B/A 로 갈린 것이고, 크기는 오히려 바닥을 넘었다. 틀린 이유를 달면
    독자는 "30 만 넘기면 된다" 로 읽고, 다음 계산을 그 기준으로 설계한다.
    """
    r = D.sdcp_wave1_rows()
    mixed = [x for x in r["dE"] if not x["basin_same"]]
    assert mixed, "전제: basin 이 갈린 행이 실제로 있다"
    for x in mixed:
        assert x["status"] == "BLOCKED", x
        assert "basin" in x["why"], x
        # ⛔ 핵심: 바닥을 **넘은** 값에 "바닥 아래" 라고 적지 않는다
        if abs(x["dE_meV"]) >= 30.0:
            head = x["why"].split("[조각 판정:")[0]
            assert "판정바닥 30 meV 아래" not in head, (
                f"바닥을 넘은 값({x['dE_meV']:+.1f} meV)에 '바닥 아래' 사유가 붙었다: {x}")


def test_invalid_delta_e_not_counted_as_valid():
    """⛔음성: basin 이 갈린 ΔE 가 유효 집계에 들어가면 안 된다."""
    r = D.sdcp_wave1_rows()
    assert r["n_valid"] < r["n_dE"], "전제: 무효 행이 있다"
    assert r["n_valid"] == sum(1 for x in r["dE"] if x["valid"])
    for x in r["dE"]:
        assert x["valid"] == (x["basin_pair"].split("/")[0]
                              == x["basin_pair"].split("/")[1])


def test_missing_or_broken_json_says_so_instead_of_vanishing(monkeypatch, tmp_path):
    """⛔음성: 원자료를 못 읽어도 예외로 안 죽고, **못 읽었다고 화면이 말한다.**

    종전 시험은 `sdcp_wave1_rows() == {}` 만 봤다("quietly"). 그런데 `{}` 는
    doc.html 의 `{% if data.jobs %}` 에 걸려 표가 **통째로 사라지고**, 사라진 표는
    "잡이 없다"로 읽힌다. 그리고 파일이 **깨진** 경우는 아예 검사 밖이라
    맨몸 `json.loads` 가 `/sdcp` 를 **500** 으로 만들고 있었다 (2026-09-07 실측).

    ⇒ 계약을 좁힌다: 예외 없음 + 사유를 실어 나름 + 화면이 그 사유를 적음.
      값·지위 판정은 그대로다 — 못 읽었을 때의 **말**만 달라진다.
    """
    for scenario, path in (("없는 파일", ROOT / "db" / "properties" / "__none__.json"),
                           ("깨진 파일", tmp_path / "broken.json")):
        if scenario == "깨진 파일":
            path.write_text("{ not json", encoding="utf-8")
        monkeypatch.setattr(D, "SDCP_WAVE1_JSON", path)
        r = D.sdcp_wave1_rows()                      # ① 예외로 죽지 않는다
        assert r.get("unreadable"), f"{scenario}: 못 읽은 사유를 안 싣는다 — {r!r}"
        assert r["jobs"] == [] and r["dE"] == [], f"{scenario}: 없는 행을 지어낸다"
        assert r["n_citable_dE"] == 0, f"{scenario}: 못 읽었는데 인용 가능 행을 센다"
        rv = app.test_client().get("/sdcp")           # ② 500 이 아니라 사유를 실은 화면
        assert rv.status_code == 200, f"{scenario}: /sdcp 가 {rv.status_code}"
        body = rv.data.decode()
        assert "못 읽" in body, f"{scenario}: 화면이 못 읽은 사실을 안 적는다"
        assert "잡이 없어서가 아니라" in body, (
            f"{scenario}: 빈 표가 '잡이 없다' 로 읽히는 것을 막는 문구가 없다")
