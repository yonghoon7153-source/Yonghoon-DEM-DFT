"""Codex 재검증 7 탐침 출력 ↔ Codex 증거 대조 (판정값 vs 환경 차이 분리).

    python3 -I -B <이 파일> <우리 재실행 evidence> <Codex evidence> <출력 json>

환경 차이로 세는 것: run id (시각 + 난수) · 경로 · 부동소수 끝자리 (상대 1e-12) · NaN = NaN · 런타임 / 패키지 판.
"""
import json,sys,os,re,math
run,orig,outp=sys.argv[1:4]
RID=re.compile(r'\d{8}T\d{6}-[0-9a-f]{8}')
PATHY=re.compile(r'(/tmp/|[A-Za-z]:\\|\\\\\?\\|scratchpad|Users\\|r7_cli_|r7_parent_cli_)')
def num(s):
    try: return float(s)
    except Exception: return None
def eq_str(a,b):
    if RID.sub('RID',a)==RID.sub('RID',b): return 'rid'
    if PATHY.search(a) or PATHY.search(b): return 'path'
    x,y=num(a),num(b)
    if x is not None and y is not None and abs(x-y)<=1e-12*max(1,abs(x),abs(y)): return 'ulp'
    # numbers embedded in strings (ULP tails)
    ta=re.split(r'(-?\d+\.\d+(?:e-?\d+)?)',RID.sub('RID',a)); tb=re.split(r'(-?\d+\.\d+(?:e-?\d+)?)',RID.sub('RID',b))
    if len(ta)==len(tb) and all((p==q) or (i%2==1 and abs(float(p)-float(q))<=1e-12*max(1,abs(float(p)))) for i,(p,q) in enumerate(zip(ta,tb))): return 'ulp_in_text'
    return None
def walk(a,b,p,out,env):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b: out.append((p+'/'+str(k),'missing'))
            else: walk(a[k],b[k],p+'/'+str(k),out,env)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): out.append((p,'len',len(a),len(b))); return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,f'{p}[{i}]',out,env)
    elif isinstance(a,float) and isinstance(b,float) and math.isnan(a) and math.isnan(b): env['nan']=env.get('nan',0)+1
    elif a!=b:
        if isinstance(a,str) and isinstance(b,str):
            r=eq_str(a,b)
            if r: env[r]=env.get(r,0)+1; return
        if isinstance(a,(int,float)) and isinstance(b,(int,float)) and not isinstance(a,bool) and abs(a-b)<=1e-12*max(1,abs(a),abs(b)): env['ulp']=env.get('ulp',0)+1; return
        if any(t in p.lower() for t in ('seconds','python','platform','version','sys.','executable','cwd','root','argv','tmp','packages')): env['runtime']=env.get('runtime',0)+1; return
        out.append((p,repr(a)[:160],repr(b)[:160]))
res={}; tot_env={}
for fn in sorted(os.listdir(orig)):
    fo=os.path.join(orig,fn); fr=os.path.join(run,fn)
    if not fn.endswith('.json') or not os.path.exists(fr): continue
    if open(fo,'rb').read()==open(fr,'rb').read(): res[fn]={'bytes_equal':True}; continue
    a=json.load(open(fr,encoding='utf-8-sig')); b=json.load(open(fo,encoding='utf-8-sig'))
    out=[];env={}; walk(a,b,'',out,env)
    res[fn]={'bytes_equal':False,'decision_diff':out,'env_diff_counts':env}
    for k,v in env.items(): tot_env[k]=tot_env.get(k,0)+v
json.dump(res,open(outp,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
bad={k:v for k,v in res.items() if v.get('decision_diff')}
print('compared',len(res),'bytes_equal',sum(v['bytes_equal'] for v in res.values()),'with_nonenv_diff',len(bad),'env totals',tot_env)
for k,v in list(bad.items())[:15]: print(k, json.dumps(v['decision_diff'][:6],ensure_ascii=False)[:700])
