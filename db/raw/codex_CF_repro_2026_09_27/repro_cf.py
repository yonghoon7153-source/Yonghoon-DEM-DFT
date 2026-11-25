"""Read-only CF audit, e025c0db7. Synthetic outputs; no VASP/UMA/DFT runs."""
import contextlib, copy, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SRC = HERE / 'source'
PKG = SRC / 'db/inputs/wad_aprime_v5_vasp_2026_09_27'
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE / '.review_bz_deps'))
asepath = BASE / 'work/ad_v10_pydeps/ase/__init__.py'
spec = importlib.util.spec_from_file_location('ase', asepath, submodule_search_locations=[str(asepath.parent)])
ase = importlib.util.module_from_spec(spec)
sys.modules['ase'] = ase
spec.loader.exec_module(ase)
import numpy as np
from ase.io import read
spec = importlib.util.spec_from_file_location('cf_target', SRC / 'tools/wad/build_v5_vasp_package.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
results = {}
def emit(k, v):
    results[k] = v
    print(k, json.dumps(v, ensure_ascii=False, allow_nan=False), flush=True)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, text):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(text, encoding='utf-8', newline='\n')
def dump(p, obj):
    write(p, json.dumps(obj, ensure_ascii=False, indent=2))

prompt = Path('C:/Users/Administrator/Downloads/codex_CF_prompt_wad_aprime_v5_vasp_outsourcing_v2_2026_09_27.md').read_text(encoding='utf-8')
declared = re.findall(r'^((?:db|tools|kb)/\S+)\s+([0-9a-f]{64})$', prompt, re.M)
emit('declared_hashes', {p: sha(SRC / p) == h for p,h in declared})
MH = sha(PKG / 'MANIFEST.sha256')
emit('manifest_files_verified', m.verify_manifest(str(PKG), MH))
meta = json.loads((PKG / 'jobs.json').read_text(encoding='utf-8'))
J = {j['dir']: j for j in meta['jobs']}
geom = []
for n,j in J.items():
    a = read(SRC / meta['source_package'] / 'structures' / (j['structure'] + '.extxyz'))
    b = read(PKG / 'jobs' / n / 'POSCAR', format='vasp')
    _, order, _ = m.poscar_text(a, 'review')
    geom.append({'job': n, 'source_sha_ok': sha(SRC / meta['source_package'] / 'structures' / (j['structure'] + '.extxyz')) == j['structure_sha256'],
                 'max_pos_diff_A': float(np.max(np.abs(a.positions[order]-b.positions))),
                 'max_cell_diff_A': float(np.max(np.abs(a.cell.array-b.cell.array))),
                 'order_ok': order == j['poscar_order_to_original_index']})
emit('geometry', geom)
log = io.StringIO()
try:
    with contextlib.redirect_stdout(log):
        rc = m._selftest()
    emit('native_selftest', {'rc': rc, 'log': log.getvalue()})
except Exception as e:
    emit('native_selftest', {'not_completed': repr(e), 'log': log.getvalue()})

with tempfile.TemporaryDirectory(prefix='cf_audit_', dir=HERE) as td:
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
        dump(d/'attempt.json', {'job':n,'attempt':att,'run_id':f'fixture-{n}-{att}','rc':rc,
            'sha256':{**{f:sha(d/f) for f in ['INCAR','POSCAR','KPOINTS','OUTCAR','OSZICAR']}, 'POTCAR':ph}})
        return d
    def status(n, reg=None):
        return m.check(str(PKG),str(ret),MH,reg)[1][n]
    def collect(u=None, reg=None):
        r=m.collect(str(PKG),str(ret),MH,uma if u is None else u,reg)
        return {'G3':r['G3'], 'G4':r['G4'], 'G5':r['G5'], 'rc':m.collect_exit(r), 'jobs_not_ok':r['jobs_not_ok']}
    for n in J: mk(n)
    uma={'schema':'uma_energies/v1','calculator':{'model':m.UMA_REQ['model'],'task':m.UMA_REQ['task'],'inference_settings':'default',
        'fairchem.core':'2.21.0','checkpoint':[{'sha256':m.UMA_REQ['checkpoint_sha256']}]},'energies':{}}
    for n,j in J.items():
        uma['energies'].setdefault(j['structure'], {'sha256':j['structure_sha256'],'n_atoms':j['nions'],'pbc':[True,True,True], 'E_UMA_eV':E[n]-REF[n]})
    emit('positive', collect())
    reg=m.seal_pp(str(PKG),str(ret),MH)
    emit('positive_sealed', collect(reg=reg))
    F='V5_s_outer_A_far'
    # All of these are expected to be blocked in CE; inputs/record hashes stay internally consistent.
    oldcases={}
    for label,kw in [('semicolon',{'extra':'NCORE = 1 ; EFIELD = 0.01\n'}),('rc1',{'rc':1}),('concat',{'extra_run':True}),
                     ('encut400',{'encut':400}),('nelect_absent',{'drop':('NELECT',)}),('d3_absent',{'edisp':False})]:
        mk(F,**kw); oldcases[label]=status(F)['status']; mk(F)
    dd=mk(F); (dd/'POTCAR.sha256').unlink(); oldcases['pp_sha_absent']=status(F)['status'];mk(F)
    dd=mk(F);write(dd/'OUTCAR',(dd/'OUTCAR').read_text(encoding='utf-8')+'\n');oldcases['outcar_changed']=status(F)['status'];mk(F)
    un=copy.deepcopy(uma)
    for row in un['energies'].values():row['E_UMA_eV']=float('nan')
    oldcases['all_nan']=collect(u=un)['G5']['status']
    un=copy.deepcopy(uma);un['calculator']['task']='omol';oldcases['wrong_task']=collect(u=un)['G5']['status']
    emit('CE_direct_regressions', oldcases)
    # Mixed defect + nonconvergence/rc path must not wash out a settings or PP violation.
    mk(F,encut=400,rc=1); mk(F,'r1');emit('bad_settings_and_rc1_rescued', status(F,reg))
    mk(F,encut=400,conv=False);emit('bad_settings_and_nonconv_rescued', status(F,reg))
    mk(F,rc=1,sp={**SPSHA,'Ag':'f'*64});emit('bad_pp_and_rc1_rescued',status(F,reg))
    rd=run/(F+'_r1'); assert rd.resolve().is_relative_to(T.resolve());shutil.rmtree(rd);mk(F)
    # Registry is omitted or semantically incomplete; valid final data must not authorize use.
    emit('no_pp_registry', collect())
    emit('empty_pp_registry', collect(reg={}))
    badreg=copy.deepcopy(reg);badreg['schema']='nonsense';badreg['package_manifest_sha256']='0'*64
    badreg.pop('vasp_version');badreg.pop('assembled_sha256')
    emit('invalid_registry_metadata', collect(reg=badreg))
    # Same fixed geometry => same D3 term; a D3 drift can conceal G4 nonconvergence.
    G='V5_s_outer_A_G4_e70_far';gb='V5_s_outer_A_G4_e70_bound'
    e_true=E[gb]+dE(.521)
    mk(G,text=m._fake_outcar(J[G],e_true,REF[G]));emit('G4_true_021',collect(reg=reg))
    err=dE(-.002)
    mk(G,text=m._fake_outcar(J[G],e_true+err,REF[G]+err))
    emit('G4_masked_by_D3',{'D3_shift_eV':err,'relative_ED_shift':abs(err/REF[G]),'result':collect(reg=reg)})
    mk(G)
    # Structured numeric parse failures: malformed/non-finite final values must not fall back to earlier records.
    good=m._fake_outcar(J[F],E[F],REF[F])
    mk(F,text=good.replace('ISMEAR =     1;', 'ISMEAR =     1;').replace('0.14  broadening','0.14  broadening'))
    # A malformed final TOTEN is skipped and an earlier TOTEN is silently used.
    malformed=good.replace(' General timing', ' free  energy   TOTEN  =  NaN eV\n General timing')
    mk(F,text=malformed);emit('nonfinite_final_TOTEN',status(F,reg));mk(F)
    # Drop execution identity fields without affecting hashes.
    d=run/F;a=json.loads((d/'attempt.json').read_text());a.pop('run_id');dump(d/'attempt.json',a)
    emit('missing_run_id',status(F,reg));mk(F)
    # Check G3 budget and the restricted diagnostic independently of native selftest.
    G=m.G3_JOBS[2]
    mk(G,text=m._fake_outcar(J[G],E[G]+dE(.0015),REF[G]+dE(.0015)))
    emit('G3_D3_budget_blocks',collect(reg=reg));mk(G)
    mk(G,text=m._fake_outcar(J[G],E[m.G3_JOBS[0]]+dE(.512),REF[G]))
    emit('G3_FAIL_keeps_raw_only',collect(reg=reg));mk(G)
    # CLI registry checks, including the hash-valid but empty registry.
    up=T/'uma.json'; dump(up,uma)
    er=T/'empty_registry.json';dump(er,{})
    cli=[sys.executable,str(SRC/'tools/wad/build_v5_vasp_package.py'),'--collect','--out',str(PKG),'--ret',str(ret),
         '--manifest_sha256',MH,'--uma',str(up)]
    cli_results={}
    for label, extra in [('absent',[]),('empty_with_matching_sha',['--pp_registry',str(er),'--pp_registry_sha256',sha(er)])]:
        cp=subprocess.run(cli+extra, text=True, encoding='utf-8',capture_output=True,timeout=60)
        cli_results[label]={'rc':cp.returncode,'last_line':cp.stdout.splitlines()[-1] if cp.stdout else cp.stderr[-500:]}
    emit('registry_cli',cli_results)
    # Exercise the unmodified deployed bash runner with Python fake VASP only.
    fake=T/'fake_vasp.py';write(fake,m.FAKE_VASP)
    pp=T/'pp'
    for s in m.SPECIES_ORDER:
        write(pp/m.POTCAR_MAP[s]/'POTCAR',f' {m.PP_EXPECTED_TITEL[s]}\n TITEL = {m.PP_EXPECTED_TITEL[s]}\n POMASS = 1; ZVAL = {m.ZVAL[s]:.3f}\n LEXCH = PE\n')
    perf=T/'perf';write(perf,'NCORE = 4\nKPAR = 1\n')
    badperf=T/'badperf';write(badperf,'NCORE = 1 ; EFIELD = 0.01\n')
    bash='C:/Program Files/Git/bin/bash.exe'
    baseenv={**os.environ,'POTCAR_DIR':pp.as_posix(),'FAKE_TOOLDIR':(SRC/'tools/wad').as_posix(),'FAKE_PKG':PKG.as_posix(),
             'JOBS':' '.join(m.PILOT_JOBS),'VASP_CMD':f'{Path(sys.executable).as_posix()} {fake.as_posix()}',
             'PERF_TAGS_FILE':perf.as_posix(),'PYTHONUTF8':'1','PYTHONDONTWRITEBYTECODE':'1'}
    def runpkg(label,changes=None,existing=None):
        w=existing if existing is not None else T/('runner_'+label)
        if existing is None:shutil.copytree(PKG,w)
        cp=subprocess.run([bash,(w/'run_all.sh').as_posix()],env={**baseenv,**(changes or {})},capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
        rs=m.check(str(PKG),str(w),MH)[1]
        return w, {'rc':cp.returncode,'pilot':{p:{k:rs[p].get(k) for k in ['status','attempt','first_attempt','r1','why']} for p in m.PILOT_JOBS},
                    'tgz_exists':(w/'V5_vasp_return.tgz').exists(),'log_tail':(cp.stdout+cp.stderr)[-750:]}
    w,rr=runpkg('ok');emit('runner_positive',rr)
    _,rr=runpkg('repeat',existing=w);emit('runner_repeat',rr)
    for label,env in [('false',{'VASP_CMD':'false'}),('badperf',{'PERF_TAGS_FILE':badperf.as_posix()}),
                      ('rescue',{'FAKE_MODE':'noconv_unless_amix'}),('rc1',{'FAKE_MODE':'rc1'}),
                      ('missing_perf',{'PERF_TAGS_FILE':(T/'missing').as_posix()}),('missing_pp',{'POTCAR_DIR':(T/'missingpp').as_posix()})]:
        _,rr=runpkg(label,env);emit('runner_'+label,rr)
    # Shell archive failure: force tar failure without changing production code.
    shims=T/'shims';write(shims/'tar','#!/usr/bin/env bash\necho REVIEW_TAR_FAILURE >&2\nexit 73\n')
    env_sh=T/'bash_env';write(env_sh,'export PATH="/c/'+shims.as_posix()[3:]+':$PATH"\n')
    _,rr=runpkg('tar_failure',{'BASH_ENV':env_sh.as_posix()});emit('runner_tar_failure',rr)
    # Keep detailed fixture-independent results, no materialized synthetic calculation masquerading as real output.
    dump(HERE/'results.json',results)
