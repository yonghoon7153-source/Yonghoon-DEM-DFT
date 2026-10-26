"""Independent exact-rational oracle for the pinned directional quotient."""
import json, math, random, struct, sys
from pathlib import Path
from fractions import Fraction
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'repo' / 'scripts'))
import ca_ext_svcf as V
rng = random.Random(20261026)
special = [math.ulp(0.0), math.ulp(0.0)*2, sys.float_info.min, math.nextafter(1.0, 0.0), 1.0, math.nextafter(1.0, math.inf), sys.float_info.max, 0.1, 3.0, 10.0]
pairs = [(a,b) for a in special for b in special]
for _ in range(25000):
    a = struct.unpack('>d', rng.randrange(1,0x7ff0000000000000).to_bytes(8,'big'))[0]
    b = struct.unpack('>d', rng.randrange(1,0x7ff0000000000000).to_bytes(8,'big'))[0]
    pairs.append((a,b))
bad=[]
counts={'pairs':len(pairs),'overflow':0,'subnormal_or_zero':0}
for a,b in pairs:
    exact=Fraction(a)/Fraction(b)
    lo,hi=V._div_dir(a,b,False),V._div_dir(a,b,True)
    if exact > Fraction(sys.float_info.max):
        counts['overflow']+=1
        ok=lo==sys.float_info.max and hi is None
    else:
        ok=Fraction(lo)<=exact<=Fraction(hi)
        lon,hip=math.nextafter(lo,math.inf),math.nextafter(hi,-math.inf)
        ok=ok and (not math.isfinite(lon) or Fraction(lon)>exact) and Fraction(hip)<exact
        if lo < sys.float_info.min: counts['subnormal_or_zero']+=1
    if not ok: bad.append({'a':a,'b':b,'lo':lo,'hi':hi})
print(json.dumps({'oracle':'Fraction exact inequalities and adjacent-float optimality','seed':20261026,'counts':counts,'failures':bad},indent=2,allow_nan=False))
assert not bad
