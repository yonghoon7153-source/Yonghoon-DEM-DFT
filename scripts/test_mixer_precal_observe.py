"""Small synthetic observation contracts; no simulator or research data."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import shutil
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('mixer_precal_observe', HERE/'mixer_precal_observe.py')
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)


def data(n=3):
    return dict(id=np.arange(1, n+1, dtype=float),
                type=np.array(([1, 2]+[3]*(n-2)) if n >= 2 else [3], dtype=float),
                x=np.arange(n, dtype=float)*0.01, y=np.zeros(n), z=np.zeros(n),
                radius=np.full(n, 0.001))


def binding(n=3, role='E0'):
    ph = {p: dict(type=i, radius_m=.001) for i, p in enumerate(('AM_P','AM_S','SE'), 1)}
    rev = 0 if role == 'E0' else 2
    return dict(case_id='PRECAL_E0' if role == 'E0' else 'PRECAL_R1_B1_U', role=role,
                phases=ph, n_planned=n, expected_counts={'1':1,'2':1,'3':n-2},
                revolutions=rev, seed=32452843, r_container=.5, axis='x', np_proposed=20,
                density_generation='lab20261014',
                geometry=dict(axis='x', r_container=.5, length=.2, cgf=151.4),
                frame_pm=dict(phases=ph, n_planned=n, revolutions=rev,
                              meta_steps=dict(t0_planned=200, dump_every=50),
                              arm='synthetic', seed=32452843, n_expected_file=None))


def stats(value):
    return dict(s2=value, used=2, dropped=0, p=np.array([0.,1.]), n=40,
                vol_kept_by_type={1:1.,2:1.,3:1.}, nonempty=2, s2_all=value,
                am_vol_kept=1.,se_vol_kept=1.,am_n_kept=1.,se_n_kept=1.,cell_n_median=20.)


def completion_log(runs, n=3):
    total=0;lines=[]
    for r in runs:
        total+=r
        lines.extend(['Step Atoms KinEng c_rke Volume',
                      '%d %d 0 0 1'%(total,n),
                      'Loop time of 1 on 20 procs for %d steps with %d atoms'%(r,n)])
    return '\n'.join(lines)+'\n'


# Actual log.liggghts text form of the sealed build (LIGGGHTS-PUBLIC 3.8.0, git 3d5c00f),
# registration draft 7-4.  Every line form below is copied from same-build logs in this
# repository, not invented:
#  - thermo header for `thermo_style custom step atoms ke c_rke vol` has no c_ prefix and every
#    Loop line ends with a ctime finish stamp: docs/data/mixer_highbo_devu_prelim_20261006/
#    exact_runs/exact_LU212_settled/log.exact L65-67 (same thermo_style line as the deck);
#  - fix insert/pack writes a two-line report inside the thermo table of the run that inserts:
#    docs/data/kg50_d07_end_20261105/kg50_d07_b50_log_ins1.liggghts L116-121;
#  - log.liggghts echoes every input line, comments included (the kg50 logs carry 48-54 '#'
#    lines each), so the planned deck comment L34 that quotes `ERROR:` is echoed verbatim.
ACTUAL_HEADER = '    Step    Atoms         KinEng            rke         Volume '
ACTUAL_FINISH = ', finish time Tue Oct  6 19:30:09 2026'
ERROR_COMMENT = '#   (`ERROR: youngsModulus <= 1e9 required for SI units`, global_properties.cpp:371).'
INSERT_FIX = ('fix ins all insert/pack seed 32452843 distributiontemplate pdd &\n'
              '    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &\n'
              '    region ins_reg particles_in_region 3 ntry_mc 20000\n')
SMALL_DECK = ('timestep 0.01\nfix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 2\n'
              'dump dmp all custom 50 post/dump_*.liggghts id type x y z radius\nrun 1\nrun 100\nrun 100\nrun 0\n')
E0_DECK = ('docs', 'reviews', 'mixer_first8_launch_preparation_20261106', 'planned_assets', 'PRECAL_E0', 'in.mixer')
E0_DECK_SHA256 = '8b588b24117ab77bf72d93662237268b401f714df8515d62ef7b964d01c6e718'


def actual_row(step, atoms):
    # Thermo row of this build: %8d %8d then %14.8g per float column and a trailing space.
    ke, rke = (3.2685651e-12, 1.0960987e-10) if atoms else (0., 0.)
    return '%8d %8d %14.8g %14.8g %14.8g ' % (step, atoms, ke, rke, 2.7589053e-05)


def actual_log(deck_text, inserted, procs=20):
    """Synthetic log.liggghts in the sealed build's form for `deck_text`.

    Echoes every input line ('&' continuations joined) and, at each `run`, writes the setup
    lines, the thermo table (setup row, every `thermo` steps, end row), the insertion report
    after the setup row of the first run that follows an insert/pack fix, the Loop line with
    its finish stamp and the timing summary.  `inserted` maps fix id -> particles placed."""
    out = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-03-26-14:37:06 by builder, '
           'git commit 3d5c00f20519e6bb6eb6756f51f1ad36564e649d)']
    lines = deck_text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    step = atoms = every = 0
    pending, started, i = [], set(), 0
    while i < len(lines):
        logical = lines[i].rstrip(); i += 1
        while logical.endswith('&') and not logical.lstrip().startswith('#') and i < len(lines):
            logical = logical[:-1]+' '+lines[i].rstrip(); i += 1
        out.append(logical)
        tokens = logical.split('#')[0].split()
        if tokens[:1] == ['thermo'] and len(tokens) == 2:
            every = int(tokens[1])
        elif tokens[:1] == ['fix'] and len(tokens) > 3 and tokens[3] == 'insert/pack':
            pending.append(tokens[1])
        elif tokens[:1] == ['run']:
            n = int(tokens[1]); start, end = step, step+n
            out += ['Setting up run at Tue Oct  6 15:00:00 2026', '']
            for fix in pending:
                if fix not in started:
                    out.append('INFO: Particle insertion %s: inserting every 0 steps' % fix); started.add(fix)
            out += ['Memory usage per processor = 102.09 Mbytes', ACTUAL_HEADER, actual_row(start, atoms)]
            if n and pending:
                for fix in pending:
                    k = inserted[fix]; atoms += k
                    out += ['INFO: Particle insertion %s: inserted %d particle templates (mass %e) at step %d'
                            % (fix, k, 1e-4*k, start+1),
                            ' - a total of %d particle templates (mass %e) inserted so far.' % (k, 1e-4*k)]
                pending = []
            if every:
                out += [actual_row(s, atoms) for s in range((start//every+1)*every, end, every)]
            if end != start:
                out.append(actual_row(end, atoms))
            out.append('Loop time of 1.25 on %d procs for %d steps with %d atoms%s' % (procs, n, atoms, ACTUAL_FINISH))
            out += ['', '', 'Pair  time (%) = 0 (0)', 'Neigh time (%) = 0 (0)', 'Comm  time (%) = 0 (0)',
                    'Outpt time (%) = 0 (0)', 'Other time (%) = 1.25 (100)', '',
                    'Nlocal:    %d ave %d max %d min' % (atoms, atoms, atoms), 'Histogram: 1 0 0 0 0 0 0 0 0 0', '',
                    'Total # of neighbors = 0', 'Ave neighs/atom = 0', 'Neighbor list builds = 0',
                    'Dangerous builds = 0']
            step = end
    return '\n'.join(out)+'\n'


def write_dump(path, step, D):
    text = 'ITEM: TIMESTEP\n%d\nITEM: NUMBER OF ATOMS\n%d\nITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\nITEM: ATOMS id type x y z radius\n' % (step, len(D['id']))
    text += ''.join(' '.join('%.17g' % D[k][i] for k in ('id', 'type', 'x', 'y', 'z', 'radius'))+'\n' for i in range(len(D['id'])))
    path.write_text(text)


class SourceBoundary(unittest.TestCase):
    def child(self, action, before_import=""):

        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            names=('mixer_precal_observe','mixer_precal_prepare','mixer_contact_reader',
                   'measure_mixing_index','measure_bed_aspect','make_mixer_deck',
                   'mixer_deck_readback','mixer_deck_diff','make_mixer_resume',
                   'test_mixer_precal_observe')
            for name in names:shutil.copyfile(HERE/(name+'.py'),root/(name+'.py'))
            code="""import sys,json,importlib.util
from pathlib import Path
sys.path.insert(0,sys.argv[1])
"""+before_import+"""
import test_mixer_precal_observe as T
O=T.O
fixture=T.DiskContract();fixture.setUp()
run,B=fixture.make_run('e0')
"""+action+"""
result=fixture.invoke(run,B)
print(json.dumps({'status':result['status'],'reasons':result['reasons']}))
fixture.doCleanups()
"""
            proc=subprocess.run([sys.executable,'-I','-B','-c',code,str(root)],
                                text=True,capture_output=True,timeout=20)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertFalse(list(root.rglob('*.pyc')))
            return json.loads(proc.stdout)

    def test_import_then_dependency_disk_change(self):
        got=self.child("p=Path(sys.argv[1])/'mixer_contact_reader.py'\np.write_bytes(p.read_bytes()+b'\\nSENTINEL_PRE8=1\\n')\n")
        self.assertEqual(got['status'],'TECH',got)

    def test_import_then_observer_disk_change(self):
        got=self.child("p=Path(sys.argv[1])/'mixer_precal_observe.py'\np.write_bytes(p.read_bytes()+b'\\n# changed self\\n')\n")
        self.assertEqual(got['status'],'TECH',got)

    def test_fresh_registry_ignores_stale_canonical_modules(self):
        before="""import types
names=('mixer_precal_prepare','mixer_contact_reader','measure_mixing_index',
       'measure_bed_aspect','make_mixer_deck','mixer_deck_readback','mixer_deck_diff','make_mixer_resume')
stale={n:types.ModuleType(n) for n in names}
sys.modules.update(stale)
"""
        action="""assert all(sys.modules[n] is stale[n] for n in names)
assert all(O._REGISTRY[n] is not stale[n] for n in names)
assert O.preparation.gen is O._REGISTRY['make_mixer_deck']
assert O.preparation.diff.logical_commands is O._REGISTRY['make_mixer_resume'].logical_commands
assert O.contact.frame_quantities.__globals__ is O.contact.__dict__
"""
        self.assertEqual(self.child(action,before)['status'],'OK')

    def test_observer_executing_code_must_match_captured_bytes(self):
        before="""from unittest import mock
original_read=Path.read_bytes
def changed_read(path):
    raw=original_read(path)
    return raw+b'\\nSOURCE_BOUNDARY_SENTINEL=1\\n' if path.name=='mixer_precal_observe.py' else raw
patcher=mock.patch.object(Path,'read_bytes',changed_read);patcher.start()
"""
        self.assertEqual(self.child('patcher.stop()\n',before)['status'],'TECH')

    def test_fresh_process_executes_the_new_captured_dependency(self):
        before="""p=Path(sys.argv[1])/'mixer_contact_reader.py'
with p.open('a') as stream:
    stream.write('\\n_original_frame=frame_quantities\\ndef frame_quantities(*args):\\n    out=_original_frame(*args)\\n    out["fresh_source_sentinel"]=991\\n    return out\\n')
"""
        action="""assert O.contact.frame_quantities(T.data(),T.binding()['frame_pm'])['fresh_source_sentinel']==991
assert O._BOUND_RAW['mixer_contact_reader']==(Path(sys.argv[1])/'mixer_contact_reader.py').read_bytes()
"""
        self.assertEqual(self.child(action,before)['status'],'OK')

    def test_generator_source_open_is_captured(self):
        action="""p=Path(sys.argv[1])/'make_mixer_deck.py'
raw=p.read_bytes();p.write_bytes(raw+b'\\n# temporary ABA\\n')
try:
    with O.preparation.gen.__dict__['__builtins__']['open'](str(p),'rb') as stream:
        assert stream.read()==raw
finally:p.write_bytes(raw)
"""
        self.assertEqual(self.child(action)['status'],'OK')



class Qualification(unittest.TestCase):
    def test_d13_zero_ten_eleven_and_excess(self):
        D=data(3)
        for missing in (0,10):
            B=binding(3+missing)
            got=O.qualify_arrays([D], B)
            self.assertEqual(got['initial_missing'], missing)
            self.assertEqual(got['planned_total'], 3+missing)
            self.assertEqual(got['observed_total'], 3)
        for n in (14,2):
            with self.assertRaises(O.Tech): O.qualify_arrays([D], binding(n))

    def test_id_sequence_type_radius_and_late_change(self):
        for key, values in [('id',[1,2,4]),('id',[1,1,3]),('id',[1,2,3.5]),
                            ('type',[1,2,4]),('type',[1,2,3.2]),
                            ('radius',[.001,.001,.002]),('x',[0.,float('nan'),.1])]:
            D=data(); D[key]=np.array(values)
            with self.subTest(key=key,values=values):
                with self.assertRaises(O.Tech): O.qualify_arrays([D],binding())
        for key,value in [('id',4),('type',1),('radius',.00100001)]:
            D=data(); D[key][-1]=value
            with self.assertRaises(O.Tech): O.qualify_arrays([data(),D],binding())

    def test_phase_allocation_differs_without_new_threshold(self):
        D=data(); D['type']=np.array([1.,1.,3.])
        got=O.qualify_arrays([D],binding())
        self.assertEqual(got['planned_by_type'], {'1':1,'2':1,'3':1})
        self.assertEqual(got['observed_by_type'], {'1':2,'2':0,'3':1})

    def test_reference_geometry_seed_and_role(self):
        B=binding(role='U'); R=binding()
        O.qualify_reference(B,R)
        for key,value in [('role','N0'),('seed',99),('density_generation','gen1'),('revolutions',2)]:
            bad=copy.deepcopy(R);bad[key]=value
            with self.assertRaises(O.Tech): O.qualify_reference(B,bad)
        bad=copy.deepcopy(R);bad['geometry']['length']=.3
        with self.assertRaises(O.Tech): O.qualify_reference(B,bad)

    def test_hand_m_no_clipping_and_undefined(self):
        got=O.mixing_summary(stats(.25),stats(.05),[stats(.15),stats(.35)],[400,450])
        self.assertAlmostEqual(got['frames'][0]['M'], .5)
        self.assertAlmostEqual(got['frames'][1]['M'], -.5)
        self.assertAlmostEqual(got['M_mean'], 0.)
        self.assertEqual(got['S0'],.25);self.assertEqual(got['SR'],.05)
        for s0,sr,st in [(.05,.05,.01),(.01,.05,.01),(.2,.1,float('nan'))]:
            with self.assertRaises(O.Undefined): O.mixing_summary(stats(s0),stats(sr),[stats(st)],[400])

    def test_hand_contact_clusters_and_overlapping_am_fractions(self):
        # Two SE spheres touch both AM spheres; type-specific attachment fractions
        # are overlapping sets, not a partition of SE atoms.
        D=data(4);D['x']=np.array([0.,0.,.0005,.001])
        B=binding(4)
        O.qualify_arrays([D],B)
        q=O.contact.frame_quantities(D,B['frame_pm'])
        self.assertEqual(q['pairs']['SE-SE'],1)
        self.assertEqual(q['pairs']['AM_P-SE'],2)
        self.assertEqual(q['pairs']['AM_S-SE'],2)
        a=q['s2_am_se_attach']
        self.assertEqual(a['se_attached_any_frac'],1.)
        self.assertEqual(a['se_attached_frac_AM_P']+a['se_attached_frac_AM_S'],2.)


class DiskContract(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def make_run(self,name,role='E0',n=3):
        run=self.root/name;(run/'post').mkdir(parents=True)
        B=binding(n,role)
        # Explicit unit fixture: validate_case alone is mocked. Frozen-byte frame plan,
        # strict dump parser and observation functions are exercised.
        deck='timestep 0.01\nfix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 2\ndump dmp all custom 50 post/dump_*.liggghts id type x y z radius\nrun 1\nrun 100\nrun 100\nrun '+('0' if role=='E0' else '400')+'\n'
        (run/'in.mixer').write_text(deck)
        (run/'deck_meta.json').write_text(json.dumps(B))
        runs=[1,100,100,0 if role=='E0' else 400]
        (run/'log.liggghts').write_text(completion_log(runs,n))
        for step in ([200] if role=='E0' else [200,400,450,500,550]):
            self.dump(run,step,data(n))
        return run,B

    def dump(self,run,step,D):
        text='ITEM: TIMESTEP\n%d\nITEM: NUMBER OF ATOMS\n%d\nITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\nITEM: ATOMS id type x y z radius\n' % (step,len(D['id']))
        text+=''.join(' '.join('%.17g'%D[k][i] for k in ('id','type','x','y','z','radius'))+'\n' for i in range(len(D['id'])))
        (run/'post'/('dump_%d.liggghts'%step)).write_text(text)

    def invoke(self,run,B,ref=None):
        with mock.patch.object(O,'validate_case',side_effect=lambda case,deck,meta:meta):
            return O.analyse_run(B['case_id'],run,ref)

    def test_e0_real_small_dump_and_no_bin(self):
        run,B=self.make_run('e0')
        before={str(p.relative_to(run)):p.read_bytes() for p in run.rglob('*') if p.is_file()}
        result=self.invoke(run,B)
        after={str(p.relative_to(run)):p.read_bytes() for p in run.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
        self.assertEqual(result['status'],'OK',result)
        self.assertFalse(result['execution_authorized'])
        self.assertEqual(result['contact']['bin']['status'],'NOT_APPLICABLE')

    def test_rotating_wiring_with_explicit_cell_stats_unit_mock(self):
        run,B=self.make_run('u','U');ref,_=self.make_run('e0')
        # Tiny dumps cannot populate n_min=20 grids. Only cell_stats is mocked;
        # this asserts orchestration, not scientific/full-size grid validation.
        one=[stats(.25)]+[stats(.15) for _ in range(4)]+[stats(.05)]
        with mock.patch.object(O.mixing,'cell_stats',side_effect=one*3) as cell:
            got=self.invoke(run,B,ref)
        self.assertEqual(got['status'],'OK',got)
        self.assertEqual(cell.call_count,18)
        for grid in got['mixing']['grids']:
            self.assertAlmostEqual(grid['M_mean'],.5)
            self.assertEqual(grid['n_min'],20)
            self.assertEqual(grid['axis'],'x')
        self.assertIn('믹서 판독 전용',got['contact']['observable_label'])
        self.assertEqual(len(got['provenance']['module_sha256']),9)

    def test_missing_dependency_source_is_tech(self):
        run,B=self.make_run('e0')
        with mock.patch.dict(O._BOUND_PATHS, {'measure_mixing_index':str(self.root/'missing.py')}):
            got=self.invoke(run,B)
        self.assertEqual(got['status'],'TECH')
        self.assertIsNone(got['contact'])

    def test_late_failure_never_computes_partial_metrics(self):
        run,B=self.make_run('u','U');ref,_=self.make_run('e0')
        D=data();D['id'][-1]=4;self.dump(run,550,D)
        with mock.patch.object(O.contact,'frame_quantities') as metric:
            result=self.invoke(run,B,ref)
        self.assertEqual(result['status'],'TECH');metric.assert_not_called()
        self.assertIsNone(result['contact']);self.assertIsNone(result['mixing'])

    def test_missing_duplicate_malformed_frame(self):
        for how in ('missing','duplicate','malformed'):
            run,B=self.make_run(how,'U');ref,_=self.make_run(how+'e0')
            path=run/'post'/'dump_450.liggghts'
            if how=='missing':path.unlink()
            elif how=='duplicate':(run/'post'/'copy_450.liggghts').write_bytes(path.read_bytes())
            else:path.write_text('bad header\n')
            result=self.invoke(run,B,ref)
            self.assertEqual(result['status'],'TECH',result)
            self.assertIsNone(result['contact'])

    def test_bad_meta_and_changed_deck(self):
        run,B=self.make_run('e0')
        (run/'deck_meta.json').write_text('{"x":1,"x":2}')
        result=self.invoke(run,B);self.assertEqual(result['status'],'TECH')
        (run/'deck_meta.json').write_text(json.dumps(B))
        original=O.contact.frame_quantities
        def change(*args):
            (run/'in.mixer').write_text('changed')
            return original(*args)
        with mock.patch.object(O.contact,'frame_quantities',side_effect=change):
            result=self.invoke(run,B)
        self.assertEqual(result['status'],'TECH');self.assertIsNone(result['contact'])

    def test_reference_wrong_id_and_runtime_bad_binding(self):
        run,B=self.make_run('u','U');ref,R=self.make_run('e0')
        R['case_id']='PRECAL_N0'
        (ref/'deck_meta.json').write_text(json.dumps(R))
        with mock.patch.object(O.contact,'frame_quantities') as metric:
            got=self.invoke(run,B,ref)
        self.assertEqual(got['status'],'TECH');metric.assert_not_called()
        R['case_id']='PRECAL_E0';R['frame_pm']['seed']=1
        (ref/'deck_meta.json').write_text(json.dumps(R))
        self.assertEqual(self.invoke(run,B,ref)['status'],'TECH')

    def test_changed_metadata_and_frame_discard_metrics(self):
        for name in ('deck_meta.json','post/dump_200.liggghts'):
            run,B=self.make_run(name.replace('/','_'))
            original=O.contact.frame_quantities
            def change(*args):
                path=run/name
                path.write_bytes(path.read_bytes()+b' ')
                return original(*args)
            with mock.patch.object(O.contact,'frame_quantities',side_effect=change):
                got=self.invoke(run,B)
            self.assertEqual(got['status'],'TECH')
            self.assertIsNone(got['contact']);self.assertIsNone(got['mixing'])

    def test_raw_aba_cannot_change_metrics(self):
        run,B=self.make_run('e0')
        path=run/'post'/'dump_200.liggghts';raw=path.read_bytes()
        original=O.bed.read_dump
        def swapped(p):
            D=data();D['x'][:]=0
            self.dump(run,200,D)
            try:return original(p)
            finally:path.write_bytes(raw)
        with mock.patch.object(O,'read_dump',side_effect=swapped,create=True):
            got=self.invoke(run,B)
        self.assertEqual(got['status'],'OK',got)
        self.assertEqual(got['contact']['t0']['pairs']['AM_P-SE'],0)

    def test_interrupted_missing_short_or_extra_log_is_tech(self):
        for kind in ('error','missing','short','extra','resume','concatenated','error_then_normal'):
            run,B=self.make_run(kind)
            path=run/'log.liggghts'
            if kind=='error':path.write_text(path.read_text()+'ERROR: synthetic interruption\n')
            elif kind=='missing':path.unlink()
            elif kind=='short':path.write_text(path.read_text().replace('201 3','200 3'))
            elif kind=='resume':path.write_text('RESUME_STEP 100\n'+path.read_text())
            elif kind=='concatenated':path.write_text(path.read_text()*2)
            elif kind=='error_then_normal':path.write_text('ERROR: interrupted\n'+path.read_text())
            else:path.write_text(path.read_text()+'Loop time of 1 on 20 procs for 0 steps with 3 atoms\n')
            got=self.invoke(run,B)
            self.assertEqual(got['status'],'TECH',got)
            self.assertIsNone(got['contact'])

    def test_frozen_parser_raw_survives_path_aba(self):
        run,B=self.make_run('e0')
        path=run/'post'/'dump_200.liggghts';raw=path.read_bytes()
        original=O._parse_dump
        def swapped(raw_arg,step):
            D=data();D['x'][:]=0;self.dump(run,200,D)
            try:return original(raw_arg,step)
            finally:path.write_bytes(raw)
        with mock.patch.object(O,'_parse_dump',side_effect=swapped):
            got=self.invoke(run,B)
        self.assertEqual(got['status'],'OK',got)
        self.assertEqual(got['contact']['t0']['pairs']['AM_P-SE'],0)

    def test_log_header_and_each_run_endpoint(self):
        runs=[1,100,100,0]
        good=completion_log(runs)
        cases=[good.replace('Step Atoms KinEng c_rke Volume\n',''),
               good.replace('201 3 0 0 1','200 3 0 0 1')+'201 3 0 0 1\n',
               good.replace('101 3 0 0 1','100 3 0 0 1'),
               good.replace('201 3 0 0 1','201 3 nan 0 1'),
               good.replace('201 3 0 0 1','201 3 0 0')]
        for bad in cases:
            with self.subTest(log=bad):
                with self.assertRaises(O.Tech):O._log_contract(bad.encode(),runs)
        self.assertEqual(O._log_contract(good.encode(),runs)['last_thermo_step'],201)

    def test_frozen_dump_strict_headers_and_shape(self):
        run,B=self.make_run('e0');path=run/'post'/'dump_200.liggghts'
        raw=path.read_bytes()
        for bad in (raw.replace(b'BOX BOUNDS',b'BROKEN'),
                    raw.replace(b'200',b'201',1),
                    raw.replace(b'id type',b'id id'),
                    raw+b'1 2 3\n',raw.replace(b'-1 1',b'1 -1')):
            with self.assertRaises(O.Tech):O._parse_dump(bad,200)

    def test_optional_n_expected_creation_is_tech(self):
        for where in ('run','reference'):
            for when in ('after_load','metrics'):
                for kind in ('regular','dangling_symlink'):
                    with self.subTest(where=where,when=when,kind=kind):
                        tag=where+when+kind
                        run,B=self.make_run(tag+'u','U');ref,_=self.make_run(tag+'e0')
                        target=run if where=='run' else ref
                        def create():
                            path=target/'n_expected'
                            if kind=='regular':path.write_text('3')
                            else:path.symlink_to(target/'does_not_exist')
                        original=O._load
                        def load(*args,**kw):
                            result=original(*args,**kw)
                            if Path(args[1])==target:create()
                            return result
                        def metric(*args):
                            if when=='metrics':create()
                            return {},{}
                        with mock.patch.object(O,'_metrics',side_effect=metric):
                            if when=='after_load':
                                with mock.patch.object(O,'_load',side_effect=load):got=self.invoke(run,B,ref)
                            else:got=self.invoke(run,B,ref)
                        self.assertEqual(got['status'],'TECH',got)
                        self.assertIsNone(got['contact']);self.assertIsNone(got['mixing'])

    def test_optional_n_expected_initial_presence_contract(self):
        for kind in ('absent','valid','wrong','dangling_symlink'):
            run,B=self.make_run('optional_'+kind)
            path=run/'n_expected'
            if kind=='valid':path.write_text('3')
            elif kind=='wrong':path.write_text('4')
            elif kind=='dangling_symlink':path.symlink_to(run/'missing')
            got=self.invoke(run,B)
            self.assertEqual(got['status'],'OK' if kind in ('absent','valid') else 'TECH')

    def test_no_se_is_undefined_not_zero(self):
        run,B=self.make_run('e0',n=2)
        result=self.invoke(run,B)
        self.assertEqual(result['status'],'UNDEFINED',result)
        self.assertIsNone(result['contact'])


class ActualLiggghtsLogForm(unittest.TestCase):
    """Registration draft Q5: a normal completed run written in the sealed build's actual log
    form (header without c_, Loop finish stamp, insertion report inside the first table,
    echoed deck comment quoting ERROR) must qualify; the observer must not call it TECH."""
    RUNS = [1, 100, 100, 0]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_dir(self, name, deck, log, B=None, step=200):
        run = self.root/name; (run/'post').mkdir(parents=True)
        B = B or binding(3)
        (run/'in.mixer').write_bytes(deck if isinstance(deck, bytes) else deck.encode())
        (run/'deck_meta.json').write_text(json.dumps(B))
        (run/'log.liggghts').write_text(log)
        write_dump(run/'post'/('mix_%d.liggghts' % step), step, data(3))
        return run, B

    def invoke(self, run, B):
        with mock.patch.object(O, 'validate_case', side_effect=lambda case, deck, meta: meta):
            return O.analyse_run(B['case_id'], run, None)

    def assert_ok(self, deck, inserted, name):
        run, B = self.run_dir(name, deck, actual_log(deck, inserted))
        got = self.invoke(run, B)
        self.assertEqual(got['status'], 'OK', got['reasons'])
        self.assertEqual(got['provenance']['completion_log']['loop_steps'], self.RUNS)
        self.assertEqual(got['provenance']['completion_log']['last_thermo_step'], 201)
        return got

    def test_actual_header_and_loop_forms_direct(self):
        # Forms 1+2 only (no insert fix, no ERROR comment in the deck): header without c_ and
        # the Loop finish stamp are present in every log of this build.
        try:
            got = O._log_contract(actual_log(SMALL_DECK, {}).encode(), self.RUNS)
        except O.Tech as exc:
            self.fail('normal actual-form log rejected: %s' % exc)
        self.assertEqual(got['loop_steps'], self.RUNS)
        self.assertEqual(got['last_thermo_step'], 201)

    def test_actual_header_and_loop_forms(self):
        self.assert_ok(SMALL_DECK, {}, 'forms12')

    def test_actual_insertion_report_inside_first_table(self):
        self.assert_ok(INSERT_FIX+SMALL_DECK, {'ins': 3}, 'forms123')

    def test_actual_deck_comment_echo_quoting_error(self):
        self.assert_ok(ERROR_COMMENT+'\n'+SMALL_DECK, {}, 'forms124')

    def test_actual_all_four_forms(self):
        self.assert_ok(ERROR_COMMENT+'\n'+INSERT_FIX+SMALL_DECK, {'ins': 3}, 'forms1234')

    def test_planned_precal_e0_deck_and_full_length_log(self):
        # The exact planned PRECAL_E0 deck bytes (static asset sha256) and a full-length log:
        # run 1 / 560606 / 560606 / 0, thermo every 5000, NP20.  Atom count is kept equal to
        # the tiny t0 dump; the log contract does not compare it with the planned 100000.
        deck = HERE.parent.joinpath(*E0_DECK).read_bytes()
        self.assertEqual(hashlib.sha256(deck).hexdigest(), E0_DECK_SHA256)
        B = binding(3)
        B['frame_pm']['meta_steps'] = dict(t0_planned=1121000, dump_every=1000)
        run, B = self.run_dir('e0_planned', deck, actual_log(deck.decode('utf-8'), {'ins': 3}), B, 1121000)
        got = self.invoke(run, B)
        self.assertEqual(got['status'], 'OK', got['reasons'])
        log = got['provenance']['completion_log']
        self.assertEqual(log['loop_steps'], [1, 560606, 560606, 0])
        self.assertEqual(log['last_thermo_step'], 1121213)
        self.assertEqual(got['provenance']['frames'][0]['step'], 1121000)


if __name__=='__main__':unittest.main(verbosity=2)
