"""Independent frozen-delivery reconciliation + actual reviewer mutants. No solves."""
from pathlib import Path
import csv,json,math,hashlib,collections,statistics,shutil,sys,subprocess
R=Path(__file__).resolve().parents[1];S=R/'source';B=S/'docs/data/lhs_network194_11fcf91e8';H=B/'handover_v12_20261006';E=R/'evidence'
sys.path.insert(0,str(S/'scripts'))
def read(p,sep=','):
 with p.open(encoding='utf8',newline='') as f:
  d=csv.DictReader(f,delimiter=sep);rows=list(d);return d.fieldnames,rows
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b):
 if a==b:return True
 try:return math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=0)
 except (ValueError,TypeError):return False
def write(p,cols,rows,sep=','):
 with p.open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,delimiter=sep,lineterminator='\n');w.writeheader();w.writerows(rows)
def load(p):return json.loads(p.read_text(encoding='utf8'))
def dist(v):return dict(n=len(v),min=min(v),median=statistics.median(v),max=max(v)) if v else dict(n=0)
fail=[];out={};allids=[]
man=load(B/'manifest.json')
for c,n in [('lhs',130),('lhsx',64)]:
 cols,rows=read(H/f'{c}_handover_v12_20261006.csv');ids=[r['case_id'] for r in rows];allids+=ids
 expected={f'lhs00_{i:03}' for i in range(130)} if c=='lhs' else {f'lhsx_{i:03}' for i in range(1,65)}
 assert len(rows)==n and len(set(ids))==n and set(ids)==expected
 assert len(cols)==len(set(cols));assert not any(x.startswith('stress') for x in cols)
 pc,prev=read(S/f'docs/data/{c}_handover_20261001.csv');pd={r['case_id']:r for r in prev}
 _,dr=read(H/f'{c}_handover_v12_20261006_columns.tsv','\t');assert len(dr)==len(cols) and {r['column'] for r in dr}==set(cols)
 common=set(cols)&set(pc)-{'case_id'};diffs=[(r['case_id'],k,pd[r['case_id']][k],r[k]) for r in rows for k in common if not close(r[k],pd[r['case_id']][k])]
 fail += [('old_cell',*x) for x in diffs];dropped=sorted(set(pc)-set(cols));assert not dropped
 _,mr=read(B/f'merged/{c}/metrics_flat.csv');metrics={r['case']:r for r in mr}
 _,pr=read(H/f'{c}_handover_v12_20261006_tau_provenance.tsv','\t');prov={r['case']:r for r in pr};assert len(pr)==n and set(prov)==expected
 _,perc=read(S/f'docs/data/lhs_perc_audit_20261001/{c}_20261001_d1ec42fba/perc_audit.tsv','\t');pa={r['case']:r for r in perc}
 st=load(B/f'merged/{c}/status.json');runs={r['case']:r for r in st['runs']};assert len(runs)==n
 samples={m:collections.defaultdict(list) for m in ['hertz','physics']};status={m:collections.Counter() for m in samples};mb=[];cf=[];cf_above_phi=[];cf_above1=[];cf_null=[];source_checks=0;basis_error=[];audit_hashes={}
 for r in rows:
  i=r['case_id'];p=R/'tau_sources/cases'/i/'work/results'/i;d=load(p/'network_conductivity_dual.json');f=load(p/'full_metrics.json');np=load(p/'network_provenance.json');a=prov[i];q=metrics[i]
  assert sha(p/'network_conductivity_dual.json')==a['dual_sha256'] and sha(p/'full_metrics.json')==a['full_metrics_sha256']
  rid=a['network_run_id'];assert rid==np['network_run_id']==f['network_run_id']==st['cases'][i]['network_run_id']
  assert np['code_sha']==runs[i]['git_sha']=='11fcf91e8a1f4837b83892b7e4a81125eaeee4e5' and runs[i]['dirty'] is False
  assert np['input_digests']['atoms.csv']==a['atoms_csv_digest'] and np['input_digests']['contacts.csv']==a['contacts_csv_digest']
  assert sha(S/'scripts/tau_flux.py')==a['tau_flux_py_sha256']==man['code_hashes']['scripts/tau_flux.py']
  phi=float(q['phi_se_mass_conserving']);lg=float(q['thickness_um']);lm=float(q['thickness_mass_conserving_um']);phis=phi*lm/lg
  basis_error.append(abs(phis-f['phi_se']))
  assert float(r['ion_sigma0_mScm'])==3 and float(r['ion_sigma0_T_C'])==25 and r['phi_basis']=='mass_conserving' and r['L_basis']=='L_mc',(i,'shared')
  for mode,key in [('hertz','hertzian'),('physics','physics')]:
   rec=d[key];s=r[f'ion_net_status_{mode}'];status[mode][s]+=1
   assert rec['boundary_rule']=='L0';tp=rec['temperature_provenance'];assert rec['sigma_grain_S_cm']==.003 and tp['T_ref_C']==25 and tp['sigma_ion_T_factor']==1
   full=rec['sigma_full']
   assert (full is None and q[f'network_dual.{key}.sigma_full']=='') or full==float(q[f'network_dual.{key}.sigma_full'])
   if s=='NOT_PERCOLATING':
    assert pa[i]['se_perc_webapp_dump']=='False' and rec['sigma_full_status']=='valid_zero' and rec['sigma_full_reason']=='no_through_path'
    assert float(r[f'f_ion_{mode}'])==0 and r[f'tau2_ion_{mode}']==r[f'tau_ion_{mode}']==''
   else:
    assert pa[i]['se_perc_webapp_dump']=='True' and rec['sigma_full_status']=='computed'
    fm=full*lg/lm;T=phi/fm
    assert math.isclose(float(r[f'f_ion_{mode}']),fm,rel_tol=1e-9)
    assert math.isclose(float(r[f'f_ion_{mode}_gap']),full,rel_tol=1e-9)
    assert math.isclose(float(r[f'tau2_ion_{mode}']),T,rel_tol=1e-9)
    assert math.isclose(float(r[f'tau_ion_{mode}']),math.sqrt(T),rel_tol=1e-9)
    assert (s=='MODEL_BELOW_CONTINUUM_BOUND')==(T<1)
    samples[mode]['T'].append(T);samples[mode]['ion_mScm_mc'].append(3*fm);samples[mode]['ion_mScm_gap'].append(3*full)
    if mode=='physics' and T<1:mb.append(dict(case=i,T=T,phi_mc=phi,phi_spheres=phis,boundary_band_frac=rec['boundary_band_frac']))
   assert d['hertzian']['sigma_bulk_net']==d['physics']['sigma_bulk_net']
  cfv=d['hertzian']['sigma_bulk_net']
  if d['hertzian']['sigma_full_status']=='computed':
   if cfv is None:cf_null.append([i,d['hertzian'].get('sigma_bulk_net_reason')])
   else:
    cf.append(cfv)
    if cfv>phis:cf_above_phi.append(i)
    if cfv>1:cf_above1.append(i)
  source_checks+=1
 out[c]=dict(rows=n,columns=len(cols),common_columns=len(common),old_cells=n*len(common),old_cell_diffs=diffs,new_columns=len(set(cols)-set(pc)),dropped=dropped,source_checks=source_checks,status={k:dict(v) for k,v in status.items()},distributions={m:{k:dist(v) for k,v in z.items()} for m,z in samples.items()},below_bound=mb,CF=dist(cf),CF_above_phi=len(cf_above_phi),CF_above1=len(cf_above1),CF_null=cf_null,basis_error_max=max(basis_error))
_,au=read(H/'seal_audit.tsv','\t');assert len(au)==len(set(a['case'] for a in au))==194 and set(a['case'] for a in au)==set(allids)
assert all(a['verdict']=='SEALED_LEGACY' and a['merged']=='same' for a in au)
out['audit_ids_unique']=194;out['fail']=fail
(E/'delivery_independent.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))

# Submitted CLI: baseline and two isolated evidence-corruption mutants.
script=H/'reread_v12.py';M=R/'mutants';M.mkdir(exist_ok=True)
results=[]
for name in ['baseline','common_cell','audit_duplicate']:
 h=M/name;h.mkdir(exist_ok=True)
 for p in H.iterdir():
  if p.suffix in ('.csv','.tsv'):shutil.copyfile(p,h/p.name)
 mutation=None
 if name=='common_cell':
  p=h/'lhs_handover_v12_20261006.csv';cols,rr=read(p);key='coverage_AM_total_hertz_pct';mutation=[rr[0]['case_id'],key,rr[0][key],'99'];rr[0][key]='99';write(p,cols,rr)
 if name=='audit_duplicate':
  p=h/'seal_audit.tsv';cols,rr=read(p,'\t');mutation=[rr[-1]['case'],rr[0]['case']];rr[-1]=dict(rr[0]);write(p,cols,rr,'\t')
 op=E/f'reread_{name}.json';cp=subprocess.run([sys.executable,str(script),'--handover-dir',str(h),'--seal-audit',str(h/'seal_audit.tsv'),'--tau-sources',str(R/'tau_sources'),'--out',str(op)],text=True,encoding='utf8',capture_output=True)
 (E/f'reread_{name}.log').write_text(cp.stdout+cp.stderr,encoding='utf8')
 data=load(op) if op.exists() else {}
 results.append(dict(name=name,mutation=mutation,rc=cp.returncode,verdict=data.get('verdict'),fails=data.get('fails'),regression=data.get('lhs',{}).get('C4_regression',{}).get('cells'),C8=data.get('C8_seal_audit')))
(E/'reread_mutants.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(results,ensure_ascii=False,indent=2))
