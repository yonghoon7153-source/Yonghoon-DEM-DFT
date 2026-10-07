"""Validate saved review results and pinned bytes. NOT a production acceptance gate."""
from pathlib import Path
import hashlib,json,sys,platform,re
R=Path(__file__).resolve().parent
PIN='0801d4ceb540f5a5813761b20a5e0f304ed80a03'
def read(name):return json.loads((R/'evidence'/name).read_text(encoding='utf8'))
checks=[]
def check(name,value):
    checks.append(dict(name=name,ok=bool(value)))
    print(('PASS ' if value else 'FAIL ')+name)
manifest=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
bad=[]
for x in manifest:
    b=(R/'source'/x['path']).read_bytes()
    if not (x['ref']==PIN and len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
            and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['sha']):bad.append(x['path'])
check('Pinned source bytes and Git blob IDs (432 files)',len(manifest)==432 and not bad)
attachments=[]
for p in sorted((R/'submitted').glob('*.md')):
    b=p.read_bytes();src=R/'source/docs/reviews'/p.name
    same=b.decode('utf8').replace('\r\n','\n').rstrip('\n')==src.read_text(encoding='utf8').rstrip('\n')
    attachments.append(dict(name=p.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),matches_pinned_text_ignoring_line_endings=same))
    check('Submitted text matches pin: '+p.name,same)
s=read('seal_paths.json');a={x['label']:x for x in s['audit']};rr={x['label']:x for x in s['reread']}
check('G2RR2-01 baseline passes',a['baseline']['rc']==0)
check('G2RR2-01 original and deletion/null mutants refuse',all(x['rc']!=0 for k,x in a.items() if k!='baseline'))
check('G2RR2-02 independent reread control passes',rr['baseline']['rc']==0)
check('G2RR2-02 zero-case mutants fail',all(x['rc']!=0 and x['result']['n_fail']>0 for k,x in rr.items() if k!='baseline'))
sc=read('scope_checks.json')
check('20 required-field removal/null mutants invalid',len(sc['deletions'])==20 and all(x['kind']=='invalid' for x in sc['deletions']))
check('Historical admission is explicit',sc['historical']['kind']=='historical' and all(x['result']['kind']=='invalid' for x in sc['history_mutants'] if x['label']!='baseline'))
d=read('dependency_gap.json')
check('G2RR2-03 fracture mutation now changes seal',not d['hash_unchanged'] and d['fracture_model_in_closure'])
check('Registered 32-file fingerprint matches',s['code_files']==32 and s['code_fp']=='e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71')
i=read('input_digest.json');check('Independent registered ID/metadata table hashes agree',i['equal'] and i['counts']=={'lhs':130,'lhsx':64})
b={x['label']:x for x in read('branch_policy.json')}
check('G2RR2-04/05 publication refuses all three mutants',all(b[k]['status']=='failed' for k in ['cf_sigma0_x2','full_cert_sigma0_x2','diagnostic_fields_absent']))
check('Honest branch failure preserves FULL and passes reread',all(b[k]['status']=='done' and b[k]['full_q']==b['baseline']['full_q'] and not b[k]['reread_bad'] and b[k]['cf_dim'] is None for k in ['honest_cf_exception','honest_cf_cert_failure']))
check('Temperature/activation-energy positive controls',len(sc['temperature_positive'])==8 and all(not x['problems'] for x in sc['temperature_positive']))
check('S3 six-file dependency check',len(sc['s3_dependencies']['files'])==6 and not sc['s3_dependencies']['problems'])
check('S3 valid six accepted, four mutated bundles refused (Git adapter)',[x['accepted'] for x in sc['s3_bundle_adapter_checks']]==[True,False,False,False,False])
ng=read('new_gates.json');n={x['label']:x for x in ng['audit']}
check('NEW G2RR3-02 no-log control refuses',n['none']['rc']!=0)
check('NEW G2RR3-02 empty/non-repo log falsely passes',all(n[k]['rc']==0 and not n[k]['observed']['observed'] for k in ['empty_file','only_nonrepo_line']))
check('NEW G2RR3-02 lost-log differential',n['unsealed_log']['rc']!=0 and n['unsealed_log_lost']['rc']==0)
g={x['label']:x for x in read('release_gate.json')['cases']}
check('NEW G2RR3-01 build positive/explicit-failure controls discriminate',g['pass_control']['accepted'] and not g['pass_control']['check'] and not g['explicit_failure']['accepted'])
check('NEW G2RR3-01 six incomplete/failed evidence variants build and check green',all(g[k]['accepted'] and not g[k]['check'] for k in ['absent_reread','invalid_reread','empty_reread','null_nfail','refused_audit','unsealed_audit']))
packages={}
for name in ['numpy','scipy','matplotlib','networkx']:
    try:packages[name]=__import__(name).__version__
    except ImportError:packages[name]='not importable by this verifier'
out=dict(pin=PIN,checks=checks,n=len(checks),n_fail=sum(not x['ok'] for x in checks),source_errors=bad,attachments=attachments,
         environment=dict(python=sys.version,platform=platform.platform(),packages=packages),
         scope='Verifies review evidence, including EXPECTED current-code failures. Does not run or approve a 194 batch or registered S3 campaign.')
(R/'evidence/verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(f"Review evidence checks: {out['n']-out['n_fail']}/{out['n']}")
sys.exit(bool(out['n_fail']))
