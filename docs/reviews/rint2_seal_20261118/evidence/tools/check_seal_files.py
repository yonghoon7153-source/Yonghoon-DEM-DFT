#!/usr/bin/env python3
"""봉인 꼴 커밋의 파일마다 경계 — 풀이 코드 목록 다섯 경로 (개발 탐침 원장 §3 54 줄) · 사슬 CODE_FILES 20 · S0 일곱 (`S0_SAME_FILES`) ·
규율 검사 입력 (`scripts/check_method_discipline.py`: scripts/** · docs/reviews/claims.json · docs/manuscript/methods_simulation_v7_draft.md ·
.github/workflows/discipline.yml) 밖인지 + `git diff --quiet <핀> <봉인 꼴> -- <다섯 경로>` (원장 §2 "같은 핀" 판정) — 읽기만.

argv: <봉인 꼴 사본 (git)> <핀 rev> <봉인 꼴 rev>
"""
import os
import subprocess
import sys

REPO, PIN, HEAD = sys.argv[1:4]
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import rint_r_chain as R  # noqa: E402

SOLVER = ('scripts/', 'docs/reviews/rint2_probe6_prep_20261110/tools/', 'docs/data/rint2_s0_sbe_20261108/', 'docs/data/rint_eis_anchors.csv',
          'docs/reviews/sdcp_gain_prereg_v2_20260816.md')
DISC = ('docs/reviews/claims.json', 'docs/manuscript/methods_simulation_v7_draft.md', '.github/workflows/discipline.yml')
CODE = {'scripts/' + n for n in R.CODE_FILES}
S0 = {'scripts/' + n for n in R.S0_SAME_FILES}


def git(*a):
    r = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, env=ENV)
    return r.returncode, r.stdout


def in_solver(p):
    return any(p == s or (s.endswith('/') and p.startswith(s)) for s in SOLVER)


rc, out = git('diff', '--name-status', PIN, HEAD)
rows = [ln.split('\t') for ln in out.strip().splitlines()]
groups = {}
code_bad, disc_in = [], []
for st, path in rows:
    f_sol, f_code, f_disc = in_solver(path), (path in CODE or path in S0), (path.startswith('scripts/') or path in DISC)
    if f_sol or f_code:
        code_bad.append(f'{st} {path}')
    if f_disc:
        disc_in.append(f'{st} {path}')
    top = '/'.join(path.split('/')[:3]) if path.startswith('docs/data/') or path.startswith('docs/reviews/rint2_') else path
    g = groups.setdefault((st, top), [0, False, False, False])
    g[0] += 1
    g[1] |= f_sol
    g[2] |= f_code
    g[3] |= f_disc
print(f'# 핀 {PIN[:12]} → 봉인 꼴 {HEAD[:12]} · 바뀐 파일 {len(rows)} (A 새 {sum(r[0] == "A" for r in rows)} · M 고침 {sum(r[0] == "M" for r in rows)} · '
      f'D 지움 {sum(r[0] == "D" for r in rows)})')
print('| 상태 | 자리 (폴더는 묶음) | 파일 수 | 다섯 경로 밖 | CODE_FILES 20 · S0 일곱 밖 | 규율 검사 입력 밖 |')
print('|---|---|---|---|---|---|')
for (st, top), (n, a, b, c) in sorted(groups.items(), key=lambda x: x[0][1]):
    print(f'| {st} | `{top}` | {n} | {"안" if a else "밖"} | {"안" if b else "밖"} | {"**안**" if c else "밖"} |')
rcq, _ = git('diff', '--quiet', PIN, HEAD, '--', *SOLVER)
print(f'git diff --quiet {PIN[:12]} {HEAD[:12]} -- <다섯 경로> → rc {rcq} ({"같음 = 원장 §2 같은 핀" if rcq == 0 else "다름"})')
print(f'CODE_FILES {len(CODE)} · S0 일곱 {len(S0)} · 다섯 경로 · CODE_FILES · S0 일곱 안의 바뀐 파일: {code_bad if code_bad else "없음"}')
print(f'규율 검사 입력 안의 바뀐 파일: {disc_in if disc_in else "없음"}' + (' (→ 그 판으로 규율 검사를 직접 돌려 본다)' if disc_in else ''))
sys.exit(0 if (rcq == 0 and not code_bad and rc == 0) else 1)
