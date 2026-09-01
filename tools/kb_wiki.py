#!/usr/bin/env python3
"""kb_wiki.py — kb 위키 하네스: lint | index | new | env  (stdlib 전용).

kb/SCHEMA.md (2026-08-11 채택) 의 기계 검사기. llm-wiki-kit 의 lint.py 를 이 repo 에
번안한 것 — [[wikilink]] 대신 **repo-상대경로 존재 검사**, 수동 index 대신 **생성 index**.

  python3 tools/kb_wiki.py lint          # 0 errors 가 마무리 조건 (경고는 레거시 허용)
  python3 tools/kb_wiki.py index         # kb/index.md 재생성
  python3 tools/kb_wiki.py new results my_slug        # frontmatter 스캐폴드
  python3 tools/kb_wiki.py new questions my_question  # RQ 카드 스캐폴드
  python3 tools/kb_wiki.py env           # **낡을 수 있는 환경 주장** 목록 + 검증 스크립트
  python3 tools/kb_wiki.py env --script > /tmp/chk.sh   # 서버에서 돌릴 검사 스크립트

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
    # 🔴 2026-08-31 — 나이만 보는 규칙은 '회신이 왔는데 status 가 대기' 를 못 봤다.
    #   프롬프트 27건이 그렇게 굳어 있었다. 증거와 status 의 **모순**을 직접 본다.
    try:
        _, _contra = review_chain()
        for _n, _st, _why in _contra:
            warnings.append("kb/reviews/%s: status '%s' 인데 %s" % (_n, _st, _why))
    except Exception as _e:                                      # noqa: BLE001
        warnings.append("리뷰 사슬 검사 실패: %r" % _e)
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
    # 레거시 깨진 경로는 **한 줄 요약만** — 소급 수정을 안 하므로 매번 20줄을 찍는 건
    # 순수 낭비다(전체 출력의 85%였다). 목록이 필요하면 `lint --legacy`.
    if legacy_missing:
        if "--legacy" in sys.argv:
            print(f"\n레거시 깨진 경로 {len(legacy_missing)}건 (소급 수정 안 함):")
            for x in legacy_missing:
                print("  ·", x)
        else:
            print(f"\n레거시 깨진 경로 {len(legacy_missing)}건 (목록은 lint --legacy)")
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



# ── env: 낡을 수 있는 환경 주장 ──────────────────────────────────────────────
#   왜 필요한가 (2026-08-12): kb 가 "Nd frozen-4f PP 없음"·"gabia 에 neb.x 미설치" 라고
#   적고 있었는데 둘 다 **있었다**. 후자는 "UMA NEB 로 전체 대체" 라는 설계 결정의
#   근거였다. 판정·논거는 안 낡지만 **환경 상태는 낡는다** — 그걸 골라내 검증 가능하게 한다.
#
#   이 검사가 **못 하는 것**: 문장의 뜻을 이해하지 못한다. 패턴으로 후보를 고를 뿐이라
#   오탐이 섞인다. 사람이 목록을 보고 고르라고 만든 것이지 자동 판정기가 아니다.
EXIST_WORDS = ("미설치", "설치", "없다", "없음", "있다", "존재", "빌드에", "하나뿐",
               "처음부터 없", "안 들어", "못 찾", "빠져")
ART_RE = re.compile(r"(/(?:data|scratch|home|opt|usr)/[\w./+-]+|~/[\w./+-]+|"
                    r"\b\w+\.x\b|\b[\w.+-]+\.UPF\b|\bconda\b|\bpseudo\b)")
#: 검증 명령이 근처에 있으면 "재확인 가능" 으로 본다
VERIFY_HINT = re.compile(r"(ls |which |pgrep|--inventory|watch_|nvidia-smi|test -[fdx])")


#: 바로 아래에 이 표시가 붙은 주장은 **이미 정정/해소**된 것이다. 계속 띄우면
#:  도구가 늑대소년이 되고 아무도 안 읽는다 (2026-08-12: neb.x 2건이 그랬다).
CORRECTED_RE = re.compile(r"낡음|정정|해소|폐기|superseded|⛔|✅")


def scan_env(root=None):
    """(파일, 줄번호, 문장, 아티팩트들, 검증힌트있음, 정정됨) 목록."""
    hits = []
    for f in sorted((root or KB).rglob("*.md")):
        if f.name in ("index.md", "SCHEMA.md"):
            continue
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for i, ln in enumerate(lines, 1):
            if not any(w in ln for w in EXIST_WORDS):
                continue
            arts = sorted(set(ART_RE.findall(ln)))
            if not arts:
                continue
            near = "\n".join(lines[max(0, i - 4):i + 3])
            # 아래 4줄 안에 정정 표시가 있으면 이미 손본 주장이다
            below = "\n".join(lines[i:i + 4])
            corrected = bool(CORRECTED_RE.search(below))
            try:
                rel = str(f.relative_to(REPO))
            except ValueError:
                rel = str(f)                      # selftest 의 임시 경로
            hits.append((rel, i, ln.strip()[:150], arts,
                         bool(VERIFY_HINT.search(near)), corrected))
    return hits


def cmd_env(as_script=False):
    hits = scan_env()
    arts = {}
    for f, i, _ln, aa, _v, _c in hits:
        for a in aa:
            arts.setdefault(a, []).append(f"{f}:{i}")
    if as_script:
        print("#!/usr/bin/env bash")
        print("# kb 의 환경 주장 검증 — 서버에서 돌리고 출력을 그대로 회수한다.")
        print("# (kb_wiki.py env --script 로 생성. 손으로 고치지 말 것)")
        for a in sorted(arts):
            if a in ("conda", "pseudo"):
                continue
            # ⚠ `(ls ... | head -1) || echo MISSING` 은 종료코드가 head 것이라
            #   **MISSING 이 절대 안 찍힌다**. 변수에 받아 비어 있는지로 판정한다.
            if a.endswith(".x") and "/" not in a:
                print(f'p=$(ls -d /data/apps/qe-*/bin/{a} /data/work/apps/qe-*/bin/{a} '
                      f'/scratch/*/kgy/apps/qe-*/bin/{a} 2>/dev/null | head -1); '
                      f'printf "%-42s %s\\n" "{a}" "${{p:-MISSING}}"')
            else:
                print(f'printf "%-42s %s\\n" "{a}" '
                      f'"$([ -e \'{a}\' ] && echo OK || echo MISSING)"')
        return 0
    fixed = [h for h in hits if h[5]]
    noverify = [h for h in hits if not h[4] and not h[5]]
    print(f"환경 주장 후보 {len(hits)}건 · 아티팩트 {len(arts)}종 · "
          f"이미 정정됨 {len(fixed)}건 · 검증 명령도 정정도 **없는** 것 "
          f"{len(noverify)}건" + ("  (정정본 목록은 --corrected)" if fixed else ""))
    print("\n── 아티팩트별 (많이 언급된 순) ──")
    for a, where in sorted(arts.items(), key=lambda kv: -len(kv[1]))[:18]:
        print(f"  {a:38s} {len(where):2d}곳  {', '.join(where[:3])}"
              + (" …" if len(where) > 3 else ""))
    if fixed and "--corrected" in sys.argv:
        print("\n── 이미 정정된 주장 (참고) ──")
        for f, i, ln, _aa, _v, _c in fixed[:20]:
            print(f"  {f}:{i}\n     {ln[:100]}")
    print("\n── 검증 명령도 정정도 없는 주장 (여기부터 낡는다) ──")
    for f, i, ln, aa, _v, _c in noverify[:20]:
        print(f"  {f}:{i}\n     {ln}")
    if len(noverify) > 20:
        print(f"  … 외 {len(noverify) - 20}건")
    print("\n검증 스크립트:  python3 tools/kb_wiki.py env --script > /tmp/chk.sh"
          "  → 서버에서 bash /tmp/chk.sh")
    return 0


def selftest_env():
    import tempfile
    td = Path(tempfile.mkdtemp(prefix="kbenv_"))
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    (td / "a.md").write_text("- **QE neb.x**: 미설치 (확인됨, 2026-06-01)\n")
    (td / "b.md").write_text("갭은 fixed-occ nscf 고유값이 정본이다. DOS 문턱 판독 금지.\n")
    (td / "c.md").write_text("확인:  ls /data/apps/qe/bin/ph.x\n\nph.x 가 빌드에 없다.\n")
    (td / "d.md").write_text("Nd UPF 가 /data/work/pseudo 에 하나뿐이고 z=14.0 이다.\n")
    h = scan_env(td)
    files = {x[0].split("/")[-1] for x in h}
    chk("a.md" in files, "존재 주장 + 바이너리 → 잡는다")
    chk("d.md" in files, "존재 주장 + 경로 → 잡는다")
    # 음성: 판정·논거 문장은 잡으면 안 된다 (그건 안 낡는다)
    chk("b.md" not in files, "판정 문장(환경 아님)은 **안 잡는다**")
    # 검증 명령이 근처에 있으면 '없는 것' 목록에서 빠져야 한다
    cc = [x for x in h if x[0].endswith("c.md")]
    chk(bool(cc) and cc[0][4], "근처에 ls 가 있으면 '검증 가능' 으로 표시")
    aa = [x for x in h if x[0].endswith("a.md")]
    chk(bool(aa) and not aa[0][4], "검증 명령 없으면 '없음' 으로 표시")
    # ── 정정 감지 (2026-08-12) ──
    #   이미 손본 주장을 계속 띄우면 도구가 늑대소년이 되고 아무도 안 읽는다.
    #   실제로 neb.x 2건이 정정 주석까지 붙었는데 매번 최상위로 올라왔다.
    chk(bool(aa) and not aa[0][5], "정정 주석 없으면 corrected=False")
    (td / "e.md").write_text(
        "- **QE neb.x**: 미설치 (확인됨, 2026-06-01)\n\n"
        "> ⛔ **낡음 (2026-08-12 정정)** — 있다. /data/apps/qe-7.4.1-gpu/bin/neb.x\n")
    ee = [x for x in scan_env(td) if x[0].endswith("e.md") and "미설치" in x[2]]
    chk(bool(ee) and ee[0][5], "바로 아래 정정 주석 → corrected=True")
    # ★ 음성: **멀리 떨어진** 정정은 그 주장의 것이 아니다 (4줄 창 밖)
    (td / "f.md").write_text(
        "- **QE neb.x**: 미설치\n" + "\n" * 8 + "> ⛔ 낡음 — 다른 얘기\n")
    ff = [x for x in scan_env(td) if x[0].endswith("f.md")]
    chk(bool(ff) and not ff[0][5],
        "멀리 있는 정정은 안 세어 준다 (아무 ⛔ 나 있으면 통과가 아니다)")
    import shutil
    shutil.rmtree(td, ignore_errors=True)
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1



# ── 리뷰 사슬 (2026-08-31) ────────────────────────────────────────────────
#: 프롬프트 파일명 규약: codex_<라벨>_prompt_<주제>_<날짜>.md
#: 회신 파일명은 **라벨이 어긋난다** — 실물에 둘 다 있다:
#:    codex_AT_reply_...  ← codex_AT_prompt_...   (같은 라벨)
#:    codex_AV_reply_...  ← codex_AU_prompt_...   (다음 라벨)
#: 그래서 파일명으로 짝을 추측하지 않는다. 본문의 `요청:` 역링크가 정본이고,
#: 없으면 주제 slug 일치를 쓴다.
#: ⚠ 파일명 날짜는 `2026_08_31` — **밑줄**이다 (frontmatter 의 `2026-08-31` 과 다르다)
REV_PROMPT = re.compile(r"^codex_([A-Z]{1,2}\d?)_prompt_(.+)_(\d{4}_\d{2}_\d{2})\.md$")
REV_REPLY = re.compile(r"^codex_([A-Z]{1,2}\d?)_(?:reply_)?(.+?)(?:_reply)?_(\d{4}_\d{2}_\d{2})\.md$")
#: status 가 이 꼴이면 '아직 안 보냈다' 는 주장이다
REV_WAITING = re.compile(r"발송\s*(대기|전)|미발송")
#: 회신 본문이 프롬프트를 가리키는 역링크
REV_BACKLINK = re.compile(r"요청[:\s]*`?(kb/reviews/[^\s`]+\.md)`?")
#: 판정을 인용한 흔적 — 회신에만 있는 것들 (P0 번호·해제조건·Q 답)
REV_VERDICT = re.compile(r"회신\s+([A-Z]{1,2}\d?)\s*(?:P0|P1|해제조건|판정|Q\d)")


def review_chain():
    """kb/reviews 를 훑어 (프롬프트, 회신, 모순) 을 낸다.

    → (records, contradictions)
      records: dict(label, prompt, date, status, reply, answered_by, evidence)

    ⛔ 이 함수가 **못 하는 것**
      · 회신이 대화에만 있고 파일이 없으면 `reply=None` 이다 — 인용 흔적으로
        '받았다' 고 **추정**할 뿐 원문을 복원하지 못한다.
      · 라벨이 캠페인 사이에 재사용된다 (S·T·U 가 각 2개). 인용 횟수는 두 캠페인이
        **합산**되므로 라벨만으로 어느 쪽인지 못 가른다 — 그래서 인용은 보조 증거다.
    """
    rd = REPO / "kb" / "reviews"
    prompts, replies = {}, []
    for p in sorted(rd.glob("*.md")):
        m = REV_PROMPT.match(p.name)
        if m:
            fm, _ = parse_fm(p.read_text(errors="ignore"))
            prompts[p.name] = {"label": m.group(1), "slug": m.group(2),
                               "date": m.group(3).replace("_", "-"), "path": p,
                               "status": (fm or {}).get("status", "(frontmatter 없음)")}
            continue
        if "_reply" in p.name:
            m2 = REV_REPLY.match(p.name)
            t = p.read_text(errors="ignore")
            bl = REV_BACKLINK.search(t)
            replies.append({"path": p, "name": p.name,
                            "label": m2.group(1) if m2 else "?",
                            "slug": m2.group(2) if m2 else "",
                            "backlink": bl.group(1) if bl else None})
    # 판정 인용 (보조 증거) — repo 전체에서
    cited = {}
    for f in list((REPO / "kb").rglob("*.md")) + list((REPO / "db").rglob("*.json")):
        try:
            t = f.read_text(errors="ignore")
        except OSError:
            continue
        for m in REV_VERDICT.finditer(t):
            cited[m.group(1)] = cited.get(m.group(1), 0) + 1

    _lab_n = {}
    for _r in prompts.values():
        _lab_n[_r["label"]] = _lab_n.get(_r["label"], 0) + 1
    for name, rec in prompts.items():
        rec["reply"], rec["answered_by"], rec["evidence"] = None, None, []
        for r in replies:
            if r["backlink"] and r["backlink"].endswith(name):
                rec["reply"], rec["answered_by"] = r["name"], r["label"]
                rec["evidence"].append("회신 본문의 `요청:` 역링크")
                break
        if not rec["reply"]:
            # 주제 slug 일치 (역링크 없는 판). ⚠ 완전일치만 보면 실물을 놓친다 —
            #   `X_bundle_reply` ↔ `X_prompt_prospective_bundle_ready`,
            #   `T_reply_polaron_pilot` ↔ `T_prompt_polaron_pilot_seeds`.
            #   그래서 **같은 라벨 안에서** 토큰 겹침으로 맺는다. 라벨을 고정하는
            #   것이 안전장치다 (라벨이 다르면 겹쳐도 맺지 않는다).
            _pt = set(rec["slug"].split("_"))
            for r in replies:
                if r["label"] != rec["label"] or not r["slug"]:
                    continue
                _rt = set(r["slug"].split("_"))
                if _rt <= _pt or _pt <= _rt or len(_rt & _pt) >= 2:
                    rec["reply"], rec["answered_by"] = r["name"], r["label"]
                    rec["evidence"].append("같은 라벨 · 주제 토큰 일치 %s"
                                           % sorted(_rt & _pt))
                    break
        if not rec["reply"]:
            # ⚠ 라벨이 **어긋난** 짝: `AR_reply_c12_v15` ← `AQ_prompt_c12_v15`.
            #   역링크도 같은 라벨도 없으므로 주제가 **정확히 같을 때만** 맺는다
            #   (토큰 겹침으로 느슨하게 맺으면 캠페인이 섞인다).
            for r in replies:
                if r["slug"] and r["slug"] == rec["slug"]:
                    rec["reply"], rec["answered_by"] = r["name"], r["label"]
                    rec["evidence"].append(
                        "⚠ 라벨 어긋남(%s→%s) · 주제 slug 완전일치"
                        % (rec["label"], r["label"]))
                    break
        # ⚠ 라벨이 **재사용**되면(S·T·U 가 각 2개) 인용 횟수는 두 캠페인이 합산된다.
        #   2026-08-31 실물: U(polaron S0)는 미발송인데 U(neutral_close)의 인용 11회를
        #   물려받아 '회신 수령' 으로 오판됐다. ⇒ 재사용 라벨은 인용을 **증거로 쓰지 않는다**.
        n = cited.get(rec["label"], 0)
        rec["label_reused"] = _lab_n.get(rec["label"], 0) > 1
        if n and not rec["label_reused"]:
            rec["evidence"].append("판정 인용 %d회" % n)
        elif n:
            rec["evidence"].append("⚠ 인용 %d회 — 라벨 재사용이라 **증거 아님**" % n)
        rec["cited"] = 0 if rec["label_reused"] else n

    contra = []
    for name, rec in sorted(prompts.items()):
        if not REV_WAITING.search(str(rec["status"])):
            continue
        if rec["reply"]:
            contra.append((name, rec["status"],
                           "회신 파일이 있다: %s" % rec["reply"]))
        elif rec["cited"] >= 5:
            contra.append((name, rec["status"],
                           "판정이 %d회 인용됐다 — 회신을 받은 것으로 보인다 "
                           "(원문 파일 없음)" % rec["cited"]))
    return prompts, contra


def cmd_reviews(write=False):
    """리뷰 사슬을 산출물에서 재구성해 보여 준다 (`--write` 면 INDEX 갱신)."""
    prompts, contra = review_chain()
    print("프롬프트 %d건" % len(prompts))
    if contra:
        print("\n🔴 status 와 증거가 **모순**되는 것 %d건:" % len(contra))
        for n, st, why in contra:
            print("   %-56s [%s]\n        → %s" % (n, st, why))
    else:
        print("모순 0건")
    if write:
        L = ["---",
             'title: "리뷰 사슬 색인 — 프롬프트↔회신 (자동 생성)"',
             "date: %s" % datetime.date.today().isoformat(),
             "updated: %s" % datetime.date.today().isoformat(),
             "tags: [index, review, codex]", "status: 자동생성", "kind: index",
             "confidence: high", "verificationStatus: verified",
             "verifiedAt: %s" % datetime.date.today().isoformat(),
             "verifiedBy: tools/kb_wiki.py reviews --write (산출물에서 재구성)",
             "explored: false", "authoredBy: agent", "effort: low",
             "claimType: empirical", "evidenceScope: multi-source-primary",
             "---", "",
             "# 리뷰 사슬 색인", "",
             "> ⛔ **손으로 고치지 않는다.** `python3 tools/kb_wiki.py reviews --write` 로",
             "> 재생성한다. 정본은 `kb/reviews/` 의 실물 파일이다.", "",
             "회신 파일명의 라벨이 프롬프트와 **어긋나는 판이 섞여 있다**",
             "(`AT_reply`←`AT_prompt` 이지만 `AV_reply`←`AU_prompt`).",
             "그래서 짝은 파일명이 아니라 회신 본문의 `요청:` 역링크로 맺는다.", "",
             "| 라벨 | 날짜 | 프롬프트 | 회신 | status | 근거 |",
             "|---|---|---|---|---|---|"]
        for name, r in sorted(prompts.items(), key=lambda kv: (kv[1]["date"], kv[0])):
            L.append("| %s | %s | `%s` | %s | %s | %s |"
                     % (r["label"], r["date"], name,
                        ("`%s`" % r["reply"]) if r["reply"] else "—",
                        r["status"], "; ".join(r["evidence"]) or "—"))
        if contra:
            L += ["", "## 🔴 모순 (status 는 대기인데 증거는 회신 수령)", ""]
            L += ["- `%s` [%s] — %s" % c for c in contra]
        (REPO / "kb" / "reviews" / "INDEX.md").write_text("\n".join(L) + "\n",
                                                          encoding="utf-8")
        print("\n→ kb/reviews/INDEX.md")
    return 1 if contra else 0


def selftest_reviews():
    """⛔음성 포함 — 모순 탐지가 실제로 도는가."""
    ok = [True]

    def chk(c, m):
        print(("  ✔ " if c else "  ⛔ ") + m)
        if not c:
            ok[0] = False

    prompts, contra = review_chain()
    chk(len(prompts) > 10, "리뷰 사슬을 실물에서 읽는다 (%d 프롬프트)" % len(prompts))
    # 양성: 역링크가 있는 짝을 실제로 맺는가
    _bl = [n for n, r in prompts.items()
           if r["reply"] and "역링크" in " ".join(r["evidence"])]
    chk(bool(_bl), "회신 본문의 `요청:` 역링크로 짝을 맺는다 (%s)" % (_bl[:1] or "없음"))
    # ⛔음성: 대기 상태 + 회신 파일 → 모순으로 **잡혀야** 한다
    _fake = {"x.md": {"label": "ZZ", "slug": "s", "date": "2026-01-01",
                      "status": "발송 대기", "reply": "r.md", "cited": 0,
                      "evidence": [], "path": None}}
    _c = [(n, r["status"], "x") for n, r in _fake.items()
          if REV_WAITING.search(str(r["status"])) and r["reply"]]
    chk(len(_c) == 1, "[음성] 대기 상태인데 회신 파일이 있으면 모순으로 잡는다")
    chk(not REV_WAITING.search("회신 수령 — 후속 AB"),
        "[음성] '회신 수령' 은 대기로 세지 않는다")
    chk(bool(REV_WAITING.search("발송전")) and bool(REV_WAITING.search("발송 대기")),
        "'발송전'·'발송 대기' 두 표기를 다 잡는다 (실물에 둘 다 있다)")
    # ⛔음성: 파일명으로 짝을 추측하면 틀리는 실물 사례 (AV_reply ← AU_prompt)
    _au = [r for n, r in prompts.items() if n.startswith("codex_AU_prompt")]
    if _au:
        chk(_au[0]["reply"] and _au[0]["reply"].startswith("codex_AV_reply"),
            "[음성] 라벨이 어긋난 짝(AU 프롬프트 ← AV 회신)을 역링크로 맺는다")
    _aq = [r for n, r in prompts.items() if n.startswith("codex_AQ_prompt")]
    if _aq:
        chk(_aq[0]["reply"] and _aq[0]["reply"].startswith("codex_AR_reply"),
            "[음성] 역링크도 같은 라벨도 없는 짝(AQ←AR)을 주제 완전일치로 맺는다")
    # ⛔음성: 주제가 다르면 라벨이 어긋나도 **맺지 않는다** (캠페인 섞임 방지)
    chk(not any(r["reply"] and "sdcp_binding" in n and "polaron" in str(r["reply"])
                for n, r in prompts.items()),
        "[음성] 라벨 재사용(T 둘)에서 다른 캠페인의 회신을 잘못 맺지 않는다")
    # ⛔음성: 생성한 INDEX 가 **자기 lint 를 통과**해야 한다 (2026-08-31: claimType
    #   descriptive 로 내보내 ERROR 1건을 스스로 만들었다)
    _ix = REPO / "kb" / "reviews" / "INDEX.md"
    if _ix.is_file():
        _fm, _ = parse_fm(_ix.read_text(errors="ignore"))
        _bad = [k for k, allowed in ENUMS.items()
                if (_fm or {}).get(k) and _fm[k] not in allowed]
        chk(not _bad, "생성한 INDEX 가 자기 lint enum 을 통과한다 (위반 %s)" % _bad)
    _reused = sorted({r["label"] for r in prompts.values() if r.get("label_reused")})
    chk(bool(_reused), "재사용된 라벨을 표시한다 (%s)" % _reused)
    _us0 = [r for n, r in prompts.items() if n.startswith("codex_U_prompt_polaron")]
    if _us0:
        chk(not _us0[0]["reply"] and _us0[0]["cited"] == 0,
            "⛔음성: 재사용 라벨(U)의 인용을 **증거로 쓰지 않는다** — 2026-08-31 에 "
            "미발송 U(polaron S0)가 다른 U 의 인용으로 '회신 수령' 오판됐다")
    print("reviews selftest %s" % ("PASS" if ok[0] else "FAIL"))
    return 0 if ok[0] else 1


def main():
    if "--selftest" in sys.argv:
        return selftest_env() or selftest_reviews()
    if len(sys.argv) < 2 or sys.argv[1] not in ("lint", "index", "new", "env",
                                                "reviews"):
        print(__doc__)
        return 1
    if sys.argv[1] == "lint":
        return cmd_lint()
    if sys.argv[1] == "index":
        return cmd_index()
    if sys.argv[1] == "reviews":
        return cmd_reviews("--write" in sys.argv)
    if sys.argv[1] == "env":
        return cmd_env("--script" in sys.argv)
    if len(sys.argv) != 4:
        sys.exit("쓰기: python3 tools/kb_wiki.py new <dir> <slug>")
    return cmd_new(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    sys.exit(main())
