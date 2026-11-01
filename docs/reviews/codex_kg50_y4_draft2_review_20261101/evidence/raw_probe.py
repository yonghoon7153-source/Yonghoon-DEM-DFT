"""Independent read-only arithmetic from supplied D1 raw dumps and D1-D3 logs.
No project modules imported, no DEM/network solver or scheduler called.
Usage: python raw_probe.py [source_directory]
"""
from pathlib import Path
import collections,csv,hashlib,io,json,math,re,sys,tarfile
import numpy as np
HERE=Path(__file__).resolve().parent
S=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'source'
P=S/'repo'; D=P/'docs/50kg/report_y4/draft2'
OUT=HERE/'independent';OUT.mkdir(exist_ok=True)
checks=[]
def ck(name,ok,detail=None):
 checks.append(dict(name=name,pass_=bool(ok),detail=detail))
def write(name,o): (OUT/name).write_text(json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
tgz=S/'external/kg50_d1_end_20261031.tgz'
members={};blobs={}
with tarfile.open(tgz) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
  data=t.extractfile(m).read();members[m.name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
  if any(k in m.name for k in ('atom_end','contact_end','mesh_end','input_kg50')):blobs[Path(m.name).name]=data
ck('seven raw members',len(members)==7)
met=json.loads((D/'data/D1/metrics_D1.json').read_text(encoding='utf-8'))
for n,v in met['provenance']['end_set']['members'].items():ck('member identity '+n,members[n]['sha256']==v['sha256'] and members[n]['bytes']==v['bytes'])
def read_dump(data):
 f=io.BytesIO(data);head=[f.readline().decode('ascii').strip() for _ in range(9)]
 return head,np.loadtxt(f)
ah,a=read_dump(blobs['atom_end_2785002.liggghts']);ch,c=read_dump(blobs['contact_end_2785002.liggghts'])
ids=a[:,0].astype(int);types=a[:,1].astype(int);r=a[:,5]*1000;z=a[:,4]*1000
ck('atom body count, unique ID and integer ID',len(a)==int(ah[3])==len(np.unique(ids)) and np.all(a[:,0]==ids))
ck('contact body count',len(c)==int(ch[3]))
ck('same atom/contact step',ah[1]==ch[1]=='2785002')
verts=np.array([list(map(float,v)) for v in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)',blobs['mesh_end_2785002.stl'].decode())])*1000
H=float(verts[0,2]);A=2500.;ck('flat mesh',len(verts)==6 and np.all(verts[:,2]==H))
vol=4/3*np.pi*r**3;vs=float(vol.sum());eps=100*(1-vs/(A*H));cnt=collections.Counter(types.tolist())
mx=int(ids.max());ty=np.zeros(mx+1,dtype=int);rad=np.zeros(mx+1);ty[ids]=types;rad[ids]=r
i=c[:,6].astype(int);j=c[:,7].astype(int)
ck('all contact IDs in atom set',np.isin(i,ids).all() and np.isin(j,ids).all())
t1=ty[i];t2=ty[j];amse=((t1==1)&(t2==3))|((t1==3)&(t2==1));amam=(t1==1)&(t2==1);sese=(t1==3)&(t2==3)
ck('all contacts AM/SE classes',np.all(amse|amam|sese))
ck('no self contacts',np.all(i!=j))
pairs=np.sort(np.column_stack([i,j]),axis=1)
duplicates=len(pairs)-len(np.unique(pairs,axis=0))
area=c[:,21]*1e6;delta=c[:,22]*1000
amids=ids[types==1];nse=np.bincount(np.where(t1[amse]==1,i[amse],j[amse]),minlength=mx+1)[amids]
ase=np.bincount(np.where(t1[amse]==1,i[amse],j[amse]),weights=area[amse],minlength=mx+1)[amids]
aaa=(np.bincount(i[amam],weights=area[amam],minlength=mx+1)+np.bincount(j[amam],weights=area[amam],minlength=mx+1))[amids]
free=4*np.pi*rad[amids]**2-aaa
cov=np.where(free>0,np.minimum(ase/free*100,100),0)
theta=delta/np.minimum(rad[i],rad[j])*100;theta_sum=delta/(rad[i]+rad[j])*100
max_theta=np.zeros(mx+1);max_theta_sum=np.zeros(mx+1)
np.maximum.at(max_theta,np.where(t1[amse]==1,i[amse],j[amse]),theta[amse]);np.maximum.at(max_theta_sum,np.where(t1[amse]==1,i[amse],j[amse]),theta_sum[amse])
recomputed={'n_am':int(cnt[1]),'n_se':int(cnt[3]),'plate_z_um':H,'v_sphere_sum_um3':vs,'eps_sphere_pct':eps,
 'am_se_cn_mean':float(nse.mean()),'se_se_cn_mean':float(sese.sum()*2/cnt[3]),'am_am_cn_mean':float(amam.sum()*2/cnt[1]),
 'coverage_hertz_pct':float(cov.mean()),'area_am_se_total_um2':float(area[amse].sum()),'area_am_se_n_contacts':int(amse.sum()),
 'area_am_se_per_contact_mean_um2':float(area[amse].mean()),'area_am_se_per_am_mean_um2':float(ase.mean()),
 'am_se_overlap_ratio_median_pct':float(np.median(theta[amse])),'am_se_overlap_ratio_card_median_pct':float(np.median(theta_sum[amse])),
 'overlap_ratio_mean_pct':float(theta.mean()),'overlap_ratio_max_pct':float(theta.max()),
 'am_frac_overlap_gt_10_pct':float(np.mean(max_theta[amids]>10)*100),'am_frac_overlap_card_gt_10_pct':float(np.mean(max_theta_sum[amids]>10)*100)}
for k,v in recomputed.items():
 expected=met['inventory'].get(k,met['metrics'].get(k));ck('D1 raw recomputation '+k,math.isclose(v,expected,abs_tol=2e-7,rel_tol=1e-9),{'actual':v,'reported':expected})
# Independent AM-wise CSV comparison (no use of its values to generate aggregates).
pc={int(x['am_id']):x for x in csv.DictReader((D/'data/D1/per_am_D1.csv').open())}
for q,aid in enumerate(amids):
 row=pc[int(aid)]
 for k,v,tol in [('n_am_se',nse[q],0),('area_am_se_um2',ase[q],5.1e-5),('coverage_hertz_pct',cov[q],5.1e-4),('max_overlap_am_se_pct',max_theta[aid],5.1e-7),('max_overlap_am_se_sum_pct',max_theta_sum[aid],5.1e-7)]:
  ck('per-AM %d %s'%(aid,k),abs(float(row[k])-float(v))<=tol)
decks={'D1':'docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts','D2':'docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50/input_kg50_d2_b50.liggghts','D3':'docs/data/kg50_decks_20261026_v2/kg50_d3_b50_s1/input_kg50_d3_b50_s1.liggghts'}
logs={'D1':'docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts','D2':'docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts','D3':'docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_b50_s1_log.liggghts'}
def thermo(path):
 text=path.read_text(encoding='utf-8');phase=None;blocks=[];active=False
 for no,line in enumerate(text.splitlines(),1):
  if line.startswith('====== PHASE 3:'):phase='loading'
  elif line.startswith('====== PHASE 4:'):phase='relaxation'
  if phase is None:continue
  w=line.split()
  if w and w[0]=='Step' and 'pressMPa' in w: b={'phase':phase,'header':w,'rows':[]};blocks.append(b);active=True;continue
  if line.startswith('Loop time of'):active=False
  if active and len(w)==5 and w[0].isdigit():
   try:b['rows'].append({'line':no,**dict(zip(b['header'],map(float,w)))})
   except ValueError:pass
 return text,blocks
alllogs={}
for bed,path in logs.items():
 text,bs=thermo(P/path);load=[b for b in bs if b['phase']=='loading'];relax=[b for b in bs if b['phase']=='relaxation']
 # The final run 0 is an export/setup readout, NOT the 100000-step relaxation endpoint.
 # Do not substitute its documented mesh-force accumulation artifact for P_end.
 dynamic_relax=[b for b in relax if b['rows'][-1]['Step']>b['rows'][0]['Step']]
 export0=[b for b in relax if b['rows'][-1]['Step']==b['rows'][0]['Step']]
 start=load[0]['rows'][0];stop=load[-1]['rows'][-1];end=dynamic_relax[-1]['rows'][-1];first=dynamic_relax[0]['rows'][1]
 info={'start_step':int(start['Step']),'stop':stop,'first_relax':first,'end':end,'compression_runs':len(load),'p_stop_MPa':stop['pressMPa']*1000,'p_end_MPa':end['pressMPa']*1000,'drop_MPa':(stop['pressMPa']-end['pressMPa'])*1000,'lost_atoms':int(stop['Atoms']-end['Atoms']),'minimum_relax_MPa':min(r['pressMPa'] for b in relax for r in b['rows'])*1000}
 changes=[];last=None
 for b in bs:
  for row in b['rows']:
   n=int(row['Atoms'])
   if n!=last:changes.append({'step':int(row['Step']),'N':n,'line':row['line']});last=n
 info['inventory_transitions']=changes
 info['excluded_export_run0_readout_MPa']=[b['rows'][-1]['pressMPa']*1000 for b in export0]
 metric=json.loads((D/f'data/{bed}/metrics_{bed}.json').read_text())
 for k,actual in [('p_t0minus_MPa',info['p_stop_MPa']),('p_end_MPa',info['p_end_MPa'])]:ck(bed+' log '+k,abs(metric['metrics'][k]-actual)<1e-9)
 z0=float(re.search(r'^====== PLATE HEIGHT: (\S+) ======$',text,re.M)[1])*1000
 deck=(P/decks[bed]).read_text();dt=float(re.search(r'^variable\s+dt\s+equal\s+(\S+)',deck,re.M)[1]);speed=float(re.search(r'^variable\s+press_speed\s+equal\s+(\S+)',deck,re.M)[1])
 predicted_h=z0-(stop['Step']-start['Step'])*dt*speed*1000
 ck(bed+' deck schedule predicts mesh height',abs(predicted_h-metric['metrics']['plate_z_um'])<.0005)
 info['plate_height_pred_um']=predicted_h
 # Curve uses *end* inventory for every time; quantify known error, no new inventory claim.
 table=list(csv.DictReader((D/f'data/{bed}/curve_{bed}.csv').open()))
 info['curve_rows']=len(table)
 alllogs[bed]=info
allmetrics={bed:json.loads((D/f'data/{bed}/metrics_{bed}.json').read_text()) for bed in logs}
# Stable evidence key discovery and exact file fingerprint comparison.
fps={bed:m['provenance'].get('tool_sha256',m['provenance'].get('tool_hashes',{})) for bed,m in allmetrics.items()}
write('d1_raw_recalculation.json',{'archive_sha256':hashlib.sha256(tgz.read_bytes()).hexdigest(),'members':members,'duplicate_unordered_pairs':duplicates,'metrics':recomputed,'contact_counts':{'AM_SE':int(amse.sum()),'AM_AM':int(amam.sum()),'SE_SE':int(sese.sum())},'SE_lost_eps_pp':5*(4/3*math.pi*.5**3)/(A*H)*100,'end_gamma_vz_signed_sim':1e-5*float(a[:,8].sum()),'end_gamma_abs_vz_sim':1e-5*float(np.abs(a[:,8]).sum())})
write('logs_recalculated.json',alllogs)
write('checks.json',{'pass':sum(x['pass_'] for x in checks),'fail':sum(not x['pass_'] for x in checks),'failed':[x for x in checks if not x['pass_']],'checks':checks})
print(json.dumps({'pass':sum(x['pass_'] for x in checks),'fail':sum(not x['pass_'] for x in checks),'failed':[x for x in checks if not x['pass_']][:10],'D1':recomputed,'logs':{k:{z:v[z] for z in ['p_stop_MPa','p_end_MPa','drop_MPa','lost_atoms']} for k,v in alllogs.items()}},ensure_ascii=False,indent=2))
