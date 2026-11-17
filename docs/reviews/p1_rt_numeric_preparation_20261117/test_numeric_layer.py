"""Synthetic legacy differential and copy-only numeric layer checks."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2]/'docs/data/ps45_unload_20261009'
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(SOURCE))
from test_rt_numeric import row, write, flipped, m
import ul_gates


def load(path):
    spec=importlib.util.spec_from_file_location('layer',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def snapshot(root):
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}


class CopyLayer(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def builder(self):
        path=HERE/'prepare_numeric.py'
        self.assertTrue(path.is_file(),'numeric layer builder not implemented')
        return load(path)
    def test_copy_preserves_all_historical_and_prior_layer_bytes(self):
        before=snapshot(SOURCE);old=self.root/'old';new=self.root/'new'
        load(HERE.parent/'p1_rt_runner_preparation_20261117/prepare_rt_runner.py').build(SOURCE,old)
        report=self.builder().build(SOURCE,new)
        self.assertEqual(len(before),94);self.assertEqual(before,snapshot(SOURCE))
        expected=snapshot(old);actual=snapshot(new)
        self.assertEqual(len(expected),111);self.assertEqual(len(actual),113)
        self.assertEqual(expected,{k:actual[k] for k in expected})
        self.assertEqual(actual['rt_numeric.py'],(HERE/'rt_numeric.py').read_bytes())
        self.assertFalse(report['operational_kit_ready']);self.assertFalse(report['consumer_integrated'])
        self.assertEqual(json.loads(actual['RT_NUMERIC_LAYER.json']),report)
    def test_existing_target_refused_without_writing(self):
        target=self.root/'exists';target.mkdir();(target/'sentinel').write_bytes(b'preserve')
        before=snapshot(target)
        with self.assertRaises((ValueError,FileExistsError)):self.builder().build(SOURCE,target)
        self.assertEqual(before,snapshot(target))
    def test_source_overlap_refused(self):
        before=snapshot(SOURCE)
        with self.assertRaises((ValueError,FileExistsError)):self.builder().build(SOURCE,SOURCE)
        self.assertEqual(before,snapshot(SOURCE))
    def test_generated_candidate_keeps_immediate_stop(self):
        target=self.root/'new';self.builder().build(SOURCE,target)
        text=(target/'run_unload_rt_dev.sh').read_text()
        self.assertLess(text.index('exit 2'),text.index('reader()'))
        self.assertIn('RT_RUNNER_LAYER_ONLY',text)
        numeric=load(target/'rt_numeric.py')
        a,b=self.root/'a.dump',self.root/'b.dump'
        write(a,[row()]);write(b,[row()])
        self.assertEqual(numeric.g2cp_compare(b,a,expected_step=2000)['status'],'PASS')
        self.assertFalse((target/'restore_verdict.json').exists())
    def test_legacy_differential_on_synthetic_common_columns(self):
        base=[row(),row(3,.02,.02)]
        cases=[copy.deepcopy(base),[flipped(v) for v in base],base+[flipped(base[0])],base[1:],[],[row(7)]]
        wrapped=copy.deepcopy(base)
        for v in wrapped:
            for i in (0,1,3,4,27,28):v[i]+=.05
        cases.append(wrapped)
        for col in list(range(6))+list(range(9,18))+list(range(25,30))+[8,18,19,20]:
            changed=copy.deepcopy(base);changed[0][col]+=.001;cases.append(changed)
        paths=[self.root/n for n in ('o30','t30','o26','t26')]
        a,b,c,d=paths
        for i,changed in enumerate(cases):
            with self.subTest(case=i):
                write(a,base);write(b,changed);write(c,base,26);write(d,changed,26)
                old=ul_gates.g2c_compare(d,c,expected_step=2000)
                new=m.g2cp_compare(b,a,expected_step=2000)
                self.assertEqual(old['status'],new['status'])
                self.assertEqual(old['n_dup_consistent'],new['n_dup_consistent'])
        self.assertEqual(len(cases),31)


if __name__=='__main__':unittest.main(verbosity=2)
