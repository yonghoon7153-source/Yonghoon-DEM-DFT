"""CJ semantic review: synthetic fixtures only, no VASP/UMA/DFT calculations.
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
    dump(HERE/'semantic_cj_results.json',results)
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
    F=m.PILOT_JOBS[1];tl=J[F]['pp_expected_titel']
    cases={}
    for label,ts,rc,term,r1 in [
       ('partial_last_failed',tl[:2]+[tl[2][:12]],1,False,True),
       ('partial_last_success',tl[:2]+[tl[2][:12]],0,True,True),
       ('last_of_full_list_truncated',tl[:-1]+[tl[-1][:-4]],0,True,False),
       ('wrong_species_partial',[tl[0],'PAW_PBE S'],1,False,True),
       ('complete_prefix_failed',tl[:2],1,False,True),
       ('complete_prefix_success',tl[:2],0,True,True),
    ]:
        mk(F,text=m._fake_outcar(J[F],E[F],REF[F],titel_override=ts,term=term),rc=rc)
        if r1:mk(F,'r1')
        rr=status(F);cases[label]={k:rr.get(k) for k in ('status','attempt','why','r1_ignored')}
        if (run/(F+'_r1')).exists():shutil.rmtree(run/(F+'_r1'))
        mk(F)
    emit('titel_boundary',cases)
    n='V5_li_outer_A_far'
    good=m._fake_outcar(J[n],E[n],REF[n])
    mk(n,text=good+'\n energy without entropy =')
    rr=m.collect(str(PKG),str(ret),MH,uma,reg)
    emit('noentropy_missing_nonpilot',{'job_status':rr['jobs'][n]['status'],'E_noentropy_eV':rr['jobs'][n]['E_noentropy_eV'],
      'G5_status':rr['G5']['status'],'samples':{k:{x:v[x] for x in ('W_J_m2','W_sigma0_J_m2','mTS_term_J_m2')} for k,v in rr['samples'].items() if n in (v['bound'],v['far'])}})
    mk(n)
    text=re.sub(r'(energy\s+without\s+entropy\s*=)\s*\S+',r'\g<1> 0.00000000',good)
    mk(n,text=text);rr=m.collect(str(PKG),str(ret),MH,uma,reg)
    emit('noentropy_zero_nonpilot',{'job_status':rr['jobs'][n]['status'],'E_noentropy_eV':rr['jobs'][n]['E_noentropy_eV'],
      'samples':{k:v['mTS_term_J_m2'] for k,v in rr['samples'].items() if n in (v['bound'],v['far'])}})
    emit('finished','No actual scientific calculation.')
