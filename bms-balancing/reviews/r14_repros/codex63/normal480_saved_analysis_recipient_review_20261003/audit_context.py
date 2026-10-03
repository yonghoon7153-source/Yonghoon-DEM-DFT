"""Small provenance and units checks. Reads code as text only."""
from pathlib import Path
import csv,json,hashlib
from decimal import Decimal as D,getcontext
getcontext().prec=50
ROOT=Path(__file__).resolve().parent
R=ROOT/'received'; P=ROOT.parent/'normal480_native_review_20261001'
T=P/'received/run/tables'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
checks=[]
def ck(n,v):
    checks.append({'check':n,'pass':bool(v)})
    assert v,n
for p in sorted(T.glob('units_*_evaluated.csv')):
    if p.name not in {Path(x['file']).name for x in json.loads((R/'INPUT_BINDING.json').read_bytes())['used_payload_entries']}:continue
    with p.open(encoding='utf-8-sig',newline='') as f:rr=list(csv.DictReader(f))
    ck('Unit readback '+p.name,all(r['expected']==r['actual'] for r in rr))
before=json.loads((R/'SOURCE_PRESERVATION_BEFORE.json').read_bytes())
bp=ROOT.parent/'b020_voltage_review_20260928/received/SUMMARY.json'
rec=[r for r in before if 'b020_voltage_decomposition' in r['path'] and r['path'].endswith('SUMMARY.json')]
ck('B020 prior summary byte identity',len(rec)==1 and bp.stat().st_size==rec[0]['bytes'] and sha(bp)==rec[0]['sha256'])
b=json.loads(bp.read_bytes());s=json.loads((R/'SUMMARY.json').read_bytes())
for term in ['Eeq','etaMid','phiL']:
    ck('B020 summary delta '+term,D(s['intervals'][0][term+'_change_mV'])-D(b['components'][term]['change_mV'])==D(s['B020_accepted_summary_difference_mV'][term]))
ck('B020 voltage change delta',D(s['intervals'][0]['voltage_change_mV'])-D(b['voltage_change_mV'])==D(s['B020_accepted_summary_difference_mV']['voltage_change_mV']))
source=(P/'received/candidate/src/Normal480Candidate.java').read_text(encoding='utf-8-sig')
expressions=['comp1.intd1(comp1.liion.cs_average)/(L_el*cs_Gr_max)','comp1.intd3(comp1.liion.cs_average)/(L_pos*cs_NCM_max)','comp1.intd1(comp1.liion.ivtot)','comp1.intd3(comp1.liion.ivtot)','-comp1.intd2(comp1.liion.Isx)/L_sep','liion.cs_average/liion.csmax','def.Eeq(liion.socloc_surface)']
ck('Definitions trace to sealed Java text',all(e in source for e in expressions))
ck('Source temperature definition retained','{"T_init","298.15[K]"}' in source and '(T_init-298[K])' in source)
pdf=json.loads((ROOT/'ARCHIVE_AUDIT.json').read_bytes())
res={'status':'PASS','checks':checks,'visual_review':{'pages_inspected':[1,2,3,4,5,6,7],'render':'Bundled Poppler 105 dpi','readable_axes_units_legends_tables':True,'unintended_clipping_observed':False,'not_claimed':'Every PDF vector point reverse-verified'},'source_preservation_scope':{'sender_before_after_entries':len(before),'mapped_to_current_recipient_bytes':len(before),'mapping':'native ZIP, prior reviewer ZIP, 20 input binding entries, prior B020 summary','not_claimed':'Current sender filesystem/MPH/prefs/OS/process state'},'originals_after':{n:sha(Path('C:/Users/Administrator/Downloads')/n) for n in ['NORMAL480_ANALYSIS.pdf','COMSOL63_NORMAL480_SAVED_ANALYSIS_20261001.zip']},'limitations':['The post-delivery timing and execution counts of the sender analysis were not independently observed.','No source analyzer, COMSOL or received test was executed.','Rtol-only 30-second proposal is not acceptance of 480-second convergence and is not a new execution approval.']}
reviewzip=P/'COMSOL63_NORMAL480_NATIVE_RECIPIENT_REVIEW_20261001.zip'
rv=json.loads((R/'INPUT_BINDING.json').read_bytes())['review_zip']
ck('Prior reviewer ZIP bound',sha(reviewzip)==rv['sha256'] and reviewzip.stat().st_size==rv['bytes'])
ck('Review preserves original standalone PDF',res['originals_after']['NORMAL480_ANALYSIS.pdf']==pdf['pdf']['sha256'])
ck('Review preserves original analysis ZIP',res['originals_after']['COMSOL63_NORMAL480_SAVED_ANALYSIS_20261001.zip']==pdf['zip']['sha256'])
(ROOT/'CONTEXT_AUDIT.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':res['status'],'checks':len(checks),'pages':7,'mapped_sender_preservation_entries':len(before)}))
