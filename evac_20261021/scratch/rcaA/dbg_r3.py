import sys
import numpy as np
sys.path.insert(0, 'scripts')
import test_carbon_junction as T
import step3_sigma as S3
import carbon_junction as CJ
T.S3 = S3
T.CJ = CJ
P, sid = T._rc_bed()
r = T._rc_reg(sid, P, 0.0)
inst = r['instances']
print('n inst', len(inst['fi']), 'self', inst['self'])
q = int(np.flatnonzero(inst['self'])[0])
print('s', inst['s'][q], 'Lc', inst['Lc'][q], 'xa', inst['self_xa'][q], 'xb', inst['self_xb'][q])
print('ports', T._pcells(r, q, 'i'), T._pcells(r, q, 'j'), 'tie', inst['tie_i'][q], inst['tie_j'][q])
print('A', [tuple(r['positions']['ijk'][p]) for p in inst['self_A'][q]])
print('B', [tuple(r['positions']['ijk'][p]) for p in inst['self_B'][q]])
print('census ties', r['census'].get('n_port_ties'))
