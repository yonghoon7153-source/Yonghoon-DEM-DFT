#!/usr/bin/env python3
"""build_index.py — litdb 인덱스를 **생성**한다 (손으로 유지하지 않는다).

왜 (open_items #7, 2026-08-06 해결):
  `INDEX.md` 는 argyrodite/SE 축 전용이라 DEM·기계·건식전극 digest 가 안 들어간다.
  그래서 digest 159편 중 **64편이 어느 인덱스에도 없었다**. 사이트(`list_papers()`)는
  디렉터리를 직접 읽어 멀쩡했지만, 마크다운 인덱스만 계속 뒤처졌다.
  손으로 맞추면 또 밀린다 — **DEM 축 인덱스를 생성**하고, 어디에도 없는 digest를
  `--check` 로 잡는다.

  · `INDEX.md`            = SE 축 (사람이 큐레이션, 논평이 붙는다) — 건드리지 않는다
  · `INDEX_DEM.md`        = DEM·MPM 축 (이 도구가 생성)
  · `--check`             = 두 인덱스 어디에도 없는 digest 보고 (CI/점검용, 0=깨끗)

usage
  python3 tools/litdb/build_index.py            # INDEX_DEM.md 생성 + 정합 점검
  python3 tools/litdb/build_index.py --check    # 점검만 (파일 안 씀)
"""
import argparse
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LITDB = ROOT / "litdb"
sys.path.insert(0, str(ROOT / "webapp"))
import data as D                                                   # noqa: E402

DEM_INDEX = LITDB / "INDEX_DEM.md"
SE_INDEX = LITDB / "INDEX.md"

# 주제 묶음 — slug/제목에 이 낱말이 있으면 그 절로. 위에서부터 먼저 맞는 것.
GROUPS = [
    # ⚠ MPM 을 먼저 — 'snow elastoplastic'·'Drucker-Prager' 는 접촉역학 낱말도 갖고 있어
    #   뒤에 두면 그쪽으로 샌다 (실측: stomakhin2013·klar2016).
    ("MPM · 연속체", ("mpm", "material point", "snow", "sand", "drucker")),
    ("접촉역학 · 소성 (DEM 이론)",
     ("contact", "adhesion", "elastoplastic", "indentation", "hertz", "densification",
      "packing", "similarity", "cohesive", "eepa", "dmt", "kogut", "storakers",
      "thornton", "pasha", "luding", "bouvard", "mcgeary", "jacksongreen", "mesarovic")),
    ("복합양극 미세구조 · percolation",
     ("microstructure", "microstructural", "percolation", "porosity", "tortuosity",
      "taufactor", "conductive_path", "conductive_paths", "effective", "volumetric")),
    ("공정 — 캘린더링 · 압축 · 건식전극",
     ("calender", "compaction", "mold_pressure", "coldpress", "dry", "rolling",
      "mixer", "sintering", "drying", "wet_process", "manufacturing", "binder", "ptfe")),
    ("화학-기계 열화 · 계면", ("chemomech", "failure", "cracking", "degradation",
                              "delamination", "stress", "interfac", "impedance")),
    ("Digital twin · ML 최적화", ("digital_twin", "digitaltwin", "ml_", "duquesnoy",
                                  "multiobjective", "optimization")),
]


def group_of(pid, title):
    t = (pid + " " + title).lower()
    for name, keys in GROUPS:
        if any(k in t for k in keys):
            return name
    return "기타"


def rows(papers, track):
    out = []
    for p in papers:
        if p["track"] != track:
            continue
        title = re.sub(r"\s+", " ", p["title"]).strip()
        title = re.sub(r"^[⭐★🔴🟡✅⬜📄]+\s*", "", title)
        out.append({"id": p["id"], "title": title[:180], "type": p["type"][:60],
                    "digested": p["digested"], "group": group_of(p["id"], title)})
    return out


def build(dry=False):
    papers = D.list_papers()
    dem = rows(papers, "dem")
    figs = D.papers_with_figures()
    by = {}
    for r in dem:
        by.setdefault(r["group"], []).append(r)
    order = [g for g, _k in GROUPS] + ["기타"]

    L = ["# 🧱 LITDB — DEM · MPM 축 인덱스",
         "",
         "> **이 파일은 `tools/litdb/build_index.py` 가 생성한다 — 손으로 고치지 말 것.**",
         "> 논평·우선순위가 붙는 SE 축 인덱스는 `INDEX.md` (사람이 큐레이션).",
         f"> digest {len(dem)}편 · 생성 {time.strftime('%Y-%m-%d')}",
         "",
         "왜 따로 두나 — `INDEX.md` 는 argyrodite 전해질 축이라 접촉역학·MPM·건식전극",
         "digest 가 들어갈 자리가 없다. 그래서 한때 64편이 **어느 인덱스에도 없었다**",
         "(open_items #7). 축을 나누고 생성으로 바꿔 그 구멍을 닫는다.",
         ""]
    for g in order:
        rs = by.get(g)
        if not rs:
            continue
        L += [f"## {g} ({len(rs)}편)", "",
              "| slug | 논문 | 유형 | digest | 그림 |", "|---|---|---|---|---|"]
        for r in sorted(rs, key=lambda x: x["id"]):
            n = figs.get(r["id"], 0)
            L.append(f"| `{r['id']}` | {r['title']} | {r['type']} | "
                     f"{r['digested'] or '—'} | {('🖼 ' + str(n)) if n else '—'} |")
        L.append("")

    # ── 발표 덱 (litdb/talks) ────────────────────────────────────────────
    # ⚠ 덱은 peer-review 를 안 거쳐 **papers/ 와 인용 등급이 다르다**(talks/README.md).
    #   그래서 위 표에 섞지 않고 **별도 절 + 편수도 따로** 낸다. 그래도 인덱스에 실어야
    #   하는 이유: DEM 축 덱이 어느 인덱스에도 안 나와 검색으로만 찾이는 상태였다.
    talks = [t for t in D.list_talks()
             if "dem" in _talk_axis(t["id"]) or "microstructure" in _talk_axis(t["id"])]
    if talks:
        L += [f"## 🎤 발표 덱 ({len(talks)}편) — ⚠ 인용 등급이 papers/ 보다 한 단계 낮다", "",
              "> `litdb/talks/README.md` 의 인용 규율. **덱 수치는 우리 db 절대값과 같은 표에 넣지 않는다.**",
              "", "| slug | 발표자 | 주제 | 발표 | 그림 |", "|---|---|---|---|---|"]
        for t in sorted(talks, key=lambda x: x["id"]):
            n = figs.get(t["id"], 0)
            L.append(f"| `{t['id']}` | {t.get('speaker') or '—'} | {t['title'][:150]} | "
                     f"{t.get('session') or t.get('digested') or '—'} | "
                     f"{('🖼 ' + str(n)) if n else '—'} |")
        L.append("")

    txt = "\n".join(L)
    if not dry:
        DEM_INDEX.write_text(txt, encoding="utf-8")
    return dem, txt


def _talk_axis(slug):
    """덱 digest 헤더의 `axis:` 값 (없으면 ''). DEM 축 덱만 이 인덱스에 싣기 위한 판정.

    이 함수가 못 하는 것: `axis:` 태그가 없는 옛 덱은 항상 ''를 돌려주므로 실리지 않는다
    (소급 태깅은 사람이 한다 — 자동 추측하면 축이 섞인다).
    """
    f = LITDB / "talks" / f"{slug}.md"
    try:
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]:
            m = re.search(r"axis:\s*`?([a-z0-9_\-]+)", line, re.I)
            if m:
                return m.group(1).lower()
    except Exception:
        pass
    return ""


def check():
    """두 인덱스 어디에도 없는 digest → 목록. 0 이면 깨끗."""
    papers = D.list_papers()
    se = SE_INDEX.read_text(encoding="utf-8") if SE_INDEX.exists() else ""
    dem = DEM_INDEX.read_text(encoding="utf-8") if DEM_INDEX.exists() else ""
    missing = [p for p in papers if p["id"] not in se and p["id"] not in dem]
    return papers, missing


CMP_DFT = LITDB / "comparison_vs_ours.md"
CMP_DEM = LITDB / "comparison_vs_ours_DEM.md"


def check_comparison(papers):
    """비교문서 편입률 — **트랙별로** 센다.

    ⚠ 통째로 세면 "159편 중 98편 미언급" 같은 오해가 나온다(2026-08-06 실측).
      comparison_vs_ours.md 는 **DFT 물성축** 문서라 DEM 논문이 들어갈 자리가 없고,
      DEM 논문은 comparison_vs_ours_DEM.md 가 받는다. 축이 다른 걸 한 분모로 세면
      '안 한 일'이 부풀어 보인다.
    """
    dft_md = CMP_DFT.read_text(encoding="utf-8") if CMP_DFT.exists() else ""
    dem_md = CMP_DEM.read_text(encoding="utf-8") if CMP_DEM.exists() else ""
    out = {}
    for track, doc, name in (("dft", dft_md, CMP_DFT.name), ("dem", dem_md, CMP_DEM.name)):
        want = [p for p in papers if p["track"] == track]
        # 자기 축 문서에 없고 **다른 축 문서에도** 없으면 진짜 미편입
        other = dem_md if track == "dft" else dft_md
        miss = [p for p in want if p["id"] not in doc and p["id"] not in other]
        out[track] = {"doc": name, "n": len(want), "miss": miss}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="점검만 (파일 안 씀)")
    a = ap.parse_args()

    if not a.check:
        dem, _ = build()
        print(f"→ litdb/INDEX_DEM.md  (DEM 축 {len(dem)}편)")

    papers, missing = check()
    print(f"=== 정합 점검: digest {len(papers)}편 · 어느 인덱스에도 없는 것 {len(missing)}편")
    for p in missing[:30]:
        print(f"   [{p['track']}] {p['id']}")
    if len(missing) > 30:
        print(f"   … 외 {len(missing)-30}편")

    cmp_ = check_comparison(papers)
    print("\n=== 비교문서 편입 (트랙별 — 축이 다르므로 분모를 섞지 않는다)")
    for track, r in cmp_.items():
        done = r["n"] - len(r["miss"])
        print(f"   {track.upper():3} {done:3}/{r['n']:<3} → {r['doc']}"
              + (f"   미편입 {len(r['miss'])}편" if r["miss"] else "   ✅ 전부 편입"))
        for p in r["miss"][:12]:
            print(f"        {p['id']}")
        if len(r["miss"]) > 12:
            print(f"        … 외 {len(r['miss'])-12}편")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
