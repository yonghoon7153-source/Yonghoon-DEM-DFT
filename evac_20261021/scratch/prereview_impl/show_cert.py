import json
import os
D = os.path.dirname(os.path.abspath(__file__))
for e in ('default', 'Haswell'):
    d = json.load(open(os.path.join(D, f'probe_cert_codex_{e}.json')))
    print(e, d['threadpool'])
    for k in ('main', 'small', 'connected'):
        x = d[k]
        print(' ', k, {kk: x[kk] for kk in ('rel_err', 'pass_a', 'pass_b', 'pass_c', 'pass_d', 'ok', 'status', 'true_in_bracket',
                                           'err_bound_rel', 'imbalance', 'why')})
    print('  warm', {kk: d['warm_candidate'][kk] for kk in ('posted_G', 'pass_d', 'ok', 'status', 'lo', 'hi', 'why')})
    print('  zero', d['valid_zero'])
