import sys, json, numpy as np
from ase.io import read
from ase.geometry import get_distances
D='db/raw/wad_se_pairs_uma_2026_10_01/relax'
out={}
for term in ('s_outer','li_outer'):
    for reg in ('A','B'):
        a=read(f'{D}/P1_{term}/{reg}/relaxed.extxyz')
        sym=np.array(a.get_chemical_symbols()); z=a.positions[:,2]
        ag=np.where(sym=='Ag')[0]; se=np.where(sym!='Ag')[0]
        ag_low=z[ag].min(); se_top=z[se].max()
        above = z[ag].mean()>z[se].mean()
        # distances SE->Ag with MIC
        _,dm=get_distances(a.positions[se],a.positions[ag],cell=a.cell,pbc=a.pbc)
        dmin=dm.min(axis=1)
        # P neighbours of S (PS4 membership)
        P=np.where(sym=='P')[0]; S=np.where(sym=='S')[0]
        _,dsp=get_distances(a.positions[S],a.positions[P],cell=a.cell,pbc=a.pbc)
        s_in_ps4={int(S[i]):bool((dsp[i]<2.5).any()) for i in range(len(S))}
        area=float(np.linalg.norm(np.cross(a.cell[0],a.cell[1])))
        cnt={}
        for k,i in enumerate(se):
            el=sym[i]; d=dmin[k]
            cut={'S':2.9,'Li':3.0,'Cl':3.0,'P':3.2}[el]
            if d<=cut:
                key=el if el!='S' else ('S_PS4' if s_in_ps4[int(i)] else 'S_free')
                cnt[key]=cnt.get(key,0)+1
        out[f'{term}_{reg}']={'n_atoms':len(a),'ag_above':bool(above),'area_A2':round(area,2),'contacts':cnt,
            'gap_A':round(float(ag_low-se_top) if above else float(z[se].min()-z[ag].max()),3)}
print(json.dumps(out,indent=1))
json.dump(out,open(sys.argv[1],'w'),indent=1)
