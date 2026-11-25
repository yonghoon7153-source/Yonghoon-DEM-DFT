"""Deep analysis stage (the '논문 에이전트').

Two execution modes share one contract (prompts/deep_analysis.md JSON schema):
  * direct  — LLM backend (anthropic / claude-cli) is called here.
  * queued  — a job file is written to data/analysis/pending/<paper_id>.json for Hermes Agent /
              Claude Code / Cowork to fill in; results are imported with `import_analysis_file`.
"""
from __future__ import annotations

import json
from pathlib import Path

from .config import Config
from .db import PaperDB
from .llm import LLM
from .models import Paper, now_iso

REQUIRED_KEYS = {"one_liner", "selection_reason", "key_findings"}


def build_prompt(cfg: Config, p: Paper) -> tuple[str, str]:
    system = "\n\n".join([
        cfg.load_prompt("deep_analysis"),
        "# [문체 규칙]\n" + cfg.load_prompt("style_guide"),
        "# [연구 프로필]\n" + cfg.load_research_profile(),
    ])
    user = "\n".join([
        "# [논문 정보]",
        f"- id: {p.id}",
        f"- title: {p.title}",
        f"- authors: {', '.join(p.authors) or 'unknown'}",
        f"- venue: {p.journal_canonical or p.venue} ({p.year or 'n.d.'}) · IF {p.journal_if}",
        f"- doi/url: {p.doi or ''} {p.url}",
        f"- keywords_matched: {', '.join(p.keywords_matched)}",
        f"- rule relevance: {p.relevance} ({p.relevance_reason})",
        f"- snippet: {p.snippet}",
        f"- abstract: {p.abstract or '(없음 — 스니펫 기준으로 분석하고 evidence_level=snippet)'}",
        f"- extra: {json.dumps(p.extra, ensure_ascii=False) if p.extra else '{}'}",
    ])
    return system, user


def validate_analysis(a: dict) -> tuple[bool, str]:
    if not isinstance(a, dict):
        return False, "JSON 객체가 아님"
    missing = REQUIRED_KEYS - set(a)
    if missing:
        return False, f"필수 키 누락: {sorted(missing)}"
    if not isinstance(a.get("key_findings"), list):
        return False, "key_findings는 배열이어야 함"
    return True, "ok"


def apply_analysis(p: Paper, a: dict, cfg_threshold: float | None = None, tiers: dict | None = None) -> Paper:
    """Store the analysis and re-derive relevance/tier/priority from the LLM's judgement."""
    from .triage import TriageConfig
    p.analysis = a
    p.analyzed_at = now_iso()
    try:
        rel = float(a.get("relevance", p.relevance or 0))
        if 0 <= rel <= 1:
            p.relevance = round(rel, 3)
            if a.get("relevance_reason"):
                p.relevance_reason = "LLM: " + str(a["relevance_reason"])
    except (TypeError, ValueError):
        pass
    tc = TriageConfig(relevance_threshold=cfg_threshold if cfg_threshold is not None else 0.35, tiers=tiers)
    p.tier = tc.tier_for(p.journal_if or 0.0, p.relevance or 0.0)
    p.priority = round((p.journal_if or 0.0) * 1000 + (p.relevance or 0.0) * 100, 3)
    if (p.relevance or 0) < tc.relevance_threshold:
        p.status = "rejected"
        p.tier = ""
    else:
        p.status = "analyzed"
    return p


def queue_job(cfg: Config, p: Paper) -> Path:
    pending = cfg.path("storage.analysis_queue")
    pending.mkdir(parents=True, exist_ok=True)
    system, user = build_prompt(cfg, p)
    job = {
        "paper_id": p.id,
        "title": p.title,
        "created_at": now_iso(),
        "instructions": "아래 prompt_user를 읽고 prompt_system의 JSON 스키마대로 `analysis` 필드를 채운 뒤 "
                        "`ra analyze --from-file <this file>` 로 가져오세요. (Hermes: paper-agent 스킬 절차 3단계)",
        "prompt_system": system,
        "prompt_user": user,
        "analysis": None,
    }
    path = pending / f"{_safe(p.id)}.json"
    path.write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def _safe(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)


def analyze_direct(cfg: Config, llm: LLM, p: Paper) -> dict | None:
    system, user = build_prompt(cfg, p)
    return llm.complete_json(system, user)


def import_analysis_file(cfg: Config, db: PaperDB, path: Path, paper_id: str | None = None) -> Paper:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    # accept either the job-file shape {"paper_id","analysis":{...}} or a bare analysis dict
    if "analysis" in data and isinstance(data["analysis"], dict):
        a, pid = data["analysis"], data.get("paper_id") or paper_id
    else:
        a, pid = data, paper_id or data.get("paper_id")
    if not pid:
        raise ValueError("paper_id를 알 수 없음 (--paper-id 지정 필요)")
    ok, msg = validate_analysis(a)
    if not ok:
        raise ValueError(f"분석 JSON 검증 실패: {msg}")
    p = db.get(pid)
    if not p:
        raise KeyError(f"DB에 없는 paper_id: {pid}")
    apply_analysis(p, a, float(cfg.get("triage.relevance_threshold", 0.35)), cfg.get("triage.tiers"))
    db.save(p)
    done = cfg.path("storage.analysis_done")
    done.mkdir(parents=True, exist_ok=True)
    (done / f"{_safe(pid)}.json").write_text(json.dumps({"paper_id": pid, "analysis": a, "imported_at": now_iso()},
                                                         ensure_ascii=False, indent=1), encoding="utf-8")
    pend = cfg.path("storage.analysis_queue") / f"{_safe(pid)}.json"
    if pend.exists() and pend.resolve() != Path(path).resolve():
        pend.unlink()
    elif pend.exists():
        pend.unlink()
    return p
