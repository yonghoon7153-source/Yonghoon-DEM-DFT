from pathlib import Path
import hashlib,json,zipfile,re,subprocess
R=Path('/workspace/.cloud-setup/nonrint-20261024/ulpr');D=R/'deliverables';E=D/'docs/reviews/ulpr_resume_integer_evidence_20261024';O=Path('/workspace/.cloud-setup/nonrint-20261024/audit/ulpr');sha=lambda b:hashlib.sha256(b).hexdigest();checks=[]
def check(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d})
actual={str(p.relative_to(D)):p.read_bytes() for p in D.rglob('*') if p.is_file()};m=json.loads((E/'package_manifest.json').read_text());excluded={str((E/x).relative_to(D)) for x in ['package_manifest.json','MANIFEST.sha256']};listed={x['path'] for x in m['files']};check('package exact member selection',listed==set(actual)-excluded);check('package 280 member hashes/bytes',len(m['files'])==280 and all(sha(actual[x['path']])==x['sha256'] and len(actual[x['path']])==x['bytes'] for x in m['files']));check('package byte total',sum(len(actual[p]) for p in listed)==m['total_bytes'])
man=dict((l.split(None,1)[1].lstrip('*'),l.split(None,1)[0]) for l in (E/'MANIFEST.sha256').read_text().splitlines());check('outer manifest exact set',set(man)==set(actual)-{str((E/'MANIFEST.sha256').relative_to(D))});check('outer manifest hashes',all(sha(actual[p])==h for p,h in man.items()))
f=json.loads((R/'deliverables-filelist.json').read_text());files=f['files'] if isinstance(f,dict) else f;check('external list exact set',set(x['path'] for x in files)==set(actual));check('external all 282 identities',len(files)==282 and all(sha(actual[x['path']])==x['sha256'] and len(actual[x['path']])==x['bytes'] for x in files));check('total 4317460 bytes',sum(map(len,actual.values()))==4317460,sum(map(len,actual.values())))
p=json.loads((E/'archive-provenance.json').read_text());bad=[];members=0
for r in p['records']:
 b=actual[r['path']]
 if sha(b)!=r['sha256']:bad.append([r['path'],'hash'])
 if r.get('transformation')=='byte-identical copy' and b!=Path(r['original']).read_bytes():bad.append([r['path'],'copy'])
 if 'members' in r:
  with zipfile.ZipFile(D/r['path']) as z:
   if set(z.namelist())!=set(x['member'] for x in r['members']):bad.append([r['path'],'member set'])
   for x in r['members']:
    b=z.read(x['member']);members+=1
    if sha(b)!=x['sha256'] or len(b)!=x['bytes'] or b!=(Path(r['original_root'])/x['member']).read_bytes():bad.append([x['member'],'original bytes'])
check('all original copies/archives current match',not bad,{'records':len(p['records']),'zip_members':members,'failures':bad})
s=json.loads((E/'source_manifest.json').read_text());check('six reviewed source bytes unchanged',len(s['files'])==6 and all(sha(actual[x['path']])==x['sha256'] and actual[x['path']]==(R/'work'/x['path']).read_bytes() for x in s['files']))
check('baseline six hashes pinned Git',all(sha(subprocess.check_output(['git','show',s['baseline_pin']+':'+x['path']],cwd='/workspace/Yonghoon-DEM-DFT'))==x['baseline_sha256'] for x in s['files']))
check('source diff identity',sha((E/'source/candidate.diff').read_bytes())=='ccd610c9e7c9b3d1443edba03324a8c0fdf0bed0330f908ca7844586b293efd0')
check('portable copies exact',all((E/'independent/ulpr/portable'/x).read_bytes()==(O/'portable'/x).read_bytes() for x in ['attack_ulpr_resume.py','independent_mutations.py','provenance.json']))
paths=[D/'docs/reviews/codex_dem_unloading_resume_integer_request_20261024.md',D/'docs/collab/codex_to_claude/20261024-0320_unloading-resume-integer.md',E/'README.md',E/'NOTE.md'];bad=[]
for path in paths:
 for rel in re.findall(r'\]\(([^)]+)\)',path.read_text()):
  if not rel.startswith(('http','mailto','#')) and not(path.parent/rel.split('#')[0]).exists():bad.append([str(path.relative_to(D)),rel])
check('current live document links resolve',not bad,bad)
receipt=json.loads((E/'full_gate_receipt.json').read_text());check('fullgate not silently promoted','PENDING' in str(receipt),receipt)
res={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','failures':[x for x in checks if not x['pass']],'file_count':len(actual),'total_bytes':sum(map(len,actual.values())),'checks':checks,'scope':'Frozen pre-integration package preservation, document scope and manifest audit; fullgate remains PENDING.'};(O/'import-package-review.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='checks'},ensure_ascii=False,indent=2))
