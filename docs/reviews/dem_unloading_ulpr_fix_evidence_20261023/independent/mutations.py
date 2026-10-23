import argparse,pathlib,sys,types,contextlib,io,json,traceback
ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit))
import ul_gates,ul_reader
specs=[
 ('no_resume_reconcile','ul_reader','    _resume_reconcile(out, auth, used_rows, rewound_events, stale_windows)\n','    pass  # mutation: reconciliation omitted\n','R37'),
 ('resume_outside_manifest','ul_reader',"elif e['step'] not in rf:","elif False:",'R38'),
 ('resume_nonnumeric','ul_reader',"if e['k'] is None or e['step'] is None:","if False:",'R38'),
 ('resume_state_mismatch','ul_reader',"if st.get('ul_rstep') == s and st.get('ul_k') == ks[0]:","if True:",'R38'),
 ('event_k_guard','ul_reader',"stale and b in auth and b not in used and all(x['k'] is not None and x['k'] > e['k'] for x in stale)","stale and b in auth and b not in used",'R38'),
 ('grammar_list_guard','ul_reader',"elif listed is None or listed.get(n) != h:","elif False:",'R38'),
 ('grammar_process_rc','ul_reader'," or p.returncode != 0:",":",'R38'),
 ('g2_duplicate_id','ul_gates',"if ids is None or len(set(ids)) != len(ids):","if ids is None:",'C5'),
 ('g2_parser_ok','ul_gates',"if not d['ok']:\n        raise ValueError('; '.join(d['problems']))","if False:\n        raise ValueError('; '.join(d['problems']))",'C5'),
 ('g2_expected_step','ul_gates',"if sa != sb or (expected_step is not None and sa != expected_step):","if sa != sb:",'C5'),
 ('g2_normalize_tokens','ul_gates',"tuple(t[i] for i in idx)","tuple(str(float(t[i])) for i in idx)",'C5'),
 ('g2c_observation_status','ul_gates',"out['status'] = 'NOT_COMPUTED'   # ULPR-04","out['status'] = 'FAIL'   # ULPR-04",'C4'),
]
results=[]
for name,target,old,new,label in specs:
    p=kit/(target+'.py');source=p.read_text();assert source.count(old)==1,(name,source.count(old));mut=source.replace(old,new,1)
    mod=types.ModuleType('mutant_'+name);mod.__file__=str(p)
    buf=io.StringIO();err=None;rc=None
    try:
        exec(compile(mut,str(p),'exec'),mod.__dict__)
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf): rc=mod.selftest()
    except Exception:
        err=traceback.format_exc()
    txt=buf.getvalue();(out/(name+'.log')).write_text(txt+(err or ''))
    failures=[ln.strip() for ln in txt.splitlines() if '✗' in ln]
    relevant=[ln for ln in failures if label in ln]
    rec={'name':name,'suite':target,'rc':rc,'error':err,'failures':failures,'relevant_failures':relevant,'killed_for_expected_reason':bool(relevant) and err is None}
    results.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ['failures','error']},ensure_ascii=False),flush=True)
(out/'mutations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
