"""Triage: relevance scoring (rule-based, optionally LLM-refined) + IF lookup → tier & priority.

Ordering rule requested by the owner: **IF-first** among papers that pass the relevance gate.
    priority = journal_if * 1000 + relevance * 100 + keyword_bonus
so sorting by priority DESC yields IF-major / relevance-minor ordering while preprints (IF 0)
still sort by relevance among themselves.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .journals import JournalTable
from .models import Paper

# (pattern, weight) — mirrors config/research_profile.md "채점용 용어 가중치"
#   core   : 추적 키워드 3축의 핵심 방법론 용어 (하나만 있어도 '내 분야'로 인정)
#   system : 내 재료계 (황화물 ASSB / composite cathode)
#   property/method : 비교 가능한 물성·공정·계면 용어
#   general: 배터리 일반 (약한 신호)
#   negative: 다른 분야
_TERMS: list[tuple[str, float]] = [
    (r"discrete[- ]element|\bDEM\b|LIGGGHTS|resistor[- ]network|percolat"
     r"|first[- ]principles|\bDFT\b|density functional|ab initio|machine[- ]learning (interatomic )?potential|\bMLIP\b|\bAIMD\b|universal (interatomic )?potential"
     r"|anode[- ]free|anode[- ]less|zero[- ]excess", 0.35),
    (r"all[- ]solid[- ]state|solid[- ]state|sulfide|Li6PS5Cl|Li₆PS₅Cl|LPSCl|argyrodite|thiophosphate|halide (solid )?electrolyte"
     r"|solid electrolyte(?!\s+interphase)|composite (positive electrode|cathode)", 0.25),
    (r"elastic|modulus|adhesion|interfac|\bNCM\b|\bNMC\b|porosity|calender|compaction|contact|tortuosity|percolation"
     r"|lithium metal|Li metal|current collector|interlayer|coating|microstructure|\bSEI\b|plating|deposition|\bFEM\b|COMSOL|PyBaMM", 0.15),
    (r"batter|electrolyte|cathode|anode|electrode", 0.05),
    (r"supercapacitor|zinc[- ]ion|sodium[- ]ion|fuel cell|photocatal|perovskite solar|wind|grid[- ]scale|hydrogen storage|thermoelectric|redox flow", -0.30),
]
_TERM_RES = [(re.compile(p, re.I), w) for p, w in _TERMS]


@dataclass
class TriageConfig:
    relevance_threshold: float = 0.35
    if_unknown_default: float = 3.0
    preprint_if: float = 0.0
    tiers: dict | None = None
    keyword_weights: dict | None = None
    active_keywords: list[str] | None = None

    def tier_for(self, if_: float, rel: float) -> str:
        tiers = self.tiers or {"A": {"min_if": 15, "min_relevance": 0.55},
                               "B": {"min_if": 8, "min_relevance": 0.45},
                               "C": {"min_if": 0, "min_relevance": 0.35}}
        for name in ("A", "B", "C"):
            t = tiers.get(name)
            if t and if_ >= float(t["min_if"]) and rel >= float(t["min_relevance"]):
                return name
        return ""


def rule_relevance(p: Paper) -> tuple[float, str]:
    """Deterministic fallback score in [0,1] with a short reason string."""
    text = " ".join([p.title, p.snippet or "", (p.abstract or "")[:1500]])
    score = 0.0
    hits: list[str] = []
    for rx, w in _TERM_RES:
        found = {m.group(0).lower() for m in rx.finditer(text)}
        if found:
            # diminishing returns: first hit full weight, each extra hit +25% up to 2x
            k = min(len(found), 5)
            score += w * (1 + 0.25 * (k - 1))
            hits += sorted(found)[:3]
    # title hits matter more than snippet hits
    title_bonus = 0.0
    for rx, w in _TERM_RES[:2]:
        if w > 0 and rx.search(p.title):
            title_bonus += 0.05
    score = max(0.0, min(0.95, score + title_bonus))  # 0.95 cap: LLM만 1.0을 줄 수 있음
    reason = "규칙 기반: " + (", ".join(dict.fromkeys(hits)) if hits else "매칭 용어 없음")
    return round(score, 3), reason


def apply_triage(p: Paper, journals: JournalTable, cfg: TriageConfig,
                 llm_relevance: tuple[float, str] | None = None) -> Paper:
    jm = journals.lookup(p.venue)
    p.journal_canonical = jm.canonical
    p.is_preprint = jm.is_preprint
    p.journal_if = cfg.preprint_if if jm.is_preprint else (jm.impact_factor if jm.matched_by != "default" else cfg.if_unknown_default)
    rel, reason = rule_relevance(p)
    if llm_relevance is not None:
        # LLM judgment dominates; rule score acts as a sanity floor/ceiling (±0.35 band)
        lrel, lreason = llm_relevance
        rel = max(min(lrel, rel + 0.35), rel - 0.35) if rel else lrel
        reason = f"LLM: {lreason} | {reason}"
    p.relevance = round(rel, 3)
    p.relevance_reason = reason
    kw_bonus = 0.0
    if cfg.keyword_weights:
        kw_bonus = sum(float(cfg.keyword_weights.get(k, 0.0)) for k in p.keywords_matched)
    p.tier = cfg.tier_for(p.journal_if or 0.0, p.relevance)
    inactive_only = bool(cfg.active_keywords) and p.keywords_matched and not (set(p.keywords_matched) & set(cfg.active_keywords))
    if inactive_only:
        p.status, p.tier = "rejected", ""
        p.relevance_reason = "키워드 추적 중단(" + ", ".join(p.keywords_matched) + ") | " + p.relevance_reason
        p.priority = round((p.journal_if or 0.0) * 1000 + p.relevance * 100, 3)
        return p
    if p.relevance < cfg.relevance_threshold:
        p.status = "rejected"
        p.tier = ""
    elif p.status in ("new", "rejected"):
        p.status = "triaged"
    p.priority = round((p.journal_if or 0.0) * 1000 + p.relevance * 100 + kw_bonus, 3)
    return p


def rank(papers: list[Paper]) -> list[Paper]:
    return sorted(papers, key=lambda x: (x.priority or 0.0, x.relevance or 0.0), reverse=True)
