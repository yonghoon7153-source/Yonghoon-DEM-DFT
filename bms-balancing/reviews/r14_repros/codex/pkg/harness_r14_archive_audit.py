"""Read-only stored-artifact audit; does not import target code or replay runners."""
import csv
import ast
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
root=Path(sys.argv[1]);repo=root.parent
schema_literals={}
for node in ast.parse((root/'bms_balancing/schema.py').read_text()).body:
    if isinstance(node,ast.Assign):
        for t in node.targets:
            if isinstance(t,ast.Name) and t.id in {'MATRIX_ROW','PROFILE_ROW','SHAPE_ROW','DEGENERACY_KEYS'}:
                schema_literals[t.id]=ast.literal_eval(node.value)
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args])
def sha(b):return hashlib.sha256(b).hexdigest()
def num(v):
    if isinstance(v,bool):return None
    try:return Decimal(str(v))
    except (InvalidOperation,ValueError):return None
def recursive_numeric(a,b,p=''):
    result=[];compared=0
    if isinstance(a,dict) and isinstance(b,dict):
        for key in a.keys() & b.keys():
            if key in {'run_id','inputs_sha','ref_inputs_sha'}:continue
            n,ds=recursive_numeric(a[key],b[key],p+'/'+key);compared+=n;result+=ds
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b):result.append([p,'list_length',len(a),len(b)])
        for i,(x,y) in enumerate(zip(a,b)):
            n,ds=recursive_numeric(x,y,p+'/'+str(i));compared+=n;result+=ds
    elif isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool):
        compared+=1
        if num(a)!=num(b):result.append([p,a,b])
    return compared,result

head=git('rev-parse','HEAD').decode().strip()
arch=root/'out/archive/legacy_r6_u14'
archive=[]
for p in sorted(arch.iterdir()):
    if not p.is_file():continue
    old=git('show','37a889b^:bms-balancing/out/'+p.name)
    archive.append({'name':p.name,'bytes':p.stat().st_size,'prepromotion_bytes_identical':p.read_bytes()==old})
print('HEAD',head)
print('ARCHIVE',json.dumps({'count':len(archive),'mismatches':[e for e in archive if not e['prepromotion_bytes_identical']]}))
prom=git('show','--format=fuller','--no-patch','37a889b').decode()
print('PROMOTION_COMMIT_MESSAGE',prom)
print('MIXED_COMMITS_PY_SH_DIFF',git('diff','--name-only','0668665','419c1ab','--','*.py','*.sh').decode())
artifacts=[]; numeric_total=0; numeric_diff=[]; commits={};starts=set();envs=set()
for meta_path in sorted((root/'out').glob('*.meta.json')):
    m=json.loads(meta_path.read_bytes());p=meta_path.with_name(meta_path.name[:-10])
    if not p.name.startswith(('matrix_','profile_gamma_','degeneracy_','ne_shape_')):continue
    old=arch/p.name;body=p.read_bytes();prior=old.read_bytes()
    commit=m['git_commit'];commits[commit]=commits.get(commit,0)+1
    starts.add(m.get('starts'));envs.add(json.dumps(m.get('env'),sort_keys=True))
    e={'artifact':p.name,'size':len(body),'sidecar_sha_ok':sha(body)==m['sha256'],'git_start_end_equal':m.get('git_commit_at_start')==commit,'clean_start_and_end':m.get('git_dirty') is False and m.get('git_dirty_at_start') is False and m.get('git_state_changed_during_run') is False,'roster':m.get('roster'),'start':m.get('started_utc'),'created':m.get('created_utc')}
    if p.suffix=='.csv':
        rows=list(csv.DictReader(io.StringIO(body.decode('utf-8-sig'))));oldrows=list(csv.DictReader(io.StringIO(prior.decode('utf-8-sig'))))
        e['rows']=len(rows);e['old_rows']=len(oldrows);e['run_ids_match']=all(r.get('run_id')==m['run_id'] for r in rows)
        kind='MATRIX' if p.name.startswith('matrix_') else 'PROFILE' if p.name.startswith('profile_') else 'SHAPE'
        e['header_exact_schema']=set(rows[0])==set(schema_literals[kind+'_ROW'])
        e['header_columns']=len(rows[0])
        keys=('half_cell','si','w_dqdv') if kind=='MATRIX' else ('gamma_Si',) if kind=='PROFILE' else ('state',)
        e['old_new_ordered_row_identity_equal']=[tuple(r[k] for k in keys) for r in oldrows]==[tuple(r[k] for k in keys) for r in rows]
        e['roster_rows_match']=m.get('roster',{}).get('rows')==len(rows)
        e['added_columns']=sorted(set(rows[0])-set(oldrows[0])) if rows and oldrows else []
        n=0;ds=[]
        if len(rows)!=len(oldrows):ds.append(['row_count',len(oldrows),len(rows)])
        for i,(a,b) in enumerate(zip(oldrows,rows)):
            for k in a.keys()&b.keys():
                if k in {'run_id','inputs_sha','ref_inputs_sha'}:continue
                av=num(a[k]);bv=num(b[k])
                if av is not None and bv is not None:
                    n+=1
                    if av!=bv:ds.append([i,k,a[k],b[k]])
        e['shared_numeric_cells']=n;e['shared_numeric_differences']=ds
    else:
        b=json.loads(body);a=json.loads(prior);n,ds=recursive_numeric(a,b)
        e['required_schema_keys_present']=all(k in b for k in schema_literals['DEGENERACY_KEYS'])
        e['run_ids_match']=b.get('run_id')==m['run_id'];e['shared_numeric_leaves']=n;e['shared_numeric_differences']=ds
        e['roster']=m.get('roster')
    numeric_total+=n;numeric_diff.extend([(p.name,d) for d in ds]);artifacts.append(e)
print('ARTIFACTS',json.dumps(artifacts,ensure_ascii=False))
print('SUMMARY',json.dumps({'artifact_count':len(artifacts),'commits':commits,'env_variants':len(envs),'shared_numeric_compared':numeric_total,'numeric_diff_count':len(numeric_diff),'raw_input_exists_not_tested':True},ensure_ascii=False))
shape=json.loads((root/'out/ne_shape_GITT_Li.csv.meta.json').read_bytes())
links=[]
for state,v in shape['consumed_inputs'].items():
    if 'matrix' not in v:continue
    ref=v['matrix'];target=root/'out'/Path(ref['file']).name;rows=list(csv.DictReader(target.open()))
    selected=rows[ref['row']['index']]
    links.append({'state':state,'matrix_hash_matches':sha(target.read_bytes())==ref['sha256'],'row_fields_match':all(selected[k]==str(value) for k,value in ref['row'].items() if k!='index')})
print('SHAPE_MATRIX_BINDING',json.dumps(links))
