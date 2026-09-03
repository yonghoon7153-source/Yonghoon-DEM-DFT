"""Manual / bootstrap ingestion.

Drop JSON files into data/inbox/manual/ (one paper per file, or a list) with keys:
  title, authors[], venue, year, doi, url, abstract, snippet, keyword | keywords[], source
Also used by `ra ingest --json` and by the bootstrap seed. Processed files are moved to .../done/.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from ..models import Paper, paper_id_from


def paper_from_record(rec: dict, default_source: str = "manual") -> Paper:
    kws = rec.get("keywords") or ([rec["keyword"]] if rec.get("keyword") else [])
    doi = (rec.get("doi") or None)
    if doi:
        doi = doi.strip().removeprefix("https://doi.org/").removeprefix("doi:")
    p = Paper(
        id=paper_id_from(rec["title"], doi),
        title=rec["title"].strip(),
        authors=[a.strip() for a in rec.get("authors", []) if a and a.strip()],
        venue=rec.get("venue", "") or "",
        year=rec.get("year"),
        doi=doi,
        url=rec.get("url", "") or (f"https://doi.org/{doi}" if doi else ""),
        snippet=rec.get("snippet", "") or "",
        abstract=rec.get("abstract", "") or "",
        keywords_matched=[k.lower() for k in kws],
        source=rec.get("source", default_source),
    )
    if rec.get("first_seen"):
        p.first_seen = rec["first_seen"]
    if rec.get("extra"):
        p.extra = dict(rec["extra"])
    return p


def load_manual_dir(folder: Path, move_done: bool = True) -> list[Paper]:
    folder = Path(folder)
    if not folder.exists():
        return []
    done = folder / "done"
    papers: list[Paper] = []
    for f in sorted(folder.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        recs = data if isinstance(data, list) else [data]
        for rec in recs:
            if isinstance(rec, dict) and rec.get("title"):
                papers.append(paper_from_record(rec))
        if move_done:
            done.mkdir(exist_ok=True)
            shutil.move(str(f), str(done / f.name))
    return papers
