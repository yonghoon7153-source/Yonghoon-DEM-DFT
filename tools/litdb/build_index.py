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

표 셀수 검사 (2026-09-22 추가)
  ⛔⛔ **마크다운 표는 헤더보다 칸이 많으면 넘치는 칸을 *조용히 버린다*.** 파일엔 글자가
  있는데 렌더된 화면에는 안 나온다 — 웹앱이 `litdb/` 를 라이브로 읽으므로 실제로 사라진다.
  칸이 **모자라면** 반대로 셀이 밀려 엉뚱한 열에 붙는다. 둘 다 오류를 안 낸다.
  2026-09-22 실측: `comparison_vs_ours.md` 에 **30행**이 이 상태였고 원인은 둘뿐이었다 —
  ① 절댓값 `|x|` 표기의 파이프 미이스케이프(`\\|` 로 써야 한다) ② 칸을 하나 더/덜 쓴 행.
  ⇒ `--check` 가 **항상** 같이 돈다. 침묵하지 않는다.

usage
  python3 tools/litdb/build_index.py            # INDEX_DEM.md 생성 + 정합 점검 + 표 검사
  python3 tools/litdb/build_index.py --check    # 점검만 (파일 안 씀)
  python3 tools/litdb/build_index.py --selftest # 자체 점검 (양성 + 음성 경로)

⛔ 이 도구가 **못 하는 것**
  · digest 내용이 맞는지 — 인덱스에 *있나 없나*만 본다.
  · 표 안의 값이 옳은지 · 열 순서가 의미상 맞는지 — **셀 개수**만 센다.
    (2026-09-22 실측: `[Jain26Rev]` 행은 논문/digest 칸이 **뒤바뀐 채** 칸 수만 맞을 수도 있었다.)
  · 여러 줄에 걸친 표 셀(마크다운이 지원 안 함)과 HTML `<table>` — 인식하지 않는다.
  · 편입률의 **질** — 한 줄 언급도 '편입'으로 센다.
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


def cell(s):
    """생성 표의 한 칸으로 안전하게 만든다.

    ⛔⛔ **digest 본문에서 온 글자에 `|` 가 있으면 표가 조용히 깨진다** (2026-09-22 실측).
      `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)` 한 칸이 **8 칸으로 쪼개져**
      `INDEX_DEM.md` 70 행이 12 칸이 됐고, 렌더에서는 넘친 칸이 **버려져** 안 보였다.
      오류도 안 났다 — 조용히 틀린 경로다. ⇒ 생성하는 모든 칸은 여기를 통과한다.
    """
    return re.sub(r"\s*[\r\n]+\s*", " ", str(s)).replace("|", r"\|")


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
            L.append(f"| `{cell(r['id'])}` | {cell(r['title'])} | {cell(r['type'])} | "
                     f"{cell(r['digested'] or '—')} | {('🖼 ' + str(n)) if n else '—'} |")
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
            L.append(f"| `{cell(t['id'])}` | {cell(t.get('speaker') or '—')} | "
                     f"{cell(t['title'][:150])} | "
                     f"{cell(t.get('session') or t.get('digested') or '—')} | "
                     f"{('🖼 ' + str(n)) if n else '—'} |")
        L.append("")

    txt = "\n".join(L)
    if not dry:
        DEM_INDEX.write_text(txt, encoding="utf-8")
    return dem, txt


_AXIS_RE = re.compile(r"^>.*?\baxis:\s*[`*]*([a-z0-9_\-]+)", re.I)
#: axis 태그를 읽는 **메타 블록 창**. 정책이지 우연이 아니다 (위 _talk_axis 주석).
_AXIS_WINDOW = 20
#: 창 **밖**에서 발견된 axis 태그 — 조용히 버리지 않고 여기 모아 보고한다.
LATE_AXIS_TAGS: list = []


def _talk_axis(slug):
    """덱 digest **메타 블록**의 `axis:` 값 (없으면 ''). DEM 축 덱만 인덱스에 싣기 위한 판정.

    ⚠ 왜 `^>` 를 요구하나 (2026-08-25 실측 사고): 처음엔 아무 줄에서나 `axis:` 를 찾았더니,
      **"저쪽 파일에는 `axis: dem-microstructure` 태그가 있다"고 *설명하는 산문*** 이 걸려
      통합 stub 이 인덱스에 같이 실렸다. 태그는 항상 머리말 인용블록(`> slug … · axis: … ·`)에
      있으므로 **줄이 `>` 로 시작할 때만** 태그로 인정한다.

    이 함수가 못 하는 것: `axis:` 태그가 없는 옛 덱은 항상 ''를 돌려주므로 실리지 않는다
    (소급 태깅은 사람이 한다 — 자동 추측하면 축이 섞인다).
    """
    f = LITDB / "talks" / f"{slug}.md"
    try:
        # ⚠ 2026-09-13 검토 — 이 20줄은 `list_papers` 의 18줄과 **겉만 같고 다르다.**
        #   저기는 우연이었지만(넓혀서 고침) 여기는 **정책**이다: axis 는 *덱 머리의
        #   메타 블록* 에서만 읽는다. 산문 오탐 방어는 `^>` 가 하지만(음성①), `^>` 만으로는
        #   본문 깊은 곳의 인용줄과 메타 블록을 못 가른다 — 창이 그 역할을 한다.
        #   ⇒ 넓히지 않는다. 대신 **창 밖 태그를 조용히 버리지 않고 보고**한다 (아래).
        _lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line in _lines[:_AXIS_WINDOW]:
            m = _AXIS_RE.match(line)
            if m:
                return m.group(1).lower()
        # 창 밖에 태그가 있으면 **그 사실을 남긴다.** "태그 없음" 과 구분되어야
        #   사람이 "메타 블록으로 옮겨라" 를 판단할 수 있다 (조용히 버리면 못 한다).
        for i, line in enumerate(_lines[_AXIS_WINDOW:], start=_AXIS_WINDOW + 1):
            if _AXIS_RE.match(line):
                LATE_AXIS_TAGS.append((slug, i, _AXIS_RE.match(line).group(1).lower()))
                break
    except Exception:
        pass
    return ""


def selftest():
    """_talk_axis 자체 점검 — **음성 경로 포함** (산문 오탐이 실제로 났던 자리)."""
    import tempfile
    global LITDB
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        print(("  ⭕ " if cond else "  ⛔ ") + name)
        ok, fail = ok + bool(cond), fail + (not cond)

    with tempfile.TemporaryDirectory() as td:
        keep, LITDB = LITDB, Path(td)
        (LITDB / "talks").mkdir(parents=True)
        w = lambda n, s: (LITDB / "talks" / f"{n}.md").write_text(s, encoding="utf-8")
        w("pos_plain", "# T\n\n> slug `x` · type `talk` ·\n> **axis: `dem-microstructure`** ·\n")
        w("pos_nostar", "# T\n\n> axis: dem-microstructure\n")
        w("neg_prose", "# T\n\n4. **`axis: dem-microstructure` 태그**가 있어 인덱스가\n")
        w("neg_none", "# T\n\n> slug `x` · type `talk` ·\n")
        w("neg_late", "# T\n" + "\n" * 25 + "> axis: dem-microstructure\n")
        try:
            chk("양성: 메타 블록의 `> **axis: `…`**`", _talk_axis("pos_plain") == "dem-microstructure")
            chk("양성: 백틱/별표 없어도", _talk_axis("pos_nostar") == "dem-microstructure")
            chk("음성①: **산문 속 axis: 는 태그가 아니다** (통합 stub 오탐 재발 방지)",
                _talk_axis("neg_prose") == "")
            chk("음성②: 태그가 없으면 ''", _talk_axis("neg_none") == "")
            LATE_AXIS_TAGS.clear()
            chk("음성③: 메타 블록 창(20줄) 밖은 태그로 안 읽는다 — **정책**이다",
                _talk_axis("neg_late") == "")
            chk("음성③-b: 그러나 **조용히 버리지 않는다** — 창 밖 태그를 기록한다",
                len(LATE_AXIS_TAGS) == 1 and LATE_AXIS_TAGS[0][0] == "neg_late")
            LATE_AXIS_TAGS.clear()
            _talk_axis("neg_none")
            chk("음성③-c: 진짜로 태그가 없으면 기록도 없다 (없음 ≠ 창 밖)",
                LATE_AXIS_TAGS == [])
            chk("음성④: 파일이 없으면 '' (예외 안 터짐)", _talk_axis("no_such_slug") == "")
        finally:
            LITDB = keep

    # ── check_tables — **음성 경로가 본체다** (양성만 있으면 아무것도 보증 못 한다) ──
    H = "| 주장 | 출처 | 우리 |\n|---|---|---|\n"
    chk("표 양성: 헤더와 행이 같으면 0건",
        check_tables(H + "| a | b | c |\n| d | e | f |\n") == [])
    chk("표 음성①: 칸이 **남으면** 잡는다 (렌더에서 조용히 버려지는 쪽)",
        [b[1:3] for b in check_tables(H + "| a | b | c | d |\n")] == [(4, 3)])
    chk("표 음성②: 칸이 **모자라면** 잡는다 (셀이 밀려 엉뚱한 열에 붙는 쪽)",
        [b[1:3] for b in check_tables(H + "| a | b |\n")] == [(2, 3)])
    chk("표 음성③: **이스케이프된 `\\|` 는 경계가 아니다** — 절댓값 표기는 통과해야 한다",
        check_tables(H + r"| \|E_d\| < 0.05 | b | c |" + "\n") == [])
    chk("표 음성④: **이스케이프 안 한 `|x|` 는 잡는다** (2026-09-22 실제 버그 30건의 원인)",
        [b[1:3] for b in check_tables(H + "| |E_d| < 0.05 | b | c |\n")] == [(5, 3)])
    # ⚠ 아래 둘은 **한 번 헛것을 쟀다** (2026-09-22). 구분자 요구를 빼도 `j = i+2` 가 그 줄을
    #   어차피 건너뛰어서 옛 음성⑤는 깨진 판에서도 초록이었고, 구분자 줄은 칸 수가 헤더와
    #   **항상 같아서** 옛 음성⑥은 세어도 안 걸렸다. ⇒ **판별하는 입력으로 바꿨다.**
    chk("표 음성⑤: 구분자 줄이 없으면 **표가 아니다** — 산문의 `|` 를 표로 오인하지 않는다",
        check_tables("| a | b |\n| c |\n| d | e | f |\n") == [])
    chk("표 음성⑥: 행번호는 **1-기준 실제 행**을 가리킨다 (사람이 그 줄을 열어야 한다)",
        [b[0] for b in check_tables("머리말\n\n| x | y |\n|---|---|\n| 1 | 2 |\n| 3 |\n")] == [6])
    chk("표 음성⑦: 표가 끝나면 다음 표의 헤더를 새로 잡는다 (분모를 섞지 않는다)",
        [b[1:3] for b in check_tables(H + "| a | b | c |\n\n| p | q |\n|---|---|\n| 1 |\n")] == [(1, 2)])
    chk("표 음성⑧: 실물 정본이 지금 깨끗하다 (회귀 탐지)",
        (not CMP_DFT.exists()) or check_tables(CMP_DFT.read_text(encoding="utf-8")) == [])
    # ── cell() — 생성 경로의 이스케이프. **이게 없어서 INDEX_DEM 70행이 12칸이었다** ──
    chk("cell 음성①: `|` 를 이스케이프한다 (안 하면 한 칸이 8칸으로 쪼개진다)",
        cell("⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)")
        == r"⏳ 문서 대기 (exp\|DFT\|AIMD\|MLIP\|DEM\|MPM\|FEM\|mixed)")
    chk("cell 음성②: 줄바꿈을 접는다 (표 셀은 여러 줄을 못 담는다)",
        cell("가\n  나\r\n다") == "가 나 다")
    chk("cell 음성③: 이스케이프한 칸은 검사를 **통과**한다 (양·음성이 맞물린다)",
        check_tables("| a | b |\n|---|---|\n| " + cell("x|y|z") + " | c |\n") == [])
    chk("cell 음성④: 이스케이프를 안 하면 **잡힌다** (위 ③이 헛것이 아님을 보인다)",
        [b[1:3] for b in check_tables("| a | b |\n|---|---|\n| x|y|z | c |\n")] == [(4, 2)])

    print(f"\nselftest: {ok} 통과 / {fail} 실패")
    return 1 if fail else 0


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


def _row_cells(line):
    """표 행을 셀로 쪼갠다. ⛔ **이스케이프된 `\\|` 는 셀 경계가 아니다** — 절댓값 `|x|`
    표기가 여기서 갈린다. 표 행이 아니면 None."""
    s = line.strip()
    if not s.startswith("|"):
        return None
    return re.split(r"(?<!\\)\|", s)[1:-1]


def check_tables(md_text):
    """헤더와 칸 수가 다른 행을 찾는다. 반환 = [(행번호, 얻은칸, 헤더칸, 행앞머리)].

    표의 시작은 **구분자 줄**(`|---|---|`)로 판정한다 — 그게 마크다운이 표를 표로 보는
    조건이고, 본문에 우연히 섞인 `|` 줄을 표로 오인하지 않는 유일한 기준이다.
    ⚠ 다수결로 헤더를 고치지 않는다. 헤더가 정본이고 행이 따라간다 — 어느 쪽이 맞는지는
      사람이 정할 일이지 개수가 정할 일이 아니다.
    """
    lines = md_text.split("\n")
    bad, i = [], 0
    while i < len(lines):
        hdr = _row_cells(lines[i])
        if hdr is not None and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|\s*$", lines[i + 1]):
            n_hdr, j = len(hdr), i + 2
            while j < len(lines) and _row_cells(lines[j]) is not None:
                cs = _row_cells(lines[j])
                if len(cs) != n_hdr:
                    bad.append((j + 1, len(cs), n_hdr, cs[0].strip()[:60] if cs else ""))
                j += 1
            i = j
        else:
            i += 1
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="점검만 (파일 안 씀)")
    ap.add_argument("--selftest", action="store_true", help="자체 점검 (양성 + 음성 경로)")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

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

    # ── 표 셀수 (넘치는 칸은 렌더에서 **조용히 사라진다**) ──────────────────
    print("\n=== 표 셀수 점검 (헤더 ≠ 행 → 렌더에서 칸이 버려지거나 밀린다)")
    n_tbl_bad = 0
    for doc in (CMP_DFT, CMP_DEM, SE_INDEX, DEM_INDEX):
        if not doc.exists():
            continue
        bad = check_tables(doc.read_text(encoding="utf-8"))
        n_tbl_bad += len(bad)
        print(f"   {doc.name:28} {'✅ 0건' if not bad else f'⛔ {len(bad)}건'}")
        for ln, got, want, head in bad[:12]:
            print(f"        {ln}행  {got}칸 → 헤더 {want}칸   {head}")
        if len(bad) > 12:
            print(f"        … 외 {len(bad)-12}행")
    return 1 if (missing or n_tbl_bad) else 0


if __name__ == "__main__":
    sys.exit(main())
