"""Core data models. Kept dependency-free so Hermes/Claude Code can import them cheaply."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_title(title: str) -> str:
    t = unicodedata.normalize("NFKC", title or "").lower()
    t = re.sub(r"[^a-z0-9가-힣 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def paper_id_from(title: str, doi: str | None = None) -> str:
    """Stable id: DOI if present, else sha1 of normalized title."""
    if doi:
        return "doi:" + doi.lower().strip().removeprefix("https://doi.org/")
    return "t:" + hashlib.sha1(normalize_title(title).encode()).hexdigest()[:16]


def slugify(text: str, max_len: int = 80) -> str:
    t = unicodedata.normalize("NFKC", text)
    t = re.sub(r"[\\/:*?\"<>|#^\[\]]+", " ", t)  # Obsidian-illegal chars
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > max_len:
        cut = t[:max_len]
        t = cut[: cut.rfind(" ")] if " " in cut[max_len // 2:] else cut
    return t.rstrip(" .-,:;")


STATUS_ORDER = ["new", "triaged", "analyzed", "digested", "rejected", "known"]


@dataclass
class Paper:
    id: str
    title: str
    authors: list[str] = field(default_factory=list)
    venue: str = ""                 # journal / conference / preprint server as printed in the alert
    year: int | None = None
    doi: str | None = None
    url: str = ""
    snippet: str = ""               # Scholar alert snippet
    abstract: str = ""              # enriched abstract (Crossref/OpenAlex/S2) or manual
    keywords_matched: list[str] = field(default_factory=list)
    source: str = "scholar_email"   # scholar_email | manual | bootstrap
    alert_message_id: str | None = None
    first_seen: str = field(default_factory=now_iso)
    # --- triage ---
    journal_canonical: str = ""
    journal_if: float | None = None
    is_preprint: bool = False
    relevance: float | None = None
    relevance_reason: str = ""
    tier: str = ""                  # A | B | C | "" (rejected)
    priority: float | None = None   # sort key (IF-major, relevance-minor)
    status: str = "new"
    # --- analysis ---
    analysis: dict[str, Any] = field(default_factory=dict)
    analyzed_at: str | None = None
    note_path: str | None = None
    digested_at: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------------------------
    @property
    def first_author(self) -> str:
        if not self.authors:
            return "Unknown"
        a = self.authors[0].strip()
        # "Kissel M" / "M Kissel" / "Maximilian Kissel" → family name heuristic
        parts = a.replace(",", " ").split()
        if not parts:
            return "Unknown"
        if len(parts) >= 2 and len(parts[0]) <= 2 and parts[0].isupper():  # "M Kissel" (Scholar style)
            return parts[-1]
        return parts[-1] if len(parts) >= 2 and len(parts[-1]) > 2 else parts[0]

    @property
    def short_title(self) -> str:
        return slugify(self.title, 60)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Paper":
        known = {f for f in cls.__dataclass_fields__}
        clean = {k: v for k, v in d.items() if k in known}
        for k in ("authors", "keywords_matched"):
            if isinstance(clean.get(k), str):
                clean[k] = json.loads(clean[k]) if clean[k].startswith("[") else [clean[k]]
        for k in ("analysis", "extra"):
            if isinstance(clean.get(k), str):
                clean[k] = json.loads(clean[k]) if clean[k] else {}
        return cls(**clean)


@dataclass
class Alert:
    message_id: str
    keyword: str
    received_at: str
    subject: str
    n_items: int
    raw_path: str | None = None
    processed_at: str | None = None


@dataclass
class RunRecord:
    job: str
    started_at: str
    finished_at: str | None = None
    status: str = "running"
    summary: dict[str, Any] = field(default_factory=dict)
