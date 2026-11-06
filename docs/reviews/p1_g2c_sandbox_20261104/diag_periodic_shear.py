import sys, math, pathlib
sys.path.insert(0, sys.argv[1]); import compare as C
O = pathlib.Path(sys.argv[2]); N = 40000
A = C.read_local(O/'A/post'/f'c_{N}.txt'); B = C.read_local(O/'B/post'/f'c_{N}.txt'); Cc = C.read_local(O/'C/post'/f'c_{N}.txt')
def per(r): return int(r[0][8]) != 0
def fdiff(x, k): return any(A[k][0][c] != x[k][0][c] for c in range(9, 18))
ks = sorted(A)
nper = sum(per(A[k]) for k in ks)
cd = [k for k in ks if fdiff(Cc, k)]
print('pairs', len(ks), 'periodic-flag pairs', nper, '| C force-differ', len(cd), 'of which periodic', sum(per(A[k]) for k in cd), '| periodic pairs not differing in C', sum(1 for k in ks if per(A[k]) and k not in set(cd)))
def nrm(v): return math.sqrt(sum(t*t for t in v))
def sn(r):
    v = r[0]; d = [v[3]-v[0], v[4]-v[1], v[5]-v[2]]; L = nrm(d); n = [t/L for t in d]; s = v[22:25]; m = nrm(s)
    return abs(sum(s[i]*n[i] for i in range(3)))/m if m > 0 else 0.0
np_ = [k for k in ks if not per(A[k])]
mA = max(sn(A[k]) for k in np_); mB = max(sn(B[k]) for k in np_)
import statistics as st
print('non-periodic pairs: |shear.n|/|shear| max A', '%.2e' % mA, 'B', '%.2e' % mB, 'median B', '%.2e' % st.median(sn(B[k]) for k in np_))
