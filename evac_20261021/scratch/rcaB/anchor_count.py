"""Count T18 mutation anchors in a step3_conv_cert.py / run_contract.py pair (each must occur exactly once)."""
import sys

cc_path, rc_path = sys.argv[1], sys.argv[2]
cc = open(cc_path, encoding='utf-8').read()
rc = open(rc_path, encoding='utf-8').read()
CC_ANCH = ('u1, e1 = _fsum_bound(c * dphi)', '    if _tree:\n        acc = d.copy()', 'elif fe > lim:', '    if _defect_term:\n',
           'hi = (U + e1 + e2 + e3) * (1.0 + 8.0 * _UNIT)', '    if (np.abs(rs - pl) > ',
           "zero_exact = bool(out['I_bot'] == 0.0 and out['I_top'] == 0.0 and out['sigma'] == 0.0)", '    if fw > lim:',
           "jd = target_judge(tb['target_lo'], tb['target_hi'], out['I_bot'])")
RC_ANCH = ("    if jd['pass_d'] is not True:", 'and s == 0.0 and _fin_num(sigma) and sigma == 0.0')
for a in CC_ANCH:
    print(f'cc {cc.count(a)}  {a!r}')
for a in RC_ANCH:
    print(f'rc {rc.count(a)}  {a!r}')
