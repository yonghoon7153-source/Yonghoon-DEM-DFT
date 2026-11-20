"""POSIX collection interruption tests with no scheduler, counterfactual or engine."""
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import mixer_b1_pair_ibb as b
def publish(ctx, record):
    # Also apply the same assertions to the predecessor's actual publication operation.
    if hasattr(b,"publish_return"):
        return b.publish_return(ctx,record)
    return b.put(ctx/"return.json",record)

class CollectionCommit(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def test_no_final_name_before_complete_exclusive_link(self):
        called=[]
        real_link=os.link
        def link(src,dst):
            self.assertFalse((self.root/"return.json").exists())
            self.assertEqual(b.read(src),{"job":"56"})
            called.append(True)
            real_link(src,dst)
        from unittest.mock import patch
        with patch.object(os,"link",link):
            publish(self.root,{"job":"56"})
        self.assertEqual(called,[True])
        raw=(self.root/"return.json").read_bytes()
        with self.assertRaises(FileExistsError):
            publish(self.root,{"job":"57"})
        self.assertEqual((self.root/"return.json").read_bytes(),raw)

    def test_failed_serialization_preserves_previous_artifacts(self):
        partial=self.root/".return-abandoned.tmp"
        partial.write_bytes(b'{"old"')
        with self.assertRaises((TypeError,ValueError)):
            publish(self.root,{"bad":float("nan")})
        self.assertFalse((self.root/"return.json").exists())
        self.assertEqual(partial.read_bytes(),b'{"old"')
        publish(self.root,{"good":True})
        self.assertEqual(b.read(self.root/"return.json"),{"good":True})

    @unittest.skipUnless(sys.platform.startswith("linux"),"requires a Linux process killed inside flock")
    def test_killed_archiver_releases_kernel_lease_for_new_attempt(self):
        # Interrupt the real collect path during creation of its full tar.
        ctx=b.create_attempt(self.root,"U")
        (ctx/"control").mkdir()
        (ctx/"evidence").mkdir()
        name=b.case_name("U")
        here=self.root/"B"/b.F8
        case=here/"cases"/name
        (case/"post").mkdir(parents=True)
        for i in range(1,235):
            (case/"post"/("mix_%d.liggghts"%(i*32976))).write_bytes(b"frame")
        b.put(case/"job_end.json",dict(job_id="56",returncode=0,end_unix=100))
        for k in ("control/pair_pin.json","control/pair_authority.json","B_manifest.json"):
            b.put(self.root/k,{})
        for k in ("campaign_policy.json","approvals/"+name+"/approval.json","admission/"+name+".reservation.json"):
            b.put(here/k,{})
        script="""import pathlib,sys,time,tarfile
sys.path.insert(0,sys.argv[1])
import mixer_b1_pair_ibb as b
root=pathlib.Path(sys.argv[2])
def pause(*args,**kwargs):
    print('locked',flush=True)
    time.sleep(60)
tarfile.TarFile.add=pause
b.base['runtime']=lambda *args: {'matches':True}
b.collect(root,'U','56','56|COMPLETED|0:0|',(0,0,0),True,'a'*40)
"""
        child=subprocess.Popen([sys.executable,"-I","-B","-u","-c",script,str(HERE),str(self.root)],
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(),"locked")
            (old,)=ctx.glob("collection_*")
            partial=(old/"b1_full_result.tar.gz").read_bytes()
            self.assertFalse((ctx/"return.json").exists())
            with self.assertRaises((BlockingIOError,FileExistsError)):
                b.collect(self.root,"U","56","56|COMPLETED|0:0|",(0,0,0),False,"a"*40)
            child.send_signal(signal.SIGKILL)
            child.wait(timeout=5)
            from unittest.mock import patch
            with patch.dict(b.base,runtime=lambda *a: {"matches":True}):
                self.assertEqual(b.collect(self.root,"U","56","56|COMPLETED|0:0|",(0,0,0),False,"a"*40),0)
            pointer=b.read(ctx/"return.json")
            self.assertNotEqual(pointer["directory"],old.name)
            self.assertEqual(pointer["w9"],"RECOVERY_ONLY")
            self.assertEqual(b.verified_sums(ctx/pointer["directory"]),pointer["archive_hashes"])
            self.assertEqual((old/"b1_full_result.tar.gz").read_bytes(),partial)
            self.assertTrue((ctx/"collection.flock").is_file())
        finally:
            if child.poll() is None:
                child.kill()
            child.communicate(timeout=5)

if __name__=="__main__":
    unittest.main()
