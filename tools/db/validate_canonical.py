#!/usr/bin/env python3
"""validate_canonical.py — 정본 레지스트리가 **원자료와 실제로 일치하는지** 검사한다.

왜 필요한가
  레지스트리를 만든 목적이 "db 를 고치면 화면이 갱신된다" 인데, 레지스트리 값과 원자료가
  따로 놀면 문제를 딕셔너리에서 JSON 으로 옮긴 것뿐이다. 그래서 항목마다 적힌
  (source_path, source_key) 를 **실제로 따라가서** 값을 대조한다.

  python3 tools/db/validate_canonical.py           # 검사
  python3 tools/db/validate_canonical.py --show    # 그룹별 정본표까지
  종료코드 0 = 통과 · 1 = 불일치 (CI 에서 이걸 본다)
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "webapp"))
import canonical as C  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="그룹별 정본표도 출력")
    a = ap.parse_args()

    reg = C.load_registry()
    ents = reg.get("entries", [])
    if not ents:
        print("⛔ 레지스트리가 비었다 — db/properties/canonical_registry.json 확인")
        return 1

    by_status = {}
    for e in ents:
        by_status[e.get("status", "?")] = by_status.get(e.get("status", "?"), 0) + 1
    print(f"항목 {len(ents)}개  ·  " + " · ".join(f"{k} {v}" for k, v in sorted(by_status.items())))

    bad = C.validate(reg)
    wired = [e for e in ents if e.get("source_path")]
    print(f"출처 배선 {len(wired)}/{len(ents)}  ·  대조 실패 {len(bad)}")

    if bad:
        print("\n⛔ 원자료와 어긋나는 항목")
        for e, why in bad:
            print(f"   {e.get('metric'):22s} {e.get('system'):18s} {why}")

    pend = [e for e in ents if e.get("status") == "source_pending"]
    if pend:
        print(f"\n⚠ 출처 미배선 {len(pend)}개 — 값은 쓰되 **검증되지 않는다**")
        for e in pend:
            print(f"   {e.get('metric'):22s} {e.get('system'):18s} {(e.get('note') or '')[:70]}")

    if a.show:
        metrics = sorted({e.get("metric") for e in ents})
        for m in metrics:
            print(f"\n══ {m}")
            for g, es in sorted(C.groups_of(reg, m).items()):
                print(f"   [{g}]")
                for e in sorted(es, key=lambda x: (x.get("value") is None, x.get("value"))):
                    u = f" ± {e['uncertainty']}" if e.get("uncertainty") is not None else ""
                    ns = f" n_seed={e['n_seed']}" if e.get("n_seed") else ""
                    st = "" if e.get("status") == "canonical" else f"  <{e.get('status')}>"
                    print(f"     {e['system']:18s} {e.get('value')}{u}{ns}{st}")
            print("   ⚠ 순위·최저값·레이더는 **한 [group] 안에서만** 유효하다.")

    if bad:
        print("\n판정: ⛔ 실패 — 레지스트리를 고치거나 원자료를 확인할 것")
        return 1
    print("\n판정: ✅ 배선된 항목은 전부 원자료와 일치")
    return 0


if __name__ == "__main__":
    sys.exit(main())
