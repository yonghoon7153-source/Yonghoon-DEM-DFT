#!/usr/bin/env python3
"""D2 development consumer regressions; synthetic decks only, no simulator.

MXD2R-01 · 02 · 03 (Codex 10-27 재검토 HOLD · 수정 계획 docs/reviews/mxd2r_fix_plan_20261030.md · 1저자 11-02 Q1–Q3 (가)):
반례를 고치기 **전에** 옮겼다 — 고치기 전 소비자는 아래 공통 변조 · CRLF 바이트를 세 소비자 모두 PASS / rc 0 으로 받았다.
"""
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_mixer_deck as gen
import mixer_deck_readback as rb
import mixer_deck_diff as dd
import mixer_smoke_blind as smoke


def fixture(phases=('AM_P', 'AM_S', 'SE'), generation='lab20261014', stiff=20., rho=.3,
            coated=False, bo=.73, n=100000, cgf=151.4, layered=True, seed=32452843, dt_factor=1.):
    old = gen.TYPES
    try:
        gen.set_phases(phases)
        gamma = {p: 1. if coated or p == 'SE' else rho for p in phases}
        arm = gen.gm_arm(gamma, gamma_wall=gen.gm_wall_from_ncm(rho), bo_se=bo,
                         rho_uncoated_ncm=rho)
        arm['layered'] = layered
        gen.ARMS['D2CONSUMER'] = arm
        p = gen.plan(n, cgf=cgf, stiffen_se=stiff, dens_gen=generation)
        rpm = gen.resolve_rpm(p['R'])
        text = gen.deck(p, rpm, 2, seed=seed, arm='D2CONSUMER', hold_bo_pairwise=True, dt_factor=dt_factor)
        meta = gen.deck_meta(p, rpm, 2, seed, 'D2CONSUMER', text, hold_bo_pairwise=True, dt_factor=dt_factor)
        return text, meta, {str(i+1): int(p['n'][phase]) for i, phase in enumerate(phases)}
    finally:
        gen.ARMS.pop('D2CONSUMER', None)
        gen.set_phases(old)


def rebound(text, meta):
    meta = copy.deepcopy(meta)
    meta['deck_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    meta['deck_bytes'] = len(text.encode())
    return meta


def rebound_bytes(raw, meta):
    """Metadata that states the given physical file bytes (MXD2R-03 'CRLF metadata' direction)."""
    meta = copy.deepcopy(meta)
    meta['deck_sha256'] = hashlib.sha256(raw).hexdigest()
    meta['deck_bytes'] = len(raw)
    return meta


def _block(fix_id, rows):
    """Remove `fix <id> …` and its `rows` continuation lines (Codex friction_missing form)."""
    return lambda s: re.sub(r'(?m)^fix ' + fix_id + r' [^\n]*\n(?:    [^\n]*\n){' + str(rows) + '}', '', s)


def _move_after(pattern, anchor):
    """Move the lines matched by `pattern` (multi-line allowed) to just after the line `anchor`."""
    def transform(s):
        m = re.search(pattern, s, flags=re.M)
        assert m, pattern
        s = s[:m.start()] + s[m.end():]
        a = re.search(r'(?m)^' + re.escape(anchor) + r'\n', s)
        assert a, anchor
        return s[:a.end()] + m.group(0) + s[a.end():]
    return transform


def _friction_values(new):
    def transform(s):
        m = re.search(r'(?m)^fix m4 [^\n]*\n(?:    [^\n]*\n){4}', s)
        return s[:m.start()] + m.group(0).replace('0.9', new) + s[m.end():]
    return transform


#: Codex d2/evidence/independent_probe.py 의 공통 변조 여섯 — 식 그대로 · 두 덱에 같이 · 메타 해시 · 길이 재결합.
#: 값 = (변조, 고친 뒤 거부 사유에 있어야 할 문구 — 다른 사유로 우연히 거부된 것이 아님을 확인한다)
CODEX_COMMON_MODE = {
    'run_upto': (lambda s: re.sub(r'(?m)^run (\d+)$', r'run \1 upto', s), 'run <integer>'),
    'late_timestep': (lambda s: re.sub(r'(?m)^timestep[^\n]*\n', '', s)
                      + re.search(r'(?m)^timestep[^\n]*', s).group(0) + '\n', 'timestep <dt>'),
    'insert_start_late': (lambda s: s.replace('insert_every once', 'insert_every once start 9000000'),
                          'insert/pack must be the generator form'),
    'front_period': (lambda s: re.sub(r'(fix mvF[^\n]* period )[^\s]+', r'\g<1>0.1', s), 'Drum period'),
    'exclude_SE_SE': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    delay 0\nneigh_modify exclude type 3 3'),
                      '`neigh_modify delay 0`'),
    'friction_missing': (lambda s: re.sub(r'(?m)^fix m4[^\n]*\n(?:    [^\n]*\n){4}', '', s), 'coefficientFriction'),
}

#: 같은 부류 (생성기 문법 밖 · 고치기 전 세 소비자 PASS) — Codex 여섯 밖의 변형으로 문법이 닫혔는지 본다 (API).
MXD2R01_SAME_CLASS = {
    'run_pre_post': (lambda s: re.sub(r'(?m)^run (\d+)$', r'run \1 pre no post no', s), 'run <integer>'),
    'run_start_stop': (lambda s: re.sub(r'(?m)^run (\d+)$', r'run \1 start 0 stop 99999999', s), 'run <integer>'),
    'timestep_after_insert_run': (_move_after(r'^timestep[^\n]*\n', 'run 1'), 'timestep <dt>'),
    'timestep_extra_token': (lambda s: re.sub(r'(?m)^(timestep\s+\S+)$', r'\1 2.373e-07', s), 'timestep <dt>'),
    'insert_repeat_every': (lambda s: s.replace('insert_every once', 'insert_every 1000'), 'insert/pack must be the generator form'),
    'insert_start_first_step': (lambda s: s.replace('insert_every once', 'insert_every once start 1'),
                                'insert/pack must be the generator form'),
    'insert_velocity': (lambda s: s.replace('vel constant 0. 0. -0.2', 'vel constant 0. 0. -2.0'),
                        'insert/pack must be the generator form'),
    'back_period': (lambda s: re.sub(r'(fix mvB[^\n]* period )[^\s]+', r'\g<1>0.1', s), 'Drum period'),
}
MXD2R02_SAME_CLASS = {
    'exclude_AM_SE': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    delay 0\nneigh_modify exclude type 1 3'),
                      '`neigh_modify delay 0`'),
    'exclude_same_line': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    delay 0 exclude type 3 3'),
                          '`neigh_modify delay 0`'),
    'neigh_every_check_no': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    every 10 delay 0 check no'),
                             '`neigh_modify delay 0`'),
    'neigh_missing': (lambda s: s.replace('neigh_modify    delay 0\n', ''), '`neigh_modify delay 0`'),
    'restitution_missing': (_block('m3', 4), 'coefficientRestitution'),
    'rolling_missing': (_block('m5', 4), 'coefficientRollingFriction'),
    'charvel_missing': (lambda s: re.sub(r'(?m)^fix m9 [^\n]*\n', '', s), 'characteristicVelocity'),
    'friction_duplicate': (lambda s: s.replace('fix m5 all', 'fix m4b all property/global coefficientFriction peratomtypepair 4 &\n'
                                               + '    0.1 0.1 0.1 0.1 &\n' * 3 + '    0.1 0.1 0.1 0.1\nfix m5 all', 1), 'coefficientFriction'),
    # 사전 공격 변이 M11 생존 (11-03) — 값이 다른 중복은 상수 검사가 먼저 잡아 '중복' 규칙이 시험에 묶이지 않았다 → 같은 값 중복으로 묶는다
    'friction_duplicate_same_values': (lambda s: s.replace('fix m5 all', 'fix m4b all property/global coefficientFriction peratomtypepair 4 &\n'
                                                           + '    0.9 0.9 0.9 0.9 &\n' * 3 + '    0.9 0.9 0.9 0.9\nfix m5 all', 1),
                                       'defined more than once'),
    'friction_value': (_friction_values('0.1'), 'coefficientFriction'),
    'friction_after_pair_style': (_move_after(r'^fix m4 [^\n]*\n(?:    [^\n]*\n){4}', 'pair_coeff      * *'), 'coefficientFriction'),
    'unknown_property': (lambda s: s.replace('fix m9 all', 'fix mX all property/global coefficientRestitutionWall scalar 0.5\nfix m9 all', 1),
                         'unsupported material property'),
    'pair_style_late': (_move_after(r'^pair_style[^\n]*\npair_coeff[^\n]*\n', 'write_restart restart/settled.bin'), 'pair_coeff * *'),
    'pair_coeff_partial': (lambda s: s.replace('pair_coeff      * *', 'pair_coeff      1 1'), 'pair_coeff * *'),
}


def _write_case(folder, old, new, old_meta, new_meta):
    """Deck files are written as exact bytes (MXD2R-03: the CLI hashes physical bytes — text-mode writes would be CRLF on Windows)."""
    folder = Path(folder)
    for name, deck in (('old.in', old), ('new.in', new)):
        (folder / name).write_bytes(deck if isinstance(deck, bytes) else deck.encode('utf-8'))
    for name, meta in (('old.json', old_meta), ('new.json', new_meta)):
        (folder / name).write_text(json.dumps(meta), encoding='utf-8')


def _run_three_cli(folder):
    """Real CLIs of the three development consumers → {consumer: (rc, stdout, stderr)}."""
    folder, scripts = Path(folder), Path(__file__).resolve().parent
    commands = {'readback': ['mixer_deck_readback.py', '--d2', str(folder / 'old.in'), str(folder / 'old.json')],
                'pair': ['mixer_deck_diff.py', str(folder / 'old.in'), str(folder / 'new.in'), '--allow', 'D2',
                         '--meta-ref', str(folder / 'old.json'), '--meta-new', str(folder / 'new.json')],
                'plan': ['mixer_smoke_blind.py', '--d2-plan', str(folder / 'old.in'), '--d2-meta', str(folder / 'old.json')]}
    out = {}
    for key, cmd in commands.items():
        proc = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(scripts / cmd[0]), *cmd[1:]], capture_output=True)
        out[key] = (proc.returncode, proc.stdout.decode('utf-8', 'replace'), proc.stderr.decode('utf-8', 'replace'))
    return out


class D2Consumers(unittest.TestCase):
    def assert_pass(self, result):
        self.assertEqual(result['verdict'], 'PASS', result.get('failures'))
        self.assertFalse(result['execution_authorized'])
        self.assertIsNone(result['registered'])

    def assert_fail(self, result):
        self.assertEqual(result['verdict'], 'FAIL', result)
        self.assertTrue(result['failures'])
        self.assertFalse(result['execution_authorized'])

    def test_generation_and_supported_phase_positive(self):
        for phases, generation, stiff, rho, coated, layered in itertools.product(
                [('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')], ['gen1', 'lab20261014'],
                [1., 20.], [.03, .3, 1., 10.], [False, True], [False, True]):
            with self.subTest(phases=phases, gen=generation, stiff=stiff, rho=rho, coated=coated, layered=layered):
                text, meta, counts = fixture(phases, generation, stiff, rho, coated, layered=layered)
                result = rb.read_d2(text, meta)
                self.assert_pass(result)
                self.assertEqual(result['expected_counts'], counts)
                self.assertEqual(result['density_generation'], generation)
                self.assertLess(abs(result['Bo_SE'] / meta['adhesion_rule']['bo_se'] - 1), 2e-5)

    def test_counts_are_from_actual_inputs(self):
        observed = {}
        for n, cgf, layered, generation in itertools.product([8000, 77777, 100000, 100001],
                [75.7, 151.4, 302.8], [False, True], ['gen1', 'lab20261014']):
            text, meta, counts = fixture(n=n, cgf=cgf, layered=layered, generation=generation)
            result = smoke.d2_plan_check(text, meta)
            self.assert_pass(result)
            self.assertEqual(result['expected_counts'], counts)
            self.assertEqual(result['n_atoms_planned'], sum(counts.values()))
            if n == 100000 and cgf == 151.4: observed[generation] = counts
        self.assertEqual(observed['gen1'], {'1': 176, '2': 859, '3': 98965})
        self.assertEqual(observed['lab20261014'], {'1': 143, '2': 699, '3': 99158})
        self.assertEqual(smoke._expected_counts({'stiffen_se': 20}), {1: 176, 2: 859, 3: 98965})

    def test_d2_pairs_and_old_contracts(self):
        for phases, generation, stiff, rho in itertools.product(
                [('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')], ['gen1', 'lab20261014'], [1., 20.], [.03,.3,1.,10.]):
            a, am, _ = fixture(phases, generation, stiff, rho, False)
            b, bm, _ = fixture(phases, generation, stiff, rho, True)
            self.assert_pass(dd.diff_d2_decks(a, b, am, bm))
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        for allow in ['A','B','U','E','EB']:
            self.assertEqual(dd.diff_decks(a,b,allow=allow)['verdict'], 'FAIL', allow)
        self.assertEqual(set(dd.ALLOW), {'A','B'})
        self.assertNotIn('D2', dd.COHORTS)

    def test_actual_common_mode_mutations(self):
        for transform in [lambda t:t.replace('gravity 9.81', 'gravity 1.0'),
                          lambda t:t.replace('density constant 1640', 'density constant 2000'),
                          lambda t:t.replace('units           si', 'units           cgs'),
                          lambda t:t.replace('radius constant 7.57e-05', 'radius constant 7.58e-05'),
                          lambda t:t.replace('pt1 0.700000', 'pt1 0.710000'),
                          lambda t:t.replace('particles_in_region 842', 'particles_in_region 843')]:
            a,am,_=fixture(); b,bm,_=fixture(coated=True)
            aa,bb=transform(a),transform(b)
            self.assertNotEqual(aa,a)
            self.assert_fail(rb.read_d2(aa,rebound(aa,am)))
            self.assert_fail(dd.diff_d2_decks(aa,bb,rebound(aa,am),rebound(bb,bm)))

    def test_meta_binding_and_numeric_boundaries(self):
        t,m,_=fixture()
        mutations = [lambda q:q.update(dens_gen='gen1'),lambda q:q.update(dens_gen='unknown'),
            lambda q:q.update(dens_gen=' lab20261014'),lambda q:q.update(deck_sha256='0'*64),
            lambda q:q.update(deck_bytes=m['deck_bytes']+1),lambda q:q.update(n_atoms_planned=99999),
            lambda q:q.update(cgf=200.), lambda q:q.update(seed=15485863),
            lambda q:q.update(unrecognized_contract_axis=True),lambda q:q['dens_g_cm3'].update(SE=2.),
            lambda q:q['types'].update({'2':'SE','3':'AM_S'}),lambda q:q['E_Pa'].update(SE=1e7),
            lambda q:q['nu'].update(SE=.37),lambda q:q['radius_m'].update(SE=1e-4),
            lambda q:q['adhesion_rule'].update(gamma_wall=.0256),lambda q:q['adhesion_rule'].update(rho_uncoated_ncm=.2),
            lambda q:q['adhesion_rule'].update(unknown=1),lambda q:q.update(registered='new-policy-v5')]
        for f in mutations:
            q=copy.deepcopy(m);f(q);self.assert_fail(rb.read_d2(t,q))
        for v in [float('nan'),float('inf'),0,-1,True,'0.73','０.７３',1e-310,10**1000,None,[],{}]:
            q=copy.deepcopy(m);q['adhesion_rule']['bo_se']=v;self.assert_fail(rb.read_d2(t,q))
        for q in [None,[],True,{},'meta']:
            self.assert_fail(rb.read_d2(t,q))

    def test_pair_identity_and_orientation(self):
        a,am,_=fixture();b,bm,_=fixture(coated=True)
        self.assert_fail(dd.diff_d2_decks(b,a,bm,am))
        for kwargs in [dict(rho=.2),dict(generation='gen1'),dict(cgf=200.),dict(stiff=1.),dict(bo=1.5),dict(seed=15485863),dict(n=8000)]:
            t,m,_=fixture(coated=True,**kwargs);self.assert_fail(dd.diff_d2_decks(a,t,am,m))
        self.assert_fail(dd.diff_d2_decks(a,a,am,am))

    def test_ceiling_and_ced_meta_rebinding(self):
        t,m,_=fixture()
        lines=t.splitlines(); start=next(i for i,x in enumerate(lines) if 'cohesionEnergyDensity peratomtypepair' in x)
        # Matrix is continued across four rows; alter both symmetric values and rebind the content hash.
        for i in range(start+1,start+5):
            lines[i]=' '.join(str(float(x)*2) if x not in ('&',) else x for x in lines[i].split())
        changed='\n'.join(lines)+'\n'; self.assert_fail(rb.read_d2(changed,rebound(changed,m)))
        # Keep the absolute Bo declaration consistent with CED cubed so only
        # the actual static-overlap ceiling can reject this large-cohesion deck.
        lines=t.splitlines()
        for i in range(start+1,start+5):
            lines[i]=' '.join(str(float(x)*100) if x!='&' else x for x in lines[i].split())
        changed='\n'.join(lines)+'\n';meta=rebound(changed,m)
        meta['adhesion_rule']['bo_se']*=100**3
        result=rb.read_d2(changed,meta)
        self.assert_fail(result)
        self.assertTrue(any('static pair overlap' in failure for failure in result['failures']),result)

    def test_coordinated_density_and_gravity_vector(self):
        # A common density scale preserves all count ratios. Recompute the deck's
        # forces/time consistently, then falsely relabel only the declared table.
        # This must still fail the independent actual-density generation binding.
        canonical=gen.DENS_GENERATIONS['lab20261014']
        try:
            gen.DENS_GENERATIONS['lab20261014']={k:v*1.1 for k,v in canonical.items()}
            a,am,_=fixture();b,bm,_=fixture(coated=True)
        finally:
            gen.DENS_GENERATIONS['lab20261014']=canonical
        for m in (am,bm):m['dens_g_cm3']=dict(canonical)
        self.assert_fail(rb.read_d2(a,am))
        self.assert_fail(dd.diff_d2_decks(a,b,am,bm))
        a,am,_=fixture();b,bm,_=fixture(coated=True)
        aa=a.replace('vector 0.0 0.0 -1.0','vector 0.0 0.0 1.0')
        bb=b.replace('vector 0.0 0.0 -1.0','vector 0.0 0.0 1.0')
        self.assertNotEqual(aa,a)
        self.assert_fail(rb.read_d2(aa,rebound(aa,am)))
        self.assert_fail(dd.diff_d2_decks(aa,bb,rebound(aa,am),rebound(bb,bm)))

    def test_tokens_and_nested_schema(self):
        text,meta,_=fixture()
        for transform in [lambda t:t.replace('density constant 1640','density constant 1_640'),
                          lambda t:t.replace('radius constant 7.57e-05','radius constant ７.57e-05'),
                          lambda t:t.replace('pt1 0.700000','pt1 0_0.700000'),
                          lambda t:t.replace('gravity 9.81','gravity ９.81')]:
            changed=transform(text);self.assertNotEqual(changed,text)
            self.assert_fail(rb.read_d2(changed,rebound(changed,meta)))
        for field in ['dt','steps','physical_s']:
            q=copy.deepcopy(meta);q[field]['unrecognized']=1;self.assert_fail(rb.read_d2(text,q))
        for value in [True, '2', float('nan'),float('inf'),-1]:
            q=copy.deepcopy(meta);q['revolutions']=value;self.assert_fail(rb.read_d2(text,q))

    def test_actual_command_scope(self):
        text,meta,_=fixture()
        for transform in [lambda t:t.replace('gravi all gravity','gravi subset gravity'),
                          lambda t:t.replace('density constant 1640','density gaussian 1640'),
                          lambda t:t.replace('wall/gran model hertz','wall/gran model hooke'),
                          lambda t:t+'\nunfix gravi\n',lambda t:t+'\nset type 3 density 2000\n',
                          lambda t:t+'\ninclude other.in\n']:
            changed=transform(text);self.assertNotEqual(changed,text)
            self.assert_fail(rb.read_d2(changed,rebound(changed,meta)))
        other=fixture(coated=True)
        changed=other[0].replace('neighbor        ', 'neighbor        ',1)
        lines=other[0].splitlines()
        i=next(i for i,line in enumerate(lines) if line.startswith('neighbor'))
        tokens=lines[i].split();tokens[1]=str(float(tokens[1])*1.1);lines[i]=' '.join(tokens)
        changed='\n'.join(lines)+'\n'
        self.assert_pass(rb.read_d2(changed,rebound(changed,other[1])))
        self.assert_fail(dd.diff_d2_decks(text,changed,meta,rebound(changed,other[1])))

    def test_command_lifecycle(self):
        def transform(text,case):
            lines=text.splitlines()
            if case=='early_unfix':
                lines.remove('unfix insA');lines.insert(lines.index('run 1'),'unfix insA')
            elif case=='missing_integrator':
                lines=[line for line in lines if ' all nve/sphere' not in line]
            elif case=='early_rotation':
                moves=[line for line in lines if ' all move/mesh ' in line]
                lines=[line for line in lines if line not in moves]
                index=lines.index('run 1');lines[index:index]=moves
            elif case=='late_integrator':
                line=next(line for line in lines if ' all nve/sphere' in line)
                lines.remove(line);lines.insert(lines.index('run 1')+1,line)
            elif case=='bad_region':return text.replace('region ins_reg particles_in_region','region no_such_region particles_in_region')
            elif case=='no_insert_removal':lines.remove('unfix insA')
            elif case=='missing_mesh':return text.replace('meshes Drum Front Back','meshes Missing Front Back')
            elif case=='bad_rotation_mesh':return text.replace('mesh Drum  rotate','mesh Missing  rotate')
            elif case=='duplicate_region':
                lines.insert(lines.index('run 1'),next(line for line in lines if line.startswith('region ins_reg ')))
            elif case=='unknown_create_region':return text.replace('4 reg','4 unknown',1)
            else:raise AssertionError(case)
            return '\n'.join(lines)+'\n'
        for case in ['early_unfix','missing_integrator','early_rotation','late_integrator','bad_region',
                     'no_insert_removal','missing_mesh','bad_rotation_mesh','duplicate_region','unknown_create_region']:
            with self.subTest(case=case):
                a,am,_=fixture();b,bm,_=fixture(coated=True)
                aa=transform(a,case);bb=transform(b,case)
                self.assertNotEqual(aa,a)
                self.assert_fail(rb.read_d2(aa,rebound(aa,am)))
                self.assert_fail(dd.diff_d2_decks(aa,bb,rebound(aa,am),rebound(bb,bm)))
                self.assert_fail(smoke.d2_plan_check(aa,rebound(aa,am)))

    def test_dt_half_and_legacy_cli_positive(self):
        for factor in [1.,.5,.25]:
            text,meta,counts=fixture(dt_factor=factor);self.assert_pass(rb.read_d2(text,meta))
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            for name,stiff in [('soft',1.),('ref',20.)]:
                text=dd.expected_deck('LC',32452843,stiffen_se=stiff,hold_bo_pairwise=True)
                (p/name).write_text(text)
            proc=subprocess.run([sys.executable,'-I',str(Path(dd.__file__)),str(p/'soft'),str(p/'ref'),'--allow','E'],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            self.assertNotIn('Traceback',proc.stderr)

    def test_cli_and_duplicate_json(self):
        with tempfile.TemporaryDirectory() as temp:
            b=Path(temp);a,am,_=fixture();c,cm,_=fixture(coated=True)
            for name,text,meta in [('a',a,am),('b',c,cm)]:
                # MXD2R-03: the CLI hashes physical bytes — write exact LF bytes (text-mode write = CRLF on Windows)
                (b/(name+'.in')).write_bytes(text.encode('utf-8'));(b/(name+'.json')).write_text(json.dumps(meta))
            scripts=Path(__file__).resolve().parent
            commands=[['mixer_deck_readback.py','--d2',str(b/'a.in'),str(b/'a.json')],
                      ['mixer_deck_diff.py',str(b/'a.in'),str(b/'b.in'),'--allow','D2','--meta-ref',str(b/'a.json'),'--meta-new',str(b/'b.json')],
                      ['mixer_smoke_blind.py','--d2-plan',str(b/'a.in'),'--d2-meta',str(b/'a.json')]]
            for cmd in commands:
                p=subprocess.run([sys.executable,'-I',str(scripts/cmd[0]),*cmd[1:]],capture_output=True,text=True)
                self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                self.assertIn('개발',p.stdout)
            raw=(b/'a.json').read_text();(b/'a.json').write_text(raw.replace('"dens_gen":', '"dens_gen":"gen1", "dens_gen":'))
            for cmd in commands:
                p=subprocess.run([sys.executable,'-I',str(scripts/cmd[0]),*cmd[1:]],capture_output=True,text=True)
                self.assertNotEqual(p.returncode,0)
                self.assertNotIn('Traceback',p.stderr)

    # ── MXD2R (Codex 10-27 · 1저자 11-02 Q1–Q3 (가)) — 반례를 고치기 전에 옮겼다 ─────────────────────────────────
    def _common_mode(self, transform, reason, cli=False):
        """Same mutation in both decks, metadata hash/bytes rebound → all three consumers must reject for `reason`."""
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        aa, bb = transform(a), transform(b)
        self.assertNotEqual(aa, a); self.assertNotEqual(bb, b)
        ma, mb = rebound(aa, am), rebound(bb, bm)
        results = {'readback': rb.read_d2(aa, ma), 'pair': dd.diff_d2_decks(aa, bb, ma, mb), 'plan': smoke.d2_plan_check(aa, ma)}
        for key, result in results.items():
            with self.subTest(api=key):
                self.assert_fail(result)
                self.assertTrue(any(reason in failure for failure in result['failures']), (key, reason, result['failures']))
        if cli:
            with tempfile.TemporaryDirectory() as temp:
                _write_case(temp, aa, bb, ma, mb)
                for key, (rc, out, err) in _run_three_cli(temp).items():
                    with self.subTest(cli=key):
                        self.assertEqual(rc, 1, out + err)
                        self.assertIn(reason, out)
                        self.assertNotIn('Traceback', err)

    def test_mxd2r01_codex_time_insert_rotation(self):
        """MXD2R-01 — Codex 네 공통 변조 (run upto · 늦은 timestep · 삽입 start · Front 주기): API 셋 FAIL · CLI 셋 rc 1 · 사유."""
        for name in ('run_upto', 'late_timestep', 'insert_start_late', 'front_period'):
            with self.subTest(case=name):
                self._common_mode(*CODEX_COMMON_MODE[name], cli=True)

    def test_mxd2r01_same_class_generator_grammar(self):
        """MXD2R-01 같은 부류 — run 옵션 · timestep 위치/토큰 · 삽입 반복/start/속도 · Back 주기 (API 셋)."""
        for name, (transform, reason) in MXD2R01_SAME_CLASS.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason)

    def test_mxd2r02_codex_contact_exclusion_and_friction(self):
        """MXD2R-02 — Codex SE–SE 접촉 제외 · 보조 탐침 마찰 행렬 삭제: API 셋 FAIL · CLI 셋 rc 1 · 사유."""
        for name in ('exclude_SE_SE', 'friction_missing'):
            with self.subTest(case=name):
                self._common_mode(*CODEX_COMMON_MODE[name], cli=True)

    def test_mxd2r02_same_class_contact_and_materials(self):
        """MXD2R-02 같은 부류 — 다른 제외 · 이웃 갱신 옵션 · 재료 fix 결손/중복/값/순서/모르는 이름 · pair 위치/계수 (API 셋)."""
        for name, (transform, reason) in MXD2R02_SAME_CLASS.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason)

    def test_mxd2r02_material_copies_match_generator(self):
        """재료 fix 목록 · 상수 = 생성기 덱에서 뽑은 것과 정확히 같다 (사본이 갈리면 여기서 드러난다 · fail-closed)."""
        text, _, _ = fixture()
        names = [t[4] for t in (line.split() for line in text.splitlines())
                 if len(t) > 4 and t[0] == 'fix' and t[3] == 'property/global']
        self.assertEqual(sorted(names), sorted(rb.D2_MATERIAL))
        self.assertEqual(rb.D2_MATERIAL['coefficientRestitution'][1], gen.COR)
        self.assertEqual(rb.D2_MATERIAL['coefficientFriction'][1], gen.MU_S)
        self.assertEqual(rb.D2_MATERIAL['coefficientRollingFriction'][1], gen.MU_R)
        self.assertIn('fix m9 all property/global characteristicVelocity scalar 2.0\n', text)
        self.assertEqual(rb.D2_MATERIAL['characteristicVelocity'], ('scalar', 2.0))

    def test_mxd2r03_physical_bytes_api(self):
        """MXD2R-03 — API 가 실제 파일 바이트를 받는다: LF 바이트 PASS · CRLF+LF 메타 = SHA 사유 · CRLF+CRLF 메타 (바이트 · 텍스트) = LF-only 사유."""
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        ca, cb = a.replace('\n', '\r\n').encode(), b.replace('\n', '\r\n').encode()
        cam, cbm = rebound_bytes(ca, am), rebound_bytes(cb, bm)
        for key, result in {'readback': rb.read_d2(a.encode(), am), 'pair': dd.diff_d2_decks(a.encode(), b.encode(), am, bm),
                            'plan': smoke.d2_plan_check(a.encode(), am)}.items():
            with self.subTest(lf_bytes=key):
                self.assert_pass(result)
        for key, result in {'readback': rb.read_d2(ca, am), 'pair': dd.diff_d2_decks(ca, cb, am, bm),
                            'plan': smoke.d2_plan_check(ca, am)}.items():
            with self.subTest(crlf_bytes_lf_meta=key):
                self.assert_fail(result)
                self.assertTrue(any('SHA256' in f for f in result['failures']), result['failures'])
        for key, result in {'readback': rb.read_d2(ca, cam), 'pair': dd.diff_d2_decks(ca, cb, cam, cbm),
                            'plan': smoke.d2_plan_check(ca, cam), 'readback_text': rb.read_d2(ca.decode(), cam),
                            'pair_text': dd.diff_d2_decks(ca.decode(), cb.decode(), cam, cbm)}.items():
            with self.subTest(crlf_crlf_meta=key):
                self.assert_fail(result)
                self.assertTrue(any('LF-only' in f for f in result['failures']), result['failures'])

    def test_mxd2r03_physical_bytes_cli_both_directions(self):
        """MXD2R-03 — 세 CLI: LF 바이트 rc 0 · CRLF 덱 + LF 메타 rc 1 (SHA) · CRLF 덱 + CRLF 메타 rc 1 (LF-only 사유)."""
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        ca, cb = a.replace('\n', '\r\n').encode(), b.replace('\n', '\r\n').encode()
        cases = [('lf', (a.encode(), b.encode(), am, bm), 0, '개발'),
                 ('crlf_lf_meta', (ca, cb, am, bm), 1, 'SHA256'),
                 ('crlf_crlf_meta', (ca, cb, rebound_bytes(ca, am), rebound_bytes(cb, bm)), 1, 'LF-only')]
        with tempfile.TemporaryDirectory() as temp:
            for label, decks, rc_want, reason in cases:
                folder = Path(temp) / label
                folder.mkdir()
                _write_case(folder, *decks)
                for key, (rc, out, err) in _run_three_cli(folder).items():
                    with self.subTest(case=label, cli=key):
                        self.assertEqual(rc, rc_want, out + err)
                        self.assertIn(reason, out)
                        self.assertNotIn('Traceback', err)

    def test_mxd2r_positive_codex_independent_48(self):
        """양성 보존 (판정문 §7 (4)) — Codex 독립 정상 48 조합: 세 소비자 PASS · SE Bo · 상별 계획수 독립 산술 일치 · 증서 아님."""
        seen = 0
        for phases, generation, rho, stiff, layered in itertools.product(
                [('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')], ['gen1', 'lab20261014'], [.2, 1., 2.], [1., 20.], [True, False]):
            with self.subTest(phases=phases, gen=generation, rho=rho, stiff=stiff, layered=layered):
                kw = dict(phases=phases, generation=generation, rho=rho, stiff=stiff, layered=layered, n=90007, cgf=135, bo=1.1, seed=49979687)
                a, am, _ = fixture(**kw); b, bm, _ = fixture(coated=True, **kw)
                result = rb.read_d2(a, am)
                for r in (result, dd.diff_d2_decks(a, b, am, bm), smoke.d2_plan_check(a, am)):
                    self.assert_pass(r)
                raw = rb.read_deck(a); se = len(phases)
                rad, dens = raw['templates'][se]['radius'], raw['templates'][se]['density']
                E, nu = raw['E'][se - 1], raw['nu'][se - 1]
                es, rs, ced = E / (2 * (1 - nu * nu)), rad / 2, raw['ced'][se, se]
                bo = ((2 * math.pi * rs * ced) ** 3 / ((4 / 3) * es * math.sqrt(rs)) ** 2) / ((4 / 3) * math.pi * rad ** 3 * dens * 9.81)
                self.assertLess(abs(bo / 1.1 - 1), 2e-5)
                d0 = {'gen1': {'AM': 4800, 'SE': 2000}, 'lab20261014': {'AM': 4850, 'SE': 1640}}[generation]
                nr = [{'AM_P': 56, 'AM_S': 24, 'SE': 18}[p] / (d0['SE' if p == 'SE' else 'AM'] * ({'AM_P': 9, 'AM_S': 4, 'SE': 1}[p] ** 3))
                      for p in phases]
                self.assertEqual(list(result['expected_counts'].values()), [round(90007 * x / sum(nr)) for x in nr])
                seen += 1
        self.assertEqual(seen, 48)


if __name__ == '__main__':
    unittest.main(verbosity=2)
