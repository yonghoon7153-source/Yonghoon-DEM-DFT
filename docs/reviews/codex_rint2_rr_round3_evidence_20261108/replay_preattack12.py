"""Replay submitted F1-F5 fixtures through current code. No real runner.
Disclosed Windows adaptations: regular-file O_NONBLOCK=0; /proc identity and
group emptiness fixtures; sequential ledger lock; safe.directory per scratch.
The repository remains unmodified. This is not Linux field qualification.
"""
import contextlib, hashlib, io, json, os, re, subprocess, sys, tempfile, types
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root/'package/repo'
src=repo/'docs/reviews/rint2_rr2_fix_evidence_20261105/preattack12'
out=root/'preattack12_replay';out.mkdir(exist_ok=True)
scratch=out/'scratch';scratch.mkdir(exist_ok=True)
os.environ['TEMP']=os.environ['TMP']=str(root/'temp')
tempfile.tempdir=str(root/'temp')
os.O_NONBLOCK=getattr(os,'O_NONBLOCK',0)
sys.path.insert(0,str(repo/'scripts'))
import rint_r_chain as R
import test_rint_r_chain as T
fixture_root=scratch/'fixture_source_root';fixture_root.mkdir(exist_ok=True)
(fixture_root/'.gitignore').write_bytes((root/'remote_gitignore').read_bytes())
T.ROOT=fixture_root # only .gitignore lookup; pinned SCRIPTS/REG_DOC remain unchanged
HOST={'machine_id':'review-machine','boot_id':'review-boot','pidns':'pid:[review]'}
R.host_ident=lambda:dict(HOST)
R.proc_stat=lambda pid:None
R.group_members=lambda *a,**k:[]
R.group_settle=lambda *a,**k:(True,[])
@contextlib.contextmanager
def unlocked(*a,**k): yield
R.ledger_lock=unlocked
rawrun=subprocess.run
def git_safe(argv,*a,**k):
    if isinstance(argv,list) and argv[:2]==['git','-C'] and Path(argv[2]).resolve().is_relative_to(scratch.resolve()):
        argv=argv[:3]+['-c','safe.directory='+str(Path(argv[2]).resolve()).replace('\\','/')]+argv[3:]
    return rawrun(argv,*a,**k)
subprocess.run=git_safe
hs=(src/'harness.py').read_text(encoding='utf-8')
hs=hs.replace("sys.path.insert(0, '/home/user/Yonghoon-DEM-DFT/scripts')",'sys.path.insert(0, '+repr(str(repo/'scripts'))+')')
hs=re.sub(r"SCR = Path\([^\n]+\)", 'SCR = Path('+repr(str(scratch)).replace('\\','/')+')', hs)
hs=hs.replace("f = Path(T.TD) / 'syn' / tag / 'attempt_1'", "f = Path(T.TD) / 'syn' / ''.join(c if c not in '<>:\"/\\\\|?*' else '_' for c in tag) / 'attempt_1'")
(out/'harness_adapted.py').write_text(hs,encoding='utf-8')
h=types.ModuleType('harness');h.__file__=str(out/'harness_adapted.py');exec(compile(hs,h.__file__,'exec'),h.__dict__);sys.modules['harness']=h
rows=[]
for name in ['p1_outdir_coedit.py','p2_real_ledger.py','p4_tl_none_after_fail.py','p5_misc_b.py','p6_rejected.py']:
    text=(src/name).read_text(encoding='utf-8')
    buf=io.StringIO();error=None
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
        try:exec(compile(text,str(src/name),'exec'),{'__name__':'__main__','__file__':str(src/name)})
        except Exception as e:
            import traceback
            error=repr(e);traceback.print_exc()
    (out/(name+'.log')).write_text(buf.getvalue(),encoding='utf-8')
    rows.append({'probe':name,'source_sha256':hashlib.sha256((src/name).read_bytes()).hexdigest(),'error':error})
    print(name,error or 'completed')
    if name=='p5_misc_b.py':
        # New strict reader correctly returns None; let the rest of original
        # diagnostic print execute without changing any eligibility expectation.
        text=text.replace("s['runs'][0]['arms'], s['runs'][0]['outdir']", "s['runs'][0]['arms'] if s else None, s['runs'][0]['outdir'] if s else None")
        buf=io.StringIO();error=None
        with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
            try:exec(compile(text,str(src/name),'exec'),{'__name__':'__main__','__file__':str(src/name)})
            except Exception as e:
                import traceback
                error=repr(e);traceback.print_exc()
        (out/'p5_none_safe.log').write_text(buf.getvalue(),encoding='utf-8')
        rows.append({'probe':'p5_none_safe','change':'print only: guard two None subscripts; eligibility unchanged','error':error})
        print('p5_none_safe',error or 'completed')
(out/'replay_metadata.json').write_text(json.dumps({'pin':'17d45fb9cdfc7033bdfd41509527cea23ba1654c','python':sys.version,'rows':rows,'adaptations':['paths and Windows filename sanitization only','O_NONBLOCK=0 regular files','synthetic host/proc/groups','sequential ledger lock','per scratch Git safe.directory'],'research_runs':0,'linux_qualification':False},ensure_ascii=False,indent=2),encoding='utf-8')
