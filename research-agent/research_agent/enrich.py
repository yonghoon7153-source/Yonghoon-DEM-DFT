"""Metadata enrichment via public scholarly APIs (Crossref → OpenAlex → Semantic Scholar).

Runs on the user's machine (these hosts are not reachable from the Cowork sandbox).
Every provider is optional; failures degrade silently so the pipeline never blocks on the network.
"""
from __future__ import annotations

import re
import time
from typing import Any

import requests

from .models import Paper

_UA = "research-agent/0.1 (mailto:{mailto})"


def _get(url: str, params: dict | None, timeout: int, mailto: str) -> dict | None:
    try:
        r = requests.get(url, params=params, timeout=timeout, headers={"User-Agent": _UA.format(mailto=mailto)})
        if r.status_code == 429:
            time.sleep(2.0)
            r = requests.get(url, params=params, timeout=timeout, headers={"User-Agent": _UA.format(mailto=mailto)})
        if r.ok:
            return r.json()
    except Exception:
        return None
    return None


def _strip_jats(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s or "").replace("\n", " ").strip()


# ----------------------------------------------------------------------------- Crossref
def crossref(p: Paper, timeout: int, mailto: str) -> dict[str, Any]:
    if p.doi:
        j = _get(f"https://api.crossref.org/works/{p.doi}", {"mailto": mailto}, timeout, mailto)
        item = (j or {}).get("message")
    else:
        j = _get("https://api.crossref.org/works",
                 {"query.bibliographic": p.title, "rows": 3, "mailto": mailto,
                  "select": "DOI,title,author,container-title,issued,abstract,URL,type"}, timeout, mailto)
        items = ((j or {}).get("message") or {}).get("items") or []
        item = next((it for it in items if _title_match(p.title, (it.get("title") or [""])[0])), None)
    if not item:
        return {}
    out: dict[str, Any] = {"doi": item.get("DOI")}
    if item.get("container-title"):
        out["venue"] = item["container-title"][0]
    if item.get("author"):
        out["authors"] = [f"{a.get('given','')} {a.get('family','')}".strip() for a in item["author"]]
    if item.get("abstract"):
        out["abstract"] = _strip_jats(item["abstract"])
    dp = ((item.get("issued") or {}).get("date-parts") or [[None]])[0]
    if dp and dp[0]:
        out["year"] = int(dp[0])
    if item.get("URL"):
        out["url"] = item["URL"]
    return {k: v for k, v in out.items() if v}


# ----------------------------------------------------------------------------- OpenAlex
def _inv_to_text(inv: dict | None) -> str:
    if not inv:
        return ""
    pos: list[tuple[int, str]] = []
    for w, idxs in inv.items():
        pos += [(i, w) for i in idxs]
    return " ".join(w for _, w in sorted(pos))


def openalex(p: Paper, timeout: int, mailto: str) -> dict[str, Any]:
    if p.doi:
        j = _get(f"https://api.openalex.org/works/doi:{p.doi}", {"mailto": mailto}, timeout, mailto)
        item = j
    else:
        j = _get("https://api.openalex.org/works", {"search": p.title, "per-page": 3, "mailto": mailto}, timeout, mailto)
        items = (j or {}).get("results") or []
        item = next((it for it in items if _title_match(p.title, it.get("title") or "")), None)
    if not item:
        return {}
    out: dict[str, Any] = {}
    if item.get("doi"):
        out["doi"] = item["doi"].removeprefix("https://doi.org/")
    src = ((item.get("primary_location") or {}).get("source") or {})
    if src.get("display_name"):
        out["venue"] = src["display_name"]
    if item.get("publication_year"):
        out["year"] = int(item["publication_year"])
    if item.get("authorships"):
        out["authors"] = [a.get("author", {}).get("display_name", "") for a in item["authorships"] if a.get("author")]
    ab = _inv_to_text(item.get("abstract_inverted_index"))
    if ab:
        out["abstract"] = ab
    out["extra"] = {"openalex_id": item.get("id"), "cited_by_count": item.get("cited_by_count"),
                    "is_oa": (item.get("open_access") or {}).get("is_oa"),
                    "oa_url": (item.get("open_access") or {}).get("oa_url")}
    return {k: v for k, v in out.items() if v}


# ------------------------------------------------------------------------ Semantic Scholar
def semanticscholar(p: Paper, timeout: int, mailto: str) -> dict[str, Any]:
    fields = "title,abstract,venue,year,externalIds,citationCount,tldr,authors"
    if p.doi:
        j = _get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{p.doi}", {"fields": fields}, timeout, mailto)
        item = j
    else:
        j = _get("https://api.semanticscholar.org/graph/v1/paper/search",
                 {"query": p.title, "limit": 3, "fields": fields}, timeout, mailto)
        items = (j or {}).get("data") or []
        item = next((it for it in items if _title_match(p.title, it.get("title") or "")), None)
    if not item:
        return {}
    out: dict[str, Any] = {}
    if item.get("abstract"):
        out["abstract"] = item["abstract"]
    if item.get("venue"):
        out["venue"] = item["venue"]
    if item.get("year"):
        out["year"] = int(item["year"])
    ext = item.get("externalIds") or {}
    if ext.get("DOI"):
        out["doi"] = ext["DOI"]
    if item.get("authors"):
        out["authors"] = [a.get("name", "") for a in item["authors"]]
    extra = {"s2_citations": item.get("citationCount")}
    if item.get("tldr") and item["tldr"].get("text"):
        extra["tldr"] = item["tldr"]["text"]
    out["extra"] = extra
    return {k: v for k, v in out.items() if v}


# ------------------------------------------------------------------------------ driver
def _title_match(a: str, b: str) -> bool:
    from .models import normalize_title
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    return len(shorter) > 25 and shorter in longer


PROVIDERS = {"crossref": crossref, "openalex": openalex, "semanticscholar": semanticscholar}


def enrich_paper(p: Paper, providers: list[str], timeout: int = 15, mailto: str = "") -> Paper:
    """Fill blanks (doi, venue, year, authors, abstract) without overwriting existing non-empty fields,
    except `venue` which is upgraded to the canonical container-title when available."""
    for name in providers:
        fn = PROVIDERS.get(name)
        if not fn:
            continue
        data = fn(p, timeout, mailto)
        if not data:
            continue
        for k, v in data.items():
            if k == "extra":
                p.extra.update({kk: vv for kk, vv in v.items() if vv is not None})
            elif k == "venue" and v and len(v) > len(p.venue or ""):
                p.venue = v
            elif not getattr(p, k, None):
                setattr(p, k, v)
        if p.doi and p.abstract and p.venue:
            break
        time.sleep(0.3)
    if p.doi and not p.url:
        p.url = f"https://doi.org/{p.doi}"
    return p
