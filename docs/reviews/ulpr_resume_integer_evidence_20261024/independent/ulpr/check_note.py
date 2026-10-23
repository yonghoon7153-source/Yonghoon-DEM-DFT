from pathlib import Path
import hashlib,json,re,subprocess
R=Path('/workspace/.cloud-setup/nonrint-20261024/ulpr');E=R/'evidence';K=R/'work/docs/data/ps45_unload_20261009';O=Path('/workspace/.cloud-setup/nonrint-20261024/audit/ulpr');B='8347d32ea678c0174bd77d4c79cfbd7b0591e4a3';sha=lambda b:hashlib.sha256(b).hexdigest();checks=[]
def check(n,v,detail=None):checks.append({'name':n,'pass':bool(v),'detail':detail})
m=json.loads((E/'final-artifact-manifest.json').read_text());check('manifest 54 recorded members',len(m['sha256'])==54,len(m['sha256']));bad=[p for p,h in m['sha256'].items() if not(R/p).is_file() or sha((R/p).read_bytes())!=h];check('all manifest members match',not bad,bad)
s=json.loads((E/'final-v5-suite/summary.json').read_text());check('13 suite commands rc0 fail0',len(s['results'])==13 and all(x['rc']==0 and x['n_check_lines_fail']==0 for x in s['results']));bad=[p for p,h in s['working_files_sha256'].items() if sha((K/p).read_bytes())!=h];check('94 tested kit files equal current',len(s['working_files_sha256'])==94 and not bad,bad)
counts={};expected=[24,16,21,202,304,12,1,291,1,172,1,56,38]
for x,want in zip(s['results'],expected):
 t=(E/'final-v5-suite'/(x['name']+'.log')).read_text();n=sum(l.lstrip().startswith('✓') for l in t.splitlines());f=sum(l.lstrip().startswith('✗') for l in t.splitlines());counts[x['name']]={'pass':n,'fail':f};check('raw '+x['name'],n==want==x['n_check_lines_ok'] and f==0 and '# ── rc = 0 ──' in t,counts[x['name']])
sc=json.loads((E/'scope.json').read_text());bad=[]
for p,h in sc['baseline_sha256'].items():
 b=subprocess.check_output(['git','show',B+':docs/data/ps45_unload_20261009/'+p],cwd='/workspace/Yonghoon-DEM-DFT')
 if sha(b)!=h:bad.append(p)
check('scope baseline 94 hashes against pinned Git',len(sc['baseline_sha256'])==94 and not bad,bad)
changed=[p for p,h in sc['baseline_sha256'].items() if sha((K/p).read_bytes())!=h];check('exact five kit changes',set(changed)==set(sc['changed_kit_files']) and len(changed)==5,changed)
check('64 production decks unchanged',sum(p.startswith('decks/') for p in sc['baseline_sha256'])==64 and not any(p.startswith('decks/') for p in changed))
check('16 history files unchanged',sum(p.startswith('history_test/') for p in sc['baseline_sha256'])==16 and not any(p.startswith('history_test/') for p in changed))
mut=json.loads((E/'mutations-v5/results.json').read_text());want=[22,12,5,2,7,1,4,2,6,3,3];check('author 11 mutations and exact failure counts',len(mut['mutations'])==11 and [x['failed'] for x in mut['mutations']]==want and all(x['error'] is None and x['killed'] for x in mut['mutations']),[(x['name'],x['failed']) for x in mut['mutations']])
cli=json.loads((E/'cli-v5/results.json').read_text());check('CLI 2 OK same rho plus8 unidentified null',len(cli['cases'])==10 and all(x['csv_unchanged'] and x['rc']==0 for x in cli['cases']) and all(x['primary_status']=='OK' and x['rho']==.20260778734286913 and x['auth'] for x in cli['cases'][:2]) and all(x['primary_status']=='UNIDENTIFIED' and x['rho'] is None and not x['auth'] for x in cli['cases'][2:]))
for x in cli['cases']:
 root=E/'cli-v5'/x['name'];r=json.loads((root/'ps_7_3_r45/UT/arm_verdict.json').read_text());check('CLI saved verdict '+x['name'],r['primary_status']==x['primary_status'] and r['rho_pct']==x['rho'])
d=json.loads((E/'deck-probe-v5/deck_probe.json').read_text());check('four modeled producer resumes limited equality',len(d)==4 and [x['kr'] for x in d]==[0,1,2,3] and all(x['new_sim_result']=='RM_STOP' and x['primary_status']=='OK' and x['rho']==.20260778734286913 and x['cli_rc']==0 for x in d) and [x['csv_rows_match_uninterrupted'] for x in d]==[False,False,True,True])
redcounts={}
for p,want in [('test-first-final.log',44),('test-first-r39.log',46),('test-first-state-space.log',4),('test-first-manifest-space.log',2),('test-first-line-separator.log',9),('test-first-event-separator.log',3)]:
 t=(E/p).read_text();n=sum(l.lstrip().startswith(('✗','FAIL R39')) and 'R39' in l for l in t.splitlines());redcounts[p]=n;check('historical red count '+p,n==want,n)
note=(R/'NOTE.md').read_text();links=re.findall(r'\]\(([^)]+)\)',note);check('all note local links resolve',all((R/p).exists() for p in links),links)
res={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','note_sha256':sha((R/'NOTE.md').read_bytes()),'check_count':len(checks),'checks':checks,'red_counts':redcounts,'scope':'Document claims independently compared to raw log/verdict/manifest and pinned baseline bytes; no new fullgate or physical execution.'};(O/'note-review.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='checks'},indent=2));print('failures',json.dumps([x for x in checks if not x['pass']],ensure_ascii=False))
