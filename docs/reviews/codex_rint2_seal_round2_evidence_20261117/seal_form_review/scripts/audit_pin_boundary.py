"""Read-only git metadata, claims structure, and selected document blob identity checks."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
REPO=ROOT/'candidate_source'
PIN='64e4d213e8267bafaf3ae5af00a42996cefd3f33'
SEAL='c80d700bdd5915da82f77f839cb96ed4a5a6582e'
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
def git(*args):
    return subprocess.run(['git','-c','safe.directory='+str(REPO),'-C',str(REPO),*args],env=env,capture_output=True,check=True).stdout
out={'read_only':True,'checks':{},'unverified':[]}
def check(name,value): out['checks'][name]=bool(value); assert value,name
check('candidate_parent_is_code_pin',git('rev-parse',SEAL+'^').decode().strip()==PIN)
changed=git('diff-tree','--no-commit-id','--name-status','-r',PIN,SEAL).decode().splitlines()
out['changed_count']=len(changed)
rows=[r.split('\t') for r in changed]
out['status_counts']={s:sum(r[0]==s for r in rows) for s in ['A','M','D']}
solver=('scripts/','docs/reviews/rint2_probe6_prep_20261110/tools/','docs/data/rint2_s0_sbe_20261108/','docs/data/rint_eis_anchors.csv','docs/reviews/sdcp_gain_prereg_v2_20260816.md')
check('all_solver_boundary_paths_identical',git('diff',PIN,SEAL,'--',*solver)==b'')
sys.path.insert(0,str(ROOT/'seal_form_review/work/scripts'))
import rint_r_chain as R
check('CODE_FILES_20_identical',all(git('diff',PIN,SEAL,'--','scripts/'+p)==b'' for p in R.CODE_FILES))
check('S0_SAME_FILES_7_identical',all(git('diff',PIN,SEAL,'--','scripts/'+p)==b'' for p in R.S0_SAME_FILES))
claims='docs/reviews/claims.json'
before=json.loads(git('show',PIN+':'+claims)); after=json.loads(git('show',SEAL+':'+claims))
check('claims_status_content_unchanged',before['claims']==after['claims'])
check('claims_top_level_keys_unchanged',before.keys()==after.keys())
check('claims_all_non_ban_keys_unchanged',all(before[k]==after[k] for k in before if k!='quotation_ban'))
check('ban_entry_count_unchanged',len(before['quotation_ban'])==len(after['quotation_ban'])==42)
diff=[]
for i,(a,b) in enumerate(zip(before['quotation_ban'],after['quotation_ban'])):
    if a==b:continue
    check('ban_nonallow_fields_unchanged_'+str(i),{k:v for k,v in a.items() if k!='allowed_in'}=={k:v for k,v in b.items() if k!='allowed_in'})
    diff.append({'index':i,'added':sorted(set(b['allowed_in'])-set(a['allowed_in'])),'removed':sorted(set(a['allowed_in'])-set(b['allowed_in']))})
out['ban_allowance_changes']=diff
check('exact_two_allowances_changed',len(diff)==2)
check('only_literal_1113_1116_S0_paths_added',all(not r['removed'] and len(r['added'])==2 and all('*' not in p and p.endswith('/s0_stage1_kit_SBE_vgcf100.json') for p in r['added']) for r in diff))
out['candidate_claims_blob']=git('rev-parse',SEAL+':'+claims).decode().strip()
check('claims_declared_stoic_blob',out['candidate_claims_blob']=='3f83245436d927dc534880fa32a958bc99ce7ddf')
out['q14_blobs']={}
for path,want in [('block_manifest.json','b3e47a30d21c457136ab02b6116683e8758e899f'),('s0_preregistration.md','b0f35d9780e6babf71bf05807195f9e184a32abc')]:
    rel='docs/reviews/rint2_q14_finalpin_preparation_20261113/'+path
    got=git('rev-parse',SEAL+':'+rel).decode().strip();out['q14_blobs'][path]=got
    check('q14_blob_matches_submitted_'+path,got==want)
    check('q14_bytes_match_review_zip_'+path,git('show',SEAL+':'+rel)==(ROOT/'input/repo'/rel).read_bytes())
for rev,path,want in [('b3481336c','docs/reviews/rint2_time_reestimate_20261111/README.md','8e4781ac4e89b5968e788ed21d486824ed3fcf45'),('b3481336c','docs/reviews/rint2_time_reestimate_20261111/v3','b07ecf38e1fa620b3b9e81fc51b0f282670cfb1f')]:
    try:check('stoic_ref_'+path,git('rev-parse',rev+':'+path).decode().strip()==want)
    except subprocess.CalledProcessError:out['unverified'].append('object not locally present: '+rev+':'+path)
out['overall']='PASS locally available checks; explicit missing-object limits' if out['unverified'] else 'PASS'
print(json.dumps(out,ensure_ascii=False,indent=2))
