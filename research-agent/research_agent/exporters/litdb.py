"""litdb integration.

Two adapters, selected by config `litdb.mode`:

  cli   — John Kitchin's `litdb` (https://github.com/jkitchin/litdb): OpenAlex-backed local literature
          DB with vector search. We call `litdb add <doi>` for every accepted paper and (if supported)
          `litdb tag`/notes. Requires `litdb` on PATH and a litdb project (litdb.toml) at `litdb.project_dir`.

  file  — a repo-local literature DB (the user's own litdb in the branch). We append/merge records into
          `litdb.path` as JSONL (default) or SQLite (`litdb.format: sqlite`, table `papers`) using the
          field map in `litdb.field_map`. Adjust field_map once the real schema is known.

Both are idempotent (keyed by DOI, else by ra_id) and never delete.
"""
from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
from pathlib import Path

from ..config import Config
from ..models import Paper

DEFAULT_FIELD_MAP = {
    "id": "ra_id", "doi": "doi", "title": "title", "authors": "authors", "venue": "journal", "year": "year",
    "url": "url", "abstract": "abstract", "keywords_matched": "keywords", "journal_if": "impact_factor",
    "tier": "tier", "relevance": "relevance", "status": "status", "note_path": "note_path",
    "first_seen": "added", "analyzed_at": "analyzed",
}


def _record(p: Paper, field_map: dict) -> dict:
    d = p.to_dict()
    out = {}
    for src, dst in field_map.items():
        if src in d:
            out[dst] = d[src]
    a = p.analysis or {}
    out["summary"] = a.get("one_liner", "")
    out["selection_reason"] = a.get("selection_reason", "")
    out["key_findings"] = a.get("key_findings", [])
    out["citation_sentence"] = (a.get("use_in_my_paper") or {}).get("suggested_citation_sentence", "")
    out["tags"] = a.get("tags", [])
    out["source"] = "research-agent"
    return out


def export_file(cfg: Config, papers: list[Paper]) -> dict:
    fmt = cfg.get("litdb.format", "jsonl")
    path = cfg.path("litdb.path", "data/litdb.jsonl")
    fmap = cfg.get("litdb.field_map") or DEFAULT_FIELD_MAP
    recs = [_record(p, fmap) for p in papers if p.status != "rejected"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "sqlite":
        conn = sqlite3.connect(str(path))
        cols = sorted({k for r in recs for k in r})
        conn.execute(f"CREATE TABLE IF NOT EXISTS papers ({', '.join(c + ' TEXT' for c in cols)}, PRIMARY KEY(ra_id))")
        for r in recs:
            vals = [json.dumps(r.get(c), ensure_ascii=False) if isinstance(r.get(c), (list, dict)) else r.get(c) for c in cols]
            conn.execute(f"INSERT OR REPLACE INTO papers ({', '.join(cols)}) VALUES ({', '.join('?' for _ in cols)})", vals)
        conn.commit()
        conn.close()
        return {"mode": "file", "format": "sqlite", "path": str(path), "n": len(recs)}
    # jsonl: merge by key
    key = "doi"
    existing: dict[str, dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                existing[(r.get(key) or r.get("ra_id") or "")] = r
            except Exception:
                continue
    for r in recs:
        k = r.get(key) or r.get("ra_id") or ""
        merged = {**existing.get(k, {}), **{kk: vv for kk, vv in r.items() if vv not in (None, "", [], {})}}
        existing[k] = merged
    with open(path, "w", encoding="utf-8") as f:
        for r in existing.values():
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return {"mode": "file", "format": "jsonl", "path": str(path), "n": len(recs)}


def export_cli(cfg: Config, papers: list[Paper]) -> dict:
    bin_ = cfg.get("litdb.bin", "litdb")
    if shutil.which(bin_) is None:
        return {"mode": "cli", "error": f"`{bin_}` not on PATH — pip install litdb 후 litdb.project_dir에서 `litdb init`"}
    proj = cfg.path("litdb.project_dir", ".")
    added, skipped, failed = [], [], []
    for p in papers:
        if p.status == "rejected":
            continue
        if not p.doi:
            skipped.append(p.id)
            continue
        try:
            res = subprocess.run([bin_, "add", f"https://doi.org/{p.doi}"], cwd=str(proj), capture_output=True, text=True, timeout=120)
            (added if res.returncode == 0 else failed).append(p.doi)
        except Exception:
            failed.append(p.doi)
    return {"mode": "cli", "added": added, "skipped_no_doi": skipped, "failed": failed}


# ── markdown 어댑터 (2026-09-04) ─────────────────────────────────────────────
#  사용자의 실제 litdb 는 JSONL 도 SQLite 도 아니라 **Markdown digest** 다
#  (`litdb/papers/<slug>.md` + `INDEX.md` / `INDEX_DEM.md`).  `file` 어댑터로는 그 서랍에
#  못 쓴다 — 평행 JSONL 이 생기고 영영 안 합쳐진다.  그래서 세 번째 어댑터를 둔다.
#
#  ⛔ 이 어댑터가 **못 하는 것** (제일 중요하다):
#    · 실물 논문 없이 digest 를 채우지 못한다.  기존 카드는 §3 수치표·§4 계산사양·§5 그림·
#      §7 우리 대비까지 **논문 한 편 수준**이고, 그건 PDF·SI 를 읽어야 나온다.
#      ⇒ 이 어댑터는 **뼈대만** 만들고 못 채운 칸을 `⏳ 문서 대기` 로 **명시**한다.
#      status 를 `✅` 로 찍지 않는다 (`🌱 skeleton`).  사람이 PDF 를 주면 그때 채운다.
#    · **INDEX 를 건드리지 않는다.**  INDEX 항목은 손으로 쓴 분석 산문이라 자동 append 하면
#      오염된다.  대신 **제안 줄**을 따로 파일에 떨군다.
#    · 기존 카드를 **덮어쓰지 않는다** (중복 판정은 papers/ 전수로 — INDEX 로 하면 샌다).
_SKEL_STATUS = "🌱 skeleton (문서 대기)"


def _slug(p: Paper) -> str:
    """`<제1저자성><년도>_<제목낱말>` — 기존 208장의 규칙에서 뽑았다."""
    import re as _re
    import unicodedata as _ud

    def _ascii(s: str) -> str:
        return _ud.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")

    au = (p.authors or [""])[0]
    last = _ascii(au).replace(",", " ").split()[-1].lower() if _ascii(au).strip() else "unknown"
    last = _re.sub(r"[^a-z]", "", last) or "unknown"
    stop = {"the", "a", "an", "of", "for", "and", "in", "on", "with", "to", "by", "via",
            "using", "from", "into", "as", "at", "its", "their", "this", "that", "is", "are"}
    words = [w for w in _re.findall(r"[a-z0-9]+", _ascii(p.title).lower()) if w not in stop]
    return f"{last}{p.year or 'nd'}_{'_'.join(words[:6]) or 'untitled'}"


def _skeleton(p: Paper, slug: str) -> str:
    a = p.analysis or {}
    wait = "⏳ 문서 대기"
    authors = ", ".join(p.authors or []) or wait
    kf = a.get("key_findings") or []
    kf_md = "\n".join(f"- {x}" for x in kf) if kf else f"- {wait}"
    return f"""<!-- 🌱 research-agent 가 만든 **뼈대**다.  실물(PDF·SI)을 읽고 채워야 digest 가 된다.
     깊이 기준 = litdb/papers/_TEMPLATE.md · 실제 사례 = bazzoun2026_dem_fem_rnm_ionic.md.
     ⛔ `⏳ 문서 대기` 가 하나라도 남아 있으면 이 카드를 **인용하지 않는다**. -->
# {p.title or wait} — {(p.authors or [wait])[0]} ({p.journal_canonical or p.venue or wait} {p.year or ''})

> slug `{slug}` · DOI `{p.doi or wait}` · type `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)`
> · PDF `⏳ 미확보` · digested `{(p.first_seen or '')[:10]}` · status `{_SKEL_STATUS}`
> · evidence_level `{a.get('evidence_level') or getattr(p, 'evidence_level', None) or 'title'}`
> · IF `{p.journal_if if p.journal_if is not None else '?'}` · tier `{p.tier or '?'}` · relevance `{p.relevance if p.relevance is not None else '?'}`

## 0. 왜 이 카드가 열렸나 (research-agent 판정)
{a.get('selection_reason') or wait}

## 1. 한 줄 요약
{a.get('one_liner') or wait}

## 2. 메타
| 저자 | 저널/년 | DOI | 조성·계 | 연구유형 |
|---|---|---|---|---|
| {authors} | {p.journal_canonical or p.venue or wait} {p.year or ''} | {p.doi or wait} | {wait} | {wait} |

## 3. 핵심 물성 (수치) ★ 실물 필요
> ⛔ 초록만으로 채우지 말 것.  단위·조건 없는 값은 우리 db 와 **같은 표에 놓을 수 없다**.
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| {wait} |  |  |  |

## 4. 방법 ★ 실물 필요
- **code / version**: {wait}
- **축 A(DEM/MPM/복셀)**: 접촉모델·강성·마찰·압축압력·입경분포·셀·복셀 크기 —
- **축 B(DFT/MLIP)**: functional·vdW·pseudo/PAW·k-points·ecut·supercell·U·MLIP 학습셋 —
- **축 C(실험)**: 셀 구성·면적용량·온도·율·EIS 조건·등가회로 —
- **무질서·상태 선택 규칙**(있으면):
- **특이사항**:

## 5. Figure set ★ 실물 필요
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| {wait} |  |  |

## 6. Post-processing ★ 실물 필요
- **무엇**: (NEB / BVSE / COHP / TauFactor / Kirchhoff / Heckel / CNLS fit …)
- **도구**:
- **수치화·플롯 방식**:

## 7. 우리 대비 ★ 실물 필요 — 이 카드의 값어치는 여기서 나온다
- **어느 축인가**: (A: DEM/MPM/복셀 · B: DFT/MLIP · C: 실험 EIS · none)
- **우리 확보값과의 일치/충돌**: → `db/properties/canonical_registry.json`(축 B) ·
  `docs/db/section7_10case_sweep.csv`(축 A) 와 대조
- **인용 포인트**: (축 A = `main.tex` 절 이름 / 축 B = `kb/` 카드 또는 `db/properties/` 항목)
- **비판 포인트**: (보고량 정의가 있는가 · 상태 선택 규칙이 있는가 · 수렴을 보였는가 ·
  DEM↔MPM 을 서로 보정했는가[frame[4] 위반] · DOS-threshold 갭 · 단일시드 σ 비)

## 8. research-agent 초록 판정 (실물 판독으로 대체될 것)
{kf_md}

## 9. 남은 일
- [ ] PDF·SI 확보 → §3–§7 채우기
- [ ] `status` 를 `✅` 로, `evidence_level` 을 `fulltext` 로
- [ ] `INDEX.md`(argyrodite SE 축) 또는 `INDEX_DEM.md`(DEM 축)에 **손으로** 등재
"""


def export_markdown(cfg: Config, papers: list[Paper]) -> dict:
    """`litdb/papers/<slug>.md` 뼈대 생성. 기존 카드는 건드리지 않는다."""
    base = cfg.path("litdb.markdown_dir", "litdb/papers")
    base.mkdir(parents=True, exist_ok=True)
    have_doi = {}
    have_slug = set()
    for f in base.glob("*.md"):
        if f.stem.startswith("_"):
            continue
        have_slug.add(f.stem)
        head = f.read_text(encoding="utf-8", errors="replace")[:3000]
        for m in __import__("re").finditer(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", head):
            have_doi[m.group(0).rstrip(".,)`")] = f.stem
    written, skipped, proposals = [], [], []
    for p in papers:
        if p.status == "rejected":
            continue
        slug = _slug(p)
        if p.doi and p.doi in have_doi:
            skipped.append({"slug": slug, "why": "DOI 중복", "existing": have_doi[p.doi]})
            continue
        if slug in have_slug:
            skipped.append({"slug": slug, "why": "slug 중복", "existing": slug})
            continue
        (base / f"{slug}.md").write_text(_skeleton(p, slug), encoding="utf-8")
        have_slug.add(slug)
        if p.doi:
            have_doi[p.doi] = slug
        written.append(slug)
        proposals.append(
            f"| `papers/{slug}.md` | {(p.authors or ['?'])[0]} {p.year or ''} — {p.title or '?'} "
            f"(IF {p.journal_if if p.journal_if is not None else '?'} · tier {p.tier or '?'}) "
            f"⏳ **뼈대 — 실물 대기** | (축 미정) |")
    if proposals:
        pp = base.parent / "_INDEX_proposals.md"
        old = pp.read_text(encoding="utf-8") if pp.exists() else (
            "# INDEX 등재 제안 (research-agent 자동 생성)\n\n"
            "> ⛔ **여기서 INDEX.md 로 옮기는 것은 사람이 한다.** INDEX 항목은 손으로 쓴 분석\n"
            "> 산문이라 자동 append 하면 오염된다. 실물을 읽고 카드를 채운 뒤 등재할 것.\n\n")
        pp.write_text(old + "\n".join(proposals) + "\n", encoding="utf-8")
    return {"mode": "markdown", "dir": str(base), "written": written,
            "skipped": skipped, "index_proposals": len(proposals)}


def export(cfg: Config, papers: list[Paper]) -> dict:
    if not cfg.get("litdb.enabled", False):
        return {"mode": "disabled"}
    mode = cfg.get("litdb.mode", "file")
    if mode == "markdown":
        return export_markdown(cfg, papers)
    out = export_cli(cfg, papers) if mode == "cli" else export_file(cfg, papers)
    if cfg.get("litdb.also_file", False) and mode == "cli":
        out["file"] = export_file(cfg, papers)
    return out
