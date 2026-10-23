import argparse,pathlib,json,hashlib,subprocess,re,ast
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);a=p.parse_args();repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);E=repo/'docs/reviews/dem_unloading_ulpr_fix_evidence_20261023';kit=repo/'docs/data/ps45_unload_20261009';s=json.loads((E/'final/summary.json').read_text());res={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
res['final_hash_mismatch']=[x for x,h in s['working_files_sha256'].items() if not (kit/x).exists() or sha(kit/x)!=h]
logs=[]
for r in s['results']:
 t=(E/'final'/(r['name']+'.log')).read_text();oks=sum(x.lstrip().startswith('✓') for x in t.splitlines());fails=sum(x.lstrip().startswith('✗') for x in t.splitlines());rc=re.findall(r'# ── rc = (\d+) ──',t);logs.append({'name':r['name'],'ok':oks,'fail':fails,'rc':rc[-1] if rc else None,'matches_summary':oks==r['n_check_lines_ok'] and fails==r['n_check_lines_fail'] and bool(rc) and int(rc[-1])==r['rc']})
res['final_logs']=logs;res['first_test_counts']={}
for p in sorted((E/'tests_first').glob('*.log')):
 t=p.read_text();res['first_test_counts'][p.name]={'ok':sum(x.lstrip().startswith('✓') for x in t.splitlines()),'fail':sum(x.lstrip().startswith('✗') for x in t.splitlines())}
bs=json.loads((E/'baseline_files_sha256.json').read_text());scope=json.loads((E/'scope-verification.json').read_text());ref=scope['baseline_source_commit'];res['baseline_mismatch']=[];res['changed_paths']=[]
for name,h in bs.items():
 old=subprocess.check_output(['git','-C',str(repo),'show',ref+':'+name]);oldh=hashlib.sha256(old).hexdigest()
 if oldh!=h:res['baseline_mismatch'].append(name)
 if sha(repo/name)!=h:res['changed_paths'].append(name)
res['baseline_count']=len(bs);res['scope_changed_paths_match']=res['changed_paths']==scope['kit_changed_paths'];res['scope_sealed32_mismatch']=[]
for name,d in scope['sealed32_files'].items():
 old=subprocess.check_output(['git','-C',str(repo),'show',ref+':'+name]);oldh=hashlib.sha256(old).hexdigest()
 if sha(repo/name)!=d['working'] or oldh!=d['baseline'] or oldh!=sha(repo/name):res['scope_sealed32_mismatch'].append(name)
res['formal_seals']=[]
for path in [kit/'SHA256SUMS',kit/'history_test/SHA256SUMS']:
 rows=[ln.split(None,1) for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith('#')];bad=[]
 for h,rel in rows:
  pp=path.parent/rel.strip().lstrip('*')
  if not pp.is_file() or sha(pp)!=h:bad.append(rel)
 res['formal_seals'].append({'path':str(path.relative_to(repo)),'count':len(rows),'bad':bad})
res['evidence_manifests']=[]
for path in E.rglob('MANIFEST.sha256'):
 bad=[];rows=[ln.split(None,1) for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith('#')]
 for h,rel in rows:
  pp=path.parent/rel.strip().lstrip('*')
  if not pp.is_file() or sha(pp)!=h:bad.append(rel)
 res['evidence_manifests'].append({'path':str(path.relative_to(E)),'count':len(rows),'bad':bad[:20],'bad_count':len(bad)})
res['baseline_logs']=[]
for row in json.loads((E/'baseline/summary.json').read_text())['results']:
 t=(E/'baseline'/(row['name']+'.log')).read_text();ok=sum(x.lstrip().startswith('✓') for x in t.splitlines());fail=sum(x.lstrip().startswith('✗') for x in t.splitlines());rc=re.findall(r'# ── rc = (\d+) ──',t)
 res['baseline_logs'].append(dict(name=row['name'],ok=ok,fail=fail,rc=rc[-1] if rc else None,matches_summary=ok==row['n_check_lines_ok'] and fail==row['n_check_lines_fail'] and bool(rc) and int(rc[-1])==row['rc']))
res['mutation_logs']={}
for rel,key,namekey in [('mutations/resume-six','mutations','mutation'),('dump-final/mutations','runs','name')]:
 rows=json.loads((E/rel/'results.json').read_text())[key];checks=[]
 for row in rows:
  t=(E/rel/(row[namekey]+'.log')).read_text();fails=[x.strip() for x in t.splitlines() if '✗' in x]
  checks.append(dict(name=row[namekey],failures_match_raw=fails==[x.strip() for x in row['failures']],traceback='Traceback (most recent call last)' in t))
 res['mutation_logs'][rel]=checks
tree=ast.parse((E/'tools/mutation_check.py').read_text());spec=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MUTATIONS' for t in n.targets));src=(kit/'ul_reader.py').read_text();res['reconstructed_mutants']=[]
for row in json.loads((E/'mutations/resume-six/results.json').read_text())['mutations']:
 old,new=spec[row['mutation']];h=hashlib.sha256(src.replace(old,new,1).encode()).hexdigest();res['reconstructed_mutants'].append(dict(name=row['mutation'],sitecount=src.count(old),hash_matches=h==row['mutant_sha256']))
res['reviewed_code_copies']={name:(E/'independent/v2'/(name+'.reviewed.py')).read_bytes()==(kit/(name+'.py')).read_bytes() for name in ['ul_reader','ul_gates']}
res['r10_bytes_equal']={name:(E/'probes/r10-evidence/before'/name).read_bytes()==(E/'probes/r10-evidence/after'/name).read_bytes() for name in ['ul_windows.csv','ul_steps.csv','ul_events.csv']}
res['fullgate']=json.loads((E/'full_gate_receipt.json').read_text());res['python']=s['python'];res['script_sha256']=sha(pathlib.Path(__file__));(out/'audit.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False,indent=2))
