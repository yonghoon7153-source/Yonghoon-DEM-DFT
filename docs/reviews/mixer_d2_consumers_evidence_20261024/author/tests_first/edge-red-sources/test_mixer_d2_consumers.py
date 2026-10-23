#!/usr/bin/env python3
"""D2 development consumer regressions; synthetic decks only, no simulator."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
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
                (b/(name+'.in')).write_text(text);(b/(name+'.json')).write_text(json.dumps(meta))
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
