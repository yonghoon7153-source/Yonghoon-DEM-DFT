"""SQLite store + JSONL mirror.

Design goals
- Single-file SQLite (data/papers.sqlite) is the source of truth.
- data/papers.jsonl is regenerated after every write batch so git diffs stay readable
  and other tools (litdb, Obsidian Dataview, pandas) can consume it without sqlite.
- Schema migrations are additive; `schema_version` lives in the meta table.
"""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

from .models import Alert, Paper, RunRecord, now_iso

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE IF NOT EXISTS papers (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  title_norm TEXT NOT NULL,
  authors TEXT NOT NULL DEFAULT '[]',
  venue TEXT DEFAULT '',
  year INTEGER,
  doi TEXT,
  url TEXT DEFAULT '',
  snippet TEXT DEFAULT '',
  abstract TEXT DEFAULT '',
  keywords_matched TEXT NOT NULL DEFAULT '[]',
  source TEXT DEFAULT 'scholar_email',
  alert_message_id TEXT,
  first_seen TEXT NOT NULL,
  journal_canonical TEXT DEFAULT '',
  journal_if REAL,
  is_preprint INTEGER DEFAULT 0,
  relevance REAL,
  relevance_reason TEXT DEFAULT '',
  tier TEXT DEFAULT '',
  priority REAL,
  status TEXT NOT NULL DEFAULT 'new',
  analysis TEXT DEFAULT '{}',
  analyzed_at TEXT,
  note_path TEXT,
  digested_at TEXT,
  extra TEXT DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_papers_status ON papers(status);
CREATE INDEX IF NOT EXISTS idx_papers_title_norm ON papers(title_norm);
CREATE INDEX IF NOT EXISTS idx_papers_priority ON papers(priority);

CREATE TABLE IF NOT EXISTS alerts (
  message_id TEXT PRIMARY KEY,
  keyword TEXT,
  received_at TEXT,
  subject TEXT,
  n_items INTEGER,
  raw_path TEXT,
  processed_at TEXT
);

CREATE TABLE IF NOT EXISTS digests (
  date TEXT PRIMARY KEY,
  path TEXT,
  n_papers INTEGER,
  paper_ids TEXT DEFAULT '[]',
  sent_at TEXT,
  mail_message_id TEXT
);

CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job TEXT NOT NULL,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  status TEXT,
  summary TEXT DEFAULT '{}'
);
"""


class PaperDB:
    def __init__(self, sqlite_path: Path, jsonl_path: Path | None = None):
        self.sqlite_path = Path(sqlite_path)
        self.jsonl_path = Path(jsonl_path) if jsonl_path else None
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.sqlite_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA)
        self.conn.execute(
            "INSERT OR IGNORE INTO meta(key, value) VALUES ('schema_version', ?)", (str(SCHEMA_VERSION),)
        )
        self.conn.commit()

    # ------------------------------------------------------------------ utils
    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        try:
            yield self.conn
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def close(self) -> None:
        self.conn.close()

    # ----------------------------------------------------------------- papers
    @staticmethod
    def _row_to_paper(row: sqlite3.Row) -> Paper:
        d = dict(row)
        d.pop("title_norm", None)
        d["is_preprint"] = bool(d.get("is_preprint"))
        return Paper.from_dict(d)

    def get(self, paper_id: str) -> Paper | None:
        row = self.conn.execute("SELECT * FROM papers WHERE id=?", (paper_id,)).fetchone()
        return self._row_to_paper(row) if row else None

    def find_by_title(self, title: str) -> Paper | None:
        from .models import normalize_title
        row = self.conn.execute("SELECT * FROM papers WHERE title_norm=?", (normalize_title(title),)).fetchone()
        return self._row_to_paper(row) if row else None

    def find_by_doi(self, doi: str) -> Paper | None:
        row = self.conn.execute("SELECT * FROM papers WHERE lower(doi)=lower(?)", (doi,)).fetchone()
        return self._row_to_paper(row) if row else None

    def upsert(self, p: Paper) -> tuple[Paper, bool]:
        """Insert or merge. Returns (stored_paper, is_new).

        Merge rule: an existing record keeps its triage/analysis fields; new alert data only
        fills blanks and unions keywords_matched. This makes re-ingestion idempotent.
        """
        from .models import normalize_title
        existing = self.get(p.id) or (self.find_by_doi(p.doi) if p.doi else None) or self.find_by_title(p.title)
        if existing:
            merged = existing
            for f in ("venue", "doi", "url", "snippet", "abstract", "alert_message_id"):
                if not getattr(merged, f) and getattr(p, f):
                    setattr(merged, f, getattr(p, f))
            if not merged.year and p.year:
                merged.year = p.year
            if len(p.authors) > len(merged.authors):
                merged.authors = p.authors
            merged.keywords_matched = sorted(set(merged.keywords_matched) | set(p.keywords_matched))
            self._write(merged, normalize_title(merged.title))
            return merged, False
        self._write(p, normalize_title(p.title))
        return p, True

    def save(self, p: Paper) -> None:
        from .models import normalize_title
        self._write(p, normalize_title(p.title))

    def _write(self, p: Paper, title_norm: str) -> None:
        d = p.to_dict()
        d["title_norm"] = title_norm
        for k in ("authors", "keywords_matched", "analysis", "extra"):
            d[k] = json.dumps(d[k], ensure_ascii=False)
        d["is_preprint"] = int(bool(d["is_preprint"]))
        cols = ", ".join(d.keys())
        marks = ", ".join("?" for _ in d)
        updates = ", ".join(f"{k}=excluded.{k}" for k in d if k != "id")
        with self.tx() as c:
            c.execute(
                f"INSERT INTO papers ({cols}) VALUES ({marks}) ON CONFLICT(id) DO UPDATE SET {updates}",
                list(d.values()),
            )

    def list(self, status: str | Iterable[str] | None = None, order: str = "priority DESC, first_seen DESC",
             limit: int | None = None) -> list[Paper]:
        q = "SELECT * FROM papers"
        args: list = []
        if status:
            statuses = [status] if isinstance(status, str) else list(status)
            q += " WHERE status IN (%s)" % ",".join("?" for _ in statuses)
            args += statuses
        q += f" ORDER BY {order}"
        if limit:
            q += f" LIMIT {int(limit)}"
        return [self._row_to_paper(r) for r in self.conn.execute(q, args).fetchall()]

    def since(self, iso_ts: str, field: str = "analyzed_at") -> list[Paper]:
        assert field in {"analyzed_at", "first_seen", "digested_at"}
        rows = self.conn.execute(
            f"SELECT * FROM papers WHERE {field} IS NOT NULL AND {field} >= ? ORDER BY priority DESC", (iso_ts,)
        ).fetchall()
        return [self._row_to_paper(r) for r in rows]

    def counts(self) -> dict[str, int]:
        rows = self.conn.execute("SELECT status, COUNT(*) n FROM papers GROUP BY status").fetchall()
        out = {r["status"]: r["n"] for r in rows}
        out["total"] = sum(out.values())
        return out

    # ----------------------------------------------------------------- alerts
    def alert_seen(self, message_id: str) -> bool:
        return self.conn.execute("SELECT 1 FROM alerts WHERE message_id=?", (message_id,)).fetchone() is not None

    def record_alert(self, a: Alert) -> None:
        with self.tx() as c:
            c.execute(
                "INSERT OR REPLACE INTO alerts(message_id, keyword, received_at, subject, n_items, raw_path, processed_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (a.message_id, a.keyword, a.received_at, a.subject, a.n_items, a.raw_path, a.processed_at or now_iso()),
            )

    # ---------------------------------------------------------------- digests
    def record_digest(self, date: str, path: str, paper_ids: list[str], sent_at: str | None = None,
                      mail_message_id: str | None = None) -> None:
        with self.tx() as c:
            c.execute(
                "INSERT OR REPLACE INTO digests(date, path, n_papers, paper_ids, sent_at, mail_message_id)"
                " VALUES (?,?,?,?,?,?)",
                (date, path, len(paper_ids), json.dumps(paper_ids), sent_at, mail_message_id),
            )

    def last_digest(self) -> dict | None:
        row = self.conn.execute("SELECT * FROM digests ORDER BY date DESC LIMIT 1").fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------- runs
    def start_run(self, job: str) -> int:
        with self.tx() as c:
            cur = c.execute("INSERT INTO runs(job, started_at, status) VALUES (?,?, 'running')", (job, now_iso()))
            return int(cur.lastrowid)

    def finish_run(self, run_id: int, status: str, summary: dict) -> None:
        with self.tx() as c:
            c.execute(
                "UPDATE runs SET finished_at=?, status=?, summary=? WHERE id=?",
                (now_iso(), status, json.dumps(summary, ensure_ascii=False), run_id),
            )

    def recent_runs(self, n: int = 10) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (n,)).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------ jsonl mirror
    def export_jsonl(self) -> Path | None:
        if not self.jsonl_path:
            return None
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        papers = self.list(order="first_seen ASC, id ASC")
        with open(self.jsonl_path, "w", encoding="utf-8") as f:
            for p in papers:
                f.write(json.dumps(p.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
        return self.jsonl_path
