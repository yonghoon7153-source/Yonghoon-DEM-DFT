import itertools, math
from collections import Counter
D,S,M,O,X = '다름','같음','중간','반대','버림'
def point_grade(R):            # R = per-packing ratios (all reached, not noise)
    g = math.exp(sum(math.log(r) for r in R)/len(R))
    labs=[]
    if g >= 1.3 and all(r >= 1.15 for r in R): labs.append(D)
    if 0.87 <= g <= 1.15 and all(0.77 <= r <= 1.3 for r in R): labs.append(S)
    if g <= 0.77 and all(r <= 0.87 for r in R): labs.append(O)
    return labs or [M]
def test_grade(pts):           # decision list as written; X = dropped point
    pts=[p for p in pts if p!=X]
    if not pts: return M
    if O in pts: return O
    if pts[0]==D: return D
    if all(p==S for p in pts): return S
    return M
def resolve(g12,g16,g24):
    if g12==g16: return g12
    return g16 if g16==g24 else M
def merge(a,b):
    if O in (a,b): return O
    if D in (a,b): return D
    if a==S and b==S: return S
    return M
TAB={(D,'in'):'나',(S,'in'):'가',(M,'in'):'마',(O,'in'):'라'}
def branch(tech,G,F,A):
    if tech: return '라'
    b = TAB[(G,F)] if F=='in' else '라'
    if b in ('가','마'):
        if A=='부족': return '나'
        if A=='반대': return '라'
        if A=='중간': return '마'
    return b
# 1) point-level grade uniqueness on a dense grid incl. band edges
edges=[0.5,0.7,1/1.3,0.77,0.8,0.86,1/1.15,0.87,0.9,1.0,1.1,1.15,1.2,1.29,1.3,1.31,1.5,2.0,5.0]
multi=0; cnt=Counter()
for R in itertools.product(edges,repeat=3):
    labs=point_grade(R); cnt[len(labs)]+=1
    if len(labs)!=1: multi+=1
print('point grade: triples',sum(cnt.values()),'labels-per-triple',dict(cnt))
# symmetry probe: grade(R) vs grade(1/R) should mirror D<->O, S<->S, M<->M
mir={D:O,O:D,S:S,M:M}; asym=[]
for R in itertools.product(edges,repeat=3):
    a=point_grade(R)[0]; b=point_grade(tuple(1/r for r in R))[0]
    if mir[a]!=b: asym.append((R,a,b))
print('reciprocal-asymmetric triples:',len(asym)); 
for R,a,b in asym[:6]: print('  ',tuple(round(r,4) for r in R),a,'| 1/R ->',b)
# 2) test-level enumeration: 3a 3 points, 3b-k1 2 points, 5 states each, x resolution
st=[D,S,M,O,X]; tc=Counter()
for pts in itertools.product(st,repeat=3): tc[test_grade(list(pts))]+=1
print('3a test grade over 5^3 point combos:',dict(tc))
# 3) top level: tech x G inputs x F x A
bc=Counter(); n=0
for ta,tb in itertools.product([D,S,M,O],repeat=2):
  for F in ['in','out']:
    for A in ['부족','충분','반대','중간']:
      for tech in [False,True]:
        n+=1; bc[branch(tech,merge(ta,tb),F,A)]+=1
print('top-level combos',n,'branches',dict(bc))
# 4) resolution: 4^3 grade triples -> exactly one
rc=Counter(resolve(*t) for t in itertools.product([D,S,M,O],repeat=3)); print('resolution 64 ->',dict(rc))
# 5) counterexamples
print('CE-A 3a (0.84 같음, 0.90 다름, 0.95 다름):', test_grade([S,D,D]))
print('CE-B 3a (0.84 다름, 0.90 같음, 0.95 같음):', test_grade([D,S,S]))
print('CE-A grades:', point_grade((1.0,1.05,1.1)), point_grade((1.5,1.6,1.7)), point_grade((1.9,2.0,2.1)))
print('noisy-F (1.8,1.8,1.1):', point_grade((1.8,1.8,1.1)), 'gm', round((1.8*1.8*1.1)**(1/3),3))
print('edge 1.15 vs 1/1.15:', point_grade((1.15,1.15,1.15)), point_grade((1/1.15,)*3))
print('edge 1.3 vs 1/1.3:', point_grade((1.3,)*3), point_grade((1/1.3,)*3), ' 0.7695 ->',point_grade((0.7695,)*3),' 1/0.7695=',round(1/0.7695,4),'->',point_grade((1/0.7695,)*3))
