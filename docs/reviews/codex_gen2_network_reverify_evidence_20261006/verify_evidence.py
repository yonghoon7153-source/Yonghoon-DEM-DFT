"""Check recorded review outcomes, including expected counterexamples (not a production gate)."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parent;E=R/'evidence'
def read(p):return json.loads(p.read_text(encoding='utf8'))
checks=[]
def ck(name,cond):
 checks.append((name,bool(cond)));print(('PASS ' if cond else 'FAIL ')+name)
ck('14 test entrypoints exited 0',len(read(E/'tests.json'))==14 and all(x['rc']==0 for x in read(E/'tests.json')))
a=read(E/'adversarial.json');high=a['cg_dead_end'][-1]
ck('prior CG error rejected and exact G recovered',high['G']==15000.5 and high['info']['attempts'][0]['outcome']=='certificate_failed' and high['info']['method']=='spsolve_fallback')
ck('zero Rc constriction-only refuses instead of opening',a['zero_Rc']['G'] is None and a['zero_Rc']['info']['reason']=='zero_resistance_requires_contraction')
ck('8 previous generation mutants rejected',len(a['generation_mutants'])==8 and all(set(m['statuses'].values())=={'NOT_COMPUTED'} and m['stop9'] for m in a['generation_mutants']))
p=read(E/'acceptance.json');pub={x['label']:x for x in p['publication']};stamp={x['label']:x for x in p['stamp']}
ck('actual CLI baseline publishes',pub['baseline']['status']=='done')
ck('absent FULL certificate blocked',pub['missing_full_cert']['status']=='failed')
ck('G2RR-01 stamp contradictions still pass',all(stamp[k]['accepted'] and stamp[k]['generation']=='g2' for k in ('all_unknown','all_null','g2_declares_legacy')) and not stamp['stamp_absent_keys']['accepted'])
ck('G2RR-02 foreign branch certificates still publish',all(pub[k]['status']=='done' and pub[k]['full_q']==pub['baseline']['full_q'] and pub[k]['full_certificate']['I_bottom']!=pub['baseline']['full_certificate']['I_bottom'] for k in ('full_cert_from_cf','full_cert_from_h12')))
ck('diagnostic-only certificate failures do not gate FULL',all(pub[k]['status']=='done' for k in ('missing_cf_cert','cf_bad_conservation','missing_constr_cert')))
re={x['label']:x for x in read(E/'reread_extra.json')}
ck('C8 positive baseline',re['baseline']['rc']==0 and re['baseline']['c8']['queue_n']==194)
ck('G2RR-03 missing/duplicate queue still passes',all(re[k]['rc']==0 for k in ('queue_empty','plan_absent','queue_duplicate')) and re['queue_empty']['c8']['queue_n']==0)
old=read(E/'prior_real_beds.json');new=read(E/'real_beds.json');comparison=[]
def hexed(vals):return [None if v is None else float(v).hex() for v in vals]
for bed,b in old.items():
 for arm,r in b['arms'].items():
  for mode,vals in r['solves'].items():
   now=new[bed]['arms'][arm]['solves'][mode]
   comparison.append(dict(bed=bed,arm=arm,mode=mode,old=vals,new=now,identical=hexed(vals)==hexed(now)))
ck('20/24 raw-bed solves bit-identical including g1 control',sum(x['identical'] for x in comparison)==20)
ck('all FULL and CF raw-bed values bit-identical',all(x['identical'] for x in comparison if x['mode']!='constriction_only'))
ck('only physics g1/g2 constriction-only changed to None',all(x['identical'] or (x['arm'] in ('g1_mul','g2') and x['mode']=='constriction_only' and x['new']==[None,None]) for x in comparison))
(E/'real_beds_comparison.json').write_text(json.dumps(comparison,indent=2),encoding='utf8')
(E/'evidence_checks.json').write_text(json.dumps(dict(checks=checks,pass_count=sum(c for n,c in checks),fail_count=sum(not c for n,c in checks)),indent=2),encoding='utf8')
raise SystemExit(0 if all(c for n,c in checks) else 1)
