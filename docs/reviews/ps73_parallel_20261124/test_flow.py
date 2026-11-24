"""Offline regression with the frozen reader, generated deck headers, and a synthetic Slurm journal."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),*sys.argv[2:4]]
KIT=Path(sys.argv[1]).resolve()
del sys.argv[1:]
import site_ops as site
import parallel as p
import engine as e
sys.path.insert(0,str(KIT))
import rt_restore_a5
old=rt_restore_a5.legacy_reader(KIT)
params=p.read(KIT/"unload_params.json")

class Lifecycle(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base=Path(tmp.name).resolve()
        self.ops=self.base/"ops"
        self.root=self.base/"original"
        self.state=self.base/"old"
        self.ops.mkdir()
        (self.ops/"results").mkdir()
        self.root.mkdir()
        self.queue={p.UB_JOB:("RUNNING",6),"401":("RUNNING",20),"402":("PENDING",20)}
        self.calls=[]
        self.counter=500
        (self.root/"selection.json").write_text("untouched")
        self.state.mkdir()
        (self.state/"worker.lock").write_text("untouched")
        for obj,name,val in [(site,"OPS",self.ops),(e,"OPS",self.ops),(e,"ROOT",self.root),
                             (e,"STATE",self.state),(e,"reserved",lambda:None),
                             (site,"command",self.command),(site,"HERE",self.base)]:
            ctx=patch.object(obj,name,val)
            ctx.start()
            self.addCleanup(ctx.stop)
        (self.base/"SOURCE_SHA256SUMS").write_text("fixture")

    def command(self,args):
        if args[0]=="squeue":
            return "".join("%s|%s|%d\n"%(j,s,c) for j,(s,c) in self.queue.items() if s in p.ACTIVE)
        if args[0]=="sacct":
            j=args[args.index("-j")+1]
            return "%s|%s|0:0|02:00:00|5-00:00:00\n"%(j,self.queue[j][0])
        self.assertEqual(args[0],"sbatch")
        self.assertIn("--time=5-00:00:00",args)
        self.assertIn("--ntasks=6",args)
        self.assertIn("--no-requeue",args)
        self.counter+=1
        j=str(self.counter)
        self.calls.append((args[-3],j))
        self.queue[j]=("PENDING",6)
        return j+"\n"

    def test_pending_counts_before_each_and_ub_release(self):
        self.assertEqual(site.capacity(12),58)
        site.process("UT")
        site.process("UC")
        site.process("UB")
        site.process("UVa")
        self.assertEqual(self.calls,[("UT","501"),("UC","502")])
        site.process("UT")
        site.process("UC")
        self.assertEqual(len(self.calls),2)
        self.queue[p.UB_JOB]=("COMPLETED",6)
        p.publish(site.result("UB"),dict(scheduler={"state":"COMPLETED"},receipt={"runner_rc":0,"technical_ok":True}))
        site.process("UVa")
        self.assertEqual(self.calls[-1],("UVa","503"))
        self.assertEqual((self.root/"selection.json").read_text(),"untouched")
        self.assertEqual((self.state/"worker.lock").read_text(),"untouched")

    def test_partial_pair_capacity_changes(self):
        site.process("UT")
        self.queue["403"]=("PENDING",3)
        with self.assertRaisesRegex(ValueError,"CAPACITY_STOP"):
            site.process("UC")
        self.assertEqual(self.calls,[("UT","501")])

    def test_checkpoint_resume_probe_and_no_gain(self):
        site.process("UT")
        self.queue["501"]=("TIMEOUT",6)
        d=site.paths("UT")
        rs=d/"restart"
        rs.mkdir(parents=True)
        step=p.S0+10000
        (rs/("restart_unload_%d.bin"%step)).write_bytes(b"fixture_binary")
        state="".join("variable %s equal %d\n"%(name,step if name=="ul_rstep" else 2)
                      for name in p.FIELDS if name!="ul_kind")+"variable ul_kind string A\n"
        (rs/("state_unload_%d.in"%step)).write_text(state)
        site.process("UT")
        self.assertEqual(self.calls,[("UT","501"),("UT","502")])
        self.assertEqual(p.read(site.attempts("UT")[-1]/"ack.json")["resume"]["step"],step)
        self.queue["502"]=("TIMEOUT",6)
        with self.assertRaisesRegex(ValueError,"NO_FORWARD_CHECKPOINT"):
            site.process("UT")
        (rs/("restart_unload_%d.bin"%(step+1))).write_bytes(b"partial")
        with self.assertRaisesRegex(ValueError,"incomplete latest"):
            p.checkpoint(d)

    def test_control_timeout_never_submits_new_segment(self):
        site.process("UC")
        self.queue["501"]=("TIMEOUT",6)
        with self.assertRaisesRegex(ValueError,"no eligible"):
            site.process("UC")
        self.assertEqual(len(self.calls),1)

    def test_slurm_unknown_fails_closed(self):
        with patch.object(site,"command",return_value=""):
            self.assertEqual(site.acct("123")["state"],"ACCOUNTING_PENDING")

    def test_selection_uses_registered_threshold_and_respects_control(self):
        def data(ut,good=True):
            rows={a:dict(receipt={"technical_ok":True,"endpoint_usable":True,"control_ok":good},verdict={
                  "job":a,"primary_status":"OK","rho_pct":rho}) for a,rho in zip(p.ARMS,(ut,0.,1.,1.))}
            return site.decision(rows,old,params)
        self.assertEqual(data(1.10)["UVa_role"],"selected_for_speed_comparison")
        self.assertEqual(data(1.101)["next"],["UVb"])
        self.assertEqual(data(1.101)["UVa_role"],"auxiliary")
        self.assertEqual(data(1.0,False)["stage"],"TECHNICAL_HOLD")

    def test_restart_probe_uses_sealed_restart_branch_and_np6(self):
        for a in ("UT","UB","UVa"):
            deck=KIT/"decks"/p.BED/("in."+e.original.STAGES[a]+".liggghts")
            text=e.probe_deck(deck.read_text(encoding="utf8"))
            self.assertIn("label ul_resumed",text)
            self.assertNotIn("label ul_next",text)
            self.assertIn("run 0\nvariable probe_atoms equal atoms\n",text)
        self.assertNotIn("reader select",e.run_function(KIT))
        # Execute the actual Bash wrapper with a no-physics substitute MPI program.
        import subprocess
        dest=self.base/"test deck"
        dest.mkdir()
        ck=dest/"checkpoint"
        ck.write_text("nonempty")
        fake=dest/"mpi"
        fake.write_text('#!/bin/bash\ntest "$1" = -np && test "$2" = 6 || exit 2\necho "LIGGGHTS-PUBLIC 3.8.0"\necho "Loop time of 0 on 6 procs"\n')
        fake.chmod(0o700)
        env=dict(os.environ,KIT=str(KIT),BED=p.BED,BASE=str(ck),NP="6",MPIRUN=str(fake),
                 MPIRUN_FLAGS="",LMP="standin",PLATE=str(ck))
        script='set -u\nEXTRA_VARS=()\nFAILS=0\nsay(){ :; }\nnote(){ :; }\ndie(){ exit 2; }\n'+e.run_function(KIT)+'\nrun_deck "$@"\n'
        subprocess.run(["bash","-c",script,"fixture",str(dest),"UT",str(ck),"-","0","screen.txt"],env=env,check=True)
        self.assertIn("PASS rc=0 procs=6",(dest/"run_check.txt").read_text())

    def test_copy_ub_keeps_independent_inodes(self):
        src=self.root/"UB"
        rs=src/"restart"
        rs.mkdir(parents=True)
        step=p.S0+10
        (rs/("restart_unload_%d.bin"%step)).write_bytes(b"fixture")
        (rs/("state_unload_%d.in"%step)).write_text("".join("variable %s equal %d\n"%(n,step if n=="ul_rstep" else 1) for n in p.FIELDS[:-1])+"variable ul_kind string B\n")
        dest=site.paths("UB")
        e.snapshot(src,dest,p.checkpoint(src))
        out=next((dest/"restart").glob("*.bin"))
        out.write_bytes(b"changed private copy")
        self.assertEqual(next(rs.glob("*.bin")).read_bytes(),b"fixture")

    def test_np6_probe_checks_real_marker_and_atom_count(self):
        deck=KIT/"decks"/p.BED/"in.UT.liggghts"
        atoms=params["beds"][p.BED]["atoms"]
        step=p.S0+10000
        ck=self.base/"fixture_restart"
        ck.write_text("fixture")
        mpi=self.base/"fake_mpi"
        mpi.write_text('#!/bin/bash\ntest "$1" = -np && test "$2" = 6 || exit 2\n'
                       'echo "LIGGGHTS-PUBLIC 3.8.0"\necho "Loop time of 0 on 6 procs"\n'
                       'echo "RESTART_PROBE_OK step=%d k=3 atoms=%d"\n'%(step,atoms))
        mpi.chmod(0o700)
        env=dict(os.environ,MPIRUN=str(mpi),MPIRUN_FLAGS="",LMP="standin")
        for expected in (atoms,atoms+1):
            folder=self.base/str(expected)
            folder.mkdir()
            def check():
                e.run_probe(folder,deck,dict(step=step,k=3),env,ck,ck,ck,ck,expected)
            if expected==atoms:
                check()
                self.assertTrue((folder/"probe_ok.json").is_file())
            else:
                with self.assertRaisesRegex(ValueError,"probe refused"):
                    check()
                self.assertFalse((folder/"probe_ok.json").exists())

    def test_registered_cutoff_unusable_uv_a_cannot_block_uv_b(self):
        rows={a:dict(receipt={"technical_ok":True,"endpoint_usable":True,"control_ok":True},
                     verdict={"job":a,"primary_status":"OK","rho_pct":1.0}) for a in p.ARMS}
        rows["UT"]["verdict"]["rho_pct"]=1.2
        rows["UVa"]["receipt"]["endpoint_usable"]=False
        rows["UVa"]["receipt"]["technical_ok"]=False
        self.assertEqual(site.decision(rows,old,params)["next"],["UVb"])
        rows["UT"]["verdict"]["rho_pct"]=1.1
        self.assertEqual(site.decision(rows,old,params)["stage"],"SELECTION_UNRESOLVED")

    def test_second_go_does_not_overwrite_existing_dispatch(self):
        def reserve():
            with patch.object(site.socket,"gethostname",return_value="ibb-master"),patch.object(site,"detach") as launch:
                site.main([p.GO])
                launch.assert_called_once()
        (self.ops/"results").rmdir()
        reserve()
        with self.assertRaises(FileExistsError):
            reserve()
        self.assertEqual(self.calls,[])

    def test_return_is_read_only_and_marks_partial(self):
        import contextlib,hashlib,io,zipfile
        out=io.StringIO()
        with patch.object(site,"status",return_value={"final_ready":False}),contextlib.redirect_stdout(out):
            site.archive()
        name,checksum,flag=out.getvalue().strip().split()
        path=self.ops/name/"ps73_return.zip"
        self.assertEqual((flag,p.digest(path)),("PARTIAL",checksum))
        with zipfile.ZipFile(path) as z:
            for row in z.read("SHA256SUMS").decode().splitlines():
                digest,member=row.split("  ")
                self.assertEqual(hashlib.sha256(z.read(member)).hexdigest(),digest)
        self.assertEqual(self.calls,[])

    def test_terminal_original_ub_timeout_queues_private_resume_only(self):
        self.queue[p.UB_JOB]=("TIMEOUT",6)
        src=self.root/p.BED/"UB"/"restart"
        src.mkdir(parents=True)
        step=p.S0+1000
        first=src/("restart_unload_%d.bin"%step)
        first.write_bytes(b"ub Binary")
        (src/("state_unload_%d.in"%step)).write_text("".join("variable %s equal %d\n"%(n,step if n=="ul_rstep" else 1) for n in p.FIELDS[:-1])+"variable ul_kind string A\n")
        before={f.name:p.digest(f) for f in src.iterdir()}
        site.process("UB")
        site.process("UVa")
        self.assertEqual(self.calls,[("UB","501")])
        self.assertEqual(before,{f.name:p.digest(f) for f in src.iterdir()})
        self.assertEqual(p.read(site.attempts("UB")[0]/"ack.json")["resume"]["step"],step)

if __name__=="__main__":
    unittest.main()
