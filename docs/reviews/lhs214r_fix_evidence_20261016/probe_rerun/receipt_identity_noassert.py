# 파생 탐침 (메인 세션 · L214R 재실행) — Codex receipt_identity.py 와 같은 변이 · 같은 출력 파일 · assert 만 뺐다 (결함의 존재를 적은 줄이라 고친 트리에서 결과를 남기지 못한다):
#   뺀 줄: assert out['current_receipt']['bad']==['D1']
#   뺀 줄: assert out['variants']['arbitrary_pending']['bad']==['D1']
#   뺀 줄: assert out['variants']['two_distinct_pending']['rc']==1
#   뺀 줄: assert out['variants']['minimal_activate_section3']['bad']==['R0','D1']
#   뺀 줄: assert out['variants']['all_old_machine_tokens_updated']['rc']==0
#   뺀 줄: assert out['variants']['redundant_identical_pending']['bad']==['D1']
#   뺀 줄: assert rc==0
"""Independent identity and pending-vs-launch probes, without changing source."""
from pathlib import Path
import contextlib,hashlib,io,json,os,re,sys,tempfile
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];S=R/'source';O=R/'evidence/receipt_identity';O.mkdir(exist_ok=True)
deps=[str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps')]
sys.path[:0]=[str(S/'scripts'),*deps]
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
tempfile.tempdir=str(R/'tmp')
import supp20_input_receipt as sr
np=sr.NP
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
now=np.code_hashes();old=np.code_hashes(R/'base')
rows={p:{'before':old[p],'after':now[p]} for p in np.CODE_FILES if now[p]!=old[p]}
base=sr.receipt()
reg=base['registration']['values'];regtext=(S/sr.REG_DOC).read_text(encoding='utf8')
def compact(rec):
    return {'rc':rec['rc'],'bad':[c['id'] for c in rec['checks'] if not c['ok']],
            'registration':rec['registration']['values'],
            'D1':next(c['detail'] for c in rec['checks'] if c['id']=='D1')}
out={'pin':'9e3ef54ca228111360bfe5f6d9dad4ebe26d54af','code_files':len(now),'before_fp':np.code_fp(old),'after_fp':np.code_fp(now),'changed':rows,'current_receipt':compact(base),'variants':{}}
(O/'current_receipt.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf8')
fp=np.code_fp(now);prev=reg['code_fp']
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='registration_') as td:
    no_pending=re.sub(r'`code_fp_pending [0-9a-f]{64}`','(pending declaration removed)',regtext)
    # Follow exactly the described future operation: update active section 3 and remove pending.
    minimal=no_pending.replace(f'`code_fp {prev}`',f'`code_fp {fp}`',1)
    all_tokens=no_pending.replace(f'`code_fp {prev}`',f'`code_fp {fp}`')
    tests={'no_pending':no_pending,'minimal_activate_section3':minimal,'all_old_machine_tokens_updated':all_tokens,
           'arbitrary_pending':regtext.replace(f'code_fp_pending {fp}','code_fp_pending '+'b'*64),
           'two_distinct_pending':regtext+'\n`code_fp_pending '+'b'*64+'`\n',
           'malformed_pending':regtext.replace(f'code_fp_pending {fp}',f'code_fp_pending {fp[:-1]}'),
           'redundant_identical_pending':regtext+f'\n`code_fp_pending {fp}`\n'}
    for name,txt in tests.items():
        p=Path(td)/(name+'.md');p.write_text(txt,encoding='utf8')
        rec=sr.receipt(reg_doc=str(p));out['variants'][name]=compact(rec)
# A duplicate declaration with the same value is deliberately collapsed by the parser.
raw_run=np.subprocess.run;raw_main=np.main;bootstrap='import sys; sys.path[:0]='+repr(deps)+'\n';calls=[]
def run(argv,*a,**kw):
    if isinstance(argv,list) and len(argv)>4 and argv[1:4]==['-I','-B','-c'] and argv[4]==np.GEN_PROBE:
        argv=list(argv);argv[4]=bootstrap+argv[4];calls.append({'code_root':argv[5],'bootstrap':bootstrap})
    return raw_run(argv,*a,**kw)
def main(argv=None):
    rc=raw_main(argv)
    if argv and '--preflight-receipt' in argv:
        p=Path(argv[argv.index('--preflight-receipt')+1])
        if p.name=='pos_preflight.json' and p.is_file():
            rec=json.loads(p.read_text(encoding='utf8'))
            (O/'selftest_pos_preflight.json').write_bytes(p.read_bytes())
            (O/'selftest_pos_preflight.log').write_bytes(Path(rec['log']['path']).read_bytes())
    return rc
buf=io.StringIO()
with patch.object(np.subprocess,'run',run),patch.object(np,'main',main),contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
    rc=sr.main(['--selftest'])
(O/'selftest_dependency_only.log').write_text(buf.getvalue(),encoding='utf8')
out['selftest']={'rc':rc,'bootstrap_calls':len(calls),'final':buf.getvalue().strip().splitlines()[-1],
                 'failures':[s for s in buf.getvalue().splitlines() if s.lstrip().startswith('FAIL')],
                 'qualification':'Only existing third-party dependency paths supplied to actual isolated GEN_PROBE subprocess; source, gate, numerical algorithms unchanged.'}
(O/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:out[k] for k in ('before_fp','after_fp','changed','selftest')},ensure_ascii=False,indent=2))
