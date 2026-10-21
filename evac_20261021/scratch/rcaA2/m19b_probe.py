"""M19b probe — side-1 branch of the self sub-edge opposite-point restriction (pa[pb == Xs[j]]).
Asymmetric U: leg 1 top 7.5 · leg 2 top 8.5 → leg-2 touch run longer → side 1.  usage: python3 m19b_probe.py {fixed|mut}"""
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
S3 = load('step3_sigma', WT + '/scripts/step3_sigma.py')
src = open(WT + '/scripts/carbon_junction.py', encoding='utf-8').read()
if mode == 'mut':
    old = '                    m_ = pa[pb == Xs[j]]\n'
    assert src.count(old) == 1
    src = src.replace(old, '                    m_ = pa\n')
td = tempfile.mkdtemp(prefix='m19b_', dir=os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(td, 'carbon_junction.py')
open(p, 'w', encoding='utf-8').write(src)
CJ = load('carbon_junction', p)
import shutil  # noqa: E402
shutil.rmtree(td, ignore_errors=True)
T = load('tcj', WT + '/scripts/test_carbon_junction.py')
T.S3, T.CJ = S3, CJ
P = T.rows([[(1.5, 1.5, 7.5), (1.5, 1.5, 0.5), (2.3, 1.5, 0.5), (2.3, 1.5, 8.5)]])
sid, _ = T.bed(P, (4, 3, 9))
reg = T.registry(sid, P, s_min_um=6.0, L_par_um=0.25)
I, sub = reg['instances'], reg['subedges']
qs = [q for q in range(len(I['fi'])) if I['self'][q]]
print('self', qs, 'Lc', [repr(float(I['Lc'][q])) for q in qs], 'nsub', [int(I['nsub'][q]) for q in qs])
rows_ = [x for x in range(len(sub['inst'])) if I['self'][sub['inst'][x]]]
for x in sorted(rows_, key=lambda x: float(sub['X_j'][x][2]))[:3]:
    print('  sub', x, 'side', int(sub['side'][x]), 'Xi', [repr(float(v)) for v in sub['X_i'][x]], 'Xj', [repr(float(v)) for v in sub['X_j'][x]])
print('expect lowest Xj z', repr(2.75 + 5.35 / 44.0))
