"""Receiver-owned bounded checks: no science fit, COMSOL, or source-tree writes."""
from __future__ import annotations
import hashlib, json, os, pathlib, shutil, subprocess, sys, time

OUT = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path('C:/Users/Administrator/Documents/Codex/g70_20260924')
DD = REPO / 'degradation-degeneracy'
HEAD = '8568f782db3acbf00d872ce5527147258c00bec7'
CODE = 'f0dfaff3bea1e1caedcd7a34275e908284cc2d4f'
BASE = 'e6ddcd1efb7df4be69849a4fd5b59c43cccff873'
SCOPE = ['src','tools','configs','scripts','run.sh','requirements*.txt']
def sha(b): return hashlib.sha256(b).hexdigest()
def save(name, obj):
    p = OUT / name; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def git(*args): return subprocess.check_output(['git', *args], cwd=REPO)
def run(name, argv, cwd, env=None, timeout=240):
    start=time.monotonic()
    p=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,timeout=timeout)
    (OUT/(name+'.stdout.bin')).write_bytes(p.stdout)
    (OUT/(name+'.stderr.bin')).write_bytes(p.stderr)
    row={'argv':list(map(str,argv)), 'cwd':str(cwd), 'rc':p.returncode,
         'seconds':time.monotonic()-start, 'stdout_sha256':sha(p.stdout), 'stderr_sha256':sha(p.stderr)}
    save(name+'.json',row);print(json.dumps(row,ensure_ascii=True),flush=True)
    return p
def identity():
    assert git('rev-parse','HEAD').decode().strip()==HEAD
    row={'head':HEAD,'code_target':CODE,'base_review':BASE,
         'status_before':git('status','--porcelain=v1').decode(), 'python':sys.version,
         'executable':sys.executable}
    assert not row['status_before']
    req=pathlib.Path('C:/Users/Administrator/Downloads/GATE70_REQUEST.md').read_bytes()
    blob=git('show',HEAD+':degradation-degeneracy/docs/22p_gap/GATE70_REQUEST.md')
    (OUT/'GATE70_REQUEST_RECEIVED.md').write_bytes(req)
    (OUT/'GATE70_REQUEST_GIT_BLOB.md').write_bytes(blob)
    (OUT/'SEND_GATE70_RECEIVED.md').write_bytes(pathlib.Path('C:/Users/Administrator/Downloads/SEND_GATE70_2026-09-24.md').read_bytes())
    row.update(request_raw_equal=req==blob, request_received_sha256=sha(req), request_blob_sha256=sha(blob))
    for name,args in {
        'RUN_SCOPE_DIFF':['-C',str(DD),'diff',BASE,HEAD,'--',*SCOPE],
        'CODE_TO_HEAD_SCOPE':['-C',str(DD),'diff',CODE,HEAD,'--',*SCOPE],
        'RUN_SCOPE_HISTORY':['-C',str(DD),'log','-6','--format=%H %s',HEAD,'--',*SCOPE],
        'TARGET_HISTORY':['log','-8','--format=%H %s',HEAD],
        'RECEIPT_CHANGE':['diff',CODE,HEAD,'--','degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml','degradation-degeneracy/docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml'],
    }.items():
        data=git(*args);(OUT/(name+'.txt')).write_bytes(data)
        row[name]={'bytes':len(data),'sha256':sha(data)}
    protected={}
    for raw in git('ls-files','-z','degradation-degeneracy').split(b'\0'):
        if raw:
            rel=raw.decode();p=REPO/rel
            protected[rel]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
    save('SOURCE_BEFORE.json',protected)
    save('IDENTITY.json',row)
    r=run('source_digest',[sys.executable,'-X','utf8','-B','-c','from src.io import source_digest; print(source_digest())'],DD,os.environ.copy())
    assert r.returncode==0
    print(json.dumps({k:v for k,v in row.items() if k!='python'},ensure_ascii=True),flush=True)
def synthetic():
    root=pathlib.Path('C:/Users/Administrator/Documents/Codex/g70_synthetic_checks')
    root.mkdir(exist_ok=False)
    tree=root/'degradation-degeneracy';tree.mkdir()
    copied={}
    # Code/tests plus top-level contract data only; no historical result trees.
    for folder in ['src','tools','configs','scripts','tests']:
        shutil.copytree(DD/folder,tree/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for p in DD.glob('requirements*.txt'):shutil.copy2(p,tree/p.name)
    for name in ['run.sh','.gitattributes','.gitignore']:
        if (DD/name).exists():shutil.copy2(DD/name,tree/name)
    gap=tree/'docs/22p_gap';gap.mkdir(parents=True)
    for p in (DD/'docs/22p_gap').iterdir():
        if p.is_file() and p.suffix in {'.py','.yaml','.yml','.json'}:shutil.copy2(p,gap/p.name)
    for p in tree.rglob('*'):
        if p.is_file():copied[p.relative_to(tree).as_posix()]=sha(p.read_bytes())
    save('SYNTHETIC_COPY.json',{'path':str(tree),'files_sha256':copied,
        'historical_registry_not_copied':True,'conftest_disabled':True,
        'fixture_class_records_are_new_synthetic_only':True})
    e=os.environ.copy();e.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',TEMP=str(root),TMP=str(root))
    for k in ['PYTEST_ADDOPTS','PYTEST_PLUGINS','PYTEST_CURRENT_TEST']:e.pop(k,None)
    nodes=['tests/test_compare.py::test_f50b_start_file_check_ignores_git_commit_like_the_run_check',
           'tests/test_compare.py::test_dirty_scope_ignores_unrelated_subproject',
           'tests/test_compare.py::test_dirty_scope_bypasses_are_closed',
           'tests/test_io_bookkeeping.py::test_source_digest_covers_full_run_scope',
           'tests/test_io_bookkeeping.py::test_run_scope_matcher_shared_with_digest',
           'tests/test_io_bookkeeping.py::test_scope_exclusion_helper_is_shared',
           'tests/test_io_bookkeeping.py::test_tracked_dirty_is_conservative_for_excluded_paths']
    opts=['--noconftest','-q','-p','no:cacheprovider','--json-report']
    r=run('focused',[sys.executable,'-X','utf8','-B','-m','pytest',*nodes,*opts,'--json-report-file='+str(OUT/'focused.pytest.json')],tree,e)
    # Controlled reversal of exactly the new comparison tuple, never the target repo.
    if r.returncode==0:
        p=tree/'src/io.py';original=p.read_bytes()
        old=b'sdiff = sorted(k for k in ("source_digest", "git_dirty",'
        new=b'sdiff = sorted(k for k in ("source_digest", "git_commit", "git_dirty",'
        assert original.count(old)==1
        p.write_bytes(original.replace(old,new,1))
        save('F50B_REVERSAL.json',{'source':str(p),'before_sha256':sha(original),'after_sha256':sha(p.read_bytes()),'replacement_count':1,'target_repo_modified':False})
        run('f50b_reversal',[sys.executable,'-X','utf8','-B','-m','pytest',nodes[0],*opts,'--json-report-file='+str(OUT/'f50b_reversal.pytest.json')],tree,e)
    print('Synthetic checks finished; artifacts retained, target untouched.',flush=True)
if __name__=='__main__':
    {'identity':identity,'synthetic':synthetic}[sys.argv[1]]()
