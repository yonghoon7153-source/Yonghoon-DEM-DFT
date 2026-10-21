#!/usr/bin/env python3
"""Compare assertion lines of two test logs (Codex vs ours) after path normalization.

Assertion line = starts (after spaces) with PASS / FAIL / OK / ✓ / ✗ / PENDING, or is a 'N PASS · M FAIL' /
'SELFTEST ...' summary.  Absolute paths and Windows separators are normalized; RuntimeWarning lines ignored.
Usage: compare_logs.py codex.log ours.log label [out.json]
"""
import json, re, sys

a_p, b_p, label = sys.argv[1], sys.argv[2], sys.argv[3]
out_p = sys.argv[4] if len(sys.argv) > 4 else None
PAT = re.compile(r'^\s*(PASS|FAIL|OK|✓|✗|PENDING)\b|^\s*\d+ PASS · \d+ FAIL|SELFTEST')


def norm(s):
    s = s.replace('\\\\', '/').replace('\\', '/')
    s = re.sub(r'[A-Za-z]:/[^\s\'"]*?/(source|staged_source|oldsrc_2b9efa253/source|rint2rev_repro/source)/', '<SRC>/', s)
    s = re.sub(r'/tmp/claude-0/[^\s\'"]*?/(source|oldsrc_2b9efa253/source)/', '<SRC>/', s)
    s = re.sub(r'(<SRC>/)+', '<SRC>/', s)
    s = re.sub(r'[A-Za-z]:/[^\s\'"]+|/tmp/[^\s\'"]+', '<PATH>', s)
    return s.rstrip()


def lines(p):
    with open(p, 'rb') as f:
        t = f.read().decode('utf-8', 'replace').replace('\r\n', '\n').replace('\r', '\n')
    return [norm(x) for x in t.split('\n') if PAT.search(x)]


A, B = lines(a_p), lines(b_p)
same = sum(1 for x, y in zip(A, B) if x == y)
diffs = [{'i': i, 'codex': x, 'ours': y} for i, (x, y) in enumerate(zip(A, B)) if x != y]
res = {'label': label, 'codex_n': len(A), 'ours_n': len(B), 'same_in_order': same, 'n_diff': len(diffs) + abs(len(A) - len(B)),
       'diffs': diffs[:60], 'codex_only_tail': A[len(B):][:20], 'ours_only_tail': B[len(A):][:20]}
print(f"{label}: codex {len(A)} lines · ours {len(B)} · same-in-order {same} · differing {len(diffs)} · len-gap {len(A)-len(B)}")
for d in diffs[:8]:
    print('   codex:', d['codex'][:230]); print('   ours :', d['ours'][:230])
if out_p:
    json.dump(res, open(out_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
