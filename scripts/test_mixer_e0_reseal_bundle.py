"""Small copy/identity regressions; no engine, host or scheduler."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('reseal', Path(__file__).with_name('mixer_e0_reseal_bundle.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
GATE = 'dem_scripts/mixer_20260921/launch_highbo.sh'


class Reseal(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / 'source'
        self.src.mkdir()

    def inventory(self):
        rows = []
        for i in range(86):
            p = m.OBSERVER if i == 0 else 'fixtures/file%d' % i
            raw = ('source-%d' % i).encode()
            m.put(self.src / p, raw)
            rows.append(dict(path=p, bytes=len(raw), sha256=m.sha(raw), git_blob='old', original_sha256='historical'))
        inv = dict(source_dependencies=rows[:12], launch_snapshot=rows[12:85], preparation_test=rows[85])
        m.put(self.src / m.OBSERVER, b'new-observer')
        return inv

    def package(self):
        m.put(self.src / 'a.txt', b'fixed')
        v = dict(source_pin='1'*40, files=[dict(path='a.txt', bytes=5, sha256=m.sha(b'fixed'))])
        m.put(self.src / GATE, b'fixed gate')
        v['files'].append(dict(path=GATE, bytes=10, sha256=m.sha(b'fixed gate')))
        m.put(self.src / 'PACKAGE_MANIFEST.json', m.encode(v))
        return v

    def b_fixture(self):
        f8 = self.src / m.F8
        assets, sums = [], []
        candidate = self.root / 'candidate'
        for cid in m.CASES:
            for name in ('in.mixer','deck_meta.json','Drum.stl','Front.stl','Back.stl'):
                raw = (cid + '-' + name).encode()
                m.put(f8 / 'planned_assets' / cid / name, raw)
                m.put(candidate / 'candidate_assets' / cid / name, raw + b'-new' if name == 'deck_meta.json' else raw)
                assets.append(dict(path='planned_assets/'+cid+'/'+name, bytes=len(raw), sha256=m.sha(raw)))
                sums.append(m.sha(raw)+'  '+cid+'/'+name)
        m.put(f8 / 'static_asset_manifest.json', m.encode(dict(source_pin='2'*40, files=assets)))
        m.put(f8 / 'planned_assets/SHA256SUMS', ('\n'.join(sums)+'\n').encode())
        rows=[]
        for i in range(12):
            p='scripts/dep%d.py'%i; raw=('code%d'%i).encode(); m.put(self.src/p,raw)
            rows.append(dict(path=p,sha256=m.sha(raw)))
        m.put(f8/'source_seal.json',m.encode(dict(source_pin='2'*40,files=rows)))
        m.put(self.src/m.SMOKE,b'fixed SELF170')
        m.put(self.src/GATE,b'fixed gate')
        m.put(self.src/'PACKAGE_MANIFEST.json',m.encode(dict(files=[dict(path=m.SMOKE,sha256=m.sha(b'fixed SELF170'),bytes=13),dict(path=GATE,sha256=m.sha(b'fixed gate'),bytes=10)])))
        m.put(candidate/'candidate_asset_manifest.json',m.encode(dict(original_asset_generation_pin='2'*40,metadata_generation_source_pin='3'*40)))
        return candidate

    def test_only_observer_inventory_changes(self):
        inv=self.inventory(); new=m.update_inventory(self.src,inv)
        self.assertNotEqual(new['source_dependencies'][0]['sha256'], inv['source_dependencies'][0]['sha256'])
        self.assertEqual(new['source_dependencies'][0]['original_sha256'],'historical')
        self.assertEqual(new['launch_snapshot'],inv['launch_snapshot'])

    def test_other_inventory_drift_refused(self):
        inv=self.inventory(); m.put(self.src/'fixtures/file5',b'drift')
        with self.assertRaisesRegex(ValueError,'unapproved'): m.update_inventory(self.src,inv)

    def test_package_tampering_refused(self):
        self.package(); m.package_check(self.src); m.put(self.src/'a.txt',b'wrong')
        with self.assertRaisesRegex(ValueError,'hash'): m.package_check(self.src)

    def test_extra_package_file_refused(self):
        self.package(); m.put(self.src/'extra',b'new')
        with self.assertRaisesRegex(ValueError,'extra'): m.package_check(self.src)

    def test_existing_or_nested_output_refused(self):
        with self.assertRaises(ValueError): m.safe_output(self.src,self.src/'nested')
        with self.assertRaises(ValueError): m.safe_output(self.src,self.src)
        out=self.root/'new'; self.assertEqual(m.safe_output(self.src,out)[1],out.resolve())

    def test_all_eight_metadata_and_provenance(self):
        candidate=self.b_fixture(); target=self.root/'B'
        m.stage_b(self.src,candidate,target,'4'*40)
        self.assertEqual(m.verify_b(target)['assets'],40)
        manifest=json.loads((target/m.F8/'static_asset_manifest.json').read_bytes())
        self.assertEqual(manifest['source_pin'],'2'*40)
        self.assertEqual(manifest['metadata_generation_source_pin'],'3'*40)
        for cid in m.CASES:
            for name in ('in.mixer','Drum.stl','Front.stl','Back.stl'):
                self.assertEqual((target/m.F8/'planned_assets'/cid/name).read_bytes(),(self.src/m.F8/'planned_assets'/cid/name).read_bytes())
            self.assertTrue((target/m.F8/'planned_assets'/cid/'deck_meta.json').read_bytes().endswith(b'-new'))
        self.assertEqual(json.loads((target/m.F8/'source_seal.json').read_bytes())['source_pin'],'4'*40)

    def test_changed_deck_does_not_finish_B(self):
        candidate=self.b_fixture(); m.put(candidate/'candidate_assets/PRECAL_E0/in.mixer',b'changed')
        with self.assertRaisesRegex(ValueError,'deck/STL'): m.stage_b(self.src,candidate,self.root/'B','4'*40)

    def test_self170_identity_rechecked(self):
        candidate=self.b_fixture(); target=self.root/'B'; m.stage_b(self.src,candidate,target,'4'*40)
        m.put(target/m.SMOKE,b'stale wrapper')
        with self.assertRaisesRegex(ValueError,'tool drift'): m.verify_b(target)

    def test_package_missing_gate_dependency_refused(self):
        manifest=self.package()
        (self.src/GATE).unlink()
        manifest['files']=[r for r in manifest['files'] if r['path']!=GATE]
        m.put(self.src/'PACKAGE_MANIFEST.json',m.encode(manifest))
        with self.assertRaisesRegex(ValueError,'runtime dependency'): m.package_check(self.src)

    def test_gate_dependency_bound_and_rechecked_in_B(self):
        candidate=self.b_fixture(); target=self.root/'B'; m.stage_b(self.src,candidate,target,'4'*40)
        identity=json.loads((target/m.F8/'e0_runtime_tool_identity.json').read_bytes())
        self.assertIn(GATE,[r['path'] for r in identity['files']])
        m.verify_b(target)
        m.put(target/GATE,b'stale gate')
        with self.assertRaisesRegex(ValueError,'tool drift'): m.verify_b(target)


if __name__=='__main__': unittest.main(verbosity=2)
