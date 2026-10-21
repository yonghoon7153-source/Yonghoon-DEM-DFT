#!/usr/bin/env python3
"""Summarize Codex probe outputs in <dir>/evidence (resume · receipt · grammar) → stdout JSON (short)."""
import json
import os
import sys

D = os.path.abspath(sys.argv[1])
E = os.path.join(D, 'evidence')
out = {}


def load(n):
    p = os.path.join(E, n)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


r = load('resume_recheck.json')
if r is not None:
    cs = r.get('cases', {})
    items = cs.items() if isinstance(cs, dict) else enumerate(cs)
    mism = {}
    n = 0
    for k, v in items:
        n += 1
        if isinstance(v, dict) and v.get('matches') is False:
            mism[k if isinstance(k, str) else v.get('name')] = {'expected': v.get('expected'), 'actual': v.get('actual')}
    out['resume_recheck'] = {'keys': list(r.keys())[:12], 'n_cases': n, 'mismatch': mism, 'summary': r.get('summary')}

q = load('receipt_ids_recheck.json')
if q is not None:
    cs = q.get('cases', {})
    mism = {k: {'expected': v.get('expected'), 'actual': v.get('actual')} for k, v in cs.items() if isinstance(v, dict) and v.get('matches') is False}
    sel = {k: {'matches': v.get('matches'), 'actual': v.get('actual')} for k, v in cs.items()
           if k in ('g2c_c_cpl7_missing', 'g2c_c_cpl8_missing', 'g2c_missing_column_actual_cli', 'lexical_precision_boundary')}
    out['receipt_ids_recheck'] = {'n_cases': len(cs), 'summary': q.get('summary'), 'mismatch': mism, 'selected': sel}

for name in ('grammar_provenance.json',):
    g = load(name)
    if g is not None:
        res = g.get('results', {})
        out[name] = {'case_count': g.get('case_count'), 'all_expectations_satisfied': g.get('all_expectations_satisfied'),
                     'unsatisfied': {k: {'expected_gate': v.get('expected_gate'), 'gate': v.get('gate'), 'raw_status': v.get('raw_status'),
                                         'problems_head': [p[:140] for p in v.get('problems', [])[:3]]}
                                     for k, v in res.items() if not v.get('expectation_satisfied')},
                     'satisfied': sorted(k for k, v in res.items() if v.get('expectation_satisfied'))}
gw = load('grammar_windows_r32.json')
if gw is not None:
    out['grammar_windows_r32'] = {'initial': gw.get('initial'), 'crlf': {k: v.get('crlf_count') for k, v in gw.get('file_bytes', {}).items()},
                                  'after': gw.get('after_synthetic_fixture_lf_bytes_only')}
gt = load('grammar_types.json')
if gt is not None:
    out['grammar_types'] = gt if len(json.dumps(gt)) < 2500 else {'keys': list(gt.keys())}
kb = load('kit_byte_checks.json')
if kb is not None:
    out['kit_byte_checks'] = {k: kb[k] for k in kb if k not in ('decks', 'physical_table', 'files')} if isinstance(kb, dict) else None
ha = load('history_actual_audit.json')
if ha is not None:
    out['history_actual'] = {k: ha.get(k) for k in ('reader_rc', 'equal_except_run_dir', 'rows', 'unsafe_members', 'sealed_manifest_matches')}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
