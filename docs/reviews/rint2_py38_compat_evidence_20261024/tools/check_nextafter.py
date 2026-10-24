import sys, math, struct, random
sys.path.insert(0, sys.argv[1] + '/scripts')
import ca_ext_svcf as S
real = math.nextafter
del math.nextafter                      # force the 3.8 fallback branch
try:
    fb = S._nextafter
    rng = random.Random(20261024)
    def bits(u): return struct.unpack('<d', struct.pack('<Q', u))[0]
    edge = [0.0, -0.0, 5e-324, -5e-324, 2.2250738585072014e-308, -2.2250738585072014e-308, 1.0, -1.0, 0.5, 2.0,
            sys.float_info.max, -sys.float_info.max, math.inf, -math.inf, math.nan, 1e-300, 3.0, 0.1]
    vals = edge + [bits(rng.getrandbits(64)) for _ in range(200000)]
    tows = [math.inf, -math.inf, 0.0, -0.0, 1.0, -1.0, math.nan]
    n = bad = 0
    for x in vals:
        for t in tows + [bits(rng.getrandbits(64))]:
            a, b = real(x, t), fb(x, t)
            n += 1
            same = (math.isnan(a) and math.isnan(b)) or struct.pack('<d', a) == struct.pack('<d', b)
            if not same:
                bad += 1
                if bad <= 5: print('MISMATCH', x, t, a, b)
    print(f'compared {n} pairs · mismatches {bad} (bit-exact incl. sign of zero)')
finally:
    math.nextafter = real
