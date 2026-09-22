"""Exercise _execution_receipt itself, with original ROOT and unchanged target files."""
from pathlib import Path
import argparse,json,os,sys
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--sandbox',type=Path,help='Existing upstream replay sandbox, read only')
a=p.parse_args()
a.repo=a.repo.resolve();a.out=a.out.resolve()
a.out.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(a.repo/'docs/22p_gap'))
import mutation_replay as mr
assert mr.ROOT==a.repo
initial=os.getcwd()
original_env=mr.replay_env
records=[]
cases=['explicit_import','relative_caller_only']
if a.sandbox:
    cases.append('relative_from_repo_with_real_sandbox')
for case in cases:
    d=a.out/case;d.mkdir()
    s=d/'startup';s.mkdir()
    (s/'sitecustomize.py').write_text('import usercustomize\n' if case=='explicit_import' else '# caller startup; not on replay cwd path\n',encoding='utf-8')
    (s/'usercustomize.py').write_text('VALUE = 42\n',encoding='utf-8')
    if case=='relative_from_repo_with_real_sandbox':
        mr.SANDBOX=a.sandbox.resolve()
        os.environ['PYTHONPATH']=os.path.relpath(s,a.repo)
        os.chdir(a.repo)
    else:
        os.environ['PYTHONPATH']=str(s) if case=='explicit_import' else 'startup'
        os.chdir(d)
    rec={'case':case,'ROOT':str(mr.ROOT),'cwd':os.getcwd(),'sandbox':str(mr.SANDBOX) if mr.SANDBOX else None,'pythonpath':os.environ['PYTHONPATH']}
    # Real replay_env is unchanged. Use normal venv (user site disabled) for N1.
    try:
        raw=mr._observed_receipt()
        mr._assert_receipt_is_complete(raw)
        rec['receipt_complete']=True
        rec['customization']=raw['startup']['customization']
        rec['enabled']=mr._parent_user_site_enabled()
        rec['parent']=mr._parent_customization_view()
        try:
            mr._execution_receipt()
            rec['entry_result']='ACCEPTED'
        except Exception as e:
            rec['entry_result']='REJECTED';rec['error']=f'{type(e).__name__}: {e}'
    except Exception as e:
        rec['diagnostic_error']=f'{type(e).__name__}: {e}'
    finally:
        os.chdir(initial)
        mr.SANDBOX=None
    records.append(rec)
(a.out/'observations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for r in records: print(json.dumps(r,ensure_ascii=False))
