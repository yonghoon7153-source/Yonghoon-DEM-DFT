"""Independently recompute arithmetic on committed summaries, not new DEM runs."""
from pathlib import Path
import sys,csv,json,math,copy
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence'
sys.path.insert(0,str(S/'scripts'))
import lhs_design_dataset as L
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
results=[]
for label,design,harvest,union,batch in [
 ('130',L.DESCRIPTOR_FILL_EXPECTED['path'],'docs/data/lhs_descriptors_cov_1e09f661d',L.DEFAULT_UNION_TSV,'docs/data/lhs_webapp_contact_d1ec42fba'),
 ('64','docs/data/lhsx_design_adapted_20260929.csv','docs/data/lhsx_descriptors_cov_1e09f661d','docs/data/lhs_union_20260927/lhsx64_union.tsv','docs/data/lhsx_webapp_contact_d1ec42fba')]:
 d=rows(S/design); h=L.load_harvest(S/harvest);u=L.load_union(S/union);wa=L.load_webapp(S/batch)
 args=dict(union=u,webapp=wa,webapp_groups='contact,percolation,f1,fracture,area')
 oc,cc,rc=L.build_handover(copy.deepcopy(d),copy.deepcopy(h),**args)
 nw=copy.deepcopy(wa);nw['stop_after']='network'
 on,cn,rn=L.build_handover(copy.deepcopy(d),copy.deepcopy(h),union=u,webapp=nw,webapp_groups=args['webapp_groups'])
 # Raw committed summary: no production gate used to calculate these residuals.
 raw=rows(S/batch/'metrics_flat.csv');peak_pct=peak_fi=peak_am=peak_pairs=0.;pairchecks=0
 for x in raw:
  nt=float(x['n_total_AM_AM_force']);ns=[float(x['n_'+s+'_force_AM_AM']) for s in L.FRAC_STAGES]
  assert sum(ns)==nt
  for s,n in zip(L.FRAC_STAGES,ns):peak_pct=max(peak_pct,abs(float(x['frac_'+s+'_force_pct'])-100*n/nt))
  peak_fi=max(peak_fi,abs(float(x['fracture_index_force'])-(ns[3]+ns[4])/nt))
  amn=float(x['am_am_n_contacts']);t=float(x['am_am_total_area']);m=float(x['am_am_mean_area'])
  peak_am=max(peak_am,abs(m*amn-t)/max(abs(t),1e-300))
  for b in L.WA_PAIR_BASES:
   if x.get(b+'_n') not in (None,'') and float(x[b+'_n'])>0:
    n=float(x[b+'_n']);t=float(x[b+'_total']);m=float(x[b+'_mean']);pairchecks+=1
    peak_pairs=max(peak_pairs,abs(m*n-t)/max(abs(t),1e-300))
 results.append(dict(cohort=label,rows=len(oc),contact_network_rows_identical=oc==on,columns_identical=cc==cn,
  frac_pct_max_abs_error_pp=peak_pct,frac_index_max_abs_error=peak_fi,am_area_max_rel_error=peak_am,
  pair_area_max_rel_error=peak_pairs,pair_checks=pairchecks))
print(json.dumps(results,indent=2))
(E/'handover_replay.json').write_text(json.dumps(results,indent=2),encoding='utf8')
