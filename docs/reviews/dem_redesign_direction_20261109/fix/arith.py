import math
L13=math.log(1.3); L115=math.log(1.15)
def r(p):  # d2/d1 for n=12,16,24 single term
    return (1-(2/3)**p)/((4/3)**p-1)
def bis(f,lo,hi,target):
    for _ in range(200):
        m=(lo+hi)/2
        if (f(m)-target)*(f(lo)-target)<=0: hi=m
        else: lo=m
    return (lo+hi)/2
p11=bis(r,0.01,5,1.1); p05=bis(r,0.01,10,0.5)
print('r(p): p0->',round(math.log(1.5)/math.log(4/3),4),' p@1.1=',round(p11,4),' p@0.5=',round(p05,4))
for p in (0.5,0.72,1,2,3,3.1,4): print(' p',p,'r',round(r(p),4),'resid factor 1/(1.5^p-1)',round(1/(1.5**p-1),3))
# new rule
def newgrade(qs,d=0.02,lo_r=0.5,hi_r=1.1):
    q12,q16,q24=qs; d1=q16-q12; d2=q24-q16
    ok = d1*d2>0 and lo_r*abs(d1)<=abs(d2)<=hi_r*abs(d1)
    if not ok: return '중간(미수렴)',d1,d2,None
    lo=min(q24,q24+3*d2)-d; hi=max(q24,q24+3*d2)+d
    if lo>=L13: g='다름'
    elif lo>=-L115 and hi<=L115: g='같음'
    elif hi<=-L13: g='반대'
    else: g='중간'
    return g,d1,d2,(lo,hi)
# reviewer counterexamples
for p,qinf,sign in ((0.1,0.0,1),(0.1,math.log(1.5),-1),(0.3,0.0,1),(0.3,math.log(1.5),-1)):
    c=0.02/abs(24**(-p)-16**(-p))
    qs=[qinf+sign*c*n**(-p) for n in (12,16,24)]
    print('P1-2 ex p',p,'qinf',round(qinf,4),'q',[round(x,4) for x in qs],'->',newgrade(qs)[0])
# verdict counterexample
qs=[math.log(1.10+3.36/n) for n in (12,16,24)]
g,d1,d2,iv=newgrade(qs); print('DRD-01 ex',[round(x,4) for x in qs],round(d1,4),round(d2,4),round(d2/d1,3),g,[round(x,4) for x in iv])
# memo two-term 3/n-24/n^2
qs=[3/n-24/n**2 for n in (12,16,24)]; print('memo two-term',[round(x,4) for x in qs],newgrade(qs)[0])
# two-term fooling example 4/n-72/n^2
f=lambda n:4/n-72/n**2
qs=[f(n) for n in (8,12,16,24)]; print('two-term fool q8..q24',[round(x,4) for x in qs])
g,d1,d2,iv=newgrade(qs[1:]); print('  ratio',round(d2/d1,3),'grade(q at qinf=0 offset)',g,'interval rel q24',round(iv[0]-qs[3],4),round(iv[1]-qs[3],4),'limit rel q24',round(-qs[3],4))
# shift so that it flips: qinf=0.24 -> q24=qinf+f(24)
qinf=0.24; qq=[qinf+f(n) for n in (12,16,24)]; g,d1,d2,iv=newgrade(qq); print('  qinf 0.24 -> q24',round(qq[2],4),'interval',[round(x,4) for x in iv],'grade',g,'truth R',round(math.exp(qinf),3))
