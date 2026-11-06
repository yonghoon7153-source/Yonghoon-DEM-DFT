from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
R=Path('/workspace/nonrint-1104/mixer');W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
report={'commands':[],'scope':'temporary synthetic inputs only; no host, scheduler, MPI or DEM'}
def run(label,args,expected):
 p=subprocess.run([sys.executable,'-I','-X','utf8','-B',*map(str,args)],cwd=R,env=env,capture_output=True,timeout=60)
 (W/(label+'.log')).write_bytes(p.stdout+p.stderr)
 report['commands'].append({'name':label,'argv':list(map(str,args)),'rc':p.returncode,'expected_rc':expected,'log':label+'.log'})
 assert p.returncode==expected,(label,p.returncode)
 print(label,p.returncode,flush=True)
before={p:sha((R/'scripts'/p).read_bytes()) for p in ['make_mixer_deck.py','mixer_deck_readback.py','mixer_deck_diff.py','mixer_smoke_blind.py','test_mixer_d2_consumers.py']}
with tempfile.TemporaryDirectory(prefix='mxd2rr01-',dir='/tmp') as temp:
 s=Path(temp)/'scripts';shutil.copytree(R/'scripts',s,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 candidate=(s/'mixer_deck_readback.py').read_text()
 (s/'mixer_deck_readback.py').write_bytes((W/'red_sources/mixer_deck_readback.py').read_bytes())
 run('red_cli_probe',[W/'probe.py',s,W/'red_cli'],0)
 (s/'mixer_deck_readback.py').write_text(candidate)
 run('green_cli_probe',[W/'probe.py',s,W/'green_cli'],0)
 mutations={
  'range_guard_removed':("    _d2_need(seed <= D2_SEED_MAX, label + f': outside 1..{D2_SEED_MAX}' + rule)","    pass  # range guard mutation"),
  'prime_guard_removed':("    _d2_need(_d2_next_prime(seed) == seed, label + ': not prime' + rule)","    pass  # primality guard mutation")}
 for name,(old,new) in mutations.items():
  assert candidate.count(old)==1
  (s/'mixer_deck_readback.py').write_text(candidate.replace(old,new))
  test='test_layered_max_seed_api_refuses_derived_overflow' if name.startswith('range') else 'test_each_actual_seed_range_and_primality'
  run(name,[s/'test_mixer_d2_consumers.py','D2InsertionSeedBounds.'+test],1)
  log=(W/(name+'.log')).read_text()
  assert 'FAILED (failures=' in log and 'ERROR:' not in log
  (s/'mixer_deck_readback.py').write_text(candidate)
red=json.loads((W/'red_cli/summary.json').read_bytes())['rows'];green=json.loads((W/'green_cli/summary.json').read_bytes())['rows']
for a,b in zip(red,green):
 assert a['case']==b['case'] and a['bytes']==b['bytes']
 assert all(x['verdict']=='PASS' for x in a['apis'].values())
 assert all(x['rc']==0 for x in a['cli'].values())
 bad=a['case']=='max_layered'
 assert all(x['verdict']==('FAIL' if bad else 'PASS') for x in b['apis'].values())
 assert all(x['rc']==(1 if bad else 0) for x in b['cli'].values())
 if bad:assert all(any('insB seed 2147483659: outside 1..2147483647' in f for f in x['failures']) for x in b['apis'].values())
assert before=={p:sha((R/'scripts'/p).read_bytes()) for p in before}
report.update(source_hashes=before,tracked_sources_unchanged_by_probes=True,
 generated_pairs_byte_preserved=3,positive_pairs_byte_preserved=2,
 negative_case='max_layered',mutations_detected=2,
 mutation_limits={'range_guard_removed':'original overflow accepted again',
                  'prime_guard_removed':'independent actual seed diagnostic lost; later form guard can still reject these composites'},
 generator_changed=False,consumer_code_changed=['mixer_deck_readback.py'],simulation_runs=0)
(W/'evidence_summary.json').write_bytes(enc(report));print('bounded evidence complete')
