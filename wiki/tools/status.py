#!/usr/bin/env python3
"""LLM Wiki status — counts, verification coverage, verify queue.

Usage: python3 tools/status.py
"""
import re, glob, pathlib, sys

# ★ 21차 리뷰 발견 10 — 파일 읽기를 UTF-8 로 고정한 것만으로는 13-3 이 안 닫혔다.
# 리뷰어의 Windows 기본 환경에서 이 스크립트는 **출력 중에** CP949
# UnicodeEncodeError 로 죽었다 (본문의 em dash). 입력이 아니라 stdout 이 문제였다.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

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
        pages[p.stem] = (d, parse_fm(p.read_text(encoding='utf-8')))

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

# (킷의 study-path 진도 바는 2026-08-20 제거 — `guides/llm-wiki-study-path.md`
#  가 있을 때만 그리는데 이 위키는 학습용이 아니라 프로젝트 위키라 그 파일이
#  존재한 적이 없다. lint 의 study-path 커버리지 검사도 같이 걷어냈다.)

# verify queue
unverified = sorted(s for s, (_, fm) in pages.items()
                    if fm.get('verificationStatus') == 'unverified')
if unverified:
    print(f'\nverify 대기 (unverified {len(unverified)}):')
    print('  ' + ' · '.join(unverified))

# recent log entries (Karpathy's parseable-log tip)
log = (BASE / 'log.md').read_text(encoding='utf-8')
entries = re.findall(r'^## \[.*$', log, re.M)
print(f'\n최근 log ({len(entries)} entries, last 5):')
for e in entries[-5:]:
    print('  ' + e.lstrip('# '))
