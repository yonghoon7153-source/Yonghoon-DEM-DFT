"""Obsidian vault writer: paper notes, keyword MOCs, digests, home MOC."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from . import __version__
from .config import Config
from .models import Paper, slugify

_TAG_BY_KEYWORD = {
    "dem battery": "paper/dem",
    "dft battery": "paper/dft",
    "anode-less assb": "paper/anode-free",
}


def _yaml_list(items: list[str]) -> str:
    return "[" + ", ".join(json.dumps(str(i), ensure_ascii=False) for i in items) + "]"


def _bullets(items, empty: str = "- (없음)") -> str:
    items = [str(i).strip() for i in (items or []) if str(i).strip()]
    return "\n".join(f"- {i}" for i in items) if items else empty


def _callout_lines(items, empty: str = "> - (없음)") -> str:
    items = [str(i).strip() for i in (items or []) if str(i).strip()]
    return "\n".join(f"> - {i}" for i in items) if items else empty


def _render(template: str, mapping: dict[str, str]) -> str:
    out = template
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", "" if v is None else str(v))
    return re.sub(r"\{\{[a-z_]+\}\}", "", out)


class Vault:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.root = cfg.path("vault.root")
        self.papers_dir = self.root / cfg.get("vault.papers_dir", "Papers")
        self.digests_dir = self.root / cfg.get("vault.digests_dir", "Digests")
        self.keywords_dir = self.root / cfg.get("vault.keywords_dir", "Keywords")
        self.moc_path = self.root / cfg.get("vault.moc", "00_MOC/Research Agent Home.md")
        self.tz = ZoneInfo(cfg.timezone)
        for d in (self.papers_dir, self.digests_dir, self.keywords_dir, self.moc_path.parent):
            d.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ names
    def note_name(self, p: Paper) -> str:
        fmt = self.cfg.get("vault.note_filename", "{year} - {first_author} - {short_title}")
        name = fmt.format(year=p.year or "n.d.", first_author=slugify(p.first_author, 30), short_title=p.short_title)
        return slugify(name, 120)

    def note_path(self, p: Paper) -> Path:
        year_dir = self.papers_dir / str(p.year or "unknown")
        year_dir.mkdir(parents=True, exist_ok=True)
        return year_dir / f"{self.note_name(p)}.md"

    # ------------------------------------------------------------------ paper
    def write_paper_note(self, p: Paper, digest_date: str | None = None) -> Path:
        a = p.analysis or {}
        m = a.get("methods") or {}
        c = a.get("connection_to_my_work") or {}
        u = a.get("use_in_my_paper") or {}
        tags = list(dict.fromkeys(
            [_TAG_BY_KEYWORD.get(k, f"paper/{slugify(k, 20).replace(' ', '-')}") for k in p.keywords_matched]
            + [f"tier/{p.tier}" if p.tier else "tier/none"]
            + [t.strip("#") for t in (a.get("tags") or [])]
        ))
        keyword_links = " · ".join(f"[[{k}]]" for k in p.keywords_matched) or "-"
        related = a.get("related_notes") or []
        mapping = {
            "title": p.title.replace('"', "'"),
            "short_title": p.short_title.replace('"', "'"),
            "authors_yaml": _yaml_list(p.authors[:12]),
            "authors_line": ", ".join(p.authors[:6]) + (" et al." if len(p.authors) > 6 else "") or "저자 미상",
            "journal": p.journal_canonical or p.venue,
            "year": p.year or "",
            "doi": p.doi or "",
            "url": p.url or "",
            "if": p.journal_if if p.journal_if is not None else "",
            "tier": p.tier or "-",
            "relevance": p.relevance if p.relevance is not None else "",
            "status": p.status,
            "keywords_yaml": _yaml_list(p.keywords_matched),
            "tags_yaml": _yaml_list(tags),
            "source": p.source,
            "date_added": p.first_seen[:10],
            "analyzed_at": (p.analyzed_at or "")[:10],
            "evidence_level": a.get("evidence_level", "pending"),
            "id": p.id,
            "doi_line": f"DOI: [{p.doi}](https://doi.org/{p.doi})" if p.doi else (f"URL: {p.url}" if p.url else ""),
            "keyword_links": keyword_links,
            "one_liner": a.get("one_liner") or "(분석 대기 중 — `ra analyze` 실행 필요)",
            "selection_reason": a.get("selection_reason") or p.relevance_reason or "",
            "key_findings_md": _bullets(a.get("key_findings")),
            "m_system": m.get("system", ""),
            "m_technique": m.get("technique", ""),
            "m_parameters_md": ", ".join(m.get("parameters") or []) or "-",
            "m_validation": m.get("validation", ""),
            "c_dem": c.get("dem") or "-",
            "c_dft": c.get("dft") or "-",
            "c_anode": c.get("anode_free") or "-",
            "numbers_md": _bullets(c.get("numbers_to_compare")),
            "u_intro": u.get("introduction", ""),
            "u_methods": u.get("methods", ""),
            "u_discussion": u.get("discussion", ""),
            "citation_sentence": u.get("suggested_citation_sentence", ""),
            "critique_md": _callout_lines(a.get("critique")),
            "follow_up_md": "\n".join(f"- [ ] {x}" for x in (a.get("follow_up") or [])) or "- [ ] (없음)",
            "abstract_block": ("> " + p.abstract.replace("\n", " ")) if p.abstract else ("> " + p.snippet if p.snippet else "> (초록 없음)"),
            "related_links": ", ".join(f"[[{r}]]" for r in related) or "-",
            "digest_link": f"[[{digest_date}]]" if digest_date else "-",
        }
        text = _render(self.cfg.load_template("paper_note"), mapping)
        path = self.note_path(p)
        path.write_text(text, encoding="utf-8")
        p.note_path = str(path.relative_to(self.cfg.root))
        return path

    # ---------------------------------------------------------------- keyword
    def write_keyword_mocs(self, papers: list[Paper]) -> list[Path]:
        out = []
        for kw in self.cfg.keywords:
            name = kw.get("vault_note") or kw["name"]
            rows = [p for p in papers if kw["name"] in p.keywords_matched and p.status != "rejected"]
            rows.sort(key=lambda x: (x.priority or 0), reverse=True)
            lines = [
                "---",
                f"title: \"{name}\"",
                f"tags: [keyword-moc, {_TAG_BY_KEYWORD.get(kw['name'], 'paper/other')}]",
                f"keyword: \"{kw['name']}\"",
                f"n_papers: {len(rows)}",
                "---",
                "",
                f"# {name}",
                "",
                f"> [!info] {kw.get('description', '')}" + ("" if kw.get("active", True) else " — **추적 중단(아카이브)**"),
                f"> Google Scholar alert 검색어 `{kw['name']}` · 누적 {len(rows)}편 · 갱신 {datetime.now(self.tz):%Y-%m-%d}",
                "",
                "| Tier | IF | 연도 | 노트 | 한 줄 |",
                "|---|---|---|---|---|",
            ]
            for p in rows:
                one = (p.analysis or {}).get("one_liner", "").replace("|", "/")
                lines.append(f"| {p.tier or '-'} | {p.journal_if if p.journal_if is not None else '-'} | {p.year or '-'} | [[{self.note_name(p)}]] | {one[:110]} |")
            path = self.keywords_dir / f"{slugify(name)}.md"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            out.append(path)
        return out

    # -------------------------------------------------------------------- home
    def write_home(self, papers: list[Paper], counts: dict, digests: list[str]) -> Path:
        tz_now = datetime.now(self.tz)
        top = [p for p in papers if p.status in ("analyzed", "digested")]
        top.sort(key=lambda x: (x.priority or 0), reverse=True)
        lines = [
            "---", "title: Research Agent Home", "tags: [moc, research-agent]", f"updated: {tz_now:%Y-%m-%d %H:%M}", "---", "",
            "# Research Agent Home", "",
            f"> [!summary] 상태 ({tz_now:%Y-%m-%d %H:%M} KST)",
            f"> 누적 {counts.get('total', 0)}편 · 분석 완료 {counts.get('analyzed', 0) + counts.get('digested', 0)}편 · triage 대기 {counts.get('triaged', 0)}편 · 제외 {counts.get('rejected', 0)}편 · research-agent v{__version__}",
            "",
            "## 키워드 MOC",
            *[f"- [[{k.get('vault_note') or k['name']}]] — {k.get('description', '')}" for k in self.cfg.keywords],
            "",
            "## 최근 디제스트",
            *([f"- [[{d}]]" for d in digests[:14]] or ["- (아직 없음)"]),
            "",
            "## 우선순위 상위 논문 (IF → 관련도)",
            "| # | Tier | IF | 저널 | 노트 |",
            "|---|---|---|---|---|",
            *[f"| {i+1} | {p.tier or '-'} | {p.journal_if} | {p.journal_canonical or p.venue} | [[{self.note_name(p)}]] |" for i, p in enumerate(top[:25])],
            "",
            "## 사용법",
            "- 12:00 `ra noon` — alert 수집·triage·심층분석·DB·vault 갱신",
            "- 09:00 `ra morning` — 디제스트 생성·메일 발송",
            "- 수동: `ra ingest --json file.json`, `ra analyze --paper-id <id> --from-file <json>`, `ra status`",
            "",
            "```dataview",
            "TABLE tier, if, journal, relevance FROM \"Papers\" WHERE status != \"rejected\" SORT if DESC",
            "```",
        ]
        self.moc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return self.moc_path

    # ------------------------------------------------------------------ digest
    def write_digest(self, date: str, body: str, stats: dict) -> Path:
        mapping = {"date": date, "body": body, "version": __version__,
                   "keyword_links": " · ".join(f"[[{k.get('vault_note') or k['name']}]]" for k in self.cfg.keywords),
                   **{k: str(v) for k, v in stats.items()}}
        text = _render(self.cfg.load_template("daily_digest"), mapping)
        path = self.digests_dir / f"{date}.md"
        path.write_text(text, encoding="utf-8")
        return path
