#!/usr/bin/env python3
"""validate_canonical.py — 정본 레지스트리가 **원자료와 실제로 일치하는지** 검사한다.

왜 필요한가
  레지스트리를 만든 목적이 "db 를 고치면 화면이 갱신된다" 인데, 레지스트리 값과 원자료가
  따로 놀면 문제를 딕셔너리에서 JSON 으로 옮긴 것뿐이다. 그래서 항목마다 적힌
  (source_path, source_key) 를 **실제로 따라가서** 값을 대조한다.

  python3 tools/db/validate_canonical.py           # 앵커 검사
  python3 tools/db/validate_canonical.py --show    # 그룹별 정본표까지
  python3 tools/db/validate_canonical.py --audit   # **db 전체** 신선도 감사
  python3 tools/db/validate_canonical.py --selftest
  종료코드 0 = 통과 · 1 = 불일치 (CI 에서 이걸 본다)

--audit 이 보는 것 (2026-08-12 추가)
  앵커 검사는 레지스트리에 **배선된 28항목**만 본다. db/properties 는 196개다.
  나머지 168개가 최신인지, 채울 자리가 남았는지는 아무도 안 봤다. 세 가지를 본다:
    ① 날짜 필드가 없다      → 최신인지 판단할 근거가 없다 (76 중 45가 그랬다)
    ② source 경로가 죽었다  → 원자료를 못 따라간다 = 재현 불가
    ③ null/None 값이 있다   → **채울 자리**다 (예: sei_formation_voltage 의 Nd 3종)
    ④ superseded 쌍         → 같은 파일에 `X` 와 `X_frozen4f` 처럼 구판·신판이 공존

이 도구가 **못 하는 것**
  · 숫자가 물리적으로 맞는지는 모른다. "언제 것인지·따라갈 수 있는지"만 본다.
  · ③ null 이 전부 결함은 아니다 — 의도적 미측정도 null 이다. **후보**로만 낸다.
"""
import argparse
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "webapp"))
import canonical as C  # noqa: E402


REPO = pathlib.Path(__file__).resolve().parents[2]
PROPS = REPO / "db" / "properties"
DATE_KEYS = ("collected", "date", "generated", "updated", "run_date", "collected_at")
SRC_KEYS = ("source", "source_dir", "source_path", "source_file", "from", "inputs")
#: 같은 파일 안에서 구판/신판이 공존하는 접미사 — 뒤엣것이 신판이다
SUPERSEDE_SUFFIX = ("_frozen4f", "_v2", "_v3", "_rerun", "_fixed", "_mto")


def _paths_in(v, out):
    """값 안의 경로처럼 생긴 문자열을 긁는다 (문자열·리스트·딕셔너리 재귀)."""
    if isinstance(v, str):
        for m in re.finditer(r"[\w./~-]*(?:runs|db|tools|/data/work)/[\w./#-]+", v):
            s = m.group(0).rstrip(".,)")
            if len(s) > 6:
                out.add(s)
    elif isinstance(v, dict):
        for x in v.values():
            _paths_in(x, out)
    elif isinstance(v, (list, tuple)):
        for x in v[:40]:
            _paths_in(x, out)


def _nulls_in(v, path="", out=None, cap=6):
    """null 인 잎(leaf)의 경로들 — **채울 자리** 후보."""
    out = [] if out is None else out
    if len(out) >= cap:
        return out
    if v is None:
        out.append(path or "(root)")
    elif isinstance(v, dict):
        for k, x in v.items():
            _nulls_in(x, f"{path}.{k}" if path else str(k), out, cap)
    elif isinstance(v, list):
        for i, x in enumerate(v[:20]):
            _nulls_in(x, f"{path}[{i}]", out, cap)
    return out


def audit_file(f):
    """파일 하나의 감사 결과. (rec, 읽기실패사유) 를 낸다."""
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"{type(e).__name__}"
    try:
        rel = str(f.relative_to(REPO))
    except ValueError:
        rel = str(f)                      # selftest 의 임시 경로
    rec = {"file": rel, "kind": type(d).__name__}
    if not isinstance(d, dict):
        rec["date"] = None
        rec["notes"] = ["dict 가 아님 — 메타 필드를 못 단다"]
        return rec, None
    rec["date"] = next((str(d[k]) for k in DATE_KEYS if k in d), None)
    ps = set()
    for k in SRC_KEYS:
        if k in d:
            _paths_in(d[k], ps)
    rec["sources"] = sorted(ps)[:6]
    rec["dead_sources"] = [s for s in rec["sources"]
                           if s.startswith(("db/", "runs/", "tools/"))
                           and not (REPO / s).exists()]
    rec["nulls"] = _nulls_in(d.get("results", d))
    # 구판/신판 공존 — 같은 파일에서 X 와 X_frozen4f 가 같이 있으면 X 는 구판이다
    res = d.get("results")
    sup = []
    if isinstance(res, dict):
        for k in res:
            for sfx in SUPERSEDE_SUFFIX:
                if k.endswith(sfx) and k[:-len(sfx)] in res:
                    sup.append((k[:-len(sfx)], k))
    # ★ 구판/신판이 같이 있는 것 자체는 정상이다(경위 보존). 문제는 **표시가 없는**
    #   경우다 — 소비자(webapp·그림·원고)가 옛 값을 정본으로 읽는다.
    #   2026-08-12: sei_electronic 의 4f-in-valence 갭 3건이 그 상태였다.
    rec["superseded"] = sup
    rec["superseded_unmarked"] = [
        (o, n) for o, n in sup
        if not (isinstance(res.get(o), dict)
                and (str(res[o].get("status", "")).upper().startswith("DEPRECAT")
                     or res[o].get("superseded_by")
                     or res[o].get("canonical") is False))]
    return rec, None


def cmd_audit(show_all=False):
    """db/properties 전체 신선도 감사 — 요약이 기본, 목록은 --audit_all."""
    files = sorted(PROPS.rglob("*.json"))
    recs, broken = [], []
    for f in files:
        r, err = audit_file(f)
        if err:
            broken.append((str(f.relative_to(REPO)), err))
        else:
            recs.append(r)
    nodate = [r for r in recs if not r.get("date")]
    dead = [r for r in recs if r.get("dead_sources")]
    nulls = [r for r in recs if r.get("nulls")]
    sup = [r for r in recs if r.get("superseded")]
    unmarked = [r for r in recs if r.get("superseded_unmarked")]
    nosrc = [r for r in recs if r.get("kind") == "dict" and not r.get("sources")]
    print(f"=== db 신선도 감사 ===  json {len(files)}개 (읽기 실패 {len(broken)})")
    print(f"  ① 날짜 없음        {len(nodate):3d}  — 최신인지 판단 불가")
    print(f"  ② 출처 경로 없음    {len(nosrc):3d}  — 원자료를 못 따라간다")
    print(f"  ③ 죽은 출처 경로    {len(dead):3d}  — 적힌 경로가 사라졌다")
    print(f"  ④ null 값 있음      {len(nulls):3d}  — **채울 자리** 후보")
    print(f"  ⑤ 구판/신판 공존    {len(sup):3d}  (그중 **표시 없음** {len(unmarked)} "
          f"← 옛 값이 정본으로 읽힌다)")
    for r in broken:
        print(f"  ⛔ 읽기 실패 {r[0]} ({r[1]})")
    if unmarked:
        print("\n── ⑤ **표시 없는** 구판/신판 (여기부터 고친다) ──")
        for r in unmarked:
            for old, new in r["superseded_unmarked"]:
                print(f"  {r['file']}\n     {old}  ←구판?   {new}  ←신판?"
                      f"\n     고치는 법: 구판에 status='DEPRECATED' + superseded_by "
                      f"+ reason 을 달 것 (지우지 말고 표시한다)")
    elif sup:
        print(f"\n  ⑤ 공존 {len(sup)}건은 전부 DEPRECATED 표시가 되어 있다 ✓")
    if dead:
        print("\n── ③ 죽은 출처 ──")
        for r in dead[:10]:
            print(f"  {r['file']}  →  {r['dead_sources'][:2]}")
    if nulls:
        print(f"\n── ④ 채울 자리 후보 (상위 {'전부' if show_all else 12}) ──")
        for r in (nulls if show_all else nulls[:12]):
            print(f"  {r['file']:52s} {', '.join(r['nulls'][:3])}")
    if not show_all:
        print("\n  (전체 목록은 --audit_all · 날짜/출처 없는 파일 목록도 거기에)")
    if unmarked:
        print(f"\n⛔ 표시 없는 구판 {len(unmarked)}건 — exit 1")
        return 1
    else:
        print("\n── ① 날짜 없음 ──")
        for r in nodate:
            print(f"  {r['file']}")
        print("\n── ② 출처 없음 ──")
        for r in nosrc:
            print(f"  {r['file']}")
    return 0


def selftest():
    """양성 + **음성**. 감사기가 아무것도 못 잡으면 통과해도 의미가 없다."""
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok = ok and bool(c)

    td = pathlib.Path(tempfile.mkdtemp())
    (td / "good.json").write_text(json.dumps({
        "date": "2026-08-12", "source": "runs/x/y.out",
        "results": {"a": {"gap": 1.0}}}), encoding="utf-8")
    (td / "bad.json").write_text(json.dumps({
        "results": {"a": {"gap": None}, "a_frozen4f": {"gap": 2.0}},
        "source_dir": "runs/사라진경로"}), encoding="utf-8")
    (td / "broken.json").write_text("{not json", encoding="utf-8")
    g, e = audit_file(td / "good.json")
    chk(e is None and g["date"] == "2026-08-12", "날짜 회수")
    chk(not g["nulls"] and not g["superseded"], "정상 파일엔 아무것도 안 걸린다")
    b, e2 = audit_file(td / "bad.json")
    chk(e2 is None and b["date"] is None, "날짜 없음 감지")
    chk(b["nulls"] and "a.gap" in b["nulls"][0], f"null 잎 경로 회수 ({b['nulls'][:1]})")
    chk(b["superseded"] == [("a", "a_frozen4f")],
        f"구판/신판 공존 감지 ({b['superseded']})")
    chk(b["superseded_unmarked"] == [("a", "a_frozen4f")],
        "표시 없는 구판으로 잡는다")
    # ★ 음성: DEPRECATED 를 달면 **더는 안 걸려야** 한다 (안 그러면 고쳐도 계속 운다)
    (td / "marked.json").write_text(json.dumps({"results": {
        "a": {"gap": 1.0, "status": "DEPRECATED", "superseded_by": "a_frozen4f"},
        "a_frozen4f": {"gap": 2.0}}}), encoding="utf-8")
    mk, _ = audit_file(td / "marked.json")
    chk(mk["superseded"] and not mk["superseded_unmarked"],
        "DEPRECATED 표시하면 '표시 없음' 목록에서 빠진다")
    (td / "marked2.json").write_text(json.dumps({"results": {
        "a": {"gap": 1.0, "canonical": False}, "a_frozen4f": {"gap": 2.0}}}),
        encoding="utf-8")
    m2, _ = audit_file(td / "marked2.json")
    chk(not m2["superseded_unmarked"], "canonical:false 도 표시로 인정")
    chk(b["dead_sources"] == ["runs/사라진경로"], f"죽은 출처 감지 ({b['dead_sources']})")
    _, e3 = audit_file(td / "broken.json")
    chk(e3 is not None, f"깨진 json → 조용히 건너뛰지 않는다 ({e3})")
    # ★ 음성: 접미사가 있어도 **짝이 없으면** superseded 가 아니다
    (td / "solo.json").write_text(json.dumps(
        {"results": {"only_frozen4f": {"gap": 1.0}}}), encoding="utf-8")
    s, _ = audit_file(td / "solo.json")
    chk(s["superseded"] == [], "짝 없는 _frozen4f 는 구판/신판이 아니다")
    # ★ 음성: 존재하는 경로를 죽었다고 하면 안 된다
    (td / "live.json").write_text(json.dumps(
        {"source": "tools/db/validate_canonical.py"}), encoding="utf-8")
    lv, _ = audit_file(td / "live.json")
    chk(lv["dead_sources"] == [], f"살아 있는 경로는 안 잡는다 ({lv['sources']})")
    import shutil
    shutil.rmtree(td, ignore_errors=True)
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="그룹별 정본표도 출력")
    ap.add_argument("--audit", action="store_true",
                    help="db/properties **전체** 신선도 감사 (날짜·출처·null·구판)")
    ap.add_argument("--audit_all", action="store_true", help="--audit 의 전체 목록판")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.audit or a.audit_all:
        return cmd_audit(show_all=a.audit_all)

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
    nprov = sum(1 for e in ents if e.get("provenance_open"))
    print(f"출처 배선 {len(wired)}/{len(ents)}  ·  대조 실패 {len(bad)}"
          + (f"  ·  ⚠ provenance_open {nprov}" if nprov else ""))

    if bad:
        print("\n⛔ 원자료와 어긋나는 항목")
        for e, why in bad:
            print(f"   {e.get('metric'):22s} {e.get('system'):18s} {why}")

    # ★ provenance_open 은 수치 대조를 통과해도 남는 문제다 (2026-08-07 Codex 6라운드).
    #   레지스트리·open_items 에만 있으면 validator 를 돌려도 무경고 ✅ 라 놓친다.
    prov = [e for e in ents if e.get("provenance_open")]
    if prov:
        print(f"\n⚠ provenance_open {len(prov)}건: "
              + ", ".join(f"{e.get('metric')}/{e.get('system')}" for e in prov))
        print("   값은 정본 파일과 일치하지만 **그 값을 만든 실행을 파일로 재현할 수 없다.**")
        print("   kb/open_items.md 의 데이터 감사 항목 참조 (회수 → 재계산 → 등급 하향).")

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
