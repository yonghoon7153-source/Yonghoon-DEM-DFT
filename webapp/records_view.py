"""기록 화면(/log · /todo · /requests · /notes · /files)이 쓰는 파생 표시층.

이 모듈이 지키는 규율 하나: **숫자·판정은 여기서 짓지 않는다.** 전부 원장에서 읽어
파생시킨다 (db/properties/*_closed_*.json · citation_hazards.json · canonical_registry.json).
손으로 적은 요약은 반드시 낡기 때문이다.

⛔ 이 모듈이 **못 하는 것**
  · 문장을 읽지 않는다. `mark_closed_axis` 는 마감된 축의 **수**가 그 자리에 있는지만
    본다 — 그 문장이 정당한 이력 서술인지(“이건 철회됐다”)는 사람이 판단할 몫이다.
    그래서 표식은 “인용 금지”가 아니라 “이 수는 마감된 축의 것이다”라고만 말한다.
  · 원문(kb 마크다운)을 고치지 않는다. 렌더된 HTML 조각에만 표식을 얹는다.
  · 마감 카드가 **이름을 대지 않은** 수는 못 잡는다. 카드가 “0.222 eV 포함”이라고
    적었기 때문에 잡는 것이지, 축에 속한 모든 수를 아는 게 아니다.
  · `journal_groups` 는 kind 를 판정하지 않는다 — 표시층 어휘로 접을 뿐, 원문
    journal.jsonl 의 kind 문자열은 절대 고치지 않는다.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path

import canonical as _C

_ROOT = Path(__file__).resolve().parent.parent

#: 마감 카드에서 **금지·철회를 말하는 절**만 읽는다. 살아있는 축(밴드갭 1.9671 등)이
#: 같은 파일에 있으므로, 절 이름으로 가리지 않으면 살아있는 값까지 표식이 붙는다.
_FORBID_KEY = re.compile(r"금지|철회|retract|forbid", re.I)
#: 소수 두 자리 이상만 본다 — `1.6`(LPSCl1.6)·`800 K`·`145 meV` 같은 것에 안 걸리게.
_NUM_IN_TEXT = re.compile(r"\d+\.\d{2,}")


def _load(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                   # noqa: BLE001
        return None


def _strings_under(node, key_ok: bool) -> list:
    """중첩 구조에서 문자열을 긁는다. 금지·철회를 말하는 키 아래만 판다."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            out += _strings_under(v, key_ok or bool(_FORBID_KEY.search(str(k))))
    elif isinstance(node, list):
        for v in node:
            out += _strings_under(v, key_ok)
    elif isinstance(node, str) and key_ok:
        out.append(node)
    return out


def _live_values(root=None) -> set:
    """지금 **인용 가능한** 정본 수 — 여기 있는 수에는 절대 표식을 안 붙인다.

    음성 안전장치다. 마감 카드가 살아있는 축을 언급하는 절(“살아있는_축”)을 실수로
    긁어도, 그 값이 레지스트리에서 canonical 이면 표식이 나가지 않는다.
    """
    out = set()
    try:
        reg = _C.registry(root=root)
    except Exception:                                   # noqa: BLE001
        return out
    for e in reg.get("entries", []):
        if e.get("status") == "canonical" and e.get("citable") is not False:
            v = e.get("value")
            if isinstance(v, (int, float)):
                out.add(round(float(v), 12))
    return out


def _already_bound(root=None) -> set:
    """표준 결속기(`bound_claims`)가 **이미 덮는** 수.

    겹쳐 감싸면 표식이 두 번 찍힌다 (실측: `0.199[⛔인용위험][⛔철회·인용금지]`).
    이미 이름이 붙은 수는 다시 붙이지 않는다 — 우리 몫은 **레지스트리가 모르는** 수다.
    """
    out = set()
    try:
        for c in _C.bound_claims(root=root):
            if c.get("kind") == "number" and c.get("text"):
                v = _C._num_of(c["text"])
                if v is not None:
                    out.add(round(abs(v), 12))
    except Exception:                                   # noqa: BLE001
        pass
    return out


def _registry_retraction_text(hz: dict, root=None) -> str:
    """위험 행의 `claim`(=`<metric>@<system>`)이 가리키는 레지스트리 철회 사유문."""
    cid = str(hz.get("claim") or "")
    if "@" not in cid:
        return ""
    metric, system = cid.split("@", 1)
    try:
        reg = _C.registry(root=root)
    except Exception:                                   # noqa: BLE001
        return ""
    for e in reg.get("entries", []):
        if e.get("metric") == metric and e.get("system") == system:
            r = e.get("retracted") or {}
            return " ".join(str(r.get(k) or "") for k in ("what", "why"))
    return ""


def _precision_variants(tok: str) -> set:
    """카드가 적은 **자릿수까지 같으면 같은 수**로 본다.

    카드는 `0.224`(3자리)라고 적었는데 화면은 `0.2241`(4자리)로 찍는다 — 실측
    누출이 정확히 이 모양이었다(/requests 의 “저온 구간 Ea = 0.2241 ± 0.0606 eV”).
    한 자리 더 정밀한 표기 중 카드 자릿수로 반올림했을 때 같아지는 것들을 같이 낸다.

    ⛔ 못 하는 것: 두 자리 이상 더 정밀한 표기(`0.22412`)는 안 잡는다.
    """
    out = {tok}
    if "." not in tok:
        return out
    d = len(tok.split(".", 1)[1])
    # ⚠ 두 자리에서 늘리지 않는다. `1.33`(단일시드 σ 비) 을 세 자리로 펴면 1.325–1.335
    #   열한 수가 어휘에 들어가고, 실측에서 **무관한 `LiCl 엑셀 1.335`** 를 칠했다.
    #   카드가 세 자리 이상을 적었을 때만 “자릿수 하나 더” 를 인정한다.
    if d < 3:
        return out
    try:
        v = float(tok)
    except ValueError:
        return out
    step = 10.0 ** -(d + 1)
    for k in range(-9, 10):
        c = round(v + k * step, d + 1)
        if round(c, d) == round(v, d):
            out.add(("%%.%df" % (d + 1)) % c)
    return out


def closed_axis_claims(root=None) -> list:
    """마감된 축의 **숫자 어휘** → `annotate_claims` 가 먹는 claim 목록.

    파생 사슬 (손으로 적은 수 0개):
      ① `db/properties/*_closed_*.json` 중 **비준된**(status=ratified) 마감 카드
      ② 그 카드에서 금지·철회를 말하는 절의 문자열 → 소수 두 자리 이상 숫자 토큰
      ③ 그 카드 파일명을 `fix`/`why` 에서 이름 댄 인용위험 행 → 결속 id
    ③ 이 없으면 그 카드는 **건너뛴다** — 원장에 없는 id 로 결속하면 유령 결속이다.
    """
    base = Path(root) if root else _ROOT
    live = _live_values(root=root) | _already_bound(root=root)
    try:
        rows = _C._hazard_rows(root=root)
    except Exception:                                   # noqa: BLE001
        rows = []
    out, seen = [], set()
    for card in sorted((base / "db" / "properties").glob("*_closed_*.json")):
        d = _load(card)
        if not isinstance(d, dict):
            continue
        rat = d.get("ratification") or {}
        if d.get("status") != "ratified" and rat.get("state") != "ratified":
            continue
        hz = next((z for z in rows
                   if z.get("id") and card.name in json.dumps(z, ensure_ascii=False)), None)
        if not hz:
            continue
        why = " · ".join(_strings_under(d.get("금지_서술"), True))[:240] \
            or str(hz.get("what") or "")
        toks = set()
        for s in _strings_under(d, False):
            toks |= set(_NUM_IN_TEXT.findall(s))
        # 위험 행이 가리키는 레지스트리 항목의 **철회 사유문**도 같은 어휘다 —
        # 카드가 안 적은 짝(`800→1000 0.077`)이 거기 있다. 값 자체는 이미
        # `bound_claims` 가 덮으므로 아래 `live` 필터가 중복을 걸러낸다.
        toks |= set(_NUM_IN_TEXT.findall(_registry_retraction_text(hz, root=root)))
        for t in sorted(toks):
            for v in sorted(_precision_variants(t)):
                try:
                    fv = round(float(v), 12)
                except ValueError:
                    continue
                if fv in live:                       # 음성 안전장치 — 살아있는 정본은 건너뛴다
                    continue
                key = (hz["id"], fv)
                if key in seen:
                    continue
                seen.add(key)
                out.append({
                    "id": hz["id"], "metric": hz["id"], "system": "closed_axis",
                    "state": "hazard_" + str(hz.get("level", "")).lower(),
                    "text": v, "kind": "number", "unit": None,
                    "system_tokens": _C.system_tokens(
                        str(hz.get("claim") or "").split("@")[-1] or None),
                    "why": why,
                    "instead": {"none": True,
                                "decision": hz.get("decision") or "미상"},
                })
    return out


_SECTION_SPLIT = re.compile(r"(?=<h[1-6][\s>])", re.I)
_HEAD_OPEN = re.compile(r"<h([1-6])[\s>]", re.I)
_HEAD_TEXT = re.compile(r"<h[1-6][^>]*>(.*?)</h[1-6]>", re.I | re.S)
_TAGS = re.compile(r"<[^>]*>")


def _annotate_by_section(html: str, claims: list) -> str:
    """**제목 계보가 그 계를 말할 때만** 표식한다 (절 = h1–h6 사이 구간).

    왜 제목 계보인가: 마감된 축의 수(0.222·0.224·0.371)는 다른 계에도 그냥 나온다 —
    실측 오탐 셋 `LPSOCl β 표 0.371` · `LiCl 엑셀 1.335` · `Nd σ-drop Ea 0.224`. 값만
    보면 못 가른다. `qualify_hit` 의 문맥 창(앞 240자)은 너무 좁아 표 한 장 건너 있는
    절 제목(`### 15-4. ⛔ b2o3 Ea·σ 철회`)을 못 본다. 반대로 절 **본문** 전체를 보면
    긴 절(open_items §11) 안의 무관한 수까지 딸려 들어온다. 가운데가 제목 계보다 —
    조상 제목 + 자기 제목만 본다. 문서 제목(h1)도 계보에 든다(handoff 문서가 그렇다).

    ⛔ 못 하는 것
      · 계 이름을 못 대는 위험 행(`claim` 필드 없음)은 **표식하지 않는다.** 게이트를
        걸 근거가 없는 채로 넓은 수를 칠하면 오탐이 진짜 경고를 묻는다.
      · 제목에 계 이름이 없는 절은 못 잡는다 — 본문에만 있으면 놓친다(미탐 방향).
      · 한 절이 두 계를 함께 말하면 못 가른다.
    """
    groups: dict = {}
    for c in claims:
        toks = tuple(t for t in (c.get("system_tokens") or ()) if t)
        if not toks:
            continue                       # 계를 못 대면 게이트를 못 건다 → 안 칠한다
        groups.setdefault(toks, []).append(c)
    if not groups:
        return html
    out, chain = [], {}                    # chain: {레벨: 그 레벨의 현재 제목 텍스트}
    for sec in _SECTION_SPLIT.split(html):
        m = _HEAD_OPEN.match(sec)
        if m:
            lv = int(m.group(1))
            for k in [k for k in chain if k >= lv]:
                del chain[k]
            ht = _HEAD_TEXT.search(sec)
            chain[lv] = _TAGS.sub(" ", ht.group(1)) if ht else ""
        ctx = " ".join(chain[k] for k in sorted(chain)).lower()
        use = [c for toks, cs in groups.items() if any(t in ctx for t in toks) for c in cs]
        out.append(_C.annotate_claims(sec, claims=use)[0] if use else sec)
    return "".join(out)


_CACHE: dict = {"key": None, "out": None}


def _claims_cached(root=None) -> list:
    base = Path(root) if root else _ROOT
    f = base / "db" / "properties" / "citation_hazards.json"
    try:
        k = (str(base), f.stat().st_mtime_ns)
    except OSError:
        k = (str(base), 0)
    if _CACHE["key"] != k:
        _CACHE.update(key=k, out=closed_axis_claims(root=root))
    return _CACHE["out"]


def mark_closed_axis(html, root=None):
    """렌더된 조각에서 **마감된 축의 수**에 표식을 얹는다 → 같은 타입으로 돌려준다.

    왜 필요한가 (2026-09-09 실측 누출): 마감 결정 `D-2026-09-07-b2o3-md-closure-
    retrospective` 는 b2o3 UMA-MD 축 **전체**(D·Ea·σ·구간 Ea, “0.222 eV 포함”)를
    닫았는데, 스캐너 어휘는 레지스트리 수 둘(0.199·0.2234)뿐이라 아래가 **초록인 채로**
    금지된 수를 권했다:
      · /requests “✅ 쓸 수 있는 것: 저온 구간 Ea = 0.2241 ± 0.0606 eV”
      · /todo    “대신 쓸 것은 저온 구간 Ea 다”(바로 앞이 0.222 / 0.077)
      · /api/handoff/b2o3_arrhenius_curvature_2026_08_23 “✅ 600→800 구간 Ea = 0.222 eV”
    /methods 는 사람이 손으로 취소선을 그어 막고 있었다 — 사람 눈이 지키는 규율은
    다음에 또 샌다.

    ⚠ 실패해도 화면을 죽이지 않는다. 다만 **조용히 통과시키지도 않는다** — 시험이
      음성 경로(가짜 원장을 주면 표식이 안 붙는다)를 따로 잡는다.
    """
    if not html:
        return html
    try:
        claims = _claims_cached(root=root)
        if not claims:
            return html
        out = _annotate_by_section(str(html), claims)
    except Exception:                                   # noqa: BLE001
        return html
    try:
        from markupsafe import Markup
        return Markup(out) if hasattr(html, "__html__") else out
    except Exception:                                   # noqa: BLE001
        return out


# ── /log 타임라인 (묶음 H) ────────────────────────────────────────────────────
#: 표시층 어휘 통일. ⛔ journal.jsonl 의 과거 kind 문자열은 **고치지 않는다** —
#: 여기서 접을 뿐이다. 왼쪽이 파일에 실제로 있는 값, 오른쪽이 화면 어휘다.
KIND_MAP = {
    "note": "메모", "메모": "메모", "plan": "메모", "미결": "메모",
    "decision": "결정", "결정": "결정", "retract": "결정", "정정": "결정", "fix": "결정",
    "calc": "계산", "compute": "계산",
    "result": "결과", "결과": "결과", "analysis": "결과", "review": "결과",
    "figure": "그림", "figures+db": "그림",
    "tool": "도구", "도구": "도구", "webapp": "도구",
    "data": "자료", "db": "자료", "kb": "자료", "litdb": "자료",
    "db+kb": "자료", "kb+webapp": "자료",
}
#: 칩 순서 = 화면 순서. 여기 없는 값은 접지 않고 **원문 그대로** 보인다(“기타”가 아니다).
KIND_ORDER = ("결정", "계산", "결과", "그림", "도구", "자료", "메모")


def kind_label(raw: str) -> str:
    """저장된 kind → 화면 어휘. 모르는 값은 **원문 그대로** 돌려준다."""
    return KIND_MAP.get(str(raw or "").strip(), str(raw or "").strip() or "메모")


def _day(ts: str) -> str:
    s = str(ts or "")[:10]
    return s if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s) else ""


def journal_groups(entries, gap_note=None) -> list:
    """저널 항목 → 날짜 묶음 `[{date, n, items, gap}]` (최신순).

    · 정렬은 **파일 줄 순서가 아니라 `ts`** 다. journal.jsonl 자체가 시간순이 아니다
      (실측 어긋난 쌍 3개: 08-04T23:59>23:40 · 08-06T03:00>08-04T13:44 · 08-25T14:30>13:30).
    · `ts` 가 없거나 깨진 줄은 **버리지 않고** 맨 뒤 `date=""`(시각 없음) 묶음에 모은다.
    · 날짜 묶음 **사이가 비면** 그 사실을 `gap` 으로 남긴다 — 비어 있는 것과 일이
      없었던 것은 다른 말이다. `gap_note` 는 그 구간에 무엇이 있었는지(커밋 수 등)를
      부르는 쪽이 넘긴다. **여기서 지어내지 않는다.**

    ⛔ 못 하는 것: 기록이 옳은지 판정하지 않는다. 본문은 한 글자도 안 고친다.
    """
    dated, undated = [], []
    for e in entries or []:
        (dated if _day(e.get("ts")) else undated).append(e)
    dated.sort(key=lambda e: str(e.get("ts") or ""), reverse=True)
    groups = []
    for e in dated:
        d = _day(e.get("ts"))
        if not groups or groups[-1]["date"] != d:
            groups.append({"date": d, "items": [], "gap": None})
        groups[-1]["items"].append(e)
    # 묶음 사이의 빈 구간 — 이틀 이상 벌어진 자리에만 적는다(하루 건너뛴 건 갭이 아니다).
    for i in range(len(groups) - 1):
        try:
            a = _dt.date.fromisoformat(groups[i]["date"])
            b = _dt.date.fromisoformat(groups[i + 1]["date"])
        except ValueError:
            continue
        if (a - b).days > 2:
            lo = (b + _dt.timedelta(days=1)).isoformat()
            hi = (a - _dt.timedelta(days=1)).isoformat()
            groups[i]["gap"] = {"from": lo, "to": hi, "days": (a - b).days - 1,
                                "note": (gap_note or {}).get((lo, hi), "")}
    if undated:
        groups.append({"date": "", "items": undated, "gap": None})
    for g in groups:
        g["n"] = len(g["items"])
    return groups


# ── kb/results handoff 격자 (묶음 H) ─────────────────────────────────────────
_DATE_IN_NAME = re.compile(r"(20\d\d)[_-](\d\d)[_-](\d\d)")


def handoff_cards(paths, first_line=None) -> list:
    """kb/results/*.md → 카드 `[{id, name, date, comps, first}]`, **날짜 역순**.

    종전 정렬은 `sorted(..., reverse=True)` = 파일명 역알파벳순이라 첫 줄이
    vgcf·uma·slide2 였다. 파일명 안의 날짜를 1차 키로 쓴다 — 날짜가 없는 문서는
    **뒤로 보내되 지우지 않는다**(`date=""`).

    ⛔ 못 하는 것: 파일 안을 열어 날짜를 찾지 않는다. 파일명에 없으면 “날짜 미상”이다.
    """
    from data import COMPOSITIONS  # 지연 import — 이 모듈이 data 를 끌고 오지 않게
    out = []
    for p in paths:
        stem = p.stem if hasattr(p, "stem") else str(p)
        m = _DATE_IN_NAME.search(stem)
        date = "-".join(m.groups()) if m else ""
        low = stem.lower()
        comps = [c for c in COMPOSITIONS if c and c.lower() in low]
        first = ""
        if first_line is not None:
            first = first_line(p) or ""
        out.append({"id": stem, "name": stem.replace("_", " "), "date": date,
                    "comps": comps, "first": first})
    out.sort(key=lambda r: (r["date"] or "0000-00-00", r["id"]), reverse=True)
    return out


_FIRST_CACHE: dict = {}


def first_sentence(path, limit=140) -> str:
    """md 첫 문장 한 줄 — 제목·인용·빈 줄은 건너뛴다. 못 읽으면 빈 문자열.

    ⚠ mtime 으로 캐시한다 — /log 한 번에 kb/results 94개를 열기 때문이다.
    ⛔ 못 하는 것: 요약이 아니다. **첫 문장을 그대로** 자를 뿐이라 그 문서의 결론이
      아닐 수 있다 (카드가 판정을 대신 말하지 않게 하려는 것이기도 하다).
    """
    p = Path(path)
    try:
        key = (str(p), p.stat().st_mtime_ns, limit)
    except OSError:
        return ""
    if key in _FIRST_CACHE:
        return _FIRST_CACHE[key]
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    out = ""
    for ln in txt.splitlines():
        t = ln.strip()
        if not t or t.startswith(("#", ">", "---", "|", "```", "!")):
            continue
        t = re.sub(r"[*`_~]+", "", t).strip()
        if len(t) < 8:
            continue
        out = t[:limit] + ("…" if len(t) > limit else "")
        break
    _FIRST_CACHE[key] = out
    return out


def _selftest() -> int:
    """양성·**음성** 양쪽. 음성이 없는 selftest 는 통과해도 아무것도 보증 못 한다."""
    bad = 0

    def ck(name, cond):
        nonlocal bad
        if not cond:
            bad += 1
            print("FAIL", name)

    # ① 파생: 실제 원장에서 마감 축 어휘가 나온다 + b2o3 구간 Ea 두 표기를 덮는다
    cl = closed_axis_claims()
    vals = {c["text"] for c in cl}
    ck("closed_axis_claims 비어있지 않다", bool(cl))
    ck("0.222 포함", "0.222" in vals)
    ck("0.2241 포함(자릿수 확장)", "0.2241" in vals)
    ck("결속 id 가 원장 어휘 안", all(c["id"] in _C.hazard_ids() for c in cl))
    # ② 음성: 살아있는 정본(밴드갭 1.9671)에는 표식을 안 붙인다
    ck("살아있는 정본 미포함", "1.9671" not in vals)
    # ③ 양성: 실제 누출 문장(제목 계보에 계 이름이 있다)에 표식이 붙는다
    leak = "<p>✅ 쓸 수 있는 것: 저온 구간 Ea = 0.2241 ± 0.0606 eV</p>"
    got = mark_closed_axis("<h3>15-4. ⛔ b2o3 Ea·σ 철회</h3>" + leak)
    ck("누출 문장 표식", "claim-flag" in got and "⛔" in got)
    # ④ 음성: 같은 수라도 **제목이 그 계를 말하지 않으면** 안 붙는다
    #    (실측 오탐: `Nd σ-drop (Ea 0.224)` · `LiCl 엑셀 1.335` · `LPSOCl β 0.371`)
    ck("다른 계 미표식",
       "claim-flag" not in mark_closed_axis("<h3>Nd σ-drop</h3><p>Ea 0.224 불변</p>"))
    ck("계 없는 제목 미표식", "claim-flag" not in mark_closed_axis("<h3>메모</h3>" + leak))
    # ⑤ 음성: 관계없는 수에는 안 붙는다
    ck("무관한 수 미표식", "claim-flag" not in
       mark_closed_axis("<h3>b2o3</h3><p>격자상수 5.9999 Å</p>"))
    # ⑥ 음성: 자릿수 확장은 세 자리부터 — `1.33` 을 `1.335` 로 펴지 않는다
    ck("2자리 토큰 미확장", "1.335" not in {c["text"] for c in cl})
    # ⑦ 음성: 원장이 없는 뿌리를 주면 **조용히 통과하지 않고** 빈 어휘가 된다
    ck("빈 뿌리 → 어휘 0", closed_axis_claims(root="/nonexistent-root") == [])
    ck("빈 뿌리 → 원문 그대로",
       mark_closed_axis("<p>0.222 eV</p>", root="/nonexistent-root") == "<p>0.222 eV</p>")

    # ⑧ 저널 정렬·갭 (양성 + 음성)
    ent = [{"ts": "2026-08-04T23:40", "text": "a"}, {"ts": "2026-08-04T23:59", "text": "b"},
           {"ts": "2026-09-08T18:00", "text": "c"}, {"ts": "", "text": "d"}]
    g = journal_groups(ent)
    ck("최신 날짜가 먼저", g[0]["date"] == "2026-09-08")
    ck("같은 날 안에서도 ts 내림차순", g[1]["items"][0]["ts"] == "2026-08-04T23:59")
    ck("시각 없음 묶음 유지", g[-1]["date"] == "" and g[-1]["n"] == 1)
    ck("갭 표시", g[0]["gap"] and g[0]["gap"]["from"] == "2026-08-05")
    ck("갭 없으면 None", journal_groups([{"ts": "2026-09-08T01:00"}])[0]["gap"] is None)

    # ⑨ kind 어휘 (음성: 모르는 값은 원문 그대로)
    ck("kind 매핑", kind_label("webapp") == "도구" and kind_label("결과") == "결과")
    ck("모르는 kind 원문 유지", kind_label("zzz-unknown") == "zzz-unknown")

    # ⑩ handoff 정렬 (음성: 날짜 없는 문서가 사라지지 않는다)
    cards = handoff_cards([Path("a_2026_07_02.md"), Path("z_2026_09_08.md"),
                           Path("nodate_doc.md")])
    ck("날짜 역순", [c["id"] for c in cards][:2] == ["z_2026_09_08", "a_2026_07_02"])
    ck("날짜 없는 것 보존", any(c["id"] == "nodate_doc" and c["date"] == "" for c in cards))
    print("selftest:", "OK" if not bad else f"{bad} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    print(__doc__)
