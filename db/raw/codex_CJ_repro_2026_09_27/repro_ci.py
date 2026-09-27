"""CI review: synthetic fixtures only, no VASP/UMA/DFT calculations.
Run: python repro_ci.py --source /path/to/checkout --bash /bin/bash
Python standard library suffices; production D3 references are reused, not recomputed.
All scratch files are in a TemporaryDirectory; source files are never modified.
"""
import argparse, copy, gzip, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,default=Path(__file__).resolve().parent/'source')
ap.add_argument('--bash',default=shutil.which('bash') or 'bash')
ap.add_argument('--assert-fixed',action='store_true',help='Fail unless find/sort/tar-list errors return 4 and preserve the old archive pair.')
args=ap.parse_args()
HERE=Path(__file__).resolve().parent
SRC=args.source.resolve()
PKG=SRC/'db/inputs/wad_aprime_v5_vasp_2026_09_27'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('ci_target',SRC/'tools/wad/build_v5_vasp_package.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results={}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,text):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(text,encoding='utf-8',newline='\n')
def dump(p,obj): write(p,json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False))
def emit(k,v):
    results[k]=v
    dump(HERE/'results_ci.json',results)
    print(k,json.dumps(v,ensure_ascii=False,allow_nan=False),flush=True)
MH=sha(PKG/'MANIFEST.sha256')
emit('identity',{'manifest':MH,'tool':sha(SRC/'tools/wad/build_v5_vasp_package.py'),'verified_files':m.verify_manifest(str(PKG),MH)})
meta=json.loads((PKG/'jobs.json').read_text(encoding='utf-8'))
J={j['dir']:j for j in meta['jobs']}
with tempfile.TemporaryDirectory(prefix='ci_audit_', dir=HERE) as td:
    T = Path(td)
    ret = T / 'ret'
    run = ret / 'run'
    REF = {n: j['d3_2body_eV_ref'] for n,j in J.items()}
    E = {n: -1000.0 for n in J}
    dE = lambda w: w * J[m.PILOT_JOBS[0]]['area_A2'] * m.A2_M2 / m.EV_J
    for k,(b,f) in m.G5_SAMPLES.items():
        E[f] = E[b] + dE(.5)
    E['V5_s_outer_A_p05_bound'] = E['V5_s_outer_A_far'] - dE(.45)
    for tag,w in [('i', .505), ('ii', .509)]:
        E['V5_s_outer_A_G3_c2_far_'+tag] = E[m.G3_JOBS[0]] + dE(w)
    for tag,w in [('e70',.51),('k1',.49),('s05',.5)]:
        E[f'V5_s_outer_A_G4_{tag}_far'] = E[f'V5_s_outer_A_G4_{tag}_bound'] + dE(w)
    SPSHA = {p: hashlib.sha256(p.encode()).hexdigest() for p in m.POTCAR_MAP.values()}
    def mk(n, att='0', *, text=None, rc=0, extra='', sp=None, **kw):
        j = J[n]; d = run / (n if att == '0' else n+'_r1')
        # Clear only this explicitly resolved review-owned fixture directory.
        if d.exists():
            assert d.resolve().is_relative_to(T.resolve())
            shutil.rmtree(d)
        d.mkdir(parents=True)
        src = PKG / 'jobs' / n
        for f in ['POSCAR','KPOINTS']:
            shutil.copyfile(src / f, d / f)
        write(d/'INCAR', (src/('INCAR.r1' if att=='r1' else 'INCAR')).read_text(encoding='utf-8')+extra)
        write(d/'OUTCAR', text if text is not None else m._fake_outcar(j,E[n],REF[n],**kw))
        write(d/'OSZICAR', 'DAV: 1\n')
        ss = SPSHA if sp is None else sp
        ph = hashlib.sha256(''.join(ss[p] for p in j['potcar_spec']).encode()).hexdigest()
        write(d/'POTCAR.titel', ''.join(f' TITEL = {t}\n POMASS=1; ZVAL = {z:.3f}\n LEXCH = PE\n' for t,z in zip(j['pp_expected_titel'],j['zval_expected'])))
        write(d/'POTCAR.species.sha256', ''.join(f'{p} {ss[p]}\n' for p in j['potcar_spec']))
        write(d/'POTCAR.sha256', ph+'\n')
        dump(d/'attempt.json', {'job':n,'attempt':att,'run_id':f'20260927T120000-42-{list(J).index(n)+1}{1 if att=="r1" else 0}','t_start':100,'t_end':101,'rc':rc,
            'sha256':{**{f:sha(d/f) for f in ['INCAR','POSCAR','KPOINTS','OUTCAR','OSZICAR']}, 'POTCAR':ph}})
        return d
    def status(n, reg=None):
        return m.check(str(PKG),str(ret),MH,reg)[1][n]
    def collect(u=None, reg=None):
        try:
            r=m.collect(str(PKG),str(ret),MH,uma if u is None else u,reg)
        except m.PkgError as e:
            return {'blocked':str(e)}
        return {'G3':r['G3'], 'G4':r['G4'], 'G5':r['G5'], 'rc':m.collect_exit(r), 'jobs_not_ok':r['jobs_not_ok']}
    for n in J: mk(n)
    uma={'schema':'uma_energies/v1','calculator':{'model':m.UMA_REQ['model'],'task':m.UMA_REQ['task'],'inference_settings':'default',
        'fairchem.core':'2.21.0','checkpoint':[{'sha256':m.UMA_REQ['checkpoint_sha256']}]},'energies':{}}
    for n,j in J.items():
        uma['energies'].setdefault(j['structure'], {'sha256':j['structure_sha256'],'n_atoms':j['nions'],'pbc':[True,True,True], 'E_UMA_eV':E[n]-REF[n]})

    reg=m.seal_pp(str(PKG),str(ret),MH)
    F=m.PILOT_JOBS[1]
    emit('positive_sealed',collect(reg=reg))
    up=T/'uma.json';rp=T/'registry.json';dump(up,uma);dump(rp,reg)
    cli=[sys.executable,str(SRC/'tools/wad/build_v5_vasp_package.py'),'--collect','--out',str(PKG),'--ret',str(ret),'--manifest_sha256',MH,'--uma',str(up),'--pp_registry',str(rp),'--pp_registry_sha256',sha(rp)]
    def cli_status():
        cp=subprocess.run(cli,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60)
        return {'rc':cp.returncode,'tail':(cp.stdout+cp.stderr)[-900:]}
    emit('positive_cli',cli_status())
    d=run/F;a=json.loads((d/'attempt.json').read_text());a['run_id']='20260928T120000-99-456';dump(d/'attempt.json',a)
    emit('pilot_replaced_id',{'status':status(F,reg)['status'],'unsealed_status':status(F)['status'],'cli':cli_status()})
    mk(F);d=run/F;write(d/'OUTCAR',(d/'OUTCAR').read_text()+'\n')
    a=json.loads((d/'attempt.json').read_text());a['sha256']['OUTCAR']=sha(d/'OUTCAR');dump(d/'attempt.json',a)
    emit('pilot_same_id_changed_output',{'status':status(F,reg)['status'],'unsealed_status':status(F)['status'],'cli':cli_status()})
    mk(F)
    good=m._fake_outcar(J[F],E[F],REF[F])
    partials={}
    expected=J[F]['pp_expected_titel']
    for label,ts,rc,full in [
        ('prefix1_rc1',expected[:1],1,False),('prefix3_rc1',expected[:3],1,False),
        ('wrong_order_rc1',expected[1:2]+expected[:1],1,False),
        ('wrong_date_rc1',[expected[0][:-4]+'2099'],1,False),
        ('extra_species_rc1',expected+['PAW_PBE Fe 06Sep2000'],1,False),
        ('half_line_rc1',[expected[0][:-4]],1,False),
        ('successful_prefix2',expected[:2],0,True)]:
        if full:
            text=re.sub(r'^.*TITEL.*\n','',good,flags=re.M)
            text=text.replace(m.DEFAULT_FAKE_VERSION,m.DEFAULT_FAKE_VERSION+'\n'+''.join(' TITEL = '+x+'\n' for x in ts),1)
        else:text=' '+m.DEFAULT_FAKE_VERSION+'\n'+''.join(' TITEL = '+x+'\n' for x in ts)
        mk(F,text=text,rc=rc);mk(F,'r1')
        r=status(F);partials[label]={k:r.get(k) for k in ('status','attempt','r1_ignored','conflicts')}
        shutil.rmtree(run/(F+'_r1'));mk(F)
    emit('titel_paths',partials)
    mk(F,text=' '+m.DEFAULT_FAKE_VERSION+'\n TITEL = '+expected[0]+'\n',rc=1);mk(F,'r1')
    r1reg=m.seal_pp(str(PKG),str(ret),MH)
    emit('r1_seal_reuse',{'fresh_registry':status(F,r1reg)['status'],'old_registry':status(F,reg)['status'],'selected_attempt':status(F,r1reg).get('attempt')})
    shutil.rmtree(run/(F+'_r1'));mk(F)
    regressions={}
    for label,kw in [('encut400_rc1',{'encut':400,'rc':1}),('encut400_nonconv',{'encut':400,'conv':False}),('other_pp_rc1',{'rc':1,'sp':{**SPSHA,'Ag':'f'*64}})]:
        mk(F,**kw);mk(F,'r1');r=status(F)
        regressions[label]={'status':r['status'],'r1_ignored':r.get('r1_ignored')}
        shutil.rmtree(run/(F+'_r1'));mk(F)
    emit('contradiction_not_rescued',regressions)
    blanks={}
    for label,suffix in [('TOTEN',' free energy TOTEN ='),('sigma0',' energy(sigma->0) ='),('noentropy',' energy without entropy ='),('Edisp',' Edisp (eV)'),('Edisp_nextline',' Edisp (eV)\nFREE ENERGIE')]:
        mk(F,text=good+'\n'+suffix);r=status(F)
        blanks[label]={'status':r['status'],'parsed':{k:v for k,v in m.parse_outcar(good+'\n'+suffix).items() if k in ('TOTEN_eV','E_sigma0_eV','E_noentropy_eV','Edisp_eV')}}
    emit('empty_final_records',blanks);mk(F)
    raw=gzip.decompress((SRC/m.REAL_OUTCAR_544_SRC).read_bytes()).decode('utf-8')
    o=m.parse_outcar(raw)
    emit('actual_raw_outcar',{k:o[k] for k in ('version','TOTEN_eV','E_sigma0_eV','Edisp_eV')})
    emit('actual_dipol_evidence',m.dipol_evidence(o,m.REAL_OUTCAR_544_DIPOL_Z))
    fake=T/'fake_vasp.py';write(fake,m.FAKE_VASP)
    pp=T/'pp'
    for s in m.SPECIES_ORDER:
        write(pp/m.POTCAR_MAP[s]/'POTCAR',f' {m.PP_EXPECTED_TITEL[s]}\n TITEL = {m.PP_EXPECTED_TITEL[s]}\n POMASS = 1; ZVAL = {m.ZVAL[s]:.3f}\n LEXCH = PE\n')
    baseenv={**os.environ,'POTCAR_DIR':pp.as_posix(),'FAKE_TOOLDIR':(SRC/'tools/wad').as_posix(),'FAKE_PKG':PKG.as_posix(),
        'JOBS':' '.join(m.PILOT_JOBS),'VASP_CMD':f'{Path(sys.executable).as_posix()} {fake.as_posix()}',
        'PYTHONUTF8':'1','PYTHONDONTWRITEBYTECODE':'1'}
    baseenv.pop('BASH_ENV',None)
    if os.name=='nt':
        baseenv['PATH']=str(Path(args.bash).resolve().parent.parent/'usr/bin')+os.pathsep+baseenv.get('PATH','')
    def runpkg(label,changes=None,existing=None):
        w=existing or T/('runner_'+label)
        if existing is None:shutil.copytree(PKG,w)
        cp=subprocess.run([args.bash,(w/'run_all.sh').as_posix()],env={**baseenv,**(changes or {})},capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
        tg=w/'V5_vasp_return.tgz'
        names=[]
        if tg.exists():
            with tarfile.open(tg) as tf:names=tf.getnames()
        return w,{'rc':cp.returncode,'members':names,'forbidden':[n for n in names if Path(n).name in m.RETURN_FORBIDDEN],'tail':(cp.stdout+cp.stderr)[-1400:]}
    w,rr=runpkg('positive');emit('runner_positive',rr)
    sealed=m.seal_pp(str(PKG),str(w),MH)
    emit('runner_seal_reuse',{n:m.check(str(PKG),str(w),MH,sealed)[1][n]['status'] for n in m.PILOT_JOBS})
    shacheck=T/'sha_check.sh';write(shacheck,'#!/usr/bin/env bash\nsha256sum -c V5_vasp_return.tgz.sha256\n')
    c=subprocess.run([args.bash,shacheck.as_posix()],cwd=w,env=baseenv,capture_output=True,text=True)
    emit('runner_sha_check',{'rc':c.returncode,'output':c.stdout,'stderr':c.stderr})
    for f in m.RETURN_FORBIDDEN:write(w/'run'/F/f,'REVIEW_DUMMY_NOT_POTENTIAL_DATA')
    before={str(p.relative_to(w)):sha(p) for p in (w/'run').rglob('*') if p.is_file() and p.name not in ('env.txt',)}
    _,rr=runpkg('pack_only',{'PACK_ONLY':'1','VASP_CMD':'','POTCAR_DIR':''},w)
    after={str(p.relative_to(w)):sha(p) for p in (w/'run').rglob('*') if p.is_file() and p.name not in ('env.txt',)}
    emit('runner_pack_only',{'result':rr,'files_unchanged':before==after,'reported':m.return_manifest_info(str(w),MH)['forbidden_files']})
    partialpp=T/'partialpp';shutil.copytree(pp/'Li_sv',partialpp/'Li_sv')
    wf,rr=runpkg('missing_pp',{'POTCAR_DIR':partialpp.as_posix()})
    emit('runner_partial_pp_failure',{'result':rr,'potcar_left':list(map(str,(wf/'run').rglob('POTCAR')))})
    # Failure injection only in subprocess tool calls, not production source.
    # Simulates an I/O failure of find, sort, tar-create, tar-list, or second rename.
    # No VASP commands run in these PACK_ONLY tests.
    injections={
       'find_failure':'find(){ echo REVIEW_FIND_FAILURE >&2; return 73; }\n',
       'sort_failure':'sort(){ echo REVIEW_SORT_FAILURE >&2; return 73; }\n',
       'tar_create_failure':'tar(){ echo REVIEW_TAR_CREATE_FAILURE >&2; return 73; }\n',
       'tar_list_failure':'tar(){ if [ "$1" = tzf ]; then echo REVIEW_TAR_LIST_FAILURE >&2; return 73; fi; command tar "$@"; }\n',
       'second_mv_failure':'mv(){ case "$*" in *sha256.part*) echo REVIEW_MV_FAILURE >&2; return 73;; esac; command mv "$@"; }\n',
    }
    saved={f:(w/f).read_bytes() for f in ('V5_vasp_return.tgz','V5_vasp_return.tgz.sha256')}
    for label,body in injections.items():
        for f,b in saved.items():(w/f).write_bytes(b)
        sh=T/(label+'.sh');write(sh,body)
        _,rr=runpkg(label,{'PACK_ONLY':'1','BASH_ENV':sh.as_posix()},w)
        rr['old_pair_preserved']=all((w/f).read_bytes()==b for f,b in saved.items())
        emit(label,rr)
    emit('done',{'note':'Synthetic calculations only; source unchanged; temporary fixtures removed on exit.'})
    if args.assert_fixed:
        for label in ('find_failure','sort_failure','tar_list_failure'):
            assert results[label]['rc']==4 and results[label]['old_pair_preserved'], (label,results[label])
