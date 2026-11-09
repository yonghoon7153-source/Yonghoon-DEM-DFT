"""Small fixed geometry only: actual registry, no mocks and no conductivity solve.

python -I -B -X utf8 reproduce_smin_counterexample.py --repo /path/to/pinned/repo
"""
import argparse, hashlib, json, math, pathlib, sys
import numpy as np

p=argparse.ArgumentParser()
p.add_argument('--repo',type=pathlib.Path,required=True)
p.add_argument('--out',type=pathlib.Path)
a=p.parse_args(); repo=a.repo.resolve()
sys.path.insert(0,str(repo/'scripts'))
import carbon_junction as C
from fibre_segment_raster import segment_cells

P=np.array([[0.9729629131445341,0.5844095225512604,0.225],
            [0.49,0.455,0.225],
            [0.9729629131445341,0.32559047744873965,0.225]])
h=.15; D=.22381254285530133
base=np.zeros((10,10,4),np.uint8)
for u,v in zip(P[:-1],P[1:]):
    ijk=segment_cells(u,v,h);base[tuple(ijk.T)]=3

def run(sid,t):
    sd=np.argwhere(sid==5)
    Q=np.vstack([P,(sd+.5)*h]);ph=np.r_[np.full(3,2),np.full(len(sd),5)]
    fid=np.r_[np.full(3,11),np.arange(22,22+len(sd))]
    kind=np.r_[np.ones(3,int),np.zeros(len(sd),int)]
    return C.cjunc_registry(sid,(0.,0.,0.),h,Q,ph,fid,kind,
       r_f_um=.075,tol_ff_um=D-.15,L_par_um=.3,r_port_um=.3,s_min_um=t)

records=[]
for label in ['V_only','V_plus_SDCP']:
    sid=base.copy()
    if label=='V_plus_SDCP':sid[4,2,2]=5;sid[4,3,2]=5
    regs=[run(sid,t) for t in [0.,D/2,D,.3,math.pi/2*D]]
    rows=[]
    for t,r in zip([0.,D/2,D,.3,math.pi/2*D],regs):
        assert not r['rejections'],r['rejections']
        c=r['census'];assert c['n_self_candidates']==0
        rows.append({'s_min_um':t,**{k:c[k] for k in ['n_self_candidates','n_self_kept','n_unreg_faces','n_self_fused_faces','n_bridging_components','n_sv_faces_cut_rows']},'rejections':r['rejections']})
    assert rows[0]['n_unreg_faces']==3 and rows[3]['n_unreg_faces']==2
    assert rows[0]['n_self_fused_faces']==0 and rows[3]['n_self_fused_faces']==1
    if label=='V_plus_SDCP':
        assert rows[0]['n_sv_faces_cut_rows']==2 and rows[3]['n_sv_faces_cut_rows']==0
    for r in regs[1:3]:
        for key in regs[0]['faces']:
            assert np.array_equal(r['faces'][key],regs[0]['faces'][key]),key
        assert r['census']==regs[0]['census']
    f0,f1=regs[0]['faces'],regs[3]['faces'];changes=[]
    for i in np.flatnonzero(f0['kind']!=f1['kind']):
        owner_a,owner_b=int(f0['pa'][i]),int(f0['pb'][i])
        s,d=C._pos_pair_sd(owner_a,owner_b,regs[0]['positions'],regs[0]['segments'],regs[0]['lo'],h)
        changes.append({'row':int(i),'lin':int(f0['lin'][i]),'axis':int(f0['ax'][i]),'kind0':int(f0['kind'][i]),'kind03':int(f1['kind'][i]),'s_face_um':s,'d_face_um':d})
    records.append({'fixture':label,'vgcf_points_um':P.tolist(),'sid3':np.argwhere(sid==3).tolist(),'sid5':np.argwhere(sid==5).tolist(),'results':rows,'face_changes':changes})

out={'review_pin':'abf0911ebc994167ac50132c78207c6c8d4421f1','scope':'two small synthetic geometries; no mock, no conductivity solver, no real S0 run',
     'python':sys.version,'source_sha256':{n:hashlib.sha256((repo/'scripts'/n).read_bytes()).hexdigest() for n in ['carbon_junction.py','fibre_segment_raster.py']},'D_um':D,'records':records}
txt=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
if a.out:a.out.write_text(txt,encoding='utf-8')
print(txt,end='')
