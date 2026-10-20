"""Read-only Part B review harness. Writes only review evidence/temp data.

Run from this directory's project root with the bundled Python.  Paths may be
overridden with --source; production modules are never rewritten.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, runpy, shutil, subprocess, sys, time, types

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = ROOT.parent
BASELINE = HERE/'baseline'
OLD = BASELINE/'old_join' if (BASELINE/'old_join/scripts/rint_iface_join.py').exists() else WORK/'rint_join_q7_recheck_20261020/source'
PRIOR_REVIEW = BASELINE if (BASELINE/'probes').exists() else WORK/'rint_join_q7_recheck_20261020'
EARLY = BASELINE/'early' if (BASELINE/'early/source/scripts/rint_iface_join.py').exists() else WORK/'rint_g2_impl_reverify_20261015'
DEPS = [WORK/'lhs_coverage_review_20260930/deps', WORK/'gen2_network_reverify3_20261007/deps']

def prep(src):
    sys.dont_write_bytecode = True
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        os.environ[key] = '1'
    (HERE/'tmp').mkdir(parents=True,exist_ok=True)
    for key in ('TEMP','TMP','TMPDIR'):
        os.environ[key] = str(HERE/'tmp')
    sys.path[:0] = [str(src/'scripts'),*[str(p) for p in DEPS]]
    if os.name == 'nt':
        resource = types.ModuleType('resource')
        resource.RUSAGE_SELF = 0
        resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=float('nan'))
        sys.modules['resource'] = resource
    original = shutil.rmtree
    def safe_rmtree(path,*a,**kw):
        target = Path(path).resolve()
        target.relative_to((HERE/'tmp').resolve())
        if target == (HERE/'tmp').resolve():
            raise ValueError('Refusing to remove review temp root')
        return original(target,*a,**kw)
    shutil.rmtree = safe_rmtree

def execute(args):
    src = Path(args.source).resolve()
    prep(src)
    if args.task == 'test':
        test = Path(args.test_source).resolve()/'scripts'/args.test
        virtual = src/'scripts'/args.test
        code = test.read_text(encoding='utf8')
        if args.lf_test_writer:
            before="with open(p, 'w', encoding='utf-8') as fh:"
            assert code.count(before)==1
            code=code.replace(before,"with open(p, 'w', encoding='utf-8', newline='\\n') as fh:")
        if args.loose_fixture:
            code,n=re.subn(r'^HECKEL_LOOSE_AM =.*$', 'HECKEL_LOOSE_AM = '+repr(str(Path(args.loose_fixture).resolve())).replace('\\','\\\\'),code,count=1,flags=re.M)
            assert n==1
        sys.argv = [str(virtual),*args.test_arg]
        exec(compile(code,str(virtual),'exec'),dict(__name__='__main__',__file__=str(virtual)))
    elif args.task == 'probe':
        probe = PRIOR_REVIEW/'probes'/args.test
        code = probe.read_text(encoding='utf8')
        # Path-only adaptation. Previous review arithmetic and checks unchanged.
        code = code.replace('ROOT = Path(__file__).resolve().parents[1]', 'ROOT = Path('+repr(str(HERE))+')')
        code = code.replace('WORK = ROOT.parent', 'WORK = Path('+repr(str(WORK))+')')
        code = code.replace('ROOT / "source"', 'Path('+repr(str(src))+')')
        code = code.replace('ROOT / "source/scripts"', 'Path('+repr(str(src/'scripts'))+')')
        code = code.replace('ROOT / "source/docs/data"', 'Path('+repr(str(src/'docs/data'))+')')
        code = code.replace('ROOT.parent / "rint_g2_impl_reverify_20261015"', 'Path('+repr(str(EARLY))+')')
        code = code.replace('ROOT.parent / "rint_g2_impl_reverify_20261015/source"', 'Path('+repr(str(EARLY/'source'))+')')
        code = code.replace('ROOT.parent / "rint_g2_impl_reverify_20261015/tmp/join_independent"', 'Path('+repr(str(EARLY/'tmp/join_independent'))+')')
        code = code.replace('ROOT.parent / "lhs_coverage_review_20260930/deps"', 'Path('+repr(str(DEPS[0]))+')')
        code = code.replace('ROOT.parent / "gen2_network_reverify3_20261007/deps"', 'Path('+repr(str(DEPS[1]))+')')
        sys.argv = [str(probe)]
        (HERE/'evidence').mkdir(exist_ok=True)
        (HERE/'adapted').mkdir(exist_ok=True)
        (HERE/'adapted'/args.test).write_text(code,encoding='utf8')
        exec(compile(code,str(probe),'exec'),dict(__name__='__main__',__file__=str(probe)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('task',choices=['test','probe'])
    ap.add_argument('test')
    ap.add_argument('--source',default=str(ROOT/'source'))
    ap.add_argument('--test-source',default=str(ROOT/'source'))
    ap.add_argument('--child',action='store_true')
    ap.add_argument('--lf-test-writer',action='store_true',help='Explicit test-only Windows newline adapter; production untouched.')
    ap.add_argument('--loose-fixture',help='Explicit path-only adaptation for immutable fixture outside selected old snapshot.')
    ap.add_argument('--test-arg',action='append',default=[],help='Argument passed unchanged to a reviewed selftest entry point.')
    a=ap.parse_args()
    if a.child:
        try:
            execute(a)
        finally:
            imported={}
            src=Path(a.source).resolve()
            for name,mod in list(sys.modules.items()):
                p=getattr(mod,'__file__',None)
                if not p: continue
                p=Path(p).resolve()
                try: rel=p.relative_to(src)
                except ValueError: continue
                if p.is_file(): imported[str(rel).replace('\\','/')]=hashlib.sha256(p.read_bytes()).hexdigest()
            adapter='_lf_adapter' if a.lf_test_writer else ''
            argtag=''.join('_'+re.sub(r'[^A-Za-z0-9_-]','_',x).strip('-') for x in a.test_arg)
            (HERE/'evidence'/(a.task+'_'+src.parent.name+'_'+a.test+adapter+argtag+'.imports.json')).write_text(json.dumps(imported,indent=2),encoding='utf8')
        return
    (HERE/'evidence').mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    cmd=[sys.executable,'-X','utf8','-B',str(Path(__file__).resolve()),*sys.argv[1:],'--child']
    t=time.monotonic()
    p=subprocess.run(cmd,env=env,capture_output=True,timeout=600)
    label=a.task+'_'+Path(a.source).parent.name+'_'+a.test+('_testsfrom_'+Path(a.test_source).parent.name if a.task=='test' else '')+('_lf_adapter' if a.lf_test_writer else '')
    label+=''.join('_'+re.sub(r'[^A-Za-z0-9_-]','_',x).strip('-') for x in a.test_arg)
    data=p.stdout+p.stderr
    log=HERE/'evidence'/(label+'.log')
    log.write_bytes(data)
    row=dict(command=cmd,rc=p.returncode,seconds=time.monotonic()-t,source=a.source,test_source=a.test_source,lf_test_writer_adapter=a.lf_test_writer,
             log=str(log),log_sha256=hashlib.sha256(data).hexdigest(),tail=data.decode('utf8','replace').splitlines()[-12:])
    (log.with_suffix('.json')).write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(row,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
