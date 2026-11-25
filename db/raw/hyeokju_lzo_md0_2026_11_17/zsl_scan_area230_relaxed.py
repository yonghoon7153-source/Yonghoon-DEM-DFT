import warnings, itertools; warnings.filterwarnings("ignore")
import numpy as np
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.interfaces.zsl import ZSLGenerator
from pymatgen.core.surface import SlabGenerator
from ase.io import read
R="/home/user/Yonghoon-DEM-DFT/"
se=AseAtomsAdaptor.get_structure(read(R+"db/structures/comp1_V0_k444.xyz"))
lzo=AseAtomsAdaptor.get_structure(read(R+"db/structures/hyeokju_Li2ZrO3_mp-aaaaagdw.vasp"))
lzo_c=SpacegroupAnalyzer(lzo,symprec=0.05).get_conventional_standard_structure()
rho_se=len(se)/se.volume; rho_lzo=len(lzo_c)/lzo_c.volume
def pv(st,h):
    sl=SlabGenerator(st,h,min_slab_size=5,min_vacuum_size=5,in_unit_planes=True,primitive=False,reorient_lattice=True).get_slab()
    return sl.lattice.matrix[:2]
uniq=[];seen=set()
for h in itertools.product(range(-1,2),repeat=3):
    if not any(h) or tuple(-x for x in h) in seen: continue
    seen.add(h); uniq.append(h)
svs={sh:pv(se,sh) for sh in [(0,0,1),(1,1,0),(1,1,1)]}
fvs={}
for fh in uniq:
    try: fvs[fh]=pv(lzo_c,fh)
    except Exception: pass
for tol,atol in [(0.03,0.03),(0.05,0.01),(0.05,0.03),(0.06,0.03)]:
    z=ZSLGenerator(max_area_ratio_tol=0.09,max_area=230,max_length_tol=tol,max_angle_tol=atol)
    best=[]
    for sh,sv in svs.items():
        for fh,fv in fvs.items():
            for m in z(fv,sv):
                fs=np.array(m.film_sl_vectors); ss=np.array(m.substrate_sl_vectors)
                lf=np.linalg.norm(fs,axis=1); ls=np.linalg.norm(ss,axis=1)
                st=np.abs(lf/ls-1).max()*100
                af=np.degrees(np.arccos(np.dot(fs[0],fs[1])/lf.prod())); as_=np.degrees(np.arccos(np.dot(ss[0],ss[1])/ls.prod()))
                best.append((round(m.match_area,1),sh,fh,round(st,2),round(af-as_,2),np.round(ls,2).tolist(),int(m.match_area*(rho_se*10+rho_lzo*8))))
    best.sort()
    print(f"== length tol {tol*100:.0f}% · angle tol {atol*100:.0f}% · area<=230: {len(best)} matches")
    shown=set()
    for b in best:
        k=(b[0],b[1])
        if k in shown: continue
        shown.add(k); print("  ",b)
        if len(shown)>=5: break
