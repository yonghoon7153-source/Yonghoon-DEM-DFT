import sys, itertools, warnings
warnings.filterwarnings("ignore")
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.interfaces.zsl import ZSLGenerator
from pymatgen.core.surface import SlabGenerator
from ase.io import read
R="/home/user/Yonghoon-DEM-DFT/"
se=AseAtomsAdaptor.get_structure(read(R+"db/structures/comp1_V0_k444.xyz"))
lzo=AseAtomsAdaptor.get_structure(read(R+"db/structures/hyeokju_Li2ZrO3_mp-aaaaagdw.vasp"))
lzo_c=SpacegroupAnalyzer(lzo,symprec=0.05).get_conventional_standard_structure()
print("LZO conv", lzo_c.composition.reduced_formula, len(lzo_c), np.round(lzo_c.lattice.abc,3), np.round(lzo_c.lattice.angles,2), SpacegroupAnalyzer(lzo,symprec=0.05).get_space_group_symbol())
print("SE", len(se), np.round(se.lattice.abc,3), "sg", SpacegroupAnalyzer(se,symprec=0.05).get_space_group_symbol())
rho_se=len(se)/se.volume; rho_lzo=len(lzo_c)/lzo_c.volume
zsl=ZSLGenerator(max_area_ratio_tol=0.09, max_area=520, max_length_tol=0.03, max_angle_tol=0.01)
def plane_vecs(struct, hkl):
    sg=SlabGenerator(struct, hkl, min_slab_size=5, min_vacuum_size=5, in_unit_planes=True, primitive=False, reorient_lattice=True)
    sl=sg.get_slab()
    return sl.lattice.matrix[:2], sl
res=[]
se_hkls=[(0,0,1),(1,1,0),(1,1,1)]
print("scanning")
lzo_hkls=sorted({tuple(int(x) for x in h) for h in itertools.product(range(-1,2),repeat=3) if any(h)})
# keep one of ±hkl
seen=set(); uniq=[]
for h in lzo_hkls:
    if tuple(-x for x in h) in seen: continue
    seen.add(h); uniq.append(h)
for sh in se_hkls:
    sv,_=plane_vecs(se, sh)
    for fh in uniq:
        try:
            fv,_=plane_vecs(lzo_c, fh)
        except Exception as e:
            continue
        for m in zsl(fv, sv):   # film vectors, substrate vectors
            A=m.match_area
            fs=np.array(m.film_sl_vectors); ss=np.array(m.substrate_sl_vectors)
            lf=np.linalg.norm(fs,axis=1); ls=np.linalg.norm(ss,axis=1)
            strain=np.abs(lf/ls-1).max()*100
            ang_f=np.degrees(np.arccos(np.dot(fs[0],fs[1])/lf.prod())); ang_s=np.degrees(np.arccos(np.dot(ss[0],ss[1])/ls.prod()))
            n10=A*(rho_se*10+rho_lzo*10)
            res.append((A, sh, fh, round(strain,2), np.round(ls,2), round(ang_s,1), round(ang_f-ang_s,2), int(n10)))
res.sort(key=lambda r:(r[0], r[3]))
seenk=set()
print("area_A2 | SE hkl | LZO hkl | max len strain % | SE vec lengths | SE angle | d_angle | N(10A+10A)")
for r in res:
    k=(round(r[0],0), r[1], r[2])
    if k in seenk: continue
    seenk.add(k)
    if r[0]<=520: print(r)
