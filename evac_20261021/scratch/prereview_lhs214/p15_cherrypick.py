#!/usr/bin/env python3
"""P15 — 작업 트리 커밋 (e9267000b · a45a980e9) ↔ 본 가지 cherry-pick (fe23f2b83 · f82929b06) 내용 대조 (요청서 §1 '충돌 0 · 내용 같음').
재실행: python3 -I p15_cherrypick.py <worktree>"""
import hashlib, json, subprocess, sys
WT = sys.argv[1]


def git(*a):
    return subprocess.run(['git', *a], cwd=WT, capture_output=True).stdout


res = {}
for wt_c, main_c in (('e9267000b', 'fe23f2b83'), ('a45a980e9', 'f82929b06')):
    files = sorted(set(git('diff', '--name-only', f'{main_c}^', main_c).decode().split()) | set(git('diff', '--name-only', f'{wt_c}^', wt_c).decode().split()))
    same = {f: hashlib.sha256(git('show', f'{wt_c}:{f}')).hexdigest() == hashlib.sha256(git('show', f'{main_c}:{f}')).hexdigest() for f in files}
    res[f'{wt_c}->{main_c}'] = dict(parent_wt=git('rev-parse', f'{wt_c}^').decode().strip(), parent_main=git('rev-parse', f'{main_c}^').decode().strip(),
                                    files=len(files), all_same=all(same.values()), differ=[f for f, v in same.items() if not v],
                                    patch_id_wt=git('show', wt_c).decode('utf-8', 'replace').count('\n'), msg_same=git('log', '-1', '--format=%B', wt_c) == git('log', '-1', '--format=%B', main_c))
print(json.dumps(res, ensure_ascii=False, indent=1))
