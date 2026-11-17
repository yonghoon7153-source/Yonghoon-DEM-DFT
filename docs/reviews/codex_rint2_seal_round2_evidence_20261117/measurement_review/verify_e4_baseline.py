"""Read only declared S0 geometric baseline blobs; no solver/NPZ/research log."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
BASE=OUT/'baseline_1113'
BASE.mkdir(exist_ok=True)
ENV=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
def git(*args):
    return subprocess.check_output(['git','--git-dir='+str(ROOT/'objects.git'),*args],env=ENV)
REV=git('rev-parse','6bf70fe4a^{commit}').decode().strip()
prefix='docs/data/rint2_s0_sbe_20261113/'
sub='files/ca1_s0_sbe_20261113T014726Z_q2q11/'
paths=['SHA256SUMS','NPZ_SHA256.txt','MANIFEST.tsv',sub+'cjunc_plan.json',sub+'cjunc_plan.sha256',sub+'s0_stage1_kit_SBE_vgcf100.json']
extracted=[]
for rel in paths:
    data=git('show',REV+':'+prefix+rel)
    dest=BASE/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(data)
    extracted.append({'source':REV+':'+prefix+rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                      'git_blob':git('rev-parse',REV+':'+prefix+rel).decode().strip()})
checks=[]
for line in (BASE/'SHA256SUMS').read_text(encoding='utf-8').splitlines():
    digest,rel=line.split(maxsplit=1)
    p=BASE/rel.lstrip('*')
    if p.is_file():
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        checks.append({'path':rel,'expected':digest,'actual':actual,'ok':digest==actual})
newbase=ROOT/'input/repo/docs/data/rint2_s0_sbe_20261116'
newsub='files/ca1_s0_sbe_20261116T004809Z_q14final/'
old=json.loads((BASE/sub/'s0_stage1_kit_SBE_vgcf100.json').read_text(encoding='utf-8'))
new=json.loads((newbase/newsub/'s0_stage1_kit_SBE_vgcf100.json').read_text(encoding='utf-8'))
def flatten(obj,path='',list_mode='all'):
    result={}
    if isinstance(obj,dict):
        for key,value in obj.items():result.update(flatten(value,path+'.'+key if path else key,list_mode))
    elif isinstance(obj,list) and (list_mode=='all' or (list_mode=='objects' and all(isinstance(v,dict) for v in obj))
                                  or (list_mode=='metadata' and (path=='code.file_digests' or not any(isinstance(v,(dict,list)) for v in obj)))):
        for i,value in enumerate(obj):result.update(flatten(value,f'{path}[{i}]',list_mode))
        if not obj:result[path]=obj
    else:result[path]=obj
    return result
comparisons={}
for mode in ['atomic','objects','all','metadata']:
    a,b=flatten(old,list_mode=mode),flatten(new,list_mode=mode)
    keys=sorted(set(a)|set(b))
    differences=[{'field':k,'old':a.get(k),'new':b.get(k)} for k in keys if a.get(k)!=b.get(k)]
    comparisons[mode]={'old_fields':len(a),'new_fields':len(b),'difference_count':len(differences),'differences':differences}
plans=[json.loads(p.read_text(encoding='utf-8')) for p in [BASE/sub/'cjunc_plan.json',newbase/newsub/'cjunc_plan.json']]
pa,pb=map(flatten,plans)
plan_diff=[{'field':k,'old':pa.get(k),'new':pb.get(k)} for k in sorted(set(pa)|set(pb)) if pa.get(k)!=pb.get(k)]
def npzhashes(p):
    return {Path(name.lstrip('*')).name:dig for dig,name in (l.split(maxsplit=1) for l in p.read_text(encoding='utf-8').splitlines() if l.strip())}
npz_old,npz_new=npzhashes(BASE/'NPZ_SHA256.txt'),npzhashes(newbase/'NPZ_SHA256.txt')
result={'baseline_commit':REV,'extracted_raw_blobs':extracted,'baseline_SHA256SUMS_checks':checks,
        'comparisons':comparisons,'plan_differences':plan_diff,'NPZ_hash_records_equal':npz_old==npz_new,
        'NPZ_hash_records':npz_old,'NPZ_bytes_opened':False}
identity=[]
for label,obj in [('old',old),('new',new)]:
    rev=obj['code']['git_head']
    rows=[]
    for rec in obj['code']['file_digests']:
        path='scripts/'+rec['file']
        actual=hashlib.sha256(git('show',rev+':'+path)).hexdigest()
        rows.append({'file':rec['file'],'ok':actual==rec['sha256'],'actual':actual,'record':rec['sha256']})
    identity.append({'which':label,'code_pin':rev,'file_digests':rows,
                     'tool_sha_matches_census':obj['code']['tool_sha256']==next(x['actual'] for x in rows if x['file']=='ca_s0_census.py')})
result['old_new_code_attribution']=identity
result['settings_and_input_fields_unchanged_except_argv']=all(d['field']=='inputs.payload_argv_sha256' for d in comparisons['all']['differences'] if d['field'].startswith('inputs.'))
(OUT/'e4_baseline_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'baseline_commit':REV,'hash_checks':checks,
                  'field_counts':{m:{k:v for k,v in r.items() if k!='differences'} for m,r in comparisons.items()},
                  'changed_fields_all':[v['field'] for v in comparisons['all']['differences']],
                  'plan_changed_fields':[v['field'] for v in plan_diff], 'NPZ_hash_records_equal':npz_old==npz_new},ensure_ascii=False,indent=2))
