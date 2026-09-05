"""Obsidian vault writer: paper notes, keyword MOCs, digests, home MOC."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from . import __version__
from .config import Config
from .feedback import feedback_block, parse_note, verdict_of
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


def _scooping_block(a: dict) -> str:
    sc = a.get("scooping_alert") or {}
    if not sc.get("hit"):
        return ""
    return ("> [!danger] 선점 경보 — " + str(sc.get("target", "")) + "\n> " +
            str(sc.get("why", "")).replace("\n", " ") + "\n")


class Vault:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.root = cfg.path("vault.root")
        self.papers_dir = self.root / cfg.get("vault.papers_dir", "Papers")
        self.digests_dir = self.root / cfg.get("vault.digests_dir", "Digests")
        self.keywords_dir = self.root / cfg.get("vault.keywords_dir", "Keywords")
        self.borderline_dir = self.root / cfg.get("vault.borderline_dir", "Borderline")
        self.moc_path = self.root / cfg.get("vault.moc", "00_MOC/Research Agent Home.md")
        self.tz = ZoneInfo(cfg.timezone)
        for d in (self.papers_dir, self.digests_dir, self.keywords_dir,
                  self.borderline_dir, self.moc_path.parent):
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

    def borderline_path(self, p: Paper) -> Path:
        return self.borderline_dir / f"{self.note_name(p)}.md"

    # ------------------------------------------------- 피드백 보호 (P0 ①-b, 2026-09-05)
    def unharvested_feedback(self, path: Path, p: Paper) -> dict | None:
        """노트에 DB 가 모르는 판정이 적혀 있으면 그것을 돌려준다 (없으면 None).

        `_vault_sync` 는 harvest → write 순서로 돌지만, harvest 가 **어떤 이유로든**
        실패·누락하면 그 뒤의 재생성이 사용자 체크를 지운다. 실패 경로는 예외뿐이 아니라
        (sqlite 락, ra_id 파싱 실패, 경로 누락…) 여러 갈래라 **파일 단계에서 한 번 더** 막는다.
        디제스트의 `write_digest` 축소 덮어쓰기 거부와 같은 계열의 두 번째 겹이다.
        """
        if not path.exists():
            return None
        try:
            parsed = parse_note(path.read_text(encoding="utf-8"))
        except OSError:
            return None
        if not parsed:
            return None
        stored = (p.extra or {}).get("feedback") or {}
        if parsed["verdict"] == stored.get("verdict") and parsed.get("note", "") == (stored.get("note") or ""):
            return None
        return parsed

    # ------------------------------------------------------------------ paper
    def write_paper_note(self, p: Paper, digest_date: str | None = None) -> Path:
        path = self.note_path(p)
        pending = self.unharvested_feedback(path, p)
        if pending:
            print(f"[ra] 노트 보호: {path.name} 에 아직 안 걷은 피드백('{pending['verdict']}')이 있어 "
                  f"덮어쓰지 않았다. `ra feedback` 으로 먼저 걷으십시오.", flush=True)
            p.note_path = str(path.relative_to(self.cfg.root))
            return path
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
            "feedback": verdict_of(p) or "none",
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
            "c_exp": c.get("experimental") or "-",
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
            "scooping_block": _scooping_block(a),
            "feedback_block": feedback_block(p),
        }
        text = _render(self.cfg.load_template("paper_note"), mapping)
        path.write_text(text, encoding="utf-8")
        p.note_path = str(path.relative_to(self.cfg.root))
        return path

    # -------------------------------------------------- 경계선 stub (P0 ③, 2026-09-05)
    def write_borderline_stub(self, p: Paper) -> Path:
        """디제스트가 "잘못 뺀 게 있나" 를 물어본 논문에 **답할 자리**를 만든다.

        걸러진 논문은 분석이 없어 `_vault_sync` 가 노트를 안 만든다. 그런데 디제스트는
        "노트 맨 아래 `## 피드백`에 남기면 됩니다" 라고 안내했다 — 사용자는 Obsidian 을 열고
        그 논문을 못 찾는다. 그러면 오탈락 측정치가 구조적으로 영원히 0이 되고, 더 나쁘게는
        **"물어봤는데 답이 없으니 다 무관한 게 맞구나"** 로 읽힌다.

        그래서 판정만 받는 최소 노트를 `vault/Borderline/` 에 따로 만든다. Papers MOC 와
        분리해 논문 노트 위계를 어지럽히지 않는다.
        """
        path = self.borderline_path(p)
        pending = self.unharvested_feedback(path, p)
        if pending:
            print(f"[ra] 경계선 노트 보호: {path.name} 에 안 걷은 피드백이 있어 덮어쓰지 않았다.", flush=True)
            return path
        j = p.journal_canonical or p.venue or "저널 미상"
        link = (f"DOI: [{p.doi}](https://doi.org/{p.doi})" if p.doi else (f"URL: {p.url}" if p.url else ""))
        asked = ((p.extra or {}).get("borderline_asked_at") or "")[:10]
        body = "\n".join([
            "---",
            f'title: "{p.title.replace(chr(34), chr(39))}"',
            f'journal: "{j}"', f"year: {p.year or ''}", f'doi: "{p.doi or ""}"',
            f"if: {p.journal_if if p.journal_if is not None else ''}",
            f"relevance: {p.relevance if p.relevance is not None else ''}",
            "status: rejected", "tags: [borderline, research-agent]",
            f"asked_at: {asked}",
            f"feedback: {verdict_of(p) or 'none'}",
            f'ra_id: "{p.id}"',
            "---", "",
            f"# {p.title}", "",
            f"*{j}* {p.year or ''} · IF {p.journal_if} · 관련도 **{p.relevance}**",
            link, "",
            "> [!question] 이 논문은 관련도가 기준 바로 아래라 **걸러졌습니다.**",
            "> 잘못 뺀 것인지만 봐 주세요. 대부분 무관한 게 정상입니다 —",
            "> 이 칸은 걸러내는 기준이 너무 좁아지지 않았는지 재는 용도입니다.", "",
            "## 뺀 이유", "", p.relevance_reason or "(사유 없음)", "",
            "## 초록 / 스니펫", "",
            ("> " + (p.abstract or p.snippet or "(없음)").replace("\n", " ")), "",
            feedback_block(p), "",
            "---", f"*이 노트는 판정을 받기 위한 최소 노트입니다. 분석은 하지 않았습니다.*",
        ])
        path.write_text(body.rstrip() + "\n", encoding="utf-8")
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
            "## 선별 품질",
            f"- [[피드백 보정]] — 판정 {sum(1 for p in papers if verdict_of(p))}건 누적",
            "- 논문 노트 맨 아래 `## 피드백`에서 하나만 체크하면 반영된다",
            "",
            "## 사용법",
            "- 12:00 `ra noon` — alert 수집·triage·심층분석·DB·vault 갱신",
            "- 09:00 `ra morning` — 디제스트 생성·메일 발송",
            "- 주 1회 `ra feedback --show` — 체크박스 수집·보정 보고서 갱신",
            "- 수동: `ra ingest --json file.json`, `ra analyze --paper-id <id> --from-file <json>`, `ra status`",
            "",
            "```dataview",
            "TABLE tier, if, journal, relevance FROM \"Papers\" WHERE status != \"rejected\" SORT if DESC",
            "```",
        ]
        self.moc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return self.moc_path

    # ------------------------------------------------------------------ digest
    def write_digest(self, date: str, body: str, stats: dict, force: bool = False) -> Path:
        """Render a digest. NEVER destroys a richer existing digest.

        A regenerated digest can legitimately come out empty (the selection window moved on),
        and overwriting a written digest with that empty result loses work irrecoverably.
        So: refuse to overwrite when the new digest has fewer papers than the existing one,
        unless `force=True`. A refused write leaves the file untouched and logs why.
        """
        path = self.digests_dir / f"{date}.md"
        n_new = int(stats.get("n_papers", 0) or 0)
        if path.exists() and not force:
            n_old = self._digest_n_papers(path)
            if n_old is not None and n_new < n_old:
                print(f"[ra] digest 보호: {path.name} 은 {n_old}편인데 새로 만든 것은 {n_new}편 — "
                      f"덮어쓰지 않았다 (덮어쓰려면 --force).", flush=True)
                return path
        mapping = {"date": date, "body": body, "version": __version__,
                   "keyword_links": " · ".join(f"[[{k.get('vault_note') or k['name']}]]" for k in self.cfg.keywords),
                   **{k: str(v) for k, v in stats.items()}}
        text = _render(self.cfg.load_template("daily_digest"), mapping)
        if path.exists() and path.read_text(encoding="utf-8").strip() != text.strip():
            bak = self.digests_dir / ".backup"
            bak.mkdir(exist_ok=True)
            stamp = datetime.now(self.tz).strftime("%Y%m%d-%H%M%S")
            (bak / f"{date}.{stamp}.md").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        return path

    @staticmethod
    def _digest_n_papers(path: Path) -> int | None:
        """Read n_papers from an existing digest's frontmatter; None if unreadable."""
        try:
            head = path.read_text(encoding="utf-8")[:600]
            m = re.search(r"^n_papers:\s*(\d+)", head, re.M)
            return int(m.group(1)) if m else None
        except Exception:
            return None
