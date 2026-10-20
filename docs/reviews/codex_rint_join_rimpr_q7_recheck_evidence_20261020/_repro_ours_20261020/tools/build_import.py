"""Build the repo import of the Codex Rint join / Q7 recheck bundle (10-20).

Writes ONLY:
  docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md        (verdict, bytes as received)
  docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/        (bundle review folder minus verdict,
      bundle tmp/ -> fixtures/ (repo .gitignore has tmp/), GitHub tree lists = hash only, + PACKAGE_MANIFEST.json,
      _members_mini.tsv; _README_import.md and _repro_ours_20261020/ are written separately)
Refuses to overwrite anything.
Usage: python3 -I build_import.py
"""
import hashlib
import json
import os
import shutil
import sys

SCR = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad'
X = SCR + '/import_rq7/x'
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a43562c127acff2de'
REV = 'rint_join_q7_recheck_20261020'
PRIOR = 'rint_g2_impl_reverify_20261015'
VERDICT_NAME = 'codex_review_rint_join_rimpr_q7_recheck_20261020.md'
VERDICT_DEST = 'docs/reviews/' + VERDICT_NAME
EVD = 'docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020'
PRIOR_EVD = 'docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015'
BIG = {
    REV + '/evidence/tree.json':
        'GitHub tree 응답 (검토 핀 2b9efa253) · 내용 = git ls-tree -r 2b9efa253 의 blob 11,446 (경로 · sha · 모드 같음 · 10-20 확인) · 2 MB 초과 → 해시만',
    REV + '/evidence/base_tree.json':
        'GitHub tree 응답 (대조 핀 dcb97f1ed) · 내용 = git ls-tree -r dcb97f1ed 의 blob 9,768 (같음 · 10-20 확인) · 2 MB 초과 → 해시만',
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_new(rel, data):
    dest = os.path.join(WT, rel)
    if os.path.exists(dest):
        sys.exit('refuse to overwrite ' + rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'xb') as fh:
        fh.write(data)


pkg = json.load(open(os.path.join(X, 'PACKAGE_MANIFEST.json'), encoding='utf-8'))
listed = {e['path']: e for e in pkg['files']}
rows = []
kept = kept_bytes = 0
# all members = manifest entries + the manifest itself
members = sorted(listed) + ['PACKAGE_MANIFEST.json']
for m in members:
    src = os.path.join(X, m)
    data = open(src, 'rb').read()
    h, n = sha(data), len(data)
    if m != 'PACKAGE_MANIFEST.json':
        assert h == listed[m]['sha256'] and n == listed[m]['bytes'], m
    if m == 'PACKAGE_MANIFEST.json':
        write_new(EVD + '/PACKAGE_MANIFEST.json', data)
        status, note = 'meta', '묶음 뿌리 · 1,306 항목 sha256 · 크기 = 풀린 파일 전수 같음 (10-20) · 전체 묶음 (소스 포함 · 받지 않음) sha256 2588ff6f0185e8cd64e5d1e2e03a19c901da7d575d95485e5b50439161895127'
        kept += 1; kept_bytes += n
    elif m == REV + '/' + VERDICT_NAME:
        write_new(VERDICT_DEST, data)
        status, note = 'verdict', '→ ' + VERDICT_DEST + ' (바이트 그대로)'
    elif m in BIG:
        status, note = 'big-hash-only', BIG[m]
    elif m.startswith(PRIOR + '/'):
        rest = m[len(PRIOR) + 1:]
        if rest == 'codex_review_rint_g2_impl_fix_recheck_20261015.md':
            repo = 'docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md'
        elif rest == 'source_manifest.json':
            repo = PRIOR_EVD + '/source_manifest.json'
        elif rest.startswith('tmp/join_independent/'):
            repo = PRIOR_EVD + '/evidence/join_fixtures/' + rest[len('tmp/join_independent/'):]
        else:
            sys.exit('unexpected prior member ' + m)
        if open(os.path.join(WT, repo), 'rb').read() != data:
            sys.exit('prior member differs from repo copy: ' + m)
        status, note = 'dup-repo', '리포 사본 = ' + repo + ' (같은 이름 · 같은 바이트)'
    elif m.startswith(REV + '/'):
        rest = m[len(REV) + 1:]
        if rest.startswith('tmp/'):
            rel = EVD + '/fixtures/' + rest[len('tmp/'):]
            note = '리포 = fixtures/' + rest[len('tmp/'):] + ' (리포 .gitignore 의 tmp/ 때문에 폴더 이름만 바꿈 · 바이트 그대로)'
        else:
            rel = EVD + '/' + rest
            note = '-'
            if rest == 'submitted/codex_rint_join_rimpr_q7_recheck_request_20261020_send.md':
                note = '발송본 · 리포 docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md (2b9efa253 판 = HEAD 판) 과 7 행 (리뷰 핀 SHA 자리 표시 → 실제 SHA) 만 다름'
        write_new(rel, data)
        status = 'keep'
        kept += 1; kept_bytes += n
    else:
        sys.exit('unexpected member ' + m)
    rows.append((h, n, status, m, note))

with open(os.path.join(WT, EVD, '_members_mini.tsv'), 'x', encoding='utf-8') as fh:
    fh.write('sha256\tbytes\tstatus\tpath (받은 묶음 안)\tnote\n')
    for r in rows:
        fh.write('\t'.join(map(str, r)) + '\n')
from collections import Counter
c = Counter(r[2] for r in rows)
print('members', len(rows), dict(c), 'kept files', kept, 'kept bytes', kept_bytes)
