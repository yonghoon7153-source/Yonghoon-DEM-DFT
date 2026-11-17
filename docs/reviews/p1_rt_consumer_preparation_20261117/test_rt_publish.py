"""Exclusive complete publication; synthetic filesystem failures only."""
import concurrent.futures,importlib.util,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('rt_publish',os.environ.get('RT_PUBLISH_SOURCE',str(HERE/'rt_publish.py')))
M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
class Publish(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.environ.get('RT_TEST_TMPDIR'));self.addCleanup(self.tmp.cleanup);self.job=Path(self.tmp.name)
        self.report={'schema':'rt_restore_candidate_v1','restore_rule':'rev5_g2cp','status':'RESTORED','operational_qualification':False}
    def publish(self):
        self.assertTrue(callable(getattr(M,'publish_new',None)),'publish_new missing');return M.publish_new(self.job,self.report)
    def test_complete_once(self):
        self.publish();p=self.job/'restore_verdict.json';raw=p.read_bytes();self.assertEqual(json.loads(raw),self.report)
        with self.assertRaises(FileExistsError):self.publish()
        self.assertEqual(raw,p.read_bytes());self.assertEqual(len(list(self.job.iterdir())),1)
    def test_existing_file_directory_and_symlink_refused(self):
        target=self.job/'restore_verdict.json'
        for kind in ('file','dir','link'):
            if kind=='file':target.write_bytes(b'old')
            elif kind=='dir':target.mkdir()
            else:
                try:target.symlink_to(self.job/'absent')
                except OSError:continue
            with self.assertRaises(FileExistsError):self.publish()
            if kind=='file':self.assertEqual(target.read_bytes(),b'old')
            if kind=='dir':target.rmdir()
            else:target.unlink()
    def test_two_publishers_one_winner(self):
        self.assertTrue(callable(getattr(M,'publish_new',None)))
        def attempt(_):
            try:M.publish_new(self.job,self.report);return 0
            except FileExistsError:return 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(attempt,range(2)))
        self.assertEqual(sorted(results),[0,1]);self.assertEqual(json.loads((self.job/'restore_verdict.json').read_bytes()),self.report)
    def test_serialization_failure_leaves_no_certificate(self):
        self.report['bad']=float('nan')
        with self.assertRaises(ValueError):self.publish()
        self.assertFalse((self.job/'restore_verdict.json').exists())
    def test_partial_write_and_link_and_fsync_failure(self):
        self.assertTrue(callable(getattr(M,'publish_new',None)))
        for name in ('_write_complete','os.link','os.fsync'):
            def partial(fd,data):
                os.write(fd,b'{');raise OSError('partial')
            with patch.object(M,'_write_complete',side_effect=partial) if name=='_write_complete' else patch(name,side_effect=OSError('injected')):
                with self.assertRaises(OSError):M.publish_new(self.job,self.report)
            self.assertFalse((self.job/'restore_verdict.json').exists());self.assertEqual(list(self.job.iterdir()),[])
    def test_missing_parent_not_created(self):
        self.assertTrue(callable(getattr(M,'publish_new',None)))
        with self.assertRaises(FileNotFoundError):M.publish_new(self.job/'missing',self.report)
        self.assertFalse((self.job/'missing').exists())
    def test_writer_leaves_fd_ownership_to_publisher(self):
        self.assertTrue(callable(getattr(M,'_write_complete',None)))
        fd=os.open(self.job/'probe',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        try:
            M._write_complete(fd,b'complete');self.assertEqual(os.fstat(fd).st_size,8)
        finally:
            try:os.close(fd)
            except OSError:pass
    def test_error_after_link_does_not_delete_complete_certificate(self):
        real_link=os.link
        def link_then_error(source,target):
            real_link(source,target);raise OSError('completion acknowledgement failed')
        with patch('os.link',side_effect=link_then_error):
            with self.assertRaises(OSError):self.publish()
        self.assertEqual(json.loads((self.job/'restore_verdict.json').read_bytes()),self.report)
        with self.assertRaises(FileExistsError):self.publish()

if __name__=='__main__':unittest.main(verbosity=2)
