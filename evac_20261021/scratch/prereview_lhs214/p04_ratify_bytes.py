#!/usr/bin/env python3
"""P04 — 비준 커밋 바이트 대조 (요청서 §0 ① · 부록 A 끝 '날짜 자리 대조') 와 메인 정정 (7f99be67c) 이 두 등록에서 바꾼 줄.
 ① 묶음 문서 (f82929b06 판) 의 ````diff 블록 둘을 떼어 그대로 (⬜(날짜) 남김) 비준 전 문서 (fe23f2b83 판) 에 git apply → E
 ② 비준 커밋 문서에서 '10-21 ·' → '⬜(날짜)' 로 되돌린 글 → R'  ·  E == R' (바이트)
 ③ 자리 수 (묶음 diff 의 ⬜(날짜) 수 · 비준 문서의 '10-21 ·' 수 · 비준 전 문서의 '10-21 ·' 수)
 ④ f82929b06 → 7f99be67c 의 두 등록 diff 줄 · 그 줄이 §9-9 / §9-4 '대화 원문' 자리인지
 ⑤ 묶음 문서 diff 블록이 a69963967 · f82929b06 · 7f99be67c 에서 같은지 (메인 정정이 diff 블록을 건드렸나)
재실행: python3 -I p04_ratify_bytes.py <worktree> <scratch_dir>"""
import json, re, subprocess, sys, tempfile, difflib
from pathlib import Path
WT = sys.argv[1]
SCR = Path(sys.argv[2])
PKG = 'docs/reviews/lhs214_relaunch_package_20261020.md'
D194 = 'docs/reviews/lhs_network_batch_registration_20261007_g2.md'
DSUP = 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md'
PRE, RAT, HEAD, MAINP = 'fe23f2b83', 'f82929b06', '7f99be67c', 'a69963967'


def show(rev, f):
    return subprocess.run(['git', 'show', f'{rev}:{f}'], cwd=WT, capture_output=True, check=True).stdout


def blocks(pkg_bytes):
    t = pkg_bytes.decode('utf-8')
    return re.findall(r'^````diff\n(.*?)^````\n', t, re.M | re.S)


res = {}
pk = {r: show(r, PKG) for r in (MAINP, RAT, HEAD)}
bl = {r: blocks(b) for r, b in pk.items()}
res['diff_blocks_n'] = {r: len(v) for r, v in bl.items()}
res['diff_blocks_same_a699_f829_head'] = bl[MAINP] == bl[RAT] == bl[HEAD]
b194, bsup = bl[RAT]
res['placeholder_in_diff'] = {'194': b194.count('⬜(날짜)'), 'supp': bsup.count('⬜(날짜)')}
res['placeholder_in_diff_added_lines_only'] = {k: sum(ln.count('⬜(날짜)') for ln in b.split('\n') if ln.startswith('+')) for k, b in (('194', b194), ('supp', bsup))}
with tempfile.TemporaryDirectory(dir=SCR) as td:
    td = Path(td)
    for f in (D194, DSUP):
        p = td / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(show(PRE, f))
    (td / 'p194.diff').write_text(b194, encoding='utf-8')
    (td / 'psup.diff').write_text(bsup, encoding='utf-8')
    r1 = subprocess.run(['git', 'apply', '--no-index', '-v', 'p194.diff'], cwd=td, capture_output=True, text=True)
    r2 = subprocess.run(['git', 'apply', '--no-index', '-v', 'psup.diff'], cwd=td, capture_output=True, text=True)
    res['apply_rc'] = [r1.returncode, r2.returncode]
    res['apply_err'] = [r1.stderr[-300:], r2.stderr[-300:]]
    E = {f: (td / f).read_bytes() for f in (D194, DSUP)}
for f, tag in ((D194, '194'), (DSUP, 'supp')):
    pre = show(PRE, f).decode('utf-8')
    rat = show(RAT, f).decode('utf-8')
    hd = show(HEAD, f).decode('utf-8')
    rev = rat.replace('10-21 ·', '⬜(날짜)')
    res[f'{tag}_pre_has_10-21·'] = pre.count('10-21 ·')
    res[f'{tag}_rat_has_10-21·'] = rat.count('10-21 ·')
    res[f'{tag}_rat_reverted_equals_applied'] = rev.encode('utf-8') == E[f]
    if rev.encode('utf-8') != E[f]:
        res[f'{tag}_mismatch_diff'] = list(difflib.unified_diff(E[f].decode('utf-8').split('\n'), rev.split('\n'), lineterm='', n=0))[:40]
    # 정정 커밋의 변화
    dl = list(difflib.unified_diff(rat.split('\n'), hd.split('\n'), lineterm='', n=0))
    res[f'{tag}_rat_to_head_changed_lines'] = [ln for ln in dl if ln[:1] in '+-' and not ln.startswith(('+++', '---'))]
    # 같은 커밋 쌍에서 바이트 sha256
    import hashlib
    res[f'{tag}_sha256'] = {r: hashlib.sha256(show(r, f)).hexdigest() for r in ('34713ac96', PRE, RAT, HEAD)}
print(json.dumps(res, ensure_ascii=False, indent=1))
