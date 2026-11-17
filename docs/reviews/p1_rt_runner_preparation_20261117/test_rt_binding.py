"""Read-only RT record tests with synthetic bytes; no engine or research data."""
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rt_binding',os.environ.get('RT_BINDING_SOURCE',str(HERE/'rt_binding.py')))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Binding(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.environ.get('RT_TEST_TMPDIR'));self.addCleanup(self.tmp.cleanup)
        self.job=Path(self.tmp.name)/'RJ';(self.job/'RT1').mkdir(parents=True);(self.job/'RT2').mkdir()
        self.binary=self.job/'RT1/rt.bin';self.binary.write_bytes(b'synthetic restart bytes')
        self.sha=hashlib.sha256(self.binary.read_bytes()).hexdigest()
        self.job_text=self.job.as_posix();self.path=self.job_text+'/RT1/rt.bin'
        self.rows=['job_dir='+self.job_text,'rt1_bin='+self.path+' sha256='+self.sha,'rt2_ckpt='+self.path+' sha256='+self.sha]
        self.log='# read_restart ignored\nread_restart ${ckpt}\nread_restart '+self.path+'  # expanded\n'
        self.write()
    def write(self):
        (self.job/'run_manifest.txt').write_text('\n'.join(self.rows)+'\n',encoding='utf8')
        (self.job/'RT2/log_screen.liggghts').write_text(self.log,encoding='utf8')
    def check(self,expected='PASS',job=None,**kw):
        self.assertTrue(callable(getattr(m,'check_binding',None)),'RT binding parser is not implemented')
        r=m.check_binding(job or self.job,**kw);self.assertEqual(r['status'],expected,r);return r
    def test_normal_records_and_input_bytes_unchanged(self):
        before={str(p):p.read_bytes() for p in self.job.rglob('*') if p.is_file()}
        r=self.check();self.assertFalse(r['physical_qualification']);self.assertFalse(r['certificate_published'])
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.job.rglob('*') if p.is_file()})
    def test_comments_unexpanded_command_and_inline_comment(self):
        self.log='#read_restart wrong\n# commentary read_restart wrong\nread_restart ${ckpt}\nread_restart '+self.path+'   # trailing\n'
        self.write();self.check()
    def test_duplicate_each_key_even_identical(self):
        original=list(self.rows)
        for i in range(3):
            with self.subTest(key=i):
                self.rows=original+[original[i]];self.write();self.check('SYNTAX_FAIL')
    def test_malformed_hashes_and_extra_tokens(self):
        original=list(self.rows)
        for value in ('',self.sha.upper(),self.sha[:-1],self.sha+'0','g'*64,self.sha+' extra=1'):
            for i in (1,2):
                with self.subTest(value=value,index=i):
                    self.rows=original.copy();self.rows[i]=self.rows[i].split(' sha256=')[0]+' sha256='+value
                    self.write();self.check('SYNTAX_FAIL')
    def test_missing_each_record_is_unconfirmed(self):
        original=list(self.rows)
        for i in range(3):
            with self.subTest(key=i):
                self.rows=original[:i]+original[i+1:];self.write();self.check('UNCONFIRMED')
    def test_missing_files_are_unconfirmed_without_contradiction(self):
        for p in (self.binary,self.job/'RT2/log_screen.liggghts',self.job/'run_manifest.txt'):
            with self.subTest(file=p.name):
                b=p.read_bytes();p.unlink();self.check('UNCONFIRMED');p.write_bytes(b)
    def test_missing_binary_does_not_mask_duplicate_or_hash_conflict(self):
        self.binary.unlink();self.rows.append(self.rows[0]);self.write();self.check('SYNTAX_FAIL')
        self.rows=self.rows[:3];self.rows[2]=self.rows[2].replace(self.sha,'0'*64)
        self.write();self.check('SYNTAX_FAIL')
    def test_missing_job_key_does_not_mask_cross_record_conflict(self):
        self.rows=self.rows[1:];self.rows[1]=self.rows[1].replace(self.path,self.path+'.other')
        self.write();self.check('SYNTAX_FAIL')
    def test_other_job_and_renamed_job_are_syntax_fail(self):
        renamed=self.job.with_name('RJ.try1');self.job.rename(renamed);self.check('SYNTAX_FAIL',job=renamed)
    def test_literal_spelling_required_even_same_resolved_file(self):
        self.log=self.log.replace('read_restart '+self.path,'read_restart '+self.job_text+'/RT1/../RT1/rt.bin')
        self.write();self.check('SYNTAX_FAIL')
    def test_double_slash_honest_spelling_passes(self):
        literal=self.job_text+'/'
        self.rows=['job_dir='+literal]+[k+'='+literal+'/RT1/rt.bin sha256='+self.sha for k in ('rt1_bin','rt2_ckpt')]
        self.log='read_restart '+literal+'/RT1/rt.bin\n';self.write();self.check()
    def test_real_root_alias_and_both_sides_resolve(self):
        alias=self.job.with_name('alias')
        try:alias.symlink_to(self.job,target_is_directory=True)
        except OSError as exc:self.skipTest('directory symlink unavailable: '+type(exc).__name__)
        literal=alias.as_posix();self.rows=['job_dir='+literal]+[k+'='+literal+'/RT1/rt.bin sha256='+self.sha for k in ('rt1_bin','rt2_ckpt')]
        self.log='read_restart '+literal+'/RT1/rt.bin\n';self.write();self.check();self.check(job=alias)
    def test_two_expanded_log_commands_are_syntax_fail(self):
        self.log+='read_restart '+self.path+'\n';self.write();self.check('SYNTAX_FAIL')
    def test_malformed_log_command_beats_missing_binary(self):
        self.binary.unlink();self.log='read_restart '+self.path+' unexpected\n';self.write();self.check('SYNTAX_FAIL')
    def test_missing_expansion_is_unconfirmed(self):
        self.log='#read_restart '+self.path+'\nread_restart ${ckpt}\n';self.write();self.check('UNCONFIRMED')
    def test_actual_file_hash_changed(self):
        self.binary.write_bytes(b'changed restart');self.check('SYNTAX_FAIL')
    def test_existing_certificates_never_written(self):
        for name in ('restore_verdict.json','receipt.json'):(self.job/name).write_bytes(b'original certificate')
        before=[(self.job/n).read_bytes() for n in ('restore_verdict.json','receipt.json')]
        self.check();self.binary.unlink();self.check('UNCONFIRMED')
        self.assertEqual(before,[(self.job/n).read_bytes() for n in ('restore_verdict.json','receipt.json')])
    def test_fixture_ckpt_and_log_layout(self):
        (self.job/'RT2/log.liggghts').write_text(self.log,encoding='utf8')
        (self.job/'RT2/ckpt.txt').write_text(self.path+'\n',encoding='utf8')
        self.check(log_name='log.liggghts',require_ckpt=True)
        (self.job/'RT2/ckpt.txt').write_text(self.path+'.other\n',encoding='utf8')
        self.check('SYNTAX_FAIL',log_name='log.liggghts',require_ckpt=True)
    def test_declared_technical_failure_has_priority(self):
        self.binary.unlink();self.check('SYNTAX_FAIL',technical_ok=False)
    def test_whitespace_or_empty_path_is_syntax_fail(self):
        original=list(self.rows)
        for line in ('job_dir=','job_dir='+self.job_text+' extra',' job_dir='+self.job_text,'job_dir ='+self.job_text):
            self.rows=[line]+original[1:];self.write();self.check('SYNTAX_FAIL')

if __name__=='__main__':unittest.main(verbosity=2)
