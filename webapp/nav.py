#!/usr/bin/env python3
"""nav.py — 사이드바 · ⌘K 검색 · 온보딩 숫자의 **단일 출처** (v3 묶음 A).

왜 만들었나
  base.html 사이드바(21줄)와 data.py 의 ⌘K pages 목록(15줄)을 사람이 각각 손으로
  유지해서 갈라졌다 — /governance /ledger /fairchem /seminar /requests /sdcp 6개가
  검색에 안 나왔다. 손으로 맞춘 두 목록은 반드시 또 갈라진다. 그래서 목록을 여기
  하나만 둔다.

  · 사이드바  → base.html 이 `NAV`(=sidebar()) 를 받아 그린다
  · ⌘K       → data.search_index() 가 search_pages() 를 그대로 쓴다
  · 짝 검사   → tests/test_v3_nav.py 가 "nav href ⊆ 검색 url" 을 확인한다

⛔ 이 모듈이 **못 하는 것** (한계를 먼저 적는다)
  · 라우트가 실제로 있는지 확인하지 않는다. 여기 url 을 적어도 app.py 에 라우트가
    없으면 404 다. 짝 검사 시험은 nav↔검색만 본다 — 존재 확인은 test_v3_nav.py 의
    `test_nav_hrefs_are_live` 가 따로 한다.
  · 캠페인 지위를 **판정하지 않는다.** 배지는 db(결정 원장·마감/보고량 카드)에 있는
    것을 세기만 한다. 없으면 배지도 없다 — 0 으로 찍지 않는다.
  · 조성이 '활성'인지 판단하지 않는다. 붙어 있는 자료 수로 정렬할 뿐이다.
  · 온보딩 4칸은 db 를 못 읽으면 n=None 을 낸다. **0 으로 메우지 않는다** —
    "없다" 와 "못 읽었다" 는 화면에서 달라야 한다.
  · 표지(⭐⚠⛔…) 뜻은 규칙이 아니라 **관례**다. 지금 쓰인 것만 세어 보여 준다.

selftest:  python3 webapp/nav.py --selftest
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────────────────────────────────────────
# 1) 사이드바 선언 — 여기가 정본이다
# ─────────────────────────────────────────────────────────────────────────
# v3 6묶음 (.v3_survey/00_PLAN.md "v3 사이드바"):
#   오늘 / 값 / 어떻게 쟀나 / 캠페인 / 문헌 / 자료·보관
# ⚠ Dashboard 는 지금처럼 머리말 없는 첫 묶음으로 둔다 — 그래야 ⚖ 판정 원장이
#   **두 번째 묶음 첫 줄**이 된다(승격 요구). 종전 위치는 5번째 묶음 5번째 줄이었다.
#
# item 필드
#   url    : 링크 (⌘K 에도 이 url 이 그대로 들어간다)
#   label  : 화면·검색에 쓰는 이름
#   icon   : 사이드바 아이콘 (aria-hidden)
#   sub    : ⌘K 부제 = "이 페이지가 뭐 하는 곳인가" 한 줄
#   active : app.py 가 render_template 에 넘기는 active= 값
#   also   : 이 값들도 부모 강조 (예: /log 는 requests·sdcp 하위를 가진다)
#   nsub   : True 면 하위 항목(들여쓰기 + 세로선)
#   kw     : ⌘K 추가 검색어 (label 은 자동으로 들어간다)
#   camp   : 캠페인 슬러그 — db 에서 배지를 만든다 (campaign_status)
SECTIONS: list[dict] = [
    {"id": "nav-top", "label": None, "items": [
        {"url": "/", "label": "Dashboard", "icon": "▦", "active": "home",
         "sub": "오늘 상태 · 커버리지 매트릭스 · 핵심 발견"},
    ]},
    # ── 2번째 묶음: 첫 줄이 판정 원장이다 ────────────────────────────────
    {"id": "nav-today", "label": "오늘", "items": [
        {"url": "/governance", "label": "판정 원장", "icon": "⚖", "active": "governance",
         "sub": "결정 · 인용 위험 · 산출물 소재 — 이 값을 써도 되나",
         "kw": "governance 판정 결정 원장 인용위험 hazard decision 유실"},
        {"url": "/todo", "label": "미결 리스트", "icon": "📋", "active": "todo",
         "sub": "판정 대기 · PDF 확보 대기 · ML 후속", "kw": "open items todo 미결"},
        {"url": "/log", "label": "작업 기록", "icon": "✎", "active": "log",
         "also": ["requests", "sdcp", "weekly"], "sub": "날짜별 작업 기록 · handoff · 주간 정리",
         "kw": "log journal 기록"},
        {"url": "/notes", "label": "메모", "icon": "📝", "active": "notes", "nsub": True,
         "sub": "날짜별 메모 · 코멘트 · 형광펜", "kw": "notes memo 메모 코멘트"},
        {"url": "/requests", "label": "1저자 요청", "icon": "✉", "active": "requests", "nsub": True,
         "sub": "1저자가 보낸 요청·지침 원문", "kw": "requests 요청 지침"},
        # 2026-09-14 — 주간보고를 쓸 때 "지난주 뭐 했나" 를 git log 471건에서 다시 캐고 있었다.
        #   정리는 kb 문서(kb/reports/weekly_*.md)에 두고 화면은 읽기만 한다 (작업 기록 하위).
        {"url": "/weekly", "label": "주간 정리", "icon": "📅", "active": "weekly", "nsub": True,
         "sub": "일주일 단위 정리 · 주간보고 초안 (kb/reports/weekly_*.md)",
         "kw": "weekly 주간 보고 주간보고 정리 report"},
    ]},
    # ── 값: 인용 전에 여기 ───────────────────────────────────────────────
    {"id": "nav-value", "label": "값 · 인용 전에 여기", "comps": True, "items": [
        {"url": "/explorer", "label": "Property Explorer", "icon": "▤", "active": "explorer",
         "sub": "정본 값 진입점 — 정렬·필터 물성 표 + provenance",
         "kw": "explorer 정본 canonical 물성"},
        {"url": "/compare", "label": "두 계 비교", "icon": "⇄", "active": "compare",
         "sub": "조성 간 비교 + 레이더", "kw": "compare comparison 비교"},
        {"url": "/elements", "label": "주기율표", "icon": "⊞", "active": "elements",
         "sub": "원소별 조성 탐색", "kw": "periodic table elements 주기율표 원소"},
    ]},
    # ── 어떻게 쟀나 ─────────────────────────────────────────────────────
    {"id": "nav-how", "label": "어떻게 쟀나", "items": [
        {"url": "/methods", "label": "Methods", "icon": "▤", "active": "methods",
         "sub": "계산 방법 canonical", "kw": "methods 방법 규약"},
        {"url": "/glossary", "label": "Glossary", "icon": "▧", "active": "glossary",
         "sub": "용어 설명집", "kw": "glossary 용어 사전"},
        {"url": "/fairchem", "label": "Fair-Chem·UMA", "icon": "⚛", "active": "fairchem",
         "sub": "UMA 모델 · 힘 벤치 · 사용 범위", "kw": "fairchem uma mlip"},
        {"url": "/benchmarks", "label": "Benchmarks", "icon": "🎯", "active": "bench",
         "sub": "외부 재현 표적 · 덱 정정 원장 · 판정 이력",
         "kw": "benchmark 벤치 재현 검증"},
        # ⚠ v3 안(00_PLAN)에는 /compute 자리가 없다. 라우트는 살아 있으므로
        #   지우지 않고 '어떻게 쟀나' 로 옮겼다 — 배치는 1저자 확인 대상.
        {"url": "/compute", "label": "계산 입력 생성", "icon": "⚡", "active": "compute",
         "sub": "조성×계산 → QE/UMA 입력 스캐폴드", "kw": "compute 계산 입력 qe"},
    ]},
    # ── 캠페인 (지위 배지는 db 에서) ──────────────────────────────────────
    {"id": "nav-camp", "label": "캠페인", "items": [
        {"url": "/composition/lpsocl", "label": "LPSOCl 3×3×1", "icon": "🧪",
         "sub": "O-doped LPSCl · 마감 조건 비준 캠페인",
         "camp": "lpsocl", "kw": "lpsocl 마감 closure box331"},
        {"url": "/sdcp", "label": "SDCP wave1", "icon": "🧪", "active": "sdcp",
         "sub": "SDCP 분자계 wave1 게이트 · 마감 카드",
         "camp": "sdcp", "kw": "sdcp wave1 orca 분자"},
        {"url": "/sdcp/self-doping", "label": "자가도핑 해설", "icon": "📖", "nsub": True,
         "sub": "배경지식 0 독자용 SDCP 해설", "kw": "self-doping 자가도핑 해설"},
        {"url": "/cascade", "label": "Cascade (Screening·ML)", "icon": "🤖", "active": "cascade",
         "sub": "47종 도핑 스크리닝 감사 — 승인 랭킹 0종",
         "camp": "cascade", "kw": "cascade screening ml 도핑 스크리닝"},
        {"url": "/cascade/rebuild", "label": "Cascade 재건 일지", "icon": "🧭", "active": "cascade",
         "sub": "보고량 카드 v4 · 리뷰 BN→BO→BP · 정적대조 완료 · 파일럿 실행 전",
         "camp": "cascade", "kw": "cascade rebuild 재건 일지 estimand 보고량 정적대조 static pair 파일럿 pilot"},
        {"url": "/li2s", "label": "LPSCl@Li₂S 계면상", "icon": "🔋", "active": "li2s",
         "sub": "0층 → 1층 400원자 → 자원 마감 → 120원자 소셀 (G-B2 탈락 · G-B3 통과)",
         "camp": "li2s", "kw": "li2s 계면상 interphase 소셀 smallcell 비정질 amorphous melt quench 담금질"},
        {"url": "/composition/modelc_nd_doped", "label": "Nd/O 공치환", "icon": "🧬",
         "sub": "Nd₂O₃-LPSCl · DFT 재채점 중",
         "camp": "nd", "kw": "nd ndo 공치환 neodymium"},
    ]},
    # ── 문헌 ────────────────────────────────────────────────────────────
    {"id": "nav-lit", "label": "문헌", "items": [
        {"url": "/literature", "label": "Literature", "icon": "▣", "active": "lit",
         "sub": "DEM/DFT digest · 발표덱 · 축별 대조", "kw": "literature 문헌 논문 litdb"},
    ]},
    # ── 자료 · 보관 (기본 접힘) ───────────────────────────────────────────
    {"id": "nav-arch", "label": "자료 · 보관", "fold": True, "items": [
        {"url": "/files", "label": "Files", "icon": "🗂", "active": "files",
         "sub": "그림·데이터·구조 전체 갤러리 (💬 코멘트)", "kw": "files 파일 그림 갤러리"},
        {"url": "/ledger", "label": "T·Q 원장", "icon": "🧾", "active": "ledger",
         "sub": "T·Q 항목 원장 (스냅샷)", "kw": "ledger 원장 tq"},
        {"url": "/seminar", "label": "Seminar", "icon": "🎤", "active": "seminar",
         "sub": "세미나 발표 자료", "kw": "seminar 세미나 발표"},
        {"url": "/nd-survey", "label": "Nd 치환 서베이", "icon": "🧬", "active": "nd",
         "sub": "원소 치환 문헌 54편 색인", "kw": "nd survey 서베이 치환"},
    ]},
]


def _items() -> list[dict]:
    """선언된 모든 nav 항목 (묶음 순서 그대로)."""
    return [it for sec in SECTIONS for it in sec["items"]]


def nav_page_urls() -> set:
    """사이드바가 거는 url 집합. 짝 검사의 왼쪽."""
    return {it["url"] for it in _items()}


def search_pages() -> list:
    """⌘K 의 '페이지' 항목 — data.search_index() 가 이걸 그대로 쓴다.

    반환 모양은 data.py 가 기대하는 `(t, label, sub, url)` 튜플이다.
    """
    return [("페이지", it["label"], it.get("sub", ""), it["url"]) for it in _items()]


def search_keywords() -> dict:
    """url → ⌘K 추가 검색어. label 은 data.py 가 이미 kw 에 넣는다."""
    return {it["url"]: it.get("kw", "") for it in _items() if it.get("kw")}


def pairing_gaps(nav_urls, search_urls) -> list:
    """짝 검사기 — 사이드바에는 있는데 검색에는 없는 url.

    ⛔ 못 하는 것: 반대 방향(검색에만 있는 url)은 위반이 아니다. 논문·용어·조성처럼
      사이드바에 없는 항목이 검색에는 당연히 더 많다.
    """
    return sorted(set(nav_urls) - set(search_urls))


# ─────────────────────────────────────────────────────────────────────────
# 2) Compositions — FAMILY_ORDER 로 묶고, 자료 없는 것은 접는다
# ─────────────────────────────────────────────────────────────────────────
#: 화면이 붙일 수 있는 자료(정본값 + 분석파일 + 구조)가 이 수 **이하**면
#: "계획됨(자료 없음)" 으로 접는다. 1 인 이유: comp3/4/5·modelc_v3 는 씨앗 구조
#: 파일 하나뿐이고, lic6 는 li3n 과 공유하는 CSV 한 장이 _PREFIX 로 딸려올 뿐이다.
#: ⚠ 접는 것이지 **지우는 게 아니다** — 이 목록은 캠페인 범위 선언이다.
PLANNED_EVIDENCE_MAX = 1


def _evidence(cid: str, D) -> int:
    """조성 하나에 화면이 붙일 수 있는 자료 수. 클수록 활성."""
    try:
        n_can = sum(1 for v in D.canonical_values(cid).values() if v is not None)
    except Exception:                                    # noqa: BLE001
        n_can = 0
    try:
        n_file = len(D.datafiles_for(cid))
    except Exception:                                    # noqa: BLE001
        n_file = 0
    try:
        n_str = len(D.structures_for(cid))
    except Exception:                                    # noqa: BLE001
        n_str = 0
    return n_can + n_file + n_str


def composition_groups(D=None) -> dict:
    """사이드바 Compositions — 대시보드와 **같은** FAMILY_ORDER 로 묶는다.

    반환 {"groups": [{"family", "items": [...]}, ...], "planned": [...]}
      · groups  : family 순서대로, 각 family 안(links)은 자료 많은 순(=활성 먼저)
      · planned : 자료가 PLANNED_EVIDENCE_MAX 이하인 조성 — 접힘 묶음

    인자 없이 부르면 db 트리 지문(mtime)으로 캐시한다 — `structures_for` 가 조성마다
    db/structures 를 rglob 해서 캐시 없이는 요청마다 0.5 s 다(실측). db 가 바뀌면
    지문이 바뀌어 자동으로 다시 센다("db 를 고치면 화면이 따라온다" 계약 유지).

    ⛔ 못 하는 것: '활성 캠페인' 을 판정하지 않는다. 붙은 자료 수로 줄을 세울 뿐이다.
      캠페인 지위는 db/governance 가 정하고, 그건 campaign_status() 가 따로 본다.
    ⛔ 또 못 하는 것: 캐시된 dict 를 그대로 돌려준다 — 받아서 고치지 마라(읽기 전용).
    """
    if D is None:
        import data as D                                  # noqa: N806  (지연 import — 순환 방지)
        try:
            sig = (D._dir_sig(D.DB / "structures", "**/*"),
                   D._dir_sig(D.DB / "properties", "**/*"),
                   D._dir_sig(D.DB / "spectra", "**/*"))
        except Exception:                                 # noqa: BLE001
            return _composition_groups(D)
        return _comp_groups_cached(sig)
    return _composition_groups(D)


@lru_cache(maxsize=4)
def _comp_groups_cached(_sig):
    import data as D                                      # noqa: N806
    return _composition_groups(D)


def _composition_groups(D) -> dict:
    ev = {cid: _evidence(cid, D) for cid in D.COMPOSITIONS}
    order = {cid: i for i, cid in enumerate(D.COMPOSITIONS)}   # 선언 순서 = 안정 정렬 기준
    groups, planned = [], []
    for fam in D.FAMILY_ORDER:
        rows = []
        for cid, c in D.COMPOSITIONS.items():
            if c.get("family") != fam:
                continue
            row = {"cid": cid, "label": c["label"], "formula": c["formula"],
                   "color": c["color"], "n": ev[cid]}
            (planned if ev[cid] <= PLANNED_EVIDENCE_MAX else rows).append(row)
        if rows:
            rows.sort(key=lambda r: (-r["n"], order[r["cid"]]))
            # "items" 가 아니라 "links" — Jinja 에서 dict.items 와 부딪힌다(위 주석 참조)
            groups.append({"family": fam, "links": rows})
    planned.sort(key=lambda r: order[r["cid"]])
    return {"groups": groups, "planned": planned}


# ─────────────────────────────────────────────────────────────────────────
# 3) 캠페인 지위 배지 — db 에 있는 것만 센다
# ─────────────────────────────────────────────────────────────────────────
def _slug_re(slug: str):
    """슬러그를 **토큰 경계**로 찾는 정규식.

    ⚠ 단순 부분문자열이면 `nd` 가 `hash-bou**nd**-carry` · `cascade_d_rel_estima**nd**`
      에 걸려 없는 배지가 생긴다(실측). 앞뒤가 영숫자가 아닐 때만 센다.
    """
    return re.compile(r"(?<![a-z0-9])" + re.escape(slug.lower()) + r"(?![a-z0-9])")


def campaign_status(slug: str, root=None) -> dict:
    """캠페인 슬러그 → {"decisions": n, "cards": n}. 손으로 쓴 요약은 반드시 낡는다.

      · decisions = 결정 원장에서 **살아 있는**(state=active) 것 중 id 에 슬러그가 든 수
      · cards     = db/properties 의 마감/보고량/사전등록 카드 파일 수

    ⛔ 못 하는 것: 그 결정이 이 캠페인에 **정말** 적용되는지 못 본다 — id 토큰
      매칭이다. 그래서 배지는 숫자만 내고 판정 문구는 내지 않는다.
    ⛔ 또 못 하는 것: 슬러그가 원장 id 어휘와 다르면 조용히 0 이 된다(배지가 안 뜬다).
      없는 것을 0 으로 찍는 것보다는 낫지만, 배지가 안 보이면 슬러그부터 의심할 것.
    """
    base = Path(root) if root else ROOT
    rx = _slug_re(slug)
    out = {"decisions": 0, "cards": 0}
    try:
        import canonical as C
        for d in C.decisions(root=str(base)).values():
            if rx.search(str(d.get("id", "")).lower()) and C.decision_state(d) == "active":
                out["decisions"] += 1
    except Exception:                                    # noqa: BLE001
        pass
    try:
        p = base / "db" / "properties"
        pat = re.compile(r"(closed|estimand|prereg)", re.I)
        out["cards"] = sum(1 for f in p.glob("*.json")
                           if rx.search(f.name.lower()) and pat.search(f.name))
    except Exception:                                    # noqa: BLE001
        pass
    return out


# ─────────────────────────────────────────────────────────────────────────
# 4) 사이드바 조립
# ─────────────────────────────────────────────────────────────────────────
def sidebar(D=None, root=None) -> list:
    """base.html 이 받는 최종 구조 — 묶음 + 항목 + (캠페인 배지)."""
    out = []
    for sec in SECTIONS:
        items = []
        for it in sec["items"]:
            row = dict(it)
            camp = row.pop("camp", None)
            if camp:
                st = campaign_status(camp, root=root)
                # 없으면 배지도 없다 (0 으로 찍지 않는다)
                bits = []
                if st["decisions"]:
                    bits.append(f"결정 {st['decisions']}")
                if st["cards"]:
                    bits.append(f"카드 {st['cards']}")
                row["badge"] = " · ".join(bits) or None
                row["badge_title"] = ("살아 있는 결정 · 마감/보고량 카드 수 — "
                                      "db/governance/decisions.json · db/properties/") if bits else None
            out_it = row
            items.append(out_it)
        # ⚠ 키 이름이 "items" 면 안 된다 — Jinja 에서 `sec.items` 가 **dict.items 메서드**로
        #   먼저 잡혀 `'builtin_function_or_method' object is not iterable` 로 죽는다.
        out.append({"id": sec["id"], "label": sec.get("label"),
                    "fold": bool(sec.get("fold")), "comps": bool(sec.get("comps")),
                    "links": items})
    return out


# ─────────────────────────────────────────────────────────────────────────
# 5) 온보딩 4칸 + 위험 배너 — 숫자는 전부 db 파생
# ─────────────────────────────────────────────────────────────────────────
#: h1 아래 한 줄 정체. 이 앱이 무엇인지 한 문장으로.
IDENTITY = ("황화물 고체전해질을 계산으로 스크리닝한 기록입니다. "
            "값보다 먼저 **그 값을 써도 되는지**를 봅니다.")


def onboard_stats(root=None) -> dict:
    """온보딩 4칸 + 위험 배너. 숫자는 손으로 쓰지 않는다.

    반환 {"cards": [...], "risk": {...}}
      card = {key, n, label, unit, url, src, why, err}
      n=None 은 **못 읽었다**는 뜻이다 (0 이 아니다). 화면이 그렇게 말해야 한다.

    ⛔ 못 하는 것: 값이 맞는지 보지 않는다. 원장에 몇 건 있는지만 센다.
    """
    base = str(Path(root) if root else ROOT)
    cards = []

    def _card(key, label, unit, url, src, why, fn):
        try:
            n, err = fn(), None
        except Exception as ex:                          # noqa: BLE001
            n, err = None, f"{type(ex).__name__}: {ex}"
        cards.append({"key": key, "n": n, "label": label, "unit": unit,
                      "url": url, "src": src, "why": why, "err": err})

    def _canon():
        import canonical as C
        # path 까지 root 로 잡아 준다 — 그래야 selftest 가 "db 를 치우면 숫자가 사라지는지"
        # 를 실제로 볼 수 있다 (root 만 넘기면 REGISTRY 상수를 계속 읽는다).
        reg = C.load_registry(path=Path(base) / "db/properties/canonical_registry.json",
                              root=base)
        return sum(1 for e in reg.get("entries", []) if e.get("status") == "canonical")

    def _hazards():
        import data as D
        return len(D.citation_hazards().get("hazards") or [])

    def _hazard_why():
        """29 건이 전부 '지금 금지' 는 아니다.

        원장에는 RESOLVED(해소됨)·SUPERSEDED(폐기됨)도 남아 있고 — 남기는 게
        규율이다 — /governance 는 그걸 빼고 `인용 금지(BLOCKED) 9건` 이라 찍는다.
        홈이 29 만 보여 주면 처음 온 사람은 두 화면에서 3배 다른 수를 보고
        둘 다 안 믿는다. 그래서 여기서 쪼개 말한다. 숫자는 손으로 안 쓴다.
        """
        try:
            import canonical as C
            import data as D
            rows = D.citation_hazards().get("hazards") or []
            # 화면이 세는 '지금 유효' 는 **금지가 살아 있는** 건수다 (BI-3 P0-1) —
            # level 로 세면 SUPERSEDED 인데 금지는 살아 있는 행을 빠뜨린다.
            live = sum(1 for z in rows if C.prohibition_active(z))
            blk = sum(1 for z in rows if z.get("level") == "BLOCKED")
            return ("철회·보류·조건부 등재 전건 — 지금 유효 %d · 그중 인용 금지 %d"
                    % (live, blk))
        except Exception:                                # noqa: BLE001
            # 못 세면 없는 수를 지어내지 않는다 — 원래 문장으로 돌아간다.
            return "철회·보류·조건부 — 쓰기 전에 여기부터"

    def _decisions():
        import canonical as C
        return sum(1 for d in C.decisions(root=base).values()
                   if C.decision_state(d) == "active")

    def _terms():
        import glossary as G
        return len(G.GLOSSARY)

    _card("canonical", "정본 값", "건", "/explorer",
          "db/properties/canonical_registry.json (status=canonical)",
          "인용해도 되는 값", _canon)
    _card("hazard", "인용하면 안 되는 것", "건", "/governance",
          "db/properties/citation_hazards.json",
          _hazard_why(), _hazards)
    _card("decision", "지금 살아 있는 결정", "건", "/governance",
          "db/governance/decisions.json (state=active)",
          "규칙이 언제 왜 바뀌었나", _decisions)
    _card("term", "용어", "개", "/glossary", "webapp/glossary.py",
          "모르는 말이 나오면 여기", _terms)

    # 위험 배너 — 유실은 되돌릴 수 없고, 유일본은 매체 하나가 죽으면 유실이 된다.
    risk = {"lost": None, "single": None, "err": None}
    try:
        import canonical as C
        art = C.artifacts(root=base).values()
        risk["lost"] = sum(1 for a in art if a.get("status") == "lost")
        risk["single"] = sum(1 for a in art
                             if a.get("copies") == 1 and a.get("status") != "lost")
    except Exception as ex:                              # noqa: BLE001
        risk["err"] = f"{type(ex).__name__}: {ex}"
    return {"cards": cards, "risk": risk, "identity": IDENTITY}


# ─────────────────────────────────────────────────────────────────────────
# 6) 범례 — 어휘를 손으로 쓰지 않는다
# ─────────────────────────────────────────────────────────────────────────
def status_legend(D=None) -> list:
    """상태 배지 범례를 `data._STATUS_BADGE` 에서 **그대로** 만든다.

    화면마다 어휘가 갈리는 걸 막는 게 그 dict 의 원래 목적이다. 여기서 문구를 다시
    쓰면 사본이 둘이 된다.

    같은 표시명(예: superseded·retracted → '철회')은 한 줄로 합치고, 설명은 **가장 긴
    것**을 쓴다(짧은 쪽이 정보를 덜 담는다). 그래서 '6종' 은 세어 나온 수지 손으로
    적은 수가 아니다.
    """
    if D is None:
        import data as D                                  # noqa: N806
    rows, by_label = [], {}
    for key, (label, fg, bg, desc) in D._STATUS_BADGE.items():
        if label in by_label:
            r = by_label[label]
            r["keys"].append(key)
            if len(desc) > len(r["desc"]):
                r["desc"] = desc
            continue
        r = {"label": label, "fg": fg, "bg": bg, "desc": desc, "keys": [key]}
        by_label[label] = r
        rows.append(r)
    return rows


#: 세 상태를 반드시 갈라 가르친다 — 지금은 셋이 같은 점선 회색 칸으로 뭉쳐 있다.
#: (뜻은 개념이라 db 에 없다. 대신 실물 예시·수는 아래 unknown_legend 가 db 에서 붙인다.)
UNKNOWN_KINDS = [
    {"key": "todo", "mark": "TODO", "label": "안 했다",
     "desc": "아직 계산·회수를 안 한 칸이다. 하면 값이 생긴다."},
    {"key": "na", "mark": "N/A", "label": "성립 안 한다",
     "desc": "이 계에는 정의되지 않거나 규율이 금지한 축이다 "
             "(예: 분자계에 주기 밴드갭, UMA-Li₃N)."},
    {"key": "noncite", "mark": "비인용", "label": "했는데 못 쓴다",
     "desc": "값은 있는데 원자료가 인용을 금지했거나 게이트가 미평가다."},
]


def unknown_legend(D=None) -> list:
    """TODO / N/A / 비인용 3구분 + db 에서 붙인 실물 예시."""
    if D is None:
        import data as D                                  # noqa: N806
    rows = [dict(r) for r in UNKNOWN_KINDS]
    try:
        na = D.NOT_APPLICABLE
        rows[1]["n"] = len(na)
        # 규율상 금지 사례를 하나 골라 보인다 (진척률이 아니라 '금지' 라는 걸 보이려고)
        pick = next((v for (c, k), v in na.items() if c == "li3n"), None)
        rows[1]["example"] = pick or next(iter(na.values()), None)
    except Exception:                                    # noqa: BLE001
        pass
    try:
        import canonical as C
        reg = C.load_registry()
        rows[2]["n"] = sum(1 for e in reg.get("entries", [])
                           if e.get("status") in ("non_citable", "retracted"))
    except Exception:                                    # noqa: BLE001
        pass
    return rows


#: 카드 표지 — **규칙이 아니라 관례다.** 뜻은 여기 적되, 수는 실제 카드에서 센다.
#: 관례에 없는 표지가 나오면 '뜻 미정' 으로 그대로 드러낸다 (범례가 거짓말하지 않게).
MARK_MEANING = {
    "⭐": "비준 · 재현됨", "⚠": "주의 · 조건부", "⛔": "철회 · 인용 금지",
    "🔑": "교훈 · 규율", "🔴": "P0 · 지금 틀린 것", "✅": "완료",
}
_MARK_RE = re.compile(r"^\s*([^\w\s\d])")


def mark_legend(D=None) -> list:
    """카드 표지 범례 — 지금 화면에 실제로 쓰인 것만, 쓰인 수와 함께.

    ⛔ 못 하는 것: 카드가 표지를 **옳게** 달았는지 못 본다. 세기만 한다.
    """
    if D is None:
        import data as D                                  # noqa: N806
    try:
        cards = D.dashboard_highlights()
    except Exception:                                    # noqa: BLE001
        return []
    seen = {}
    for c in cards:
        m = _MARK_RE.match(str(c.get("t") or ""))
        if not m:
            continue
        seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    rows = [{"mark": k, "means": MARK_MEANING.get(k) or "뜻 미정 — 관례에 없다", "n": n}
            for k, n in seen.items()]
    rows.sort(key=lambda r: (-r["n"], r["mark"]))
    return rows


# ─────────────────────────────────────────────────────────────────────────
# selftest — 음성 경로(틀린 입력을 잡아내는지)까지
# ─────────────────────────────────────────────────────────────────────────
def _selftest() -> int:
    import sys
    bad = []

    def ck(cond, msg):
        if not cond:
            bad.append(msg)

    # ① 선언 자체의 무결성
    urls = [it["url"] for it in _items()]
    ck(len(urls) == len(set(urls)), f"nav url 중복: {sorted({u for u in urls if urls.count(u) > 1})}")
    ck(all(u.startswith("/") for u in urls), "nav url 이 '/' 로 시작하지 않는다")
    ck(len(SECTIONS) == 7, f"묶음 수가 7(머리말 없는 Dashboard + 6묶음)이 아니다: {len(SECTIONS)}")
    ck(SECTIONS[1]["items"][0]["url"] == "/governance",
       "판정 원장이 두 번째 묶음 첫 줄이 아니다")
    for u in ("/governance", "/ledger", "/fairchem", "/seminar", "/requests", "/sdcp"):
        ck(u in urls, f"검색에서 빠졌던 {u} 가 nav 선언에 없다")

    # ② 짝 검사기 — 양성 / **음성**
    ck(pairing_gaps({"/a", "/b"}, {"/a", "/b", "/c"}) == [], "짝 검사가 정상인데 위반을 냈다")
    ck(pairing_gaps({"/a", "/b"}, {"/a"}) == ["/b"],
       "짝 검사가 **빠진 url 을 못 잡는다** (음성 경로 실패)")
    ck(pairing_gaps(nav_page_urls(), set()) != [], "빈 검색 인덱스인데 위반이 0 이다 (음성 경로 실패)")

    # ③ search_pages 모양 — data.py 가 4-튜플로 언팩한다
    sp = search_pages()
    ck(all(isinstance(t, tuple) and len(t) == 4 for t in sp), "search_pages 가 4-튜플이 아니다")
    ck(all("items" not in s_ for s_ in sidebar()[0]), "사이드바 키에 'items' 가 있다 — Jinja 가 dict.items 로 잡는다")
    ck({t[3] for t in sp} == set(urls), "search_pages url 이 nav url 과 다르다")

    # ④ 범례가 _STATUS_BADGE 에서 나오는지 — 손으로 쓰면 여기서 걸린다
    import data as D
    leg = status_legend(D)
    ck({k for r in leg for k in r["keys"]} == set(D._STATUS_BADGE),
       "status_legend 가 _STATUS_BADGE 를 다 담지 않는다")
    ck(len(leg) == len({v[0] for v in D._STATUS_BADGE.values()}),
       "status_legend 표시명 합치기가 어긋났다")

    # ④-b 음성: 가짜 배지 dict 를 넣으면 그대로 따라와야 한다(=하드코딩이 아니다)
    class _Fake:
        _STATUS_BADGE = {"zz_test": ("가짜상태", "#000", "#fff", "시험용")}
    fk = status_legend(_Fake)
    ck(len(fk) == 1 and fk[0]["label"] == "가짜상태",
       "status_legend 가 입력 dict 를 안 따른다 — 어휘가 하드코딩됐다")

    # ⑤ 조성 묶음 — 자료 없는 것이 접히고, **지워지지 않는다**
    cg = composition_groups(D)
    shown = {r["cid"] for g in cg["groups"] for r in g["links"]} | {r["cid"] for r in cg["planned"]}
    ck(shown == set(D.COMPOSITIONS),
       f"조성이 사라졌다: {sorted(set(D.COMPOSITIONS) - shown)}")
    ck(all(r["n"] <= PLANNED_EVIDENCE_MAX for r in cg["planned"]), "planned 에 자료 있는 조성이 들어갔다")
    for g in cg["groups"]:
        ns = [r["n"] for r in g["links"]]
        ck(ns == sorted(ns, reverse=True), f"{g['family']} 묶음이 활성 순이 아니다")

    # ⑥ 온보딩 — 못 읽으면 None (0 아님)
    st = onboard_stats()
    ck(len(st["cards"]) == 4, "온보딩 칸이 4개가 아니다")
    ck(all(c["url"].startswith("/") for c in st["cards"]), "온보딩 칸에 갈 곳이 없다")
    ck(all(c["n"] is None or c["n"] >= 0 for c in st["cards"]), "온보딩 숫자가 이상하다")
    miss = onboard_stats(root="/nonexistent-root-for-selftest")
    ck(all(c["n"] in (None, 0) for c in miss["cards"] if c["key"] in ("canonical", "decision")),
       "db 가 없는데 숫자가 나왔다 — 하드코딩 의심 (음성 경로 실패)")
    ck(miss["risk"]["lost"] in (None, 0), "db 가 없는데 유실 수가 나왔다 (음성 경로 실패)")

    if bad:
        print("⛔ nav.py selftest 실패 %d건" % len(bad))
        for b in bad:
            print("  ·", b)
        return 1
    print("✅ nav.py selftest 통과 — 묶음 %d · 항목 %d · 조성 %d(접힘 %d)"
          % (len(SECTIONS), len(urls), len(shown), len(cg["planned"])))
    return 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        raise SystemExit(_selftest())
    print(__doc__)
