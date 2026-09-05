"""피드백 루프 — Obsidian 노트의 체크박스를 읽어 선별 품질을 실측한다.

설계 원칙 세 가지. 전부 "적게 하되 정직하게"에 가깝다.

1. **노트가 진실의 원본이 아니다.** `Vault.write_paper_note` 는 매번 템플릿에서 노트를 다시 쓴다.
   그래서 체크한 것을 DB(`Paper.extra["feedback"]`)로 먼저 걷어 오고(harvest), 노트를 다시 쓸 때
   그 상태를 되살린다. 순서가 뒤집히면 사용자가 체크한 것이 조용히 사라진다 — `_vault_sync` 는
   반드시 harvest 를 먼저 부른다.

2. **표본이 적을 때는 학습하지 않는다.** n=4 로 만든 가중치는 없느니만 못하다. 점수 보정은
   `feedback.apply_to_scoring: true` 를 켜고 축별 표본이 `min_samples`(기본 8) 이상일 때만
   작동하고, 총 보정폭은 ±0.10 으로 묶여 있다. 기본값은 **꺼짐**이다.
   그때까지 이 모듈이 하는 일은 "보고"뿐이다.

3. **통과한 논문만 보는 표는 거짓말을 한다.** vault 에는 threshold 를 넘은 논문만 있으므로,
   여기서 계산한 정밀도(precision)는 **오탈락률(false negative)을 절대 못 본다.**
   그래서 `borderline_sample()` 로 threshold 바로 아래 논문을 주기적으로 디제스트에 끼워 넣어
   경계선을 실측한다. 이게 없으면 5년간 읽는 범위가 조용히 좁아진다.

triage.py 는 건드리지 않는다 (Claude Code 정본). 축 판별용 정규식도 여기서 따로 갖는다 —
그쪽 `_TERMS` 가 바뀌어도 이 보고서의 의미가 조용히 변하지 않게 하려는 의도적인 중복이다.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .models import Paper, now_iso

# --------------------------------------------------------------------------- 판정 정의
# label: (한국어 라벨, 점수, 별칭들)
VERDICTS: dict[str, tuple[str, float, tuple[str, ...]]] = {
    "useful":     ("유용함", 1.00, ("useful", "인용", "쓸모")),
    "irrelevant": ("무관",  -1.00, ("irrelevant", "잘못", "관련없음")),
    "read":       ("읽음",   0.25, ("read", "읽었음")),
    "skipped":    ("안 봄", -0.25, ("skipped", "안봄", "패스")),
}
# 여러 개를 체크했을 때: |점수|가 큰 것 우선, 같으면 아래 순서. (유용함 > 무관 > 읽음 > 안 봄)
_ORDER = ("useful", "irrelevant", "read", "skipped")

_FEEDBACK_HEADING = "## 피드백"
_RA_ID_RE = re.compile(r'^ra_id:\s*"?([^"\n]+)"?', re.M)
_WHY_RE = re.compile(r"^왜[:：]\s*(.*)$", re.M)

# 보고서용 축 판별 — 의도적으로 거칠고, triage.py 와 독립이다.
_AXIS_RES = {
    "축 A · DEM/MPM": re.compile(
        r"discrete[- ]element|\bDEM\b|material[- ]point|\bMPM\b|voxel|percolat|tortuos"
        r"|resistor[- ]network|coordination number|compaction|calender", re.I),
    "축 B · DFT/MLIP": re.compile(
        r"first[- ]principles|\bDFT\b|density functional|ab initio|\bVASP\b|\bNEB\b|\bAIMD\b"
        r"|machine[- ]learning (interatomic )?potential|\bMLIP\b|formation energy|adsorption", re.I),
    "축 C · 실험": re.compile(
        r"\bEIS\b|electrochemical impedance|symmetric cell|\bLi[- ]In\b|areal capacity"
        r"|rate capability|\bASR\b|full cell|cycling", re.I),
}


def _checkbox_re(label: str, aliases: tuple[str, ...]) -> re.Pattern:
    alts = "|".join(re.escape(x) for x in (label, *aliases))
    return re.compile(rf"^\s*-\s*\[([ xX])\]\s*(?:{alts})\b", re.M)


_VERDICT_RES = {k: _checkbox_re(v[0], v[2]) for k, v in VERDICTS.items()}


# --------------------------------------------------------------------------- 렌더링
def feedback_block(p: Paper) -> str:
    """노트에 넣을 피드백 섹션. 기존 판정이 있으면 체크된 상태로 되살린다."""
    fb = (p.extra or {}).get("feedback") or {}
    cur, why = fb.get("verdict"), (fb.get("note") or "")
    lines = [_FEEDBACK_HEADING,
             "> [!question] 읽고 나서 하나만 체크해 주세요 — 다음 선별에 반영됩니다."]
    for key in _ORDER:
        label, _, _ = VERDICTS[key]
        mark = "x" if cur == key else " "
        lines.append(f"- [{mark}] {label}{_HINT[key]}")
    lines.append(f"왜: {why}")
    if fb.get("at"):
        lines.append(f"<!-- feedback: {fb['verdict']} @ {fb['at']} -->")
    return "\n".join(lines)


_HINT = {
    "useful": " — 인용하거나 방법을 가져올 것",
    "irrelevant": " — 잘못 골랐음 (선별 기준을 고쳐야 함)",
    "read": " — 나쁘지 않지만 당장 쓸 곳은 없음",
    "skipped": " — 제목만 보고 넘김",
}


# --------------------------------------------------------------------------- 수집
def parse_note(text: str) -> dict[str, Any] | None:
    """노트 본문에서 판정을 뽑는다. 체크된 것이 없으면 None."""
    picked: list[tuple[str, float]] = []
    for key, rx in _VERDICT_RES.items():
        m = rx.search(text)
        if m and m.group(1).lower() == "x":
            picked.append((key, abs(VERDICTS[key][1])))
    if not picked:
        return None
    picked.sort(key=lambda kv: (-kv[1], _ORDER.index(kv[0])))
    verdict = picked[0][0]
    why = ""
    mw = _WHY_RE.search(text)
    if mw:
        why = mw.group(1).strip()
    return {"verdict": verdict, "note": why}


def harvest(cfg, db, papers_dir: Path | None = None) -> dict[str, int]:
    """vault 의 논문 노트와 경계선 노트를 훑어 체크된 판정을 DB 로 옮긴다.

    노트를 다시 쓰기 **전에** 불러야 한다. 매칭은 파일명이 아니라 frontmatter 의 `ra_id` 로
    한다 — 제목·연도가 나중에 보정돼 파일명이 바뀌어도 피드백이 끊기지 않는다.

    `Borderline/` 도 반드시 같이 훑는다. 디제스트가 "잘못 뺀 게 있나" 를 물어보는 곳이
    거기라, 여기서 빠지면 오탈락 측정이 구조적으로 영원히 0이 된다.
    """
    vault_root = cfg.path("vault.root")
    roots = ([papers_dir] if papers_dir else
             [vault_root / cfg.get("vault.papers_dir", "Papers"),
              vault_root / cfg.get("vault.borderline_dir", "Borderline")])
    stats = {"scanned": 0, "found": 0, "updated": 0, "unmatched": 0}
    paths = [q for root in roots if root.exists() for q in root.rglob("*.md")]
    if not paths:
        return stats
    by_id = {p.id: p for p in db.list()}
    for path in sorted(paths):
        stats["scanned"] += 1
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        m = _RA_ID_RE.search(text)
        if not m:
            continue
        parsed = parse_note(text)
        if not parsed:
            continue
        stats["found"] += 1
        p = by_id.get(m.group(1).strip())
        if p is None:
            stats["unmatched"] += 1
            continue
        old = (p.extra or {}).get("feedback") or {}
        if old.get("verdict") == parsed["verdict"] and old.get("note") == parsed["note"]:
            continue
        p.extra = dict(p.extra or {})
        p.extra["feedback"] = {**parsed, "at": now_iso(), "source": "vault"}
        db.save(p)
        stats["updated"] += 1
    return stats


def verdict_of(p: Paper) -> str | None:
    return ((p.extra or {}).get("feedback") or {}).get("verdict")


def score_of(p: Paper) -> float | None:
    v = verdict_of(p)
    return VERDICTS[v][1] if v in VERDICTS else None


# --------------------------------------------------------------------------- 집계
def _bucket_if(v: float | None) -> str:
    if v is None:
        return "IF 미상"
    for lo, name in ((20, "IF 20+"), (15, "IF 15–20"), (10, "IF 10–15"), (5, "IF 5–10"), (0.01, "IF 0–5")):
        if v >= lo:
            return name
    return "preprint"


def _axes_of(p: Paper) -> list[str]:
    text = " ".join([p.title or "", p.snippet or "", (p.abstract or "")[:1500]])
    return [name for name, rx in _AXIS_RES.items() if rx.search(text)] or ["미분류"]


def _agg(rows: list[Paper], key_fn) -> list[dict]:
    groups: dict[str, list[Paper]] = {}
    for p in rows:
        keys = key_fn(p)
        for k in (keys if isinstance(keys, list) else [keys]):
            groups.setdefault(str(k), []).append(p)
    out = []
    for k, ps in groups.items():
        n = len(ps)
        n_useful = sum(1 for p in ps if verdict_of(p) == "useful")
        n_bad = sum(1 for p in ps if verdict_of(p) in ("irrelevant", "skipped"))
        out.append({"key": k, "n": n, "n_useful": n_useful, "n_bad": n_bad,
                    "precision": round(n_useful / n, 3) if n else None,
                    "mean": round(sum(score_of(p) or 0 for p in ps) / n, 3) if n else None})
    return sorted(out, key=lambda r: (-r["n"], r["key"]))


def collect(db) -> list[Paper]:
    return [p for p in db.list() if verdict_of(p)]


def stats(db, min_samples: int = 8) -> dict[str, Any]:
    rows = collect(db)
    n = len(rows)
    base = {"n_feedback": n, "min_samples": min_samples, "enough": n >= min_samples,
            "counts": {k: sum(1 for p in rows if verdict_of(p) == k) for k in _ORDER}}
    if not rows:
        return base
    useful = [p for p in rows if verdict_of(p) == "useful"]
    bad = [p for p in rows if verdict_of(p) == "irrelevant"]
    base.update({
        "by_tier": _agg(rows, lambda p: p.tier or "-"),
        "by_if": _agg(rows, lambda p: _bucket_if(p.journal_if)),
        "by_keyword": _agg(rows, lambda p: p.keywords_matched or ["(없음)"]),
        "by_axis": _agg(rows, _axes_of),
        "rel_useful": round(sum(p.relevance or 0 for p in useful) / len(useful), 3) if useful else None,
        "rel_irrelevant": round(sum(p.relevance or 0 for p in bad) / len(bad), 3) if bad else None,
        "if_useful": round(sum(p.journal_if or 0 for p in useful) / len(useful), 2) if useful else None,
        "if_irrelevant": round(sum(p.journal_if or 0 for p in bad) / len(bad), 2) if bad else None,
    })
    return base


# --------------------------------------------------------------------------- 점수 보정
def axis_adjustments(db, min_samples: int = 8, cap: float = 0.10) -> dict[str, float]:
    """축별 relevance 보정값. 표본이 모자란 축은 아예 넣지 않는다 (0 이 아니라 부재).

    보정 = (축 평균 - 전체 평균) × 축소계수(n/(n+8)) × cap, |합| ≤ cap.
    """
    rows = collect(db)
    if len(rows) < min_samples:
        return {}
    overall = sum(score_of(p) or 0 for p in rows) / len(rows)
    out: dict[str, float] = {}
    for r in _agg(rows, _axes_of):
        if r["n"] < min_samples or r["key"] == "미분류":
            continue
        shrink = r["n"] / (r["n"] + 8.0)
        delta = (r["mean"] - overall) * shrink * cap
        out[r["key"]] = round(max(-cap, min(cap, delta)), 4)
    return out


def adjust_relevance(p: Paper, adjustments: dict[str, float], cap: float = 0.10) -> tuple[float, str]:
    """논문 하나에 축 보정을 적용해 (새 relevance, 사유) 를 돌려준다. 원본은 안 건드린다."""
    base = p.relevance or 0.0
    if not adjustments:
        return base, ""
    deltas = [(a, adjustments[a]) for a in _axes_of(p) if a in adjustments]
    if not deltas:
        return base, ""
    total = max(-cap, min(cap, sum(d for _, d in deltas)))
    reason = "피드백 보정: " + ", ".join(f"{a} {d:+.3f}" for a, d in deltas)
    return round(max(0.0, min(1.0, base + total)), 3), reason


def enabled(cfg) -> bool:
    """`feedback.apply_to_scoring` 가 명시적으로 켜져 있을 때만 True. 기본은 꺼짐."""
    try:
        return bool(cfg.get("feedback.apply_to_scoring", False))
    except Exception:
        return False


# --------------------------------------------------------------------------- 경계선 표본
def borderline_sample(db, n: int = 2, band: float = 0.10, threshold: float = 0.35,
                      cooldown_days: int = 30) -> list[Paper]:
    """threshold 바로 아래에서 걸러진 논문을 n편 뽑는다 — 오탈락률을 재기 위한 표본.

    vault 만 보면 "골라낸 것 중 몇 개가 좋았나"만 알 수 있고 "버린 것 중 좋은 게 있었나"는
    영영 안 보인다. 5년짜리 시스템에서 이건 조용히 읽는 범위를 좁힌다. 그래서 가끔 물어본다.
    이미 판정을 준 논문과 최근에 물어본 논문은 다시 뽑지 않는다.
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(days=cooldown_days)).isoformat(timespec="seconds")
    cands = []
    for p in db.list(status="rejected"):
        rel = p.relevance or 0.0
        if not (threshold - band <= rel < threshold):
            continue
        if verdict_of(p):
            continue
        asked = (p.extra or {}).get("borderline_asked_at")
        if asked and asked > cutoff:
            continue
        cands.append(p)
    cands.sort(key=lambda x: (x.relevance or 0, x.journal_if or 0), reverse=True)
    return cands[:n]


def mark_asked(db, papers: list[Paper]) -> None:
    for p in papers:
        p.extra = dict(p.extra or {})
        p.extra["borderline_asked_at"] = now_iso()
        db.save(p)


# --------------------------------------------------------------------------- 보고서
def _table(rows: list[dict], head: str) -> list[str]:
    if not rows:
        return []
    out = [f"**{head}**", "", "| | n | 유용함 | 무관·안 봄 | 정밀도 | 평균점수 |", "|---|---|---|---|---|---|"]
    for r in rows:
        prec = "-" if r["precision"] is None else f"{r['precision']:.2f}"
        mean = "-" if r["mean"] is None else f"{r['mean']:+.2f}"
        out.append(f"| {r['key']} | {r['n']} | {r['n_useful']} | {r['n_bad']} | {prec} | {mean} |")
    out.append("")
    return out


def render_report(db, cfg=None, min_samples: int = 8) -> str:
    s = stats(db, min_samples)
    n = s["n_feedback"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ["---", "title: 피드백 보정", "tags: [research-agent, calibration]",
             f"updated: {now}", f"n_feedback: {n}", "---", "", "# 피드백 보정", ""]
    c = s["counts"]
    lines += [f"> [!summary] 피드백 {n}건 "
              f"(유용함 {c['useful']} · 무관 {c['irrelevant']} · 읽음 {c['read']} · 안 봄 {c['skipped']})", ""]
    if n < min_samples:
        lines += [f"> [!warning] 아직 판단할 표본이 아니다 — {n}/{min_samples}건",
                  "> 지금 표를 그려도 잡음이다. 점수 보정도 켜지 않는다.",
                  "> 논문 노트 맨 아래 `## 피드백`에서 하나만 체크하면 여기에 쌓인다.", ""]
        return "\n".join(lines) + "\n"

    lines += _table(s.get("by_tier", []), "Tier 별 — Tier A 가 실제로 제일 유용한가")
    lines += _table(s.get("by_if", []), "IF 구간 별 — IF 우선 정렬이 맞았는지 여기서 판가름난다")
    lines += _table(s.get("by_keyword", []), "키워드 별")
    lines += _table(s.get("by_axis", []), "축 별")

    ru, ri = s.get("rel_useful"), s.get("rel_irrelevant")
    if ru is not None and ri is not None:
        gap = ru - ri
        lines += ["**threshold 점검**", "",
                  f"- 유용함 판정 논문의 평균 관련도 **{ru:.3f}** / 무관 판정 **{ri:.3f}** (차이 {gap:+.3f})",
                  (f"- 차이가 {gap:+.3f} 로 작다 — 관련도 점수가 유용함을 잘 못 가른다는 뜻이다. "
                   "threshold 를 올리는 것보다 채점 용어를 손보는 쪽이 맞다."
                   if abs(gap) < 0.10 else
                   "- 관련도 점수가 유용함과 같은 방향으로 움직인다 — 채점이 작동하고 있다."), ""]
    iu, ii = s.get("if_useful"), s.get("if_irrelevant")
    if iu is not None and ii is not None:
        lines += [f"- 유용함 논문 평균 IF **{iu}** / 무관 **{ii}** — "
                  + ("IF 가 유용함을 예측하지 못한다. IF 우선 정렬을 재검토할 근거다."
                     if iu <= ii else "IF 우선 정렬을 유지할 근거가 있다."), ""]

    adj = axis_adjustments(db, min_samples)
    lines += ["## 점수 보정", ""]
    if not adj:
        lines += [f"- 축별 표본이 {min_samples}건에 못 미쳐 보정값을 만들지 않았다.", ""]
    else:
        lines += [f"- {a}: **{d:+.3f}**" for a, d in sorted(adj.items())]
        on = enabled(cfg) if cfg is not None else False
        lines += ["", f"- 적용 여부: **{'켜짐' if on else '꺼짐'}** "
                      f"(`config/agent.yaml` 의 `feedback.apply_to_scoring` — 기본값은 꺼짐)", ""]

    lines += ["> [!danger] 이 표가 못 보는 것",
              "> 여기 있는 논문은 전부 **threshold 를 통과한 것**이다. 그래서 정밀도는 보이지만",
              "> **오탈락(좋은데 걸러낸 것)은 안 보인다.** 그쪽은 디제스트의 '경계선 확인' 항목으로만",
              "> 잴 수 있으니, 거기 뜨는 2편에도 판정을 남겨 주세요.", ""]
    return "\n".join(lines) + "\n"
