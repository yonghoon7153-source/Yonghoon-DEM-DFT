#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 7 회차 (11-02) — 고침 보고 둘 · 등록 R §10-5 의 숫자 · 전칭 · 줄 번호를 git · 시험 로그 · 코드와 대조 (읽기 전용 · git = 이 작업 트리).

  python3 claims_check.py <작업 트리>
출력 = JSON 줄 (항목마다 잰 값).  판정 (같음 · 다름 · 잴 수 없음) 은 보고서 표에서 사람이 매긴다.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()


def git(*a):
    p = subprocess.run(['git', '-C', str(WT), *a], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else f'<rc {p.returncode}: {p.stderr.strip()[:200]}>'


def out(tag, **kw):
    print(json.dumps(dict(item=tag, **kw), ensure_ascii=False, sort_keys=True), flush=True)


COMMITS = ['483cf413e', '93d8c3d34', 'dde41fb2f', 'db2e1b2b4', 'ac888877d', '7f1d7dde3', 'b309f0b78', 'f3f6de276', '8bf1fd6ad',
           'c738a6826', '4499f3ffd', '7f277f9e7', '2bef88e60', '2c1a06c57', '0658c0ac6', 'e12756051', '7d6ea1e6f']
order = git('rev-list', '--reverse', 'd6e8d1b44..0658c0ac6').split()
for c in COMMITS:
    full = git('rev-parse', '--verify', '-q', c + '^{commit}').strip()
    files = [ln for ln in git('show', '--name-only', '--format=', c).splitlines() if ln.strip()]
    body = git('log', '-1', '--format=%B', c)
    out('commit', short=c, full=full[:12] if full else None, subject=git('log', '-1', '--format=%s', c).strip()[:120],
        in_range=(full in order), pos=(order.index(full) if full in order else None),
        cherry_picked=('cherry picked from commit' in body), n_files=len(files),
        code_files=[f for f in files if f.startswith('scripts/') or 'registration_R' in f])

#  S0_SAME_FILES · CODE_FILES (194 봉인) 와 바뀐 파일의 겹침
changed = sorted(set(git('diff', '--name-only', '7d6ea1e6f', '0658c0ac6').split()))
chain = (WT / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
m = re.search(r'S0_SAME_FILES\s*=\s*\(([^)]*)\)', chain)
s0 = re.findall(r"'([^']+)'", m.group(1)) if m else None
code194 = None
for cand in sorted((WT / 'scripts').glob('*194*.py')) + [WT / 'scripts' / 'run_network_194_parallel.py']:
    if cand.exists():
        t = cand.read_text(encoding='utf-8', errors='replace')
        mm = re.search(r'CODE_FILES\s*=\s*[\(\[]([^\)\]]*)[\)\]]', t, re.S)
        if mm:
            code194 = (cand.name, re.findall(r"['\"]([^'\"]+)['\"]", mm.group(1)))
            break
out('seal_overlap', changed_n=len(changed), changed_code=[f for f in changed if f.startswith(('scripts/', 'webapp/'))],
    s0_same_files=s0, s0_overlap=sorted(set(changed) & {('scripts/' + x if not x.startswith('scripts/') else x) for x in (s0 or [])}),
    code194_file=(code194 or [None])[0], code194_n=(len(code194[1]) if code194 else None),
    code194_overlap=(sorted(set(changed) & {('scripts/' + x if '/' not in x else x) for x in code194[1]}) if code194 else None))

#  줄 번호 — 보고서 둘이 적은 판의 함수 자리
LINE_CLAIMS = {
    'db2e1b2b4': {'def proc_stat': 2357, 'def _run_session_ours': 2410, 'def _run_kin': 2421, 'def group_members': 2457, 'def group_settle': 2557,
                  'def run_in_group': 2630, 'def recover_group': 6411, 'CUDA_ERROR_WORDS = ': 2787, 'def words_cause': 3590, 'def words_keep': 3603,
                  'def stop_cause': 3619, 'def orphan_cause': 3646, 'def attempt_open': 3349, 'def found_attempts_problem': 3780},
    '4499f3ffd': {'def stop_cause': 3643, "    elif code == 'GROUP_UNCONFIRMED':": 3665, 'def runner_rc_failed': 3620, 'def recover_group': 6444,
                  'def orphan_cause': 3675, 'def chain_end_failed': 3627, 'CUDA_ERROR_WORDS = ': 2796, 'def words_cause': 3600},
}
for rev, claims in LINE_CLAIMS.items():
    src = git('show', f'{rev}:scripts/rint_r_chain.py').splitlines()
    got = {}
    for needle, want in claims.items():
        hits = [i + 1 for i, ln in enumerate(src) if ln.startswith(needle)]
        got[needle] = {'claimed': want, 'found': hits[:3]}
    out('lines', rev=rev, rows=got)
#  4499f3ffd 의 개별 줄 (보고서 PC6-13 이 적은 줄의 글)
src13 = git('show', '4499f3ffd:scripts/rint_r_chain.py').splitlines()
out('lines_4499_text', rows={str(n): src13[n - 1].strip()[:110] for n in (3667, 4194, 3714, 6470, 6518, 3620, 3627, 2796, 3600)})
#  db2e1b2b4 이후 사슬 파일을 바꾼 커밋
out('chain_file_commits', rows=git('log', '--format=%h %s', 'd6e8d1b44..0658c0ac6', '--', 'scripts/rint_r_chain.py').splitlines())
out('chain_same_4499_head', same=(git('rev-parse', '4499f3ffd:scripts/rint_r_chain.py') == git('rev-parse', '0658c0ac6:scripts/rint_r_chain.py')))

#  웹앱 grep (보고서 PC6-13 "0 건")
words = ['GROUP_UNCONFIRMED', 'CUDA_ERROR_', 'runner_rc', 'group_unconfirmed', 'parent_dead', 'cudaError', 'CUBLAS']
hits = {}
for w in words:
    r = subprocess.run(['grep', '-rIl', '--', w, str(WT / 'webapp')], capture_output=True, text=True)
    hits[w] = [str(Path(x).relative_to(WT)) for x in r.stdout.split()]
out('webapp_grep', rows=hits)

#  시험 로그 (고침 증거 폴더) 끝 줄
for sub in ('pc6_fix/logs', 'pc6_13_fix/logs'):
    d = WT / 'docs' / 'reviews' / 'rint2_rr_fix_evidence_20261023' / sub
    rows = {}
    for p in sorted(d.rglob('*')):
        if p.is_file() and p.suffix in ('.log', '.out', '.txt', '.json'):
            t = p.read_text(encoding='utf-8', errors='replace')
            tl = [ln.strip() for ln in t.splitlines() if re.search(r'test_rint_r_chain(_e2e)?:|PASS · \d+ FAIL|\d+ PASS|FAILED', ln)]
            rows[str(p.relative_to(d))] = tl[-3:] if tl else (f'<{p.suffix} {len(t)} B>' if p.suffix == '.json' else None)
    out('evidence_logs', sub=sub, rows=rows)
