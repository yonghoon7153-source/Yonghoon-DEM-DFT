#!/usr/bin/env python3
"""Local CLI regression for candidate/evidence separation; no engine or host.

Only the explicitly supplied verifier, copied and byte-checked, is launched with
this Python executable. Its existing child audit boundary blocks further process
and network use before scientific modules load. Inputs and every test copy remain
preserved; this harness never deletes a tree or runs an attached probe.
"""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import unittest

OPTIONS = None
MODES = ('old', 'build', 'verify', 'preparation-tests')
REASON = b'candidate and evidence directories disjoint'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8')


def graph(root):
    if not root.exists():
        return None
    result = {}
    for path in (root, *sorted(root.rglob('*'))):
        info = path.lstat()
        if path.is_symlink() or getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
            raise ValueError('test inputs must have no links/reparse points')
        relative = path.relative_to(root).as_posix()
        if path.is_dir():
            result[relative] = dict(kind='directory')
        elif path.is_file():
            raw = path.read_bytes()
            result[relative] = dict(kind='file', bytes=len(raw), sha256=sha(raw))
        else:
            raise ValueError('test inputs must contain regular files/directories')
    return result


def files_count(state):
    return sum(row['kind'] == 'file' for row in (state or {}).values())


def graph_hash(state):
    return sha(encode(state))


def copy_tree(source, target):
    expected = graph(source)
    if target.exists() or expected is None:
        raise ValueError('new copy target and existing source required')
    target.mkdir(parents=True)
    for path, entry in expected.items():
        dest = target / path
        if entry['kind'] == 'directory':
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open('xb') as handle:
                handle.write((source / path).read_bytes())
    if graph(target) != expected:
        raise ValueError('copy bytes/directory graph differs')


def install_parent_process_boundary():
    state = dict(expected_argv=None, calls=0, rejected=[])
    executable = Path(sys.executable).resolve(strict=True)

    def audit(event, args):
        if event == 'subprocess.Popen':
            supplied_executable, argv = args[:2]
            expected = state['expected_argv']
            command_matches = expected is not None and (
                argv == subprocess.list2cmdline(expected) if isinstance(argv, str) else list(argv) == expected)
            if (not command_matches
                    or Path(supplied_executable).resolve(strict=True) != executable):
                state['rejected'].append(event)
                raise RuntimeError('only declared local verifier Python invocation is allowed')
            state['calls'] += 1
        elif (event.startswith('socket.') or event.startswith(('os.exec', 'os.spawn', 'os.posix_spawn'))
              or event in ('os.system', 'os.startfile', 'os.fork', 'os.forkpty')):
            state['rejected'].append(event)
            raise RuntimeError('parent test boundary denies other process/network use')

    sys.addaudithook(audit)
    return state


class EvidenceBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = OPTIONS.work.absolute()
        if cls.work.exists():
            raise ValueError('preserve previous evidence: --work must not exist')
        cls.verifier_source = OPTIONS.verifier.resolve(strict=True)
        cls.snapshot_source = OPTIONS.snapshot.resolve(strict=True)
        cls.candidate_source = OPTIONS.candidate_source.resolve(strict=True)
        cls.inventory_source = cls.verifier_source.with_name('source_inventory.json')
        cls.original_source_bytes = cls.verifier_source.read_bytes()
        cls.original_inventory_bytes = cls.inventory_source.read_bytes()
        cls.original_snapshot_graph = graph(cls.snapshot_source)
        cls.original_candidate_graph = graph(cls.candidate_source)
        if files_count(cls.original_snapshot_graph) != 86 or files_count(cls.original_candidate_graph) != 43:
            raise ValueError('expected fixed snapshot86 and candidate43')
        cls.work.mkdir(parents=True)
        cls.tool = cls.work / 'tool'
        cls.tool.mkdir()
        cls.verifier = cls.tool / 'verify_inactive.py'
        cls.verifier.write_bytes(cls.original_source_bytes)
        (cls.tool / 'source_inventory.json').write_bytes(cls.original_inventory_bytes)
        cls.tool_graph = graph(cls.tool)
        cls.snapshot = cls.work / 'snapshot'
        copy_tree(cls.snapshot_source, cls.snapshot)
        cls.snapshot_graph = graph(cls.snapshot)
        (cls.work / 'cases').mkdir()
        (cls.work / 'logs').mkdir()
        (cls.work / 'rechecks').mkdir()
        cls.observations = []
        cls.boundary = install_parent_process_boundary()

    def preserved_inputs(self):
        return (self.verifier_source.read_bytes() == self.original_source_bytes
                and self.inventory_source.read_bytes() == self.original_inventory_bytes
                and graph(self.snapshot_source) == self.original_snapshot_graph
                and graph(self.candidate_source) == self.original_candidate_graph
                and graph(self.tool) == self.tool_graph
                and graph(self.snapshot) == self.snapshot_graph)

    def case_root(self, label):
        root = self.work / 'cases' / label
        root.mkdir()
        return root

    def cli(self, label, mode, candidate, evidence):
        self.assertEqual(graph(self.tool), self.tool_graph)
        command = [sys.executable, '-I', '-B', '-X', 'utf8', str(self.verifier),
                   '--mode', mode, '--snapshot', str(self.snapshot),
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

    def normal_case(self, mode):
        root = self.case_root('sibling_' + mode)
        candidate, evidence = root / 'candidate', root / 'evidence'
        if mode != 'build':
            copy_tree(self.candidate_source, candidate)
        before = graph(candidate)
        result = self.cli('sibling_' + mode, mode, candidate, evidence)
        after = graph(candidate)
        report_path = evidence / 'report.json'
        report = json.loads(report_path.read_bytes()) if report_path.is_file() else None
        row = dict(case='sibling_' + mode, mode=mode, rc=result.returncode,
                   candidate_files_before=files_count(before), candidate_files_after=files_count(after),
                   candidate_graph_before_sha256=graph_hash(before), candidate_graph_after_sha256=graph_hash(after),
                   inputs_preserved=self.preserved_inputs(), report=report)
        self.observations.append(row)
        self.assertEqual(result.returncode, 1 if mode == 'old' else 0)
        self.assertTrue(row['inputs_preserved'])
        self.assertEqual(after, self.original_candidate_graph)
        self.assertIsNotNone(report)
        if mode == 'old':
            self.assertEqual((report['methods'], report['failures'], report['errors']), (1, 8, 0))
            self.assertIn(b'metadata differs from the fixed case recipe', result.stdout)
        elif mode == 'preparation-tests':
            self.assertEqual((report['methods'], report['failures'], report['errors']), (14, 0, 0))
        else:
            self.assertEqual(report['candidate_bundle_files'], 43)
        if mode != 'build':
            self.assertEqual(before, after)

    def test_01_sibling_verify_preserves_all_candidate_bytes_and_directories(self):
        self.normal_case('verify')

    def test_02_sibling_build_makes_a_new_identical_inactive_copy(self):
        self.normal_case('build')

    def test_03_sibling_old_mode_rc1_is_only_the_expected_metadata_baseline(self):
        self.normal_case('old')

    def test_04_sibling_preparation_tests_keep_inputs_unchanged(self):
        self.normal_case('preparation-tests')

    def test_05_all_modes_reject_overlap_before_any_filesystem_mutation(self):
        for mode in MODES:
            for relation in ('equal', 'child', 'ancestor'):
                for spelling in ('direct', 'evidence_dotdot', 'candidate_dotdot'):
                    label = mode + '_' + relation + '_' + spelling
                    with self.subTest(mode=mode, relation=relation, spelling=spelling):
                        root = self.case_root(label)
                        parts = ('container', 'candidate') if relation == 'ancestor' else ('candidate',)
                        canonical_candidate = root.joinpath(*parts)
                        if mode != 'build':
                            copy_tree(self.candidate_source, canonical_candidate)
                        canonical_evidence = (canonical_candidate / 'new_evidence' if relation == 'child'
                                              else canonical_candidate.parent if relation == 'ancestor'
                                              else canonical_candidate)
                        candidate, evidence = canonical_candidate, canonical_evidence
                        if spelling != 'direct':
                            (root / 'route').mkdir()
                        if spelling == 'evidence_dotdot':
                            evidence = root / 'route' / '..' / canonical_evidence.relative_to(root)
                        elif spelling == 'candidate_dotdot':
                            candidate = root / 'route' / '..' / canonical_candidate.relative_to(root)
                        before = graph(root)
                        before_candidate = graph(canonical_candidate)
                        evidence_existed = canonical_evidence.exists()
                        result = self.cli(label, mode, candidate, evidence)
                        after = graph(root)
                        after_candidate = graph(canonical_candidate)
                        before_paths, after_paths = set(before), set(after)
                        row = dict(case=label, mode=mode, relation=relation, spelling=spelling,
                                   rc=result.returncode, expected_rejection_reason=REASON in result.stderr,
                                   evidence_existed_before=evidence_existed,
                                   evidence_exists_after=canonical_evidence.exists(),
                                   candidate_files_before=files_count(before_candidate),
                                   candidate_files_after=files_count(after_candidate),
                                   fixture_graph_before_sha256=graph_hash(before),
                                   fixture_graph_after_sha256=graph_hash(after),
                                   fixture_graph_unchanged=before == after,
                                   added_paths=sorted(after_paths-before_paths),
                                   removed_paths=sorted(before_paths-after_paths),
                                   changed_paths=sorted(p for p in before_paths & after_paths if before[p] != after[p]),
                                   inputs_preserved=self.preserved_inputs())
                        if mode == 'verify' and relation == 'child' and spelling == 'direct':
                            recheck = self.cli(label + '_recheck', 'verify', canonical_candidate,
                                               self.work / 'rechecks' / 'internal_evidence_case')
                            row.update(recheck_rc=recheck.returncode,
                                       recheck_exact_file_set_refusal=b'exact candidate bundle file set' in recheck.stderr,
                                       candidate_files_after_recheck=files_count(graph(canonical_candidate)))
                        self.observations.append(row)
                        self.assertNotEqual(result.returncode, 0, row)
                        self.assertTrue(row['expected_rejection_reason'], row)
                        self.assertEqual(after, before, row)
                        self.assertEqual(canonical_evidence.exists(), evidence_existed, row)
                        self.assertTrue(row['inputs_preserved'], row)
                        if 'recheck_rc' in row:
                            self.assertEqual(row['recheck_rc'], 0, row)


def main():
    global OPTIONS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifier', type=Path, required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--candidate-source', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True, help='new external evidence directory only')
    OPTIONS = parser.parse_args()
    test_raw = Path(__file__).read_bytes()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EvidenceBoundary)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    cls = EvidenceBoundary
    report = dict(schema='mip01_candidate_evidence_cli_regression/1',
                  methods=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                  rc=0 if result.wasSuccessful() else 1,
                  test_sha256=sha(test_raw), verifier_sha256=sha(cls.original_source_bytes),
                  inventory_sha256=sha(cls.original_inventory_bytes),
                  python_executable_sha256=sha(Path(sys.executable).read_bytes()),
                  snapshot_files=86, original_candidate_files=43,
                  snapshot_reference_graph=cls.original_snapshot_graph,
                  candidate_reference_graph=cls.original_candidate_graph,
                  observations=cls.observations,
                  allowed_local_python_cli_calls=cls.boundary['calls'],
                  denied_unexpected_process_or_network=cls.boundary['rejected'],
                  original_inputs_preserved=EvidenceBoundary().preserved_inputs(),
                  scope='Synthetic local CLI only; no actual symlink/junction creation or security certification',
                  simulator_calls=0, scheduler_calls=0, mpi_calls=0, research_results=0,
                  execution_authorized=False, operational_activation=False, whole_gate='HOLD')
    (cls.work / 'report.json').write_bytes(encode(report))
    (cls.work / 'tested_test_source.py').write_bytes(test_raw)
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('snapshot_reference_graph', 'candidate_reference_graph', 'observations')}))
    return report['rc']


if __name__ == '__main__':
    raise SystemExit(main())
