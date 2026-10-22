# -*- coding: utf-8 -*-
"""변이 실행기 (2 회차 · impl) — 변이 하나 = 파일 한 자리 (정확히 한 번 나오는 글) 를 바꾼다 → 시험 묶음 실행 → 원본 바이트로 되돌림
(sha256 대조).  리포에 남기지 않는다 (작업 트리 = 내 격리 사본 · 봉인 32 파일 아님 — 실행 전 확인).
사용: python3 -I mutate.py <변이 JSON> <결과 JSON>"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d'
SEALED = {'scripts/network_conductivity.py', 'scripts/se_material.py', 'scripts/tau_flux.py', 'webapp/app.py'}   # 대표 (전수 = 실행 전 목록 대조)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_one(m):
    path = os.path.join(WT, m['file'])
    assert m['file'] not in SEALED
    orig = open(path, 'rb').read()
    h0 = sha(orig)
    text = orig.decode('utf-8')
    n = text.count(m['old'])
    if n != 1:
        return {'id': m['id'], 'error': f'old 글이 {n} 번 (1 이어야)'}
    mutated = text.replace(m['old'], m['new'])
    open(path, 'wb').write(mutated.encode('utf-8'))
    t0 = time.time()
    try:
        r = subprocess.run(m['cmd'], cwd=WT, capture_output=True, text=True, timeout=m.get('timeout', 900),
                           env=dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1'))
        out = r.stdout + r.stderr
        rc = r.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = (e.stdout or '') if isinstance(e.stdout, str) else '', 'timeout'
    finally:
        open(path, 'wb').write(orig)
    assert sha(open(path, 'rb').read()) == h0, '되돌림 실패'
    fails = re.findall(r'^\s*FAIL\s+(\S+)', out, re.M)
    summ = [ln for ln in out.splitlines() if re.search(r'PASS', ln) and re.search(r'(\d+/\d+ PASS|\d+ PASS · \d+ FAIL)', ln)]
    caught = bool(fails) or (rc not in (0,))
    exp = m.get('expect')
    return {'id': m['id'], 'file': m['file'], 'what': m['what'], 'rc': rc, 'seconds': round(time.time() - t0, 1),
            'n_fail': len(fails), 'fails': fails[:20], 'summary': summ[-1:] if summ else out.splitlines()[-3:],
            'caught': caught, 'expect_any_of': exp,
            'caught_by_expected': (None if not exp else bool(set(exp) & set(fails)))}


def main():
    ms = json.load(open(sys.argv[1], encoding='utf-8'))
    only = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
    res = []
    for m in ms:
        if only and m['id'] not in only:
            continue
        r = run_one(m)
        res.append(r)
        print(json.dumps(r, ensure_ascii=False), flush=True)
    json.dump(res, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
