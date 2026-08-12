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
    # ⚠ 2026-08-12 정정 — 처음엔 최상위 SRC_KEYS 만 봤다. 그랬더니 정본 앵커 28건이
    #   전부 "사슬 끊김" 으로 나왔는데 **오탐**이었다: electronic.json 도 eos.json 도
    #   경로를 갖고 있고, 다만 블록 안쪽에 중첩돼 있었다. 둘을 갈라서 본다.
    #     declared : 최상위 출처 필드 — 기계가 믿고 따라갈 수 있다
    #     any      : 문서 어디든 있는 경로 문자열 — 사람은 따라갈 수 있다
    ps = set()
    for k in SRC_KEYS:
        if k in d:
            _paths_in(d[k], ps)
    rec["sources_declared"] = sorted(ps)[:6]
    pa = set()
    _paths_in(d, pa)
    rec["sources"] = sorted(pa)[:8]
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


#: 인용처로 볼 트리
CITE_TREES = ("tools", "kb", "webapp", "docs", "litdb")
#: **강한 인용** = 그 숫자가 독자에게 도달하는 경로. 여기 걸리면 provenance 가 필수다.
#:   · 그림 생성기 (tools/figures/, plot_*.py) — 논문·발표 그림이 된다
#:   · webapp/canonical.py 레지스트리 — 화면의 정본 앵커
#:   · 원고/세미나 문서
#: kb 노트의 단순 언급은 **약한 인용**이다. 68/77 이 걸려 필터가 무의미해진다.
HARD_CITE = ("tools/figures/", "webapp/canonical.py", "webapp/data.py",
             "docs/manuscript", "kb/seminars/", "kb/reports/")


def _is_hard(where):
    return (any(where.startswith(h) for h in HARD_CITE)
            or "/plot_" in where or where.endswith("_origin.py"))


def build_citation_index():
    """db/properties/<파일> 을 참조하는 repo 내 위치를 센다.

    ⚠ 파일명만으로 센다 (경로 표기가 제각각이라). 흔한 단어가 파일명이면 과다검출될
      수 있으므로 **stem 이 6자 이상**인 것만 신뢰한다 — 짧은 것은 별도 표시.
    """
    names = {}
    for f in PROPS.rglob("*.json"):
        names[f.name] = str(f.relative_to(REPO))
    for f in PROPS.rglob("*.csv"):
        names[f.name] = str(f.relative_to(REPO))
    idx = {v: [] for v in names.values()}
    for tree in CITE_TREES:
        d = REPO / tree
        if not d.is_dir():
            continue
        for f in d.rglob("*"):
            if not f.is_file() or f.suffix not in (".py", ".md", ".html", ".sh", ".json"):
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for nm, rel in names.items():
                if nm in txt:
                    idx[rel].append(str(f.relative_to(REPO)))
    return idx


def chain_check(recs):
    """정본 앵커의 **두 번째 고리**를 본다 (2026-08-12).

    ⚠ 기존 검증은 `앵커 값 == db 파일 값` 만 본다. 그래서 "28/28 일치" 가 나와도
      그 db 파일이 **원자료에 닿는지**는 아무도 안 묻는다. 실제로 ICOHP P–S 정본
      두 개(−5.938 / −5.9997)가 원자료 경로 없는 파일을 가리키고 있었다.
      사슬은  앵커 → db 파일 → 원자료  인데 첫 고리만 검사해 온 셈이다.
    """
    reg = C.load_registry()
    by_file = {r["file"]: r for r in recs}
    out = []
    for e in reg.get("entries", []):
        sp = str(e.get("source_path") or "")
        if not sp:
            out.append((e, "앵커에 source_path 가 없다"))
            continue
        r = by_file.get(sp)
        if r is None:
            out.append((e, f"가리키는 파일이 감사 대상에 없다: {sp}"))
        elif not r.get("sources"):
            out.append((e, f"{sp} 에 원자료 경로가 **아예 없다** — 사슬이 끊긴다"))
    return out


def cmd_audit(show_all=False, cited_only=False):
    """db/properties 전체 신선도 감사 — 요약이 기본, 목록은 --audit_all."""
    cites = build_citation_index()
    files = sorted(PROPS.rglob("*.json"))
    recs, broken = [], []
    for f in files:
        r, err = audit_file(f)
        if err:
            broken.append((str(f.relative_to(REPO)), err))
        else:
            r["cited_by"] = cites.get(r["file"], [])
            r["hard_cited_by"] = [w for w in r["cited_by"] if _is_hard(w)]
            r["short_name"] = len(pathlib.Path(r["file"]).stem) < 6
            recs.append(r)
    if cited_only:
        recs = [r for r in recs if r.get("hard_cited_by")]
    nodate = [r for r in recs if not r.get("date")]
    dead = [r for r in recs if r.get("dead_sources")]
    nulls = [r for r in recs if r.get("nulls")]
    sup = [r for r in recs if r.get("superseded")]
    unmarked = [r for r in recs if r.get("superseded_unmarked")]
    nosrc = [r for r in recs if r.get("kind") == "dict" and not r.get("sources")]
    nodecl = [r for r in recs if r.get("kind") == "dict"
              and r.get("sources") and not r.get("sources_declared")]
    ncited = sum(1 for r in recs if r.get("cited_by"))
    print(f"=== db 신선도 감사 ===  json {len(files)}개 (읽기 실패 {len(broken)})"
          + (f" · **강한 인용만** {len(recs)}개 (그림/원고/정본 앵커)" if cited_only
             else f" · 인용됨 {ncited} / 미인용 {len(recs) - ncited}"))
    print(f"  ① 날짜 없음        {len(nodate):3d}  — 최신인지 판단 불가")
    print(f"  ② 출처 경로 아예 없음 {len(nosrc):3d}  — 원자료를 못 따라간다")
    print(f"  ②' 경로는 있으나 **선언 안 됨** {len(nodecl):3d}  — 사람은 찾지만 "
          f"기계는 못 따라간다")
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
    chain = chain_check(recs)
    if chain:
        print(f"\n── ⑥ 정본 앵커의 **끊긴 사슬** {len(chain)}건 ──")
        print("   (앵커→db파일 은 검증되지만 db파일→원자료 가 끊겨 있다)")
        seen = set()
        for e, why in chain:
            k = (str(e.get("value")), why)
            if k in seen:
                continue
            seen.add(k)
            print(f"  값 {e.get('value')}  status={e.get('status')}\n     {why}")
    if cited_only:
        gap = [r for r in recs if not r.get("date") or not r.get("sources")]
        print(f"\n── provenance 가 빈 강한-인용 파일 {len(gap)}건 (여기부터 채운다) ──")
        for r in sorted(gap, key=lambda x: -len(x["hard_cited_by"])):
            miss = ("날짜" if not r.get("date") else "") + \
                   (" 출처" if not r.get("sources") else "")
            print(f"  {r['file']:50s} [{miss.strip()}]  ← {r['hard_cited_by'][0]}"
                  + (f" 외 {len(r['hard_cited_by']) - 1}" if len(r["hard_cited_by"]) > 1 else ""))
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
    # ── declared vs any (2026-08-12) ──
    #   ★ 처음엔 최상위 SRC_KEYS 만 봐서 정본 앵커 28건이 전부 "사슬 끊김" 으로 나왔다.
    #     **오탐**이었다 — 경로가 블록 안쪽에 중첩돼 있었을 뿐이다. 그 재발을 막는다.
    (td / "nested.json").write_text(json.dumps({
        "band_gaps": {"comp1": {"note": "from runs/comp1_v3/k444/V0_dos_summary.json",
                                "gap": 2.066}}}), encoding="utf-8")
    nz, _ = audit_file(td / "nested.json")
    chk(nz["sources"] and "comp1_v3" in nz["sources"][0],
        f"**중첩된** 경로도 찾는다 ({nz['sources'][:1]}) — 최상위만 보면 오탐이 난다")
    chk(nz["sources_declared"] == [],
        "다만 '선언된 출처' 는 아니다 (기계가 따라갈 수 없다)")
    (td / "decl.json").write_text(json.dumps(
        {"source": "runs/x/y.out", "results": {}}), encoding="utf-8")
    dc, _ = audit_file(td / "decl.json")
    chk(dc["sources_declared"] == ["runs/x/y.out"], "최상위 source 는 declared 로 잡는다")
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
    ap.add_argument("--cited", action="store_true",
                    help="**실제로 참조되는** db 파일만 감사한다 (tools/kb/webapp/docs/litdb "
                         "에서 파일명이 나오는 것). 안 쓰이는 파일의 provenance 를 지금 채워도 "
                         "검증할 방법이 없다 — 인용되는 것부터 채우는 게 값이 된다.")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.audit or a.audit_all or a.cited:
        return cmd_audit(show_all=a.audit_all, cited_only=a.cited)

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
