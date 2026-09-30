#!/usr/bin/env python3
"""LLM Wiki lint — mechanical health check.

Checks (SCHEMA.md conventions):
  1. every wiki page has required frontmatter keys, and type matches its folder
  2. verified pages carry verifiedAt/verifiedBy
  3. sources paths exist
  4. all wikilinks resolve to real pages (code spans/blocks excluded)
  5. each page has >= 2 distinct wikilinks (warning)
  6. index.md lists every page, lists nothing that doesn't exist, and its
     "Total pages" count is accurate
  7. raw file sha256 matches body (immutability check)
  8. orphan pages — zero inbound wikilinks from other pages (warning)
  9. stale pages — `updated` older than STALE_DAYS (warning)
 10. confidence:high pages without a Bias Check / 불확실성 section (note)
 11. enum keys carry allowed values (claimType, evidenceScope, effort,
     research-question status) — checked only when present
 12. description frontmatter, if present, is quoted (v1.8 rule)
 13. evidenceScope single-source with confidence high (warning — 근거 폭이 상한)
 14. verified pages with verifiedAt older than STALE_DAYS (warning — re-verify)
 15. no wiki page hardcodes a git branch name — the branch rule lives in the
     root CLAUDE.md only (2026-08-20: 5 wiki files had drifted to a dead branch)
 16. no model identifier in wiki pages or tools (root CLAUDE.md hard rule 6)
 17. Parity Contract — CLAUDE.md and AGENTS.md carry the same Essential Rules
 18. canonical-copy — research constants (cathode ratio, target capacity) copied
     into webapp templates/index must match the reference-cell entity page
 19. no two raw files share the same body sha256 (2026-09-30: a parallel paper-agent
     run sealed one digest with another paper's body; each file's own hash matched)
 20. a digest's frontmatter `doi` must also appear in its body (same failure, caught
     from a single file)

The kit's study-path coverage check was dropped on 2026-08-20: it only ran when
`guides/llm-wiki-study-path.md` existed, and this is a project wiki, not a
learning wiki, so that file never existed and the check never ran. A check that
silently does nothing is worse than no check — it reads as coverage.

Usage: python3 tools/lint.py
Exit code 0 = no errors (warnings allowed), 1 = errors found.
"""
import re, glob, hashlib, pathlib, sys, datetime

# 출력 경로도 UTF-8 로 닫는다. 파일 읽기에 encoding='utf-8' 을 넣은 것만으로는
# 부족했다 — 21차 리뷰 발견 10: Windows 기본 콘솔(CP949)에서 em dash 를 찍는
# 순간 UnicodeEncodeError 로 죽는다. 리뷰어는 status.py 에서 실측했고 이쪽도
# 같은 구조라 함께 닫는다. errors='replace' 는 마지막 안전망 —
# 콘솔 코드페이지가 UTF-8 을 못 받아도 검사 결과 자체는 나와야 한다.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):      # 파이프 래핑 등 — 무시하고 진행
        pass

STALE_DAYS = 90

BASE = pathlib.Path(__file__).resolve().parent.parent
DIRS = ['concepts', 'entities', 'comparisons', 'queries', 'guides',
        'questions', 'syntheses']
REQ = ['title', 'created', 'updated', 'type', 'tags', 'sources',
       'confidence', 'explored', 'verificationStatus']
TYPE_BY_DIR = {'concepts': 'concept', 'entities': 'entity',
               'comparisons': 'comparison', 'queries': 'query', 'guides': 'guide',
               'questions': 'research-question', 'syntheses': 'synthesis'}
ENUMS = {
    'confidence': {'high', 'medium', 'low'},
    'verificationStatus': {'unverified', 'verified', 'disputed'},
    'claimType': {'definition', 'empirical', 'theoretical', 'historical',
                  'prescriptive', 'interpretive', 'mixed'},
    'evidenceScope': {'single-source', 'multi-source-primary', 'multi-source-mixed',
                      'synthesis-only', 'user-original'},
    'effort': {'low', 'medium', 'high', 'max'},
}
RQ_STATUS = {'open', 'active', 'answered', 'abandoned'}

errors, warnings = [], []

def parse_fm(s):
    fm = {}
    for line in s.splitlines():
        m = re.match(r'^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm

def strip_code(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)   # fenced blocks
    text = re.sub(r'`[^`\n]*`', '', text)               # inline code
    return text

pages = {}
for d in DIRS:
    for f in glob.glob(str(BASE / d / '*.md')):
        p = pathlib.Path(f)
        pages[p.stem] = p

fm_by_page = {}
outbound = {}
for stem, p in sorted(pages.items()):
    text = p.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        errors.append(f'{p.name}: no frontmatter')
        continue
    fm = parse_fm(m.group(1))
    fm_by_page[stem] = fm
    for k in REQ:
        if k not in fm:
            errors.append(f'{p.name}: missing frontmatter key `{k}`')
    want = TYPE_BY_DIR[p.parent.name]
    if fm.get('type') != want:
        errors.append(f'{p.name}: type `{fm.get("type")}` in {p.parent.name}/ (want {want})')
    if fm.get('verificationStatus') == 'verified' and ('verifiedAt' not in fm or 'verifiedBy' not in fm):
        errors.append(f'{p.name}: verified but missing verifiedAt/verifiedBy')
    # 12. enum values (only when key present and non-empty)
    for k, allowed in ENUMS.items():
        v = fm.get(k, '')
        if v and v not in allowed:
            errors.append(f'{p.name}: `{k}: {v}` not in {sorted(allowed)}')
    if fm.get('type') == 'research-question':
        st = fm.get('status', '')
        if st and st not in RQ_STATUS:
            errors.append(f'{p.name}: `status: {st}` not in {sorted(RQ_STATUS)}')
    # 13. description must be quoted (v1.8 — YAML 파싱 보호)
    desc = fm.get('description', '')
    if desc and not (desc.startswith('"') and desc.endswith('"')):
        errors.append(f'{p.name}: description not quoted')
    # 14. evidence scope caps confidence
    if fm.get('evidenceScope') == 'single-source' and fm.get('confidence') == 'high':
        warnings.append(f'{p.name}: single-source but confidence high — 근거 폭이 상한 (SCHEMA Provenance)')
    src_field = fm.get('sources', '')
    srcs = re.findall(r'[\w/.-]+\.md', src_field)
    urls = re.findall(r'https?://\S+', src_field)
    if not srcs and not urls:
        errors.append(f'{p.name}: no sources parsed')
    for s in srcs:
        if not (BASE / s).exists():
            errors.append(f'{p.name}: source path missing: {s}')
    body = strip_code(text[m.end():])
    links = re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]', body)
    for l in links:
        if l.strip() not in pages:
            errors.append(f'{p.name}: broken wikilink [[{l}]]')
    if len(set(links)) < 2:
        warnings.append(f'{p.name}: fewer than 2 distinct wikilinks')
    outbound.setdefault(stem, set()).update(
        l.strip() for l in links if l.strip() in pages and l.strip() != stem)

index = (BASE / 'index.md').read_text(encoding='utf-8')
idx_links = set(re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]', index))
for stem in pages:
    if stem not in idx_links:
        errors.append(f'index.md: page not listed: {stem}')
for l in idx_links:
    if l not in pages:
        errors.append(f'index.md: listed but file missing: {l}')
mc = re.search(r'Total pages: (\d+)', index)
if mc and int(mc.group(1)) != len(pages):
    errors.append(f'index.md: claims {mc.group(1)} pages, actual {len(pages)}')

raws = glob.glob(str(BASE / 'raw/**/*.md'), recursive=True)
raw_bodies, raw_fm = {}, {}
for f in raws:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.S)
    if not m:
        errors.append(f'{f}: no raw frontmatter')
        continue
    fm = parse_fm(m.group(1))
    h = hashlib.sha256(m.group(2).lstrip('\n').encode()).hexdigest()
    if fm.get('sha256') != h:
        errors.append(f'{pathlib.Path(f).name}: sha256 mismatch '
                      f'(declared {str(fm.get("sha256"))[:12]}…, actual {h[:12]}…)')
    raw_bodies.setdefault(h, []).append(pathlib.Path(f).name)
    raw_fm[pathlib.Path(f).name] = (fm, m.group(2))

# 19. 같은 본문이 두 raw 파일에 들어 있으면 하나는 내용이 잘못 들어간 것이다.
#     2026-09-30 사고: 논문 에이전트 5개를 병렬로 돌렸는데 `yu2024_…` 가 **Yu frontmatter +
#     Wang 본문**으로 봉인됐다. 두 파일 각자는 sha256 이 declared 와 일치해서 검사 7을
#     통과했다 — 봉인은 "본문이 바뀌지 않았음" 만 보증하고 "올바른 본문인지" 는 안 본다.
#     이 검사가 그 구멍을 막는다. 본문 해시가 겹치는 순간 죽는다.
for h, names in sorted(raw_bodies.items()):
    if len(names) > 1:
        errors.append(f'raw 본문 중복: {" · ".join(sorted(names))} 의 본문이 동일하다 '
                      f'(sha256 {h[:12]}…) — 하나는 다른 논문의 내용이 들어갔다')

# 20. digest 의 frontmatter `doi` 가 본문에도 인용되어야 한다. frontmatter 만 갈아 끼우고
#     본문이 다른 논문인 사고(위 19번)를 **한 파일만 봐도** 잡는 검사다. 2026-09-30 실측:
#     이 위키의 digest 7편 모두 서지 절에 자기 DOI 를 적는다 — 관례를 검사로 굳힌다.
#     `doi` 키가 없는 raw(전사·기사 등)는 면제.
for name, (fm, body) in sorted(raw_fm.items()):
    doi = (fm.get('doi') or '').strip().rstrip('.')
    if doi and doi not in body:
        errors.append(f'{name}: frontmatter 의 doi `{doi}` 가 본문에 없다 — '
                      f'frontmatter 와 본문이 다른 논문일 수 있다 (2026-09-30 사고 참조)')

# 15. branch names are not wiki content — the rule lives in the root CLAUDE.md.
#     Hardcoding it here drifts silently: on 2026-08-20 five wiki files (and
#     three more outside the wiki) still named a branch that had been fully
#     absorbed 88 commits earlier. `raw/` is exempt
#     (immutable snapshots legitimately record the branch they were taken on).
#     `.claude/` and `.github/` paths are not branch names — the lookbehind
#     drops them.
#     20차 리뷰 발견 12: lookbehind 에 `/` 가 있어 `origin/claude/…` 와
#     `github.com/…/tree/claude/…` 를 놓쳤다. `.` 만 배제하면 `.claude/`
#     경로는 계속 면제되면서 remote-qualified·URL 형태를 잡는다.
#     한계: `Codex/` 는 넣지 않는다 — 위키가 도구 이름으로 `Codex/Cursor`
#     를 쓰므로 오탐이 난다. 이 검사는 `claude/` 계열만 본다.
BRANCH_RE = re.compile(r'(?<![.\w])claude/[A-Za-z0-9][A-Za-z0-9-]*')
for f in [BASE / n for n in ('SCHEMA.md', 'CLAUDE.md', 'AGENTS.md', 'README.md',
                             'index.md')] + sorted(pages.values()):
    if not f.exists():
        continue
    for hit in sorted(set(BRANCH_RE.findall(f.read_text(encoding='utf-8')))):
        errors.append(f'{f.name}: hardcoded branch name `{hit}` — '
                      f'루트 CLAUDE.md 의 브랜치 하드룰을 참조하라 (drift 방지)')

# 16. no-model-identifier — 루트 CLAUDE.md 하드룰 6. 모델 식별자는 위키 페이지·도구에
#     적지 않는다. 2026-09-11 전수조사 발견: `tools/new-page.py --model` 이 하드룰이
#     금지한 바로 그 자리(페이지 frontmatter)에 길을 내주고 있었다 — 플래그를 뺐고
#     이 검사로 재발을 막는다.
#     `raw/` 는 면제 (불변 스냅샷이 당시 기록을 legitimately 담는다).
#     예외 하나: API 클라이언트가 호출에 쓰는 모델 문자열은 `webapp/chat.py` 의 env
#     기본값 **한 곳**에만 둔다 (하드룰 6 에 명시). 이 검사는 위키만 보므로 닿지 않는다.
MODEL_RE = re.compile(
    r'(?<![\w-])(?:claude-(?:opus|sonnet|haiku|fable|instant)[\w.-]*'
    r'|gpt-[0-9][\w.-]*|gemini-[0-9][\w.-]*)', re.I)
for f in [BASE / n for n in ('SCHEMA.md', 'CLAUDE.md', 'AGENTS.md', 'README.md',
                             'index.md')] + sorted(pages.values()) + [BASE / 'tools' / 'new-page.py']:
    if not f.exists():
        continue
    for hit in sorted(set(MODEL_RE.findall(f.read_text(encoding='utf-8')))):
        errors.append(f'{f.name}: model identifier `{hit}` — '
                      f'루트 CLAUDE.md 하드룰 6 (위키 페이지·코드에 적지 않는다)')

# 17. Parity Contract — CLAUDE.md 와 AGENTS.md 의 "## Essential Rules" 절은 같은 규칙의
#     미러다. 두 파일 모두 "lint 로 parity 를 확인한다" 고 적어 놓았지만 2026-09-11
#     전수조사 시점까지 그런 검사가 없었다 — 문서가 있지도 않은 게이트를 주장하고 있었다.
#     이제 실제로 센다.
def _essential(path):
    if not path.exists():
        return None
    txt = path.read_text(encoding='utf-8')
    m = re.search(r'^## Essential Rules.*?\n(.*?)(?=^## )', txt, re.S | re.M)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else None

_c, _a = _essential(BASE / 'CLAUDE.md'), _essential(BASE / 'AGENTS.md')
if _c is None or _a is None:
    errors.append('parity: CLAUDE.md/AGENTS.md 의 `## Essential Rules` 절을 찾지 못했다')
elif _c != _a:
    errors.append('parity: CLAUDE.md 와 AGENTS.md 의 Essential Rules 가 다르다 — '
                  'Parity Contract 위반 (두 파일을 함께 고친다)')

# 18. canonical-copy — 연구 상수(복합양극 조성·목표 용량)의 정본은 reference cell
#     entity 페이지 하나다. 그 값이 webapp 템플릿·index 로 복사되어 있고 2026-09-11
#     전수조사 시점에 이를 묶어주는 것이 아무것도 없었다 — 브랜치 이름 drift(검사 15)와
#     정확히 같은 구조다. 사본이 정본과 어긋나면 여기서 죽는다.
#     `raw/` 는 면제 (논문 수치·세션 원문이 다른 값을 legitimately 담는다).
CANON_PAGE = BASE / 'entities' / 'li2s-assb-reference-cell.md'
COMP_RE = re.compile(r'(?<![\d.:])(\d{1,3})\s*:\s*(\d{1,3})\s*:\s*(\d{1,3})(?![\d.:])')
#     용량 범위는 **기준(basis)까지 함께** 읽는다. 2026-09-30: 기준을 안 보는 첫 판이
#     `143–159 mAh g⁻¹(composite)` 를 "목표가 바뀌었다" 로 오탐했다 — 그건 목표의 drift 가 아니라
#     복합양극 기준 환산값이다. 하드룰 5 가 기준 표기를 의무화하므로, `(S)`·`(composite)` 처럼
#     **다른 정규화가 명시된** 값은 환산으로 보고 면제한다. 기준이 없거나 목표와 같은 기준
#     (`(Li2S)`·`(기준 미확인)`)인 값만 정본과 대조한다 — 그게 사본 drift 가 생기는 자리다.
CAP_RE = re.compile(r'(\d{3,4})\s*[\u2013-]\s*(\d{3,4})\s*mAh(?:\s*g⁻¹)?\s*(\([^)]{1,12}\))?')
DERIVED_BASIS = ('(S)', '(composite)')

def _consts(txt):
    caps = set()
    for a, b, basis in CAP_RE.findall(txt):
        if (basis or '').strip() in DERIVED_BASIS:
            continue                      # 환산값 — 정본과 다른 분모다
        caps.add(f'{a}-{b}')
    return ({':'.join(m) for m in COMP_RE.findall(txt)}, caps)

if not CANON_PAGE.exists():
    errors.append(f'canonical-copy: 정본 페이지가 없다: {CANON_PAGE.name}')
else:
    canon_comp, canon_cap = _consts(CANON_PAGE.read_text(encoding='utf-8'))
    copies = [BASE / 'index.md', BASE / 'README.md', BASE / 'SCHEMA.md']
    copies += sorted(pages.values())
    copies += sorted((BASE.parent / 'webapp').rglob('*.html'))
    copies += [BASE.parent / 'webapp' / 'app.py', BASE.parent / 'webapp' / 'README.md',
               BASE.parent / 'README.md']
    for f in copies:
        if not f.exists() or f == CANON_PAGE:
            continue
        comp, cap = _consts(f.read_text(encoding='utf-8'))
        for hit in sorted(comp - canon_comp):
            errors.append(f'{f.name}: 복합양극 조성 `{hit}` 가 정본과 다르다 — '
                          f'정본 {sorted(canon_comp)} ({CANON_PAGE.name})')
        for hit in sorted(cap - canon_cap):
            errors.append(f'{f.name}: 목표 용량 `{hit} mAh` 가 정본과 다르다 — '
                          f'정본 {sorted(canon_cap)} ({CANON_PAGE.name})')

# 8. orphans — no inbound links from any other page
inbound = {s: 0 for s in pages}
for src, targets in outbound.items():
    for t in targets:
        inbound[t] += 1
for stem, n in sorted(inbound.items()):
    if n == 0:
        warnings.append(f'{stem}: orphan (no inbound wikilinks from other pages)')

# 9. stale — updated older than STALE_DAYS
today = datetime.date.today()
for stem, fm in fm_by_page.items():
    try:
        upd = datetime.date.fromisoformat(str(fm.get('updated', '')))
        if (today - upd).days > STALE_DAYS:
            warnings.append(f'{stem}: stale (updated {upd}, {(today - upd).days}d ago)')
    except ValueError:
        errors.append(f'{stem}: unparseable `updated` date: {fm.get("updated")}')

# 14. verified but verification itself is stale
for stem, fm in fm_by_page.items():
    if fm.get('verificationStatus') != 'verified':
        continue
    try:
        va = datetime.date.fromisoformat(str(fm.get('verifiedAt', '')))
        if (today - va).days > STALE_DAYS:
            warnings.append(f'{stem}: verification stale (verifiedAt {va}) — /wiki-verify 재실행 권장')
    except ValueError:
        pass  # missing/bad verifiedAt already an error above

# 10. bias-check coverage for confidence:high (note, not warning)
no_bias = [s for s, fm in fm_by_page.items()
           if fm.get('confidence') == 'high'
           and not re.search(r'불확실성|Bias Check|반대해석|한계', pages[s].read_text(encoding='utf-8'))]

print('=== LINT REPORT ===')
print(f'pages: {len(pages)} | raw files: {len(raws)}')
vs, ex = {}, {}
for fm in fm_by_page.values():
    vs[fm.get('verificationStatus')] = vs.get(fm.get('verificationStatus'), 0) + 1
    ex[fm.get('explored')] = ex.get(fm.get('explored'), 0) + 1
print('verificationStatus:', vs)
print('explored:', ex)
print(f'\nERRORS ({len(errors)}):')
for e in errors:
    print(' ✗', e)
print(f'\nWARNINGS ({len(warnings)}):')
for w in warnings:
    print(' ⚠', w)
if no_bias:
    print(f'\nNOTES: confidence:high without Bias Check/불확실성 section — {len(no_bias)} pages')
    print('  ' + ' · '.join(sorted(no_bias)))
if not errors:
    print('\nRESULT: 0 errors')
sys.exit(1 if errors else 0)
