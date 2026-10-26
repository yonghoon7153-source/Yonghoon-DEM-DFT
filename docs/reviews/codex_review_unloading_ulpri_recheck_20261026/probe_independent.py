"""Independent raw-marker matrix. Synthetic arm CLI only; no DEM/MPI.
python -I -X utf8 -B probe_independent.py --repo <snapshot> --out <new dir>
"""
from pathlib import Path
import argparse,hashlib,importlib,json,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False);kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit));sys.dont_write_bytecode=True
u=importlib.import_module('ul_reader');P=u.ul_lib.load_params();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
template=out/'template';template.mkdir();d,_=u._ut_trace_arm(str(template),P,4);d=Path(d);u._fake_restored(str(template),u.B73);u._w(str(template/u.B73/'ul_base.in'),'variable ul_S2max equal 1e-05\n')
plain=u.arm_verdict(str(d),u.B73,'UT',P,root=str(template));assert plain['primary_status']=='OK';sr=u._hold_resume(str(d),P,old_nw=2,auth=True,kr=1)
cols=P['records']['events_cols'];ek=cols.index('k');base_event=(d/'ul_events.csv').read_text(encoding='utf8').splitlines();idx=next(i for i,s in enumerate(base_event) if s.split(',')[0]=='RESUME');rawrow=base_event[idx].split(',');rows=[]
def event_edit(marker,coexist,token='1'):
 def edit(arm):
  lines=list(base_event);r=list(rawrow);r[0]=marker;r[ek]=token
  if coexist:lines.append(','.join(r))
  else:lines[idx]=','.join(r)
  (arm/'ul_events.csv').write_bytes(('\n'.join(lines)+'\n').encode('utf8'))
 return edit
def capture(label,edit=None,accept=False,reason=None):
 n=len(rows);root=out/f'c{n:03}';shutil.copytree(template,root);arm=root/u.B73/'UT'
 if edit:edit(arm)
 files=[arm/f'ul_{s}.csv' for s in ('events','windows','steps')]+[arm/'run_manifest.txt',*sorted((arm/'restart').glob('state*.in'))]
 before={str(f.relative_to(root)):sha(f) for f in files};rr=u.read_run(str(arm),P)
 cmd=[sys.executable,'-I','-X','utf8','-B',str(kit/'ul_reader.py'),'arm',str(root),u.B73,'UT'];cp=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
 (root/'cli.stdout').write_bytes(cp.stdout);(root/'cli.stderr').write_bytes(cp.stderr);v=json.loads((arm/'arm_verdict.json').read_text(encoding='utf8'));after={str(f.relative_to(root)):sha(f) for f in files}
 valid=(rr['resume_auth']==[(1,sr)] and rr['n_superseded_rows']==5 and not rr['problems'] and v['primary_status']=='OK' and v['rho_pct']==plain['rho_pct'] and v['rank_eligible'] is True)
 refused=(not rr['resume_auth'] and rr['n_superseded_rows']==0 and bool(rr['problems']) and v['primary_status']=='UNIDENTIFIED' and v['rho_pct'] is None and v['rank_eligible'] is False)
 r=dict(case=n,label=label,expected='accept' if accept else 'reject',auth=rr['resume_auth'],dropped=rr['n_superseded_rows'],problems=rr['problems'],primary=v['primary_status'],rho=v['rho_pct'],rank=v['rank_eligible'],rc=cp.returncode,input_hashes=before,input_unchanged=before==after,command=cmd)
 r['pass']=(valid if accept else refused) and cp.returncode==0 and before==after and (reason is None or any(reason in x for x in rr['problems']));rows.append(r)
 (out/'result.json').write_text(json.dumps(dict(reader_sha256=sha(kit/'ul_reader.py'),python=sys.version,physical_runs=0,baseline_rho=plain['rho_pct'],cases=rows,passed=sum(x['pass'] for x in rows),total=len(rows)),ensure_ascii=False,indent=2),encoding='utf8')
 if not r['pass'] or len(rows)%25==0:print(f'{len(rows)} cases, {sum(x["pass"] for x in rows)} pass; latest={label}',flush=True)
capture('normal_stale_control',accept=True)
ws=[chr(c) for c in range(sys.maxunicode+1) if chr(c).isspace() and chr(c) not in '\r\n']
for c in ws:
 for pos in ('prefix','suffix','both'):
  token={'prefix':c+'RESUME','suffix':'RESUME'+c,'both':c+'RESUME'+c}[pos]
  for coexist in (False,True):capture(f'event_U+{ord(c):04X}_{pos}_{"coexist" if coexist else "single"}',event_edit(token,coexist),reason='ULPRI-01')
for token in ('1.49','1e-1','NaN'):capture('canonical_bad_number_'+token,event_edit('RESUME',True,token))
capture('near_marker_fractional',event_edit('\u00a0RESUME\t',True,'1.49'),reason='ULPRI-01')
for c in '\v\f\x1c\x1d\x1e\x85\u2028\u2029':
 for pos in ('prefix','suffix','hidden','unrelated'):
  text={'prefix':f'{c}resume_from={sr}.49\n','suffix':f'resume_from={sr}{c}note=old\n','hidden':f'note=old{c}resume_from={sr}.49\n','unrelated':f'note=old{c}note=new\n'}[pos]
  def edit(arm,text=text):
   m=arm/'run_manifest.txt';m.write_bytes(m.read_bytes()+text.encode())
  capture(f'manifest_U+{ord(c):04X}_{pos}',edit,reason='ULPRI-02')
for ending in ('\n','\r\n','\r'):
 def edit(arm,ending=ending):
  files=[arm/f'ul_{s}.csv' for s in ('events','windows','steps')]+[arm/'run_manifest.txt',*sorted((arm/'restart').glob('state*.in'))]
  for f in files:f.write_bytes(f.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n').replace(b'\n',ending.encode()))
 capture('all_inputs_newline_'+repr(ending),edit,accept=True)
for t in ('1.0','1e0','1.00000000000000000000000000001'):capture('exact_decimal_'+t,event_edit('RESUME',False,t),accept=t!='1.00000000000000000000000000001')
for m in ('UNKNOWN','resume'):capture('out_of_scope_'+m,event_edit(m,True),accept=True)
def restored(arm):
 f=arm/'ul_events.csv';before=f.read_bytes();event_edit('RESUME ',True)(arm);f.write_bytes(before)
capture('removed_bad_marker_control',restored,accept=True)
print(json.dumps({'total':len(rows),'passed':sum(x['pass'] for x in rows),'whitespace_codepoints':len(ws),'failed':[x['label'] for x in rows if not x['pass']]}),flush=True)
raise SystemExit(0 if all(x['pass'] for x in rows) else 1)
