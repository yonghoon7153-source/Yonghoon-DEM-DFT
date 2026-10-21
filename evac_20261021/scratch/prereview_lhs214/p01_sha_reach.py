#!/usr/bin/env python3
"""P01 — SHA 존재 · 원격 본 가지 머리 (eabeda83c, gh api 로 읽은 값) 에서 닿는지 · 로컬 본 가지 ref 에서 닿는지.
재실행: python3 -I p01_sha_reach.py <worktree>   (읽기 전용 git 만)"""
import json, subprocess, sys
WT = sys.argv[1] if len(sys.argv) > 1 else '.'
REMOTE_HEAD = 'eabeda83cbe2da166a0216087f25afd98bf97097'   # gh api repos/.../branches/claude/stoic-knuth-NObVQ (10-21 08:1x UTC)
LOCAL_BRANCH = 'claude/stoic-knuth-NObVQ'


def git(*a):
    r = subprocess.run(['git', *a], cwd=WT, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


shas = ['a45a980e9', 'e9267000b', 'a76f59d0d16c58b2f7816d67a3432f94367e46f0', '34713ac9650ece7c8d59b7c4d9a2aefccee693ea',
        'a6996396774064fa159d360da0e1d26877b66c33', 'fe23f2b839f0a49adb077348fec6d4c85443b62a', 'f82929b0644be39b44e9fba9ea04cf9d60de9146',
        '02393562f', '7f99be67c']
out = {}
_, lb, _ = git('rev-parse', LOCAL_BRANCH)
for s in shas:
    rc, t, _ = git('cat-file', '-t', s)
    full = git('rev-parse', s)[1] if rc == 0 else None
    on_remote = git('merge-base', '--is-ancestor', s, REMOTE_HEAD)[0] == 0 if rc == 0 else None
    on_local_branch = git('merge-base', '--is-ancestor', s, lb)[0] == 0 if rc == 0 else None
    out[s] = dict(exists=(rc == 0), type=t if rc == 0 else None, full=full, on_remote_head=on_remote, on_local_branch_ref=on_local_branch)
print(json.dumps(dict(remote_head=REMOTE_HEAD, local_branch_ref=lb, shas=out), indent=1))
