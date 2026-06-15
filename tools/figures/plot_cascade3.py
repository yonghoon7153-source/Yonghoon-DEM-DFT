import json,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
triv=json.load(open('db/properties/doping_cascade_trivalent_M3.json'))['champions']
g13={'Al2O3','Ga2O3','In2O3'}; X={'x002':0.02,'x005':0.05,'x010':0.10}
fig,ax=plt.subplots(1,3,figsize=(17,5))
def series(d,key):
    xs=[];ys=[]
    for xk,xv in X.items():
        e=triv[d].get(xk)
        if isinstance(e,dict) and key in e and not e.get('_FLAG'): xs.append(xv); ys.append(e[key])
    return xs,ys
dops=sorted(triv,key=lambda d:triv[d]['r_A'])
import matplotlib.cm as cm
colors=cm.tab10(np.linspace(0,1,len(dops)))
for (key,ylab,ttl),a in zip([('de_post_anneal_eV_atom','formation dE (eV/atom)','(a) stability vs doping level'),
                              ('E_young_GPa','E_VRH (GPa)','(b) modulus vs doping level'),
                              ('score_combined','combined score','(c) cascade score vs doping level')],ax):
    for d,c in zip(dops,colors):
        xs,ys=series(d,key)
        if xs: a.plot(xs,ys,'o-',c=c,ms=6,lw=1.5,label=d.replace('2O3',''))
    a.set_xlabel('dopant fraction x'); a.set_ylabel(ylab); a.set_title(ttl); a.grid(alpha=.3); a.set_xticks([0.02,0.05,0.10])
ax[0].legend(fontsize=7,ncol=2,loc='upper right')
plt.suptitle('M3+ cascade: concentration trends (x=0.02/0.05/0.10, UMA)',fontsize=12,y=1.02)
plt.tight_layout(); plt.savefig('docs/figures/cascade/cascade_conc_trends.png',dpi=150,bbox_inches='tight')
print('saved -> cascade_conc_trends.png')
