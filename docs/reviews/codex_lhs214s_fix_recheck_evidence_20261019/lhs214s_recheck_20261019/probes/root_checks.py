"""Pin, seal, registration, and small unchanged-policy checks. No production edits."""
from pathlib import Path
import difflib, hashlib, json, os, sys, tempfile, contextlib, time, subprocess
R=Path(__file__).resolve().parents[1]; W=R.parent; O=R/'evidence'
BASE=W/'lhs214rr_recheck_20261019'
mode=sys.argv[1] if len(sys.argv)>1 else 'metadata'
which=sys.argv[2] if len(sys.argv)>2 else 'new'
S=(R if which=='new' else BASE)/'source'
deps=[W/'lhs_coverage_review_20260930/deps',W/'gen2_network_reverify3_20261007/deps',BASE/'deps']
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONPATH=os.pathsep.join(map(str,deps)),TEMP=str(R/'tmp'),TMP=str(R/'tmp'))
sys.path[:0]=list(map(str,[S/'scripts',S/'webapp',*deps]));sys.dont_write_bytecode=True;tempfile.tempdir=str(R/'tmp')
def read(p):
    st=str(p)
    return Path('\\\\?\\'+st).read_bytes() if os.name=='nt' and not st.startswith('\\\\?\\') else p.read_bytes()
def sha(p):return hashlib.sha256(read(p)).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def metadata():
    import supp20_input_receipt as sr
    old=json.loads(read(BASE/'source_manifest.json'));new=json.loads(read(R/'source_manifest.json'))
    a={v['path']:v for v in old['files']};b={v['path']:v for v in new['files']}
    changed=json.loads(read(O/'tree_diff.json'))['changed']
    seal=[dict(path=p,old=sha(BASE/'source'/p),new=sha(S/p)) for p in sr.NP.CODE_FILES]
    hand=[dict(path=p,old=sha(BASE/'source'/p),new=sha(S/p)) for p in sr.NP.HANDOVER_FILES]
    diff={}
    for p in changed:
        if p.startswith(('scripts/','webapp/')):
            prev=read(BASE/'source'/p).decode('utf8') if p in a else ''
            curr=read(S/p).decode('utf8')
            diff[p]=''.join(difflib.unified_diff(prev.splitlines(True),curr.splitlines(True),fromfile='77d8fd445/'+p,tofile='685c2bbdb/'+p))
    save('root_code_diff.json',diff)
    req=read(R/'submitted/codex_lhs214s_fix_recheck_request_20261019_send.md').decode('utf8').splitlines()
    repo_req=read(S/'docs/reviews/codex_lhs214s_fix_recheck_request_20261019.md').decode('utf8').splitlines()
    reqdelta=list(difflib.unified_diff(repo_req,req,fromfile='repo',tofile='sent'))
    result=dict(pin=new['pin'],source_files=len(new['files']),changed_code=list(diff),seal_count=len(seal),seal=seal,seal_same=all(x['old']==x['new'] for x in seal),handover_same=all(x['old']==x['new'] for x in hand),handover=hand,fp=sr.NP.code_fp(sr.NP.code_hashes()),registration=sr.registration_values(),sent_request_delta=reqdelta)
    save('root_metadata.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('seal','handover','registration','sent_request_delta')},ensure_ascii=False))
def receipt():
    import supp20_input_receipt as sr
    # Extracted snapshot has no git checkout. Supply only that fact, never a clean approval.
    sr.NP.git_info=lambda:dict(sha=None,branch=None,dirty=None)
    rec=sr.receipt()
    save('root_receipt_'+which+'.json',rec)
    print(json.dumps(dict(which=which,rc=rec['rc'],bad=[c['id'] for c in rec['checks'] if not c['ok']],registration=rec['registration']),ensure_ascii=False))
def regression():
    tasks=['scripts/test_l214r_r04_cf_label.py','webapp/test_pipeline_provenance.py']
    results=[]
    for rel in tasks:
        if not (S/rel).exists():
            results.append(dict(path=rel,skipped='path absent'));continue
        start=time.monotonic();p=subprocess.run([sys.executable,'-X','utf8','-B',str(S/rel)],cwd=S,capture_output=True,timeout=600)
        (O/('root_reg_'+Path(rel).stem+'.log')).write_bytes(p.stdout+p.stderr)
        results.append(dict(path=rel,rc=p.returncode,seconds=time.monotonic()-start,tail=p.stdout.decode('utf8','replace').splitlines()[-5:]))
        save('root_regressions.json',results);print(json.dumps(results[-1],ensure_ascii=False),flush=True)
if __name__=='__main__':globals()[mode]()
