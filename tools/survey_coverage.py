#!/usr/bin/env python3
"""survey_coverage.py — 조사가 **실제로 몇 %를 봤나** 를 센다.

    python3 tools/survey_coverage.py <조사폴더>              # 요약표
    python3 tools/survey_coverage.py <조사폴더> --area tools  # 그 영역의 미인용 목록
    python3 tools/survey_coverage.py --selftest

왜 생겼나
  2026-09-08 밤 전수조사(29 에이전트 · 6.7 M 토큰 · 3.2 h)가 552 발견을 냈고 스스로를
  "전수" 라고 불렀다. 그런데 2026-09-09 에 273 캐스케이드가 Stage 04 에서 전멸했고,
  그 원인(`tier_cascade.sh` 가 `run_anneal.py --seed` 를 안 넘김)은 조사가 **한 번도
  열지 않은 파일**에 있었다. 조사 문서 자신이 적어 놓았다 — *"cascade 11개 전부의
  본문", "run_anneal … 본문" 못 봄*. 그리고 `tier_cascade.sh` 를 **"끝난 캠페인"** 으로
  분류해 P0 대상에서 뺐다.
  실측 커버리지는 **34.3 %** 였다 (tools 25.8 % · webapp 86.8 %).
  ⇒ "전수조사 했다" 는 **검증 가능한 주장**이어야 한다. 그걸 재는 게 이 도구다.

⛔ 자기오염 (2026-09-09 실측 — 이 도구가 스스로에게 당한 것)
  `--json .v3_survey/_UNCITED.json` 로 **측정 결과를 측정 대상 폴더 안에** 떨궜더니,
  다음 측정에서 그 파일의 1,381개 경로가 전부 "인용됨" 으로 재분류돼 **34.3 % → 99.7 %** 가
  됐다. 커버리지 지표가 한 번 재는 순간 스스로를 100 % 로 만든 것이다.
  ⇒ 이제 ① `--json` 대상이 조사 폴더 안이면 **거부**하고 ② 스캔 중 자기 출력 모양의
  JSON(영역→경로목록)을 만나면 **건너뛰고 경고**한다. selftest 가 이 경로를 음성으로 잡는다.

⛔ 이 도구가 **못 하는 것** (제일 중요한 절)
  · **"인용됐다 = 제대로 봤다" 가 아니다.** 파일명이 한 번 스쳐도 인용으로 센다.
    그래서 여기 나오는 수는 **상한**이고 실제 정독률은 그보다 낮다.
    실측으로 확인됐다: 2026-09-09 사고 파일 3개 중 `tier_cascade.sh`·`master_batch_273.sh`
    2개가 이미 "본" 쪽(34.3 %)에 들어 있었다 — 파일명만 언급됐고 본문은 안 열렸다.
  · 반대로 **안 봐도 되는 파일**을 못 가른다 — 화석·일회성 복구 스크립트까지 분모에 넣는다.
    분모를 좁히려면 호출자가 `--glob` 으로 범위를 준다.
  · 조사의 **품질**은 안 본다. 잘못된 판정을 걸러내지 못한다.
  · 파일명이 흔한 것(`README.md` · `__init__.py`)은 다른 곳의 언급에 묻어 통과한다.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

#: 세는 확장자. 바이너리·데이터 덤프는 조사 대상이 아니다.
EXTS = (".py", ".sh", ".json", ".md", ".html", ".css", ".js")
#: 영역 — 이 순서로 앞에서 맞는 첫 번째를 쓴다.
AREAS = ("tools/", "kb/", "db/", "webapp/", "litdb/", "docs/", "research_agent/")
_PATH_RE = re.compile(r"[A-Za-z0-9_./-]+\.(?:py|sh|json|md|html|css|js|csv|cif|xyz)")


def _area(rel: str) -> str:
    for a in AREAS:
        if rel.startswith(a):
            return a.rstrip("/")
    return "(root/기타)"


def is_own_output(text: str) -> bool:
    """이 도구가 뱉은 미인용 목록인가 — {영역: [경로…]} 모양이면 그렇다.

    자기 출력을 조사 문서로 세면 미인용 파일이 전부 인용됨으로 뒤집힌다
    (2026-09-09: 34.3 % → 99.7 %). 이름이 아니라 **모양**으로 판정한다 —
    `--json` 대상 이름은 호출자가 아무렇게나 줄 수 있기 때문이다.
    """
    try:
        obj = json.loads(text)
    except Exception:                                   # noqa: BLE001
        return False
    if not isinstance(obj, dict) or not obj:
        return False
    return all(isinstance(v, list) and v and all(isinstance(x, str) for x in v)
               and any("/" in x for x in v) for v in obj.values())


def cited_paths(survey_dir: Path, warn=None) -> set:
    """조사 문서들이 언급한 경로·파일명 전부. 자기 출력은 뺀다."""
    out = set()
    for p in sorted(survey_dir.rglob("*")):
        if not p.is_file() or p.suffix not in (".md", ".json", ".txt"):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if p.suffix == ".json" and is_own_output(text):
            if warn is not None:
                warn.append(str(p))
            continue
        for m in _PATH_RE.finditer(text):
            out.add(m.group(0).lstrip("./"))
    return out


def tracked_files(root: Path, globs=None) -> list:
    try:
        files = subprocess.check_output(["git", "-C", str(root), "ls-files"],
                                        text=True).split()
    except (OSError, subprocess.CalledProcessError):
        files = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]
    files = [f for f in files if f.endswith(EXTS)]
    if globs:
        import fnmatch
        files = [f for f in files if any(fnmatch.fnmatch(f, g) for g in globs)]
    return sorted(files)


def coverage(survey_dir: Path, root: Path = REPO, globs=None, warn=None):
    """→ (영역별 {n, miss}, {영역: [미인용 파일…]})"""
    cited = cited_paths(survey_dir, warn)
    cited_base = {c.rsplit("/", 1)[-1] for c in cited}
    stat = collections.defaultdict(lambda: {"n": 0, "miss": 0})
    missing = collections.defaultdict(list)
    for f in tracked_files(root, globs):
        a = _area(f)
        stat[a]["n"] += 1
        if f not in cited and f.rsplit("/", 1)[-1] not in cited_base:
            stat[a]["miss"] += 1
            missing[a].append(f)
    return dict(stat), dict(missing)


def _print(stat, missing, area=None, limit=0):
    if area:
        files = missing.get(area, [])
        print(f"# {area} 미인용 {len(files)}개")
        for f in (files[:limit] if limit else files):
            print(" ", f)
        if limit and len(files) > limit:
            print(f"  … 외 {len(files) - limit}개")
        return
    print(f"{'영역':<14}{'추적':>7}{'미인용':>8}   커버리지")
    tot = miss = 0
    for a in sorted(stat, key=lambda x: -stat[x]["n"]):
        n, m = stat[a]["n"], stat[a]["miss"]
        tot += n
        miss += m
        print(f"{a:<14}{n:>7}{m:>8}   {100 * (1 - m / n):5.1f}%" if n else "")
    if tot:
        print(f"{'합계':<14}{tot:>7}{miss:>8}   {100 * (1 - miss / tot):5.1f}%")
    print("\n⚠ 이 수는 **상한**이다 — 파일명이 한 번 스쳐도 인용으로 센다. 실제 정독률은 더 낮다.")


def selftest() -> int:
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as d:
        # ⚠ 조사 폴더를 **측정 대상 밖**에 둔다. 안에 두면 조사 문서 자신이 분모에
        #   들어가 자기오염 검사가 무엇을 쟀는지 흐려진다 (main() 도 --json 을 폴더
        #   안에 쓰는 것을 거부하므로, 이게 실제 운용 배치이기도 하다).
        t = Path(d) / "repo"
        (t / "tools").mkdir(parents=True)
        (t / "webapp").mkdir()
        for rel in ("tools/seen.py", "tools/unseen.py", "webapp/app.py"):
            (t / rel).write_text("x\n")
        sv = Path(d) / "survey"
        sv.mkdir()
        # 조사가 seen.py 와 app.py 만 언급했다
        (sv / "a.md").write_text("tools/seen.py 를 봤고 webapp/app.py 도 봤다\n")
        stat, missing = coverage(sv, t)
        # ⛔음성: 안 본 파일을 못 잡으면 실패
        if missing.get("tools") != ["tools/unseen.py"]:
            print("⛔ selftest: 미인용 파일을 못 잡았다:", missing)
            ok = False
        # ⛔음성: 본 파일을 미인용으로 오탐하면 실패
        if "webapp" in missing and missing["webapp"]:
            print("⛔ selftest: 인용된 파일을 미인용으로 오탐했다:", missing["webapp"])
            ok = False
        if stat["tools"]["n"] != 2 or stat["tools"]["miss"] != 1:
            print("⛔ selftest: 집계가 틀렸다:", stat)
            ok = False
        # ⛔음성: 파일명만 같아도 인용으로 세는 **알려진 한계**가 실제로 그런지
        #   (문서에 적은 한계가 사실인지 확인한다 — 한계를 적어 놓고 틀리면 더 나쁘다)
        (sv / "b.md").write_text("어디선가 unseen.py 라고만 적혀 있다\n")
        _, m2 = coverage(sv, t)
        if m2.get("tools"):
            print("⛔ selftest: 파일명만으로 통과하는 한계가 문서와 다르다:", m2)
            ok = False
        (sv / "b.md").unlink()
        # ⛔음성 (2026-09-09 실제 사고): 자기 출력을 조사 폴더 안에 떨궈도
        #   커버리지가 흔들리면 안 된다. 실측에서 34.3 % → 99.7 % 로 뒤집혔었다.
        base_stat, base_miss = coverage(sv, t)
        (sv / "_UNCITED.json").write_text(
            json.dumps({"tools": ["tools/unseen.py"]}, ensure_ascii=False), encoding="utf-8")
        warn = []
        stat2, miss2 = coverage(sv, t, warn=warn)
        if (stat2, miss2) != (base_stat, base_miss):
            print("⛔ selftest: 자기 출력이 커버리지를 바꿨다 (자기오염):", stat2)
            ok = False
        if not warn:
            print("⛔ selftest: 자기 출력을 건너뛰고도 경고를 안 남겼다 — 조용히 넘기면 안 된다")
            ok = False
        # ⛔음성: 남의 JSON(같은 확장자)까지 삼키면 안 된다 — 모양이 다르면 세야 한다
        (sv / "notes.json").write_text(
            json.dumps({"본문": "tools/unseen.py 를 봤다"}, ensure_ascii=False), encoding="utf-8")
        _, miss3 = coverage(sv, t)
        if miss3.get("tools"):
            print("⛔ selftest: 자기 출력 판정이 너무 넓다 — 평범한 조사 JSON 도 버렸다:", miss3)
            ok = False
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("survey_dir", nargs="?", help="조사 결과 폴더 (예: .v3_survey)")
    ap.add_argument("--root", default=str(REPO))
    ap.add_argument("--area", help="그 영역의 미인용 목록만")
    ap.add_argument("--glob", nargs="*", help="분모를 좁힌다 (예: 'tools/**')")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--json", help="미인용 목록을 이 경로에 JSON 으로")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.survey_dir:
        ap.error("조사 폴더를 주거나 --selftest 를 써라")
    sv = Path(a.survey_dir).resolve()
    if a.json:
        # ⛔ 자기오염 차단 (2026-09-09): 결과를 조사 폴더 안에 쓰면 다음 측정이 그걸
        #   조사 문서로 읽어 미인용 파일 전부가 "인용됨" 이 된다. 실측 34.3 % → 99.7 %.
        out = Path(a.json).resolve()
        if sv == out or sv in out.parents:
            ap.error(f"⛔ --json 대상이 조사 폴더 안이다 ({out}) — 다음 측정이 자기 출력을 "
                     f"조사 문서로 읽어 커버리지가 100 % 로 뒤집힌다. 폴더 밖에 써라.")
    warn = []
    stat, missing = coverage(sv, Path(a.root), a.glob, warn=warn)
    for w in warn:
        print(f"⚠ 자기 출력으로 보여 스캔에서 뺐다: {w}")
    if a.json:
        Path(a.json).write_text(json.dumps(missing, ensure_ascii=False, indent=1),
                                encoding="utf-8")
        print(f"미인용 목록 → {a.json}")
    _print(stat, missing, a.area, a.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
