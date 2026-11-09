#!/usr/bin/env python3
"""Windows namespace rejection on disposable local copies; no host/device I/O.

The earlier implementation-window CLI harness is loaded from exact source only
to reuse its copy/graph/allowed-Python boundary. No attached reviewer probe is
executed. Extended local paths use real CLI; UNC/device policy checks stop every
filesystem operation with sentinels before it could inspect the supplied token.
"""
import argparse
from contextlib import ExitStack
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest import mock

BASE_TEST_SHA = 'a6f57d19a92e7c91975feac67cd8e76f07b0deff7568b8e8a9e5c62b0b27d9b3'
BASE_PATH = Path(__file__).parents[1] / 'mixer_inactive_path_fix_20261109/test_evidence_boundary.py'
BASE_RAW = BASE_PATH.read_bytes()
if hashlib.sha256(BASE_RAW).hexdigest() != BASE_TEST_SHA:
    raise ValueError('fixed previous harness bytes required')
base = types.ModuleType('mipr01_verified_test_support')
base.__file__ = str(BASE_PATH)
exec(compile(BASE_RAW, str(BASE_PATH), 'exec'), base.__dict__)
REASON = 'unsupported Windows namespace path'
BACKSLASH = chr(92)


def extended(path):
    return Path(BACKSLASH*2 + '?' + BACKSLASH + str(path.absolute()))


class WindowsBoundary(base.EvidenceBoundary):
    @classmethod
    def setUpClass(cls):
        if os.name != 'nt':
            raise ValueError('this actual-CLI regression requires Windows')
        super().setUpClass()
        cls.prewrite_observations = []

    def cli(self, label, mode, candidate, evidence, snapshot_argument=None):
        self.assertEqual(base.graph(self.tool), self.tool_graph)
        snapshot = self.snapshot if snapshot_argument is None else snapshot_argument
        command = [sys.executable, '-I', '-B', '-X', 'utf8', str(self.verifier),
                   '--mode', mode, '--snapshot', str(snapshot),
                   '--candidate', str(candidate), '--evidence', str(evidence)]
        self.boundary['expected_argv'] = command
        try:
            result = subprocess.run(command, executable=sys.executable, cwd=self.work,
                                    capture_output=True, timeout=60, check=False)
        finally:
            self.boundary['expected_argv'] = None
        (self.work / 'logs' / (label + '.stdout')).write_bytes(result.stdout)
        (self.work / 'logs' / (label + '.stderr')).write_bytes(result.stderr)
        return result

    def test_01_supported_sibling_modes_preserved(self):
        for mode in base.MODES:
            with self.subTest(mode=mode):
                self.normal_case(mode)

    def test_02_supported_local_casefold_dotdot_and_relative(self):
        for spelling in ('casefold', 'dotdot', 'relative'):
            with self.subTest(spelling=spelling):
                root = self.case_root('supported_' + spelling)
                candidate = root / 'candidate'
                evidence = root / 'candidate_sibling'
                base.copy_tree(self.candidate_source, candidate)
                before = base.graph(candidate)
                candidate_arg, evidence_arg, snapshot_arg = candidate, evidence, self.snapshot
                if spelling == 'casefold':
                    candidate_arg = Path(str(candidate).upper())
                elif spelling == 'dotdot':
                    (root / 'route').mkdir()
                    candidate_arg = root / 'route' / '..' / 'candidate'
                    evidence_arg = root / 'route' / '..' / 'candidate_sibling'
                else:
                    candidate_arg = candidate.relative_to(self.work)
                    evidence_arg = evidence.relative_to(self.work)
                    snapshot_arg = Path('snapshot')
                result = self.cli('supported_' + spelling, 'verify', candidate_arg, evidence_arg, snapshot_arg)
                after = base.graph(candidate)
                row = dict(case='supported_' + spelling, rc=result.returncode,
                           candidate_files_before=base.files_count(before), candidate_files_after=base.files_count(after),
                           candidate_graph_unchanged=before == after, inputs_preserved=self.preserved_inputs())
                self.observations.append(row)
                self.assertEqual(result.returncode, 0, row)
                self.assertEqual(before, after, row)
                self.assertTrue(row['inputs_preserved'], row)

    def test_03_extended_candidate_and_evidence_rejected_all_modes(self):
        for mode in base.MODES:
            for relation in ('equal', 'child', 'ancestor'):
                for side in ('candidate', 'evidence'):
                    label = 'extended_' + mode + '_' + relation + '_' + side
                    with self.subTest(mode=mode, relation=relation, side=side):
                        root = self.case_root(label)
                        parts = ('container', 'candidate') if relation == 'ancestor' else ('candidate',)
                        candidate = root.joinpath(*parts)
                        if mode != 'build':
                            base.copy_tree(self.candidate_source, candidate)
                        evidence = (candidate / 'new_evidence' if relation == 'child'
                                    else candidate.parent if relation == 'ancestor' else candidate)
                        candidate_arg = extended(candidate) if side == 'candidate' else candidate
                        evidence_arg = extended(evidence) if side == 'evidence' else evidence
                        before, candidate_before = base.graph(root), base.graph(candidate)
                        result = self.cli(label, mode, candidate_arg, evidence_arg)
                        after, candidate_after = base.graph(root), base.graph(candidate)
                        row = dict(case=label, mode=mode, relation=relation, extended_side=side,
                                   rc=result.returncode, namespace_reason=REASON.encode() in result.stderr,
                                   candidate_files_before=base.files_count(candidate_before),
                                   candidate_files_after=base.files_count(candidate_after),
                                   fixture_graph_before_sha256=base.graph_hash(before),
                                   fixture_graph_after_sha256=base.graph_hash(after),
                                   fixture_graph_unchanged=before == after,
                                   added_paths=sorted(set(after)-set(before)),
                                   removed_paths=sorted(set(before)-set(after)),
                                   changed_paths=sorted(p for p in set(before)&set(after) if before[p] != after[p]),
                                   inputs_preserved=self.preserved_inputs())
                        if mode == 'verify' and relation == 'child':
                            recheck = self.cli(label + '_recheck', 'verify', candidate,
                                               self.work / 'rechecks' / side)
                            row.update(recheck_rc=recheck.returncode,
                                       recheck_exact_file_set_refusal=b'exact candidate bundle file set' in recheck.stderr,
                                       candidate_files_after_recheck=base.files_count(base.graph(candidate)))
                        self.observations.append(row)
                        self.assertNotEqual(result.returncode, 0, row)
                        self.assertTrue(row['namespace_reason'], row)
                        self.assertEqual(before, after, row)
                        self.assertTrue(row['inputs_preserved'], row)
                        if 'recheck_rc' in row:
                            self.assertEqual(row['recheck_rc'], 0, row)

    def test_04_extended_snapshot_rejected_before_output_all_modes(self):
        for mode in base.MODES:
            with self.subTest(mode=mode):
                label = 'extended_snapshot_' + mode
                root = self.case_root(label)
                candidate, evidence = root / 'candidate', root / 'evidence'
                if mode != 'build':
                    base.copy_tree(self.candidate_source, candidate)
                before = base.graph(root)
                result = self.cli(label, mode, candidate, evidence, extended(self.snapshot))
                after = base.graph(root)
                row = dict(case=label, mode=mode, rc=result.returncode,
                           namespace_reason=REASON.encode() in result.stderr,
                           fixture_graph_unchanged=before == after,
                           evidence_created=evidence.exists(), inputs_preserved=self.preserved_inputs())
                self.observations.append(row)
                self.assertNotEqual(result.returncode, 0, row)
                self.assertTrue(row['namespace_reason'], row)
                self.assertEqual(before, after, row)
                self.assertFalse(evidence.exists(), row)
                self.assertTrue(row['inputs_preserved'], row)

    def test_05_unsupported_raw_namespace_never_touches_filesystem(self):
        verifier = types.ModuleType('mipr01_prewrite_verifier')
        verifier.__file__ = str(self.verifier)
        exec(compile(self.original_source_bytes, str(self.verifier), 'exec'), verifier.__dict__)
        # Synthetic lexical tokens only; no token is resolved or sent to an OS
        # API. Ordinary local extended aliases are separately exercised by CLI.
        b = BACKSLASH
        local = self.work.drive + b + 'SYNTHETIC_LOCAL_TOKEN'
        unc = b*2 + 'SYNTHETIC_HOST' + b + 'SYNTHETIC_SHARE'
        extended_local = b*2 + '?' + b + local
        tokens = {
            'extended_dos': extended_local,
            'device_dos': b*2 + '.' + b + local,
            'unc': unc,
            'extended_unc': b*2 + '?' + b + 'UNC' + b + 'SYNTHETIC_HOST' + b + 'SYNTHETIC_SHARE',
            'nt_namespace': b + '??' + b + local,
            'forward_extended': extended_local.replace(b, '/'),
            'forward_unc': unc.replace(b, '/'),
            'mixed_leading': b + '/' + '?' + b + local,
            'triple_leading': b*3 + 'SYNTHETIC_NAMESPACE',
            'forward_nt': '/' + '??' + '/' + local.replace(b, '/'),
        }
        for mode in base.MODES:
            for argument in ('snapshot', 'candidate', 'evidence'):
                for label, token in tokens.items():
                    with self.subTest(mode=mode, argument=argument, namespace=label):
                        touched = []

                        def blocked(operation):
                            def fail(*args, **kwargs):
                                touched.append(operation)
                                raise RuntimeError('FILESYSTEM_SENTINEL:' + operation)
                            return fail

                        args = dict(snapshot='SYNTHETIC_SNAPSHOT', candidate='SYNTHETIC_CANDIDATE',
                                    evidence='SYNTHETIC_EVIDENCE')
                        args[argument] = token
                        argv = ['verify_inactive.py', '--mode', mode]
                        for key, value in args.items():
                            argv.extend(['--' + key, value])
                        exception_name, message = None, None
                        with ExitStack() as stack:
                            stack.enter_context(mock.patch.object(sys, 'argv', argv))
                            for operation in ('absolute', 'resolve', 'exists', 'lstat', 'stat', 'is_symlink',
                                              'is_file', 'is_dir', 'mkdir', 'read_bytes'):
                                stack.enter_context(mock.patch.object(Path, operation, blocked(operation)))
                            stack.enter_context(mock.patch.object(verifier, 'reject_link_ancestors', blocked('link_check')))
                            stack.enter_context(mock.patch.object(verifier, 'install_boundary', blocked('install_boundary')))
                            try:
                                verifier.main()
                            except (ValueError, RuntimeError) as exc:
                                exception_name, message = type(exc).__name__, str(exc)
                        row = dict(mode=mode, argument=argument, namespace=label,
                                   exception=exception_name, namespace_reason=message == REASON,
                                   filesystem_calls_attempted=touched)
                        self.prewrite_observations.append(row)
                        self.assertEqual(message, REASON, row)
                        self.assertEqual(touched, [], row)
        self.assertTrue(self.preserved_inputs())


TEST_NAMES = (
    'test_01_supported_sibling_modes_preserved',
    'test_02_supported_local_casefold_dotdot_and_relative',
    'test_03_extended_candidate_and_evidence_rejected_all_modes',
    'test_04_extended_snapshot_rejected_before_output_all_modes',
    'test_05_unsupported_raw_namespace_never_touches_filesystem',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifier', type=Path, required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--candidate-source', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True, help='new scratch evidence directory')
    base.OPTIONS = parser.parse_args()
    test_raw = Path(__file__).read_bytes()
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(
        unittest.TestSuite(WindowsBoundary(name) for name in TEST_NAMES))
    cls = WindowsBoundary
    report = dict(schema='mipr01_windows_namespace_regression/1',
                  methods=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                  rc=0 if result.wasSuccessful() else 1, test_sha256=base.sha(test_raw),
                  reused_harness_sha256=BASE_TEST_SHA, verifier_sha256=base.sha(cls.original_source_bytes),
                  inventory_sha256=base.sha(cls.original_inventory_bytes),
                  python_executable_sha256=base.sha(Path(sys.executable).read_bytes()),
                  snapshot_files=86, original_candidate_files=43,
                  snapshot_reference_graph=cls.original_snapshot_graph,
                  candidate_reference_graph=cls.original_candidate_graph,
                  observations=cls.observations, prewrite_observations=cls.prewrite_observations,
                  allowed_local_python_cli_calls=cls.boundary['calls'],
                  denied_unexpected_process_or_network=cls.boundary['rejected'],
                  original_inputs_preserved=WindowsBoundary().preserved_inputs(),
                  actual_unc_device_or_host_access=False, actual_links_created=False,
                  prewrite_scope='Filesystem APIs replaced by stop sentinels; no actual UNC/device probing',
                  simulator_calls=0, scheduler_calls=0, mpi_calls=0, research_results=0,
                  execution_authorized=False, operational_activation=False, whole_gate='HOLD')
    (cls.work / 'report.json').write_bytes(base.encode(report))
    (cls.work / 'tested_test_source.py').write_bytes(test_raw)
    (cls.work / 'reused_harness_source.py').write_bytes(BASE_RAW)
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('snapshot_reference_graph', 'candidate_reference_graph',
                                   'observations', 'prewrite_observations')}))
    return report['rc']


if __name__ == '__main__':
    raise SystemExit(main())
