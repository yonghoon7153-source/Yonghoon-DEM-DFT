"""Rebuild committed summary handovers through both versions, without raw-dump analysis."""
from pathlib import Path
import sys,copy,csv,io,json,hashlib,importlib.util
R=Path(__file__).resolve().parents[1];S=R/'source'
sys.path.insert(0,str(S/'scripts'))
import lhs_design_dataset as new
spec=importlib.util.spec_from_file_location('lhs_before',Path(__file__).parent/'reference_lhs_before.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def serial(rows,cols,sep=','):
 f=io.StringIO(newline='');w=csv.DictWriter(f,cols,delimiter=sep,lineterminator='\n');w.writeheader();w.writerows(rows)
 return f.getvalue().encode('utf8')
def sha(b):return hashlib.sha256(b).hexdigest()
out=[]
for label,design,harvest,union,batch in [
 ('130',new.DESCRIPTOR_FILL_EXPECTED['path'],'docs/data/lhs_descriptors_cov_1e09f661d',new.DEFAULT_UNION_TSV,'docs/data/lhs_webapp_contact_d1ec42fba'),
 ('64','docs/data/lhsx_design_adapted_20260929.csv','docs/data/lhsx_descriptors_cov_1e09f661d','docs/data/lhs_union_20260927/lhsx64_union.tsv','docs/data/lhsx_webapp_contact_d1ec42fba')]:
 d=rows(S/design);h=new.load_harvest(S/harvest);u=new.load_union(S/union);wa=new.load_webapp(S/batch)
 for groups in ('contact,percolation','contact,percolation,f1,fracture,area'):
  both=[]
  for module in (old,new):
   o,c,_=module.build_handover(copy.deepcopy(d),copy.deepcopy(h),union=copy.deepcopy(u),webapp=copy.deepcopy(wa),webapp_groups=groups)
   both.append((serial(o,c),serial(module.column_dictionary(c,webapp=wa),['column','source','verdict','meaning','caveat'],'\t')))
  assert both[0]==both[1]
  out.append(dict(cohort=label,groups=groups,rows=len(d),columns=len(c),table_sha256=sha(both[1][0]),dictionary_sha256=sha(both[1][1]),byte_identical=True))
# Independent literal names: overlapping suffixes and old diagonal-VM names.
lw=['stress_cv_lw','stress_cv_lw_nowall','stress_ratio_AM_P_lw','stress_ratio_SE_lw_nowall','stress_lw_timestep','stress_lw_check_virial_total_rel']
legacy=['stress_cv','stress_ratio_AM_P','stress_z_layer_cv','stress_cv_contract','stress_cv_status']
assert all((new.wa_excluded(c) or '').startswith('frame_unverified') for c in lw)
assert all(new.wa_excluded(c) is None for c in legacy)
new.write_exclusion_notes(R/'evidence/handover_excluded.tsv')
result=dict(comparisons=out,LW_rejected=lw,legacy_not_LW_excluded=legacy,
 reference_sha256=sha((Path(__file__).parent/'reference_lhs_before.py').read_bytes()))
(R/'evidence/handover_before_after.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
