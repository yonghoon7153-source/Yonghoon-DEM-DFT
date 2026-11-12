"""Small synthetic observation contracts; no simulator or research data."""
import copy
import hashlib
import importlib.util
import json
import re
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
    # Header and Loop lines in the sealed build's form (see ACTUAL_HEADER below); the old
    # `c_rke` header and stamp-less Loop line were never produced by that build.
    total=0;lines=[]
    for r in runs:
        total+=r
        lines.extend([ACTUAL_HEADER,
                      '%d %d 0 0 1'%(total,n),
                      'Loop time of 1 on 20 procs for %d steps with %d atoms%s'%(r,n,ACTUAL_FINISH)])
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
        cases=[good.replace(ACTUAL_HEADER+'\n',''),
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

    def test_planned_layered_deck_log_form_direct(self):
        # Log contract only (not the rotating observation path): the planned N0 deck inserts
        # twice (insA in run 1, insB in run 3), so its log carries two reports in two tables.
        deck = HERE.parent.joinpath(*E0_DECK[:-2], 'PRECAL_N0', 'in.mixer').read_bytes()
        self.assertEqual(hashlib.sha256(deck).hexdigest(),
                         'adbbc8fa8f46730779fbf4f028f95a7aaf90c27ef2697c0dbe21a9ae1b5c6de3')
        facts = O._deck_log_facts(deck)
        self.assertEqual(facts['insert_fix_run'], {'insA': 0, 'insB': 2})
        raw = actual_log(deck.decode('utf-8'), {'insA': 842, 'insB': 99158}).encode()
        got = O._log_contract(raw, [1, 560606, 560606, 6595382], facts)
        self.assertEqual(got['insertion_reports'], [dict(fix='insA', step=1, inserted=842),
                                                    dict(fix='insB', step=560608, inserted=99158)])
        self.assertEqual(got['last_thermo_step'], 7716595)


class ActualLogRejections(unittest.TestCase):
    """Q5 rejection side: admitting the four actual forms must not admit a true defect.
    Each case is the full-length actual-form PRECAL_E0 log with one defect injected."""
    RUNS = [1, 560606, 560606, 0]

    @classmethod
    def setUpClass(cls):
        cls.deck = HERE.parent.joinpath(*E0_DECK).read_bytes()
        assert hashlib.sha256(cls.deck).hexdigest() == E0_DECK_SHA256
        cls.facts = O._deck_log_facts(cls.deck)
        cls.base = actual_log(cls.deck.decode('utf-8'), {'ins': 100000})
        L = cls.base.split('\n')
        cls.hdr = [i for i, l in enumerate(L) if l == ACTUAL_HEADER]
        cls.loop = [i for i, l in enumerate(L) if l.startswith('Loop time of')]
        cls.info = [i for i, l in enumerate(L) if ': inserted ' in l]
        cls.err = L.index(ERROR_COMMENT)

    def edit(self, change):
        L = self.base.split('\n')
        change(L)
        return '\n'.join(L)

    def rejects(self, text, reason, facts='deck'):
        raw = text if isinstance(text, bytes) else text.encode('utf-8')
        with self.assertRaises(O.Tech) as ctx:
            O._log_contract(raw, self.RUNS, self.facts if facts == 'deck' else facts)
        self.assertIn(reason, str(ctx.exception))

    def test_base_is_a_normal_actual_log(self):
        self.assertEqual((len(self.hdr), len(self.loop), len(self.info)), (4, 4, 1))
        self.assertEqual(self.facts['insert_fix_run'], {'ins': 0})
        self.assertEqual(self.facts['comment_lines'][ERROR_COMMENT], 1)
        got = O._log_contract(self.base.encode('utf-8'), self.RUNS, self.facts)
        self.assertEqual(got['loop_steps'], self.RUNS)
        self.assertEqual(got['insertion_reports'], [dict(fix='ins', step=1, inserted=100000)])
        self.assertEqual(got['deck_comment_echo_error_lines'], 1)
        self.assertEqual(got['loop_procs'], [20]*4)

    def test_true_error_lines_stay_tech(self):
        row1 = self.hdr[1]+3
        cases = {
            'error_in_table': lambda L: L.insert(row1, 'ERROR: Lost atoms: original 100000 current 99999 (../thermo.cpp:395)'),
            'error_on_proc': lambda L: L.insert(self.loop[1]+1, 'ERROR on proc 7: Cannot open dump file (../dump.cpp:478)'),
            'error_at_end': lambda L: L.append('ERROR: Particle insertion: Internal error (../fix_insert.cpp:719)'),
            'word_mid_line': lambda L: L.insert(self.loop[0]+2, 'WARNING: ERROR handling switched off (../input.cpp:1)'),
            'line_start_prefix': lambda L: L.insert(self.loop[2]+2, 'ERRORS: synthetic'),
            'altered_comment': lambda L: L.insert(self.err+1, ERROR_COMMENT.replace('youngsModulus', 'poissonsRatio')),
            'comment_echoed_twice': lambda L: L.insert(self.err+1, ERROR_COMMENT),
            'comment_reindented': lambda L: L.__setitem__(self.err, '  '+ERROR_COMMENT),
        }
        for name, change in cases.items():
            with self.subTest(name):
                self.rejects(self.edit(change), 'error/resume log is not fresh completion evidence')
        with self.subTest('no_deck_facts'):
            self.rejects(self.base, 'error/resume log is not fresh completion evidence', facts=None)

    def test_truncated_logs_stay_tech(self):
        L = self.base.split('\n')
        last_loop = L[self.loop[3]]
        cases = [('inside_run2', '\n'.join(L[:self.hdr[1]+10])+'\n', 'log fresh four-run completion mismatch'),
                 ('before_run0', '\n'.join(L[:self.loop[2]+1])+'\n', 'log fresh four-run completion mismatch'),
                 ('loop_stamp_cut', '\n'.join(L[:self.loop[3]]+[last_loop[:last_loop.index(',')]]), 'malformed Loop line'),
                 ('loop_mid_stamp', '\n'.join(L[:self.loop[3]]+[last_loop[:-9]]), 'malformed Loop line'),
                 ('row_cut', '\n'.join(L[:self.hdr[3]+1]+[L[self.hdr[3]+1][:12]]), 'invalid five-column thermo row'),
                 ('empty', '', 'log fresh four-run completion mismatch')]
        for name, text, reason in cases:
            with self.subTest(name):
                self.rejects(text, reason)
        with self.subTest('utf8_cut'):
            # Cut inside a multi-byte character of an echoed Korean comment (deck L4).
            raw = self.base.encode('utf-8')
            with self.assertRaises(UnicodeDecodeError):
                O._log_contract(raw[:raw.index('조성'.encode())+1], self.RUNS, self.facts)

    def test_corrupted_rows_stay_tech(self):
        r = self.hdr[1]+3
        def value(old, new):
            return lambda L: L.__setitem__(r, L[r].replace(old, new, 1))
        good = actual_row(15000, 100000)
        cases = [('nan', value('3.2685651e-12', 'nan'), 'nonfinite thermo row'),
                 ('-nan', value('3.2685651e-12', '-nan'), 'nonfinite thermo row'),
                 ('inf', value('1.0960987e-10', 'inf'), 'nonfinite thermo row'),
                 ('overflow', value('2.7589053e-05', '1e999'), 'nonfinite thermo row'),
                 ('unicode_digit', value('3.2685651e-12', '٣.2685651e-12'), 'non-ASCII line inside thermo table'),
                 ('nbsp', lambda L: L.__setitem__(r, L[r].replace(' ', ' ')), 'non-ASCII line inside thermo table'),
                 ('unicode_blank_line', lambda L: L.insert(r, '　'), 'non-ASCII line inside thermo table'),
                 ('unit_separator', lambda L: L.__setitem__(r, good.strip().replace(' ', '\x1f', 1)), 'invalid five-column thermo row'),
                 ('four_columns', lambda L: L.__setitem__(r, ' '.join(good.split()[:4])), 'invalid five-column thermo row'),
                 ('six_columns', lambda L: L.__setitem__(r, good+' 1'), 'invalid five-column thermo row'),
                 ('float_step', lambda L: L.__setitem__(r, good.replace('15000', '15000.0', 1)), 'invalid five-column thermo row'),
                 ('negative_atoms', lambda L: L.__setitem__(r, good.replace(' 100000', '-100000', 1)), 'invalid five-column thermo row'),
                 ('text_value', value('3.2685651e-12', 'abc'), 'invalid five-column thermo row'),
                 ('underscore_value', value('2.7589053e-05', '1_000'), 'invalid five-column thermo row'),
                 ('unknown_warning', lambda L: L.insert(r, 'WARNING: synthetic (../fix.cpp:1)'), 'invalid five-column thermo row')]
        for name, change, reason in cases:
            with self.subTest(name):
                self.rejects(self.edit(change), reason)

    def test_lost_particles_stay_tech(self):
        def atoms(i, count):
            return lambda L: L.__setitem__(i, L[i].replace('100000', str(count), 1))
        cases = [('run2_row', atoms(self.hdr[1]+5, 99999), 'thermo atom count decreased'),
                 ('run3_setup_row', atoms(self.hdr[2]+1, 99999), 'thermo atom count decreased'),
                 ('run0_row', atoms(self.hdr[3]+1, 99999), 'thermo atom count decreased'),
                 ('step1_after_report', atoms(self.info[0]+2, 99999), 'differs from the report')]
        for name, change, reason in cases:
            with self.subTest(name):
                self.rejects(self.edit(change), reason)

    def test_insertion_report_contract(self):
        i = self.info[0]
        report = self.base.split('\n')[i:i+2]
        def setline(k, old, new):
            return lambda L: L.__setitem__(k, L[k].replace(old, new, 1))
        def move_to_run2(L):
            del L[i:i+2]
            k = L.index(ACTUAL_HEADER, i)+2
            L[k:k] = [report[0].replace('at step 1', 'at step 2'), report[1]]
        cases = [('total_count', setline(i+1, 'a total of 100000', 'a total of 99999'), 'inconsistent insertion report'),
                 ('total_mass', setline(i+1, '1.000000e+01', '1.000001e+01'), 'inconsistent insertion report'),
                 ('total_period', setline(i+1, 'so far.', 'so far'), 'inconsistent insertion report'),
                 ('total_missing', lambda L: L.__delitem__(i+1), 'inconsistent insertion report'),
                 ('wrong_step', setline(i, 'at step 1', 'at step 2'), 'not at the first step of its run'),
                 ('zero_inserted', lambda L: (L.__setitem__(i, L[i].replace('inserted 100000', 'inserted 0')),
                                             L.__setitem__(i+1, L[i+1].replace('a total of 100000', 'a total of 0'))),
                  'invalid insertion report values'),
                 ('nan_mass', lambda L: (L.__setitem__(i, L[i].replace('1.000000e+01', 'nan')),
                                        L.__setitem__(i+1, L[i+1].replace('1.000000e+01', 'nan'))),
                  'invalid insertion report values'),
                 ('repeated', lambda L: L.__setitem__(slice(i+2, i+2), report), 'undeclared, repeated or misplaced'),
                 ('undeclared_fix', setline(i, 'insertion ins:', 'insertion insB:'), 'undeclared, repeated or misplaced'),
                 ('moved_to_run2', move_to_run2, 'undeclared, repeated or misplaced'),
                 ('before_setup_row', lambda L: L.__setitem__(slice(i-1, i+2), report+[L[i-1]]), 'not at the first step of its run'),
                 ('after_two_rows', lambda L: L.__setitem__(slice(i, i+3), [L[i+2]]+report), 'not at the first step of its run'),
                 ('less_insertions_warning', lambda L: L.insert(i+2, 'WARNING: Particle insertion: Less insertions than requested (../fix_insert.cpp:814)'),
                  'invalid five-column thermo row'),
                 ('start_info_inside_table', lambda L: L.insert(i+2, 'INFO: Particle insertion ins: inserting every 0 steps'),
                  'invalid five-column thermo row'),
                 ('report_then_loop', lambda L: L.__delitem__(i+2), 'insertion report without its thermo row'),
                 ('report_missing', lambda L: L.__delitem__(slice(i, i+2)), 'declared insert/pack fix without its insertion report'),
                 ('report_outside_table', lambda L: (L.__delitem__(slice(i, i+2)), L.__setitem__(slice(i-3, i-3), report)),
                  'declared insert/pack fix without its insertion report')]
        for name, change, reason in cases:
            with self.subTest(name):
                self.rejects(self.edit(change), reason)

    def test_table_structure_stays_tech(self):
        legacy_loop = re.compile(r', finish time .*$', re.M)
        fifth = [ACTUAL_HEADER, actual_row(1121213, 100000),
                 'Loop time of 1.25 on 20 procs for 0 steps with 100000 atoms'+ACTUAL_FINISH]
        cases = [('header_inside_table', lambda L: L.insert(self.hdr[1]+4, ACTUAL_HEADER), 'thermo header inside an unfinished table'),
                 ('fifth_run', lambda L: L.__setitem__(slice(len(L)-1, len(L)-1), fifth), 'cumulative run endpoint mismatch'),
                 ('loop_steps', lambda L: L.__setitem__(self.loop[1], L[self.loop[1]].replace('for 560606', 'for 560605')),
                  'cumulative run endpoint mismatch'),
                 ('loop_atoms', lambda L: L.__setitem__(self.loop[1], L[self.loop[1]].replace('100000 atoms', '99999 atoms')),
                  'Loop atom count differs'),
                 ('fullwidth_procs', lambda L: L.__setitem__(self.loop[0], L[self.loop[0]].replace('20 procs', '２０ procs')),
                  'malformed Loop line'),
                 ('prefixed_loop', lambda L: L.__setitem__(self.loop[2], 'X'+L[self.loop[2]]), 'invalid five-column thermo row'),
                 ('legacy_header', lambda L: [L.__setitem__(k, 'Step Atoms KinEng c_rke Volume') for k in self.hdr],
                  'Loop lacks a qualified thermo table'),
                 ('resume_marker', lambda L: L.insert(1, 'RESUME_STEP 560607'), 'error/resume log is not fresh completion evidence'),
                 ('read_restart_echo', lambda L: L.insert(self.err+1, 'read_restart restart/a.bin'), 'error/resume log is not fresh completion evidence')]
        for name, change, reason in cases:
            with self.subTest(name):
                self.rejects(self.edit(change), reason)
        with self.subTest('legacy_loop'):
            self.rejects(legacy_loop.sub('', self.base), 'malformed Loop line')
        with self.subTest('concatenated'):
            self.rejects(self.base*2, 'error/resume log is not fresh completion evidence')

    def test_end_to_end_defects_are_tech_without_metrics(self):
        runner = ActualLiggghtsLogForm('test_actual_header_and_loop_forms')
        runner.setUp(); self.addCleanup(runner.doCleanups)
        B = binding(3); B['frame_pm']['meta_steps'] = dict(t0_planned=1121000, dump_every=1000)
        small = actual_log(self.deck.decode('utf-8'), {'ins': 3})
        L = small.split('\n'); r = L.index(ACTUAL_HEADER, L.index(ACTUAL_HEADER)+1)+3
        cases = {'ok': small.encode(),
                 'error': (small+'ERROR: Lost atoms: original 3 current 2 (../thermo.cpp:395)\n').encode(),
                 'truncated': '\n'.join(L[:r]).encode(),
                 'lost': '\n'.join(L[:r]+[L[r].replace('       3 ', '       2 ', 1)]+L[r+1:]).encode(),
                 'utf8_cut': small.encode()[:small.encode().index('조성'.encode())+1]}
        for name, raw in cases.items():
            with self.subTest(name):
                run, B2 = runner.run_dir('e2e_'+name, self.deck, '', copy.deepcopy(B), 1121000)
                (run/'log.liggghts').write_bytes(raw)
                got = runner.invoke(run, B2)
                self.assertEqual(got['status'], 'OK' if name == 'ok' else 'TECH', got['reasons'])
                if name != 'ok':
                    self.assertIsNone(got['contact']); self.assertIsNone(got['mixing']); self.assertIsNone(got['counts'])


if __name__=='__main__':unittest.main(verbosity=2)
