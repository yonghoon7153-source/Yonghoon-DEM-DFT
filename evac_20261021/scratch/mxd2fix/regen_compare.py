#!/usr/bin/env python3
"""Regenerate the review's 9 D2 decks with the HEAD generator and the FIXED generator (scratch) and compare:
in.mixer = only comment lines may differ (non-comment logical commands token-identical) · deck_meta.json key-level diff.
usage: python3 -I -B regen_compare.py <old_gen.py> <new_gen.py> <out_json>"""
import json
import os
import subprocess
import sys
import tempfile

OLD, NEW, OUTJ = sys.argv[1:4]
CASES = [
    ('coated_g1_w0256_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244', '--dens-gen', 'lab20261014']),
    ('uncoated_r03_ncm_lab_soft', ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244', '--dens-gen', 'lab20261014']),
    ('coated_world_r03_ncm_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244', '--dens-gen', 'lab20261014']),
    ('mixed_03_05_w0256_lab_ref20', ['--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244',
                                     '--dens-gen', 'lab20261014', '--stiffen-se', '20', '--hold-bo-pairwise']),
    ('coated_g1_gen1_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244', '--dens-gen', 'gen1']),
    ('sticky_AM_r10_ncm_lab_soft', ['--gm-gamma', 'AM_P=10,AM_S=10', '--gm-wall-ncm', '10', '--gm-bo-se', '5', '--dens-gen', 'lab20261014']),
    ('coated_g1_bo637_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '637.32', '--dens-gen', 'lab20261014']),
    ('coated_g1_bo637_gen1_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '637.32', '--dens-gen', 'gen1']),
    ('mixed_ref20_dthalf_fullprec', ['--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244', '--dens-gen', 'lab20261014',
                                     '--stiffen-se', '20', '--hold-bo-pairwise', '--dt-factor', '0.5', '--dump-full-precision']),
]
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2']


def logical(text):
    lines, out, i = text.split('\n'), [], 0
    while i < len(lines):
        buf = [lines[i]]
        while buf[-1].rstrip().endswith('&') and i + 1 < len(lines):
            i += 1
            buf.append(lines[i])
        joined = ' '.join(b.rstrip()[:-1] if b.rstrip().endswith('&') else b for b in buf)
        code = joined.split('#', 1)[0]
        if code.split():
            out.append(code.split())
        i += 1
    return out


def run(gen, out, args):
    p = subprocess.run([sys.executable, '-I', '-B', gen, '--out', out] + BASE + args, capture_output=True, text=True,
                       env=dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1'))
    return p.returncode, (p.stderr.strip().splitlines() or [''])[-1]


res = {}
with tempfile.TemporaryDirectory() as td:
    for label, args in CASES:
        oa, ob = os.path.join(td, label, 'old'), os.path.join(td, label, 'new')
        ra, ea = run(OLD, oa, args)
        rb, eb = run(NEW, ob, args)
        rec = dict(rc_old=ra, rc_new=rb, refused_new=(eb if rb else None))
        if ra == 0 and rb == 0:
            ta, tb = (open(os.path.join(d, 'in.mixer'), encoding='utf-8').read() for d in (oa, ob))
            la, lb = ta.split('\n'), tb.split('\n')
            import difflib
            dl = [l for l in difflib.unified_diff(la, lb, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
            rec['diff_lines'] = dl
            rec['diff_non_comment'] = [l for l in dl if not l[1:].lstrip().startswith('#')]
            rec['cmds_token_identical'] = logical(ta) == logical(tb)
            ma, mb = (json.load(open(os.path.join(d, 'deck_meta.json'), encoding='utf-8')) for d in (oa, ob))
            ks = sorted(set(ma) | set(mb))
            rec['meta_changed_keys'] = [k for k in ks if ma.get(k) != mb.get(k) and k not in ('argv', 'generator_sha256', 'deck_sha256', 'deck_bytes')]
            rec['meta_schema'] = (ma.get('schema'), mb.get('schema'))
            rec['meta_registered_new'] = mb.get('registered')
            aa, ab = ma.get('adhesion_rule') or {}, mb.get('adhesion_rule') or {}
            rec['adhesion_rule_changed'] = {k: (aa.get(k), ab.get(k)) for k in sorted(set(aa) | set(ab)) if aa.get(k) != ab.get(k)}
            rec['meta_pairs_identical'] = ma.get('pairs') == mb.get('pairs')
        res[label] = rec
json.dump(res, open(OUTJ, 'w'), ensure_ascii=False, indent=1)
for k, v in res.items():
    if v['rc_new'] != 0 or v['rc_old'] != 0:
        print(f"{k:32s} rc old {v['rc_old']} new {v['rc_new']} · {(v['refused_new'] or '')[:150]}")
        continue
    print(f"{k:32s} diff {len(v['diff_lines'])} lines (non-comment {len(v['diff_non_comment'])}) · cmds identical {v['cmds_token_identical']} · "
          f"meta keys {v['meta_changed_keys']} · schema {v['meta_schema']} · adhesion_rule +{sorted(v['adhesion_rule_changed'])} · "
          f"pairs same {v['meta_pairs_identical']}")
