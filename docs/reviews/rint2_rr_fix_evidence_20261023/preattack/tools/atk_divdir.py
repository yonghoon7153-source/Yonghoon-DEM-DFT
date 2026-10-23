"""Fuzz ca_ext_svcf._div_dir (directed rounding of a/b) + show the M7 survivor's unsafe effect on a real record."""
import json, math, os, random, sys
from fractions import Fraction as F
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import ca_ext_svcf as SV

random.seed(5)
bad = []
n = 0
specials = [5e-324, 1e-320, 2.2250738585072014e-308, 1e-300, 0.1, 1.0, 3.0, 1e300, 1.7976931348623157e308]
pairs = [(a, b) for a in specials for b in specials]
for _ in range(20000):
    a = math.ldexp(random.random() + 0.5, random.randint(-1074, 1023))
    b = math.ldexp(random.random() + 0.5, random.randint(-1074, 1023))
    pairs.append((a, b))
for a, b in pairs:
    if not (a > 0 and b > 0 and math.isfinite(a) and math.isfinite(b)):
        continue
    n += 1
    q = F(a) / F(b)
    lo, hi = SV._div_dir(a, b, False), SV._div_dir(a, b, True)
    ok_lo = lo is not None and F(lo) <= q and (lo == sys.float_info.max or F(math.nextafter(lo, math.inf)) > q)
    ok_hi = (hi is None and q > F(sys.float_info.max)) or (hi is not None and F(hi) >= q and F(math.nextafter(hi, -math.inf)) < q)
    if not (ok_lo and ok_hi):
        bad.append((a, b, lo, hi))
print(json.dumps({'checked': n, 'violations': len(bad), 'examples': bad[:3]}))
