"""canonical.py — 정본값의 **단일 진실 원천**을 db 에서 읽고 원자료와 대조한다.

왜 만들었나 (2026-08-07 Codex 코드리뷰 P1)
  화면 정본값이 `db/properties` 가 아니라 `data.py` 의 `CANONICAL` 딕셔너리에 **한 번 더**
  하드코딩돼 있었다. 새 계산을 db 에 등록해도 이 딕셔너리를 손대지 않으면 화면은 그대로다
  — 교차검증 도구에서 제일 위험한 형태의 조용한 drift.

  ★ 그리고 리뷰가 짚은 것보다 한 겹 더 나쁜 게 있었다. `CANONICAL["MD_Ea_eV"]` 안에서
    **프로토콜이 섞여 있었다**: comp1 0.253·modelc 0.224 는 단일 궤적인데 lpsocl 0.287 은
    4-seed×3-T 다. 그러니 대시보드가 `sorted()` 로 고른 "최저값"은 라벨을 고쳐도 여전히
    무효다 — 단일시드와 멀티시드를 한 줄에 세운 순위였다.
    → 그래서 값마다 `comparison_group` 을 달고, **같은 group 안에서만** 순위·비교를 한다.

무엇이 정본인가
  db/properties/canonical_registry.json 의 entries. 각 항목은 원자료 위치를
  (source_path, source_key) 로 가리키고, 이 모듈이 그걸 **따라가서 값이 맞는지 검사**한다.

  from canonical import load_registry, canonical_map, validate
  reg = load_registry()
  canonical_map(reg, "gap_eV")                    # {"comp1": 2.066, ...}
  canonical_map(reg, "MD_Ea_eV", group="md-ea-multiseed-v1")
  validate(reg)                                   # [(entry, 문제) ...]
"""
from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "db" / "properties" / "canonical_registry.json"

# source_key 미니 문법 — 일부러 작게 유지한다. 못 읽는 표기는 조용히 넘기지 않고 오류로 낸다.
#   JSON:  /a/b/c                     중첩 키
#          /a/results[?id=comp1]/E_VRH   리스트에서 id==comp1 인 원소
#   CSV:   [?system=LPSCl1.6]/Ea_eV   system 열이 그 값인 행의 Ea_eV 열
_SEL = re.compile(r"^\[\?([^=\]]+)=([^\]]*)\]$")


class ResolveError(Exception):
    pass


def _step(node, tok, where):
    m = _SEL.match(tok)
    if m:
        k, want = m.group(1), m.group(2)
        if not isinstance(node, list):
            raise ResolveError(f"{where}: {tok} 는 리스트에만 쓸 수 있다 (실제 {type(node).__name__})")
        for it in node:
            if isinstance(it, dict) and str(it.get(k)) == want:
                return it
        raise ResolveError(f"{where}: {k}={want} 인 원소가 없다")
    if isinstance(node, dict):
        if tok not in node:
            raise ResolveError(f"{where}: 키 '{tok}' 없음 (있는 키: {list(node)[:8]})")
        return node[tok]
    if isinstance(node, list):
        try:
            return node[int(tok)]
        except (ValueError, IndexError):
            raise ResolveError(f"{where}: 리스트 인덱스 '{tok}' 를 쓸 수 없다")
    raise ResolveError(f"{where}: '{tok}' 아래로 못 들어간다 ({type(node).__name__})")


def resolve(source_path: str, source_key: str, root=None):
    """원자료에서 실제 값을 꺼낸다. 못 꺼내면 ResolveError — **조용히 None 을 주지 않는다.**

    ⚠ `root` 는 **테스트 전용**이다. 이게 없으면 회귀 테스트가 추적 중인 정본 파일
      (db/properties/*.json)을 직접 고쳤다 뺐다 해야 하는데, hard kill·전원 손실처럼
      finally 가 안 도는 중단에서 **정본이 오염된 채 남는다** (2026-08-07 Codex 3라운드).
      root 를 임시 디렉터리로 주면 fixture 가 repo 밖에서 완결된다.
    """
    p = (Path(root) if root else ROOT) / source_path
    if not p.is_file():
        raise ResolveError(f"{source_path}: 파일 없음")
    toks = [t for t in source_key.split("/") if t != ""]
    if p.suffix.lower() == ".csv":
        # ⚠ 우리 CSV 는 '#' 주석 줄이 섞여 있다(인용 금지 문구가 거기 산다). 걸러내고 읽는다.
        with open(p, encoding="utf-8", errors="ignore") as f:
            rows = [ln for ln in f if not ln.lstrip().startswith(("#", '"#'))]
        node = list(csv.DictReader(rows))
    else:
        node = json.load(open(p, encoding="utf-8"))
    for t in toks:
        node = _step(node, t, source_path)
    if isinstance(node, str):
        # "0.287 +/- 0.024" 같은 서술형은 앞의 수만 받는다 (오차는 uncertainty 필드에 따로)
        m = re.match(r"\s*(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)", node)
        if not m:
            raise ResolveError(f"{source_path}:{source_key}: 문자열에서 수를 못 읽었다 ({node[:40]!r})")
        return float(m.group(1))
    if isinstance(node, bool) or node is None:
        raise ResolveError(f"{source_path}:{source_key}: 수가 아니다 ({node!r})")
    return float(node)


def load_registry(path=None, live=True, root=None) -> dict:
    """레지스트리를 읽고, **원자료 값으로 덮어쓴다**(live=True).

    ★ 2026-08-07 Codex 재검증의 지적: 첫 판은 레지스트리에 `value` 를 **복제**해 두고
      원자료 대조는 validator 에서만 했다. 그러면 "원자료 한 곳만 고치면 화면이 갱신된다"
      가 성립하지 않는다 — db 를 고쳐도 화면은 그대로고 검사만 실패한다.
      → 이제 로드할 때 source_path/source_key 를 **실제로 따라가** 그 값을 쓴다.
        레지스트리의 `value` 는 이제 "마지막으로 확인한 값"(기대치)이고, 원자료가 우선이다.
        어긋나면 `value_drift` 에 기록해 화면·검사가 볼 수 있게 남긴다.

    ⚠ 원자료를 못 읽으면 레지스트리 값으로 떨어지되 **status 를 `source_error` 로 내린다**
      (2026-08-07 Codex 3라운드). 첫 판은 `resolve_error` 만 적고 status 는 canonical 로
      뒀는데, 화면 순위는 validator 를 안 돌리므로 **stale 값이 계속 정본으로 쓰였다.**
      사이트가 죽는 것보다는 낫지만, 검증 안 된 값이 정본 자리에 남는 건 더 나쁘다.
    """
    p = Path(path) if path else REGISTRY
    if not p.is_file():
        return {"schema": "canonical_registry/v1", "entries": []}
    reg = json.load(open(p, encoding="utf-8"))
    if not live:
        return reg
    for e in reg.get("entries", []):
        sp, sk = e.get("source_path"), e.get("source_key")
        if not (sp and sk):
            continue
        try:
            got = resolve(sp, sk, root)
        except ResolveError as ex:
            e["resolve_error"] = str(ex)
            e["status"] = "source_error"      # ← 자동판정에서 반드시 빠진다
            continue
        want = e.get("value")
        tol = float(e.get("tolerance", 5e-4))
        e["value_from_source"] = got
        if want is not None and abs(got - float(want)) > tol:
            # ★ 원자료가 레지스트리 기대치를 넘어 바뀌었다 = **새 계산이 들어왔다.**
            #   화면은 원자료를 따라간다(그래야 "db 한 곳만 고치면 갱신"이 성립).
            #   대신 status 를 내려 **순위·레이더에서 자동으로 빠지게** 하고 validator 를
            #   실패시킨다 — 사람이 레지스트리를 갱신하며 검토해야 정본으로 돌아온다.
            #   이게 "조용한 drift" 와 "조용한 채택" 을 둘 다 막는 유일한 배치다.
            e["value"] = got
            e["value_drift"] = {"registry": want, "source": got}
            e["status"] = "unreviewed_drift"
        elif e.get("prefer") == "registry":
            # ⚠ 원자료가 **반올림된 사본**인 예외 (eos.json 26.2 vs 정본 26.23).
            #   정밀한 원 출처를 배선하기 전까지만 쓰는 표식이고, 이유를 note 에 적는다.
            pass
        else:
            e["value"] = got          # ★ 기본: db 를 고치면 화면이 따라온다
    return reg


# ─────────────────────────────────────────────────────────────
# 실행 중 갱신 (2026-08-07 Codex 3라운드)
#
# 첫 판의 live 는 **프로세스 시작 시 한 번**이었다 — data.py 가 import 때 _REG 를 만들고
# 라우트가 그 전역을 그대로 넘겼다. 그래서 gunicorn worker 가 오래 살아 있으면 db 를 고쳐도
# 재시작 전에는 화면이 안 바뀐다. "db 한 곳만 고치면 갱신" 이 반쪽이었다.
#   → 레지스트리 + **참조하는 모든 원자료**의 mtime 을 합쳐 캐시 키로 쓴다.
#     파일이 하나라도 바뀌면 다시 읽는다. stat 몇 번이라 요청마다 해도 싸다.
#     (이 앱은 원래 "db 를 요청마다 읽는다" 가 설계 전제다.)
# ─────────────────────────────────────────────────────────────
_CACHE = {"key": None, "reg": None}


def _mtime_key(path=None, root=None) -> tuple:
    p = Path(path) if path else REGISTRY
    keys = [(str(p), p.stat().st_mtime_ns if p.is_file() else 0)]
    try:
        raw = json.load(open(p, encoding="utf-8")) if p.is_file() else {"entries": []}
    except (OSError, ValueError):
        return tuple(keys)
    for sp in sorted({e.get("source_path") for e in raw.get("entries", []) if e.get("source_path")}):
        f = (Path(root) if root else ROOT) / sp
        keys.append((sp, f.stat().st_mtime_ns if f.is_file() else 0))
    return tuple(keys)


def registry(path=None, root=None) -> dict:
    """캐시된 레지스트리. **원자료가 바뀌면 자동으로 다시 읽는다.**

    화면 코드는 `load_registry()` 대신 이걸 쓴다 — 그래야 오래 사는 worker 에서도
    db 수정이 다음 요청에 반영된다.
    """
    k = (_mtime_key(path, root), str(path), str(root))
    if _CACHE["key"] != k:
        _CACHE["reg"] = load_registry(path, root=root)
        _CACHE["key"] = k
    return _CACHE["reg"]


#: 게이트 판정 어휘 — **단일 출처**. 화면·API·validator·테스트가 전부 여기를 읽는다.
#: ⛔ 2026-08-20 (codex 동결감사) — 이전에는 `blocking_gate` 가 있으면 무조건 "미통과"
#:   였고, 그 사본이 data.py·compare.html·canonical.py·test_webapp.py 네 곳에 흩어져
#:   있었다. b2o3 골격 게이트는 **미평가(not_assessed)** 이지 실패가 아닌데 네 곳 모두
#:   실패로 읽었다 — F2(화면 ≠ db)의 재발이다. 어휘와 판정을 한 함수로 모은다.
GATE_OUTCOMES = ("not_assessed", "pass", "fail", "inapplicable")

_GATE_LABEL = {
    "not_assessed": "게이트 미평가(실패 판정이 아니다)",
    "pass":         "게이트 통과",
    "fail":         "게이트 미통과",
    "inapplicable": "게이트 비해당",
    None:           "게이트 미통과",      # 결과 미기재 = 옛 항목. 보수적으로 실패로 읽는다
}


ASSESSMENTS_PATH = "db/governance/assessments.json"


def assessments(root=None) -> dict:
    """게이트 판정 원장 (append-only sidecar). {assessment_id: record}.

    ⛔ 못 하는 것: 판정을 **만들지 않는다**. 원장을 읽을 뿐이고, 판정 산출은
       도구(msd_diffusive_check --framework 등) 소관이다.
    """
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    p = base / ASSESSMENTS_PATH
    if not p.exists():
        return {}
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:                        # noqa: BLE001
        raise RuntimeError(f"⛔ {ASSESSMENTS_PATH} 를 못 읽는다 — 판정 원장 없이 지위를 "
                           f"계산하지 않는다 (fail-closed): {exc!r}") from exc
    return {a["assessment_id"]: a for a in raw.get("assessments", [])}


def gate_outcome(e: dict, root=None):
    """canonical entry 의 게이트 판정. 게이트가 없으면 None.

    반환: "not_assessed" | "pass" | "fail" | "inapplicable" | None(게이트 없음)

    우선순위:
      ① required_assessment_refs → sidecar 의 state=active 레코드 (권위)
      ② gate_detail.lineage.gate_outcome (레거시 경로 — 아직 이관 안 된 항목)
      ③ 둘 다 없으면 fail (보수적)

    ⛔ 2026-08-20 (codex 동결감사) — 판정을 canonical claim 안에 두면 consumer 마다
      '현재 판정' 을 다르게 고를 수 있다. ①이 있으면 ②는 **보지 않는다**.
    ⛔ 못 하는 것: 게이트를 평가하지 않는다. 기록된 판정을 읽을 뿐이다.
    """
    if not e.get("blocking_gate"):
        return None
    refs = e.get("required_assessment_refs")
    if refs:
        book = assessments(root)
        missing = [r for r in refs if r not in book]
        if missing:
            raise RuntimeError(f"⛔ {e.get('metric')}/{e.get('system')} 이 없는 판정을 "
                               f"참조한다: {missing} — fail-closed")
        active = [book[r] for r in refs if book[r].get("state") == "active"]
        if len(active) != 1:
            raise RuntimeError(f"⛔ {e.get('metric')}/{e.get('system')} 의 active 판정이 "
                               f"{len(active)}개다 (1개여야 한다): {refs}")
        out = active[0].get("result")
        return out if out in GATE_OUTCOMES else "fail"
    lin = (e.get("gate_detail") or {}).get("lineage") or {}
    out = lin.get("gate_outcome") or (lin.get("current_assessment") or {}).get("result")
    if out in GATE_OUTCOMES:
        return out
    return "fail"       # 게이트는 걸렸는데 판정 기록이 없다 → 보수적으로 실패


def gate_blocks_canonical(e: dict) -> bool:
    """이 게이트 상태에서 status=canonical 이 허용되는가(의 반대).

    미평가도 **통과가 아니므로** 정본을 막는다 — 다만 사유 문구가 다르다.
    """
    return gate_outcome(e) in ("fail", "not_assessed")


def gate_prefix(e: dict) -> str:
    """툴팁·배지 앞에 붙는 게이트 문구. 게이트가 없으면 빈 문자열."""
    o = gate_outcome(e)
    if o is None:
        return ""
    return f"{_GATE_LABEL.get(o, _GATE_LABEL[None])}: {e['blocking_gate']}. "


#: lineage 축 어휘 — **두 축은 독립**이다 (codex R4). 한 enum 으로 합치면 사다리가 된다.
LINEAGE_BINDING = ("missing", "prose_only", "unverified", "unwired", "wired", "verified")
NUMERIC_REPRO = ("none", "approximate", "exact")


def decisions(root=None) -> dict:
    """판례 원장. {decision_id: record}. 없으면 빈 dict."""
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    p = base / "db/governance/decisions.json"
    if not p.exists():
        return {}
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:                        # noqa: BLE001
        raise RuntimeError(f"⛔ decisions.json 을 못 읽는다 (fail-closed): {exc!r}") from exc
    return {d["id"]: d for d in raw.get("decisions", [])}


def decision_digest(d: dict) -> str:
    """결정 내용의 지문 — `ratification` 을 **뺀** 나머지의 sha256.

    ⛔ 2026-08-20 (codex: "ratification 에 policy 포함 + decision digest 에 결속") —
      승인이 상태 문자열 하나면, 승인 뒤 statement·enforcement 를 고쳐도 승인이 남는다.
      승인 시점의 내용을 지문으로 묶어 두면 내용이 바뀐 순간 승인이 **무효로 보인다**.
    """
    import hashlib
    body = {k: v for k, v in d.items() if k != "ratification"}
    return "sha256:" + hashlib.sha256(
        json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


#: 산출물 원장 어휘
ARTIFACT_STATUS = ("canonical", "reference", "suspect_banned", "superseded", "lost")
LOCATION_KINDS = ("repo", "offline_backup", "server", "lost")


def artifacts(root=None) -> dict:
    """repo 밖 원자료 원장. {artifact_id: record}. 없으면 빈 dict.

    ⛔ 못 하는 것: **파일이 실제로 거기 있는지 확인하지 않는다** (로컬 마운트·원격 서버라
      CI 가 닿지 못한다). 어휘·일관성만 검사한다.
    """
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    p = base / "db/governance/artifacts.json"
    if not p.exists():
        return {}
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:                        # noqa: BLE001
        raise RuntimeError(f"⛔ artifacts.json 을 못 읽는다 (fail-closed): {exc!r}") from exc
    return {a["id"]: a for a in raw.get("artifacts", [])}


def validate_artifacts(root=None) -> list:
    """산출물 원장의 내부 일관성. 위반 문자열 리스트.

    ⛔ 2026-08-20 — 하루에 같은 사고가 다섯 번 났다: 산출물은 있는데 **위치·지위·판정이
      기계 경로 밖**(사람 기억·파일명 접두사·다른 서버 CSV 헤더)에 있었다.
      이 검사는 그 판정들이 **원장 안에** 있는지를 본다.
    """
    bad = []
    for a in artifacts(root).values():
        i = a.get("id", "?")
        st = a.get("status")
        if st not in ARTIFACT_STATUS:
            bad.append(f"산출물 {i} 의 status 가 어휘 밖이다: {st!r}")
        kind = (a.get("location") or {}).get("kind")
        if kind not in LOCATION_KINDS:
            bad.append(f"산출물 {i} 의 location.kind 가 어휘 밖이다: {kind!r}")
        # ⭐ 밴은 사유가 원장 안에 있어야 한다 — 파일명·기억은 판정이 아니다
        if st == "suspect_banned" and not a.get("ban_evidence"):
            bad.append(f"산출물 {i} 가 suspect_banned 인데 ban_evidence 가 없다 — "
                       f"판정이 원장 밖(파일명·기억)에 있다는 뜻이다")
        if st == "suspect_banned" and not a.get("unban_condition"):
            bad.append(f"산출물 {i} 에 unban_condition 이 없다 — 영구 보류가 된다")
        # 유일본 + canonical 이면 이중화 표시가 있어야 한다
        if st == "canonical" and a.get("copies") == 1 and not a.get("needs_duplication"):
            bad.append(f"산출물 {i} 가 canonical 유일본인데 needs_duplication 표시가 없다")
        if st == "lost" and a.get("copies") not in (0, None):
            bad.append(f"산출물 {i} 가 lost 인데 copies={a.get('copies')} 다")
        if kind in ("offline_backup", "server") and not (a.get("verified") or {}).get("level"):
            bad.append(f"산출물 {i} 가 repo 밖인데 verified.level 이 없다 "
                       f"(위치만 봤는지 내용까지 봤는지 구분해야 한다)")
    return bad


def validate_governance(reg: dict = None, root=None) -> list:
    """판례·판정 원장의 무결성. 위반 문자열 리스트 (빈 리스트 = 통과).

    ⛔ 2026-08-20 (codex 동결감사) — validate_canonical 이 새 필드를 안 읽어 이번 정정을
      **db 도구가 스스로 검증하지 못했다**. webapp 테스트만 잡는 상태였다.
      이 함수 하나를 db 도구와 테스트가 **같이** 쓴다 (검사 로직 사본 금지).

    ⛔ 못 하는 것: 판정의 **과학적 타당성**은 안 본다. 그래프 무결성과 어휘만 본다.
    """
    bad = list(validate_artifacts(root))
    dec, book = decisions(root), assessments(root)

    # ── 판례 그래프 ──────────────────────────────────────────────────────
    for d in dec.values():
        for ref in d.get("supersedes", []):
            if ref not in dec:
                bad.append(f"결정 {d['id']} 의 supersedes 대상 {ref} 가 원장에 없다 (dangling)")
        sb = d.get("superseded_by")
        if sb and sb not in dec:
            bad.append(f"결정 {d['id']} 의 superseded_by {sb} 가 원장에 없다 (dangling)")
        rat = d.get("ratification") or {}
        if d.get("decision_state") == "active" and not (
                rat.get("state") == "ratified" and rat.get("role") == "scientific_owner"):
            bad.append(f"결정 {d['id']} 이 사람(scientific_owner) 승인 없이 active 다")
        # ⭐ 승인은 **그 시점의 내용**에 묶인다. 승인 뒤 내용을 고치면 지문이 어긋난다.
        if rat.get("state") == "ratified":
            want = rat.get("decision_digest")
            if not want:
                bad.append(f"결정 {d['id']} 이 승인됐는데 decision_digest 가 없다 — "
                           f"승인 뒤 내용을 고쳐도 티가 안 난다")
            elif want != decision_digest(d):
                bad.append(f"결정 {d['id']} 이 **승인 이후에 내용이 바뀌었다** "
                           f"(digest 불일치) — 재승인이 필요하다")
            for f in ("actor_id", "timestamp", "commit"):
                if not rat.get(f):
                    bad.append(f"결정 {d['id']} 의 승인에 {f} 가 없다")
            if rat.get("commit") and len(str(rat["commit"])) != 40:
                bad.append(f"결정 {d['id']} 의 승인 commit 이 40-hex 가 아니다 "
                           f"(짧은 해시 금지)")
    # slot 유일성 — 같은 slot 에 active 가 둘이면 어느 쪽이 이기는지 알 수 없다
    slots = {}
    for d in dec.values():
        if d.get("decision_state") == "active":
            slots.setdefault(d.get("slot"), []).append(d["id"])
    for slot, ids in slots.items():
        if len(ids) > 1:
            bad.append(f"slot '{slot}' 에 active 결정이 {len(ids)}개다: {ids}")

    # ── 판정 원장 ────────────────────────────────────────────────────────
    for a in book.values():
        for ref in a.get("decision_ids", []):
            if ref not in dec:
                bad.append(f"판정 {a['assessment_id']} 이 없는 결정 {ref} 를 가리킨다")
        sup = a.get("supersedes_assessment_id")
        if sup and sup not in book:
            bad.append(f"판정 {a['assessment_id']} 의 supersedes 대상 {sup} 가 없다")
        if a.get("kind") == "correction" and "scope" not in a:
            bad.append(f"정정 {a['assessment_id']} 에 scope 가 없다 — 사유가 다른 항목으로 "
                       f"번지는 것을 막는 필드다 (F10)")
        if a.get("kind") == "gate" and a.get("result") not in GATE_OUTCOMES:
            bad.append(f"판정 {a['assessment_id']} 의 result 가 어휘 밖이다: {a.get('result')!r}")

    # ── canonical entry ↔ 원장 ───────────────────────────────────────────
    if reg is None:
        reg = registry(root=root)
    for e in reg.get("entries", []):
        tag = f"{e.get('metric')}/{e.get('system')}"
        refs = e.get("required_assessment_refs") or []
        if refs and not e.get("blocking_gate"):
            bad.append(f"{tag} 이 게이트 없이 판정을 참조한다")
        missing = [r for r in refs if r not in book]
        if missing:
            bad.append(f"{tag} 이 없는 판정을 참조한다: {missing}")
        elif refs:
            act = [r for r in refs if book[r].get("state") == "active"]
            if len(act) != 1:
                bad.append(f"{tag} 의 active 판정이 {len(act)}개다 (1개여야 한다)")
            for r in refs:
                if book[r].get("claim_ref") != f"value:{tag}":
                    bad.append(f"{tag} 이 다른 claim 의 판정을 참조한다: "
                               f"{r} → {book[r].get('claim_ref')}")
        lin = (e.get("gate_detail") or {}).get("lineage") or {}
        if refs and ("gate_outcome" in lin or "current_assessment" in lin):
            bad.append(f"{tag} 의 claim 안에 판정이 남아 있다 — sidecar 가 단일 원장이다")
        for k, vocab in (("lineage_binding", LINEAGE_BINDING),
                         ("numeric_reproduction", NUMERIC_REPRO)):
            if k in lin and lin[k] not in vocab:
                bad.append(f"{tag} 의 {k} 가 어휘 밖이다: {lin[k]!r} (허용: {vocab})")
        if "lineage_status" in lin:
            bad.append(f"{tag} 이 lineage_status 를 되살렸다 — 재현 가능성과 배선 여부는 "
                       f"독립 축이다 (lineage_binding / numeric_reproduction)")
    return bad


def validate(reg: dict, root=None) -> list:
    """(entry, 문제) 목록. 빈 목록 = 레지스트리가 원자료와 일치한다."""
    bad = []
    for e in reg.get("entries", []):
        # ⚠ live 로드가 이미 원자료를 채택하고 어긋남을 value_drift 에 적어 뒀다면,
        #   아래 수치 대조는 (값을 덮어썼으므로) 통과해 버린다 — 여기서 먼저 잡는다.
        #   이게 없으면 "화면은 새 값을 쓰는데 검사는 통과" 라는 최악의 조합이 된다.
        if e.get("value_drift"):
            d = e["value_drift"]
            bad.append((e, f"원자료가 바뀌었다 — 레지스트리 {d['registry']} vs 원자료 {d['source']}. "
                           f"화면은 원자료를 쓰지만 검토 전까지 순위·레이더에서 빠진다. "
                           f"검토 후 레지스트리 value 를 갱신할 것"))
            continue
        if e.get("resolve_error"):
            bad.append((e, f"원자료를 못 읽었다 — {e['resolve_error']}"))
            continue
        # ★ 값이 원자료와 맞아도 **판정 게이트를 통과 못 했으면 정본이 아니다** (2026-08-07).
        #   LPSOCl MD_Ea 가 정확히 그 경우였다 — 숫자는 db 와 일치하는데 600 K 의
        #   β=0.615 가 Fickian 게이트(0.8–1.2)를 못 넘어 kb/open_items.md 가 인용 보류로
        #   묶어 둔 값이었다. 첫 판에서 이 대조를 빠뜨려 canonical 로 올렸고 Codex 가 잡았다.
        #   → 수치 대조와 **별개 축**으로 검사한다.
        if e.get("status") == "canonical" and gate_blocks_canonical(e):
            _o = gate_outcome(e)
            bad.append((e, f"{_GATE_LABEL.get(_o, _GATE_LABEL[None])}({e['blocking_gate']})인데 "
                           f"status=canonical 이다 — 값이 맞아도 정본이 될 수 없다"
                           + (" (미평가는 통과가 아니다)" if _o == "not_assessed" else "")))
        sp, sk = e.get("source_path"), e.get("source_key")
        if not sp or not sk:
            # 출처가 없어도 되는 상태 = 애초에 "검증되지 않았다"고 화면에 밝히는 상태들.
            # canonical 인데 출처가 없으면 그건 숨은 하드코딩이므로 실패로 잡는다.
            if e.get("status") not in ("source_pending", "provisional", "superseded"):
                bad.append((e, f"status={e.get('status')} 인데 source_path/source_key 가 없다 "
                               f"— 정본은 반드시 원자료를 가리켜야 한다"))
            continue
        try:
            got = resolve(sp, sk, root)
        except ResolveError as ex:
            bad.append((e, f"원자료를 못 따라간다 — {ex}"))
            continue
        tol = float(e.get("tolerance", 5e-4))
        want = e.get("value")
        if want is None or abs(got - float(want)) > tol:
            bad.append((e, f"값 불일치 — 레지스트리 {want} vs 원자료 {got} (허용 ±{tol})"))
    return bad


def entries(reg, metric=None, group=None, status=("canonical",)):
    out = []
    for e in reg.get("entries", []):
        if metric and e.get("metric") != metric:
            continue
        if group and e.get("comparison_group") != group:
            continue
        if status and e.get("status") not in status:
            continue
        out.append(e)
    return out


def canonical_map(reg, metric, group=None, status=("canonical",)) -> dict:
    """{system: value} — 화면이 쓰는 형태.

    ⚠ group 을 안 주면 **그 metric 의 모든 프로토콜이 섞인다.** 표시용으로는 괜찮지만
      순위·최저값·레이더에는 반드시 group 을 지정할 것 (MD_Ea 가 정확히 그 사고를 냈다).
    """
    return {e["system"]: e["value"] for e in entries(reg, metric, group, status)}


def groups_of(reg, metric) -> dict:
    """{comparison_group: [entry...]} — 비교 가능한 묶음을 그대로 돌려준다."""
    g = {}
    for e in entries(reg, metric, status=None):
        g.setdefault(e.get("comparison_group") or "ungrouped", []).append(e)
    return g


def index(reg) -> dict:
    """(metric, system) → entry. 배지·툴팁이 상태/출처를 바로 꺼내 쓰기 위한 색인."""
    return {(e.get("metric"), e.get("system")): e for e in reg.get("entries", [])}
