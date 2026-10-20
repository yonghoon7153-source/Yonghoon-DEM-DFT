"""Exact same-name byte check: bundle rint_g2_impl_reverify_20261015/tmp/join_independent/X  <->  repo
docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/evidence/join_fixtures/X ; plus verdict and
source_manifest.  Read-only.

Usage: python3 -I prior_vs_repo_named.py <bundle_root> <repo_root> <out.tsv>
"""
import hashlib
import os
import sys

broot, rroot, out = sys.argv[1], sys.argv[2], sys.argv[3]
EVD = 'docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015'
pairs = [
    ('rint_g2_impl_reverify_20261015/codex_review_rint_g2_impl_fix_recheck_20261015.md',
     'docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md'),
    ('rint_g2_impl_reverify_20261015/source_manifest.json', EVD + '/source_manifest.json'),
]
jd = os.path.join(broot, 'rint_g2_impl_reverify_20261015/tmp/join_independent')
for f in sorted(os.listdir(jd)):
    pairs.append(('rint_g2_impl_reverify_20261015/tmp/join_independent/' + f, EVD + '/evidence/join_fixtures/' + f))
n_files_bundle = sum(len(fn) for _, _, fn in os.walk(os.path.join(broot, 'rint_g2_impl_reverify_20261015')))
same = 0
rows = []
for b, r in pairs:
    pb, pr = os.path.join(broot, b), os.path.join(rroot, r)
    xb = open(pb, 'rb').read()
    ok = os.path.isfile(pr) and open(pr, 'rb').read() == xb
    same += ok
    rows.append((b, hashlib.sha256(xb).hexdigest(), len(xb), r if ok else '-'))
with open(out, 'w', encoding='utf-8') as fh:
    for row in rows:
        fh.write('\t'.join(map(str, row)) + '\n')
print('bundle prior files', n_files_bundle, 'pairs checked', len(pairs), 'same-name byte-identical', same)
for row in rows:
    if row[3] == '-':
        print('  DIFFERENT/MISSING', row[0])
repo_fixtures = len(os.listdir(os.path.join(rroot, EVD, 'evidence/join_fixtures')))
print('repo join_fixtures files', repo_fixtures)
