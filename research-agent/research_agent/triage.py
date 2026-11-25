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
#
# 🔴 2026-09-04 — `db/` 407 · `kb/` 351 전수조사로 축 B 가 **캠페인 11개**임이 드러났고,
#   그중 ④산화안정성 cascade · ⑤도핑 깔때기 · ⑧Li₃N/LiC₆ · ⑨VGCF/h-BN · ⑪Cu–Zn 은
#   이 표에 **한 낱말도 없었다**. 아래 campaign/zn_rescue 두 줄이 그 구멍이다.
#   ⚠ `_TERM_RES[:2]` 가 title_bonus 에 쓰인다 — core/system 두 줄의 **자리를 옮기지 말 것**.
# 🔴 2026-09-04 병합 (Cowork v0.1.3) — 그쪽이 세 축 기준으로 재작성한 표에서 **내게 없던 것**을
#   보탰다. 겹치면 이쪽(캠페인 실측 기반) 우선. 제일 큰 구멍 셋이었다:
#     · 축 A 의 **MPM·Taichi·voxel·Kirchhoff·Bruggeman·Holm** — MPM 은 그 브랜치 90일 최다 주제(283회)인데 없었다
#     · **축 C(실험 협업)가 통째로 없었다** — EIS·대칭셀·Li-In·ASR 로 한 줄 신설
#     · 축 A 물성 용어(배위수·force chain·fabric tensor·Von Mises·유효전도도)
_TERMS: list[tuple[str, float]] = [
    (r"discrete[- ]element|\bDEM\b|LIGGGHTS|resistor[- ]network|percolat"
     r"|material[- ]point method|\bMPM\b|Taichi|voxel|Kirchhoff|Bruggeman|constriction|Holm"
     r"|first[- ]principles|\bDFT\b|density functional|ab initio|machine[- ]learning (interatomic )?potential|\bMLIP\b|\bAIMD\b|universal (interatomic )?potential"
     r"|nudged elastic band|\bNEB\b|LOBSTER|\bI?COHP\b|bond[- ]valence|\bBVSE\b|grand[- ]potential"
     r"|\bMACE\b|CHGNet|M3GNet|\bVASP\b|Quantum ESPRESSO"
     r"|anode[- ]free|anode[- ]less|zero[- ]excess", 0.35),
    (r"all[- ]solid[- ]state|solid[- ]state|sulfide|Li6PS5Cl|Li₆PS₅Cl|LPSCl|argyrodite|thiophosphate|halide (solid )?electrolyte"
     r"|solid electrolyte(?!\s+interphase)|composite (positive electrode|cathode)|single[- ]crystal", 0.25),
    # 축 C — 실험 협업(이종원 그룹). 내 표에 **한 줄도 없었다** (Cowork v0.1.3 이 잡았다).
    (r"\bEIS\b|electrochemical impedance|equivalent circuit|symmetric cell|\bLi[- ]In\b"
     r"|areal capacity|rate capability|\bASR\b|area specific resistance", 0.25),
    (r"elastic|modulus|adhesion|interfac|\bNCM\b|\bNMC\b|porosity|calender|compaction|contact|tortuosity|percolation"
     r"|coordination number|contact number|force chain|fabric tensor|Von Mises"
     r"|effective conductivity|ionic conductivity|electronic conductivity|thermal conductivity|grain boundary"
     r"|activation energy|diffusion barrier|binder|\bPTFE\b"
     r"|lithium metal|Li metal|current collector|interlayer|coating|microstructure|\bSEI\b|plating|deposition|\bFEM\b|COMSOL|PyBaMM", 0.15),
    # campaign — 축 B 의 개별 캠페인 계·관측량. 이것만으로는 threshold 를 못 넘긴다(설계).
    (r"Li3N|Li₃N|lithium nitride|LiC6|LiC₆|\bh-?BN\b|hexagonal boron nitride|\bVGCF\b"
     r"|LiNiO2|LiNiO₂|sulfonated|polaron|dopant|high[- ]throughput|screening funnel"
     r"|electrochemical stability window|convex hull|formation energy|decomposition (energy|reaction)"
     r"|band ?gap|adsorption energy|binding energy|migration barrier|surface diffusion|adatom"
     r"|Nernst[- ]Einstein|Haven ratio|mean squared displacement|Arrhenius|Van Hove", 0.15),
    (r"batter|electrolyte|cathode|anode|electrode", 0.05),
    # zn_rescue — ⑪ Zn ALZIB 는 **Cu–Zn 상동정**만 관련이다. 아래 −0.30 을 상쇄할 만큼만
    #   주고(0.20), 일반 zinc-ion 논문은 상쇄가 안 걸려 감점 그대로 탈락한다.
    #   ⚠ 0.30 으로 뒀다가 Cu–Zn 논문이 상한 0.95 까지 튀었다 — 상한은 LLM 몫이라 되돌렸다.
    (r"Cu[- ]Zn|\bbrass\b|Rietveld|phase identification|phase fingerprint", 0.20),
    (r"supercapacitor|zinc[- ]ion|sodium[- ]ion|potassium[- ]ion|fuel cell|photocatal|perovskite solar"
     r"|wind|grid[- ]scale|hydrogen storage|thermoelectric|redox flow|CALPHAD"
     r"|state[- ]of[- ]charge estimation|\bBMS\b", -0.30),
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
