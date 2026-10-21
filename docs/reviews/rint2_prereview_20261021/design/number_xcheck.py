"""Cross-check long numbers (>= 7 significant digits) quoted in the design / registration / kgy documents against the
Codex verdict and our reproduction README.  A doc number 'matches' if its significant-digit string equals (or is a
rounding of) a significant-digit string present in the sources.

Usage: python3 -I number_xcheck.py <repo_root>
"""
import json
import os
import re
import sys

root = sys.argv[1]
DOCS = ['docs/reviews/rint_carbon_additive_design_v1_20261020.md',
        'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md',
        'docs/reviews/rint2_kgy_commands_20261020.md']
SRCS = ['docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md',
        'docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/_repro_ours_20261021/README.md',
        'docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/registration/registration_probe_results.json',
        'docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/geometry/convergence_probe_results.json',
        'docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/geometry/geometry_probe_results.json']
NUM = re.compile(r'\d[\d,]*\.\d+|\d{7,}')


def sig(tok):
    t = tok.replace(',', '')
    t = t.replace('.', '').lstrip('0')
    return t.rstrip('0') or '0'


def tokens(text):
    return [m.group(0) for m in NUM.finditer(text)]


src_text = ''
for s in SRCS:
    p = os.path.join(root, s)
    if os.path.exists(p):
        src_text += open(p, encoding='utf-8').read() + '\n'
src_sigs = set(sig(t) for t in tokens(src_text))

report = {}
for d in DOCS:
    text = open(os.path.join(root, d), encoding='utf-8').read()
    rows = []
    for ln_no, line in enumerate(text.splitlines(), 1):
        for tok in tokens(line):
            sg = sig(tok)
            if len(sg) < 7:
                continue
            exact = sg in src_sigs
            rounded = exact or any(s.startswith(sg[:-1]) and len(s) > len(sg) for s in src_sigs)
            rows.append({'line': ln_no, 'tok': tok, 'exact': exact, 'prefix_or_round': rounded})
    report[d] = rows
n_all = sum(len(v) for v in report.values())
n_miss = [(d, r) for d, v in report.items() for r in v if not r['prefix_or_round']]
print('long numbers in docs:', n_all, ' unmatched in sources:', len(n_miss))
for d, r in n_miss:
    print(' ', os.path.basename(d), 'L%d' % r['line'], r['tok'])
json.dump(report, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'number_xcheck.json'), 'w'), indent=1)
