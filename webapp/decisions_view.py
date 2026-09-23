"""조성 페이지가 **원장에서 파생시키는 것들** — 살아 있는 결정 · 마감 카드 · 값 지위 주석.

왜 별도 모듈인가 (v3 묶음 D · 2026-09-09)
  `/composition/<cid>` 는 값 타일을 잘 그리는데, **그 값을 지금 어떤 판정이 지배하고 있는지**
  를 한 글자도 안 실었다. 실측: 2026-09-08 에 1저자가 LPSOCl 3×3×1 닫힘 조건을 비준했고
  `decisions.json` 에 active 로 있는데 `/composition/lpsocl` 렌더 결과에 '닫힘'·'400 ps'·
  '보고량' 이 **0회**였다. 화면이 자기 캠페인을 모르는 상태다.

  같은 이유로 `copyComp`(값 복사)가 철회값 0.199 를 `(canonical, 방법 표기 포함)` 꼬리를
  달고 클립보드에 넣고 있었다 — 배지는 화면에만 있고 **복사 경로에는 없었다**.
  화면과 복사가 같은 사실을 말하려면 출처가 하나여야 한다. 그 하나가 여기다.

⛔ 이 모듈이 **못 하는 것**
  · 판정이 옳은지 보지 않는다. 원장에 든 대로 옮길 뿐이다.
  · 결정↔조성 대응을 추론하지 않는다 — `applies_to.systems` 토큰이 조성 이름을 담고
    있어야 걸린다. 담고 있지 않으면 **조용히 빠진다**(그건 원장 쪽 결함이고, 여기서
    추측으로 메우면 없는 판정을 화면이 만들어 낸다).
  · 인용위험(citation_hazards)의 금지 **범위**를 좁히지 못한다. 원장이 파일 단위로만
    적어 둔 위험은 파일 단위로만 낸다 — 값마다 금지 여부를 판정하지 않는다.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import canonical as C

ROOT = Path(__file__).resolve().parent.parent

#: 전 계 공통 정책을 뜻하는 토큰. 조성마다 8장씩 깔면 그 조성 고유의 판정이 파묻힌다 —
#: 개수만 세어 `/governance` 로 보낸다.
_WILDCARD = "*"

#: 조성 카드에서 재개 조건 한 항목이 차지하는 글자 상한. 넘으면 `…` 를 붙여 **잘렸음을
#: 표시**한다 (표식 없이 자르면 사람이 그게 전문인 줄 안다).
_REOPEN_CLIP = 240


def reopen_items(d) -> list:
    """결정의 재개 조건을 **문자열 목록**으로 정규화한다. 원장이 두 모양으로 적는다.

    ⛔ 2026-09-15 — 원장 34건 중 **6건이 `reopen_criteria` 를 배열**로 적는데, 화면 두
      곳이 그걸 문자열처럼 다뤘다. 둘 다 오류를 안 냈다 (조용히 틀린 경로):
        · `/governance` : `{{ d.reopen_criteria|bold }}` → 필터가 `str(list)` 를 하는 바람에
          **파이썬 repr** 이 그대로 화면에 나왔다 — `['다음 5–10 캠페인에서 …']`.
          1저자 실측 보고: "뭔가 깨져서 나와 · 줄바꿈되어있고".
        · `/composition`: `(… or "")[:240]` 가 리스트에서는 **원소 240개**를 자른다.
          240자 제한이 한 글자도 걸리지 않았고, 역시 repr 로 샜다.
      선언(재개 조건을 보인다)은 맞았고 실행 경로만 다른 일을 했다.

    ⛔ 이 함수가 **못 하는 것**: 재개 조건이 옳은지·충족됐는지 판정하지 않는다. 모양만
      고른다. 빈 항목은 버리지만 **개수는 줄이지 않는다** — 전부 낸다.
    """
    rc = d.get("reopen_criteria") if isinstance(d, dict) else d
    if rc is None or rc == "" or rc == []:
        return []
    items = rc if isinstance(rc, (list, tuple)) else [rc]
    return [str(x).strip() for x in items if str(x).strip()]


def _clip(s: str, n: int = _REOPEN_CLIP) -> str:
    s = str(s)
    return s if len(s) <= n else s[:n].rstrip() + "…"


#: 화면에 펼쳐 보이는 상태. 나머지(superseded·retracted·rejected)는 **접어서** 남긴다.
LIVE_STATES = ("active", "proposed")


def _sys_matches(token: str, cid: str) -> bool:
    """결정 원장의 계 토큰이 이 조성을 가리키나.

    규칙은 셋뿐이다 — ① 같다 ② 토큰이 `<cid>_…` 로 시작한다(sdcp_neutral → sdcp)
    ③ 레지스트리 별칭(`canonical.system_tokens`)이 조성 이름을 든다(b2o3-lpscl → b2o3).
    ⛔ 부분문자열 매칭은 **쓰지 않는다** — 'nd' 가 'hash-bound' 에 걸린 전례가 있다.
    """
    t = str(token or "").strip().lower()
    c = cid.lower()
    if not t or t == _WILDCARD:
        return False
    return t == c or t.startswith(c + "_") or c in C.system_tokens(t)


def decisions_for(cid: str, root=None) -> dict:
    """이 조성을 지배하는 판정 — `{"live": [...], "folded": [...], "n_global": int}`.

    각 항목: `{"id","title","state","kind","date","statement","reopen","card"}`
    ⚠ `reopen` 은 **문자열 목록**이다 (원장이 배열로도 적는다 — `reopen_items` 참조).
    """
    # `canonical.decisions()` 는 **id → 판례** dict 다 (배열이 아니다).
    rows = list((C.decisions(root=root) or {}).values())
    live, folded, n_global = [], [], 0
    for d in rows:
        systems = ((d.get("applies_to") or {}).get("systems")) or []
        if any(str(s).strip() == _WILDCARD for s in systems):
            n_global += 1
            continue
        if not any(_sys_matches(s, cid) for s in systems):
            continue
        state = C.decision_state(d)
        rec = {"id": d.get("id"), "title": d.get("title") or d.get("id"),
               "state": state, "kind": d.get("kind"),
               "date": _date_of(d.get("id")),
               "statement": (d.get("statement") or "")[:400],
               # ⚠ 목록이다 (문자열 아님) — 원장이 배열로도 적는다. reopen_items 참조.
               "reopen": [_clip(x) for x in reopen_items(d)],
               "card": d.get("card")}
        (live if state in LIVE_STATES else folded).append(rec)
    live.sort(key=lambda r: r["date"], reverse=True)
    folded.sort(key=lambda r: r["date"], reverse=True)
    return {"live": live, "folded": folded, "n_global": n_global}


def decisions_by_scope(prefix: str, extra_ids=(), root=None) -> dict:
    """`scope` 가 prefix 로 시작하는 판정 (+ 원장이 이름으로 댄 관련 결정) — `{"live", "folded"}`.

    항목 모양은 `decisions_for` 와 같다. 조성 기준이 아니라 **캠페인 기준**으로 모을 때 쓴다
    (/adhesion — W_ad 결정은 scope `adhesion.wad_lpscl_agc.*` 를 쓴다).

    ⛔ 못 하는 것: scope 가 비었거나 다른 접두어인 결정은 못 잡는다 — 그런 결정은 원장이
      `extra_ids` 로 **이름을 대야** 걸린다 (추측으로 끌어오지 않는다).
    """
    rows = list((C.decisions(root=root) or {}).values())
    extra = {str(x) for x in (extra_ids or ())}
    live, folded = [], []
    for d in rows:
        sc = str(d.get("scope") or "")
        if not ((prefix and sc.startswith(prefix)) or d.get("id") in extra):
            continue
        state = C.decision_state(d)
        rec = {"id": d.get("id"), "title": d.get("title") or d.get("id"),
               "state": state, "kind": d.get("kind"),
               "date": _date_of(d.get("id")),
               "statement": (d.get("statement") or "")[:400],
               "reopen": [_clip(x) for x in reopen_items(d)],
               "card": d.get("card")}
        (live if state in LIVE_STATES else folded).append(rec)
    live.sort(key=lambda r: (r["date"], r["id"] or ""), reverse=True)
    folded.sort(key=lambda r: (r["date"], r["id"] or ""), reverse=True)
    return {"live": live, "folded": folded}


#: 결정 id 는 `-`, 카드 파일명은 `_` 로 날짜를 쓴다. 둘 다 읽고 표기는 `-` 로 통일한다.
_DATE = re.compile(r"(\d{4})[-_](\d{2})[-_](\d{2})")


def date_of(s) -> str:
    """결정 id·카드 파일명에서 날짜(`YYYY-MM-DD`)를 뽑는다. 못 찾으면 빈 문자열.

    ⛔ 못 하는 것: 그 날짜가 **무슨** 날짜인지(결정일·비준일·마감일) 구분하지 않는다.
      id 에 박힌 글자를 읽을 뿐이다 — 비준 시각은 `ratification.timestamp` 가 원본이다.
    """
    m = _DATE.search(str(s or ""))
    return "-".join(m.groups()) if m else ""


#: 옛 이름 (모듈 안에서만 쓰였다)
_date_of = date_of


#: 마감·사전등록·보고량 카드 파일명 표식. 파일명이 규약이라 이름으로 판다
#: (`db/properties/<계>_closed_<날짜>.json` — CLAUDE.md 마감 규율).
_CARD_MARKS = (("closed", "마감"), ("closure_conditions", "닫힘 조건"),
               ("estimand", "보고량 카드"), ("prereg", "사전등록"))


def closure_cards_for(cid: str, prefixes=None, root=None) -> list:
    """이 조성의 마감/닫힘/보고량/사전등록 카드 파일 목록.

    ⛔ 내용을 고치지 않는다. `ratification.content_digest` 가 박힌 카드가 여럿이라
      **읽기만** 한다 — 제목 한 줄과 날짜만 뽑아 링크를 건다.
    """
    base = Path(root) if root else ROOT
    d = base / "db" / "properties"
    if not d.exists():
        return []
    pref = [p.lower() for p in (prefixes or [cid])]
    out = []
    for f in sorted(d.glob("*.json")):
        n = f.name.lower()
        if not any(n.startswith(p) for p in pref):
            continue
        kind = next((lab for mark, lab in _CARD_MARKS if mark in n), None)
        if not kind:
            continue
        out.append({"file": f"db/properties/{f.name}", "kind": kind,
                    "date": _date_of(f.name), "title": _card_title(f)})
    out.sort(key=lambda r: r["date"], reverse=True)
    return out


def _tables(raw) -> list:
    """해석 카드의 `표` → 화면용. **모양을 검사하고, 어긋나면 말한다.**

    ⛔ 조용히 자르거나 버리지 않는다 — 표가 반쯤 그려지면 사람은 그걸 전부로 읽는다.
    """
    out = []
    for t in raw:
        if not isinstance(t, dict):
            continue
        cols = [str(c) for c in (t.get("columns") or [])]
        rows = [[str(c) for c in r] for r in (t.get("rows") or []) if isinstance(r, (list, tuple))]
        bad = [i for i, r in enumerate(rows) if len(r) != len(cols)]
        out.append({"title": str(t.get("제목") or t.get("title") or ""),
                    "columns": cols, "rows": rows,
                    "note": str(t.get("note") or ""),
                    "source": str(t.get("source") or ""),
                    "error": (f"열 {len(cols)}개인데 칸 수가 다른 행 {bad}" if bad else "")})
    return out


#: 해석 카드에서 **이미 따로 렌더되는** 키. `card_sections` 가 두 번 싣지 않게 뺀다.
_INTERP_RENDERED = {
    "3_반대_증거_숨기지_않는다",      # counter
    "미결_이것이_있어야_주장이_선다",  # open
}


def card_sections(j: dict) -> list:
    """해석 카드의 **번호 절**을 화면용으로 펼친다. → [{key, title, body}]

    왜 생겼나 (2026-09-16): `interpretation_cards_for` 가 정해진 키만 뽑았다. 그래서
    카드에 `5_…` `6_…` 절을 추가해도 **화면에 한 글자도 안 떴다** — 파일은 자라는데
    화면은 그대로라, 사람은 "그 내용이 없다" 고 읽는다. 조용히 틀린 경로다.

    ⛔ 이 함수가 못 하는 것
      · 내용을 판정하지 않는다. 카드가 쓴 대로 싣는다.
      · 마크다운을 파싱하지 않는다 — 서버의 `mdlite` 필터가 템플릿에서 한 번만 한다
        (CLAUDE.md §화면 규율: 브라우저에서 다시 파싱하지 않는다).
      · 숫자의 출처를 만들어 주지 않는다 — 출처는 **카드가 절 안에 적어야** 한다.
    """
    out = []
    if not isinstance(j, dict):
        return out
    for k, v in j.items():
        if not isinstance(k, str) or k in _INTERP_RENDERED:
            continue
        # 번호 절(`1_…`)과 ★ 절만. `★_한_줄` 은 headline 이라 뺀다.
        if not (k[:1].isdigit() or k.startswith("★")) or k == "★_한_줄":
            continue
        out.append({"key": k, "title": k.replace("_", " ").strip(),
                    "body": _flatten(v)})
    return out


#: 카드 본문 어디에 있든 **밖으로 꺼내는** 링크. `[글](https://…)` 을 먼저 보고,
#: 라벨 없는 맨 URL 도 줍는다.
_CARD_LINK = re.compile(r"\[([^\]\n]{1,120})\]\((https://[^\s()<>\"'|]{1,500})\)")
_BARE_URL = re.compile(r"(?<![(\w])(https://[^\s()<>\"'|]{1,500})")
#: 이 화면 **자신이 서빙하는** 보고서. 2026-09-17 신설.
#:   왜: Nd/O 카드의 보고서 버튼이 외부 아티팩트 URL 하나만 가리키고 있었는데, 그 URL 은
#:   **만든 세션 밖에서는 갱신이 안 된다**(원본을 못 받아 publish 가 거부된다 — 실측).
#:   그래서 repo 가 최신인데 버튼은 낡은 화면을 열었다. 정본을 webapp 이 직접 서빙한다.
#:   ⛔ **마크다운 형식만** 줍는다 — 맨 경로는 안 줍는다. 산문에 `/api/...` 가 우연히
#:     들어가도 버튼이 생기면 안 된다 (링크는 선언이지 발견이 아니다).
_CARD_LOCAL = re.compile(r"\[([^\]\n]{1,120})\]\((/(?:api/file|files|kb)/[^\s()<>\"'|]{1,300})\)")


def card_links(j: dict) -> list:
    """카드가 가리키는 **외부 링크**를 접힘 밖으로 꺼낸다. → [{url, label}]

    왜 생겼나 (2026-09-16 실측): 카드 §7 에 아티팩트 URL 을 넣었는데 그 절이
      `<details>`(본문 N절) **안**이라 접혀 있었다. 1저자가 화면을 보고
      *"여기에 url 이 어디 있어"* 라고 물었다 — **접힌 링크는 붙인 것이 아니다.**
      CLAUDE.md §화면 규율과 같은 논리다: 화면에 안 실리면 없는 것이다.

    ⛔ 이 함수가 못 하는 것
      · 링크가 살아 있는지 확인하지 않는다 (네트워크를 안 탄다).
      · https 가 아닌 것은 안 줍는다 — 화면에 앵커로 나가는 값이다.
      · 카드가 그 링크를 **어떤 뜻으로** 달았는지 판정하지 않는다. 경고·조건은
        절 본문에 있고, 여기서 요약하지 않는다.
      · 내부 링크(`local: True`)가 **실제로 서빙되는지** 확인하지 않는다 —
        경로가 맞는지는 `/api/file` 의 `safe_repo_path` 가 요청 시에 본다.
    """
    out, seen = [], set()
    if not isinstance(j, dict):
        return out
    blob = json.dumps(j, ensure_ascii=False)
    # 내부 정본을 **먼저** 낸다 — 외부 거울보다 앞에 서야 사람이 그걸 누른다.
    for label, url in _CARD_LOCAL.findall(blob):
        if url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "label": label.replace("\\n", " ").strip(), "local": True})
    for label, url in _CARD_LINK.findall(blob):
        if url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "label": label.replace("\\n", " ").strip()})
    for url in _BARE_URL.findall(blob):
        url = url.rstrip('\\"')
        if url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "label": url})
    return out


def _flatten(v, depth: int = 0) -> list:
    """중첩 dict/list → [{indent, label, text}] 평면 목록. 깊이 3 에서 멈춘다.

    ⛔ 잘라내지 않는다 — 카드 산문을 화면에서 줄이면 근거가 잘린다.
    """
    rows = []
    if depth > 3:
        return rows
    if isinstance(v, dict):
        for k, x in v.items():
            if isinstance(x, (dict, list)):
                rows.append({"indent": depth, "label": str(k), "text": ""})
                rows.extend(_flatten(x, depth + 1))
            else:
                rows.append({"indent": depth, "label": str(k), "text": str(x)})
    elif isinstance(v, (list, tuple)):
        for x in v:
            if isinstance(x, (dict, list)):
                rows.extend(_flatten(x, depth + 1))
            else:
                rows.append({"indent": depth, "label": "", "text": str(x)})
    else:
        rows.append({"indent": depth, "label": "", "text": str(v)})
    return rows


def interpretation_cards_for(cid: str, root=None) -> list:
    """이 조성의 **해석 카드** (`schema: interpretation_card/v1`).

    왜 파일명 접두어로 찾지 않나 (2026-09-14): `closure_cards_for` 는 접두어로 찾는데,
    그 방식은 이름이 우연히 겹치면 남의 조성 화면에 뜬다. 해석은 서술이라 그 사고가 더
    비싸다 — **카드가 `composition` 으로 자기 소속을 선언**하게 하고 그것만 본다.

    ⛔ 이 함수가 못 하는 것
      · 내용을 판정하지 않는다. `citable` 을 그대로 실어 보낼 뿐이다.
      · 못 읽은 파일을 **조용히 건너뛰지 않는다** — `error` 를 달아 돌려준다.
        (조용히 빼면 화면이 '해석 카드 없음' 으로 보이고, 그건 사실이 아니다.)
    """
    base = Path(root) if root else ROOT
    d = base / "db" / "properties"
    if not d.exists():
        return []
    out = []
    for f in sorted(d.glob("*.json")):
        try:
            head = f.read_text(encoding="utf-8", errors="ignore")[:400]
        except OSError:
            continue
        if "interpretation_card/v1" not in head:
            continue
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            out.append({"file": f"db/properties/{f.name}", "composition": None,
                        "error": f"{type(e).__name__} — 못 읽었다", "title": f.name})
            continue
        if j.get("composition") != cid:
            continue
        out.append({
            "file": f"db/properties/{f.name}", "composition": cid,
            "date": str(j.get("date") or _date_of(f.name)),
            "status": str(j.get("status") or ""),
            "citable": bool(j.get("citable")),
            "title": str(j.get("제목") or j.get("title") or f.stem),
            "headline": str(j.get("★_한_줄") or ""),
            "allowed": list(j.get("허용_서술_이대로만") or []),
            "forbidden": list(j.get("금지_서술") or []),
            "counter": list(j.get("3_반대_증거_숨기지_않는다") or []),
            "open": list(j.get("미결_이것이_있어야_주장이_선다") or []),
            # 숫자 표 — 카드가 선언한 것만, **출처 파일을 달고** 온다.
            #   ⚠ 모양이 어긋난 표(열 수 ≠ 칸 수)는 버리지 않고 `error` 를 달아 낸다.
            "tables": _tables(j.get("표") or []),
            # 번호 절 — 카드가 쓴 산문을 **그대로** 싣는다 (2026-09-16 신설).
            "sections": card_sections(j),
            # 외부 링크 — **접힘 밖**으로 꺼낸다 (2026-09-16: 접힌 링크는 붙인 게 아니다)
            "links": card_links(j),
        })
    out.sort(key=lambda r: r.get("date") or "", reverse=True)
    return out


def _card_title(f: Path) -> str:
    """카드의 한 줄 정체. 없으면 빈 문자열 — **지어내지 않는다**."""
    try:
        j = json.loads(f.read_text(encoding="utf-8"))
    except Exception:                                       # noqa: BLE001
        return ""
    if not isinstance(j, dict):
        return ""
    # ⚠ `schema` 는 쓰지 않는다 — 'md_estimand_prereg/v1' 은 제목이 아니라 형식 이름이다.
    for k in ("제목", "title", "what", "_purpose", "purpose"):
        v = j.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()[:160]
    return ""


# ── 값 지위 주석 — 화면 타일과 클립보드가 **같은 출처**를 쓴다 ─────────────────
#: 인용 지위를 바꾸는 금지 토큰. 원장 `prohibitions` 어휘에서 판다 —
#: 손으로 metric 이름을 적으면 그 순간 원장과 갈라진다.
_HOLD_MARKS = ("on_hold", "cite_until_")

#: status → 복사문에 **반드시** 실리는 말. 화면 배지 어휘(`data._STATUS_BADGE`)와 같은 낱말.
_COPY_MARK = {"retracted": "⛔ 철회 — 인용 금지",
              "non_citable": "⛔ 인용불가 — 원자료가 금지했다",
              "superseded": "⛔ 철회 — 인용 금지",
              "provisional": "⚠ 잠정 — 정본 아님",
              "source_error": "⚠ 출처오류",
              "source_pending": "⚠ 출처미배선",
              "unreviewed_drift": "⚠ 미검토"}


def metric_notices(cid: str, root=None) -> dict:
    """metric → `{"mark","instead","hold","hold_why","source_path","updated","citable"}`.

    · `mark` — 라벨 뒤에 **강제로** 붙는 말(철회/잠정/인용불가/보류). 정본이면 "".
    · `instead` — 대체값 문장. sentinel 이면 `canonical.instead_text` 가 "대체값 없음" 이라 말한다.
    · `hold` — `prohibitions` 에 보류 토큰이 있는 축(예: SDCP 절대 E_ads 는 δ_m·δ_LREAL
      미측정으로 **조건부 보류**다). 값은 있으나 절대값을 그대로 인용하면 안 된다.

    ⛔ 못 하는 것: 보류가 언제 풀리는지 모른다. 해제 조건은 항목의 `note` 와 마감 카드에 있다.
    """
    reg = C.registry(root=root)
    instead = {(c["metric"], c["system"]): c for c in C.bound_claims(reg=reg, root=root)}
    out = {}
    for e in reg.get("entries", []):
        if e.get("system") != cid:
            continue
        m = e.get("metric")
        if not m:
            continue
        st = e.get("status")
        prohibitions = [str(p) for p in (e.get("prohibitions") or [])]
        hold = [p for p in prohibitions if any(k in p for k in _HOLD_MARKS)]
        mark = _COPY_MARK.get(st, "")
        if e.get("citable") is False and not mark:
            mark = _COPY_MARK["non_citable"]
        if hold and not mark:
            mark = "⏸ 조건부 보류 — 절대값 인용 보류"
        cl = instead.get((m, cid))
        out[m] = {"mark": mark,
                  "instead": C.instead_text(cl.get("instead")) if cl else "",
                  "claim": cl.get("id") if cl else None,
                  "hold": bool(hold), "hold_why": " · ".join(hold),
                  "prohibitions": prohibitions,
                  "citable": e.get("citable") is not False,
                  "source_path": e.get("source_path"), "updated": e.get("updated")}
    return out


def other_family_axes(cid: str, families: dict, values: dict, na_keys=(), root=None) -> set:
    """이 조성의 **계열에 등록된 적이 없는** metric 집합 — 타일이 아니라 접힘 줄로 보낸다.

    ⛔ P0-09 (2026-09-09) — `metric_meta()` 가 레지스트리의 모든 metric 을 내보내고
      템플릿이 그걸 전수 렌더해서, SDCP 분자 metric 11개가 **14개 조성 전부**에 TODO 로
      찍혔다. `/composition/comp1`(LPSCl) 이 PTFE 흡착에너지를 "미계산" 으로 광고했고,
      그건 애초에 보류(HOLD)된 양이다. TODO 는 "하면 되는데 안 했다" 라는 약속이라
      아무 데나 찍으면 안 된다.

    판정: metric 의 레지스트리 항목들이 사는 **계열 집합**에 이 조성의 계열이 없으면 접는다.
      값이 있거나 N/A 사유가 적힌 축은 **언제나 보인다**(접기 대상이 아니다).

    ⛔ 못 하는 것
      · "이 계열엔 원리적으로 성립하지 않는다" 고 말하지 않는다. 그건 `CANONICAL_NA` 의
        사유 문장이 하는 일이고, 여기 판정은 *"원장에 전례가 없다"* 까지다.
      · 계열이 없는 계(`b2o3_vs_modelc` 같은 쌍 이름)는 `None` 계열로 묶인다 — 어느 조성
        계열과도 같지 않으므로 그 축은 접힌다.
    """
    reg = C.registry(root=root)
    fam = families.get(cid)
    scope: dict = {}
    for e in reg.get("entries", []):
        m = e.get("metric")
        if m:
            scope.setdefault(m, set()).add(families.get(e.get("system")))
    na = set(na_keys)
    return {m for m, v in values.items()
            if v is None and m not in na and fam not in scope.get(m, set())}


def copy_lines(cid: str, values: dict, labels: dict, units: dict, root=None) -> list:
    """`📋 값 복사` 가 클립보드에 넣을 줄 — **지위가 값과 한 몸으로** 나간다.

    ⛔ P0-04 (2026-09-09) — 종전 `copyComp` 는 canonical/labels/units/meta 만 읽고
      `canonical_status` 를 안 읽었다. 그래서 `/composition/b2o3` 의 복사 버튼이
      철회값 `MD Ea: 0.199 eV` 를 내보내면서 마지막 줄에 `(canonical, 방법 표기 포함)`
      까지 붙였다 — **철회값이 정본 꼬리표를 달고 나간 것**이다.
      이제 지위가 없는 줄은 만들 수 없다: mark 가 있으면 라벨 바로 뒤에 들어간다.

    반환 `[{"text", "clean"}]` — `clean` 이 False 인 줄이 하나라도 있으면 꼬리말에서
    'canonical' 이라는 말을 뺀다(꼬리말은 템플릿이 만든다).
    """
    nt = metric_notices(cid, root=root)
    rows = []
    for k, v in values.items():
        if v is None:
            continue
        n = nt.get(k) or {}
        mark, ins = n.get("mark") or "", n.get("instead") or ""
        head = f"{labels.get(k, k)}{(' [' + mark + ']') if mark else ''}"
        line = f"{head}: {v} {units.get(k, '')}".rstrip()
        if ins:
            line += f"\n    ↳ 대신 쓸 값: {ins}"
        elif mark.startswith("⛔"):
            line += "\n    ↳ 대신 쓸 값: 원장에 등록된 대체값이 없다"
        rows.append({"key": k, "text": line, "clean": not mark})
    return rows


def hazards_for(cid: str, prefixes=None, root=None) -> list:
    """이 조성의 **원자료 파일**에 걸린 인용 위험 (살아 있는 것만).

    잇는 방법 두 가지 — ① 위험 행의 `claim`(metric@system)이 이 조성을 가리킨다
    ② 위험 행의 `file` 이 이 조성 항목의 `source_path` 와 같다.
    ⛔ 파일 단위 위험을 **값 단위 금지로 번역하지 않는다**. 그건 원장이 `claim` 이나
      `forbidden_phrases` 로 좁혀 줘야 하는 일이고, 여기서 넘겨짚으면 멀쩡한 값에
      금지 딱지가 붙는다(같은 파일의 dE_site 는 영향 없다고 원장이 명시했다).
    """
    reg = C.registry(root=root)
    srcs = {str(e.get("source_path")) for e in reg.get("entries", [])
            if e.get("system") == cid and e.get("source_path")}
    out = []
    for z in C._hazard_rows(root=root):
        # 집행 기준은 level 이 아니라 **금지 상태**다 (BI-3 P0-1)
        if not C.prohibition_active(z):
            continue
        claim_sys = str(z.get("claim") or "").split("@")[-1]
        if claim_sys:
            # ★ `claim` 이 있으면 **그게 범위다** — 원장이 계를 좁혀 적어 뒀는데 파일까지
            #   같이 보면 넓어진다(실측: `MD_Ea_eV@lpsocl` HOLD 가 같은 파일을 출처로 둔
            #   modelc·b2o3 페이지에도 붙었다).
            if not _sys_matches(claim_sys, cid):
                continue
            by_claim = True
        else:
            by_claim = False
            files = [s.strip() for s in str(z.get("file") or "").split("·")]
            if not any(f in srcs for f in files):
                continue
        out.append({"id": z.get("id"), "level": z.get("level"), "what": z.get("what"),
                    "why": (z.get("why") or "")[:400], "fix": (z.get("fix") or "")[:400],
                    "file": z.get("file"), "how": "claim" if by_claim else "source_path"})
    out.sort(key=lambda r: (C.HAZARD_LEVELS.index(r["level"])
                            if r["level"] in C.HAZARD_LEVELS else 99))
    return out


def _selftest() -> int:                                      # pragma: no cover - CLI
    """양성 + **음성** 경로. 음성이 없는 selftest 는 통과해도 아무것도 보증 못 한다."""
    bad = []

    # ① 양성 — 실제 원장에서 걸려야 하는 것
    if not decisions_for("lpsocl")["live"]:
        bad.append("lpsocl 에 살아 있는 결정이 0건이다 (원장엔 active 가 있다)")
    if not decisions_for("sdcp")["live"]:
        bad.append("sdcp 가 sdcp_neutral/sdcp_doped 결정을 못 받는다")
    if not closure_cards_for("lpsocl"):
        bad.append("lpsocl 닫힘 조건 카드를 못 찾는다")

    # ② 음성 — 걸리면 안 되는 것
    if any(_sys_matches(t, "nd") for t in ("hash-bound-carry", "cascade_d_rel_estimand")):
        bad.append("부분문자열 매칭이 되살아났다 — 'nd' 가 낱말 안쪽에 걸린다")
    if _sys_matches("*", "lpsocl"):
        bad.append("전 계 와일드카드가 조성 결정으로 샜다")
    if _sys_matches("b2o3", "lpsocl"):
        bad.append("다른 계 결정이 lpsocl 로 샌다")
    if decisions_for("comp3")["live"]:
        bad.append("결정이 없는 조성에 결정이 생겼다")

    # ③ 음성 — 지위 없는 복사줄이 만들어지면 안 된다
    lines = copy_lines("b2o3", {"MD_Ea_eV": "0.199"}, {"MD_Ea_eV": "MD Ea"},
                       {"MD_Ea_eV": "eV"})
    if not lines or "철회" not in lines[0]["text"]:
        bad.append(f"철회값 복사줄에 철회 표시가 없다: {lines}")
    if lines and lines[0]["clean"]:
        bad.append("철회값 줄이 clean 으로 표시된다 — 꼬리말이 canonical 을 자칭하게 된다")

    # ④ 음성 — 보류가 dE_site 로 번지면 안 된다
    nt = metric_notices("sdcp")
    if not nt.get("SDCP_Eads_eV__sdcp_neutral_Litop", {}).get("hold"):
        bad.append("SDCP 절대 E_ads 의 조건부 보류가 안 잡힌다")
    if nt.get("SDCP_dE_site_meV__ptfe_c10_pm1", {}).get("hold"):
        bad.append("자리대비(dE_site)까지 보류로 번졌다 — 원장은 영향 없다고 적었다")

    for b in bad:
        print("⛔", b)
    print("selftest:", "FAIL" if bad else "ok")
    return 1 if bad else 0


if __name__ == "__main__":                                   # pragma: no cover - CLI
    import sys
    sys.exit(_selftest())
