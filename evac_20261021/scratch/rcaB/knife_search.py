"""Search a knife-edge (lo, hi, G) where the float judge passes but the exact rational bound exceeds tau = 1/10000."""
import math
import random
from fractions import Fraction as Fr

TAU = Fr(1, 10000)
tol = 1e-4
rng = random.Random(20261021)
found = []
for k in range(400000):
    G = 1.0 + rng.random()
    # smallest float hi with (hi - G) > TAU*G exactly
    target = Fr(G) * (1 + TAU)
    hi = float(target)
    while Fr(hi) <= target:
        hi = math.nextafter(hi, math.inf)
    lo = G - (hi - G) * 0.5           # inside: error bound = hi - G (width = 1.5 (hi - G) -> width check would fail)
    lo = G                            # keep lo = G so width = hi - G = error bound
    w = (hi - lo) / G
    e = max(hi - G, G - lo) / G
    float_pass = not (w > tol) and not (e > tol)
    exact_e = (Fr(hi) - Fr(G)) / Fr(G)
    if float_pass and exact_e > TAU:
        found.append((k, G.hex(), hi.hex(), float(exact_e - TAU)))
        if len(found) >= 3:
            break
print(len(found), found)
