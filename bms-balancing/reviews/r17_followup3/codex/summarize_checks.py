"""Summarize executed reviewer evidence, not claims from the response."""
import collections,datetime,hashlib,json,pathlib,subprocess,sys,xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
H=pathlib.Path(__file__).resolve().parent;R=H.parents[1]/'work/r17-followup3-head'
def load(n):return json.loads((H/n).read_text(encoding='utf-8'))
def dump(n,o):(H/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(n,ok):checks.append(dict(name=n,observed=bool(ok)))
old=load('REPRO_RESULTS.json')['cases'];fast=load('NEW_FAST_RESULTS.json')['cases'];prod=load('NEW_PRODUCER_RESULTS.json')['cases']
ck('old case count 47',len(old)==47)
oldrc={'width_positive':0,'receipt_positive':0,'gc_control':0,'gc_old_cross_artifact':0,
 'gc_duplicate':2,'gc_cleanup_escape':2,'gc_retained_path_alias':2,'gc_unknown_file':2,'gc_unknown_dir_negative':2}
for n,v in old.items():
 if n in oldrc:ck(n,v['rc']==oldrc[n])
 elif n.startswith('width_') and 'rc' in v:ck(n,v['rc']==2)
 elif n.startswith('receipt_') and 'rc' in v:ck(n,v['rc']==3)
ck('old NaN best refuses',old['width_nan_best']['exception']=='ValueError')
p=load('PRODUCER_READER_RESULTS.json');ck('old actual producer reader rc0',p['rc']==0)
ck('old remove cycle control rc2',p['control_without_row_cycle']['rc']==2)
for n in ['gc_valid_control','gc_changed_bytes','gc_missing_retained']:ck(n,fast[n]['rc']==0)
ck('gc unindexed negative control rc2',fast['gc_unindexed_control']['rc']==2)
oldname='partial/matrix/A/matrix_100.csv';newname='partial/matrix/B/matrix_100.csv'
ck('mismatched bytes actually removed',oldname in fast['gc_changed_bytes']['before'] and oldname not in fast['gc_changed_bytes']['after'])
ck('missing retained => no payload left',oldname in fast['gc_missing_retained']['before'] and oldname not in fast['gc_missing_retained']['after'] and newname not in fast['gc_missing_retained']['after'])
ck('unindexed negative preserves full snapshot',fast['gc_unindexed_control']['before']==fast['gc_unindexed_control']['after'])
for n in ['starts1_single','starts2_single']:ck(n,prod[n]['rc']==0)
for n,k in [('starts_axis_compare','n_multistart'),('n_multistart_axis_compare','starts')]:ck(n,prod[n]['rc']==2 and k in prod[n]['stderr'])
for n in ['receipt_code_null','receipt_instrument_list']:ck(n,fast[n]['rc']==1 and 'AttributeError' in fast[n]['stderr'] and 'RUN_RECEIPT_VERIFY' not in fast[n]['stdout'])
ck('receipt positive remains rc0',fast['receipt_valid_control']['rc']==0)
ck('source of old scripts unmodified',all((H/n).read_bytes()==(H.parent/'r17_followup2_a4c311ef'/n).read_bytes() for n in ['repro_followup2.py','repro_producer_reader.py']))
dump('OBSERVATION_CHECK.json',dict(scope='Checks recorded observations only; not a product GO',passed=sum(c['observed'] for c in checks),total=len(checks),checks=checks))
assert all(c['observed'] for c in checks)

if (H/'full.xml').exists():
 tree=ET.parse(H/'full.xml');counts=collections.Counter();groups=collections.Counter();failed=[];newfile=collections.Counter()
 for c in tree.iter('testcase'):
  f=c.find('failure');e=c.find('error');s=c.find('skipped');state='passed'
  if f is not None or e is not None:
   state='failed' if f is not None else 'error';q=f if f is not None else e;t=q.text or '';name=c.get('name')
   if 'ModuleNotFoundError' in t and 'fcntl' in t:g='missing_fcntl'
   elif ('WinError 2' in t or 'FileNotFoundError' in t) and ('bash' in t or '/bin/' in t):g='missing_shell'
   elif 'WinError 1314' in t:g='symlink_privilege'
   elif 'WinError 123' in t or ('Invalid argument' in t and 'a -> b.csv' in t):g='invalid_windows_filename'
   elif name in ('test_git_state_can_exclude_the_artifact_being_rewritten','test_r5_11_git_provenance_classifies_quoted_non_ascii_paths'):g='path_separator_assertion'
   else:g='needs_individual_triage'
   groups[g]+=1;failed.append(dict(name=name,classname=c.get('classname'),group=g,message=q.get('message'),text=t))
  elif s is not None:state='skipped'
  counts[state]+=1
  if c.get('classname','').endswith('test_r17_followup2'):newfile[state]+=1
 prevpath=H.parent/'r17_followup2_a4c311ef/full_scoped_failures.json';prev=json.loads(prevpath.read_text(encoding='utf-8'))
 prevset={f['classname']+'::'+f['name'] for f in prev['failures']};curset={f['classname']+'::'+f['name'] for f in failed}
 record=dict(counts=dict(counts),new_regression_file=dict(newfile),groups=dict(groups),failures=failed,
  delta=dict(previous_failure_count=len(prevset),previous_evidence_sha256=sha(prevpath),new_failures=sorted(curset-prevset),not_failing_this_run=sorted(prevset-curset)))
 dump('TEST_RESULTS.json',record);print(json.dumps({k:v for k,v in record.items() if k!='failures'},ensure_ascii=False,indent=2))
else:print('Full pytest not yet complete; no full success claim.')
def git(*args):return subprocess.check_output(['git','-c','http.sslBackend=openssl','-C',str(R),*args]).decode('utf-8').strip()
initial=load('IDENTITY.json');changes=[]
for f in initial['files']:
 if sha(R/f['path'])!=f['sha256']:changes.append(f['path'])
final=dict(head=git('rev-parse','HEAD'),git_status=git('status','--porcelain'),changed_reviewed_files=changes,
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),old_script_identical=True,reviewed_sources={})
for rel in ['scripts/gc_partial.py','scripts/width_report.py','scripts/verify_run_receipt.py','bms_balancing/schema.py','bms_balancing/verify.py','bms_balancing/cycles.py','reviews/evidence_gate.py','tests/test_r17_followup2.py']:
 p=R/'bms-balancing'/rel;raw=p.read_bytes();blob=subprocess.check_output(['git','-c','http.sslBackend=openssl','-C',str(R),'show','HEAD:bms-balancing/'+rel])
 final['reviewed_sources'][rel]=dict(raw_sha256=sha(p),git_blob_content_sha256=hashlib.sha256(blob).hexdigest(),exact_bytes_equal=raw==blob,lf_normalized_equal=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n'))
dump('FINAL_IDENTITY.json',final);assert not changes and not final['git_status'];print('Observation checks',len(checks),'passed; reviewed code unchanged.')
