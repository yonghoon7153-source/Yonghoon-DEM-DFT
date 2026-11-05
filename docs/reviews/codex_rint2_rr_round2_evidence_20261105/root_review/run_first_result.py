import pathlib,tempfile,sys,runpy,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
scratch=ROOT/'root_review/scratch';scratch.mkdir(exist_ok=True)
tempfile.tempdir=str(scratch)
p=ROOT/'received/repo/scripts/test_rint_first_result.py'
sys.path.insert(0,str(p.parent));sys.argv=[str(p)]
# Windows child -I ignores UTF8 env; only transport encoding is forced.
# No repository file or assertion changes.
original_run=subprocess.run
def utf8_run(argv,*a,**kw):
    if isinstance(argv,list) and argv and argv[0]==sys.executable:
        argv=[argv[0],'-X','utf8']+argv[1:]
    return original_run(argv,*a,**kw)
subprocess.run=utf8_run
runpy.run_path(str(p),run_name='__main__')
