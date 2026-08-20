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

The kit's study-path coverage check was dropped on 2026-08-20: it only ran when
`guides/llm-wiki-study-path.md` existed, and this is a project wiki, not a
learning wiki, so that file never existed and the check never ran. A check that
silently does nothing is worse than no check — it reads as coverage.

Usage: python3 tools/lint.py
Exit code 0 = no errors (warnings allowed), 1 = errors found.
"""
import re, glob, hashlib, pathlib, sys, datetime

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
            warnings.append(f'{stem}: verification stale (verifiedAt {va}) — /verify 재실행 권장')
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
