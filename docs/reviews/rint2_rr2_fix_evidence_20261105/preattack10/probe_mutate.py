#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 10 회차 (독립) 변이 — 리포 밖 git 없는 사본 트리에서 한 번에 하나 · 정확한 글 바꿈 (한 번만 나와야) · 시험 `--only` 몇 개 · 매번 원 바이트로
되돌리고 sha256 확인.  N* = 가드 끄기 · 옛 꼴 (새 시험이 옳은 까닭으로 FAIL 하는지) · P* = 이 보고의 PB-01 권고 고침을 넣었을 때 기존 시험 반응 (어느 시험이
지금 허용을 기대값으로 박아 두었는지).

쓰는 법: python3 -I probe_mutate.py <사본 트리> <출력 json> [이름 쉼표]
"""
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

MT, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
SEL = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
RRF, TST = 'scripts/rint_r_chain.py', 'scripts/test_rint_r_chain.py'
M = [
    ('BASE', [], 'RC05,CE01,LG01,SU01,SU02', []),
    ('N1_float_is_none', [(RRF, "    if rc is None:\n        return 'none'\n    if type(rc) is int:",
                           "    if rc is None or isinstance(rc, float):\n        return 'none'\n    if type(rc) is int:")], 'RC05,RC02', ['RC05']),
    ('N2_drop_O_NONBLOCK', [(RRF, "os.O_RDONLY | os.O_NONBLOCK | getattr(os, 'O_NOCTTY', 0)", "os.O_RDONLY | getattr(os, 'O_NOCTTY', 0)")], 'LG03', ['LG03']),
    ('N3_timelimit_accepts_no_run', [(RRF, "    if state != 'missing' or (sr.get('code') or s.get('status')) != 'TIME_LIMIT':",
                                      "    if state not in ('missing', 'no_run') or (sr.get('code') or s.get('status')) != 'TIME_LIMIT':")], 'LG01', ['LG01']),
    ('N4_no_status_check', [(RRF, "        if st == 'unreadable' or (st == 'ok' and not isinstance(v.get('status'), str)):", "        if st == 'unreadable':")],
     'SU01', ['SU01']),
    ('N5_summary_not_atomic', [(RRF, "    write_json_atomic(path, _clean(s))", "    write_json(path, s)")], 'SU02', ['SU02']),
    ('N6_recover_accepts_empty_cause', [(RRF, "            if 'chain_end' in er and not (isinstance(ce, dict) and chain_cause_known(ce.get('cause'))):",
                                         "            if 'chain_end' in er and not (isinstance(ce, dict) and (chain_cause_known(ce.get('cause')) or ce.get('cause') == '')):")],
     'CE01', ['CE01']),
    ('P1_chain_end_rc_none_is_failure', [(RRF, "    return isinstance(ce, dict) and ce.get('cause') is None and runner_rc_failed(ce.get('rc'))",
                                          "    return isinstance(ce, dict) and ce.get('cause') is None and not rc_success(ce.get('rc'))")], 'CE,RC,PE03u', []),
    ('P2_gu_rc_unknown_is_failure', [(RRF, "        if runner_rc_failed((rr or {}).get('rc')):",
                                      "        if rr is None or (rr.get('group_cause') is None and not rc_success(rr.get('rc'))) or runner_rc_failed(rr.get('rc')):")],
     'LG01', []),
]


def sha(f):
    return hashlib.sha256((MT / f).read_bytes()).hexdigest()


start = {f: sha(f) for f in (RRF, TST)}
res = {'tree': str(MT), 'start_sha256': start, 'runs': {}}
for name, edits, only, want in M:
    if SEL and name not in SEL:
        continue
    orig = {}
    try:
        for f, old, new in edits:
            t = orig.setdefault(f, (MT / f).read_bytes()).decode('utf-8')
            n = t.count(old)
            if n != 1:
                raise SystemExit(f'{name}: 바꿀 글이 {n} 번 나온다 ({f})')
            (MT / f).write_bytes(t.replace(old, new).encode('utf-8'))
        t0 = time.time()
        p = subprocess.run([sys.executable, '-I', '-B', TST, '--only', only], cwd=str(MT), capture_output=True, text=True, timeout=3000)
        fails = re.findall(r'^\s+FAIL\s+(\S+)', p.stdout, re.M)
        summ = [x for x in p.stdout.splitlines() if x.startswith('test_rint_r_chain:')]
        detail = {c: [x.strip()[:900] for x in p.stdout.splitlines() if re.match(rf'^\s+FAIL\s+{re.escape(c)}\b', x)] for c in fails}
        caught = all(c in fails for c in want) if want else None
        res['runs'][name] = {'only': only, 'rc': p.returncode, 'fails': fails, 'summary': summ, 'want_fail': want, 'caught': caught,
                             'seconds': round(time.time() - t0, 1), 'fail_detail': detail, 'stderr_tail': p.stderr[-400:]}
        print(name, 'rc', p.returncode, 'FAIL', fails, summ, 'caught' if caught else ('' if caught is None else 'NOT caught'), flush=True)
    finally:
        for f, b in orig.items():
            (MT / f).write_bytes(b)
end = {f: sha(f) for f in (RRF, TST)}
res['end_sha256'], res['restored'] = end, end == start
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('restored', res['restored'])
