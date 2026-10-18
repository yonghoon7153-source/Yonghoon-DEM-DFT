"""Check received bytes against Git blobs and rerun received A4 without Git mutations.

Only __file__ and A4.git_bytes source provision are adapted. The received source
text, numerical functions, fixtures, assertions and comparisons are unchanged.
"""
from pathlib import Path
import contextlib,hashlib,io,json,os,sys,tarfile,tempfile,time
R=Path(__file__).resolve().parent
P=R.parent/'lhs214r_fix_recheck_20261017'
S=P/'source';B=P/'base'
X=R/'submitted/lhs214r_recheck_a4a1e52c0'
E=X/'docs/reviews/lhs214r_fix_evidence_20261016'
O=R/'evidence';(R/'tmp').mkdir(exist_ok=True)
def lp(p):return Path('\\\\?\\'+str(p.resolve())) if os.name=='nt' else p
def read(p):return lp(p).read_bytes()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
remote=json.loads((O/'remote_evidence_blobs.json').read_text(encoding='utf8'))
checks=[{'path':x['path'],'expected':x['sha'],'actual':blob(read(E/x['path']))} for x in remote['files']]
for x in checks:x['ok']=x['expected']==x['actual']
assert all(x['ok'] for x in checks)
request=X/'docs/reviews/codex_lhs214r_fix_recheck_request_20261016.md'
remotereq=json.loads((O/'remote_request_content.json').read_text(encoding='utf8'))['content'].encode('utf8')
assert read(request)==remotereq
intake=json.loads((O/'intake.json').read_text(encoding='utf8'))
prov={'git_blob_checks':checks,'request_remote_exact':True,'tracked_files':len(checks)+1,'extra_zip_files':['PIN.txt'],'intake':{k:v for k,v in intake.items() if k not in ('files','sha256sums')}}
(O/'remote_match.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2),encoding='utf8')
print('Remote byte checks PASS',len(checks)+1,flush=True)
if '--verify-only' in sys.argv:sys.exit(0)
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8',TEMP=str(R/'tmp'),TMP=str(R/'tmp'))
deps=[P.parent/'lhs_coverage_review_20260930/deps',P.parent/'gen2_network_reverify3_20261007/deps']
sys.path[:0]=[str(p) for p in [S/'scripts',S/'webapp',*deps]]
os.environ['PYTHONPATH']=os.pathsep.join(map(str,deps));sys.dont_write_bytecode=True;tempfile.tempdir=str(R/'tmp')
file=E/'a4_l214r_no_impact.py';raw=read(file)
scope={'__file__':str(S/'docs/reviews/lhs214r_fix_evidence_20261016/a4_l214r_no_impact.py'),'__name__':'received_a4_review'}
exec(compile(raw,str(file),'exec'),scope)
basepin='6cb2569569ec74b7f5a96e0ef19494e872da5272'
calls=[]
maps={k:{r['path']:r for r in json.loads(read(P/f'{k}_manifest.json'))['files']} for k in ['source','base']}
for k,root in [('source',S),('base',B)]:
    for row in maps[k].values():
        if row['path'].startswith(('scripts/','webapp/')):
            assert hashlib.sha256(read(root/row['path'])).hexdigest()==row['sha256']
changed=json.loads(read(P/'evidence/pin_resolution.json'))['script_web_changes']
def git_bytes(*args):
    calls.append(args)
    if args[0]=='show':
        ref,path=args[1].split(':',1);assert basepin.startswith(ref)
        b=read(B/path);assert hashlib.sha256(b).hexdigest()==maps['base'][path]['sha256'];return b
    if args[:3]==('archive','--format=tar','6cb256956'):
        assert args[3:]==('webapp','scripts')
        out=io.BytesIO()
        with tarfile.open(fileobj=out,mode='w') as t:
            for path,row in sorted(maps['base'].items()):
                if path.startswith(('webapp/','scripts/')):
                    b=read(B/path);n=tarfile.TarInfo(path);n.size=len(b);n.mode=0o644;t.addfile(n,io.BytesIO(b))
        return out.getvalue()
    if args==('diff','--name-only','6cb256956','--','scripts','webapp'):
        return ('\n'.join(changed)+'\n').encode()
    raise AssertionError(('unexpected Git request',args))
scope['A4'].git_bytes=git_bytes
sys.argv=[str(file),'--base','6cb256956','--json',str(O/'received_a4_rerun.json')]
start=time.monotonic()
print('Received A4 actual rerun started',flush=True)
try:
    with (O/'received_a4_rerun.log').open('w',encoding='utf8') as f,contextlib.redirect_stdout(f),contextlib.redirect_stderr(f):
        rc=scope['main']()
finally:
    adapter={'source_sha256':hashlib.sha256(raw).hexdigest(),'received_source_unchanged':True,'file_relocation':scope['__file__'],'git_calls_supplied_by_pinned_snapshots':calls,'no_git_command_executed':True,'seconds':time.monotonic()-start,'dependencies':list(map(str,deps))}
    (O/'a4_adapter.json').write_text(json.dumps(adapter,ensure_ascii=False,indent=2),encoding='utf8')
out=json.loads((O/'received_a4_rerun.json').read_text(encoding='utf8'))
print(json.dumps({'rc':rc,'pass':sum(bool(x['identical']) for x in out['rows']),'total':len(out['rows']),'ok':out['ok'],'seconds':out['sec']},ensure_ascii=False),flush=True)
sys.exit(rc)
