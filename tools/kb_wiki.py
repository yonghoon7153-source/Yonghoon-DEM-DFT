#!/usr/bin/env python3
"""kb_wiki.py — kb 위키 하네스: lint | index | new  (stdlib 전용).

kb/SCHEMA.md (2026-08-11 채택) 의 기계 검사기. llm-wiki-kit 의 lint.py 를 이 repo 에
번안한 것 — [[wikilink]] 대신 **repo-상대경로 존재 검사**, 수동 index 대신 **생성 index**.

  python3 tools/kb_wiki.py lint          # 0 errors 가 마무리 조건 (경고는 레거시 허용)
  python3 tools/kb_wiki.py index         # kb/index.md 재생성
  python3 tools/kb_wiki.py new results my_slug        # frontmatter 스캐폴드
  python3 tools/kb_wiki.py new questions my_question  # RQ 카드 스캐폴드

설계 결정 (kb/methodology/llm_wiki_adoption_2026_08_11.md):
  · frontmatter 는 **새 문서부터** — 있는 문서만 깊이 검사, 레거시 199개는 소급 없음.
  · 경로 검사: frontmatter 문서의 깨진 경로 = error, 레거시 = warning (상위 20개만 출력).
  · explored 는 사람만 바꾼다 — lint 는 값 검증만 하고 강제하지 않는다.
"""
import datetime
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KB = REPO / "kb"

#: index 에 전 파일을 나열하는 디렉터리 (관리 대상)
MANAGED = ["concepts", "physics", "methodology", "results", "reviews", "reports",
           "projects", "questions", "syntheses", "platforms", "descriptors",
           "papers", "literature_db", "seminars"]
#: 개수만 표시 (생성물·대용량)
SUMMARIZED = ["elements", "templates"]

ENUMS = {
    "confidence": {"high", "medium", "low"},
    "verificationStatus": {"unverified", "verified", "disputed", "retracted"},
    "explored": {"true", "false"},
    "authoredBy": {"agent", "human"},
    "effort": {"low", "medium", "high", "max"},
    "claimType": {"definition", "empirical", "theoretical", "prescriptive",
                  "interpretive", "mixed"},
    "evidenceScope": {"single-source", "multi-source-primary", "multi-source-mixed",
                      "synthesis-only", "user-original"},
}
RQ_STATUS = {"open", "active", "answered", "abandoned"}
REQ_KEYS = ["title", "date", "tags", "status"]          # 우리 레거시 4키가 최소
#: 본문 필수 절 (SCHEMA 문서 3분법)
RQ_SECTIONS = ["왜 중요한가", "Evidence For", "Evidence Against", "결정 실험", "Status Log"]
SY_SECTIONS = ["Thesis", "Counter-arguments", "Gap"]

#: repo-상대경로로 취급하는 접두 (서버 절대경로 /data/... 는 자동 제외)
PATH_RE = re.compile(
    r"(?<![\w/])((?:db|tools|kb|docs|litdb|webapp|runs)/[\w][\w./-]*\.(?:py|json|md|csv|sh|vasp|xyz|cif|png|txt|yaml|yml|tsv|in|UPF|upf))")
#: 스킵: 글롭·플레이스홀더가 섞인 토큰
SKIP_TOKEN = re.compile(r"[*{}<>]")
STALE_STATUS = re.compile(r"대기|HOLD|진행|보류|pending", re.I)
STALE_DAYS = 14


def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$", line)
        if km:
            fm[km.group(1)] = km.group(2).strip()
    return fm, text[m.end():]


def all_pages():
    out = []
    for d in MANAGED:
        dd = KB / d
        if dd.is_dir():
            out += sorted(dd.glob("*.md"))
    return out


def title_of(p, fm):
    if fm and fm.get("title"):
        return fm["title"].strip('"')
    for line in p.read_text(errors="ignore").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return p.stem


# ─────────────────────────────────────────────────────────────────────────────
def cmd_lint():
    errors, warnings = [], []
    legacy_missing = []            # 레거시 문서의 깨진 경로 (요약 출력)
    pages = all_pages()
    n_fm = 0
    today = datetime.date.today()

    for p in pages:
        text = p.read_text(errors="ignore")
        fm, body = parse_fm(text)
        rel = p.relative_to(REPO)
        has_fm = fm is not None
        if has_fm:
            n_fm += 1
            for k in REQ_KEYS:
                if k not in fm:
                    errors.append(f"{rel}: frontmatter 에 `{k}` 없음")
            for k, allowed in ENUMS.items():
                v = fm.get(k, "")
                if v and v not in allowed:
                    errors.append(f"{rel}: `{k}: {v}` ∉ {sorted(allowed)}")
            if fm.get("verificationStatus") == "verified" and \
                    ("verifiedAt" not in fm or "verifiedBy" not in fm):
                errors.append(f"{rel}: verified 인데 verifiedAt/verifiedBy 없음")
            if fm.get("evidenceScope") == "single-source" and fm.get("confidence") == "high":
                warnings.append(f"{rel}: single-source 인데 confidence high — 근거 폭이 상한 (SCHEMA)")
            if fm.get("authoredBy") == "agent" and "effort" not in fm:
                warnings.append(f"{rel}: authoredBy agent 인데 effort 없음")
            # 고여 있는 대기 문서 — 오늘 만든 '회신 대기' 류가 조용히 늙는 것 방지
            st = fm.get("status", "")
            ref_date = fm.get("updated") or fm.get("date") or ""
            try:
                dd = datetime.date.fromisoformat(ref_date)
                if STALE_STATUS.search(st) and (today - dd).days > STALE_DAYS:
                    warnings.append(f"{rel}: status '{st}' 인 채 {(today - dd).days}일 — "
                                    f"닫혔으면 status 갱신, 아니면 후속 조치")
            except ValueError:
                if ref_date:
                    errors.append(f"{rel}: date/updated 파싱 불가: {ref_date}")
            if p.parent.name == "questions":
                stq = fm.get("status", "")
                if stq not in RQ_STATUS:
                    errors.append(f"{rel}: questions/ 는 status ∈ {sorted(RQ_STATUS)} (지금 '{stq}')")
                for sec in RQ_SECTIONS:
                    if sec not in body:
                        errors.append(f"{rel}: 필수 절 없음 — '{sec}'")
            if p.parent.name == "syntheses":
                for sec in SY_SECTIONS:
                    if sec not in body:
                        errors.append(f"{rel}: 필수 절 없음 — '{sec}'")
        elif p.parent.name in ("questions", "syntheses"):
            errors.append(f"{rel}: 신설 디렉터리는 frontmatter 필수 (tools/kb_wiki.py new)")

        # 경로 인용 존재 검사 — 이 repo 의 '링크' 검사.
        # 'lint-skip-path' 가 있는 줄은 제외 (존재하지 않는 경로의 인용/역사 기록용 —
        # 예: 리뷰어가 잘못 인용한 파일명, repo 미수록 서버 전용 스크립트 목록).
        seen_tok = set()
        for line in text.splitlines():
            if "lint-skip-path" in line:
                continue
            for tok in PATH_RE.findall(line):
                if tok in seen_tok or SKIP_TOKEN.search(tok):
                    continue
                seen_tok.add(tok)
                if not (REPO / tok).exists():
                    if has_fm:
                        errors.append(f"{rel}: 깨진 경로 인용 — {tok}")
                    else:
                        legacy_missing.append(f"{rel}: {tok}")

    # index 신선도 — 생성물이 현실과 맞나
    idx = KB / "index.md"
    if not idx.is_file():
        errors.append("kb/index.md 없음 — python3 tools/kb_wiki.py index")
    else:
        m = re.search(r"managed-files: (\d+)", idx.read_text())
        if not m or int(m.group(1)) != len(pages):
            errors.append(f"kb/index.md 가 낡음 (기록 {m.group(1) if m else '?'} vs 실제 "
                          f"{len(pages)}) — python3 tools/kb_wiki.py index 재실행")

    # litdb INDEX 커버리지 (경고 — litdb 는 자체 관리).
    # INDEX 가 여럿이다 (INDEX.md=DFT/전지 · INDEX_DEM.md=DEM …) — 전부 합쳐서 본다.
    idx_files = sorted((REPO / "litdb").glob("INDEX*.md"))
    if idx_files:
        it = "\n".join(f.read_text(errors="ignore") for f in idx_files)
        missing = [f.stem for f in sorted((REPO / "litdb" / "papers").glob("*.md"))
                   if f.stem not in it and not f.stem.startswith("_")]
        if missing:
            warnings.append(f"litdb INDEX*.md 어디에도 없는 digest {len(missing)}개: "
                            + ", ".join(missing[:5]) + ("…" if len(missing) > 5 else ""))

    print("=== kb lint ===")
    print(f"문서 {len(pages)}개 (frontmatter {n_fm} · 레거시 {len(pages) - n_fm} — 소급 없음)")
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(" ✗", e)
    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings:
        print(" ⚠", w)
    if legacy_missing:
        print(f"\n레거시 깨진 경로 {len(legacy_missing)}건 (참고용 상위 20 — 소급 수정 안 함):")
        for x in legacy_missing[:20]:
            print("  ·", x)
    if not errors:
        print("\nRESULT: 0 errors")
    return 1 if errors else 0


# ─────────────────────────────────────────────────────────────────────────────
def cmd_index():
    pages = all_pages()
    lines = ["# kb 카탈로그 (생성물 — 손으로 고치지 말 것)", "",
             f"> `python3 tools/kb_wiki.py index` 가 만든다 · {datetime.date.today()} · "
             f"managed-files: {len(pages)}", "",
             "규칙: kb/SCHEMA.md · 열린 질문: kb/questions/ · 논지 카드: kb/syntheses/ · "
             "원장: kb/open_items.md · 문헌: litdb/INDEX.md", ""]
    for d in MANAGED:
        dd = KB / d
        if not dd.is_dir():
            continue
        files = sorted(dd.glob("*.md"))
        if not files:
            continue
        lines.append(f"## {d}/ ({len(files)})")
        for p in files:
            fm, _ = parse_fm(p.read_text(errors="ignore"))
            t = title_of(p, fm)
            mark = ""
            if fm:
                vs = fm.get("verificationStatus", "")
                if vs == "retracted":
                    mark = " ⛔철회"
                elif vs == "disputed":
                    mark = " ⚠disputed"
                if fm.get("explored") == "false":
                    mark += " ○미열람"
                if p.parent.name == "questions":
                    mark += f" [{fm.get('status', '?')}]"
            lines.append(f"- `kb/{d}/{p.name}` — {t}{mark}")
        lines.append("")
    for d in SUMMARIZED:
        dd = KB / d
        if dd.is_dir():
            n = len(list(dd.glob("*")))
            lines.append(f"## {d}/ — {n}개 (생성물/템플릿, 목록 생략)")
    lines += ["", f"## litdb/ — digest {len(list((REPO / 'litdb' / 'papers').glob('*.md')))}개 "
              f"(정본 목록: litdb/INDEX.md)"]
    (KB / "index.md").write_text("\n".join(lines) + "\n")
    print(f"→ kb/index.md (관리 문서 {len(pages)}개)")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
SCAFFOLD_RQ = """## 질문

(1문장)

## 왜 중요한가

## 가설

## Evidence For

## Evidence Against

## 결정 실험

무엇이 이 질문을 결판내나.

## Status Log

- {today}: 카드 생성.
"""
SCAFFOLD_SY = """## Thesis

(1문장)

## Argument

## Counter-arguments

(반론은 **보존** — 반박되더라도 지우지 않고 반박을 병기)

## Gap

(아직 비어 있는 근거)
"""


def cmd_new(d, slug):
    if not (KB / d).is_dir():
        sys.exit(f"⛔ kb/{d} 가 없다 (관리 대상: {', '.join(MANAGED)})")
    p = KB / d / f"{slug}.md"
    if p.exists():
        sys.exit(f"⛔ 이미 있다: {p}")
    today = datetime.date.today().isoformat()
    fm = ["---", f"title: {slug}", f"date: {today}", f"updated: {today}", "tags: []",
          "status: open" if d == "questions" else "status: 진행",
          "confidence: medium", "verificationStatus: unverified", "explored: false",
          "authoredBy: agent", "effort: medium", "claimType: empirical",
          "evidenceScope: single-source"]
    if d == "questions":
        fm.append("feedsInto: ")
    if d == "syntheses":
        fm.append("targetVenue: ")
    fm.append("---")
    body = SCAFFOLD_RQ.format(today=today) if d == "questions" else \
        SCAFFOLD_SY if d == "syntheses" else "\n# " + slug + "\n"
    p.write_text("\n".join(fm) + "\n\n" + body)
    print(f"→ {p}\n   (index 재생성 잊지 말 것: python3 tools/kb_wiki.py index)")
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("lint", "index", "new"):
        print(__doc__)
        return 1
    if sys.argv[1] == "lint":
        return cmd_lint()
    if sys.argv[1] == "index":
        return cmd_index()
    if len(sys.argv) != 4:
        sys.exit("쓰기: python3 tools/kb_wiki.py new <dir> <slug>")
    return cmd_new(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    sys.exit(main())
