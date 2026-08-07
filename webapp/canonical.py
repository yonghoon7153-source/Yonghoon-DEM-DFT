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
        if e.get("status") == "canonical" and e.get("blocking_gate"):
            bad.append((e, f"게이트 미통과({e['blocking_gate']})인데 status=canonical 이다 "
                           f"— 값이 맞아도 정본이 될 수 없다"))
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
