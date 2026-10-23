"""Independent direct canonical-reader attacks. Writes only --out fixtures/results."""
from pathlib import Path
import argparse, ast, contextlib, hashlib, json, subprocess, sys
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser(description='Independent ULPR reader attacks; --repo is the baseline Git repository, --work is the candidate repository/export.');ap.add_argument('--repo',required=True);ap.add_argument('--work',required=True);ap.add_argument('--out',required=True);ap.add_argument('--reader-sha',required=True);a=ap.parse_args()
work=Path(a.work);out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
kit=work/'docs/data/ps45_unload_20261009'; repo=Path(a.repo);base='8347d32ea678c0174bd77d4c79cfbd7b0591e4a3';rel='docs/data/ps45_unload_20261009/ul_reader.py'
sha=lambda b:hashlib.sha256(b).hexdigest(); before=(kit/'ul_reader.py').read_bytes();assert sha(before)==a.reader_sha
sys.path.insert(0,str(kit));import ul_reader as u
baseline=subprocess.check_output(['git','show',f'{base}:{rel}'],cwd=repo); old={'__file__':str(kit/'ul_reader.py'),'__name__':'baseline_reader'};exec(compile(baseline,f'{base}:{rel}','exec'),old)
P=u.ul_lib.load_params();d=Path(u._unfinished_resume(str(out/'fixture'),P));ep=d/'ul_events.csv';mp=d/'run_manifest.txt';sr=int(u.ul_lib.read_kv(str(mp))['resume_from']);sp=d/'restart'/f'state_unload_{sr}.in'
original={p:p.read_bytes() for p in [ep,mp,sp]};records=[]
def reset():
 for p,b in original.items():p.write_bytes(b)
def observe(name,expected,reader=u.read_run,expect_no_discard=True):
 raw={p.name:sha(p.read_bytes()) for p in [ep,d/'ul_steps.csv',d/'ul_windows.csv']};r=reader(str(d),P);same=all(sha((d/n).read_bytes())==h for n,h in raw.items());ok=r['resume_auth']==expected and same and (bool(expected) or not expect_no_discard or r['n_superseded_rows']==0)
 records.append({'case':name,'pass':ok,'expected_auth':expected,'actual_auth':r['resume_auth'],'superseded_rows':r['n_superseded_rows'],'csv_bytes_unchanged':same,'problems':r['problems']})
 return r

def event(field,token,duplicate=False):
 def edit(rows):
  r=next(r for r in rows if r['event']=='RESUME')
  if duplicate: rows.insert(rows.index(r),dict(r))
  r[field]=token
 u._edit_rows(str(ep),edit)
def state(key,token):
 value=3 if key=='ul_k' else sr
 sp.write_text(original[sp].decode().replace(f'variable {key} equal {value}\n',f'variable {key} equal {token}\n'))
reset();event('k','3.49');observe('baseline reproduces fractional 3.49 acceptance',[(3,sr)],old['read_run'])
reset();observe('normal',[(3,sr)])
for field,value in [('k',3),('step',sr)]:
 for token in [str(value),f'{value}.0',f'{value}e0',f'{value}E+00',f'+{value}',f'000{value}',f'{value}.',f' \t{value}\t ']:
  reset();event(field,token);observe(f'event {field} positive {token!r}',[(3,sr)])
 for token in [f'{value}.49',f'{value}.5',f'{value}.51',f'{value}.0000000000000001',f'{value-1}.9999999999999999','nan','NaN','inf','-inf','1e309','1e1000000000','1e-1000000000','','-0','-3','٣','３','3_0','\u00a03','3\u2003','3\u200b','3\x00','3\v','3\f','0'*4097+'3']:
  reset();event(field,token);observe(f'event {field} invalid {token[:60]!r} length={len(token)}',[])
 for token in ['3.49','NaN','3.0000000000000001']:
  reset();event(field,token,duplicate=True);observe(f'mixed valid/invalid event {field} {token!r}',[])
for key,value in [('ul_k',3),('ul_rstep',sr)]:
 for token in [str(value),f'{value}.0',f'{value}e0',f'+{value}',f'\t{value}\t']:
  reset();state(key,token);observe(f'state {key} positive {token!r}',[(3,sr)])
 for token in [f'{value}.49',f'{value}.0000000000000001','nan','inf','1e309','1e1000000000','٣',f'\u00a0{value}',f'{value}\u202f',f'{value}\u0085#tail',f'{value}\u2028#tail',f'{value}\u2029#tail',f'{value}\v#tail',f'{value} extra']:
  reset();state(key,token);observe(f'state {key} invalid {token!r}',[])
 for suffix in [f'variable {key} equal {value}\n',f'variable {key} equal {value+1}\n',f'variable {key} equal bad\n',f'variable {key} equal {value}\nvariable {key} equal {value}\n']:
  reset();sp.write_bytes(original[sp]+suffix.encode());observe(f'state {key} duplicate {suffix!r}',[])
for token in [f'{sr}.0',f'{sr}.49','nan','',str(sr)+'\u00a0','٣','1e309','0'*4097+str(sr)]:
 reset();mp.write_bytes(original[mp]+f'resume_from={token}\n'.encode());observe(f'manifest mixed malformed {token[:60]!r} length={len(token)}',[])
for sep in ['\u00a0','\u2003','\u0085','\u2028','\u2029','\v','\f']:
 reset();mp.write_bytes(original[mp]+f'{sep}resume_from=3.49\n'.encode());observe(f'manifest malformed prefix {sep!r}',[])
 reset();mp.write_bytes(original[mp]+f'resume_from={sr}{sep}#tail\n'.encode());observe(f'manifest malformed suffix {sep!r}',[])
for lineend in ['\r\n','\r']:
 reset();sp.write_bytes(original[sp].decode().replace('\n',lineend).encode());mp.write_bytes(original[mp].decode().replace('\n',lineend).encode());observe(f'state+manifest {lineend!r} positive',[(3,sr)])
for sep in ['\u0085','\u2028','\u2029']:
 reset();event('k','3'+sep+'.49',duplicate=True);observe(f'mixed event Unicode separator {sep!r}',[])
# Exact identity at the first float-unrepresentable adjacent integer; no claim that the synthetic steps use this k.
for state_k,expect in [(2**53+1,[(2**53+1,sr)]),(2**53,[])]:
 reset();state('ul_k',str(state_k));event('k',str(2**53+1));observe(f'large exact identity state {state_k}',expect)
reset();observe('normal after all negative attacks',[(3,sr)])
# No broad parser rewrite: top-level function AST differences are explicitly enumerated.
def functions(b):
 return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
f0,f1=functions(baseline),functions(before);changed=sorted(k for k in f0.keys()&f1.keys() if f0[k]!=f1[k]);added=sorted(f1.keys()-f0.keys());same_i=f0['_i']==f1['_i'];same_csv=f0['_csv']==f1['_csv']
manifest=[]
for line in (kit/'SHA256SUMS').read_text().splitlines():
 h,name=line.split(None,1);name=name.lstrip('*');p=kit/name;manifest.append({'path':name,'match':p.is_file() and sha(p.read_bytes())==h})
with (out/'canonical_reader_selftest.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):rc=u.selftest()
log=(out/'canonical_reader_selftest.log').read_text();after=(kit/'ul_reader.py').read_bytes()
result={'status':'PASS' if all(x['pass'] for x in records) and rc==0 and all(x['match'] for x in manifest) and before==after and same_i and same_csv else 'FAIL','base':base,'reader_sha256':sha(before),'reader_unchanged_during_test':before==after,'cases':records,'case_count':len(records),'passed':sum(x['pass'] for x in records),'failed':sum(not x['pass'] for x in records),'canonical_selftest':{'rc':rc,'pass':sum(l.startswith('  ✓ ') for l in log.splitlines()),'fail':sum(l.startswith('  ✗ ') for l in log.splitlines()),'log_sha256':sha(log.encode())},'existing_functions_changed':changed,'new_functions':added,'general_i_unchanged':same_i,'general_csv_unchanged':same_csv,'kit_manifest':manifest}
(out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('cases','kit_manifest')},ensure_ascii=False,indent=2));sys.exit(0 if result['status']=='PASS' else 1)
