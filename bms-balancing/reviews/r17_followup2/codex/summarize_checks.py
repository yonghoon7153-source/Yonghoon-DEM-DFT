"""Evidence summary from JUnit, real command logs and exact checkout identities."""
import collections, datetime, hashlib, importlib.metadata, json, pathlib, subprocess, sys, xml.etree.ElementTree as ET
H=pathlib.Path(__file__).resolve().parent
R=H.parents[1]/'work/r17-followup2-a4c311ef/bms-balancing'
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True).strip()
out={}
for name in ('focused_scoped','full_scoped'):
    p=H/(name+'.xml')
    if not p.exists():continue
    tree=ET.parse(p);counts=collections.Counter();fail=[]
    for c in tree.iter('testcase'):
        f=c.find('failure');e=c.find('error');s=c.find('skipped')
        if f is not None or e is not None:
            tag='failure' if f is not None else 'error';counts[tag]+=1
            q=f if f is not None else e
            fail.append({'name':c.get('name'),'classname':c.get('classname'),'kind':tag,'message':q.get('message'),
                         'text':q.text or ''})
        elif s is not None:counts['skipped']+=1
        else:counts['passed']+=1
    groups=collections.Counter()
    for f in fail:
        t=f['text']
        if 'ModuleNotFoundError' in t and 'fcntl' in t:g='missing_fcntl'
        elif ('WinError 2' in t or 'FileNotFoundError' in t) and ('bash' in t or '/bin/' in t):g='missing_shell'
        elif 'WinError 1314' in t:g='symlink_privilege'
        elif 'WinError 123' in t or ('Invalid argument' in t and 'a -> b.csv' in t):g='invalid_windows_filename'
        elif f['name'] in ('test_git_state_can_exclude_the_artifact_being_rewritten','test_r5_11_git_provenance_classifies_quoted_non_ascii_paths'):g='path_separator_assertion'
        else:g='needs_individual_triage'
        f['coarse_group']=g;groups[g]+=1
    out[name]={'counts':dict(counts),'coarse_groups':dict(groups),'failures':fail}
    (H/(name+'_failures.json')).write_text(json.dumps(out[name],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if 'full_scoped' in out:
    prior=H.parent/'r17_followup_7c8f61f9/FULL_TEST_TRIAGE.json'
    old=json.loads(prior.read_text(encoding='utf-8'))
    oldnames={x for group in old['groups'].values() for x in group}
    newnames={x['classname']+'::'+x['name'] for x in out['full_scoped']['failures']}
    delta={'previous_triage_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),
           'previous_failures':len(oldnames),'current_failures':len(newnames),
           'newly_failing':sorted(newnames-oldnames),'no_longer_failing_this_run':sorted(oldnames-newnames),
           'remaining_unresolved':[x['classname']+'::'+x['name'] for x in out['full_scoped']['failures'] if x['coarse_group']=='needs_individual_triage']}
    (H/'FULL_TEST_DELTA.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=['reviews/R17_FOLLOWUP_RESPONSE.md','reviews/R17_RESPONSE.md','scripts/gc_partial.py','scripts/width_report.py',
       'scripts/verify_run_receipt.py','bms_balancing/verify.py','bms_balancing/cycles.py','bms_balancing/schema.py',
       'scripts/fit_cycles.py','reviews/evidence_gate.py','reviews/r11_repros/replay_codex_r11.py','tests/test_r17_followup.py']
identity={'target':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}'),'bms_fix':git('rev-parse','8733453'),
          'bms_diff_fix_to_head':git('diff','--name-only','8733453','HEAD','--','.'),'git_status':git('status','--short'),
          'python':sys.version,'packages':{n:importlib.metadata.version(n) for n in ['numpy','scipy','pandas','openpyxl','pytest']},
          'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{}}
for name in files:
    p=R/name;raw=p.read_bytes();blob=subprocess.check_output(['git','show','HEAD:./'+name],cwd=R)
    # Windows checkout CRLF can differ from committed LF; record both, not false byte equality.
    identity['files'][name]={'checkout_sha256':hashlib.sha256(raw).hexdigest(),'blob_sha256':hashlib.sha256(blob).hexdigest(),
        'exact_byte_equal':raw==blob,'lf_normalized_equal':raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')}
(H/'REVIEW_IDENTITY.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'identity':{k:v for k,v in identity.items() if k!='files'},
                  'tests':{k:{a:b for a,b in v.items() if a!='failures'} for k,v in out.items()}},ensure_ascii=True,indent=2))
