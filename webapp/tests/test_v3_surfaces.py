# -*- coding: utf-8 -*-
"""전 정의역 표면 검사 — 렌더 · 게이트 · 결속 (검증 ①, 2026-09-09).

무엇을 보나
  ① 인자 없는 GET 라우트 **전부** + 동적 라우트를 **디스크의 실물 인자로 전개**한
     정의역(조성 14 · 개념 · 발표덱 · handoff 95 · litdb 논문 218 · property 181)이
     전부 200 이거나, **선언된 게이트**로 막혀 있다.
  ② 그 정의역 어디에도 미결속(`unbound`)·유령 결속(`dangling`)이 없다.
  ③ ②의 0 이 **선언 덕분**인지 **글자가 없어서**인지 표면마다 가른다 — 결속이 있는
     화면은 `data-claim` 선언만 지웠을 때 반드시 미결속으로 떨어져야 한다.

왜 새로 쓰나 (test_webapp.py 와 겹치지 않는 부분)
  · 기존 `test_each_surface_zero_comes_from_declarations_not_from_absence` 의 음성시험
    표면은 **손으로 적은 10개**다. 손 목록은 반드시 낡는다 — 여기서는 정의역을
    **자동 열거**해 결속이 있는 **모든** 표면을 음성시험한다(실측 31개).
  · 기존 결속 검사의 동적 라우트는 대표 인자 1–2개(`DYNAMIC_FIXTURES`)다. 여기서는
    handoff 95 · 논문 218 · 조성 14 를 **전건** 민다.

⛔ 이 시험이 **못 하는 것** (덮인 줄 알면 안 되는 것)
  · **JSON 원자료는 결속 검사가 성립하지 않는다.** `scan_claim_bindings` 는 HTML
    텍스트 노드를 훑는다 — `/api/property/<n>` 은 db JSON 을 그대로 내보내므로
    `data-claim` 을 달 자리가 없다. 이 시험은 그 경로의 **status code 만** 본다.
  · 태그 **속성** 안의 값(`title=`)과 JS 가 나중에 그리는 DOM 은 못 본다
    (`scan_claim_bindings` 자체의 한계).
  · POST/PATCH/DELETE 는 안 민다 — 읽기 표면만이다.
  · 값이 **물리적으로 맞는지**는 여전히 검사하지 않는다.
"""
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as A          # noqa: E402
import canonical as C    # noqa: E402
import data as D         # noqa: E402

#: 결속 선언만 지운다 — 텍스트는 그대로. 음성시험의 도구다.
#: ⚠ 따옴표 두 종류를 다 받는다 (홑따옴표를 빼먹으면 파이썬 문자열 안의 선언이 안 지워져
#:   음성시험이 조용히 통과한다 — test_webapp.py 가 2026-09-08 에 실제로 겪었다).
_STRIP_DECL = re.compile(r"""\s+data-claim(?:-not)?=(?:"[^"]*"|'[^']*')""")

#: 200 이 아니어도 되는 화면과 **그것을 여는 인자**. 여기 넣는 것은 "봐주세요" 가 아니라
#:   *"이건 fail-closed 게이트이고 이 인자로 열린다"* 는 **검증 가능한 주장**이다 —
#:   아래 시험이 ① 인자 없이 막히고 ② 인자를 주면 열리는지 **둘 다** 확인한다.
_UNLOCK = {
    "/cascade/diagnostic": {
        "param": "view=diagnostic",
        "why": "진단 뷰는 감사용이다. 기본 진입에서 열면 미승인 랭킹이 그냥 화면이 된다 "
               "(fail-closed 게이팅 3종 중 하나 — Codex 가 두 번 잡아 만든 장치다).",
    },
}


def _domain():
    """→ [(url, origin)] — **손 목록을 쓰지 않는다**. 새 화면·새 문서가 자동으로 든다.

    litdb 경로는 `origin="external"` 이다 — 남의 문서라 우리 값 매처를 그대로 대면
    원장이 남의 논문으로 부풀고 "미결속 0" 이 더 그럴듯하게 틀린 수가 된다.
    """
    out = [(str(r), "internal") for r in A.app.url_map.iter_rules()
           if not r.arguments and "GET" in (r.methods or set())
           and not str(r).startswith("/static")]
    out += [(f"/composition/{c}", "internal") for c in sorted(D.COMPOSITIONS)]
    out += [(f"/concept/{c}", "internal") for c in sorted(D.concept_ids())]
    out += [(f"/api/handoff/{p.stem}", "internal")
            for p in sorted((D.KB / "results").glob("*.md"))]
    out += [(f"/talk/{p.stem}", "external")
            for p in sorted((D.LITDB / "talks").glob("*.md")) if not p.stem.startswith("_")]
    papers = [p.stem for p in sorted((D.LITDB / "papers").glob("*.md"))
              if not p.stem.startswith("_")]
    out += [(f"/api/paper/{p}", "external") for p in papers]
    out += [(f"/paper/{p}", "external") for p in papers]
    out += [(f"/api/property/{p.stem}", "internal")
            for p in sorted((D.DB / "properties").glob("*.json"))]
    return sorted(set(out))


def _html_of(rv):
    """→ 스캔 가능한 HTML | "" . 바이너리(pptx)는 **텍스트로 디코드하지 않는다**."""
    mt = rv.mimetype or ""
    if mt == "text/html":
        return rv.get_data(as_text=True)
    if mt == "application/json":
        try:
            d = json.loads(rv.get_data(as_text=True))
        except Exception:                                          # noqa: BLE001
            return ""
        return d.get("html") or "" if isinstance(d, dict) else ""
    return ""


@pytest.fixture(scope="module")
def crawl():
    """정의역을 한 번만 민다 (실측 571 URL · ~45 s). 아래 시험들이 이 결과를 나눠 쓴다."""
    cli = A.app.test_client()
    reg = C.registry()
    claims = C.all_claims(reg=reg)
    rows = []
    for url, origin in _domain():
        rv = cli.get(url)
        row = {"url": url, "origin": origin, "status": rv.status_code,
               "mimetype": rv.mimetype, "body": rv.get_data()}
        html = _html_of(rv) if rv.status_code == 200 else ""
        if html:
            sc = C.scan_claim_bindings(html, claims=claims, reg=reg, origin=origin)
            row["scan"] = sc
            row["html"] = html
        rows.append(row)
    return {"rows": rows, "claims": claims, "reg": reg}


# ── ① 렌더 ────────────────────────────────────────────
def test_every_surface_renders_or_is_a_declared_gate(crawl):
    """전 정의역이 200 이거나 **자기가 게이트라고 말하는** 403 이다.

    ⛔음성: 200 도 아니고 게이트 선언도 없는 응답(404·500·빈 게이트)은 실패다.
    ⚠ 게이트를 "그냥 403 이면 통과" 로 두면 500 을 403 으로 바꿔 숨길 수 있다 —
      그래서 게이트는 **스스로 근거를 대야** 한다(아래 두 시험이 그걸 확인한다).
    """
    bad = []
    for r in crawl["rows"]:
        if r["status"] == 200:
            continue
        if r["url"] in _UNLOCK:
            continue
        if r["status"] == 403 and r["mimetype"] == "application/json":
            continue                                # 근거 검사는 다음 시험이 한다
        bad.append((r["url"], r["status"], r["mimetype"]))
    assert not bad, "200 도 아니고 선언된 게이트도 아닌 표면이 있다:\n" + \
        "\n".join(f"  {u} → {s} ({m})" for u, s, m in bad)


def test_artifact_gate_states_its_reason_and_is_not_a_blanket(crawl):
    """양성+⛔음성: artifact 게이트 403 은 **근거를 대고**, 전체를 덮지 않는다.

    양성 — 막힌 응답은 `artifact`(무엇을 막았나)와 사유 문자열을 같이 낸다.
    ⛔음성 ① — 사유가 비면 실패다. 빈 403 은 "왜 막혔는지 모르는 것" 이고,
      그건 게이트가 아니라 사고다.
    ⛔음성 ② — 막힌 property 가 **전부**면 그건 게이트가 아니라 담요다.
      게이트되지 않은 property 가 실제로 200 으로 나와야 한다.
    """
    props = [r for r in crawl["rows"] if r["url"].startswith("/api/property/")]
    assert props, "전제: /api/property 정의역이 비어 있지 않다"
    gated = [r for r in props if r["status"] == 403]
    assert gated, "전제: fail-closed artifact 게이트가 실제로 걸린 자리가 있다"
    naked = []
    for r in gated:
        try:
            env = json.loads(r["body"].decode("utf-8"))
        except Exception:                                          # noqa: BLE001
            naked.append((r["url"], "JSON 이 아니다"))
            continue
        if not env.get("artifact"):
            naked.append((r["url"], "무엇을 막았는지(artifact) 를 안 적었다"))
        if not str(env.get("error") or env.get("reason") or "").strip():
            naked.append((r["url"], "왜 막았는지 사유가 비어 있다"))
    assert not naked, "근거 없는 403 이 있다 — 게이트는 스스로 이유를 대야 한다: " + str(naked)
    ok = [r["url"] for r in props if r["status"] == 200]
    assert ok, ("property 가 전부 막혔다 — 게이트가 아니라 담요다. "
                "artifact_policy 가 fail-closed 로 넘어갔는지 봐라.")


def test_unlock_declarations_are_true_both_ways(crawl):
    """양성+⛔음성: `_UNLOCK` 선언이 **말뿐이 아닌지**.

    ⛔음성 — 인자 없이 200 이 나오면 게이트가 사라진 것이다(선언이 거짓).
    양성   — 선언한 인자로는 200 이어야 한다(선언이 낡아 못 여는 것도 거짓이다).
    """
    cli = A.app.test_client()
    seen = {r["url"]: r["status"] for r in crawl["rows"]}
    wrong = []
    for url, dec in _UNLOCK.items():
        assert dec.get("why", "").strip(), f"{url}: 게이트 사유가 비었다 (빈 사유 금지)"
        assert url in seen, f"{url}: 없어진 라우트의 게이트 선언이 남아 있다"
        if seen[url] == 200:
            wrong.append((url, "인자 없이 열렸다 — 게이트가 사라졌다"))
        if cli.get(f"{url}?{dec['param']}").status_code != 200:
            wrong.append((url, f"선언한 인자({dec['param']})로도 안 열린다 — 선언이 낡았다"))
    assert not wrong, str(wrong)


# ── ② 결속 ────────────────────────────────────────────
def test_no_unbound_and_no_dangling_across_full_domain(crawl):
    """전 정의역에 미결속·유령 결속이 없다.

    ⚠ 이 시험 **하나만으로는 아무것도 보증하지 못한다** — `unbound == 0` 은 지표가
      아니다(자동 결속 경로가 지나가면 구조적으로 0 이 된다). 아래 두 음성시험과
      **같이** 읽어야 한다.
    """
    unbound, dangling = [], []
    for r in crawl["rows"]:
        sc = r.get("scan")
        if not sc:
            continue
        unbound += [(r["url"], c["id"], ctx[:120]) for c, ctx in sc["unbound"]]
        if sc["dangling"]:
            dangling.append((r["url"], sc["dangling"]))
    assert not unbound, "결속 없는 철회·금지 주장:\n" + \
        "\n".join(f"  {u} · {i}\n      …{x}…" for u, i, x in unbound)
    assert not dangling, "레지스트리에 없는 claim id 를 선언한다 (유령 결속): " + str(dangling)


def test_every_bound_surface_drops_when_declarations_are_stripped(crawl):
    """⛔음성 **표면별·자동**: 결속이 있는 화면은 선언을 지우면 반드시 떨어진다.

    기존 시험은 이 검사를 **손으로 적은 10개 표면**에만 했다. 여기서는 정의역 전체에서
    `bound > 0` 인 표면을 **찾아서** 전부 민다(실측 31개 — handoff 15 · 조성 3 ·
    개념 4 · litdb 1 · 화면 8). 안 떨어지는 화면이 있으면 그 화면의 초록은
    결속 때문이 아니다.
    """
    reg, claims = crawl["reg"], crawl["claims"]
    tested, nodrop = 0, []
    for r in crawl["rows"]:
        sc = r.get("scan")
        if not sc or not sc["bound"]:
            continue
        tested += 1
        naked = C.scan_claim_bindings(_STRIP_DECL.sub("", r["html"]),
                                      claims=claims, reg=reg, origin=r["origin"])
        if len(naked["unbound"]) < len(sc["bound"]):
            nodrop.append((r["url"], len(sc["bound"]), len(naked["unbound"])))
    assert tested >= 20, (f"전제가 깨졌다 — 결속이 있는 표면이 {tested}개뿐이다. "
                          "스캐너가 눈이 멀었거나 결속이 통째로 빠졌다.")
    assert not nodrop, ("선언을 지웠는데도 미결속으로 안 떨어진 화면이 있다 — "
                        "그 화면의 초록은 결속 때문이 아니다: " + str(nodrop))


def test_scanner_itself_is_not_blind(crawl):
    """⛔음성 **위의 위**: 스캐너가 눈이 멀면 이 파일의 초록이 전부 공허해진다.

    합성 입력으로 확인한다 — 벌거벗은 철회값은 잡히고, 선언을 달면 잡히지 않는다.
    (스캐너가 아무것도 못 보게 되는 회귀는 위 시험들을 **전부 통과시킨다**.)
    """
    claims = crawl["claims"]
    tgt = next((c for c in claims if c["state"] == "retracted" and c.get("text")), None)
    assert tgt, "전제: 스캔 가능한 철회 정본값이 실제로 있다"
    t = tgt["text"]
    naked = C.scan_claim_bindings(f"<p>b2o3 의 MD Ea 는 {t} eV 다.</p>", claims=claims)
    assert naked["unbound"], f"벌거벗은 철회값 {t} 을 못 잡는다 — 스캐너가 눈이 멀었다"
    tied = C.scan_claim_bindings(f'<p data-claim="{tgt["id"]}">MD Ea {t} eV</p>', claims=claims)
    assert not tied["unbound"] and tied["bound"], "선언을 달았는데 결속으로 안 센다"


# ── ④ 툴팁(title=) — 화면이 마크다운 원문을 노출하지 않는가 ──────────────────
_TITLE_ATTR = re.compile(r'title="([^"]*)"')


def test_no_markdown_bold_markers_leak_into_tooltips(crawl):
    """⛔음성: `title=` 속성에 `**강조**` 표기가 새면 안 된다 — 툴팁이 깨져 보인다.

    왜 속성이 따로인가: **HTML 속성값에는 태그가 안 먹는다.** `|bold` 를 걸면 `<b>` 가
    글자로 뜨고, 아무것도 안 걸면 별표가 뜬다. 둘 다 깨진 화면이라 `|plain`(표식만 제거)이
    따로 있다. 원장 산문에 `**` 가 흔해서(citation_hazards `binding_scope_why` 33건 중 14건)
    이 누출은 계속 재발한다.

    실측 2026-09-15 (1저자 보고 "깨져서 나온다" 로 시작): 9개 화면 **툴팁 100개**가
    별표를 달고 있었다 — /explorer 27 · /requests 20 · /literature 12 · /governance 14 ·
    조성 25 · 기타. 한 자리만 `replace('**','')` 로 땜질돼 있었다.

    ⛔ 이 시험이 못 하는 것: 툴팁 **내용**이 맞는지는 안 본다. 표기만 본다.
      그리고 `*기울임*`·백틱은 일부러 안 본다 — 툴팁에서 깨져 보이지 않는다.
    """
    bad = []
    for r in crawl["rows"]:
        h = r.get("html")
        if not h:
            continue
        for t in _TITLE_ATTR.findall(h):
            if "**" in t:
                bad.append((r["url"], t[:120]))
    assert not bad, (
        f"툴팁 {len(bad)}개가 마크다운 `**` 를 그대로 노출한다 — `|plain` 을 걸어라:\n"
        + "\n".join(f"  {u} :: {t}" for u, t in bad[:12]))


def test_plain_filter_actually_strips_and_keeps_text():
    """양성+⛔음성: `|plain` 이 표식만 떼고 **글자는 안 지우는가**.

    표식을 떼면서 내용까지 지우면 경고가 조용히 사라진다 — 별표가 보이는 것보다 나쁘다.
    """
    assert C.plain_text("a **b** c") == "a b c", "표식을 못 뗀다"
    assert C.plain_text("**전부**") == "전부", "양끝 표식을 못 뗀다"
    # ⛔음성 ① 홀로 선 `*` 는 건드리지 않는다 (곱셈·각주 표기가 죽는다)
    assert C.plain_text("2 * 3 = 6") == "2 * 3 = 6", "짝 없는 별표를 건드렸다"
    # ⛔음성 ② 글자를 지우면 안 된다
    assert C.plain_text("**어느 것도** 인용 금지") == "어느 것도 인용 금지", "내용이 사라졌다"
    # ⛔음성 ③ None 은 빈 문자열 — "None" 이라고 쓰면 안 된다
    assert C.plain_text(None) == "", "None 이 글자로 샜다"
