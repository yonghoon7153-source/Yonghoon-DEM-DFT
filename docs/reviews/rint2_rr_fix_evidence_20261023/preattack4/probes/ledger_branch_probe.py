#!/usr/bin/env python3
"""Round-4 probe — Q9 rev 3 §3-5 '같은 단위 시도는 차례로만' (L112–L114) as literally written:
  · 시도 폴더는 시작 때의 원장 커밋 sha 를 싣는다 · 합치기는 그 커밋에 자기 항목과 같은 단위 앞 항목들의 결과 줄이 모두 있는지 본다
  · 첫 · 끝 합치기의 원장은 바이트 접두 관계
Question: does the literal check stop attempt #2 started BEFORE #1's real result line exists, if #2's start commit is a side-branch commit
carrying a placeholder result line for #1?  Compared with two stronger checks (start-commit ledger = byte prefix of the merged ledger ·
start commit = ancestor of the merged ledger commit).  Then: what can the operator gain, given L105 ATTEMPT_AFTER_ADOPTED?
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

d = Path(tempfile.mkdtemp(prefix='ledger_probe_', dir=sys.argv[1] if len(sys.argv) > 1 else None))


def git(*a):
    return subprocess.run(['git', '-C', str(d), *a], capture_output=True, text=True, check=True).stdout.strip()


def commit(text, msg):
    (d / 'ledger.txt').write_text(text)
    git('add', 'ledger.txt')
    git('-c', 'user.name=p', '-c', 'user.email=p@x', 'commit', '-q', '-m', msg)
    return git('rev-parse', 'HEAD')


git('init', '-q', '-b', 'main')
E1 = 'entry #1 unit=U(c1,P1,R_j_hi) machine=kgy env=E_k\n'
E2 = 'entry #2 unit=U(c1,P1,R_j_hi) machine=gabia env=E_g\n'
c1 = commit(E1, 'e1')
c2 = commit(E1 + E2, 'e2')
git('checkout', '-q', '-b', 'side')
FAKE = 'result #1 stop=pre_result folder_sha=0000000000000000\n'
s = commit(E1 + E2 + FAKE, 'placeholder result #1')
start_sha_2 = s                                    # attempt #2 starts here (on gabia) and records this sha (L113)
git('checkout', '-q', 'main')
REAL1 = 'result #1 stop=pre_result cause=presolve_reject folder_sha=9f2c…\n'   # #1 run later with a forbidden env var → 풀기 전 거부
c3 = commit(E1 + E2 + REAL1, 'r1')
R2 = 'result #2 complete folder_sha=41aa…\n'
c4 = commit(E1 + E2 + REAL1 + R2, 'r2')
final = (d / 'ledger.txt').read_bytes()
at_start = subprocess.run(['git', '-C', str(d), 'show', f'{start_sha_2}:ledger.txt'], capture_output=True, check=True).stdout
literal = all(f'result #{k}'.encode() in at_start for k in (1,)) and b'entry #2' in at_start
prefix = final.startswith(at_start)
ancestor = subprocess.run(['git', '-C', str(d), 'merge-base', '--is-ancestor', start_sha_2, c4]).returncode == 0
res = {'start_commit_of_#2': start_sha_2[:10], 'is_on_main': ancestor,
       'literal_check_L113 (earlier result lines present in start commit)': literal,
       'byte_prefix_check (start-commit ledger ⊑ merged ledger)': prefix,
       'ancestor_check (start commit ⊑ merged commit)': ancestor}
# what the operator gets once #2's σ was seen first (enumerating #1's fate; rules L119 · L129 · L105)
res['outcomes_after_seeing_#2'] = {
    '#1 = deliberate pre-solve reject (결과 전)': 'adopt #2',
    '#1 = normal run (완주)': '#1 adopted → #2 = ATTEMPT_AFTER_ADOPTED → STOPPED',
    '#1 never run (폴더 · 거부 기록 없음 = 결과 뒤 · L118)': '#1 adopted (folderless) → unit STOPPED (+ #2 ATTEMPT_AFTER_ADOPTED)'}
res['net'] = '{adopt #2 | STOPPED} — a veto, not a choice between two σ draws (ATTEMPT_AFTER_ADOPTED closes the second branch)'
res['tmp'] = str(d)
print(json.dumps(res, ensure_ascii=False, indent=1))
