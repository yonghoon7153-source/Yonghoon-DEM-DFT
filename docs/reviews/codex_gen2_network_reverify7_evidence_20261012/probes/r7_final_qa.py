from pathlib import Path
import hashlib,json,platform,sys,importlib.metadata
R=Path(__file__).resolve().parents[1];E=R/'evidence'
def read(name):return json.loads((E/name).read_text(encoding='utf8'))
c=read('r7_cli.json');p=read('r7_parent_cli.json')
for x in c['rows']:
    assert x['matched'] and len(x['meta'])==2
    assert x['meta'][0]['ok'] is True and x['meta'][1]['ok']==(x['expected_rc']==0),x
assert len(c['rows'])==23 and len(p['rows'])==26
assert p['all_expected'] and (p['parent_accepts'],p['current_accepts'])==(24,0)
log=(E/'reread.log').read_text(encoding='utf8')
count=sum(l.startswith('  ✓ ') for l in log.splitlines())
assert read('run_reread.json')['rc']==0 and count==26,count
m=json.loads((R/'source_manifest.json').read_text(encoding='utf8'));bad=[]
for x in m['files']:
    file=R/'source'/x['path']
    if sys.platform=='win32':file=Path('\\\\?\\'+str(file))
    if hashlib.sha256(file.read_bytes()).hexdigest()!=x['sha256']:bad.append(x['path'])
assert not bad,bad
versions={}
for pkg in ('numpy','scipy','networkx','flask','pandas','matplotlib'):
    try:versions[pkg]=importlib.metadata.version(pkg)
    except importlib.metadata.PackageNotFoundError:versions[pkg]=None
out={'source_files':len(m['files']),'source_changed_after_tests':bad,'actual_cli_23_all_meta_expected':True,
     'before_after_cli_25_mutants_all_expected':True,'reread_selftest_passes':count,
     'runtime':{'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'packages':versions},
     'limitations':['Windows has no os.wait4: smoke fast selftest aborted after 9 successful checks; no portability patch used.',
                    'smoke --selftest-real and check_all not executed in this review; no WSL, DEM/MPM, case15 full pipeline or production194 run.',
                    'case15 positive reused original 10-09 report; three normal publications use current real synthetic producer.']}
(E/'r7_final_qa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False))
