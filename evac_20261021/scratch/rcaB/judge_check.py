"""Light check of the exact target_judge on the knife triples + inner control (scratch tree module)."""
import sys
from fractions import Fraction as Fr

sys.path.insert(0, sys.argv[1])
import step3_conv_cert as CC  # noqa: E402

KNIFE = ((float.fromhex('0x1.fd70a3d70875fp+0'), float.fromhex('0x1.fd7dae8186635p+0')),
         (float.fromhex('0x1.fd70a3d70604fp+0'), float.fromhex('0x1.fd7dae8183f24p+0')),
         (float.fromhex('0x1.fd70a3d70393fp+0'), float.fromhex('0x1.fd7dae8181813p+0')))
tau = Fr(1, 10 ** 4)
for G, hi in KNIFE:
    j = CC.target_judge(G, hi, G)
    ex = (Fr(hi) - Fr(G)) / Fr(G)
    print('knife', j['pass_d'], float(ex - tau), j['target_why'])
    # the same triple with hi one ulp lower must pass (exactly at or below tau)
    import math
    hi2 = math.nextafter(hi, 0.0)
    j2 = CC.target_judge(G, hi2, G)
    print('  one ulp lower', j2['pass_d'], float((Fr(hi2) - Fr(G)) / Fr(G) - tau))
print('inner', CC.target_judge(1.0, 1.0 + 2.0 ** -20, 1.0)['pass_d'])
print('bad tol', CC.target_judge(1.0, 1.0, 1.0, tol=float('nan'))['pass_d'], CC.target_judge(1.0, 1.0, 1.0, tol=-1e-4)['pass_d'])
print('exact', CC.target_judge(0.5, 0.5, 0.5))
