#!/usr/bin/env python3
"""Fixed offline copy preparation; never an operating seal, launcher or GO.

Input: a separately exported, hash-bound snapshot of twelve dependencies, the
current launch 73 and the unchanged preparation test. No Git, child process,
socket, scheduler, simulator, actual run data or host qualification is used here.
"""
import argparse
import copy
import hashlib
import importlib
import importlib.abc
import importlib.util
import json
import os
from pathlib import Path
import platform
import stat
import sys
import unittest

BASE = 'e48e5fa0498ab7ee8fd84163d9af024d07cbb135'
OLD = '527e244e4ebd6f0cb04c6cfb2ff5f3a52fb01996'
ACCEPTED = '69b6bec7ac20343dd884f8d5fa63e8bf45e7df97'
RECEIPT = 'e6000405b7625acf8c2c0a393571b116479e0e97'
LAUNCH = 'docs/reviews/mixer_first8_launch_preparation_20261106'
TEST = 'scripts/test_mixer_precal_prepare.py'
DEPENDENCIES = (
    'scripts/mixer_precal_prepare.py', 'scripts/mixer_precal_observe.py',
    'scripts/mixer_contact_reader.py', 'scripts/measure_mixing_index.py',
    'scripts/measure_bed_aspect.py', 'scripts/make_mixer_deck.py',
    'scripts/mixer_deck_readback.py', 'scripts/mixer_deck_diff.py',
    'scripts/make_mixer_resume.py', 'dem_scripts/mixer_20260919/Drum.stl',
    'dem_scripts/mixer_20260919/Front.stl', 'dem_scripts/mixer_20260919/Back.stl')


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def install_boundary(write_roots):
    roots = [p.resolve() for p in write_roots]
    denied = []

    def allowed(path):
        target = Path(path).resolve()
        return any(target == root or root in target.parents for root in roots)

    def audit(event, args):
        if (event.startswith('subprocess.') or event.startswith('socket.')
                or event in ('os.system', 'os.startfile', 'os.startfile/2', 'os.fork', 'os.forkpty')
                or event.startswith(('os.exec', 'os.spawn', 'os.posix_spawn'))):
            denied.append(event)
            raise RuntimeError('offline boundary denies ' + event)
        if event == 'open':
            path, mode, flags = args
            writing = isinstance(mode, str) and any(c in mode for c in 'wax+')
            writing = writing or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if writing and not isinstance(path, int) and not allowed(path):
                raise RuntimeError('write outside new candidate/evidence boundary')
        if event in ('os.mkdir', 'os.remove', 'os.rmdir') and not allowed(args[0]):
            raise RuntimeError('filesystem mutation outside new candidate/evidence boundary')
        if event in ('os.rename', 'os.link', 'os.symlink'):
            raise RuntimeError('rename/link forbidden by offline boundary')

    sys.addaudithook(audit)
    # Synthetic audit events only: no real Popen/socket call is made.
    for event in ('subprocess.Popen', 'socket.connect'):
        try:
            sys.audit(event, 'synthetic-boundary-probe')
        except RuntimeError:
            pass
        else:
            raise AssertionError('audit denial absent')
    return denied


def inventory_rows(inventory):
    need(inventory['base_b'] == BASE and inventory['original_asset_generation_pin'] == OLD
         and inventory['accepted_validation_source_pin'] == ACCEPTED
         and inventory['original_launch_reference_pin'] == RECEIPT, 'fixed source provenance')
    rows = inventory['source_dependencies']
    need([r['path'] for r in rows] == list(DEPENDENCIES), 'bounded twelve dependency paths')
    launch = inventory['launch_snapshot']
    need(len(launch) == 73 and len({r['path'] for r in launch}) == 73, 'launch seventy-three paths')
    need(all(r['path'].startswith(LAUNCH + '/') and '..' not in r['path'].split('/') for r in launch),
         'bounded launch paths')
    need(inventory['preparation_test']['path'] == TEST, 'fixed preparation test')
    return rows + launch + [inventory['preparation_test']]


def check_snapshot(raws, rows):
    need(set(raws) == {r['path'] for r in rows}, 'complete snapshot paths')
    for row in rows:
        raw = raws[row['path']]
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'snapshot SHA256: ' + row['path'])
        oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        need(oid == row['git_blob'], 'snapshot Git blob: ' + row['path'])


def reject_link_ancestors(path):
    """Reject lexical symlink/junction components before resolve erases their identity."""
    for part in (path, *path.parents):
        need(not part.is_symlink(), 'snapshot/output link ancestor')
        try:
            attributes = getattr(part.lstat(), 'st_file_attributes', 0)
        except FileNotFoundError:
            continue
        need(not attributes & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0),
             'snapshot/output reparse link ancestor')


def reject_unsupported_namespace(path):
    """Reject namespace spellings, without stripping prefixes or querying them."""
    spelling = os.fspath(path).replace('/', '\\')
    need(not spelling.startswith(('\\\\', '\\??\\')), 'unsupported Windows namespace path')


def snapshot_bytes(root, rows):
    reject_link_ancestors(root)
    need(root.is_dir(), 'regular snapshot directory')
    expected_files = {row['path'] for row in rows}
    expected_dirs = {parent.as_posix() for path in expected_files
                     for parent in Path(path).parents if parent.as_posix() != '.'}
    observed_files = set()
    for path in root.rglob('*'):
        reject_link_ancestors(path)
        relative = path.relative_to(root).as_posix()
        if path.is_dir():
            need(relative in expected_dirs, 'snapshot directory graph contains extra path')
        else:
            need(path.is_file(), 'snapshot graph contains nonregular path')
            observed_files.add(relative)
    need(observed_files == expected_files, 'snapshot file graph is not exact')
    result = {}
    for row in rows:
        p = root / row['path']
        need(p.is_file() and not p.is_symlink(), 'regular snapshot file: ' + row['path'])
        need(root in p.resolve().parents, 'snapshot file containment')
        result[row['path']] = p.read_bytes()
    check_snapshot(result, rows)
    return result


class VerifiedSourceFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Compile only already hash-checked source bytes; never consult a pyc cache."""
    def __init__(self, root, snapshot, module_names):
        self.root = root
        self.sources = {name: snapshot['scripts/' + name + '.py'] for name in module_names}
        self.loaded = {}

    def find_spec(self, fullname, path=None, target=None):
        if fullname not in self.sources:
            return None
        filename = str(self.root / 'scripts' / (fullname + '.py'))
        return importlib.util.spec_from_loader(fullname, self, origin=filename)

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        name = module.__name__
        raw = self.sources[name]
        filename = str(self.root / 'scripts' / (name + '.py'))
        module.__file__ = filename
        module.__cached__ = None
        exec(compile(raw, filename, 'exec', dont_inherit=True), module.__dict__)
        self.loaded[name] = sha(raw)


def original_assets(raws, case_ids):
    manifest = json.loads(raws[LAUNCH + '/static_asset_manifest.json'])
    need(manifest['source_pin'] == OLD, 'original asset provenance')
    expected = {'planned_assets/' + cid + '/' + name for cid in case_ids
                for name in ('in.mixer', 'deck_meta.json', 'Drum.stl', 'Front.stl', 'Back.stl')}
    rows = manifest['files']
    need(len(rows) == 40 and {r['path'] for r in rows} == expected, 'original forty asset paths')
    assets = {}
    for row in rows:
        raw = raws[LAUNCH + '/' + row['path']]
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'original asset hash')
        assets[row['path'].replace('planned_assets/', 'candidate_assets/', 1)] = raw
    return assets


def new_assets(prep, originals, inventory):
    result = dict(originals)
    generator = next(r['sha256'] for r in inventory['source_dependencies'] if r['path'] == 'scripts/make_mixer_deck.py')
    bindings = []
    for cid in prep.CASE_IDS:
        prefix = 'candidate_assets/' + cid + '/'
        fresh = prep.prepare_case(cid)
        need(fresh['deck'] == originals[prefix + 'in.mixer'], 'regenerated deck differs: ' + cid)
        oldraw = originals[prefix + 'deck_meta.json']
        oldmeta = json.loads(oldraw)
        need(oldmeta['generator_sha256'] != generator, 'new generator hash must differ')
        need(oldraw.count(oldmeta['generator_sha256'].encode('ascii')) == 1, 'one generator hash token')
        newraw = oldraw.replace(oldmeta['generator_sha256'].encode('ascii'), generator.encode('ascii'))
        need(prep._json_exact(json.loads(newraw)) == prep._json_exact(fresh['meta']), 'only generator SHA may change: ' + cid)
        result[prefix + 'deck_meta.json'] = newraw
        binding = prep.validate_case(cid, fresh['deck'], json.loads(newraw))
        need(binding['execution_authorized'] is False and binding['registered'] is None, 'inactive case binding')
        bindings.append(binding)
    return result, bindings


def manifest_for(assets, originals):
    return dict(schema='first8_inactive_copy_assets/1', original_asset_generation_pin=OLD,
                metadata_generation_source_pin=BASE, validation_source_pin=BASE,
                scope='Copied old deck/STL bytes; metadata differs only in generator_sha256',
                execution_authorized=False, operational_activation=False, research_results=0, whole_gate='HOLD',
                files=[dict(path=p, bytes=len(raw), sha256=sha(raw), original_sha256=sha(originals[p]),
                            provenance='current_generator_metadata' if p.endswith('/deck_meta.json') else 'preserved_original_asset_bytes')
                       for p, raw in sorted(assets.items())])


def contract_for(inventory_raw, inventory, manifest_raw, bindings_raw):
    return dict(schema='first8_inactive_current_source_copy/1', status='INACTIVE_PENDING_EXTERNAL_REVIEW',
                validation_source_pin=BASE, metadata_generation_source_pin=BASE,
                original_asset_generation_pin=OLD, previous_validation_source_pin=ACCEPTED,
                original_launch_reference_pin=RECEIPT, whole_gate='HOLD', execution_authorized=False,
                operational_activation=False, registration_changed=False, research_results=0,
                source_inventory_sha256=sha(inventory_raw), asset_manifest_sha256=sha(manifest_raw),
                case_bindings_sha256=sha(bindings_raw),
                files=[dict(path=r['path'], sha256=r['sha256']) for r in inventory['source_dependencies']])


def check_contract(prep, candidate, expected):
    need(prep._json_exact(candidate) == prep._json_exact(expected), 'exact inactive candidate contract')


def check_bundle(prep, bundle, expected_assets, originals, expected_bindings, inventory_raw, inventory):
    asset_paths = {p for p in bundle if p.startswith('candidate_assets/')}
    need(asset_paths == set(expected_assets), 'complete candidate forty assets')
    for cid in prep.CASE_IDS:
        prefix = 'candidate_assets/' + cid + '/'
        binding = prep.validate_case(cid, bundle[prefix + 'in.mixer'], json.loads(bundle[prefix + 'deck_meta.json']))
        need(binding == expected_bindings[list(prep.CASE_IDS).index(cid)], 'regenerated case binding')
    need(all(bundle[p] == expected_assets[p] for p in asset_paths), 'exact copied candidate asset bytes')
    manifest_raw = encode(manifest_for(expected_assets, originals))
    bindings_raw = encode(dict(schema='first8_inactive_case_bindings/1', validation_source_pin=BASE,
                               execution_authorized=False, operational_activation=False,
                               research_results=0, whole_gate='HOLD', cases=expected_bindings))
    need(bundle['candidate_asset_manifest.json'] == manifest_raw, 'candidate asset manifest')
    need(bundle['candidate_bindings.json'] == bindings_raw, 'candidate case bindings')
    expected = contract_for(inventory_raw, inventory, manifest_raw, bindings_raw)
    check_contract(prep, json.loads(bundle['inactive_candidate.json']), expected)
    return expected


def load_bundle(root, asset_paths):
    paths = set(asset_paths) | {'candidate_asset_manifest.json', 'candidate_bindings.json', 'inactive_candidate.json'}
    need({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()} == paths, 'exact candidate bundle file set')
    result = {}
    for path in paths:
        p = root / path
        need(p.is_file() and not p.is_symlink() and root in p.resolve().parents, 'regular candidate path')
        result[path] = p.read_bytes()
    return result


def negative_checks(prep, bundle, expected_assets, originals, bindings, inventory_raw, inventory, expected, snapshot, rows):
    results = []

    def refuse(label, action):
        try:
            action()
        except ValueError as exc:
            results.append(dict(case=label, rejected=True, reason=str(exc)))
        else:
            raise AssertionError('negative accepted: ' + label)

    mutations = {
        'missing_dependency': lambda x: x['files'].pop(),
        'duplicate_dependency': lambda x: x['files'].__setitem__(1, x['files'][0]),
        'dependency_hash': lambda x: x['files'][0].update(sha256='0' * 64),
        'validation_pin': lambda x: x.update(validation_source_pin=ACCEPTED),
        'metadata_pin': lambda x: x.update(metadata_generation_source_pin=OLD),
        'original_provenance': lambda x: x.update(original_asset_generation_pin=BASE),
        'activation': lambda x: x.update(operational_activation=True),
        'execution': lambda x: x.update(execution_authorized=True),
        'registration': lambda x: x.update(registration_changed=True),
        'whole_gate': lambda x: x.update(whole_gate='GO'),
        'results_bool': lambda x: x.update(research_results=False),
        'operating_source_pin': lambda x: x.update(source_pin=BASE),
        'submission_list': lambda x: x.update(allowed_submissions=[]),
        'manifest_binding': lambda x: x.update(asset_manifest_sha256='0' * 64),
        'binding_hash': lambda x: x.update(case_bindings_sha256='0' * 64),
        'inventory_binding': lambda x: x.update(source_inventory_sha256='0' * 64),
    }
    for label, mutation in mutations.items():
        bad = copy.deepcopy(expected)
        mutation(bad)
        refuse(label, lambda bad=bad: check_contract(prep, bad, expected))
    for cid in prep.CASE_IDS:
        bad = dict(bundle)
        p = 'candidate_assets/' + cid + '/deck_meta.json'
        bad[p] = originals[p]
        refuse('old_metadata_' + cid, lambda bad=bad: check_bundle(prep, bad, expected_assets, originals, bindings, inventory_raw, inventory))
    first = 'candidate_assets/' + prep.CASE_IDS[0] + '/'
    for label in ('missing_asset', 'stl_hash', 'rehashed_deck', 'metadata_type', 'bindings', 'manifest'):
        bad = dict(bundle)
        if label == 'missing_asset':
            del bad[first + 'Front.stl']
        elif label == 'stl_hash':
            bad[first + 'Front.stl'] += b'\n'
        elif label == 'rehashed_deck':
            bad[first + 'in.mixer'] += b'\n'
            meta = json.loads(bad[first + 'deck_meta.json'])
            meta.update(deck_sha256=sha(bad[first + 'in.mixer']), deck_bytes=len(bad[first + 'in.mixer']))
            bad[first + 'deck_meta.json'] = encode(meta)
        elif label == 'metadata_type':
            meta = json.loads(bad[first + 'deck_meta.json'])
            meta['revolutions'] = float(meta['revolutions'])
            bad[first + 'deck_meta.json'] = encode(meta)
        elif label == 'bindings':
            value = json.loads(bad['candidate_bindings.json'])
            value['cases'][0]['execution_authorized'] = True
            bad['candidate_bindings.json'] = encode(value)
        else:
            value = json.loads(bad['candidate_asset_manifest.json'])
            value['operational_activation'] = True
            bad['candidate_asset_manifest.json'] = encode(value)
        refuse(label, lambda bad=bad: check_bundle(prep, bad, expected_assets, originals, bindings, inventory_raw, inventory))
    for label in ('missing_source', 'source_bytes', 'test_bytes'):
        bad = dict(snapshot)
        if label == 'missing_source':
            del bad[DEPENDENCIES[0]]
        else:
            bad[TEST if label == 'test_bytes' else DEPENDENCIES[0]] += b'\n'
        refuse(label, lambda bad=bad: check_snapshot(bad, rows))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('old', 'build', 'verify', 'preparation-tests'), required=True)
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--evidence', required=True, help='new directory only')
    args = parser.parse_args()
    supplied = (args.snapshot, args.candidate, args.evidence)
    # Reject all raw tokens before Path can normalize them or any path is queried.
    for path in supplied:
        reject_unsupported_namespace(path)
    snapshot_path, candidate_root, output = (Path(path).absolute() for path in supplied)
    for path in (snapshot_path, candidate_root, output):
        reject_unsupported_namespace(path)
        reject_link_ancestors(path)
    # Check lexical links first, then compare canonical paths before any writes.
    snapshot_root = snapshot_path.resolve(strict=True)
    candidate_root = candidate_root.resolve(strict=False)
    output = output.resolve(strict=False)
    for path in (snapshot_root, candidate_root, output):
        reject_unsupported_namespace(path)
    need(candidate_root != output and candidate_root not in output.parents
         and output not in candidate_root.parents, 'candidate and evidence directories disjoint')
    need(not output.exists(), 'preserve earlier evidence directory')
    need(output != snapshot_root and snapshot_root not in output.parents, 'evidence outside fixed snapshot')
    if args.mode == 'build':
        need(not candidate_root.exists(), 'preserve earlier candidate')
        need(candidate_root != snapshot_root and snapshot_root not in candidate_root.parents
             and candidate_root not in snapshot_root.parents, 'candidate outside fixed snapshot')
    inventory_raw = (Path(__file__).resolve().parent / 'source_inventory.json').read_bytes()
    inventory = json.loads(inventory_raw)
    rows = inventory_rows(inventory)
    denied = install_boundary([output] + ([candidate_root] if args.mode == 'build' else []))
    output.mkdir(parents=True)
    snapshot = snapshot_bytes(snapshot_root, rows)
    sys.dont_write_bytecode = True
    module_names = [Path(p).stem for p in DEPENDENCIES if p.endswith('.py')] + [Path(TEST).stem]
    need(not any(name in sys.modules for name in module_names), 'fresh scientific module process')
    source_finder = VerifiedSourceFinder(snapshot_root, snapshot, module_names)
    sys.meta_path.insert(0, source_finder)
    prep = importlib.import_module('mixer_precal_prepare')
    originals = original_assets(snapshot, prep.CASE_IDS)
    report = dict(mode=args.mode, base_b=BASE, python=platform.python_version(),
                  python_executable_sha256=sha(Path(sys.executable).read_bytes()),
                  source_dependencies_verified=12, launch_files_verified=73, original_assets_verified=40,
                  actual_child_process_calls=0, actual_socket_calls=0, scheduler_calls=0, mpi_calls=0,
                  execution_authorized=False, operational_activation=False, research_results=0, whole_gate='HOLD')
    rc = 0
    if args.mode == 'old':
        class OldMetadataCompatibility(unittest.TestCase):
            def test_all_eight_old_metadata_match_current_source(self):
                for cid in prep.CASE_IDS:
                    with self.subTest(case_id=cid):
                        p = 'candidate_assets/' + cid + '/'
                        try:
                            prep.validate_case(cid, originals[p + 'in.mixer'], json.loads(originals[p + 'deck_meta.json']))
                        except ValueError as exc:
                            self.fail(str(exc))
        result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(OldMetadataCompatibility))
        report.update(methods=result.testsRun, failures=len(result.failures), errors=len(result.errors))
        rc = 0 if result.wasSuccessful() else 1
    elif args.mode == 'preparation-tests':
        tests = importlib.import_module('test_mixer_precal_prepare')
        result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromModule(tests))
        report.update(methods=result.testsRun, failures=len(result.failures), errors=len(result.errors))
        rc = 0 if result.wasSuccessful() else 1
    else:
        assets, bindings = new_assets(prep, originals, inventory)
        manifest_raw = encode(manifest_for(assets, originals))
        bindings_raw = encode(dict(schema='first8_inactive_case_bindings/1', validation_source_pin=BASE,
                                   execution_authorized=False, operational_activation=False,
                                   research_results=0, whole_gate='HOLD', cases=bindings))
        contract = contract_for(inventory_raw, inventory, manifest_raw, bindings_raw)
        if args.mode == 'build':
            candidate_root.mkdir(parents=True)
            bundle = dict(assets, **{'candidate_asset_manifest.json': manifest_raw,
                                     'candidate_bindings.json': bindings_raw, 'inactive_candidate.json': encode(contract)})
            for path, raw in bundle.items():
                target = candidate_root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
        bundle = load_bundle(candidate_root.resolve(strict=True), assets)
        expected = check_bundle(prep, bundle, assets, originals, bindings, inventory_raw, inventory)
        pairs = []
        for level in (1, 2, 3):
            u, c = ('candidate_assets/PRECAL_R1_B%d_%s/' % (level, role) for role in ('U', 'C'))
            value = prep.diff.diff_d2_decks(bundle[u + 'in.mixer'], bundle[c + 'in.mixer'],
                                           json.loads(bundle[u + 'deck_meta.json']), json.loads(bundle[c + 'deck_meta.json']))
            need(value['verdict'] == 'PASS' and value['execution_authorized'] is False, 'D2 pair')
            pairs.append(dict(pair='R1_B%d' % level, verdict=value['verdict'], failures=value['failures']))
        negatives = negative_checks(prep, bundle, assets, originals, bindings, inventory_raw, inventory, expected, snapshot, rows)
        report.update(cases=8, regenerated_deck_bytes_equal=8, metadata_only_generator_sha_changed=8,
                      unchanged_stl_copies=24, bindings=8, pairs=pairs, negative_probes=negatives,
                      candidate_bundle_files=len(bundle), candidate_sha256=sha(bundle['inactive_candidate.json']))
    for name in module_names:
        if name in sys.modules:
            need(Path(sys.modules[name].__file__).resolve() == (snapshot_root / 'scripts' / (name + '.py')).resolve(),
                 'loaded module path: ' + name)
    need(snapshot_bytes(snapshot_root, rows) == snapshot, 'snapshot changed during checks')
    driver = snapshot[LAUNCH + '/submit_one.py.txt'].decode('utf-8')
    need("Path(__file__).resolve().parent/'source_seal.json'" in driver, 'driver sibling seal')
    need("c.get('source_pin')==seal['source_pin']" in driver, 'driver source pin guard')
    need(json.loads(snapshot[LAUNCH + '/source_seal.json'])['source_pin'] == OLD, 'operating draft seal unchanged')
    need(denied == ['subprocess.Popen', 'socket.connect'], 'unexpected process/network attempt')
    report.update(audit_synthetic_denial_probes=denied, real_process_or_socket_attempts=0,
                  source_import_method='Compile verified in-memory source only; no pyc loading',
                  loaded_source_sha256=source_finder.loaded,
                  exact_snapshot_file_graph_verified=True, snapshot_links_rejected=True,
                  driver_boundary_method='Static source inspection only; driver not imported or invoked',
                  driver_still_reads_original_sibling_seal=True, old_source_seal_unchanged=True, rc=rc)
    (output / 'report.json').write_bytes(encode(report))
    print(json.dumps({k: v for k, v in report.items() if k not in ('negative_probes', 'pairs')}, ensure_ascii=False))
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
