"""Contracted units and native mesh markers, data only."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent;R=ROOT/'received';T=R/'run/tables'
checks=[]
def check(name,ok):checks.append({'check':name,'pass':bool(ok)});assert ok,name
units={'eguard':['s']+['mol/m^3']*5+['1']*3,'nglobal':['s']+['mol/m^2']*3+['1']*7+['A/m^2']*3,'point1':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],'point4':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],'MinLinece':['s','mol/m^3'],'MaxLinece':['s','mol/m^3'],'profiletimes':['s'],'profileN':['s','m','1','1','V','V','V','1'],'profileP':['s','m','1','1','V','V','V','1']}
for tag,expected in units.items():
    for phase in (['inferred','configured','evaluated'] if tag=='eguard' else ['configured','evaluated']):
        a=expected.copy()
        if phase!='configured':
            for i in ([6,7,8] if tag=='eguard' else [10] if tag=='nglobal' else [7] if tag in ['profileN','profileP'] else []):a[i]=''
        value='['+', '.join(a)+']'
        with (T/f'units_{tag}_{phase}.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        check(tag+' '+phase,rows==[{'tag':tag,'phase':phase,'expected':value,'actual':value}])
expected=['AXES_PHYSICAL_MESH_DOMAIN=1|numelem=120','AXES_PHYSICAL_MESH_DOMAIN=2|numelem=60','AXES_PHYSICAL_MESH_DOMAIN=3|numelem=120','AXES_PARTICLE=pce1|Nel=320|Nord=1|Distribution=CubicRoot','AXES_PARTICLE=pce2|Nel=320|Nord=1|Distribution=CubicRoot','AXES_ACTUAL_MESH=mesh1|edges=300|vertices=301','PREFLIGHT_SOLVE_BEGIN=0..60 seconds; NO full protocol or sweep','ELECTROLYTE_THRESHOLD_EXPRESSION=0[mol/m^3]','ELECTROLYTE_THRESHOLD_SI=0.0']
counts=dict.fromkeys(expected,0)
with (R/'run/batch_console.log').open(encoding='utf-8-sig') as f:
    for line in f:
        if line.strip() in counts:counts[line.strip()]+=1
for k,v in counts.items():check(k,v==1)
source=(R/'candidate/src/Normal60Candidate.java').read_text()
check('one textual model runAll call',source.count('.runAll();')==1)
result={'status':'PASS','checks':checks,'scope':'Contracted units, source text and native log markers; not executing source.'}
(ROOT/'SUPPLEMENTAL_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','checks':len(checks)}))
