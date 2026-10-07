from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;E=R/'evidence';load=lambda p:json.loads(p.read_text(encoding='utf8'))
checks=[]
def ck(name,ok,detail=None):
 checks.append(dict(name=name,ok=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
src=load(R/'source_manifest.json');bad=[]
for x in src:
 b=(R/'source'/x['path']).read_bytes()
 if hashlib.sha256(b).hexdigest()!=x['sha256'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=x['sha']:bad.append(x['path'])
ck('source448 unchanged after probes',len(src)==448 and not bad,bad)
s=load(E/'submitted_evidence.json');ck('WSL manifest byte SHA binding',s['manifest_sha']==s['reread_manifest_sha'])
ck('WSL sealed code and handover tools identical',not s['code_mismatch'] and not s['handover_mismatch'])
ck('WSL hook identical',s['hook_identical'])
c=s['receipt_counts'];ck('WSL starts15 finals15 completed3',c['n_started']==c['n_finalized']==15 and len(c['completed_attempts'])==3)
ck('WSL modules30 subset32',len(c['observed'])==30 and c['outside']==[])
ck('WSL reread3 detailed success',s['reread_n_cases']==3 and not s['reread_checks_failed'])
a={x['label']:x for x in load(E/'observation_cli.json')}
ck('actual audit positive rc0',a['all5']['rc']==0 and a['all5']['n_start']==5)
ck('actual audit final-only loss rc1',a['helper_final_missing']['rc']==1)
ck('counterexample helper pair loss rc0',a['helper_pair_missing']['rc']==0 and a['helper_pair_missing']['n_start']==4)
ck('counterexample only two core roles rc0',a['only_worker_and_solver']['rc']==0 and a['only_worker_and_solver']['n_start']==2)
r={x['label']:x for x in load(E/'release_gate.json')['cases']}
ck('actual release positive builds and checks',r['control']['accepted'] and r['control']['check']==[])
ck('original missing/bad witnesses rejected',all(not r[k]['accepted'] for k in ('absent_reread','null_nfail','failed_audit','wrong_manifest')))
ck('counterexamples detailed false/missing accepted',all(r[k]['accepted'] and r[k]['check']==[] for k in ('reread_checks_false','reread_cases_missing','audit_observation_failed')))
scope=load(E/'scope194.json');ck('194 input record census',scope['lhs']['n']==130 and scope['lhsx']['n']==64)
ck('194 all L0 overlap0 in archived audit',all(v['se_levels']=={'L0':v['n']} and v['am_levels']=={'L0':v['n']} and v['se_overlap']==v['am_overlap']==0 for v in scope.values()))
ck('32806189 positive finite known-id contacts in harvested records',sum(v['area_counts']['n_rows'] for v in scope.values())==32806189 and all(v['area_counts'][k]==0 for v in scope.values() for k in ('n_area_dump_negative','n_area_dump_zero','n_orphan_rows_skipped','n_nonfinite_skipped')))
ck('archived geometry linkage',all(not v['linkage_mismatch'] for v in scope.values()))
b=load(E/'case15_channels.json');ch=b['channels']
ck('case15 raw negative rows2',len(b['negative_area'])==2 and b['plate_um']==19.1455)
ck('case15 four overlapping IDs',ch['electronic_hertzian']['intersection']==ch['electronic_physics']['intersection']==ch['thermal_hertzian']['intersection']==[24,40,57,103])
ck('case15 physics thermal refuses negative', 'ligg_area < 0' in ch['thermal_physics']['error'])
ck('case15 ionic agrees at eight decimals',round(ch['ionic_hertzian']['value'][1],8)==0.00032635 and round(ch['ionic_physics']['value'][1],8)==0.00036225)
ck('case15 ionic certificates pass',all(ch[k]['solve_info']['conservation_rel']<1e-6 and ch[k]['solve_info']['residual_rel']<1e-6 for k in ('ionic_hertzian','ionic_physics')))
t=load(E/'wsl_code_identity.json');ck('WSL tool git blobs agree',len(t['rows'])==5 and all(x['old']==x['pin'] for x in t['rows']))
ck('release regression reports exactly two qualified fails','133 PASS · 2 FAIL' in (E/'release.log').read_text(encoding='utf8'))
o=dict(scope='Review evidence consistency only, NOT production approval',checks=checks,n_pass=sum(x['ok'] for x in checks),n_fail=sum(not x['ok'] for x in checks))
(E/'verification.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf8')
raise SystemExit(bool(o['n_fail']))
