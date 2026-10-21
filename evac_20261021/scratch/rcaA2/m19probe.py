"""M19 probe — does the self sub-edge opposite-point restriction (pb[pa == Xs[j]]) change X_j on a designed fixture?
usage: python3 m19probe.py {fixed|mut} [s_min]"""
import importlib.util
import os
import sys
import tempfile

import numpy as np

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
sys.path.insert(0, WT + '/scripts')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


mode = sys.argv[1]
smin = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
S3 = load('step3_sigma', WT + '/scripts/step3_sigma.py')
src = open(WT + '/scripts/carbon_junction.py', encoding='utf-8').read()
if mode == 'mut':
    old = '                    m_ = pb[pa == Xs[j]]\n'
    assert src.count(old) == 1
    src = src.replace(old, '                    m_ = pb\n')
td = tempfile.mkdtemp(prefix='m19_')
p = os.path.join(td, 'carbon_junction.py')
open(p, 'w', encoding='utf-8').write(src)
CJ = load('carbon_junction', p)
T = load('tcj', WT + '/scripts/test_carbon_junction.py')
T.S3, T.CJ = S3, CJ

fixtures = {
    # U: leg 1 down at x 1.5 · bottom across · leg 2 up at x 2.3 (gap 0.8 < D 1)
    'U08': ([[(1.5, 1.5, 8.5), (1.5, 1.5, 0.5), (2.3, 1.5, 0.5), (2.3, 1.5, 8.5)]], (4, 3, 9)),
    # U with leg 2 slanted toward leg 1 at the bottom
    'U08s': ([[(1.5, 1.5, 8.5), (1.5, 1.5, 0.5), (2.2, 1.5, 0.5), (2.4, 1.5, 8.5)]], (4, 3, 9)),
}
for nm, (poly, n) in fixtures.items():
    P = T.rows(poly)
    sid, _ = T.bed(P, n)
    reg = T.registry(sid, P, s_min_um=smin, L_par_um=float(os.environ.get("LPAR", "2.0")))
    I = reg['instances']
    sub = reg['subedges']
    qs = [q for q in range(len(I['fi'])) if I['self'][q]]
    print(nm, 'self instances', qs, 'Lc', [round(float(I['Lc'][q]), 6) for q in qs], 's', [round(float(I['s'][q]), 6) for q in qs],
          'nsub', [int(I['nsub'][q]) for q in qs])
    for x in range(len(sub['inst'])):
        if I['self'][sub['inst'][x]]:
            print('   sub', x, 'side', int(sub['side'][x]), 'Xi', np.round(sub['X_i'][x], 6).tolist(), 'Xj', np.round(sub['X_j'][x], 6).tolist(),
                  'ports', int(sub['port_i'][x]), int(sub['port_j'][x]), bool(sub['realized'][x]))
