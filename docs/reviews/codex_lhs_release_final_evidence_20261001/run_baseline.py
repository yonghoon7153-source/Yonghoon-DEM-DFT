import concurrent.futures,hashlib,json,os,pathlib,subprocess,sys,time
R=pathlib.Path(__file__).resolve().parent; S=R/'snapshot'; O=R/'evidence';O.mkdir(exist_ok=True)
env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R.parent/'lhs_coverage_review_20260930/deps'))
names=['lhs_design_dataset','lhs_descriptor_harvest','lhs_webapp_batch','lhs_perc_audit','lhs_contact_audit','analyze_contacts','lhs_release_build']
def run(name):
    t=time.monotonic()
    try:
        p=subprocess.run([sys.executable,'scripts/'+name+'.py','--selftest'],cwd=S,env=env,capture_output=True,text=True,encoding='utf-8',timeout=180)
        log=p.stdout+p.stderr;(O/(name+'_selftest.log')).write_text(log,encoding='utf-8')
        return {'name':name,'rc':p.returncode,'seconds':round(time.monotonic()-t,2),'tail':log.splitlines()[-5:]}
    except subprocess.TimeoutExpired: return {'name':name,'timeout':180}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    result=list(ex.map(run,names))
(O/'baseline.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
