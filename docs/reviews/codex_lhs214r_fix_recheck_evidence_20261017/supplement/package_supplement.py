"""Freeze supplementary evidence without changing the earlier review package."""
from pathlib import Path
import datetime,hashlib,json,os,zipfile
R=Path(__file__).resolve().parent
P=R.parent/'lhs214r_fix_recheck_20261017'
def lp(p):return Path('\\\\?\\'+str(p.resolve())) if os.name=='nt' else p
def read(p):return lp(p).read_bytes()
integrity={}
for label in ['source','base']:
    m=json.loads(read(P/f'{label}_manifest.json'));bad=[]
    for row in m['files']:
        if hashlib.sha256(read(P/label/row['path'])).hexdigest()!=row['sha256']:bad.append(row['path'])
    integrity[label]={'files':len(m['files']),'mismatches':bad,'pin':m['pin']};assert not bad
(R/'evidence/source_integrity_after_a4.json').write_text(json.dumps(integrity,indent=2),encoding='utf8')
result=json.loads(read(R/'evidence/received_a4_rerun.json'))
assert result['ok'] and len(result['rows'])==36 and all(x['identical'] for x in result['rows'])
items=[]
for folder,dirs,files in os.walk(lp(R)):
    dirs[:]=sorted(d for d in dirs if d not in ['tmp','__pycache__','.git'])
    for name in sorted(files):
        p=Path(folder)/name;rel=p.relative_to(lp(R)).as_posix()
        if rel=='PACKAGE_MANIFEST.json' or rel.endswith(('.pyc','.pyo')):continue
        b=p.read_bytes();items.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'schema':'review_supplement/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pin':'a4a1e52c0bc01731f4c1d00924099b56c05a055f','tested_code_pin':'60ba39e224aff48a030dccfe750342f3bf9db61f','verdict':'HOLD','files':items}
(R/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
dest=R.parent/'codex_lhs214r_a4a1e52c0_supplement_20261017.zip'
with zipfile.ZipFile(dest,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for x in items:z.write(lp(R/x['path']),R.name+'/'+x['path'])
    z.write(lp(R/'PACKAGE_MANIFEST.json'),R.name+'/PACKAGE_MANIFEST.json')
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))
    for x in items:assert hashlib.sha256(z.read(R.name+'/'+x['path'])).hexdigest()==x['sha256']
rec={'file':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(read(dest)).hexdigest(),'entries':len(items)+1,'file_checks':'PASS','crc':'PASS','pin':manifest['pin'],'a4':'36/36','verdict':'HOLD','source_integrity':integrity}
dest.with_suffix('.receipt.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rec,ensure_ascii=False,indent=2))
