"""artifact_policy.py — cascade artifact 의 **중앙 노출 정책**.

왜 (2026-08-14, Codex Round-3 P0-3)
  fail-closed 가 headline 타일에만 걸려 있었다. manifest 가 invalid 여도
  `load_cascade()` 는 legacy/v2/themes/funnel 을 직접 읽었고,
  `/api/file` · `/api/csv` · `/api/property` 는 정책을 통째로 우회했다.
  즉 "기본 화면에서 숨겼다" 가 "받을 수 없다" 를 뜻하지 않았다.

규약
  원장(`db/properties/cascade_audit_manifest.json`)이 artifact 마다 두 축을 싣는다:

    approval_status : historical | recovered_unvalidated | approved | superseded
                      | invalid | audit_current      ← "얼마나 믿을 수 있나"
    use_scope       : default_visible | archive_only | diagnostic_only | blocked
                      ← "어디까지 보여줄 수 있나"

  두 축은 **직교**한다. historical 이면서 archive_only 일 수 있고,
  recovered_unvalidated 이면서 diagnostic_only 일 수 있다.

  요청이 필요한 opt-in 을 안 들고 오면 **거부한다**(fail-closed).
    archive_only    → `?archive=1`
    diagnostic_only → `?view=diagnostic`
    blocked         → 어떤 파라미터로도 열리지 않는다
    원장에 없는 cascade artifact → 거부 (미등록 = 미승인)

이 모듈이 못 하는 것
  · cascade 밖 파일은 판정하지 않는다 (`is_governed()` 가 False → 통과).
  · 값을 검증하지 않는다. 지위만 본다.
  · 인증이 아니다 — 실수로 인용하는 것을 막는 장치이지 접근 통제가 아니다.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "db" / "properties" / "cascade_audit_manifest.json"

APPROVAL_STATUS = ("historical", "recovered_unvalidated", "approved",
                   "superseded", "invalid", "audit_current")
USE_SCOPE = ("default_visible", "archive_only", "diagnostic_only", "blocked")

#: scope → 필요한 쿼리 파라미터 (None 이면 조건 없음)
SCOPE_GATE = {"default_visible": None,
              "archive_only": ("archive", "1"),
              "diagnostic_only": ("view", "diagnostic"),
              "blocked": False}

#: 이 접두사에 걸리는 경로는 **반드시** 원장에 있어야 한다. 없으면 거부.
GOVERNED_PREFIXES = ("db/properties/cascade_", "db/properties/oxidation_stability_cascade",
                     "docs/figures/cascade/")


def _norm(rel: str) -> str:
    return str(rel).replace("\\", "/").lstrip("./")


def is_governed(rel: str) -> bool:
    r = _norm(rel)
    return any(r.startswith(p) for p in GOVERNED_PREFIXES)


def _load() -> dict:
    """원장 → {path: entry}. 원장이 없거나 깨졌으면 빈 dict (= 전부 거부)."""
    try:
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    for a in man.get("artifacts", []):
        out[_norm(a["source_path"])] = a
    for s in man.get("supporting_tables", []):
        out[_norm(s["path"])] = s
    for f in man.get("figures", []):
        for k in ("image", "csv"):
            out[_norm(f[k])] = f
    return out


def resolve(rel: str, args=None) -> dict:
    """이 경로를 지금 요청 조건에서 내보내도 되나.

    반환: {governed, allowed, approval_status, use_scope, reason, needs}
      · governed=False  → cascade 밖. 정책 대상 아님(통과).
      · allowed=False   → 거부. `needs` 가 필요한 파라미터, `reason` 이 사유.
    """
    r = _norm(rel)
    if not is_governed(r):
        return {"governed": False, "allowed": True, "reason": "", "needs": None,
                "approval_status": None, "use_scope": None}

    entry = _load().get(r)
    if entry is None:
        return {"governed": True, "allowed": False,
                "approval_status": None, "use_scope": None, "needs": None,
                "reason": ("원장(cascade_audit_manifest.json)에 없는 cascade artifact 다 — "
                           "미등록은 미승인으로 다룬다. "
                           "python3 tools/cascade/build_cascade_audit_manifest.py 로 등록할 것")}

    appr = entry.get("approval_status")
    scope = entry.get("use_scope")
    if appr not in APPROVAL_STATUS or scope not in USE_SCOPE:
        return {"governed": True, "allowed": False, "approval_status": appr,
                "use_scope": scope, "needs": None,
                "reason": f"어휘 밖 지위 (approval={appr!r} scope={scope!r}) — fail-closed"}

    if appr == "invalid":
        return {"governed": True, "allowed": False, "approval_status": appr,
                "use_scope": scope, "needs": None,
                "reason": "생성기 결함이 확인된 artifact 다 (invalid). 어떤 경로로도 내보내지 않는다"}

    gate = SCOPE_GATE[scope]
    if gate is False:
        return {"governed": True, "allowed": False, "approval_status": appr,
                "use_scope": scope, "needs": None, "reason": "blocked — 노출 금지"}
    if gate is None:
        return {"governed": True, "allowed": True, "approval_status": appr,
                "use_scope": scope, "needs": None, "reason": ""}

    key, want = gate
    got = None
    if args is not None:
        got = args.get(key) if hasattr(args, "get") else None
    if str(got) == want:
        return {"governed": True, "allowed": True, "approval_status": appr,
                "use_scope": scope, "needs": None, "reason": ""}
    return {"governed": True, "allowed": False, "approval_status": appr, "use_scope": scope,
            "needs": f"{key}={want}",
            "reason": (f"{scope} artifact 다 — `?{key}={want}` 없이는 내보내지 않는다. "
                       "승인된 current ranking 은 0종이므로 이건 결과가 아니라 "
                       + ("보관 기록" if scope == "archive_only" else "acquisition 진단물") + "이다")}


def envelope(rel: str, verdict: dict) -> dict:
    """API 응답에 붙일 지위 봉투. 값과 **같이** 나가야 인용 시 지위가 안 떨어진다."""
    return {"artifact": _norm(rel),
            "approval_status": verdict.get("approval_status"),
            "use_scope": verdict.get("use_scope"),
            "approved_current_ranking_species": 0,
            "note": ("cascade artifact 다. 승인된 current ranking 은 0종이며, 이 파일은 "
                     "감사·회수 근거이지 결과표가 아니다. "
                     "docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md")}
