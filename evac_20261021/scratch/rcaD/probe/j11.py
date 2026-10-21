import sys, os, json
W = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82'
sys.path.insert(0, os.path.join(W, 'scripts'))
import numpy as np
import test_carbon_junction as T
import step3_sigma as S3
import carbon_junction as CJ
T.S3 = S3
T.CJ = CJ
S3.CONV_CERT = True
n = (5, 5, 2)
polys = [[(0.5, 2.5, 0.5), (4.5, 2.5, 0.5)], [(2.5, 0.5, 1.5), (2.5, 4.5, 1.5)]]
P = T.rows(polys)
sid, _ = T.bed(P, n)
reg = T.registry(sid, P)
r0 = T.solve(sid, T.sig_e(), n, T.plan(reg, 0.0, allow_rj_limits=True))
print('reason', r0.get('reason'), 'sigma', r0.get('sigma_eff'))
print('cert', json.dumps(r0.get('conv_cert'), default=str)[:900])
cj = r0.get('cjunc') or {}
print('cjunc short', cj.get('short'), 'solved', cj.get('solved'), 'reason', cj.get('reason'))
