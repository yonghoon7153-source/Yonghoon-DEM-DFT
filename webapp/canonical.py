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
from html.parser import HTMLParser as _HTMLParser
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

    ⛔⛔ 2026-09-07 — **못 읽는 사유 중 하나만 ResolveError 였다.** "파일 없음" 은
      ResolveError 라 `load_registry` 가 그 항목을 `source_error` 로 내리는데(설계대로),
      **깨진 JSON/CSV** 는 `json.load` 의 JSONDecodeError 가 그대로 올라가
      `/`·`/compare`·`/explorer`·`/governance` 가 통째로 **500** 이었다(실측).
      `float(node)` 가 dict/list 를 만나는 경우도 TypeError 로 샜다.
      load_registry 의 문서가 이미 "원자료를 못 읽으면 status 를 source_error 로
      내린다" 고 적어 놓은 설계인데, 그 경로를 **한 종류만** 타고 있었다.
      ⇒ 못 읽는 사유는 **전부** ResolveError 로 모은다. 판정은 안 바꾼다 —
        source_error 는 여전히 자동판정에서 빠지고 화면에 '출처오류' 배지가 붙는다.
    """
    p = (Path(root) if root else ROOT) / source_path
    if not p.is_file():
        raise ResolveError(f"{source_path}: 파일 없음")
    toks = [t for t in source_key.split("/") if t != ""]
    try:
        if p.suffix.lower() == ".csv":
            # ⚠ 우리 CSV 는 '#' 주석 줄이 섞여 있다(인용 금지 문구가 거기 산다). 걸러내고 읽는다.
            with open(p, encoding="utf-8", errors="ignore") as f:
                rows = [ln for ln in f if not ln.lstrip().startswith(("#", '"#'))]
            node = list(csv.DictReader(rows))
        else:
            with open(p, encoding="utf-8") as f:
                node = json.load(f)
    except (OSError, ValueError, csv.Error) as ex:      # JSONDecodeError ⊂ ValueError
        raise ResolveError(
            f"{source_path}: 원자료를 못 읽었다 ({type(ex).__name__}: {ex})") from ex
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
    try:
        return float(node)
    except (TypeError, ValueError) as ex:
        raise ResolveError(f"{source_path}:{source_key}: 수로 못 바꾼다 "
                           f"({type(node).__name__} {str(node)[:40]!r})") from ex


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


def _by_id(records, key, what, path) -> dict:
    """리스트를 {id: record} 로 바꾸되 **중복 ID 를 조용히 덮지 않는다**.

    ⛔⛔ 회신 AW P0-4 (2026-09-01) — 종전 세 원장이 전부 `{d[key]: d for d in raw}` 였다.
      dict 컴프리헨션은 같은 키가 두 번 나오면 **뒤엣것으로 조용히 덮는다.** 그래서
      *무승인 `active` 기록 뒤에 같은 ID 의 `proposed` 를 하나 더 두면* validator 가
      active 기록 자체를 못 보고 통과한다 — 승인 검사를 우회하는 가장 싼 경로다.
      원장은 append-only 라 이런 중복이 **실수로도** 생긴다(같은 결정을 두 번 등록).

    ⇒ 중복을 만나면 예외를 던진다. "어느 쪽이 맞나" 는 사람이 정할 일이지
      마지막 줄이 이기게 둘 일이 아니다.

    ⛔ 이 함수가 못 하는 것: 두 기록 중 **어느 쪽이 옳은지** 판정하지 않는다.
      충돌이 있다는 사실만 알린다.
    """
    out, dup = {}, {}
    for r in records:
        i = r.get(key)
        if i is None:
            raise RuntimeError(f"⛔ {path} 에 {key} 없는 {what} 기록이 있다 (fail-closed)")
        if i in out:
            dup.setdefault(i, 1)
            dup[i] += 1
        out[i] = r
    if dup:
        detail = ", ".join(f"{i}×{n}" for i, n in sorted(dup.items()))
        raise RuntimeError(
            f"⛔ {path} 에 {what} ID 가 중복이다 ({detail}) — 조용히 덮으면 "
            f"승인·게이트 검사가 앞 기록을 통째로 못 본다. 원장에서 하나로 정리할 것 "
            f"(회신 AW P0-4, fail-closed)")
    return out


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
    return _by_id(raw.get("assessments", []), "assessment_id", "판정", ASSESSMENTS_PATH)


def gate_outcome(e: dict, root=None):
    """canonical entry 의 게이트 판정. 게이트가 없으면 None.

    반환: "not_assessed" | "pass" | "fail" | "inapplicable" | None(게이트 없음)

    우선순위:
      ① required_assessment_refs → sidecar 의 state=active 레코드 (권위)
      ② gate_detail.lineage.gate_outcome (레거시 경로 — 아직 이관 안 된 항목)
      ③ gate_detail.verdict (항목이 **자기 말로** 적어 둔 판정)
      ④ 아무 데도 없으면 fail (보수적)

    ⛔ 2026-08-20 (codex 동결감사) — 판정을 canonical claim 안에 두면 consumer 마다
      '현재 판정' 을 다르게 고를 수 있다. ①이 있으면 ②는 **보지 않는다**.

    ⛔⛔ 2026-09-09 (v3 P0-17) — ③이 없었다. σ 비 3항목은 `gate_detail.verdict` 에
      `not_assessed` 라고 **이미 적혀 있었는데** 기계가 읽는 자리가 lineage 하나뿐이라
      화면이 '게이트 미통과'(fail)로 그렸다. D-2026-08-20-no-retro-gate-without-artifact
      ("미평가는 pending 이 아니다")와 정면으로 어긋난다. 판정 자체는 안 바꾼다 —
      not_assessed 는 여전히 정본을 막는다(`gate_blocks_canonical`). **문구만** 달라진다:
      "평가해 봤더니 떨어졌다" 와 "평가한 적이 없다" 는 다른 말이다.
      ⚠ 그렇다고 ③이 fail-open 은 아니다 — verdict 가 어휘 밖이면 그대로 ④(fail)로 간다.
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
    gd = e.get("gate_detail") or {}
    lin = gd.get("lineage") or {}
    out = lin.get("gate_outcome") or (lin.get("current_assessment") or {}).get("result")
    if out in GATE_OUTCOMES:
        return out
    if gd.get("verdict") in GATE_OUTCOMES:      # ③ 항목이 자기 말로 적어 둔 판정
        return gd["verdict"]
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
#: ⛔ 회신 AW P0-4 — 결정 상태 어휘. **모르는 상태는 검사를 조용히 건너뛰게 한다**
#:   (예: `status: "aktive"` 오타가 active 검사에도 superseded 검사에도 안 걸린다).
DECISION_STATES = frozenset(("proposed", "active", "superseded", "retracted", "rejected"))
NUMERIC_REPRO = ("none", "approximate", "exact")

#: 금지·역사 문맥 표지 — 이 중 하나가 주변에 있으면 그 출현은 **주장이 아니라 금지**다.
#: ⛔ 회신 AW P0-2 (2026-09-05) — 종전엔 이 목록이 시험 파일마다 복사돼 있었다.
#:   표지를 한쪽에만 더하면 같은 문장이 한 화면에선 통과하고 다른 화면에선 걸린다.
#:   철회 서술 검사는 **여러 화면이 같은 어휘를 써야** 의미가 있으므로 여기 하나로 둔다.
PROHIBITION_MARKS = (
    "⛔", "⚠", "금지", "철회", "보류", "않는다", "가 아니다", "이 아니다", "가 아니라",
    "이 아니라", "못 쓴다", "안 쓴다", "못 쓰는", "라 쓰지", "라고 쓰지", "쓸 수 없다",
    "HISTORICAL", "BLOCKED", "SUPERSEDED", "RETRACTED", "미해결", "비인용", "무효",
    "인용 불가", "굽는다", "단일 직선",
)


#: `/sdcp` 마감문서 검사가 쓰는 **좁은** 표지 집합. 위 목록의 **부분집합**이다.
#:
#: ⚠ 왜 두 벌인가 (2026-09-07) — 이건 실수가 아니라 **의도된 비대칭**이다.
#:   검사는 "숫자 주변에 표지가 없으면 그 출현은 **주장**이다" 로 돈다. 그래서
#:   표지가 **적을수록 검사가 엄격**해진다(금지로 봐주는 문맥이 줄어든다).
#:   `/sdcp` 는 마감문서라 제일 엄격해야 하고, 다른 화면은 넓은 목록으로 본다.
#:   ⛔ 둘을 합치지 마라 — 합치면 `/sdcp` 검사가 **느슨해진다.**
#:   ⛔ 여기에 표지를 더하지도 마라 — 더하는 것이 곧 완화다.
#: 종전에는 이 목록이 `tests/test_sdcp_wave1.py` 에 **사본**으로 있었다(회신 AW P0-2 가
#: "여러 화면이 같은 어휘를 써야 의미가 있다" 며 한 곳에 모으라고 한 바로 그 상황).
#: 사본은 없애되 **좁다는 사실은 유지**하려고, 두 목록을 여기 나란히 두고
#: 부분집합 관계를 시험이 지킨다.
PROHIBITION_MARKS_STRICT = (
    "⛔", "금지", "철회", "보류", "않는다", "가 아니다", "이 아니다",
    "못 쓴다", "안 쓴다", "라 쓰지", "라고 쓰지",
    "HISTORICAL", "BLOCKED", "SUPERSEDED", "미해결", "비인용",
)


def is_prohibition_context(ctx: str) -> bool:
    """문맥에 금지·역사 표지가 있나. 없으면 그 출현은 **주장으로 읽힌다**.

    ⛔ 이 함수가 못 하는 것
      · 표지가 **그 값에 대한** 것인지는 못 본다. 옆 문장의 ⚠ 도 표지로 센다 —
        느슨한 쪽이 맞다(올바른 글을 지우는 실수가 더 비싸다). 정밀도는 창 폭으로 조절한다.
      · 표지가 없다고 그 문장이 **틀렸다**는 뜻은 아니다. "결속이 없다" 는 뜻이다.
    """
    return any(m in ctx for m in PROHIBITION_MARKS)


# ══════════════════════════════════════════════════════════════════════════
# claim ID 결속 (2026-09-08 · 회신 BG ② — ±140자 근접성 폐기)
#   ⛔⛔ 왜 바꾸나
#     종전 결속 검사는 "철회값 근처 140자 안에 ⛔ 같은 표지가 있나" 였다. 세 가지가 틀렸다:
#       ① 표지가 **그 값에 대한 것인지** 못 본다 — 옆 문단의 경고도 통과시킨다.
#       ② 표 안에서는 셀이 길어 표지가 창 밖으로 밀린다 (실측: /governance 인용위험 표의
#          `Ea … 0.199±0.034` 행이 스스로 위험 경고인데도 **미결속**으로 잡혔다).
#       ③ 검사 대상 화면이 **손 목록**이었다 — 목록에 없는 화면은 아무리 틀려도 안 잡힌다.
#     ⇒ 결속을 **구조**로 바꾼다. 값을 그리는 요소(또는 그 조상)가 `data-claim="<id>"` 로
#       **어느 주장인지 이름을 대야** 한다. 이름이 맞으면 근접성은 보지 않는다.
#
#   claim id = "<metric>@<system>" — 레지스트리에서 파생하므로 별도 목록이 없다.
#
#   ⛔ 이 결속이 못 하는 것
#     · 그 요소의 **글이 맞는지**는 안 본다. "이 값이 어느 주장인지 선언했나" 만 본다.
#     · 선언이 거짓일 수 있다 (아무 값에나 data-claim 을 붙이는 것). 그건 레지스트리 대조
#       (`scan_claim_bindings` 의 `dangling`)로 잡되, 사람의 성실성을 대체하지는 않는다.
def claim_id(metric, system) -> str:
    """화면 결속에 쓰는 주장 식별자. 레지스트리 (metric, system) 한 쌍이 곧 id 다."""
    return f"{metric}@{system}"


def bound_claims(reg=None, root=None) -> list:
    """화면에서 **이름을 대야 하는** 주장들 — 철회 + 비인용(citable:false).

    반환 `[{"id","metric","system","state","text","why","instead"}]`.
      · `state` — "retracted" | "non_citable"
      · `text`  — 화면에서 찾을 숫자열. 숫자 정본값이 없으면 `None` (id 만 검증한다).

    ⚠ `text` 는 **네 글자 이상**일 때만 넣는다. "1.08" 같은 짧은 수를 전 화면에서 찾으면
      무관한 표(원자수·비율)에 걸려 검사가 소음이 된다 — 그때는 결속을 강제하지 못하고
      id 유효성만 본다. σ 비 3항목이 그 경우다 (`_ratio_display` 는 스캔에 쓰지 않는다).
    """
    reg = reg if reg is not None else registry(root=root)
    out = []
    for e in reg.get("entries", []):
        st = e.get("status")
        state = ("retracted" if st == "retracted"
                 else ("non_citable" if e.get("citable") is False else None))
        if state is None:
            continue
        v = e.get("value")
        txt = f"{float(v):g}" if v is not None else None
        if txt is not None and len(txt) < 4:
            txt = None
        r = e.get("retracted") or {}
        out.append({"id": claim_id(e.get("metric"), e.get("system")),
                    "metric": e.get("metric"), "system": e.get("system"),
                    "state": state, "text": txt,
                    # 매처 조건 (Codex BI ③) — 숫자는 값으로, 단위·계 이름은 문맥으로
                    "kind": "number" if txt else None,
                    "unit": e.get("unit"), "system_tokens": system_tokens(e.get("system")),
                    "why": r.get("why", "") or e.get("why_non_citable", ""),
                    "instead": r.get("usable_instead", "")})
    return out


def noncitable_metrics(reg=None, root=None) -> dict:
    """**축 전체가 비인용**인 metric → `{"why", "systems", "group", "allowed"}`.

    왜 필요한가 (v3 묶음 C · 2026-09-09) — `/explorer` 가 σ 비 3열을 14행 전부
    `TODO` 로 그렸다. 값이 없는 게 아니라 **원자료가 인용을 금지**한 축인데,
    "아직 안 했다"(TODO)와 "했는데 못 쓴다"(비인용)를 같은 기호로 쓰면 화면이
    거짓말을 한다. 그래서 이런 축은 본 표에서 빼고 사유와 함께 따로 보인다.

    판정: 그 metric 의 레지스트리 항목이 **전부** `citable is False` 일 때만 든다.
      하나라도 인용 가능한 항목이 있으면 축을 통째로 접으면 안 된다 (그 값이 사라진다).

    ⛔ 못 하는 것
      · 언제 인용 가능해지는지 말하지 않는다. 지금 원장이 금지했다는 사실만 낸다.
      · 개별 칸의 금지(`bound_claims`)를 대신하지 않는다 — 이건 **열** 단위 판정이다.
      · `status=retracted` 는 여기 안 든다. 철회는 값이 있었던 것이고, 화면에서
        취소선·결속으로 보여야 한다(숨기면 이력이 사라진다).
    """
    reg = reg if reg is not None else registry(root=root)
    by: dict = {}
    for e in reg.get("entries", []):
        m = e.get("metric")
        if not m:
            continue
        by.setdefault(m, []).append(e)
    out = {}
    for m, es in by.items():
        if not all(e.get("citable") is False for e in es):
            continue
        why = next((e.get("why_non_citable") for e in es if e.get("why_non_citable")), "")
        out[m] = {"why": str(why),
                  "systems": sorted({str(e.get("system")) for e in es}),
                  "group": next((e.get("comparison_group") for e in es
                                 if e.get("comparison_group")), None),
                  "allowed": next((e.get("allowed_sentence") for e in es
                                   if e.get("allowed_sentence")), ""),
                  "gate": next((e.get("blocking_gate") for e in es
                                if e.get("blocking_gate")), None),
                  "gate_outcome": next((gate_outcome(e) for e in es
                                        if e.get("blocking_gate")), None)}
    return out


#: 계 이름의 표기 변이 — 남의 논문과 우리 값을 가르는 **문맥 조건**에 쓴다.
#: ⚠ 손으로 늘리기보다 계 이름에서 파생시킨다. 여기 적는 것은 파생으로 안 나오는 별칭뿐.
_SYS_ALIAS = {
    "b2o3": ("b2o3", "b₂o₃", "b2o3-lpscl", "b₂o₃-lpscl", "b2o3-도핑"),
    "modelc": ("modelc", "model c", "lpscl1.6", "lpscl 1.6"),
    "comp1": ("comp1", "li6ps5cl"),
    "lpsocl": ("lpsocl", "lpso cl", "o 도핑"),
    "b2o3_vs_modelc": ("b2o3", "b₂o₃", "modelc", "lpscl1.6"),
}


def system_tokens(system) -> tuple:
    """그 계를 가리키는 소문자 토큰들 — `origin="external"` 문맥 조건용."""
    s = str(system or "").strip().lower()
    if not s:
        return ()
    base = {s, s.replace("_", " "), s.replace("_", "-")}
    return tuple(sorted(base | set(_SYS_ALIAS.get(s, ()))))


_HZ_CACHE = {"key": None, "out": None}

#: 인용위험 원장의 `level` 어휘 — 전수(2026-09-08 실측 25행: CONDITIONAL 12 · BLOCKED 5 ·
#: RESOLVED 2 · HOLD 2 · STALE 2 · SUPERSEDED 1 · PREVIEW 1). 여기 없는 값은 UNKNOWN 이다.
HAZARD_LEVELS = ("BLOCKED", "CONDITIONAL", "HOLD", "PREVIEW", "STALE",
                 "SUPERSEDED", "RESOLVED")
#: ⛔⛔ **`level` 은 규칙의 상태지 금지의 상태가 아니다** (Codex BI-3, 2026-09-09).
#:
#: 2026-09-08 에 `HAZARD_INACTIVE = {"RESOLVED", "SUPERSEDED"}` 를 두고 `hazard_claims()`
#: 에서 걸렀다. **그게 틀렸다.** `HZ-beta-hard-gate` 의 `what` 은
#: *"β ≥ 0.80 하드게이트 — **판정으로 인용 금지**"* 다. 폐기된 것은 **통과·탈락 규칙**이고,
#: *"그 규칙을 지금 판정에 쓰지 마라"* 는 **금지는 그대로 살아 있다** — 규칙이 죽었으니
#: 오히려 더 살아 있다. 그런데 나는 그것을 끄고 `binding_scope_why` 에
#: *"집행되지 않는다"* 라고 **정당화까지 적었다.** 실측: 화면에
#: "판정은 β ≥ 0.80 하드게이트를 통과하면 된다" 를 넣으면 탐지·미결속·suspect 가 전부 0.
#:
#: 그래서 두 축을 **분리**한다:
#:   · `level`              = **규칙 상태** (rule_state) — 그 판정·문턱이 아직 유효한가
#:   · `prohibition_state`  = **금지 상태** — 그 문구를 지금 인용하면 안 되는가
#: 기본값은 **fail-closed**: 명시가 없으면 `RESOLVED` 만 금지가 꺼지고 나머지는 **켜진다**.
#: (`SUPERSEDED`·`STALE`·`PREVIEW`·`HOLD`·어휘 밖 오타 전부 살아 있는 금지로 친다.)
#:
#: 이력·반증 목적의 언급은 금지를 끄는 것이 아니라 **화면이 용도를 선언**해서 다룬다
#: — `data-claim` + `data-claim-use="historical"|"refutation"` (아래 `USE_MODES`).
#: ⚠ **표시 전용.** "그 규칙·판정이 더는 유효하지 않다" 를 화면이 세는 데만 쓴다
#:   (`/governance` 의 '살아있는 위험 N건', nav 배지 등). **집행에 쓰지 마라** —
#:   집행은 `prohibition_active()` 다. 이 둘을 같은 것으로 본 게 BI-3 P0-1 이다.
HAZARD_INACTIVE = frozenset(("RESOLVED", "SUPERSEDED"))
PROHIBITION_STATES = ("active", "inactive")
#: 명시 없을 때 금지가 꺼지는 유일한 level. 나머지는 전부 켜진다.
_PROHIBITION_OFF_BY_DEFAULT = frozenset(("RESOLVED",))
#: 결속된 자리가 **어떤 용도**로 그 문구를 쓰는가. 기본은 `citation`(=금지 대상).
USE_MODES = ("citation", "historical", "refutation")


def prohibition_active(row: dict) -> bool:
    """이 위험 행의 **금지**가 지금 살아 있는가 — `level` 이 아니라 이걸 본다.

    · 행이 `prohibition_state` 를 명시하면 그것이 이긴다 (어휘 밖 값은 **active**).
    · 없으면 `level == "RESOLVED"` 일 때만 꺼지고, 나머지는 전부 켜진다.
    ⛔ 못 하는 것: 금지가 **정당한가**는 안 본다. 원장이 그렇게 말하는지만 본다.
    """
    raw = row.get("prohibition_state")
    if raw is not None and str(raw).strip():
        ps = str(raw).strip().lower()
        # ⚠ 어휘 밖 값은 **active** 다 — 오타 하나로 금지가 사라지면 안 된다.
        return ps != "inactive"
    return str(row.get("level", "")).upper() not in _PROHIBITION_OFF_BY_DEFAULT


def _hazard_rows(root=None) -> list:
    """citation_hazards.json 의 hazards 배열 (mtime 캐시). 못 읽으면 빈 목록."""
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    f = base / "db/properties/citation_hazards.json"
    if not f.exists():
        return []
    k = (str(f), f.stat().st_mtime_ns)
    if _HZ_CACHE["key"] == k:
        return _HZ_CACHE["out"]
    try:
        hz = json.loads(f.read_text(encoding="utf-8"))
    except Exception:                                   # noqa: BLE001
        return []
    out = list(hz.get("hazards") or [])
    _HZ_CACHE.update(key=k, out=out)
    return out


def hazard_ids(root=None) -> set:
    """**결속 어휘** — 원장에 있는 hazard id 전부 (level 무관).

    `hazard_claims()`(=결속 *요구*)와 갈라 둔다. 해소·폐기된 위험도 화면이 이력으로
    이름을 댈 수 있어야 하고, 그때 유령 결속(dangling)으로 터지면 안 된다.
    """
    return {z.get("id") for z in _hazard_rows(root=root) if z.get("id")}


def hazard_claims(root=None) -> list:
    """인용 위험 원장에서 **비수치 주장**의 결속 대상을 만든다 (회신 BG ② · 2026-09-08).

    숫자 결속(`bound_claims`)은 canonical_registry 의 수치만 본다. 그래서 산문으로 된
    금지 주장 — 계간 Ea `+90 meV` 비교, 폐기된 β 0.80 하드게이트 — 을 못 잡는다.
    원장의 `forbidden_phrases` 를 claim 으로 바꿔 같은 스캐너에 태운다.

    반환: `[{"id","metric","system","state","text","why","instead"}]` (bound_claims 와 같은 모양).
    ⛔ 못 하는 것: 문구가 **그 위험을 뜻하는지**는 못 본다. 문자열이 있으면 결속을 요구할 뿐이다.
      그래서 `forbidden_phrases` 는 **구체적**이어야 한다 — 흔한 낱말을 넣으면 오탐이 된다.
    ⛔ 또 못 하는 것: level 어휘가 `HAZARD_LEVELS` 밖이면 **살아있는 것으로 친다**(fail-closed).
      조용히 건너뛰면 오타 하나로 금지가 사라진다.
    """
    out = []
    for z in _hazard_rows(root=root):
        hid, ph = z.get("id"), (z.get("forbidden_phrases") or [])
        # ⛔ `level` 로 거르지 않는다 — 규칙이 폐기돼도 금지는 살아 있을 수 있다.
        #    (Codex BI-3: SUPERSEDED 를 걸렀다가 폐기된 β 게이트의 '사용 금지' 까지 껐다.)
        if not hid or not prohibition_active(z):
            continue
        # ⚠ 금지 문구가 없어도 **id 는 낸다** (`text=None`). 그래야 화면이 그 위험을
        #   선언했을 때 유령 결속(dangling)으로 잡히지 않는다 — bound_claims 의 짧은 수와 같은 처리.
        for t in (ph or [None]):
            out.append({"id": hid, "metric": hid, "system": "hazard",
                        "state": "hazard_" + str(z.get("level", "")).lower(),
                        "text": t, "kind": "phrase", "unit": None,
                        # 위험 행이 어느 계를 말하는지 — `claim` 이 있으면 거기서 딴다
                        "system_tokens": system_tokens(
                            str(z.get("claim") or "").split("@")[-1] or None),
                        "why": z.get("why", ""),
                        "instead": z.get("fix", "")})
    return out


#: 축 단위 금지가 취하는 꼴 (Codex BI-4 Q5 · 2026-09-09).
#:   `{"system": …, "method": …, "quantity_group": [...], "use": [...]}`
#: ⛔ 왜 필요한가: 금지는 **양의 종류**로 선언되는데 스캐너는 `(metric, system)` 쌍만 안다.
#:   실측 — `HZ-b2o3-md-ea` 가 *"D · Ea · σ · 구간 Ea 전부 인용 불가"* 인데
#:   `binding_scope_why` 자신이 *"같은 축의 D·σ·구간 Ea 는 **레지스트리에 없어 안 덮인다**"*
#:   라고 적어 두었다. 어휘 밖 표기(`0.2241`)가 걸어 나간 것도 같은 구멍이다.
#: ⚠ 그래서 축은 **claim 을 대신하지 않는다** — claim 위에 얹혀 **상속**시킨다.
AXIS_KEYS = ("system", "method", "quantity_group", "use")


def _axis_tokens(cid: str) -> dict:
    """claim id `MD_Ea_eV@b2o3` → `{"system": "b2o3", "method": "MD", "quantity": {...}}`.

    ⛔ 못 하는 것: id 규약(`{metric}@{system}`)에 의존한다. 규약이 바뀌면 여기가 먼저 깨진다.
      그래서 아래 `validate_hazards` H5 가 **축이 실제로 무엇을 덮는지 세어** 0이면 잡는다.
    """
    metric, _, system = str(cid or "").partition("@")
    parts = [p for p in metric.split("_") if p]
    return {"system": system.lower(),
            "method": (parts[0] if parts else "").upper(),
            # 남은 토큰 전부를 양 이름 후보로 본다 (Ea · sigma · D · ratio · singleseed …)
            "quantity": {p.lower() for p in parts[1:]} | {metric.lower()}}


def axis_covers(cid: str, axis: dict) -> bool:
    """이 claim id 가 그 금지 축 **안**인가.

    셋을 **모두** 만족해야 한다 — 계 · 방법 · 보고량군. 하나라도 어긋나면 밖이다.
    (`use` 는 소비 시점 조건이라 여기서 안 본다 — 소비자가 본다.)
    """
    t = _axis_tokens(cid)
    sysd = str(axis.get("system", "")).lower()
    if not sysd or sysd not in t["system"]:
        return False
    meth = str(axis.get("method", "")).upper().replace("-", "_")
    # `UMA-MD` · `MD` 둘 다 claim 접두 `MD` 와 맞아야 한다
    if meth and not any(m and m == t["method"] for m in meth.split("_")):
        return False
    qs = {str(q).lower() for q in (axis.get("quantity_group") or [])}
    return bool(qs & t["quantity"]) if qs else False


def axis_prohibitions(root=None) -> list:
    """살아있는 **축 단위 금지** 목록 → `[{axis, id, level, why, fix, decision}]`."""
    out = []
    for z in _hazard_rows(root=root):
        ax = z.get("prohibition_axis")
        if not isinstance(ax, dict) or not prohibition_active(z):
            continue
        out.append({"axis": ax, "id": z.get("id"), "level": z.get("level"),
                    "why": z.get("why", ""), "fix": z.get("fix", ""),
                    "decision": z.get("decision")})
    return out


def axis_blocked(cid: str, root=None, axes=None) -> list:
    """이 claim 을 덮는 축 금지들 → `[{id, axis, why, fix}]` (빈 목록 = 축 밖).

    **claim 이 레지스트리에 없어도 판정된다** — 그게 축을 넣은 이유다.
    """
    return [a for a in (axes if axes is not None else axis_prohibitions(root=root))
            if axis_covers(cid, a["axis"])]


def all_claims(reg=None, root=None) -> list:
    """결속을 요구하는 주장 **전부** — 수치(레지스트리) + 비수치(인용위험 원장).

    화면 검사는 이 목록을 기준으로 한다. 둘을 따로 부르면 한쪽을 빠뜨린 채 초록이 뜬다
    (BG ② 실측: 숫자만 보던 검사가 `+90 meV` 계간 비교를 여덟 화면에서 놓쳤다).
    """
    return bound_claims(reg=reg, root=root) + hazard_claims(root=root)


# ── 마크다운 조각의 자동 결속 (회신 BG ② · 2026-09-08) ────────────────────────
#   kb 산문(`/todo`·`/requests`·저널)은 손으로 `data-claim` 을 달 수 없다 — 원문이
#   마크다운이고, 거기에 HTML 을 심으면 원장이 화면 형식에 오염된다. 그래서 **렌더할 때**
#   결속 대상 문자열을 찾아 그 자리를 감싼다.
#
#   ⚠ 자동 결속이 정직하려면 **눈에 보여야** 한다. 속성만 붙이면 검사만 초록이 되고
#     읽는 사람은 여전히 철회값을 그냥 읽는다 — 그건 결속이 아니라 도장이다.
#     그래서 `.claim-flag` 는 CSS 로 밑줄 + ⛔ 를 그리고 title 에 사유를 싣는다.
_TAG_SPLIT = re.compile(r"(<[^>]*>)")
_STATE_MARK = {"retracted": "⛔ 철회 — 인용 금지",
               "non_citable": "⛔ 비인용 — 정본으로 옮기지 않는다"}

# ── 매처 (Codex BI ③ · 2026-09-08) ──────────────────────────────────────────
#   실측 두 방향의 오차가 같이 있었다.
#   · 오탐 — litdb 219편 자동결속 18건 중 **17이 남의 논문**이다
#     (deng2026 H₂O 흡착 −0.199 eV 7 · spencer2022 exciton 50–90 meV 3 · …).
#   · 미탐 — 문자열 그대로 찾으니 `0.1990` 한 자리로 결속을 **벗어난다**
#     (`<td>0.199</td>` unbound 1 vs `<td>0.1990</td>` unbound 0, 스캐너 직접 투입).
#   ⇒ 숫자는 **문자열이 아니라 값**으로 본다. 부호·단위·출처를 조건으로 건다.
#
# ⛔⛔ 이 매처가 **못 잡는 것** (Codex BI-4 P1, 2026-09-09 — 실측)
#   종전 회신은 *"`.199` 도 잡는다"* 고 적었다. **철회한다. 재현되지 않는다.**
#   스캐너에 직접 넣어 잰 결과:
#       `0.199` ✅ 1건 · `1.99e-1` ✅ 1건 · `0.1990` ✅ 1건
#       `.199`  ⛔ 0건 — 정수부가 없으면 `_NUM_TOKEN` 이 `\d+` 를 요구해 안 걸린다
#       `199 meV` ⛔ 0건 — **단위 환산을 안 한다** (eV↔meV)
#       `0.<em>199</em>` ⛔ 0건 — 태그로 갈리면 `handle_data` 조각이 나뉜다
#   ⚠ **정규식을 키워서 쫓지 않는다.** 표기의 가짓수는 끝이 없고, 하나 늘릴 때마다
#     오탐이 같이 는다(§3-1 에서 우리가 자백한 "분모 부풀리기"가 그 길이다).
#     닫는 방향은 **축 단위 금지 상속**이다 — 값 하나하나를 문자열로 쫓는 대신
#     `(대상계 · 방법 · 보고량군 · 용도)` 로 금지를 선언하고 소비자가 그것을 상속한다.
#     아직 안 했다. **그래서 이 셋은 지금 새는 구멍이고, 여기 적어 둔다.**
_NUM_TOKEN = re.compile(r"[-−–+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
#: 값 바로 뒤의 단위 토큰 (`±0.034 eV` 처럼 오차막대를 건너뛴다)
_UNIT_AFTER = re.compile(r"\s*(?:[±+]/?-?\s*[\d.]+\s*)?([A-Za-zμµΩ%]+(?:/[A-Za-z³]+)?)")


def _num_of(tok: str):
    """`−0.199` · `+0.1990` → float. 못 읽으면 None."""
    try:
        return float(tok.replace("−", "-").replace("–", "-").lstrip("+"))
    except ValueError:
        return None


#: 단위로 **인정하는** 낱말. ⚠ 여기 없는 낱말은 "다른 단위" 가 아니라 **단위가 아니다**.
#:   실측 사고: `Ea 0.199±0.034 vs 0.197±0.032` 에서 `vs` 를 단위로 읽어 진성 인용
#:   한 건을 suspect 로 떨어뜨렸다. 모르는 낱말을 증거로 쓰면 안 된다.
UNIT_WORDS = frozenset((
    "ev", "mev", "kev", "ry", "ha", "kj", "kcal", "j", "k", "c",
    "a", "å", "nm", "pm", "cm", "m", "mm", "s", "ps", "fs", "ns", "ms",
    "gpa", "mpa", "pa", "bar", "v", "mv", "e", "μb", "µb", "ub",
    "s/cm", "ms/cm", "mscm", "cm2/s", "cm²/s", "g/cm3", "g/cm³", "%",
    "mev/atom", "ev/atom", "ev/å", "mev/å", "ω", "ωcm",
))


def _unit_conflict(claim: dict, seg: str, end: int) -> bool:
    """값 뒤의 단위가 정본 단위와 **다르면** True (같거나·단위가 아니면 False).

    ⛔ 못 하는 것: 단위가 같은 다른 물리량은 못 가른다 — `E_ads = −0.199 eV` 와
      `Ea = 0.199 eV` 는 단위까지 같다. 그건 부호·출처 조건이 맡는다.
    """
    u = (claim.get("unit") or "").strip()
    if not u:
        return False
    m = _UNIT_AFTER.match(seg, end)
    if not m:
        return False
    got = m.group(1)
    if got.lower() not in UNIT_WORDS:        # 모르는 낱말 = 단위가 아니다 (증거 아님)
        return False
    return got != u and got.lower() != u.lower()


def qualify_hit(claim: dict, seg: str, start: int, end: int, origin: str = "internal",
                before: str = "") -> str:
    """이 자리의 일치가 **얼마나 그 주장인가** → "match" | "suspect".

    · `suspect` — 문자열은 같지만 그 주장이라고 보기 어렵다. 결속을 요구하지 않고
      **목록으로만** 남긴다(침묵이 아니다). 판정 근거 셋:
        ① 부호가 다르다 (`−0.199` 은 `0.199` 이 아니다)
        ② 값 뒤 단위가 정본 단위와 다르다
        ③ 출처가 외부 문서인데(`origin="external"`) 우리 계 이름이 근처에 없다
    ⛔ 못 하는 것: 문장의 뜻은 안 본다. 세 조건 다 지나가면 `match` 다.
    """
    tok = seg[start:end]
    if claim.get("kind") == "number":
        if tok.lstrip("+").startswith(("-", "−", "–")):
            return "suspect"                                   # ① 부호
        if _unit_conflict(claim, seg, end):
            return "suspect"                                   # ② 단위
    if origin == "external":                                   # ③ 출처
        # ⚠ 창은 **태그 경계를 넘어서** 잡는다. 렌더된 HTML 은 `**동등**` 같은 강조에서
        #   텍스트 노드가 잘려서, 노드 안만 보면 바로 앞 문장의 계 이름을 못 본다
        #   (실측: fan2026 의 진성 인용 1건이 그 때문에 suspect 로 떨어졌다).
        win = (before[-CTX_BEFORE:] + seg[:start]).lower()[-CTX_BEFORE:] \
            + seg[start:end + CTX_AFTER].lower()
        toks = claim.get("system_tokens") or ()
        if not any(t in win for t in toks):
            return "suspect"
    return "match"


#: 출처 조건의 문맥 창 — 앞 240자 / 뒤 90자. 앞을 넓게 잡는 이유: 인용문은 계 이름을
#: **먼저** 대고 값을 뒤에 쓴다("b2o3/modelc … Ea 0.199±0.034").
CTX_BEFORE, CTX_AFTER = 240, 90


def find_claim_hits(seg: str, claims, origin: str = "internal", before: str = ""):
    """텍스트 한 토막에서 결속 대상 자리를 찾는다 → `[(start, end, claim, quality)]`.

    `annotate_claims`(감싸기)와 `_ClaimScanner`(검사)가 **같은 함수**를 쓴다.
    둘이 갈리면 화면과 검사가 다른 것을 보게 된다.

    숫자 주장은 **값으로** 비교한다 — `0.199` 과 `0.1990` 은 같은 수다.
    ⛔ 종전 문자열 매칭은 `0.1990` 을 놓쳤고, 그건 *"자릿수 하나로 결속을 벗어난다"* 는
      뜻이었다 (Codex BI 재현 중 발견 — 리뷰가 못 짚은 회피면).
    """
    nums = [c for c in claims if c.get("kind") == "number"]
    phrases = sorted([c for c in claims if c.get("kind") != "number"],
                     key=lambda c: len(c.get("text") or ""), reverse=True)
    hits = []
    if nums:
        want = {}
        for c in nums:
            v = _num_of(c["text"])
            if v is not None:
                want.setdefault(round(v, 12), []).append(c)
        for m in _NUM_TOKEN.finditer(seg):
            v = _num_of(m.group(0))
            if v is None:
                continue
            for c in want.get(round(abs(v), 12), ()):
                hits.append((m.start(), m.end(), c,
                             qualify_hit(c, seg, m.start(), m.end(), origin, before)))
    for c in phrases:
        t = c.get("text")
        if not t:
            continue
        i = seg.find(t)
        while i != -1:
            hits.append((i, i + len(t), c,
                         qualify_hit(c, seg, i, i + len(t), origin, before)))
            i = seg.find(t, i + len(t))
    # 겹치는 자리는 **긴 쪽**만 남긴다 ("+90 meV" 가 "90 meV" 를 먹는다)
    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    out, cut = [], -1
    for h in hits:
        if h[0] >= cut:
            out.append(h)
            cut = h[1]
    return out


def instead_text(instead) -> str:
    """대체값 선언을 **화면 문장**으로. sentinel 이면 "대체값 없음" 이라고 말한다.

    ⛔ 종전에는 자유 문자열만 상정해서 `.strip()` 을 바로 불렀다. sentinel(dict)이 오면
      터지고, 무엇보다 *"대체값이 없다"* 를 화면이 **말할 방법이 없었다** — 그래서
      원장이 금지된 값을 대체값 자리에 넣고 있었다 (Codex BI P0-1 · 2026-09-08).
    """
    if isinstance(instead, dict):
        if instead.get("none") is True:
            d = instead.get("decision") or "미상"
            return f"대체값 없음 — 이 축에서 인용 가능한 수는 0개다 ({d})"
        return ""
    return (instead or "").strip()


#: `**강조**` 표기 (짝이 맞는 것만 — 홀로 선 `*` 는 건드리지 않는다).
_UNBOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)


def plain_text(s) -> str:
    """`**강조**` 의 **표식만 떼고** 글자는 그대로 둔다 — `title=` 속성용.

    ⛔ 왜 필요한가: HTML **속성값에는 태그가 안 먹는다.** 툴팁에 `|bold` 를 걸면 `<b>` 가
      글자로 뜨고, 아무것도 안 걸면 별표가 뜬다. 둘 다 깨진 화면이다. 실측 2026-09-15:
      9개 화면에서 툴팁 **100개**가 별표를 달고 있었다.
      원장 산문에 `**` 가 흔해서(citation_hazards 의 `binding_scope_why` 33건 중 14건)
      이 자리를 한 곳으로 모은다 — 화면마다 `replace('**','')` 를 따로 쓰면 갈라진다.

    ⛔ 못 하는 것: 마크다운을 렌더하지 않는다. `*기울임*`·백틱·링크는 글자 그대로 남는다.
      이스케이프도 안 한다 — 부르는 쪽이 한다.
    """
    if s is None:
        return ""
    return _UNBOLD_RE.sub(r"\1", str(s))


def _claim_flag(c: dict, text: str) -> str:
    from html import escape as _e
    _ins = instead_text(c.get("instead"))
    # ⚠ 툴팁은 **속성값**이라 태그가 안 먹는다 — `**` 를 떼고 글자만 넣는다(plain_text).
    #   2026-09-15 실측: 이 자리에서만 /requests 20개 · /todo 3개 툴팁이 별표를 달고 있었다.
    tip = " · ".join(x for x in (_STATE_MARK.get(c.get("state"), "⛔ 인용 위험"),
                                 plain_text(c.get("why")).strip(),
                                 ("대신: " + plain_text(_ins)) if _ins else "")
                     if x)
    # 잘렸으면 **잘렸다고 말한다** — 인용 경고를 표식 없이 자르면 그게 전문으로 읽힌다.
    tip = tip if len(tip) <= 300 else tip[:299] + "…"
    # ⚠ 표식은 **텍스트로도** 남아야 한다 — Codex BI Q3. ⛔ 를 CSS `::after` 로만 그리면
    #   복사·인쇄·텍스트추출·보조기기에서 경고가 사라지고 철회값만 따라간다.
    return (f'<span class="claim-flag" data-claim="{_e(str(c["id"]), True)}"'
            f' title="{_e(tip, True)}">{text}'
            f'<span class="claim-mark">[{_e(_claim_mark_text(c))}]</span></span>')


#: 표식의 **본문** — CSS 가 없어도, 텍스트만 뽑아도 남는 말. 짧아야 문장이 안 깨진다.
_MARK_TEXT = {"retracted": "⛔철회·인용금지", "non_citable": "⛔비인용"}


def _claim_mark_text(c: dict) -> str:
    st = str(c.get("state") or "")
    if st in _MARK_TEXT:
        return _MARK_TEXT[st]
    if st.startswith("hazard_"):
        return "⛔인용위험"
    return "⛔인용위험"


def annotate_claims(fragment: str, claims=None, reg=None, root=None, origin="internal"):
    """마크다운으로 렌더된 **조각**에서 결속 대상 자리를 찾아 그 자리에 이름을 붙인다.

    → `(html, [결속한 claim id …])`

    `origin="external"` 이면 남의 문서다(litdb digest 등) — 우리 계 이름이 근처에 없는
    일치는 `suspect` 로 보고 **감싸지 않는다**. 실측: litdb 219편 자동결속 18건 중 17이
    남의 논문이었다(deng2026 H₂O 흡착 −0.199 eV 7건 등). 오탐이 분모를 부풀리면
    "미결속 0" 이 더 그럴듯하게 틀린 수가 된다.

    ⛔ 이 함수가 **못 하는 것**
      · 문장을 읽지 않는다. 조건(값·부호·단위·계 이름)이 맞으면 감싼다 — 그 문맥이
        정당한 인용인지(역사 기록·반례 인용)는 **사람이** 판단할 몫이다.
      · **완전한 HTML 문서에 쓰면 안 된다.** 태그 밖 텍스트만 건드리도록 태그 단위로
        쪼개는데, `<script>`·`<style>`·주석 안의 `>텍스트<` 는 구분하지 못한다.
      · `<pre><code>` 안은 건드리지 않는다 — 코드·로그의 숫자는 인용이 아니다.
      · 이미 붙은 결속을 지우거나 겹쳐 감싸지 않는다.
    """
    claims = claims if claims is not None else all_claims(reg=reg, root=root)
    usable = [c for c in claims
              if c.get("text") and not any(ch in c["text"] for ch in "<>&")]
    if not usable or not fragment:
        return fragment, []
    found, ctx = [], ""                           # ctx = 태그 밖 텍스트의 러닝 버퍼
    parts = _TAG_SPLIT.split(fragment)
    depth = 0                                     # <pre> 안에서는 감싸지 않는다
    for k, part in enumerate(parts):
        if k % 2:                                 # 홀수 = 태그
            t = part[1:].strip().split()[0].lower().rstrip(">/") if len(part) > 2 else ""
            if t == "pre":
                depth += 1
            elif t == "/pre":
                depth = max(0, depth - 1)
            continue
        if not part.strip():
            continue
        prev, ctx = ctx, (ctx + part)[-CTX_BEFORE:]
        if depth:
            continue
        hits = [h for h in find_claim_hits(part, usable, origin, prev) if h[3] == "match"]
        if not hits:
            continue
        out, i = [], 0
        for a, b, c, _q in hits:
            out.append(part[i:a])
            out.append(_claim_flag(c, part[a:b]))
            found.append(c["id"])
            i = b
        out.append(part[i:])
        parts[k] = "".join(out)
    return "".join(parts), sorted(set(found))


class _ClaimScanner(_HTMLParser):
    """`data-claim` 조상을 추적하며 텍스트 노드를 훑는다 (stdlib 만 쓴다)."""

    #: 닫는 태그가 없는 요소 — 스택에 쌓으면 균형이 깨진다.
    VOID = frozenset(("area", "base", "br", "col", "embed", "hr", "img", "input",
                      "link", "meta", "param", "source", "track", "wbr"))
    SKIP = frozenset(("script", "style"))

    #: 결속을 요구하지 않는 곳 — **코드블록**(`<pre>`)의 숫자는 인용이 아니다.
    #: ⚠ 인라인 `<code>` 는 **넣지 않는다.** 실측: 대시보드가 값을 강조하는 데
    #:   `<code class="mono">Ea 0.199±0.034</code>` 로 쓴다 — 그건 코드가 아니라 값이다.
    #:   여기 code 를 넣었더니 `/` 표면이 통째로 눈이 멀었다(bound 0).
    CODE = frozenset(("pre",))

    def __init__(self, claims, origin="internal"):
        super().__init__(convert_charrefs=True)
        self._claims = claims          # [claim, ...] — 매처가 값·부호·단위를 본다
        self._origin = origin
        self._stack = []               # [(tag, claim_id|None, not_id|None)]
        self._skip = 0
        self._code = 0
        self._ctx = ""                 # 태그 밖 텍스트의 러닝 버퍼 (출처 조건의 문맥 창)
        self.hits = []                 # [(claim, 상태, context, not_src)] 상태: bound|disclaimed|
                                       #   suspect|skipped|None(=unbound)
        self.declared = []             # 화면이 선언한 data-claim / data-claim-not 값 전부

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
            return
        if tag in self.CODE:
            self._code += 1
        d = dict(attrs)
        cid, nid = d.get("data-claim"), d.get("data-claim-not")
        # ⛔ BI-3 P0-2: 부인은 **어디의 무엇인지**를 같이 선언해야 한다. 건수만 맞으면
        #   그 자리의 의미가 바뀌어도 통과했다 (Codex 반례: 셀 하나를 철회값으로 갈아도
        #   disclaimed 1 · unbound 0 으로 초록). `data-claim-not-src` 가 그 자리의 계보다.
        nsrc = d.get("data-claim-not-src")
        for x in (cid, nid):
            if x:
                self.declared.append(x)
        if tag not in self.VOID:
            # ⛔ BI-4 P0-2: 좌표만 들고 **그 자리의 글**을 버렸다. 그래서 같은 좌표에서
            #   표시 내용을 통째로 갈아도 disclaimed 1 · unbound 0 으로 초록이었다
            #   (Codex 재현: `0.199` → `b2o3 MD Ea = 0.199 eV`). 부인 프레임은 이제
            #   자기 안의 텍스트를 모은다 — 나중에 원자료와 대조하기 위해서다.
            self._stack.append({"tag": tag, "cid": cid, "nid": nid, "nsrc": nsrc,
                                "buf": [] if nid else None})

    def handle_startendtag(self, tag, attrs):
        d = dict(attrs)
        for x in (d.get("data-claim"), d.get("data-claim-not")):
            if x:
                self.declared.append(x)

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self._skip = max(0, self._skip - 1)
            return
        if tag in self.CODE:
            self._code = max(0, self._code - 1)
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["tag"] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._skip or not data.strip():
            return
        # 부인 프레임들에 이 글을 넣어 둔다 (셀 전체가 여러 조각으로 올 수 있다)
        for fr in self._stack:
            if fr["buf"] is not None:
                fr["buf"].append(data)
        yes = {x for f in self._stack if f["cid"] for x in f["cid"].split()}
        no = {x for f in self._stack if f["nid"] for x in f["nid"].split()}
        # 가장 안쪽(=가장 구체적인) 부인 자리
        frame = next((f for f in reversed(self._stack) if f["nid"]), None)
        prev, self._ctx = self._ctx, (self._ctx + data)[-CTX_BEFORE:]
        for a, b, cl, q in find_claim_hits(data, self._claims, self._origin, prev):
            ctx = " ".join(data[max(0, a - 90): b + 90].split())
            if self._code:                     # 코드블록 안 — 결속 요구 밖(목록만)
                st = "skipped"
            elif cl["id"] in yes:
                st = "bound"
            elif cl["id"] in no:
                st = "disclaimed"
            elif q == "suspect":
                st = "suspect"
            else:
                st = None
            self.hits.append((cl, st, ctx,
                              frame if st == "disclaimed" else None))


def scan_claim_bindings(html: str, claims=None, reg=None, root=None,
                        origin="internal") -> dict:
    """한 화면의 결속 상태.
    → `{"bound", "unbound", "disclaimed", "suspect", "skipped", "declared", "dangling"}`

    · `bound`     — 값이 **자기 claim id 를 단 요소 안에** 있다 (구조 결속).
    · `disclaimed`— `data-claim-not="<id>"` 안에 있다: *"이 문자열은 그 주장이 아니다"*.
      우연 일치를 위한 것이다 — 실측 예: `/cascade` 스크리닝 표의 `window_gain 0.199`(V)는
      b2o3 MD Ea 0.199(eV)와 **아무 관계가 없다**. 그걸 결속하면 거짓 선언이 된다.
      ⚠ 이건 **면제가 아니라 선언**이다. id 를 이름으로 대야 하고(`*` 없음), 화면 검사가
        따로 세어 목록으로 남긴다 — 감사 대상이지 침묵이 아니다.
    · `suspect`   — 매처가 **그 주장이 아니라고 본다**(부호·단위·출처 조건). 결속을
      요구하지 않지만 **목록에 남는다** — 조용히 버리면 오탐 규칙 자체가 감사 불가가 된다.
    · `skipped`   — `<pre>`/`<code>` 안. 코드·로그의 숫자는 인용이 아니다.
    · `unbound`   — 위 어디에도 안 든다. **근접성은 보지 않는다** (⛔ 표지가 옆에 있어도
      id 를 대지 않으면 미결속이다 — 그게 BG ② 의 요지다).
    · `dangling`  — 선언한 id 중 레지스트리·위험원장에 없는 것 (오타·유령 결속).
      `data-claim-not` 도 같이 검사한다 — 오타 난 부인은 **조용히 억제**로 이어지므로.

    ⛔ 이 함수가 **못 하는 것**
      · 태그 **속성** 안의 값은 못 본다 (`title="b2o3(0.199±0.034)"` 툴팁). 텍스트 노드만 훑는다.
      · JS 가 나중에 그리는 것은 못 본다 (서버 응답 시점의 DOM 이 아니다).
      · `unbound == 0` 은 **지표가 아니다**. `md_html` 이 일치 자리를 자동으로 감싸므로
        그 경로를 지나는 화면의 0 은 "결속됐다" 가 아니라 "치환기가 돌았다" 이기도 하다.
        의미 있는 수는 `bound` 중 **선언(`declared`)으로 결속된 것**의 비율이다.
    """
    claims = claims if claims is not None else all_claims(reg=reg, root=root)
    usable = [c for c in claims if c.get("text")]
    # ⚠ 유령 결속 판정은 **레지스트리 전체**로 한다 (결속 대상 목록으로 하면 정상 항목을
    #   가리키는 결속까지 유령이 된다 — 실측: `MD_Ea_eV_singleseed@b2o3`).
    _r = reg if reg is not None else registry(root=root)
    known = {claim_id(e.get("metric"), e.get("system")) for e in _r.get("entries", [])}
    known |= {c["id"] for c in claims}
    # ⚠ **결속 어휘**로 판정한다 (`hazard_claims` 가 아니라 `hazard_ids`). 해소·폐기된
    #   위험을 화면이 이력으로 이름 대는 것은 정당하다 — 그걸 유령으로 터뜨리면 안 된다.
    known |= hazard_ids(root=root)
    sc = _ClaimScanner(usable, origin=origin)
    sc.feed(html)
    pick = lambda w: [(c, ctx) for c, s, ctx, _n in sc.hits if s == w]   # noqa: E731
    # ⚠ `disclaimed` 만 4-튜플 `(claim, ctx, src, cell)` 다 — 부인은 **어디의 무엇인지**를
    #   같이 내야 검사가 양방향으로 대조할 수 있다 (BI-3 P0-2).
    # ⛔ BI-4 P0-2: `cell` = **그 부인 자리에 실제로 표시된 글**. 좌표만으로는 같은 칸의
    #   내용이 바뀌어도 못 잡는다 (Codex 재현). `verify_disclaimers()` 가 이걸 원자료와 댄다.
    disc = [(c, ctx, (fr or {}).get("nsrc"),
             " ".join("".join((fr or {}).get("buf") or []).split()))
            for c, s, ctx, fr in sc.hits if s == "disclaimed"]
    return {"bound": pick("bound"), "disclaimed": disc, "unbound": pick(None),
            "suspect": pick("suspect"), "skipped": pick("skipped"),
            "declared": sc.declared,
            "dangling": sorted({x for d in sc.declared for x in d.split() if x not in known})}


#: `data-claim-not-src` 문법 — `"<데이터셋>|<키열>=<키값>|<열>"`.
#: 데이터셋이 없는 옛 형식(`"<키열>=<키값>|<열>"`)도 읽지만 **검증 불가**로 판정한다.
_NOTSRC_RE = re.compile(r"^(?:(?P<ds>[A-Za-z0-9_.:-]+)\|)?"
                         r"(?P<kcol>[^=|]+)=(?P<kval>[^|]*)\|(?P<col>.+)$")


def _num(s):
    """문자열에서 **하나의** 수를 뽑는다. 수가 0개거나 2개 이상이면 None."""
    m = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", str(s))
    if len(m) != 1:
        return None
    try:
        return float(m[0])
    except ValueError:
        return None


def verify_disclaimers(disc, resolve=None, root=None) -> list:
    """부인이 **가리킨 자리의 실제 값**과 화면에 뜬 글을 댄다 (Codex BI-4 P0-2).

    종전 검사는 **좌표와 건수**만 봤다. 그래서 같은 칸의 내용을 통째로 갈아도
    `disclaimed=1 · unbound=0` 으로 초록이었다 (Codex 재현: `0.199` →
    `b2o3 MD Ea = 0.199 eV`). 좌표가 맞다는 것은 **그 자리에 무엇이 떠 있는지**를
    말해 주지 않는다.

    검사 셋 — 하나라도 걸리면 그 부인은 `ok=False` 다:
      ① **좌표 해독** — `data-claim-not-src` 가 문법에 맞고 데이터셋을 이름 댔는가
      ② **행·열 실재** — 그 키값의 행이 원자료에 있고 그 열이 있는가
      ③ **값·표시 일치** — 셀의 글이 그 원자료 값 **하나만** 담는가.
         산문·단위·다른 주장이 섞이면 그건 **다른 발화**다 (그게 Codex 의 독약이다).

    `resolve(dataset) -> [row dict, ...]` 를 주면 그걸 쓰고, 안 주면
    `db/properties/<dataset>.csv` 를 읽는다.

    ⛔ 이 함수가 **못 하는 것**
      · 산문을 이해하지 않는다. *"이 셀이 지정한 열에서 나온 수 하나인가"* 만 본다.
      · 단위를 환산하지 않는다 — 셀에 단위가 붙어 있으면 **다른 발화로 보고 떨어뜨린다**.
      · 원자료가 그날 이후 바뀐 것은 못 본다 (버전 고정은 별도 항목이다).
    """
    import csv as _csv
    base = Path(root) if root else ROOT
    cache: dict = {}

    def _rows(ds):
        if ds in cache:
            return cache[ds]
        if resolve is not None:
            cache[ds] = resolve(ds) or []
            return cache[ds]
        f = base / "db/properties" / (ds + ".csv")
        try:
            # ⚠ 우리 CSV 는 머리에 `#` 주석줄을 단다 (codoping_ml_v2 실측) — 안 걸러내면
            #   DictReader 가 그 줄을 헤더로 읽어 **전 행이 조용히 어긋난다**.
            lines = [ln for ln in f.read_text(encoding="utf-8").splitlines()
                     if not ln.lstrip().startswith("#")]
            cache[ds] = list(_csv.DictReader(lines))
        except OSError:
            cache[ds] = None          # None = 못 읽었다 (빈 목록과 구분한다)
        return cache[ds]

    out = []
    for item in disc:
        cl, ctx, src, cell = (list(item) + [None] * 4)[:4]
        rec = {"claim": cl.get("id") if isinstance(cl, dict) else cl,
               "src": src, "cell": cell, "ok": False, "why": ""}
        if not src:
            rec["why"] = "좌표가 없다 — data-claim-not-src 미선언"
            out.append(rec); continue
        m = _NOTSRC_RE.match(src.strip())
        if not m:
            rec["why"] = f"좌표 문법이 아니다: {src!r}"
            out.append(rec); continue
        ds, kcol, kval, col = (m.group("ds"), m.group("kcol").strip(),
                               m.group("kval").strip(), m.group("col").strip())
        rec.update(dataset=ds, key_col=kcol, key_val=kval, col=col)
        if not ds:
            rec["why"] = ("좌표가 **데이터셋을 이름 대지 않았다** — 어느 원자료인지 모르면"
                          " 대조할 수 없다 (옛 2칸 형식)")
            out.append(rec); continue
        rows = _rows(ds)
        if rows is None:
            rec["why"] = f"원자료를 못 읽었다: db/properties/{ds}.csv — **확인 불가는 통과가 아니다**"
            out.append(rec); continue
        kv = _num(kval)
        hit = [r for r in rows
               if str(r.get(kcol, "")).strip() == kval
               or (kv is not None and _num(r.get(kcol)) == kv)]
        if not hit:
            rec["why"] = f"원자료에 {kcol}={kval} 행이 없다 ({ds}, {len(rows)}행)"
            out.append(rec); continue
        if len(hit) > 1:
            rec["why"] = f"{kcol}={kval} 이 {len(hit)}행이라 행을 특정 못 한다"
            out.append(rec); continue
        if col not in hit[0]:
            rec["why"] = f"원자료에 `{col}` 열이 없다 ({ds})"
            out.append(rec); continue
        raw = hit[0][col]
        rec["raw"] = raw
        rv, cv = _num(raw), _num(cell)
        if cv is None:
            rec["why"] = (f"셀에 수가 하나가 아니다 — 표시된 글: {str(cell)[:60]!r}. "
                          "부인은 **그 열의 값 하나**에만 걸린다")
            out.append(rec); continue
        if rv is None or abs(rv - cv) > 1e-9 * max(1.0, abs(rv)):
            rec["why"] = f"값이 다르다 — 원자료 {col}={raw!r} vs 셀 {cell!r}"
            out.append(rec); continue
        # ③ 셀이 **그 수만** 담는가 — 산문·단위가 붙으면 다른 발화다
        rest = re.sub(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", "", str(cell)).strip()
        if re.sub(r"[\s±,·|/()\[\]%–—-]", "", rest):
            rec["why"] = (f"셀에 값 밖의 글이 붙어 있다: {rest[:40]!r} — "
                          "부인한 자리와 다른 발화가 됐다")
            out.append(rec); continue
        rec["ok"] = True
        rec["why"] = f"{ds}[{kcol}={kval}].{col} = {raw} 와 일치"
        out.append(rec)
    return out


def retracted_values(reg=None, root=None) -> list:
    """철회된 정본값 목록 — `[{"metric","system","text","why","instead"}...]`.

    화면 검사가 **하드코딩 없이** "이 숫자는 철회됐다" 를 알기 위한 단일 출처다.
    `status=retracted` 인 레지스트리 항목에서 파생하므로, 값을 되살리면 검사도 같이 풀린다.
    """
    reg = reg if reg is not None else registry(root=root)
    out = []
    for e in reg.get("entries", []):
        if e.get("status") != "retracted":
            continue
        v = e.get("value")
        if v is None:
            continue
        r = e.get("retracted") or {}
        out.append({"metric": e.get("metric"), "system": e.get("system"),
                    "text": f"{float(v):g}", "why": r.get("why", ""),
                    "instead": r.get("usable_instead", "")})
    return out


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
    return _by_id(raw.get("decisions", []), "id", "결정", "db/governance/decisions.json")


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
# ⚠ 2026-08-20 확장: 사용자 워크스테이션(WSL/로컬 디스크)에만 있는 산출물이 실제로 나왔다
#   (~/'C:Users안용훈Downloadsbml_kisti' 18 GB — 폴더 이름이 깨져 어떤 수색에도 안 걸렸던 것).
#   server(원격 계산기)도 offline_backup(외장 매체)도 아니다. 어휘를 늘리는 게 맞다.
LOCATION_KINDS = ("repo", "offline_backup", "server", "workstation", "lost")


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
    return _by_id(raw.get("artifacts", []), "id", "산출물", "db/governance/artifacts.json")


def protocol_generations(root=None) -> dict:
    """MD 잣대 세대 원장. {generation_id: record}. 없으면 빈 dict.

    왜 (2026-09-07, 1저자 지시 "예전 잣대면 예전 잣대라고 db 에도 표시해두고")
      `comparison_group` 이 **프로토콜**(시드 수·온도 집합)을 가른다면, 이건 **잣대**를
      가른다 — 그 값이 만들어질 당시 어떤 게이트가 **존재했는가**. 둘은 직교한다.
      같은 group 안에서도 세대가 다를 수 있고, 그러면 한 표에 올리면 안 된다.

    ⛔ 이 함수가 못 하는 것
      · 세대를 **추론하지 않는다.** 항목이 스스로 `protocol_generation` 을 들고 있어야 한다.
        날짜로 자동 판정하면 재실행·소급 승격이 조용히 틀린 라벨을 받는다.
      · 세대는 **품질 등급이 아니다.** gen0 은 "현행 게이트로 검증되지 않았다" 이지
        "틀렸다" 가 아니다 (원장 `_이_파일이_못_하는_것` 참조).
    """
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    p = base / "db/properties/md_protocol_generations.json"
    if not p.exists():
        return {}
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:                        # noqa: BLE001
        raise RuntimeError(f"⛔ md_protocol_generations.json 을 못 읽는다 "
                           f"(fail-closed): {exc!r}") from exc
    return {g["id"]: g for g in raw.get("generations", []) if isinstance(g, dict) and g.get("id")}


def generation_of(e: dict, root=None) -> dict | None:
    """레지스트리 항목의 세대 기록. 세대가 없거나 어휘 밖이면 None."""
    gid = e.get("protocol_generation")
    if not gid:
        return None
    return protocol_generations(root).get(gid)


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


def _dstate(d: dict):
    """판례의 상태를 읽는다 — `decision_state` 가 정본, `status` 는 별칭.

    ⛔ 왜 별칭까지 읽나 (2026-09-01): 승인 검사가 `decision_state` 만 보던 동안
      원장에 `status` 만 든 기록이 있었고, 그 기록은 `status: active` 로 올려도
      **어떤 검사에도 안 걸렸다**. 별칭을 같이 읽어 그 경로를 막는다.
      (필드 부재·두 필드 불일치 자체도 validate_governance 가 위반으로 낸다.)
    """
    return d.get("decision_state", d.get("status"))


def decision_state(d: dict):
    """판례 하나의 상태 문자열 — 화면·검사가 **같은 함수**를 쓰게 하려고 공개한다.

    ⛔ 왜 필요했나 (2026-09-08): /governance 판례 표가 `d.decision_state` 만 읽어서
      `status` 만 든 기록(D-2026-08-31-sdcp-polaron-Fbb)이 상태 칸에 **`None` 이라고
      찍혀 있었다.** 검사(_dstate)는 별칭을 읽는데 화면만 안 읽던 것 — 같은 원장을
      두 규칙으로 읽으면 화면이 조용히 틀린다.

    ⛔ 이 함수가 **못 하는 것**: 상태가 옳은지·허용 어휘인지 판정하지 않는다.
      그건 validate_governance 가 한다 (여기서 또 검사하면 사본이 둘이 된다).
    """
    return _dstate(d)


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
        # ⛔ 2026-09-01 fail-open 봉인 — 아래 승인 검사가 `decision_state` 만 보는데
        #   원장에 `status` 만 든 기록이 2건 있었다(polaron Fbb·S0). 그 기록은
        #   나중에 `status: active` 로 올려도 **어떤 검사에도 안 걸린다** —
        #   즉 사람 승인 없이 active 가 되는 경로가 열려 있었다.
        #   두 필드를 같이 읽고, 어긋나거나 둘 다 없으면 그 자체를 위반으로 낸다.
        if "decision_state" not in d and "status" not in d:
            bad.append(f"결정 {d['id']} 에 decision_state 가 없다 — 승인 검사가 통째로 "
                       f"건너뛰어진다 (fail-open)")
        elif ("decision_state" in d and "status" in d
                and d["decision_state"] != d["status"]):
            bad.append(f"결정 {d['id']} 의 decision_state({d['decision_state']!r}) 와 "
                       f"status({d['status']!r}) 가 어긋난다 — 어느 쪽이 정본인지 알 수 없다")
        # ⛔ 상태 어휘 (AW P0-4) — 모르는 상태는 검사를 조용히 건너뛰게 한다
        # ⛔⛔ 2026-09-07 회신 BG ④ — 종전 판은 **두 구멍**이 있었다:
        #   ① 위 부재 검사가 `"decision_state" not in d` 라 **키가 있고 값이 null** 이면 통과
        #   ② 여기서도 `if _st is not None` 이라 **null 이면 enum 검사를 건너뛴다**
        #   ⇒ `{"decision_state": null}` 은 어느 검사에도 안 걸리고, 그 상태로
        #      `_dstate(d) == "active"` 비교만 피하면 사람 승인 없이 흘러간다.
        #   상태는 "키가 있음" 이 아니라 **비어 있지 않은 문자열 + 허용 어휘**여야 한다.
        _st = _dstate(d)
        if not isinstance(_st, str) or not _st.strip():
            bad.append(f"결정 {d['id']} 의 상태가 문자열이 아니거나 비어 있다 "
                       f"({_st!r}) — null·숫자·리스트·빈 문자열은 상태가 아니다")
        elif _st not in DECISION_STATES:
            bad.append(f"결정 {d['id']} 의 상태 {_st!r} 가 허용 어휘 밖이다 "
                       f"({sorted(DECISION_STATES)})")
        for f in ("supersedes", "does_not_supersede", "open_conflicts", "evidence"):
            if f in d and not isinstance(d[f], list):
                bad.append(f"결정 {d['id']} 의 {f} 가 리스트가 아니다 ({type(d[f]).__name__})")
        #: ⛔ 2026-09-21 — 바로 위 검사가 "리스트가 아니다" 를 `bad` 에 넣는데, 그 다음 줄이
        #:   **보고 전에** 순회하다 TypeError 로 죽었다 (`supersedes: null` 인 결정 하나로 실측).
        #:   진단을 내놓아야 할 자리에서 crash 하면 그건 fail-closed 가 아니다.
        #:   ⚠ 키가 **없는** 경우는 종전처럼 정상이다 — 원장 대부분이 그 모양이다.
        _sup = d.get("supersedes")
        for ref in (_sup if isinstance(_sup, list) else []):
            if ref not in dec:
                bad.append(f"결정 {d['id']} 의 supersedes 대상 {ref} 가 원장에 없다 (dangling)")
            else:
                # ⛔⛔ 회신 AW P0-3 · AZ P0-6 (2026-09-01) — **좁은 노드가 전역 정책을
                #   supersede 할 수 없다.** C-12 estimand 노드(systems 2개)가 전역
                #   마감정책(systems `*`)을 대체하고 있었고, 그 상태로 계산을 던지면
                #   결과가 정책 결정에 압력을 준다 (사전등록의 의미가 사라진다).
                _t = dec[ref]
                _ts = ((_t.get("applies_to") or {}).get("systems") or [])
                _ds = ((d.get("applies_to") or {}).get("systems") or [])
                if "*" in _ts and "*" not in _ds:
                    bad.append(
                        f"결정 {d['id']}(systems {_ds}) 가 **전역** 결정 {ref}"
                        f"(systems ['*']) 를 supersede 한다 — 좁은 노드는 전역 정책을 "
                        f"대체할 수 없다 (회신 AW P0-3 불허 · AZ P0-6)")
                if _t.get("kind") == "policy" and d.get("kind") != "policy":
                    bad.append(
                        f"결정 {d['id']}(kind={d.get('kind')!r}) 가 policy 결정 {ref} 를 "
                        f"supersede 한다 — 정책은 정책으로만 대체한다")
        sb = d.get("superseded_by")
        if sb and sb not in dec:
            bad.append(f"결정 {d['id']} 의 superseded_by {sb} 가 원장에 없다 (dangling)")
        rat = d.get("ratification") or {}
        if _dstate(d) == "active" and not (
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
    # ⛔ 2026-09-13 — **뼈대 마감 카드로 마감을 선언하는 길**을 막는다.
    #   §4b 마감 기록은 종료 문구·재개 조건을 비운 채 먼저 만들었다(1저자 결정 · 회신 대기).
    #   그 상태에서 결정만 active 로 올라가면 "재개 조건이 비어 있다" 가 *아무 때나 재개* 로도
    #   *절대 재개 불가* 로도 읽힌다 — 둘 다 우리 규율이 아니다.
    #   ⚠ 방향을 **카드 → 결정** 으로 본다. `method_ref` 를 키로 삼으면 조용히 빗나간다:
    #     실측으로 active 마감 결정 4건 중 **3건의 method_ref 가 카드 경로가 아니었다**
    #     (도구+플래그 · 산문 · 리스트). 그래서 카드 쪽에서 역참조를 찾는다.
    #   ⚠ `closed` 키가 **없는** 카드는 뼈대가 아니다 — 이 필드보다 먼저 만들어진 카드들이다.
    #     "못 찾음" 과 "없음" 을 구분한다: 못 읽은 카드는 아래에서 **위반으로** 낸다.
    try:
        _b3 = Path(root) if root else Path(__file__).resolve().parent.parent
        for _cf in sorted((_b3 / "db" / "properties").glob("*closed*.json")):
            try:
                _cd = json.loads(_cf.read_text(encoding="utf-8"))
            except (OSError, ValueError) as _e:
                bad.append(f"마감 카드를 못 읽었다: {_cf.name} — {type(_e).__name__} "
                           f"(못 읽음은 '뼈대 아님' 이 아니다)")
                continue
            if not isinstance(_cd, dict) or _cd.get("closed") is not False:
                continue
            _rel = _cf.relative_to(_b3).as_posix()
            for _d in dec.values():
                if _dstate(_d) != "active":
                    continue
                if _rel in json.dumps(_d, ensure_ascii=False):
                    bad.append(
                        f"결정 {_d['id']} 이 active 인데 참조한 마감 카드 {_rel} 가 "
                        f"`closed: false` 다 — 뼈대 카드로는 마감을 선언할 수 없다 "
                        f"(빈 재개 조건은 '재개 사유 없음' 이 아니다)")
    except OSError as _e:                      # db/properties 가 없는 격리 시험용 root
        bad.append(f"마감 카드 디렉터리를 못 열었다: {type(_e).__name__}: {_e}")

    # slot 유일성 — 같은 slot 에 active 가 둘이면 어느 쪽이 이기는지 알 수 없다.
    # ⚠ 2026-09-07 — 종전 구현은 **slot 이름만** 봤는데, 원장 `_rules` 는
    #   *"유일성은 scope 가 아니라 **slot + 겹치는 applicability** 에서 검사한다"* 라고
    #   적혀 있다. 규칙과 구현이 갈라져 있었고, `campaign_closure` 처럼 계마다 하나씩
    #   생기는 slot 에서 **두 번째 계를 등록하는 순간 무조건 실패**했다
    #   (sdcp 마감 + b2o3 마감 — 두 결정은 서로 아무 관계가 없다).
    #   ⇒ 문서된 규칙대로 **applicability 가 겹칠 때만** 충돌로 낸다.
    # ⛔ 완화가 아니다: 겹침 판정은 **systems 만** 본다(tasks·methods 로 더 잘게 쪼개
    #   빠져나가는 길을 열지 않는다). systems 가 비었거나 `*` 면 **전역 = 모두와 겹친다.**
    def _sys_set(d):
        s = ((d.get("applies_to") or {}).get("systems") or [])
        if isinstance(s, str):          # 문자열 하나를 글자로 순회하지 않는다
            s = [s]
        return set(s)

    def _sys_overlap(a, b):
        sa, sb = _sys_set(a), _sys_set(b)
        if not sa or not sb or "*" in sa or "*" in sb:
            return True                 # 전역은 모두와 겹친다
        return bool(sa & sb)

    slots = {}
    for d in dec.values():
        if _dstate(d) == "active":
            slots.setdefault(d.get("slot"), []).append(d)
    for slot, ds in slots.items():
        for i, a in enumerate(ds):
            for b in ds[i + 1:]:
                if _sys_overlap(a, b):
                    bad.append(f"slot '{slot}' 에 applicability 가 겹치는 active 결정이 "
                               f"둘이다: {[a['id'], b['id']]} "
                               f"(systems {sorted(_sys_set(a)) or '*'} ∩ "
                               f"{sorted(_sys_set(b)) or '*'})")
    # ⛔ 회신 AW P0-4 — 중복 ID 는 **로더가 조용히 덮어쓴다** (dict 라 뒤가 이긴다).
    #   원장을 손으로 이어붙이다 같은 id 를 두 번 쓰면 앞 기록이 사라지는데
    #   아무 검사에도 안 걸렸다. 원본 리스트에서 직접 센다.
    try:
        _base = Path(root) if root else Path(__file__).resolve().parent.parent
        _raw = json.loads((_base / "db/governance/decisions.json")
                          .read_text(encoding="utf-8")).get("decisions") or []
        _ids = [x.get("id") for x in _raw if isinstance(x, dict)]
        _dup = sorted({i for i in _ids if i and _ids.count(i) > 1})
        if _dup:
            bad.append(f"결정 id 가 중복이다 {_dup} — 로더가 조용히 덮어쓴다")
        if len(_raw) != len(dec):
            bad.append(f"원장 항목 {len(_raw)}개인데 적재된 결정은 {len(dec)}개다 "
                       f"— 조용히 사라진 기록이 있다")
    except Exception as exc:                                    # noqa: BLE001
        bad.append(f"decisions.json 원본을 다시 읽지 못했다 (fail-closed): {exc!r}")

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


#: `retracted.usable_instead` 가 취할 수 있는 **꼴**. 스키마가 이걸 못 표현하면
#: "대체값이 없다" 를 적을 자리가 없어져 사람이 **아무 문장이나** 채워 넣는다.
#: ⛔ 실측 사고 (Codex BI P0-1 · 2026-09-08): b2o3 MD_Ea 의 `usable_instead` 가
#:   "저온 구간만 0.2241±0.0606" 이었는데, 그건 D-2026-09-07-b2o3-md-closure-retrospective
#:   가 **인용 금지로 못박은 구간 Ea** 다. 즉 원장이 자기가 금지한 값을 대체값으로 권했다.
#:   원인은 거짓말이 아니라 **자리가 없었던 것** — 종전 validate 가 빈 값을 거부했다.
INSTEAD_KINDS = ("sentinel_none", "claim_ref", "prose")


def _check_usable_instead(r: dict, root=None) -> list:
    """`retracted` 절의 대체값 선언을 검사한다 → 문제 문자열 목록 (빈 목록 = 통과).

    받는 꼴 셋 — 어느 것이든 `instead_kind` 로 **무엇인지 이름을 대야** 한다.
      · `sentinel_none` — `usable_instead = {"none": true, "decision": "D-…", "why": "…"}`
        *"인용 가능한 대체값이 0개"*. 그 판정을 내린 결정 id 를 반드시 든다.
      · `claim_ref`     — `"<metric>@<system>"`. 레지스트리에 있고 **인용 가능**해야 한다.
      · `prose`         — 자유 문장. 검사기가 정당성을 못 본다는 뜻이므로 사람 검토
        (`instead_reviewed_by` + `instead_reviewed_at`)를 요구한다.

    ⛔ 이 검사가 **못 하는 것**: prose 의 내용이 참인지, 그 문장이 다른 원장의 금지를
      어기는지는 못 본다. 그걸 보는 것은 결정↔값 배선(`enforcement.binds`)이고 아직 없다.
      그래서 prose 는 통과가 아니라 **사람 서명**으로만 지나간다.
    """
    ui, kind = r.get("usable_instead"), r.get("instead_kind")
    if kind is None:
        return [("retracted.instead_kind 가 없다 — 대체값이 무엇인지(없음/다른 정본값/산문) "
                 f"이름을 대야 한다 (허용: {list(INSTEAD_KINDS)})")]
    if kind not in INSTEAD_KINDS:
        return [f"retracted.instead_kind 가 어휘 밖이다: {kind!r} (허용: {list(INSTEAD_KINDS)})"]
    if kind == "sentinel_none":
        if not isinstance(ui, dict) or ui.get("none") is not True:
            return ["instead_kind=sentinel_none 인데 usable_instead 가 "
                    "{\"none\": true, …} 꼴이 아니다"]
        did = ui.get("decision")
        if not did:
            return ["대체값 없음(sentinel_none)인데 그 판정을 내린 decision id 가 없다 — "
                    "'없다' 도 판정이라 누가 언제 정했는지가 원장에 있어야 한다"]
        ds = decisions(root=root)
        if did not in ds:
            return [f"usable_instead.decision 이 원장에 없는 결정을 가리킨다: {did!r}"]
        if (ds[did].get("ratification") or {}).get("state") != "ratified":
            return [f"usable_instead.decision {did!r} 이 아직 비준되지 않았다 — "
                    f"미비준 결정으로 대체값을 없앨 수 없다"]
        if not (ui.get("why") or "").strip():
            return ["대체값 없음(sentinel_none)인데 why 가 비었다"]
        return []
    if kind == "claim_ref":
        if not isinstance(ui, str) or "@" not in ui:
            return ["instead_kind=claim_ref 인데 usable_instead 가 '<metric>@<system>' 이 아니다"]
        _r = registry(root=root)
        hit = [e for e in _r.get("entries", [])
               if claim_id(e.get("metric"), e.get("system")) == ui]
        if not hit:
            return [f"usable_instead 가 레지스트리에 없는 항목을 가리킨다: {ui!r}"]
        e2 = hit[0]
        if e2.get("status") == "retracted" or e2.get("citable") is False:
            return [f"대체값 {ui!r} 자신이 인용 불가다 (status={e2.get('status')!r}, "
                    f"citable={e2.get('citable')!r}) — 철회값을 철회값으로 대체할 수 없다"]
        return []
    # prose
    if not (ui or "").strip() if isinstance(ui, str) else not ui:
        return ["instead_kind=prose 인데 usable_instead 가 비었다"]
    miss = [k for k in ("instead_reviewed_by", "instead_reviewed_at") if not r.get(k)]
    if miss:
        return [f"instead_kind=prose 는 사람 검토가 필요하다 — 없는 필드: {miss}. "
                f"검사기는 산문이 다른 원장의 금지를 어기는지 못 본다"]
    return []


def validate_hazards(root=None, reg=None) -> list:
    """인용위험 원장 자체의 무결성 → 문제 문자열 목록.

    ⛔ 종전에는 **아무도 이 파일을 검사하지 않았다.** `validate()` 는 레지스트리↔원자료만,
      `validate_governance()` 는 결정↔판정만 본다. 그래서 hazard 의 `fix` 가 **존재하지 않는
      키**(`FINAL_for_paper.Ea_eV_PAPER`)를 "이것만 인용하라" 고 3주 동안 가리키고 있었다.

    검사 다섯 (전부 사실검사 — 사람 판단 0):
      H1  `level` 이 `HAZARD_LEVELS` 어휘 안인가
      H2  `claim` 이 레지스트리에 실재하는 (metric, system) 인가
      H3  `fix`/`what` 이 지목하는 **점표기 키**가 그 원자료 파일에 실재하는가
      H4  `id` 가 중복되지 않는가
      H5  `prohibition_axis` 가 어휘·모양을 지키고 **실제로 무엇인가를 덮는가**
          (Codex BI-4 Q5 · 2026-09-09)

    ⛔ 못 하는 것: 금지가 **옳은지**, 화면이 그 금지를 지키는지는 못 본다 (그건 결속 검사다).
      그리고 H5 는 축이 **너무 넓은지**는 못 본다 — `quantity_group` 에 흔한 낱말을 넣으면
      과잉차단이 되는데, 그건 사람이 본다.
    """
    import re as _re
    bad, seen = [], {}
    _r = reg if reg is not None else registry(root=root)
    known = {claim_id(e.get("metric"), e.get("system")) for e in _r.get("entries", [])}
    src = {e.get("source_path") for e in _r.get("entries", []) if e.get("source_path")}
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    for i, z in enumerate(_hazard_rows(root=root)):
        tag = f"hazard[{i}] {z.get('id') or z.get('doc') or z.get('what', '')[:34]!r}"
        lv = z.get("level")
        if lv not in HAZARD_LEVELS:                                          # H1
            bad.append(f"{tag}: level 이 어휘 밖이다 — {lv!r} (허용: {list(HAZARD_LEVELS)}). "
                       f"어휘 밖은 살아있는 금지로 친다(fail-closed)")
        hid = z.get("id")
        if hid:                                                              # H4
            if hid in seen:
                bad.append(f"{tag}: id 가 중복이다 — hazard[{seen[hid]}] 와 같다. "
                           f"id 는 재사용 금지 영구 식별자다")
            seen[hid] = i
        cl = z.get("claim")
        if cl and cl not in known:                                           # H2
            bad.append(f"{tag}: claim {cl!r} 이 레지스트리에 없다")
        for fld in ("fix", "what", "why"):                                   # H3
            for m in _re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)\b",
                                  str(z.get(fld) or "")):
                dotted = m.group(1)
                if dotted.endswith((".json", ".py", ".sh", ".md", ".csv", ".xyz")):
                    continue
                head = dotted.split(".")[0]
                # 그 점표기가 가리키는 원자료 후보 — hazard 가 든 파일, 없으면 레지스트리 전체
                explicit = bool(z.get("source_path"))
                cands = [z.get("source_path")] if explicit else sorted(src)
                # ⛔⛔ BI-4 P1 (2026-09-09) — 종전에는 **파일 없음 · 읽기 실패 · 최상위 키
                #   없음** 을 전부 `continue` 로 넘겼다. 그래서 원자료가 하위 키만 잃으면
                #   잡았지만 **`FINAL_for_paper` 자체를 개명하면 오류 0건**이었다 (Codex 재현).
                #   즉 H3 가 막으려던 그 사고(2026-08-24 개명)의 **정확한 모양을 못 잡았다.**
                #   ⇒ `source_path` 를 명시한 hazard 는 셋 다 오류다. 명시가 없는 경우만
                #     "그 키를 가진 파일을 찾는" 휴리스틱으로 남긴다 (산문 오탐 방지).
                for sp in cands:
                    if not sp or not str(sp).endswith(".json"):
                        continue
                    p = base / sp
                    if not p.exists():
                        if explicit:
                            bad.append(f"{tag}: {fld} 가 가리키는 **원자료가 없다** — {sp} "
                                       f"({dotted!r}). 죽은 포인터다")
                            break
                        continue
                    try:
                        doc = json.loads(p.read_text(encoding="utf-8"))
                    except Exception as ex:                                  # noqa: BLE001
                        if explicit:
                            bad.append(f"{tag}: {fld} 가 가리키는 **원자료를 못 읽었다** — "
                                       f"{sp} ({type(ex).__name__}). 확인 불가는 통과가 아니다")
                            break
                        continue
                    if not isinstance(doc, dict):
                        if explicit:
                            bad.append(f"{tag}: {fld} 가 가리키는 원자료가 객체가 아니다 — "
                                       f"{sp} ({type(doc).__name__})")
                            break
                        continue
                    if head not in doc:
                        if explicit:
                            bad.append(f"{tag}: {fld} 가 {sp} 에 **없는 최상위 키**를 "
                                       f"지목한다 — {head!r} (개명·삭제 의심). "
                                       f"화면·원고가 그 지시를 따를 수 없다")
                            break
                        continue
                    cur, ok = doc, True
                    for part in dotted.split("."):
                        if isinstance(cur, dict) and part in cur:
                            cur = cur[part]
                        else:
                            ok = False
                            break
                    if not ok:
                        bad.append(f"{tag}: {fld} 가 {sp} 에 **없는 하위 키**를 지목한다 — "
                                   f"{dotted!r}. 화면·원고가 그 지시를 따를 수 없다")
                    break
        # ── H5: 축 단위 금지의 모양·어휘·실효성 ──────────────────────────
        ax = z.get("prohibition_axis")
        if ax is not None:
            if not isinstance(ax, dict):
                bad.append(f"{tag}: prohibition_axis 가 객체가 아니다 ({type(ax).__name__})")
            else:
                unk = sorted(set(ax) - set(AXIS_KEYS)
                             - {"why", "decision", "added"}
                             - {k for k in ax if str(k).startswith(("⛔", "⚠"))})
                if unk:
                    bad.append(f"{tag}: prohibition_axis 에 어휘 밖 키 {unk} "
                               f"(허용: {list(AXIS_KEYS)} + why/decision/added + ⛔·⚠ 주석)")
                for k in ("system", "quantity_group"):
                    if not ax.get(k):
                        bad.append(f"{tag}: prohibition_axis 에 `{k}` 가 없다 — "
                                   f"계와 보고량군이 없으면 축이 무엇을 덮는지 모른다")
                if not isinstance(ax.get("quantity_group", []), list):
                    bad.append(f"{tag}: prohibition_axis.quantity_group 이 배열이 아니다")
                # ⛔ 실효성 — 이 축이 **레지스트리의 무엇도 안 덮으면** 죽은 선언이다.
                #   (오타·잘못된 계 이름이 여기서 잡힌다. 축의 값어치는 레지스트리 밖
                #    claim 도 덮는 것이지만, 하나도 안 덮히면 그건 배선 실패다.)
                if isinstance(ax, dict) and ax.get("system") and ax.get("quantity_group"):
                    if not any(axis_covers(k, ax) for k in known):
                        bad.append(f"{tag}: prohibition_axis 가 레지스트리의 어떤 claim 도 "
                                   f"안 덮는다 — 계 이름이나 보고량군 오타를 의심해라 "
                                   f"(system={ax.get('system')!r}, "
                                   f"method={ax.get('method')!r})")
    return bad


def validate(reg: dict, root=None) -> list:
    """(entry, 문제) 목록. 빈 목록 = 레지스트리가 원자료와 일치한다."""
    bad = []
    # ⛔ 회신 AW P0-4 — `index()` 가 같은 (metric, system) 을 조용히 덮던 것을 표식으로
    #   바꿨다. 그 표식을 **여기서 위반으로 내지 않으면** 표식만 달고 아무 일도 안 난다.
    #   index() 를 여기서 한 번 돌려 충돌을 세운다 (부작용으로 항목에 표식이 붙는다).
    index(reg)
    for e in reg.get("entries", []):
        if e.get("_index_conflict"):
            bad.append((e, f"색인 충돌 — {e['_index_conflict']}. 배지·툴팁이 어느 항목을 "
                           f"보여줄지 정해져 있지 않다 (회신 AW P0-4)"))
        # ── protocol_generation (2026-09-07) ────────────────────────────────
        # ⛔ fail-closed. MD 축은 2026-07~09 사이에 **판정 규칙 자체**가 세 번 바뀌었다.
        #   세대 표시가 없으면 화면은 gen0(구 잣대) 값을 현행 값처럼 보여준다 — 어제
        #   1저자가 세미나 값을 보고 "생각보다 옛날 값 아니야?" 라고 물은 그 구멍이다.
        #   빠뜨림을 **통과로 읽지 않는다**: 없어도 오류, 어휘 밖이어도 오류.
        _gid = e.get("protocol_generation")
        _vocab = protocol_generations(root)
        if str(e.get("metric", "")).startswith("MD_") and not _gid:
            bad.append((e, "MD_* 항목인데 protocol_generation 이 없다 — 이 값이 어느 "
                           "잣대(게이트 세대)로 만들어졌는지 원장 밖에 있다는 뜻이다. "
                           "db/properties/md_protocol_generations.json 참조"))
        elif _gid and not _vocab:
            bad.append((e, f"protocol_generation={_gid!r} 인데 세대 원장을 못 읽는다 "
                           f"(db/properties/md_protocol_generations.json) — 어휘를 대조할 "
                           f"수 없으므로 통과시키지 않는다"))
        elif _gid and _gid not in _vocab:
            bad.append((e, f"protocol_generation 이 어휘 밖이다: {_gid!r} "
                           f"(허용: {sorted(_vocab)})"))
        # ── status=retracted ────────────────────────────────────────────────
        # ⛔ 2026-08-25 — 철회된 값은 **원자료에 살아 있으면 안 된다**(철회하면서 키를
        #   _RETRACTED_… 로 옮기거나 문자열로 바꾼다). 그래서 수치 대조가 성립하지 않는다.
        #   그렇다고 그냥 건너뛰면 "철회" 가 검사를 피하는 뒷문이 된다 —
        #   **사유와 대체값을 원장 안에** 요구한다. (b2o3 MD_Ea 0.199 가 첫 사례)
        if e.get("status") == "retracted":
            r = e.get("retracted")
            if not isinstance(r, dict):
                bad.append((e, "status=retracted 인데 retracted 절이 없다 — "
                               "철회는 사유가 원장 안에 있어야 한다(파일명·기억은 판정이 아니다)"))
                continue
            if not r.get("why"):
                bad.append((e, "retracted.why 가 없다 — 왜 철회했는지를 적지 않으면 "
                               "다음 사람이 같은 값을 다시 인용한다"))
            bad += [(e, m) for m in _check_usable_instead(r, root=root)]
            continue
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
    sel = entries(reg, metric, group, status)
    # ⛔ 회신 AW P0-4 — 같은 system 이 두 번 나오면 종전엔 **마지막 값이 이겼다.**
    #   화면·순위·레이더가 전부 이 dict 를 쓰므로, 중복은 조용히 "다른 계산의 값" 을
    #   정본 자리에 앉힌다. group 을 안 준 호출에서 특히 쉽게 난다(프로토콜 혼입).
    seen = {}
    for e in sel:
        s = e["system"]
        if s in seen and seen[s] != e["value"]:
            raise RuntimeError(
                f"⛔ canonical_map({metric!r}, group={group!r}) 에 system {s!r} 이 값이 다른 채 "
                f"두 번 있다 ({seen[s]} vs {e['value']}) — 마지막 값이 조용히 이기면 안 된다. "
                f"comparison_group 을 지정하거나 레지스트리에서 하나로 정리할 것 (회신 AW P0-4)")
        seen[s] = e["value"]
    return seen


def groups_of(reg, metric) -> dict:
    """{comparison_group: [entry...]} — 비교 가능한 묶음을 그대로 돌려준다."""
    g = {}
    for e in entries(reg, metric, status=None):
        g.setdefault(e.get("comparison_group") or "ungrouped", []).append(e)
    return g


def index(reg) -> dict:
    """(metric, system) → entry. 배지·툴팁이 상태/출처를 바로 꺼내 쓰기 위한 색인.

    ⛔ 회신 AW P0-4 — 같은 `(metric, system)` 이 둘이면 종전엔 마지막 항목이 덮었다.
      배지·툴팁이 **다른 항목의 status·출처**를 보여주게 되고, `validate()` 는 그걸
      문제로 내지 않았다. 색인은 조용히 고르지 않는다 — 충돌을 항목에 적어 둔다.

    ⚠ 여기서는 예외를 던지지 않는다. 색인은 **화면 전체**가 쓰기 때문에 한 항목의 중복이
      사이트를 통째로 죽이면 안 된다. 대신 `_index_conflict` 를 달아 `validate()` 가
      위반으로 내고, 배지가 그 사실을 표시할 수 있게 한다.
    """
    out = {}
    for e in reg.get("entries", []):
        k = (e.get("metric"), e.get("system"))
        if k in out:
            prev = out[k]
            note = (f"같은 (metric, system) 항목이 둘 이상이다 — "
                    f"group {prev.get('comparison_group')!r} / {e.get('comparison_group')!r}, "
                    f"값 {prev.get('value')} / {e.get('value')}")
            prev["_index_conflict"] = note
            e["_index_conflict"] = note
        out[k] = e
    return out
