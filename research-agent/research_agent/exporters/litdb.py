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


def export(cfg: Config, papers: list[Paper]) -> dict:
    if not cfg.get("litdb.enabled", False):
        return {"mode": "disabled"}
    mode = cfg.get("litdb.mode", "file")
    out = export_cli(cfg, papers) if mode == "cli" else export_file(cfg, papers)
    if cfg.get("litdb.also_file", False) and mode == "cli":
        out["file"] = export_file(cfg, papers)
    return out
