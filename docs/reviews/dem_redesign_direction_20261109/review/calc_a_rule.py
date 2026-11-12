import math
d=0.02; L13=math.log(1.3); L115=math.log(1.15)
def grade_single(qinf,c,p):
    q={n:qinf+c*n**(-p) for n in (12,16,24)}
    d1=q[16]-q[12]; d2=q[24]-q[16]
    a=(abs(d1)<=d and abs(d2)<=d); b=(d1*d2>=0 and abs(d2)<=1.1*abs(d1))
    lo=min(q[24],q[24]+3*d2)-d; hi=max(q[24],q[24]+3*d2)+d
    g='중간'
    if a or b:
        if lo>=L13: g='다름'
        elif lo>=-L115 and hi<=L115: g='같음'
        elif hi<=-L13: g='반대'
    else: g='중간(미수렴)'
    return q,d1,d2,a,b,lo,hi,g
for p,qinf in ((0.1,0.0),(0.3,math.log(1.21)),(0.5,0.0)):
    # choose c so |d2| = 0.02 exactly
    c=0.02/abs(24**(-p)-16**(-p))
    q,d1,d2,a,b,lo,hi,g=grade_single(qinf,c,p)
    print(f"p={p} qinf={qinf:.4f}(R={math.exp(qinf):.3f}) c={c:.4f} q12={q[12]:.4f} q16={q[16]:.4f} q24={q[24]:.4f} d1={d1:.4f} d2={d2:.4f} ratio={abs(d2/d1):.3f} (a)={a} (b)={b} lo={lo:.4f} hi={hi:.4f} -> {g}; contains qinf={lo<=qinf<=hi}; R24={math.exp(q[24]):.3f}")
# Jacobi KE example
m=1; vA=1; N=4; J=0.5
vA2=vA-N*J; others=J
print('Jacobi A+4 KE before',0.5*vA**2,'after',0.5*vA2**2+N*0.5*others**2)
