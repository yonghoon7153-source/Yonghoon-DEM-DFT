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
        rel = f.relative_to(REPO).as_posix()
    except ValueError:
        rel = pathlib.Path(f).as_posix()                      # selftest 의 임시 경로
    rec = {"file": rel, "kind": type(d).__name__}
    if not isinstance(d, dict):
        rec["date"] = None
        rec["notes"] = ["dict 가 아님 — 메타 필드를 못 단다"]
        return rec, None
    # ★ provenance 는 최상위에도, `_provenance_audit` 블록 안에도 올 수 있다.
    #   감사기가 **자기가 요구한 규약**을 못 읽으면 고쳐도 계속 운다 (2026-08-12).
    pa = d.get("_provenance_audit") if isinstance(d.get("_provenance_audit"), dict) else {}
    rec["date"] = next((str(d[k]) for k in DATE_KEYS if k in d),
                       next((str(pa[k]) for k in DATE_KEYS if k in pa), None))
    if rec["date"] in ("불명", "unknown", "None"):
        rec["date"] = None
    rec["audited"] = bool(pa)
    rec["confidence"] = pa.get("confidence")
    # ⚠ 2026-08-12 정정 — 처음엔 최상위 SRC_KEYS 만 봤다. 그랬더니 정본 앵커 28건이
    #   전부 "사슬 끊김" 으로 나왔는데 **오탐**이었다: electronic.json 도 eos.json 도
    #   경로를 갖고 있고, 다만 블록 안쪽에 중첩돼 있었다. 둘을 갈라서 본다.
    #     declared : 최상위 출처 필드 — 기계가 믿고 따라갈 수 있다
    #     any      : 문서 어디든 있는 경로 문자열 — 사람은 따라갈 수 있다
    ps = set()
    for k in SRC_KEYS:
        if k in d:
            _paths_in(d[k], ps)
        if k in pa:
            _paths_in(pa[k], ps)
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
                and (str(res[o].get("status", "")).lower()
                     in ("deprecated", "retracted", "superseded", "historical")
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
        names[f.name] = f.relative_to(REPO).as_posix()
    for f in PROPS.rglob("*.csv"):
        names[f.name] = f.relative_to(REPO).as_posix()
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
                    idx[rel].append(f.relative_to(REPO).as_posix())
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
    # ★ P0-5 — 감사는 json 만 본다. db/properties 는 csv 가 더 많다(146 vs 77).
    #   Origin-ready CSV 가 그림 숫자에 직결되므로 **덮지 못한다는 사실**을 먼저 찍는다.
    by_fmt = {}
    for f in PROPS.rglob("*"):
        if f.is_file():
            by_fmt[f.suffix.lower() or "(없음)"] = by_fmt.get(f.suffix.lower() or "(없음)", 0) + 1
    files = sorted(PROPS.rglob("*.json"))
    recs, broken = [], []
    for f in files:
        r, err = audit_file(f)
        if err:
            broken.append((f.relative_to(REPO).as_posix(), err))
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
    _tot = sum(by_fmt.values())
    print(f"⚠ 감사 범위: **json 만** {len(files)}/{_tot} 파일 "
          f"({100*len(files)/max(1,_tot):.0f}%) — " +
          " · ".join(f"{k}{v}" for k, v in sorted(by_fmt.items(), key=lambda kv: -kv[1])[:5]))
    print(f"  csv/npy/cube 는 provenance 감사 밖이다 (Codex 2026-08-12 P0-5). "
          f"Origin-ready CSV 가 그림 숫자에 직결되므로 schema v1 에서 덮어야 한다.")
    print(f"=== db 신선도 감사 ===  json {len(files)}개 (읽기 실패 {len(broken)})"
          + (f" · **강한 인용만** {len(recs)}개 (그림/원고/정본 앵커)" if cited_only
             else f" · 인용됨 {ncited} / 미인용 {len(recs) - ncited}"))
    print(f"  ① 날짜 없음        {len(nodate):3d}  — 최신인지 판단 불가")
    print(f"  ② 출처 경로 아예 없음 {len(nosrc):3d}  — 원자료를 못 따라간다")
    print(f"  ②' 경로는 있으나 **선언 안 됨** {len(nodecl):3d}  — 사람은 찾지만 "
          f"기계는 못 따라간다")
    print(f"  ③ 죽은 출처 경로    {len(dead):3d}  — 적힌 경로가 사라졌다")
    print(f"  ④ null 값 있음      {len(nulls):3d}  — **채울 자리** 후보")
    aud = [r for r in recs if r.get("audited")]
    lowc = [r for r in recs if r.get("confidence") in ("medium", "low")]
    print(f"  ★ provenance 감사 완료 {len(aud):3d}  (그중 confidence medium/low "
          f"{len(lowc)} — 추적이 확정 안 된 것)")
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
    # ★ P0-1 회귀 — 경로는 **POSIX 로** 나와야 한다. Windows 에서 tools\\figures 가 되면
    #   _is_hard() 의 "tools/figures/" 검사가 전부 빗나가 --cited 가 0건이 된다.
    chk("\\" not in dc["file"], f"내부 경로에 역슬래시가 없다 ({dc['file']})")
    chk(_is_hard("tools/figures/x.py") and _is_hard("webapp/data.py")
        and not _is_hard("kb/notes/x.md"), "강한 인용 판정이 POSIX 경로로 동작")
    # ★ retracted 를 표시로 인정 (Codex: superseded 가 아니라 retracted 가 정확)
    (td / "retr.json").write_text(json.dumps({"results": {
        "a": {"gap": -6.4, "status": "retracted"}, "a_frozen4f": {"gap": 3.9}}}),
        encoding="utf-8")
    rt, _ = audit_file(td / "retr.json")
    chk(rt["superseded"] and not rt["superseded_unmarked"],
        "status=retracted 도 표시로 인정한다")
    # ★ 음성: 모르는 status 는 표시로 인정하면 안 된다
    (td / "weird.json").write_text(json.dumps({"results": {
        "a": {"gap": 1.0, "status": "maybe_ok"}, "a_frozen4f": {"gap": 2.0}}}),
        encoding="utf-8")
    wd, _ = audit_file(td / "weird.json")
    chk(wd["superseded_unmarked"] == [("a", "a_frozen4f")],
        "낯선 status 는 '표시됨' 으로 봐주지 않는다")
    # ── 판례·판정 원장 (2026-08-20 codex 동결감사). 음성 경로가 본론이다 ──────
    gd = td / "gov"
    (gd / "db" / "governance").mkdir(parents=True, exist_ok=True)
    (gd / "db" / "properties").mkdir(parents=True, exist_ok=True)

    def _gov(dec, ass, entries=()):
        (gd / "db/governance/decisions.json").write_text(
            json.dumps({"decisions": dec}), encoding="utf-8")
        (gd / "db/governance/assessments.json").write_text(
            json.dumps({"assessments": ass}), encoding="utf-8")
        return C.validate_governance({"entries": list(entries)}, root=gd)

    D_OK = {"id": "D-x", "decision_state": "proposed", "slot": "s1",
            "ratification": {"state": "proposed"}}
    A_OK = {"assessment_id": "A-x", "kind": "gate", "state": "active",
            "result": "not_assessed", "claim_ref": "value:M/sys", "decision_ids": ["D-x"]}
    E_OK = {"metric": "M", "system": "sys", "blocking_gate": "g",
            "required_assessment_refs": ["A-x"]}

    chk(_gov([D_OK], [A_OK], [E_OK]) == [], "[양성] 온전한 원장은 통과한다")
    chk(any("dangling" in v for v in _gov(
        [{**D_OK, "supersedes": ["D-nope"]}], [A_OK], [E_OK])),
        "[음성] supersedes 가 매달린 간선을 잡는다")
    chk(any("승인 없이 active" in v for v in _gov(
        [{**D_OK, "decision_state": "active"}], [A_OK], [E_OK])),
        "[음성] 사람 승인 없이 active 인 결정을 잡는다")
    chk(any("slot" in v for v in _gov(
        [{"id": "D-a", "decision_state": "active", "slot": "s1",
          "ratification": {"state": "ratified", "role": "scientific_owner"}},
         {"id": "D-b", "decision_state": "active", "slot": "s1",
          "ratification": {"state": "ratified", "role": "scientific_owner"}}], [], [])),
        "[음성] 같은 slot 에 active 가 둘이면 잡는다")
    chk(any("없는 결정" in v for v in _gov(
        [D_OK], [{**A_OK, "decision_ids": ["D-nope"]}], [E_OK])),
        "[음성] 판정이 없는 결정을 가리키면 잡는다")
    chk(any("scope 가 없다" in v for v in _gov(
        [D_OK], [A_OK, {"assessment_id": "A-c", "kind": "correction",
                        "supersedes_assessment_id": "A-x"}], [E_OK])),
        "[음성] 정정에 scope 가 없으면 잡는다 (사유가 다른 항목으로 번진다)")
    chk(any("어휘 밖" in v for v in _gov(
        [D_OK], [{**A_OK, "result": "probably_fine"}], [E_OK])),
        "[음성] 판정 result 가 어휘 밖이면 잡는다")
    chk(any("없는 판정" in v for v in _gov(
        [D_OK], [A_OK], [{**E_OK, "required_assessment_refs": ["A-nope"]}])),
        "[음성] claim 이 없는 판정을 참조하면 잡는다")
    chk(any("active 판정이 0개" in v for v in _gov(
        [D_OK], [{**A_OK, "state": "retracted"}], [E_OK])),
        "[음성] active 판정이 없으면 잡는다 (철회본만 가리키는 경우)")
    chk(any("다른 claim" in v for v in _gov(
        [D_OK], [{**A_OK, "claim_ref": "value:OTHER/zzz"}], [E_OK])),
        "[음성] 남의 판정을 참조하면 잡는다")
    chk(any("판정이 남아 있다" in v for v in _gov(
        [D_OK], [A_OK], [{**E_OK, "gate_detail": {"lineage": {"gate_outcome": "pass"}}}])),
        "[음성] claim 안에 판정이 남아 있으면 잡는다 (sidecar 가 단일 원장)")
    chk(any("lineage_status 를 되살렸다" in v for v in _gov(
        [D_OK], [A_OK], [{**E_OK, "gate_detail": {
            "lineage": {"lineage_status": "numerically_reproducible"}}}])),
        "[음성] 두 축을 한 enum 으로 되돌리면 잡는다")
    chk(any("어휘 밖" in v for v in _gov(
        [D_OK], [A_OK], [{**E_OK, "gate_detail": {
            "lineage": {"lineage_binding": "sorta_wired"}}}])),
        "[음성] lineage_binding 어휘 밖을 잡는다")

    # ── 승인은 **그 시점 내용**에 묶인다 (codex: decision digest 결속) ──────
    _rat = {"state": "ratified", "actor_id": "y", "role": "scientific_owner",
            "timestamp": "2026-08-20T00:00:00Z", "commit": "f" * 40}
    D_RAT = {"id": "D-r", "decision_state": "active", "slot": "s9",
             "statement": "원문", "ratification": dict(_rat)}
    D_RAT["ratification"]["decision_digest"] = C.decision_digest(D_RAT)
    chk(_gov([D_RAT], [], []) == [], "[양성] 승인 + 지문이 맞으면 통과")
    D_TAMPER = json.loads(json.dumps(D_RAT)); D_TAMPER["statement"] = "몰래 고친 문장"
    chk(any("승인 이후에 내용이 바뀌었다" in v for v in _gov([D_TAMPER], [], [])),
        "[음성] ★ 승인 뒤 statement 를 고치면 잡는다 (승인이 상태 문자열이면 못 잡는다)")
    D_NODIG = json.loads(json.dumps(D_RAT)); del D_NODIG["ratification"]["decision_digest"]
    chk(any("decision_digest 가 없다" in v for v in _gov([D_NODIG], [], [])),
        "[음성] 지문 없는 승인을 잡는다")
    D_SHORT = json.loads(json.dumps(D_RAT)); D_SHORT["ratification"]["commit"] = "bb9f9c5d"
    D_SHORT["ratification"]["decision_digest"] = C.decision_digest(D_SHORT)
    chk(any("40-hex 가 아니다" in v for v in _gov([D_SHORT], [], [])),
        "[음성] 짧은 commit 을 잡는다")
    D_NOWHO = json.loads(json.dumps(D_RAT)); del D_NOWHO["ratification"]["actor_id"]
    D_NOWHO["ratification"]["decision_digest"] = C.decision_digest(D_NOWHO)
    chk(any("actor_id 가 없다" in v for v in _gov([D_NOWHO], [], [])),
        "[음성] 누가 승인했는지 없으면 잡는다")

    # ── 중복 ID · 중복 색인 (회신 AW P0-4, 2026-09-05) ─────────────────────
    # 종전 세 원장이 전부 `{r[id]: r for r in ...}` 였다. dict 컴프리헨션은 같은 키를
    # **마지막 것으로 조용히 덮는다** — 무승인 active 뒤에 같은 ID 의 proposed 를 두면
    # 승인 검사가 active 기록 자체를 못 보고 통과한다. 셋 다 fail-closed 로 막았다.
    def _raises(fn, frag):
        try:
            fn()
        except RuntimeError as ex:
            return frag in str(ex)
        except Exception:
            return False
        return False

    D_DUPA = {"id": "D-dup", "decision_state": "active", "slot": "sd",
              "ratification": {"state": "ratified", "role": "scientific_owner"}}
    D_DUPP = {"id": "D-dup", "decision_state": "proposed", "slot": "sd",
              "ratification": {"state": "proposed"}}
    chk(_raises(lambda: _gov([D_DUPA, D_DUPP], [], []), "ID 가 중복"),
        "[음성] ★ 무승인 active 를 같은 ID 의 proposed 로 가리는 경로를 막는다")
    chk(_raises(lambda: _gov([D_OK], [A_OK, dict(A_OK)], [E_OK]), "ID 가 중복"),
        "[음성] 판정 원장의 중복 ID 를 잡는다")
    chk(_raises(lambda: _gov([{**D_OK, "id": None}], [], []), "id 없는"),
        "[음성] ID 없는 결정 기록을 잡는다")

    # 산출물 원장도 같은 경로다 (artifacts.json 은 위 _gov 가 안 만들므로 직접 쓴다)
    (gd / "db/governance/artifacts.json").write_text(
        json.dumps({"artifacts": [{"id": "R-1"}, {"id": "R-1"}]}), encoding="utf-8")
    chk(_raises(lambda: C.artifacts(root=gd), "ID 가 중복"),
        "[음성] 산출물 원장의 중복 ID 를 잡는다")
    (gd / "db/governance/artifacts.json").unlink()

    # canonical 색인 — 같은 (metric, system) 이 둘이면 배지가 어느 쪽인지 정해져 있지 않다
    _dupreg = {"entries": [
        {"metric": "M", "system": "sys", "value": 1.0, "status": "canonical",
         "comparison_group": "g1"},
        {"metric": "M", "system": "sys", "value": 2.0, "status": "canonical",
         "comparison_group": "g2"}]}
    chk(any("색인 충돌" in p for _e, p in C.validate(_dupreg, root=gd)),
        "[음성] ★ 같은 (metric, system) 두 항목을 validate 가 위반으로 낸다")
    chk(_raises(lambda: C.canonical_map(_dupreg, "M"), "두 번 있다"),
        "[음성] canonical_map 이 마지막 값으로 조용히 덮지 않는다")
    _okreg = {"entries": [
        {"metric": "M", "system": "a", "value": 1.0, "status": "canonical"},
        {"metric": "M", "system": "b", "value": 2.0, "status": "canonical"}]}
    chk(C.canonical_map(_okreg, "M") == {"a": 1.0, "b": 2.0},
        "[양성] 중복이 없으면 그대로 돌려준다")

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

    # ── 판례·판정 원장 무결성 (2026-08-20 codex 동결감사) ────────────────────
    #   ⛔ 이전에는 이 도구가 새 필드(required_assessment_refs · lineage_binding)를 아예
    #     안 읽어 **자기가 지키는 db 의 정정을 스스로 검증하지 못했다.** webapp 테스트만
    #     잡는 상태였다. 검사 로직은 webapp/canonical.py 에 한 벌만 두고 여기서 부른다.
    gov = C.validate_governance(reg)
    if gov:
        print(f"\n⛔ 판례·판정 원장 위반 {len(gov)}건")
        for g in gov:
            print(f"   {g}")
    else:
        nd, na = len(C.decisions()), len(C.assessments())
        if nd or na:
            print(f"거버넌스 결정 {nd} · 판정 {na}  ·  그래프 무결성 ✅")

    if bad or gov:
        print("\n판정: ⛔ 실패 — 레지스트리를 고치거나 원자료를 확인할 것")
        return 1
    print("\n판정: ✅ 배선된 항목은 전부 원자료와 일치")
    return 0


if __name__ == "__main__":
    sys.exit(main())
