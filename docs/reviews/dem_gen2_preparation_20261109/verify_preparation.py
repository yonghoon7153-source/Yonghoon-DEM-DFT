"""Offline synthetic tests and inactive rendering. No engine or network calls.

Invoke with Python -I -B, --repo SNAPSHOT_ROOT --out NEW_EMPTY_DIRECTORY.
Reads exactly the four named new source files; never imports an attachment.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import types
import unittest

FILES = ('make_dem_gen2_decks.py', 'dem_gen2_qualification.py',
         'test_make_dem_gen2_decks.py', 'test_dem_gen2_qualification.py')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    source = {}
    for name in FILES:
        path = args.repo/'scripts'/name
        if path.is_symlink() or not path.is_file():
            raise ValueError('regular exact source required')
        source[name] = path.read_bytes()
    events = []

    def audit(event, arguments):
        if event.startswith(('subprocess.', 'socket.', 'os.exec', 'os.spawn')) or event in ('os.system', 'pty.spawn'):
            events.append(event)
            raise RuntimeError('external process/network prohibited during synthetic verification')
    sys.addaudithook(audit)
    summary = dict(scope='SYNTHETIC_PREPARATION_ONLY', research_results=0,
                   T5='NOT_RUN', T11='NOT_RUN', T12='NOT_RUN', physical_ready=False,
                   source_sha256={n: hashlib.sha256(b).hexdigest() for n, b in source.items()}, suites=[])
    all_ok = True
    for name in FILES[2:]:
        module = types.ModuleType(name[:-3])
        module.__file__ = str(args.repo/'scripts'/name)
        exec(compile(source[name], name, 'exec'), module.__dict__)
        output = io.StringIO()
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(module))
        # Retain original exception text outside repository if any. Passing logs
        # contain only test names/counts and no environment-specific paths.
        (args.out/(name+'.log')).write_text(output.getvalue(), encoding='utf-8', newline='\n')
        summary['suites'].append(dict(name=name, tests=result.testsRun,
                                      failures=len(result.failures), errors=len(result.errors),
                                      skipped=len(result.skipped), passed=result.wasSuccessful()))
        all_ok &= result.wasSuccessful()
    producer = types.ModuleType('candidate_producer')
    producer.__file__ = str(args.repo/'scripts'/FILES[0])
    exec(compile(source[FILES[0]], FILES[0], 'exec'), producer.__dict__)
    summary['synthetic_candidates'] = []
    for material_count in (1, 2, 3):
        candidate = producer.bundle(producer.synthetic_config(material_count))
        for name, value in candidate.items():
            dest = args.out/('synthetic_candidate_'+str(material_count))/name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(value, encoding='utf-8', newline='\n')
        summary['synthetic_candidates'].append(dict(materials=material_count, files=len(candidate)))
    summary['external_process_or_network_attempts'] = events
    summary['original_sources_unchanged'] = all((args.repo/'scripts'/n).read_bytes() == b for n, b in source.items())
    summary['passed'] = bool(all_ok and not events and summary['original_sources_unchanged'])
    (args.out/'verification.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(summary))
    return 0 if summary['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
