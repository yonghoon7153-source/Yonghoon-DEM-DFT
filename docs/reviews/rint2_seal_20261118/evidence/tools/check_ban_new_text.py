#!/usr/bin/env python3
"""봉인 꼴 커밋이 더하거나 고친 파일 전부를 철회값 등록부 (`docs/reviews/claims.json` `quotation_ban` · 핀 판) 로 훑는다 — 게이트와 같은 함수
(`scripts/check_review_findings.ban_sweep(files=…)` · 정규화 · 배너 · ±2 줄 표지 규칙 그대로) · 읽기만.

argv: <봉인 꼴 사본 (git)> <핀 rev> <봉인 꼴 rev> [<등록부 기대 rev (기본 = 핀 rev)>]
덧붙여: 붙일 글 · 봉인본 · 명령 문서의 **더한 줄만** 모아 등록부 글자 (정규화 포함) 가 있는지 따로 센다 (배너 · 표지 면제 없이 — 더 엄한 쪽).
"""
import fnmatch
import os
import subprocess
import sys

REPO, PIN, HEAD = sys.argv[1:4]
CLAIMS_REV = sys.argv[4] if len(sys.argv) > 4 else PIN
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import check_review_findings as CRF  # noqa: E402


def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, env=ENV).stdout.decode('utf-8', 'replace')


claims_pin = subprocess.run(['git', '-C', REPO, 'show', f'{CLAIMS_REV}:docs/reviews/claims.json'], capture_output=True, env=ENV).stdout
claims_tree = open(os.path.join(REPO, 'docs/reviews/claims.json'), 'rb').read()
print(f'# claims.json 트리 = {CLAIMS_REV[:12]} 판 바이트 같음: {claims_pin == claims_tree}')
rows = [ln.split('\t') for ln in git('diff', '--name-status', PIN, HEAD).strip().splitlines()]
files = [os.path.join(REPO, p) for st, p in rows if st in ('A', 'M')]
probs, n, nb = CRF.ban_sweep(REPO, files=files)
in_globs = sum(any(fnmatch.fnmatch(p, g) for g in CRF.BAN_SCAN_GLOBS) for _st, p in rows)
print(f'ban_sweep (게이트 함수 · 바뀐 파일 {n} · 그 가운데 게이트 스윕 글롭 안 {in_globs} · 등록부 {nb} 패턴) → 문제 {len(probs)}')
for p in probs:
    print('  ', p)
bans = [b.get('pattern') for b in CRF.load_bans(os.path.join(REPO, CRF.CLAIMS_DEFAULT))[0] if b.get('pattern')]
added = []
for st, p in rows:
    if st not in ('A', 'M') or not (p.endswith('.md') or p.endswith('.py')) or not (p.startswith('docs/reviews/rint2_seal_') or p in (
            'docs/reviews/rint2_kgy_commands_20261020.md', 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md')):
        continue
    d = git('diff', '-U0', PIN, HEAD, '--', p)
    added += [(p, ln[1:]) for ln in d.splitlines() if ln.startswith('+') and not ln.startswith('+++')]
hits = [(p, b) for p, ln in added for b in bans if b in ln or CRF._ban_norm(b) in CRF._ban_norm(ln)]
print(f'더한 줄 (봉인 기록 폴더 · 명령 문서 · 원본 자리) {len(added)} 줄 · 등록부 글자 (면제 없이) {len(hits)} 건' + (f' {hits[:5]}' if hits else ''))
sys.exit(0 if (not probs and not hits and claims_pin == claims_tree) else 1)
