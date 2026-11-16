"""Static deck tests: no engine, host, or historical result input."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2]/'docs/data/ps45_unload_20261009'
spec = importlib.util.spec_from_file_location('rt_prepare', HERE/'prepare_rt_decks.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
BEDS = ('ps_0_10_r45','ps_3_7_r45','ps_5_5_r45','ps_7_3_r45','ps_10_0_r45')

def block(raw, name):
    return re.search(rb'^# >>> block '+name.encode()+rb'[^\n]*\n.*?^# <<< block '+name.encode()+rb'\r?\n', raw, re.M|re.S).group()

def commands(raw):
    return [line.strip() for line in raw.decode().splitlines() if line.strip() and not line.lstrip().startswith('#')]

class RTDecks(unittest.TestCase):
    def setUp(self):
        self.files=m.generated_additions(SOURCE)

    def deck(self, bed=BEDS[0], kind='RT1'):
        name='decks/'+bed+'/in.'+kind+'.liggghts'
        self.assertIn(name,self.files)
        return self.files[name]

    def test_ten_production_two_fixture_and_one_table(self):
        self.assertEqual(len(self.files),13)
        self.assertEqual(sum(k.endswith('.liggghts') for k in self.files),12)

    def test_all_heads_and_parameters_are_R_bytes(self):
        for bed in BEDS:
            with self.subTest(bed=bed):
                original=(SOURCE/'decks'/bed/'in.R.liggghts').read_bytes()
                for kind in ('RT1','RT2'):
                    for name in ('head','r_params'):
                        self.assertEqual(block(self.deck(bed,kind),name),block(original,name))

    def test_only_restart_write_differs_between_RT_commands(self):
        for bed in BEDS:
            a=commands(self.deck(bed)); b=commands(self.deck(bed,'RT2'))
            self.assertEqual(a.count('write_restart ${out}/rt.bin'),1)
            self.assertEqual([s for s in a if s!='write_restart ${out}/rt.bin'],b)

    def test_30_columns_precision_and_order(self):
        c=commands(self.deck())
        dump=next(x for x in c if x.startswith('dump ul_rp '))
        self.assertEqual(dump.split()[6:],['c_ul_ph[%d]'%i for i in range(1,31)])
        fmt=next(x for x in c if x.startswith('dump_modify ul_rp '))
        self.assertEqual(fmt.count('%.17g'),30)
        self.assertLess(c.index('uncompute cpl'),next(i for i,x in enumerate(c) if x.startswith('compute ul_ph ')))
        self.assertLess(c.index(dump),c.index('run 0'))
        self.assertLess(c.index('run 0'),c.index('write_restart ${out}/rt.bin'))

    def test_exactly_one_read_and_no_balance(self):
        c=commands(self.deck())
        self.assertEqual([x for x in c if x.split()[0]=='read_restart'],['read_restart ${ckpt}'])
        self.assertFalse(any(x.split()[0]=='balance' or (x.startswith('fix ') and ' balance ' in x) for x in c))

    def test_single_wall_compute_and_no_live_dump_at_write(self):
        c=commands(self.deck())
        self.assertEqual(sum(' wall/gran/local ' in x for x in c),1)
        for name in ('ul_rp','ul_ra','ul_rw'):
            self.assertLess(c.index('undump '+name),c.index('write_restart ${out}/rt.bin'))
        self.assertIn('${out}/obs/rt_wall_*.dump', '\n'.join(c))

    def test_ten_zero_RJ_default_3600000(self):
        self.assertIn(b'variable ul_s0 index 3600000',self.deck('ps_10_0_r45'))
        self.assertNotIn(b'variable ul_s0 index 3650000',self.deck('ps_10_0_r45'))

    def test_fixture_and_production_same_rt_body(self):
        for kind in ('RT1','RT2'):
            key='history_test/in.hist_'+kind.lower()+'.liggghts'
            self.assertIn(key,self.files)
            for bed in BEDS:
                self.assertEqual(block(self.files[key],'rt'),block(self.deck(bed,kind),'rt'))

    def test_fixture_parameters_come_from_history_table(self):
        key='history_test/rt_grammar_params.json';self.assertIn(key,self.files)
        p=json.loads(self.files[key]); h=json.loads((SOURCE/'history_test/history_params.json').read_bytes())
        self.assertEqual(p['ul_s0'],sum(h['steps'][k] for k in ('load','shear','hold')))
        self.assertEqual(p['ul_atoms0'],len(h['particles']))
        self.assertEqual((p['ul_s0'],p['ul_atoms0'],p['ul_big']),(2000,20,h['grammar_probe']['big']))

    def test_fixture_head_matches_each_R_semantically(self):
        key='history_test/in.hist_rt1.liggghts';self.assertIn(key,self.files)
        for bed in BEDS:
            self.assertEqual(commands(block(self.files[key],'head')),commands(block((SOURCE/'decks'/bed/'in.R.liggghts').read_bytes(),'head')))

    def test_reject_mutated_fixture_and_production(self):
        self.assertIn('history_test/in.hist_rt1.liggghts',self.files)
        for key,old,new in [('history_test/in.hist_rt1.liggghts',b'run 0',b'run 1'),('decks/ps_10_0_r45/in.RT1.liggghts',b'index 3600000',b'index 3650000')]:
            bad=dict(self.files);bad[key]=bad[key].replace(old,new)
            with self.subTest(key=key),self.assertRaises(ValueError):m.validate_generated(SOURCE,bad)

    def test_no_source_mutation(self):
        before={p.relative_to(SOURCE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.rglob('*') if p.is_file()}
        m.generated_additions(SOURCE)
        after={p.relative_to(SOURCE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

if __name__=='__main__':unittest.main(verbosity=2)
