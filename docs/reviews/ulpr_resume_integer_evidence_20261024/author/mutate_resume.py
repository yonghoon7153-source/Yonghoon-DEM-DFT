"""Run isolated RESUME guard mutations against resident R39; --repo/--out portable."""
import argparse,contextlib,hashlib,io,json,pathlib,sys,traceback,types
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);a=p.parse_args()
kit=pathlib.Path(a.repo).resolve()/'docs/data/ps45_unload_20261009';out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(kit));src=(kit/'ul_reader.py').read_text()
specs=[
 ('round_event_before_validation',"index = _resume_integer if r['event'] == 'RESUME' else _i","index = _i"),
 ('truncate_decimal',"v.is_finite() and v == v.to_integral_value()","v.is_finite()"),
 ('allow_unicode_digits',"[0-9]",r"\d"),
 ('last_state_definition_wins',"key not in out and len(w) == 4","len(w) == 4"),
 ('ignore_bad_manifest',"if pr or not rf:","if not rf:"),
 ('ignore_ambiguous_event',"if any(e['event'] == 'RESUME' and (e['k'] is None or e['step'] is None) for e in events):","if False:"),
 ('normalize_state_whitespace',' and ascii_space else None',' else None'),
 ('ignore_unicode_manifest_prefix',"elif ln.strip().startswith('resume_from='):","elif line.startswith('resume_from='):"),
 ('split_unicode_state_lines',"open(path, encoding='utf-8', errors='replace').read().split('\\n')","open(path, encoding='utf-8', errors='replace').read().splitlines()"),
 ('split_unicode_manifest_lines',"open(man, encoding='utf-8', errors='replace').read().split('\\n')","open(man, encoding='utf-8', errors='replace').read().splitlines()"),
 ('ignore_event_csv_structure',"auth, apr = ([], []) if pr else _resume_auth(d, events)","auth, apr = _resume_auth(d, events)"),
]
results=[]
for name,old,new in specs:
 if name=='allow_unicode_digits':
  old="r'\\+?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?'";new=old.replace('[0-9]',r'\d')
 assert src.count(old)==1,(name,src.count(old));mut=src.replace(old,new,1);mp=out/(name+'.py');mp.write_text(mut)
 mod=types.ModuleType('mutant_'+name);mod.__file__=str(kit/'ul_reader.py');buf=io.StringIO();failures=[];counts=[0,0];error=None
 def chk(label,test,extra=''):
  ok=test();counts[0 if ok else 1]+=1;print(('PASS ' if ok else 'FAIL ')+label+' '+extra)
  if not ok:failures.append(label)
 try:
  exec(compile(mut,mod.__file__,'exec'),mod.__dict__)
  with contextlib.redirect_stdout(buf):mod._resume_integer_tests(chk,mod.ul_lib.load_params())
 except Exception:error=traceback.format_exc()
 (out/(name+'.log')).write_text(buf.getvalue()+(error or ''));rec=dict(name=name,passed=counts[0],failed=counts[1],failures=failures,error=error,killed=bool(failures) and error is None,mutant_sha256=hashlib.sha256(mp.read_bytes()).hexdigest());results.append(rec);print(json.dumps(rec,ensure_ascii=False),flush=True)
(out/'results.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.encode()).hexdigest(),script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),mutations=results),ensure_ascii=False,indent=2))
raise SystemExit(not all(x['killed'] for x in results))
