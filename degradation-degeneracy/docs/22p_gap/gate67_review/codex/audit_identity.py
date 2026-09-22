"""Read-only Git/byte inventory. No registry restoration or classification writes."""
import collections, datetime, hashlib, json, pathlib, subprocess
HERE=pathlib.Path(__file__).resolve().parent
REPO=HERE.parents[1]/'work/gate67-head'
OLD='fa947cc9b17cdbeffbb39447c99159bc2c831e6e'
EARLY='5e4cf1038f0f26a6a624d9984386cfd046657ac3'
EXPECTED='cdc49e91af15b2ef968753110cfae3bbe7ab5c2f'
SCI='743f65bead671bf353ce38027c2e8e457738ec08'
PREFIX='degradation-degeneracy/docs/22p_gap/_exec_class/'
def git(*args):return subprocess.check_output(['git','-c','core.longpaths=true','-c','http.sslBackend=openssl','-C',str(REPO),*args])
def tree(ref):
 rows={}
 for line in git('ls-tree','-r',ref,'--',PREFIX).decode().splitlines():
  meta,path=line.split('\t',1)
  if path.endswith('.json') and '/' not in path[len(PREFIX):]: rows[path]=meta.split()[2]
 return rows
head=git('rev-parse','HEAD').decode().strip();assert head==EXPECTED
early,old,new=tree(EARLY),tree(OLD),tree(head)
deleted=sorted(early.keys()-old.keys());added=sorted(new.keys()-old.keys())
prior=json.loads((HERE.parents[0]/'gate66_review_20260922/registry-audit.json').read_text(encoding='utf-8'))
assert set(deleted)=={r['path'] for r in prior['deleted']}
changes={'previous_count':len(old),'current_count':len(new),'added':added,'deleted':sorted(old.keys()-new.keys()),'changed_survivors':[p for p in old.keys()&new.keys() if old[p]!=new[p]],
 'historic_early_count':len(early),'historic_deleted_count':len(deleted),'historic_deleted_paths_match_previous_review':True,
 'historic_deleted_git_blobs':{p:early[p] for p in deleted},'historic_deleted_records_from_prior_review':prior['deleted'],
 'historical_json_scope':'path/blob identities rechecked from Git trees; original deleted payload SHA/JSON reused from prior independently reviewed audit, not reread as remote execution history',
 'added_records':{p:json.loads((REPO/p).read_text(encoding='utf-8')) for p in added}}
(HERE/'registry-audit.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
paths=['CLAUDE.md','degradation-degeneracy/docs/22p_gap/GATE67_REQUEST.md','degradation-degeneracy/docs/08_REVIEW_RESPONSE.md','degradation-degeneracy/docs/GATE66_WORKING_STATE.md','degradation-degeneracy/docs/22p_gap/mutation_replay.py','degradation-degeneracy/tests/interpreter_fixture.py','degradation-degeneracy/tests/test_gate66_defensive.py','degradation-degeneracy/tests/test_gate65_defensive.py','degradation-degeneracy/tests/test_gate64_defensive.py','degradation-degeneracy/tests/test_gate63_defensive.py','degradation-degeneracy/tests/conftest.py','degradation-degeneracy/tools/preserve.py']
rec=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=head,previous_review=OLD,scientific_reference=SCI,source_digest=json.loads((HERE/'identity.json').read_text())['rc']==0 and (HERE/'identity.stdout.bin').read_text().strip().splitlines()[-1],
 scientific_scope_log=git('log','--oneline',SCI+'..'+head,'--',*['degradation-degeneracy/'+p for p in ('src','tools','configs','scripts','run.sh','requirements*.txt')]).decode(),
 status_porcelain=git('status','--porcelain').decode(),files=[dict(path=p,bytes=(REPO/p).stat().st_size,sha256=hashlib.sha256((REPO/p).read_bytes()).hexdigest(),git_blob=git('rev-parse',head+':'+p).decode().strip()) for p in paths])
(HERE/'TARGET_IDENTITY.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
diff=git('diff',OLD,head,'--',*[p for p in paths if p.endswith('.py')])
(HERE/'reviewed-code.diff').write_bytes(diff)
print(json.dumps({k:rec[k] for k in ('head','source_digest','scientific_scope_log','status_porcelain')}))
print(json.dumps({k:v for k,v in changes.items() if k not in ('historic_deleted_git_blobs','historic_deleted_records_from_prior_review','added_records')},ensure_ascii=True))
