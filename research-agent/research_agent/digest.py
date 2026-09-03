"""Daily digest rendering.

The deterministic renderer below produces a complete, well-formed Obsidian digest from the analysis
JSON already stored in the DB — no LLM needed at 09:00. If an LLM backend is available and
`digest.llm_polish` is true, the body is additionally rewritten for flow (same facts, better prose).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from .config import Config
from .db import PaperDB
from .llm import LLM
from .models import Paper
from .vault import Vault


def select_for_digest(db: PaperDB, cfg: Config, since_hours: int | None = None) -> list[Paper]:
    """Papers analyzed since the last digest (or a window), not yet digested, excluding rejected."""
    last = db.last_digest()
    window_h = since_hours or int(cfg.get("mail.digest_window_hours", 36))
    since = datetime.now(timezone.utc) - timedelta(hours=window_h)
    since_iso = since.isoformat(timespec="seconds")
    if last and last.get("sent_at"):
        since_iso = min(since_iso, last["sent_at"])  # never skip papers analyzed between digests
    cands = [p for p in db.since(since_iso, "analyzed_at") if p.status == "analyzed"]
    # also include anything analyzed but never digested (e.g. first run / failed mail)
    for p in db.list(status="analyzed"):
        if p.id not in {c.id for c in cands}:
            cands.append(p)
    cands.sort(key=lambda x: (x.priority or 0, x.relevance or 0), reverse=True)
    return cands


def _paper_block(p: Paper, vault: Vault, depth: str) -> str:
    a = p.analysis or {}
    c = a.get("connection_to_my_work") or {}
    u = a.get("use_in_my_paper") or {}
    m = a.get("methods") or {}
    note = vault.note_name(p)
    journal = p.journal_canonical or p.venue or "저널 미상"
    doi_md = f" · [DOI](https://doi.org/{p.doi})" if p.doi else (f" · [link]({p.url})" if p.url else "")
    head = [f"### [[{note}]]",
            f"*{journal}* {p.year or ''} · IF **{p.journal_if}** · 관련도 **{p.relevance}** · {', '.join(p.keywords_matched)}{doi_md}",
            (f"_{', '.join(p.authors[:3])}{' et al.' if len(p.authors) > 3 else ''}_" if p.authors else "_저자 미확인 (로컬 enrich 필요)_"), ""]
    body: list[str] = []
    if a.get("one_liner"):
        body.append(f"> [!abstract] {a['one_liner']}")
        body.append("")
    body.append(f"**왜 골랐나** — {a.get('selection_reason') or p.relevance_reason}")
    body.append("")
    kf = [k for k in (a.get("key_findings") or []) if k]
    n_kf = {"A": 5, "B": 3, "C": 2}.get(depth, 3)
    if kf:
        body.append("**핵심 내용**")
        body += [f"- {k}" for k in kf[:n_kf]]
        body.append("")
    if depth in ("A", "B"):
        conn = [("DEM", c.get("dem")), ("DFT/MLIP", c.get("dft")), ("Anode-free", c.get("anode_free"))]
        conn = [(k, v) for k, v in conn if v and v.strip("-")]
        if conn or c.get("numbers_to_compare"):
            body.append("**내 연구 연결**")
            body += [f"- **{k}**: {v}" for k, v in conn]
            if depth == "A":
                body += [f"- 비교 수치: {n}" for n in (c.get("numbers_to_compare") or [])[:3]]
            body.append("")
        use = [("Intro", u.get("introduction")), ("Methods", u.get("methods")), ("Discussion", u.get("discussion"))]
        use = [(k, v) for k, v in use if v]
        if use:
            body.append("**논문 작성 활용** — " + " / ".join(f"*{k}*: {v}" for k, v in use))
            body.append("")
        if depth == "A" and u.get("suggested_citation_sentence"):
            body.append(f"> [!quote] {u['suggested_citation_sentence']}")
            body.append("")
        if depth == "A" and m.get("technique") and not str(m.get("technique")).lower().startswith("unknown"):
            body.append(f"**방법** — {m.get('system', '')} · {m.get('technique', '')}" + (f" · 검증: {m['validation']}" if m.get("validation") else ""))
            body.append("")
    crit = [x for x in (a.get("critique") or []) if x]
    if crit and depth != "C":
        body.append("**비판 포인트** — " + " / ".join(crit[:2]))
        body.append("")
    return "\n".join(head + body).rstrip() + "\n"


def _reference(i: int, p: Paper, vault: Vault) -> str:
    auth = ", ".join(p.authors[:3]) + (" et al." if len(p.authors) > 3 else "")
    auth = (auth.rstrip(".") + ". ") if auth else ""
    j = p.journal_canonical or p.venue
    link = f"[{p.doi}](https://doi.org/{p.doi})" if p.doi else (p.url or "")
    return f"{i}. {auth}{p.title.rstrip('.')}. *{j}* {p.year or ''}. {link} — [[{vault.note_name(p)}]]"


def render_body(papers: list[Paper], cfg: Config, vault: Vault, date: str) -> str:
    tiers = {"A": [], "B": [], "C": []}
    for p in papers:
        tiers.get(p.tier or "C", tiers["C"]).append(p)
    n = len(papers)
    kw_counts: dict[str, int] = {}
    for p in papers:
        for k in p.keywords_matched:
            kw_counts[k] = kw_counts.get(k, 0) + 1
    kw_str = ", ".join(f"{k} {v}편" for k, v in sorted(kw_counts.items(), key=lambda x: -x[1])) or "-"
    top = papers[0] if papers else None
    lines = [f"안녕하세요 용훈님, {date} 디제스트예요.",
             (f"오늘은 총 {n}편이고 키워드별로는 {kw_str}입니다. "
              + (f"가장 먼저 볼 논문은 *{top.journal_canonical or top.venue}*의 {top.first_author} 논문이에요." if top else "새로 분석된 논문이 없어요.")),
             ""]
    titles = {"A": "## Tier A — 반드시 읽을 것", "B": "## Tier B — 읽어볼 만함", "C": "## Tier C — 참고"}
    for t in ("A", "B", "C"):
        if not tiers[t]:
            continue
        lines.append(titles[t])
        lines.append("")
        for p in tiers[t]:
            lines.append(_paper_block(p, vault, t))
    # cross-cutting insight: derived deterministically from tags/keywords
    if papers:
        lines.append("## 오늘의 한 줄")
        themes = _themes(papers)
        lines.append(themes)
        lines.append("")
    lines.append("## References")
    lines += [_reference(i + 1, p, vault) for i, p in enumerate(papers)] or ["(없음)"]
    return "\n".join(lines).rstrip() + "\n"


def _themes(papers: list[Paper]) -> str:
    kws = {k for p in papers for k in p.keywords_matched}
    a_cnt = sum(1 for p in papers if p.tier == "A")
    parts = []
    if "dem battery" in kws:
        parts.append("DEM 쪽은 공정 파라미터(압축·혼합)와 미세구조 지표를 잇는 논문이 계속 나오고 있어, 내 porosity–percolation 결과를 공정 변수로 번역해 두면 인용 지점이 넓어진다")
    if "dft battery" in kws:
        parts.append("DFT/MLIP 쪽은 계산 조건(functional, supercell, 학습 데이터)이 결과를 좌우하므로 Methods에 내 조건을 명시하고 비교표를 만들어 두는 편이 좋다")
    if "anode-less assb" in kws:
        parts.append("anode-free 쪽은 계면(집전체·interlayer) 설계가 핵심 변수라, 셀 레벨 시뮬레이션 확장 시 경계조건으로 삼을 수 있다")
    if a_cnt:
        parts.append(f"Tier A {a_cnt}편은 이번 주 안에 SI까지 확인하는 것을 권한다")
    return " ".join(p + "." for p in parts) if parts else "오늘 논문들은 각자 독립적이라 공통 흐름은 뚜렷하지 않다."


def polish_with_llm(cfg: Config, llm: LLM, body: str, date: str) -> str:
    if not llm.available:
        return body
    system = cfg.load_prompt("digest") + "\n\n# [문체 규칙]\n" + cfg.load_prompt("style_guide")
    user = (f"날짜: {date}\n아래는 규칙 기반으로 생성한 디제스트 초안이다. 사실·수치·링크·위키링크·References는 그대로 두고 "
            f"문장만 자연스럽게 다듬어 전체 Markdown을 다시 출력하라.\n\n{body}")
    out = llm.complete(system, user)
    return out.strip() + "\n" if out and "## References" in out else body


def digest_stats(db: PaperDB, papers: list[Paper]) -> dict:
    counts = db.counts()
    week = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(timespec="seconds")
    return {
        "n_papers": len(papers),
        "n_a": sum(1 for p in papers if p.tier == "A"),
        "n_b": sum(1 for p in papers if p.tier == "B"),
        "n_c": sum(1 for p in papers if p.tier == "C"),
        "db_total": counts.get("total", 0),
        "n_week": len(db.since(week, "first_seen")),
        "n_rejected": counts.get("rejected", 0),
    }


def today_str(cfg: Config) -> str:
    return datetime.now(ZoneInfo(cfg.timezone)).strftime("%Y-%m-%d")
