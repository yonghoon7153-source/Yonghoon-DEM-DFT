#!/usr/bin/env python3
"""prereg_ratify.py — 사전등록을 **내용 변경 없이 재비준**한다 (1저자 결정 뒤에만).

왜 별도 도구인가
  `c12_prereg_amend_kconv.py` 는 C-12 전용이고 **내용을 고치는** 도구다(개정 + 비준).
  이건 다른 일이다: 리뷰 지적을 코드로 고치면 봉인 대상(빌더 SHA 등)이 바뀌고,
  그러면 사전등록 내용이 바뀌어 `content_digest` 가 어긋나 게이트가 재승인을 요구한다.
  **문서는 이미 맞고 도장만 다시 찍으면 되는** 상황이다.
  폴라론 S0 만 해도 회신 Y·Z·Z-2·Z-3 로 네 번 필요했다.

  python3 tools/sdcp/prereg_ratify.py --prereg db/properties/<x>.json --decision D-... --ratify
  python3 tools/sdcp/prereg_ratify.py --prereg <x> --decision <id>          # 미리보기(쓰지 않음)
  python3 tools/sdcp/prereg_ratify.py --selftest

⛔ 이 도구가 **못 하는 것**
  · 과학적 타당성을 판정하지 않는다. 문서가 옳은지는 사람이 본다.
  · **내용을 고치지 않는다.** 고쳐야 하면 그건 개정이고 다른 도구/손이다.
  · 코드가 실제로 고쳐졌는지 확인하지 않는다 — 그건 그 도구의 `--selftest` 몫이다.
    (그래서 `--ratify` 전에 해당 selftest 를 **직접 돌려 보고** 오라고 화면에 적는다.)
  · 어느 결정이 어느 사전등록에 걸리는지 추론하지 않는다. `--decision` 으로 명시해야 한다.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve()
while not ((REPO / "db" / "properties").is_dir() and (REPO / "db" / "governance").is_dir()):
    REPO = REPO.parent
    if REPO == REPO.parent:
        raise SystemExit("repo 루트를 못 찾았다 (db/properties + db/governance 가 있는 곳)")
DEC = REPO / "db/governance/decisions.json"
BY = "yonghoon7153@gmail.com"


def content_digest(doc: dict) -> str:
    """`ratification` 을 **뺀** 내용의 sha256.

    ⚠ 이 함수의 계약: 비준 블록은 지문의 대상이 아니다. 그래야 "지문을 기록하는 행위"가
      지문을 바꾸지 않는다. C-12 쪽 `prereg_digest` 와 같은 규약이다 — 갈라지면 안 된다.
    """
    c = {k: v for k, v in doc.items() if k != "ratification"}
    return hashlib.sha256(json.dumps(c, sort_keys=True, ensure_ascii=False)
                          .encode("utf-8")).hexdigest()


def decision_digest(d: dict) -> str:
    c = {k: v for k, v in d.items() if k != "ratification"}
    return hashlib.sha256(json.dumps(c, sort_keys=True, ensure_ascii=False)
                          .encode("utf-8")).hexdigest()


def ratify_doc(doc: dict, today: str, now: str, head: str, note: str) -> dict:
    """문서를 비준 상태로 만든다. **지문은 맨 마지막에** 계산한다.

    🔴 렌즈6′ P0 (C-12 에서 실측된 함정) — 지문을 먼저 뽑고 그 다음 status/history 를
      고치면 기록된 지문이 최종 문서와 어긋난다. 그러면 게이트가 "비준 이후 내용이
      바뀌었다"로 읽어 ratified=False 가 되고, 그 문서로 만든 산출물이 전부 막힌다.
    """
    doc.setdefault("status_history", []).append(
        {"at": today, "state": "ratified", "note": note})
    doc["status"] = "ratified"
    doc.pop("ratification", None)               # 지문 대상에서 확실히 뺀다
    doc["ratification"] = {
        "state": "ratified", "role": "scientific_owner", "at": today, "by": "1저자",
        "content_digest": content_digest(doc),   # ← 마지막에, 최종 내용으로
        "actor_id": BY, "timestamp": now, "commit": head,
        "⛔_무엇에_대한_비준인가": ("이 문서에서 `ratification` 을 뺀 내용의 sha256 이다. "
                                    "한 글자라도 바뀌면 지문이 달라지고 게이트가 재승인을 "
                                    "요구한다 — 비준을 받아 놓고 내용을 고치는 경로를 닫는다."),
        "⚠_base_commit_이_아니다": ("`commit` 은 기록일 뿐 앵커가 아니다. 앵커는 위 digest 다."),
    }
    if doc["ratification"]["content_digest"] != content_digest(doc):
        raise SystemExit("⛔ 내부 오류: 기록 digest ≠ 최종 문서 digest")
    return doc


def _selftest() -> int:
    """⛔ 음성 포함. 양성만 있는 selftest 는 통과해도 아무것도 보증하지 못한다 (CLAUDE.md)."""
    import copy
    n = [0, 0]

    def chk(c, m):
        n[0] += 1
        n[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    base = {"schema": "prereg/v1", "status": "proposed", "대상": {"x": 1},
            "status_history": [{"at": "2026-09-01", "state": "proposed"}]}

    d1 = ratify_doc(copy.deepcopy(base), "2026-09-04", "T", "abc", "n")
    chk(d1["status"] == "ratified" and d1["ratification"]["state"] == "ratified",
        "양성: 비준하면 status·ratification 이 ratified 다")
    chk(d1["ratification"]["content_digest"] == content_digest(d1),
        "양성: 기록 지문이 **최종 문서**의 지문과 같다")
    chk(len(d1["status_history"]) == 2 and d1["status_history"][-1]["state"] == "ratified",
        "이력이 덧붙는다 (덮어쓰지 않는다)")

    # ⛔음성 — 지문을 **먼저** 뽑는 옛 방식이면 어긋난다 (렌즈6′ P0 회귀)
    d2 = copy.deepcopy(base)
    early = content_digest(d2)
    d2["status_history"].append({"at": "2026-09-04", "state": "ratified"})
    d2["status"] = "ratified"
    d2["ratification"] = {"content_digest": early}
    chk(content_digest(d2) != early,
        "⛔음성: 지문을 먼저 뽑고 status/history 를 고치면 **어긋난다** — 그래서 마지막에 계산한다")

    chk(content_digest({"a": 1}) == content_digest({"a": 1, "ratification": {"z": 9}}),
        "지문은 `ratification` 칸을 뺀 내용의 것이다")
    # ⛔음성 — 내용이 한 글자만 달라도 지문이 달라진다
    chk(content_digest({"a": 1}) != content_digest({"a": 2}),
        "⛔음성: 내용이 바뀌면 지문이 달라진다 (그게 재승인을 강제하는 장치다)")
    # ⛔음성 — 비준을 두 번 해도 두 번째 지문이 첫 번째와 다르다(이력이 늘므로)
    d3 = ratify_doc(copy.deepcopy(d1), "2026-09-05", "T2", "def", "n2")
    chk(d3["ratification"]["content_digest"] != d1["ratification"]["content_digest"],
        "⛔음성: 재비준하면 이력이 늘어 지문이 **달라진다** (같으면 이력을 안 쓴 것이다)")
    chk(d3["ratification"]["content_digest"] == content_digest(d3),
        "재비준본도 자기 지문과 맞는다")

    chk(DEC.is_file(), "decisions.json 경로 해석이 맞다 (%s)" % DEC)
    print("selftest %d/%d · %s" % (n[1], n[0], "PASS" if n[1] == n[0] else "FAIL"))
    return 0 if n[1] == n[0] else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--prereg", required=True, help="db/properties/<...>.json")
    ap.add_argument("--decision", required=True, help="decisions.json 의 결정 id")
    ap.add_argument("--note", default="", help="status_history 에 남길 사유")
    ap.add_argument("--ratify", action="store_true", help="1저자 '비준' 뒤에만")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    pre_p = pathlib.Path(a.prereg)
    if not pre_p.is_absolute():
        pre_p = REPO / a.prereg
    if not pre_p.is_file():
        raise SystemExit("⛔ 사전등록이 없다: %s" % pre_p)
    pre = json.loads(pre_p.read_text(encoding="utf-8"))
    dec = json.loads(DEC.read_text(encoding="utf-8"))
    tgt = next((d for d in dec["decisions"] if d.get("id") == a.decision), None)
    if tgt is None:
        raise SystemExit("⛔ 결정 id 를 못 찾았다: %s" % a.decision)
    # ⛔ 결정이 이 사전등록을 가리키는지 **확인한다** — 엉뚱한 문서에 도장 찍는 경로를 닫는다.
    rec = str(tgt.get("record") or "")
    if pre_p.name not in rec:
        raise SystemExit("⛔ 결정 %s 의 record 가 이 사전등록이 아니다:\n   record = %s\n   prereg = %s"
                         % (a.decision, rec, pre_p.name))

    old_dig = (pre.get("ratification") or {}).get("content_digest")
    now_dig = content_digest(pre)
    print("사전등록 : %s" % pre_p.relative_to(REPO))
    print("  status         : %s" % pre.get("status"))
    print("  기록된 digest  : %s" % old_dig)
    print("  현재  digest   : %s" % now_dig)
    print("  일치           : %s" % (old_dig == now_dig))
    print("결정     : %s (%s)" % (tgt["id"], tgt.get("status")))
    if old_dig == now_dig and pre.get("status") in ("ratified", "active") \
            and tgt.get("status") in ("active",):
        print("→ 이미 비준돼 있고 지문도 맞는다. 할 일이 없다.")
        return 0
    if not a.ratify:
        print("\n(미리보기 — 아무것도 쓰지 않았다. 실제로 찍으려면 --ratify)")
        print("⚠ 찍기 전에 해당 도구의 `--selftest` 를 **직접 돌려 보라** — 이 도구는 "
              "코드가 고쳐졌는지 확인하지 않는다.")
        return 0

    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    note = a.note or ("1저자 비준 (scientific_owner) — 내용 변경 없는 **재비준**. "
                      "리뷰 이행으로 봉인 대상이 바뀌어 지문이 어긋나 있었다.")
    pre = ratify_doc(pre, a.date, now, head, note)
    pre_p.write_text(json.dumps(pre, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    tgt["status"] = "active"
    tgt["decision_state"] = "active"
    tgt.setdefault("status_history", []).append(
        {"at": a.date, "state": "active",
         "note": "1저자 비준 (scientific_owner). 사전등록 재봉인과 함께."})
    tgt.pop("ratification", None)
    tgt["ratification"] = {
        "state": "ratified", "role": "scientific_owner", "actor_id": BY,
        "timestamp": now, "commit": head,
        "decision_digest": "sha256:" + decision_digest(tgt),
        "⚠_digest_의_뜻": "`ratification` 을 뺀 결정 내용의 sha256 이다.",
    }
    DEC.write_text(json.dumps(dec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print("\n→ %s : status %s" % (pre_p.name, pre["status"]))
    print("   content_digest  = %s" % pre["ratification"]["content_digest"])
    print("→ %s : %s → %s" % (DEC.name, tgt["id"], tgt["status"]))
    print("   decision_digest = %s" % tgt["ratification"]["decision_digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
