"""Independent byte-decision and report probes. Recomputed verdict is a fixed mock;
this is NOT a producer, Linux shell, or 12-unit merged end-to-end reproduction."""
import sys,pathlib,json,hashlib,contextlib,io,copy,tempfile,random,math
from unittest.mock import patch
BASE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'received/repo/scripts'))
import rint_r_chain as R
import test_rint_r_chain as T
T.RR=R
OUT=BASE/'root_review'
OUT.mkdir(exist_ok=True)
scratch=OUT/'scratch';scratch.mkdir(exist_ok=True);tempfile.tempdir=str(scratch)
checks=[]
def chk(name,ok,details=None):
    checks.append({'name':name,'pass':bool(ok),'details':details})
ok,why=T.t_RV05();chk('resident_RV05_report_classifier',ok,str(why))
pub={'verdict':'PASS','state':'COMPUTED','flags':[],'blocking_flags':[],'sentence_allowed':True,'registration':{'path':'synthetic.md'},'input_dirs':[],'ledger_input':None}
res={'reference':{'G0':1.125},'scale':1,'accepted':True,'none':None,'nested':[1,'가',{'x':0.125}]}
bp=R.canon_bytes(pub);br=R.canon_bytes(res)
def dig(d):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in d.iterdir() if p.is_file()}
cases=[
 ('unchanged',bp,br,0),
 ('public_trailing_space',bp+b' ',br,1),
 ('result_crlf',bp,br.replace(b'\n',b'\r\n'),1),
 ('result_key_order',bp,(json.dumps(dict(reversed(list(res.items()))),ensure_ascii=False,indent=1)+'\n').encode(),1),
 ('boolean_as_one',bp,br.replace(b'true',b'1'),1),
 ('number_as_bool',bp,br.replace(b'"scale": 1',b'"scale": true'),1),
 ('one_float_same_value',bp,br.replace(b'"scale": 1',b'"scale": 1.0'),1),
 ('duplicate_conflicting',bp,br.replace(b'"scale": 1',b'"scale": 9, "scale": 1'),1),
 ('duplicate_same',bp,br.replace(b'"scale": 1',b'"scale": 1, "scale": 1'),1),
 ('null_as_false',bp,br.replace(b'null',b'false'),1),
 ('deep_result',bp,b'['*2000+b'0'+b']'*2000,1),
 ('deep_public',b'['*2000+b'0'+b']'*2000,br,1),
 ('public_array',b'[]\n',br,1),
 ('public_invalid_utf8',b'\xff',br,1),
 ('missing_result',bp,None,1),
 ('result_scalar',bp,b'1\n',1),
 ('same_grade_value_changed',bp,br.replace(b'1.125',b'1.126'),1),
]
with tempfile.TemporaryDirectory(prefix='rv_',dir=str(scratch)) as tmp:
    d=pathlib.Path(tmp)
    for name,rawp,rawr,want in cases:
        (d/'verdict.json').write_bytes(rawp)
        rp=d/'verdict_results.json'
        if rawr is None:
            if rp.exists():rp.unlink()
        else:rp.write_bytes(rawr)
        before=dig(d)
        so=io.StringIO()
        try:
            with patch.object(R,'verdict_compute',side_effect=lambda *a,**k:(copy.deepcopy(pub),copy.deepcopy(res))),patch.object(R,'env_record',return_value={'synthetic':True}),contextlib.redirect_stdout(so):
                rc=R.reverify(d,None,str(d))
            chk('reverify_'+name,rc==want and dig(d)==before,{'rc':rc,'stdout':so.getvalue(),'original_unchanged':dig(d)==before})
        except Exception as e:
            chk('reverify_'+name,False,{'exception':repr(e)})
    # Restored original is SAME, even after repeated mutations
    (d/'verdict.json').write_bytes(bp);rp.write_bytes(br)
    with patch.object(R,'verdict_compute',return_value=(copy.deepcopy(pub),copy.deepcopy(res))),patch.object(R,'env_record',return_value={}),contextlib.redirect_stdout(io.StringIO()):
        chk('restore_same',R.reverify(d,None,str(d))==0)
    # Report function is not the decision: a deliberately uninformative report still cannot convert DIFF into SAME.
    rp.write_bytes(br+b' ')
    orig=R.byte_diff_view
    with patch.object(R,'verdict_compute',return_value=(copy.deepcopy(pub),copy.deepcopy(res))),patch.object(R,'env_record',return_value={}),patch.object(R,'byte_diff_view',return_value={'differ':False,'kinds':[],'first_diff_offset':None,'len_delta':0}),contextlib.redirect_stdout(io.StringIO()):
        chk('report_classifier_not_decision',R.reverify(d,None,str(d))==1)
    for name,rawp,rawr,_want in cases:
        if rawp!=bp:continue
        with patch.object(R,'env_record',return_value={}):
            rep=R.reverify_report(d,pub,pub,rawr,res,rawr==br,None,old_pub=bp,new_pub=bp,new_res=br)
        expected_differ=name in ('boolean_as_one','number_as_bool','duplicate_conflicting','null_as_false','deep_result','missing_result','result_scalar','same_grade_value_changed')
        expected_kind='unreadable' if name=='deep_result' else 'missing' if name=='missing_result' else 'value' if expected_differ else None
        chk('report_semantics_'+name,rep['results_differ']==expected_differ and (expected_kind is None or expected_kind in rep['results_bytes']['kinds']),{k:rep[k] for k in ('results_differ','results_keys_differ','results_bytes')})
# Independent strict JSON equivalence reference and metamorphic raw-byte cases
def eq(a,b):
    if type(a) is bool or type(b) is bool:return type(a)is type(b) and a==b
    if a is None or b is None:return a is b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):return a==b
    if type(a)is not type(b):return False
    if isinstance(a,list):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
    if isinstance(a,dict):return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
    return a==b
rng=random.Random(20261105)
vals=[None,False,True,0,1,1.0,-0.0,2.5,'x','가',[],{},[1,True],{'x':True},{'x':1}]
for i in range(300):
    a=rng.choice(vals);b=rng.choice(vals)
    chk('strict_reference_'+str(i),R.json_same(a,b)==eq(a,b))
    n=R.canon_bytes({'item':a,'k':i})
    for tag,o in [('same',n),('space',n+b' '),('crlf',n.replace(b'\n',b'\r\n')),('compact',json.dumps({'item':a,'k':i},ensure_ascii=True).encode())]:
        v=R.byte_diff_view(o,n)
        chk('byte_metamorphic_'+str(i)+'_'+tag,v['differ']==(o!=n) and v['len_delta']==len(n)-len(o) and all(k in R.BYTE_DIFF_KINDS for k in v['kinds']),v if v['differ']!=(o!=n) else None)
out={'scope':'Windows pure Python: actual reverify/report with mocked recomputation; not actual producer/ledger end-to-end','python':sys.version,'checks':checks,'total':len(checks),'pass':sum(c['pass'] for c in checks)}
(OUT/'reverify_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},ensure_ascii=False))
sys.exit(0 if out['pass']==out['total'] else 1)
