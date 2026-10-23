from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
KIT=Path('/workspace/.cloud-setup/nonrint-20261024/ulpr/work/docs/data/ps45_unload_20261009');OUT=Path('/workspace/.cloud-setup/nonrint-20261024/audit/ulpr/lexical-v2-linebreak');OUT.mkdir(exist_ok=False)
sys.path.insert(0,str(KIT));import ul_reader as u
P=u.ul_lib.load_params();d=Path(u._unfinished_resume(str(OUT/'fixture'),P));m=d/'run_manifest.txt';ev=d/'ul_events.csv';man=m.read_text();sr=int(u.ul_lib.read_kv(str(m))['resume_from']);state=d/'restart'/f'state_unload_{sr}.in';old=state.read_text();results=[]
def save(name):
 r=u.read_run(str(d),P);results.append({'case':name,'resume_auth':r['resume_auth'],'superseded':r['n_superseded_rows'],'problems':r['problems'],'state_vars':u._state_vars(str(state))})
save('normal')
for key,val in [('ul_k',3),('ul_rstep',sr)]:
 for space in ['\u0085','\u2028','\u2029']:
  state.write_text(old.replace(f'variable {key} equal {val}\n',f'variable {key} equal {val}{space}#tail\n'))
  save(key+'_suffix_linebreak_U'+format(ord(space),'04X'))
state.write_text(old)
for prefix in ['\u0085','\u2028','\u2029']:
 m.write_text(man+f'resume_from={sr}'+prefix+'#tail\n');save('manifest_bad_mark_prefix_U'+format(ord(prefix),'04X'))
m.write_text(man)
(OUT/'results.json').write_text(json.dumps({'reader_sha256':hashlib.sha256((KIT/'ul_reader.py').read_bytes()).hexdigest(),'cases':results},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
