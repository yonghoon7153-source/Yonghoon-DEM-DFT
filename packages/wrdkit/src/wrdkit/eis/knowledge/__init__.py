"""What the impedance papers say, record by record (ADR 0042).

The audit's judgements rest on a handful of papers -- which capacitance is
which process, which resistance goes into an effective capacitance, how a
Kramers–Kronig test picks its size.  A rule that cites nothing gets argued
with; a rule that cites "Irvine–Sinclair–West 1990, p. 135, Fig. 4b" gets
checked.  So the papers live here as data, one JSON file per paper:

* every record is **our paraphrase** with the printed page and where on it --
  ``claim_ko`` for the lab, ``claim`` in English;
* ``math``, ``values`` and ``conditions`` carry the formula, the numbers and
  when they hold;
* a verbatim ``quote`` (25 words at most) is kept **only** for the records the
  code cites, to find the passage again.  The repository is public and the
  papers are not ours; everything else is in our own words.

Record ids are stable (``SOURCE.slug``).  `audit.REFERENCES` maps each finding
code to the records it rests on, and a test keeps every id resolvable.

Nothing here imports numpy -- it is reading, not arithmetic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cache
from importlib import resources

__all__ = ["Record", "Source", "cite", "record", "records", "search", "sources"]

_FILES = ("isw1990.json", "hirschorn2010.json", "schoenleber2014.json",
          "vadhva2021.json", "lasia1999.json", "ecsif2019.json")


@dataclass(frozen=True)
class Source:
    key: str
    #: 사람이 읽는 짧은 이름 — "Irvine–Sinclair–West 1990".
    short: str
    authors: str
    title: str
    venue: str
    year: int
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""


@dataclass(frozen=True)
class Record:
    id: str
    source: str
    #: definition / formula / criterion / range / model / procedure / caveat / example
    kind: str
    topics: tuple[str, ...]
    claim_ko: str
    claim: str
    #: The **printed** page (what a citation gives), not the PDF page.
    page: int | str
    where: str = ""
    math: str = ""
    values: object = None
    conditions: str = ""
    confidence: str = ""
    quote: str = ""


@cache
def _load() -> tuple[dict[str, Source], dict[str, Record]]:
    found_sources: dict[str, Source] = {}
    found: dict[str, Record] = {}
    base = resources.files(__name__)
    for name in _FILES:
        payload = json.loads(base.joinpath(name).read_text(encoding="utf-8"))
        for item in payload["sources"]:
            found_sources[item["key"]] = Source(**item)
        for item in payload["records"]:
            item = dict(item)
            item["topics"] = tuple(item.get("topics") or ())
            if item["id"] in found:
                raise ValueError(f"duplicate knowledge record {item['id']!r}")
            found[item["id"]] = Record(**item)
    return found_sources, found


def sources() -> dict[str, Source]:
    """Every paper, by key."""
    return dict(_load()[0])


def records() -> dict[str, Record]:
    """Every record, by id, in file order."""
    return dict(_load()[1])


def record(record_id: str) -> Record:
    """One record.  Raises ``KeyError`` for an id that is not in the files."""
    return _load()[1][record_id]


def cite(record_id: str) -> str:
    """``"Irvine–Sinclair–West 1990, p. 135 (Sect. 2.2; Fig. 4b,c)"``."""
    one = record(record_id)
    source = _load()[0][one.source]
    where = f" ({one.where})" if one.where else ""
    return f"{source.short}, p. {one.page}{where}"


def search(*, topic: str | None = None, text: str | None = None,
           source: str | None = None) -> list[Record]:
    """Records with the topic, the source key, and the text (in either
    language, any case) -- every given condition must hold."""
    needle = text.lower() if text else None
    out = []
    for one in _load()[1].values():
        if topic is not None and topic not in one.topics:
            continue
        if source is not None and one.source != source:
            continue
        if needle is not None and needle not in (one.claim_ko + " " + one.claim).lower():
            continue
        out.append(one)
    return out
