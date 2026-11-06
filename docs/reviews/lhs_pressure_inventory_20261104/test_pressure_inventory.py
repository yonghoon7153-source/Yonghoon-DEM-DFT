"""Synthetic contract tests. No real ibb/WSL paths are opened."""
import ast
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
COMMAND = HERE / 'pressure_inventory.sh'
LEAK = 'DO_NOT_PRINT_947261.3386'


def load_module():
    shell = COMMAND.read_text()
    code = shell.split("-c '\n", 1)[1].split("\n' \"$@\"", 1)[0]
    ast.parse(code, feature_version=(3, 8))
    module = types.ModuleType('inventory_test_import')
    exec(compile(code, str(COMMAND), 'exec'), module.__dict__)
    return module


class InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_module()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.roots = {'base': self.base/'base', 'supp': self.base/'supp', 'local': self.base/'local'}
        for root in self.roots.values():
            root.mkdir()

    def layout(self, mode, content=None):
        if content is None:
            content = 'Current Pressure: 0.123 MPa (Target: 0.456)\n'
        for key, case in self.m.plan(mode):
            folder = self.roots[key]/case
            folder.mkdir(exist_ok=True)
            (folder/'log.liggghts').write_text(content)
            if mode == 'wsl':
                (folder/'log.txt').write_text(content)

    def invoke(self, mode):
        result = self.m.inventory(mode, self.roots)
        encoded = json.dumps(result)
        self.assertNotIn(LEAK, encoded)
        self.assertNotIn('Current Pressure:', encoded)
        return result

    def scan(self, folder, name='log.liggghts'):
        fd = os.open(str(folder), os.O_RDONLY|os.O_DIRECTORY)
        try:
            return self.m.scan_log(fd, name)
        finally:
            os.close(fd)

    def test_01_ibb_scope_184_and_wsl_scope_30(self):
        self.layout('ibb'); self.layout('wsl')
        for mode, count in [('ibb', 184), ('wsl', 30)]:
            report = self.invoke(mode)
            self.assertEqual(report['rc'], 0)
            self.assertEqual(len(report['cases']), count)
            self.assertEqual(report['expected_cases'], count)
            self.assertEqual(report['status'], 'INVENTORY_COMPLETE')
        names = [c for _, c in self.m.plan('ibb')]
        self.assertIn('lhs00_099', names); self.assertIn('lhss_020', names)
        self.assertNotIn('lhs00_100', names)

    def test_02_missing_root_directory_and_logs_fail_closed(self):
        self.layout('wsl')
        (self.roots['local']/'lhs00_100'/'log.txt').unlink()
        self.assertEqual(self.invoke('wsl')['rc'], 2)
        for f in (self.roots['local']/'lhs00_101').iterdir(): f.unlink()
        (self.roots['local']/'lhs00_101').rmdir()
        self.assertEqual(self.invoke('wsl')['rc'], 2)
        other = dict(self.roots, local=self.base/'missing')
        self.assertEqual(self.m.inventory('wsl', other)['rc'], 2)

    def test_03_empty_malformed_nan_are_counts_not_eligibility(self):
        folder = self.roots['local']
        (folder/'log.liggghts').write_text('')
        self.assertEqual(self.scan(folder)['b7_matches'], 0)
        (folder/'log.liggghts').write_text('Current Pressure: broken\nCurrent Pressure: NaN MPa (Target: inf)\n')
        got = self.scan(folder)
        self.assertEqual((got['b7_matches'], got['pressure_prefix_malformed']), (1, 1))
        self.assertEqual(got['status'], 'COUNTED')

    def test_04_exact_b7_regex_and_splitlines_semantics(self):
        text = ('Current Pressure: '+LEAK+' MPa (Target: text)\r\n'
                '\tCurrent Pressure: 1 MPa (Target: 2)\x85'
                'Current Pressure: 3 MPa (Target: 4)\u2028'
                'print "Current Pressure: ${current_press} MPa (Target: ${target_press})"\n'
                'Current Pressure: 5 MPa (Target: 6) trailing\n')
        (self.roots['local']/'log.liggghts').write_bytes(text.encode())
        got = self.scan(self.roots['local'])
        self.assertEqual(got['b7_matches'], 3)
        self.assertEqual(got['pressure_prefix_malformed'], 1)
        self.assertNotIn(LEAK, json.dumps(got))

    def test_05_duplicate_local_logs_are_kept_separate(self):
        self.layout('wsl')
        result = self.invoke('wsl'); row=result['cases'][0]
        self.assertEqual(row['logs_with_b7_matches'], 2)
        self.assertEqual(row['logs']['log.liggghts']['b7_matches'], 1)
        self.assertEqual(row['logs']['log.txt']['b7_matches'], 1)
        self.assertEqual(result['rc'], 0)

    def test_06_restart_echo_and_message_not_events(self):
        (self.roots['local']/'log.liggghts').write_text(
            'read_restart '+LEAK+'\nReading restart file '+LEAK+'\n'
            '# read_restart ignored\nprint "Reading restart file"\n')
        got = self.scan(self.roots['local'])
        self.assertEqual(got['read_restart_echo_lines'], 1)
        self.assertEqual(got['reading_restart_message_lines'], 1)
        self.assertNotIn('restart_events', got)

    def test_07_final_symlink_directory_and_fifo_refused(self):
        root=self.roots['local']; target=self.base/LEAK; target.write_text(LEAK)
        log=root/'log.liggghts'; log.symlink_to(target)
        self.assertEqual(self.scan(root)['status'], 'SYMLINK')
        log.unlink(); log.mkdir()
        self.assertEqual(self.scan(root)['status'], 'NONREGULAR')
        log.rmdir(); os.mkfifo(str(log))
        self.assertEqual(self.scan(root)['status'], 'NONREGULAR')

    def test_08_case_and_out_directory_symlinks_refused(self):
        self.layout('wsl'); folder=self.roots['local']/'lhs00_100'
        (folder/'logs').symlink_to(self.base, target_is_directory=True)
        self.assertEqual(self.invoke('wsl')['rc'], 2)
        (folder/'logs').unlink()
        for f in folder.iterdir(): f.unlink()
        folder.rmdir(); folder.symlink_to(self.base, target_is_directory=True)
        self.assertEqual(self.invoke('wsl')['rc'], 2)

    def test_09_hostile_out_filename_count_only(self):
        self.layout('ibb'); folder=self.roots['base']/'lhs00_000'/'logs'; folder.mkdir()
        (folder/(LEAK+'\n.out')).write_text(LEAK)
        shared=self.roots['base']/'logs'; shared.mkdir()
        (shared/('output_lhs00_000_'+LEAK+'.out')).write_text(LEAK)
        row=self.invoke('ibb')['cases'][0]
        self.assertEqual(row['case_out']['regular_files'], 1)
        self.assertEqual(row['root_out']['regular_files'], 1)

    def test_10_out_symlink_refused_without_name(self):
        self.layout('wsl'); folder=self.roots['local']/'lhs00_100'/'logs'; folder.mkdir()
        (folder/(LEAK+'.out')).symlink_to(self.base/'missing')
        self.assertEqual(self.invoke('wsl')['rc'], 2)

    def test_11_unreadable_exception_never_leaks(self):
        (self.roots['local']/'log.liggghts').write_text(LEAK)
        fd=os.open(str(self.roots['local']),os.O_RDONLY|os.O_DIRECTORY)
        try:
            with mock.patch.object(self.m.os, 'open', side_effect=PermissionError(LEAK)) as denied:
                got=self.m.scan_log(fd, 'log.liggghts')
                denied.assert_called_once()
                self.assertEqual(denied.call_args.kwargs['dir_fd'],fd)
        finally:
            os.close(fd)
        self.assertEqual(got['status'], 'UNREADABLE')
        self.assertNotIn(LEAK, json.dumps(got))

    def test_12_changed_during_read_discards_counts(self):
        root=self.roots['local']; log=root/'log.liggghts'; log.write_text('Current Pressure: 1 MPa (Target: 2)\n')
        original=self.m.count_text
        def alter(stream):
            result=original(stream)
            with log.open('a') as f: f.write(LEAK)
            return result
        with mock.patch.object(self.m, 'count_text', side_effect=alter): got=self.scan(root)
        self.assertEqual(got['status'], 'CHANGED')
        self.assertNotIn('b7_matches', got)

    def test_13_replacement_after_open_refused(self):
        root=self.roots['local']; log=root/'log.liggghts'; log.write_text('')
        original=self.m.count_text
        def replace(stream):
            result=original(stream); log.unlink(); log.write_text(LEAK); return result
        with mock.patch.object(self.m, 'count_text', side_effect=replace): got=self.scan(root)
        self.assertEqual(got['status'], 'CHANGED')

    def test_14_guard_uses_actual_account_host_kernel(self):
        for identity, mode in [
            (('Linux','ibb-master','generic','yonghoon',1000,1000),'ibb'),
            (('Linux','desktop','microsoft-standard-WSL2','yonghoon71',1000,1000),'wsl')]:
            self.assertTrue(self.m.identity_allowed(mode, identity))
        for identity, mode in [
            (('Linux','ibb','generic','yonghoon',1000,1000),'ibb'),
            (('Linux','ibb-master','generic','wrong',1000,1000),'ibb'),
            (('Linux','desktop','generic','yonghoon71',1000,1000),'wsl'),
            (('Linux','ibb-master','generic','yonghoon',0,1000),'ibb')]:
            self.assertFalse(self.m.identity_allowed(mode, identity))

    def test_15_cli_no_root_override_or_error_leak(self):
        for argv in [[], ['ibb', '--root', LEAK], [LEAK]]:
            out=io.StringIO()
            with contextlib.redirect_stdout(out): rc=self.m.main(argv)
            self.assertEqual(rc, 2); self.assertNotIn(LEAK,out.getvalue())
        with mock.patch.object(self.m,'runtime_identity',return_value=('Linux',LEAK,'generic',LEAK,1000,1000)):
            out=io.StringIO()
            with contextlib.redirect_stdout(out): rc=self.m.main(['ibb'])
        self.assertEqual(rc,2); self.assertNotIn(LEAK,out.getvalue())

    def test_16_home_lustre_alias_policy(self):
        self.assertTrue(self.m.root_alias_allowed('/home/yonghoon/dem_test/lhs','/lustre/home/yonghoon/dem_test/lhs'))
        self.assertTrue(self.m.root_alias_allowed('/home/yonghoon/lhs_supp_20261006','/lustre/home/yonghoon/lhs_supp_20261006'))
        self.assertFalse(self.m.root_alias_allowed('/home/yonghoon/dem_test/lhs','/tmp/'+LEAK))
        self.assertFalse(self.m.root_alias_allowed('/home/yonghoon/dem_test/lhs','/lustre/home/other/dem_test/lhs'))
        self.assertFalse(self.m.root_alias_allowed('/home/yonghoon71/lhs_local','/lustre/home/yonghoon71/lhs_local'))

    def test_17_no_explicit_writes_or_external_processes(self):
        self.layout('wsl')
        before={str(p.relative_to(self.base)):(p.stat().st_size,p.stat().st_mtime_ns,p.read_bytes()) for p in self.base.rglob('*') if p.is_file()}
        observed=[]; active=[True]
        def audit(event,args):
            if not active[0]: return
            if event=='open':
                flags=args[2]
                if isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND): observed.append(event)
            if event in ('os.mkdir','os.remove','os.rename','os.rmdir','os.symlink','subprocess.Popen','os.system'): observed.append(event)
        sys.addaudithook(audit)
        try: self.assertEqual(self.invoke('wsl')['rc'],0)
        finally: active[0]=False
        after={str(p.relative_to(self.base)):(p.stat().st_size,p.stat().st_mtime_ns,p.read_bytes()) for p in self.base.rglob('*') if p.is_file()}
        self.assertEqual(before,after); self.assertEqual(observed,[])

    def test_18_long_line_refuses_without_payload(self):
        (self.roots['local']/'log.liggghts').write_text(LEAK+'x'*(self.m.MAX_LINE+1))
        got=self.scan(self.roots['local'])
        self.assertEqual(got['status'],'LIMIT'); self.assertNotIn(LEAK,json.dumps(got))

    def test_19_shell_syntax_and_wrong_host_run(self):
        self.assertEqual(subprocess.run(['sh','-n',str(COMMAND)],capture_output=True).returncode,0)
        p=subprocess.run(['sh',str(COMMAND),'ibb'],capture_output=True,text=True)
        self.assertEqual(p.returncode,2); self.assertEqual(p.stderr,'')
        self.assertEqual(json.loads(p.stdout)['status'],'NOT_ESTABLISHED')

    def test_20_growing_stream_has_a_total_read_bound(self):
        with mock.patch.object(self.m,'MAX_LOG_BYTES',8):
            with self.assertRaises(self.m.Refusal):
                self.m.count_text(io.StringIO('a\n'*6))


if __name__=='__main__': unittest.main(verbosity=2)
