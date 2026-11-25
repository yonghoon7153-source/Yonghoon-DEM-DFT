"""Journal name → canonical name + impact factor lookup."""
from __future__ import annotations

import re
from dataclasses import dataclass


def _norm(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\b(the|of|and|in|for|on)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


@dataclass
class JournalMatch:
    canonical: str
    impact_factor: float
    is_preprint: bool
    matched_by: str  # exact | alias | partial | preprint | default


class JournalTable:
    def __init__(self, table: dict):
        self.default_if = float(table.get("default_if", 3.0))
        self.preprints = [p.lower() for p in table.get("preprint_servers", [])]
        self.exact: dict[str, tuple[str, float]] = {}
        self.aliases: dict[str, tuple[str, float]] = {}
        for j in table.get("journals", []):
            name, if_ = j["name"], float(j["if"])
            self.exact[_norm(name)] = (name, if_)
            for a in j.get("aliases", []) or []:
                self.aliases[_norm(a)] = (name, if_)

    def lookup(self, venue: str) -> JournalMatch:
        v = _norm(venue)
        if not v:
            return JournalMatch("", self.default_if, False, "default")
        for p in self.preprints:
            if p in v:
                return JournalMatch(venue.strip(), 0.0, True, "preprint")
        if v in self.exact:
            n, f = self.exact[v]
            return JournalMatch(n, f, False, "exact")
        if v in self.aliases:
            n, f = self.aliases[v]
            return JournalMatch(n, f, False, "alias")
        # partial: Scholar often truncates ("… Energy Storage Materials, 2026" or "Adv. Energy …")
        best: tuple[int, str, float] | None = None
        for key, (n, f) in list(self.exact.items()) + list(self.aliases.items()):
            if len(key) >= 6 and (key in v or v in key):
                score = len(key)
                if best is None or score > best[0]:
                    best = (score, n, f)
        if best:
            return JournalMatch(best[1], best[2], False, "partial")
        return JournalMatch(venue.strip(), self.default_if, False, "default")
