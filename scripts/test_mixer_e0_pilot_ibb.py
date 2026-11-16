"""Synthetic parser/approval/watch regressions; no scheduler, engine or network."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

s=importlib.util.spec_from_file_location('pilot',os.environ.get('E0_TEST_SOURCE',str(Path(__file__).with_name('mixer_e0_pilot_ibb.py'))))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class Pilot(unittest.TestCase):
    def test_queue_counts_cpu_and_case_workdir(self):
        q='1|g2cp|RUNNING|4|cpu-60|cpu|/work/g2cp\n2|runner|PENDING|20|cpu-60|cpu|/work/cases/PRECAL_E0\n'
        self.assertEqual(m.queue_counts(q),(24,1))
        self.assertEqual(m.queue_counts(''),(0,0))

    def test_malformed_queue_is_not_empty(self):
        for q in ['broken','1|x|RUNNING|unknown|cpu-60|cpu|/work','1|x|NEW_STATE|20|cpu-60|cpu|/work']:
            with self.subTest(q=q),self.assertRaises(ValueError):m.queue_counts(q)

    def test_storage_requires_ost_and_both_floors(self):
        df='Filesystem 1B-blocks Used Available Use% Mounted\nx 999999999999 0 40000000000 0% /work\n'
        di='Filesystem Inodes IUsed IFree IUse% Mounted\nx 99999 1 99998 1% /work\n'
        ost='UUID 1K-blocks Used Available Use% Mounted\nfs-OST0000_UUID 999999999 1 40000000 1% /work[OST:0]\n'
        self.assertTrue(m.storage_ok(df,di,ost)['disk_budget_verified'])
        for a,b,c in [(df.replace('40000000000','3'),di,ost),(df,di.replace('99998','1'),ost),(df,di,'no OST data')]:
            with self.assertRaises(ValueError):m.storage_ok(a,b,c)

    def test_qos_and_association_are_real_outputs(self):
        m.scheduler_ok('cpu-60|cpu=60,gres/gpu=0|\n','operator|cpu-60|7-00:00:00|\n','PartitionName=cpu State=UP MaxTime=14-00:00:00','operator')
        for qos,assoc,part in [('cpu-60|cpu=600|','operator|cpu-60|7-00:00:00|','State=UP MaxTime=14-00:00:00'),('cpu-60|cpu=60|','operator|other|7-00:00:00|','State=UP MaxTime=14-00:00:00'),('cpu-60|cpu=60|','operator|cpu-60|7-00:00:00|','State=DOWN MaxTime=14-00:00:00')]:
            with self.assertRaises(ValueError):m.scheduler_ok(qos,assoc,part,'operator')

    def test_runtime_file_list_keeps_order_and_exact_json(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'a').write_bytes(b'a');(root/'b').write_bytes(b'b')
            meta=root/'p.json';m.put(meta,{'files':['a','b']})
            ref={'json_sha256_or_reason':m.sha(meta),'files':[[1,'f','0','f','1','0',m.sha(root/'a')],[2,'f','0','f','1','0',m.sha(root/'b')]]}
            self.assertEqual(m.package_rows(root,meta,ref)[1],[])
            (root/'a').write_bytes(b'b');(root/'b').write_bytes(b'a')
            self.assertEqual(len(m.package_rows(root,meta,ref)[1]),2)
            # This fixture deliberately changes existing metadata; put() stays exclusive.
            meta.write_text(json.dumps({'files':['b','a']}),encoding='utf8')
            with self.assertRaises(ValueError):m.package_rows(root,meta,ref)

    def test_numeric_progress_not_name_sort_or_mtime(self):
        state={};m.progress(state,'RUNNING',100,[99000,990000],50)
        self.assertEqual(state['max_step'],990000)
        self.assertTrue(m.progress(state,'RUNNING',1901,[99000,990000],50))
        self.assertFalse(m.progress(state,'RUNNING',1902,[1000000],50))

    def test_pending_and_finished_do_not_trip_stall(self):
        for status in ['PENDING','COMPLETED']:
            self.assertFalse(m.progress({},status,9999,[],1))
        self.assertTrue(m.progress({},'RUNNING',1900,[],1))

    def test_logs_ignore_comments_info_and_partial_rows(self):
        text='# ERROR example\nINFO: harmless\nStep Atoms KinEng A B\n1 10 0 0 0\n20 10 0 0 0\nLoop time x\n'
        self.assertEqual(m.log_flags(text),{'error':0,'quota':0,'nonfinite':0,'lost':0,'last_step':20,'last_atoms':10,'initial_atoms':10})
        self.assertEqual(m.log_flags('INFO: INF nan\n')['nonfinite'],0)
        self.assertEqual(m.log_flags(text+'Step Atoms KinEng A B\n21 10')['nonfinite'],0)

    def test_real_error_nonfinite_and_loss(self):
        text='ERROR from rank\nStep Atoms KinEng A B\n1 10 0 0 0\n20 9 nan 0 0\nDisk quota exceeded\n'
        flags=m.log_flags(text)
        for k in ['error','quota','nonfinite','lost']:self.assertEqual(flags[k],1)

    def test_terminal_record_is_exact_job_not_batch_or_empty(self):
        self.assertIsNone(m.terminal('4.batch|COMPLETED|0:0\n','4'))
        self.assertIsNone(m.terminal('','4'))
        self.assertIsNone(m.terminal('4|RUNNING|0:0\n','4'))
        self.assertEqual(m.terminal('4|FAILED|1:0\n','4')['state'],'FAILED')

    def test_only_e0_scope_and_limits(self):
        p=m.policy('approved-root','a'*64)
        self.assertEqual(p['max_concurrency'],1);self.assertEqual(p['np'],20)
        self.assertEqual(m.CASE,'PRECAL_E0');self.assertEqual(m.WALLTIME,'1-00:00:00')
        self.assertEqual(m.FREE_BYTES,32193231348);self.assertEqual(m.MAX_BYTES,29266573952)

    def test_collection_inventory_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);(p/'one').write_bytes(b'one')
            rows=m.inventory(p);self.assertEqual(rows[0]['sha256'],m.sha(p/'one'))
            try:(p/'link').symlink_to(p/'one')
            except OSError:self.skipTest('OS does not grant symlink creation')
            with self.assertRaises(ValueError):m.inventory(p)

    def test_inventory_link_guard_without_os_link_privilege(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);(p/'one').write_bytes(b'one')
            with patch.object(Path,'is_symlink',return_value=True),self.assertRaises(ValueError):
                m.inventory(p)

    def test_terminal_truncated_rows_are_incomplete_not_index_errors(self):
        for text in ('4','4|COMPLETED','4|COMPLETED|0:0\n4|FAILED|1:0'):
            with self.subTest(text=text):self.assertIsNone(m.terminal(text,'4'))

    def test_explicit_author_scope_is_bound_to_approved_B_and_controller(self):
        self.assertTrue(hasattr(m,'author_scope'),'missing explicit authority binding')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'control').mkdir()
            manifest={'approved_return_sha256':'a'*64,'source_pin':'b'*40}
            m.put(root/'B_manifest.json',manifest)
            go=dict(schema='mixer_e0_author_go/1',execution_authorized=True,
                    allowed_to_submit=[m.CASE],author_action='GO_E0_ONCE',label='DEVELOPMENT_DATA_ONLY',
                    approved_B_manifest_sha256=m.sha(root/'B_manifest.json'),
                    approved_reseal_return_sha256='a'*64,pilot_controller_sha256=m.sha(m.__file__))
            m.put(root/'control/author_go.json',go)
            m.author_scope(root,manifest)
            for key,bad in [('execution_authorized',False),('allowed_to_submit',['PRECAL_N0']),
                            ('approved_B_manifest_sha256','c'*64),('pilot_controller_sha256','c'*64),
                            ('approved_reseal_return_sha256','c'*64),('author_action','YES')]:
                changed=dict(go);changed[key]=bad
                (root/'control/author_go.json').write_text(json.dumps(changed))
                with self.subTest(key=key),self.assertRaises(ValueError):m.author_scope(root,manifest)

    def test_watch_budget_does_not_cancel_or_submit(self):
        self.assertTrue(hasattr(m,'WATCH_LIMIT_SECONDS'),'monitor budget missing')
        with tempfile.TemporaryDirectory() as td:
            with patch.object(m.time,'monotonic',side_effect=[0,m.WATCH_LIMIT_SECONDS+1]),patch.object(m,'command') as cmd:
                with self.assertRaisesRegex(ValueError,'monitor budget'):
                    m.wait_job(Path(td),Path(td),'4')
                cmd.assert_not_called()

    def test_live_preflight_timeout_never_retries_collection(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);clock=iter([0,11,22,33,44,55,66,77])
            def fake(folder,label,argv,timeout=60):return '',{}
            with patch.object(m,'runtime',return_value={'matches':True}),patch.object(m,'scheduler_ok'),\
                 patch.object(m,'capture',side_effect=fake) as cap,patch.dict(os.environ,{'USER':'operator'}),\
                 patch.object(m.time,'time',side_effect=lambda:next(clock)):
                with self.assertRaises(ValueError):m.preflight(root,root/'bin',root/'mpi',root)
                self.assertEqual(cap.call_count,8,'three fixed checks + one collection of five; no retry')

    def test_ambiguous_submission_calls_guard_once_and_preserves_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'evidence').mkdir();(root/'returns').mkdir();(root/'control').mkdir()
            (root/'binary').write_bytes(b'b');(root/'mpi').write_bytes(b'm')
            m.put(root/'B_manifest.json',{'files':[]})
            case=root/'B'/m.F8/'cases'/m.CASE;case.mkdir(parents=True)
            report=root/'returns/e0_report.tar.gz';report.write_bytes(b'fake report')
            argv=['pilot','--root',str(root),'--binary',str(root/'binary'),'--mpi',str(root/'mpi'),'--env-prefix',str(root)]
            authority=patch.object(m,'author_scope',create=True)
            with patch.object(m.sys,'argv',argv),patch.object(m.sys,'platform','linux'),patch.dict(os.environ,{'USER':'operator'},clear=True),\
                 patch.object(m,'verify_deployment'),patch.object(m,'preflight'),authority,\
                 patch.object(m,'prepare_approval',return_value=(root/'approval.json',case)),\
                 patch.object(m,'command',return_value=SimpleNamespace(returncode=1,stdout='',stderr='synthetic ambiguous')) as call,\
                 patch.object(m,'report_archive',return_value=m.ref(report)):
                self.assertEqual(m.main(),2)
                self.assertEqual(call.call_count,1)
                self.assertIn('submit_one.py.txt',str(call.call_args.args[0]))
            records=list((root/'evidence').glob('controller_*.json'))
            self.assertEqual(len(records),1)
            self.assertEqual(m.read(records[0])['state'],'INCOMPLETE')

    def test_approved_B_pin_disagreement_is_rejected_before_approval_files(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);here=root/'B'/m.F8;here.mkdir(parents=True)
            m.put(here/'source_seal.json',{'source_pin':'a'*40})
            with self.assertRaisesRegex(ValueError,'B source pin'):
                m.prepare_approval(root,{'source_pin':'b'*40},root/'bin',root/'mpi')
            self.assertFalse((here/'cases').exists())

    def test_authorized_assembly_uses_unchanged_B_guard_one_submission_only(self):
        fixture=os.environ.get('E0_APPROVED_ROOT')
        if not fixture:self.skipTest('approved B return fixture not supplied')
        fixture=Path(fixture)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();shutil.copytree(fixture/'approved_B',root/'B')
            (root/'control').mkdir();(root/'evidence').mkdir()
            shutil.copyfile(fixture/'B_manifest.json',root/'B_manifest.json')
            shutil.copyfile(fixture/'AB_RECEIPT.json',root/'control/AB_RECEIPT.json')
            m.put(root/'control/runtime_reference.json',{'synthetic_fixture':True})
            binary=root/'binary';mpi=root/'mpi';binary.write_bytes(b'fake binary');mpi.write_bytes(b'fake MPI')
            manifest=m.verify_deployment(root)
            m.put(root/'control/author_go.json',dict(schema='mixer_e0_author_go/1',execution_authorized=True,
                author_action='GO_E0_ONCE',allowed_to_submit=[m.CASE],label='DEVELOPMENT_DATA_ONLY',
                approved_B_manifest_sha256=m.sha(root/'B_manifest.json'),
                approved_reseal_return_sha256=manifest['approved_return_sha256'],pilot_controller_sha256=m.sha(m.__file__)))
            m.author_scope(root,manifest)
            m.put(root/'evidence/live_preflight.json',dict(observed_unix=m.time.time(),qos='cpu-60',partition='cpu',
                  qos_verified=True,disk_budget_verified=True,inode_budget_verified=True,d07_finished=True,
                  paths_verified=True,reserved_cpus=0,running_first8=0,qualification_accepted=False))
            original_loader=m.runpy.run_path
            namespaces=[]
            def loader(path):
                ns=original_loader(path);original=ns['canonical_runner']
                # Windows-only path syntax adapter. Guard source bytes remain unchanged.
                # No filesystem, authorization, reservation or process rule is removed.
                def canonical(c,approval):
                    if os.name!='nt':return original(c,approval)
                    copied=dict(c);copied['runner_bindings']=dict(c['runner_bindings'])
                    for key in ('python','job_start','stdout','stderr'):
                        copied['runner_bindings'][key]='/synthetic_posix_bindings/'+key
                    return original(copied,approval)
                ns['main'].__globals__['canonical_runner']=canonical
                ns['canonical_runner']=canonical;namespaces.append(ns);return ns
            with patch.object(m.runpy,'run_path',side_effect=loader):
                ap,case=m.prepare_approval(root,manifest,binary,mpi)
            guard=namespaces[0]
            self.assertEqual(m.read(ap)['source_pin'],manifest['source_pin'])
            for row in manifest['files']:
                self.assertEqual(m.sha(root/'B'/row['path']),row['sha256'])
            with patch.dict(os.environ,{'PATH':'synthetic','USER':'operator'},clear=True),\
                 patch.object(m.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout='424242\n',stderr='')) as submit:
                guard['main'](str(ap))
                self.assertEqual(submit.call_count,1)
                argv=submit.call_args.args[0]
                self.assertEqual(argv[0],'sbatch');self.assertIn('--ntasks=20',argv)
                self.assertIn('--no-requeue',argv);self.assertIn('--time=1-00:00:00',argv)
                with self.assertRaises(ValueError):guard['main'](str(ap))
                self.assertEqual(submit.call_count,1)
            receipt=m.read(case/'submission.receipt.json')
            self.assertEqual(receipt['job_id'],'424242')
            self.assertEqual(receipt['state'],'SUBMITTED')

if __name__=='__main__':unittest.main(verbosity=2)
