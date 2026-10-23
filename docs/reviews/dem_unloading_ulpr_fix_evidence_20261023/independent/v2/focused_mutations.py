import argparse,pathlib,sys,types,contextlib,io,json,traceback
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);a=p.parse_args();repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit));cases=[
('no_uncertain_output','ul_reader',"            out.setdefault('resume_uncertain', []).append({'k': kr, 'step': sr, 'why': why})","            pass # mutation",'R37'),
('keep_union_of_prefix','ul_reader',"        v['union_bracket_um'] = v['union_bracket_pct'] = v['nonmonotone'] = None","        pass # mutation",'R37'),
('nonfinite_box_allowed','ul_gates',"elif any(not math.isfinite(v) for axis in box for v in axis):","elif False:",'C6'),
('reversed_box_allowed','ul_gates',"elif any(lo >= hi for lo, hi in box):","elif False:",'C6')]
results=[]
for name,target,old,new,label in cases:
 source=(kit/(target+'.py')).read_text();assert source.count(old)==1,(name,source.count(old));m=types.ModuleType('independent_v2_'+name);m.__file__=str(kit/(target+'.py'));exec(compile(source.replace(old,new,1),m.__file__,'exec'),m.__dict__);buf=io.StringIO();fails=[];error=None
 def chk(name,cond,detail=''):
  try:ok=bool(cond() if callable(cond) else cond)
  except Exception as e:ok=False;detail=repr(e)
  if not ok:fails.append(name+' '+detail)
 try:
  with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
   if target=='ul_reader':m._ulpr_resume_tests(chk,m.ul_lib.load_params())
   else:m.selftest()
 except Exception:error=traceback.format_exc()
 if target=='ul_gates':fails=[ln.strip() for ln in buf.getvalue().splitlines() if '✗' in ln]
 relevant=[ln for ln in fails if label in ln];rec={'name':name,'error':error,'failures':fails,'relevant_failures':relevant,'killed_for_expected_reason':bool(relevant) and error is None};results.append(rec);(out/(name+'.log')).write_text(buf.getvalue()+'\n'.join(fails)+(error or ''));print(name,len(relevant),error)
(out/'focused_mutations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
