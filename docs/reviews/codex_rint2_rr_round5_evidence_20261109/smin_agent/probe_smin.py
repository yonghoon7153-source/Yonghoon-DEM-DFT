"""Independent static/small-synthetic review. No solver, S0 or research run."""
import argparse, hashlib, json, math, pathlib, sys
import numpy as np

ap=argparse.ArgumentParser()
ap.add_argument('--repo', type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent.parent/'package'/'repo')
ap.add_argument('--out', type=pathlib.Path, default=pathlib.Path(__file__).with_name('probe_smin.json'))
a=ap.parse_args(); repo=a.repo.resolve()
sys.path.insert(0,str(repo/'scripts'))
import carbon_junction as C
from fibre_segment_raster import segment_cells

def clean(x):
    if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [clean(v) for v in x]
    if isinstance(x,np.ndarray): return x.tolist()
    if isinstance(x,np.generic): return x.item()
    return x
def readbytes(p):
    if sys.platform=='win32': p=pathlib.Path('\\\\?\\'+str(p.resolve()))
    return p.read_bytes()
raw=readbytes(repo/'docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/s0_stage1_kit_SBE_vgcf100.json')
j=json.loads(raw); jc=j['junction_census']; ce=jc['census']; lc=jc['long_contacts']
D=2*j['thresholds_used']['r_f_um']+j['thresholds_used']['tol_ff_um']; sm=math.pi/2*D
result={'pin':'abf0911ebc994167ac50132c78207c6c8d4421f1','python':sys.version,'source_sha256':{n:hashlib.sha256(readbytes(repo/'scripts'/n)).hexdigest() for n in ['carbon_junction.py','fibre_segment_raster.py']},
 'raw_json':{'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'stage':j['stage'],'code':j['code'],'thresholds_used':j['thresholds_used'],'threshold_inputs':j['threshold_inputs'],
 'census_relevant':{k:v for k,v in ce.items() if any(s in k for s in ['self','revisit','unreg'])},'self_candidates_len':len(jc['self_candidates']),'long_contacts_len':len(lc),'long_first':lc[:1],
 'revisit':jc['revisit'],'declared_n_instances':jc['n_instances'],'declared_n_long_self':jc['n_long_self']},
 'arithmetic':{'D_um':D,'half_pi_D_um':sm,'rprime_Ohm_per_um':1e-4/(1e4*math.pi*(.075e-4)**2),
 'rprime_s_Ohm':{str(s):(1e-4/(1e4*math.pi*(.075e-4)**2))*s for s in [D,.3,sm]}}}
if lc and isinstance(lc[0],dict):
    result['raw_json']['long_field_keys']=list(lc[0])
    result['raw_json']['long_kind_counts']={k:sum(x.get('kind')==k for x in lc) for k in sorted({x.get('kind') for x in lc})}
    result['raw_json']['long_above_Lpar_count']=sum(float(x['Lc_um'])>j['thresholds_used']['L_par_um']*(1+C.CJUNC_LPAR_RTOL) for x in lc)
s=np.array([0,D,np.nextafter(D,np.inf),.25,.3,sm,.4,1.])[:,None]
d=np.array([0,.1,D,.3,.5])[None,:]
base=C._continuity(s,d,D,None)
result['floor_equivalence']=[{'s_min':t,'same_as_None':bool(np.array_equal(base,C._continuity(s,d,D,t)))} for t in [0,D/2,D]]
result['predicate_example']=[{'s_min':t,'s_um':.25,'d_um':.15,'floor':bool(C._self_floor(.25,.15,D)),'continuous':bool(C._continuity(.25,.15,D,t))} for t in [0,.3,sm]]

def registry(P,t,sid=None):
    n=(10,10,4); h=.15
    if sid is None:
        sid=np.zeros(n,np.uint8)
        for p,q in zip(P[:-1],P[1:]):
            cells=segment_cells(p,q,h)
            sid[tuple(cells.T)]=3
    sd=np.argwhere(sid==5); Q=np.vstack([P,(sd+.5)*h])
    ph=np.r_[np.full(len(P),2),np.full(len(sd),5)]
    fi=np.r_[np.full(len(P),11),np.arange(22,22+len(sd))]
    ki=np.r_[np.ones(len(P),int),np.zeros(len(sd),int)]
    return C.cjunc_registry(sid,(0.,0.,0.),h,Q,ph,fi,ki,r_f_um=.075,tol_ff_um=D-.15,L_par_um=.3,r_port_um=.3,s_min_um=t),sid

# Tiny two-segment V: its global segment closest point is the shared vertex.
# Search only registry geometry; no field/conductivity solve or input value read.
found=None; tried=0
for angle in [30,40,50,60,70,80]:
  if found: break
  th=math.radians(angle/2)
  for rot in [0,15,30,45,60,75]:
    if found: break
    rt=math.radians(rot); R=np.array([[math.cos(rt),-math.sin(rt)],[math.sin(rt),math.cos(rt)]])
    arms=np.array([[math.cos(th),math.sin(th)],[math.cos(th),-math.sin(th)]])@R.T*.5
    for ox in [.005,.04,.075,.11,.145]:
      if found: break
      for oy in [.005,.04,.075,.11,.145]:
        b=np.array([.45+ox,.45+oy,.225]); P=np.stack([b+np.r_[arms[0],0],b,b+np.r_[arms[1],0]])
        r0,sid=registry(P,0.); r1,_=registry(P,.3,sid); tried+=1
        c0,c1=r0['census'],r1['census']
        if c0['n_self_candidates']==0 and c0['n_self_fused_faces']!=c1['n_self_fused_faces']:
            found={'points':P,'sid3':np.argwhere(sid==3),'thresholds':[0,.3], 'census0':c0,'census03':c1,'registry_keys':list(r0)}
            break
result['geometry_search']={'tried':tried,'found':found}
if found:
    P=np.asarray(found['points']); r0,sid=registry(P,0.); r1,_=registry(P,.3,sid)
    f0,f1=r0['faces'],r1['faces']; changed=np.flatnonzero(f0['kind']!=f1['kind'])
    result['geometry_search']['face_changes']=[{'row':int(i),'linear':int(f0['lin'][i]),'axis':int(f0['ax'][i]),'owners':[int(f0['pa'][i]),int(f0['pb'][i])],
        'kind0':int(f0['kind'][i]),'kind03':int(f1['kind'][i]),'s_d_um':C._pos_pair_sd(int(f0['pa'][i]),int(f0['pb'][i]),r0['positions'],r0['segments'],r0['lo'],r0['vox'])} for i in changed]
    result['geometry_search']['rejections']=[r0['rejections'],r1['rejections']]
    result['geometry_search']['equivalence_0_D']=[{'s_min':t,'face_kind_same':bool(np.array_equal(registry(P,t,sid)[0]['faces']['kind'],r0['faces']['kind']))} for t in [D/2,D]]
    svfound=None; svtried=0
    for x in range(2,8):
      if svfound: break
      for y in range(1,5):
        q=sid.copy();q[x,y,1]=5
        a0,_=registry(P,0.,q);a1,_=registry(P,.3,q);svtried+=1
        c0,c1=a0['census'],a1['census']
        if c0['n_self_candidates']==0 and c0['n_sv_faces_cut_rows']!=c1['n_sv_faces_cut_rows']:
            svfound={'points':P,'sid3':np.argwhere(q==3),'sid5':np.argwhere(q==5),'rejections':[a0['rejections'],a1['rejections']],
                'census0':c0,'census03':c1,'sv_cut0':a0['faces']['sv_cut'],'sv_cut03':a1['faces']['sv_cut']}
            break
    if not svfound:
        # Cover two cells immediately above the changed VV face, touching only its two owners.
        q=sid.copy(); q[4,2,2]=5; q[4,3,2]=5
        a0,_=registry(P,0.,q);a1,_=registry(P,.3,q);svtried+=1
        c0,c1=a0['census'],a1['census']
        if c0['n_self_candidates']==0 and c0['n_sv_faces_cut_rows']!=c1['n_sv_faces_cut_rows']:
            svfound={'points':P,'sid3':np.argwhere(q==3),'sid5':np.argwhere(q==5),'rejections':[a0['rejections'],a1['rejections']],
                'census0':c0,'census03':c1,'sv_cut0':a0['faces']['sv_cut'],'sv_cut03':a1['faces']['sv_cut']}
    result['sv_geometry_search']={'tried':svtried,'found':svfound}
a.out.write_text(json.dumps(clean(result),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(clean({k:result[k] for k in ['arithmetic','floor_equivalence','predicate_example','geometry_search','sv_geometry_search']}),ensure_ascii=False,indent=2))
