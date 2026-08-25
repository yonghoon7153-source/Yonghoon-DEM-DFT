"""fairchem.py — Fair-Chem/UMA 공식 지식 번들 **읽기 전용** 로더.

번들(`db/knowledge/fairchem/`)은 2026-08-21 공식 repo 스냅샷
(commit 93a03d65…)에서 만들어진 것이고, 이 모듈은 그것을 **읽기만** 한다.

## 왜 읽기 전용인가 — 인계 문서의 규칙
> 우리 수치를 `db/fairchem` 에 복사해 **두 번째 정본**을 만들지 마.

역할 경계가 이미 정해져 있다:
  · PDF·그림 해석 → `litdb`      · 사람용 설명 → `kb`
  · 우리 수치 정본 → `db/properties`   · 판정 → `db/governance`
  · 이 번들 → 위 entity 를 **FK 로 연결하는 검색/관계 DB**

그래서 이 모듈은 값을 만들지 않는다. 링크만 만든다.

## 세 축을 절대 합치지 않는다
`http_status`(페이지가 열리나) · `execution_status`(예제가 도나) ·
`applicability`(우리 계에 쓸 수 있나) 는 **서로 다른 축**이다. 하나로 뭉쳐
"정상" 이라고 말하면 200 인데 실행 실패한 튜토리얼이 정상으로 보인다.

## 이 모듈이 **못 하는 것**
  · 번들을 갱신하지 않는다 (그건 `tools/fairchem_kb/build_fairchem_kb.py`).
  · 공식 체크포인트·논문 PDF 를 담지 않는다 (재배포 금지).
  · claim 의 참/거짓을 판정하지 않는다 — `claim_status` 를 옮길 뿐이다.
  · 우리 수치와 공식 수치를 **섞지 않는다**. crosswalk 는 FK 이지 값이 아니다.
"""
from __future__ import annotations

import hashlib
import json
import os
from functools import lru_cache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FCDIR = os.path.join(ROOT, "db", "knowledge", "fairchem")
MANIFEST = os.path.join(FCDIR, "_release_manifest.json")

#: 인계 문서의 탭 순서. 공식 사이트 구조를 따르되 뒤 셋이 우리 차별점이다.
SECTIONS = [
    ("overview", "Overview"),
    ("models", "Models & Tasks"),
    ("domains", "Application Domains"),
    ("datasets", "Datasets & Benchmarks"),
    ("papers", "Papers"),
    ("lpscl", "Our LPSCl Use"),
    ("claims", "Decisions & Limitations"),
    ("provenance", "Source & Provenance"),
]

#: 상태축 — **합치지 않는다.** 값이 이 목록 밖이면 UI 에서 'unknown' 으로 뜬다.
ENUMS = {
    "claim_status": ["proposed", "verified", "disputed", "superseded", "retracted"],
    "applicability": ["pass", "fail", "not_assessed", "inapplicable"],
    "citable_status": ["no", "conditional", "yes"],
    "execution_status": ["passed", "failed", "not_run", "not_applicable"],
}

#: paper 진행은 네 단계를 **따로** 보여준다 (하나로 합치면 '읽었다' 가 과장된다)
PAPER_STAGES = ["indexed", "digest_read", "figure_reviewed", "human_approved"]


def _read(name):
    p = os.path.join(FCDIR, name)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def manifest():
    return _read("_release_manifest.json") or {}


@lru_cache(maxsize=1)
def snapshot():
    return _read("snapshot.json") or {}


@lru_cache(maxsize=32)
def entities(name):
    """entity 목록. 없으면 빈 리스트 — 화면이 죽지 않게 한다."""
    o = _read(f"{name}.json")
    return o if isinstance(o, list) else []


@lru_cache(maxsize=4)
def blob(name):
    """dict 형태 관측치(live_link_audit / release_observations)."""
    o = _read(f"{name}.json")
    return o if isinstance(o, dict) else {}


def available():
    """번들이 설치돼 있나. 없으면 라우트가 404 대신 안내를 낸다."""
    return os.path.isfile(MANIFEST)


def verify_hashes(limit=None):
    """manifest 의 sha256 과 **실제 파일**을 대조한다.

    ⚠ 이게 이 모듈의 유일한 무결성 근거다. 번들은 외부에서 온 것이고,
      repo 에 들어온 뒤 누가 손대면 조용히 달라진다 — 그러면 화면이 공식
      스냅샷이라고 말하면서 다른 내용을 보여준다. **fail-closed** 로 다룬다.

    반환: {"ok": bool, "checked": n, "mismatch": [...], "missing": [...]}
    """
    m = manifest()
    files = m.get("files") or []
    if limit:
        files = files[:limit]
    mismatch, missing, checked = [], [], 0
    for f in files:
        rel = f.get("repo_path", "")
        want = f.get("sha256")
        # 번들 안의 repo_path 는 db/knowledge/fairchem/… 형태다
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            missing.append(rel)
            continue
        if not want:
            continue
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        checked += 1
        if h.hexdigest() != want:
            mismatch.append(rel)
    return {"ok": not mismatch and not missing, "checked": checked,
            "mismatch": mismatch, "missing": missing,
            "declared": len(m.get("files") or [])}


def envelope(data, warnings=None):
    """인계 문서가 정한 응답 봉투. 모든 API 가 같은 모양이어야 한다."""
    m = manifest()
    return {
        "schema_version": m.get("schema_version", "unknown"),
        "generated_at": m.get("generated_at"),
        "source_commit": m.get("official_source_commit"),
        "status": "ok" if not warnings else "warning",
        "warnings": warnings or [],
        "data": data,
    }


def page_status_rows():
    """site_pages 를 상태축 **셋으로 나눠** 준다 (합치지 않는다)."""
    rows = []
    for p in entities("site_pages"):
        rows.append({
            "page_id": p.get("page_id"),
            "source_path": p.get("source_path"),
            "title": p.get("title"),
            "nav_section": p.get("nav_section"),
            "in_toc": p.get("in_myst_toc"),
            "url": p.get("derived_live_url"),
            "http_status": p.get("http_status"),
            "content_status": p.get("content_status"),
            "execution_status": p.get("execution_status", "not_run"),
        })
    return rows


def crosswalk_rows():
    """LPSCl crosswalk — 우리 쪽 값을 **복사하지 않고** FK 만 들고 온다."""
    out = []
    for c in entities("lpscl_crosswalk"):
        out.append({
            "crosswalk_id": c.get("crosswalk_id"),
            "capability": c.get("fairchem_capability"),
            "project_use": c.get("project_use"),
            "official_task": c.get("official_task"),
            "project_status": c.get("project_status"),
            "project_rule": c.get("project_rule"),
            "paper_language": c.get("paper_language"),
            "n_sources": len(c.get("sources") or []),
        })
    return out


def papers_rows():
    """논문 목록 + 네 단계 진행. litdb 에 digest 가 있으면 그걸로 단계를 올린다.

    ⚠ 값을 litdb 에서 **복사하지 않는다** — 있는지 없는지(FK 존재)만 본다.
    """
    litdir = os.path.join(ROOT, "litdb", "papers")
    have = set()
    if os.path.isdir(litdir):
        have = {os.path.splitext(f)[0].lower() for f in os.listdir(litdir)
                if f.endswith(".md")}
    figdir = os.path.join(ROOT, "litdb", "figures")
    figs = set(os.listdir(figdir)) if os.path.isdir(figdir) else set()

    out = []
    for p in entities("papers"):
        pid = (p.get("paper_id") or "").lower()
        title = p.get("title") or ""
        # 느슨한 매칭: paper_id 가 digest 파일명에 들어 있으면 연결된 것으로 본다
        slug = next((h for h in have if pid and (pid in h or h in pid)), None)
        out.append({
            "paper_id": p.get("paper_id"),
            "title": title,
            "category": p.get("category"),
            "arxiv_url": p.get("arxiv_url"),
            "doi_url": p.get("doi_url"),
            "source_path": p.get("source_path"),
            "litdb_slug": slug,
            "stages": {
                "indexed": True,                       # 번들에 있으면 색인된 것
                "digest_read": bool(slug),
                "figure_reviewed": bool(slug and slug in figs),
                "human_approved": False,               # 사람만 올린다
            },
        })
    return out


def summary():
    """Overview 카드용 집계. 숫자만 세고 판정하지 않는다."""
    pv = verify_hashes()
    audit = blob("live_link_audit")
    papers = papers_rows()
    return {
        "release_id": manifest().get("release_id"),
        "source_commit": manifest().get("official_source_commit"),
        "commit_time": manifest().get("official_source_commit_time"),
        "counts": {k: len(entities(k)) for k in
                   ("models", "tasks", "datasets", "papers", "claims",
                    "technologies", "site_pages", "packages", "lpscl_crosswalk")},
        "integrity": pv,
        "link_audit": {
            "checked": audit.get("unique_internal_targets_checked"),
            "http_200": audit.get("http_200_targets"),
            "broken": len(audit.get("broken_targets") or []),
            "render_errors": len(audit.get("execution_render_findings") or []),
        },
        "papers_progress": {
            s: sum(1 for p in papers if p["stages"][s]) for s in PAPER_STAGES
        },
    }
