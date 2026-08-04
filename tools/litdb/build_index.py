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
    txt = "\n".join(L)
    if not dry:
        DEM_INDEX.write_text(txt, encoding="utf-8")
    return dem, txt


def check():
    """두 인덱스 어디에도 없는 digest → 목록. 0 이면 깨끗."""
    papers = D.list_papers()
    se = SE_INDEX.read_text(encoding="utf-8") if SE_INDEX.exists() else ""
    dem = DEM_INDEX.read_text(encoding="utf-8") if DEM_INDEX.exists() else ""
    missing = [p for p in papers if p["id"] not in se and p["id"] not in dem]
    return papers, missing


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
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
