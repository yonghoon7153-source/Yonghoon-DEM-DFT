#!/usr/bin/env python3
"""P02 — 요청서 · 묶음 문서 · 증거 README · 두 등록 문서 (HEAD 판) 와 네 커밋 메시지의 7–40 자리 hex 토큰 → 커밋이면 HEAD (7f99be67c) 의 조상인지.
재실행: python3 -I p02_sha_tokens.py <worktree>"""
import json, re, subprocess, sys
WT = sys.argv[1] if len(sys.argv) > 1 else '.'
HEAD = '7f99be67c7bd66416e2b125e62cba50ca6f8a03a'
FILES = ['docs/reviews/codex_lhs214_relaunch_check_request_20261020.md', 'docs/reviews/lhs214_relaunch_package_20261020.md',
         'docs/reviews/lhs214_relaunch_s0b_evidence_20261021/README.md', 'docs/reviews/lhs_network_batch_registration_20261007_g2.md',
         'docs/reviews/lhs_network_batch_registration_20261012_supp20.md']
COMMITS = ['fe23f2b83', 'f82929b06', '02393562f', '7f99be67c']


def git(*a):
    r = subprocess.run(['git', *a], cwd=WT, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


tok = re.compile(r'(?<![0-9a-fA-F])([0-9a-f]{7,40})(?![0-9a-fA-F])')
res = {}
srcs = {f: git('show', f'{HEAD}:{f}')[1] for f in FILES}
for c in COMMITS:
    srcs[f'commit-msg {c}'] = git('log', '-1', '--format=%B', c)[1]
# 이 회차에서 바뀐 줄만 따로 (a69963967..HEAD 의 + 줄)
srcs['added-lines a69963967..HEAD'] = ''.join(ln[1:] + '\n' for ln in git('diff', 'a6996396774064fa159d360da0e1d26877b66c33', HEAD).splitlines()
                                              if ln.startswith('+') and not ln.startswith('+++')) if False else ''
d = git('diff', 'a6996396774064fa159d360da0e1d26877b66c33', HEAD)[1]
srcs['added-lines a69963967..HEAD'] = '\n'.join(ln[1:] for ln in d.splitlines() if ln.startswith('+') and not ln.startswith('+++'))
for name, txt in srcs.items():
    for m in tok.finditer(txt):
        t = m.group(1)
        if t.isdigit():
            continue
        rc, typ, _ = git('cat-file', '-t', t)
        typ = typ.strip()
        if rc != 0:
            kind = 'not-an-object'
        elif typ != 'commit':
            kind = typ
        else:
            anc = git('merge-base', '--is-ancestor', t, HEAD)[0] == 0
            kind = 'commit-ancestor-of-HEAD' if anc else 'commit-NOT-ancestor-of-HEAD'
        res.setdefault(kind, {}).setdefault(t, set()).add(name)
out = {k: {t: sorted(v) for t, v in sorted(d_.items())} for k, d_ in res.items()}
print(json.dumps({k: (v if k != 'commit-ancestor-of-HEAD' else {'count': len(v)}) for k, v in out.items()}, ensure_ascii=False, indent=1))
