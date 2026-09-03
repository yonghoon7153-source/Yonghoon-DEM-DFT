"""Parser for Google Scholar alert e-mails.

Google Scholar alert mails (sender: scholaralerts-noreply@google.com) contain, per hit:

    <h3><a class="gse_alrt_title" href="https://scholar.google.com/scholar_url?url=<REAL_URL>&hl=..">Title</a></h3>
    <div style="color:#006621">A Author, B Author, C Author - Journal Name, 2026 - publisher.com</div>
    <div class="gse_alrt_sni">…snippet with <b>keyword</b> highlights…</div>

Subject variants (locale dependent):
    "New results for dem battery"        / "새로운 결과 - dem battery"
    "Google Scholar Alert - [ dem battery ]"
    "dem battery - new results"           / "[ dem battery ] - 새 검색결과"
    "New articles in ..." (author/citation alerts)

The parser is deliberately tolerant: it works on HTML when available and falls back to a
plain-text heuristic. It never raises on a malformed hit; it just skips it.
"""
from __future__ import annotations

import html as htmllib
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup

from ..models import Paper, paper_id_from

_KEYWORD_SUBJECT_RES = [
    re.compile(r"\[\s*(.+?)\s*\]"),                                   # [ dem battery ]
    re.compile(r"new results for\s+[\"“]?(.+?)[\"”]?\s*$", re.I),      # New results for dem battery
    re.compile(r"새로운 결과\s*[-–—:]\s*[\"“]?(.+?)[\"”]?\s*$"),        # 새로운 결과 - dem battery
    re.compile(r"^[\"“]?(.+?)[\"”]?\s*[-–—:]\s*(new results|새 검색결과|새로운 결과)", re.I),
    re.compile(r"new articles (?:for|in)\s+[\"“]?(.+?)[\"”]?\s*$", re.I),
]

_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def keyword_from_subject(subject: str) -> str:
    s = (subject or "").strip()
    for rx in _KEYWORD_SUBJECT_RES:
        m = rx.search(s)
        if m:
            return m.group(1).strip().strip('"“”').lower()
    return s.lower()


def unwrap_scholar_url(href: str) -> str:
    """scholar_url?url=<real>&... → <real>. Leaves other URLs untouched."""
    if not href:
        return ""
    try:
        u = urlparse(href)
        if "scholar.google" in (u.netloc or "") and u.path.endswith("scholar_url"):
            real = parse_qs(u.query).get("url", [""])[0]
            return unquote(real) if real else href
    except Exception:
        pass
    return href


_DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>?#&]+", re.I)


def doi_from_url(url: str) -> str | None:
    if not url:
        return None
    m = _DOI_RE.search(unquote(url))
    if not m:
        return None
    doi = m.group(0).rstrip(".,;)")
    # drop trailing path fragments publishers append (e.g. /full, /pdf)
    doi = re.sub(r"/(full|pdf|abstract|epdf|html)$", "", doi, flags=re.I)
    return doi


@dataclass
class ParsedHit:
    title: str
    url: str
    authors: list[str]
    venue: str
    year: int | None
    snippet: str

    def to_paper(self, keyword: str, message_id: str | None) -> Paper:
        doi = doi_from_url(self.url)
        return Paper(
            id=paper_id_from(self.title, doi),
            title=self.title,
            authors=self.authors,
            venue=self.venue,
            year=self.year,
            doi=doi,
            url=self.url,
            snippet=self.snippet,
            keywords_matched=[keyword] if keyword else [],
            source="scholar_email",
            alert_message_id=message_id,
        )


def _split_byline(byline: str) -> tuple[list[str], str, int | None]:
    """'A Author, B Author - Journal, 2026 - site.com' → (authors, venue, year)."""
    byline = htmllib.unescape(byline).replace("\xa0", " ").strip()
    parts = [p.strip() for p in re.split(r"\s+[-–—]\s+", byline)]
    authors_part = parts[0] if parts else ""
    venue_part = parts[1] if len(parts) > 1 else ""
    authors = [a.strip(" …") for a in authors_part.split(",") if a.strip(" …")]
    # Scholar truncates long author lists with "…"
    year = None
    m = _YEAR_RE.search(venue_part) or _YEAR_RE.search(byline)
    if m:
        year = int(m.group(0))
    venue = re.sub(r",?\s*(19|20)\d{2}\s*$", "", venue_part).strip(" ,")
    # citation/author alerts sometimes put year in authors_part only
    if not venue and len(parts) == 1 and year:
        authors = [a for a in authors if not _YEAR_RE.fullmatch(a)]
    return authors, venue, year


def parse_alert_html(html: str) -> list[ParsedHit]:
    soup = BeautifulSoup(html, "lxml")
    hits: list[ParsedHit] = []
    for a in soup.select("a.gse_alrt_title, h3 a"):
        try:
            title = " ".join(a.get_text(" ", strip=True).split())
            if not title:
                continue
            url = unwrap_scholar_url(a.get("href", ""))
            h3 = a.find_parent("h3") or a
            byline_el = h3.find_next_sibling("div")
            byline = byline_el.get_text(" ", strip=True) if byline_el else ""
            sni_el = None
            if byline_el:
                nxt = byline_el.find_next_sibling("div")
                if nxt and ("gse_alrt_sni" in (nxt.get("class") or []) or not nxt.find("a")):
                    sni_el = nxt
            snippet = " ".join(sni_el.get_text(" ", strip=True).split()) if sni_el else ""
            authors, venue, year = _split_byline(byline)
            hits.append(ParsedHit(title=title, url=url, authors=authors, venue=venue, year=year, snippet=snippet))
        except Exception:
            continue
    # de-dup by title within one mail
    seen: set[str] = set()
    out = []
    for h in hits:
        k = h.title.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(h)
    return out


def parse_alert_text(text: str) -> list[ParsedHit]:
    """Fallback for text/plain bodies: blocks of 'Title\\nAuthors - Venue, Year\\nsnippet…\\n<url>'."""
    hits: list[ParsedHit] = []
    blocks = re.split(r"\n\s*\n", text.replace("\r", ""))
    for b in blocks:
        lines = [l.strip() for l in b.strip().splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        url = next((unwrap_scholar_url(l) for l in lines if l.startswith("http")), "")
        body = [l for l in lines if not l.startswith("http")]
        if len(body) < 2 or " - " not in body[1] and "–" not in body[1]:
            continue
        title = body[0]
        authors, venue, year = _split_byline(body[1])
        snippet = " ".join(body[2:])
        if title.lower().startswith(("this message was sent", "list alerts", "cancel alert", "이 메시지는")):
            continue
        hits.append(ParsedHit(title=title, url=url, authors=authors, venue=venue, year=year, snippet=snippet))
    return hits


def parse_alert(subject: str, html: str | None, text: str | None, message_id: str | None) -> tuple[str, list[Paper]]:
    keyword = keyword_from_subject(subject)
    hits = parse_alert_html(html) if html else []
    if not hits and text:
        hits = parse_alert_text(text)
    return keyword, [h.to_paper(keyword, message_id) for h in hits]
