"""Construct knife-edge triples: G = m 2^-52 (m = 9999 mod 10000, G in [1.91, 1.9998)), hi = smallest float > G (1 + 1/10000)."""
import math
from fractions import Fraction as Fr

TAU = Fr(1, 10000)
tol = 1e-4
out = []
m0 = int(1.99 * 2 ** 52)
m = m0 - ((m0 - 9999) % 10000)
for step in range(200):
    mm = m - step * 10000
    G = mm * 2.0 ** -52
    target = Fr(G) * (1 + TAU)
    hi = float(target)
    while Fr(hi) <= target:
        hi = math.nextafter(hi, math.inf)
    lo = G
    w = (hi - lo) / G
    e = max(hi - G, G - lo) / G
    float_pass = not (w > tol) and not (e > tol)
    exact_e = (Fr(hi) - Fr(G)) / Fr(G)
    if float_pass and exact_e > TAU:
        out.append((G.hex(), hi.hex(), float(exact_e - TAU), repr(G), repr(hi)))
print(len(out))
for r in out[:3]:
    print(r)
