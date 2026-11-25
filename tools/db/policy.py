#!/usr/bin/env python3
"""policy.py — **원자료를 소비하는 도구가 마감·금지 판정을 읽는다.**

    python3 tools/db/policy.py db/properties/b2o3_md_arrhenius.json   # 이 파일 상태
    python3 tools/db/policy.py --selftest

왜 생겼나 (Codex BI-3 P0-4 · 2026-09-09)
  `db/properties/b2o3_md_arrhenius.json` 의 인용 지위를 고쳤는데,
  `tools/modelc_v3/nernst_einstein_300K.py` 에 그 파일을 주면 **정상 종료하면서**
  `Ea = 0.2241 eV` 와 300 K 외삽 D·σ 를 다시 만들고 *"비교는 비율로만"* 이라고
  권했다. 마감 카드가 그 축의 **수송 비교와 300 K 외삽을 둘 다 금지**하는데도.
  원인: 그 도구가 개명한 필드가 아니라 **다른 가지**(`⛔_RETRACTED….multiseed_3x3`)를
  키 이름으로 훑기 때문에 원자료 정정의 영향을 받지 않았다.
  ⇒ **원자료를 고치는 것만으로는 하류가 안 닫힌다. 소비자가 정책을 읽어야 한다.**

무엇을 읽나
  ① `db/properties/*_closed_*.json` · `*_closed_retrospective_*.json` — 마감 카드
     (`닫는_범위` · `금지_서술` · `근거_파일` · `확정값`)
  ② `db/properties/citation_hazards.json` — 행의 `file` 이 이 파일을 가리키고
     **금지가 살아 있으면**(`prohibition_state`, 기본 fail-closed) 걸린다.

⛔ 이 도구가 **못 하는 것**
  · 무엇을 계산하려는지 모른다. **파일 단위**로만 본다 — 같은 파일 안의 살아있는
    축(예: b2o3 의 0 K DFT)을 쓰려는 경우도 일단 막고, 호출자가 사유를 대고 넘긴다.
  · 금지 서술의 **의미**를 해석하지 않는다. 카드가 닫혔다고 말하는지만 본다.
  · 마감 카드가 `근거_파일` 에 안 적어 둔 파일은 **못 잡는다** — 원장이 근거다.
  · **대상이 무엇인지 알아내지 못한다** — 이름으로만 맞춘다. 그래서 아래 규칙이 있다.

⛔⛔ 2026-09-09 — **없는 파일에 ✅ 를 줬다** (BI-4 P0-1 이 다른 축에서 재발)
  `python3 tools/db/policy.py db/properties/modelc_md_arrhenius.json` 가
  **✅ 열려 있음 (금지가 없음을 확인)** 을 찍었다. 그런데 그 파일은 저장소에 **없다.**
  (`kb/reviews/codex_BI_reply_2026_09_09.md` §7-4 가 그 줄을 ✅ 경로의 **실측 예시**로
  쓰고 있었다 — 기능이 아니라 구멍을 보여 주고 있었다. kb 린트의 깨진 경로 검사가 잡았다.)
  원인: `state` 셋을 원장 쪽에만 걸었고 **대상 쪽에는 안 걸었다.**
  ⇒ 규칙: **대상을 실재하는 파일로 못 붙이면 `policy_error`.**
  *"그런 파일 못 찾았다"* 는 *"금지가 없다"* 가 아니다. 오타 한 글자가 초록불이 됐었다.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PROPS = REPO / "db/properties"
#: 명시가 없을 때 금지가 꺼지는 유일한 level (webapp/canonical.py 와 같은 규약).
_PROHIBITION_OFF = frozenset(("RESOLVED",))


def _prohibition_active(row: dict) -> bool:
    """webapp `canonical.prohibition_active` 와 **같은 규칙**. fail-closed."""
    raw = row.get("prohibition_state")
    if raw is not None and str(raw).strip():
        return str(raw).strip().lower() != "inactive"
    return str(row.get("level", "")).upper() not in _PROHIBITION_OFF


def closure_cards(root: Path = None, errors: list = None) -> list:
    """마감 카드 전수 → `[{path, 범위, 금지, 근거, 확정값}]`.

    ⛔ **못 읽은 카드는 조용히 건너뛰지 않는다** (Codex BI-4 P0-1). `errors` 를 주면
    거기에 사유를 적고, 호출자는 그것을 `policy_error` 로 승격해야 한다.
    """
    base = Path(root) if root else REPO
    errs = errors if errors is not None else []
    d_props = base / "db/properties"
    if not d_props.is_dir():
        errs.append(f"마감 카드 디렉터리가 없다: {d_props}")
        return []
    out = []
    for f in sorted(d_props.glob("*closed*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            errs.append(f"마감 카드를 못 읽었다: {f.name} — {type(e).__name__}: {e}")
            continue
        if not isinstance(d, dict):
            errs.append(f"마감 카드가 객체가 아니다: {f.name} — {type(d).__name__}")
            continue
        out.append({"path": f.relative_to(base).as_posix(),
                    "범위": d.get("닫는_범위") or d.get("scope") or "",
                    "금지": d.get("금지_서술") or [],
                    "근거": d.get("근거_파일") or [],
                    "확정값": d.get("확정값") or {}})
    return out


def _resolve_target(base: Path, target) -> Path | None:
    """`target` 을 **실재하는 파일**로 붙인다. 못 붙이면 `None`.

    셋을 차례로 본다 — ① 절대경로 그대로 ② `base` 기준 상대경로
    ③ `base/db` 안에서 **같은 이름**(근거_파일 꼬리 라벨 때문에 이름 매칭이 필요하다).

    ⛔ 못 하는 것: 같은 이름이 db/ 안에 둘 이상이면 **어느 쪽인지 안 가린다** —
    실재 여부만 확인하는 함수다. 정책 판정 자체가 이름 기반이라 그 이상은 의미가 없다.
    """
    s = str(target).strip()
    if not s:
        return None
    p = Path(s)
    if p.is_absolute() and p.is_file():
        return p
    if (base / p).is_file():
        return base / p
    db = base / "db"
    if db.is_dir():
        for hit in db.rglob(p.name):
            if hit.is_file():
                return hit
    return None


def policy_for_file(target, root: Path = None) -> dict:
    """이 원자료가 **마감/금지에 걸리는가** → `{state, closed, cards, hazards, why, errors}`.

    `state` 는 셋이다 (Codex BI-4 P0-1 — 종전에는 둘이었고 그게 결함이었다):

    | state | 뜻 | 소비 |
    |---|---|---|
    | `open` | **금지가 없음을 확인했다** | 허용 |
    | `closed` | 마감 카드나 살아있는 금지에 걸린다 | ⛔ 금지 |
    | `policy_error` | **금지를 확인할 수 없다** (원장 누락·손상·읽기 실패) | ⛔ 금지 |

    ⇒ *"못 읽었다"* 는 *"없다"* 가 아니다. `closed` 는 **`state != "open"`** 인 파생 bool 이라
    이 값을 그대로 보던 호출자는 자동으로 fail-closed 된다.

    `target` 은 repo 상대경로든 절대경로든 파일명이든 받는다 — 이름으로 맞춘다
    (근거_파일 항목이 `"db/properties/x.json ⛔라벨"` 처럼 꼬리를 달고 있어서).

    ⛔ 그런데 **그 이름의 파일이 실재해야 한다** (2026-09-09). 못 붙이면 `policy_error` 다 —
    없는 파일에 *"금지가 없음을 확인했다"* 를 찍던 것이 이 함수의 결함이었다.
    """
    base = Path(root) if root else REPO
    name = Path(str(target)).name
    errors: list = []
    if not _resolve_target(base, target):
        errors.append(f"대상 파일을 못 찾았다: {target} — 이름으로도 db/ 안에 없다 "
                      "(오타이거나 지워진 파일이다)")
    cards = [c for c in closure_cards(base, errors=errors)
             if any(name in str(g) for g in c["근거"]) or name in str(c["범위"])]

    haz = []
    hz = base / "db/properties/citation_hazards.json"
    if not hz.is_file():
        errors.append(f"인용위험 원장이 없다: {hz}")
    else:
        try:
            doc = json.loads(hz.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            errors.append(f"인용위험 원장을 못 읽었다: {hz.name} — {type(e).__name__}: {e}")
            doc = None
        if doc is not None:
            if not isinstance(doc, dict) or not isinstance(doc.get("hazards"), list):
                errors.append(f"인용위험 원장 모양이 아니다: {hz.name} "
                              "— `hazards` 배열이 없다")
            else:
                for z in doc["hazards"]:
                    if not isinstance(z, dict):
                        errors.append(f"인용위험 행이 객체가 아니다: {type(z).__name__}")
                        continue
                    if name in str(z.get("file", "")) and _prohibition_active(z):
                        haz.append({"id": z.get("id"), "level": z.get("level"),
                                    "what": z.get("what"), "fix": z.get("fix")})

    why = [f"마감 카드 `{c['path']}` — {str(c['범위'])[:120]}" for c in cards]
    why += [f"인용위험 `{h['id']}` ({h['level']}) — {str(h['what'])[:110]}" for h in haz]

    if cards or haz:
        state = "closed"
    elif errors:
        state = "policy_error"          # ⛔ 확인 불가 ≠ 금지 없음
        why += [f"⛔ 정책을 확인할 수 없다 — {e}" for e in errors]
    else:
        state = "open"
    return {"state": state, "closed": state != "open", "cards": cards,
            "hazards": haz, "why": why, "errors": errors}


def axis_blocked(claim_id: str, root: Path = None) -> list:
    """이 claim 을 덮는 **축 단위 금지** → `[{id, level, why, fix}]` (Codex BI-4 Q5).

    소비자가 **claim 이름으로** 물을 수 있게 한다 — `policy_for_file` 은 파일 단위라
    *"이 파일의 어느 양을 쓰려는가"* 를 모른다. 축은 그 질문에 답한다.

    ⛔ 못 하는 것: `webapp/canonical.py` 의 `axis_covers` 와 **같은 규칙을 두 번 구현**한다.
      (webapp 을 import 하면 flask 의존이 따라온다.) 규칙이 갈라지지 않도록
      `--selftest` 가 양쪽 판정을 같은 픽스처로 대조한다.
    """
    base = Path(root) if root else REPO
    try:
        rows = json.loads((base / "db/properties/citation_hazards.json")
                          .read_text(encoding="utf-8")).get("hazards", [])
    except (OSError, ValueError):
        return [{"id": None, "level": "POLICY_ERROR",
                 "why": "인용위험 원장을 못 읽었다 — 확인 불가는 통과가 아니다", "fix": ""}]
    metric, _, system = str(claim_id or "").partition("@")
    parts = [p for p in metric.split("_") if p]
    t_sys, t_meth = system.lower(), (parts[0] if parts else "").upper()
    t_q = {p.lower() for p in parts[1:]} | {metric.lower()}
    out = []
    for z in rows:
        ax = z.get("prohibition_axis") if isinstance(z, dict) else None
        if not isinstance(ax, dict) or not _prohibition_active(z):
            continue
        s = str(ax.get("system", "")).lower()
        if not s or s not in t_sys:
            continue
        m = str(ax.get("method", "")).upper().replace("-", "_")
        if m and not any(x and x == t_meth for x in m.split("_")):
            continue
        qs = {str(q).lower() for q in (ax.get("quantity_group") or [])}
        if qs & t_q:
            out.append({"id": z.get("id"), "level": z.get("level"),
                        "why": z.get("why", ""), "fix": z.get("fix", "")})
    return out


def require_open(target, override: bool = False, what: str = "", root: Path = None) -> str:
    """닫힌 축이면 **시작하지 않는다**. `override` 면 경고를 찍고 스탬프를 돌려준다.

    돌려주는 스탬프 문자열은 호출자가 **출력·json 에 박아야** 한다 — 우회한 사실이
    산출물에 남지 않으면 우회는 조용한 위반이 된다.
    """
    p = policy_for_file(target, root=root)
    if p["state"] == "open":
        return ""
    err = p["state"] == "policy_error"
    head = (f"⛔ 이 원자료의 **정책을 확인할 수 없다**: {Path(str(target)).name}"
            if err else
            f"⛔ 이 원자료는 **마감·금지된 축**이다: {Path(str(target)).name}")
    body = "\n".join("   · " + w for w in p["why"])
    if not override:
        print(head, file=sys.stderr)
        print(body, file=sys.stderr)
        if err:
            print("   ⇒ **확인 불가는 허용이 아니다.** 원장을 고친 뒤 다시 오거나,\n"
                  "      이력·진단 목적이면 사유를 대고 넘겨라:", file=sys.stderr)
        else:
            print("   ⇒ 시작하지 않는다. 이력·진단 목적이면 사유를 대고 넘겨라:",
                  file=sys.stderr)
        print("      --policy_override \"<왜 그래도 돌리는가>\"", file=sys.stderr)
        raise SystemExit(2)
    kind = "정책을 **확인하지 못한 채**" if err else "마감된 축을 **우회해서**"
    stamp = (f"⛔ {kind} 낸 값이다 — 인용 금지. "
             f"사유: {override if isinstance(override, str) else what or '미기재'} · "
             f"근거: {' / '.join(p['why'])}")
    print(head, file=sys.stderr)
    print(body, file=sys.stderr)
    print("   ⚠ --policy_override 로 통과. 산출물에 스탬프를 박는다.", file=sys.stderr)
    return stamp


def _selftest() -> int:
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        (r / "db/properties").mkdir(parents=True)
        (r / "db/properties/x_closed_2026_01_01.json").write_text(json.dumps({
            "닫는_범위": "x 축 전체", "금지_서술": ["⛔ 아무것도 인용 금지"],
            "근거_파일": ["db/properties/x_data.json ⛔라벨"]}, ensure_ascii=False),
            encoding="utf-8")
        (r / "db/properties/citation_hazards.json").write_text(json.dumps({"hazards": [
            {"id": "HZ-y", "level": "SUPERSEDED", "file": "db/properties/y_data.json",
             "what": "규칙은 폐기됐지만 인용은 여전히 금지"},
            {"id": "HZ-z", "level": "RESOLVED", "file": "db/properties/z_data.json",
             "what": "해소됨"},
        ]}, ensure_ascii=False), encoding="utf-8")
        # 대상 파일들이 **실재해야** 한다 (2026-09-09 규칙) — 픽스처가 원장만 만들고
        # 원자료를 안 만들던 것이 종전 selftest 의 공백이었다.
        for n in ("x_data.json", "y_data.json", "z_data.json", "unrelated.json"):
            (r / "db/properties" / n).write_text("{}", encoding="utf-8")

        # ⛔음성 ①: 마감 카드가 가리키는 원자료를 못 잡으면 실패
        if not policy_for_file("db/properties/x_data.json", root=r)["closed"]:
            print("⛔ selftest: 마감 카드가 가리키는 파일을 못 잡았다"); ok = False
        # ⛔음성 ②: **SUPERSEDED 라도 금지는 살아 있다** (BI-3 P0-1 과 같은 규칙)
        if not policy_for_file("y_data.json", root=r)["closed"]:
            print("⛔ selftest: SUPERSEDED 인데 금지를 껐다 — P0-1 재발"); ok = False
        # ⛔음성 ③: RESOLVED 는 통과해야 한다 (과잉차단도 결함이다)
        if policy_for_file("z_data.json", root=r)["closed"]:
            print("⛔ selftest: RESOLVED 를 막았다 — 과잉차단"); ok = False
        # ⛔음성 ④: 무관한 파일을 막으면 실패
        if policy_for_file("db/properties/unrelated.json", root=r)["closed"]:
            print("⛔ selftest: 무관한 파일을 막았다"); ok = False
        # ⛔음성 ⑤: 닫힌 축은 **시작하지 않아야** 한다
        try:
            require_open("x_data.json", root=r)
            print("⛔ selftest: 닫힌 축인데 그냥 통과했다"); ok = False
        except SystemExit:
            pass
        # ⛔음성 ⑥: override 는 **스탬프를 돌려줘야** 한다 (조용한 우회 금지)
        s = require_open("x_data.json", override="진단 목적", root=r)
        if "인용 금지" not in s or "진단 목적" not in s:
            print("⛔ selftest: override 스탬프가 사유·금지를 안 담았다:", s); ok = False
        # ⛔음성 ⑦: 정상 파일은 state 가 정확히 open 이어야 한다
        if policy_for_file("z_data.json", root=r)["state"] != "open":
            print("⛔ selftest: 정상인데 open 이 아니다"); ok = False

        # ── 2026-09-09: **없는 파일에 ✅ 를 주던 구멍** (BI-4 P0-1 재발) ──────
        # ⛔음성 ⑮: 실재하지 않는 대상은 open 이면 안 된다
        p = policy_for_file("db/properties/없는파일.json", root=r)
        if p["state"] != "policy_error":
            print(f"⛔ selftest: 없는 파일인데 state={p['state']} — "
                  "'못 찾았다' 가 '금지 없다' 가 됐다"); ok = False
        if not p["closed"]:
            print("⛔ selftest: 없는 파일인데 closed=False — 옛 호출자가 그냥 통과한다")
            ok = False
        # ⛔음성 ⑯: require_open 이 **시작을 막아야** 한다
        try:
            require_open("없는파일.json", root=r)
            print("⛔ selftest: 없는 파일인데 require_open 이 통과시켰다"); ok = False
        except SystemExit:
            pass
        # ⛔음성 ⑰: 실재하는 무관한 파일은 **여전히 open** (과잉차단도 결함이다)
        if policy_for_file("unrelated.json", root=r)["state"] != "open":
            print("⛔ selftest: 실재하는 무관한 파일을 막았다 — 과잉차단"); ok = False
        # ⛔음성 ⑱: db/ 아무 데나 있어도 이름으로 찾아야 한다 (하위 폴더)
        (r / "db/structures").mkdir(parents=True, exist_ok=True)
        (r / "db/structures/깊은곳.json").write_text("{}", encoding="utf-8")
        if policy_for_file("깊은곳.json", root=r)["state"] != "open":
            print("⛔ selftest: db/ 하위 폴더 파일을 못 찾았다"); ok = False

    # ── Codex BI-4 P0-1: **못 읽음 ≠ 금지 없음** ────────────────────────────
    hz = "db/properties/citation_hazards.json"
    for 이름, 만들기 in (
        ("원장 없음", lambda r: None),
        ("원장 JSON 깨짐", lambda r: (r / hz).write_text("{ 깨진", encoding="utf-8")),
        ("원장 모양 아님", lambda r: (r / hz).write_text('{"nope": 1}', encoding="utf-8")),
        ("hazards 가 배열 아님", lambda r: (r / hz).write_text('{"hazards": {}}',
                                                              encoding="utf-8")),
    ):
        with tempfile.TemporaryDirectory() as d:
            r = Path(d); (r / "db/properties").mkdir(parents=True)
            만들기(r)
            p = policy_for_file("무관한.json", root=r)
            # ⛔음성 ⑧–⑪: 확인 불가가 open 으로 새면 실패
            if p["state"] != "policy_error":
                print(f"⛔ selftest: {이름} 인데 state={p['state']} — 확인 불가가 허용이 됐다")
                ok = False
            if not p["closed"]:
                print(f"⛔ selftest: {이름} 인데 closed=False — 옛 호출자가 그냥 통과한다")
                ok = False
            # ⛔음성 ⑫: require_open 이 **시작을 막아야** 한다
            try:
                require_open("무관한.json", root=r)
                print(f"⛔ selftest: {이름} 인데 require_open 이 통과시켰다"); ok = False
            except SystemExit:
                pass
            # ⛔음성 ⑬: override 스탬프가 **'확인 못 했다'** 를 말해야 한다
            s = require_open("무관한.json", override="진단", root=r)
            if "확인하지 못한" not in s:
                print(f"⛔ selftest: {이름} override 스탬프가 마감 우회처럼 말한다: {s[:80]}")
                ok = False

    # ⛔음성 ⑭: db/properties 디렉터리 자체가 없으면 policy_error
    with tempfile.TemporaryDirectory() as d:
        if policy_for_file("무관한.json", root=Path(d))["state"] != "policy_error":
            print("⛔ selftest: db/properties 가 없는데 policy_error 가 아니다"); ok = False

    # ── 축 단위 금지 상속 (Codex BI-4 Q5) ──────────────────────────────────
    with tempfile.TemporaryDirectory() as d:
        r = Path(d); (r / "db/properties").mkdir(parents=True)
        (r / "db/properties/citation_hazards.json").write_text(json.dumps({"hazards": [{
            "id": "HZ-ax", "level": "BLOCKED", "file": "db/properties/q.json",
            "what": "축 전체", "prohibition_axis": {
                "system": "b2o3", "method": "UMA-MD",
                "quantity_group": ["d", "ea", "sigma", "ratio"]}}]},
            ensure_ascii=False), encoding="utf-8")
        for cid, want, 이름 in (
            ("MD_Ea_eV@b2o3", True, "레지스트리에 있는 claim"),
            ("MD_D_cm2s@b2o3", True, "★레지스트리에 **없는** claim (축을 넣은 이유)"),
            ("MD_sigma_300K@b2o3", True, "★없는 파생량"),
            ("MD_sigma_ratio_600K@b2o3_vs_modelc", True, "비교 claim"),
            ("gap_eV@b2o3", False, "⛔음성: 같은 계의 **다른 방법**(0 K DFT)"),
            ("B0_GPa@b2o3", False, "⛔음성: 같은 계의 **다른 양**"),
            ("MD_Ea_eV@modelc", False, "⛔음성: 같은 양의 **다른 계**"),
        ):
            got = bool(axis_blocked(cid, root=r))
            if got != want:
                print(f"⛔ selftest 축: {이름} — {cid} → {got} (기대 {want})"); ok = False
        # ⛔음성: 원장을 못 읽으면 **POLICY_ERROR 를 낸다** (빈 목록 = 통과가 아니다)
        (r / "db/properties/citation_hazards.json").write_text("{깨진", encoding="utf-8")
        b = axis_blocked("MD_Ea_eV@b2o3", root=r)
        if not b or b[0].get("level") != "POLICY_ERROR":
            print("⛔ selftest 축: 원장을 못 읽었는데 통과했다 —", b); ok = False

    # ⛔ 두 구현이 갈라지지 않는가 — webapp/canonical.py 와 **같은 판정**이어야 한다
    try:
        import importlib.util as _ilu
        _sp = _ilu.spec_from_file_location("_c4x", REPO / "webapp/canonical.py")
        _c = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_c)
    except Exception as _e:                                          # noqa: BLE001
        print(f"   ⚠ webapp/canonical.py 대조 생략 ({type(_e).__name__}) — "
              "두 구현이 갈라져도 여기서 못 잡는다")
    else:
        for cid in ("MD_Ea_eV@b2o3", "MD_D_cm2s@b2o3", "MD_sigma_300K@b2o3",
                    "gap_eV@b2o3", "B0_GPa@b2o3", "MD_Ea_eV@modelc",
                    "MD_sigma_ratio_600K@b2o3_vs_modelc"):
            a, b = bool(axis_blocked(cid)), bool(_c.axis_blocked(cid))
            if a != b:
                print(f"⛔ selftest: 두 구현이 갈라졌다 — {cid}: policy={a} canonical={b}")
                ok = False

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", help="db/properties 의 원자료")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.path:
        ap.error("파일을 주거나 --selftest 를 써라")
    p = policy_for_file(a.path)
    label = {"open": "✅ 열려 있음 (금지가 **없음을 확인**)",
             "closed": "⛔ 닫힘/금지",
             "policy_error": "⛔ 정책 확인 불가 — **허용이 아니다**"}[p["state"]]
    print(f"{Path(a.path).name} → {label}")
    for w in p["why"]:
        print("   ·", w)
    return 0 if p["state"] == "open" else (1 if p["state"] == "closed" else 3)


if __name__ == "__main__":
    sys.exit(main())
