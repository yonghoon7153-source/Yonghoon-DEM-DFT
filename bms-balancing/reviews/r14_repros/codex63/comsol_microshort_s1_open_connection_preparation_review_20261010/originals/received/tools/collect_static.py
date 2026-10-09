"""Author-owned file/text collector. Does not import/execute candidate programs."""
from pathlib import Path
import hashlib, json, re, html, zipfile
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parents[1]
SRC=WORK/'outputs/microshort_s1o_r1_20261008'
DOC=Path('C:/Program Files/COMSOL/COMSOL63/Multiphysics/doc/help/wtpwebapps/ROOT/doc/com.comsol.help.comsol')
def identity(p):
    raw=p.read_bytes()
    return {'path':p.as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def save(name,obj):
    p=ROOT/name
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
mf=json.loads((SRC/'CODE_MANIFEST.json').read_bytes())
selected=[identity(SRC/'CODE_MANIFEST.json')]
checks=[]
for e in mf['files']:
    got=identity(SRC/e['path']);selected.append(got)
    checks.append({'path':e['path'],'expected':e,'observed':got,'match':got['sha256']==e['sha256'] and got['bytes']==e['bytes']})
assert len(checks)==21 and all(c['match'] for c in checks)
assert selected[0]['sha256']=='4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da'
binding=json.loads((SRC/'contracts/EXECUTION_BINDING.json').read_bytes())
for e in binding['dependency_pins']:
    p=Path(e['path']);got=identity(p);selected.append(got)
    assert got['sha256']==e['sha256'] and got['bytes']==e['bytes'],str(p)
for e in binding['engine_pins']:
    p=Path(e['path']);got=identity(p);selected.append(got)
    assert got['sha256']==e['sha256'] and got['bytes']==e['bytes'],str(p)
archive_specs=[
('C:/Users/BML/Desktop/COMSOL_MICROSHORT_S1O_R1_004_SUPPLEMENT_REVIEW_20261009.zip','17779cbd61b2d592c15195d6b9810402042d790a6badd43bc9c5df1512bb5e0e'),
(str(SRC/'future_validation_fixture_R1_003/COMSOL_MICROSHORT_S1O_R1_003_VALIDATION_STOP_20261008.zip'),'11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b'),
(str(SRC/'future_validation_fixture_R1_004/COMSOL_MICROSHORT_S1O_R1_004_VALIDATION_RESULT_20261009.zip'),'cb85fa123395caf9ea323b0c531144bf30754322ba9b0362f1bbac3e5bc8ff2c')]
for path,digest in archive_specs:
    got=identity(Path(path));assert got['sha256']==digest;selected.append(got)
save('evidence/SELECTED_SOURCES_BEFORE.json',selected)
save('evidence/SOURCE_IDENTITY_CHECK.json',checks)
documents=[
'comsol_api_solver.51.19.html','comsol_api_solver.51.50.html','comsol_api_solver.51.51.html',
'comsol_ref_solver.36.118.html','comsol_ref_solver.36.120.html','comsol_ref_solver.36.158.html','comsol_ref_solver.36.163.html',
'api/com/comsol/model/physics/FeatureInfo.html','api/com/comsol/model/SolverSequence.html','api/com/comsol/model/SolutionInfo.html',
'api/com/comsol/model/PropFeature.html','api/com/comsol/model/NumericalFeature.html','comsol_api_general.47.51.html']
records=[]
for i,name in enumerate(documents,1):
    p=DOC/name;raw=p.read_bytes();s=raw.decode('utf-8')
    s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',s,flags=re.S|re.I)
    s=re.sub(r'</(?:div|p|tr|h[1-6]|pre|li|dt|dd)>','\n',s,flags=re.I)
    s=html.unescape(re.sub('<[^>]+>',' ',s))
    lines=[' '.join(t.split()) for t in s.splitlines() if t.strip()]
    out=ROOT/f'evidence/DOC_{i:02d}.txt'
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    records.append({'id':f'DOC_{i:02d}','original':identity(p),'text_extract':identity(out),'transform':'HTML tags removed, entities decoded, whitespace normalized; not native observation'})
save('evidence/LOCAL_DOCUMENTS.json',records)
print(json.dumps({'selected':len(selected),'source_members':len(checks),'documents':len(records),'candidate_execution':0}))
