import numpy as np
c,s=np.cos(np.radians(120)),np.sin(np.radians(120))
v={'A':np.array([0.,0.]),'B':np.array([-1.,0.]),'C':np.array([-1.,0.])}
n={'A':np.array([1.,0.]),'B':np.array([c,s]),'C':np.array([c,-s])}
m={'A':1.,'B':1.,'C':1.}
vcm=sum(m[k]*v[k] for k in v)/sum(m.values())
KE0=sum(0.5*m[k]*v[k]@v[k] for k in v); P0=sum(m[k]*v[k] for k in v)
v2={}
for k in v:
    u=v[k]-vcm; un=u@n[k]
    v2[k]= v[k]-un*n[k] if un>0 else v[k]
KE1=sum(0.5*m[k]*v2[k]@v2[k] for k in v); P1=sum(m[k]*v2[k] for k in v)
print('vcm',vcm.round(4),'KE',round(KE0,4),'->',round(KE1,4),'P',P0.round(4),'->',P1.round(4))
for k in v2: print(k, v2[k].round(4))
# friction direction example
v1=np.array([1.,0.5]); w=np.array([-1.,-0.5]); J1=np.array([-1.,+0.5]); 
a=v1+J1; b=w-J1
print('fric-wrong: KE',0.5*(v1@v1+w@w),'->',0.5*(a@a+b@b),'P',v1+w,'->',a+b,'|Jt|/|Jn|',abs(J1[1])/abs(J1[0]))
