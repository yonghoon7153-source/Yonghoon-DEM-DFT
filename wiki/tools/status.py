#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wiki status — 스냅샷: 타입별 페이지 수 · 품질축 분포 · 열린 RQ · 최근 로그 · 다음 행동.

사용: python3 wiki/tools/status.py [--selftest]
"""
from __future__ import annotations

import glob
import pathlib
import re
import sys
from collections import Counter

BASE = pathlib.Path(__file__).resolve().parent.parent
DIRS = ['concepts', 'entities', 'comparisons', 'queries', 'guides', 'questions', 'syntheses']


def parse_fm(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        k = re.match(r'^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$', line)
        if k:
            fm[k.group(1)] = k.group(2).strip()
    return fm


def snapshot(base=BASE):
    by_type, conf, ver, exp, rq_open = Counter(), Counter(), Counter(), Counter(), []
    for d in DIRS:
        for f in sorted(glob.glob(str(base / d / '*.md'))):
            fm = parse_fm(pathlib.Path(f).read_text(encoding='utf-8'))
            by_type[d] += 1
            conf[fm.get('confidence', '?')] += 1
            ver[fm.get('verificationStatus', '?')] += 1
            exp[fm.get('explored', '?')] += 1
            if fm.get('type') == 'research-question' and fm.get('status') in ('open', 'active'):
                rq_open.append((pathlib.Path(f).stem, fm.get('status')))
    return {'by_type': by_type, 'conf': conf, 'ver': ver, 'exp': exp, 'rq_open': rq_open}


def recent_log(base=BASE, n=5):
    p = base / 'log.md'
    if not p.exists():
        return []
    return re.findall(r'^## \[.*$', p.read_text(encoding='utf-8'), re.M)[-n:]


def next_action(s):
    if s['ver'].get('unverified', 0) > 0:
        return f"unverified {s['ver']['unverified']}건 — 오래된 것부터 /wiki-verify"
    if s['rq_open']:
        return f"열린 RQ {len(s['rq_open'])}건 — 새 자료가 근거를 주는지 확인"
    if s['exp'].get('false', 0) > 0:
        return f"explored:false {s['exp']['false']}건 — 사람이 읽고 승격 (사람만)"
    return '새 자료 하나 ingest'


def _selftest():
    import shutil
    import tempfile
    ok = fail = 0

    def chk(msg, cond):
        nonlocal ok, fail
        print(('  PASS  ' if cond else '  FAIL  ') + msg)
        ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)

    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        (tmp / 'concepts').mkdir(parents=True)
        (tmp / 'questions').mkdir()
        (tmp / 'concepts' / 'a.md').write_text(
            '---\ntype: concept\nconfidence: medium\nverificationStatus: unverified\n'
            'explored: false\n---\nx', encoding='utf-8')
        (tmp / 'questions' / 'q.md').write_text(
            '---\ntype: research-question\nstatus: active\nconfidence: low\n'
            'verificationStatus: unverified\nexplored: false\n---\nx', encoding='utf-8')
        s = snapshot(tmp)
        chk('1) 타입별 카운트', s['by_type']['concepts'] == 1 and s['by_type']['questions'] == 1)
        chk('2) 열린 RQ 수집', s['rq_open'] == [('q', 'active')])
        chk('3) 다음 행동 = unverified 우선', 'unverified' in next_action(s))
        (tmp / 'log.md').write_text('# L\n\n## [2026-08-11] create | x\n', encoding='utf-8')
        chk('4) 최근 로그', recent_log(tmp) == ['## [2026-08-11] create | x'])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\nstatus selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main():
    if '--selftest' in sys.argv:
        return _selftest()
    s = snapshot()
    total = sum(s['by_type'].values())
    print(f'wiki 스냅샷 — 페이지 {total}')
    print('  타입별  : ' + ' · '.join(f'{d} {s["by_type"][d]}' for d in DIRS if s['by_type'][d]))
    print('  confidence: ' + ' · '.join(f'{k} {v}' for k, v in sorted(s['conf'].items())))
    print('  verification: ' + ' · '.join(f'{k} {v}' for k, v in sorted(s['ver'].items())))
    print('  explored : ' + ' · '.join(f'{k} {v}' for k, v in sorted(s['exp'].items())))
    if s['rq_open']:
        print('  열린 RQ : ' + ' · '.join(f'{n}({st})' for n, st in s['rq_open']))
    for line in recent_log():
        print('  log: ' + line)
    print(f'\n다음 행동 1가지: {next_action(s)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
