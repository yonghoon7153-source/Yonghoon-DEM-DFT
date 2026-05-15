#!/usr/bin/env python
"""literature_harvest.py — Auto-fetch papers via OpenAlex + Semantic Scholar.

Builds a personal literature "Bible" DB by searching priority keywords and
saving deduplicated paper metadata to kb/literature_db/raw.json.

Usage:
  python3 literature_harvest.py                   # default keywords
  python3 literature_harvest.py --keywords file.json
  python3 literature_harvest.py --max 100         # papers per keyword
"""
import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

# Default keyword list (project-specific, see kb/platforms/literature_db_tools.md)
DEFAULT_KEYWORDS = [
    # Argyrodite / Sulfide SE
    "argyrodite Li6PS5Cl halogen substitution",
    "Li5.4PS4.4 Cl Br halide-rich argyrodite",
    "sulfide solid electrolyte ionic conductivity",
    "anion site disorder 4a 4d argyrodite",
    "lithium argyrodite halide segregation",
    # Interface / Adhesion
    "all-solid-state battery cathode interface stability",
    "sulfide NCM interface adhesion energy",
    "LiNbO3 LiCoO2 NCM coating buffer layer",
    "Li2S Li6PS5Cl surface termination DFT",
    "halide segregation cathode interface battery",
    # MLIP / Computational
    "MLIP universal materials atomistic UMA FAIRChem",
    "MACE NequIP machine learning interatomic potential",
    "DFT high-throughput screening battery materials atomate2",
    # ML / Screening
    "active learning materials discovery solid electrolyte",
    "Bayesian optimization cathode coating screening",
    "inverse design generative model battery materials",
    # Doping / Substitution
    "LPSCl cation doping Mg Al Na",
    "argyrodite anion substitution O F I",
    # Mechanism
    "Madelung potential solid electrolyte interface",
    "Pauli repulsion anion oxide interface battery",
]


def harvest_openalex(keywords: list[str], max_per: int = 30) -> dict[str, dict]:
    """Fetch via OpenAlex (no API key needed for now, free until 2026-02)."""
    try:
        from pyalex import Works, config
        # config.email = os.environ.get('OPENALEX_EMAIL')  # polite pool
    except ImportError:
        print("Install pyalex: pip install pyalex")
        return {}

    db = {}
    print(f"--- OpenAlex harvest ({len(keywords)} keywords, {max_per}/keyword) ---")
    for kw in keywords:
        try:
            works = Works().search(kw).get(per_page=max_per)
            for w in works:
                pid = w.get("id")
                if pid is None:
                    continue
                # Skip if already in DB (dedup on OpenAlex ID)
                if pid in db:
                    db[pid].setdefault('keywords', []).append(kw)
                    continue
                # Extract abstract from inverted_index
                abs_inv = w.get("abstract_inverted_index")
                abstract = _abstract_from_inverted(abs_inv) if abs_inv else None
                db[pid] = {
                    'source': 'openalex',
                    'id': pid,
                    'doi': w.get("doi"),
                    'title': w.get("title"),
                    'abstract': abstract,
                    'year': w.get("publication_year"),
                    'venue': (w.get("primary_location") or {}).get("source", {}).get("display_name") if w.get("primary_location") else None,
                    'authors': [a["author"]["display_name"]
                               for a in w.get("authorships", [])][:8],
                    'cited_by_count': w.get("cited_by_count"),
                    'keywords': [kw],
                }
            print(f"  '{kw[:60]}' → +{len(works)} papers (total {len(db)})")
            time.sleep(0.1)  # be polite
        except Exception as e:
            print(f"  '{kw[:60]}' → ERROR: {e}")
    return db


def _abstract_from_inverted(inv: dict[str, list[int]]) -> str:
    """Reconstruct abstract text from OpenAlex inverted index."""
    if not inv:
        return ""
    max_pos = max(max(positions) for positions in inv.values())
    words = [""] * (max_pos + 1)
    for word, positions in inv.items():
        for p in positions:
            words[p] = word
    return " ".join(words)


def harvest_semantic_scholar(keywords: list[str], max_per: int = 20) -> dict[str, dict]:
    """Fetch via Semantic Scholar (better TLDR summaries)."""
    try:
        from semanticscholar import SemanticScholar
    except ImportError:
        print("Install semanticscholar: pip install semanticscholar")
        return {}

    sch = SemanticScholar(timeout=30)
    db = {}
    print(f"\n--- Semantic Scholar harvest ({len(keywords)} keywords, {max_per}/keyword) ---")
    for kw in keywords:
        try:
            papers = sch.search_paper(kw, limit=max_per)
            for p in papers:
                pid = f"S2:{p.paperId}" if p.paperId else None
                if pid is None:
                    continue
                if pid in db:
                    db[pid].setdefault('keywords', []).append(kw)
                    continue
                tldr = getattr(p, 'tldr', None)
                tldr_text = tldr.get('text') if isinstance(tldr, dict) else (
                    tldr.text if hasattr(tldr, 'text') else None)
                db[pid] = {
                    'source': 'semantic_scholar',
                    'id': pid,
                    'doi': getattr(p, 'externalIds', {}).get('DOI') if hasattr(p, 'externalIds') else None,
                    'title': p.title,
                    'abstract': p.abstract,
                    'tldr': tldr_text,
                    'year': p.year,
                    'venue': p.venue,
                    'authors': [a.name for a in (p.authors or [])][:8],
                    'cited_by_count': p.citationCount,
                    'keywords': [kw],
                }
            print(f"  '{kw[:60]}' → +{len(papers)} papers (total {len(db)})")
            time.sleep(3.0)  # S2 rate limit: 100/5min => 1/3s
        except Exception as e:
            print(f"  '{kw[:60]}' → ERROR: {e}")
    return db


def merge_dbs(*dbs: dict[str, dict]) -> dict[str, dict]:
    """Merge OpenAlex + S2 DBs, dedup by DOI when possible."""
    merged = {}
    doi_to_id = {}
    for db in dbs:
        for pid, paper in db.items():
            doi = paper.get('doi')
            if doi and doi in doi_to_id:
                # Merge with existing
                existing_id = doi_to_id[doi]
                ex = merged[existing_id]
                # Prefer tldr from S2
                if paper.get('tldr') and not ex.get('tldr'):
                    ex['tldr'] = paper['tldr']
                ex.setdefault('keywords', []).extend(paper.get('keywords', []))
                ex['keywords'] = list(set(ex['keywords']))
            else:
                merged[pid] = paper
                if doi:
                    doi_to_id[doi] = pid
    return merged


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--keywords', help='JSON file with list of keywords')
    parser.add_argument('--max', type=int, default=30, help='Max papers per keyword (OpenAlex)')
    parser.add_argument('--max-s2', type=int, default=20, help='Max papers per keyword (Semantic Scholar)')
    parser.add_argument('--out', default='kb/literature_db/raw.json', help='Output JSON path')
    parser.add_argument('--no-s2', action='store_true', help='Skip Semantic Scholar (rate limited)')
    parser.add_argument('--update', action='store_true', help='Merge with existing DB')
    args = parser.parse_args()

    if args.keywords:
        keywords = json.loads(Path(args.keywords).read_text())
    else:
        keywords = DEFAULT_KEYWORDS
    print(f"Harvesting {len(keywords)} keywords...")

    db_oa = harvest_openalex(keywords, max_per=args.max)
    db_s2 = {} if args.no_s2 else harvest_semantic_scholar(keywords, max_per=args.max_s2)
    merged = merge_dbs(db_oa, db_s2)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if args.update and out_path.exists():
        existing = json.loads(out_path.read_text())
        merged = merge_dbs(existing, merged)

    out_path.write_text(json.dumps(merged, indent=2, default=str))
    print(f"\n✓ Saved {len(merged)} unique papers to {out_path}")
    print(f"  OpenAlex: {len(db_oa)}, Semantic Scholar: {len(db_s2)}")


if __name__ == '__main__':
    main()
