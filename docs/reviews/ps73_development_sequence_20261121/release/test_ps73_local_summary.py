"""Synthetic author-return tests, with separate UT endpoint and UTc separation."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
import zipfile

spec=importlib.util.spec_from_file_location('local_summary', Path(__file__).with_name('local_summary.py'))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def js(obj):
    return (json.dumps(obj,separators=(',',':'))+'\n').encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def archive(path, armnames, row=None, corrupt=False):
    parts={}
    for i,a in enumerate(armnames):
        arm='UT3' if row=='t3' else 'UB'
        sel=js({'stage':'resolved','tuple':row,'arm':arm})
        v=js({'job':a,'bed':'ps_7_3_r45','rho_pct':1 if a=='UT' else 2,
              'primary_status':'synthetic','trajectory_status':'full' if a=='UTc' else 'endpoint'})
        raw={a+'/arm_verdict.json':v,a+'/run_manifest.txt':b'fixture', 'selection.json':sel}
        buffer=io.BytesIO()
        with tarfile.open(mode='w:gz',fileobj=buffer) as t:
            for n,b in raw.items():
                h=tarfile.TarInfo(n); h.size=len(b); t.addfile(h,io.BytesIO(b))
        p=buffer.getvalue()
        parts['reports/'+a+'.report.tgz']=p
        parts['state/jobs/'+a+'/receipt.json']=js({'arm':a,'state':'COMPLETED','exit_code':'0:0','technical_ok':True,
           'job_id':str(100+i),'report_sha256':sha(p),'manifest_sha256':sha(b'fixture'),
           'verdict_sha256':sha(v) if not corrupt else '0'*64,'selection_sha256':sha(sel)})
    if row:
        parts['state/sequence_result.json']=js({'status':'REVIEW','plan':{'tuple':row,'completed':armnames,'reason':'PS73_PRIMARY_REVIEW'}})
        parts['reports/selection.json']=sel
    parts['collection.json']=js({'submitted_by_collection':False,'terminal_reports':armnames,'captured_utc':'test'})
    parts['SHA256SUMS']=''.join(sha(v)+'  '+n+'\n' for n,v in parts.items()).encode()
    with zipfile.ZipFile(path,'w') as z:
        for n,v in parts.items(): z.writestr(n,v)


class TestLocalSummary(unittest.TestCase):
    def check(self,arms,row=None,corrupt=False):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ret.zip'
            archive(p,arms,row,corrupt)
            return m.summarize(p)

    def test_partial_ub_is_never_final(self):
        r=self.check(['UB'])
        self.assertIsNone(r['selected_comparison'])
        self.assertEqual(r['sequence_status'],'PARTIAL_RETURN')

    def test_t3_separates_primary_and_auxiliary(self):
        r=self.check(['UB','UT','UC','UVb','UTc'],'t3')['selected_comparison']
        self.assertEqual((r['primary_arm'],r['rho_pct']),('UT',1))
        self.assertEqual((r['auxiliary_arm'],r['trajectory_status']),('UTc','full'))

    def test_invalid_source_stops_report(self):
        with self.assertRaises(ValueError):
            self.check(['UB'],corrupt=True)

    def test_missing_control_blocks_final_comparison(self):
        with self.assertRaises(ValueError):
            self.check(['UB','UT','UVa'],'t1')

if __name__=='__main__':
    unittest.main()
