#!/usr/bin/env python3
"""Both R/g2/atom_S0 and in/atom_S0 written with header step S0 - 1000 — restore verdict + G2 status (kit given as argv[1])."""
import json
import os
import sys
import tempfile

K = os.path.abspath(sys.argv[1])
sys.path.insert(0, K)
import ul_lib  # noqa: E402
import ul_reader as U  # noqa: E402

P = ul_lib.load_params()
B = U.B73
s0 = P['beds'][B]['s0']
with tempfile.TemporaryDirectory() as root:
    J = U._mk_rj(root, B, P)
    hv = os.path.join(root, 'hv.json')
    U._w(hv, json.dumps({'schema': 'ps45_unload_history_verdict_v1', 'exit_code': 0, 'rows': {f'H{i}': {'status': 'PASS'} for i in range(6)},
                         'info': {'syn': {'status': 'PASS', 'plate_fn_sign': -1}, 'force_timing': 'PASS'}}))
    for p in (os.path.join(root, B, 'in', f'atom_{s0}.liggghts'), os.path.join(J, 'R', 'g2', f'atom_{s0}.liggghts')):
        d = ul_lib.read_dump(p, 'custom')
        ul_lib.write_custom(p, s0 - 1000, d['cols'], d['rows'], fmt=lambda x: f'{x:g}')
    r = U.restore_verdict(root, B, 'RJ', hv, P)
    print(json.dumps({'status': r['status'], 'G2': r['checks']['G2'].get('status'), 'G2_why': r['checks']['G2'].get('why', [])[:2],
                      'pre_post': r['checks']['pre_post']}, ensure_ascii=False, default=str))
