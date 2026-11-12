import math
d=0.02; L13=math.log(1.3); L115=math.log(1.15)
def grade(qinf,c,p,sign):
    q={n: qinf + sign*c*n**(-p) for n in (12,16,24)}
    d1=q[16]-q[12]; d2=q[24]-q[16]
    a = abs(d1)<=d and abs(d2)<=d
    b = d1*d2>=0 and abs(d2)<=1.1*abs(d1)
    lo=min(q[24],q[24]+3*d2)-d; hi=max(q[24],q[24]+3*d2)+d
    if lo>=L13: g='다름'
    elif lo>=-L115 and hi<=L115 and lo>=-L13 and hi<=L13: g='같음'
    elif hi<=-L13: g='반대'
    else: g='중간'
    return dict(q12=round(q[12],4),q16=round(q[16],4),q24=round(q[24],4),d1=round(d1,4),d2=round(d2,4),a=a,b=b,lo=round(lo,4),hi=round(hi,4),R24=round(math.exp(q[24]),3),Rinf=round(math.exp(qinf),3),grade=g)
for p in (0.1,0.3):
    # choose c so |d2| = 0.02 exactly
    c = 0.02/abs(24**(-p)-16**(-p))
    print('p',p,'c',round(c,4))
    print(' from above, qinf=0      ', grade(0.0,c,p,+1))
    print(' from above, qinf=ln1.21 ', grade(math.log(1.21),c,p,+1))
    print(' from below, qinf=ln1.5  ', grade(math.log(1.5),c,p,-1))
# Heckel TD-free ratio from LE25 read values
e100=math.exp(-1.24); e300=math.exp(-1.90)
print('LE25 eps100,eps300',round(e100,4),round(e300,4),'D300/D100',round((1-e300)/(1-e100),4))
# 1.64-basis slope under reading (a) (printed on 1.86 basis)
D100=(1-e100)*1.860/1.64; D300=(1-e300)*1.860/1.64
print('(a) on 1.64 basis eps',round(1-D100,4),round(1-D300,4),'slope e-4',round((-math.log(1-D300)+math.log(1-D100))/200*1e4,1))
# BH00 CM multi-body example
import numpy as np
v={'A':np.array([0.,0.]),'B':np.array([-3.,0.]),'C':np.array([-3.,0.])}
n={'A':np.array([1.,0.]),'B':np.array([0.,1.]),'C':np.array([0.,-1.])}
vcm=sum(v.values())/3
KE0=sum(0.5*x@x for x in v.values()); P0=sum(v.values())
v2={}
for k in v:
    u=v[k]-vcm
    v2[k]= v[k]-(u@n[k])*n[k] if u@n[k]>0 else v[k]
KE1=sum(0.5*x@x for x in v2.values()); P1=sum(v2.values())
print('BH00-CM 3body: vcm',vcm,'KE',KE0,'->',KE1,'P',P0,'->',P1)
