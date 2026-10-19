from pathlib import Path
import contextlib,hashlib,io,json,os,re,sys,tarfile,tempfile,time,urllib.request
R=Path(__file__).resolve().parents[1]; S=R/'source'; O=R/'evidence'; OLD=R.parent/'lhs214r_fix_recheck_20261017'; B=OLD/'base'
PIN='77d8fd44545c33cd10ab18fc250c7ad3023833ea'
deps=[R/'deps',R.parent/'lhs_coverage_review_20260930/deps',R.parent/'gen2_network_reverify3_20261007/deps']
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8',TEMP=str(R/'tmp'),TMP=str(R/'tmp'),PYTHONPATH=os.pathsep.join(map(str,deps)))
sys.path[:0]=list(map(str,[S/'scripts',S/'webapp',*deps]));sys.dont_write_bytecode=True;tempfile.tempdir=str(R/'tmp')
def read(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes() if os.name=='nt' else p.read_bytes()
def save(name,obj): (O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
def metadata():
    a=json.loads(read(R/'source_manifest.json'));b=json.loads(read(OLD/'source_manifest.json'))
    ma={x['path']:x for x in a['files']};mb={x['path']:x for x in b['files']}
    changed=[p for p in sorted(set(ma)|set(mb)) if p.startswith(('scripts/','webapp/')) and ma.get(p,{}).get('sha256')!=mb.get(p,{}).get('sha256')]
    diff={}
    import difflib
    for p in changed:
        if p in ma and p in mb:
            d=''.join(difflib.unified_diff(read(OLD/'source'/p).decode('utf8').splitlines(True),read(S/p).decode('utf8').splitlines(True),fromfile='60ba39e22/'+p,tofile=PIN+'/'+p))
            diff[p]=d
    save('code_diff.json',diff)
    req=json.loads(read(O/'request_history.json'))
    evidence=S/'docs/reviews/lhs214rr_fix_evidence_20261018'
    sha=[]
    for line in (evidence/'SHA256SUMS').read_text(encoding='utf8').splitlines():
        if not line.strip():continue
        h,p=line.split(maxsplit=1);p=p.lstrip('*')
        q=evidence/p
        if not q.exists():q=S/p
        sha.append(dict(path=p,expected=h,actual=hashlib.sha256(read(q)).hexdigest()))
    # Read the complete Git trees, rather than the compare endpoint's 300-file cap.
    url='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/git/trees/155534744fed2263af221b1003ba104844cdf96b?recursive=1'
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'read-only-review'})) as f:t155=json.load(f)
    save('tree_155534744.json',t155)
    tp=json.loads(read(O/'tree.json'));assert not t155['truncated'] and not tp['truncated']
    t1={x['path']:x['sha'] for x in t155['tree'] if x['type']=='blob'};t2={x['path']:x['sha'] for x in tp['tree'] if x['type']=='blob'}
    delta155=[p for p in sorted(t1.keys()|t2.keys()) if p.startswith(('scripts/','webapp/')) and t1.get(p)!=t2.get(p)]
    import supp20_input_receipt as sr
    fp=sr.NP.code_fp(sr.NP.code_hashes());reg=sr.registration_values()
    sealchanged=[p for p in sr.NP.CODE_FILES if hashlib.sha256(read(S/p)).hexdigest()!=hashlib.sha256(read(OLD/'source'/p)).hexdigest()]
    result=dict(pin=PIN,request_commit=req[0]['sha'],changed_scripts_webapp_vs_60ba=changed,changed_scripts_webapp_vs_155=delta155,code_fp=fp,seal_changed=sealchanged,registration=reg,submitted_hashes=sha,all_submitted_hashes_ok=all(x['actual']==x['expected'] for x in sha))
    save('root_metadata.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
def a4():
    file=S/'docs/reviews/lhs214r_fix_evidence_20261016/a4_l214r_no_impact.py';raw=read(file)
    ns={'__file__':str(file),'__name__':'review_a4'};exec(compile(raw,str(file),'exec'),ns)
    bm={r['path']:r for r in json.loads(read(OLD/'base_manifest.json'))['files']};sm={r['path']:r for r in json.loads(read(R/'source_manifest.json'))['files']}
    changed=[p for p in sorted(bm.keys()|sm.keys()) if p.startswith(('scripts/','webapp/')) and bm.get(p,{}).get('sha256')!=sm.get(p,{}).get('sha256')]
    calls=[]
    def git_bytes(*args):
        calls.append(args)
        if args[0]=='show':
            ref,p=args[1].split(':',1);assert '6cb2569569ec74b7f5a96e0ef19494e872da5272'.startswith(ref)
            b=read(B/p);assert hashlib.sha256(b).hexdigest()==bm[p]['sha256'];return b
        if args[:3]==('archive','--format=tar','6cb256956'):
            assert args[3:]==('webapp','scripts');out=io.BytesIO()
            with tarfile.open(fileobj=out,mode='w') as t:
                for p,row in sorted(bm.items()):
                    if p.startswith(('webapp/','scripts/')):
                        b=read(B/p);assert hashlib.sha256(b).hexdigest()==row['sha256'];n=tarfile.TarInfo(p);n.size=len(b);n.mode=0o644;t.addfile(n,io.BytesIO(b))
            return out.getvalue()
        if args==('diff','--name-only','6cb256956','--','scripts','webapp'):return ('\n'.join(changed)+'\n').encode()
        raise AssertionError(args)
    ns['A4'].git_bytes=git_bytes;sys.argv=[str(file),'--base','6cb256956','--json',str(O/'a4_rerun.json')]
    t=time.monotonic()
    with (O/'a4_rerun.log').open('w',encoding='utf8') as f,contextlib.redirect_stdout(f),contextlib.redirect_stderr(f):rc=ns['main']()
    save('a4_adapter.json',dict(original_sha256=hashlib.sha256(raw).hexdigest(),source_text_unchanged=True,git_requests=calls,no_git_commands=True,seconds=time.monotonic()-t,rc=rc))
    out=json.loads(read(O/'a4_rerun.json'));print(json.dumps(dict(rc=rc,total=len(out['rows']),passed=sum(bool(x['identical']) for x in out['rows']),seconds=out['sec'])),flush=True)
def receipt_tests():
    import supp20_input_receipt as sr
    from unittest.mock import patch
    raw_run=sr.NP.subprocess.run;calls=[]
    # Only provide installed dependencies to isolated interpreter; certificate logic unchanged.
    def run(argv,*a,**kw):
        if isinstance(argv,list) and len(argv)>4 and argv[1:4]==['-I','-B','-c'] and argv[4]==sr.NP.GEN_PROBE:
            argv=list(argv);argv[4]='import sys; sys.path[:0]='+repr(list(map(str,deps)))+'\n'+argv[4];calls.append('isolated GEN_PROBE dependency roots')
        return raw_run(argv,*a,**kw)
    t=time.monotonic()
    with patch.object(sr.NP.subprocess,'run',run),(O/'receipt_selftest.log').open('w',encoding='utf8') as f,contextlib.redirect_stdout(f),contextlib.redirect_stderr(f):rc=sr._selftest()
    save('receipt_selftest_adapter.json',dict(rc=rc,calls=calls,seconds=time.monotonic()-t))
    print(json.dumps(dict(rc=rc,seconds=time.monotonic()-t)),flush=True)
def fences():
    import supp20_input_receipt as sr
    from markdown_it import MarkdownIt
    md=MarkdownIt('commonmark')
    text=(S/sr.REG_DOC).read_text(encoding='utf8');fp=sr.NP.code_fp(sr.NP.code_hashes())
    no_pending=re.sub(r'`code_fp_pending [0-9a-f]{64}`','(pending removed in isolated diagnostic)',text)
    no_active=re.sub(r'^## 3\.', '## 30.',no_pending,flags=re.M)
    active=f'\n## 3. Active registration\n`code_fp {fp}`\n'
    examples={}
    for char in ['`','~']:
        for width in [3,4,5,8]:
            name=f'{ord(char)}_{width}'
            op=char*width;inner=char*(width-1)
            for indent,lab in [('', 'empty'),(' ', 'space1'),('   ','space3'),('\t','tab'),(' \t','space_tab')]:
                examples[name+'_indent_'+lab]=f'\n{op}markdown\n{indent}{op}\n## 3. Example only\n`code_fp {fp}`\n{op}\n'
            for tail,lab in [('','empty'),(' ','space'),('\t','tab'),('\u00a0','nbsp'),('\u2003','emspace'),(' x','text')]:
                examples[name+'_tail_'+lab]=f'\n{op}markdown\n{op}{tail}\n## 3. Example only\n`code_fp {fp}`\n{op}\n'
            examples[name+'_shorter']=f'\n{op}markdown\n{inner}\n## 3. Example only\n`code_fp {fp}`\n{op}\n'
            examples[name+'_unclosed']=f'\n{op}markdown\n## 3. Example only\n`code_fp {fp}`\n'
            examples[name+'_normal_active_after']=f'\n{op}markdown\n{inner}\n## 3. Example only\n`code_fp {fp}`\n{op}\n'+active
    examples['active_section_fenced_value']='\n## 3. Active heading but example value only\n````markdown\n`code_fp '+fp+'`\n````\n'
    examples['active_section_plain_value']=active
    out=[];d=O/'receipt_fence_cases';d.mkdir(exist_ok=True)
    for name,extra in examples.items():
        txt=no_active+extra;p=d/(name+'.md');p.write_text(txt,encoding='utf8')
        tokens=md.parse(extra);heads=[]
        for i,t in enumerate(tokens):
            if t.type=='heading_open' and t.tag=='h2' and re.match(r'3\.(\s|$)',tokens[i+1].content):heads.append(tokens[i+1].content)
        body,why=sr._md_section(txt,3)
        # Run the complete receipt for mismatches and representative controls only.
        mismatch=bool(body)!=(len(heads)==1)
        need=mismatch or name in ['96_4_shorter','126_4_shorter','96_4_normal_active_after','active_section_fenced_value','active_section_plain_value']
        rec=sr.receipt(reg_doc=str(p)) if need else None
        row=dict(name=name,extra=extra,commonmark_active_h2=heads,parser_accept=body is not None,parser_reason=why,heading_mismatch=mismatch)
        if rec is not None:row.update(receipt_rc=rec['rc'],bad=[c['id'] for c in rec['checks'] if not c['ok']],code_fp=rec['registration']['values']['code_fp'])
        out.append(row)
    save('receipt_fence_matrix.json',dict(commonmark_impl='markdown-it-py '+__import__('importlib.metadata').metadata.version('markdown-it-py'),cases=out,total=len(out),mismatches=sum(x['heading_mismatch'] for x in out)))
    print(json.dumps(dict(total=len(out),mismatches=[{k:v for k,v in x.items() if k not in ['extra']} for x in out if x['heading_mismatch']]),ensure_ascii=False),flush=True)
def regressions():
    import subprocess
    tasks=['test_l214r01_certificate.py','test_l214r02_model_limit_flag.py','test_l214r05_published_certificate.py','test_l214r06_same_class.py','test_l214r09_same_class.py']
    rows=[]
    for f in tasks:
        t=time.monotonic();p=subprocess.run([sys.executable,'-X','utf8','-B',str(S/'scripts'/f)],cwd=S,capture_output=True,timeout=600)
        (O/('regression_'+f+'.log')).write_bytes(p.stdout+p.stderr)
        row=dict(file=f,rc=p.returncode,seconds=time.monotonic()-t,tail=p.stdout.decode('utf8',errors='replace').splitlines()[-3:]);rows.append(row)
        save('regressions.json',rows);print(json.dumps(row,ensure_ascii=False),flush=True)
if __name__=='__main__':globals()[sys.argv[1]]()
