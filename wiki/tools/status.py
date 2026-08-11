#!/usr/bin/env python3
"""LLM Wiki status — counts, verification coverage, study progress.

Usage: python3 tools/status.py
"""
import re, glob, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
DIRS = ['concepts', 'entities', 'comparisons', 'queries', 'guides',
        'questions', 'syntheses']

def parse_fm(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            km = re.match(r'^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$', line)
            if km:
                fm[km.group(1)] = km.group(2).strip()
    return fm

pages = {}
for d in DIRS:
    for f in sorted(glob.glob(str(BASE / d / '*.md'))):
        p = pathlib.Path(f)
        pages[p.stem] = (d, parse_fm(p.read_text()))

raws = glob.glob(str(BASE / 'raw/**/*.md'), recursive=True)

print('=== LLM WIKI STATUS ===\n')

# counts by type
by_dir = {}
for stem, (d, fm) in pages.items():
    by_dir[d] = by_dir.get(d, 0) + 1
print(f'wiki pages: {len(pages)}  (' +
      ' · '.join(f'{d} {by_dir.get(d, 0)}' for d in DIRS) + ')')
print(f'raw sources: {len(raws)}')

# quality coverage
def dist(key):
    out = {}
    for _, (_, fm) in pages.items():
        v = fm.get(key, '?')
        out[v] = out.get(v, 0) + 1
    return ' · '.join(f'{k} {v}' for k, v in sorted(out.items()))

print(f'\nconfidence:         {dist("confidence")}')
print(f'verificationStatus: {dist("verificationStatus")}')
print(f'explored:           {dist("explored")}')

# study path progress — parse checklist lines "- Stage N: [ ] a · [ ] b"
sp_path = BASE / 'guides/llm-wiki-study-path.md'
if sp_path.exists():
    print('\n학습 진도 (explored: true 기준):')
    for line in sp_path.read_text().splitlines():
        m = re.match(r'^- (Stage \d+): (.+)$', line)
        if not m:
            continue
        stage = m.group(1)
        stems = [s for s in re.findall(r'\[ \] ([\w-]+)', m.group(2)) if s in pages]
        done = sum(1 for s in stems if pages[s][1].get('explored') == 'true')
        bar = '█' * done + '░' * (len(stems) - done)
        print(f'  {stage}: {bar} {done}/{len(stems)}')

# verify queue
unverified = sorted(s for s, (_, fm) in pages.items()
                    if fm.get('verificationStatus') == 'unverified')
if unverified:
    print(f'\nverify 대기 (unverified {len(unverified)}):')
    print('  ' + ' · '.join(unverified))

# recent log entries (Karpathy's parseable-log tip)
log = (BASE / 'log.md').read_text()
entries = re.findall(r'^## \[.*$', log, re.M)
print(f'\n최근 log ({len(entries)} entries, last 5):')
for e in entries[-5:]:
    print('  ' + e.lstrip('# '))
