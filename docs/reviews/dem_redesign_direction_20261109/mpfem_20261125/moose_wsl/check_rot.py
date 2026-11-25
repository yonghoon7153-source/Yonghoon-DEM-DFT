# Reads rot_test_out.csv and prints R1 / R2 (criteria fixed before the run).
import csv, math, sys
SY = 4e5
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
def at(t):
    for r in rows:
        if abs(float(r['time']) - t) < 1e-9:
            return {k: float(v) for k, v in r.items()}
    raise SystemExit('no row at t=%s' % t)
a, b = at(100.0), at(400.0)
th = math.radians(30.0)
c, s = math.cos(th), math.sin(th)
bxx = c * c * b['sxx'] + s * s * b['syy'] + 2 * c * s * b['sxy']
byy = s * s * b['sxx'] + c * c * b['syy'] - 2 * c * s * b['sxy']
bxy = -c * s * b['sxx'] + c * s * b['syy'] + (c * c - s * s) * b['sxy']
diff = max(abs(bxx - a['sxx']), abs(byy - a['syy']), abs(bxy - a['sxy']), abs(b['szz'] - a['szz']))
r1 = diff <= 1e-3 * SY
r2 = abs(a['svm'] / SY - 1.0) <= 0.02
print('ROT_TEST t100 sxx=%.6g syy=%.6g szz=%.6g sxy=%.6g svm/sy=%.6f' % (a['sxx'], a['syy'], a['szz'], a['sxy'], a['svm'] / SY))
print('ROT_TEST t400 sxx=%.6g syy=%.6g szz=%.6g sxy=%.6g' % (b['sxx'], b['syy'], b['szz'], b['sxy']))
print('ROT_TEST diff/sy=%.3e  R1=%s  R2=%s  rows=%d' % (diff / SY, 'PASS' if r1 else 'FAIL', 'PASS' if r2 else 'FAIL', len(rows)))
