from pathlib import Path
import csv,json,hashlib,math,sys,collections
R=Path(__file__).resolve().parents[1];S=R/'source';B=S/'docs/data/lhs_network194_11fcf91e8';H=B/'handover_v12_20261006'
sys.path.insert(0,str(S/'scripts'));import run_network_194_parallel as runner
def read(p,sep=','):
 with p.open(encoding='utf8',newline='') as f:return list(csv.DictReader(f,delimiter=sep))
def j(p):return json.loads(p.read_text(encoding='utf8'))
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
man=j(B/'manifest.json');run=j(B/'runs/run_001.json');audit={r['case']:r for r in read(H/'seal_audit.tsv','\t')};out={'worker_records':[],'mapping_disagreements':[],'gate_counts':collections.Counter(),'mono_remaps':[]}
for c in ['lhs','lhsx']:
 rows=read(H/f'{c}_handover_v12_20261006.csv');prev=read(S/f'docs/data/{c}_handover_20261001.csv');oldcols=set(prev[0]);m={r['case']:r for r in read(B/f'merged/{c}/metrics_flat.csv')};st=j(B/f'merged/{c}/status.json');runs={r['case']:r for r in st['runs']}
 new=[k for k in rows[0] if k not in oldcols and k in m[rows[0]['case_id']]];assert len(new)==34
 for row in rows:
  i=row['case_id'];wr=j(B/f'cases/{i}/worker.json');a=wr['attempts'];rec=st['cases'][i];raw=m[i]
  assert len(a)==1 and a[0]['attempt']==a[0]['run']==1 and a[0]['rc']==0 and a[0]['outcome']=='done' and a[0]['network_run_id']==rec['network_run_id']
  assert digest(rec)==audit[i]['record_sha256']
  verdict,why=runner._judge_legacy(man,a,rec,[runs[i]],{1:run},man['git']['sha']);assert verdict=='SEALED_LEGACY'
  out['worker_records'].append(dict(case=i,verdict=verdict,record_hash_equal=True))
  # Compare new non-tau fields after mono phase-name translation.
  # Identify raw versus delivered AM label from phase presence (not guessed radii).
  delivered=[ph for ph in ['AM_P','AM_S'] if row.get(f'area_{ph}_SE_n','')!='']
  produced=[ph for ph in ['AM_P','AM_S'] if raw.get(f'area_{ph}_SE_n','')!='']
  swap=len(delivered)==len(produced)==1 and delivered!=produced
  if swap:out['mono_remaps'].append(dict(case=i,delivered=delivered[0],raw=produced[0]))
  for k in new:
   src=k
   if swap:src=k.replace('AM_P','AM_TMP').replace('AM_S','AM_P').replace('AM_TMP','AM_S')
   va=row[k];vb=raw.get(src,'')
   eq=va==vb
   if not eq:
    try:eq=math.isclose(float(va),float(vb),rel_tol=1e-12,abs_tol=0)
    except (ValueError,TypeError):pass
   # Defined zero-contact means are absent, not physical zeros.
   if not eq and va=='' and k.endswith('_mean'):
    countk=k[:-5]+'_n';count= row.get(countk,row.get('am_am_n_contacts') if k=='am_am_mean_area' else None)
    eq=count in ('0','0.0') and vb in ('','0','0.0')
   if not eq:out['mapping_disagreements'].append([i,k,src,va,vb])
  # Independent arithmetic identities on delivered fields.
  for k,v in row.items():
   if k.startswith('area_') and k.endswith('_mean'):
    b=k[:-5];nt=row.get(b+'_n','');tt=row.get(b+'_total','')
    if nt and float(nt)>0:assert v and tt and math.isclose(float(v)*float(nt),float(tt),rel_tol=1e-10)
    elif nt and float(nt)==0:assert v=='' and float(tt)==0
  stages=['intact','microcrack','multicrack','fragmentation','pulverization'];nt=row['n_total_AM_AM_force']
  if nt:
   nt=float(nt);ns=[float(row[f'n_{s}_force_AM_AM']) for s in stages];assert sum(ns)==nt and nt<=float(row['am_am_n_contacts'])
   if nt>0:
    for s,ns0 in zip(stages,ns):assert abs(float(row[f'frac_{s}_force_pct'])-100*ns0/nt)<=.005000001
    assert abs(float(row['fracture_index_force'])-(ns[3]+ns[4])/nt)<=.000050001
  out['gate_counts']['rows_area_fracture']+=1
  # N_SE = exact ionic node count (same atom table; full_metrics count may round).
  dual=j(R/f'tau_sources/cases/{i}/work/results/{i}/network_conductivity_dual.json');nse=dual['hertzian']['n_nodes']
  assert math.isclose(float(row['se_se_cn_aug']),float(row['se_se_cn'])+2*float(row['se_se_cn_aug_n_extra'])/nse,rel_tol=1e-10)
  out['gate_counts']['F1_identity']+=1
out['source19']={p:hashlib.sha256((S/p).read_bytes()).hexdigest()==v for p,v in man['code_hashes'].items()}
assert all(out['source19'].values())
out['run']=run;out['merge']=j(B/'merged/merge_report.json')
sm=j(B/'smoke_postfix/smoke_report.json');out['smoke_keys']=list(sm);out['smoke_checks']=sm.get('checks');out['smoke_failures']=sm.get('failures')
(R/'evidence/execution_and_567.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ['worker_records','smoke_checks']},ensure_ascii=False,indent=2))
print('workers',len(out['worker_records']))
