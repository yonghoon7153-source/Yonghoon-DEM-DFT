"""Exercise the assembled production entry and the original-site reader on synthetic files."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("A5_TEST_REPO", HERE.parents[2]))
REVIEWS = REPO / "docs/reviews"
SOURCE = REPO / "docs/data/ps45_unload_20261009"

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def sha(b):
    return hashlib.sha256(b).hexdigest()

def identity(folder):
    return {p.relative_to(folder).as_posix():sha(p.read_bytes())
            for p in folder.rglob("*") if p.is_file()}

def run_cli(path, *args):
    return subprocess.run([sys.executable,"-I","-X","utf8","-B",str(path),*map(str,args)],
                          capture_output=True, timeout=60)

class Preseal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(dir=os.environ.get("RT_TEST_TMPDIR"))
        cls.root=Path(cls.tmp.name)
        cls.kit=cls.root/"kit"
        cls.previous=cls.root/"previous"
        previous=load("old_assembly",REVIEWS/"p1_rt_fixture_runner_preparation_20261117/prepare_assembly.py")
        previous.build(SOURCE, cls.previous)
        if os.environ.get("A5_BEFORE")=="1":
            shutil.copytree(cls.previous,cls.kit)
        else:
            builder=load("new_assembly",HERE/"build_a5.py")
            builder.build(REPO,cls.kit)
        cls.consumer_dir=REVIEWS/"p1_rt_consumer_preparation_20261117"
        sys.path.insert(0,str(cls.consumer_dir))
        from test_rt_fixture import fixture
        cls.fixture=staticmethod(fixture)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()
        sys.path.remove(str(cls.consumer_dir))

    def setUp(self):
        self.tmpdir=tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.tmpdir.cleanup)
        self.site=Path(self.tmpdir.name).resolve()/"site"
        self.site.mkdir()
        self.reader=self.kit/"a5_precheck.py"
        self.runner=self.kit/"run_unload_a5_candidate.sh"

    def module(self):
        self.assertTrue(self.reader.is_file(),"A3 consumer must be installed in real kit")
        return load("precheck",self.reader)

    def test_historical_assembly_bytes_and_complete_new_inventory(self):
        original=identity(self.previous)
        current=identity(self.kit)
        self.assertEqual(len(original),128)
        originals_metadata={"RT_DECK_LAYER.json","history_test/RT_HISTORY_SNAPSHOT_SHA256SUMS","RT_ASSEMBLY_SHA256SUMS"}
        self.assertTrue(all(current.get(n)==h for n,h in original.items() if n not in originals_metadata))
        self.assertEqual(current["RT_ASSEMBLY_SHA256SUMS"],"e14f8f2687d04c3cbe0a682fca5b87283e2271d7c05c1dd95ebc15c141965010")
        if os.name=="posix":
            self.assertTrue(original.items() <= current.items())
        self.assertIn("A5_SHA256SUMS",current,"missing full candidate inventory")
        del current["A5_SHA256SUMS"]
        manifest={n:h for h,n in (s.split("  ",1) for s in (self.kit/"A5_SHA256SUMS").read_text().splitlines())}
        self.assertEqual(manifest,current)

    def test_normal_preflight_calls_A3_before_job_creation_and_copies_candidate(self):
        self.assertTrue(self.runner.is_file(),"new production shell absent")
        raw=self.runner.read_text(encoding="utf-8")
        self.assertIn('a5_precheck.py',raw)
        self.assertIn('rt_prerequisites\n',raw)
        self.assertLess(raw.index('  rt_prerequisites\n'),raw.index('JD="$WORK_ROOT/$BED/$JOB"'))
        self.assertIn('done < "$SELF_DIR/A5_SHA256SUMS"',raw)
        self.assertIn('exec bash "$KIT/run_unload_a5_candidate.sh"',raw)
        self.assertIn('rt_grammar_prereq=PASS',raw)
        self.assertIn('"$KIT/rt_dispatch_a5.py" gate',raw)
        self.assertIn('reader restore "$WORK_ROOT" "$BED" --job "$JOB" --publish-new',raw)
        self.assertNotIn('RT_ASSEMBLY_INACTIVE',raw)

    def test_default_entry_cannot_start_job_and_rejects_other_target(self):
        self.assertTrue(self.runner.is_file(),"new RJ candidate missing")
        bash=os.environ.get("RT_BASH") or shutil.which("bash")
        self.assertIsNotNone(bash)
        for args in (["ps_7_3_r45","RJ"],["ps_10_0_r45","RJ","--preflight-only"]):
            cp=subprocess.run([bash,"-s","--",*args],input=self.runner.read_bytes(),capture_output=True,timeout=10)
            self.assertEqual(cp.returncode,2)
            self.assertIn(b"A5_",cp.stderr)

    def test_corrected_production_parsers_match_fixture_headers(self):
        entry=self.kit/"rt_dispatch_a5.py"
        self.assertTrue(entry.is_file(),"production dispatch with corrected numeric modules missing")
        dispatch=load("new_dispatch",entry)
        run=self.fixture(self.site,self.kit)
        pair=run/"RT1/post/rt_pair_2000.dump"; atom=run/"RT1/post/rt_atom_2000.dump"
        for s,ok in ((" ",True),("  ",False),("\t",False)):
            with self.subTest(s=s):
                for f in (pair,atom):
                    lines=f.read_text().splitlines()
                    lines[8]=lines[8].rstrip()+s
                    f.write_bytes(("\n".join(lines)+"\n").encode())
                self.assertEqual(dispatch.R.C.read_atoms(atom,20)["ok"],ok)
                p=dispatch.R.C.N.g2cp_compare(pair,pair,expected_step=2000)
                self.assertEqual(p["status"]=="PASS",ok)

    def test_packaged_observations_match_prior_pins(self):
        m=self.module()
        fixed=m.fixed_files(self.kit)
        self.assertEqual(len(fixed["evidence"]["files"]),45)
        self.assertEqual(fixed["receipt"]["checks"],{k:True for k in fixed["receipt"]["checks"]})
        self.assertEqual(len(fixed["receipt"]["checks"]),20)
        self.assertEqual(sha(fixed["reader"]),fixed["receipt"]["reader_sha256"])
        self.assertEqual(fixed["a4"]["result"]["n_common"],562605)

    def synthetic(self,m):
        """Substitute synthetic identities explicitly inside the test; real CLI uses fixed anchors."""
        fixed=m.fixed_files(self.kit)
        work=self.site/"work";work.mkdir()
        run=self.fixture(work,self.kit)
        sourcekit=work/"kit";sourcekit.mkdir()
        for name in ["RT_CANDIDATE_SHA256SUMS",*json.loads((self.kit/"RT_FIXTURE_CANDIDATE_IDENTITIES.json").read_bytes())]:
            shutil.copyfile(self.kit/"history_test"/name,sourcekit/name)
        for stage,deck in (("P","in.hist_producer.liggghts"),("RT1","in.hist_rt1.liggghts"),("RT2","in.hist_rt2.liggghts")):
            for name in (deck,"plate_hist.stl"):
                shutil.copyfile(sourcekit/name,run/stage/name)
            (run/stage/"deck.txt").write_text(deck+"\n")
        for stage in ("RT1","RT2"):
            for kind in ("atom","pair"):
                p=run/stage/"post"/f"rt_{kind}_2000.dump"
                lines=p.read_text().splitlines()
                lines[8]+=" "
                p.write_bytes(("\n".join(lines)+"\n").encode())
        (self.site/"SOURCE_PIN").write_text(fixed["evidence"]["source_pin"])
        (self.site/"submission.txt").write_text("367546;synthetic\n")
        manifest=run/"run_manifest.txt"
        with manifest.open("a") as f:
            f.write(f"kit={sourcekit.as_posix()}\njob_id=367546\nnp=6\nmode=rt_grammar\nend=complete\n")
            f.write(f"lmp_sha256={m.LMP}\nsums_sha256={sha((sourcekit/'RT_CANDIDATE_SHA256SUMS').read_bytes())}\n")
        facts=fixed["receipt"]
        (run/"rt_grammar_verdict.json").write_text(json.dumps(dict(status="FAIL",exit_code=2,checks=facts["original_checks"])))
        for name in fixed["evidence"]["files"]:
            p=work/name
            if not p.exists():
                p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes(b"synthetic metadata\n")
        fixed["evidence"]=dict(fixed["evidence"],files={n:sha((work/n).read_bytes()) for n in fixed["evidence"]["files"]})
        return fixed

    def test_verified_reader_replays_original_files_and_keeps_old_failure(self):
        m=self.module();f=self.synthetic(m)
        old=self.site/"work/fixture/rt_grammar_verdict.json"
        before=old.read_bytes()
        result=m.check_site(self.site,m.LMP,f)
        self.assertTrue(result["ok"],result)
        self.assertEqual(result["checks_passed"],20)
        self.assertEqual(before,old.read_bytes())

    def test_wrong_binary_duplicate_and_raw_change_refused(self):
        m=self.module();f=self.synthetic(m)
        with self.assertRaises(ValueError):m.check_site(self.site,"0"*64,f)
        altered=self.site/"work/fixture/RT1/in.hist_rt1.liggghts"
        altered.write_bytes(altered.read_bytes()+b"\n")
        with self.assertRaises(ValueError):m.check_site(self.site,m.LMP,f)
        altered.unlink()
        with self.assertRaises((OSError,ValueError)):m.check_site(self.site,m.LMP,f)

    def test_copy_and_pass_only_paper_refused(self):
        m=self.module();f=self.synthetic(m)
        clone=self.site.with_name("copy");shutil.copytree(self.site,clone)
        with self.assertRaises(ValueError):m.check_site(clone,m.LMP,f)
        frontend=run_cli(self.reader,self.site,"--lmp-sha",m.LMP,"--bed-input",self.site)
        self.assertEqual(frontend.returncode,2,"fixed anchors must refuse synthetic 45 files")
        self.assertFalse(json.loads(frontend.stdout)["ok"])
        f["receipt"]={"status":"PASS"}
        with self.assertRaises((ValueError,KeyError)):m.check_site(self.site,m.LMP,f)

    def test_changed_reader_a4_receipt_and_return_report_refused(self):
        m=self.module()
        with tempfile.TemporaryDirectory(dir=self.root) as temp:
            local=Path(temp)
            for name in m.ANCHORS:shutil.copyfile(self.kit/name,local/name)
            for name in m.ANCHORS:
                p=local/name;original=p.read_bytes();p.write_bytes(original+b"\n")
                with self.assertRaises(ValueError):m.fixed_files(local)
                p.write_bytes(original)

    def test_registered_26_rule_review_set_retains_legacy_rules(self):
        self.assertTrue((self.kit/"A5_active_rules.json").is_file(),"candidate rule inventory absent")
        old=json.loads((self.previous/"active_rules.json").read_bytes())
        new=json.loads((self.kit/"A5_active_rules.json").read_bytes())
        by_id={r["id"]:r for r in new["rules"]}
        self.assertEqual(len(by_id),26)
        self.assertEqual(set(by_id)-{r["id"] for r in old["rules"]},{"rt_grammar_prereq","g2cp_roundtrip"})
        self.assertEqual(new["forbidden_rules"],old["forbidden_rules"])
        self.assertEqual(new["forbidden"],old["forbidden"])
        for r in old["rules"]:
            if r["id"] not in ("stage_rc","parse_complete","restore_complete","grammar_prereq"):
                self.assertEqual(r,by_id[r["id"]])

    def test_certificate_consumer_requires_bound_proofs_and_complete_receipt(self):
        m=self.module()
        restore=load("certificate_consumer",self.kit/"rt_restore_a5.py")
        job=self.site/"ps_7_3_r45/RJ";job.mkdir(parents=True)
        cert=dict(schema="rt_restore_candidate_v1",restore_rule="rev5_g2cp",status="RESTORED",bed="ps_7_3_r45",job="RJ")
        (job/"restore_verdict.json").write_text(json.dumps(cert))
        lines=["grammar_prereq=PASS","rt_grammar_prereq=PASS","orig_grid_prereq=PASS",
               "rt_grammar_verdict_sha256="+m.ANCHORS["a3_return.json"],
               "a3_readback_reader_sha256="+m.ANCHORS["a3_corrected_reader.py"],
               "a4_historical_sha256="+m.ANCHORS["a4_continuity.json"],"end=fixture fails=0 reader_rc=0"]
        def accepts(selected):
            (job/"run_manifest.txt").write_text("\n".join(selected)+"\n")
            return restore.job_restored(self.site,"ps_7_3_r45","RJ",self.kit)
        self.assertFalse(accepts(lines))
        for i in range(len(lines)):
            self.assertFalse(accepts(lines[:i]+lines[i+1:]),lines[i])
        self.assertFalse(accepts(lines+["rt_grammar_prereq=PASS"]))
        self.assertFalse(accepts(lines[:-1]+["end=fixture fails=0 reader_rc=2"]))

    def test_digest_binds_exclusive_publication_to_same_completed_job(self):
        m=self.module()
        restore=load("fresh_certificate_consumer",self.kit/"rt_restore_a5.py")
        from test_rt_contract import BASE,job_fixture
        bed="ps_7_3_r45"
        original,reference,rows=job_fixture(self.site,bed=bed)
        report=restore.C.evaluate(original,bed=bed,step=2000,atoms=800,reference_contact=reference,
            grid_text="2 by 2 by 1 MPI processor grid\non 4 procs",grid=(2,2,1),written_np=4,
            legacy_checks=BASE,job_kind="RJ")
        self.assertEqual(report["status"],"RESTORED")
        job=self.site/bed/"RJ";job.mkdir(parents=True)
        manifest=job/"run_manifest.txt";cert=job/"restore_verdict.json"
        sums=sha((self.kit/"A5_SHA256SUMS").read_bytes())
        prefix=("bed="+bed+"\njob=RJ\nnp=6\nresume=0\ngate=ALLOW\njob_dir="+str(job)+
                "\nstart=2026-11-20T00:01:00Z\nsums_sha256="+sums+"\nlmp_sha256="+m.LMP+
                "\ngrammar_prereq=PASS\nrt_grammar_prereq=PASS\norig_grid_prereq=PASS"+
                "\nrt_grammar_verdict_sha256="+m.ANCHORS["a3_return.json"]+
                "\na3_readback_reader_sha256="+m.ANCHORS["a3_corrected_reader.py"]+
                "\na4_historical_sha256="+m.ANCHORS["a4_continuity.json"]+"\n").encode()
        end=b"reader_restore_rc=0\nreader_kebase_rc=0\nend=fixture fails=0 reader_rc=0\n"
        manifest.write_bytes(prefix)
        def accepts():
            return restore.job_restored(self.site,bed,"RJ",self.kit)
        with patch.object(restore,"restore",return_value=report),contextlib.redirect_stdout(io.StringIO()):
            result=restore.main([str(self.site),bed,"--kit",str(self.kit),"--publish-new"])
        self.assertEqual(result,0)
        record=manifest.read_bytes();issued=cert.read_bytes();h=sha(issued).encode()
        self.assertIn(b"a5_certificate_sha256="+h+b"\n",record)
        self.assertFalse(accepts())
        manifest.write_bytes(record+end);self.assertTrue(accepts())
        document=json.loads(issued)
        for key in ("G2cp","cont_R","cont_RT1","rt_binding","rt_post_list","g0"):
            altered=json.loads(issued);del altered["checks"][key]
            raw=json.dumps(altered).encode();cert.write_bytes(raw)
            manifest.write_bytes(record.replace(h,sha(raw).encode())+end)
            self.assertFalse(accepts(),key)
        subset={k:document[k] for k in ("schema","restore_rule","status","bed","job")}
        for bad in (subset,{**document,"certificate_published":False}, {**document,"job":"RJ2"}):
            raw=json.dumps(bad).encode();cert.write_bytes(raw)
            manifest.write_bytes(record.replace(h,sha(raw).encode())+end);self.assertFalse(accepts())
        cert.write_bytes(issued+b" ");manifest.write_bytes(record+end);self.assertFalse(accepts())
        cert.write_bytes(issued)
        for rec in (record.replace(b"00:01",b"00:02")+end,record+end+end,record+end.replace(b"rc=0",b"rc=2"),
                    record+end+b"extra=1\n",record+record[len(prefix):]+end,record+end.replace(b"reader_restore_rc=0\n",b"")):
            manifest.write_bytes(rec);self.assertFalse(accepts())
        manifest.write_bytes(record+end)
        with patch.object(restore,"restore",return_value=report),contextlib.redirect_stderr(io.StringIO()):
            self.assertNotEqual(restore.main([str(self.site),bed,"--kit",str(self.kit),"--publish-new"]),0)
        self.assertEqual(cert.read_bytes(),issued);self.assertEqual(manifest.read_bytes(),record+end)

    @unittest.skipUnless(os.name=="posix","full runner test uses POSIX executable mode")
    def test_real_preflight_no_job_write_positive_and_changed_deck_negative(self):
        m=self.module()
        fixed=self.synthetic(m)
        kit=self.site.parent/"fullkit";shutil.copytree(self.kit,kit)
        work=self.site.parent/"work";work.mkdir()
        source=work/"ps_7_3_r45/in";source.mkdir(parents=True)
        prm=json.loads((kit/"unload_params.json").read_bytes())["beds"]["ps_7_3_r45"]
        (source/prm["last_deck"]).write_text("run 0\n")
        (source/prm["orig_log"]).write_text("6 by 4 by 1 MPI processor grid\nLoop time of 0 on 24 procs\n")
        (source/prm["in_files"]["contact"]["file"]).write_bytes(b"synthetic reference")
        fake=self.site.parent/"synthetic-lmp"
        fake.write_text("#!/bin/sh\nexit 91\n");fake.chmod(0o700)
        binary=sha(fake.read_bytes())
        manifest=self.site/"work/fixture/run_manifest.txt"
        manifest.write_bytes(manifest.read_bytes().replace(m.LMP.encode(),binary.encode()))
        fixed["evidence"]["files"]["fixture/run_manifest.txt"]=sha(manifest.read_bytes())
        evidence=kit/"a3_inputs.json";evidence.write_text(json.dumps(fixed["evidence"]))
        # Bind only this scratch candidate to manufactured files/binary, never to the returned archive.
        checker=kit/"a5_precheck.py"
        checker.write_text(checker.read_text().replace(m.LMP,binary).replace(m.ANCHORS["a3_inputs.json"],sha(evidence.read_bytes())))
        if (kit/"a4_receipt.json").exists():
            ref=kit/"a4_receipt.json";proof=json.loads(ref.read_bytes())
            names=proof["original_inputs_sha256_matched_to_historical_pins"]
            for key,n in (("reference.dump",prm["in_files"]["contact"]["file"]),
                         ("writer.log",prm["orig_log"]),("writer.deck",prm["last_deck"])):
                names[key]=sha((source/n).read_bytes())
            ref.write_text(json.dumps(proof))
            checker.write_text(checker.read_text().replace(m.ANCHORS["a4_receipt.json"],sha(ref.read_bytes())))
        sums=kit/"A5_SHA256SUMS"
        sums.write_text("".join(sha((kit/n).read_bytes())+"  "+n+"\n" for n in
                                (r.split("  ",1)[1] for r in sums.read_text().splitlines())))
        shim=self.site.parent/"synthetic-python"
        shim.write_text("#!/bin/sh\ncase \"$2:$3\" in */ul_reader.py:inputs|*/ul_reader.py:grammar|*/rt_dispatch_a5.py:gate) exit 0;; esac\nexec "+sys.executable+' "$@"\n')
        shim.chmod(0o700)
        gram=self.site.parent/"old_grammar.json";gram.write_text("{}")
        env=dict(os.environ,WORK_ROOT=str(work),RT_FIXTURE_SITE=str(self.site),PY=str(shim),LMP=str(fake),
                 GRAMMAR_VERDICT=str(gram),MPIRUN="/bin/false",NP="6",ALLOW_OTHER_LMP="1",ALLOW_CONCURRENT="1",
                 PYTHONDONTWRITEBYTECODE="1")
        args=["bash",str(kit/"run_unload_a5_candidate.sh"),"ps_7_3_r45","RJ","--preflight-only"]
        def exercise():
            return subprocess.run(args,env=env,capture_output=True,timeout=60)
        green=exercise()
        self.assertEqual(green.returncode,0,(green.stdout+green.stderr).decode(errors="replace"))
        self.assertIn(b'"checks_passed": 20',green.stdout)
        self.assertFalse((source.parent/"RJ").exists())
        lp=source/prm["orig_log"]
        original=lp.read_bytes();lp.write_bytes(original+b"# still the same grid\n")
        different=exercise()
        self.assertNotEqual(different.returncode,0,"wrong writer log admitted with the correct grid text")
        self.assertIn(b"writer.log",different.stdout)
        lp.write_bytes(original)
        (self.site/"work/fixture/RT1/in.hist_rt1.liggghts").write_text("different")
        denied=exercise()
        self.assertNotEqual(denied.returncode,0)
        self.assertIn(b"original-site reread",denied.stderr)
        self.assertFalse((source.parent/"RJ").exists())

if __name__=="__main__":
    unittest.main(verbosity=2)
